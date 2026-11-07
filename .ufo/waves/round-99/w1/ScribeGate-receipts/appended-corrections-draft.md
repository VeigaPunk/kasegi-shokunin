# Draft — exact `## Appended corrections` block for `corpus/lessons/round-98.md`

Status: draft only. The lane was not edited. The committed block is at
`corpus/lessons/round-98.md:145-196` (HEAD `2c2124f`, introduced by `bedb6c4`).
This draft keeps the committed block's structure and corrects the three
defects found by the audit (word counts, the landing/integration conflation,
the S140 used-by enumeration) plus the redaction count. Differences are listed
after the block.

---

## Appended corrections (round 99 — closes the round-98 spot-check's routed defects 4 and 5)

**Routed defect 4 — the missing Gate records for S148/S149.** The round-98
`## Gate` block above records S140 and S144 and the S144-IAM reject, but not
the two rows the wave's ScoutSources added. Their records, from the rows in
`corpus/SOURCES.md` and the round-98 wave's receipt
`.ufo/waves/round-98/w1/ScoutSources-receipts/new-row-candidate-upstream-md.txt`
(which records `HTTP 200 for all 30 .md files`):

- **S148** — GitLab secret-detection rule prose, session cookie,
  `rules/mit/gitlab/gitlab_session_cookie.md` at commit 59ada1f4.
  URL:
  `https://gitlab.com/api/v4/projects/gitlab-org%2Fsecurity-products%2Fsecret-detection%2Fsecret-detection-rules/repository/files/rules%2Fmit%2Fgitlab%2Fgitlab_session_cookie.md/raw?ref=59ada1f4ca53d5a69fafb9cb0f10bb893720ce39`.
  Opened 2026-11-07 (HTTP 200, 1,028 bytes / 23 lines, sha256
  `b50856e4413c392ffe47fd0f212d5dd22067d52db710a7a8f93a11e9182ac319`). Quote,
  line 6 (13 words):
  ``The value is a 64-character hexadecimal session ID, with an optional `cell-<ID>-` prefix.``
  Admitted: kind `docs`, tier A, status `mined`.
- **S149** — GitLab secret-detection rule prose, IAM refresh token and
  authorization code, `rules/mit/gitlab/gitlab_iam_refresh_token.md` and
  `rules/mit/gitlab/gitlab_iam_authorization_code.md` at commit 59ada1f4.
  URLs: the same repository-files API path with `gitlab_iam_refresh_token.md`
  (HTTP 200, 1,190 bytes / 26 lines, sha256
  `9b37df1ebb06fd96a1ebefd0e8ba2dc0ae9d7f4e44ebce91c7bd4bec87aba456`) and
  `gitlab_iam_authorization_code.md` (HTTP 200, 1,322 bytes / 27 lines, sha256
  `52348dd60e586a08b6dc9188e573cc86a204da05636e2550c2028a4901bfc1c7`), both
  `?ref=59ada1f4ca53d5a69fafb9cb0f10bb893720ce39`.
  Opened 2026-11-07. Quotes, line 5 of each (13 words each):
  ``A GitLab IAM OAuth refresh token was identified. The token starts with `gliamrt-`.``
  and
  ``A GitLab IAM OAuth authorization code was identified. The code starts with `gliamac-`.``
  Admitted: kind `docs`, tier B, status `mined`.

**Routed defect 5 — the correction sweep.** Three sentences in this lesson and
in `SCORECARD.md`'s round-98 section contradict the landed state; the landed
state is authoritative and the sentences are corrected here rather than
rewritten in place (R9):

- the `## Gate` line "Registry 147 → 147 rows" and the SCORECARD round-98
  bullet "Sources: registry 147 → 147 (no new row)" are wrong at the round's
  close: the base `2133f5bd` and both landing commits (`e2caf4a1`,
  `e2d3de7b`) carry 147 rows, and the round-98 integration commit `2790774`
  added S148 and S149, so the round closed at **149** (`git show
  2790774:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3} \|'` prints 149;
  the round-99 base `6195db3` also prints 149);
