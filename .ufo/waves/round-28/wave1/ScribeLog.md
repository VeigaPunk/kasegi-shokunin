# ScribeLog — round 28 wave 1 report

**Seat:** ScribeLog (scribe) · **UTC:** 2026-10-25T17:24:28Z · **Lane HEAD:** `94f387c`
**Freeze commit:** `c9f8b115a098c65356e4b3b6048af45a37ab8395`
**Owned production path:** `LOG.md` (append only). **Status:** landed, after-values PENDING at close.

## Behavior

Appended one Round 28 section at the end of `LOG.md` — freeze commit, one line per claim (C1
depth:verifiability, C2 coverage), a census line and a wave line, plus receipt pointers. `git diff
--numstat -- LOG.md` = `49	0` (append only; R9 mechanically verified). Every counter was re-run
from the lane root at run time (three passes: 17:23:04Z, 17:23:53Z, re-confirmed 17:24:28Z); no
value was transcribed from another seat. Because the wave was still in flight, all post-values are
written as PENDING with the exact L1 re-run commands named in the entry.

## Measured at run time (frozen counters, lane root)

| counter | observed |
|---|---|
| `anchorcheck.py` bad-fixture exit | 0 (before value; after pending) |
| bounties-fixture `BOUNTIES-ABSENT` lines | 0 (CITE does not match; after pending) |
| `--selftest` / `c1-receipt-index.txt` | index absent, selftest exit 1 (after pending) |
| `anchorcheck.py SKILL.md` | exit 0, bad=0, `LOST-RECORDED=306 PIN-BROKEN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` |
| instrument sha256 | `c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748` (pre-change) |
| frontier `admitted` | 11 → 12 (F12 row landed mid-wave) |
| knowledge entries `^source: S042 ` | 0 → 0 (entry never present during the passes) |
| `S042` registry row / registry rows | 0 → 1 / 41 → 42 |
| `frontier-recheck-count.py` | `entries=14 pass=14 exit=0` → `FileNotFoundError: … japanese-domestic-disclosure-workflow.md` |
| census `validate --root /home/vgpnk/Projects/shokunin kasegi` | before exit 0 / 41 rows; mid-wave exit 1 / 42 rows |
| wave | one v2 wave, 69 spawn / 0 resume |

Verbatim mid-wave census findings:
`kasegi	E11	S041 missing used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md` and
`kasegi	E11	S042 missing used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md`.

## Gates

- **Passed at run time:** append-only LOG diff; freeze commit present; census-before reproduced
  (exit 0, 41 rows); SKILL.md no-harm baseline reproduced (exit 0, bad=0, LOST-RECORDED=306);
  captures `S041.txt`/`S042.txt` present; spec/dispatch counts 69/69; receipt diff byte-identical
  to `git diff -- LOG.md` (57-line block verified with `diff`).
- **Pending (not observed by this seat):** C1 after-values (a)-(d) at the landed instrument digest;
  C2 entry present, harness 15/15, census exit 0 at 42 rows.
- **Blocking finding:** the tree is mid-wave inconsistent — F12 admitted and S042 registered while
  `corpus/knowledge/japanese-domestic-disclosure-workflow.md` is absent, so census exits 1 and the
  harness crashes. Must close before the lane commit. If ScribeEntryC2's file never lands, C2
  cannot reach its frozen after-values.

## Touched surfaces

`LOG.md` (+49/−0) · `.ufo/waves/round-28/receipts/ScribeLog.txt` (this seat's receipt, exact diff)
· `.ufo/waves/round-28/wave1/ScribeLog/measure*.txt` (scratch transcripts).

## Out of scope

No other production file edited; no claims.json / lesson / SCORECARD / instrument / registry /
README / QUALITY / SKILL change. No git or jj write, no commit/push. No subagent, no background job.
No tool installed/upgraded; no pacman transaction. `/home/vgpnk/Projects/shokuknow` read-only and
untouched.
