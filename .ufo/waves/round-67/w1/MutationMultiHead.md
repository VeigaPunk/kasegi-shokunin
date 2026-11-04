# MutationMultiHead — R67 v1 wave, mutant battery for the per-head SIGPIPE input-count rule

Axes: depth:verifiability, coverage. Seat: mutation-tester (leaf, no dispatch).

## Identity of what was tested

| object | path | sha256 | bytes |
|---|---|---|---|
| candidate gate (frozen by ExecMultiHeadGate) | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ExecMultiHeadGate/figure-audit.py` | `d5e8fcae6f1523d0ffbe8f21540fde839a24abbe98958378e54da284eec38c05` | 34750 |
| base production gate | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py` | `51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac` | 30283 |
| battery (this seat) | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/MutationMultiHead/multihead-mutbat.py` | `937f8677fb6276635501ac8b6fa6cbe631e7d5ef9dc3b8a2e1cc0c7f9b66e233` | 17582 |

ExecMultiHeadGate confirmed no further candidate change ("d5e8fcae… stands"). All verdicts below are
pinned to those bytes; two consecutive full runs produced identical verdict lines.

## What the battery does

`multihead-mutbat.py --instrument <gate> --work <dir> [--collector <probes.py>]` copies the candidate
into scratch, applies **one** text replacement at the smallest behaviour-bearing point per limb
(anchors must match exactly once; otherwise the limb is `invalid` and never counted), then runs the
same detectors on pristine and mutated bytes:

* the candidate's own `--selftest` (must be 0 on pristine, 1 with `selftest cases=` on a kill);
* 14 named ledger probes built on deterministic 4 MiB fixtures (`big.txt`/`other.txt`/`xlines.txt`,
  plus `small.txt` and dash-named `-a`/`-c`), each asserted as an exact ok value or an exact
  stale reason;
* three equivalence controls that must reproduce the pristine result exactly.

A baseline failure is reported as `invalid by=pristine-baseline-not-satisfied` for every limb — never
as a kill. Exit is 0 iff `failures==0 and survivors==0 and killed==total`.

## Verdicts (candidate `d5e8fcae`)

```
MUTANT L1-grep-base-1-to-0 killed by=P8-grep-single-sigpipe selftest_exit=1
MUTANT L2-grep-base-1-to-2 killed by=P4-grep-two-existing selftest_exit=1
MUTANT L3-catcutwc-base-0-to-1 killed by=P14-wc-two-existing selftest_exit=0
MUTANT L4-drop-dashdash killed by=P11-dashdash-leading selftest_exit=0
MUTANT L5-count-options-as-operands killed by=P5-cut-single selftest_exit=0
MUTANT L6-unknown-head-stale killed by=P12-unknown-head-sigpipe selftest_exit=1
MUTANT L7-headblind-sigpipe-exempt killed by=P1-cut-multi-missing selftest_exit=1
MUTANT E1-trailing-space-control equivalent by=trailing-space control: two bytes added, no behavioural change
MUTANT E2-le-one-vs-lt-two equivalent by=len(x) <= 1 and len(x) < 2 are the same predicate over integers
MUTANT E3-sigpipe-constant equivalent by=signal.SIGPIPE is 13 on this host and the status is negated
MUTBAT killed=7/7 survivors=0 equivalents=3 invalid_rejected=0 failures=0
MUTBAT killed=7 survivors=0
```

Exit 0, wall 46.7 s (run 1) and 46.1 s (run 2), verdict lines identical.

### Limb by limb (mutation → detector → observed deviation)

1. **L1 grep base 1→0** (`SIGPIPE_REQUIRED_NONFILE_ARGS = {"grep": 0}`). `grep x big.txt | head -n 1`
   (native stage0 −13 on 30/30) becomes stale `derive-upstream-signal-13` because the pattern is no
   longer skipped; the candidate exempts it. Also flips P11. Killed by **P8** and by the candidate's
   own `upstream-grep-single-pattern-file-sigpipe-benign` case.
2. **L2 grep base 1→2** (`{"grep": 2}`). `grep x xlines.txt big.txt | head -n 1` becomes exempt
   (count 3−2 = 1) and reports a value instead of stale; the candidate stales at count 2. Killed by
   **P4** (P3 also flips). Killed by the candidate's `upstream-grep-multi-missing-stale` case too.
3. **L3 cat/cut/wc base 0→1** (`{"grep": 1, "cat": 1, "cut": 1, "wc": 1}`). `wc small.txt big.txt |
   head -n 1` (native −13 on 30/30) becomes exempt because the first operand is skipped; the
   candidate stales at count 2. Killed by **P14**. `--selftest` stays green (see gap G1). The `cat`
   entry of this limb is behaviourally dead (cat returns through `cat_sigpipe_exempt` first): P9/P10
   are unchanged under the mutant, evidence that the mutation is the three-entry dict only.
4. **L4 drop the leading-`--` branch** in `sigpipe_input_count` (`if tokens and tokens[0] == "--":`
   → `pass`). `grep -- x big.txt | head -n 1` (native −13 on 30/30) turns stale: the required-pattern
   skip eats `--` and the pattern is then counted as an operand (2). Killed by **P11**.
   `--selftest` stays green (gap G2).
5. **L5 count option tokens as operands** (`return len(tokens)`). `cut -f1 -d: big.txt | head -n 1`
   (native −13, correctly exempt) becomes stale because `-f1`/`-d:` are counted. Killed by **P5**.
   `--selftest` stays green (gap G3).
6. **L6 unknown head stale** (`return True` for heads outside `READ_ONLY_HEADS`).
   `python3 corpus/instruments/pipe.py | head -n 1 | wc -l` (SIGPIPE, unknown head, benign) becomes
   stale. Killed by **P12** and by the candidate's `upstream-sigpipe-nonfinal-benign` case.
7. **L7 head-blind SIGPIPE exemption** (whole `cat`/`READ_ONLY_HEADS`/unknown branch → `return
   False`, the base rule). P1/P2/P3/P4/P10/P14 all go green with a value; killed by **P1**, and by the
   candidate's `upstream-cut-multi-missing-sigpipe-stale` and `upstream-cat-multi-missing-sigpipe-stale`
   cases. This is the C1 defect itself re-injected; the candidate is not equivalent to base.

## Equivalents (recorded, never counted)

* **E1 trailing-space control** — two spaces appended to the `return sum(...)` line. No behavioural change.
* **E2 `<= 1` → `< 2`** — same predicate over integers (`cat_sigpipe_exempt`).
* **E3 `-signal.SIGPIPE` → `-13`** — `signal.SIGPIPE` is 13 here and the status is negated.

All three reproduce `--selftest` 0/71 and all 14 probe expectations exactly.

## Paired run against base (`51f299af`) — honestly red

`MUTBAT killed=0/7 survivors=0 equivalents=0 invalid_rejected=10 failures=5`, exit 1. Baseline
failures are exactly the C1 false greens: P1 (`cut` multi-missing), P2 (`wc` multi-missing), P3
(`grep` multi-missing), P4 (`grep` two existing) and P14 (`wc` two existing) all returned a **value**
instead of the required `derive-upstream-signal-13`, while P5–P9, P10–P13 passed and base's own
`--selftest` was 67/0. No mutant was counted as killed on base.

## Existing production mutbat against the candidate

`corpus/instruments/figure-audit-mutbat.py --instrument <candidate>`:
`PRISTINE selftest_exit=0`, control held, `mutbat killed=5/5 survivors=0 invalid=0 controls=pass`,
exit 0. (m4, m6, m7, m8, m9 all killed by selftest; `gate-anchor='return parts[0] in READ_ONLY_HEADS'`
sites=1.)

## Coverage findings (the point of the exercise)

* **G1** The 71-case selftest does not kill L3: no counted case exercises a SIGPIPE'd multi-input
  `wc` whose first token is an operand (`wc small.txt big.txt`). The candidate's `wc` case accepts
  either reason on the *missing*-file shape, which also cannot distinguish base count 0 from 1
  because `-l` is the first token and absorbs the skip.
* **G2** The leading-`--` branch is observable **only through grep**. For every other read-only head
  the dropped token is `--`, which is option-shaped and never counted, so dropping the branch is a
  no-op there (L4's only deviation is P11). It is not dead code overall, but it is dead for
  cut/wc/sort/sha256sum/head/tail/ls/tr.
* **G3** There is no single-input SIGPIPE-green counted case for `cut`/`wc`/`sort`/`sha256sum`; only
  grep was added. A mutation that counts option tokens as operands (L5) makes single-input `cut`
  stale and the selftest stays green; only the battery catches it.
* **G4** `wc -l big.txt missing.txt` measured −13 on 25/25 gate-level repeats and 30/30 native, but
  one exit-1 face was observed under load: in a run against the pre-freeze candidate bytes (978c98a2),
  L7's P2 deviation read `('stale', 'derive-upstream-exit-1')` while the pristine baseline of the same
  run read `-13`. The battery therefore accepts either reason for P2; the candidate's either-reason
  case is the right shape. P14 stays strict (`wc small.txt big.txt`, both files exist, 25/25 −13) and
  is the deterministic L3 killer.
* **G5** L1/L2 also flip P3/P11, i.e. the pattern-skip budget is load-bearing for four probe shapes;
  a one-case pin for grep's base would not be enough.

## Measurements (receipts)

`receipts/native-statuses.txt` — 30 repeats per pipeline, `set -o pipefail`: multi-input
cut/wc/grep −13 (141), single-input `cut`/`grep x big.txt`/`cat`/`grep -- x big.txt` −13 but exempt,
`wc -l big.txt`/`sha256sum big.txt` 0, `head -n 5 big.txt missing.txt` 1, python `pipe.py` −13.
`receipts/mutbat-candidate-run1.log`, `…run2.log`, `receipts/mutbat-base-paired.log`,
`receipts/prod-figure-audit-mutbat.log`, `receipts/candidate-selftest.log` (71 cases, 0 failures,
including the four R67 cases), `receipts/mutant-diffs.txt` (exact unified diff and mutant sha256 per
limb/equivalence), `receipts/candidate-sha.txt`.

## Honesty and bounds

* No sandbox claim: the battery executes the selected instrument's selftest and probes; the fixtures
  are 4 MiB files in the battery's own work dir, removed on exit unless `--keep`.
* Every probe is a ledger derive run through the candidate gate itself, not a reimplementation of
  its rule; native statuses were measured, never assumed.
* One invalid-mutant path was exercised only in the base paired run (baseline not satisfied); no
  anchor/syntax invalidation occurred against `d5e8fcae`.
* No production byte, ledger, SOURCES/README/knowledge, SCORECARD/SKILL/PROVINCE/LOG, git/jj state or
  sibling lane was touched. Scratch `/fast/scratch/hyaku/kasegi-r67/MutationMultiHead/` was removed
  after the receipts were copied here.
* No tool install or upgrade was needed.

## Residuals (named, not repaired here — L1's call)

1. Counted-suite extension for G1/G2/G3 (single-input cut/wc/sort/sha256sum SIGPIPE-green cases, a
   `wc` two-operand case with the operand first, and a `grep -- pattern file` case).
2. `--` handling for non-grep heads remains unobservable; if the intent is to honour `--` before
   dash-named operands, the count needs an "after `--` everything is an operand" state, not just a
   token drop.
3. `wc` multi-input SIGPIPE status is timing-dependent on this host; any counted case must keep the
   either-reason shape.
