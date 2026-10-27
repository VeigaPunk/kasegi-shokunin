# kasegi-shokunin corpus — index

Proprietary memory for the bounty & security research domain. Everything here
was read from `/home/vgpnk/Projects/bounties` on 2026-09-28; each entry names
its source. No generic filler. [r22 correction: this holds for the 25 legacy entries only; the five round-22 entries (Frontier F01–F05) were read from public sources S001–S015 on 2026-10-19 — see SOURCES.md; r23 correction: the three round-23 entries (Frontier F06–F08) were read from public sources S018, S031 and S029 opened 2026-10-20 and 2026-10-25 — 33 entries in total; r24 correction: the round-24 entry count is 35 — F09 admits two entries read from public sources S032-S035 opened 2026-10-25; r25 correction: the round-25 entry count is 37 — F10 admits two entries re-grounded from public sources S036-S040 captured 2026-10-25]

## Coverage map

| Area | Entry | Source basis |
|---|---|---|
| Claim-package contract | `knowledge/claim-package-contract.md` | `fleets/mission-template.md` + live packages |
| Complete claim-gate list | `knowledge/claim-gates.md` | `ops/claim-check.mjs`, `ops/claim-index.mjs`, `ops/prepare-claims.mjs` (read in full) |
| Policy access per platform | `knowledge/policy-access-playbook.md` | `mission-template.md`, `docs/autopsies/`, `claims/bugcrowd-seek/` |
| Triage economics | `knowledge/ev-model.md` | `ops/ev-report.mjs`, `bounty-map/schema.json` |
| Mission outcome statistics | `knowledge/terminal-classes.md` | `docs/continuation-notes.md`, `docs/review-verdicts.jsonl`, `docs/wrap-report.md` |
| VDP disclosure packages | `knowledge/vdp-disclosure-packages.md` | `vdp-disclosures/anthropic-plugin-dev-cmd-injection/` + `claims/*-vdp-no-payout/` |
| Mission ledger + ops | `knowledge/mission-ledger.md` | `ledger/*.jsonl` census, `ops/shared.mjs`/`rank.mjs`/`import-board.mjs`/`fleet-dispatch.mjs`, `docs/plan-round0.md` |
| Mission control plane | `knowledge/mission-control.md` | `ops/fleet-dispatch.mjs` full read, `fleets/missions|run|leases|priority|state-snapshots`, `claimer-mission.md`, `review-mission.md`, sighting scripts, `RUNBOOK-resume.md`, `.ufo-mission-report-bh*`, `.ufo-ingestion/`, `.ufo-warden/` |
| Per-program audit store | `knowledge/evidence-dir.md` | `evidence/` census (592 dirs), `ops/fleet-dispatch.mjs`, `evidence/bugcrowd-seek/`, `evidence/sherlock-8/` |
| Retirement + autopsies | `knowledge/retirement-autopsies.md` | `ops/park-disposition.mjs` full read, `docs/autopsies/` 31-file census, `fleets/run/` live classifier re-run |
| Ops integrity layer | `knowledge/ops-invariants.md` | `ops/shared.mjs` (BANNED/PARKED/K3/TELEMETRY_EVENTS/gitMutationBlocker), `validate.mjs`, `registry-check.mjs`, `reroute-drill.mjs`, `check-freshness.mjs`, `sighting*.sh` — all read in full |
| Board intake + batch finalize | `knowledge/intake-and-finalize.md` | `ops/import-board.mjs` (binding/P6/P7/S4) + `ops/finalize-all.mjs` (claim sweep/tag/atomic push) — full reads |
| Claim-hardening defect taxonomy + archive | `knowledge/ufo-archive-2026.md` | `fleets/ufo-archive-2026/` full walk: 20 `claim-*` report.json defect censuses (round-12 correction), keeper/whipper (b1k-NNN origin), inquiries briefs, programs/ old evidence shape |
| Submitted-state / do-not-refile registry | `knowledge/submitted-registry.md` | live census: all `claims/*/*/status.json` submission fields (19 signatures), `ledger/missions.jsonl` SUBMITTED/DISCLOSED_FREE, `portal-reconciliation-2026-09-11.json`, `final-audit.json`, `origin-work/open-bug-bounties/claim-packages/submission-review/` (real receipt store), VDP `SUBMITTED.md`, `claim-ready/*`+`claim-hold/*` tags, `_claimer.status.json`, 15 status-less stub dirs |
| Operator queue audit | `knowledge/operator-queue.md` | live `claim-check.mjs` re-run of all 12 queued rows + `claim-index.mjs` source read (`claim-hold/*` inert), per-row checklist gates, runbook distill, anthropic↔VDP fingerprint byte-match |
| Intake surface (map census, ingestion path, registry decrees) | `knowledge/intake-surface.md` | 1088-record census, `fleet-dispatch.mjs::buildQueue` scoring source read, `.ufo-ingestion/` full walk, `fleets/registry.json` decree ledger, live `check-freshness`/`validate` runs |
| UFO runtime workspaces (`.ufo/` layer + `.omp/`) | `knowledge/ufo-workspaces.md` | full census: 25 `bh*` warden workspaces + 22 reports + `reroutes.jsonl` (121 records), `bounty-fleet/` 805 M keeper tree (second `missions.jsonl`), `sessions/` bpolish1..8 (refile verdict NONE + grep traps), `grok-bounty-assessment-20260911/` (frozen, self-invalidating), `claim-recovery/`, `.omp/` tracked-vs-live, root `README.md`/`.gitignore` |
| Repo git state | `knowledge/repo-git-state.md` | live `git status/branch/rev-list/merge-base/ls-files`: stalled mid-rebase ≥17 days, 903 dirty entries, 12 tags pushed, `claim-ship` superseded ancestor, claims/ 198 tracked files vs 3361 on disk |
| Target checkouts + provenance pins | `knowledge/target-checkouts.md` | `pendle-core-v2-public/` (shallow clone `f242659`=v6.10.0, pin-bound), `george/` parked, 187/255 `provenance.json` pin census, `[lost-tree] claim-check.mjs:96-97` never validates pins (lost-tree line range; mirror `ops/claim-check.mjs` is only 83 lines) |
| Canonical triage thresholds (gates/weights/constants, line-cited) | `knowledge/triage-thresholds.md` | full reads of `ops/claim-check.mjs`+`ev-report.mjs`+`fleet-dispatch.mjs`+`shared.mjs`+`bounty-map/schema.json` + live censuses; 3-way verified round-13 (L1 read × executor draft × reviewer derivation) |
| Per-program quirks (fee/precondition patterns) | `knowledge/program-quirks.md` | sibling-package sampling (dydx same-blocker class; morpho/euler/uniswap/reserve honest-zero) — index-orphaned until round 13 |
| Claim-anatomy sample (per-program `status.json`) | `knowledge/claim-anatomy-sample.md` | round-14: 20 NEW full reads via deterministic stratified rule (script preserved, L1-reproduced); 10→30/280 = 10.7%; deviation classes D1-D13 with anchors |
| Source-tree loss + mirror provenance (PROVINCE root absent) | `knowledge/source-tree-loss-2026-09-28.md` | round-15: detection commands, 23:32Z–23:51:31Z disappearance window, per-file mirror provenance (`wc -l` + sha256 + anchor verdicts for 11 files), forensic blind spots, anchor-base rule, resolvability census, the never-re-verifiable DATA-half list, 9 L2 audit corrections |
| Root loss — second event (mirror + origin-work absent; ufo-fsd relocated) | `knowledge/root-loss-2026-10-12.md` | round-19 re-census: `the-bounty-hunter` and the whole `origin-work` tree ABSENT (no relocated copy); `ufo-fsd-alpha` relocated intact to `~/Projects/ufo-fsd-alpha` @ `964f443e`; `[lost-base]` vocabulary, derived-root instruments, `BASE-ABSENT` verdict |
| Depth instruments (committed, re-runnable; r23 adds `mirror-containment-check.py` + `mirror-containment-fixtures.json` and `source-recheck.py` + `source-snapshots/round-23/manifest.json`; r24 adds `capture-source.py`, `resolve-dispatch-check.py` + `resolve-dispatch-fixtures.json`, `frontier-recheck-count.py` and `source-snapshots/round-24/manifest.json`) | `instruments/{density.py,resolve.py,anchorcheck.py,mirror-containment-check.py,source-recheck.py,README.md}` + `instruments/citation-survival.{md,tsv}` | round-15: evidence-density census, live citation-resolvability census (instrument of record + definition + known limits), mirror anchor range/semantic gate; bar rule `BAR_R15 = 142.5` frozen + conjunctive ≥60 % resolvability gate from r16 |
| Lessons | `lessons/round-1.md` … `lessons/round-15.md` | `LOG.md` rounds, commits, `.ufo/reports/` |
| CVSS v4.0 severity and vector semantics | knowledge/cvss-v4-severity-and-vector.md | S001, S002 — public primary, opened 2026-10-19 |
| Coordinated-disclosure timelines | knowledge/coordinated-disclosure-timelines.md | S003, S004, S005 — public primary, opened 2026-10-19 |
| Authorization, safe harbor, and scope | knowledge/authorization-safe-harbor-and-scope.md | S006, S007, S008 — public primary, opened 2026-10-19 |
| AI-assisted finding validation | knowledge/ai-assisted-finding-validation.md | S009, S010, S011, S012 — public primary, opened 2026-10-19 |
| CWE Top 25 2025 methodology | knowledge/cwe-top25-2025-methodology.md | S013, S014, S015 — public primary, opened 2026-10-19 |
| Citation-base vocabulary (D6; previously unmapped) | knowledge/citation-bases.md | kaika W1 STATE dossier defect D6 (fleet-ledger .ufo/waves/kaika-w1/kasegi-state.md, outside this repo); existing corpus vocabulary |
| Admission bar + source registry | QUALITY.md, SOURCES.md | Round-22 admission and source-registry contract |
| Lessons (r22 correction) | lessons/round-1.md … lessons/round-22.md (25 files; gaps at 2, 16, 18, 19) | The old Lessons row understated coverage: current files include rounds 17, 20, 21, and 22. |
| Multi-party coordination (round 23) | knowledge/multiparty-vulnerability-coordination.md | S018 — public primary, opened 2026-10-20 |
| CNA assignment rules, current version (round 23) | knowledge/cna-assignment-and-vulnerability-rules.md | S031 (4.2.6, effective 2026-10-20) supersedes S030 — public primary, opened 2026-10-25 |
| CRA manufacturer reporting duties (round 23) | knowledge/cra-manufacturer-reporting-duties.md | S029 — public primary, opened 2026-10-20 |
| Engagement authorisation — rules of engagement (round 24) | knowledge/authorised-testing-rules-of-engagement.md | S032 — public primary (NIST SP 800-115), opened 2026-10-25 |
| Statutory definition of unauthorised access, Japan (round 24) | knowledge/statutory-authorization-and-unauthorized-access.md | S033 (e-Gov consolidated text) with S034/S035 as tier-B/commentary, opened 2026-10-25 |
| Vendor-side disclosure policies as corpus objects (round 25) | knowledge/vendor-disclosure-policies-as-corpus-objects.md | S036, S037, S038, S039 — four Japanese vendor pages captured 2026-10-25 |
| A vendor policy commits to a clock, not a scope (round 25) | knowledge/vendor-disclosure-policy-commitments-crosswalk.md | S040 (Cisco) crosswalked against S036/S038/S039 — captured 2026-10-25 |
## Known gaps

