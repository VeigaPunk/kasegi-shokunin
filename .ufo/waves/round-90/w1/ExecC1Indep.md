# ExecC1Indep — independent verification of C1 (kasegi round 90, attempt 1)

Verdict: **AGREE with every frozen C1 number; no routed defects.** The landing
commit 4a7e676895d3fc74e18c853457c9b465ade2ddf5 changes exactly
`corpus/knowledge/triage-thresholds.md`, only at the 34 mapped sites (32 lines;
261 and 270 carry two sites each), each change is a single backticked
key→value token swap bound to a non-author WRONG label, and the round-90
meter's archive pin survives a working-tree environment attack that moves the
round-89 meter.

Method: I wrote my own verifier (receipts/verify_c1.py, sha256
38adcec63d6fae23ee08886bc361e3d45735cfcec77b1649b8486b5ae840eea1) that reads
nothing from either counter — every input is `git show` / `diff-tree` /
`ls-tree` of the lane object store plus the frozen map/excluded/labels bytes.
The frozen counter was then run as a black box on two different checkouts, and
attacked through the working tree. Scratch root
`/fast/scratch/hyaku/kasegi-r90/ExecC1Indep/` was deleted before this report;
no counter/gate output ever touched /tmp.

## 1. Own-script site verification — PASS 17/17 (receipts/verify_c1.out)

- **P3**: `git diff-tree --no-commit-id --name-only -r 4a7e6768` names exactly
  one path: `corpus/knowledge/triage-thresholds.md`.
- **Only changed lines are the map sites**: base→after line diff of the 488-line
  document = exactly the 32 distinct map lines (34 rows; lines 261 and 270 carry
  two sites each, matching the 32/32 diffstat). The 4 excluded sites
  (152, 155, 249, 438) are byte-identical to base.
- **Each changed token equals the map value**: every after line equals its base
  line with the backticked key replaced by the backticked value (chained on the
  two-site lines); each key occurs exactly once on its base line; no other
  differences anywhere.
- **Label binding**: all 34 map rows equal a WRONG row of tranche5-labels.tsv at
  02b6d88f1c059e2f881fd07c73834f502b4f212d — same citing-file:line, same key,
  supported range == map value. unbound=none.
- **Tranche arithmetic closes**: the labels file holds 40 WRONG verdict rows,
  38 with a supported range = 34 mapped + 4 excluded, leftover=none, and both
  excluded rows named in excluded.tsv exist as WRONG-with-range labels. The
  other 2 WRONG rows carry `none` and are correctly outside the tranche.
  (Reading note, not a defect: `grep -c WRONG` gives 41 because one reason
  column contains the word "WRONG".)
