# Round 61 — three python-head escape probes refused; F42 Big Sleep SQLite case admitted

Claims: C1 depth:verifiability (lowest owned axis, nominal per R58, 4 held); C2 coverage (8 held). Frozen predicates and kill rules: `.ufo/waves/round-61/claims.json`, freeze `6f88f3a7f6b9689b49241e3f4a8e551c57a3f766`, base `c33d24ddd11abf1ebdea0dccf7327e9069dd9104`. Implementation `13c8060b343e002339ffd72da37ff74514f82765`. This round is a named probe-set repair and first-party documentation research, never a sandbox or live-target vulnerability test.

## Mistakes

Sweep: read all eight routed defects in `corpus/lessons/round-60-verifier-spotcheck.md` section 6; run the commands in `.ufo/waves/round-61/controls/carry-in-r61.txt` and the base probe runner. The first measurement shows R79/R80 missing (0 each), while the base gate executes P1/P2/P3 (markers=1 each). These are red-before controls, not an assertion that no mistake exists.

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M61-1 | number-drift / unlanded criterion claim | round-60 closure D1; round-60 LOG says R79/R80 landed, base row counts are 0/0 | none — a proposed criterion was mistaken for an existing row | R79/R80 land now, counts 1/1 in controls/carry-in-r61.txt; R83 requires checking the actual rows |
| M61-2 | instrument / literal-prefix traversal | controls/c1-probes-base-r61.txt: P1/P2/P3 markers=1 | R72 named the residual; not closed by r60 | resolve script path against derive root, preserve original prefix restriction, follow symlinks; candidate P1/P2/P3 exit=2 markers=0; the confinement-off mutant is killed |
| M61-3 | reference-drift | round-60 closure D2/D3/D4/D6: stale digest line, dead receipt pointer, unsupported base-limb pointer, unlocatable DeepMind 404 | R19 stale premise; outside closure | append the corrections below and SKILL pointer reconciliation; base-limb line measured in carry-in receipt; withdraw unsupported 404 rather than invent its URL |
| M61-4 | vacuous first probe fixture | first runner draft put P2's script in its child root while its three-up path resolves to the parent | R79 environment requirement | put the script in both places before freezing; final BASE P2 actually creates its marker (exit=1 markers=1) |
| M61-5 | process-order | stand-in frontier counter ran before a recorded sentence-by-sentence claim table | R76 | record as a process miss; the wave's EntryClaims table is the later safety net, not retroactively a pre-count table |

## Carry-in corrections — round-60 D1–D8

- D1: the actual r60 criteria were R78/R81/R82, not R78–R80. R79/R80 are added THIS round, append-only after R82. LOG and SCORECARD corrections name the error; R83 guards a recurrence.
- D2: `round-60/controls/freeze-digests-r60.txt` line 1 records stale instrument digest `91b46e7f54…`, not the frozen/landed `35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2`. The r60 bytes match the latter; the old receipt is not silently regenerated. This is the correction of record.
- D3: SKILL's historical `controls/c1-probes-lane-after-r60.txt` is erroneous. The real paths are `.ufo/waves/round-60/controls/c1-lane-after-r60.txt` and `c1-lane-after-committed-r60.txt`; the appended SKILL correction resolves the pointer.
- D4: `.ufo/waves/round-61/controls/carry-in-r61.txt` now actually prints `R74-base-limb=0` from r60's base `cdeea55bea09ed08765d3c3d3a56f23db44e66f4`. The old receipts never printed that limb, so their earlier attribution was wrong.
- D5: supersede round-59 Gate rejection (a)'s unqualified “no README text is locatable there”: absence holds ONLY after capture-source.py's HTML conversion removes scripts. Raw issue HTML contains README text in bootstrap script data, as `round-59-verifier-spotcheck.md` section 3 records. The machine endpoint remains the chosen capture route; this correction makes no raw-HTML absence claim.
- D6: withdraw the alleged DeepMind 404 and supposed round-58 history pointer: no recorded URL/result can be recovered from the named bytes. It is an unsupported historical assertion, not an opened source or rejection. The old 2024-post deferral now flips: this round opened it and found the SQLite case ground below.
- D7: SHONEN box 2 now has one evidence line, not four; its mark stays honestly open.
- D8: r60 formalized ONE new capability row (`derive-gate-chain-refusal`) and extended ONE existing row (`move-log-figure-audit`), not “two new capability rows”. No new capability acquisition is asserted this round; C1 extends existing behavior.

