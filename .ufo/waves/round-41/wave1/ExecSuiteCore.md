# ExecSuiteCore — `corpus/instruments/r41-closure.sh` (round-41 C1 suite)

Item: author the committed round-41 closure counter for claim C1 (`depth:verifiability`),
twelve checks I1-I12, export mode only, graded selftest, receipt = teed transcript of run +
selftest. Deliverable bytes (landable, byte-exact):

    .ufo/waves/round-41/wave1/ExecSuiteCore.r41-closure.sh
    2209 lines, sha256 3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd
    -> land as corpus/instruments/r41-closure.sh (chmod +x)

## Design notes (twenty lines)

1. Export mode only: `--export-ref H` extracts `git -C <lane> archive H | tar -xf - -C <work>/export`;
   a plain run refuses exit 2. `--work` must be outside the lane and is cleared before use.
2. `--lane` defaults to the repo the script lives in (resolved from `$BASH_SOURCE`, never the cwd).
3. Each check prints one `I<n> payload=<k=v,...> closed=0|1` line; the transcript ends with
   `closed=K/12 exit=0|1`; exit 0 only for K=12. Any read error fails closed (`closed=0` + a payload).
4. Receipt grammar is fixed at 31 lines: `all-gates v1`, export-ref, suite-sha256,
   `time-basis=ref-commit`, run-utc, 12 run lines, 12 graded selftest lines, selftest summary, closed.
5. `run-utc` is the committer instant of the ref the RECEIPT NAMES (J), read with
   `git log -1 --format=%ct`; `not-future` is the external anchor (`verification clock +120s`).
6. I2 rebuilds the canonical transcript from the tree facts; the cmp carves out the two
   self-referential run lines (I2's, I8's) and the I2 case's own selftest line (r40 `h7_inner`
   pattern); I2's line is rebuilt from the receipt minus itself, so the self-reference is closed.
7. If the receipt is absent from the export (the judged head J) the suite SEEDS the receipt it is
   about to write with the canonical transcript, so the first iteration is already the fixed point
   and the J run prints the same bytes the Y run prints.
8. The twelve selftest lines inside the receipt are re-EXECUTED on every run and byte-compared; the
   selftest never reads the receipt under test (scratch fixtures only), so the block is a pure
   function of the exported tree. A shape check would reopen r40 D2.
9. I3 bounds values as `[[:space:][:punct:]]`-delimited tokens (`closed=7/80` does not satisfy
   `closed=7/8`); I4 runs a CommonMark fence state machine (4-backtick/tilde fences) and reports the
   EOF fence state; fenced lines never satisfy a line-anchored limb.
10. I5/I12 read `$R41_DECLARED` (default `.ufo/waves/round-41/declared-blocks.txt`), canonicalize
    each declared path with `realpath -m` and require it under the export root, then require the
    declared tail sha256 and `git diff --numstat` (added==lines, deleted==0).
11. I6 is the live scratch scan: recursive, dot-inclusive, case/separator-insensitive (`kasegi-r41`),
    work dir and clean ancestor chain tolerated, family symlink to an ancestor is a stray, scan error
    fails closed.
12. I7 requires the registry row's FIRST cell to be the instrument basename, >=8 fields, a preceding
    table row/separator (never a blank line: the D6 break) and a contiguous table header naming `name`.
13. I8 grades six forgery variants independently (its own clause each), from synthetic receipts, never
    by a mismatch count; I9 tampers one payload line per id and requires EXACTLY that id to flag.
14. I10 runs the export's own suite over the base and the round-40 head in leaf mode (`R41_DEPTH=1`)
    and accepts only `exit=1 AND tally<12 AND I1,I2,I7 red`; the killability probe rejects a 12/12
    tally with exit 1 (the MutH6H10 M-H8a class).
15. I11 constructs the eight committed CritKillRule escape states F1-F8 and requires each red
    (`escapes=8,red=8`); F7 is the pending-marker class on `corpus/lessons/round-41.md`, F8 the
    worktree clause (skip-worktree/assume-unchanged + ignored entries).
16. I12: the negative controls red, declared blocks whole-tail, SKILL/PROVINCE append-only,
    `density.py` byte-identical to base, zero deleted tracked paths, census exit 0 over the EXPORT's
    registry, the `ref-not-found` distinctness probe, and no index markers on the lane.
17. An unresolvable `--export-ref` prints `suite-ref-status=ref-not-found`, twelve
    `payload=ref-not-found,...` lines and `closed=0/12 exit=1` — a distinct red, never a vacuous tally.
18. Environment knobs for wave-2 seats (documented in the header): `R41_DECLARED`,
    `R41_RECEIPT_TARGET`, `R41_FORGE_DISABLE`, `R41_ISOLATE_BREAK`, `R41_NEG_WEAK`,
    `R41_I11_BREAK`, `R41_DEPTH`.
19. Selftest: twelve graded cases, each with a positive limb (the export) and defeat fixtures; a case
    passes only when the positive passes AND every defeat is rejected with a payload that names the
    reopened limb AND differs from the positive payload. Six forged selftest reports are rejected.
