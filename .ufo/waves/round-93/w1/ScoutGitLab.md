# ScoutGitLab — round 93, attempt 1, wave 1

Seat: `ScoutGitLab` (role: scout, per-surface reconnaissance on the GitLab source).
Axes judged: `depth:verifiability`, `coverage`.
Wave: `kasegi-r93-w1` — 13 seats.

Scope note: this seat is reconnaissance on the GitLab source only. It does not edit
`corpus/`, does not run the C1/C2 counters, and does not re-score either frozen claim.
Findings that do not re-score a frozen claim are routed defects/qualifiers for a later round.

## Verdict

- **capture-equal=yes** — the re-fetched page converts to bytes **identical** to the committed
  capture `corpus/source-snapshots/round-93/S139.txt`
  (sha256 `154a7e1535b4a245e45e3f82705c271344f59aa6c344807645fa0bc4d1e1b188`, `cmp` rc=0,
  no differing lines). The capture is current and reproduces exactly.
- **new leads=9** (ranked list in §5; 4 rest on the GitLab source itself, 5 on GitLab's own
  authoritative rules repo).
- **Verdict on the two frozen claims: STANDS.** C1 is out of this seat's surface. C2's frozen
  predicate is unaffected by anything below: every `gitlab-pat` limb of the round-93 counter
  still holds, and the divergences found are **outside** the frozen predicate. They are routed
  defects/qualifiers, not verdict changes. Two are load-bearing for round 94 and are flagged
  as such in §4.

## 1. Re-fetch and byte comparison

Method: the lane's own `corpus/instruments/capture-source.py` conversion functions
(`fetch`, `html_to_text`, `collapse`) were **imported, not copied**, and the page was re-fetched
with the lane's default instrument UA, exactly as the manifest records
(`"fetch_method": "capture-source.py --kind html, default instrument UA; raw 156159 bytes, snapshot 25370 bytes"`).

| | committed capture | re-fetch 2026-11-07 |
|---|---|---|
| HTTP status | 200 (manifest) | 200 |
| fetched bytes | 156159 | 156159 |
| snapshot bytes | 25370 | 25370 |
| sha256 | `154a7e15…1b188` | `154a7e15…1b188` |

`cmp fetch/detected.txt corpus/source-snapshots/round-93/S139.txt` → **rc=0**; `diff -u` →
**empty**. **capture-equal=yes**, and there are no differing lines to quote.

Independently corroborated upstream: the page's own markdown source
(`gitlab-org/gitlab`, `doc/user/application_security/secret_detection/detected_secrets.md`,
master) carries the same sentence at lines 22–23 with the prefix in backticks
(§4 lead L1). The rendered page states it once, as `<code>glpat-</code> followed by a 20-character string`.

## 2. Every statement on the page about `glpat-` and the 20 characters

The page has **exactly one** such statement. Verified in both the snapshot and the raw HTML
(`glpat` count = 1, `character` count = 1 in each).

* Snapshot line **87** (the sentence begins at line 86):
  > `glpat- followed by a 20-character string. GitLab supports`
* Full sentence, snapshot lines 86–87:
  > `credential type, called a rule. For example, a GitLab personal access token is identified by the pattern`
  > `glpat- followed by a 20-character string. GitLab supports`
* Raw HTML (single occurrence, byte offset 34430):
  > `…a GitLab personal access token is identified by the pattern\n<code>glpat-</code> followed by a 20-character string. GitLab supports\n…`

**The page's own line numbers:** the statement sits at snapshot line **87** (sentence spans
86–87); the markdown source puts it at lines **22–23**. The manifest's recorded anchor is 87 —
confirmed.

**Alphabet: NOT stated.** The page gives no character class for the 20 characters. The landed
scanner is explicit about this and says so in its own docstring (`"the string drawn from
A-Za-z0-9_- (a lane choice: the page states the length, not the alphabet)"`). That characterisation
is **correct and verified**: the page contains no alphabet statement, and `character` occurs
exactly once on the page.

**Total length: NOT stated.** The page states the length of the *string* after the prefix (20),
not a total token length. `grep -w 26` on the snapshot finds no standalone `26`; there is no
statement of "26 characters" or "glpat- plus 20" as a total. So the frozen claim's reading
("`glpat-` followed by exactly 20 characters", i.e. a 6+20=26 total) is a **correct inference
from the page**, not a page statement.

## 3. Other first-party GitLab pages

All fetched live on 2026-11-07 and converted through the same lane pipeline. Full record in
receipt `R02-other-gitlab-pages.txt`.

