# Round 30 — kasegi

Lane: `kasegi-shokunin`. This lesson reports working-tree evidence, not a commit-level or canonical judge decision. Revisions: base `a94871315cafa368f79c17d8c62d71fddd967986`; claims-freeze commit `3c5573541300ba0fd3d89372dda3d841172eaa3f`; wave-1 spec/dispatch commit and HEAD at measurement `002e92ce07ed398334ef7cd8ca08d3fd99631351`; final landed integration commit is **not available in the inspected evidence**. `ScoutDatawalk.md` confirms base is ancestor of freeze; `ExecBeforeVerify.md` confirms freeze receipts are byte-identical and authentic.

Shape: one v2-policy wave, `kasegi-r30-build`, 64 seats spawned, resume 0 (`wave1-dispatch.json`, counts 64/0/64). Declared role counts from the spec/registry: scout 6, connector 4, executor 15, scribe 13, reviewer 10, critic 4, mutation-tester 4, sentinel 2, revenger 1, simplifier 1. The execution roster uses generic role labels and registry `agentId` fields are null; the authoritative executed model/attack role mix is not evidenced in inspected artifacts. Therefore m_flash majority and attack-role ≥25% are **unverified**, not inferred from role labels. Axes: depth:verifiability (4) and coverage (7); frozen saturation 9/10, window N=3.

Answering model on seat receipts: `inception/mercury-3` (config route table; no model passed). No tools installed or upgraded; no pacman transaction.

## Frozen claims — before → after

| Claim | Axis | Before (freeze receipts) | After (settled working-tree receipts) | Verdict / boundary |
|---|---|---|---|---|
| C1 | depth:verifiability (4) | A1 exit 1 traceback, no row marker; A2 exit 0/pass=2 duplicate; B1 exit 0 despite stem mismatch; B2 exit 0 with occurrences=2 and no anchor (`c1-controls/before.txt`) | A1 exit 1 names F98/path as `missing-entry`; A2 exit 1 names duplicate F98/F97 realpath; B1 exit 1 `reason=stem-mismatch`; frozen B2 exits 1, but for the same stem-mismatch (B1 fires first), not the occurrence limb. Selftest 9/9, exit 0. All 34 previously passing manifest source rechecks (rounds 23–29) and round-30 source rechecks pass; real frontier harness 17/17, exit 0. Digests: frontier `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893`; source checker `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f`. | Instrument behavior improved; score held 4. Overall frozen kill rule is not fully robust: B2 frozen counter is non-isolating and mutant-B2 does not flip on it. Its generic failure-reason clause is satisfied by B1 instead. Correctly report improvement with this strict discrimination caveat, not an unconditional C1 pass. |
| C2 | coverage (7) | Frontier 13; entries citing S046/S047 0; total registry 45; census exit 0; harness 16/16, exit 0 (`c2-controls/before.txt`, `census-before.txt`) | Frontier 14; exactly one knowledge file cites S046/S047 (F14); two new source rows; registry 47; census exit 0 (W04 S028/S029 warnings only); harness entries=17 pass=17 exit=0; S046/S047/S041 rechecks exit 0. Manifest `dfc8835750bbdcbc2480fc579f7204ba8215d3018d0bd0942e4ea97f3e5e75a6`; F14 entry `f584f06c74942a36d9bce6bb97adcb7ab3bd1b2b0503faf8a68d5c60f4494a32`. | Target predicates met at measured working-tree bytes; score held 7. No final integration-commit recheck evidenced. |

Frozen C1 instrument hashes: `c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261` and `9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96`. The before receipts and control results are reproducible on an isolated freeze export (`ExecBeforeVerify.md`).

## Landed changes

- `corpus/instruments/frontier-recheck-count.py`: named fail-closed missing-entry error and duplicate-entry realpath rejection. A1/A2 both discriminate on fixed bytes; mutant-A1/A2 flip. Settled digest above.
- `corpus/instruments/source-recheck.py`: capture path stem must equal record id; repeated normalized quote requires a verified anchor; selftest covers stem, unanchored/anchored duplicates, invalid anchors. Settled digest above. B1 mutant flips. B2 limb is implemented and supplementary same-stem fixture flips mutant-B2, but the committed B2 fixture itself is confounded.
- `corpus/source-snapshots/round-30/{S046.txt,S047.txt,S041.txt,manifest.json}`; `S041.txt` is byte-identical to the round-28 capture. S046 and S047 were captured with `capture-source.py`; no curl fallback. Manifest binds 12 assertions and capture digests.
- `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` (F14), `corpus/SOURCES.md` (S046/S047 append + R8 log), `corpus/README.md` (append-only F14 frontier and coverage-map entries), `corpus/instruments/knowledge-expected.txt` (43 entries after F14 + proposals ledger), `corpus/knowledge/considerthese-proposals-ledger.md`, and append-only `SKILL.md` gate registry entry. `SCORECARD.md` has round-30 result/move-log; round 30 `LOG.md` entry was not found in the inspected files.
- Wave artifacts include `.ufo/waves/round-30/harness-after.txt`, `post-commit-recheck.sh`, `c2-after.txt`-equivalent report `wave1/ExecCensusAfter.md`, and the seat reports referenced below. No claim freeze correction was observed.

