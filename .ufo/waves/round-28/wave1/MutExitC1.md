# MutExitC1 — C1 exit-code limb mutation test (round 28, wave 1)

Seat: MutExitC1 (leaf, no subagents). UTC 2026-10-25. Scope: scratch only under
`.ufo/waves/round-28/wave1/MutExitC1/`; the live instrument was never written
(restoration evidence below). No tools installed; no pacman transaction attempted.

## State at attack time (no PRE-STATE caveat applies)

- 17:26:36Z: live digest was still the frozen pre-change `c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748`.
- Mid-setup ExecImplC1 landed: a torn-read intermediate snapshot `cab98bcc0cf76eac125b16819c48f21945d3112282cac3e7b27129232e1be1f4`
  (my first copy; behaviorally still pre-change on all four probes: bad-fixture exit 0,
  0 BOUNTIES lines, `--selftest` FileNotFoundError exit 1, SKILL.md 306/bad=0) — kept as
  `anchorcheck.intermediate-cab98bcc.py` for the timeline.
- 17:28:31Z: landed instrument `95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514`
  (523 lines), measured live: bad-fixture exit **1**; bounties-fixture **1** BOUNTIES-ABSENT line;
  `--selftest` exit 0; SKILL.md exit 0, bad=0, LOST-RECORDED=306 — all four C1 after-values hold.
- **All mutants below derive from the landed bytes `95333e29…`** (`anchorcheck.pristine.py`).

## Detectors (identical bounded four for every program, cwd = lane root)

- T1 bad-fixture: `python3 <P> .ufo/waves/round-27/c1-controls/bad-fixture.md` → exit must be 1
- T2 bounties-fixture: `python3 <P> .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT` → must be 1
- T3 selftest: `python3 <P> --selftest` → must print `selftest cases=9 failures=0` and exit 0
- T4 no-harm: `python3 <P> SKILL.md` → exit 0, `0 bad`, `LOST-RECORDED=306`

Baseline pristine `95333e29…` passes all four → the matrix is interpretable (no baseline-failure cells).

## Mutants (single-point edits; full unified diffs in scratch dir vs pristine)

| id | file | mutation | sha256 |
|---|---|---|---|
| M1 | `M1-always-exit-0.py` | `:519` `return 1 if any(kinds.get(k,0) for k in FAIL_CLASSES) else 0` → `return 0` | `8673613dec9d0b72107bf7bf1e82160b2373b6395bb7d08d7107d3d5a5a86918` |
| M2 | `M2-always-exit-1.py` | `:523` `sys.exit(main(sys.argv[1:]))` → `main(sys.argv[1:])` + `sys.exit(1)` | `07ac4c0ceea6dacdb915e5ffbcca5301f9135184a92961fa269b179027713e9e` |
| M3 | `M3-drop-BASE-ABSENT.py` | `:169-170` drop `'BASE-ABSENT'` from `FAIL_CLASSES` | `7ac9718d4924d9f0c116c248a6932f760571559835ecc367da249b8f20fe3121` |
| M4 | `M4-drop-PIN-BROKEN.py` | `:169-170` drop `'PIN-BROKEN'` from `FAIL_CLASSES` | `904f6b13f46216613b33f16824228a6231b74669672a17d768418c742371d881` |

## Scoreboard — mutant × test (actual outputs, verbatim)

| mutant | T1 bad-fixture (exit 1) | T2 bounties (1 line) | T3 selftest (cases=9 failures=0, exit 0) | T4 SKILL.md (exit 0, bad=0, 306) | verdict |
|---|---|---|---|---|---|
| pristine | **1** + `BASE-ABSENT md:2 …zz-r27-anchorcheck-missing.md:99` | **1** | **`selftest cases=9 failures=0`, exit 0** | **exit 0**, `0 bad`, `LOST-RECORDED=306` | baseline |
| M1 always-exit-0 | **KILLED** — exit **0** (BASE-ABSENT still printed) | survived (1) | **KILLED** — `selftest cases=9 failures=6`, exit 1; failcases `missing-file, past-eof, outside-base, pin-broken, base-absent, bounties-absent`, each `exit: want 1, got 0` | survived (exit 0, 306) | **killed** |
| M2 always-exit-1 | spurious pass — exit 1 with unchanged stdout (detector satisfied for the wrong reason) | survived (1) | **KILLED** — `selftest cases=9 failures=3`, exit 1; failcases `bounties-in-range, lost-recorded, clean`, each `exit: want 0, got 1` | **KILLED** — exit **1** on clean input (stdout still 0 bad / 306) | **killed** |
| M3 drop BASE-ABSENT | **KILLED** — exit **0** despite printed BASE-ABSENT | survived (1) | **KILLED (canonical)** — `selftest cases=9 failures=1`, exit 1; sole failcase `base-absent`: `BASE-ABSENT: want 1, got None; exit: want 1, got 0` | survived (exit 0, 306) | **killed** |
| M4 drop PIN-BROKEN | survived (exit 1; fixture has no PIN cite) | survived (1) | **KILLED (canonical)** — `selftest cases=9 failures=1`, exit 1; sole failcase `pin-broken`: `PIN-BROKEN: want 1, got None; exit: want 1, got 0` | survived (exit 0, 306) | **killed** |

## Verdict

**All four mutants killed; no live mutation.** Every dispatched expectation held:
M1 fails bad-fixture (exit 0 vs 1); M2 fails SKILL.md (exit nonzero on clean input);
M3 fails the selftest BASE-ABSENT limb; M4 fails the PIN-BROKEN limb. The M3/M4 selftest
diffs each name exactly one limb — no fixture failed a limb other than its own, so the
run doubles as isolation evidence for the C1 kill rule.

Coverage findings (findings only, no contract change):
1. M4's **only** killer is the selftest — no other detector input exercises PIN-BROKEN; the selftest is load-bearing for that limb.
2. T1's exit-only detector is trivially satisfied by any unconditional-exit mutant (M2 row); the SKILL.md no-harm run is the discriminating test.
3. Dropping a class from `FAIL_CLASSES` propagates through both consumers (`_counts` keying and the exit rule), and both consequences were caught — single mutation point, no silent path.

## Restoration evidence

- Live `corpus/instruments/anchorcheck.py`: sha256 `95333e29…f144514` before the attack and at
  17:34:30Z after; mtime still `2026-10-25 14:28:31 -0300` (ExecImplC1's landing write) — **never
  modified by this seat**; mutants ran exclusively from scratch copies.
- All writes confined to `.ufo/waves/round-28/wave1/MutExitC1/` (six files: pristine, intermediate,
  four mutants) and this receipt. Scratch copies retained as evidence, not deleted.

## Re-verification at any later digest (for the L1)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
S=.ufo/waves/round-28/wave1/MutExitC1
cp corpus/instruments/anchorcheck.py $S/anchorcheck.pristine.py          # rebase mutants first
# re-apply the four single-point edits above to fresh M1..M4 copies, then:
for P in $S/anchorcheck.pristine.py $S/M1-always-exit-0.py $S/M2-always-exit-1.py $S/M3-drop-BASE-ABSENT.py $S/M4-drop-PIN-BROKEN.py; do
  python3 "$P" .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo "T1 $?"
  python3 "$P" .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT
  python3 "$P" --selftest 2>&1 | grep -E '^(selftest cases=|selftest FAIL)'; echo "T3 ${PIPESTATUS[0]}"
  python3 "$P" SKILL.md 2>&1 | grep -m1 '^== '; echo "T4 ${PIPESTATUS[0]}"
done
```
Expected: pristine row matches the baseline above; each mutant shows at least one KILLED cell.
