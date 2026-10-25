# AttackE1 — R25 digest lineage re-derivation (falsify/confirm)

Seat: `L1Kasegi26.AttackE1` (leaf, read-only). Date: 2026-10-25 UTC.
Tool installs: none (git, sha256sum, coreutils preinstalled; no pacman/uv
touches). Lane bounds respected: no subagent dispatch, no VCS mutations, no
writes outside `.ufo/waves/round-26/wave2/`.

## What this attacks

The C1 gate-conformance AFTER state and its planted cross-reference: (1) the
round-25 "pinned digest" `c3c19adc…` really is the round-25 tip instrument
sha; (2) the committed round-25 receipt index really has no selftest line at
:4; (3) the regenerated round-26 receipt at the landed digest `3fc0d751…`
really fixes the R25-2 cross-reference with a note line, with both the old
line 4 and the new selftest line quotable.

## Evidence chain (all read-only)

| # | Command | Result |
|---|---|---|
| E1 | `git show 41a77b8:corpus/instruments/recheck-audit.py \| sha256sum` | `c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f` |
| E2 | `git merge-base --is-ancestor 41a77b8 1b076fa` | exit 0 (round-25 tip is ancestor of round-26 freeze HEAD) |
| E3 | `git diff --exit-code 98261eb 41a77b8 -- corpus/instruments/recheck-audit.py` | empty (pin commit + repair commit carry identical instrument bytes) |
| E4 | `sha256sum corpus/instruments/recheck-audit.py` (working tree) | `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` |
| E5 | `git show 41a77b8:.ufo/waves/round-25/c1-receipt-index.txt` (blob `09befb97…`) | line 4 = `executes=12 gated=0 broken=23  (gated = …; broken = …)` |
| E6 | `git show 41a77b8:.ufo/waves/round-25/c1-receipt-index.txt \| grep -c -i selftest` | `0` |
| E7 | `git show 41a77b8:.ufo/waves/round-25/wave2/C1InstrumentDigest.md` | asserts "Matches `c1-receipt-index.txt:4` exactly." after printing `selftest cases=14 failures=0 exit=0` — false reference (index line 4 is not a selftest tally) |
| E8 | read `.ufo/waves/round-26/c1-receipt-index.txt` (working tree) | line 2 `instrument_sha256=3fc0d751…` = E4; line 3 `base_sha256_control=c3c19adc…` = E1; line 4 `selftest cases=15 failures=0 exit=0`; lines 11–12 crossreference correction note quoting the old line 4; lines 13–14 regeneration history |
| E9 | `grep -cE '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt` | 39 (matches receipt `expected=39`, `c1-live.json` `expect=present expected=39 missing=0 unexpected=0 strict pass=39/39`) |

## Quotes

**Old line 4** (round-25 committed receipt index, `41a77b8`, line 4):
```
executes=12 gated=0 broken=23  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
```

**New selftest line** (round-26 receipt at landed digest, line 4):
```
selftest cases=15 failures=0 exit=0
```

**Cross-reference note** (round-26 receipt, lines 11–12):
```
## crossreference correction (R25-2)
note: round-25 c1-receipt-index.txt has no selftest line at :4 (its line 4 is `executes=12 gated=0 broken=23`); wave2/C1InstrumentDigest.md said the selftest tally matched `c1-receipt-index.txt:4` exactly. This index carries the selftest receipt at the landed instrument digest above.
```

## Verdict

CONFIRMED on all three limbs — no divergence found. The round-25 tip
instrument blob sha equals `c3c19adc…` (E1/E3); the committed round-25 receipt
index contains no selftest line (zero hits file-wide, E6) and its line 4 is
the `executes=12 gated=0 broken=23` line (E5); the round-26 receipt regenerated
at the landed `3fc0d751…` digest pins the matching `instrument_sha256`, carries
the `selftest cases=15 failures=0 exit=0` line, and fixes the R25-2
cross-reference with the quoted note + regeneration history (E8). Caveat
recorded: the round-26 receipt is untracked at HEAD (wave-1 build lands in the
working tree below freeze commit `1b076fa`); the cross-reference fix is
verified against those working-tree bytes, and the `cases=15` selftest figure is
receipted, not re-run by this read-only seat.