## Gate — assimilation set

Package `/home/vgpnk/Projects/shokuknow/merge/kasegi/` and absent-defect register were read-only. Theme: **Japanese severity vocabulary and the handling-priority model**. Adoption mapping is by document identity, not arithmetic: staged S049 (IPA JVN activity report) → lane S046; staged S050 (IPA quarterly report) → lane S047; staged S043 (JPCERT/CC guideline) → already-registered lane S041. The package SOURCES appendix bytes were measured by ScoutAssimPackage as SHA-256 `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb`.

### Admitted

| Item | Evidence | Gate decision |
|---|---|---|
| F14 — `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` | F14 binds S046/S047/S041. S046/S047 captures and manifest pins are in `ExecCaptureAssim.md` and `harness-after.txt`; entry SHA above. Non-author `RevC2Entry.md` verdict: **ADMIT, gate agree**. Q1 header/source URLs/anchors and verified-at, Q2 tier-A source support, Q3 located quotations, Q4 attribution, Q5 falsifiable checks and rejected generalizations, Q6 documentation-only scope, Q7/Q10 executable one-line recheck, bash syntax, cwd-independence and trailing note, Q8 normalization output, Q9 stem and occurrence/anchor evidence were reviewed. This is a pinned-capture recheck, not fresh network verification. | Admit. |
| S046 — IPA JVN activity report PDF | Captured `S046.txt` SHA `884481f3781e200d4c7e6efd91b2912ada513fa126c534d3392ccd48003a03a3`; CVSSv2/v3 band definitions lines 555–570. Q assertions all pass; Q3/Q4 normalized `markup-whitespace`. | Tier A, mined; staged S049 mapped by document. |
| S047 — IPA JVN 2026 Q3 registration report | Captured `S047.txt` SHA `bcf4f605d75909301f02560df894e0c4c15d97c7928a1759f57b15b5a7d905f4`; severity distribution lines 215–240. Q1 occurs 3× with verified anchor 123; Q3 occurs 2× with verified anchor 130; others once; source recheck passes. | Tier A, mined; staged S050 mapped by document. |
| S041 — JPCERT/CC 2026 guideline | Round-30 copy SHA `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`, same as round 28; F14 uses 付録4 handling-priority material, source assertions pass. | Existing row reused; no new registry row. |

Example short located quotations from the capture/manifest evidence: S046 “CVSSv3 基本値の深刻度による色分け”; S047 “公開日：2026年10月21日”; S041 `ExecCaptureAssim.md` records its exact assertions. Access date is 2026-10-25. No universal severity or remediation claim is made from these organization-specific materials.

### Refused package candidates

- `knowledge/chinese-criminal-thresholds-and-authorisation.md` (standing refusal): staged evidence is not lane-registered, the cross-instrument conclusion generalizes beyond located text (Q2/Q4), and located quotes/compliant executable recheck are missing (Q3/Q7/Q10). Flip only after registering/capturing cited sources, attributing each claim to its instrument, adding located quotes and qualifying recheck, and reassessing ground/Q5.
- `program-scope-rules-and-asset-boundaries.md`: staged platform claims cite unregistered CNVD/360SRC rows and lack located quotes/compliant recheck; ground does not bind to a lane frontier. Flip requires lane registration/capture, located quotes, qualifying recheck and named frontier topic.
- `claim-packaging-and-report-quality.md`: cited staged sources are not lane-registered; package F-space does not bind to a lane frontier and claims lack located quotations/recheck. Flip after lane rows/captures, quote locations, recheck and re-grounding.
- No Q/R bar was relaxed and no refused candidate file was copied into the lane.

### Quarantine slice verdicts

Seven rows from `ScoutQuarantineSlice.md`; final findings from `ExecQuarantineFetch.md`, `ConnQuarantine.md`, `RevQuarantineInd.md`, summarized in `ScribeQuarantine.md`. None adopted.

