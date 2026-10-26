# CritC2Junk — round 40

## Deliverable

`CritC2Junk.txt` (56 lines, 5,248 bytes), sha256 `f97215ff6ff7ce9eae968591755f947e38d7eab5b2d78eaa44e012d6a0ba5dde`.

## Evidence

- Read frozen `.ufo/waves/round-40/claims.json` first; C2 kill rule requires all nine decided, >=4 mined, Gate evidence per decided row (mined: capture+entry+passing source-recheck; rejected: reason+flip), S060+ row and entry, 23 frontier rows, harness 26/26, census exit 0, and rejects a junk twin.
- Read frozen `c2-controls/before.txt` and `c2-controls/junk-decisions.md`; observed baseline queued=9 and the control's all-rejected/no-evidence design.
- Read relevant `frontier-recheck-count.py`, `capture-binding-check.py`, `source-recheck.py`, census validator, `SOURCES.md`, `corpus/README.md`, round-39 lesson and entry formats.
- Ran `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`: scratch root use 26%, free 601.9G; proceeded only after green.
- Built controlled copies of the lane corpus under `/fast/scratch/hyaku/kasegi-r40/CritC2Junk/` (varA, varB, varC), leaving the lane corpus unchanged. `python3 build_fixtures.py` completed (`done`). No tool installs.
- Variant A: queued 0 / mined 0 / nine entries 0 / S060+ rows 0 / S060+ entries 0 / frontier 22 / harness 25/25 / census exit 0, W04 S028/S029 only. All-rejected gives the scalar `(20+22)/(20+22)=42/42=1.000`, but fails mined floor and the Gate block evidence requirement.
- Variant B: queued 0 / mined 4 / nine entries 4; no round-40 capture or manifest; source-recheck S016 returned `manifest UNAVAILABLE reason=missing`, exit 2. Five rejected rows had reason+flip. The mined Gate-evidence clause rejects the dummy entries.
- Variant C: queued 0 / mined 4 / nine entries 4 / S060+ rows 1 / S060+ entries 1 / frontier 23 / harness 26/26 / capture binding 51/51, unbound 0 / source-recheck all tested IDs exit 0 / census exit 0 with W04 S028/S029 only. This shows the counter's local integrity checks do not authenticate invented capture provenance. The finding is a freeze defect/risk: Gate quote+URL/fetch provenance needs an explicit independent evidence condition. This is not presented as a valid source-gathering result.
- Deliverable confined to scoped output; no lane source edits, git mutations, or tool installs. Scratch directory removed before filing this receipt.
