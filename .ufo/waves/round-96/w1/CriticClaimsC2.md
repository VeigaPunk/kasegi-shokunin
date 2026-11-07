# CriticClaimsC2 — round 96, attempt 1: attack on C2's frozen predicate

Seat: leaf critic (no dispatch). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Frozen claim: C2 in `.ufo/waves/round-96/claims.json` (counter sha256 `989a443f…`,
instrument pin `71876619…`, gate pin `8b6f8493…`).
Landing `7ef1d365eb523a83b2567342a6c0f585ab028ab0`; base `d8a2bb0a…`; history `252df0c9…`.
Scratch `S=/fast/scratch/hyaku/kasegi-r96/CriticClaimsC2` (clone + fixtures, removed on exit).

## Verdict

**C2 STANDS** — K1–K6 re-derived at the landing at three seeds of my own; the seven shapes
agree with S140 on 86 differential cases; no earlier shape is lost; no shape fires on a
boundary negative. No counterexample found that fails a limb.

## Re-derived limbs (seed 424242; 777001 and 90210 identical)

| Limb | Observed at `7ef1d36` | Holds |
|---|---|---|
| K1 | `inst_sha=pin-ok gate_sha=pin-ok selftest=pass cases=128` | yes |
| K2 | `rc=0 scanned=2744 hits=0 allowed=27 unused_allow=0` | yes |
| K3 | `rc=1 hits=7 missing=none extra=none` | yes |
| K4 | `base_new_shape_hits=0 old_shapes_missing=none` | yes |
| K5 | `rows=1 last=87 named=True` | yes |
| K6 | `rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential` | yes |

`CAPABILITY-CHECK-RESULT pass rc=0` at all three seeds. The lane advanced to the round-96
integration commit `b7f59c6` while this seat ran; a fourth run there (seed 31337) also passes
every limb (`scanned=2746 hits=0 allowed=27 unused_allow=0`; the instrument, the gate and the
SCORECARD row are byte-identical to the landing), so the verdict holds at lane HEAD too. The landing commit touches exactly
two files (`SCORECARD.md`, `corpus/instruments/capture-secret-scan.py`; +50/−7); the
instrument at the landing is byte-identical to the frozen candidate
(`71876619…`), and the landed SCORECARD row is byte-identical to the frozen
`c2/candidate-row.txt` (`diff` rc 0).

## Independent S140 differential — 86 cases, 0 mismatches

I transcribed the seven published regexes verbatim from
`corpus/source-snapshots/round-94/S140.txt` (lines 30, 51, 73, 136, 324, 358, 375 — each
cited line is exactly the `regex = '''…'''` line, so the provenance is accurate) and
compared them to the landing instrument on the same bytes: 78 cases in `probe.py` plus 8
in `probe-extra.txt`, every one agreeing with S140.

- **27-char head floor / 300 ceiling**: 26 → miss, 27 → hit, 300 → hit, 301 → miss
  (routable and versioned, with and without a prefix).
- **Tails**: `.`+2+7 (routable) and `.`+2+`.`+2+7 (versioned) hit; 1-char middle,
  3-char middle, 6-char last segment, 8-char last segment, upper-case 2-char and 7-char
  segments all miss.
- **Right boundary**: trailing alnum and `_` miss; trailing `-`, `.`, space, tab and EOS hit —
  this is S140's `\b` semantics, not the `(?![A-Za-z0-9_-])` of the sibling round-93/94
  patterns, so the new fragments are *more* S140-faithful than their neighbours.
