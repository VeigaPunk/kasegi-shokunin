author: hyaku closure (non-author integrator, @m_opus)

# Round 34 — verifier spot-check (kasegi)

Non-author closure of lane-round kasegi 34. The lane's L1s were `KasegiR34` (attempt 1) and
`KasegiR34a2` (attempt 2). This reviewer re-measured the claims over committed bytes and
re-opened sources. It edited no lane-authored file.

- Report: `.ufo/reports/round-34/kasegi.md` (fleet commit `82eb2a461206fb3ae5fd682fe9282b44387fb29a`, author `kasegi-shokunin`, 2026-10-26 03:19:22 -03:00)
- Prompt: `.ufo/prompts/kasegi-round-34.md` (attempt-1 commit `6e0b9fd7`, attempt-2 commit `baa0a7f6`)
- Lane base: `014ee2d7aa8c3c095ff57ae51097606a9906228c`. Lane tip: `c1c6a5f826d2425446347173de527c42991b78b0` (branch `master`)

Driver digest (`.ufo/watchdog.log`, copied verbatim because the log is mutable):

```
2026-10-26T02:24:07-03:00 launch kasegi round=34 pgid=98669 driver=hyaku-inline attempt=1
2026-10-26T03:15:20-03:00 lane-dead-no-report kasegi round=34; retry same round (hyaku-inline attempt=1: L1 KasegiR34 exited without a landed round: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-34/kasegi.md)
2026-10-26T03:15:22-03:00 launch kasegi round=34 pgid=1260200 driver=hyaku-inline attempt=2
2026-10-26T03:19:31-03:00 complete kasegi round=34; hyaku-inline attempt=2
```

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an %H' -- .ufo/reports/round-34/kasegi.md` | `kasegi-shokunin 82eb2a46…` (03:19:22 -03:00, which is after lane tip `c1c6a5f` at 03:19:01) | ok |
| `SHONEN` heading, one line per box | `grep -c '^- \[' SHONEN.md` → 4. The report's `## SHONEN` section has 4 `[~]` lines that cite `SHONEN.md:5/21/34/54` | 4/4 | ok |
| Cited commits exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for `014ee2d 206e5108 29f606d 4b0a9f2 4eafa84 c1c6a5f` | all exit 0. Every round commit's author is `kasegi-shokunin` | ok |
| Lane pushed | `scripts/hyaku/jj-lane.sh state …/kasegi-shokunin` | `local=remote=c1c6a5f… ahead=0 behind=0 head=detached tracked=0 untracked=0` | ok |
| No uncommitted round work | `git -C kasegi-shokunin status --porcelain` | Empty at closure start. At 06:21:40Z: ` M .ufo/waves/round-34/wave1/ExecRegressionC1.md` (a seat rewrote it at 06:21:33Z and restored it at 06:22:26Z, sha back to `6b3604cb…`). At 06:23:46Z: `?? .ufo/waves/round-34/wave1-results.json` (312874 B, sha256 `3afa3581afb14aba…`, written 06:23:19Z, 65 results) | **defect D4**: wave writes landed after the `complete` line |
| Prompt carries the template contract | `diff <(sed -n 1,140p .ufo/prompts/kasegi-round-34.md) kimi-shokunin/templates/round-prompt.md` | Differences are only the `{{LANE}}/{{ROUND}}/{{AXES}}/{{FLEET_ROOT}}` substitutions. §1–§5 are verbatim, followed by hyaku §6/§7. No L2 route map is quoted | ok |
| Marker vs report | The report names work, evidence pointers and the commits `4b0a9f2/4eafa84/c1c6a5f` | real report | **status ok** |

Attempt 1 died without a report. Attempt 2 landed the same frozen claims (claims-freeze `29f606d`).
This is a retry within one lane-round and not a defect.

## 2. Claims — before → after (re-checked against `c1c6a5f`)

### C1 — depth:verifiability (score 4 held): R1–R9 closure suite

**Re-measured** with plain git/grep reads over committed blobs (`git show <rev>:<path>`, base `014ee2d` → tip `c1c6a5f`):

