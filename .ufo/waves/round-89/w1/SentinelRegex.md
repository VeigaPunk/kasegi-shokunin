# SentinelRegex — round 89 attack seat

**Subject.** `corpus/instruments/capture-secret-scan.py` at the C2 landing
`c61c55868e6d28653f57413bac6a6de5a398d11f`, sha256
`95f24a541db8b3d6693315a03de28d0b6de0fb0b6e53a68471265382114d20ec` — byte-equal
to the working tree and to the C2 landing receipt's K1 pin
(`.ufo/waves/round-89/l1/c2-landing-r89.txt:4`). r88 baseline: the same file at
`b43dc2154bc09470da2209fb626021da3af3593e`, sha256
`d73495364f90f78fa5ee6ad28b83fce772a349a5339d240b21db4d5d04425417` — the digest
r88's report cites. Both read with `git show` + `sha256sum`, never from the
claim (`SentinelRegex-receipts/pins.txt`).

**Hypothesis (falsifiable).** The two r89 pattern changes — the new
`cloudfront-signed-url-signature` and `azure-sas-signature`'s left-boundary
group that admits `\u0026`/`%26` — grow super-linearly on adversarial 1–4 MiB
single-line inputs, or exceed 5 s at 4 MiB.

**Verdict: REFUTED.** No input class grows super-linearly. The paired doubling
ratio — both sizes measured inside the same rep, so both see the same host load
— is **1.97–2.04 against 2.000 for linear**, at every step from 1 to 8 MiB, for
every adversarial class. Worst case at 4 MiB is **1.52 s** for the full
11-shape scan (`cf-many-long`) and **1.44 s** for `az-sv-dense`; at 8 MiB the
worst is **2.43 s**. Nothing reaches 5 s at any tested size. The r89 change
does make one *existing* shape **25–28× more expensive** (`\u0026`-dense text,
§5), which is a real performance qualifier and still linear, still under 1 s at
4 MiB.

Scoring impact: none. No frozen predicate of C1 or C2 reads performance; K1–K8
are untouched by this seat. Everything below is a routed defect / qualifier for
round 90.

---

## 1. The two changed patterns, exactly

```python
_SEP  = rb"(?:&amp;|&|\\u0026)"
_PARAM = rb"(?:" + _SEP + rb"[A-Za-z]{2,6}=[^&\s\"'<>\\]*){0,20}?"
_SIG   = rb"sig=[A-Za-z0-9%+/]{40,}(?:=|%3D){0,2}"
_SV    = rb"sv=\d{4}-\d{2}-\d{2}"
_LB   = rb"(?:(?<![A-Za-z0-9_])|(?<=\\u0026)|(?<=%26))"          # r89: was (?<![A-Za-z0-9_])
_CF_LB    = rb"(?:(?<![A-Za-z0-9_-])|(?<=\\u0026)|(?<=%26))"
_CF_PARAM = rb"(?:" + _SEP + rb"[A-Za-z][A-Za-z0-9_-]{0,31}=[^&\s\"'<>\\]*){0,20}?"
_CF_SIG   = rb"Signature=[A-Za-z0-9_~-]{40,}"
_CF_KPI   = rb"Key-Pair-Id=[A-Z0-9]{8,32}(?![A-Za-z0-9_-])"

azure     = rb"(?i)" + _LB + rb"(?:" + _SV + _PARAM + _SEP + _SIG
                            + rb"|" + _SIG + _PARAM + _SEP + _SV + rb")"
cloudfront= _CF_LB + rb"(?:" + _CF_SIG + _CF_PARAM + _SEP + _CF_KPI
                            + rb"|" + _CF_KPI + _CF_PARAM + _SEP + _CF_SIG + rb")"
```

Four structural facts bound the work, and they are why the hypothesis fails:

1. **Both patterns have no literal prefix.** Each starts with a zero-width
   lookbehind group, so CPython attempts a match at *every* byte offset instead
   of skipping to a literal. That is a per-byte constant, not a growth term —
   it is the same property r88 documented for the azure alternation (r88 D1).
