author: kasegi (round 100, attempt 1)

# Round 100 — lesson

Lane: kasegi. Round 100 (graduation round), attempt 1. Base
`6e63a7dc249ade9a3fc6d219b44049017bdb24a1`; freeze
`f04d63de2ab55e240472c31d551f6a2759a1d7fb`; C2 landing
`ff267d12e7c915986a62253bd40f9289ee6cec5d`; C1 landing
`1605775b0388b309ed05513f6862b669e80e3f30`.

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

## Learning

- **A separator model is a union, not a choice.** Round 99 replaced the
  round-98 whitespace/quote/operator class with S140's operator window and
  lost 23 classes; round 100 took the bounded union and recovered the three
  that a capture actually carries (the Netscape jar's TAB and space forms, the
  `_geo_` space form) while keeping every window form. The twenty classes the
  union still refuses are exactly the ones S140's own bound refuses — a
  newline between keyword and operator, and gaps of 9-12 bytes — so the
  residual is a *stated* bound, not an accident. The lesson for a shape
  landing: when two sources describe different separator models, the shape is
  the union of what each *accepts*, and the residual is the intersection of
  what each *refuses*.
- **A record that is checked against a regenerated copy is not checked against
  itself.** The round-99 census passed every digest and every regenerated-line
  comparison while its header (host-inclusive 2645/7624, 2683/8026) and its
  body (resolve.py 2646/7624, 2684/8026) named different definitions: the
  header was generated by the instrument, the body by `resolve.py`, and
  nothing compared them. The reconciliation identity is now explicit and
  machine-checked — body numerator = host-inclusive + confined, per scope;
  class table sums to the distinct total; INTERNAL - confined = pinned — and
  the `confined:` line states the difference a reader needs.
- **A tamper class killed by a format mismatch is not evidence for a limb.**
  The round-99 harness's T09 (poisoned cache) was "killed" by `no-confined`
  because its `header_lines()` knows only five fields; the round-100 harness
  carries all six, so T09 now fails `pinned-mismatch` — the cache really is
  not read.
- **A positive control must be the instrument's own fresh output.** The first
  reconcile limb rejected a correct record because the parse regex assumed
  `**165/732**` while the body writes `**165/732 = 22.54%**`; only the
  write-then-check control caught it. A new limb is trusted after a positive
  control passes, never before.

## Mistakes

- **M100-1** — the `resolvability_numbers()` regex omitted the `= NN.NN%`
  segment, so `reconcile-body` fired on a correct record. Evidence: the first
  `CENSUS-WRITE ok` + `CENSUS-CHECK fail reason=reconcile-body rc=1` pair in
  the round's working log; captured-by: the write-then-check positive control
  (a control set with only negative fixtures would have frozen a broken limb).
  Fix: the regex matches the body's real line; the positive control is part of
  the frozen control set.
- **M100-2** — `HEADER_FIELDS` used the new host-inclusive *label* for presence
  matching, so the round-99 record failed `no-host-inclusive` and the kill was
  attributable to the relabel, not to the reconciliation. Captured-by: none
  (the control output was read, not trusted). Fix: presence matches a stable
  prefix (`host-inclusive rate`) and the full line is compared separately; the
  base record now fails `no-confined`.
- **M100-3** — the tamper harness's `reseal()` dropped the `header-sha256`
  line when only the body changed, so T14/T15 failed `no-header-sha` instead
  of their limbs. Captured-by: the per-class `reason=` line (R150's
  attribution rule, now applied to the reason). Fix: a body-only reseal keeps
  the header digest; T14/T15 print `reconcile-body`/`reconcile-classes`.
- **M100-4** — the census description line hardcoded "regenerated in round
  99", which would go stale on every later regeneration. Captured-by: reading
  the regenerated record. Fix: the line carries no round number; the round is
  named in `LOG.md`.
