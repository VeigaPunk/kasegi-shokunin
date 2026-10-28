VERDICT: BROKEN

# R46CritControls — controls critic, round 46

Scope: the frozen counters `corpus/instruments/r46-c1-gate.py` (C1, seven limbs L1–L7) and `corpus/instruments/r46-c2-gate.py` (C2, seven gates G1–G7), run from the lane's own copies against attack trees built from the pure base (`git archive 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba corpus`, verified identical to the pure copy). Attack trees live in scratch and were removed on exit. Nothing was committed or mutated; no shared file was touched.

Control reproduction (re-run): `python3 .ufo/waves/round-46/controls/freeze-controls.py --lane <lane> --base 914ca0b6… --work <scratch>` ends with `controls total=9 red=9 green=0`, and `diff` against `controls/freeze-controls.txt` printed nothing. The nine frozen controls are reproduced exactly.

Two of the four candidate families reach 7/7 on each counter. Each is a BROKEN verdict under the spec.

## C1 — depth:verifiability

### F1 (BROKEN) Self-authored anchor fixtures reach 7/7 with anchored lines that say the claim is false

Recipe (tree = base + edits):
- New files `corpus/instruments/r46-fx-a1.txt` = `status: NOT VERIFIED` / `six contract files present: false` / `R-FILES fails closed`; `corpus/instruments/r46-fx-a2.json` = `"six contract files present": false,` / `"NO_SCOPE_OBJECTION": false`. Same pattern for `b1.txt`/`b2.json` (`gate verdict: fail`, `G6 mutation survives`).
- In `claim-package-contract.md` and `claim-gates.md`, replace the `recheck:` line with `cd <lane> && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<e>` (copy the lane's gate into the tree's `corpus/instruments/`, as the controls do) and append `## Re-ground (round 46)` with six rows, two files per entry, e.g.:
  `| G2 | six contract files are present | `corpus/instruments/r46-fx-a1.txt:2` | `six contract files present` |`
  `| G5 | no scope objection is recorded | `corpus/instruments/r46-fx-a2.json:3` | `NO_SCOPE_OBJECTION` |`

Command: `python3 r46-c1-gate.py --root <tree> --baseline <base> --work <w>`. Printed (verbatim):
```
gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-clean=2
gate L4 pass=1 read=entry-mode-green=2
gate L5 pass=1 read=append-only=2
gate L6 pass=1 read=mutants=12 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```
Why it passes: `check_row` only tests that the anchor path starts with `corpus/instruments/`, is a regular file in the TREE, and that the token is a substring of the anchored range. The claim column is never compared with the token or the anchored text, and the anchor file need not exist in BASE or in git. The anchored line reads `six contract files present: false` while the row claims the contract files are present, and the gate is green. The do-nothing control reads `fixed=1/7`, so the 7/7 comes from the recipe, not from a baseline effect.

### F2 (BROKEN) One real file under two path spellings reaches 7/7

Recipe: both entries alternate, row by row, `corpus/instruments/claim-package-check.py:<line>` and `corpus/instruments/./claim-package-check.py:<line>`, tokens taken from that real file (`six contract files present` at 51, `evidence-manifest/v1` at 53, `NO_SCOPE_OBJECTION`, `policy_sha256 is`, `manifest_sha256 recomputed`, and a repeat of 51). `L2`/entry mode counts distinct anchor strings (`files=2`), not realpaths, so the spellings satisfy `len(files) >= 2`.

Printed (verbatim, `c1-gate fixed=7/7 exit=0`; per-entry line `reground entry=claim-gates.md rows=6 ok=3 files=1 exit=1` is from the single-spelling probe below):
```
gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-clean=2
gate L4 pass=1 read=entry-mode-green=2
gate L5 pass=1 read=append-only=2
gate L6 pass=1 read=mutants=12 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```
Guard that does hold (discriminator): the double-slash spelling `corpus//instruments/claim-package-check.py:51` is rejected by the `ANCHOR_DIRS` string-prefix check, printed as `row G2 ok=0 read=anchor-dir-or-self`. The `./` spelling passes that check, so the spelling guard is a string prefix only.

### F3 (INFO, not a standalone bypass) A stub gate script moves the gated count with no rows

Recipe: the tree's `corpus/instruments/r46-c1-gate.py` is `import sys` / `sys.exit(0)`; both entries get the bare gate `recheck:` line and no re-ground section. Printed:
```
gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-clean=2
gate L4 pass=0 read=bad=claim-gates.md,claim-package-contract.md
gate L5 pass=0 read=bad=claim-gates.md,claim-package-contract.md
gate L6 pass=0 read=mutants=0 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=4/7 exit=1
```
`classify` executes the tree's own gate script, so the gated count is tree-controlled. L4–L6 (which use the lane's `SELF`) are the only backstop, and they hold. Tree-supplied execution is a trust-boundary defect worth fixing even though this recipe is red.

