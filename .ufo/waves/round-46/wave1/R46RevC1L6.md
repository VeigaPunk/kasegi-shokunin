VERDICT: BROKEN

# R46RevC1L6 — C1 limb L6 (per-row load-bearing) attack

Target: `corpus/instruments/r46-c1-gate.py` gate L6 (lines 203-236), the frozen C1 `after` sentence in `.ufo/waves/round-46/claims.json` ("every row load-bearing (blanking the row's token in a scratch copy turns the entry check red)").

## How L6 works (read from the code, not from the docstring)

- L6 runs once per row of each re-grounded entry. It copies `corpus/` into a scratch dir with `shutil.copytree(..., symlinks=True, ignore=shutil.ignore_patterns("lessons", "__pycache__"))` (lines 216-217).
- The mutation is applied to the anchored file only (line 218). If the exact token is in the raw file, `raw.replace(tok, "#"*len(tok))` blanks **every** occurrence in that file (line 222), not the first one. Otherwise the whole anchored line range is blanked (lines 223-228).
- A row survives iff per-entry mode exits 0 on the scratch copy (line 231). `mutants` is incremented before the run (line 229), so the count never checks what the red was caused by.
- Missing: no check that the **unmutated** scratch copy is green. Any non-mutation reason for red counts as "load-bearing".
- Any exception (e.g. missing anchor in scratch) is caught in `main` (lines 264-265) and fails all seven limbs (fail-closed).

## Scratch and control

Scratch root: `/fast/scratch/hyaku/kasegi-r46/R46RevC1L6/` (removed on exit). Base: a copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure` with the counter copied in. Nothing committed; no git mutation; no tools installed.

Do-nothing control (`--root base --baseline base`):
```
gate L6 pass=0 read=mutants=0 survivors=none
c1-gate fixed=1/7 exit=1
```
This matches `expect_before` and the freeze-controls `c1 do-nothing` reading.

## Finding 1 (cheapest BROKEN construction): rows that pass L6 but support nothing — `weak`

Recipe. Copy the base tree. In `corpus/knowledge/claim-gates.md` and `corpus/knowledge/claim-package-contract.md`:
1. Replace the `recheck:` line in place with `recheck: cd kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<entry>`.
2. Append a `## Re-ground (round 46)` section, 6 rows each, exactly as below.

`claim-package-contract.md` rows (verbatim from the tree):
```
| G1 | a claim-ready package has six files | `corpus/instruments/r46-c1-gate.py:1-3` | `round-46 C1 counter` |
| G2 | a claim-ready package has six files | `corpus/instruments/r46-c1-gate.py:1-3` | `round-46 C1 counter` |
| G3 | a claim-ready package has six files | `corpus/instruments/r46-c1-gate.py:1-3` | `round-46 C1 counter` |
| G4 | a claim-ready package has six files | `corpus/instruments/r46-c1-gate.py:1-3` | `round-46 C1 counter` |
| G5 | a claim-ready package has six files | `corpus/instruments/r46-c1-gate.py:1-3` | `round-46 C1 counter` |
| G6 | a claim-ready package has six files | `corpus/instruments/claim-package-check.py:32` | `Exit status: 0 only when` |
```
`claim-gates.md` rows: G1-G5 `every gate fails closed` | `corpus/instruments/claim-package-check.py:44` | `Fail-closed (R30)`; G6 `every gate fails closed` | `corpus/instruments/r46-c1-gate.py:55` | `TARGET_GATED = 22`.

Command and output (`python3 weak/corpus/instruments/r46-c1-gate.py --root weak --baseline base`, exit 0):
```
gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-clean=2
gate L4 pass=1 read=entry-mode-green=2
gate L5 pass=1 read=append-only=2
gate L6 pass=1 read=mutants=12 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```

The exact gate line: `gate L6 pass=1 read=mutants=12 survivors=none`.

Why this is not load-bearing in the real sense: the contract claim "a claim-ready package has six files" is supported by the counter's header comment (`"""r46-c1-gate.py — round-46 C1 counter`) and an unrelated `Exit status` line in `claim-package-check.py`. Blanking those tokens does turn the counter's gate red, so L6 is satisfied, but the claim never depended on them. L6 measures "removing this token breaks the gate", not "this row supports the claim". The claims.json kill rule's non-author semantic clause fails this tree; the counter cannot.

## Finding 2: duplicate rows over one line pass L6 — `dup`

