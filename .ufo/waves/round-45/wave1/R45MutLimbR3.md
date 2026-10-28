VERDICT: BROKEN

# R45MutLimbR3 — C1 mutation test of limb R3 (selftest token, SKILL registry rows, README row)

Target: `corpus/instruments/r45-routed-defects.py` limb R3 (`limb_r3`, lines 187-207).
Counter under test: sha256 `82004c700decbc3453baa57919ccff71cbfe322a8d2a71b558d75951c24f04ee`, identical to the git-tracked lane file (sha256sum of the lane copy, same hash). Copied to scratch and run from there; not edited.
Base: `git -C <lane> archive dc5bb8c6e31efc4a6650819df85e79b72fd64bcd` exported to scratch (`base/`); used as `--baseline`.
Hand-built satisfied tree: base + a selftest added to `corpus/instruments/r44-frontier-count.py` (8 cases, prints `selftest cases=8 failures=0`) + a 3-row `## Round-45 Gates & probes registry addition` section appended to `SKILL.md` + one row `r44-frontier-count.py` appended to `corpus/instruments/README.md` + a copy of `corpus/source-snapshots/round-45`. The base has no `--selftest` (`base-R44-has-selftest=False`), so the satisfied tree is synthetic; the survivors below depend on the counter's parsing, not on the selftest body.

## Survivors (counter does NOT reject while the defect is present)

### S1 — M4-second-contradicting-token (defect: gate reports failures=3 and failures=0)
- Edit (one inserted line in `corpus/instruments/r44-frontier-count.py`, directly before `    return 0 if failures == 0 else 1` inside `selftest()`):
  `    print("selftest cases=8 failures=3")`
- Direct run of the mutant's selftest (`rc=0`):
  ```
  selftest cases=8 failures=0
  selftest cases=8 failures=3
  ```
- Counter: `mutant=M4-second-contradicting-token rejected=0 r3-read=selftest-cases=8 counter-exit=1`
- Cause: `r45-routed-defects.py:183` uses `re.search` (first match only); no check that the token appears once or that later tokens agree.

### S2 — M5-loop-runs-zero-cases (defect: selftest executes zero cases but claims 8)
- Edit in `corpus/instruments/r44-frontier-count.py`: `    for name, body, want in SELFTEST_CASES:` → `    for name, body, want in SELFTEST_CASES[:0]:`
- Direct run (`rc=0`): `selftest cases=8 failures=0` (and no `selftest case=` lines).
- Counter: `mutant=M5-loop-runs-zero-cases rejected=0 r3-read=selftest-cases=8 counter-exit=1`
- Cause: `N` is self-reported on stdout; the limb never counts executed `selftest case=` lines against N (lines 183, 191).

### S3 — M6-registry-cell-escaped-pipe (defect: wave-registry row has 7 real cells, GFM `\|` not a delimiter)
- Edit in `SKILL.md` line 1151: `| none | registry file | write-once |` → `| none \| registry file | write-once |`
- Printed row: `| wave-registry.py | emitter | ... | writes \`wave=\`, \`lane=\` | none \| registry file | write-once | kasegi |`
- GFM-aware cell count (escaped `\|` kept inside the cell): `gfm-cells=7` for this row; `gfm-cells=8` for the satisfied row. Naive `split("|")` count: `naive-split=8`.
- Counter: `mutant=M6-registry-cell-escaped-pipe rejected=0 r3-read=selftest-cases=8 counter-exit=1`
- Cause: line 202 `len(rows[0].strip().strip("|").split("|")) != 8` counts the escaped pipe as a delimiter, so a single-edit replacement of a separator with `\|` keeps the naive count at 8.

## Rejected mutants (counter behaves as intended)
- M1-selftest-case-fails — `one-open` expectation `(1, 0)` → `(1, 1)`: `mutant=M1-selftest-case-fails rejected=1 r3-read=selftest-rc=1-tokens=(8, 1)`
- M2-selftest-drops-case-to-7 — delete the `dup-ids` case tuple: `mutant=M2-selftest-drops-case-to-7 rejected=1 r3-read=selftest-rc=0-tokens=(7, 0)`
- M3-token-leading-space — `print(f"selftest cases=…` → `print(f" selftest cases=…`: `mutant=M3-token-leading-space rejected=1 r3-read=selftest-rc=0-tokens=None`
- M7-registry-heading-demoted — `## Round-45 Gates …` → `### Round-45 Gates …`: `mutant=M7-registry-heading-demoted rejected=1 r3-read=registry-section-absent`
- M8-readme-row-removed — delete the README `r44-frontier-count.py` row: `mutant=M8-readme-row-removed rejected=1 r3-read=readme-row-absent`