## Gate

S094 — https://projectzero.google/2024/10/from-naptime-to-big-sleep.html, accessed 2026-11-04; source page dated 2024-Nov-01, Big Sleep team (S094.txt:13-15). The URL's 2024/10 path is not its publication-date assertion. capture-source.py default urllib/UA HTML conversion fetched HTTP 200, 56257 raw bytes at 2026-11-04T14:13:15Z; snapshot `corpus/source-snapshots/round-61/S094.txt`, 15904 bytes, 125 lines, sha256 `663ac16df13b7c93c2d9848265854625c46e8f59d0c39a5bbb4d68bf6573e804`. Manifest `corpus/source-snapshots/round-61/manifest.json` pins seven quotes. Located quotes below (counts use Python whitespace splitting; every quote <=25 words):

| quote | location | words | text |
|---|---|---|---|
| Q1 | S094.txt:18 | 17 | we found this issue before it appeared in an official release, so SQLite users were not impacted. |
| Q2 | S094.txt:25 | 17 | We collected a number of recent commits to the SQLite repository, manually removing trivial and documentation-only changes. |
| Q3 | S094.txt:25 | 14 | provide the agent with both the commit message and a diff for the change |
| Q4 | S094.txt:112 | 12 | The harness used by OSS-Fuzz isn't built with the generate_series extension enabled |
| Q5 | S094.txt:113 | 9 | the issue remained undiscovered after 150 CPU-hours of fuzzing. |
| Q6 | S094.txt:118 | 5 | these are highly experimental results. |
| Q7 | S094.txt:118 | 15 | it's likely that a target-specific fuzzer would be at least as effective (at finding vulnerabilities). |

Admit: `corpus/knowledge/project-zero-big-sleep-sqlite-variant-analysis.md`, F42 on S094. The account's pre-release exposure qualification, recent-commit seeded setup and harness-bound AFL negative result add a dated real-world finding case. F04 already holds principles, F40 the tracker, F41 the later V8 comparison; none held this SQLite account (`controls/neighbor-screen-r61.txt`, recorded before freeze). Anchor-referent table: `controls/anchor-referents-prefreeze-r61.txt` (13 printed anchor lines, source lines read before the freeze); the wave's ExecAnchors provides the pre-landing independent table.

Reject: reading S094 as universal agent superiority or proof that fuzzing cannot find this class. Reason: S094.txt:118 calls the results highly experimental and says a target-specific fuzzer would likely be at least as effective. Flip: independent comparative evidence with a declared population and comparable budgets — not supplied by this case. No rejected source row is fabricated: this is a rejected inference from the mined S094 source, not a rejected document.

Defer: Fuzzilli primary docs, unopened (lead only), because no new tool-technique instruction is needed for this bounded finding account and province/sibling ownership must be screened first. No claim rests on them. No assimilation package entry adopted. `considerthese/2026-10-26.md` was read; proposal 2 (a real end-to-end claim package) is not implemented here, and the report does not call this source-reading exercise a live bounty task.

Outside discernment review is owed to the non-author closure; the lane's own dispatched seats are still the lane (LEARNING.md). Their source, claim and scope checks are evidence, not promotion verification.

## Sources & frontier

Base controls/do-nothing-c2-r61.txt: rows=41 admitted=41 closed=41 problem-rows=0 registry=93; entries=44 pass=44; capture records=76 bound=76. Stand-in controls/c2-standin-r61.txt: rows=42 admitted=42 closed=42 problem-rows=0 registry=94; FRONTIER-PASS F42 ids=S094; entries=45 pass=45; capture records=77 bound=77 unbound=0; seven Q-OK lines; census exit 0. Commands are frozen in claims.json. Start census is durable in controls/census-round-start-r61.txt (exit 0; pre-existing W04 warnings).

