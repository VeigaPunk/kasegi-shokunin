# SentinelEscape — round 93, attempt 1

Leaf seat. Surface: adversarial probe of the landed `capture-secret-scan` at
`9225954a6e3f177af46bdb9d811c062a4353a552` (C2 landing), run from copies of that rev's
`capture-secret-scan.py`, `claim-package-check.py` and `capture-secret-allow.tsv` in seat scratch.
Lane git/jj state only read; no tool installed or upgraded; no lane file edited by this seat.

## Verdict

**C2 STANDS on the frozen predicate** (re-derived, not repeated): P1 `CAPABILITY-CHECK-RESULT pass rc=0`
at seeds 1, 9191 and a printed random seed; P2 all three pins equal; P3 exactly the two named paths.
67 adversarial probes: **44 DETECTED / 23 MISSED** — 11 misses are statement-named negatives behaving
as written, **12 are unnamed miss classes routed to round 94**; FP-shaped detections in the FP class: **2**
(plus 4 boundary qualifiers); **22 adversarial lines (20 of them ≥ 1 MB) × 3 samples: max 1.241 s, no timeout at 30 s**,
the new shapes at or below the 1 MB filler baseline.

| measure | observed |
|---|---|
| probes | 67 (34 encodings around `glpat-`, 25 escape-family for `github-token`, 8 FP/boundary) |
| DETECTED / MISSED | 44 / 23 |
| statement-named negatives correctly missed | 11 of 11 |
| unnamed misses (routed, round 94) | 12 |
| FP-shaped detections (class c) | 2 (`c01` documentation placeholder, `c02` 20-character prose run) |
| boundary qualifiers | 4 (3 encoded-letter evasions, 1 `github-token` right `-` asymmetry) |
| ReDoS | 22 lines × 3 samples, 0 timeouts, max 1.241 s (`t22`, 1.26 MB); new shapes max 0.547 s; 1 MB filler max 0.680 s |
| P2 pins | instrument `7d9d7309…83c5` = candidate; gate `8b6f8493…c8e6`; counter `8a4ad508…1bb6` |
| P3 paths | `SCORECARD.md`, `corpus/instruments/capture-secret-scan.py` only; capability row byte-equal |

No frozen-predicate limb failed. The 12 unnamed misses and the 4 qualifiers below do not re-score the
claim; they are routed defects/qualifiers for round 94.

## What was measured

