# MutC1B2 — C1 mutant-B2 probe

**Axes:** depth:verifiability; coverage. **Target:** remove only the Q9/B2 non-unique-occurrence/anchor rejection from an isolated scratch copy of `source-recheck.py`.

## Digest and detector

The digest poll log (`c1-controls/mutants/digest-poll.log`) records the instrument update at 18:50:40 (`source-recheck.py` `0b841d5d…`). At probe time the working instrument's actual SHA-256 was `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f` (the poll digest no longer matched current bytes); I used and recorded those actual bytes, without editing the shared instrument. The bounded detector was `python3 <scratch checker> --manifest <B2 manifest> --source S045`.

The frozen B2 manifest names record `S045` but points to `B2.txt`, whose stem is not `S045`. Against the unmodified frozen fixture the pristine checker exits 1 with `S045:manifest MISMATCH reason=stem-mismatch`; B1 intercepts the case before B2, so that run alone is **inconclusive** for B2. To isolate B2 without changing the frozen control, I made a scratch-only copy of `B2.txt` named `S045.txt` (same SHA-256 `55124b0e96417204cddc4de64e55058ab9ae4c9e00b50ee1f8c704f1f6d5fb06`) and a scratch manifest changing only its path. The corrected manifest/capture stay under `c1-controls/mutants/mutant-b2/`.

## Receipts and verdict

| State | Checker SHA-256 | Actual output | Exit |
|---|---|---|---:|
| Pristine scratch copy | `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f` | `S045:sha256 OK` / `S045:Q1 MISMATCH reason=occurrence-not-unique` | 1 |
| Mutant: removed lines 190–200 (B2 rejection and its reason mapping only) | `e12c8c7561de752f40605f78f304904de4117dc0c4e7e448b3f3544c09117db0` | `S045:sha256 OK` / `S045:Q1 OK occurrences=2 anchor=MISSING` | 0 |
| Restored scratch copy | `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f` | `S045:sha256 OK` / `S045:Q1 MISMATCH reason=occurrence-not-unique` | 1 |

The mutant produces the requested flip: exit 0 with `occurrences=2` and no verified anchor. **Verdict: B2 limb behaviorally demonstrated; mutant survives the fixture as an ordinary test mutant (the fixture goes green when the guard is removed).** The frozen fixture itself remains an additional coverage finding: it fails at stem validation instead of reaching B2.

## Restoration evidence

The shared `corpus/instruments/source-recheck.py` was never mutated; its SHA-256 remained `33602a9d…` across the probe. The scratch checker was restored by copying those exact instrument bytes back: scratch and shared checker hashes match at `33602a9d…`; restored run returns the pristine B2 failure above. The frozen manifest was restored to its original `path: B2.txt` bytes (SHA-256 `3a13e5c32995ca57f8a72fcc99f9f1672c1a140411e10a092f2fb5567e42dfc1`; `cmp` against an independently reconstructed no-final-newline copy exited 0). The frozen capture was unchanged by construction and hash-matches the scratch copy. All scratch artifacts and this report are within the lane; no tool installed.
