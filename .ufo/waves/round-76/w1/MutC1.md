# MutC1 — mutation battery on the amended recheck-cwd census candidate (round 76, attempt 1)

Verdict: **NOT RUN — blocked on missing candidate.** No mutant was generated, applied or scored. No kill/survive verdict is claimed for any mutant in this report.

## Blocker

- Required input `.ufo/waves/round-76/w1/ExecC1Amend.patch` is absent.
  - Command: `ls -la <lane>/.ufo/waves/round-76/w1/ExecC1Amend.patch` → `No such file or directory`, rc=2.
  - Checked once, after scratch setup, as the spec requires (no wait-loop). The w1 directory at that time held only `ScribeEntry-recheck-S111.txt` and `swarm-registry.json`.
- Without the amended bytes there is no baseline to run (the spec's baseline is the unmutated candidate), so none of M1–M6 or the two design mutants can be executed against the candidate.

## What was verified (read-only)

- Base bytes export: `git -C <lane> show 5da54cd4451cbbb9e4b87e2f83475feb13c65c9e:corpus/instruments/recheck-cwd-census.py > <scratch>/base.py` → rc=0.
  - `sha256sum base.py` → `e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a` (matches the C1 base hash in `claims.json`).
  - `wc -l base.py` → 281 lines.
- `controls/mut/README.md` read: the three committed red-before mutants (m1-forged-relabel, m2-result-limb-removed, m3-restoration-forces) are base-counter mutants and were not re-run here; they are the input to the amended-selftest kill check that the candidate owner must run, not something this seat can substitute for it.
- `claims.json` read in full (C1 predicates A1–A5, C2 predicates B1–B7); no predicate text was altered.

## Mutant table

| id | mutant | patch | baseline rc | mutant rc | verdict |
|---|---|---|---|---|---|
| M1 | neither-header files counted as restoration_only | not generated (no candidate) | not run | not run | not run |
| M2 | case-6 RESULT limb computation removed | not generated | not run | not run | not run |
| M3 | restoration-recheck presence alone forces restoration_only | not generated | not run | not run | not run |
| M4 | RESULT gate drops `norecheck == 0` | not generated | not run | not run | not run |
| M5 | case 8 marker-absent conjunct removed | not generated | not run | not run | not run |
| M6 | selftest print literal stays `cases=6` while eight cases run | not generated | not run | not run | not run |
| D1 (design) | both-headers fixture: `restoration-recheck:` precedence forces restoration_only (inverts the case-8 classification) | not generated | not run | not run | not run |
| D2 (design) | RESULT line reports `restoration_only` value in the `norecheck` slot (tally swap on the new neither-header bucket) | not generated | not run | not run | not run |

No mutant directory `w1/mutc1-mutants/` was created: there are no mutant files to store, and I did not write placeholder files.

## Notes for the candidate owner / L1

- The candidate owner should commit the amended bytes and the patch file to `w1/ExecC1Amend.patch` before the battery can run. The battery then needs: one baseline run per candidate state, one `find->replace` patch per mutant applied to a fresh copy of the amended bytes, and the verdict rule from the spec (killed only on nonzero exit, `failures>0`, or changed tally; `invalid:*` for patch-not-applicable, byte-identical noop, nocompile, or 120 s timeout).
- Pre-battery sanity that is possible now without the candidate: the committed base mutants (`controls/mut/m1..m3`) should each produce `selftest cases=6 failures=0` rc=0 against the base counter. I did not run this (out of scope for a seat that must not score the control; it is recorded in `controls/c1-redbefore-mutant-survival-r76.txt` already).
- Coverage/denominator note: C1 is judged on depth:verifiability; without any executed mutant there is no depth evidence from this seat.

## Scratch and cleanup

- Scratch: `/fast/scratch/hyaku/kasegi-r76/MutC1/` (holds only the exported `base.py`). Removed before yield.
- No writes to the lane tree other than this report. No git mutating commands run. No network access.
