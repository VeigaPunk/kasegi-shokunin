# CritInstruments — round-42 wave-1 attack receipt (C2 instrument assumptions)

Seat: CritInstruments (critic). Scope per dispatch: attack the C2 instrument
assumptions — `corpus/instruments/source-recheck.py` (find the mutation it
cannot catch) and `corpus/instruments/capture-binding-check.py` (blind spots
beyond the already-routed missing-path/URL-variant family). Receipt-only item;
no deliverable bytes. Lane base 5053a7f46de35784cff4b56756906e9014a38276;
frozen claims read first (claims.json r42); instruments audited at lane tip.

Read first: `.ufo/waves/round-42/claims.json` (C1 kill rule names seven repair
families; C2 kill rule requires S064's capture to *pass* source-recheck and its
manifest record to be bound). Also read end-to-end: `source-recheck.py`,
`capture-binding-check.py`, `recheck-audit.py`, `frontier-recheck-count.py`,
`anchorcheck.py`, `corpus/SOURCES.md` row shape, round-41 manifest + entry,
r41-verifier spotcheck §5.

Scratch: `/fast/scratch/hyaku/kasegi-r42/CritInstruments/` (removed at exit —
see foot). Disk guard green before work. No tools installed (python3/curl
already present; channel n/a).

## Verdict up front

Two instruments each hold internally, but the chain has **content-blind
joints**: nothing anywhere binds *URL → capture bytes*, *manifest quotes → the
claims an entry actually makes*, or *declared-anchor truth on unique quotes*.
Every escape below was demonstrated live against the current committed
instrument bytes (fixture lane trees under scratch; transcripts verbatim).

---

## F1 (PRIMARY, source-recheck): a declared `anchor` on a unique-occurrence quote is decorative — a fabricated anchor prints `anchor=N-BROKEN` and still exits 0

`anchor_verdict()` returns `"broken"` for any declared anchor whose 4-line
window lacks the normalized quote, but `check_source()` only escalates to
MISMATCH when `occurrences > 1 and verdict != "ok"`. For a quote occurring
once, `anchor` is **reported yet never fatal** — a manifest can pin a quote to
a line that does not contain it and still produce an all-OK transcript. The
entry's `location:` prose (`"L330-L331; Section 3 …"`) is likewise unchecked
free text.

Demo (fixture `pay.txt`, quote occurs once on line 6; declared anchor=2):

```
### d1.json exit 0
S900:sha256 OK
S900:Q1 OK occurrences=1 anchor=2-BROKEN     <-- fabricated anchor, exit 0
```

Why it matters for C2: the S064 manifest record "passing source-recheck" is
the claim's evidence gate. A wrong anchor on a single-occurrence quote —
exactly the kind a hurried capture writes — sails through as
`anchor=N-BROKEN` on an `OK` line. The transcript *admits* the break; the
exit code denies it.

Smallest safe correction: in `check_source`, treat any declared-anchor
verdict outside `{unique, ok}` as a failure — i.e. extend the existing gate
to `if (occurrences > 1 or assertion.get("anchor") is not None) and
anchor_verdict_result != "ok"`. One-line shape change; keeps anchor-less
unique quotes passing.

## F2 (PRIMARY, source-recheck): the anchor window tolerates ±3 lines of drift, and does not resolve *which* occurrence it names

`window = raw_lines[max(0,anchor-1):anchor+3]` (1-based lines `anchor` through
`anchor+3`), so for a non-unique quote the declared anchor verifies when the
quote sits on `anchor`, `anchor+1`, or `anchor+2` — an anchor pointing 3 lines
above the quote is `anchor=N-ok`. And since the check is "quote in window",
an anchor at the *second* occurrence's line also verifies even if the pin was
meant for the first: the declared anchor never has to name the occurrence it
claims.

Demo (quote on lines 4 and 6):

```
### d2.json  (anchor=1, quote not on line 1 at all)   exit 0   anchor=1-ok
### d2b.json (anchor=6, i.e. the OTHER occurrence)    exit 0   anchor=6-ok
```

Smallest safe correction: require the quote to *begin within the anchor line
itself* (check `expected in normalize(raw_lines[anchor-1])` first, falling
back to the joined window only for multi-line quotes whose span legitimately
crosses lines — flag `anchor-offset=N` when it does).

## F3 (PRIMARY, source-recheck): quote↔record and capture↔document assignment is unchecked — identical captures under distinct ids, boilerplate quote swaps, and url-vs-bytes all pass

