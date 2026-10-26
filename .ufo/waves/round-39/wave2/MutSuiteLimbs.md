# MutSuiteLimbs — round-39 wave-2 (falsify): mutation test of r39-closure.sh limbs G1–G8

Seat: MutSuiteLimbs (leaf, no subagents). Item: mutate the landed
`corpus/instruments/r39-closure.sh` one limb at a time in a sandbox clone (one mutation per
run), run `--selftest --export-ref <Y>` per the item spec, and record for each mutation
whether the selftest catches it or it survives; cover every conjunct of G1–G8 at least once.
Any surviving mutation is a suite defect: report the mutation and the limb.
Full table (95 runs, every mutation with exact edit, verdict and evidence):
`.ufo/waves/round-39/wave2/MutSuiteLimbs.mutations.txt`.

Date: 2026-10-26. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` read-only to this
seat; read-only git only; no mutating git/jj command anywhere; no writes outside the three
allowed paths plus scratch. I am not the author of the suite under attack.

## 0. Target bytes and refs (measured at campaign start)

- lane tip / verification ref **Y** = `5006097a84305267c9a3e8c1e1d560e60fe41d37`
- judged head **J** = `46c66c268502abd1b2c342fc71bf88ccf721845b`;
  `git diff --name-only J Y` = `.ufo/waves/round-39/final-gates/all-gates.txt` only → Y = J + receipt (erratum E4)
- suite bytes sha256 = `2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b`
  = the committed receipt's `suite-sha256` (verified equal)
- pinned r37 digest constant `PIN_R37_SHA` = `0da98e37…42434d`, pin commit `2387dcf6…`
- base `480b1a505a2dfc14a4f718d16d63808247214d0a`

## 1. Detector, and why it is differential (E5 non-vacuous semantics)

The item's literal command (`bash <mutant> --selftest --export-ref Y`) cannot by itself
discriminate limbs on this suite: the receipt's `suite-sha256` binds the **executing**
bytes, so *any* byte mutation trips G2's positive limb against the stale real receipt.
Measured control **M0** (one comment byte changed, no semantics touched):

```
selftest case=G2 positive=fail mutants=8/8 verdict=fail
selftest cases=8 failures=1            (exit=1; all 34 fixtures still rejected=1)
```

That catch is independent of the mutated limb and evaporates in the real threat model — a
defective suite committed together with its own fresh receipt (the normal landing
workflow) regenerates `suite-sha256` from the mutated bytes, the tripwire goes blind, and
the **only** remaining discrimination is the selftest's built-in fixture set. The
authoritative detector is therefore differential at fixed ref Y, per the round-38
precedent (`wave1/MutG1G2.md` §Detector note) and erratum E5:

- **KILLED** — the verdict layer reacts vs pristine: a fixture flips to `rejected=0`, a
  positive/control flips to fail (non-tripwire), a judge forgery flips, or failures>1.
- **SURVIVED** — the only delta vs pristine is the M0 tripwire signature (or payload
  values inside still-passing lines): the limb is pinned by no fixture, so a defective
  suite with a fresh receipt self-certifies. Per the item, every survivor is reported.

Both columns are in the table: `lit.fail` (the literal failures count) and the verdict.

## 2. Stabilization (measured, disclosed by the suite's own deviation= lines)

- `--lane $S/lanesnap`: clean clone of the lane at Y. The real worktree holds untracked
  wave-2 files from concurrent sibling seats, and the pinned r37 suite's live E9 limb
  (`status --porcelain` empty, lane HEAD == export ref) reds G8 on any run against it.
  Measured literal pristine run (default lane + default scratch root): **failures=2** —
  `G6 … r39=present,work=inside,tolerated=none` (26 sibling seat dirs under
  `/fast/scratch/hyaku/kasegi-r39` at probe time) and
  `G8 … pinned-sha=1,export-copy=1,r37-copy=1,r37-closed=0,r37-exit=1` (dirty worktree).
  Both are environmental, not suite defects; the stabilized baseline removes them.
- `--scratch-root $S/sroot`: private empty dir, same reason for G6.
- Plain local clone (hardlinked objects; every git call against it is read-only —
  archive/show/diff/merge-base/cat-file/rev-parse; no gc/repack ever runs). Identical
  objects verified for Y, J, base, PIN_REF.
- Determinism: a repeat pristine run is byte-identical after path normalization
  (delta = 0 lines).

## 3. Pristine baseline (stabilized) — the suite is green at Y before any mutation

```
$ bash $S/pristine/r39-closure.sh --selftest --export-ref 5006097a84305267c9a3e8c1e1d560e60fe41d37 \
      --lane $S/lanesnap --work $S/work-base --scratch-root $S/sroot
