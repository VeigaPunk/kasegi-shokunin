# R47ExecGateReplay — counter before-value replay

## Result

Axes: depth:verifiability; coverage. The base export reproduces the frozen before-values. The lane working tree does **not** match the specified C1 do-nothing before-value: it has two passing limbs (L7, L11), while the requested expectation was 0/11 fixed. C2 matches the stated base and working-tree values.

Commands were run against a read-only `git archive fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8` export in `/fast/scratch/hyaku/kasegi-r47/R47ExecGateReplay`, then the lane working tree. Both counter instruments were taken from the lane path. Scratch was removed on command exit. No files outside this findings file and scratch were written; no git/jj mutation was performed.

## Exact counter output

C1 base (`--root <base-export> --baseline <base-export>`):

```text
limb L1 (D5) fixed=0 read=scaffold-phrases=4
limb L2 (D5) fixed=0 read=bad=fence-markers=4,search-log-bullet-absent,s074-row-bullet-absent,capture-note-bullet-absent
limb L3 (D5) fixed=0 read=corrections-section-absent
limb L4 (D6) fixed=0 read=false-phrases=2
limb L5 (D6) fixed=0 read=order-phrase-still-present
limb L6 (D6) fixed=0 read=two-cases-absent
limb L7 (D6) fixed=0 read=dropped-findings-unnamed
limb L8 (D7) fixed=0 read=row-S076=absent-or-duplicated hits=0
limb L9 (D7) fixed=0 read=old-citations=59
limb L10 (D8) fixed=0 read=rest-api-lead-bullet-absent
limb L11 (D8) fixed=0 read=round-47-lesson-absent
routed-defects total=11 fixed=0 unresolved=11 exit=1
process_exit=1
```

C2 base (`--root <base-export>`):

```text
gate H1 pass=0 read=rows=29 admitted=29 dup=0
gate H2 pass=0 read=entry-absent zdi-named=
gate H3 pass=0 read=row-S075=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=0 read=manifest-absent
gate H5 pass=0 read=entry-absent zdi-named=
gate H6 pass=0 read=entry-absent zdi-named=
gate H7 pass=1 read=census-rc=0 ok-line=1
f30-gate fixed=1/7 exit=1
process_exit=1
```

C1 working tree (`--root <lane> --baseline <lane>`):

```text
limb L1 (D5) fixed=0 read=scaffold-phrases=4
limb L2 (D5) fixed=0 read=bad=fence-markers=4,search-log-bullet-absent,s074-row-bullet-absent,capture-note-bullet-absent
limb L3 (D5) fixed=0 read=corrections-section-absent
limb L4 (D6) fixed=0 read=false-phrases=2
limb L5 (D6) fixed=0 read=order-phrase-still-present
limb L6 (D6) fixed=0 read=two-cases-absent
limb L7 (D6) fixed=1 read=dropped-findings-named in=corpus/lessons/round-47.md
limb L8 (D7) fixed=0 read=row-S076=absent-or-duplicated hits=0
limb L9 (D7) fixed=0 read=old-citations=59
limb L10 (D8) fixed=0 read=rest-api-lead-bullet-absent
limb L11 (D8) fixed=1 read=zdi-reservation=1 s068-precision=1
routed-defects total=11 fixed=2 unresolved=9 exit=1
process_exit=1
```

C2 working tree (`--root <lane>`):

```text
gate H1 pass=0 read=rows=29 admitted=29 dup=0
gate H2 pass=0 read=entry-absent zdi-named=
gate H3 pass=0 read=row-S075=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=1 read=recheck-rc=0 quotes-ok=10 frozen-cores-missing=0
gate H5 pass=0 read=entry-absent zdi-named=
gate H6 pass=0 read=entry-absent zdi-named=
gate H7 pass=1 read=census-rc=0 ok-line=1
f30-gate fixed=2/7 exit=1
process_exit=1
```

## Interpretation and limits

The base export is the do-nothing control: C1 0/11 and C2 1/7, as specified. The working-tree C1 output contradicts the seat card's asserted C1 fixed=0 expected reading; two existing working-tree changes are recognized by the counter (L7 and L11). Working-tree C2 is exactly the specified freeze-tree 2/7. None of these readings claims closure: C1 has 9 unresolved, and C2 has 5 failing gates. I did not run the mutation battery or any build, tests, lint, or formatter. The full counter output above is the evidence; counter output itself provides no file:line citations.
