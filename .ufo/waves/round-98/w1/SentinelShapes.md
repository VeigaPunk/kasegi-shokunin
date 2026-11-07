# SentinelShapes — round 98, C2 nine-shape attack matrix

Seat: SentinelShapes (leaf; no subagent). Lane: `kasegi-shokunin`.
Landing under test: `e2caf4a1561b544a6ea684b0bcfa975f7e7f6061` (C2), read-only.
Instrument: `corpus/instruments/capture-secret-scan.py`; observed sha256
`45f8d226b65e5bf16b9323bfc246c2748319713af5740a608838d6a6eb6f9f0e` = the frozen
pin; `--selftest` prints `SELFTEST-RESULT pass cases=170` (receipt
`selftest-pin.txt`).

## Method

1. Extracted the landing tree with `git archive e2caf4a… | tar -x -C $S/landing`
   (read-only; no lane mutation).
2. Built a 450-payload matrix (`matrix2.py`, receipt) over the nine shapes:
   the 26 separators (`_ - . ; & %26 \u0026 &#x26;`, whitespace, quotes,
   `) ] } , : = / ? # % + |`, CRLF), eight contexts (bare, JSON value,
   Authorization header, URL query, markdown cell, log line, git remote,
   YAML), case variants, length over/under (middle 0/1/5/6, tail 19/20/21,
   IAM 42/43/44, hex 63/64/65, `cell-` digit counts), left-boundary variants,
   and the session-cookie contexts (line start, after a quote, after `; `,
   JSON key, `Cookie:`, `Set-Cookie:`, `_geo_`, `cell-`).
3. Ran every payload through the landed `scan_bytes(data, GITLAB_PATTERNS)`
   (`capture-secret-scan.py:380`) and through a translation of the cited S140
   regexes; classified each cell.
4. Ran exhaustive ASCII sweeps (128 cells each) over the byte before the
   token, the byte after the body, the cookie separator, the gap before/after
   the operator, the cookie value's right boundary, and the keyword's left
   boundary; plus body-grammar sweeps over every length field
   (`body_sweep.py`).

S140 translation (receipts `s140-lines.txt`, `assignment-context.txt`):