- **`~/Projects/bounties` is GONE** (removed 2026-09-28T23:51:31Z, actor
  UNDETERMINED, PRESUMED-LOST locally): the 18-surface coverage denominator is
  0/18 present, 704 genuine citations in `SKILL.md` + 765 lost-tree
  `path:line` cites across 21 `knowledge/*.md` files no longer resolve, and the
  DATA-half censuses (1088 records, 280 packages, 592 evidence dirs, 7227
  telemetry lines, 31 autopsies, the `.git` rebase state) can never be
  re-verified. Recorded round 15 in `knowledge/source-tree-loss-2026-09-28.md`;
  operator decision requested in `../../../.ufo/l0-questions.md` (reorg vs
  deletion, recoverability, PROVINCE re-point). Two surviving roots:
  `~/Projects/the-bounty-hunter` (frozen 2026-09-05 code mirror, censused r15)
  and `~/Projects/origin-work/open-bug-bounties` (**inventory only — the r16
  coverage move**) — both now ABSENT, see next bullet.
- **`~/Projects/the-bounty-hunter` + all of `~/Projects/origin-work` are also
  GONE** (absent since ~2026-10-12, detected 2026-10-14 re-census — the two
  "surviving roots" this map was re-based onto in round 15): every
  `the-bounty-hunter`/`open-bug-bounties`/`origin-work` path cited anywhere in
  this corpus is now a historical record — `[lost-base]` where anchored —
  unless the sentence re-anchors it to `~/Projects/ufo-fsd-alpha` (the one
  tree that relocated intact, HEAD `964f443e`). Evidence:
  `knowledge/root-loss-2026-10-12.md`; vocabulary: `knowledge/citation-bases.md`.
- Anchor bases are pinned per file, and only 1 of 21 `knowledge/*.md` entries
  (`triage-thresholds.md`, pinned to blob `fc6d398` for its `SKILL.md:NNN`
  cites) carries an explicit pin so far — pinning the other 20 is the r16
  `depth:verifiability` move.
