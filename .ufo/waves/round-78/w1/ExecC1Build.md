# ExecC1Build — round-78 attempt 1, C1 recheck-cwd successor

Seat: ExecC1Build (executor, leaf). Scope: C1 only (TMPDIR refusal + named-kill set). C2 not in this seat.
No commit, no lane-tree edit, no git writes, no sysctl/pacman/tool installs, no labrat probe spawned.

## Result

- Candidate: `successor/recheck-cwd-census.py`
  sha256 `f68499715f38b6e74f368c441766954a240d7f5036d68157110e5017c8457db1`
- Selftest on candidate: `selftest cases=13 failures=0`, rc 0.
- TMPDIR refusal: `TMPDIR=/nonexistent-kasegi-r78` → rc 2, stderr `recheck-cwd: TMPDIR /nonexistent-kasegi-r78 is not a directory`, stdout empty, no Traceback.
- Real-tree census (rc 0): `RECHECK-CWD entries=91 noprefix=0 exit2_foreign=0 exit0_foreign=69 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0`, `RECHECK-CWD-RESULT conformant`. Matches the expected figures.
- Named-kill set: **7 of 8 killed by FAIL assertion. K-X2 survives (rc 0). It is an equivalent mutant under the frozen transform; see "K-X2" below. This is a routed defect in claim C1 as written, not a candidate defect I can close.**

## Kill table (mutants derived from the candidate, run as `TMPDIR=$S/t python3 -B <mutant> --selftest`)

| id | rc | FAIL lines | Traceback |
|---|---|---|---|
| K-M1 | 1 | `gate-regs FAIL registered=[]`; `gate-consume FAIL no-registration`; `gate-negpolarity FAIL no-registration`; `failures=3` | no |
| K-M2 | 1 | `gate-negpolarity FAIL neg_ok=True`; `gate-consume` ok (`clean_ok=True limb_log=[True]`); `failures=1` | no |
| K-M3 | 1 | `gate-consume FAIL exception=NameError("name 'out6' is not defined")`; `gate-negpolarity FAIL not-evaluated-after-exception`; `failures=2` | no |
| K-M4 | 1 | `gate-negpolarity FAIL neg_ok=False`; `failures=1` | no |
| K-M5 | 1 | `gate-checkids FAIL missing=['both-headers'] extra=[] relabel_log=[True]`; `cases=12 failures=1` | no |
| K-X1 | 1 | `gate-consume FAIL clean_ok=True limb_log=[]`; `failures=1` | no |
| K-X2 | **0** | none; `selftest cases=13 failures=0` | no |
| K-M8 | 1 | `gate-checkids FAIL missing=[] extra=[] relabel_log=[]`; `failures=1` | no |

Outputs: `successor/mutants/<id>.py` (mutant), `successor/mutants/<id>.out` (run output), `successor/mutants/<id>.diff` (mutant vs candidate, one hunk each).

## K-X2 (survives): why it cannot be killed under the frozen transform

Transform: replace the condition `clean_ok is True` in `check("gate-consume", ...)` with `True`.
On the real tree `clean_ok` is `True` (the registered limb returns a bool True on the case-6 output, asserted by the same check). The mutated condition therefore evaluates to the same value as the original, and the subexpression has no side effect. Replacing a subexpression with its own real value cannot change any check outcome, the printed `ok`/`FAIL` tokens, the detail text, or the exit code. The mutant is provably equivalent on any candidate that passes its own selftest with the anchored text. Verified: K-X2 output is identical in verdict lines to the candidate (`gate-consume ok clean_ok=True limb_log=[True]`).
Only a non-equivalent design can kill it, which requires changing the anchored text (not a candidate change). Routed to the L1/Reviewer as a claim defect in C1 (the "selftest exits 1" requirement for K-X2 is unsatisfiable as written).

The same argument applies in principle to K-X1 and K-M8 as originally frozen (value-preserving replacement). Both are killed here only because the candidate adds a consumption ledger whose record is a side effect inside the replaced text (see below).

