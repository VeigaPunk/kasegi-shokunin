# R47W2Pointers — integrated durable-pointer review

Axes: **depth:verifiability** (unambiguous evidence retrieval), **coverage** (all five requested documentary surfaces, without manufacturing F30).

Revision: `65e19bdb142c90a08103eb4b2af60c71218a920e`; base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`.

Static review only. Read the committed lesson with `git show`; a read-only comparison found no differences between this commit and the six reviewed files (LOG, lesson, corpus README, root README, QUALITY, SKILL). Explicit committed-path lookups and local `stat` observations are saved in `R47W2Pointers.receipt.txt` beside this report. No project runtime, selftest, mutant battery, live-source fetch or domain action was executed. No tools installed/updated; no scratch created; no shared files edited.

## Evidence and finding

**Low-severity retrieval defect: several live documentary references require an unstated base directory. Their intended durable targets exist; their literal lane-root expansions do not.** This is not evidence that the underlying receipts are absent.

| Integrated citation | Literal problem | Committed resolution |
|---|---|---|
| `LOG.md:2036`, `wave1-results.json` | No file at lane-root `wave1-results.json`; round context supplies the missing directory | `.ufo/waves/round-47/wave1-results.json` |
| `corpus/lessons/round-47.md:9`, `controls/selftest-receipt.txt` | No lane-root `controls/selftest-receipt.txt`; not lesson-directory-relative either | `.ufo/waves/round-47/controls/selftest-receipt.txt` |
| `corpus/lessons/round-47.md:11`, `controls/capture-determinism.txt` | Same missing base; no literal lane-root target | `.ufo/waves/round-47/controls/capture-determinism.txt` |
| `corpus/lessons/round-47.md:9`, `round-46-verifier-spotcheck.md` | No lane-root file; this one resolves naturally relative to the lesson's directory | `corpus/lessons/round-46-verifier-spotcheck.md` |
| `SKILL.md:1183`, `entry29-fixed-bytes.md` | No lane-root file; runtime source explicitly resolves it beside the instrument (`corpus/instruments/r47-counters-selftest.py:203-206`) | `corpus/instruments/entry29-fixed-bytes.md` |

The first three observations are actual nonexistent literal paths, confirmed by `stat` and absent committed entries. The last two are context-relative references, not broken runtime dependencies. Do not classify all five as missing artifacts.

Historical finding names also need their original wave/attempt to resolve without searching:

- Lesson `:10`: `R46bW2RevEntryClaims` → `.ufo/waves/round-46/attempt2/wave2/R46bW2RevEntryClaims.md`.
- Lesson `:10`: `R46bConnPatterns` → `.ufo/waves/round-46/attempt2/wave1/R46bConnPatterns.md` (not wave2).
- Lesson `:33`: `R46ScoutLeadZDI.md` → `.ufo/waves/round-46/wave1/R46ScoutLeadZDI.md` (not attempt2).

These three targets exist in the integrated commit. Their content is historical evidence, not instructions or current admission authority.

## Positive resolution and evidence-state boundaries

- **LOG:** `LOG.md:2035-2039` points to existing claims, current ZDI entry, QUALITY and lesson. The four wave-1 review names at `:2036` resolve under its explicitly stated wave directory: `R47RevCounterC1.md`, `R47RevCounterC2.md`, `R47RevD7.md`, `R47CritNovelty.md`. Do not resolve those basenames from fleet root.
- **Lesson:** explicit current-wave paths at `corpus/lessons/round-47.md:3,13,51,55,59-61,69` all resolve in the commit. Gate capture paths at `:20-21` resolve to S075/S076 under `corpus/source-snapshots/round-47/`; the source-id shorthand at `:25-31` is bound by those preceding capture declarations. Historical review output at `:51` is explicitly a moving-tree/base replay, not an integrated-tree measurement.
- **README:** `corpus/README.md:699-700` points to both committed current knowledge entries and the round-47 snapshot directory/manifest. `:702` explicitly labels the earlier F29 row historical and current guidance S076-backed. The original S074 capture and manifest exist under `corpus/source-snapshots/round-46-a2/`; retaining them is not a stale-pointer defect. Root `README.md:12-14` points only to existing SKILL/corpus/PROVINCE surfaces, with no current-round evidence claim.
- **QUALITY:** `corpus/QUALITY.md:397,401` points to the committed lesson, D7 review and `R47RevD7.receipts.txt`; the receipt is the historical B3 before/after demonstration, not a new integrated execution.
- **SKILL:** `SKILL.md:1181-1184` names four committed instruments; `:1181` names the existing freeze record; `:1186` points to existing QUALITY/lesson. `:1177` explicitly bounds these as diagnostic and era-bounds the old F29 counter. The dependency basename issue above is documentary, not proof of a failed invocation.
- **Draft-only:** `.ufo/waves/round-47/w1/R47SrLesson.draft/round-47.md` and `.ufo/waves/round-47/w1/R47SrF30Entry.draft/zdi-disclosure-policy.md` exist but do not supersede the integrated lesson/current entry. `R47SrLesson.md:5,35-39,49` preserves draft-stage claims, including an obsolete rejected-S074 transition and a different REST-page spelling; those are not the integrated decision. The integrated lesson `:59-67` controls the recorded disposition, not the draft report.
- **Absent proposed instrument:** `.ufo/waves/round-47/w1/R47SrPlain.draft/r47-plain-measure.sh` exists; `corpus/instruments/r47-plain-measure.sh` is absent from the reviewed commit. None of the reviewed current-round appendices claims this script landed. Do not promote the draft path into a current runnable-instrument claim.

## One bounded proposed move

**Normalize only the current round's documentary evidence references into explicit lane-relative canonical paths, with short state labels (`historical receipt`, `draft only`, `current entry`).** Expand the five abbreviated references and three historical finding names above; do not move, rewrite or regenerate their targets. This connects the runtime's already-correct sibling dependency lookup to the registry's human-facing reference while preventing the draft F30/S074 transition from acquiring authority through a resolvable filename.

Affected axes: improves depth:verifiability through deterministic retrieval; preserves coverage by retaining both current-source entries and historical evidence without inventing a new frontier. No score increase is claimed.

Second-order surfaces:

- Runtime: no instrument bytes, lookup behavior or execution changes proposed.
- Contract: no frozen predicates, admission decisions, source states or B3 relaxation.
- Substrate: no capture bytes or historical wave artifacts change; old-to-new provenance remains traceable.
- Verification: a reader can open the named evidence directly without guessing wave/attempt bases; receipt existence remains distinct from semantic correctness or successful execution.

Risks: blindly rewriting every historical block would violate preservation boundaries; adding state labels must not convert archived draft assertions into current facts. Restrict any accepted repair to current-round reference text and preserve the explicitly historical F29 row. No such repair was applied by this seat.

## Contradictions that remain explicit

C1's frozen S074 rejection conflicts with retained-capture B3. The integrated lesson `:59,67,69`, LOG `:2037`, and QUALITY R54 preserve mined historical evidence and disclose C1 not fully met. C2's frozen F30 target conflicts with the F02-enrichment decision (lesson `:60,65`; README `:702`; LOG `:2038`). It remains unmet. Pointer resolution, green mechanical gates, and draft assertions cannot repair either claim failure.

## Verification handoff

Executed: static reads, committed inventory lookups, six-file commit comparison, and five literal-path `stat` queries. Unrun: all project gates, selftests, batteries and source captures. For the proposed documentation-only move, Main should check that every expanded path exists at the final reviewed revision and that historical/draft labels retain the above decision boundaries; no full mutant rerun is warranted by this proposal.

Report: .ufo/waves/round-47/w2/R47W2Pointers.md
Receipt: .ufo/waves/round-47/w2/R47W2Pointers.receipt.txt
