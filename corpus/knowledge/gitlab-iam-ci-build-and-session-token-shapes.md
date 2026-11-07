# GitLab's IAM, CI-build and session-cookie token shapes — four rules S140 publishes

source: S140 — GitLab secret-detection rules, `rules/mit/gitlab/gitlab.toml` at commit 59ada1f4, lines 291-294, 478-481, 495-498 and 547-551 (capture `corpus/source-snapshots/round-94/S140.txt`, sha256 `f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`, 563 lines, example values structurally redacted, line numbering preserved); S144 — GitLab Docs, Security — Tokens, https://docs.gitlab.com/security/tokens/ (capture `corpus/source-snapshots/round-96/S144.txt:356` and `:362`, the prefix table's `glcbt-` and `_gitlab_session=` rows); S150 — GitLab secret-detection-rules merge request !151, the assignment-context generator, https://gitlab.com/gitlab-org/security-products/secret-detection/secret-detection-rules/-/merge_requests/151 (the MR description's "Generated Regex" block, HTTP 200, 128,120 bytes, sha256 `aa60d7af465cad03b64259362dfa862a8d5c3176ebc2e6b5909a38daddea11e8`); S148 — GitLab secret-detection rule prose, `rules/mit/gitlab/gitlab_session_cookie.md` at commit 59ada1f4 (https://gitlab.com/api/v4/projects/gitlab-org%2Fsecurity-products%2Fsecret-detection%2Fsecret-detection-rules/repository/files/rules%2Fmit%2Fgitlab%2Fgitlab_session_cookie.md/raw?ref=59ada1f4ca53d5a69fafb9cb0f10bb893720ce39, 1,028 bytes / 23 lines / sha256 `b50856e4…`, line 6); S149 — the same repository's per-rule prose for the two IAM forms, `gitlab_iam_refresh_token.md` (1,190 bytes / 26 lines / sha256 `9b37df1e…`, line 5) and `gitlab_iam_authorization_code.md` (1,322 bytes / 27 lines / sha256 `52348dd6…`, line 5)
verified-at: 2026-11-07 (both captures re-read at their pinned digests; the S140 live `/-/raw/` fetch answered HTTP 403 again this round — a Cloudflare challenge page, 6,078 bytes, 2026-11-07T20:54:03Z, receipt `.ufo/waves/round-98/l1/source-reopen-r98.txt` — so the committed capture is the citation base; S148/S149 were fetched live via the repository-files API, HTTP 200, at their recorded digests)
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sed -n '291,294p;478,481p;495,498p;547,551p' corpus/source-snapshots/round-94/S140.txt | grep -c 'regex' && sed -n '356p;362p' corpus/source-snapshots/round-96/S144.txt | grep -cE 'glcbt-|_gitlab_session=' && python3 -B corpus/instruments/capture-secret-scan.py --selftest >/dev/null && echo RECHECK-OK

## What this holds

Four more families the same rules file publishes, and one rule about the
boundary that decides whether a real token is seen at all:

- the CI build token is `glcbt-` + 1-5 alphanumerics + `_` + exactly 20
  characters — a different grammar from the JWT form (`glcbt-eyJ…`) the lane
  already holds, because the underscore separator is mandatory;
- the IAM refresh token and the IAM authorization code are two 43-character
  segments joined by a dot (`gliamrt-…`, `gliamac-…`);
- the session cookie is not a prefixed token at all: the value is 64 lower-case
  hex characters, optionally behind a `cell-<N>-` prefix, and the rule only
  fires where the assignment context names `_gitlab_session` (optionally with
  a `_geo_<64 hex>` suffix). A bare 64-hex string is not the shape.
- the assignment context is a *window*, not a separator list: the generator
  expands `assignmentContext` to `<keyword>.{0,8}[:=].{0,8}<value>` (S150), so
  `_gitlab_session => H`, `_gitlab_session%20=%20H`, `_gitlab_session,=H` and
  `_gitlab_session=cell--H` are all the shape. A matcher built on a
  whitespace/quote/operator class refuses eight of the twelve real session
  values the round-98 sentinel measured (round 99).

The rules file also settles the right boundary the round-97 shapes got wrong:
`(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)` admits `_` and `-` after the tail,
because both are ASCII punctuation. A matcher that refuses them misses a real
token followed by either character.