## Candidate design (diff vs base and vs r77 reference)

- Base (`0687cca8…`, `corpus/instruments/recheck-cwd-census.py`, sha `e666ae11…`): `first_recheck`, `has_restoration_recheck`, `run_foreign`, `census`, `main` are byte-identical to the base (`candidate-vs-base.diff` hunks are only the module docstring, the new `tmpdir_refused` helper, the selftest body, and the main guard). The r77 reference already equalled base outside selftest and docstring; the candidate equals the r77 reference outside: docstring, guard, helper, selftest.
- Diffs saved: `successor/candidate-vs-base.diff` (6 hunks), `successor/candidate-vs-r77-reference.diff` (7 hunks).
- (a) TMPDIR guard: `tmpdir_refused()` prints `recheck-cwd: TMPDIR <value> is not a directory` to stderr and returns True when `TMPDIR` is set and `os.path.isdir` is False. Called first in `main()` (exit 2 before the selftest/census dispatch) and first in `selftest()` (exit 2 before any mkdtemp).
- (a') Case 13 `tmpdir-refusal`: sets `TMPDIR` to a nonexistent path inside the selftest scratch, calls `main()` with stderr captured, requires rc 2, empty stdout and the message; restores `TMPDIR` (pop if originally unset) in `finally`.
- (b) Consumption ledgers (needed to make K-X1 and K-M8 non-equivalent):
  - `limb_log`: the gate calls the registered limb through a wrapper `consumed(limb_log, regs[...](out, ret))`; `gate-consume` requires `clean_ok is True and limb_log == [True]`. Removing the consumer `clean_ok = limb(out6, ret6)` now fails `gate-consume`.
  - `relabel_log`: the relabel-detection expression is wrapped in `consumed(relabel_log, ...)`; `gate-checkids` requires `relabel_log == [True]`. Replacing the expression removes the record and fails `gate-checkids`.
  - The registration closure (`regs["restoration-only-result"]`) is unchanged, so K-M1/K-M2 anchors are verbatim.
- Selftest REQUIRED_CHECKS gains `tmpdir-refusal`; cases=13.
- Transform anchors (`c1-mutant-transforms.md`) were all present in the candidate verbatim except K-M8, whose `<expr>` is now `consumed(relabel_log, …)` (derived on that text, so it still applies). K-X1 anchor `clean_ok = limb(out6, ret6)` preserved verbatim.

## Judgment calls (for L1 review)

- `TMPDIR=""` (set but empty) is refused as "not an existing directory", literal reading of the spec. `tempfile` treats empty as unset, so this is stricter than tempfile. Not exercised in the real run (TMPDIR unset in this shell).
- The gate-checkids and gate-consume detail strings gained `relabel_log=` / `limb_log=` fields.

## Outputs written (all under `.ufo/waves/round-78/w1/`)

- `successor/recheck-cwd-census.py` (candidate)
- `successor/mutants/K-M1.py K-M2.py K-M3.py K-M4.py K-M5.py K-X1.py K-X2.py K-M8.py` (+ `.out`, `.diff`)
- `successor/selftest.out` (candidate selftest, rc 0)
- `successor/tmpdir-refusal.out`, `successor/tmpdir-refusal.err` (rc 2)
- `successor/census-real.out`, `successor/census-real.err` (rc 0), `successor/census-real-verbose.out`
- `successor/candidate-vs-base.diff`, `successor/candidate-vs-r77-reference.diff`
- `ExecC1Build.md` (this file)

## Not derived / not verified

- K-X2: not killable under the frozen anchored transform (proof above). Counts as NOT VERIFIED per the claims kill rule.
- Not run: the lane's full gate suite (out of scope by instruction). Not run: C2 items (other seats).
- Tools installed: none. Scratch `/fast/scratch/hyaku/kasegi-r78/ExecC1Build/` removed before yield.
