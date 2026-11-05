# DraftLog — round-71 attempt 2: LOG.md round-71 entry draft

Seat: `DraftLog` (scribe, leaf). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, tip read: `3cc8cd45cb6f8ca49a292f3b2647c5bddac71486` (`git rev-parse --short HEAD` → `3cc8cd4`). Frozen claims `0e260a54b0a670cee2915237ac403d37164c749d`.
Only file written: `.ufo/waves/round-71/w2/LogDraft.md` (plus this report). No `LOG.md` edit, no commit, no push, no git mutation, no subagent, no tool installed or upgraded. The `LOG.md` append is the L1's.

## 1. Deliverable

- Draft path: `.ufo/waves/round-71/w2/LogDraft.md`
- Line count: **22** (`wc -l`); 22 bullets, one bullet per line, shape matching the round-68/69/70 entries (`## Round 71 — …` heading, then bullets).
- Bytes: 10317; `sha256sum` `2cd824b0d5cbbe2be74a4de11c18e937da5c4f7f30d8e30d2b5479ab01d86e66`.
- Bullet order: declared claims; controls and freeze; pinned gate and candidate receipt; attempt 1 (incomplete, seat roster, dead seats, dead L1); C1 reproduction; C1 selftest isolation; C1 mutation evidence; C1 forgery limb; C1 scope; C2 at `4e33119`; where C2 integration landed; C2 after-values; C2 quotes; C2 overlap with F02/S075; assimilation; routed defects; quiescence; capability and score posture; admission.

## 2. The four required record items

(a) Attempt 1 spawned 14 seats; four attack seats died with no output: `CriticC1`, `CriticC2`, `MutationC1`, `SentinelGate`. Recorded in the draft's attempt-1 bullet. Evidence: `w1/swarm-registry.json` (14 members) and `w1-dispatch.json` (`"spawn": 14`); the ten committed reports in `w1/` are the only verdict sources.

(b) Attempt 1's L1 died before filing a report; the round completes in attempt 2. Recorded. Evidence: commit subject `453275f` "preserve in-flight work at hyaku run-15 wrap-up (L1 died on provider failure; not a landed round)"; `w1/ScribeF49.md` §8 ("L1 died on a provider failure and the run-15 wrap-up exported the working tree as commit `453275f`").

(c) C2's registry row and the `ReviewC2` NOT VERIFIED — **the assignment's commit attribution is corrected in the draft.** The brief said the registry row landed only in `34faab9`. Measured: the row landed in `453275f`. `34faab9` added only the `corpus/SOURCES.md` `## Registry changes` bullet and the `ScribeRegistry` report. The draft states this. The `ReviewC2` NOT VERIFIED at `4e33119` stands, because `4e33119` predates every corpus integration file (see §3).

(d) Tip at integration `3cc8cd45cb6f8ca49a292f3b2647c5bddac71486`; round not admitted until a non-author closure verifies it. Recorded in the admission bullet.

## 3. Facts the draft corrects or adds beyond the brief

