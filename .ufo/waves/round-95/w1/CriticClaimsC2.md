# CriticClaimsC2 — kasegi round 95, attempt 1 (C2 attack)

Seat: CriticClaimsC2 (leaf). Reviewed claim: C2 at landing
`38e7319f44a9fab2978b59ffd43faf207cf62b32` (parent `53ec479d…`, C1 landing; base
`9ef0126c…`, freeze `347519f2…`). Counter `.ufo/waves/round-95/c2/capability-check.py`,
sha256 `9011e1b474d74a376b35301af562e70f4a6235c09798d15f429b70f0144fddf6` (equals the
frozen `counter_sha256` at the landing and in the working tree). All work in
`/fast/scratch/hyaku/kasegi-r95/CriticClaimsC2` (removed at seat exit); the landing was
read through a clone made from the lane, never mutated.

## Verdict

**C2 STANDS** on its frozen predicate P1 ∧ P2 ∧ P3, re-derived at the landing with the
pinned counter: seeds **77031**, **913457** and **20261107** each print
`CAPABILITY-CHECK-RESULT pass rc=0` with
K1 `inst_sha=pin-ok gate_sha=pin-ok selftest=pass cases=115`,
K2 `rc=0 scanned=2477 hits=0 allowed=26 unused_allow=0`,
K3 `rc=1 hits=6 missing=none extra=none`, K4 `base_new_shape_hits=0 old_shapes_missing=none`,
K5 `rows=1 last=87`, K6 `rc=1` with `aws-sts-session-token` present. P2 holds (landed
instrument sha256 `66edd661…` equals the candidate pin; `claim-package-check.py` sha256
`8b6f8493…` equals the gate pin). P3 holds: the C2 landing commit has one parent
(`53ec479d…`) and changes exactly `SCORECARD.md`,
`corpus/instruments/capture-secret-allow.tsv` and
`corpus/instruments/capture-secret-scan.py`.

One **routed citation defect** and two wording/doc qualifiers are recorded below; none
re-scores C2.

## Counterexample (routed, not claim-scoring)

**The statement's S140 anchor is off by one.** The frozen statement (and the surface row)
cite "S140 lines 429, 446, 463". In `corpus/source-snapshots/round-94/S140.txt` those are
the `keywords` lines (`keywords = ["glcbt-"]`, `["glsat-"]`, `["gliamat-"]`); the regexes
that carry the optional 1–20-character instance prefix and the 10–1000 / 20–1000 segment
lengths the sentence describes are lines **430, 447, 464** (`nl -ba`, receipt 21). The
round-94 scout had already recorded the required anchors and the rule: "S140's own row
only names their *regex* lines, so a round-95 claim citing them must cite S140 L447/L464
explicitly" (`.ufo/waves/round-94/w1/ScoutGitLabRules.md:213`, also `:252`). The landed
instrument is internally inconsistent about it: its module docstring cites
`S140 lines 430, 447, 464` (`capture-secret-scan.py:123-124`) while the newly added
selftest comment cites `S140 lines 429, 446, 463` (`capture-secret-scan.py:437-438`).

This is citation precision, not a shape defect: the three regexes at 430/447/464 carry the
same optional 1–20-character prefix range and 10–1000 / 20–1000 segment lengths the landed
pattern uses (the landed pattern replaces the source's leading `\b` with the class's
pre-existing escape-aware left boundary); 40 independent probes (below) hit only the
claimed shapes; and no predicate P1–P3 reads line numbers. The statement cannot be
re-worded after landing (kill rule), so this is routed to the L1 for a future wording
pass, not a verdict change.

## Re-derivation (independent of the frozen controls)

### P1 — counter at the landing, three own seeds

`python3 -B .ufo/waves/round-95/c2/capability-check.py --lane <landing clone> --rev
38e7319f… --work <scratch>/work-<seed> --instrument-sha256 66edd661… --gate-sha256
8b6f8493… --seed <seed>`. Receipts `01-capcheck-seed-{77031,913457,20261107}.txt`; all
three runs are byte-identical apart from the seed line and print the K1–K6 values above,
`CAPABILITY-CHECK-RESULT pass rc=0`. Observed counts, same at all three seeds:
`scanned=2477`, `hits=0`, `allowed=26`, `unused_allow=0` (K2); plant HIT set size `6`,
`missing=none`, `extra=none` (K3); `base_new_shape_hits=0` (K4); `rows=1`, last cell `87`
(K5); K6 `rc=1`, shapes `aws-access-key-id,aws-sts-session-token,credential`.