- ~~ops tail (`validate`/`registry-check`/`reroute-drill`/`check-freshness`/
  `finalize-all`/sighting scripts + `shared.mjs` constants) name-only~~ —
  CLOSED round 7: `knowledge/ops-invariants.md` + `knowledge/intake-and-finalize.md`.

- ~~`ops/claim-check.mjs` gate list~~ — CLOSED round 1:
  `knowledge/claim-gates.md` holds the full extracted gate list.
- Cantina fee/precondition pattern: siblings sampled (dydx same blocker class;
  morpho/euler/uniswap/reserve honest-zero) — see `program-quirks.md`.
- ~~`vgn-bounty-lab/` unwalked~~ — CLOSED round 4: empty `git init`, zero
  commits, nothing to learn (`knowledge/evidence-dir.md` §adjacent dirs).
- ~~`evidence/` per-program vs `claims/*/evidence/` unexamined~~ — CLOSED
  round 4: `knowledge/evidence-dir.md` (592-dir census + record schemas).
- ~~`ledger/` writers/state machine undocumented~~ — CLOSED round 4:
  `knowledge/mission-ledger.md` (transition counts, telemetry event census,
  ops inventory).
- ~~`fleets/ufo-archive-2026/` unwalked~~ — CLOSED round 8:
  `knowledge/ufo-archive-2026.md` (19-mission defect taxonomy, b1k-NNN
  keeper origin, `claim-packages/`→`claims/` naming drift, reconciliation
  evidence chain).
- ~~`fleets/registry.json` lane→model routing — possibly cross-domain~~ — CLOSED round 11: `knowledge/intake-surface.md` (in-domain: `operator_decrees` is the authoritative decree ledger — claim queue order, 3cx never-filed, intel hold, freebie attribution flip — plus lane/bucket routing consumed by validate/registry-check).
- `george/` (49G comma.ai research dir) — parked round 4: no claim package
  references it; revisit only if one does.
- ~~No consolidated do-not-submit list~~ — CLOSED round 9:
  `knowledge/submitted-registry.md` (3 verified H1 + 3 archive-era live in
  origin-work tree + 3 probable orphans + 1 VDP; Anthropic claim↔VDP
  same-finding collision verified by live claim-check OK; origin-work
  corpus outside every scan; field-spelling + polarity traps; 15
  status-less stub dirs; root zips = dated snapshots).
- ~~`claim-hold/*` semantics + queued-row audit~~ — CLOSED round 10:
  `knowledge/operator-queue.md` (claim-index ignores hold tags → 3 held rows
  queued; anthropic row = own VDP disclosure, verified byte-identical;
  per-row residual-gate dossier).

- ~~`.ufo/bh*/` mission workspaces, `.ufo/sessions/`, `.ufo/bounty-fleet/`, and
  `grok-bounty-assessment-20260911` un-censused~~ — CLOSED round 12:
  `knowledge/ufo-workspaces.md` (25 bh workspaces incl. the 507 M foreign-tree
  outlier; warden producer + lifecycle; keeper tree with the second
  `missions.jsonl`; 8 bpolish seats, refile verdict NONE, 471-false-positive
  grep trap; frozen self-invalidating grok assessment; `.omp/` second routing
  truth; 656 claims files cite `.ufo/` paths, 51/543 refs already dangling).
- `pendle-core-v2-public/` (63 M vendored hunt target, never named in LOG) +
  the provenance-pin contract — CLOSED round 12:
  `knowledge/target-checkouts.md`.
- Repo git runtime state — CLOSED round 12: `knowledge/repo-git-state.md`
  (stalled mid-rebase since before 2026-09-11, `gitMutationBlocker` refuses
  all fleet commits, all Sep 7–15 work working-tree-only; escalated to L0 via
  `.ufo/l0-questions.md`).
- Round-12 citation audit (independent L2 reviewer: 74 citations checked —
  64 OK / 9 spot-mismatch / 1 broken) — all 10 repaired in place across
  SKILL.md + 5 corpus entries, each marked "round-12 correction/addition";
  two critic falsifications also repaired (claims denominator 275→274; bh
  audits "21 all BLOCKED"→22: 20 BLOCKED/2 READY).
- Round-13 depth audit (5 independent L2 auditors + L1 full-source
  derivation): full-set citation re-audit 705/708 counted citations resolved
  (99.6%; 3 broken repaired: `raw-rN/`→`raw/`, `B-bounty-fleet/` zip
  misattribution, dangling `ufo-fsd-alpha/.ufo/missions/hunt-*`); ~106
  attached-fact checks found ~30 defects — all repaired in place this round
  (markers "round-13 correction/addition"): reroute universals→distributions
  (23/121 non-grok causes, devin target 88/121), keeper run_ids 184→183 +
  unledgered 81→82 + "2 unparseable"→0, candidates 116→105 ids, sessions
  grep tallies (strict 9→4 files; naive 471/61→402/91; null-url ~51→56/61),
  `3d28a716` stamp→05:42:43-03:00, tracked claims 20→19 dirs, pendle 10→6
  top-level dirs, pin-family taxonomy→verified 187/188 census (157 bare hex,
  24 dicts, 3 nulls; no {cmd,exit} family), archive missions 19→20 (both
  regressed lines), queued-hold rows 3→4 (8x8 tag exists since 09-05),
  `submitted_url` route-URL claim→null on all 12 (routes live in
  submission_url/claim_url/payload), crypto severity critical→Low,
  superhuman lab-redaction gate nonexistent, openai-oauth→openai-codex peak
  model, 3→4 usage-limit signatures, `reward.min` 48→14 numeric + 1024
  (796+228) degenerate records + five-term score incl. `is_live(1)`,
  seeded-13 "without map records"→9/13 have records (4 map-less), rank.mjs
  "never ran"→ran ≥2× 09-04, bump never persisted, telemetry 7218→7225
  as-of-stamped + 3 committed conflict markers + rankings ~30→234/229,
  ev-report exit/basis/cutoff semantics, `claim_checklist.json`→`.md`,
  HARD_STOP double-error, symlink-ban + 5 MiB walk gates added.
- ~~Per-program claim anatomy is ~3.6% sampled (≈10 of 280 status-gated
  packages read line-by-line)~~ — ADVANCED round 14: +20 full reads via a
  deterministic stratified selection (script preserved + L1 re-run) →
  **30/280 = 10.7%** (`knowledge/claim-anatomy-sample.md`; D1-D13 deviation
  classes, 260/280 packages deviate from the canonical key set). The full
  100% census remains a future coverage sub-axis candidate — deliberate,
  not a gap-by-omission.
- `corpus/lessons/` has no round-2 record and LOG.md jumps round 1→round 3:
  a round-2 ledger hole from the lane's first day (round-2 work, if any,
  was folded into the round-3 entry). History is not rewritten; recorded
  round 13 so the absence is known-deliberate, not lost.
