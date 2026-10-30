# Round 34 — kasegi

Lane: `kasegi-shokunin`. This lesson reports working-tree and receipt evidence, not a canonical
judge decision. Revisions: base `014ee2d7aa8c3c095ff57ae51097606a9906228c`; claims-freeze commit
`29f606dbdd28aff6fd4573ab4b90788bbb90af13`; wave-1 dispatch commit
`206e5108f1190e61b3e2622d21cab8a5d921650c`; final integration hash `4b0a9f29a8797828fb711faed80ee151afdf5117` (the L1
fills this after the integration commit; this seat does not commit).

Shape: **one v2 wave**. Wave 1 `kasegi-r34-build`, **65 seats**, dispatch one batched task call
(`.ufo/waves/round-34/wave1-dispatch.json`: `schema=ufo-swarm-wave-dispatch-v1`, `wave=kasegi-r34-build`,
`counts={spawn: 65, resume: 0, total: 65}`, `policy.maxLanes=128`; `wave1-spec.json` carries 65
`items`; `wave1.ready` names `l1: KasegiR34`). Declared role counts from `wave1-spec.json`:
executor 19, reviewer 13, scribe 10, mutation-tester 7, scout 5, critic 5, connector 3,
sentinel 2, simplifier 1 (= 65). Route: L1 inline spawn handoff, hyaku run 8 (chain:
`29f606d` freeze → `206e510` dispatch, committer times `2026-10-26 02:28:39 -0300` /
`02:29:48 -0300`, read from `git log` by `wave1/ExecScorecardMarkers.md` §1). Axes owned
(`claims.json` `axes_owned`): `depth:density`, `depth:verifiability`, `coverage`; saturation line
9/10 per axis, window N=3; lowest non-retired axis `depth:verifiability (4)`.

Receipt coverage at composition: **61 of 65** seats filed a receipt in
`.ufo/waves/round-34/wave1/`, counted four times as the wave settled (53 at `05:48:55Z`, 57 at
`05:56Z`, 59 at `05:58Z`, 61 at `05:59Z` — `ls wave1/*.md` vs `wave1-spec.json` names). Absent at the
last count: `ExecNoHarmFinal`, `ExecRegressionC1`, `ScribeShonen`, `ScribeReportDraft`,
`SimplifierCleanup` (plus `ScribeLesson`, this file). One receipt is filed under a name the spec
does not carry — `wave1/ScribeReportDraft-2.md` — so the name-vs-file comparison counts one extra
file and one missing name for the same seat family; the match is stated rather than silently
repaired. (`ScribeScorecard` landed both its receipt and its `SCORECARD.md` section during
composition; this lesson reads the section directly at `:1149-1152`.) Every "after" number below is
therefore either (a) a
receipt's own measured output, quoted with its digest, or (b) this seat's own composition batch at
the timestamps and digests stated inline. The census-after receipt (`wave1/ExecCensusAfter.md`) landed
at `05:56Z` and is cited where it applies; **no no-harm or regression receipt**
(`ExecNoHarmFinal`, `ExecRegressionC1`) had landed, so the § No-harm table is this seat's own
measurement plus the earlier `RevNoHarm` and `SentScopeFinal` snapshots, and it says so rather than
inventing a receipt.

Answering model on seat receipts (by the name each receipt states for itself): **5 of 61**
receipts name one — `opencode-go/deepseek-v4.1-flash` in `wave1/ExecBeforeReceipts.md:5`,
`wave1/ExecLessonErrata.md:4`, `wave1/ScribeSkillGate.md:5`; `anthropic/claude-sonnet-5-5` in
`wave1/ScoutPackageThemes.md:3`; and one more in `wave1/ScribeReportDraft-2.md`. The other 56 name
no model. (Round 33 reported 25/56 naming a model; the drop is a receipt-hygiene change, not a
model observation this lesson can make.)

Frozen controls caveat: `.ufo/waves/round-34/{census-before.txt,c1-controls/before.txt,c2-controls/before.txt}`
are **byte-identical** (`d90ce017…db5f0`, measured by this seat with `sha256sum`), so the round has
one before-receipt copied three times, not three independent captures
(`wave1/ScoutDatawalk.md` §0). The values are reproducible; the placement implies more evidence
than exists.

## Frozen claims — before → after

Before column: the frozen controls at base `014ee2d` (claims-freeze evidence, not seat work).
After column: measured on the wave-1 working tree, with the receipt that holds the run, plus this
seat's composition batch (`2026-10-26T05:48–05:52Z`, digests in § No-harm).

| Claim | Axis | Before (frozen controls, base `014ee2d`) | After (landed bytes) | Verdict / boundary |
|---|---|---|---|---|
| **C1** | depth:verifiability (4) | `r-defect-closure.sh` absent (`ls_exit=2`); `capture-binding --selftest cases=11 failures=0`; `SCORECARD.md` `<LANE_HASH>`=2; round-32 `fetched_utc=2026-10-25T23:14:00-03:00` ×2; round-26 manifest `records=1 paths=['S041.txt']` (no S040); QUALITY `exactly one`=1; round-33 lesson `Erratum`=4 with `R7`=0; plain audit `records=40 bound=40 unbound=0`; rule A one-directional; no junk twin (`c1-controls/before.txt`; replayed line-by-line in `wave1/ScoutDatawalk.md` §1 and `wave1/RevC1BeforeAfter.md` §1) | `closed=9/9 exit=0`; `--selftest cases=9 failures=0`; `kill-rule-check` `mutants=3 killed=3 survivors=0 invalid=0`, `gates` all `ok`, `survivors=0`; `capture-binding --selftest cases=23 failures=0` (23 case lines, all `verdict=pass`); plain audit `records=41 bound=41 unbound=0`, `orphans=1 orphan=S040-live.txt`; `grep -c '<LANE_HASH>' SCORECARD.md` → 0 with `Correction (round 34)` at `SCORECARD.md:1116`; round-32 `fetched_utc` `2026-10-26T04:16:06Z`/`:16Z`; round-26 `orphans[0]=S040-live.txt` with sha `b7f7b55f…`; `corpus/QUALITY.md:220-222` R20 note, `:226` R22, `:228` R24; `corpus/lessons/round-33.md:140` (R7) and `:215` (R4); rule A bidirectional (`mirror=0 reverse=1`, harness `selftest cases=6 failures=0`); junk twin committed at freeze (`29f606d`, blob `50f7a84c`) | **Predicate reproduces literally**; nine R1–R9 limbs closed on the tree measured. Boundaries: the junk-twin rejection limb is disputed (below), and `CritC1Kill` measures four routes on which the predicate is satisfiable without the property it certifies. C1 is **held, not increased**. |
| **C2** | coverage (7) | frontier 16; registry 50; `S051` rows 0; entries citing S051 0; harness `entries=19 pass=19 exit=0`; `source-recheck` S051 `manifest UNAVAILABLE reason=missing`, exit 2; knowledge entries 45 (`c2-controls/before.txt`; re-run at base by `wave1/RevC2BeforeAfter.md` §0b) | frontier **17** (`corpus/README.md:361` F17 row); registry **51** (`corpus/SOURCES.md:57`); `S051` row 1; entries citing `^source: S051 ` 1; knowledge entries **46**; harness `entries=20 pass=20 exit=0` with `PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051`; `source-recheck --source S051` exit 0, 18 assertions `OK`, 16×`occurrences=1`, Q9/Q17 `occurrences=2 anchor=77-ok`/`96-ok`; census exit 0, W04 S028/S029 only | **Counters reproduce**; capture is real (two independent live re-fetches byte-identical to `S051.txt`, `wave1/ScoutImmunefiLive.md`, `wave1/CritC2Kill.md` §2). Boundaries: the twin's executable rejection is ambiguous (below), "every assertion occurrences=1" is false as worded, and the landing checks cannot tell a fabricated capture from a real one (`CritC2Kill` G1–G5). C2 is **held, not increased**. |

