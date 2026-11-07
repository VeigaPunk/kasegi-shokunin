# CriticTrend — round 84 self-assessment audit (read-only)

Scope: `SCORECARD.md` latest rows + `Planned round 84`, `SHONEN.md`, `corpus/README.md` `## Frontier` (and the `SOURCES.md`/`knowledge-expected.txt` rows they cite) against the tree at freeze `7f76b7eb` / base `a089ff3d`. No lane edit was made; receipts are in `CriticTrend-receipts/`.

Wave shape: **one v1 wave of 12 seats** (this spec's items; `.ufo/waves/round-84/w1-dispatch.json` `counts.spawn=12 total=12`, `w1/swarm-registry.json` members=12, `lesson-round-84.md:3`). No other number is asserted.

## Bottom line

- The four numeric surfaces the brief names **agree**: census pin rows 27/27/27 (measured `selftest cases=27 failures=0`, sha `343b21e4…`); frontier 59/59/59 all `admitted`; SOURCES 118 rows with every mined used-by present and tracked, queued/rejected used-by `—`; knowledge 97 tracked at freeze (98 on disk = the untracked F60 draft).
- **8 mismatched assertions**: 2 in `SHONEN.md` (pointer `:6`, `:8`) and 6 item-level divergences on the single `Planned round 84` line (`SCORECARD.md:3099`). 0 on the pin/frontier/registry/used-by surfaces.
- **C1 is quality/gate work, not a depth move.** It is *not* dressed — the claim holds the score at 4 nominal and names the non-moving metric — but under prompt §9 the axis label `depth:verifiability` is wrong, the lowest-axis obligation is not discharged by it, and the `Saturation: depth:verifiability at 4 keeps the lowest-axis obligation` sentence is the identity claim to correct. Honest label: quality (gate hardening), nominal, no lane-scored axis move.

## Mismatches (file:line pair → one-line fix)

### SHONEN.md

| # | file:line | Claim | Observed | Fix |
|---|---|---|---|---|
| 1 | `SHONEN.md:8` | box 2 evidence blames `corpus/lessons/round-61.md` for "former roots absent and live-target testing refused" | `round-61.md` has no `absent`/`bounties`/`former root` sentence; it says "never a sandbox or live-target vulnerability test" (`:3`) and "does not call this source-reading exercise a live bounty task" (`:46`). The roots-absent sentence is `corpus/lessons/round-65-verifier-spotcheck.md:155` ("source roots absent and live-target testing refused") | cite `round-65-verifier-spotcheck.md:155` for that clause (keep `round-61.md:46` for the bounty-task clause) |
| 2 | `SHONEN.md:6` | box 1 evidence is "SKILL.md — Author assertion; outside promotion verification remains required" | the pointer is the file under test (self-reference), so it cannot resolve the box from outside; the actual non-author check is `corpus/lessons/round-47-verifier-spotcheck.md:94` ("boxes 1, 3 and 4 look fully checkable by a non-author…") | cite `round-47-verifier-spotcheck.md:94` or mark box 1 `[ ]` |

### SCORECARD.md:3099 — `Planned round 84 (not frozen)`

The freeze commit `7f76b7eb` and the round's own lesson carry six of the eight planned items as **carried/substituted**, not delivered. Each is a plan-vs-freeze mismatch on the same line:

| # | Planned item | Frozen/observed state | One-line fix |
|---|---|---|---|
| 3 | "a rename-based D3 decoy (CriticClaims probe)" | no rename-based D3: `mutbat.py:13`/`:226` D3 is the r83 trailing-comment decoy; `:168` D2 rename is pre-existing; lesson row 1 says "carried, not claimed" (`lesson-round-84.md:103`) | move to the carried list on `:3099` (or the round-85 plan) |
| 4 | "F12/F13 as counter controls" | 0 literal F12/F13 in `.ufo/waves/round-84/c1/mutbat.py` and all `controls/`; `claims.json:6` carries "defect 1 (F12/F13 forgeries; F8 limit)"; lesson row 1 | same |
| 5 | "the `comment_lines` f-string fix (ReviewC1 Major 1)" | r83→r84 counter diff hunks are only `@@ -546,6 +546,20 @@` and `@@ -561,12 +575,13 @@` (the r84_limbs selftest); `comment_lines` unchanged; `claims.json:6` carries "defect 6 (comment_lines f-string, latent)"; lesson row 6 (`:108`) | same |
| 6 | "a non-lexical G6 calibrated per R134" | C2 B8 pins the r83 gate unchanged (`claims.json:45`, sha `42f4b2ac…`); lesson row 4 (`:106`) says carried | same |
| 7 | "land and review the stated-output instrument (r82 routed defect 5)" | no "stated"/"rename" token in `claims.json`; no stated-output instrument under `corpus/instruments/`; only the r83 draft `.ufo/waves/round-83/w1/ExecStatedOutput-candidate-stated-output-check.py`; lesson row 8 (`:110`) carries r82 defect 5 | same |
| 8 | "C2 lead: OSV 'data-quality initiatives' post (ScoutPerish lead 1)" | C2 admits S118, which is ScoutPerish **lead 2** (`ScoutPerish.md:164` lead 1 vs `:182` lead 2; `claims.json:34` "It is the r83 ScoutPerish lead 2") | rewrite the line to "C2 lead: S118 Data sources page (ScoutPerish lead 2); lead 1 carried" |

Delivered planned items: the `extra` counter-selftest limb (M09; `mutbat.py:549-575`, `controls/c1-counter-mutants-r84.txt`) and the MutC1Hunt gaps (H01-H12 + six checks; lesson row 5).

## Numeric surfaces that agree (0 mismatches, re-runnable)

- **census `cases=` pins**: `SCORECARD.md:3085` (r83 After "pin rows `cases=27`"), `SKILL.md:982`, `corpus/instruments/README.md:354` all say 27; the landed instrument prints `selftest cases=27 failures=0` and hashes `343b21e4…` (base a089ff3d; r82 instrument `81677e9d…` also confirmed via `git show`). `claims.json` P8's "name 33 at landing" is a landing target, not a current-state claim.
- **frontier**: `FRONTIER-CENSUS rows=59 admitted=59 closed=59 problem-rows=0 registry=118`; `corpus/README.md` has 59 distinct F ids, all status `admitted`. Guard against a false positive: `grep -cE '^\| F[0-9]+ '` prints 61 because `README.md:699`/`:700` are round-47 provenance rows for F02/F29, not frontier rows.
- **SOURCES**: 118 rows = 97 `mined` + 2 `queued` (S111 `:123`, S118 `:130`, both used-by `—`) + 19 `rejected` (all used-by `—`); every mined used-by exists and is tracked (five point at `corpus/lessons/*.md`, all tracked).
- **knowledge**: 97 tracked at freeze (C2 B2 before), 98 on disk = untracked `corpus/knowledge/osv-gcs-data-dump-layout.md`; `knowledge-expected.txt` is 97 entries, set-equal to the tracked set. Watch item: `knowledge-expected.txt:2` says "Sorted list from the working tree… keep in sync with corpus/knowledge/" while the working tree has 98 — B2 fixes it at landing; if landing omits the row this becomes a real mismatch.
- Registry/knowledge counts across r80-r83 rows (114/94 → 115/95 → 116/96 → 117/97) are consistent with `git show a089ff3d:corpus/SOURCES.md` = 117 and the freeze = 118 (S118 queued).

## C1 — is it "quality work dressed as depth"? (§9)

**Surface changed.** Six new census checks (`recheck-cwd-census.py:729-838`: `noprefix-only`, `summary-fields`, `entry-bare-pass`, `argv-values`, `verbose-order`, `entry-set`) plus the counter's selftest limbs `extra`/`dup`/`decoy_line` (`mutbat.py:549-575`). The twelve H01-H12 rows are mutants of the instrument itself: the do-nothing control over the landed r83 bytes prints `killed=64 survived=12 neutral_ok=0/3` (`controls/c1-donothing-r84.txt:83`).

**Counterexample the claim must survive.** The depth:verifiability meter is `resolve.py` (scope: `<root>/SKILL.md` + `<root>/corpus/**/*.md`, `resolve.py:7-8`) and `anchorcheck.py` (`.md` anchors). Neither reads the census instrument, its check set, the counter, or the kill tally. The only quantities that move are numbers the instrument produces about itself: selftest cases 27→33, table rows 67→79, kills 64→76. Five of the six checks re-assert behaviours the gate already had (noprefix boundary, ENTRY set, summary fields, verbose flag); `argv-values` is CLI parsing. Under §9's sentence — "Re-scoring a rule the lane already holds on new inputs… is quality work, never coverage or depth" — this is the tool's operability/self-check, not new domain verification.

**"Dressed"?** No. The claim does not claim the score: `claims.json` axis_score says "score 4 held (nominal per R58: … the scored `resolve.py` citation-survival census does not read this instrument and is not claimed to move)", and the r83 row (`SCORECARD.md:3085`) carries the same disclosure. R58-compliant. The defect is narrower and still material: the axis **label**.

**The stall.** depth:verifiability is 4 since r15 (`SCORECARD.md:66`, 2→4), held at r18 (`:103`), and every round r70-r83 records "held at 4 / nominal" (`:2748`, `:2855`, `:2871`, `:2902`, `:3041`, `:3063`, `:3085`), with the r84 frozen claim repeating the same nominal label. The lowest-axis obligation has been carried by nominal labels, not a meter move, for the whole recent series. The stagnation nudge does not waive it: the saturation line is 9 (`SCORECARD.md:2964`) and the owned scores are 4 and 8. `SCORECARD.md:3097`'s "Saturation: unchanged; depth:verifiability at 4 keeps the lowest-axis obligation" is therefore an identity change: the 4 is cited as the obligation met, while C1 moves nothing the 4 measures.

**Honest label.** Quality work (gate/operability hardening), nominal, **no lane-scored axis move**. Closest named axis is calibration (AXES.md six-axes table: "self-assessment quality… SHONEN/SCORECARD entries match observed repo state") — but a calibration claim must count self-assessment-vs-repo mismatches (§9), which C1 does not; this review's 8-mismatch count is available if the L1 wants to record that count. `depth:verifiability` should read "held, no move".

**Smallest safe correction.**
1. Do **not** change the frozen predicate/counter/kill rule (pre-data; the do-nothing control fails the target 64/76, so the target is not do-nothing-reachable).
2. In the closure row and lesson, record C1 as "quality (nominal), depth:verifiability held — no axis move", and delete/qualify the `:3097` "keeps the lowest-axis obligation" sentence.
3. Put one of two items in the round-85 plan **before freeze**: a `resolve.py`-read metric move (e.g. the SKILL.md citation-survival numerator/denominator, or `anchorcheck.py` MISSING-FILE) or a recorded retirement/split of depth:verifiability with the reason (the scored census is no longer what the lane's verifiability work changes).
4. Update `SCORECARD.md:3099` per the table above.

## Receipts

- `CriticTrend-receipts/surface-census.txt` — pin rows + landed selftest + sha, frontier census, tracked/worktree knowledge, registry, statuses.
- `CriticTrend-receipts/pointer-probes.txt` — SHONEN pointer probes (`round-61.md:3/:46`, `round-65-verifier-spotcheck.md:155`, `round-47-verifier-spotcheck.md:94`, `PROVINCE.md:52`) and the `:3099` line.
- `CriticTrend-receipts/plan-vs-freeze.txt` — F12/F13 counts, stated/rename token counts, r83→r84 counter hunks, r83 gate sha, ScoutPerish lead lines, lesson carry rows.
- `CriticTrend-receipts/stall-evidence.txt` — r15/r18 score rows, recent nominal rows, `resolve.py` scope, do-nothing control tail.
