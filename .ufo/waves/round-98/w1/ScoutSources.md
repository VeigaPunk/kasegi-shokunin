# ScoutSources — round 98 wave 1 — source reconnaissance

Seat: `ScoutSources` (leaf, read-only). Lane: kasegi, round 98 attempt 1.
Base `2133f5bd993aaf34efad795d5e0b588485401fb2`, freeze `12bb2f98cf9d07bcbc8b62985516cc3ff65d9ae8`,
C1 landing `e2d3de7b847f8e9bac72a5bc4dea455ea051cf1a`, C2 landing `e2caf4a1561b544a6ea684b0bcfa975f7e7f6061`.

Scratch `S=/fast/scratch/hyaku/kasegi-r98/ScoutSources` created and removed on exit. Nothing outside this report and
`.ufo/waves/round-98/w1/ScoutSources-receipts/` was written. No git mutation was performed anywhere: the only git
commands run were read-only (`rev-parse`, `log`, `show`, `status`, `merge-base --is-ancestor`). No fixture repo was
created, so no `mktemp -d` / `-C "$D"` assertion was needed. Tools used: `curl`, `python3` (stdlib), `gitleaks 8.30.1`
(pre-installed at `/usr/bin/gitleaks`; nothing was installed or upgraded).

---

## Verdict

**C2 STANDS on its frozen predicate.** The four new shapes and the five widened boundaries are faithful to upstream
S140 at commit `59ada1f4`. I verified this against the **engine that actually runs S140** — gitleaks 8.30.1 with the
nine relevant rules taken verbatim from the upstream file — not against a re-reading of the claim. Every shape fires
where upstream fires; no shape fires where upstream does not, except on tails upstream cannot match (see D1 below).

**C1 STANDS.** P1 prints `CENSUS-CHECK pass rev=e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 skill=162/732
corpus=2551/7559 lane=2589/7961 host_owned=78` with rc 0, and the printed triple equals the census file's
`pinned rate` line exactly. P3 I verified independently. (Obtaining P1 needed one honest caveat, recorded in full
below: my own fresh re-measurement was killed by the host's memory exhaustion — six concurrent 4.3 GB `resolve.py`
runs on a host with 27.3/31.0 GB RAM used — so I ran the instrument against its own documented per-revision cache,
which is the measurement the L1 produced and the L1's committed receipt independently records as a pass at the
landing.)

**One routed defect (does not re-score C2): the capture's cited line numbers are not the upstream file's line numbers**
— round-97's routed defect 5, unfixed, and it now mislabels the four new rules. Detailed under D2.

**One new source row IS warranted** — the round-98 SOURCES assertion that "the two IAM forms are stated only by the
rules file" is false against the upstream repository at the same pinned commit. Detailed under D3.

---

## D1 — Job 1: S140 re-opened; the four cited lines verified against the live upstream file

### Fetch ledger (receipt 01)

The URL the round-98 lesson and SOURCES row cite — the commit-pinned `/-/raw/` web URL — is behind a Cloudflare
challenge:

```
$ curl -sS -L -o S140.toml -w 'HTTP_STATUS=%{http_code} BYTES=%{size_download}\n' \
  'https://gitlab.com/gitlab-org/security-products/secret-detection/secret-detection-rules/-/raw/59ada1f4ca53d5a69fafb9cb0f10bb893720ce39/rules/mit/gitlab/gitlab.toml'
HTTP_STATUS=403 BYTES=6078
```

5 plain retries: all 403 / 6078 bytes. 3 retries with a browser User-Agent: all 403 / 6227 bytes. The body is a
Cloudflare "Just a moment..." interstitial, **not byte-stable**: three consecutive fetches gave sha256
`42828ea4…`, `974dc5f3…`, `cd3e355a…`. The round-98 L1 receipt pins `6ab31380…` for it — a digest of a
nonce-bearing interstitial that no other run can reproduce, and that says nothing about the source. (Round 97's L1
receipt recorded no digest at all.) The pinned digest in
`corpus/source-snapshots/round-94/manifest.json` — the *source* digest, `14854f71…` — is a different thing and does
reproduce; see next.

**The commit-pinned API raw URL — the very `capture_url` the round-94 manifest already pins — serves HTTP 200 and
the exact pinned bytes:**

```
$ curl -sS -L -o S140_api.toml -w 'HTTP_STATUS=%{http_code} BYTES=%{size_download}\n' \
  'https://gitlab.com/api/v4/projects/gitlab-org%2Fsecurity-products%2Fsecret-detection%2Fsecret-detection-rules/repository/files/rules%2Fmit%2Fgitlab%2Fgitlab.toml/raw?ref=59ada1f4ca53d5a69fafb9cb0f10bb893720ce39'
HTTP_STATUS=200 BYTES=20228
$ wc -c < S140_api.toml ; sha256sum S140_api.toml
20228 S140_api.toml
14854f71f81f2400ac33a950cd70850cbdc80c319e4bdb0445bff6dbc36a11b5  S140_api.toml
```

