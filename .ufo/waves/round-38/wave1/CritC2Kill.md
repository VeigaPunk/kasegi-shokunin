# CritC2Kill — do the C2 counters and the C2 kill rule catch a hollow admission? (round 38, coverage)

Receipt only. No lane file lands from this seat, so there is no deliverable block: every command,
mirror and number below is evidence, and the corrections are proposals for the C2 kill rule in
`.ufo/waves/round-38/claims.json` and for the instruments' owners.

Same-route check against siblings: `CritC2Ground` covers ground/version/province, `ExecC2Junk`
covers manifest-level rejection of the twin's sentences, `ExecC2Harness` covers the harness limbs,
`ExecC2Census`/`ExecC2Binding`/`ExecC2Capture` cover the individual counters on the real files. This
seat tests the **composition**: what the counters in `claims.json` C2 `counting_commands` do when one
link is hollow while every command still exits green.

## Verdict

Two of the seven routes in the item spec are caught by a C2 counter as written (1 and 6). The other
five survive at least one counter configuration (2/4 stub entry, 3a/3b/3c anchors, 5 entry-side
paraphrase, 7 typo name), an eighth route I tested survives outright (raw capture), and the C2 kill
rule has two text gaps that let a hollow admission report fully green (+9, +10):

| # | hollow route | caught by | survivor? |
|---|---|---|---|
| 1 | F21 row without entry | harness `missing-entry`, `source: S055` count, audit `missing=1`, census E11 | no |
| 2 | stub entry (7 lines, no claim, no quote) | **nothing** | **yes** |
| 3a | manifest anchor out of range on a unique quote | **nothing** (`source-recheck` exits 0, prints `anchor=OUT-OF-RANGE`) | **yes** |
| 3b | entry backticked cite past EOF | `anchorcheck` only — no C2 counting command runs it | **yes (against the C2 counters)** |
| 3c | SOURCES.md anchor cell citing lines past EOF | **nothing** | **yes** |
| 4 | harness passing on a stub entry | same as 2: nothing | **yes** |
| 5 | junk twin bypassed by paraphrase | **nothing** — `source-recheck` rejects only quotes that were pinned in a manifest | **yes** |
| 6 | census passing with an indented row | `capture-binding` `rule=no-row` + the id-specific greps, **not** census | no (but census says `ok`) |
| 7 | `knowledge-expected.txt` synced to a misspelled name | **nothing** | **yes** |
| 8 | raw HTML capture instead of normalized text | **nothing** | **yes** |
| +9 | F21 row indented, column-zero decoy F-row takes its slot | **nothing** in the kill rule text (count=21, harness 24/24 both hold) | **yes (kill-rule gap)** |
| +10 | frontier row's `sources` cell ≠ the entry's declared set | **nothing** (the harness prints `ids=` from the entry, not from the row) | **yes (kill-rule gap)** |

The four survivors are all *admission* defects (entry quality, anchor honesty, capture shape, row↔entry
binding); none touches the before-control numbers, so none is a reason to re-open C1.

## Method

Measurement head is the lane HEAD at extraction (read-only `git archive HEAD`; measurements completed
2026-10-26T18:50Z): `700153593eb586c70a6499c8ca225ee4d673bc9b`
(round-38 dispatch commit; the round-38 C2 files are wave-1 deliverables not yet landed). Each mirror
is a `git -C <lane> archive HEAD | tar -x` extraction into `$S`, then the round-38 C2 admission
synthesized exactly as `claims.json` C2 describes it (F21 row, S055 row, entry, `round-38/S055.txt` +
`manifest.json`, expected-list line, knowledge 49→50). The synthetic entry's recheck line `cd`s to the
mirror root so `recheck-audit --root <mirror>` is green for the mirror and not only for the lane
(without that rewrite the mirror reports `cdroot_fail=48` on the 48 inherited entries — a mirror
artifact, not a finding).

Scratch and variants: `/fast/scratch/hyaku/kasegi-r38/CritC2Kill/{base,v1_noentry,v2a_anchor,
v2b_pasteof,v2c_rowanchor,v3_stub,v4_fabricated,v5a_indent,v5b_decoy,v6_typo,v7_rawhtml,v8_rowswap,
v9_rowcell,v10_twininentry}`, each a `cp -a --reflink=auto` of `base`, removed at exit. `TMPDIR` and
`HYAKU_SCRATCH` were both set inside `$S`. No network fetch; no tool installed; no pacman.

