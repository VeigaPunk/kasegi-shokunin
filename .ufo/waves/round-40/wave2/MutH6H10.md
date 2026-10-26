# MutH6H10 — round-40 falsify wave 2 — mutation-test of suite limbs H6–H10

Seat: MutH6H10 (mutation-tester, leaf member). Attacked item: the committed
instrument `corpus/instruments/r40-closure.sh` (suite sha256
`bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e`, byte-identical
at lane HEAD `3074c7679d6f527ec3930d7748ccce1dbae4a58a`, at the wave-1 export
copy, and in every run below) — specifically whether the selftest fixture suite
can kill behavior-preserving-in-intent mutations of checks H6–H10, and whether
the frozen claims' selftest window is executable at the lane tip.

Method (same for every patch): copy the pristine suite into scratch, apply one
minimal patch to the smallest behavior-bearing point, run the bounded
behavioral detector on pristine, mutated, and restored bytes, record
killed/survivor per patch, and prove every survivor with a targeted behavioral
probe. Restored bytes re-verified by sha256 after every pass.

## Detector

`bash <suite> --selftest --export-ref <Y'> --lane <clone> --work <scratch>`
— the graded selftest (ten `selftest case=H<n> … verdict=` lines plus the
`selftest judge=` forgery rejections), exit 0 only at `cases=10 failures=0`.

Green window: no lane commit contains the receipt
(`git log --all -- .ufo/waves/round-40/final-gates/all-gates.txt` is empty; the
receipt is untracked in the lane worktree), so the selftest's H7 positive limb
(receipt must be present inside the export) cannot run against any lane commit.
The window was built as a scratch fixture clone: `fixY.MlRaR9ca`, cloned from
the lane at J=`3074c7679d6f527ec3930d7748ccce1dbae4a58a`, toplevel asserted,
receipt bytes copied unmodified, committed with fixture identity
`r40-mut-h6h10@local` → Y'=`8a2ab4ff0513e3a85a65c30eacdf877ed4ca6f60`;
`git diff --name-only J Y'` = the receipt path only.

## Baseline (pristine bytes)

1. Full run at the lane tip:
   `bash pristine.sh --export-ref 3074c7679d6f527ec3930d7748ccce1dbae4a58a --work $S/wk-base --receipt-out $S/receipt-repro.txt`
   → `closed=10/10 exit=0` rc=0, and the written receipt is **byte-identical**
   (`cmp` clean) to the lane's
   `.ufo/waves/round-40/final-gates/all-gates.txt`
   (sha256 `7b8cda36c793c5855fa6ffcb78d241fca47f0d3679b2d7c38f7a959042463484`).
   Reproduced — the C1 full-run counting command holds at the lane tip.
2. Selftest at the lane tip (`--export-ref 3074c7679d6f527ec3930d7748ccce1dbae4a58a`):
   **RED** — `selftest case=H7 positive=fail mutants=6/6 verdict=fail`,
   `selftest cases=10 failures=1`, rc=1. Cause: the export of the lane tip does
   not contain the uncommitted receipt, so H7's positive limb prints
   `receipt=0`. See finding F1.
