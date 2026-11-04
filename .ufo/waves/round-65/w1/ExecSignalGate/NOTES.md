# ExecSignalGate — round 65 candidate notes

Candidate: `.ufo/waves/round-65/w1/ExecSignalGate/figure-audit.py` (copy of `corpus/instruments/figure-audit.py` at base master `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`; production file untouched, `git status --porcelain corpus/instruments/figure-audit.py` empty).

Line numbers: production (prod) → candidate (cand). Candidate anchor tag after edit: `1FA7`.

## Anchor changes (`line: old -> new`)

- prod 38-39 / cand 38-39 (Exit codes paragraph): `(fail-closed: nonzero final status, upstream positive status other than grep exit1,` / `or empty stdout is stale);` -> `(fail-closed: nonzero or signal final status, upstream positive status other than grep exit1,` / `or upstream signal other than SIGPIPE, or empty stdout is stale);`
- prod 41-44 / cand 41-47 (module docstring rule sentence): `...(derive-exit-N); otherwise ... (derive-upstream-exit-N). Grep exit1 is an ordinary no-match and is not an error; negative signal statuses remain ignored. This is not` -> final stage signal N as `derive-signal-N`; upstream stage killed by signal N as `derive-upstream-signal-N`; SIGPIPE (-13) on a non-final stage documented as benign ("a later stage closed the pipe early, so the truncated producer output is not the value; the final stage's output is"). The phrase "negative signal statuses remain ignored" is removed.
- prod (none) / cand 58: `import shlex` (cand 57) -> new line `import signal` inserted between `import shlex` and `import subprocess`.
- prod 72 / cand 76: `EXPECTED_CASES = 59` -> `EXPECTED_CASES = 63` (59 + 4 new cases).
- prod 79-86 / cand 83-94 (`upstream_stale`): docstring `Stale upstream statuses: any >1, or exit1 from a program other than grep.` / `Grep exit1 is an ordinary no-match; negative (signal) statuses stay ignored.` -> docstring names the signal rule and SIGPIPE; body gains `if status < 0: return status != -signal.SIGPIPE` before the unchanged `>1` and `exit1 non-grep` checks.
- prod 116-122 / cand 124-134 (`run_derive` status classification):
  - final: `return None, out, "derive-exit-%d" % status` -> `if status < 0: return None, out, "derive-signal-%d" % -status` then the unchanged `derive-exit-%d` return (final nonzero keeps precedence and the `derive-exit--N` form is gone).
  - upstream: `return None, out, "derive-upstream-exit-%d" % p.returncode` -> `if p.returncode < 0: return ... "derive-upstream-signal-%d" % -p.returncode` then the unchanged `derive-upstream-exit-%d` return.
- prod (none) / cand 379-382 (selftest fixtures): inserted after the `kill.py` fixture write (prod 365-366):
  - `kill9.py`: writes `35` to stdout, flushes, then `os.kill(os.getpid(), signal.SIGKILL)`.
  - `pipe.py`: sets `SIGPIPE` to `SIG_DFL`, writes 4096 lines of 1024 bytes (4 MiB) to stdout. `SIG_DFL` is needed because Python ignores SIGPIPE by default and would instead exit 1 with BrokenPipeError (which the gate correctly treats as stale).
- prod 449 / cand 466-467 (existing case, expectation flipped, NOT removed): `run_case("upstream-python-signal-ignored", 0, ...)` -> `run_case("upstream-python-signal-ignored", 1, ..., reason="derive-upstream-signal-15")` with a comment. Id kept for lineage; its old `exit 0` expectation was the defect this round fixes. The id still contains the word "ignored", which is now misleading; flagged for L1.
- prod (none) / cand 469-475: four new cases, in this order:
  - cand 469-470 `upstream-middle-sigterm-stale`: `cat g.txt | python3 corpus/instruments/kill.py | wc -l`, want exit 1, reason `derive-upstream-signal-15`.
  - cand 471-472 `upstream-python-sigkill-stale`: `python3 corpus/instruments/kill9.py | wc -l`, want exit 1, reason `derive-upstream-signal-9` (writer printed `35` before SIGKILL, so stale despite output).
  - cand 473-474 `final-stage-signal-stale`: `python3 corpus/instruments/kill.py`, want exit 1, reason `derive-signal-15`.
  - cand 475 `upstream-sigpipe-nonfinal-benign`: `python3 corpus/instruments/pipe.py | head -n 1 | wc -l`, want exit 0, want value `1`.