Baseline (`base`) — the claim's after-state, all green, F21 named by id:

```
grep -cE '^\| F[0-9]+ \|' corpus/README.md                      -> 21
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 55
grep -cE '^\|[[:space:]]*S055[[:space:]]*\|' corpus/SOURCES.md   -> 1
grep -rlE '^source: S055' corpus/knowledge | wc -l               -> 1
ls corpus/knowledge/*.md | wc -l                                 -> 50
python3 corpus/instruments/frontier-recheck-count.py --root .    -> entries=24 pass=24 exit=0
   PASS     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055           exit=0
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055
   S055:sha256 OK / S055:Q1 OK occurrences=1 anchor=27-ok / Q2 anchor=30-ok / Q3 anchor=33-ok   exit=0
python3 corpus/instruments/capture-binding-check.py --root .     -> records=45 bound=45 unbound=0  exit=0
python3 corpus/instruments/recheck-audit.py --root . --quiet     -> lines=50 ... expect=present
                                                                    expected=50 missing=0 unexpected=0 exit=0
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-26 .
                                                                 -> ok (W04 S028/S029 only)      exit=0
```

Every variant below is a single `cp -a` of that green baseline with one edit; the battery is the nine
commands above. "green" means every one of them exits 0 and keeps its expected value.

## 1 — F21 row without entry (caught)

`v1_noentry`: entry file deleted, row and registry untouched.

```
frontier_rows 21, F21_row 1, registry_rows 55, S055_row 1, knowledge 49
PASS/FAIL: FAIL     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=-  exit=-  problems=missing-entry
entries=24 pass=23 exit=1
recheck-audit: expected=50 missing=1 unexpected=0 exit=1
census: E11 S055 missing used-by corpus/knowledge/csaf-vex-product-status-and-justifications.md   exit=1
grep -rlE '^source: S055' corpus/knowledge | wc -l -> 0
```

Caught four ways. Kill clause that fires: `harness not entries=24 pass=24 exit=0`; also
`audit unexpected != 0 or expected != 50` (as `missing`) and `census exit != 0`. The harness fails
closed through rule E with the row id and path printed (`missing-entry`, not a traceback), so the
receipt can name the limb.

## 2 and 4 — stub entry / harness passing on a stub (survivor)

`v3_stub`: the entry is replaced by its whole 7-line body (title, one `source:` line, one `recheck:`
line, one prose sentence; no claim section, no quote).

```
PASS     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055           exit=0
entries=24 pass=24 exit=0
recheck-audit: strict pass=50/50 ... expected=50 missing=0 unexpected=0 exit=0
source-recheck --source S055: three OK lines, exit=0
capture-binding: records=45 bound=45 unbound=0     exit=0
census: ok, exit=0 ; knowledge 50
```

Everything the kill rule names is green. The harness's `ids=S055` is read from the entry's own
`source:` line, so a stub prints it; the audit's strict limbs (`instrument`, `own`, `cdroot`) are form
limbs and a stub satisfies them. The kill clause `entry absent or failing QUALITY Q1-Q6` is therefore
**unenforced**: `grep -rn 'QUALITY' corpus/instruments/*.py` returns only `source-recheck.py:86/123/191`
(`QUALITY Q9`) and `kill-rule-check.py:64` (`QUALITY R17`); no instrument reads `corpus/QUALITY.md`
Q1–Q6.

## 3a — manifest anchor out of range on a unique quote (survivor)

