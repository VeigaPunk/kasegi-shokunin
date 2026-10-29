VERDICT: DRAFT-READY

Seat: R46bW2MutPlain (wave 2, leaf). Artifact attacked: the plain-measure script
`.ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/plain-measure2.sh`
(sha256 `3d169bbabef302d99aaac64f0f6eb1ef28f8175a2d38215b1abc938411f0c1a8`).
The draft and its landed successor are byte-identical: the same file exists at HEAD
96379ae26ef9 under the same path with the same sha256 (verified via
`git show 96379ae:<path> | sha256sum`). The file is NOT present at fe0f56b.

Target-tree note (dispatch discrepancy): the dispatch calls fe0f56b "integration of
wave 1", but at fe0f56b the corpus is still at the before-values (28/73/65, e=2, no
F29 entry — verified) and the script is absent. The landed integration commit is
96379ae26ef9 (current HEAD). Per the item ("must change a printed value on the landed
tree") the mutants were graded against a `git archive 96379ae corpus` export; the
fe0f56b export was run as an additional control.

Method: script copied to scratch (`/fast/scratch/hyaku/kasegi-r46/R46bW2MutPlain/`);
every run: `PLAIN2_SCRATCH=<own seat dir> PLAIN2_LANE=<exported tree> TMPDIR=<own>
PLAIN2_BATTERY_COUNTERS=<see below> bash <script> <tree-export>`; each mutant is a
single-edit copy (diff shown per finding); all runs battery-off except where stated
(the g lines print `not-run` under that env in BOTH pristine and mutant runs, so it
cannot mask any non-g mutant; the g-targeting mutant m07 is graded against a full
default-env pristine run). Trees were only read; the lane working tree was not
modified (porcelain clean for corpus/ and .ufo/waves/round-46/attempt2/wave1/ after
all runs). Scratch removed at end.

PRISTINE BASELINE — landed export (96379ae corpus), battery off:
```
a_frontier_rows=29
b_frontier_counter=frontier rows/admitted=[frontier rows=29 admitted=29] exit=0
c_sources_rows=74
d_knowledge_files=66
e_absence_sweep_files=4
f_selftest_c1=selftest cases=83 failures=0 (rc=0)
f_selftest_c2=NameError: name 'C1_ENTRIES' is not defined (rc=1; form: --pure --work --jobs)
g_battery_c1=not-run
g_battery_c2=not-run
```
DO-NOTHING CONTROL — comment-only edit (m10, sha256
`f8b0322c57ce9b1c6ee42b45417d0e0e11e7d3a04a8b963a03566aa77ea716bc`):
`diff out/orig96.out out/m10.out` → no differences ("CONTROL-M10-IDENTICAL"); the
script does not flag innocent edits.

TREE DISCRIMINATION CONTROL — same script, base 04af9bc corpus export:
```
a_frontier_rows=28
b_frontier_counter=frontier rows/admitted=[frontier rows=28 admitted=28;frontier expected=29 admitted=28 verdict=SHORT exit=1] exit=1
c_sources_rows=73
d_knowledge_files=65
e_absence_sweep_files=2
f_selftest_c1=selftest cases=76 failures=0 (rc=0)
f_selftest_c2=selftest cases=137 failures=0 (rc=0; form: --pure only (--work/--jobs rejected by argparse: r46-counters-selftest-c2.py: error: unrecognized arguments: --work ... --jobs 8))
```
Every a–f line differs from the landed run, and this reproduces the frozen
before-values (28 / 28-28-short-exit-1 / 73 / 65 / 2 / 76-0 / 137-0). The same run
against the fe0f56b export printed a=28 c=73 d=65 e=2 f1=cases=76 failures=0
f2=cases=137 failures=0 — identical to the base export on every line. The script
tells the three trees apart.

MUTANTS (each verified single-edit by diff; expect-before/after = pristine line)

M01 — drop the absence sweep. `-rliE` sweep line replaced by `e=0`.
  sha256 d1698d92a837fde6a663ba16ac431593e49c8a1b57a82f7810b8d78e69c4ce2a
  printed: `e_absence_sweep_files=0` (was 4). KILLED.
M02 — count knowledge files recursively (drop `-maxdepth 1`).
  sha256 4b0af3b8ac966cfc16465efd779236a53bd6429926eee7ca8e764f4d465083f9
  printed on landed export: `d_knowledge_files=66` — UNCHANGED. SURVIVED on the
  landed tree (equivalent-on-this-tree: corpus/knowledge has no subdirectories at
  96379ae). Discriminated on a constructed tree (export + empty
  `corpus/knowledge/nested-subdir/constructed.md`): pristine `d_knowledge_files=66`,
  mutant `d_knowledge_files=67`. Recipe: create any subdirectory holding a `.md`
  under corpus/knowledge; a verifier comparing d against 66 catches the mutant there.
M03 — unquote the (a) grep: `grep -cE ^\| F[0-9]+ \| "$T/corpus/README.md"`.
  sha256 39ed16ac9ed206f4906e180cfb47210d7e4faeb612726a08195402389401333d
  printed: `a_frontier_rows=/fast/.../t96/corpus/README.md:693` (was 29; the unquoted
  pattern splits into words and grep -c prints path:count). KILLED.
M04 — unquote the (e) sweep: `grep -rliE repository securit. advisor|GHSA ...`.
  sha256 c72c51d9a5ddfceaa7a865e4db3e8fd49a79ddf86ba0583c6b5cee887a326a96
  printed: `e_absence_sweep_files=0` (was 4; the unquoted `|` pipes grep's first
  words into the command `GHSA`, which fails, so wc -l counts nothing). KILLED.
M05 — weaken the frontier gate: `--expect 29` → `--expect 28`.
  sha256 deec225077d59f01e8612ebb5f784d4a580e17c9888fa0ebcaf367e752aa9a7a
  printed: `b_frontier_counter=frontier rows/admitted=[frontier rows=29 admitted=29;frontier expected=28 admitted=29 verdict=SHORT exit=1] exit=1`
  (was `[frontier rows=29 admitted=29] exit=0`). KILLED. (Cosmetic only: the r44
  counter labels any admitted!=expect mismatch "SHORT", even too-many; verdict logic
  is `is_short = lambda admitted, expect: admitted != expect`, line 117 of
  r44-frontier-count.py.)
M06 — fake a passing baseline: `f1=$(printf '%s' "$f1_out" | tail -1)` →
  `f1="selftest cases=76 failures=0"`.
  sha256 6959169968b793d864eef3ff135fc87b7f290a8d18cb8d2396705e3cf56b52da
  printed: `f_selftest_c1=selftest cases=76 failures=0 (rc=0)` (was
  `selftest cases=83 failures=0 (rc=0)`). KILLED.
M07 — silently skip the battery: default `BATT_COUNTERS` `c1 c2` → `none`.
  sha256 407e16e689132ba2b5d606a967f275c403c2b7dac8da9d47deb949194ee02498
  run with NO env override so the mutated default is exercised; compared against the
  full default-env pristine run. Mutant printed:
  `g_battery_c1=not-run` / `g_battery_c2=not-run`; pristine full run printed:
  `g_battery_c1=mutbat counter=c1 mutants=20 caught=19 equivalent=0 uncaught=1 baseline_failures=0`
  `g_battery_c2=mutbat counter=c2 BASELINE-DIRTY baseline_failures=-1`
  KILLED (a verifier sees the summaries vanish).
M08 — drop `-i` from the (e) sweep (`grep -rlE`).
  sha256 01945b9b8cc08416fd451e27dfec881f395b2ffe27fd67b45ccdc32fbfc1c061
  printed on landed export: `e_absence_sweep_files=4` — UNCHANGED. SURVIVED on the
  landed tree (all four matching files contain case-exact tokens). Discriminated on a
  constructed fixture (file containing only "The Repository Security Advisory
  lifecycle is maintainer-side"): with -i `1`, without -i `0` (direct grep, both
  quoted verbatim in the transcript). Recipe: a knowledge file whose only occurrence
  of the phrase is mixed-case catches the mutant via e against 4.
M09 — loosen the (d) name filter: `-name '*.md'` → `-name '*'` (also counts the
  knowledge directory itself).
  sha256 0fdb57f32a31b0b107044ef2745d4757d831f1c7bc89192472d7d792e495022c
  printed: `d_knowledge_files=67` (was 66). KILLED.

Score: 7 of 9 behavioral mutants change a printed value on the landed tree; M02 and
M08 survive there (both discriminated on constructed trees with recipes above). The
do-nothing control is clean and the script separates base / fe0f56b / landed on
every a–f line.

DEFECTS THE RUN EXPOSED ON THE LANDED TREE (not mutants; reported as observed)
1. `corpus/instruments/r46-counters-selftest-c2.py` at 96379ae crashes at import on
   EVERY invocation: line 68 `EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER} ...` runs before
   line 69 `C1_ENTRIES = {"claim-gates.md", "claim-package-contract.md"}` (use before
   definition; at fe0f56b the definition is at line 60 and precedes all uses). Printed:
   `Traceback ... line 68, in <module> EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER} ... NameError: name 'C1_ENTRIES' is not defined`.
   Because the exit code is 1 (not argparse's 2), the script's documented `--pure
   --work --jobs`-then-fallback logic keeps the crashed form and prints
   `form: --pure --work --jobs`; the landed "cases=137 failures=0" is not reproducible
   here. This touches claim C1's `after` (selftests failures=0 at final revision) and
   the "selftests 83/147" line of the 96379ae commit message.
2. With the script's full defaults on the landed export:
   `g_battery_c2=mutbat counter=c2 BASELINE-DIRTY baseline_failures=-1` — the c2
   battery does not produce a summary (consistent with the broken c2 selftest feeding
   its baseline), and `g_battery_c1` prints `uncaught=1` (caught=19, equivalent=0,
   baseline_failures=0), i.e. claim C1's `expect_after` (uncaught=0 both) is not met
   by this exact command (`python3 <export>/corpus/instruments/r46-mutbat.py --root
   <landed export> --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work <scratch>
   --counter c1 --jobs 8`, via plain-measure2.sh defaults). C1/C2 adjudication belongs
   to other seats; quoted here because my instrument printed it.

LIMITATIONS
- Mutant runs (and the m07 comparison) ran with PLAIN2_BATTERY_COUNTERS=none except
  the full pristine run; the g-line mutants are covered by M07 only.
- The full pristine battery ran once (wall ~100 min under host load avg ~80; peers
  were running batteries concurrently), with the script's default PURE
  (/fast/scratch/hyaku/kasegi-r46/L1/pure2) and PLAIN2_LANE=the 96379ae corpus
  export; no per-mutant battery log was retained (PLAIN2_LOG_DIR unset, scratch
  cleaned), so the single uncaught c1 mutant is not identified here.
- The instrument set itself (r46-counters-selftest-c2.py, r46-mutbat.py) is attacked
  by sibling seats; this report only records what plain-measure2.sh printed.
- No commits, pushes, git/jj/index mutations; nothing written outside the named
  report path and scratch; scratch (including all mutant copies and outputs) deleted
  after this report was written.
