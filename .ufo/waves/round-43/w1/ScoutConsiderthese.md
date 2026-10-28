# ScoutConsiderthese — receipt (round 43, wave 1)

Item: read frozen `.ufo/waves/round-43/claims.json` (not edited), `considerthese/2026-10-26.md`, and `corpus/knowledge/considerthese-proposals-ledger.md`. Confirm the one still-unimplemented proposal this round can mine is proposal 2's claim-checker remainder, quote that proposal, draft the R31 old→new row, and state the `## Round-42 dispositions` append if it is still owed.

Lane `kasegi-shokunin`. Frozen base `ab98fac9dce87130bc4f66de89e30650d63943dc`. HEAD at measurement `4cb6d4ae768481e1a14afbedc2d865a060ebacfd` (`round-43: frozen claims…`), ancestor check exit 0. `git diff --name-only ab98fac9 HEAD -- corpus/instruments/` is empty; ledger blob `f761dbc2a724846e7c0bf607bfb21a684948fb72` is the same at base and HEAD. Instruments were read from `git archive ab98fac9`, not from the live tree. No tool installed. No mutating git. Scratch `/fast/scratch/hyaku/kasegi-r43/ScoutConsiderthese/` removed before yield.

## Answer

The one mineable unimplemented proposal is **2026-10-26 proposal 2's claim-checker remainder**. It is unimplemented at base. Round 43 C2 (`corpus/instruments/claim-package-check.py`) is that remainder. Proposals 4 and 6 stay open and operator-owned; they are not this mine. Proposal 7 is already landed; its missing `## Round-42 dispositions` section is owed upkeep and is the append in `ScoutConsiderthese.txt`. That upkeep does not replace the checker.

`grep -rli 'claim'` on the base instrument tree is **not** empty (54 paths). None of them is a checker. Direct basenames containing `claim`: 0. `claim-package-check.py`: 0. The 54 hits are the substring `claim` inside other instruments (closure "claim C1", `claims/` paths, `ops/claim-check.mjs` cited as GONE) plus `claims-erratum-d5.md` fixture copies.

## Proposal 2, own words

`considerthese/2026-10-26.md:30` at `ab98fac9` (ASCII; no non-ASCII code points on the line):

> 2. **Run one end-to-end domain task round.** SHONEN box 2 is the only box with no path forward. Proposal: take one public disclosed report (an H1 Hacktivity or Immunefi disclosure), build the six-file claim package from `corpus/knowledge/claim-package-contract.md`, and price it through F13/F17/F18. Rebuild a minimal claim checker under `corpus/instruments/`, since the `ops/*` executables are gone. That is also the first real calibration test of my claim-review rubric (`kasegi/claim-review-rubric.md` in my store).

Planks already landed before this round: the public-report package and the F13/F17/F18 price (round 40, PARKED `claimable:false`; ledger Round-41 row). Plank this round mines: the minimal checker under `corpus/instruments/`. The frozen C2 predicate does not need the r41/r42 deferral ground (a claimable-positive path). It gates well-formedness and keeps `claimable` false.

## R31 disposition row (draft — not in the append)

Land this in `corpus/lessons/round-43.md` and in a **new** `## Round-43 dispositions` section, in the same commit that adds `corpus/instruments/claim-package-check.py`. Do not put it in the Round-42 section. Do not land it while that path is absent (the record would claim a landing the tree does not have).

| proposal | status before → status after | landed pointer | remainder named open |
|---|---|---|---|
| 2. Run one end-to-end domain task round | before: `partially landed r40 — remainder open (unchanged)` (ledger Round-41 row, `:124`) → after: partially landed — claim-checker mined r43; remainder open | `corpus/instruments/claim-package-check.py` (C2, rules R-FILES, R-MANIFEST, R-REDACT, R-CUSTODIAN, R-PROVENANCE, R-STATUS, R-REPORT, R-NOSECRET); exemplar `corpus/instruments/fixtures/claim-package/exemplar/`; doc `corpus/knowledge/claim-package-gate.md` (`.ufo/waves/round-43/claims.json` C2) | SHONEN box 2 stays `[~]` (no live domain task). Exemplar stays `claimable:false`. Authorization, prior-submission, and reviewer-distinctness stay operator gates, not passed. `kasegi/claim-review-rubric.md` is not a lane path (`git ls-tree` at base: no match). |

R31 (`corpus/QUALITY.md:278`) also wants the other six proposals restated `unchanged` in that Round-43 section, not omitted. Their evidence is the Round-42 section. Only proposal 2 changes.

## Round-42 section (owed; append this)

Owed. At `ab98fac9` the ledger is 131 lines and ends `unedited.\n`. `grep -c '^## Round-42 dispositions'` → exit 1 (no heading). `grep -c '^## Round-41 dispositions'` → 2, because line 111 is scout prose (`## Round-41 dispositions` section — `grep -c …`) ahead of the real heading at line 119. Do not edit line 111 (R6/R9). Append one section; the landable bytes already start with a blank line.