| URL | status | `glpat`? | length statement? | located quote |
|---|---|---|---|---|
| `…/user/profile/personal_access_tokens/` | 200 | **no** (0) | **YES** | line 297: `The token must be 20 characters long.` |
| `…/api/admin/token/` | 200 | **yes** (5) | no | line 176: `When making a request, personal, project, or group access tokens must begin with glpat or the current custom prefix.` |
| `…/security/tokens/` | 200 | **yes** (4) | no | line 349: `Personal access tokenglpat-` (prefix table, lines 344–364) |
| `…/user/project/settings/project_access_tokens/` | 200 | no | no | — |
| `…/user/group/settings/group_access_tokens/` | 200 | no | no | — |
| `…/api/personal_access_tokens/` | 200 | no | no | — |
| `…/user/application_security/secret_detection/` | 200 | no | no | — |
| `…/user/project/deploy_tokens/` | 200 | no | no | — |
| `…/ci/runners/` | 200 | no | no | — |
| `…/administration/incoming_email/` | 200 | no | no | — |
| `…/api/tokens/`, `…/user/project/settings/deploy_tokens/`, `…/ci/runners/registration/`, `…/user/project/settings/feed_tokens/`, `…/api/project_trigger_tokens/`, `…/user/project/settings/feature_flags/`, `…/administration/scim/` | **404** | — | — | — |

### A correction to the frozen frontier note

`claims.json` `frontier.rejected` says the PAT profile page *"carries no `glpat` occurrence, so
it states neither the prefix nor the length"*. The first half is **confirmed** (0 occurrences,
raw HTML included). The second half is **wrong**: the page does carry a length statement, at
snapshot line **297**, in the "create a personal access token programmatically" section:

> `The token must be 20 characters long. The scopes must be valid and are visible`
> `in the source code.`

and the example it gives on the next lines is `token.set_token('token-string-here123')` — a
**20-character** value (`len('token-string-here123') == 20`). So the page states the token length
twice over, once in prose and once in the sample value; it is only the `glpat-` prefix it omits.

This does not change the rejection of that page as *the C2 source* (it still names no prefix, so
it cannot ground the prefix), but the recorded reason is inaccurate, and the page is a
**second independent corroboration of the 20-character length** — which is a `depth:verifiability`
asset for round 94, not a defect in C2.

## 4. GitLab's other token prefixes on the detection page

The detection page names **only `glpat-`** as a prefix. Exhaustive check of the raw HTML: the
only `gl…` tokens present are `glpat-`, `global-nav`, `global-nav-wrapper` (the last two are CSS
class names, not tokens). `glrt`, `gldt`, `glptt`, `glsoat`, `glimt`, `glcbt`, `glffct`,
`glagent`, `gloas` all occur **0** times.

What the page *does* carry is a table of **rule IDs** for GitLab's own token types (snapshot
lines 259–274), with no prefixes attached:

```
259  gitlab_ci_build_token
260  gitlab_deploy_token
262  gitlab_feed_token
263  gitlab_feed_token_v2
264  gitlab_incoming_email_token
265  gitlab_kubernetes_agent_token
266  gitlab_oauth_app_secret
267  gitlab_personal_access_token
268  gitlab_personal_access_token_routable
269  gitlab_personal_access_token_routable_versioned
270  gitlab_pipeline_trigger_token
271  gitlab_runner_auth_token
272  gitlab_runner_auth_token_routable
273  gitlab_runner_registration_token
274  gitlab_scim_oauth_token
```

**Consequence for the landed scanner's "Known limits" wording.** The scanner says
`GitLab runner (glrt-) and other GitLab token prefixes (S139 line 86 names only glpat-)`. The
parenthetical is true *of S139* but the limits are **no longer undocumented** — the prefixes are
listed first-party on `…/security/tokens/` (lines 344–364), and the lengths are published in
GitLab's own rules repo (§5, L4–L5). The limit is still a limit; its stated *justification* is
now stale. Routed qualifier, round 94.

### Divergences between the landed scanner and GitLab's authoritative rule

GitLab's own rule for the personal access token (from the first-party rules repo, §5 L4):

```
regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glpat-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''
```

The landed scanner (round-93 landing commit `9225954a`):

```
_G_LB = rb"(?:(?<![A-Za-z0-9_-])|(?<=\\[ntr])|(?<=\\u[0-9A-Fa-f]{4})|(?<=%[0-9A-Fa-f]{2})|(?<=&#[0-9]{2};)|(?<=&#[xX][0-9A-Fa-f]{2};))"
("gitlab-pat", re.compile(_GL_LB + rb"glpat-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])")),
```

Measured against GitLab's own published examples (receipt `R04`):

