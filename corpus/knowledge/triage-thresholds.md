# Triage thresholds — every gate, constant, and weight

Source: `~/Projects/bounties/ops/{claim-check,ev-report,fleet-dispatch,shared}.mjs`
+ `~/Projects/bounties/bounty-map/schema.json`, all read in full 2026-09-28.
Paths below are relative to `~/Projects/bounties/` unless absolute. Line numbers
are source lines, not rendered lines.

This is the single derivation of the numeric thresholds the bounty pipeline
runs on: queue admission weights (`fleet-dispatch.mjs::buildQueue`), package
gates (`claim-check.mjs`), the adjusted-EV formula (`ev-report.mjs`), the
shared constants every ops file imports (`shared.mjs`), and the record contract
(`schema.json`). Narrative companions remain `claim-gates.md` (gate list),
`ev-model.md` (EV), `ops-invariants.md` (shared constants) — the `Corpus tie`
column records the round-13 audit verdict per row: `MATCHES` (agreed) or
`SUPERSEDES` (corrected the companion — every such target was repaired in
place round-13, marker "round-13 correction"; §9 is the ledger). Out of scope
here: `claim-index.mjs`,
`prepare-claims.mjs`, `validate.mjs` (see `claim-gates.md`, `ops-invariants.md`).

Pipeline order: **queue admission** (`buildQueue`) → **package validation**
(`claim-check.mjs`) → **commit/tag/push** (`commitClaims`→`finalizePush`).
`ev-report.mjs` gates nothing (reporting tool); `schema.json` gates record
shape only, and only through `validate.mjs`.

## 1. Queue admission — candidate filters

`buildQueue()` iterates `bounty-map/programs/*.json` and drops a record when any
filter matches (`fleet-dispatch.mjs:88-114`):

| Filter | Exact condition | Line | Corpus tie |
|---|---|---|---|
| unreadable record | `readJson(...)` falsy → skip | 100-101 | — |
| leased | `leaseAlive(leases[id])`: `Date.parse(leases[id].expires_at) > Date.now()` | 102, 58 | MATCHES: `mission-control.md:20-24` |
| attempts exhausted | `attempts(id) >= MAX_ATTEMPTS` (MAX_ATTEMPTS = 2) | 103, 46 | MATCHES: `SKILL.md:117`, `mission-control.md:20-21` |
| active mission | `readStatus(id)` exists AND its `state` ∉ TERMINAL — i.e. a non-terminal `fleets/run/<id>.status.json` blocks redispatch | 105 | MATCHES: `mission-control.md:20-21` |
| delivered | `status.state === 'DONE'` (stated separately as "never redispatch") | 106 | MATCHES: `mission-control.md:21` |

`attempts(id)` = `max(0, parks − resets)`, where `parks` counts telemetry lines in
`ledger/telemetry.jsonl` matching `"program": "<id>"[,}]` **and**
`/mission_(parked|failed)/`, and `resets` counts lines containing
`attempt_reset` (`fleet-dispatch.mjs:78-85`).

Consequence: pane/tmux crashes write `mission_failed` (:327), which
`attempts()` counts identically to evidence parks — two infra failures
permanently exhaust a program's `MAX_ATTEMPTS = 2` hunt budget (:46, :103).

`leases` default is `{}` when `fleets/leases.json` is absent/unparseable
(`fleet-dispatch.mjs:56`); lease records are
`{program_id, mission_id, leased_at, expires_at}` (`fleet-dispatch.mjs:182`).

## 2. Queue score weight table

Single expression, `fleet-dispatch.mjs:110`:

```
score = priority_hit(9e12) + continue_verdict(2e12) + curated_ev(1e12)
      + reward.min * 1000 + is_live(1)
```

| Weight | Exact trigger | Numeric | Line | Corpus tie |
|---|---|---|---|---|
| priority | `id ∈ fleets/priority.json` `priority[]` (missing file → `{priority:[]}`) | `9e12` = 9,000,000,000,000 | 91, 110 | MATCHES: `intake-surface.md:71`, `mission-control.md:19` |
| continue | `id ∈ {v.program : v.verdict === 'continue'}` from `docs/review-verdicts.jsonl` | `2e12` = 2,000,000,000,000 | 92-96, 110 | MATCHES: `intake-surface.md:71`, `mission-control.md:19-20` |
| curated | `rec.ev_inputs && Object.keys(rec.ev_inputs).length > 0` (boolean, not EV magnitude) | `1e12` = 1,000,000,000,000 | 107, 110 | SUPERSEDES: `SKILL.md:113-114` (four terms, no `is_live`) and `SKILL.md:175-176` (same omission; names the term `curated-EV` although the source tests only non-emptiness); see §2.2 |
| reward | `(rec.reward?.min ?? 0) * 1000` | 50 → 5e4 … 10000 → 1e7 (observed) | 110 | SUPERSEDES: `SKILL.md:175` — that line writes `reward.min`, source multiplies by 1000 |
| freshness | `rec.freshness?.label === 'live' ? 1 : 0` | `1` | 110 | MATCHES: `intake-surface.md:72`, `mission-control.md:20-21`; SUPERSEDES: `SKILL.md:113-114,175-176` (term omitted) |

Sort is `(a,b) => b.score - a.score`, descending, stable (`fleet-dispatch.mjs:113`).

### 2.1 Tier arithmetic — the collision bound

Tiers are additive, so tier separation only holds while each lower term stays
below the next tier: `reward.min * 1000 < 1e12` ⟺ **`reward.min < 1e9`**. No
guard exists at `fleet-dispatch.mjs:110`; a record with `reward.min ≥ 1e9`
would tie or outrank the curated tier (`≥ 2e9` outranks the continue tier;
`≥ 9e9` outranks priority). Observed headroom is five orders of magnitude — see
census below. The `is_live` term can never outrank a `reward.min ≥ 1` record
(1 ≪ 1000), so freshness only orders records whose reward term is 0.

### 2.2 Census (read-only, 2026-09-28)

