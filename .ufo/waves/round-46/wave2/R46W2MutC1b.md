VERDICT: BROKEN

# R46W2MutC1b — C1 counter v1.1 mutation probe, limbs L4 (per-entry mode, anchors byte-identical) and L5 (append-only + restoration-recheck)

Target: `corpus/instruments/r46-c1-gate.py` (v1.1) at committed tip 5437afeaf9b642c267bba3c31f00ae701e49da68, base = pure export of 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba (`/fast/scratch/hyaku/kasegi-r46/L1/pure`, copied, not edited). Counter run from the lane instrument path: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-c1-gate.py --root <copy> --baseline <base copy>`. The lane was not modified; mutants were applied to copies of the tip export; scratch removed on exit.

## Survivors (counter did not reject; defect present)

Five of twelve single-edit mutants survive. Each survivor reads `c1-gate fixed=7/7 exit=0`.

1. **A3-l4-anchor-crlf-in-window** (target L4). Edit: `corpus/instruments/claim-package-check.py`, one inserted byte 0x0D (`\r`) at byte offset 11806, immediately before the LF ending line 308 (`    if isinstance(sequence, bool) or not isinstance(sequence, (int, float)):`). Sha256 8b6f84934915 -> 6cd6d1a192ec. Output:
   ```
   gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
   c1-gate fixed=7/7 exit=0
   ```
   Direct check (`python3`, the counter's own `read()` semantics): `text_equal= True bytes_equal= False splitlines_equal= True`. The anchor file is no longer byte-identical to BASE, yet L4 reads it as unchanged.
   Cause: `read()` at tip `r46-c1-gate.py:100-105` opens in text mode (`open(path, "r", encoding="utf-8")`, universal newlines), and the L4 planted check at line 244 is `read(bp) == read(tp)`. CRLF is folded to LF before comparison, so the limb's sentence "every anchored file is byte-identical to BASE's" is not what the code checks.

2. **A4-l4-anchor-lone-cr-for-lf** (target L4). Edit: `corpus/instruments/claim-package-check.py`, the LF at byte 11853 (ending line 309, `raise _GateFail('sequence=not-number')`) replaced by a lone CR. Sha256 8b6f84934915 -> 1fa0a7556acf. Output: `gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2`, `c1-gate fixed=7/7 exit=0`. `text_equal= True bytes_equal= False`. `python3 -m py_compile` on the mutated file prints `compiled-ok`, so the anchored source still compiles; the defect is the byte-identity claim, not the code.

3. **A6-l4-row-retarget-to-identical-base-file** (target L4; all seven gates green). Edit: `corpus/knowledge/claim-gates.md` row G24 (tip line 157), the anchor cell `` `corpus/instruments/fixtures/claim-package/defect-8-marker/expected-rule:1` `` replaced by `` `corpus/instruments/claim-package-selftest.py:84` ``. Token `R-REPORT` is unchanged. Base line 84 of `claim-package-selftest.py` is `    (("marker", "no-submission"), "R-REPORT"),`. Output:
   ```
   gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
   gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
   gate L5 pass=1 read=append-only-restoration-kept=2
   gate L6 pass=1 read=mutants=46 survivors=none
   c1-gate fixed=7/7 exit=0
   ```
   The row now cites a byte-identical base file that contains the token, not the fixture the claim names ("the committed defect fixture names R-REPORT"). The counter checks token location, not that the cited file is the claim's evidence. This is the declared semantic gap (kill rule: the non-author reading is the check), but it is an evidence-chain defect the counter passes.

4. **B3-l5-base-line-crlf** (target L5). Edit: `corpus/knowledge/claim-gates.md`, inserted byte 0x0D before the LF of base line 121 (`## Provenance (round-22 correction, appended)`). Sha256 a5837a2f4cfb -> ec6f0c8f421a. Output: `gate L5 pass=1 read=append-only-restoration-kept=2`, `c1-gate fixed=7/7 exit=0`. `text_equal= True bytes_equal= False splitlines_equal= True`. Cause: `entry_lines()` (tip lines 214-215) is `read().splitlines()`, which is blind to CRLF.