`v2a_anchor`: `Q1.anchor` changed 27 → 9999; nothing else. The capture is 73 lines.

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055
S055:sha256 OK
S055:Q1 OK occurrences=1 anchor=OUT-OF-RANGE
S055:Q2 OK occurrences=1 anchor=30-ok
S055:Q3 OK occurrences=1 anchor=33-ok
exit=0
```

The instrument prints the bad anchor and still exits 0, because `check_source()` only makes an anchor
verdict fatal when `occurrences > 1` (source-recheck.py, "B2: a non-unique quote passes only when its anchor verifies"). The
kill clause `source-recheck S055 exit != 0` cannot fire. The row anchor cell is prose, so nothing
else looks at it either.

Safety of the obvious correction (make a declared anchor that does not verify fatal in every case):
every committed manifest was re-run and every declared anchor verifies —

```
manifests audited: 14   quote lines with an anchor note: 42   OUT-OF-RANGE/BROKEN/MISSING: 0
```

so the change has zero false positives on the current corpus (and the 42 pins already declare anchors,
so no entry has to be edited).

## 3b — entry backticked cite past EOF (survivor against the C2 counters)

`v2b_pasteof`: the entry's prose cites `` `corpus/source-snapshots/round-38/S055.txt:9999` `` (capture
has 73 lines). All nine C2 commands stay green (harness 24/24, audit exit=0, binding 45/45,
source-recheck exit=0, census ok). The only red is an instrument the C2 kill rule does not name:

```
$ python3 corpus/instruments/anchorcheck.py corpus/knowledge/csaf-vex-product-status-and-justifications.md
PAST-EOF md:24 corpus/source-snapshots/round-38/S055.txt:9999 (file has 73 lines)
exit=1
```

Note the shape seam that makes this cheap to miss: `anchorcheck`'s CITE matches backticked
`path:NN[-MM]` only. The honest F20 entry writes its anchors as `(L247)` inside prose, so
`anchorcheck` reports `0 in-range cite instances` on a real entry — an entry can carry L-anchors that
no instrument ever resolves, whether or not the file is cited.

## 3c — SOURCES.md anchor cell citing lines past EOF (survivor)

`v2c_rowanchor`: the capture is rebuilt as 20 lines (quotes at L2–L4, manifest re-pinned, anchors
2/3/4), while the S055 row keeps its anchor cell (`the product_status categories at lines 26-33 of
capture corpus/source-snapshots/round-38/S055.txt`).

```
source-recheck: S055:Q1 OK anchor=2-ok / Q2 anchor=3-ok / Q3 anchor=4-ok   exit=0
harness entries=24 pass=24 exit=0 ; binding 45/45 ; audit expected=50 missing=0 exit=0 ; census ok exit=0
```

Every counter green while the registry row points at lines that do not exist. A two-line detector on
the row cell + the manifest's own `lines` field discriminates it:

```
$ python3 rowanchor.py <mirror>            # parses 'lines N-M' from the S055 row's anchor cell
base(73-line capture)  rc=0  row_anchor_numbers=[26, 33] record_lines=73 verdict=ok
v2c(20-line capture)   rc=1  row_anchor_numbers=[26, 33] record_lines=20 verdict=ANCHOR-PAST-EOF
```

## 5 — junk twin bypassed by paraphrase (survivor)

The shipped twin (`.ufo/waves/round-38/c2-controls/junk-f21.md`, byte-identical to
`wave1/ExecC2Junk.junk-f21.md`) is rejected only because its four invented sentences are **pinned in a
manifest**; `junk-f21-recheck.txt` shows the mechanism: `S055:J1..J4 MISMATCH reason=quote-not-found`,
exit=1. The entry side is unguarded.

`v10_twininentry`: the twin's four sentences, verbatim, are appended to the entry as a quoted claim
section (`> "CSAF requires every advisory to carry a CVSS v4.0 score." — L10` …). The manifest keeps
the genuine pins.

```
harness: PASS     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055           exit=0
         entries=24 pass=24 exit=0
