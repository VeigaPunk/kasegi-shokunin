# CriticClaimsC1 — round 94, C1 (tranche 9, 19 repoints, meter 1008/1999 -> 1009/2000)

Seat: `CriticClaimsC1` (leaf; no dispatch). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `dff5a0a01e8aafe6be81f4ee61567745c3c4c485`, freeze `96b5033f4dfa8d6605c13e0c9aad458be3cd7df3`,
C1 landing `d51220aeb4a538b7b211bb2629e83210669cd56d`, C2 landing / lane head `996460861d4130ddb2da6b7554e905d3e47504a3`.
All work in scratch `/fast/scratch/hyaku/kasegi-r94/CriticClaimsC1`, removed at exit; every fixture commit was made in a
`git clone --shared` of the lane under scratch after `git rev-parse --show-toplevel` equalled the clone. The lane's git state
was only read (`show`, `ls-tree`, `diff-tree`, `cat-file`, `merge-base`, `archive`).

## Verdict

**DOES-NOT-STAND** on the frozen predicate, on P4's reproduction limb; the frozen kill rule reads
`Any limb FAIL at the landing, P3 naming another path set, or P4 not reproducing: C1 NOT VERIFIED`.

- **P1 STANDS.** The frozen command run from committed bytes in a fresh `git clone --shared` of the landing prints
  `KNOWLEDGE-METER-RESULT pass rc=0` with every named row exactly as frozen (M0 1008/1999, M1 1009/2000, M3
  same_files=True bad_lines=0 old_not_once=0 dup_rows=0, M4 bad=none, M5 out_of_range=none, M9 rows=19 unbound=none,
  M10 labelled=29 want=19 mapped=19 kinds=excluded=10,range=19 unknown=none unapplied=none unlabelled=none,
  M6 11de45a7…8847, after_rev=d51220ae…6d).
- **P2 STANDS.** Counter/map/labels sha256 equal the frozen pins at freeze, landing and head
  (`03947734…1f67`, `11de45a7…8847`, `41bc438b…556b`).
- **P3 STANDS.** `git diff-tree --no-commit-id --name-only -r d51220a` names exactly
  `corpus/knowledge/considerthese-proposals-ledger.md` and `corpus/knowledge/triage-thresholds.md`
  (18 insertions / 18 deletions); `SKILL.md` is unchanged freeze -> landing.
- **P4 DOES NOT REPRODUCE at the landing.** The receipt is a freeze blob and does print
  `C1-CONTROLS-RESULT pass controls=12`, but re-executing the committed control driver against the landing gives
  `C1-CONTROLS-RESULT fail controls=12` with
  `CONTROL m5-cell-repair-before-r93 rc=1 want=0 FAIL` (r93 output `base=1008/1999 after=1010/2001 … M1 FAIL after=1010/2001`,
  `M3 FAIL … bad_lines=18`). The cause is the driver's r93-before fixture: it clones the *mutable live lane* (`LANE`) instead of
  a pinned rev, so after the tranche lands the fixture's own base tree contains the 18 applied lines. Pinning that one clone to the
  frozen base rev restores the whole suite: `C1-CONTROLS-RESULT pass controls=12`, `m5-cell-repair-before-r93 rc=0 want=0 PASS`
  (my probe; `diff` of the copy against the frozen driver shows one line, `ONE-LINE-DIFF-ONLY`). Independently, the receipt's
  `candidate=e7adac6a07525eb5773725da15d47f6699492785` is not an object in the lane **or** the fleet repo
  (`fatal: git cat-file: could not get object info`), so the exact recorded run cannot be re-derived from committed bytes.

If P4 is read as a file-content assertion only (the receipt prints 12/12, freeze blob intact), then P4's literal content is
satisfied and this finding is a routed control-durability/provenance defect, not a verdict change. The frozen kill rule's plain
reading — the controls must reproduce — is the reading I score: P4 fails, so C1 is NOT VERIFIED as claimed. The claim's substance
(the 19 repoints, the map/labels/EXCLUDED set, the landing meter run) is correct and independently re-derived below; the defect is a
one-line control pin, not an edit, map, label, or counter-limb defect.

## Counterexample (smallest, exact)

The committed driver, one argument changed (candidate clone = landing), live lane at the C2 landing:

```
C1-CONTROLS candidate=d51220ae…6d base=dff5a0a…85
CONTROL m5-cell-repair-before-r93 rc=1 want=0 FAIL
  KNOWLEDGE-METER base=1008/1999 after=1010/2001 base_target=1008/1999 target=1009/2000 sites=1 labels=1 …
  LIMB M1 FAIL after=1010/2001
  LIMB M3 FAIL same_files=True bad_lines=18 old_not_once=0 dup_rows=0
  LIMB M5 pass out_of_range=none
```

