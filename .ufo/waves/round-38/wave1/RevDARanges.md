# RevDARanges — round 38: D-A fact verification (receipt only)

Seat: `RevDARanges` (leaf, reviewer; axis depth:verifiability). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only for this seat except this receipt).
Item: verify the D-A facts the round-38 Correction lines will state — the `git diff -U0 b56a4168 a173b0c2 -- PROVINCE.md corpus/README.md` hunks, the intended-amendment vs scaffolding split of PROVINCE.md L79-L152 and corpus/README.md L399-L454 (against `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md`), the README heading loss, and a recompute of the verifier's digests `cdfe44e3…` (2 lines) and `2ebd8cd2…` (27 lines); then grade the two `Correction (round 38)` lines in `wave1/ScribeFrontierBlocks.*.md` for factual accuracy. Receipt only — no deliverable file, no lane edit, no mutating git command, no network fetch, no tool install.

## 1. Diff hunks (measured)

`git -C <lane> diff -U0 b56a41680cefd391868c1c370dc063c69d827e7d a173b0c2b98c5ae39599fa9be76027fbbead0b9e -- PROVINCE.md corpus/README.md` → exactly two hunks:

```
@@ -78,0 +79,74 @@ against the round-31 capture `corpus/source-snapshots/round-31/S048.txt`.   (PROVINCE.md)
@@ -398,0 +399,56 @@ stays outside it.                                                          (corpus/README.md)
```

`git show <ref>:<file> | wc -lc`: PROVINCE.md 78 lines/4,954 B at b56a4168 → 152 lines/10,894 B at a173b0c2; corpus/README.md 398 lines/38,881 B → 454 lines/43,629 B. Pure additions, zero deletions. Exactly one commit in `b56a4168..a173b0c2` touched either file: `0acffc8` ("round-37: F0 integration — …README-PROVINCE…"); `83975acc` (r37 lane tip) is an ancestor of a173b0c2 (merge-base --is-ancestor → 0), whose tip parent is the verifier spot-check commit. So L79-L152 / L399-L454 is the whole round-37 append of each file.

## 2. PROVINCE.md L79-L152 — intended amendment vs scaffolding

- **L79-L80 = the intended amendment**, byte-identical to the receipt §2 declared block: L79 = blank line, L80 = `[r37 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F20 — SSVC … (source S054)`. The landed append starts with the declared block bytes (`prov_append.startswith(blockA) → True`).
- **L81-L152 = misplaced receipt scaffolding (72 lines), byte-identical to `ScribeFrontierAmendments.md` L52-L123** (verified by list equality). Map: L81 stray ` ``` ` (the receipt §2 block's closing fence, landing with nothing to close); L83-L88 the §2 property table (incl. the `cdfe44e3…` row); L90-L94 the §3 header + "Append verbatim at EOF…" instructions; **L96-L124 the complete intended README block embedded inside a ` ```text ` fence** (L97 = the `## Round-37 admission` heading — the heading survives in PROVINCE only inside this receipt copy); L126-L132 the §3 property table (incl. the `2ebd8cd2…` row); L134-L152 the §4 "Validation on a scratch mirror" heading, fixture paragraph, 8-row check table and the harness-tail intro line `--root <mirror>`, tail):`. The paste stops at receipt L123; receipt L125-L129 (harness output fence) and §5-§6 were not pasted.
- **Fences**: three fence lines (L81 ` ``` `, L96 ` ```text `, L124 ` ``` `); whole-file ` ``` ` count = 3 (odd, unbalanced); base file had 0. Render semantics [INFERENCE, CommonMark]: L81 opens a fenced block that L124 closes (L96's info string disqualifies it as a closer), so L82-L124 render as one code block; the file is not open-at-EOF.
- **Duplicated F20 row**: the six-cell F20 row sits at PROVINCE L114 (inside the embedded receipt copy) and is **byte-identical (1,223 B) to README L416's F20 row**; it is the only F20 row in PROVINCE. PROVINCE's own amendment style (base L77-L78) is one `[rNN Frontier amendment…]` line per admission, so the row-shaped table is receipt furniture, not province content.

## 3. corpus/README.md L399-L454 — the heading loss

- **L399 = an extra blank line** belonging to no declared block (the declared instruction said the block starts directly with `##`, "no extra leading newline").
- **L400-L425 = the declared 27-line block minus its first line**, byte-identical (2,865 B) to `ScribeFrontierAmendments.md` §3 block lines 2-27 (paragraph, Area table, six-cell F20 id-table row at L416, count paragraph, trailing blank).
- **The heading `## Round-37 admission — coverage map row and Frontier F20 (appended 2026-10-26)` never landed**: no line in README@a173 starts with it; the string survives only inside the pasted §4 check-table grep command at L448 (`| section header | grep -c '^## Round-37 admission' … | 1 |`). README lost its heading — verified.
- **L426 = a stray ` ``` `** (receipt L95, the §3 block's closing fence, landing where no fence is open). Whole-file ` ``` ` count = 1 (odd); since README@base had zero fences, L426 opens an unclosed fenced block at EOF and L427-L454 render as code — matches c1-controls/before.txt: "opener at 426 never closed: open-at-EOF=1".
- **L427-L454 = receipt scaffolding, byte-identical to `ScribeFrontierAmendments.md` L96-L123** (29 lines: §3 property table, §4 "Validation on a scratch mirror" + check table, harness-tail intro). Receipt L125+ not pasted.