Rows added by tier: A=1 (S094 docs/mined/recheck 90d). Existing registry status/recheck/used-by cells: unchanged (no old→new changes). Leads old→new: ISO retired as S089/S090; AISI as S091; GitHub REST as S087; CISA list as S088; OpenSSF narrowed to unopened aggregate/API ground (S086 holds checks); Big Sleep SQLite post admitted as S094; Fuzzilli remains unopened. The NVD S085 search-log paragraph is moved from Leads to Search log. SOURCES Registry-changes bullets log the same reconciliation and withdraw the unsupported DeepMind assertion.

Assimilation: none — `merge/kasegi/` not adopted, no staged ids or rows appended; no renumber map required.

## Limits

C1 is an empirical three-probe improvement, nominal under R58 (score 4 held), not an OS sandbox. The code examines undecoded shell text; shell expansion remains explicitly open in claims.json. Other heads' write/execute flag spellings and allowed Python counters' own writes remain open. The frozen instrument retains its pre-existing overbroad docstring phrase “the audit never runs a mutating command”; that phrase is contradicted by known residuals and is not this round's promise. A later instrument claim must correct it before its new digest freeze. Selftest case counts remain host-conditional because it invokes bare python (R82). The new runner explicitly requires GNU coreutils, bash, python3 and a guarded /fast/scratch/hyaku/kasegi-r61 seat path.

C2 does not reproduce SQLite exploitation, rerun AFL, verify the publisher's priority claim, or give general agent evaluation/method advice. Its 150 CPU-hours is an attributed source value, not this lane's measured cost. R67 body-substance counter and R69 census-range-base decisions remain open in existing kasegi round-57/58 L0 rows; round-59 sandbox and round-60 decoded-flag boundary questions also remain unanswered in the queue read this round.

## Wave-1 integration — WAVE-DONE received before filing

The orchestrator delivered WAVE-DONE for all 11 dispatched seats and `.ufo/waves/round-61/w1-results.json`. Eight seats produced evidence files; ScoutSource, EntryClaims and SiblingOverlap have empty outputs and no report. They are not treated as successful verification and are not replaced. Role mix dispatched: scout1, scribe1, connector1, reviewer2, critic2, mutation-tester1, executor3. Attack seats5/11; connector1/11; L1 holds the planner seat.

| seat | observed recommendation | integration |
|---|---|---|
| ReviewC1 | PASS, frozen predicate and both digests reproduce | C1 verified on named probes, not universal confinement |
| ReviewC2 | PASS, all five counters and 93 old registry rows reproduce; stale old tracker statement found | appended correction in google-big-sleep-findings-tracker.md; no frozen predicate changes |
| CriticPython | No frozen counterexample; 11 quoted/expanded variants still execute outside, including `python3 corpus/instruments/"../../outside.py"` with audit exit0 on both base and pin | residual explicitly named; no new security guarantee inferred |
| MutationPython | committed battery3/3; prefix-off and boundary-separator-off mutants survive selftest and runner | valid survivors recorded open under R17; next instrument claim's test obligation |
| ExecCounters | frozen after-wants reproduce; runner scratch argument safely relocated to owned seat path | commands are parameterized by scratch; not a fake literal shared-path execution |
| ExecAnchors | 21 references hold (entry10, registry6, README5); seven quotes occur once, 89 words total | corroborates the prefreeze anchor reading |
| ExecRegression | Q1–Q7 refused, controls pass; 192 base/pin comparisons show87 unchanged admissions,72 unchanged refusals,33 tightenings,0 new admissions | bounded no-new-admission guard, not universal no-harm proof |
| HarnessAttack | named probes pass; runner can delete an instrument beneath its scratch arg and return0; broken instrument99 and failed find can still return0 | collector status is not a predicate verdict; freeze unchanged, defects named for next counter claim |
| ScoutSource / EntryClaims / SiblingOverlap | no evidence delivered | no invented votes; L1 fallback source reopen, sentence table and scope sweep below |

