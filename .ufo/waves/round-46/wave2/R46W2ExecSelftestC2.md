VERDICT: DRAFT-READY

Seat R46W2ExecSelftestC2. Draft: `.ufo/waves/round-46/wave2/R46W2ExecSelftestC2.draft/r46-counters-selftest-c2.py` (628 lines, sha256 `bf7cca541e386b103c7f5fb480162df71ca48a2fd3d5f1dacb7f773f4fafa5d1`). The lane selftest `corpus/instruments/r46-counters-selftest-c2.py` is untouched (`diff <(git show 5437afe:corpus/instruments/r46-counters-selftest-c2.py) corpus/instruments/r46-counters-selftest-c2.py` printed nothing). The L1 copies the draft over the lane file when it integrates.

All runs: `--lane` = an export of 5437afeaf9b642c267bba3c31f00ae701e49da68 (`git archive ... | tar -x -C $SCRATCH/tip`), `--pure` = the default `/fast/scratch/hyaku/kasegi-r46/L1/pure`, `HYAKU_SCRATCH=/fast/scratch/hyaku`, `TMPDIR` set explicitly. Counter graded by default = the tip export's `corpus/instruments/r46-c2-gate.py` (sha256 `b52fea3183a393fa2f5bb40879241034e9db0b45f7914244d9f3bed134958621`, the v1.1 hash named in counter-errata.md).

## F1. Problem reproduced: the wave-1 selftest against v1.1
Command: `python3 <wave-1 selftest copy> --lane $S/tip`. Last lines printed:
```
probe       probe-entry-pad-is-garbage-bytes fixed=6/7 failing=['G2'] (rejected) -- G6 floor is bytes, not content
selftest cases=95 failures=62
```
First control: `FAIL control ctl-complete-tree fixed=6/7 failing=['G2']  <- control-not-7/7 failing=['G2']` with `gate G2 pass=0 read=source=1 verified-at=1 recheck=1 sections=4/4 full=3/4 table-rows=7 xrefs=2/2` (the Limits section was one bullet plus a pad line counted as one word). G3 `bad=kind` came from `mut-census-bad-kind` (kind `blog` now also fails G3).

## F2. The draft on the committed tip export: failures=0
Command: `python3 $DRAFT/r46-counters-selftest-c2.py --lane $S/tip`. Exact last three lines (rc 0):
```
probe       probe-four-tick-fence-with-inner-three-tick-line fixed=7/7 failing=[] (ACCEPTED) -- renderer treats the row as fenced code; counter closes the fence early
probe       probe-entry-pad-is-garbage-bytes fixed=7/7 failing=[] (ACCEPTED) -- G6 floor is bytes, not content
selftest cases=148 failures=0
```
148 counted cases = 1 null + 25 controls + 122 mutants (the wave-1 file counted 95); 7 probes are printed, not counted. Case counts from the run: `null 1 / control 25 / mutant 122`, `grep -c '^probe'` = 7. Every mutant reads `ok` with exactly its target gate red and no collateral outside target|allow.