selftest case=G1 positive=pass mutants=4/4 verdict=pass
selftest case=G2 positive=pass mutants=8/8 verdict=pass
selftest case=G3 positive=pass mutants=2/2 verdict=pass
selftest case=G4 positive=pass mutants=6/6 verdict=pass
selftest case=G5 positive=pass mutants=4/4 verdict=pass
selftest case=G6 positive=pass mutants=4/4 verdict=pass
selftest case=G7 positive=pass mutants=3/3 verdict=pass
selftest case=G8 positive=pass mutants=3/3 verdict=pass
selftest cases=8 failures=0
selftest judge=own-report accepted=1        (+ six forgeries all rejected=1)
exit=0
```

(Captured verbatim from the run; the same eight graded lines and tally are in the
committed receipt's selftest block, re-verified against the export.)

## 4. Campaign result

**95 runs = 1 control (M0) + 94 limb mutants. 34 KILLED, 60 SURVIVED.**

| check | mutants | killed | survived |
|---|---|---|---|
| G1 | 25 | 5 | 20 |
| G2 | 27 | 6 | 21 |
| G3 | 5 | 2 | 3 |
| G4 | 11 | 5 | 6 |
| G5 | 5 | 4 | 1 |
| G6 | 8 | 5 | 3 |
| G7 | 7 | 4 | 3 |
| G8 | 6 | 3 | 3 |
| **total** | **94** | **34** | **60** |

Survivor taxonomy: **34 live holes** (fixture-unpinned limbs that gate real defect
classes), 21 dead/redundant conjuncts (implied by sibling conjuncts — unpinned but
harmless), 2 masked single routes of a doubly-enforced limb, 1 reporting-only, 1
weakened-parser-outcome-preserved, 1 unreachable fail-open.

## 5. Findings — the live holes (suite defects per the item; C1's frozen predicate itself is NOT falsified)

The frozen C1 predicate's stated behavior **holds as measured** at Y: `closed=8/8 exit=0`
over the receipt-bearing tip, `selftest cases=8 failures=0` with eight graded lines, all
built-in fixtures rejected, all six forgeries rejected, judge accepted. What the campaign
falsifies is the *strength* behind that line: the fixture set pins only 34 of 94 one-limb
mutants. The material holes, by check:

- **F1 · G2 · the tamper-evidence limb is itself unpinned (M-G2-15, strongest).** Dropping
  `[ "$digest" -eq 1 ]` from check_g2's predicate leaves the selftest **fully green**:
  `selftest cases=8 failures=0`, exit=0, judge accepted. The digest-mismatch fixture stays
  red only via the sibling export-copy limb, so no fixture reacts. The one limb that binds
  a receipt to the bytes that produced it is guarded by nothing but itself.
- **F2 · G1 · fence-type: the tilde-opener limb is unpinned (M-G1-01).** Deleting tilde
  recognition leaves the selftest green — the tilde fixture still reds, but through the
  accidental ``` line opening a backtick fence, so its needle (`readme-fence=open`) is
  satisfied for the wrong reason and the fixture pins nothing about tildes. A *properly
  closed* tilde fence becomes invisible: a `Correction (round 39)` inside it counts as
  outside, so the inside-fence defect class the fixture was built to close reopens through
  tilde fences. (The closer-side twin M-G1-13 is killed — the limb is half-pinned.)
- **F3 · G1 · whole-tail: the tail-sha equality limb is unpinned (M-G1-02).** Dropping
  `[ "$got" = "$sha" ]` leaves the selftest green: the short fixture reds via the numstat
  count limb and never exercises a wrong-sha-right-count declaration. A declaration
  binding the wrong bytes (right line count) validates — the declared digest stops
  meaning anything. (The count-side twin M-G1-03 is killed.)
- **F4 · G1 · the PROVINCE side of three limbs is unpinned (M-G1-06d compound, M-G1-07a,
  M-G1-16).** Every G1 fixture reds via README (tilde, corin) or via both doors
  (short, escape). No fixture exercises a fenced correction in PROVINCE.md (compound
  mutant with both province routes dropped survives), a province tail-position failure,
  or an open province fence. The readme twins are killed (M-G1-06c, M-G1-17) — coverage
  is asymmetric per door.
- **F5 · G2 · graded-parser fields partially unpinned (M-G2-01, M-G2-02, M-G2-03,
  M-G2-19).** The grading rule demands BOTH `positive=pass` AND `verdict=pass`; dropping
  the positive-field requirement survives (the verdict-fail fixture still reds via
  `verdict=fail`). A case line `positive=fail … verdict=pass` — a check whose positive
  failed while its fixtures rejected — would count as graded. Likewise ids outside
  G1..G8 count (G0/G9), duplicate graded ids pass, and a ninth ungraded case line passes.
- **F6 · G2 · receipt-shape conjuncts unpinned (M-G2-04, M-G2-06, M-G2-12, M-G2-13,
  M-G2-14).** A receipt containing a `closed=0` line, or lacking the
  `selftest cases=8 failures=0` summary line, or lacking the `closed=8/8 exit=0` line,
  or carrying nine G-lines with eight distinct ids, or eight G-lines with a duplicate id
  — each passes G2 under its single mutation. No fixture supplies any of these shapes.
- **F7 · G2 · cross-reference phrases unpinned (M-G2-08, M-G2-09).** The SCORECARD and
  SHONEN `judged head: export-ref of …` phrases go unchecked; no fixture removes them.
