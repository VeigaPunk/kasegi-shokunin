# kasegi round 35 — report draft

**Draft only.** This file is composed by seat `ScribeReportDraft` (scribe, leaf of wave 1) from the
round-35 wave receipts; the L1 (`KasegiR35`) integrates it into `.ufo/reports/round-35/kasegi.md` and
substitutes every `<LANE_HASH>` / `<WAVE_DISPATCH_HASH>` / `<LOG_COMMIT>` placeholder. Nothing here
is written to the fleet repo. Where a value was measured at draft time the read instant is given;
where a value depends on a landing the L1 has not made yet, both the draft-time reading and the
post-landing expectation are stated, and the receipt that proves the fix is named.

Lane: `kasegi-shokunin` (bounty & security research; axes depth + coverage). Lane base
`3266c9937b03062d9bbc2f436e20820115ed179c`; claims-freeze commit
`617496b9c6e92bc671e7e78b83df69a04470d0e9`; wave-1 spec/dispatch commit
`da2d3c687f82a9814ee71c91c930cb733050d37c`; final lane commit `<LANE_HASH>`.

## Work performed

The round declares **two claims**, frozen before dispatch in `.ufo/waves/round-35/claims.json`
(sha256 `fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982`, `frozen_at_utc`
`2026-10-26T07:30:00Z`):

- **C1 — depth:verifiability (score 4, held):** the seven round-34 verifier-routed defects D1–D7
  land with runnable closure checks: `corpus/instruments/r35-defect-closure.sh` prints
  `closed=7/7 exit=0` and `--selftest` prints `cases=7 failures=0`; SCORECARD.md `filled by the L1`
  count 0 with an appended correction naming `c1c6a5f`; an appended round-34 depth:density-row
  erratum naming the corrected mean 201.2; SKILL.md Gates & probes registry registers
  `r-defect-closure.sh` + `kill-rule-check.py`; `wave1-results.json` tracked with a provenance note
  beside it; `claims-erratum-d5.md` carries the discriminating-invocation and per-id occurrences
  statements; `L1Integration.md` stale dead-seat sentence corrected; QUALITY supersedes-R22/R23 rows
  present.
- **C2 — coverage (score 7, held):** Frontier F18 admitted 17 → 18 (CISA Known Exploited
  Vulnerabilities catalog — exploitation-status-based prioritization distinct from CVSS severity;
  row S052, registry 51 → 52, opened 2026-10-26), one knowledge entry citing `source: S052`, harness
  `entries=21 pass=21 exit=0` incl. `PASS F18 ids=S052`, source-recheck S052 exit 0, census exit 0
  (W04 S028/S029 only).

**Claim status at draft time (so no frozen after-value reads as achieved):** C2's counters are all
true on the worktree. Of C1's seven limbs, four are closed and measured (D1, D2, D3, D5); three are
**not** — D4 `tracked=0` (the L1's commit), D6 `dead-seat-sentence=1, correction-round-35=0`, D7
`supersedes-R22=0, supersedes-R23=0` — and the suite's own draft-time reading is
`closed=4/7 exit=1`, `--selftest cases=7 failures=3`. Both frozen literals (`closed=7/7`,
`cases=7 failures=0`) are reachable only after those three land (the suite prints them on its
all-fixed tree today, `ExecClosureSuite.md` §5/§7).

**Wave.** One v2 wave `kasegi-r35-build`, 64 seats, `spawn 64 / resume 0`, dispatched through the
inline spawn handoff (`wave1.ready` → `wave1.ready.dispatched`; spec `.ufo/waves/round-35/wave1-spec.json`,
dispatch `wave1-dispatch.json`, both in commit `da2d3c68`): executor 18, scribe 12, reviewer 10, scout
6, mutation-tester 5, critic 5, connector 4, sentinel 2, simplifier 2 — attack share 22/64 = 34.4%.
Receipts under `.ufo/waves/round-35/wave1/`.

**Before-controls at the freeze** (`git archive 617496b9`; digests pinned in
`ExecBeforeReceipts.md` §2): `c1-controls/before.txt` `352d3da2…`, `c2-controls/before.txt`
`2835700332…`, `census-before.txt` `74fc6a26…`. `ExecBeforeReceipts` replays all 18 stored C1/C2
values plus the census on the freeze export and reports **every one MATCH** (§3–§5), so the "before"
halves below are grounded on committed bytes alone. The same seat records three
reproduction findings (§7 items 2–4): D2's stale figure occurs twice in `SCORECARD.md` (the round-34
row at `:1145` and the *legitimate* round-33 after-value at `:1003`), so a global `201.7 == 0` check
would be unsatisfiable; D1 has **two** placeholder spellings and the frozen `filled by the L1` count
sees only one (`SCORECARD.md:1129` read `the L1 fills this line in the closing commit`); and the
before-controls had no committed runner.

