# R47MutBattery — battery integrity (wave 1, kasegi round 47, lane kasegi-shokunin)

Scope executed exactly as tasked: `r47-mutbat.py --base <fresh base export> --work <scratch> --counter both --list`; (a) per-triple exactly-once check; (b) receipt verdict on `baseline_failures=0` / `uncaught=0`; (c) 5 named mutants re-run end-to-end + 1 bonus survivor probe. Full 56-mutant battery NOT re-run (per tasking and KasegiR47a3 scratch reminder). No tooling installed (no pacman; stock python3/grep/sha256sum sufficient).

## Restoration evidence (live lane bytes untouched)
Base export: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8 corpus | tar -x -C <scratch>/base` (read-only archive; export root used as `--base`). All mutations were applied to scratch COPIES; the live instruments dir was never written. sha256 before == after == freeze pins (`freeze.txt:3-6`):

```
e6ede7b668155fc173ad9a1c0f83168f173d6c31b12ecb85da406e1660424aee  corpus/instruments/r47-routed-defects.py
563d52b827acf3afe269a0079f76ba7b208cefed69c14ff24ea47b86030e6b3b  corpus/instruments/r47-f30-gate.py
4c7c0aab5b5eb3885965bd9e0ec3c1b8ddda7f3f393af6a3863c6eeea6347ec4  corpus/instruments/r47-counters-selftest.py
eda81d5d4162d8732ce333867c6e3efcf806e5947c81f886454771e6c5f8c8d3  corpus/instruments/r47-mutbat.py
```
Identical pre-run and post-run; match `freeze.txt:3-6` byte-for-byte.

## (a) Old-substring exactly-once — PASS (with a grep method caveat)
`--list` emits exactly 56 triples (35 c1 + 21 c2; `R47MutBattery.draft/list.txt`; the raw file is 66 physical lines because five triples embed real newlines). `grep -Fc` per triple, scripted (`R47MutBattery.draft/grep-sweep.txt`):
- 51/56 triples: `grep-Fc=1` ✓.
- 5 triples (L1c-wrong-file, L2a-fences-ignored, L5a-order-ignored, L5c-order-inverted, L9a-oldcite-ignored) report `grep-Fc` 2–3: GNU grep OR-splits a newline-embedded `-F` pattern into per-line alternatives and counts matching LINES, so `grep -Fc` cannot express "exactly once" for multi-line patterns. This is a measurement artifact, not drift.
- Authoritative exact-substring check (`text.count(old)`, the same primitive the battery asserts in `r47-mutbat.py` `apply_mutant`): **56/56 count==1, `checked=56 drift=0`** ⇒ no battery-vs-counter drift.

## (b) Committed receipt verdict — baseline PASS; uncaught=0 NOT MET (disclosed, honestly reported)
- `baseline_failures=0` for both counters: **PASS**. `controls/mutbat-receipt.txt:36` `mutbat counter=c1 mutants=35 caught=19 equivalent=0 uncaught=16 baseline_failures=0 exit=1`; `:58` `mutbat counter=c2 mutants=21 caught=3 equivalent=0 uncaught=18 baseline_failures=0 exit=1`. Independently reproduced live: do-nothing control on pristine bytes (committed counters, no `--gate`) → `selftest cases=43 failures=0 exit=0` with both green verdicts exact (`total=11 fixed=11 unresolved=0 exit=0`; `fixed=7/7 exit=0`) — `R47MutBattery.draft/baseline-selftest.txt`.
- `uncaught=0` for both: **NOT MET — 16 (c1) + 18 (c2) = 34 survivors**. Per tasking, the seat text asking for `uncaught=0` is superseded by the observed receipt; I do not fabricate a pass. The counts match the frozen disclosures exactly: `claims.json:18` ("C1 35 counter mutants, 19 caught, 16 uncaught, baseline_failures=0"), `claims.json:41` ("C2 21 counter mutants, 3 caught, 18 uncaught"), `freeze.txt:2` ("34 counter-mutant survivors disclosed in claims, not called equivalent"). The 34 coverage gaps stand for wave 2.

## (c) Named mutant re-runs end-to-end — 5/5 caught reproduced; survivor reproduces uncaught
Recipe mirrors `r47-mutbat.py` exactly: copy live `corpus/instruments` to scratch, assert `count(old)==1`, substitute once, run `python3 -I r47-counters-selftest.py --base <export root> --work <scratch>/run --counter <c> --gate <mutated counter>` (`R47MutBattery.draft/mutant-probe.txt`):

| mutant | receipt verdict | observed | match |
|---|---|---|---|
| c1:L1b-always-true | caught | `mutant_failures=1` caught (`cases=20 failures=1 exit=1`) | ✓ |
| c1:L5c-order-inverted | caught | `mutant_failures=1` caught | ✓ |
| c1:L11c-or-verdict | caught | `mutant_failures=1` caught | ✓ |
| c2:H3b-scope-low | caught | `mutant_failures=1` caught (`cases=23 failures=1 exit=1`) | ✓ |
| c2:H6a-counts-loose | caught | `mutant_failures=1` caught | ✓ |
| c2:H7a-verdict-or (bonus survivor) | uncaught | `mutant_failures=0` NOT-CAUGHT (`cases=23 failures=0 exit=0`) | ✓ |

Discrimination vs do-nothing control: pristine bytes → `failures=0`; each caught mutant flips the selftest to `failures=1`, so the detections attribute to the mutation, not a dirty baseline. The H7a survivor reproducing `uncaught` verifies the receipt's survivor list is honest and reproducible at the sampled point.

Coverage finding (not a contract change): c2:H7a-verdict-or (`p.returncode == 0 and ok_line` → `or`) survives the 23-case C2 selftest. The sampled detector does not distinguish this conjunction weakening. The precise masking mechanism was not investigated; equivalence is not established.

## Limitations
1. Bounded probes only: 6/56 mutants re-run; the remaining survivors' status rests on the committed receipt + claims disclosure, not a fresh full run.
2. `grep -Fc` is line-oriented; multi-line old-substrings require an exact substring count (documented in (a)).
3. `--base` semantics footgun for wave-2 replicators: the selftest expects the EXPORT ROOT (the dir containing `corpus/`). Passing the corpus dir crashes at `r47-counters-selftest.py:215` with `FileNotFoundError: .../c1-green/corpus/SOURCES.md` (observed). `--list` mode ignores `--base` entirely.
4. `--list` truncates old/new to 60 chars; full strings exist only in the tables (`r47-mutbat.py:57-116`) — `--list` output alone cannot drive exact substitution.
5. The two r47 counter files are absent from the base export (observed sha256sum file-not-found); the battery's mutation target is the live lane files, which byte-match the freeze pins.
6. Disk guard: `/fast/scratch/hyaku` 53% used, 379.3G free at start — no ENOSPC; scratch `/fast/scratch/hyaku/kasegi-r47/R47MutBattery` removed before yield.
7. Restored/pristine detector leg rerun after mutant-copy disposal: fresh export of the same base, unchanged frozen live counters, same 43-case detector → `selftest cases=43 failures=0 exit=0 restored_exit=0` (`R47MutBattery.draft/restored-selftest.txt`). Scratch removed again in `finally`; printed `scratch_removed=True`. Together with pre/post identical counter hashes, this closes pristine → mutated → restored-pristine evidence without touching production bytes.

## Bounds compliance
No commits/pushes/mutating git or jj commands (only read-only `git archive` of the base commit); writes limited to `w1/R47MutBattery.md`, `w1/R47MutBattery.draft/` (grep-sweep.txt, list.txt, baseline-selftest.txt, mutant-probe.txt) and scratch; fleet repo, `.ufo/state/`, MANIFEST.json, siblings untouched; no `agent://all`; no pacman; no delegation/background jobs (two short bash calls were auto-backgrounded by the harness and their outputs consumed above).
