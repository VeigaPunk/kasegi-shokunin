VERDICT: BROKEN

# R46W2CritErratum — counter-classification critic (counter-errata.md, v1 -> v1.1)

Seat: R46W2CritErratum (leaf critic, read-only; this Report is the only write). Lane: kasegi round 46. Tip `5437afeaf9b642c267bba3c31f00ae701e49da68` (lane HEAD `0d121a2`, tracked tree equal to the tip). Freeze `9f23aab`. Base `914ca0b`. Tip and base were exported with `git archive` into scratch; the frozen v1 counters were read with `git show 9f23aab:...`. Scratch was removed on exit. No commit, index or git mutation.

Bottom line:
- The plain re-derivation at the end of counter-errata.md HOLDS. Every printed value reproduces.
- The ruling's stated basis is BROKEN. The erratum says every v1.1 change is "the sentence made literal" and that the v1.1 pass set is "narrower than v1's". Neither holds as written: (a) five C1 limb sentences (L3-L7) were rewritten, and four of them now require something the frozen text does not say; (b) no C2 gate sentence changed (only the header line), so every C2 change is a new code-side requirement; (c) the C2 pass set is not narrower: at the tip v1 reads `c2-gate fixed=6/7` and v1.1 reads `7/7`; (d) the kill-rule parenthesis the erratum leans on covers "bug fixes that keep a limb's sentence", and L3-L7 do not keep their sentences; (e) the round-45 precedent kept the limb sentences unchanged.

## 1. Frozen claim text vs the v1.1 change, as a prose predicate

`git diff 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5 5437afeaf9b642c267bba3c31f00ae701e49da68 -- .ufo/waves/round-46/claims.json` printed 0 bytes. `sha256sum .ufo/waves/round-46/claims.json` = `e56ebf872b6073964d98812608275f5799afc9ee2334d4aab1363c06e59cd740`, equal to `freeze.txt` `claims-sha256`. The C1 and C2 `after` sentences and kill rules are therefore literally unchanged. The question is the counter's limb sentences, which the errata's basis (1) names.

Kill-rule clauses, quoted from claims.json:
- C1 kill_rule: "...or if the counter's seven limb sentences change after a seat has scored (bug fixes that keep a limb's sentence are logged as counter errata in counter-errata.md with a plain re-derivation that does not use the counter)."
- C2 kill_rule: "C2 fails if r46-c2-gate.py prints fixed<7/7 at the final lane revision; or if any control (...) grades 7/7; or if the non-author closure re-opening the page does not locate the cited quotes; or if the entry restates the page without a decision rule a reporter can act on. The target (28 admitted rows, 65 entries) is not narrowed after landing."
- C2 has NO limb-sentence clause. The erratum's kill-rule basis (item 2) therefore covers C1 only.

Docstring diff, `git show <rev>:corpus/instruments/r46-c2-gate.py` (v1 vs tip), first 45 lines: the only change is line 2 (`v1.` -> `v1.1 (hardened ... erratum E1 ...)`). All seven C2 gate sentences (G1-G7, lines 12-31) are byte-identical to v1. The errata's sentence "the seven C2 gate sentences changed only where a wave-1 falsification showed the CODE did not do what the SAME sentence says" is therefore not a description of what happened; for C2 no sentence changed and the code changed.

C1 docstring diff, v1 vs tip: lines 27 (token >= 6 -> >= 8), 31-36 (L3-L7 rewritten) and the mode paragraph (lines 37-40) changed. L1 and L2 sentences are unchanged.

## 2. Limb-by-limb: frozen sentence vs v1.1 sentence and code

C1 (v1 sentence first, then v1.1 sentence, then the code that enforces it, then my verdict):

- L3. v1: "recheck line names no ~/ or $HOME path and runs this gate's --entry mode on itself". v1.1: "exactly one `recheck:` line, and it is `cd <lane> && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<itself>.md` (optional trailing ` # comment`), no ~/ or $HOME path". Code: `exact_line()` (tip lines 70-72), `n != 1` (line 230). Frozen claim: "a recheck line that runs `r46-c1-gate.py --entry` on itself with no ~/ or $HOME path". Verdict: PARTLY EXTENDED. "exactly one" is not stated (it does close a shadow-line attack, R46RevC1L1 Finding 2). The cd prefix is the lane's own convention: `grep -h '^recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ' corpus/knowledge/*.md` over the base gives 63 of 64 recheck lines. Defensible, but the hard-coded `/home/vgpnk/...` (LANE_CD, line 60) makes every re-grounded entry fail L3 on any other HOME (a portability cost the erratum does not disclose).

