author: kasegi (round 98, attempt 1)

# Round 98 — lesson

Lane: kasegi. Round 98, attempt 1. Base `2133f5bd993aaf34efad795d5e0b588485401fb2`;
freeze `12bb2f98cf9d07bcbc8b62985516cc3ff65d9ae8`; C2 landing
`e2caf4a1561b544a6ea684b0bcfa975f7e7f6061`; C1 landing
`e2d3de7b847f8e9bac72a5bc4dea455ea051cf1a`.

## Gate

Candidates considered this round:

1. **S140 — GitLab secret-detection rules, `rules/mit/gitlab/gitlab.toml` at
   commit 59ada1f4** — re-opened from its committed capture for the four rules
   this round implements (lines 291-294, 478-481, 495-498, 547-551; capture
   `corpus/source-snapshots/round-94/S140.txt`, sha256
   `f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`, 563
   lines). URL:
   `https://gitlab.com/gitlab-org/security-products/secret-detection/secret-detection-rules/-/raw/59ada1f4ca53d5a69fafb9cb0f10bb893720ce39/rules/mit/gitlab/gitlab.toml`.
   Opened 2026-11-07; the live fetch answered HTTP 403 (a Cloudflare challenge
   page, 6,078 bytes, sha256 `6ab31380…`, receipt
   `.ufo/waves/round-98/l1/source-reopen-r98.txt`), the same result round 97
   recorded, so the committed capture is the citation base. Quotes (each under
   25 words, capture lines):
   - `S140:293` — `regex = "\\b(glcbt-[0-9a-zA-Z]{1,5}_[0-9a-zA-Z_\\-]{20})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)"`
   - `S140:480` — `regex = '''\b(gliamrt-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:[^0-9a-zA-Z_\-]|$)'''`
   - `S140:497` — `regex = '''\b(gliamac-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:[^0-9a-zA-Z_\-]|$)'''`
   - `S140:549` — `regex = '''(?:cell-[0-9]+-)?[0-9a-f]{64}'''`
   - `S140:550` — `assignmentContext.keywordGroup = '''_gitlab_session(?:_geo_[0-9a-f]{64})?'''`
2. **S144 — GitLab Docs, Security — Tokens** — re-opened from its committed
   capture for the two prefix-table rows that state two of the four shapes.
   URL: `https://docs.gitlab.com/security/tokens/`. Opened 2026-11-07; live
   fetch HTTP 200, 67,805 bytes, sha256 `765becf3…`; the live page carries
   `glcbt-` and `_gitlab_session=`. Quotes (capture
   `corpus/source-snapshots/round-96/S144.txt`):
   - `S144:356` — `CI/CD Job tokenglcbt-`
   - `S144:362` — `GitLab session cookies_gitlab_session=`
3. **S144 as a second source for the two IAM forms — REJECTED.** S144's
   prefix table (capture lines 344-362) names `glcbt-` and `_gitlab_session=`
   but no IAM prefix: `grep -c 'gliam' corpus/source-snapshots/round-96/S144.txt`
   prints 0; the live page was fetched (67,805 bytes, sha256 `765becf3…`, receipt `.ufo/waves/round-98/l1/source-reopen-r98.txt`) but is not committed, so the capture grep is the verified sweep. The two IAM
   forms are stated only by the rules file, so no new row is written for them:
   a row no admitted entry can cite is not appended (CORPUS rule 4). Flip: a
   docs page that names `gliamrt-`/`gliamac-` or their lengths.

Status / used-by changes this round, old → new:

- S140: status `mined` (unchanged), recheck `180d` (unchanged); used-by
  `corpus/instruments/capture-secret-scan.py` → `corpus/instruments/capture-secret-scan.py, corpus/knowledge/gitlab-remaining-token-families.md, corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`
  (the round-97 entry's citation was missing from the cell and is added here).
- S144: status `mined` (unchanged), recheck `180d` (unchanged); used-by
  `corpus/instruments/capture-secret-scan.py, corpus/knowledge/gitlab-routable-and-versioned-token-forms.md` → `corpus/instruments/capture-secret-scan.py, corpus/knowledge/gitlab-routable-and-versioned-token-forms.md, corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`.

Registry 147 → 147 rows:
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` prints 147 at the
base and 147 in the working tree. Census:
`cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
prints `kasegi ok` rc 0 with the seven inherited W04 duplicate-URL warnings
(S028, S029, S072, S076, S080, S085, S143).

Spot-check result: pending the round-98 non-author closure.

## Learning

- **expansion: improved** — the four further S140 rules land as a sourced
  knowledge entry (`corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`)
  on ground the coverage map does not hold (no credential-shape row), the
  `capture-secret-scan` capability row is extended, and two already-mined rows
  were re-opened and their `used-by` cells corrected (S140 had lost the
  round-97 entry's citation).
- **quality: improved** — the census of record is now a reading of a named
  revision with a pinned, revision-stable rate beside the host-inclusive one
  (before: `132/701` from an unnamed 224-file tree); the scanner gains four
  published shapes and restores S140's own right boundary on five shapes
  (selftest 148 → 170); the round-94 receipt's ci-build fixture literal is
  redacted structurally.
- **discernment: improved** — six mistakes mined (M98-1…M98-6), including the
  two the round's own checks caught before the freeze, the one the new shape
  exposed in an old receipt, and the `\-` SyntaxWarning the wave's reviewer
  found; the round-97 spot-check's routed defect 1 (the M4 wrong-instrument
  hole) is captured as R155. The wave's C1 finding (the pinned rate is not
  revision-stable) is recorded in the Wave findings section and routed.