With `LANE` pinned to a clone of `dff5a0a` (one line; nothing else changed):

```
CONTROL m5-cell-repair-before-r93 rc=0 want=0 PASS
  KNOWLEDGE-METER base=1008/1999 after=1009/2000 … sites=1 labels=1
  LIMB M1 pass after=1009/2000
  LIMB M3 pass same_files=True bad_lines=0 old_not_once=0 dup_rows=0
  LIMB M5 pass out_of_range=none
C1-CONTROLS-RESULT pass controls=12
```

The reception itself ("r93 exits 0 on the backticked out-of-range cell lane token; the successor fails M5") is real on a
base-pinned fixture; the shipped harness simply does not pin it. The first red-before reception does reproduce at the landing:
`CONTROL m3-union-applied-before-r93 rc=1 want=1 PASS traceback=True`, with `Traceback (most recent call last):` in the r93 output,
while the successor passes the same union fixture (`CONTROL m3-union-applied rc=0 want=0 PASS`).

## Limb-by-limb re-derivation (P1)

Command (map extracted from the freeze blob; working-tree map sha equals the pin):

```
python3 -B .ufo/waves/round-94/c1/knowledge-meter.py --lane <fresh --shared clone> \
  --base-rev dff5a0a01e8aafe6be81f4ee61567745c3c4c485 --after-rev d51220aeb4a538b7b211bb2629e83210669cd56d \
  --map repair-map.tsv@96b5033 --labels-rev 96b5033f4dfa8d6605c13e0c9aad458be3cd7df3 \
  --base-target 1008/1999 --target 1009/2000 --map-sha256 11de45a74337b945b5179645e18e0f710a2f9ec54935450806a0e4bda7a78847 --work <scratch>
```

Observed rc=0:

```
LIMB M0 pass base=1008/1999
LIMB M1 pass after=1009/2000
LIMB M3 pass same_files=True bad_lines=0 old_not_once=0 dup_rows=0
LIMB M4 pass bad=none
LIMB M5 pass out_of_range=none
LIMB M9 pass rows=19 unbound=none
LIMB M10 pass labelled=29 want=19 mapped=19 kinds=excluded=10,range=19 unknown=none unapplied=none unlabelled=none
LIMB M6 pass sha256=11de45a74337b945b5179645e18e0f710a2f9ec54935450806a0e4bda7a78847
KNOWLEDGE-METER-RESULT pass rc=0
```