Named after-values with the receipt that produced each (all re-measured by this seat at
`05:48–05:52Z`, digests in § No-harm):

| limb (claims.json) | receipt | this seat's run |
|---|---|---|
| `r-defect-closure.sh` → `closed=9/9 exit=0` | `wave1/ExecRDefectClosureSuite.md` §3; `wave1/RevC1BeforeAfter.md` §2 c1; `wave1/RevRSuite.md` §2; `wave1/ExecDoNothingReject.md` §1 | `closed=9/9 exit=0`, exit 0 |
| `--selftest` → `cases=9 failures=0` | same four receipts; nine `selftest case=R# live=pass fixture=rejected verdict=pass` lines | `cases=9 failures=0`, exit 0 |
| suite fails on base → `closed=0/9` | `wave1/ExecRDefectClosureSuite.md` §5; `wave1/RevC1BeforeAfter.md` §3; `wave1/ExecDoNothingReject.md` §1 | quoted from receipts only (this seat did not re-extract base) |
| `capture-binding --selftest` N≥19 with nine named cases | `wave1/ExecCaptureBindingHarden.md` §2; `wave1/RevC1BeforeAfter.md` §2 c3 (all 23 case names listed); `wave1/CritOverclaim.md` §1 | `selftest cases=23 failures=0`, 23 case lines |
| `kill-rule-check` → `survivors=0` | `wave1/ExecKillRuleCheck.md` §3; `wave1/MutKillRuleMutants.md` §2; `wave1/CritOverclaim.md` §1 | `mutants=3 killed=3 survivors=0 invalid=0`; `gates=7 failed=0` |
| `<LANE_HASH>` 0 in `SCORECARD.md` | `wave1/ExecScorecardMarkers.md` §3–§4; `wave1/RevErrata.md` §2 | `grep -c` → 0 (exit 1) |
| erratum 2 + pre-freeze step | `wave1/ExecErratum2.md` § "Post-state"; `wave1/ExecQualityAppends.md` §2; suite R2 `open=0` | `SCORECARD.md:1014-1035` present |
| QUALITY R20 per-id note | `wave1/ExecQualityAppends.md` §2–§3 | `corpus/QUALITY.md:220-222` |
| round-33 lesson R7 erratum | `wave1/ExecLessonErrata.md` §1–§2; `wave1/RevC1BeforeAfter.md` §4 R7 | `corpus/lessons/round-33.md:140` |
| round-32 strict-UTC only | `wave1/ExecManifestR32Normalize.md` §3; `wave1/RevManifestR32.md` §2 | `72ab4e68…`, both `…Z` |
| S040 record-or-orphan | `wave1/ExecS040Orphan.md`; `wave1/RevOrphan.md` §1–§2 | `orphans=1 orphan=S040-live.txt`, exit 0 |
| rule A both directions | `wave1/ExecFrontierBidirectional.md` §4–§5; suite R9 `open=0` | harness exit 0, 20/20 |
| junk twin committed and rejected | `wave1/RevJunkTwin.md` §1, §3 | committed at `29f606d`; **rejection disputed — see Gate** |
| C2 reach + capture + manifest | `wave1/ExecRegistryAppend.md` §3–§4; `wave1/ExecSnapshotR34.md`; `wave1/RevRowS051.md` §1–§5; `wave1/RevC2BeforeAfter.md` §1–§6; `wave1/ExecHarnessAfter.md` §4 | 17/51/1/1, 46, `entries=20 pass=20 exit=0`, recheck exit 0, census exit 0 |

Limb-oracle evidence (receipts only — this seat re-ran none of these matrices, and says so):
`wave1/MutRSuiteChecks.md` fields **nine** one-limb mutants of `r-defect-closure.sh`
(`bc489312…` … `8240a328…`) and each is KILLED twice over — `cases=9 failures=1` / rc=1 under
`--selftest`, `closed=8/9 exit=1` under the plain run — which is the two-sided shape QUALITY R24
now requires. `wave1/MutFrontierRuleA.md` §5–§6 kills the reverse-direction (`M-REV`) and
forward-direction (`M-FWD`) mutants against the landed rule A, with the no-op control explicitly
**not** a kill. `wave1/MutKillRuleMutants.md` §2–§3 replays the three named counter mutants and the
forged-summary forms (`wave1/MutSelftestSummary.md` §§3–4: `cases=0` and a forged `cases=19`
summary are both rejected). `wave1/MutC2Entry.md` kills M1 (dropped `source:` line → harness
`pass=19 exit=1`), M2 (`quote-not-found`), M3a (`anchor-broken`) and M4 (unregistered `--source`),
and records **one survivor**: M3b — moving the Q9 anchor from 77 to 62 still prints
`occurrences=2 anchor=62-ok`, because the quote legitimately occurs at both lines; the anchor pins
a *window*, not the intended occurrence (open item 16). `wave1/MutManifestField.md` and
`wave1/MutCaptureBindingLimbs.md` field seven and one-limb instrument mutants against the
capture-manifest rules; their verdict tables read `KILLED` for every field mutant, with the
controls behaving as required.

Claim-text corrections of record (frozen text is never edited; these are appended files):
`.ufo/waves/round-34/claims-erratum-1.md` (`sha256 6a3cd99e…`, filed by the L1 before any scoring
verdict) rescopes C1's counting literal `records=40 bound=40 unbound=0` to
`records=41 bound=41 unbound=0` once S051's row lands; the intermediate
`unbound=1 FAIL rule=no-row record=S051` state is itself the proof rule B binds. Its disclosure
duty ("disclosed on every surface that reads the C1 counter") was **not** visible when
`wave1/RevC1BeforeAfter.md` F2 measured, because the round-34 SCORECARD section did not exist yet;
it now lands in that section (`SCORECARD.md`, the `claims-erratum-1.md` paragraph at `:1149-1152`,
naming `records=41 bound=41 unbound=0` and labelling the intermediate reading PRE-STATE), appended
by `ScribeScorecard` while this lesson was being composed. The round-33 Rule-B erratum-2
restatement is `SCORECARD.md:1014-1027`, its pre-freeze satisfiability step `:1028-1035`.

## Gate