- `positive-blocked-*` verdict class: exactly 2 attested instances
  (cantina-pendle, cantina-dydx), free-form string, no schema definition,
  unrecognized by claim-check.mjs:169's not-claimable regex — annotated in
  SKILL.md round 13; it is a package-state convention, not a gate class.
- Round-14 depth audit (9 independent L2s: 3 scouts, 2 executors, critic,
  reviewer, connector, revenger + L1 full-source derivation): per-item
  citations landed for both thin sections (Program-rule checklist,
  Disclosure anti-patterns); 3 falsified SKILL claims repaired in place —
  "every fix is a disclosure defect" header (2 NO-GO rows are reproduction
  gates, `docs/wrap-report.md:9,:20-21`), the :412 receipt-drift pointers
  (4028846/a169f309 live in origin-work `submission-review/`, NOT in
  `portal-reconciliation-2026-09-11.json`/`final-audit.json`), Immunefi
  `policy_sha256` overreach (beanstalk provenance has zero hash keys;
  Immunefi page hashes land as `html_sha256` in keeper telemetry); 2 corpus
  defects repaired (state enum omitted PARKED 248/280; playbook seek-autopsy
  misattribution); vocabularies widened with census anchors
  (`provenance.json.pin` 4 shapes, `coverage.status` second value, verdict
  suffixes `-identity`×121 / `-host-binding`×69, decree git timeline
  b3b1b7e3→2ef530c6). Markers "round-14 correction/addition". One critic
  falsification REJECTED with evidence (the 2026-09-05 severity decree
  exists at `[lost-tree] fleets/claimer-mission.md:29` — critic grepped only `docs/`).

## Interactive cutover evidence — round 21

| Entry | Evidence status |
|---|---|
| `lessons/round-17-mirror-relocation.md` | Inherited interrupted-worker record; preserved verbatim. Round-number and mutable-filesystem guard corrections are in the new round-21 entry, not rewritten into this historical lesson. |
| `lessons/round-21-routing-blocked.md` | Routing-blocked authority audit, zero verified-round credit; inherited CLI behavior re-executed, failed 32/506 replays preserved, Git-export versus live-filesystem definitions separated. |

No new domain knowledge is admitted by this index addition. The required
quality bar `corpus/QUALITY.md` is absent; it remains conformance debt.

Correction (2026-10-19): corpus/QUALITY.md now exists; the preceding closing paragraph records the earlier state and is retained as history.

## Frontier

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F01 | CVSS v4.0 severity and vector semantics | admitted | knowledge/cvss-v4-severity-and-vector.md | S001, S002 | Keep scores distinct from program-specific risk and policy. |
| F02 | Coordinated-disclosure timelines | admitted | knowledge/coordinated-disclosure-timelines.md | S003, S004, S005 | Compare stated timelines while preserving each source's attribution. |
| F03 | Authorization, safe harbor, and scope | admitted | knowledge/authorization-safe-harbor-and-scope.md | S006, S007, S008 | Attribute protections to the policy that grants them; do not generalize. |
| F04 | AI-assisted finding validation | admitted | knowledge/ai-assisted-finding-validation.md | S009, S010, S011, S012 | Preserve independent validation and source-specific limitations. |
| F05 | CWE Top 25 2025 methodology | admitted | knowledge/cwe-top25-2025-methodology.md | S013, S014, S015 | Treat the ranking as a methodology-specific prioritization, not a universal risk order. |
| F06 | Multi-party CVD — FIRST guidelines v1.1 | admitted | knowledge/multiparty-vulnerability-coordination.md | S018 | Record each party's role and relationship; an upstream fix is not downstream evidence. |
| F07 | CVE CNA operational rules | admitted | knowledge/cna-assignment-and-vulnerability-rules.md | S031 | Separate technical impact, assignment scope and identifier count; do not reuse 4.1.0 section numbers. |
| F08 | EU Cyber Resilience Act reporting duties | admitted | knowledge/cra-manufacturer-reporting-duties.md | S029 | Distinguish manufacturer statutory tracks from researcher disclosure; Article 14 applies from 2026-09-11. |
| F09 | Authorisation outside the platform: the engagement document and the statute | admitted | knowledge/authorised-testing-rules-of-engagement.md, knowledge/statutory-authorization-and-unauthorized-access.md | S032, S033, S034, S035 | A safe-harbour badge is not the grant and not the legal definition: read the ROE's scope/exclude list, and the access manager the statute requires. |
| F10 | Vendor-side disclosure policies as corpus objects | admitted | knowledge/vendor-disclosure-policies-as-corpus-objects.md, knowledge/vendor-disclosure-policy-commitments-crosswalk.md | S036, S037, S038, S039, S040 | A vendor's published policy is a standing first-party statement, not a programme: read its intake channels, its handling-versus-disclosure scope, the standard edition it names, and the conditions (and count of conditions) under which it goes faster. |
| F11 | ISO/IEC 29147/30111 division-of-labour meta | admitted | knowledge/iso-29147-and-30111-division-of-labour.md, knowledge/iso-29147-divergence-and-clause-crosswalk.md | S041 | Treat 29147 as the vendor's outward-facing disclosure standard and 30111 as its internal handling process; record the edition a source names (JPCERT/CC compares against 2014, Cisco claims 2018). |
| F12 | Japanese state-coordinated disclosure workflow | admitted | knowledge/japanese-domestic-disclosure-workflow.md | S041, S042 | Use 起算日 — the day the guideline's Ⅳ.4.2) notification was first attempted (S041 footnote 4), not an acknowledgement or a submission date — as the Japanese column when comparing coordinator timelines against F02. The same 45-day figure is triggered differently on each side: S041's publication date is a 目安 of 45 days from 起算日 (Ⅳ.3)), CERT/CC's 45 days runs from the initial report (S004, F02). |

The original domain-root map is exhausted: 0/18 surfaces are present.
That sentence describes the lost `/home/vgpnk/Projects/bounties` surface set only; the
public-practice frontier above is a separate denominator (11/11 admitted at round 26; F01-F08 at
round 23, F09 at round 24, F10 at round 25, F11 at round 26) and is not counted into the 0/18 figure.

[r28 amendment, appended 2026-10-25] The parenthetical above records the round-26 frontier state and is
retained as history, not rewritten (R9): at round 28 the frontier stands at **12/12 admitted** —
F01-F08 at round 23, F09 at round 24, F10 at round 25, F11 at round 26, F12 at round 28. The 0/18
sentence is untouched: the lost-domain denominator still holds 0 of 18 surfaces present, and the
frontier count stays outside it.

## Round-28 reconciliation — coverage map and expected list (appended 2026-10-25)

