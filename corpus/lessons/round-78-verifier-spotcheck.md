author: hyaku closure (non-author integrator, @m_zfl)

# Round 78 — verifier spot-check (kasegi, non-author)

Subject: kasegi round 78 (attempt 1). Lane HEAD measured: `c2f4119b13bd8afd2679521fd815a1a2356cbd39`. Base: `0687cca8645884aba30c8eb5fa2d8ecaca7245cf`. Freeze: `2d81fe84506b323fb32beb137d5bd21db6a5c13d`. Report: `.ufo/reports/round-78/kasegi.md`. Frozen claims: `.ufo/waves/round-78/claims.json`. Dispatch digest (`.ufo/watchdog.log`, mutable, copied from the log at closure): `2026-11-05T10:47:08-03:00 launch kasegi round=78 pgid=1315799 driver=hyaku-inline attempt=1`; `2026-11-05T12:00:09-03:00 complete kasegi round=78; hyaku-inline attempt=1`.

This file is written by a non-author. It does not improve the round; it checks it. Commands were run by the integrator at closure; outputs quoted are observed.

## 1. Conformance

- Report authorship: `git log --format='%an %H' -- .ufo/reports/round-78/kasegi.md` (fleet repo) → `kasegi-shokunin 1daf1614003adbd30e61746fd5ebd8ea1da42aba round-78: kasegi report`. Lane identity. Commit time 11:59:02 -0300, after the landing commit at 11:58:39 -0300 (`git log -1 --format='%ad %an %h' c2f4119b` in the lane repo): the report lands after its cited commit.
- Cited lane commits, ancestry against `master`: `c2f4119b` ANC_OK; `0687cca8` BASE_OK; `2d81fe84` ancestor (yes). The lane branch tip equals `ls-remote origin refs/heads/master` = `c2f4119b13bd8afd2679521fd815a1a2356cbd39`.
- Lane state: `scripts/hyaku/jj-lane.sh state …/kasegi-shokunin` → `state branch=master local=c2f4119b… remote=c2f4119b… ahead=0 behind=0 head=detached tracked=0 untracked=0`. `git status --porcelain` in the lane: empty.
- Report sections present in order: Work performed, Landed changes, Before → after measurements, Sources & frontier (`SOURCES.md` 112 → 112 with counting command), Trend verdicts (expansion/quality/discernment), SHONEN with one line per box (`[~]`, `[ ]`, `[~]`, `[~]`), Other report items. Conformant.
- Prompt `.ufo/prompts/kasegi-round-78.md`: carries §1 MISSION/AXES binding, §2 claims, §2b frontier step, §3 L2 floor, §4 report contract (five child-lane items: report path, commit-before-report, SHONEN heading, hash citation, write scope), §5 commit/push/L0. Conformant.
- Conformance defect (status-neutral): the report's Work performed states the round's trend `discernment: unchanged` with no non-author evidence; this file supplies it (§5). Report's `C2` row claims "coverage score held at 8" while the axis verdict here is `improved` (see §3); the difference is recorded, not corrected.
- Conformance defect (status-neutral, round-78 lesson `## Gate`): the lesson's S112 row bullet does not carry the ≤25-word quote with location that CORPUS.md rule 1 asks for. Rule 1 applies to rows the round writes; S112 was written in round 77 and round 78 changed only `status`/`used-by` (allowed by rule 2). The seven quotes with locations are in the knowledge entry's Gate table, so no quote is missing; the defect is placement only.

## 2. Claims — re-measured or evidence-verified

**C2 (coverage, VERIFIED by the lane) — RE-MEASURED by the integrator.**

