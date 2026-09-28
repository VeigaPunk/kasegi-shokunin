# `.ufo/` runtime workspaces + `.omp/` — the untracked execution layer

All numbers verified live 2026-09-28 by census over `/home/vgpnk/Projects/bounties/.ufo/`
and `.omp/` (`find | wc -l`, `du -sh`, `git ls-files`, structured first/middle/last
sampling) by 4 scouts + 2 executors + L1, read-only. Nothing in `.ufo/` is mission
state until copied into `evidence/` or `claims/` — but claim packages *cite* `.ufo/`
paths as provenance (see §citations), which makes the layer load-bearing anyway.

## Overview — one untracked tree, five generations of workspace

`.ufo/` total = 1.5 G; `git ls-files .ufo` = **0**; `git status --porcelain .ufo`
collapses to a single `?? .ufo/`; `git check-ignore .ufo/` exits 1 — **untracked AND
un-ignored** (`.gitignore` hides only `.ufo/cache/`, which doesn't exist, and
`.ufo/bounty-fleet/session[s]/`).

| Subtree | Kind | Producer | State |
|---|---|---|---|
| `.ufo/bh<hex>/` ×19 (+6 under `bounty-fleet/sessions/`) | per-mission readiness-audit workspaces | L0 bounty-warden (`.ufo-warden/{warden.log,state.json}`) | frozen 2026-09-14/15 |
| `.ufo/bounty-fleet/` 805 M | overnight hunter fleet (`bountyfleet1`, b1k-NNN) | `fleets/ufo-archive-2026/bounty-keeper/keeper.mjs` | dead since 2026-09-11T09:37Z halt |
| `.ufo/sessions/` 117 M | raw omp seat transcripts (`bpolish1..8`) | omp session recorder v3 | single day 2026-09-15 |
| `.ufo/grok-bounty-assessment-20260911/` 3.3 M | one-shot corpus reconciliation | planner-lane L1 (`openai-codex/gpt-daybreak-blue-latest`) + 10 review seats | frozen, self-invalidating (§grok) |
| `.ufo/claim-recovery/` 16 K | post-hoc b1k recovery audit | `Main (L1)` | frozen 2026-09-11 |

Plus 22 root files `.ufo-mission-report-bh*.md` (the audit reports themselves).

## `.ufo/bh*` — warden-dispatched readiness-audit workspaces

Producer: L0 **bounty-warden** (`.ufo-warden/warden.log` + `state.json`:
`DISPATCH <program> -> bh<id>`, TICK, COMPLETE via tick/handoff-present|settle|
status-absent). `bh`+12hex ids are minted by the warden — not by omp
fleet-dispatcher (which mints `gq`+16hex) nor by keeper (`b1k-NNN`).

Lifecycle: warden dispatch → L1 wwkd `plan.md` (Spec = mission prompt + L0 relay +
`fleets/mission-template.md` + `claims/README.md`, Author `Main (L1)`) → planner →
batched 16-seat wave (`proposals/<Agent>.md`, up to 17 identities: Planner/Scout/
Scout2/Executor/Executor2/Reviewer/Reviewer2/KxReviewer/Critic/Critic2/Sentinel/
Sentinel2/Scribe/Connector/Simplifier/MutationTester/Revenger) → distiller →
Pareto-integrate into claims/evidence → `ops/claim-check.mjs` → root
`.ufo-mission-report-bh<id>.md` → handshake JSON → warden COMPLETE → pane retire.
Fast-exit branch skips the wave when claimability is falsified up front.

Census: 18 of 19 top-level workspaces are small (2–25 files, 8 K–490 K). Outlier
`bh953b65628b4e` = **507 M / 12,125 files** — a cloned Rust target tree
(`grok-1.0.30-linux-x86_64`, 9,358 `.rs` files under `harvest/scout-grokbuild`),
foreign corpus, not fleet output; any `.ufo/` file census that includes it inflates
~12k.

