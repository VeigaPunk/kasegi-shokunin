# K72Mutate — mutation probe report (round 72, wave 1)

Seat: K72Mutate (leaf). Scratch: `/fast/scratch/hyaku/kasegi-r72/K72Mutate/` (deleted after run; all cited bytes reproduced below).
Lane clone: `git clone --shared` of the lane, `checkout a34ce4c` (`a34ce4c146b669ea8038da32ba47d7ca3b36ea43`).

## Bytes under test (measured)

- Candidate gate copied from the lane working tree: sha256 `4f59bda47eab2f93d54ccc7abe6256a878db5cbee98684d9d110043d91f9d221` — the frozen `b146c81a…` plus the one comment-line drift KasegiR72 announced; `diff` vs. the live file is empty (identical). Base gate at a34ce4c verified `182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603`.
- Counter `derive-head-census.py` sha256 `255fd4072dfe8e2a6bf53d5fcc0f92d2af486d40711d03c4573a4017ccd8db52` (matches freeze).
- Method note: `probes()` copies `figure-audit.py`, `gate-quote-audit.py`, `capture-binding-check.py`, `claim-package-check.py` from the gate's own directory, so every mutant is a full copy of `corpus/instruments/` (`$S/mut/<id>/`) with the mutated file inside; counter mutants keep the pristine candidate gate in the same dir.

## Baseline (pristine candidate gate + pristine counter)

```
$ (cd $S/lane && TMPDIR=$S python3 derive-head-census.py --gate <cand gate> --instruments <inst dir>)
CENSUS heads=45 write_class_pairs=5 READMITTED=0
ALIAS-PROBE verdict=refused rc=2 FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=probe
POSITIVE admitted=2/2
CENSUS-RESULT ok
EXIT=0
```

## Gate mutants (detector: `derive-head-census.py` exit / CENSUS-RESULT)

| Mutant | Change | Decisive output | Verdict |
|---|---|---|---|
| M1 | drop `"--work"` from `PY_DENIED_ANY` | `CENSUS heads=45 write_class_pairs=5 READMITTED=15` … `CENSUS-RESULT defect`, `EXIT=1` | KILLED |
| M2 | drop `"--scratch"` from `PY_DENIED_ANY` | `READMITTED=4` (capture-binding-check, citation-ground-check, frontier-recheck-count, kill-rule-check `--scratch` rows) … `CENSUS-RESULT defect`, `EXIT=1` | KILLED |
| M3 | `script = os.path.basename(parts[1])` (argv basename, not realpath) | `ALIAS-PROBE verdict=admitted rc=1` … `CENSUS-RESULT defect`, `EXIT=1` | KILLED |
| M4 | `python_flags_ok` returns `True` unconditionally | `ALIAS-PROBE verdict=admitted rc=1` … `CENSUS-RESULT defect`, `EXIT=1` | KILLED |
| M5 | remove `"derive-head-census.py": ()` from `PY_SCRIPT_CENSUS` | `READMITTED=0`, `ALIAS-PROBE verdict=refused`, `POSITIVE admitted=2/2`, `CENSUS-RESULT ok`, `EXIT=0` | **SURVIVED** |

M5 survivor analysis (measured, not inferred): `derive-head-census.py` contains zero `add_argument` calls (manual `sys.argv` loop), so `declared_options` yields no write-class flags for it — removing it from the census cannot produce READMITTED rows. No probe derive names `derive-head-census.py` either (probes run figure-audit.py, gate-quote-audit.py, capture-binding-check.py, claim-package-check.py). The detector is blind to census-membership of a flag-free head. This is a coverage finding, not a contract change.

## Counter mutants (detector: census exit / printed verdicts)