1. **Registry row location.** `S106` row, `F49` README row, knowledge entry, `knowledge-expected.txt` line and `PROVINCE.md` line all first appear in `453275f` (see §4, command 4). `34faab9` adds the `## Registry changes` bullet. `3cc8cd4` adds `corpus/lessons/round-71.md` and `ScribeLesson` report only.
2. **Controls were committed with the freeze, not before it.** `0e260a5` adds six files (`claims.json`, `c1-base-r71.txt`, `c1-donothing-r71.txt`, `c1-probe-run-r71.py`, `c2-base-counters-r71.txt`, `pins-r71.txt`; 494 insertions). Round 70 committed its controls at `15d4da87`, before its freeze. The draft says so and does not claim a pre-freeze order.
3. **The gate sha is not pinned in `pins-r71.txt`.** The file has five lines; the `182f4ef7…` gate hash appears only in the `claims.json` predicate text. The candidate receipt `c1-candidate-trial-r71.txt` (sha256 `2231c8c8…`, per `ExecRerun`) is unpinned.
4. **Attack share.** Attempt 1 had four attack seats of 14 (critic 2, mutation-tester 1, sentinel 1; 29 %), and all four died. No non-author adversarial verdict on C1 or C2 exists in attempt 1.
5. **C1 forgery limb was never produced as a committed receipt.** `claims.json` says "to be produced at the wave". `ScribeLesson`'s forgery run (`failures=12`, exit 1) used the round-70 forgery gate as its own control, not a committed round-71 receipt. The draft says so.
6. **C1 mutation evidence is author-side.** The lesson's one-limb battery came from `ScribeLesson`; `MutationC1` died. The only non-scribe mutation evidence is `ExecSelftest`'s 10-case isolation audit (9/10 isolated).
7. **C1 receipt drift at `4e33119`.** `direct_rc` of R1 and R8 is 0 in the committed receipts but 1 on re-run at `4e33119`, because the S106 registry row is absent there (`FAIL rule=no-row record=S106 dir=round-71`). The draft records this as observed; it does not claim the receipts reproduce at `3cc8cd45`. That re-measure is for the non-author closure.
8. **C2 overlap with F02/S075.** `ScoutF49` measured four of the five declared items (120-day window, 30/60/90 shortening, 15-business-day escalation, limited-versus-full advisory) already held in `corpus/knowledge/zdi-disclosure-policy.md` (F02/S075). The new ground is the acquisition-side flow. `CriticC2` died, so this is not adjudicated. The draft says so.
9. **Quotes.** Fourteen of 15 manifest quotes occur once; Q01-scope occurs twice (`S106.txt:28` and `:102`). The entry cites `:28`.
10. **Dates.** Entry dates are UTC (`2026-11-05`); the host-local date at capture was 2026-11-04. The draft notes this.
11. **Quiescence.** `git status --porcelain` at `3cc8cd4` shows `M SCORECARD.md` (+30), `M corpus/QUALITY.md` (+2), `M corpus/lessons/round-71.md` (+18) and untracked `.ufo/waves/round-71/` attempt-2 files. R110 is not met yet. The draft reads committed bytes only and does not use the uncommitted edits.

## 4. Measured commands and observed output (read-only)

All run from the lane root; no lane file written, no git mutation.

