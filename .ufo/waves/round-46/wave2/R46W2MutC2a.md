VERDICT: BROKEN

# R46W2MutC2a — C2 mutation probe of `corpus/instruments/r46-c2-gate.py` v1.1 (gates G1–G3)

Scope: frontier table (G1), entry header/sections/words/table rows/xrefs (G2), registry row cells (G3).
Tree: export of `5437afeaf9b642c267bba3c31f00ae701e49da68` (counter bytes at 5437afe = lane file = sha256 `b52fea31…958621`, the v1.1 hash in counter-errata.md). Lane HEAD is now `0d121a2`; 5437afe is its ancestor (`git merge-base --is-ancestor` true). Not edited: the counter, the lane, git.

Method: `recipe.py` (scratch, removed on exit) copies the export, applies ONE edit to one file per mutant, grades with the lane's counter (`python3 <lane>/corpus/instruments/r46-c2-gate.py --root <mutant>`), and reads the target gate. `rejected=1` iff counter exit ≠ 0 AND the target gate reads `pass=0`. Every mutant changed exactly one file (`edit(1 file(s))`).

## Controls (do-nothing and positive)

```
control=untouched-tip exit=0 gates=1111111 c2-gate fixed=7/7 exit=0
control=pure-base exit=1 gates=0000001 c2-gate fixed=1/7 exit=1
```

The untouched tip is green, so a rejection is attributable to its edit. The pure base (914ca0b, no F28 row) is red.

## Survivors (rejected=0), first. Each survivor's counter output equals the untouched control's (`c2-gate fixed=7/7 exit=0`).

**S1 `g1-sourceless-F28`: the frontier row can be sourceless.** Edit, `corpus/README.md`, the F28 row only: ` | S073 | ` → ` | - | ` (source cell is the 5th cell; post-edit cell5 = `[-]`, cell3 = `[admitted]`, cell4 = the entry path).
Output: `mutant=g1-sourceless-F28 rejected=0` / `target=G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md`.
Why: `g1()` (counter lines 167–186) reads only the id, the status cell and the entry cell (`r[3]`). No limb reads the row's source cell, so the frontier-to-source link is ungraded. This contradicts the counter's own docstring (lines 6–8): "counted through seven limbs that a junk row, a sourceless row or an entry that quotes text the source does not hold cannot satisfy". Highest priority.

**S2 `g2-recheck-noop`: the entry's recheck line need not run anything.** Edit, `github-private-vulnerability-reporting.md` line 5: `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073 # 180d` → `recheck: true  # python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073 # 180d`.
Output: `mutant=g2-recheck-noop rejected=0` / `target=G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=8 xrefs=4/4`.
Why: `ok_r` (line 200) is a substring test over the first eight live lines; the line is never executed. G4 runs `source-recheck.py` directly, not the entry's line. Cross-check, read-only: `python3 corpus/instruments/recheck-audit.py --root <tip> --quiet` and `--root <mutant>` both print `executes=43 gated=22 broken=0`, so the sibling instrument does not catch it either.

**S3 `g2-xref-range-end`: cross-reference range end is never checked.** Edit: `corpus/knowledge/ai-assisted-finding-validation.md:7-8 holds that` → `…:7-9999 holds that` (Overlap section).
Output: `mutant=g2-xref-range-end rejected=0` / `target=G2 pass=1 … xrefs=4/4`.
Why: line 210 `re.findall(r"corpus/knowledge/([A-Za-z0-9._-]+\.md):(\d+)", body)` captures only the start line; the docstring promises "file:line, in range".