**Do-nothing controls (untracked at draft time):** `c1-controls/fake-suite.sh` (sha256
`292aaac048c9cacff081c24b54fd71fc67a86d3c6ab6845398e0e2856c5be121`; prints `closed=7/7 exit=0` and
`cases=7 failures=0` while checking nothing) and `c2-controls/junk-f18.md` (sha256
`0abec3591e4a2dc5195b23b1c2c920f66052327b7f971aa578af76c3459dc176`; F18-shaped, fabricated quotes,
no manifest record). Both sit in the wave directory but are **not in the freeze commit** —
`git ls-tree -r --name-only 617496b9 -- .ufo/waves/round-35/` lists only `claims.json`,
`c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt`, and `git status --porcelain`
still shows both as `??`. The L1's commit is what makes them durable; the draft does not call them
committed (`ScribeMistakesDraft.md` M35-9).

**Work items by area** (evidence in `.ufo/waves/round-35/wave1/`):

- **C1 build** — `ExecClosureSuite` wrote `corpus/instruments/r35-defect-closure.sh` (773 lines at the author's receipt, sha256 `d7ad8438…`; **834 lines / 35391 B / sha256
  `0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f` at this draft's read** — the
  file moved 773 → 832 → 834 lines during the wave, so the L1 must pin the final digest; one `check_d1`…`check_d7`
  per defect, every check `cd`-prefixed and honouring `--root`); `ExecSelftestFixtures` built
  `corpus/instruments/r35-fixtures/` (63 files: `D1/`…`D7/`, `clean/`, `two-defect/D1D2/`, plus
  `README.md` + `fixtures.json` sha256 `b9a07afa…`). D1 `ExecD1Markers`, D2 `ExecD2DensityRow`,
  D3 `ExecD3SkillRegistry`, D4 `ExecD4ResultsTrack` (note `e1c44301…`), D5 `ScribeErratumD5`, D6/D7
  drafts `ScribeIntegrationNotes` / `ScribeQualityDraft`.
- **C1 attack/review** — `RevClosureSuite` (base `closed=0/7`, live `closed=4/7`, all-fixed
  `closed=7/7`, selftest `cases=7 failures=0` on the all-fixed tree with `clean` 7/7 and
  `two-defect` exact D1,D2 controls, forged summaries rejected 4/4); `RevSelftestFixtures` (63-file
  set, per-fixture clause isolation, no vacuous fixture); `RevD1D2`, `RevD3D4`, `RevD5D6D7`;
  `MutFixturesLimbs`; `CritC1Kill` (16 clause mutants, eight attack trees, gaps F-1…F-5 recorded);
  `ExecBeforeReceipts`, `ExecNoHarmFinal`.
- **C2 build** — `ExecC2Capture` (feed capture + manifest), `ScribeEntryF18` (entry),
  `ScribeSOURCESRow` + `ExecRegistryAppend` (registry row, search-log bullet, R8 lines),
  `ExecExpectedListSync` (expected list 47), `ExecCensusAfter`, `ExecScoreGap`.
- **C2 attack/review** — `ScoutKEVLive` (live re-open, 0 differing lines; BOD 22-01 revocation
  finding), `ScoutSiblingSweep` (20/20 siblings zero hits), `RevEntryF18`, `RevRowS052`,
  `RevC1BeforeAfter`/`RevC2BeforeAfter`, `MutC2Entry`, `MutJunkTwin`, `MutCounterBase`, `CritC2Kill`,
  `CritOverclaim`.
- **Non-claim frontier items** — assimilation: `ExecIdCollisions` (guard proven on an indented row;
  `collisions=21`), `ExecQuarantineSlice` + `ScoutQuarantine` (7 register rows re-derived, verdicts in
  `assimilation/quarantine-verdicts.md` sha256 `b0869369…`), `ScoutPackageThemes`,
  `ScribeGateAssimilation`; considerthese proposal 2 mined by `ExecScoreGap` → QUALITY draft
  `ScribeQualityDraft`; mistakes drafted by `ScribeMistakesDraft`.
- **Scope/credential sentinels and simplifiers** — `SentCred`, `SentScopeFinal`, `CritBoundary`,
  `SimplifierCleanup`, `SimplifierDocs` (verdicts summarised under § Boundary and open items).
- **L1 integration** — re-runs the frozen counters on the integrated bytes, lands D4's commit, D6 and
  D7, appends the lesson/SCORECARD/SHONEN/LOG, and commits `<LANE_HASH>`.

## Landed changes

Every landing is tied to the round-35 `LOG.md` entry (commit `<LOG_COMMIT>`; draft text in
`.ufo/waves/round-35/wave1/ScribeIntegrationNotes.md` Draft A) and these commits:

| Change | Commit |
|---|---|
| Claims freeze (`claims.json`, `census-before.txt`, `c1-controls/`, `c2-controls/`) | `617496b9` |
| Wave spec/dispatch (`build-spec.py`, `wave1-spec.json`, `wave1-dispatch.json`, `wave1.ready`) | `da2d3c68` |
| C1 counter: `corpus/instruments/r35-defect-closure.sh` + `corpus/instruments/r35-fixtures/` | `<LANE_HASH>` |
| D1/D2: `SCORECARD.md` placeholder substitution + appended round-34 depth:density erratum | `<LANE_HASH>` |
| D3: `SKILL.md` "Round-35 Gates & probes registry addition" (13/0 lines) | `<LANE_HASH>` |
| D4: `.ufo/waves/round-34/wave1-results.json` + `.provenance.md` (new files) | `<LANE_HASH>` |
| D5: `.ufo/waves/round-35/claims-erratum-d5.md` | `<LANE_HASH>` |
| D6/D7: `wave1/L1Integration.md` correction note; `corpus/QUALITY.md` Round-35 supersession block | `<LANE_HASH>` |
| C2: `corpus/knowledge/cisa-kev-catalog.md`, `corpus/SOURCES.md` S052 row + search-log bullet + R8 lines, `corpus/README.md` F18 row, `corpus/source-snapshots/round-35/{S052.txt,manifest.json}`, `corpus/instruments/knowledge-expected.txt` | `<LANE_HASH>` |
| Round close: SCORECARD round-35 section, `SHONEN.md`, `corpus/lessons/round-35.md`, `LOG.md` entry | `<LANE_HASH>` |

## Before → after measurements

All values read from the lane worktree at the named receipt; the draft-time read of the closure suite
is at 2026-10-26T06:52Z, before the L1's D4/D6/D7 landings.

### C1 — `depth:verifiability`, seven defects

| defect | before (freeze, `c1-controls/before.txt`) | after (landed bytes) | closure check / receipt |
|---|---|---|---|
| D1 placeholder | `filled by the L1` = 1 (`:1240`), `c1c6a5f` citations = 0; sibling spelling `the L1 fills this line` also = 1 (`:1129`) | `filled by the L1` = **0**, `c1c6a5f` = **3**, both slots now carry `c1c6a5f826d2425446347173de527c42991b78b0`; `<LANE_HASH>` = 0 | suite `D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0`; `ExecD1Markers.md` |
| D2 stale density row | `201.7` = 2 (round-33 after-value `:1003` + stale round-34 row `:1145`), `201.2` = 0 | appended erratum names the corrected mean **201.2** (two `201.2` lines) with the stale row's bytes untouched (`row-bytes=1`) | suite `D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0`; `ExecD2DensityRow.md` |
| D3 gates unregistered | `grep -c 'r-defect-closure'` = 0, `'kill-rule-check'` = 0 | 4 and 4 (an appended `## Round-35 Gates & probes registry addition`, `SKILL.md:1093-1104`, 13/0 numstat); transient `BASE-ABSENT=1` from a bare `S050.txt:70` citation fixed to a lane-relative path, `anchorcheck.py` exit 0 | suite `D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0`; `ExecD3SkillRegistry.md`, `ExecNoHarmFinal.md` §1 |
| D4 results after `complete` | tracked = 0, provenance note = 0 | results file present with note beside it (312874 B, sha256 `3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4`; note 5639 B `e1c44301…`); **`tracked` becomes 1 only at the L1's commit** | suite `D4 check=tracked=0,provenance=1 open=1` at draft time (expected `tracked=1 … open=0` after `<LANE_HASH>`); `ExecD4ResultsTrack.md` |
| D5 predicate wording | `claims-erratum-d5.md` absent | erratum landed; `discriminating invocation` ×5, `per-id occurrences` ×5, both clauses exercised as runnable invocations (twin sentence pinned in a manifest → `MISMATCH reason=quote-not-found`, exit ≠ 0; present-quote control exit 0) | suite `D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0`; `ScribeErratumD5.md`, `RevD5D6D7.md` §1 |
| D6 stale dead-seat sentence | `did not file a receipt (dead seat` = 1 (`L1Integration.md:30`) | **not landed at draft time**: `dead-seat-sentence=1, correction-round-35=0`. Premise verified: `ExecRegressionC1.md` *is* committed at `617496b` and `c1c6a5f` (`RevD5D6D7.md` §D6 premise) | suite `D6 … open=1` → expected `=0`, `correction-round-35>=1`; L1 applies; `RevD5D6D7.md` §2 |
| D7 QUALITY grounding | `supersedes R22` = 0, `supersedes R23` = 0 | **not landed at draft time** (block drafted at `ScribeQualityDraft.md` §1, 21 lines / 2842 B, sha256 `e3aa99a1…`; measured `supersedes-R22=1, supersedes-R23=1, open=0` on a copy carrying it) | suite `D7 … open=1` → expected `1,1 open=0`; L1 applies; `ScribeQualityDraft.md`, `RevD5D6D7.md` §3 |

