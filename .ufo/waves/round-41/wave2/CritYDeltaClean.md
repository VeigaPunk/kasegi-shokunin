# CritYDeltaClean — I2 unrelated-delta falsification

## Counterexample

I2 enforces the intended exact-delta property: a Y that adds both the receipt and a tracked unrelated file must be red. The implementation does not merely accept arbitrary extra paths: it compares each changed path to the one receipt path and flips `diffclean=0` on any other path.

## Evidence

At integrated ref `ad7147532cb702b0d541d40499874552183d9132`, `corpus/instruments/r41-closure.sh` documents at lines 127–131 that the named export-ref is J and Y may differ only by the receipt. The I2 implementation at lines 783–797 verifies that the named ref is a commit, checks ancestry, then runs `git diff --name-only "$refhex" "$REF_RESOLVED"`; it initializes `diffclean=1` and sets it to 0 whenever a nonempty changed path is not `$RECEIPT`. `check_i2` requires `diff-clean=1` (lines 939–941).

Thus for J→Y with the receipt plus a tracked unrelated file, the name loop necessarily observes that unrelated path and marks the exact-delta predicate red. The diff is path-based, so a rename/add/delete of an unrelated tracked path is also exposed by the name-only diff. This conclusion is directly derived from the inspected implementation; I did not mutate the lane or run a final-Y verification. No commit graph/diff transcript from a constructed J/Y pair was obtained, so this does not claim an executed mutation result.

## Impacted axes

- depth:verifiability: this specific I2 exact-delta check appears resistant to the requested extra tracked-file counterexample.
- coverage: no impact identified.

## Smallest safe correction

None indicated for the tested case. Preserve the per-path equality check. For stronger evidence, add an isolated scratch fixture with J, then Y containing the receipt and a separate tracked file, and assert I2 reports `diff-clean=0` and the gate fails. Do not create that fixture in the lane.