- Unchanged: `upstream-grep-count-nomatch-ignored`, `successful-pipeline-counts-one`, `final-exit7-precedes-upstream-exit1`, every other case and checker code.

## Counts

- Selftest case count before: `case=59` (production baseline, `HYAKU_SCRATCH` set, exit 0, `selftest cases=59 failures=0`).
- After: `cases=63 failures=0` (59 kept + 4 new; one of the 59 flipped in expectation).

## Discrimination controls (old gate vs candidate, same fixtures)

Run with `/fast/scratch/hyaku/kasegi-r65/ExecSignalGate/control-old-vs-new/`; receipt `control-old-vs-new.txt`.

- SIGKILL producer: old `FIG s-sigkill ... derived=1 ok` exit 0 (defect); new `reason=derive-upstream-signal-9 stale` exit 1.
- Final-stage SIGTERM: old `reason=derive-exit--15 stale` (malformed label); new `reason=derive-signal-15 stale`.
- SIGPIPE non-final: old `derived=1 ok` exit 0; new `derived=1 ok` exit 0 (unchanged positive control).

## Known limits (not hidden)

- SIGPIPE benign is a documented rule and applies only to a producer that dies by signal. A producer that catches the broken pipe and exits 1 is still stale (`derive-upstream-exit-1`), fail-closed.
- The SIGPIPE fixture relies on Linux pipe capacity (64 KiB) being far smaller than 4 MiB, so the producer is still writing after `head -n 1` exits. This is deterministic on the lane's Linux host.

## F44 source screen (S098, FIRST PSIRT Services Framework v1.1) — screen only, not admitted

Source opened 2026-11-04 by URL (reader text; the document's own PDF is linked, not opened). Reader-text line numbers below are into the reader artifact, not into a held capture. S098 is not yet a `SOURCES.md` row and no `corpus/source-snapshots/` capture exists, so no `source-recheck` is possible in this wave.

Overlap map:
- F06 / S018 (multi-party coordination): PSIRT Service 5.2.2 "Multi-Vendor Coordination" (reader lines ~1752-1768: "Where appropriate, a vendor PSIRT should make arrangements for sharing vulnerability information with coordinators or other vendors.") and Service 5.2 coordination overlap the F06 role model. Exclude from F44.
- F43 (CERT/CC phase-to-role matrix): Sub-function 4.2.2.3 "Validate Remedy with Finders" (reader line ~1418: "Partner with third-party finder or stakeholder to validate the remedy.") and 5.2.1.3 "Validation by Finder" overlap F43's Reporter fix confirmation. Exclude from F44.
- Candidate distinct ground (PSIRT-internal triage routing, not role attribution and not multi-party coordination): Service 3.2 "Established Finders", Function 3.2.2 "Accelerated Handling for Established Finders" (reader line ~1162): "When the finder is well known to you and you have determined that the majority of the issues they report will be fixed, consider skipping the qualification/vetting process all together and moving straight to remediation."

Falsifiable local rule for F44 (candidate): an accelerated-handling claim must name both conditions (a well-known finder AND the organization's own judgment that most of that finder's reports will be fixed); the source says "consider", not "must". Rejected over-generalization: "a PSIRT skips triage for trusted finders" as a universal rule.

Admission is NOT granted by this wave: claims are predata, F44 needs a held capture, manifest, and source row, and L1 owns admission.

## Verification commands actually run

- `python3 -B .../figure-audit.py --selftest` (candidate), `HYAKU_SCRATCH=/fast/scratch/hyaku/kasegi-r65/ExecSignalGate` → exit 0, `selftest cases=63 failures=0`, 0 `verdict=fail` lines. Receipt `selftest-candidate.txt`.
- `python3 -B .../figure-audit.py --ledger corpus/instruments/figure-audit-ledger.json --root <lane>` (candidate) → exit 0, `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`. Receipt `ledger-candidate.txt`.
- Production selftest baseline before edits: exit 0, `selftest cases=59 failures=0`. Receipt `selftest-production-baseline.txt`.
- `git -C <lane> status --porcelain corpus/instruments/figure-audit.py` → empty.
- Old-vs-new controls listed above.

No tools installed. No subagent dispatched.
