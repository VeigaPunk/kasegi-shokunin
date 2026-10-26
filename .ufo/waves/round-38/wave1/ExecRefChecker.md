# ExecRefChecker — independent reference checker for the round-38 closure contract (G1–G8)

Seat: `ExecRefChecker` (leaf, executor). Round kasegi-shokunin 38. Deliverable:
`.ufo/waves/round-38/wave1/ExecRefChecker.py` — an independent Python 3 (stdlib only)
implementation of the eight G1–G8 verdicts, written from the frozen claims contract
(`.ufo/waves/round-38/claims.json`, C1) and from the committed r37 suite's *documented
contract*, not its code. It imports nothing from the bash suite, never sources it, and
shells out to bash only for G8's carry-over limb (which by contract runs the export's own
`corpus/instruments/r37-closure.sh`).

## Deliverable facts

| Item | Value |
|---|---|
| Path | `.ufo/waves/round-38/wave1/ExecRefChecker.py` |
| Lines | 1208 |
| Bytes | 47556 |
| sha256 | `05dcafcedaaa6126eb531abc7030c4c1b846dc29340b4507e04d28352daeeb00` |
| Language | Python 3.14, standard library only (`hashlib json os re shutil subprocess sys tempfile`) |
| Lane writes | none (archive export + `--work` outside the lane only) |

Flags implemented exactly as the contract states: `--export-ref <hash>`, `--selftest
[--export-ref <hash>]`, `--lane DIR` (default `/home/vgpnk/Projects/shokunin/kasegi-shokunin`),
`--work DIR` (must resolve outside the lane; `export/` `mut/` `base/` `r37/` cleared before
use), `--scratch-root DIR` (default `/fast/scratch/hyaku`), `-h`. Plain run → exit 2.

Output shape (export mode):

```
export-ref=<40 hex> mode=export lane=<lane> suite-sha256=<digest>
G1 payload=<k=v,...> closed=0|1
…
G8 payload=<k=v,...> closed=0|1
closed=<k>/8 exit=<0|1>
```

Selftest mode prints `mode=selftest`, one `selftest case=G<n> positive=… mutants=<o>/<n>
verdict=…` line per check, one `selftest detail=G<n> mutant=<label> rejected=0|1` line per
mutant, then `selftest cases=8 failures=<k>`.

## Contract readings that the L1 must know before diffing against the bash suite

These are the places where the written contract leaves a choice; the verdict table is
comparable, the payload **key names are deliberately independent** (no shared code):

1. **Scope of the round-38 SCORECARD carrier (G2/G5).** The section is the **LAST**
   `^## Round 38` heading block, closed by the next `^## ` heading (the round appends one;
   the r37 suite uses the same last-block rule for round-37). `payload=round38-sections=N`
   and `carrier-lines=N` expose both counts so a divergence is visible.
2. **SHONEN scope (G2).** Every line matching `round[- ]38` case-insensitively. Base SHONEN
   lines name round 37 only, so they are out of scope by construction — verified by the
   synthetic positive, where only the added round-38 line is scanned.
3. **G1 declared blocks.** `tail -n <lines>` semantics are implemented byte-exactly (last n
   lines with their terminators, `b"".join(data.splitlines(keepends=True)[-n:])`); a
   non-3-field line, a non-numeric count or a 64-hex-mismatched digest makes the whole limb
   red (fail closed), and both front-door files need >= 1 declared line.
4. **G3 added-line source.** On a real run: `git -C <lane> diff <BASE> <REF> -- . ':!.ufo'
   ':!corpus/instruments/r38-closure.sh' ':!corpus/instruments/r38-fixtures'`. For a
   selftest mutant (a copied tree that is not a commit) it is `git diff --no-index` of the
   base export against the mutant tree with the same exclusions — both compute "lines added
   relative to the base tree", which is what makes the `TODO` mutant rejectable.
5. **G4 acceptance.** The sibling `*-results.json` (stem of the dispatch) is tried first,
   then the dispatcher's `<wave>-results.json` (the dispatch's `wave` field) in the same
   directory, accepted only when the file's own `wave` agrees. Seat count = `len(results)`,
   and the top-level `seats` count, when present, must agree.
6. **G6 allowance.** `kasegi-r38` may contain only the resolved `--work` dir or its
   top-level parent under `kasegi-r38`. Other seats' scratch dirs are **not** exempted, so a
   live wave reads RED by design — see the live reading below.