```
$ node -e "…"   # reads bounty-map/programs, fleets/priority.json, docs/review-verdicts.jsonl, fleets/leases.json
records 1088 reward-obj 48 reward.min-num 14 freshness {"stale_snapshot":830,"live":258}
priority.json keys [ 'priority', 'note' ] len 14
review-verdicts lines 486 {"leave":430,"continue":50,"drop":6} distinct continue programs 50
leases entries 224 alive 0
ev_inputs-nonempty 1
adjusted_ev occurrences across all 1088 program files: 0
reward.min values: 50,100,200,200,200,250,500,500,500,500,750,1250,3000,10000  (max*1000 = 1e7)

# same run, score expression evaluated per record
score bands  priority 14 | continue 36 | curated 1 | reward 13 | live-only 228 | zero 796
priority.json ∩ continue-verdict programs = 14/14 (priority ⊂ continue)
priority.json entries present in the map = 14/14 ; curated record = github-bug-bounty
```

Consequences, all derived from the expression at line 110:

- 796 records (73.2%) score exactly `0` and 228 (21.0%) score exactly `1`
  (freshness only) — 1024 records are decided by `readdirSync` order
  (`fleet-dispatch.mjs:98`); only 64 records (5.9%) hold any tier: 14 priority
  (+2e12 each, all also continue hits), 36 continue-only, 1 curated, 13
  reward-band.
- `priority.json` is a **subset** of the 50 continue-verdict programs
  (14/14 intersection), matching the code comment "continue-verdict programs
  hunt first (operator decree: continue the 50)" (`fleet-dispatch.mjs:90`): the
  9e12 term only breaks ties *inside* the continue cohort, it does not add a
  disjoint tier.
- `adjusted_ev` never contributes: `buildQueue` reads it nowhere, and no record
  stores it (see §5.3).

## 3. Dispatcher runtime constants

| Constant | Value | Line | Corpus tie |
|---|---|---|---|
| `MAX` (`--max`) | default `5` | 29 | MATCHES: `mission-control.md:13-14` |
| `STAGGER_S` (`--stagger`) | default `20` s; enforced as `STAGGER_S*1000 − (now − lastLaunch)` before the 2nd+ launch in a tick | 30, 399-400 | MATCHES: `mission-control.md:13-14` |
| `LEASE_MS` | `2 * 3600 * 1000` = 7,200,000 ms = 2 h | 45 | MATCHES: `mission-control.md:23-24`, `SKILL.md:526` |
| `MAX_ATTEMPTS` | `2` | 46 | MATCHES: `SKILL.md:117`, `mission-control.md:20-21` |
| `TERMINAL` | `['DONE','PARKED','FAILED','RETIRED']` | 47 | MATCHES: `mission-control.md:28-33` |
| `MODEL` (initial) | `alibaba-token-plan/deepseek-v4-pro:max` | 34 | MATCHES: `mission-control.md:36-38` |
| stagger/round-robin | `--models-rr m1,m2,m3 --rr-until <epochMs>`; active only while `Date.now() < RR_UNTIL` | 38-44 | MATCHES: `mission-control.md:38-40` |
| poll interval | `setTimeout(tick, 30000)` = 30 s | 409 | MATCHES: `mission-control.md:13-14` |
| `--sync` cadence | `tickCount % 10 === 0` (~5 min at 30 s ticks) | 352-353 | MATCHES: `mission-control.md:42-46` |
| `SYNC_PATHS` | 11 entries: `claims/README.md, evidence, ledger, docs, ops, fleets/missions, bounty-map, fleets/registry.json, fleets/mission-template.md, README.md, .gitignore` | 348 | MATCHES: `mission-control.md:43-46` |
| grid/session | `SESSION='ufo_sighting'`, `GRID='formation'` | 27, 65 | MATCHES: `SKILL.md:526` |
| limit-log window | log `mtimeMs` within `15 * 60e3` = 900,000 ms = 15 min; tail = last `20000` chars | 276-277 | MATCHES: `mission-control.md:40-45` |
| off-peak window | `h = (getUTCHours() − 3 + 24) % 24; offpeak = h >= 12 && h < 22` (UTC−3) | 298-299 | MATCHES: `mission-control.md:36-38`, `SKILL.md:14-15` |
| off-peak model | `alibaba-token-plan/deepseek-v4-pro:max` | 300 | MATCHES: `mission-control.md:36-38` |
| peak model | `openai-codex/gpt-6-astra:max` | 300 | SUPERSEDES: `mission-control.md:37-38` — that entry writes `openai-oauth/gpt-6-astra:max`; source says `openai-codex/` |
| limit-fallback model | `xai-oauth/grok-4.6:low` | 281 | MATCHES: `mission-control.md:43-44` |
| limit family regex | `MODEL.includes('token-plan') ? /qwen|deepseek|token.?plan/i : /astra|daybreak|codex|openai/i` | 271 | MATCHES: `mission-control.md:41-45` |
| limit signature regex | `/usage limit has been reached\|usage_limit_reached\|rate limit exceeded\|429 Too Many/i` (ANDed with family, tail-only) | 272, 278 | SUPERSEDES: `mission-control.md:41-43` — that entry lists 3 signatures, omitting `usage_limit_reached` |
| dry-run log | `dry: would lease+launch <id> (state <s>, attempts <n>, score <score>)` | 177 | — |

`windowModel()` applies to **new launches only**: on window flip, `MODEL` is
rewritten and `limitFallback` reset (383-394); running missions keep their pin
and the lease is not touched.

## 4. `claim-check.mjs` — the gate tables

Contract: `node ops/claim-check.mjs claims/<program-id>/<slug>`; errors
accumulate in an array and are printed in order — **no early exit**, so one run
reports every violation (`claim-check.mjs:18-19, 228-231`). 48 `err()` call
sites across 8 gate families.

### 4.1 Invocation and file presence

