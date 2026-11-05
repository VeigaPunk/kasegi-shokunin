# K73MutateCounter — mutate-run-revert probe of `recheck-cwd-census.py`

Seat: K73MutateCounter (leaf mutation-tester, no subagents). Item attacked: C1 counter
`corpus/instruments/recheck-cwd-census.py` (QUALITY Q10 recheck-cwd census), at lane HEAD
3b53ff83 (base fdf17413). No lane file was edited; no git mutation was run.

## 1. Baseline and provenance

- Scratch: `/fast/scratch/hyaku/kasegi-r73/K73MutateCounter` (kept for re-run; receipts copied below).
- `sha256sum orig.py` before all runs = `854456db322db2ee7263a0339a2b841515d36ae165c146eaa2708dfc59d3538e`;
  after all runs = the same. Equal to `git show 3b53ff83:corpus/instruments/recheck-cwd-census.py | sha256sum`
  and to the lane working-tree file, so the mutants come from the frozen counter.
- Base export: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive fdf17413 corpus/knowledge | tar -x -C $S/base`
  (exit 0; 88 files).
- Original selftest: `TMPDIR=$S python3 $S/orig.py --selftest` → last line `selftest cases=1 failures=0`, exit 0.
- Original census: `TMPDIR=$S python3 $S/orig.py --root $S/base --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin`
  → `RECHECK-CWD entries=88 noprefix=11 exit2_foreign=10 exit0_foreign=56 exit1_foreign=22 exit_other=0 norecheck=0`,
  then `RECHECK-CWD-RESULT nonconformant`, exit 1. Matches the frozen base values.
- Tooling: read `/home/vgpnk/.omp/agent/RULES.md`. Installed or updated nothing. Host Python 3.14.8 was used as found.
- Lane writes by this seat: none. The census runs execute the prefixed `cd <lane> && ...` rechecks inside the
  lane by design of the counter; I did not capture a full `git status` before the runs (see §6).

## 2. Mutants (each a copy of orig.py with exactly one change; `diff -u` verified)

Receipt: `K73MutateCounter-diffs.txt`.

| ID | Single change (orig line → mutant line) |
|----|------------------------------------------|
| M1 | L77 `noprefix = not value.startswith(prefix)` → `noprefix = False` |
| M2 | L54 `return proc.returncode` → `return 0 if proc.returncode == 2 else proc.returncode` |
| M3 | L51 `cwd=scratch` → `cwd=DEFAULT_LANE` (run_foreign has no `--root` in scope; the lane root is the only directory the counter names) |
| M4 | L157 `% ("conformant" if conform else "nonconformant")` → `% "conformant"` (exit code unchanged) |
| M5 | L46 `mkdtemp(prefix="recheck-cwd-", dir=env_tmp)` → `dir="/tmp"` |
| M6 | L58 `shutil.rmtree(scratch, ignore_errors=True)` (in run_foreign's finally) → `pass` |
| M7 | `first_recheck` returns the LAST `recheck:` line instead of the first (see §5 on "first AND last") |
| M8 | L66 `prefix = "cd %s && " % lane` → `% root` |

## 3. Kill matrix (commands, exit codes)

Runner: `K73MutateCounter-run.sh` (receipt `K73MutateCounter-matrix.txt`). Per mutant:
(a) `TMPDIR=$S python3 <m> --selftest`; (b) `TMPDIR=$S python3 <m> --root $S/base --lane <lane>`.
Leftover = `recheck-cwd-*` dirs left in $S (cumulative across the run order; see notes).

| Mutant | Diff summary | (a) selftest rc / last line | (b) RECHECK-CWD line; census rc; RESULT line | Verdict (kill rule as written) | orig.py sha256 before → after |
|---|---|---|---|---|---|
| orig | — | 0 / `selftest cases=1 failures=0` | `entries=88 noprefix=11 exit2_foreign=10 exit0_foreign=56 exit1_foreign=22 exit_other=0 norecheck=0`; 1; nonconformant | baseline | 854456db…538e → 854456db…538e |
| M1 | noprefix never true | 1 / `selftest cases=1 failures=1` | `entries=88 noprefix=0 exit2_foreign=10 …`; 1; nonconformant | **KILLED** (a, b) | same |
| M2 | exit 2 reported as 0 | 1 / `selftest cases=1 failures=1` | `entries=88 noprefix=11 exit2_foreign=0 exit0_foreign=66 …`; 1; nonconformant | **KILLED** (a, b) | same |
| M3 | foreign run in lane root | 0 / `selftest cases=1 failures=0` | `entries=88 noprefix=11 exit2_foreign=0 exit0_foreign=66 …`; 1; nonconformant | **KILLED** (b only) | same |
| M4 | RESULT prints conformant unconditionally | 0 / `selftest cases=1 failures=0` | identical to orig RECHECK-CWD line; 1; **`RECHECK-CWD-RESULT conformant`** | **SURVIVED** on the RECHECK-CWD line and exit code (the kill rule's two checked items). The printed RESULT line contradicts exit 1. Caught by fixture F-result (§4). | same |
| M5 | scratch parent hard-coded `/tmp` | 0 / `selftest cases=1 failures=0` | identical to orig; 1; nonconformant | **SURVIVED** (literal). Caught by F-foreign (§4). | same |
| M6 | scratch not removed | 0 / `selftest cases=1 failures=0` | identical to orig; 1; nonconformant | **SURVIVED** (literal). Leaks 3 dirs after selftest; census added 88 (cumulative 91, orig 0). Caught by F-leak (§4). | same |
| M7 | first_recheck returns last line | 0 / `selftest cases=1 failures=0` | identical to orig; 1; nonconformant | **SURVIVED** (literal). Base has exactly one `recheck:` line per entry (88 of 88), so first = last on the base. Caught by F-first (§4). | same |
| M8 | prefix built from `--root` | 0 / `selftest cases=1 failures=0` (root = lane inside selftest) | `entries=88 noprefix=88 exit2_foreign=10 …`; 1; nonconformant | **KILLED** (b only) | same |

Exit codes were recorded for every run: selftest rc 0 for orig/M3/M4/M5/M6/M7/M8 and 1 for M1/M2;
census rc 1 for all nine rows (the base is nonconformant in every case, so the exit code alone does
not discriminate, which is why the printed line is part of the verdict).

Re-run checks (same commands, clean scratch): M7 census `rc=1 leftover=0`, line identical to orig;
M8 census `rc=1 leftover=0 noprefix=88`; orig census `rc=1 leftover=0`. The leftover column in the matrix
is cumulative from the M6 run and is therefore not attributed to M7 or M8.

Literal-rule result: 4 killed (M1, M2, M3, M8), 4 survived (M4, M5, M6, M7). §4 gives a fixture for each survivor.

## 4. Survivors and proposed fixtures

Fixture driver: `K73MutateCounter-fixtures.py` (receipt `K73MutateCounter-fixtures.txt`). It loads a counter by
path and runs five fixtures. Command: `TMPDIR=<empty dir> python3 fixtures.py <counter>`.
Run for orig and each mutant from an empty TMPDIR:

- orig: driver rc 0, `failures=0`. All five fixtures PASS.
- M1: rc 2 (F-foreign and F-result FAIL). M2: rc 0 (no fixture here; M2 is killed by (a) and (b)).
- M3: rc 1 (F-foreign FAIL: `exit0_foreign=0 exit_other=1`). M4: rc 1 (F-result FAIL: RESULT says conformant, rc_bad=1).
- M5: rc 1 (F-foreign FAIL: `exit_other=1`). M6: rc 1 (F-leak FAIL: `leftover=1`).
- M7: rc 1 (F-first FAIL: `exit2_foreign=1 noprefix=1`). M8: rc 1 (F-lane FAIL: `noprefix=1`).

Driver note: two of my first-pass fixture versions were wrong. F-lane pointed `cd` at a nonexistent
directory, so orig failed it. The leak check also read leftovers from the previous mutant's run. Both were
fixed (a fresh fixture lane directory, and an empty TMPDIR per run) and the driver was rerun. Only the rerun
is reported above.

Survivor fixtures. Each is one entry in the knowledge tree. "Expected" is the orig counts.

1. **M5 (and M3 at selftest level): F-foreign.** Entry `a.md`, prefix-less on purpose, value:
   `recheck: case "$(pwd -P)" in "<realpath(gettempdir())>"/recheck-cwd-*) exit 0;; *) exit 3;; esac`
   Expected: `entries=1 noprefix=1 exit0_foreign=1 exit_other=0`. Fails M5 (`exit_other=1`) and M3 (`exit_other=1`).
   Belongs in the selftest: **yes**. It asserts the scratch is a fresh dir under TMPDIR, which the selftest
   does not check today. Use `os.path.realpath(tempfile.gettempdir())`.

2. **M6: F-leak.** After a census run over a tree, assert `glob(os.path.join(TMPDIR, "recheck-cwd-*")) == []`.
   Use a dedicated subdirectory of the selftest's scratch as TMPDIR for that run. Expected leftover 0.
   Fails M6 (leftover=1 after a one-entry census). Belongs in the selftest: **yes**.

3. **M7: F-first.** Entry `b.md` with two lines:
   `recheck: cd <fixture-root> && true` then `recheck: python3 corpus/instruments/absent.py`.
   Expected: `entries=1 noprefix=0 exit2_foreign=0 exit0_foreign=1`. Fails M7 (`noprefix=1 exit2_foreign=1`).
   Belongs in the selftest: **yes**. It pins the docstring rule "reads the FIRST recheck: line".
   The base corpus cannot distinguish first from last, so only a fixture can.

4. **M4: F-result.** Call `main(["x","--root",bad,"--lane",bad])` on a tree with `recheck: true`
   (prefix-less, so nonconformant) with stdout captured. Expected: return 1 and last line
   `RECHECK-CWD-RESULT nonconformant`. The conformant tree (prefixed `true`) must return 0 with
   `RECHECK-CWD-RESULT conformant`. Fails M4 (prints conformant for the nonconformant tree).
   Belongs in the selftest: **yes**. The selftest never calls `main()`, so the printed verdict is unchecked.

Selftest-level gap for M8 (killed in §3 by (b) but not by (a)): F-lane.
Entry `c.md` with `recheck: cd <other-existing-dir> && true`, run with `--lane <other>` on a root that differs
from it. Expected `noprefix=0 exit0_foreign=1`. Fails M8 (`noprefix=1`). Belongs in the selftest: **yes**.
The current selftest sets root = lane, so it cannot separate `--root` from `--lane`.

Constraint on folding these into the selftest (from the frozen claim, not reworded): C1's predicate
requires the selftest to print exactly `selftest cases=1 failures=0`. The fixtures must be folded into the
single existing fixture case (extend the tree and the `want` dict) and must not add a second case.
Folding into the existing tree was not run; only the separate-tree forms above were executed.

## 5. Notes on the mutant set

- "First AND last" (M7 wording). I implemented the last-line variant only. The base has one `recheck:` line per
  entry (88 entries, 88 with exactly one), so both readings give the same base census. F-first kills the
  last-line variant. Under the AND reading, the same fixture fails too (the second line is the exit-2 line),
  which I did not run as a separate mutant.
- M3 used `cwd=DEFAULT_LANE` because `run_foreign` does not receive `--root`. A cwd of `--root` would need an
  extra parameter, which is a second change.
- M6 leaves recheck scratch dirs behind. Those leftovers are real, but the census lines and exit codes do not
  change, so the literal kill rule cannot see this mutant. F-leak can.

## 6. Limits and observations

- The base census has 77 prefixed values that execute `cd <lane> && ...` inside the lane. Only the 11
  prefix-less values run from a foreign cwd in the intended sense. The `exit2_foreign` counts for prefixed
  lines therefore test the `cd`, not the foreign cwd.
- The census selftest checks counts only. It never checks the RESULT line or exit code of `main()` (M4).
- Lane status: I compared `git status --porcelain | head -n 5` before and after the runs (the same 5 lines).
  The full count was not captured before the runs. It is 7 now: `.ufo/waves/round-73/w1-dispatch.err`,
  `w1-dispatch.json`, `w1-spec.json`, `w1.ready`, `w1.ready.dispatched`, `w1/`, `corpus/source-snapshots/round-73/`.
  None of these came from this seat's runs, which wrote only to scratch.
- I did not run a conformant candidate tree. The C1 predicate (after-state) is outside this probe.

## 7. Receipts (under this wave dir)

- `K73MutateCounter-matrix.txt`: runner output, one row per run (selftest rc, census line, census rc, leftovers)
- `K73MutateCounter-run.sh`: the runner
- `K73MutateCounter-diffs.txt`: `diff -u orig.py mut-<id>.py` for M1–M8
- `K73MutateCounter-fixtures.py`: survivor fixture driver
- `K73MutateCounter-fixtures.txt`: driver output for orig and M1–M8

Scratch kept at `/fast/scratch/hyaku/kasegi-r73/K73MutateCounter` (mutants `mut-M1.py`…`mut-M8.py`, `orig.py`, `base/`).
