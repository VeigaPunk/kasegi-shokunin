# ExecSuiteSelftestRun — round-40 wave-1 receipt

Seat: `ExecSuiteSelftestRun` (executor, leaf). Item: copy the built suite into scratch and run
four prescribed invocations, recording every transcript verbatim.

Axes named up front: **depth:verifiability** (does `r40-closure.sh` actually execute and print
graded evidence at the frozen refs?) and **coverage** (unchanged by this seat — no registry or
knowledge bytes touched).

## Dependency and identity (measured)

ExecSuiteBuild revised its deliverable mid-seat. The superseded bytes
(`1da1d76d…`, 70922 B, 1713 lines) were re-copied and re-run against the revised bytes, which
are the only ones this receipt and deliverable bind:

```
$ ls -la .ufo/waves/round-40/wave1/ExecSuiteBuild.r40-closure.sh
-rw-r--r-- 1 vgpnk vgpnk 71895 Oct 26 18:44 ExecSuiteBuild.r40-closure.sh
$ sha256sum .ufo/waves/round-40/wave1/ExecSuiteBuild.r40-closure.sh
bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
$ wc -l → 1734 ;  bash -n → SYNTAX-OK
$ cp .ufo/.../ExecSuiteBuild.r40-closure.sh $S/corpus/instruments/r40-closure.sh
$ sha256sum $S/corpus/instruments/r40-closure.sh
bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
$ (digest re-checked after the four runs) → unchanged
```

Builder message: *"Correction to the deliverable … new sha256 `bdbd18a3…`, 1734 lines, same path …
The `1da1d76d…` file is superseded."* Two fixes in the revision: (a) `--receipt-out` writes the
run's own transcript on a red ref; (b) H4's locator clause accepts `L<NN>`/`#anchor`/`paragraph N`.

Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, HEAD `5e985b7` (claims freeze).
Refs: base `a7af2ce63bce153757d39bf66b366a96caf30c13` (a descendant of the r39 head),
r39 judged head `8371e7ac9f32cae5ed72f8c28205634603f836fa`, claims freeze
`5e985b74075dd3813a63d7750966bf8abf693465`.

Ref-tree facts before running (read-only `git cat-file`/`git show`):

| ref | r40 suite | r40 final-gates receipt | `Correction (round 40)` in SCORECARD | `M39-2` in QUALITY |
|---|---|---|---|---|
| a7af2ce (base) | ABSENT | ABSENT | 0 | 0 |
| 8371e7a (r39 head) | ABSENT | ABSENT | 0 | 0 |
| 5e985b7 (freeze) | ABSENT | ABSENT | 0 | 0 |

Every tested ref is **pre-build**: none carries the round-40 artifacts. The green window is
`Y = J + receipt only`, produced at the final-gate wave; this seat measures the honest
pre-commit baseline.

Scratch: `S=/fast/scratch/hyaku/kasegi-r40/ExecSuiteSelftestRun` (recreated for the revision,
removed before yield). `TMPDIR=$S`; `--work $S/sf`. Disk guard read green before the runs.

## Deliverable

`.ufo/waves/round-40/wave1/ExecSuiteSelftestRun.transcript.txt` — 138 lines,
sha256 `2d8c2c356bb8d0eed4acd57d8e93eec85f4104fbd682391ca340571d98219ead`.
It holds the four required transcripts verbatim (exact command, combined stdout+stderr, `exit=N`),
with a five-line header naming suite digest `bdbd18a3…` and the invocation `run-utc`.

## The four prescribed runs (results)

| # | command (as executed) | result | required? |
|---|---|---|---|
| 1 | `--selftest --export-ref 5e985b7… --work $S/sf --lane <lane>` | `selftest cases=10 failures=9`; exit **1** | recorded verbatim (no expected value in spec) |
| 2 | plain run, no args | refusal message; exit **2** | must exit 2 — **MET** |
| 3 | `--export-ref a7af2ce…` (default scratch root) | `closed=3/10 exit=1` | must print `closed<10/10 exit=1` — **MET** |
| 4 | `--export-ref 8371e7a…` (default scratch root) | `closed=2/10 exit=1` | must print `closed<10/10 exit=1` — **MET** |

