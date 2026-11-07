# ExecC1Indep — independent byte check of C1 tranche 9 at d51220a

Seat: ExecC1Indep (leaf, read-only). Scope: re-derive the C1 landing
`d51220aeb4a538b7b211bb2629e83210669cd56d` (base `dff5a0a01e8aafe6be81f4ee61567745c3c4c485`)
without importing any counter code: `git archive` both revs into scratch, parse
`.ufo/waves/round-94/c1/repair-map.tsv` (19 rows) myself, reconstruct each expected
line edit, and compare against the after tree.

## Verdict

**AGREE / STANDS** — every frozen C1 byte-level claim re-derived independently:

- All 19 map rows reproduce the after-tree line exactly (rows 14+15 on
  `triage-thresholds.md:397` are two edits on one line; composing both
  replacements onto the base line yields the after line byte-for-byte, in either
  application order).
- The changed-line set between base and after is exactly 18 lines:
  `corpus/knowledge/triage-thresholds.md` lines
  {143, 151, 153, 220, 267, 310, 311, 312, 313, 355, 374, 390, 394, 397, 446,
  459, 460} (17 lines; 397 carries two edits) plus
  `corpus/knowledge/considerthese-proposals-ledger.md:156` (1 line). No other
  line in either file changed; `SKILL.md` is byte-identical between the two
  trees (`diff -q` rc=0), so every repoint lands on unchanged anchors.
- Every old token occurs at least once on its base line (per-row counts below;
  the ledger key `SKILL.md:1163` occurs **2** times on base line 156 and its
  replacement `SKILL.md:1164` occurs **2** times on after line 156; zero
  residual `SKILL.md:1163`/`SKILL.md:1164` cross-occurrences).
- Every new value's anchor lies inside `SKILL.md` (after tree, 1251 lines): all
  19 ranges in-bounds; spot-read of each anchor range confirms the claimed
  content (e.g. 828 `p_success = …`, 999 schema bullet, 1164 `r46-landing-gate.py`
  registry row, 191 `attempts()≥2`, 910-913 12-step ladder).
- Knowledge meter independently re-run at both revs:
  `dff5a0a` → `rate=1008/1999`, `d51220a` → `rate=1009/2000` — matches the
  frozen claim 1008/1999 → 1009/2000.

## Per-row results (`line key expected==after`)

Format: `row  file:line  expected==after  old_tok_count  new_tok_count`.
Single-token rows show per-token counts; rows 14/15 share line 397 and are
verified by composition (see receipts/line397-compose.txt).

```
 1  triage-thresholds.md:143   True   old=1 new=1   `SKILL.md:526`        -> `SKILL.md:251-253`
 2  triage-thresholds.md:151   True   old=1 new=1   `SKILL.md:526`        -> `SKILL.md:251-253`
 3  triage-thresholds.md:153   True   old=1 new=1   `SKILL.md:14-15`      -> `SKILL.md:264-266`
 4  triage-thresholds.md:220   True   old=1 new=1   `SKILL.md:90-91`      -> `SKILL.md:157-158`
 5  triage-thresholds.md:267   True   old=1 new=1   `SKILL.md:94-95`      -> `SKILL.md:161-162`
 6  triage-thresholds.md:310   True   old=1 new=1   `SKILL.md:498`        -> `SKILL.md:828`
 7  triage-thresholds.md:311   True   old=1 new=1   `SKILL.md:499`        -> `SKILL.md:829`
 8  triage-thresholds.md:312   True   old=1 new=1   `SKILL.md:500-501`    -> `SKILL.md:830-831`
 9  triage-thresholds.md:313   True   old=1 new=1   `SKILL.md:502`        -> `SKILL.md:832`
10  triage-thresholds.md:355   True   old=1 new=1   `SKILL.md:522`        -> `SKILL.md:999`
11  triage-thresholds.md:374   True   old=1 new=1   `SKILL.md:111-112`    -> `SKILL.md:910-913`
12  triage-thresholds.md:390   True   old=1 new=1   `SKILL.md:525`        -> `SKILL.md:321-324`
13  triage-thresholds.md:394   True   old=1 new=1   `SKILL.md:525`        -> `SKILL.md:340-346`
14  triage-thresholds.md:397   True*  old=1 new=1   `SKILL.md:146`        -> `SKILL.md:224-226`   (composed)
15  triage-thresholds.md:397   True*  old=1 new=1   `SKILL.md:246`        -> `SKILL.md:331-335`   (composed)
16  triage-thresholds.md:446   True   old=1 new=1   `SKILL.md:115`        -> `SKILL.md:184-187`
17  triage-thresholds.md:459   True   old=1 new=1   `SKILL.md:146, 245-247` -> `SKILL.md:224-226,335-338`
18  triage-thresholds.md:460   True   old=1 new=1   `SKILL.md:113-117`    -> `SKILL.md:191`
19  considerthese-proposals-ledger.md:156  True  old=2 new=2  `SKILL.md:1163` -> `SKILL.md:1164`
```

