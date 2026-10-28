VERDICT: BROKEN

Seat R46Revenger (leaf, read-only). Question: is "re-ground a current claim onto committed bytes, mark the rest historical" a faithful answer to the original intent of gating the 24 `recheck:` lines, or a way to move the counter? Base 914ca0b; lane HEAD 323d1f5; frozen counter `corpus/instruments/r46-c1-gate.py` sha256 b0c730c8 (matches freeze.txt). Nothing committed, nothing mutated; all fixtures lived in scratch and were removed on exit.

Short answer: as the frozen C1 counter defines it, the move is a way to move the counter. The counter cannot tell a same-claim re-ground from a substitute, and a re-ground silently removes the on-restoration check of the entry it touches. It is faithful only for a narrow class of claims whose subject is a committed lane artifact.

## 1. Intent: the sentences that decide it

- `corpus/lessons/round-22.md:140-143`: "C1 is re-stated as provenance *disclosure*: headers name the lost base, and `recheck:` is a fail-closed command … ; no lost claim is presented as re-verified and the resolver fraction is not credited."
- `PROVINCE.md:13-15`: "Whether this file re-points is an operator decision, requested in `../.ufo/l0-questions.md` (kasegi round-15 row); the lane did not re-scope itself."
- `corpus/knowledge/source-tree-loss-2026-09-28.md:155`: "Facts whose only source was the DATA half can never be re-verified; they carry `[corpus-attested as-of 2026-09-28T23:32Z; source tree absent]`."
- `corpus/knowledge/source-tree-loss-2026-09-28.md:219-220`: "none is re-derivable, and no lane output should present them as live again without a restored tree."
- `SCORECARD.md:1540`: "it is an unsupported current claim until its base exists or its anchor is re-based."
- `SCORECARD.md:1545`: "an entry could instead be re-grounded on a committed capture or have its anchors marked `LOST-RECORDED`, and neither has been done for these 23 because it changes what the recheck proves."
- `SCORECARD.md:1577` (round-40 plan): "continue the 0-gated distance (… needs external bases or re-grounding)."
- `corpus/instruments/r46-c1-gate.py:7-9` (docstring): "whether a line stopped being gated because the entry was re-grounded on committed bytes, never because the line was softened."

Reading. The original gate is a disclosure device. Its job was that a reader could not take a lost-tree sentence as re-verified, and that re-verification of lost facts was deferred to "on-restoration" with the re-scope left to the operator. The lane's own r39 text (SCORECARD.md:1545) says re-grounding "changes what the recheck proves". So re-grounding is not the disclosure operation; it is a claim-level change. SCORECARD.md:1540 permits it only where "its anchor is re-based" means the same claim now sits on bytes that can carry it.

What the counter checks, and what it does not:
- The L3 limb checks only the new recheck line's shape: `r46-c1-gate.py` present, `--entry corpus/knowledge/<e>.md` present, no `~/`, `$HOME` or `/home/` after the `cd` (`gate_list`, L3 block).
- L4 and `entry_mode` check only that each row's token (>=6 chars, whitespace-normalised) occurs in a <=40-line range of a committed file under `corpus/instruments/` or `corpus/source-snapshots/`. The "current claim" column is never read.
- L5 (append-only) explicitly excludes the recheck line: the L5 block drops every `RECHECK_RE` line before comparing. So an entry's original recheck can be replaced and no limb notices.
- The frozen kill rule concedes this: `.ufo/waves/round-46/claims.json` C1 kill_rule: "a non-author reading finds a re-grounded entry whose rows do not support the entry's current claims (the rows are the semantic check the counter cannot make)".

Decision. "Re-ground + mark historical" is faithful only if (a) each re-grounded row restates the same claim with the committed artifact as its subject, and (b) the lost-tree sentences that remain keep a check that runs on restoration. The counter enforces neither.

Strongest objection to this verdict: SCORECARD.md:1540 names "re-based" as a legitimate exit from "unsupported current claim", and SCORECARD.md:1577 plans re-grounding. The lane has already accepted the operation. My objection is not to the operation but to a counter that cannot distinguish a same-claim re-base from a subject swap, and to a rule that drops the restoration check without saying so.

## 2. Falsification of the frozen counter (every run is mine; the fixture is my construction)

Do-nothing control, base export as TREE and BASE (`python3 corpus/instruments/r46-c1-gate.py --root <base> --baseline <base> --work <scratch>`):
```
gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64
gate L2 pass=0 read=base-gated=24 regrounded=0
gate L7 pass=1 read=still-gated=24 changed=none
c1-gate fixed=1/7 exit=1
```
Matches freeze-controls.txt "c1 do-nothing". The counter discriminates do-nothing from re-ground.