Gate requirement (≥1 admit + ≥1 reject) is met by **one admission (F17 + S051)** and **seven
standing refusals plus two quarantine refusals and one committed junk control**. The package
`/home/vgpnk/Projects/shokuknow/merge/kasegi/` and the register
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(`sha256 5afe1810a6c3…`, 375 lines) were read-only throughout; no package tool
(`renumber-staged.py`, `merge-plan.py`, `quote-lint.py`, `absent-defect-register.py`) was run, and
nothing was written under `shokuknow` this round (`wave1/SentScopeFinal.md` §3 Axis C: PASS).

### Admitted — F17 / S051

| item | evidence | decision |
|---|---|---|
| **F17** — `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` (`sha256 948b202e…c1d8a`, 113 lines) | Q1–Q10 all `pass` on measured evidence, every quote exactly-once at its cited line or anchor-verified (`wave1/RevEntryF17.md` §2–§3, **ADMIT**, §7); 11/11 falsifiable-check counts reproduced (§4); recheck parses, runs from `/tmp`, exits 0, fails closed on a missing manifest (§5) | **Admit.** |
| **S051** — Immunefi Vulnerability Severity Classification System v2.2, `https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/` | Access date **2026-10-26**; capture `corpus/source-snapshots/round-34/S051.txt` (`4fd8ed98…b325a5`, 8502 B, 175 lines), manifest record `fetched_utc 2026-10-26T05:31:10Z` (strict UTC), `fetched_bytes=219383`; live re-opens byte-identical at `05:33:38Z`, `05:35:45Z`, `05:42:46Z` (`wave1/ScoutImmunefiLive.md`, `wave1/RevRowS051.md` §2, `wave1/CritC2Kill.md` §2); registry row `corpus/SOURCES.md:57`, tier `A`, status `mined`, `opened 2026-10-26`, `recheck 90d`, used-by the F17 entry (`wave1/RevRowS051.md` §1) | Tier A, mined. Live-capture admission, not a staged row (`grep -riE 'immunefi\|vscs'` over the package → 0 files). |

Gate quotes (≤25 words, located, access date 2026-10-26):

1. «At Immunefi, we classify bugs on a simplified 5-level scale:» — 11 words, `S051.txt:46`,
   exactly once in the capture and once live (`wave1/ScoutImmunefiLive.md`).
2. «Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield» —
   14 words, `S051.txt:75`, exactly once in the capture and once live; it is manifest Q8
   (`anchor=75-ok`).

Scoping that bounds every future quote from this row: the page names v2.2 at L1 and L45 and
carries no v2.3 string; the Immunefi index lists **both** v2.2 and v2.3 under "Currently in Use",
so "the current/latest system" is **not** supported and the row carries no `latest`/`current`
claim (`wave1/ScoutImmunefiLive.md` Finding 2, `wave1/RevRowS051.md` §5). The page states no CVSS
mapping, no reward figure and no version-selection rule (FC-2/FC-3/FC-4 → 0 occurrences).

### Rejected — standing refusals (all re-measured this round, flips still unmet)

