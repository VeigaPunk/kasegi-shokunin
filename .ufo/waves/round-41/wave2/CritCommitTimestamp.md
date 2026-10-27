# CritCommitTimestamp — falsification result

## Counterexample and reproduced transcript

The timestamp gate is a wall-clock comparison, not a provenance check on the timestamp's origin. The suite's `ref_utc` reads `git log -1 --format=%ct` from the lane (`corpus/instruments/r41-closure.sh:464-470`); `iso_past` accepts a syntactically shaped UTC value iff its parsed epoch is at most the checking process's current epoch plus 120 seconds (`:472-482`). I2 requires the receipt timestamp to equal the named ref's committer instant and requires `not-future=1` (`:916-933`). Thus arbitrary commit metadata inside that allowance is accepted as the ref-commit time.

I created an isolated repository at `/fast/scratch/hyaku/kasegi-r41/CritCommitTimestamp/repo`, verified its top level before committing, then supplied `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` directly. This exact transcript was produced (UTC host date was 2026-10-27):

```
requested=119 actual_offset=119 iso=2026-10-27T11:47:51Z acceptable=1
requested=120 actual_offset=120 iso=2026-10-27T11:47:52Z acceptable=1
requested=121 actual_offset=121 iso=2026-10-27T11:47:53Z acceptable=0
requested=3600 actual_offset=3600 iso=2026-10-27T12:45:52Z acceptable=0
requested=86400 actual_offset=86400 iso=2026-10-28T11:45:52Z acceptable=0
```

The exact bound is inclusive: `timestamp <= verification-clock-at-evaluation + 120 seconds`. The one-second-over case is red. For bounded past time, the function has no lower bound; any correctly formatted date before the clock is accepted. The sandbox experiment directly exercised the helper's stated comparison against Git-generated commit epochs; it did not invoke the whole suite or verify the final J/Y, which do not yet exist.

## Implication / challenge

`time-basis=ref-commit` does bind `run-utc` to the commit metadata, but does not establish that metadata as trusted wall-clock provenance. A commit whose committer date was deliberately set 120 seconds into the future passes the not-future criterion at evaluation; after the allowance elapses, the same committed timestamp would fail on re-execution. Therefore the timestamp component is deliberately time-dependent and permits small future-dated metadata. This is a bounded tradeoff, not evidence that a farther-future timestamp passes. It does not falsify the frozen predicate: its explicit 120-second allowance and ref-equality requirement imply precisely this acceptance behavior.

**Impacted axes:** depth:verifiability (timestamp evidence has a bounded, mutable wall-clock acceptance window); coverage (no direct impact found).

**Smallest safe correction:** none required absent a changed frozen claim. If a future claim wants immutable wall-clock provenance, it must define a trusted clock/attestation source or disallow future skew; changing this implementation or claim now would be out of scope.

No tools installed. Disk guard status before probes: /tmp 3%, /var/tmp 35%, /fast/scratch/hyaku 43%. Scratch was removed on command exit.