\* Rows 14 and 15 target the same base line; each individual `replace` alone does
not equal the after line (the other token is still old), but applying both map
edits to the base line reproduces the after line exactly. This is the expected
behaviour for a two-edit line, not a defect.

## Changed-line set (exact)

```
corpus/knowledge/triage-thresholds.md:            17 changed lines
  [143, 151, 153, 220, 267, 310, 311, 312, 313, 355, 374, 390, 394, 397, 446, 459, 460]
corpus/knowledge/considerthese-proposals-ledger.md: 1 changed line
  [156]
total = 18 changed lines, matching the frozen claim.
```

Full-tree `diff -rq` between the two archives shows the only corpus file
changes are the two named files plus `corpus/SOURCES.md` (the S140 row, part of
the freeze commit's C2 evidence, not a C1 edit) and the new
`.ufo/waves/round-94/` + `corpus/source-snapshots/round-94/` trees. The
`.ufo/waves/round-31/wave1/ExecCensusDry/validate/` embedded fixture copies of the
two corpus files also differ between trees — verified they carry exactly the
same 18 line edits and nothing else (subset of the allowed line set).

## Ledger occurrence counts (line 156)

- base line: `SKILL.md:1163` occurs **2** times (registry-row pointer + the
  "date-order" quote context); `SKILL.md:1164` occurs 0 times.
- after line: `SKILL.md:1164` occurs **2** times; `SKILL.md:1163` occurs 0 times.
- Both occurrences were repointed, consistent with the label's "both
  occurrences on the line" instruction.

## Receipts

All command outputs cited above are in
`.ufo/waves/round-94/w1/ExecC1Indep-receipts/`:

- `verify-map-rows.txt` — full per-row verifier output (parse of
  repair-map.tsv, per-row expected==after, changed-line census, old-token
  presence, anchor bounds, ledger counts). Script: scratch `verify.py`
  (independent; no counter code imported).
- `triage-thresholds.diff` — `diff -u` of the two archived trees' file.
- `ledger.diff` — same for the ledger file.
- `line397-compose.txt` — composed two-edit check for line 397.
- `tree-diff-summary.txt` — `git archive` rc, `diff -q SKILL.md` rc=0.
- `meter.txt` — `knowledge-meter.py --measure-rev` at both revs:
  `1008/1999` → `1009/2000`.

Commands run (all rc observed):

```
mkdir -p /fast/scratch/hyaku/kasegi-r94/ExecC1Indep{,/base,/after}
git archive dff5a0a01e8aafe6be81f4ee61567745c3c4c485 | tar -x -C $S/base   # rc=0
git archive d51220aeb4a538b7b211bb2629e83210669cd56d      | tar -x -C $S/after  # rc=0
diff -u base/.../triage-thresholds.md after/.../triage-thresholds.md         # rc=1 (17 hunks->18 lines)
diff -u base/.../considerthese-proposals-ledger.md after/...                  # rc=1 (1 line)
diff -q base/SKILL.md after/SKILL.md                                          # rc=0 (identical)
diff -rq base after                                                           # only expected paths
diff base/.ufo/.../validate/corpus/knowledge/triage-thresholds.md \
     after/.ufo/.../validate/corpus/knowledge/triage-thresholds.md            # same 17 line numbers
diff .../considerthese-proposals-ledger.md (embedded copies)                 # same line 156
python3 verify.py                                                             # all rows OK
diff -q embedded-copy vs base/after corpus files (cmp)                        # copies == respective tree version
python3 knowledge-meter.py --lane . --measure-rev dff5a0a...                  # rate=1008/1999
python3 knowledge-meter.py --lane . --measure-rev d51220a...                  # rate=1009/2000
sed -n '<anchor ranges>p' after/SKILL.md                                      # content matches labels
```

## Notes / non-findings

- The two-edit line 397 initially looked like a per-row mismatch under naive
  single-token reconstruction; composing both map rows resolves it exactly.
  Not a defect.
- The embedded `.ufo/waves/round-31` fixture copies changing is expected: they
  are byte-copies of the corpus files at their respective revisions and the
  landing regenerated them consistently (same 18 lines, no extras).
- `corpus/SOURCES.md` changed by +2 lines (S140 row) — that is the freeze/C2
  evidence commit content already landed at `96b5033`, inside the
  base..landing diff window but not a C1 tranche-9 edit; out of this seat's
  claim scope, noted for completeness.
- No tool installs were needed; no pacman transactions; scratch
  `/fast/scratch/hyaku/kasegi-r94/ExecC1Indep` removed on seat exit per spec.
