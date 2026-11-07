# ScoutGitLabRules — per-surface reconnaissance on the GitLab source

**Seat:** ScoutGitLabRules (w1, round 94, attempt 1) · **role:** scout · **lane:** kasegi
**Judged on:** depth:verifiability, coverage
**Scope:** read-only recon on the GitLab source. No file under `corpus/` was edited; no git/jj mutation was run.

## Verdict

**AGREE on the C2 source row (S140) as it stands — with a defect routed, not a verdict change.**

The S140 capture reproduces exactly. I re-fetched the commit-pinned GitLab API raw URL and the bytes are
identical to the digest the frozen manifest recorded (`sha256 14854f71…a11b5`, 20228 bytes), the whitespace-collapsed
form is byte-identical to the manifest's collapsed digest (`sha256 04fc5cfa…d921`, 20035 bytes / 563 lines), and the
committed capture differs from it on **82 lines, every one of them the redaction marker, and nothing else**
(0 non-marker differing lines). Line numbering is preserved and the three quoted regexes still sit at anchors 4,
114 and 255. That is the strongest possible re-derivation of the S140 premise, and I re-derived it myself.

**One number in my own seat brief does not reconcile: the brief says "the 18 redacted line numbers"; the artifact has
82 redacted lines across 24 rules.** I checked every natural reading of "18" (rules with exactly 2 redacted lines =
12, rules with ≥3 = 11, rules with redaction = 24, rules without = 6, 24−6 = 18, total rules = 30, distinct prefixes
= 15/13) — the only arithmetic that yields 18 is *redacted rules minus non-redacted rules*, which is not a meaningful
quantity here. **I report 82 lines / 24 rules, because that is what the bytes say.** This is a defect in the seat brief,
not in the artifact: **routed to the spec author, not a claim re-score.** Nothing in C2's frozen predicate depends on
the count being 18 (P2 pins shas, P3 pins the path set, P4 pins the control rc's).

**C1 is out of this seat's surface** (knowledge-meter repoints, not the GitLab source). I did not re-derive C1 and say
nothing about it.

**The round-95 lead ranking is below. The headline: the `ghr_` 76-character refresh token is now grounded by a
tier-A first-party GitHub source, not only by the tier-B third-party copy — that changes which row may cite it. And a
much larger finding sits underneath: GitHub's own published example tokens for `ghp_`/`gho_`/`ghu_` carry a 40-character
tail, while the lane's landed rule and GitHub's own blog say 36.**

## 1. S140 re-fetch and byte comparison

**Fetched (R01):** the commit-pinned raw URL from `corpus/source-snapshots/round-94/manifest.json`.

```
http=200 bytes=20228 ctype=text/plain; charset=utf-8
sha256  14854f71f81f2400ac33a950cd70850cbdc80c319e4bdb0445bff6dbc36a11b5  s140.raw
```

That is **byte-identical to the manifest's recorded raw digest** — the source has not moved under the pin.

**Comparison (R02):** applying the lane's own `collapse()` (the same whitespace-collapse `capture-source.py` applies),
then diffing line-by-line against the committed capture:

```
FETCHED_RAW  bytes=20228 sha256=14854f71f81f2400ac33a950cd70850cbdc80c319e4bdb0445bff6dbc36a11b5
COLLAPSED    bytes=20035 lines=563 sha256=04fc5cfa200c92f54e14a7d104bb56e479aeccf45746234f0965c3c8e637d921
COMMITTED    bytes=25537 lines=563 sha256=f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c
DIFF_LINES total=82   DIFF_LINES_NONMARKER total=0
```

`04fc5cfa…d921` is exactly the digest the frozen manifest records as the "collapsed snapshot". So the committed
capture is the collapsed upstream file with 82 example-value lines replaced by one fixed marker, and **not one other
byte changed**.

**Redacted line numbers (R03, R04) — 82 lines, not 18:**

```
6,7,8,9,10,11,12, 32,33, 53,54,55, 75,76,77,78,79,80,81,82,83,84,
116,117,118,119, 140,141,142,143,144, 192,193,194,195,196,
231,232,233,234,235,236,237,238, 257,258,259,260,261,
310,311, 326,327, 343,344, 360,361, 377,378, 394,395,396,397,
414,415,416, 432,433, 449,450, 466, 482,483, 499,500,
516,517,518, 534,535, 553,554
```

These match `.ufo/waves/round-94/controls/redaction-r94.txt` exactly, rule for rule and line for line (24 distinct rule
ids, 82 lines). An independent count of the raw file's `examples = [` array element lines also gives **82** — every
redacted line is an array element, and the array delimiters, rule ids, keywords and regex lines are untouched.

**Anchors re-verified in the committed capture:** line 4 `glpat-`, line 114 `glrtr?-`, line 255 `gldt-`, each with the
custom-instance prefix and the 20-character tail — byte-identical to the manifest's three quotes.

**Verdict on the source row: STANDS.** The capture is faithful and the redaction is exactly as documented.

## 2. Round-95 leads — every page opened, status, whether the page states the shape, and a located quote

Full ledger in **R07** (all 42 pages, with rejections and reasons). Each candidate was fetched, converted to the
lane's collapsed text, and run through the instrument's own `scan_bytes()` to record the intake-gate outcome (**R09**).

### 2a. The GitLab shapes — S140 is the ground, and GitLab's own docs page now names the prefixes

The lead shapes all live in S140 itself (the vendor's own rules file, tier A). Nothing outside S140 is needed to ground
them. The one thing S140's *prose* pages could add is the prefix table, and GitLab's own token-overview page has it:

**`https://docs.gitlab.com/security/tokens/` — HTTP 200, page states the shape.** (R10, converted text 418 lines,
sha256 `d6e52927…83d`, intake gate **PASS**, no hits.)

Located quote (converted-text lines 344–364, the "Token prefixes" table; the header "Token prefixes" is line 344 and
the table rows are 349–364):

> The following table shows the prefixes for each type of token.
> With the exception of Personal Access tokens, these prefixes cannot be configured, as they are designed to be standard identifications.
> Personal access token `glpat-` · OAuth Application Secret `gloas-` · Deploy token `gldt-` · Runner authentication token `glrt-` or `glrtr-` if created via registration token · CI/CD Job token `glcbt-` · Trigger token `glptt-` · Feed token `glft-` · Incoming mail token `glimt-` · GitLab agent for Kubernetes token `glagent-` · Workspace token `glwt-` (Added in GitLab 18.2) · GitLab session cookies `_gitlab_session=` · SCIM Tokens `glsoat-` · Feature Flags Client token `glffct-`

**This is the load-bearing new page.** It is GitLab's own prose, tier A, and it independently confirms **every one of
the 15 GitLab prefixes** — including the seven the landed scanner still calls known limits (`glptt-`, `glft-`,
`glimt-`, `glagent-`, `glwt-`, `glsoat-`, `glffct-`, `gloas-`, `glrct-`) and the JWT forms' base prefixes (`glcbt-`,
`glsat-`, `gliamat-`). It confirms the prefix but **not the length**; the length still comes only from S140's regex.

It also carries the `glagent-xxx` example (line 259, in the Rails-console snippet) and the `_gitlab_session=` cookie
form. The page's `glagent-xxx` is a placeholder, not a 50-character token, so it does not trip the gate.

### 2b. The GitHub shapes — the tier-A ground is found, and it is not the row S141 names

**`https://gitlab.com/api/v4/projects/…/rules%2Fmit%2Fgithub%2Fgithub.toml/raw?ref=59ada1f4…` — HTTP 200.** (R08)
sha256 `02c67cebbf24803552c5696b65f9f9885569580ec38480bc29ee56957c2a83e0`, 3955 bytes, 130 lines — **byte-identical
to the digest S141's row already records.** Its rules:

| line | rule id | regex |
|---|---|---|
| 72 | Github Refresh Token | `ghr_[0-9a-zA-Z]{76}` |
| 93 | GithubFineGrainedPersonalAccessToken | `github_pat_[0-9A-Za-z]{22}_[0-9A-Za-z]{59}` |
| 114 | GithubAppInstallationToken | `v1\.[0-9A-Fa-f]{40}` |
| 4 / 30 / 51 | Github PAT / OAuth / App | `ghp_[0-9a-zA-Z]{36}`, `gho_…{36}`, `(ghu\|ghs)_…{36}` |

**But I found a tier-A first-party ground GitHub itself publishes** (R06), which the S141 row's "flip" clause anticipated
without knowing about:

**`https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json`
— HTTP 200, 14 206 638 bytes.** This is **GitHub's own OpenAPI description, in GitHub's own repository** — not GitLab's
copy of GitHub's shapes. In the `POST /credentials/revoke` request-body example GitHub publishes:

```json
"credentials": [
  "ghp_1234567890abcdef1234567890abcdef12345678",
  "github_pat_0A1B2C3D4E5F6G7H8I9J0K_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456",
  "gho_1234567890abcdef1234567890abcdef12345678",
  "ghu_1234567890abcdef1234567890abcdef12345678",
  "ghr_1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890ab"
]
```

Measured lengths (R06): `ghr_` tail = **76** exactly; `github_pat_` = 22 + `_` + 59 exactly; `ghp_`/`gho_`/`ghu_` tail =
**40**.

The same block is on a first-party docs page, which is lighter to capture:

**`https://docs.github.com/en/rest/credentials/revoke` — HTTP 200** (277 713 bytes raw; converted 6560 bytes / 325
lines, sha256 `8582eca5…f0`, intake gate **PASS** today). Located quote at converted line 311:

> -d '{"credentials":["ghp_1234567890abcdef1234567890abcdef12345678","github_pat_0A1B2C3D4E5F6G7H8I9J0K_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456","gho_…","ghu_…","ghr_1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890ab"]}'

And the page's own prose names the prefixes (converted line 281): *"Refresh tokens from GitHub Apps (`ghr_`)"*.

GitHub's other first-party pages give the prefix but **not** the length: `refreshing-user-access-tokens` (HTTP 200,
converted line 169: *"The refresh token. If the access token doesn't expire, this parameter will be omitted. The token
starts with `ghr_`."*) and the credential-types reference (HTTP 200, converted line 143: *"GitHub App refresh token
`ghr_` Long-lived (6 months)"*). Both are tier A and both confirm the prefix; neither states a length.

### 2c. The finding underneath: GitHub's own example `ghp_` tail is 40, the lane's rule says 36

The landed scanner's GitHub rule is `[A-Za-z0-9]{36}` for all five prefixes, sourced to S136/S137 — "30 random plus a
6-character CRC32 checksum" = 36, "40 characters in all" counting the `ghp_` prefix.

**GitHub's own published example values do not match that.** `ghp_1234567890abcdef1234567890abcdef12345678` has a
**40**-character tail (44 total), not 36. Probed against the landed scanner (R05):

```
github-refresh ghr_+76                       -> NO HIT
github-fine-grained github_pat_ 22_59        -> NO HIT
github-app-installation v1.+40hex            -> NO HIT
CONTROL already-landed github-token ghp_+36  -> [('github-token', 1)]
```

**Every GitHub token shape in GitHub's own first-party example is a miss for the landed scanner** (R05). That includes
`ghp_`, `gho_` and `ghu_` at 40 — the very prefixes the scanner claims to cover.

Two readings, and the lane must not pick one silently:
1. The 36-character rule is right and GitHub's *example* is a 40-character placeholder (note the same file's `ghs_` /
   `ghu_` values elsewhere are 36 — `ghs_16C7e42F292c6912E7710c838347Ae178B4a`, measured tail = 36). The example
   strings look like hand-written placeholders (`1234567890abcdef` repeated), not minted tokens.
