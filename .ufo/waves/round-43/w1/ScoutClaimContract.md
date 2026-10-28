# ScoutClaimContract — JSON paths for R-FILES..R-NOSECRET

Seat: ScoutClaimContract. Frozen claims read, not edited: `.ufo/waves/round-43/claims.json`. Base `ab98fac9dce87130bc4f66de89e30650d63943dc`. No `lsp` device is mounted in this seat; the sources are markdown, not a typed schema. Key paths below are sentences in those files, not a language-server definition.

Axes: depth:verifiability (every path tagged with the sentence that states it), coverage (eight rules plus the round-13 fields the lost checker never read).

## How to read the tags

- **CONTRACT** — `corpus/knowledge/claim-package-contract.md` states the path or the value. Quote given.
- **LOST-CHECKER** — stated by `corpus/knowledge/claim-gates.md` and/or `corpus/knowledge/triage-thresholds.md` §4 as what `ops/claim-check.mjs` enforced. Not in the contract sentence.
- **C2** — stated only by the frozen C2 predicate, not by the contract.
- **UNSTATED** — neither the contract nor the lost checker names this JSON key. A gate that requires it is a convention this lane would be choosing. Say so in the instrument; do not describe it as parity with `claim-check.mjs`.

The lost trees are absent (this run: `~/Projects/bounties`, `~/projects/bounties`, `~/Projects/the-bounty-hunter`, `~/Projects/origin-work/open-bug-bounties` all ABSENT; no `claim-check.mjs` under `~/Projects` or `~/projects` within depth 6). Shapes are corpus-attested only.

C2's eight rules are a subset of the lost checker, plus four fields the lost checker never read. A gate that re-implements `claim-gates.md` in full is claiming parity the contract's round-13 note forbids, and it will reject the exemplar: C2 requires `claimable` to stay false.

## Do not claim parity — fields `claim-check.mjs` never read

Contract lines 18-26:

> Round-13 boundary note — not every row above is gate-enforced: `~/Projects/the-bounty-hunter/ops/claim-check.mjs` never reads the manifest `schema_version`, the provenance `pin`/`policy_sha256`/`external_effects_performed`, `status.severity`, or `status.reward` — the tokens do not occur in the file (the entire provenance gate is the :96-97 non-emptiness check). Those fields are contract-by-convention (reviewer/runbook-checked), not machine gates. The report.md "no submission" gate is a PROSE regex (`/no submission (performed|made)/i`, :29), distinct from the JSON `no_submission_performed` field.

`triage-thresholds.md` §4.5 (lines 236-242) is the same boundary: the only provenance check is `(steps ?? transitions ?? []).length === 0` AND falsy `agents`. No `schema_version`, `policy_sha256`, `external_effects_performed`, pin/`commit`, or per-transition models.

| Token the lost checker never read | In an r43 rule? | Gate scope |
|---|---|---|
| `evidence/manifest.json#/schema_version` | Yes, R-MANIFEST | New. Not parity. |
| `provenance.json` `pin` | Yes, R-PROVENANCE | New. Not parity. Key is named; shape is not unique (below). |
| `provenance.json#/policy_sha256` | Yes, R-PROVENANCE | New. Not parity. |
| `provenance.json#/external_effects_performed` | Yes, R-PROVENANCE | New. Not parity. Domain is empty array. |
| `status.json#/severity` | No | Leave unread. `claim-gates.md:113` uses it only in `prepare-claims.mjs`, not in claim-check. |
| `status.json#/reward` (`min`/`max`/`currency`) | No | Leave unread. `claim-gates.md:102` is the index column, not claim-check. |
| Provenance agents/models/commands beyond non-emptiness of `steps`/`transitions`/`agents` | Yes, R-PROVENANCE | The old gate's `:96-97` check is not this rule. Implementing only non-emptiness fails C2. |