Marker-only control (two recheck lines replaced by `true`): reproduced `c1-gate fixed=3/7 exit=1`, matching freeze-controls.txt. The recheck-shape limb (L3) catches it.

Hollow re-ground (my fixture): base copy; `claim-gates.md` and `claim-package-contract.md` each get a `## Re-ground (round 46)` section of 7 and 8 rows. Each row's "current claim" is a claim about the lost `ops/claim-check.mjs` gate list (e.g. "claim-check.mjs requires six files in the package directory (L22-24)"). Each anchor is a line of `corpus/instruments/claim-package-check.py` or `corpus/instruments/README.md` whose text contains the row's token. Recheck lines are replaced by `cd <fixture> && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<e>.md`. Output:
```
reground entry=claim-gates.md rows=7 ok=7 files=2 exit=0
gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-clean=2
gate L4 pass=1 read=entry-mode-green=2
gate L5 pass=1 read=append-only=2
gate L6 pass=1 read=mutants=14 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```
One row (G4) states that the lost tool does not enforce `external_effects_performed` and is anchored to a line of a different tool that does enforce it. The counter grades it green.

Planted-anchor variant: I appended `# claim-check.mjs L22-24 requires report.md, claim_checklist.md, custodian-receipts.json` to the fixture's `claim-package-check.py` (line 804) in the same edit and re-anchored G1 to it. Output: `c1-gate fixed=7/7 exit=0`. The counter cannot tell an anchor that predates the entry from one written alongside it.

Score-facing audit (`python3 corpus/instruments/recheck-audit.py --root <fixture> --quiet`). Base: `executes=40 gated=24 broken=0`. Hollow fixture with the two `cd` paths re-pointed at the fixture root: `executes=42 gated=22 broken=0`. So the number the score reads moves by 2 with no check on what the rows say. (Caveat in §6.)

Conclusion of the falsification: the counter discriminates do-nothing (1/7) from re-ground (7/7), but not faithful from hollow. Its "fixed=7/7" predicate is satisfied by a re-ground whose rows are not about the entry's claims.

## 3. Where the substitution happens

- Subject of the two intended entries: "The lost claimant tool (~/Projects/bounties/ops/claim-check.mjs) was documentation-only for this lane; this file is the executable gate for the subset the contract states, and nothing more. Round 43 of kasegi-shokunin: the capability is acquired, not asserted." (`corpus/instruments/claim-package-check.py:5-9`.) The committed gate is a new implementation, not the lost tool.
- Gate sections of `claim-gates.md` with no committed counterpart (`grep -c -- <token> corpus/instruments/claim-package-check.py`):
```
APPROVED 0 | kx-reviewer 0 | DONE 0 | BLOCKED.md 0 | claim-index 0 | prepare-claims 0
not-claimable 0 | OPERATOR-GATED 0 | submitted_url 0 | submission_performed 0 | producer_identity 0
```
  `claim-index` and `prepare-claims` have no committed counterpart at all. The status state machine (`state === 'DONE'`, APPROVED, reviewer role, prior-submission guard) is absent. The committed R-STATUS checks the manifest digest, hard_gates and subchecks keys, reviewer identity, and claimable/finding_count coherence.
- The re-ground deletes the on-restoration check. Base `corpus/knowledge/claim-package-contract.md:68`:
  `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-package-contract.md  # on-restoration — …`
  After the re-ground the line is `… && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md`. If `~/Projects/bounties` returns, nothing re-runs anchorcheck over this entry's lost-tree anchors (`claim-package-contract.md:3-5, 66`). The base recheck that would have caught that is gone, and L5 permits it.

## 4. A faithful candidate outside the intended pair: `corpus/knowledge/citation-bases.md`

Its gate is not a claim about the lost tree. `anchorcheck.py corpus/knowledge/citation-bases.md` prints `BASE-ABSENT md:31 ~/Projects/the-bounty-hunter/ops/rank.mjs:55-58` and `LOST-RECORDED md:52 [lost-tree] ops/claim-check.mjs:174-199 (not checked)`, both quoted as worked examples of the vocabulary. The entry's current claims (the citation-base rules) are about `corpus/instruments/anchorcheck.py` and `resolve.py`, both committed (`anchorcheck.py` contains 25 `BASE-ABSENT` and 14 `LOST-RECORDED` tokens). It is the one entry in the 24 where a same-claim re-ground is possible. It is not in the intended pair.

## 5. The DATA-half list: which of the 24 can never honestly be re-grounded

Classification uses each entry's `source:` header and the first lines of its body. "Never" means the subject's bytes exist nowhere in the lane's committed tree, so re-grounding is possible only as a different claim.

