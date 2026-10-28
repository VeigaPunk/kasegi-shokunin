VERDICT: INFO

**Assimilation: none.** No staged theme is the coverage-map ground the lane lacks (Frontier F27, the Linux kernel security-bugs process). Id collisions are 40. Lane ids 70, staged ids 94. The 0–3-space guard is proved; the column-zero control misses the indented collision.

## Findings

**1. Package (read-only; no campaign tool).** `/home/vgpnk/Projects/shokuknow/merge/kasegi/MERGE-REPORT.md` sha256 `0e6759b47595f1bce5fbf49bf0422838ff89a394b2f424d17fb17d96a09106df`. `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` sha256 `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb`. `MERGE-REPORT.md:3` says nothing was written into the lane. `MERGE-REPORT.md:5-9`: accepted **94**, refused **0**, knowledge entries **67**, “lane registry currently holds **30** rows; first staged id is **S031**” — stale against the measured 70-row registry. `find …/knowledge -name '*.md' | wc -l` → 67. Guard pattern from `.ufo/prompts/kasegi-round-45.md:582-595`.

**2. Live id-collision guard.** Run 2026-10-28T21:05:39Z in `/fast/scratch/hyaku/kasegi-r45/R45ScoutMergePackage` (removed on exit). Lane HEAD `5242db6fbf2b3575da6600974f0b5b4292caa62f`; base `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd` is an ancestor. `git status --porcelain -- corpus/SOURCES.md` printed nothing. `git show dc5bb8c6e31efc4a6650819df85e79b72fd64bcd:corpus/SOURCES.md` ids equal the worktree (`diff -q` empty).

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <file> | grep -oE 'S[0-9]+' | sort
comm -12 reg-ids staged-ids > collisions
```

Printed counts:

```
reg-ids 70 unique 70
staged-ids 94 unique 94
collisions 40 unique 40
reg range S001 .. S070
staged range S031 .. S124
collision range S031 .. S070
5191c1d729f34958edd5aa0079e7e343a8c44f32e18dcfec2f17a8da2879c054  reg-ids
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  staged-ids
019cbfea1c9e0c1d095614454ac01bd596336f8161a68310954a59ac74724a05  collisions
S002 absent from staged-ids
S002 present in reg-ids
worktree reg-ids == base reg-ids
col0 reg 70 staged 94 collisions 40
live collisions identical under both extractors
indented 1-3 space pipe rows lane: 0
indented 1-3 space pipe rows staged: 0
4+ space pipe rows lane: 0
4+ space pipe rows staged: 0
do-nothing collisions lines 0 bytes 0
real collisions lines 40 bytes 200
do-nothing DIFFERS from real guard
```

Collisions (verbatim `comm -12` file): S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060 S061 S062 S063 S064 S065 S066 S067 S068 S069 S070. Lane ids are the contiguous run S001–S070 (70). Staged ids are the contiguous run S031–S124 (94). Free staged ids (not in the lane): 54, S071–S124.

Of the 40 overlapping ids, **1 URL is the same document** (`S042`, `https://www.ipa.go.jp/security/todokede/vuln/process.html`) and **39 are different documents**. Samples printed by the URL join:

```
S031
  lane   https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf
  staged https://hackerone.com/security/policy_versions
S070 is a different document on each side (lane: Google Bug Hunters rules directory; staged: GB/T 30279—202X drafting note).
```

Document-level URL intersection: 19 distinct URLs, 21 staged rows whose URL is already a lane row: S031→S043, S032→S044, S033→S045, S034→S049, S035→S050, S039→S033, S040→S034, S041→S035, S042→S042, S043→S041, S049→S046, S050→S047, S055→S036, S056→S037, S057→S038, S060→S039, S064→S041, S068→S040, S076→S041, S080→S048, S123→S032. No renumber map: nothing is adopted, so the collision list is a refusal input. Staged S071 (CNVD PHP advisory) and staged S072 (own-work annex transcription) are different documents from the S071/S072 this round’s frozen C2/C1 mint.

**3. Guard proof, indented `  | S002 |`.** Scratch registry: column-zero `S001`, then a two-space-indented `S002` row (11 columns, status `queued`). Scratch staged file holds only `S002` (live staged-ids do not). Printed:

```
0-3 reg: S001 / S002
0-3 collisions: S002
GUARD_NONEMPTY=yes
col0 reg: S001
col0 collisions bytes 0 lines 0
COL0_NONEMPTY=no
validate_exit=0
file	ok	…/guard/corpus/SOURCES.md
census_exit=0
file	rows	2
file	tier.B	2
file	status.queued	2
```

`rows=2` means the indented row was parsed. Second proof against the live staged-ids: column-zero `S001` plus indented `  | S031 |`. 0–3-space `comm -12` printed `S031` (`GUARD31_NONEMPTY=yes`); column-zero collisions were 0 bytes (`COL0_31_NONEMPTY=no`).

**4. Theme vs province and the missing coverage ground.** Province domain (`PROVINCE.md:3`) is bounty and security research, program rules, claim packages. Frozen C2 (`.ufo/waves/round-45/claims.json`) is F27 = the Linux kernel security-bugs process; the before-state says that surface is held nowhere in `corpus/`. Re-run:

```
grep -rliE 'security-bugs|linux kernel|kernel\.org' \
  corpus/knowledge corpus/SOURCES.md corpus/README.md
```

printed nothing (the command’s own echo was `lane_grep_exit_no_hits` and `package_grep_exit_no_hits`) on the lane and on the package. `grep -cE '^\| F27 \|' corpus/README.md` → `0`. `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → `26`. The coverage-map ground the lane lacks is not in the package.

In-province staged themes that the lane’s coverage map also does not hold — Chinese national grading `chinese-vulnerability-taxonomy-and-grading.md` (`ground: F14 (new frontier item)`, sources staged S037/S038; `grep -l 30279` under `corpus/knowledge` finds no knowledge file; README’s only Chinese row is F16, platform scope and rewards, not GB/T 30279) and Chinese criminal thresholds `chinese-criminal-thresholds-and-authorisation.md` (`ground: F12`, which the lane already uses for the Japanese disclosure workflow) — are not recommended. The grading theme’s S037 row was refused in `corpus/lessons/round-33.md` (spliced quote; flip unmet). Adopting either would be a new target the frozen C1/C2 predicates do not name (`.ufo/prompts/kasegi-round-45.md:650-656`: shokuknow material may serve a frozen claim only as ordinary curation, never as a new or widened target). Claim-packaging and program-scope themes are standing refusals (`corpus/lessons/round-33.md`) and overlap ground the lane already holds (HackerOne policy is lane S043). Four knowledge basenames exist in both trees (`authorised-testing-rules-of-engagement.md`, `japanese-domestic-disclosure-workflow.md`, `japanese-severity-vocabulary-and-impact-model.md`, `program-severity-ladders-and-reward-scales.md`); 63 staged basenames are absent from the lane. Lane knowledge file count printed `63`.

## Limitations

- No source was re-opened and no quote was located. This seat did not run the quarantine slice or a census of the live registry.
- Same-document counts use the first `http(s)` URL in the source cell, trailing slash stripped. They are not an anchor comparison.
- The lane worktree is two commits past the frozen base (`8cf62c8` freeze, `5242db6` wave spec). `corpus/SOURCES.md` ids match the base blob.
- Scratch `/fast/scratch/hyaku/kasegi-r45/R45ScoutMergePackage` is removed after this report is written. Nothing was written under `/home/vgpnk/Projects/shokuknow` or into the lane registry.
