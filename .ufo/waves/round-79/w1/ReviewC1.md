# ReviewC1 — round-79 C1 surgical correctness review (depth:verifiability)

Seat: ReviewC1 (leaf reviewer). Read-only review of the frozen C1 candidate; all runs under
`TMPDIR=/fast/scratch/hyaku/kasegi-r79/ReviewC1` (scratch deleted before yield). No lane/fleet
writes except this report. No tools installed; no pacman/sysctl/git mutations (read-only
`git show`/`git ls-tree` only). No `lsp` device is mounted in this seat's tool inventory, so
caller/definition checks were done by byte-exact diff plus direct execution — every verdict
below is grounded in an executed run, not text matching alone.

## Provenance checks (all pass)

- Candidate wave-dir bytes `sha256=eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f`
  == freeze-commit `9d0b1eb0` blob == claim P2. `mutbat.py` `735d2336…` and `mutant-table.json`
  `0cb50dc8…` also identical between wave dir and freeze commit.
- Base instrument at freeze `corpus/instruments/recheck-cwd-census.py` sha `e666ae11…` == claim's
  `target_instrument` base sha.
- All 19 table anchors occur **exactly once** in the candidate (independent `str.count` audit;
  battery `notderived=0` agrees).

## BLOCKER 1 — frozen predicate P3 fails on the frozen bytes (killed=18, dirty=1, rc=1)

Frozen counting command over exact scratch copies of the frozen triple:

```
MUTANT K-T1 verdict=EXCEPTION-KILL rc=1 fails=1 counted=no
MUTBAT target_sha256=eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f \
       baseline=ok rows=19 killed=18 survived=0 dirty=1 notderived=0     exit 1
```

P3 demands `rows=19 killed=19 survived=0 dirty=0 notderived=0` and exit 0; the frozen kill rule
counts "EXCEPTION-KILL on an assertion-class row" as NOT VERIFIED. Reproduced three times
(battery run, `--keep` output, solo re-run) — deterministic, not environmental.

Root cause chain, all inside frozen bytes:

1. Row **K-T1** (`tmpdir_refused()` → `return False`) has `"class": "assertion"`.
2. Neutered, `main()` proceeds; `run_foreign()`'s `tempfile.mkdtemp(dir=bogus)` raises
   `FileNotFoundError`; the **r79-added case-13 guard** (`except Exception as exc13:` — absent in
   the r78 candidate, confirmed in the r78→r79 diff) converts it to `ret13=-99` and sets
   `out13="exception=%r" % (exc13,)`.
3. The FAIL detail is `"ret=%d stdout=%r stderr=%r"` → the FAIL line contains
   `stdout="exception=FileNotFoundError(2, 'No such file or directory')"` — observed verbatim.
4. mutbat `EXC_RE = ^selftest case=\S+ FAIL .*exception` matches → verdict `EXCEPTION-KILL`;
   counted only for `class == "exception"` → `counted=no` → `dirty=1`, `rc=1`.

So the K-T1 transform **does** die with a FAIL line and no traceback (its `expect` text
"tmpdir-refusal FAIL (exception caught as ret=-99)" matches observed behavior exactly), but the
counter's verdict semantics + the row's `class` field make it uncountable. Note the r78 shape
(no guard) would traceback → `DIRTY`, also uncounted; under the frozen triple the only ways to
reach killed=19 are class `exception` on K-T1, or a verdict-semantics change, or a guard marker
that does not embed `exception` — all freeze-time decisions, and the table is declared frozen
against edits. Claim `measured_after_target` ("MUTBAT killed=19/19 rc0") is **not reproducible**
against the frozen candidate+counter+table on this host. As frozen, C1 cannot be verified by its
own kill rule.

## Frozen-table verification (passes, independent of the blocker)

Battery verdicts and per-row observed FAIL cases (from `--keep` outputs) vs `expect` text —
every row's expect matches observed behavior:

