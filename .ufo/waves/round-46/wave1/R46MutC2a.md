VERDICT: BROKEN

Scope: mutation test of corpus/instruments/r46-c2-gate.py limbs G1 (frontier table), G2 (entry header, sections, table rows, cross-refs) and G3 (SOURCES.md S073 registry row). Counter file sha256 0ee958578b592370… (first 16 hex), read-only; not edited. Ten single-edit mutants, each applied to a hand-built good tree (pure base export + F28 README row + S073 SOURCES row + entry corpus/knowledge/github-private-vulnerability-reporting.md) that grades 7/7. Rejection = any of G1–G3 prints pass=0.

## Survivors (counter does not reject; defect present, confirmed by an independent oracle)

### S1 — G2 recheck names a source the entry does not cite (counter line 193)
- Edit: entry line 4, `--source S073` → `--source S0730`.
- Counter output: `gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=6 xrefs=2/2`; `c2-gate fixed=7/7 exit=0`.
- Defect oracle: `grep -n '^recheck:' …/mut-g2-recheck-names-wrong-source/corpus/knowledge/github-private-vulnerability-reporting.md` printed `4:recheck: … --source S0730`, and `source-recheck.py --source S0730` printed `S0730:source UNAVAILABLE reason=not-listed` rc=2, while `--source S073` printed `S073:sha256 OK … S073:Q8 OK occurrences=1 anchor=578-ok rc=0`.
- Why: line 193 tests `"--source S073" in h`, a substring test that S0730 satisfies. The counter never executes the entry's own recheck line; G4 runs source-recheck on S073 directly.

### S2 — G2 table-row count accepts a junk row (counter lines 195–196)
- Edit: entry line 19, `| SECURITY.md is separate | S073.txt:564 | Never read a SECURITY.md statement as proof that the form is enabled. |` → `| - | - | - |`.
- Counter output: `gate G2 pass=1 … table-rows=6 …`; `c2-gate fixed=7/7 exit=0`.
- Defect oracle (grep/independent regex): `19:| - | - | - |`; data rows with a pinned anchor = 5 (need 6).
- Why: line 195 counts every three-cell pipe line minus a fixed 2 (header and separator), with no content test. The docstring's "real tables only" hardening (counter lines 8–9) is not enforced.

### S3 — G2 `## Limits` section emptied (counter line 194)
- Edit: the Limits body (all bullets) deleted; heading kept. Entry now reads `35:## Limits` / `36-` / `37-## Falsifiable package rule`.
- Counter output: `gate G2 pass=1 … sections=4/4 …`; `c2-gate fixed=7/7 exit=0`.
- Defect oracle: non-blank lines under `## Limits` = 0.
- Why: line 194 checks heading presence (`^## …\s*$`) only; section content is not graded.

### S4 — G3 registry source cell wraps the canonical URL in another host (counter line 231)
- Edit: SOURCES.md line 79, source cell `— https://docs.github.com/…/report-privately` → `— https://mirror.example.invalid/?u=https://docs.github.com/…/report-privately`.
- Counter output: `gate G3 pass=1 read=row-S073=ok`; `c2-gate fixed=7/7 exit=0`.
- Defect oracle: first URL in the source cell = `https://mirror.example.invalid/?u=https://docs.github.com/...`, not the canonical URL.
- Why: line 231 is `if URL not in row[1]`, a substring test. Counter docstring line 22 says the source cell "holds the canonical URL".

## Caught mutants (rejected=1)

| mutant | target | counter line | defect oracle |
|---|---|---|---|
| g1-dup-frontier-id (F27 row id → F28) | G1 | G1 pass=0 (G1-G3 line: G1:0,G2:0,G3:0; full 2/7) | F-ids=28 duplicate-ids=1 |
| g1-f28-status-proposed | G1 | G1 pass=0 | F28 status cell='proposed' |
| g1-f28-entry-shared-with-f27 | G1 | G1 pass=0 | F27 row mentions F28 entry path=True |
| g1-f28-entry-missing-file | G1 | G1 pass=0 | F28 entry file exists=False |
| g2-xref-line-out-of-range | G2 | G2 pass=0 | out-of-range xrefs=['ai-assisted-finding-validation.md:700'] |
| g3-tier-B | G3 | G3 pass=0 | tier cell='B' |

## Output of the recipe run (verbatim; scratch removed after this report)