- **Optional custom instance prefix**: `acme-`, a 20-char prefix and a 21-char prefix all
  hit (S140's `{1,20}` can also be skipped, since `\b` holds after the hyphen); a prefix
  without the hyphen (`acmeglrtr-`) misses.
- **`glptt-`**: 19/21/39/41 miss; 20 and 40 hit; trailing `-`, `_`, alnum miss; `.`, EOS,
  prefix hit. `glptt-`+20+`-`+19 (40 total) hits and `glptt-`+20+`-`+20 (41 total) misses,
  matching the alternation.
- **No swallow of a plain 20-char family token**: `glpat-`/`gldt-`/`glrt-`(+`t1_`)/`glrtr-`
  at exactly 20 chars fire only the round-93/94 shapes; a 20-char token followed by a
  `.`-tail stays `gitlab-pat`/`gitlab-runner-auth-token`/`gitlab-deploy-token`; a 20-char
  token extended by `-`+6 chars to a 27-char head correctly becomes the routable/versioned
  shape. Routable and versioned never both fire on the same token.
- **Earlier shapes**: 12/12 old shapes fire identically on the base and landing instruments
  (`OLD-FIRE-BAD=0`); shape-name diff `lost=none added=7 NEW in base=none`.

Selftest: landing `cases=128` with 128 `ok` and 0 `FAIL`; base `cases=115` with 115 `ok`
and 0 `FAIL`; the 13 new case tuples are present and each asserts an exact shape set.
The docstring's known-limits paragraph drops the six routable/versioned families and
`glptt-`, keeps the six remaining prefixes (`glft-`, `glimt-`, `glsoat-`, `glffct-`,
`gloas-`, `glrct-`) and all non-GitLab limits, and adds five newly named limits (S140
lines 101, 160, 341, 308, 532).

## Counterexamples tested and rejected

- **`glrtr` versioned pattern omits `_GL_PREFIX`** that S140 publishes
  (`(?:[a-zA-Z0-9]{1,20}-)?glrtr?-`). Detection is unaffected: `_GL_LB` admits a preceding
  `-`, so `acme-glrtr-…` still hits (match starts at `glrtr-`). Only the match span — and
  therefore a future allowlist digest — differs from the sibling shapes. Not a false
  negative, not a K-limb failure.
- **New fragments' right boundary is laxer than the neighbouring patterns** (`-` allowed
  after the tail). This is exactly S140's `\b`; the landing instrument and S140 agree on
  every boundary case I built. Not a false positive w.r.t. the source.
- **Escape-terminator left boundary** (`\n`-escaped tokens) is a deliberate superset of
  S140's `\b`, inherited from the round-93/94 family; it does not make any K3 negative fire.
- **Allowlist**: 25 rows, none for a round-96 shape, so `allowed=27 unused_allow=0` is not
  masking a new-shape hit. The allowlist is unchanged from base (same sha256).
- **Intake gate**: `capture-source.py` imports `patterns()` from the scanner, so the seven
  shapes now apply at intake too. Its pinned instrument sha is `0630d32b…`
  (`capture-source.py` itself, unchanged), so the round-90 pin still holds; no K limb of
  either claim is disturbed.

## Routed defects / qualifiers (no verdict change)

- **Q1 — K4 is base-vs-base and cannot fail for a bad landing instrument.** With the
  round-95 instrument committed at the landing tree (fixture `c608a6ea`), K4 still prints
  `ok`. The "no earlier shape lost" intent is therefore covered only by K6 (one shape) in
  the frozen set; I closed it independently with 12 old-shape plants (all fire on the base
  *and* landing instruments) and a shape-name diff (`lost=none`).
- **Q2 — K3's six negatives do not isolate the right boundary or the 300 ceiling.** Two
  fixture mutants pass K1–K6 unchanged: dropping `(?![A-Za-z0-9_])` from `_GJ_VER`/
  `_GJ_ROUTABLE` (`d07c5d84`, rc 0) and widening `{27,300}` to `{27,}` (`f9f2d98a`, rc 0).
  Both mutants produce false positives on inputs the landing instrument rejects
  (`glpat-`+27+`.ab`+`cd12345`+`x`, `…`+`_`, and a 301-char head). The landing instrument
  itself is correct on all of them — this is control strength, not a defect in the landing.
- **Q3 — the claim's `do_nothing` text names the wrong limb.** The round-95 instrument at
  the landing tree fails **K1 (cases=115) and K3 (missing=7)**, rc 1 — not "K4 (0 of the
  seven shapes)". The outcome (fail, rc 1) is as stated; only the limb name is wrong.
- **Q4 — the docstring clause is unbound by any K limb.** K1–K6 never read the docstring;
  I verified the clause by reading both paragraphs (it holds, see above).
- **Q5 — `glrtr` span asymmetry** (see counterexamples): harmless today, but a future
  allowlist row for a prefixed `glrtr` token would be keyed on the bare-token digest.

## Impacted axes

`coverage` (score 8, held): the capability extension is real, S140-faithful and does not
regress any earlier shape. No axis moves; the qualifiers above are control-strength and
provenance notes, not coverage losses.