5. **B4-l5-base-newline-as-U+2028** (target L5). Edit: `corpus/knowledge/claim-gates.md`, the LF at byte 6429 (after base line 123, `source: [lost-tree] ...read.`) replaced by U+2028 (bytes e2 80 a8). Sha256 a5837a2f4cfb -> 5a7914269ab7. Output: `gate L5 pass=1 read=append-only-restoration-kept=2`, `c1-gate fixed=7/7 exit=0`. Cause: `str.splitlines()` splits on U+2028, so the counter's line model sees the same lines. A plain line-anchored grep does not:
   ```
   tip:                                  grep -c '^verified-at: 2026-09-28' = 1 ; splitlines-count = 1
   m/B4-l5-base-newline-as-U+2028:       grep -c '^verified-at: 2026-09-28' = 0 ; splitlines-count = 1
   ```
   The lane's plain-command audits (`grep -lE '^recheck:...'`, per claim.json `plain`) therefore disagree with the counter about this entry's lines.

## Rejected mutants (counter exit 1)

- A1-l4-anchor-append-outside-window (`# r46 mutation probe` appended to claim-package-check.py): `gate L4 pass=0 read=bad=claim-gates.md,claim-package-contract.md`, `c1-gate fixed=6/7 exit=1`. Caught by L4.
- A2-l4-anchor-trailing-space-in-window (one space before the LF of line 308): `gate L4 pass=0 read=bad=claim-gates.md,claim-package-contract.md`, `fixed=6/7`. Caught by L4 (the token window still matches after whitespace normalisation, so only the byte check catches it).
- A5-l4-row-anchor-dotdot (`corpus/instruments/../instruments/claim-package-check.py:307-309` in G2): `gate L4 pass=1 read=entry-mode-green-anchors-unchanged=1`, `gate L2 pass=0 read=base-gated=24 regrounded=1 claim-package-contract.md`, `gate L7 pass=0 read=still-gated=23 changed=claim-gates.md`, `c1-gate fixed=4/7 exit=1`. **Note:** rejected, but not by L4. claim-gates.md fails its per-entry check and so drops out of the regrounded set R that L4 iterates over. L4 is therefore blind to any entry whose per-entry check fails; L2/L7 catch it instead.
- B1-l5-base-history-rewritten (`verified-at: 2026-09-28` -> `2026-10-20`): `gate L5 pass=0 read=bad=claim-gates.md`, `fixed=6/7 exit=1`.
- B2-l5-base-line-deleted (the `source: [lost-tree] ...` line): `gate L5 pass=0 read=bad=claim-gates.md`, `fixed=6/7 exit=1`.
- B5-l5-restoration-command-edited (`test -d` -> `test -e` on the restoration line): `gate L5 pass=0 read=bad=claim-gates.md`, `fixed=6/7 exit=1`.
- B6-l5-restoration-line-deleted: `gate L5 pass=0 read=bad=claim-gates.md`, `fixed=6/7 exit=1`.

## Verbatim recipe output (`python3 recipe.py`, scratch, `tee` to recipe-run.txt)

```
mutant=A3-l4-anchor-crlf-in-window rejected=0 target=L4 target_gate=pass=1 red=none c1-gate fixed=7/7 exit=0
mutant=A4-l4-anchor-lone-cr-for-lf rejected=0 target=L4 target_gate=pass=1 red=none c1-gate fixed=7/7 exit=0
mutant=A6-l4-row-retarget-to-identical-base-file rejected=0 target=L4 target_gate=pass=1 red=none c1-gate fixed=7/7 exit=0
mutant=B3-l5-base-line-crlf rejected=0 target=L5 target_gate=pass=1 red=none c1-gate fixed=7/7 exit=0
mutant=B4-l5-base-newline-as-U+2028 rejected=0 target=L5 target_gate=pass=1 red=none c1-gate fixed=7/7 exit=0
mutant=A1-l4-anchor-append-outside-window rejected=1 target=L4 target_gate=pass=0 red=L4 c1-gate fixed=6/7 exit=1
mutant=A2-l4-anchor-trailing-space-in-window rejected=1 target=L4 target_gate=pass=0 red=L4 c1-gate fixed=6/7 exit=1
mutant=A5-l4-row-anchor-dotdot rejected=1 target=L4 target_gate=pass=1 red=L1,L2,L7 c1-gate fixed=4/7 exit=1
mutant=B1-l5-base-history-rewritten rejected=1 target=L5 target_gate=pass=0 red=L5 c1-gate fixed=6/7 exit=1
mutant=B2-l5-base-line-deleted rejected=1 target=L5 target_gate=pass=0 red=L5 c1-gate fixed=6/7 exit=1
mutant=B5-l5-restoration-command-edited rejected=1 target=L5 target_gate=pass=0 red=L5 c1-gate fixed=6/7 exit=1
mutant=B6-l5-restoration-line-deleted rejected=1 target=L5 target_gate=pass=0 red=L5 c1-gate fixed=6/7 exit=1
mutant=C0-control-unmutated-tip rejected=0 target=control target_gate=n/a red=none c1-gate fixed=7/7 exit=0
mutant=C1-control-benign-append-after-restoration rejected=0 target=control target_gate=n/a red=none c1-gate fixed=7/7 exit=0
mutant=D0-control-do-nothing-base-as-tree rejected=1 target=control target_gate=n/a red=L1,L2,L3,L4,L5,L6 c1-gate fixed=1/7 exit=1
```

