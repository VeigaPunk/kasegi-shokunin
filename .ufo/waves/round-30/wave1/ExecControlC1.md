# ExecControlC1 — Canonical C1 control matrix (round 30, wave 1)

- Seat: `ExecControlC1-2` (L2 leaf, kasegi lane). Axis: depth:verifiability (C1). Milestone: round-30.
- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write scope). Fleet root never written.
- Measured at `2026-10-25T19:22Z` (final runs). All commands run from the lane root; `python3` = `python3` on PATH.
- No tool installed (no pacman/uv/cargo/npm action; RULES.md noted, nothing needed).

## 1. What was measured

The four frozen C1 probes from `claims.json` C1 `counter_commands` were run twice:

| Run | Bytes | Receipt |
|---|---|---|
| BEFORE (run 2) | freeze commit `3c557354` bytes == working tree at run time (digests `c8a62888…` / `9fe6a4a0…`), identical to committed `before.txt` | `.ufo/waves/round-30/c1-controls/before-run-2.txt` |
| AFTER | landed (settled) bytes: `aa60b581…` (frontier-recheck-count.py) / `33602a9d…` (source-recheck.py) | `.ufo/waves/round-30/c1-controls/c1-after.txt` |

Digest movement observed while polling (M29-6 discipline — the after receipt pins the digests immediately before the run, after ≥29 min of stability):

| instrument | freeze | first observed change | settled |
|---|---|---|---|
| frontier-recheck-count.py | `c8a62888…` | `bab0d321…` (~60 s in) | `aa60b581…` (then stable ≥29 min) |
| source-recheck.py | `9fe6a4a0…` | `0b841d5d…` (~60 s in) | `33602a9d…` (after one further edit `72f411b0…` → `33602a9d…`; stable ≥29 min) |

## 2. Before/after table (exit codes + key output lines)

| probe | before (freeze bytes) | after (landed bytes) | kill-rule clause |
|---|---|---|---|
| A1 missing-entry | exit 1 — `FileNotFoundError` traceback, no named-row marker | exit 1 — `FAIL F98 knowledge/zz-missing.md ids=- exit=- problems=missing-entry`, `entries=1 pass=0 exit=1` | a1_exit=1 and output names row id F98 → **satisfied** |
| A2 duplicate-target | exit 0 — `PASS F98`/`PASS F97` dup-entry, `entries=2 pass=2 exit=0` | exit 1 — `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md`, `entries=2 pass=2 exit=1` | a2_exit=1 and output names the duplicate entry → **satisfied** |
| B1 stem-mismatch | exit 0 — `S043:Q1 OK normalized=markup-whitespace occurrences=1` | exit 1 — `S043:manifest MISMATCH reason=stem-mismatch` | b1_exit=1 and reason=stem-mismatch → **satisfied** |
| B2 double-occurrence | exit 0 — `S045:Q1 OK occurrences=2 anchor=MISSING` | exit 1 — `S045:manifest MISMATCH reason=stem-mismatch` | literal clause (exit≠0, failure reason present) → **satisfied**; predicate-sentence semantic (reason=occurrence-not-unique) **not demonstrated by the committed fixture** — see §4 |

## 3. Regression — prove the base passes unchanged

All at the settled bytes (`aa60b581…` / `33602a9d…`):

- `python3 corpus/instruments/frontier-recheck-count.py` on the real corpus → **`entries=17 pass=17 exit=0`**, including `PASS F14 knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0`. All 16 rows that passed at base (census-before: entries=16 pass=16) still pass; the only new row (F14) also passes.
- Per-id `source-recheck.py` sweep across every round manifest (round-23, 24, 25, 26, 28, 29, 30): **every source exits 0**. In particular the base-passing round-29 set S043/S044/S045 still passes (S043 anchors 31/40/170/92 `-ok`, all occurrences=1), unchanged.
- `source-recheck.py --selftest` → `selftest cases=9 failures=0`, exit 0 (covers stem-mismatch, double-occurrence fail, double-occurrence-anchored pass, out-of-range, broken).
- Harness JSON receipt: `entries=17 pass=17 duplicate_entry=null`, exit 0.

No regression found. Kill-rule regression clause satisfied at the round's current final state.

## 4. Finding — B2 fixture does not exercise the occurrence-not-unique limb

The committed `manifest-b2.json` record is `id=S045`, `path="B2.txt"`. The capture file **B2.txt** does contain the quote `vulnerability rating taxonomy crosswalk node` exactly twice (and no anchor), but its file stem (`B2`) ≠ `S045`, so the landed instrument's stem check (checked before occurrence) fires first: `S045:manifest MISMATCH reason=stem-mismatch`. The B2 probe therefore proves the *stem* limb, not the *occurrence* limb.

Falsifiable probe (scratch only, `/tmp/q9scratch`): copying the fixture byte-identically to `S045.txt` and re-pointing the manifest path yields `S045:sha256 OK` then `S045:Q1 MISMATCH reason=occurrence-not-unique`, exit 1 — the occurrence limb exists, fires when the stem matches, and is also covered by `--selftest` (`double-occurrence PASS expected-exit=1`). So the *instrument* limb is present and discriminative; the *fixture* as committed cannot isolate it (a mutant-B2 that drops the occurrence check would still exit 1 on the committed fixture via the stem check). Recommendation for the L1: re-file the B2 fixture with path `S045.txt` (bytes unchanged) so the frozen counter exercises the limb it names — or record the fixture as a stem-mismatch control and add a second B2 fixture for occurrence.

## 5. Scope / evidence

- Writes: `.ufo/waves/round-30/c1-controls/before-run-2.txt`, `c1-after.txt`, `.ufo/waves/round-30/wave1/ExecControlC1.md` (this report). No other lane bytes touched; no git/jj mutation; no fleet-root/shokuknow writes; no live bounty target contacted.
- Freeze bytes materialized via `git show 3c55735:…` into `/tmp` for comparison (read-only).
- Caveat: the after receipt reflects the landed bytes at 19:22Z. If the executor edits the instruments again after this receipt, the pinned digests will not match and the runs must be redone.
