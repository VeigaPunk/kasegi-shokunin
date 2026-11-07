# CriticClaimsC1 — round 96, C1 attack (attempt 1)

Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
Landing under attack: `3c0581e2616df7a10af494a785b479d5e5293749`
Base: `d8a2bb0a2bdc2f6337ea2f849a1a557297067ad6`; freeze: `804e7bc344df0808c880815dde077c28be5db18a`
Method: fresh `git clone --shared` of the lane, detached at the landing; every limb re-derived by me (no value quoted from the claim). Receipts: `.ufo/waves/round-96/w1/CriticClaimsC1-receipts/`.

## Verdict

**C1 STANDS on P1-P4 at the landing `3c0581e`**, with the limb values I measured:

- P1: `KNOWLEDGE-METER-RESULT pass rc=0`; M0 `base=1030/2027`, M1 `after=1032/2028`, M3 `same_files=True bad_lines=0 old_not_once=0 dup_rows=0`, M4 `bad=none`, M5 `out_of_range=none`, M9 `rows=5 unbound=none`, M10 `labelled=5 want=5 mapped=5 kinds=part=4,range=1 unknown=none`, M6 `7d9bb49f366a594df3cd13e5651a6db4aabef1ab4b5a7081d89fd5f8c68b1d0f`, `after_rev=3c0581e…`.
- P2: `C1-CONTROLS-RESULT pass controls=12`, `ATTRIBUTION pass fixtures=11` at the landing; every declared FAIL set equals the observed set.
- P3: the landing commit's own diff (`804e7bc..3c0581e`) is exactly `corpus/knowledge/triage-thresholds.md` and `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md`.
- P4: do-nothing `rc=1` limbs `M1,M3` (M1 `after=1030/2027`); the round-95 counter with only `LABELS_PATH` repointed `rc=1` limbs `M4,M5`.

Nothing in the qualifiers below re-scores the frozen predicate; they are routed defects for the counter/control set, not verdict changes.

## Evidence (re-derived)

1. **P1 exact.** Receipt `01-meter-landing.txt`: the frozen command at the landing prints the predicate's line and every limb pass, rc=0.
2. **M0/M1 independently.** My own tokenizer/classifier (`census.py`, no `resolve.py` import) over `corpus/knowledge/*.md` at both revisions: base `1030/2027`, after `1032/2028` (receipts `03`, `04`). Token-set diff: `−1` GONE (`S041.txt:1680-1681`), `+2` INTERNAL (`SKILL.md:182-185`, `corpus/source-snapshots/round-30/S041.txt:1680-1681`); `2027−1+2=2028`, `997−1=996` GONE ⇒ `1032` non-GONE. The counter's own `--measure-rev` agrees (`50.81%` → `50.89%`, receipt `07`).
3. **M3 independently.** Applying the frozen map to the base blobs and comparing to the after blobs byte-for-byte over all 104 `corpus/knowledge` files: `same_files=True`, `bad=0` (receipt `05`).
4. **M9/M10 independently.** From the frozen labels file: 5 rows, 5 bound, `want=mapped=5`, `kinds part=4,range=1`, no unapplied/unlabelled (receipt `05`).
5. **P3.** `git diff --name-only 804e7bc..3c0581e` lists exactly the two knowledge files; `git show --stat 3c0581e` is 2 files, 4 insertions, 4 deletions.
6. **P2.** Harness re-run at the landing (receipt `02`): 12 controls, all as declared; the do-nothing control cannot reach the target (`after=1030/2027`).
7. **P4.** Do-nothing `rc=1 M1,M3`; r95 counter `rc=1 M4,M5` (receipt `02`).
8. **Content truth.** `SKILL.md:182-185` carries the five-term expression and the correction `text omitted \`is_live(1)\`` completing on 185; `SKILL.md:255-257` carries the curated-boolean correction. `S041` 1832 `d) Information that would be useful when submitting a`, 1833 `possible vulnerability report`, 1834 `e) Out-of-scope services`, 1835 `f) How submitted reports are tracked`. The capture `corpus/source-snapshots/round-30/S041.txt` is tracked and 1680-1681 is in range of 2354 lines. Each of the five keys occurs exactly once on its base line.
9. **Provenance.** The frozen `labels.tsv` is byte-identical to the round-95 w1 receipt `ReviewC1Sites-receipts/round96-labels.tsv`; the five rows are the round-95 `ReviewC1Sites` follow-ups — `ReviewC1Sites.md:146-150` lists exactly these five edits (F2 at triage :88/:90, F1 at iso :13, F3 at iso :36), and `:75` names them "round-96 label rows 1-2". No bare `S041.txt` token remains in `corpus/knowledge` at the landing.

## Counterexamples (routed qualifiers, not verdict changes)

