# LabDeterminism — r39 suite determinism probe (H7 baseline)

Method: `bash corpus/instruments/r39-closure.sh --export-ref 8371e7ac9f32cae5ed72f8c28205634603f836fa --work $S/<x>` run four times, TMPDIR=$S=/fast/scratch/hyaku/kasegi-r40/LabDeterminism, work dirs a,b,c,d (all distinct, outside the lane). a/b with explicit `--lane <lane>` from the fleet root; c/d from cwd=lane without --lane. Disk guard green before the run. No lane writes (git status shows only pre-existing untracked round-40 files).

## Observed
- a vs b: `diff` empty, stdout 1286 bytes each, sha256 a5c7c3405d47b4a01fc200434ce195f07a72234cdd613cd092e32f756b4ca40b, stderr 0 bytes both, exit 1 both. BYTE-IDENTICAL despite distinct --work dirs (no work path, mktemp name, timestamp or PID is printed).
- c vs d: `diff` empty (BYTE-IDENTICAL), stderr 0 bytes, exit 1 both.
- a vs c: single differing line: a/b print `deviation=non-default --lane` (line 2) because --lane was passed explicitly; everything else identical (same suite-sha256 2856a210...b4222b).
- Result of the judged-head export: `closed=6/8 exit=1` here (G2 closed=0, G8 closed=0; G1,G3-G7 closed=1). Note: the frozen claims quote the final r39 receipt as closed=7/8 — this probe observed 6/8 at today's lane state, so the r39 verdict is NOT constant across time: G2 (ancestor=0, final-lane-commit=0, closed-line=0, selftest-summary=0, sentinel=0) and G8 (r37-closed=0 r37-exit=1) read live git/ref/host state outside the tree. [INFERENCE: the 6 vs 7 difference comes from those live-state limbs, e.g. ancestry/post-receipt reads and the pinned r37 run; I did not isolate which; not tested.]

## Implications for H7
- Stdout of an export-mode run is a pure function of (export bytes, ref-scoped git reads, host scratch scan) at a fixed lane state: re-run reproduction of a teed transcript is achievable provided the transcript excludes the work dir and carries no run-time clock; a run-utc line printed by the run itself would be the sole non-reproducible line and must be excluded/fixed from the byte-identity comparison (or taken from the receipt, as H7 requires run-utc printed once and re-run compared after masking/consistently).
- Plan the r40 receipt re-run to happen with the same lane HEAD/refs: the r39 suite's live limbs (G2 ancestry/diff, G6 scratch scan, G8 pinned git show/r37 run) mean byte-identity holds only at unchanged repo/host state.
- G6 depends on host scratch siblings (kasegi-r39*/r40 absent at probe time: r37=absent,r38=absent,r39=absent).

Deliverable: LabDeterminism.txt (captured run output + diff verdict lines), 13 lines, sha256 23b004894abee4f39d665c9323523ce152be70187527d0d5247c46fe0d45c312.
Tools installed: none. Scratch removed on exit.
