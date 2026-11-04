# ExecSignalGate — round 65 findings (predata build-and-falsify)

Seat: ExecSignalGate, executor, leaf. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`. Production files not edited. No commit, push, or mutating git.

## C1 — signal fail-closed gate (candidate built, falsified)

Candidate: `.ufo/waves/round-65/w1/ExecSignalGate/figure-audit.py` (anchor tag `1FA7`). Details, old→new anchors, controls, and limits: `.ufo/waves/round-65/w1/ExecSignalGate/NOTES.md`.

Behavior implemented:
- Non-final stage killed by a signal other than SIGPIPE → stale, `derive-upstream-signal-<N>`.
- Final stage killed by any signal → stale, `derive-signal-<N>` (replaces malformed `derive-exit--<N>`).
- Non-final SIGPIPE (-13) → benign, documented in the module docstring (a later stage closed the pipe early; the final stage's output is the value). Pinned by `upstream-sigpipe-nonfinal-benign`.
- Unchanged: grep exit1 no-match stays benign; positive upstream statuses keep `derive-upstream-exit-N`; final nonzero keeps precedence.
- Docstring sentence "negative signal statuses remain ignored" replaced with the implemented rule (module docstring exit-code paragraph and `upstream_stale` docstring updated).

Selftest counts:
- Before: `cases=59 failures=0` (production baseline, exit 0).
- After (candidate): `cases=63 failures=0`, exit 0 (59 kept + 4 new). One existing case, `upstream-python-signal-ignored`, flipped expectation from exit 0 to exit 1 with reason `derive-upstream-signal-15` because its old expectation was the defect; it was not removed. Its id still says "ignored"; flagged for L1.
- New cases: `upstream-middle-sigterm-stale`, `upstream-python-sigkill-stale`, `final-stage-signal-stale`, `upstream-sigpipe-nonfinal-benign`.

Ledger: `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0` (exact line).

Discrimination controls (old production gate vs candidate, same fixtures): SIGKILL producer old `ok` exit 0 (defect) vs new `derive-upstream-signal-9 stale`; final SIGTERM old `derive-exit--15` vs new `derive-signal-15`; SIGPIPE unchanged benign under both. Receipt `control-old-vs-new.txt`.

Production check: `git -C <lane> status --porcelain corpus/instruments/figure-audit.py` → empty.

## C2 — F44 source screen (S098, FIRST PSIRT Services Framework v1.1)

Screen only; no admission is claimed. The source was opened by URL (reader text). The PDF is linked but not opened. No S098 row exists in SOURCES.md and no capture or manifest exists, so `source-recheck` cannot run this wave.

- F06/S018 overlap: Service 5.2 and 5.2.2 Multi-Vendor Coordination (multi-party role model). Excluded from F44.
- F43 overlap: Sub-function 4.2.2.3 "Validate Remedy with Finders" and 5.2.1.3 "Validation by Finder" (finder confirms fix). Excluded from F44.
- Candidate distinct ground: Service 3.2 / Function 3.2.2 Accelerated Handling for Established Finders — "consider skipping the qualification/vetting process all together and moving straight to remediation" when the finder is well known and the organization judges most of their reports will be fixed. This is PSIRT-internal triage routing, not role attribution or multi-party coordination.
- Falsifiable rule and rejected over-generalization are in NOTES.md.

L1 must decide admission: it needs a held capture, manifest, and SOURCES row for S098, and a frozen claim.

## Blockers / questions for L1 (to agent://KasegiR65)

- The flipped case keeps the id `upstream-python-signal-ignored`; L1 may rename it at integration, which is a production-side choice.
- No S098 capture exists yet; F44 admission is blocked on capture and manifest.

## Checks the main agent should run (not run by this seat)

- `python3 -B corpus/instruments/figure-audit.py --selftest` after integrating the candidate into production (expect `cases=63 failures=0`).
- `python3 -B corpus/instruments/figure-audit.py --ledger corpus/instruments/figure-audit-ledger.json --root .` (expect 35/35).

## Commands actually run by this seat

- `python3 -B corpus/instruments/figure-audit.py --selftest` on production (`HYAKU_SCRATCH` scratch) → exit 0, `cases=59 failures=0`.
- `python3 -B <candidate> --selftest` → exit 0, `cases=63 failures=0`, 0 verdict=fail.
- `python3 -B <candidate> --ledger ... --root <lane>` → exit 0, `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`.
- Old-vs-new controls (fixture ledgers in scratch).
- `git -C <lane> status --porcelain corpus/instruments/figure-audit.py` → empty.
- `cp`/`printf`/heredoc only in scratch and the seat directory; no production write.

Tools installed: none. Subagents dispatched: none. Scratch `/fast/scratch/hyaku/kasegi-r65/ExecSignalGate` removed after copying receipts.
