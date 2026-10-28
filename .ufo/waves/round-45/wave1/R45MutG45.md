VERDICT: BROKEN

# R45MutG45: C2 mutation test of counter gates G4 (manifest/recheck) and G5 (entry quote location)

Scope: `corpus/instruments/r45-c2-gate.py` read-only (not edited). Eight single-hunk mutants were applied to scratch copies of a satisfied hand-built tree, and the unmodified counter was run on each. Five of the eight mutants are NOT rejected by the target gate. Those five are the finding.

## Survivors (defect present, target gate still passes)

1. **g4-core-moved-to-note** (G4). Edit to `corpus/source-snapshots/round-45/manifest.json`, the Q4 record's quote line:
   - OLD: `"quote": "By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug."`
   - NEW: `"quote": "without consent from the reporter, unless they are already public.", "note": "By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug."`
   - Result: `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`. The frozen core "cannot be reproduced, it is not exploitable" is no longer a pinned quote; G4 accepts it because `MANIFEST_CORES` is a substring test over the whole manifest text (`r45-c2-gate.py:163-164`), not over the S071 quote list.
   - Cause: `r45-c2-gate.py:163-165` (`mt = norm(manifest text)`, `miss = [c ... if norm(c) not in mt]`).

2. **g4-unique-anchor-out-of-range** (G4). Edit to the manifest:
   - OLD: `"anchor": 39,`
   - NEW: `"anchor": 9999,`
   - Result: `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`. The source-recheck receipt printed verbatim: `S071:Q3 OK normalized=markup-whitespace occurrences=1 anchor=OUT-OF-RANGE`.
   - Cause: G4 rejects only the substring `BROKEN` (`r45-c2-gate.py:165`). `source-recheck.py:108-109` emits `OUT-OF-RANGE` for the same anchor, and `source-recheck.py:192` enforces anchors only for non-unique quotes, so a dead pin on a unique quote is never failed.
   - Contrast (run separately): anchor 40 on the same unique quote gives `S071:Q3 OK normalized=markup-whitespace occurrences=1 anchor=40-BROKEN` and `gate G4 pass=0 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`. So the survival is specific to the out-of-range branch that the counter does not string-match.

3. **g5-embargo-exception-dropped** (G5). Edit to `corpus/knowledge/linux-kernel-security-bugs.md`:
   - OLD: `“for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days” (`S071.txt:310-311`)`
   - NEW: `“for up to 7 calendar days” (`S071.txt:310-311`)`
   - Result: `gate G5 pass=1 read=spans=5 located=5 failed=0 cores=4/4`. The entry now reports the 7-day ceiling as the whole embargo with the 14-day exception removed, and the claim text requires "7-day embargo ceiling with 14-day exception". G5's core regex for this limb is `up to 7 calendar days` (`r45-c2-gate.py:49`), which is a prefix of the full frozen sentence, so the missing exception passes.

4. **g5-uncited-fabricated-quote** (G5). Edit to the entry:
   - OLD: `(`S071.txt:39-40`).`
   - NEW: `(`S071.txt:39-40`). Disclosure is “reports are published within 30 calendar days of receipt” by the security team.`
   - Result: `gate G5 pass=1 read=spans=5 located=5 failed=0 cores=4/4`. The span regex (`r45-c2-gate.py:175`) requires a backticked `S071.txt:N` citation directly after each curly-quoted span, so the fabricated claim is never counted. The docstring promises that "an entry that quotes text the source does not hold cannot satisfy" (`r45-c2-gate.py:7-8`), and this does not hold for uncited quotes.

5. **g5-cite-widened-to-file** (G5). Edit to the entry:
   - OLD: `(`S071.txt:39-40`).`
   - NEW: `(`S071.txt:1-372`).`
   - Result: `gate G5 pass=1 read=spans=5 located=5 failed=0 cores=4/4`. Window is `snap[max(a-1,0):b]` (`r45-c2-gate.py:180`); a range covering the whole capture makes any located text pass. The citation's line pin is therefore not enforced.

## Rejected by the target gate (expected)

