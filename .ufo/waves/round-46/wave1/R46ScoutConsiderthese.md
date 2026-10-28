VERDICT: INFO

# R46ScoutConsiderthese — considerthese proposal status and proposal 3 adoption

Read-only scout. No commits, no git/jj mutation, no edits to tracked files. Scratch under `$HYAKU_SCRATCH/kasegi-r46/R46ScoutConsiderthese/` was removed on exit. Frozen base `914ca0b6956f01d87b2e252ffad06fe74ec5d9ba`.

## 1. Proposal status (considerthese/2026-10-26.md, seven proposals)

Source: `considerthese/2026-10-26.md` lines under "Self-improvement suggestions" (1–7); ledger `corpus/knowledge/considerthese-proposals-ledger.md`.

| # | proposal | status now (my reading) | evidence |
|---|---|---|---|
| 1 | distance-to-next-score explicit | landed (r31 measurement, r39 criteria) | `SCORECARD.md` at base: `git show 914ca0b:SCORECARD.md \| grep -cE 'Distance-to-next-score\|Threshold for 8'` → `1`. Run on base export: `python3 corpus/instruments/score-gap.py --root <base-export>` → `gap: 24 of 64 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`. Ledger "round-42" row says 61 rechecks at a different base; base figure is 64. |
| 2 | run one end-to-end domain task round | **ledger row is STALE**: the claim-checker remainder landed in round 43 | `git show 914ca0b:corpus/instruments/claim-package-check.py \| head -12` prints the header "The claim-package gate: eight rules ... Round 43 of kasegi-shokunin". `git log --oneline -1 -- corpus/instruments/claim-package-check.py` → `5b4a850 round-43 C2: claim-package gate (8 rules) + selftest + exemplar + ...`. The ledger's round-42 section says the checker is absent, measured at `ab98fac9`, which predates `5b4a850`. Nothing in the ledger records the landing. Remaining open part: SHONEN box 2 still `[~]`; exemplar still PARKED per ledger (not re-verified here). Selftest of the checker NOT run by me. |
| 3 | quiescence gate before `complete` | **partly landed as counters; the pre-`complete` gate is NOT wired anywhere** (see §2) | see §2 |
| 4 | cap/externalise wave evidence | open, operator-owned (unchanged) | `git ls-tree -r --name-only 914ca0b \| wc -l` → `9155`; `... -- .ufo \| wc -l` → `8688`. Not a decision; no LFS/prune artefact. |
| 5 | land owed F18 PROVINCE amendment | landed r36 (unchanged) | ledger carries `PROVINCE.md:77`; not re-measured. |
| 6 | re-tune cadence/depth | open, operator-owned (unchanged) | `git ls-tree -r --name-only 914ca0b -- considerthese \| wc -l` → `8` (one per day, `2026-10-19` … `2026-10-26`). |
| 7 | proposal-status ledger | landed (r30; fills r37–r42); **round-43 to round-45 dispositions unfiled** | `grep -cE '^## Round-4[345] dispositions' corpus/knowledge/considerthese-proposals-ledger.md` → `0` (exit 1). Ledger base at 914ca0b is 146 lines. |

## 2. Proposal 3 (quiescence gate before `complete`): what exists

Commands run (absolute paths under the lane):

- `grep -rnc 'porcelain' SKILL.md PROVINCE.md corpus/QUALITY.md` → `SKILL.md:0`, `PROVINCE.md:0`, `corpus/QUALITY.md:3`.
- `grep -lr 'porcelain' corpus/instruments` → `citation-survival.md`, `r36-closure.sh`, `r37-closure.sh`, `r41-closure.sh`, `README.md`, `resolve.py` (the `resolve.py` and `citation-survival.md` hits are path-like rule noise: "git-porcelain snippets", not a gate).
- `git show 914ca0b:SKILL.md | grep -niE 'complete' | grep -iE 'gate|clean|quiet|status|before'` → no line gating a `complete` on tree cleanliness. Hits are unrelated (`coverage.status:"incomplete"`, the score-gap.py row).
- `git grep -lI 'status --porcelain' 914ca0b -- ':!.ufo'` → SCORECARD/LOG/QUALITY prose and the closure suites; no driver or script invoked at `complete`.

Placeholder half (`filled by the L1` / `<LANE_HASH>`):
- Implemented as a read-only counter in `corpus/instruments/r35-defect-closure.sh` D1 (`placeholders=[1-9]` open; line 164 `ph=$(grep -c -F -- 'filled by the L1' SCORECARD.md …)`).
- Do-nothing control: `bash corpus/instruments/r35-defect-closure.sh --root <base export>` printed `D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=4 open=0` and `closed=4/7 exit=1`. D1 is ALREADY green at base, so the placeholder half does not distinguish "adopted" from "not adopted" on this tree. It is discriminated only by the committed fixture `corpus/instruments/r35-fixtures/D1/SCORECARD.md` (reintroduced `filled by the L1` prose, line 22), which reads red.
- Plain run on lane tree: `closed=7/7 exit=0`.