- L4. v1: "per-entry mode (this script's own bytes, not the tree's) exits 0 at TREE". v1.1 adds "and every anchored file is byte-identical to BASE's"; code lines 243-246 (`read(bp) == read(tp)`), and line 140 excludes anchors named `r46-c1-gate.py`. Frozen claim: "re-grounded on committed bytes" and "committed anchor path:line". Verdict: EXTENDED. "Committed" is read as "present, unchanged, at BASE". That is a defensible anti-planting choice (the erratum's stated reason), but it is not the sentence made literal. Tip is unaffected: both anchor files are base files.

- L5. v1: "every BASE line except the recheck line is, in order, a prefix of TREE's". v1.1 adds "and the BASE recheck command survives verbatim as one `restoration-recheck:` line". Frozen claim: "every BASE line kept (append-only)". Verdict: DEFENSIBLE LITERALIZATION, the closest of the set. The claim keeps every BASE line and also drives gated 24 -> <=22, so the old recheck line must stop being a `recheck:` line; `restoration-recheck:` is the only form that keeps its text. Still a reinterpretation (the BASE line is not kept as written). Tip: `diff` of the BASE recheck command against `restoration-recheck:` prints nothing for both entries (plain check below).

- L6. v1: "blanking that row's token ... turns per-entry mode non-zero". v1.1: "after an unmutated scratch copy reads green, blanking that row's token ... turns per-entry mode red on exactly that row" (code lines 263-301: green precondition, `red != [r[0]]`). Frozen claim: "blanking the row's token in a scratch copy turns the entry check red." Verdict: PARTLY EXTENDED. The green precondition is harness hygiene (R46RevC1L6 Finding 3). "Exactly that row" is not in the claim.

- L7. v1: "entries gated at BASE and still gated at TREE keep their BASE recheck line byte-identical". v1.1: "are byte-identical to BASE" (code line 305 compares whole-file text). Frozen claim: "Entries still gated keep their BASE recheck line byte-identical." Verdict: NOT LITERAL. The sentence protects one line; v1.1 protects the whole entry. The motivating wave-1 report, R46RevC1L7, says itself: "Cheap hardening exists but is the counter author's call"; its construction A edits a still-gated body (scrubbing provenance markers) and leaves the recheck line untouched, which the frozen sentence does not forbid. At the tip nothing changed in still-gated entries, so the tip reads the same either way.

- Token length (C1 docstring line 27): v1 ">= 6 chars", v1.1 ">= 8 chars" (code MIN_TOKEN line 59). Frozen claim is silent. EXTENDED (minor).

- L1 and L2: sentences unchanged. Their measurement changed through `classify()` (C1-E6): lines that are not allow-listed are now "broken" and rechecks run under a minimal environment. This is a method change, disclosed as C1-E6. Base reads `gated=24 broken=0` and tip `gated=22 broken=0` under it (reproduced below).

Tally for C1: L5 defensible; L3 (cd form) defensible, "exactly one" extended; L4, L7 clearly extended; L6 "exactly that row" extended; token >= 8 extended. Five of seven limb sentences changed, and each changed sentence states a requirement the frozen claim sentence did not state, except L5.

C2 (no sentence changed; the code is what changed). The v1.1 code requirements that the unchanged sentence does not state:
- G2: each section >= 25 words (code line 202; the erratum's "package rule >= 12" is claim-package-contract's rule, not C2's); table rows must be 3 cells of >= 2 words each with an `S073.txt:N` cite (lines 205-208); the recheck line must name `round-46/manifest.json` (line 200). Sentence: "carries the four sections ..., >= 6 table rows and cross-references (file:line, in range)".
- G3: `kind == docs`, scope >= 8 words, teaches >= 8 words, recheck cell a cadence or date, anchor cell names `S073.txt` and a locator, first URL equals canonical, registry rows read only under `## Registry` (lines 138-147, 242-254). Sentence: "11 cells, tier A, status mined, opened 2026-10-28, source cell holds the canonical URL, used-by lists the entry path, the anchor cell carries the snapshot's sha256."
- G4: quotes pairwise distinct, equal to the OK count, >= 7 distinct anchors (lines 272-273); the threshold is `oks >= 8` (line 276). Sentence: ">= 8 quotes OK". The claim says "eight located manifest quotes". Code accepts nine or more.
- G5: spans must lie in the page body, lines 556-583 (BODY, line 69; check line 296); each cited span <= 12 lines (line 296); ASCII-quoted spans of >= 4 words must be cited and located (lines 288-289, 301); HTML comments and fences are ignored (lines 114-126). Sentence: "every curly-quoted span followed by a backticked `S073.txt:N[-M]` citation is located ... in snapshot lines N..M, every span is <= 25 words, at least four pass, no curly quote is uncited, and the five frozen cores each appear inside a located span." The erratum says so itself (C2-E4); the sentence does not.
- G6: sentence "`find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` == 65 and the other 64 files are the round-46 tip's bytes." Code: two base entries exempt (CONTENT_EXEMPT, line 68), so 62 are pinned; the entry must be >= 3000 bytes (line 319). The sentence is now false (it still says 64). The loosening is the erratum's C2-E5 and is justified by the joint-tip conflict (below), but the docstring was not updated and the erratum does not say the pin value changed (v1 `base-knowledge-content` f734506f... -> v1.1 5e0796fd...).
- G7: sentence "`sources-census.sh validate --file <root>/corpus/SOURCES.md` exits 0." Code also requires an `ok` line (line 325) and a fixed fleet-root path outside the lane (CENSUS, line 54, `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`). The counter's reading therefore depends on a file outside the lane.
- G1: no material change (dead code `or (False)` at line 179; harmless).

## 3. Measured: the counters, tip and do-nothing controls

All commands are read-only; output quoted from my runs.

Counter v1.1 at tip (`python3 -I corpus/instruments/r46-c1-gate.py --root <tip> --baseline <base>`):
```
gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-exact=2
gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
gate L5 pass=1 read=append-only-restoration-kept=2
gate L6 pass=1 read=mutants=46 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```
Counter v1.1, do-nothing (base as tree): `gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64` ... `c1-gate fixed=1/7 exit=1`.
Counter v1 at tip: `c1-gate fixed=7/7 exit=0` (every limb pass=1). So the C1 tip reading does not discriminate v1 from v1.1; the disputed changes matter only to trees built by the wave-1 attacks.

Counter v1.1, C2 at tip: `gate G1..G7` all `pass=1`, `c2-gate fixed=7/7 exit=0`. Counter v1.1, C2 do-nothing (base): `c2-gate fixed=1/7 exit=1`.
Counter v1, C2 at tip: `gate G6 pass=0 read=knowledge=65 base-names-intact=0 entry-bytes-ok=1`, `c2-gate fixed=6/7 exit=1`. Counter v1, C2 at base: `c2-gate fixed=1/7 exit=1`.

So the errata's basis (3), "The v1.1 pass set is narrower than v1's", is false for C2: the tip is accepted by v1.1 and rejected by v1. The G6 change loosens the gate (the joint-tip cause is real: I recomputed the v1 content pin over all 64 base entries, `all64 64 f734506f3041f6802602ba43c8ce7164f7df156c176b48a51549cd809171e4df`, which equals v1's pin, and over the 62 non-exempt entries, `62-exempt 62 5e0796fd3617f7626880950a5b25d1818f58eff58a12dec99ce7a0f3836b8f47`, which equals v1.1's pin; `names64 bf3044814698b31b2d63a47ef6933cfe4d2d09635c2d717b05c8adf0bf719f5d` is unchanged in both). The erratum's attribution of the v1 G6 failure to the C1 edits is correct.

Frozen controls (`.ufo/waves/round-46/controls/freeze-controls.py --lane <lane> --base 914ca0b... --work <scratch>`, run against the lane's v1.1 counters): `controls total=9 red=9 green=0`, so no control reaches 7/7. But the output is NOT the frozen receipt: diffed against `controls/freeze-controls.txt`, all nine control blocks differ, for example `c1 marker-only` `c1-gate fixed=3/7` -> `2/7` (its L1 now `broken=2`), `c2 junk-row` `c2-gate fixed=4/7` -> `3/7` (G3 now fails `bad=scope-words,teaches-words,anchor-locator`), `c1 gutted-entry` `6/7` -> `0/7`. The round-46 controls directory has no v1.1 receipt. Round 45 recorded one for each counter version (`.ufo/waves/round-45/controls/freeze-controls-v1.1.txt`, `freeze-controls-v1.2.txt`). The errata does not mention the stale receipt.

## 4. Re-derivation of the claim by plain commands (no counter)

Run at the tip export (file reads) and against the lane's git history (`git -C <lane> ...`). Output quoted.

```
## C1 1: recheck shape per re-grounded entry (expect 1 and 1)
corpus/knowledge/claim-gates.md:1
corpus/knowledge/claim-package-contract.md:1
## C1 2: restoration diff (expect no output)
claim-gates restoration identical
claim-package-contract restoration identical
## C1 3: numstat (expect deletions 1 each)
36	1	corpus/knowledge/claim-gates.md
30	1	corpus/knowledge/claim-package-contract.md
## C1 4: plain rows (controls/plain-rows.sh)
rows=25 located=25
rows=21 located=21
## C1 5: recheck-audit (instrument of record, not a counter)
tip:  executes=43 gated=22 broken=0
base: executes=40 gated=24 broken=0
## C1 6: plain test -d count
tip 21, base 23
```
Note on the errata's arithmetic: recheck-audit's `executes` counts non-gated lines (`executes = len(entries) - fail_closed`, recheck-audit.py line 426), so 43 = 40 base + 2 re-grounded + 1 new F28 entry, which the errata's sum gives. The label "40 base executing lines" is correct only under that reading.

Score gap (`score-gap.py` run in each tree's own copy): base `gap: 24 of 64 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`; tip `gap: 22 of 65 rechecks still gated ...`.

C2 plain set (claims.json `plain`, which the errata does not reproduce):
```
base: README F rows 27, SOURCES S rows 72, knowledge 64; absence sweep: (none)
tip:  README F rows 28, SOURCES S rows 73, knowledge 65;
      absence sweep: corpus/knowledge/github-private-vulnerability-reporting.md
                     corpus/SOURCES.md
                     corpus/README.md
source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073:
      S073:sha256 OK ... S073:Q1..Q8 OK ... rc=0
sources-census.sh validate (tip SOURCES.md): file ok ... census rc=0
```
Quotes, plain (Python, whitespace-normalised substring of the cited capture lines): 21 of 21 curly spans with an `S073.txt:N` cite located, 0 failed. The entry's own quotes are located in the capture.

Gaps in the claim that no counter gates: the claim asks for "a stated contrast with F27 (AI-assisted finds) and F04". The tip entry contrasts F27 by name (line 30) and contrasts `corpus/knowledge/ai-assisted-finding-validation.md` (line 31; the file behind README row F04) without writing "F04". Satisfied by file reference; no gate checks it. The decision rule (line 13) and falsifiable rule (line 49) are present.

## 5. Precedent test (round-44/45)

Round-45 counter v1 -> v1.2 (`git show 8cf62c8:corpus/instruments/r45-c2-gate.py` vs `git show 3106889:...`): the docstring keeps all its limb sentences; the only additions are a header line and a paragraph "VERSION 1.1 (erratum E1, predicate and gate names unchanged; ...)". The round-45 errata (`.ufo/waves/round-45/counter-errata.md` line 3) says "The predicate sentences of both claims ... are unchanged. What changed is the code that reads them." Round-45 spot-check section 2 rules erratum on three grounds: frozen claim sentences unchanged; kill rule parenthesis "exempts 'bug fixes that keep the predicate'"; plain re-derivation agrees. Round-45's own errata (line 24) says the wave-2 critic called the v1.1 changes "new pass conditions, not bug fixes" and the closure "picks one".

Against that precedent, round 46:
- claim sentences unchanged: YES (claims.json empty diff). Precedent met.
- counter limb sentences unchanged: NO for C1 (L3-L7 rewritten), YES for C2 (code-only). Round 45 was code-only. Precedent does not cover C1 L3-L7.
- kill-rule parenthesis: round-45 "bug fixes that keep the predicate"; round-46 C1 "bug fixes that keep a limb's sentence". The round-46 wording is the narrower one, and L3-L7 do not keep their sentences.
- plain re-derivation: present for C1; absent from the errata for C2 (I ran the claims.json list above and it holds).
- controls receipt per version: round 45 yes; round 46 no (section 3).
- "narrower pass set": round 45 stated it and was true; round 46's C2 is not narrower (section 3).

Round 44 was cited only second-hand (round-45 section 2); I did not read its errata.

## 6. Strongest objection to this verdict, and the rebuttal

Objection: the disputed changes do not move any tip reading. C1 reads 7/7 under v1 and v1.1 at the tip. The only tip reading that moved is C2 G6, and that move is a loosening. A closure that only cares about tip readings should accept the erratum, and the reviewers (R46RevC1L5, R46RevC1L7) themselves describe L5 and L7 as "the frozen sentence".

Rebuttal: (1) The erratum's stated basis is what the closure will rely on, and that basis is false for L3-L7 and for the C2 gates (section 2). (2) The reviewer reading supports L5 and the whole-file L7 only as a hardening ("the counter author's call", R46RevC1L7), and its construction A does not touch the recheck line the sentence protects. (3) The C1 kill rule makes the limb-sentence text the test; the erratum's parenthesis covers only bug fixes that keep a sentence. (4) The round-45 precedent kept limb sentences; round 46 did not. Defensible as a ruling would need the explicit per-limb split, not the sentence-literal claim.

## 7. Smallest safe correction (for the L1 to decide)

1. Replace "every v1.1 change is the sentence made literal" with a per-limb table (section 2). Classify L4, L6 ("exactly that row"), L7, the token threshold, and the C2 gate additions (G2-G7) as new pass conditions. Either (a) the closure rules them a changed rule under round-45 section 6 item 9, or (b) restore the v1 limb sentences and add the v1.1 requirements as a labelled "v1.1 requirement" paragraph, the round-45 pattern.
2. Correct the C2 G6 docstring: 62 base entries pinned, two named exemptions, pin value changed. State the loosening as a loosening.
3. Strike "narrower pass set" or restrict it to the limbs where it holds; at the tip C2 v1.1 accepts what v1 rejects.
4. Record a v1.1 controls receipt beside `freeze-controls.txt` (round-45 pattern). The frozen receipt no longer reproduces: all nine blocks differ; `red=9 green=0` holds.
5. Add the C2 plain re-derivation to the errata (the claims.json list above).
6. Disclose that L3's LANE_CD hard-codes `/home/vgpnk/Projects/shokunin/kasegi-shokunin`: a different HOME fails every re-grounded entry.

## Limitations

- I did not run the selftests (`r46-counters-selftest-c1.py`, `-c2.py`), the freeze-tree readings under v1.1, or `freeze-check.py`.
- The semantic question (do the rows support the entries) is for the non-author reading, not this seat.
- Wave-1 reports were checked by grep for the phrases the errata cites (R46MutC2a S1-S2, R46MutC2b M07/P4, R46RevC2G3, R46RevC1L7 A-C, R46RevC1L3 F2, R46Revenger planted-anchor, R46RevC1L5 F5, R46RevC1L1 F2); I did not re-run those attacks.
- Round-44 precedent is second-hand.
- The v1 C1 tip run used the tip's own instrument copy inside the recheck lines (the tree's rechecks run the tree's `corpus/instruments`); this affects only the rechecks, not the limb logic.
- `freeze-controls.py` was run with `--lane` pointing at the lane (its harness needs a git repo for `git archive`); it writes only to its scratch `--work`. Output was saved in scratch and removed.
- Sibling wave-2 drafts (for example `R46W2ExecControlsV11.draft/`) were not read.
