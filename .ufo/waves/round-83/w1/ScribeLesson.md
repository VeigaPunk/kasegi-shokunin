# ScribeLesson — round 83 (kasegi), attempt 1

**Behavior.** Drafted the round-83 lesson body for the L1 at `.ufo/waves/round-83/w1/lesson-round-83.md` (219 lines): `## Gate` with the C1 successor half (frozen-byte table, 67-row composition, G1–G4 rows, counter limbs, four control blocks, forgeries F6–F11) and the C2 half for S117 (access record, six located quotes with `len(q.split())` counts, registry change, a REJECT row with a flip condition, unpinned list, B8 control); `## Mistakes` M83-1 and M83-2; `## Routed-defect disposition` for the r82 spot-check defects 1–7; `## Landing values`; `## Cite-check receipts`. No lane file was edited, no `corpus/` file written, no git/jj write anywhere, no counter or lane gate suite run.

**Commands run** (read-only, over frozen bytes or the worktree; all outputs in the receipts):

- `sha256sum` over 12 frozen paths + `git show 0cd499db:<path> | sha256sum` equality — 12/12 `EQUAL` (claims, candidate, counter, table, builder, forgery driver, stub builder, entry gate, C2 control driver, S117, manifest, base instrument).
- `git show`/`git ls-tree`/`git diff` for the S117 registry cells (`queued`/`—` at freeze → `mined`/entry path at the instant), the one-row diff shape, registry 117 both sides, knowledge 96 → 97.
- `python3` over `manifest.json` (each quote on its anchor line, word counts 11/6/19/12/17/12 = 77), over `mutant-table.json` (67 = 63 assertion + 3 neutral + 1 exception; id set = r82 + G1–G4; no r81 id missing), over `claims.json`.
- 25 `grep -n -F` cite checks (R131), each printing the line holding the token.
- Frozen candidate: `--selftest` → `selftest cases=27 failures=0` rc 0; `--root <lane> --lane <lane>` → `entries=97 … conformant` rc 0.
- Frozen r83 entry gate (`42f4b2ac…`) over four inputs: frozen F57 (A: `untied=1` fail rc 1), F57 with Claim 2's rule rewritten (B: `untied=0` pass rc 0), the F59 draft at sha `c3499b12…` (C: `ruleless=0 untied=0` pass rc 0), the F59 draft with a vacuous Claim 1 rule (D: pass rc 0).

**Gates.** Every control quoted in the lesson is the committed freeze-commit file and was not re-run; the only instrument runs are the four entry-gate runs above and the two candidate runs, all in scratch with `TMPDIR` set. No C1 predicate and no C2 predicate was graded — the lesson states that.

**Findings.**

- **M83-1** `claim-prose-names-one-residual-class` — the r82 claim's "F8 is the declared limit" was not the only residual (the path-label forgery F9 scored `rc=0` under the r82 counter). Captured-by: none (R128 binds mutants, R119 a Gate reject, R133 placeholders). Fix shown able to fail and pass by the frozen r83 control: F9/F10/F11 `rc=0` under `counter=r82`, `rc=1` under `counter=r83`, candidate still `rc=0`.
- **M83-2** `gate-tie-limb-measures-stems` — class decided on executed evidence: the G6 limb measures vocabulary, not entailment. False positive on the admitted F57 entry (`untied=1`, its Claim 2 rule names none of its quote's operative terms: the rule line matches `target|operator|home|database|import` 0 times); false negative on a vacuous echo (run D passes). Fix demonstrated for the false-positive face only (run B, one-line rule amendment); the false-negative face is routed to round 84 and does not touch B8, whose three forgeries are all rejected.
- **REJECT row** — the r82 lead "Managing the Perishability of OSV Records" (`S116.txt:27`) is not admitted: no URL in the capture, no public copy found, lane note at `corpus/SOURCES.md:284`; flip condition stated. `ScoutPerish.md` was absent at my measurement instant, so the row says "search receipt in `ScoutPerish.md`" — the L1 must confirm or replace it.
- **Provenance risk** — the F59 gate run and every entry line cite are bound to draft sha `c3499b12…`; `ReviewC2.md` files Medium 1–2 and Low 1–3 against that draft, so applying any of them voids run C and the cites, and the L1 must re-run and re-cite after the entry settles.

**Out of scope / not done.** No verdict lines (the L1 owns them); no landing values measured (listed by name in `## Landing values`); no `mutbat` battery, no `source-recheck.py`, no `sources-census.sh`, no `capture-binding-check.py` run (quoted from the frozen controls); no decision on registering the unclaimed `ExecStatedOutput-candidate-stated-output-check.py`; no corpus, SKILL.md, PROVINCE.md, SCORECARD.md or LOG.md edit.

**Touched surfaces.** Only `.ufo/waves/round-83/w1/lesson-round-83.md`, this report, and `.ufo/waves/round-83/w1/ScribeLesson-receipts/`.

**Artifact paths.**

- `.ufo/waves/round-83/w1/lesson-round-83.md`
- `.ufo/waves/round-83/w1/ScribeLesson.md`
- `.ufo/waves/round-83/w1/ScribeLesson-receipts/cite-checks.txt`
- `.ufo/waves/round-83/w1/ScribeLesson-receipts/c1-candidate-measured.txt`
- `.ufo/waves/round-83/w1/ScribeLesson-receipts/m83-2-gate-runs.txt`

**Tooling.** None installed or upgraded; no pacman transaction.

**Limits.** Measurements are at `2026-11-06T22:06:42Z` on a mid-landing worktree (instrument and both pin rows still base, `cases=24`); the lesson marks every landing-only value by name. The scratch copies used in runs B and D lived under `/fast/scratch/hyaku/kasegi-r83/ScribeLesson/` and were deleted at exit; the receipts record the exact rewrites.
