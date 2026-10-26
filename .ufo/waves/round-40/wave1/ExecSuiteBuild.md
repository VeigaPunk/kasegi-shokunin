# ExecSuiteBuild — round 40, wave 1 (C1 depth:verifiability, held 4)

Item: build the committed suite `corpus/instruments/r40-closure.sh` from the frozen C1
predicate (`.ufo/waves/round-40/claims.json`, read; not edited). Deliverable:
`.ufo/waves/round-40/wave1/ExecSuiteBuild.r40-closure.sh` — **byte-exact, landable bytes
only**, land at `corpus/instruments/r40-closure.sh`.

```
$ sha256sum .ufo/waves/round-40/wave1/ExecSuiteBuild.r40-closure.sh
bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
$ wc -lc .ufo/waves/round-40/wave1/ExecSuiteBuild.r40-closure.sh
   1734  71895
$ bash -n .ufo/waves/round-40/wave1/ExecSuiteBuild.r40-closure.sh && echo SYNTAX-OK
SYNTAX-OK
```

Scratch `S=/fast/scratch/hyaku/kasegi-r40/ExecSuiteBuild` (removed at yield; all work dirs,
fixture repos and transcripts below lived under it). No lane file, no fleet-root file and no
sibling repo was written. Read-only git only (`rev-parse`, `cat-file`, `merge-base`, `diff`,
`show`, `log`, `archive`); fixture commits were made **only** inside `$S/gold` and
`$S/.../mut/hrepo` with `-c user.email=r40-fixture@local` after asserting
`git -C <fixture> rev-parse --show-toplevel` equals that fixture. Tooling: none installed,
none upgraded. Network: none used.

## 1. What the suite is

Export mode is the only run mode. `--export-ref <hash>` extracts the lane with
`git -C <lane> archive <hash> | tar -xf - -C <work>/export` (make_work guards `--work`
outside the lane, refuses `/`, re-checks the physical path for a symlink into the lane, and
clears `export/`, `mut/`, `neg-*`, `h5/` before use). Plain run → exit 2. Harness errors
(bad argument, unresolvable ref, `--work` in the lane) → exit 2. Exit 0 only at K=10.

Ten checks, one defect class each:

| id | clause (payload fields) | defect closed |
|---|---|---|
| H1 | `suite=`,`digest=`,`registry=`,`registry-in=` — the export's own `corpus/instruments/r40-closure.sh` hashes to the executing bytes and a `\|` table row naming `r40-closure.sh` exists in SKILL.md or the instruments README | suite absent / drifted / unregistered |
| H2 | `corrections=`,`named=`,`missing=`,`fences=` — fence-aware scan of SCORECARD.md, LOG.md, SHONEN.md, corpus/lessons/round-39.md; a line beginning `Correction (round 40)` OUTSIDE a fence must carry both `closed=7/8` and `failures=1` in each record; `fences=open` reds | R2 overstatement |
| H3 | `mentions=`,`rows=` — `M39-2` occurs in corpus/QUALITY.md and at least one `\|` criterion row cites it | R5 unlearned mistake |
| H4 | `s056=`,`s058=`,`s059=`,`oversize=` — one Gate block per code with a URL, an access date, a quoted span of 1..25 words and a location token (`:NN`, `line NN`, `page N`, `L<NN>`, `#anchor`, `§`, `section`, `paragraph N`); `oversize` counts rejected >25-word quotes | R6 unlocated/oversize quotes |
| H5 | `source=`,`control=n/8`,`utc=`,`forged-payload=`,`future-dated=`,`summary-only=` — builds a receipt in `$WORK/h5` and requires the *same verifier H7 uses* to accept the eight canonical non-H5/H7 lines and to reject a payload contradicting the export, a future-dated `run-utc`, and a summary-only body | G2 accepts forged payload values (`wave2/CritG2Exploit.md`), R1 |
| H6 | `strays=`,`read=` — LIVE scan of the scratch root's top level by NAME FAMILY `kasegi-r39*`/`kasegi-r40*`; every family entry that does not contain this run's `--work` realpath is a stray (empty ones included); an unreadable scan is `read=fail` | G6 fixed two names + quiescence-only (`wave2/CritC1Kill.md`), R4 |
| H7 | `sentinel=,ref=,digest=,time-basis=,run-utc=,not-future=,header-lines=,run-lines=,body-lines=,closed-0=,closed-line=,ancestor=,diff-clean=,diff-read=,payload-match=,h7-line=` — the receipt is re-derived: nine payloads compared byte-for-byte, the H7 line rebuilt from the receipt-minus-its-own-H7-line, the whole transcript rebuilt and `cmp`-ed (closed flags and tally included) | R1 + R3 + G2 payload forgery |
| H8 | `base=n/10,base-exit=`,`r39=n/10,r39-exit=` — the export's own suite copy runs (leaf mode) over `a7af2ce6…` and `8371e7ac…`; each must print `closed<10/10` with exit 1 | C1's negative clause |
| H9 | `declared=,valid=,tail=,pure=,paths=,diff-read=` — every `<path> <lines> <sha256>` in `.ufo/waves/round-40/declared-blocks.txt`: safe relative path, tail sha, `git diff --numstat <base> <ref>` added count equals `<lines>`, zero deletions | D-A whole-tail declarations |
| H10 | `skill-del=,province-del=,density=,deleted=,diff-read=` — SKILL.md/PROVINCE.md append-only, `corpus/instruments/density.py` digest equals the base digest `ee803726…`, `--diff-filter=DR` empty | no-harm guard |