- **M100-5** — the instrument docstring carried `[^\S\n]` in a non-raw string,
  raising a `SyntaxWarning` (the round-98 F2 class). Captured-by: the
  `SyntaxWarning` on the first `c2-check` run. Fix: the docstring escapes the
  backslashes; the selftest run is clean.
- **M100-6** — the round-99 T09 kill was a format artifact, not a cache test
  (see Learning). Captured-by: reading the reason string. Fix: the round-100
  harness's `header_lines()` carries all six fields; T09 fails
  `pinned-mismatch`.

## Wave findings

(to be filled after WAVE-DONE)

## Routed defects

- Round-99 spot-check defects closed this round: 1 (C2 harm — the bounded
  union lands), 2 (census header/body reconciliation — C1), 3 (53 → 57 and the
  mistake count, corrected in `SCORECARD.md`, `LOG.md` and `QUALITY.md` R160;
  the round-99 report's "nine" is superseded and not rewritten), 4 (the landed
  digests of the four redacted receipts recorded in
  `.ufo/waves/round-100/l1/r99-landed-digests.txt`), 7 (the round-99
  wave-evidence bullet appended to `LOG.md`), 8 (the round-98 bullet-pointer
  correction appended to `LOG.md`).
- Defects that cannot be closed without rewriting a closed record: 5 (the
  round-99 report's "round-98 hits=1" citation; the matrix is the real
  regression evidence), 6 (the round-99 probe's docstring provenance; the
  round-100 copy carries a corrected docstring, the round-99 original and its
  pin are unchanged), 9 (the round-99 report's 2.23 s / 512,980 kB against the
  receipt's 2.29 s / 512,064 kB). Recorded here, not rewritten.
- Defect 10 is operator-side (`templates/round-prompt.md` line 1 renders
  `<kasegi-repo>`); reported, not edited.

## Routed to round 101

1. **C1 limb coverage (high).** The 15-class harness is a format/digest harness:
   10 of 12 single-point *check* mutants survive it, T14/T15 do not isolate
   `reconcile-body`/`reconcile-classes` (the pre-existing `body-mismatch` also
   kills them), and four real defects (m08b/m10/m11/m12) are invisible to it.
   Build a limb-coverage harness that mutates the check's own limbs and
   requires each to be the unique catcher of at least one fixture.
2. **C1 extract provenance (high).** `--check` reuses an extract directory if
   `resolve.py` is present, so a poisoned extract makes it accept an
   unreconciled record (CriticClaimsC1 attack a). Re-extract per check or bind
   the extract by a tree hash of the revision.
3. **C2 pinned operand class (high).** The pinned `assignmentOperand`
   (S151) admits quote, semicolon, comma, parenthesis, backslash and pipe
   delimiters and a 10-byte bound; the union implements only whitespace and
   `:`/`=` with an 8-byte bound. Six realistic export forms pass unseen
   (quoted CSV, SQL, tuple, JSON pair array, unbackticked markdown table).
   Land the operand class (or a measured superset) with the frozen negatives
   re-derived, not re-used.
4. **C2 oracle (medium).** `matrix.py`'s S140 translation is the MR !151
   window, not the pinned `assignmentOperand`; 58/192 cells change verdict
   under the pinned form. A round-101 counter must name its oracle and carry
   both translations.
5. **C2 unpinned limbs (medium).** The whitespace run's upper bound (`{1,8}`)
   and its newline exclusion are unpinned by both the selftest and the matrix
   (MutC2Union m03/m04 survive). Add a boundary-negative pair: a 9-byte
   whitespace run and a newline inside the whitespace limb.
6. **C2 over-detection (low).** Four non-credential forms hit: a
   prefix-collision name `_gitlab_session_old=`, 64-72 hex runs, an empty
   session followed by another cookie's 64 hex, and a SHA-256 digest paired
   with the cookie name.
7. **C1 citation drift (low).** 35 `census-at-rev.py:NN` cites in knowledge
   files point 5-6 lines off their referent (already 43+ lines off at base);
   CriticHarm records the smallest safe correction.