| Gate | Trigger (fails when) | Error template | Line | Corpus tie |
|---|---|---|---|---|
| arg/dir | no arg, or dir does not exist | `claim-check: usage: node ops/claim-check.mjs claims/<program-id>/<slug>` + exit 1 | 14-15 | MATCHES: `claim-gates.md:4-5` |
| package root | `realpathSync(dir)` resolves the package once for symlink confinement | — | 16 | MATCHES: `claim-gates.md:21-23` |
| required files | any of `report.md`, `claim_checklist.md`, `custodian-receipts.json`, `provenance.json`, `status.json` missing | `missing <f>` | 22-23 | MATCHES: `claim-gates.md:10-11`, `claim-package-contract.md:9-16` |
| manifest file | `evidence/manifest.json` missing | `missing evidence/manifest.json` | 24 | MATCHES: `claim-gates.md:10-11` |

### 4.2 Content markers

| Gate | Trigger | Error template | Line | Corpus tie |
|---|---|---|---|---|
| scope excerpt | `report.md` present AND does not match `/scope excerpt/i` | `report.md: no scope excerpt section` | 27-28 | MATCHES: `claim-gates.md:15` |
| no-submission marker | `report.md` present AND does not match `/no submission (performed\|made)/i` (phrase in prose, not the JSON field) | `report.md: missing explicit "no submission performed" marker` | 29 | MATCHES: `claim-gates.md:15`, `claim-package-contract.md:11` |
| operator gate | `claim_checklist.md` present AND does not match `/OPERATOR-GATED/i` | `claim_checklist.md: missing OPERATOR-GATED marker` | 31-32 | MATCHES: `claim-gates.md:16` |

Absent files are skipped here (presence is already gated in 4.1) — note the
`if (report)` / `if (checklist)` guards.

### 4.3 Manifest + artifacts + redaction receipts (`L39-71`)

| Gate | Trigger | Error template | Line | Corpus tie |
|---|---|---|---|---|
| sequence | `manifest.sequence` not a number | `manifest: missing sequence` | 40 | MATCHES: `claim-gates.md:20` |
| head key | `'expected_head_sha256' in manifest` false | `manifest: missing expected_head_sha256` | 41 | MATCHES: `claim-gates.md:20` |
| path confinement | `resolve(dir,'evidence',a.path)` does not start with `dir + sep` | `manifest artifact escapes package: <path>` | 45-46 | MATCHES: `claim-gates.md:21-23` |
| existence | `a.path` empty or file absent | `manifest artifact missing on disk: <path>` | 47 | MATCHES: `claim-gates.md:21-23` |
| symlink confinement | `realpathSync(ap)` does not start with `realDir + sep` | `manifest artifact symlink escapes package: <path>` | 48-49 | MATCHES: `claim-gates.md:21-23` |
| digest | `sha256File(ap) !== a.sha256` | `manifest artifact hash mismatch: <path>` | 50 | MATCHES: `claim-gates.md:22-23` |
| polarity | `a.polarity ∉ {'positive','negative'}` | `manifest artifact <path>: polarity must be positive\|negative` | 51 | MATCHES: `claim-gates.md:23` |
| positive floor | zero positive-polarity artifacts in the whole manifest | `manifest: claim package requires at least one positive-polarity artifact` | 52, 70 | MATCHES: `claim-gates.md:24`, `claim-package-contract.md:13` |
| same-digest receipt | no redaction with `artifact_sha256 === a.sha256 && scanned_artifact_sha256 === a.sha256` AND non-empty distinct `producer`/`verifier` (trimmed compare) | `manifest artifact <path>: missing same-digest redaction receipt with distinct producer/verifier` | 53-60 | MATCHES: `claim-gates.md:25-27` |
| receipt↔receipt | `r.scanned_artifact_sha256 !== r.artifact_sha256` | `redaction receipt not bound to artifact digest: <json>` | 65 | MATCHES: `claim-gates.md:25-27` |
| receipt identities | `producer` or `verifier` empty after trim | `redaction receipt: producer and verifier identities are required` | 66 | MATCHES: `claim-gates.md:26` |
| receipt distinctness | `producer === verifier` | `redaction receipt: verifier must differ from producer` | 67 | MATCHES: `claim-gates.md:27` |
| receipt↔manifest | receipt digest not equal to any `a.sha256` | `redaction receipt does not bind a manifest artifact: <digest or '(missing digest)'>` | 68 | MATCHES: `claim-gates.md:27` |

Extracted values: `positiveArtifactCount` increments on
`polarity === 'positive'` (52); `manifestSha256 = sha256File(manifestPath)` over
exact file bytes (37) — used later for the status binding (4.8).

### 4.4 Custodian decision chain (`L74-93`)

| Gate | Trigger | Error template | Line | Corpus tie |
|---|---|---|---|---|
| chain present | `chain = receipts.chain ?? receipts.decisions ?? []` not a non-empty array | `custodian-receipts.json: claim package requires a non-empty decision chain` | 77-79 | MATCHES: `claim-gates.md:31` |
| hard stop | `String(d.scope_signal).trim().toUpperCase() === 'HARD_STOP'` (checked first, own message) | `custodian HARD_STOP present: <action> — package must park, not ship` | 82-83 | MATCHES: `claim-gates.md:32-33` |
| scope signal | uppercased/trimmed `scope_signal !== 'NO_SCOPE_OBJECTION'` | `custodian decision <action>: scope_signal must be exactly NO_SCOPE_OBJECTION` | 84 | MATCHES: `claim-gates.md:32-33`, `SKILL.md:90-91` |
| grant id | `matched_grant_id` empty after trim | `custodian decision <action>: matched_grant_id is required` | 85 | MATCHES: `claim-gates.md:33-34` |
| decision digest | `decision_sha256` fails `/^[a-f0-9]{64}$/i` | `custodian decision lacks a valid decision_sha256: <action>` | 86 | MATCHES: `claim-gates.md:34` |
| head digest | `head_sha256` fails `/^[a-f0-9]{64}$/i` | `custodian-receipts.json: missing valid head_sha256` | 88 | MATCHES: `claim-gates.md:35-36` |
| head chain-end | `chain.at(-1).decision_sha256 !== custodianHead` | `custodian-receipts.json: head_sha256 does not match the final decision` | 89 | MATCHES: `claim-gates.md:35-36` |
| manifest binding | `manifest.expected_head_sha256 !== custodianHead` (three-way binding) | `manifest expected_head_sha256 does not bind the custodian decision-chain head` | 90 | MATCHES: `claim-gates.md:35-36`, `claim-package-contract.md:14` |
| unreadable file | file exists but `readJson` returned falsy | `custodian-receipts.json: present but unreadable` | 91-92 | MATCHES: `claim-gates.md:29-36` |