2. **The `{0,20}?` parameter window is a work cap.** At a start position the
   engine performs at most 21 expansions, then gives up. Only ≤20 starts can
   reach any given value run.
3. **Every unbounded value class excludes every separator byte.** `_CF_SIG`'s
   `[A-Za-z0-9_~-]` and `_SIG`'s `[A-Za-z0-9%+/]` both exclude `&` and `\`, the
   only two bytes any `_SEP` alternative can start with. So a value run's right
   boundary is unique, `_SEP` can never match inside one, and each backtrack
   position of the run costs O(1) — not O(value).
4. **The unbounded run is terminal in one branch.** In branch 2 `_CF_SIG` is the
   last element, so a long run there matches and the branch *succeeds*
   immediately: no backtracking at all. In branch 1 the run is followed by the
   capped parameter walk, which cannot enter a value at a backtrack position
   (fact 3). A run's own `=` is outside both value classes, so a run can never
   contain a second `Signature=`/`sig=` start.

Per start position the work is therefore O(21 units + one run), and each run is
reachable from at most 21 starts: total O(22·N). The 21-expansion walk is what
produces the large constants in §4; it cannot produce a growth term.

## 2. Method

Buffers are generated from scratch at each size by `bench.py` (single line, no
newlines): one-character atoms repeated, so no credential-shaped literal exists
in any script or receipt. Every row is a *non-match* by construction — that is
the worst case, because the scanner must walk the whole buffer — and the match
count is printed per row to prove it. The single exception is
`az-sig-run-svtail`, kept as the matching control: the scan short-circuits on
it, so its reading is a lower bound, not a worst case. Timing is
`scan_bytes(data, patterns())` (all 11 shapes, the real entry point) plus each
of the two patterns alone.

Host: CPython 3.14.8, Linux 7.2.11-arch1-1, x64, 32 cores. Load average moved
between 8 and 86 during the session, so every figure is either best-of-N with a
calibration probe, or a **paired ratio computed inside one rep**. Calibration is
the azure regex over a fixed 1.45 MiB buffer: constant work, so its time tracks
host speed. Quiet baseline **0.0230–0.0273 s**; loaded 0.0495 s. The growth numbers come
from runs at calibration ≤0.0273; the paired ratios are load-normalised by
construction, and the run taken at 0.0495 reproduced the same 1.99–2.04.

Growth is reported two ways:

