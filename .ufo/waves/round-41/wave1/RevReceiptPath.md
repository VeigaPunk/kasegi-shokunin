# RevReceiptPath — how the round-40 receipt was actually produced, and where a dishonest L1 could stand

Seat: `RevReceiptPath`, round-41 build wave 1, leaf, receipt-only. No subagent, no lane writes, no git/jj
mutation, no tool installs, no network fetches. Scratch `S=/fast/scratch/hyaku/kasegi-r41/RevReceiptPath`
(removed before yield). All reads below are over the lane repo and read-only git; all runs of the round-40
suite are export-mode runs with `--work` under `$S` and no `--receipt-out` into the lane.

Refs used (verified to resolve):

```
B   (r40 base)              = a7af2ce63bce153757d39bf66b366a96caf30c13
J5  (r40 suite minted)      = 3074c7679d6f527ec3930d7748ccce1dbae4a58a
J7  (r40 judged head J)     = c7aea5ef97902f38289cbdc1cf267068876a62dd   19:32:37-03:00 = 22:32:37Z
Y   (r40 receipt ref)       = d0fe34d3fa27ff4de745a0c54c203fa8bf7141e5   19:33:07-03:00 = 22:33:07Z
Z   (r40 lane tip)          = b01cbd50d514bb7f8e154b40e0e608be3e6cf217
r39 head / r39 attempt-1    = 8371e7ac9f32cae5ed72f8c28205634603f836fa / 5006097a (v3 receipt)
```

## 1. The reconstructed production path

Six steps, in this order. Steps P2 and P4 are the ones that write or re-print receipts; both were
re-executed today and both reproduce the committed 16 bytes exactly.

**P0 — the suite is minted earlier in the round and never changes after J5.**
`corpus/instruments/r40-closure.sh` is byte-identical at J5, the wave-2 head, J7, Y, Z and the round-41
base (`sha256 bdbd18a3…897f1e` at every ref), so the digest in the receipt header is a property of the tree,
not of the run.

```
$ for r in 3074c76 8040db9 c7aea5e d0fe34d b01cbd50 b3b08b2; do
    printf '%s %s\n' "$r" "$(git show $r:corpus/instruments/r40-closure.sh | sha256sum | cut -d' ' -f1)"; done
3074c76 bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
8040db9 bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
c7aea5e bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
d0fe34d bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
b01cbd50 bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
b3b08b2 bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
```

