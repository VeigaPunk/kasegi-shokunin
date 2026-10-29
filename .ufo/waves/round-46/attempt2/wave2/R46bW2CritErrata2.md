VERDICT: BROKEN

## Findings

1. **`counter-errata.md` does not provide an instrument-independent re-derivation for the extensions/amendments it records.** E1–E4 name the main battery, selftest, C2-gate, and F29-gate changes, but `## Plain re-derivations` (lines 79–86) only replays the pre-change C1/C2 readings and points to the claim's plain commands. In particular, the E2 selftest tallies are not independently substantiated by the listed count command, and the E3 `junk == 0` behavior has no plain junk-tree result there.
   - Artifact: `claims.json` C1 `plain[2]` and `counter-errata.md` E2 / `## Plain re-derivations`.
   - Search: pattern `def case_` in both `r46-counters-selftest-c1.py` and `r46-counters-selftest-c2.py`.
   - Output: `No matches found`.
   - The claimed `grep -c 'def case_' ...` therefore cannot establish the 76→83 / 137→147 totals; the source represents cases as `CASES = [...]` / `add(Case(...))`. Errata's “selftest tallies” reuse the changed selftests, not a plain derivation. Smallest correction: replace that count with a count derived from the actual case declarations, and add independent fixture/tree measurements for the changed E2/E3 predicates (or explicitly mark them as not independently re-derived).

2. **Unitemized instrument changes remain.**
   - Artifact: `corpus/instruments/r46-counters-selftest-c1.py` and `counter-errata.md` E2.
   - Command: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --unified=2 fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4..HEAD -- corpus/instruments/r46-counters-selftest-c1.py corpus/instruments/r46-counters-selftest-c2.py`.
   - Output includes `+    ap.add_argument("--only", help="run only the cases whose name contains this substring (the tip/control readings still run)")` and `+    cases = CASES if not a.only else [c for c in CASES if a.only in c[0]]`; searching `counter-errata.md` for `--only` returned `No matches found`. E2 records case additions but not this new test-selection interface. It is not used by the frozen battery command, but changes selftest behavior for explicit invocations; log it as a test-only helper and state that the default full suite remains the claim path.
   - The same freeze-to-HEAD instrument diff reports `M corpus/instruments/README.md` and `M corpus/instruments/knowledge-expected.txt`; searching the errata for either path returned `No matches found`. These are registry/input changes rather than gate-logic edits, but their disposition is absent from the errata. Smallest correction: explicitly classify them as documentation/input updates (or include their derivation in the errata).

3. **Frozen claims identity check passes.**
   - Artifact: `.ufo/waves/round-46/attempt2/claims.json`.
   - Command: `diff <(git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4:.ufo/waves/round-46/attempt2/claims.json) /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/claims.json`.
   - Output: no diff text; `claims_diff_exit=0`. The live file is byte-identical to the freeze.

## Limitations

- My attempted v1 battery replay with `--root <base> --pure <base>` returned `mutbat counter=c1 BASELINE-DIRTY baseline_failures=-1` and `mutbat counter=c2 BASELINE-DIRTY baseline_failures=-1`; this was not a faithful reproduction because the documented controls recipe uses a separate pure reference. A retry using that reference timed out at 3600 seconds, so I do not count the before receipt as independently replayed here.
- The freeze-v1 F29 gate did run against the base export: `f29-gate fixed=1/7 exit=1`; against the freeze tree: `f29-gate fixed=2/7 exit=1`. These reproduce the stated readings but use the gate itself, not an independent derivation of its amended behavior.
- No tools were installed. Seat scratch was removed.
