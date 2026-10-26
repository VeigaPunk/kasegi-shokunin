# Scribe ScribeQualityDraft — round 35

Seat: `ScribeQualityDraft` (L2 leaf, kasegi-shokunin round 35). Lane base
`3266c9937b03062d9bbc2f436e20820115ed179c`; claims freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`.
Assignment: draft the exact append-only `corpus/QUALITY.md` amendment for frozen claim **C1**'s D7 clause
(`corpus/QUALITY.md` carries appended `supersedes R22` + `supersedes R23` rows) and for the non-claim
frontier item "considerthese proposal 2 → QUALITY R26".

I did **not** touch `corpus/QUALITY.md` or any other product path: the L1 applies the text below. This
seat's only write is this receipt (plus scratch under `/fast/scratch/hyaku/kasegi-r35/ScribeQualityDraft/`,
removed at exit — §6).

---

## 1. Draft — exact text to append to `corpus/QUALITY.md`

Append after the file's final newline (line 229, `records=41`) |). The block starts with one blank
line, i.e. exactly the 21 lines / 2842 bytes between the two markers below; the enclosed bytes hash to
`sha256 e3aa99a16b725335ceac2928f61d2d65ff1cc4e105c9c150fe51f2985eaa6918`.

<!-- BEGIN QUALITY.md append (21 lines, 2842 bytes, sha256 e3aa99a16b725335ceac2928f61d2d65ff1cc4e105c9c150fe51f2985eaa6918) -->

```markdown

## Round-35 supersession — R22/R23 grounded-in corrections and the next-score gap (append-only)

