# ExecNoHarmC1 — C1 no-harm measurements (round 28, wave 1)

Seat: ExecNoHarmC1 (executor, **read-only** — no production file edited).
Measured 2026-10-25T17:23Z. Lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
worktree HEAD `94f387c`, lane base `c9f8b11`.
Full raw receipt: `.ufo/waves/round-28/receipts/ExecNoHarmC1.txt`.

## State label: PRE-STATE

`corpus/instruments/anchorcheck.py` sha256 = `c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748`,
exactly the frozen pre-change digest recorded in `.ufo/waves/round-28/c1-controls/instrument-digest-before.txt`.
ExecImplC1's C1 edit had not landed when I measured. Everything below is the pre-change
baseline; it cannot certify the post-change instrument and must be re-run.

## 1. anchorcheck.py SKILL.md — no movement

```
exit=0
== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
```

| class | count | before | match |
|---|---:|---:|---|
| IN-RANGE (`OK md:`) | 7 | 7 | yes |
| LOST-RECORDED | 306 | 306 | yes |
| PIN-BROKEN | 0 | 0 | yes |
| ORIGIN (`IN-RANGE(ORIGIN)`) | 0 | 0 | yes |
| OUTSIDE-BASE | 0 | 0 | yes |
| BASE-ABSENT | 0 | 0 | yes |
| MISSING-FILE | 0 | 0 | yes |
| PAST-EOF | 0 | 0 | yes |
| **bad** | **0** | **0** | **yes** |

315 stdout lines / 27315 bytes / sha256 `2f29df46…e03835`; two consecutive runs byte-identical;
LOST `md:` span 57→998; distinct anchors 7.

Stronger than counting: the fresh stdout is **byte-identical to the body of**
`.ufo/waves/round-28/c1-controls/skill-before.txt` (that receipt is this body + `exit=0`).
So the SKILL.md live run reproduces the frozen before exactly — **no-harm holds at PRE-STATE**.

Honest limit: the pre-change instrument has no fail path (a bad verdict still exits 0, as
`c1-controls/bad-fixture-before.txt` shows: `BASE-ABSENT … exit=0`). This exit 0 is the
no-movement guard, not a test of the new gate.

## 2. density.py — same-byte guard holds; the assigned comparand is stale

```
exit=0
# Density census — r28-noharm (1032 lines, 20 blocks)
mean dens 150.3
Total path-citation instances: 652 across 20 blocks
```

| metric | measured | assigned comparand | verdict |
|---|---:|---:|---|
| mean dens | **150.3** | 154.0 | not equal — see reconciliation |
| blocks | **20** | 19 | not equal — see reconciliation |
| path-citation instances | **652** | 652 | **equal** |

Reconciliation (measured, not assumed):

- `git show c8b719d:SKILL.md` (round-22 bytes, 1023 lines) → **19 blocks, mean 154.0, 652 cites**.
  Runs of the same instrument on those bytes reproduce the round-24/25 baseline exactly.
- `git show a04cc6c:SKILL.md` (round-26 bytes, 1032 lines) — sha256
  `fa09d5b8…d64f2d`, identical to the worktree and to `git show c9f8b11:SKILL.md` →
  **20 blocks, mean 150.3, 652 cites**.
- Cause: commit `a04cc6c` (round 26) added 9 lines — a new `## Gates & probes registry`
  section (one table data row, **0 path-cites**, nb=5 ev=4 **dens=80.0**) before
  `## Cited paths`. Blocks 19→20; the new low-density block pulls the *unweighted* mean
  154.0→150.3. Cites unchanged at 652 because the block contributes none.

Applying 154.0 unchanged to the current bytes would log a false −3.7 regression. The
same-byte guard for this wave is therefore **150.3 / 20 blocks / 652 cites at base
`c9f8b11`**, and the measured run hits it with delta 0 on all three.

Identity guard: `git diff c9f8b11… -- SKILL.md` → empty; worktree sha256 equals the base
blob sha256; `git status --porcelain -- SKILL.md corpus/instruments/anchorcheck.py` → empty.
**ScribeSkillGate's R6 append has not landed**, and no round-28 byte has touched SKILL.md.

## Re-run the L1 must execute after production lands

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/instruments/anchorcheck.py
python3 corpus/instruments/anchorcheck.py SKILL.md > /tmp/r28-post-anchor.out 2>&1; echo exit=$?
sed -n '2p' /tmp/r28-post-anchor.out
awk '/^OK md:/{k["OK"]++} /^(LOST-RECORDED|MISSING-FILE|PAST-EOF|OUTSIDE-BASE|PIN-BROKEN|BASE-ABSENT) /{k[$1]++} END{for(x in k) printf "%s=%d\n", x, k[x]}' /tmp/r28-post-anchor.out | sort
python3 corpus/instruments/density.py SKILL.md --label r28-post | grep -E 'mean dens|Total path|^# Density'
```

Required post-change: anchorcheck exit 0; bad=0; LOST-RECORDED=306; PIN-BROKEN=0; ORIGIN=0;
OUTSIDE-BASE=0; BASE-ABSENT=0; in-range=7. Density: path-citation instances ≥ 652; mean
compared to 150.3 with any delta attributed to the appended block's own dens (a new `##`
section makes it block 21 and moves the unweighted mean by construction, not by drift).

## Files touched

- `.ufo/waves/round-28/receipts/ExecNoHarmC1.txt` (new, this seat's receipt)
- `.ufo/waves/round-28/wave1/ExecNoHarmC1.md` (new, this report)

No production file, no claims file, no SKILL.md byte changed. No tool installed; no pacman
transaction attempted.