## Controls and discrimination
Command (from scratch): `TMPDIR=$SCR/tmp python3 recipe.py` (exit 0; full output retained in scratch, reproduced in the lines quoted here).
- C0 do-nothing base (`--root base --baseline base`): `control C0-do-nothing-base R3=(0, 'selftest-rc=2-tokens=None') counter-exit=1`
- C1 satisfied, unmutated: `limb R3 fixed=1 read=selftest-cases=8`; direct selftest `rc=0`, eight `selftest case=<name> verdict=pass` lines then `selftest cases=8 failures=0`.
- Verdict table: 5 rejected, 3 survived — `summary mutants=8 rejected=5 survived=3`.

## Extra finding — false reject of a valid row (E1)
- E1 = satisfied tree with the `r44-frontier-count.py` verdict cell written as `exit=0\|1` (the same GFM-escaped convention SKILL.md already uses, e.g. `closed=0\|1` in the round-42 row).
- GFM cells = 8, naive split = 9. Counter: `control E1-valid-escaped-pipe-row R3=(0, 'registry-row-r44-frontier-count.py=1')`. A valid row is rejected, and the read token `registry-row-…=1` reports the row count (1), not the failing cell count.
- Same naive count on the lane's existing round-42/43 rows: `SKILL.md:1134` and `:1143` each give `naive-cells=10` (awk NF-2 on the `|` split), so the predicate as written cannot accept the file's own escaped-pipe convention.

## Probe of a stricter R3 predicate (scratch only; the counter was NOT edited, nothing committed)
Stricter checks evaluated in a standalone scratch script: exactly one `selftest cases=N failures=M` line, N >= 8, M = 0; the number of `selftest case=… verdict=pass` lines equals N; registry rows counted by a GFM-aware split (escaped `\|` kept in cell) must be 8.
```
proposed-R3 tree=satisfied: accept selftest=8
proposed-R3 tree=M1-selftest-case-fails: reject selftest tok=[('8', '1')] rc=1
proposed-R3 tree=M2-selftest-drops-case-to-7: reject selftest tok=[('7', '0')] rc=0
proposed-R3 tree=M3-token-leading-space: reject selftest tok=[] rc=0
proposed-R3 tree=M4-second-contradicting-token: reject selftest tok=[('8', '0'), ('8', '3')] rc=0
proposed-R3 tree=M5-loop-runs-zero-cases: reject case-lines=0 claimed=8
proposed-R3 tree=M6-registry-cell-escaped-pipe: reject row wave-registry.py rows=1 gfm=[7]
proposed-R3 tree=M7-registry-heading-demoted: reject section-absent
proposed-R3 tree=M8-readme-row-removed: reject readme
proposed-R3 tree=E1: accept selftest=8
proposed-R3 do-nothing-base: reject selftest tok=[] rc=2
```
This closes S1-S3 and E1 in the probe; it is not a repair draft and is not committed.

## Limitations
- Single-edit mutants only (8 by assignment); no multi-edit combinations, and no mutation of the SKILL append-only check or the `\Z` section boundary.
- Survivor classes depend on the counter trusting stdout: a gate that prints fabricated `selftest case=… verdict=pass` lines would survive the proposed probe too. I did not construct that mutant (it needs a multi-line edit); it is an unmeasured residual.
- The satisfied tree is synthetic (base has no r44 selftest). I did not inspect the lane's current working-tree `r44-frontier-count.py`/`SKILL.md`, and did not run the counter on the live lane tree.
- The stricter predicate was run only on the scratch trees; it has no committed artifact and no independent review.
- Scratch `/fast/scratch/hyaku/kasegi-r45/R45MutLimbR3/` is removed on exit; the outputs quoted above are the retained evidence.
- Nothing was committed, pushed, or mutated in git/jj/index; no shared production file was touched. No tools were installed.
