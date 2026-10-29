VERDICT: BROKEN

## Testable after-value
The battery's necessary summary value is `(C1 uncaught, C2 uncaught, C1 baseline_failures, C2 baseline_failures) = (0, 0, 0, 0)`, with mutant totals `20` and `21`. This summary alone does not establish that trusted selftests ran or that an equivalence proof is valid.

## Findings

1. **Do-nothing control is nonzero in the frozen receipt.** I exported base `04af9bc92229232ea5cce8b32bfe59dd969eb26d`; the frozen battery file's `sha256sum` was `f7a7cdfa187ef6f2a074e9bda06af7d6163e43da69593b500b95c2c3a29e7fa8`, matching `freeze.txt:4`. I ran the frozen battery against that export, with the original base selftests untouched:
   ```
   TMPDIR=<scratch>/tmp python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-mutbat.py --root <scratch>/base --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work <scratch>/work/noop --counter both --jobs 8
   ```
   It printed `mutant=M01-L1-target-24 baseline_failures=0 mutant_failures=26 verdict=caught`, `mutant=M02-L1-broken-ignored baseline_failures=0 mutant_failures=8 verdict=caught`, and `mutant=M03-L1-floor-dropped baseline_failures=0 mutant_failures=1 verdict=caught`, then timed out at 3600s before a summary. The authoritative frozen before receipt prints `mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0`, `mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0`, `BATEXIT=1` (`controls/mutbat-before.txt:21,43-44`). Thus the preserved do-nothing value is not zero; the complete independent replay is a limitation noted below.

2. **A gutted selftest can produce `uncaught=0`.** In a separate scratch export, I replaced both selftests with two-line stubs that execute no cases and print `selftest cases=1 failures=1` only when `--counter` is present (baseline prints `failures=0`). Command:
   ```
   TMPDIR=<scratch>/tmp python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-mutbat.py --root <scratch>/stubcaught --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work <scratch>/work/stubcaught --counter both --jobs 8
   ```
   Printed `mutant=M06-L3-home-dropped baseline_failures=0 mutant_failures=1 verdict=caught`, `mutbat counter=c1 mutants=20 caught=20 equivalent=0 uncaught=0 baseline_failures=0`, `mutbat counter=c2 mutants=21 caught=21 equivalent=0 uncaught=0 baseline_failures=0`, `STUB_CAUGHT_EXIT=0`. The stub source at `<scratch>/stubcaught/corpus/instruments/r46-counters-selftest-c1.py` is only `import sys` plus `print(...)`; it has no test cases. This is a false green for the summary predicate.

   Source evidence: `r46-mutbat.py:98-108` executes the selftest from `--root`, extracts only the last `failures=<n>` match, and ignores the subprocess return code/case count; `:166-175` calls any `mutant_failures >= 1` caught. It does not establish that the tested file is the committed selftest.

3. **A zero-byte, false “proof” also yields `uncaught=0`.** I used always-passing empty selftest stubs and an `--equivalent` map pointing all mutant IDs at one zero-byte file. Command:
   ```
   TMPDIR=<scratch>/tmp python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-mutbat.py --root <scratch>/stubeq --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work <scratch>/work/stubeq --counter both --jobs 8 --equivalent <scratch>/empty-equivalences.json
   ```
   Printed `mutant=M06-L3-home-dropped baseline_failures=0 mutant_failures=0 verdict=equivalent`, `mutbat counter=c1 mutants=20 caught=0 equivalent=20 uncaught=0 baseline_failures=0`, `mutbat counter=c2 mutants=21 caught=0 equivalent=21 uncaught=0 baseline_failures=0`, `EMPTY_PROOF_EXIT=0`, `empty-proof-size=0`. This is not evidence of equivalence: the M06 input probe below changes the frozen gate's L3 result.

   Probe output for the constructed allowed line `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md # /home/reviewer`:
   ```
   exact_line=1 home_clause=1 L3_original=0 L3_M06_after_clause_drop=1
   ```
   `r46-mutbat.py:49` defines M06 as deleting the HOME_RE clause; `r46-c1-gate.py:71-73` allows an arbitrary trailing comment, and `:266-268` uses HOME_RE to reject it. The constructed comment therefore falsifies an M06 equivalence argument under the frozen clause. The battery's `:169-171` accepts the empty proof because it checks only `os.path.isfile(eq[mid])`.

## Weakest kill-rule sentence and correction
The weakest sentence is the claim that an `--equivalent` map entry pointing at a written argument file is a “committed proof” (`claims.json:15`); the kill rule says an empty or falsified proof must fail (`:16`), but `r46-mutbat.py:169` accepts any existing path, including a zero-byte file. The “graded by the committed selftests” sentence (`:15`) is similarly unenforced because the driver runs whichever selftest is in `--root`.

Smallest safe correction: have the grader use/pin the final committed selftest bytes (and require successful exit plus the expected case-count/failure summary); do not treat path existence as equivalence. Count an equivalence only after a nonempty, hash-pinned proof has independent review and survives a constructed counterexample search. M06 must be caught by a real dedicated case or not be classified equivalent. This affects C1's verifiability evidence for both mutation sets, not the unchanged gate-limb semantics or the separate F29 coverage axis.

## Limitations
The full pristine-base replay timed out after 3600s; its full before pair above comes from the frozen receipt, while my replay only reached M01-M03. Both successful predicate attacks used scratch-only altered selftests/maps; I did not alter shared instruments, gates, claims, or selftests, and did not adjudicate the final lane revision or F29.