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
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md
restoration-recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-gates.md  # on-restoration — fails closed today: base absent since 2026-09-28; not re-verifiable; re-scope is L0 kasegi round-15

## Re-ground (round 46)

The current claims of this entry are only the rows of the table below (G24 and G25 are witnesses, not entry claims). The committed gate is a round-43 re-implementation written from this entry (`corpus/instruments/claim-package-check.py:4-8` says it derives from `claim-gates.md`, and that the lost `claim-check.mjs` was documentation-only for this lane), so the rows show that the committed gate implements the gate list this entry states; they do not show that the lost checker enforced it. each restates one claim the entry makes (entry line in parentheses) and is anchored on committed bytes, the round-43 re-implementation `corpus/instruments/claim-package-check.py` and its fixtures. Where the committed gate is narrower than the entry's wording the row says what the committed bytes say and is marked narrowed; every other line of this entry (the lost checker's source description, the gate list outside this table, the claim-index and prepare-claims notes, and the round-22 provenance block) is a recorded observation of a lost tree ([lost-tree] the bounties lane's `ops/claim-check.mjs`, verified 2026-09-28), no longer re-verifiable, and never to be read as a current claim.

| id | current claim | committed anchor | token |
|---|---|---|---|
| G1 | Required: `report.md`, `claim_checklist.md`, `custodian-receipts.json`, `provenance.json`, `status.json`, `evidence/manifest.json` (L10-11) | `corpus/instruments/claim-package-check.py:101-108` | `'custodian-receipts.json',` |
| G2 | `sequence` is a number (L20) | `corpus/instruments/claim-package-check.py:307-309` | `isinstance(sequence, (int, float))` |
| G3 | Every artifact's `polarity` is `positive` or `negative` (L23) | `corpus/instruments/claim-package-check.py:332-335` | `elif artifact.get('polarity') != 'negative':` |
| G4 | Every artifact's `sha256` matches the bytes it resolves to (L23) | `corpus/instruments/claim-package-check.py:340-347` | `actual = hashlib.sha256(handle.read()).hexdigest()` |
| G5 | At least one positive-polarity artifact (L24) | `corpus/instruments/claim-package-check.py:354-355` | `if positive < 1:` |
| G6 | Each artifact's redaction receipt has `artifact_sha256` = `scanned_artifact_sha256` = the manifest digest (L25-26) | `corpus/instruments/claim-package-check.py:407-409` | `first.lower() == second.lower() == recorded.lower()` |
| G7 | Each redaction receipt's producer and verifier are nonempty and distinct (L26-27) | `corpus/instruments/claim-package-check.py:413-416` | `producer.strip().casefold() == verifier.strip().casefold()` |
| G8 | Every decision's `scope_signal` is exactly `NO_SCOPE_OBJECTION` (L32-33) | `corpus/instruments/claim-package-check.py:460-461` | `decision.get('scope_signal') != 'NO_SCOPE_OBJECTION'` |
| G9 | `head_sha256` equals `manifest.expected_head_sha256` (L36-37) | `corpus/instruments/claim-package-check.py:469-472` | `if head.lower() != head_expected.lower():` |
| G10 | `head_sha256` equals the final decision's `decision_sha256` (L36-37) | `corpus/instruments/claim-package-check.py:465-467` | `head.lower() != final_digest.lower()` |
| G11 | `status.json` `manifest_sha256` = sha256 of the current `evidence/manifest.json` bytes (L69) | `corpus/instruments/claim-package-check.py:584-589` | `actual = hashlib.sha256(manifest_bytes).hexdigest()` |
| G12 | `claim_review.reviewer` has a nonempty identity, nonempty requested and resolved models, and a boolean `fallback` (L72-73); narrowed: the committed gate does not check `role === 'kx-reviewer'` (left historical below) | `corpus/instruments/claim-package-check.py:598-606` | `if not isinstance(reviewer.get('fallback'), bool):` |
| G13 | Reviewer identity differs from the producer identity (L74); narrowed to: differs from every producer and verifier named in the redaction receipts | `corpus/instruments/claim-package-check.py:607-608` | `if identity.strip().casefold() in _identities(manifest):` |
| G14 | Hard gates `written_scope`, `authorization`, `evidence_integrity`, `no_duplicate_or_prior_submission` all `PASS` (L75-76); narrowed to: all `PASS` only when `claimable` is true, otherwise key presence only | `corpus/instruments/claim-package-check.py:594-613` | `failing = [key for key in HARD_GATE_KEYS if hard.get(key) != 'PASS']` |
| G15 | Subchecks `no_secrets`, `operator_attribution` all `PASS` (L77); narrowed the same way as G14 | `corpus/instruments/claim-package-check.py:595-614` | `failing += [key for key in SUBCHECK_KEYS if subchecks.get(key) != 'PASS']` |
| G16 | `claimable === true` requires a `finding_count` that is a positive integer (L68); narrowed: applied only when `claimable` is true | `corpus/instruments/claim-package-check.py:617-619` | `if isinstance(count, bool) or not isinstance(count, int) or count < 1:` |
| G17 | A bare labelled `api_key`, `secret`, `token` or `password` followed by `:` or `=` and 16 or more token characters is a secret hit (L48); narrowed: the committed label is word-bounded, so compound labels such as `GITHUB_TOKEN=` or `client_secret:` are not hits, and the entry's `bearer` followed by `:` or `=` is not checked (the committed bearer pattern at line 138 is `bearer` plus whitespace plus a token) | `corpus/instruments/claim-package-check.py:138-140` | `('credential', re.compile(rb'(?i)` |
| G18 | Any directory entry that is a symlink errors, and the walk does not traverse it (L54-55) | `corpus/instruments/claim-package-check.py:656-660` | `os.walk(pkg.root, followlinks=False)` |
| G19 | Files over `5 * 1024 * 1024` bytes are oversize and their secrets scan is skipped (L57-58) | `corpus/instruments/claim-package-check.py:672-674` | `if st.st_size > MAX_SCAN_BYTES:` |
| G20 | Each artifact path resolves inside the package, with a realpath escape check (L21-23) | `corpus/instruments/claim-package-check.py:185-187` | `if real != root and not real.startswith(root + os.sep):` |
| G21 | `report.md` matches a scope-excerpt marker, case-insensitively (L15 writes `/scope excerpt/i`); narrowed to: the committed regex is whitespace-tolerant `scope\s+excerpt` | `corpus/instruments/claim-package-check.py:120` | `re.compile(r'scope\s+excerpt', re.IGNORECASE)` |
| G22 | `report.md` contains the no-submission marker (L15); narrowed to: the committed gate requires the literal `No submission performed` and no other wording | `corpus/instruments/claim-package-check.py:121` | `NO_SUBMISSION = 'No submission performed'` |
| G23 | `provenance.json` has at least one non-empty array among `steps`, `transitions`, `agents` (L41); narrowed to: the committed gate requires a non-empty `agents` list | `corpus/instruments/claim-package-check.py:489-491` | `if not isinstance(agents, list) or not agents:` |
| G24 | Witness (a label only): the committed defect fixture `defect-8-marker` names `R-REPORT` as its expected rule; the entry's marker gate (L15) is covered by that one fixture and the label is not itself gate output | `corpus/instruments/fixtures/claim-package/defect-8-marker/expected-rule:1` | `R-REPORT` |
| G25 | Witness (a label only): the committed defect fixture `defect-9-secret` names `R-NOSECRET` as its expected rule; the witnessed secret shape is not the entry's own labelled regex (see G17) | `corpus/instruments/fixtures/claim-package/defect-9-secret/expected-rule:1` | `R-NOSECRET` |

Claims left historical (no committed check, or the committed check says the opposite): `claim_checklist.md` must match `OPERATOR-GATED` (L16); the `made` alternative of the no-submission marker (L15, narrowed in G22); the `steps` and `transitions` alternatives of the provenance gate (L41, narrowed in G23); the `bearer` labelled pattern as the entry writes it in one regex (L48); the error-set caveat (L59-61); the `triage-thresholds.md` section 4 pointer (L63); every status.json gate not listed as a row (L67-91), including `state === 'DONE'`, `claim_review.outcome === 'APPROVED'`, `claim_ready`, `producer_identity`, the `kx-reviewer` role, the not-claimable heuristics (the committed gate accepts `claimable: false` with a named blocker, the reverse of the entry), the prior-submission guard and its global scan, the blocker fields and the nested readiness contexts; the HARD_STOP double-error message (L32-34); the `claim-index.mjs` and `prepare-claims.mjs` notes (L93-119). Witness rows G24-G25 show that the committed fixtures name a rule; the gate's behaviour is attested by the rule rows and by the per-entry run of the round-46 counter, not by the fixtures.
