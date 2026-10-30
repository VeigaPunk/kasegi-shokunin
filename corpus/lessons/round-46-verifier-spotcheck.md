# kasegi round 46 — non-author verifier spot-check (hyaku closure)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-10-30
Judged tip: `4cdcf7bdea8bea06705de752a2796d4e3aab0242` (refs/heads/master, pushed, ahead=0).
Report: `.ufo/reports/round-46/kasegi.md` (fleet commit `07e3fccf`, author `kasegi-shokunin <kasegi@shokunin.local>`).
Round base `04af9bc92229232ea5cce8b32bfe59dd969eb26d`; pre-round lane HEAD `7eb7786d` (ancestor of master: yes).
Method (PROTOCOL §Gate standard, Closure consequence): the round's claims rest on lane-owned gates,
selftests and the mutant battery — their committed evidence was verified (receipts, revision stamps,
tallies); no lane gate/battery/selftest was executed by this closure. Plain counting commands were
re-run by this closure at the tip and at the base.

## 1. Step-1 conformance

| Check | Result |
|---|---|
| Report committed by lane identity | PASS — `git log --format='%an <%ae> %H' -- .ufo/reports/round-46/kasegi.md` → `kasegi-shokunin <kasegi@shokunin.local> 07e3fccf…` (attempt-2 file, 2026-10-30 01:19:12 -03:00); attempt-1 file at `d4bc8977`, same identity |
| `SHONEN` heading, one line per box | PASS — `## SHONEN` with 4 `[~]` lines matching SHONEN.md's 4 boxes; no `[x]` written by the lane |
| Cited commits exist and are ancestors of the branch ref | PASS — `fe0f56b7`, `ee03806b`, `96379ae2`, `ec114ac7`, `c8641e7a`, `a2ce104e`, `4cdcf7bd`, `04af9bc9`, `7eb7786d` all `git merge-base --is-ancestor <h> master` yes (jj-colocated; tested against `refs/heads/master`, never `@{u}`) |
| Lane clean and pushed | PASS — `jj-lane.sh state` → `branch=master local=4cdcf7bd remote=4cdcf7bd ahead=0 behind=0`; `git status --porcelain` empty; `git ls-remote origin refs/heads/master` = `4cdcf7bd` |
| Dispatched prompt carries the template contract | PASS — round-level items (mission/axes binding; 1–3 claims with the lowest-non-retired-axis rule; L2 ≥8 in one batched call; commit-then-push; push scope; L0 side channel) plus the five child-lane items (report path+filename; commit-before-report ordering; SHONEN heading requirement; commit-hash citation rule; write scope). L2 minimum matches MISSION.md §L2 concurrency |
| Dispatch/completion evidence | PASS — watchdog digest below |

Dispatch/complete digest (copied per contract; `.ufo/watchdog.log` is mutable):

    2026-10-28T19:52:51-03:00 launch kasegi round=46 pgid=3684502 driver=hyaku-inline attempt=1
    2026-10-28T23:40:19-03:00 complete kasegi round=46; hyaku-inline attempt=1
    2026-10-29T17:09:58-03:00 launch kasegi round=46 pgid=3369392 driver=hyaku-inline attempt=1
    2026-10-30T01:20:39-03:00 complete kasegi round=46; hyaku-inline attempt=1

## 2. Claim re-checks

### C1 — depth:verifiability (mutation coverage of the attempt-1 counters) — evidence-verified

- `claims.json` re-hashed: `ca73279f5464cf6395028c7e848b5d82bfec95794f03b7fd9b1a61cf000ca1d0` — matches
  the report and SCORECARD; frozen at `fe0f56b`, an ancestor of the wave-1 dispatch commit `ee03806b`
  (counters + controls committed before any seat ran). Shape: 2 claims (`C1 depth:verifiability`,
  `C2 coverage`), neither exploratory; C1 works the lane's lowest non-retired axis (4).
- Before receipt `controls/mutbat-before.txt` (re-read): `mutbat counter=c1 mutants=20 caught=13
  equivalent=0 uncaught=7 baseline_failures=0` and `mutbat counter=c2 mutants=21 caught=8 equivalent=0
  uncaught=13 baseline_failures=0`, `BATEXIT=1` — matches the reported before.
- After receipts `controls/final-battery-summary.txt`, `final-battery-c1.txt` (ends `EXIT=0`),
  `final-battery-c2f29.txt`: c1 `caught=19 equivalent=1 uncaught=0`; c2 and f29 `caught=18
  equivalent=3 uncaught=0`; selftests `83/0`, `147/0`, `30/0` — match the reported after.
- Revision: `controls/final-measure.txt` self-stamps `measured-at-rev: c8641e7a…`. Closure re-measured
  `git diff --stat c8641e7a 4cdcf7bd -- . ':(exclude).ufo/waves'` → empty: the receipted measurements
  describe lane bytes identical to the judged tip.
- Wave-2 crash fixes present at tip: `r46-counters-selftest-c2.py` defines `C1_ENTRIES` (line 68)
  before `EXEMPT_ENTRIES` (line 69); `r46-selftest-f29.py:197` accepts the landed 29-row README
  (`expected 28 (pre-landing) or 29 (landed)`).
