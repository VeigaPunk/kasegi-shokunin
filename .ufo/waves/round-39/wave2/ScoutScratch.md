# ScoutScratch — round 39 wave 2 (falsify): post-wave scratch audit

Seat: ScoutScratch (scout, leaf). I wrote none of the work under attack. Deliverable: `.ufo/waves/round-39/wave2/ScoutScratch.scratch.txt` (full listing, sizes, df, /tmp scan, demonstrations).
Scan: 2026-10-26T20:13:59Z and 20:15:52Z. Lane head at scan Y = `5006097a84305267c9a3e8c1e1d560e60fe41d37`; J = `46c66c268502abd1b2c342fc71bf88ccf721845b`. Tools installed: none.

## Result (target: C1 kill-rule clause "any leftover kasegi-r37/r38/r39 scratch entry at filing")

| root | state at 20:15:52Z |
|---|---|
| `/fast/scratch/hyaku/kasegi-r37` | absent |
| `/fast/scratch/hyaku/kasegi-r38` | absent |
| `/fast/scratch/hyaku/kasegi-r39` | 33 top-level entries: 32 live wave-2 seat dirs (created 17:13–17:15 host-local, owners running) + `gates-work` |
| `/fast/scratch/hyaku/kasegi-r39-l1` | present, 15 files, 33845 B |

`df -h /fast/scratch/hyaku`: `/dev/nvme1n1p2 804G 189G 615G 24% /fast` (first scan 186G used, 619G avail). Disk guard green. /tmp: no file over 50 MB (`find /tmp -xdev -size +50M` empty); no kasegi wave-era file in /tmp (the r39 files there belong to kaidoku).

## Defects (by owner)

1. **`kasegi-r39/gates-work`** — 82137 B, mtime 17:12, no process, no seat. It is the `--work` dir named in the committed receipt (`final-gates/all-gates.txt` G6: `r39=present,work=inside,tolerated=/fast/scratch/hyaku/kasegi-r39/gates-work`). Owner: L1 KasegiR39 (all-gates run). Holds `r37-pinned/r37-closure.sh` (73132 B, 16:59), `r37/live-lines.txt`, `st/` (7 forge/selftest files) and three empty dirs. Counts under the kill rule unless removed before filing; the receipt was green only because G6 excuses the run's own `--work`.
2. **`/fast/scratch/hyaku/kasegi-r39-l1`** — L1 working dir (drafts, `run-J.txt`, `selftest-J.txt`, `verify-Y.txt`). Owner: L1 KasegiR39. G6 only matches the exact names `kasegi-r37`/`kasegi-r38`/`kasegi-r39`, so this dir is invisible to the suite (Run D below). Remove before filing.
3. The 32 live seat dirs are not defects now; the filing scan must be re-run after the last seat exits (heaviest: CritG2Exploit 1.29 GB, CritC1Kill 288 MB, CritBaseControl 254 MB). ScoutScratch's own dir was removed before the final scan (absent in the listing).

## Suite observations (this seat's runs; all scratch under my own dir, removed after)

- Run A `--export-ref J --work $S/w`: G2 `receipt=0` (matches E4: J run is 7/8 by construction), G6 red, G8 red → `closed=5/8 exit=1`. (My own stray `run.out` in my scratch dir made G6 say `tolerated=none`; I removed it afterwards. The chain rule "only the next path component below the tolerated parent" is strict, as documented.)
- Run B `--export-ref Y`: G1,G2,G3,G4,G5,G7 `closed=1`; G2 payload `receipt=1 … graded-cases=8 … final-lane-commit=0`; G6 `closed=0` (`r39=present`: gates-work + sibling seats, live); G8 `closed=0` → `closed=6/8 exit=1`.
- Run C: pinned r37 suite (`git show 2387dcf6…:corpus/instruments/r37-closure.sh`) at Y → `closed=13/14 exit=1`, E9 `status-dirty=5` (five untracked wave-2 entries in the lane). So G8 (and C1's `closed=8/8` at Y) is only green with a clean lane tree and an empty scratch root: both are filing preconditions the L1 must satisfy, and neither holds now. Not a suite defect.
- Run D `--scratch-root $S/root` holding only `kasegi-r39-l1/f`: `G6 payload=r37=absent,r38=absent,r39=absent,work=outside,tolerated=none,read=ok closed=1` — a `kasegi-r39-<suffix>` leftover passes G6 (name-scope gap; the L1's own `kasegi-r39-l1` is a live instance).
- Run E root holding file `kasegi-r39/leftover`: G6 `r39=present closed=0` (fail-closed, correct) but stderr leaks `r39-closure.sh: line 893: cd: …/leftover: Not a directory` (same pattern at `g6_chain_ok` line 555, `real=$( cd "$e" && pwd -P )` on a non-directory). Verdict unaffected; cosmetic noise.
- G6 design note: a caller-supplied `--work` under `kasegi-r39` is never removed by the suite (`cleanup()` removes `export/ mut/ r37/ r37-pinned/` only; `WORK_AUTO=0`), so the receipt run itself manufactures the leftover that the kill rule forbids unless the caller deletes it. In `gates-work`, `r37-pinned/` and `r37/` dated 16:59 are still present although `cleanup` would `rm -rf` them on a normal exit (observation only; cause not established — a killed earlier run is one explanation, [INFERENCE]).

## Verdict

C1 kill-rule clause: **would trip right now** on `gates-work` and `kasegi-r39-l1` (L1-owned) and the live seat dirs; none is a seat defect except those two. Required before filing: remove `gates-work` and `kasegi-r39-l1`, let all seat dirs clear, re-scan, and run the filing gates on a clean lane tree.