| staged entry | decision | reason (lane-side, measured today) | flip condition |
|---|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` (`120d8cd5…`) | **REFUSED** (standing from round 30) | `grep -cE 'txt:[0-9]+'` → 0 located quotes; its `ground: F09` collides with the admitted F09 at `corpus/README.md:210` | Register+capture CNVD helpList and 360SRC rules (**met**, S049/S050), **and** located quotes, per-platform attribution, executable recheck, re-grounding on a lane F-id |
| `claim-packaging-and-report-quality.md` (`6ad64d78…`) | **REFUSED** (standing) | `grep -c bilibili corpus/SOURCES.md` → 0; BILISRC `S036` in no lane row | Register+capture S034/S035/**S036** |
| `cn-crowdsourced-testing-roles-and-conduct.md` (`a5302aaf…`) | **REFUSED** (standing) | no H1 (`grep -c '^# '` → 0); S081/S082 absent from the registry | H1, register+capture S081/S082, page/line quotes with exactly-once counts |
| `chinese-crowd-testing-national-standard-2026-10-23.md` (`6c15d941…`) | **REFUSED** (standing) | `std.sacinfo.org.cn`/`sac.gov.cn`/`hcno=57CAF3B4` → 0 rows; `^\| F24 \|` → 0 (frontier is F01–F17); zero 「…」-marked strings | Register+capture S077/S078/S079, roles-and-duties sentence quoted with a location, re-ground on a lane F-id |
| `chinese-criminal-thresholds-and-authorisation.md` (`1660c00c…`) | **REFUSED** (standing, round 30) | its staged ids `S044`–`S046` are occupied by Bugcrowd VRT / Bugcrowd CWE / IPA JVN rows, so registration needs the package renumbered first | Register+capture S044/S045/S046 in non-colliding id space, bound the conclusion to located text |
| `chinese-program-severity-instrument.md` (`442e0f2b…`) | **REFUSED as an entry** (round 33) | anchor `newsType_6` absent from `S049.txt` (`newsType_21` → 1); `sse.com.cn` unregistered | Anchor present in a capture, second source registered; its S049-verified facts stay reusable with locators |
| `program-severity-ladders-and-reward-scales.md` (`35de5f8b…`) | **REFUSED / do-not-copy** | same-name lane entry with different bytes (`35de5f8b…`/50 L vs lane `6c05c98f`/67 L) — an overwrite hazard | Overwrite hazard, not a flip; treat as do-not-copy |

Evidence: `wave1/ScribeAssimilationGate.md` §3 (table + two timed runs, `05:31Z` and `05:39Z`,
values identical across the S051 landing), `wave1/ScoutPackageThemes.md` §2–§3.

### Quarantine slice — 7 register rows re-derived and re-fetched

Slice re-derived (same seven ids and order as the committed
`.ufo/waves/round-34/assimilation/quarantine-slice`, `slice_rows=7 slice_malformed_lines=0`) and
each row fetched live at `2026-10-26T05:31–05:32Z` (`wave1/ScribeAssimilationGate.md` R2–R3;
independently `wave1/ScoutQuarantine.md`):

| staged id | register class | live fetch | verdict |
|---|---|---|---|
| S037 openstd GB/T 30279-2020 | `payload-absent` | 200, 24209 B | **refuse** — the registered span is a spliced field collage: the full span is absent (exact and whitespace-folded `False`) while each of its 8 fragments occurs exactly once. Flip: re-stage the contiguous field sequence, and add a lane row first (`grep -c openstd corpus/SOURCES.md` → 0) |
| S054 内閣府 vulnerability-information request | `payload-absent` | 200, 513648 B, 3 pp | **refuse** — the registered span elides the statutory parenthetical; only the suffix is contiguous. Flip: quote §1（ア）'s full clause verbatim, after a lane row exists (`grep -c 府連 corpus/SOURCES.md` → 0) |
| S048 GB record | `unreachable` | **404** (748 B) | **unreachable** — no quote was recorded, so nothing is testable; never a fabrication |
| S065 法律目录 PDF | `unreachable` | 200, 7465472 B | **reachable today, no recorded span** — class that describes today's fetch is `reachable`; `payload-present/absent` cannot be adjudicated without a located span |
| S068 GB record | `unreachable` | **403** (465 B `Access Denied`) | **unreachable** — host refuses the instrument UA |
| S069 / S070 | `unreachable` | 200, **0 B** (same URL twice) | **unreachable in substance** — empty body; the register holds two rows for one source |

Net disposition: **0 adopted, 2 refused, 5 unreachable**. Blast radius inside the lane: **0** —
all seven staged entries that cite these ids are absent from `corpus/knowledge/`
(`wave1/ScribeAssimilationGate.md` §1).

### Id-collision check — re-run, guard shown load-bearing

`reg_ids=51 staged_ids=94 collisions=21 collision_range=S031..S051` (51-row registry
`4c85ff86…`; the 94 staged ids are `S031`–`S124` in the package's 67 knowledge files). At the
50-row moment the same command read `collisions=20 S031..S050`, and the committed
`.ufo/waves/round-34/assimilation/{reg-ids,staged-ids,collisions}` are the pre-S051 derivation
(`ecc9c3b9…`/`550a0129…`/`dcfd73c7…`). Guard sensitivity: an indented `S031` row is caught by the
0–3-space pattern and missed by the column-0 pattern (1 vs 0). Fixed-id examples that make
adoption-by-number impossible: staged `S044`/`S045`/`S046` are 最高人民法院 2011 解释 / 刑法 2023
修正 / 南京市检察院 指南, while lane `S044`/`S045`/`S046` are Bugcrowd VRT README / Bugcrowd VRT
CWE mapping / IPA JVN activity report. **Adoption is by document, never by number.**

### Assimilation: none adopted

`grep -rliE 'immunefi|vscs|web3'` over the package's 67 knowledge files → **0 files**, so F17/S051
cannot unblock any refused entry and is not an assimilation candidate. No staged entry's flip set
is fully met (table above; two independent runs, before and after the S051 landing, print the same
values). No new refusal opened and no prior refusal lifted.

### The junk-twin control — committed, and its rejection is contested

The frozen C2 clauses say the twin is "rejected by the admission gate (source-recheck exit != 0;
reviewer REFUSE)" and list "junk twin passes source-recheck or is admitted" as a C2 kill.
Committed state: `.ufo/waves/round-34/c2-controls/junk-f17.md` (`2752a994…4026`) is in the freeze
commit (`git ls-tree 29f606d` → `junk-f17.md` blob `50f7a84c`), absent at base, and the shape-only
checker passes it `3/3` by design (`wave1/RevC2BeforeAfter.md` §8).

Two readings are on record and **they disagree**; both are reproduced verbatim here because the
canonical judge, not this lesson, resolves them:

- **Holds (reviewer).** `wave1/RevJunkTwin.md` verdict: "the junk-twin control holds. All four seat
  criteria verified by execution" — the twin's asserted sentence, built into a control manifest and
  checked against the committed capture, prints `S051:J1 MISMATCH reason=quote-not-found`,
  `junk_recheck_exit=1` (§3), and the F17 review does not admit the junk bytes (§4). Same
  demonstration independently: `wave1/RevC2BeforeAfter.md` §8 (`quote-not-found`, exit 1),
  `wave1/ExecDoNothingReject.md` §3 (`junk-sentence` `MISMATCH`, exit 1).
- **Does not hold as frozen (critics).** `wave1/CritOverclaim.md` F1: "the junk-twin rejection limb
  is false as frozen; the twin passes its own recheck at tip" — the twin's `recheck:` line is
  byte-identical to the real entry's, so both exit **0**; `source-recheck` never accepts a markdown
  file, so "exit != 0 on the twin" only reproduces by handing it a non-manifest (any file yields
  exit 2 — non-discriminating); and "no reviewer REFUSE for `junk-f17.md` exists in `wave1/` at
  read time". `wave1/CritC2Kill.md` G5 reaches the same conclusion: "so 'junk twin rejected' is
  true for the committed twin against the committed capture, and false in general".
  `wave1/ScoutDatawalk.md` F-1: "junk-twin rejection has no executable form as phrased"; F-1b: the
  twin is a **mixed** control — `grep -c 'Direct theft of any user funds' S051.txt` → **1**, so one
  of its two "fabricated" sentences is true and only `five severity levels for smart-contract
  exploits` is absent (`grep -c` → 0).

What the round can state without adjudicating: the twin is committed, the shape counters pass it,
and the fabricated **sentence** is rejected against the committed capture by three independent
runs. What the frozen wording additionally asserts (a rejecting `source-recheck` invocation of the
twin's own line, and a reviewer REFUSE receipt naming the twin) is not demonstrated on disk at
composition time.

## Mistakes

Numbering follows `claims.json` `non_claim_frontier_items.mistake` M34-1 and M34-2. Rows marked
**provisional** are minted by this lesson from wave receipts; the frozen claims own the numbering,
so the L1 must file them as a separate appended erratum before they are cited as ids (the
`claims-erratum-1.md` form). Field schema is round 33's: class · evidence pointer · captured-by ·
fix · fix shown able to fail.

- **M34-1 — the round-33 report said "all mutants killed" while the frozen kill rule caught 3 of 4.**
  Class: overstatement / summarization past measured evidence. **Evidence:** `MutCtrSelftestSkip.md:63,68`
  prints `selftest cases=0 failures=0` exit 0; `MutCtrUnbound.md:136,212` headlines **SURVIVOR**;
  routed as `corpus/lessons/round-33-verifier-spotcheck.md` §5 R4. **Captured by:**
  `MutCtrSelftestSkip` and `MutCtrUnbound` — the two seats whose receipts held the truth while the
  report summarized past them (`wave1/CritMistakes.md` F3 corrects the frozen claim's
  `captured-by: R13`, which is a criterion, not a seat; the criterion missed is R13). **Fix:**
  `corpus/instruments/kill-rule-check.py` — replays each mutant against the landed instrument bytes
  and prints `mutants=3 killed=3 survivors=0 invalid=0` plus six/seven `GATE ok` lines and a
  do-nothing-control rejection. **Able to fail, measured:** the same counter replayed against base
  bytes prints `survivor` for `skip-selftest-summary` (`killed=0`) and `survivors=1`
  (`wave1/RevC1BeforeAfter.md` §3); its `CTL-equivalent` control is reported as a survivor with
  `witness_survivors=1 witness_exit=1`, and the fake runner is rejected `opaque … differs=1`
  (`wave1/ExecKillRuleCheck.md` §3, `wave1/ExecDoNothingReject.md` §2). Caveat the row keeps: the
  red-before is the *old rule's receipts*, not a re-run of the old prose rule.

- **M34-2 — `<LANE_HASH>` placeholders were filed in `SCORECARD.md`.** Class:
  landing / reference-drift. **Evidence:** base `SCORECARD.md` carries 2 (at `:988`, `:1087`);
  routed as `round-33-verifier-spotcheck.md` §5 R1. **Captured by:** `none` **as a defect** — the
  markers were recorded as an intended L1 handoff at `corpus/lessons/round-33.md:7,17,126`, so no
  seat treated them as drift; first filed as a defect by the round-33 verifier R1
  (`wave1/CritMistakes.md` F2 falsifies the bare `captured-by: none`). **Fix:**
  replacement with `7963976e60b2564860553c6ab4838128d5ca06ea` ×3 plus an appended
  `Correction (round 34)` naming the lane tip `014ee2d7…` (`wave1/ExecScorecardMarkers.md` §2–§4,
  absorbing `ExecErratum2`'s +23-line insert; `SCORECARD.md:1116-1119`). **Able to fail:**
  `grep -c '<LANE_HASH>' SCORECARD.md` reads 2 at base and 0 at tip (suite R1 `open=1` at base,
  `open=0` at tip). **Sweep still owed:** the token survives twice in `corpus/lessons/round-33.md`
  and once (legitimately, as the finding's own quotation) in
  `corpus/lessons/round-33-verifier-spotcheck.md`; `:126` still says the markers are unfilled, so
  the C1-scoped count (0) is not a repo-wide count. `wave1/RevErrata.md:44`'s "none in
  `SCORECARD.md` or any `corpus/` production file" is false as written.

- **M34-3 (provisional, minting required) — a post-freeze counting-literal erratum was filed eight
  minutes after the round froze a criterion that forbids exactly that, and the criterion cannot see
  it.** Class: freeze satisfiability. **Evidence:** `claims-erratum-1.md` mtime `02:36:22` vs freeze
  commit `02:28:39` (`+7m43s`, `sha256 6a3cd99e…`); `corpus/QUALITY.md:226` (R22) requires each
  literal to be evaluated **against base bytes**; `records=40` was true at base
  (`git diff --stat 7963976e 014ee2d -- corpus/source-snapshots corpus/instruments corpus/SOURCES.md`
  prints nothing — base and freeze audit surfaces are identical) and false on arrival at 41. Second
  instance, unfiled: the C2 predicate/after text carries `PASS F17 ids=S051`, which greps **0** in the
  harness output (the column-padded line is `PASS     F17  … ids=S051           exit=0`); measured by
  `wave1/ScoutDatawalk.md` F-4a and `wave1/RevC2BeforeAfter.md` §5. **Captured by:**
  `wave1/CritMistakes.md` F5 (R22-vs-erratum-1 pairing) and `wave1/ScoutDatawalk.md` F-4a (harness
  literal). **Fix (not landed by this seat):** add R22's planned-state limb — evaluate each literal
  against base **+ the round's declared after-adds**; reword the C2 after-list to the printed column
  truth. **Able to fail:** base-only R22 accepts `records=40` (`diff` empty) while the planned-state
  test rejects it (`records=41`); `grep -c 'PASS F17 ids=S051'` on the harness output → 0 while the
  F17 line is present. Constraint: this row must be minted in a **separate appended file** (frozen
  claims own numbering) before any surface cites `M34-3`.

- **M34-4 (provisional) — the new closure suite's first version could print green while measuring the
  wrong tree.** Class: own-instrument false green. **Evidence:** author self-report,
  `wave1/ExecRDefectClosureSuite.md` §11.2: (a) the selftest's live run reused `$RD_ROOT` after the
  fixture run reassigned it, so cases 2–9 measured the previous fixture tree; (b) the first R9
  reverse fixture also tripped `selection-not-cited-by-entry`, which the base instrument already
  enforces, so it would have read "bidirectional" against base. **Captured by:** the author seat
  itself, before freezing. **Fix:** capture `live_root` once before the loop; rebuild the fixture to
  cite both ids in prose. **Able to fail, measured:** the landed R9 reverse fixture gives landed
  `reverse_exit=1` with `problems=selection-not-declared-by-entry` and base `base_reverse_exit=0`
  (§7); the suite reads `closed=0/9` on base and `9/9` at tip (§5).

- **M34-5 (provisional) — one receipt declares "no git/jj mutation" while its own `jj log` calls
  created working-copy snapshots.** Class: overstatement (M34-1's class). **Evidence:**
  `wave1/SentScopeFinal.md` §2 B2–B3: four `snapshot working copy` ops (`3038db8e52bc`
  `ScoutQuarantine`, `1c80be616d4b` `ScoutDatawalk-2`, `497fe0c449c0` `RevErrata`,
  `2d099a7898ec` `RevClaimsFreeze-2`), all lacking `--ignore-working-copy`; `RevErrata.md:12,153`
  deny any jj mutation. **Captured by:** `SentScopeFinal`. **Fix:** append an erratum to the
  receipt naming the two jj reads, and use `jj --ignore-working-copy` (or no jj) in seats.
  **Able to fail:** `jj --ignore-working-copy op log` shows the four ops against the L1's own
  `snapshot.auto-track="none()"` operations; the seat's own two reads at +5 min returned the same
  top op `3038db8e52bc`, so the check is stable.

- **M34-6 (provisional) — one seat wrote outside its write scope twice, by relative-path
  resolution.** Class: write-scope drift. **Evidence:** `wave1/CritC1Kill.md` "Seat hygiene
  (self-reported defect, corrected)": its first receipt write resolved against the session
  workspace root and landed at `/home/vgpnk/Projects/shokunin/.ufo/waves/round-34/wave1/` (fleet
  root), copied byte-identically (`sha256 ab80628c…`) into the lane and the stray deleted. Separate
  and still on disk: `baseline-plain.txt` at the fleet root (`850 B`, `sha256 56f08a92…`, mtime
  `02:37:04`) and `selftest-baseline.txt` at the lane root (`1552 B`, `sha256 ca3759d1…`), both from
  one seat command captured in `~/.omp/agent/sessions/…/RevKillRule.jsonl` and attributed by
  `wave1/SentScopeFinal.md` §1 A1 (the lane-root stray is also `wave1/CritOverclaim.md` F4 and
  `wave1/RevC1BeforeAfter.md` F5). **Captured by:** `SentScopeFinal` (and `CritOverclaim`/`RevC1BeforeAfter`
  for the lane-root file). **Fix:** absolute paths under the seat scratch; both strays disposed of
  before the integration commit. **Able to fail:** `git -C /home/vgpnk/Projects/shokunin status
  --porcelain` lists `?? baseline-plain.txt`; `git ls-files --error-unmatch selftest-baseline.txt`
  in the lane → not tracked; both commands read 0/none once the files are removed.

Word sweep this section rests on — `for w in BLOCKED DEFECT SURVIVOR survivor FAIL traceback; do
printf '%-10s files=%s hits=%s\n' "$w" "$(grep -l "$w" *.md | wc -l)" "$(grep -o "$w" *.md | wc -l)"; done`
over the receipts present at composition:

```
BLOCKED    files=0   hits=0
DEFECT     files=0   hits=0
SURVIVOR   files=3   hits=10
survivor   files=18  hits=237
FAIL       files=29  hits=157
traceback  files=0   hits=0
```

The three `SURVIVOR` files are `wave1/CritMistakes.md`, `wave1/ExecBeforeReceipts.md` and
`wave1/ExecLessonErrata.md`, all quoting the round-33 survivor receipts rather than reporting a
live one; `FAIL` (157 hits) is dominated by fixture and gate output and was **not** read line by
line. This is a word sweep, not a review: § Mistakes is the list of events this seat opened.

## considerthese

`considerthese/2026-10-25.md` proposal 6 ("Event-driven reflections", `:76`) is **mined → landed**
as `corpus/QUALITY.md:227` **R23**: "A lane records an event-driven reflection cadence: burst
activity and idle stretches are reviewed within the next round's lesson, citing the considerthese
file and date. Grounded in: considerthese/2026-10-25.md proposal 6." Landed by
`wave1/ExecQualityAppends.md` §2 (append at EOF, byte-prefix proof that lines 1–213 kept their
numbers).

The landed row is **narrower than the drafted criterion**: `wave1/ScribeQualityDraft.md`'s block
required the lesson to state each proposal's disposition ("mined into a named path, declined, or
unchanged with the reason … a proposal left `open` through consecutive lessons with no disposition
line is a cadence failure"), while `corpus/QUALITY.md:227` requires only "citing the considerthese file and
date" (`wave1/CritOverclaim.md` F8). The narrowing is recorded here rather than corrected in place
(the bar is append-only); this paragraph is the disposition line the draft asked for, and a future
round may restore the limb.

Dispositions of the other five proposals (from the lane's own ledger, not assumed):

1. *Cap wave-evidence bloat* — **mined round 28 → R14**, and measured again this round: `.ufo/waves/round-34`
   holds **1,166,898 B in three planner artifacts** (`wave1-spec.json` 370,733 + `wave1-dispatch.json`
   398,451 + `wave1-plan.out` 397,714) out of **2,421,531 B** for the whole wave directory (48.2 %),
   with 61 receipts at 1,114,510 B (46.0 %) — measured by this seat at composition with `du -sb` /
   `wc -c`; the 53-receipt moment was 2,255,164 B / 51.7 % / 948,143 B, i.e. the receipts grow and the
   planner share shrinks as seats land. **0** `/corpus/` paths and **0** scratch trees sit inside the
   committed set.
2. *Track distance to the next score* — `mined round 31`; no `score-gap.py` run this round and no
   receipt claims one.
3. *Bounty craft / SHONEN box 2* — `partially landed`: F17 adds a Web3 severity ladder (a craft
   surface the lane did not hold), but no hunt-to-claim pipeline; `SHONEN.md` is
   `ScribeShonen`'s seat this round.
4. *Proposal status ledger* — `mined round 30` into `corpus/knowledge/considerthese-proposals-ledger.md`;
   unchanged.
5. *Open-defects ledger with runnable closure checks* — `mined round 29 → R15`, and this round is
   the largest application of it: R1–R9 each carry a runnable check inside
   `corpus/instruments/r-defect-closure.sh`, and `closed=9/9` is itself the ledger's read.

## Census before → after

- **Before** (`.ufo/waves/round-34/census-before.txt`, frozen at claims time, `sha256 d90ce017…`):
  `kasegi W04 S028 duplicate url docs.hackerone.com/…`, `kasegi W04 S029 duplicate url
  eur-lex.europa.eu/…`, `kasegi ok …/corpus/SOURCES.md`, `census_exit=0`; plus the six contract
  values it records for the C1/C2 surfaces (`rows=50` implied by `S051 rows 0` and the C2 block;
  `frontier_admitted=16`; `knowledge entries=45`; `harness entries=19 pass=19 exit=0`).
- **After** (this seat's run at `2026-10-26T05:49Z`; independently `wave1/RevCensus.md` §1–§2,
  `wave1/RevC2BeforeAfter.md` §7, `wave1/ExecRegressionC2.md` §3, and
  `wave1/ExecCensusAfter.md` §2–§5, which fired its quiescence predicate at `05:48:31Z` over the
  same byte set):

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

Same three lines, same exit, no new `W`, no `E` line. `ExecCensusAfter` reports the same contract
counters on its quiescent bytes (`rows=51 s051=1 front=17 citing=1 know=46`, quoted at its `:291`).
Counters on this seat's bytes: frontier 17,
registry rows 51, `S051` rows 1, entries citing S051 1, knowledge entries 46, harness
`entries=20 pass=20 exit=0`, `source-recheck S051` exit 0 (18 assertions; Q9/Q17 `occurrences=2`
anchored), `capture-binding` `records=41 bound=41 unbound=0` exit 0.

## No-harm

Measured by this seat at composition (`2026-10-26T05:48–05:52Z`) on the wave-1 working tree; the
assigned no-harm seats (`ExecNoHarmFinal`, `ExecRegressionC1`) had **not** filed at that moment, so
this table is the lesson's own measurement plus `wave1/RevNoHarm.md` (an earlier snapshot, `02:31–02:38`)
and `wave1/SentScopeFinal.md` (scope axes, `02:44`).

| Instrument | Before (base `014ee2d`) | After (wave-1 tip) | Verdict |
|---|---|---|---|
| `density.py SKILL.md` | mean dens **201.7** (710 cites / 25 blocks, `exit=0`) — measured by this seat on a `git archive 014ee2d` tree | mean dens **201.7** (710 cites / 25 blocks, `exit=0`) | Unchanged, because `SKILL.md` is untouched (absent from the numstat below). `wave1/RevNoHarm.md` §C reports the same 201.7/710/25 |
| `anchorcheck.py SKILL.md` | 12 in-range cites, **0 bad**, `LOST-RECORDED=306`, `PIN-BROKEN=0`, `ORIGIN=0`, `OUTSIDE-BASE=0`, `BASE-ABSENT=0`, `exit=0` | identical: 12 in-range, **0 bad**, all failure classes 0, `exit=0` | No failure class moved. `LOST-RECORDED=306` is the recorded-not-fail class |
| `git diff --numstat 014ee2d` | — | `SCORECARD.md 31 3`; `corpus/instruments/capture-binding-check.py 487 87`; `frontier-recheck-count.py 220 15`; `instruments/README.md 291 0`; `lessons/round-29.md 74 0`; `lessons/round-33.md 109 0`; `QUALITY.md 15 0`; `README.md 26 0`; `SOURCES.md 5 0`; `round-26/manifest.json 12 1`; `round-32/manifest.json 3 3`; `SKILL.md`/`PROVINCE.md`/`LOG.md` absent (0) | Corpus records append-only; the 109 deletions are the C1-mandated marker removals, instrument hardening and manifest data corrections (classified line-by-line in `wave1/RevNoHarm.md` §A) |
| unowned writes | — | lane root: `?? selftest-baseline.txt` (1552 B, `ca3759d1…`, mtime `02:37:05`); fleet root: `?? baseline-plain.txt` (850 B, `56f08a92…`, `02:37:04`); ` M .ufo/waves/round-33/wave1/ScribeReportDraft.md` (37/0 append); 4 jj working-copy snapshots | **Three findings**, all attributed: the two root strays to one command captured in the `RevKillRule` transcript (`wave1/SentScopeFinal.md` §1 A1), the round-33 receipt append to `RevKillRule`/its author, the jj snapshots to four seats (`wave1/SentScopeFinal.md` §2 B2). Out-of-lane write by `CritC1Kill` self-reported and deleted. Sentinels: fleet root **FAIL (1 file)**, lane git/jj **FAIL (4 snapshots + 1 false claim)**, shokuknow **PASS**, scratch **PASS at snapshot** |

Instrument digests moved **during** this lesson's composition, twice for two files
(`r-defect-closure.sh` `0beafed2…` → `357a7e49…` → `2a635bf5…`; `SCORECARD.md` `b8fc8c66…` →
`efa646c8…` when `ScribeScorecard` appended the round-34 section; `kill-rule-check.py` `7a20e724…`
→ `c279d952…` and its gate count 6 → 7). `wave1/CritOverclaim.md` F3 records the same class one
step earlier (`closed=8/9` at `05:38Z`, `closed=9/9` at `05:40Z`). So **any after-value must be
quoted with its digest**, and the L1 must re-run at quiescence:

```
last read 2026-10-26T05:54:57Z (counters re-run at these bytes)
2a635bf5…dcfc  corpus/instruments/r-defect-closure.sh        closed=9/9 exit=0; selftest cases=9 failures=0
c279d952…5d61  corpus/instruments/kill-rule-check.py         mutants=3 killed=3 survivors=0; gates=7 failed=0
3d9e5e0d…99fa  corpus/instruments/capture-binding-check.py   selftest cases=23 failures=0; records=41 bound=41 unbound=0
1be79af6…8249  corpus/instruments/frontier-recheck-count.py  entries=20 pass=20 exit=0
efa646c8…7e91  SCORECARD.md           77d99df9…1af8  corpus/QUALITY.md
4c85ff86…77b6  corpus/SOURCES.md      876be9cc…6f29  corpus/README.md
f69472f3…8807  corpus/lessons/round-33.md
72ab4e68…8eb6  round-32/manifest.json  d5077f81…eebe  round-34/manifest.json  33ac33c3…cefa  round-26/manifest.json
948b202e…c1d8  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
2752a994…4026  .ufo/waves/round-34/c2-controls/junk-f17.md
dedb9ea8…0850  .ufo/waves/round-34/claims.json (byte-identical to the freeze commit)
```

## Open items / unverified

1. **`LANDED_HASH_PENDING`** = the L1's integration commit `4b0a9f29a8797828fb711faed80ee151afdf5117`. Nothing else in this
   file is a placeholder.
2. **Twelve seats had no receipt** at composition (list in the header). Three of them own numbers
   this lesson therefore measured itself and not from a receipt: census-after
   (`ExecCensusAfter`), the no-harm final battery (`ExecNoHarmFinal`/`ExecRegressionC1`), and the
   survivor-counter review (`RevKillRule`, `MutRSuiteChecks`, `MutFrontierRuleA`, `MutC2Entry`,
   `CritBoundary`). `ExecRegressionC2`'s final battery did land and agrees with this lesson's C2
   numbers.
3. **Instrument digests are in-flight.** `r-defect-closure.sh` and `kill-rule-check.py` both moved
   after `RevC1BeforeAfter`'s `05:39Z` batch (`7aca98b3…` / `1af15e59…` → `357a7e49…` / `c279d952…`,
   and the gate count 6 → 7). The L1 must re-run the three C1 commands on the integration bytes and
   quote them with the committed digests; a `9/9` quoted from a mid-wave read is unfalsifiable.
4. **C1's four surviving routes** (`wave1/CritC1Kill.md` § Verdict, "3 leave the kill rule satisfiable
   without the property it certifies"): summary-only suite (1c), forged `survivors=0` with a
   probe-invisible mutant (3b), fabricated/non-instant `fetched_utc` accepted by R8 and the
   instrument (4a/4b), and an all-orphan directory printing `records=0 bound=0 unbound=0` exit 0 (5),
   plus `R1` spelling brittleness. Each has a named deterministic correction; none landed this round.
   The lesson therefore records C1 as **held**, not increased.
5. **C2's gate is not provenance-sound** (`wave1/CritC2Kill.md` § Verdict, G1–G5): a fabricated
   capture with a self-consistent manifest passes every C2 counter (17/51/1/1, harness 20/20,
   `source-recheck` exit 0, `capture-binding` 41/41); a fabricated entry body passes too
   (harness binds ids only; `anchorcheck` sees 0 cites because the entry's anchors are not
   backticked); an uncited mined row with no capture passes census and `capture-binding`; harness
   rule D can leave the tested root via the entry's absolute `cd`. C2's **evidence** this round is
   real (two independent live re-captures byte-identical), its **gate** is what the gaps name.
6. **The junk-twin limb is contested** (§ Gate): reviewer `RevJunkTwin` holds; critics
   `CritOverclaim` F1/F1b, `CritC2Kill` G5 and `ScoutDatawalk` F-1/F-1b say the frozen wording is
   not executable and the control is mixed (`Direct theft of any user funds` occurs once at
   `S051.txt:75`). The canonical judge resolves; this lesson does not.
7. **"Every assertion occurrences=1" is false as worded** (`CritOverclaim` F2, `RevC2BeforeAfter` §6,
   `ScoutDatawalk` F-2): 16 assertions are `occurrences=1`, Q9 and Q17 are `occurrences=2` with
   verified anchors at L77/L96. The exit status and the sha256 hold either way.
8. **`PASS F17 ids=S051` is not a grep-able literal**; the printed line is column-padded. The
   predicate's literal and the after-list's ellipsis form differ from the output.
9. **`records=40` vs `records=41`** is ruled by `claims-erratum-1.md`; its disclosure duty is now
   discharged in the round-34 SCORECARD section (`:1149-1152`) appended by `ScribeScorecard` during
   composition. It was **not** visible when `RevC1BeforeAfter` measured (F2), so any reader who
   stopped at that receipt's timestamp still owes the re-read.
10. **M34-3 and M34-5/M34-6 are provisional** and must be minted as a separate appended erratum
    (the frozen claims own numbering); M34-4 is minted by this lesson from the author's own
    disclosure. Until that erratum lands, `corpus/QUALITY.md:226` cites M34-2 as R22's grounding
    while M34-2 is the marker defect (`wave1/CritMistakes.md` F7) — the correct grounding is M34-3.
11. **The junk twin is committed but its label is internally false**: `c2-controls/junk-f17.md:16`
    is a true substring of the capture and `:17` calls the block fabricated
    (`wave1/CritOverclaim.md` F1b, `wave1/ScoutDatawalk.md` F-1b). Fix the label or drop the line
    before citing it as a control again.
12. **Stray files still on disk at composition**: lane `selftest-baseline.txt` (untracked) and fleet
    `baseline-plain.txt` (untracked, out of scope). Both must not ride into the integration commit;
    the lane one is also the evidence `RevC1BeforeAfter.md:37` cites for the 23-case baseline, so
    deletion after the commit is safe (the count is quoted inline in that receipt).
13. **Anchor drift deepened** (`wave1/RevRowS051.md` §7): the 5-line `SOURCES.md` append moves
    `## Paths` 58→59, `## Search log` 65→66, `## Leads` 77→79, `## Registry changes` 83→85; the
    stale `SOURCES.md:83` citation trail (`corpus/lessons/round-29.md:214`,
    `round-29-verifier-spotcheck.md:74`) was +7 and is now +9. Routed to `corpus/lessons/**`, not
    fixed here (R6 forbids moving cited lines in place).
