# MutateC1 — round 71 attempt 2: one-limb mutation probe of the derive gate's refusal rules

Seat: mutation-tester (leaf; no subagent dispatch). Lane tip `3cc8cd45cb6f8ca49a292f3b2647c5bddac71486`.
Gate under test `corpus/instruments/figure-audit.py` sha256
`182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603` (952 lines) — reproduced by the
clone, so the bytes measured are the frozen claim bytes. All clones, fixtures, mutants and receipts
lived in `/fast/scratch/hyaku/kasegi-r71/MutateC1` (removed at yield). No mutating git/jj command ran
anywhere; the only git calls were `clone --shared` + `checkout <tip>` inside scratch.

## 1. Setup and baseline

```
$ git -C kasegi-shokunin clone --shared kasegi-shokunin $S/clone
$ git -C $S/clone checkout 3cc8cd45cb6f8ca49a292f3b2647c5bddac71486
HEAD is now at 3cc8cd4 kasegi r71: late seat output (ScribeLesson round-71 lesson draft + report) after wrap-up; not a landed round
$ sha256sum $S/clone/corpus/instruments/figure-audit.py
182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603  .../corpus/instruments/figure-audit.py
$ python3 -B corpus/instruments/figure-audit.py --selftest
selftest cases=106 failures=0
EXIT=0
```

Each mutant is a full copy of the real `corpus/instruments/` tree at `$S/mutants/<id>/corpus/instruments/`
(so the `python-census-covers-instruments` limb still sees a real instrument set — the gate's basename
stays `figure-audit.py`), with exactly one rule removed by one string replacement. Every mutant
compiles (`py_compile`, `doraise=True`); each diff against the pristine gate is one hunk.

Selftest invocation per mutant, exactly:

```
$ cd $S/mutants/<id> && HYAKU_SCRATCH=$S/work/<id> TMPDIR=$S/work/<id> \
    python3 $S/mutants/<id>/corpus/instruments/figure-audit.py --selftest
```

## 2. Kill matrix (15 assigned mutants)

| # | mutant | rule removed (diff) | gate sha256 (16) | selftest exit | cases | failures | failing selftest case (observed line) | counter | verdict |
|---|---|---|---|---|---|---|---|---|---|
| M1 | `--selftest` out of `PY_DENIED_ANY` | `("-out","--output","--selftest")` → `("--out","--output")` | cacba1a4f79e5f6f | 1 | 106 | 1 | `python-selftest-refused exit=1 want=2` | not run | **killed** |
| M2 | `--output` out of `PY_DENIED_ANY` | → `("--out","--selftest")` | 6bfc80de6a7ab77a | 1 | 106 | 1 | `python-output-long-refused exit=1 want=2` | not run | **killed** |
| M3 | short `-o` arm of `python_flags_ok` | `if tok == "-o" or tok.startswith("-o"): return False` deleted | 36a266001d75820a | 1 | 106 | 1 | `python-short-o-refused exit=1 want=2` | not run | **killed** |
| M4 | `PY_HEAD_REFUSED` entry | `("frontier-recheck-count.py",)` → `()` | 81020b26a0e8b60d | 1 | 106 | 1 | `python-no-option-head-refused exit=1 want=2` | `measurements=25 failures=4` exit 1 | **killed (both)** |
| M5 | `capture-source.py --url` | `("--url","--work","--scratch")` → `("--work","--scratch")` | 6d45dbd7bcf7a3aa | 1 | 106 | 1 | `python-url-refused exit=1 want=2` | not run | **killed** |
| M6 | census allowlist check | `if script not in PY_SCRIPT_CENSUS and …: return False` deleted | 71fa15d7141ed6f1 | 1 | 106 | 1 | `python-unknown-head-refused exit=1 want=2` | `measurements=25 failures=3` exit 1 | **killed (both)** |
| M7 | per-script deny → global deny (round-70 regression) | `denied = PY_DENIED_ANY + PY_DENIED_BY_SCRIPT.get(...)` → `+ ("--root","--json") + …` | 835192fd5fb76d87 | 1 | 106 | 1 | `python-per-script-root-admitted exit=2 want=0` | not run | **killed** |
| M8a | `citation-ground-check.py --json` | `("--json",)` → `()` | 017b7be9392a8feb | 0 | 106 | **0** | — | `25 failures=0` exit 0 | **SURVIVED** |
| M8b | `gate-quote-audit.py --json` | `("--json",)` → `()` | b3ff98d2cf508fa4 | 0 | 106 | **0** | — | `25 failures=0` exit 0 | **SURVIVED** |
| M8c | `mirror-containment-check.py --json` | `("--json",)` → `()` | 1573796ba23fdb87 | 0 | 106 | **0** | — | `25 failures=0` exit 0 | **SURVIVED** |
| M8d | `resolve-dispatch-check.py --json` | `("--json",)` → `()` | 0dde68d01adb7fe1 | 0 | 106 | **0** | — | `25 failures=0` exit 0 | **SURVIVED** |
| M8e | `limb-mutation-check.py --root` | `("--root",)` → `()` | 6e7d1d55d7d54626 | 0 | 106 | **0** | — | `25 failures=0` exit 0 | **SURVIVED** |
| M8f | `r46-c1-gate.py --root` | `("--root",)` → `()` | e00f9720256638a4 | 0 | 106 | **0** | — | `25 failures=0` exit 0 | **SURVIVED** |
| M8g | `capture-source.py --work` | `("--url","--work","--scratch")` → `("--url","--scratch")` | e387f4f1a33a6f28 | 0 | 106 | **0** | — | `25 failures=0` exit 0 | **SURVIVED** |
| M8h | `capture-source.py --scratch` | `("--url","--work","--scratch")` → `("--url","--work")` | 411780ca9c88afa6 | 0 | 106 | **0** | — | `25 failures=0` exit 0 | **SURVIVED** |