- **g4-sha-digit-flip** (G4): last hex digit of the pinned S071 sha256 changed. `gate G4 pass=0 read=recheck-rc=1 quotes-ok=0`. The source-recheck receipt: `S071:sha256 MISMATCH expected=0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f41 actual=0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40`.
- **g4-ai-core-paraphrased** (G4): manifest Q2 `…treat it as public` changed to `…treat it as private`. `gate G4 pass=0 read=recheck-rc=1 quotes-ok=4 frozen-cores-missing=1`. Receipt: `S071:Q2 MISMATCH reason=quote-not-found`.
- **g5-cite-misattributed** (G5): Q3 citation moved from `39-40` to `41-43`. `gate G5 pass=0 read=spans=5 located=4 failed=1 cores=3/4`.

## Controls (discrimination)

- Do-nothing (pure base export only): `control=do-nothing G4.pass=0 G5.pass=0 expect=0,0 counter-exit=1 c2-gate fixed=1/7 exit=1`; `G4 read: manifest-absent`; `G5 read: F27-rows=0`. The `fixed=1/7` value matches the frozen control line `control do-nothing-base counter=C2 c2-gate fixed=1/7 exit=1` in `.ufo/waves/round-45/controls/freeze-controls.txt:2`.
- Satisfied tree (base + snapshot dir + hand-built entry + F27 README row): `control=satisfied G4.pass=1 G5.pass=1 expect=1,1`; `G4 read: recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`; `G5 read: spans=5 located=5 failed=0 cores=4/4`. The overall counter exit is 1 only because G3 (no S071 SOURCES row in this hand-built tree) is red and I did not build that row, which is out of scope for G4/G5.
- Recipe integrity: lane inputs (`S071.txt`, `S072.txt`, `manifest.json`, counter) hashed before and after; all unchanged (`lane-inputs-unchanged 1`). Every mutant was applied to a fresh copy; each edit asserted exactly one occurrence of OLD before replacement (`edit precondition failed` guard). Mismatches vs the designed expectation: 0.

## Summary

`mutant=<name> rejected=<0|1>` as printed by the recipe:
```
mutant=g4-sha-digit-flip rejected=1
mutant=g4-ai-core-paraphrased rejected=1
mutant=g4-core-moved-to-note rejected=0
mutant=g4-unique-anchor-out-of-range rejected=0
mutant=g5-embargo-exception-dropped rejected=0
mutant=g5-uncited-fabricated-quote rejected=0
mutant=g5-cite-widened-to-file rejected=0
mutant=g5-cite-misattributed rejected=1
```
Survivors: 5 of 8 (listed above). SUMMARY line from the run: `g4-sha-digit-flip=1 g4-ai-core-paraphrased=1 g4-core-moved-to-note=0 g4-unique-anchor-out-of-range=0 g5-embargo-exception-dropped=0 g5-uncited-fabricated-quote=0 g5-cite-widened-to-file=0 g5-cite-misattributed=1`.

Possible counter errata (predicate-preserving, per the claims kill rule): (a) reject `OUT-OF-RANGE` alongside `BROKEN` in G4 and require each frozen core to sit inside a quote with the S071 id, not anywhere in the manifest; (b) require the G5 core check to match the full frozen sentence (including "14 calendar days") rather than the prefix; (c) flag any curly-quoted span with no citation, or any citation outside the located window. I did not edit the counter; these are recommendations for the L1.

## Limitations

- The satisfied tree is hand-built from my own entry text, not the lane's F27 entry (not yet authored in the lane). Survivors are therefore shown against my entry shape; the real entry may differ, but the G4/G5 code paths exercised are the same.
- Only G4 and G5 were attacked; G1, G2, G3, G6, G7 were not targeted. G3's red state in the satisfied control is a tree-building gap, not a finding.
- "Rejected" means the target gate printed `pass=0`; I did not separately confirm the overall counter exit, which is 1 in every tree for the G3 reason above.
- Survivors 4 and 5 depend on the counter's documented scope (curly spans with a following citation; "located in lines N..M"). I report them as gaps in the counter's stated intent, not as violations of its literal text.
- Only one contrast run was made for the anchor finding; I did not separately mutate other unique-quote anchors.
- Scratch dir `/fast/scratch/hyaku/kasegi-r45/R45MutG45` (recipe script, trees, run log) removed after the run; the exact OLD/NEW edits are quoted above so the recipe can be re-created.
- No tools installed; no git/jj mutation; no lane file was written except this report.