### P2 — pins

- `git show 38e7319…:corpus/instruments/capture-secret-scan.py | sha256sum` =
  `66edd66143ec62f6e40c864817a97383916d7ff67e5ab384e130b65c44516707` = candidate pin
  (`candidate-scanner.py` has the same sha).
- `git show 38e7319…:corpus/instruments/claim-package-check.py | sha256sum` =
  `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` = gate pin; the
  gate is unchanged from base to landing (`git diff --stat` empty).
- Counter working-tree and landing-blob sha both equal the frozen `9011e1b4…`.

### P3 — landing commit path set

`git show --name-status 38e7319…` prints parent `53ec479d…` and exactly three modified
paths: `SCORECARD.md`, `corpus/instruments/capture-secret-allow.tsv`,
`corpus/instruments/capture-secret-scan.py`. No other path, no rename/delete/mode change.
The `## Capabilities` row at `SCORECARD.md:307` is byte-equal to
`.ufo/waves/round-95/c2/candidate-row.txt` (3876 bytes; receipt 19), contains both
`github-refresh-token` and `gitlab-jwt-token`, and its last cell is `87`.

### Shape behaviour — 40 own fixtures

The landed instrument was extracted from the landing commit into scratch and run with
`--files` against my own fixtures (30 + 10), then parsed by basename; expected sets were
written from the claim before the run. **30/30 and 10/10 match; 0 mismatches**
(receipts 06, 06b, 26). Key results:

| shape probe | observed |
|---|---|
| `ghr_` + 76 `[A-Za-z0-9]` | `github-refresh-token` |
| `ghr_` + 75 / + 77 | none |
| `ghr_` + 36 classic | `github-token` |
| `ghr_` 76 followed by `_` / by a letter | none (right bound); followed by `-` or `/` hits |
| `glcbt-` / `glsat-` bare and with 1- and 20-character instance prefix | `gitlab-jwt-token` |
| `gliamat-` bare | `gitlab-jwt-token` |
| non-`eyJ` first or middle segment | none |
| third segment 19 / 20 / 1000 / 1001 characters | none / hit / hit / none |
| letter before `glcbt-`, `gliamat-`, or `ghr_` | none |
| `\u0020`, `%20`, `%26`, `&#x26;`, `\n`-escaped left context (both classes) | hit |
| classic 36 `ghr_` in `\u0020` context | `github-token` |

Baseline discrimination: the base instrument at `9ef0126c` prints
`SELFTEST-RESULT pass cases=101`; the landing prints `cases=115`. On the same 40 fixtures
the base instrument reports only `github-token` (the 36-character classic), i.e. neither
new shape. On the actual base tree the base instrument prints
`scanned=2476 hits=0 … allowed=24 unused_allow=0 rc=0`; on the landing tree it still
misses both new classes (`scanned=2477 hits=0 allowed=24`), so no-work cannot reach the
target (receipt 27). The extraction of quoted selftest case names found 99 base names and
113 landing names, with every base name present and exactly 14 new names; the selftest's
own counts are 101 and 115.

### Allowlist row — digest bound to the exact matched bytes

The landing allowlist has 24 data rows (23 at base; the C2 commit adds exactly one). The
new row is `(path, github-refresh-token, c7ad99a1ba7ef9a9eb954d3b93e3dea3d109ac298fc2c580cacf35c959ef060d)`.
In the landing blob for that path, the refresh pattern matches twice (offsets 669–748,
line 10; 1450–1529, line 26), and **both matches hash to `c7ad99a1…`** — the row is bound
to the exact matched bytes, not to the file or path alone (receipt 04; the placeholder
value is masked in the receipt). Lens:

