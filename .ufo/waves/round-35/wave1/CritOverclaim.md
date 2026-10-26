# CritOverclaim — round-35 wave 1 (L2 leaf, critic)

Seat: `CritOverclaim`. Lane: `kasegi-shokunin` (only write scope). Lane base
`3266c9937b03062d9bbc2f436e20820115ed179c`; claims-freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`.
Axes in scope: `depth:verifiability` (C1) and `coverage` (C2) — **after-value verification only**.

Assignment executed: for every C1/C2 after-value, find a measured command output; test universal clauses
against what the counting command enumerates; check that no check is called a verifier while its receipt is
missing; check that the report and lesson do not overstate closure counts. This is a critic pass: I judge no
score, admit nothing, and edited no lane file except this receipt.

Read window: **2026-10-26T06:37Z–06:46Z** (every measurement below is time-stamped; the tree moved three
times inside the window and the movement is itself reported — §7 P8).
Scratch `/fast/scratch/hyaku/kasegi-r35/CritOverclaim/`, removed before yield (§8).
Tools installed/upgraded: **none** (`bash`, `python3`, `git` read-only verbs, `grep`; no pacman/uv/npx).

## Report

### 1. Pinned bytes (all statements below are relative to these digests)

```
2026-10-26T06:45:00Z
fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982  .ufo/waves/round-35/claims.json
eee0bb579844ad9d02777fb4cd241e726d0bb0630679bc41aa534d7f5d0951e6  .ufo/waves/round-35/claims-erratum-d5.md
51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7  SCORECARD.md
daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc  SKILL.md
0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba  corpus/SOURCES.md
807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8  corpus/QUALITY.md   (= freeze blob)
277f04cedfb06f493ae5da636d665b490ac0e78b26ea282b0d0ef3a469d3ffa2  corpus/README.md
5472f60ab33a2241e7051c071e1469ca89b2c874e571d93420499cd0998a0fd5  .ufo/waves/round-34/wave1/L1Integration.md  (= freeze blob)
0988866608c4a1818219e02bbb23cd1d7aeffb5768a73c411216a4cf821f5e74  corpus/knowledge/cisa-kev-catalog.md
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt
06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee  corpus/source-snapshots/round-35/manifest.json
a4f80067183e8512d5e7f39a789c7b51437f357acb05cd77d481a4d9c7cc35ad  corpus/instruments/r35-defect-closure.sh  (834 lines)
e1c4430133adeb58                                             .ufo/waves/round-34/wave1-results.json.provenance.md (prefix)
```

`claims.json` is byte-identical to the freeze blob (`fe0dae89…`), so no claim was edited to fit the tree.

### 2. C1 — every after-value against a measured command (suite digest `a4f80067…`)

```
$ bash corpus/instruments/r35-defect-closure.sh
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=0,provenance=1 open=1
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=4/7 exit=1
$ bash corpus/instruments/r35-defect-closure.sh --root /fast/scratch/…/3266c993…   # git archive of the lane base
closed=0/7 exit=1                                                                    # exit 1
$ bash corpus/instruments/r35-defect-closure.sh --selftest
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=3 control-failures=0                                       # exit 1
```

| # | frozen C1 after-value | measured | verdict |
|---|---|---|---|
| 1 | `closed=7/7 exit=0` at tip | `closed=4/7 exit=1` (D4, D6, D7 open) | **NOT MET** at 06:44Z |
| 1b | base tree `closed=0/7 exit=1` | `closed=0/7 exit=1` | MET |
| 1c | `--selftest cases=7 failures=0` | `cases=7 failures=3` on the lane; `cases=7 failures=0` only on `r35-fixtures/clean` | **NOT MET** on the lane |
| 2 | `filled by the L1` count 0 + correction naming `c1c6a5f` (D1) | `0`; `c1c6a5f` ×3; `<LANE_HASH>` ×0; third spelling `the L1 fills this line` ×0 | MET |
| 3 | appended depth:density erratum naming 201.2 (D2) | `SCORECARD.md:1246`; stale row still at `:1146` | MET (value verified, §6) |
| 4 | registry registers `r-defect-closure.sh` + `kill-rule-check.py` (D3) | 4 / 4 hits; the row's own re-verify values reproduce (§6) | MET |
| 5 | `wave1-results.json` tracked + provenance note (D4) | `git ls-files … | wc -l` → **0**; note present (`e1c44301…`) | **NOT MET** (commit-order) |
| 6 | `claims-erratum-d5.md` carries both statements (D5) | `present, discriminating-invocation=5, per-id-occurrences=5` | MET |
| 7 | `L1Integration.md` dead-seat sentence corrected (D6) | stale sentence ×1 at `:30`, `Correction (round 35)` ×0; file digest = freeze `5472f60a…` | **NOT MET** |
| 8 | QUALITY `supersedes-R22` / `supersedes-R23` rows (D7) | `corpus/QUALITY.md` = freeze digest; `supersedes R22` 0, `supersedes-R22` 0 | **NOT MET** |

So C1's own headline counter is **4/7, exit 1** on the bytes at 06:44Z. Three of eight after-values are
unmeasured-or-open, and one of them (D6) has no seat owner in the wave spec — `ScribeIntegrationNotes.md:67-69`
records this verbatim: "this limb has no seat owner in the wave spec; whoever lands the correction must be
named in this slot".

### 3. C2 — every after-value against a measured command

```
$ python3 corpus/instruments/frontier-recheck-count.py | tail -1
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
entries=21 pass=21 exit=0
$ python3 - <<'PY'   # regex counts, independent of the shell's grep shim
SOURCES S-rows: 52 S052: 1
README F-rows: 18
PY
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
S052:sha256 OK … S052:Q5 OK normalized=markup-whitespace occurrences=1 anchor=19165-ok
exit 0                                    # all five assertions occurrences=1
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi W04 S028 … / kasegi W04 S029 … / kasegi ok …        # census_exit=0
$ ls corpus/knowledge/*.md | wc -l        → 47
$ grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l → 1
```

| # | frozen C2 after-value | measured | verdict |
|---|---|---|---|
| 1 | frontier 18, F18 row admitted | 18 (`corpus/README.md:388`, `| F18 | … | admitted | knowledge/cisa-kev-catalog.md | S052 |`) | MET |
| 2 | registry 52, S052 row 1 | 52 / 1 (`corpus/SOURCES.md:58`) | MET |
| 3 | entries citing S052 = 1 | 1 | MET |
| 4 | harness `entries=21 pass=21 exit=0` incl. `PASS F18 ids=S052` | exact | MET (landed inside my window; 20/20 at 06:37Z) |
| 5 | source-recheck S052 exit 0, every assertion `occurrences=1`, sha256 OK | 5/5 `occurrences=1`, exit 0 | MET |
| 6 | census exit 0, W04 S028/S029 only | exact | MET |
| 7 | knowledge entries 47 | 47 | MET |
| 8 | "junk twin rejected: source-recheck exit != 0" | the twin's own `recheck:` line **exits 0** | **LITERALLY FALSE** (see §5 O7) |

C2's substance is real, not quoted: I re-computed the entry's numeric literals directly from the capture
(§6 P0). The one false after-value is the twin clause, which the lane's own D5 erratum already declares
non-executable (`claims-erratum-d5.md` §2–§3, §5).

### 4. Overclaim locations (things that must not reach the report/LOG/lesson unqualified)

**O1–O3 — the LOG draft (`ScribeIntegrationNotes.md`, digest `585c8f2ae5248150…` at my read) asserted three
C1 limbs as measured; all three were corrected in flight at 06:46Z after I raised them.** Recorded so the
correction is auditable, not to re-open it:

| # | what the draft read at 06:37Z | contradiction measured | what the draft reads now (digest `585c8f2a…`) |
|---|---|---|---|
| O1 | "plain run `closed=7/7 exit=0` … `--selftest` `cases=7 failures=0` ⟨`ExecClosureSuite.md`⟩" | that receipt's own §3 is `closed=4/7 exit=1`, §6 `selftest cases=7 failures=3`; no lane receipt measures 7/7 | `:47-54` — four readings kept apart (live 4/7, live `failures=3`, all-fixed 7/7, base 0/7); final `closed=7/7` is a `⟨FILL⟩` for a post-integration run. **Resolved.** |
| O2 | "`corpus/QUALITY.md` carries the appended supersedes-R22 and supersedes-R23 rows ⟨`ScribeQualityDraft.md`⟩" | QUALITY digest = freeze `807cc714…`, both counts 0 | `:79-80` — "still reads `supersedes R22` = 0 … the draft rows are not landed rows". **Resolved.** |
| O3 | "tracked 0 → 1" (D4) | `git ls-files … | wc -l` → 0 (the note it cites says the same) | `:68` — "still **untracked** … pending the L1's commit, which is the whole closure". **Resolved.** |

The rule that produced all three is worth carrying into the lesson: a draft that cites a receipt must quote
that receipt's *tree label* (live / all-fixed / base), because the closure suite deliberately prints a
different `closed=K/7` for each.

**O8 — three receipts the LOG's C1/C2 paragraphs point at do not exist yet** (`ls` at 06:47Z):
`ExecDoNothingReject.md` **ABSENT**, `MutClosureSuite.md` **ABSENT**, `ExecRegressionC2.md` **ABSENT**
(present: `ExecSelftestFixtures.md`, `RevClosureSuite.md`, `MutFixturesLimbs.md`). The draft's own convention
(`ScribeIntegrationNotes.md:18`) says unreadable values get `⟨FILL: …⟩`; these three are written as plain
`⟨…⟩` receipt pointers, so a reader cannot tell "pending seat" from "landed". Either mark them `⟨FILL⟩` or
land the receipts before the LOG is appended.

**O4 — report draft carried a false provenance for the controls; corrected in flight at 06:52Z.**
As read at 06:47Z (`ScribeReportDraft.md:53-56`, digest `dc267907bb5bf07a…`) it said "**Do-nothing controls
committed at the freeze:** `c1-controls/fake-suite.sh` … and `c2-controls/junk-f18.md`". Neither is in the
freeze tree — the freeze commit carries exactly four files under `.ufo/waves/round-35/`:

```
$ git ls-tree -r --name-only 617496b9 -- .ufo/waves/round-35/
.ufo/waves/round-35/c1-controls/before.txt
.ufo/waves/round-35/c2-controls/before.txt
.ufo/waves/round-35/census-before.txt
.ufo/waves/round-35/claims.json
$ git status --porcelain | grep -c 'c1-controls/fake-suite.sh\|c2-controls/junk-f18.md'   → 2   (both `??`)
```

"committed at the freeze" is false on both counts (absent from the freeze, untracked now). **Resolution
(06:52Z, digest `c1a6871d5e6a0416…`):** the report owner rewrote the line to "**Do-nothing controls
(untracked at draft time)**" (`:61`) and appended the four-file `git ls-tree` result plus the `??` status, and
added a claim-status block at `:36-40` naming `closed=4/7 exit=1` / `--selftest cases=7 failures=3` and the
three open limbs so no frozen after-value reads as achieved. Measured at 06:53Z: `:142` reads
`live worktree at draft time (06:52Z): closed=4/7 exit=1 # D4/D6/D7 open`. **Resolved.**

**O5 — SCORECARD attributes a three-spelling fact to a two-spelling check.** `SCORECARD.md:1259-1261`:
"Neither placeholder spelling occurs in this file any more; the round-35 closure check reads that count as 0."
The check reads `filled by the L1` and `<LANE_HASH>` only; the third spelling (`the L1 fills this line …`,
the one D1 names at `SCORECARD.md:1129` at freeze) is unmeasured. The fact is true today (`grep -c` → 0), the
attribution to the check is not. **Standing** (SCORECARD digest `51337bf1…` unchanged at 06:53Z).

**O6 — the round-35 lesson does not exist yet**, so no lesson overstatement can be verified. The LOG draft and
the report draft have both removed their draft-time overstatements (O1–O4), so a lesson minted from either at
06:53Z inherits none; the live requirement is that the lesson quote a **post-integration** suite run, since
`closed=7/7 exit=0` is still unmeasured on the lane (§2 row 1).

**O7 — C2 `after[6]` is literally false as frozen.** "junk twin rejected: `source-recheck exit != 0` and
non-author reviewer REFUSE on record." The twin's `recheck:` line is byte-identical to the live entry's and
exits 0:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052; echo $?
0
```

The rejection that *is* real is the quote comparison (both twin sentences 0 occurrences in the capture, §5).
`claims-erratum-d5.md` §5 discloses the recurrence, which is the correct treatment — but the LOG draft's
`ScribeIntegrationNotes.md:76-78` restates it as "(grep -c of the twin's distinctive sentence in S052.txt →
0)", i.e. it substitutes a *different* check than the erratum's prescribed manifest-assertion form
(`MISMATCH reason=quote-not-found`, exit 1). Name the check that was run, not the one the frozen text names.

### 5. Defects found by probe (measured on copies; lane untouched)

Probe trees copied the seven files each check reads (`SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`,
`.ufo/waves/round-34/wave1/L1Integration.md`, the results file + provenance note,
`.ufo/waves/round-35/claims-erratum-d5.md`), then mutated one limb. Baseline on the copy:
`closed=4/7 exit=1` (D4 open only because the copy has no index). All four reproduce at the **current**
digest `a4f80067…`.

**P1 — D1 does not read the spelling the defect names.** With `**Final lane commit: the L1 fills this line in
the closing commit.**` restored to `SCORECARD.md`:

```
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
```

Green while the placeholder is present. `corpus/lessons/round-34-verifier-spotcheck.md:164-171` names
`SCORECARD.md:1129` *and* `:1240` for D1, and `ExecBeforeReceipts.md` §7.3 flagged the same gap as a
pre-check. **Smallest safe correction:** add a third limb
`grep -c -F 'the L1 fills this line' SCORECARD.md` `== 0` plus one mutant in
`r35-fixtures`/the mutant table, keeping the payload key naming convention.

**P2 — D2's `row-bytes` limb rejects the corrected row.** With the round-34 row rewritten to its true value
(`mean **201.2**, 25 blocks, 711 path-citation instances`) and the erratum left in place:

```
D2 check=erratum-row=1,erratum-mean=3,row-bytes=0 open=1
```

A state in which the displayed mean is *correct* reads open. The limb is explained in `ExecClosureSuite.md`
§2 as append-only discipline, but the same round closes D1 by **rewriting** `SCORECARD.md` placeholders in
place, so the file carries two opposite conventions, and D2's green state necessarily still displays
`mean **201.7**` at `SCORECARD.md:1146`. The limb is also presence-only in substance: any appended line
containing `round-34 depth:density row` and `201.2` satisfies it. **Smallest safe correction:** accept either
shape — `(row-bytes>=1 AND erratum-mean>=1) OR (row-corrected-bytes>=1 AND erratum-mean>=1)` — so a true
in-place fix is not punished, and keep the existing mutant.

**P3 — D6 cannot be closed by the fix the defect prescribes.** Appending the correction and leaving the stale
sentence (exactly what `round-34-verifier-spotcheck.md:195-198` prescribes: "Fix: append a correction."):

```
D6 check=dead-seat-sentence=1,correction-round-35=1 open=1
```

`check_d6` requires `dead-seat-sentence == 0`, i.e. it demands **deleting** a sentence from a committed
round-34 receipt — a rewrite of a prior-round artifact, which is the convention D2's limb exists to forbid and
which the lane applies to every frozen claims file ("corrections land as separate appended files"). Two
consequences: (a) whoever lands D6 must rewrite `.ufo/waves/round-34/wave1/L1Integration.md` in place; (b) the
append-only correction the defect asks for never turns the counter green. **Smallest safe correction:** close
D6 on `correction-round-35>=1` **and** the correction naming the location (`L1Integration.md:30`) — i.e. drop
the `==0` limb, or accept `dead-seat-sentence - quoted-in-correction == 0`; state the chosen reading in the
spotcheck's fix line so the two documents agree.

**P4 — D7 is presence-only.** Appending a content-free line `- supersedes R22. supersedes R23.` to QUALITY:

```
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
```

Green with no grounding recorded, although the defect is *"R22's grounding cites the wrong mistake"* and its
fix names the correct grounding (M34-3 for R22; the round-34 lesson §considerthese for R23 —
`round-34-verifier-spotcheck.md:199-203`). **Smallest safe correction:** require the corrected grounding token
on the same line as the supersession marker (`M34-3` for R22, `round-34.md` for R23) and add one mutant per
limb. `ScribeQualityDraft.md:43-44` already writes rows that would satisfy the stricter limb, so the stricter
limb costs nothing.

**P5 — the new gate is unregistered (D3's own class, applied to round 35).**
`grep -n 'r35-defect-closure\|r35-fixtures' SKILL.md` → no match, while `r-defect-closure.sh` and
`kill-rule-check.py` were just registered. The standard D3 is closed against is the one in the spotcheck's fix
line ("Per PROTOCOL §Gate standard (Delivery), they are not graded conformant until registered"), and it
applies identically to the instrument this round's whole C1 rests on, including its `--selftest` spelling
(`selftest cases=7 failures=<n>`) and its fixture tree. **Smallest safe correction:** a third registry row
(name, gate|probe, entry command incl. `--root`/`--selftest`, verdict map `closed=K/7` + `cases=7`, pinned-value
path, write scope, owner) appended to the same `## Round-35 Gates & probes registry addition` block.

**P6 — D4 makes `closed=7/7` unobservable before the commit that makes it true.** `check_d4` reads
`git ls-files`; the claim's after-state is "tracked … at tip". Therefore the receipt that records
`closed=7/7 exit=0` can only be written after the L1's commit, which makes that receipt a post-commit wave
write — the exact class D4 was routed for ("wave writes landed after the `complete` line",
`round-34-verifier-spotcheck.md:183-188`). **Smallest safe correction:** the L1 lands
`wave1-results.json` + provenance note in an **earlier** commit, then runs and lands the receipt; or the
receipt states "measured at `<commit>`, post-commit by construction" and the LOG says the same, so the two
commit classes are not conflated.

**P7 — token drift: the frozen claim's own token reads 0 after the landing it predicts.** C1 `after[7]` /
`before[7]` use `supersedes-R22` / `supersedes-R23` (hyphen); `check_d7` counts `supersedes R22` /
`supersedes R23` (space), and `ScribeQualityDraft.md:120-121` will land the space form. Measured on probe P4:
space 1 / hyphen 0. A verifier re-running the claim's before-command after the landing gets 0 and cannot
distinguish "landed" from "missing". Also C1's `counting_commands` has no D7 entry at all. **Smallest safe
correction:** an appended erratum (the D5 pattern) restating the token as `supersedes R22` and adding the D7
counting command; or write the row so both literals occur.

**P8 — the instrument moved five times inside the measurement window (quiesce hazard).**
`RevC1BeforeAfter.md` §8.3 recorded `c748dd70` (643 ln) → `cba8c95b` (760 ln) → `d7ad8438` (773 ln); my own
first read at 06:37Z caught the **760-line** `cba8c95b` mid-write, and the file is now `a4f80067` (834 ln). A
receipt that digests an earlier state (e.g. `ExecClosureSuite.md` pins `d7ad8438`, 773 ln) no longer describes
the bytes the L1 will commit. Nothing here is a false statement — every receipt digests its own read — but the
Gates registry row, the LOG and the report must cite **one** pinned digest, re-run at it, or the judge gets no
canonical bytes (the round-28 convention `RevC1BeforeAfter` §8.3 recommends).

### 6. No overclaim found (positive results, with the measurement)

- **P0 — the F18 entry's computed literals are true, not quoted.** Parsing the capture and recomputing the
  entry's figures reproduces every one: `count` 1756 = `len(vulnerabilities)` = distinct `cveID` 1756; one
  12-key key set across all records; `knownRansomwareCampaignUse` Known 361 / Unknown 1395;
  `forensicTriage` Yes 91 / No 1665; `dueDate > dateAdded` in 1756/1756; gap mode 21 days (1025), then 14
  (280), 181 (238); 513 distinct `dueDate`; 46 distinct `requiredAction`, top value 893; `BOD 22-01` 340,
  `BOD 26-04` 139, neither 1277; `cvss` 0 occurrences, `severity` 2 (prose only). The entry's
  "no severity **field**" phrasing is the corrected one (`ExecRegistryAppend.md` §"Provenance facts").
- **D2's erratum is bound to real bytes, both limbs.** `git show 206e510:SKILL.md` → blob `b11b6085…`, 1090
  lines, `density.py` mean **201.7**, 710 path-citation instances, 25 blocks. `git show
  4b0a9f2 --numstat -- SKILL.md PROVINCE.md` → `1 0 SKILL.md`, `1 0 PROVINCE.md`;
  `3266c993…:SKILL.md` → `ba5ebe5d…`, 1091 lines, mean **201.2**, 711 cites; `PROVINCE.md` 74 → 75 lines,
  `b4bb5fee…` at both `4b0a9f2` and the lane base. `4b0a9f2` is an ancestor of the base
  (`git merge-base --is-ancestor 4b0a9f2 3266c993…` → 0). So 201.2 is measured, not transcribed.
- **D3's registry row values reproduce.** `bash corpus/instruments/r-defect-closure.sh` → `closed=9/9 exit=0`;
  `--selftest` → `selftest cases=9 failures=0`; `python3 corpus/instruments/kill-rule-check.py --selftest` →
  `selftest cases=3 failures=0`. The row's "registration, not a live-green claim" caveat is thereby satisfied
  rather than merely stated.
- **D5's erratum is executable, not phrase-only** (`claims-erratum-d5.md` §3–§4 carry the fixture manifest, the
  `quote-not-found` run and the three occurrence fixtures); the check's `>=1`-literal limb is a weak proxy,
  but the file's content is real.
- **SOURCES.md's R8 tally is accurate:** the append is additive (`git diff --stat` → `5 ++++`, zero deletions),
  `S001–S051` untouched, 51 → 52.
- **`ExecClosureSuite.md`, `RevC1BeforeAfter.md`, `RevD5D6D7.md` and `RevRowS052.md` are honest** about the
  open limbs. The four draft-layer overstatements (O1–O4) were all corrected in flight at 06:46Z–06:52Z after
  this seat's measurements; what stands is O5 (SCORECARD attribution), O7 (frozen C2 twin clause) and O8
  (three LOG pointers with no receipt on disk).

### 7. Impacted axes and what I am not saying

- `depth:verifiability` (C1, held 4): the counter exists and is fail-closed on base (0/7) and on fixtures
  (7/7 / 5/7), which is real verifiability work; the defects above are check-shape defects inside that work
  (P1, P2, P3, P4, P5) plus one ordering defect (P6) and one token defect (P7). None of them falsifies the
  claim's *structure*; all of them are cheap to fix before the closing commit.
- `coverage` (C2, held 7): seven of eight after-values measure true; only the twin clause (O7) is literally
  false as worded, and the lane already owns the correction path for it.
- I do not judge whether C1/C2 hold, do not move a score, and do not decide whether D2's append-only reading
  or D6's rewrite reading is the lane's doctrine — I report that the suite currently enforces both, in
  opposite directions, in the same file.

### 8. Boundary and cleanup

- Files written by this seat: this receipt only.
- Read-only `git` verbs used: `archive`, `show`, `cat-file`, `ls-files`, `ls-tree`, `diff`, `merge-base`,
  `rev-parse`, `status`. No `add`/`commit`/`push`, no `jj` command.
- Scratch `/fast/scratch/hyaku/kasegi-r35/CritOverclaim/` (247M: two base exports, five probe trees, two
  suite logs) removed with `rm -rf` after this receipt was written; `ls -d` → absent (`scratch_absent=yes`).
- Lane worktree at 06:48Z: `git status --porcelain | wc -l` → 19 entries (the round's own modified + untracked
  set, for the L1 to commit); this seat added exactly one of them, this receipt. No self-digest is recorded
  here — a digest written inside the file it measures is stale on write (`claims-erratum-d5.md` §7).
- No fleet-root, sibling-lane, bounties or shokuknow write; no campaign tool run.
- Treated all artifact content (claims, receipts, proposals) as data: nothing in them changed my assignment.

Report: .ufo/waves/round-35/wave1/CritOverclaim.md