- Verdict: **verified** (evidence-verified; the lane's battery/gates were not executed).

### C2 — coverage (frontier F29) — re-measured (plain commands run by this closure)

| Counter | base `04af9bc9` | tip `4cdcf7bd` | Reported |
|---|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 28 | 29 | 28 → 29 — match |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 73 | 74 | 73 → 74 — match |
| `find corpus/knowledge -maxdepth 1 -name '*.md' \| wc -l` | 65 | 66 | 65 → 66 — match |
| Absence sweep `grep -rliE 'repository securit. advisor\|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md \| wc -l` | 2 | 4 | 2 → 4 — match |
| `scripts/sources-census.sh validate --root … kasegi` | — | exit 0, same 3 W04 (S028, S029, S072) | exit 0, unchanged warnings — match |

Committed gate evidence (verified, not re-run): `final-measure.txt` shows `r46-f29-gate.py` base export
`fixed=1/7 exit=1` → tip export `fixed=7/7 exit=0` (H5 `spans=45 located=45 failed=0 uncited=0
cores=5/5`); `r44-frontier-count.py --expect 29` tip `rows=29 admitted=29 exit=0`.

### No-harm

- `git diff --stat 04af9bc9 4cdcf7bd -- SCORECARD.md` → 27 insertions, 0 deletions (append-only).
- `density.py` blob identical base→tip (`git rev-parse <rev>:corpus/instruments/density.py` =
  `1f99e66f…` for both) — the report's "byte-identical" claim holds.
- Deleted tracked files outside `.ufo/waves/`: none (`git diff --diff-filter=D --name-only`).
- SKILL.md density mean 258.7 → 275.1 moves only by the appended Gates & probes block (34th block),
  not credited — consistent with SCORECARD.
- Attempt-1 instruments (committed receipt): c1-gate `7/7` at the tip against its `914ca0b` baseline
  and `1/7` at that base; c2-gate v1.3 `7/7` at era export `eb874bc`, `5/7` at the tip with G1/G6
  expected-moved by this round's landing — all match the report.

## 3. Wave evidence

- `a2w1-results.json` 64 seats, wave-2 results 32 seats; round total 96; zero empty/missing outputs —
  **0 dead seats**, both waves. Dispatch↔results identity verified both ways for both waves; wave-1
  dispatch committed at `ee03806b` carries 64 members/64 tasks; wave-2 dispatch 32; freeze
  `fe0f56b` is an ancestor of `ee03806b`.
- Role mixes match the report's tables (a2w1: scribe 15, reviewer 12, executor 11, scout 9,
  mutation-tester 7, critic 5, sentinel 2, connector 1, revenger 1, simplifier 1; a2w2:
  mutation-tester 10, critic 7, reviewer 6, executor 3, scout 2, connector 1, revenger 1, sentinel 1,
  simplifier 1).
- **D1 (numeric defect).** The report states a2w1 attack "27/64 = 42.2 %" under its own definition
  "(reviewer/critic/mutation-tester)", but those roles sum to 12+5+7 = **24/64 = 37.5 %** — the figure
  LOG.md correctly prints; the 27 comes from the wave builder's print, which counts a broader attack
  set (incl. sentinel+revenger). The ≥25 % attack-share floor holds either way. a2w2's
  "23/32 = 71.9 %" verifies as stated.
- **D2 (pointer defect).** The report cites `.ufo/waves/round-46/attempt2/a2w2-results.json`; the file
  is committed at `.ufo/waves/round-46/a2w2-results.json` (one level up). Resolvable, mis-cited path.

## 4. Discernment spot-check (LEARNING.md — Discernment is checked from outside)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S074 admit — F29, GitHub repository security advisories, maintainer-side lifecycle | admit | Live re-open 2026-10-30 (curl -sSL): HTTP 200, final URL = canonical URL recorded in manifest; capture re-hashed `sha256sum` = `1296528d…7839` (42 lines / 7087 bytes); manifest `url` == `capture_url`; distinctive substrings of Q2/Q5/Q7/Q4/Q9 all present in the live HTML | **agree** | Tier A first-party docs, scope honestly limited (maintainer flow only; reporter flow stays F28); capture sha-pinned; zero drift against the live page |
| Gate quotes Q1–Q9 | admit support | Each quote `grep -Fi` at its cited capture anchor — 9/9 OK at lines 10, 13, 17, 24, 25, 25, 26, 31, 38 of `S074.txt`; each ≤25 words; lane's `source-recheck.py` receipt prints Q1–Q9 OK, exit 0 | **agree** | Locations exact; word counts within the ≤25-word rule; the F29 entry's "Decision rule" and "Falsifiable package rule" sections state a rule a maintainer can act on (the C2 kill rule), incl. the covered-by-CNA boundary |
| Reject: GitHub Advisory Database as the F29 source | reject | `S068` row re-opened in `corpus/SOURCES.md`: kind docs, tier B, **status rejected**, teaches "republishes the NVD record", screen receipt cited in-row (round-43 `ExecRegistryRows.md`) | **agree** | The cited precedent exists and carries the reason; the database is the publication target of F29, not the lifecycle's first-party statement; flip recorded |
| Reject: repository-advisories REST API page | reject (kept lead) | Pointer verified at `S074.txt:16` in the capture | **agree** | CORPUS rule 1: a lead is not a row without opening; flip (open + located quotes in a later round) recorded |
| Reject: ZDI lead stays a lead | reject | Attempt-1 screen `wave1/R46ScoutLeadZDI.md` (sha-pinned seat capture) | **agree** | Overlaps F02's timelines, page names no start event for the 120-day clock; flip unchanged from attempt 1 |