Run 2 verbatim:

```
r40-closure: refusing to run against the live worktree: this suite is export-mode only.
r40-closure: pass --export-ref <hash> (see --help) or --selftest.
```

Run 1 is the **red direction by construction** at a pre-build ref (builder's own note: *"That is
the red direction and is CORRECT at the freeze … Record it verbatim; do not read it as suite
breakage"*). Case verdicts: H1,H2,H3,H4,H7,H8,H9 fail; **H5,H6,H10 pass**. `failures=9` =
7 failed case lines + H8's two mutants (`base-ref-unresolvable`, `r39-ref-unresolvable` both
`rejected=0` because the export carries no suite to nest). All 28 mutant lines that did run were
`rejected=1` naming their reopened limb:

```
selftest case=H1 positive=fail mutants=3/3 verdict=fail
selftest case=H2 positive=fail mutants=3/3 verdict=fail
selftest case=H3 positive=fail mutants=2/2 verdict=fail
selftest case=H4 positive=fail mutants=3/3 verdict=fail
selftest case=H5 positive=pass mutants=2/2 verdict=pass
selftest case=H6 positive=pass mutants=4/4 verdict=pass
selftest case=H7 positive=fail mutants=6/6 verdict=fail
selftest case=H8 positive=fail mutants=0/2 verdict=fail
selftest case=H9 positive=fail mutants=5/5 verdict=fail
selftest case=H10 positive=pass mutants=3/3 verdict=pass
selftest cases=10 failures=9
selftest judge=own-report accepted=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=forged-failed-cases rejected=1
selftest judge=forged-detail-free rejected=1
selftest judge=forged-9-cases rejected=1
selftest judge=forged-no-verdict rejected=1
```

`own-report accepted=0` is **correct fail-closed**, not a defect: `judge_selftest_report`
requires ten `verdict=pass` case lines and `selftest cases=10 failures=0`; a red run's own report
must not be accepted. On a green Y the builder measured `accepted=1`. All six forged report
shapes are rejected (`6/6`).

## H6 is live and load-bearing (two measurements, one host)

The same bytes produced two different export-mode results minutes apart, because H6 scans the
live scratch root by name family (`kasegi-r39*|kasegi-r40*`) and counts every family entry that
does not contain the run's `--work` dir. Both are honest; the second is the deliverable's.