| ID | Verdict | Evidence / disposition |
|---|---|---|
| S037 | `fetched-no-quote` | GET 200, 24,189 B; composite quote not contiguous (components present). Reviewer disagreed with historical absent classification as fabrication. Unrelated to F14; not appendable. |
| S054 | `fetched-no-quote` | GET 200, 513,648 B PDF; phrase split across line break, not contiguous. Reviewer found phrase in local capture, so historical ABSENT label is not upheld as fabrication. IPA lineage related to F14 but isolated; F14 does not cite it. |
| S048 | `unfetchable` | GET 404/748 B; no quote check; remains unverified, not fabrication. |
| S065 | `reachable-quote-located` | GET 200, 7,465,472 B PDF; locators found. No admitted entry cites it, so not appended. |
| S068 | `already-mined-by-document` | URL byte-equal to existing lane S040 Cisco row; map to S040, no duplicate registration. |
| S069 | `unfetchable` | Full staged URL redirected then TLS verification failed (curl exit 60); no bypass. Flip from round-29 recorded reachable under the full staged URL. |
| S070 | `unfetchable` | Same redirect/TLS failure class, no bypass; not confirmed reachable. |

The seven-row verdict table distinguishes the current fetch from the older register label; two `payload-absent` candidates were not established as fabrications by the fresh evidence. Full measurements and SHA/status details are in `wave1/ScribeQuarantine.md` and `wave1/ExecQuarantineFetch.md`.

## Registry changes — old → new

- Registry total **45 → 47**; S046 and S047 appended after S045, both tier A/mined, opened `2026-10-25`, used-by the F14 entry. S046 recheck `180d`; S047 `90d` (staged `180d` normalized to lane cadence). Both staged anchors rewritten against the actual round-30 captures; staged S049/S050 opened date `2026-10-23` → `2026-10-25`.
- No pre-existing row changed; S041–S045 untouched. R8 changes logged in `corpus/SOURCES.md` lines 89–91. `RevC2Registry`/`ExecRegistryAppend.md` report schema/census clean. Final census histogram: tier A 44 / B 1 / C 2; status mined 35 / queued 9 / rejected 3; malformed 0, duplicate ids none, enum violations none, missing mined used-by paths none.
- Before census exit 0 / 45 rows / W04 S028/S029; after exit 0 / 47 rows / same two W04 duplicate-URL warnings only (`ExecCensusAfter.md`).

## Mistakes (M30-*)

Based on `wave1/ScribeMistakes.md`, `CritC1Kill.md`, `ExecMutantsC1.md`, `ScribeDigest.md`, `ExecBeforeVerify.md`, and later final receipts:

- **M30-1 — B2 fixture fails to isolate its claimed limb (counter/fixture design).** Frozen B2 record has id S045 but path `B2.txt`, so B1 stem-mismatch exits before occurrence handling. The B2-dropping mutant still exits 1 on this fixture; its flip is **NO**. A supplementary stem-matching repeated-quote fixture demonstrates live B2 failure `reason=occurrence-not-unique`, mutant exit 0; this proves implementation behavior, not the frozen counter's discrimination. Fix: append/use a stem-correct B2 fixture and tighten its kill requirement to `reason=occurrence-not-unique`; do not mutate frozen claims in place. Evidence: `c1-controls/before.txt`, `ExecMutantsC1.md` §4, `CritC1Kill.md` §3–4, `ScribeDigest.md`.
- **M30-2 — source instrument digest drift during implementation (bookkeeping/sequence).** Polls observed `0b841d5d…` → `2c893aa8…` → settled `33602a9d…`; earlier measurements are not final. Final receipt digest agrees with final harness evidence. Fix: hash immediately before/after each canonical receipt and label transient states; no stale digest may be treated as landed. Evidence `ScribeDigest.md`.
- **M30-3 — concurrent edits produce transient non-comparative outputs.** `ExecBeforeVerify.md` observed transient NameError and silent census exit 1 during concurrent writes; isolated freeze export and quiescent runs reproduced the frozen values. These are wave timing observations, not confirmed product defects. Fix: gate consumers on stable subject artifacts and treat in-flight outputs as non-comparative.
- **M30-4 — post-landing ancillary audit fails on proposals ledger recheck form.** `ExecExpectedList.md` records expected-list equality (43 entries) but `recheck-audit.py` exit 1 (`strict pass=42/43`, `instrument_fail=1`, `own_fail=1`) because `considerthese-proposals-ledger.md` recheck does not name a corpus instrument or itself. This is outside C1/C2 frozen counters but remains open. Fix through an admissible recheck form / instrument criterion, then rerun audit; do not claim green expected-list gate.
- **M30-5 — historical report-conformance and uncommitted-leftover defects routed from round 29.** Round-29 verifier routed missing literal Trend verdicts, incomplete/nonstandard SHONEN tokens, absent literal “Landed changes” / “Before → after measurements” headings, and closure with 44 deletions plus an untracked S069 PDF. Round-30 closure disposition for those report requirements is not established by the evidence inspected here; `ScribeMistakes.md` likewise declines to claim closure. Evidence: `corpus/lessons/round-29-verifier-spotcheck.md` §§Conformance/Routed defects; `wave1/ScribeMistakes.md`.

