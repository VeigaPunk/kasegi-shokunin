## Gate

Candidates considered this round:

1. **S152 — curl, HTTP cookies, the cookie jar file format** — opened this
   round, accessed 2026-11-07 (live fetch HTTP 200, 13,717 bytes, sha256
   `c202d81f7b37d049e3aaa7b9e3ef781cb0658bbc5cf89716f2b213278442c59a`).
   URL: `https://curl.se/docs/http-cookies.html` (`#cookie-file-format`).
   Quote (16 words, located in the "Cookie file format" section):
   - `Each line that specifies a single cookie consists of seven text fields separated with TAB characters.`
   Admitted: kind `docs`, tier B, status `mined`, used-by
   `corpus/instruments/capture-secret-scan.py, corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`.
   Why it clears the bar: it states the on-disk format a capture artifact
   carries, which is the fact the round-99 harm turned on — the jar separates
   the session name from its value with a TAB and no operator, so a matcher
   built on an operator window alone cannot see it. Tier B, not A: the page
   documents a client's file format, not a security rule.

2. **S153 — IETF RFC 6265, HTTP State Management Mechanism** — opened this
   round, accessed 2026-11-07 (live fetch HTTP 200, 79,724 bytes, sha256
   `dc4177094813e85a44a7897b892b76bc09160b3a03aea44f0f511f3a98f91933`).
   URL: `https://www.rfc-editor.org/rfc/rfc6265.txt`. Quote (17 words, §1
   Introduction, lines 195-196):
   - `Prior to this document, there were at least three descriptions of cookies: the so-called "Netscape cookie specification"`
   **REJECTED** for this round's purpose: the RFC defines the `Cookie` and
   `Set-Cookie` semantics and the cookie store model, and it names the
   Netscape specification as a prior description, but it states no on-disk
   file format — so it cannot ground the jar class S152 grounds. Flip: admit
   if a round needs cookie *semantics* (prefixes, SameSite, the store model)
   rather than the file format; the row stays `rejected` with this reason.

3. **S140 — GitLab secret-detection rules, `rules/mit/gitlab/gitlab.toml` at
   commit 59ada1f4** — re-opened from its committed capture for the
   session-cookie rule (lines 547-551; capture
   `corpus/source-snapshots/round-94/S140.txt`, sha256
   `f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`). The
   live `/-/raw/` fetch answered HTTP 403 again (a Cloudflare challenge page,
   6,078 bytes; receipt `.ufo/waves/round-98/l1/source-reopen-r98.txt`), so
   the capture is the citation base. Quote (`S140:550`):
   - `assignmentContext.keywordGroup = '''_gitlab_session(?:_geo_[0-9a-f]{64})?'''`
   Status `mined`, recheck `180d`, used-by unchanged.

4. **S148 — GitLab secret-detection rule prose, session cookie** — re-opened
   by live fetch at the pinned digest (HTTP 200, 1,028 bytes / 23 lines,
   sha256 `b50856e4413c392ffe47fd0f212d5dd22067d52db710a7a8f93a11e9182ac319`;
   the row's anchor is the repository-files URL at `corpus/SOURCES.md:160`,
   not a committed capture). Quote (`S148:6`):
   - ``The value is a 64-character hexadecimal session ID, with an optional `cell-<ID>-` prefix.``
   Status `mined`, recheck `180d`, used-by unchanged.

5. **S151 — GitLab secret-detection-rules, the assignment-context generator
   `pkg/rules/assignment_regex.go` at commit 59ada1f4** — re-opened for the
   terminal class and the delimiter set (live fetch HTTP 200, 9,776 bytes,
   sha256 `91519731800ab8d96a00a03fff44e72c1c16a3bad12c9e017d7d679a8fad756d`,
   byte-identical to the round-99 fetches). URL:
   `https://gitlab.com/api/v4/projects/gitlab-org%2Fsecurity-products%2Fsecret-detection%2Fsecret-detection-rules/repository/files/pkg%2Frules%2Fassignment_regex.go/raw?ref=59ada1f4ca53d5a69fafb9cb0f10bb893720ce39`.
   Quotes (`S151:28-29`, each under 25 words):
   - line 28 — ``assignmentOperand = `[="' :>\],\t.()\\?|]{1,10}` ``
   - line 29 — ``terminalRegex     = `(?:\\['"rn]|['"\x60; \s]|</|$)` ``
   Status `mined`, recheck `180d`, used-by unchanged.

6. **S150 — the rules repo's MR !151** — not re-opened this round; S151
   supersedes its form at the pinned commit and its HTML digest is
   nonce-bound (the round-99 finding). No cell change.

Status / used-by changes this round, old → new:

- S152: new row, status `mined`, used-by
  `corpus/instruments/capture-secret-scan.py, corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`.
- S153: new row, status `rejected`, used-by `—`.
- S140, S148, S151: no cell change (re-opened; S140 live 403, S148/S151 live
  200 at their pinned digests).

Registry 151 → 153 rows (S152 and S153):
`grep -cE '^ {0,3}\| S[0-9]{3} \|' corpus/SOURCES.md` prints 151 at the base
`6e63a7dc` and 153 in the working tree (152 at the C1 landing `1605775b`,
before S153). Census at round end:

```text
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi  W04  S028 duplicate url … (seven inherited W04 warnings)
kasegi  ok   /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
rc=0
```

