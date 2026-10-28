VERDICT: BROKEN

Scope: C1 limb L2 of corpus/instruments/r46-c1-gate.py (regrounded set R = gated(BASE) - gated(TREE), |R| >= 2 and gated(TREE) = gated(BASE) - |R|, no new gated), attacked on a scratch export of the frozen base. Tree = /fast/scratch/hyaku/kasegi-r46/L1/pure copied, with the counter copied in (sha256 b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294, identical to the lane file). Baseline = a copy of the same export. Scratch removed on exit.

## Finding 1 (BROKEN): L2 reads pass=1 with two literal `true` recheck lines, no re-grounding

Cheapest recipe: in the tree copy, replace the single `recheck:` line of corpus/knowledge/claim-gates.md and corpus/knowledge/claim-package-contract.md with `recheck: true`. Nothing else changes. Run:

    python3 <tree>/corpus/instruments/r46-c1-gate.py --root <tree> --baseline <base>

Printed (verbatim):

    gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
    gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
    gate L3 pass=0 read=bad=claim-gates.md,claim-package-contract.md
    gate L4 pass=0 read=bad=claim-gates.md,claim-package-contract.md
    gate L5 pass=0 read=bad=claim-gates.md,claim-package-contract.md
    gate L6 pass=0 read=mutants=0 survivors=none
    gate L7 pass=1 read=still-gated=22 changed=none
    c1-gate fixed=3/7 exit=1

The line `gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md` is the limb being fooled: no row, no section, no anchor was added. This matches the freeze control `c1 marker-only` in .ufo/waves/round-46/controls/freeze-controls.txt (same L2 line, fixed=3/7), so the control is reproduced and not a new effect.

Do-nothing discriminator (same command on the untouched tree):

    gate L2 pass=0 read=base-gated=24 regrounded=0 
    c1-gate fixed=1/7 exit=1

## Finding 2 (BROKEN): L2 is equally fooled by other non-re-grounding trees (all reproduced)

Each run used the same command; the L2 and composite lines printed:

- A2 softened in-tree test: the two lines replaced by `recheck: test -d corpus/knowledge`.
  `gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md`; `c1-gate fixed=3/7 exit=1`
- A3 borrowed executing line: the two lines replaced by the verbatim executing recheck line of claim-package-gate.md (copied, not moved).
  `gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md`; `c1-gate fixed=3/7 exit=1`
- A4 header-only fake section: an empty `## Re-ground (round 46)` header appended to the two entries and their lines replaced by `recheck: grep -qxF '## Re-ground (round 46)' corpus/knowledge/<entry>`. No rows.
  `gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md`; `gate L5 pass=1 read=append-only=2`; `c1-gate fixed=4/7 exit=1`

So L2 accepts any construction that makes two gated lines exit 0. It cannot tell re-grounding from line softening, which is the reason it is not load-bearing as a standalone limb. The composite still catches A2-A4 (3/7 and 4/7), via L3 (no `--entry` self-check) and L4/L6 (no section to run).

## Finding 3 (not a bypass, recorded): HOME override does not move L2, and it moves L1 alone

Assignment's suggested construction: create `Projects/bounties` under a scratch HOME and run the counter with that HOME:

    HOME=/fast/scratch/hyaku/kasegi-r46/R46RevC1L2/home python3 <tree>/corpus/instruments/r46-c1-gate.py --root <tree> --baseline <base>
    gate L1 pass=1 read=gated=10 broken=0 lines=64/base=64
    gate L2 pass=0 read=base-gated=10 regrounded=0 
    c1-gate fixed=2/7 exit=1

- L2 fails: the counter classifies the BASE under the same process environment, so the baseline's `test -d ~/Projects/bounties` also flips. R = 0. The HOME override cannot create R in isolation.
- L1 passes with zero edits to the tree: gated drops 24 -> 10 only because the grader's bash sees a different HOME. L1 is environment-dependent, and it can pass alone under a HOME that contains the tested directories. This is a limb-level defect of L1 in the same counter, not of L2.

## Finding 4 (fail-alone): L2 can fail alone; the construction needs three well-formed re-grounds plus one new gated line

Analysis: with |R| <= 1, gt = gb - |R| >= 23 and L1 fails too, so L2 cannot fail alone that way. L2 fails alone only through the third clause: n >= 1 new gated lines with |R| >= 2 + n so that L1 still reads gated <= 22.

