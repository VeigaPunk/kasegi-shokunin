# C1InstrumentDigest — wave-2 falsification report

**Item:** recompute the final C1 instrument digest and compare it with each C1 receipt/index.
**Attack date (UTC):** 2026-10-25T09:01Z. Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
**Tool installs:** none (sha256sum, python3, git — all preinstalled). Pacman untouched.

## Verdict

**CONFIRMED — no defect found.** The claimed final digest
`c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f` is the digest of
the bytes on disk now, it is the only `instrument_sha256` value pinned by any C1
strict receipt, and re-running the instrument at that digest reproduces all three
committed strict receipts **JSON-byte-for-JSON-byte** (including every per-entry
`lane_output_sha256`/`foreign_output_sha256`) and every summary line in
`c1-receipt-index.txt`. The do-nothing kill-rule outcome (pass=6, exit=1) was
re-derived under the final digest directly.

## Attack axes

1. **Pin consistency** — is `c3c19adc…` the only digest the evidence pins, and does it match disk?
2. **Reproduction under the pinned sha** — do the receipts regenerate from the pinned bytes?
3. **Snapshot integrity** — are the receipted roots the bytes they claim (git base / frozen 35 / live 37)?
4. **Kill-rule under final digest** — does the do-nothing control still fail under `c3c19adc`?

## Commands, outputs, exits

### 1. Recompute the live digest

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum corpus/instruments/recheck-audit.py
c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f  corpus/instruments/recheck-audit.py   (exit 0)
```

Matches `c1-instrument-digest.txt:1` (`instrument=c3c19adc…`),
`c1-receipt-index.txt:3` (`instrument_sha256=c3c19adc…`), and
`claims.json:49` (`receipts before/after on final instrument digest c3c19adc…`).
File is 15065 B, mtime 2026-10-25 05:54:21 -0300 — **before** the digest file
(05:54:26), index (05:54:27), and all three strict receipts (05:54:23–05:54:26).
Unchanged since receipt capture.

### 2. Census of every pinned digest in the receipt set

```
$ grep -rh '"instrument_sha256"' .ufo/waves/round-25/ | sort | uniq -c
      3  "instrument_sha256": "c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f",