`action` defaults to `'(unnamed action)'` (81). Note `HARD_STOP` emits **both**
its own message and the `NO_SCOPE_OBJECTION` message — two errors for one
decision.

### 4.5 Provenance (`L96-97`)

| Gate | Trigger | Error template | Line | Corpus tie |
|---|---|---|---|---|
| provenance substance | `provenance.json` parses AND `(steps ?? transitions ?? []).length === 0` AND falsy `agents` | `provenance.json: no steps/transitions/agents recorded` | 96-97 | MATCHES: `claim-gates.md:38-40` |

Boundary: this is the **entire** provenance gate. `claim-check.mjs` contains no
reference to `schema_version`, `policy_sha256`, `external_effects_performed`,
`commit`/pin, or per-transition models — the provenance fields enumerated in
`claim-package-contract.md:15` are unenforced. Likewise the manifest
`schema_version: "evidence-manifest/v1"` (`claim-package-contract.md:13`) is
never read.

### 4.6 Symlink / size / secrets sweep (`L100-114`)

| Gate | Trigger | Error template | Line | Corpus tie |
|---|---|---|---|---|
| symlink | any directory entry is a symlink (`lstatSync`) — aborts into that path | `symlink is forbidden in claim package: <rel>` | 104-105 | — (new; `claim-gates.md:42-47` covers the regex only) |
| size | text file `> 5 * 1024 * 1024` bytes = 5,242,880 B (≈5 MiB), skip scan | `oversize artifact (>5MB): <path>` | 111 | — (new) |
| secrets | `/(api[_-]?key\|secret\|token\|password\|bearer)\s*[:=]\s*["']?[A-Za-z0-9_\-]{16,}/i` matches file text | `possible secret in <rel> — redact before commit` | 100, 113 | MATCHES: `claim-gates.md:42-47` |

Decoded pattern: keyword (`api key`/`apikey`/`api-key`, `secret`, `token`,
`password`, `bearer`) then `:` or `=` then an optional quote then ≥16 chars of
`[A-Za-z0-9_-]`. A bare 16-char token with no `:`/`=` separator does not trip it.

### 4.7 `status.json` — terminal gates (`L117-160`)

| Gate | Trigger | Error template | Line | Corpus tie |
|---|---|---|---|---|
| state | `status.state !== 'DONE'` (any other value, incl. `SUBMITTED`) | `status.json state is <state>, commits require DONE` | 119 | MATCHES: `claim-gates.md:51`, `claim-package-contract.md:25` |
| claimable | `status.claimable !== true` (strict identity) | `status.json must affirm claimable: true` | 120 | MATCHES: `claim-gates.md:52` |
| finding count | `!Number.isInteger(status.finding_count) \|\| status.finding_count < 1` | `status.json finding_count must be a positive integer` | 121 | MATCHES: `claim-gates.md:52` |
| manifest binding | `manifest_sha256` fails `/^[a-f0-9]{64}$/i` OR `!== sha256File(evidence/manifest.json)` at run time | `status.json manifest_sha256 does not bind the current evidence/manifest.json` | 122-123 | MATCHES: `claim-gates.md:53-54` |
| review outcome | `String(claim_review.outcome).toUpperCase() !== 'APPROVED'` OR `claim_review.claim_ready !== true` | `status.json requires an APPROVED claim_review with claim_ready: true` | 126-127 | MATCHES: `claim-gates.md:54-55` |
| producer | `claim_review.producer_identity` empty after trim | `status.json claim_review must name producer_identity` | 132 | MATCHES: `claim-gates.md:55` |
| reviewer shape | `reviewer.role !== 'kx-reviewer'` (exact) OR empty `identity`/`requested_model`/`resolved_model` OR `typeof reviewer.fallback !== 'boolean'` | `status.json claim_review must bind kx-reviewer identity, requested/resolved model, and fallback provenance` | 133-141 | MATCHES: `claim-gates.md:56-58`, `SKILL.md:94-95` |
| identity separation | `producer_identity === reviewer.identity` (both non-empty, exact compare, untrimmed equality after per-field trim) | `status.json claim_review reviewer must differ from producer` | 142-143 | MATCHES: `claim-gates.md:58-59` |
| hard gates | each of `written_scope`, `authorization`, `evidence_integrity`, `no_duplicate_or_prior_submission` uppercased ≠ `'PASS'` — one error per gate | `status.json claim_review hard gate <gate> must be PASS` | 145-155 | MATCHES: `claim-gates.md:59-61`, `claim-package-contract.md:28-29` |
| subchecks | each of `no_secrets`, `operator_attribution` uppercased ≠ `'PASS'` | `status.json claim_review subcheck <subcheck> must be PASS` | 156-160 | MATCHES: `claim-gates.md:61`, `claim-package-contract.md:30` |

### 4.8 `status.json` — claimability, duplication, blockers (`L162-225`)