| value (from GitLab's rule examples) | GitLab's rule | landed scanner |
|---|---|---|
| `acme-glpat-REDACTED-r93` (custom prefix) | MATCH | **NO-HIT** |
| `glpat-REDACTED-r93` (plain) | MATCH | HIT |
| `glpat-REDACTED-r93` (routable) | routable rule MATCH | **NO-HIT** |
| `glpat-REDACTED-r93` (versioned routable) | versioned-routable rule MATCH | **NO-HIT** |
| `mycompany-glpat-REDACTED-r93` (host-style custom prefix) | MATCH | **NO-HIT** |

**D1 (coverage, round-94).** GitLab's rule permits an **optional custom instance prefix**
(`(?:[a-zA-Z0-9]{1,20}-)?`) before `glpat-`, and GitLab's own example list ships
`acme-glpat-REDACTED-r93`. The landed scanner's left boundary rejects any preceding
`[A-Za-z0-9_-]`, so it misses every custom-prefixed token. This is **not** a false-positive
risk — it is a **miss**. The custom prefix is first-party documented on `…/api/admin/token/`
("must begin with glpat or the current custom prefix") and `…/security/tokens/`
("With the exception of Personal Access tokens, these prefixes cannot be configured"). GitLab
itself raised this shape on 2026-11-03 in commit `59ada1f4` "Add rules for missing GitLab token
formats". Note the round-93 negative `letter-prefixed token is not a hit` is *consistent with the
page* but **wrong against GitLab's own rule** for the hyphenated custom-prefix form (a plain
letter immediately before, e.g. `xglpat-…`, is correctly not a hit by GitLab's rule too).

**D2 (coverage, round-94).** The **routable** PAT forms
(`glpat-<27–300 chars>.<2><7>` and the versioned `…<2>.<2><7>`) are separate, stable GitLab
rules with published examples, and are listed as supported rules on the detection page itself
(lines 268–269). The landed scanner does not detect either.

**D3 (coverage, round-94).** Same rules repo, `rules/mit/github/github.toml`, versus the landed
`github-token` shape:

| value (GitLab's own example) | GitLab's rule | landed scanner |
|---|---|---|
| `ghr_…` refresh token (**76** chars) | `ghr_[0-9a-zA-Z]{76}` | **NO-HIT** (scanner fixes 36) |
| `github_pat_…` fine-grained | `github_pat_[0-9A-Za-z]{22}_[0-9A-Za-z]{59}` | **NO-HIT** (named limit) |
| `v1.…` app installation token | `v1\.[0-9A-Fa-f]{40}` | **NO-HIT** |
| `ghp_…` classic (36) | MATCH | HIT |
| `ghu_…` app (36) | MATCH | HIT |

The `ghr_` 76-vs-36 divergence is a **silent miss**: the landed scanner's `github-token` shape
uses one fixed 36-character tail for `gh[pousr]_`, so `ghr_` refresh tokens are never matched.
`github_pat_` remains the named limit (its length *is* now published — see L5 — so the limit's
stated justification "neither opened source states their length or alphabet" is stale).

**None of D1–D3 re-scores C2.** C2's frozen predicate is the counter's K1–K8 limbs at the
landing, the pinned shas, and the path set. D1–D3 concern tokens *outside* the frozen
`gitlab-pat`/`github-token` shapes, and the frozen negatives (19/21-char tails, bare prefix,
case, `glrt-`) all still hold. They are routed defects for round 94.

## 5. Ranked leads for round 94

Each lead rests on the exact quote given. L1–L3 are the highest value; L1 in particular can
close a `depth:verifiability` gap (the alphabet) that the lane currently carries as an
unsourced "lane choice".

**L1 — The alphabet is now first-party sourced; the "lane choice" caveat can be retired.**
GitLab's own rule for the personal access token publishes the exact character class:
`regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glpat-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''`
— i.e. the tail is `[0-9a-zA-Z_-]{20}`, exactly the landed scanner's `A-Za-z0-9_-`, and the
right boundary is `[^0-9a-zA-Z_\-]|$`, exactly the landed `(?![A-Za-z0-9_-])`. The landed
scanner's alphabet and right boundary are **confirmed correct** by a first-party source, which
removes the "the page states the length, not the alphabet" hedge from a claim that asserts an
alphabet. Source: `gitlab-org/security-products/secret-detection/secret-detection-rules`,
`rules/mit/gitlab/gitlab.toml`, blob `fa1ca53f85b416f2bf5586b9b28597a9757d15c6`, last commit
`59ada1f4ca53d5a69fafb9cb0f10bb893720ce39` (2026-11-03, "Add rules for missing GitLab token formats").

**L2 — A second independent source for the 20-character length** (currently the round-93
frontier note says the PAT page states neither prefix nor length; it states the length).
`https://docs.gitlab.com/user/profile/personal_access_tokens/`, snapshot line 297:
`The token must be 20 characters long. The scopes must be valid and are visible`
— with the worked example `token.set_token('token-string-here123')`, a 20-character value.
Gives C2's length a second first-party witness independent of S139.

**L3 — GitLab's own rules repo is a first-party, citable, versioned ruleset** — the page links to
it directly: `https://gitlab.com/gitlab-org/security-products/secret-detection/secret-detection-rules/-/tree/main`
(href present in the detection page's raw HTML, receipt `R05`). It is a machine-readable
`.toml` with `regex`, `keywords`, `examples`, `negativeExamples`, `maturity` and
`scanningCapabilities` per rule, and each rule has a sibling `.md` under `rules/mit/<vendor>/`.
For the GitLab vendor it carries **33 rules** (`gitlab_personal_access_token`,
`…_routable`, `…_routable_versioned`, `gitlab_deploy_token`, `gitlab_runner_auth_token`,
`gitlab_ci_build_token`, `gitlab_pipeline_trigger_token`, `gitlab_kubernetes_agent_token`,
`gitlab_incoming_email_token`, `gitlab_iam_access_token`, `gitlab_workspace_token`,
`gitlab_stateless_access_token`, `gitlab_session_cookie`, …). This single source can ground the
whole GitLab token family in one capture, with regex-level precision the prose docs never give.

**L4 — The GitLab token-prefix table on `…/security/tokens/`** (snapshot lines 344–364):
`The following table shows the prefixes for each type of token.` /
`With the exception of Personal Access tokens, these prefixes cannot be configured,`
followed by the table: `Personal access tokenglpat-`, `OAuth Application Secretgloas-`,
`Impersonation tokenglpat-`, `Project access tokenglpat-`, `Group access tokenglpat-`,
`Deploy tokengldt-`, `Runner authentication tokenglrt- or glrtr- if created via registration token`,
`CI/CD Job tokenglcbt-`, `Trigger tokenglptt-`, `Feed tokenglft-`,
`Incoming mail tokenglimt-`, `GitLab agent for Kubernetes tokenglagent-`,
`Workspace tokenglwt- (Added in GitLab 18.2)`, `GitLab session cookies_gitlab_session=`,
`SCIM Tokensglsoat-`, `Feature Flags Client tokenglffct-`. This retires the landed scanner's
"S139 line 86 names only `glpat-`" justification and names the exact prefixes to widen to —
`gldt-`, `glrt-`/`glrtr-`, `glcbt-`, `glptt-`, `glft-`, `glimt-`, `glagent-`, `glwt-`, `glsoat-`,
`glffct-`, `gloas-`, `_gitlab_session=`. Note `glrt-` is the prefix the round-93 counter already
holds as a *negative*; it is a real, documented, first-party-prefixed token family.

**L5 — Lengths for every GitLab token family**, published in the same rules repo (`gitlab.toml`),
e.g. `gldt-[0-9a-zA-Z_\-]{20}`, `glffct-[0-9a-zA-Z_\-]{20}`, `glft-[0-9a-zA-Z_\-]{20}`,
`glsoat-[0-9a-zA-Z_\-]{20}`, `glimt-[0-9a-z]{20,25}`, `glagent-[0-9a-zA-Z_\-]{50}`,
`gloas-[0-9a-zA-Z_\-]{64}`, `glptt-(?:…{20}|…{40})`, `glrt-(?:t[1-3]_)?…{20}`,
`glcbt-eyJ…` (JWT), `glsat-eyJ…`, `gliamat-eyJ…`, `glrct-…{20}`. Each is a distinct
one-line shape with a published length — a ready-made expansion list for the scanner.

**L6 — The routable PAT forms** are first-party and separately listed: on the detection page
itself, lines 268–269 name `GitLab Personal Access Token (routable)` /
`gitlab_personal_access_token_routable` and `GitLab Personal Access Token (routable, versioned)` /
`gitlab_personal_access_token_routable_versioned`; the rules repo gives their regexes
(`\b((?:[a-zA-Z0-9]{1,20}-)?glpat-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}[0-9a-z]{7})\b` and the
`\.[0-9a-z]{2}\.` versioned variant) and worked examples. Both are currently undetected.

**L7 — The custom instance prefix** is first-party: `…/api/admin/token/` line 176,
`When making a request, personal, project, or group access tokens must begin with glpat or the
current custom prefix. If the token begins with a previous custom prefix, the operation fails.`
and `…/security/tokens/` line 346, `With the exception of Personal Access tokens, these prefixes
cannot be configured`. GitLab's rule regex encodes the optional prefix
`(?:[a-zA-Z0-9]{1,20}-)?glpat-` and its own example list ships
`acme-glpat-REDACTED-r93`. A GitLab instance with a configured prefix currently yields
no `gitlab-pat` hit.

**L8 — GitHub rule shapes from GitLab's own repo** (`rules/mit/github/github.toml`):
`ghr_[0-9a-zA-Z]{76}` (the landed scanner fixes 36 for all `gh[pousr]_`, so refresh tokens are
silently missed), `github_pat_[0-9A-Za-z]{22}_[0-9A-Za-z]{59}` (the landed named limit — its
length is now published, so the limit's stated reason is stale), and
`v1\.[0-9A-Fa-f]{40}` (GitHub App Installation Token, currently undetected). The same file
also carries `negativeExamples` for `ghp_` (`ghp_deadbeef…`), a negative-source idiom the lane
does not yet use.

**L9 — Upstream markdown source of the same page**, for a cheaper, more stable capture than the
rendered HTML: `https://gitlab.com/gitlab-org/gitlab/-/raw/master/doc/user/application_security/secret_detection/detected_secrets.md`
(HTTP 200, 45143 bytes). The statement is at lines 22–23 with the prefix in backticks:
`` `glpat-` followed by a 20-character string. `` — the same words, one glyph different. The
rendered page also links to this file and to the rules repo, so both are first-party-reachable
from the captured source itself.

## 6. Tooling

No tools were installed, upgraded, or removed this seat; no pacman transaction was attempted.
The host guard's pacman pause was therefore never engaged. Everything used was already present:
`curl` (`/usr/bin/curl`), `python3` (3.14), `jq` (`/home/vgpnk/.local/bin/jq`), and the lane's
own `corpus/instruments/capture-source.py`.

## Receipts

Command outputs cited above are in
`.ufo/waves/round-93/w1/ScoutGitLab-receipts/`:

- `R01-refetch-and-page-content.txt` — re-fetch via the lane's `capture-source.py` conversion
  (status 200, 156159 fetched / 25370 snapshot, sha256 `154a7e15…1b188`); `cmp` rc=0 against the
  committed S139.txt; both sha256 lines; `grep -n glpat` and `grep -n character` (single
  occurrence each, line 87); raw-HTML counts (`glpat_count_raw= 1`, `character_count_raw= 1`)
  with the surrounding HTML; the raw-HTML `gl*` prefix set (`global-nav`, `global-nav-wrapper`,
  `glpat-`).
- `R02-other-gitlab-pages.txt` — the §3 table (URL / status / `glpat` presence / length
  statement) for all 19 pages fetched, including the seven 404s; the PAT page line 297 quote in
  context; the PAT page 0-`glpat` re-check in both snapshot and raw HTML; the `…/api/admin/token/`
  `glpat` lines (176, 209, 223, 277, 291); the `…/security/tokens/` prefix-table rows with
  snapshot line numbers (349–364).
- `R03-gitlab-authoritative-rules.txt` — the rules repo identity (project 60960406,
  `gitlab-org/security-products/secret-detection/secret-detection-rules`, branch `main`,
  blob `fa1ca53f85b416f2bf5586b9b28597a9757d15c6`, last commit `59ada1f4` 2026-11-03) and the
  verbatim `gitlab_personal_access_token`, `…_routable` and `…_routable_versioned` rule blocks
  with their example lists.
- `R04-scanner-vs-gitlab-rule-divergence.txt` — the landed scanner's `gitlab-pat` regex and the
  five-way comparison against GitLab's rule (custom prefix / plain / routable / versioned routable
  / host-style custom prefix), with GitLab-rule vs landed-scanner verdicts.
- `R05-upstream-source-and-provenance.txt` — the upstream `.md` source fetch (HTTP 200, 45143
  bytes) with lines 20–26 and its `glpat`/`character` counts, plus the detection page's own hrefs
  to the `.md` source and to the rules repo.
- `R06-github-rule-divergence.txt` — GitLab's six GitHub rules with their regexes; the landed
  scanner's verdicts on each of GitLab's own example values (`ghr_` 76 chars NO-HIT,
  `github_pat_` NO-HIT, `v1.` NO-HIT, `ghp_` HIT, `ghu_` HIT); the landed `github-token` regex;
  the verbatim `github_pat_` named-limit sentence; and the custom-prefix three-way detail.

All fetches were HTTP GETs against public first-party URLs; no credentials were sent and no
matched secret value is reproduced in this report or in the receipts.