Committed-bytes check for the lost code (read-only): `git ls-tree -r --name-only 914ca0b | grep -c '^ops/'` → `0`; `git grep -l -E 'ev_inputs|adjusted_ev|p_success' 914ca0b -- corpus/instruments` → no hits. The only committed `claim-check.mjs` is `.ufo/waves/round-28/wave1/MutArmC1/tmp/bounties-root/ops/claim-check.mjs`; `wc -lc` → `2 68`, content `function claimCheck() { return true; }`. A stub, not lost bytes, and a hazard: anything anchored there reads as passing.

A. DATA-half (subject is lost-tree records or state; never re-groundable as the same claim) — 15:
1. claim-anatomy-sample.md — `[lost-tree] ~/Projects/bounties/claims/*/*/status.json` census.
2. evidence-dir.md — `[lost-tree] ~/Projects/bounties/evidence/` (592 dirs).
3. intake-surface.md — `bounty-map/programs/*.json` (1088 records).
4. mission-ledger.md — `ledger/` jsonl.
5. operator-queue.md — `docs/claim-ready-index.md` at a lost revision.
6. program-quirks.md — `claims/cantina-pendle/…` packages.
7. repo-git-state.md — the lost repo's git state, 2026-09-28 snapshot.
8. submitted-registry.md — submission and claim records.
9. target-checkouts.md — `claims/*/*/provenance.json` scan.
10. terminal-classes.md — `docs/continuation-notes.md`, `docs/review-verdicts`.
11. ufo-archive-2026.md — `fleets/ufo-archive-2026/` snapshot.
12. ufo-workspaces.md — `.ufo/` and `.omp/` census.
13. vdp-disclosure-packages.md — `vdp-disclosures/`.
14. policy-access-playbook.md — `fleets/mission-template.md` plus `docs/autopsies/*.md` and claim evidence (body not read in full; classed on the header).
15. source-tree-loss-2026-09-28.md — the loss event record itself: window and 18-surface census. Its *absence* claim is currently true and is checked by the live test in `corpus/knowledge/root-loss-2026-10-12.md:76` (`test ! -e …`, exit 0 today), but that is host state, not committed bytes, so it does not satisfy the C1 rule.

B. CODE-half (subject is lost script behaviour; no committed bytes; re-grounding would substitute a different program) — 8:
16. claim-gates.md — `ops/claim-check.mjs` (233 lines). Partial overlap with claim-package-check.py only for the file-presence and manifest subset.
17. claim-package-contract.md — `fleets/mission-template.md` deliverable contract plus claim-check behaviour. Its six-file contract overlaps R-FILES, R-MANIFEST, R-REDACT and R-CUSTODIAN in the committed gate, but the claim as written is about the lost template.
18. ev-model.md — `ops/ev-report.mjs`, `bounty-map/schema.json`. No committed EV code exists.
19. intake-and-finalize.md — `ops/import-board.mjs`, `ops/finalize-all.mjs`.
20. mission-control.md — `ops/fleet-dispatch.mjs` (427 lines).
21. ops-invariants.md — `ops/{shared,validate,registry-check,reroute-drill,check-freshness,sighting…}`.
22. triage-thresholds.md — constants from `ops/{claim-check,ev-report,fleet-dispatch,shared}.mjs` and `schema.json`.
23. retirement-autopsies.md — `ops/park-disposition.mjs` (classifier, B) plus `docs/autopsies/` (31 files, A).

C. Re-groundable as the same claim (lane-owned subject) — 1:
24. citation-bases.md (§4).

Total: 15 + 8 + 1 = 24.

Note on the intended pair: claim-gates.md and claim-package-contract.md are both B-class. The pair was chosen because a committed gate exists, not because their subject is re-groundable. That is why the hollow fixture grades 7/7.

## 6. Limitations

- Milestone not done: I did not build the F28 entry or the C1 re-grounds as drafts. The seat is read-only and the builder seats own them. Only falsification of the counter was in scope, and I did it on scratch fixtures.
- Classification in §5 is from each entry's `source:` header and first lines; I did not read all 24 bodies in full. Entry 14 (policy-access-playbook) is the least verified.
- `corpus/instruments/recheck-audit.py`'s `strict` line on the fixture prints `cdroot_fail=61` because only the two re-grounded `cd` paths were re-pointed; the `executes/gated` limb, which the score reads, is unaffected.
- `../.ufo/l0-questions.md` (the operator decision cited at PROVINCE.md:13-15) lives at the fleet root and is off-limits to this seat. I did not read it; whether the operator has answered the re-scope question is unverified.
- No live `~/Projects/bounties` restoration was tested; the host lacks it.
- Installs: none. Commits: none. Git: read-only `log`, `ls-tree`, `grep`, `show`, plus one `git archive` into scratch.
- Scratch was removed on exit.