**Two workspace roots, disjoint:** 19 at `.ufo/bh*` + 6 under
`.ufo/bounty-fleet/sessions/` (`bh0c9b600312b5`, `bh150650a15515`, `bh25252897468e`,
`bh68dc6980e31b`, `bh6a6e38c876fe`, `bh89c676911502`) = **25 workspaces** vs **22
reports** → 19 shared / 3 report-only (`bh0cb2eb6ca20b`, `bh3d2d3d538556`,
`bh557fda669b20`) / 6 workspace-only; plus 1 dispatch-only phantom
(`bhb0bfa2c8715d`, no workspace, no report). "Find the workspace for report X"
fails 3/22; a top-level-only scan over-counts failures 6-fold.

Verdicts (grep `Outcome` over all 22 reports, triple-verified): **2 READY / 20
BLOCKED** — READY = `bh0cb2eb6ca20b` (intigriti-yahoo, "1 claimable finding, gate
`ops/claim-check.mjs` → OK") and `bh557fda669b20` (hackerone-superhuman,
`node ops/claim-check.mjs claims/hackerone-superhuman/ingestion-20260914` → OK).
Other `READY` string occurrences are negations ("0 READY, 1 BLOCKED", "Why not
READY"). This **falsifies round 5's "21 readiness audits all BLOCKED"** (fixed in
SKILL.md/mission-control.md this round). Of the 20 BLOCKED: 5 workspaces closed on
an L0 "warden filter bug" (placeholder shells dispatched in error) — their BLOCKED
is dispatcher bookkeeping, not scope analysis.

Id hazards:
- `.ufo-warden/state.json` is keyed by **PROGRAM**: re-dispatch silently overwrites
  `runId` (bugcrowd-t-mobile, hackerone-bcny, intigriti-yahoo each got a second run
  within ~7 min); superseded run ids survive only in reports/sessions.
- **Provenance split on a READY package:** `claims/intigriti-yahoo/ingestion-20260914/status.json:6`
  + `provenance.json:3` carry `mission_id: bh7609023286b0` (superseded, report-less
  run) while `PLAN.md:1` + the root report say `bh0cb2eb6ca20b`. Joining on
  `mission_id` mis-attributes a READY finding; `bh7609023286b0` must not be pruned —
  it is the producing workspace.
- Report-less workspaces are not safe to delete: two are producing workspaces of
  shipped packages (3 of the workspace-only set are warden `done:false` = unretired).

### `reroutes.jsonl` — per-mission model-fallback ground truth

Present in 8/19 top-level + 4/6 session-layer workspaces (12 files, **121 records**);
absence = zero reroutes, not missing data. Line schema
(`.ufo/bh008834d61250/reroutes.jsonl:1`): `{round, identity, from, to, cause,
action}`. Cause census: **every observed cause is a grok/xai path failure** —
21× `403 personal-team-blocked:spending-limit (grok credits exhausted)`, 17×
`403 spending-limit, credits exhausted`, 6× `HTTP 403 personal-team-blocked`, 4× each
`rerouted task route also resolved to dead xai…` / `task-default spawn resolved to
xai-oauth/grok…`; targets are `devin/swe-2:max` (17× via `ufo-l2` transport).
Consequence: the bh wave's registry-pinned model identity (`grok-4.5:low`) is
unreliable provenance — a claim citing "the grok review" needs the reroute log.

## `.ufo/bounty-fleet/` — the overnight keeper tree (b1k-NNN, 805 M)

Producer (verified in source): `fleets/ufo-archive-2026/bounty-keeper/keeper.mjs:48-63`
— `runId = b1k-<slot pad3>`, `ufo-sighting launch --session-dir
.ufo/bounty-fleet/sessions/<runId>`, prompt `@.ufo/bounty-fleet/p-wave-l1.md`,
`UFO_ROOT=~/Projects/origin-work/ufo-fsd-alpha`, `FLEET=bounties`, `WINDOW_CAP=16`,
`LAUNCH_CAP=384`, `NIGHT_MS=12h`; `:72` night_budget halt. Per-run L1 rode
`xai-oauth/grok-4.6:xhigh`.