- **Value ranges inside their entries at the landing**: every
  `corpus/knowledge/<file>.md:A[-B]` value is within 1..linecount of that file
  at 4a7e6768 (out_of_range=none); each target file is the only tracked file
  outside .ufo/ with its basename; the 5 distinct target files are
  claim-gates.md, claim-package-contract.md, ev-model.md, intake-surface.md,
  mission-control.md; all 5 key basenames are absent at the base repo root
  (independent replica of the keys' GONE binding; mirror_absent=True).
- **Pins**: worktree map sha256 7c420856c3347d362bfc419030aa474cbc253975f3026bc13355b654055fb8b3
  and meter sha256 8f4ac21823979adb4096977ede78140eeade19baaa9072f546a5d6dd703836d4
  equal the claims.json pins and the freeze-rev bytes of both files.

## 2. Frozen counter, live lane vs `git clone --shared` — AGREE

Command (claims.json form; identical args except `--lane`; receipts
meter-lane.out / meter-clone.out):

```
python3 -B .ufo/waves/round-90/c1/knowledge-meter.py --lane <lane-or-clone> \
  --base-rev 6088c3eb0c29040415c69e7b5fb91e110480ab26 \
  --after-rev 4a7e676895d3fc74e18c853457c9b465ade2ddf5 \
  --map .ufo/waves/round-90/c1/repair-map.tsv \
  --labels-rev 02b6d88f1c059e2f881fd07c73834f502b4f212d \
  --base-target 812/1827 --target 843/1829 \
  --map-sha256 7c420856c3347d362bfc419030aa474cbc253975f3026bc13355b654055fb8b3 \
  --work $S/w
```

| number | live lane | shared clone | frozen receipt | verdict |
|---|---|---|---|---|
| base | 812/1827 | 812/1827 | 812/1827 | AGREE |
| after | 843/1829 | 843/1829 | 843/1829 | AGREE |
| M0/M1/M3/M4/M5/M9/M6 | all pass | all pass | all pass | AGREE |
| rc | 0 | 0 | 0 | AGREE |

The two outputs are byte-identical (`diff` clean, OUTPUTS-IDENTICAL) and match
l1/c1-landing-r90.txt line for line, including
`HOST base abs_tokens=127 abs_nongone=23` on both readings.

## 3. Environment attack on the pin claim — AGREE (r89 moves, r90 does not)

In the scratch clone (git rev-parse --show-toplevel asserted = the clone), I
planted an **untracked** file `ExecCapS043.md` at the repo root — a path named
by the bare GONE citation `` `ExecCapS043.md:57` `` at
`corpus/knowledge/program-severity-ladders-and-reward-scales.md:57` (selected
from my own gone-token scan of the 4a7e6768 scope; the token is absent from
both the landing tree's and HEAD's root listings, so it is GONE in the pinned
classification). `git status --porcelain` shows `?? ExecCapS043.md`. Planted
content is a two-line prose note (nothing credential-shaped). Then, with
`--measure-rev 4a7e676895d3fc74e18c853457c9b465ade2ddf5`:

| meter | before plant | after plant | moves? | verdict |
|---|---|---|---|---|
| round-89 meter (`.ufo/waves/round-89/c1/knowledge-meter.py`) | 845/1829 | **846/1829** | yes (+1, working-tree classify) | expected: moved |
| round-90 meter (`.ufo/waves/round-90/c1/knowledge-meter.py`) | 843/1829 | **843/1829** | no — output byte-identical (`diff` clean) | required: unmoved — holds |

The round-89 meter imports resolve.py from and classifies against the live
checkout, so the untracked file flips one bare token GONE→INTERNAL; the
round-90 meter classifies a `git archive` extract, so it cannot see the file.
This is a sharper reproduction of the freeze-time env control (r89 815 live /
814 clone vs r90 812/812 at base): the pre-existing r89 drift on the clean
clone (845 vs 843 at the same rev) is the same unpinned-readiness defect the
round-90 successor closes. Receipts: r89-before/after.out, r90-before/after.out,
gone-candidates.txt.

## Environment / hygiene

- No tools installed or upgraded (none needed); no pacman use.
- Lane untouched except my wave files; all git use read-only
  (`show`/`diff-tree`/`ls-tree`/`status`/`clone --shared`); the only mutation
  anywhere was the untracked plant inside my own scratch clone (deleted with
  the scratch).
- Scratch `/fast/scratch/hyaku/kasegi-r90/ExecC1Indep/` deleted before yield —
  confirmed gone.
- No credential-shaped value appears in any file below w1/ (meter outputs and
  the verifier carry no secrets; the plant content is plain prose recorded in
  §3).

## Files written

- `.ufo/waves/round-90/w1/ExecC1Indep.md` (this report)
- `.ufo/waves/round-90/w1/ExecC1Indep-receipts/verify_c1.py`
- `.ufo/waves/round-90/w1/ExecC1Indep-receipts/verify_c1.out`
- `.ufo/waves/round-90/w1/ExecC1Indep-receipts/meter-lane.out`
- `.ufo/waves/round-90/w1/ExecC1Indep-receipts/meter-clone.out`
- `.ufo/waves/round-90/w1/ExecC1Indep-receipts/r89-before.out`
- `.ufo/waves/round-90/w1/ExecC1Indep-receipts/r89-after.out`
- `.ufo/waves/round-90/w1/ExecC1Indep-receipts/r90-before.out`
- `.ufo/waves/round-90/w1/ExecC1Indep-receipts/r90-after.out`
- `.ufo/waves/round-90/w1/ExecC1Indep-receipts/gone-candidates.txt`
- `.ufo/waves/round-90/w1/ExecC1Indep-receipts/c1-landing-r90.txt` (copy of the cited landing receipt)
