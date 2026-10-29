VERDICT: BROKEN

Seat R46bRevPriorEscapes — regression guard, round 46 attempt 2. Rebuilt two of the prior attempt's wave-1
falsifier trees against the CURRENT v1.2 counters (tip 04af9bc92229232ea5cce8b32bfe59dd969eb26d, exported to
scratch) and re-ran the old recipes. Result: the C1 rebuild now reads red (hole closed), the C2 rebuild still
reads green (regression finding, Finding 1). Raw receipts: .ufo/waves/round-46/attempt2/wave1/R46bRevPriorEscapes.draft/.

Counter lineage (evidence: R46bRevPriorEscapes.draft/counter-lineage.txt): the wave-1 falsifier reports attacked
v1 (attempt-1 freeze shas c1 b0c730c8…, c2 0ee95857…); rev 5437afe (R46RevC1L3's verdict rev) carries v1.1
(errata E1); rev 93140c1 (R46MutC2a's verdict rev) and the tip 04af9bc carry v1.2 (errata E2), byte-identical to
the working tree. Errata E1 cites wave1/R46RevC1L3.md as the forcing report for C1-E1 (L3) and wave1/R46MutC2a.md
S1–S4 for C2-E1/E2 — the two reports rebuilt here.

================================================================================
FINDING 1 (REGRESSION) — rebuilt R46MutC2a S2 "junk filler row" tree grades 7/7 on r46-c2-gate.py v1.2
================================================================================

Built: tree = `git -C <lane> archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus | tar -x` (the integrated
tip tree), one edit to corpus/knowledge/github-private-vulnerability-reporting.md: the SECURITY.md data row
(line 18, the row citing S073.txt:564 — the same semantic site as the old recipe's line-19 row
`| SECURITY.md is separate | S073.txt:564 | … |`) replaced with `| - | - | - |`. This is the old S2 recipe:
a junk filler row in the entry's cited table.

Do-nothing control (tip export, unedited), command
`TMPDIR=$S/tmp python3 $S/c2tree/corpus/instruments/r46-c2-gate.py --root $S/c2tree`:

    gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 anchored=1 table-rows=8 xrefs=4/4
    …
    c2-gate fixed=7/7 exit=0

Mutant tree (single junk row), same command — reads GREEN:

    gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 anchored=1 table-rows=7 xrefs=4/4
    gate G3 pass=1 read=row-S073=ok
    gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
    gate G5 pass=1 read=spans=26 located=26 failed=0 uncited=0 cores=5/5
    gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
    gate G7 pass=1 read=census-rc=0 ok-line=1
    c2-gate fixed=7/7 exit=0

The old report's reading of this construction at v1 (quoted from wave1/R46MutC2a.md S2): "gate G2 pass=1 …
table-rows=6 …; c2-gate fixed=7/7 exit=0", oracle "data rows with a pinned anchor = 5 (need 6)". The tree-level
verdict reproduces verbatim at v1.2.

Mechanism (why it is still green). E1's fix works as documented: a junk row no longer COUNTS toward the table
floor — r46-c2-gate.py:212-218 counts only 3-cell lines whose cells each hold >= 2 words AND carry a located
S073.txt:N cite inside lines 556-583, and r46-c2-gate.py:236 conjuncts `tbl >= 6`. The junk row is excluded
(table-rows fell 8 → 7, not 8). But the gate polices non-counted rows not at all, the committed counter sets
PINS["entry"] = None (r46-c2-gate.py:62 — entry bytes are graded structurally, never pinned, per errata C2-E6),
and the tip entry's table has 8 real rows, i.e. 2 rows of slack above the floor. Net: the exact falsifier tree
— an entry carrying a junk filler row in its cited table, grading 7/7 — still passes.

Boundary (same tree, rows 17/18 then 19 also junked to `| - | - | - |`; receipts c2-junk-boundary.txt):

    two junk rows:   gate G2 pass=1 … table-rows=6 …  c2-gate fixed=7/7 exit=0
    three junk rows: gate G2 pass=0 … table-rows=5 …  c2-gate fixed=6/7 exit=1

Independent oracle on the three-junk entry (mirrors the wave-1 oracle): "data rows with pinned anchor in body
556-583 = 5 (need 6)". So v1.2 tolerates exactly (counted real rows − 6) junk rows in a table; the third junk
row is the first that tips the real count below the floor.

Severity: MEDIUM. This is a hardening residual, not a verdict-forgery path: junk rows carry no claims, G5 still
grades every quoted span, and junk cannot make an unsound entry pass — it is tolerated decoration in an otherwise
sound entry. But the seat criterion is tree-level ("any tree that now reads green is a regression finding"), and
the prior falsification's demonstrated verdict — defective tree, 7/7 — reproduces. The E1 erratum closed the
mechanism (junk no longer counts) without closing the verdict; whether the frozen C2 kill rule is violated is
the L1's call (a junk-carrying entry is arguably still "a real table" under the docstring's own G2 sentence,
r46-c2-gate.py:18 "a >= 6-row table whose cells each hold >= 2 words", since the counted 7 rows satisfy it).

================================================================================
FINDING 2 (no regression) — rebuilt R46RevC1L3 Finding-1 tree reads red on r46-c1-gate.py v1.2
================================================================================

Built: tree = copy of /fast/scratch/hyaku/kasegi-r46/L1/pure2 (the attempt-2 designated base export, round-15
914ca0b corpus; claim-gates.md is 125 lines with the recheck at :125, the same recipe site as the old run) plus
the current v1.2 r46-c1-gate.py. Mutant = the old Finding-1 recipe: corpus/knowledge/claim-gates.md:125 replaced
with `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && true  # r46-c1-gate.py --entry
corpus/knowledge/claim-gates.md`. Command for both runs:
`TMPDIR=$S/tmp python3 $S/c1tree/corpus/instruments/r46-c1-gate.py --root $S/c1tree --baseline /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work $S/tmp`

Do-nothing control (unedited tree), prints (receipt c1-control.txt):

    gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64
    gate L2 pass=0 read=base-gated=24 regrounded=0
    gate L3 pass=0 read=recheck-lines-exact=0
    gate L4 pass=0 read=entry-mode-green-anchors-unchanged=0
    gate L5 pass=0 read=append-only-restoration-kept=0
    gate L6 pass=0 read=mutants=0 survivors=none
    gate L7 pass=1 read=still-gated=24 changed=none
    c1-gate fixed=1/7 exit=1

Mutant tree, prints (receipt c1-mutant-finding1.txt):

    gate L1 pass=0 read=gated=23 broken=1 lines=64/base=64
    gate L2 pass=0 read=base-gated=24 regrounded=1 claim-gates.md
    gate L3 pass=0 read=bad=claim-gates.md
    gate L4 pass=0 read=bad=claim-gates.md
    gate L5 pass=0 read=bad=claim-gates.md
    gate L6 pass=0 read=mutants=0 survivors=claim-gates.md:unmutated-copy-not-green
    gate L7 pass=1 read=still-gated=23 changed=none
    c1-gate fixed=1/7 exit=1

Prior v1 reading of the same recipe (quoted from wave1/R46RevC1L3.md Finding 1):
`gate L3 pass=1 read=recheck-lines-clean=1` / `c1-gate fixed=2/7 exit=1`. Under v1.2 the L3 bypass is closed:
the exact-line requirement (r46-c1-gate.py:71 `exact_line`, enforced at :266-268 together with the exactly-one
recheck line and the HOME test) rejects the `&& true # …` line, and classify() marks the non-allow-listed line
broken (r46-c1-gate.py:237-238), which turns L1 red with broken=1 before L3 even runs. The control discriminates
cleanly: it is red for "nothing re-grounded" (recheck-lines-exact=0, broken=0) while the mutant is red WITH the
defect identified (regrounded=1 claim-gates.md, L3 bad=claim-gates.md, L1 broken=1) — and the delta against the
old run is purely the L3 flip (fixed 2/7 → 1/7). No regression on the C1 side.

================================================================================
Limitations
================================================================================
- C1: rebuilt Finding 1 only (the old report's headline recipe). Findings 2/4(a-e) of wave1/R46RevC1L3.md were
  not rebuilt (seat scope: one tree per report). The rebuild uses pure2 (round-15 914ca0b), the attempt-2
  designated base export, not the old L1/pure; the recipe site (claim-gates.md:125) is identical.
- C2: rebuilt on the tip entry (8 data rows), not the old hand-built 6-row entry; the junk edit is at the same
  semantic site (SECURITY.md row, S073.txt:564). The verdict difference vs the old run is mechanism-level (v1
  counted the junk row; v1.2 excludes it but tolerates it); both readings are quoted above.
- I did not re-run the v1 counters; v1's acceptance is cited from the wave-1 reports' own quoted output.
- Junk tolerance arithmetic (real_rows − 6) was measured on this entry's table; other tables shift the tolerance
  with their own real-row count.
- No commits, pushes, or mutating git/jj anywhere; the fleet repo, sibling lanes, MANIFEST.json, .ufo/state and
  shokuknow untouched. Scratch /fast/scratch/hyaku/kasegi-r46/R46bRevPriorEscapes removed after receipts were
  copied into the draft dir. No tools installed or upgraded (none needed; python3/git/tar only). No live-target
  testing: the trees are scratch exports; the only executed recheck lines were the counters' own classify() of
  base/tree lines (read-only test -d / instrument invocations, exactly as the gate runs on any tree).