Constructed tree (B): three entries (claim-gates.md, claim-package-contract.md, ev-model.md) re-grounded with six MECHANICAL rows each (tokens copied from corpus/instruments/r46-c1-gate.py:55,56,57,60,62 and corpus/instruments/anchorcheck.py:138; recheck `cd . && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<e>.md`), plus claim-package-gate.md's `test -s corpus/knowledge/claim-package-gate.md` changed to `test -s corpus/knowledge/no-such-r46.md` (executes at base -> gated, n=1).

    gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
    gate L2 pass=0 read=base-gated=24 regrounded=3 claim-gates.md,claim-package-contract.md,ev-model.md
    gate L3 pass=1 read=recheck-lines-clean=3
    gate L4 pass=1 read=entry-mode-green=3
    gate L5 pass=1 read=append-only=3
    gate L6 pass=1 read=mutants=18 survivors=none
    gate L7 pass=1 read=still-gated=21 changed=none
    c1-gate fixed=6/7 exit=1

Answer: yes, L2 can fail alone, and only in this way (n new gated lines, with >= 3 R entries). Mechanically, it is load-bearing only through the "no new gated" clause; its |R| >= 2 clause is subsumed by L1 at base 24.

## Finding 5 (composite, out of limb scope but decisive for C1): the counter reads 7/7 exit=0 on content-free rows

Same tree as Finding 4, with claim-package-gate.md restored to its base bytes (the new gated line removed):

    gate L1 pass=1 read=gated=21 broken=0 lines=64/base=64
    gate L2 pass=1 read=base-gated=24 regrounded=3 claim-gates.md,claim-package-contract.md,ev-model.md
    gate L3 pass=1 read=recheck-lines-clean=3
    gate L4 pass=1 read=entry-mode-green=3
    gate L5 pass=1 read=append-only=3
    gate L6 pass=1 read=mutants=18 survivors=none
    gate L7 pass=1 read=still-gated=21 changed=none
    c1-gate fixed=7/7 exit=0

The rows in those entries say only `| G1 | mechanical row 1 | ...`. The counter accepts them. It cannot grade content; C1's kill rule (non-author reading of the rows) is the only check that would catch this. So a "7/7 exit=0" from the counter alone is not evidence that C1's claim holds.

## Constructions tried (for the 'HOLDS' criterion, which is NOT met)

1. literal `true` on two recheck lines — L2 pass=1 (BYPASS)
2. in-tree softened test `test -d corpus/knowledge` — L2 pass=1 (BYPASS)
3. borrowed executing recheck line from another entry (copy) — L2 pass=1 (BYPASS)
4. empty section header + `grep -qxF` on it — L2 pass=1 (BYPASS)
5. HOME override with ~/Projects/bounties created — L2 pass=0 (defeated: base measured in the same env); L1 pass=1 (side effect)
6. swap of claim-gates.md's gated line with claim-package-gate.md's executing line — L2 pass=0 (regrounded=1, L1 fails)
7. three mechanical re-grounds + one new gated line — L2 pass=0 alone (fixed=6/7) (fail-alone)
8. three mechanical re-grounds, no new gated — fixed=7/7 exit=0 (composite content-free pass)

## Limitations

- Trees are a copy of the frozen base export (pure), not the freeze commit 9f23aab4 tree; no git was run. The freeze tree equals base for the counter (as claimed in claims.json C1 freeze_tree_reading), and my do-nothing run reproduces the freeze control `c1 do-nothing` line.
- All trees ran with HOME=/home/vgpnk (the grader's HOME in this shell) except the HOME-override run, which used a scratch HOME holding only Projects/bounties. The real HOME was not modified (verified: /home/vgpnk/Projects/bounties does not exist; no file written there).
- Findings 4 and 5 use mechanically generated rows; they demonstrate what the counter accepts, not any real re-ground's support of its claims.
- I did not test the other six limbs beyond the observed lines; I did not run recheck-audit.py, score-gap.py, or any C2 counter.
- Tooling: no tools were installed; python3 stdlib only; the counter file was used as-is (sha256 unchanged).
- Scratch: /fast/scratch/hyaku/kasegi-r46/R46RevC1L2 removed on exit (rm -rf after the report was written).

No commit, push, git mutation, or edit to any tracked file was made. The only write is this Report file.