| row | verdict | counted | fail_cases | expect match |
|---|---|---|---|---|
| K-M1 | KILLED | yes | gate-regs, gate-consume, gate-negpolarity | gate-regs FAIL ✓ (superset) |
| K-M2 | KILLED | yes | gate-negpolarity | exact ✓ |
| K-M3 | EXCEPTION-KILL | yes (class exception) | gate-consume (`exception=NameError("name 'out6' is not defined")`), gate-negpolarity | exact ✓ |
| K-M4 | KILLED | yes | gate-predicates, gate-negpolarity | exact ✓ |
| K-M5 | KILLED | yes | gate-checkids (missing=both-headers) | exact ✓ |
| K-X1 | KILLED | yes | gate-consume (`clean_ok=True limb_log=[]`) | exact ✓ |
| K-X2a | KILLED | yes | gate-predicates | exact ✓ |
| K-X2b | KILLED | yes | gate-wiring (`F1+F2+F3` on gate-consume:486), gate-checkids | exact ✓ |
| K-M8 | KILLED | yes | gate-wiring (`F1:relabel-detection:408`), gate-checkids | exact ✓ |
| K-W1 | KILLED | yes | gate-predicates | exact ✓ |
| K-W2 | KILLED | yes | gate-checkids (side_logs) | exact ✓ |
| K-N1 | KILLED | yes | gate-predicates | exact ✓ |
| K-P1 | KILLED | yes | gate-checkids (`side_logs=[[True],[True],[False]]`) | exact ✓ |
| K-P2 | KILLED | yes | gate-wiring, gate-checkids | gate-wiring FAIL ✓ |
| K-G1 | KILLED | yes | gate-predicates | exact ✓ |
| K-C1 | KILLED | yes | gate-wiring, gate-checkids | gate-wiring FAIL ✓ |
| K-NP | KILLED | yes | gate-wiring, gate-checkids | gate-wiring FAIL ✓ |
| K-CL | KILLED | yes | gate-predicates | exact ✓ |
| K-T1 | EXCEPTION-KILL | **no** | tmpdir-refusal | expect matches behavior; counter classification broken (Blocker 1) |

No traceback in any kept output (`dirty` row is EXCEPTION-KILL, not Traceback).

## Other frozen-predicate components on candidate bytes

- **P1** ✓ `selftest cases=15 failures=0`, rc=0.
- **P4** ✓ `TMPDIR=/nonexistent-kasegi-r79-ReviewC1` → rc=2, stderr
  `recheck-cwd: TMPDIR … is not a directory`, stdout empty, no `Traceback`.
- **P7** ✓ with one measurement hazard (R5): exactly one `subprocess.run(`, exactly one
  `"bash", "-c"`, no `os.system(`/`eval(`/`exec(`; the only `/tmp` occurrence is docstring prose
  (candidate line 25: "no path is hard-coded under /tmp."), not a path literal; both `mkdtemp`
  calls take their parent from `TMPDIR`/env.
- **census() unchanged vs base** ✓: the base→candidate diff touches only the module docstring,
  `import ast`, the new gate/wiring functions, the selftest body, and `main`'s r78-carried
  `tmpdir_refused()` gate. `first_recheck`, `has_restoration_recheck`, `run_foreign`, `census`
  appear in neither the base→r79 nor the r78→r79 diff. r78→r79 delta is exactly what the claim
  states: gate verdicts → module-level predicates + gate-wiring AST limb + the case-13 guard.
- **Gate-predicates row table**: every predicate body-neutering dies — K-X2a
  (`gate_consume_ok`), K-M4 (`gate_negpolarity_ok`), K-G1 (`gate_checkids_ok`), K-N1
  (`wiring_ok`), K-W1 (`wiring_findings`), K-CL (`_calls`), K-P1 (`predicates_ok`, via the third
  side log) all counted KILLED; the two-polarity rows make inversion/blanket-True visible.
  Deleting the `GATE_PREDICATES["gate-wiring"]` entry also dies (probe PB8) because the frozen
  `bad_src` expected findings hardcode `F3:gate-wiring`.
- **Gate-checkids side logs** ✓: `[False]` and `[]` both fail the gate → check deletion (K-M5),
  crash-before-log, and `consumed()` neutering (PB10) are caught. Label-evasion on a gate check
  is caught (non-Constant label → never `wired` → F3); moving a gate check into an in-file
  helper is NOT an evasion (`ast.walk` is structural, sees nested defs); constant-`False` ok on
  a gate check self-kills at runtime.

## Routed findings (outside the frozen 19-row table; none changes a verdict)

