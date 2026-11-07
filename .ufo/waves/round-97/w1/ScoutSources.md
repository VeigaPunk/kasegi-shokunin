# ScoutSources — round 97 wave 1 — source reconnaissance

Seat: `ScoutSources` (leaf, read-only; the L1 writes the rows).
Lane: kasegi, round 97 attempt 1. Base `b06af5e07efbd961a8449f7de6b57eeea62c6bd3`,
freeze `daf7fc6a627d615178c27594110e956e592e4cd9`, C1 landing `75a471809cba265c8981ece1c0ed29c7895d9308`,
C2 landing `a9a53608dce6aea07d298bb9d5133532078eb1dd`.
Host paths were read only. Scratch `S=/fast/scratch/hyaku/kasegi-r97/ScoutSources` was created and removed on exit;
no file outside this report and `.ufo/waves/round-97/w1/ScoutSources-receipts/` was written. No git/jj mutation was
performed anywhere: the only git commands run were read-only (`rev-parse`, `log`, `show`, `status`).

## Verdict

**C2 STANDS** on the ten GitLab families: I re-derived all ten rules from the live upstream source and every one of
them is present at commit `59ada1f4` with the exact regex the claim quotes.

**One routed defect (does not re-score C2): the committed capture's line numbers are not the upstream file's line
numbers.** The round-94 manifest note asserts *"The array delimiters, rule ids, keywords, regex lines and every
other byte are unchanged, so line numbering is preserved"*, and the `S140` registry row repeats "line numbering
preserved". Both are inaccurate against the live file: the capture dropped the file's 30 blank lines and stripped
the 2-space indent of the 82 example-element lines, so every cited anchor is offset from the upstream file by a
growing amount. The **content** of every cited line is byte-identical between the two, and the capture is
reproducible byte-for-byte from the live file, so no shape or predicate is affected — but an auditor who opens the
live URL and goes to "line 101" finds `GR1348941` at line 105, and "line 412" finds `glffct-` while `glrct-` is at
live line 433. This is a provenance/anchor-integrity qualifier on `depth:verifiability`, not a verdict change.

**C1 STANDS**: all nine bare lane-instrument basenames named by tranche 12 resolve to tracked
`corpus/instruments/` paths that exist at the landing (receipt 08).

**Job 2 — tier verdict:** the scope "GitLab token prefix and length" is **tier A** for `S140` (the vendor's own
machine-readable rules publish prefix, alphabet *and* length) and **tier B** for every GitLab prose page I opened
(they publish prefixes, never lengths). No new prose source can raise that: a corpus-wide sweep of 21 distinct
GitLab docs URLs found exactly **one** page stating a prefix together with a length, and it is the already-registered
`S139`.

**Job 3 — one candidate rejected**: `https://docs.gitlab.com/user/project/settings/project_access_tokens/`
(HTTP 200, 52,715 bytes) — 0 hits across 20 prefix tokens and 0 token-length statements in the raw HTML (receipt 06).

---

## Job 1 — re-open S140's live source and confirm the ten rules

**Source.** GitLab secret-detection rules, `rules/mit/gitlab/gitlab.toml` at commit
`59ada1f4ca53d5a69fafb9cb0f10bb893720ce39`.
Capture URL (the one pinned in `corpus/source-snapshots/round-94/manifest.json`):
`https://gitlab.com/api/v4/projects/gitlab-org%2Fsecurity-products%2Fsecret-detection%2Fsecret-detection-rules/repository/files/rules%2Fmit%2Fgitlab%2Fgitlab.toml/raw?ref=59ada1f4ca53d5a69fafb9cb0f10bb893720ce39`.

**Re-fetch (2026-11-07): HTTP 200, 20,228 bytes, sha256
`14854f71f81f2400ac33a950cd70850cbdc80c319e4bdb0445bff6dbc36a11b5`** — identical to the manifest's pinned "raw"
digest. The upstream file is unchanged at that commit (receipt 01).

### The ten rules — quoted from the committed capture `corpus/source-snapshots/round-94/S140.txt`