| item | before | after | reported | match |
|---|---|---|---|---|
| `corpus/instruments/r-defect-closure.sh` exists (`git cat-file -e`) | absent | present | absent → present | yes |
| `corpus/instruments/kill-rule-check.py` exists | absent | present | new | yes |
| `grep -c '<LANE_HASH>' SCORECARD.md` | 2 | 0 | 2 → 0 | yes |
| round-32 manifest `fetched_utc` values | `2026-10-25T23:14:00-03:00` ×2 | `2026-10-26T04:16:06Z`, `2026-10-26T04:16:16Z` | strict-UTC only | yes, but see note |
| round-26 manifest mentions of `S040-live` | 1 | 3 (top-level `orphans:[{"path":"S040-live.txt",…}]`) | orphan listed | yes |
| QUALITY R rows (`grep -oE '^\| *R[0-9]+ '`) | R1–R21 | R1–R25. The R20 per-id note sits under the appended block | R22–R25 + R20 note | yes |
| `c2-controls/junk-f17.md` in tree | absent at base | present (freeze `29f606d`) | committed | yes |
| `corpus/lessons/round-33.md`, `round-29.md` | — | +109/0 and +74/0 lines (`git diff --numstat`), so append-only | R7 erratum appended | yes |

Note on R8: the new values are not the original fetch time converted to UTC. They are
re-verification instants of byte-equal content. The manifest `purpose` text says so
(`wave1/ExecManifestR32Normalize.md`:54). Because this is disclosed it is not a defect. A separate
`reverified_utc` field would keep `fetched_utc` meaning what its name says.

**Evidence-verified (lane gate outputs, not executed here per §Gate standard):**
- `wave1/L1Integration.md` and `.raw` were measured on the integrated tree before commit `4b0a9f2`.
  `git diff --stat 4b0a9f2 c1c6a5f` touches only `ExecRegressionC1.md`, `LOG.md` and
  `corpus/lessons/round-34.md`, so no instrument or measured input moved after that commit.
  Committed outputs:
  - `closed=9/9 exit=0`
  - `selftest cases=9 failures=0`
  - `selftest cases=23 failures=0`
  - `records=41 bound=41 unbound=0`
  - `mutants=3 killed=3 survivors=0 invalid=0`, `gates=7 failed=0`
- Base-tree failure direction: `wave1/ExecRDefectClosureSuite.md` §5 → `closed=0/9 exit=1`, `base_exit=1`.
- `wave1/MutRSuiteChecks.md` → `18/18 killed, 0 survived`.
- Do-nothing controls (`c1-controls/`): the fake suite is rejected by `judge=forged-summary`, and
  `CTL-fake-killrule` → `opaque differs=1`.
- `records=40` literal: `claims-erratum-1.md` was filed before any scoring seat. The kill rule
  does not contain the `records` literal, so this is not a kill.

Kill-rule clauses were checked one by one: suite present; `closed=9/9`; selftest 9/9; capture-binding N=23≥19;
survivors=0; markers 0; strict-UTC; S040 orphan listed. **None triggered. C1 verifies.**

### C2 — coverage (score 7 held): F17 / S051

**Re-measured:**

| counter (frozen command, run on committed blobs) | before | after | reported | match |
|---|---|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 16 | 17 | 16 → 17 | yes |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 50 | 51 | 50 → 51 | yes |
| `grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md` | 0 | 1 | 0 → 1 | yes |
| knowledge entries with `^source: S051 ` | 0 | 1 | 0 → 1 | yes |
| `corpus/knowledge/*.md` count | 45 | 46 | 45 → 46 | yes |
| `sha256sum corpus/source-snapshots/round-34/S051.txt` | — | `4fd8ed98…b325a5` = manifest `sha256` | sha256 OK | yes |
| Manifest Q1–Q18, counted by this reviewer in Python over the capture (whitespace-normalized for Q2/Q5/Q6; anchor window = anchor line + 3) | — | 16 quotes occur exactly once. Q9 and Q17 occur twice and are anchor-verified at 77/96. Every anchored quote is inside its window | 18 OK, Q9/Q17 `occurrences=2` anchored | yes |
| `scripts/sources-census.sh validate --root … kasegi` (run at closure) | exit 0 | exit 0. Output is `W04 S028`, `W04 S029`, `kasegi ok` | exit 0, W04 only | yes |

**Evidence-verified:** the harness result `entries=20 pass=20 exit=0` incl. `PASS F17 … ids=S051`
comes from `wave1/L1Integration.md` and `.raw:68`. `recheck-audit.py` reports `strict pass=46/46`.

**Junk-twin dispute (lesson §Gate, left to the judge). Ruling:**
- The kill clause reads "junk twin passes source-recheck or is admitted". It is **not triggered**.
- The twin is not admitted (`ls corpus/knowledge | grep -ci junk` → 0).
- Its distinctive fabricated sentence is absent from the capture
  (`grep -c 'five severity levels for smart-contract' S051.txt` → 0). The quote check against the
  committed capture rejects it (`RevJunkTwin.md` §3: `MISMATCH reason=quote-not-found`, exit 1).