| Mutant | Change | Decisive output | Verdict |
|---|---|---|---|
| C1 | `load_tables` returns `([], {})` | `census: gate-quote-audit.py no longer denies --json; probe stale`, `EXIT=1` | KILLED (by the `probes()` staleness guard at line 117–118, before any row prints) |
| C1b | `load_tables` returns `([], found["PY_DENIED_BY_SCRIPT"])` | `READMITTED=21` … `CENSUS-RESULT defect`, `EXIT=1` | KILLED via the intended READMITTED limb |
| C2 | `ok = (not rows) and alias_verdict == "refused"` (POSITIVE dropped) | on good gate: `POSITIVE admitted=2/2`, `CENSUS-RESULT ok`, `EXIT=0` | **SURVIVED** on the good gate — see below |
| C3 | alias probe replaced by hardcoded `("refused", "mutated-unconditional")` | on good gate: `ALIAS-PROBE verdict=refused mutated-unconditional`, `POSITIVE admitted=2/2`, `CENSUS-RESULT ok`, `EXIT=0` | **SURVIVED** — see below |

C2 decisive measurement (blanket-refusal gate B, see step 4): pristine counter prints `POSITIVE admitted=0/2` → `CENSUS-RESULT defect`, `EXIT=1`; C2-mutated counter prints the same `POSITIVE admitted=0/2` line but then `CENSUS-RESULT ok`, `EXIT=0`. The mutant masks a gate that admits nothing — POSITIVE is still *printed* but no longer gates `ok`.

C3 decisive measurement (alias-admitting gate M3): C3-mutated counter prints `ALIAS-PROBE verdict=refused mutated-unconditional` and `CENSUS-RESULT ok`, `EXIT=0` — it masks the exact symlink-alias bypass the limb exists to catch. The item expected "must go red because POSITIVE is still checked"; measured otherwise: the two POSITIVE derives are independent of the alias verdict, so they still pass (2/2) and nothing else observes the forged alias result. The alias limb trusts `probes()`'s return value with no independent re-check.

## Step 4 — blanket-refusal gate

`python_head_ok` mutated to `return False` as its first statement (B). Pristine counter:

```
CENSUS heads=45 write_class_pairs=5 READMITTED=0
ALIAS-PROBE verdict=refused rc=2 FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=probe
POSITIVE admitted=0/2
CENSUS-RESULT defect
EXIT=1
```

Required behavior confirmed: exit 1 with `POSITIVE admitted=0/2`.

## Kill matrix (summary)

| Mutant | Target | Outcome | Decisive line |
|---|---|---|---|
| M1 | gate | KILLED | `READMITTED=15` / `CENSUS-RESULT defect` / exit 1 |
| M2 | gate | KILLED | `READMITTED=4` / `CENSUS-RESULT defect` / exit 1 |
| M3 | gate | KILLED | `ALIAS-PROBE verdict=admitted` / `CENSUS-RESULT defect` / exit 1 |
| M4 | gate | KILLED | `ALIAS-PROBE verdict=admitted` / `CENSUS-RESULT defect` / exit 1 |
| M5 | gate | **SURVIVED** | `CENSUS-RESULT ok` / exit 0 |
| C1 | counter | KILLED | `probe stale` SystemExit / exit 1 (guard, not READMITTED) |
| C1b | counter | KILLED | `READMITTED=21` / `CENSUS-RESULT defect` / exit 1 |
| C2 | counter | **SURVIVED** (good gate); masks blanket-refusal gate (exit 0, `ok`) | `CENSUS-RESULT ok` under B |
| C3 | counter | **SURVIVED** (good gate); masks alias-admitting gate M3 | `ALIAS-PROBE verdict=refused mutated-unconditional` / `CENSUS-RESULT ok` |
| B | gate (blanket refusal) | detected | `POSITIVE admitted=0/2` / `CENSUS-RESULT defect` / exit 1 |

## Survivors

1. **M5** — census-membership removal of `derive-head-census.py` is invisible: the head declares no write-class options and no probe derives through it.
2. **C2** — POSITIVE limb is advisory-only under mutation: printed but removable from `ok` without changing the good-gate verdict; only observable against a refusing gate.
3. **C3** — alias verdict is trusted verbatim from `probes()`; a counter that forges `refused` passes the good gate AND masks a real alias bypass (verified against M3).

No tools installed; no network fetches; no git mutations (clone + `checkout a34ce4c` in own scratch only). Scratch tree `/fast/scratch/hyaku/kasegi-r72/K72Mutate/` deleted on exit per seat rules.
