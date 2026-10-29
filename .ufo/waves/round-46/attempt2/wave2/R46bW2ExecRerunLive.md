VERDICT: BROKEN

Seat R46bW2ExecRerunLive — round 46 attempt 2 wave 2, single item: re-run the selftest/battery
suite on the LIVE lane, expect the claim after-values, then export-vs-live delta.
Live lane at start of run: HEAD 96379ae26ef9443097b860ddb33ef924b2cd5b5a (wave-1 integration;
freeze fe0f56b beneath it). All runs read-only; nothing committed, pushed or mutated.

HEADLINE
The frozen claim after-values (claims.json C1/C2) do NOT hold at the final lane revision
(96379ae). Two of the five committed instruments crash on the landed tree; the battery's c2 and
f29 modes are therefore dead at that commit. Every after-value DOES hold — but only on an
uncommitted, unlogged amendment batch (six tracked corpus files + one untracked proof file,
mtime 2026-10-29T21:34–22:08Z) that landed in the live tree WHILE wave-2 reruns were in flight
(my battery ran 21:20→23:34Z across the edit boundary). That is exactly the uncommitted-drift
finding this seat hunts, at claim-killing scale.

FINDINGS

F1 — Committed c2 selftest crashes at the landing commit (C1 after-value false at 96379ae)
Artifact: corpus/instruments/r46-counters-selftest-c2.py @96379ae (line 68 uses `C1_ENTRIES`
before its line-69 definition; module-level, deterministic).
Command: `python3 corpus/instruments/r46-counters-selftest-c2.py --pure
/fast/scratch/hyaku/kasegi-r46/L1/pure2` (cwd = lane; the item's exact invocation).
Output (rc=1, empty stdout):
  File ".../corpus/instruments/r46-counters-selftest-c2.py", line 68, in <module>
    EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}  # ...
                     ^^^^^^^^^^
  NameError: name 'C1_ENTRIES' is not defined
Same crash on the 96379ae integration export. The wave's own receipt
controls/final-battery.txt (untracked) already records this NameError and ends mid-file at
"== battery c1:" with no battery output — the landing shipped knowing the extended c2 baseline
never ran. C1 after-value "the extended selftests ... keep `failures=0` baselines at the final
revision" is false at 96379ae.

F2 — Committed f29 selftest crashes on the landed lane (C2 selftest duty false at 96379ae)
Artifact: corpus/instruments/r46-selftest-f29.py @96379ae, build_positive() line 188: accepts
only a 28-row (pre-landing) lane; the landed lane has 29 rows.
Command: `python3 corpus/instruments/r46-selftest-f29.py` (exact item invocation, no args; also
with --pure/--work/--jobs). Output rc=1, zero case lines:
  selftest: lane README carries 29 frontier rows, expected 28
Do-nothing discriminator: same selftest file with `--lane <freeze fe0f56b export (28 rows)>
--counter <live r46-f29-gate.py>` reads `selftest cases=30 failures=0` rc=0 (9.3s) — the
instrument is complete; its own landing commit broke its default-lane precondition.

F3 — Battery f29 mode dead at the landing commit (C2 frozen duty unmet at 96379ae)
Command: `python3 corpus/instruments/r46-mutbat.py --root <tree> --pure .../L1/pure2 --work
<scratch> --counter f29 --jobs 8` against the live tree at HEAD and against the 96379ae export.
Output (rc=1, both):
  mutbat counter=f29 BASELINE-DIRTY baseline_failures=-1
(-1 = the grader selftest printed no failures= line: F1/F2 crashes.) C2 after-value "reaches the
same caught-or-equivalent state for the f29 gate's 21 mutants via the battery's f29 mode" is
false at the final revision commit.

F4 — Mid-wave uncommitted amendment batch (the export-vs-live delta)
`git status --porcelain` (tracked, non-.ufo) at 2026-10-30T02:30Z — six modified corpus files +
one untracked file, mtimes all inside the wave-2 rerun window:
  21:34:03 corpus/instruments/r46-f29-gate.py       (+1: LEDGER_MIN_BYTES 30696 -> 40843)
  21:34:03 corpus/knowledge/github-repository-security-advisories.md (rule-3 prose, CNA coverage)
  21:34:16 corpus/instruments/r46-selftest-f29.py   (accepts 28-or-29-row lanes)
  21:49:20 corpus/instruments/r46-mutant-equivalents.json (+3 f29 entries)
  21:49:20 corpus/instruments/r46-mutant-equivalents/f29-H1b-H7a-H7c-proofs.md (UNTRACKED, 2066 B)
  21:57:26 corpus/instruments/r46-c2-gate.py        (+29/-3: G2 junk-row clause rewritten to
                                                     tolerate "well-formed no-cite rows")
  22:08:42 corpus/instruments/r46-counters-selftest-c2.py (C1_ENTRIES reordered — fixes F1 —
                                                     plus ctl-committed-tip-direct rebaselined
                                                     to fixed=5/7 failing ['G1','G6'])