Size map: `sessions/` 592 M (2,251 files; 265 b1k + 6 bh + 9 claim-* dirs) +
`scopes/` 198 M (2,453 files; 305 program dirs, 1,004 raw `.html`) = **98% of the
tree**; the knowledge surface is <7 M: root plans 242 files (`plan-b1k-NNN.md` ×233,
`plan-bh*.md` ×3, `plan-round0.md`, `p-l1.md`, `p-wave-l1.md`, `p-claim-astra.md`,
`p-claim-seq-astra.md`), `report.md` (fleet halt: `UFO_SIGHTING_RUN_ID: bountyfleet1`,
`as_of 2026-09-10T21:56:00Z`, honest stops M2 GitHub-CLI overfit → honest-zero, M3
Node.js halted on I9 bounty-status conflict, "Safety invariant held: no submission,
contact, disclose, exfiltrate"), `ledger/` 3 jsonl, `reports/` 1,071 files
(249 `b1k-NNN.md` + 8 `claim-claim-*.md` + 140 per-hypothesis `<slug>/` bundles with
`pin.json` + `planner-r0-m2-host-a-to-b.md`), `claim-prompts/` 8 md, `session/`
(singular!) 617 files = durable L1 notes + 9 plan copies + `data-walk.md`.

Plan schema (wave): header (Spec `p-wave-l1.md`, wwkd posture, `UFO_SIGHTING_RUN_ID`)
→ Data Walk → 4 frozen axes (safety is an invariant, NOT an axis) → M1 hash-gate →
M2 overfit ONE → M3 generalize ONE → M_halt. `plan-round0.md` here is the
bountyfleet1 hunt plan and explicitly disclaims `docs/plan-round0.md` (the HQ
bootstrap) — same filename, different document.

**Second `missions.jsonl`, second state machine:** `.ufo/bounty-fleet/ledger/missions.jsonl`
= 525 rows / 184 run_ids (LEARNED 183 / SCOPED 174 / PLANNED 161 / EVIDENCED 2 /
EXECUTED 1 / VERIFIED 1 / SUBMISSION_PREPARED 1 / 2 unparseable) vs root
`ledger/missions.jsonl` = 718 lines / 260 missions. Any `**/missions.jsonl` glob
merges two unrelated machines. `telemetry.jsonl` 281 rows (lease_claimed 88,
operator_decree 32, mission_parked 83); `candidates.jsonl` 118 pre-hunt triage rows
(116 program_ids). Writers are each run's own L1, not a central ops tool.

**Four irreconcilable run counts:** keeper `state.json launched=265` = `sessions/`
dirs (b1k-001…265, no gaps), but reports 249, root plans 233 (+9 in `session/`),
ledgered run_ids 184, telemetry 172 → **81 launched runs left no ledger line**.
Silent truncation: `b1k-248` + `b1k-251..265` have transcripts but no report and no
ledger row (b1k-253 sole exception); ledger frozen 2026-09-11T03:39Z while keeper
ran to 09:37Z. Two halts, not one: `launch_cap` at launched=64 (2026-09-10T23:01Z),
then `night_budget` (09:37Z); 80/348 `launch_errors` (23%) with no recorded cause.

`reports/claim-claim-*.md` (8) reconcile packaged findings against live/prior H1
submission state → the archive-wave's third terminal state **BLOCKED** (alongside
REFINED→DONE and NOT-SUBMITTABLE); `claim-seq` has a prompt + sessions dir but no
reconcile report.

Not a private tree: `fleets/leases.json` holds a b1k-224 lease pointing into
`.ufo/bounty-fleet/scopes/`; `fleets/run/_b1k-{134,148,157}.status.json` exist —
`fleets/` and `.ufo/bounty-fleet/` are two generations of one fleet.

## `.ufo/sessions/` — bpolish seat transcripts (117 M)

