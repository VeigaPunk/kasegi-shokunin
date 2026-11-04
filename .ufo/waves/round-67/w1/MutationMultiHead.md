# MutationMultiHead — R67 v1 wave, mutant battery for the per-head SIGPIPE input-count rule

Axes: depth:verifiability, coverage. Seat: mutation-tester (leaf, no dispatch).

## What was tested (exact bytes)

| object | path | sha256 |
|---|---|---|
| candidate gate (L1 landed it as production) | `.ufo/waves/round-67/w1/ExecMultiHeadGate/figure-audit.py` (== `corpus/instruments/figure-audit.py` after landing) | `8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247` (36939 bytes, 73 selftest cases, 0 failures) |
| base gate (recovered read-only from lane rev `8e2a8fe…`) | `git show 8e2a8fe8eb92d7c824902a4b70aab027a9aacee0:corpus/instruments/figure-audit.py` → scratch | `51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac` (30283 bytes, 67 cases) |
| shared collector | `.ufo/waves/round-67/w1/ExecMultiHeadProbes/probes.py` | `d56a1437cdd1463d99e5f7f9c15877d855c836bad8236efd0cef0afc370ae34a` |
| battery at L1's freeze (superseded by the on-disk row below) | `.ufo/waves/round-67/w1/MutationMultiHead/multihead-mutbat.py` | `547b4ce26e54ebdefc48cfcfb91af91b1e74b0623c39bd109579fe13b11f9a3d` |

| **battery as it stands on disk now** | `.ufo/waves/round-67/w1/MutationMultiHead/multihead-mutbat.py` (537 lines) | `ea31d43929529de60602fecdbbb72a0723012288fce0d195fc7bdca6c200ac01` |

1. `937f8677…` — first pinned battery (against `d5e8fcae`, superseded candidate).
2. `cf42921b…` — my face-tolerant DIFFERENTIAL version, used for the `FINAL-*` runs (receipts `SUPERSEDED-cf42921b-*.log`). Note these are on the candidate's pre-split; they are superseded.
3. `88e0c3e6…` — reverted to an earlier state by L1 at 18:12:49 ("reverted a post-commit edit"). I did not write this state; L1 confirmed it.
4. `bdc27e2e…` — my re-application of the face-tolerant block (tag F4E8). This is the version `V-cand-1` and `V-base-1` started on.
5. `547b4ce2…` — L1's "Erratum 2 (round 67)" comment block plus a duplicated `WC_REASONS` line, applied at 18:15:14. No behavioural change versus `bdc27e2e…`. L1 instructed a freeze here; I have not written or run it since.
6. `ea31d439…` — L1 removed the duplicated `WC_REASONS` line after the freeze. This is the file on disk now. Only comment and duplicate-constant bytes differ from `bdc27e2e…`; the battery has not been run since this state.

Evidence-to-bytes mapping: `V-cand-1` and `V-base-1` ran on `bdc27e2e…`; `V-cand-2` straddled the 18:15:14 edit (`bdc27e2e…` → `547b4ce2…`); `V-base-2` ran entirely on `547b4ce2…`. `ea31d439…` (the current file) has not been run. The three states differ only by a comment block and a duplicated constant, so the verdicts apply to `ea31d439…` by inspection, not by a run on those exact bytes. L1 instructed no further runs.

## What the battery does

`multihead-mutbat.py --instrument <gate> --collector <probes.py> --work <dir>`

* copies the candidate into scratch and applies **one** text replacement per limb at the smallest
  behaviour-bearing point; anchors must match exactly once, otherwise the limb is `invalid` and is never
  counted;
* runs the same detectors on pristine and mutated bytes: the candidate's own `--selftest`; 14 built-in
  ledger probes on 4 MiB fixtures; and the shared collector's probes;
* prints per-limb `MUTANT <limb> killed|survived|equivalent|invalid by=<case>`, then one
  `MUTBAT killed=<k>/<total> survivors=<s> equivalents=<e> invalid_rejected=<i> failures=<f>` line;
* exits 0 iff `failures==0 and survivors==0 and killed==total and collector-base-mismatch==0`.

Collector consumption: `--collector` is consumed, never silently ignored. Its `build_fixtures` runs in
`work/collector-root` (FIXTURE pins enforced). Its `probe_table(root)` rows are used as `C:<id>`, with
the collector's any-of reason sets kept (`P10_REASON_SET`, `P1920_REASON_SET`). A collector row whose
pristine result is not stable across two runs is dropped and reported as `COLLECTOR unstable=<id>`.
A collector row that the pristine instrument does not satisfy is reported as
`COLLECTOR-BASE mismatch=<id>` and counted in a separate counter, never in `failures`.

Timing-dependent probes are `DIFFERENTIAL`: `P2-wc-multi-missing` and `P14-wc-two-existing`. Their
pristine face is captured twice; mutants must reproduce green-vs-stale, with any stale reason accepted.
A probe that flips between two immediate repeats is dropped, not counted.

## Verdicts

### Candidate `8147350c` (runs `V-cand-1`, `V-cand-2`)

