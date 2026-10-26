# ExecH7Determinism — H7 determinism probe (kasegi round 40, wave 1)

Seat: leaf executor, receipt-only, no lane writes. Suite under test is the wave-1 deliverable
`.ufo/waves/round-40/wave1/ExecSuiteBuild.r40-closure.sh` — **final bytes sha256
`bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e`, 1734 lines, 71895 bytes**
(supersedes `1da1d76d6df352618104d1ce55e3b1d51d16703c5dac8beef738db3a3a1ba6f6`, 1713 lines, which I
measured first; its two receipt defects are recorded below and both are fixed in the final bytes).
Lane working tree was never written; every run outside the lane used a scratch clone
(`git rev-parse --show-toplevel` asserted equal to the clone dir before any fixture commit, fixture
identity `r40fixture <r40@fixture.invalid>` only), scratch under
`/fast/scratch/hyaku/kasegi-r40/ExecH7Determinism`. No tool installed, no network fetch.

## Verdict

| property the claim's H7 needs | measured | result |
|---|---|---|
| two runs of the suite produce the same bytes (distinct `TMPDIR`, distinct `--work`, distinct `--scratch-root`) | freeze ref `5e985b7` (×2), red ref `a7af2ce` (×2), r39 head `8371e7ac` (×2), green J (×2); the single green-Y run prints the same bytes as both J runs | **byte-identical every measured pair** |
| the receipt is the run's own transcript (re-run over J reproduces it) | green J: `--receipt-out` file `cmp`-equal to stdout | **pass** (`c874bcf4…`, 16 lines) |
| committed receipt at Y reproduced by a fresh run at Y, modulo nothing | `cmp` committed vs fresh: equal; H7 `payload-match=9,h7-line=1` | **pass** |
| fresh mint (`--receipt-out`) at Y equals the committed `all-gates.txt` | `cmp`: equal | **pass** |
| run-utc printed by the run, not future-dated, deterministic | `run-utc=2026-10-26T21:45:48Z` = committer instant of the receipt's `export-ref` J; identical on every re-run | **pass** |
| tampered committed receipt rejected on the counting path | H3 payload `rows=1`→`rows=9` at Yt: `H5 control=7/8`, `H7 payload-match=7,h7-line=0`, `closed=8/10 exit=1` | **pass** |
| red mint cannot be promoted | base + `--receipt-out`: file `cmp`-equal to stdout, `closed=3/10 exit=1`, `H7 …closed-0=7,closed-line=0` | **pass** |
| negative controls | base `closed=3/10 exit=1`; r39 head `closed=2/10 exit=1`; plain run exit 2 | **pass** |

One residual nondeterminism remains, **outside the receipt**: the `--selftest` transcript differs by
exactly one line between two runs (a path-bearing `cd:` diagnostic at suite line 770). One-line
normalization delivered below. The run transcript / receipt itself has no residual nondeterminism.

## Measurements (commands and raw output)

### 1. Two runs at the seat's probe ref, separate work dirs

```
S=/fast/scratch/hyaku/kasegi-r40/ExecH7Determinism
for n in 1 2; do TMPDIR=$S/run$n bash r40b.sh --export-ref 5e985b74075dd3813a63d7750966bf8abf693465 \
   --lane $S/jcl3 --work $S/run$n/work --scratch-root $S/run$n/sroot --receipt-out $S/run$n/receipt.txt \
   > $S/run$n/out 2>$S/run$n/err; done
```
```
run1 rc=1 outsha=f43361c2c3191a52e3bea31309640f45432d5c76fe1dc22fc61a5d044c2cb328 recsha=f43361c2c3…
run2 rc=1 outsha=f43361c2c3191a52e3bea31309640f45432d5c76fe1dc22fc61a5d044c2cb328 recsha=f43361c2c3…
diff: RUN-IDENTICAL, RECEIPT-IDENTICAL; tail: closed=3/10 exit=1
```
`--lane` names the scratch clone because the suite is not yet committed in the lane; the exported
tree is the same commit object, so the export bytes are identical. Re-run of the counting form
without `--receipt-out` (default `--lane`, two TMPDIRs) is also identical:
`sha256=4649d8ca7d77a74b5eeb5b27366543062d24918ef9e30b5c6672e34f756c44b2` twice.

### 2. Green J (clone = freeze + lane worktree snapshot + `declared-blocks.txt`) and Y = J + receipt

