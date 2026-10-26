# RevH2Corrections — kasegi-shokunin round 40, falsify wave 2

- **Seat / item attacked:** H2 — the `Correction (round 40)` records that wave 1 appended to
  SCORECARD.md, LOG.md, SHONEN.md and corpus/lessons/round-39.md, and the claims.json C1
  predicate clause they carry ("H2 `Correction (round 40)` lines naming the final r39 receipt
  values (closed=7/8 exit=1; selftest failures=1) exist in …, count >= 1 each").
- **Method:** every command re-run against committed bytes via `git show <ref>:<path>` from the
  lane repo (read-only git only). Refs: lane tip **Y = 3074c7679d6f527ec3930d7748ccce1dbae4a58a**;
  claims-freeze **5e985b74075dd3813a63d7750966bf8abf693465**; base a7af2ce63bce153757d39bf66b366a96caf30c13;
  r39 judged head 8371e7ac9f32cae5ed72f8c28205634603f836fa. Frozen claims read first, not edited.
- **Result:** **reproduced on every counting command; 1 minor defect found** (SHONEN box mislabel,
  D1 below). No falsification of the corrections' substance.

## 1. Counting command re-run — REPRODUCED

`git show Y:<file> | grep -c '^Correction (round 40)'`:

| file | count at Y | count at freeze 5e985b7 | lines at Y |
|---|---|---|---|
| SCORECARD.md | 2 | 0 | 1588, 1589 |
| LOG.md | 2 | 0 | 1723, 1724 |
| SHONEN.md | 2 | 0 | 207, 208 |
| corpus/lessons/round-39.md | 2 | 0 | 98, 99 |

≥1 in each of the four ✓ (total 8, matching the r40 receipt's `H2 payload=corrections=8`).
Lane-wide `git grep -n '^Correction (round 40)' Y` finds exactly these 8 record lines plus the
8 copies inside the wave-1 deliverable `.ufo/waves/round-40/wave1/ExecH2Corrections.txt` — no
stray corrections elsewhere. Corrections landed in 4766b9d (round-39.md block) and bfca9ae
(SCORECARD/LOG/SHONEN blocks), both after the freeze.

## 2. Final r39 receipt values named — REPRODUCED

Line 1 of each pair names `closed=7/8 exit=1` and `selftest failures=1` (plus `selftest cases=8
failures=1`, `selftest-exit=1`, `G2 positive=fail`, all-gates v5, sha256 8d46d7b2…); round-39.md
line 2 additionally restates both values verbatim. Independent token scan over the 8 committed
lines: **5 carry both `closed=7/8` and `failures=1`** — exactly reproducing the r40 receipt's
`H2 payload=…,named=5,…` (suite h2_scan counts lines with both tokens; `missing=0`, `fences=closed`).

Ground truth re-verified from committed bytes, not taken from the corrections:

- `.ufo/waves/round-39/final-gates/all-gates.txt` at 8371e7a: sha256
  **8d46d7b251fd6736ba1841814274201176d3a7628f9330e8c9b1917013741471** — matches the sha256 every
  correction cites; header `all-gates v5` ✓; `closed=7/8 exit=1`, `run-exit=1` ✓; G2 is the single
  red, `closed=0` on `diff-clean=0,final-lane-commit=0` (G1,G3–G8 closed=1) ✓; selftest
  `cases=8 failures=1`, `selftest-exit=1`, `selftest case=G2 positive=fail … verdict=fail` ✓;
  `deviation=non-default --lane` ✓. File unchanged 8371e7a→Y (`git diff` empty).
- Attempt-1 receipt at 5006097a84305267c9a3e8c1e1d560e60fe41d37: `all-gates v3`,
  `closed=8/8 exit=0`, `selftest cases=8 failures=0`, `run-utc=2026-10-26T21:35:00Z` —
  committer-date 2026-10-26T17:12:12-03:00 (= 20:12:12Z) < run-utc ✓ "after its containing
  commit"; 5006097a is an ancestor of 8371e7a ✓. The corrections' "the only 8/8 tally is the
  attempt-1 receipt … which the round discards" is accurate (the committed receipt at 8371e7a is
  v5, not v3).

## 3. G2/G6 non-independence reason named — REPRODUCED

Line 2 of each pair names both reasons with committed citations:

- **G2** grades receipt shape/digest and accepts forged payload values — grounded in
  `.ufo/waves/round-39/wave2/CritG2Exploit.md` (committed at Y): §F2 "DEFECT: erratum E5's graded
  semantics are not enforced on the receipt", probe table shows mut-f/g/h/j/k all rc=0 (mut-i
  also passes but is the ref-vacuity class; F2's heading lists f,g,h,j — the corrections' token
  list is a true subset of the passing probes).
- **G6** greens only while `/fast/scratch/hyaku/kasegi-r39/` is quiet although the seat protocol
  populates that root — grounded in `.ufo/waves/round-39/wave2/CritC1Kill.md` (committed at Y):
  line 94 verbatim `G6 payload=r37=absent,r38=absent,r39=present,work=inside,tolerated=none,read=ok closed=0`
  measured with seats live (11→25 scratch entries), plus `deviation=non-default --lane` on the
  green runs.

## 4. Pure appends, previous claims untouched — REPRODUCED

`diff 5e985b7:<file> Y:<file>` per file:

| file | hunk | added | removed |
|---|---|---|---|
| SCORECARD.md | 1584a1585,1589 | 5 | 0 |
| LOG.md | 1719a1720,1724 | 5 | 0 |
| SHONEN.md | 203a204,208 | 5 | 0 |
| corpus/lessons/round-39.md | 94a95,105 | 11 | 0 |