14. **Currency**: the S051 re-opens are three single-instant fetches on one host
    (`05:33:38Z`, `05:35:45Z`, `05:42:46Z`); byte-identity across them says nothing about the page
    before or after, and the v2.2-vs-v2.3 selection rule the round brief asked about is an open item
    in the entry, not a finding.
15. **This lesson's § Mistakes is a word sweep plus opened receipts, not a completeness claim**;
    the `FAIL` token appears in fixture output across receipts and was not read line by line.
16. **One C2 anchor mutant survives** (`wave1/MutC2Entry.md` § Mutants, M3b): moving manifest Q9's
    `anchor` from 77 to 62 still exits 0 (`occurrences=2 anchor=62-ok`) because
    `Permanent freezing of funds` genuinely occurs at both `S051.txt:62` (Blockchain/DLT table) and
    `:77` (Smart Contracts table). The anchor therefore pins *a* line holding the quote, not the
    intended occurrence — a coverage limit of the Q9 anchor limb, not a defect in this entry
    (which cites L77 and discloses the pair). It is not routed as a defect here; it is named so a
    future round can decide whether Q9 should require the anchor to be the cited line.

## Touched surfaces and provenance

This lesson's only production path is `corpus/lessons/round-34.md`; the scoped seat report is
`.ufo/waves/round-34/wave1/ScribeLesson.md`, which holds the commands, their output, exit codes and
file digests. Evidence paths are named inline, principally
`.ufo/waves/round-34/{claims.json,claims-erratum-1.md,census-before.txt,c1-controls/*,c2-controls/*,assimilation/*,wave1-spec.json,wave1-dispatch.json,wave1.ready}`
and `wave1/{ExecRDefectClosureSuite,ExecCaptureBindingHarden,ExecKillRuleCheck,ExecFrontierBidirectional,ExecManifestR32Normalize,ExecS040Orphan,ExecLessonErrata,ExecErratum2,ExecQualityAppends,ExecScorecardMarkers,ExecRegistryAppend,ExecSnapshotR34,ExecHarnessAfter,ExecDoNothingReject,ExecRegressionC2,ExecBeforeReceipts,RevC1BeforeAfter,RevC2BeforeAfter,RevRSuite,RevEntryF17,RevRowS051,RevClaimsFreeze,RevErrata,RevNoHarm,RevCensus,RevJunkTwin,RevManifestR32,RevOrphan,MutKillRuleMutants,MutSelftestSummary,MutManifestField,MutCaptureBindingLimbs,CritC1Kill,CritC2Kill,CritOverclaim,CritMistakes,ScoutImmunefiLive,ScoutDatawalk,ScoutQuarantine,ScoutPackageThemes,ScoutSiblingSweep,ConnClaims,ConnCrossCheck,ConnSibling,ScribeEntryF17,ScribeSOURCESRow,ScribeSearchLog,ScribeSkillGate,ScribeQualityDraft,ScribeAssimilationGate,SentCred,SentScopeFinal}`.
No claim in this file rests on a file this seat did not open; the twelve absent seats are named
where their numbers would otherwise have been cited.

