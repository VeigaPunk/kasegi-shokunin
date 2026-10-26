# kasegi round 35 — report draft

**Draft only.** Written by seat `ScribeReportDraft` (scribe, leaf of wave 1) from the round-35 wave
receipts; the L1 (`KasegiR35`) integrates it into `.ufo/reports/round-35/kasegi.md` and substitutes
`<LANE_HASH>` (the closing commit; the tree carried `48e6053` with three uncommitted entries when this draft's final pass ran). Nothing
here is written to the fleet repo. Every number below is either a receipt quote with its named
location or a read-only command this seat ran at the stated instant; where the worktree moved after
the last commit, the draft says so and gives both readings.

Lane: `kasegi-shokunin` (bounty & security research; axes depth + coverage). Lane base
`3266c9937b03062d9bbc2f436e20820115ed179c`; claims-freeze commit
`617496b9c6e92bc671e7e78b83df69a04470d0e9`; wave-1 spec/dispatch commit
`da2d3c687f82a9814ee71c91c930cb733050d37c`; integration commits `aa6ad99b…` and `0aee0ef…`;
closing lane commit `<LANE_HASH>`.

## Work performed

The round declares **two claims**, frozen before dispatch in `.ufo/waves/round-35/claims.json`
(sha256 `fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982`, `frozen_at_utc`
`2026-10-26T07:30:00Z`, attempt 1):

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

**Claim status on the landed bytes: both held, all seven C1 limbs closed.** Read at
2026-10-26T07:06Z on `48e6053`:
`bash corpus/instruments/r35-defect-closure.sh` → `D1..D7 … open=0`, `closed=7/7 exit=0`;
`--selftest` → `selftest cases=7 failures=0` with `control=clean closed=7/7 verdict=pass`,
`control=two-defect closed=5/7 failed=D1,D2 verdict=pass`; the base export
(`git archive 617496b9`, which carries no suite) → `closed=0/7 exit=1` with every D open
(`ExecDoNothingReject.md` §1b). The same seat's §1c records the five forged-report judges rejecting
(`forged-summary`, `forged-caselines`, `short-report`, `fake-suite`, `fake-plain`).

**Wave.** One v2 wave `kasegi-r35-build`, 64 seats, `spawn 64 / resume 0` (`wave1-dispatch.json`;
`counts {'spawn': 64, 'resume': 0, 'total': 64}`, policy `maxLanes 128`), dispatched through the
inline spawn handoff (`wave1.ready` → `wave1.ready.dispatched`; spec `.ufo/waves/round-35/wave1-spec.json`,
`build-spec.py`): executor 18, scribe 12, reviewer 10, scout 6, mutation-tester 5, critic 5,
connector 4, sentinel 2, simplifier 2. Attack share **20/64 = 31.2 %** on the lesson's definition
(reviewer + mutation-tester + critic; `corpus/lessons/round-35.md:3`) — if the two simplifier seats
are counted as attack the share is 22/64 = 34.4 %, and the report should say which definition it
uses. 63 seat receipts were on disk at this draft's final read (60 at the first count); `wave1-results.json` for round 35 was
still pending dispatcher finalize at the L1's close-out (`LOG.md:1658`).

**Before-controls at the freeze** (`git archive 617496b9`; digests pinned in `ExecBeforeReceipts.md`
§2): `c1-controls/before.txt` `352d3da2…`, `c2-controls/before.txt` `2835700332…`,
`census-before.txt` `74fc6a26…`. `ExecBeforeReceipts` replays all 18 stored C1/C2 values plus the
census on the freeze export and reports **every one MATCH** (§3–§5), so the "before" halves below are
grounded on committed bytes alone. Its three reproduction findings (§7 items 2–4): D2's stale figure
occurs twice in `SCORECARD.md` (the stale round-34 row at `:1145` and the *legitimate* round-33
after-value at `:1003`), so a global `201.7 == 0` check would be unsatisfiable; D1 has **two**
placeholder spellings and the frozen `filled by the L1` count sees only one
(`SCORECARD.md:1129` read `the L1 fills this line in the closing commit`); and the before-controls
have no committed runner (still true at close — `grep -rln 'before.txt' corpus/instruments/` is prose
only, `CritMistakes.md` F6).

**Do-nothing controls, added after the freeze.** `c1-controls/fake-suite.sh` (sha256
`292aaac048c9cacff081c24b54fd71fc67a86d3c6ab6845398e0e2856c5be121`; prints `closed=7/7 exit=0` and
`cases=7 failures=0` while checking nothing) and `c2-controls/junk-f18.md` (sha256
`0abec3591e4a2dc5195b23b1c2c920f66052327b7f971aa578af76c3459dc176`; F18-shaped, fabricated quotes,
no manifest record). Neither was in the freeze commit (`git ls-tree -r --name-only 617496b9 --
.ufo/waves/round-35/` lists exactly `claims.json`, the two `before.txt` files and
`census-before.txt`); both are tracked as of `5a25337`. `ExecDoNothingReject` is the seat that
authored them and demonstrates their rejection (fake suite rejected by the real suite's
`--selftest` discriminator; the twin rejected only on the quote-comparison invocation — see C2
below).

**Work items by area** (evidence in `.ufo/waves/round-35/wave1/`):

- **C1 build** — `ExecClosureSuite` wrote `corpus/instruments/r35-defect-closure.sh` (one
  `check_d1`…`check_d7`, every check `cd`-prefixed and honouring `--root`; 834 lines / 35391 B /
  sha256 `0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f` at the landed read; the
  author's receipt pinned `d7ad8438…`, 773 lines, and the suite moved through five digests while the
  reviewers iterated — `SCORECARD.md` § C1 blind spots); `ExecSelftestFixtures` built
  `corpus/instruments/r35-fixtures/` (65 files, 54 `.md`, 77 361 B: `D1/`…`D7/`, `clean/`,
  `two-defect/D1D2/`, `README.md`, `fixtures.json` `b9a07afa…`). D1 `ExecD1Markers`, D2
  `ExecD2DensityRow`, D3 `ExecD3SkillRegistry`, D4 `ExecD4ResultsTrack` (note `e1c44301…`), D5
  `ScribeErratumD5` (final `eee0bb57…`), D6/D7 applied by the L1 from `ScribeIntegrationNotes` /
  `ScribeQualityDraft`.
- **C1 attack/review** — `RevClosureSuite` (base `closed=0/7`; mid-wave `closed=4/7`; all-fixed
  `closed=7/7`; selftest 7/7 with `clean` and `two-defect` controls; forged summaries rejected);
  `RevSelftestFixtures` (per-fixture clause isolation, no vacuous fixture); `RevD1D2`, `RevD3D4`,
  `RevD5D6D7`; `MutClosureSuite` (**14/14 mutants killed** — 7 vacuous + 7 delete, one pair per
  check, both controls rejected); `MutFixturesLimbs`; `CritC1Kill` (16 clause mutants, eight attack
  trees, gaps F-1…F-5); `RevNoHarm`, `ExecNoHarmFinal`, `ExecBeforeReceipts`, `ExecDoNothingReject`,
  `ExecRegressionC1` (receipt not on disk at this read).
- **C2 build** — `ExecC2Capture` (feed capture + manifest), `ScribeEntryF18` (entry),
  `ScribeSOURCESRow` + `ExecRegistryAppend` (registry row, search-log bullet, R8 lines),
  `ScribeSearchLog`, `ExecExpectedListSync` (expected list 47), `ExecScoreGap`.
- **C2 attack/review** — `ScoutKEVLive` (live re-open 0 differing lines; BOD 22-01 revocation),
  `ScoutDatawalk`, `ScoutSiblingSweep`, `ScoutLeads`, `ScoutQuarantine`, `ScoutPackageThemes`,
  `RevEntryF18` (REFUSE → repair → **ADMIT**), `RevRowS052`, `RevC1BeforeAfter`, `RevC2BeforeAfter`,
  `MutC2Entry`, `MutJunkTwin`, `MutCounterBase`, `CritC2Kill`, `CritOverclaim`.
- **Non-claim frontier items** — assimilation: `ExecIdCollisions` (guard proven on an indented row;
  `reg_ids=52 staged_ids=94 collisions=22` post-C2), `ExecQuarantineSlice` + `ScoutQuarantine`
  (7 register rows re-derived; verdicts in `assimilation/quarantine-verdicts.md`), `ScoutPackageThemes`,
  `ScribeGateAssimilation`; considerthese proposal 2 mined by `ExecScoreGap` → QUALITY R26;
  mistakes minted by `ScribeMistakesDraft` and trimmed by the L1 into `corpus/lessons/round-35.md`
  M35-1…M35-5.
- **Scope/credential sentinels, connector, simplifiers** — `SentCred` (CLEAN, `blocking_findings: 0`),
  `CritBoundary`, `ConnClaims`, `ConnSibling` (+ ruling draft), `ConnCrossCheck`, `ConnTrends`,
  `SimplifierCleanup` (no dead/duplicate check, no unreachable branch), `SimplifierDocs`;
  `SentScopeFinal` receipt not on disk at this read.

## Landed changes

Every landing is tied to the round-35 `LOG.md` entry (`LOG.md:1651`, 1659 lines, commit
`<LOG_COMMIT>`) and these commits:

| Change | Commit |
|---|---|
| Claims freeze (`claims.json`, `census-before.txt`, `c1-controls/before.txt`, `c2-controls/before.txt`) | `617496b9` |
| Wave spec/dispatch (`build-spec.py`, `wave1-spec.json`, `wave1-dispatch.json`, `wave1.ready`) | `da2d3c68` |
| C1 D4/D6/D7 landings: `.ufo/waves/round-34/wave1-results.json` + `.provenance.md` tracked, `L1Integration.md` correction, `corpus/QUALITY.md` R26/R27 supersession block | `aa6ad99b` |
| Integration: `corpus/lessons/round-35.md`, SCORECARD stub, `SHONEN.md` block, `LOG.md` entry, wave receipts, assimilation artifacts, `claims-erratum-d5.md` | `0aee0ef` |
| D1 repair: the stub's closing-commit sentence reprinted the placeholder and re-armed D1 (`closed=6/7`); reworded in place | `8ce6fb4` |
| Wave leftovers: `S052.txt` (named >1 MiB), `SKILL.md` registry rows, control files, ready markers, receipts | `5a25337` |
| Receipt finalisation (`ExecDoNothingReject`, `ExecD1Markers`) | `bb2dc8c` |
| Late seat appends: full SCORECARD round-35 section, `SHONEN.md` round-35 block | `48e6053` |
| Closing commit: remaining worktree entries (`SHONEN.md`, `corpus/lessons/round-35.md`, `ScribeShonen.md`) | `<LANE_HASH>` |

*Disclosure of the D1 episode:* at `0aee0ef` the stub's sentence `**Final lane commit: filled by the
L1 in the closing commit.**` reproduced the placeholder token, so `D1 check=placeholders=1 … open=1`
→ `closed=6/7 exit=1` — the frozen kill rule was live-broken by the integration commit itself
(`SCORECARD.md` § "One C1 clause was broken and repaired inside this round"). `8ce6fb4` reworded it
(a one-line diff) and the suite reads 7/7 again. This is the third recurrence of the same class
(R1 round 33, D1 round 34, this round's own stub).

*Post-commit churn, recorded not repaired:* writes landed after each of the L1's commits. After
`5a25337`, `ExecD1Markers.md` (04:02:37) and `ExecDoNothingReject.md` (04:03:30) were rewritten and the
full `SCORECARD.md`/`SHONEN.md` sections were appended — absorbed by `bb2dc8c`/`48e6053`; after
`48e6053`, `SHONEN.md`, `corpus/lessons/round-35.md` (ScribeShonen's block and a lesson rewrite, 521
lines) and `wave1/ScribeShonen.md` were still uncommitted at this draft's final read. That is M35-1's
class in the round that files M35-1; the closing commit must absorb them and the report should name
the offset rather than describe the committed tree as final.

## Before → after measurements

Read on `48e6053` plus the worktree appends noted above (the earlier mid-wave reads on `da2d3c6`/`5a25337` are labelled as such). The closure suite's per-defect payloads are
from this seat's own run at 07:06Z and match `ExecDoNothingReject.md` §1a and the SCORECARD table.

### C1 — `depth:verifiability`, seven defects

| defect | before (freeze, `c1-controls/before.txt`) | after (landed bytes) | closure check / receipt |
|---|---|---|---|
| D1 placeholder | `filled by the L1` = 1 (`:1240`), `c1c6a5f` citations = 0; sibling spelling `the L1 fills this line` also = 1 (`:1129`) | `filled by the L1` = **0**, `c1c6a5f` = **3**, `<LANE_HASH>`-marker = 0; both slots carry `c1c6a5f826d2425446347173de527c42991b78b0` | suite `D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0`; `ExecD1Markers.md` |
| D2 stale density row | `201.7` = 2 (round-33 after-value `:1003` + stale round-34 row `:1145`), `201.2` = 0 | appended erratum names the corrected mean **201.2** with its two byte-bound limbs (`:1246` the erratum sentence, `:1248-1250` its measurement paragraph), and the round-35 guard row records both limbs (`:1314`); the stale row's bytes are untouched (`row-bytes=1`) and the round-33 after-value still reads 201.7 at `:1003` | suite `D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0`; `ExecD2DensityRow.md` |
| D3 gates unregistered | `grep -c 'r-defect-closure'` = 0, `'kill-rule-check'` = 0 | 4 / 4 (appended `## Round-35 Gates & probes registry addition`, `SKILL.md:1093`, rows at `:1097` `r-defect-closure.sh` and `:1098` `kill-rule-check.py`, `13/0` numstat) | suite `D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0`; `ExecD3SkillRegistry.md` |
| D4 results after `complete` | tracked = 0, provenance note = 0 | tracked = **1**, note = 1 (312874 B, sha256 `3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4`; note 5639 B `e1c44301…`) | suite `D4 check=tracked=1,provenance=1 open=0`; `ExecD4ResultsTrack.md` |
| D5 predicate wording | `claims-erratum-d5.md` absent | erratum landed (final `eee0bb579844ad9d02777fb4cd241e726d0bb0630679bc41aa534d7f5d0951e6`): `discriminating invocation` ×5, `per-id occurrences` ×5, both exercised as runnable invocations (twin sentence pinned in a manifest → `MISMATCH reason=quote-not-found`, exit ≠ 0; present-quote control exit 0) | suite `D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0`; `ScribeErratumD5.md`, `RevD5D6D7.md` §1 |
| D6 stale dead-seat sentence | `did not file a receipt (dead seat` = 1 (`L1Integration.md:30`) | 0 with `Correction (round 35)` = 1 (the correction paraphrases the literal, because the suite greps the whole file — `RevD5D6D7.md` F2) | suite `D6 check=dead-seat-sentence=0,correction-round-35=1 open=0` |
| D7 QUALITY grounding | `supersedes R22` = 0, `supersedes R23` = 0 | `R26` (score-distance reporting) carries `supersedes R22`; `R27` (reflection cadence) carries `supersedes R23`; `corpus/QUALITY.md` 250 lines, `d4f83bb1…` | suite `D7 check=supersedes-R22=1,supersedes-R23=1 open=0`; `ScribeQualityDraft.md`, `RevD5D6D7.md` §3 |

**Suite readings** (`bash corpus/instruments/r35-defect-closure.sh`):

```
base export (git archive 617496b9):   closed=0/7 exit=1     # every defect open; no suite in the export
mid-wave worktree (06:52Z):           closed=4/7 exit=1     # D4/D6/D7 still open, fail-closed
landed worktree (07:06Z):             closed=7/7 exit=0
all-fixed tree (ExecClosureSuite §5): closed=7/7 exit=0     # independent of the L1's landings
```

`--selftest` on the landed bytes: `selftest cases=7 failures=0`, `control=clean closed=7/7
verdict=pass`, `control=two-defect closed=5/7 failed=D1,D2 verdict=pass`, and
`judge={forged-summary,forged-caselines,short-report,fake-suite,fake-plain} rejected=1`.
`MutClosureSuite` reports 14/14 mutants killed (7 vacuous + 7 delete, one pair per check) with no
survivor; `RevSelftestFixtures` confirms each fixture re-opens exactly one defect and that a
two-defect fixture fails exactly two checks.

**Other C1 counters (read 07:06Z):** `python3 corpus/instruments/recheck-audit.py` →
`strict pass=47/47 cdroot_fail=0 instrument_fail=0 own_fail=0`, `lines=47 total=47 pass=47
fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`, `expect=present expected=47 missing=0
unexpected=0 exit=0`; `python3 corpus/instruments/anchorcheck.py SKILL.md` → `16 in-range cite
instances, 0 bad`, `LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 0;
`python3 corpus/instruments/density.py SKILL.md` → mean **220.9** over 26 blocks and 742 path-citation
instances, exit 0 (base `3266c99:SKILL.md` `ba5ebe5d…` remains 201.2 over 25 blocks / 711 cites —
the whole move is the one appended registry block, dens 712.5).

**No-harm / append-only:** `git diff --numstat 3266c99` → `SKILL.md 13/0`, `corpus/README.md 28/0`,
`corpus/SOURCES.md 7/0`, `corpus/QUALITY.md 21/0`, `PROVINCE.md` 0, `LOG.md` 0. Two files are
non-append-only and both are disclosed in SCORECARD: `SCORECARD.md` `33/15` (D1's assigned in-place
rewrite of the round-34 placeholder prose) and the round-34 `wave1/L1Integration.md` (3 deletions —
the D6 correction must be in place, because the suite's `dead-seat-sentence == 0` clause greps the
whole file).

### C2 — `coverage`, F18 / S052

| counter (frozen command) | before | after |
|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 17 | **18** (`F18` row at `corpus/README.md:388`) |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 51 | **52** (`S052` at `corpus/SOURCES.md:58`; `rows=52 malformed=0`) |
| `grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md` | 0 | **1** |
| `grep -lE '^source: S052 ' corpus/knowledge/*.md \| wc -l` | 0 | **1** (`corpus/knowledge/cisa-kev-catalog.md`) |
| `python3 corpus/instruments/frontier-recheck-count.py` | `entries=20 pass=20 exit=0` | **`entries=21 pass=21 exit=0`** incl. `PASS F18 knowledge/cisa-kev-catalog.md ids=S052 exit=0` |
| `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052` | `manifest UNAVAILABLE reason=missing`, exit 2 | **`sha256 OK`, Q1–Q5 each `occurrences=1`** (anchors 2, 3, 4, 15472, 19165; Q3–Q5 `normalized=markup-whitespace`), exit 0 |
| census (`scripts/sources-census.sh validate --root … kasegi`) | exit 0, W04 S028/S029 only | exit 0, W04 S028/S029 only |
| `corpus/knowledge/*.md` | 46 | **47** |

Capture: `corpus/source-snapshots/round-35/S052.txt` — status 200, 1479694 bytes, 27870 lines, sha256
`d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`, `fetched_utc
2026-10-26T06:32:40Z`, no redirect (request URL = final URL
`https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`); manifest
`06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee` (5631 B, record `url` +
`fetched_utc` + five assertions). Two fetches 40 s apart were byte-identical. Parsed shape:
`count=1756` = `len(vulnerabilities)`, `catalogVersion 2026.10.23`, 12 per-record keys, `cvss` 0
occurrences (`ExecC2Capture.md` §2–§4). Live re-open by `ScoutKEVLive`: **0 differing lines**, same
sha256; `Q1..Q5` each `grep -cF` = 1. `RevC2BeforeAfter` reproduces the before state 7/7 and the
after state 8/8; `ConnCrossCheck` walks the six-link chain (row ↔ capture ↔ manifest ↔ entry header ↔
harness ↔ source-recheck ids) with **no dangling link**.

**The entry's reviewer verdict is REFUSE → repair → ADMIT.** `RevEntryF18` first verdict on the
intermediate bytes `e3f233c0…` (118 lines): **"REFUSE — one criterion: Q2, for Claim 4b only"**,
because Claim 4b asserted directive force (BOD 26-04 current, BOD 22-01 revoked) from a page with no
registry row and no capture; every other criterion passed. The author took the reviewer's repair path
2: Claim 4b was deleted outright — a new tier-A row would have moved `SOURCES.md` 52 → 53 and broken
the frozen C2 literal — and on the **final** bytes
`e9de994dbe1940adb894420d566386500e4e29d69d8e6a5244ff2172c71d9761` (91 lines) the reviewer's final
verdict is **"ADMIT. Q1–Q10 all PASS"**, with two residual notes (the live-page directive-status
statement remains unregistered by design; the README frontier row was still 17 at that check). The
underlying live finding stands and is recorded: BOD 22-01 is revoked and superseded by BOD 26-04
(`ScoutKEVLive.md`; 340 records still name 22-01 in `requiredAction`, 139 name 26-04, `both=0
neither=1277`), and the entry now carries it as a labelled Scope note, not a claim.

**Junk twin, by invocation.** The frozen after-text "junk twin rejected: source-recheck exit != 0"
holds only under a discriminating invocation; the wave measured the difference:

- the twin's **own** `recheck:` line selects the real S052 record from the real manifest and **exits
  0** — it is not discriminating (`CritC2Kill.md` G4; the D5 class restated by execution);
- pinning the twin's two fabricated sentences in a scratch manifest against a byte-copy of the
  committed capture prints `S052:J1 MISMATCH reason=quote-not-found`, `S052:J2 MISMATCH
  reason=quote-not-found`, **exit 1** (`RevC2BeforeAfter.md` §3; a first attempt with record id
  `S052JUNK` failed closed with `manifest MISMATCH reason=stem-mismatch`, the instrument's B1 stem
  rule);
- the twin is nowhere admitted: `grep -c 'junk-f18' corpus/README.md` → 0, harness 21 entries, not 22.

## Sources & frontier

`corpus/SOURCES.md` before → after: **51 → 52 rows** (`corpus/SOURCES.md` `0f95a132…`, 112 lines).
Rows added by tier: **1 × A** (`S052` — CISA Known Exploited Vulnerabilities catalog JSON feed,
`https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`, kind
`dataset`, tier A scoped to CISA's own catalog statements, status `mined`, opened `2026-10-26`,
recheck `90d`, used-by `corpus/knowledge/cisa-kev-catalog.md`, anchor pinned to the round-35 capture
with line locators L2/L3/L4/L5/L7-L22 and spans L15472-L15475, L19165-L19168). Tier histogram after:
**A 49 / B 1 / C 2** (before A 48 / B 1 / C 2; `ExecRegistryAppend.md`). Rows touched old→new:
**none** — no status, recheck or used-by cell changed on any pre-existing row, `S001–S051` untouched
(`corpus/SOURCES.md:110`), and `S052`'s cells are authored once and not edited after append (`:109`).
Registry contract: `rows=52 malformed=0`, duplicate ids empty, enum/tier-inflation empty, missing
used-by empty.

Frontier rows advanced: **F17 → F18** (`corpus/README.md:388`, amendment at `:370`), subject
"CISA Known Exploited Vulnerabilities catalog — exploitation-status-based prioritization distinct
from CVSS severity", ids `S052`. A new coverage-map row records the area as
"Known-exploited-vulnerabilities prioritization (round 35)" (`corpus/README.md:380-382`); the amendment
heading is `## Round-35 admission — coverage map row and Frontier F18 (appended 2026-10-26)` at
`corpus/README.md:370`. Search log:
one round-35 bullet at `corpus/SOURCES.md:79` (question, where, date, identified/screened/included/
excluded, stop rationale), superseded-but-retained at `:111` by the wider draft in `ScribeSearchLog.md`
§5 (catalog page, CSV reconciles record-for-record — 1756 `cveID`s identical as a multiset, the CSV's
12 columns exactly the feed's 12 fields — JSON schema, both directive pages), with a scope correction
at `:112` (the bullet's zero-hit counts exclude `corpus/lessons/`, where the `KEV` token pre-existed
at `corpus/lessons/round-22.md:91`).

Census before → after: both exit 0, both carrying only the two standing W04 warnings (`S028`
docs.hackerone.com duplicate URL, `S029` EUR-Lex duplicate URL) — `census-before.txt`; after-run
`ExecCensusAfter.md` (receipt not on disk at this read; the counter is reproduced in
`ExecRegistryAppend.md` §census and in the SCORECARD measurement state).

Sourced claim: C2 rests on `S052` opened this round (capture + manifest + row + entry all landed,
source-recheck exit 0 on committed bytes, live re-open 0 differing lines). Sibling ruling: 20 siblings
scanned, 19 zero-hit; the only ground-token hits are two `kake-shokunin` lines recording the
screening-out of the **CISA BOD 20-01** template (a directive about *publishing a VDP*, not
exploitation-status prioritization), plus adjacent-theme hits in `kagi` (an NVD page used as a quote
source, explicitly not registered), `mori` (a raw evidence blob) and "in the wild" in a
mutation-testing sense — every one ruled **no contested scope**, and
`shokuknow/doctrine/channel-recurrence.md:62` (`| cisa.gov | kasegi |`) ratifies the assignment
(`ScoutSiblingSweep.md`, `ConnSibling.md`, `ConnSibling-ruling-draft.md`). No report-to-lane item
arises.

Assimilation: **none adopted.** `ExecIdCollisions` (0–3-space pattern) prints `reg_ids=52`,
`staged_ids=94`, `collisions=22` (`S031..S052`; 21 before the S052 row landed) and proves the guard
once: an indented `S031` row is caught (1) under the wide pattern and missed (0) under a
column-0-only pattern; negative control 0; absent registry exit 2. Disclosed limits: a 4-space or tab
indent is not caught; adoption is by document, never by number — staged `S052` is CNNVD weekly, lane
`S052` is CISA KEV. Quarantine slice: 7 register rows re-derived, S-id on every line, verdicts
`present-and-located 4` (S065, S068, S069, S070) · `prose-class-unverifiable 2` (S037, S054) ·
`unreachable 1` (S048, 404) · `absent 0` · **adopted 0**
(`ExecQuarantineSlice.md`; `assimilation/quarantine-verdicts.md`). Verdict corrections recorded
rather than adopted: S068's located sentence is already lane row **S040**; S069/S070 locate only
under a TLS-bypass or plain-http invocation, so under strict verification they stay
`unreachable`-by-policy. Seven standing package refusals re-confirmed with flip conditions unmet
(`corpus/lessons/round-35.md` § Gate).

## Trend verdicts

- **expansion: `improved`** — one admitted knowledge entry on ground the coverage map did not hold
  (exploitation-status prioritization, as against the severity scales S001/S002/S046/S047 and the
  platform ladders S043/S044/S049/S050/S051), frontier 17 → 18, registry 51 → 52 with the only added
  row at tier A, the entry citing the mined row `source: S052`, harness 21/21, and the sibling ruling
  finding no contested scope. **No capability row**: the closure suite is a defect counter, not new
  repertoire, so the capability window is not restarted (last entry round 33).
- **quality: `improved`** — all seven routed defects closed with a runnable counter: `closed=7/7
  exit=0`, base `closed=0/7 exit=1`, `--selftest cases=7 failures=0`, 14/14 vacuous+delete mutants
  killed (`MutClosureSuite`), 16 clause mutants in `CritC1Kill`'s battery, forged summaries
  rejected 5/5, and the D1
  episode disclosed rather than hidden (the integration stub re-armed the placeholder at `0aee0ef`
  and `8ce6fb4` repaired it); `recheck-audit.py` `strict pass=47/47` with the expectation limb clean;
  `anchorcheck.py` 0 bad; no admitted entry failed its own re-check (S052 re-opened live,
  byte-identical). **Bound this word**: the same suite is a presence-test counter whose own bytes are
  unpinned (CritC1Kill F-1) and whose D2/D3/D7 clauses a negation satisfies (F-2…F-5), and three of
  its limbs were green only after the L1's landings.
- **discernment: `improved`** — the assimilation gate adopted nothing from seven quarantine rows
  while producing four located anchors, two description-class refusals and one duplicate identified
  against an existing row; the F18 entry took a reviewer's REFUSE on Q2 and repaired by deleting the
  unsupported claim instead of registering a source that would have broken the frozen registry
  literal; the junk twin is rejected by the invocation the D5 erratum defines (and the twin's own
  line was shown non-discriminating rather than glossed); the sibling sweep produced a ruled
  non-conflict with named discriminating tests; and the round reports the score distance instead of a
  move — `score-gap.py` prints `gap: 24 of 47 rechecks still gated on a lost base; score 5 needs 0
  gated unsupported claims` against `SCORECARD.md:331`. Recorded cost: `CritC2Kill` G1–G6 and
  `CritC1Kill` F-1…F-5 are verifiability gaps left open by design this round.

## SHONEN

The round-35 block was committed at `48e6053` and edited again in the worktree (`SHONEN.md`
`90385026…`, 160 lines); the four boxes and line numbers below are the worktree's, as read at 07:08Z.

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources —
  `SHONEN.md:88`; the Gates & probes registry home now carries `r-defect-closure.sh` (`SKILL.md:1097`)
  and `kill-rule-check.py` (`:1098`) with name / type / entry command / verdict map / selftest
  spelling / pinned-value path / write scope / owner (D3); `git diff --numstat 3266c99 -- SKILL.md`
  = `13 0`; no-harm: `anchorcheck.py` 0 bad, `BASE-ABSENT=0`, and density **201.2 → 220.9** (the one
  appended high-density block) — the round-35 SCORECARD guard row states both limbs. Box stays `[~]`.
- [~] At least one end-to-end domain task executed and logged in LOG.md — `SHONEN.md:108`; **no new
  end-to-end domain task ran this round.** `LOG.md` carries the heading at `:1651` and logs instruments
  and an admission, not a hunt-to-claim task; the closest executed work is instrument closure
  (`closed=7/7`, `cases=7 failures=0`). Box stays `[~]`.
- [~] Instructions executable by an agent without oral context — `SHONEN.md:120`; the F18 entry is
  the 47th knowledge entry and its own `recheck:` line runs unmodified (`sha256 OK`, five
  assertions, exit 0) and fails closed on a moved quote (exit 1) or an absent manifest (exit 2);
  `recheck-audit.py` is `strict pass=47/47`, `expect=present expected=47 missing=0 unexpected=0`;
  the closure suite is executable end to end. Box stays `[~]` on the capability-row limb.
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `SHONEN.md:135`; `PROVINCE.md` is
  byte-unchanged (75 lines, `b4bb5fee…`, `git diff --numstat` empty), F18 sits inside the province's
  "program rules, claim packages" core, and the sibling ruling is "uncontested by any sibling
  corpus". Box stays `[~]`.

## Boundary and open items

- **Quiescence was not achieved before the L1's commit.** After `5a25337`, two receipts changed
  (`ExecD1Markers.md` 04:02:37, `ExecDoNothingReject.md` 04:03:30 local) and the full
  `SCORECARD.md`/`SHONEN.md` sections landed in the worktree. This is M35-1's class in the round that
  files M35-1; the closing commit must absorb them, and the report should name the offset rather than
  describe the committed tree as final. `wave1-results.json` for round 35 was still pending the
  dispatcher (`LOG.md:1658`); if it lands after `<LANE_HASH>` the D4 defect recurs with its own fix
  (commit it with the provenance note, as round 34's was).
- **The lesson's closing hash is a third placeholder spelling.** `corpus/lessons/round-35.md:3` writes
  `closing lane-commit hash INTEGRATION_HASH_PENDING` deliberately, "because C1's own D1 clause counts
  that token" (its words). That is honest under the frozen literals — D1 counts `filled by the L1` and
  `<LANE_HASH>` — but it means the counter cannot see this placeholder either, which is the same
  vocabulary blindness D1 filed. The L1's final commit should replace it with the real hash rather than
  leave a third spelling that no check covers.
- **Two seats had no receipt on disk at this read:** `ExecRegressionC1` and `ExecCensusAfter`
  (`ScribeShonen`, `ScribeScorecard` and `SentScopeFinal` landed at 07:05–07:10Z, after the L1's
  commits, and are still uncommitted). The L1 should record them as late/absent rather than count
  them as landed.
- **Suite identity is unpinned (CritC1Kill F-1).** The frozen kill rule's "proved by the suite's own
  `--selftest`" is discharged by the artifact under test; the file also moved through five digests
  during the wave (773 → 832 → 834 lines), so a digest pin taken at quiescence is the one-command fix.
  F-2…F-5 (file-wide literal clauses: a negation satisfies D7, a mention satisfies D2/D3, an empty
  JSON satisfies D4's tracked limb) are recorded with one-command corrections each
  (`CritC1Kill.md` §5); none landed this round.
- **Three of the seven checks are presence tests, not truth tests.** `D2`'s "no deletion" limb is
  byte survival of the row's opening (not a diff count — a fixture tree cannot run git);
  `D3`'s clause is satisfied by a prose mention (Measured: an `SKILL.md` reading "deliberately NOT in
  the Gates & probes registry" passes); `D7`'s clause is satisfied by a row that negates the
  correction. `CritMistakes.md` F2 also records that the registry rows name the round-34 instruments
  and the round's **own** `r35-defect-closure.sh` remains unregistered — the frozen D3 literal is met,
  the widening it implies is open.
- **C2 residual gaps (CritC2Kill, measured).** The artifact claim survives (the capture is
  byte-identical to a live fetch; the entry's FC checks re-compute true), but the recorded gaps are
  G1 (no instrument reads an entry's assertions), G2 (captures are bound by name and URL string, not
  content — a renamed error page with a self-consistent manifest passes), G3 (no `mined ⇒ capture`
  rule), G4 (the committed twin's own line exits 0, so that clause is not reproducible as built),
  G5 (`PASS F18 ids=S052` means binding + recheck exit, not that the entry's claims were checked),
  G6 (shape counters are text shapes). `MutC2Entry` additionally shows a retargeted manifest anchor is
  not fatal while `occurrences=1`, and that a paraphrased entry quote passes both the harness and
  `source-recheck`.
- **Score distance, measured not claimed.** `score-gap.py` (`57584fda…`; registered digest
  `855869bf…` — drift recorded, R9 forbids rewriting) prints `gap: 24 of 47 rechecks still gated on a
  lost base`; 23 gate on `~/Projects/bounties` (absent since 2026-09-28) and/or
  `~/Projects/the-bounty-hunter` (2026-10-12), one on the mirror cite in `citation-bases.md`;
  `anchorcheck.py` still reports one PAST-EOF instance outside scope (`corpus/QUALITY.md:77` → bare
  `README.md:159`). depth:verifiability stays at 4; the lowest-axis obligation stays active.
- **Credential/scope posture.** `SentCred` verdict **CLEAN** (`blocking_findings: 0`; no credential
  material, session value or private URL in any new artifact; the only literal account identifier is
  the CVE-2020-29583 description's undocumented `zyfwp` account, which is advisory text). `CritBoundary`
  records F1 (a receipt asserted `scratch-absent` before the tree was gone; measured absent at
  06:47:48Z), F2 (an uncommitted plan edit), F3 (attempt-suffix collapsing puts attempts in one
  scratch dir) and F4 (`claims-erratum-d5.md` §3 prescribes `/fast/scratch/kasegi-d5/S051`, outside
  the mandated root — documentation only). `SentScopeFinal` closes the set: **PASS** on items 1–3
  (no seat wrote outside the lane; the one fleet-root hit is attributed non-seat; no lane git/jj
  mutation by seats — 8 commits, all L1; `shokuknow` untouched), with item 4 (scratch discipline)
  carrying three deviations: F1 an unattributed bulk scratch deletion, F2 two files left outside a
  seat's own scratch dir, and a leftover check that must be re-run after settle.
- **Tools installed: none**, by this seat or, per the receipts read here, by any seat; no pacman
  transaction was attempted (host-wide pause respected).
- **Scratch.** `/fast/scratch/hyaku/kasegi-r35/ScribeReportDraft/` was never created — every
  measurement was a read-only lane command (see § Report). Nothing of this seat's remains on disk.

## Measurement state (final digests, read 2026-10-26T07:06–07:10Z)

`corpus/SOURCES.md` `0f95a132…` (112 lines, 52 rows) · `corpus/README.md` `277f04ce…` (396 lines,
18 frontier rows) · `SKILL.md` `daeff71b…` (1104 lines) · `corpus/QUALITY.md` `d4f83bb1…` (250 lines,
R1–R27) · `corpus/lessons/round-35.md` `841b1112…` (521 lines at the final read; it moved `119408b3…` → `99abcb5a…` → `177b9585…` → `841b1112…` while the wave closed) · `LOG.md` `a576d58c…` (1659 lines) ·
`SCORECARD.md` `ed6e931f…` (1404 lines, committed at `48e6053`, both round-35 sections) · `SHONEN.md`
`90385026…` (160 lines, worktree) · `corpus/instruments/r35-defect-closure.sh` `0ae4b484…` (834 lines, 35391 B) ·
`corpus/instruments/r35-fixtures/fixtures.json` `b9a07afa…` ·
`corpus/source-snapshots/round-35/S052.txt` `d69349e8…` (1479694 B, 27870 lines) ·
`corpus/source-snapshots/round-35/manifest.json` `06bfcc71…` (5631 B) ·
`corpus/knowledge/cisa-kev-catalog.md` `e9de994d…` (91 lines) ·
`corpus/instruments/knowledge-expected.txt` `d2e99ca6…` · `claims.json` `fe0dae89…` (byte-identical
to the freeze blob) · `.ufo/waves/round-34/wave1-results.json` `3afa3581…` (312874 B) ·
`.ufo/waves/round-34/wave1-results.json.provenance.md` `e1c44301…` (5639 B) ·
`.ufo/waves/round-35/claims-erratum-d5.md` `eee0bb57…`.

## Report

Seat: `ScribeReportDraft` (scribe, round-35 wave 1, leaf). Scope: draft the report body at
`.ufo/waves/round-35/wave1/ScribeReportDraft.md`. No git/jj mutation; no product file written; no
subagent; no `agent://all`; tools installed: none.

### Commands and outputs (read-only, cwd = lane)

```
$ date -u                                   → 2026-10-26T07:06Z / 07:08Z (two reads; the second after ScribeScorecard landed)
$ git log --oneline -8
48e6053 round-35: scorecard + SHONEN late seat appends
bb2dc8c round-35: receipt finalization — ExecDoNothingReject updated receipt, ExecD1Markers receipt fix
5a25337 round-35: commit wave leftovers — S052 capture (named >1MiB), SKILL registry, controls, ready markers, receipts
8ce6fb4 round-35: D1 closure fix — scorecard closing-commit wording
0aee0ef round-35: integration — lesson, scorecard, SHONEN, LOG, wave receipts, assimilation artifacts
aa6ad99 round-35: L1 integration — C1 D4/D6/D7 lands (results tracked + provenance, L1Integration correction, QUALITY supersessions)
da2d3c6 round-35: wave-1 spec + dispatch (64 seats, v2)
617496b round-35: claims freeze + before controls
$ bash corpus/instruments/r35-defect-closure.sh | tail -3        → D7 … open=0 / closed=7/7 exit=0   (exit 0)
$ bash corpus/instruments/r35-defect-closure.sh --selftest | grep 'selftest cases='  → selftest cases=7 failures=0   (exit 0)
$ grep -c 'filled by the L1' SCORECARD.md                        → 0
$ grep -c 'c1c6a5f' SCORECARD.md                                 → 3
$ grep -c '201\.7' SCORECARD.md ; grep -c '201\.2' SCORECARD.md   → 5 ; 6  (SCORECARD grew during the wave; re-run at the closing commit)
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md → 52
$ grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md  → 1
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                     → 18
$ grep -lE '^source: S052 ' corpus/knowledge/*.md                → corpus/knowledge/cisa-kev-catalog.md (1)
$ ls corpus/knowledge/*.md | wc -l                               → 47
$ python3 corpus/instruments/frontier-recheck-count.py | tail -2  → PASS F18 … ids=S052 exit=0 / entries=21 pass=21 exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052 | tail -3
  → S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=15472-ok … (exit 0)
$ python3 corpus/instruments/recheck-audit.py | tail -2           → strict pass=47/47 … exit=0 ; expect=present expected=47 missing=0 unexpected=0 exit=0
$ python3 corpus/instruments/anchorcheck.py SKILL.md | grep '^==' → 16 in-range cite instances, 0 bad; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0 (exit 0)
$ python3 corpus/instruments/density.py SKILL.md | tail -2         → 26 blocks, mean dens 220.9, 742 cites (exit 0)
$ sha256sum corpus/SOURCES.md corpus/README.md SKILL.md corpus/QUALITY.md corpus/lessons/round-35.md LOG.md SCORECARD.md SHONEN.md corpus/instruments/knowledge-expected.txt .ufo/waves/round-35/claims.json corpus/source-snapshots/round-35/manifest.json corpus/knowledge/cisa-kev-catalog.md corpus/instruments/r35-defect-closure.sh
  → the digests in § Measurement state (all exit 0)
$ git ls-tree -r --name-only 617496b9 -- .ufo/waves/round-35/   → claims.json, c1-controls/before.txt, c2-controls/before.txt, census-before.txt
$ git ls-files .ufo/waves/round-34/wave1-results.json | wc -l    → 1
$ git status --porcelain                                        → at 07:08Z: SHONEN.md, corpus/lessons/round-35.md, wave1/{ScribeShonen,ScribeScorecard}.md untracked/modified + this seat's own draft
```

### Verification boundary

- Every figure above is either a command this seat ran at the stated instant, a digest it computed,
  or a quoted receipt with a named location. Volatile files (`SCORECARD.md`, `SHONEN.md`,
  `corpus/lessons/round-35.md`) kept growing while this draft was composed; their digests are the
  read instant's and the L1 must re-digest them at the closing commit.
- **Not verified by this seat:** the wave's product claims as a whole (that is the L1's and the
  verifier's job); the receipts this seat did not read (the three missing seats, `SentCred`'s
  classifier internals, `ConnClaims`' mapping); whether the missing seats land later; whether the
  closing commit absorbs the remaining worktree entries.
- The worktree moved while this draft was written (`SCORECARD.md`/`SHONEN.md` gained the round-35
  sections, two receipts were rewritten). Both readings are given where they differ; the digests in
  § Measurement state are the worktree's at the final read.

### Fixture/scratch

```
$ test -d /fast/scratch/hyaku/kasegi-r35/ScribeReportDraft && echo PRESENT || echo ABSENT   → ABSENT
```

No scratch tree was created: every measurement was a read-only command in the lane.