| Gate | Trigger (any one) | Error template | Line | Corpus tie |
|---|---|---|---|---|
| not-claimable heuristics | `claimable === false`; `not_claimable === true`; `do_not_submit === true`; truthy `claimability_gap`; `finding_count === 0`; `verdict` matching `/not[-_\s]?claimable\|honest[-_\s]?zero/i` | `status.json explicitly marks this package not claimable` | 163-171 | MATCHES: `claim-gates.md:63-66` |
| prior submission | `submission_performed === true` OR truthy `submitted_url` OR uppercased `submission_state === 'SUBMITTED'` | `status.json records a prior submission; duplicate submission is forbidden` | 174-179 | MATCHES: `claim-gates.md:66-67` |
| global duplicate | scans every `claims/<program>/<slug>/status.json` (root = `resolve(dir,'..','..')`, self skipped, unparseable skipped): another package has a prior-submission record AND (`slug === currentSlug` OR (`currentTitle.length >= 16` AND lowercased titles equal)) | `global duplicate guard: matching finding already has a submission record at <program>/<slug>` | 181-199 | MATCHES: `claim-gates.md:67-70` |
| blockers | truthy `blocked_reason`, `submission_blocker`, `blocking_record`, OR `submit/BLOCKED.md` exists | `status.json or submit/BLOCKED.md records an unresolved readiness blocker` | 201-208 | MATCHES: `claim-gates.md:70-71` |
| nested readiness | over the truthy contexts `claim_review`, `claim_wave`, `claim_attempt`, `submission`: `String(ctx.outcome ?? ctx.state).toUpperCase() === 'BLOCKED'` OR `ctx.claim_ready === false` OR `ctx.submission_ready === false` | `status.json contains a blocked nested readiness decision` | 210-220 | MATCHES: `claim-gates.md:71-74` |
| nested blockers | same contexts, `(ctx.blocker_codes ?? ctx.blockers ?? ctx.remaining_gates)` is a non-empty array | `status.json contains unresolved nested readiness blockers` | 218-223 | MATCHES: `claim-gates.md:71-74` |

Title threshold: **16 characters** minimum before the cross-package title
comparison engages (`claim-check.mjs:194`) — shorter titles can only duplicate
by slug.

### 4.9 Output contract

| Outcome | stdout | Exit | Line |
|---|---|---|---|
| usage / missing dir | `claim-check: usage: node ops/claim-check.mjs claims/<program-id>/<slug>` | 1 | 14-15 |
| any error | one `ERROR <message>` line per error, in evaluation order, then `claim-check: FAIL (<N> errors) <dir>` | 1 | 228-231 |
| zero errors | `claim-check: OK <dir>` | 0 | 233 |

Caveat (round-13): the artifact loop `continue`s past a failing artifact
(:46-49) and the sweep skips oversize files without scanning (:111), so one
run's error set is path-dependent — not a full partition of violations.

### 4.10 Error-string register (48 `err()` call sites)

`missing <f>` (23) · `missing evidence/manifest.json` (24) · `<path>: unparseable — <msg>` (20, `readJson` on manifest/custodian/provenance/status) · `report.md: no scope excerpt section` (28) · `report.md: missing explicit "no submission performed" marker` (29) · `claim_checklist.md: missing OPERATOR-GATED marker` (32) · `manifest: missing sequence` (40) · `manifest: missing expected_head_sha256` (41) · `manifest artifact escapes package:` (46) · `manifest artifact missing on disk:` (47) · `manifest artifact symlink escapes package:` (49) · `manifest artifact hash mismatch:` (50) · `manifest artifact …: polarity must be positive|negative` (51) · `manifest artifact …: missing same-digest redaction receipt with distinct producer/verifier` (60) · `redaction receipt not bound to artifact digest:` (65) · `redaction receipt: producer and verifier identities are required` (66) · `redaction receipt: verifier must differ from producer` (67) · `redaction receipt does not bind a manifest artifact:` (68) · `manifest: claim package requires at least one positive-polarity artifact` (70) · `custodian-receipts.json: claim package requires a non-empty decision chain` (79) · `custodian HARD_STOP present: …` (83) · `custodian decision …: scope_signal must be exactly NO_SCOPE_OBJECTION` (84) · `custodian decision …: matched_grant_id is required` (85) · `custodian decision lacks a valid decision_sha256:` (86) · `custodian-receipts.json: missing valid head_sha256` (88) · `custodian-receipts.json: head_sha256 does not match the final decision` (89) · `manifest expected_head_sha256 does not bind the custodian decision-chain head` (90) · `custodian-receipts.json: present but unreadable` (92) · `provenance.json: no steps/transitions/agents recorded` (97) · `symlink is forbidden in claim package:` (105) · `oversize artifact (>5MB):` (111) · `possible secret in … — redact before commit` (113) · `status.json state is …, commits require DONE` (119) · `status.json must affirm claimable: true` (120) · `status.json finding_count must be a positive integer` (121) · `status.json manifest_sha256 does not bind the current evidence/manifest.json` (123) · `status.json requires an APPROVED claim_review with claim_ready: true` (127) · `status.json claim_review must name producer_identity` (132) · `status.json claim_review must bind kx-reviewer identity, requested/resolved model, and fallback provenance` (140) · `status.json claim_review reviewer must differ from producer` (143) · `status.json claim_review hard gate … must be PASS` (153) · `status.json claim_review subcheck … must be PASS` (158) · `status.json explicitly marks this package not claimable` (171) · `status.json records a prior submission; duplicate submission is forbidden` (179) · `global duplicate guard: matching finding already has a submission record at …` (196) · `status.json or submit/BLOCKED.md records an unresolved readiness blocker` (207) · `status.json contains a blocked nested readiness decision` (220) · `status.json contains unresolved nested readiness blockers` (223)

## 5. `ev-report.mjs` — the adjusted-EV formula

### 5.1 Formula (input shape → derived terms)

| Term | Exact expression | Finite-input requirement | Line | Corpus tie |
|---|---|---|---|---|
| `p_success` | `p_in_scope × p_reproducible × p_unique × p_accepted` (`reduce((a,b)=>a*b, 1)`) | all 4 finite | 77 | MATCHES: `ev-model.md:7`, `SKILL.md:498` |
| `gross_value` | `p_success × expected_reward` | `p_success` finite AND `expected_reward` finite | 78 | MATCHES: `ev-model.md:8`, `SKILL.md:499` |
| `total_cost` | `effort_hours × opportunity_rate + direct_cost + delay_cost + expected_risk_cost` | all 5 finite | 79-81 | MATCHES: `ev-model.md:9-10`, `SKILL.md:500-501` |
| `adjusted_ev` | `gross_value − total_cost` | both finite | 82 | MATCHES: `ev-model.md:11`, `SKILL.md:502` |

