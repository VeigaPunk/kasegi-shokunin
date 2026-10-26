# CritC2Kill — attack on the C2 counters and the C2 kill rule (round 37, coverage)

Seat: attack critic, C2. Leaf seat: no subagent, no lane edit, no mutating git, no peer broadcast, no
tool installed. Measurement instant `2026-10-26T17:11–17:25Z`; lane head
`b362068195d5489aa94b31e6ec8f880c367e0ba0`; base `b56a41680cefd391868c1c370dc063c69d827e7d` exported
with `git archive` into `/fast/scratch/hyaku/kasegi-r37/CritC2Kill/` (removed before yield). The only
lane file written is this receipt.

The C2 artifacts are **not landed** at that instant (`S054` rows 0, `round-37/` absent, `ssvc-*` entry
absent, `.ufo/waves/round-37/c2-controls/` holds only `before.txt`). Every attack is therefore a fixture
lane: a copy of the base export, `cd` paths retargeted to the fixture root, the planned landing applied
on top, then the **committed** instruments run against it. That is the useful direction: the matrix says
what the frozen C2 kill rule must reject, and the six routes the item names are the tests.

Instrument code measured (unmodified copies; digests unchanged from round 36, so no repair landed):

```
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  corpus/instruments/frontier-recheck-count.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30  scripts/sources-census.sh (fleet, read-only)
```

Base state of the export, measured: `frontier=19`, `S rows=53`, `knowledge=48`, harness
`entries=22 pass=22 exit=0`, binding `records=43 bound=43 unbound=0 exit=0`, census `W04 S028, W04
S029, ok exit=0`.

## 1. Positive control: the honest landing passes every C2 command

Fixture `a0c`: tutorial capture (erratum-1 URL), S054 row (11 cells, tier A, mined, `on-release`,
used-by = the entry), F20 row `admitted`, substantive entry (blockquote at L247), expected list 49.

```
PASS     F20  corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054 exit=0
entries=23 pass=23 exit=0
S054:sha256 OK / S054:Q1 OK occurrences=1 anchor=247-ok          (source-recheck exit 0)
MANIFEST round-37 records=1 url_bound=1 fetched=1 archival=0
records=44 bound=44 unbound=0                                    (exit 0)
lines=49 total=49 pass=49 ... expect=present expected=49 missing=0 unexpected=0 exit=0
sub-row W04 S028 / W04 S029 / ok                                 (census exit 0)
frontier=20 S_rows=54 citing_S054=1 knowledge=49
```

So **C2 is achievable on the current bytes** and my rig is not the source of the reds below. The
capture I fetched at `17:19:30Z` is byte-identical to ExecC2JunkControl's `17:02:19Z` fetch
(`snapshot_bytes=32623`, `lines=518`, sha256 `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21`);
both our home-page fetches are also identical (`7730` bytes / `a66133152a5bb8b760e6aef1c316b46777abc5dda2c1d957410ceccbce58bb56`).
Two independent fetches are the only capture-authenticity evidence this round has (see A8b and M4).

## 2. Attack matrix

Rig per row: `cp -a` of the export → retarget `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin` to
the fixture root in all `corpus/knowledge/*.md` → apply the construction → run

```
python3 corpus/instruments/frontier-recheck-count.py --root <fx>
python3 corpus/instruments/source-recheck.py --manifest <fx>/corpus/source-snapshots/round-37/manifest.json --source S054
python3 corpus/instruments/capture-binding-check.py --root <fx>
python3 corpus/instruments/recheck-audit.py --quiet --root <fx> --cdroot <fx>
scripts/sources-census.sh validate --file <fx>/corpus/SOURCES.md --today 2026-10-26
grep -cE '^\| F[0-9]+ \|' corpus/README.md ; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
grep -rlE '^source: S054 ' corpus/knowledge | wc -l ; ls corpus/knowledge/*.md | wc -l
```