## 4. Digest recompute — both declared digests verify exactly

Block bytes = the receipt's fenced block content + trailing newline (the bytes as appended). Recomputed with Python `hashlib.sha256` over `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md` §2/§3 fenced blocks:

| declared | recomputed | bytes/lines | verdict |
|---|---|---|---|
| `cdfe44e319094957ec583b7c3cd8212b882752b75682d9f1cf4d0b734f20f545` (2 lines) | `cdfe44e319094957ec583b7c3cd8212b882752b75682d9f1cf4d0b734f20f545` | 295 / 2 | **exact match** |
| `2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b` (27 lines) | `2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b` | 2,947 / 27 | **exact match** |

## 5. Grading the two Correction lines (ScribeFrontierBlocks.*.md, present on first check)

Deliverables found on check 1 of 3 (no 5-minute waits needed): `ScribeFrontierBlocks.province-eof.md` (900 B / 4 lines: L1 blank, L2 Correction, L3 blank, L4 the `[r38 Frontier amendment…]` F21 line; sha256 `797666b943244f9174b627918f84b9027858a6d4ffe0213c026c568ff1ed3acf`), `ScribeFrontierBlocks.readme-eof.md` (4,041 B / 32 lines: L1 ` ``` `, L2 blank, L3 Correction, then the F21 admission block; sha256 `f0318ac8306f52c8085c192ee0c32f8f72dd2f4f5675164294433c9210fbbdff`), `ScribeFrontierBlocks.readme-row.md` (1,267 B / 1 line, the F21 six-cell row). Exactly one `Correction (round 38)` line per front-door deliverable, each at a line start, so the G1 `^Correction (round 38)` grep will match once appended; readme-eof's first line ` ``` ` closes the L426-opened block before the Correction line, so the Correction renders as text.

**Correction line 1 (province-eof.md L2) — ACCURATE, no factual error.** Claim-by-claim: "L79-L152 — the whole round-37 append" ✓ (single hunk +79,74); "intended 2-line amendment at L79-L80 (a blank line and the `[r37 Frontier amendment…` line, sha256 cdfe44e3…)" ✓ exact, digest recomputed; "misplaced receipt scaffolding at L81-L152 copied from `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md`" ✓ byte-identical to receipt L52-L123; "a duplicated F20 row" ✓ (L114 duplicates README L416 byte-for-byte); "property tables" ✓ (L83-88, L126-132); "a 'Validation on a scratch mirror' section" ✓ (L134-152); "stray fences" ✓ (three fence lines, file count odd); "L81-L152 are to be read as not part of the province" — normative, consistent. Nuance (not an error): "a duplicated F20 row" is accurate as cross-file duplication (the row appears once in PROVINCE); a reader could misparse it as twice-in-file.

**Correction line 2 (readme-eof.md L3) — ACCURATE, no factual error.** Claim-by-claim: "L399-L454 — the whole round-37 append" ✓ (single hunk +399,56); "receipt property and validation tables, a 'Validation on a scratch mirror' section with its check table" ✓ (L427-454 = receipt L96-123); "a stray fence at L426 that leaves the rest of the file inside a code block" ✓ (open-at-EOF, matches before-control); "the intended round-37 block was 27 lines (sha256 2ebd8cd2…, the bytes of that receipt's §3 'Deliverable B — `corpus/README.md` end-of-file block')" ✓ recomputed exactly; "of which only L400-L425 landed unchanged" ✓ (block lines 2-27 byte-identical there); "L399 is a blank line where the block's `## Round-37 admission — coverage map row and Frontier F20 (appended 2026-10-26)` heading belonged" ✓ (heading absent as a line; L399 is an extra blank); "the fence opened at L426 is closed by this block, whose first line is the closing fence" ✓ (deliverable L1 = ` ``` `); "L426-L454 are to be read as not part of the corpus index" — normative, consistent.

Both Correction lines state only facts I could re-derive from the two commits and the r37 receipt; nothing over-claims. The F21 admission content in the same deliverables (S055 capture pins, 21/21 count line) is outside this item's scope and was not graded here beyond structure.

## 6. Tooling, scratch, hygiene

- No tool installed or upgraded (none needed); no pacman; no network fetch; interpreter Python 3.14.8, git 2.56.0 (preinstalled).
- Git usage read-only (`show`, `diff`, `rev-parse`, `log`, `merge-base --is-ancestor`, `status`), always `git -C <lane>`.
- Scratch `/fast/scratch/hyaku/kasegi-r38/RevDARanges/` (diff capture + four blob extracts) removed before yield; the only retained artifact is this receipt.