The coverage map above is not edited in place: the round-28 entry
`knowledge/japanese-domestic-disclosure-workflow.md` (Frontier F12, sources S041 + S042; source
basis: the JPCERT/CC 2026 早期警戒パートナーシップガイドライン re-captured this round plus the new
IPA 脆弱性関連情報の届出受付業務における取扱いプロセス row S042, both captured 2026-10-25 under
`corpus/source-snapshots/round-28/`) is recorded here as an appended amendment so every existing
line keeps its number (R6). Its count basis is not this index: `corpus/instruments/recheck-audit.py`
compares the tree against the committed `corpus/instruments/knowledge-expected.txt`, which at
round-28 start held **41 lines = 39 entries + 2 comment lines** (measured 2026-10-25:
`wc -l` → 41, `grep -vc '^#'` → 39 — the same 41-versus-39 basis the round-27 lesson named), so the
list must become 40 entries / 42 lines in the same round the entry lands or the audit reports the
new file as `unexpected=`. That basis is confirmed by the round-28 wave receipt
`.ufo/waves/round-28/receipts/ExecExpectedList.txt` (the same 41 = 39 entries + 2 comments
reconciliation, measured before the entry landed; the receipt reports no production edits, so the
list was not regenerated). Once the round-28 entry landed the audit duly printed
`expect=present expected=39 missing=0 unexpected=1 exit=1`; regenerating the list to 40 entries /
42 lines clears it. Re-verify with
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py`
(the run prints `expected=<n> missing=<n> unexpected=<n> exit=<n>`).

## Round-29 admission — coverage map row and Frontier F13 (appended 2026-10-25)

The coverage map above is not edited in place (R6): the round-29 entry
`knowledge/program-severity-ladders-and-reward-scales.md` (Frontier F13, sources S043 +
S044 + S045; source basis: the HackerOne standard program policy set, the Bugcrowd VRT
README and the Bugcrowd VRT CWE crosswalk, all captured 2026-10-25 under
`corpus/source-snapshots/round-29/`) is recorded here as an appended amendment so every
existing line keeps its number. The coverage-map row is appended here rather than inserted
into the map, and the F13 frontier row is listed here on the same table shape as the
frontier above.

| Area | Entry | Source basis |
|---|---|---|
| Program severity ladders and reward scales (round 29) | `knowledge/program-severity-ladders-and-reward-scales.md` | S043, S044, S045 — public primary, opened 2026-10-25 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F13 | Program severity ladders and reward scales | admitted | knowledge/program-severity-ladders-and-reward-scales.md | S043, S044, S045 | Keep each platform's ladder as its own suggested baseline — distinct from CVSS-B and from other programs' reward ceilings; do not generalize a payout scale across programs. |

## Round-30 admission — coverage map row and Frontier F14 (appended 2026-10-25)

The coverage map above is not edited in place (R6): the round-30 entry
`knowledge/japanese-severity-vocabulary-and-impact-model.md` (Frontier F14, sources S046 +
S047 + S041; source basis: the IPA JVN activity report PDF and the IPA JVN quarterly
registration report, both first registered this round, plus the already-registered
JPCERT/CC 2026 guideline S041, all captured 2026-10-25 under
`corpus/source-snapshots/round-30/`) is recorded here as an appended amendment so every
existing line keeps its number. The coverage-map row is appended here rather than inserted
into the map, and the F14 frontier row is listed here on the same table shape as the
frontier above.

| Area | Entry | Source basis |
|---|---|---|
| Japanese severity vocabulary and handling-priority model (round 30) | `knowledge/japanese-severity-vocabulary-and-impact-model.md` | S046, S047 (S041) — public primary, opened 2026-10-25 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F14 | Japanese severity vocabulary and the handling-priority model | admitted | knowledge/japanese-severity-vocabulary-and-impact-model.md | S046, S047, S041 | Keep each 深刻度 band label attached to the CVSS version that produced it (v2 bands survive beside v3); JVN translates CVSS base scores into Japanese vocabulary rather than scoring independently, so derive handling priority from the P-guideline steps, not from the label alone. |

[r30 amendment, appended 2026-10-25] The parenthetical above records the round-26 frontier
state and is retained as history, not rewritten (R9): at round 30 the frontier stands at
**14/14 admitted** — F01-F08 at round 23, F09 at round 24, F10 at round 25, F11 at round
26, F12 at round 28, F13 at round 29, F14 at round 30. The 0/18 sentence is untouched: the
lost-domain denominator still holds 0 of 18 surfaces present, and the frontier count stays
outside it.

## Round-31 admission — coverage map row and Frontier F15 (appended 2026-10-25)

The coverage map above is not edited in place (R6): the round-31 entry
`knowledge/vendor-third-party-finding-coordination.md` (Frontier F15, source S048; source
basis: the Microsoft Security Response Center's own Microsoft Security Vulnerability
Research (MSVR) page, captured 2026-10-25 under `corpus/source-snapshots/round-31/`) is
recorded here as an appended amendment so every existing line keeps its number. The
coverage-map row is appended here rather than inserted into the map, and the F15 frontier
row is listed here on the same table shape as the frontier above.

| Area | Entry | Source basis |
|---|---|---|
| A vendor's research programme as an intake route for other vendors' bugs (round 31) | knowledge/vendor-third-party-finding-coordination.md | S048 — public primary, opened 2026-10-25 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F15 | A vendor's research programme as an intake route for other vendors' bugs | admitted | knowledge/vendor-third-party-finding-coordination.md | S048 | Record which party coordinates a multi-vendor finding — the vendor itself, as S048's three intake routes and self-named coordinator role state, or an external centre, as F10's S039/S040 rows route it — and read no clock, contact or agreement into an intake route: the pinned capture states none. |

[r31 amendment, appended 2026-10-25] The parenthetical above records the round-26 frontier
state and is retained as history, not rewritten (R9): at round 31 the frontier stands at
**15/15 admitted** — F01-F08 at round 23, F09 at round 24, F10 at round 25, F11 at round
26, F12 at round 28, F13 at round 29, F14 at round 30, F15 at round 31. The 0/18 sentence
is untouched: the lost-domain denominator still holds 0 of 18 surfaces present, and the
frontier count stays outside it.

## Round-33 admission — coverage map row and Frontier F16 (appended 2026-10-26)

The coverage map above is not edited in place (R6): the round-33 entry
`knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` (Frontier F16, sources S049 + S050;
source basis: the CNVD 众测 platform's 使用手册 at https://zc.cnvd.org.cn/news/helpList and
360SRC's 外部漏洞处理和评分标准 V2.0 at https://security.360.cn/Reward/rules, both captured
2026-10-25 under `corpus/source-snapshots/round-32/`) is recorded here as an appended amendment so
every existing line keeps its number. The coverage-map row is appended here rather than inserted
into the map, and the F16 frontier row is listed here on the same table shape as the frontier
above.

| Area | Entry | Source basis |
|---|---|---|
| Chinese crowdsourced-testing platform scope and reward rules (round 33) | knowledge/chinese-crowdsourced-testing-scope-and-rewards.md | S049, S050 — public primary, opened 2026-10-26 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F16 | Chinese crowdsourced-testing platform scope and reward rules (CNVD 众测, 360SRC) | admitted | knowledge/chinese-crowdsourced-testing-scope-and-rewards.md | S049, S050 | Read a reward only from the platform that prints it — CNVD 众测 publishes no per-severity money table, since the enterprise's rating and the project's rules set the payout (S049.txt:419), while 360SRC pays its business-coefficient formula over base 安全币 (S050.txt:112, 129) — and read neither as scope or authorization: 360SRC's enumerating asset list is a separate page S050 names but this capture does not contain (S050.txt:71), and CNVD 众测 intake is the customer's per-project authorization, not the submission page's target list (S049.txt:211-214). |

[r33 amendment, appended 2026-10-26] The parenthetical above records the round-26 frontier state
and each later amendment paragraph states its own round; those are retained as history, not
rewritten (R9): at round 33 the frontier stands at **16/16 admitted** — F01-F08 at round 23, F09
at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30,
F15 at round 31, F16 at round 33. The 0/18 sentence is untouched: the lost-domain denominator
still holds 0 of 18 surfaces present, and the frontier count stays outside it.

## Round-34 admission — coverage map row and Frontier F17 (appended 2026-10-26)

The coverage map above is not edited in place (R6): the round-34 entry
`knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` (Frontier F17, source S051; source basis:
Immunefi's own Vulnerability Severity Classification System v2.2 at
https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/, captured
2026-10-26 under `corpus/source-snapshots/round-34/`) is recorded here as an appended amendment so
every existing line keeps its number. The coverage-map row is appended here rather than inserted
into the map, and the F17 frontier row is listed here on the same table shape as the frontier
above.

| Area | Entry | Source basis |
|---|---|---|
| Web3/smart-contract bounty severity classification (round 34) | knowledge/immunefi-vscs-v2-2-smart-contract-severity.md | S051 — public primary, opened 2026-10-26 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F17 | Immunefi Vulnerability Severity Classification System v2.2 — Web3/smart-contract bounty severity classification | admitted | knowledge/immunefi-vscs-v2-2-smart-contract-severity.md | S051 | Read a level from Immunefi's own per-asset-class table: the five numbered levels rank impacts inside one scope table, the level is fixed largely by impact — "finalizes them largely by the impact that they cause" (S051.txt:52) — under a downgrade-or-reject carve-out for elevated privileges or uncommon user interaction (S051.txt:55-56), and the funds boundary is whose funds and for how long they stay frozen: theft of any user funds is Critical (S051.txt:75) while "Temporary freezing of funds" is High (S051.txt:88). The page carries no CVSS mapping, no reward figure and no version-selection rule (FC-2/FC-3/FC-4), so neither a payout nor portability across asset classes follows from a level. |

[r34 amendment, appended 2026-10-26] The parenthetical above records the round-26 frontier state
and each later amendment paragraph states its own round; those are retained as history, not
rewritten (R9): at round 34 the frontier stands at **17/17 admitted** — F01-F08 at round 23, F09
at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30,
F15 at round 31, F16 at round 33, F17 at round 34. The 0/18 sentence is untouched: the lost-domain
denominator still holds 0 of 18 surfaces present, and the frontier count stays outside it.

## Round-35 admission — coverage map row and Frontier F18 (appended 2026-10-26)

The coverage map above is not edited in place (R6): the round-35 entry
`knowledge/cisa-kev-catalog.md` (Frontier F18, source S052; source basis:
CISA's Known Exploited Vulnerabilities JSON feed at
https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
(catalogVersion 2026.10.23, count 1756), captured 2026-10-26 under
`corpus/source-snapshots/round-35/`) is recorded here as an appended amendment so
every existing line keeps its number. The coverage-map row is appended here rather than inserted
into the map, and the F18 frontier row is listed here on the same table shape as the frontier
above.

| Area | Entry | Source basis |
|---|---|---|
| Known-exploited-vulnerabilities prioritization (round 35) | knowledge/cisa-kev-catalog.md | S052 — public primary dataset, opened 2026-10-26 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F18 | CISA Known Exploited Vulnerabilities catalog — exploitation-status-based prioritization distinct from CVSS severity | admitted | knowledge/cisa-kev-catalog.md | S052 | Keep the catalog's remediation clock attached to the directive that binds it: BOD 26-04 supersedes the revoked BOD 22-01 and uses KEV status as one of four risk-priority factors (public exposure, KEV status, automatability, technical impact), with 3-day remediation for the most urgent cases; KEV listing is an exploitation-status signal, not a severity score — the feed carries no severity field (12 keys x 1756 records, cvss 0). |
| F19 | FIRST EPSS exploitation-likelihood scoring | admitted | knowledge/epss-exploit-prediction-scoring.md | S053 | EPSS estimates the probability that a published CVE will be exploited in the wild in the next 30 days; treat it as a likelihood signal distinct from CVSS severity and KEV catalog status |

[r35 amendment, appended 2026-10-26] The parenthetical above records the round-26 frontier state
and each later amendment paragraph states its own round; those are retained as history, not
rewritten (R9): at round 35 the frontier stands at **18/18 admitted** — F01-F08 at round 23, F09
at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30,
F15 at round 31, F16 at round 33, F17 at round 34, F18 at round 35. The 0/18 sentence is
untouched: the lost-domain denominator still holds 0 of 18 surfaces present, and the frontier count
stays outside it.



The coverage map above is not edited in place (R6): the round-37 entry
`knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` (Frontier F20, source S054;
source basis: CERT/CC's SSVC "What is SSVC?" overview tutorial at
https://certcc.github.io/SSVC/tutorials/ssvc_overview/ — the overview page, not the docs home, per
`claims-erratum-1.md` and capture-binding rule B5 — captured 2026-10-26, status 200, under
`corpus/source-snapshots/round-37/`) is recorded here as an appended amendment so every existing
line keeps its number. The coverage-map row is appended here rather than inserted into the map, and
the F20 frontier row is listed here on the same table shape as the frontier above.

| Area | Entry | Source basis |
|---|---|---|
| Stakeholder-specific vulnerability categorization (round 37) | knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md | S054 — public primary, opened 2026-10-26 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F20 | SSVC (Stakeholder-Specific Vulnerability Categorization) — stakeholder-tailored, decision-point-based prioritization | admitted | knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md | S054 | Read a priority from one stakeholder's decision model, not a universal score: "A decision point itself is not representative of risk, but the series of decisions point values help a stakeholder determine how risky a vulnerability is" (S054.txt:277; the page's own typo "decisions point values" is quoted verbatim), and the inputs are per-system — Exposure asks how difficult it is for an attacker to access a system from the open Internet (S054.txt:367). Keep it distinct from CVSS severity, KEV status and EPSS likelihood: SSVC categorizes "by priority based on risk that varies among stakeholders" (S054.txt:259), and the page contrasts itself with systems that "rate on technical severity" (S054.txt:247) while naming no CVSS metric and defining neither severity nor exploitability in prose — CVSS, EPSS and KEV appear only in site navigation, so source those definitions from S001/S002, S052 and S053. Read "Carnegie Mellon" only as the site footer's owner statement, not as a methodology claim. |

[r37 amendment, appended 2026-10-26] The parenthetical above records the round-26 frontier state
and each later amendment paragraph states its own round; those are retained as history, not
rewritten (R9): at round 37 the frontier stands at **20/20 admitted** — F01-F08 at round 23, F09
at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30,
F15 at round 31, F16 at round 33, F17 at round 34, F18 at round 35, F19 at round 36, F20 at
round 37. The 0/18 sentence is untouched: the lost-domain denominator still holds 0 of 18
surfaces present, and the frontier count stays outside it.

```

