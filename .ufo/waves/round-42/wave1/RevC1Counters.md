# RevC1Counters — C1 counting commands at base (receipt-only)

Seat: RevC1Counters. Lane /home/vgpnk/Projects/shokunin/kasegi-shokunin, lane HEAD 0566bd66e93d429b2df8b6751cf10cbdc391e79b (frozen claims commit; base 5053a7f46de35784cff4b56756906e9014a38276 is its parent-chain ancestor 5053a7f). Scratch /fast/scratch/hyaku/kasegi-r42/RevC1Counters (TMPDIR bound; removed before yield). Disk guard green (/fast/scratch/hyaku 27%). No lane/fleet writes other than this receipt. No tools installed.
Host clock at first command: `date -u` = 2026-10-28T11:02:01Z (claims.json frozen_at_utc = 2026-10-28T12:05:00Z, i.e. the host clock reads earlier than the freeze stamp — noted for the L1; it matters for the run-utc <= commit-instant limb of J8).

## 1. The five frozen C1 counting commands, run with the suite absent

The r42 suite exists in neither the lane HEAD, the base tree, nor the round-41 judged-head tree:

```
$ git -C <lane> ls-tree -r --name-only 5053a7f... | grep -c r42-closure          -> 0
$ git -C <lane> cat-file -e 5053a7f...:corpus/instruments/r42-closure.sh
fatal: path 'corpus/instruments/r42-closure.sh' does not exist in '5053a7f46de35784cff4b56756906e9014a38276'   (exit 128)
$ git -C <lane> cat-file -e 1f7464612ac4c44e39886b82e812610d3c039b13:corpus/instruments/r42-closure.sh
fatal: path 'corpus/instruments/r42-closure.sh' does not exist in '1f7464612ac4c44e39886b82e812610d3c039b13'   (exit 128)
```

Frozen counting commands 1-5 (from claims.json `claims[0].counting_commands`), run from the lane root:

| # | frozen command (abridged) | frozen after-value | observed at base |
|---|---|---|---|
| 1 | `bash corpus/instruments/r42-closure.sh --export-ref <Y> ...` | `closed=13/13 exit=0` | Y does not exist; suite absent -> `bash: corpus/instruments/r42-closure.sh: No such file or directory`, exit=127 (run with `--export-ref 5053a7f... --work $S/w0 --scratch-root $S`) |
| 2 | `bash corpus/instruments/r42-closure.sh --selftest --export-ref <Y> ...` | `selftest cases=13 failures=0` + 13 graded lines | exit=127, same "No such file" message, zero graded lines |
| 3 | `... --export-ref 5053a7f... --work $S/w1 --scratch-root $S` | `closed<13/13 exit=1` | exit=127 (suite absent; no `closed=` line is printed, so it cannot print 13/13) |
| 4 | `... --export-ref 1f74646... --work $S/w2 --scratch-root $S` | `closed<13/13 exit=1` | exit=127 (suite absent; same) |
| 5 | `bash corpus/instruments/r42-closure.sh` (plain) | exit 2 | exit=127 (not 2): plain-run refusal is not reachable with the suite absent |

Verbatim transcript:
```
## 1 r42 suite absent at lane HEAD (plain run)
bash: corpus/instruments/r42-closure.sh: No such file or directory
exit=127
## 4 --export-ref base on absent suite
bash: corpus/instruments/r42-closure.sh: No such file or directory
exit=127
## 5 selftest on absent suite
bash: corpus/instruments/r42-closure.sh: No such file or directory
exit=127
```
Do-nothing is therefore red on every C1 counting command: no `closed=13/13 exit=0`, no `selftest cases=13 failures=0`, and the plain-run exit-2 limb is unobservable (127). Matches do-nothing.txt line "observed suite exit = 127".

A structural note for the suite author (not a defect at base): command 3/4 literal form runs the r42 suite FROM the lane tree against the exported base/r41 ref. The r42 suite exists only in the new commit (J/Y), so commands 3-4 must be run with the suite from Y (`bash <Y-export>/corpus/instruments/r42-closure.sh --export-ref <base|r41>`), or from the lane HEAD after the J commit; with the suite read from the target ref it would be absent (exit 127, not exit 1) in the base and r41 exports. The J9 check's "base and round-41 exports print closed<13/13 exit=1" must therefore run the suite bytes from the verification ref over the base/r41 export, as r41 I10 did (r41 I10 payload: `suite=1,base=3/12,base-exit=1,...`).