- The twin's own `recheck:` line exits 0 only because it re-checks the real S051 manifest, not the
  twin's content. That makes the frozen phrase "source-recheck exit != 0 on the twin; reviewer
  REFUSE" non-discriminating as written. The critics (`CritOverclaim` F1, `CritC2Kill` G5) are
  right about the **wording**, and the reviewer (`RevJunkTwin`) is right about the **fact**.
- Result: the wording is a defect (D5). It does not falsify C2.

The predicate clause "every assertion occurrences=1" is literally false (Q9/Q17 occur twice).
`SCORECARD.md` discloses this. The kill rule keys on `source-recheck exit != 0`, which is not met.
**C2 verifies.**

### No-harm

- `git diff 014ee2d c1c6a5f -- SCORECARD.md`: the only deletions are the 2 `<LANE_HASH>` lines
  and one `-after-column` reflow line, all replaced in place as R1 required. The rest is
  appended: the round-33 erratum 2 + R22 step, then the round-34 section.
- `SKILL.md` and `PROVINCE.md` each gain +1 line appended at end of file: an R6 correction and
  the F17 frontier amendment.
- `density.py` mean 201.7 → 201.2 (`L1Integration.md`). This is a one-line factual correction,
  with no content lost and the score held at 9. Grade: unchanged.
- Append-only lesson and QUALITY files show 0 deleted lines (`git diff --numstat`).

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| depth:verifiability | **improved** (score held 4) | C1 verified: nine routed defects closed by a fail-closed suite (base `closed=0/9`); two frozen-rule survivors killed |
| coverage | **improved** (score held 7) | C2 verified: frontier 16→17, registry 50→51, F17 entry on S051 |
| depth:density | **unchanged** | no claim. 201.7→201.2 from a 1-line R6 correction, score 9 held |

## 4. Discernment spot-check (lesson `corpus/lessons/round-34.md` § Gate)

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| F17 entry + S051 row | admit | Live `curl -sSL https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/` → `200 219384 B` (2026-10-26 ~06:20Z). Tag-stripped text contains the lesson quote «At Immunefi, we classify bugs on a simplified 5-level scale» (lesson quote 1, 11 words) and «Direct theft of any user funds, whether at-rest or in-motion» (lesson quote 2, 14 words). Also present: «Permanent freezing of funds», «Temporary freezing of funds», «Protocol insolvency», «Unbounded gas consumption», `v2.2`. Capture sha matches the manifest. Q1–Q18 were counted as above | agree | Tier A is correct: this is Immunefi's own docs, scoped to its own system. Both gate quotes are ≤25 words, located, and present both live and in the capture. The entry is on uncovered ground (F17) |
| `claim-packaging-and-report-quality.md` (`6ad64d78`) | reject (standing) | `shokuknow/merge/kasegi/knowledge/corpus/knowledge/claim-packaging-and-report-quality.md:6` cites `S036 — https://security.bilibili.com/static/docs/BILISRC_V1.7.pdf`. In the lane, `grep -ci bilibili corpus/SOURCES.md` → 0 and lane `S036` is Cybozu's 脆弱性情報ハンドリングポリシー (`SOURCES.md:42`) | agree | The source is unregistered in the lane and its id collides. Adopting by number would mis-cite |
| `chinese-crowd-testing-national-standard-2026-10-23.md` (`6c15d941`) | reject (standing) | same package: `ground: F24`, `grep -c '「'` → 0, cites S077/S078/S079. Lane: `grep -cE 'std.sacinfo.org.cn\|sac.gov.cn\|57CAF3B4' SOURCES.md` → 0. Lane frontier ends at F17 | agree | Every reason the lesson gives reproduces |
| `cn-crowdsourced-testing-roles-and-conduct.md` (`a5302aaf`) | reject (standing) | `grep -c '^# '` → 0 (no H1). It cites S081/S082, and the lane has 0 such rows | agree | Reproduces |
| Quarantine `S048` (GB record) | unreachable | Register `absent-defect-register.md:322` (sha `5afe1810a6c3`). `curl https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3` → `404 748` (twice, with and without a browser UA) | agree | Matches the lesson's `404 (748 B)` exactly. It is unreachable, not a fabrication |
| Junk twin `c2-controls/junk-f17.md` | not admitted (control) | `grep -c 'five severity levels for smart-contract' corpus/source-snapshots/round-34/S051.txt` → 0. No `junk` file in `corpus/knowledge/` | agree with non-admission | The wording dispute is ruled in §2 C2 (defect D5). The twin is a mixed control: one of its two sentences is real text (ScoutDatawalk F-1b) |