At ~21:39Z, with `/fast/scratch/hyaku/kasegi-r40-l1` present (L1's scratch), the default-root
runs printed the one-check-lower pair:

```
H6 payload=strays=1,read=ok closed=0
closed=2/10 exit=1      # base a7af2ce
closed=1/10 exit=1      # r39 head 8371e7a
```

An isolated `--scratch-root $S/cleanroot` on the same bytes gave `H6 payload=strays=0,read=ok
closed=1`, `closed=3/10` and `closed=2/10`, both exit 1 — proving the delta was exactly the live
sibling, not a suite defect.

After L1 removed `kasegi-r40-l1`, the current live state is:

```
$ ls -ld /fast/scratch/hyaku/kasegi-*
drwxr-xr-x kasegi-r40            # contains this run's --work, so tolerated
$ ls -1 /fast/scratch/hyaku/kasegi-r40
ExecH7Determinism  ExecSuiteSelftestRun  MutKillList
```

…and the default-root runs now print `H6 payload=strays=0,read=ok closed=1`, i.e. the required
`closed=3/10` and `closed=2/10` recorded in the deliverable, matching ExecSuiteBuild's table.

Consequence for the final gate: at filing, either every `kasegi-r39*`/`kasegi-r40*` scratch entry
must be gone, or the Y run must pass an isolated `--scratch-root`. Otherwise H6 reds a valid tree.

## Why H6 shows `positive=pass` in run 1 yet is host-sensitive in export mode (grounded)

`selftest_case_H6` never scans the live root. It swaps `SCRATCH_ROOT` to controlled fixtures under
`$MUT/H6-*` (control `kasegi-r40-gold/work`; mutants `kasegi-r39`, `kasegi-r39-stray`,
`kasegi-r40-stray`, an unreadable root). That keeps the selftest host-independent; the live limb
runs only in export mode. The single stderr line from the unreadable-root mutant
(`cd: …/H6-unreadable: Permission denied`) is the intended `chmod 000` probe, not a failure — its
case line is `rejected=1 limb=read=fail`.

## Retained evidence (exact)

- Deliverable: `ExecSuiteSelftestRun.transcript.txt`, 138 lines,
  sha256 `2d8c2c356bb8d0eed4acd57d8e93eec85f4104fbd682391ca340571d98219ead`.
- Suite digest executed: `bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e`
  (byte-identical to the revised ExecSuiteBuild deliverable; re-checked after the runs).
- Run rcs: `1 2 1 1`. Required predicates: run2 exit 2 ✓; run3 `3/10 exit=1` ✓; run4 `2/10 exit=1` ✓.
- Live-state probe: `kasegi-r40-l1` absent at run time; `strays=0` for runs 3/4.

## Risks / notes for the final gate

1. **Live H6 is fail-closed on host state.** It is green now only because the one remaining family
   entry (`kasegi-r40`) contains this run's `--work`; any new sibling scratch reds it. Clean
   scratch or an isolated `--scratch-root` is required at Y.
2. **Pre-build refs cannot exercise H8's teeth.** At a7af2ce/8371e7a/5e985b7 the export carries
   no `r40-closure.sh`, so H8 prints `suite=0,base=?,r39=?` and its nested base/r39 controls do
   not run. H8's teeth are only demonstrable at J/Y; the builder's fixture-Y measurement
   (`H8 payload=base=3/10,base-exit=1,r39=2/10,r39-exit=1 closed=1`) is the evidence for that
   window, which this seat does not re-measure because Y does not exist during wave 1.
3. **Run 1 is not a green-window measurement.** `selftest cases=10 failures=9` at 5e985b7 is the
   expected pre-commit red. The frozen C1 predicate's `selftest cases=10 failures=0` is asserted
   at Y. The revision's H4 locator widening cannot change this run: the round-39 lesson Gate rows
   do not exist at 5e985b7, so H4 prints `s056=0,s058=0,s059=0`.
4. **Determinism basis.** The suite stamps `time-basis=ref-commit` and `run-utc` = the export
   ref's committer instant (base `2026-10-26T21:04:36Z`, r39 head `2026-10-26T20:55:17Z`), not
   wall clock, so re-runs are byte-identical (ExecH7Determinism's item). The transcript header's
   `run-utc` is this seat's invocation time, metadata outside the suite output.

## Conduct

- Writes: only `wave1/ExecSuiteSelftestRun.transcript.txt` and this receipt, both under the wave
  dir; everything else under `$S` (removed before yield). No fleet-root, sibling-lane or source
  tree writes.
- No mutating git/jj anywhere. Lane git use was read-only (`cat-file`, `show`, `archive` via the
  suite with `--no-optional-locks`); `--receipt-out` was never used, so nothing was written under
  the lane by the suite. The tracked-file modifications visible in `git status` (LOG.md,
  PROVINCE.md, SCORECARD.md, SHONEN.md, SKILL.md, corpus/QUALITY.md, corpus/README.md,
  corpus/SOURCES.md, corpus/instruments/knowledge-expected.txt, corpus/lessons/round-39.md) are
  other wave-1 seats' edits, untouched by this seat.
- Tooling: none installed or upgraded; no pacman. Network: none.
- Supersession: the seat's first pass ran the superseded `1da1d76d…` bytes; every artifact above
  was regenerated against `bdbd18a3…` after the builder's correction.