Exactly **8** seat dirs `bpolish1..8` (the round-11 note "248 entries" was a
listing artifact — falsified), 504 files, 115.4 MiB: jsonl 129/108.2 MiB, log 240/
5.8 MiB (bash 143, bash-original 71, eval 13, read 8, hub 4, async 1), md 119, json 16.
Layout: `<lane>/<ts>_<uuid>.jsonl` (L1) + same-stem dir of `<Role>.jsonl/.md` +
`NN.<tool>.log`, nested group dirs (`ReserveProtocol-2/`, `HuntDydxModules/`,
`HuntMorphoSdk/`).

Producer: **omp session recorder v3** (`{"type":"session","version":3,"cwd":"/home/vgpnk/Projects/bounties"}`,
model `devin/swe-2`, thinking=max) driven by `.omp/skills/ufo/SKILL.md` +
`.omp/agents/*.md`; `gx-*` DESPAWN lines in 17 files confirm the UFO/godspeed host
protocol. All 8 lanes launched within 15 s at 2026-09-15T20:31:58–20:32:13Z;
bpolish8 re-ran 23:36:52Z. `bpolish` is an **operator lane label** (0 hits in
`.omp/`, never emitted by any tool) = board-polish over `claims/<program>/<slug>/`
packages for UFO missions under `origin-work/ufo-fsd-alpha/.ufo/missions/hunt-*`.

**Refile verdict: does NOT extend the do-not-refile registry.** Non-null
`submitted_url`: zero occurrences (key present with `null` in ~51 files). Strict
`(?<!no_)submission_performed:true` fires in 9 files — all Gate-3 checklist text,
negative assertions, an agent's own grep pattern, validator regex.
`custodian-receipts.json` (152 files) is a custody **hash-chain** (schema
`custodian-receipts/v1`, `prior_receipt_sha256`), not a submission receipt.

Grep traps (this corpus, measured): naive `submission_performed.*true` → **471 hits
/ 61 files, 0 real** (~50× false positives from `no_submission_performed: true`);
`receipt` → 2,841 hits, all custodian material; `submission_state:"SUBMITTED"`
counters measure checklist text volume, not state; 403 hits are agents grepping
`.ufo/sessions` itself (self-referential — never cite as independent confirmation);
108 MiB of jsonl embeds full file bodies — cheap greps only; extension/reality
mismatch (`.md` holding JSON, byte-identical `.json`/`.md` pairs, 9 zero-byte `.md`)
— `.jsonl` is the only canonical mirror. The real submission registry lives in
`claims/<program>/<slug>/status.json` + `fleets/run/*.status.json`.

## `.ufo/grok-bounty-assessment-20260911/` — frozen, unpassable, self-invalidating

43 files / 3 dirs / 3.3 M; **historical, zero live consumers** (grep: 0 hits in
`ops/*.mjs`, `fleets/registry.json`, `docs/*.md`; only 4 archival readers, incl.
`fleets/ufo-archive-2026/missions/claim-github-nines/lanes/connector-r1.md:52`
which already calls it stale; dir itself untracked).