- **F8 · G2 · parser strictness (M-G2-24, M-G2-26).** A 7-hex `export-ref` is accepted
  where the frozen predicate says 40 hex; a receipt line `selftest cases=8 failures=1`
  satisfies the summary limb (the failures count is unchecked).
- **F9 · G3 · the fail-open diff read reopens the round-38 G3-M4 class (M-G3-02).**
  Dropping `[ "$diffread" = ok ]` from G3's predicate: a failed diff read leaves
  `added=''`, no quotes are scanned, `uncovered=0`, G3 greens — the exact survivor class
  round-38 recorded (`wave1/MutG3G4.md` G3-M4) that round-39's design claims to close.
  Also unpinned: the `report-only` exemption (a labeled quote needs no transcript,
  M-G3-03) and 7-hex quoted refs invisible to the extractor (M-G3-05).
- **F10 · G4 · identity-field-present and at-least-one-dispatch unpinned (M-G4-02,
  M-G4-05).** Results entries lacking every identity field pass when the count matches;
  and a round-39 wave dir with **zero** dispatch files greens (read=ok, 0==0==0) — the
  E5 §3 semantics ("a round with zero dispatch files is RED") rests on one unpinned
  conjunct. (distinct-identity, results==tasks, wave-match, seats-ok and the precedence
  are all killed — the named distinct-id class is pinned.)
- **F11 · G6 · a non-directory leftover reads as absent (M-G6-05).** Deleting the
  `[ -e ] || [ -L ]` branch of g6_root_state: a leftover **file or symlink** at
  `kasegi-r37`/`kasegi-r38` reports `absent` and quiescence passes. Every fixture builds
  directories (mkdir), so the branch is unpinned; the kill-rule's "leftover scratch
  entry" (any entry counts) is enforced only for directory-shaped leftovers.
- **F12 · G7 · ledger-row limbs unpinned (M-G7-01, M-G7-02, M-G7-06).** Fewer than three
  proposal rows green; proposal 1 absent green; and a first cell like `1x` counts as
  proposal 1 — the round-38 hole G7-H1 is reopenable with a one-character regex
  loosening. (proposal-3, correction, section-order and the heading constant are killed.)
- **F13 · G8 · the pinned-digest comparison is unpinned (M-G8-01).** Forcing `pinned=1`
  leaves the selftest green: the fixtures only mutate the *export copy* of r37 — the
  pinfile always comes from `git show PIN_REF` in fixture-land. A doctored pinfile whose
  bytes differ from the pin but still run green passes; the digest limb is the only guard
  that the *executed* r37 bytes are the pinned bytes, and nothing pins it. (The export
  copy limb, both constants and the run limbs are killed.)

Dead/redundant conjuncts (21, unpinned but harmless — each implied by a sibling conjunct,
so dropping it changes no outcome): G1 pure-append, declared>=2, pin/rin/cor_decl
predicate conjuncts, diff-read, paths, readme no-decl branch; G2 receipt-exists,
diff-read, total, xref-present, graded==8; G4 zero-task, pairs, read, tasks>=1; G5
correction>=1 (implied by correction-labeled>=1); G6 read; G8 closed=14/14-line and
r37-exit (a redundant pair). Plus: M-G1-10 (failed numstat still reds via
valid<declared; payload misreports diff-read=ok), M-G2-25 (short digest line counted but
equality limbs still gate), M-G6-07 (work=unknown fail-open is unreachable while
make_work always sets WORK), and M-G1-06/M-G1-06a (each single inside-fence route is
masked by the other; the compound readme mutant is killed, the compound province mutant
survives — see F4).

## 6. What I did NOT do (scope)

No writes outside the three allowed paths plus scratch; no edits to any lane file; no
mutating git anywhere; no pacman (bash/git/python3 only, nothing installed); no messaging
of agent://all; no own swarm. The frozen claims files were read, not edited.

## 7. Restoration evidence

- The lane's suite bytes are untouched:
  `sha256sum corpus/instruments/r39-closure.sh` →
  `2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b` (== the pre-campaign
  digest and the receipt's `suite-sha256`).
- Every mutant lived and died under `/fast/scratch/hyaku/kasegi-r39/MutSuiteLimbs/`
  (mutants/, runs/, norm/, work-*), removed with the scratch dir before this yield.
- `git status` on the lane shows no modification to any tracked file from this seat (the
  untracked wave-2 entries present are the dispatcher's and siblings').

## 8. Handoff to the L1

- The frozen C1 predicate stands (baseline §3); no kill-rule branch fires.
- The 34 live holes above are the actionable suite defects: the highest-value fixes are
  F1 (digest conjunct), F2/F3 (fence-type opener + tail-sha), F9 (G3 fail-open — a routed
  r38 class reopened), F11 (non-directory leftover), F13 (pinned-digest), each of which
  needs one new fixture (a wrong-sha declaration; a proper tilde fence; a province-side
  corin/fence fixture; a labeled-but-untranscribed quote; a 7-hex quoted ref; a file-shaped
  leftover; a doctored pinfile) — the fixture patterns already exist in the suite's own
  fixture builders.
