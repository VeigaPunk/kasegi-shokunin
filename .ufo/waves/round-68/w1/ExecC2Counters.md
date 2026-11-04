# ExecC2Counters — round 68, C2 BEFORE state + counter behaviour

**Verdict: FINDINGS.** The C2 BEFORE state is recorded from committed bytes. At the freeze commit 7c4f9f7e the coverage counters read rows=45 / registry=101 / entries=48 / knowledge 85 lines and 83 entries / census exit 0, the same as the frozen base receipt. One counter differs from the frozen do-nothing text: at the freeze revision `capture-binding-check.py` prints **`records=82 bound=81 unbound=1` and exits 1** (`FAIL rule=no-row record=S102 dir=round-68`), not `records=81 bound=81 unbound=0`. The cause is unrelated to whether the claim holds. The S102 capture manifest landed in pre-freeze commit 3dfe6f1, and the SOURCES row S102 has not been written yet. The live tree reads the same as the freeze on every counter, so no C2 lane file has landed yet.

Receipts: `.ufo/waves/round-68/controls/seat-c2-counters-r68.txt` (sha256 `e88de40e744a2310ba09dabc1fa6a42a58a67146910c0549f4da0a4894008bc2`, 345 lines). Raw output is in `w1/ExecC2Counters/{base.out,live.out,run.sh}`: base.out sha256 `b3f35dc0…c4d3`, live.out sha256 `c064001d…4aaf`.

## What I ran
```
mkdir -p /fast/scratch/hyaku/kasegi-r68/ExecC2Counters/base
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 7c4f9f7ec096298b1edd1912249e5864ee73d985 | tar -x -C /fast/scratch/hyaku/kasegi-r68/ExecC2Counters/base
run.sh <tree> <label> <explicit-dir>   # cd <tree>; the 5 frozen commands, each followed by [exit=$?]; then sources-census.sh validate <explicit-dir>
```
I ran this on (A) the freeze export and (B) the live working tree. For context I also ran (C) the base revision d0f48405 export (capture and frontier lines only).

## Observed lines
| counter | A: freeze 7c4f9f7e export | B: live, possibly mid-edit (HEAD 82b3b7d) | frozen after-target |
|---|---|---|---|
| frontier-recheck-count | `FRONTIER-CENSUS rows=45 admitted=45 closed=45 problem-rows=0 registry=101`; last PASS line `FRONTIER-PASS F45 ids=S100,S101`; `entries=48 pass=48 exit=0` [exit=0] | identical | rows=46 registry=102, `FRONTIER-PASS F46 ids=S102`, entries=49 |
| capture-binding-check | `MANIFEST round-68 records=1 url_bound=0 fetched=1 archival=0`; `AUDIT records=82 … snapshot_dirs=41 manifest_dirs=41 … orphans=1 orphan=S040-live.txt`; `FAIL rule=no-row record=S102 dir=round-68`; `records=82 bound=81 unbound=1` **[exit=1]** | identical | records=82 bound=82 unbound=0 |
| `wc -l knowledge-expected.txt` | `85` | `85` | 86 |
| `grep -vc '^#'` | `83` | `83` | 84 |
| census `validate --root /home/vgpnk/Projects/shokunin kasegi` | 6× W04 (S028, S029, S072, S076, S080, S085), `kasegi ok …/kasegi-shokunin/corpus/SOURCES.md` [exit=0] | identical | exit 0 |
| census `validate <explicit dir>` | 6× W04 (same ids), `base ok …/ExecC2Counters/base/corpus/SOURCES.md` [exit=0] | `kasegi-shokunin ok` [exit=0] | — |

C (base d0f48405): `records=81 bound=81 unbound=0` [exit=0], `AUDIT records=81 … snapshot_dirs=40 manifest_dirs=40`, `FRONTIER-CENSUS rows=45 … registry=101`, `entries=48 pass=48 exit=0`. These match `controls/c2-base-counters-r68.txt` (header `revision d0f48405…`).

A diff of A against B, ignoring the tree-path prefix, has exactly one differing line: the explicit-dir census `ok` path. All counts are identical.

## Delta and findings
1. **Freeze ≠ base for the capture counter.** The frozen `do_nothing_control` and the `before` capture=81 were measured at d0f48405. Commit 3dfe6f1, before the freeze, added `corpus/source-snapshots/round-68/manifest.json` and `S102.txt`. So at the freeze, and live, the capture counter already counts 82 records, and S102 is unbound because SOURCES.md has no S102 row (registry=101). The counter is behaving correctly: it fails because the manifest record has no SOURCES row, not because of anything C2's admission does wrong. Consequence for the L1: the "before" for capture is 81 only at d0f48405. At the freeze it is 82/81/1 with exit 1. The after-target of 82/82/0 is still a +1 bound move, and writing the S102 row should be enough to clear the `no-row` FAIL. **[INFERENCE]** I have not run that, because there is no row yet. The frozen predicate and kill rule are unaffected. I am reporting this only so the before receipt is not read as `unbound=0` at the freeze.
2. **The census `--root` form does not read an export.** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` resolves `kasegi-shokunin` under the fleet root, so in run A it validated the LIVE SOURCES.md, not the freeze bytes. The script does accept an explicit lane directory (its usage line says "or explicit lane dirs"), and that form read the export's own SOURCES.md: `base ok`, exit 0. Both forms are in the receipt.
3. **The live tree was mid-edit during run B.** It had uncommitted tracked edits to `corpus/knowledge/first-psirt-maturity-document.md` (an appended "Corrections (round 68)" section) and `.ufo/waves/round-67/controls/driver-pins.json`. Neither file is read by these five counters. SOURCES.md, FRONTIER, the manifests and knowledge-expected.txt were not modified. Every live count equals the freeze count.
4. **Residuals I did not cause:** the persistent `orphans=1 orphan=S040-live.txt` (present at the base too, and not a FAIL) and six W04 warnings (do not change exit status).

## Bounds
No lane file was edited apart from `controls/seat-c2-counters-r68.txt` and this report and its directory. I did not run any mutating git command, did not install any tools, and used no subagents or background jobs. I removed the scratch directory /fast/scratch/hyaku/kasegi-r68/ExecC2Counters before yielding.
