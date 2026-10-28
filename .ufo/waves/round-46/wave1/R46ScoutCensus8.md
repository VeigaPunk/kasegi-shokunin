VERDICT: INFO

# R46ScoutCensus8 — C1 re-groundability census (read-only)

Item: for each of the three gated knowledge entries `ufo-archive-2026.md`,
`ufo-workspaces.md`, `vdp-disclosure-packages.md`, list CURRENT claims, search the
committed lane bytes for support, record `claim | anchor path:N[-M] | token | verified
with sed -n`, classify `full`/`partial`/`none` (r46-c1-gate.py bar: >=6 anchored
claims over >=2 files), and say which current claims are really only historical
records. No lane bytes were edited; the only lane write is this Report file.

## 0. Ground truth of the bytes cited

- Freeze commit exists and is the claims freeze:
  `git log -1 --format='%H %s' 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5` →
  `9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5 round-46: freeze claims C1/C2, counters, controls, S073 capture`.
- `git status --porcelain` shows exactly 4 dirty paths, all under
  `.ufo/waves/round-46/` (L1 integration area) — none of my cited files is dirty.
- sha256 worktree vs `git show 9f23aab…:$f` for the five headline files — all SAME:
  ```
  SAME corpus/knowledge/ufo-archive-2026.md        wt=3297f5442107 freeze=3297f5442107
  SAME corpus/knowledge/ufo-workspaces.md          wt=b412a1619a5f freeze=b412a1619a5f
  SAME corpus/knowledge/vdp-disclosure-packages.md wt=b2fc8c726b79 freeze=b2fc8c726b79
  SAME corpus/instruments/r46-c1-gate.py           wt=b0c730c834b4 freeze=b0c730c834b4
  SAME SKILL.md                                    wt=a7c4d818300d freeze=a7c4d818300d
  ```
- HEAD has moved past the freeze (`git rev-parse HEAD` → `323d1f5d825a61cfd0dbf93f9580e092ee21c72a`),
  but `git diff --stat 9f23aab… -- corpus SKILL.md | wc -l` → `0`: every `corpus/` and
  `SKILL.md` line number below is simultaneously a worktree, HEAD and freeze-commit
  line number.
- Recheck lines pinned: `ufo-archive-2026.md:210`, `ufo-workspaces.md:376`,
  `vdp-disclosure-packages.md:37` (each `test -d ~/Projects/bounties && python3
  corpus/instruments/anchorcheck.py …` — gated, verified by sed -n on :205-210 /
  :370-376 / :33-37).

## 1. Frozen counter re-run (attack on the frozen C1 reading)

Command (read-only; TMPDIR pointed at my scratch):
`TMPDIR=$SCRATCH/tmp python3 corpus/instruments/r46-c1-gate.py --root <lane> --baseline /fast/scratch/hyaku/kasegi-r46/L1/pure`

Output (quoted):
```
gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64
gate L2 pass=0 read=base-gated=24 regrounded=0
gate L3 pass=0 read=recheck-lines-clean=0
gate L4 pass=0 read=entry-mode-green=0
gate L5 pass=0 read=append-only=0
gate L6 pass=0 read=mutants=0 survivors=none
gate L7 pass=1 read=still-gated=24 changed=none
c1-gate fixed=1/7 exit=1
counter_exit=1
```
This reproduces claims.json `expect_before`/`freeze_tree_reading` (`c1-gate fixed=1/7
exit=1`) and the C1 before-facts `executes/gated` split (gated=24, broken=0, lines
64/64). The do-nothing freeze tree does NOT pass: only the trivially-true L7 holds.

The bar (r46-c1-gate.py docstring + code, verified): re-ground section
`## Re-ground (round 46)` once; rows `| G<n> | claim | \`path:N[-M]\` | \`token\` |`;
anchor must be a regular file under `corpus/instruments/` or
`corpus/source-snapshots/` (never the entry itself), range <=40 lines, token >=6
chars whitespace-normalized inside those lines, >=6 rows with unique ids over >=2
distinct anchor files.

