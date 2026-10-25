# CritC1Vacuity — C1 vacuity attack receipt (round-28 wave 1)

Seat: CritC1Vacuity (critic, C1 depth:verifiability). Timestamp: 2026-10-25 UTC.
Lane base: c9f8b115a098c65356e4b3b6048af45a37ab8395.

## Status: POST-STATE (implementation landed mid-run)

The live `corpus/instruments/anchorcheck.py` changed while this seat ran:
c2a9e6c6… (pre-change, sha256sum re-verified) → 95333e29… (stable, compiles,
git status = uncommitted `M`). All do-nothing-control numbers below were run on
the committed pre-change bytes `git show HEAD:corpus/instruments/anchorcheck.py`
(digest c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748, written
to `wave1/CritC1Vacuity/pre-change-anchorcheck.py`). Counter re-runs on the
landed bytes are quoted with digest 95333e29.

Pins: c2a9e6c6 = committed pre-change; 95333e29 = landed in-flight. If the final
committed digest differs from 95333e29, the L1 must re-run the two re-run
commands in §4 against the final bytes.

## 1. Do-nothing control (re-run, pre-change bytes)

`pre-change-anchorcheck.py` = committed c2a9e6c6 bytes. On the two committed
fixtures:

- bad-fixture.md → exit **0** (BASE-ABSENT printed, exit 0). Frozen after value
  1 NOT reached. (Note: the fixture's header comment names MISSING-FILE, but the
  cite actually exercises BASE-ABSENT — mirror root absent → `BASE-ABSENT md:2
  … (base tree absent: /home/vgpnk/Projects/the-bounty-hunter/…)`. Comment/fact
  drift, pre-existing.)
- bounties-fixture.md → **0** BOUNTIES-ABSENT lines (cite invisible to CITE).
  Frozen after value 1 NOT reached.
- `--selftest` → FileNotFoundError, exit **1**, zero `selftest cases=` lines
  (matches the frozen before-receipt `selftest-before.txt`).
- SKILL.md → exit 0, LOST-RECORDED=306 (before-value held).

Conclusion: do-nothing control discriminates; no frozen after-value is reachable
without the claimed work. No kill on the control.

## 2. Selftest vacuity attack — counter floor, not impl

`grep -cE 'selftest cases=' …` (counter 3) matches `selftest cases=0 failures=0`
and `selftest cases=9 failures=0` alike — no `N≥1` floor, no `failures=0`
assertion in the counter itself. Demonstrated: `vacuous-selftest.py` (patch of
pre-change bytes with `--selftest` → `print('selftest cases=0 failures=0');
return 0`) prints `selftest cases=0 failures=0` and exits 0 — the counter
command would read 1/`instrument_sha256`/exit 0 on it.

The LANDED impl is not vacuous: `_selftest()` builds 9 real cases
(missing-file, past-eof, outside-base, pin-broken, base-absent,
bounties-absent, bounties-in-range, lost-recorded, clean), each run as a
subprocess with KASEGI_LANE_ROOT/MIRROR/ORIGIN_ROOT/BOUNTIES pointed at fresh
temp roots (so the absent-bases host reaches every limb), and asserts the
COMPLETE verdict-class vector plus exit status per case. Red-check: a scratch
copy with the clean case's expected exit mutated to 1 prints
`selftest FAIL clean: exit: want 1, got 0` and `selftest cases=9 failures=1`
with exit 1 — the assertions bite. Landed run: `selftest cases=9 failures=0`
exit 0. A limb with no failing fixture, or a fixture tripping a second limb (any
UNEARNED count, including IN-RANGE), fails the vector check — the kill-rule
isolation clause is enforced by the impl, not just by prose.

Vulnerability remaining: the check text has no floor (`cases=N` with N=0 or a
degenerate fixture set would still read `cases=N failures=0`), so the L1/judge
should require N=9 (or ≥6 per-limb) plus the per-case fixture names in the
receipt index. Recommend strengthening the counter to
`grep -cE 'selftest cases=[1-9][0-9]* failures=0'` and requiring the receipt
index to list the per-limb fixture names.

## 3. Bounties-counter vacuity (frozen check is substring-wide)

Claim (b) counts `grep -c BOUNTIES-ABSENT` — a substring match, anchored
nowhere. Demonstrated on committed pre-change bytes: a patch that ONLY appends a
`BOUNTIES-ABSENT=0` bucket to the summary line (CITE untouched, zero
BOUNTIES-ABSENT verdicts) makes the counter read **1** (`vacuous-bounties.py`,
summary: `… BASE-ABSENT=0 BOUNTIES-ABSENT=0`). A do-nothing-with-summary-bucket
implementation would satisfy the counter vacuously.

