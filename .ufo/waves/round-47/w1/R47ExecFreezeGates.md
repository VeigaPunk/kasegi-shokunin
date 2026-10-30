# R47ExecFreezeGates — counter/freeze evidence

## Scope and checks

- `python3 -m py_compile` on `corpus/instruments/r47-routed-defects.py`, `r47-f30-gate.py`, `r47-counters-selftest.py`, and `r47-mutbat.py` exited 0 (no output).
- Neither counter accepts `--selftest`: `r47-routed-defects.py --help` lists only `--root`, `--baseline`, `--work`; `r47-f30-gate.py --help` lists `--root`, `--work`. Both attempted `--selftest` calls returned argparse errors requiring `--root`. Selftest is instead provided by `corpus/instruments/r47-counters-selftest.py` (`--base`, `--work`, optional `--counter`, `--gate`, `--keep`; lines 484–491).
- Ran the separate selftest against the current lane tree with an isolated work directory under `/fast/scratch/hyaku/kasegi-r47/R47ExecFreezeGates/` (removed by shell EXIT trap). Exact terminal: `selftest cases=43 failures=0 exit=0`. This includes c1-green (`total=11 fixed=11 unresolved=0 exit=0`) and c2-green (`fixed=7/7 exit=0`) controls plus their specified negative mutations; all 43 cases reported `ok=1`.
- Ran the counters against the current lane tree with isolated `--work` locations. C1 output: `routed-defects total=11 fixed=2 unresolved=9 exit=1`; L7 and L11 alone were fixed. C2 output: `f30-gate fixed=2/7 exit=1`; H4 and H7 alone passed. These are current-tree measurements, not frozen-base/do-nothing measurements. The c1-green and c2-green synthetic fixture controls in the separate selftest pass; no claim that the actual working tree is green.
- No full mutation battery was run. Per supplied receipt, 35/19/16 (C1) and 21/3/18 (C2) remain the disclosed caught/uncaught counts; this work does not close or reinterpret the 34 survivors.

## Working-tree scope observation

Read-only `git status --porcelain=v1 --untracked-files=all` in the lane showed these untracked paths:

```
.ufo/waves/round-47/assimilation/collisions
.ufo/waves/round-47/assimilation/reg-ids
.ufo/waves/round-47/assimilation/staged-ids
.ufo/waves/round-47/w1/R47ScoutS076Live.draft/committed-vs-live.diff
.ufo/waves/round-47/w1/R47ScoutS076Live.draft/live-1.txt
.ufo/waves/round-47/w1/R47ScoutS076Live.draft/live-2.txt
.ufo/waves/round-47/w1/R47ScoutS076Live.draft/receipt.json
.ufo/waves/round-47/w1/swarm-registry.json
.ufo/waves/round-47/wave1.ready.partial
corpus/lessons/round-47.md
```

`git diff --name-only` and `git diff --cached --name-only` printed nothing. This observed set is not the specified expected set (which also names the counter/source changes); report as a freeze-scope discrepancy, not as an assertion about concurrent sibling activity. The `w1` tree can change while fleet seats run.

## Hashes at observation

From `sha256sum`:

```
e6ede7b668155fc173ad9a1c0f83168f173d6c31b12ecb85da406e1660424aee  corpus/instruments/r47-routed-defects.py
563d52b827acf3afe269a0079f76ba7b208cefed69c14ff24ea47b86030e6b3b  corpus/instruments/r47-f30-gate.py
4c7c0aab5b5eb3885965bd9e0ec3c1b8ddda7f3f393af6a3863c6eeea6347ec4  corpus/instruments/r47-counters-selftest.py
eda81d5d4162d8732ce333867c6e3efcf806e5947c81f886454771e6c5f8c8d3  corpus/instruments/r47-mutbat.py
```

The read-only disk guard reported `/fast/scratch/hyaku` free `375.1G`; no tool was installed. No source, index, commit, or shared-production file was changed by this seat. Scratch fixtures were removed with the EXIT trap.
