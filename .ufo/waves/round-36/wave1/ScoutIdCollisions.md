# ScoutIdCollisions — round 36 assimilation id-collision check (scout, read-only)

Lane head at measurement: `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (claims-freeze); working tree has only untracked `.ufo/waves/round-36/*` files, `corpus/SOURCES.md` unmodified (sha256 `0f95a132a69e`, i.e. the 52-row registry; no S053 row yet). Staged file `shokuknow/merge/kasegi/SOURCES.append.md` sha256 `4fe049cbe4ba`. Nothing renumbered, nothing written outside this receipt and scratch.

## Commands (frozen, 0–3-space tolerant)
```
P='^ {0,3}\|[[:space:]]*S[0-9]{3,}'
grep -oE "$P" corpus/SOURCES.md                                  | grep -oE 'S[0-9]+' | sort > reg-ids
grep -oE "$P" shokuknow/merge/kasegi/SOURCES.append.md           | grep -oE 'S[0-9]+' | sort > staged-ids
comm -12 reg-ids staged-ids > collisions
```

## Result
| list | count | unique | range | digest |
|---|---|---|---|---|
| registry ids (`corpus/SOURCES.md`) | 52 | 52 | S001..S052 | `2d95a2702fa2` |
| staged ids (`SOURCES.append.md`) | 94 | 94 | S031..S124 | `550a0129a446` |
| collisions (`comm -12`) | **22** | 22 | S031..S052 (contiguous) | `11623fc54a36` |

- No duplicate ids within either list.
- Staged-id digest `550a0129a446` equals the round-35 value (same 94 ids). A second route (`^ {0,3}source:\s*S[0-9]{3,}` over the 94 staged knowledge files) yields the same 94 unique ids (`diff` empty).
- Round-35 reference was reg 52 / staged 94 / collisions 22 (S031..S052) after S052 landed; round 36 unchanged: **22 standing collisions, no new ones**.
- Registry ids: S001 S002 … S052 (every id S001–S052 present). Staged ids: S031 … S124 (every id contiguous). Collisions: S031 … S052 (all 22).
- Standing note: staged S053 is a different source (Japanese METI vulnerability-handling rule, 平成29年経済産業省告示第19号), not EPSS. Lane registry has no S053 yet (`grep -c EPSS corpus/SOURCES.md` = 0; no `epss-*` knowledge file yet). When the C2 EPSS row lands as lane S053, the same check predicts (fixture: real registry + one synthetic S053 row) **reg_ids=53, collisions=23, range S031..S053**. So lane S053 will collide with staged S053 (different source); that is the standing scratch-side renumber class, not a lane defect (append-only registry; nothing renumbered here).

## Guard proof (scratch fixture, all under /fast/scratch/hyaku/kasegi-r36/ScoutIdCollisions/fx)
Fixture registry: `S001` at column 0 and `S031` row indented 2 spaces; staged: `S031`, `S099`.
```
0-3-space pattern:      reg=S001 S031   collisions=[S031]   -> indented collision CAUGHT
column-0-only pattern:  reg=S001        collisions=[]       -> indented collision FALSE-GREEN
4-space-indent boundary (0-3 pattern): row `    | S032` NOT matched (reg=S031 only) -> known limit, same as r35
fail-closed wrapper on fixture:           reg_ids=2 collisions=1 [S031]   exit=0
missing registry path (fixture):          "missing registry: .../nonexistent.md"   exit=2
missing staged path (fixture):            "missing staged: .../nonexistent.md"     exit=2
missing registry path (real, corpus/NOPE.md vs real staged): "missing registry: ..."  exit=2
```
Verdict: guard is load-bearing (0–3-space catches the indented row that column-0-only misses) and fails closed (exit 2) on a missing registry path. Bare pipeline without the `[ -r ]` precheck would silently give reg_ids=0 (r35 measured exit 1 via the downstream check); the precheck wrapper makes it exit 2.

## Assimilation: none
No lane edits, no renumbering, no tool installs. Scratch dir removed at exit.
