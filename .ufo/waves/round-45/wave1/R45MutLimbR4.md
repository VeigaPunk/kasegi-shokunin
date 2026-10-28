VERDICT: BROKEN

# R45MutLimbR4 — C1 mutation test of limb R4 (freeze-check selftest token + claims replay)

Attacked: `corpus/instruments/r45-routed-defects.py` `def limb_r4` (lines 210-222), run unmodified (counter NOT edited). Limb R4 accepts iff `freeze-check.py --selftest` exits 0 with `selftest cases=N failures=0`, N >= 6, AND `freeze-check.py --claims <root>/.ufo/waves/round-45/claims.json --tool-root <root> --base <base>` exits 0 and prints a line matching `^freeze-check claims=2 base_ok=2\b`.

## Survivors (counter did not reject; listed first)

Official baseline A = pristine export of `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd`. Satisfied tree = that export + `corpus/source-snapshots/round-45` + the two r45 counters + the frozen `claims.json` (bytes sha256 `bbe40503281c90eb9d70f469d7bac10125b285758ca9675be9894ce6c12c6206`, identical to freeze commit 8cf62c8) + a reference `freeze-check.py` draft (scratch only, sha256 `de8372ef16f87becf2febeee9bc74fe7709b579956fabe3d0b93d2585c595cb8`).

1. **Stub freeze-check (the requested stub) — real survivor.** Replacing `corpus/instruments/freeze-check.py` with exactly:
   ```
   #!/usr/bin/env python3
   # stub: prints the two tokens, reads nothing
   print('selftest cases=6 failures=0')
   print('freeze-check claims=2 base_ok=2')
   ```
   Command: `python3 <tree>/corpus/instruments/r45-routed-defects.py --root <tree> --baseline <base>`. Printed: `limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2`. Verdict `rejected=0` at A and at perturbed base B. Also `rejected=0` after deleting `.ufo/waves/round-45/claims.json` from the tree: printed `limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2`. The counter never checks that the claims file exists or that any claim was replayed.

2. **m1-selftest-case-vacuous — real survivor.** Exact edit in the draft's `c_exact_line_rejects_other_state` body: `    return replay_one(c, d, d) is False` → `    return True`. Printed: `mutant=m1-selftest-case-vacuous rejected=0`; detail `selftest rc=0 selftest cases=6 failures=0 | replay rc=0 freeze-check claims=2 base_ok=2`. A do-nothing selftest case passes unseen; only the B replay (which is not the official base) rejects it (`mutant=m1-selftest-case-vacuous base=B rejected=1 read=replay-rc=1`).

3. **m6-summary-literal-n — latent survivor (equivalent on A).** Exact edit: `    print(f"freeze-check claims={n} base_ok={ok}")` → `    print(f"freeze-check claims={n} base_ok={n}")`. At A the replay is truthful (2/2), so the edit is observationally identical: `mutant=m6-summary-literal-n rejected=0`. At B it is caught only through the exit code: `mutant=m6-summary-literal-n base=B rejected=1 read=replay-rc=1`.

4. **m7-exit-ignored — latent survivor (equivalent on A).** Exact edit: `    return 0 if ok == n else 1` → `    return 0`. A: `mutant=m7-exit-ignored rejected=0`. B: `mutant=m7-exit-ignored base=B rejected=1 read=replay-rc=0`. Caught at B only by the summary regex (`base_ok=1` ≠ `base_ok=2`), and the counter's label then reads `replay-rc=0` (see limitation L4).

## Killed mutants (counter rejects at A)

- m2-selftest-case-dropped: remove `@case` before `c_missing_field_raises` → `rejected=1 read=selftest-rc=0-tokens=(5, 0)`.
- m3-selftest-case-inverted: `return replay_one(c, d, d) is True` → `... is False` → `rejected=1 read=selftest-rc=1-tokens=(6, 1)`.
- m4-selftest-token-trailing: token gains ` (all green)` → `rejected=1 read=selftest-rc=0-tokens=None` (the `\s*$` anchor works).
- m5-replay-result-discarded: `        ok += good` → `        ok += 1` → `rejected=1 read=selftest-rc=1-tokens=(6, 1)`. Killed by the selftest case `c_replay_counts_only_matches`, not by the claims replay.
- m8-prefix-predicate: exact-line match → `want.split()[0] in ln` → `rejected=1 read=selftest-rc=1-tokens=(6, 2)`. Killed by the selftest's exact-line cases, not by the replay.

## Controls

- `ctl-honest-satisfied` (reference draft, unmodified): `rejected=0 read=selftest-cases=6 replay=base_ok=2` — the satisfied state is accepted, so the mutant rejections are not an artifact of a broken draft.
- `ctl-do-nothing-absent` (no freeze-check.py): `rejected=1 read=freeze-check-absent`.
- Same honest draft at perturbed base B: `rejected=1 read=replay-rc=1`.
- Fact at freeze: `ls corpus/instruments/freeze-check.py` → `ls: cannot access 'corpus/instruments/freeze-check.py': No such file or directory`; `git ls-files corpus/instruments/freeze-check.py | wc -l` → `0`; `git log --all --oneline -- corpus/instruments/freeze-check.py | wc -l` → `0`. R4 is therefore unsatisfiable until the builder draft lands. The round-45 spec (`wave1-spec.json`, C1/R4 builder A/B) asks for that file; no committed version exists.

## Mutation run (verbatim from `recipe.py`, scratch, deleted on exit)

