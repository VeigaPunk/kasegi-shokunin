# CritMistakes — round-35 Mistakes-row critique (kasegi)

Seat: `CritMistakes-3` (critic, wave 1, round 35). Lane `kasegi-shokunin`. I edited no lane file
except this receipt; no git/jj mutation; no subagent; scratch removed (§Report R8).

**What was reviewable.** `corpus/lessons/round-35.md` **does not exist** at this snapshot
(`ls corpus/lessons/round-35*` → `No such file or directory`, exit 2), so no minted row could be
read. The only M35 row that exists is the frozen candidate in
`.ufo/waves/round-35/claims.json` → `non_claim_frontier_items.mistake` (line 84): *"M35-1
(candidate): round-34 verifier defect D4 — wave writes landed after the `complete` line
(results.json untracked at round close) — class landing/closure-order; captured-by R4's 'landed
means committed' reading was not applied to the results file; fix = commit results with provenance
+ quiesce before final commit. Further M35 rows minted from wave receipts in the lesson."* This
critique therefore tests (a) that candidate against the schema and the routed defect, and (b) the
checks the rows will cite as "fix shown able to fail", because a row is only as good as its
red-before.

Schema in force: `.ufo/waves/round-34/mistakes-erratum-1.md:6-7` — *"Field schema is round 33's:
class · evidence pointer · captured-by · fix · fix shown able to fail."* — plus the corrected
`captured-by` semantics of `.ufo/waves/round-34/wave1/CritMistakes.md:126-127` (*"it is a
criterion, not a capturing seat … the criterion has its own field (`**Criterion:**`)"*).

---

## F1 — M35-1 as frozen is a prose row in its two decisive fields (REPAIR REQUIRED)

| required field | frozen M35-1 | measured verdict |
|---|---|---|
| evidence pointer | **absent** — names "round-34 verifier defect D4" but no `file:line` | FAIL: the two pointers are `corpus/lessons/round-34-verifier-spotcheck.md:30` (§1 row "No uncommitted round work") and `:183` (§6 "D4 — wave writes after the `complete` line") |
| captured-by | `R4's 'landed means committed' reading` | FAIL: `corpus/QUALITY.md:38` is criterion **R4**, not a seat — the identical error M34-1 was corrected for. `Criterion missed: R4`, `Captured by: none` |
| fix | commit results with provenance + quiesce before final commit | HALF-MEASURABLE: the tracked/provenance limbs exist (below); "quiesce" has no instrument (`grep -rln 'quiesce' corpus/instruments/` → `corpus/instruments/README.md` only, prose) |
| fix shown able to fail | not stated | PARTIAL: two clauses with two mutants, but the provenance clause measures existence, not landing (F1b) |
| class | landing/closure-order, results file only | NARROWER than D4, which has two limbs (`:183-187`): the untracked results file **and** a seat's transient rewrite of the committed `wave1/ExecRegressionC1.md` |

### F1a — `captured-by: none` is the truthful value, measured

```
$ grep -rln 'wave1-results.json' .ufo/waves/round-34/wave1/ | wc -l      → 0     (67 receipt files)
$ grep -c 'wave1-results.json' .ufo/waves/round-34/wave1-results.json    → 0     (the file never names itself)
$ ls -l --time-style=full-iso .ufo/waves/round-34/wave1-results.json
  … 2026-10-26 03:23:19.274615406 -0300  (≈06:23:19Z; the driver's `complete` line is 03:19:31 -03:00 ≈06:19:31Z)
```

The writer was the **wave dispatcher**, not a seat; no round-34 seat receipt mentions the file. So
the row's field is `Captured by: none` (as a defect) + `Criterion missed: R4` + `Routed by: round-34
verifier spot-check §1 row 5 / §6 D4`. This is exactly the M34-2 pattern
(`corpus/lessons/round-34.md:256-259`: *"`Captured by: none` **as a defect** … first filed as a
defect by the round-33 verifier R1"*), and it is the opposite of what the frozen candidate wrote.

### F1b — the D4 fix *can* fail on the tracked limb, and *cannot* on the provenance limb

Red-before exists and is re-runnable at the freeze commit:

```
$ git cat-file -e 617496b9c6e92bc671e7e78b83df69a04470d0e9:.ufo/waves/round-34/wave1-results.json
fatal: path … exists on disk, but not in '617496b9…'                          exit 128
$ git cat-file -e 617496b9…:.ufo/waves/round-34/wave1-results.json.provenance.md
fatal: path … exists on disk, but not in '617496b9…'                          exit 128
$ git ls-files -- .ufo/waves/round-34/wave1-results.json | wc -l              → 0   (live, 06:44:03Z)
$ git ls-files -- .ufo/waves/round-34/wave1-results.json.provenance.md | wc -l → 0  (live, 06:44:03Z)
```

and the live suite currently reads `D4 check=tracked=0,provenance=1 open=1` — a genuine red on the
landed tree. The instrument's clauses are real (`corpus/instruments/r35-defect-closure.sh:201-212`,
digest `a4f80067…`), with one mutant per limb (`D4:-tracked` `:414`, `D4:-provenance` `:420`).

**But the second clause cannot see the failure it names.** `check_d4` counts the note by existence:

```
:206   if [ -f .ufo/waves/round-34/wave1-results.json.provenance.md ]; then prov=1; else prov=0; fi
```

Counterexample (fixture B: a git repo with the results JSON committed and the note present but
**not** added):

```
$ git ls-files -- .ufo/waves/round-34/wave1-results.json.provenance.md | wc -l → 0
$ bash corpus/instruments/r35-defect-closure.sh --root <fixture B>
D4 check=tracked=1,provenance=1 open=0
```

So committing the JSON alone — leaving the provenance note an uncommitted wave write — reads
`open=0`. That is the D4 class one level in: a wave artefact that did not land. Note the instrument's
own `D4:-tracked` fixture *tracks the note* (`:414-418`: `git add -- …provenance.md`) while
`check_d4` never counts it — the fixture and the clause disagree about whether note-tracking
matters.

**Smallest safe correction (one clause, no frozen-claim edit):**

```
prov=$(git ls-files -- .ufo/waves/round-34/wave1-results.json.provenance.md 2>/dev/null | wc -l)
[ "$tracked" -eq 1 ] && [ "$prov" -eq 1 ] && exit 0
```

(or count both paths in one `git ls-files … | wc -l` = 2). Red/green: fixture B then reads
`provenance=0 open=1`; the landed state after `git add` of both reads `2/2 open=0`.

### F1c — the fix text must be split, because half of it is not the lane's to fix

"Quiesce or kill wave seats before the L1's final commit" is **dispatcher** behaviour; the lane
cannot check it and no instrument references it. The row should say: lane-side =
`tracked=1 AND note_tracked=1` (the clause above); harness-side = post-`complete` writes, owner the
wave dispatcher, check `git status --porcelain` empty at closure start
(`corpus/lessons/round-34-verifier-spotcheck.md:30`, first column) — i.e. cited as an environment
fact, not as a lane fix.

### F1d — proposed replacement row (paste-ready; the frozen claims text is not editable)

> **M35-1 — round 34's wave wrote its results file after the round was declared complete.**
> Class: landing / closure-order. **Evidence:** `corpus/lessons/round-34-verifier-spotcheck.md:30`
> (`?? .ufo/waves/round-34/wave1-results.json`, 312874 B, `sha256 3afa3581…`, mtime 06:23:19Z vs
> the driver's `complete` line 06:19:31Z) and `:183` (§6 D4, both limbs). **Captured by:** `none`
> — the writer was the dispatcher and no round-34 seat receipt names the file
> (`grep -rln 'wave1-results.json' .ufo/waves/round-34/wave1/` → 0 of 67).
> **Criterion missed:** R4 (`corpus/QUALITY.md:38`). **Routed by:** round-34 verifier spot-check.
> **Fix:** `corpus/instruments/r35-defect-closure.sh` `check_d4` (`:201-212`) requires the results
> file tracked **and the provenance note tracked**, with one mutant per limb (`:414`, `:420`);
> `ExecD4ResultsTrack` filed the note (`.ufo/waves/round-34/wave1-results.json.provenance.md`,
> `sha256 e1c44301…`). **Fix shown able to fail:** at freeze both `git cat-file -e` calls exit 128
> and the live tree reads `tracked=0,provenance=1 open=1`; a tree with the JSON tracked and the note
> untracked reads `tracked=1,provenance=1 open=0` today (measured), which is why the note clause
> must count `git ls-files`, not `[ -f ]`. Owner for the second limb (post-`complete` dispatcher
> writes) is the harness, not the lane.

---

## F2 — M35-2 candidate (recommended): the registry limb was satisfied by a sibling instrument name; the round's own closure suite is unregistered

The frozen C1 kill rule is *"`SKILL.md` Gates & probes registry registers r-defect-closure.sh +
kill-rule-check.py"*, and the suite the claim actually runs is
`corpus/instruments/r35-defect-closure.sh`. Those are different files, and only the older one is
registered:

```
$ grep -c -F 'r35-defect-closure' SKILL.md      → 0
$ grep -c -F 'r-defect-closure'  SKILL.md      → 4     (rows SKILL.md:1097-1098)
$ bash corpus/instruments/r35-defect-closure.sh   (06:44:03Z, suite sha a4f80067…)
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
```

`check_d3` (`:188-199`) counts the substring `r-defect-closure`, which the fallback name does not
share with `r35-`; so the round's own gate passes D3 **while having no registry row at all**. Per
PROTOCOL §Gate standard as quoted at `corpus/lessons/round-34-verifier-spotcheck.md:180`
(*"not graded conformant until registered"*), the round's closure authority is unregistered at tip.

- **Captured by:** `ExecD3SkillRegistry` (receipt `:163-171`, finding 1 — *"Name split inside claim
  C1 … If C1 lands a separate `r35-defect-closure.sh`, that file still has no registry row"*) and
  `ExecScoreGap` (`:301-303`, same row's anchor red). Two seats, both non-authors of the suite.
- **Fix:** append an eight-field registry row for `r35-defect-closure.sh`, and widen `check_d3` to
  the exact basename (`grep -c -F 'r35-defect-closure.sh'`) with its own `fix_re`/mutant so a
  `filter_out` mutant reopens it (construction already exists: `D3:-registry-r-defect-closure`
  `:406-409`).
- **Able to fail:** the live tree is the red fixture — `grep -c 'r35-defect-closure' SKILL.md` → 0
  while D3 reads `open=0`. After the row lands, the `filter_out 'r35-defect-closure.sh'` mutant must
  print `registry-r35-defect-closure=0 … open=1`.

This is the strongest row of the round: the mistake is not a stale sentence, it is a check whose
literal is satisfied by a near-name sibling — a duplicate-authority defect one round after D3 was
routed for exactly this class.

---

## F3 — M35-3 candidate (recommended): the D1 closure clause does not implement the widening D1's own routed fix names

D1's routed fix is not only "append a correction"; it says *"widen the R1 check to placeholder
prose"* (`corpus/lessons/round-34-verifier-spotcheck.md:145-148`). The landed `check_d1` (`:160-172`)
has three literals — `filled by the L1`, `<LANE_HASH>`, `correction-c1c6a5f` — and no prose clause
(`clause_specs D1` `:265-269`, `mutant_specs D1` `:327-330`; no mutant for a prose spelling).

The prose spelling is the one that actually occurred: `grep -c 'the L1 fills this line'
SCORECARD.md` → **1** at freeze at `:1129` (`wave1/ExecBeforeReceipts.md:215-221`, finding 3). It is
0 now only because a seat hand-edited the sentence; the check never sees it.

Counterexample (fixture A: `filled by the L1`=0, `<LANE_HASH>`=0, one `c1c6a5f`, plus
`**Final lane commit: the L1 fills this line in the closing commit.**`):

```
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
```

- **Captured by:** `ExecBeforeReceipts` (finding 3, receipt `:215-221`) — it predicted the miss
  before the suite existed.
- **Fix:** one clause `prose-placeholders=$(grep -c -F 'the L1 fills this line' SCORECARD.md)` = 0
  with its own mutant.
- **Able to fail:** fixture A is the red fixture; with the clause it must read
  `prose-placeholders=1 … open=1`, and the same fixture with the sentence removed reads `open=0`.

---

## F4 — M35-4 candidate (recommended, may merge with F3 as "closure clauses satisfiable by non-corrective prose"): D2's erratum limbs are unscoped phrase greps

`check_d2` (`:174-186`) requires `erratum-row = grep -c -F 'round-34 depth:density row'` ≥ 1 and
`erratum-mean = grep -c -F '201.2'` ≥ 1 **anywhere** in `SCORECARD.md`, plus the stale row's exact
bytes (`row-bytes`). No correction is needed:

```
# fixture A SCORECARD.md, no correction anywhere:
Note for the reader: the round-34 depth:density row is discussed below. Unrelated: 201.2 is a
number that appears in another sentence and corrects nothing.
| depth:density | 9 | mean **201.7**, 25 blocks, 710 path-citation instances | round 34 |
→ D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
```

`wave1/ExecBeforeReceipts.md:207-214` (finding 2) warned that the global `201.7 == 0` form is
unsatisfiable; the landed check correctly inverted the **row** clause to presence (append-only
convention) but left the **erratum** limbs global and unconjoined.

- **Captured by:** `CritMistakes-3` (this seat, measured above); the near-miss is
  `ExecBeforeReceipts` finding 2.
- **Fix:** require the conjunction on one line, e.g.
  `grep -cE 'round-34 depth:density row.*201\.2' SCORECARD.md` ≥ 1 (or a dated
  `Correction (round 35)` marker), keeping `row-bytes` as is.
- **Able to fail:** fixture A reads `open=1` under the conjunction; the landed SCORECARD
  (`sha256 51337bf1…`) reads ≥ 1 line carrying both literals.

---

## F5 — M35-5 candidate (recommended, with a red-before caveat): the new registry row itself tripped the SKILL anchor gate

`ExecScoreGap.md:301-303` measured `anchorcheck.py SKILL.md` **exit 1** with `BASE-ABSENT=1`
because the row `SKILL.md:1097` carried a bare `S050.txt:70`; the addendum (`:310-330`) records the
fix and re-run: SKILL.md `0cc95638…` → `daeff71b…`, *"16 in-range, 0 bad, LOST-RECORDED=306,
BASE-ABSENT=0, exit 0"*.

- **Class:** register-a-gate-by-writing-a-file-that-fails-a-gate.
- **Captured by:** `ExecScoreGap` (peer message to `ExecD3SkillRegistry` before either yielded).
- **Fix:** landed — the token is now `corpus/source-snapshots/round-32/S050.txt:70`.
- **Able to fail:** `python3 corpus/instruments/anchorcheck.py SKILL.md` exit 1 on the pre-fix
  digest, exit 0 after. **Caveat the row must keep:** the pre-fix bytes are transient (digest-pinned
  in the receipt, not in the tree), so the red-before is receipt-captured, not re-runnable from
  committed bytes — the same caveat M34-1 carries (`corpus/lessons/round-34.md:251-252`). A
  re-runnable form is to plant the bare token in a fixture.

---

## F6 — M35-6 candidate (conditional; must be marked "fix not landed"): the before-controls remain output-only for the fourth round

`wave1/ExecBeforeReceipts.md:204-223` (finding 4): both `before.txt` files record values and labels
with no argv, and no instrument consumes them —

```
$ grep -rln 'before.txt' corpus/instruments/     → corpus/instruments/README.md (prose only)
```

This is a standing reproducibility cost (`R18` penalises the same shape on the after side), not a
single-round slip. If the L1 mints it, the fix cell must say **not landed** and the able-to-fail cell
must be the absent-check (`grep -c` → 0 at tip), never a green. If no runner lands this round, the
row is a standing-item row and belongs in the lesson's open items, not in Mistakes — a Mistakes row
whose fix never lands is exactly the prose-without-check the schema forbids.

---

## F7 — Candidates I recommend **not** minting as mistake rows

- **Dispatch URL 404** (`wave1/ExecC2Capture.md:181-186`). External drift, not lane behaviour, and
  the artefact choice is already recorded in the committed manifest; a mistake row would cite a
  live-network fact that cannot be re-run offline. Keep it as a lesson caveat under C2.
- **Entry-before-expected-list transient** (`wave1/ExecScoreGap.md:341-345`): `recheck-audit.py`
  exit 1 with `unexpected=corpus/knowledge/cisa-kev-catalog.md` for 35 s, then exit 0. That is the
  completeness gate firing correctly and the seat recording it; recording it as a mistake would
  penalise the guard. Cite as Gate evidence.

---

## Minting contract the lesson must satisfy (each row, without exception)

1. **Class** named in the lane's vocabulary and no narrower than the routed defect it learns from
   (F1's class was narrower than D4's two limbs).
2. **Evidence** = `file:line` plus the command and its output, both re-runnable from committed bytes
   or explicitly flagged as receipt-pinned (F5).
3. **Captured by** = seat ids that hold the truth in committed receipts, or `none`; a criterion goes
   in a separate `Criterion missed:` field (M34 F3 precedent, `corpus/QUALITY.md:38` = R4).
4. **Fix** = the landed artefact with its path and digest, or the words *not landed* plus an owner.
   "Quiesce"/process language without an instrument (F1c) cannot be the whole fix.
5. **Fix shown able to fail** = one command, a red value and a green value, where the red value is
   reachable without editing production files (fixtures under `corpus/instruments/r35-fixtures/` or
   scratch). A clause satisfiable by non-corrective prose (F3, F4) or by an uncommitted file (F1b)
   does not satisfy this cell.
6. **Numbering** = rows beyond M35-1 land in a separate appended erratum
   (`.ufo/waves/round-35/mistakes-erratum-1.md`, the `.ufo/waves/round-34/mistakes-erratum-1.md`
   form) before any surface cites `M35-2+`; the lesson may mark them *provisional* meanwhile
   (`corpus/lessons/round-34.md:232-236`).

## Verdict

- **M35-1 as frozen: FAIL as written** — wrong field type in `captured-by` (a criterion, the exact
  error M34-1 was corrected for), no evidence pointer, a fix half of which has no instrument, and a
  class narrower than the routed defect. It is **repairable without touching the frozen claim**
  (erratum is the vehicle); the paste-ready form is F1d. The D4 clause pair is real and its tracked
  limb is genuinely red-before today; its provenance limb must count `git ls-files` (F1b, one line).
- **Additional rows: none exist yet.** Three are recommended with landed or one-line fixes
  (F2 registry coverage — the strongest, with a live counterexample; F3 D1 prose clause; F4 D2
  conjunction), one with a red-before caveat (F5), one conditional on a fix landing (F6). Two
  candidates should not be minted (F7).
- **Frontier item status:** *"mistakes M35-1+ minted in the lesson"* is **UNMET** at this snapshot
  (`corpus/lessons/round-35.md` absent). A lesson that prints the frozen M35-1 sentence verbatim
  would be the prose row this seat is chartered to flag.

---

## Report

All commands run in the lane repo (`/home/vgpnk/Projects/shokunin/kasegi-shokunin`) unless a scratch
path is named. Snapshots: `2026-10-26T06:43:00Z`, `06:43:55Z`, `06:44:03Z` (UTC). The suite was
under edit during this seat (`d799c591…` at 06:43:00Z → `a4f80067…` at 06:43:29 -0300); every
quoted suite line number below is for **`sha256 a4f80067…` (834 lines)**, and the fixtures were
re-run at that digest.

### R1 — reviewability of the lesson

```
$ ls corpus/lessons/round-35*
ls: cannot access 'corpus/lessons/round-35*': No such file or directory        exit 2
$ ls corpus/lessons/ | grep -E '3[4-9]'
round-34-verifier-spotcheck.md
round-34.md
```

### R2 — the frozen candidate row and the schema

```
$ grep -n 'M35-' .ufo/waves/round-35/claims.json
84:    "mistake": "M35-1 (candidate): round-34 verifier defect D4 - wave writes landed after the
    `complete` line (results.json untracked at round close) - class landing/closure-order;
    captured-by R4's 'landed means committed' reading was not applied to the results file;
    fix = commit results with provenance + quiesce before final commit. Further M35 rows minted
    from wave receipts in the lesson.",
$ grep -n '^| R4 ' corpus/QUALITY.md
38:| R4 | A round counts only with a resolvable work commit (`git cat-file -e`) and a before→after
    measurement; a rendered wave is not execution and a marker is not a round. | M1 — …
$ sed -n '6,7p' .ufo/waves/round-34/mistakes-erratum-1.md
through this separate appended file. Field schema is round 33's: class ·
evidence pointer · captured-by · fix · fix shown able to fail.
$ sed -n '126,127p' .ufo/waves/round-34/wave1/CritMistakes.md
cover the overstatement — but it is a criterion, not a capturing seat, and the sibling row uses the field
for seats (`none`). Under round-33's schema the criterion has its own field (`**Criterion:**`).
```

### R3 — D4 evidence and capture provenance

```
$ sed -n '30p;183,187p' corpus/lessons/round-34-verifier-spotcheck.md
30:| No uncommitted round work | `git -C kasegi-shokunin status --porcelain` | … At 06:23:46Z:
   `?? .ufo/waves/round-34/wave1-results.json` (312874 B, sha256 `3afa3581afb14aba…`, written
   06:23:19Z, 65 results) | **defect D4**: wave writes landed after the `complete` line |
183:- **D4 — wave writes after the `complete` line.**
184-  - The wave dispatcher wrote untracked `.ufo/waves/round-34/wave1-results.json` at 06:23:19Z.
185-  - A seat transiently rewrote the committed `wave1/ExecRegressionC1.md` at 06:21:33Z, claiming
186-    measurement "at c1c6a5f", then restored it.
187-  - Fix: commit `wave1-results.json` with a provenance note. The L1 must quiesce or kill wave seats

$ grep -rln 'wave1-results.json' .ufo/waves/round-34/wave1/ | wc -l        → 0
$ grep -c 'wave1-results.json' .ufo/waves/round-34/wave1-results.json     → 0
$ ls -l --time-style=full-iso .ufo/waves/round-34/wave1-results.json
  -rw-r--r-- … 312874 2026-10-26 03:23:19.274615406 -0300
```

### R4 — D4 red-before and the provenance-clause counterexample

```
$ git cat-file -e 617496b9c6e92bc671e7e78b83df69a04470d0e9:.ufo/waves/round-34/wave1-results.json
fatal: path … exists on disk, but not in '617496b9…'                            exit 128
$ git cat-file -e 617496b9…:.ufo/waves/round-34/wave1-results.json.provenance.md
fatal: path … exists on disk, but not in '617496b9…'                            exit 128
$ git ls-files -- .ufo/waves/round-34/wave1-results.json | wc -l                → 0
$ git ls-files -- .ufo/waves/round-34/wave1-results.json.provenance.md | wc -l   → 0
$ bash corpus/instruments/r35-defect-closure.sh        (06:44:03Z, suite a4f80067…)
D4 check=tracked=0,provenance=1 open=1
```

Fixture B (`/fast/scratch/hyaku/kasegi-r35/CritMistakes/d4`: `git init`, results JSON `git add`ed,
provenance note written but not added):

```
$ git ls-files -- .ufo/waves/round-34/wave1-results.json.provenance.md | wc -l   → 0
$ bash corpus/instruments/r35-defect-closure.sh --root <fixture B>     (suite a4f80067…)
D4 check=tracked=1,provenance=1 open=0                                 exit 1 (other checks open)
```

### R5 — D1/D2/D3 counterexample fixture A

```
fixture A SCORECARD.md includes:  **Final lane commit: the L1 fills this line in the closing
commit.**  |  one unrelated c1c6a5f mention  |  the stale row  |  "the round-34 depth:density row
is discussed below. Unrelated: 201.2 is a number …"
fixture A SKILL.md registers only r-defect-closure.sh and kill-rule-check.py.

$ bash corpus/instruments/r35-defect-closure.sh --root <fixture A>     (suite a4f80067…)
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
closed=3/7 exit=1
```

### R6 — live tree at 06:44:03Z (mid-wave; not a round verdict)

```
$ sha256sum corpus/instruments/r35-defect-closure.sh SCORECARD.md SKILL.md
a4f80067183e8512d5e7f39a789c7b51437f357acb05cd77d481a4d9c7cc35ad  corpus/instruments/r35-defect-closure.sh
51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7  SCORECARD.md
daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc  SKILL.md
$ bash corpus/instruments/r35-defect-closure.sh
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=0,provenance=1 open=1
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=4/7 exit=1                                                              exit 1
$ grep -c -F 'r35-defect-closure' SKILL.md      → 0
$ grep -c -F 'r-defect-closure'  SKILL.md      → 4        (rows SKILL.md:1097-1098)
$ grep -rln 'quiesce' corpus/instruments/      → corpus/instruments/README.md   (prose only)
```

Suite anchors cited above (digest `a4f80067…`): `check_d1` `:160-172`, `check_d2` `:174-186`,
`check_d3` `:188-199`, `check_d4` `:201-212` (`[ -f ]` at `:206`), `clause_specs` `:263`, `fix_re`
`:306`, `mutant_specs` `:325`, `D3:-registry-r-defect-closure` `:406-409`,
`D3:-registry-kill-rule` `:410-413`, `D4:-tracked` `:414`, `D4:-provenance` `:420`.

### R7 — file digests (as read)

```
51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7  SCORECARD.md
daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc  SKILL.md
807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8  corpus/QUALITY.md
dc10c6501a1992abb08880b1f8d8477992db70b03b3b3f985557036d0752748e  corpus/lessons/round-34-verifier-spotcheck.md
1758d53480accc18b5fd9a39e4b6997ba8269eac0a04249ec10199959efae0c5  .ufo/waves/round-34/mistakes-erratum-1.md
3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4  .ufo/waves/round-34/wave1-results.json
e1c4430133adeb58b8d3b3af9edcb49739eacd3f40536dca529105c609e86c98  .ufo/waves/round-34/wave1-results.json.provenance.md
fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982  .ufo/waves/round-35/claims.json
805cc4b74e6b550c32ad901fb531f1bcb96dd59f95f1f2526e7954dbdc2b89b5  .ufo/waves/round-35/wave1/ExecD3SkillRegistry.md
fe795dd3b4eedd252aece34c5bbde11d3d1c83cd9ba7f5a583f2841d1f2a20c4  .ufo/waves/round-35/wave1/ExecScoreGap.md
167902c7f29fbb3daeaffea07e703973031e4283d1c6d183c252571e8cfc0a34  .ufo/waves/round-35/wave1/ExecBeforeReceipts.md
a46242849c1f1223af904dbdc8576deba2a09fbfee9828c7f0f06487fdc0f82e  .ufo/waves/round-35/wave1/ExecD4ResultsTrack.md
a4f80067183e8512d5e7f39a789c7b51437f357acb05cd77d481a4d9c7cc35ad  corpus/instruments/r35-defect-closure.sh
```

### R8 — scratch

All work under `/fast/scratch/hyaku/kasegi-r35/CritMistakes/` (fixture A `tree/`, fixture B `d4/`,
≈40 K). Removed before this receipt was finalised:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r35/CritMistakes
$ test ! -e /fast/scratch/hyaku/kasegi-r35/CritMistakes && echo clean    → clean (exit 0)
$ ls /fast/scratch/hyaku/kasegi-r35/                                    → only sibling seats' dirs
```

No tool install or upgrade. No subagent, no wave dispatch, no `agent://all`. Only read-only git
(`cat-file`, `ls-files`, `ls-tree`, `status` — the last two at 06:43 only) and no jj call. Files
written in the lane: this receipt only.