## Smallest safe correction

None required for this landing. For the next round's control set (not a post-landing edit,
which the kill rule forbids): add one right-boundary negative (`…cd12345` + `x`) and one
301-char-head negative to K3 and mirror them in the selftest; correct the `do_nothing`
text to K3; and, if span parity with S140 is wanted, add `_GL_PREFIX` to the `glrtr`
versioned pattern before any allowlist row is minted for it.

## Receipts

All outputs are in `.ufo/waves/round-96/w1/CriticClaimsC2-receipts/`.

| Command | Observed |
|---|---|
| `sha256sum .ufo/waves/round-96/c2/capability-check.py` | `989a443fa8bab83705bca670a0a5b396a5a5c87e33607dcb6a9679d17e84247c` = claims counter sha |
| `sha256sum .ufo/waves/round-96/c2/candidate-scanner.py`; `git show 7ef1d36:corpus/instruments/capture-secret-scan.py \| sha256sum` | both `71876619a62875049a5526a03806aa740e3ead122aacdc1499fe153be3048ac9` |
| `git show --stat 7ef1d36` | 2 files, +50/−7 (`SCORECARD.md`, the instrument) |
| `capability-check.py --lane <clone> --rev 7ef1d36 --work $S/work-<seed> --instrument-sha256 71876619… --gate-sha256 8b6f8493… --seed {424242,777001,90210}` | `CAPABILITY-CHECK-RESULT pass rc=0` ×3; limb lines as tabled (`harness-seed-*.txt`) |
| `capability-check.py --rev b7f59c6 --seed 31337` (post-integration HEAD) | `CAPABILITY-CHECK-RESULT pass rc=0`; K2 `scanned=2746 hits=0 allowed=27 unused_allow=0` (`harness-postintegration-head.txt`) |
| `<landing instrument> --selftest` | rc 0, `SELFTEST-RESULT pass cases=128`, 128 `ok`, 0 `FAIL` (`selftest-landing.txt`) |
| `<base instrument> --selftest` | rc 0, `SELFTEST-RESULT pass cases=115`, 0 `FAIL` (`selftest-base.txt`) |
| `probe.py` (78 S140-vs-instrument cases + 12 old-shape plants + name inventory) | `PROBE-BAD=0`, 78/78 agree, `base_missing=none new_missing=none new_extra=none`, `lost=none added=7` (`probe-out.txt`, `probe.py`) |
| `probe-extra.txt` (space/tab boundary; prefix × 26/27/300/301) | `EXTRA-BAD=0`, 8/8 agree |
| old-shape fire check (11 plain-token cases, base vs landing) | `OLD-FIRE-BAD=0` (`oldfire-out.txt`) |
| `git show 7ef1d36:SCORECARD.md \| grep '^\| capture-secret-scan'` | 1 row, 4 cells, last cell `87`, all seven round-96 names present (`scorecard-landing.md`, `row-landed.txt`) |
| `diff candidate-row.txt row-landed.txt` | rc 0, 0 lines (`row-diff.txt`) |
| `sed -n '{30,51,73,136,324,358,375}p' S140.txt` | each line is the cited `regex = '''…'''` |
| known-limits paragraphs, base vs landing | six families + `glptt-` dropped; six prefixes and non-GitLab limits kept (`known-limits-*.txt`) |
| allowlist shape histogram | 25 rows: authorization 2, bearer 2, cloudfront 2, credential 18, github-refresh-token 1; 0 round-96 shapes (`allow-shapes.txt`) |
| fixture mutants (`critic-fixture` branch in my clone, toplevel asserted) | do-nothing `c608a6ea` rc 1 (K1, K3 fail); right-boundary-dropped `d07c5d84` rc 0; ceiling-dropped `f9f2d98a` rc 0 (`mutant-*.txt`) |
| mutant false-positive demonstration | landing rejects `…cd12345x`, `…cd12345_`, 301-head; the two mutants accept them (`mutant-false-positives.txt`) |
| `sha256sum corpus/instruments/capture-source.py` | `0630d32b…` = the intake-gate pinned instrument (unchanged) |

Tooling: none installed or upgraded (python3 stdlib + git only); no pacman transaction
attempted. No lane git/jj mutation: the clone and the mutant branch live only in `$S`.
