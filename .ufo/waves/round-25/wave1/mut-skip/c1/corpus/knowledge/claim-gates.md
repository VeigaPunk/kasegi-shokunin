# claim-check.mjs — the complete gate list

Source: `~/Projects/bounties/ops/claim-check.mjs` (233 lines, read in full
2026-09-28; tag `014A`). Exit 1 + `claim-check: FAIL (N errors)` on any gate;
`OK` only when zero errors. This replaces the "gates known only via error
strings" gap.

## File-presence gates

Required: `report.md`, `claim_checklist.md`, `custodian-receipts.json`,
`provenance.json`, `status.json`, `evidence/manifest.json` (L22–24).

## Content-marker gates

- `report.md` must match `/scope excerpt/i` AND `/no submission (performed|made)/i` (L28–29).
- `claim_checklist.md` must match `/OPERATOR-GATED/i` (L32).

## Manifest gates (L39–71)

- `sequence` is a number; `expected_head_sha256` key present.
- Every artifact: resolves inside package (`resolve(dir,'evidence',a.path)`
  prefixed by `dir/`); exists; `realpathSync` stays inside realDir (symlink
  escape check); sha256 matches; `polarity` ∈ {positive, negative}.
- ≥1 positive-polarity artifact.
- Every artifact needs a redaction receipt with `artifact_sha256 ===
  scanned_artifact_sha256 === a.sha256` AND nonempty distinct producer/verifier.
- Every receipt must bind a manifest artifact digest; producer ≠ verifier.

## Custodian gates (L74–93)

- `chain`/`decisions` non-empty array.
- Per decision: `scope_signal` exactly `NO_SCOPE_OBJECTION` (any other value
  errors; `HARD_STOP` gets its own message AND the exact-signal message —
  two errors for one decision, L83-84, round-13 correction); nonempty `matched_grant_id`;
  `decision_sha256` matches `/^[a-f0-9]{64}$/i`.
- `head_sha256` = final decision's `decision_sha256` =
  `manifest.expected_head_sha256` — three-way binding.

## Provenance gate (L97)

`steps`/`transitions`/`agents` — at least one non-empty.

## Secrets gate (L100–114)

Regex over every non-symlink file ≤5 MiB in the package, read as UTF-8 —
no text/binary filter (round-13 correction: "every text file" was wrong;
L110-113):
`/(api[_-]?key|secret|token|password|bearer)\s*[:=]\s*["']?[A-Za-z0-9_\-]{16,}/i`.
Any hit errors. Note: it is a single permissive pattern — real secret hygiene
still needs judgment beyond the gate.

Same walk loop, non-regex gates (round-13 addition — omitted from earlier
lists here and in SKILL.md):
- **Blanket symlink ban**: any directory entry that is a symlink errors
  without traversal (L104-105) — separate from the manifest-artifact
  `realpathSync` confinement (L48-49).
- **Per-file size cap**: files > `5 * 1024 * 1024` B error as `oversize
  artifact (>5MB)` and skip the secrets scan (L111).
- Error-set caveat: the manifest loop `continue`s past a failing artifact
  (L46-49), so one run's error list is path-dependent, not a full partition
  of violations — while gate-level flow never exits early (L18-19, 228-231).
- Canonical per-gate derivation (triggers, error strings, line numbers,
  constants): `corpus/knowledge/triage-thresholds.md` §4 (round-13).

## status.json gates (L118–226)

- `state === 'DONE'` (anything else fails, incl. SUBMITTED).
- `claimable === true`; `finding_count` positive integer.
- `manifest_sha256` = sha256 of current `evidence/manifest.json` bytes.
- `claim_review.outcome === 'APPROVED'` (case-insensitive) and
  `claim_ready === true`; nonempty `producer_identity`.
- `claim_review.reviewer`: `role === 'kx-reviewer'` exactly, nonempty
  `identity`, `requested_model`, `resolved_model`, `fallback` is boolean.
  Reviewer identity ≠ producer identity.
- Hard gates all `PASS`: `written_scope`, `authorization`,
  `evidence_integrity`, `no_duplicate_or_prior_submission`.
- Subchecks all `PASS`: `no_secrets`, `operator_attribution`.
- Not-claimable heuristics (any triggers error): `claimable===false`,
  `not_claimable`, `do_not_submit`, `claimability_gap`,
  `finding_count===0`, verdict matching `/not[-_\s]?claimable|honest[-_\s]?zero/i`.
- Prior-submission guard: `submission_performed`, `submitted_url`, or
  `submission_state:'SUBMITTED'` fails; PLUS a **global** scan of all
  `claims/*/*/status.json` — any other package with the same slug or same
  title (≥16 chars, lowercase compare) that has a submission record errors as
  duplicate (L184–199).
- Blocker fields: `blocked_reason`, `submission_blocker`, `blocking_record`,
  or `submit/BLOCKED.md` existing → error.
- Nested readiness: `claim_review`, `claim_wave`, `claim_attempt`,
  `submission` contexts — `outcome`/`state` = BLOCKED, `claim_ready===false`,
  `submission_ready===false`, or non-empty `blocker_codes`/`blockers`/
  `remaining_gates` → error.

## claim-index.mjs (operator queue, `docs/claim-ready-index.md`)

Scans every `claims/*/*/status.json`; only `state:'DONE'` packages are
re-checked via claim-check. Errors ranked for display: prior-submission /
duplicate / not-claimable / state errors rank 0 (shown first), custodian/
manifest rank 1, rest rank 2; first 5 shown, rest `+N more gate error(s)`.
`claim-ready/*` tags are provenance only — a tag whose package fails current
bytes lands in "Historical tags blocked" (`claim-ready/<program>/<slug>`,
3 parts or INVALID_TAG). Queue columns: program, title (+ first `#` heading
from report.md, 140 chars), reward (`status.reward{min,max,currency}` or
`(see package)`), `claim_url`.

## prepare-claims.mjs (`submit-payload.json` staging)

- Only `DONE` packages that pass claim-check.
- Route: `status.submission_url ?? claim_url` must parse as explicit `https:`.
- Attachments = `claim_checklist.md` (round-13 correction: earlier text said
  `claim_checklist.json`; prepare-claims attaches the `.md`) + positive-polarity manifest artifacts
  (resolved inside package, deduped). Negative artifacts never attach.
- Payload fields: program, slug, platform (hostname), route, title (first `#`
  of report.md else status.title), `severity: status.severity ?? verdict`,
  `reward_band` from `status.reward`, `body_source`, `package_manifest_sha256`,
  `submit_state:'STAGED — operator-gated'`.
- Immutable-after-review: if `submit-payload.json` is itself a manifest-bound
  artifact and bytes differ → skip (changed bytes require re-review).
- Post-write: claim-check re-runs; on failure the original payload bytes are
  restored (or the file removed). Deterministic: writes only when bytes differ.

## Provenance (round-22 correction, appended)

source: [lost-tree] ~/Projects/bounties/ops/claim-check.mjs:1-233, tag 014A; full round-3 source read.
verified-at: 2026-09-28