```

Exactly three pins, all `c3c19adc`: `c1-before-strict.json:2`,
`c1-after-35.json:2`, `c1-after.json:2`. No receipt pins a stale digest.
`c1-before.json` and `c1-controls/*.json` carry no `instrument_sha256` field
(pre-strict schema; see residual risk).

### 3. Selftest at the pinned digest (index line 4 claims `cases=14 failures=0 exit=0`)

```
$ python3 corpus/instruments/recheck-audit.py --selftest
selftest basestate.md  pass want=True  got=True  | strict want=True  got=True  ok
selftest parseonly.md  pass want=False got=False | strict want=False got=False ok
selftest instonly.md   pass want=True  got=True  | strict want=False got=False ok
selftest completeness lines=13 total=15 complete=False ok
selftest cases=14 failures=0 exit=0
EXIT=0
```

Matches `c1-receipt-index.txt:4` exactly.

### 4. Reproduce each committed receipt under the pinned digest

`--cdroot` is required for the two snapshot runs because the receipts record
`cdroot=<lane root>` (instrument line 121: `strict["cdroot"]` compares the line's
`cd` target to `--cdroot` or `--root`; `c1-before-strict.json` records
`cdroot=/home/vgpnk/Projects/shokunin/kasegi-shokunin`).

```
$ python3 corpus/instruments/recheck-audit.py --root .ufo/waves/round-25/c1-controls/base \
    --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin --json /tmp/c1bs-rerun2.json
strict pass=6/35 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=12 gated=0 broken=23  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=35 total=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1   EXIT=1

$ python3 corpus/instruments/recheck-audit.py --root .ufo/waves/round-25/c1-after-35 \
    --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin --json /tmp/c1a35-rerun2.json
strict pass=35/35 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=12 gated=23 broken=0
lines=35 total=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0   EXIT=0

$ python3 corpus/instruments/recheck-audit.py --json /tmp/c1-after-rerun.json
strict pass=37/37 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=14 gated=23 broken=0
lines=37 total=37 pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0   EXIT=0
```

All three summary triples are verbatim the index lines
(`c1-receipt-index.txt:7-9`, `:12-14`, `:17-19`). First run without `--cdroot`
reproduced the frozen summary but `cdroot_fail=5/34` — the flag is load-bearing;
with it, strict tallies match.

JSON deep-diff (every top-level field + all 35/35/37 per-entry records incl.
`command`, `limbs`, `strict`, `lane_exit`, `foreign_exit`,
`lane_output_sha256`, `foreign_output_sha256`, `missing_paths`, `cd_target`,
`class`, `pass`, `pass_strict`):

```
c1-before-strict.json: IDENTICAL
c1-after-35.json:      IDENTICAL
c1-after.json:         IDENTICAL
```

Text receipts: `diff` shows the committed `.txt` files are my re-run output plus
one appended trailer (`c1-before-strict_EXIT=1`, `c1-after-35_EXIT=0`,
`c1-after_EXIT=0`); receipt bodies otherwise byte-identical, and each trailer
matches the observed exit code.

### 5. Do-nothing control under the final digest (kill rule)

```
$ python3 corpus/instruments/recheck-audit.py --root .ufo/waves/round-25/c1-controls/do-nothing \
    --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet --json /tmp/dn-rerun.json
strict pass=6/35 … lines=35 total=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1   EXIT=1
instrument_sha256: c3c19adc… ; pass: 6 ; pass_strict: 6 ; lines: 35
```

Kill rule (`claims.json:19`: claim void if control scores pass=35) survives —
pass=6≠35 under the actual final digest. Frozen-limb summary identical to the
committed `c1-controls/do-nothing.json` (`lines=35 pass=6 fail_closed=23`).

### 6. Snapshot-tree integrity

```
$ for f in c1-controls/base/corpus/knowledge/*.md: cmp vs git show b49948f:corpus/knowledge/<n>
base snapshot: 35 files, 0 mismatches vs git base           (b49948f = claims.json:5 base_revision)
$ ls c1-after-35/corpus/knowledge | wc -l → 35 ; byte-diff vs live corpus/knowledge → 0 mismatches
$ ls corpus/knowledge | wc -l → 37 ; diff of listings → live adds only
  vendor-disclosure-policies-as-corpus-objects.md
  vendor-disclosure-policy-commitments-crosswalk.md         (the two C2 entries)
```

So `c1-after-35` (frozen surface, `lines=35 total=35`) and `c1-after` (final
tree, `lines=37 total=37`) are measured on the trees they claim; the 35-vs-37
split in `claims.json:50` and the index is real.

## Residual risk / verification gaps

- **Instrument is untracked in git** (`git status`: `?? corpus/instruments/recheck-audit.py`;
  the file has no `git log`). The pinned sha is self-verifying today and the
  receipts embed the producing sha (`recheck-audit.py:269-272` hashes `__file__`
  at runtime), but if the worktree file were lost the pinned bytes could not be
  recovered from VCS. Smallest correction: commit the instrument file; no
  production edit made here (read-only scope).
- **Controls (`c1-controls/*.json`, `c1-before.json`) embed no
  `instrument_sha256`** — produced by pre-strict revisions during the documented
  churn (`8ab4dff7 → 8c3771e1 → c3c19adc` per wave-1 reports). Their
  frozen-limb outcomes were re-derived under `c3c19adc` above and are identical;
  gap is provenance metadata, not outcome.
- **Wave-1 reports pin earlier shas** (`wave1/SentinelCapture.md`, `CritPredicate.md`
  list `d07af435/efbd18ee/4475d2e6/1ccee066/8ab4dff7/8c3771e1` with timestamps).
  These are accurate-as-of-write historical records, not contradicted: the
  instrument churned after those reports closed and every *receipt* was
  regenerated at the final digest.
- `c1-instrument-digest.txt` pins only the instrument sha (a `c1-before.json`
  sha line present in an earlier draft was dropped — cosmetic; not required by
  any claim).

## Falsifiable bottom line

`sha256sum corpus/instruments/recheck-audit.py` = `c3c19adc…` = every
`instrument_sha256` the C1 evidence pins; re-running those bytes reproduces all
three strict receipts field-for-field and both exit codes; the kill-rule control
stays at pass=6. No wave-1 number requires correction. Report only — no
production files modified.

Report: .ufo/waves/round-25/wave2/C1InstrumentDigest.md