```
probes=collector:d56a1437…(probe_table) count=34 builtin=14 collector=20
DIFFERENTIAL P2-wc-multi-missing captured=('stale', 'derive-upstream-signal-13')
DIFFERENTIAL P14-wc-two-existing captured=('stale', 'derive-upstream-signal-13')
BASE selftest exit=0 last='selftest cases=73 failures=0'
MUTANT L1-grep-base-1-to-0 killed by=P8-grep-single-sigpipe selftest_exit=1
MUTANT L2-grep-base-1-to-2 killed by=P4-grep-two-existing selftest_exit=1
MUTANT L3-catcutwc-base-0-to-1 killed by=P14-wc-two-existing selftest_exit=0
MUTANT L4-drop-dashdash killed by=P11-dashdash-leading selftest_exit=1
MUTANT L5-count-options-as-operands killed by=P5-cut-single selftest_exit=0
MUTANT L6-unknown-head-stale killed by=P12-unknown-head-sigpipe selftest_exit=1
MUTANT L7-headblind-sigpipe-exempt killed by=P1-cut-multi-missing selftest_exit=1
MUTANT E1-trailing-space-control equivalent by=trailing-space control: two bytes added, no behavioural change
MUTANT E2-le-one-vs-lt-two equivalent by=len(x) <= 1 and len(x) < 2 are the same predicate over integers
MUTANT E3-sigpipe-constant equivalent by=signal.SIGPIPE is 13 on this host and the status is negated
MUTBAT killed=7/7 survivors=0 equivalents=3 invalid_rejected=0 failures=0
```

Both candidate runs have identical verdict lines.

### Base `51f299af` (runs `V-base-1`, `V-base-2`, both on `547b4ce2`)

```
MUTBAT killed=0/7 survivors=0 equivalents=0 invalid_rejected=10 failures=4
COLLECTOR-BASE mismatches=5   (run 2: 4; see below)
```

Counted base failures are stable across both runs: **P1** (`cut` multi-missing), **P3** (`grep`
multi-missing), **P4** (`grep` two existing) and **P11** (`grep -- x big.txt`) each return a value where
`derive-upstream-signal-13` is required. Base's own selftest is 67/0. No mutant is counted as killed on
base.

Run-to-run variation on base, reported and not hidden:
* `P2-wc-multi-missing` flipped between two immediate repeats in run 2 (`value` then `stale
  derive-upstream-exit-1`); it was dropped as unstable, so run 2 has 19 collector/built-in probes, not 20.
* collector `P10` flipped face in run 2 (`COLLECTOR unstable=P10`), giving the 4-versus-5 mismatch count.

Neither flip moves the counted `failures=4` or the killed count, so the stable counted red line for
pinning is `MUTBAT killed=0/7 survivors=0 equivalents=0 invalid_rejected=10 failures=4` (exit 1), which
is what I told ExecMultiHeadDriver. It is not `failures=5`.

## Limb by limb (mutation → named detector → observed deviation)

1. **L1 grep base 1→0** (`{"grep": 0}`). `grep x big.txt | head -n 1` (native −13, 30/30) turns stale;
   `C:P18` flips too. Killed by **P8**; also by the candidate's `upstream-grep-single-pattern-file-sigpipe-benign`.
2. **L2 grep base 1→2** (`{"grep": 2}`). `grep x xlines.txt big.txt | head -n 1` becomes exempt
   (3−2 = 1). Killed by **P4**; P3 also flips; the candidate's `upstream-grep-multi-missing-sigpipe-stale`
   covers the same count.
3. **L3 cat/cut/wc base 0→1**. `wc small.txt big.txt | head -n 1` becomes exempt because the first operand
   absorbs the skip. Killed by **P14** (differential). `--selftest` stays green (gap G1). The `cat` entry
   is behaviourally dead: cat returns through `cat_sigpipe_exempt` first.
4. **L4 end-of-options split → leading-only drop** (the pre-end-of-options shape). `grep -- x big.txt |
   head -n 1` becomes exempt, while the candidate stales because everything after `--` counts. Killed by
   **P11**, by `C:P19`/`C:P20`, and by the candidate's counted cases
   `upstream-cut-dashfile-after-separator-stale` / `upstream-grep-dashfile-after-separator-stale`
   (`selftest_exit=1`). The counted suite now closes this limb; it did not in the first candidate.
5. **L5 count option tokens as operands** (`return len(pre) + len(post)`). `cut -f1 -d: big.txt | head -n 1`
   becomes stale; `C:P12` flips too. Killed by **P5**. `--selftest` stays green (gap G3).
6. **L6 unknown head stale** (`return True` outside `READ_ONLY_HEADS`). `python3 pipe.py | head -n 1 |
   wc -l` becomes stale. Killed by **P12**; also by the candidate's `upstream-sigpipe-nonfinal-benign`.
7. **L7 head-blind SIGPIPE exemption** (the base rule). P1/P2/P3/P4/P10/P14 go green with values. Killed by
   **P1**, and by `upstream-cut-multi-missing-sigpipe-stale` / `upstream-cat-multi-missing-sigpipe-stale`.
   This is the C1 defect re-injected; the candidate is not equivalent to base.