Also not parity, the other direction: the lost checker enforces many status and sweep checks that **none** of the eight C2 sentences name. Putting them in a rule is a lane choice. The kill rule forbids reading bytes outside the package directory; the lost global duplicate scan (`claim-gates.md:82-84`, `triage-thresholds.md:278`) does that and must not be copied.

## R-FILES

Not JSON. Six paths relative to the package directory. Presence only.

| Path | Domain | Tag |
|---|---|---|
| `report.md` | file present | CONTRACT line 11, and the line 7 list. LOST-CHECKER `claim-gates.md:10-11`. |
| `claim_checklist.md` | file present | CONTRACT line 12. LOST-CHECKER same. |
| `custodian-receipts.json` | file present | CONTRACT line 14. |
| `provenance.json` | file present | CONTRACT line 15. |
| `status.json` | file present | CONTRACT line 16. |
| `evidence/manifest.json` | file present | CONTRACT line 13. LOST-CHECKER error is `missing evidence/manifest.json` (separate from `missing <f>`). |

C2 text: "the six contract files present". Nothing else.

Not this rule (do not hide inside R-FILES):

- `claim_checklist.md` marker `OPERATOR-GATED`. CONTRACT line 12: `carries "OPERATOR-GATED"`. LOST-CHECKER `/OPERATOR-GATED/i` (`claim-gates.md:16`). C2's rule sentence does not check it. C2's last sentence still requires the **exemplar** to name operator gates in `claim_checklist.md`. That is exemplar content, not an R-FILES verdict.
- Symlink-vs-regular-file. Unstated for presence. The lost blanket symlink ban is the secrets walk (`claim-gates.md:55-56`), not the presence check.
- `submit/BLOCKED.md`, `submit-payload.json`, `INGESTION.md`, `claim.json`. Anatomy D7 records packages that are not the six-file set. Not required by R-FILES.

## R-MANIFEST

File: `evidence/manifest.json`. C2: "schema_version, per-artifact sha256 over the bytes, polarity enum, at least one positive, relative paths inside the package with no symlink escape".