```
$ git log --oneline -12   (abbreviated)
3cc8cd4 kasegi r71: late seat output (ScribeLesson round-71 lesson draft + report) after wrap-up; not a landed round
34faab9 kasegi r71: late seat output (ScribeRegistry registry-changes bullet + report) after wrap-up; not a landed round
453275f kasegi r71: preserve in-flight work at hyaku run-15 wrap-up (L1 died on provider failure; not a landed round)
4e33119 round-71: C1 per-script python-head census (gate sha256 182f4ef7, selftest 106/0) and the S106 ZDI capture with its 15-quote manifest
0e260a5 round-71: freeze C1 (per-script python-head denial + census fail-closed) and C2 (F49/S106 ZDI), with the r71 probe set, do-nothing and r69-base controls
39cde8a round-70 verifier spot-check (integrator, hyaku): non-author admit/reject

$ git cat-file -t 3cc8cd45cb6f8ca49a292f3b2647c5bddac71486
commit

$ git show --stat --format='%h %s' 0e260a5   (file list)
 .ufo/waves/round-71/claims.json                    |  81 +++++
 .ufo/waves/round-71/controls/c1-base-r71.txt       |  28 ++
 .ufo/waves/round-71/controls/c1-donothing-r71.txt  |  28 ++
 .ufo/waves/round-71/controls/c1-probe-run-r71.py   | 341 +++++++++++++++++++++
 .../round-71/controls/c2-base-counters-r71.txt     |  11 +
 .ufo/waves/round-71/controls/pins-r71.txt          |   5 +
 6 files changed, 494 insertions(+)

$ for c in 4e33119 453275f 34faab9 3cc8cd4: count S106 row / F49 README row / knowledge-expected lines / knowledge entry present / "Registry changes" bullet
4e33119 SOURCES_S106=0 README_F49=0 KE=88 knowledge_zdi_new=no bullet=1
453275f SOURCES_S106=1 README_F49=1 KE=89 knowledge_zdi_new=yes bullet=1
34faab9 SOURCES_S106=1 README_F49=1 KE=89 knowledge_zdi_new=yes bullet=1
3cc8cd4 SOURCES_S106=1 README_F49=1 KE=89 knowledge_zdi_new=yes bullet=1

$ git show --stat --format='%h %s' 453275f | tail -n 4   (relevant lines)
 corpus/QUALITY.md                                  |   1 +
 corpus/README.md                                   |  23 ++
 corpus/SOURCES.md                                  |   1 +
 corpus/instruments/knowledge-expected.txt          |   1 +
 ...i-disclosure-process-and-vendor-coordination.md | 256 +++++++++++++++
 30 files changed, 2917 insertions(+)

$ git show --stat --format='%h %s' 34faab9
 .ufo/waves/round-71/w1/ScribeRegistry.md | 255 +++++++++++++++++++++++++++++++
 corpus/SOURCES.md                        |   1 +
 2 files changed, 256 insertions(+)

$ git show --stat --format='%h %s' 3cc8cd4
 .ufo/waves/round-71/w1/ScribeLesson.md | 135 ++++++++++++++++++++++
 corpus/lessons/round-71.md             | 199 +++++++++++++++++++++++++++++++++
 2 files changed, 334 insertions(+)

$ git show 3cc8cd45:corpus/instruments/figure-audit.py | sha256sum
182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603  -
$ git show 3cc8cd45:corpus/source-snapshots/round-71/S106.txt | sha256sum
291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db  -
$ git show 453275f:corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md | sha256sum
6f304a052190d988b189ed82d547b0ba53562fc6837fa3dd52a8dbfb87986684  -
$ git show 3cc8cd45:corpus/instruments/knowledge-expected.txt | wc -l
89
$ git show 3cc8cd45:corpus/README.md | grep -cE '^\| F[0-9]+ \|'
49
$ git show 3cc8cd45:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
106
$ git show 3cc8cd45:corpus/lessons/round-71.md | wc -l
199
$ git show 3cc8cd45:corpus/SOURCES.md | sed -n '118p' | cut -c1-60
| S106 | TrendAI Zero Day Initiative (ZDI), About — https:
$ git show 453275f:corpus/SOURCES.md | sha256sum  →  615e0034…
$ git show 3cc8cd45:corpus/SOURCES.md | sha256sum →  1d4d4e74…   (the 34faab9 bullet is the only difference)
$ git show 3cc8cd45:corpus/instruments/knowledge-expected.txt | grep -n zdi
88:corpus/knowledge/zdi-disclosure-policy.md
89:corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md

$ git status --porcelain | grep -v '^??'
 M SCORECARD.md
 M corpus/QUALITY.md
 M corpus/lessons/round-71.md
$ git diff --stat -- corpus/lessons/round-71.md SCORECARD.md corpus/QUALITY.md
 SCORECARD.md               | 30 ++++++++++++++++++++++++++++++
 corpus/QUALITY.md          |  2 ++
 corpus/lessons/round-71.md | 18 ++++++++++++++++++
 3 files changed, 50 insertions(+)

$ git show 3cc8cd45:.ufo/waves/round-71/assimilation/collisions | wc -l   → 75
$ git show 3cc8cd45:.ufo/waves/round-71/assimilation/staged-ids | wc -l   → 94
$ git show 3cc8cd45:.ufo/waves/round-71/assimilation/reg-ids | wc -l      → 105

$ git show 3cc8cd45:corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md | grep -n '^## '   (11 sections)
8:## Scope and decision rule
49:## What the acquisition programme states about itself
62:## The disclosure sequence ZDI states
79:## The coordination windows ZDI states
98:## The advisory choice ZDI states
113:## Credit, anonymity, and the no-backlog guarantee
125:## Scope limits
137:## Falsifiable rule
159:## Rejected over-generalizations
187:## Gate
230:## Limits
```

Not measured by this seat (and not claimed in the draft): the frozen counter, the gate selftest, the census and frontier instruments, and any `3cc8cd45` counter value. Those are attempt-2 verifier work.

## 5. Evidence pointers used by the draft

Committed claim and controls (at `0e260a5` and tip):
- `.ufo/waves/round-71/claims.json` (C1 predicate, probe set N1–N12/R1–R8, kill rule, C2 predicate, `assimilation`, `non_claims`).
- `.ufo/waves/round-71/controls/pins-r71.txt` (five hashes).
- `.ufo/waves/round-71/controls/c1-donothing-r71.txt` (`VERIFY measurements=25 failures=13`, exit 1; N8 `marker_runs=1`; R1–R8 `admitted=0`).
- `.ufo/waves/round-71/controls/c1-base-r71.txt` (`VERIFY measurements=25 failures=14`; N1–N12 `refused=0`).
- `.ufo/waves/round-71/controls/c2-base-counters-r71.txt` (`rows=48 admitted=48 registry=105`, `entries=51`, `records=84`, 88/86, 86 files).
- `.ufo/waves/round-71/controls/c1-probe-run-r71.py` (counter; `--mode` a label only per `ReviewerC1` §7).
- `.ufo/waves/round-71/controls/c1-candidate-trial-r71.txt` (landed at `4e33119`; sha256 `2231c8c8…` per `ExecRerun`).