`isNum(v) = typeof v === 'number' && Number.isFinite(v)` (46): `NaN`,
`±Infinity`, numeric strings, `null`, `undefined` are all non-finite → the term
becomes `UNKNOWN`. Formatting is `String(Number(v.toFixed(6)))` (47) — six
decimals then trailing-zero stripping; probabilities therefore print like
`0.378` or `0.1`, never `0.100000`.

### 5.2 Input list and basis provenance (`L54-70`)

Exactly 10 inputs, in this print order: `p_in_scope`, `p_reproducible`,
`p_unique`, `p_accepted`, `expected_reward`, `effort_hours`, `opportunity_rate`,
`direct_cost`, `delay_cost`, `expected_risk_cost` (54-58). Each row is
`  <key padded to 20> = <value padded to 10> basis: <basis><detail>` (70) where
`basis` is `source_url` (with `source_url` string appended), `estimate`, or
`unknown`; a non-empty `sources[k].rationale` string is appended after ` | `
(60-69). `as_of` prints raw from `ev_inputs.as_of` or `UNKNOWN` (50).

### 5.3 Output/exit contract + non-persistence of `adjusted_ev`

| Outcome | stdout | Exit | Line |
|---|---|---|---|
| no program id | `usage: node ops/ev-report.mjs <program-id>` | 2 | 23-26 |
| program file absent | `ev-report: program file missing: bounty-map/programs/<id>.json` | 2 | 30-33 |
| unparseable file | `ev-report: WARNING unparseable program file <rel>: <msg>`, then all terms `UNKNOWN` (`rec = null`, `ev = {}`) | 0 | 38-41 |
| normal | header `ev-report: <id> (<name>)`, `as_of: …`, `inputs:` block, `derived (hunter contract):` block, `positive_adjusted_ev: true\|false\|unknown` | 0 | 49-92 |

`adjusted_ev` is **derived only, never persisted**: the script writes no file,
and `schema.json` has no such property (`ev_inputs` is
`additionalProperties:false` :34, no `adjusted_ev` in :35-51).
`fleet-dispatch.mjs:200` nevertheless reads `rec.ev_inputs?.adjusted_ev` — the
read can never be a number (0/1088 records carry the key, census §2.2), so
every `mission_dispatched` line logs `adjusted_ev: "unknown"` and the
negative-EV `ev_note` branch (:204) is dead code: AR12's "negative/unknown EV
is ledgered honestly" holds only in the "unknown" direction (round-13
three-way-verified derivation: L1 full-source read × executor draft ×
reviewer derivation).

## 6. `bounty-map/schema.json` — the record contract

| Field / constraint | Exact rule | Line | Corpus tie |
|---|---|---|---|
| record | `additionalProperties: false` at top level | 5 | MATCHES: `SKILL.md:522` |
| required keys | `id, name, source_kind, official_url, freshness, lane, mission_state` | 6 | MATCHES: `SKILL.md:522` |
| `id` | pattern `^[a-z0-9-]+$` | 8 | — |
| `name` | `minLength: 1` | 9 | — |
| `source_kind` | enum `independent \| platform \| web3` | 10 | — |
| `freshness` | required `label`, `as_of`; `additionalProperties:false` | 12-15 | — |
| `freshness.label` | enum `live \| snapshot_retained \| stale_snapshot` | 17 | — |
| `freshness.as_of` | `format: date-time` | 18 | — |
| `reward` | no required keys; `additionalProperties:false` | 21-23 | — |
| `reward.min` / `max` | `number` (no min/max bound; negatives allowed by schema) | 25-26 | — |
| `reward.currency` | pattern `^[A-Z]{3}$` | 27 | — |
| `ev_inputs` | `additionalProperties:false`, **no** `required` (so `{}` is schema-valid) | 32-34 | MATCHES: `ops-invariants.md:34-40` (subset validator) |
| `p_in_scope`, `p_reproducible`, `p_unique`, `p_accepted` | `number`, `minimum: 0`, `maximum: 1` | 36-39 | MATCHES: `ev-model.md:15-16` |
| `expected_reward`, `effort_hours`, `opportunity_rate`, `direct_cost`, `delay_cost`, `expected_risk_cost` | `number`, unbounded | 40-45 | MATCHES: `ev-model.md:21-23` |
| `deadline` | `format: date-time` | 46 | MATCHES: `ev-model.md:22-23` |
| `duration_p90`, `submission_buffer` | `number` | 47-48 | MATCHES: `ev-model.md:22-23` |
| `as_of` | `format: date-time` | 49 | MATCHES: `ev-model.md:16` |
| `sources` | `object`, free-form (basis provenance per input) | 50 | MATCHES: `ev-model.md:16` |
| `lane` | `string` | 53 | — |
| `mission_state` | enum, 12 values in order: `DISCOVERED, NORMALIZED, DEDUPED, SCOPED, RANKED, PLANNED, AUTHORIZED, EXECUTED, EVIDENCED, VERIFIED, SUBMISSION_PREPARED, LEARNED` | 54 | MATCHES: `SKILL.md:111-112` (decorative in practice) |
| `board_ref` | required `dataset, record_id, refresh_run_id, evidence_id` | 55-58 | — |
| `board_ref.dataset` | enum `independent_programs \| platform_programs \| web3_programs` | 60 | — |
| `board_ref.evidence_id` | pattern `^[0-9a-f]{64}$` | 63 | — |
| `notes` | `string` | 66 | — |

Boundary: `schema.json` is enforced only as far as `validate.mjs`'s hand-rolled
subset (`ops-invariants.md:34-40`); `--strict` additionally requires non-empty
`ev_inputs` (`ops-invariants.md:41-42`), which is what makes "curated"
(`fleet-dispatch.mjs:107`) a strict-mode-valid notion rather than a
schema-mandated one.

## 7. `shared.mjs` — constants every ops file imports