- exact bytes at the exact relative path in a scratch fixture repo: `hits=0 allowed=2 rc=0`;
- one byte changed inside the first occurrence (offset 679): `hits=1 allowed=0 rc=1`
  (`github-refresh-token`, line 10) — the digest, not the path, decides;
- identical bytes moved to `other-receipts/…`: `hits=1 allowed=0 rc=1` — the path is part
  of the key.

The +2 allowed events over the +1 row are the two identical occurrences of the one
published placeholder (base 24 events, landing 26). This is consistent, not a stale row.

### Output hygiene

`HIT` lines print `shape=… path=… line=…` only; the scan summary prints counts only;
`--selftest` prints case names and shape sets only; the allow row's reason describes the
synthetic placeholder without printing its 76-character value. No matched token value
appears in any output I captured (receipts 06, 06b, 07, 12–15).

## Qualifiers (no verdict change)

1. **Counter docstring.** `capability-check.py:20` says K3's plant set is "four positives,
   six negatives"; `PLANT_SPEC` has six positives (`p1`–`p6`) and six negatives
   (`n1`–`n6`), and the limb prints `hits=6`. The counter is sha-pinned at the freeze, so
   the text can only be corrected at a future counter revision.
2. **GitHub left boundary is not stated.** The refresh sentence names only the right bound
   `(?![A-Za-z0-9_])`; the pattern also inherits the class's pre-existing `_ESC_LB` left
   boundary, so `xghr_`+76 does not hit (probe c07) while escaped contexts do. This matches
   the class convention (the GitLab `xglcbt-` negative behaves the same), but the wording
   does not say it.
3. **S141 resolution.** S141 is a registry row (`corpus/SOURCES.md:153`) plus the round-94
   R08 receipt, not a committed snapshot file; the row itself records the `ghr_` rule at
   raw line 72, and `08-github-rules-file.txt:16` confirms `72:regex = "ghr_[0-9a-zA-Z]{76}"`.
   The citation is accurate but resolves through the registry row/receipt rather than an
   `S141.txt`.

## Impacted axes

- **coverage (8 held; delta 0).** The capability extension is real: the base instrument
  misses both new classes on the landing tree, and the landed instrument hits every shape
  the statement names. No attack built here survives, so nothing justifies a downgrade or
  an increase; the coverage denominator remains operator-owned as in earlier rounds.
- **depth:verifiability.** One routed citation-precision defect (S140 off-by-one,
  duplicated in the landed selftest comment) and one counter-docstring nit; neither changes
  a predicate or the landing's behaviour.

## Smallest safe correction

At the next freeze-capable wording pass (not now; the statement is frozen after landing):
change the C2 statement/surface parenthetical "S140 lines 429, 446, 463" to
"S140 lines 430, 447, 464" (or "keyword lines 429/446/463; regexes 430/447/464"), make the
same correction in the landed selftest comment at `capture-secret-scan.py:437-438`, and
change the K3 docstring "four positives" to "six positives". No scanner, allowlist,
SCORECARD row or counter behaviour changes; the frozen artifacts stand as landed.

## Receipts

All under `.ufo/waves/round-95/w1/CriticClaimsC2-receipts/`; each file is observed output
from the command named, run from the lane root unless noted. No credential/placeholder
value is reproduced.

