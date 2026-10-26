# ConnOwnership — integration ownership + sequencing matrix (kasegi round 33, wave 1)

Seat: ConnOwnership (connector, leaf). Lane repo: /home/vgpnk/Projects/shokunin/kasegi-shokunin (only write scope; nothing outside it written). Date: 2026-10-26. Answering model actually run on: kimi-code/kimi-for-coding (config route table; no model passed by the seat — this item does not depend on model routing).

Sources of authority read: `.ufo/waves/round-33/claims.json` (frozen), `.ufo/waves/round-33/wave1-spec.json` (64 seat items), `.ufo/waves/round-33/wave1/swarm-registry.json`, `.ufo/waves/round-33/build-spec.py` (FILE OWNERSHIP string, committed), `corpus/QUALITY.md` (R1-R20), `corpus/SOURCES.md`, `corpus/README.md`, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `corpus/instruments/README.md`, `corpus/instruments/knowledge-expected.txt`, `.ufo/waves/round-33/{census-before.txt,watchdog-digest.txt,c1-controls/before.txt,c2-controls/before.txt,assimilation/*}`, `/home/vgpnk/Projects/shokunin/CORPUS.md` (read-only fleet contract).

## 1. Commands run and their output (evidence)

Roster (spec is the per-seat authority):

```
$ python3 - <<'PY'  # extract seat names from wave1-spec.json
import json; d=json.load(open('.ufo/waves/round-33/wave1-spec.json'))
print('\n'.join(sorted(it['name'] for it in d['items'])))
PY
ConnClaims ConnOwnership ConnSibling CritBoundary CritC1Kill CritC2Kill CritExpansion CritMistakes
ExecBeforeReceipts ExecCaptureBinding ExecCensusAfter ExecCensusDry ExecDeterminism ExecEntryF16
ExecErratumCheck ExecExpectedList ExecForeignCwd ExecGrowthMeasurement ExecHarnessC2 ExecManifest32
ExecManifestUpgrade ExecNoHarmFinal ExecQuarantine ExecRegistryAppend ExecRegressionC1
ExecScratchDiscipline ExecWaveEvidencePack MutCtrFetchMissing MutCtrSelftestSkip MutCtrUnbound
MutCtrUrlMismatch MutEntryF16 MutLegacyManifestDrop MutManifestLegacy RevC1BeforeAfter
RevC1Instrument RevCalibration RevClaimsFreeze RevEntryF16 RevGateSpot RevManifestUpgrade RevNoHarm
RevQuoteSweep RevRowS049 RevRowS050 RevTranslation ScoutDatawalk ScoutF16Sweep ScoutLiveDrift
ScoutManifestAudit ScoutPackageThemes ScribeInstrReadme ScribeLesson ScribeProvince ScribeQuality
ScribeReadmeF16 ScribeReportDraft ScribeScorecard ScribeSearchLog ScribeShonen ScribeSkillGate
SentCred SentScopeFinal SimplifierCleanup        # = 64 seats
```

Commit/base sanity:

```
$ git rev-parse master
53bfa59ff3fa578818e7e5db04fe60e80ed1eb6f
$ git cat-file -e 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 && echo base-ok     # -> base-ok
$ git cat-file -e 6e55c8d58a3e63efe11c0df47068bfc479bfc8e0 && echo freeze-ok  # -> freeze-ok
$ git log --oneline -3
53bfa59 round-33: dispatcher ready marker, C1 erratum 1 (Rule B per-id binding ruling), l1-ref sid-url table
a6a5023 round-33: wave-1 spec (64 seats, v2 policy), validated plan and dispatch
6e55c8d round-33: freeze claims C1/C2 with do-nothing controls, census-before, assimilation guard, watch-dog digest, LOG r32 entry (D1)
$ git show --stat --format='%s' 53bfa59 | tail -5   # adds .ufo/waves/round-33/claims-erratum-1.md, l1-ref/sid-url.tsv, wave1.ready
$ grep -nE '^## .*[Rr]ound[- ]32' LOG.md
1593:## Round 32 — 2026-10-25 — honest stop: claims frozen, ...           # D1 LOG entry present (L1-owned)
$ git show --format='%ad' 288ea9ac17a78dce644388af35b89aa96b7994da -s    # -> Sun Oct 25 23:14:00 2026 -0300 (matches INTERFACE CONTRACT fetched_utc source)
```

