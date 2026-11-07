# ExecC1Indep — round-92, one v1 wave of 13 seats

Independent re-measurement of C1 tranche 7 from committed bytes. Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Scratch root `/fast/scratch/hyaku/kasegi-r92/ExecC1Indep` — **deleted before this yield** (report written after cleanup; nothing of mine remains outside the wave dir).

## Method
- `git clone --shared` of the lane into `$S/c`; asserted `git rev-parse --show-toplevel` == `$S/c`; clone HEAD = `ee830069af1255043aeb39f1d324e6b3e5d69dbd` (receipts commit). All meter runs read-only against that clone, `python3 -B`, `--work $S`.
- Frozen meter (lane's frozen `knowledge-meter.py`, frozen map/labels/revs/sha pins) run three ways: landing, do-nothing, plus the full pre-freeze controls script.
- Independent byte check written from scratch (`ExecC1Indep-receipts/ExecC1Indep-verify.py`): imports nothing from the counter; derives expected edits from the 30 label rows at `d0bd4758a41919b2c86c079f3a1a2dfb392dcd8d` and compares `git show` bytes of base `0628fd24` vs landing `cb1ef2b9` directly.

## Results — all AGREE with the landing receipt
1. **Frozen meter in clean clone**: `KNOWLEDGE-METER-RESULT pass rc=0`; base `947/1947` → after `960/1944`; every `KNOWLEDGE-METER`/`HOST`/`LIMB` line identical to `.ufo/waves/round-92/l1/c1-landing-r92.txt` (receipt `ExecC1Indep-meter-main-r92.txt`).
2. **Do-nothing control** (`--after-rev` = base): `fail rc=1` with `M1 FAIL after=947/1947`, `M3 FAIL bad_lines=25` — the meter rejects the un-landed tree (receipt `ExecC1Indep-meter-do-nothing-r92.txt`).
3. **Controls script rerun** (`c1-controls-r92.sh lane $S/ctl`, rc=0): all 11 controls reproduce; after masking the `after=<sha>` commit ids in the `== control` headers, the full LIMB/RESULT body is byte-identical to the committed `c1-controls-r92.txt` — candidate `pass rc=0`, the ten mutants (`no-work`, `partial-24-of-25`, `partial-own-map`, `skip-qualify-59-own-map`, `excluded-437-applied`, `no-edit-qualified`, `named-cell-155-token-only`, `drop-token-58-as-dash-cell`, `wrong-key-column-86`, `working-tree-only`) all `fail rc=1` (receipt `ExecC1Indep-controls-rerun-r92.txt`).
4. **Independent byte check** (receipt `ExecC1Indep-verify.txt`): `BYTE-CHECK pass (problems=0)`, `RECEIPT AGREE`.
   - labels=30; mapped=25; unmapped=5 — the 3 no-edit pairs (`citation-bases.md:14` ×2, `japanese-domestic-disclosure-workflow.md:7`) and the 2 EXCLUDED pairs (`triage-thresholds.md:437`, `:438`) — all byte-identical base→landing.
   - Every mapped site: `old` occurs exactly once on its base line and the landing line equals `base_line.replace(old, new, 1)` — nothing else on any line moved. Map old/new match what each label names for every kind: range=10, qualify=7, drop-token=2 (58/144), dash-cell=2 (369/370), named=2 (150/152), named-cell=2 (155/249). Map sha256 matches the frozen pin `6d87cafa…b772`.
   - Whole `corpus/knowledge` tree: identical file sets; per file identical line counts; changed lines exactly `triage-thresholds.md` [58, 59, 86, 87, 90, 144, 146, 149, 150, 152, 153, 154, 155, 177, 249, 280, 281, 367, 369, 370, 390, 445, 456, 458] (24) and `root-loss-2026-10-12.md` [68] — exactly the receipt's P3 paths, no other line changed.

## Qualifiers
- The scope totals `947/1947 → 960/1944` are reproduced via the frozen counter (twice, plus controls), not recomputed from `resolve.py` classification by my own code; the byte-level tranche claims above are fully independent of the counter.
- No routed defects found; no tool installs or upgrades performed (none needed; pacman untouched).

## Files written (all under `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-92/w1/`)
- `ExecC1Indep.md` (this report)
- `ExecC1Indep-receipts/ExecC1Indep-verify.py` — independent checker source
- `ExecC1Indep-receipts/ExecC1Indep-verify.txt` — checker output (BYTE-CHECK pass, RECEIPT AGREE)
- `ExecC1Indep-receipts/c1-landing-r92.txt` — landing receipt copy cited above
- `ExecC1Indep-receipts/ExecC1Indep-meter-main-r92.txt` — frozen-meter rerun output
- `ExecC1Indep-receipts/ExecC1Indep-meter-do-nothing-r92.txt` — do-nothing control output
- `ExecC1Indep-receipts/c1-controls-r92.txt` — committed controls output copy cited above
- `ExecC1Indep-receipts/ExecC1Indep-controls-rerun-r92.txt` — controls rerun output

No credential-shaped values in any wave file; scratch dir removed.
