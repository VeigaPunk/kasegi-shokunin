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