20. Runtime ~40 s at 12/12 (I10's two nested runs dominate); the base/freeze runs are ~5 s.

## Measured evidence (this seat, this host)

Fixture used for the green window: a throwaway clone of the base under my scratch, with the round-41
content landed as the L1 will land it (the three `Correction (round 41)` blocks, the `Erratum
(round 41)` block, the SKILL.md r41 registry row + the D6 repair block, the suite, and a
declared-blocks file computed from that clone's own diff). Every commit used the fixture identity
`r41-fixture@local` after asserting `rev-parse --show-toplevel` == the clone dir.

    fixture J=df608988  J-run : closed=12/12 exit=0        (receipt produced with --receipt-out, 31 lines)
    fixture Y=e258f838  Y-run : closed=12/12 exit=0        stdout BYTE-IDENTICAL to the committed receipt
                        Y-selftest : selftest cases=12 failures=0, exit 0; own report accepted;
                                     6/6 forged reports rejected
    plain run (no flags)      : exit 2, "refusing to run against the live worktree"
    bogus ref (…dfb0000)      : suite-ref-status=ref-not-found, closed=0/12 exit=1, exit 1
    base 5b29ea1439450b712581edf5f0f0bf98dfb262ab : closed=4/12 exit=1
    round-40 judged head c7aea5ef97902f38289cbdc1cf267068876a62dd : closed=4/12 exit=1

Freeze-commit run (as the item requires; the corrections, registry row, erratum, declared blocks and
receipt do not exist there yet):

    $ bash r41-closure.sh --export-ref fbba3d96cdf8d37c1ea41304a1ba35691329684b \
        --lane <lane> --work <scratch> --scratch-root <scratch>
    I1 payload=records=3,lines=0,graded=0,evidence=0/3,missing=3 closed=0      (no correction lines)
    I2 payload=receipt=0,sentinel=0,ref=,digest=0,... closed=0                (no receipt committed)
    I3 payload=exact=2/2,substring=2/2,records=3,tally=0/3,mangled=0 closed=0  (no bounded tally)
    I4 payload=records=3,fenced=0,eof=closed,erratum=0,gate=0,tally=0,census=0 closed=0
    I5 payload=declared=0,...,diff-read=missing,file=missing closed=0          (no declared blocks)
    I7 payload=mentions=0,rows=0,well-formed=0,table=0,cells=0,broken=0,r40-table=0 closed=0
    I10 payload=suite=0,base=?,r40=?,probe=0/3 closed=0                        (suite absent from the export)
    I12 payload=...,neg-red=0 closed=0
    closed=4/12 exit=1   (green: I6, I8, I9, I11 — the tree-independent limbs)
    exit=1, wall 5.2 s

## Integration prerequisites (the L1 must land these; each one reds a named check)

1. The three correction blocks (ExecI1Blocks / ScribeCorrections) appended to SCORECARD.md, LOG.md,
   SHONEN.md — line-anchored `Correction (round 41):`, outside fences, naming `closed=10/10` as a
   bounded token, the not-verified grading, and the three evidence artifacts. -> I1, I3.
2. The `Erratum (round 41)` block appended to `corpus/lessons/round-40.md` (RevD4D5D6.lesson-erratum.txt
   already has it) — the block must name `Gate`, `census` and `25/35`. -> I4.
3. The SKILL.md registry row for `r41-closure.sh`: a table row whose FIRST cell is exactly
   `r41-closure.sh`, >=8 fields, immediately preceded by a table row or separator (no blank line), in a
   contiguous table whose header names `name`; the D6 repair block (header + separator + the r40 row)
   is reported as `r40-table=1` but not required. -> I7.
4. `.ufo/waves/round-41/declared-blocks.txt`: `<path> <added-lines> <sha256 of the last N lines>` for
   every appended block, where `git diff --numstat 5b29ea14 <J> -- <path>` must give added==N and
   deleted==0. Nothing in the wave generates this file; without it I5 and I12 fail closed
   (`declared=0,...,file=missing`). Recipe: after the content is committed as J, for each appended
   path run `git -C <lane> diff --numstat 5b29ea14 J -- <path>` and
   `tail -n <added> <path> | sha256sum`, then commit the file inside J.
5. Produce the receipt AT the judged head J and commit it as Y = J + receipt alone:
   `bash corpus/instruments/r41-closure.sh --export-ref <J> --lane <lane> --scratch-root <root> \
        --receipt-out .ufo/waves/round-41/final-gates/all-gates.txt`
   The written file is byte-identical to the run's stdout (and to `... | tee <path>`). It must read
   `closed=12/12 exit=0`; then `git commit` exactly those bytes and verify
   `git diff --name-only J Y` = that one path. -> I2.
6. I6 at filing: the `kasegi-r41` family must be gone from the scratch root — remove
   `/fast/scratch/hyaku/kasegi-r41` after every seat has left, or keep the run's `--work` inside it
   in a clean chain (each level holds exactly the next component) with nothing else inside.

## Corrections applied from the L1's mid-wave note (`.ufo/waves/round-41/wave1/CORRECTIONS-L1.md`)

1. `BASE_REF` is the 40-char `5b29ea1439450b712581edf5f0f0bf98dfb262ab` (the dispatched 38-char
   literal resolves to no git object). My base/selftest/I10 controls all use the 40-char hash.
2. I11 covers the EIGHT committed `### F` states (F1-F8), not seven; the payload reads
   `escapes=8,red=8,F1=red ... F8=red` and each state is constructed separately (no F1+F2 merge).
   The frozen predicate's "seven" wording is superseded by the claims errata block; recorded here so
   wave 2 does not re-flag it.
3. An unresolvable `--export-ref` is a distinct red (`suite-ref-status=ref-not-found` +
   `payload=ref-not-found,...`), never a vacuous tally; I12 carries the probe that asserts it.

## Design decisions a wave-2 attacker should read (not defects, chosen and documented)

- I2's cmp carves out three lines (I2's run line, I8's run line, the I2 case's selftest line): a
  literal whole-file fixed point does not exist otherwise (CritI2Receipt's attack), and each carved
  line is graded by its own fields (`i2-line`, `i8-match`, the shape's `selftest-verdicts=12`).
- `run-utc` binds to the receipt's NAMED ref, not to `--export-ref`: binding it to Y would force the
  L1 to pin `GIT_COMMITTER_DATE`, and an honest Y would then fail I2.
- I8 builds its variants from a SYNTHETIC receipt (built from the tree's payloads), so I8's payload is
  a function of the tree alone and the receipt's I8 line is never an input to its own grading; the
  committed receipt's forgery is caught by I2's byte comparison.
- The selftest's I2 positive limb uses a synthetic fixture (same builder as the seed), so the graded
  selftest block stays independent of the receipt under test.
- I10's nested runs are leaf-capped (`R41_DEPTH=1`), so the nested tally is red by construction; the
  discriminator is therefore the tree-dependent triple (I1, I2, I7 red in the nested run), and the
  probe rejects a 12/12-with-exit-1 tally. That is the killable acceptance predicate MutH6H10 D2 asked for.
- I5/I12 fail closed on a missing declared-blocks file (a validator that validates nothing is the
  r40 vacuity class). The L1's prerequisite list above is the fix.

## Risks / limits

- I6 is LIVE: the transcript is a function of the host scratch state. Verified green only on a clean
  root; the round container itself is a stray unless removed or unless `--work` sits inside it in a
  clean chain — by design (the kill rule counts a leftover container as a leftover).
- I4's erratum limb depends on the RevD4D5D6 erratum landing; without it I4 reds at Y.
- I12's census limb shells the fleet census against the EXPORT's `corpus/SOURCES.md`
  (`sources-census.sh validate --file <export>/corpus/SOURCES.md`, exit 0 with the standing
  W04 S028/S029 warnings). It reads the export's registry only; the script itself is a tool.
- I11's F8 probe uses a throwaway fixture repo (toplevel asserted); F7 uses explicit byte escapes, so
  a terminal/locale cannot change the marker class.

## Conduct

- Writes: this receipt + `ExecSuiteCore.r41-closure.sh` only (plus scratch under
  `/fast/scratch/hyaku/kasegi-r41/ExecSuiteCore`, removed before yield). No lane/fleet/source-tree
  file was edited; no mutating git/jj command ran in the lane or the fleet root (the only commits are
  in my own fixture clone, toplevel-asserted, fixture identity `r41-fixture@local`).
- Incident: at ~05:46 the seat `ExecI8Forge` ran `rm -rf /fast/scratch/hyaku/kasegi-r41` (its own
  message), deleting my in-flight `part1.sh`/`part2.sh`; I rebuilt both from my working notes and
  re-ran the whole matrix on the rebuilt bytes — every number above is from the rebuilt bytes whose
  sha256 is the delivered one.
- No tool installed or upgraded; no pacman; no network fetch. Disk guard green
  (`/fast/scratch/hyaku` 26%, 602G free).
- Scratch removed before yield (`rm -rf /fast/scratch/hyaku/kasegi-r41/ExecSuiteCore`), so I6 sees no
  `kasegi-r41` entry from this seat.

## Hand-off (main agent's checks, in order)

1. Land the suite bytes at `corpus/instruments/r41-closure.sh`; `bash -n` it (clean here).
2. Satisfy the six integration prerequisites, produce the receipt at J, commit it as Y.
3. `bash corpus/instruments/r41-closure.sh --export-ref <Y>` -> `closed=12/12 exit=0`, stdout equal to
   the committed receipt; `--selftest --export-ref <Y>` -> `selftest cases=12 failures=0`.
4. `--export-ref 5b29ea1439450b712581edf5f0f0bf98dfb262ab` and
   `--export-ref c7aea5ef97902f38289cbdc1cf267068876a62dd` -> `closed<12/12 exit=1`; plain run -> 2.
