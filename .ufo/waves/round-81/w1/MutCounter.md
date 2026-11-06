# MutCounter — round 81, attempt 1, wave 1 (C1 mutation probe)

Seat: MutCounter (leaf). Claim probed: **C1 depth:verifiability** — the r81 recheck-cwd census
successor's **counter**. Frozen target of this probe:

| file | sha256 (before and after this seat) |
|---|---|
| `.ufo/waves/round-81/c1/mutbat.py` | `fa96223b38f93b5fd9a08d11923dc7f7fe7f35a61b734c0cb3503381062843b4` |
| `.ufo/waves/round-81/c1/recheck-cwd-census.py` (battery target) | `a3b58aa52ba0744199ee97e6bd837e62c499e3e6af03a2fc26f0e6e3746dbec0` |
| `.ufo/waves/round-81/c1/mutant-table.json` (59 rows, 56+3) | `abcc834eb21102f11a11cc91b7482f68957f988ea91e68e803a82251a216d095` |
| `.ufo/waves/round-81/controls/c1-forgeries-r81.py` | `28fde3871e8fc7ead1f9f345dd39ea4779443c3f451003c997acf9cd48539246` |

No frozen byte was edited. All work in scratch `/fast/scratch/hyaku/kasegi-r81/MutCounter/`
(copied in, `TMPDIR` set there, `--work` under scratch, scratch deleted on exit).

## Method — three detectors, one mutant per run

15 mutants, each **one** textual transform of a scratch copy of `mutbat.py`; every anchor was
asserted to occur exactly once in the frozen bytes before writing the mutant
(`make_mutants.py`, occurrence counts recorded in `mutants.json`). Diffs:
`MutCounter-receipts/mutants.diff`.