| property | value |
|---|---|
| sha256 (block bytes) | `2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b` |
| bytes / lines | 2947 / 27 |
| row shape | six cells (id, topic, status, entry, sources, next), topic names SSVC as stakeholder-tailored decision-point prioritization, entry path `knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`, source `S054` |
| count line | `[r37 amendment, appended 2026-10-26]` naming `20/20 admitted` and F01-F08 r23, F09 r24, F10 r25, F11 r26, F12 r28, F13 r29, F14 r30, F15 r31, F16 r33, F17 r34, F18 r35, F19 r36, F20 r37; the 0/18 sentence is declared untouched |
| URL choice | overview tutorial page per `claims-erratum-1.md`; the paragraph says so and why (capture-binding B5) |

## 4. Validation on a scratch mirror (append, not edit)

Fixture: `git archive HEAD PROVINCE.md corpus` exported into
`/fast/scratch/hyaku/kasegi-r37/ScribeFrontierAmendments/mirror`, both blocks appended with Python to the
copies only. Measured on that mirror:

| check | command | observed |
|---|---|---|
| pure addition (PROVINCE) | `diff orig PROVINCE.md \| grep -c '^<'` | `0` (2 added lines) |
| pure addition (README) | `diff orig corpus/README.md \| grep -c '^<'` | `0` (27 added lines) |
| frontier row count | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `20` (target `20`) |
| row cells | pipe-split of the F20 line | 6 cells; next cell 155 words |
| section header | `grep -c '^## Round-37 admission' corpus/README.md` | `1` |
| count line | `grep -c 'frontier stands at \*\*20/20 admitted\*\*' corpus/README.md` | `1` |
| PROVINCE line | `grep -c '^\[r37 Frontier amendment' PROVINCE.md` | `1` |
| sizes | `wc -l` on the mirror | `PROVINCE.md` 80, `corpus/README.md` 425 |