**Suite readings** (`bash corpus/instruments/r35-defect-closure.sh`):

```
base export (git archive 3266c993):      closed=0/7 exit=1     # every defect still open
live worktree at draft time (06:52Z):    closed=4/7 exit=1     # D4/D6/D7 open, L1 landings pending
all-fixed tree (ExecClosureSuite §5):    closed=7/7 exit=0     # the predicate's passing direction
```

`bash corpus/instruments/r35-defect-closure.sh --selftest` at draft time prints
`selftest cases=7 failures=3 control-failures=0` — the three failures are D4/D6/D7, each
`verdict=unexpected` only because that fix is still open in the live bytes the case is built against
(`selftest detail=D7 live-reason=supersedes-R22=0,supersedes-R23=0`); the same run prints
`selftest control=clean closed=7/7 verdict=pass`, `selftest control=two-defect closed=5/7
failed=D1,D2 verdict=pass`, and four forged-report judges `rejected=1` (incl.
`judge=fake-suite … path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0`).
On the all-fixed tree the same command prints `selftest cases=7 failures=0`, exit 0
(`ExecClosureSuite.md` §7). **The frozen literal `cases=7 failures=0` is therefore reachable only
after the L1 lands D4/D6/D7; the draft records the ordered dependency rather than the final string.**

