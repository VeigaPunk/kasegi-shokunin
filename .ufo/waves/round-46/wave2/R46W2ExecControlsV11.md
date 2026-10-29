VERDICT: BROKEN (battery built and run; 16 of 17 controls read RED under v1.1, 1 reads GREEN: `c1 hollow-rows`; 12 controls are red-before-evidence: green under frozen v1, red under v1.1)

# R46W2ExecControlsV11 — v1.1 control battery (draft)

Deliverable: `.ufo/waves/round-46/wave2/R46W2ExecControlsV11.draft/controls-v1.1.py` (sha256 `7a634e66d73de4d9557834da8b07e50c7af1e5ae9e258415b28ccfcd0a6a295e`), full run output `.../controls-v1.1.out.txt` (sha256 `3b8995022cc9d08deecfb56df12ff225473ca2380f6f628c26001f2c0fe7d13c`, 400 lines, pasted below).
Command (from scratch dir, TMPDIR explicit, ~9 min wall):
`python3 controls-v1.1.py --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --tip 5437afeaf9b642c267bba3c31f00ae701e49da68 --base 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba --freeze 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5 --work <scratch>` -> `rc=1`, last line `controls total=17 red=16 green=1`.

## How it is built
- GOOD tree = `git archive 5437afe corpus` export. Sanity (not counted as controls, printed first): v1.1 C1 `c1-gate fixed=7/7 exit=0` and v1.1 C2 `c2-gate fixed=7/7 exit=0` on it, both run from the lane's instruments (header line `v1.1 tools (lane, == tip blobs: yes): c1 99e0ee555b68e517 c2 b52fea3183a393fa`, i.e. the lane files are the tip blobs).
- One mutation per control, applied to a fresh copy of the tip tree. Two columns per control: `v1.1` = lane counters; `v1` = frozen counters from `git show 9f23aab:corpus/instruments/r46-c{1,2}-gate.py` (header: c1 `b0c730c834b4d7c6`, c2 `0ee958578b592370`) in a scratch tools dir that is a copy of the lane's instruments.
- Two v1-only tree adjustments, stated in the script docstring (v1 can never read 7/7 on a tree that satisfies the other counter, counter-errata C2-E5): v1 C1 trees carry the v1 gate file (v1 executes the tree's own copy); v1 C2 trees carry the two C1-re-grounded entries at BASE bytes. Evidence that this is needed and not a rigging: `-- info: v1 C2 on the UNMODIFIED tip tree ... gate G6 pass=0 read=knowledge=65 base-names-intact=0 entry-bytes-ok=1 ... c2-gate fixed=6/7 exit=1`; with the adjustment `-- good tree for v1 c2 ... c2-gate fixed=7/7 exit=0` and `-- good tree for v1 c1 ... c1-gate fixed=7/7 exit=0`.
- Do-nothing discrimination: `c1 do-nothing` reads `c1-gate fixed=1/7 exit=1` and `c2 do-nothing` reads `c2-gate fixed=1/7 exit=1` in both columns, while the good tree reads 7/7 in both; every other control moves the reading from the good tree's 7/7.
- The hostile-line control is RED only if exit != 0 AND the benign scratch marker (`touch <scratch>/marker-hostile-<col>`) was not created; HOME-override uses a scratch HOME holding `Projects/{bounties,the-bounty-hunter,origin-work,ufo-fsd-alpha}` (empty dirs), never the real HOME.

## Findings
1. **F1 (v1.1 GREEN, expectation not met): `c1 hollow-rows` reads `c1-gate fixed=7/7 exit=0`** (output line 184: `v1.1  exit=0 reads=GREEN`). Mutation: in both re-grounded entries the four-column rows keep their real anchor and token but the "current claim" cells are rotated by one row, so every claim is about the lost `claim-check.mjs` yet is attached to another row's anchor/token. v1.1 cannot read claim text, so L1-L7 all pass (`L6 mutants=46 survivors=none`). This is exactly what `counter-errata.md` "What the errata do not claim" says v1.1 still cannot do; the battery makes it a measured green, not a prose caveat. The C1 verdict therefore rests on the non-author side-by-side row reading, not on 7/7. (I did not widen the counter; draft only.)
2. **12 red-before controls** (green under frozen v1, red under v1.1; the errata's evidence, read straight from the output):
   - C1: comment-trick (v1 `fixed=7/7 exit=0`, v1.1 `L1 ... broken=2`, `L3 bad=...`, `fixed=5/7`); cd-home (v1 7/7, v1.1 `L3 pass=0`, 6/7); planted-anchor (v1 7/7, v1.1 `L4 pass=0 read=bad=claim-gates.md,claim-package-contract.md`, 6/7); restoration-recheck removed (v1 7/7, v1.1 `L5 pass=0`, 6/7); hostile-line (v1 exit=1 but `marker-created=1`, i.e. v1 executed the tree-supplied line; v1.1 `marker-created=0`, `L1 ... broken=1`, 2/7).
   - C2: wrong-source recheck (v1 7/7, v1.1 `G2 recheck=0`); junk table rows (v1 `table-rows=8`, v1.1 `table-rows=5`); emptied Limits (v1 7/7, v1.1 `full=3/4`); source-cell URL wrapped in another host (v1 7/7, v1.1 `G3 bad=url`); citation range 1-589 (v1 7/7, v1.1 `G5 failed=1 cores=4/5`); core in HTML comment (v1 7/7, v1.1 `G5 cores=4/5`); extra non-md file (v1 7/7, v1.1 `G6 entries=66 base-intact=0`).
3. **Not a v1 false-green, still red in both columns:** `c1 shadow-recheck` (v1 `L3 pass=0`, 6/7; v1.1 5/7) — v1 already caught a `recheck: true` placed above the re-grounded gate line because v1's L3 reads the first line; the wave-1 shadow case was above the BASE line. `c1 home-override`: both columns read `L1 pass=1 read=gated=6` (L1 alone moves with host HOME) but `L2 regrounded=0`, `fixed=2/7 exit=1`; v1.1 retains HOME on purpose (errata "Not changed on purpose"), so this is a disclosed host dependence, red in both. `c1/c2 do-nothing`: red in both.
4. Counter output nuance: under `c1 hostile-line` v1.1 prints `L2 pass=1 ... regrounded=3 citation-bases.md,...` (the broken, never-run line counts as non-gated) while `L1 broken=1`, `L3/L4/L5 bad=citation-bases.md`, so the red does not depend on L1 alone.

## Limitations
- Each control is a single mutation of one shape; one kill per control, not a mutation-score. The planted-anchor control re-anchors only contract G1 (but v1.1 L4 goes red for both entries because both anchor the changed file).
- The v1 column is v1 on adjusted trees (above); v1 on the raw tip reads C1 7/7 and C2 6/7 as shown.
- The hollow control is my construction (cyclic rotation of claim cells); a hand-written hollow fixture could differ, but any claim-only edit keeps all seven limbs green, so the finding is structural.
- Live host untouched: the counters strip `cd <lane> &&` and run in scratch roots; only scratch HOME was supplied; no network. Scratch dir `/fast/scratch/hyaku/kasegi-r46/R46W2ExecControlsV11` removed (`ls` -> no such file). No tool installs. No git/jj mutation; draft files only under `wave2/R46W2ExecControlsV11.draft/` plus this report.

## Full output (controls-v1.1.out.txt, verbatim)

```
tip=5437afeaf9b642c267bba3c31f00ae701e49da68 base=914ca0b6956f01d87b2e252ffad06fe74ec5d9ba freeze=9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5
v1.1 tools (lane, == tip blobs: yes): c1 99e0ee555b68e517 c2 b52fea3183a393fa
v1 tools (frozen, git show 9f23aab4636b): c1 b0c730c834b4d7c6 c2 0ee958578b592370
-- good tip tree, v1.1 c1 (sanity, not a control)
   gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
   gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
   gate L3 pass=1 read=recheck-lines-exact=2
   gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
   gate L5 pass=1 read=append-only-restoration-kept=2
   gate L6 pass=1 read=mutants=46 survivors=none
   gate L7 pass=1 read=still-gated=22 changed=none
   c1-gate fixed=7/7 exit=0
   exit=0
-- good tree for v1 c1 (sanity, not a control)
   gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
   gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
   gate L3 pass=1 read=recheck-lines-clean=2
   gate L4 pass=1 read=entry-mode-green=2
   gate L5 pass=1 read=append-only=2
   gate L6 pass=1 read=mutants=46 survivors=none
   gate L7 pass=1 read=still-gated=22 changed=none
   c1-gate fixed=7/7 exit=0
   exit=0
-- good tip tree, v1.1 c2 (sanity, not a control)
   gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
   gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=8 xrefs=4/4
   gate G3 pass=1 read=row-S073=ok
   gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
   gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5
   gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
   gate G7 pass=1 read=census-rc=0 ok-line=1
   c2-gate fixed=7/7 exit=0
   exit=0
-- good tree for v1 c2 (sanity, not a control)
   gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
   gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=8 xrefs=4/4
   gate G3 pass=1 read=row-S073=ok
   gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
   gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5
   gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
   gate G7 pass=1 read=census-rc=0 ok-line=1
   c2-gate fixed=7/7 exit=0
   exit=0
-- info: v1 C2 on the UNMODIFIED tip tree (the two re-grounded entries differ from BASE; counter-errata C2-E5)
   gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
   gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=8 xrefs=4/4
   gate G3 pass=1 read=row-S073=ok
   gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
   gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5
   gate G6 pass=0 read=knowledge=65 base-names-intact=0 entry-bytes-ok=1
   gate G7 pass=1 read=census-rc=0 ok-line=1
   c2-gate fixed=6/7 exit=1
   exit=1

== c1 do-nothing (tree = baseline = base export)
v1.1  gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64
v1.1  gate L2 pass=0 read=base-gated=24 regrounded=0 
v1.1  gate L3 pass=0 read=recheck-lines-exact=0
v1.1  gate L4 pass=0 read=entry-mode-green-anchors-unchanged=0
v1.1  gate L5 pass=0 read=append-only-restoration-kept=0
v1.1  gate L6 pass=0 read=mutants=0 survivors=none
v1.1  gate L7 pass=1 read=still-gated=24 changed=none
v1.1  c1-gate fixed=1/7 exit=1
v1.1  exit=1 reads=RED
v1    gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64
v1    gate L2 pass=0 read=base-gated=24 regrounded=0 
v1    gate L3 pass=0 read=recheck-lines-clean=0
v1    gate L4 pass=0 read=entry-mode-green=0
v1    gate L5 pass=0 read=append-only=0
v1    gate L6 pass=0 read=mutants=0 survivors=none
v1    gate L7 pass=1 read=still-gated=24 changed=none
v1    c1-gate fixed=1/7 exit=1
v1    exit=1 reads=RED

== c1 comment-trick (`cd LANE && true  # r46-c1-gate.py --entry ...`, valid rows kept)
v1.1  gate L1 pass=0 read=gated=22 broken=2 lines=65/base=64
v1.1  gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
v1.1  gate L3 pass=0 read=bad=claim-gates.md,claim-package-contract.md
v1.1  gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
v1.1  gate L5 pass=1 read=append-only-restoration-kept=2
v1.1  gate L6 pass=1 read=mutants=46 survivors=none
v1.1  gate L7 pass=1 read=still-gated=22 changed=none
v1.1  c1-gate fixed=5/7 exit=1
v1.1  exit=1 reads=RED
v1    gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
v1    gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
v1    gate L3 pass=1 read=recheck-lines-clean=2
v1    gate L4 pass=1 read=entry-mode-green=2
v1    gate L5 pass=1 read=append-only=2
v1    gate L6 pass=1 read=mutants=46 survivors=none
v1    gate L7 pass=1 read=still-gated=22 changed=none
v1    c1-gate fixed=7/7 exit=0
v1    exit=0 reads=GREEN

== c1 cd-home (`cd ~/Projects/bounties && python3 corpus/instruments/r46-c1-gate.py --entry ...`)
v1.1  gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
v1.1  gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
v1.1  gate L3 pass=0 read=bad=claim-gates.md,claim-package-contract.md
v1.1  gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
v1.1  gate L5 pass=1 read=append-only-restoration-kept=2
v1.1  gate L6 pass=1 read=mutants=46 survivors=none
v1.1  gate L7 pass=1 read=still-gated=22 changed=none
v1.1  c1-gate fixed=6/7 exit=1
v1.1  exit=1 reads=RED
v1    gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
v1    gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
v1    gate L3 pass=1 read=recheck-lines-clean=2
v1    gate L4 pass=1 read=entry-mode-green=2
v1    gate L5 pass=1 read=append-only=2
v1    gate L6 pass=1 read=mutants=46 survivors=none
v1    gate L7 pass=1 read=still-gated=22 changed=none
v1    c1-gate fixed=7/7 exit=0
v1    exit=0 reads=GREEN

== c1 shadow-recheck (`recheck: true` line above the real gate line)
v1.1  gate L1 pass=0 read=gated=22 broken=2 lines=65/base=64
v1.1  gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
v1.1  gate L3 pass=0 read=bad=claim-gates.md,claim-package-contract.md
v1.1  gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
v1.1  gate L5 pass=1 read=append-only-restoration-kept=2
v1.1  gate L6 pass=1 read=mutants=46 survivors=none
v1.1  gate L7 pass=1 read=still-gated=22 changed=none
v1.1  c1-gate fixed=5/7 exit=1
v1.1  exit=1 reads=RED
v1    gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
v1    gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
v1    gate L3 pass=0 read=bad=claim-gates.md,claim-package-contract.md
v1    gate L4 pass=1 read=entry-mode-green=2
v1    gate L5 pass=1 read=append-only=2
v1    gate L6 pass=1 read=mutants=46 survivors=none
v1    gate L7 pass=1 read=still-gated=22 changed=none
v1    c1-gate fixed=6/7 exit=1
v1    exit=1 reads=RED

== c1 planted-anchor (comment appended to claim-package-check.py, contract G1 re-anchored on it)
v1.1  gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
v1.1  gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
v1.1  gate L3 pass=1 read=recheck-lines-exact=2
v1.1  gate L4 pass=0 read=bad=claim-gates.md,claim-package-contract.md
v1.1  gate L5 pass=1 read=append-only-restoration-kept=2
v1.1  gate L6 pass=1 read=mutants=46 survivors=none
v1.1  gate L7 pass=1 read=still-gated=22 changed=none
v1.1  c1-gate fixed=6/7 exit=1
v1.1  exit=1 reads=RED
v1    gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
v1    gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
v1    gate L3 pass=1 read=recheck-lines-clean=2
v1    gate L4 pass=1 read=entry-mode-green=2
v1    gate L5 pass=1 read=append-only=2
v1    gate L6 pass=1 read=mutants=46 survivors=none
v1    gate L7 pass=1 read=still-gated=22 changed=none
v1    c1-gate fixed=7/7 exit=0
v1    exit=0 reads=GREEN

== c1 restoration-recheck removed (both entries)
v1.1  gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
v1.1  gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
v1.1  gate L3 pass=1 read=recheck-lines-exact=2
v1.1  gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
v1.1  gate L5 pass=0 read=bad=claim-gates.md,claim-package-contract.md
v1.1  gate L6 pass=1 read=mutants=46 survivors=none
v1.1  gate L7 pass=1 read=still-gated=22 changed=none
v1.1  c1-gate fixed=6/7 exit=1
v1.1  exit=1 reads=RED
v1    gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
v1    gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
v1    gate L3 pass=1 read=recheck-lines-clean=2
v1    gate L4 pass=1 read=entry-mode-green=2
v1    gate L5 pass=1 read=append-only=2
v1    gate L6 pass=1 read=mutants=46 survivors=none
v1    gate L7 pass=1 read=still-gated=22 changed=none
v1    c1-gate fixed=7/7 exit=0
v1    exit=0 reads=GREEN

== c1 hollow-rows (claim cells rotated: rows about the lost claim-check.mjs anchored to the committed gate)
v1.1  gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
v1.1  gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
v1.1  gate L3 pass=1 read=recheck-lines-exact=2
v1.1  gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
v1.1  gate L5 pass=1 read=append-only-restoration-kept=2
v1.1  gate L6 pass=1 read=mutants=46 survivors=none
v1.1  gate L7 pass=1 read=still-gated=22 changed=none
v1.1  c1-gate fixed=7/7 exit=0
v1.1  exit=0 reads=GREEN
v1    gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
v1    gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
v1    gate L3 pass=1 read=recheck-lines-clean=2
v1    gate L4 pass=1 read=entry-mode-green=2
v1    gate L5 pass=1 read=append-only=2
v1    gate L6 pass=1 read=mutants=46 survivors=none
v1    gate L7 pass=1 read=still-gated=22 changed=none
v1    c1-gate fixed=7/7 exit=0
v1    exit=0 reads=GREEN

== c1 hostile-line (`recheck: touch <scratch marker>` in unrelated citation-bases.md; marker must not be created)
v1.1  gate L1 pass=0 read=gated=21 broken=1 lines=65/base=64
v1.1  gate L2 pass=1 read=base-gated=24 regrounded=3 citation-bases.md,claim-gates.md,claim-package-contract.md
v1.1  gate L3 pass=0 read=bad=citation-bases.md
v1.1  gate L4 pass=0 read=bad=citation-bases.md
v1.1  gate L5 pass=0 read=bad=citation-bases.md
v1.1  gate L6 pass=0 read=mutants=46 survivors=citation-bases.md:unmutated-copy-not-green
v1.1  gate L7 pass=1 read=still-gated=21 changed=none
v1.1  c1-gate fixed=2/7 exit=1
v1.1  marker-created=0
v1.1  exit=1 reads=RED
v1    gate L1 pass=1 read=gated=21 broken=0 lines=65/base=64
v1    gate L2 pass=1 read=base-gated=24 regrounded=3 citation-bases.md,claim-gates.md,claim-package-contract.md
v1    gate L3 pass=0 read=bad=citation-bases.md
v1    gate L4 pass=0 read=bad=citation-bases.md
v1    gate L5 pass=0 read=bad=citation-bases.md
v1    gate L6 pass=1 read=mutants=46 survivors=none
v1    gate L7 pass=1 read=still-gated=21 changed=none
v1    c1-gate fixed=4/7 exit=1
v1    marker-created=1
v1    exit=1 reads=GREEN

== c1 home-override (do-nothing tree under a scratch HOME that holds ~/Projects/bounties)
v1.1  gate L1 pass=1 read=gated=6 broken=0 lines=64/base=64
v1.1  gate L2 pass=0 read=base-gated=6 regrounded=0 
v1.1  gate L3 pass=0 read=recheck-lines-exact=0
v1.1  gate L4 pass=0 read=entry-mode-green-anchors-unchanged=0
v1.1  gate L5 pass=0 read=append-only-restoration-kept=0
v1.1  gate L6 pass=0 read=mutants=0 survivors=none
v1.1  gate L7 pass=1 read=still-gated=6 changed=none
v1.1  c1-gate fixed=2/7 exit=1
v1.1  exit=1 reads=RED
v1    gate L1 pass=1 read=gated=6 broken=0 lines=64/base=64
v1    gate L2 pass=0 read=base-gated=6 regrounded=0 
v1    gate L3 pass=0 read=recheck-lines-clean=0
v1    gate L4 pass=0 read=entry-mode-green=0
v1    gate L5 pass=0 read=append-only=0
v1    gate L6 pass=0 read=mutants=0 survivors=none
v1    gate L7 pass=1 read=still-gated=6 changed=none
v1    c1-gate fixed=2/7 exit=1
v1    exit=1 reads=RED

== c2 do-nothing (base export)
v1.1  gate G1 pass=0 read=rows=27 admitted=27 dup=0
v1.1  gate G2 pass=0 read=F28-rows=0
v1.1  gate G3 pass=0 read=row-S073=absent-or-malformed
v1.1  gate G4 pass=0 read=manifest-absent
v1.1  gate G5 pass=0 read=F28-rows=0
v1.1  gate G6 pass=0 read=knowledge=64 entries=64 nested-md=64 base-intact=1 entry-bytes-ok=0
v1.1  gate G7 pass=1 read=census-rc=0 ok-line=1
v1.1  c2-gate fixed=1/7 exit=1
v1.1  exit=1 reads=RED
v1    gate G1 pass=0 read=rows=27 admitted=27 dup=0
v1    gate G2 pass=0 read=F28-rows=0
v1    gate G3 pass=0 read=row-S073=absent-or-malformed
v1    gate G4 pass=0 read=manifest-absent
v1    gate G5 pass=0 read=F28-rows=0
v1    gate G6 pass=0 read=knowledge=64 base-names-intact=1 entry-bytes-ok=0
v1    gate G7 pass=1 read=census-rc=0 ok-line=1
v1    c2-gate fixed=1/7 exit=1
v1    exit=1 reads=RED

== c2 wrong-source recheck (`--source S0730`)
v1.1  gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
v1.1  gate G2 pass=0 read=source=1 verified-at=1 recheck=0 sections=4/4 full=4/4 table-rows=8 xrefs=4/4
v1.1  gate G3 pass=1 read=row-S073=ok
v1.1  gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
v1.1  gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5
v1.1  gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
v1.1  gate G7 pass=1 read=census-rc=0 ok-line=1
v1.1  c2-gate fixed=6/7 exit=1
v1.1  exit=1 reads=RED
v1    gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
v1    gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=8 xrefs=4/4
v1    gate G3 pass=1 read=row-S073=ok
v1    gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
v1    gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5
v1    gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
v1    gate G7 pass=1 read=census-rc=0 ok-line=1
v1    c2-gate fixed=7/7 exit=0
v1    exit=0 reads=GREEN

== c2 junk-table-rows (three real rows replaced by `| - | - | - |`)
v1.1  gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
v1.1  gate G2 pass=0 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=5 xrefs=4/4
v1.1  gate G3 pass=1 read=row-S073=ok
v1.1  gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
v1.1  gate G5 pass=1 read=spans=18 located=18 failed=0 uncited=0 cores=5/5
v1.1  gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
v1.1  gate G7 pass=1 read=census-rc=0 ok-line=1
v1.1  c2-gate fixed=6/7 exit=1
v1.1  exit=1 reads=RED
v1    gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
v1    gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=8 xrefs=4/4
v1    gate G3 pass=1 read=row-S073=ok
v1    gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
v1    gate G5 pass=1 read=spans=18 located=18 failed=0 uncited=0 cores=5/5
v1    gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
v1    gate G7 pass=1 read=census-rc=0 ok-line=1
v1    c2-gate fixed=7/7 exit=0
v1    exit=0 reads=GREEN

== c2 emptied-Limits (heading kept, body deleted)
v1.1  gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
v1.1  gate G2 pass=0 read=source=1 verified-at=1 recheck=1 sections=4/4 full=3/4 table-rows=8 xrefs=4/4
v1.1  gate G3 pass=1 read=row-S073=ok
v1.1  gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
v1.1  gate G5 pass=1 read=spans=15 located=15 failed=0 uncited=0 cores=5/5
v1.1  gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
v1.1  gate G7 pass=1 read=census-rc=0 ok-line=1
v1.1  c2-gate fixed=6/7 exit=1
v1.1  exit=1 reads=RED
v1    gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
v1    gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=8 xrefs=4/4
v1    gate G3 pass=1 read=row-S073=ok
v1    gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
v1    gate G5 pass=1 read=spans=15 located=15 failed=0 uncited=0 cores=5/5
v1    gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
v1    gate G7 pass=1 read=census-rc=0 ok-line=1
v1    c2-gate fixed=7/7 exit=0
v1    exit=0 reads=GREEN

== c2 source-cell URL wrapped in another host (SOURCES.md S073 row)
v1.1  gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
v1.1  gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=8 xrefs=4/4
v1.1  gate G3 pass=0 read=bad=url
v1.1  gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
v1.1  gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5
v1.1  gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
v1.1  gate G7 pass=1 read=census-rc=0 ok-line=1
v1.1  c2-gate fixed=6/7 exit=1
v1.1  exit=1 reads=RED
v1    gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
v1    gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=8 xrefs=4/4
v1    gate G3 pass=1 read=row-S073=ok
v1    gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
v1    gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5
v1    gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
v1    gate G7 pass=1 read=census-rc=0 ok-line=1
v1    c2-gate fixed=7/7 exit=0
v1    exit=0 reads=GREEN

== c2 citation-range 1-589 (one cite widened to the whole capture)
v1.1  gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
v1.1  gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=8 xrefs=4/4
v1.1  gate G3 pass=1 read=row-S073=ok
v1.1  gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
v1.1  gate G5 pass=0 read=spans=21 located=20 failed=1 uncited=0 cores=4/5
v1.1  gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
v1.1  gate G7 pass=1 read=census-rc=0 ok-line=1
v1.1  c2-gate fixed=6/7 exit=1
v1.1  exit=1 reads=RED
v1    gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
v1    gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=8 xrefs=4/4
v1    gate G3 pass=1 read=row-S073=ok
v1    gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
v1    gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5
v1    gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
v1    gate G7 pass=1 read=census-rc=0 ok-line=1
v1    c2-gate fixed=7/7 exit=0
v1    exit=0 reads=GREEN

== c2 core-in-HTML-comment (the AI-assistance row wrapped in <!-- -->)
v1.1  gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
v1.1  gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=7 xrefs=4/4
v1.1  gate G3 pass=1 read=row-S073=ok
v1.1  gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
v1.1  gate G5 pass=0 read=spans=20 located=20 failed=0 uncited=0 cores=4/5
v1.1  gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
v1.1  gate G7 pass=1 read=census-rc=0 ok-line=1
v1.1  c2-gate fixed=6/7 exit=1
v1.1  exit=1 reads=RED
v1    gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
v1    gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=7 xrefs=4/4
v1    gate G3 pass=1 read=row-S073=ok
v1    gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
v1    gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5
v1    gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
v1    gate G7 pass=1 read=census-rc=0 ok-line=1
v1    c2-gate fixed=7/7 exit=0
v1    exit=0 reads=GREEN

== c2 extra-non-md-file (corpus/knowledge/notes.txt)
v1.1  gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
v1.1  gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=8 xrefs=4/4
v1.1  gate G3 pass=1 read=row-S073=ok
v1.1  gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
v1.1  gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5
v1.1  gate G6 pass=0 read=knowledge=65 entries=66 nested-md=65 base-intact=0 entry-bytes-ok=1
v1.1  gate G7 pass=1 read=census-rc=0 ok-line=1
v1.1  c2-gate fixed=6/7 exit=1
v1.1  exit=1 reads=RED
v1    gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
v1    gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=8 xrefs=4/4
v1    gate G3 pass=1 read=row-S073=ok
v1    gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
v1    gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5
v1    gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
v1    gate G7 pass=1 read=census-rc=0 ok-line=1
v1    c2-gate fixed=7/7 exit=0
v1    exit=0 reads=GREEN

v1 false-greens (green under v1, red under v1.1; the red-before evidence for the errata): c1 comment-trick; c1 cd-home; c1 planted-anchor; c1 restoration-recheck removed; c1 hostile-line; c2 wrong-source recheck; c2 junk-table-rows; c2 emptied-Limits; c2 source-cell URL wrapped in another host; c2 citation-range 1-589; c2 core-in-HTML-comment; c2 extra-non-md-file
v1.1 greens (must be none): c1 hollow-rows
v1 total=17 red=4 green=13
controls total=17 red=16 green=1
```