| # | construction | harness | src-recheck S054 | binding | audit | census | counts (F/S/cite/K) | caught by |
|---|---|---|---|---|---|---|---|---|
| A1 | F20 row, **entry file absent** | `entries=23 pass=22 exit=1`, `FAIL F20 … problems=missing-entry` | exit 0 | 44/44 exit 0 | — | **exit 1** `E11 S054 missing used-by` (because used-by named the absent entry) | 20/54/**0**/48 | K4 (harness), K2/C2 (cite count) |
| A2 | S054 row + declaring entry, **no capture dir** | `FAIL F20 problems=manifest-unreadable` 22/23 | `exit=2 manifest UNAVAILABLE reason=missing` | **43/43 exit 0** | — | exit 0 | 20/54/1/49 | K5, K4; binding blind |
| A2b | capture present, **manifest url = first.org/epss** | 23/23 exit 0 | exit 0 | **exit 1 `FAIL rule=url-mismatch record=S054 row=S054`** | — | exit 0 | 20/54/1/49 | **K8 only** |
| A2c | manifest record present, **capture file absent** | `FAIL F20 problems=recheck-exit-2` | `exit=2 S054:source UNAVAILABLE reason=missing` | **44/44 exit 0** | — | exit 0 | 20/54/1/49 | K5, K4; binding blind (r36 K2 open) |
| A3c | **4-line stub entry** on the erratum page: `# SSVC` / `source: S054 — <url>` / `recheck: … --source S054` / `S054.` (22 words total) | **23/23 exit 0** | exit 0 | 44/44 exit 0 | **49/49 exit 0** | exit 0 | 20/54/1/49 | **nothing** |
| A3b | same stub **without** the `S054` prose token | `FAIL F20 problems=selection-not-cited-by-entry` | exit 0 | 44/44 | — | 0 | 20/54/1/49 | K4 (the only body requirement that exists) |
| A4 | **fabricated body admitted as F20**: "SSVC guarantees a fixed remediation deadline … replaces CVSS severity scoring", manifest pins two genuine quotes | **23/23 exit 0** | exit 0 | 44/44 exit 0 | **49/49 exit 0** | exit 0 | 20/54/1/49 | **nothing** |
| A4b | the same fabricated sentence **as a pinned quote** | — | `exit=1 S054:J1 MISMATCH reason=quote-not-found` | — | — | — | — | K7 mechanism (quote channel only) |
| A4d | one **57-char tutorial sentence** as the sole pin | — | `exit=0 Q1 OK occurrences=1` | — | — | — | — | — (no substance floor) |
| A4d'' | the bare 12-char word **`concentrated`** (and `Utility (ssvc`, 13 chars) as the sole pin | — | `exit=0 Q1 OK occurrences=1` for both | — | — | — | — | **nothing**: `MIN_QUOTE_CHARS=12` accepts a single word; `organization` (also 12) is `exit=1 occurrence-not-unique` until an anchor is added; 11 chars → `quote-too-short` |
| A5 | **S054 row 4-space indented** | 23/23 | exit 0 | **exit 1 `FAIL rule=no-row record=S054`** | — | **exit 0; `FLEET rows 53`, no E-code** | 20/**53**/1/49 | K2/C2 (row count), K8 |
| A5c | indented S054 **+ a well-formed column-zero decoy S055 row** | 23/23 | exit 0 | **exit 1 `FAIL rule=no-row record=S054`** | — | **exit 0** | 20/**54**/1/49 | **K8 only**; K1/K2/C2 spoofed |
| A6 | expected list names a **nonexistent** entry | 23/23 | exit 0 | 44/44 | **exit 1 missing=1 unexpected=1** | 0 | 20/54/1/49 | C7/K9 |
| A6b | expected list carries a **duplicate line** | 23/23 | exit 0 | 44/44 | **exit 0 (!)** `missing=0 unexpected=0` but `expected=50` | 0 | 20/54/1/49 | **C7's literal `expected=49` only** (K9 blind) |
| A7d | **F20 → byte-copy of the KEV entry** (H1 "CISA Known Exploited Vulnerabilities catalog", `source: S052`, `ids=S052`); `source: S054` header added to an unharnessed evidence entry whose own recheck is untouched | **23/23 exit 0** (`PASS F20 … ids=S052`) | exit 0 | 44/44 exit 0 | **49/49 exit 0** | exit 0 | 20/54/**1**/49 | **nothing operational** (K3 only if read as "the named path") |
| A8 | **capture bytes = the EPSS page** under the row/manifest URL; manifest pins the EPSS quotes | 23/23 (`ids=S054`) | `Q1..Q4 OK anchor=216/217/217/235 exit 0` | 44/44 exit 0 | 49/49 exit 0 | exit 0 | 20/54/1/49 | **nothing** (r36 A3f) |
| A8b | **registry + manifest url = the erratum tutorial page, capture bytes = the docs home page**; entry body quotes tutorial L247 | 23/23 (`ids=S054`) | `exit 0` | 44/44 exit 0 | 49/49 exit 0 | exit 0 | 20/54/1/49 | **nothing** |
| A9b | **F20 row `status=proposed`** (never admitted), its entry also appended as a second entry cell on the F19 row; S054 row used-by = that stub | **23/23 exit 0**, `PASS F19 … ssvc-stub.md ids=S054`, **no F20 line** | exit 0 | 44/44 exit 0 | 49/49 exit 0 | exit 0 | **20**/54/1/49 | **nothing**: K1 counts the unadmitted row |