Every polled receipt maps to a seat (no seat waits on a file nobody owns):

```
$ python3 - <<'PY'
import json,re
d=json.load(open('.ufo/waves/round-33/wave1-spec.json'))
seats={it['name'] for it in d['items']}
referenced={m for it in d['items'] for m in re.findall(r'\{WD\}/([A-Za-z0-9_.-]+\.md)', it['prompt'])}
missing=sorted(r for r in referenced if r[:-3] not in seats)
print('seats:',len(seats),'referenced receipts:',len(referenced)); print('referenced-but-no-seat:', missing)
PY
seats: 64 referenced receipts: 64
referenced-but-no-seat: []
```

In-flight state at matrix time (git status --porcelain, read-only):

```
 M corpus/QUALITY.md                                  # ScribeQuality (R20/R21 additions, in flight)
 M corpus/source-snapshots/{round-23,24,25,26,28,29,30,31}/manifest.json   # ExecManifestUpgrade
?? corpus/instruments/capture-binding-check.py        # ExecCaptureBinding
?? corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md       # ExecEntryF16
?? corpus/source-snapshots/round-32/manifest.json     # ExecManifest32
?? .ufo/waves/round-33/wave1/ + wave1.ready.dispatched
$ python3 - <<'PY'   # field audit of the 9 manifests (working tree)
import json,glob
tot=u=a=f=0
for p in sorted(glob.glob('corpus/source-snapshots/round-*/manifest.json')):
    if 'round-32' in p: continue
    for s in json.load(open(p))['sources']:
        tot+=1; u+='url' in s; a+=s.get('archival') is True; f+='fetched_utc' in s
print('legacy records=%d with_url=%d archival_true=%d fetched=%d'%(tot,u,a,f))
# round-32: S049 url=https://zc.cnvd.org.cn/news/helpList fetched=2026-10-25T23:14:00-03:00 quotes=8
#           S050 url=https://security.360.cn/Reward/rules fetched=2026-10-25T23:14:00-03:00 quotes=6
PY
legacy records=38 with_url=38 archival_true=38 fetched=0
```

Receipt census at matrix time: 23 of 64 wave receipts present, including all five scouts, ExecManifestUpgrade, ExecManifest32, ExecCaptureBinding, ExecCensusDry, ExecErratumCheck, ExecQuarantine, ExecBeforeReceipts, ScribeQuality, ConnClaims, ConnSibling; ExecEntryF16's entry file exists (its receipt pending). Downstream seats messaged below had NOT yet landed (ExecRegistryAppend, ScribeSearchLog, ScribeReadmeF16, ScribeProvince, ExecExpectedList, ExecHarnessC2, ScribeShonen, ScribeSkillGate, ScribeInstrReadme, ScribeScorecard, ScribeLesson, ScribeReportDraft).

Section geometry for R6 (grep -nE '^#{1,3} '):

```
corpus/SOURCES.md:  ## Registry :3 | table rows ... S048 at :54 | ## Paths :56 | ## Search log :63 | ## Leads :74 | ## Registry changes :80 (EOF region)
PROVINCE.md:        # title :1 | ## Core :27 | ## Frontier :35 | ## Adjacent :43 | ## Frontier amendment — F12-F15 :54 (EOF :72)
corpus/README.md:   ## Coverage map :7 | ## Known gaps :52 | ## Frontier :198 | round-appended sections :226/:247/:266/:293 (EOF :316)
SHONEN.md: 42 lines (box-2 evidence sentence at :34); SKILL.md 1071; QUALITY.md 213; SCORECARD.md 980; instruments/README.md 511; LOG.md (r32 entry :1593)
```

