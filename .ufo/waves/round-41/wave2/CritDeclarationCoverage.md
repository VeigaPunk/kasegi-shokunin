# CritDeclarationCoverage — I5/I12 declared-blocks attack

## Axes
- **depth:verifiability:** whether the closure suite detects changes omitted from `declared-blocks.txt`.
- **coverage:** whether declarations cover the changed-file set rather than only validating listed declarations.

## Reproduced probe
At integrated ref `ad7147532cb702b0d541d40499874552183d9132`, I made a scratch shared clone (asserted its top-level path before committing), appended one line to `SCORECARD.md` and one to `corpus/QUALITY.md`, committed as `d9c87946115c096aa755a92033e730e202ca5146`, and ran its committed suite copy using that clone as `--lane` and the scratch export/work paths. No lane-tree writes were made.

The run did **not** close: `I5 payload=declared=132,valid=130,... closed=0`; `I12 ... declared=132,valid=130,... closed=0`; final `closed=8/12 exit=1`. The transcript also had I6 red because this seat's work path was within the scanned `/fast/scratch/hyaku` family container. Thus this run does not establish a passing kill-rule survivor. In particular, it is not evidence that the two appended changes were independently detected: the aggregate declaration mismatch and unrelated I6 failure confound that conclusion.

## Counterexample in the predicate / remaining gap
The reproduced source makes the coverage gap concrete: `declared_blocks_check` (`corpus/instruments/r41-closure.sh:1054-1115`) iterates declaration records and validates each listed path's tail and diff. It never enumerates all paths changed between `BASE_REF` and `REF`, nor checks that every changed append-only file has a declaration. `check_i5` simply runs this validator (`1118-1125`). The declarations are therefore a validated subset, not a completeness assertion. A newly changed path absent from the declaration file is not visited by this loop. I could not demonstrate a green committed probe for the requested mutation pair; report this as a coverage weakness, not as a reproduced kill-rule escape.

## Smallest safe correction
Compare the complete changed-path set for `BASE_REF..REF` with the declared-path set and require exact coverage (with explicitly specified exclusions only if the contract names them). For each changed path, also require the already-claimed append-only/no-deletion condition; reject unlisted paths. Add separate selftest fixtures for (1) an undeclared append to `SCORECARD.md` and (2) a changed path omitted from declarations, asserting that each specific mutation causes I5/I12 red. The current probe is red overall, so it does not settle whether those focused fixtures can produce a false green.

## Verification limits
The scratch fixture suite output is recorded above exactly as observed. This is a scratch probe against the integrated ref, not a final Y run; I make no claim of final Y verification. No tools were installed. Scratch was removed before filing. No change was made to suite, lane source, frozen claims, or another seat's deliverable.

Report: .ufo/waves/round-41/wave2/CritDeclarationCoverage.md