This is limb-sentence/semantics change to two frozen counters, post-freeze, post-wave-1 —
counter-errata.md still ends at E4 (no E5/E6), violating the claims' own rule: "the two
counters' limb semantics are unchanged (any byte change to them is a logged erratum)". On the
amended bytes the suite goes green:
  `r46-counters-selftest-c2.py --pure .../pure2`      -> `selftest cases=147 failures=0` rc=0
  `r46-selftest-f29.py`                               -> `selftest cases=30 failures=0` rc=0
  `r46-mutbat.py --root <live> ... --counter f29`     -> `mutbat counter=f29 mutants=21
     caught=18 equivalent=3 uncaught=0 baseline_failures=0` rc=0 (34.8s)
  `r46-f29-gate.py --root <live>`                     -> `f29-gate fixed=7/7 exit=0`
i.e. every C1/C2 after-value holds ONLY on uncommitted bytes.

F5 — The three f29 "equivalents" rest on an uncommitted proof with a dangling receipt
The amended map routes H1b-raw-loose, H7a-verdict-or, H7c-okline-loose to
corpus/instruments/r46-mutant-equivalents/f29-H1b-H7a-H7c-proofs.md — git status `??`
(UNTRACKED → not a committed proof; C1 after-value: "every equivalent verdict names a committed
proof"). The proof cites as its receipt `.ufo/waves/round-46/attempt2/controls/f29-battery-f29.txt`
— that file does NOT exist in controls/. It also names mutant "H7b-registry-count", which is not
in the battery's F29_MUTANTS table (H7b = symlink-dead). The claim kill rule ("an equivalent
verdict's proof file is missing ... keeps the claim red") is engaged in spirit: the f29
uncaught=0 state is manufactured by uncommitted map + untracked proof + missing cited receipt.

F6 — Values that hold on the live tree (retained for the tally)
- c1 selftest (item command, --jobs 8): rc=0, `residual-false-greens=1 (disclosed mechanical
  limits, not counted as failures: R-claim-text-unrelated-to-anchor)`,
  `selftest cases=83 failures=0` (481.7s) — C1 after-value (76 -> 83) holds; c1 selftest bytes
  unchanged by the amendment batch, so this is a HEAD-bytes value.
- mutbat `--counter both --jobs 8` on live (21:20→23:34Z, 8017.6s):
  `mutbat counter=c1 mutants=20 caught=19 equivalent=1 uncaught=0 baseline_failures=0`
  `mutbat counter=c2 mutants=21 caught=18 equivalent=3 uncaught=0 baseline_failures=0`
  (c1 phase = HEAD bytes; c2 phase = post-21:57/22:08 amended bytes — see F4; the equivalents
  are M14 / G6b+G7a+G7c, all pointing at COMMITTED proof files, both verified non-empty and
  substantive: 15-tree differential identical, mutation-class differentials with 0 differing
  readings).
- f29-gate `--root` live AND `--root` 96379ae export: `f29-gate fixed=7/7 exit=0` (limbs
  H1–H7 all pass=1; 1.0s).
- C2 plain counts, live AND integ export: frontier rows 29 (28→29), SOURCES rows 74 (73→≥74),
  knowledge entries 66 (65→66), absence sweep 4 files (2→4) — all four C2 count moves hold.
- S074 capture: sha256 1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039, 42
  lines — matches the claims text and the manifest's pinned sha (gate H4: quotes-ok=9,
  frozen-cores-missing=0).
- Frozen before-receipt: controls/mutbat-before.txt sha256 13c21fcd9e04c76b769013e56cb8db4f654
  6c52b2a436c08376b9f3459efb1fd — byte-matches the sha pinned in claims.json.

F7 — Export-vs-live delta summary
Tracked corpus bytes differ live-vs-96379ae in exactly the six F4 files (diff otherwise empty;
only gitignored artifacts extra). Consequences measured: c2 selftest crash↔147/0, f29 selftest
crash↔30/0, mutbat f29 BASELINE-DIRTY↔21/18/3/0/0. No unexplained drift beyond F4.

LIMITATIONS (each missing check named)
- The `--counter both` battery on the 96379ae EXPORT was cancelled at the L1 wrap nudge mid-c1
  (baseline + M01..M18 printed; every printed per-mutant value equals the live battery's
  line-for-line, e.g. M14 equivalent, M15 caught=2). Missing: the export c1 final summary line
  and the export c2 phase. Mitigation on record: c1-affecting bytes (r46-counters-selftest-c1.py,
  r46-c1-gate.py, r46-mutbat.py, pure2 fixtures) are byte-identical live-vs-export (diff empty),
  so the live c1 tally is already a HEAD-bytes value; the export c2 phase is fixed by F1's
  demonstrated crash on the export plus the export mutbat-f29 BASELINE-DIRTY (F3).
- Per-mutant selftest receipts (wave-1 per-mutant verification) not re-derived; the battery
  caught tallies stand in for the "new dedicated case fails under its targeted mutant" clause.
- The three committed equivalence arguments (M14, G6b/G7a/G7c) were checked for existence and
  substance, not independently falsified by a constructed input (crit seats' lane).
- No live-target testing, no credentials touched (spec). Scratch
  /fast/scratch/hyaku/kasegi-r46/R46bW2ExecRerunLive removed after this report was written;
  no /tmp-citable evidence; nothing outside my item's paths was written.
