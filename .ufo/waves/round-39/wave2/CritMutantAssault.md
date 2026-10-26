# CritMutantAssault — round-39 wave 2: replay of the 25 named round-38 mutant shapes

Seat: CritMutantAssault (leaf, no subagents). Judged axis: depth:verifiability.
Item: replay the 25 named round-38 mutant shapes against the **landed r39 suite** in a
sandbox clone, one limb mutated per mutant, run `--selftest`, require every mutant
rejected (survivors = 0 for the targeted set); any survivor is a suite defect.

I did not author anything under attack. The suite (`corpus/instruments/r39-closure.sh`),
the receipt, the wave-1 artifacts and the frozen claims were written by other seats; my
only lane write is this receipt. I never edited the lane, the fleet root, or shokuknow.

## 0. Verdict in one paragraph

**Literal criterion passes; the intended criterion fails.** All 22 executable shapes
exit non-zero under `--selftest --export-ref <Y>`, but 18 of them are rejected by a single
whole-file limb (G2's `suite-sha256` self-digest), not by any fixture: their selftest
output at the base ref is **byte-identical to pristine** after normalising work paths.
Twelve of those 18 have a reachable isolating input — a tree where pristine and mutant
disagree (verified below) — so they are genuine fixture gaps, i.e. suite defects on
depth:verifiability. Six are equivalent/shadowed limbs (no input distinguishes them);
they cannot be killed by any fixture, so they are not evidence of coverage either.
Four shapes are killed by fixtures (M38-02, -05, -07, -08). Three of the 25 named shapes
have no limb in the landed bytes at all (retired by redesign).

## 1. Environment and write scope

- Lane repo read at HEAD `5006097a84305267c9a3e8c1e1d560e60fe41d37` (Y; J =
  `46c66c268502abd1b2c342fc71bf88ccf721845b` per `.ufo/waves/round-39/final-gates/all-gates.txt`
  `export-ref=`). Read-only clone into scratch; the lane repo was never written by me.
- Suite under test: `corpus/instruments/r39-closure.sh`, 1793 lines,
  `sha256 2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b` — equal to the
  receipt's `suite-sha256=` line, so the bytes under mutation are the bytes the claim scores.
- Scratch: `S=/fast/scratch/hyaku/kasegi-r39/CritMutantAssault` (all suite runs used
  `TMPDIR=$S` and `--work` under `$S`); removed before yield.
- No network fetches, no pacman, nothing installed or upgraded (bash/git/awk/python3 sufficed).

## 2. Method: two detectors, and why one alone is vacuous

Detector **A (the item's literal command)**: `bash <mutant> --selftest --export-ref 5006097a…`.

Detector **B (per-limb discrimination)**: the same selftest at the base ref
`480b1a505a2dfc14a4f718d16d63808247214d0a`, diffed against the pristine run. At the base
ref every positive fails in the pristine *and* in every mutant for the same reason (the base
export carries no round-39 files), so the only remaining variable is the fixture machinery:
a mutant is **killed by fixtures** iff its output differs from pristine's at all.

Detector **C (D3, isolating input)**: for each survivor, a purpose-built tree on which
pristine and mutant disagree in the verdict — the proof that the limb is load-bearing and
its missing fixture is a real gap.

### Why Detector A cannot attribute a kill (measured)

Pristine at Y: `selftest cases=8 failures=0`, exit 0. Normalised diff pristine → M38-01
at Y (`grep -v` of the header/export-ref/deviation lines, work paths and the g6 stderr path
normalised; payload middles elided with `…`, changed fields verbatim):

```
8c8
< selftest detail=G2 positive=pass payload=receipt=1,…,diff-read=ok,digest-match=1,…
> selftest detail=G2 positive=fail rc=1 payload=receipt=1,…,diff-read=ok,digest-match=0,…
17c17
< selftest case=G2 positive=pass mutants=8/8 verdict=pass
> selftest case=G2 positive=fail mutants=8/8 verdict=fail
57,58c57,58
< selftest cases=8 failures=0
< selftest judge=own-report accepted=1
---
> selftest cases=8 failures=1
> selftest judge=own-report accepted=0
```

Exactly one payload field changes (`digest-match`), in the check whose contract is "the
receipt's suite-sha256 equals the executing bytes". **Any one-byte change to the file reds
the selftest.** So `--selftest` at Y is a whole-file mutation detector; "every mutant
rejected" is a statement about file identity, not about the mutated limb. Every one of the
22 mutants shows `G2 positive=fail … digest-match=0` and every other case at full ratio.

## 3. The 25 named shapes: 22 executable, 3 retired

Round-38 lesson §Instrument attack findings names 19 MutG1G2 survivors (`wave1/MutG1G2.md`
table), 2 MutG3G4 survivors (`wave1/MutG3G4.md`: G3-M3, G3-M4) and 4 MutG5G8 survivors
(`wave1/MutG5G8.md`: F-G5/F-G6/F-G7/F-G8). Mapping them onto the landed r39 limbs:

| r38 shape | landed r39 limb | status |
|---|---|---|
| M3-G1-10 (readme-correction `-ge 1`) | **absent**: no minimum-correction conjunct; corrections are only tied to the declared tail (`cor_decl`) | retired |
| M3-G2-15 (name-status A/M-only) | **absent**: `grep -c 'name-status' = 0`; replaced by `diff --name-only` + "only the receipt path" | retired |
| M3-G2-17 (per-commit history) | **absent**: no commit walk; the two `history` hits are comments (L1127, L1428) | retired |

Measured: `grep -c 'name-status'` → `0`; `grep -cE '(pout|routh)[^)]*-[gi]e 1'` → `0`;
`grep -n history` → only L1127/L1428 comments. (Commands and output in §7.)

Each retired shape is a **redesign**, not a fixture gap: the successor limb is the
pure-append/diff-clean pair, and the diff-clean half is fixtured (M38-08 kill via
`post-receipt-diff-extra`). [INFERENCE] A pure rename of a second file inside
`export-ref..REF` would show two paths under `diff --name-only` and red `diff-clean`; I did
not build that input, and a rename of the receipt itself is red earlier (`receipt=0`).

## 4. Mutant table (22 executable shapes, one limb each)

`A` = Y-ref selftest (all exit 1); `B` = base-ref differential; `C` = isolating input.
`—` = no isolating input (equivalent limb, mechanism in F3). Mutant sha256 prefixes are
of the generated mutant files.

| id | r38 shape | mutation (one limb) | sha256 | A | B | C | class |
|---|---|---|---|---|---|---|---|
| M38-01 | M3-G1-01 | delete `&& [ "$pf" = closed ]` | f2c4f02e74eb | exit 1 | no delta | **D01 red→green** | **survivor** |
| M38-02 | M3-G1-02 | delete `&& [ "$rf" = closed ]` | 3aa14fe4bf6e | exit 1 | G1 3/4 | — | killed |
| M38-03 | M3-G1-03 | `index(s,"Correction (round 39)") == 1` → `> 0` | 17b20df52fe2 | exit 1 | no delta | **D03 green→red** | **survivor** |
| M38-04 | M3-G1-06 | delete `&& [ "$declared" -ge 2 ]` | a7bff41fad0a | exit 1 | no delta | — | equivalent (F3.1) |
| M38-05 | M3-G1-07 | `case $c in ''\|.) ;; ..) return 1 ;; esac` → drop `..)` | 9220829aef71 | exit 1 | G1 3/4 | — | killed |
| M38-06 | M3-G1-08 | README `[ "$c" -gt $((rtotal - decl_r)) ] \|\| cor_decl=0` → `:` | 09479e443c7c | exit 1 | no delta | **D06 red→green** | **survivor** |
| M38-07 | M3-G2-01 | delete `&& [ "$ancestor" -eq 1 ]` | daec8e008560 | exit 1 | G2 7/8 | — | killed |
| M38-08 | M3-G2-02 | delete `&& [ "$diffclean" -eq 1 ]` | 918867face8a | exit 1 | G2 7/8 | — | killed |
| M38-09 | M3-G2-03 | `'^closed=8/8 exit=0$'` → `'^closed=8/8'` | ee4eba8bf7e6 | exit 1 | no delta | **D09 red→green** | **survivor** |
| M38-10 | M3-G2-06 | `[ c1 -eq 8 ] && [ c0 -eq 0 ] && [ ids -eq 8 ] && run_ok=1` → `[ c0 -eq 0 ] && run_ok=1` | a4988d7a2d11 | exit 1 | no delta | **D10 red→green** | **survivor** |
| M38-11 | M3-G2-10 | delete `&& [ "$summary" -eq 1 ]` | 9d173d516c60 | exit 1 | no delta | **D11 red→green** | **survivor** |
| M38-12 | M3-G2-11 | delete `&& [ "$scref" -eq 1 ]` | 9ab6128fad69 | exit 1 | no delta | **D12 red→green** | **survivor** |
| M38-13 | M3-G2-12 | delete `&& [ "$shonenref" -eq 1 ]` | 26a3b37666f3 | exit 1 | no delta | **D13 red→green** | **survivor** |
| M38-14 | M3-G2-14 | `cat-file -t "${xref}^{commit}"` → `"${xref}"` | 141d3859e366 | exit 1 | no delta | D14 red→red | equivalent (F3.2) |
| M38-15 | M3-G2-16 | delete `[ -n "$xref" ] &&` | a1938c2e0b07 | exit 1 | no delta | — | equivalent (F3.3) |
| M38-16 | M3-G2-18 | `[ "$n" -eq 1 ]` → `[ "$n" -ge 1 ]` (export-ref count) | 0fff8a2beb0c | exit 1 | no delta | D16 red→red | equivalent (F3.4) |
| M38-17 | G3-M3 | `*closed=*` → `*closed=8/8*` | a4bc93a062b9 | exit 1 | no delta | **D17 red→green** | **survivor** |
| M38-18 | G3-M4 | drop `diffread=fail` from the diff-failure branch | 63eb4a38ad3a | exit 1 | no delta | **D18 red→green** | **survivor** |
| M38-19 | M-G5-corwid | drop `&& index($0,"f06148c6") > 0` from the `cor` awk | 390620d53d13 | exit 1 | no delta | D19 red→red | equivalent (F3.5) |
| M38-20 | M-G6-elifdel | delete `elif [ -e "$d" ] \|\| [ -L "$d" ]; then printf present` | e66caf861422 | exit 1 | no delta | **D20 red→green** | **survivor** |
| M38-21 | M-G7-secwid | `if (NR > s && $0 ~ /^## /) exit; print` → `print` | dff75fb2d715 | exit 1 | no delta | **D21 red→green** | **survivor** |
| M38-22 | M-G8-rcdel | delete `&& [ "$rc" -eq 0 ]` | 462a34438214 | exit 1 | no delta | D22 code-proof | equivalent (F3.6) |

Totals: **4 killed · 12 survivors (isolating input verified) · 6 equivalent · 3 retired**.
Generator asserts per mutant: find-string unique in the file (exactly one occurrence),
exactly one line changed, `bash -n` clean, and the executing digest in the run header
equals the mutant's own sha256 (22/22 — proof the mutant bytes ran).

Baselines (actual):
```
plain run                          -> "r39-closure: refusing to run against the live worktree…", exit 2
pristine @ Y   --selftest          -> selftest cases=8 failures=0        exit 0
pristine @ 480b1a5 --selftest      -> selftest cases=8 failures=6        exit 1
   (G1/G2/G4/G5/G7/G8 positive=fail; G3, G6 positive=pass; every fixture ratio full)
all 22 mutants @ Y                 -> exit 1 each
all 22 mutants @ 480b1a5           -> exit 1 each; 18 byte-identical to pristine, 4 delta
```

## 5. Findings

### F1 — the Y-ref selftest rejects a source mutant only through G2's file digest (structural)

Measured: 18/22 mutants produce output that is identical to pristine at the base ref after
normalising work paths, the script path and the header digest. Their Y-ref failure is the
single field `digest-match 1 → 0` (evidence in §2). Consequence: **a report that says
"all 25 round-38 shapes are rejected by `--selftest`" is true only as "the file hash
changed".** The suite's per-limb verdicts are the fixture lines, and those are where the
coverage has to be read. This is the same detector weakness round-38 recorded as
"counted, not graded"; r39 graded the *case lines* but did not make the fixtures track the
mutation.

### F2 — twelve surviving shapes have a reachable isolating input (suite defects)

Each demo (D<n>) builds a small tree, then runs `check_g<n>` from the **sourced pristine
suite** and from the **sourced mutant** (`BASH_SOURCE != $0`, so both are sourceable), with
`LANE`/`BASE_REF`/`WORK` set explicitly. Git fixtures: `git init` + toplevel asserted equal
to the fixture dir before any commit; commits use `-c user.email=demo@local`.

| demo | shape | isolating tree | pristine | mutant |
|---|---|---|---|---|
| D01 | M38-01 | PROVINCE gains an unclosed `~~~` fence inside its declared tail | `province-fence=open` **rc=1** | same payload **rc=0** |
| D03 | M38-03 | PROVINCE carries `Note: see Correction (round 39): …` mid-line above the declared tail | `corrections-outside=1 corrections-declared=1` **rc=0** | `corrections-outside=2 corrections-declared=0` **rc=1** (false red on a valid tree) |
| D06 | M38-06 | non-contiguous append: 2 lines inserted mid-file (one is a start-anchored `Correction (round 39)`), 2 lines appended at EOF, declare the last 4 | `corrections-declared=0` **rc=1** | **rc=0** |
| D09 | M38-09 | receipt whose last line is `closed=8/8 exit=1` | `closed-line=0` **rc=1** | `closed-line=1` **rc=0** |
| D10 | M38-10 | 8 `closed=1` run lines, one id duplicated (`G1` twice) | `distinct-ids=7` **rc=1** | **rc=0** |
| D11 | M38-11 | all 8 graded case lines, `selftest cases=8 failures=0` line removed | `selftest-summary=0` **rc=1** | **rc=0** |
| D12 | M38-12 | round-39 SCORECARD section without the judged-head phrase | `scorecard-ref=0` **rc=1** | **rc=0** |
| D13 | M38-13 | SHONEN round-39 line without the judged-head phrase | `shonen-ref=0` **rc=1** | **rc=0** |
| D17 | M38-17 | added line quoting `--export-ref 3333… -> closed=7/8 exit=1`, no transcript | `added-quotes=1,uncovered=1` **rc=1** | `added-quotes=0,uncovered=0` **rc=0** |
| D18 | M38-18 | lane repo without `BASE_REF` ancestry (diff read fails) | `diff-read=fail` **rc=1** | `diff-read=ok` **rc=0** |
| D20 | M38-20 | scratch root where `kasegi-r38` is a regular file | `r38=present` **rc=1** | `r38=absent` **rc=0** |
| D21 | M38-21 | round-39 dispositions section with rows and `Correction (round 39)` in the *next* `## ` section | `rows=0,correction=0` **rc=1** | `rows=4,correction=1` **rc=0** |

Missing fixture per shape (all are knobs on builders that already exist):
`g1_fixture pfence=yes`; `g1_fixture provcor=inline` (expect GREEN); `g1_fixture
noncontiguous=yes`; `g2_fixture closedline=exit1`; `g2_fixture dupid=yes`; `cases=nosummary`;
`scorecard-ref=no`; `shonen-ref=no`; `selftest_case_G3` red-run quote (`closed=7/8`);
`selftest_case_G3` no-base-ancestry repo; `selftest_case_G6` file root; `g7_fixture
trailing=rows`.

### F3 — six shapes are equivalent/shadowed limbs (not defects, not coverage)

- **F3.1 M38-04** (`declared -ge 2`): implied by the pass chain itself — `valid == declared`
  and `doors == 2`, and each door counter is set only for a *valid* line, so `valid ≥ 2`.
  No single-fault input can isolate it. (Same class round-38 F-C recorded for `valid -ge 2`;
  r39 changed the subject to `declared` but did not make it discriminating.)
- **F3.2 M38-14** (`${xref}^{commit}` peel): a non-commit name is still rejected downstream.
  D14 (`export-ref=<blob sha>`): pristine **rc=1** `ancestor=0,diff-clean=0`; mutant **rc=1**
  `ancestor=0,diff-clean=0,diff-read=fail`. Verdict unchanged; only the payload's
  `diff-read` value differs.
- **F3.3 M38-15** (`[ -n "$xref" ]`): when `xref` is empty the whole ancestor/diff block is
  skipped, so `ancestor=0 ∧ diffclean=0` already force red. Logically redundant.
- **F3.4 M38-16** (export-ref count widened to `-ge 1`): D16 (two identical `export-ref=`
  lines): pristine **rc=1** (`export-ref=0,ancestor=0,diff-clean=0`), mutant **rc=1**
  (`export-ref=1,ancestor=0,diff-clean=0`) — the multi-line `xref` cannot resolve, so the
  duplicate is still caught. Closed by construction.
- **F3.5 M38-19** (hash conjunct dropped from `cor`): `ro` carries the same hash conjunct,
  and the pass chain needs `ro ≥ 1`, so `ro ≥ 1 ⇒ cor ≥ 1`. D19 (correction naming
  `9abcdef0` with `report-only`): pristine **rc=1** `correction=0,correction-labeled=0`;
  mutant **rc=1** `correction=1,correction-labeled=0`. Round-38 F-G5's gap is closed by
  construction, not by a fixture.
- **F3.6 M38-22** (`[ "$rc" -eq 0 ]`): for the pinned bytes the two signals are the same
  bit. `git show 2387dcf6:corpus/instruments/r37-closure.sh` lines 868–871:

  ```
  868:  if [ "$k" -eq 14 ]; then
  869-    printf 'closed=%s/14 exit=0\n' "$k"
  870-    return 0
  871-  fi
  ```

  That is the only emitter of the pinned line and it returns 0; `main`'s `run)` branch
  returns that status. So `last == 'closed=14/14 exit=0' ⟺ rc == 0`, and the conjunct
  cannot be exercised by any fixture that must hash to `PIN_R37_SHA` first.

### F4 — the four killed shapes, and their kill mechanism

- **M38-02** → `selftest case=G1 mutants=3/4`; `tilde-opener-closed-by-backticks rejected=0
  rc=0 payload=…readme-fence=open`. Fixture pins the readme-fence conjunct.
- **M38-05** → `declaration-path-escape rejected=0 rc=1 payload=…paths=1…diff-read=fail`:
  the mutilated guard no longer yields `paths=0`, so the payload needle fails even though the
  check still reds (via the diff read). Killed on the needle — acceptable, but note the tree
  is red for a different reason than the fixture intends.
- **M38-07** → `export-ref-not-ancestor rejected=0 rc=0 payload=…ancestor=0…` (the fixture
  repo is real in r39, so the round-38 F-A vacuity is fixed).
- **M38-08** → `post-receipt-diff-extra rejected=0 rc=0 payload=…diff-clean=0…`.

## 6. Impact on the frozen claim, and the smallest safe correction

C1's predicate is **not falsified as written**: its "one graded `selftest case=G<n> …
verdict=pass` line per check whose mutants are all rejected" refers to the suite's own
fixture mutants, and every case line is `mutants=n/n` with `n ≥ 1` (4/4, 8/8, 2/2, 6/6,
4/4, 4/4, 3/3, 3/3) at Y, judged `accepted=1` with zero fixture `rejected=0`. What is
falsified is the **round-38 closure claim this item exists to enforce**: survivors = 0 for
the 25 named shapes. Fixture-level survivors = 12; equivalence-level = 6; retired = 3;
killed = 4.

Impacted axis: `depth:verifiability` (4). The suite's *own* verdicts at J/Y stand — G1–G8
close the routed R1–R4 defects and the four base-red/r38-red controls are unchanged. The
overstatement risk is in the round-39 narrative: "the 25 round-38 mutants are now fixtures"
is false for 12 of them, and vacuous for the other 6.

Smallest safe correction (for the L1 — I apply nothing):
1. Report the count as **killed 4 / equivalent 6 / unfixtured 12 / retired 3**, not
   "survivors = 0"; and say plainly that `--selftest` at Y reds any source mutation through
   `G2 digest-match`, so it is not per-limb evidence.
2. If fixtures are added, the twelve knobs in F2 are each one branch in an existing
   builder; the cheapest three with the largest payload (D01 province fence, D21 G7
   trailing rows, D20 G6 file root) close the shapes round-38 named explicitly
   (F-B province half, F-G7, F-G6).
3. Keep the six equivalent limbs as defence-in-depth, labelled as such — do not add
   fixtures for them (impossible) and do not count them as coverage.

## 7. Reproduction (exact commands)

```
S=/fast/scratch/hyaku/kasegi-r39/CritMutantAssault
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kasegi-shokunin "$S/lane"
sha256sum "$S/lane/corpus/instruments/r39-closure.sh"
  -> 2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b
python3 mutants.py "$S/lane/corpus/instruments/r39-closure.sh" "$S/mut"
  -> generated 22 mutants; all find-strings unique
bash "$S/mut/M38-01.sh" --selftest --export-ref 5006097a84305267c9a3e8c1e1d560e60fe41d37 \
     --lane "$S/lane" --work "$S/wk/M38-01" --scratch-root "$S/sroot"      # -> exit 1
# same with --export-ref 480b1a505a2dfc14a4f718d16d63808247214d0a for detector B
bash demos.sh                                                              # D01..D22
```

Deviation recorded: my runs pass `--lane <sandbox clone>` and
`--scratch-root <isolated empty dir>` (the suite prints `deviation=non-default --lane` /
`--scratch-root`). The scratch-root override is required because the default
`/fast/scratch/hyaku` sees this seat's own scratch dir as a `kasegi-r39` sibling, which G6
would red for an environmental reason; with an empty root G6 is green in both pristine and
every mutant, so the override cannot mask a G6 kill (M38-20's D20 demo sets the root
explicitly). The lane override points at a byte-identical clone at Y; the pristine run there
prints `selftest cases=8 failures=0`.

Retirement evidence:
```
grep -c 'name-status' corpus/instruments/r39-closure.sh                       -> 0
grep -cE '(pout|routh)[^)]*-[gi]e 1' corpus/instruments/r39-closure.sh        -> 0
grep -n 'history' corpus/instruments/r39-closure.sh                            -> 1127 (comment), 1428 (comment)
```

## 8. Hygiene

- Lane writes: this receipt only. No git/jj mutation anywhere (clones/fixtures were created
  with `git init` in scratch, toplevel asserted before every commit; commits use
  `-c user.email=demo@local`, never a global identity).
- Restoration: pristine re-runs at Y and at base after the campaign are byte-identical to
  the baselines recorded above; the lane's suite bytes were never written (all 22 mutants
  live under `$S/mut`).
- Scratch `$S` removed on exit.
