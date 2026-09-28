# Policy access playbook (per platform)

Source: `~/Projects/bounties/fleets/mission-template.md` ("Policy access
playbook"), `docs/autopsies/*.md`, `claims/bugcrowd-seek/honest-zero/evidence/`.
Read 2026-09-28.

| Platform | Observed reality | Correct move |
|---|---|---|
| HackerOne | HTML page is a JS shell; `/policy` can 403 unauthenticated (figma autopsy) | Public GraphQL `team(handle)` for policy/scope/structured_scopes — no auth. Verified path per mission template. |
| Bugcrowd | Auth-walled SPA shell for anonymous fetch; embedded brief sometimes yields rating prose but no target table (seek, openai, spacex autopsies) | Try public brief/changelog JSON once (`engagement_known_issues.json` 401, brief doc 404 patterns observed); if no in-scope asset list → park at SCOPED. Do not retry HTML. |
| Immunefi / Cantina / HackenProof | Public bounty pages carry real scope (deployments JSON keys, whitelist rules) | Capture page into `evidence/`; bind via `policy_sha256` in `provenance.json` (pendle package). |
| RFC 9116 security.txt | Stub ≠ scope | No assets + no grant → park. |
| Terms-gated policy | SIX Group: reading Program Rules requires terms acceptance | Terms acceptance is a forbidden external effect → autopsy + retire, not a workaround (`docs/autopsies/hackerone-six-group.md`). |

## Scope-snapshot rules

- Generic invitation prose ("we invite the security researcher community to
  test…") does NOT bind an asset. SEEK example: `testing_grant_verbatim`
  non-empty but `in_scope_assets:[]` → `stop_reason:
  PUBLIC_BRIEF_INCOMPLETE_NO_EXACT_ASSETS`.
- `in_scope_assets:[]` records "not observed in this response", never "program
  has no scope" (`submit/BLOCKED.md`, bugcrowd-seek).
- Record volatile-field redactions: seek snapshot replaced 5 anti-CSRF/nonces
  with fixed markers and hashed the sanitized bytes (`content_hash_basis`).
- Grant fields (`authorization-envelope.json`): actor, asset, action, purpose,
  impact_ceiling, data_classes, time_window, credential_policy,
  `external_effect_authorization` (null unless operator preauthorized).
