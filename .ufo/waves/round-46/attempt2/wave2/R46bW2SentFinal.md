# R46bW2SentFinal — final integrity pass on the landed tree

VERDICT: BROKEN

Tree attacked: HEAD `96379ae26ef9443097b860ddb33ef924b2cd5b5a` ("wave-1 integration"). The assignment names `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4` as the integration; that commit is the freeze (`fe0f56b round-46 (attempt 2): freeze claims ...`). I attacked 96379ae (it carries the 5 new and 4 changed instruments) and checked fe0f56b for the frozen-before inputs. Exports were made with `git archive` into scratch; nothing was committed, pushed, or mutated, and no tool was installed.

Summary: read-only-on-root HOLDS for every instrument I ran. Tree-supplied execution HOLDS for the allow-list (12 hostile recheck shapes, none executed). No credentials or session material found in the wave dir. Integrity is BROKEN on: (1) `r46-counters-selftest-c2.py` cannot run at HEAD (import-time NameError), so the frozen battery's C2 side prints BASELINE-DIRTY; (2) the errata claim that the dead `--pure` defaults were fixed is false; (3) the `--pure` input the selftests and battery require is an unpinned scratch export, not the base commit; (4) the F29 selftest cannot grade the landed lane.

## 1. Read-only on `--root` — HOLDS (for what I ran)