2. GitHub's own examples are the ground and the 36-character rule is too narrow.

**I am not resolving this, and this seat is not the right seat to resolve it.** It is a **depth:verifiability** question
about a landed rule, not a coverage question about round 95. I flag it, with the measurements, for a seat that can
attack it. What is certain and re-derived: the landed scanner does not detect GitHub's own published example values,
and `ghr_`+76 and `github_pat_` 22_59 are both misses.

### 2d. The routable / versioned forms

These are in S140 only (lines 30, 51, 136, 324, 358, 375), and **GitLab's prose pages do not state them**. I searched
six GitLab pages for "routable" (`docs.gitlab.com/security/tokens/`, `/api/deploy_tokens/`,
`/user/project/deploy_tokens/`, `/ci/environments/`, `/api/cluster_agents/`, `/user/profile/personal_access_tokens/`)
and got **zero hits on every one**. The routable forms are therefore **grounded by S140 alone**, at lines 30, 51, 136,
324 — already the anchor set S140's own row names. No new source row is needed; they are a scope decision, not a
sourcing problem.

### 2e. Shape-by-shape: does the page state the shape?

| Shape | Landed scanner | Ground (row) | Tier | Page states the shape? | Quote located |
|---|---|---|---|---|---|
| `glpat-` +20 (+custom prefix) | **HIT** (landed) | S139 + S140 | A | yes | S139 L87; S140 L4 |
| `glrt-`/`glrtr-` +`t1_`/`t2_`/`t3_` +20 | **HIT** (landed) | S140 | A | yes | S140 L114 |
| `gldt-` +20 | **HIT** (landed) | S140 | A | yes | S140 L255 |
| `glagent-` +50 | NO HIT | S140 L213 (+ prefix table) | A | prefix only | security/tokens L360 |
| `glsoat-` +20 | NO HIT | S140 L278 (+ prefix table) | A | prefix only | security/tokens L363 |
| `glffct-` +20 | NO HIT | S140 L392 (+ prefix table) | A | prefix only | security/tokens L364 |
| `gloas-` +64 | NO HIT | S140 L174 (+ prefix table) | A | prefix only | security/tokens L350 |
| `glcbt-eyJ…` JWT | NO HIT | S140 L430 (+ prefix table) | A | prefix only | security/tokens L356 |
| `glsat-eyJ…` JWT | NO HIT | S140 L447 | A | **no** — `glsat-` absent from the prefix table | — |
| `gliamat-eyJ…` JWT | NO HIT | S140 L464 | A | **no** — `gliamat-` absent | — |
| `glpat-` routable / versioned | NO HIT | S140 L30, L51 | A | **no** — no prose states it | — |
| `glrt-`/`gldt-` routable | NO HIT | S140 L136, L324 | A | **no** | — |
| `ghr_` +76 | NO HIT | **S141 (tier B) or the new tier-A GitHub row** | A now reachable | yes (example, 76 measured) | docs.github.com/rest/credentials/revoke L311 |
| `github_pat_` 22_59 | NO HIT | S141 L93 **or the new tier-A GitHub row** | A now reachable | yes (example, 22+59 measured) | same line 311 |
| `v1.` +40 hex | NO HIT | S141 L114 | B | no first-party page found | — |

