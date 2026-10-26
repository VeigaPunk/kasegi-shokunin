# MutFRExisting — mutation probe of frontier-recheck-count.py (round-31 wave 1)

Date: 2026-10-25 (live-lane runs 23:33–23:36 UTC). Seat: MutFRExisting (mutation-tester, leaf).
Target: `corpus/instruments/frontier-recheck-count.py` — mutated in scratch only; lane read-only.
Lane HEAD at probe time: `8a8916c7043bd873d191b30dd1744b241b91f4d9` (read-only `git rev-parse`).
Pristine sha256: `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893`.
Scratch: `/tmp/mutfrexisting/` (fleet-root `.scratch` untouched). No tools installed (operator rule 5: nothing to record).

PRE-STATE label (bounds 6): live-lane runs below ran before S048/F15 landed — live README listed F01–F14, 17 admitted entries, registry still pre-48. Live vs FROZEN outputs were identical at probe time, so the frozen-corpus columns are the comparative ones.

## Method (bounded detector, fixed before runs)

Detector = the exact triple (exit code, stdout, stderr) of
`python3 <script> --root <R> 2>&1-captured-separately`. A mutant is **killed by oracle R** iff its
triple for R differs from pristine's triple for R; **survivor** iff triple-identical on every oracle.

Oracles:
- LIVE: `--root /home/vgpnk/Projects/shokunin/kasegi-shokunin` (PRE-STATE)
- FROZEN: `--root /tmp/mutfrexisting/frozen` (`cp -a` of lane `corpus/` at probe time; deterministic)
- A1: `--root .ufo/waves/round-30/c1-controls/harness-root-a1` (missing-entry control)
- A2: `--root .ufo/waves/round-30/c1-controls/harness-root-a2` (duplicate-realpath control)

Mutants built by exact-string replacement on the pristine bytes; each `find` asserted to occur
exactly once; every mutant passed `py_compile` (no invalid:nocompile). Diffs below.

## Pristine baselines (all four roots)

LIVE and FROZEN, byte-identical outputs: 17 rows F01–F14 all `PASS ... exit=0`, ending
`entries=17 pass=17 exit=0`, process exit 0. (Seat-predicted oracle confirmed.)

A1:
```
FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry
entries=1 pass=0 exit=1
exit=1
```
A2:
```
PASS     F98  knowledge/dup-entry.md                               ids=S003           exit=0
PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0
DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md
entries=2 pass=2 exit=1
exit=1
```

## Verdict table

| mutant | edit (single point) | killed by | survivor on |
|---|---|---|---|
| mut1-drop-missing-entry-marker | `evaluate()` None-branch: `"problems": ["missing-entry"]` → `"problems": []` (status stays `FAIL`) | **A1 — stdout only; exit unchanged 1→1** | LIVE, FROZEN, A2 |
| mut2-drop-duplicate-realpath | main(): duplicate-detection `if rp in seen_realpath:` block → `pass` | **A2** (exit 1→0, `DUPLICATE-ENTRY` line gone) | LIVE, FROZEN, A1 |
| mut3-accept-source-less | `problems.append("no-source-selection")` → `pass` | — none — | **SURVIVOR** on LIVE, FROZEN, A1, A2 |
| mut4-accept-true-selftest | `elif "source-recheck.py" not in recheck or "--selftest" in recheck:` → `elif False:` | — none — | **SURVIVOR** on LIVE, FROZEN, A1, A2 |
| mut5-missing-entry-pass | None-branch: `"status": "FAIL"` → `"status": "PASS"` | **A1** (exit 1→0, `entries=1 pass=1 exit=0`) | LIVE, FROZEN, A2 |

## Observed deltas (changed roots only; all other roots triple-identical)

mut1 @ A1 (exit stays 1 — row line loses `problems=missing-entry`; killed only by a stdout-sensitive oracle):
```
FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-   
entries=1 pass=0 exit=1
exit=1
```
mut2 @ A2:
```
PASS     F98  knowledge/dup-entry.md                               ids=S003           exit=0   
PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0   
entries=2 pass=2 exit=0
exit=0
```
mut5 @ A1:
```
PASS     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry
entries=1 pass=1 exit=0
exit=0
```

## Survivor proofs (mut3/mut4 are live mutants, not equivalent — synthetic probe roots in scratch)

Neither LIVE nor A1/A2 contains an admitted row exercising these routes (grep: zero `recheck:` lines
with `--selftest` under `corpus/`; all 17 admitted entries carry `--source`). Probe roots built under
`/tmp/mutfrexisting/probe-*/` (one admitted row; a2's S003 manifest + capture; lane `source-recheck.py` copy):

probe-sourceless entry line: `recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json` (no `--source`, whole-manifest run)
```
pristine @ probe-sourceless: FAIL ... problems=no-source-selection / entries=1 pass=0 exit=1 (exit 1)
mut3    @ probe-sourceless: PASS F98 ... exit=0 / entries=1 pass=1 exit=0 (exit 0)
```
probe-true entry line: `recheck: true --source S003 --manifest corpus/source-snapshots/round-24/manifest.json`
```
pristine @ probe-true: FAIL ... problems=not-a-recheck-invocation / entries=1 pass=0 exit=1 (exit 1)
mut4    @ probe-true: PASS F98 ... exit=0 / entries=1 pass=1 exit=0 (exit 0)
```
So both defects are reachable and behavior-bearing; they survive only because today's oracles lack a
row on those routes. That is a coverage gap, not evidence the guards are dead code.

Scoping note: "drop the missing-entry named-row error" (assigned mutant 1) was implemented as the
smallest behavior-bearing point that loses the named-row marker while still failing closed. The
alternative reading (remove the None guard entirely → uncaught `TypeError` traceback, violating the
docstring's no-traceback guarantee) was not probed — assigned list capped at five.

## Diffs

Unified diffs of every mutant vs pristine are reproduced in `/tmp/mutfrexisting/mut{1..5}-*.diff`;
the five edits are exactly the single points listed in the verdict table (each verified
occurs-exactly-once before replacement, all `py_compile` clean).

## Restoration evidence

- Before = after sha256 of the lane instrument: `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893`.
- `git -C <lane> status --porcelain -- corpus/instruments/frontier-recheck-count.py` → empty (exit 0).
- Restored-bytes detector re-run on the lane file itself: `entries=17 pass=17 exit=0`, exit 0 (matches baseline).
- All mutations lived only in `/tmp/mutfrexisting/*.py`; no lane byte was written by this probe.

## Findings for ExecFRLimbs (also messaged)

1. **mut3 survivor**: the `no-source-selection` guard has no oracle today. A fixture root with one
   admitted row whose recheck line is a whole-manifest `source-recheck.py` run (valid `--manifest`,
   no `--source`) kills it: pristine `FAIL problems=no-source-selection`, mutant `PASS`/exit 0.
2. **mut4 survivor**: the invocation-shape guard (`source-recheck.py` prefix / `--selftest`) has no
   oracle today. A fixture row with `recheck: true --source S003 --manifest <valid>` (or a
   `--selftest` variant) kills it: pristine `FAIL problems=not-a-recheck-invocation`, mutant PASS.
3. **mut1 kill-signal shape**: dropping the `missing-entry` marker leaves exit 1 intact on A1 — the
   C1 ledger's `kill`/`signal` for a missing-entry limb MUST inspect stdout (e.g. signal
   `problems=missing-entry`), an exit-only kill command survives this mutant.
4. FR-missing-entry (mut5 route) and FR-duplicate-entry (mut2 route) are well-covered by A1/A2 as-is.
