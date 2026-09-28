# Retirement lane — disposition classifier + autopsy contract

Source: `~/Projects/bounties/ops/park-disposition.mjs` (80 lines, read in
full), `docs/autopsies/` (31 files, all read), `fleets/mission-template.md`
line 23 (park-at-SCOPED grant), `fleets/run/*.status.json` live re-census.
Read 2026-09-28.

## Producer: `ops/park-disposition.mjs`

`node ops/park-disposition.mjs [--apply]` — dry-run default; `--apply` acts.
Operator decree 2026-09-05: RETRY what has a live path, RETIRE what is
structurally blocked. Iterates every `fleets/run/*.status.json` whose
`state` is `PARKED` or `FAILED` and regex-classifies `st.detail` — the
first match wins:

```
HONEST  /honest.zero/i                                   → LEARNED  (no action — honest park is terminal-good)
H1SPA   /scope unverifiable.*hackerone|hackerone.*SPA|
        content-negotiated to RFC 9116|security\.txt stub/i → RETRY_METHOD (GraphQL path exists)
AUTH    /auth-walled|requires login|SPA login|accept_terms|
        account creation|AUTH_UNVERIFIED|in_scope_assets empty|
        SPA shell|login-walled|no testing grant|testing paused|
        requires agreement|privacy hard stop|forbidden|
        prohibited personal-data|not in publi/i          → RETIRE_AUTH
TRANSIENT /unreachable|timeout|HTTP 5\d\d|ECONN|ENOTFOUND|
        DNS|network/i                                    → RETRY_TRANSIENT
else                                                     → REVIEW (no action)
```

- RETRY_* (`RETRY_METHOD` + `RETRY_TRANSIENT`): telemetry
  `attempt_reset` + `mission_unparked`, then `rm` the status file — the
  queue re-dispatches on the current window model.
- `RETIRE_AUTH`: writes `docs/autopsies/<id>.md` (name/URL pulled from
  `bounty-map/programs/<id>.json`), rewrites the status to
  `state:"RETIRED"` with `detail: retired: RETIRE_AUTH — see
  docs/autopsies/<id>.md`, emits `mission_retired` telemetry.

## Autopsy schema (generated, five fixed parts)

```markdown
# Mission autopsy — <name> (<program-id>)
**Outcome:** RETIRED (structurally blocked)
**Program URL:** <rec.official_url>
**State at retirement:** <prior state>
**Reason (verbatim):** <status detail, verbatim>
## Why it could not succeed autonomously      ← boilerplate, see caveat
## Unlock prerequisite                        ← operator session/token, or
## Evidence                                    ← evidence/<id>/ pointer
```

Requeue procedure is spelled inside the artifact: operator provides an
authenticated session/Read token (or the program publishes a public policy
page), then **delete both** `docs/autopsies/<id>.md` **and**
`fleets/run/<id>.status.json` — either file left behind keeps the program
out of the queue.

**Boilerplate caveat:** the "Why" paragraph is template text asserting an
account-login wall. It is verbatim-accurate for the SPA-shell majority but
misleading for the two real sub-causes below — read `Reason (verbatim)`
for the actual cause, never the boilerplate.

## The 31 autopsies — sub-cause partition

Source: `grep "Reason (verbatim)" docs/autopsies/*.md`, read 2026-09-28.
Outcome is `RETIRED (structurally blocked)` in all 31.

| Sub-cause | Count | Representatives |
|---|---:|---|
| Auth-walled/SPA shell: no `in_scope_assets` in public HTML; changelog brief 404 or engagement JSON 406 | 27 | `bugcrowd-openai`, `bugcrowd-spacex`, `bugcrowd-okta`, `hackerone-elastic`, `hackerone-figma`, `hackerone-greenhouse`, `bugcrowd-sap-private-invite` |
| Terms-gated policy: reading requires accepting Program Rules (forbidden external effect) | 1 | `hackerone-six-group` |
| Privacy hard stop: prohibited personal-data identifiers surfaced in pre-existing registry metadata | 1 | `hackerone-airtable` |
| Paused/non-enumerable scope: `engagement in_progress_paused` (`blockopensource`) or non-enumerable "all internet-facing assets" (`sky-plc-mbb-og2`, signup forbidden) | 2 | `bugcrowd-blockopensource`, `bugcrowd-sky-plc-mbb-og2` |

Platform split: 26 bugcrowd / 5 hackerone — the H1 cohort predates the
GraphQL `team(handle)` workaround now in `policy-access-playbook.md`; those
four (`elastic`, `figma`, `greenhouse` + `six-group` terms gate) are the
ones a provisioned H1 session could un-park today.

## Regex-drift finding (live, 2026-09-28)

Re-running the exact classifier over today's `fleets/run/` (646 PARKED +
0 FAILED at census, `ls fleets/run/*.status.json | wc -l` → 703 total):

| Class | Count |
|---|---:|
| LEARNED | 529 |
| REVIEW (no action) | 85 |
| RETIRE_AUTH | 30 |
| RETRY_METHOD | 1 |
| RETRY_TRANSIENT | 1 |

The 85 REVIEW are almost all the same structural block in **newer
wording** the regex doesn't know: "no exact in-scope assets",
"active-testing grant", "policy body unavailable", "login links",
"custodian HARD_STOP", "SCOPE_UNVERIFIABLE". Keyword-level census of the
85: ~31 `scope unverifiable`-family, ~28 same-meaning paraphrases
("login shell", "no verifiable asset list"), ~14 custodian/hard-stop
variants, ~9 honest-negative prose, ~3 program-inactive.

**Operational consequence:** `status.detail` is a machine-consumed field,
not free prose. A mission-L1 wording its park reason without a keyword
from the AUTH/HONEST/H1SPA tables parks *invisibly* — RETIRE_AUTH never
fires, the program sits PARKED forever instead of getting an autopsy or
an unpark. Two valid fixes: write detail strings containing a classifier
keyword (e.g. literal `in_scope_assets empty`, `no testing grant`,
`auth-walled`), or extend the regexes. The current corpus-side rule:
**when parking a mission, include at least one AUTH-table keyword
verbatim in `detail`** or the disposition pass will no-op on you.

## Failure signatures worth recognizing on first contact

Read the unauthenticated policy surface once (AR14 grant); retire without
a second fetch when you see:

- React/SPA shell + `/engagements/<slug>.json` → HTTP 406 or changelog
  brief 404 → Bugcrowd auth wall; park at SCOPED, do not burn fetches.
- H1 `/policy` → 403 `sign_in` + `<slug>.json` 404 + security.txt stub →
  try public GraphQL `team(handle)` once (policy/scope/structured_scopes,
  no auth); if that also yields no assets → autopsy class.
- "Accept Program Rules" interstitial (SIX Group) → terms acceptance is a
  forbidden external effect → autopsy + retire, same day.
- Personal-data identifiers in scope metadata (airtable) → privacy hard
  stop → autopsy; do not "work around" it.
- `engagement in_progress_paused` announcement → no testing grant exists →
  autopsy sub-cause "paused", not a retry.