Evidence excerpts (fixtures `a3c`, `a7d`, `a8b`, `a9b`; full transcripts existed in the removed
scratch):

```
A7d  PASS F20 knowledge/ssvc-kev-copy.md ids=S052 exit=0   entries=23 pass=23 exit=0
     [F20 entry H1] # CISA Known Exploited Vulnerabilities catalog — exploitation membership with a per-record remediation clock
     [only file declaring S054] corpus/knowledge/considerthese-proposals-ledger.md
A8b  PASS F20 corpus/knowledge/ssvc-...md ids=S054 exit=0 ; source-recheck exit 0 ; census ok
     cmp capture round-37/S054.txt == docs home page -> IDENTICAL
     grep -cF 'SSVC rates vulnerabilities on risk to the concerned stakeholder' capture -> 0
A9b  [F20 row] | F20 | SSVC stakeholder-specific vulnerability categorization | proposed | knowledge/ssvc-stub.md | S054 | planned |
     PASS F19 knowledge/epss-exploit-prediction-scoring.md ids=S053
     PASS F19 knowledge/ssvc-stub.md ids=S054
     entries=23 pass=23 exit=0   ; grep -cE '^\| F[0-9]+ \|' -> 20
```

## 3. Clause-by-clause: what the frozen kill rule catches

Frozen rule: "Any of: frontier rows != 20; S054 row absent or malformed (NF != 13); entry absent or
failing Q1-Q6; harness not entries=23 pass=23 exit=0; source-recheck S054 exit != 0; census exit != 0;
junk-f20 accepted by source-recheck or harness; capture/manifest absent or unbound; recheck-audit
unexpected != 0."