Harness on the same mirror (`HYAKU_SCRATCH=<scratch> python3 corpus/instruments/frontier-recheck-count.py
--root <mirror>`, tail):
```

Correction (round 38): corpus/README.md L399-L454 — the whole round-37 append — carry misplaced receipt scaffolding copied from `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md`: receipt property and validation tables, a "Validation on a scratch mirror" section with its check table, and a stray fence at L426 that leaves the rest of the file inside a code block; the intended round-37 block was 27 lines (sha256 2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b, the bytes of that receipt's §3 "Deliverable B — `corpus/README.md` end-of-file block"), of which only L400-L425 landed unchanged — L399 is a blank line where the block's `## Round-37 admission — coverage map row and Frontier F20 (appended 2026-10-26)` heading belonged; the fence opened at L426 is closed by this block, whose first line is the closing fence, and L426-L454 are to be read as not part of the corpus index.

## Round-38 admission — coverage map row and Frontier F21 (appended 2026-10-26)

The coverage map above is not edited in place (R6): the round-38 entry
`knowledge/csaf-vex-product-status-and-justifications.md` (Frontier F21, source S055;
source basis: the OASIS CSAF TC's own normative text, the CSAF 2.0 OASIS Standard at
https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html — the standard document itself, not
a summary page or the TC's home — captured 2026-10-26T18:25:51Z, HTTP status 200, 272441 bytes /
5146 lines, sha256 63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42, under
`corpus/source-snapshots/round-38/`) is recorded here as an appended amendment so every existing
line keeps its number. The coverage-map row is appended here rather than inserted into the map, and
the F21 frontier row is listed here on the same table shape as the frontier above.

| Area | Entry | Source basis |
|---|---|---|
| VEX product-status categories and not-affected justification flags (round 38) | knowledge/csaf-vex-product-status-and-justifications.md | S055 — public primary, opened 2026-10-26 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F21 | OASIS CSAF v2.0 (Common Security Advisory Framework) — VEX product-status categories and machine-readable not-affected justification flags | admitted | knowledge/csaf-vex-product-status-and-justifications.md | S055 | Read a product's affect status from the vendor's own VEX block, not a severity score: "The main purpose of the VEX format is to state that and why a certain product is, or is not, affected by a vulnerability" (S055.txt:2135), and every vulnerability item MUST carry at least one of fixed, known_affected, known_not_affected or under_investigation in product_status (S055.txt:2844). known_not_affected is not a bare label — "an impact statement SHALL exist as machine readable flag" (S055.txt:2152) drawn from the labels that "reflect the VEX not affected justifications" (S055.txt:1762), such as vulnerable_code_not_in_execute_path, "The affected code is not reachable through the execution of the code, including non-anticipated states of the product." (S055.txt:1767). Keep it distinct from CVSS severity, KEV status, EPSS likelihood and SSVC decisions: CSAF states whether the vendor's own product is affected and why, not how severe the vulnerability is or how likely its exploitation is — this capture defines no severity scale. |

[r38 amendment, appended 2026-10-26] The parenthetical above records the round-26 frontier state
and each later amendment paragraph states its own round; those are retained as history, not
rewritten (R9): at round 38 the frontier stands at **21/21 admitted** — F01-F08 at round 23, F09
at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30,
F15 at round 31, F16 at round 33, F17 at round 34, F18 at round 35, F19 at round 36, F20 at round
37, F21 at round 38. The 0/18 sentence is untouched: the lost-domain denominator still holds 0 of 18
surfaces present, and the frontier count stays outside it.


## Round-39 admission — coverage map row and Frontier F22 (appended 2026-10-26)