Method: `T0` = `git archive 96379ae` copy. Before: sha256 of all 9939 regular files plus the entry list (11035 entries). Every instrument was run with `--root`/`--lane` pointed at T0 under `python3 -B`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` and `HYAKU_SCRATCH` set into my scratch. After all runs: `T0-HASH-IDENTICAL-after-all-runs` and `T0-LIST-IDENTICAL`. Base export `04af9bc` re-checked against a fresh archive: `BASE-EXPORT-UNCHANGED-vs-fresh-archive`.

| run (T0 unless noted) | exit | output |
|---|---|---|
| `r46-f29-gate.py --root T0` | 0 | `f29-gate fixed=7/7 exit=0` |
| `r46-f29-gate.py --root base` | 1 | `f29-gate fixed=1/7 exit=1` (do-nothing reading) |
| `r46-c2-gate.py --root T0` | 1 | `c2-gate fixed=5/7 exit=1` (G1 `rows=29`, G6 `knowledge=66 ... base-intact=0`) |
| `r46-c2-gate.py --root base` | 0 | `c2-gate fixed=7/7 exit=0` |
| `r46-c1-gate.py --root T0 --baseline base` | 1 | `c1-gate fixed=2/7 exit=1` (`gated=22 broken=0 lines=66/base=65`) |
| `r46-c1-gate.py --entry ...` | 1 | `reground entry=github-private-vulnerability-reporting.md rows=0 ok=0 exit=1` (wrong entry for C1; not a defect) |
| `r46-counters-selftest-c1.py --lane T0 --pure <914ca0b export>` | 0 | `selftest cases=83 failures=0` (`residual-false-greens=1`, disclosed) |
| `r46-counters-selftest-c2.py --lane T0` | 1 | `NameError: name 'C1_ENTRIES' is not defined` (no tree write: crash at import) |
| `r46-selftest-f29.py --lane T0` | 1 | `selftest: lane README carries 29 frontier rows, expected 28` |
| `r46-mutbat.py --root T0 --counter c2` | 1 | `mutbat counter=c2 BASELINE-DIRTY baseline_failures=-1` |
| `r46-mutant-equivalents/m14-equivalence-differential.py` (T0 as both counters) | 0 | `m14-equivalence trees=15 differing=0` (trivially identical: both arguments were the same counter; a smoke run, not the differential) |

Not run: `r46-mutbat.py --counter c1` (20 mutants, long; other seats run it). I statically read its writes: `apply_mutant` writes only into `mdir` under `--work` (`r46-mutbat.py:174-176`); `f29_build_fixture_corpus` writes only into `work` (`:241-252`).

Do-nothing discrimination: the same instruments reading `base` versus T0 give different verdicts (f29 1/7 vs 7/7; c2 7/7 vs 5/7), so the readings are tree-sensitive, and none of them touched the tree.

## 2. Tree-supplied execution — HOLDS for the allow-list

Only `r46-c1-gate.py` `classify()` executes lines taken from the tree (`recheck:` lines, `r46-c1-gate.py:225-243`): `bash -n`, then `allowed()`, then `bash -c` with `cwd=root`, env minimal (`HOME PATH TMPDIR LANG`). The c2 and f29 gates run only fixed commands whose paths come from `__file__` (`TOOL_ROOT`, `INSTRUMENTS`), and the census call `bash CENSUS validate --file <root>/corpus/SOURCES.md` is an argument list, not a shell string.

I copied T0 to a scratch tree P, put 12 hostile `recheck:` lines in 12 scratch entries, each writing a marker file into a marker directory on success, and ran `classify()`:

```
zz-probe-h1.md  broken     (`; touch M`)
zz-probe-h2.md  broken     (`test -d . && touch M`)
zz-probe-h3.md  executes   (`test -d . # && touch M`: comment strip; marker absent)
zz-probe-h4.md  executes   (`cd P || touch M && test -d .`: cd-prefix strip; marker absent)
zz-probe-h5.md  broken     (`cd P & touch M && test -d .`)
zz-probe-h6.md  broken     (`--label "$(touch M)"`)
zz-probe-h7.md  broken     (`| grep -x 'z'; touch M`)
zz-probe-h8.md  gated      (`r46-c1-gate.py --entry ... --work M8dir`: no dir created)
zz-probe-h9.md  broken     (`--label $HOME`)
zz-probe-h10.md executes   (`source-recheck.py --selftest`: writes only to TMPDIR tempdir)
zz-probe-h11.md broken     (`python3 -c 'print(1)'`)
zz-probe-h12.md broken     (`--label "a && touch M"`)
markers: []
```

Direct `allowed()` probes: `test -d . && touch /x` False; `test -d . ; touch /x` False; `python3 corpus/instruments/density.py a 'b && c'` False; `density.py a<TAB>b` False; `git -C ~/Projects/x rev-parse HEAD` True (read-only); `source-recheck.py --selftest` True (writes only to its own tempdir).

Real tree: `classify` over T0 gives `broken=0`, so the allow-list rejects nothing in the committed entries.

Residuals (not defects of the allow-list, but disclosed):
- Allowed shapes let a tree name any path under the grader's HOME (`density.py ~/...`); the only channel is exit status (an existence oracle).
- The battery and both selftests execute the tree's own Python (`python3 -I <root>/corpus/instruments/r46-counters-selftest-*.py`, `r46-selftest-f29.py`). That is outside any allow-list by design: `--root` must be trusted.

## 3. Scratch and absolute paths — BROKEN (the named defects are still there; the errata is wrong)

`grep -rnE '/fast/|/tmp/' corpus/instruments` (landed): executable literals are listed below. `/tmp/` hits are docstrings or data only (`README.md:4,31`, `density.py:6-7`, `resolve.py:10,43`, `citation-survival.tsv`).

The two known dead PURE defaults:
- `r46-counters-selftest-c1.py:57` `PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"` and `:649` `ap.add_argument("--pure", default=PURE)`.
- `r46-counters-selftest-c2.py:54` `PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"` and `:459` `ap.add_argument("--pure", default=PURE)`.
- Dead: `ls /fast/scratch/hyaku/kasegi-r46/L1/pure` → `No such file or directory`. Running c1 without `--pure`: `FileNotFoundError: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kasegi-r46/L1/pure'` (`exit=1`).

Third, not named by the errata: `r46-mutant-equivalents/m14-equivalence-differential.py:38` `PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure2"` (a volatile scratch dir, 448 files; hard-coded, unpinned). It also hard-codes `LANE` at line 31.