```
mutant=m1-selftest-case-vacuous rejected=0
    A(frozen base) R4 read=selftest-cases=6 replay=base_ok=2
    freeze-check: selftest rc=0 selftest cases=6 failures=0 | replay rc=0 freeze-check claims=2 base_ok=2
mutant=m2-selftest-case-dropped rejected=1
    A(frozen base) R4 read=selftest-rc=0-tokens=(5, 0)
mutant=m3-selftest-case-inverted rejected=1
    A(frozen base) R4 read=selftest-rc=1-tokens=(6, 1)
mutant=m4-selftest-token-trailing rejected=1
    A(frozen base) R4 read=selftest-rc=0-tokens=None
mutant=m5-replay-result-discarded rejected=1
    A(frozen base) R4 read=selftest-rc=1-tokens=(6, 1)
mutant=m6-summary-literal-n rejected=0
    A(frozen base) R4 read=selftest-cases=6 replay=base_ok=2
mutant=m7-exit-ignored rejected=0
    A(frozen base) R4 read=selftest-cases=6 replay=base_ok=2
mutant=m8-prefix-predicate rejected=1
    A(frozen base) R4 read=selftest-rc=1-tokens=(6, 2)
mutant=ctl-honest-satisfied rejected=0
    A(frozen base) R4 read=selftest-cases=6 replay=base_ok=2
mutant=ctl-do-nothing-absent rejected=1
    A(frozen base) R4 read=freeze-check-absent
mutant=stub-two-tokens rejected=0
    A(frozen base) R4 read=selftest-cases=6 replay=base_ok=2
--- perturbed base B (frozen base + refiled receipt pair) ---
mutant=m1-selftest-case-vacuous base=B rejected=1 read=replay-rc=1
mutant=m2-selftest-case-dropped base=B rejected=1 read=selftest-rc=0-tokens=(5, 0)
mutant=m3-selftest-case-inverted base=B rejected=1 read=selftest-rc=1-tokens=(6, 1)
mutant=m4-selftest-token-trailing base=B rejected=1 read=selftest-rc=0-tokens=None
mutant=m5-replay-result-discarded base=B rejected=1 read=selftest-rc=1-tokens=(6, 1)
mutant=m6-summary-literal-n base=B rejected=1 read=replay-rc=1
mutant=m7-exit-ignored base=B rejected=1 read=replay-rc=0
mutant=m8-prefix-predicate base=B rejected=1 read=selftest-rc=1-tokens=(6, 2)
mutant=ctl-honest-satisfied base=B rejected=1 read=replay-rc=1
mutant=ctl-do-nothing-absent base=B rejected=1 read=freeze-check-absent
mutant=stub-two-tokens base=B rejected=0 read=selftest-cases=6 replay=base_ok=2
--- survivors at official base A (rejected=0) ---
SURVIVOR m1-selftest-case-vacuous read=selftest-cases=6 replay=base_ok=2
SURVIVOR m6-summary-literal-n read=selftest-cases=6 replay=base_ok=2
SURVIVOR m7-exit-ignored read=selftest-cases=6 replay=base_ok=2
SURVIVOR ctl-honest-satisfied read=selftest-cases=6 replay=base_ok=2   (control: expected to be accepted)
SURVIVOR stub-two-tokens read=selftest-cases=6 replay=base_ok=2
```
Base-only probes (run directly): `python3 freeze-check.py --selftest` on the stub → `selftest cases=6 failures=0` rc 0; `--claims /nonexistent --tool-root /nonexistent --base /nonexistent` on the stub → `freeze-check claims=2 base_ok=2`, rc 0. The honest draft with claims deleted → counter `limb R4 fixed=0 read=replay-rc=1` (rejected only because the draft itself raises FileNotFoundError).

## Limitations and notes

- L1 The mutants are single edits to my reference draft, not to the lane's real freeze-check (which does not exist yet). The draft follows the counter's contract and the R4 limb, not the full builder spec: it does not model `expect_after` rejection, the whole-line spec wording beyond exact-line match, or `--work`. Dropping an `expect_after` check is equivalent on A and B (expect_before fails at B too) and would need a fully GREEN perturbed base to detect; not run.
- L2 Only one perturbed base was tried (B = frozen base + round-44 refiled receipt pair, making R5 fixed and C1 read `fixed=1`). Latent survivors m6/m7 are caught at B only; other perturbations were not tested.
- L3 Recursion hazard [INFERENCE from source, not run]: a freeze-check that replays C1 against the satisfied tree would re-enter R4 of the nested counter and recurse without bound. The honest draft avoids it only because its replay uses the base tree, which lacks freeze-check.py. Any mutant pointing the C1 replay at the tool root was therefore not run.
- L4 Counter diagnostic defect (not counted, observed): when the summary token mismatches while the exit code is 0 (m7 at B), R4 prints `read=replay-rc=0`. The label reports a return code that was 0 and does not name the token mismatch. The same label prints `replay-rc=1` for a missing claims file in the honest draft.
- L5 The counter was not edited. The tree is minimal: R1, R2, R3 and R5 are unsatisfied, and only the R4 line is read.

## Suggested repairs (drafts for the L1 to decide; counter unchanged)

- Negative control for the freeze-check itself: R4 should also require that the freeze-check rejects a bundled known-bad claims fixture (a do-nothing counter whose output lacks expect_before). A stub or a vacuous case then fails at the limb, not only at a perturbed base.
- Require the replay summary to be derived from the per-claim lines (or to be re-computed by the counter from the claims file), so a literal `base_ok=N` cannot pass.
- Fix the R4 diagnostic label so a token mismatch reports `replay-token-mismatch` instead of `replay-rc=<rc>`.
- Do not count the stub as a freeze-check: it has no selftest logic and reads no claims.

Scratch: `/fast/scratch/hyaku/kasegi-r45/R45MutLimbR4` (removed on exit). No commit, push, index or git mutation; read-only `git archive`/`git show`/`git diff --stat`/`git log`/`git ls-files` only. No tools installed.