Note `glsat-` and `gliamat-` appear in **no** GitLab prose page I opened — the rules file is their only source, and
S140's own row only names their *regex* lines, so a round-95 claim citing them must cite S140 L447/L464 explicitly.

## 3. Ranked for round 95

Ordered by (ground quality × coverage gained × verification cost), best first.

**1. `ghr_` +76 refresh token — and the source row that may now cite it.**
The shape is a confirmed miss (R05). S141 was REJECTED as tier B ("GitLab is not the vendor of GitHub tokens"), and its
own flip clause says: *"a round admits the `ghr_` refresh-token shape and cites this row."* **That flip is now
reachable through a tier-A row**: GitHub's own OpenAPI (R06) and GitHub's own REST docs page publish the 76-character
example verbatim. Round 95 should open a **new tier-A row** for `docs.github.com/en/rest/credentials/revoke` (or the
OpenAPI description) and cite *that*, leaving S141 rejected; S141's tier-B status was a sourcing limitation, not a
shape limitation. Highest value: it converts a "tier B at most" shape into a tier-A one.

**2. The GitLab prefix table (`docs.gitlab.com/security/tokens/`) as one row covering nine prefixes.**
Tier A, GitLab's own prose, 15 prefixes confirmed, intake gate clean (R09), and it removes the "the docs pages do not
state the shape" objection for `glagent-`, `glsoat-`, `glffct-`, `gloas-`, `glcbt-`, `glptt-`, `glft-`, `glimt-`,
`glwt-`, `glrct-`. It states the **prefix**; S140 supplies the length. One row, many shapes — best
ground-per-source ratio in the set.

