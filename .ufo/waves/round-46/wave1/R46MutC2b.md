VERDICT: BROKEN

Scope: C2 mutation test of `corpus/instruments/r46-c2-gate.py`, gates G4 (manifest/recheck pins) and G5 (quote location, cores). Read-only: the counter was copied into scratch trees and never edited. Scratch removed on exit. No git mutation, no commit, no install.

## Survivors (defect present, target gate passes)

Five single-edit defects survive under the default pins. All are G5, which is unpinned (`PINS["entry"]` is `None`, counter line 59; `g5` at lines 255-276). Edits are on a hand-built fixture entry `corpus/knowledge/github-private-vulnerability-reporting.md`. The base line used is `- Eligibility: “You can only report vulnerabilities privately for repositories where this feature is enabled.” (`S073.txt:564`)`.

1. **M07, citation range widened to the whole capture (G5).** Edit: `(`S073.txt:564`)` -> `(`S073.txt:1-589`)`. The citation no longer locates the quote, since the window is all 589 lines of S073.txt.
   Output: `mutant=M07-citation-range-widened-to-file [default-pins] rejected=0 gate=G5 hunks=2 expected=survive as-expected=yes read=spans=7 located=7 failed=0 uncited=0 cores=5/5`
   Cause: `window = norm(" ".join(snap[max(a - 1, 0):b]))` (line 267) accepts any range. There is no width bound.

2. **M08, frozen core hidden in an HTML comment (G5).** Edit: the AI-disclosure line `- AI disclosure: “Optionally, select I used AI assistance to find or write up this report.” (`S073.txt:574`)` wrapped as `<!-- ... -->`.
   Output: `mutant=M08-core-3-wrapped-in-html-comment [default-pins] rejected=0 gate=G5 hunks=2 expected=survive as-expected=yes read=spans=7 located=7 failed=0 uncited=0 cores=5/5`
   Cause: `g5` reads raw text (`body = txt(root, p) or ""`, line 259). `live_lines()`, which strips HTML comments and fences, is used by G2 (line 189) but not by G5. The rendered entry shows no AI-assistance statement, yet core 3 is counted.

3. **M09, cited non-core quote in ASCII quotes (G5).** Edit: `- Who may report: “Anyone can privately report a security vulnerability to repository maintainers.” (`S073.txt:560`)` with the curly quotes replaced by `"`.
   Output: `mutant=M09-cited-quote-straight-quotes [default-pins] rejected=0 gate=G5 hunks=2 expected=survive as-expected=yes read=spans=6 located=6 failed=0 uncited=0 cores=5/5`
   Cause: `allcurly` and `spans` match only `“…”` (lines 261-262). A cited claim in ASCII quotes is never checked for location.

4. **P1, citation starting at line 0 (G5, probe).** Edit: `(`S073.txt:564`)` -> `(`S073.txt:0-564`)`.
   Output: `mutant=P1-citation-line-zero-range [default-pins] rejected=0 gate=G5 hunks=2 expected=survive as-expected=yes read=spans=7 located=7 failed=0 uncited=0 cores=5/5`
   Cause: `a = int(a)` has no `>= 1` check (line 265). `max(a - 1, 0)` silently clamps to line 1.