The instrument verifies manifest-internal consistency only: `path` exists,
`sha256` matches the file on disk, `quotes` occur in that file. Three
concrete escapes, all demonstrated:

```
### d3.json — two quote ids pinning the SAME sentence ("pin-count inflation")
S900:Q1 OK occurrences=1
S900:Q2 OK occurrences=1          exit 0   (dedup is on assertion id, never quote text)

### d4.json — S900.txt and S901.txt byte-identical, two records, two different urls
S900:sha256 OK / S900:Q1 OK / S901:sha256 OK / S901:Q1 OK   exit 0
```

- **Twin captures (d4):** one document registered as two sources — sha256 pins
  match each file, quotes occur in each file, and `capture-binding-check.py`
  binds each record because the *urls differ* (`multi_row_url` only counts a
  shared url across rows, never shared bytes). Coverage axis impact: a "new"
  registry row can be a re-capture of a document the lane already holds, and
  both instruments print green. This is the live form of the prompt's
  "manifest sha256 matching a DIFFERENT capture" — sha256 binds the manifest
  to *a* file, never to *the* document at `url`.
- **Quote-swap on shared text:** the `quotes` list belongs to the record, but
  the quote text is matched against the capture only. Swapping two records'
  `quotes` blocks escapes detection whenever the swapped text occurs in both
  captures (boilerplate, license headers, RFC front-matter). What is actually
  unchecked is whether the quote bears on *this* document — purely local
  instruments cannot prove that; they can only refuse *identical-byte*
  duplicates and *identical-text* pins.
- **Whole-document substitution:** swap `S064.txt` for a different document
  containing the same pinned substrings, recompute sha256 — pass. By design
  (bytes-vs-URL is unverifiable offline); the C2 receipt records this, but no
  instrument counts it.

Smallest safe correction: per-manifest (and per-tree) duplicate-content
guard — emit `note=duplicate-capture` (or fail) when two records share a
`sha256`, and dedup quotes on normalized text: `if normalize(quote) in seen_text:
reason=duplicate-quote-text`. Both are ~5 lines inside `check_source`'s
existing loops.

## F4 (source-recheck, secondary): `--source` masking hides sibling-record rot; minimum evidence floor is one 12-char normalized substring

- `recheck(manifest, source_id)` filters to the named record **before**
  `check_source` — a manifest whose *other* records are malformed reports only
  the selected record's verdicts. An entry's recheck line (`--source S064`)
  therefore never re-validates the manifest it lives beside; rot in a sibling
  record is invisible to the per-entry gate (caught only by a whole-manifest
  run, which no counting command performs — see F10).
- `MIN_QUOTE_CHARS = 12` on normalized text: a single 12-character substring
  (`"Apache License"` = 14 normalized chars, `"Version 2.0"` = 11 → fails,
  `"License, Version"` = 16 → passes) is the entire evidence floor — one such
  quote makes a record "passing source-recheck". Weak-evidence floor, not a
  logic bug; worth a named bound (e.g. ≥2 quotes or ≥40 normalized chars) if
  the claim wants "passing" to mean "evidenced".
- `<u>`/`</u>` markup is stripped from *both* sides (declared behavior); quote
  text uniqueness is enforced on `id`, not text (see F3).

## F5 (PRIMARY, capture-binding): the legacy exemption is forgeable by directory name — a record created this round in a `round-<32` dir skips `fetched_utc`

`provenance_ok()` grants the archival exemption purely by
`parse_round(dirname) < MODERN_ROUND` — it never checks whether the *record*
(or its manifest) is actually old. A round-42 record dropped into
`corpus/source-snapshots/round-1/` with `"archival": true` binds with no
fetch timestamp:

```
### B4 archival in fake-legacy dir round-1: exit 0
MANIFEST round-1 records=1 url_bound=1 fetched=0 archival=1
records=1 bound=1 unbound=0
```

The lane's real legacy dirs are fixed (`round-23,24,25,26,28,29,30,31` — no
round-1/27 dirs exist; anything named `round-<32` other than that set is
new). False-provenance class: a capture with no fetch instant presents as
"bound".

Smallest safe correction: replace `round_no < MODERN_ROUND` with membership
in the enumerated legacy-dir set (`{"round-23","round-24","round-25",
"round-26","round-28","round-29","round-30","round-31"}` — the dirs that
existed when rule C was introduced). Any other directory, parseable or not,
is modern.

