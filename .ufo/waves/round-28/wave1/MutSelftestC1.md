# MutSelftestC1 — C1 selftest completeness mutation test (round 28 wave 1)

Seat: MutSelftestC1 (mutation-tester, leaf). Axis: depth:verifiability (C1). Date: 2026-10-25 UTC.
State label: **POST-STATE** — the C1 instrument landed mid-wave (live digest changed from `c2a9e6c6…`
to `95333e29…`), so the matrix below was run against the landed bytes. A first scratch-only pass
(PRE-STATE) ran before the landing; findings are identical, and the final matrix is grounded in the
live file (copy `live-base.py`, sha `95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514`,
= live `corpus/instruments/anchorcheck.py`).

## Subject and detector

- Subject: landed `anchorcheck.py` with `--selftest` (9 cases: missing-file, past-eof, outside-base,
  pin-broken, base-absent, bounties-absent, bounties-in-range, lost-recorded, clean; each case
  asserts the COMPLETE verdict-class vector + exit code).
- Detector = frozen counter (c): `grep -cE 'selftest cases=' INDEX && grep -oE 'instrument_sha256=…' INDEX
  && sha256sum corpus/instruments/anchorcheck.py | awk '{print "instrument_sha256="$1}' && python3
  corpus/instruments/anchorcheck.py --selftest >/dev/null 2>&1; echo selftest_exit=$?` plus the
  kill-rule clause "a limb with no failing fixture kills C1".

## Baseline (pristine live run)

```
$ python3 corpus/instruments/anchorcheck.py --selftest
selftest cases=9 failures=0
$ echo $?
0
```
Counter (a)/(b)/(d) on live bytes: bad-fixture exit=1; bounties-fixture BOUNTIES-ABSENT lines=1; SKILL.md exit=0, lost=306. Baseline green.

## Mutant matrix (each mutant = live bytes + one minimal mutation; output = what the frozen counter would see)

| # | Mutation | Exact `--selftest` output | Exit | Receipt-line condition (`grep 'selftest cases='` + exit) | Verdict vs counter (c) |
|---|---|---|---|---|---|
| M1 | `for c in cases:` → `for c in ():` (skip ALL fixtures; count string still len(cases)=9) | `selftest cases=9 failures=0` | 0 | PASSES (line matches, failures=0, exit 0) | **SURVIVES** |
| M2 | delete the `add('missing-file', …)` block (drop one fixture silently; count accurate = 8) | `selftest cases=8 failures=0` | 0 | PASSES (regex binds no N; exit 0) | **SURVIVES** |
| M3 | `if diffs:` → `if diffs and c['name'] != 'missing-file':` (missing-file fixture asserts trivially-true) | `selftest cases=9 failures=0` | 0 | PASSES | **SURVIVES** |
| LB | subject mutation: MISSING-FILE fallback verdict → BASE-ABSENT (limb genuinely broken) | `selftest FAIL missing-file: MISSING-FILE: want 1, got 0; BASE-ABSENT: want 0, got 1` + `selftest cases=9 failures=1` | 1 | CATCHES (`selftest_exit=1` ≠ after value 0) | **KILLED** |

## Findings / gap

1. **Frozen N is a metavariable, not a constant.** `claims.json` binds `cases=N` twice (C1 predicate
   and implementation note); no number (6 or 9) is pinned. `grep -cE 'selftest cases='` matches any
   N — 9, 8, or 0 — so M1 and M2 pass the receipt-line condition unchanged.
2. **The counter never cross-checks the receipt's N against the instrument's actual case count.** The
   assembled index is auto-generated from the live `--selftest` output, so a landed mutant writes its
   own green receipt; nothing parses N.
3. **Completeness is guarded only by the kill-rule audit clause** ("a limb with no failing fixture kills
   C1"), which no counter command operationalizes. M1/M2/M3 each reduce/neutralize a limb without any
   counter changing value; only a reviewer audit of fixture presence and assertion strength catches them.
4. **The honest selftest does catch real breakage** (LB: failures=1, exit 1), so the kill rule is
   enforceable — but only when the landed instrument is honest. The receipt-condition alone cannot
   distinguish M1/M2/M3 from an honest suite.
5. Also noted: counter (c) greps that an `instrument_sha256=` line EXISTS in the index but does not
   compare it against the live `sha256sum` value (chain just echoes the live sha).

## Kill-rule demonstration (LB)

On the LB subject the honest selftest prints `selftest FAIL missing-file: MISSING-FILE: want 1, got 0;
BASE-ABSENT: want 0, got 1` and `selftest cases=9 failures=1`, exit 1 — the non-isolating/absent-limb
condition is caught, and `selftest_exit=1` fails the counter's after value. Same LB subject under M3's
vacuous assertion: `selftest cases=9 failures=0`, exit 0 — the limb's breakage is invisible.

## Restoration / mutation evidence

- Live `corpus/instruments/anchorcheck.py`: sha `95333e29…` before AND after the whole run (untouched;
  read-only). Control receipts re-run: `bad_exit=1`, `BOUNTIES-ABSENT_lines=1`, `skill_exit=0`, `lost=306`.
- Scratch artifacts in `.ufo/waves/round-28/wave1/MutSelftestC1/`:
  - `anchorcheck-ref.py` = frozen pre-change bytes (`c2a9e6c6…`, identical to live at session start) — unchanged.
  - `live-base.py` = live bytes copy (`95333e29…`).
  - `live-m1.py` `dfd41f5f…`, `live-m2.py` `08e27619…`, `live-m3.py` `9efa7563…`, `live-lb.py` `9dcb78dc…`.
  - PRE-STATE scratch reference (`anchorcheck-impl.py` `4b305d79…`, `m1-skip-fixtures.py`, `m2-drop-fixture.py`,
    `m3-trivial-assert.py`, `impl-limb-broken.py`) — first pass artifacts, same verdicts.
- No production file outside read access was modified by this seat.

## Re-run (L1, post-landing)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/anchorcheck.py --selftest   # expect cases=9 failures=0 exit=0
# then run assemble-receipts.py and the frozen counter (c) chain verbatim
```