recheck-audit: expected=50 missing=0 unexpected=0 exit=0
source-recheck --source S055: Q1/Q2/Q3 OK, exit=0
capture-binding: records=45 bound=45 unbound=0 ; census ok
```

Then the same sentences, moved into the manifest, red immediately — the only difference is where the
claim was filed:

```
$ python3 corpus/instruments/source-recheck.py --manifest <scratch>/manifest.json --source S055   # mirror round-38 manifest, its Q1-Q3 replaced by the entry's four twin quotes (ids T1..T4, anchors 10..13); capture bytes unchanged
S055:T1 MISMATCH reason=quote-not-found
S055:T2 MISMATCH reason=quote-not-found
S055:T3 MISMATCH reason=quote-not-found
S055:T4 MISMATCH reason=quote-not-found
exit=1
```

So the kill clause `junk-f21 accepted` proves manifest-level rejection, not that an entry carrying the
twin's text is refused. The twin's rejection is a *form* test as currently demonstrated; a paraphrase
that keeps the fabrication in the entry body passes every counter.

Safety of the correction "every blockquoted sentence ≥25 normalized chars in the entry must occur in a
capture the entry cites": measured over the committed corpus —

```
entries: 50   entries with blockquote quotes + a resolvable capture: 6   quote sentences: 42   matched in capture: 42   unmatched: 0
```

zero false positives today. Run as a receipt check over the four variants it decides them cleanly
(`entryquotes.py <mirror>`: every blockquote ≥25 normalized chars must occur in a capture the entry
cites, and the entry must carry ≥1 claim heading):

```
base                rc=0  captures=['corpus/source-snapshots/round-38/S055.txt'] entry_quotes=3 not_in_capture=0 claims=2 verdict=ok
v3_stub             rc=1  captures=[] entry_quotes=0 not_in_capture=0 claims=0 verdict=HOLLOW
v4_fabricated       rc=1  captures=['corpus/source-snapshots/round-38/S055.txt'] entry_quotes=4 not_in_capture=1 claims=3 verdict=HOLLOW
v10_twininentry     rc=1  captures=['corpus/source-snapshots/round-38/S055.txt'] entry_quotes=7 not_in_capture=4 claims=3 verdict=HOLLOW
```

(`v10`'s four unmatched sentences are exactly the twin's `J1..J4`.)

## 6 — census passing with an indented row (caught, but not by census)

`v5a_indent`: the S055 row is indented two spaces. `sources-census.sh` documents and honours "0–3
leading ASCII spaces before Markdown rows", the round-38 counters are column-zero anchored:

```
census validate -> ok, exit=0    census census -> v5a_indent rows 55
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 54
grep -cE '^\|[[:space:]]*S055[[:space:]]*\|' corpus/SOURCES.md       -> 0
capture-binding: FAIL rule=no-row record=S055 dir=round-38 ; records=45 bound=44 unbound=1 ; exit=1
```

Census says `ok` with 55 rows; `capture-binding` (ROW_RE is column-zero) refuses the record. That is the
catch, not `census exit != 0`.

`v5b_decoy` closes the obvious dodge: S055 indented, a column-zero decoy S056 row carrying a real
11-column row, and the capture record renamed to S056 with the entry declaring S056.

```
census validate -> ok exit=0 ; census census -> rows 56
grep '^| S[0-9]{3,} |' -> 55 ; grep 'S055 row' -> 0 ; grep -rl '^source: S055' -> 0
harness: PASS     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S056 ; entries=24 pass=24 exit=0
capture-binding: records=45 bound=45 unbound=0 ; audit expected=50 missing=0 exit=0
source-recheck --source S055 -> S055:source UNAVAILABLE reason=not-listed ; exit=2
```

Under only the counts named in `claims.json` (rows 55, `source: S055` = 1) this variant reds on the
`source: S055` grep; the id-scoped `source-recheck --source S055` also reds (exit=2). Both are
load-bearing and neither is spelled out in the kill rule: a receipt that ran `source-recheck` over the
whole manifest instead of `--source S055` would pass it.

## 7 — `knowledge-expected.txt` synced to a misspelled name (survivor)

`v6_typo`: `csaf-vex-product-status-and-justifications.md` → `…justificaton.md` (one `s` dropped),
with `knowledge-expected.txt`, the F21 README cell and the S055 `used-by` cell synced.

```
harness: PASS     F21  knowledge/csaf-vex-product-status-and-justificaton.md ids=S055  exit=0
         entries=24 pass=24 exit=0