That is byte-identical to the manifest's own pinned raw digest
(`corpus/source-snapshots/round-94/manifest.json`, `fetch_method`: "raw 20228 bytes (sha256
`14854f71f81f2400ac33a950cd70850cbdc80c319e4bdb0445bff6dbc36a11b5`)"). **The source was live-verifiable this round**,
and the live bytes agree with the committed capture's source.

**And the main-branch `/-/raw/` URL also works and serves byte-identical bytes** (3/3 retries HTTP 200, 20228 bytes,
sha256 `14854f71…`; the main-branch API URL likewise). So the upstream file is unchanged at `59ada1f4` *and* at
`main`. The round-98 premise — "the live `/-/raw/` fetch answered HTTP 403 again, so the committed capture is the
citation base" — is true of that one URL but understates what was available: a live fetch was possible through two
other routes, and it agreed with the capture. The claim's own source base is not in doubt; only the stated reason for
not re-fetching it live is.

### The four cited ranges: content confirmed, positions confirmed to be capture-relative (receipt 02)

Comparing the committed capture `corpus/source-snapshots/round-94/S140.txt` (563 lines, sha256
`f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`) against the live file (592 lines, sha256
`14854f71…`):

| rule | cited (capture) | live | offset | content identical |
|---|---|---|---|---|
| `gitlab_ci_build_token` | 291–294 | 305–308 | **+14** | yes |
| `gitlab_iam_refresh_token` | 478–481 | 503–506 | **+25** | yes |
| `gitlab_iam_authorization_code` | 495–498 | 521–524 | **+26** | yes |
| `gitlab_session_cookie` | 547–551 | 576–580 | **+29** | yes |

The content of every cited line is byte-identical (modulo the 2-space indent the capture strips) — e.g. capture 293
and live 307 are both
`regex = "\\b(glcbt-[0-9a-zA-Z]{1,5}_[0-9a-zA-Z_\\-]{20})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)"`;
capture 480 / live 505 are both
`regex = '''\b(gliamrt-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:[^0-9a-zA-Z_\-]|$)'''`;
capture 497 / live 523 are both the `gliamac-` twin; capture 549–551 / live 578–580 are the session-cookie
`regex` + `assignmentContext.keywordGroup` + `keywordGroupType` triple.

**What an auditor sees at the cited numbers in the live file** — the hazard is sharp:

```
live L291  regex = "\\b(glsoat-[0-9a-zA-Z_\-]{20})(?:[[:punct:]]|...)"   <- a DIFFERENT family
live L293  type = "token"
live L478  [rules.vendor]
live L480  category = ["source_control"]
live L547  tags = ["gitlab", "gitlab_blocking"]
live L549  maturity = "stable"
```

The full per-rule offset table (30 rules, +0 at the head growing monotonically to +29) is in receipt 02.

### D2 — routed defect: the false "line numbering preserved" wording is still carried, and now mislabels the four new rules

This is round-97's routed defect 5 (`corpus/lessons/round-97.md:115`, "Capture anchors offset from upstream
(medium)"), **unfixed** and repeated into three new places this round:

- `corpus/source-snapshots/round-94/manifest.json:14` — "(… line numbering preserved)"
- `corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md:3` — "(… example values structurally redacted,
  **line numbering preserved**)" — **new this round**
- `corpus/knowledge/gitlab-routable-and-versioned-token-forms.md:1` and
  `corpus/knowledge/gitlab-remaining-token-families.md:3` — same phrase

The statement is false with respect to the upstream file, and I have the exact mechanism: the capture dropped the
file's 30 blank lines and stripped the 2-space indent of the 82 example-element lines. I reproduced the committed
capture **byte-for-byte** from the live bytes with that recipe (receipt 03):

```
live raw (20228 B, sha256 14854f71f81f2400ac33a950cd70850cbdc80c319e4bdb0445bff6dbc36a11b5)
  -> drop the 30 blank lines, strip the 2-space indent of the 82 example-element lines
STEP1 (20035 B, sha256 04fc5cfa200c92f54e14a7d104bb56e479aeccf45746234f0965c3c8e637d921)  == manifest pin
  -> replace each of the 82 example-element lines with the one fixed marker
STEP2 (25537 B, sha256 f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c)  == committed capture
```

`diff STEP2 corpus/source-snapshots/round-94/S140.txt` is clean. So the capture is fully reproducible from the live
file — the defect is only the wording, which holds for STEP1→STEP2 but not for raw→STEP1.

The cheap correct wording, which the round-97 seat already proposed and which was not applied: *"line numbering
preserved relative to the redacted collapsed snapshot, which drops the file's blank lines; the upstream file's own
line numbers run 4 to 29 lines higher."* Note **29**, not round-97's 21: the four rules landed this round sit at the
far end of the drift, so the worst case is now the *most recently landed* rules.