`assessment-manifest.json` (`schema_version: grok-bounty-assessment-manifest/v2`,
`created_at 2026-09-11T15:05:59Z`): 7 axes (technical_validity, scope_safety,
evidence_integrity, claim_readiness, model_attribution, operational_reliability,
review_coverage); 5 hard gates (written_scope, authorization, evidence_integrity,
no_duplicate_or_prior_submission, **clean_repository_closure** — a 5th gate
`claim-check.mjs` doesn't have); `corpus_binding` = 266 declared missions
(bountyfleet1 + 265 b1k), 250 finalized reports, 16 reportless, 691 transcripts /
588,976,407 bytes, 0 parse errors; `completion.claim_package_gate_census:
"COMPLETE_ZERO_PASSING"`.

Scorer (`compute-review-score.mjs`, read in full): state_points {pass:100, warn:50,
fail:0, unknown:0, not_applicable:null → excluded from numerator AND denominator};
per-dimension D = roundHalfUp(100·Σpoints/|eligible|); overall = gcd-reduced
Σ(n·w, d·100) fold, clamped [1,100]; gate `BLOCKED_BY_NONCOMPENSABLE_GATES` iff any
hard gate fail+unknown>0 or any mandatory subcheck non-pass; "the descriptive score
never overrides this gate." Result: **88.30/100** (exact rational 66643979/754775;
0.25·99.56 + 0.20·99.60 + 0.20·99.20 + 0.10·0.00 + 0.10·100.00 + 0.10·86.47 +
0.05·100.00) with `claim_readiness` 0.00 (denominator 1 = Gamma) and gate BLOCKED.
Dispositions: 226 supported_honest_zero / 23 incomplete / 16 provider_failure /
1 substantiated_positive; `claim_ready` never used. **Never quote 88.30 without the
gate string** — the scalar is inflated by NA-exclusion (265/266 units NA on
claim_readiness) and 226 honest-zero passes.

Gate unpassable **by construction** this epoch: `clean_repository_closure`
hardcoded fail ×266 (the dirty-tree/rebase condition, recorded as
`repository_commit: "BLOCKED_ACTIVE_PREEXISTING_REBASE"` +
`clean_tree_proof: "…_AND_AMBIENT_CHANGES"` at manifest :41-42 — the round-12
discovery that the rebase stall is ≥17 days old).

Review seats: 9 semantic + 1 claim-security on operator-mapped
`alibaba-token-plan/deepseek-v4-pro:max` ("DeepSeek V4 Pro 0813" — identity attested
by operator, not locally verifiable); wave 1 died on provider 429, wave 2 resumed on
operator attestation; planner lane = `openai-codex/gpt-daybreak-blue-latest`; 2
grok-4.5 lanes did census + a claim-gate mutation probe.

`claim-readiness.json` (v3, 09-11T14:51Z): 254 status files = 242 PARKED / 8
BLOCKED / 3 DONE / 1 SUBMITTED; the 12 nonparked packages **all failed claim-check
(15–38 errors each)**; `operator_queue_sha256 8f3ddffc…` is **stale** vs the live
`docs/claim-ready-index.md` (`b8b3bf13…`, regenerated after the 09-14/15
ingestions). Trap: those 12 nonparked ≠ today's 12 queue rows — disjoint sets, both
"12"; today's rows are all DONE+claimable. Candidate `b1k-210` (immunefi-gamma)
restates `.ufo/claim-recovery/final-audit.json` blockers from 2 h earlier — not
independent evidence.

**Self-invalidation:** re-running the frozen scorer with its own nine byte-identical
bound lane outputs now exits `ok:false` at `lanes/deepseek-review-07.json`
units[23]=b1k-210, because `validate-review-output.mjs:58` re-derives cited line
ranges against **current** file lengths and
`claims/immunefi-gamma/hypervisor-deposit-from-to/submit/readiness-audit.json` was
rewritten 2026-09-14 (now 129 lines; frozen citation says `:95-133`). Lesson: an
assessment whose validator reads live repo state is not reproducible after the repo
moves — and its 588 MB of grounding transcripts are gitignored (`.gitignore:11`), so
only sha256 aggregates survive; nothing is re-derivable from a checkout.

## `.ufo/claim-recovery/` — the b1k post-mortem (16 K, 3 files)