- `corpus/knowledge/*.md` count at base vs landing (`git ls-tree -r --name-only <rev> corpus/knowledge/ | grep -c '\.md$'`): `91` → `92`. Matches.
- Registry rows (`git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`): `112` → `112`. Matches.
- Status column (`grep -c '| mined '` / `grep -c '| queued '`): mined `91` → `92`; queued `2` → `1`. One row moved, S112 only. Matches the lane's one-row claim.
- `corpus/instruments/knowledge-expected.txt`: `93` lines / `91` `.md` rows → `94` / `92`. Matches.
- README frontier rows (`grep -cE '^\|[[:space:]]*F[0-9]+'`): `55` → `56`; `PROVINCE.md` F54 line: `0` → `1`. Consistent with one admitted frontier row.
- Literal distinctness (B6 literal half): for each of the seven claimed quotes, count of base-tree `corpus/knowledge/*.md` files containing it by `git show … | grep -qF`: `0` for all seven. Matches.
- Snapshot bytes: `git show c2f4119b:corpus/source-snapshots/round-78/S112.txt | sha256sum` → `f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907`, equal to the manifest pin and to the round-77 capture.
- Exact-line anchors (manifest quote contained in `snapshot[anchor-1]`, checked by a plain script over committed bytes): Q01, Q02, Q03 on line 24; Q09 on 166; Q10 on 168; Q11 on 169; Q13 on 195 — all `exact-on-line`; word counts 15, 7, 10, 18, 11, 9, 20 (all ≤25).
- Live re-open (integrator, 2026-11-05): `curl https://google.github.io/osv.dev/post-v1-querybatch/` → `HTTP 200 bytes 30406` (the raw size the manifest records). After tag stripping, script/style removal, entity decoding and whitespace collapse, each of Q01, Q02, Q03, Q09, Q10, Q11, Q13 occurs exactly once.
- Not re-run: the lane's gates `frontier-recheck-count.py`, `source-recheck.py`, `capture-binding-check.py`, `recheck-audit.py` are lane-owned and were not executed (PROTOCOL §Gate standard, Closure consequence). Their committed evidence was read: pre-freeze control `.ufo/waves/round-78/controls/c2-prerecheck-r78.txt` (`S112:sha256 OK`, seven `anchor=<n>-ok`), base counters `controls/c2-donothing-counters-r78.txt`, and `controls/c2-recheck-audit-base-r78.txt`.
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` (run by the integrator): six inherited W04 duplicate-url warnings (S028, S029, S072, S076, S080, S085), each `ok`, `rc=0`. Matches.
- Verdict: C2 **VERIFIED** on the counts above. Re-measured: all counts, quotes, live fetch. Evidence-verified: gate outputs.

**C1 (depth:verifiability, NOT VERIFIED by the lane) — EVIDENCE-VERIFIED by the integrator.**

- The landed instrument is unchanged: `git show c2f4119b:corpus/instruments/recheck-cwd-census.py | sha256sum` → `e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a`, equal to base. The candidate `w1/successor/recheck-cwd-census.py` is not landed, so no landed-tree measurement exists for C1.
- P3 (all eight named mutants must die by FAIL assertion) fails on committed receipts: `.ufo/waves/round-78/w1/successor/mutants/K-X2.out` ends `selftest case=gate-consume ok clean_ok=True limb_log=[True]` … `selftest cases=13 failures=0`, i.e. K-X2 survives. The mutant diff (`K-X2.diff`) matches the frozen transform row K-X2 in `c1-mutant-transforms.md`: `clean_ok is True` → `True`. The lane's named-kill count of 7 of 8 is consistent with the receipts.
- Frozen kill rule: "Any named mutant that survives (selftest exit 0) = NOT VERIFIED." Applies. Claim C1 is not verified.
- Not executed: the candidate script (an unlanded sibling artifact). Its committed `.out` receipts were read.

## 3. Per-axis verdicts (owned axes: depth, coverage — `MISSION.md` line 23)

| axis | verdict | reason |
|---|---|---|
| depth:verifiability | unchanged | C1 not landed; score 4 held; the landed counter is byte-identical to base. |
| depth:density | unchanged | no `SKILL.md` change in the round diff (`git diff --stat 0687cca8 c2f4119b` lists no `SKILL.md`). |
| coverage | improved | C2 verified: one new admitted F54 entry on uncovered ground (frontier 53 → 54, knowledge 91 → 92), S112 `queued` → `mined`. Numeric score held at 8 by the lane because the denominator is operator-owned; the axis moved, the score did not. |

No owned axis is harmed. SCORECARD diff: only the `## Round 78` section and the move-log rows are added; no earlier score row changed.

## 4. Trend verdicts (with evidence)

- **expansion: improved.** One new admitted entry (`corpus/knowledge/osv-post-batch-query-contract.md`) on ground the coverage map did not hold (literal sweep 0/7 across 91 base entries), citing the `mined` S112 row.
- **quality: unchanged.** No admitted entry superseded or re-verified; S112 was newly admitted, not re-checked. The instrument successor did not land.
- **discernment: unchanged.** Spot-check (§5): admits agree, rejects agree on the gate outcome, and one reject's stated reason disagrees (item 4). The disagreement is routed, not yet a lesson with a criterion. The lane's own self-grade is accepted.