`MUTANTS killed=7/15 survivors=M8a,M8b,M8c,M8d,M8e,M8f,M8g,M8h`

Every killed mutant is killed by exactly one case (`failures=1`, 106 cases still run) — the one-limb
isolation property holds for M1–M7. The kill shape is uniform and non-accidental: an admitted derive
that itself exits 2 is reported by the gate as a stale figure, so the case sees `exit=1 want=2` with
`reasons=derive-exit-2`, never a bare rc coincidence.

## 3. Survivor admission — measured, not inferred

Each survivor's rule was probed against a fixture root `F` that mirrors the selftest tmp
(`F/corpus/instruments` exists, the named script does not), ledger `_one`-shaped, run as
`cd F && python3 <gate> --ledger <ledger> --root .`, printing `rc` and the count of
`derive-not-read-only` lines. Nothing was executed that could write or fetch: the head's file is absent,
so python3 fails before the instrument runs.

```
$ for n in M8a..M8h: run pristine gate, then mutant gate
M8a-pristine rc=2 refused=1     M8a-mutant rc=1 refused=0
M8b-pristine rc=2 refused=1     M8b-mutant rc=1 refused=0
M8c-pristine rc=2 refused=1     M8c-mutant rc=1 refused=0
M8d-pristine rc=2 refused=1     M8d-mutant rc=1 refused=0
M8e-pristine rc=2 refused=1     M8e-mutant rc=1 refused=0
M8f-pristine rc=2 refused=1     M8f-mutant rc=1 refused=0
M8g-pristine rc=2 refused=1     M8g-mutant rc=1 refused=0
M8h-pristine rc=2 refused=1     M8h-mutant rc=1 refused=0
```

So the behaviour survives: every one of the eight rules is load-bearing in the pristine gate (refused,
rc=2) and is gone in its mutant (admitted, rc=1).

## 4. Frozen counter on the survivors — the round's own probe set does not kill any of them

```
$ python3 -B .ufo/waves/round-71/controls/c1-probe-run-r71.py --mode candidate \
    --gate $S/mutants/<id>/corpus/instruments/figure-audit.py --work $S/work/<id>/counter
M8a VERIFY measurements=25 failures=0 gate_sha256=017b7be9392a8feb6c558d9e4e16e2aefa68b2e99004f87668e27b19a35f28f6 mode=candidate  exit=0
M8b VERIFY measurements=25 failures=0 gate_sha256=b3ff98d2cf508fa4fc3bf8561546f22e01f93a25bcb320c51d759cd0fc317143 mode=candidate  exit=0
M8c VERIFY measurements=25 failures=0 gate_sha256=1573796ba23fdb87e5da7f42e3753ef7e1ddccb139d4b7524c67543094c64249 mode=candidate  exit=0
M8d VERIFY measurements=25 failures=0 gate_sha256=0dde68d01adb7fe11438b239e84d7e5bf0c7c19245507e2786c0b146f885add7 mode=candidate  exit=0
M8e VERIFY measurements=25 failures=0 gate_sha256=6e7d1d55d7d546267d17fd1c338347f25c0c2da374136b9bc709a32d0c8cf88f mode=candidate  exit=0
M8f VERIFY measurements=25 failures=0 gate_sha256=e00f9720256638a40d962eeb7191273061e7501e53132cb26f85cc17483dab9f mode=candidate  exit=0
M8g VERIFY measurements=25 failures=0 gate_sha256=e387f4f1a33a6f28a04e99491f74689f1b27362ee9f9ca1329dd6939af0aa138 mode=candidate  exit=0
M8h VERIFY measurements=25 failures=0 gate_sha256=411780ca9c88afa673697c07dbad95984f70bcee91e78a516bfa2e4dd8aee58d mode=candidate  exit=0
```