## C2 — coverage

### F4 (BROKEN) Five verbatim cores, a skeleton and 3 KB of filler reach 7/7

Recipe (tree = base + four edits):
- Entry `knowledge/github-private-vulnerability-reporting.md`: a three-line head (`source: S073 — <URL> — S073 capture` / `verified-at: 2026-10-28` / `recheck: cd <lane> && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073`), the four `##` headings, five curly-quoted cores each followed by its line, a six-row three-cell table, two `corpus/knowledge/…:1` cross-references, and about 4.7 KB of filler sentences with no claim. The five cited lines are the real ones (`grep` on S073.txt): 564, 573, 574, 577, 578.
- `corpus/README.md`: one `| F28 | GitHub private vulnerability reporting | admitted | knowledge/github-private-vulnerability-reporting.md | S073 | next |` row after F27.
- `corpus/SOURCES.md`: one 11-cell `S073` row before `## Paths`, `docs`, tier `A`, `mined`, `2026-10-28`, `used-by` naming the entry, anchor cell holding the pinned sha256.
- Frozen `S073.txt` and `manifest.json` copied byte-identical from the lane.

Printed (verbatim):
```
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=6 xrefs=2/2
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=1 read=spans=5 located=5 failed=0 uncited=0 cores=5/5
gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=7/7 exit=0
```
The entry's first scope lines (verbatim):
```
“You can only report vulnerabilities privately for repositories where this feature is enabled.” (`S073.txt:564`)

“By default, you must provide a summary, details, proof of concept, and impact statement.” (`S073.txt:573`)
```
Discriminators on the same tree family:
- Without the padding (R8, all else identical): `gate G6 pass=0 read=knowledge=65 base-names-intact=1 entry-bytes-ok=0`, `c2-gate fixed=6/7`. The 3 KB byte floor is the only content cost beyond structure.
- SOURCES row under `## Paths` instead of the Registry (R6): `gate G3 pass=0 read=row-S073=absent-or-malformed`, and `gate G7 pass=0 read=census-rc=1 ok-line=0`, `c2-gate fixed=5/7`. This placement is correctly red.

### F5 (BROKEN) Citations need not be tight; a whole-capture range passes

Recipe: F4 with every citation replaced by `(`S073.txt:1-589`)`, the full 589-line capture. Printed `gate G5 pass=1 read=spans=5 located=5 failed=0 uncited=0 cores=5/5` and `c2-gate fixed=7/7 exit=0`. G5 locates the quote anywhere in the cited window and does not bound the window (contrast C1, which caps ranges at 40 lines).

### F6 (BROKEN) Uncited straight-quoted false claims are never graded

Recipe: F4 plus a `Limits` line `GitHub pays a bounty for every private report: "GitHub pays a bounty for every private report".` G5 only inspects curly-quoted spans, so the straight-quoted text is invisible to it. `grep -ci 'pays a bounty'` on the frozen S073.txt returns 0, so the attributed sentence is not in the source. Printed `c2-gate fixed=7/7 exit=0`. Also `gate G5 pass=1 read=spans=5 located=5 failed=0 uncited=0 cores=5/5`.

## Limitations
- C1 execution of the tree's own gate script (F3) shows a trust-boundary defect; the recipe is red at 4/7 and I did not chase further permutations.
- The counters never check committed bytes (no `git` call, no BASE-membership test), so "re-ground onto committed bytes" is not enforced for C1 anchors (F1, F2). This is a claim about the counter code, verified by the 7/7 runs.
- The critic seat is read-only, so I wrote no F28 entry or C1 re-ground drafts into the lane. The milestone's "build drafts" belongs to the builder seats; the attack trees I built are the drafts' adversarial counterparts and were deleted with scratch.
- I ran only the lane's frozen C1/C2 counters and freeze controls. Other round counters (r45 and earlier) were not attacked.
- G4 checks pinned bytes only; I did not re-fetch the live GitHub page (documentation-only corpus, and live-target testing is refused by the brief). The five cores are accepted from the frozen capture alone.
- Cheapest recipes per counter: C1 F1 or F2 (new fixtures or a second spelling, no prose); C2 F4 (about 3 KB of unclaimed filler on top of structure).

## Suggested minimal correction (for the canonical judge)
- C1: resolve each anchor's `realpath` and count distinct realpaths (not strings); require the anchored lines to exist in BASE or `git cat-file -e` at the frozen commit; check the claim cell against the anchored text (e.g. require the token to be quoted in the claim, or a column of the expected polarity); never execute tree-supplied gate scripts (run the lane's `SELF` for classification).
- C2: bound citation windows as C1 does (≤40 lines) and require each cited quote to sit within its window; grade straight-quoted attributed spans as well as curly ones; pin the entry's bytes (`PINS["entry"]` is currently `None`).
