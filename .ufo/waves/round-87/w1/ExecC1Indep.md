# ExecC1Indep — independent C1 re-derivation (round-87, 12-seat wave)

Seat: ExecC1Indep. Base cd1f568a, C1 landing d87b1b55a51d78411438e962a9abbebdd17930cd.

## 1. Independent selector (own code in scratch, no import of build-map.py / knowledge-meter.py)

- Enumerated backticked bare `S<digits>.txt[:N[-M]]` tokens in all 98
  `corpus/knowledge/*.md` at base via `git ls-tree` / `git show`:
  **93 distinct tokens**.
- Resolved each basename against tracked files under `corpus/source-snapshots/`
  at base (163 tracked files); kept tokens with exactly one holder and anchor in
  range; dropped S020/S021/S023/S025 (QUOTED manifest-field tokens).
- Result: **83 kept, 10 dropped** — S020/S021/S023/S025 (QUOTED) + 6× S041
  (3 distinct captures at base, `candidates=3`).
- Diff vs frozen `.ufo/waves/round-87/c1/repair-map.json`:

  ```
  mine 83  frozen 83
  keys only mine []
  keys only frozen []
  value diffs 0
  IDENTICAL
  ```

**Map verdict: MATCH (83/83 identical keys and values).**

## 2. Frozen counter on `git clone --shared` of C1 landing (census-of-record root)

Command (per claims.json C1 counter, `--lane` = clone under scratch,
`--work` under scratch, all other args as frozen):

```
python3 -B .ufo/waves/round-87/c1/knowledge-meter.py --lane <scratch>/clone-c1 \
  --base-rev cd1f568a6be2656b5f5dc479eb90ef99b91131b5 \
  --map .ufo/waves/round-87/c1/repair-map.json --target 678/1719 \
  --map-sha256 7db928c77efe2f594c0fcbc26174b79db1f60f7a1d244055b679512c778f1eaa \
  --work <scratch>
```

Full output (verbatim):

```
KNOWLEDGE-METER base=596/1720 after=678/1719 target=678/1719 keys=83 mirror_absent=True
LIMB M1 pass after=678/1719
LIMB M2 pass removed=83 keys=83 stray_removed=0 stray_added=0 unrepaired=0
LIMB M3 pass same_files=True bad_lines=0 keys_hit=83
LIMB M4 pass bad=none
LIMB M7 pass quoted_in_map=none quoted_moved=none
LIMB M5 pass out_of_range=none
LIMB M6 pass sha256=7db928c77efe2f594c0fcbc26174b79db1f60f7a1d244055b679512c778f1eaa
KNOWLEDGE-METER-RESULT pass rc=0
```

**Counter rc: 0, KNOWLEDGE-METER-RESULT pass, after=678/1719** (expectation met).

## 3. `--measure-rev d87b1b55...` readings

- At the lane path (`--lane /home/vgpnk/Projects/shokunin/kasegi-shokunin`):
  `KNOWLEDGE-METER rev=d87b1b55... rate=679/1719 pct=39.50 mirror_absent=True` (rc=0)
- On the scratch clone (`--lane <scratch>/clone-c1`):
  `KNOWLEDGE-METER rev=d87b1b55... rate=678/1719 pct=39.44 mirror_absent=True` (rc=0)

Both readings confirm the known +1 at the lane path (r86 CriticRoot); the
census-of-record clone reading is **678/1719**, matching the counter after-state.

## Receipts

`.ufo/waves/round-87/w1/ExecC1Indep-receipts/`: `counter-clone.txt`,
`measure-lane.txt`, `measure-clone.txt`, `my-map.json` (independent 83-key map).

## Summary for L1

- Map verdict: **MATCH (83/83)**
- Counter rc: **0** (pass, after=678/1719)
- `--measure-rev` readings: lane path **679/1719**, clone **678/1719**
- No diff between independent re-derivation and frozen map; no routed defect from this seat.