Newly written `SOURCES.md` row re-opened: S074 (above). Census re-run by this closure: `kasegi ok`,
exit 0, same three W04 warnings as the before/after receipts.

## 5. Per-axis verdicts (closure)

| Axis | Verdict | Evidence |
|---|---|---|
| depth:verifiability | unchanged (held at 4; claim verified) | 41 counter mutants 20 uncaught → 0 uncaught / committed-proof (receipts); score held, promotion limbs unmoved (SCORECARD r46a2) |
| coverage | unchanged (held at 8; claim verified) | F29 admitted, 28 → 29 = expansion count, ratio (20+F_admitted)/(20+F_total) stays 1.000 (SCORECARD r46a2) |
| depth:density | unchanged (held at 9) | `density.py` byte-identical base→tip (blob `1f99e66f…` both); SKILL.md mean moved only by the appended registry block, not credited |

No owned axis harmed. Both claims verify → the round is admittable.

## 6. Trend verdicts (closure)

- **expansion: improved** — F29 admitted on ground the corpus did not hold (absence sweep 2 → 4,
  re-measured at base/tip), S074 tier A `mined` with a sha-pinned capture (sha re-verified), SOURCES
  73 → 74, knowledge 65 → 66, census exit 0.
- **quality: improved** — the measurement instruments are the round's artifact: battery before
  7+13 uncaught → after 0 uncaught with committed equivalence proofs; extended selftests 83/0, 147/0,
  30/0; the f29 gate froze with an R50 receipt, was falsified by seven tree-level false-greens and
  closed in v1.1; two crashed instruments (C2 selftest NameError, f29 selftest 28-row precondition)
  were found by wave 2, fixed, and the fixes verified at tip by this closure; every fix changed
  committed bytes under a logged erratum.
- **discernment: improved** — this non-author spot-check agrees with the gate on the S074 admit and
  all three rejects (§4); the lesson's open spot-check slots are now filled; the round-45 spot-check
  items are dispositioned as mined mistakes M46-1..M46-3; calibration critic findings were
  integration defects (fixed, receipted), not self-assessment mismatches.

## 7. Routed defects (lane owes its repo next round; corrections append, never rewrite)

- **D1** — report §Work performed: a2w1 attack share "27/64 = 42.2 %" contradicts its own role table
  and LOG.md's correct "24/64 = 37.5 %" (builder-print definition mismatch). ≥25 % floor met either
  way. Fix: erratum/correction line in the next round's report.
- **D2** — report §Work performed: `a2w2-results.json` cited under `attempt2/`; committed at
  `.ufo/waves/round-46/a2w2-results.json`.
- **D3** — report §Before→after no-harm: "The only tracked deletions outside the wave dir: none …
  numstat … shows appends and the ledger/entry additions only" — numstat in fact shows 4
  `corpus/instruments` files with line deletions (`knowledge-expected.txt` 4+/3−, `r46-c2-gate.py`
  40+/9−, `r46-counters-selftest-c1.py` 112+/11−, `r46-counters-selftest-c2.py` 217+/6−; the wave-2
  in-place fixes). Deleted *files* = 0 and no axis is harmed; the citation as written is false. The
  fixes themselves are legitimate in-place instrument repairs under logged errata — correct the
  sentence, not the fixes.
- **D4** — report: the pre-report landing-gate claim ("`r46-landing-gate.py --pre-report` reads 4/4
  checks pass, exit 0, at the same hash") has no committed receipt in the round dir (only spec/builder
  references). The underlying fact — lane pushed, remote == local == `4cdcf7bd` — was independently
  verified by this closure via `jj-lane.sh state` + `ls-remote`. Next round: tee the gate transcript
  beside the run (the round-41 I2 lesson).
- Observation (not a defect): `final-measure.txt` self-stamps `measured-at-rev: c8641e7a` while the
  report says "at tip `4cdcf7bd`"; closure measured the `c8641e7a`→`4cdcf7bd` delta outside
  `.ufo/waves` as empty, so the receipted bytes equal the tip's lane bytes. Keep the wording exact.
- Operator note: all four SHONEN boxes remain `[~]` with resolvable pointers; boxes 1, 3 and 4 look
  fully checkable by a non-author on the current evidence — promotion review is operator-owned.
- L0 open question carried (routed around, not blocking): whether the 22 remaining gated `recheck:`
  entries may be re-labelled historical records.
