# ExecHarnessAfter — round-30 wave-1 harness-after receipt

Seat: `ExecHarnessAfter` (L2 executor, leaf). Milestone round-30, wave-1 v2. Axes:
`coverage` (C2). Assignment: after the F14 row, entry, registry rows and round-30 manifest
all exist, run `frontier-recheck-count.py` and the per-id `source-recheck.py` S046/S047/S041
runs, save outputs to `.ufo/waves/round-30/harness-after.txt`, and report.

## 1. Prerequisites — poll timeline

Polled every 30s (ceiling 60 min) with `grep` for the F14 row in `corpus/README.md`,
`test -f` for the entry and for the round-30 manifest:

| poll | UTC | F14 row | entry | manifest |
|---|---|---|---|---|
| 1–2 | 18:50:01–18:50:31 | 0 | no | no |
| 3 | 18:51:01 | 1 | no | no |
| 4–5 | 18:51:31–18:52:01 | 1 | no | yes |
| 6 | 18:52:31 | 1 | yes | yes — ALL-PRESENT |

No fabricated wait; the run below measured the bytes present after ALL-PRESENT.

## 2. Bytes measured (sha256, at run time)

```
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f  corpus/instruments/source-recheck.py
dfc8835750bbdcbc2480fc579f7204ba8215d3018d0bd0942e4ea97f3e5e75a6  corpus/source-snapshots/round-30/manifest.json
f584f06c74942a36d9bce6bb97adcb7ab3bd1b2b0503faf8a68d5c60f4494a32  corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md
884481f3781e200d4c7e6efd91b2912ada513fa126c534d3392ccd48003a03a3  corpus/source-snapshots/round-30/S046.txt
bcf4f605d75909301f02560df894e0c4c15d97c7928a1759f57b15b5a7d905f4  corpus/source-snapshots/round-30/S047.txt
e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47  corpus/source-snapshots/round-30/S041.txt
```

`S041.txt` digest equals the round-28 capture digest (`e18acbf9…`, per ScoutAssimPackage §6) —
the reuse recorded in the wave spec.

## 3. Assigned instrument runs (output saved to `.ufo/waves/round-30/harness-after.txt`)

### 3a. `python3 corpus/instruments/frontier-recheck-count.py`
- **17/17 admitted rows PASS**, `entries=17 pass=17 exit=0`, `harness_exit=0`.
- F14 row: `PASS F14 knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0`.
  Note: the instrument prints the declared id set sorted lexicographically, so the printed order
  is `S041,S046,S047`; the set is exactly the claim's `{S046,S047,S041}` (same three ids).
- All prior rows (F01–F13) unchanged PASS vs census-before plus F13.

### 3b. `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source S04X`
| id | output | exit |
|---|---|---|
| S046 | sha256 OK; Q1–Q4 all `occurrences=1` (Q3/Q4 normalized=markup-whitespace) | 0 |
| S047 | sha256 OK; Q1 `occurrences=3 anchor=123-ok`, Q3 `occurrences=2 anchor=130-ok`, Q2/Q4/Q5 `occurrences=1` | 0 |
| S041 | sha256 OK; Q1–Q3 all `occurrences=1` | 0 |

All assertions exactly-once or anchor-verified (Q9); every quoted occurrence count printed.

## 4. C2 counter cross-check (kill-rule clauses measured)

| counter | expected (after) | measured |
|---|---|---|
| frontier admitted rows (awk) | 14 | **14** |
| entries citing S04[6-7] (grep -l) | 1 | **1** |
| S046+S047 registry rows (grep -c) | 2 | **2** |
| registry total rows | 47 | **47** |
| sources census `validate` | exit 0 | **exit 0** (W04 S028/S029 only) |
| frontier harness | entries=17 pass=17 exit=0 incl. F14 | **17/17 exit=0**, F14 PASS |
| source-recheck S046/S047/S041 | each exit 0 | **0 / 0 / 0** |

Every C2 predicate clause this seat can measure is satisfied at the landed bytes.

## 5. Scope / safety / tooling

- Wrote only `.ufo/waves/round-30/harness-after.txt` and this report, both inside the lane repo.
- No git/jj mutation, no fleet-root/`shokuknow` write, no network traffic (all runs local
  against committed captures; no live target contacted).
- Tooling installs: none (no tool installed/upgraded by this seat).

## 6. Risks / notes

- The instrument output order `ids=S041,S046,S047` differs from the claim text's
  `ids=S046,S047,S041`; byte-for-byte string equality against the claim line would fail, but the
  semantics (same id set, exit 0) hold. Flagging so the L1 does not read this as a mismatch.
- `S047` Q1/Q3 quotes occur 3×/2× and carry verified anchors (`123-ok`/`130-ok`); the
  source-recheck instrument prints the occurrence counts it observed, per Q9.
- This receipt measures the working-tree bytes at the time of run (section 2). Post-integration
  re-runs at the commit belong to `ExecPostCommitRecheck`, as in round 29.