3. Selftest at fixture-Y (Y'=`8a2ab4ff…`): **GREEN** —
   `selftest cases=10 failures=0` rc=0, all ten cases
   `positive=pass verdict=pass`, all six `selftest judge=` lines correct
   (own-report accepted, five forgeries rejected). This is the baseline every
   mutant below is judged against.

## Finding F1 (defect, verifiability): the claims' selftest counting command is not executable at the lane tip, and the green selftest was never measured in the lane

- Frozen claim C1 counting command #2 is
  `bash corpus/instruments/r40-closure.sh --selftest --export-ref <Y> -> selftest cases=10 failures=0 exit=0`.
  At the frozen state Y is not a commit: the receipt is untracked
  (`git status --porcelain` lists `?? .ufo/waves/round-40/final-gates/`), no
  commit in `--all` contains it, so `--export-ref Y` cannot resolve (exit 2),
  and `--export-ref HEAD` reds H7-positive as shown in baseline run 2
  (`cases=10 failures=1`). The command only executes green against a
  fixture-Y clone (baseline run 3) — a repo state the lane does not contain.
- Wave 1's own receipt (`wave1/ExecSuiteSelftestRun.md`) records the selftest
  at the freeze commit 5e985b7 as `selftest cases=10 failures=9` (rc=1) and
  states the `failures=0` predicate "is asserted at Y" — i.e. asserted, never
  measured. Confirmed by this seat: no green selftest measurement exists
  anywhere in wave-1 artifacts; the first green measurement is this seat's
  fixture-Y run.
- Scope note: the full-run counting command (#1) IS reproduced at the lane tip
  (baseline run 1, byte-identical receipt). The defect is specific to the
  selftest command's Y referent.

## Patch list and verdicts

Pristine file: 1734 lines; line numbers refer to it. `S` =
`/fast/scratch/hyaku/kasegi-r40/MutH6H10` (removed before yield). Every mutant
selftest was run as
`bash $S/mut-<id>.sh --selftest --export-ref 8a2ab4ff0513e3a85a65c30eacdf877ed4ca6f60 --lane $S/fixY.MlRaR9ca --work $S/wk-st-<id>`.

Byte-identity collateral (applies to every mutant, explained once): running
mutated bytes makes H1's digest limb compare the export's pristine copy against
the executing mutant bytes → `digest=0` → H1 positive red → the payload table
carries the changed H1 payload → H5 control=7/8 and H7 payload-match=7 → H5/H7
positives red. The inert control below proves this cascade fires for ANY byte
change and is therefore not evidence of semantic detection. Verdicts grade the
TARGET case's fixture limbs (`mutants=<ok>/<n>`), not the collateral.

| id | patch (before → after) | mutated sha256 | selftest target case | probe | verdict |
|---|---|---|---|---|---|
| M-H6a | L761 `local root=$SCRATCH_ROOT` → `local root=$WORK` (scan the wrong root) | `793198e0ddadf4e36c0589fc36d20ccab0b21406f5a70f1483811fd63f2bb6e5` | `case=H6 positive=pass mutants=0/4 verdict=fail` — all four limbs flipped: `empty-sibling-family-entry`, `r39-sibling-family`, `r40-sibling-family`, `unreadable-scratch-root` all `rejected=0 rc=0 payload=strays=0,read=ok` | selftest fixtures are the probe: defect present (stray family siblings, unreadable root), mutated check accepts | **KILLED** |
| M-H6b | L779 `kasegi-r39*\|kasegi-r40*) ;;` → `kasegi-r40*) ;;` (wrong prefix: r39 family invisible) | `97ca87b4463dfa280334ea46537d0a71c3489e05bd6216dc8c013bcf59aaba0f` | `case=H6 positive=pass mutants=2/4 verdict=fail` — `empty-sibling-family-entry` and `r39-sibling-family` flipped `rejected=0 rc=0 payload=strays=0,read=ok`; r40-sibling and unreadable-root still rejected | selftest fixtures are the probe | **KILLED** |
| M-H7a | L849 removed: `cmp -s -- "$rebuild" "$f" \|\| ok=0` (skip the re-run byte-comparison) | `c722da207693a2a37407334d901d666417e9be6dc034256050609cf7248505dc` | `case=H7 positive=fail mutants=6/6 verdict=fail` — all six mutant fixtures still `rejected=1`; the case red is pure byte-identity collateral (inert control reproduces it exactly) | reorder-receipt probe: pristine rc=1 vs mutant rc=0 on the same tampered bytes (defect D1) | **SURVIVOR — defect D1** |
| M-H8a | L886 `[ "$b" -lt 10 ]` → `[ "$b" -le 10 ]` (accept a 10/10 base as green) | `d17760b3d09dc0658d57c51a3c0ff217599b0438863a5ab246b311d435389c6f` | `case=H8 positive=pass mutants=2/2 verdict=pass` — both limbs (`base-ref-unresolvable`, `r39-ref-unresolvable`) still rejected; no fixture exercises the acceptance predicate | green-base probe: mutant byte-identical to pristine (equivalent); pristine itself accepts a leaf-capped green negative control (defect D2) | **SURVIVOR — defect D2** |
| M-H9a | L929 removed: `[ "$add" = "$lines" ] \|\| continue` (skip whole-tail added-line equality) | `0dbe96621a6ab61d9329d02cc032b45794dc4fd04b795218b13559a8b9689302` | `case=H9 positive=pass mutants=4/5 verdict=fail` — `declared-short-of-added` flipped: `rejected=0 rc=0 payload=declared=2,valid=2,tail=2,pure=1,paths=1,diff-read=ok` (a declaration one line short of the added block accepted) | selftest fixture is the probe | **KILLED** |
| M-H10a | L973 `&& [ "$dens" -eq 1 ] && [ "$deleted" -eq 0 ] && exit 0` → `&& [ "$dens" -eq 1 ] && exit 0` (skip tracked-path deletion guard) | `bcc237dda8378d00985ce22a18888f4e0536797864625e546b6514064c7b39bf` | `case=H10 positive=pass mutants=2/3 verdict=fail` — `tracked-path-deleted` flipped: `rejected=0 rc=0 payload=skill-del=0,province-del=0,density=1,deleted=1,diff-read=ok` | selftest fixture is the probe | **KILLED** |
| M-H10b | L972–973 `[ "$diffread" = ok ] && [ "$skdel" -eq 0 ] && [ "$pvdel" -eq 0 ] \` + `&& [ "$dens" -eq 1 ] && [ "$deleted" -eq 0 ] && exit 0` → `[ "$diffread" = ok ] && [ "$dens" -eq 1 ] && [ "$deleted" -eq 0 ] && exit 0` (skip append-only guard) | `2b39280daa3d55146a496e0d31923cc75e391c2190cd3629aa0c98fc0d654ce8` | `case=H10 positive=pass mutants=2/3 verdict=fail` — `skill-line-deleted` flipped: `rejected=0 rc=0 payload=skill-del=1,province-del=0,density=1,deleted=0,diff-read=ok` | selftest fixture is the probe | **KILLED** |
| M-inert (control, not a seat patch) | appended L1735 `# inert byte-mutation control (comment only)` | `5d6a7e88f380af0abe3ba5fd8c11a3f13e776b23a736ffe092766a6d70bcbe7b` | `cases=10 failures=3` — H1+H5+H7 positives red, H6 4/4, H8 2/2, H9 5/5, H10 3/3 all green | proves the H1→H5→H7 positive cascade is byte-identity, not semantics | control |

Score: 5 killed (M-H6a, M-H6b, M-H9a, M-H10a, M-H10b), 2 survivors (M-H7a,
M-H8a), 1 inert control. Per the seat contract, any survivor is a defect.

## Defect D1 (H7 survivor): no selftest limb guards the re-run byte-comparison; a reordered receipt is accepted once `cmp` is removed

- The selftest's six H7 fixtures (`absent`, `future`, `ancestor`, `digest`,
  `extraline`, `h7line`) are each caught by a shape/payload clause that is
  independent of `cmp`; with `cmp` removed all six are still rejected
  (`mutants=6/6`), so no fixture would notice the clause's absence.
- Behavioral probe (clause-isolation driver `probe-h7.sh`: source the suite,
  `prepare_export` Y', inject the pristine run's payload table so
  `payload-match=9` regardless of executing bytes, run `check_h7` against the
  tampered fixture):
  - fixture `MutH6H10.h7-reorder-receipt.txt` (sha256
    `0951033b91d4461d8e3a2021584f9582ec0d688d2fcf25ffc8f58ef0b0a9e1f6`): the
    real receipt bytes with the H2 and H3 payload lines swapped — every
    computed field stays green (sentinel, ref, digest, time-basis, run-utc,
    not-future, header-lines=5, run-lines=10, body-lines=11, closed-0=0,
    closed-line=1, ancestor=1, diff-clean=1, payload-match=9, h7-line=1);
    only byte order differs from the canonical rebuild.
  - pristine: `H7PROBE suite=pristine.sh rc=1 payload=sentinel=1,…,payload-match=9,h7-line=1`
    — rejected, with an all-green payload string, proving `cmp` is the ONLY
    clause rejecting this tamper class.
  - mutant: `H7PROBE suite=mut-H7a.sh rc=0 payload=sentinel=1,…,payload-match=9,h7-line=1`
    — **accepted**. A check passing while its defect (tampered transcript
    bytes) is present.
- Consequence: the "byte identity with the re-run transcript" property that the
  suite's own header advertises ("requires `cmp` equality with the committed
  receipt") is enforced by exactly one unguarded clause; a future edit that
  drops it passes the entire selftest (modulo the byte-identity collateral that
  fires for any byte change). A committed fixture showing a check passing while
  its defect is present is a C1 kill-rule item.

## Defect D2 (H8 survivor): the negative-control acceptance predicate is unkillable, and pristine H8 already accepts a leaf-capped green base

- Patch M-H8a (`-lt 10` → `-le 10` on the base comparison) is **equivalent** on
  every reachable input: `neg()` runs leaf mode (`R40_LEAF=1`), and leaf mode
  reds H8 unconditionally (`printf 'leaf=1,base=?,r39=?'; return 1`), so the
  nested tally can never reach 10 — `b ≤ 9` always, `-lt` ≡ `-le`. The selftest
  cannot kill it (its only H8 limbs point `R40_NEG_BASE`/`R40_NEG_R39` at
  unresolvable refs and assert `base-exit=2`/`r39-exit=2`, which the numeric
  guard rejects before the comparison) — `case=H8 positive=pass mutants=2/2`.
- The deeper finding, measured on **pristine** bytes:
  `R40_NEG_BASE=8a2ab4ff0513e3a85a65c30eacdf877ed4ca6f60 bash pristine.sh --export-ref 8a2ab4ff… --lane $S/fixY.MlRaR9ca --work $S/wk-h8probe-p --receipt-out $S/h8probe-p-receipt.txt`
  prints `H8 payload=base=7/10,base-exit=1,r39=2/10,r39-exit=1 closed=1` —
  H8 **accepts a green ref as its negative control**. The leaf cap floors a
  fully-green nested run at 7/10 exit=1 (H5 control=7/8, H7 payload-match=8,
  H8 leaf=1), and `[ "$b" -lt 10 ] && [ "$rc" -eq 1 ]` accepts that. The same
  command under mut-H8a prints the identical H8 line (equivalence confirmed
  empirically; that run's extra reds are its own H1 byte-identity collateral).
- Consequence: H8's discriminator is "the nested run terminates and prints a
  well-formed sub-10 tally" — it cannot distinguish a genuinely red base
  (3/10) from a base that is byte-identical to the green window (7/10). The
  claims' H8 predicate ("base … prints closed<10/10 exit=1") is satisfied
  vacuously through the leaf cap for any green base. The documented limit
  ("R40_NEG_BASE/R40_NEG_R39 exist only so the selftest can reopen the
  exit-code clause") matches this, but the acceptance floor is nowhere stated
  or fixture-guarded.

## Killed-mutant evidence (selftest detail lines, verbatim)

- M-H6a: `selftest detail=H6 mutant=empty-sibling-family-entry rejected=0 rc=0 payload=strays=0,read=ok` (and the same `rejected=0` for `r39-sibling-family`, `r40-sibling-family`, `unreadable-scratch-root`).
- M-H6b: `selftest detail=H6 mutant=empty-sibling-family-entry rejected=0 rc=0 payload=strays=0,read=ok`; `selftest detail=H6 mutant=r39-sibling-family rejected=0 rc=0 payload=strays=0,read=ok`.
- M-H9a: `selftest detail=H9 mutant=declared-short-of-added rejected=0 rc=0 payload=declared=2,valid=2,tail=2,pure=1,paths=1,diff-read=ok`.
- M-H10a: `selftest detail=H10 mutant=tracked-path-deleted rejected=0 rc=0 payload=skill-del=0,province-del=0,density=1,deleted=1,diff-read=ok`.
- M-H10b: `selftest detail=H10 mutant=skill-line-deleted rejected=0 rc=0 payload=skill-del=1,province-del=0,density=1,deleted=0,diff-read=ok`.

In every killed case the mutated check accepted a fixture whose defect was
present — i.e. the selftest fixtures do reopen the mutated clause, which is the
kill.

## Restoration evidence

- The lane's committed suite was never written to: `git cat-file -p
  HEAD:corpus/instruments/r40-closure.sh | sha256sum` =
  `bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e` before the
  first run and after the last run; the scratch pristine copy and the wave-1
  export copy hash identically. All mutations lived in scratch copies
  (`mut-*.sh`), deleted with the scratch.
- The receipt fixture shipped beside this receipt is a byte-exact copy of the
  lane receipt with exactly the H2/H3 line swap (verified by sha256 above and
  by `cmp` of all other lines).
- No mutating git/jj command was run anywhere; the only git writes are inside
  the scratch fixture clone `fixY.MlRaR9ca` (toplevel asserted before its one
  fixture commit, fixture identity `r40-mut-h6h10@local`).

## Conduct

- Writes: `wave2/MutH6H10.md` (this receipt) and
  `wave2/MutH6H10.h7-reorder-receipt.txt` (attack fixture) only; everything
  else under `$S=/fast/scratch/hyaku/kasegi-r40/MutH6H10`, removed before
  yield. No fleet-root tracked file, no PATH dir, no sibling/lane/source-tree
  write; `/home/vgpnk/Projects/shokuknow` untouched.
- Lane git use read-only (`rev-parse`, `status`, `log`, `diff`,
  `merge-base --is-ancestor`, `cat-file`, `archive` via the suite).
- Tooling: none installed or upgraded; no pacman; no network fetches.
- Scratch: `rm -rf $S` executed before yield (H6 checks it live).
