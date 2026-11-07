# ExecC2Probe — round-95 C2 fixture-repo probe (independent)

Seat: ExecC2Probe (leaf). Scope: build my own fixture repository, run the landed
C2 scanner with `--files` at 38e7319f44a9fab2978b59ffd43faf207cf62b32, diff the
exact (file, shape) hit set against an independently derived expectation, and
probe the round-94 base instrument (9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10)
on the same fixtures to show discrimination. Lane fixtures were never touched;
all fixture bytes are synthetic placeholders (aB3/x/y/z repeats).

## Verdict

PROBE RESULT: **PASS**.

- Landed scanner hit set == expected hit set exactly: 23 expected (file, shape)
  pairs over 38 fixture files, observed 23, missing=0, extra=0, rc=1,
  `CAPTURE-SECRET-SCAN mode=files scanned=38 hits=23 files=22 allowed=0 unused_allow=0 rc=1`.
- Round-94 base instrument on the same 38 files: exactly the 3 old-shape pairs
  (`github-token` on neg/ghr36-classic.txt and relocated/c/vendor-notes/ghp36.txt,
  `gitlab-pat` on reg/glpat20.txt), `scanned=38 hits=3 files=3 rc=1` —
  it matches **neither** new shape (base_new_shape_hits=0 on my fixtures).
- Selftest: landed `SELFTEST-RESULT pass cases=115` (rc=0); base
  `SELFTEST-RESULT pass cases=101` (rc=0) — the 101 -> 115 growth re-derived.
- Landed instrument sha256 equals the frozen candidate pin
  66edd66143ec62f6e40c864817a97383916d7ff67e5ab384e130b65c44516707.
- Where I re-derived it myself I say AGREE: the `ghr_` 75/76/77 boundary, the
  escape left boundaries (`\u0020`, `%41`, `\n`, entity, start-of-input), the
  GitLab JWT three-segment grammar (glcbt-/glsat- with optional <=20-char
  instance prefix, gliamat-, first/middle >=10, third >=20, right boundary),
  old shapes still firing (ghp_/ghr_ 36-classic, glpat-), and selftest 101/115.

### Coverage matrix (all required case classes present)

| class | fixtures | C2 observed | R94 observed |
|---|---|---|---|
| ghr_+76 plain / relocated dir+basename / JSON-joined / quote-right | 4 files | github-refresh-token each | none |
| ghr_+76 escaped contexts: `\u0020`, `%41` (forced), HTML entity, start-of-input | 4 files | github-refresh-token each | none |
| 75/76/77 boundary | ghr_+75, ghr_+77 | none (correct) | none |
| ghr_+76 lookahead/lookbehind kills: trailing `_`, dash inside, letter-, underscore-prefixed | 4 files | none (correct) | none |
| ghr_ 36 classic | 1 file | github-token only | github-token |
| glcbt- no prefix / 20-char prefix (max) / in URL query (?ticket=) / JSON `\n` escape / gliamat- / acme-gliamat- / 21-char label + -glcbt / dash inside tail / tail=1000 | 9 files | gitlab-jwt-token each | none |
| glsat- middle not `eyJ`; head not `eyJ`; tail 19; seg 9; tail 1001; seg 1001; letter before; glued 21-alnum prefix; generic JWT in URL; doc placeholder | 10 files | none (correct) | none |
| old shapes regression | ghp_36, glpat-20 | github-token / gitlab-pat | same |

### Probe findings (routed observations, not verdict changes)

1. `pos/gl-jwt-prefix21-overflow.txt` (21-char instance label + `-glcbt-…`)
   **hits**: the grammar caps the *consumed* instance prefix at 20 chars, but the
   match simply begins at `glcbt` (left boundary is the preceding `-`), so
   over-long instance labels still fire. Over-match direction; consistent with
   the instrument's boundary design.
2. `pos/gl-jwt-dash-inside-tail.txt` (`…zzz…-more`) **hits**: `-` is inside the
   third-segment charset `[A-Za-z0-9_-]`, so the variable-length tail absorbs it.
   My first draft labelled this a negative and the v1 run correctly exposed my
   expectation as wrong (EXTRA). The real upper-boundary negatives are the
   {20,1000} caps: third segment 1001 and first segment 1001 both cleanly miss.
3. `neg/generic-jwt-url.txt` (valid three-segment JWT, no provider prefix, in a
   URL query) misses both new shapes — the shapes require the glcbt-/glsat-/
   gliamat- (or ghr_) anchor, so URL context alone does not widen the match.
4. v1 run also caught my own `glpat-` fixture being 19 chars (expectation
   defect, both instruments agreed); fixed to 20 in v2. All v1 divergences were
   fixture/expectation defects, none instrument defects.

## Receipts

All outputs at `.ufo/waves/round-95/w1/ExecC2Probe-receipts/` (written from the
scratch run before the scratch trap wiped it; scratch itself holds nothing):

- `00-setup.txt` — lane base rev 9ef0126…, landing rev 38e7319…, instrument
  sha256s: landed 66edd661…707 (== frozen pin True), base 22ba32d1…eaf.
- `01-fixture-manifest.txt` — 38 files (19 positives-new-shape, 17
  negatives-new-shape, 2 old-shape regression), per-file case-class tags;
  expected pairs C2=23, R94=3; fixture git toplevel asserted
  (exec2probe-fx-o6_q0x3v under TMPDIR scratch).
- `02-scan-c2-files.txt` — landed scanner `--files` full stdout: 21 HIT lines +
  summary `scanned=38 hits=23 files=22 allowed=0 unused_allow=0 rc=1`.
- `03-scan-r94-files.txt` — base scanner `--files` full stdout: 3 HIT lines +
  summary `scanned=38 hits=3 files=3 allowed=0 unused_allow=0 rc=1`.
- `04-selftest-c2.txt` — `SELFTEST-RESULT pass cases=115` (rc=0).
- `05-selftest-r94.txt` — `SELFTEST-RESULT pass cases=101` (rc=0).
- `06-diff-passfail.txt` — empty diff, discrimination findings none, summary
  consistent, `PROBE RESULT: PASS`.
- `07-driver-source.py` — the exact driver (fixture bytes, hand-derived
  expected sets, comparison logic) for reproduction.

Commands executed (rc observed):
1. `git -C <lane> show <rev>:corpus/instruments/…` ×4 (extract both instruments
   + gates to scratch; sha256sum re-verified before running) — rc=0.
2. `git init -q <fixture>` + `git -C <fixture> rev-parse --show-toplevel` == fixture dir — rc=0 asserted.
3. `python3 -B driver.py` (builds fixtures, runs both scanners with `--files
   … --allow <absent>`, selftests, diffs) — v1 rc=1 (2 expectation defects,
   documented above), v2 rc=0 PASS.
4. `ls` receipts dir — 8 files present.

Rules compliance: lane git/jj untouched (read-only `git show`/`rev-parse` only);
no lane fixture used; scratch S=/fast/scratch/hyaku/kasegi-r95/ExecC2Probe with
`trap rm -rf` EXIT and TMPDIR=$S; nothing written outside my report, receipts,
and scratch; no tool installs (none needed); token values are synthetic and
never printed in receipts.