- Go `\b` is ASCII → `(?<![0-9A-Za-z_])`; Go `[[:punct:]]` =
  `[!-/:-@\[-`{-~]`, `[[:space:]]` = `[\t\n\v\f\r ]`, `[[:blank:]]` = `[\t ]`.
- Eight prefixed shapes: the published regexes verbatim (S140:293, 480, 497,
  101, 160, 174, 190, 278).
- Session cookie: S140:549 value `(?:cell-[0-9]+-)?[0-9a-f]{64}` plus
  `assignmentContext.keywordGroup = _gitlab_session(?:_geo_[0-9a-f]{64})?`
  with `keywordGroupType = "raw"` (S140:550-551). GitLab's assignment-regex
  generator (MR !151, fetched 2026-11-07, HTTP 200) emits
  `<keywordGroup>.{0,8}[:=].{0,8}(<rhs>)`; `raw` injects the keyword group
  directly. Model **S140_A** = that generated regex. Model **S140_B** (loose
  sensitivity bound only: keyword then value anywhere on the line, no
  operator) is reported separately and is **not** the contract.

## Matrix result

```
MATRIX cases=450
CLASSES AGREE-HIT=359 AGREE-MISS=58 MUST-FIX=12 QUAL-MODEL-B=4 QUAL-S140A-ONLY=7 QUAL-SCANNER-ONLY=10
```

Per-shape (`final-checks.txt`):

```
gitlab-ci-build-token                {'AGREE-HIT': 51, 'AGREE-MISS': 12, 'QUAL-SCANNER-ONLY': 2}
gitlab-iam-refresh-token             {'AGREE-HIT': 47, 'AGREE-MISS': 11, 'QUAL-SCANNER-ONLY': 2}
gitlab-iam-authorization-code        {'AGREE-HIT': 33, 'AGREE-MISS': 6}
gitlab-session-cookie                {'AGREE-HIT': 19, 'AGREE-MISS': 8, 'QUAL-S140A-ONLY': 7, 'MUST-FIX': 12, 'QUAL-MODEL-B': 4, 'QUAL-SCANNER-ONLY': 2}
gitlab-runner-registration-token     {'AGREE-HIT': 51, 'AGREE-MISS': 6, 'QUAL-SCANNER-ONLY': 2}
gitlab-feed-token                    {'AGREE-HIT': 36, 'AGREE-MISS': 3}
gitlab-oauth-app-secret              {'AGREE-HIT': 50, 'AGREE-MISS': 6, 'QUAL-SCANNER-ONLY': 2}
gitlab-feed-token-v2                 {'AGREE-HIT': 36, 'AGREE-MISS': 3}
gitlab-scim-oauth-token              {'AGREE-HIT': 36, 'AGREE-MISS': 3}
```

The eight prefixed shapes are a **superset** of S140_A on every axis tested:
the 128-byte pre and post sweeps produce **zero** S140-only cells
(`ASSERT prefixed-shape sweeps: S140_A-only cells = 0 (expected 0)`), and the
body sweeps produce zero divergence in both directions:

```
ci-build middle                        s140A_only=0 scanner_only=0 both=5 neither=203
iam-refresh segs                       s140A_only=0 scanner_only=0 both=1 neither=120
iam-auth segs                          s140A_only=0 scanner_only=0 both=1 neither=120
gitlab-runner-registration-token tail  s140A_only=0 scanner_only=0 both=1 neither=10
gitlab-feed-token tail                 s140A_only=0 scanner_only=0 both=1 neither=10
gitlab-oauth-app-secret tail           s140A_only=0 scanner_only=0 both=1 neither=10
gitlab-feed-token-v2 tail              s140A_only=0 scanner_only=0 both=1 neither=10
gitlab-scim-oauth-token tail           s140A_only=0 scanner_only=0 both=1 neither=10
```

The five widened shapes do hit a real token followed by `_`/`-`
(`pos-reg-underscore`, `pos-reg-hyphen`, `pos-feed-underscore`,
`pos-oauth-hyphen`, `pos-feed2-underscore`, `pos-scim-hyphen` = AGREE-HIT), so
the round-97 defect class is closed for them. The only divergences on the
eight are the scanner being **looser** than S140 (control bytes after the six
punct/space-bounded shapes; `%26`/`\u0026` left escapes; see qualifiers).

## MUST-FIX

All twelve are the **session-cookie assignment context**. The scanner's
separator model is `[\s\"'=:;]+` (`capture-secret-scan.py:308-310`); S140's
generated regex is `<keyword>.{0,8}[:=].{0,8}<value>`. Every payload below is
a full real 64-hex session value, `scan_bytes` returns no hit, S140_A returns
`gitlab-session-cookie`, and the **full 39-pattern gate set** also returns no
hit (`final-checks.txt`, `gap-map.txt`):

| id | payload (H = 64 lower-case hex) | scanner | S140_A | full gate |
|---|---|---|---|---|
| M1 `ck-ruby-hash-rocket` | `_gitlab_session => H` | miss | hit | miss |
| M2 `ck-rocket-nospace` | `_gitlab_session=> H` | miss | hit | miss |
| M3 `ck-pct20-eq` | `_gitlab_session%20=%20H` | miss | hit | miss |
| M4 `ck-pct20-colon` | `_gitlab_session%20:%20H` | miss | hit | miss |
| M5 `ck-pct20-after-eq` | `_gitlab_session=%20H` | miss | hit | miss |
| M6 `ck-geo-pct20` | `_gitlab_session_geo_H%20=%20H` | miss | hit | miss |
| M7 `ck-comma-eq` | `_gitlab_session,=H` | miss | hit | miss |
| M8 `ck-pipe-eq` | `_gitlab_session` + `|=` + H (pipe escaped in this table) | miss | hit | miss |
| M9 `ck-plus-eq` | `_gitlab_session+=H` | miss | hit | miss |
| M10 `ck-paren-eq` | `_gitlab_session(=H)` | miss | hit | miss |
| M11 `ck-paren-gap` | `_gitlab_session ( = ) H` | miss | hit | miss |
| M12 `len-cookie-cell0` | `_gitlab_session=cell--H` | miss | hit | miss |

Observed (`gap-map.txt`):

```
ruby-hash-rocket     scan_hit=False s140A_hit=True full_gate=-
ruby-rocket-nospace  scan_hit=False s140A_hit=True full_gate=-
pct20-eq             scan_hit=False s140A_hit=True full_gate=-
pct20-colon          scan_hit=False s140A_hit=True full_gate=-
pct20-after-eq       scan_hit=False s140A_hit=True full_gate=-
geo-pct20            scan_hit=False s140A_hit=True full_gate=-
comma-eq             scan_hit=False s140A_hit=True full_gate=-
pipe-eq              scan_hit=False s140A_hit=True full_gate=-
plus-eq              scan_hit=False s140A_hit=True full_gate=-
paren-eq             scan_hit=False s140A_hit=True full_gate=-
paren-gap            scan_hit=False s140A_hit=True full_gate=-
cell--               scan_hit=False s140A_hit=True full_gate=-
```

The class is general, not a list of twelve strings: the ASCII sweep over the
gap before the operator (`_gitlab_session<C>=H`) and after it
(`_gitlab_session=<C>H`) finds **117 of 128** characters where S140_A hits and
the scanner misses (the 11 non-misses are `\n`, which is scanner-only, and the ten other
characters of the scanner's own class, which both hit). The plausible real-world members are `=>` (Ruby/Perl
hash rocket, high realism), `%20` around `:`/`=` (percent-encoded whitespace,
medium), and `, | + ( ) [ ] { } < >` (structured logs, low). M12 (`cell--`) is
the same gap mechanism consuming a malformed `cell-` prefix; low realism.

Impact: a real GitLab session cookie value written in any of these forms
passes the lane's capture gate unseen, while GitLab's own rule detects it.
The C2 claim's K3 negatives (`capability-check.py:159-170`) test only length
defects per shape (`63` hex, `42`/`44`-char IAM segments, `6`-char CI middle,
`21`-char tails), so this class is outside the claim's counter.

## Routed qualifiers (not MUST-FIX)

- **Q1 — keyword left boundary (S140_A-only, prefixed keyword).**
  `x_gitlab_session=H` and `__gitlab_session=H` are missed by the scanner but
  hit by S140_A, because the raw keyword group has no left boundary while the
  scanner's `_GL_LB` requires a non-word byte. The value is real but the
  cookie name is not GitLab's; S140 over-detects a prefixed name. Sweep:
  63/128 preceding ASCII chars (`[0-9A-Za-z_]`) are S140_A-only
  (`gap-map.txt`).
- **Q2 — 65+ hex truncation (S140_A-only).** `_gitlab_session=H0` (65 hex):
  S140 matches the first 64 hex (the value regex has no right boundary), the
  scanner's `(?![0-9a-f])` refuses. No 64-hex token is present as a delimited
  value; sweep: 16/128 following chars (the hex alphabet).
- **Q3 — scanner over-detection (scanner-only).** The scanner hits where
  S140_A does not: `_gitlab_session cell-7-H` (no operator; separator class
  accepts a space), `_gitlab_session\n=H` (newline in `\s`; S140's `.` does
  not cross lines), and the `%26`/`\u0026` left escapes before the eight
  prefixed shapes (the scanner's `_GL_LB` escape alternatives are looser than
  Go `\b`). These are false positives / gate cost, not misses.
- **Q4 — IAM shapes followed by `_`/`-` (both miss).** `gliamrt-…_x` and
  `gliamac-…-x` are refused by both the scanner (`(?![A-Za-z0-9_-])`) and
  S140 (`[^0-9a-zA-Z_\-]`). This is source-faithful; the round-97 widening
  claim covers the five punct-bounded shapes only, so no defect is charged
  here, but the round-97 lesson's miss class still exists for the two IAM
  shapes if S140's boundary is wrong.
- **Q5 — documentation/implementation mismatch.** The knowledge entry says
  "a cookie value separated from its name by a line break is out of scope —
  the rule's own context window is the same line"
  (`corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`,
  Limits). The scanner's `\s` includes `\n`, so it *does* detect
  `_gitlab_session\n=H` (QUAL-SCANNER-ONLY). Over-detection, not a miss.
- **Q6 — S140 over-attribution.** `_gitlab_session; foo=H` and
  `_gitlab_session x=H` are S140_A hits (the `.{0,8}` gap bridges to another
  assignment's `=`) and scanner misses. The value is real but assigned to
  `foo`/`x`; S140's gap model is the false-positive source. Not charged as a
  scanner defect.

## Smallest remediation (reported, not applied — read-only seat)

In `capture-secret-scan.py:308-310`, replace the session-cookie separator
`[\s\"'=:;]+` with the union
`(?:[\s\"'=:;]+|.{0,8}[:=].{0,8})` (keeps every current detection and adds the
S140 assignment gaps), or with `.{0,8}[:=].{0,8}` alone for strict S140 parity
(which drops the current no-operator/newline detections and adds S140's
over-attribution). Keep the value's `(?![0-9a-f])` right boundary (stricter
than S140; prevents the Q2 truncation false positive). Add selftest cases for
`_gitlab_session => H`, `_gitlab_session%20=%20H`, and
`_gitlab_session,=H`; the current 170 cases have no assignment-gap case.

## Evidence index

- `matrix2.py`, `body_sweep.py` — harnesses (receipt dir).
- `matrix.tsv` (450 rows), `matrix-run.txt`, `sweeps.tsv`, `body-sweep.txt`,
  `gap-map.txt`, `final-checks.txt`.
- `s140-lines.txt` (S140:293/480/497/549-551 and the five widened rules),
  `scanner-lines.txt` (landing lines 302-322, 380-395),
  `assignment-context.txt` (MR !151 generated-regex form + knowledge entry),
  `capability-negatives.txt` (K3 negatives), `selftest-pin.txt`.

Commands (all read-only; the scratch tree is removed after the seat, and the
landing extract is reproducible with `git archive e2caf4a…`):

```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show e2caf4a…:corpus/instruments/capture-secret-scan.py | sha256sum
cd $S/landing && python3 -B corpus/instruments/capture-secret-scan.py --selftest
cd $S && python3 -B matrix2.py
cd $S && python3 -B body_sweep.py
```

VERDICT: gitlab-ci-build-token — PASS: scanner ⊇ S140_A (0 S140-only cells in the 128-byte pre/post sweeps; body sweep middle 0-7 × tail 0-25: 0 divergence).
VERDICT: gitlab-iam-refresh-token — PASS: 0 S140-only cells; body sweep 38-48 × 38-48: 0 divergence; a real token followed by `_`/`-` is missed by both, source-faithful.
VERDICT: gitlab-iam-authorization-code — PASS: 0 S140-only cells; body sweep 38-48 × 38-48: 0 divergence; same `_`/`-` note.
VERDICT: gitlab-session-cookie — MUST-FIX: the `[\s"'=:;]+` separator is narrower than S140's generated `<keyword>.{0,8}[:=].{0,8}<value>`; 117/128 ASCII gap chars, `=>`, and `%20` forms are missed, and the full 39-pattern gate returns no hit.
VERDICT: gitlab-runner-registration-token — PASS: widened `_`/`-` boundary matches S140's punct/space/EOL; 0 S140-only cells.
VERDICT: gitlab-feed-token — PASS: widened boundary matches S140; 0 S140-only cells.
VERDICT: gitlab-oauth-app-secret — PASS: widened boundary matches S140; 0 S140-only cells.
VERDICT: gitlab-feed-token-v2 — PASS: widened boundary matches S140; 0 S140-only cells.
VERDICT: gitlab-scim-oauth-token — PASS: widened boundary matches S140; 0 S140-only cells.
VERDICT: C2 landing instrument — PASS: sha256 equals the frozen pin; selftest 170.
