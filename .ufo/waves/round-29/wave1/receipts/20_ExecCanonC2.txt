# ExecCanonC2 — canonical C2 receipt set (round 29 wave 1)

Seat: `ExecCanonC2` (canonical receipt, runs last for C2). UTC: 2026-10-25T18:15–18:16Z.
Lane HEAD at measurement: `46e07f6ae8f23debb10034164252e7027b4d9091` (wave-1 dispatch commit).

## Verdict

**PRE-STATE — the C2 subject has not landed.** Every counter value differs from its frozen
expectation for one reason: the F13 admission (entry + S043/S044/S045 registry rows + round-29
captures manifest) is not yet on disk. Per the M28-1 rule these numbers are labelled PRE-STATE,
the re-run is named below, and none of them is comparable to an after column.

## Subject landing evidence (measured at receipt time)

- `corpus/README.md` frontier table: admitted rows F01–F12 only; **no F13 row**.
- `corpus/SOURCES.md`: registry rows S001–S042 (42 rows); **no S043/S044/S045 rows**.
- `corpus/knowledge/program-severity-ladders-and-reward-scales.md`: **absent**.
- `corpus/source-snapshots/round-29/`: exists (untracked) but holds only `S044.txt` + `S045.txt`;
  **no `manifest.json`, no `S043.txt`**.
- `git status --porcelain`: only `.ufo/waves/round-29/` and `corpus/source-snapshots/round-29/`
  untracked; no corpus file modified. So the subject is mid-flight, not committed.

## Frozen counters — PRE-STATE values

All commands run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

| # | Counter (commands.json C2) | PRE-STATE value | Expected | Verdict |
|---|---|---|---|---|
| 1 | frontier admitted awk | **12** | 13 | DIFFERS — F13 not admitted |
| 2 | `grep -lE '^source: S04[3-5] ' corpus/knowledge/*.md \| wc -l` | **0** | 1 | DIFFERS — entry absent |
| 3 | `grep -cE '^\|[[:space:]]*S04[3-5][[:space:]]*\|' corpus/SOURCES.md` | **0** | 3 | DIFFERS — rows absent |
| 4 | registry rows (census) | **42** | 45 | DIFFERS |
| 5 | census validate exit | **0** (W04 S028/S029 only) | 0 | MATCHES on exit; row count still 42 |
| 6 | frontier-recheck-count harness | **entries=15 pass=15 exit=0** | entries=16 pass=16 exit=0 | DIFFERS on counts (exit matches) |
| 7 | per-id recheck S043/S044/S045 | **exit 2 each** (`manifest UNAVAILABLE reason=missing`) | exit 0 each | DIFFERS — round-29 manifest absent |

All seven discrepancies are fully explained by the single un-landed subject; none indicates an
instrument fault. The harness and census behave exactly as at round 28 (15/15, exit 0; W04 S028/S029).

## Named re-run (required when the subject lands)

Run from the lane root, and capture alongside this file as the AFTER state:

```
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md          # expect 13
grep -lE '^source: S04[3-5] ' corpus/knowledge/*.md | wc -l                                        # expect 1
grep -cE '^\|[[:space:]]*S04[3-5][[:space:]]*\|' corpus/SOURCES.md                                # expect 3
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "census_exit=$?"   # expect exit 0; rows 45
python3 corpus/instruments/frontier-recheck-count.py; echo "harness_exit=$?"                       # expect entries=16 pass=16 exit=0
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S043 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S044 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S045; echo "recheck_exit=$?"   # expect exit 0 each; every manifest assertion occurrences=1
```

Kill-rule check on the re-run: frontier admitted = 13; entries citing S04[3-5] = 1;
S043+S044+S045 rows = 3; registry rows = 45; census_exit = 0; harness entries = 16, pass = 16,
harness_exit = 0; recheck_exit = 0 with no failed manifest assertion.

## Best-effort residues

- The round-29 snapshot dir partially exists (S044.txt, S045.txt, untracked) but without a
  manifest or S043.txt it cannot be rechecked; source-recheck exits 2 (missing base), which is
  the fail-closed behavior, not a false pass.
- No lane file was edited by this seat; this receipt and the md report are the only writes.
- Tooling: no install/upgrade performed (none needed; stdlib + committed instruments only).

## AFTER (POST-STATE) — re-run at the landed subject, 2026-10-25T18:22Z

The subject landed after the PRE-STATE batch (F13 row, S043/S044/S045 registry rows, entry
`program-severity-ladders-and-reward-scales.md`, round-29 manifest + three captures). All seven
frozen counters were re-run from the lane root; lane HEAD still `46e07f6` (subject files landed
uncommitted in the working tree; receipts measure the bytes the counters read).

| # | Counter | AFTER value | Expected | Verdict |
|---|---|---|---|---|
| 1 | frontier admitted awk | **13** | 13 | MATCHES |
| 2 | entries citing S04[3-5] | **1** | 1 | MATCHES |
| 3 | S043+S044+S045 rows | **3** | 3 | MATCHES |
| 4 | registry rows (census) | **45** | 45 | MATCHES |
| 5 | census validate exit | **0** (W04 S028/S029 only) | 0 | MATCHES |
| 6 | frontier-recheck-count harness | **entries=16 pass=16 exit=0** | 16/16/0 | MATCHES |
| 7 | per-id recheck S043/S044/S045 | **exit 0 each** | exit 0 each | MATCHES |

Harness PASS line for the new frontier row:
`PASS F13 knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0`.

Per-id recheck detail: S043 Q1–Q4 all OK (Q1/Q2/Q4 print `occurrences=12 anchor=1-ok` — these
quotes carry manifest anchors the instrument verifies, the Q9 exactly-once-or-anchor binding; Q3
`occurrences=1`); S044 Q1–Q4 all `occurrences=1`; S045 Q1–Q4 all `occurrences=1`. All exit 0.

## Kill-rule verdict (C2)

**PASS.** frontier admitted = 13; entries citing S04[3-5] = 1; S043+S044+S045 rows = 3; registry
rows = 45; census_exit = 0; harness entries = 16, pass = 16, harness_exit = 0; recheck_exit = 0
per id with no failed manifest assertion. The dated S043 12-occurrence quotes are Q9-anchored,
not an assertion failure.

## Final state note

- The receipt `receipts/ExecCanonC2.txt` contains both labeled states (PRE-STATE 18:15Z,
  POST-STATE 18:22Z) per R3; the PRE-STATE numbers are never compared to the after column.
- No lane file was edited by this seat; the only writes are this report and the receipt.
- Tooling: no install/upgrade performed.

## FINAL (POST-STATE, stabilized bytes) — 2026-10-25T18:25Z

`ExecEntryF13` then stabilized the round-29 manifest/capture bytes (manifest
`910608e6…`; S043 record-scoped `d3b815…`; S044/S045 unchanged; entry `6c05c98f…`).
All counters re-run at these bytes: frontier 13, entries 1, rows 3, registry 45, census exit 0
(W04 S028/S029 only), harness `entries=16 pass=16 exit=0`, per-id rechecks exit 0 each. S043
Q1–Q4 now all `occurrences=1` with verified anchors (31/40/170/92); S044/S045 Q1–Q4 all
`occurrences=1`. All 12 manifest assertions exactly-once.

**Final kill-rule verdict (C2): PASS** at the stabilized bytes, with the PRE-STATE (18:15Z) and
intermediate POST-STATE (18:22Z) runs preserved above as labeled replay states (R3).
