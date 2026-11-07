# SentinelRegex — round 88 attack seat

**Subject:** `corpus/instruments/capture-secret-scan.py` at the C2 landing
`b43dc2154bc09470da2209fb626021da3af3593e`, instrument sha256
`d73495364f90f78fa5ee6ad28b83fce772a349a5339d240b21db4d5d04425417`
(byte-equal to `.ufo/waves/round-88/c2/candidate/capture-secret-scan.py` and to the
working-tree file; verified with `git show` + `sha256sum`, not from the claim).

**Hypothesis (falsifiable).** The r88 additions — `azure-sas-signature`'s lazy
`{0,20}` parameter window inside an alternation, and `gcs-signed-url-signature` —
show super-linear time on adversarial input.
**Verdict: REFUTED.** No input class grows super-linearly; no input class
reproducibly exceeds 5 s at 4 MiB. Both observations above 5 s in the first pass
are shown below to be host-load artifacts of a 5× oversubscribed machine
(load average 162 on 32 cores), not algorithmic growth.

Scoring impact: none. No frozen predicate of C1 or C2 reads performance; K1–K6
are untouched by this seat. Everything below is a routed defect / qualifier for
round 89.

---

## 1. What the patterns actually are

```python
_SEP   = rb"(?:&amp;|&|\\u0026)"
_PARAM = rb"(?:" + _SEP + rb"[A-Za-z]{2,6}=[^&\s\"'<>\\]*){0,20}?"
_SIG   = rb"sig=[A-Za-z0-9%+/]{40,}(?:=|%3D){0,2}"
_SV    = rb"sv=\d{4}-\d{2}-\d{2}"

("azure-sas-signature", re.compile(
    rb"(?i)(?<![A-Za-z0-9_])(?:" + _SV + _PARAM + _SEP + _SIG
    + rb"|" + _SIG + _PARAM + _SEP + _SV + rb")"))
("gcs-signed-url-signature", re.compile(
    rb"(?i)X-Goog-Signature(?:=|\\?[\"']?\s*:\s*\\?[\"']?)[0-9a-f]{64,}"))
```

Three structural facts bound the work, and they are why the hypothesis fails:

1. **The `{0,20}` window is a work cap, not only a coverage cap.** At a start
   position the engine performs at most 21 `_PARAM` expansions, then gives up. So
   per start position the work is O(21 + ℓ) where ℓ is the length of the single
   value run the chain reaches. Only ≤20 starts can reach any given value run
   (step 20 is the last expansion), so the total is O(N).
