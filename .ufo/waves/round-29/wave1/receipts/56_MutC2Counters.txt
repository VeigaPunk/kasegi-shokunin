# MutC2Counters — C2 counter/harness mutation probe (round-29 wave1)

Seat: MutC2Counters (leaf mutation-tester, no subagents). Date: 2026-10-25.
Answering model: session model `inception/mercury-3` (workstation context; no model was passed —
the task is deterministic tool work, so no model-dependent route choice was made).
Tooling: no installs/upgrades performed (python3 3.x, awk, grep, sha256sum, cp preinstalled;
pacman untouched, per operator rules).

## 1. Subject state (important)

The frozen C2 claim was measured while the wave's build was **still landing**. Live-tree state
changed twice during this session:

- First live counter run (pre-subject): frontier admitted **12** (no F13 row), entries citing
  S04[3-5] **1**, SOURCES rows S043–S045 **0** (registry 42). This is the M28-1 class —
  labeled PRE-STATE, never compared to an after column.
- The subject landed mid-session (README F13 row appended at `corpus/README.md:264` in the
  "Round-29 admission" section; SOURCES S043–S045 rows already present). A second live run at the
  landed digest reproduced the claim exactly: **13 / 1 / 3 / 45 rows, census_exit=0, harness
  entries=16 pass=16 exit=0, source-recheck S043/S044/S045 exit=0**.

Mutation testing ran on a fixture: a byte-for-byte copy of the landed live `corpus/` (sha256 of
README, SOURCES, entry, both instruments, S043.txt captured before), with **no** reconstruction —
the live tree at copy time already contained the full subject. Baseline on the fixture equals the
live landed counts (verified: 13/1/3/45, harness 16/16 exit0, recheck exit0).

## 2. Method

Detector = the frozen C2 counter commands (claims.json `counter_commands`). For each mutant:
run detector on pristine fixture bytes → mutate the smallest behavior-bearing point in the scratch
copy → run detector again → restore exact bytes → run detector again. All work in
`/tmp/mutc2-lane/` (disposable scratch); the live tree was never written.

## 3. Results

### M1 — widen awk frontier pattern to accept a non-admitted row

Mutation (counter 1): `$4 ~ /^ *admitted *$/` → `$4 ~ /^ *[a-z]+ *$/` (any alphabetic status
counts). Data condition: added one non-admitted row (`| F14 | … | proposed | … |`) to the scratch
README behind the F13 row so the widened acceptance is observable.

| run | detector | output |
|---|---|---|
| pristine | `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}'` | **13** |
| mutated | same, `$4 ~ /^ *[a-z]+ *$/` | **14** (F14-proposed counted) |
| restored | pristine again | **13** |

Verdict: **killed — counter flips** (13→14) when a non-admitted row exists. Variant measured:
`$4 ~ /^ *admit/` (drop end-anchor only) → 13, no flip. Coverage note: on the *current* landed
data (zero non-admitted F-rows) even the `[a-z]+` mutant returns 13, so the status filter is only
discriminated when a non-admitted row exists — a negative fixture is absent from the claim's
counter set (a blind spot the counter can only expose given such a row).

### M2 — make `grep -lE '^source: S04[3-5] '` match a partial id

Mutation (counter 2): pattern `^source: S04[3-5] ` → `^source: S04` (partial prefix; matches
S040–S042 and any id whose first three digits are S04; trailing-space requirement dropped).

| run | detector | output |
|---|---|---|
| pristine | `grep -lE '^source: S04[3-5] ' corpus/knowledge/*.md \| wc -l` | **1** (program-severity-ladders-and-reward-scales.md) |
| mutated | `grep -lE '^source: S04' corpus/knowledge/*.md \| wc -l` | **5** (adds iso-29147-and-30111-division-of-labour.md, iso-29147-divergence-and-clause-crosswalk.md, japanese-domestic-disclosure-workflow.md, vendor-disclosure-policy-commitments-crosswalk.md) |