## L1 integration appendix (appended 2026-10-26, after composition)

The L1 (`KasegiR34a2`) landed the round on top of this lesson's working tree; everything below is
additive to the composition above, no earlier sentence is rewritten.

- Integration commit `4b0a9f29a8797828fb711faed80ee151afdf5117` (round-34: all wave evidence,
  instruments, corpus additions, claims/erratum files).
- L1 re-ran every frozen counter on the integrated bytes before the commit; full receipt
  `.ufo/waves/round-34/wave1/L1Integration.md` (+ raw output `L1Integration.raw`): suite
  `closed=9/9 exit=0`, `--selftest cases=9 failures=0`; capture-binding `--selftest cases=23
  failures=0`, plain `records=41 bound=41 unbound=0 exit=0`; kill-rule
  `mutants=3 killed=3 survivors=0`, `gates=7 failed=0`, `survivors=0`; frontier `17`, registry
  rows `51`, S051 rows `1`, entries citing S051 `1`; harness `entries=20 pass=20 exit=0`;
  source-recheck S051 exit 0; `<LANE_HASH>` count 0; census exit 0 (W04 S028/S029 only);
  `recheck-audit.py` `strict pass=46/46` and `expect=present expected=46 missing=0 unexpected=0
  exit=0`.
- L1 production edits beyond the seats' work (all end-of-file appends or new files):
  `PROVINCE.md:75` F17 frontier amendment (the SHONEN box-4 "owed" item); `SKILL.md:1091`
  round-34 re-verify correction (the SHONEN box-1 "open, not closed" item);
  `corpus/instruments/knowledge-expected.txt` synced to 46 entries (F17);
  `corpus/QUALITY.md:229` R25 (planned-state satisfiability, grounded in M34-3);
  `.ufo/waves/round-34/mistakes-erratum-1.md` minting M34-3/M34-5/M34-6; the strays
  `selftest-baseline.txt` (lane root) and `baseline-plain.txt` (fleet root) confirmed absent at
  integration (M34-6 fix). Post-append no-harm: `density.py SKILL.md` mean 201.2 (base 201.7,
  no score move claimed), `anchorcheck.py SKILL.md` exit 0, 0 bad.
- Wave receipt census at round end: 65 spec names; 65 receipt files present in `wave1/` with one
  name-vs-file swap (`ScribeReportDraft-2.md` supplements `ScribeReportDraft.md`) and one missing
  name (`ExecRegressionC1.md` — dead seat 1 of 65; covered by the L1 regression re-run above and
  `ExecRDefectClosureSuite.md` §5, base `closed=0/9` exit 1). No `wave1-results.json` exists:
  attempt 1 ended before the dispatcher finalized results, so receipts are the evidence.

**Post-commit erratum (appended 2026-10-26, after the integration commit):** the missing receipt
`wave1/ExecRegressionC1.md` landed at `2026-10-26T06:16:16-06:16:29Z` — after the integration
commit — and is committed in the follow-up commit. It re-runs the six frozen C1 counting commands
verbatim at a quiescent input digest (`6ed34f48…`, stable from 06:04:29Z): all six match the
frozen literals (command 6 `records=41 bound=41 unbound=0 exit=0` under erratum 1), the suite
fails on base bytes (`base_exit=1` at `014ee2d`), and the repeat-run triple is byte-identical.
The round therefore closes with 65/65 receipts filed (the name-vs-file swap noted above
unchanged).