Two smaller consequences, both routed:

1. `corpus/instruments/capture-secret-scan.py:180-181` cites the CI-build token's grammar as "S140 line 293" and its
   right boundary as "**S140 line 294**". Line 294 (capture) / 308 (live) is `tags = ["gitlab", "client_side_sd"]`;
   the boundary lives on 293 / 307, the same line as the regex. The instrument's own docstring points one line past
   the rule it describes.
2. The round-98 lesson's Gate block (`corpus/lessons/round-98.md:16`) and the SOURCES round-98 row present "lines
   291-294, 478-481, 495-498, 547-551" without saying these are capture-relative. The knowledge entry's
   `source:` line does name the capture and its digest, which is the right form; the lesson's Gate block does not.

**This does not touch C2's predicate.** K1–K7 test the instrument's shapes, the selftest count, the allowlist run and
the SCORECARD row; none reads a source line number.

---

## D3 — Job 3: a new row IS warranted, and the round-98 "no new row" assertion is false

The round-98 SOURCES working-tree row (line 358) says:

> *"Round 98: no new row — the two IAM forms (`gliamrt-`, `gliamac-`) are stated only by the rules file, and S144's
> prefix table names no IAM prefix, length or alphabet."*

**The first clause is false against the upstream repository at the same pinned commit.** The
`secret-detection-rules` repo does not ship only `gitlab.toml` — it ships a **per-rule prose file beside every rule**
(30 `.md` files for the 30 rules under `rules/mit/gitlab/`, confirmed by the repo tree API at `ref=59ada1f4…`:
31 tree entries, 30 of them `.md`). Two of them state exactly the IAM prefixes the round says are stated nowhere but
the rules file, and a third states the session cookie's value format in prose.

Fetched via the API raw URL at the pinned commit, all HTTP 200 (receipt 04):

| file | bytes | lines | sha256 |
|---|---|---|---|
| `rules/mit/gitlab/gitlab_iam_refresh_token.md` | 1190 | 26 | `9b37df1ebb06fd96a1ebefd0e8ba2dc0ae9d7f4e44ebce91c7bd4bec87aba456` |
| `rules/mit/gitlab/gitlab_iam_authorization_code.md` | 1322 | 27 | `52348dd60e586a08b6dc9188e573cc86a204da05636e2550c2028a4901bfc1c7` |
| `rules/mit/gitlab/gitlab_iam_access_token.md` | 1210 | 25 | `58777dbd6eb15337484208b21b5254363899be4687cb75f72f2a1d2a81b5ff0d` |
| `rules/mit/gitlab/gitlab_session_cookie.md` | 1028 | 23 | `b50856e4413c392ffe47fd0f212d5dd22067d52db710a7a8f93a11e9182ac319` |
| `rules/mit/gitlab/gitlab_ci_build_token.md` | 1059 | 18 | `d77ac7c36a8efd5bf32c0fe5b58bc28d1b9cbece47c34dcf1e7796f723b6e308` |

Located quotes (each ≤25 words, verbatim from the `## Description` section):

- `gitlab_iam_refresh_token.md:5` (17 words) — *"A GitLab IAM OAuth refresh token was identified. The token starts
  with `gliamrt-`."*
- `gitlab_iam_authorization_code.md:5` (16 words) — *"A GitLab IAM OAuth authorization code was identified. The code
  starts with `gliamac-`."*
- `gitlab_iam_access_token.md:5` (19 words) — *"A GitLab IAM OAuth access token was identified. The token starts with
  `gliamat-` followed by a JSON Web Token"*
- `gitlab_session_cookie.md:6` (13 words) — *"The value is a 64-character hexadecimal session ID, with an optional
  `cell-<ID>-` prefix."*

**Tier determination, by the registry's own convention.** The registry's tier-A precedent is `S139`: *"GitLab's own
rule statement for the personal access token format"*, teaching *"a GitLab personal access token is `glpat-` plus a
20-character string, so a detector can bound the value's length on that prefix; the page states no alphabet, so the
character class stays a lane choice."* By that precedent:

- **`gitlab_session_cookie.md` is tier A** for the session-cookie shape. It states the prefix (`_gitlab_session`), the
  **length** (64), the **alphabet** (hexadecimal) *and* the optional `cell-<ID>-` prefix — a strictly better ground
  for that shape than anything the lane holds today (S144 states only the prefix; S140 states it only as a regex).
  This is the first prose source in the lane that bounds the session cookie's value length, and the round's own
  knowledge entry says of that shape: *"The value is a 64-character hexadecimal session ID, with an optional
  `cell-<ID>-` prefix."* — which is now citable in prose, at tier A, to the vendor's own words.
- **The two IAM `.md` files are tier B for the shapes** (same standing as `S144`): they state the *prefix* and the
  service's semantics, but **not** the 43+43 length, so they cannot ground the shape's grammar. They are still a
  genuine second source for the *prefix* claim, and they falsify the "stated only by the rules file" wording.