The coverage map above is not edited in place (R6): the round-39 entry
`knowledge/cisa-when-to-issue-vex.md` (Frontier F22, source S057; source basis: CISA's own
"When to Issue VEX Information" page at
https://www.cisa.gov/resources-tools/resources/when-issue-vex-information — the issuance,
lifecycle, timestamp-reaffirmation and upstream-inheritance guidance that sits beyond the CSAF
VEX document-content profile — captured 2026-10-26 under `corpus/source-snapshots/round-39/`) is
recorded here as an appended amendment so every existing line keeps its number. The coverage-map
row is appended here rather than inserted into the map, and the F22 frontier row is listed here
on the same table shape as the frontier above.

| Area | Entry | Source basis |
|---|---|---|
| VEX issuance and lifecycle guidance (round 39) | knowledge/cisa-when-to-issue-vex.md | S057 — public primary, opened 2026-10-26 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F22 | VEX issuance, lifecycle and inheritance guidance (CISA When to Issue VEX Information) | admitted | knowledge/cisa-when-to-issue-vex.md | S057 | Keep the issuance layer distinct from the CSAF VEX document-content standard; a status update or reaffirmation is a new VEX statement, not a rewrite; upstream not_affected inheritance is conditional. |

[r39 amendment, appended 2026-10-26] The parenthetical above records the round-26 frontier state
and each later amendment paragraph states its own round; those are retained as history, not
rewritten (R9): at round 39 the frontier stands at **22/22 admitted** — F01-F08 at round 23, F09
at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30,
F15 at round 31, F16 at round 33, F17 at round 34, F18 at round 35, F19 at round 36, F20 at round
37, F21 at round 38, F22 at round 39. The 0/18 sentence is untouched: the lost-domain denominator
still holds 0 of 18 surfaces present, and the frontier count stays outside it.


## Round-40 admission — coverage map row and Frontier F23 (appended 2026-10-26)

The coverage map above is not edited in place (R6): the round-40 entry
`knowledge/cyclonedx-analysis-subtree.md` (Frontier F23, source S060; source basis: the CycloneDX
v1.7 JSON reference's `vulnerabilities[].analysis` subtree at https://cyclonedx.org/docs/1.7/json/ —
the `analysis.state`, `analysis.justification` and `analysis.response` fields that record an
analyst's decision about a vulnerability — captured 2026-10-26 under `corpus/source-snapshots/round-40/`)
is recorded here as an appended amendment so every existing line keeps its number. The coverage-map
row is appended here rather than inserted into the map, and the F23 frontier row is listed here
on the same table shape as the frontier above.

| Area | Entry | Source basis |
|---|---|---|
| Vulnerability analysis decisions in a CycloneDX BOM (round 40) | knowledge/cyclonedx-analysis-subtree.md | S060 — public primary, opened 2026-10-26 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F23 | CycloneDX v1.7 `vulnerabilities[].analysis` — the analyst-decision record (six states, nine justifications, five responses) beyond CSAF/VEX product status | admitted | knowledge/cyclonedx-analysis-subtree.md | S060 | Read an analyst decision from the BOM's own `analysis` object, not from a product-status block: `state` is one scalar of six values — "Declares the current state of an occurrence of a vulnerability, after automated or manual analysis." (S060.txt:L7) — and `false_positive` (S060.txt:L14) has no CSAF `product_status` twin; `justification` is one of nine reasons whose rule is only "Justification should be specified for all not_affected cases." (S060.txt:L15), weaker than S055's flag SHALL (S055.txt:L2151-L2152); `response` is a repeatable intention (S060.txt:L32), not a status change; and a version entry that omits its status defaults to `affected` (S060.txt:L105). None of this is an issuance or inheritance rule — that layer is S057's. |

[r40 amendment, appended 2026-10-26] The parenthetical above records the round-26 frontier state
and each later amendment paragraph states its own round; those are retained as history, not
rewritten (R9): at round 40 the frontier stands at **23/23 admitted** — F01-F08 at round 23, F09
at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30,
F15 at round 31, F16 at round 33, F17 at round 34, F18 at round 35, F19 at round 36, F20 at round
37, F21 at round 38, F22 at round 39, F23 at round 40. The 0/18 sentence is untouched: the
lost-domain denominator still holds 0 of 18 surfaces present, and the frontier count stays
outside it.

## Round-41 admission — coverage map row and Frontier F24 (appended 2026-10-27)

The coverage map above is not edited in place (R6): the round-41 entry
`knowledge/rfc-9116-security-txt.md` (Frontier F24, source S063; source basis: RFC 9116 "A File
Format to Aid in Security Vulnerability Disclosure" at https://www.rfc-editor.org/rfc/rfc9116.txt —
the machine-readable disclosure-channel discovery format, its `/.well-known/` location rule, its
eight defined fields with Contact and Expires the only REQUIRED ones and its Expires staleness
clock — captured 2026-10-27 under `corpus/source-snapshots/round-41/`) is recorded here as an
appended amendment so every existing line keeps its number. The coverage-map row is appended here
rather than inserted into the map, and the F24 frontier row is listed here on the same table shape
as the frontier above.

| Area | Entry | Source basis |
|---|---|---|
| Machine-readable disclosure-channel discovery via security.txt (round 41) | knowledge/rfc-9116-security-txt.md | S063 — public primary, opened 2026-10-27 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F24 | RFC 9116 security.txt — the machine-readable disclosure-channel discovery file (one well-known path, two REQUIRED fields, an Expires staleness clock) | admitted | knowledge/rfc-9116-security-txt.md | S063 | Read the channel from the file the target publishes rather than from a guessed page: the location is fixed at `/.well-known/security.txt` (§3), the default a reader starts from is "Unless otherwise stated, all fields MUST be considered optional." (§2.5) with Contact and Expires the two exceptions (§2.5.3, §2.5.5), the file dates itself — "This field MUST always be present and MUST NOT appear more than once." (§2.5.5) — with a sub-year horizon that is only "It is RECOMMENDED that the value of this field be less than a year into the future to avoid staleness." (§2.5.5), so an Expires instant in the past marks the whole file stale and a file whose presence or absence is read as permission has been misread (§5.5). |

[r41 amendment, appended 2026-10-27] The parenthetical above records the round-26 frontier state
and each later amendment paragraph states its own round; those are retained as history, not
rewritten (R9): at round 41 the frontier stands at **24/24 admitted** — F01-F08 at round 23, F09
at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30,
F15 at round 31, F16 at round 33, F17 at round 34, F18 at round 35, F19 at round 36, F20 at round
37, F21 at round 38, F22 at round 39, F23 at round 40, F24 at round 41. The 0/18 sentence is
untouched: the lost-domain denominator still holds 0 of 18 surfaces present, and the frontier
count stays outside it.

