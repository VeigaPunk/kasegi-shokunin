# ScoutAdjacency — round 30, wave 1 (hyaku run 7 inline spawn)

Role: UFO-FSD scout (L2 leaf; no subagent dispatch). Lane: `kasegi-shokunin`.
Assignment: scan `MISSION.md`, `AXES.md` and every sibling `PROVINCE.md` (chousa, kake, kagi,
kengaku, kumitate, kotoba, kama, souji, tabi, kaidoku, tsukuroi, mado, tameshi, mori,
revenger, kotodama) and report whether any sibling lane **holds the ground of** (1) the
*Japanese severity vocabulary and JVN handling-priority model* (IPA JVN reports, CVSS→深刻度
mapping, quarterly statistics) or (2) the *C1 harness / Q9 checker instruments* (frontier-recheck-count.py,
source-recheck.py, QUALITY Q9). Report adjacency findings; absorb nothing.

## Method and evidence bytes

- Read (full files, working-tree bytes): `MISSION.md`, `AXES.md`, claims `claims.json`,
  before-receipts `c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt`,
  lane `SCORECARD.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`,
  `corpus/lessons/round-29.md`, `corpus/lessons/round-29-verifier-spotcheck.md`, the read-only
  package `/home/vgpnk/Projects/shokuknow/merge/kasegi/MERGE-REPORT.md` and `SOURCES.append.md`,
  and `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`.
- Read every sibling `PROVINCE.md` listed above (16), plus `lore`, `audio`, `game-dev-2d`,
  `game-dev-3d` (present on disk; scanned incidentally).
- Token searches over sibling lanes (all 20 sibling repos, read-only): `JVN` (case-insensitive),
  `深刻度`, `CVSS` (case-insensitive), `frontier-recheck|source-recheck|frontier-recheck-count`,
  `Q9|occurrence-not-unique|stem-mismatch|stem == id|stem==id`,
  `iPedia|登録状況|活動報告|深刻度|severity-vocabulary|handling-priority|severity vocabulary`.
- No tools installed; no writes outside the lane repo; no git/jj mutations; no live targets contacted.

## Verdict (summary)

**No sibling lane holds either ground.**

1. **Japanese severity vocabulary / JVN handling-priority (C2, F14).** The ground exists
   nowhere in the fleet but in the read-only merge package staged for this lane:
   - `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` rows **S049** (JVN iPedia
     活動報告レポート — CVSS→深刻度 band definitions; 注1) CVSSv2 基本値の深刻度による色分け, 注2) CVSSv3 …)
     and **S050** (JVN iPedia 登録状況 2026年第3四半期 — quarterly severity distribution, 図2-2/図2-3,
     CWE ranking), both `used-by` `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md`.
   - `claims.json` C2 `staged_rows_adopted`: S049→S046, S050→S047; `MERGE-REPORT.md` line 27 lists
     the knowledge entry as a staged new-file (round2).
   - Fleet-wide `深刻度` hits: **0**. JVN hits: only kake sitemap crawl fixtures (ruby-lang.org
     URLs in data), kotoba omp-binary string tables and random base64 test fixtures — none semantic.
   - `CVSS` hits in siblings are peripheral (kagi NVD-API capture fixture; kotoba disclaiming
     kasegi's F01–F08 as not craft; mori archived GitHub-page capture; chousa/kake/souji/tsukuroi/
     kaidoku/kotodama random-byte or man-page hits). None maps CVSS to Japanese 深刻度 or owns
     JVN statistics.
2. **C1 harness / Q9 checker instruments.** `frontier-recheck-count.py` and `source-recheck.py`
   (kasegi `corpus/instruments/`) and QUALITY Q9 are kasegi-owned. Siblings cite them as
   *prior art / method overlap* only:
   - chousa `ConnectorSiblings31.md:29-33` — mechanism comparison of `anchorcheck.py`/`source-recheck.py`
     vs lore/kagi/kumitate gates (review, not ownership);
   - kagi `ConnKasegi.md:41` — "Recheck prior art" note on `source-recheck.py`;
   - tabi `ConnSiblings.md:112` — instrument inventory, verdict "method overlap → report adjacency";
   - mori `ConnSiblings.md:9` — "Cite only; no reuse" for `corpus/instruments/source-recheck.py`.
   No sibling runs `frontier-recheck-count.py`; the Q9 semantics (stem==id, exactly-once occurrence,
   anchor-verified) appear in no sibling bar.

## Per-lane scan (16 named siblings)