| shape | grammar | S140 line | second source |
|---|---|---|---|
| `gitlab-ci-build-token` | `glcbt-` + 1-5 `A-Za-z0-9` + `_` + 20 `A-Za-z0-9_-` | 293 | S144:356 (`glcbt-`) |
| `gitlab-iam-refresh-token` | `gliamrt-` + 43 `A-Za-z0-9_-` + `.` + 43 | 480 | S149:5 (`gliamrt-`) |
| `gitlab-iam-authorization-code` | `gliamac-` + 43 `A-Za-z0-9_-` + `.` + 43 | 497 | S149:5 (`gliamac-`) |
| `gitlab-session-cookie` | `_gitlab_session` context, S140's assignment-context separator `<keyword>.{0,8}[:=].{0,8}`, optional `cell-<N>-`, 64 lower-case hex | 549-551 | S144:362 (`_gitlab_session=`), S148:6 (the value's length and alphabet), S150 (the separator window) |

## The four published rules, verbatim

Each quote is one line (or two for the session cookie) of
`rules/mit/gitlab/gitlab.toml` at commit 59ada1f4, reproduced exactly as the
capture holds it. Every quote is under 25 whitespace-separated words.

- S140:293 — `regex = "\\b(glcbt-[0-9a-zA-Z]{1,5}_[0-9a-zA-Z_\\-]{20})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)"`
- S140:480 — `regex = '''\b(gliamrt-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:[^0-9a-zA-Z_\-]|$)'''`
- S140:497 — `regex = '''\b(gliamac-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:[^0-9a-zA-Z_\-]|$)'''`
- S140:549 — `regex = '''(?:cell-[0-9]+-)?[0-9a-f]{64}'''`
- S140:550 — `assignmentContext.keywordGroup = '''_gitlab_session(?:_geo_[0-9a-f]{64})?'''`

S148:6 — `The value is a 64-character hexadecimal session ID, with an optional \`cell-<ID>-\` prefix.`

S149:5 — `A GitLab IAM OAuth refresh token was identified. The token starts with \`gliamrt-\`.` and, in the sibling file, `A GitLab IAM OAuth authorization code was identified. The code starts with \`gliamac-\`.`

The two documentation rows S144 states are the prefix table's own cells:
`CI/CD Job tokenglcbt-` (line 356) and `GitLab session cookies_gitlab_session=`
(line 362). S144's table names no prefix, length or alphabet for the two IAM
forms, so S140 is their only source here.

## Falsifiable rule

A capture that contains `glcbt-` + 1-5 alphanumerics + `_` + 20 characters,
`gliamrt-`/`gliamac-` + 43 + `.` + 43, or a `_gitlab_session` assignment whose
value is 64 lower-case hex (optionally `cell-<N>-`-prefixed) with at most eight
non-newline bytes on either side of a `:` or `=` operator is a credential
capture and must be redacted before commit; a 64-hex string with no
`_gitlab_session` context is not. Check: `python3 -B
corpus/instruments/capture-secret-scan.py --selftest` covers twelve separator
positives and ten boundary negatives for the session cookie, and one positive
and one boundary negative per other shape.

## Limits

- The IAM forms' alphabet and lengths are stated by the rules file only; no
  GitLab documentation page opened this round states them.
- The session-cookie rule is context-bound (`assignmentContext.keywordGroupType
  = "raw"`, S150). The instrument now uses S140's window
  `[^\n]{0,8}[:=][^\n]{0,8}`; a value on the next line is out of scope (S150's
  window is same-line), and a gap wider than eight bytes before the operator is
  a miss by the generator's own rule. The instrument keeps a left boundary
  (`_GL_LB`) that S140's raw keyword group does not have, so a prefixed name
  (`x_gitlab_session=`) is a deliberate miss (the round-98 sentinel's Q1: S140
  over-detects there). The value-before-keyword form stays a miss.
- The IAM service is not generally available yet (S149:5-6, the vendor's own
  statement), so the IAM shapes are forward-looking ground.
- The `glcbt-` JWT form stays the `gitlab-jwt-token` shape; this entry's
  `gitlab-ci-build-token` is the underscore-separated form only.
