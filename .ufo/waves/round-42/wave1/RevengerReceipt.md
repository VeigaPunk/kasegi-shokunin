# RevengerReceipt — how the round-41 receipt was produced, and the round-42 receipt-production spec

Seat `RevengerReceipt`, round-42 build wave 1, leaf, receipt-only. No subagent, no lane writes except this
file, no git/jj mutation, no tool installs, no network fetches. Scratch
`S=/fast/scratch/hyaku/kasegi-r42/RevengerReceipt` (removed before yield). Every suite run is export-mode
with `--work` outside the lane.

Refs, all resolved in `/home/vgpnk/Projects/shokunin/kasegi-shokunin`:

```
B     r42 base             = 5053a7f46de35784cff4b56756906e9014a38276
J     r41 judged head      = 1f7464612ac4c44e39886b82e812610d3c039b13   committer 1793103394 = 2026-10-27T12:16:34Z
Y     r41 receipt ref      = 0f64b8c5b3522d4db2160db087002e3a5f321880   committer 2026-10-27T12:31:58Z
Z     r41 lane tip         = 7ebe3cc71b3d1c18d44155ce5f71f92e07d6c409
receipt                    = .ufo/waves/round-41/final-gates/all-gates.txt
receipt sha256             = 0915f51d774e5f4bd744912b6b2a87b7387f5437730bef166457766ca10b9e94 (2481 bytes, 31 lines)
suite sha256 at B..Z       = 3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd
```

## 1. Reconstructed production path

There is no `make-receipt.sh` in this lane and never was. `git log --all -- '*make-receipt*'` prints
nothing, and the only added `.sh` whose path matches `receipt` is the round-28
`ExecReceiptCanonC2/emit-c2-block.sh`. The `make-receipt.sh` that wave receipts cite lived in the **L1's
scratch**, never committed: round-39's seat inventory lists it
(`round-39/wave1/RevScratchDiscipline.md:21`, `ExecDiskGuardProbe.md:90`) and the round-39 verifier records
that it "printed no `run-utc` line" (`round-39-verifier-spotcheck.md` §5 R1; restated at
`round-41/wave1/RevReceiptPath.md:187`). Its shape was `echo "export-ref=$J"` followed by the suite run —
the hand-assembly the r39 spot-check rejected.

The r41 generator is the suite itself. `corpus/instruments/r41-closure.sh:84-96`:

