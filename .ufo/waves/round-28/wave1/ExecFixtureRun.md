# ExecFixtureRun — round 28, wave 1 (frozen C1 counters, exact re-run)

**Seat:** leaf executor. **Write scope used:** `.ufo/waves/round-28/receipts/ExecFixtureRun.txt` and this report only.
**Production edits:** none. **Tool installs:** none.
**Run time:** 2026-10-25T17:22Z (UTC), CWD `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## State label: PRE-STATE

```
sha256sum corpus/instruments/anchorcheck.py
c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748
```

Digest identical before and after every counter run, and equal to `claims.json` C1.before.
`ExecImplC1` had not landed (no `.ufo/waves/round-28/wave1/ExecImplC1/` scratch at run and at
write time), so all three counters are labeled **PRE-STATE** and are the **do-nothing control**,
not the predicate.

## Results (verbatim)

| # | Counter | Command | Observed | before (frozen) | after (required) |
|---|---|---|---|---|---|
| 1 | bad-fixture exit | `python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo $?` | `0` | 0 | 1 |
| 2 | bounties BOUNTIES-ABSENT lines | `... bounties-fixture.md 2>/dev/null \| grep -c BOUNTIES-ABSENT` | `0` | 0 | 1 |
| 3 | `--selftest` | `python3 corpus/instruments/anchorcheck.py --selftest` | `FileNotFoundError: '--selftest'`, `selftest_exit=1`, zero bytes on stdout | flag absent, crash exit 1 | `selftest cases=N failures=0`, exit 0 |

Counter (1) printed summary line — the unverifiable cite is *reported* and the process still exits 0:

```
== .ufo/waves/round-27/c1-controls/bad-fixture.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=1
BASE-ABSENT md:2 corpus/knowledge/zz-r27-anchorcheck-missing.md:99 (base tree absent: /home/vgpnk/Projects/the-bounty-hunter/corpus/knowledge/zz-r27-anchorcheck-missing.md)
```

Counter (2) full output — the `~/Projects/bounties/ops/claim-check.mjs:96` cite is invisible, so the
fixture produces no cite instances in any class and no BOUNTIES verdict:

```
== .ufo/waves/round-27/c1-controls/bounties-fixture.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
```

Counter (3) — `grep -c 'selftest cases='` on stdout = `0`, stdout is `0` bytes.

Side baseline for C1(d) no-harm ground truth (not one of my three counters, run because it is the
comparator the parent needs): `SKILL.md` → `exit=0`,
`== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`
— matches both `claims.json` before values and `.ufo/waves/round-28/c1-controls/skill-before.txt`.

## Structural confirmation (digest alone is not the whole story)

```
grep -c 'BOUNTIES-ABSENT'      anchorcheck.py -> 0
grep -c 'selftest'             anchorcheck.py -> 0
grep -c 'FAIL_CLASSES'         anchorcheck.py -> 0
grep -c 'Projects/bounties/'   anchorcheck.py -> 0   (no bounties arm in CITE)
grep -c 'KASEGI_BOUNTIES'      anchorcheck.py -> 0   (no bounties root derivation)
grep -nE 'sys\.exit\(1\)|return 1' anchorcheck.py -> no match
```

`main()` has no non-zero return path at all (it falls off the end into `sys.exit(None)` = 0), which
is the mechanism behind counter (1) and (2) failing their after-values. All three limbs are absent
from the bytes, not merely unexercised.

## Input pinning

| File | sha256 |
|---|---|
| `.ufo/waves/round-27/c1-controls/bad-fixture.md` | `969e2b92f1d14c47ebd5152aebc2df7342fc1743a914cac8f846fd27758e7471` |
| `.ufo/waves/round-27/c1-controls/bounties-fixture.md` | `5c37b69e0ec662b6bafd98e5d8a5def3d78be563489db891790dc2f543eb77b5` |
| `SKILL.md` | `fa09d5b835451f2443fc96353432a330608baf5f3631d1b382141f7e86d64f2d` |

## Verdict

C1 is **unproven** at this digest. My three runs reproduce the frozen *before* values exactly and reach
no *after* value; per the honesty rule an unrun (post-change) check has not passed. What this run does
establish is the other half of the kill rule: the committed pre-change bytes did **not** drift into
any after-value, so the control is clean and the after-values remain attributable to `ExecImplC1`'s
change when it lands.

## Exact post-change re-run the L1 must execute (from the lane root)

```bash
sha256sum corpus/instruments/anchorcheck.py
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo "bad_fixture_exit=$?"
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT
python3 corpus/instruments/anchorcheck.py --selftest; echo "selftest_exit=$?"
python3 corpus/instruments/anchorcheck.py SKILL.md >/dev/null 2>&1; echo "skill_exit=$?"
python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | grep '^== '
```

Expected at the landed digest: `bad_fixture_exit=1`; `1`; a `selftest cases=N failures=0` line with
`selftest_exit=0`; `skill_exit=0`; summary `7 in-range, 0 bad, LOST-RECORDED=306 PIN-BROKEN=0
OUTSIDE-BASE=0 BASE-ABSENT=0`. The receipt-index pair from `claims.json` counter_commands[2]
(`grep -cE 'selftest cases=' .ufo/waves/round-28/c1-receipt-index.txt`, the
`instrument_sha256=[0-9a-f]{64}` compare, `selftest_exit`) additionally requires the landed index file,
which does not exist yet — that half is the L1's gate, not mine.

## Risks / blockers

- Blocker (informational, expected): no post-change instrument existed at run time, so C1 cannot be
  closed from this seat. Nothing else blocked me; no waiting or polling was performed (single digest
  check at write time only).
- Receipt path: `.ufo/waves/round-28/receipts/ExecFixtureRun.txt`.