| Export | Value | Line | Corpus tie |
|---|---|---|---|
| `BANNED` | `['cursor', 'opencode']` | 9 | MATCHES: `ops-invariants.md:18`, `SKILL.md:525` |
| `PARKED` | `[]` (chatgpt park lifted 2026-09-04) | 10 | MATCHES: `ops-invariants.md:19` |
| `K3_SEATS` | `['judge', 'planner']` | 11 | MATCHES: `ops-invariants.md:20` |
| `K3_TOKEN` | `/kimi-code\/k3\|kimi-k3\|moonshot\/kimi-k3/i` | 13 | MATCHES: `ops-invariants.md:21` |
| `TELEMETRY_EVENTS` | 8 registry kinds: `lane_parked, lane_degraded, operator_decree, xask_dry, board_imported, binding_verified, reroute_drill, provenance_drift` | 15-24 | MATCHES: `ops-invariants.md:22`, `SKILL.md:525` |
| `sha256File` | sha256 hex of exact file bytes; `null` when path absent/unreadable | 27-33 | MATCHES: `ops-invariants.md:23` |
| `gitMutationBlocker` | markers `rebase-merge, rebase-apply, MERGE_HEAD, CHERRY_PICK_HEAD` → `{code:'ACTIVE_GIT_OPERATION'}`; detached HEAD → `{code:'HEAD_NOT_ON_MAIN'}`; branch ≠ `main` → `{code:'HEAD_NOT_ON_MAIN'}`; else `null` | 36-48 (markers 37, codes 40/44/46) | MATCHES: `ops-invariants.md:24`, `SKILL.md:245-247` |
| `appendLedger` | appends `{ts, ...entry}` to `ledger/<kind>.jsonl`; if the serialized line exceeds **3500 bytes** it is replaced by a `{truncated:true, …}` stub recording `bytes` (POSIX `PIPE_BUF` atomicity guard) | 53-58 (cap 55) | MATCHES: `ops-invariants.md:25`, `SKILL.md:146`, `SKILL.md:246` |

`gitMutationBlocker` is the reason the live tree's stalled rebase blocks every
dispatcher git path (`fleet-dispatch.mjs:123, 216, 255, 354`).

## 8. Emitted telemetry + console strings (`fleet-dispatch.mjs`)

| Event | Emitted when | Line |
|---|---|---|
| `mission_dispatched` | pane spawned; carries `model`, `pane`, `experiment`, `adjusted_ev`, `freshness`, and `ev_note` only when `typeof ev === 'number' && ev < 0` | 201-205 |
| `mission_done` | terminal `DONE` **with** `deliverable`; carries `claims_commits` | 309-312 |
| `mission_parked` / `mission_failed` | terminal `PARKED` / any other terminal non-DONE state | 315 |
| `mission_failed` | tmux spawn failure (194); stale lease + dead pane (322); pane exited without terminal status → status overwritten `{state:'FAILED', detail:'pane exited'}` (327-328) | 194, 322, 327 |
| `claim_commit_blocked` | `gitMutationBlocker` non-null inside `commitClaims` | 125 |
| `claim_rejected` | claim-check exit ≠ 0 (last 400 chars of stdout kept) | 136 |
| `claim_commit_failed` | `git add` fail (144); `git commit` fail (153); no commit contains the bytes (161); bytes differ from selected commit (166) | 144-166 |
| `claim_push_blocked` | git blocker in `finalizePush` (218) or re-check before push (257) | 218, 257 |
| `claim_tag_rejected` | claim-check red at tag time (230); tag-bytes mismatch (235) | 230-235 |
| `claim_tag_conflict` | existing tag resolves to a different sha | 241 |
| `claim_tag_failed` | `git tag -a` failed | 248 |
| `claims_pushed` | `git push --atomic origin main + refs/tags/*` result recorded with `ok` | 261-262 |
| `model_reroute` | usage-limit fallback (282) or window flip (388) | 282, 388 |
| `fleet_sync_blocked` / `fleet_sync_failed` / `fleet_synced` | `--sync` periodic commit path | 356, 362-377 |
| `dispatcher_tick` | end of every tick, `{active, pending}` | 405 |

Console strings: `fleet-dispatch: <N> assignable programs, max <M>, stagger <S>s, model <model>[ (dry)][ (periodic sync enabled)]` (336) · `dry: would lease+launch …` (177) · `dispatched: <id> (pane <pane>, ufo_sighting:formation)` (206) · `claim-check REJECTED <id>/<slug> — not committed` (137) · `DONE: <id> -> claims commits <json>` (313) · `<STATE>: <id> — <detail>` (316) · `limit detected (<log>) — new launches on <model>` (283) · `window flip -> new launches on <model>` (389) · `tick: active <n>, pending <m>` (406) · `--once: missions running in tmux; next invocation sweeps` (407) · `queue exhausted — halt` (408) · `reconciled: <id> (<pane>)` (420).

## 9. Round-13 correction ledger (SUPERSEDES register)

Each row is a claim derivable from the named source that the round-13 audit
found stated differently — or not at all — in the corpus/SKILL. Every row was
landed as an in-place repair this round (marker: "round-13 correction"); the
Supersedes column names the audit-time target, not current text.