## 2. Entry `ufo-archive-2026.md` (210 lines)

entry	claim	anchor	token	verified
ufo-archive-2026	snapshot = 20 `claim-*` L1 hardening missions (round-13-corrected count)	corpus/README.md:23	20 `claim-*` report.json defect censuses	sed -n '23{=;p}' corpus/README.md — line 23 prints `… full walk: 20 `claim-*` report.json defect censuses (round-12 correction), keeper/whipper (b1k-NNN origin), inquiries briefs, programs/ old evidence shape`
ufo-archive-2026	the taxonomy is the empirical superset of `claim-check.mjs`	SKILL.md:682-687	empirical superset of `claim-check.mjs`	sed -n '682,687{=;p}' SKILL.md — line 684 prints `r12 fixed the companion) is the empirical superset of `claim-check.mjs`:`
ufo-archive-2026	bounty-keeper (16-pane wall, launched 265, 12 h night budget) is the producer of the `b1k-NNN` run_ids still referenced by `ledger/candidates.jsonl`	SKILL.md:708-710	16-pane wall, launched 265	sed -n '708,710{=;p}' SKILL.md — line 709 prints `(16-pane wall, launched 265, halted on 12 h night budget) is the producer`
ufo-archive-2026	naming drift: archive `claim-packages/<slug>` paths are the pre-rename tree, now `claims/<platform>-<program>/<slug>/`	SKILL.md:711-712	pre-rename tree	sed -n '711,713{=;p}' SKILL.md — line 711 prints `reference. Archive `claim-packages/<slug>` paths are the pre-rename tree —`
ufo-archive-2026	outcome vocabulary: `REFINED→DONE` / `HOLD` with named blockers / `NOT-SUBMITTABLE` / `reconcile-only` / `stop — frontier saturated`	SKILL.md:702-705	Outcome vocabulary the wave established	sed -n '702,706{=;p}' SKILL.md — line 702 prints exactly that phrase
ufo-archive-2026	`NOT-SUBMITTABLE` = gamma-deposit (published audit finding + deployed asset verified fixed first-hand); elastic `falsified-by-execution` → exclusion-notice draft	SKILL.md:700	Proven-but-not-claimable	sed -n '700{=;p}' SKILL.md — full row prints both states verbatim
ufo-archive-2026	defect class 1/2: custodian `head_sha256` mis-binding / `manifest.expected_head_sha256` bound to a stale pre-chain digest — and the committed gate codifies the fix (three-way binding)	corpus/knowledge/claim-gates.md:36-37	three-way binding	sed -n '33,37{=;p}' corpus/knowledge/claim-gates.md — lines 36-37 print `- `head_sha256` = final decision's `decision_sha256` =` / `  `manifest.expected_head_sha256` — three-way binding.`
ufo-archive-2026	same class codified in the round-43 instrument (gate-eligible anchor)	corpus/instruments/claim-package-check.py:60-63	final decision digest and manifest.expected_head_sha256	sed -n '51,66{=;p}' corpus/instruments/claim-package-check.py — lines 62-63 print `scope_signal exactly "NO_SCOPE_OBJECTION"; head_sha256 equals the` / `final decision digest and manifest.expected_head_sha256.`
ufo-archive-2026	defect class 3: manifest artifacts without same-digest redaction receipts — codified gate (gate-eligible anchor)	corpus/instruments/claim-package-check.py:57-59	exactly one receipt binds each artifact	sed -n '51,66{=;p}' corpus/instruments/claim-package-check.py — line 57 prints `R-REDACT     redactions[] non-empty; exactly one receipt binds each artifact;`
ufo-archive-2026	defect class 8: missing in-package `submission-draft.md` is the dominant defect; draft carries verbatim scope excerpt + clone prerequisite + prior-art/dedupe disclosures	SKILL.md:693	dominant defect	sed -n '691,693{=;p}' SKILL.md — line 693 prints `| Missing in-package `submission-draft.md` | dominant defect — nearly every `claim-ready` package | stage canonical paste-ready draft: verbatim scope excerpt, clone prerequisite, prior-art/dedupe disclosures |`
ufo-archive-2026	defect class 9: stale `submission-review/packets/` admin drafts (one materially wrong); `DO-NOT-USE` banner; in-package draft canonical	SKILL.md:694	DO-NOT-USE	sed -n '694{=;p}' SKILL.md
ufo-archive-2026	defect class 11: pre-submission receipt exists (H1 #4028846 k8s; Bugcrowd a169f309 ld-node) → `RECEIPT EXISTS — DO NOT RESUBMIT`	SKILL.md:695	RECEIPT EXISTS	sed -n '695{=;p}' SKILL.md — row names both receipt ids and the banner
ufo-archive-2026	defect class 14: claims marked "verified" but never executed (coinbase vectors 3-4 + path-form boundary; spacex "both resolvers" = DoH only)	SKILL.md:696	"Verified" but never executed	sed -n '696{=;p}' SKILL.md
ufo-archive-2026	defect class 13: stale file:line citations — most common narrative defect (metamask :161→:162, elastic :604→:605, aiven "README.rst:706", web1 READY.md)	SKILL.md:697	most common narrative defect	sed -n '697{=;p}' SKILL.md — the row even back-cites `corpus/knowledge/ufo-archive-2026.md:145-149`
ufo-archive-2026	defect class 18: canonical/alias indistinguishable; fix `status:"claim-ready-alias"` + `claim.json alias_of` + `DO-NOT-ATTACH`	SKILL.md:699	claim-ready-alias	sed -n '699{=;p}' SKILL.md
ufo-archive-2026	defect class 20: REPORT flags `UNRESOLVED CONFLICT` while manifest says `claim-ready`; manifest is gate-visible	SKILL.md:698	UNRESOLVED CONFLICT	sed -n '698{=;p}' SKILL.md
ufo-archive-2026	reconciliation-evidence-chain artifacts (portal-reconciliation-2026-09-11.json, `.ufo/claim-recovery/final-audit.json`) are the do-not-refile registry basis	corpus/knowledge/submitted-registry.md:6-8	final-audit.json	sed -n '5,8{=;p}' corpus/knowledge/submitted-registry.md — line 7 lists both files; also SKILL.md:719-721
ufo-archive-2026	`no_submission_performed` is the norm even in DONE packages	SKILL.md:705-706	is the norm even in DONE packages	sed -n '705,706{=;p}' SKILL.md
ufo-archive-2026	mine the archive for defect patterns; it is not live state	SKILL.md:712-713	not live state	sed -n '712,713{=;p}' SKILL.md — line 713 prints `for defect patterns; it is not live state.`
ufo-archive-2026	"16 per-program L0 mission briefs" (entry :36) — NO SUPPORT; falsified on record	corpus/lessons/round-6-aggregator-audit.md:71-74	15 per-program briefs	sed -n '70,75{=;p}' corpus/lessons/round-6-aggregator-audit.md — `Command: ls fleets/ufo-archive-2026/inquiries/bounty-fleet-2026-09-06/` → `15 per-program briefs + farmscout-hidden.md + feeder01-sources.md + dispatch.log (18 entries)`; still an open correction row at :131
ufo-archive-2026	sighting/handoffs schema-v1 resume handoffs `continuity:"resumed-exact"` (entry :43-44)	NONE (historical record only)	—	negative control: `grep 'resumed-exact'` over corpus+SKILL hits only the entry itself and a citation-survival.tsv GONE row (a loss record, not support)
ufo-archive-2026	bountyA0912 read-only control-plane study with explicit `non_execution` manifest (entry :45-47)	NONE (historical record only)	—	negative control: `grep 'bountyA0912'` → only the entry itself + citation-survival.tsv:1231 `GONE`
ufo-archive-2026	report.json schema field list (`packages_assigned`, `lane_topology`, `route_failures`+`reroutes`, `staged_drafts`, …) (entry :20-24)	PARTIAL — only the `no_submission_performed` norm is committed (SKILL.md:705-706); the full field list exists nowhere else	historical record only for the field list

Classification: `full` — 18 claims with anchors over 6 committed files (SKILL.md,
corpus/README.md, corpus/knowledge/claim-gates.md, corpus/knowledge/submitted-registry.md,
corpus/instruments/claim-package-check.py, corpus/lessons/round-6-aggregator-audit.md).
Gate-eligible subset (anchors under `corpus/instruments/` | `corpus/source-snapshots/`
only): 2-3 rows (claim-package-check.py:57-63 + fixture field shape
`corpus/instruments/fixtures/claim-package/defect-2-digest/evidence/manifest.json:84`,
token `expected_head_sha256`, verified sed -n '83,85{=;p}') — below MIN_ROWS=6, so a
legal `## Re-ground (round 46)` section cannot be filled for this entry without
stretching rows beyond what the committed instruments say.

Historical-record analysis: the entry's tree-description claims (report.json schema
fields :20-24, programs/ evidence shape :26-29, inquiries-brief count :36-40 — itself
falsified on record, sighting/handoffs :43-44, bountyA0912 study :45-47) are records
of a lost tree; the durable, committed-alive content is the defect taxonomy and
outcome vocabulary, which SKILL.md:682-713 restates nearly row-for-row (two of those
rows even back-cite this entry's own line ranges).

## 3. Entry `ufo-workspaces.md` (376 lines)

entry	claim	anchor	token	verified
ufo-workspaces	`.ufo/` = 1.5 G runtime tree, `git ls-files` → 0, mostly not ignored; 25 bh workspaces (19 top + 6 session-layer) vs 22 root reports (19 shared / 3 report-only / 6 workspace-only / 1 phantom); 805 M bounty-fleet; 117 M sessions; two frozen audits	SKILL.md:279-284	25 `bh*` warden-audit workspaces	sed -n '279,284{=;p}' SKILL.md — lines 280-283 print the whole census sentence
ufo-workspaces	`.ufo/` tracked = 0 files, un-ignored except `bounty-fleet/session[s]/`	corpus/knowledge/repo-git-state.md:52	un-ignored except `bounty-fleet/session[s]/`	sed -n '49,54{=;p}' corpus/knowledge/repo-git-state.md
ufo-workspaces	`reroutes.jsonl` = per-mission model-fallback ground truth; 121 records, every observed cause a grok/xai 403/429 → `devin/swe-2:max`; model provenance = resolved route at run time, not the registry pin	SKILL.md:286-288	every cause a grok/xai 403/429	sed -n '286,288{=;p}' SKILL.md
ufo-workspaces	warden `state.json` keyed by PROGRAM → re-dispatch silently overwrites runIds; the yahoo READY package cites the superseded runId; never prune workspace-only ids	SKILL.md:288-290	keyed by PROGRAM	sed -n '288,290{=;p}' SKILL.md
ufo-workspaces	`bounty-fleet/` = keeper overnight fleet; second `ledger/missions.jsonl` (525 rows); 265 launched / 249 reported; two halts (launch_cap@64, night_budget)	SKILL.md:291-294	525 rows / 184 run_ids	sed -n '291,294{=;p}' SKILL.md — see discrepancy note below: SKILL says 184 run_ids/81 unledgered, the entry's round-13 correction says 183/82
ufo-workspaces	bpolish1..8 sessions: zero submission evidence (`submitted_url` all null; receipts = custodian hash-chain); `no_submission_performed` grep trap	SKILL.md:295-298	grep trap	sed -n '295,298{=;p}' SKILL.md — line 297 prints `hash-chain); grep trap — `no_submission_performed: true` → 471 false`
ufo-workspaces	`grok-bounty-assessment-20260911/` = frozen 266-mission reconciliation; 88.30/100 descriptive, never quote without `BLOCKED_BY_NONCOMPENSABLE_GATES`; `clean_repository_closure` unpassable by construction; self-invalidating validator	SKILL.md:299-303	BLOCKED_BY_NONCOMPENSABLE_GATES	sed -n '299,303{=;p}' SKILL.md; also SKILL.md:1018 `(88.30 descriptive, gate BLOCKED, self-invalidating validator)`
ufo-workspaces	`.ufo/` is a cited evidence store: 656 `claims/` files cite `.ufo/…`; 51 of 543 JSON refs dangle; `claim-check.mjs` resolves none → copy bytes; a `.ufo/` citation is not durable evidence	SKILL.md:304-306	51 of 543	sed -n '304,306{=;p}' SKILL.md
ufo-workspaces	`.omp/` = second routing truth: uncommitted `config.yml` rewrites all six `fleet_*` roles; `registry-check` RED with 7 violations; 4 non-registry cards invisible to every check	SKILL.md:307-310	RED with 7 violations	sed -n '307,310{=;p}' SKILL.md; also SKILL.md:1019
ufo-workspaces	claim-recovery `final-audit.json` pins the three preexisting submissions (4002776/4002810/4002789)	corpus/knowledge/submitted-registry.md:17-19	H1 `4002776`	sed -n '16,19{=;p}' corpus/knowledge/submitted-registry.md — three table rows print all three ids with `closed_duplicate` of 3721615 / 3892215
ufo-workspaces	final-audit superseded in place by the package readiness-audit; read the newest artifact first	SKILL.md:1018	superseded in place	sed -n '1018{=;p}' SKILL.md
ufo-workspaces	verdicts 2 READY (`bh0cb2eb6ca20b` intigriti-yahoo, `bh557fda669b20` hackerone-superhuman) / 20 BLOCKED; 5 workspaces closed on warden filter bug (placeholder shells)	corpus/knowledge/mission-control.md:143-148	2 READY	sed -n '140,150{=;p}' corpus/knowledge/mission-control.md — lines 144-148 print the ids, the round-12 correction, and `placeholder shell, dispatched in error` (warden filter bug, fixed 2026-09-14)`
ufo-workspaces	root README "9 lanes" stale vs 10; `.gitignore` asymmetric; `fleets/run/` ignored by design	SKILL.md:1020	ignored by design	sed -n '1011,1021{=;p}' SKILL.md — line 1020 prints `"9 lanes" stale = 10); asymmetric 11-line ignore set (`fleets/run/` ignored by design, `.ufo/` bulk mostly not)`; also repo-git-state.md:53
ufo-workspaces	repo stalled mid-rebase since >=2026-09-11; all Sep 7-15 fleet work (b1k, bh*, ingestion, bpolish) working-tree-only	corpus/knowledge/repo-git-state.md:16-17	working-tree-only	sed -n '14,18{=;p}' corpus/knowledge/repo-git-state.md — line 16 prints the claim; line 17 pins the stall predating 09-11 via `assessment-manifest.json:41-42`
ufo-workspaces	outlier `bh953b65628b4e` = 507 M foreign Rust tree that inflates any naive `.ufo/` census; bulk is untracked AND un-ignored	corpus/knowledge/repo-git-state.md:60-63	507 M `.ufo/bh953b65628b4e`	sed -n '60,63{=;p}' corpus/knowledge/repo-git-state.md; corroborated by corpus/lessons/round-12.md:27-28 (foreign Rust tree, ~12k inflation)
ufo-workspaces	keeper tree holds `reports/` = 249 b1k + 8 claim reconciliations; `plan-b1k-*.md` x233	SKILL.md:1016	249 b1k + 8 claim reconciliations	sed -n '1015,1018{=;p}' SKILL.md
ufo-workspaces	candidate `b1k-210` (immunefi-gamma) merely restates `final-audit.json` — not independent evidence (entry :245-248)	NONE (historical record only)	—	negative control: `grep 'b1k-210'` over corpus+SKILL hits only the entry itself (three self-references)
ufo-workspaces	`claim-readiness.json` v3 census (254 status files = 242 PARKED / 8 BLOCKED / 3 DONE / 1 SUBMITTED), the 12-vs-12 disjoint trap, scorer `state_points`, dispositions 226/23/16/1	NONE (historical record only)	—	zero committed restatement found; these numbers exist only in the entry
ufo-workspaces	reroutes.jsonl line schema `{round, identity, from, to, cause, action}`; "absence = zero reroutes, not missing data"; `gq`+16hex vs `bh`+12hex vs `b1k-NNN` id minting; bpolish 504-file/115.4 MiB breakdown; live `config.yml` `maxConcurrency: 32`	NONE (historical record only)	—	no committed restatement found anywhere in the enumerated scope

Classification: `full` — 15 claims with anchors over 4 committed files in scope
(SKILL.md, repo-git-state.md, mission-control.md, submitted-registry.md; plus
corpus/lessons/round-12.md outside the enumerated scope). Gate-eligible subset:
NONE — no corpus/instruments/ or corpus/source-snapshots/ bytes support any
ufo-workspaces claim (citation-survival.tsv `.ufo/…` rows are GONE loss records, and
anchorcheck.py's prefix lists are instrument mechanics, not claim support). This
entry is census-full but gate-incompatible: it cannot host a legal re-ground section.

Historical-record analysis: the lost tree's occurrence numbers (per-file counts,
scorer internals, claim-readiness census, config.yml values, id-minting trivia) are
historical records; the committed-alive content is the five operational takeaways and
the census ratios, which SKILL.md:279-310 restates. One live committed-bytes
contradiction: entry says 183 run_ids / 82 unledgered (its own round-13 correction),
SKILL.md:292-294 still says 184 / 81 — a re-ground row must not paper over this.

## 4. Entry `vdp-disclosure-packages.md` (37 lines)

entry	claim	anchor	token	verified
vdp-disclosure-packages	`vdp-disclosures/<slug>/` is a distinct, lighter (four-file) contract, not the six-file claims contract	SKILL.md:451	distinct, lighter contract	sed -n '449,473{=;p}' SKILL.md — line 451; contrast the six-file table corpus/knowledge/claim-package-contract.md:11-16 (verified sed -n '9,16{=;p}')
vdp-disclosure-packages	ROUTE.md = channel + attribution decree: free + fully attributed via the vendor security.txt Contact route, e.g. an H1 `embedded_submissions` URL	SKILL.md:451-453	embedded_submissions	sed -n '451,453{=;p}' SKILL.md — line 453
vdp-disclosure-packages	the route is attested in the actual filed record (Anthropic VDP embedded form via security.txt contact)	corpus/knowledge/submitted-registry.md:89-91	security.txt contact	sed -n '86,93{=;p}' corpus/knowledge/submitted-registry.md — line 90 prints `2026-09-06T01:19:04Z via Anthropic VDP embedded form (security.txt contact →`
vdp-disclosure-packages	cover-note.md = short operator-facing cover text prepended at send time	SKILL.md:454	cover-note.md	sed -n '449,473{=;p}' SKILL.md — line 454
vdp-disclosure-packages	report.md = same craft contract as claim reports ("Disclosed freely by", pinned commit/file/sha256, CWE, CVSS, verbatim scope excerpt)	SKILL.md:454-455	same-craft	sed -n '454,455{=;p}' SKILL.md; craft-field detail matches claim-package-contract.md:11 `"Scope excerpt" = verbatim policy text + URL + observed_at + content sha256` (verified sed -n '9,16{=;p}')
vdp-disclosure-packages	SUBMITTED.md = timestamp + verbatim platform confirmation	SKILL.md:455-456	verbatim platform confirmation	sed -n '455,456{=;p}' SKILL.md
vdp-disclosure-packages	the actual SUBMITTED.md content is committed: timestamp 2026-09-06T01:19:04Z, route, attribution	corpus/knowledge/submitted-registry.md:89-93	2026-09-06T01:19:04Z	sed -n '86,93{=;p}' corpus/knowledge/submitted-registry.md
vdp-disclosure-packages	free + attributed is an operator decree superseding the anonymity clause; no payout	corpus/knowledge/intake-surface.md:129-131	supersedes the anonymity	sed -n '126,131{=;p}' corpus/knowledge/intake-surface.md — line 131 also explains `vdp-disclosures/anthropic-*/` ships attributed; also SKILL.md:213-215 `freebie-class ATTRIBUTED not anonymous` (verified sed -n '213,231{=;p}')
vdp-disclosure-packages	attribution identity vgpnk1337@gmail.com	corpus/knowledge/submitted-registry.md:91	vgpnk1337@gmail.com	sed -n '86,93{=;p}' corpus/knowledge/submitted-registry.md
vdp-disclosure-packages	operator personally sends; the fleet stages, never sends	SKILL.md:456-457	fleet stages, never sends	sed -n '455,457{=;p}' SKILL.md; also SKILL.md:229-230 `…are operator-attributed ledger facts, never fleet actions` (verified sed -n '213,231{=;p}')
vdp-disclosure-packages	such disclosures are real filings: ledger `DISCLOSED_FREE` row at the byte-identical timestamp; the anthropic VDP was freely disclosed 2026-09-06	corpus/knowledge/mission-ledger.md:48-49	DISCLOSED_FREE	sed -n '46,50{=;p}' corpus/knowledge/mission-ledger.md; submitted-registry.md:92-93 `byte-identical timestamp`; SKILL.md:739-740 `freely disclosed 2026-09-06` (verified sed -n '719,747{=;p}')
vdp-disclosure-packages	sibling `claims/*/honest-zero-vdp-no-payout/` = the two-file parked VDP shape (report.md + status.json)	SKILL.md:457-459	honest-zero-vdp-no-payout	sed -n '455,459{=;p}' SKILL.md; verdict family `honest-zero-<reason>` in claim-package-contract.md:35-36 (verified sed -n '9,16{=;p}' shows table; :35 verified in the full-file read)
vdp-disclosure-packages	the whole VDP surface is corpus-attested only — SKILL points back at this entry as the only record	SKILL.md:461-473	now the only record	sed -n '449,473{=;p}' SKILL.md — lines 471-473 print `Every VDP fact above is anchored in `corpus/knowledge/vdp-disclosure-packages.md` (`:3-5`, `:9`, `:13-16`, `:20`, `:22-31`), which is now the only record.`
vdp-disclosure-packages	cover-note content = a rickroll joke line (entry :14)	NONE (historical record only)	—	negative control: `grep 'rickroll'` over corpus+SKILL hits only the entry itself

Classification: `full` — 12 claims with anchors over 5 committed files (SKILL.md,
submitted-registry.md, intake-surface.md, mission-ledger.md,
claim-package-contract.md; coordinated-disclosure-timelines.md:28 also names the
sibling format). Gate-eligible subset: NONE — no instruments/source-snapshots bytes
carry VDP content (source-tree-loss-2026-09-28.md:120 records the VDP surface as
`NOT IN MIRROR`). Census-full, gate-incompatible.

Historical-record analysis: this entry is by design the sole record of a lost tree —
SKILL.md:461-473 says so explicitly and summarizes it at :451-459. Claims that exceed
that committed summary (CVSS-vector specifics, hackerone-ruby/nextcloud status.json
field shapes, the rickroll cover note) rest on the entry alone and are historical
records within the corpus; everything SKILL.md restates is alive.

## 5. Decision-relevant summary for the C1 planner

- All three entries are `full` by the census bar (>=6 anchored claims over >=2 files
  of committed bytes) — their claims are NOT lost with the tree; SKILL.md and sibling
  knowledge entries restate most of them.
- None of the three is a viable C1 re-ground target under r46-c1-gate.py's
  `ANCHOR_DIRS = ("corpus/instruments/", "corpus/source-snapshots/")`:
  - ufo-archive-2026: only 2-3 gate-legal rows exist (claim-package-check.py:57-63 +
    a fixture field shape) — below MIN_ROWS=6; the archive's occurrence claims have no
    instruments-dir support.
  - ufo-workspaces: zero gate-legal anchors.
  - vdp-disclosure-packages: zero gate-legal anchors.
- The frozen intended pair (claim-package-contract.md, claim-gates.md) remains the
  right choice; this census does not attack it. These three entries should stay
  gated; re-grounding them would require exactly the token-stretching my seat forbids.
- Frozen C1 reading reproduced: `c1-gate fixed=1/7 exit=1`, `gated=24 broken=0
  lines=64/base=64` (re-run this session, quoted in §1).

## 6. Discrepancies found in committed bytes (reported, not fixed)

1. run-id count: ufo-workspaces.md (round-13 correction) says the second
   `ledger/missions.jsonl` has 183 run_ids / 82 launched runs left no ledger line;
   SKILL.md:292-294 still says 184 / 81. The entry's own correction says 184 counted
   the runless `bountyfleet1` producer.
2. ufo-archive-2026.md:36 "16 per-program L0 mission briefs" remains falsified on
   record (lessons/round-6-aggregator-audit.md:71-74: live 15 per-program + 2 named
   briefs + dispatch.log; open correction row :131).
3. corpus/README.md:94 "19-mission defect taxonomy" sits inside a `CLOSED round 8`
   historical note while README.md:23 says 20 (round-12 correction) — historical
   value kept as recorded, consistent with root-loss-2026-10-12.md:67-70 policy.

## 7. Controls, method, limitations

- Positive verification: every anchor above was printed with
  `sed -n 'N,M{=;p}'` (line number + content) on files proven byte-identical to the
  freeze commit; tokens quoted are literal substrings of the printed lines.
- Do-nothing discrimination: junk token `kasegi-census8-negative-control-zzz` over
  corpus/knowledge+SKILL.md → `No matches found`; historical-only tokens
  (`bountyA0912`, `resumed-exact`, `bh953b65628b4e`, `b1k-210`, `rickroll`) surface
  only in the entries themselves, in GONE loss records (citation-survival.tsv), or —
  for `bh953b65628b4e` — in genuine independent restatements (repo-git-state.md:60-63,
  lessons/round-12.md:27-28), which I then counted as anchors. The frozen counter
  itself reproduces 1/7 on the untouched freeze bytes, so a do-nothing tree does not
  grade green.
- Scope: search space was the seat's enumerated scope (corpus/instruments/ incl.
  fixtures, corpus/source-snapshots/, other corpus/knowledge entries, SKILL.md, gate
  docstring) plus committed corpus/README.md and corpus/lessons/* where they carried
  decisive records — labeled as such. citation-survival.tsv/md rows were treated as
  loss records (they record that a citation is GONE), never as claim support.
- Limitations: I did not re-derive lost-tree numbers (impossible — trees absent); I
  did not run anchorcheck.py per entry (the gated recheck lines already encode that
  and fail closed); lessons/ and corpus/README.md anchors are outside the gate's
  ANCHOR_DIRS and are marked whenever used. No tool installs were needed or made.
- Hygiene: read-only on the lane except this Report file; scratch
  /fast/scratch/hyaku/kasegi-r46/R46ScoutCensus8 removed before yield; no git/jj
  mutation anywhere; no live-target testing; no credentials in this file.