(The list is exact output; the round-41 tip `b3b08b2` is the wave-1 spec commit, so the r40 bytes are still
the tip's bytes.)

**P1 — J7 is the tree that becomes J.** `c7aea5e` "refresh declared-blocks for wave-2 artifacts" (19:32:37-03:00).
It is the commit whose declared-blocks whole-tail declarations H9 validates (`declared=293,valid=293,tail=293`).

**P2 — mint at J7.** The receipt is *written* by `--receipt-out` at the judged head, not at Y:

```
bash corpus/instruments/r40-closure.sh --export-ref c7aea5ef97902f38289cbdc1cf267068876a62dd \
  --work <dir outside the lane> --scratch-root <scratch root> \
  --receipt-out .ufo/waves/round-40/final-gates/all-gates.txt
```

Re-executed today into my own scratch (same ref, different `--work`/`--scratch-root`), exit 0:

```
$ bash corpus/instruments/r40-closure.sh --export-ref c7aea5ef… --work $S/work \
      --scratch-root /fast/scratch/hyaku --receipt-out $S/mint-at-J7.txt
rc=0
all-gates v4
export-ref=c7aea5ef97902f38289cbdc1cf267068876a62dd
…
closed=10/10 exit=0
$ cmp $S/mint-at-J7.txt <(git show d0fe34d:.ufo/waves/round-40/final-gates/all-gates.txt)   # equal
$ cmp $S/mint-at-J7.txt $S/mint-at-J7.stdout                                                # equal
```

All three — mint file, mint stdout, committed bytes — hash to `7f55d540d6f41b5112d11bceb9e60e1d217308476b63ecd8c86c34e87ff1c79b`.

**P3 — commit that one path as Y.** `git diff --name-only J7 Y` =

```
.ufo/waves/round-40/final-gates/all-gates.txt
```

and nothing else. Y's committer instant is 30 s after J7's (22:33:07Z vs 22:32:37Z), so the receipt's
`run-utc=2026-10-26T22:32:37Z` is strictly in the past relative to its own commit.

**P4 — the count run at Y, which is what the report quotes.** `--export-ref d0fe34d…` (Y). Re-executed:

```
$ bash corpus/instruments/r40-closure.sh --export-ref d0fe34d3fa27ff4de745a0c54c203fa8bf7141e5 \
      --work $S/work --scratch-root /fast/scratch/hyaku
rc=0   … H7 payload=…,ref=c7aea5ef…,ancestor=1,diff-clean=1,diff-read=ok,payload-match=9,h7-line=1 closed=1
closed=10/10 exit=0
$ cmp <run stdout> <committed receipt>   # identical (sha 7f55d540…)
```

The run at Y re-emits the mint's header verbatim, including `export-ref=c7aea5e` and
`run-utc=2026-10-26T22:32:37Z`, because `assemble_transcript` reads `export-ref` back out of the receipt it
is judging and derives `run-utc` from *that* ref's committer instant. The report's C1 line
(`.ufo/reports/round-40/kasegi.md:32`) quotes this P4 command with
`--work /fast/scratch/hyaku/r40gates/w --scratch-root /fast/scratch/hyaku/r40gates`.

**P5 — the graded selftest at Y.** `--selftest --export-ref d0fe34d…` → `selftest cases=10 failures=0`,
exit 0 (69 lines). This transcript was **not** committed and is **not** in the receipt:

```
$ grep -c selftest <committed receipt>
0
```

**P6 — records committed after Y.** Z adds `LOG.md`, `SCORECARD.md`, `SHONEN.md` only
(`git diff --name-only Y Z`). They quote the P4 values *and* the P5 tally.

## 2. Falsifiers that pin the order

Each one excludes an alternative production path; all were run, not assumed.

| Alternative | Measurement | Result |
|---|---|---|
| the committed bytes are a plain (no `--receipt-out`) run at J7 | `--export-ref c7aea5e`, no receipt-out | `closed=9/10 exit=1`; `H7 payload=receipt=0,… closed=0` (fail-closed: the receipt is absent from J7's export). Discarded. |
| the committed bytes are a plain run at some earlier ref | J7 measured directly; older refs red more checks (base has no round-40 counters) | J7 `closed=9/10` (H7 red); the round's own H8 transcript records base `closed=3/10` and r39 head `closed=2/10`, all `exit=1`. Discarded. |
| the committed bytes are a plain run at Y | `--export-ref d0fe34d` | identical bytes, 10/10 — **consistent**, but a P4 run at Y cannot *create* the file it reads, so P4 alone cannot produce Y. |
| mint at J7 | `--receipt-out` at `c7aea5e` | identical bytes, 10/10, file == stdout. **This is the only path that writes the bytes while naming J7.** |
| mint at a cheap red ref and promote it | `--receipt-out` at B (`a7af2ce`) | `closed=3/10 exit=1`, file == stdout (`19b41b69…`). A red mint carries its own red flags; it cannot be promoted without editing bytes. |
| the header was re-stamped after the fact | `run-utc` vs committer instants | `run-utc=2026-10-26T22:32:37Z` = J7's `%ct` exactly; Y is +30 s. No gap to hide a wall-clock stamp. |

Counting and mint runs at the same ref are byte-identical (three runs today: the P4 run, the P2 mint file
and the P2 mint stdout, one hash). The graded selftest is the one exception (§4.2). So the receipt is a
*reproducible function of the tree and the ref*; it is not a witness of a particular invocation.

## 3. Mechanism, read from the committed bytes

`corpus/instruments/r40-closure.sh` (all line numbers in the J5..tip bytes):

- `run_suite_report` (985-1043) seeds the mint: `assemble_transcript '' > $WORK/h7-source.txt` (1007),
  `h7val=$(h7_inner "$WORK/h7-source.txt"),h7-line=1`, then writes the transcript with green defaults
  (1014) and points `H7_TARGET=$RECEIPT_OUT` (1016). The H7 line the run prints at J is therefore computed
  **from a file the run just wrote**, not from a committed artifact.
- H7 then re-derives everything it can: `receipt_shape` (440-482) recomputes sentinel, ref, digest,
  `time-basis`, `utc` (= `ref_utc(receipt's export-ref)`), `not-future`, header-lines, run-lines,
  body-lines, `closed-0`, `closed-line`; `h7_inner` (519-560) adds `ancestor` (`merge-base --is-ancestor`
  ref→run-ref), `diff-clean` (`git diff --name-only ref run-ref` must list nothing but the receipt) and
  `payload-match` against the nine other payloads; the line under test is never read while being rebuilt.
- The green window is real and one commit wide: at J a plain run is 9/10 (`receipt=0`); at Y it is 10/10
  because ref→run-ref diff is the receipt alone. At J the *mint* is 10/10 because `ref == run-ref`:
  `ancestor=1` and `diff-clean=1` hold vacuously on an empty diff.
- `H5`'s baseline at mint is synthetic: with no receipt in the export, `H5_SOURCE=$WORK/h5-source.txt`
  (997) = `assemble_transcript ''` (998) — a green, self-assembled pristine. `control=8/8` at J is measured
  against the suite's own fabrication.
- `H6` binds host state, not the invocation: top level only (`find … -mindepth 1 -maxdepth 1`, 771),
  case-sensitive prefix family `kasegi-r39*|kasegi-r40*` (779), and the payload prints only a count
  (`strays=0,read=ok`). My P2/P4 runs used a different `--work` and a different `--scratch-root` from the
  round's and printed the identical H6 payload.

**What the committed receipt therefore binds:** the tree (suite digest, 293 declarations, corrections, the
counters), the ref pair (J7 → Y with the receipt as the only delta), and the fact that some run of *these
bytes* printed these lines. **What it does not bind:** which invocation, which host, which work dir, and —
decisively — that any *second* observation was made at Y. P4 is reproducible but is not itself an artifact:
it exists in the report as a claimed command, and the committed receipt is P2's write.

## 4. Divergences between the designed contract and the landed bytes

1. **Atomic tee was required and not implemented.** `CritC1AntiSuite.md:72` (wave-1 critic, requirement 5)
   demanded "one invocation, one clock, atomic tee (tmp + rename) after run completion". The landed suite
   writes the destination directly (`printf … > "$RECEIPT_OUT"`, 1014 and 1033) and rewrites it inside an
   iteration loop capped at 4 passes (`[ "$iter" -ge 4 ] && break`, 1035). The final bytes do equal stdout
   (measured), but the file is written up to four times and a killed run can leave a partial receipt.
2. **The selftest transcript is excluded and is not byte-stable.** Two `--selftest` runs at Y today:
   `69` lines each, `sha256 d37914bf…` vs `f2e49c33…`; the only difference is line 33, a path-bearing
   diagnostic (`r40-closure.sh: line 770: cd: <work>/mut/H6-unreadable: Permission denied`). This is the
   structural reason the receipt carries no selftest line — and the structural reason D2 happened: the
   record still quotes a tally that no committed transcript holds.
3. **The forgery limb is count-relative.** `check_h5` (715-755) decides `forged=rejected` iff
   `payload_matches(forged) < $control` (732) — a strict decrease relative to whatever the pristine controls
   scored, plus two shape limbs (`not-future`, `run-lines=0 && closed-line=1`). It never says *which* value
   was compared, and at mint the pristine is `h5-source.txt`.
4. **A graded mutant is credited by a needle anywhere in the payload.** `st_neg` (1313-1325) accepts a
   mutant when `rc ≠ 0` **and** `grep -qF -- "$needle"` matches the payload string; a tampered-payload
   mutant therefore passes if any co-firing limb prints the same needle, and the aggregate
   `mutants=<ok>/<n>` (1327-1337) hides which sub-limb reded.
5. **The scratch scan is narrower than the leftover class it closes.** Top level only
   (`-maxdepth 1`), exact case prefix, no dot handling, no separator folding. A scan error does red the
   check (`[ "$read" = ok ]`, 793), so that limb is fail-closed; the coverage is the gap.

Points 3-5 are the r40→r41 hand-offs; 1-2 are the receipt-provenance hand-offs.

## 5. Intervention map — where a dishonest L1 stands, and which r41 limb stands there

Intervention points are stated as the step of §1 they corrupt. The "class" column names the verifier
finding the r40 spot-check recorded (`corpus/lessons/round-40-verifier-spotcheck.md` §5 D1-D6) or the
r39 R1/R2 class it descends from.

| # | Intervention point | What the L1 would do | Evidence it was reachable | r41 limb that catches it |
|---|---|---|---|---|
| A | P2 header | Write or re-stamp the five header lines instead of letting a run print them (the r39 attempt-1 shape: `5006097a` carries `run-utc=2026-10-26T21:35:00Z` while its commit is `20:12:12Z`, and `G2`/`G5` print `final-lane-commit=0`) | R1 class; per the r39 verifier (`round-39-verifier-spotcheck.md` §5 R1) that round's `make-receipt.sh` printed no `run-utc` line, so the committed stamp cannot have come from that run | **I2** — "the round-41 receipt at Y is the teed transcript of BOTH the suite run and the graded selftest at Y, with `time-basis=ref-commit` and run-utc equal to the ref's committer instant" |
| B | P2 ref choice | Tee a ref whose receipt already exists and is green (green-window arbitrage), or tee J and then commit a wider Y | At J the mint is 10/10 while a plain J run is 9/10 (measured); `diff-clean` is vacuous when `ref == run-ref` | **I2** again — the transcript must be produced *at Y*, so the mint's self-reference is no longer the only observation; plus retained `ancestor`/`diff-clean` |
| C | P2→P3 tally promotion | Edit a red mint into a green receipt, or paste a tally from several invocations | Red mint is evidence-honest (`closed=3/10`, file==stdout) but nothing forbids editing the file after the write; `--receipt-out` is not atomic (1014/1033) | **I8** — each forgery variant (payload-contradicting, future-dated, foreign-ref, nonexistent-ref, summary-only, tampered payload line) is INDEPENDENTLY flagged, not count-relative; **I9** — a tampered payload reds exactly its own case |
| D | P5 selftest | Quote `selftest cases=<n> failures=0` with no committed transcript | **Happened.** `SHONEN.md:219` at Z says "the final round-40 receipt values are recorded in `.ufo/waves/round-40/final-gates/all-gates.txt` … graded `selftest cases=10 failures=0`"; `grep -c selftest` over that receipt = `0`. D2 | **I2** — the receipt must carry the graded selftest transcript too, which forces the §4.2 nondeterminism to be normalised before it can be teed |
| E | P4 count run | Report a 10/10 count run that nobody can check (or a run with different args than reported) | The transcript is byte-invariant to the invocation: the committed receipt (run with `--work /fast/scratch/hyaku/r40gates/w --scratch-root /fast/scratch/hyaku/r40gates` per the report) equals my run today with different `--work`/`--scratch-root` | **I2** (the teed artifact, not the claim, is the object) + **I6** (scratch scan recursive/case/separator-insensitive, dot-inclusive, fail-closed) |
| F | P5 grading | Let a graded case pass because a *different* limb reded the mutant | `st_neg` credits on a needle anywhere in the payload (1313-1325); `mutants=k/n` aggregates | **I9** — "the graded selftest isolates the payload-value comparison per case — a tampered payload reds exactly its own case" |
| G | P2/P4 value limbs | Rely on substring value matching (`closed=7/80` reads as `closed=7/8`; `failures=10` as `failures=1`) | Round-40 wave-2 T2 delivered both fixtures | **I3** — token-boundary value matching, the two substring fixtures rejected |
| H | P6 corrections/criteria | Put the `Correction (round 41)` line or a QUALITY criterion inside a code fence so a line-anchored grep still counts it | r40 wave-2 T3/T4 | **I4** — fenced lines do not satisfy line-anchored limbs, fence state CLOSED at EOF |
| I | P3/P6 declared blocks | Point a declaration at a symlink that escapes the export root | r40 wave-2 T7 | **I5** — declared-block paths readlink-canonicalised under the export root |
| J | P0/P6 registry | Add a mention-only SKILL.md row, or a row broken out of its table by a blank line | r40 wave-2 T13, and D6 (L1120 separator, blank L1121, row L1122) | **I7** — the registry row must be a well-formed table row with structured cells |
| K | P6 records | Grade a claim verified while its own counter/fixtures show the defect (**D1**: SCORECARD at Z reads `4 (held; verified)` while H2/H3/H6/H9/H1/H8 have committed fixtures that pass with the defect present) and leave the earlier round's 8/8 standing (**R2**) | D1, R2 | **I1** — `Correction (round 41)` lines in SCORECARD/LOG/SHONEN grade r40 C1 NOT verified on the frozen counter and name the firing evidence (RevC1Counters.defeats.txt, CritKillRule.md, MutH6H10.md); **I2** binds the record's quoted values to the teed transcript |
| L | P1/P2 negative controls | Have the pristine suite accept a leaf-capped green base export | `MutH6H10.md` §Defect D2 as read by the spot-check ("H8's acceptance predicate is unkillable") | **I10** — real numeric comparison in the negative-control predicate; the accepting mutation is killed by the graded selftest |
| M | P2 escape states | Survive via one of the seven committed CritKillRule escapes | `wave2/CritKillRule.md` | **I11** — each of the seven states reds the limb it escapes |

Rows A-D and K are the R1/R2 class proper (false receipt provenance; records contradicting the artifact).
Rows F-I, L, M are the wave-2 attack class that made the r40 kill rule fire.

## 6. What I2 will require of the round-41 receipt (measured consequence, for the L1)

I2 is satisfiable only if three things hold, and the first is not free:

1. The graded selftest's stdout must be byte-stable across runs at Y. In two runs today it is not: the only
   nondeterminism is the `cd: …: Permission denied` diagnostic at `r40-closure.sh:770` (line 33 of the
   transcript; both runs 69 lines, `d37914bf…` vs `f2e49c33…`). Either that diagnostic is
   normalised/removed in `r41-closure.sh`, or the teed selftest transcript cannot be byte-compared and I2
   degenerates into a quote — the exact D2 shape.
2. The teed selftest must run at the *same* ref as the suite run (Y), and the receipt must carry both
   blocks with a delimiter that the parser counts (`selftest cases=12 failures=0` present exactly once).
3. The receipt is still written at J (a commit cannot contain its own hash), so I2's "teed transcript at Y"
   must be produced by the P4 form — a run over Y whose stdout is captured — and that capture, not the J
   mint, has to be the committed bytes. At J an I2-shaped receipt cannot exist by construction.

## 7. Confidence

- **Production path P0-P4: high.** Every step is either byte-checked (P0 digest, P2 mint equality, P4
  equality, P3 one-path delta) or arithmetically forced (P2's `run-utc` = J7's `%ct`; Y = J7 + receipt; a
  plain J7 run is 9/10 so the bytes cannot come from one). The only unresolvable residual is that
  byte-identity cannot distinguish "minted at P2, then committed" from "minted at P2 after Y existed" —
  irrelevant to the bytes, relevant to the claim that an observation at Y occurred.
- **P5/P6: high** (no selftest transcript exists in any committed file; Z adds records only).
- **Intervention map A-M: high for the mapping, medium for exhaustiveness.** The limbs quoted are the
  frozen r41 claims' text; they do not exist as bytes yet (no `corpus/instruments/r41-closure.sh` at the
  round-41 base or tip today), so each mapping is a claim-to-claim binding, not a measured rejection.
- **Inference (not measured):** that the round's L1 in fact ran P2 with `--receipt-out` rather than hand
  assembling bytes that happen to be identical. The header values are fully determined by `export-ref`
  (`receipt_shape`: header-lines 1-5 are all recomputed), so a hand assembly is possible in principle; it
  is not distinguished by the committed evidence.

Depth contribution of this seat: I2 stops being a sentence and becomes three measured requirements (§6),
the first of which the landed r40 bytes cannot meet without a normalisation they do not contain. The
intervention map (§5) is the list of places a round-41 receipt can still lie, each tied to the limb that
must red it.

## 8. Hygiene

- Tool installs/upgrades: none (no pacman — paused host-wide; no uv/npx needed). Network fetches: none.
- Git: read-only only (`log`, `show`, `diff`, `cat-file`, `rev-list`, `grep`, `status`, `ls-tree`). No add,
  commit, checkout, reset, stash, worktree, or jj command. Lane `git status --porcelain` shows only other
  seats' untracked round-41 files; nothing of mine outside this receipt.
- Suite runs: export mode only, `--work` under `$S`, `--receipt-out` written to `$S` only. No file under
  the lane was written by any run.
- Disk guard green before every heavy step (`/fast/scratch/hyaku` 25%, 604.9G free).
- Scratch `$S` removed before yield.

Report: .ufo/waves/round-41/wave1/RevReceiptPath.md