R6 form: every line above keeps its number — this block is appended after line 229 (the file is
30889 bytes before it, `head -c 30889 corpus/QUALITY.md | sha256sum` →
`807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8`), and R22 (line 226) and R23
(line 227) are not edited. Both corrections are round-34 verifier defect D7
(`corpus/lessons/round-34-verifier-spotcheck.md:199-203`: "QUALITY R22 cites M34-2, but its grounding
is M34-3 (lesson open item 10; `CritMistakes` F7)"), landed as supersessions because the bar is
append-only.

R22's corrected citation reaches M34-3 from the side that matters: M34-3's own capture line reads
"`none` at freeze time — `QUALITY.md` R22 (pre-freeze satisfiability) existed but had no planned-state
limb" (`.ufo/waves/round-34/mistakes-erratum-1.md:18-20`), so R22 is the criterion that could not see
the defect; R25 cites the same row as the mistake it mints, and neither citation is a second source
for the other.

| id | criterion | grounded in |
|---|---|---|
| R26 | A round reports the distance to the next score, not only "improved, held": a read-only gap computation against the recorded next-score threshold, cited in the round lesson. Grounded in: `considerthese/2026-10-25.md` proposal 2 (2026-10-25). R22's criterion is unchanged by this row. | supersedes R22 — R22's Grounded-in column cites M34-2, but M34-2 is the SCORECARD unfilled-placeholder defect (R1 class); the correct mistake is M34-3, the freeze-satisfiability row minted at `.ufo/waves/round-34/mistakes-erratum-1.md:9-29` (round-34 lesson open item 10, `corpus/lessons/round-34.md:482-485`) — the C1 `records=40` literal was true at base and false at the declared after-state `records=41`. The new criterion's runnable form is `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/score-gap.py` (read-only; prints the `SCORECARD.md` threshold line it reads and one computed `gap:` line, exit 0), whose ledger row is `corpus/knowledge/considerthese-proposals-ledger.md` § Round-31 status flips (proposal 2 `mined round 31`). |
| R27 | A lane records an event-driven reflection cadence: burst activity and idle stretches are reviewed within the next round's lesson, citing the considerthese file and date. R23's criterion is unchanged by this row. | supersedes R23 — R23's Grounded-in column cites `considerthese/2026-10-25.md:76` proposal 6 alone; the landed grounding is the round-34 lesson's own § considerthese disposition of that proposal (`corpus/lessons/round-34.md:343-358`: proposal 6 "mined → landed" as R23, including the recorded narrowing against `wave1/ScribeQualityDraft.md`'s block), which a re-verifier re-opens in-lane rather than in a reflection file. |
```

<!-- END QUALITY.md append -->

### Why this shape

- **R26 carries both jobs.** The dispatch allowed the new distance-to-next-score criterion either as
  the supersedes-R22 row or as its own row. Two rows are what C1's after-list names
  ("appended supersedes-R22 and supersedes-R23 rows"), and the R1–R25 ids are taken (max is R25), so
  a third, independently-ided row would either renumber the supersessions or leave R26/R27 unfilled.
  The row therefore states the new criterion in the criterion cell, states in-cell that R22's rule is
  unchanged, and carries the correction in the grounded-in cell — the same cell convention as
  `| R19 | … | supersedes R13 — … |` at `corpus/QUALITY.md:127`.
- **R27 restates R23 verbatim** and corrects only the citation, because D7's complaint is that the
  grounded-in column cites the reflection file "rather than the round-34 lesson §considerthese". It
  deliberately does **not** restore the disposition limb the round-34 lesson recorded as narrowed
  (`corpus/lessons/round-34.md:352-358`); that is a separate bar decision for the L1 (finding F5).
- **No volatile figure is written into the bar.** R19 makes a quoted specimen figure a closure
  obligation, so the row cites the command and the ledger, not `gap: 24 of 46 …`. The live figure is
  in finding F7 for the lesson to cite.

## 2. Apply + verify (commands for the L1)

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
wc -lc corpus/QUALITY.md                      # before: 229 30889
sha256sum corpus/QUALITY.md                   # before: 807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8
# append the 21-line block from §1, then:
wc -lc corpus/QUALITY.md                      # after:  250 33731
head -c 30889 corpus/QUALITY.md | sha256sum    # after:  807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8  (byte-prefix proof)
grep -c -F -- 'supersedes R22' corpus/QUALITY.md   # 1
grep -c -F -- 'supersedes R23' corpus/QUALITY.md   # 1
bash corpus/instruments/r35-defect-closure.sh | grep -E '^D7 |^closed='   # D7 open=0
```

Expected D7 line after the append: `D7 check=supersedes-R22=1,supersedes-R23=1 open=0`.

## 3. Measurements (this seat, read-only)

`corpus/instruments/r35-defect-closure.sh` — D7 reads the two literals with
`grep -c -F -- 'supersedes R22'` / `'supersedes R23'` (`corpus/instruments/r35-defect-closure.sh:214-215`;
usage line `:49-50`), so the literals must appear in the file verbatim and case-sensitively.

| run | command | D7 payload | suite tail | exit |
|---|---|---|---|---|
| lane now (before) | `bash corpus/instruments/r35-defect-closure.sh` | `supersedes-R22=0,supersedes-R23=0 open=1` | `closed=3/7 exit=1` | 1 |
| lane copy + this block (after) | `bash corpus/instruments/r35-defect-closure.sh --root $S/root-d7` | `supersedes-R22=1,supersedes-R23=1 open=0` | `closed=1/7 exit=1` | 1 |
| copy with both literal lines filtered out (mutant) | `bash corpus/instruments/r35-defect-closure.sh --root $S/root-mut` | `supersedes-R22=0,supersedes-R23=0 open=1` | `closed=0/7 exit=1` | 1 |

`$S/root-d7` and `$S/root-mut` each carried only `corpus/QUALITY.md` (real file, then real file + block,
then block-filtered), which is why the fixture suite tails move D1/D2/… as their subjects vanish; the D7
clause is the measured one. The mutant removes exactly the two appended row lines
(`sed '/supersedes R22/d;/supersedes R23/d'`), so the flip is carried by these rows and nothing else.

The lane's full before-read, for the L1's cross-check:

```
D1 check=placeholders=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=0,provenance=1 open=1
D5 check=erratum-file=absent,discriminating-invocation=0,per-id-occurrences=0 open=1
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=3/7 exit=1
```

## 4. Findings

- **F1 — the block closes D7 and only D7 can close it here.** Before: `supersedes-R22=0,supersedes-R23=0
  open=1`. With the block: `1,1 open=0`. Filtering the two row lines: back to `0,0 open=1`. The literals
  occur exactly once each in the appended file (`grep -c -F` → `1`, `1`), so each row line is
  load-bearing on its own.
- **F2 — literal form matters.** The landed check is a case-sensitive fixed-string count, not a
  row-shaped regex; a row that only said "Supersedes R22" in sentence case, or "R22's grounding", would
  read `0`. Both draft rows carry the exact `supersedes R22` / `supersedes R23` forms, in the
  grounded-in cell where `R19` puts its `supersedes R13` clause.
- **F3 — one row, two purposes, stated in-row.** R26 is a new criterion *and* the R22 correction. The
  criterion cell says `R22's criterion is unchanged by this row`, so a reader is not asked to infer that
  R22 was rewritten; the supersession lives in the grounded-in cell.
- **F4 — R22's correction is not double authority for R25.** `R25` already cites M34-3
  (`corpus/QUALITY.md:229`). M34-3's own capture line records R22 as the criterion that existed "but had
  no planned-state limb" (`.ufo/waves/round-34/mistakes-erratum-1.md:18-20`), so the two citations read
  the same mistake from the two sides: R22 could not see it, R25 is the limb that fixes it. The draft's
  preamble says this in-place rather than leaving it to a reader.
- **F5 — R27 does not restore the narrowed limb.** The round-34 lesson records R23 as "narrower than the
  drafted criterion": `QUALITY.md:227` asks only for "citing the considerthese file and date", while the
  round-34 draft required a per-proposal disposition line, and the narrowing was "recorded here rather
  than corrected in place" (`corpus/lessons/round-34.md:352-358`). D7's scope is the grounded-in column,
  so R27 keeps R23's wording byte-for-byte (plus the explicit "unchanged by this row") and leaves the
  limb decision to the L1.
- **F6 — the cited instrument's digest has moved since the ledger row.** Live
  `corpus/instruments/score-gap.py` hashes to `57584fda83b813e44fb2e2cb6cb2b1e4af1dd20f07877a6b119db9ba9feb43cf`,
  while the round-31 ledger row (`corpus/knowledge/considerthese-proposals-ledger.md:28`) and
  `corpus/instruments/README.md:463` quote `855869bf97ae2081c24ed28630d587ad2988872b6625f6e0a1f8c7b2e3f201fb`.
  R9 forbids rewriting a filed record, so neither is edited here and R26 cites the **command**, not a
  digest; routed to the L1 as a dated drift observation, not a defect claim (I did not diff the two
  versions).
- **F7 — the live gap figure R26 obliges the lesson to cite.** `python3 corpus/instruments/score-gap.py`
  exit 0 (measured 2026-10-26 by this seat) prints
  `threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."`
  and `gap: 24 of 46 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`.
  Note the threshold line is `SCORECARD.md:331` today while `considerthese/2026-10-25.md:54` says `:327`
  — R26 therefore says "the recorded next-score threshold" and pins no line number.
- **F8 — every cited span was re-opened at the current revision** (not carried from the dispatch):
  `corpus/lessons/round-34.md:482-485` (open item 10, all four lines read), `:343-358` (§ considerthese
  incl. the narrowing paragraph), `.ufo/waves/round-34/mistakes-erratum-1.md:9-29` (M34-3 minted) and
  `:18-20` (its capture line), `corpus/lessons/round-34-verifier-spotcheck.md:199-203` (D7),
  `considerthese/2026-10-25.md:53-57` (proposal 2) and `:76` (proposal 6), `corpus/QUALITY.md:226-229`
  (R22, R23, R24, R25). R23's filed `considerthese/2026-10-25.md:76` is accurate; D7's point is that it
  is the only citation.
- **F9 — no forbidden literal rides in.** The block contains 0 occurrences of the SCORECARD placeholder
  token and 0 of `filled by the L1` (`grep -c` → 0 over the 2842-byte block), so it cannot re-open D1's
  kill clauses, and it adds no `<` `>` token that a later marker sweep could read as a placeholder.
- **F10 — quote fidelity.** The two quotations in the block are verbatim: `QUALITY R22 cites M34-2, but
  its grounding is M34-3 (lesson open item 10; `CritMistakes` F7)` from spotcheck `:200`, and "`none` at
  freeze time — `QUALITY.md` R22 (pre-freeze satisfiability) existed but had no planned-state limb" from
  erratum `:18-19` (its two wrapped source lines are joined on one line in the block; 14 words, under
  Q3's 25-word cap).

## 5. Out of scope / not done

- `corpus/QUALITY.md` not edited (the L1 applies §1); no other corpus path touched.
- No correction made to `considerthese-proposals-ledger.md` or `instruments/README.md` for F6 (R9
  append-only discipline; filed records are not rewritten in place by a scribe).
- The R23 disposition-limb restoration (F5) is not drafted — it changes R23's bar, not just its citation,
  and is the L1's call.
- No claim of a completed `score-gap.py` dossier: I ran it once, read exit 0 and its five field blocks'
  tail; I did not audit its internals.
- No subagents, no wave dispatch, no `agent://all`, no git/jj mutation, no writes outside the lane.

## Report

### Files read (path — sha256 at read time)

| path | sha256 |
|---|---|
| `corpus/QUALITY.md` | `807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8` |
| `corpus/lessons/round-34.md` | `aa60f4e9e2d6fc43e8c9ea9c0ccfae0aa3e52131000f6c9050836fb1b419f96b` |
| `corpus/lessons/round-34-verifier-spotcheck.md` | `dc10c6501a1992abb08880b1f8d8477992db70b03b3b3f985557036d0752748e` |
| `.ufo/waves/round-34/mistakes-erratum-1.md` | `1758d53480accc18b5fd9a39e4b6997ba8269eac0a04249ec10199959efae0c5` |
| `considerthese/2026-10-25.md` | `6adc24d64e3c04884d029d380278bb49b50f8e6e9c7bdc1951f56a38c027052e` |
| `corpus/knowledge/considerthese-proposals-ledger.md` | `c354ca0242bf7da44589e45c464deba0714dc083e2bf480a6c855ec30a1629c2` |
| `corpus/instruments/score-gap.py` | `57584fda83b813e44fb2e2cb6cb2b1e4af1dd20f07877a6b119db9ba9feb43cf` |
| `corpus/instruments/r35-defect-closure.sh` | `58ca311556a9f297ea8597b618c14e20f0dc0036e0bb525b31faa76c19894326` |
| `SCORECARD.md` | `51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7` |
| `.ufo/waves/round-34/claims.json` | read in-place (no digest taken; field `non_claim_frontier_items.mistake` quoted in F4/F6 reasoning) |
| `.ufo/waves/round-35/claims.json` | read in-place (frozen claims C1/C2 + non-claim frontier items; not edited) |

### Commands and outcomes (all read-only except the scratch tree and this receipt)

1. `wc -lc corpus/QUALITY.md` → `229 30889` (exit 0).
2. `sha256sum corpus/QUALITY.md` → `807cc714…b74a8` (exit 0).
3. `tail -c 60 corpus/QUALITY.md | xxd | tail -2` → file ends `… |0a` after `records=41`) |` (exit 0,
   i.e. final newline present; the append needs no separator fix).
4. `grep -nE '^\| R2[2-6] \|' corpus/QUALITY.md` → rows R22–R25 at lines 226–229, no R26/R27 (exit 0).
5. `grep -rln 'supersedes R22\|#{0,2} *Round-35 supersession' .ufo/waves/round-35 corpus` → matches only
   `.ufo/waves/round-35/{build-spec.py,wave1-spec.json,wave1-plan.out,wave1-dispatch.json}` and
   `corpus/instruments/r35-defect-closure.sh` (exit 0) — no peer seat had drafted or applied a
   `## Round-35 supersession` block, so this draft is the first.
6. `git status --porcelain corpus/QUALITY.md` → empty (exit 0): QUALITY.md unmodified at read time.
7. `stat -c '%y %s' corpus/QUALITY.md` → `2026-10-26 03:17:22.358907962 -0300 30889` (exit 0).
8. `python3 corpus/instruments/score-gap.py > out 2>&1` → exit 0; tail lines
   `threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."`
   and `gap: 24 of 46 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`;
   `grep -cE '^gap: '` → `1`.
9. `bash corpus/instruments/r35-defect-closure.sh` (lane) → exit 1, `D7 … open=1`, `closed=3/7 exit=1`
   (full text in §3).
10. `cat corpus/QUALITY.md $S/quality-append.md > $S/root-d7/corpus/QUALITY.md` then
    `bash corpus/instruments/r35-defect-closure.sh --root $S/root-d7` → exit 1,
    `D7 check=supersedes-R22=1,supersedes-R23=1 open=0`, `closed=1/7 exit=1`.
11. `sed '/supersedes R22/d;/supersedes R23/d' … > …/QUALITY.filtered.md`; `grep -c -F -- 'supersedes R22'`
    on it → `0`; same suite `--root $S/root-mut` → exit 1, `D7 … =0,=0 open=1`, `closed=0/7 exit=1`.
12. `head -c 30889 $S/root-d7/corpus/QUALITY.md | sha256sum` → `807cc714…b74a8`; `wc -lc` → `250 33731`
    (byte-prefix proof of the append, exit 0).
13. `grep -c -F -- 'supersedes R22' / …'R23'` on the appended file → `1` and `1` (exit 0).
14. `grep -c '<LANE_HASH>\|filled by the L1' $S/quality-append.md` → `0` (exit 0).
15. `sha256sum $S/quality-append.md` → `e3aa99a16b725335ceac2928f61d2d65ff1cc4e105c9c150fe51f2985eaa6918`;
    `wc -lc` → `21 2842`.
16. `awk 'NR>=482 && NR<=485' corpus/lessons/round-34.md`, `NR>=343 && NR<=358`, erratum `NR>=9 && NR<=30`,
    spotcheck `NR>=196 && NR<=208`, considerthese `NR>=53 && NR<=58` → the spans cited in §1/F8 (all
    exit 0, text quoted in F8/F10).
17. Fidelity of §1 as shipped:
    `sed -n '/BEGIN QUALITY[.]md append/,/END QUALITY[.]md append/p' .ufo/waves/round-35/wave1/ScribeQualityDraft.md | sed '1,3d' | head -n -3`
    (the two marker lines, the blank line and the fence lines dropped; the bracket in the pattern keeps this
    sentence from matching itself) → `wc -lc` `21 2842`,
    `sha256sum` `e3aa99a16b725335ceac2928f61d2d65ff1cc4e105c9c150fe51f2985eaa6918` (exit 0) — identical to
    the bytes measured in §3 before the scratch tree was removed.

### Tooling

No installs or upgrades. Tools used: `bash`, `coreutils`, `grep`, `sed`, `awk`, `sha256sum`, `python3`
(stdlib only), `xxd`. All present; no package transaction ran (pacman is paused host-wide).

### Scratch

`/fast/scratch/hyaku/kasegi-r35/ScribeQualityDraft/` held `quality-append.md`, `score-gap.out`,
`lane-run.out`, `d7-run.out`, `mut-run.out`, `root-d7/`, `root-mut/`. Values needed above were copied
into this receipt first; the tree was deleted at exit and the deletion verified (see §6).

### 6. Scratch cleanup evidence

```sh
rm -rf -- /fast/scratch/hyaku/kasegi-r35/ScribeQualityDraft
test -e /fast/scratch/hyaku/kasegi-r35/ScribeQualityDraft; echo "scratch_gone_rc=$?"   # 1 = gone
ls -d /fast/scratch/hyaku/kasegi-r35
```

Observed at exit: `scratch_gone_rc=1` (my tree is gone) and `ls -d` still lists
`/fast/scratch/hyaku/kasegi-r35` — the round's parent directory, shared with other seats' trees, so this
seat neither created nor removes it. My tree held `quality-append.md`, `score-gap.out`, `lane-run.out`,
`d7-run.out`, `mut-run.out`, `extracted.md`, `root-d7/`, `root-mut/`; every value quoted above was written
into this receipt before the removal.

**Verdict for the L1:** the §1 block is ready to append verbatim; on a copy it flips D7 from
`supersedes-R22=0,supersedes-R23=0 open=1` to `supersedes-R22=1,supersedes-R23=1 open=0` with the file's
first 30889 bytes unchanged. Two decisions are flagged, not taken: R26's dual purpose and R23's narrowed
limb (F3, F5).