## Mistakes

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M98-1 | landing | the first census generation embedded the scratch extract path in 1,243 places, e.g. `/fast/scratch/hyaku/kasegi-r98/l1/census-land/tree-e2caf4a1561b/./PROVINCE.md`; the count is recorded in the committed claim erratum (`.ufo/waves/round-98/claims.json` `erratum`), and the landed file prints `grep -c 'tree-e2caf4a1561b'` = 0 (`.ufo/waves/round-98/l1/p3-r98.txt`) | the P3 command (as corrected) — a census of a revision must not cite the scratch tree it was measured in | the instrument rewrites the extract path to the lane root before writing the body; the regenerated file prints `extract: 0`, `scratch: 0`, `tmp: 0` and `CENSUS-CHECK pass`; R156 records the rule |
| M98-2 | predicate-misspecification | P3's frozen command counted the corpus's own `/fast/scratch` citations (219 distinct, from earlier rounds' lessons) rather than a leak; the first run printed 1243 and could never print 0 | the first P3 run, before any seat scored | the erratum in `claims.json` names the mis-specified command and the correct one (`grep -c 'tree-e2caf4a1561b'` prints 0); the frozen P3 text is kept, the erratum appended |
| M98-3 | fixture-base | the C1 control harness cloned the lane tip and asserted it equalled `--base`; after the C2 landing advanced the tip the assertion fired (`base-mismatch`, harness code `.ufo/waves/round-98/controls/c1-controls-r98.py:104`; the fix is the freeze→landing diff that adds `git checkout -q <base>`) | the harness's own base assertion | the fixture clone checks out `--base` explicitly before the candidate commits; the 8 controls pass on the fixed harness (`.ufo/waves/round-98/controls/c1-controls-r98-postfix.txt`) |
| M98-4 | shape-exposes-old-receipts | the new `gitlab-ci-build-token` shape hit `.ufo/waves/round-94/w1/SentinelShapes-receipts/08-unlisted-classes.txt:75` (the base file held `glcbt-abc12_0123456789abcdefghij`, a round-94 synthetic fixture literal); the K2 hit is recorded in `.ufo/waves/round-98/l1/redaction-r98.txt` and the landed K2 prints `hits=0` | K2's clean-run limb, on the first candidate run | the value is redacted structurally (`glcbt-[ci-build-token-fixture-redacted-r98]`, line numbering preserved, before/after digests in `.ufo/waves/round-98/l1/redaction-r98.txt`); the sweep is by shape set, never by round (the M97-2 class recurring because the shape set grows) |
| M98-5 | landing | `claims.json` pinned the census instrument at `435128a2…` before the body-rewrite fix; the landing bytes are `66383371…` | the instrument sha check in the erratum pass | the erratum records old → new and the single change (the body rewrite); the post-fix control receipt is committed beside the freeze receipt |
| M98-6 | quality | the landed scanner's docstring carries `[^0-9a-zA-Z_\-]` in a non-raw string; a fresh compile prints `SyntaxWarning: "\-" is an invalid escape sequence` (the lane's own runs hide it behind `__pycache__`; the gate's scratch extract compiles fresh) | a fresh `python3 -B <extracted instrument> --selftest` (the wave's receipts) | routed to round 99: change the docstring to `[^0-9a-zA-Z_-]` and update the instrument pin in the same round; the landing bytes are not rewritten after data (the frozen pin `45f8d226…` stays the landing's) |

## Wave findings (round-98 w1, 13 seats)

All thirteen seats settled; none died (`.ufo/waves/round-98/w1-results.json`,
`seats=13`). **C2 stands on its frozen predicate; C1 does not** — the wave
falsified C1's central label, and the round reports that honestly.

**C1 — NOT VERIFIED on P1 and P2; P3 stands.** CriticClaimsC1: the exact frozen
command printed `CENSUS-CHECK fail reason=resolve-rc-15 rc=2` on three attempts
(earlyoom SIGTERM on the 2–3.5 GB `resolve.py` child, journal-attributed), and
— the substantive defect — the pinned rate is not revision-stable: the same
revision `e2caf4a1` measures 2589/7961 in a clean scratch and 2591/7961 in a
scratch whose parent carries `MISSION.md` and `.ufo/…`, because two `../`
citations (`corpus/knowledge/source-tree-loss-2026-09-28.md:315`,
`corpus/lessons/round-20-recensus.md:4`) resolve against the extract's parent;
the landed census passes against one cache and fails `pinned-mismatch` against
the other. ReviewC1Census reached the same finding independently (F1) while
re-deriving the numbers (VERIFIED: 162/732, 2551/7559, 2589/7961, host-owned
78). ExecC1Indep AGREE on the numbers and P3. MutC1Counter: 5/12 mutants
killed, 7/12 survive (measured-at format/length, `--write` revision validation,
the host-owned line, body provenance, resolve rc, pinned semantics).
CriticHarm: H1 the frozen `harness_sha256` matches no committed harness (freeze
`0488d796…`, landing `d9713268…`), H2 the `\-` SyntaxWarning. ScribeGate: D1
the dispatch's census numbers are the base reading, D2 the harness pin, D3 the
used-by gaps, D4 the entry's stale `verified-at`, D5 the redaction line count,
D6 the uncommitted live page, D7 the tally, D8 uncommitted evidence, D11 the
219 figure — all corrected in the integration commit. The check also verifies
only the pinned line: body hand-edits, host-line tampering, a `measured-at`
re-point and a poisoned cache all pass (CriticClaimsC1 §4).
Routed to round 99: confine `../` walk-outs to the measured tree (R157);
re-pin the harness and the instrument (R158); strengthen the check to verify
the body and the host-owned line; add controls for the seven survivors.

**C2 — STANDS on K1–K7.** CriticClaimsC2 PASS at seeds 777001 and 424242 (no
kill condition met); ExecC2Probe CONFIRMED (12/12 grammar-derived positives,
15/15 negatives, 0 extra; the round-97 instrument misses 22/22);
MutC2Counter 13/13 required mutants killed; SentinelShapes PASS for all nine
shapes; ScoutSources STANDS against gitleaks 8.30.1 running the upstream rules
(1048 probes, 180 mismatches all tails upstream cannot match, zero divergences
on the two IAM shapes); ConnectorOverlap NONE (no sibling overlap).
Qualifiers: F1 the widened boundary is a superset of S140's class, not the
class (statement erratum; the regex is kept), F2 the SyntaxWarning, F3 the
entry's line-break limit contradicted the instrument, F4 the S140 line citation
(294 → 293), G1 the ci-build boundary is unbound by K3 (M14 survives), G3 K3
does not bind the session context (M16, killed by K2), G4 the selftest does not
bind the registration length (M17), and the behavioural limbs are passable
without the sha pin (counter-coverage). ScoutSources also found the upstream
per-rule prose files: S148 (session cookie, tier A) and S149 (IAM prefixes,
tier B) are added, and the round's "no new row" assertion is corrected.

## Appended corrections` block for `corpus/lessons/round-98.md`

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