```
CONTROL do-nothing (pure base, no F28/S073):
gate G1 pass=0 read=rows=27 admitted=27 dup=0
gate G2 pass=0 read=F28-rows=0
gate G3 pass=0 read=row-S073=absent-or-malformed
gate G4 pass=0 read=manifest-absent
gate G5 pass=0 read=F28-rows=0
gate G6 pass=0 read=knowledge=64 base-names-intact=1 entry-bytes-ok=0
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=1/7 exit=1

== SURVIVORS FIRST (rejected=0, defect present) ==
mutant=g2-junk-table-row rejected=0
mutant=g2-limits-section-emptied rejected=0
mutant=g2-recheck-names-wrong-source rejected=0
mutant=g3-source-url-wrapped-in-other-host rejected=0
== ALL MUTANTS ==
mutant=g2-junk-table-row rejected=0
  target=G2 hunks=1 defect-present=1 oracle: data rows=6 rows-with-pinned-anchor=5 (need 6)
  G1-G3=G1:1,G2:1,G3:1 full=7/7 exit=0
mutant=g2-limits-section-emptied rejected=0
  target=G2 hunks=1 defect-present=1 oracle: non-blank lines under ## Limits=0
  G1-G3=G1:1,G2:1,G3:1 full=7/7 exit=0
mutant=g2-recheck-names-wrong-source rejected=0
  target=G2 hunks=1 defect-present=1 oracle: entry recheck names source=S0730 (entry source is S073)
  G1-G3=G1:1,G2:1,G3:1 full=7/7 exit=0
mutant=g3-source-url-wrapped-in-other-host rejected=0
  target=G3 hunks=1 defect-present=1 oracle: first URL in source cell=https://mirror.example.invalid/?u=https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately
  G1-G3=G1:1,G2:1,G3:1 full=7/7 exit=0
mutant=g1-dup-frontier-id rejected=1
  target=G1 hunks=1 defect-present=1 oracle: F-ids=28 duplicate-ids=1
  G1-G3=G1:0,G2:0,G3:0 full=2/7 exit=1
mutant=g1-f28-entry-missing-file rejected=1
  target=G1 hunks=1 defect-present=1 oracle: F28 entry file=github-private-vuln-reporting.md exists=False
  G1-G3=G1:0,G2:0,G3:0 full=2/7 exit=1
mutant=g1-f28-entry-shared-with-f27 rejected=1
  target=G1 hunks=1 defect-present=1 oracle: F27 row mentions F28 entry path=True
  G1-G3=G1:0,G2:0,G3:0 full=2/7 exit=1
mutant=g1-f28-status-proposed rejected=1
  target=G1 hunks=1 defect-present=1 oracle: F28 status cell='proposed'
  G1-G3=G1:0,G2:1,G3:1 full=6/7 exit=1
mutant=g2-xref-line-out-of-range rejected=1
  target=G2 hunks=1 defect-present=1 oracle: out-of-range xrefs=['ai-assisted-finding-validation.md:700']
  G1-G3=G1:1,G2:0,G3:1 full=6/7 exit=1
mutant=g3-tier-B rejected=1
  target=G3 hunks=1 defect-present=1 oracle: tier cell='B'
  G1-G3=G1:1,G2:1,G3:0 full=6/7 exit=1
CONTROL good (unmutated) G1-G3: {'G1': 1, 'G2': 1, 'G3': 1} rejected= 0
```

Good-tree control (unmutated), full run, as printed by the same counter: `gate G1..G7 pass=1` and `c2-gate fixed=7/7 exit=0`.

## Mutant edits (old → new, each one hunk, applied to the good tree)

1. g1-dup-frontier-id, corpus/README.md: `| F27 | Linux kernel` → `| F28 | Linux kernel`
2. g1-f28-status-proposed, README: `| admitted | \`corpus/knowledge/github-private` → `| proposed | …`
3. g1-f28-entry-shared-with-f27, README: F27 entry cell gains `, \`corpus/knowledge/github-private-vulnerability-reporting.md\``
4. g1-f28-entry-missing-file, README: F28 entry path `github-private-vulnerability-reporting.md` → `github-private-vuln-reporting.md`
5. g2-recheck-names-wrong-source, entry: `--source S073` → `--source S0730` (SURVIVES)
6. g2-limits-section-emptied, entry: Limits body → blank (SURVIVES)
7. g2-junk-table-row, entry: `| SECURITY.md is separate | … |` → `| - | - | - |` (SURVIVES)
8. g2-xref-line-out-of-range, entry: `ai-assisted-finding-validation.md:7` → `:700`
9. g3-source-url-wrapped-in-other-host, SOURCES.md S073 source cell: canonical URL wrapped as `https://mirror.example.invalid/?u=<URL>` (SURVIVES)
10. g3-tier-B, SOURCES.md S073: `| docs | A | GitHub's own` → `| docs | B | GitHub's own`

## Limitations
- Ten mutants, each one hunk. This is a sample of G1–G3 defect classes, not an exhaustive enumeration; no mutant was run against G4–G7 except as reported in the full-counter columns.
- The good tree is my own hand-built fixture (F28 row, S073 row, entry written in scratch), not the executor's or scribe's draft. It is a structural control only; the 7/7 result says the counter accepts that fixture, not that the entry is good.
- Oracles are independent predicates written in the recipe (not the counter's code). The S1 oracle ran source-recheck.py directly; the other oracles are structural text checks.
- Code-read suspicions I did not run (stated as [INFERENCE]): line 232 `p not in row[10]` (used-by is a substring test); line 160 `m[0] in r[3]` (shared-entry check is a substring test); line 141 `^ {0,3}## Registry\b` would also accept a heading such as `## Registry-retired`.
- Frozen controls read, not re-graded here: .ufo/waves/round-46/controls/freeze-controls.txt shows `c2 junk-row … c2-gate fixed=4/7 exit=1` and `c2 uncited-filler … fixed=5/7` (controls not ours to re-derive).
- Environment: no git or jj command was run; no edit to the counter, the lane tree, the fleet repo, MANIFEST.json, .ufo/state or ~/Projects/shokuknow; no installs (pacman paused host-wide; none needed). Scratch under $HYAKU_SCRATCH (default /fast/scratch/hyaku/kasegi-r46/R46MutC2a), TMPDIR set to its tmp/ subdirectory, removed on exit.

Recommended counter change (for the L1; not applied here): grade G2 recheck by parsing the `--source` token exactly and running it; grade the table by requiring a pinned anchor in each counted row; grade each section by non-blank body; grade G3 source cell by the first URL token equal to the canonical URL.