| clause | catches | does not catch |
|---|---|---|
| K1 `frontier rows != 20` | a missing F20 row | **A9b** — the grep counts any `F<n>` row, admitted or not; the claim's word "admitted" has no command |
| K2 `S054 row absent or malformed (NF != 13)` | A1's cite count, A5 (row not counted → 53), NF=12 shapes (census `E01 fields=12` measured on a decoy) | **A5c** (decoy restores 54); any *content* of the row: `anchor`/`teaches` cells are never compared to the capture |
| K3 `entry absent or failing Q1-Q6` | literally, a row cell naming an absent file (A1); by reading, a 22-word stub (A3c) or a KEV copy (A7d) | **no command**: Q1-Q6 are a human rubric; the clause names no counter, no path, and no referent ("the entry" = the row's cell? the path in the predicate?). Only this clause has any purchase on A3c/A7d, and it is unoperationalized |
| K4 `harness not entries=23 pass=23 exit=0` | A1 (missing-entry), A2 (manifest-unreadable), A2c (recheck-exit-2), A3b (selection-not-cited) | **A9b** (padded from another row), A3c, A4, A7d, A8, A8b (all 23/23) |
| K5 `source-recheck S054 exit != 0` | A2, A2c (absent bytes), the A4b quote channel | A8, A8b: exit 0 on the wrong document; A4d: exit 0 on a 57-char sentence |
| K6 `census exit != 0` | A5b's NF=12 decoy, A9's E11 | **A5/A5c**: census is *green* on a 4-space-indented row (it is a code block; no E-code, `rows` drops silently) |
| K7 `junk-f20 accepted by source-recheck or harness` | the fabricated **quote** channel (A4b) | **no consumer exists** for the committed file (`grep` over `corpus/instruments/` finds no `c2-controls` reference except round-34's existence-only R9, which names `junk-f17.md`); A4 shows junk is admitted through the **body** channel, which K7 never tests |
| K8 `capture/manifest absent or unbound` | A2b (url-mismatch), A5/A5c (no-row) | **A2c** (record bound while its capture file is absent: `records=44 bound=44 unbound=0`), **A8/A8b** (bound to the URL *string*, sha over unrelated bytes) |
| K9 `recheck-audit unexpected != 0` | A6 (unexpected=1) | **A6b** (duplicate expected line: audit exits **0**; only C7's literal `expected=49` reds); `missing` is not named in K9 at all |

## 4. Missing clauses (each is a demonstrated hole, not a hypothetical)

- **M1 — row↔entry↔source triple is unbound.** `FRONTIER_ROW` captures id/title/status/entry only;
  column 5 (`sources`) is discarded and never compared to the entry's declared set. A7d/A9b:
  `F20 … S054` row, entry declares and rechecks S052, battery green (A7d `ids=S052`).
- **M2 — the row's `status` cell is never read by any counter.** A9b: `status=proposed`, row counted,
  harness padded from the F19 row, every command green. (Same class as r36 A5g, still open.)
- **M3 — entry body ↔ pinned quote is unbound.** Nothing compares an entry's blockquotes to its
  capture. A3c (no claim), A4 (false claim), A8b (claim text absent from the capture, `grep -c` 0) all
  pass. Q1/Q3/Q5 are exactly the rubric items that would reject them, and none is instrumented.
- **M4 — capture authenticity.** A8b is the round-37 instance of r36's A3f/K1: the erratum moved the
  literal to `/SSVC/tutorials/ssvc_overview/` *because the load-bearing claims are not on the home
  page*, and the battery still cannot tell the two pages apart. `capture-source.py` still has no
  `--verify`/`IDENTICAL|DIFFERS` mode (`grep` for `verify|IDENTICAL|DIFFERS` → nothing).
- **M5 — the junk control has no consumer.** The r34 suite checked `junk-f17.md` *existence* only; r35
  and r36 suites reference no junk twin; nothing references `c2-controls/junk-f20.md`. The clause is a
  receipt-replay, not a counter, and it tests the wrong channel (quote vs body).
- **M6 — pin substance floor.** `MIN_QUOTE_CHARS = 12` is met by a *single common word*: `concentrated`
  (12 chars) and `Utility (ssvc` (13) are accepted as the entry's only pinned evidence, `Q1 OK
  occurrences=1`, exit 0 (A4d''). Only an 11-char string is refused, and only non-uniqueness forces an
  anchor (`organization` → `occurrence-not-unique`). A fabricated claim is therefore "supported" by a
  word, and Q3's "load-bearing claim" test has no machine proxy.
- **M7 — expected-list comparison is set-based.** `load_expected` keeps duplicates; `expected_mismatch`
  diffs sets, so a duplicated line yields `missing=0 unexpected=0 exit=0` with `expected=50` (A6b). Only
  the claim's literal `expected=49` string reds it; K9 does not.
- **M8 — census silence on indented rows.** The parser accepts 0–3 leading spaces and treats 4+ as code;
  a skipped row produces no E-code and no count, so "census exit 0" carries no information about that
  row (A5). The row count and binding are the only catchers, i.e. the conjunction, not K6.
- **M9 — binding counts absent captures as bound.** A2c: `records=44 bound=44 unbound=0 exit=0` with
  `S054.txt` missing (r36 K2, unfixed). K8's "capture absent" is enforceable only through K5.

## 5. Verdict

1. **C2 is not falsified as achievable.** A0c lands every killing command at the frozen literals
   (20 / 54 / 1 / 49, 23/23 exit 0, source-recheck 0, 44/44, 49/49, census 0).
2. **The kill rule is not an admission test.** Four constructions pass **every** clause: A9b (F20 never
   admitted), A3c (22-word stub), A7d (a KEV entry admitted as F20), A8b (home-page bytes under the
   tutorial URL). A9b falsifies K1 as written; A3c falsifies K3 as written; A8b falsifies K8 as written.
   Three of those are *body/content* hollows that only a human Q1-Q6 read rejects.
3. **The one that reaches the frozen predicate's letter is A8b.** Post-erratum, A8b satisfies every
   artifact and count string the predicate names — row and manifest url = the tutorial page, capture
   committed and "bound", entry cites `source: S054`, harness `PASS F20 ids=S054`, source-recheck 0,
   census 0, expected 49 — while the pinned bytes are the docs home page and the entry's L247 quote is
   absent from them (`grep -c` → 0). Credit taken on that shape is false provenance: it certifies a
   reading of the page the claim does not hold. This is a **fixable defect** (K1 verify mode + body
   binding), not a tradeoff: the reason it is not caught is missing instrumentation, and the round has
   independent capture evidence (two byte-identical tutorial fetches) that no counter consumes.
4. **Which way the canonical judge should read it.** If the judge applies the kill rule literally, C2
   passes on hollow landings, including A9b where the admission never happened; if the judge applies the
   predicate plus Q1-Q6 by reading, A3c/A4/A7d are rejectable but only by inspection. Either way the
   claim's own counters cannot distinguish A0c from A8b. The smallest safe disposition is: accept C2
   only with (a) a Gate line recording live-fetch equality for the tutorial page (the two-seat
   reproduction above), (b) M1's row-sources binding, and (c) an explicit statement that the kill rule
   does not test entry content; otherwise the claim must be re-filed with a counter that does.

## 6. Smallest safe corrections

- **S1 (closes A9b, M1, M2 — 20 lines in `frontier-recheck-count.py`).** Parse column 5
  (`sources`) of `FRONTIER_ROW`; require `row_sources == declared ∪ evidence`
  (`problems=row-sources-not-matching-entry`); treat any status outside `{admitted, proposed,
  rejected, retired}` as `problems=unknown-status`; print `rows=<n> admitted=<m>` in the summary and
  make the claim's harness line require `rows=20 admitted=20 entries=23 pass=23 exit=0` **and**
  `PASS F20 <exact entry path> ids=S054`.
- **S2 (closes A8b, A8, M4 — a verify mode, the r36 K1 ask).** `capture-source.py --verify --id S054
  --url <row url> --manifest <round-37 manifest>` re-fetches, normalizes with the same
  `html_to_text()`, prints `IDENTICAL|DIFFERS pinned=<sha> live=<sha> utc=<Z>`; the round-37 Gate
  records that line (a live check cannot be a fail-closed rule for a mutable page, but it is the only
  thing that separates the capture from A8b).
- **S3 (closes A3c, A4, A8b body half, M3, M6).** Extend `source-recheck.py` with `--entry <path>`:
  every blockquoted `> "…"` in an admitted entry must normalize into the manifest's capture, and at
  least one must be ≥ 25 normalized characters; the harness passes `--entry` for every admitted row and
  fails `problems=entry-quote-not-in-capture` / `problems=entry-has-no-pinned-quote`.
- **S4 (closes A4, M5).** Commit `c2-controls/junk-f20.md` **and** a selftest/closures case that parses
  its `> "…"` lines into a manifest over the landed capture and asserts exit 1, so K7 is checkable from
  repo bytes; state in the receipt that it tests the quote channel only (A4 is the body channel).
- **S5 (closes A5/A5c, M8).** In `sources-census.sh`, report a 4-space-indented row-shaped line under
  `## Registry` as a finding (E01-shaped, or a new `E13 indented registry row`), or count it in
  `rows=` with a `skipped=` metric — silence is the defect, not the indentation.
- **S6 (closes A6b, M7).** `load_expected` fails on a duplicate line (`expect-duplicate <name>`), and
  the C2 kill rule's audit clause names `missing` as well as `unexpected`.
- **S7 (closes A2c, M9; carried from r36 K2).** `capture-binding-check.py` rule A3: a manifest `path`
  that names no file is `FAIL rule=capture-missing record=<id>`, so `bound=` means "bytes present".

## 7. Replay recipe (scratch-free rebuild)

```bash
S=$(mktemp -d); git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  archive b56a41680cefd391868c1c370dc063c69d827e7d | tar -x -C "$S"
find "$S/corpus/knowledge" -name '*.md' -exec sed -i \
  "s|/home/vgpnk/Projects/shokunin/kasegi-shokunin|$S|g" {} +
# A3c stub (the whole hollow landing apart from row/capture):
printf '# SSVC\n\nsource: S054 — https://certcc.github.io/SSVC/tutorials/ssvc_overview/\nrecheck: cd %s && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054\n\nS054.\n' "$S" \
  > "$S/corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md"
# S054 row: 11 cells, tier A, mined, opened 2026-10-26, on-release, used-by the entry path
# F20 row: | F20 | SSVC … | admitted | knowledge/ssvc-stakeholder-…md | S054 | … |
# expected list: append corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md
# capture: S054.txt = capture-source.py html_to_text() of the tutorial fetch; manifest url = tutorial url
(cd "$S" && python3 corpus/instruments/frontier-recheck-count.py --root . \
  && python3 corpus/instruments/capture-binding-check.py --root . \
  && python3 corpus/instruments/recheck-audit.py --quiet --root . --cdroot .)
python3 "$S/corpus/instruments/source-recheck.py" --manifest "$S/corpus/source-snapshots/round-37/manifest.json" --source S054
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/corpus/SOURCES.md" --today 2026-10-26
```

A9b is the same rig with `status=proposed` on the F20 row, the stub appended as a second entry cell on
the F19 row (`… | knowledge/epss-…md , knowledge/ssvc-stub.md | S053 | …`), and the S054 row's used-by
pointing at the stub. A7d replaces the F20 entry with `cp corpus/knowledge/cisa-kev-catalog.md
corpus/knowledge/ssvc-kev-copy.md` and prefixes `source: S054 — <url>` to an unharnessed evidence entry.
A8b copies the home-page capture to `round-37/S054.txt` while the row and manifest keep the tutorial
URL.

## 8. What I did not do

- Wrote only this receipt; no lane instrument/artifact edited; fleet root, sibling lanes, `shokuknow`,
  `~/Projects/*` untouched; no mutating git/jj; no subagent; no `agent://all`; no swarm.
- No tool installed or upgraded: `python3` 3.14.8, `curl`, `cmp`, `tar`, read-only `git` sufficed; no
  pacman.
- `curl` used twice, read-only, for fixture captures: the SSVC home page
  (`http=200`, 105,807 B, `17:11:38Z`) and the erratum tutorial page (`http=200`, 143,053 B,
  `17:19:30Z`); both normalized digests reproduce the other C2 seat's fetches exactly.
- Scratch `/fast/scratch/hyaku/kasegi-r37/CritC2Kill/` (export, 20 fixture roots, rig scripts, attack
  logs) removed before yield.