7. **G8 is the r37 suite, unchanged.** It inherits r37 E9(d) ("the exported ref IS the
   lane's HEAD") and E9(b) (clean worktree). A historical export therefore can never read
   quiescent now; the base and r37-judged-head exports fail G8 for that **live** reason, not
   for a byte defect (evidence below). G8 passes on a ref the runner has checked out —
   which is exactly the state of the judged head J when the L1 runs its gates.

## Verdict table — historical trees (RED control)

Commands (final checker bytes, `sha256=05dcafce…`):

```
python3 .ufo/waves/round-38/wave1/ExecRefChecker.py \
  --export-ref a173b0c2b98c5ae39599fa9be76027fbbead0b9e --work <S>/w-base        -> exit 1
python3 .ufo/waves/round-38/wave1/ExecRefChecker.py \
  --export-ref 2387dcf6ccfefcfb703783387b9aade8fc82abfa --work <S>/w-r37judged   -> exit 1
```

| Check | base `a173b0c2` | r37 judged head `2387dcf6` |
|---|---|---|
| G1 | `closed=0` — `province-correction=0,readme-correction=0,province-fence=closed,readme-fence=open,declared-lines=0,declared-match=0,declared-covered=0` | idem |
| G2 | `closed=0` — `receipt=missing,version=absent,export-ref=none,export-ref-exists=0,ancestor=0,diff-extra=-1,digest=0,run-lines=0,run-open=0,closed-line=0,selftest-cases=0,selftest-summary=0,carrier-lines=0,carrier-reference=0,label-hashes=0` | idem |
| G3 | `closed=0` — `lesson-section=0,markers=0/8,marker-rows=0,added-scan=read,added-fixed-tokens=0,added-word-tokens=0` | idem |
| G4 | `closed=0` — `dispatches=0,paired=0,seats-match=0,detail=none` | idem |
| G5 | `closed=0` — `round38-sections=0,final-lane-commit=0,anchor-correction=0` | idem |
| G6 | `closed=0` — `r36=absent,r37=absent,r38=stray,offenders=26` (live) | idem |
| G7 | `closed=0` — `filled-heading=0,after-original=0,correction=0,rows=0,proposals=0/7` | idem |
| G8 | `closed=0` — `r37=present,last=closed=13/14,exit=1,lines=17` | idem |
| **total** | **`closed=0/8 exit=1`** | **`closed=0/8 exit=1`** |

Both trees contradict nothing in `c1-controls/before.txt`: G1 sees README.md's fence OPEN at
EOF (`readme-fence=open`, opener at L426) and no round-38 corrections; G7 sees the empty
`## Round-37 dispositions (appended 2026-10-26, R31 home)` heading with 0 rows; G2/G4/G5 see
no round-38 files at all.

G8's live red at base is the r37 suite's own E9 limb, measured directly:

```
$ bash corpus/instruments/r37-closure.sh --export-ref a173b0c2… --work <S>/r37probe
E9 payload=status-read=ok,status-dirty=3,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=absent closed=0
closed=13/14 exit=1
```

`head-match=0` (lane HEAD is `7001535`, not the exported ref) and `status-dirty=3` (the
untracked round-38 wave files). At the freeze moment (`c1-controls/before.txt`) the lane HEAD
*was* the base, which is why the L1 measured 14/14 then. G8 re-passes on the judged head J,
where J is the checkout.

## Synthetic all-green overlay (POSITIVE control, 8/8)

Fixture (scratch only, `/fast/scratch/hyaku/kasegi-r38/ExecRefChecker/synth/repo`):

```
git clone --shared --no-checkout <lane> <fixture>      # history so BASE and the r37 hashes resolve
git -C <fixture> rev-parse --show-toplevel             # == <fixture> (verified before any mutation)
git -C <fixture> checkout -q -B synth a173b0c2…        # worktree bytes == git archive of BASE
git -C <fixture> diff --name-only a173b0c2…            # empty
```

Synthetic round-38 files applied on top of the base tree:

| Path | Synthetic content |
|---|---|
| `PROVINCE.md` | + 1 line `Correction (round 38) … L79-L152 … misplaced` (fences stay CLOSED: 81 opens, 96 ```` ```text ```` does not close, 124 closes) |
| `corpus/README.md` | + bare ```` ``` ```` closing the L426 fence, then `Correction (round 38) … L399-L454 … misplaced` |
| `SCORECARD.md` | + `## Round 38 result` section: axis row naming `judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt`, and one line `Correction (round 38): f3246559… is an anchor ancestor …` (no `Final lane commit:`) |
| `SHONEN.md` | + one round-38 evidence line carrying the same by-reference sentence, no commit hash |
| `corpus/lessons/round-37.md` | + `## Pending-marker resolutions (round 38)` with rows L10, L85, L90, L95, L216, L265, L300, L320 |
| `corpus/knowledge/considerthese-proposals-ledger.md` | + `## Round-37 dispositions — filled (round 38)` after the original heading, a `Correction (round 38)` line and 7 proposal rows |
| `.ufo/waves/round-38/declared-blocks.txt` | `PROVINCE.md 1 057f1524…` / `corpus/README.md 2 a2e02a16…` (tail-sha verified) |
| `.ufo/waves/round-38/wave1-dispatch.json` | byte copy of the real dispatch (73 `taskCall.tasks`) |
| `.ufo/waves/round-38/wave1-results.json` | `seats=73`, `results` = 73 entries named from the dispatch |
| `.ufo/waves/round-38/final-gates/all-gates.txt` | `all-gates v2`, `export-ref=<T0>`, `suite-sha256=<python digest>`, 8 `G<n> payload=… closed=1`, `closed=8/8 exit=0`, 8 selftest case lines + details, `selftest cases=8 failures=0` |

Receipt bootstrap and fixed point (a commit cannot contain its own hash, so `export-ref`
names its parent `T0`; `git diff T0 REF` is the receipt alone):

```
T0  = 6c5313e309e66cda6a8369bd761af1bde7109611   (overlay, no receipt)
REF = 5dd62f96408fb89789273f140087f5d38a2c9e49   (overlay + receipt)
suite-sha256 = 05dcafcedaaa6126eb531abc7030c4c1b846dc29340b4507e04d28352daeeb00
iteration 1 REF=758aa4fa… run-rc=0 selftest-rc=0
iteration 2 REF=5dd62f96… run-rc=0 selftest-rc=0
fixed-point=True iterations=2
diff T0..REF = .ufo/waves/round-38/final-gates/all-gates.txt
```

The fixed point is real, not asserted: after the second amend the recorded G-lines and
selftest lines are **byte-identical** to a fresh run at the commit that contains them
(`fixed-point run-lines=True selftest-lines=True`). The receipt's only authored line is
G2's own payload; it is replaced by the produced one on iteration 2.

Run at REF (`--lane <fixture> --scratch-root <fixture-scratch>` where that scratch root is
absent, i.e. quiescent):

```
export-ref=5dd62f96408fb89789273f140087f5d38a2c9e49 mode=export lane=<fixture> suite-sha256=05dcafce…
G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-lines=2,declared-match=2,declared-covered=1 closed=1
G2 payload=receipt=present,version=v2,export-ref=6c5313e309e66cda6a8369bd761af1bde7109611,export-ref-exists=1,ancestor=1,diff-extra=0,digest=1,run-lines=8,run-open=0,closed-line=1,selftest-cases=8,selftest-summary=1,carrier-lines=8,carrier-reference=1,label-hashes=0 closed=1
G3 payload=lesson-section=1,markers=8/8,marker-rows=10,added-scan=read,added-fixed-tokens=0,added-word-tokens=0 closed=1
G4 payload=dispatches=1,paired=1,seats-match=1,detail=none closed=1
G5 payload=round38-sections=1,final-lane-commit=0,anchor-correction=1 closed=1
G6 payload=r36=absent,r37=absent,r38=absent,offenders=0 closed=1
G7 payload=filled-heading=1,after-original=1,correction=1,rows=7,proposals=7/7 closed=1
G8 payload=r37=present,last=closed=14/14,exit=0,lines=17 closed=1
closed=8/8 exit=0
```

**8/8 exit 0 on the all-green overlay; 0/8 exit 1 on both historical trees.** That is the
two-sided discrimination the L1 needs to diff against the bash suite.

### G6 is live, and it is not spoofable

Same synthetic tree, same REF, but `--scratch-root /fast/scratch/hyaku` (the live wave root):

```
G6 payload=r36=absent,r37=absent,r38=stray,offenders=33 closed=0
closed=7/8 exit=1
```

The synthetic 8/8 therefore rests on a quiescent scratch root passed explicitly; the live
root reads RED while 33 sibling seat dirs exist, which is the honest live reading. The final
gate reads G6 green only after scratch cleanup.

## Selftest (mutant discrimination) — `selftest cases=8 failures=0`, exit 0

```
selftest case=G1 positive=pass mutants=3/3 verdict=pass
selftest detail=G1 mutant=drop-province-correction rejected=1
selftest detail=G1 mutant=reopen-readme-fence rejected=1
selftest detail=G1 mutant=declared-digest-flip rejected=1
selftest case=G2 positive=pass mutants=5/5 verdict=pass
selftest detail=G2 mutant=header-v1 rejected=1
selftest detail=G2 mutant=export-ref-not-ancestor rejected=1
selftest detail=G2 mutant=extra-file-in-diff rejected=1
selftest detail=G2 mutant=digest-mismatch rejected=1
selftest detail=G2 mutant=final-head-label rejected=1
selftest case=G3 positive=pass mutants=2/2 verdict=pass
selftest detail=G3 mutant=drop-L265-row rejected=1
selftest detail=G3 mutant=add-toggle-marker rejected=1
selftest case=G4 positive=pass mutants=2/2 verdict=pass
selftest detail=G4 mutant=drop-results rejected=1
selftest detail=G4 mutant=drop-seat-entry rejected=1
selftest case=G5 positive=pass mutants=2/2 verdict=pass
selftest detail=G5 mutant=final-lane-commit-label rejected=1
selftest detail=G5 mutant=drop-anchor-correction rejected=1
selftest case=G6 positive=pass mutants=2/2 verdict=pass
selftest detail=G6 mutant=stray-kasegi-r36 rejected=1
selftest detail=G6 mutant=stray-kasegi-r38 rejected=1
selftest case=G7 positive=pass mutants=2/2 verdict=pass
selftest detail=G7 mutant=drop-proposal-row-4 rejected=1
selftest detail=G7 mutant=drop-correction-line rejected=1
selftest case=G8 positive=pass mutants=2/2 verdict=pass
selftest detail=G8 mutant=mutant-stub-carry-over rejected=1
selftest detail=G8 mutant=ref-with-red-r37 rejected=1
selftest cases=8 failures=0
```

20 single-defect mutants, each rejected, each positive green. Mutant mechanics: a hardlink
copy of the export (`copytree(copy_function=os.link)`; every mutation unlinks before writing,
so the source tree is never touched), then exactly one clause reopened:
G1 drops the PROVINCE correction / appends a fence opener at EOF / flips one digest byte in
`declared-blocks.txt`; G2 sets `all-gates v1` / points `export-ref` at a commit that is not an
ancestor (or an unresolvable hash when no such commit exists) / points it at `BASE` so the
receipt diff grows / sets a false `suite-sha256` / injects `Final head deadbeef…` into the
round-38 SCORECARD section; G3 drops the `L265` row / appends a `TODO` line (rejected through
the added-lines limb, which for a copied tree is the base-vs-mutant no-index diff);
G4 deletes the results file / drops one seat entry; G5 injects `Final lane commit: abc1234` /
drops the anchor-ancestor correction; G6 plants `kasegi-r36/Stray/leftover.txt` and
`kasegi-r38/…` in a fake scratch root; G7 drops proposal row 4 / drops the correction line;
G8 replaces the export's `r37-closure.sh` with a transcript that ends `closed=13/14 exit=1`
and, separately, runs G8 at `BASE` where the r37 suite is red.

## Summary-only forgery probe

The contract requires that a receipt full of green lines cannot satisfy a check by itself.
On a clone of the fixture (`<S>/forge/repo`), the PROVINCE correction was deleted and the
receipt left untouched (its G1 line still claims `province-correction=1 … closed=1`):

```
province correction lines left = 0
receipt claim: G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-lines=2,declared-match=2,declared-covered=1 closed=1
G1 payload=province-correction=0,readme-correction=1,province-fence=closed,readme-fence=closed,declared-lines=2,declared-match=1,declared-covered=0 closed=0
G2 payload=…,diff-extra=1,…,run-lines=8,run-open=0,… closed=0
closed=6/8 exit=1
```

The receipt's claim is not evidence: G1 reads the bytes (red) and G2's committed-diff limb
sees the new file between the receipt's `export-ref` and the forged ref (red).

## Guard probes (harness discipline)

```
$ python3 ExecRefChecker.py --export-ref HEAD --work corpus/work-inside
ExecRefChecker: --work must be outside the lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/work-inside
exit=2                                   # and `ls corpus/work-inside` -> No such file (refused before creating)
$ python3 ExecRefChecker.py --export-ref deadbeef… --work <S>/w-bad
ExecRefChecker: cannot resolve export ref in /home/vgpnk/Projects/shokunin/kasegi-shokunin: deadbeef…
exit=2
$ python3 ExecRefChecker.py                       # plain run
ExecRefChecker: plain run refused: --export-ref <hash> is required (or --selftest); …
exit=2
$ python3 ExecRefChecker.py -h                    # usage, exit 0
```

Export and work-dir rules mirror the committed r37 suite: `realpath` guard before anything
is created, a second guard after `mkdir` (a symlink into the lane is refused), the `export/`
`mut/` `base/` `r37/` subdirectories cleared before use, `git archive <ref> | tar -x` as the
only export mechanism, and an auto-created work dir under `TMPDIR` that is removed on exit.

## Cross-check handoff (what to diff)

The bash suite and this checker must agree on the **verdict vector**, not on payload text:
historical base and r37 judged head → `closed=0/8 exit=1` each; well-formed round-38 tree →
`closed=8/8 exit=0`; selftest → `cases=8 failures=<0>`. Points to compare closely:

- G2's receipt contract: 8 closed=1 G-lines covering G1–G8 exactly once, one
  `closed=8/8 exit=0`, 8 case lines, one `selftest cases=8 failures=0`, digest = the running
  suite's digest, `export-ref` ancestor-or-equal with diff == receipt only. The **v2 receipt
  the L1 lands must carry the bash suite's own digest**, not this file's
  (`05dcafce…`); the synthetic receipt above is a Python-fixture artifact and is not a lane
  file.
- G6 live: both suites are red while sibling scratch dirs exist; both must read green after
  cleanup. An empty `--scratch-root` argument is the only honest way to demonstrate a green
  G6 out of wave time.
- G8: identical instrument by construction; at base it is red for the r37 E9 head/dirty
  limbs, and it is green only at a ref the runner has checked out.

If the bash suite's verdict differs anywhere on a real tree, the divergence is a contract
reading, and the payload keys above name which limb to inspect.

## Risks and limits (disclosed, not hidden)

- G2 proves receipt **shape**, digest, ancestry and the committed diff; it cannot prove the
  recorded *values* were produced before the receipt commit. The judged head is therefore
  named only by reference, and the receipt's export-ref must name an ancestor (a commit
  cannot contain its own hash).
- G3's placeholder limb reads the base..REF diff of the lane; a placeholder introduced in a
  file outside the diff scope (e.g. under `.ufo`) is out of scope by contract.
- G4 is a parity check: empty-but-named seat entries still count. Content quality of the
  results file is the QUALITY gates' business, not this checker's.
- G6 trusts the `--scratch-root` it is given; a typo'd root reads `absent` (green for
  r36/r37/r38). The payload prints the three directory states so the reading is auditable.
- This file is wave evidence: it is **not** a lane instrument, is not registered in
  `SKILL.md`, and is not referenced by `r38-closure.sh`. The committed instrument remains
  the bash suite; this checker exists to contradict it if it is wrong.

## Tooling and cleanliness

- No tool was installed or upgraded this seat; nothing to record. `python3` and `git` were
  already present.
- No network fetch was made (no HTTP status/bytes/time to record).
- Scratch `/fast/scratch/hyaku/kasegi-r38/ExecRefChecker/` (base/r37 evidence transcripts,
  the fixture repo and its build script) was removed after this receipt was written; no
  `kasegi-r36`/`kasegi-r37`/`kasegi-r38/<SEAT>` entry is left by this seat.
- No lane file other than this receipt and the deliverable `.py` was written; no git mutation
  was run in the lane (only read-only `log/show/ls-tree/rev-parse/diff/status/archive`), and
  all fixture commits happened inside `<S>/synth/repo` after `rev-parse --show-toplevel`
  equalled it.