```
J=a90e36ded53fb17ba2011ed0c0614c5fa0a13829   (tree of the lane worktree at probe time)
run-utc=2026-10-26T21:45:48Z                 (= git log -1 --format=%ct J, TZ=UTC)
closed=10/10 exit=0 ; H4 s056=1,s058=1,s059=1 ; H9 declared=2,valid=2,tail=2,pure=1
j1/j2 outsha=recsha=c874bcf49aa49ef815e84a0d4979b3ebcc1a50968aeaf2bc0ec1bec3c6561b07
STDOUT-IDENTICAL / RECEIPT-IDENTICAL / RECEIPT-IS-STDOUT
Y=d1656db8b8a9f080063e64b67b3afd1cef30bbfa
y outsha=recsha=c874bcf4…  Y-REPRODUCES-RECEIPT  Y-MINT-EQUAL
```
The header names J (`export-ref=a90e36de…`) while the run ref is Y, so no commit contains its own
hash; `run-utc` is J's committer instant on the Y run as well — printed by the run, in the past,
and identical on every re-run.

### 3. Tampered-receipt control (counting path, no `--receipt-out`)

Committed receipt at Yt with `H3 payload=mentions=1,rows=9` (run computes `rows=1`):
```
H5 payload=source=1,control=7/8,utc=1,forged-payload=accepted,future-dated=rejected,summary-only=rejected closed=0
H7 payload=…,payload-match=7,h7-line=0 closed=0
closed=8/10 exit=1
```
The cascade is correct: the tampered H3 row and the resulting H5 row fail the payload binding.

### 4. Negative controls and refusal, final bytes

```
--export-ref a7af2ce63bce153757d39bf66b366a96caf30c13 -> rc=1 closed=3/10 exit=1
   two runs, distinct TMPDIR/work/scratch-root: sha=59a00629b368fe1f2ec1cbddc22a8542368a1bb73b94f0fbc225c82a878b29e5 (both)
--export-ref 8371e7ac9f32cae5ed72f8c28205634603f836fa -> rc=1 closed=2/10 exit=1
   two runs: sha=705725213b28d9325de4196ac2dee99916a774466b08b8839d94e6ced5889d26 (both)
no arguments -> "refusing to run against the live worktree: this suite is export-mode only." rc=2
```

### 5. `--selftest --export-ref Y` (two runs, distinct TMPDIR/work/scratch-root)

```
s1 rc=0 lines=69 sha=91167b95f8c2dcb898106294a73bfe51b6c7b19f5c31198d724b63dd154e074e
s2 rc=0 lines=69 sha=241488c227112037779b2355857b8a617870132ecf2948db669304c89b1bc7c6
selftest case=H1..H10 positive=pass verdict=pass (10 graded lines); selftest cases=10 failures=0
```
Exactly one differing line between the two runs:
```
-…/r40-closure.sh: line 770: cd: …/s1/work/mut/H6-unreadable: Permission denied
+…/r40-closure.sh: line 770: cd: …/s2/work/mut/H6-unreadable: Permission denied
```
Source: `check_h6`, line 770 — `realroot=$( cd "$root" && pwd -P )`. The sibling `cd` calls in the
same file already suppress stderr (`realw=`, `r=`); this one does not, so the *selftest* fixture for
`unreadable-scratch-root` writes the per-run work path into the transcript. The fail-closed logic is
unaffected (the `||` branch still runs on a failed `cd`). Not part of the receipt (the v4 receipt is
the run block only, 16 lines), but it is the only non-reproducible line I found anywhere in the
suite, and the same class was the r39 defect (`corpus/instruments/r39-closure.sh` lines 530/555/889/893 and
its committed receipt lines 14/59/60/63/65/66 carry absolute `tolerated=`/`cd:`/`find:` paths).

Measured baseline for that claim (r39 suite, this host, before the r40 suite existed): two
`--selftest` runs at `5e985b7` with distinct work dirs differed in 8 diff lines (4 changed lines: two `tolerated=` paths,
one `cd:` diagnostic, one `find:` diagnostic); after applying the same normalizations to a scratch
copy, 0 lines differed. The r40 run transcript already has none of these.

### 6. Live-state coupling (H6), by design — operational constraint for the counting run

H6's payload is the live scratch scan, and H5/H7 bind the receipt's payload rows to it, so one
stray entry cascades:
```
empty sibling kasegi-r40 under the scratch root -> H6 strays=1, H5 control=6/8,
   H7 payload-match=6,h7-line=0, closed=7/10 exit=1   (at an otherwise green Y)
--work inside the family entry (…/kasegi-r40/<seat>/work) -> H6 strays=0, closed=10/10 exit=0
default root, --work outside any kasegi-r39*/r40* entry, with /fast/scratch/hyaku/kasegi-r40 present
   -> H6 strays=1, closed=7/10 exit=1
```
Consequence for the L1: the counting form `bash corpus/instruments/r40-closure.sh --export-ref <Y>`
takes no `--work`, so its auto work dir lands under the ambient `TMPDIR` (outside the family) and
**any** `kasegi-r39*`/`kasegi-r40*` entry under `/fast/scratch/hyaku` reds H6 — including an *empty*
`kasegi-r40/` parent left after the seats remove their own subdirectories. Remove the parent (or set
`TMPDIR` inside it) before the final Y run. This seat's own scratch is removed at hand-off.