`plan.md` + `data-walk.md` + `final-audit.json`. Window 2026-09-10→11; inputs: 265
launched b1k missions, 249 finalized reports, 16 reportless (b1k-248, b1k-251..265),
fleet-ledger terminal rows, omp transcripts, claims inventory + claim-wave
`submit/BLOCKED.md`. Exactly one overnight terminal row is `LEARNED` with
`finding_count=1`: **b1k-210 `immunefi-gamma/hypervisor-deposit-from-to`** — later
flipped to BLOCKED. `final-audit.json` keys: schema_version, audited_at, mode, axes,
mission_census, reportless_disposition, codex_spark_review, candidate,
prior_disclosure_reconciliation, administrative_action, yield. It pins the three
preexisting submissions (airtable 4002789 not_established, spotify 4002810
closed_duplicate of 3892215, mozilla 4002776 closed_duplicate of 3721615; account
veigapunk, CDP 9222, `submission_verified: true`, 0 mutations) — corroborates
round 9. **But it is superseded in place** for gamma: its blockers
(REQUIRED_POC_MISSING etc., "no PoC / l1-replica.py source-string predicates only")
were resolved by the package's own `submit/readiness-audit.json` (2026-09-14: PoC
`evidence/poc-deposit-from-to.test.ts` exists, "2 passing (785ms)",
A_TO_B_LEAK alice −2000/bob +2000 shares) which adds 3 NEW blockers
(KNOWN_ISSUE_PRIOR_AUDIT, DEPLOYED_ASSET_ALREADY_FIXED, OOS_OPERATIONAL_CONFIG).
Outcome unchanged (BLOCKED, 0 submissions) but the blocker set moved — always read
the *newest* audit in a package, never the recovery snapshot.
`claims/immunefi-gamma/…/status.json` still points `mission_report` at
`.ufo/missions/claim-gamma-deposit/report.json` — **`.ufo/missions/` does not
exist** (dangling citation, invisible to every gate).

## `.omp/` — the second routing truth (cross-domain mechanics; bounty consequences kept)

120 K / 17 files. Tracked (10): `config.yml` + `agents/{kx-connector,kx-distiller,
kx-executor,kx-labrat,kx-reviewer,kx-scout,kx-security,scope-evidence-custodian,
the-bounty-hunter}.md`. On disk but **untracked**: `agents/ing-scout.md`,
`agents/ufo-l2.md` (both literal `devin/swe-2:max`), `skills/` (whole subtree).
11 cards for 10 registry lanes; the 4 non-registry cards (ing-scout, ufo-l2,
scope-evidence-custodian, the-bounty-hunter) are invisible to every registry-check
test except the banned-token scan — the round-7 "bijection holds" verdict is
directory-driven over `kx-\w+.md` only (`registry-check.mjs:57-80`).

Live `config.yml` (36 l, **modified-uncommitted**): `task.maxConcurrency: 32`,
`maxRecursionDepth: 2`; `modelRoles`: task/smol/default → `@ufo_deepseek_max` →
`alibaba-token-plan/deepseek-v4.1-flash:max`; `fleet_judge/fleet_planner/
fleet_executor/fleet_depth` → `devin/swe-2:max`; `fleet_volume/fleet_utility` →
`@ufo_deepseek_max`; `retry.fallbackChains` (deepseek-v4.1-flash:max →
deepseek-v4-1-flash:high → grok-4.5:low ×2 → devin/swe-2:max),
`fallbackRevertPolicy: never`. The committed HEAD version instead matches the root
README's 2026-09-04 decree table (k3/qwen3.8-max:xhigh/deepseek-v4-pro:max/
deepseek-v4-flash-0731/grok-4.5:low) — **README describes git HEAD, not the live
router**; `registry-check.mjs` reads the working file and is RED (exit 1, 7 `@role`
violations: 3 genuine card↔registry mismatches + resolver artifacts from the
single-level quote-retaining alias resolver at `:87-91`). Every one of the 7 kx
cards self-contradicts: description names the registry primary, `model:` pin
resolves elsewhere. `.omp/skills/ufo/SKILL.md` is a drifted untracked fork of the
canonical `origin-work/ufo-fsd-alpha` skill (304 l / sha256 `2d5bfd3e…` vs 626 l /
`40949973…`, 685 diff lines; cites `scripts/{sync-ufo-contracts,…}` that don't
exist in bounties). Bounty-domain consequence: **model attributions in claim
provenance must name the resolved route at run time (reroutes.jsonl / session
headers), never the registry pin.** Router mechanics themselves → kumitate/protocol
(reported, not absorbed).

