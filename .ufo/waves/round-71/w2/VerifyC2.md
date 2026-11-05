# VerifyC2 — kasegi round-71 attempt 2, wave 1 — C2 re-measure at tip 3cc8cd4

Seat: reviewer, leaf. Only a read-only clone touched this round; no lane file was modified.
Scratch: /fast/scratch/hyaku/kasegi-r71/VerifyC2 (clone + counter run), deleted before yield,
receipts copied here first. Environment: Python 3.14.8, GNU coreutils 9.12, git 2.56.0
(as printed by the converted counter's HOST line; tooling authorization used: none — no
package was installed or upgraded).

## Verdict

C2: VERIFIED

Every frozen after-value reproduces from my own plain counts on a clone at tip
`3cc8cd45cb6f8ca49a292f3b2647c5bddac71486` (clean, 0 changed files; clone HEAD printed
= tip). No value differs, zero drift. The judge note is resolved: attempt-1's ReviewC2
reported NOT VERIFIED at `4e33119` because the registry row landed in `34faab9`; the tip
`3cc8cd4` already contains both, so the artifacts are now on the ground at the fork point.

## Count table (one output line per command)

| # | command (all on the tip clone) | observed output |
|---|---|---|
| 1 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `106` |
| 2 | `ls corpus/knowledge/*.md \| wc -l` | `87` |
| 3 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `49` |
| 4 | `wc -l < corpus/instruments/knowledge-expected.txt` | `89` |
| 5 | `grep -vc '^#' corpus/instruments/knowledge-expected.txt` | `87` |
| 6 | `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt` | exit 0 |
| 7 | python: summed `sources[]` over `corpus/source-snapshots/**/manifest.json` | `manifests=44 total sources=85` |
| 8 | `python3 corpus/instruments/capture-binding-check.py` | ends `records=85 bound=85 unbound=0` exit 0 |
| 9 | `python3 corpus/instruments/frontier-recheck-count.py` | `FRONTIER-CENSUS rows=49 admitted=49 closed=49 problem-rows=0 registry=106` then `entries=52 pass=52 exit=0` |
| 10 | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md exit=0` (six inherited W04 duplicate-URL warnings: S028 S029 S072 S076 S080 S085, unchanged from frozen before/after theory) |
| 11 | LAST LINE: census `python3 -B .ufo/waves/round-71/controls/c1-probe-run-r71.py --gate <exported candidate> --work ... --mode candidate` | `VERIFY measurements=25 failures=0 gate_sha256=182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603 mode=candidate`, exit 0 (25 MEASURE rows, all `ok`; N8 `marker_runs=0 wrote=0`, N9 refused, N12 refused) |

Frozen sha cross-checks on the tip clone: `corpus/instruments/figure-audit.py` →
`182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603` (candidate gate is the
bytes the claims SHA names), `corpus/source-snapshots/round-71/S106.txt` →
`291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db`, 148 lines,
15004 bytes (both match pins-r71.txt / claims.json).

## Claim-artifact audit (all four named artifacts)

**S106 registry row — 11 cells, tier A, status mined, opened 2026-11-05, used-by resolves.**
Row at `corpus/SOURCES.md:118`. Cells split: 11 (pipe-norm), all 106 rows also 11 cells (no
shape outlier). Tier cell `A`, status cell `mined`, opened cell `2026-11-05`. `used-by` cell =
`corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md`, which exists on the tip
clone.

**F49 present in corpus/README.md naming both S106 and the entry path.**
`corpus/README.md:1114` frontier row `| F49 | TrendAI ZDI's own disclosure process and vendor
coordination — ... | admitted | knowledge/zdi-disclosure-process-and-vendor-coordination.md | S106 | ...`,
with the same ZDI claims text (120-day standard window, 30/60/90-day shortening, 15-business-day
escalation, full-vs-limited advisory choice, validation → formal monetary offer → payment →
vendor coordination, credit or anonymity). frontier-recheck-count.py emits
`FRONTIER-PASS F49 knowledge/zdi-disclosure-process-and-vendor-coordination.md ids=S106 exit=0`.

**Entry file cites S106 and every anchor resolves.**
`corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md` (256 lines) header cites
`source: S106 — https://www.zerodayinitiative.com/about/ ... round-71/S106.txt sha256 ...
fetched 2026-11-05T01:27:03Z`. 12 distinct `S106.txt:<line>` anchors referenced: 28 31 47 49 51
52 60 61 62 69 70 72 — all within 1..148, all resolve to non-empty capture lines when read back
by sed.

**Manifest integrity (my conversion of the claims SHA into the manifest).**
`corpus/source-snapshots/round-71/manifest.json`: single source S106, 15 quotes Q01-Q15, anchor
integrity — all 15 quote texts match verbatim at their anchored line in the capture (15/15
exact-substring OK; longest quote = 25 words, none above 25; anchors L28 L31 L47 L49 L70 L70 L70
L52 L51 L60 L62 L61 L69 L72 L60 — three legit distinct quotes share L70, two share L60).

## Note for the record — attempt-1 fork point vs tip

`34faab9` ("late seat output, ScribeRegistry registry-changes bullet") adds exactly 1 line to
`corpus/SOURCES.md` plus its own w1 report file. That line is the full round-71 S106
admission bullet; the Registry table namecount at tip already includes it. Despite the commit
message, the diff is substantive (registry append, not prose alone) and is what carries the
S106 row onto the tip. `knowledge-expected.txt` is byte-identical between `34faab9` and tip
(diff empty). So ReviewC1's NOT VERIFIED at `4e33119` was correct for that commit and stale for
the tip; my re-measure closes it.

## Residual risk / verification gaps

- attempt-1's frozen do-nothing-gate control blob (sha256
  `7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5`) was not re-run by me —
  that blob is not reachable as a git object in this clone and the frozen counter in donothing
  mode points at round-70 gate bytes; this is VerifyC2's charge only as C2 regression, not C1's
  do-nothing limb (VerifyC1 owns that limb). Candidate-run limb re-run and matching here stands
  as the sole census evidence.
- `grep -c 'S106'` on the entry = 85 (header plus repeated anchor refs); the count alone is not
  an audit — the per-anchor resolution above is the actual check.
- sources-census.sh W04 duplicate-URL warnings are inherited, not new; they are identical ids
  and URLs as in the frozen before_receipt and do not block validate exit 0.