* `exp` — least-squares slope of log₁₀(sec) on log₁₀(size) over
  10 KB/100 KB/1 MB/4 MB (the r88 method, comparable to r88's table).
* `paired ratio` — sec(2n)/sec(n) measured inside the same rep, 9 reps, median
  reported. Linear = 2.000, quadratic = 4.000. This is the statistic that
  survives a loaded host, and it is the decisive one.

## 3. Growth — the classes named in the brief, plus controls

Full 81-row matrix with calibration and per-pattern columns:
`SentinelRegex-receipts/timing-matrix.txt` (quiet, calibration 0.0255).
Seconds, full 11-shape `scan_bytes` unless the column says otherwise.

| case | what it is | 10 KB | 100 KB | 1 MB | 4 MB | exp |
|---|---|---|---|---|---|---|
| `cf-sig-many` | repeated `Signature=`+64 url-safe, **no Key-Pair-Id** | 0.0032 | 0.0345 | 0.3640 | 1.4082 | 1.011 |
| `cf-many-long` | repeated `Signature=`+1024 url-safe, no KPI | 0.0014 | 0.0361 | 0.3485 | 1.7086 | 1.150\* |
| `cf-sig-run` | one 4 MB url-safe run after `Signature=`, no KPI | 0.0007 | 0.0074 | 0.0759 | 0.3064 | 1.001 |
| `cf-kpi-first-nosig` | **Key-Pair-Id-first, no Signature** | 0.0008 | 0.0074 | 0.0740 | 0.2943 | 0.991 |
| `cf-kpi-chain` | KPI then long `&aa=` **parameter chains** | 0.0007 | 0.0064 | 0.0625 | 0.2508 | 0.986 |
| `cf-u0026` | **many `\u0026` separators**, invalid KPI | 0.0007 | 0.0068 | 0.0698 | 0.2546 | 0.979 |
| `cf-pct26` | many `%26` separators | 0.0008 | 0.0073 | 0.0731 | 0.2864 | 0.972 |
| `cf-amp-chain` | `&amp;` soup | 0.0009 | 0.0089 | 0.0733 | 0.2875 | 0.957 |
| `az-u0026` | `\u0026`-dense `sv=` (the F1 shape) | 0.0031 | 0.0309 | 0.3016 | 1.2314 | 0.995 |
| `az-sv-dense` | `&`-dense `sv=` (r88's dominant shape) | 0.0037 | 0.0381 | 0.4108 | 1.5088 | 1.003 |
| `az-u0026-sig39` | `\u0026` chain, 39-char `sig=` (window pressure) | 0.0023 | 0.0227 | 0.2273 | 0.9626 | 1.000 |
| `az-sig-run` | one 4 MB `sig=` run, no `sv=` | 0.0009 | 0.0090 | 0.0916 | 0.3749 | 1.003 |
| `plain` | prose control | 0.0007 | 0.0070 | 0.0714 | 0.2956 | 1.007 |

\* `cf-many-long`'s 1.150 is a **small-size regime effect, not growth**: the
21-expansion walk needs 21 units to reach full depth, and a 9 KB buffer holds 9.
Per-byte cost is flat across the whole measured range — 271 ns/B at 100 KB,
304 ns/B at 1 MB, 304 ns/B at 4 MB — and the paired 1→8 MiB ratios are
1.997/1.983/2.003 (§4). The same artifact explains `cf-sig-tail` (1.065) and
`cf-sig-keysoup` (1.072), both of which carry a fixed 1000/2000-entry prefix.
All 81 rows lie in 0.924–1.194; the only rows above 1.05 are the three cases
named above, and every one of them is flat per byte from 100 KB upward. The
next highest is `cf-sig-many`'s azure column at 1.020, on sub-millisecond
values.

## 4. Growth — paired doubling ratios (the decisive statistic)

9 reps per size, ratio computed inside each rep, median reported.
Linear = 2.000. Receipts: `SentinelRegex-receipts/pair-cf.txt`,
`SentinelRegex-receipts/pair-az.txt` (load 9–31 across the two runs).

| case | 1→2 MiB | 2→4 MiB | 4→8 MiB | 4 MiB min | 8 MiB min |
|---|---|---|---|---|---|
| `cf-many-long` | 1.997 | 1.983 | 2.003 | 1.2013 | 2.4346 |
| `cf-sig-many` | 2.000 | 2.012 | 2.005 | 1.0563 | 2.1176 |
| `cf-sig-run` | 2.018 | 1.973 | 2.000 | 0.1219 | 0.2424 |
| `az-u0026` | 1.998 | 2.005 | 2.038 | 0.9172 | 1.7963 |
| `az-sv-dense` | 1.996 | 2.015 | 1.990 | 1.1719 | 2.3296 |
| `az-u0026-sig39` | 2.002 | 2.001 | 1.994 | 0.7093 | 1.4158 |
| `az-sig-run` | 1.995 | 2.003 | 2.001 | 0.1915 | 0.3831 |

Every ratio sits inside 1.97–2.04 of the linear value. A quadratic term would
put 4→8 at 4.0; a 1.15-exponent term would put it at 2.22. Neither appears.
The `cf-many-long` 4→8 ratio is 2.003 — the same case whose 10 KB→4 MB exponent
reads 1.150.

**Worst-case seconds.** 4 MiB full scan, best observed: **1.52 s**
(`cf-many-long`; the sum of its eleven per-shape bests is 1.35 s, the rest is
host variance), **1.44 s** (`az-sv-dense`), **1.27 s** (`cf-sig-many`),
**1.11 s** (`az-u0026`). Single pattern, best of 9 paired reps: 1.20 s
cloudfront (`cf-many-long`), 1.17 s azure (`az-sv-dense`). 8 MiB: 2.43 s
cloudfront, 2.33 s azure. Nothing reaches 5 s at any tested size, and the
instrument's own `--rev master` sweep of the whole lane takes 1.46 s (§7).

## 5. Compared to the r88 baseline — the one real regression

Same buffers, same host, both instruments, interleaved
(`SentinelRegex-receipts/r88-vs-r89.txt`, calibration baseline 0.0230). Seconds
at 4 MiB; `x` is r89/r88.

| case | r88 azure | r89 azure | × | r88 full | r89 full | × |
|---|---|---|---|---|---|---|
| `az-u0026` | 0.0336 | 0.9436 | **28.1** | 0.1492 | 1.1124 | 7.45 |
| `az-u0026-sig39` | 0.0290 | 0.7948 | **27.5** | 0.1357 | 0.9595 | 7.07 |
| `az-u0026-longval` | 0.0257 | 0.6556 | **25.6** | 0.1290 | 0.8281 | 6.42 |
| `az-pct26` | 0.0305 | 0.0938 | 3.07 | 0.1484 | 0.2915 | 1.96 |
| `az-sv-dense` | 1.1733 | 1.2290 | 1.05 | 1.3061 | 1.4384 | 1.10 |
| `plain` | 0.0402 | 0.0895 | 2.22 | 0.1729 | 0.3111 | 1.80 |
| `cf-sig-many` | — | — | — | 0.1186 | 1.2736 | 10.74 |
| `cf-many-long` | — | — | — | 0.1197 | 1.5223 | 12.72 |

Reading:

* **`\u0026`-dense text is 25–28× more expensive than in r88.** In r88 the left
  boundary `(?<![A-Za-z0-9_])` failed instantly after `\u0026` (the preceding
  byte is `6`), so a JSON-escaped capture never entered the parameter walk. The
  r89 boundary `(?<=\\u0026)` now admits that start, and every `sv=` in a
  JSON-escaped capture pays the 21-expansion walk. The cost is the *pre-existing*
  per-start cost, not a new mechanism: `az-u0026` at 4 MiB (0.94 s) is now the
  same order as `az-sv-dense` (1.23 s), the `&`-separated shape that was already
  r88's worst, where in r88 the `\u0026` shape was 35× cheaper than the `&` one
  (0.034 vs 1.17 s). JSON-escaped captures are the normal shape of a JSON
  evidence file, so this is the number that matters for the lane.
* `az-sv-dense` — r88's dominant shape — is **unchanged** (1.05×), so the
  regression is specific to the `\u0026`/`%26` boundary, not to the pattern's
  per-offset cost.
* `plain` prose pays 2.22× on the azure shape: the `_LB` group adds two
  lookbehind checks at every offset where the previous byte is alphanumeric.
  That is the floor cost of the F1 fix.
* The CloudFront ×10.7–12.7 rows are **new capability, not a regression**: r88
  has no CloudFront pattern, so its 0.119 s is the cost of the other ten shapes
  on a buffer built for a shape it cannot see.
* r88's own report recorded 2.76 s worst at 4 MiB on a host with calibration
  0.0140. This host's quiet calibration is 0.0230–0.0273, so the figures are not
  directly comparable; on *identical* buffers the r88 instrument's worst 4 MiB
  full scan here is 1.31 s and the r89 instrument's is 1.52 s — **1.16×** — and
  both are linear.

Per-shape attribution at 4 MiB (`SentinelRegex-receipts/per-pattern-4mb.txt`):
the changed pattern owns 83% of the `az-u0026` total (azure 0.908 of 1.092 s)
and 88% of the `cf-sig-many` total (cloudfront 1.130 of 1.290 s). On plain text
the two cost 0.077 s each — the per-offset floor, 2.2× the next shape
(`credential`, 0.036 s).

## 6. HIT lines never print matched bytes

**Static.** The frozen instrument has eight `print` sites (lines 217, 219, 288,
300, 313, 314, 336, 338); the r89 C2 diff adds none
(`SentinelRegex-receipts/static-print-sites.txt`). The two production sites
print `shape`, `path`, `line` and integer counters. `m.group(0)` appears three
times: an equality test against `ALLOWED_VALUES` (165), a `sha256` (167), and a
selftest hash (303). The instrument opens files read-only — two `open()` calls,
no write mode (`SentinelRegex-receipts/io-sites.txt`) — so every "receipt" is a
stdout redirect and inherits the property.

**Dynamic.** A planted tree of four capture-class files carrying a CloudFront
signed URL (both orders, `&` and `\u0026`), an Azure SAS with `\u0026`, and an
STS session token was scanned in `--files` mode: five HIT lines, zero
occurrences of any of six fixture markers in the output, and of the five 40+
url-safe runs in that output **all five are substrings of the printed paths**
(`SentinelRegex-receipts/leak-and-rev.txt`). The same fixture committed to a
scratch git repo and scanned with `--rev HEAD` gives four HIT lines, same
result. The lane's own `--rev master` output is 1530 scanned blobs, `hits=0`,
`allowed=20` — counts only.

Residual, unchanged from r88 D4: `report()` prints `path=%s` verbatim, so a
capture *file name* carrying a credential-shaped string would be reprinted. No
lane path does this today, and the L1 scans every wave file with this instrument
before committing it.

## 7. `--rev master` over the lane

Five runs, calibration before each (`SentinelRegex-receipts/rev-master.txt`):

```
RUN 1 cal=0.0273 wall=1.67s rss=25792KB   RUN 4 cal=0.0263 wall=1.46s rss=24524KB
RUN 2 cal=0.0273 wall=1.61s rss=24568KB   RUN 5 cal=0.0258 wall=1.51s rss=25032KB
RUN 3 cal=0.0253 wall=1.52s rss=24996KB
CAPTURE-SECRET-SCAN mode=rev:master scanned=1530 hits=0 files=0 allowed=20 unused_allow=0 rc=0
```

1530 capture-class blobs, 18.3 MB, largest 1.83 MB. Wall 1.46–1.67 s
(≈12 MB/s), peak RSS ≈25 MB. The sweep finishes with timings and needs no
special handling.

## 8. Routed qualifiers (round 90, not re-scoring)

**R89-Q1 — `\u0026`-dense captures are 25–28× more expensive than in r88
(performance, severity medium).** §5. Linear, but the constant is now the same
as `&`-separated text, and JSON evidence files are `\u0026`-dense by
construction. 4 MiB worst 0.94 s azure / 1.11 s full scan; the lane's actual
corpus is 18.3 MB total and the whole sweep is 1.5 s, so exposure today is
small. Re-runnable: `SentinelRegex-receipts/r88-vs-r89.txt`, row `az-u0026`.

**R89-Q2 — the 21-expansion window gives 21–60× amplification on
`Signature=`+run-dense text (performance, severity low).** `cf-many-long` costs
1.20 s for a 4 MiB buffer of 1 KB url-safe runs; `cf-sig-many` 1.06 s. The
amplification is bounded by the `{0,20}` cap and is linear, but a 4 MiB
CloudFront-heavy capture costs ~10× what the same bytes cost through the other
ten shapes (1.27 s vs 0.12 s).
If the cap is ever raised (r88 D2 asks for exactly that, to 64), this constant
triples. Re-runnable: `SentinelRegex-receipts/pair-cf.txt`.

**R89-Q3 — `%26` is a left boundary but not an inter-parameter separator
(coverage, severity low).** `_LB`/`_CF_LB` admit a match start after `%26`, but
`_SEP` does not contain `%26`, so a fully `%26`-joined query is still not
detected:

```
?sp=rw%26sv=2022-11-02&sig=<40>      -> azure HIT      (starts after %26, & between)
?sp=rw%26sv=2022-11-02%26sig=<40>    -> no match        (%26 between)
?x=1%26Signature=<40>&Key-Pair-Id=.. -> cloudfront HIT
?x=1%26Signature=<40>%26Key-Pair-Id=.-> no match
```

This is inside the documented "a whole URL percent-encoded inside another URL's
query" limit, but the left-boundary alternative reads as if `%26` were a
separator. Name the asymmetry in "Known limits" or add `%26` to `_SEP` (that
would be a coverage change, so it is a round-90 decision, not this seat's).

**R89-Q4 — HIT lines echo the path verbatim (residual, informational).** r88 D4,
unchanged; §6.

**R89-Q5 — refuted: the allowlist does not make `scan_bytes` quadratic.** I
suspected the two new CloudFront allowlist rows made a repeated doc-example
value quadratic, because `scan_bytes` calls `data.count(b"\n", 0, m.start())`
per match. Measured with the real S128 line-13 match (209 bytes, sha256
`f8d573cb…`, equal to the frozen row's third cell) repeated 48→19 972 times:
0.0004 / 0.0047 / 0.0487 / 0.1905 s, exponent **1.005**; with the allowlist
removed, 0.0004 / 0.0045 / 0.0451 / 0.1768 s, exponent 1.006. The reason is in
the code: `data.count` sits in the *non-allowed* branch, which `break`s the
`finditer` loop — an allowlisted match `continue`s without counting. No defect.
Receipt: `SentinelRegex-receipts/allowlist-repeat.txt`.

Confirmed **not** defects: the `{40,}` runs are single-parse (right boundary
unique, §1); `Key-Pair-Id=` followed by a >32-char upper-case run costs 25
lookahead steps and fails (`cf-kpi-longrun` 0.074 s at 4 MiB); `%26`/`&amp;`
soup is cheap (`cf-pct26` 0.098 s, `cf-amp-chain` 0.102 s); a 4 MB
`X-Amz-Signature=` run never starts a CloudFront match; the `(?<=%26)` /
`(?<=\u0026)` lookbehinds are fixed-width.

## 9. Files written

- `.ufo/waves/round-89/w1/SentinelRegex.md` (this report)
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/pins.txt`
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/timing-matrix.txt`
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/pair-cf.txt`
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/pair-az.txt`
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/r88-vs-r89.txt`
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/per-pattern-4mb.txt`
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/allowlist-repeat.txt`
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/leak-and-rev.txt`
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/rev-master.txt`
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/static-print-sites.txt`
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/io-sites.txt`
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/bench.py` (generators + matrix)
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/compare.py` (r88 vs r89)
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/recheck3.py` (paired ratios)
- `.ufo/waves/round-89/w1/SentinelRegex-receipts/allowrep.py` (Q5 probe)

Fixtures, the planted repo, the scratch copy of both instruments and the
selftest-fake capture bytes lived only in
`/fast/scratch/hyaku/kasegi-r89/SentinelRegex/`, which is deleted before this
seat yields. No receipt contains a matched value: they carry digests, timings,
counts and `HIT shape/path/line` lines. The generators build every value by
repeating one-character atoms, so no 40+ character url-safe literal exists in
any file above.

## 10. Reproduce

```sh
S=$(mktemp -d /fast/scratch/hyaku/kasegi-r89/repro.XXXXXX); cd "$S"
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
mkdir inst
git -C $L show c61c55868e6d28653f57413bac6a6de5a398d11f:corpus/instruments/capture-secret-scan.py > inst/capture-secret-scan.py
git -C $L show c61c55868e6d28653f57413bac6a6de5a398d11f:corpus/instruments/claim-package-check.py > inst/claim-package-check.py
git -C $L show c61c55868e6d28653f57413bac6a6de5a398d11f:corpus/instruments/capture-secret-allow.tsv  > inst/capture-secret-allow.tsv
git -C $L show b43dc2154bc09470da2209fb626021da3af3593e:corpus/instruments/capture-secret-scan.py > inst88.py
sha256sum inst/capture-secret-scan.py inst88.py   # 95f24a54…  d7349536…
cp $L/.ufo/waves/round-89/w1/SentinelRegex-receipts/{bench,compare,recheck3,allowrep}.py .
python3 -B bench.py --inst ./inst --sizes 10240,102400,1048576,4194304 | grep ^ROW
python3 -B recheck3.py --inst ./inst --cases cf-many-long,cf-sig-many --mode cf --reps 9
python3 -B compare.py --r88 ./inst88.py --r89 ./inst --sizes 1048576,4194304 --reps 2
```