No path, no flag and no clock is printed: the transcript is a function of the tree and the
ref-scoped facts only.

## 2. The receipt contract and the production procedure (for the L1)

The receipt is the transcript, 16 lines:

```
all-gates v4
export-ref=<J or the ref the tee was taken at>
suite-sha256=<export's suite digest>
time-basis=ref-commit
run-utc=<committer instant of export-ref, UTC>
H1 payload=… closed=1
… H10 payload=… closed=1
closed=10/10 exit=0
```

`run-utc` is deliberately **not** a wall clock: `time-basis=ref-commit` states that it is
`git log -1 --format=%ct <export-ref>` printed as UTC, so the transcript is reproducible and a
re-stamped or future-dated value is RED (the r39 R1/M39-1 false-provenance defect was a
wall-clock stamp that outran its own commit).

`--receipt-out PATH` writes **exactly the transcript the run prints** — red or green. On a red
ref the file carries the run's own `closed=0` lines and its own red tally; it is never a tally
the run did not print (measured in §4). Production at the judged head J, then commit exactly
those bytes as Y — and only when they read `closed=10/10`:

```
bash corpus/instruments/r40-closure.sh --export-ref <J> \
  --receipt-out .ufo/waves/round-40/final-gates/all-gates.txt
# git add that one path; commit → Y = J + receipt
bash corpus/instruments/r40-closure.sh --export-ref <Y>        # prints the same 16 lines, exit 0
```

The receipt produced at J is byte-identical to the plain run at Y, because the transcript names
J (read back from the receipt) and every payload is ref-independent.

## 3. Measured runs on a green sample (fixture lane, not the lane)

Y does not exist during a build wave, so satisfiability was measured on a green sample:
`$S/gold`, a fixture repository (`git init`, toplevel asserted; `fetch --no-tags <lane>
a7af2ce6… 8371e7ac…`; `checkout -f --detach a7af2ce6…`) carrying the round-40 stand-ins every
check requires (suite copy, SKILL.md registry row, PROVINCE/README F23 appends with real
`tail -n` shas in `declared-blocks.txt`, a QUALITY row citing M39-2, the four
`Correction (round 40)` lines, three located Gate quotes), committed as fixture
**J = 88b1e58a36d097141cfc77b36b0403e7a0712d84**; the receipt written by `--receipt-out` and
committed as fixture **Y = 9533a44bd33c4e0769e9f81709cb7922139dc98c**
(`git diff --name-only J Y` = the receipt only). The receipt's `suite-sha256` is the
deliverable's digest `bdbd18a3…`.

