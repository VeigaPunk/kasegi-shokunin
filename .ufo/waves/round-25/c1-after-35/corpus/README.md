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

The original domain-root map is exhausted: 0/18 surfaces are present.
That sentence describes the lost `/home/vgpnk/Projects/bounties` surface set only; the
public-practice frontier above is a separate denominator (10/10 admitted at round 25; F01-F08 at
round 23, F09 at round 24, F10 at round 25) and is not counted into the 0/18 figure.