- the SCORECARD round-98 C2 row ("the five shapes widened to S140's
  punct/space/EOL class") and the `## Learning` sentence ("restores S140's own
  right boundary on five shapes") are wrong as equalities: the C2 erratum in
  `.ufo/waves/round-98/claims.json` states `(?![A-Za-z0-9])` is a **strict
  superset** of S140's `(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)` — it also
  accepts every non-ASCII byte and every non-whitespace C0 control plus DEL
  (156 of 256 right-boundary bytes); the regex is unchanged and the erratum
  stands;
- the `## Gate` S140 used-by old→new records two added paths; the landed cell
  (`2790774` and the tip) adds **four**:
  `corpus/knowledge/github-refresh-tokens-and-gitlab-jwt-tokens.md` (the
  round-95 entry), `corpus/knowledge/gitlab-remaining-token-families.md` (the
  round-97 entry), `corpus/knowledge/gitlab-routable-and-versioned-token-forms.md`
  (the round-96 entry) and
  `corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md` (the
  round-98 entry); `corpus/instruments/capture-secret-scan.py` was already
  there.

The round-98 wave-evidence receipts
`.ufo/waves/round-98/w1/SentinelShapes-receipts/{body-sweep,final-checks,matrix-run,matrix.tsv}`
were redacted in round 99 (57 synthetic session values, one
`[session-cookie-fixture-redacted-r99]` marker per matched value across 57
lines in the four files; the addendum `a3db47e7` adds 57 markers and the line
counts are unchanged). The before/after digests in
`.ufo/waves/round-99/controls/redaction-r99.txt` cover the first matched line
of each file (4 of the 57 lines); the other 53 lines carry the marker without
a per-line digest. No claim number changes.

---

## Differences from the committed block (HEAD `2c2124f`)

1. **S148 word count.** Committed: `Quote, line 6 (17 words)`. Measured:
   `python3` `len(quote.split())` = **13**; the round-98 ScoutSources receipt
   also says `(13 words)`
   (`.ufo/waves/round-98/w1/ScoutSources-receipts/new-row-candidate-upstream-md.txt:17`).
   Corrected to 13.
2. **S149 word counts.** Committed: `(13 and 14 words)`. Measured: **13 and
   13** for the two quoted sentences. The receipt's 17 and 16 count the longer
   fragments that continue `The GitLab IAM service` / `The GitLab IAM`
   (`new-row-candidate-upstream-md.txt:14-15`), not the block's quotes.
   Corrected to 13 and 13.
3. **Quote fidelity.** The committed quotes escape the source's backticks as
   `\`` inside a single-backtick code span; CommonMark does not process
   backslash escapes inside code spans, so the rendered quote carries literal
   backslashes and is not verbatim. The draft uses double-backtick spans.
4. **147 → 149.** Committed: `the round landed **147 → 149**`. Measured: the
   base and both landing commits carry **147**; the integration commit
   `2790774` carries **149**. The draft states the landing/integration split.
5. **S140 used-by enumeration.** Committed: `the three added are
   ...remaining-token-families.md, ...iam-ci-build-and-session-token-shapes.md
   and, from the round-97 entry that had lost its citation, the round-97 entry
   itself` — three names for two distinct paths (the round-97 entry *is*
   `gitlab-remaining-token-families.md`), omitting
   `github-refresh-tokens-and-gitlab-jwt-tokens.md` and
   `gitlab-routable-and-versioned-token-forms.md`. The draft names all four.
6. **Redaction count.** Committed: `53 synthetic session values, one ...
   marker each`. Measured: **57** markers at HEAD (8+12+18+19); the addendum
   diff adds 57 marker lines; the receipt records **4** lines, not 57.
   Corrected to 57 with the receipt-coverage caveat.
7. **Provenance wording.** The committed block says the records come "from the
   rows in `corpus/SOURCES.md` and the round-98 wave's receipts"; the draft
   names the receipt file so the HTTP-200 and word-count claims are locatable.
