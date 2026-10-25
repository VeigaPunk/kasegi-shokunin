# ExecReceiptIndex — round 26, wave 1 (kasegi)

Seat: `L1Kasegi26.ExecReceiptIndex`. Scope: C1 (b) — committed gate receipt index at the
instrument's own digest + R25-2 crossreference correction. Run 2026-10-25 (UTC). Lane root:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## Files written (owned paths)

1. `.ufo/waves/round-26/c1-receipt-index.txt` (990 B)
2. `.ufo/waves/round-26/c1-instrument-digest.txt` (340 B)
3. `.ufo/waves/round-26/c1-live.json` (36,316 B — produced by the live audit below, per item)
4. `.ufo/waves/round-26/wave1/ExecReceiptIndex.md` (this report)

No other files touched. No round-25 files edited. No VCS writes.

## Receipt index — exact lines (the committed file)

```
# Round 26 — C1 gate receipt index (recheck-audit gate conformance; depth:verifiability)
instrument_sha256=c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f
base_sha256_control=c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f  # pre-change bytes (round-25 pinned digest); instrument unchanged at write time, so control equals instrument line
selftest cases=14 failures=0 exit=0
EXIT=0
## live lane audit (machine receipt: .ufo/waves/round-26/c1-live.json)
strict pass=37/37 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=37 total=37 pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
EXIT=0
## crossreference correction (R25-2)
note: round-25 c1-receipt-index.txt has no selftest line at :4 (its line 4 is `executes=12 gated=0 broken=23`); wave2/C1InstrumentDigest.md said the selftest tally matched `c1-receipt-index.txt:4` exactly. This index carries the selftest receipt at the current instrument digest above (instrument_sha256 line).
```

Claim counter `grep -cE 'selftest cases=' .ufo/waves/round-26/c1-receipt-index.txt` → 1.

## Instrument digest file — exact lines

```
instrument_sha256=c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f
old_digest_note: round-25 pinned digest c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f — identical to current bytes at write time (2026-10-25 UTC, sha256sum); no byte change to corpus/instruments/recheck-audit.py since round-25 closure.
```

## Commands run — verbatim outputs

1. `sha256sum corpus/instruments/recheck-audit.py`
   ```
   c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f  corpus/instruments/recheck-audit.py
   ```
   Base control `c3c19adc…` (= round-25 pinned digest, pre-change bytes) equals the current
   bytes: the instrument has not changed at write time, so `base_sha256_control` ≡
   `instrument_sha256`. Reported as-is; the receipt is for the bytes on disk now.

2. `python3 corpus/instruments/recheck-audit.py --selftest` → `EXIT=0`, full output:
   ```
   selftest good.md       pass want=True  got=True  | strict want=True  got=True  ok
   selftest prose.md      pass want=False got=False | strict want=False got=False ok
   selftest cwd.md        pass want=False got=False | strict want=False got=False ok
   selftest ghost.md      pass want=False got=False | strict want=False got=False ok
   selftest degenerate.md pass want=True  got=True  | strict want=False got=False ok
   selftest elsewhere.md  pass want=True  got=True  | strict want=False got=False ok
   selftest ownonly.md    pass want=True  got=True  | strict want=False got=False ok
   selftest selftesty.md  pass want=True  got=True  | strict want=False got=False ok
   selftest sourced.md    pass want=True  got=True  | strict want=True  got=True  ok
   selftest basetest.md   pass want=True  got=True  | strict want=False got=False ok
   selftest basestate.md  pass want=True  got=True  | strict want=True  got=True  ok
   selftest parseonly.md  pass want=False got=False | strict want=False got=False ok
   selftest instonly.md   pass want=True  got=True  | strict want=False got=False ok
   selftest completeness lines=13 total=15 complete=False ok
   selftest cases=14 failures=0 exit=0
   EXIT=0
   ```
   All 13 isolating fixtures pass; the completeness fixture (one knowledge file without a
   recheck line must break the exit rule) passes as expected (`complete=False` is the wanted
   outcome). Verified count = **14** (13 fixtures + completeness), not the 15 in the item
   text — the instrument computes `len(cases)+1 = 14`. Recorded honestly as `cases=14`.

3. Live lane audit (from lane root):
   `python3 corpus/instruments/recheck-audit.py --json .ufo/waves/round-26/c1-live.json --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin`
   → `EXIT=0`, summary:
   ```
   strict pass=37/37 cdroot_fail=0 instrument_fail=0 own_fail=0
   executes=14 gated=23 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
   lines=37 total=37 pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
   EXIT=0
   ```
   Machine receipt `c1-live.json`: `instrument_sha256=c3c19adc…`, `lines=37`,
   `total_knowledge_files=37`, `pass_strict=37`, `complete=true`. JSON written by the audit
   itself (runs the same bytes it hashes — `__file__` digest at runtime).

## Crossreference correction (R25-2)

The round-25 index `.ufo/waves/round-25/c1-receipt-index.txt` has **no** selftest line: its
line 4 is `executes=12 gated=0 broken=23` (before-state). `wave2/C1InstrumentDigest.md` states
the selftest tally "matches `c1-receipt-index.txt:4` exactly" — that claim referenced a line
that does not exist. This round's index carries the selftest receipt (`selftest cases=14
failures=0 exit=0`) at the current instrument digest and states the correction in the note
line. Round-25 files left untouched (read-only).

## Risks / notes

- The instrument remains untracked in git (inherited round-25 residual: `git status` shows
  `?? corpus/instruments/recheck-audit.py`); the receipt pins the bytes on disk at write time,
  which is the frozen predicate's meaning. If a later wave changes the instrument, this index's
  digest line must be regenerated under the new bytes before commit.
- Item text said `selftest cases=15`; actual instrument output is `cases=14` (13 fixtures +
  completeness, matching round-25's recorded `cases=14`). The claim counter only requires one
  `selftest cases=` line; the recorded 14 is the truthful figure.
- Tooling: no installs; used preinstalled `sha256sum`, `python3`, `grep`. Pacman untouched.