> There is NO make-receipt mode: the L1 produces the receipt by tee-ing the run, e.g.
> `bash corpus/instruments/r41-closure.sh --export-ref <J> --receipt-out .ufo/waves/round-41/final-gates/all-gates.txt`
> (the written file is byte-identical to the run's stdout, so `... | tee <path>` is equivalent).

Six steps, in order:

**P0 — the suite is fixed before J and never changes.** `corpus/instruments/r41-closure.sh` hashes to
`3971a112…` at `1f74646`, at `HEAD`, and in the working tree (three separate `sha256sum` reads). The header
digest is a property of the tree, so a transcript can be re-derived long after production.

**P1 — J is the tree the receipt names.** `1f74646…`, committer `1793103394` = `2026-10-27T12:16:34Z`.

**P2 — mint at J.** `run_suite_report` (2036-2091) runs, in this order: `selftest_prepare`;
`compute_payloads` over `PAYLOAD_ORDER=(I1 I3 I4 I5 I6 I7 I10 I11 I12 I8 I9)`; `run_selftest_cases` into
`$WORK/selftest-detail.txt`, which writes one `$WORK/sel-<ID>.line` per case — **those twelve lines are the
ones the receipt embeds**; `i2_fixture "$SEED"` (the canonical transcript, already the fixed point); then a
loop of at most four passes that runs I2 against `receipt_source`, rewrites the I2 row, calls
`assemble_transcript`, writes `$RECEIPT_OUT`, and re-runs I2 until the payload stops moving; then a final
`assemble_transcript`, a final write, and `printf '%s\n' "$bytes"` to stdout.

**P3 — commit exactly those bytes as Y, and only that path.** Measured:

```
$ git diff --name-only 1f74646 0f64b8c
.ufo/waves/round-41/final-gates/all-gates.txt
$ git merge-base --is-ancestor 1f74646 0f64b8c && echo YES
YES
$ git show 0f64b8c:.ufo/waves/round-41/final-gates/all-gates.txt | diff - .ufo/…/all-gates.txt
(no output — identical)
```

Y's committer instant is 15 min after `run-utc`, so the stamp never post-dates its own commit. The receipt
is absent at J by construction (`git cat-file -e 1f74646:…/all-gates.txt` fails), as it must be: a commit
cannot contain its own hash.

**P4 — the count run at Y is the published observation.** Measured today, with `--work` under
`--scratch-root`:

```
$ bash corpus/instruments/r41-closure.sh --export-ref 0f64b8c5… --work $S/workY --scratch-root $S
rc=1
0915f51d774e5f4bd744912b6b2a87b7387f5437730bef166457766ca10b9e94  replayY.out
BYTE_IDENTICAL                      # diff -u against the committed receipt: no output
```

**P5 — nothing else enters the file.** Z adds `LOG.md`, `SCORECARD.md`, `SHONEN.md`,
`corpus/lessons/round-41.md` and does not touch the receipt.

**What a run at J can and cannot reproduce.** The same command at J prints 31 lines that differ from the
committed receipt on **exactly one line**, the integrity line:

```
-I2 payload=receipt=1,sentinel=1,ref=1f74646…,digest=1,…,header-lines=5,run-lines=12,selftest-lines=12,selftest-verdicts=8,summary=0,closed-line=0,payload-match=11/11,ancestor=1,diff-clean=1,diff-read=ok,i8-match=1,cmp=0,i2-line=0 closed=0
+I2 payload=receipt=0,sentinel=0,ref=,digest=0,…,header-lines=0,run-lines=0,selftest-lines=0,selftest-verdicts=0,summary=0,closed-line=0,payload-match=0/11,ancestor=0,diff-clean=0,diff-read=ok,i8-match=0,cmp=0,i2-line=0 closed=0
```

The header, I1, I3-I12, the twelve graded selftest lines, the summary and the closed line are byte-identical.
`--receipt-out` is what lets the mint's integrity line grade the seed instead of reporting an absent
receipt. That is the "green window": the file is *written* at J and *verified* at Y.

## 2. The grammar that landed (r41, measured on the committed bytes)

Five header lines, one run line per check, one graded selftest line per check, the summary and the closed
line — 31 lines, one trailing newline, no blank line anywhere:

```
all-gates v1
export-ref=1f7464612ac4c44e39886b82e812610d3c039b13
suite-sha256=3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd
time-basis=ref-commit
run-utc=2026-10-27T12:16:34Z
I1 payload=<k=v,…> closed=0|1
… I2-I12 …
selftest case=I<n> mutants=<ok>/<n> positive=pass|fail payload-match=1|0 verdict=pass|fail
… I1-I12 …
selftest cases=12 failures=6
closed=10/12 exit=1
```

| line | text | derivation (`assemble_transcript` 1997-2029, `receipt_shape` 697-745) |
|---|---|---|
| 1 | `all-gates v1` | `SENTINEL`, compared byte-exactly against line 1 |
| 2 | `export-ref=<40 hex>` | the ref the receipt names (J), never the run ref; `grep -cE '^export-ref=[0-9a-f]{40}$'` must be 1 |
| 3 | `suite-sha256=<64 hex>` | `sha256sum` of `corpus/instruments/r41-closure.sh` **inside the export under test** |
| 4 | `time-basis=ref-commit` | literal; `grep -cxF` must be 1 |
| 5 | `run-utc=<YYYY-MM-DDTHH:MM:SSZ>` | `TZ=UTC date -u -d "@$(git log -1 --format=%ct <line-2 ref>)"`; also must not exceed now+120 s |
| 6-17 | `I<n> payload=… closed=0\|1` | printed in `CHECK_IDS` order regardless of evaluation order |
| 18-29 | `selftest case=I<n> …` | printed in `CHECK_IDS` order; these lines are re-executed on every run |
| 30 | `selftest cases=12 failures=<k>` | `CASES`/`FAILS` of the selftest this run executed |
| 31 | `closed=<k>/12 exit=<0\|1>` | k = run lines with `closed=1`; exit 0 iff k=12 |

`payload` is `k=v` pairs joined by `,` with no spaces. The id, `payload=` and ` closed=` are the only anchors
a parser may use.

## 3. The tee grammar and the red paths

- The file *is* the stdout: `bytes=$(assemble_transcript)` (command substitution strips trailing newlines),
  then `printf '%s\n' "$bytes" > "$RECEIPT_OUT"` and `printf '%s\n' "$bytes"`. Exactly one trailing newline,
  so `cmp file <(run)` is clean and `| tee <path>` is equivalent.
- `--receipt-out` requires `--export-ref` and is refused under `--selftest` (exit 2).
- Exit codes: 0 closed, 1 open defect(s), 2 harness error. A plain run is exit 2, stdout empty, stderr
  exactly:

```
r41-closure: refusing to run against the live worktree: this suite is export-mode only.
r41-closure: pass --export-ref <hash> (see --help) or --selftest.
```

- An unresolvable `--export-ref` is **not** a harness error. `print_ref_not_found` (376-393) prints
  `suite-ref-status=ref-not-found`, the five header lines with `run-utc=unreadable`, one
  `I<n> payload=ref-not-found,ref=<want> closed=0` per check, `selftest cases=0 failures=0`, then
  `closed=0/12 exit=1`, and exits 1. A mistyped ref therefore cannot be read as a partly-closed run.

## 4. What binds each payload line to the run

Five bindings, each recomputed by the receipt-integrity check (I2), never read on trust:

**B1 — ref pair.** Line 2 must resolve in the lane (`git cat-file -e <ref>^{commit}`), be an ancestor of
the run ref (`merge-base --is-ancestor`), and satisfy `git diff --name-only <ref> <run-ref>` = nothing but
the receipt path. Measured: `ancestor=1,diff-clean=1,diff-read=ok`.

**B2 — suite bytes.** Line 3 is recomputed from the export; a mismatch sets `digest=0`.

**B3 — the clock is the commit's.** Line 5 is re-derived from line 2's committer instant. A re-stamped or
wall-clock value sets `run-utc=0`; a future stamp sets `not-future=0`. Measured: `12:16:34Z` is exactly
`%ct` of `1f74646`, and is 15 min before Y's own commit.

**B4 — payload values.** Every `I<n> payload=` is compared as a whole string against the payload the run
recomputes from the export (`payload_match_count` over `NON_I2`, `payload_get`). I8's line is re-derived
against fresh scratch fixtures (`i8-match`). I2's own line is rebuilt from the receipt **minus its own
line** (`i2_canonical`) and byte-compared (`cmp`). Measured: `payload-match=11/11`.

**B5 — the selftest block is re-executed.** The twelve graded lines are not shape-checked: the run executes
the twelve cases again and compares the block byte for byte, excluding only I2's own case line. The summary
must be exactly `selftest cases=12 failures=0` exactly once.

The shape constants that only a green receipt satisfies: `summary` is
`grep -cxF 'selftest cases=12 failures=0'`, `closed-line` is `grep -cxF 'closed=12/12 exit=0'`, and
`selftest-verdicts` counts `verdict=pass` lines and must equal 12. The committed receipt is red
(`failures=6`, `closed=10/12`), so its own I2 is necessarily red: the integrity check is a green-ness gate
as well as a fidelity gate.

## 5. What it does not bind — measured, not argued

The suite claims (157-159): *"No path, no flag and no clock is printed: the transcript is a function of the
tree and the ref-scoped facts only, so two plain runs over the same ref are byte-identical."* That is false
for I6, and the falsifier is measured.

I6 scans `--scratch-root` recursively for entries whose basename normalizes (lowercase, separators collapsed
to `-`) into the family `kasegi-r41`/`kasegi-r41-*`. The lane's own tree contains six such basenames:

```
.ufo/waves/round-41/kasegi-r41-build-results.json
.ufo/waves/round-41/kasegi-r41-build.ready
.ufo/waves/round-41/kasegi-r41-build.ready.dispatched
.ufo/waves/round-41/kasegi-r41-falsify-results.json
.ufo/waves/round-41/kasegi-r41-falsify.ready
.ufo/waves/round-41/kasegi-r41-falsify.ready.dispatched
```

When `--work` lies **under** `--scratch-root` — which is exactly what the claim's own counting command does,
`--work <scratch>/work --scratch-root <scratch>` — the export is inside the scanned root and those six files
are counted as strays. Because they are regular files, `cd "$e"` fails and the scan also reports
`read=fail`. When `--work` lies outside the scanned root they are never seen.

**Direct measurement** (the suite's own functions, sourced, run against materialised roots):

```
clean-empty   : strays=0,read=ok,scanned=0
six-files     : strays=6,read=fail,scanned=6
real-seat-dir : strays=1,read=ok,scanned=1

A) export OUTSIDE scan root : I6 payload=strays=0,read=ok,scanned=0   rc=0
B) export INSIDE scan root  : I6 payload=strays=6,read=fail,scanned=6 rc=1
```

**Whole-suite measurement** — same ref `Y`, same suite bytes `3971a112…`, same command, only the placement
of `--work` changed:

```
                        --work under --scratch-root      --work outside --scratch-root
rc                      1                                1
sha256                  0915f51d… (== committed receipt) 1d678477c9eb313d1478ae856fbd606c0a38500c5470924de01387cf02f0fd2a
I2 payload-match        11/11                            9/11
I6 payload              strays=6,read=fail,scanned=6      strays=0,read=ok,scanned=0
I6 closed               0                                1
I10 payload             suite=1,base=3/12,base-exit=1,    suite=1,base=4/12,base-exit=1,
                        r40=3/12,r40-exit=1,probe=3/3     r40=4/12,r40-exit=1,probe=3/3
selftest case=I6        mutants=5/5 positive=fail        mutants=5/5 positive=pass
                        payload-match=0 verdict=fail      payload-match=1 verdict=pass
selftest cases=12       failures=6                        failures=5
closed                  10/12 exit=1                      11/12 exit=1
```

So the committed `strays=6,read=fail,scanned=6` is **not** host stray state: it is the six committed marker
files, and `read=fail` is a file-versus-directory misclassification. The receipt records the invocation's
directory placement. The same tree prints two different transcripts, and even the nested negative-control
tallies move (`base=3/12` vs `base=4/12`) because the nested runs inherit the placement.

A third data point, from an accidental 7th family entry in the scan root: `I6 payload=strays=7,read=fail,
scanned=7` and `payload-match=10/11`, with every other payload line still byte-identical. One placement or
one extra directory is enough to red the binding.

`[INFERENCE]` The production run's scratch root contained the export (so the six were seen) and no live
seat directories (`scanned=6` exactly), because a replay with the same placement reproduces `scanned=6`.

## 6. Lineage and divergences

The receipt contract converged over three rounds:

| round | line 1 | lines | shape | measured defect |
|---|---|---|---|---|
| r39 | `all-gates v5` | 87 | hand-assembled; **no `time-basis` line**; a literal `== run ==` separator; embeds `lane=/fast/scratch/hyaku/kasegi-r39/gates-work/lane` | the R1 class; a path and a stamp the run did not print |
| r40 | `all-gates v4` | 16 | 5 header + 10 run + `closed=10/10` | **no selftest block** (`grep -c '^selftest'` = 0), so the quoted `selftest cases=10 failures=0` has no committed transcript |
| r41 | `all-gates v1` | 31 | + the twelve graded selftest lines and the summary | red (`10/12`, `failures=6`); I6 placement dependence; the I2 cascade below |

| # | Divergence (r41) | Measured |
|---|---|---|
| D1 | I6's payload is a function of the `--work`/`--scratch-root` placement, not of the tree | §5: same ref, two placements, `closed=10/12` vs `11/12` |
| D2 | A family **file** is counted as an unreadable scratch entry (`cd` into a file fails → `read=fail`) | `six-files → strays=6,read=fail,scanned=6` vs `real-seat-dir → strays=1,read=ok` |
| D3 | The graded receipt case is not isolated: `i2_fixture` embeds the other cases' real verdict lines, so one failing check reds I2 | `selftest detail=I2 positive=fail … selftest-verdicts=9 … cmp=1 … i2-line=0`; the only failing limb is the count of other verdicts |
| D4 | `foreign-ref` and `nonexistent-ref` are the **same** clause (`git cat-file -e` fails), so they are not independent | `forge_flags` 1252-1257 |
| D5 | Duplicate `I2`/`I8` run lines and duplicate selftest case lines are stripped before the byte compare | `i2_compare` 910-925; the graded case has no digest and no duplicate-line mutant (1717-1745) |
| D6 | The receipt is written up to four times inside the fixed-point loop, not atomically | `run_suite_report` 2060-2077 |
| D7 | The sentinel is not a version: v5 → v4 → v1, so the token cannot identify a grammar revision | first lines of the three receipts |
| D8 | `failures=<k>` is not the number of failing cases: `st_neg` and `st_verdict` both increment `FAILS` | 4 failing cases, `failures=6` |
| D9 | The receipt is red, so the round-41 C1 after-state was never reached | `closed=10/12 exit=1`, `selftest cases=12 failures=6` |
| D10 | The nested negative-control tallies are placement-dependent too | `base=3/12` vs `base=4/12`, `r40=3/12` vs `4/12` |

The two live defeat families at `1f74646` are visible in the replayed selftest detail — the evidence the
round-42 J1/J2 must close:

```
selftest detail=I1 mutant=evidence-not-named   rejected=0 rc=0 payload=records=3,lines=14,graded=3,evidence=3/3,missing=0
selftest detail=I3 mutant=mangled-value-token  rejected=0 rc=0 payload=exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0
```

## 7. The round-42 receipt-production spec (landable as `ExecJ8Receipt.spec.txt`)

### 7.1 Constants

```
RECEIPT   = .ufo/waves/round-42/final-gates/all-gates.txt
SENTINEL  = all-gates v6
SUITE     = corpus/instruments/r42-closure.sh
CHECK_IDS = J1 J2 J3 J4 J5 J6 J7 J8 J9 J10 J11 J12 J13
N         = 13
```

`all-gates v6` is a **new** token. The r41→r42 change alters N (12→13), the id set (I→J) and the path, so
the grammar revision must be identifiable from line 1 alone; reusing `all-gates v1` would make an r41
receipt and an r42 receipt agree on their first line. The token names the contract, not the round, and is
compared byte-exactly. (D7: never carry a token forward across a grammar change.)

### 7.2 Line grammar — exactly 33 lines, one trailing newline, no blank line

```
all-gates v6
export-ref=<40 lowercase hex>
suite-sha256=<64 lowercase hex>
time-basis=ref-commit
run-utc=<YYYY-MM-DDTHH:MM:SSZ>
J<n> payload=<k=v[,k=v]*> closed=<0|1>                                   n = 1..13, in order
selftest case=J<n> mutants=<ok>/<n> positive=<pass|fail> payload-match=<1|0> verdict=<pass|fail>
                                                                         n = 1..13, in order
selftest cases=13 failures=<k>
closed=<k>/13 exit=<0|1>
```

| line | rule |
|---|---|
| 1 | byte-equal to `SENTINEL` |
| 2 | the judged head J. `grep -cE '^export-ref=[0-9a-f]{40}$'` = 1. Never Y — a commit cannot contain its own hash |
| 3 | `sha256sum` of `SUITE` **inside the export under test**. `grep -cE '^suite-sha256=[0-9a-f]{64}$'` = 1 |
| 4 | literal `time-basis=ref-commit`, `grep -cxF` = 1 |
| 5 | `TZ=UTC date -u -d "@$(git -C <lane> log -1 --format=%ct <line-2 ref>)" +%Y-%m-%dT%H:%M:%SZ`; must equal that instant and not exceed now+120 s |
| 6-18 | exactly thirteen, each id exactly once, in `CHECK_IDS` order; no space, `|` or newline inside a payload |
| 19-31 | exactly thirteen, each id exactly once, in `CHECK_IDS` order; `mutants=<ok>/<n>` with `n>=1` and `ok=n`; `positive=pass`; `payload-match=1`; `verdict=pass` |
| 32 | exactly `selftest cases=13 failures=0` |
| 33 | exactly `closed=13/13 exit=0` |

No path, no flag and no wall clock appears in any line.

### 7.3 The J8 payload — receipt integrity

One line, `k=v` pairs joined by `,`, in this order:

```
receipt=<0|1>,sentinel=<0|1>,ref=<40hex|empty>,digest=<0|1>,time-basis=<0|1>,run-utc=<0|1>,
not-future=<0|1>,header-lines=<n>,run-lines=<n>,selftest-lines=<n>,selftest-verdicts=<n>,
summary=<0|1>,closed-line=<0|1>,payload-match=<m>/12,ancestor=<0|1>,diff-clean=<0|1>,
diff-read=<ok|fail>,j8-fresh-match=<0|1>,cmp=<0|1>,j8-line=<0|1>
```

`closed=1` iff every one of: `receipt=1`, `sentinel=1`, `digest=1`, `time-basis=1`, `run-utc=1`,
`not-future=1`, `header-lines=5`, `run-lines=13`, `selftest-lines=13`, `selftest-verdicts=13`,
`summary=1`, `closed-line=1`, `payload-match=12/12`, `ancestor=1`, `diff-clean=1`, `diff-read=ok`,
`j8-fresh-match=1`, `cmp=1`, `j8-line=1`.

Definitions — all recomputed from the export, never read on trust:

- `header-lines` — how many of lines 1-5 equal their recomputed value. A count, so a partial forgery is
  visible instead of collapsing to a boolean.
- `payload-match=<m>/12` — how many of the twelve ids other than J8 have a recorded payload equal to the
  payload this run computes. One id at a time; a count-relative limb (one mismatch flagging every id) is the
  M-H9a defect and is REJECTED.
- `ancestor` / `diff-clean` / `diff-read` — `merge-base --is-ancestor <line-2 ref> <run ref>`;
  `git diff --name-only <line-2 ref> <run ref>` names nothing but `RECEIPT`; the diff command itself
  succeeded.
- `cmp` — the receipt, with **only** its own `J8 payload=` line and its own `selftest case=J8 ` line
  excluded, is byte-equal to a canonical rebuild. Every other line, including a duplicate, an extra or a
  reordered one, is compared.
- `j8-line` — the recorded `J8 payload=` value equals the canonical value this run computes, so the
  self-reference is closed (rebuilt from the receipt minus itself), not trusted.
- `j8-fresh-match` — J8 grades its forgery fixtures against fresh scratch files and never reads the receipt
  under test, so this comparison stays a function of the tree.

Uniqueness is a **separate** limb from `cmp`: require `grep -c '^J<n> payload='` = 1 and
`grep -c '^selftest case=J<n> '` = 1 for every id, so a duplicate J8 or J2 line cannot hide behind the
exclusion (D5).

### 7.4 Forgery classes — each graded, each with its own printed limb

The graded case `selftest_case_j8` runs the honest receipt as its positive and rejects, **each on its own
limb**, all of:

| class | fixture | limb the payload must name |
|---|---|---|
| missed control | the honest receipt | must NOT be flagged (`control=missed/missed`) |
| payload-contradicting | one `J<n> payload=` replaced with `zz-forged` | `payload-match=11/12` |
| future-dated | `run-utc=2999-01-01T00:00:00Z` | `not-future=0` |
| foreign-ref | a ref that **resolves** in the lane but is not an ancestor of the run ref | `ancestor=0` |
| nonexistent-ref | `export-ref=0000000000000000000000000000000000000000` | a limb distinct from foreign-ref (D4) |
| summary-only | the five header lines and `closed=13/13 exit=0` only | `run-lines=0` |
| tampered-payload-line | one `J<n>` line flipped to `closed=0` with a foreign payload | `closed-0>0` |
| digest-after-run | honest receipt with `suite-sha256=` replaced after the fact | `digest=0` |
| duplicate-run-line | honest receipt plus a second `J5 payload=` line | `runs-unique=0` |
| duplicate-selftest-line | honest receipt plus a second `selftest case=J5 ` line | `cases-unique=0` |
| extra-line | honest receipt plus an unrelated appended line | `cmp=0` |
| reordered-selftest-block | two graded lines swapped | `cmp=0` |

The positive fixture is built with **all-pass** graded lines and must not embed the other twelve cases' real
verdict lines (D3); otherwise the J8 case can pass only when the whole suite passes, which is not isolation.

### 7.5 Production sequence

**Step 1 — mint at J** (the tree that does not yet contain the receipt):

```
bash corpus/instruments/r42-closure.sh --export-ref <J> \
  --work <dir outside the lane> --scratch-root <dir> \
  --receipt-out <dir outside the lane>/all-gates.txt
```

Exit 0, `closed=13/13 exit=0`; then `cmp <all-gates.txt> <(same command's stdout)` clean. The write is
atomic: write `<path>.tmp`, rename once after the fixed point is reached, so a killed run cannot leave a
partial receipt (D6). `--receipt-out` must never name a path inside the lane; the L1 copies the finished
bytes in.

**Step 2 — commit exactly those bytes as Y**, and only that path:

```
git diff --name-only J Y     # prints: .ufo/waves/round-42/final-gates/all-gates.txt
```

**Step 3 — verify at Y.** A plain run over Y must reproduce the committed bytes exactly:

```
bash corpus/instruments/r42-closure.sh --export-ref <Y> --work <dir> --scratch-root <dir>
# exit 0, 33 lines, cmp against the committed receipt clean
```

This run is the artifact the report quotes. Line 2 still names J; at Y the ancestor, diff-clean and
`receipt=1` limbs become non-vacuous, which is what discharges the bootstrap.

**Step 4 — the report** quotes the Y run's 33 lines verbatim and the receipt's sha256.

### 7.6 Required invariants

1. **Placement invariance (closes D1/D2).** J5 evaluates a fixture root it materializes under `--work`; it
   must never scan the caller's `--scratch-root` or the export. A run with `--work` under `--scratch-root`
   and a run with `--work` elsewhere MUST print the same J5 payload, and a family *file* must be classified
   as a non-directory, not counted as an unreadable scratch entry. This is load-bearing: the claim's own
   counting command passes `--work <scratch>/work --scratch-root <scratch>`, which under r41's semantics
   yields 10/12 or 11/12, never 13/13.
2. **Tree-only payloads.** Every `J<n> payload=` is a function of the export and the named ref. No payload
   may contain a host path, a pid, a wall-clock value or a live-directory count.
3. **Nested controls are placement-invariant too (closes D10).** J9 re-invokes the suite on the base and
   r41-head exports; those nested payloads must not change with the outer placement, or the J9 payload and
   the J8 `payload-match` count will move between two runs over one tree.
4. **Re-run determinism.** Two plain runs over the same ref must be byte-identical regardless of
   `--work`, `--scratch-root` and `TMPDIR`.
5. **No red promotion.** A red run's receipt carries its red values and is never edited into a green one.
   The round-42 artifact must be green: `closed=13/13 exit=0`, `selftest cases=13 failures=0`.
6. **The claim's counting commands must be the exact commands that produced the artifact.** The teed
   selftest is `--selftest --export-ref <Y>`: thirteen `verdict=pass` lines and `selftest cases=13
   failures=0`, exit 0.

### 7.7 Acceptance commands

```
bash corpus/instruments/r42-closure.sh --export-ref <Y> --work <scratch>/work --scratch-root <scratch>
   -> 33 lines, closed=13/13 exit=0
bash corpus/instruments/r42-closure.sh --selftest --export-ref <Y> --work … --scratch-root …
   -> 13 x `selftest case=J<n> … positive=pass … verdict=pass`, `selftest cases=13 failures=0`, exit 0
bash corpus/instruments/r42-closure.sh --export-ref 5053a7f46de35784cff4b56756906e9014a38276 --work …
   -> closed<13/13 exit=1
bash corpus/instruments/r42-closure.sh --export-ref 1f7464612ac4c44e39886b82e812610d3c039b13 --work …
   -> closed<13/13 exit=1
bash corpus/instruments/r42-closure.sh
   -> exit 2, stdout empty
bash corpus/instruments/r42-closure.sh --export-ref deadbeef00000000000000000000000000000000
   -> `suite-ref-status=ref-not-found`, every J<n> line `payload=ref-not-found`, exit 1
```

## 8. Hygiene

- Tool installs/upgrades: none. Network fetches: none. `pacman` not run.
- Git: read-only only (`log`, `show`, `diff`, `merge-base`, `cat-file`, `ls-tree`, `rev-parse`). No add,
  commit, checkout, reset, stash, worktree, or jj command. Nothing written under the lane except this file.
- Suite runs: export mode only, `--work` under `$S` or `/var/tmp`, no `--receipt-out` into the lane.
- Disk guard green before every heavy step (`/fast/scratch/hyaku` 27 %).
- Scratch `$S` and `/var/tmp/kasegi-r42-rvr` removed before yield.

Report: .ufo/waves/round-42/wave1/RevengerReceipt.md
