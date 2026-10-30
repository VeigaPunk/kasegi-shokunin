# R47MutC1a — C1 counter-source mutations, limbs L1–L6

Axes: depth:verifiability and coverage. Result: **6 novel single-edit mutants: 1 caught, 5 surviving and demonstrably non-equivalent.** The requested caught-or-equivalent condition is NOT met. These are additional disclosed selftest coverage gaps, not equivalent mutants and not repaired production behavior.

All paths below are lane-relative unless absolute. Evidence bundle: `.ufo/waves/round-47/w1/R47MutC1a.draft/`.

## Method and do-nothing control

Read-only base export: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8 corpus`, extracted only under `/fast/scratch/hyaku/kasegi-r47/R47MutC1a/base`. No wave history was copied. Scratch instruments included a byte-identical gate copy and the committed sibling `source-recheck.py`, preserving L8 helper resolution.

For EACH mutant, ran the identical bounded detector on pristine, mutated, then exactly restored gate bytes:

```text
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r47-counters-selftest.py --base /fast/scratch/hyaku/kasegi-r47/R47MutC1a/base --work /fast/scratch/hyaku/kasegi-r47/R47MutC1a/work-<ID>-<phase> --counter c1 --gate /fast/scratch/hyaku/kasegi-r47/R47MutC1a/instruments/gate.py
```

Each `<ID>-<phase>.txt` retains the actual command, complete stdout/stderr and process exit. Pristine and restored phases are the do-nothing controls; all twelve printed `selftest cases=20 failures=0 exit=0` and process exit 0. An edit was asserted to replace exactly one occurrence (L1 scoped to its function).

Novelty: compared exact old/new edits against `corpus/instruments/r47-mutbat.py:51-70`. None is in that table: A2 drops a section boundary rather than disabling the registry check; A3 changes heading termination rather than dropping content conjuncts; A4 widens a regex rather than ignoring chrome; A5 keeps a prefix requirement rather than eliminating the requirement; A6 changes newline matching rather than eliminating the three-cases check.

## Actual detector verdicts

| ID / limb | Single counter-source edit | Pristine failures | Mutated output | Restored failures | Verdict |
|---|---|---:|---|---:|---|
| A1 / L1 | `if p in t]` → `if p in t.lower()]`, only in L1 | 0 | `selftest cases=20 failures=1 exit=1` | 0 | caught |
| A2 / L2 | `search = section(raw, "Search log")` → `search = raw` | 0 | `selftest cases=20 failures=0 exit=0` | 0 | survived, non-equivalent |
| A3 / L3 | `r"^## Corrections \(round 47\)\s*$"` → `r"^## Corrections \(round 47\)\s*"` | 0 | `selftest cases=20 failures=0 exit=0` | 0 | survived, non-equivalent |
| A4 / L4 | `r"\bchrome\b"` → `r"chrome"` | 0 | `selftest cases=20 failures=0 exit=0` | 0 | survived, non-equivalent |
| A5 / L5 | required `CVE request before the fix-version` → required `CVE request` | 0 | `selftest cases=20 failures=0 exit=0` | 0 | survived, non-equivalent |
| A6 / L6 | `r"three cases[^.]*let a maintainer publish"` → `r"three cases[^.\n]*let a maintainer publish"` | 0 | `selftest cases=20 failures=0 exit=0` | 0 | survived, non-equivalent |

Receipt: `.ufo/waves/round-47/w1/R47MutC1a.draft/receipt.txt:1-18`.

A1's discriminating detector case printed:

```text
case c1-s1left ok=0 want=L1 red + exit!=0 got=routed-defects total=11 fixed=11 unresolved=0 exit=0
```

Evidence: `.ufo/waves/round-47/w1/R47MutC1a.draft/A1-L1-lowercase-haystack-mutated.txt:19-22`.

## Non-equivalence witnesses (not equivalence waivers)

Built separate witness trees using the committed selftest's `build_c1_green` builder. Ran the targeted predicate from pristine and mutated gate copies over the SAME witness. These predicate-level results establish non-equivalence; they are not claimed as complete counter passes.

| Mutant | Witness change to green fixture | Actual pristine result | Actual mutant result |
|---|---|---|---|
| A1 | Append `The \`## Search log\` bullet to append` to SOURCES.md | `false, scaffold-phrases=1` | `true, scaffold-phrases=0` |
| A2 | Move the F29 Search-log bullet to EOF, under Registry changes, retaining every bullet's bytes | `false, bad=search-log-bullet-absent` | `true, bullets-landed fences=0` |
| A3 | Change heading to `## Corrections (round 47) withdrawn` | `false, corrections-section-absent` | `true, corrections-section-present content=1` |
| A4 | Replace whole-word `chrome` with `chromeless` throughout the entry | `false, chrome-note-absent` | `true, prose-claims-corrected chrome=present` |
| A5 | Replace `CVE request before the fix-version` with `CVE request after the fix-version` | `false, corrected-order-sentence-absent` | `true, order-claim-corrected` |
| A6 | Append `three cases` followed by newline then `let a maintainer publish` | `false, three-cases-still-present` | `true, fix-version-cases-corrected` |

