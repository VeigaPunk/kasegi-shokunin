VERDICT: DRAFT-READY

Scope: registry drafter (seat R46ScribeRegistry). Deliverable: `.ufo/waves/round-46/wave1/R46ScribeRegistry.draft/registry-append.md` (sha256 13244f7184f465105388a04084f0e737692644bbc51cb7c425b2a00a6bea6822). It holds (a) the SKILL.md block `## Round-46 Gates & probes registry addition (appended 2026-10-28)` with one 8-cell row per name, and (b) the five matching rows for `corpus/instruments/README.md`, to be appended under its existing table after line 997. Nothing was applied to SKILL.md or README.md. Two of the five rows describe landed bytes; three describe drafts that have not landed. Those three are marked NOT LANDED in the cells, and the L1 has to repoint or delete them before the registry is final. No commit, push, git mutation, or install was made.

## Findings

### F1. Inputs are base-equal (the do-nothing baseline for the registry)
Command: `sha256sum` of the base export of SKILL.md (`git archive 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba`), the pure export, and the live file; same for README.md.
Output:
```
a7c4d818300df64eaa9f636658a4a0ed514fb777d7750435c79cceac43ba15ca  <base export>/SKILL.md
a7c4d818300df64eaa9f636658a4a0ed514fb777d7750435c79cceac43ba15ca  <pure export>/SKILL.md
a7c4d818300df64eaa9f636658a4a0ed514fb777d7750435c79cceac43ba15ca  <lane>/SKILL.md
1aab9a407ea1382a56e2557d5a7f3b8c3d9aa80f83045e84a65cb5250ac47630  <base export>/corpus/instruments/README.md
1aab9a407ea1382a56e2557d5a7f3b8c3d9aa80f83045e84a65cb5250ac47630  <lane>/corpus/instruments/README.md
```
SKILL.md has 1155 lines at base; the round-45 block is its last section (lines 1146-1155).

### F2. Block shape matches the round-45 shape
Command: python check of the draft (heading, header, cell count with GFM splitting on every unescaped pipe, one row per name).
Output:
```
SKILL [8, 8, 8, 8, 8] True True        (cells per row; names exactly once; order matches)
README [8, 8, 8, 8, 8] True True
heading exact True
header exact True                       (name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner)
header GFM 8
```
Fixed in this pass: an earlier draft had a raw `|` inside a code span (`exit=0|1`) that GFM would split. It now reads `exit=` then 0 or 1.

### F3. Five names: two landed, three not
Command: `ls corpus/instruments | grep r46`; `git ls-files | grep -c 'r46-landing\|r46-counters'`; `ls .ufo/waves/round-46/wave1/`.
Output:
```
r46-c1-gate.py
r46-c2-gate.py
0
R46ExecLandingA.draft R46ExecLandingB.draft ... R46ExecSelftestC1.draft R46ExecSelftestC2.draft ...
```
`r46-c1-gate.py` (sha256 b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294) and `r46-c2-gate.py` (sha256 0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6) both match freeze.txt. The rows for `r46-landing-gate.py`, `r46-counters-selftest-c1.py` and `r46-counters-selftest-c2.py` say NOT LANDED. They point at the sibling drafts they were read from:
- `R46ExecLandingA.draft/r46-landing-gate.py`, sha256 prefix 1e0ce85c99acf115 (read 20:11)
- `R46ExecLandingB.draft/r46-landing-gate.py`, sha256 prefix 7ad171e73b1b211d (read 20:12)
- `R46ExecSelftestC1.draft/r46-counters-selftest-c1.py`, 22374 bytes (read 20:15)
- `R46ExecSelftestC2.draft/r46-counters-selftest-c2.py`, 37646 bytes (read 20:14)

The drafts were still changing during measurement. The rows state their intended behaviour from the drafts' own docstrings and argparse. They were not run by this seat. The two selftest draft directories were absent at my first listing (about 20:10) and present at the second (about 20:15); the Landing B draft also appeared after the first listing. The rows reflect the second listing.

### F4. Self-test column: the counters have no `--selftest`
Command: `python3 corpus/instruments/r46-c1-gate.py --selftest`; `python3 corpus/instruments/r46-c2-gate.py --selftest`; the --root and --baseline error paths.
Output:
```
r46-c1-gate.py: error: unrecognized arguments: --selftest      rc=2
r46-c2-gate.py: error: the following arguments are required: --root      rc=2
r46-c1-gate: /fast/.../no-such is not a directory               rc=2
r46-c1-gate: aggregate mode needs --baseline <dir>               rc=2
reground entry=claim-gates.md rows=0 ok=0 exit=1 read=section-count=0    rc=1
```
The last line is the per-entry mode on the live `corpus/knowledge/claim-gates.md`. It is not yet re-grounded, so it fails closed. The discrimination record for both counters is therefore the frozen controls harness (F5), not a built-in self-test.