| capture line | rule id (upstream) | regex line as committed (example values redacted upstream; none appear on these lines) |
|---|---|---|
| 101 | `gitlab_runner_registration_token` | `regex = "\\b(GR1348941[0-9a-zA-Z_\-]{20})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)"` |
| 160 | `gitlab_feed_token` | `regex = "\\b(feed_token=[0-9a-zA-Z_\-]{20})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)"` |
| 174 | `gitlab_oauth_app_secret` | `regex = "\\b(gloas-[0-9a-zA-Z_\-]{64})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)"` |
| 190 | `gitlab_feed_token_v2` | `regex = "\\b(glft-[0-9a-zA-Z_\-]{20})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)"` |
| 213 | `gitlab_kubernetes_agent_token` | `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glagent-[0-9a-zA-Z_\-]{50})(?:[^0-9a-zA-Z_\-.]|\.[0-9a-z]|\.$|$)'''` |
| 229 | `gitlab_incoming_email_token` | `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glimt-[0-9a-z]{20,25})(?:[^0-9a-zA-Z_\-]|$)'''` |
| 278 | `gitlab_scim_oauth_token` | `regex = "\\b(glsoat-[0-9a-zA-Z_\-]{20})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)"` |
| 341 | `gitlab_deploy_token_in_url` | `regex = '''gitlab\+deploy-token-[0-9]+:([0-9a-zA-Z_\-]{20})@'''` |
| 392 | `gitlab_feature_flags_client_token` | `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glffct-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''` |
| 412 | `gitlab_runner_controller_token` | `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glrct-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''` |