Attempt-1 reports (`.ufo/waves/round-71/w1/`), all ten read in full:
- `ReviewerC1.md` (C1 VERIFIED; three runs reproduced; R1/R8 drift §5; `--mode` label §7).
- `ExecRerun.md` (pins 5/5; two runs per mode byte-identical; selftest 106/0; mutbat 5/5; ledger 35/35).
- `ExecSelftest.md` (ISOLATED=9/10; `python-out-only-refused` survives M09a/M04/M09c; r70 cases 4/4; dead config observation).
- `ReviewC2.md` (NOT VERIFIED at `4e33119`; five after-values at before values; capture half verified).
- `ExecCapture.md` (S106 re-fetch at 2026-11-05T01:30:56Z byte-identical; Q01-scope twice; no date signal on the page).
- `ScribeF49.md` (entry 256 lines, sha256 `6f304a05…`; `frontier-recheck-count` FRONTIER-PASS F49; L1-death note §8).
- `ScribeRegistry.md` (registry, README, knowledge-expected, PROVINCE edits; after-values 49/106/52/89/87; `capture-binding-check` records=85 bound=85 unbound=0; six inherited W04).
- `ScoutF49.md` (F02/S075 overlap §1.3; acquisition-flow gap; zero hits for `monetary offer|pseudonym|remain anonymous`).
- `ConnectorScope.md` (six-party comparison; overlap scan §3.1; ledger-bind proposal §4, not done).
- `ScribeLesson.md` (lesson 199 lines; counter re-runs; mutation audit author-side; forgery `failures=12`).
- Not present (died): `CriticC1.md`, `CriticC2.md`, `MutationC1.md`, `SentinelGate.md`.

Committed corpus at tip `3cc8cd45`:
- `corpus/lessons/round-71.md` (sha256 `1186b63b…`; sections C1, C2, Gate, Mistakes M71-1, Routed defects V71-1…V71-3, Residuals).
- `corpus/README.md` F49 row (line 1114; `admitted`; entry `knowledge/zdi-disclosure-process-and-vendor-coordination.md`; sources `S106`) and the round-71 admission block (line 1099).
- `corpus/SOURCES.md` S106 row (line 118; tier A; `mined`; `opened 2026-11-05`; `recheck 180d`; used-by the entry); `## Registry changes` bullet (line 172 region, added in `34faab9`).
- `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md` (256 lines; Scope limits §125–135 name F02/S075 as owner of the policy-page timelines).
- `corpus/instruments/knowledge-expected.txt` (89 lines; line 89 is the new entry).
- `corpus/source-snapshots/round-71/S106.txt` and `manifest.json` (capture half, landed `4e33119`).

History and LOG shape:
- `LOG.md` lines 2709–2744 (round-68, round-69, round-70 entries: bullet shape, wave-outcome bullet, round-70 "not admitted" phrasing).
- `git log` subjects for `0e260a5`, `4e33119`, `453275f`, `34faab9`, `3cc8cd4`.

Attempt-2 dispatch (dispatched, not reported; listed in the draft):
- `.ufo/waves/round-71/w2-dispatch.json` (`spawn: 12`), `.ufo/waves/round-71/w2/swarm-registry.json`.
- `.ufo/waves/round-71/w1-dispatch.json` (`spawn: 14`), `.ufo/waves/round-71/w1/swarm-registry.json` (roles of all 14 members).

## 6. Gaps and what the L1 still owes

- The attempt-2 verdicts (`VerifyC1`, `AttackC1`, `MutateC1`, `SentinelC1`, `VerifyC2`, `AttackC2`) are not in the draft; the L1 appends them from `w2/` when they land.
- Counter values at tip `3cc8cd45` are not measured by this seat (the draft says so); the non-author closure measures them.
- Assimilation: the draft records that the collision count is not re-derived in any attempt-1 report; the L1 states the count from `assimilation/`.
- The `LOG.md` entry is a draft; it is not appended here. The L1 appends it after the non-author closure, or records the round as not admitted.
- R110: the lane has uncommitted round edits at `3cc8cd4` (§3 item 11); the L1 clears them.

## 7. Tooling and scratch

- Tools installed or upgraded: none. No `pacman`, `uv`, `npm`, or `cargo` activity; no `~/.local/bin` write.
- Scratch: `/fast/scratch/hyaku/kasegi-r71/DraftLog/` (one `git show` copy of the committed entry, used for §4 grep counts) and the one stray path `/fast/scratch/hyaku/kasegi-r71/DraftLog-entry.md`. Both removed before yield (see the final command of this seat).
- No subagent dispatched (leaf member). No `agent://all` message.