**S4 `g2-table-paraphrase-navcite`: an uncited-quote paraphrase cited to a navigation line passes.** Edit, entry table row 3: the curly-quoted sentence `“following the instructions in the security policy … preferred security contact.” (`S073.txt:566`)` → unquoted `the repository's security policy, or an issue asking the maintainers for a security contact (`S073.txt:5`)`.
Output: `mutant=g2-table-paraphrase-navcite rejected=0` / `target=G2 pass=1 … table-rows=8 …`; the recipe's line `counter exit=0 failed-gates=none` shows G5 also passes.
Why: G2 counts any 3-cell row with an `S073.txt:\d+` cite (line 209) and checks no range. G5 grades only curly-quoted spans, so an unquoted paraphrase is never located. `S073.txt` lines 1–6 are GitHub navigation (`Skip to main content`, `Search or ask Copilot/`, `Menu`), outside the body 556–583 (`sed -n '1,6p'` / `sed -n '556,557p'` of the capture).

**S5 `g3-anchor-nav-locator`: the registry anchor can point at navigation.** Edit, `corpus/SOURCES.md` S073 row: `body lines 556-583 of` → `body lines 1-5 of`.
Output: `mutant=g3-anchor-nav-locator rejected=0` / `target=G3 pass=1 read=row-S073=ok`.
Why: line 247 accepts any `lines N` locator (`\blines?\s+\d+`) and never checks it against BODY = (556, 583) (line in counter).

**S6 `g2-limits-filler-26w`: a section can be filler.** Edit: body of `## Limits` (the lines before the next `## `) replaced by 30 words: "Filler text fills this section so the heading and word count stand while no limit of the page is recorded here and nothing about the source is said at all."
Output: `mutant=g2-limits-filler-26w rejected=0` / `target=G2 pass=1 read=… sections=4/4 full=4/4 …`.
Why: `full` is a `\w+` word count ≥25 (line 202); the limb is structure-only. The errata already says "the gate grades structure and located quotes". Reported as a survivor of the words limb as written, but it is a disclosed scope limit.

## Rejections (rejected=1; target gate pass=0)

```
mutant=g1-pending-F28 rejected=1        target=G1 pass=0 read=rows=28 admitted=27 dup=0            (edit: F28 status admitted -> pending)
mutant=g1-duplicate-id-F27 rejected=1   target=G1 pass=0 read=rows=28 admitted=28 dup=1            (edit: F27 id -> F28; exit=1 failed=G1,G2,G3,G5,G6 fixed=2/7)
mutant=g2-limits-renamed rejected=1     target=G2 pass=0 read=… sections=3/4 full=3/4 …            (edit: "## Limits" -> "## Limitations")
mutant=g2-overlap-24w rejected=1        target=G2 pass=0 read=… sections=4/4 full=3/4 …            (edit: Overlap body -> 24 words, xrefs kept; boundary is 25)
mutant=g2-table-rows-cut-to-5 rejected=1 target=G2 pass=0 read=… table-rows=5 …                    (edit: table rows 6-8 deleted; G5 also fails: spans=18 located=18 failed=0 uncited=0 cores=3/5)
mutant=g3-usedby-wrong-entry rejected=1 target=G3 pass=0 read=bad=used-by                          (edit: S073 used-by -> linux-kernel entry path)
```

The table-rows rejection is confounded: the three deleted rows carried two of the five frozen cores, so G5 fails too. The G2 table-row floor is therefore not isolated by a clean single-edit test.

Full summary line from the battery: `summary mutants=12 rejected=6 survived=6`.

## Limitations
- Twelve hand-chosen single edits, not an exhaustive mutation set. G4–G7 were not mutated, and G1 was tested only at row level.
- The "do-nothing" control is the untouched export, and the positive control is the pure base. The counter was run from the lane file, so `TOOL_ROOT` is the lane: G4 uses the lane's pinned `source-recheck.py` and G7 runs the fleet's read-only `sources-census.sh validate`.
- Lane HEAD is `0d121a2`, not the cited `5437afe`. I graded the export of the cited commit; the counter bytes match in both.
- The survivors are judged against stated claims. S6 is a disclosed structure-only scope limit; S1–S5 are gaps in the stated limbs.
- The recipe lives only in scratch, which is removed on exit. The exact survivor edits are above, and the `edit(1 file(s))` lines in the battery confirm each mutant touched one file.
- I did not test whether any survivor's prose overreaches; that is the non-author closure's job.