## 5. Discernment spot-check (non-author)

The round's `## Gate` in `corpus/lessons/round-78.md` records the admits (seven clauses Q01, Q02, Q03, Q09, Q10, Q11, Q13) and rejects (Q04, Q05, Q06, Q07, Q08, Q12). Re-opened sources:

| # | item · decision | re-opened source | agree / disagree | reason |
|---|---|---|---|---|
| 1 | Q13 · admit | live `https://google.github.io/osv.dev/post-v1-querybatch/` (HTTP 200) and `corpus/source-snapshots/round-78/S112.txt:195` | agree | Quote "To get the next page of results, your next request should specify page_token only for the queries that returned next_page_token." present once live and on line 195. Not present in any base knowledge entry. |
| 2 | Q10 · admit | same live page; `S112.txt:168` | agree | Quote "An individual query within the queryset returns more than 1,000 vulnerabilities" present once live and on line 168. The entry attributes it to one query, not the whole set, which matches the page's wording. |
| 3 | Q07 · reject (restates F51) | `S112.txt:34-36` and `corpus/knowledge/osv-post-v1-query-contract.md:21` | agree | Page: "Use either version or a versioned purl, not both." F51 line 21 holds the same rule with its 400 consequence (S108.txt:40-41). Restatement of admitted ground. |
| 4 | Q12 · reject ("the threading-variance note restates ground F51 already holds at :47") | `S112.txt:170`; `corpus/knowledge/osv-post-v1-query-contract.md:47` and a grep of F51 | **disagree (on the stated reason)** | `grep -n -i 'threading\|vary' corpus/knowledge/osv-post-v1-query-contract.md` → no matches. F51 line 47 holds the pagination trigger (1,000 vulnerabilities / 20 seconds, S108.txt:136), not the variance caveat. The caveat qualifies the 1,000 and 3,000 counts in Q10/Q11 (S112.txt:168-170). The reject outcome is defensible as a qualifier that belongs with Q10/Q11, which the lane itself routed; the cited reason is wrong. |

Summary: 3 agree, 1 disagree on reason (item 4). Rejects agree on outcome, admits agree. Per LEARNING.md the disagreement is routed; no criterion added with no lesson behind it.

Other observations (not gate disagreements): the entry's Claim 4 "Rejected over-generalization" line states "3,000 is a per-query count and 1,000 is a whole-set count" before saying the page attaches them the other way round. Read as written it is a rejected reading, but it is hard to parse; a clearer phrasing is a next-round edit, not a defect in the admit.

## 6. Routed defects for the lane (next round, lane-owned)

1. **Item 4 — correct the Q12 reject reason.** Replace the F51 :47 cite in the entry's `Not claimed` line and in the lesson with the true reason (the caveat qualifies Q10/Q11). Fold the qualifier into the Q10/Q11 clause with its own quote (`S112.txt:170`) in a successor entry, or record it as a named `Q12`-qualifier note. Corrections are appended, never in-place rewritten (PROTOCOL §Evidence standard).
2. **C1 K-X2 class.** A successor must add an independent assertion on the case-6 `limb_log` conjunct before freezing; the frozen transform table must be checked against the candidate's structure first (`ReviewC1` Finding 1, `MutC1-proposals.patch`). The rule is unchanged: a surviving named mutant is NOT VERIFIED.
3. **M77-3 (census crash on nonexistent TMPDIR)** stays open until a C1 successor lands the refusal; the fix is not landed and must not be cited as landed.
4. **Lesson placement.** Move the seven ≤25-word quotes with locations into the lesson's `## Gate` for the S112 row, or cite the entry's Gate table by path, per CORPUS.md rule 1 (placement only).
5. **Coverage denominator and C2 hardening** (critic): an entry clause-set enforcement predicate and a threshold-qualifier note for Q10/Q11 — both routed, not admitted.
6. **B7 command form.** The literal `--root /home/vgpnk/Projects/shokunin kasegi` form needs the fleet conf; the explicit-dir form passes. Freeze the explicit-dir form next round.

## 7. SHONEN (non-author observation for the operator)

Nothing in this round makes a SHONEN box checkable by a non-author. Box 2 (end-to-end domain task logged) is untouched. Box 1 and 3 need the lane's own evidence of decision tables and executable instructions; this integrator has not reviewed them. Promotion is operator-owned; no `[x]` is written here.