## 2. r41 suite (93905 bytes, sha256 3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd; identical bytes at base and lane HEAD) — plain run and exports

Plain run: `bash corpus/instruments/r41-closure.sh` -> `r41-closure: refusing to run against the live worktree: this suite is export-mode only.` / `r41-closure: pass --export-ref <hash> (see --help) or --selftest.` exit=2.

### 2a. `r41-closure.sh --export-ref 5053a7f... --work $S/wb --scratch-root $S` (real 5m31s, exit=1)

```
all-gates v1
export-ref=1f7464612ac4c44e39886b82e812610d3c039b13
suite-sha256=3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd
time-basis=ref-commit
run-utc=2026-10-27T12:16:34Z
I1 payload=records=3,lines=14,graded=3,evidence=3/3,missing=0 closed=1
I2 payload=receipt=1,...,payload-match=9/11,ancestor=1,diff-clean=0,...,i2-line=0 closed=0
I3 payload=exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0 closed=1
I4 payload=records=3,fenced=0,eof=closed,erratum=1,gate=1,tally=1,census=1 closed=1
I5 payload=declared=153,valid=149,tail=149,malformed=0,pure=1,paths=1,canon=1,nul=0,diff-read=ok,file=present closed=0
I6 payload=strays=6,read=fail,scanned=6 closed=0
I7 payload=mentions=1,rows=1,well-formed=1,table=1,cells=10,broken=0,r40-table=1 closed=1
I8 payload=control=missed/missed,payload-contradicting=rejected,future-dated=rejected,foreign-ref=rejected,nonexistent-ref=rejected,summary-only=rejected,tampered-payload-line=rejected closed=1
I9 payload=cases=12,isolated=12 closed=1
I10 payload=suite=1,base=3/12,base-exit=1,r40=3/12,r40-exit=1,probe=3/3 closed=1
I11 payload=escapes=8,red=8,F1=red F2=red F3=red F4=red F5=red F6=red F7=red F8=red,pending=0,read=ok closed=1
I12 payload=declared=153,valid=149,tail=149,pure=1,skill-del=0,province-del=0,density=1,deleted=0,census=1,ref-not-found=1,markers=0,neg-red=1 closed=0
selftest case=I1 mutants=1/2 positive=fail payload-match=0 verdict=fail
selftest case=I2 mutants=5/5 positive=fail payload-match=0 verdict=fail
selftest case=I3 mutants=0/1 positive=fail payload-match=0 verdict=fail
selftest case=I4 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest case=I5 mutants=1/1 positive=fail payload-match=0 verdict=fail
selftest case=I6 mutants=5/5 positive=fail payload-match=0 verdict=fail
selftest case=I7 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest case=I8 mutants=1/1 positive=pass payload-match=1 verdict=pass
selftest case=I9 mutants=1/1 positive=pass payload-match=1 verdict=pass
selftest case=I10 mutants=1/1 positive=pass payload-match=1 verdict=pass
selftest case=I11 mutants=1/1 positive=pass payload-match=1 verdict=pass
selftest case=I12 mutants=3/3 positive=fail payload-match=0 verdict=fail
selftest cases=12 failures=8
closed=8/12 exit=1
```
(I2/I8 payload fields abridged with `...` only where marked; every other line is verbatim.)

Known defeats at base, confirmed alive:
- I1 (F-EVID): `selftest case=I1 mutants=1/2 positive=fail verdict=fail` — one of two mutants survives (the union-evidence mutation) although the live I1 line prints `closed=1` (`evidence=3/3`): the check is green on the live tree while its own defeat artifact is accepted. This is exactly the "closed=1 on live data, mutant survives" shape the r42 REPLAY limb must reject.
- I3 (F-TOKEN): `selftest case=I3 mutants=0/1 ... verdict=fail` — the single mangled-token mutant (`closed=10/100` class) survives; live `I3 ... mangled=0 closed=1`.
- Further reds at base: I2 closed=0 (`payload-match=9/11`, `diff-clean=0`), I5 closed=0 (`declared=153,valid=149`), I6 closed=0 (`strays=6,read=fail`), I12 closed=0 (`valid=149`). Selftest reds: I1, I2, I3, I5, I6, I12.
- closed set at base = I1,I3,I4,I7,I8,I9,I10,I11 (8); open = I2,I5,I6,I12 (4). Matches `c1-controls/do-nothing.txt` (`selftest cases=12 failures=8`, `closed=8/12 exit=1`).