**3. `glagent-` +50, `glsoat-` +20, `glffct-` +20, `gloas-` +64.**
Four fixed-length shapes, each with an exact regex already published in S140 (L213, L278, L392, L174), each confirmed
a miss (R05), each with a prefix confirmed by the new tier-A page. The cheapest four to land: fixed tail length, one
boundary rule, no JWT structure.

**4. The GitHub example-length discrepancy — a depth:verifiability defect, not a round-95 coverage claim.**
GitHub's own published `ghp_`/`gho_`/`ghu_` examples have 40-char tails; the landed rule says 36; the scanner misses
all three (R05). High value, but it attacks a **landed** rule and needs a hostile reading of two first-party sources
before it can be called. **Route it to a critic/reviewer seat with the counter time**, not into a coverage claim.

**5. The routable / versioned forms (S140 L30, L51, L136, L324).**
No prose source exists; S140 is the only ground. Grounded, but the shapes are the most structurally awkward (a
`.<tld>.<suffix>` tail inside a token), so they cost the most verification per unit of coverage. Also a known-limit
removal the round-93 lineage already deferred.

**6. `github_pat_` 22_59 and `v1.`+40hex.**
`github_pat_` is now tier-A reachable via the same new GitHub row as #1 — bundle it there. `v1.`+40hex has **no
first-party ground I could find** (only S141, tier B) — leave it a limit.

