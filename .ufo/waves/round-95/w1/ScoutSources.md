# ScoutSources — round 95, wave 1

Seat: source re-derivation for the three sources the round rests on (S142, S141, S140),
plus the round-96 lead inventory of S140's remaining GitLab families.

Lane: kasegi. Base `9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10`, freeze
`347519f21524d2bc13eb6c91cf3550930a4265b3`, C1 landing `53ec479d71d25cf5be052db794a548a5904564b8`,
C2 landing `38e7319f44a9fab2978b59ffd43faf207cf62b32`, HEAD at the time of this report
`43cc15e8d807a06baf9d2dd789bb121364944169`.

## Verdict

**AGREE on all three source anchors, re-derived live and independently.** S142 line 169
states the `ghr_` prefix and nothing more; S141 line 72 states `ghr_[0-9a-zA-Z]{76}`;
S140 lines 429/446/463 name the `glcbt-`/`glsat-`/`gliamat-` rules. Every fetch returned
HTTP 200 and every re-fetch is **byte-identical** to the digest the lane already pins.
No claim re-score: C1 and C2's frozen predicates are unaffected by anything below.

Six findings are routed (defects/qualifiers), none of which re-scores a claim:

| # | Finding | Owner | Re-scores a claim? |
|---|---|---|---|
| R1 | `corpus/source-snapshots/round-95/` has **no `manifest.json`**; `capture-binding-check.py` FAILs `rule=missing-manifest dir=round-95` from the freeze commit onward, still open at HEAD | integrator | no (neither predicate runs the binding check) |
| R2 | S140's "line numbering preserved" note holds against the *collapsed* capture, **not** the raw fetch: the three JWT rules sit at raw lines 451/469/487 (+22/+23/+24) | integrator / scribe | no (the claim's anchors are correct against the committed capture) |
| R3 | The 76-length ground is tier B (GitLab's copy of GitHub's shapes) although a **tier-A ground exists** and is now **uncapturable** by the lane's own tool | round 96 | no (tier is not in C2's predicate or kill rule) |
| R4 | S142's registry row pins no digest for the capture (S143's row pins its file's digest) | scribe / integrator | no |
| R5 | Two lane shapes are **stricter than the source regexes** they implement (right-boundary divergences) | round 96 / reviewer | no |
| R6 | C2's frozen statement cites **S141** for the 76-length, but S141's registry row is `rejected` / used-by `—`; the landed citation is **S143** (`mined`), which did not exist at the freeze | scribe / integrator | no (the predicate does not test the registry row) |

---

## 1. S142 — GitHub Docs, "Refreshing user access tokens"

**URL:** `https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/refreshing-user-access-tokens`

* HTTP **200**, fetched **196,832** bytes, live HTML sha256
  `f57ab983e8bf1dd61d1dae18cc874327485e0c8c76213c01d8c43d803d779804`.
* Re-captured through the lane's own instrument (`capture-source.py --kind html`) into scratch:
  `snapshot_bytes=7944 sha256=727ba6a0294318324e43ddd266832c49b3895303667b9419336d3265f8a42864`.
* The committed capture `corpus/source-snapshots/round-95/S142.txt` is
  **byte-identical** to that re-capture (`diff` rc=0, 0 lines; committed sha256
  `727ba6a0…42864`, 7,944 bytes, 182 lines).

**Located anchor — snapshot line 169** (the only `ghr_` occurrence in the file):

```
169: refresh_tokenstringThe refresh token. If the access token doesn't expire, this
     parameter will be omitted. The token starts with ghr_.
```

**Located quote (18 words):** "The refresh token. If the access token doesn't expire, this
parameter will be omitted. The token starts with ghr_."

**What S142 does and does not ground.** It grounds the **prefix** `ghr_` and the fact that
the token arrives as a `refresh_token` field in the exchange response. It states **no
length**. `grep -c 'The token starts with ghr_'` on the committed capture → `1`.
The live HTML carries the same sentence in the response-parameter table.