Independent cross-check (no counter import; `git show` bytes only): map rows=19, distinct (file,line) sites=18, labels=29,
EXCLUDED=10; mapped pairs = the 19 label-named edits; `mapped ∩ EXCLUDED` empty; `mapped - labels` empty; every map `new` equals
the label-named target; every knowledge file after = base with each mapped `old` replaced; `bad_lines=0`, 20 old occurrences
replaced (19 rows; the ledger row's key occurs twice and both are repointed); changed knowledge files are exactly the two named;
ledger line 156: base 2x `SKILL.md:1163`, after 2x `SKILL.md:1164`, 0x `SKILL.md:1163`; `SKILL.md` has 1252 lines and every
written lane anchor is in range; the 10 unmapped label pairs equal the frozen EXCLUDED set exactly, each with a reason.

## Attacks run (all in scratch clones of the landing unless noted)

| # | Forgery | Observed | Consequence |
|---|---|---|---|
| F1 | unlabelled in-scope edit (`corpus/knowledge/ev-model.md` line 1 + text, no map row) | rc=1; `M3 FAIL bad_lines=1`; M1 still pass 1009/2000 | detected |
| F2a | out-of-scope inert edit (`corpus/instruments/resolve.py` appended comment) | rc=0; every limb pass | counter is blind to out-of-scope edits; P3 is the guard |
| F3 | map row's `new` differs from the label; after text follows the map | rc=1; `M9 FAIL rows=19 unbound=triage-thresholds.md:143`; M1 pass at the fixture's measured 1010/2001; M3/M4/M5/M10 pass | M9 isolates the mismatch |
| F4 | label anchor out of range (`SKILL.md:999999`, label and text both moved) | rc=1; `M5 FAIL out_of_range=triage-thresholds.md:143`; M9 pass (label and text agree) | M5 isolates range |
| F5 | cell-repair replacement with backticked `SKILL.md:9999` beside a valid corpus value | rc=1; `M5 FAIL out_of_range=triage-thresholds.md:440`; M1 pass 1010/2001; M3/M4/M9/M10 pass; map sha `df536b43…e013` equals the shipped control's fixture sha | successor rejects it |
| F6 | duplicate map row for one (site,key) | rc=1; `M3 FAIL … dup_rows=1`; M9/M10 pass | duplicate row caught |
| F7 | EXCLUDED pair mapped coherently (label exists; text applied) | rc=1; `M9 FAIL unbound=triage-thresholds.md:88`; `M10 FAIL … unlabelled=triage-thresholds.md:88/SKILL.md:113-114` | EXCLUDED is enforced |
| F8 | labelled file outside `corpus/knowledge` (`corpus/QUALITY.md:537`, label `SKILL.md:1224`->`1225`) | successor: rc=0, `M3 pass same_files=True`, sites=20 labels=30; r93 counter: rc=1 with `Traceback (most recent call last):` | M3 union limb works; r93 crash reception reproduces |
| F9 | unpinned classifier tamper (landing + `resolve.py` forced `SKILL.md:251-253` GONE and a GONE token INTERNAL) | rc=0, all limbs pass; measured classes in the after tree: `SKILL.md:251-253=GONE`, `../MISSION.md:49-56=INTERNAL` | counter trusts the measured tree's `resolve.py`; P3 closes it at this landing |
| F10 | unbackticked `SKILL.md:9999` inside a cell replacement (beside a valid corpus value) | rc=0, all limbs pass at the measured 1009/2000 | binding is backtick-scoped (see Q7) |

All five variants named in the seat brief were covered (F1, F2a, F3, F4, F5), plus F6-F10.

## Qualifiers (separate from the verdict)

1. **The meter delta is a unique-token accounting artifact, not a repaired citation.** Independent set diff of the two meter
   readings: 16 unique tokens added, 15 removed, **0 class flips**, and GONE is **991 before and 991 after**; the added and removed
   tokens are all `INTERNAL` lane anchors. The numerator +1 is the extra distinct, already-resolving anchor; no GONE citation was
   repaired. `M1` therefore does not witness anchor correctness; that is carried by `M3` (exact text), `M5` (in range) and `M9`
   (label binding). The claim's numbers are true; the phrase "measured knowledge meter" should not be read as a resolvability gain.
2. **The counter does not pin its classifier.** `M6` pins the map; `P2` pins counter/map/labels; nothing pins
   `corpus/instruments/resolve.py`. F9 shows a full-pass run on an after tree whose `resolve.py` swaps which tokens resolve. At this
   landing P3 excludes `resolve.py` from the landing commit, so the run is sound; the counter alone is circular.
3. **The control driver's r93-before fixture clones the live lane, not a rev.** This is the P4 reproduction failure; it also makes the
   receipt's `candidate=e7adac6…` line unrecoverable (absent from lane and fleet). The pin is mechanical: clone `dff5a0a` (or pass
   the base rev as an argument, as the round-93 harness did) for that one fixture.
4. **"19 sites" is overloaded.** There are 19 map rows over **18 distinct (file,line) sites**: 17 `triage-thresholds.md` lines, with
   line 397 carrying two rows, plus one ledger line with two occurrences of its key. The printed `sites=19` is `len(rows)`; the
   statement's own "17 sites … 1 site" arithmetic is the accurate one. No limb fails.
5. **"Ten … prose reword" is imprecise for two of ten.** `triage-thresholds.md:356/SKILL.md:522` and `:396/SKILL.md:245-247` are
   `qualify` rows whose EXCLUDED reasons say the target file does not carry the content; the other eight are cell rewords. All ten
   are genuinely unmapped with a frozen reason, and M10 is satisfied.
6. **The binding is backtick-scoped.** F10 passes with a bare `SKILL.md:9999` in a cell replacement. This is consistent with the
   instrument's citation definition (`resolve.py` collects only backticked spans), but the docstring/statement phrase "lane-root
   tokens embedded anywhere in a written value" should say "backticked lane-root values"; a bare anchor is prose to both instruments.
7. **M3 replaces every occurrence of `old` on a site line.** The ledger row needs exactly that (2 -> 2). A future row whose `old`
   occurs twice but should change once cannot be expressed; not exercised by this map, and the map's `old_not_once=0`/`bad_lines=0`
   shows the current set is consistent.

## Impacted axes

- `depth:verifiability` (lowest non-retired axis, score 4): P4's evidence durability and the meter's semantics. P1/P2/P3 and the 19
  repoints' byte correctness are verified; the score is not claimed to move and this report does not move it.
- `coverage` (C2, score 8): not implicated by C1; no C2 artifacts were edited or judged here.

## Smallest safe correction

1. In `.ufo/waves/round-94/controls/c1-controls-r94.py`, replace the r93-before fixture's live-lane clone with a clone of the frozen
   base rev (`git clone --shared "$LANE" "$d2"` + `git -C "$d2" checkout -q --detach dff5a0a…`), or take the base rev as an argument
   and clone it. One line; my probe shows the suite then prints `pass controls=12` and the reception `rc=0 want=0`.
2. Record a candidate commit that exists in the lane (or drop the `candidate=` column), and if the controls must be re-runnable,
   take the candidate rev as an argument — do not re-freeze this receipt post-landing; re-execute and re-freeze next round.