All ten are present in the live upstream file with **byte-identical** regex text, at these upstream line numbers:
105, 167, 182, 199, 223, 240, 291, 358, 412, 433 (receipt 03). Every element of the claim's surface list is
confirmed: the runner registration token, the `feed_token=` query form, `gloas-`+64, `glft-`+20, the plain
`glagent-` 50-character form (the round-96 spot-check's routed defect 1), `glimt-`+20-25 lower-case with the
optional instance prefix, `glsoat-`+20, the `gitlab+deploy-token-<N>:<token>@` URL form, `glffct-`+20 and
`glrct-`+20. The `glimt-` alphabet really is lower-case-only (`[0-9a-z]{20,25}`), and `glagent-` really is the
50-character form (`{50}`) as the claim states.

The three forms the round-97 known-limits list keeps are all confirmed present upstream and at the capture's
cited lines: the path-dependent `glft-` 64-hex form (capture 512/514, live 539/541), the `t1_` legacy partition
token (capture 308, live 323) and the `/trigger/pipeline` URL form (capture 532, live 560). The `t1_`/`t2_`/`t3_`
partition keywords are at live line 322.

### Routed defect: the capture's line numbers are not the upstream file's line numbers

The manifest note says the committed snapshot "replaces the 82 example/negativeExamples array element lines with one
fixed marker, **line numbering preserved**", and the `S140` registry row repeats "line numbering preserved with the
82 `examples`/`negativeExamples` array element lines replaced by one fixed marker". Both are **false with respect to
the upstream file**. The capture dropped the 30 blank lines and stripped the 2-space indent of the 82 example-element
lines; I reproduced the committed bytes exactly from the live bytes with that recipe:

```
live raw (20228 B, sha256 14854f71f81f2400ac33a950cd70850cbdc80c319e4bdb0445bff6dbc36a11b5)
  -> drop blank lines, strip 2-space indent of the 82 example-element lines
STEP1 collapsed  (20035 B, sha256 04fc5cfa200c92f54e14a7d104bb56e479aeccf45746234f0965c3c8e637d921)  == manifest pin
  -> replace each of the 82 example-element lines with the one fixed marker
STEP2 final     (25537 B, sha256 f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c)  == committed capture
```

Both intermediate digests match the manifest's own pins exactly, and STEP2 is byte-identical to the committed
capture (receipt 04). So the capture is fully reproducible from the live file — the defect is only in the
"line numbering preserved" claim, which holds for STEP1→STEP2 but not for raw→STEP1.

Consequence for an auditor: the cited anchors resolve to the right **content** but not at the cited **position** in
the upstream file (capture → live: 101→105, 160→167, 174→182, 190→199, 213→223, 229→240, 278→291, 341→358,
392→412, 412→433). The hazard is sharpest at the top of the range: upstream line 101 is a **blank line**, and
upstream line 412 holds `glffct-` while `glrct-` sits at 433 — so "line 412" read off the live URL names the wrong
family. The same drift applies to the 16 older anchors the landing instrument cites (4, 30, 51, 73, 114, 136, 255,
308, 324, 358, 375, 429, 446, 463, 512, 532): every one resolves to the correct rule content in the capture and
none lands on a redaction marker (receipt 09), and each is offset from upstream by the same blank-line drift.

**Scope of the defect.** It does not touch C2's predicate: K1–K6 test the *instrument's* shapes, the selftest
count, the allowlist run and the SCORECARD row, none of which read a source line number. The shapes themselves are
correct. The fix belongs in the two prose cells that assert "line numbering preserved" (the round-94 manifest note
and the `S140` row's anchor cell), and the cheap correct wording is "line numbering preserved relative to the
redacted collapsed snapshot, which drops the file's blank lines; the upstream file's own line numbers run 4 to 21
lines higher". Per the round's rule that a finding which does not re-score a claim is a routed defect, this is
routed, not a verdict change.

## Job 2 — one candidate source stating GitLab token prefixes with their lengths

**Candidate opened: GitLab Docs, Security — Tokens ("GitLab token overview") —
`https://docs.gitlab.com/security/tokens/`**

- **URL**: `https://docs.gitlab.com/security/tokens/`
- **Access date**: 2026-11-07
- **HTTP status**: `200` (67,805 bytes; also re-fetched at 67,793 bytes on a second pass, same page)
- **Exact section heading**: `Token prefixes` (an `h2`; the page's `h1` is "GitLab token overview")
- **Located quote** (≤25 words, from that section): *"With the exception of Personal Access tokens, these prefixes cannot be configured, as they are designed to be standard identifications."* (20 words; verified present verbatim on the fetched page)
- **What it states**: a two-column table mapping token name → prefix — `glpat-` (personal, impersonation, project
  and group access tokens), `gloas-`, `gldt-`, `glrt-`/`glrtr-`, `glcbt-`, `glptt-`, `glft-`, `glimt-`, `glagent-`,
  `glwt-`, `glsoat-`, `glffct-`, `_gitlab_session=`. **It states no lengths and no alphabets** — an absence sweep for
  `\b20\b`, `\b64\b`, `\b50\b`, `\b25\b`, `\b40\b`, `\b27\b` and for `<digit>[- ]?(character|long|digit|alphanumeric)`
  returns **0 hits** each (receipt 10).
- **Round-97 family coverage of the prefix table**: of the ten families the round landed, the page names the prefix
  of six — `gloas-`, `glft-`, `glagent-`, `glimt-`, `glsoat-`, `glffct-` — and names none of the other four:
  `GR1348941` (0 hits), `feed_token` (0), `gitlab+deploy-token-` (0) and `glrct-` (0). So even the prefix half of the
  scope is not fully covered by prose, which is a second, independent reason `S140` is the ground for all ten
  (receipt 10).

**Tier verdict for the scope "GitLab token prefix and length": tier B.**
By the registry's own convention a tier-B source is one that cannot ground the shape it was opened for — the
`S145` and `S147` rows are tier B for exactly this reason ("states no token prefix, length or alphabet, so it cannot
ground the shape"). This page publishes the prefix half of the scope and is silent on the length half, so on the
joint scope it is tier B. It is already registered as `S144` (tier A, status mined, used-by
`corpus/instruments/capture-secret-scan.py`, `corpus/knowledge/gitlab-routable-and-versioned-token-forms.md`),
where its scope cell correctly narrows it to "the standard token prefix
set and which prefixes may be configured" and its teaches cell correctly says "the page states prefixes, never
lengths or tails" — so the registry is already right about this page; nothing needs to change for it.

**The length half has no prose source.** A corpus-wide sweep of 21 distinct GitLab URLs (30 fetch artifacts, some
pages fetched twice under different file names) for a prefix co-occurring within 250 characters of both a bare digit
and length prose found exactly **one** qualifying
page: `https://docs.gitlab.com/user/application_security/secret_detection/detected_secrets/`, already registered as
`S139` (tier A, mined, used-by the same instrument), whose "Rule-based detection" section says *"a GitLab personal
access token is identified by the pattern `glpat-` followed by a 20-character string"* — the one prefix/length pair
in prose, and only for `glpat-` (receipt 07). The other pages that carry prefixes state them without lengths:
`/api/admin/token/` (`glpat-` only), `/security/tokens/token_troubleshooting/` (`glpat-` only),
`/development/authentication/` (`glpat-`, `gldt-`, `glcbt-`, `gloas-` with storage modes, still no lengths).

**Conclusion for the scope**: `S140` remains the only source that grounds prefix **and** alphabet **and** length
together for the round-97 families, which is why the C2 shapes cite S140 rather than prose. That is tier A for the
scope and it is the reason no new registry row is needed for job 2. A second, unregistered candidate I opened for
comparison — `https://docs.gitlab.com/development/authentication/`, HTTP 200, 81,314 bytes, `h2` "Token prefixes",
quote *"Use token prefixes to identify token types during debugging and code review"* — states four prefixes with
their storage mode and **0** length statements; on the joint scope it is tier B too, and it is not in
`corpus/SOURCES.md`, so it is a live flip candidate if the round ever needs a prose prefix table that
`/security/tokens/` does not cover.

## Job 3 — one candidate expected to be REJECTED

**Candidate: GitLab Docs, Project access tokens —
`https://docs.gitlab.com/user/project/settings/project_access_tokens/`**

- **URL**: `https://docs.gitlab.com/user/project/settings/project_access_tokens/`
- **Access date**: 2026-11-07
- **HTTP status**: `200`, 52,715 bytes, sha256 `c1a1a18469085b5cda637164f23bddd14288c040f5b13d890c0afc2c63859dd5`
- **Headings**: `h1` "Project access tokens"; `h2` Create a project access token / View your access tokens /
  Rotate a project access token / Revoke a project access token / Access token expiration / Bot users for projects /
  Restrict the creation of project access tokens / Related topics
- **Not in the registry**: 0 matches for `project_access_tokens` in `corpus/SOURCES.md`.

**Rejection, grounded by the absence sweep** (receipt 06):

- **20 token-prefix strings in the raw HTML: 0 hits total.** `glpat`, `glptt`, `glrt`, `glrtr`, `gldt`, `glagent`,
  `glimt`, `glsoat`, `gloas`, `glft`, `glffct`, `glrct`, `glwt`, `glcbt`, `glsat`, `gliamat`, `gliamrt`, `GR1348941`,
  `feed_token`, `deploy-token` — every one 0.
- **Token-length prose: 0 hits.** `\b20\b`, `\b64\b`, `\b50\b`, `\b25\b`, `\b40\b`, `\b27\b` and the combined
  `<digit>[- ]?(character|characters|char|long|digits|alphanumeric)` pattern all return 0.
- The only length-ish sentence on the page concerns the **token name**, not the token value, and it never names a
  prefix.

**Reason**: the page documents the lifecycle of project access tokens (create, view, rotate, revoke, expiry, bot
users) and states nothing about the token's byte form — no prefix, no length, no alphabet. It therefore cannot
ground any of the round's GitLab shapes, and `S140` remains the only ground for the `glpat-` family.

**Flip**: the page adds a token-format section naming `glpat-` or its length, or a table of token formats.

This rejection mirrors the two existing tier-B GitLab rows (`S145`, `S147`), which were opened on the same ground.

## Cross-check of the landing instrument against the live source (supporting, not a verdict)

The landing instrument `corpus/instruments/capture-secret-scan.py` cites S140 lines 4, 30, 51, 73, 101, 114, 136,
160, 174, 190, 213, 229, 255, 278, 308, 324, 341, 358, 375, 392, 412, 429, 446, 463, 512, 532 — all 26 resolve to
rule content in the committed capture and none to a redaction marker (receipt 09). The landing's known-limits list
keeps exactly the three forms the claim names (path-dependent `glft-`, `t1_` legacy partition, `/trigger/pipeline`
URL), and each is confirmed present upstream.

## Remaining unknowns

- I did not execute the C1 knowledge-meter or the C2 capability-check; the predicates are the executor seats'.
- The `S140` row's `anchor` cell and the round-94 manifest note both assert "line numbering preserved". Correcting
  them is an L1 edit; I did not touch them (my seat is read-only except for this report and its receipts).
- Whether GitLab's prose pages have ever stated a token length for a family other than `glpat-` was not
  exhaustively searched outside `docs.gitlab.com`; I limited the sweep to the vendor's own docs, which is the tier-A
  boundary the scope requires.

## Receipts

All under `.ufo/waves/round-97/w1/ScoutSources-receipts/`.

1. `01-s140-live-fetch.txt` — live re-fetch of the pinned S140 capture URL: `http_status=200 bytes=20228`,
   `sha256sum` = `14854f71f81f2400ac33a950cd70850cbdc80c319e4bdb0445bff6dbc36a11b5`, `wc -c -l` = 592 lines /
   20,228 bytes.
2. `02-s140-capture-anchors.txt` — the ten claimed anchors read out of the committed capture with
   `sed -n "<L>p"`: lines 101, 160, 174, 190, 213, 229, 278, 341, 392, 412 (regex text only; no example values).
3. `03-s140-live-anchors.txt` — the same ten regexes located in the live upstream file by
   `grep -nE 'regex = ' | grep -E 'GR1348941|feed_token=|gloas-|glft-|glagent-|glimt-|glsoat-|deploy-token-|glffct-|glrct-'`:
   live lines 105, 167, 182, 199, 223, 240, 291, 358, 412, 433, plus the path-dependent `glft-` rule at 541.
4. `04-s140-derivation.txt` — the byte-exact derivation: raw → collapsed (`sha256 04fc5cfa…`, matching the manifest
   pin) → marker-substituted (`sha256 f3fd09e4…`, **byte-identical to the committed capture**), plus the
   capture→live line-offset table and the marker string (157 chars, 82 occurrences, all identical).
5. `05-job2-candidate-authentication.txt` — job-2 candidate `https://docs.gitlab.com/development/authentication/`:
   `http=200 bytes=81314`, `sha256 0382533f…`, the `h2` "Token prefixes" heading, the located quote, and the
   length-prose absence sweep (0 hits for `\b20\b`, `\b64\b`, `\b50\b`, `\b25\b` and the character/long/digit/
   alphanumeric pattern).
6. `06-job3-reject-candidate.txt` — job-3 candidate
   `https://docs.gitlab.com/user/project/settings/project_access_tokens/`: `http=200 bytes=52715`, `sha256
   c1a1a184…`, all headings, and the grounding absence sweep (20/20 prefix strings at 0 hits; 7/7 length patterns at
   0 hits).
7. `07-corpus-wide-prefix-length-sweep.txt` — the 21-URL / 30-artifact sweep: only
   `detected_secrets` (already `S139`) co-occurs a prefix with length prose; every other page fails, including
   `/security/tokens/` (13 prefix strings, 0 length statements) and `/api/admin/token/`,
   `/security/tokens/token_troubleshooting/`, `/development/authentication/`.
8. `08-c1-instrument-paths.txt` — the nine tranche-12 bare basenames checked against `corpus/instruments/` at the
   landing: 9/9 `PRESENT`.
9. `09-cited-lines-resolve.txt` — all 26 S140 line numbers cited by the landing instrument resolve to rule content
   in the committed capture, none to a redaction marker, with the upstream line each maps to.
10. `10-job2-primary-token-overview.txt` — the primary job-2 candidate
    `https://docs.gitlab.com/security/tokens/`: `http=200 bytes=67805`, `sha256`, all `h1`/`h2`/`h3` headings, the
    exact section heading `Token prefixes`, the 20-word located quote (verified verbatim), the seven-pattern
    length absence sweep (0 hits each), the 13 prefix tokens the page does state, and the four round-97 families
    whose prefix the page does **not** state (`GR1348941`, `feed_token`, `gitlab+deploy-token-`, `glrct-` — 0 hits
    each).

### Commands run (observed results)

```
$ curl -sSL -o raw-gitlab.toml -w 'http_status=%{http_code} bytes=%{size_download}' '<pinned capture_url>'
http_status=200 bytes=20228
$ sha256sum raw-gitlab.toml
14854f71f81f2400ac33a950cd70850cbdc80c319e4bdb0445bff6dbc36a11b5  raw-gitlab.toml
$ for L in 101 160 174 190 213 229 278 341 392 412; do sed -n "${L}p" corpus/source-snapshots/round-94/S140.txt; done
(ten regex lines; see receipt 02)
$ grep -nE 'regex = ' raw-gitlab.toml | grep -E 'GR1348941|feed_token=|gloas-|glft-|glagent-|glimt-|glsoat-|deploy-token-|glffct-|glrct-'
105, 167, 182, 199, 223, 240, 291, 358, 412, 433, 541   (see receipt 03)
$ git show <rev>:corpus/source-snapshots/round-94/S140.txt | sha256sum     # base, freeze, C1 landing, C2 landing
f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c   (identical at all four revisions)
$ curl -sSL -o j2-60ea8275.html -w 'http=%{http_code} bytes=%{size_download}' https://docs.gitlab.com/development/authentication/
http=200 bytes=81314
$ curl -sSL -o cand-091f4350.html -w 'http=%{http_code} bytes=%{size_download}' https://docs.gitlab.com/security/tokens/
http=200 bytes=67805
$ curl -sSL -o cand-13b53333.html -w 'http=%{http_code} bytes=%{size_download}' https://docs.gitlab.com/user/project/settings/project_access_tokens/
http=200 bytes=52715
$ for N in resolve.py anchorcheck.py capture-source.py source-recheck.py density.py capture-secret-scan.py \
          claim-package-check.py r35-defect-closure.sh r36-closure.sh; do test -f corpus/instruments/$N; done
9/9 PRESENT   (receipt 08)
```

No credential values are reproduced in this report or in the receipts: the S140 example arrays are upstream
redaction markers in the committed capture, and the live file was only read for regex/keyword/id lines, never for its
published example values.
