VERDICT: BROKEN

# R45RevLimbR2 — C1 limb attack on `limb_r2` (QUALITY.md criteria R47/R48/R49)

Attacked: `corpus/instruments/r45-routed-defects.py` `def limb_r2` (lines 150-179; sha256 `82004c700decbc3453baa57919ccff71cbfe322a8d2a71b558d75951c24f04ee`, copied to scratch and run from the copy). Predicate sentence attacked: the module docstring R2 entry and claims.json C1 `after` ("R2 QUALITY.md criteria R47/R48/R49 grounded in corpus/lessons/round-44.md"). Defect stood for: spot-check round-44 §6 item 2, "QUALITY.md criteria from mistakes" (M44-3/M44-8, M44-4/M44-7/M44-10, the capture-method spot-check).

Base: `/fast/scratch/hyaku/kasegi-r45/L1/pure` (copied) plus `corpus/source-snapshots/round-45`. The lane's working `corpus/QUALITY.md` is byte-identical to the pure base (`cmp` exit 0): no round-45 criteria exist in the lane yet.

## What limb_r2 actually checks (read from source)
- L153-155: `QUALITY.md` must start with the base bytes and differ from it (append-only).
- L156: exactly one line matching `^## Round-45 additions` in the appended tail.
- L159-171: for R47/R48/R49, exactly one tail line matching `^\|\s*R4x\s*\|`; `strip("|").split("|")` yields 3 cells; cell 3 contains the substring `corpus/lessons/round-44.md`; cell 2 matches each needle case-insensitively (R47: `do-nothing`, `before data`; R48: `presence-only`; R49: `capture method`, `reject`).
- L172-177: every `` enforced-by: `...` `` path in cell 2 must satisfy `os.path.exists` under the tree (directories pass).
- Nothing reads whether the criterion is implemented, whether the enforcing path enforces anything, or whether the ground cell resolves to a real lesson entry or M44 id.

## Findings

### F1 (BROKEN) — fabricated three-row append reads limb R2 fixed=1
Command (scratch tree `v4-min` = base + 3 appended lines, 247 bytes):
```
python3 tool/r45-routed-defects.py --root "$S/v4-min" --baseline "$S/base" | grep -E "limb R2|total"
limb R2 fixed=1 read=criteria=3
routed-defects total=5 fixed=1 unresolved=4 exit=1
```
Appended bytes (`diff base/corpus/QUALITY.md v4-min/corpus/QUALITY.md`):
```
372a373,377
> 
> ## Round-45 additions
> |R47|do-nothing before data enforced-by: `corpus`|corpus/lessons/round-44.md|
> |R48|presence-only enforced-by: `corpus`|corpus/lessons/round-44.md|
> |R49|capture method reject enforced-by: `corpus`|corpus/lessons/round-44.md|
```
Recipe: append a `## Round-45 additions` heading and three rows whose criterion cell is the class words plus ``enforced-by: `corpus` `` (a directory that exists), and whose ground cell is `corpus/lessons/round-44.md`. No criterion text, no enforcing script, no check is written. The limb prints `fixed=1`. Same result with the enforced-by target `corpus/QUALITY.md` (itself prose; `v2-fab`, 441 appended bytes, `limb R2 fixed=1 read=criteria=3`) and with an unrelated README (`v7-real`: rows with real-sounding criterion prose and `enforced-by: corpus/instruments/README.md`, `limb R2 fixed=1 read=criteria=3`).

### F2 (BROKEN, minor) — grounding is a substring test
`v3-unrelated` row R47 has ground cell `not corpus/lessons/round-44.md, see it` and R48 has `corpus/lessons/round-44.md (nonexistent-anchor)`; the limb prints `limb R2 fixed=1 read=criteria=3` for that tree. Any text containing the string passes; no M44 id or anchor is resolved.

### F3 (controls discriminate only the gross cases — INFO)
Controls run on the same tree:
```
v1-marker  (heading only, no rows):  limb R2 fixed=0 read=R47-rows=0
base       (do-nothing):             limb R2 fixed=0 read=quality-not-append-only-or-unchanged
v5-ungrounded (R47 ground round-22): limb R2 fixed=0 read=R47-ungrounded
v6-missing (enforced-by no-such-file.py): limb R2 fixed=0 read=R47-enforced-by-missing-corpus/no-such-file.py
```
So the limb rejects missing rows, missing paths and ungrounded rows, and accepts any criterion whose words and existing paths match. The frozen C1 controls in `.ufo/waves/round-45/controls/freeze-controls.txt` are only `do-nothing-base` and `c1-marker-only` (plus C2 controls); no fabricated-criterion control exists for R2, so the frozen control set cannot falsify F1. (Did not inspect the `c1-marker-only` tree contents — I only read its printed RED line.)

### F4 (note) — the limb is itself presence-only
The defect class R2 is meant to add (M44-10: "presence-only predicates accept denials, stubs and rewrites") is the exact class `limb_r2` is. The enforced-by existence check is satisfied by a directory and by the QUALITY.md file that contains the criterion.

## Constructions tried (≥5, distinct)
1. Do-nothing base (A) — fixed=0.
2. Heading-only marker (v1-marker) — fixed=0, `R47-rows=0`.
3. Three class-word rows, enforced-by QUALITY.md itself (v2-fab) — fixed=1.
4. Three rows, enforced-by an unrelated README, substring-ground tricks (v3-unrelated) — fixed=1.
5. Minimal three rows, no id-space prose, enforced-by directory `corpus` (v4-min, 247 bytes) — fixed=1.
6. Ungrounded R47 (round-22 ground) (v5-ungrounded) — fixed=0.
7. Missing enforced-by path (v6-missing) — fixed=0.
8. Honest-looking criteria prose, enforced-by existing README (v7-real) — fixed=1.

## Limitations
- Only limb R2 was attacked, as assigned. The full C1 `fixed=5` claim needs R1, R3, R4 and R5 too; I did not run those, so no statement about C1 as a whole is made here. A full-counter run on v4-min printed only R2 as fixed (`total=5 fixed=1`), which means the other four limbs are not satisfied by this tree.
- The attack uses a copy of the lane's counter at the sha above. I did not run the counter from the lane tree.
- I did not inspect the real round-45 criteria the lane may add later; the lane QUALITY.md is still the base bytes at the time of this check.
- Scratch was removed on exit.

## Suggested direction for L1 (not applied; no lane edit by this seat)
Per the claims kill rule, bug fixes that keep the predicate are logged as errata. Candidate tightenings for L1 to decide: require the enforced-by target to be a file other than `corpus/QUALITY.md` that mentions the class id or an M44 id; require the ground cell to name an M44 id present in `corpus/lessons/round-44.md`; add a fabricated-row control (v4-min shape) to the frozen controls that must grade `limb R2 fixed=0`. Any change to the predicate sentence after a seat has scored would fall under the kill rule.