No FAIL MEASURE line in any of the eight receipts. The counter's N rows exercise head-level rules
(`frontier-recheck-count.py`, `capture-source.py`) and its R rows never pass `--json` to
`citation-ground-check.py`/`gate-quote-audit.py`/`mirror-containment-check.py`/`resolve-dispatch-check.py`,
never pass `--root` to `limb-mutation-check.py`/`r46-c1-gate.py`, and never pass `--work`/`--scratch`
to `capture-source.py`.

### Controls proving the 25/0 readings are not a broken-counter artifact

```
PRISTINE VERIFY measurements=25 failures=0 gate_sha256=182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603 mode=candidate exit=0
  HOST sort (GNU coreutils) 9.12; git version 2.56.0; Python 3.14.8
  MEASURE N8-python-no-option-head ok rc=2 refused=1 marker_runs=0 wrote=0
  MEASURE N12-python-unknown-head ok rc=2 refused=1 marker_runs=0 wrote=0
  MEASURE selftest ok selftest cases=106 failures=0 rc=0 min=104
  MEASURE mutbat ok rc=0 mutbat killed=5/5 survivors=0 invalid=0 controls=pass
  MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 rc=0
  MEASURE no-write-side-effect ok fixture_changed=0 marker_runs=0
M4 VERIFY measurements=25 failures=4 exit=1
  MEASURE N8-python-no-option-head FAIL rc=1 refused=0 marker_runs=1 wrote=0
  MEASURE selftest FAIL selftest cases=106 failures=1 rc=1 min=104
  MEASURE mutbat FAIL rc=1 mutbat killed=5/5 survivors=0 invalid=0 controls=fail
  MEASURE no-write-side-effect FAIL fixture_changed=0 marker_runs=1
M6 VERIFY measurements=25 failures=3 exit=1
  MEASURE N12-python-unknown-head FAIL rc=1 refused=0 marker_runs=0 wrote=0
  MEASURE selftest FAIL selftest cases=106 failures=1 rc=1 min=104
  MEASURE mutbat FAIL rc=1 mutbat killed=5/5 survivors=0 invalid=0 controls=fail
```

The pristine run reproduces the frozen candidate predicate on the frozen bytes. The counter detects the
head-level rules (M4: N8 admitted, `marker_runs=1`; M6: N12 admitted) and misses all eight per-script
entries. Note the `mutbat FAIL` in M4/M6 is a broken-base artifact — `figure-audit-mutbat.py`'s control
arm re-runs the base gate's selftest, which is already red — so it is not independent evidence.

## 5. Smallest selftest case that would kill each survivor

Every survivor falls to one `run_case(..., 2, _one(...))` line, using the same fixture the selftest
already builds (the named instrument is absent there, so an admitted head exits 2 at the python level and
the gate returns 1 — measured in §3, `rc=1 refused=0`). Rule and expected rc:

| survivor | case id | derive passed to `_one` | expected rc | mutant measured |
|---|---|---|---|---|
| M8a | `python-citation-ground-json-refused` | `python3 corpus/instruments/citation-ground-check.py --json j.json` | 2 | rc=1 refused=0 |
| M8b | `python-gate-quote-json-refused` | `python3 corpus/instruments/gate-quote-audit.py --json j.json` | 2 | rc=1 refused=0 |
| M8c | `python-mirror-containment-json-refused` | `python3 corpus/instruments/mirror-containment-check.py --json j.json` | 2 | rc=1 refused=0 |
| M8d | `python-resolve-dispatch-json-refused` | `python3 corpus/instruments/resolve-dispatch-check.py --json j.json` | 2 | rc=1 refused=0 |
| M8e | `python-limb-mutation-root-refused` | `python3 corpus/instruments/limb-mutation-check.py --root .` | 2 | rc=1 refused=0 |
| M8f | `python-r46-c1-gate-root-refused` | `python3 corpus/instruments/r46-c1-gate.py --root .` | 2 | rc=1 refused=0 |
| M8g | `python-capture-work-refused` | `python3 corpus/instruments/capture-source.py --work w` | 2 | rc=1 refused=0 |
| M8h | `python-capture-scratch-refused` | `python3 corpus/instruments/capture-source.py --scratch s` | 2 | rc=1 refused=0 |

Eight cases would take `EXPECTED_CASES` 106 → 114 and would close V71-1 at the selftest level. None was
added: this seat does not write the gate; the L1 applies them.

## 6. The two "equivalent" claims (V71-2, V71-3) — re-verified

Two extra one-limb mutants, built the same way, both `selftest cases=106 failures=0` exit 0:

| probe | mutation | selftest | direct probe |
|---|---|---|---|
| E1 (V71-2) | `PY_DENIED_ANY` → `("--output", "--selftest")` (the `--out` element removed) | exit 0, failures=0 | `capture-source.py --out out.txt`: pristine `rc=2 refused=1`; E1 `rc=2 refused=1` |
| E2 (V71-3) | `PY_DENIED_BY_SCRIPT["frontier-recheck-count.py"]` → `()` | exit 0, failures=0 | `frontier-recheck-count.py --json j.json`: pristine `rc=2 refused=1`; E2 `rc=2 refused=1`; E2 no-option head `rc=2 refused=1` |

- **V71-2 confirmed.** The `--out` element is redundant, not merely duplicated: with it gone, `--out`
  is still refused because `python_flags_ok` treats a token whose name is a prefix of a denied flag as
  that flag, and `--output` remains denied. The converse holds (M2): removing `--output` *admits*
  `--output`, so `--output` is the load-bearing element of the pair.
- **V71-3 confirmed.** The `frontier-recheck-count.py` per-script entry is inert config: `python_head_ok`
  returns False on `PY_HEAD_REFUSED` before the per-script deny list is consulted, so removing the entry
  changes neither the `--json` refusal nor the no-option refusal.

## 7. Findings for the L1

1. **V71-1 stands and is understated on the counter limb.** The attempt-1 lesson says eight per-script
   entries are unpinned, "two of them invisible to the frozen counter as well". Measured: 8/8 are
   unpinned by the selftest, and 8/8 also score `measurements=25 failures=0` exit 0 on the frozen
   counter. The `two` is an undercount; it is all eight.
2. **The census has one enforcement limb, not two.** `python-unknown-head-refused` is the only case that
   pins the allowlist's *enforcement*; `python-census-covers-instruments` pins the *table's completeness*
   against `os.listdir` and passes on M6, where enforcement is deleted (M6's single failure is
   `python-unknown-head-refused`). A reader of the R71 comment ("the census is pinned complete") could
   over-read that limb.
3. **Nothing here falsifies C1's frozen predicate.** The pristine control on the frozen bytes prints
   `VERIFY measurements=25 failures=0` exit 0; the eight survivors are a coverage finding (R103: every
   refusal rule carries a killing case), not a contract breach — the gate does refuse all eight shapes
   (§3) and the counter does have teeth on head-level rules (§4 controls). The contract is not narrowed
   on the strength of a survivor.
4. **C1's declared scope is unaffected by the survivors.** The survivors are all per-script deny entries
   whose shapes lie outside N1–N12/R1–R8; C1's kill_rule (which constrains those rows) is untouched.

## 8. Not done / residual

- Counter was run on the pristine gate and on the survivors plus M4/M6 only; M1, M2, M3, M5, M7 were not
  counter-run (they are already killed at the selftest). Their counter verdict is unmeasured here.
- Mutation of the "open classes" the claim names (positional arguments, options after `--`, writes on a
  positional path, nested python) was out of this seat's assignment and not attempted.
- The selftest harness compares `rc` only (plus an optional `reason=` substring). A mutant whose admitted
  derive also returns 2 *and* whose gate then returns 2 would be a false survivor; no such shape occurred
  in this set, and the observed kill signature for admitted derives is uniformly `rc=1` with
  `reasons=derive-exit-2`.
- Lane hygiene: the working tree carried 21 dirty entries when this seat began (LOG.md, SCORECARD.md,
  SKILL.md, corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md,
  corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md, corpus/lessons/round-71.md,
  corpus/source-snapshots/round-71/manifest.json, plus round-71 wave files); this seat wrote only this
  report file. No commit, push, tag, `git add/checkout/reset`, or `jj` command ran in the lane.
- Tooling: nothing installed or upgraded; the pacman guard was not invoked (no package needed). Host
  tools as resolved by the counter: sort 9.12, git 2.56.0, python3 3.14.8.

## 9. Reproduction

```
S=/fast/scratch/hyaku/kasegi-r71/MutateC1
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin clone --shared \
    /home/vgpnk/Projects/shokunin/kasegi-shokunin $S/clone
git -C $S/clone checkout 3cc8cd45cb6f8ca49a292f3b2647c5bddac71486
for n in <mutant ids>; do mkdir -p $S/mutants/$n/corpus; \
    cp -a $S/clone/corpus/instruments $S/mutants/$n/corpus/instruments; done
# apply one replacement per mutant (diffs in §2), then:
cd $S/mutants/$n && HYAKU_SCRATCH=$S/work/$n TMPDIR=$S/work/$n \
    python3 $S/mutants/$n/corpus/instruments/figure-audit.py --selftest
python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-71/controls/c1-probe-run-r71.py \
    --mode candidate --gate $S/mutants/$n/corpus/instruments/figure-audit.py --work $S/work/$n/counter
```