1. **M5 is not applied to prose-pointer rows.** `A-out-of-range` (receipt `06`): a `part` row keyed `f) how submitted reports are tracked (L1835)` → `(L99999)` passes M4, M5, M9, M10 and the meter (`rc=0`). The M4 prose branch `continue`s before every M5 range check, so the docstring's "every written value's anchor lies inside the entry" does not hold for prose pointers. S041 is 2354 lines; L99999 is out of range.
2. **No occurrence isolation.** `B-duplicate-pointer` (`rc=0`): a row keyed `(L1835)` → `(L1834)` on iso:36 edits the **f)** pointer as well (M3's `replace` is global; the frozen e) row consumes the e) occurrence first), while the label's own evidence says the f) pointer is correct. The row is accepted.
3. **Pointer insertion passes.** `E-pointer-insertion` (`rc=0`): a key ending in a space (`f) how submitted reports are tracked `) plus `(L99999)` satisfies `PTR.sub(old)==PTR.sub(new)`, so the branch accepts an **inserted** pointer, not only a number change. The statement's "only its `(L...)` numbers change" is therefore not enforced.
4. **Citation smuggling is closed; occurrence bleed is not.** `C-nonbackticked-citation` (`rc=1 M4,M5`) fails the PTR equality; `D-backticked-citation` (`rc=1 M1,M4,M5`) fails the backtick test (M1 also moves because the backticked token changes the rate). So the non-backticked-citation form is blocked — the PTR equality, not the backtick test, is the guard. But the other attack named in the seat spec, editing text outside its own pointer, is open in the duplicate-occurrence form (B): the branch binds the key *text*, not an occurrence, and M3 replaces globally.
5. **Control-set coverage gap.** The fixture named `row-old-absent-only` does **not** exercise `old_not_once`: its key `(L1819)` is on base line 36 (the a) pointer), and the observed detail is `bad_lines=1 old_not_once=0`. A true `old_not_once` fixture (key `(L9999)` absent, new `(L9998)`) gives `M3 old_not_once=1` with M4/M5/M9/M10 green (receipt `08b`). Consequently `old_not_once`, `dup_rows`, `same_files`, the four M4 prose rejection rules and M5's own range checks have no isolating fixture — the round-95 defect pattern (a rule with no negative fixture) survives at sub-rule granularity, even though every shipped fixture's limb-level FAIL set equals its declaration.
6. **Attribution accounting.** `fixtures=11` = the candidate control (`declared=[]`) + 10 declared negatives. The claim's "eleven attribution fixtures" counts the positive control as a fixture.
7. **Receipt provenance.** The committed `controls/c1-controls-r96.txt` is a pre-freeze run (`candidate=f60c11a`, `freeze=179deaaa`); P2's landing claim rests on the re-run, which reproduces every limb value.

## Impacted axes

- `depth:verifiability`: the landing's five edits are verified byte-exactly, in range, on unique keys, with traceable provenance; M0/M1/M3/M9/M10 reproduce independently. The counter's new M4 prose branch is weaker than its docstring (no range check, no occurrence isolation, insertion allowed), and the control set does not isolate the M3 sub-rules or the M4 prose rejection rules. No re-score of C1's frozen predicate or its score.

## Smallest safe correction

- **Claim:** none at the landing; P1-P4 hold. If the control-set sentence is kept, say "ten negative fixtures plus the candidate control" instead of "eleven attribution fixtures".
- **Counter (next round, not this landing):** in the prose branch, (a) range-check the new pointer against the cited capture (M5), (b) require the key to occur exactly once on its base line, (c) require the new text to carry the same number of `(L...)` groups as the old (no insertion).
- **Control set:** add a true `old_not_once` fixture, a `dup_rows` fixture, a `same_files` fixture and one fixture per prose rejection rule; rename `row-old-absent-only` to `row-not-applied`.

## Receipts

All under `.ufo/waves/round-96/w1/CriticClaimsC1-receipts/`:

| file | command | observed |
|---|---|---|
| `00-commands.txt` | full command log | — |
| `01-meter-landing.txt` | `knowledge-meter.py --lane <clone> --base-rev d8a2bb0 --after-rev 3c0581e --map … --labels-rev 804e7bc --base-target 1030/2027 --target 1032/2028 --map-sha256 7d9bb49f… --work $S/work` | rc=0; M0 1030/2027, M1 1032/2028, M3 0/0/0, M4 none, M5 none, M9 5/none, M10 5/5/5 part=4,range=1, M6 7d9bb49f… |
| `02-controls-landing.txt` | `c1-controls-r96.py <clone> 804e7bc .ufo/waves/round-95/c1/knowledge-meter.py $S/work $S/out` | rc=0; 12 controls PASS; ATTRIBUTION pass fixtures=11 |
| `03-census-base.txt` | `census.py <clone> d8a2bb0 $S/work` | `rate=1030/2027 mirror_absent=True` |
| `04-census-after.txt` | `census.py <clone> 3c0581e $S/work` | `rate=1032/2028 mirror_absent=True` |
| `05-indep-m3-m9-m10.txt` | `indep-m3.py <clone> d8a2bb0 3c0581e 804e7bc repair-map.tsv labels-freeze.tsv` | rc=0; M3 n=104/104 bad=0; M9 5/0; M10 5/5/5 part=4,range=1 |
| `06-prose-attacks.txt` | `attack-prose.py <clone> d8a2bb0 knowledge-meter.py $S/attack` | A rc=0, B rc=0, C rc=1 M4,M5, D rc=1 M1,M4,M5, E rc=0 |
| `07-measure-crosscheck.txt` | `knowledge-meter.py --measure-rev <base|after>` | 1030/2027 and 1032/2028 |
| `08-old-not-once-fixture.txt` | first fixture, key `ZZZ-not-on-line` | rc=1; M3 old_not_once=1, M4 FAIL (non-pointer text change rejected), M5 implied |
| `08b-old-not-once-fixture.txt` | key `(L9999)` absent, new `(L9998)` | rc=1; M3 old_not_once=1, M4/M5/M9/M10 pass |

Other checks (in `00-commands.txt`): `git diff --name-only 804e7bc..3c0581e` → exactly the two knowledge files; `git show 3c0581e:<artifact> | sha256sum` → the four pinned hashes; `diff` labels vs the round-95 receipt → IDENTICAL; occurrence counts on the base lines → 1 each; `git grep '\`S041\.txt'` at the landing → empty.

Tooling: none installed or upgraded (no pacman, no uv, no npx).