SOURCES row re-opened: **S051** (`SOURCES.md:57`). The URL resolves live. Both ≤25-word gate quotes
are present live and in the capture. The anchor cites capture lines L45/L46/L72–L96, which match the
manifest anchors. Tier A, kind `docs`, status `mined`, used-by the F17 entry (the path exists).
Census exits 0.

## 5. Trend verdicts

- **expansion: improved.** One admitted knowledge entry on ground the coverage map did not hold
  (F17). It cites `source: S051`, a `mined` row opened this round. Frontier 16→17.
- **quality: improved.** Instruments were hardened and no admitted entry failed its re-check:
  - R1–R9 closure checks fail closed on the base tree.
  - capture-binding selftest 11→23.
  - recheck-audit `strict pass=46/46` (evidence-verified).
  - S051 re-opened live and agrees with the capture.
  - Stale pins corrected append-only (`SKILL.md` +1, round-29/33 lessons).
- **discernment: improved.** This spot-check agrees with the gate on 1 admit and 4 rejects or
  refusals. Round-33's routed defects R1–R9 all landed. Mistakes M34-1…M34-6 became grounded
  criteria: R24 (lesson round-33 verifier R4) and R25 (M34-3).

## 6. Routed defects (owner: kasegi, land next round; status-neutral)

- **D1 — unfilled lane-commit placeholder (R1 class, recurs).**
  - Where: `SCORECARD.md:1129` ("**Final lane commit: the L1 fills this line in the closing
    commit.**") and `SCORECARD.md:1240` ("**Round-34 final lane commit: filled by the L1 in the
    closing commit.**"). Both are still unfilled at `c1c6a5f`.
  - Why the suite missed it: the R1 marker check only matches the `<LANE_HASH>` spelling
    (CritC1Kill: "spelling-brittle").
  - Fix: append a correction naming `c1c6a5f826d2425446347173de527c42991b78b0`, and widen the R1
    check to placeholder prose.
- **D2 — stale SCORECARD depth:density row.**
  - Where: `SCORECARD.md:1145` (round-34 depth:density row).
  - It says `SKILL.md`/`PROVINCE.md` have 0 changed lines and mean 201.7. At the tip each has
    +1 line and the mean is 201.2 (`wave1/L1Integration.md`).
  - Fix: append a correction.
- **D3 — gates unregistered at the registry home.**
  - `r-defect-closure.sh` and `kill-rule-check.py` have no row in the `SKILL.md` Gates & probes
    registry (`grep -n 'r-defect-closure\|kill-rule-check' SKILL.md` → none).
  - Per PROTOCOL §Gate standard (Delivery), they are not graded conformant until registered.
  - Fix: register each with name, gate|probe, entry command, verdict map, selftest spelling,
    pinned-value path, write scope and owner.
- **D4 — wave writes after the `complete` line.**
  - The wave dispatcher wrote untracked `.ufo/waves/round-34/wave1-results.json` at 06:23:19Z.
  - A seat transiently rewrote the committed `wave1/ExecRegressionC1.md` at 06:21:33Z, claiming
    measurement "at c1c6a5f", then restored it.
  - Fix: commit `wave1-results.json` with a provenance note. The L1 must quiesce or kill wave seats
    before its final commit.
- **D5 — frozen predicate wording not executable or literally false.**
  - The C2 junk-twin phrase "source-recheck exit != 0; reviewer REFUSE" has no discriminating
    invocation.
  - "Every assertion occurrences=1" is false for Q9/Q17.
  - Fix: append a claims erratum with the wording RevClaimsFreeze D-2 recommended. Future twins
    should carry only absent sentences.
- **D6 — stale note in `wave1/L1Integration.md:30`.**
  - The note says `ExecRegressionC1` "did not file a receipt (dead seat)". That receipt is
    committed in `c1c6a5f`.
  - Fix: append a correction.
- **D7 — R22 grounding cites the wrong mistake.**
  - QUALITY R22 cites M34-2, but its grounding is M34-3 (lesson open item 10; `CritMistakes` F7).
  - QUALITY R23's grounded-in column cites `considerthese/2026-10-25.md:76` rather than the
    round-34 lesson §considerthese.
  - Fix: append a supersession row or note.

## 7. SHONEN

All four boxes are still `[~]`. No new end-to-end domain task ran (box 2), so the boxes are not
fully checkable by a non-author this round. There is nothing to raise with the operator for
promotion.