| Lane | PROVINCE domain (verbatim core) | Holds theme 1 (JVN/深刻度)? | Holds theme 2 (C1/Q9 instruments)? | Evidence |
|---|---|---|---|---|
| chousa | deep-research method (調査); owns question framing, source hierarchy, citation chaining, claim-vs-source verification | No | No (reviews kasegi's instruments at `ConnectorSiblings31.md:29-33`; own Q-numbers Q1–Q37 are a different bar) | `PROVINCE.md:3-17`; `grep JVN/CVSS/深刻度` → no semantic hits |
| kake | web properties & publishing; explicitly refuses vulnerability handling ("report intake, triage, remediation, disclosure timing, bounty and policy operation … are not kake's ground") | No | No — but runs its **own** same-named instrument `kake-source-recheck-v1` (`measure.py`, round-26) over its 32-row web-property population; different schema/subject, cite-level name collision | `PROVINCE.md:283-287`; `.ufo/waves/round-26/verification/measure-final.json` |
| kagi | secrets & vault ops; refuses anything outside | No (NVD/CVSS bytes appear only in a retained API-capture fixture) | No (prior-art review of kasegi's `source-recheck.py`) | `PROVINCE.md:3-67`; `ConnKasegi.md:41` |
| kengaku | LLM/model research & evaluation; kasegi adjacency = bounty-ledger mission-state/dispatcher semantics | No | No | `PROVINCE.md:3-143` |
| kumitate | orchestration & tooling (OMP, ufo-fsd); routes MCP/OAuth security practice → kasegi/kagi | No | No | `PROVINCE.md:3-28` |
| kotoba | prompt & skill craft; explicitly disclaims kasegi's Frontier F01–F08 (incl. CVSS v4) as "no skill or prompt craft" | No | No (own Q9 in kake-style numbering is its own bar) | `RowKasegi.md:29`; `PROVINCE.md:3-69` |
| kama | local model serving & endpoint health | No | No | `PROVINCE.md:3-53` |
| souji | fleet/workspace hygiene (掃除) | No | No | `PROVINCE.md:1-87` |
| tabi | browser & web-interaction craft; reports kasegi instrument overlap, absorbs nothing | No | No (instrument inventory verdict "report adjacency") | `ConnSiblings.md:112`; `PROVINCE.md:1-21` |
| kaidoku | RE of shipped artifacts with REA | No | No — uses "stem-mismatch" only in its own EVM evidence-ledger attack fixtures (`arc3-loop1-round1/claims/c1/EX-13/verify-battery.py:15`, `arc3-loop1-round3/claims/c1/EX-14/inputs/attacks.py:80`) | `PROVINCE.md:3-300` |
| tsukuroi | host operability & system repair; ADJ-06 routes driver/firmware RE to kaidoku/revenger | No | No | `PROVINCE.md:3-193` |
| mado | desktop & compositor craft | No | No | `PROVINCE.md:3-95` |
| tameshi | verification-fixture craft/mutation method; refuses product domains — "every lane's gate remains its own"; recorded legs are kumitate/kagi/kaidoku/game lanes/tsukuroi/mado, **not kasegi** | No | No (method owner only; never edits a sibling's gate) | `PROVINCE.md:3-118` |
| mori | fleet & host observability; cites kasegi's `source-recheck.py` "cite only; no reuse" | No (own C2 "severity vocabulary" = warn/crit roll vocab, unrelated) | No | `ConnSiblings.md:8-9`; `ReviewC2Contract.md:22` |
| revenger | RE of shipped artifacts with evidence ledger; explicitly **refuses** "harness/evidence auditing (harness-integrity, gate-evidence, rlm-dispatch)" | No | No (explicit refusal) | `PROVINCE.md:19-23` |
| kotodama | linguistic-cultural worldbuilding; own gate "severity vocabulary" `[reject]/[hold]/[note]` is internal finding-severity, unrelated to JVN | No | No | `corpus/knowledge/synthesis/finding-disposition-workflow.md:20`; `reports/round-9/baselines/registry.md:116` |

Other lanes scanned incidentally (not in the named list): `lore` (fictional-world records; no),
`audio` (game audio production; no), `game-dev-2d`/`game-dev-3d` (game production; both refuse
harness/evidence auditing; no). Protocol/aggregator lanes live at the fleet root
(`MISSION.md`): they own fleet-meta protocol/gate integrity and cross-lane quality/mint/dormancy/
corpus review — integrators of corpus review, not domain ground; they never appear as owners of
either theme.

## Adjacency findings (report only, nothing absorbed)

1. **Same-name/different-mechanism collisions** — `source-recheck` exists in three distinct
   contracts: kasegi `corpus/instruments/source-recheck.py` (captured-source manifest, Q9),
   kake `scripts/source_recheck.py` + `kake-source-recheck-v1` (web-property population HOLD/STALE),
   and mori's round-36 cited prior art. `stem-mismatch` also appears in kaidoku's EVM ledger
   fixtures; `severity vocabulary` in kotodama/mori gate vocabularies. None overlaps kasegi's.
2. **Sibling reviews of kasegi's instruments** (chousa connectors, kagi ConnKasegi, tabi
   ConnSiblings, mori ConnSiblings) are the only cross-lane traces of the C1 instruments; all are
   review/citation, none ownership — consistent with the adjacency axis (report, don't absorb).
3. **JVN theme origin is external to the fleet**: the package `/home/vgpnk/Projects/shokuknow/merge/kasegi/`
   (read-only) is the sole holder of S049/S050 and the staged entry `japanese-severity-vocabulary-and-impact-model.md`;
   lane may land it as C2/F14 with S046/S047 per `claims.json` `staged_rows_adopted`.
4. **No contested scope found** for either theme in any sibling PROVINCE.md; no L0 question needed.

## Confidence and limits

- PROVINCE.md scans: complete (16 named + 4 incidental), read at current working-tree bytes.
- Token searches: full-repo greps over sibling lanes; hits evaluated semantically. Noise from
  wave scratch/fixture files (base64 strings, sitemap data, binary string tables) was identified
  and excluded; listed as such above.
- `[INFERENCE]` only where a classification (e.g. "no semantic hit") rests on reading hit context
  rather than a formal semantic check; the zero-`深刻度` result is a literal scan.