Line-citation inventory into append targets (grep -rnE '<file>:[0-9]' over corpus/*.md + SKILL.md + SCORECARD.md + LOG.md):

```
SOURCES.md:  round-28.md:203->:48, round-25.md:90->:22, round-28.md:104/:193->:46/:47, round-31.md:29 + round-31-verifier-spotcheck.md:92->:54, round-29.md:214 + round-29-verifier-spotcheck.md:74->:83 (M31-3: already off by +4)
PROVINCE.md: citation-survival.md:110->:3, source-tree-loss:3+:353->:3, round-17-mirror-relocation:26->:16-22, round-24.md:55->:29/:37, round-24-verifier-spotcheck:112->:38, :141->:31-40   (nothing >= :43)
SHONEN.md:   round-31-verifier-spotcheck.md:23 and :107 cite :34
manifest.json / knowledge-expected.txt: ZERO line-cites (path-cited only) -> field edits / sorted insert anchor-safe
README.md :49/:54/:82/:145/:168/:211/:309, QUALITY.md :77/:83/:89/:95/:102, SCORECARD.md :251/:331/:813-819/:947, LOG.md :1101/:1469 — all above the EOF appends their owners make
```

Contradiction evidence (build-spec.py, committed at a6a5023):

```
$ grep -n "ScribeSearchLog\|Search log" .ufo/waves/round-33/build-spec.py | head
41:  ... corpus/SOURCES.md (append rows S049/S050 + Search log + R8 lines): ExecRegistryAppend | ...   # FILE OWNERSHIP list: whole path -> ExecRegistryAppend
92: it("ExecRegistryAppend", ... "Append to the Search log one prose note for this round's bounded search (rule 5, using ScoutF16Sweep + ScoutPackageThemes numbers) and R8-style log lines ...")
133: it("ScribeSearchLog", "scribe", """Own the Search log section of {LANE}/corpus/SOURCES.md ONLY ... append one prose note for this round's bounded search ... Keep the R8-style registry-change lines to ExecRegistryAppend.""")
```

Prior-round pattern (ls .ufo/waves/round-2*/wave1/): rounds 28-31 had NO ScribeSearchLog seat; the single registry seat (ScribeRegistryC2/ExecRegistryAppend) landed rows + Search log + R8 lines. ScribeSearchLog exists only in round 33.

## 2. Ownership matrix (verified against spec items; no path with two writers under the FILE OWNERSHIP list; no required write without an owner)