## F6 (capture-binding): rule D (`dup-record`) is per-manifest — the same record id in two different snapshot dirs binds twice, invisibly

`duplicate_records(records)` scans one manifest's `sources[]`. Two manifests
each carrying `{"id":"S001",...}` — same row, double-counted record:

```
### B3 cross-manifest dup id: exit 0
MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-42 records=1 url_bound=1 fetched=1 archival=0
records=2 bound=2 unbound=0
```

`records=56` in the C2 counter is "records seen", not "distinct ids seen"; a
duplicated record inflates `bound` while documenting one capture. Smallest
correction: `seen_ids` dict across the manifest loop; a repeat emits
`FAIL rule=dup-record-id-across-manifests`.

## F7 (capture-binding): registry rows are found by shape alone — a `| S0xx |`-shaped line inside an HTML comment or fence satisfies rule B1–B5

`ROW_RE = r"^\|\s*(S\d{3,})\s*\|"` runs on every line of SOURCES.md with no
comment/fence/table-context awareness. A record binds to a "row" that exists
only inside `<!-- -->` (a commented-out rejected row, a doc example):

```
### B5 row inside HTML comment: exit 0
records=1 bound=1 unbound=0
```

The claim's own registry counter (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`)
shares this blindness, so a spoofed line inflates **both** the instrument's
registry and the claim's 63→64 count in the same direction — self-consistent
forgery. Smallest correction: skip fenced/commented regions while scanning
(simple state machine over `<!--`/`-->` and ```` ``` ````), or require the row
to appear after the `| id |` header inside the table block. **Family note:**
this is a URL/row-binding variant — plausibly inside the named F-BIND family
(see "Kill-clause routing" below); a J-check limb with a comment-spoofed row
would pin it.

## F8 (capture-binding): `fetched_utc` needs only well-formedness — year 2030 (and any date after the fetch it claims) binds

`classify_fetched()` validates shape (`Z`/`+00:00`, real calendar instant) and
nothing more. `2030-01-01T00:00:00Z` on a round-42 record:

```
### B7 fetched_utc year 2030: exit 0
MANIFEST round-42 records=1 url_bound=1 fetched=1 archival=0
```

No instrument cross-checks `fetched_utc` against the record's commit instant,
the round directory's existence, or `http.fetched_utc`/`capture_url` fields
the manifest already carries (a record can say `url=X, capture_url=Y` — only
`url` is read). Smallest correction: advisory bound vs. a reference instant
(the manifest's own commit time or an explicit `--now`), or an r42-suite limb
comparing `fetched_utc` to the capture commit's committer date.

## F9 (capture-binding): `bound=` counts id+url+timestamp, not a verified record — a record with no `sha256`, no `quotes`, no file check, empty `sources: []` all leave `bound` intact

`bind_record` reads `id`, `url`, `fetched_utc`, `archival` only. A record
missing every content pin binds; `"sources": []` yields `records=0 bound=0`
(a manifest saying nothing passes); `schema_version` is unread here while
`source-recheck` hard-requires `1` — the same manifest can be `bound` by one
instrument and `UNAVAILABLE` to the other. All three are documented
split-of-duties, but they make `bound=56` a weaker sentence than the claim's
prose ("manifest record unbound" as a kill clause) suggests: `bound=56`
guarantees 56 id/url/timestamp triples, not 56 verified captures. Smallest
correction: a joint counter — the C2 counting set (or the J-check suite)
should run `source-recheck.py` over **every** bound record (whole-manifest
pass), making `bound` imply `recheckable`.

## F10 (PRIMARY, composition/kill-rule hazard): for non-frontier records nothing executes the recheck, and `recheck-audit.py` reports a *failing* recheck as `gated` PASS — demonstrated exit 0 over a corrupted capture

`recheck-audit.py` verifies a recheck *line's form* (parse/cwd/path limbs),
never its verdict: `class="gated"` — the line runs and fails — still counts
as PASS (frozen by design for absent external bases). `frontier-recheck-count.py`
*does* execute the entry's line and require exit 0 (rule D) — but only for
entries behind `admitted` frontier rows, bound via the README entry-path
column. Non-frontier records (any registry row whose source feeds a
non-frontier entry) are rechecked by **nobody**: `bound` for them is pure
paper.

Demonstrated on a 2-entry fixture lane (`bad.md`'s capture sha256 corrupted;
the entry's recheck is a verbatim `source-recheck --source S901` line):

```
### recheck-audit exit 0
bad.md   frozen=111 strict=111111 lane=1   foreign=1   gated    PASS
good.md  frozen=111 strict=111111 lane=0   foreign=0   executes PASS
lines=2 total=2 pass=2 fail-closed=1 ... exit=0
expect=present expected=2 missing=0 unexpected=0 exit=0
--- direct source-recheck on bad record ---
exit 1
S901:sha256 MISMATCH expected=ba65… actual=c2f7…
```

C2 impact is conditional but sharp: the frozen counting set contains **no
direct `source-recheck` invocation** — `capture-binding-check → bound`,
`recheck-audit → expected=61`, `frontier-recheck → pass=28`. If the F25 row's
entry is the S064 entry (the natural wiring, per the F24 precedent where the
admitted row names `knowledge/rfc-9116-security-txt.md` whose recheck carries
`--source S063`), the frontier harness transitively executes S064's recheck
and the chain holds. If F25's entry declares a *different* source and no
frontier-admitted entry cites S064, every counting command can print green
while S064's record fails source-recheck — the kill clause "its capture
failing source-recheck" is then unobservable to the frozen counters and
depends on the judge running an unlisted command. Smallest safe correction:
C2 gate runs `source-recheck.py --manifest …/round-42/manifest.json` (no
`--source`) once; or `recheck-audit` gains a `--require-executes` mode that
fails when a `source-recheck`-line is `gated` (a capture mismatch is not an
absent base — the `gated` class conflates them today).

## Holds (checked, not findings)

- Rejected-row anchoring currently binds correctly: real rejected rows keep
  `status` at `parts[7]` (`| S022 | … | rejected | 2026-10-19 | …`); B3 fires.
  The fragility is *prospective*: `==` vs a literal is case- and
  position-brittle — `Rejected`, `rejected `, or a column insert silently
  reverses the rule (demonstrated `### B1`/`### B2`, both exit 0). Correct:
  compare `status.strip().lower()` and require membership in the row's status
  vocabulary rather than a literal at a fixed index.
```
### B1 Rejected-capital-R: exit 0   (status cell reads "Rejected"; rule B3 needs exact "rejected")
MANIFEST round-42 records=1 url_bound=1 fetched=1 archival=0
records=1 bound=1 unbound=0
### B2 column-shifted rejected: exit 0   (row with 9 cells: "rejected" at index 8, parts[7] is "t")
records=1 bound=1 unbound=0
```
- `no-snapshot-tree` guard exists (`UNAVAILABLE … exit 2`) — the
  vacuous-pass route I probed (B6) is closed.
- `round-30/inner` nested dirs inherit the parent's round
  (`dirname.split("/",1)[0]`) — not a legacy-exemption hole.
- Orphan accounting, `orphan-declared-missing`, double-https rows,
  per-file binding, `quote-too-short-to-be-evidence`,
  `outside-manifest-directory` containment, the `gated`/`fail-closed`
  distinction for base-less entries — all verified working as documented.

## Kill-clause routing

Of the escapes above, **F7 (comment/prose-spoofed registry row) is the one
most plausibly inside the named F-BIND family** ("capture-binding
missing-path/URL variants"): it is a row/URL-shape variant of the same
binding rule the routed queue already names, and a committed artifact showing
the current suite accepting it could read as in-family under the C1 kill
rule. F5 (archival-forgery), F8 (unbounded fetched_utc) are provenance
variants — adjacent to F-BIND but arguably new. F1–F4 are source-recheck
interior (no named family covers it); F10 is a counting-set composition gap,
the strongest evidence-quality risk to C2's "passing source-recheck" claim.
Recommend the J-check owner add limbs for F5/F6/F7 (cheap fixture rows) and
the C2 gate add the one whole-manifest `source-recheck` invocation (F10) —
all are additive limbs, nothing already-green needs to change.

Axes: `depth:verifiability` + (anchors meaningless when declared, recheck
form-vs-verdict conflation); `coverage` + (twin-capture double-registration,
spoofed-row inflation of the registry counter). No axis harmed by repairing
any limb; each repair is a stricter rejection on inputs that currently pass.

Environment: python3 3.x fixtures only; `trap 'rm -rf -- "$S"'` — scratch
`/fast/scratch/hyaku/kasegi-r42/CritInstruments/` removed before yield.