`corpus/lessons/round-42.md` has no considerthese section (R31's lesson half for the round-42 touch was not filed). `LOG.md:1800-1801` only says the ledger row was appended, which is the Round-41 section.

Shape: end-of-file append, heading `## Round-42 dispositions (appended 2026-10-28, R6/R9)`, columns `proposal | status | evidence`, seven rows, then a scope paragraph. Bytes: `ScoutConsiderthese.txt` (14 lines, sha256 `76c3468bf2354968941a3543d202e374bb80919d4b8ffd1db5cd2bcc20b79f30`). Every claim in that file was measured below. Proposal 2's row there stays "remainder open" because the checker is a round-43 fact.

## Commands and output

```
$ git -C kasegi-shokunin rev-parse HEAD
4cb6d4ae768481e1a14afbedc2d865a060ebacfd
$ git -C kasegi-shokunin rev-parse ab98fac9dce87130bc4f66de89e30650d63943dc
ab98fac9dce87130bc4f66de89e30650d63943dc
$ git merge-base --is-ancestor ab98fac9 HEAD ; echo $?
0
$ git diff --name-only ab98fac9 HEAD -- corpus/instruments/
(empty)
$ git rev-parse ab98fac9:corpus/knowledge/considerthese-proposals-ledger.md
f761dbc2a724846e7c0bf607bfb21a684948fb72
$ git rev-parse HEAD:corpus/knowledge/considerthese-proposals-ledger.md
f761dbc2a724846e7c0bf607bfb21a684948fb72
```

```
$ git archive ab98fac9 corpus/instruments | tar -x -C $S/export
$ grep -rli 'claim' $S/export/corpus/instruments | wc -l
54
$ find $S/export/corpus/instruments -name 'claim-package-check.py' | wc -l
0
$ git ls-tree --name-only ab98fac9 corpus/instruments/ | grep -ic claim || echo 0
0
$ git cat-file -e ab98fac9:corpus/instruments/claim-package-check.py
ABSENT
$ git cat-file -e ab98fac9:corpus/knowledge/claim-package-gate.md
ABSENT
$ git ls-tree -r --name-only ab98fac9 | grep -i claim-review-rubric || echo NO_RUBRIC
NO_RUBRIC
```

Top-level content hits (25), none a checker: README.md, anchorcheck.py, capture-binding-check.py, capture-source.py, citation-survival.md, citation-survival.tsv, density.py, frontier-recheck-count.py, kill-rule-check.py, knowledge-expected.txt, mirror-containment-fixtures.json, r-defect-closure.sh, r35 through r42 closure scripts, recheck-audit.py, resolve-dispatch-fixtures.json, resolve.py, score-gap.py, test_resolve.py. First match in each is "claim C1", a `claims/` path, or `ops/claim-check.mjs` as a lost citation. Recursive `*claim*` basenames are only `claims-erratum-d5.md` copies under `r35-fixtures/`. The only `ops/claim-check.mjs` path at base is `.ufo/waves/round-28/wave1/MutArmC1/tmp/bounties-root/ops/claim-check.mjs`, not a live instrument. `claim-package-contract.md:19` and `:58` still name `ops/claim-check.mjs` outside the lane.

```
$ git grep -c '^## Round-42 dispositions' ab98fac9 -- corpus/knowledge/considerthese-proposals-ledger.md
(exit 1)
$ git grep -c '^## Round-41 dispositions' ab98fac9 -- corpus/knowledge/considerthese-proposals-ledger.md
2
$ git show ab98fac9:corpus/knowledge/considerthese-proposals-ledger.md | wc -l
131
$ git grep -i considerthese ab98fac9 -- corpus/lessons/round-42.md
NO_MATCH
```

```
$ python3 corpus/instruments/score-gap.py | grep -E 'gap:|Threshold'
threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."
gap: 24 of 61 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
$ bash corpus/instruments/r35-defect-closure.sh
D1 … open=0
…
closed=7/7 exit=0
$ git ls-tree -r -l ab98fac9 | awk '{n++; bytes+=$4; if ($5 ~ /^\.ufo\//) {un++; ub+=$4}} END {print n, un, bytes, ub}'
8442 8115 139341514 131709109
$ git cat-file -e ab98fac9:.gitattributes
NO_GITATTRIBUTES
$ git ls-tree --name-only ab98fac9 considerthese/ | wc -l
8
```

`SHONEN.md:249-256` box 2 is `[~]` ("no end-to-end domain hunt ran this round"). `PROVINCE.md:77` is the r36 F18 line. `LOG.md:1800-1801` is the round-42 considerthese bullet. SCORECARD, SHONEN, PROVINCE, round-42 lesson, QUALITY, and score-gap.py blobs match base. Disk guard before the archive: `/fast/scratch/hyaku` 25% used, 603.9G free. UTC of the count pass: 2026-10-28T16:42:47Z. Deliverable hashed 2026-10-28T16:44:17Z.

## Files

- `.ufo/waves/round-43/w1/ScoutConsiderthese.txt` — 14 lines, sha256 `76c3468bf2354968941a3543d202e374bb80919d4b8ffd1db5cd2bcc20b79f30`. Ledger append only.
- This receipt. Nothing else written.