- **R1 (sharpest): gate checks accept constant-arg predicate calls.** `_calls()` verifies only
  the callee name. Probe **PB2**: `check("gate-negpolarity", gate_negpolarity_ok(False), …)` →
  SURVIVED; probe **PB3**: `check("gate-consume", gate_consume_ok(True, limb_log), …)` →
  SURVIVED. A neutered-to-constant-True gate verdict that no gate observes — the nearest
  neighbor of the r78 K-X2 survivor class, and the round-79 motivation ("makes such neutering
  observable") does not hold for this transform. Routed per the kill rule (composites/new
  transforms); recommend the L1 route it to the next candidate round (e.g. F2 also rejecting
  predicate calls whose args reference none of the live variables).
- **R2: non-gate checks have no structural net.** F1 covers only Constant-True and
  BoolOp-with-True-operand; F2/F3 apply only to `GATE_PREDICATES` names. Probe **PB1**
  (`restoration-only` ok → `not False`) → SURVIVED; probe **PB6** (`gate-regs` ok → `not False`)
  → SURVIVED. `gate-regs` is an R127 gate yet absent from `GATE_PREDICATES`, so even a gate-family
  check can be silently blinded (composed with K-M1 it defeats the registration gate — composite,
  routed). `1`, ternaries, or aliased non-gate calls fall in the same class.
- **R3: harness neutering is a universal evader.** Probe **PB4** (`if not ok:` → `if False:` in
  `check()`) → SURVIVED: the wiring gate scans check() call sites, not the check/failures
  machinery. Standard mutation scope excludes the harness; recorded because the round's selling
  point is structural observability.
- **R4: gate-predicates rows list and side-log tripwire have no completeness net.** Probe **PB9**
  (delete row `(predicates_ok([]), False),`) → SURVIVED; probe **PB7** (third side log
  `[predicates_ok([(True,False)]) is False]` → `[True]`) → SURVIVED. K-P1's ONLY kill thread is
  that unnamed inline tripwire (PB7 composed with K-P1 would let the frozen K-P1 transform
  survive). No gate scans the rows list or the tripwire expression.
- **R5 (measurement hazard, not behavior): P7 '/tmp' grep.** `grep -c '/tmp'` on the candidate
  returns 1 (docstring prose, line 25). A landing-day P7 check that greps for `/tmp` unscoped
  will misfire; scope it to tempfile call args or exclude the docstring.

## Probe log (10/10 run under TMPDIR=$S; target sha prefix eda49d32)

| probe | transform | verdict | fail_cases |
|---|---|---|---|
| PB1 | restoration-only ok → `not False` | SURVIVED | — |
| PB2 | gate-negpolarity ok → `gate_negpolarity_ok(False)` | SURVIVED | — |
| PB3 | gate-consume ok → `gate_consume_ok(True, limb_log)` | SURVIVED | — |
| PB4 | `if not ok:` → `if False:` (harness) | SURVIVED | — |
| PB5 | `done.append(case)` → `pass` | KILLED | gate-checkids |
| PB6 | gate-regs ok → `not False` | SURVIVED | — |
| PB7 | third side log → `[True]` | SURVIVED | — |
| PB8 | delete `"gate-wiring": "wiring_ok",` map entry | KILLED | gate-predicates (frozen bad_src row) |
| PB9 | delete `(predicates_ok([]), False),` row | SURVIVED | — |
| PB10 | `consumed()` → `return True` | KILLED | gate-consume, gate-negpolarity, gate-checkids |

## Residual risk / verification gaps

- P5/P6 (landing-tree census run, pin rows) and all C2 predicates are landing-commit claims, not
  reviewable from candidate bytes — out of this seat's scope; not run (also avoids executing the
  lane's recheck suite, which this seat must not trigger).
- mutbat's own toy selftest was not re-run (committed control `c1-mutbat-selftest-r79.txt`
  covers it; not a named command for this seat).
- All runs on one host/CPython 3; the K-T1 classification depends only on the guard's
  `exception=%r` marker reaching the FAIL detail, which is version-stable.
- Bottom line: **1 blocker** (P3 false: killed=18/dirty=1/rc=1 from the frozen triple — C1 NOT
  VERIFIED by its own kill rule as frozen), **5 routed** findings, table/expect audit and all
  other C1 components clean.