Single pure-addition hunk each, starting exactly at the freeze file's last line (1584/1719/203/94)
→ EOF appends; `wc -l` at Y = freeze + added (1589/1724/208/105) ✓. Fence parity unchanged
(SCORECARD 12↔12, others 0↔0); SCORECARD's last fence closes at :856, far above :1584, so the
appended lines sit outside any fence (consistent with the suite's `fences=closed`). The 11th–5th
lines of the round-39.md append are the R6 Gate additions (S056/S058/S059) — also append-only.
Byte-exact provenance: the 8 committed correction lines are byte-identical to the wave-1
deliverable `wave1/ExecH2Corrections.txt` (`diff` empty).

## 5. Stale "r39 C1 8/8" sweep at Y — no uncorrected live record

- The four records' pre-existing 8/8 rows (SCORECARD:1567, LOG:1709, SHONEN:194, round-39.md:15)
  still contain their original text by design (append-only) and each now stands corrected by the
  appended block in the same file ✓.
- Frozen `.ufo/waves/round-39/claims.json` C1 after-cell ("closed=8/8 exit=0 at J") is a frozen
  artifact; it is explicitly named and corrected by the round-39.md block ("the Frozen claims C1
  after-cell states …") ✓.
- `corpus/lessons/round-38.md` 8/8 rows (:21, :94) carry the round-39 correction at :311 ✓.
- `corpus/lessons/round-39-verifier-spotcheck.md` mentions 8/8 only as the R2 defect record ✓.
- Remaining 8/8 hits are historical wave/dispatch/build artifacts (round-21…39 seat receipts,
  specs, build-results JSONs), instrument forge-fixtures (r38/r39-closure.sh selftest forgeries),
  and output-format descriptions (SKILL.md:1114-1115 registry rows) — none is a live r39 C1
  pass claim. **No record still claiming r39 C1 8/8 at Y without a correction.**

## 6. Defects

- **D1 (minor, wording) — SHONEN corrections mislabel their target as "box 3"; it is box 1.**
  SHONEN.md:207 quotes "the round-39 box 3 evidence line ("suite `--selftest` graded cases=8
  failures=0 at the verification ref")" and :208 concludes "so box 3 stays `[~]`". The quoted
  line is SHONEN.md:194, the round-39 evidence of the box at :193 — "SKILL.md contains real
  decision tables, error patterns, checklists, cited sources" = **box 1** of the four fixed
  promotion criteria (SHONEN.md:9-58 fixes the order; :80 "box 1's 'byte-unchanged' sentence"
  and :81 "box 4's 'owed' sentence" confirm the convention). Box 3 = "Instructions executable by
  an agent without oral context" (:197); its round-39 evidence (:198) reads "r39 suite run +
  graded selftest at the verification ref Y (all-gates.txt)" and does not contain the quoted
  text. The convention is proven by the round-39 correction at :190, which correctly calls :185
  ("r38 suite run + selftest over the judged head…") "box 3's round-38 evidence line" (:185 sits
  under :184 = box 3). The landed label contradicts round-39-verifier-spotcheck.md §5 R2
  ("SHONEN.md round-39 box 1") and wave-1 CritClaimsContradiction.md:26 ("SHONEN.md:194 (box 1)").
  Impact: the verbatim quote still pins the target and both boxes remain `[~]`, so nothing
  semantic breaks — but a correction line mislabeling the record it corrects is a precision
  defect in exactly the class R2 polices. Suggested fix (next round, append-only): a
  `Correction (round 40)` line in SHONEN.md noting the evidence line is box 1's, not box 3's.

## 7. Observations (non-defects, flagged for owners)

- LOG:1723 says the round-39 correction (LOG:1719) "cites the report-only `3fa81ef5…` measurement
  without naming the final receipt values". LOG:1719 does print `closed=7/8 exit=1` and
  `cases=8 failures=1` — but attributes them to a report-only measurement at 3fa81ef, never to
  the committed receipt; the phrase is true in the provenance sense it operates in (the round-40
  line immediately supplies the receipt-tied values). Ambiguity noted; not judged a defect.
- The r40 receipt `.ufo/waves/round-40/final-gates/all-gates.txt` is **untracked** at the tip
  (`git ls-tree Y .ufo/waves/round-40/final-gates/` → 0 entries; status `?? …/final-gates/`), so
  the claims' judged_head_rule "git diff --name-only J Y = all-gates.txt" has no satisfying
  commit pair; the receipt header (all-gates v4) itself records `export-ref=3074c76` (= Y).
  Outside this seat's scope — flagged for the receipt/H7/judged-head owners.
- Lane working tree dirty with 4 untracked entries at measurement time (final-gates/, wave2/,
  two `.ready` dispatch markers) — expected mid-wave; C1's kill rule evaluates cleanliness "at
  filing".

## 8. Verdict

REPRODUCED with 1 minor defect. Counts 2/2/2/2 (≥1 each ✓); every correction pair names the
final r39 receipt values (`closed=7/8 exit=1`, `selftest failures=1`) and the G2/G6
non-independence reason, all verified against committed receipt bytes and committed wave-2
attack artifacts; appends are pure EOF additions with zero deletions; no uncorrected r39-8/8
record survives at Y. D1 (SHONEN "box 3" → box 1) is the only finding.

**Fixture:** `RevH2Corrections.appended-tails.txt` — the 26 appended lines byte-exact as
committed at Y (git show extraction), sha256
a295f169ee9f70a8aa358eaaaa908290d660af28643b075c38d1f9d3b0426d49.

Scratch `/fast/scratch/hyaku/kasegi-r40/RevH2Corrections/` removed before yielding. No lane,
fleet, sibling, or source-tree file edited; no mutating git/jj command run; no pacman; no
tool installs needed.