| # | Statement | Source basis | Supersedes |
|---|---|---|---|
| 9.1 | Dispatch score has **five** terms, not four — `is_live(1)` is part of the ordering (`fleet-dispatch.mjs:110`). | 110 | `SKILL.md:113-114` and `SKILL.md:175-176` omit it (both are summaries of this expression) |
| 9.2 | The `reward` term is `reward.min × 1000`, so the ordering tail is `… > reward.min×1000 > live(1)`, not `… > reward.min`. | 110 | `SKILL.md:175` writes `reward.min` |
| 9.3 | `curated` is a **boolean** on `Object.keys(ev_inputs).length > 0`; no EV magnitude is ever compared. The `buildQueue` header's "EV ordering (curated first …)" is doubly wrong: curated ranks **third**, behind priority and continue. | 10, 107, 110 | `fleet-dispatch.mjs:10` (in-file comment), `SKILL.md:10-11`-style "EV ordering" phrasing |
| 9.4 | `rec.ev_inputs?.adjusted_ev` (`fleet-dispatch.mjs:200`) can never be a number: `schema.json` `ev_inputs` is `additionalProperties:false` (34) with no `adjusted_ev` property (35-51), `ev-report.mjs` computes it without persisting (82), and 0 of 1088 program records contain the key (census §2.2). Consequence: every `mission_dispatched` line logs `adjusted_ev: "unknown"` and the negative-EV `ev_note` branch (204) is dead — AR12's "negative/unknown EV is ledgered honestly" is true only in the "unknown" direction. | 200-205, `schema.json:34-51` | `fleet-dispatch.mjs:11` (in-file comment), `mission-control.md:21-23` |
| 9.5 | `reward.min` numeric on **14** records; `reward` object on 48. | census §2.2 | `intake-surface.md:75-76` ("`reward.min` present on 48"), `SKILL.md:111` ("`reward` exists on 48" — true but conflated downstream) |
| 9.6 | Peak-window model is `openai-codex/gpt-6-astra:max`. | `fleet-dispatch.mjs:300` | `mission-control.md:37-38` (`openai-oauth/gpt-6-astra:max`) |
| 9.7 | Usage-limit signatures are four (incl. `usage_limit_reached`), ANDed with a family regex, tail-only, 15-min mtime window. | 271-278 | `mission-control.md:41-43` (three signatures) |
| 9.8 | `claim-check.mjs` never validates manifest `schema_version`, `provenance.json` pins/`policy_sha256`/`external_effects_performed`, `status.severity`, or `status.reward` — the tokens do not appear in the file. Those `claim-package-contract.md` rows are contract-by-convention. | grep of `claim-check.mjs` for `schema_version\|policy_sha256\|external_effects\|reward\|severity\|mission_id` → only `title` (183, 194) matches | `claim-package-contract.md:13,15,33-38` (implies gate-enforced) |
| 9.9 | Tier collision bound: `reward.min ≥ 1e9` breaks the priority/continue/curated separation (no guard). Observed max `reward.min` = 10000 → `1e7`, five orders under the curated tier. | 110 + census §2.2 | — |
| 9.10 | Pane-exit failures write `mission_failed` (327) and `attempts()` counts `mission_(parked\|failed)` (82), so two infra crashes exhaust a program's 2-attempt hunt budget. | 78-85, 325-328 | `mission-control.md:31-33` (notes budget counts it, not the infra-consumption consequence) |
| 9.11 | `report.md` "no submission" is a **prose phrase** regex (`/no submission (performed\|made)/i`, 29), distinct from the `no_submission_performed` JSON guard listed in observed statuses. | 29 | `claim-package-contract.md:27` |
| 9.12 | `HARD_STOP` emits two errors for one decision (its own message plus the `NO_SCOPE_OBJECTION` message). | 83-84 | `claim-gates.md:32-33` ("`HARD_STOP` gets its own message" — it gets both) |
| 9.13 | claim-check aborts the artifact loop on the first path/existence/symlink failure per artifact, and skips oversize files without scanning, so a single run's error set is path-dependent, not a full partition of violations. | 46-49, 111 | `claim-gates.md:5-6` (no-early-exit framing is accurate for the gate list, not per-artifact) |
| 9.14 | "~1040 records" contribute 0 or 1 points — the census says **1024** (796 zero + 228 one), plus 13 reward-band records at ≤1e7. | census §2.2 | `SKILL.md:115` |
| 9.15 | `priority.json` is a strict subset of the continue-verdict programs (14/14), so the 9e12 tier only orders *within* the continue cohort; it is not a disjoint class. | 90-96 + census §2.2 | — (new) |

## 10. Overlap register (MATCHES ties, consolidated)

| Prior claim | Location | Status |
|---|---|---|
| claim-check gate list + error-based discovery | `claim-gates.md:3-6, 8-74` | MATCHES (this entry adds exact trigger conditions, numeric bounds, and per-gate line numbers) |
| EV formula + UNKNOWN fail-closed | `ev-model.md:6-20`, `SKILL.md:494-506` | MATCHES (adds 6-decimal `fmt`, 10-input print order, exit-2 paths, non-persistence) |
| shared constants table | `ops-invariants.md:17-25` | MATCHES (adds exact marker list and the 3500-byte truncation stub shape) |
| queue score incl. `is_live(1)` | `intake-surface.md:68-79`, `mission-control.md:19-21` | MATCHES (both are correct; §9.1/9.5 supersede their census tail) |
| six-file package contract | `claim-package-contract.md:9-16, 28-38` | MATCHES for gate-enforced rows; §9.8 marks the convention-only rows |
| dispatcher runtime shape | `mission-control.md:13-46` | MATCHES except §9.6/9.7 |
| appendLedger 3500 B cap / gitMutationBlocker | `SKILL.md:146, 245-247` | MATCHES |
| `attempts() ≥ 2` as real termination | `SKILL.md:113-117` | MATCHES |

## Source basis

Read in full 2026-09-28 (line counts per `wc -l`; `fleet-dispatch.mjs` has an
unterminated final line, so `read` numbering shows 428):

- `~/Projects/bounties/ops/claim-check.mjs` — 233 lines
- `~/Projects/bounties/ops/ev-report.mjs` — 92 lines
- `~/Projects/bounties/ops/fleet-dispatch.mjs` — 427 lines
- `~/Projects/bounties/ops/shared.mjs` — 58 lines
- `~/Projects/bounties/bounty-map/schema.json` — 68 lines

Corpus files read for overlap: `claim-gates.md`, `ev-model.md`,
`ops-invariants.md`, `mission-control.md`, `intake-surface.md`,
`claim-package-contract.md`, `SKILL.md` (§Finding-triage decision table,
§Intake surface, §Triage economics, §Cited paths).

Read-only census commands (no writes to the bounty tree; programs,
`fleets/priority.json`, `docs/review-verdicts.jsonl`, `fleets/leases.json` read
only) produced §2.2; outputs quoted verbatim there. `[UNVERIFIED]`: nothing —
every numeric claim above carries a source line or a quoted command output.