Summary: 12 mutants, 7 rejected, 5 survived (A3, A4, A6, B3, B4). Controls discriminate: the unmutated tip reads 7/7 and the do-nothing base-as-tree reads 1/7; a benign append after the restoration line reads 7/7, so the append path is not over-rejecting.

## Mutant edit list (all single contiguous edits; each verified by a common-prefix/suffix span check)

| name | file | edit |
|---|---|---|
| A1 | corpus/instruments/claim-package-check.py | append `# r46 mutation probe\n` at EOF |
| A2 | claim-package-check.py | one space before LF of line 308 |
| A3 | claim-package-check.py | insert `\r` before LF of line 308 |
| A4 | claim-package-check.py | LF of line 309 -> `\r` |
| A5 | claim-gates.md G2 | anchor `claim-package-check.py` -> `../instruments/claim-package-check.py` |
| A6 | claim-gates.md G24 | anchor -> `corpus/instruments/claim-package-selftest.py:84` |
| B1 | claim-gates.md line 124 | `verified-at: 2026-09-28` -> `2026-10-20` |
| B2 | claim-gates.md line 123 | delete the `source: [lost-tree] ...` line |
| B3 | claim-gates.md line 121 | insert `\r` before LF |
| B4 | claim-gates.md line 123 | LF -> U+2028 |
| B5 | claim-gates.md line 126 | `test -d` -> `test -e` in restoration line |
| B6 | claim-gates.md line 126 | delete the restoration line |

## Recommendation (no edit made here)

L4 should compare bytes (`open(..., "rb")`), and L5 should compare line-level on bytes split on `\n` only, not `str.splitlines()`/text mode. The limb sentences say "byte-identical" and "append-only", so this is a bug fix that keeps the sentence; per the claims kill rule it must be logged as a counter erratum in counter-errata.md with a plain re-derivation. L4 also cannot see an entry whose per-entry check fails (it drops out of R); L2/L7 cover that, which is acceptable but should be stated. A6 is a semantic/anchor-provenance gap that no byte-level limb can close; it belongs to the non-author reading.

## Limitations

- 12 single-edit mutants chosen by hand, targeting L4/L5. The recipe ran all seven limbs on every mutant, but L1-L3, L6, L7 were not targeted and their coverage is not claimed. Not exhaustive; other separator bytes (U+000B, U+001C-U+001E, U+0085) are the same class as B4 by reasoning [INFERENCE], not run.
- Only claim-gates.md was mutated for L5; claim-package-contract.md shares the same code path but was not separately mutated.
- A3/A4/B3/B4 are byte/line-model defects. I did not show a behavioural change beyond the byte-identity and grep-line-model divergence (A4 compiles; B4 changes grep line counts).
- classify() runs `test -d ~/Projects/bounties` on this host, so all counts are measured under this HOME.
- Lane HEAD is 0d121a2; `git -C <lane> diff --stat 5437afe 0d121a2 -- corpus` printed nothing, so the corpus is identical to the tip. The counter and the two re-grounded entries in the lane were cmp-identical to the tip export.
- Runtime about 7.5 minutes (recipe run). No tools installed; no git mutation; no commit.