## Root `README.md` + `.gitignore` — the tracked/untracked boundary

`README.md` (70 l, mtime 2026-09-06 04:08): "the fleet: **9 lanes**" is stale —
registry has 10 lane keys and `validate.mjs` prints 10; the "9" traces to the stale
header comment at `registry-check.mjs:6`. Its routing table matches registry
primaries but omits `mission_l1` and matches nothing in the live `config.yml`.
`.gitignore` = 11 lines in the worktree (HEAD has 9; the last two —
`.ufo/bounty-fleet/session[s]/` — are uncommitted): `node_modules/ .next/ out/ .env*
.DS_Store .ufo/cache/ vgn-bounty-lab/ fleets/run/ fleets/leases.json
.ufo/bounty-fleet/session/ .ufo/bounty-fleet/sessions/`. Asymmetric and
load-bearing: the 6 session-layer bh workspaces are permanently un-committable
(ignored) while top-level `.ufo/bh*` (incl. the 507 M outlier) is one `git add -A`
from being committed; `fleets/run/` ignored **by design** → round 9's evidence
source `portal-reconciliation-2026-09-11.json` and every `*.status.json` are
untracked; a fresh clone would surface `session/`+`sessions/` (622 M) as untracked.

## `.ufo/` is a cited evidence store — and the citations are unversioned

The strongest in-domain fact of this census: **656 files under `claims/` contain a
`.ufo/` path string**; JSON-scoped scan finds **543 distinct `.ufo/…` references,
51 already dangling (~9%)** — e.g. `claims/immunefi-gamma/…/status.json:45` →
`.ufo/missions/…` (dir never existed), `claims/github-bounty/nines-githubapp-dangling-cname/status.json`
→ `.ufo/scopes/claim-github-nines/`, `claims/intel-bug-bounty/pqos-pci-ids-stack-overflow/custodian-receipts.json`
→ `.ufo/missions/claim-intel/…`. `claim-check.mjs` never resolves them (it checks
in-package digests), so a dangling `.ufo/` citation is invisible to every gate.
**Rule: never treat a `.ufo/…` reference as durable evidence — copy the bytes into
the package before relying on them.** Same durability gap one directory over:
`fleets/run/` (ignored). Repo git state (stalled rebase, 903 dirty entries) →
`knowledge/repo-git-state.md`.

## Operational takeaways

1. Runtime artifacts become citable mission evidence only when copied into
   `claims/<pkg>/evidence/` or `evidence/<program>/` — `.ufo/` paths rot silently
   (51/543 already dangling) and no gate notices.
2. Do-not-confuse pairs: root `ledger/missions.jsonl` (718/260) vs
   `.ufo/bounty-fleet/ledger/missions.jsonl` (525/184); `.ufo/bounty-fleet/report.md`
   (fleet halt) vs `reports/` (per-run); `.ufo/bounty-fleet/plan-round0.md` vs
   `docs/plan-round0.md`; `session/` (notes) vs `sessions/` (transcripts);
   `.ufo/sessions/bpolish*` (2026-09-15 board-polish) vs
   `.ufo/bounty-fleet/sessions/b1k-*` (2026-09-10/11 hunt).
3. Model provenance = resolved route at run time: warden wave → `reroutes.jsonl`
   (121 records, all grok/xai 403/429 → `devin/swe-2:max`); b1k wave → session
   headers (`grok-4.6:xhigh`); bpolish → recorder v3 headers (`devin/swe-2`,
   thinking=max). Registry pins describe intent, not history.
4. Frozen audits are epoch snapshots: `final-audit.json` (09-11) was superseded
   in place by package-local `readiness-audit.json` (09-14); `claim-readiness.json`
   binds a stale queue sha. Read the newest artifact in the package first.
5. Check `git status` before any commit-sourced claim — the repo has been stalled
   mid-rebase since ≥2026-09-11 and all Sep 7–15 work is working-tree-only
   (`knowledge/repo-git-state.md`).