L1 fallbacks (not independent seats): `controls/l1-source-second-open-r61.txt` records a second public curl open, HTTP200/56257 bytes, byte-identical conversion sha663ac16d… and seven exact quote anchors; `controls/l1-sentence-table-r61.md` reads the substantive assertions and reject against the full capture; `controls/l1-sibling-scope-r61.txt` excludes SQLite storage/catalog/TB2-grader lexical hits from this first-party finding account. Independent source/scope review remains owed to the non-author closure. No L1 fallback is called a dispatched scribe/scout/connector success.

The full downstream/sibling screen was completed only after freeze (`controls/neighbor-screen-postfreeze-r61.txt`). The prefreeze receipt screened knowledge/README/PROVINCE/SOURCES/SKILL but omitted snapshot consumers and sibling PROVINCEs: this is an R80 process miss, not retroactively a full extended prefreeze pass. The postfreeze screen locates the old tracker reading-list pointer and no already-admitted SQLite case; the tracker correction makes its old “no admitted source row” statement explicitly historical.

Routing: live operator authority moved all18 roles to @m_zfl for Devin account/model unavailability (`scripts/hyaku/lane-addendum.md:569-573`, fleet commit `0ad04e305ddcad137802299fe6c17bf3d7669045`). Existing seats retain captured routes; no lane config mutation or safety-refusal retry occurred. Models are not asserted from role labels alone.

## Mistakes — wave and process additions

| id | class | evidence pointer | captured-by | fix or honest disposition |
|---|---|---|---|---|
| M61-6 | process-order / incomplete screen | prefreeze screen vs postfreeze consumer/sibling screen | R80 | full screen performed as safety net; order miss recorded, no retroactive conformance claim |
| M61-7 | harness / collector exit mistaken for verdict | w1/HarnessAttack.md: instrument-under-scratch removed, eight execution failures still runner exit0; find failure masked | R82 | outputs must be compared to named tuples; no exit0-only pass claim. Repair held for a new pre-data counter claim; raw runner remains frozen evidence |
| M61-8 | survivor | w1/MutationPython.md: prefix-off and boundary-separator-off survive | R17 | named open, not suppressed; next claim must kill these valid mutants |
| M61-9 | stale-premise introduced by new admission | w1/ReviewC2.md; tracker entry lines62–63 | R19 / report review | appended dated correction makes former unopened-post statement historical |
| M61-10 | provider / missing evidence | w1-results.json, three empty outputs with no report | wave accounting rule | no success inferred and no replacement; L1 completes reachable checks, independent verification debt remains explicit |

**Verdicts against frozen predicates:** C1 verified (ReviewC1, ExecCounters); C2 verified (ReviewC2, ExecAnchors, grounded L1 table). Scores held4/8, density9 untouched. Scoped regression matrix found0 new admissions; known shell-expansion residuals existed on base too. Expansion improved (new dated finding case on uncovered ground); quality unchanged (no stale source or failed admitted entry recheck left unmarked); discernment improved through the outside round-60 D1 correction and R83, while independent round-61 admit/reject spot-check remains owed. These are lane recommendations for closure, not promotion verdicts.

**Nonproducing-seat telemetry (parent supplied, preserved verbatim in `.ufo/waves/round-61/seat-error-telemetry.json`).** ScoutSource-11, EntryClaims and SiblingOverlap-12 each recorded `Devin stream error permission_denied: This model is no longer available for your account. Please switch to a different model.` (swe-2/devin), followed by `401 Invalid 'Authorization' header or token. (type=authentication_error param=UNAUTHORIZED)` (deepseek/deepseek-v4.1-flash/commandcode). These are actual recorded error events, not inferred terminal job statuses; proc records expired, so terminal status is unavailable. Accounting: 11 dispatched,8 evidence-producing,3 errored/no-output seats; no replacement or retry. The parent retained the dispatcher identities and supplied session provenance; this lane did not read historical session transcripts.
