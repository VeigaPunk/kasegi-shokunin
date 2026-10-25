# RevCloseCheck — round 28 wave 1 final close-out checklist

- Seat: RevCloseCheck (reviewer, leaf; read-only — no production edit, no subagents, no installs, no pacman).
- Snapshot taken: 2026-10-25T17:24:47Z (UTC). **The wave was still in flight** — several seats land after this
  snapshot; every PENDING below names the exact check the L1 runs at close. An unrun check has not passed.
- Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin; claims freeze base c9f8b115a098c65356e4b3b6048af45a37ab8395
  (verified ancestor of worktree HEAD 94f387cbee71a532a51ce075f01701a557231e85 = "round-28: wave1 spec + dispatch").
- Sources of record: .ufo/waves/round-28/claims.json (frozen), wave1-dispatch.json, wave1/swarm-registry.json,
  .ufo/waves/round-28/receipts/*, .ufo/waves/round-2{7,8}/c1-controls/*, c2-controls/*, census-before.txt.

## Checklist — go/no-go list

### (1) Every production change maps to the ownership map AND to a wave receipt — GO (structure), receipts PARTIAL
No cross-ownership write observed: `git status --porcelain` at snapshot shows exactly the owner files modified
(QUALITY.md, README.md, SOURCES.md, LOG.md) plus untracked `corpus/source-snapshots/round-28/`; all seat scratch
is confined to `wave1/<SeatName>/`. Per-change map (state at 17:24:47Z):

| production file | owner (dispatch) | landed? | receipt `.ufo/waves/round-28/receipts/<Seat>.txt` |
|---|---|---|---|
| corpus/instruments/anchorcheck.py | ExecImplC1 | NO — digest still c2a9e6c6… (frozen before) | PENDING |
| corpus/instruments/README.md | ExecInstrReadme | NO | PENDING (scratch `wave1/ExecInstrReadme/` present) |
| SKILL.md | ScribeSkillGate | NO | PENDING |
| corpus/source-snapshots/round-28/S041.txt | ExecCaptureS041 | YES | LANDED (capture_exit=0, sha256 e18acbf9… log==disk) |
| corpus/source-snapshots/round-28/S042.txt | ExecCaptureS042 | YES | LANDED |
| corpus/source-snapshots/round-28/manifest.json | ExecManifest | YES (S041+S042, sha256 match captures, Q9 quote assertions) | PENDING |
| corpus/knowledge/japanese-domestic-disclosure-workflow.md | ScribeEntryC2 | NO | PENDING (scratch `wave1/ScribeEntryC2/`) |
| corpus/SOURCES.md | ScribeRegistryC2 | YES (S042 row: tier A field4, mined field8, opened 2026-10-25 field9, used-by field11 = exactly the entry; S041 used-by old→new logged in the file's own changelog, line 79) | PENDING (scratch `wave1/ScribeRegistryC2/`) |
| corpus/README.md | ScribeReadmeC2 | YES (F12 row admitted, README.md:213) | PENDING |
| corpus/QUALITY.md | ScribeR14 | YES (R14 appended at end, 6 insertions/0 deletions) | LANDED |
| corpus/lessons/round-28.md | ScribeLesson | NO | PENDING |
| LOG.md | ScribeLog | YES (round-28 entry, after-values marked PENDING honestly) | PENDING (scratch `wave1/ScribeLog/`) |
| SCORECARD.md | ScribeScorecard | NO | PENDING |

Rule for close: a production change without its receipt is not closed. The five PENDING receipts for already-landed
files (ExecManifest, ScribeRegistryC2, ScribeReadmeC2, ScribeLog + ExecImplC1/ExecInstrReadme/ScribeSkillGate/
ScribeEntryC2/ScribeLesson/ScribeScorecard when their files land) must exist before the L1 commits.

### (2) Four routed dispatch requirements (claims.json `dispatch_requirements`) — 2 evidenced, 2 owed at close
- **R1 reviewer seats inside the build wave — GO, EVIDENCED.** wave1-dispatch.json `counts.spawn=69`;
  swarm-registry.json lists 69 members, of which **12 are reviewer seats**: RevImplC1, RevFixturesC1, RevNoHarmC1,
  RevEntryC2, RevRegistryC2, RevManifestC2, RevCounters1, RevCounters2, RevCensusEnd, RevDensityGuard,
  RevReceiptsCanon, RevCloseCheck (this seat). Round-26 routed defect 2 is structurally fixed.
- **R2 inline ≤25-word Gate quotes in the round lesson — PENDING.** `corpus/lessons/round-28.md` ABSENT at
  snapshot (ScribeLesson; Gate draft seat ScribeLessonGate also not yet in wave1/). L1 check at close: the lesson's
  Gate block carries ≥1 admit and ≥1 reject, each with an inline quote ≤25 words (see item 5).
- **R3 one canonical receipt index at the landed instrument digest; no mid-wave receipt artifacts — GO on the
  guard, artifact OWED at close.** `.ufo/waves/round-28/c1-receipt-index.txt` is correctly ABSENT mid-wave; the
  draft seats' prompts explicitly forbid creating it ("Do NOT create .ufo/waves/round-28/c1-receipt-index.txt
  (defect 4: one canonical receipt, assembled by the L1 at the landed digest)"), and the L1's assembly helper
  `.ufo/waves/round-28/assemble-receipts.py` exists but has not been run. Per-seat receipts accumulate only under
  `receipts/` (no scattered canonical artifacts — defect 4 guard holds). At close, AFTER ExecImplC1 lands and the
  evidence commits, the L1 runs `python3 .ufo/waves/round-28/assemble-receipts.py` from the lane root; the index
  must contain `instrument_sha256=` equal to `sha256sum corpus/instruments/anchorcheck.py` and a
  `selftest cases=N failures=0` line (claims C1 counter 3 greps exactly these).
- **R4 round-27 routed defects — BOTH OWED AT CLOSE.**
  - *Fleet report before returning* (r26 defect 1, r27 ordering note): L1 close-out action; no seat artifact can
    evidence it. The LOG.md round-28 entry already reserves the after-value append for the L1 at close.
  - *Expected-list count basis reconciled* (r27 carry-forward 4): PENDING — `receipts/ExecExpectedList.txt`
    ABSENT. Measured basis at 17:24Z: `corpus/knowledge/*.md` = **39** entries;
    `corpus/instruments/knowledge-expected.txt` = **39** entries (41 lines incl. 2 comment lines);
    `python3 corpus/instruments/recheck-audit.py` → `expected=39 missing=0 unexpected=0 exit=0`. The moment the
    F12 entry lands the tree has 40 entries against an expected list of 39 → audit exits nonzero
    (`unexpected=1`) unless the list is **regenerated via recheck-audit `--expect`** (regeneration, not
    arithmetic — r27 carry-forward 4). Order at close: entry lands → ExecExpectedList regenerates → audit exit 0.

### (3) Misroot sweep evidence (ExecScopeSweep) — PENDING (seat working)
`receipts/ExecScopeSweep.txt` ABSENT at snapshot; scratch `wave1/ExecScopeSweep/scope-check.sh` present.
Supplementary sweep by this seat (17:24Z, read-only): fleet root `/home/vgpnk/Projects/shokunin` git status shows
only L1-machinery files (`.scratch/goal-20261025-hyaku-run7.md`, `.ufo/state/{kasegi,kengaku,souji,tabi}.report-baseline`,
`.ufo/watchdog.log`) — no kasegi seat-owned path; no kasegi wave file outside `kasegi-shokunin/.ufo/waves/round-28/`.
The authoritative misroot evidence is ExecScopeSweep's (and SentinelScope's) receipt — still owed.

### (4) No fleet-root writes — GO on observed evidence, confirmation receipt pending
Same sweep as (3): zero writes by this wave's seats to the fleet root, sibling lanes, or the READ-ONLY package.
`/home/vgpnk/Projects/shokuknow`: **0 files** with mtime ≥ 2026-10-25 17:00 local (wave spawned 14:22:08 local
per `wave1.ready.dispatched`). Sibling lanes kengaku/souji/tabi/etc.: 0 wave-time writes; the only `-newermt`
hits fleet-wide were 6 **future-dated** (2026-11/12) fixture files under `chousa-shokunin/.ufo/waves/round-33/…`
— that lane's own round-33 artifacts, not kasegi seats. The modified fleet-root state files are the hub's own
report-baseline/watchdog machinery (attribution: L1), to be confirmed by ExecScopeSweep/SentinelScope at close.

### (5) Lesson Gate ≥1 admit + ≥1 reject with inline quotes — PENDING
Lesson ABSENT (same blocker as R2). Gate raw material already exists in the wave:
`assimilation/guard-proof.txt`, `assimilation/collision-check.txt`, `assimilation/fixture/*` (ScoutAssimilation),
ScribeSourcesGate try-files (`wave1/ScribeSourcesGate/S041.try.txt`, `S042.try.txt`), ScribeRegistryC2 scratch.
L1 check at close: `corpus/lessons/round-28.md` Gate block quotes ≥1 admit and ≥1 reject inline, each ≤25 words.

### (6) Do-nothing receipts exist (r27 + r28 before receipts) — GO, VERIFIED ON DISK
- r27: `.ufo/waves/round-27/c1-controls/` = bad-fixture-before.txt, bounties-fixture-before.txt,
  instrument-digest-before.txt, selftest-before.txt, skill-before.txt; `.ufo/waves/round-27/c2-controls/before.txt`.
  All present.
- r28 (fresh re-runs, read by this seat): `.ufo/waves/round-28/c1-controls/` = same five files +
  `c2-controls/before.txt` + `census-before.txt`. Contents reproduce every frozen before value:
  bad-fixture exit=0 (BASE-ABSENT printed); bounties-fixture 0 BOUNTIES-ABSENT lines; selftest crash
  FileNotFoundError exit=1; SKILL.md exit=0 bad=0 LOST-RECORDED=306 PIN-BROKEN=0 OUTSIDE-BASE=0 BASE-ABSENT=0;
  instrument digest c2a9e6c6…ef748; frontier_admitted=11, S042-citing=0, S042 rows=0, census exit=0 (W04 S028/S029
  pre-existing), harness entries=14 pass=14 exit=0. The do-nothing control is clean — no before-receipt drifted
  into an after-value.

## Residual risks (NO-GO if unchanged at close)
1. **TOP — C2 mid-wave ordering hazard (observed, verbatim):** README.md:213 admits F12 while the entry file is
   absent → `python3 corpus/instruments/frontier-recheck-count.py` crashes
   `FileNotFoundError: .../corpus/knowledge/japanese-domestic-disclosure-workflow.md`, exit 1 (observed 17:23Z).
   Transient ONLY if ScribeEntryC2 lands. If the wave closed now, C2's kill rule ("harness pass < entries") trips
   and the harness is worse than before (crash vs 14/14). Gate the close on the C5 re-run: entries=15 pass=15 exit=0.
2. **C1 entirely unproven at snapshot:** anchorcheck.py still at frozen pre-change digest c2a9e6c6…; all three
   ExecFixtureRun counters reproduce `before`, none reach `after`. Until ExecImplC1 lands and the counters re-run,
   C1 is NOT VERIFIED (same honest stop as round 27).
3. **Receipt debt for landed files:** ExecManifest, ScribeRegistryC2, ScribeReadmeC2, ScribeLog receipts absent
   while their production files are already modified (item 1 table).
4. **Expected-list ordering:** if the F12 entry lands and ExecExpectedList does not regenerate
   `knowledge-expected.txt` (39→40 via `--expect`), the round-end recheck-audit exits nonzero — a self-inflicted
   gate failure (r27 carry-forward 4).
5. **Canonical index timing:** `c1-receipt-index.txt` must be assembled by the L1 only after the instrument lands
   and the digest is final; running assemble-receipts.py earlier would pin a stale digest (defect 4 recurrence).

## Exact L1 close-out verification block (lane root; consolidated from ExecFixtureRun + ExecC2Counters + this seat)
```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/instruments/anchorcheck.py
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo "bad_fixture_exit=$?"          # expect 1
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT            # expect 1
python3 corpus/instruments/anchorcheck.py --selftest; echo "selftest_exit=$?"                                                                  # expect cases=N failures=0, exit 0
python3 corpus/instruments/anchorcheck.py SKILL.md >/dev/null 2>&1; echo "skill_exit=$?"                                                       # expect 0
python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | grep '^== '                                                                   # expect bad 0, LOST-RECORDED=306, others 0
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md                                                   # expect 12
grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l                                                                                        # expect 1
grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md                                                                                 # expect 1
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "census_exit=$?"             # expect 0, 42 rows
python3 corpus/instruments/frontier-recheck-count.py                                                                                           # expect entries=15 pass=15 exit=0
python3 corpus/instruments/recheck-audit.py | tail -1                                                                                          # expect expected=40 missing=0 unexpected=0 exit=0 (after --expect regen)
grep -cE 'selftest cases=' .ufo/waves/round-28/c1-receipt-index.txt && grep -oE 'instrument_sha256=[0-9a-f]{64}' .ufo/waves/round-28/c1-receipt-index.txt   # after assemble-receipts.py
```
Plus the close-only L1 actions: assemble the canonical index (post-commit, at the landed digest); land the fleet
report before returning; confirm ExecScopeSweep + SentinelScope receipts; confirm the lesson Gate quotes.

## Seat hygiene
No tools installed or upgraded; no pacman transaction; no VCS write; no writes outside this receipt file and the
read-only checks above. All numbers in this receipt were run or read by this seat at the stated timestamps.
