# CritMeta — Round-29 mechanics conformance review

Axes reviewed: **depth:verifiability** (lowest non-retired axis, score 4) and **coverage** (score 7). This is a review of round mechanics, not domain-source correctness. Evidence was read from the frozen claims, round prompt and hyaku lane addendum, wave spec/dispatch/ready files, receipts, and current lane tree.

## Deviations

1. **C2’s measured counters do not establish its source-binding predicate.** The frozen claim requires one entry citing S043/S044/S045 and every manifest assertion to be exactly-once (`claims.json:34–44`). Yet `manifest.json:6–29` has S043 quotes with repeated content, and `ExecManifestC2.md:13,21` reports occurrences above one while `source-recheck.py` exits 0. `CritC2Kill.md:13–39,74–93` reproduces that the counter does not enforce the claimed Q9 binding or entry-to-frontier identity. The then-current F13 entry was only a stub (`corpus/knowledge/program-severity-ladders-and-reward-scales.md:1–7`). **Impacted axes:** coverage, depth:verifiability. **Smallest safe correction:** do not count F13 as admitted until the complete entry passes Q1–Q10 and a fail-closed Q9 check binds each declared source to its capture and the F13 row. Keep the claim’s counter result separate from the admission decision.

2. **Quarantine freshness is asserted inconsistently.** The round-29 `assimilation/quarantine-slice` contains only seven staged IDs and old register labels; it has no fresh fetch/quote evidence. `ScribeAssimReport.md:44` explicitly says fresh outcomes are not claimed, while `ScribeLessonGate.md:47–62` describes the slice as hand-checked this round and gives new fetch results. The contradiction is not resolved by the cited slice. **Impacted axis:** coverage (assimilation evidence). **Smallest safe correction:** attach the handcheck command/output and per-row evidence, or describe the work as register-class review rather than fresh quarantine verification.

3. **Frontier-step completion is not evidenced at the inspected state.** `census-before.txt` records the before census (exit 0), but `ExecCanonC2.md:8–21` labels its counters PRE-STATE and says the subject had not landed; it reports 42 rows, not the claimed 45. `corpus/lessons/round-29.md` was absent at inspection, despite the round contract requiring a lesson with `## Mistakes`; `ScribeLessonGate.md` is only a draft. The required after census and final lesson were therefore not evidenced. **Impacted axis:** coverage, with depth:verifiability affected by missing audit trail. **Smallest safe correction:** record a post-integration census with output and exit code, and land the final lesson with one mined mistake, evidence pointer, captured-by criterion/rule, and a fix shown able to fail.

4. **Required round report was absent at inspection.** `.ufo/reports/round-29/kasegi.md` was not present in the fleet report listing. The round prompt requires, in order, Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, and SHONEN (`templates/round-prompt.md:99–125`). Absence means conformance was not demonstrated; it does not establish what a later report contains. **Impacted axes:** both. **Smallest safe correction:** produce the required report with evidence for each section; do not present missing sections as verified.

5. **Godspeed prompts omit the required verbatim directive.** All 64 item prompts contain `/skill:godspeed`, but none includes the host directive text (`directive.md`); this is also identified as a prompt-conformance defect in the round-28 report (`.ufo/reports/round-28/kasegi.md:14`). The lane addendum requires the verbatim directive bytes, not just the skill marker. **Impacted axes:** depth:verifiability and coverage (execution/process evidence). **Smallest safe correction:** include the host-provided directive verbatim in each child prompt on future dispatches; do not claim this wave complied.

## Conforming mechanics observed

- Frozen claims declare **two** claims on distinct axes; C1 targets **depth:verifiability**, explicitly the lowest non-retired axis (`claims.json:7–18, 27–35`). This satisfies the 1–3 claim cap, distinct-axis rule, and lowest-axis obligation.
- Frontier-step artifacts include `census-before.txt`, a named mistake source (`claims.json:55–58`), and sourced claim C2. Their existence does not cure the missing final census/lesson evidence above.
- Assimilation theme is stated as “program severity ladders and reward scales” in C2 and `ScribeAssimReport.md:3`; the requested seven-row quarantine slice exists, though its freshness claims need reconciliation.
- Inline ready file has the required fields: `lane`, `round`, `wave`, absolute `dispatch`, and `l1` (`wave1.ready:1`); `wave1.ready.dispatched` exists.
- Dispatch reports spawn=64, resume=0, total=64; spec, dispatch and registry agree on 64 seats (`wave1-dispatch.json:16–19`; member counts verified from the files). This meets the 64–100 band.

## Bottom line

The structural claim/axis and handoff/seat-count requirements are met. The main conformance blockers are C2’s unenforced admission/source-binding clauses, contradictory quarantine provenance, missing post-state frontier/lesson evidence, absent round report at inspection, and omitted verbatim Godspeed directives. No score or domain-admission judgment is made here.