### F5. Frozen controls re-run: reproduced byte-for-byte, all red
Command: `python3 .ufo/waves/round-46/controls/freeze-controls.py --lane <lane> --base 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba --work <scratch>`; then `diff` of its stdout against `.ufo/waves/round-46/controls/freeze-controls.txt`.
Output:
```
rc=0
c2-gate fixed=5/7 exit=1
exit=1
controls total=9 red=9 green=0
diff lines: 0
```
Do-nothing controls, read from the same run:
```
== c1 do-nothing (tree = baseline = base export)
... gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64
... gate L7 pass=1 read=still-gated=24 changed=none
c1-gate fixed=1/7 exit=1
== c2 do-nothing (base export)
gate G1 pass=0 read=rows=27 admitted=27 dup=0
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=1/7 exit=1
```
The other controls read red as recorded: c1 fabricated-anchors 0/7, single-anchor-file 0/7, marker-only 3/7, gutted-entry 6/7; c2 junk-row 4/7, fabricated-quote 4/7, uncited-filler 5/7. All nine are red (total=9 red=9 green=0). The run took 26.8 s.

### F6. Pinned values
Command: `sha256sum` of the five pinned files, compared with the pins in freeze.txt and the counter's PINS table.
Output:
```
corpus/instruments/r46-c1-gate.py MATCH
corpus/instruments/r46-c2-gate.py MATCH
corpus/source-snapshots/round-46/S073.txt MATCH          (66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930)
corpus/source-snapshots/round-46/manifest.json MATCH     (01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34)
corpus/instruments/source-recheck.py MATCH               (fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003)
```
The sources-census script that G7 calls exists at `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (35466 bytes).

### F7. anchorcheck: the block's cites resolve; the README baseline is already red
Command: `python3 corpus/instruments/anchorcheck.py` (no argument), then on the draft, the live SKILL.md, and the live README.md.
Output:
```
usage: anchorcheck.py <file.md> | anchorcheck.py --selftest      rc=2
registry-append.md: 26 in-range cite instances, 0 bad; 13 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0      rc=0
SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0      rc=0
README.md: 5 in-range cite instances, 0 bad; 5 distinct anchors; LOST-RECORDED=2 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=4      rc=1
```
The README rc=1 is baseline, not this draft. The live README is byte-identical to base, and its four BASE-ABSENT cites (lines 114, 116, 164, 807) point at `~/Projects/the-bounty-hunter`, which is absent. The draft's 26 cites are all full `corpus/instruments/...:N[-M]` paths. Bare `:N` shorthand was removed on purpose, because anchorcheck ignores it.

Discrimination control: a fixture lane (a SKILL.md marker plus copies of the two counters) with the draft copied in, then one anchor mutated to `r46-c1-gate.py:9999`.
Output:
```
control (unmutated):  26 in-range cite instances, 0 bad ...   rc=0
mutant:               24 in-range cite instances, 2 bad ...   rc=1
PAST-EOF md:5 corpus/instruments/r46-c1-gate.py:9999 (file has 275 lines)
PAST-EOF md:13 corpus/instruments/r46-c1-gate.py:9999 (file has 275 lines)
```
Running anchorcheck on a copy outside the lane gives BASE-ABSENT=16 for both the base SKILL.md and the augmented one. That is a location artifact, not the block.

### F8. density: the block does not lower the mean
Command: `python3 corpus/instruments/density.py <SKILL.md> --label r46`, run on the base export and on base + block; plus the exact per-block means computed by importing `density.split_blocks` and `density.census_block`.
Output:
```
base:  | | **mean dens** | ... | **249.1** |           (32 blocks; exact 249.1077)
aug:   | 33 | Round-46 Gates & probes registry addition (appended 2026-10-28) | 9 | 8 | 34 | 5 | 14 | 3 | 56 | 700.0 |
       | | **mean dens** | ... | **262.8** |         (33 blocks; exact 262.7711)
delta=+13.6634  lowered=False
```
Discrimination: a control block with no cites (`## Filler control`, plain prose) lowers the mean to 241.5589, so the instrument can register a drop. The block's own density is 700.0, well above the mean.

### F9. Final counts for the report line
- anchorcheck on the draft: `26 in-range cite instances, 0 bad`, rc=0 (13 distinct anchors)
- density mean: base 249.1 (exact 249.1077) to 262.8 (exact 262.7711), not lowered

## Limitations
- anchorcheck confirms only that each cited line range exists in the lane. It does not check that the lines say what the row claims. I checked content by hand: `corpus/instruments/r46-c1-gate.py:55` is `TARGET_GATED = 22`; `:180` is `ok = len(gt) <= TARGET_GATED and not broken and len(ct) >= len(cb)`; `:269` is `code = 0 if fixed == 7 else 1`; `corpus/instruments/r46-c2-gate.py:54` is the CENSUS path; `:307` is `if not os.path.isdir(a.root):`; `:319` is `code = 0 if fixed == len(GATES) else 1`.
- Only two of the five rows describe landed bytes. Rows 3-5 describe moving drafts (times above). They must be re-measured at landing, and the L1 must repoint or delete them.
- The counters have no self-test. The falsification I ran is the frozen controls harness. I did not run the sibling selftest drafts or the landing drafts; their self-test last lines (`selftest cases=<N> failures=<F>`) are as stated by their docstrings and remain unmeasured.
- The density result covers only this block addition under the instrument's block rule. It is not a judgement of the density or quality of the rows.
- The README rows are a draft for appending after README.md line 997. They are not written into README.md.
- Cleanup: my scratch directory was removed. I also removed `corpus/instruments/__pycache__/density.cpython-314.pyc`, a gitignored cache my import created. `corpus/instruments/__pycache__/r46-c1-gate.cpython-314.pyc` (20:13) is not mine and was left alone.
- Installs: none. Commits, pushes, and git/jj mutations: none.