## F3. Falsifiability: the frozen v1 counter, and the do-nothing control
v1 bytes: `git show 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5:corpus/instruments/r46-c2-gate.py` (sha256 `0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6`), placed at `$S/v1root/corpus/instruments/r46-c2-gate.py` with the lane's source-recheck.py beside it (v1's G4 resolves source-recheck.py from its own TOOL_ROOT). Command: `python3 $DRAFT/r46-counters-selftest-c2.py --lane $S/tip --counter $S/v1root/corpus/instruments/r46-c2-gate.py`. Exact last lines (rc 1):
```
probe       probe-entry-pad-is-garbage-bytes fixed=7/7 failing=[] (ACCEPTED) -- G6 floor is bytes, not content
selftest cases=148 failures=35
```
`failures>0` (35). The wave-1 survivors v1 accepts, each printed as `<- ACCEPTED-targeted-gate-passes=[...]; tree read 7/7`:
- `--source S0730`: `mut-recheck-source-S0730` (G2); also `mut-recheck-manifest-other-round` (G2)
- junk `| - | - | - |` row: `mut-table-junk-dash-rows`, `mut-table-junk-letter-rows`, `mut-table-six-junk-rows-quotes-in-bullets`, `mut-table-six-rows-one-uncited`, `mut-table-rows-without-numeric-cite` (G2)
- emptied Limits and thin sections: `mut-limits-section-emptied`, `mut-section-{scope,overlap,limits}-24-words`, `mut-section-falsifiable-11-words` (G2)
- URL wrapped in another host: `mut-row-url-wrapped-in-other-host` (G3); plus `mut-row-scope-seven-words`, `mut-row-teaches-seven-words`, `mut-row-anchor-without-locator`, `mut-row-recheck-cell-filler`, `mut-row-after-sub-heading-in-registry` (G3)
- duplicate manifest quote: `mut-manifest-duplicate-quote-repinned` (G4); `mut-manifest-six-distinct-anchors-repinned` (G4)
- citation 1-589 / line 0: `mut-citation-1-589-real-quote`, `mut-citation-range-0-577`, `mut-citation-13-lines`, `mut-citation-starts-at-555`, `mut-citation-ends-at-584` (G5). Plain `S073.txt:0` is red under v1 as well (its window is empty), so it is not a v1 survivor; the `0-577` form is.
- core in an HTML comment / fenced core: `mut-core-row-in-html-comment`, `mut-core-row-in-fenced-block` (G5)
- ASCII-quoted cited quote: `mut-ascii-quoted-fabrication-cited`, `mut-ascii-quoted-fabrication-uncited` (G5)
- non-md file and nested md in corpus/knowledge: `mut-non-md-file-in-knowledge`, `mut-nested-md-in-knowledge-subdir`, `mut-hidden-file-in-knowledge` (G6)
- v1 also fails three controls: `ctl-ascii-quoted-real-quote-located` (G5), `ctl-c1-landed-two-entries` (G6) and `ctl-committed-tip-direct` (G6) -- the v1 joint-tip collision the errata names (C1 necessarily edits two pinned base files).

Do-nothing control: `... --lane $S/tip --do-nothing-control` (counter replaced by a stub that prints 7/7). Exact last lines (rc 1):
```
probe       probe-entry-pad-is-garbage-bytes fixed=7/7 failing=[] (ACCEPTED) -- G6 floor is bytes, not content
selftest cases=148 failures=123
```
123 = 122 mutants + the null tree; all 25 controls stay `ok` (a stub cannot fail a "must be 7/7" control, as designed), and `grep '^FAIL' | grep -vc 'ACCEPTED\|null'` printed 0.

