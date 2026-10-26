# MutC2Entry — mutation test: F17 entry + harness binding (round 34, wave 1)

Seat: MutC2Entry (mutation-tester, leaf). Scope: F17 knowledge entry
`corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`, its manifest pin
`corpus/source-snapshots/round-34/manifest.json`, capture `corpus/source-snapshots/round-34/S051.txt`,
detectors `corpus/instruments/source-recheck.py` and `corpus/instruments/frontier-recheck-count.py`.
All mutation work ran on isolated scratch copies under
`/fast/scratch/hyaku/kasegi-r34/MutC2Entry/` (lane copies `lane`, `lane-m1`, `lane-m2`, `lane-m3a`,
`lane-m3b`, `lane-m4`, `lane-cur`, `lane-m1b`, `lane-m4b`, plus `pristine-corpus`); the lane repo was
never mutated. Tooling: system `python3` only — no installs (pacman untouched).

## Report

### Pristine baseline (must pass — it does)

Before-hashes (repo bytes, start of session):

```
948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe  corpus/source-snapshots/round-34/manifest.json
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  corpus/source-snapshots/round-34/S051.txt
876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29  corpus/README.md
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
8a79010d557dc9b24c6cd763bc6d2b5f8c3febe0fafde408a8c752107f57499c  corpus/instruments/frontier-recheck-count.py
```

1. `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051` (cwd lane root) → all 18 assertions OK (`Q1 OK occurrences=1 anchor=46-ok` … `Q9 OK occurrences=2 anchor=77-ok`, `Q17 OK occurrences=2 anchor=96-ok`, `Q2 OK normalized=markup-whitespace occurrences=1`), `S051:sha256 OK`, **exit=0**.
2. `python3 corpus/instruments/frontier-recheck-count.py` (cwd lane root) → 20 rows, all PASS incl.
   `PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0`,
   `entries=20 pass=20 exit=0`, **exit=0**.
3. Scratch copy proven byte-identical: `diff -r corpus <scratch>/pristine-corpus` → empty, exit 0; both
   detectors re-run on the scratch copy → same pass results (recheck exit=0; harness `entries=20 pass=20 exit=0`).

### Mutants — each is a single behavior-bearing point (delta proof below)

| # | Mutant point | Detector | Observed | Verdict |
|---|---|---|---|---|
| M1 | drop entry line 3 `source: S051 — …` | harness `--root <scratch>/lane-m1` (and `lane-m1b` on current bytes) | `FAIL F17 knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=- exit=- problems=no-source-line` + `entries=20 pass=19 exit=1`, exit 1 | **killed** |
| M2 | manifest Q1 quote paraphrased: `classify` → `categorize` | source-recheck `--manifest <scratch>/lane-m2/…/manifest.json --source S051` | `S051:Q1 MISMATCH reason=quote-not-found` (all other 17 OK), **exit=1** | **killed** |
| M3a | manifest Q9 `anchor: 77` → `12` (line not holding the quote) | source-recheck on lane-m3a manifest | `S051:Q9 MISMATCH reason=anchor-broken`, **exit=1** | **killed** |
| M3b | manifest Q9 `anchor: 77` → `62` (the *other* occurrence, Blockchain/DLT table) | source-recheck on lane-m3b manifest | `S051:Q9 OK occurrences=2 anchor=62-ok`, **exit=0** | **SURVIVED — coverage finding** |
| M4 | entry recheck line gains unregistered `--source S999` | harness `--root <scratch>/lane-m4` (and `lane-m4b` on current bytes) | `FAIL F17 … ids=S051 exit=- problems=selection-not-declared-by-entry,selection-not-cited-by-entry,manifest-missing-ids` + `entries=20 pass=19 exit=1`, exit 1 | **killed** |

Verbatim commands (mutant lanes; each mutant applied by a one-point edit to its own copy):

```
python3 <S>/lane-m1/corpus/instruments/frontier-recheck-count.py --root <S>/lane-m1; echo exit=$?
python3 <S>/lane-m4/corpus/instruments/frontier-recheck-count.py --root <S>/lane-m4; echo exit=$?
python3 <S>/lane-m2/corpus/instruments/source-recheck.py --manifest <S>/lane-m2/corpus/source-snapshots/round-34/manifest.json --source S051; echo recheck-exit=$?
python3 <S>/lane-m3a/corpus/instruments/source-recheck.py --manifest <S>/lane-m3a/corpus/source-snapshots/round-34/manifest.json --source S051; echo exit=$?
python3 <S>/lane-m3b/corpus/instruments/source-recheck.py --manifest <S>/lane-m3b/corpus/source-snapshots/round-34/manifest.json --source S051; echo exit=$?
```
(`<S>` = `/fast/scratch/hyaku/kasegi-r34/MutC2Entry`.)