2. **The value class cannot be partitioned ambiguously.** `[^&\s\"'<>\\]*`
   excludes every character that can begin `_SEP` (`&`, `\`), so a value's right
   boundary is unique and the quantified repetition has exactly one parse. There
   is no `2^k` path count: this is not a nested-quantifier blowup.
3. **The gcs trailing class is terminal.** `[0-9a-f]{64,}` is the last element of
   that pattern, so a long hex run is matched once and never backtracked. The
   only unbounded quantifier before it (`\s*`) can be walked at most once per
   occurrence of the literal.

What *is* expensive is that the azure alternation has **no literal prefix** (a
lookbehind followed by a two-way literal branch defeats CPython's prefix scan),
so the engine attempts a match at *every byte offset* instead of skipping to a
literal. The evidence is `many-params`: 1 MiB of text with no `sv=`, no `sig=`
and almost no `s` bytes costs 0.11 s, i.e. ~110 ns/byte — three orders of
magnitude above a memchr pass over the same buffer, and the same order as a
per-position regex attempt. On `sv=`-dense text that per-offset attempt is what
dominates: 1.2–2.4 s per 4 MiB against ~0.03 s for every other shape (30–80×);
on text with no `sv=` it is 0.05 s, comparable to the others. Routed defect D1.

## 2. Method

Byte strings are generated from scratch per case at 10 KiB / 100 KiB / 1 MiB /
4 MiB (`bench.py`), then `css.scan_bytes(data, css.patterns())` — the real
instrument entry point with all ten shapes — is timed, plus the azure and gcs
regexes alone. Every figure is **best-of-3** with a fixed 1.45 MiB calibration
probe timed immediately before the row; a row is retried if calibration exceeds
3× the startup baseline (`bench2.py`). Growth exponent = least-squares slope of
log₁₀(time) on log₁₀(size) over the four sizes; 1.0 = linear, 2.0 = quadratic.

Runtime: CPython 3.14.8, Linux 7.2.11-arch1-1, x64, 32 cores. Quiet-host
calibration baseline 0.0140 s (0.0124–0.0158 s across rows).

## 3. Timing table — full `scan_bytes`, seconds

The four classes named in the brief are rows 1–4.

| case | 10 KB | 100 KB | 1 MB | 4 MB | exp(full) | exp(azure) |
|---|---|---|---|---|---|---|
| `many-params` (long `&`-separated short params) | 0.0008 | 0.0062 | 0.0758 | 0.2866 | 0.995 | 1.082 |
| `sv-no-sig` (long runs of `sv=…&` with no sig) | 0.0058 | 0.0616 | 0.6430 | 2.7583 | 1.023 | 1.038 |
| `gcs-hex` (4 MB hex run after the parameter name) | 0.0006 | 0.0064 | 0.0766 | 0.2671 | 1.013 | 0.993 |
| `sig39` (many short `sig=` values) | 0.0007 | 0.0054 | 0.0679 | 0.2849 | 1.002 | 1.028 |
| `gcs-hex-upper` | 0.0006 | 0.0061 | 0.0644 | 0.2361 | 0.986 | 0.984 |
| `gcs-near-miss` (63 hex then a non-hex, repeated) | 0.0007 | 0.0065 | 0.0711 | 0.3007 | 1.003 | 1.021 |
| `gcs-spaces` (name + 4 MB of spaces, no colon) | 0.0004 | 0.0050 | 0.0610 | 0.9498* | 1.236* | 1.259* |
| `sig-nosep` | 0.0005 | 0.0111 | 0.0781 | 0.2520 | 1.005 | 1.040 |
| `amp-entities` (`&amp;` soup) | 0.0007 | 0.0069 | 0.0729 | 0.2899 | 1.007 | 1.008 |
| `u0026-blocks` | 0.0008 | 0.0090 | 0.0757 | 0.2972 | 0.984 | 1.019 |
| `realistic-sas` (SAS prefix repeated, no sig) | 0.0034 | 0.0306 | 0.3755 | 1.4772 | 1.015 | 1.026 |
| `sig-giant` (one 4 MB in-class run after `sig=`) | 0.0011 | 0.0115 | 0.1296 | 0.5397 | 1.037 | 1.011 |
| `sv-giant-value` (one 4 MB value cut by a space) | 0.0009 | 0.0086 | 0.0941 | 0.3548 | 0.996 | 1.010 |
| `sv-sig39` (full window pressure, short sig) | 0.0037 | 0.0458 | 0.5011 | 1.9918 | 1.046 | 1.028 |
| `sig40-svbad` (full window, wrong-order/date miss) | 0.0041 | 0.0362 | 0.3909 | 5.3968* | 1.154* | 1.021 |
| `amp-soup` | 0.0005 | 0.0090 | 0.0917 | 0.3032 | 1.073 | 1.041 |
| `u0026-chain` | 0.0008 | 0.0063 | 0.0720 | 0.3125 | 0.998 | 0.992 |
| `sv-longtail` (k starts + one shared long cut run) | 0.0071 | 0.0526 | 0.6178 | 2.4798 | 0.982 | 0.997 |
| `sv-longtail-quote` | 0.0060 | 0.0604 | 0.6588 | 2.6423 | 1.014 | 1.049 |

`*` = row measured during a load excursion; retracted in §4. Raw table with the
calibration and per-regex columns: `SentinelRegex-receipts/timing-matrix.tsv`.

**Every exponent is 0.98–1.07 except the two retracted rows** (`gcs-spaces`
1.24 and `sig40-svbad` 1.15, both load artifacts, §4). The three shapes
built specifically to break it (`sv-longtail`, `sv-longtail-quote`, `sig-giant`:
k candidate start positions before one shared long run that ends where no
separator can match, i.e. the classic shape that makes a greedy value backtrack
once per start) come out at 0.98/1.01/1.04, because the `{0,20}` cap means at
most 20 starts ever reach that run.

No input class exceeds 5 s at 4 MiB except the two starred rows, which do not
reproduce (§4). Worst reproducible: `sv-no-sig` 2.76 s, `sv-longtail-quote`
2.64 s, `sv-longtail` 2.48 s, `sv-sig39` 1.99 s.

## 4. The two >5 s readings, and why they are not the pattern

First pass (uncalibrated, host load average 162/32 cores) gave 13.05 s for
`sv-sig39` and 8.94 s for its azure limb at 4 MiB. Repeats minutes later gave
1.75–1.91 s. The matrix then flagged two rows, and a dedicated 5-run re-check
with a calibration probe before every scan (`SentinelRegex-receipts/outlier-recheck.txt`)
settles it:

| run | cal (s) | `sig40-svbad` full (s) | `gcs-spaces` full (s) |
|---|---|---|---|
| 1 | 0.0404 | 4.597 | 0.522 |
| 2 | 0.0552 | 3.572 | 0.478 |
| 3 | 0.0145 | 1.551 | 0.538 |
| 4 | 0.0143 | 1.517 | 0.272 |
| 5 | 0.0124 | 1.932 | 0.269 |

Wall time tracks the calibration probe, not the input: 0.055 s-of-cal → 3.6 s,
0.0124 s-of-cal → 1.9 s, same bytes, same process. Coincident with contention,
not a backtracking cliff. Per-pattern attribution on the same 4 MiB also rules
out interaction between patterns: the sum over all ten shapes is 1.38 s for
`sig40-svbad` (`SentinelRegex-receipts/per-pattern-4mb.txt`), so the 5.40 s row
cannot be the patterns' work.

**Consequence for the verdict:** the ">5 s at 4 MB" clause is not met by any
class under load-normalised measurement. On a loaded host the instrument can
take 5–13 s on a 4 MiB capture, but that is the host, and the growth is linear
in every case.

## 5. Routed defects and qualifiers (round 89, not re-scoring)

**D1 — the azure alternation is the instrument's dominant cost (performance
qualifier, severity low).** It is the only pattern with no literal prefix, so it
attempts a match at every byte offset. On 4 MiB it costs 1.2–2.4 s when `sv=`
occurs densely and 0.05 s when it does not; every other shape is ~0.03 s
(`SentinelRegex-receipts/per-pattern-4mb.txt`). Real exposure at the landing
(`SentinelRegex-receipts/exposure.txt`): 1414 capture-class blobs, 17.7 MB
total, largest 1.83 MB → worst-case single-file ≈ 1.1 s quiet, and a full
`--rev` sweep pays it across the tree.

Two candidates were built and measured (`SentinelRegex-receipts/remediation-try.txt`,
1 MiB, best of 5, both verified to return the identical match-start set as the
landed pattern on every adversarial buffer):

| shape | as landed | A: literal prefilter | B: atomic value `(?>[^…]*)` |
|---|---|---|---|
| no `sv=`/`sig=` at all (`many-params`) | 0.110 | **166×** faster | 1.0× |
| no candidate (`gcs-near-miss`) | 0.086 | **108×** faster | 1.0× |
| `&amp;` soup (`amp-soup`) | 0.099 | **152×** faster | 1.7× |
| `sv=` dense, no sig (`sv-no-sig`) | 0.740 | **0.2× (5× slower)** | 1.3× |
| `realistic-sas` | 1.69 | 1.4× | **4.6×** |
| `sv-sig39` | 1.16 | 2.2× | 1.2× |
| `sig-giant` | 0.289 | 3.7× | **2.5×** |

(Taken on the loaded host — calibration 0.08–0.12 s against a 0.014 s quiet
baseline — so the multipliers are indicative ratios; the ratios, not the
seconds, are the point.)

Reading: **A is two orders of magnitude faster exactly where it matters** —
captures that contain no candidate literal, which is almost every capture — and
it *backfires* when `sv=` is dense, because a Python-level loop per candidate
costs more than the offset probes it saves. A prefilter must therefore be gated
(e.g. use it only when the candidate count is below N/64) or it trades one cost
for a worse one. **B is a 1–5× win at 1 MiB and never loses there**, but the
4 MiB spot checks (in the receipt, 3–4× the load, no per-row calibration) do not
confirm it — one reads 0.7× — so B's multiplier is a 1 MiB result only. Neither
variant changes any verdict, and neither is required by any frozen predicate:
this is a round-89 item.

**D2 — the ≥21-parameter window is a silent false negative and is not in the
documented limits (severity medium).** `sv=…` followed by 21 intervening
parameters and then `sig=…` is not detected; 20 is
(`SentinelRegex-receipts/sensitivity.txt`). The docstring's "Known limits"
paragraph names GCS V2, CloudFront, percent-encoded parameter names and wrapped
captures — not this window. Re-runnable:
`python3 -B -c 'import importlib.util as u; s=u.spec_from_file_location("c","corpus/instruments/capture-secret-scan.py"); m=u.module_from_spec(s); s.loader.exec_module(m); rx=dict(m.CLOUD_PATTERNS)["azure-sas-signature"]; print(bool(rx.search(b"sv=2022-11-02" + b"&ab=1"*21 + b"&sig=" + b"Z"*40)))'`
prints `False`; with `*20` it prints `True`. Note D1 and D2 pull in opposite
directions only in appearance: total work is O(window × N), so widening the
window to 64 costs ≈3× the current constant and stays linear — the cap is not
holding up the linearity, the per-offset attempt is.

**D3 — the 2–6 letter parameter-name class breaks the chain (severity low).**
A single-letter parameter between `sv=` and `sig=` (e.g. `sv=…&s=b&sig=…`) is not
detected, and neither is a 7-letter one
(`SentinelRegex-receipts/sensitivity.txt`). Azure's own SAS parameter names are
2–5 letters, so this is a limit rather than a current miss; it should be named
in "Known limits" with D2.

**D4 — HIT lines echo the path verbatim (residual, severity informational).**
`report()` prints `path=%s`, so a credential-shaped *file name* inside a capture
path would be reprinted into stdout and any receipt redirected from it. No
matched *value* can be printed — see §6 — but a future capture named after a
token would leak through the path. No lane path does this today.

Confirmed **not** defects: percent-escaped parameter names and GCS V2 are already
named limits; `&amp;`, `\u0026`, either parameter order, upper-case parameter
names, empty-value parameters and a `%3D` suffix all detect correctly.

## 6. Output hygiene — the r88 shapes never print matched bytes

Static: the instrument has eight `print` sites (lines 190, 192, 250, 262, 275,
276, 298, 300 of the landed file). The two production sites print
`shape`, `path`, `line` and integer counters; the error sites print
`type(e).__name__` only. `m.group(0)` is used just for an equality test against
`ALLOWED_VALUES` (line 138), for `sha256` (line 140) and, in the selftest, to
hash a fixture (line 265). The instrument opens files read-only
(`open(path)`, `open(p, "rb")`) and writes nothing to disk, so every "receipt" is
a stdout redirect and inherits this property.

Dynamic: a planted 380-byte capture carrying a session-token value, a 72-hex GCS
signature and an Azure SAS sig was scanned in `--rev` and `--files` mode
(`SentinelRegex-receipts/leak-check.txt`). All four shapes hit; the output is
four `HIT shape=… path=… line=…` lines plus one summary line. Grepping that
output for every fixture marker (the token stem, the SAS stem, two interior
digest fragments) returns 0 for each; grepping for any run of 40+ base64/hex
characters returns exactly one thing, the scratch *path* fragment
`r88/SentinelRegex/leak/repo/corpus/source` — no fixture value, and the same
class of exposure as D4. The lane's own receipts match: the C2 landing
receipt carries `LIMB K4 … files_hits=1` and `LIMB K3 … scanned=1414,hits=0,…`
— counts, never values — and `capability-check.py` parses HIT lines with
`^HIT shape=(\S+) path=(\S+) line=\d+$` into `(path, shape)` sets only.

## 7. Scope note

This seat probed the landed scanner's r88 regexes only. No C1 (sibling-entry
repoint) finding is claimed here; C1's counter/verifier seats own that surface,
and nothing in this report touches the knowledge meter, the repair map or the
landing scope.

## 8. Files written

- `.ufo/waves/round-88/w1/SentinelRegex.md` (this report)
- `.ufo/waves/round-88/w1/SentinelRegex-receipts/timing-matrix.tsv`
- `.ufo/waves/round-88/w1/SentinelRegex-receipts/outlier-recheck.txt`
- `.ufo/waves/round-88/w1/SentinelRegex-receipts/per-pattern-4mb.txt`
- `.ufo/waves/round-88/w1/SentinelRegex-receipts/exposure.txt`
- `.ufo/waves/round-88/w1/SentinelRegex-receipts/sensitivity.txt`
- `.ufo/waves/round-88/w1/SentinelRegex-receipts/leak-check.txt`
- `.ufo/waves/round-88/w1/SentinelRegex-receipts/bench.py`
- `.ufo/waves/round-88/w1/SentinelRegex-receipts/bench2.py`
- `.ufo/waves/round-88/w1/SentinelRegex-receipts/remeasure.py`
- `.ufo/waves/round-88/w1/SentinelRegex-receipts/remediation-try.txt`

Fixtures, planted repositories and the scratch copy of the instrument live only
in `/fast/scratch/hyaku/kasegi-r88/SentinelRegex/` (deleted before this seat
yielded); receipts carry digests, timings, counts and `HIT shape/path/line`
lines only.

## 9. Reproduce

```sh
S=$(mktemp -d /fast/scratch/hyaku/kasegi-r88/repro.XXXXXX); cd "$S"
mkdir inst
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show \
  b43dc2154bc09470da2209fb626021da3af3593e:corpus/instruments/capture-secret-scan.py > inst/capture-secret-scan.py
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show \
  b43dc2154bc09470da2209fb626021da3af3593e:corpus/instruments/claim-package-check.py > inst/claim-package-check.py
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show \
  b43dc2154bc09470da2209fb626021da3af3593e:corpus/instruments/capture-secret-allow.tsv > inst/capture-secret-allow.tsv
sha256sum inst/capture-secret-scan.py   # d7349536…
cp /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-88/w1/SentinelRegex-receipts/bench.py  .
cp /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-88/w1/SentinelRegex-receipts/bench2.py .
python3 -B bench2.py --reps 3 | tee matrix.tsv
```