## considerthese

Frozen frontier step mined proposal 4 (“Give my own proposals a status ledger”) from `considerthese/2026-10-25.md`. `corpus/knowledge/considerthese-proposals-ledger.md` records proposals 1–6: 1 mined→R14/round 28; 2 open; 3 partially landed (round 29); 4 mined→this round/this ledger; 5 mined→R15/round 29; 6 open. `RevConsiderthese.md` found no status/path mismatch and source file hash unchanged. This ledger is not a second F14 admission. Its recheck form has the open audit failure M30-4.

## Census, density, and no-harm

- Sources census before: 45 rows, exit 0; W04 S028/S029 warnings only (`census-before.txt`). After: 47 rows, exit 0; same warnings (`ExecCensusAfter.md`).
- F14/C2 final counters are pinned in `.ufo/waves/round-30/harness-after.txt`: F14 PASS; 17/17; per-source S046/S047/S041 exits 0, S047 repetitions anchored at 123/130; C2 all structural numbers confirmed.
- Scorecard records C1 and C2 scores held at 4 and 7; density remains 9 with measurement mean 167.5 → 171.1 and anchorcheck classes unchanged (7 in-range, 0 bad, LOST-RECORDED 306, other failure classes 0). No density score move claimed.
- Caution: `RevNoHarm.md` did not independently certify all requested final-byte comparisons (notably PROVINCE); `CritGlobal.md` likewise says final no-harm is not certified. Preserve that verification boundary rather than equating unchanged verdict labels with a fully independent no-harm audit.

## Compliance and ownership

Single-writer declarations in wave spec/reports: frontier harness—`ExecImplFrontierHarness`; source checker—`ExecImplSourceRecheck`; captures/manifest—`ExecCaptureAssim`; F14 entry—`ExecEntryF14`; registry—`ExecRegistryAppend`; README—`ExecReadmeF14`; expected list—`ExecExpectedList`; proposals ledger—`ExecConsiderthese`; SKILL append—`ScribeSkillGate`; lesson—this seat. C1 controls, quarantine verdicts, census, C2 harness and reviews each have named owners/receipts. No evidence of duplicate production-file ownership was reported.

`ExecScopeSweep.md` found no attributable out-of-bounds seat write; no files written into shokuknow since wave start, no sibling-lane write attributable to this wave. It notes a fleet-root `MANIFEST.json` mtime/content change during the window, presumed orchestrator bookkeeping; L1 was asked to confirm no seat touched it. The lesson itself has no direct post-integration scope sweep. No git/jj mutation by this seat, no tooling install, no live bounty-target contact. Public source captures were the assigned IPA documentation; corpus is documentation-only under QUALITY Q6.

## Close-out ledger

1. **Integration/commit verification still owed:** run `.ufo/waves/round-30/post-commit-recheck.sh` at the final integration commit; pin committed instrument hashes to `aa60b581…` and `33602a9d…`, and retain output. No integration hash/post-commit recheck is asserted here.
2. **C1 B2 discrimination:** frozen fixture does not isolate B2; preserve this caveat or append a corrected control/claim correction, then run its mutant flip on isolated bytes. Current frozen kill clause passes for the wrong reason.
3. **Ancillary audit:** resolve the proposals-ledger `recheck-audit.py` failure; rerun audit. This is not a frozen C1/C2 counter but remains a gate failure.
4. **Run-7 evidence:** authoritative model-binding/execution role mix is absent from the inspected registry; m_flash majority and ≥25% attack roles remain unverified.
5. **No-harm/scope:** complete independent final `SKILL.md`/`PROVINCE.md` comparison and final scope sweep, including L1 confirmation about protected MANIFEST changes.
6. **Canonical report/admission:** report landing and final integration commit remain outside this lesson seat's evidence. No report/commit/push/deploy is performed by this seat.

## Touched surfaces and provenance

This lesson's production path is `corpus/lessons/round-30.md`; the scoped seat report is `.ufo/waves/round-30/wave1/ScribeLesson.md`. Evidence paths are named inline, principally `.ufo/waves/round-30/{claims.json,c1-controls/before.txt,c2-controls/before.txt,census-before.txt,harness-after.txt}`, `wave1/ExecBeforeVerify.md`, `ExecCaptureAssim.md`, `ExecEntryF14.md`, `ExecCensusAfter.md`, `ExecMutantsC1.md`, `ScribeDigest.md`, `ScribeQuarantine.md`, `ScribeMistakes.md`, `ScribeSpot.md`, `CritC1Kill.md`, `CritGlobal.md`, and `RevNoHarm.md`. No source-package files were written. No build, lint, formatter or general test suite was run by this scribe; this lesson assembles existing measured receipts and does not rerun them.