Mutant-file after-hashes: entry-m1 `0203a0cc4d64…`, entry-m4 `4e01192694fa…`, manifest-m2
`7d2d25b506a0…`, manifest-m3a `8ad820ded45e…`, manifest-m3b `214e8b4086eb…`. Deltas verified minimal:
M1 `3d2` (one line deleted), M2/M3a/M3b one manifest line each (`"quote": …categorize…`, `"anchor": 12`,
`"anchor": 62`), M4 one recheck line (`--source S051 --source S999`).

### Mid-run instrument drift (sibling seat, not mine)

Between my first copies and the restoration check, `diff -r corpus <scratch>/pristine-corpus` flagged:
`corpus/instruments/frontier-recheck-count.py` `8a79010d…` → `1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249`
(431 → 433 lines; the diff is the docstring's M33-6/R9 `cited`-set wording, lines 115-118 → 115-116 — no executable change),
plus `corpus/instruments/kill-rule-check.py`, `corpus/instruments/README.md`, and `__pycache__` churn — sibling seats'
landings. My four target files (entry, manifest, capture, corpus/README.md) show **no** drift. I re-ran the pristine
harness on the current bytes (`1be79af6…`: `entries=20 pass=20 exit=0`) and re-applied M1/M4 on fresh copies of current
bytes (`lane-m1b`, `lane-m4b`): identical kills (same problem lists, `entries=20 pass=19 exit=1`).
`source-recheck.py` did not change (`fd2e01e8…` before and after), so M2/M3a/M3b verdicts stand on current bytes.

### Coverage findings (for the L1; no contract change proposed)

1. **M3b survivor — anchor pins a window, not the intended occurrence.** B2 anchoring verifies the quote text inside
   `anchor_verdict`'s four-line window (`raw_lines[anchor-1:anchor+3]`); it cannot distinguish *which* occurrence is
   meant. Repointing Q9's `anchor` from 77 (Smart Contracts `Permanent freezing of funds`) to 62 (the identical bullet
   in the Blockchain/DLT table) prints `occurrences=2 anchor=62-ok` and passes. The entry's reading ("the Smart
   Contracts permanent-freezing bullet", Claim 5's Critical-vs-High contrast) would silently re-pin to the wrong
   asset-class table. A guard would need the manifest to pin a distinguishing context line (e.g. the level heading
   line), not just the quote's own window. Recording only; the frozen contract is not mine to change.
2. **Harness blindness is bounded by the recheck line's absolute `cd`.** With `--root <scratch lane>`, the F17 entry's
   recheck line `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …` executes against the real lane, so a
   manifest-quote mutant placed only in the scratch copy is invisible to the harness run (`PASS F17 … exit=0`,
   observed on lane-m2) while source-recheck — the entry's own declared detector, and the detector named in the C2
   counting commands — kills it (M2, exit 1). In the lane itself the mutated manifest *is* the cd target, so the
   harness would catch it as `recheck-exit-1`. Observed artifact of scratch-rooted runs, not a defect in the landed
   binding.

### Restoration evidence

- Repo after-hashes (end of session) — the four files my item touches are byte-identical to before:
  entry `948b202e…`, manifest `d5077f81…`, S051.txt `4fd8ed98…`, corpus/README.md `876be9cc…` (all equal to the
  before-hashes above). `source-recheck.py` `fd2e01e8…` unchanged. Only sibling-seat drift (§ above) differs.
- I never wrote to the lane repo (no mutations outside scratch; running the instruments as `__main__` writes no
  `__pycache__`). Fleet root, sibling lanes, `bounties`, and shokuknow untouched; no jj/git commands run.
- Scratch removed: `rm -rf /fast/scratch/hyaku/kasegi-r34/MutC2Entry && test ! -e …` → `SCRATCH-TREE-REMOVED-AND-ABSENT`.

**Summary: 4/4 assigned mutants killed (M1, M2, M3a, M4) with the pristine entry passing both detectors; 1 bonus
probe survived (M3b) and is reported as a coverage finding. Baseline conclusive; no inconclusive runs.**