Exact edit strings and witness return values: `R47MutC1a.draft/A1-L1-lowercase-haystack.json` through `A6-L6-newline-blind.json`; consolidated `R47MutC1a.draft/results.json`.

Recommended detector additions: displaced Search-log bullet; corrections heading with trailing disqualifier; chrome substring without whole-word note; reversed CVE order without the historical false phrase; multiline three-cases assertion. No detector or corpus edits were made.

## Hashes and restoration

Pristine scratch gate, restored scratch gate after EACH mutation, and production counter before/after all share SHA-256:

```text
e6ede7b668155fc173ad9a1c0f83168f173d6c31b12ecb85da406e1660424aee
```

Mutated gate SHA-256 values:

```text
A1 a5551accd69061949238c4e60e5991533a0aaeb4fe50835981d3e599aac5790a
A2 57f08d30b3bdb1f5d0cb8618402510e5b90b5512eeefcba19ffb992f22a6277b
A3 6b209f599d2574bd01b75cb6656ae41aa6c26efcfd517d10cbc998675dec8fcd
A4 b8739d2babeb7eaad613782c95e8654e3eafdedfb25512a6729585ec50f1570f
A5 4166aeea80376d3399d915d0c45d6c4676d2162d2c923a783a439f37148e5534
A6 3db7acd0c6f454bb62921cdc8040c78020a63eae1d9e2a7cc6a2fe2fa9b9282b
```

Full before/mutated/restored hashes are in `results.json`. Gate restoration occurred in `finally`; the outer `finally` removed the entire scratch directory after copying receipts. `R47MutC1a.draft/cleanup.txt:1-2` records `scratch_exists=False` and the unchanged production SHA.

## Limits and operational notes

- This bounded C1 probe does not replace or rerun the full battery, the 43-case combined tree selftest, C2, or wave-2 integration attacks. Existing disclosed 34 battery survivors remain outside this probe; no zero-survivor claim is made.
- Five new survivors are genuinely non-equivalent by the witnesses above; calling them equivalent would be false. No production fixes or integration decisions are claimed.
- Disk guard printed `/fast/scratch/hyaku 54% 375.1G free`, `/tmp 25% 96.7G free`, `/var/tmp 41% 532.8G free`; its top-consumer enumeration timed out after 15 seconds. No heavy/full battery ran.
- One setup invocation failed before executing because its scratch cwd did not yet exist; setup then succeeded from existing `/fast/scratch/hyaku`. No failed baseline was counted as a killed mutant.
- No commits, index mutation, tool installation, shared-file changes, delegation or explicit background jobs. The tool wrapper automatically backgrounded the disk-guard call before delivering its timeout result.

Self-evaluation (accuracy/completeness/clarity/actionability/conciseness): 4/4/4/4/4, average 4.0. Evidence: preserved complete detector outputs and restoration hashes; all six requested limbs probed. Limits: predicate witnesses are not full-counter runs, and the requested caught-or-equivalent outcome is disproved rather than achieved. Highest-impact improvement is adding the five witness classes to the detector through the integration owner, not relabeling survivors. Would the user agree: likely, because gaps are explicit and reproducible.