**7. `glcbt-eyJ…` / `glsat-eyJ…` / `gliamat-eyJ…` JWT forms (S140 L430, L447, L464).**
The lane already has a JWT matcher (`ghs_<APPID>_<JWT>`), so the machinery exists; but two of the three prefixes appear
in no prose page, and the `eyJ` structure invites false positives (any base64url blob starting `eyJ` matches). **Lowest
rank on this list despite three shapes** — the false-positive surface is the reason.

## 4. Which source row grounds which shape — the mapping

- **S140** (`rules/mit/gitlab/gitlab.toml`, tier A, mined): the ground for **every** GitLab shape's exact prefix,
  alphabet and length — L4, L114, L255 (landed) and L174, L213, L278, L392, L430, L447, L464, L30, L51, L136, L324.
  Verified reproducible from the pin.
- **S139** (`docs.gitlab.com/…/detected_secrets/`, tier A): `glpat-` + 20 chars, prose statement, L86–87.
- **NEW tier-A row (recommended): `docs.gitlab.com/security/tokens/`** — the GitLab prefix table, 15 prefixes, page
  states the shape. Grounds the *prefix* of every GitLab shape; lengths still come from S140.
- **NEW tier-A row (recommended): `docs.github.com/en/rest/credentials/revoke`** (or GitHub's OpenAPI description) —
  grounds `ghr_`+76 and `github_pat_` 22+59 from GitHub itself, which is what S141 could not do.
- **S141** (`rules/mit/github/github.toml`, tier B, **rejected**): remains the third-party corroboration. Its flip
  clause is satisfiable, but it should be satisfied by a *tier-A* row so the shape does not rest on tier B.

## 5. Defects routed (none re-scores a claim)

- **D-S1 — seat brief number.** "the 18 redacted line numbers" vs the artifact's **82 lines / 24 rules**. The artifact
  and the frozen receipt agree with each other and with the raw byte count; only the brief's number is wrong. Routed to
  the spec author. **No claim impact** (C2's predicate pins shas, path set and control rcs, not this count).
- **D-S2 — GitHub example length.** Landed `github-token` shape (36-char tail) does not detect GitHub's own published
  `ghp_`/`gho_`/`ghu_` examples (40-char tail). Routed to a depth:verifiability critic seat with R05/R06. **No claim
  impact on C2** (C2's predicate is the GitLab shapes and K1–K9).
- **D-S3 — intake-gate coupling (forward-looking, for round 95's capture step).** The GitHub REST page passes today's
  gate, but **adding a `ghr_`+76 or `github_pat_` shape makes the gate refuse that very page** (line 311 hits; verified
  in R09's forward check). A round-95 capture of the new ground source must therefore expect the same redaction
  treatment S140 needed, or capture the OpenAPI with the example values redacted. Worth knowing before the capture
  step, not a defect in anything landed.

## 6. Open unknowns

- Whether the 36-vs-40 GitHub length is a scanner defect or a placeholder artifact (D-S2) — **not resolvable from the
  pages I opened**; it needs GitHub's token-minting source or a measured live token.
- Whether `glsat-` and `gliamat-` are documented anywhere in GitLab's prose at all — I found none in **17** GitLab
  pages (the 17 non-404 GitLab page texts I converted and searched; verified zero hits for both prefixes in every
  one). The GitLab API reference for stateless/IAM tokens was not reachable under the paths I tried
  (`/api/project_tokens/` 404, `/user/gitlab_service_account/` 404, `/api/pipeline_trigger_tokens/` 404).
- Whether GitHub publishes a **length** statement anywhere first-party — every first-party page I opened states the
  `ghr_` prefix and its lifespan but no length; the 76 comes from the example value's measured length and from
  S141's regex.

## Receipts

All under `.ufo/waves/round-94/w1/ScoutGitLabRules-receipts/`.

| file | content |
|---|---|
| `01-s140-refetch.txt` | curl of the commit-pinned raw URL: http=200, 20228 bytes, sha256 `14854f71…a11b5` |
| `02-s140-byte-compare.txt` | raw → collapsed → committed diff: 82 differing lines, **0** non-marker |
| `03-s140-redacted-lines.txt` | committed capture sha/bytes/lines + the 82 redacted line numbers |
| `04-redaction-receipt-crosscheck.txt` | the 82 lines re-counted from `controls/redaction-r94.txt`, by rule id (24 rules) |
| `05-lead-shape-probes.txt` | all 15 lead shapes probed against the landed scanner + 2 controls |
| `06-github-firstparty-examples.txt` | GitHub's own OpenAPI `/credentials/revoke` example block + measured lengths |
| `07-pages-opened.txt` | all 40 doc pages opened with HTTP status (26 × 200, 14 × 404) + 3 vendor rules-file URLs; rejections included |
| `08-github-rules-file.txt` | `rules/mit/github/github.toml` fetch: sha256 `02c67ceb…3e0`, 3955 bytes, 130 lines, all rules |
| `09-intake-gate.txt` | intake-gate outcome for each candidate round-95 source page |
| `10-gitlab-token-prefix-table.txt` | the GitLab token-prefix table with absolute line numbers |

**Tooling:** none installed or upgraded this seat. `curl` and `python3` (standard library) as shipped. No pacman, no
`uv`, no `~/.local/bin` write. The `.ufo/waves/round-94/controls/` receipts were read, never modified.

**Constraints honoured:** no `git`/`jj` mutation of any kind; no file under `corpus/` edited (the only writes are this
report and the receipts directory named by the seat spec); no `ask`; no `agent://all`; no subagent dispatch. Scratch
`/fast/scratch/hyaku/kasegi-r94/ScoutGitLabRules` was removed on exit.