5. **P2, core inside a fenced block (G5, probe).** Edit: the core-1 line wrapped in a pair of ``` fence lines.
   Output: `mutant=P2-core-1-fenced-block [default-pins] rejected=0 gate=G5 hunks=2 expected=survive as-expected=yes read=spans=7 located=7 failed=0 uncited=0 cores=5/5`
   Cause: the same as survivor 2 (raw text, no `live_lines`).

Re-pinned survivor. It appears only when the manifest pin is recomputed for the mutant. With the default pin, the same edit is rejected by the pin.

6. **P4, one manifest record rewritten to duplicate Q3 with anchor 564 (G4, probe; hunks=4 in one record).** Manifest Q1 becomes `"anchor": 564` with the Q3 sentence as its quote.
   Default pin: `mutant=P4-manifest-q1-record-rewritten-anchor-564 [default-pins] rejected=1 gate=G4 hunks=4 expected=survive as-expected=NO read=manifest-not-the-pinned-bytes`. The `as-expected=NO` is my labelling error (see Limitations); the default-pin result is a rejection.
   Re-pinned (`R46_PINS_OVERRIDE` set to the mutant's own sha; probe only): `mutant=P4-manifest-q1-record-rewritten-anchor-564 [re-pinned-probe] rejected=0 gate=G4 hunks=4 expected=survive as-expected=yes read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0`
   Cause: `oks >= 8` (line 251) counts `^S073:Q\d+ OK` lines and does not require distinct quote text. The anchor check fails only on a non-unique quote or a `-BROKEN` note, so a duplicate whose declared anchor verifies passes.
   Consequence: under the pin, G4 has no limb beyond the pin that catches manifest content edits. Re-pinned P3 (quote replaced, anchor 560 kept) is caught only by the token `anchor=560-BROKEN` in recheck output, which G4 checks for (line 251). That is a real limb, but an incidental one.

## Rejected (limb holds)

Each row is one edit on the satisfied tree; each line is printed verbatim by one run of the recipe.

- M01, manifest.json one trailing space (G4 pin): `mutant=M01-manifest-trailing-byte [default-pins] rejected=1 gate=G4 hunks=1 expected=reject as-expected=yes read=manifest-not-the-pinned-bytes`
- M02, source-recheck.py one appended comment (G4 pin): `mutant=M02-recheck-tool-appended-line [default-pins] rejected=1 gate=G4 hunks=1 expected=reject as-expected=yes read=source-recheck-not-the-pinned-bytes`
- M03, S073.txt footer `Pricing` -> `Prizing` (G4 via manifest sha): `mutant=M03-snapshot-footer-byte [default-pins] rejected=1 gate=G4 hunks=2 expected=reject as-expected=yes read=recheck-rc=1 quotes-ok=0 frozen-cores-missing=0`
- M04, core-1 sentence line deleted (G5 cores): `mutant=M04-core-1-sentence-removed [default-pins] rejected=1 gate=G5 hunks=1 expected=reject as-expected=yes read=spans=6 located=6 failed=0 uncited=0 cores=4/5`
- M05, core-1 citation 564 -> 565 (G5 location): `mutant=M05-citation-line-shifted [default-pins] rejected=1 gate=G5 hunks=2 expected=reject as-expected=yes read=spans=7 located=6 failed=1 uncited=0 cores=4/5`
- M06, core-2 `impact statement.` -> `impact statements.` (G5 located): `mutant=M06-core-2-wording-altered [default-pins] rejected=1 gate=G5 hunks=2 expected=reject as-expected=yes read=spans=7 located=6 failed=1 uncited=0 cores=4/5`
- M10, core-1 span extended past 25 words (G5 length): `mutant=M10-core-1-span-past-25-words [default-pins] rejected=1 gate=G5 hunks=2 expected=reject as-expected=yes read=spans=7 located=6 failed=1 uncited=0 cores=4/5`
- P3, manifest Q1 quote replaced by Q3 text, anchor 560 kept. Default pin: `mutant=P3-manifest-q1-quote-is-q3-text [default-pins] rejected=1 gate=G4 hunks=2 expected=reject as-expected=yes read=manifest-not-the-pinned-bytes`. Re-pinned: `mutant=P3-manifest-q1-quote-is-q3-text [re-pinned-probe] rejected=1 gate=G4 hunks=2 expected=reject as-expected=yes read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0`. The `anchor=560-BROKEN` token fails the gate.

## Controls

- do-nothing (pure base + counter, no round-46 files): `gate G4 pass=0 read=manifest-absent`, `gate G5 pass=0 read=F28-rows=0`.
- satisfied (hand-built tree, G4 and G5 genuinely met): `gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0`, `gate G5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5`. The recipe asserts both before any mutant runs.
- Tree bytes match the freeze. Working-tree sha256 equals `git show 9f23aab…:<path> | sha256sum` for the counter (`0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6`, equal to freeze `c2-gate-sha256`), source-recheck (`fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`) and manifest (`01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34`). S073.txt is `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930`, matching the pin.

## Counter observations (no counter edit made)

- The null override does not disable the manifest pin. The comment at line 66 says "a null value disables that one pin". Run: `probe=null-override-manifest G4 pass=0 read=manifest-not-the-pinned-bytes`. Cause: `PINS["manifest.json"]` has no `is not None` guard (line 241), unlike source-recheck (244) and S073-row (217). S073.txt (line 225) has the same gap. This is selftest-only, but the comment is wrong.
- The counter does not verify its own bytes. Its pin is external (freeze.txt `c2-gate-sha256`).
- `R46_PINS_OVERRIDE` is read from the environment (lines 66-67), not from the tree. The counter does not refuse it.
- `TOOL_ROOT` (line 55) comes from the counter's location, so G4 runs the source-recheck beside the counter, not the one under `--root`. This matches the docstring, but a counter run from another location checks another tool.

## Limitations

- Only G4 and G5 are graded. Mutants were not run against G1-G3, G6 or G7. The fixture's G2 is unsatisfied (`table-rows=-2`), so the satisfied tree is not a full C2 pass.
- The fixture entry is hand-built: 7 curly quotes, 5 cores, all cited. It is a test vehicle, not the F28 draft.
- Pins make G4 rejection an artifact of the pin. The survivors are in G5 (unpinned). The G4 survivor (P4) appears only with a recomputed pin, outside the frozen controls.
- Each mutant was run once; the counter is deterministic.
- Labelling error: P4 default-pins is tagged `expected=survive`, so the run prints `as-expected=NO`. That is my expectation table, not the counter. Under the default pin the counter rejects it.
- Survivor 3 depends on the curly-only scope, which the counter states by design.
- No lane file was edited and no fix was applied. Suggested repairs, for L1 to decide: require `1 <= a <= b` and a width bound on citations; have G5 read `live_lines(raw)`; treat cited ASCII-quoted spans as curly; make the anchor/quote distinctness a G4 limb.

Commands run (scratch, `TMPDIR` set explicitly):
- `python3 recipe.py` twice. The second run is the reported output: exit 0, wall time 4.07 s.
- `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5:<path> | sha256sum` for the counter, source-recheck and manifest.
- `sha256sum` on the lane working-tree copies of the same paths and of S073.txt.