```
$ bash $G/corpus/instruments/r40-closure.sh --export-ref $Y --lane $G \
      --work $ROOT/kasegi-r40-gold/a --scratch-root $ROOT
all-gates v4
export-ref=88b1e58a36d097141cfc77b36b0403e7a0712d84
suite-sha256=bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
time-basis=ref-commit
run-utc=2026-10-26T21:43:22Z
H1 payload=suite=1,digest=1,registry=1,registry-in=skill closed=1
H2 payload=corrections=4,named=4,missing=0,fences=closed closed=1
H3 payload=mentions=1,rows=1 closed=1
H4 payload=s056=1,s058=1,s059=1,oversize=0 closed=1
H5 payload=source=1,control=8/8,utc=1,forged-payload=rejected,future-dated=rejected,summary-only=rejected closed=1
H6 payload=strays=0,read=ok closed=1
H7 payload=sentinel=1,ref=88b1e58a36d097141cfc77b36b0403e7a0712d84,digest=1,time-basis=1,run-utc=1,not-future=1,header-lines=5,run-lines=10,body-lines=11,closed-0=0,closed-line=1,ancestor=1,diff-clean=1,diff-read=ok,payload-match=9,h7-line=1 closed=1
H8 payload=base=3/10,base-exit=1,r39=2/10,r39-exit=1 closed=1
H9 payload=declared=2,valid=2,tail=2,pure=1,paths=1,diff-read=ok closed=1
H10 payload=skill-del=0,province-del=0,density=1,deleted=0,diff-read=ok closed=1
closed=10/10 exit=0                                                 # exit 0
```

Red limbs, same sample:

```
--export-ref <J>   (no receipt in the tree)           → closed=9/10 exit=1  (H7 receipt=0 — the documented green window)
--export-ref a7af2ce63bce153757d39bf66b366a96caf30c13  → closed=3/10 exit=1
--export-ref 8371e7ac9f32cae5ed72f8c28205634603f836fa  → closed=2/10 exit=1
plain run (no --export-ref)                            → exit 2, "refusing to run against the live worktree"
--export-ref HEAD --work <lane>/tmp-w                  → exit 2, "--work must be outside the lane"
--bogus                                                 → exit 2, "unknown argument"
--export-ref nosuchref                                 → exit 2, "cannot resolve export ref"
```

H4 was additionally validated against the **landed** lane text (not just the fixture): on
`corpus/lessons/round-39.md` with the round-40 Gate additions in the working tree,
`h4_code` returns `S056 → 1 17 0`, `S058 → 1 15 0`, `S059 → 1 16 0` (ok, longest accepted
quote in words, oversized quotes). That is what forced the `L<NN>` / `#anchor` /
`paragraph N` locator forms: the landed S056 row locates its quote as `raw HTML L1146`.

## 4. Defect found by a peer, fixed and re-measured

`ExecH7Determinism` measured the previous build (`1da1d76d…`): in `--receipt-out` mode the file
was always assembled in the canonical *green* form, so on a red ref the written receipt read
`H4 … closed=1`, `H9 … closed=1`, `closed=10/10 exit=0` while the same run's stdout read
`closed=8/10 exit=1` — six lines apart, and H7's payload comparison never looked at a line's
`closed=` flag or the tally, so the suite would accept a receipt that contradicted its own run.
That is exactly what QUALITY R37 forbids.

Fix: `--receipt-out` now iterates to the transcript fixed point — H7 is evaluated, the tally is
counted, the transcript is assembled with the run's real flags and tally, rewritten, and the
loop stops when the file equals the bytes the run will print (the H7 line is rebuilt from the
receipt minus its own line, so the payload is stable across the iteration). Measured on the
fixed bytes at the base ref, which is a red ref:

```
$ bash $G/corpus/instruments/r40-closure.sh --export-ref a7af2ce6… --lane $G \
      --work $ROOT/kasegi-r40-gold/red --scratch-root $ROOT --receipt-out $S/red-receipt.txt
exit=1
$ cmp -s $S/red-stdout.txt $S/red-receipt.txt && echo RED-STDOUT==RED-RECEIPT
RED-STDOUT==RED-RECEIPT
$ grep -E 'closed=0$|^closed=' $S/red-receipt.txt
H1 … closed=0   H2 … closed=0   H3 … closed=0   H4 … closed=0   H8 … closed=0   H9 … closed=0
H7 payload=…,run-lines=10,body-lines=11,closed-0=7,closed-line=0,ancestor=1,diff-clean=1,…  closed=0
closed=3/10 exit=1
```

