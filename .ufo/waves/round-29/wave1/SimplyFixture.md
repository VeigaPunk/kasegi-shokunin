# SimplyFixture — round 29 wave 1

Scope: simplify duplicated fixture/control evidence and report R14 size. Lane base `7a6591c1eb8a14f427297980a96fa8bb339f29ee`; claims freeze `f28ff5d26b29270f93163117e7255e24f0b1d947`. No tool installed or updated.

## Deletion made

Removed only the four duplicate top-level `.ufo/waves/round-29/assimilation/{collisions,staged-ids,reg-ids,quarantine-slice}` files. Before removal, `md5sum` showed each was byte-identical to its corresponding `wave1/assimilation/` file. The wave spec assigns the assimilation scratch to `ScoutAssimilation` at `wave1/assimilation/`, and the seat receipt `ExecCensusDry.md`/other wave receipts use that wave1 location. The retained copies preserve the evidence and sole working convention; no report or historical record was deleted.

## C1 controls

The `wave1/c1-controls/` bundle currently contains four text receipts: `before.txt` (1,894 bytes), `base-control-nogit.txt` (1,382), `base-control-selftest.txt` (44), and `base-control-grep.txt` (42): 3,362 bytes total, 16 KiB filesystem allocation. This is well below R14's few-hundred-KiB threshold. `before.txt` is also present at `.ufo/waves/round-29/c1-controls/before.txt` by frozen setup; the two copies were byte-identical. I contacted `ExecControlC1` before considering any bundle edits; I did not alter their bundle. Its mutant outcomes are captured in receipts, with no full mutant source copies observed in the lane tree; scratch mutant files may exist outside the lane and are not committed assets.

## Remaining size / duplicate observations

- `wave1/ExecCensusDry/` is 512 KiB, 42 files. It includes copied corpus content used for the scratch census, not merely a receipt. Compared with live corpus paths, 39 copies were byte-identical, `corpus/SOURCES.md` was intentionally modified for the planned append, and the F13 entry was a new scratch file. The seat's receipt names those exact scratch paths. `ExecCensusDry.mutations/` is 40 KiB (two altered control files); `CritC2Kill-scratch/` is 120 KiB; scout capture scratch is 28 KiB. The 512 KiB scratch mirror exceeds the R14 threshold, but replacing it with a tarball or regeneration script would require updating its owner's path-specific evidence; I did not rewrite another seat's receipt or scratch experiment. It is an outstanding consolidation candidate, not represented as compliant.
- `wave1/README.md` and `wave1/cwe.json` are standalone source duplicates. The latter parses JSON-equal to committed `corpus/source-snapshots/round-29/S045.txt`; the former is the Bugcrowd README represented by S044 capture. Multiple existing receipts explicitly cite these paths, so I retained them rather than invalidating evidence. Tradeoff: preserve cited evidence vs deduplicate further.

## Preserved contract and evidence

C1's do-nothing receipt assets remain present. `base-control-selftest.txt` records `selftest cases=9 failures=0`, exit 0; `base-control-grep.txt` records grep exit 0 and count 0; `base-control-nogit.txt` records the baseline git-free traceback and exit 1, so these controls cannot satisfy the target. Frozen `claims.json`, committed instrument bytes, and receipt paths were not changed. C1 directory measurement used `find ... -printf '%s %p'` and `du -sh`; C1 total is below R14 regardless of filesystem allocation.

No tests, build, formatter, or runtime checks run. Shared-tree bytes outside the authorized lane scope were untouched.