### 2b. `r41-closure.sh --export-ref 1f7464612ac4c44e39886b82e812610d3c039b13 --work $S/w2 --scratch-root $S` (real 6m04s, exit=1)

Check lines: I1 closed=1, I2 `receipt=0,...,payload-match=0/11,... closed=0`, I3 closed=1, I4 closed=1, I5 `declared=153,valid=153,tail=153 closed=1`, I6 `strays=6,read=fail,scanned=6 closed=0`, I7 closed=1, I8 closed=1, I9 closed=1, I10 closed=1, I11 closed=1, I12 `declared=153,valid=153 ... closed=1`. Selftest: I1 `mutants=1/2 positive=fail`, I2 `mutants=5/5 positive=fail`, I3 `mutants=0/1 positive=fail`, I6 `mutants=5/5 positive=fail`; I4,I5,I7-I12 pass. Tail verbatim:
```
selftest cases=12 failures=6
closed=10/12 exit=1
```
Same I1/I3 defects alive at the round-41 judged head (the r41 suite never closed them).

### 2c. unresolvable ref: `r41-closure.sh --export-ref deadbeef...(40) --work $S/wn --scratch-root $S` -> exit=1

```
suite-ref-status=ref-not-found
all-gates v1
tr: when not truncating set1, string2 must be non-empty
export-ref=
suite-sha256=3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd
...
I1 payload=ref-not-found,ref=deadbeef... closed=0   (I1..I12 all the same shape)
selftest cases=0 failures=0
closed=0/12 exit=1
```
The distinct `suite-ref-status=ref-not-found` red exists, but line `export-ref=` comes out EMPTY with a `tr:` stderr error: `tr -c '0-9a-f' '' ` in `print_ref_not_found` (r41-closure.sh line 381) is invalid GNU tr (second set empty). Observed defect in the r41 ref-not-found path; r42's J9 should carry a ref-not-found line that echoes the (sanitised) ref and emits no stderr noise. Not a kill-family item (not in F-EVID..F-FLIP) — route as low-severity.

## 3. claims.json `before` text vs observed — MISMATCH

claims.json C1 `before[0]` states: "the r41 suite at base prints closed=10/12 exit=1 with the I1 evidence-not-named and I3 mangled-token defeats alive".

Observed:
- r41 suite over the BASE export prints `closed=8/12 exit=1` (selftest `cases=12 failures=8`). This is also what c1-controls/do-nothing.txt records ("selftest cases=12 failures=8 / closed=8/12 exit=1").
- `closed=10/12 exit=1` is what the r41 suite prints over the round-41 JUDGED HEAD (1f74646...), selftest `failures=6`.
- Exit 127 for the r42 suite and the I1/I3 defeats alive: confirmed as stated.

So the claim text attributes the head's 10/12 to the base. The claims.json `before` should read "closed=8/12 at base (10/12 at the round-41 judged head)". claims.json is frozen (not edited by this seat); the discrepancy is a before-text inaccuracy only — the after-state predicate and kill rule are unaffected (both reds are < 13/13 and exit=1), and the do-nothing control file itself is correct. Recommend the L1 record this as an erratum in claims.json `errata` (currently `[]`) or a Correction line before the Y receipt.

## 4. Additional observations for the J-suite authors

1. Both r41 runs print I6 `strays=6,read=fail`: host-global scan state. The strays include `/tmp/kasegi_r41_outside_probe` and `/tmp/closure-kasegi-r41.json` (outside-configured-root, case/separator-insensitive family matches) — i.e. J5/J13 must be evaluated against the suite's own `--scratch-root`, as the frozen predicate says; a host-global scan stays red regardless of ref (evidence: base and head both red on I6, independent of tree content). I did not touch or remove those strays (not mine).
2. The r41 run header prints `export-ref=` from the receipt's named ref (`receipt_ref`) rather than the ref exported: the run over base printed `export-ref=1f74646...`. J8's transcript compare should bind the header to the ref actually exported.
3. Cost: r41 export run = 5.5-6 min wall (17-30 min user CPU). Counting commands 1-4 for r42 will each cost similar order; the C1 runbook should budget ~6 min per export run.
4. Lane git status during this seat: only untracked round-42 wave files (other seats' receipts and the two `kasegi-r42-build.ready*` markers); no tracked change. J13's quiescence limb should classify untracked `.ufo/waves/round-42/**` files at Y accordingly.

## 5. Scratch/cleanup
Scratch dir /fast/scratch/hyaku/kasegi-r42/RevC1Counters removed before yield. No tool installs, no pacman, no mutating git/jj.