The written receipt is now always the run's own transcript; a red mint can never be promoted to
a green receipt, and re-running H7 against such a file reds on `closed-0=7,closed-line=0`.

## 5. Forged-receipt battery (H5/H7 teeth, measured at the green Y)

Seven receipts, each committed as a fixture head over Y (only the receipt file changed):

```
payload     exit=1 closed=8/10 exit=1   # H3 payload rewritten to a value the export cannot produce
utc-future  exit=1 closed=8/10 exit=1   # run-utc=2999-01-01T00:00:00Z
utc-past    exit=1 closed=9/10 exit=1   # run-utc one hour BEFORE its ref's committer instant
ref         exit=1 closed=9/10 exit=1   # export-ref = a commit that is not an ancestor → ancestor=0
summary     exit=1 closed=8/10 exit=1   # header + closed line only → run-lines=0, body-lines=1
extra       exit=1 closed=9/10 exit=1   # one extra line → body-lines=12
h7line      exit=1 closed=9/10 exit=1   # the H7 line alone tampered → h7-line=0
```

None printed 10/10; each named the reopened limb in its payload (`payload-match=8` /
`not-future=0` / `run-utc=0` / `ancestor=0` / `run-lines=0` / `body-lines=12` / `h7-line=0`).
Exactly the R1/G2 class the frozen predicate asks H5/H7 to close.

## 6. Live scratch probe (H6)