The errata claim is false. `.ufo/waves/round-46/attempt2/counter-errata.md:44-45`, under `### E2` (line 35), reads: "Both dead `--pure` defaults now point at the committed map pattern (SentScratch F1 fix: `--pure` required, no dead absolute default)." The code shows `default=PURE` in both selftests, and `--pure` is required only in `r46-mutbat.py:374` (its own flag). So the fix did not land, and the errata misdescribes the state. Fix or name: neither was done.

Other absolute paths in the new or changed instruments:
- `r46-mutbat.py:141-144` and the duplicate `:181-184`: `F29_DRAFT_SELFTEST` and `F29_CONTROLS_ABS` point at `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/...` and `.../attempt2/controls`. Defined twice; the draft fallback is reached only when `--counter f29`, which `--counter both` never runs.
- `r46-f29-gate.py:102` and `r46-c2-gate.py:60`: `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`. This is a fleet-root script outside the lane, executed by H7/G7, and not pinned (`PINS` has no entry for it; its sha256 today is `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`). The gate's verdict changes if that file changes.
- `LANE` constants (`r46-f29-gate.py:72`, `r46-c2-gate.py:76`, `r46-c1-gate.py:61`, both selftests) are hard-wired into the pinned recheck shape `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ...`. A clone elsewhere fails the gate. Design choice; recorded as a portability limit.

## 4. Credentials and session material in the wave dir — HOLDS (none found)

- Token shapes (`ghp_`, `github_pat_`, `gho_`, `AKIA`, PEM headers, `xox[baprs]-`, `sk-ant-`, `sk-` 32+, `AIza`): 0 matches.
- `op://`: occurs only as prose in dispatch and rules text (for example `wave1-dispatch.json`: "No credential material, session URLs or op:// references in anything you write"). Not a reference.
- Assignment-shaped strings are deliberate fixtures: `bearer: abcdefghijklmnop1234` (`wave1/R46CritSoftening.md`), `api_key: abcdefghijklmnopqrstuvwxyz0123` (`wave2/R46W2RevGroundGates3.md`), a `"api_key": "0123456789abcdef..."` fixture line (same file).
- Environment dumps show names only: `SSH_AUTH_SOCK=set`, `GITHUB_TOKEN=unset` (`wave1-results.json`, `wave1/R46SentinelGate.md`).
- Session material: no `sessionId`, `session_id`, `sessionFile`, `.omp/agent/sessions`, `Set-Cookie`, `x-api-key`, `Bearer <token>`, or signed URLs (`?token=`, `?sig=`, `?session=`).
- `wave2/swarm-registry.json` (untracked, mode 600): 32 `"agentId": null`, no session or token fields.

## 5. Defects found while running (each reproduced in scratch)

D1. `r46-counters-selftest-c2.py` does not run at HEAD. `EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}` is at line 68 and `C1_ENTRIES = {...}` at line 69. Output: `NameError: name 'C1_ENTRIES' is not defined`, `exit=1`, with any `--lane`/`--pure`. The lane's own `controls/final-battery.txt` records the same NameError under "selftest c2 (extended+ledger)" with `exit=0` (pipeline masking). Effect: `r46-mutbat.py --counter c2` (and therefore the frozen `--counter both`) prints `mutbat counter=c2 BASELINE-DIRTY baseline_failures=-1`. The C2 side of the frozen battery cannot produce `caught+equivalent=21`.
  Scratch-only test (swap lines 68/69 in a copy, not committed): `selftest cases=147 failures=101 exit=1`, with `FAIL control ctl-complete-tree fixed=6/7 failing=['G2']` (18 control FAILs, 83 mutant FAILs). So even repaired, the landed v1.3 selftest is red on the landed tree (its controls expect 7/7; the landed counter reads 5/7). The receipt `wave1/R46bExecGatePinAmend.draft/receipts/selftest-v13.txt` ends `selftest cases=137 failures=0`, which is the v1.2 count, not the landed 147.