## F4. What changed against the wave-1 file (draft vs lane copy)
1. Synthetic complete tree meets v1.1: the byte pad moved to the preamble (outside every required section), each required section has its own prose (>= 25 words; Falsifiable >= 12, margin asserted in the harness via an independent `sect_words`), the table sits under its own `## Page text, by question` heading, the cross-references under `## Related entries`; 8 table rows, 7 with a located `S073.txt:N` cite; every quote inside lines 556-583 and <= 12 lines. The S073 row has kind `docs`, scope/teaches >= 8 words, a locator (`L560`, `L567-L579`) and the sha. 65 entries. Entry trimmed so the 3000-byte boundary control still fits (first attempt: `selftest harness bug: cannot fit 3000 bytes (base 3232)`).
2. 53 new cases, one or more per v1.1 limb, each named for its wave-1 report in its `note`: section floors at N and N-1 words (4+4), emptied Limits, six-rows-one-uncited, junk rows, rows without numeric cite; G3 row content (scope, teaches, locator, recheck cell, filler cells, wrapped URL, registry sub-heading reset, second URL after canonical as a control); G4 repinned manifest cases; G5 window boundaries (556 pass / 555 fail, 583 pass / 584 fail, 12 lines pass / 13 fail, `1-589`, `0-577`, chrome line 552), core row in comment / fence, ASCII-quoted fabricated, uncited and wide-cited, ASCII-quoted real quote as a control; G6 non-md, hidden file, nested md.
3. C1-landed tree: `land_c1` copies the lane's re-grounded `claim-gates.md` and `claim-package-contract.md` over the base's (harness asserts the bytes differ from the base's, so the control is not vacuous): `ctl-c1-landed-two-entries` reads 7/7; renaming or deleting an exempt entry, or changing a third entry on top, reads G6 red. `ctl-committed-tip-direct` runs the counter on `--lane` itself: `fixed=7/7`.
4. The wave-1 "mutant" `mut-fabricated-quote-in-fenced-block` is now a probe: v1.1 G5 reads live lines only, so a fenced fabrication is not graded (`probe-fabricated-quote-in-fenced-block ... ACCEPTED`). Probes that v1.1 now rejects were promoted to mutants (1-589 window, chrome line, ASCII-quoted fabrication, nested md, junk table). `mut-census-bad-kind` and `mut-census-bad-recheck` now allow G3 collateral (v1.1 G3 reads kind and recheck cell too).
5. Seat scratch dir renamed `R46W2ExecSelftestC2`; `Case` gained `direct` and `repin`.

## F5. A counter fact found while building the manifest cases
`r46-c2-gate.py` (tip) docstring/comment line 66 says "a null value disables that one pin", but `g4` compares `sha(man) != PINS["manifest.json"]` with no `is not None` guard. Observed: with override `{"manifest.json": null}` the unedited re-serialised manifest read `gate G4 pass=0 read=manifest-not-the-pinned-bytes` (selftest FAIL on `ctl-manifest-reserialised-pin-off`, run 1). So null does not switch the manifest pin off; the draft instead writes a per-case override that pins the manifest to the EDITED bytes (`repin=True`), which reaches the distinctness limb. Not a gate defect for grading (the real pin is correct); the comment is inaccurate for that one key. Left as is (the counter is frozen/errata-controlled).

Direct isolation checks (v1 vs v1.1 on a copy of the tip, manifest edited and repinned): duplicate quote `Q9`: `dup-quote v1 ['gate G4 pass=1 read=recheck-rc=0 quotes-ok=9 ...']` vs `dup-quote v1.1 ['gate G4 pass=0 read=recheck-rc=0 quotes-ok=9 ...']`. Two distinct texts moved onto line 560 (six distinct anchors): `anchors-collapsed2 v1 [... pass=1 ...quotes-ok=8]` vs `v1.1 [... pass=0 ...quotes-ok=8]`, every quote `OK ... anchor=560-ok` in source-recheck. A bare anchor edit with unchanged texts reads BROKEN in source-recheck itself and so would not isolate the limb; that variant was dropped.

## Limitations
- Ran against the tip export, not the lane working tree through the default `--lane`; the lane tree equals the commit per the assignment but I did not run the default path.
- Synthetic tree = pure base (914ca0b) + generated F28/S073/entry + the lane's capture/manifest; the real entry/row bytes are graded only by `ctl-committed-tip-direct` (7/7), not mutated.
- Accepted by design and printed as probes (7): single curly quotes uncited, unquoted false prose, fabricated quote in an HTML comment, fabricated quote in a fenced block, unclosed HTML comment before the F28 row, four-tick fence with inner three-tick line, garbage pad bytes. None is a v1.1 limb.
- Some mutants share a gate with others by construction (G7 collateral allowed on G3 row mutants); collateral outside target|allow is a failure, so a mutant that also trips an unrelated gate would have been flagged.
- Run time about 2 minutes per full run (148 tree copies); no tool was installed or upgraded. No labrat probe spawned. Scratch (`/fast/scratch/hyaku/kasegi-r46/R46W2ExecSelftestC2`) removed before yield.