| JSON path | Domain | Tag |
|---|---|---|
| `#/schema_version` | string, exactly `evidence-manifest/v1` | CONTRACT line 13: `` `schema_version: "evidence-manifest/v1"` ``. Not an integer `1` (that is the lane's other manifests). LOST-CHECKER never reads it (boundary note). |
| artifact object `#/sha256` (parent key **UNSTATED**) | sha256 of that artifact's file bytes | CONTRACT: "Per-artifact sha256". LOST-CHECKER field name is `a.sha256` (`claim-gates.md:25-26`, `triage-thresholds.md:201`: `sha256File(ap) !== a.sha256`). Hex grammar `/^[a-f0-9]{64}$/i` is **not** stated for artifact digests (it is stated for custodian and status digests only). Requiring 64 lowercase/upper hex is a lane choice copied from those other checks. |
| artifact object `#/polarity` | string, exactly `positive` or `negative` | CONTRACT line 13: `` `polarity` ∈ {positive, negative} ``. LOST-CHECKER set is `{'positive','negative'}` with no case-fold (`triage-thresholds.md:202`). Case-folding would be a lane widening. |
| count of artifacts with `polarity == "positive"` | integer ≥ 1 | CONTRACT: "≥1 positive required". LOST-CHECKER: `manifest: claim package requires at least one positive-polarity artifact`. |
| artifact object `#/path` | relative to `evidence/`; resolved path stays inside the package; `realpath` stays inside the package | CONTRACT line 13: "Artifact paths are relative to `evidence/`, must stay inside the package, no symlink traversal." LOST-CHECKER algorithm (`claim-gates.md:21-23`): `resolve(dir,'evidence',a.path)` prefix `dir/`; path non-empty and file exists; `realpathSync` prefix `realDir/`. The `resolve`/`realpathSync` steps are the lost checker's procedure, not a contract quote. C2 repeats "relative paths inside the package with no symlink escape". |

**UNSTATED parent of the artifact objects.** No sentence in the contract, `claim-gates.md`, `claim-anatomy-sample.md`, `triage-thresholds.md`, `ufo-archive-2026.md`, or `SKILL.md` names `manifest.artifacts` or any other array key. This run counted `manifest.artifacts` = 0, `"artifacts"` = 0, `` `artifacts` `` = 0 in those files. The lost checker binds `a.path`, `a.sha256`, `a.polarity` and also reads object keys `sequence` and `expected_head_sha256`, so the file is a JSON object, not a bare array. The array key itself is not recorded. Choosing `artifacts` is a **lane convention**. Do not write it down as contract.

Not this rule:

- `#/sequence` number. LOST-CHECKER only (`claim-gates.md:20`). Absent from the contract and from the C2 sentence. Requiring it is lost-checker parity, not R-MANIFEST.
- `#/expected_head_sha256`. CONTRACT names it on the custodian row (line 14), and C2 puts the binding on **R-CUSTODIAN**, not R-MANIFEST. LOST-CHECKER requires the key present (`claim-gates.md:20`).
- `#/redactions` — that is R-REDACT, same file.

## R-REDACT

Same file: `evidence/manifest.json`. C2: "one same-digest redaction receipt per artifact with nonempty distinct producer and verifier".

| JSON path | Domain | Tag |
|---|---|---|
| `#/redactions` | array. `redactions: []` fails. | CONTRACT line 13: `` `redactions[]` `` and "`redactions:[]` is never claim-ready." Archive observation, not the contract table: receipts live at `manifest.redactions` (`ufo-archive-2026.md:106`). |
| `#/redactions[]/artifact_sha256` | equals that artifact's `#/sha256` | LOST-CHECKER (`claim-gates.md:25-26`). Contract says "same-digest" and does not name this key. |
| `#/redactions[]/scanned_artifact_sha256` | equals `#/redactions[]/artifact_sha256` and equals the artifact `#/sha256` | LOST-CHECKER only. Contract does not name the key. "Same-digest" is the contract concept; these two keys are the lost checker's encoding. |
| `#/redactions[]/producer` | non-empty string | CONTRACT: "nonempty, distinct producer/verifier identities." Key spelling `producer` is LOST-CHECKER (`triage-thresholds.md:206-207`). |
| `#/redactions[]/verifier` | non-empty string, ≠ `producer` | Same split. |

Lost-checker compare is trim-then-unequal (`triage-thresholds.md:204,206,207`). Trim is not in the contract sentence. Adopting trim is a lost-checker detail, small, but it is not the contract quote.

**"One" is ambiguous.** CONTRACT and C2 both say "one ... per artifact". The lost checker is weaker and stronger in different places: at least one receipt whose two digests equal `a.sha256` with distinct nonempty producer/verifier (`triage-thresholds.md:204`), every receipt's two digests equal each other (`:205`), and every receipt digest equals some artifact (`:208`, orphans fail). Extra receipts that do bind an artifact are not rejected. Exactly-one is the stricter reading of "one" and is **not** what `claim-check.mjs` enforced. Pick one and label it. This scout does not pick.

Not this rule: redaction files elsewhere (`evidence-dir.md` `redaction-policy.json`, `redaction-verification.json`, archive `redaction-scan-authorization.json`). The contract receipt is `manifest.redactions[]` only.

## R-CUSTODIAN

File: `custodian-receipts.json`. C2: "non-empty chain, every action's matched_grant_id nonempty and scope_signal exactly NO_SCOPE_OBJECTION, head_sha256 equal to the last decision digest and to manifest.expected_head_sha256".

| JSON path | Domain | Tag |
|---|---|---|
| `#/chain` | non-empty array | CONTRACT line 14 says "Non-empty decision chain" but does not backtick the key. C2 says "non-empty chain". LOST-CHECKER (`claim-gates.md:31`): `chain = receipts.chain ?? receipts.decisions ?? []` must be a non-empty array. |
| `#/decisions` | alternate array, same element domain | LOST-CHECKER only. Not in the contract sentence and not in the C2 sentence. Accepting it is lost-checker parity. Requiring only `#/chain` matches C2's word and is narrower than the lost checker. A bare array file (archive: github-nines, `ufo-archive-2026.md:98-99`) fails both. |
| `#/chain[]/action` | string; lost checker defaults missing to `(unnamed action)` | CONTRACT brace `{action, ...}` so the key is CONTRACT. C2 does not mention it. LOST-CHECKER does not require it nonempty (`triage-thresholds.md:228`). Requiring nonempty `action` is a lane tightening. |
| `#/chain[]/input_sha256` | unstated domain | CONTRACT brace includes `input_sha256`. C2 does **not**. LOST-CHECKER never checks it (absent from `claim-gates.md:31-37` and `triage-thresholds.md` §4.4). Requiring it enforces the contract brace, not C2 and not the lost checker. |
| `#/chain[]/decision_sha256` | LOST-CHECKER: `/^[a-f0-9]{64}$/i` | Key is CONTRACT (the brace, and "final decision digest"). Hex regex is LOST-CHECKER (`claim-gates.md:35`). |
| `#/chain[]/matched_grant_id` | nonempty after trim | CONTRACT line 14: "nonempty `matched_grant_id`". Trim is LOST-CHECKER (`triage-thresholds.md:221`). |
| `#/chain[]/scope_signal` | exactly `NO_SCOPE_OBJECTION` | CONTRACT line 14: `` exactly `"NO_SCOPE_OBJECTION"` ``. LOST-CHECKER compares uppercased/trimmed (`triage-thresholds.md:220`), so `no_scope_objection` passes the lost checker and fails a literal reading of the contract quotes. C2 says "exactly NO_SCOPE_OBJECTION". Literal match matches the contract quotes; case-fold matches the lost checker. Those are different. Say which. |
| `#/head_sha256` | equals `#/chain[-1]/decision_sha256` and equals `evidence/manifest.json#/expected_head_sha256` | CONTRACT line 14: "`head_sha256` == final decision digest == `manifest.expected_head_sha256`". LOST-CHECKER is that three-way binding, plus `head_sha256` matches `/^[a-f0-9]{64}$/i` (`claim-gates.md:36-37`, `triage-thresholds.md:223-225`). The hex regex is LOST-CHECKER. Archive defect: some receipts used `expected_head_sha256` as the receipt field, or bound `event_sha256` (`ufo-archive-2026.md:97-100`). Those keys are not the contract. |

Not this rule: `HARD_STOP` double error (`claim-gates.md:32-34`). Real lost-checker behavior. C2 only requires the exact signal, which already fails `HARD_STOP`. A second error string is parity theatre, not a C2 requirement.

`manifest.expected_head_sha256` domain: key presence is LOST-CHECKER; equality is CONTRACT. No contract sentence types it as 64 hex. The lost checker compares it to `head_sha256` after validating `head_sha256` only (`triage-thresholds.md:225`).

## R-PROVENANCE

File: `provenance.json`. C2: "agents and requested/resolved models, commands with exit codes, pin, policy_sha256, external_effects_performed empty, secrets attestation".

This is the rule where the contract is prose and the lost checker read almost none of it. Nested key names below that are not quoted are **UNSTATED**.

| JSON path | Domain | Tag |
|---|---|---|
| `#/policy_sha256` | sha256 string (hex grammar unstated) | CONTRACT line 15, backticked. Boundary note: lost checker never reads it. `SKILL.md:130` cites pendle `provenance.json:32-33` and hackenproof `provenance.json:36` as the observed key. Not re-read this round (tree absent). |
| `#/external_effects_performed` | array, exactly `[]` | CONTRACT line 15: `` `external_effects_performed: []` ``. C2: "empty". Lost checker never reads it. Non-empty fails. A missing key is not the empty array; failing closed on absence matches the contract's written `[]`. |
| `#/pin` | see four shapes | Boundary note names the token `pin`. CONTRACT line 15 says "pin (remote + commit)" without a JSON pointer. `SKILL.md:112-119`: four observed shapes of `provenance.json.pin`. |
| `#/pin/remote` | string | Only shape 1. `SKILL.md:114`: `{remote, commit, note}` at pendle `provenance.json:27-31`. `note` is observed, not in the contract. |
| `#/pin/commit` | 40-hex is an observation, not a contract domain | Shape 1. Round-1 audit (`corpus/lessons/round-1-aggregator-audit.md:38`) records pendle commit `f24265966bb53f75d834ad705decde8e479d3a33`. The contract says "commit", not 40 hex. |
| `#/pin` as a bare string | observed, does not satisfy "remote + commit" | `SKILL.md:114-115` wordpress `provenance.json:8`. |
| pin nested in `#/commands[]` | observed, path inside the command object unstated | `SKILL.md:116-117` anthropic `provenance.json:29`. |
| `#/pin` as a version string `"0.2.9"` | observed, not remote+commit | `SKILL.md:118-119` airtable `provenance.json:32`. |

Only shape 1 meets the contract words "remote + commit". Accepting shapes 2-4 is a lane choice to match observed drift, and it is not the contract. Anatomy D1's b1k `pin` is on **status.json**, not provenance (`claim-anatomy-sample.md:58-61`). Do not treat that as `provenance.pin`.

| Concept in the contract sentence | Attested JSON key | Tag |
|---|---|---|
| "Agents" | `#/agents` non-empty is the lost checker's third operand (`claim-gates.md:41`). No agent-object schema is recorded. | LOST-CHECKER for the key's existence as a non-emptiness check. Object fields UNSTATED. |
| "requested/resolved models per transition" | No provenance path. `requested_model` / `resolved_model` are attested only on `status.json#/claim_review/reviewer` (`claim-gates.md:72-73`). | Copying those names onto a provenance transition is a **lane convention by analogy**. |
| "per transition" | Lost checker accepts `#/steps` or `#/transitions` (`claim-gates.md:41`, `triage-thresholds.md:236`). | LOST-CHECKER alternate keys. Contract does not choose. Element schema UNSTATED. |
| "commands + exit codes" | `#/commands` is attested only as a place a pin can nest (`SKILL.md:116`). | `exit_code` count in the six files searched this run: 0. The exit-code key is **UNSTATED**. |
| "secrets attestation" | no key | CONTRACT line 15 "secrets attestation"; `SKILL.md:553` says "secrets sweep attestation" and still names no key. `secrets_attestation` count: 0. **UNSTATED.** The scan itself is R-NOSECRET, not this field. A gate that only runs the regex and never reads an attestation field has not implemented this clause. |

Lost-checker provenance rule, **not** C2: `(steps ?? transitions ?? []).length === 0` AND falsy `agents` → fail (`triage-thresholds.md:236`). That check passes a file that has `agents: ["x"]` and nothing else. C2 does not. Using it as R-PROVENANCE would miss pin, policy hash, empty external effects, models, commands, and the attestation.

## R-STATUS

File: `status.json`. C2: "manifest_sha256 binds the manifest bytes, claim_review holds hard_gates, subchecks and a reviewer with an identity distinct from every producer".

C2 also says the exemplar keeps `claimable` false. So this rule **must not** require `claimable === true`. The lost checker does (`claim-gates.md:68`). That single import makes the exemplar DEFECT and fails the frozen claim.

| JSON path | Domain | Tag |
|---|---|---|
| `#/manifest_sha256` | sha256 of the current bytes of `evidence/manifest.json`. LOST-CHECKER also requires `/^[a-f0-9]{64}$/i` (`triage-thresholds.md:264`). | Key and binding: CONTRACT line 16 "`manifest_sha256` binds status to manifest bytes." Hex regex: LOST-CHECKER. Anatomy: absent or null in 84/280 (`claim-anatomy-sample.md` D5). |
| `#/claim_review` | object | CONTRACT line 16. |
| `#/claim_review/hard_gates` | object present | CONTRACT line 16 "holds `hard_gates`". |
| `#/claim_review/hard_gates/written_scope` | key present. Value `PASS` is LOST-CHECKER, not C2. | CONTRACT lines 52-53 name the four keys and do not type the values. |
| `#/claim_review/hard_gates/authorization` | same | CONTRACT. |
| `#/claim_review/hard_gates/evidence_integrity` | same | CONTRACT. |
| `#/claim_review/hard_gates/no_duplicate_or_prior_submission` | same | CONTRACT. |
| `#/claim_review/subchecks` | object present | CONTRACT line 16. |
| `#/claim_review/subchecks/no_secrets` | key present. Value `PASS` is LOST-CHECKER. | CONTRACT line 54. |
| `#/claim_review/subchecks/operator_attribution` | same | CONTRACT line 54. |
| `#/claim_review/reviewer` | object | CONTRACT line 16. |
| `#/claim_review/reviewer/identity` | non-empty string | Contract says "distinct identity" without the pointer. Key `identity` is LOST-CHECKER (`claim-gates.md:72-74`). |
| distinct from producers | see below | C2: "distinct from every producer". |

**"Every producer" is wider than the only recorded compare.** LOST-CHECKER (`claim-gates.md:74`, `triage-thresholds.md:268`): `claim_review.producer_identity` ≠ `claim_review.reviewer.identity` (trim each, then exact). The key `producer_identity` is not in the contract's status row. CONTRACT line 34 says "producer never self-approves" and line 61 "reviewer distinctness", still without a path. Redaction `#/redactions[]/producer` is a different field. Reading "every producer" as the one `producer_identity` compare is a **narrowing** to the lost checker. Reading it as "reviewer identity equals no redaction producer and no producer_identity" is a **widening** the contract does not state. Either way, label it. The key the lost checker actually stores is `#/claim_review/producer_identity` (also anatomy D3, hyatt keys, `claim-anatomy-sample.md:75`).

Contract line 16 also says the reviewer has "requested/resolved model, fallback flag". C2's R-STATUS sentence does **not** repeat those. Key names, if enforced, are LOST-CHECKER not contract pointers:

| Path | Domain if the lane follows the lost checker | Tag |
|---|---|---|
| `#/claim_review/reviewer/role` | exactly `kx-reviewer` (case-sensitive) | LOST-CHECKER `claim-gates.md:72`. Not in the contract status row. Not in the C2 sentence. |
| `#/claim_review/reviewer/requested_model` | nonempty string | LOST-CHECKER. Contract concept only. |
| `#/claim_review/reviewer/resolved_model` | nonempty string | LOST-CHECKER. |
| `#/claim_review/reviewer/fallback` | boolean | LOST-CHECKER `typeof fallback === 'boolean'`. Contract "fallback flag". |
| `#/claim_review/outcome` | `APPROVED` case-insensitive | LOST-CHECKER `claim-gates.md:70`. Not C2. |
| `#/claim_review/claim_ready` | `true` | LOST-CHECKER. Not C2. CONTRACT line 34 pairs `APPROVED` with `claim_ready:true` for `DONE`, which is the claimable state, not the r43 exemplar. |

Not this rule, even though the lost checker fails the package without them (`claim-gates.md:67-91`):

- `#/state` === `DONE`. CONTRACT enum is `DONE|BLOCKED|SUBMITTED|PARKED` (lines 31-34) as observed semantics, and the lost checker allows only `DONE`. C2 does not. Exemplar is not a submission.
- `#/claimable` === `true`. Forbidden for the exemplar. CONTRACT line 42 defines the queue bit; anatomy: absent 241/280, true only 12/280.
- `#/finding_count` positive integer.
- `#/verdict` free text. CONTRACT lines 35-41: not an enum. 249 distinct / 280. Do not enumerate it.
- `#/do_not_submit`, `#/no_submission_performed`. CONTRACT line 46 calls them redundant guards. The report marker is R-REPORT, not this JSON field (boundary note lines 24-26).
- `#/severity`, `#/reward`. Never read by claim-check. Not in C2.
- Not-claimable heuristics, prior-submission, global duplicate, blockers, nested readiness (`claim-gates.md:78-91`). Global duplicate reads other packages: forbidden by the C2 kill rule.

`#/claim_review/hard_gates/*` value `PASS` (uppercased, `triage-thresholds.md:269`) is LOST-CHECKER. C2 says the object "holds" the keys. Requiring `PASS` can still coexist with `claimable: false`, but it is not what C2 wrote. Anatomy D3: a `claim_review` can exist with keys `blocker_codes, claim_ready, outcome, producer_identity, reviewer` and no `hard_gates`/`subchecks`. R-STATUS as written fails that shape. Good.

## R-REPORT

File: `report.md`. Prose, not JSON. C2: "report.md carries `Scope excerpt`, the verbatim marker `No submission performed`, and every artifact's sha256 it cites".

| Check | Domain | Tag |
|---|---|---|
| Phrase `Scope excerpt` | CONTRACT line 11 quotes `"Scope excerpt"`. LOST-CHECKER is `/scope excerpt/i` (`claim-gates.md:15`), a case-insensitive substring, not a heading level. | Case-insensitive substring is the lost checker. The contract capitalization is the quoted phrase. C2 backticks `Scope excerpt`. |
| Marker `No submission performed` | CONTRACT line 11: `literal marker "No submission performed"`. C2: "verbatim marker". | LOST-CHECKER is a **different** pattern: `/no submission (performed\|made)/i` (`claim-gates.md:15`, contract lines 24-26). That accepts `no submission made` and any case. Implementing the regex is not implementing the literal, and it is the thing the boundary note separates from `#/no_submission_performed`. The r43 rule follows the literal, not the regex. |
| Every artifact sha256 cited in the report | **UNSTATED grammar** | C2 only. The contract's report sha256 is the scope-excerpt "content sha256" (line 11), which is policy-text digest prose, not "every artifact". No corpus sentence says how a citation is recognized (bare 64-hex, case, backticks, labeled). A "the artifact's recorded sha256 occurs in report.md" rule is a lane encoding of the C2 phrase. |

Not this rule: the rest of the report row (title, program URL, vuln class, repro, impact, asset, fix, timeline). CONTRACT line 11. None of it is in the C2 sentence. "repro steps without secrets" is the contract's report-local secret rule; the package-wide scan is R-NOSECRET.

JSON `#/no_submission_performed` is not this rule (contract lines 24-26).

## R-NOSECRET

Not a JSON path. C2: "no secret-shaped token in any package text".

The only recorded pattern is LOST-CHECKER, not the contract (`claim-gates.md:45-50`):

```
/(api[_-]?key|secret|token|password|bearer)\s*[:=]\s*["']?[A-Za-z0-9_\-]{16,}/i
```

Walk: every non-symlink file ≤ 5 MiB (`5 * 1024 * 1024` = 5242880 bytes), read as UTF-8, no text/binary filter (`claim-gates.md:45-47`, `triage-thresholds.md:249-255`). A hit errors. A bare 16-char token with no `:` or `=` does not.

| Piece | Tag |
|---|---|
| The regex | LOST-CHECKER. The contract never states it. C2 says "secret-shaped" and does not quote the regex. Using this regex is adopting the only recorded pattern, and it must be labeled as that, not as a contract quote. |
| "any package text" | C2. Wider than CONTRACT line 11, which limits "without secrets" to repro steps. |
| ≤ 5 MiB skip, and the oversize error | LOST-CHECKER (`claim-gates.md:57-58`). Not in the C2 sentence. Folding it into R-NOSECRET is a lane choice. The skip means oversize files are **not** scanned (`triage-thresholds.md:250`). |
| Blanket "any symlink errors" | LOST-CHECKER (`claim-gates.md:55-56`). Not R-NOSECRET's sentence. Distinct from R-MANIFEST's artifact `realpath` confinement. |
| Following a symlink to bytes outside the package | Forbidden by the C2 kill rule ("the gate reading package bytes from outside the package directory"), whether or not the blanket ban is adopted. |

`#/claim_review/subchecks/no_secrets == "PASS"` does not satisfy R-NOSECRET. That is a status flag (R-STATUS, and only if the lane requires `PASS`). The scan is the rule.

## Exemplar constraints that are not rule ids

From the C2 predicate, still binding on the package the gate must accept:

- `status.json#/claimable` is false. Not an R-STATUS pass condition.
- `claim_checklist.md` names the operator gates (contract marker `OPERATOR-GATED` is the recorded spelling).
- The report's verbatim marker is the negative of "naming a submission performed" (kill rule). Do not let the report say a submission was performed. The positive literal is `No submission performed`.

## Confidence

- High: every CONTRACT and LOST-CHECKER row cited to a file line above. Those lines were re-read this run; the quotes sit in the tables. The command section records source hashes and the unstated-key counts, not a second copy of the quotes.
- High: the six never-read tokens, the `claimable: true` clash with the exemplar, and the prose-regex vs literal-marker split.
- Medium: `redactions[]` element keys `producer` / `verifier` / `artifact_sha256` / `scanned_artifact_sha256`. The behavior is quoted; the contract itself only says "same-digest" and "producer/verifier identities".
- Low, and unresolved: artifact array key; provenance transition object; command and exit-code keys; secrets-attestation key; report sha256 citation grammar; exactly-one vs at-least-one redaction; whether "every producer" includes redaction producers; which of the four `pin` shapes R-PROVENANCE accepts. None of these can be closed without either a lane convention or the lost trees, which are absent.

## Commands (this run)

Source hashes and the unstated-key counts, from the Python reads in this seat:

```
sha256 2233cd0637a69c11d8130cfaeaf2f7ee22a196582a02abcddcc0d1980b5ea29d bytes 5169 corpus/knowledge/claim-package-contract.md
sha256 06e2bd5c485366b599774467d38f5870e6c8e1742a2dde89740172cd1b2987d8 bytes 6742 corpus/knowledge/claim-gates.md
sha256 bc33e8cb235f5a4e6549ac4745d65eddbea7ccebaf4f789cb66e9a49dc9df791 bytes 10517 corpus/knowledge/claim-anatomy-sample.md
sha256 5c0f4d4f3a180a91f08513bd4f1df66269877d9d039ef9de19988e21d2cf1c2b bytes 44953 corpus/knowledge/triage-thresholds.md
sha256 9eef84d163173c8e840732458d70b5c14050289cbf0c4f0d2414780a74f92b57 bytes 116310 SKILL.md
/home/vgpnk/Projects/bounties ABSENT
/home/vgpnk/projects/bounties ABSENT
/home/vgpnk/Projects/the-bounty-hunter ABSENT
/home/vgpnk/Projects/origin-work/open-bug-bounties ABSENT
FOUND
(no claim-check.mjs)
manifest.artifacts 0
"artifacts" 0
artifacts[] 0
`artifacts` 0
exit_code 0
secrets_attestation 0
scanned_artifact_sha256 3
```

`claim-gates.md:41` is the whole provenance gate: `` `steps`/`transitions`/`agents` — at least one non-empty. ``

No tools installed. No scratch left behind (none created; reads were in-process).