The LANDED impl prints `BOUNTIES-ABSENT md:3 …` as a verdict line and
deliberately does NOT add a summary bucket (docstring: a bucket would make the
count 2). On landed bytes the frozen counter reads 1; the anchored variant
`grep -c '^BOUNTIES-ABSENT md:'` also reads 1 (per-cite verdict line present).
So the landed code is honest, but the check as frozen cannot distinguish the
verdict line from a summary bucket. Recommend the L1/judge either tighten the
check to `grep -c '^BOUNTIES-ABSENT md:'` or hold the no-summary-bucket
docstring to the implementation.

Corpus disclosure: the 4 marked bounties citations reclassify to
LOST-RECORDED (recorded-not-fail per FAIL_CLASSES scope); SKILL.md has 0 marked
bounties cites, so its verdict classes are untouched (LOST-RECORDED=306, exit 0,
bad=0). No kill.

## 4. Exit-code reachability: gate exit-1 vs crash exit-1

Frozen counter 1 (`bad_fixture_exit`) checks only `echo $?` — it cannot
distinguish a fail-class verdict from a crash. On committed pre-change bytes AND
on landed 95333e29 bytes, exit 1 is reachable by paths that print NO verdict:
- `anchorcheck.py` (no args): pre-change IndexError exit 1; landed returns 2
  (handled — note exit 2 now also != 0, a deliberate usage error).
- `anchorcheck.py <nonexistent.md>`: FileNotFoundError traceback, exit 1.
- cite resolves to a DIRECTORY named `*.md`: `IsADirectoryError` traceback at
  `open(path)`, exit 1 (both pre-change and landed).
- checked file with invalid UTF-8 (`open(src)` without `errors='replace'` while
  cited files use it): UnicodeDecodeError traceback, exit 1.
- missing `git` binary or a lane dir that is not a repo while a pin is declared:
  `git_show` handles returncode≠0 → PIN-BROKEN (fail class, correct), but a
  missing `git` binary raises FileNotFoundError → crash exit 1.

All these crash paths exit 1 without printing the fail-class verdict line; the
frozen counter would read them as `bad_fixture_exit=1`. The landed gate itself
is correct (`return 1 if any(kinds.get(k,0) for k in FAIL_CLASSES) else 0`;
BASE-ABSENT and BOUNTIES-ABSENT are in FAIL_CLASSES, LOST-RECORDED is not), so
this is a check-robustness gap, not a claim violation. Recommend the L1/judge
require the counter to also assert the expected fail-class verdict line
(e.g. `grep -cE '^(MISSING-FILE|PAST-EOF|OUTSIDE-BASE|PIN-BROKEN|BASE-ABSENT|BOUNTIES-ABSENT) md:'`) alongside the exit code; optionally classify the two
crash paths as verdicts.

## 5. Landed no-harm

SKILL.md on 95333e29: exit 0, 0 bad, LOST-RECORDED=306, PIN-BROKEN=0,
OUTSIDE-BASE=0, BASE-ABSENT=0 — matches the frozen after values.

## 6. Re-run commands for the L1 (post-change, final committed bytes)

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/instruments/anchorcheck.py   # expect 95333e29… (or re-run below with the final digest)
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo "bad_fixture_exit=$? (want 1)"
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c '^BOUNTIES-ABSENT md:'   # want 1 (anchored; frozen substring form also 1 on landed bytes)
python3 corpus/instruments/anchorcheck.py --selftest; echo "selftest_exit=$? (want cases=9 failures=0 exit=0)"
python3 corpus/instruments/anchorcheck.py SKILL.md >/dev/null 2>&1; echo "skill_exit=$?"; python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | grep -oE 'LOST-RECORDED=[0-9]+' | head -1
```

## 7. Verdict

No vacuous pass in the landed implementation; the do-nothing control
discriminates; exit-1 gate is real. Two check-side vacancies to record: (1) the
selftest counter has no N≥1 floor (impl enforces N=9 via whole-vector asserts —
keep it); (2) the BOUNTIES-ABSENT counter is substring-wide and cannot
distinguish a verdict line from a summary bucket (landed impl avoids the bucket —
keep it that way). Neither is a kill; both are judge-facing hardening asks.