## Deliverable

One-line normalization of the remaining non-reproducible selftest line, applied to the landable suite
(`corpus/instruments/r40-closure.sh` = the wave-1 file). 11 lines, sha256
`1f50debd7833676b0f5cc42ce1552d368e30029c4dbffca389c1fd2dd0acd2f7`.

## DELIVERABLE
```diff
--- a/corpus/instruments/r40-closure.sh
+++ b/corpus/instruments/r40-closure.sh
@@ -767,7 +767,7 @@
   fi
   realw=$( cd "$WORK" 2>/dev/null && pwd -P ) || { printf 'strays=0,read=fail'; return 1; }
   if [ -d "$root" ]; then
-    realroot=$( cd "$root" && pwd -P ) || { printf 'strays=0,read=fail'; return 1; }
+    realroot=$( cd "$root" 2>/dev/null && pwd -P ) || { printf 'strays=0,read=fail'; return 1; }
     if ! out=$(find "$realroot" -mindepth 1 -maxdepth 1 -print 2>/dev/null); then
       printf 'strays=0,read=fail'
       return 1
```

## Defects found and closed during the probe (all three were in `1da1d76d…`; all three are addressed in `bdbd18a3…`)

1. **Red mint wrote a green receipt.** `assemble_transcript` defaulted to `mode=green`, so
   `--receipt-out` at a red ref wrote `closed=1` on failing checks and a `closed=10/10 exit=0` tally.
   Measured at a worktree-snapshot J that ran `closed=8/10 exit=1` (H4, H9 red): the written file
   carried `H4 …closed=1`, `H9 …closed=1`, `closed=10/10 exit=0` — 6 lines that the run did not
   print; and at the Y built from it the committed receipt differed from the fresh run by those 6
   lines while H7 still read `payload-match=9,h7-line=1 closed=1` (payload-match compares `payload=`
   fields only, never a line's `closed=` flag or the tally). That contradicts the H7 wording and the
   QUALITY `R37` criterion landed this round ("no edited tally and no value the run did not print").
   Reported to `ExecSuiteBuild-3`; the final bytes iterate the transcript to a fixed point and, at
   base, `cmp` of stdout vs `--receipt-out` file is equal with `closed=3/10 exit=1` and
   `H7 …closed-0=7,closed-line=0` — re-measured above. Scope note: this could not fake the claim's
   counting commands (the run itself still prints the real tally); it faked only the receipt.
2. **`--receipt-out` at Y verified its own new mint, not the committed receipt** (`H7_TARGET` is
   overridden by `RECEIPT_OUT`). My first tamper control passed for that reason. The counting path
   has no `--receipt-out` and rejects the tampered receipt correctly (measurement 3). Not a counting
   defect; recorded so nobody re-runs the mint path as if it were the verification.
3. **H4 locator clause** rejected the landed S056 row's `raw HTML L1146` locator (`s056=0` on the real
   lane text). Reported; final bytes accept `L<NN>`, and the same run now prints
   `H4 s056=1,s058=1,s059=1`.

## Risks / open items for integration

- H6 live coupling (measurement 6) is the only way an otherwise green Y reads `closed=7/10`; it is a
  scratch-state precondition, not nondeterminism. Clean `/fast/scratch/hyaku` of
  `kasegi-r39*`/`kasegi-r40*` entries (parent included) before the final counting run.
- The receipt must be minted from the **landed** suite bytes: H1/H7 compare `suite-sha256` with the
  export's own copy, so a receipt minted from a wave-1 path or a later-revised file reds `digest`.
- Mint only after the run itself prints `closed=10/10 exit=0`; the fixed build now refuses to fake
  it, but a red mint still produces an honest red receipt that must not be committed as Y.
- `run-utc` semantics are now `time-basis=ref-commit`; any record that describes it as wall clock at
  execution should be read as "the run's own printed stamp, the ref's committer instant".

## Evidence retained

Probe scripts and logs lived under `/fast/scratch/hyaku/kasegi-r40/ExecH7Determinism` (`probe.sh`,
`hazards.sh`, `green.sh`, `green2.sh`, `green3.sh`, `ysim.sh`; run logs under `run1/ run2/ p1/ p2/
g/ g2/ h/ s1/ s2/ live/ reallane/ neg/ neg2/`). That directory is removed before yield per seat
protocol. The shared parent `/fast/scratch/hyaku/kasegi-r40` was empty at hand-off and is removed too,
so `/fast/scratch/hyaku` now holds zero `kasegi-r39*`/`kasegi-r40*` entries (H6 measures `strays=0`);
if a later seat recreates a family entry, the L1 must clear it before the final run — see the H6 note.
No file in the lane, the fleet root, `shokuknow`, or any sibling repo was written; no git mutation was
issued outside the scratch clone.