When `/fast/scratch/hyaku` held `kasegi-r40-l1` (a sibling family entry that does not contain
this run's `--work`), a run over the green Y on the **real** scratch root printed:

```
H6 payload=strays=1,read=ok closed=0
closed=7/10 exit=1            # H6 red, and H5/H7 red too because a live-state change invalidates the receipt binding
```

After that directory was removed the same command on the real scratch root prints
`H6 payload=strays=0,read=ok closed=1` and `closed=10/10 exit=0`. The scratch-root payload
prints only counts, so moving `--work` inside or outside the family entry does not change the
transcript.

## 7. Determinism (H7's "re-run reproduces it byte-identically, modulo nothing")

```
two plain runs at Y, distinct --work dirs:      cmp → identical
plain run at Y vs the committed receipt:        cmp → identical
--receipt-out re-run at Y vs the committed:     cmp → identical
suite run from a COPY ($S/copy/instruments/…):  identical transcript, closed=10/10 exit=0
two runs at the freeze with TMPDIR=$S/h7/run1 and $S/h7/run2 (auto --work):
                                                cmp → identical
```

`ExecH7Determinism` independently measured the same on this suite: two runs at `5e985b7` with
distinct TMPDIR / `--work` / `--scratch-root`, and at a worktree-snapshot J, produced
byte-identical stdout and receipt.

## 8. Selftest

On the green sample Y:

```
selftest case=H1 positive=pass mutants=3/3 verdict=pass
selftest case=H2 positive=pass mutants=3/3 verdict=pass
selftest case=H3 positive=pass mutants=2/2 verdict=pass
selftest case=H4 positive=pass mutants=3/3 verdict=pass
selftest case=H5 positive=pass mutants=2/2 verdict=pass
selftest case=H6 positive=pass mutants=4/4 verdict=pass
selftest case=H7 positive=pass mutants=6/6 verdict=pass
selftest case=H8 positive=pass mutants=2/2 verdict=pass
selftest case=H9 positive=pass mutants=5/5 verdict=pass
selftest case=H10 positive=pass mutants=3/3 verdict=pass
selftest cases=10 failures=0                                        # exit 0
selftest judge=own-report accepted=1
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=forged-failed-cases rejected=1
selftest judge=forged-detail-free rejected=1
selftest judge=forged-9-cases rejected=1
selftest judge=forged-no-verdict rejected=1
```

Every mutant names the limb it reopened (H1 `suite=0|registry=0|digest=0`; H2 `missing=1` ×2,
`fences=open`; H3 `mentions=0`, `rows=0`; H4 `s059=0`, `oversize=1`, `s056=0`; H5 `control=7/8`,
`utc=0`; H6 `strays=1` ×3 including an EMPTY sibling family entry, `read=fail`; H7 `receipt=0`,
`not-future=0`, `ancestor=0`, `digest=0`, `body-lines=12`, `h7-line=0`; H8 `base-exit=2`,
`r39-exit=2`; H9 `valid=0` ×2, `pure=0`, `paths=0` ×2; H10 `density=0`, `skill-del=1`,
`deleted=1`), and the `st_control` fixtures prove the same checks accept the corrected tree
(H2/H3/H4 records+row+quotes; H5 canonical source; H6 own-work-dir; H9 whole tail; H10
append-only).

At the freeze `5e985b7` (what `ExecSuiteSelftestRun` measures) the same selftest prints
`selftest cases=10 failures=9`: the positives are red because the artifacts do not exist at
that ref, and H8's two mutants presuppose an export that carries the suite
(`H8 payload=suite=0` there). That is the red direction, recorded honestly.

## 9. Integration contracts this suite imposes (read before landing)

- **H1** needs one `|`-row naming `r40-closure.sh` appended to the SKILL.md instrument table
  (the r39 row sits at `SKILL.md:1115`, i.e. EOF) **and** the suite at
  `corpus/instruments/r40-closure.sh` with the deliverable's exact bytes.
- **H2** needs, in each of SCORECARD.md, LOG.md, SHONEN.md **and `corpus/lessons/round-39.md`**,
  at least one line beginning exactly `Correction (round 40)` that carries **both**
  `closed=7/8` and `failures=1` on that same line, outside any fence, with no unclosed fence
  left in those files. (Measured on the current working tree: all four records already satisfy
  it — `corrections=2,2,2,2` / `named=1,1,1,2` / `fences=closed`.)
- **H3** needs a `|`-row in corpus/QUALITY.md whose text cites `M39-2`.
- **H4** needs one Gate block per code S056/S058/S059 in `corpus/lessons/round-39.md` holding a
  URL, a `YYYY-MM-DD` access date, a double-quoted span of 1..25 words and a location token —
  the landed rows pass (see §3).
- **H9** needs `.ufo/waves/round-40/declared-blocks.txt` with `<path> <lines> <sha256>` where
  `<lines>` is the WHOLE appended tail (not a suffix) and the path has zero deletions
  base→ref. It is not in the working tree yet.
- **H10** requires SKILL.md and PROVINCE.md appends with no deleted line, density.py untouched
  (`ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710`), and no tracked path
  deleted in the round.
- **Gate operation**: mint the receipt at J with `--receipt-out`, commit it as Y, then run the
  plain command at Y on a scratch root whose ONLY `kasegi-r39*`/`kasegi-r40*` top-level entry is
  the one containing `--work` (an empty leftover family directory counts as a stray; remove it
  rather than empty it). Do not append the `--selftest` output to the receipt: H7 compares the
  whole file and any extra line reds it (`body-lines=12`).

## 10. Risks and blockers

- **Live-state coupling (inherent to H6, documented).** A receipt produced on a clean scratch
  root is reproducible only on a clean root: a stray family entry reds H6, and because H7 binds
  every payload line the same state also reds H5/H7 (`closed=7/10`, measured in §6). The frozen
  kill rule names the same condition, so the gate must run after scratch cleanup.
- **Y does not exist yet**, so `closed=10/10` is demonstrated on the fixture J/Y of the same
  shape, not on the lane; the lane's J must carry the artifacts in §9 or the matching check reds
  (H7's green window included: at J the suite prints 9/10 by design).
- **H8's negative controls run only where the export carries the suite** (J/Y); at the freeze it
  reports `suite=0` (red, honest).
- No blockers; nothing was withheld. This seat judged nothing, widened nothing and committed
  nothing.