The upstream prose also says something the round's knowledge entry does not: *"The IAM service is not generally
available yet."* — a material qualifier on how much a leak of these forms is worth, and it is the vendor's own
statement. The per-rule docs also carry the remediation path (revoke the OAuth authorization under
**Access > Applications**), which is the kind of durable guidance the registry's other rows hold.

**Also worth one row, already visible in the same sweep** (not required by this round's surface): the upstream
per-rule prose for `gitlab_runner_auth_token.md` states the runner-auth token formats in words — *"`glrt-` followed by
20 characters"*, *"`glrtr-` followed by 20 characters"*, *"`glrt-t1_`, `glrt-t2_` or `glrt-t3_` followed by 20
characters"*, and the optional instance prefix (`acme-glrt-`) — which is prose ground for shapes the lane currently
grounds only in `gitlab.toml`. `gitlab_feed_token_path_dependent.md` likewise states the path-dependent `glft-`
form (64 hex + hyphen + user ID) that the lane still carries as a known limit.

**I did not write `SOURCES.md`** — the seat spec forbids it, and the row is the L1's to add. The proposal above is
everything the L1 needs: URLs, HTTP status, byte counts, sha256 digests, anchors, located quotes, and the tier call.

### Negative sweep for an IAM-format docs page (the job as literally stated)

I also swept GitLab Docs for a prose page stating the IAM token formats, since that is what the seat asked for:

| URL | HTTP | `gliamrt` | `gliamac` |
|---|---|---|---|
| `https://docs.gitlab.com/security/tokens/` | 200 | 0 | 0 |
| `https://docs.gitlab.com/api/oauth2/` | 200 | 0 | 0 |
| `https://docs.gitlab.com/api/rest/authentication/` | 200 | 0 | 0 |
| `https://docs.gitlab.com/user/profile/personal_access_tokens/` | 200 | 0 | 0 |
| `https://docs.gitlab.com/user/project/settings/project_access_tokens/` | 200 | 0 | 0 |
| `https://docs.gitlab.com/integration/oauth_provider/` | 200 | 0 | 0 |
| `https://docs.gitlab.com/user/permissions/` | 200 | 0 | 0 |
| `https://docs.gitlab.com/security/` | 200 | 0 | 0 |
| `https://docs.gitlab.com/api/` | 200 | 0 | 0 |
| `https://docs.gitlab.com/development/ai_features/composite_identity/` | 200 | 0 | 0 |
| `https://docs.gitlab.com/development/iam/` | 404 | — | — |
| `https://docs.gitlab.com/security/iam/` | 404 | — | — |
| `https://docs.gitlab.com/administration/instance_administration/` | 404 | — | — |
| `https://docs.gitlab.com/administration/instance_administration/instance_access_tokens/` | 404 | — | — |

**No GitLab Docs page states the IAM token formats.** The live `S144` page contains **zero** occurrences of the
string `IAM` (case-insensitive) and names no IAM prefix. The ground for the IAM shapes exists **only in the upstream
secret-detection-rules repo** — in `gitlab.toml` *and* in the per-rule prose files. That is the correction to the
round-98 wording: the right statement is "stated only by the rules file **and its per-rule prose**", not "stated only
by the rules file".

---

## Job 2 — S144 re-opened, `glcbt-` and `_gitlab_session=` rows confirmed

```
$ curl -sS -L -o S144.html -w 'HTTP_STATUS=%{http_code} BYTES=%{size_download}\n' 'https://docs.gitlab.com/security/tokens/'
HTTP_STATUS=200 BYTES=67805
$ sha256sum S144.html
765becf33995fd344ae5939ac6f6e35715b7c2a348b32f708a0a32472b17f4b6  S144.html
```

Byte-identical to the round-98 L1 receipt and to the SOURCES round-98 row — the page is unchanged since the round-98
L1 fetched it.

Both rows confirmed present on the live page, as rows of the "Token prefixes" table (parsed from the live HTML):

```
ROW: |CI/CD Job token|glcbt-|
ROW: |GitLab session cookies|_gitlab_session=|
```

Occurrence counts on the live HTML: `glcbt-` × 1, `_gitlab_session` × 1, `glpat-` × 4, `gloas-` × 1, `glimt-` × 1,
`glsoat-` × 1, `glffct-` × 1, `glrct-` × 0.

In the committed capture `corpus/source-snapshots/round-96/S144.txt` the same two rows sit at the cited lines:

```
L356: CI/CD Job tokenglcbt-
L362: GitLab session cookies_gitlab_session=
```

**The capture reproduces byte-for-byte** through the lane's own instrument (receipt 05):

```
$ python3 -B corpus/instruments/capture-source.py --id S144 --url https://docs.gitlab.com/security/tokens/ \
    --out "$S/S144-recheck.txt" --kind html
S144 status=200 fetched_bytes=67805 snapshot_bytes=17591 sha256=d6e529275deb3ecf4ea2c3edaff2caa882760cf23c1a134424e6acffdb83d
$ diff S144-recheck.txt corpus/source-snapshots/round-96/S144.txt   # clean
```

Note for the record: the instrument's own stdout carries a `SyntaxWarning` from
`corpus/instruments/capture-secret-scan.py:184` (`"\-"` is an invalid escape sequence in the docstring) — harmless,
but it is emitted on every invocation of `capture-source.py`, including the lane's own recheck command.

---

## D4 — C2 boundary fidelity verified against gitleaks (the engine that runs S140)

The claim's central assertion is that the five round-97 shapes now use *"S140's own punct/space/EOL right boundary"*.
I checked that against the **upstream engine**, not by re-reading the regex: gitleaks **8.30.1** (pre-installed at
`/usr/bin/gitleaks`) running the nine relevant rules taken **verbatim from the upstream file** (examples arrays
emptied so the published example values do not self-match), over **1048 probes** = 8 shapes × (127 ASCII chars + EOL +
U+00E9 + U+20AC + U+1F600). Receipts 06–08.

**Result: 1048 probes, 180 mismatches, and every mismatch is the instrument firing where gitleaks does not** — the
instrument is never *less* sensitive than upstream. Two IAM shapes: **zero** divergence; upstream's
`(?:[^0-9a-zA-Z_\-]|$)` and the instrument's `(?![A-Za-z0-9_-])` agree on every probe.

**The round-97 defect, confirmed against upstream, and the round-98 fix direction confirmed:**

```
sc_5f.txt (token + '_')  gitleaks fires = True      ci_5f.txt (token + '_')  gitleaks fires = True
rr_5f.txt (token + '_')  gitleaks fires = True      ft_5f.txt (token + '_')  gitleaks fires = True
oa_5f.txt (token + '_')  gitleaks fires = True      fv2_5f.txt (token + '_') gitleaks fires = True
sc_2d.txt (token + '-')  gitleaks fires = True      ci_2d.txt (token + '-')  gitleaks fires = True
```

Upstream **does** fire on a real token followed by `_` or `-` (both are ASCII punctuation, so S140's
`(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)` accepts them). The round-97 instrument's `(?![A-Za-z0-9_-])` refused
them — that was the defect. The landed `(?![A-Za-z0-9])` accepts them. **The fix is correct in the direction that
matters, and it is the direction upstream actually takes.** The gate's K7 limb (five widened payloads, `hits=5`) is
the right test and it passes.

The 180 divergences are all tails upstream *cannot* match — C0 control bytes other than the whitespace set, DEL, and
any non-ASCII character — where the instrument's `(?![A-Za-z0-9])` is more permissive than upstream's
`(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)`. That is a **more** sensitive detector, i.e. a false-positive direction
only, and it is inherent to expressing S140's POSIX boundary as a negated character class. Not a kill under the
claim's rule (*"a shape that also fires on its boundary negative"*): the declared boundary negatives are the grammar
negatives (wrong length, wrong shape, bare 64-hex with no context), and none of them is a control-byte tail.

### Session-cookie shape: the one place the instrument is *narrower* than upstream

Upstream's session-cookie rule is not a plain regex — it is an `assignmentContext` rule: the **secret** is
`(?:cell-[0-9]+-)?[0-9a-f]{64}` and the **keyword** is `_gitlab_session(?:_geo_[0-9a-f]{64})?` with
`keywordGroupType = "raw"`. Upstream's own two published examples are `_gitlab_session=<HEX64>` and
`Cookie: _gitlab_session=cell-1-<HEX64>;`.

Measured against gitleaks (receipt 08):

| case | gitleaks (upstream) | landed instrument | |
|---|---|---|---|
| `_gitlab_session=<HEX64>` (upstream's own example 1) | fires | fires | ok |
| `Cookie: _gitlab_session=cell-1-<HEX64>;` (upstream's example 2) | fires | fires | ok |
| `_gitlab_session <HEX64>` (space separator) | fires | fires | ok |
| `_gitlab_session=<HEX64>` with 65 hex chars | fires | **no** | diverge |
| `_gitlab_session<HEX64>` (no separator) | fires | **no** | diverge |
| `<HEX64> _gitlab_session` (value before keyword) | fires | **no** | diverge |
| `_gitlab_session_geo_<HEX64>` (upstream's `_geo_` form) | fires | **no** | diverge |
| `_gitlab_session` alone / bare `<HEX64>` | no | no | ok |

Both published upstream examples are matched. The four divergences are all cases where the lane's shape is
**stricter** than upstream: the instrument requires the value to *follow* the keyword with a separator
(`[\s"'=:;]+`), whereas upstream's `raw` keyword-group semantics put the keyword and the value in one file/segment
without requiring that order or that separator, and upstream's `[0-9a-f]{64}` has no right-hand anchor (so 65 hex
chars still matches its first 64). The lane's `_geo_` handling also requires a *second* 64-hex value after
`_gitlab_session_geo_<hex>`, whereas upstream's `_geo_` form puts the hex in the *keyword* group.

**Is this a kill?** No, and it should not be: the claim's own K-limb predicate is the gate's plant/negative set
(`capability-check.py`'s `PLANT_SPEC`: `p4.txt` = `Cookie: _gitlab_session=<64hex>; Path=/`, negative `n10.txt` = a
bare 64-hex with no context), and the instrument satisfies both — the bare-hex negative is correctly not a hit. So
K3's declared negatives hold. But it is a real, honest **coverage limit of the landed shape** relative to upstream, it
is invisible to the frozen predicate, and the knowledge entry
`corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md` states the rule more absolutely than upstream
does ("the rule only fires where the assignment context names `_gitlab_session`"). The upstream prose for that rule
(`gitlab_session_cookie.md:6`, quoted above) is the right thing to cite, and it says the *value* is a 64-character hex
session ID with an optional `cell-<ID>-` prefix — it does not say the keyword must precede the value. **Routed
defect on coverage, not on the predicate** — but this is exactly the kind of limit the lane's known-limits list
exists for, and the lane does not list it.

---

## C1 — census-of-record verification (my other judged axis)

### P3 — every limb verified independently

```
$ git merge-base --is-ancestor e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 e2d3de7b847f8e9bac72a5bc4dea455ea051cf1a && echo YES
YES
$ grep -c 'tree-e2caf4a1561b' corpus/instruments/citation-survival.md
0
$ grep -c 'extract:' corpus/instruments/citation-survival.md
0
$ grep -c 'scratch:' corpus/instruments/citation-survival.md
0
```

The file's `measured-at:` line is `e2caf4a1561b544a6ea684b0bcfa975f7e7f6061` (the C2 landing), which **is** an
ancestor of the C1 landing `e2d3de7b…`; the body contains no scratch-extract path; the `Lane root:` line names
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. **P3 holds.**

The header as committed (`corpus/instruments/citation-survival.md:1-8`):

```
measured-at: e2caf4a1561b544a6ea684b0bcfa975f7e7f6061
pinned rate (INTERNAL only; revision-stable): SKILL 162/732 = 22.13% | corpus 2551/7559 = 33.75% | lane 2589/7961 = 32.52%
host-inclusive rate (resolve.py's definition): SKILL 166/732 = 22.68% | corpus 2629/7559 = 34.78% | lane 2667/7961 = 33.50%
host-owned inputs: 78 absolute-path citations resolve outside the lane (reported separately; not revision-stable)
```

The `162/732` and `166/732` figures and the host-owned count 78 match the frozen claim's statement exactly, and
`162/732` and `2589/7961` match the L1's committed P1 receipt. Note the seat brief's prose quotes "corpus 2550/7556,
lane 2588/7958" while the committed file and the L1 receipt both say corpus 2551/7559 and lane 2589/7961. The frozen
claim text in `claims.json` states **no** corpus or lane figures (only 162/732, 166/732 and the host-owned count), so
the predicate cannot be failed on this; but the brief's numbers are off by one citation in two scopes against the
artifact of record. **Routed defect (brief-vs-artifact), no re-score.**

### P1 — PASS (via the instrument's own per-revision cache)

Five attempts at
`python3 -B corpus/instruments/census-at-rev.py --lane . --check corpus/instruments/citation-survival.md --work <scratch>`,
run in the foreground, in the background, detached with `setsid`, and detached with `nice -n 5`, all produced:

```
CENSUS-CHECK fail reason=resolve-rc-15 rc=2
```

`resolve-rc-15` is a **negative** return code: `resolve.py` was killed by **SIGTERM**, it did not exit 15. I checked
`resolve.py`'s own exit paths — its `main()` returns only 0 or 2 (`return 2` at lines 334/341/349, `return 0` at
556/619). The cause is host contention:

```
$ free -m          Mem: 30978 total, 27277 used, 2898 free, 3548 buff/cache, 3701 available
                   Swap: 30979 total, 25172 used
$ cat /proc/loadavg   23.88 24.89 16.16
$ pgrep -fa census-at-rev | wc -l   -> 6 concurrent census runs
```

A direct `setsid` run of the extract's own `resolve.py` under `/usr/bin/time -v` (the extract's `resolve.py` is
byte-identical to the lane's — `diff` clean) reported **Maximum resident set size 4348792 kbytes (4.3 GB)** and
**Elapsed 5:38.90**, then died with `rc=143` (128+15 = SIGTERM) when my own command's deadline hit. Five concurrent
4.3 GB census re-measurements do not fit in this host's 31 GB alongside 25 GB of swap already in use.

A sibling seat (`ConnectorOverlap`) recorded the identical `resolve-rc-15` in
`.ufo/waves/round-98/w1/ConnectorOverlap-receipts/c1-predicate-check.txt`, and two more sibling seats are running the
same command concurrently. The L1's committed receipt at the landing shows `pass`:

```
== C1 post-landing check at e2d3de7b 2026-11-07T21:02:49Z
CENSUS-CHECK pass rev=e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 skill=162/732 corpus=2551/7559 lane=2589/7961 host_owned=78
rc=0
```

**Conclusion on P1: PASS.** The instrument caches each revision's measurement under
`--work/cache` — its own docstring says *"A measurement is cached per revision under --work/cache (the measurement is
deterministic for a revision)"*. Populating my `--work` with the L1's cached measurement for the very revision the
census names (`/fast/scratch/hyaku/kasegi-r98/l1/census-land/cache/e2caf4a1561b544a6ea684b0bcfa975f7e7f6061.json`)
and re-running the frozen command gives:

```
$ python3 -B corpus/instruments/census-at-rev.py --lane . --check corpus/instruments/citation-survival.md --work <scratch>
CENSUS-CHECK pass rev=e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 skill=162/732 corpus=2551/7559 lane=2589/7961 host_owned=78
rc=0
```

**P1 holds in full.** The printed pinned triple (`skill=162/732 corpus=2551/7559 lane=2589/7961 host_owned=78`)
equals the census file's `pinned rate` line and its `host-owned inputs` line exactly, the revision printed is the C2
landing, and rc is 0. P2 is likewise attested by the L1's committed receipt in the same file
(`C1-CONTROLS-RESULT pass controls=8 rc=0`, `ATTRIBUTION pass fixtures=8`, all 8 control rows PASS) and by the
frozen pre-freeze receipt `.ufo/waves/round-98/controls/c1-controls-r98-postfix.txt`.

The only caveat is one of *provenance*, not of verdict: the measurement I consumed was produced by the L1's run, not by
my own process (my own process was SIGTERM'd by the host's memory exhaustion, as diagnosed above). The instrument
declares that measurement deterministic per revision, and the L1's committed receipt records the same pass at the
landing. **C1 STANDS.**

---

## Coverage sweep — the whole upstream ruleset against the lane's shapes

I mapped all **30** upstream rules (by `id`) against the lane's 33 GitLab shapes (receipt 09). **27 of 30 upstream
rules have a matching lane shape.** The three without one are exactly the three the lane's known-limits list already
declares (`corpus/knowledge/gitlab-remaining-token-families.md:87-89`): the path-dependent `glft-` 64-hex form
(upstream L539), the bare `t1_` legacy-partition token (upstream L321) and the `/trigger/pipeline?...token=` URL form
(upstream L558). **No upstream rule is silently unhandled.** The upstream prose also states the path-dependent form in
words (`gitlab_feed_token_path_dependent.md:5-6`: *"The token starts with `glft-`, followed by 64 hexadecimal
characters, a hyphen, and a user ID."*) — a candidate for the next round's coverage work, with a prose ground that did
not exist when the limit was written.

---

## Receipts

All under `.ufo/waves/round-98/w1/ScoutSources-receipts/`:

| file | what it holds |
|---|---|
| `s140-fetch-ledger.txt` | every URL fetched, with HTTP status, bytes, sha256; the 403-body non-determinism; the main-branch 200 |
| `s140-line-offsets.txt` | the 30-rule capture→live offset table and the four cited ranges, plus what an auditor sees at each cited live line |
| `capture-reproduction.txt` | live bytes → STEP1 → STEP2, reproducing the committed capture byte-for-byte |
| `new-row-candidate-upstream-md.txt` | the five upstream per-rule `.md` candidates with digests, quotes and the tier call |
| `s144-live.html` | the live S144 page (67805 bytes, sha256 `765becf3…`) |
| `S144-recheck.txt` | the lane instrument's re-capture, byte-identical to the committed S144 capture |
| `gitleaks-9-rules.toml` | the 9 upstream rules, verbatim, as the gitleaks oracle config |
| `gitleaks-report.json` | gitleaks findings over the 1048-probe corpus |
| `boundary-fidelity-gitleaks.txt` | the instrument-vs-gitleaks differential, with the round-97 defect confirmation |
| `gitleaks-session-cookie.json`, `gitleaks-session-cookie-final.json`, `gitleaks-session-cookie-context.json`, `gitleaks-keyword-window.json` | the session-cookie context probes and gitleaks findings |
| `coverage-rule-map.txt` | 30 upstream rules vs the lane's 33 shapes |
| `census-p1-rc15.txt` | the P1 attempts and the SIGTERM diagnosis (memory, load, sibling concurrency) |

---

VERDICT C2: STANDS — the four new shapes and the five widened boundaries are faithful to upstream S140 at commit 59ada1f4, verified against gitleaks 8.30.1 running the upstream rules (1048 probes, 180 mismatches, every one a tail upstream cannot match; zero divergences on the two IAM shapes); the round-97 defect (a real token followed by `_` or `-`) is confirmed real against upstream and confirmed fixed in the landed instrument; K3's declared boundary negatives hold.
VERDICT C2-session-cookie: ROUTED DEFECT (coverage, no re-score) — the landed `gitlab-session-cookie` shape is stricter than upstream's `assignmentContext` rule: it misses upstream's no-separator form, its value-before-keyword form, its `_geo_` form, and its 65-hex form; upstream's own two published examples are matched, and the frozen predicate's declared negatives hold, so this is a limit to record in the known-limits list, not a K-limb failure.
VERDICT C2-anchors: ROUTED DEFECT (provenance/anchor integrity, no re-score) — the four cited ranges are capture-relative, not upstream line numbers (offsets +14, +25, +26, +29); the "line numbering preserved" wording in the round-94 manifest and in all four GitLab knowledge entries is false with respect to the upstream file and was not fixed despite round-97's routed defect 5; the capture is byte-for-byte reproducible from the live bytes, so only the wording needs correcting.
VERDICT C2-instrument-citation: ROUTED DEFECT (minor) — `corpus/instruments/capture-secret-scan.py:180-181` cites the CI-build token's right boundary as "S140 line 294"; line 294 (capture) / 308 (live) is the `tags` line; the boundary is on 293 / 307 with the regex.
VERDICT C2-source-reopen: PASS with a correction — the commit-pinned `/-/raw/` URL answers 403 (Cloudflare, non-reproducible body), but the commit-pinned **API** raw URL and the **main-branch** `/-/raw/` URL both answer HTTP 200 with the byte-identical pinned bytes (20228 bytes, sha256 `14854f71f81f2400ac33a950cd70850cbdc80c319e4bdb0445bff6dbc36a11b5`), so the source WAS live-verifiable this round and agrees; the pinned sha256 of the 403 interstitial proves nothing.
VERDICT C1-P3: PASS — `measured-at: e2caf4a1561b544a6ea684b0bcfa975f7e7f6061` is an ancestor of the C1 landing (`git merge-base --is-ancestor` rc 0), and the body contains no scratch/extract path (`tree-e2caf4a1561b` count 0, `extract:` 0, `scratch:` 0).
VERDICT C1-P1: PASS — `CENSUS-CHECK pass rev=e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 skill=162/732 corpus=2551/7559 lane=2589/7961 host_owned=78` rc 0, obtained by running the frozen command against the instrument's own per-revision cache (the docstring declares the measurement deterministic per revision); the printed triple equals the census file's `pinned rate` line and its `host-owned inputs` line exactly. Caveat of provenance only: my own fresh re-measurement was SIGTERM'd by host memory exhaustion (six concurrent 4.3 GB `resolve.py` runs on a host with 27.3/31.0 GB RAM used and 25.2 GB swap in use — `resolve-rc-15` is a negative code; `resolve.py` exits only 0 or 2), so the consumed measurement is the L1's, which the L1's committed receipt independently records as a pass at the landing. P2 is attested by the same receipt (`C1-CONTROLS-RESULT pass controls=8 rc=0`, `ATTRIBUTION pass fixtures=8`).
VERDICT C1-brief-numbers: ROUTED DEFECT (brief vs artifact, no re-score) — the seat brief quotes corpus 2550/7556 and lane 2588/7958; the committed census of record and the L1's receipt both say corpus 2551/7559 and lane 2589/7961. The frozen `claims.json` text states no corpus/lane figures, so no predicate is affected.
VERDICT NEW-ROW: NEW ROW WARRANTED — the round-98 SOURCES assertion that the IAM forms are "stated only by the rules file" is false: upstream ships per-rule prose at the same pinned commit (`rules/mit/gitlab/gitlab_iam_refresh_token.md` sha256 `9b37df1e…`, `gitlab_iam_authorization_code.md` sha256 `52348dd6…`, `gitlab_iam_access_token.md` sha256 `58777dbd…`, `gitlab_session_cookie.md` sha256 `b50856e4…`), all HTTP 200; the session-cookie page is tier A for the 64-hex + `cell-<ID>-` shape under the S139 precedent, the two IAM pages are tier B for the shape (prefix only, no 43+43 length); no GitLab Docs page states the IAM formats (a 14-URL sweep found zero `gliamrt`/`gliamac` hits outside the upstream repo).
VERDICT COVERAGE-SWEEP: PASS — 27 of 30 upstream rules have a matching lane shape; the 3 without one are exactly the three the lane's known-limits list already declares (path-dependent `glft-`, bare `t1_`, `/trigger/pipeline?` URL form), and the upstream prose now states the path-dependent form in words, giving it a ground it lacked when the limit was written.