Verdict: **killed — counter flips** (1→5). Variant measured: keep `[3-5]` but drop only the
trailing space (`^source: S04[3-5]`) → 1, no flip (every real `source:` line is followed by
` — `, so the space is always present in current data; a bare terminal `source: S043` id would be
missed by the frozen pattern — same blind spot family).

### M3 — remove the entry file, run frontier-recheck-count.py

Mutation: delete `corpus/knowledge/program-severity-ladders-and-reward-scales.md` from scratch
(F13 stays admitted in the README). Detector: `frontier-recheck-count.py --root <scratch>`.

Actual output: `harness_exit=1`; stdout ends at F12 PASS rows; **no `entries=`/`pass=` line**;
stderr is an uncaught traceback:

```
FileNotFoundError: [Errno 2] No such file or directory:
'/tmp/mutc2-lane/corpus/knowledge/program-severity-ladders-and-reward-scales.md'
  (frontier-recheck-count.py:65, entry_contract → evaluate → main)
```

Verdict: **must-not-pass holds (exit 1) but it crashes — exactly the M28-5 class** (uncaught
FileNotFoundError, exit 1, no verdict line, missing row not named). It does **not** name the
missing row as a clean failure; a graceful fail would be `entries=K pass=K-1` plus a missing-row
note. Restoration: entry restored from pristine copy (sha256 `6beeedd7…` re-matches), harness
rerun → 16/16 exit0.

### M4 — delete one capture, run source-recheck

Mutation: delete `corpus/source-snapshots/round-29/S043.txt` from scratch. Detector:
`source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S043`.

Actual output: `S043:source UNAVAILABLE reason=missing`, **recheck_exit=2** (vs baseline exit 0).
Restoration: S043.txt restored from pristine copy (sha256 `02ecb500…` re-matches), rerun → exit 0.

Verdict: **killed — counter flips** (0→2, clean named reason).

## 4. Fitness table

| mutant | expected detector | actual | verdict |
|---|---|---|---|
| M1 widened awk pattern | 13 → ≠13 when non-admitted row exists | 13→14 | killed (flips) |
| M2 partial-id grep | 1 → ≠1 | 1→5 | killed (flips) |
| M3 missing entry file | must not pass | exit 1 crash, M28-5 class, missing row unnamed | killed (crash) — not a false pass |
| M4 missing capture | must not exit 0 | exit 2 `reason=missing` | killed (flips) |

All four mutants flip their corresponding counter; none survives as a silent change. The two
survivor *variants* (M1 `/^ *admit/`; M2 no-trailing-space) are coverage findings, not contract
changes.

## 5. Restoration evidence

- Scratch is disposable per tasking; every mutant's bytes were still restored to the pristine copy
  and each detector re-run matched the pristine output after restore (hashes: README
  `67d94e80…`, entry `6beeedd7…`, S043.txt `02ecb500…` before/after identical).
- Live tree untouched: sha256 of live README, SOURCES, entry, frontier-recheck-count.py,
  source-recheck.py, S043.txt recorded before and after the session → **`diff` empty, all six
  byte-identical** (`/tmp/mutc2-live-before.sha` vs `…-after.sha`).

## 6. Findings for the L1

1. M28-5 persists on the round-29 C2 harness (M3 reproduced): a row admitted without its entry
   crashes `frontier-recheck-count.py` with an uncaught traceback instead of naming the missing
   entry. Not a false pass, but the harness is not a clean verdict in that state.
2. The frozen counters are sensitive to status/partial-id widening for M1/M2 (flip observed);
   blind spots exist only when (a) a non-admitted frontier row exists (M1), or (b) a `source:`
   line ends at the id with no separator (M2). Neither occurs in current data.
3. Counter stack at the landed digest (recorded, not claimed by this seat): 13 / 1 / 3 / 45 /
   census 0 / harness 16/16 / recheck 0 — matching the claim's predicate values.
