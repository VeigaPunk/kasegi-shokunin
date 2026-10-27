# RevQualityCriterion — round-41 wave 1 receipt

Seat: reviewer (leaf; no subagent, no task/agent/workpool call, no background job). Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` only. Base `5b29ea1439450b712581edf5f0bf98dfb262ab`;
claims-freeze `fbba3d96cdf8d37c1ea41304a1ba35691329684b`; worktree HEAD `b3b08b2` (wave-1 build spec +
dispatch; the corpus path is untouched by it). Frozen claims read at `.ufo/waves/round-41/claims.json`
(not edited); before-controls at `.ufo/waves/round-41/c1-controls/do-nothing.txt`,
`c2-controls/before.txt`, `census-before.txt` (read). Route chain captured at spawn: fleet-root cwd →
own scratch `/fast/scratch/hyaku/kasegi-r41/RevQualityCriterion`; every read/write by absolute path;
no git/jj mutation anywhere (only `git rev-parse`-class reads: `git log --oneline -3`, `git status
--porcelain`, `git ls-files`, `git diff --no-index`).

Disk guard before work: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` →
`/fast/scratch/hyaku use% 25`, `/tmp 3%`, `/var/tmp 35%` — green.

## Verdict: class NOT captured — criterion drafted

The r40 overclaim class (the round-41 lesson's M41-1): a lane record grades a frozen claim
`verified` / `held; verified` while the claim's own frozen kill rule fires on committed evidence.
Checked against the full QUALITY.md registry (Q1–Q10, R1–R37 read in full, with the R35/R36/R37
family read raw). No existing row captures it:

- **R35** binds a quoted `--export-ref` result to a committed transcript or a `report-only` label;
  **R37** widens that to every record stating a head/tally/gate outcome, adds receipt-as-unedited-tee
  provenance, and requires appended `Correction (round N)` for records contradicting the committed
  receipt. Neither reaches the class: in r40 the receipt at Y `d0fe34d3…` was committed and green
  (`closed=10/10 exit=0`, all-gates v4, teed transcript) and every grading record quoted it
  accurately — R37's contradiction limb is never triggered. The grade is wrong anyway, because the
  kill rule fires on committed fixtures no counter run reads.
- **R36** is captured-by closure for `none` mistakes rows — orthogonal.
- **R22/R25** are pre-freeze literal satisfiability — orthogonal (the predicate was satisfiable).
- **R11/R13/R17** require instrument/mutant discrimination — the defeat fixtures are exactly such
  evidence, but no row requires the *grade* to be calibrated against them; R13 even allows routing
  survivors "without changing the frozen counter", which r40 did, while the grade still said verified.
- **R16/R18** keep filed open-defect paragraphs open via closure checks — the opposite direction
  (a stale premise kept open), not an overclaimed verified grade.

Conclusion: **not captured-by** — drafted the next-id row `R38` (verified unclaimed:
`grep -c 'R38' corpus/QUALITY.md` → 0).

## Deliverable

| field | value |
|---|---|
| path | `.ufo/waves/round-41/wave1/RevQualityCriterion.criterion.txt` |
| bytes | 3437 |
| lines | 14 |
| sha256 | `a04a4e59d6d1ec8652eef8b7bcfedaf41a03d955d32391af9c639285402ef519` |
| shape | round-41 block appended at EOF of `corpus/QUALITY.md`: `## Round-41 additions …` heading + R6-form paragraph (pre-append byte/line/digest figures and the not-edited row list) + table header row + one criterion row `R38` |
| landing | `cat .ufo/waves/round-41/wave1/RevQualityCriterion.criterion.txt >> corpus/QUALITY.md` — append-only at end-of-file; no existing line is edited |

The bytes are the exact append bytes: nothing else is in the file (no validation text, no receipt
scaffolding, no fences). The generator asserts `"|" not in criterion` and `"|" not in grounded`
before writing.

## What the row states

- **Calibration rule (new):** a lane record grading a frozen claim `verified` / `held; verified`
  states that grade only after the claim's own frozen kill rule is re-derived for the round against
  committed evidence, including falsification fixtures. When any kill-rule clause fires on committed
  bytes, the grade is an overclaim whatever the verification ref printed — a green committed receipt
  at Y does not verify the claim.
- **Correction form:** every grading record is corrected by an appended `Correction (round N)` line
  grading the claim not verified on the frozen counter and naming the firing evidence — never by
  softening the grade in place, rewording the claim, or editing the frozen counter to fit the grade.
  The correction is itself a lane record carrying the firing fixture paths and the fired clause.
- **Grounding:** cites M41-1 (the lesson row the L1 mines this round), the round-40 verifier's D1
  routing and §4 overclaim verdict, the three grading records with line numbers, the fired kill-rule
  clause from the frozen round-40 claims, the three firing fixtures (ls-verified present), the
  R35/R37 non-capture analysis, and the round-41 operational limb I1 of `r41-closure.sh` — which at
  draft head is absent (`ls` → No such file), so it is stated as a landing requirement, not a draft
  measurement.

## Evidence — pre-append state of `corpus/QUALITY.md` (measured at write time, re-run twice)

````console
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && wc -l corpus/QUALITY.md && wc -c corpus/QUALITY.md
323 corpus/QUALITY.md
57226 corpus/QUALITY.md
$ sha256sum corpus/QUALITY.md ; head -c 57226 corpus/QUALITY.md | sha256sum
311224a000ebece91b7916942c2cfbbb03429de52010d7317c13d5d7e84e0375  corpus/QUALITY.md
311224a000ebece91b7916942c2cfbbb03429de52010d7317c13d5d7e84e0375  -
$ grep -n '^| R\(22\|23\|26\|27\|28\|29\|30\|31\|32\|33\|34\|35\|36\|37\) ' corpus/QUALITY.md | cut -d: -f1 | tr '\n' ' '
226 227 249 250 263 264 277 278 291 292 307 308 309 323
$ grep -c 'R38' corpus/QUALITY.md ; grep -c 'M41-1' corpus/QUALITY.md
0
0
````

The three figures carried in the block's R6 paragraph (323 / 57226 / `311224a…`) were re-measured
immediately before this receipt was written and were unchanged, so they are true at write time; under
R19 the landing commit must re-run them (`head -c <n> | sha256sum` + `wc -l`), because any round-41
append ahead of this block moves both.

## Evidence — grounding citations re-opened in-lane

````console
$ grep -n "D1 — C1 graded" corpus/lessons/round-40-verifier-spotcheck.md ; sed -n '95p' corpus/lessons/round-40-verifier-spotcheck.md
176:- **D1 — C1 graded "verified" while its frozen kill rule fires.** `SCORECARD.md` `## Round 40 result`
The report grades C1 "held; verified". That is an overclaim (calibration). The score stays 4 and no
$ sed -n '176,180p' corpus/lessons/round-40-verifier-spotcheck.md
  counter. Append `Correction (round 41)` lines grading C1 not verified on the frozen
  … (full D1 text read: firing fixtures `.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt`
  T2/T4/T7/T13/T14, `CritKillRule.h6-escapes.sh`, `MutH6H10.md` D2)
$ grep -n "held; verified" SCORECARD.md | head -1 ; grep -n "4 held, verified" LOG.md
1595:| depth:verifiability | 4 | **4 (held; verified)** | C1 suite `corpus/instruments/r40-closure.sh` …
1728:- C1 (depth:verifiability, 4 held, verified): `corpus/instruments/r40-closure.sh` H1–H10 landed; …
$ grep -n "held; verified" /home/vgpnk/Projects/shokunin/.ufo/reports/round-40/kasegi.md | head -1
32:- **C1 — depth:verifiability, 4 → 4 (held; verified).** …
$ ls -la .ufo/waves/round-40/wave2/RevC1Counters.defeats.txt .ufo/waves/round-40/wave2/CritKillRule.h6-escapes.sh .ufo/waves/round-40/wave2/MutH6H10.md
-rw-r--r-- 1 vgpnk vgpnk 15615 … MutH6H10.md
-rwxr-xr-x 1 vgpnk vgpnk  4377 … CritKillRule.h6-escapes.sh
-rw-r--r-- 1 vgpnk vgpnk  7978 … RevC1Counters.defeats.txt
$ python3 -c "import json; d=json.load(open('.ufo/waves/round-40/claims.json')); print(d['claims'][0]['kill_rule'])"
Any of: … a committed fixture shows a check passing while its defect is present; …
$ ls corpus/instruments/r41-closure.sh
ls: cannot access 'corpus/instruments/r41-closure.sh': No such file or directory
$ grep -n "Correction (round 41)" .ufo/waves/round-41/claims.json | head -1
  (C1 I1: `Correction (round 41)` lines in SCORECARD/LOG/SHONEN grading r40 C1 NOT verified on the frozen counter and naming the firing evidence)
````

Facts the row quotes were each read from these anchors, not from memory: the D1 routing text and the
§4 overclaim verdict; the three grading records; the frozen kill-rule clause; the three firing fixture
paths (present); the round-41 claims' I1 wording; the absence of `r41-closure.sh` at draft head.

## Evidence — dry landing in scratch (append-only proof)

`cp corpus/QUALITY.md $S/orig.md`; `cp orig.md q.md`; `cat <deliverable> >> q.md`:

````console
$ cmp <(head -c 57226 q.md) orig.md
                         (silent) => prefix bytes identical; no existing line is touched
$ git diff --no-index --numstat orig.md q.md
14	0	orig.md => q.md
                         (14 added, 0 deleted; exit 1 as expected for differing files)
$ wc -l orig.md q.md
323 orig.md
337 q.md
$ grep -c '^```' orig.md q.md
orig.md:10
q.md:10
                         (fenced-code state unchanged: the block carries no fence)
$ grep -cE '^\| R38 \|' q.md ; grep -c 'M41-1' q.md
1
1
$ awk -F'|' 'NR==337{print "fields="NF}' q.md
fields=5                 (3 cells + 2 boundary empties: the table row is intact)
$ awk 'NR==337{printf "pipes=%d len=%d\n", gsub(/\|/,"|"), length($0)}' q.md
pipes=4 len=2588         (a pipe inside a cell would make this 5+)
````

## Risks / limits of this deliverable

- **Id coupling:** R38 is the next free id at the pre-append head and M41-1 is unclaimed
  (`grep -c` → 0 each); if another seat mints R38 or the lesson numbers the row differently before
  landing, the L1 adjusts the id — the criterion text and grounding stand independent of the number.
- **M41-1 citation is forward-looking by design:** the row cites
  `corpus/lessons/round-41.md § Mistakes, minted this round` in the established R28/R29/R32
  convention; the lesson file does not exist at draft head. If the L1 names the mistake id
  differently, the citation line is updated at landing; the D1 anchors it cites are committed and
  stable.
- **R6 figures** (323 / 57226 / `311224a…`) are draft-time by construction; the landing commit must
  re-run `head -c`/`wc -l` and refresh the paragraph if they moved — the block says this itself.
- **Round-41 limb:** I1 of `corpus/instruments/r41-closure.sh` is stated as a landing requirement,
  not a measurement — the instrument is absent at draft head (wave seats are building it in
  parallel).
- No writes outside the assigned paths: deliverable + this receipt in
  `.ufo/waves/round-41/wave1/`, scratch under `/fast/scratch/hyaku/kasegi-r41/RevQualityCriterion`
  (removed before yield).

## Tooling installs

None this seat (no pacman — host-wide pause honored; no uv/npx/binary install; only `python3` from
the base system and read-only shell tools).

VERDICT: DELIVERED — `RevQualityCriterion.criterion.txt` (3437 bytes, 14 lines, sha256
`a04a4e59d6d1ec8652eef8b7bcfedaf41a03d955d32391af9c639285402ef519`) appends one `R38` criterion row
at EOF of `corpus/QUALITY.md`, citing M41-1 and D1, stating the kill-rule-calibrated claim-grade rule
and the appended-`Correction` repair form; dry landing adds 14 lines and deletes 0. The r40 overclaim
class is not captured by any existing criterion (R35/R36/R37 family checked in full).