3. Optional hardening for the next counter: pin `corpus/instruments/resolve.py` by sha (an M11) so the meter cannot be steered by an
   instrument edit in the measured tree; P3 already excludes it at this landing.

## Receipts

All outputs are in `.ufo/waves/round-94/w1/CriticClaimsC1-receipts/`.

1. `git cat-file -t` for base/freeze/landing/C2/candidate -> four `commit`, candidate `fatal: git cat-file: could not get object info`;
   `git merge-base --is-ancestor` base->freeze, freeze->landing, landing->C2 -> `rc=0` each;
   `git diff-tree --no-commit-id --name-only -r d51220a` -> the two knowledge paths; diffstat `18 insertions(+), 18 deletions(-)`;
   `git show <rev>:<artifact> | sha256sum` at freeze/landing/head -> counter `03947734…1f67`, map `11de45a7…8847`,
   labels `41bc438b…556b`, control receipt `e34a9412…fe6d`, control driver `7a404c41…6bd4`.
   File: `provenance-p2-p3-p4.txt`.
2. Fresh `git clone --shared` of the lane + toplevel assert; counter command above -> `LIMB M0..M6/M9/M10 pass`,
   `KNOWLEDGE-METER-RESULT pass rc=0`. File: `counter-landing-clone.txt`.
3. `python3 -B c1-controls-r94.py <landing clone> .ufo/waves/round-93/c1/knowledge-meter.py <work> <out>` at head 9964608
   -> `C1-CONTROLS-RESULT fail controls=12`; `CONTROL m5-cell-repair-before-r93 rc=1 want=0 FAIL` with
   `M1 FAIL after=1010/2001`, `M3 FAIL … bad_lines=18`; all other 11 controls PASS, including
   `m3-union-applied-before-r93 rc=1 want=1 PASS traceback=True` and `m5-cell-repair-lane-root rc=1 want=1 PASS limb=True`.
   File: `controls-rerun-landing.txt`.
4. Same driver copied with `LANE` = base clone; `diff -u` vs the frozen driver is exactly the one `LANE` line and
   `diff` after masking it prints `ONE-LINE-DIFF-ONLY` (frozen driver sha `7a404c41…6bd4`) -> `C1-CONTROLS-RESULT pass controls=12`;
   `m5-cell-repair-before-r93 rc=0 want=0 PASS`, `M1 pass after=1009/2000`, `M3 pass bad_lines=0`.
   Files: `controls-pinned-lane-r94.txt`, `pinned-copy-diff.txt`.
5. Pinned-base r93-before probe (clone at dff5a0a, cell row only) -> `PINNED-AT-BASE r93 rc=0`, `M5 pass out_of_range=none`,
   map sha `48fca695…13e4`. File: `pinned-r93-base-probe.txt`.
6. Own fixtures F1-F8, `python3 -B fixtures2.py` -> per-variant rc and limb lines as in the attack table; driver rc=0.
   File: `critic-fixtures2.txt` (earlier partial run: `critic-fixtures.txt`).
7. Independent cross-check `python3 -B verify.py` -> `map_rows=19 labels=29`, `distinct_sites=18 excluded=10`,
   `mapped∩excluded=[]`, `mapped-not-labelled=[]`, `label_vs_map_mismatch=[]`, `bad_lines=0 old_occurrences_replaced=20`,
   `changed_knowledge_files=[…ledger.md, …triage-thresholds.md]`, `ledger_1163_base=2 ledger_1164_after=2 ledger_1163_after=0`,
   `SKILL_md_lines=1252 out_of_range=[]`, `unmapped_label_pairs=10 equal_to_excluded=True`, `SKILL_changed_freeze_to_landing=False`.
   File: `independent-crosscheck.txt`.
8. Meter delta `python3 -B delta.py` -> `base rate=1008/1999`, `after rate=1009/2000`, `added unique tokens=16`,
   `removed unique tokens=15`, `common tokens with a class change=0`, `base_gone=991 after_gone=991`. File: `token-delta.txt`.
9. GONE-token pick (for F9) -> 570 relative GONE-in-both candidates; F9 `python3 -B` fixture -> `F2C INSTRUMENT TAMPER rc=0`,
   all limbs pass, `tampered after cls: SKILL.md:251-253=GONE  ../MISSION.md:49-56=INTERNAL`. Files: `gone-token-pick.txt`,
   `instrument-tamper-f2c.txt`.
10. F10 unbackticked cell token -> `F5B UNBACKTICKED LANE TOKEN rc=0`, all limbs pass, `sites=20 labels=30`, map sha
    `820e1c5c…ff29`. File: `f5b-unbackticked-lane-token.txt`.

Scratch was under `/fast/scratch/hyaku/kasegi-r94/CriticClaimsC1` and is removed after this report; no lane git mutation was made.