| Path | Owner (single) | Edit kind | R6 verdict |
|---|---|---|---|
| corpus/instruments/capture-binding-check.py | ExecCaptureBinding | new file | n/a (no anchors) |
| corpus/source-snapshots/{r23,r24,r25,r26,r28,r29,r30,r31}/manifest.json | ExecManifestUpgrade | per-record field add (`url`, `archival:true`, `archival_note`) | safe — manifests path-cited only; receipts show `git diff -U0` additions-only |
| corpus/source-snapshots/round-32/manifest.json | ExecManifest32 | new file | n/a |
| corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md | ExecEntryF16 | new file | n/a |
| corpus/SOURCES.md — Registry table rows + R8 lines + Search-log note | ExecRegistryAppend (F1 default executed; ScribeSearchLog held) | table insert after S048 (:54->:55/:56) + Search-log bullet :75 + R8 lines :98-:100 | measured post-land (ExecRegistryAppend receipt): in-table cites (:22,:46,:47,:48,:54) unchanged; ## Paths 56->58, ## Search log 63->65, ## Leads 74->77, ## Registry changes 80->83; census-mandated insert, M31-3 precedent — see Finding F4 |
| corpus/README.md | ScribeReadmeF16 | EOF section `## Round-33 admission` | safe — all cites < EOF |
| PROVINCE.md | ScribeProvince | one line, Frontier-section end or amendment section | safe if appended at section end (Finding F3) |
| SKILL.md | ScribeSkillGate | EOF append | safe |
| corpus/QUALITY.md | ScribeQuality | EOF `## Round-33 additions` (R20/R21) | safe |
| corpus/instruments/README.md | ScribeInstrReadme | EOF `## Round-33 additions` | safe |
| corpus/instruments/knowledge-expected.txt | ExecExpectedList | sorted insert (44 -> 45 entries) | safe — zero line-cites |
| LOG.md | L1 (no seat) | EOF append | n/a (r32 entry already at :1593) |
| SCORECARD.md | ScribeScorecard | EOF `## Round 33` + capabilities row | safe |
| SHONEN.md | ScribeShonen | in-place box-evidence updates | safe ONLY as same-line replacement (Finding F2) |
| corpus/lessons/round-33.md | ScribeLesson | new file | n/a |
| Round report (.ufo/reports/round-33/kasegi.md) | L1 (ScribeReportDraft drafts into its own receipt only) | L1 files | n/a |
| limb-mutation-check.py, limb-ledger.json, recheck-audit.py, source-recheck.py, frontier-recheck-count.py, anchorcheck.py, density.py, resolve.py, score-gap.py | READ-OWNED this round (no seat's item edits them; mutation seats copy to scratch only) | none | — |
| wave1/<Seat>.md receipts | each owning seat (64/64) | own receipt | — |
| claims.json, claims-erratum-1.md, c1-controls/, c2-controls/, census-before.txt, assimilation/, watchdog-digest.txt, wave1-spec/dispatch/registry | L1 / frozen | none by seats | — |

Verdict on the FILE OWNERSHIP list itself: no path carries two writers; every required write carries an owner. The list's SOURCES.md line ("rows + Search log + R8 lines: ExecRegistryAppend") conflicts with the ScribeSearchLog seat item — see Finding F1.

## 3. Dependency order (edges read verbatim from seat items; join barriers noted)

```
scouts (ScoutDatawalk, ScoutManifestAudit, ScoutF16Sweep, ScoutPackageThemes, ScoutLiveDrift)
  -> ExecManifest32         (waits ScoutF16Sweep.md + ScoutLiveDrift.md)
  -> ExecEntryF16           (waits ExecManifest32.md recheck exit 0; reads ScoutF16Sweep.md, ConnSibling.md)
  -> ExecCensusDry          (reads ScoutManifestAudit/ScoutPackageThemes; scratch mirror census; gates the registry append)
  -> ExecRegistryAppend     (waits ExecEntryF16.md + ExecCensusDry.md verdict)
       -> ScribeSearchLog   (waits ExecRegistryAppend.md)  [WRITE HELD — Finding F1]
       -> ExecCensusAfter   (after ExecRegistryAppend + ExecHarnessC2)
  -> {ScribeReadmeF16 (waits ExecEntryF16.md), ScribeProvince (waits ExecEntryF16.md),
      ExecExpectedList (waits ExecEntryF16.md)}
  -> ExecHarnessC2          (waits ScribeReadmeF16.md + ExecExpectedList.md + entry + manifest + registry rows)
ExecCaptureBinding -> ExecManifestUpgrade  (literal edge: ExecManifestUpgrade runs the checker and waits ExecCaptureBinding's receipt)
{ExecCaptureBinding, ExecManifestUpgrade, ExecManifest32} -> ExecRegressionC1 (polls all three receipts)
ExecErratumCheck -> ScribeLesson           (ScribeLesson polls ExecErratumCheck.md)
ScribeSkillGate / ScribeInstrReadme        (wait ExecCaptureBinding.md + ExecManifest32.md)
ScribeScorecard                            (polls ExecRegressionC1.md + ExecHarnessC2.md + ExecCensusAfter.md + >=10 receipts)
End-of-wave join barrier (>=40 receipts): ExecNoHarmFinal, ExecGrowthMeasurement, ExecScratchDiscipline,
  SentScopeFinal, ExecWaveEvidencePack, SimplifierCleanup(read-only), ExecDeterminism, ExecForeignCwd, SentCred
Reviewers/critics/mutation-testers hang off their subjects' receipts (all subjects owned — 64/64 map check §1).
```

The L1's coarse order from my item (scouts -> ExecManifest32 -> ExecEntryF16 -> {ExecRegistryAppend, ScribeReadmeF16, ScribeProvince, ExecExpectedList, ScribeSearchLog} -> ExecHarnessC2; ExecCaptureBinding -> ExecManifestUpgrade -> ExecRegressionC1; ExecErratumCheck -> ScribeLesson) is confirmed by the items, with three refinements: (a) ExecRegistryAppend additionally waits ExecCensusDry; (b) ExecHarnessC2's direct predecessors are ScribeReadmeF16 + ExecExpectedList (+ the entry/manifest/registry bytes), with ScribeSearchLog ordered before it transitively via ExecRegistryAppend; (c) ExecManifest32 also feeds ExecRegistryAppend and ExecRegressionC1 directly (it messages them by id).

Cycle check: every edge points from a later consumer to an earlier producer; no mutual wait exists (checked pairwise over the edge list above; e.g. ScribeSearchLog -> ExecRegistryAppend has no back-edge). No seat waits on a file nobody owns (64/64 receipt map, §1). One item defect: ExecEntryF16's prompt says to message "ScribeGateDraft", a seat id that does not exist in the roster — harmless (ScribeSkillGate polls receipts; it waits on no message).

## 4. Findings

- **F1 (contradiction, reported to Main; both seats messaged).** ExecRegistryAppend's item (build-spec.py:92) and ScribeSearchLog's item (build-spec.py:133) both instruct appending the SAME round-33 Search-log prose note to corpus/SOURCES.md. The frozen FILE OWNERSHIP list assigns the whole path incl. the Search log to ExecRegistryAppend. Interim default applied: ExecRegistryAppend writes the note with its rows+R8 lines (rounds 28-31 pattern: a single registry seat made every SOURCES.md append; ScribeSearchLog's edit would be a two-writer defect against the ownership list); ScribeSearchLog holds its write and verifies the landed note against ScoutF16Sweep + ScoutPackageThemes counts. Ruling requested from Main.
- **F2 (R6, messaged ScribeShonen).** SHONEN.md:34 is line-cited by round-31-verifier-spotcheck.md:23/:107. Box updates must be same-line replacements; no line insert/delete.
- **F3 (R6, messaged ScribeProvince).** Append the F16 line at the end of ## Frontier (after F15, before ## Adjacent :43) or into the F12-F15 amendment section at EOF; never insert above existing Frontier rows (would shift :38, cited by round-24-verifier-spotcheck.md:112).
- **F4 (R6, recorded for ScribeLesson; corrected post-land to the measured values).** ExecRegistryAppend's rows landed at :55/:56, its Search-log bullet at :75, its R8 lines at :98-:100 (measured, base 690b69da -> landed; 6 added lines, 0 removed). Section shifts measured: ## Paths 56->58, ## Search log 63->65, ## Leads 74->77, ## Registry changes 80->83; the S043 change-cell line 87->90. The already-stale SOURCES.md:83 trail (M31-3, +4) is now **+7** — my pre-land prediction said +6, counting only the two table rows; the landed Search-log bullet adds one more in-section line, a further +1 (measured beats predicted; recorded per R9). Remedy is an R9-style erratum row in corpus/lessons/round-33.md naming the M31-3 wording — the filed lesson sentences stay byte-identical.
- **F5 (minor, recorded for ScribeLesson).** "ScribeGateDraft" message target in ExecEntryF16's item matches no roster id (ScribeSkillGate is the intended seat; nothing blocks on the message).

## 5. Messages sent (peer coordination, no agent://all)

ExecRegistryAppend (write the note; don't wait on ScribeSearchLog; record pre/post line numbers), ScribeSearchLog (HOLD write; verify the landed note), ScribeShonen (F2), ScribeProvince (F3), ScribeLesson (F4+F5), Main (F1 ruling request + overall verdict). Delivery confirmed for all six.

## 6. Verdict

The FILE OWNERSHIP list has no two-writer path and no orphan required write; the wait-DAG is acyclic and every polled file has a producing seat. One real item-level contradiction (F1) is queued to the L1 with a safe interim default that keeps single-writer reality on corpus/SOURCES.md. R6 holds for every owner's planned edit given constraints F2/F3 and the census-mandated insert F4.

Checks NOT run (not this seat's scope): instrument counters, census, harness — those belong to ExecRegressionC1 / ExecCensusAfter / ExecHarnessC2 on quiescent bytes. No live target contacted (read-only local evidence only). No tool installed or upgraded this seat.

## 7. Post-land confirmations (peer replies received while this receipt was being finalized)

- **ScribeProvince (F3):** F16 line placed at EOF after the round-31 amendment block (line 74), NOT inside the Frontier rows. Measured: `git show HEAD:PROVINCE.md` vs worktree lines 1-72 byte-identical; cited anchors :3,:16-22,:29,:31-40,:37,:38 all stable; diff = 2 insertions (blank + one F16 line), 0 deletions. Stronger than the section-end option flagged in F3 — matrix closed on this path.
- **ExecRegistryAppend (F1 default + F4):** Landed per the default — one file, one writer: rows S049/S050 at :55-:56, the round-33 Search-log bullet at :75, three R8 lines at :98-:100. Measured R6 (base 690b69da -> landed): :22,:46,:47,:48,:54 unchanged; ## Paths 56->58, ## Search log 63->65, ## Leads 74->77, ## Registry changes 80->83; S043 change-cell 87->90; M31-3 :83 trail now +7 (corrects my pre-land +6 — see F4). Diff vs base blob: 6 added lines, 0 removed/changed. Its receipt also reports census validate exit 0 (rows=50, only W04 S028/S029) and `capture-binding-check` records=40 bound=40 unbound=0 exit 0 — cited here as its receipt data; the quiescent-byte counters belong to ExecHarnessC2/ExecRegressionC1.
- **F1 state at yield time:** interim default executed (ExecRegistryAppend wrote the note); Main's ruling was still pending when this receipt was finalized. If Main rules for ScribeSearchLog, the reversal is an L1-level edit decision — this receipt records both the contradiction and the executed default so the ruling has the full context.
- **ScribeSearchLog (post-yield confirmation):** held its write — no duplicate bullet. Verified the landed note 6/6 on rule-5 elements against receipts and bytes (counts identified 9 / screened 9 / included 2 / excluded 7, denominator = ScoutPackageThemes' 9-row table; two live re-fetches 2026-10-26T04:16Z per ScoutLiveDrift.md, HTTP 200, byte-identical text). Recorded two defects it found in the first landing, fixed by ExecRegistryAppend in-line (false "no target was re-fetched" clause; unlabelled PRE-STATE sweep count now labelled). Final bytes pinned: corpus/SOURCES.md sha256 b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b, 100 lines, exactly one "round 33" occurrence. Also confirmed: no cycle on its side (depends only on landed receipts). One scope note (not a defect), recorded in its receipt: the bullet's 7-name exclusion list omits two staged theme-byte matches that hold no F16 ground; the bullet's denominator stays internally consistent. F1 is operationally closed on the bytes; only the L1's formal ruling remains open.

Scratch: analysis copies under $HYAKU_SCRATCH/kasegi-r33/ConnOwnership/ (execregistry-prompt.txt, edges-prompts.txt) removed at seat exit; the only bytes written to the lane are this receipt.