recheck-audit: expected=50 missing=0 unexpected=0 exit=0     (the expected list is the anchor, so it drifted with the file)
census validate -> ok exit=0 ; knowledge 50 ; entry_cites_S055 1 ; binding 45/45 ; source-recheck exit=0
anchorcheck: == corpus/knowledge/csaf-vex-product-status-and-justificaton.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0 ; RC=0
```

Nothing catches a misspelling, because the expected list, the README cell and the `used-by` cell are
all editable in the same commit — set equality is self-consistent. The cheap external anchor is the
frozen claim itself, which names the path literally:

```
$ grep -o 'corpus/knowledge/[a-z0-9-]*\.md' .ufo/waves/round-38/claims.json | sort -u
corpus/knowledge/considerthese-proposals-ledger.md
corpus/knowledge/csaf-vex-product-status-and-justifications.md
$ for p in $(grep -o 'corpus/knowledge/[a-z0-9-]*\.md' .ufo/waves/round-38/claims.json | sort -u); do test -f "$p" && echo "present $p" || echo "MISSING $p"; done
base     -> present corpus/knowledge/considerthese-proposals-ledger.md; present corpus/knowledge/csaf-vex-product-status-and-justifications.md
v6_typo  -> present corpus/knowledge/considerthese-proposals-ledger.md; MISSING corpus/knowledge/csaf-vex-product-status-and-justifications.md
```

## 8 — capture of the raw HTML instead of the normalized text (survivor)

`v7_rawhtml`: `S055.txt` replaced by 517 bytes of raw HTML (`<!DOCTYPE html>`, `<html>`, `<div>`,
`<p>` wrappers, `<footer>&copy;`), sha re-pinned in the manifest, anchors moved to the real lines.

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055
S055:sha256 OK
S055:Q1 OK occurrences=1 anchor=4-ok
S055:Q2 OK occurrences=1 anchor=5-ok
S055:Q3 OK occurrences=1 anchor=6-ok
exit=0
capture-binding 45/45 ; harness 24/24 ; audit exit=0 ; census ok
```

`capture-binding` binds files to records by name and URL, not by content (its own "Known limits"); the
manifest's `normalized` field is prose. `raw_sha256` is not a check either — it exists in 1 of 7 modern
manifests (`round-37` only), so requiring it would red rounds 30–36.

Safety of a residue rule ("a capture may not contain `<!doctype`, `<html`, `<body`, `<div`, `<p[ >]`,
`<script`, or HTML entities"), measured over every committed capture:

```
captures: 46   doctype 0   html-tag 0   body 0   div 0   p-tag 0   script 0   entity 0   <u>-markup 1 (round-23/S030.txt)
```

Zero false positives; the one `<u>`-markup capture is the enrichment the instruments already normalize
(`MARKUP_RE`), so `<u>` must stay legal if this rule is added.

## +9 — indented F21 row with a column-zero decoy F-row (kill-rule gap)

`v8_rowswap`: F21 indented two spaces; a new column-zero `| F22 | … | S055 |` row points at
`knowledge/f22-shadow.md` (a second entry kept outside `corpus/knowledge/`, so the knowledge count and
the audit glob do not move).

```
grep -cE '^\| F[0-9]+ \|' corpus/README.md  -> 21          (satisfies 'frontier rows != 21')
grep -cE '^\| F21 \|' corpus/README.md      -> 0
harness: entries=24 pass=24 exit=0  with  PASS F22  knowledge/f22-shadow.md  ids=S055
         (no F21 line at all)
binding 45/45 ; audit expected=50 missing=0 exit=0 ; census ok ; knowledge 50 ; source-recheck exit=0
```

Both totals the kill rule names are green while F21 was never admitted; the harness reads rows with
`^\|` at column zero, exactly like the count. The predicate's "incl PASS F21 ids=S055" is not in the
kill rule. The decoy prints `ids=S055` because that comes from its entry, so even a
`grep 'PASS F21'` alone would not be enough if the row id were swapped; the id and the row cell must
both be bound.

## +10 — the row's `sources` cell disagreeing with the entry (kill-rule gap)

`v9_rowcell`: F21's fifth cell changed `S055` → `S054`; the entry still declares S055.

```
harness: PASS     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055           exit=0   (ids come from the entry, not the row)
row_sources_cell=[S054]
binding 45/45 ; audit exit=0 ; census ok ; all other counters green
```

Nothing compares the row cell to the entry's declared set. Safety of that comparison over the real
table:

```
rows: 21   rows whose sources cell != entry declared set (header `source:` ∪ evidence bullets): 0
```

## Impacted axes

`coverage` only (C2). Routes 2/3a/3b/3c/5/7/8/+/9/+/10 are admission-honesty seams; they change no
before-control value, and none weakens C1. The two instrument changes proposed below are lane files
owned by other seats; this receipt does not land them.

## Smallest safe corrections, in order

1. **Bind the row id and the row cell in the kill rule (kills +9, +10).** Add to the C2
   `counting_commands` and kill rule, verbatim:
   - `grep -cE '^\| F21 \|' corpus/README.md -> 1`
   - `grep -cE '^PASS +F21 .*ids=S055' <harness output> -> 1`
   - `grep -cE '^\|[[:space:]]*S055[[:space:]]*\|' corpus/SOURCES.md -> 1` (the before-controls grep,
     restored to the after measurement)
   - row-cell equality: the fifth cell of the F21 row must equal the entry's declared id set (0
     mismatches across the 21 real rows, so this can be stated as a zero-tolerance measurement).