- **D1 — the counter's own detector**: `python3 -B <mutant> --selftest --work <scratch>` (P8).
- **D2 — the forgery control** (P4's r81 role): `controls/c1-forgeries-r81.py` copied to scratch
  and repointed (`--mutbat <mutant>`, r81 counter over the full 59-row table; the r80 half is
  irrelevant to a mutant of the r81 counter). One `FORGERY` line per forgery; a forgery with
  **rc=0** is a forgery that would pass **P3** verbatim (its summary line is
  `baseline=ok rows=59 killed=56 … neutral_ok=3/3`).
- **D3 — the real battery**: the mutant over the frozen candidate + frozen 59-row table,
  `--expect-cases 22` (run only for D1 survivors — a D1-killed counter cannot be landed).

Control: the **unmodified** copy reproduces the committed control text exactly. All five
`counter=r81` lines of `controls/c1-forgeries-r81.txt` match byte-for-byte in rc and in the
`target_sha256 … neutral_ok=` summary (F1 `killed=0 miskilled=56 neutral_ok=0/3`, F2 `1/3`,
F3 `0/3`, F4 `baseline=bad 0/3`, F5 `killed=56 0/3`; every rc=1), and the frozen candidate
scores `baseline=ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3`
rc0. Receipt: `MutCounter-receipts/control-pristine-forgeries.txt`.

## Results

| mutant | own selftest | forgery rcs (F1..F5) | forgery rc0 | real 59-row battery |
|---|---|---|---|---|
| V1-drop-killcases-filter | rc=1 | 1,1,1,1,1 | none | not run (selftest rc=1) |
| V2-miskilled-as-killed | rc=1 | 1,1,1,1,1 | none | not run (selftest rc=1) |
| V3-exc-any | rc=0 | 1,1,1,1,1 | none | rc=0 ok rows=59 killed=56 … neutral_ok=3/3 |
| V4-exc-class-unguarded | rc=1 | 1,1,1,1,1 | none | not run (selftest rc=1) |
| P1-drop-nofail-conjunct | rc=1 | 1,1,1,1,1 | none | not run (selftest rc=1) |
| P2-drop-exact-line | rc=0 | 1,1,1,1,1 | none | rc=0 ok rows=59 killed=56 … neutral_ok=3/3 |
| P3-drop-traceback | rc=0 | 1,1,1,1,1 | none | rc=0 ok rows=59 killed=56 … neutral_ok=3/3 |
| B1-neutral-broken-as-ok | rc=1 | 1,1,1,1,**0** | **F5-allcases** | not run (selftest rc=1) |
| B2-drop-nneutral | rc=0 | 1,1,1,1,1 | none | rc=0 ok rows=59 killed=56 … neutral_ok=3/3 |
| B3-drop-nkill | rc=0 | 1,1,1,1,1 | none | rc=0 ok rows=59 killed=56 … neutral_ok=3/3 |
| B4-neutral-in-place | rc=1 | 1,1,1,1,**0** | **F5-allcases** | not run (selftest rc=1) |
| R1-drop-killcases-validation | rc=1 | 1,1,1,1,1 | none | not run (selftest rc=1) |
| F1-failline-drop-caret | rc=0 | 1,1,1,1,1 | none | rc=0 ok rows=59 killed=56 … neutral_ok=3/3 |
| F2b-exc-substring | rc=0 | 1,1,1,1,1 | none | **rc=1** killed=**55** dirty=**1** neutral_ok=3/3 |
| F2-failline-drop-detail | rc=1 (crash, no summary line) | 1,1,1,1,1 | none | not run (selftest rc=1) |

Frozen detector tally: **D1 kills 8/15** (7 by a named assertion, 1 by crash), **D3 adds 1**
(F2b) → 9/15 killed, **6/15 survive all three detectors**, and **0/15** inverts the counter's
tally — no mutant produced a forgery that passes P3 except the two that D1 kills.

## Findings

1. **B1 — `if ok_n: tally["neutral_ok"] += 1` → unconditional increment (D2 gap, D1 kill).**
   The stub forgery **F5-allcases** then reaches `neutral_ok=3/3` with `killed=56` and **rc=0**,
   i.e. it reproduces P3's line verbatim. So the five-forgery control set does **not** test the
   neutral-row limb's tallying at all: the only detector that rejects B1 is P8's
   self-selftest, and even there only through one literal assertion
   (`"neutral_ok=0/1" in lines_loc[-1]` on the location toy). If that string assert were ever
   relaxed, B1 would pass P4 *and* P3 with a forgery.
2. **B4 — neutral rows run the target in place (D2 gap, D1 kill).** F5-allcases again reaches
   rc=0 with P3's exact line. D1 kills it, but on a side effect worth naming: `mpath` is only
   the read path — the write below still runs — so the mutant **overwrites the target with the
   neutral mutant bytes** (observed `target_sha256` change from `4cc39d14…` to `9e848f3d…`
   mid-run, `baseline=bad` on the next battery). No frozen-claim consequence (bytes are read
   from disk by the caller), but the transform shows the in-place branch is only safe because
   it does not exist in the frozen counter.
3. **F2b — exception detail matched by substring instead of prefix (D1 miss, D3 kill).** The
   counter's own selftest cannot see it: its only exception FAILs (`T-EXC`, `T-EXCA`) carry
   details that *begin* with `exception=`. The real 59-row table kills it —
   `K-T1 verdict=EXCEPTION-KILL rc=1 fails=2 failed_cases=tmpdir-file,tmpdir-refusal counted=no`,
   landing in `dirty=1`, `killed=55`, rc=1. A live counter regression that only the frozen
   table, not P8, detects.
4. **Six mutants survive all three detectors: V3, P2, P3, B2, B3, F1.** For each, **no forgery
   passes P3** (all five rcs are 1) and D3 returns the pristine line `killed=56 … neutral_ok=3/3`
   rc0, i.e. the defects are invisible on the frozen inputs:
   - **V3** `all(on_target)` → `any(on_target)`: only differs for a row whose kill-case FAILs mix
     `exception=` and non-`exception=` details; the 59-row table has no such row. Effect would be
     `KILLED`→`EXCEPTION-KILL`; on an `assertion` row that lands in `dirty` → rc1 (**fails
     closed**).
   - **P2** dropping the exact `selftest cases=<N> failures=0` anchor: baseline accepts a
     summary-less or miscounted-but-clean run. Fails open only in the baseline limb — a target
     that skips cases still has to survive all 56 kill rows and 3 neutral rows, so no forgery
     exploits it. Untested by P8 and by every forgery.
   - **P3** dropping `"Traceback" not in out` from `clean_pass`: a target exiting 0 with a
     traceback in its output passes baseline. Widest survivor; not reachable by F1–F5 (all exit
     non-zero on the moved copy).
   - **B2** (`n_neutral > 0`) and **B3** (`n_kill > 0`): table-composition guards the self-selftest
     never exercises — it always passes an 8-row table with both kinds present, and the frozen
     table is fixed at 56+3, so these matter only for the counter used with another table.
   - **F1** dropping the `^` anchor from `FAIL_LINE_RE`: a superset matcher, stricter than the
     original (more lines count as FAILs). No forgery exploits it; the residual risk is a false
     `baseline=bad` if a legitimate target echoes `selftest case=X FAIL` mid-line.
5. **Crash mutant F2** (`(?: (.*))?` group deleted while `m.group(2)` is still read): the counter
   dies with `IndexError: no such group` in `fail_lines`, rc=1, **no `MUTBAT` summary line** for
   any target. Killed by crash, not by a verdict; a landed counter in that state fails P3 closed
   (no summary line) but the failure mode is an uncaught internal exception, not a verdict.
6. **Detector attribution.** Every limb that the case-matched kill limb depends on is directly
   exercised: V1 and V2 (the kill_cases filter) and V4 (the exception-class guard) are killed by
   D1's `T-MIS`/`T-EXCA` rows. P1 is killed by D1's baseline-forgery toy (`baseline_forgery_exit=True`).
   R1 by the `validate_rows` bad-table assertion. The two limbs that D1 alone protects — neutral
   tallying (B1) and neutral isolation (B4) — are exactly the ones the forgery set lets through.

## Verdict for C1's instrument

The r81 counter's frozen tally is **not** inverted by any of the 15 probed single transforms: no
forgery reaches P3 except under B1 and B4, and both are killed by the counter's own selftest
(P8). Residual, routed-not-verdict: the neutral-row limb is guarded only by P8's literal-string
assertions (finding 1/2), and the exception-prefix classifier is guarded only by the 59-row
table (finding 3) — both are detector-coverage notes for round 82, not changes to any frozen
predicate.

## Evidence

`MutCounter-receipts/`: `mutants.diff` (single-transform diffs + per-mutant sha256),
`mutants.json` (anchor occurrence counts, hashes), `results.json` (raw D1/D2/D3 output per
mutant), `summary-table.md`, `control-pristine-forgeries.txt` (unmodified-counter reproduction of
the frozen control), `frozen-hashes-after.txt`, and the harnesses `make_mutants.py`,
`run_all.py`, `forgeries-mutant.py` (driver copied from `controls/`, only `--mutbat` added and
the r80 half dropped).

Restoration: the frozen four files hash identically before and after (see
`frozen-hashes-after.txt`); nothing outside `/fast/scratch/hyaku/kasegi-r81/MutCounter/` and this
wave directory was written; scratch removed at exit. No tool installs (no pacman, no network).
