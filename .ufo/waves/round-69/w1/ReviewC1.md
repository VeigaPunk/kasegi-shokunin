VERIFIED

Seat ReviewC1-14, round-69 falsification wave, C1 only. All four assigned checks reproduce from committed bytes; every number below comes from a command I ran in this seat. Raw receipts: `.ufo/waves/round-69/w1/ReviewC1/01..06`. Scratch `/fast/scratch/hyaku/kasegi-r69/ReviewC1/` removed before yield. No lane file touched; no git mutation in the lane (read-only `git archive`/`log`/`diff` only). No tools installed (nothing to record under the tooling authorization).

## 1. Committed-bytes integrity and pins (receipt 01)

Exported `corpus/instruments` and `.ufo/waves/round-69/controls` with `git archive 1bd01ee1e6558925e23d3d27a4bb12b88f502656 | tar -x`, and `claims.json` + controls from the freeze commit `9b877fd916308e948b865c44ebc76e6ad322d6a7` the same way.

- `corpus/instruments/figure-audit.py` sha256 `c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde` = prompt value = pins-r69.txt line `candidate_trial_gate c09b0fb1... (working copy, not committed before this freeze)`.
- `.ufo/waves/round-69/controls/c1-probe-run-r69.py` sha256 `eb254588976f783008ff333f07b775de2a50c827bc22c7a2fe53477ed2f1d618` = prompt value = pin line `counter eb254588...`, byte-identical at the freeze commit and the implementation commit.
- `.ufo/waves/round-69/controls/base-gate-656272cf.py` sha256 `10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8` = prompt value = pin line `base_gate 10c87100...`.

The counter's argparse confirms `--lane` defaults to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, matching the frozen `counting_command` (no `--lane`).

## 2. Frozen predicate — candidate mode, default lane (receipt 03)

Command: `python3 -B <export>/.ufo/waves/round-69/controls/c1-probe-run-r69.py --gate <export>/corpus/instruments/figure-audit.py --work /fast/scratch/hyaku/kasegi-r69/ReviewC1/final-live --mode candidate` (no `--lane` → live lane). Observed, verbatim key lines:

```
MEASURE P1-sort-compress-prefix-equals ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE P2-sort-compress-prefix-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE P3-sort-output-prefix ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE P4-sort-bundled-short-o ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE P5-git-show-commit-form ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE P6-git-show-message-search ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE P7-git-cat-file-textconv ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE P8-git-cat-file-filters ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE read-only-controls-admitted ok controls=9 failed=0
MEASURE selftest ok selftest cases=86 failures=0 rc=0
MEASURE mutbat ok rc=0 mutbat killed=5/5 survivors=0 invalid=0 controls=pass
MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 rc=0
MEASURE no-write-side-effect ok fixture_changed=0 marker_runs=0
VERIFY measurements=13 failures=0 gate_sha256=c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde mode=candidate
EXIT=0
```

Exactly the frozen predicate: `VERIFY measurements=13 failures=0`, exit 0, host sort is GNU coreutils 9.12 (the counter invokes `sort` via subprocess without a shell, so it gets `/usr/bin/sort`, not any shell builtin).

## 3. Same counter with `--lane <export>` (receipt 02)

`VERIFY measurements=13 failures=1 gate_sha256=c09b0fb1... mode=candidate`, EXIT=1. The single FAIL is `MEASURE real-ledger FAIL FIGURE-AUDIT figures=35 ok=0 stale=35 exit=1 rc=1`; all other twelve measurements pass on the exported bytes. Root cause (receipt 06): a `git archive` extraction has no `.git`, and the two archived paths omit the ledger's other referenced lane files, so none of the 35 derives can run — the committed ledger's derives are `git show <sha>:...`/`git ls-tree <sha>` plus working-tree reads of corpus and `.ufo/waves/round-5x/controls` files. Environmental, not a gate or counter defect. This is why the run in section 2 (default lane, which has git history) is the canonical predicate invocation, and it passes.

## 4. Do-nothing control — base gate, `--mode base` (receipt 04)

Command: same counter, `--gate <export>/.ufo/waves/round-69/controls/base-gate-656272cf.py --work .../final-base --mode base`. Observed: P1/P2 `FAIL rc=1 refused=0 marker_runs=18288`, P3/P4 `FAIL ... wrote=1`, P5-P8 `FAIL ... marker_runs=1`, `selftest FAIL selftest cases=77`, `no-write-side-effect FAIL fixture_changed=1 marker_runs=36580`, `VERIFY measurements=13 failures=10 gate_sha256=10c87100... mode=base`, EXIT=1.

My run is line-for-line identical to the committed receipt `.ufo/waves/round-69/controls/c1-base-donothing-r69.txt` (same HOST line included; its trailing `rc=1` = my `EXIT=1`), and matches claims.json's do_nothing_control prose exactly (compressor 18288×2, P3/P4 write, textconv/smudge driver runs, selftest pins 77, failures=10, exit 1).

## 5. Commit order and no implementation byte before the freeze (receipt 05)

`git log --format='%H %cI %s' 656272cf6b753fab7ce249f286b824c87677fdf3..981115648e4108e1adf5aec010edadac285a0c78` (newest first):

```
981115648e4108e1adf5aec010edadac285a0c78 2026-11-04T19:33:07-03:00 round-69: F47 GitHub global security advisories REST API admission on S103 (C2)
1bd01ee1e6558925e23d3d27a4bb12b88f502656 2026-11-04T19:32:02-03:00 round-69: derive gate refuses long-option abbreviations, sort -o bundles, git show commit operands and git cat-file --textconv/--filters (C1)
9b877fd916308e948b865c44ebc76e6ad322d6a7 2026-11-04T19:31:53-03:00 round-69: freeze C1 enumerated program-execution/write refusal (P1-P8) and C2 F47/S103 frontier admission
4d91dcd3f3cfdb3bad0324ac20c30bce489eee61 2026-11-04T19:31:41-03:00 round-69: pre-freeze controls (C1 counter, base no-work, blanket-refusal forgery, candidate trial), C2 base counters, S103 capture input and EUVD refusal receipt
```

Freeze `9b877fd9` (19:31:53) precedes implementation `1bd01ee` (19:32:02). `git diff 4d91dcd3f3cfdb3bad0324ac20c30bce489eee61 9b877fd916308e948b865c44ebc76e6ad322d6a7 -- corpus/instruments/figure-audit.py` printed nothing (empty output between markers) — no gate byte was committed before the freeze, consistent with the pin's "(working copy, not committed before this freeze)".

## Residuals / observations

- No failure of any frozen measurement. Within the enumerated scope (P1-P8, nine positive controls, selftest 86, mutbat, real-ledger 35/35, no-write-side-effect) C1 is VERIFIED; verdict per the kill rule: no MEASURE FAIL on the canonical run, exit 0, VERIFY line present.
- Observation for the depth:verifiability axis (not a defeat): the counter cannot reach `failures=0` from a bare `git archive` of the two pinned paths alone — the real-ledger limb needs a lane checkout with git history (and the non-git ledger rows need lane files outside the archived paths). The frozen counting_command works because it uses the default live lane. If the wave wants byte-only reproducibility, the counter would need a lane-with-history input (e.g. `clone --shared` into scratch) documented in the claim; L1 may weigh or waive this.
- I did not hunt for program-execution shapes beyond the enumerated set (attack seats own that per the kill rule); nothing here supports or refutes class saturation.

Verification gaps: none material. Every output above was produced in this seat; full verbatim transcripts in receipts 01-06.