Fixtures are one file each, fabricated for this seat (`AbCdEf0123456789_-xy`-class tails, 20/36-character
constructed bodies), written under the seat scratch and deleted with it; no real value appears in any
fixture, receipt or table. `probes.tsv` carries fixture sha256 only, never matched bytes. Per-shape
behaviour was taken through `scan_bytes` (the same entry the counter uses) and cross-checked with the CLI
`--files` over all 67 fixtures (`scanned=67 hits=45 files=44 rc=1`; the extra hit is `a03`, whose JSON key
`token` also trips the gate's `credential` shape).

### (a) 34 encodings around `glpat-` (`probes.tsv` ids a01–a34)

| id | position / encoding | observed | deciding mechanism |
|---|---|---|---|
| a01 | plain prose, space before prefix | DETECTED | primary `(?<![A-Za-z0-9_-])`: space |
| a02 | JSON value, quote before | DETECTED | quote |
| a03 | JSON key `token` | DETECTED | `gitlab-pat` + gate `credential` (quote) |
| a04 | YAML mapping key | DETECTED | space |
| a05 | YAML list line `- ` | DETECTED | space |
| a06 | `.git-credentials` userinfo `oauth2:` | DETECTED | `:` |
| a07 | JSON `\t` escape | DETECTED | `(?<=\\[ntr])`, width 2 |
| a08 | JSON `\r` escape | DETECTED | `(?<=\\[ntr])` |
| a09 | JSON `\u0020` | DETECTED | `(?<=\\u[0-9A-Fa-f]{4})`, width 6 |
| a10 | JSON `\u0026` | DETECTED | same |
| a11 | `%20` | DETECTED | `(?<=%[0-9A-Fa-f]{2})`, width 3 |
| a12 | `%3A` encoded userinfo colon | DETECTED | `%XX` |
| a13 | `%2F` double-encoded path | DETECTED | `%XX` |
| a14 | `%26` | DETECTED | `%XX` |
| a15 | decimal HTML entity `&#38;` | DETECTED | `;` already passes the primary lookbehind (entity alternative redundant) |
| a16 | hex HTML entity `&#x26;` | DETECTED | `;` (same) |
| a17 | UTF-8 BOM immediately before | DETECTED | `0xBF` not in the class |
| a18 | CRLF immediately before | DETECTED | raw `0x0a` not in the class |
| a19 | double percent-encoded `%253A` | **MISSED** | last two bytes `3A` are alphanumeric; no alternative matches — unnamed |
| a20 | double percent-encoded `%2520` | **MISSED** | same — unnamed |
| a21 | C-style `\x20` | **MISSED** | no `\xXX` alternative — unnamed |
| a22 | legacy `%u0020` | **MISSED** | no `%uXXXX` alternative — unnamed |
| a23 | octal `\040` | **MISSED** | no octal alternative — unnamed |
| a24 | JSON `\f` (form feed) | **MISSED** | valid JSON escape; `[ntr]` excludes `f` — unnamed |
| a25 | JSON `\b` (backspace) | **MISSED** | valid JSON escape; `[ntr]` excludes `b` — unnamed |
| a26 | `%61` before prefix (encodes `a`) | DETECTED | `%XX` permits any byte; decoded text is `aglpat-` (see qualifier Q1) |
| a27 | `\u0061` before prefix (encodes `a`) | DETECTED | same as a26 |
| a28 | UTF-16LE whole line | MISSED | statement-named limit (`UTF-16 … not detected`) |
| a29 | JSON escaped slashes `\/` | DETECTED | `/` passes the primary lookbehind |
| a30 | two consecutive escapes `%3a%09` | DETECTED | last escape satisfies `%XX`; lower-case hex covered |
| a31 | literal TAB byte | DETECTED | `0x09` not in the class |
| a32 | literal letter before prefix | MISSED | statement negative (`letter-prefixed token`) |
| a33 | encoded prefix separator `glpat%2D` | MISSED | statement named limit (`encoded prefix separators`) |
| a34 | 20-char tail containing `-` and `_` | DETECTED | lane alphabet choice `A-Za-z0-9_-`, as documented |

All 12 encodings named in the ticket (JSON `\t`/`\u0020`/`\u0026`, `%20`/`%3A`/`%2F`/`%26`, HTML entities,
BOM, CRLF, YAML/JSON keys, `.git-credentials`, double-encoded separator) are covered above; the first 18
and a29–a31/a34 are detected, the double-encoded separator is the measured miss of that set.

### (b) 25 escape-family probes for `github-token` (b01–b25)

| id | escape before token | r92 P1 id | observed |
|---|---|---|---|
| b01 | JSON `\t` | b11 | DETECTED |
| b02 | JSON `\r` | b12 | DETECTED |
| b03 | JSON `\u000a` | b20 | DETECTED |
| b04 | JSON `\u0020` | b15 | DETECTED |
| b05 | `%20` | e05 | DETECTED |
| b06 | `%20` inside a JSON query value | b14 | DETECTED |
| b07 | `%09` | e06 | DETECTED |
| b08 | `%3A` (`x-access-token%3A`) | b13 | DETECTED |
| b09 | `%2F` (double-encoded path) | e04 | DETECTED |
| b10 | `\u0026` | e01 | DETECTED |
| b11 | `%26` | e02 | DETECTED |
| b12 | `&#38;` | e03 control | DETECTED |
| b25 | `&#x26;` | — | DETECTED |
| b18 | literal TAB byte | — | DETECTED |
| b22 | stateless `ghs_<digits>_<JWT>` behind `%20` | — | DETECTED |
| b19 | `%61` before prefix (encodes `a`) | — | DETECTED (qualifier Q1) |
| b21 | trailing `-` after a full 36-char tail | — | DETECTED (qualifier Q2) |
| b13 | JSON `\f` | — | **MISSED** (unnamed) |
| b14 | JSON `\b` | — | **MISSED** (unnamed) |
| b15 | `\x20` | — | **MISSED** (unnamed) |
| b16 | double-encoded `%2520` | — | **MISSED** (unnamed) |
| b17 | `%u0020` | — | **MISSED** (unnamed) |
| b20 | escape + trailing `_` | — | MISSED (statement negative) |
| b23 | encoded prefix separator `gh%5Fp_` | — | MISSED (statement named limit) |
| b24 | fine-grained `github_pat_` | — | MISSED (statement named limit) |

The r92 P1 eleven are reproduced class-for-class with this seat's own fabricated values (the r92 fixture
bytes were deleted with that seat's scratch, so the r92 fixture digests cannot be re-derived here); all
eleven now report `github-token`. The landing diff against the freeze replaces only `_GH_LB` (`(?<=\\n)`
→ `_ESC_LB`) and adds the gitlab shape; no round-87..91 pattern text changes.

### (c) 8 false-positive / boundary probes (c01–c08)

| id | fixture | observed | classification |
|---|---|---|---|
| c01 | documentation-style placeholder `glpat-` + 20 `x` | DETECTED | FP-shaped by the frozen shape; no `ALLOWED_VALUES` entry, needs an allow row at a capture path (qualifier Q3) |
| c02 | 20-character prose word after a bare `glpat-` | DETECTED | same class; a separator-free prose run is indistinguishable (qualifier Q3) |
| c03 | 21-character tail | MISSED | statement negative, as written |
| c04 | 19-character tail | MISSED | statement negative |
| c05 | the S139 line-87 bare-prefix sentence | MISSED | statement negative |
| c06 | `GLPAT-` upper-case prefix | MISSED | statement negative (case-sensitive) |
| c07 | `glrt-` runner prefix | MISSED | statement named limit |
| c08 | 20-char tail ending in `-` | DETECTED | legitimate shape positive (alphabet includes `-`) |

**S139 page text (the claim's own capture):** full file, 25,370 bytes, sha256
`154a7e15…1b188`; `0` hits, `allowed=4`, `used_rows=4`; raw matches on the page are
`bearer:1, credential:3` and every one is bound by one of the four S139 allow rows, so the allowlist is
load-bearing for this capture (unused rows on the single-file scan: 19). The page's only `glpat-`
occurrence is the line-87 prose (`glpat- followed by a 20-character string`) and it is not a hit.

### (d) ReDoS timing (22 adversarial lines, 20 of them ≥ 1 MB, each timed three times)

| line | bytes | max of 3 samples |
|---|---|---|
| t01 filler `A` | 1,048,576 | 0.680 |
| t02 `glpat-` + 1 MB tail | 1,048,576 | 0.547 |
| t03 `glpat-` repeated | 1,048,572 | 0.394 |
| t04 `sv=…` + `&ab=1` repeated | 1,048,573 | 0.833 |
| t05 `sv=…&ab=` + 1 MB value | 1,048,574 | 0.661 |
| t06 `CloudFront-Signature=` + 1 MB | 1,048,576 | 0.289 |
| t07 `X-Goog-Signature=` + 1 MB | 1,048,576 | 0.439 |
| t08 `%20` repeated | 1,048,575 | 0.437 |
| t09 `\u0020` repeated | 1,048,572 | 0.915 |
| t10 `&#38;` repeated | 1,048,575 | 0.987 |
| t11 `ghp_` + 1 MB tail | 1,048,576 | 0.395 |
| t12 `&` repeated | 1,048,576 | 0.726 |
| t13 `sig=` + 1 MB value | 1,048,576 | 0.718 |
| t14 20 params then `&sig=` (small control) | 118 | 0.000 |
| t15 gate JSON key + 1 MB | 1,048,576 | 0.615 |
| t16 `\` repeated | 1,048,576 | 0.708 |
| t17 `Key-Pair-Id=` + 1 MB | 1,048,575 | 0.520 |
| t18 `CloudFront-Signature=` + 1 MB | 1,048,576 | 0.532 |
| t19 `sv=`+20 params+`&sig=` repeated | 479,552 | 0.345 |
| t20 `sv=…&ab=` empty params | 1,048,576 | 0.661 |
| t21 `sv=…&sig=<39>` repeated | 1,171,920 | 0.545 |
| t22 `Key-Pair-Id=…`+params repeated | 1,256,284 | **1.241** |

0 timeouts at the 30 s per-line alarm; global max 1.241 s (`t22`, a pre-existing CloudFront shape).
The new shapes' own worst-case lines (t02/t03/t11) run at 0.39–0.55 s, i.e. at or below the 1 MB filler
baseline (0.29–0.68 s on this loaded host); the escape-repeat lines (t09/t10) peaked at 0.92–0.99 s and stay linear.
End-to-end CLI on the per-sample worst line: 0.573–1.002 s. No superlinear behaviour observed.

## Re-derived predicate (independent of the counter's own report)

- **P1** — `capability-check.py` at the pinned counter sha passed K1–K8 at seed 1, seed 9191 and one
  printed random seed (`2237662211`), `nonce` differing per run (`994cd58c`, `0dd83984`, `3a450b6a`), `missing=none extra=none`, `clauses=50 failing=none`, `rows=1`.
- **P2** — landing blob `capture-secret-scan.py` sha256 `7d9d7309d5a5eddde59dbbb49767d71f43ec78667f1c3aa05bb1c76a45f683c5`
  equals the frozen candidate; gate `8b6f849349…c8e6` equals the gate pin; counter `8a4ad508…1bb6` equals
  the counter pin; worktree copy at probe time matched the landing blob.
- **P3** — `git diff-tree --no-commit-id --name-status -r 9225954a` prints exactly
  `M SCORECARD.md` and `M corpus/instruments/capture-secret-scan.py`; the `capture-secret-scan` row in
  `SCORECARD.md` at the landing is byte-equal to `.ufo/waves/round-93/c2/candidate-row.txt`
  (frozen file sha256 `6d18d579…e3fb40`, one row in the table).
- **K3 equivalent** — full rev scan at the landing: `scanned=1957 hits=0 files=0 allowed=24 unused_allow=0 rc=0`;
  no allow row is stale and no landing capture trips the extended shapes.

## Routed defects for round 94 (unnamed misses; nothing widened here)

Every miss below is outside the frozen statement and outside its named-limit list. The remediation was
measured in memory against the same 67 fixtures (no lane file edited): extend the shared escape lookbehind
with fixed-width alternatives `(?<=\\x[0-9A-Fa-f]{2})`, `(?<=%u[0-9A-Fa-f]{4})`, `(?<=\\[0-7]{3})`,
`(?<=%25[0-9A-Fa-f]{2})`, and widen `[ntr]` to `[ntrfb]`.

| id | class | observed | closes with |
|---|---|---|---|
| a19, a20, b16 | double-encoded `%25XX` separator | MISSED | `(?<=%25[0-9A-Fa-f]{2})` |
| a21, b15 | C-style `\xXX` escape | MISSED | `(?<=\\x[0-9A-Fa-f]{2})` |
| a22, b17 | legacy `%uXXXX` escape | MISSED | `(?<=%u[0-9A-Fa-f]{4})` |
| a23 | octal `\0NN` escape | MISSED | `(?<=\\[0-7]{3})` |
| a24, b13 | JSON `\f` escape | MISSED | `[ntr]` → `[ntrfb]` |
| a25, b14 | JSON `\b` escape | MISSED | `[ntr]` → `[ntrfb]` |

Measured result: **12/12 unnamed misses flip to DETECTED**, **0 regressions** on the 11 statement-named
negatives, and the landing rev scan under the patched boundary still prints
`scanned=1957 hits=0 files=0 allowed=24 unused_allow=0 rc=0` (`patch-measure.txt`). Recommended round-94
route: one shared `_ESC_LB` for both shapes (as the code already does for github/gitlab) with those five
additions, plus selftest rows for each; the double-encoded form is the lowest-realism of the six.

## Qualifiers (not verdict changes)

- **Q1 — encoded-letter boundary.** `%61glpat-…`, `\u0061glpat-…`, `%61ghp_…` are DETECTED although the
  decoded text is `aglpat-…`/`aghp_…`, i.e. the statement's own "letter-prefixed token is not a hit"
  negative is defeated by encoding. This is faithful to the frozen sentence (the terminator *form* is
  what is allowed, regardless of the byte it encodes) but is a boundary-precision gap. A lookbehind
  cannot reject an escaped alphanumeric byte; the closest remedy is a post-match decoded-byte check in
  `scan_bytes` (not measured — a code change, not a one-line regex).
- **Q2 — right-boundary asymmetry.** `github-token` ends with `(?![A-Za-z0-9_])`, so a 41st `-` is accepted
  (`ghp_<36>-y` → hit); `gitlab-pat` ends with `(?![A-Za-z0-9_-])`. The frozen sentence states the github
  class as letter/digit/`_`, so this is consistent; note it if the github shape is ever tightened.
- **Q3 — documentation placeholder is an allowlist job.** A GitLab docs-style placeholder
  (`glpat-` + 20 `x`) or a separator-free 20-character prose run is a shape-identical hit and is not in
  `ALLOWED_VALUES`; the instrument's own contract requires an allowlist row per exact value and path.
  S139 contains no such value, so the landed corpus is clean (`hits=0`), but a future capture of a page
  that shows a 20-character example will exit 1 until a row is added.
- **Q4 — statement wording on the nonce.** K4's 76 plants are all rerooted with a per-run
  `os.urandom(4).hex()` nonce (measured: `reroot('g/…')` at K7 returns the path unchanged). K7's 27
  generated files live at fixed relative paths (`g/x-receipts/…`), so "plants every value under a
  run-time nonce directory" holds for K4 and not literally for K7. Impact is nil for the named threat:
  K4 is matched exactly (`missing=none extra=none`) and its relative paths are nonce-rotated, so a
  path-keyed forgery cannot pass K4; the G8 path-keyed forgery control is recorded rejected (`CONTROL G8-path-keyed rc=1 want=1 PASS`, `.ufo/waves/round-93/controls/c2-controls-r93.txt:112`; not re-run here). Wording only —
  suggest "every K4 value".

## Receipts

`S=/fast/scratch/hyaku/kasegi-r93/SentinelEscape`; cwd `/home/vgpnk/Projects/shokunin/kasegi-shokunin`;
`TMPDIR=$S`; scratch deleted after the seat. All outputs cited are under
`.ufo/waves/round-93/w1/SentinelEscape-receipts/`.

| command | observed |
|---|---|
| `git show 9225954a:corpus/instruments/{capture-secret-scan.py,claim-package-check.py,capture-secret-allow.tsv}` → scratch copies | rc 0; sha256 `7d9d7309…83c5`, `8b6f8493…c8e6`, `a5abeb53…7c3c` |
| `sha256sum .ufo/waves/round-93/c2/{candidate-capture-secret-scan.py,capability-check.py} corpus/instruments/claim-package-check.py` | rc 0; candidate `7d9d7309…83c5`, counter `8a4ad508…1bb6`, gate `8b6f8493…c8e6` (all equal to the frozen pins) |
| `git diff-tree --no-commit-id --name-status -r 9225954a…` | rc 0; 2 lines: `M SCORECARD.md`, `M corpus/instruments/capture-secret-scan.py` |
| `python3 -B $S/instruments/capture-secret-scan.py --selftest` | rc 0; `SELFTEST-RESULT pass cases=90` (`selftest.txt`) |
| `python3 -B $S/probe.py` | rc 0; 67 probes → `probes.tsv` (67 data rows), `probe-run-stdout.txt`, `timing.tsv` |
| `python3 -B $S/patch_measure.py` | `FLIP-COUNT 12`, `NAMED-NEGATIVE-REGRESSIONS 0`, `REV-SCAN-PATCHED rc=0 … hits=0 … unused_allow=0` (`patch-measure.txt`) |
| `python3 -B $S/timing_samples.py` | 3 samples × 23 timing lines; `GLOBAL-MAX 1.241`; CLI worst-line 0.573/1.002/0.716 s (`timing-samples.tsv`) |
| `python3 -B $S/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-93/S139.txt` | rc 0; `scanned=1 hits=0 files=0 allowed=4 unused_allow=19 rc=0` (`s139-file-scan.txt`) |
| `python3 -B $S/instruments/capture-secret-scan.py --lane <abs lane> --rev 9225954a…` | rc 0; `scanned=1957 hits=0 files=0 allowed=24 unused_allow=0 rc=0` (`rev-scan.txt`) |
| `python3 -B $S/instruments/capture-secret-scan.py --files <67 fixtures>` | rc 1; `scanned=67 hits=45 files=44 allowed=0 unused_allow=23 rc=1` (`cli-fixtures.txt`) |
| `python3 -B .ufo/waves/round-93/c2/capability-check.py --lane <abs> --rev 9225954a… --instrument-sha256 7d9d… --gate-sha256 8b6f… --seed 1` | rc 0; `CAPABILITY-CHECK-RESULT pass rc=0`, all K1–K8 pass, nonce `994cd58c` (`capability-seed1.txt`) |
| same, `--seed 9191` | rc 0; pass, nonce `0dd83984` (`capability-seed9191.txt`) |
| same, no `--seed` | rc 0; pass, seed `2237662211`, nonce `3a450b6a` (`capability-default-seed.txt`) |
| `git show 9225954a:SCORECARD.md` vs `.ufo/waves/round-93/c2/candidate-row.txt` | row equal `True`; one row; frozen file sha256 `6d18d579…e3fb40` |
| `git diff 5bad9e5 9225954a -- corpus/instruments/capture-secret-scan.py SCORECARD.md` | only `_GH_LB` → `_ESC_LB`, the added gitlab shape/selftest rows/docstring, and the capability row |
| nonce coverage of K4/K7 (`nonce-coverage.txt`) | `K4 PLANTS=76`, all rerooted; `reroot('g/…')` unchanged; `K7 FILES=27 EXPECT=12`, no nonce in paths |
| state snapshot (`state.txt`) | `head=9225954…`, worktree instrument sha256 = landing sha256; 17 porcelain lines (other seats' files, untouched) |

Fixture/scratch cleanup: `rm -rf /fast/scratch/hyaku/kasegi-r93/SentinelEscape` on seat exit; nothing of
this seat remains outside the report and receipts paths above.