**Other C1 counters at draft time:** `python3 corpus/instruments/recheck-audit.py` →
`lines=47 total=47 pass=47 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0` and
`expect=present expected=47 missing=0 unexpected=0 exit=0`; `python3 corpus/instruments/anchorcheck.py
SKILL.md` → `16 in-range cite instances, 0 bad`, `LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0
OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 0 (`ExecNoHarmFinal.md` §1–§2). No-harm: `SKILL.md` 13/0,
`corpus/README.md` 28/0, `corpus/SOURCES.md` 5/0, `PROVINCE.md`/`corpus/QUALITY.md`/`LOG.md` 0
changed lines at the no-harm seat's read; `SCORECARD.md` carries 15 deletions, all in the
round-34 D1 region the placeholder substitution replaces (`ExecNoHarmFinal.md` §3).

### C2 — `coverage`, F18 / S052

| counter (frozen command) | before | after |
|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 17 | **18** (`F18` row at `corpus/README.md:388`) |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 51 | **52** (`S052` at `corpus/SOURCES.md:58`; `rows=52 malformed=0`) |
| `grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md` | 0 | **1** |
| `grep -lE '^source: S052 ' corpus/knowledge/*.md \| wc -l` | 0 | **1** (`corpus/knowledge/cisa-kev-catalog.md`) |
| `python3 corpus/instruments/frontier-recheck-count.py` | `entries=20 pass=20 exit=0` | **`entries=21 pass=21 exit=0`** incl. `PASS F18 knowledge/cisa-kev-catalog.md ids=S052 exit=0` |
| `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052` | `manifest UNAVAILABLE reason=missing`, exit 2 | **all five assertions `occurrences=1`, `sha256 OK`, exit 0** (Q1 anchor 2, Q2 3, Q3 4, Q4 15472, Q5 19165) |
| census (`scripts/sources-census.sh validate --root … kasegi`) | exit 0, W04 S028/S029 only | exit 0, W04 S028/S029 only |
| `corpus/knowledge/*.md` | 46 | **47** |

Capture: `corpus/source-snapshots/round-35/S052.txt` — status 200, 1479694 bytes, 27870 lines, sha256
`d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`, `fetched_utc
2026-10-26T06:32:40Z`, no redirect (request URL = final URL
`https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`); manifest
`06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee` (5631 B, record `url` +
`fetched_utc`). Two fetches 40 s apart were byte-identical. Parsed shape: `count=1756` =
`len(vulnerabilities)`, `catalogVersion 2026.10.23`, 12 per-record keys, `cvss` 0 occurrences
(`ExecC2Capture.md` §2–§4). Live re-open by `ScoutKEVLive`: **0 differing lines**, same sha256;
`Q1..Q5` each `grep -cF` = 1.

**F18/S052 basis, and the one reviewer verdict plus its repair.** The entry
(`corpus/knowledge/cisa-kev-catalog.md`) states the catalog as exploitation-status membership with a
per-record remediation clock, and explicitly distinguishes it from severity and from bounty ladders.
While the wave ran, `ScoutKEVLive` measured that **BOD 22-01 is revoked and superseded by BOD 26-04**
("BOD 22-01: Reducing the Significant Risk of Known Exploited Vulnerabilities (Revoked)" ×1 in the
scratch snapshot), and that 340 records still cite 22-01 in `requiredAction` while 139 cite 26-04
(`both=0 neither=1277`). The reviewer's verdict on the intermediate bytes
(`e3f233c0…`, 118 lines) is reported verbatim: **"REFUSE — one criterion: Q2, for Claim 4b only"**,
because Claim 4b asserted directive force from a page with no registry row and no capture
(`RevEntryF18.md` §1–§2; every other criterion PASS). The author then applied the reviewer's repair
path 2: on the **final** bytes (`e9de994dbe1940adb894420d566386500e4e29d69d8e6a5244ff2172c71d9761`,
91 lines) Claim 4b is demoted to a Scope note — "Directive status: a live-page note, not an admitted
claim (Q2)" (`:89`) — and Claim 4's tail now states what S052's bytes alone support (340 rows name
BOD 22-01, 139 name BOD 26-04). **A Q2 re-check on the final bytes is the L1's integration
obligation**: the flagged claim no longer exists as a claim, but no reviewer receipt yet covers
`e9de994d…`.

**Junk twin, by invocation.** The frozen after-text "junk twin rejected: source-recheck exit != 0"
holds only under a discriminating invocation, and the wave measured the difference:

- the twin's **own** `recheck:` line selects the real S052 record from the real manifest and **exits
  0** — it is not discriminating (`CritC2Kill.md` G4; this is the D5 class restated by execution);
- pinning the twin's two fabricated sentences in a scratch manifest against a byte-copy of the
  committed capture prints `S052:J1 MISMATCH reason=quote-not-found`, `S052:J2 MISMATCH
  reason=quote-not-found`, **exit 1** (`RevC2BeforeAfter.md` §3; a first attempt with record id
  `S052JUNK` failed closed earlier with `manifest MISMATCH reason=stem-mismatch`, the instrument's B1
  stem rule);
- the twin is nowhere admitted: `grep -c 'junk-f18' corpus/README.md` → 0, and the harness counts 21
  entries, not 22.

## Sources & frontier

`corpus/SOURCES.md` before → after: **51 → 52 rows**. Rows added by tier: **1 × A** (`S052` — CISA
Known Exploited Vulnerabilities catalog JSON feed,
`https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`, kind
`dataset`, tier A scoped to CISA's own catalog statements, status `mined`, opened `2026-10-26`,
recheck `90d`, used-by `corpus/knowledge/cisa-kev-catalog.md`, anchor pinned to the round-35 capture
with line locators). Tier histogram after: **A 49 / B 1 / C 2** (`ExecRegistryAppend.md`, census
output), i.e. before was A 48 / B 1 / C 2. Rows touched old→new: **none** — no status, recheck or
used-by cell changed on any pre-existing row, `S001–S051` untouched (`corpus/SOURCES.md:109`), and
`S052`'s own cells are authored once and not edited after append (`:110`). Registry contract:
`rows=52 malformed=0`, duplicate ids empty, enum/tier-inflation empty, missing used-by empty.

Frontier rows advanced: **F17 → F18** (`corpus/README.md:388`), with the admission subject
"CISA Known Exploited Vulnerabilities catalog — exploitation-status-based prioritization distinct
from CVSS severity" and `S052` as ids. Search log: one round-35 bullet at `corpus/SOURCES.md:79`
(question, where, date, identified/screened/included/excluded, stop rationale), plus a scope
correction at `:112` recording that the bullet's zero-hit counts are scoped to `corpus/knowledge/*.md`,
`corpus/README.md`, `corpus/SOURCES.md` and `SKILL.md`, and that the `KEV` token pre-existed in
`corpus/lessons/round-22.md:91`. A third R8 line (`:111`) records that the landed bullet
(sha256 `f2ab0a64…`) is superseded by the wider draft in `ScribeSearchLog.md` §5 (4495 B, sha256
`dc1a549a…`), which additionally captures the catalog page (`Showing 1 to 20 of 1756 results`),
reconciles the CSV distribution record for record (1756 `cveID`s identical as a multiset; the CSV's
12 columns are exactly the feed's 12 record fields), captures the JSON schema, and opens both
governing directives.

Census before → after: both exit 0, both carrying only the two standing W04 warnings
(`S028` docs.hackerone.com duplicate URL, `S029` EUR-Lex duplicate URL) — `census-before.txt`,
`ExecCensusAfter.md`.

Sourced claim: C2 rests on `S052` opened this round (capture + manifest + row + entry all landed this
round, source-recheck exit 0 on committed bytes; live re-open 0 differing lines). Sibling sweep and
ruling: 20 siblings scanned (21 `*-shokunin` dirs minus kasegi), 19 zero-hit; the only ground-token
hits are two `kake-shokunin` lines that record the screening-out of the **CISA BOD 20-01** template
(a directive about *publishing a VDP*, not exploitation-status prioritization) plus adjacent-theme
hits in `kagi` (an NVD page used as a quote source, explicitly not registered), `mori` (a raw evidence
blob), and "in the wild" in a mutation-testing sense elsewhere — every one ruled **no contested
scope**, and `shokuknow/doctrine/channel-recurrence.md:62` (`| cisa.gov | kasegi |`) ratifies the
assignment rather than contesting it (`ScoutSiblingSweep.md`, `ConnSibling.md`,
`ConnSibling-ruling-draft.md`). No report-to-lane item arises this round.

Assimilation: **none adopted.** `ExecIdCollisions` (0–3-space pattern) prints `reg-ids=51`,
`staged-ids=94`, `collisions=21` (`S031..S051`), and proves the guard once: an indented `S031` row is
caught (1) under the wide pattern and missed (0) under a column-0-only pattern; negative control
(non-colliding fixture) 0; absent registry exit 2. Disclosed limits: a 4-space or tab indent is not
caught (`ExecIdCollisions.md` §2), and adoption is by document, never by number. Quarantine slice:
7 register rows re-derived, S-id on every line, verdicts `present-and-located 4` (S065, S068, S069,
S070) · `prose-class-unverifiable 2` (S037, S054) · `unreachable 1` (S048) · `absent 0` ·
**adopted 0** (`ExecQuarantineSlice.md` §R4–§R7; `assimilation/quarantine-verdicts.md` sha256
`b0869369…`). Two verdict corrections are recorded rather than adopted: S068's located sentence is
already lane row **S040** (`corpus/SOURCES.md:46`), and S069/S070 locate only under a TLS-bypass or
plain-http invocation, so under a strict-verify rule they stay `unreachable`-by-policy. Standing
package refusals re-confirmed with flip conditions unmet (`ScribeGateAssimilation.md` §3).

## Trend verdicts

- **expansion: `improved`** — one admitted knowledge entry on ground the coverage map did not hold
  (exploitation-status prioritization, as opposed to the severity scales S001/S002/S046/S047 and the
  platform ladders S043/S044/S049/S050/S051), frontier 17 → 18, registry 51 → 52 with the only added
  row at tier A, entry citing the mined row `source: S052`, harness 21/21. No new capability row:
  the round added a closure suite and a capture, not new repertoire; the capability window is
  therefore not restarted.
- **quality: `improved`** — five of the seven routed defects are closed and measured (D1, D2, D3, D5
  closed; D4's record is digest-verifiable but its `tracked` clause is the L1's commit; D6/D7 are
  drafted and measured on copies, not landed), and the closure counter is real: base `closed=0/7`,
  all-fixed `closed=7/7`, `--selftest` 7 cases with `clean`/`two-defect` controls and four forged
  reports rejected; `recheck-audit.py` `strict pass=47/47` with `expect=present expected=47 missing=0
  unexpected=0 exit=0`; `anchorcheck.py` 0 bad, `BASE-ABSENT=0`; no admitted entry failed its own
  re-check (S052 re-opened live, byte-identical). **Bound the word "improved": the frozen C1 literal
  `closed=7/7` / `cases=7 failures=0` is not yet true on the tree** — draft time reads `closed=4/7`
  and `cases=7 failures=3`, which is the correct fail-closed behaviour for the three unlanded fixes.
- **discernment: `improved`** — the assimilation gate adopted nothing from seven quarantine rows while
  producing four located anchors and two description-class refusals (a refusing gate, not an idle one);
  S068 was identified as a duplicate of an existing row rather than a new admission; S069/S070 got a
  policy-scoped verdict instead of a coin-flip; the junk F18 twin is rejected by the counter it was
  built to fool; and the round reports the score distance instead of a move: `score-gap.py` prints
  `gap: 24 of 47 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`
  against the recorded threshold (`SCORECARD.md:331`), i.e. the round improved the verifiability
  instruments while the score-5 conjunct (0 gated chains, 0 unsupported current claims) is unchanged.
  Recorded cost: `CritC1Kill` shows the suite's clauses are file-wide literal greps, so a negation or
  a mention satisfies D2/D3/D7 (gaps F-2…F-5) and nothing pins the counter's own bytes (F-1); the
  round records these as findings, not as closures.

## SHONEN

_(Pointer lines refreshed from `SHONEN.md`; the line numbers below are the round-34 grid positions
and the L1 should re-read them after `ScribeShonen` rewrites the boxes.)_

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources —
  `SHONEN.md:5`; this round appends two registry rows (`SKILL.md:1097` `r-defect-closure.sh`,
  `:1098` `kill-rule-check.py`, under the heading at `:1093`) and no decision table; `anchorcheck.py` 0 bad and `density.py` mean moves 201.2 → 220.9 because the append is a new
  high-density registry block (disclosed in `ExecNoHarmFinal.md` §1), not a score move. Box stays
  `[~]`.
- [~] At least one end-to-end domain task executed and logged in LOG.md — `SHONEN.md:21`; **no new
  end-to-end domain hunt ran this round.** The closest executed measurements are the KEV capture +
  `source-recheck` (a measurement, not a hunt) and the closure suite's base/fixed-tree runs. Box stays
  `[~]`.
- [~] Instructions executable by an agent without oral context — `SHONEN.md:34`; `recheck-audit.py`
  `strict pass=47/47`, `expect=present expected=47 missing=0 unexpected=0 exit=0`; the F18 entry's own
  `recheck:` line runs unmodified (`sha256 OK`, five assertions, exit 0) and fails closed on a moved
  quote (exit 1) or an absent manifest (exit 2). Box stays `[~]` on the capability-row limb.
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `SHONEN.md:54`; `PROVINCE.md` has **0**
  changed lines at draft time, F18 sits inside the province's "program rules, claim packages" core
  (the F13/F14/F17 severity-ladder precedent), and the 20-sibling sweep finds no contested scope. The
  appended F17/F18 frontier amendment inside `PROVINCE.md` is the L1's call and, if landed, is a
  frontier-list append. Box stays `[~]`.

## Boundary and open items

- **The three unlanded limbs are ordered, not optional.** D4 (`tracked=1`) needs the commit; D6 needs
  an appended correction in `.ufo/waves/round-34/wave1/L1Integration.md` (the note must paraphrase,
  not quote, `did not file a receipt (dead seat` — the suite's own `D6:+dead-seat-sentence` mutant
  proves a file carrying both reads open, `RevD5D6D7.md` §F2); D7 needs the `ScribeQualityDraft` §1
  block appended verbatim. After all three, re-run the suite and expect `closed=7/7 exit=0` and
  `--selftest cases=7 failures=0`.
- **D6 had no seat owner in the wave spec** (`ScribeIntegrationNotes.md` §F7); it is an L1-applied
  correction, so the integration receipt must name who landed it.
- **Suite identity (critic finding F-1).** The frozen kill rule is discharged by the suite on itself;
  nothing pins the suite's bytes. Smallest fix: record
  `sha256sum corpus/instruments/r35-defect-closure.sh` after the last edit (draft-time read
  `0ae4b484…`, 35391 B, 834 lines; the author's receipt pinned `d7ad8438…`, 32148 B, 773 lines — the
  discrepancy is itself the reason the pin must be taken at quiescence) and
  read the plain run only beside a passing `sha256sum -c`. F-2…F-5 (file-wide literal clauses:
  negation satisfies D7, a mention satisfies D2/D3, `{}` satisfies D4's tracked limb) are recorded
  with one-command corrections each (`CritC1Kill.md` §5).
- **D2's closure literal is row-scoped by necessity** (two `201.7` hits at freeze); the suite
  therefore implements "row bytes untouched" as a fixed-string survival match
  (`^| depth:density | 9 | mean \*\*201\.7\*\*, 25 blocks, 710 path-citation instances`), not a diff
  count, because neither a `git archive` export nor a fixture carries the round-34 base
  (`ExecClosureSuite.md` §2).
- **Score distance, measured not claimed.** 24 of 47 rechecks remain gated on a lost base; 23 gate on
  `~/Projects/bounties` (absent since 2026-09-28) and/or `~/Projects/the-bounty-hunter` (2026-10-12),
  one on the mirror cite in `citation-bases.md`; `anchorcheck.py` still reports one PAST-EOF instance
  outside this round's scope (`corpus/QUALITY.md:77` → bare `README.md:159`). The round adds no
  score move; depth:verifiability stays at 4 and the lowest-axis obligation stays active.
- **Entry-provenance boundary.** `ScribeEntryF18`/the entry's own §Limits: Claim 4b (BOD 26-04) is a
  live-page read with no registry row and no committed capture this round; the two quoted strings that
  cannot be exactly-once (the FCEB deadline sentence, 2 occurrences; the BOD 22-01 sentence, 327
  occurrences) are anchored and counted in the entry rather than asserted in the manifest.
- **Quarantine slice limits.** S037's verdict depends on the fetching UA (content rotation) and S069/
  S070 on TLS policy; the verdicts file records both facts so the choice is explicit, and nothing was
  adopted either way.
- **C2 residual gaps (critic, measured).** `CritC2Kill` falsifies the *verifiability* half while leaving
  the artifact claim intact: the landed capture is byte-identical to a live fetch made by that seat
  (1,807,090 served bytes → 1,479,694 normalized → same sha256, `IDENTICAL`) and the entry's own
  `FC-1/FC-3/FC-6/FC-9/FC-10` re-compute true, but the recorded gaps are G1 (no instrument reads an
  entry's assertions — `anchorcheck.py` reports 0 anchors on the F18 entry), G2 (captures are bound by
  name and URL string, not content: a renamed error page with a self-consistent manifest passes), G3
  (no `mined ⇒ capture` rule), G4 (the committed twin's own line exits 0, so that clause is not
  reproducible as built), G5 (`PASS F18 ids=S052` means binding + recheck exit, not that the entry's
  claims were checked), G6 (shape counters are text shapes). Each has a one-command correction in
  `CritC2Kill.md` §Smallest safe correction; none was applied this round.
- **Source chain, cross-checked.** `ConnCrossCheck` walks registry row ↔ capture ↔ manifest record ↔
  entry header ↔ harness ↔ source-recheck ids and URL/sha256 for S052 and reports **no dangling link**
  (six links agree; the registry row's round-35 capture path exists). `RevC2BeforeAfter` independently
  reproduces the before state 7/7 and the after state 8/8 at the tip.
- **D3 registers the round-34 instruments, not this round's counter.** The two registry rows name
  `r-defect-closure.sh` (nine checks R1–R9) and `kill-rule-check.py`; the round-35 closure counter is
  `r35-defect-closure.sh` and is **not** registered (`CritMistakes.md` F2, M35-2 candidate). The D3
  fix satisfies the frozen literal (the two named files are registered) but the widening it implies is
  open.
- **D1's closure clause does not test the spelling that actually failed.** `check_d1` carries three
  literals (`filled by the L1`, `<LANE_HASH>`, `correction-c1c6a5f`) and no prose clause, while the
  occurrence the round had to repair was `the L1 fills this line` at `SCORECARD.md:1129`
  (`CritMistakes.md` F3, M35-3 candidate; one-line mutant fix proposed).
- **Fixture set.** `ExecSelftestFixtures` lands 65 files (54 `.md`, 77,361 B) with
  `clean/` and `two-defect/D1D2/` (the latter scores `closed=5/7` with exactly D1,D2 failing), and
  demonstrates `selftest cases=7 failures=0` on a materialized all-fixed lane copy with one line
  changed (`LANE_ROOT=<clean tree>`); on the live tree the same command reads 4/7 with all fixtures
  rejecting their own defect.
- **Reviewer posture on C1/C2** is reported verbatim in the receipts
  (`RevClosureSuite.md`, `RevSelftestFixtures.md`, `RevD1D2.md`, `RevD3D4.md`, `RevD5D6D7.md`,
  `RevEntryF18.md`, `RevRowS052.md`, `RevC1BeforeAfter.md`, `RevC2BeforeAfter.md`); the L1 should quote
  the final verdict lines rather than paraphrase them.
- **Dead seats and wave completeness.** `<from the wave registry / L1: names and counts>`. The
  dispatcher's own results file for round 35, if produced, lands before the L1's final commit (the
  D4 lesson) and is committed with a provenance note.
- **Tools installed: none.** No tool was installed or upgraded by this seat or, per the wave receipts
  read here, by any seat; no pacman transaction was attempted (host-wide pause respected).
- **Scratch.** `/fast/scratch/hyaku/kasegi-r35/ScribeReportDraft/` was never needed for this seat
  (every measurement was a read-only lane command); its absence is asserted in the receipt.

## Measurement state (draft-time digests)

Read at 2026-10-26T06:5xZ on the lane worktree, before the L1's D4/D6/D7 landings and before the
round-35 SCORECARD/lesson/SHONEN appends — so these digests will move and the L1 should re-digest:

`corpus/instruments/r35-defect-closure.sh` `0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f` (35391 B, 834 lines at this
read; the author's receipt pinned `d7ad8438…`, 32148 B, 773 lines) · `corpus/instruments/r35-fixtures/fixtures.json` `b9a07afa…` ·
`corpus/source-snapshots/round-35/S052.txt` `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`
(1479694 B) · `corpus/source-snapshots/round-35/manifest.json` `06bfcc71…` · `corpus/knowledge/cisa-kev-catalog.md` `e9de994dbe1940adb894420d566386500e4e29d69d8e6a5244ff2172c71d9761`
(91 lines; the reviewed intermediate was `e3f233c0…`, 118 lines) ·
`corpus/SOURCES.md` 52 rows / `corpus/README.md` 18 frontier rows · `SCORECARD.md` `51337bf1…` (at
`CritC1Kill`'s read) · `.ufo/waves/round-34/wave1-results.json` `3afa3581…` (312874 B) ·
`.ufo/waves/round-34/wave1-results.json.provenance.md` `e1c44301…` (5639 B) ·
`.ufo/waves/round-35/claims-erratum-d5.md` `0d304b92…` (at `CritC1Kill`'s read) ·
`corpus/QUALITY.md` `807cc714…` (at `CritC1Kill`'s read, i.e. before the D7 block).