| receipt | command | rc | lines |
|---|---|---|---|
| `01-capcheck-seed-77031.txt` | `python3 -B .ufo/waves/round-95/c2/capability-check.py --lane <clone> --rev 38e7319f… --work <scratch>/work-77031 --instrument-sha256 66edd661… --gate-sha256 8b6f8493… --seed 77031` | 0 | 8 |
| `01-capcheck-seed-913457.txt` | same, `--seed 913457` | 0 | 8 |
| `01-capcheck-seed-20261107.txt` | same, `--seed 20261107` | 0 | 8 |
| `02-pins-and-allow-count.txt` | `git show … \| sha256sum` for instrument/gate/candidate; allow-row counts at base/landing; allow diff tail | 0 | 13 |
| `03-allow-rows.txt` | landing allowlist rows with `nl -ba` | 0 | 25 |
| `04-allow-digest-derivation.txt` | `git show 38e7319…:<receipt> \| python3` (match count, per-match sha256, line, masked context) | 0 | 11 |
| `05-extracted-inst-sha.txt` | `git show 38e7319…:<instrument> > <scratch>/inst/…`; `sha256sum` | 0 | 1 |
| `06-shapes-landing.txt` | landed instrument `--files` over 30 own fixtures (raw HIT/summary lines) | 1 | 22 |
| `06b-shapes2-landing.txt` | landed instrument `--files` over 10 further fixtures | 1 | 10 |
| `07-selftest-and-base-on-shapes.txt` | base `--selftest` (`cases=101`), landing `--selftest` (`cases=115`), base instrument on the 30+40 fixtures (1 then 2 hits, all `github-token`) | 0 / 1 / 0 | 13 |
| `08-provenance-lines.txt` | `grep -n` S140 regex lines; `sed -n 169p` S142; `grep -n '^| S141 '` SOURCES; R08 receipt head | 0 | 11 |
| `09-scorecard-row.txt` | `grep -n` capture row; cell/last-cell parse; landing SCORECARD diff; gate diff | 0 | 20 |
| `10-s140-cited-lines.txt` | `sed -n '427,431p;444,448p;461,465p' S140.txt` with `nl` | 0 | 18 |
| `11-s141-capture.txt` | `wc -lc` and `cat` R08 receipt | 0 | 23 |
| `12-allow-exact.txt` | fixture repo (toplevel asserted) with the exact receipt path/bytes; `--lane … --rev HEAD --allow <landing allow>` | 0 | 3 |
| `13-allow-mutated.txt` | same fixture, one byte changed at offset 679 inside the first occurrence | 1 | 4 |
| `14-allow-path-binding.txt` | same bytes at `other-receipts/…`; also greps the output for the body (0) | 1 | 7 |
| `15-output-hygiene-and-row.txt` | grep outputs for fixture token bodies (none); SCORECARD name counts; candidate-row tail | 0 | 7 |
| `16-instrument-diff.txt` | `git diff 9ef0126c… 38e7319f… -- corpus/instruments/capture-secret-scan.py` | 0 | 53 |
| `17-case-sets-and-ancestry.txt` | python extraction of base/landing selftest case names and pattern names; `git rev-parse 53ec479d^`; coverage row grep; `## Capabilities` line | 0 | 21 |
| `18-coverage-score.txt` | `grep -nE '^\| coverage \|' SCORECARD.md`; round headings | 0 | 56 |
| `19-row-equality-and-p3.txt` | python row-vs-candidate-row compare; `git show --format='parent %P' --name-status 38e7319f…` | 0 | 12 |
| `20-counter-pin-and-docstring.txt` | `sha256sum` counter working/landing; frozen pin; `grep -n "four positives\|PLANT_SPEC"` | 0 | 10 |
| `21-citation-anchors.txt` | `nl -ba` S140 429–430/446–447/463–464; S142 169; R08 `72:regex` | 0 | 20 |
| `22-mutation-offset.txt` | python list of the two placeholder match offsets/lines; notes offset 679 | 0 | 3 |
| `23-s140-conversion-and-citations.txt` | S140 manifest and first 12 lines; prior round-94 citations of L430/L447/L464 and the rule at `ScoutGitLabRules.md:213` | 0 | 65 |
| `24-r94-critic-precedent.txt` | grep of the round-94 CriticClaimsC2 verdict/defect headings (context only) | 0 | 20 |
| `25-r94-critic-tail.txt` | `sed -n '150,200p' .ufo/waves/round-94/w1/CriticClaimsC2.md` (context only) | 0 | 51 |
| `26-shape-parse-landing.txt` | python parse of receipts 06/06b against the pre-written expectations; `SUMMARY cases=30 mismatches=0` and `cases=10 mismatches=0` | 0 | 42 |
| `27-do-nothing-baseline.txt` | base instrument `--lane <landing clone> --rev 9ef0126c…` and `--rev 38e7319f…` with the base allowlist | 0 / 0 | 4 |
| `28-final-consistency.txt` | `nl -ba` selftest comment lines; `git show --raw` P3 mode/status; `sha256sum` of the three capcheck outputs with the rev/seed line removed (all three equal) | 0 | 16 |