This matches what the registry row already says ("the page states no length, so the
76-character bound must come from another source") and what the knowledge entry's
"Rejected claims" section says. **No correction needed.**

## 2. S141 / S143 — GitLab's rules copy of GitHub's shapes

**URL:** `…/repository/files/rules%2Fmit%2Fgithub%2Fgithub.toml/raw?ref=59ada1f4ca53d5a69fafb9cb0f10bb893720ce39`

* HTTP **200**, **3,955** bytes, sha256
  `02c67cebbf24803552c5696b65f9f9885569580ec38480bc29ee56957c2a83e0`, 130 lines.
* Byte-identical to the digest the round-94 wave recorded for the same fetch
  (`.ufo/waves/round-94/w1/ScoutGitLabRules-receipts/08-github-rules-file.txt`) and to the
  digest S143's registry row pins.

**Located anchor — line 72:**

```
69: [[rules]]
70: id = "Github Refresh Token"
71: keywords = ["ghr_"]
72: regex = "ghr_[0-9a-zA-Z]{76}"
```

**Located quote (3 words):** `regex = "ghr_[0-9a-zA-Z]{76}"`

**Tier B, as the row says.** This is GitLab's copy of GitHub's shapes, not GitHub's own
statement. It is **not committed as a capture** — the file's example arrays carry published
token values, and the lane's intake gate refuses the bytes. I reproduced the refusal
(§6). So the length ground exists only as a re-fetchable URL plus the digest in the
registry row; it is not offline-verifiable from the lane tree.

## 3. S140 — GitLab's own secret-detection rules

**URL:** `…/repository/files/rules%2Fmit%2Fgitlab%2Fgitlab.toml/raw?ref=59ada1f4ca53d5a69fafb9cb0f10bb893720ce39`

* HTTP **200**, **20,228** bytes, sha256
  `14854f71f81f2400ac33a950cd70850cbdc80c319e4bdb0445bff6dbc36a11b5` — **byte-identical**
  to the "raw" digest the round-94 manifest pins.
* Committed capture `corpus/source-snapshots/round-94/S140.txt`: sha256
  `f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`, 25,537 bytes, 563 lines.

**Located anchors in the committed capture** (the lines C2's frozen statement cites):

```
428: id = "gitlab_ci_build_token_jwt"
429: keywords = ["glcbt-"]
430: regex = '''\b(?:[a-zA-Z0-9]{1,20}-)?glcbt-eyJ[0-9a-zA-Z_\-]{10,1000}\.eyJ[0-9a-zA-Z_\-]{10,1000}\.[0-9a-zA-Z_\-]{20,1000}'''
445: id = "gitlab_stateless_access_token"
446: keywords = ["glsat-"]
447: regex = '''\b(?:[a-zA-Z0-9]{1,20}-)?glsat-eyJ[0-9a-zA-Z_\-]{10,1000}\.eyJ[0-9a-zA-Z_\-]{10,1000}\.[0-9a-zA-Z_\-]{20,1000}'''
462: id = "gitlab_iam_access_token"
463: keywords = ["gliamat-"]
464: regex = '''\bgliamat-eyJ[0-9a-zA-Z_\-]{10,1000}\.eyJ[0-9a-zA-Z_\-]{10,1000}\.[0-9a-zA-Z_\-]{20,1000}'''
```

**Located quote (5 words):** `keywords = ["glcbt-"]` — and `["glsat-"]`, `["gliamat-"]`.

`source-recheck.py --manifest corpus/source-snapshots/round-94/manifest.json --source S140`
→ `sha256 OK`, `Q01/Q02/Q03 OK occurrences=1 anchor=4-ok/114-ok/255-ok`, rc=0.

### R2 — the line-number caveat (routed)

The round-94 manifest's note says the redaction keeps "line numbering … preserved". That
is true against the *collapsed* capture (`capture-source.py --kind text` → 563 lines), and
the committed snapshot's anchors are the ones every lane citation uses. It is **not** true
against the raw fetch, which is 592 lines: the collapse drops the file's 30 blank lines, so
the offset between raw and snapshot grows monotonically from 0 to +29:

| rule | snapshot line | raw line | delta |
|---|---|---|---|
| `gitlab_personal_access_token` | 2 | 2 | 0 |
| `gitlab_pipeline_trigger_token` | 71 | 74 | +3 |
| `gitlab_ci_build_token_jwt` | **428** | **450** | **+22** |
| `gitlab_stateless_access_token` | **445** | **468** | **+23** |
| `gitlab_iam_access_token` | **462** | **486** | **+24** |
| `gitlab_session_cookie` | 547 | 576 | +29 |

So the three JWT *keywords* lines are 429/446/463 in the committed capture but **451/469/487**
in the raw file; jumping to 429/446/463 in a fresh fetch lands on blank/`pushProtection`
lines. Nothing in the claim or the landed entry is wrong (both cite the committed capture,
and `sed -n '429p;446p;463p' corpus/source-snapshots/round-94/S140.txt` prints the three
keywords lines correctly), but a future auditor who re-fetches and line-numbers the raw
bytes will be misled. Round-96 should either cite rule ids alongside line numbers, or
state the collapse in the row's `where` cell.

### The landed scanner, probed against the source regexes

Landed instrument `corpus/instruments/capture-secret-scan.py` sha256 `66edd661…6707`,
byte-identical to the frozen candidate `.ufo/waves/round-95/c2/candidate-scanner.py`.
`claim-package-check.py` sha256 `8b6f8493…c8e6` — equals the frozen gate pin.
`--selftest` → `SELFTEST-RESULT pass cases=115`; at base `9ef0126` the same selftest prints
`cases=101`, so 101 → 115 is confirmed independently.

| case | landed scanner | source regex |
|---|---|---|
| `ghr_` + 76 | `github-refresh-token` | S141 L72 MATCH |
| `ghr_` + 75 | NO HIT | no match |
| `ghr_` + 76 + a 77th alnum | NO HIT | **S141 L72 MATCH** (R5) |
| `ghr_` + 36 | `github-token` | — |
| `glcbt-eyJ…` | `gitlab-jwt-token` | S140 L430 MATCH |
| `acme-glcbt-eyJ…` | `gitlab-jwt-token` | S140 L430 MATCH |
| `glsat-eyJ…` / `acme-glsat-eyJ…` | `gitlab-jwt-token` | S140 L447 MATCH |
| `gliamat-eyJ…` | `gitlab-jwt-token` | S140 L464 MATCH |
| `acme-gliamat-eyJ…` | `gitlab-jwt-token` | S140 L464 MATCH (via `\b`) |
| `glcbt-eyJ…` with a 1001-char tail | NO HIT | **S140 L430 MATCH** (R5) |
| `glcbt-eyJ<header>.<payload>.<signature>` | NO HIT | no match |
| 9-char first segment / 19-char third segment | NO HIT | no match |
| legacy `glcbt-<5alnum>_<20+>` (S140 L293) | NO HIT | — |
| `glpat-`/`gldt-`/`glrt-` routable forms | NO HIT | — |
| `glagent-`/`glwt-` routable forms | NO HIT | — |

Base instrument at `9ef0126` on the same inputs: `ghr_`+76 **NO HIT**; `glcbt-`/`glsat-`/
`gliamat-` JWT **NO HIT** — the base instrument matches neither new shape, as C2's kill
rule requires.

Lane scan at HEAD: `CAPTURE-SECRET-SCAN mode=rev:HEAD scanned=2477 hits=0 files=0
allowed=26 unused_allow=0 rc=0` — the tree scans clean and the round's one new allowlist
row is **consumed** (`unused_allow=0`), i.e. it is not a dead row. Its digest
`c7ad99a1…060d` is the sha256 of the matched 80-byte `ghr_` value in the round-94 receipt
`.ufo/waves/round-94/w1/ScoutGitLabRules-receipts/06-github-firstparty-examples.txt` — I
recomputed it over the raw matched bytes.

### R5 — the lane is stricter than its sources (routed, minor)

Two places where the landed shapes are *narrower* than the regexes they cite: the `ghr_`
right bound `(?![A-Za-z0-9_])` (so a 77-character run does not fire, though S141's regex
would match its first 76) and the JWT tail bound `(?![A-Za-z0-9_-])` (so a 1001-character
tail does not fire, though S140's `{20,1000}` regex would match its first 1000). The
`ghr_` bound is disclosed in C2's frozen statement; the JWT tail bound is not. Both are
under-detection, never over-detection. Worth one sentence in the knowledge entry's
"Known limits".

## 4. R1 — the round-95 capture has no manifest (routed, highest priority)

`capture-binding-check.py` over the lane tree, at four revisions:

| revision | `missing_manifest` | FAILs |
|---|---|---|
| base `9ef0126` | 0 | `rejected-row-anchor S138` (pre-existing) |
| freeze `347519f` | **1** | **`missing-manifest dir=round-95`** + the pre-existing S138 |
| C2 landing `38e7319` | 1 | same |
| HEAD `43cc15e` | 1 | same |

`corpus/source-snapshots/round-95/` contains `S142.txt` and **no `manifest.json`**; it is
the only one of the 68 snapshot directories without one (67/67 had one at base). The
integration commit `43cc15e` did not add it.

Two consequences, both measured:

* `source-recheck.py --manifest corpus/source-snapshots/round-95/manifest.json --source S142`
  → `manifest UNAVAILABLE reason=missing`, **rc=2**. The round's own new capture cannot be
  re-checked for quote survival or anchor stability; S140's can
  (`Q01/Q02/Q03 OK … rc=0`).
* The binding audit's record count is **117 at base and 117 at HEAD** — S142's registry
  row is not bound to any manifest record, so the instrument never sees it. `bound=116
  unbound=1` is unchanged from base, and the one unbound record is the pre-existing
  `S040-live.txt` orphan. In other words the row is not *reported* unbound; it is simply
  outside the audit.

Fix shape (integrator): add `corpus/source-snapshots/round-95/manifest.json` with one
record for S142 — `url`, `fetched_utc`, `path: S142.txt`, `sha256:
727ba6a0294318324e43ddd266832c49b3895303667b9419336d3265f8a42864`, and a quote record
pinning the line-169 sentence — the same shape as round-94's manifest. That also gives the
S142 row a digest pin, closing R4 at the same time.

## 5. R3 — the length ground is tier B where a tier A ground exists (routed; round-96 lead)

GitHub itself publishes the `ghr_` + 76 shape in its own first-party material:

* `https://docs.github.com/en/rest/credentials/revoke` — HTTP 200, 277,713 bytes raw; the
  converted capture's **line 311** carries GitHub's own `-d '{"credentials":[…,"ghr_…"]}'`
  example, whose `ghr_` value is **80 bytes total / 76 tail** and whose sha256 is
  `c7ad99a1…060d` — the *same digest* as the allowlisted round-94 placeholder.
* `https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json`
  (GitHub's own OpenAPI) publishes the same example; the round-94 wave recorded it at
  `.ufo/waves/round-94/w1/ScoutGitLabRules-receipts/06-github-firstparty-examples.txt`.

The round-94 wave recommended exactly this row; round 95 landed **S143 at tier B** instead
(GitLab's copy of GitHub's shapes). That is a sourcing-quality gap, not a predicate
failure — C2's predicate and kill rule say nothing about tier.

**The blocker, measured.** At base the lane's own capture tool takes the tier-A page
cleanly; at HEAD it **refuses** it:

```
base  9ef0126: GHREVOKE_BASE status=200 fetched_bytes=277713 snapshot_bytes=6560
                sha256=8582eca5a56807d41bad7f220d1e7531080f0b0a072d7723e6ae14344d8011f0
HEAD 43cc15e: INTAKE-REFUSED GHREVOKE shape=github-refresh-token line=311 written=no
```

Same for GitHub's OpenAPI file (`INTAKE-REFUSED … shape=github-refresh-token line=22396`).
So the new shape closes the door on the tier-A ground it was derived from. Round 96 needs
one of:

1. a digest-bound allowlist row for the tier-A capture path — the allowlist key is
   `(path, shape, sha256)`, so the existing row (path = the round-94 receipt) does **not**
   cover a new capture path even though the digest matches; or
2. the same structural redaction S140 used — replace the example-element lines with one
   fixed marker, preserving line numbering; or
3. cite the tier-A page as a URL + digest in a registry row without committing a capture,
   which is what S143 does for its tier-B file.

Also measured, for whoever takes it: `S141`'s own file is refused for **two** shapes at
HEAD — `github-token` (line 6) and the new `github-refresh-token` (line 71) — and S140's
raw file is refused for `gitlab-deploy-token` (line 257) and the new `gitlab-jwt-token`
(line 432).

## 6. Round-96 leads — the remaining GitLab families in S140

All 30 S140 rules, with the verbatim regex and its line in the committed capture, plus the
id line in the raw fetch for cross-reference (see §3's drift table). Line columns:
**snap-id / snap-regex** = lines in `corpus/source-snapshots/round-94/S140.txt`;
**live-id** = the `id =` line in the raw 592-line fetch of 2026-11-07.

The scanner currently implements 5 of the 30 (glpat, glrt/glrtr, gldt, and the three JWT
rules folded into one `gitlab-jwt-token` shape). **24 rules are unlanded.** Ranked by how
well a tier-A ground corroborates them — GitLab's own docs prefix table
(`https://docs.gitlab.com/security/tokens/`, HTTP 200, sha256
`765becf33995fd344ae5939ac6f6e35715b7c2a348b32f708a0a32472b17f4b6`) names these
prefixes, so a family whose prefix appears there has a **tier-A** ground as well as S140's
tier-A rules file:

### 6a. Tier-A corroborated (prefix in GitLab's own docs table) — best round-96 candidates

| prefix | rule id | snap-id / snap-regex | live-id | regex |
|---|---|---|---|---|
| `glptt-` | `gitlab_pipeline_trigger_token` | 71 / 73 | 74 | `\b((?:[a-zA-Z0-9]{1,20}-)?glptt-(?:[0-9a-zA-Z_\-]{20}\|[0-9a-zA-Z_\-]{40}))(?:[^0-9a-zA-Z_\-]\|$)` |
| `gloas-` | `gitlab_oauth_app_secret` | 172 / 174 | 180 | `\b(gloas-[0-9a-zA-Z_\-]{64})(?:[[:punct:]]\|[[:space:]]\|[[:blank:]]\|$)` |
| `glft-` | `gitlab_feed_token_v2` | 188 / 190 | 197 | `\b(glft-[0-9a-zA-Z_\-]{20})(?:[[:punct:]]\|[[:space:]]\|[[:blank:]]\|$)` |
| `glimt-` | `gitlab_incoming_email_token` | 227 / 229 | 238 | `\b((?:[a-zA-Z0-9]{1,20}-)?glimt-[0-9a-z]{20,25})(?:[^0-9a-zA-Z_\-]\|$)` |
| `glsoat-` | `gitlab_scim_oauth_token` | 276 / 278 | 289 | `\b(glsoat-[0-9a-zA-Z_\-]{20})(?:[[:punct:]]\|[[:space:]]\|[[:blank:]]\|$)` |
| `glagent-` | `gitlab_kubernetes_agent_token` | 211 / 213 | 221 | `\b((?:[a-zA-Z0-9]{1,20}-)?glagent-[0-9a-zA-Z_\-]{50})(?:[^0-9a-zA-Z_\-.]\|\.[^0-9a-z]\|\.$\|$)` |
| `glagent-` routable | `gitlab_kubernetes_agent_token_routable` | 356 / 358 | 374 | `\b((?:[a-zA-Z0-9]{1,20}-)?glagent-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7})\b` |
| `glwt-` | `gitlab_workspace_token` | 373 / 375 | 392 | `\b((?:[a-zA-Z0-9]{1,20}-)?glwt-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7})\b` |
| `glffct-` | `gitlab_feature_flags_client_token` | 390 / 392 | 410 | `\b((?:[a-zA-Z0-9]{1,20}-)?glffct-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]\|$)` |

GitLab's docs also list `glcbt-` (CI/CD Job token) and `gldt-`/`glrt-`/`glrtr-`/`glpat-`
(already landed) and `_gitlab_session=`. `glwt-` is marked "(Added in GitLab 18.2)".

### 6b. S140-only (no tier-A corroboration on the vendor's prefix table)

| prefix | rule id | snap-id / snap-regex | live-id | regex |
|---|---|---|---|---|
| `glrct-` | `gitlab_runner_controller_token` | 410 / 412 | 431 | `\b((?:[a-zA-Z0-9]{1,20}-)?glrct-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]\|$)` |
| `gliamrt-` | `gitlab_iam_refresh_token` | 478 / 480 | 503 | `\b(gliamrt-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:[^0-9a-zA-Z_\-]\|$)` |
| `gliamac-` | `gitlab_iam_authorization_code` | 495 / 497 | 521 | `\b(gliamac-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:[^0-9a-zA-Z_\-]\|$)` |
| `glcbt-` legacy | `gitlab_ci_build_token` | 291 / 293 | 305 | `\b(glcbt-[0-9a-zA-Z]{1,5}_[0-9a-zA-Z_\-]{20})(?:[[:punct:]]\|[[:space:]]\|[[:blank:]]\|$)` |
| `glft-` path-dependent | `gitlab_feed_token_path_dependent` | 512 / 514 | 539 | `\b(?:[a-zA-Z0-9]{1,20}-)?glft-[0-9a-f]{64}-[0-9]{1,20}\b` |
| `feed_token=` | `gitlab_feed_token` | 158 / 160 | 165 | `\b(feed_token=[0-9a-zA-Z_\-]{20})(?:[[:punct:]]\|[[:space:]]\|[[:blank:]]\|$)` |
| `GR1348941` | `gitlab_runner_registration_token` | 99 / 101 | 103 | `\b(GR1348941[0-9a-zA-Z_\-]{20})(?:[[:punct:]]\|[[:space:]]\|[[:blank:]]\|$)` |
| `t1_`/`t2_`/`t3_` | `gitlab_runner_auth_token_legacy_partition` | 306 / 308 | 321 | `(?:(?m:^)\|[^0-9a-zA-Z_\-\r\n])(t[1-3]_[1-9a-km-zA-HJ-NP-Z_\-]{20})(?:[^0-9a-zA-Z_\-]\|$)` |
| in-URL | `gitlab_deploy_token_in_url` | 339 / 341 | 356 | `gitlab\+deploy-token-[0-9]+:([0-9a-zA-Z_\-]{20})@` |
| in-URL | `gitlab_pipeline_trigger_token_in_url` | 530 / 532 | 558 | `/trigger/pipeline\?(?:[0-9a-zA-Z_.%\[\]=-]{1,100}&){0,10}token=([0-9a-f]{30})\b` |
| session cookie | `gitlab_session_cookie` | 547 / 549 | 576 | `(?:cell-[0-9]+-)?[0-9a-f]{64}` |

`glrct-` appears **0 times** on GitLab's vendor prefix table (measured) — it exists only in
the rules file, so a shape built on it is tier-A-rules-only, not vendor-docs-corroborated.

### 6c. Also still unlanded (routable forms of already-landed prefixes)

`glpat-` routable (snap-id 28 / snap-regex 30 / live-id 29) and versioned-routable
(49 / 51 / 51), `glrt-`/`glrtr-` routable (134 / 136 / 140), `gldt-` routable
(322 / 324 / 338) — all four are already named in the scanner's "Known limits" text, so
they are *declared* limits rather than *silent* gaps. `glagent-` routable (356 / 358 / 374)
and `glwt-` (373 / 375 / 392) are in that list only as plain prefixes; their routable forms
are not separately declared.

## 6d. R6 — the frozen statement names S141, the registry names S143 (routed)

C2's frozen statement says "S141 line 72 gives the 76-character length" (and
`claims.json` names S141 three times, S142 three times). But:

* S141's registry row is `status: rejected`, `used-by: —` — at the freeze **and** at HEAD
  (I compared the row at `347519f` and at `43cc15e`: identical).
* The row that actually carries the length at HEAD is **S143** — `status: mined`,
  `used-by: corpus/instruments/capture-secret-scan.py, corpus/knowledge/github-refresh-tokens-and-gitlab-jwt-tokens.md`,
  "supersedes S141".
* S143 did not exist at the freeze: `git show 347519f:corpus/SOURCES.md` has **0** S142
  rows and **0** S143 rows. Both rows were added by the integration commit `43cc15e`.
* The landed knowledge entry cites S143 correctly ("S143 (supersedes S141) … superseding
  S141") and its falsification checklist still says `sed -n '72p' <S141 capture>`.

So the landed corpus is internally consistent and the S143 row is the better citation; the
stale part is the frozen claim text and the entry's checklist wording, which still says
"S141 capture" for a file that is deliberately not committed as a capture. C2's predicate
does not test any registry row, so this re-scores nothing. Round-96 should retire "S141"
from prose wherever a *live* row is meant and point at S143.

## 7. Which of the three rows I would admit, reject or re-tier

| row | my call | why |
|---|---|---|
| **S140** (`rules/mit/gitlab/gitlab.toml`, tier A, `mined`, used-by the scanner) | **ADMIT, unchanged** | GitLab's own machine-readable rules, re-fetched byte-identical to the pinned raw digest (200/20,228/`14854f71…`), `source-recheck` rc=0 with three pinned quotes, and the committed capture's anchors are what every lane citation uses. It is the strongest source in the round. Only the "line numbering preserved" wording needs qualifying (R2). |
| **S142** (GitHub Docs refresh-token page, tier A, `mined`) | **ADMIT, unchanged** | GitHub's own first-party statement; re-fetched byte-identical to the committed capture; line 169 carries the prefix and the row correctly states the page gives no length. The one gap is mechanical, not editorial: the capture has no manifest (R1) and the row pins no digest (R4) — both closed by the same one-file addition. |
| **S141 → S143** (`rules/mit/github/github.toml`, tier B, `mined`) | **RE-TIER — keep as corroboration, move the primary ground to tier A** | As written it is third-party for a GitHub shape, which the row itself says. But a tier-A ground exists and I re-derived it live: GitHub's own REST docs page publishes the `ghr_`+76 example at converted line 311 (80 bytes / 76 tail / sha256 `c7ad99a1…060d`, the same value already allowlisted). The obstacle is measured, not theoretical: the new shape makes the lane's capture tool refuse that page (`INTAKE-REFUSED … shape=github-refresh-token line=311`), so round 96 must first unblock it with a digest-bound allowlist row for the new capture path or S140's structural redaction. Until then S143 is the honest, working ground and the claim's predicate does not turn on tier — so this is a quality improvement to schedule, not a defect to raise against round 95. |

**Overall:** the round's sourcing is sound and re-derivable. The three anchors hold
byte-for-byte, the base instrument matches neither new shape, the selftest really did
101 → 115, and the one allowlist row is live and consumed. The one thing round 95 should
not ship without fixing is **R1**: the round's own new capture directory has no manifest,
so the lane's capture-binding audit is red for a directory round 95 created, and the
round's new source cannot be re-checked.

---

## Receipts

All commands were run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin` with scratch
`/fast/scratch/hyaku/kasegi-r95/ScoutSources` (removed on exit; `TMPDIR` passed explicitly).
Fixture clones were created with `mktemp -d` + `git clone --no-local`, and
`git -C <dir> rev-parse --show-toplevel` was asserted to equal the fixture dir before any
checkout in it. No lane git/jj state was mutated; no file outside the report and receipt
paths was written.

| receipt | what it holds | observed |
|---|---|---|
| `ScoutSources-receipts/01-s142-refetch.txt` | S142 curl + lane-instrument re-capture + diff vs committed | HTTP 200, 196,832 bytes, live sha `f57ab983…9804`; instrument: `snapshot_bytes=7944 sha256=727ba6a0…2864`; `diff` rc=0, 0 lines; committed `727ba6a0…2864`, 7,944 bytes, 182 lines |
| `ScoutSources-receipts/02-s142-anchor-line169.txt` | the located anchor | line 169 printed; `grep -n ghr_` → 1 occurrence, line 169 only; quote in file |
| `ScoutSources-receipts/03-s141-refetch-and-anchor.txt` | S141 curl + digest cross-check + lines 69–72 + intake refusal | HTTP 200, 3,955 bytes, sha `02c67ceb…83e0` = round-94 receipt digest; line 72 `regex = "ghr_[0-9a-zA-Z]{76}"`; `INTAKE-REFUSED … github-token line=6` and `… github-refresh-token line=71` |
| `ScoutSources-receipts/04-s140-refetch-and-anchors.txt` | S140 curl + digest cross-check + lines 428–464 | HTTP 200, 20,228 bytes, sha `14854f71…1b5` = manifest "raw" digest; committed capture `f3fd09e4…158c`, 25,537 bytes, 563 lines; the three keyword lines and three regex lines printed |
| `ScoutSources-receipts/05-round96-gitlab-family-leads.txt` | all 24 unlanded S140 rules: prefix, rule id, snapshot line, raw line, verbatim regex | table reproduced from the committed capture and the live fetch |
| `ScoutSources-receipts/06-s140-line-number-drift.txt` | snapshot-vs-raw line map for all 30 rules | `snapshot lines=563 live lines=592`; delta 0 → +29; JWT anchors 428→450, 445→468, 462→486 |
| `ScoutSources-receipts/07-landed-scanner-vs-source-regexes.txt` | landed scanner vs. S140/S141 regexes, family sweep, routable/floor/placeholder probes, tail-overflow probes | `github-refresh-token` on `ghr_`+76 only; `gitlab-jwt-token` on glcbt/glsat/gliamat; legacy `glcbt-`, all routable forms, glptt/glft/gloas/glimt/glsoat/glagent/glwt → NO HIT; 1001-char tail → NO HIT (source MATCH) |
| `ScoutSources-receipts/08-round95-missing-manifest.txt` | `capture-binding-check` at 4 revisions + manifest inventory + `source-recheck` | base `missing_manifest=0`; freeze/landing/HEAD `missing_manifest=1` + `FAIL rule=missing-manifest dir=round-95`; round-95 is the only dir without a manifest; `source-recheck` S142 → `manifest UNAVAILABLE reason=missing` rc=2 vs S140 → rc=0 |
| `ScoutSources-receipts/09-tierA-ghr-length-ground-and-its-blocker.txt` | tier-A ground for the 76-length, before/after the new shape | base capture OK (6560 bytes, sha `8582eca5…11f0`); HEAD `INTAKE-REFUSED … github-refresh-token line=311`; matched `ghr_` value 80 bytes / 76 tail / sha `c7ad99a1…060d`, identical to the C2 allowlist row's digest; the C2 allowlist row printed from the landing |
| `ScoutSources-receipts/10-gitlab-vendor-prefix-table.txt` | GitLab's own prefix table (tier-A corroboration) | HTTP 200, 67,805 bytes, sha `765becf3…f4b6`; prefix table extracted; `glrct-` count 0, `glptt-`/`glft-`/`glimt-`/`glwt-`/`glsoat-`/`glffct-`/`gloas-`/`glagent-` all present |
| `ScoutSources-receipts/11-s141-vs-s143-citation.txt` | R6: the frozen claim's S141 citation vs. the registry rows at the freeze and at HEAD | S141 `status=rejected used-by=—` at both `347519f` and `43cc15e`; S142/S143 rows: 0 present at the freeze, 1 each at HEAD; S143 `status=mined used-by=` the scanner + the knowledge entry; the landed entry cites S143 but its checklist still says `<S141 capture>` |

Additional commands cited inline (not duplicated into a receipt file):

* `sha256sum corpus/instruments/capture-secret-scan.py` → `66edd661…6707` (equals the
  frozen candidate pin; the landed file and `.ufo/waves/round-95/c2/candidate-scanner.py`
  are byte-identical); `claim-package-check.py` → `8b6f8493…c8e6` (equals the frozen gate
  pin); same two digests recomputed from `git show 38e7319:…`.
* `python3 -B corpus/instruments/capture-secret-scan.py --selftest` at HEAD →
  `SELFTEST-RESULT pass cases=115`; at base `9ef0126` (fixture clone) → `cases=101`.
* Base instrument probed on `ghr_`+76 and the three JWT forms → all `NO HIT`.
* `python3 -B corpus/instruments/capture-secret-scan.py --lane . --rev HEAD` →
  `scanned=2477 hits=0 files=0 allowed=26 unused_allow=0 rc=0`.
* `python3 -B corpus/instruments/source-recheck.py --manifest
  corpus/source-snapshots/round-94/manifest.json --source S140` →
  `sha256 OK`, `Q01/Q02/Q03 OK occurrences=1`, rc=0.
* `grep -c 'The token starts with ghr_' corpus/source-snapshots/round-95/S142.txt` → 1;
  `sed -n '429p;446p;463p' corpus/source-snapshots/round-94/S140.txt` → the three
  `keywords = [...]` lines.
* Registry row state at HEAD: S140 `mined`, S141 `rejected`, S142 `mined`, S143 `mined`
  (S143 marked "supersedes S141"; the round-94 change-log line for S141 was not rewritten).

**Tooling:** none installed, none upgraded. No pacman/uv/npm transaction was performed, so
there is no tool/channel/version to record.