Recipe: as in Finding 1, but the contract's G1-G5 are `claim-package-check.py:101` / `SIX_FILES` (five identical rows), G6 is `claim-package-selftest.py:334` / `the graded payload is the fixture's six files`. Gates: G1-G5 `claim-package-check.py:90` / `_GATE_RULE_ORDER = (`, G6 `r46-c1-gate.py:55` / `TARGET_GATED = 22`.

Command: `python3 dup/corpus/instruments/r46-c1-gate.py --root dup --baseline base` → `gate L6 pass=1 read=mutants=12 survivors=none`, `c1-gate fixed=7/7 exit=0`.

Proof the five rows are one mutation. A script that applies the counter's own replacement (`raw.replace(tok, '#'*len(tok))`) produced:
```
claim-package-contract.md G1 corpus/instruments/claim-package-check.py:101 'SIX_FILES' occurrences_in_file=2 mutant_sha256=25fc139c141f9e4c
claim-package-contract.md G2 ... same ... mutant_sha256=25fc139c141f9e4c
claim-package-contract.md G3 ... same ... mutant_sha256=25fc139c141f9e4c
claim-package-contract.md G4 ... same ... mutant_sha256=25fc139c141f9e4c
claim-package-contract.md G5 ... same ... mutant_sha256=25fc139c141f9e4c
claim-gates.md G1-G5 'corpus/instruments/claim-package-check.py:90' ... mutant_sha256=15c2ad941f606379 (identical x5)
```
Five identical mutated trees are counted as five independently load-bearing rows; MIN_ROWS = 6 is met by padding.

## Finding 3: the scratch copy omits the entry body, so every mutant is red for the wrong reason — `sym`

Recipe: move each re-grounded entry's full text (base + recheck + section) to `corpus/lessons/<entry>` and replace `corpus/knowledge/<entry>` with a relative symlink `../lessons/<entry>`. Rows as in `dup`.

Command: `python3 sym/corpus/instruments/r46-c1-gate.py --root sym --baseline base` → `gate L6 pass=1 read=mutants=12 survivors=none`, `c1-gate fixed=7/7 exit=0`.

Discriminating control (the scratch copy L6 builds, mutation not applied):
```
symlink in scratch: True -> ../lessons/claim-gates.md
target exists in scratch: False
UNMUTATED scratch, entry-mode, rc=1
reground entry=claim-gates.md rows=0 ok=0 exit=1 read=entry-absent
```
The real tree is green for the same entry: `reground entry=claim-gates.md rows=6 ok=6 files=2 exit=0`. So every L6 mutant is red because `lessons/` was omitted, and `survivors=none` says nothing about the rows. Omitting an entry body is silently accepted; omitting an anchor fails closed (Finding 5). That asymmetry is the defect.

## Finding 4: L6 can fail alone — `split` (limb is wrong in this direction)

Recipe: as `dup`, but the claim-gates G6 row is `corpus/instruments/r46-l6-split.txt:2-3` / `delta epsilon zeta eta`, where that fixture has `delta epsilon` / `zeta eta` on lines 2-3 and the exact string `delta epsilon zeta eta` on line 10.

Command: `python3 split/corpus/instruments/r46-c1-gate.py --root split --baseline base`:
```
gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-clean=2
gate L4 pass=1 read=entry-mode-green=2
gate L5 pass=1 read=append-only=2
gate L6 pass=0 read=mutants=12 survivors=claim-gates.md:G6
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=6/7 exit=1
```
So L6 can fail alone. The cause is the replace scope: `tok in raw` is true (exact copy on line 10), so only line 10 is blanked; the normalised range on lines 2-3 still satisfies the row. The evidence the row cites is untouched, so the mutant is not a mutant of that row: a false red on a correctly supported row.

## Finding 5: fail-closed when an anchor is omitted — `omit`

Recipe: as `dup`, but claim-gates G6 anchors `corpus/instruments/lessons/l6-probe.txt:2` (directory named `lessons` under `instruments/`, omitted by the scratch copy).

Command output (exit 1):
```
gate L1 pass=0 read=exception-FileNotFoundError
...
gate L7 pass=0 read=exception-FileNotFoundError
c1-gate fixed=0/7 exit=1
```
Anchors that vanish from scratch fail every limb; entry bodies that vanish (Finding 3) pass L6. This is the asymmetry noted above.

## Constructions tried (genuine, ≥5)

1. `dup` — duplicate rows over one line, plus one second-file row per entry → L6 pass, 7/7 (Finding 2).
2. `weak` — tokens unrelated to the claim, six rows per entry → L6 pass, 7/7 (Finding 1, cheapest).
3. `sym` — entry body in omitted `lessons/`, symlinked from `knowledge/` → L6 pass, 7/7 (Finding 3).
4. `split` — multi-line token with an exact copy outside the range → L6 red alone, 6/7 (Finding 4).
5. `omit` — anchor inside an omitted directory → fixed=0/7 exception (Finding 5).
Control: do-nothing base → L6 pass=0, mutants=0, fixed=1/7.

Three of five constructions pass L6 with no real support behind the rows; the verdict is BROKEN.

## Assessment

- L6 can fail alone (Finding 4), so it is not dead weight. Its failures are scope bugs, not evidence about rows.
- L6 passes on rows that support nothing (Finding 1), on duplicate rows (Finding 2), and on a scratch tree where every mutant is red for a reason that has nothing to do with the rows (Finding 3).
- Suggested counter fixes (not implemented; no edits to shared files): (a) assert the unmutated scratch copy reads green before counting mutants; (b) mutate the anchored range only, so the replace scope is the row's own evidence; (c) require distinct (anchor, token) pairs; (d) reject symlinked entries and entries whose body lies outside the scratch copy. None of these fixes the semantic gap of Finding 1, which needs a non-author reading of the rows, as the claims.json kill rule already states.
- Verdict consequence for C1: the counter reads `fixed=7/7 exit=0` on Finding 1's tree. The `after` condition therefore cannot be established by the counter alone; the kill rule's non-author semantic clause is the only check that catches Finding 1.

## Limitations

- Only L6 and the rest of the counter were run, on this host, from the scratch tree; the freeze tree was not re-run in this seat.
- "Does not support the claim" for Finding 1 and 2 is my non-author reading of the anchored lines, not a mechanical test. The claim-gates G1-G5 rows in Finding 1 are borderline (the anchor is the round-43 gate, not the lost claim-check tool).
- Finding 4's root cause is from reading the replace logic and the survivor output; I did not instrument the scratch copy beyond that.
- Finding 5 was run on a single construction; I did not test other omitted directories (`__pycache__`).
- Freeze-controls file was read, not re-graded: its `gutted-entry` control already shows L6 pass=1, which I did not trace.
- Scratch dir removed on exit; no repo file was touched other than this report.