D2. The `--pure` input is unpinned and not the base commit. Against the base export as `--pure`:
  - `r46-counters-selftest-c1.py` (base file, base lane, `--pure base`): `AssertionError: mutation was a no-op on corpus/knowledge/claim-gates.md`.
  - `r46-counters-selftest-c2.py` (base file, `--pure base`): `AssertionError: claim-gates.md`.
  The working `--pure` is `/fast/scratch/hyaku/kasegi-r46/L1/pure2`: its `corpus/knowledge` and `corpus/instruments` equal `git archive 914ca0b` (round-45 commit) exactly; it differs from base 04af9bc by the two attempt-1 C1 re-ground files and the F28 entry. With a `914ca0b` export as `--pure`, the landed C1 selftest passes `cases=83 failures=0 exit=0` (D3). So the claims' do-nothing control ("selftests untouched at base", `claims.json` C1 `expect_before`) is not reproducible from the base commit alone; it needs a pre-round pure export that is not pinned in the claims or the frozen `counter_cmd`.

D3. Positive control: `r46-counters-selftest-c1.py --lane T0 --pure <914ca0b export> --work ... --jobs 8` → `selftest cases=83 failures=0`, `exit=0`. The 83-case C1 selftest is therefore green on the landed instruments, given that pure export. Its T0 tree was unchanged (hash check above).

D4. `r46-selftest-f29.py` cannot grade the landed lane. `--lane T0` → `selftest: lane README carries 29 frontier rows, expected 28`, `exit=1`. `--lane base` fails earlier: `FileNotFoundError: .../base/corpus/source-snapshots/round-46-a2/S074.txt` (the snapshot is new). With a scratch view that removes the F29 row and entry (28 rows) and uses the landed counter: `selftest cases=30 failures=0`, `exit=0`. So the F29 selftest is green only on a pre-landing view, not on the landed lane.

D5. `r46-mutbat.py` does not hand `--root` to the C2 selftest: `run_selftest` passes `--pure` only for c2 (`r46-mutbat.py:152-160`, `:222`), so the selftest's `--lane` defaults to the live lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. C2 then copies its snapshot and knowledge entries from the live lane (`r46-counters-selftest-c2.py:473, 480, 499, 540`), not from the tree under test. The C1 selftest's recheck lines are also hard-wired to `cd LANE` (`r46-counters-selftest-c1.py:133`). For the current tree the corpus equals the live lane's, so this does not change today's numbers, but the battery is not hermetic to `--root`. (Code-cited; I did not run a corpus-perturbed comparison because the C2 selftest has the NameError in D1.)

D6. Equivalence proofs: `r46-mutbat.py:361` and `:416` test `os.path.isfile(eq[mid])`. The map values are relative to the process cwd, not to the map or the tree, and `isfile` does not check non-empty (the C1 kill rule says "missing, empty"). All four proof files are present and non-empty today (`682` and `3560` bytes), so no verdict changes now; a run from another cwd would turn equivalents into `uncaught` silently.

D7. Minor: `r46-mutbat.py` defines `F29_DRAFT_SELFTEST` and `F29_CONTROLS_ABS` twice (lines 141/181, 144/184).

## 6. Limitations

- Not run: the full `r46-mutbat.py --counter c1` (20 mutants) and `--counter both`. Their verdicts are for other seats; my read-only claim for mutbat covers its C2 path plus a static reading of its c1 writes.
- The c1 selftest result (D3) used a `914ca0b` export as `--pure`, verified equal to `pure2` for `corpus/knowledge` and `corpus/instruments` only (the rest of `corpus/` was not compared). The `pure2` dir itself was not used.
- The `m14` run compared a counter with itself; it is a smoke run, not the differential.
- The live lane was read only (`git status`, `git ls-files`, `grep`); I did not write to the live lane, `.ufo/state`, MANIFEST, the fleet repo, or shokuknow.
- The census script `scripts/sources-census.sh` was executed by the gates (read-only use); I did not audit its contents beyond its sha.
- Credentials review is pattern-based on the wave dir (tracked and untracked); it does not cover `~/.omp` or host credential stores, which I did not read.