Porcelain half (`git status --porcelain` empty before `complete`):
- Live only as post-hoc closure limbs: `r36-closure.sh` E9(b), `r37-closure.sh` E9(b) (fail-closed, `status-read=failed`), `r38` G4/G6, `r39` G2/G5/G6, `r42` J13. None is invoked by a `complete` step in the committed tree.
- Fixture behaviour, run by me in a scratch repo: clean tree → `clean-porcelain=[]`; after `echo dirty > b.txt` → `dirty-porcelain=[?? b.txt]`. The primitive discriminates.
- Known gap of bare porcelain: `corpus/instruments/r41-closure.sh:1394-1396` says "`git status --porcelain` alone misses all three mechanisms (the round-40 wave-2 F8 escape)" (gitignored entries, `assume-unchanged`/`skip-worktree` flags). r41 `worktree_state()` (lines 1397-1402) adds `ls-files -v`, `--untracked-files=all` and `--ignored=matching`. Any adopted gate should use that shape, not bare porcelain.

Ledger row 3 says "landed — unchanged", with "the operator driver porcelain check at `complete`" (round-41 section). I could not verify that driver: it is not in the lane tree (SKILL.md has zero porcelain hits). Treat it as unverified from the lane.

Draft gates already on disk (uncommitted; read-only for me):
- `.ufo/waves/round-46/wave1/R46ExecLandingA.draft/r46-landing-gate.py` (406 lines, sha256 `1e0ce85c99acf1158d80f444a5ee370c703984eb3e1003407e0647a51ce763f4`).
- `.ufo/waves/round-46/wave1/R46ExecLandingB.draft/r46-landing-gate.py` (637 lines, sha256 `7ad171e73b1b211d0fd6b8616157ffd085b4f17468a415b842ffe01ddaba8fc4`).
- Both state proposal 3 as their target and both use bare porcelain for the tree-clean limb: A line 96 `rc, por = git(lane, "status", "--porcelain")`; B line 111 `rc, out, _ = git(lane, "status", "--porcelain")`. Both repeat the R41 gap. Neither was run by me; their selftests were not executed.

So proposal 3 is NOT "implemented already" as a gate. It is implemented as counters (placeholder: D1, porcelain: E9(b)) and the adoption target is the unlanded `r46-landing-gate.py`. The ledger's "landed" for row 3 overstates this.

## 3. Ledger append needed (exact content for the L1 to commit)

The ledger is append-only (R6/R9). Proposed new section, to append at the end of `corpus/knowledge/considerthese-proposals-ledger.md`:

```
## Round-46 dispositions (appended <date>, R6/R9)

| proposal | status | evidence |
|---|---|---|
| 3. Add a quiescence gate before `complete` | proposed -> adopted in round 46: r46-landing-gate.py | Adopt only when `corpus/instruments/r46-landing-gate.py` is COMMITTED and its selftest passes; until then the row reads `proposed`. Do-nothing control: `r35-defect-closure.sh --root <base>` D1 already reads open=0 at 914ca0b (placeholder half is not discriminating on this tree). Porcelain limb must use the r41 `worktree_state` shape, not bare `status --porcelain`. |
| 2. Run one end-to-end domain task round | partially landed r40; claim-checker landed r43 (`5b4a850`, `corpus/instruments/claim-package-check.py`); remainder = SHONEN box 2 | Corrects the round-42 "absent" statement, which was measured at `ab98fac9`. |
```

Also: the existing round-42 row 3 ("landed — unchanged") should not be edited (append-only); the round-46 section above supersedes it by a new section.

## 4. Does adopting proposal 3 widen a frozen claim?

No, provided the adoption touches only a new file and the ledger. Verified by `sha256sum` against `.ufo/waves/round-46/freeze.txt`:

- `.ufo/waves/round-46/claims.json` → `e56ebf872b6073964d98812608275f5799afc9ee2334d4aab1363c06e59cd740` = `claims-sha256` in freeze.txt (match).
- `corpus/instruments/r46-c1-gate.py` → `b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294` = `c1-gate-sha256` (match).
- `corpus/instruments/r46-c2-gate.py` → `0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6` = `c2-gate-sha256` (match).

Frozen claims already name proposal 3 in the `frontier_step` field of `claims.json` ("considerthese/2026-10-26.md proposal 3 (quiescence gate) mined with the round-45 landing/ordering mistake"), so the mining is pre-declared and inside the freeze. Adoption does not:
- add a claim id, change `expect_before`/`expect_after`, or change a limb sentence in C1/C2;
- change the C1 gap target (`gap: 24 of 64`, measured on base, matches `claims.json` `before`) or the C2 row/entry targets;
- claim a score move. The claims state "No score move is claimed".

Conditions that WOULD widen a claim (must be avoided): editing `claims.json`, `r46-c1-gate.py`, `r46-c2-gate.py`, `freeze.txt` or `freeze-controls.txt`; or describing the landing gate as moving depth:verifiability or coverage.

## 5. Milestone note

The seat milestone ("build the F28 entry and C1 re-grounds as drafts; falsify frozen counters and controls") is not my item. I did not build those drafts (read-only scout). The frozen control file reads `total=9 red=9 green=0` (from freeze.txt); I did not re-run the counters.

## Limitations

- Did not run either draft's `--selftest` (`R46ExecLandingA/B`), `claim-package-check.py` selftest, `r35-defect-closure.sh --selftest` (writes scratch), or `freeze-check.py`.
- The ledger's "operator driver porcelain check at `complete`" is outside the lane tree and unverified.
- `r35-defect-closure.sh` header says a base-bytes run must read `closed=0/7`. At `914ca0b` it reads `closed=4/7`, so that header premise is stale for this base (four of seven r35 defects were already closed). Recorded, not re-decided.
- Proposal 4/6 numbers are `ls-tree` counts only; no decision is taken.
- Proposal 5 status not re-measured (ledger citation only).
- No commits, no pushes, no index changes; the only file written is this report.