## Equivalents (recorded, never counted)

* **E1 trailing-space control** — two spaces after the count's `return` line. No behavioural change.
* **E2 `<= 1` → `< 2`** — same predicate over integers.
* **E3 `-signal.SIGPIPE` → `-13`** — `signal.SIGPIPE` is 13 here; the status is negated.

All three reproduce `--selftest` 0/73 and every probe expectation exactly.

## Existing production mutbat against the candidate

`corpus/instruments/figure-audit-mutbat.py --instrument <candidate 8147350c>` (receipt
`receipts/prod-figure-audit-mutbat.log`): `PRISTINE selftest_exit=0 (73 cases)`, control held,
`mutbat killed=5/5 survivors=0 invalid=0 controls=pass`, exit 0. The same 5/5 was measured against the
pre-freeze `d5e8fcae`.

## Coverage findings

* **G1** The 73-case selftest does not kill L3: no counted case has a SIGPIPE'd multi-input `wc` whose
  first token is an operand (`wc small.txt big.txt`). The counted `wc` case uses `-l` first, which absorbs
  the base-count skip.
* **G2** Post-`--` handling counts a grep pattern as an operand. `grep -- pattern file | head -n 1` (one real
  input) is therefore a **safe false stale**: the candidate refuses a pipeline that reads one file. The
  safe direction, but the grep pattern is a required argument, not an option value; an exact rule would
  skip it after `--` too.
* **G3** There is no single-input SIGPIPE-green counted case for `cut`/`wc`/`sort`/`sha256sum`; only grep
  has one. L5 makes single-input `cut` stale and the selftest stays green; only the battery catches it.
* **G4** `wc` multi-input SIGPIPE is timing-dependent on this host: 30/30 native `−13` in one sweep, but
  gate-level flips were observed (run 2 above). Any counted case must keep the either-reason shape; any
  probe that depends on it must be differential.
* **G5** The grep base budget is load-bearing for four probe shapes (P3, P4, P8, P11); a one-case pin would
  not catch a wrong base.

## Measurements (receipts, `.ufo/waves/round-67/w1/MutationMultiHead/receipts/`)

* `native-statuses.txt` — 30 repeats per pipeline, `set -o pipefail`: multi-input `cut`/`wc`/`grep` −13;
  single-input `cut`/`grep x big.txt`/`cat`/`grep -- x big.txt` −13 but exempt; `wc -l big.txt`/`sha256sum
  big.txt` 0; `head -n 5 big.txt missing.txt` 1; python `pipe.py` −13.
* `V-cand-1.log`, `V-cand-2.log` — candidate pair (7/7, 3 equivalents, failures=0).
* `V-base-1.log`, `V-base-2.log` — base pair (0/7, failures=4; collector mismatches 5 and 4).
* `SUPERSEDED-cf42921b-*.log` — the earlier `FINAL-*` runs on `cf42921b…`; kept for lineage, not cited.
* `candidate-selftest.log` (73/0), `prod-figure-audit-mutbat.log` (5/5), `mutant-diffs.txt` (exact unified
  diff and mutant sha256 per limb), `candidate-sha.txt` (every sha above, with the run it applies to).

## Honesty and bounds

* No sandbox claim: the battery executes the selected instrument's selftest and probes; fixtures live in
  its own work dir and are removed on exit unless `--keep`.
* Every probe is a ledger derive run through the gate itself, not a reimplementation of its rule; native
  statuses were measured, never assumed.
* No invalid-mutant path was exercised against the final candidate: every anchor is exact-once and every
  mutant compiles. The invalid path is exercised by the base run (baseline not satisfied, each limb
  reported `invalid`, none counted).
* The frozen battery `547b4ce2` was **not** run cleanly end-to-end on the candidate; its candidate runs
  were on `bdc27e2e…`, which differs only by a comment and a duplicated constant. L1 froze it and instructed
  no further runs.
* No production byte, ledger, SOURCES/README/knowledge, SCORECARD/SKILL/PROVINCE/LOG, git/jj state, git
  index or sibling lane was touched by this seat. Base bytes were read with `git show` (no index or state
  mutation).
* Scratch `/fast/scratch/hyaku/kasegi-r67/MutationMultiHead/` is removed after receipts were copied.
* No tool was installed or upgraded.

## Residuals (named, not repaired here — L1's call)

1. Counted-suite extension for G1 and G3: a `wc` two-operand case with the operand first; single-input
   `cut`/`wc`/`sort`/`sha256sum` SIGPIPE-green cases.
2. G2: grep pattern after `--` is counted as an operand, so a legitimate single-file pipeline is refused.
3. `wc` multi-input SIGPIPE face is timing-dependent; counted cases keep the either-reason shape; dependent
   probes stay differential.
4. The frozen battery has not been re-run end-to-end on its own bytes (L1's freeze); its verdicts above are
   from the bytes listed per run.