2. **Name the id-scoped selector and the entry grep (kills 6/`v5b`).** Keep
   `source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055` (never a whole-manifest run) and
   `grep -rlE '^source: S055' corpus/knowledge | wc -l -> 1` in the kill rule, and state that
   `census exit 0` is not evidence that a row is visible to the column-zero counters (measured:
   census `rows 55`, counter `54`, `capture-binding rule=no-row`).
3. **Make a declared anchor fatal when it does not verify, and run `anchorcheck` on the F21 entry
   (kills 3a/3b).** The `source-recheck.py` change is one condition (`occurrences > 1 and anchor_verdict_result != "ok"` →
   `anchor_verdict_result != "ok"`); every one of the 42 committed pins already verifies, so nothing
   reds. `bash corpus/instruments/anchorcheck.py corpus/knowledge/csaf-vex-product-status-and-justifications.md`
   exits non-zero on PAST-EOF and belongs in the receipt.
4. **Add the row-anchor bound (kills 3c).** The round's new SOURCES row anchor cell's `lines N-M`
   numbers must be ≤ its record's `lines`; two lines of parsing, demonstrated above on base vs v2c.
5. **Add the entry-quote limb (kills 2/4/5 and the stub side).** In the receipt, not necessarily as a
   new committed instrument: every blockquoted sentence ≥25 normalized chars in the F21 entry must
   occur in the S055 capture (measured 42/42 for today's entries), plus at least one claim heading.
   The cheapest strong form reuses the twin: keep `junk-f21.md`'s four sentences and additionally
   re-run `source-recheck` with a manifest built from the **entry's own** quotes, which must exit 1 —
   the run in this receipt shows it does (`T1..T4 quote-not-found`).
6. **Bind the entry path to the frozen claim literal (kills 7).** `grep -o
   'corpus/knowledge/[a-z0-9-]*\.md' .ufo/waves/round-38/claims.json` → `test -f` each; demonstrated
   to pass on the honest tree and to red the typo variant.
7. **Add the capture residue rule (kills 8).** `<!doctype`, `<html`, `<body`, `<div`, `<p[ >]`,
   `<script`, HTML entities → fail; `<u>` stays legal. 46/46 committed captures clean; 1 uses `<u>`.
   Cheapest home is `source-recheck.py`'s `check_source()` next to the sha256 check (reason
   `capture-not-normalized`), because that is the instrument every entry's recheck already runs.

Items 1–2 and 4–6 are receipt-text changes the L1 can make; items 3 and 7 are two-line instrument
edits owned by the instrument seats. None changes the C2 numbers already claimed.

## Honest limits

- The synthesized admission is mine, not the wave-1 deliverable; the routes tested are counter
  mechanics, which do not depend on the bytes of the real S055 capture. Where a route needed content
  (3b, 3c, 8) the capture was rebuilt and re-pinned in the mirror so the counter could be green *while*
  the defect was present — the point of the test.
- `v6_typo`'s anchorcheck line is `0 in-range cite instances`, i.e. the honest entry has no backticked
  `path:NN` cite either; the typo is invisible to that instrument for the same reason the anchor route
  is.
- The row-anchor detector in item 4 is a regex over one cell; it is a receipt check, not a proposed
  committed instrument.
- Scratch removed at exit (`trap 'rm -rf -- "$S"' EXIT`), after no copy was needed outside the wave dir.
