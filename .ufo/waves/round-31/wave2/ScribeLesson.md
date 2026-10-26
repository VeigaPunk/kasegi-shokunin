# ScribeLesson — round 31, wave 2 (falsify wave)

- Seat: `ScribeLesson` (scribe, leaf — no delegation, no background jobs of my own, no swarm).
- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write scope). Lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`; claims freeze `738a77999a00efbca129cfccb28a481037f6241f`; wave-1 spec/dispatch commit `8a8916c7043bd873d191b30dd1744b241b91f4d9`; wave-1 integration commit `eecad59db166e0626ca2472e96ea48bc28a35153` (read-only `git rev-parse`); final integration hash `LANDED_HASH_PENDING`.
- Answering model actually run on: `opencode-go/deepseek-v4.1-flash` (workstation route table; no model passed by this seat).
- Tooling: nothing installed or upgraded; no pacman transaction (host-wide pause); no `uv`/`npx`/binary download. No network fetch by this seat.
- Writes: `corpus/lessons/round-31.md` (owned) and this receipt only. No instrument, entry, registry, README, SKILL, PROVINCE, QUALITY, SCORECARD, LOG or SHONEN byte. No git/jj mutation (read-only `rev-parse`, `status`, `ls-files` only). No fleet-root, sibling-lane or shokuknow write; no package tool run; no live bounty-target contact.
- Honest disclosure on waiting: my item's poll loop was auto-backgrounded by the shell tool as `bg_20845` (reported `BOTH_ARRIVED 2026-10-26T00:38:24Z`, wall time 340.02 s) rather than staying in the foreground. It is disclosed rather than described as a foreground run; no other job was spawned.

## 1. Gate condition — the poll my item names

Item condition: the three wave-1 receipts `ScribeGateDraft.md`, `ExecHarnessC2.md`, `ExecLedgerMerge.md` exist **and** at least 10 wave-2 receipts exist (cap 45 min). Both halves were already satisfied on first listing.

```
$ ls -la .ufo/waves/round-31/wave1/ .ufo/waves/round-31/wave2/      (cwd = lane root)
… wave1/: ScribeGateDraft.md 45728 B 21:08, ExecHarnessC2.md 17256 B 20:52, ExecLedgerMerge.md 26861 B 21:01 …
… wave2/: 23 *.md files at first listing (CritExpansion, ExecLimbFRduplicateentry, ExecLimbFRmissingentry,
   ExecLimbRAcdroot, ExecLimbRAcompleteness, ExecLimbRAcwd, ExecLimbRAexpectmissing, ExecLimbRAexpectunexpected,
   ExecLimbRAinstrument, ExecLimbRAown, ExecLimbRAparse, ExecLimbRApaths, ExecLimbSRoccurrencenotunique,
   ExecLimbSRstemmismatch, MutCtrAlwaysKilled, MutCtrNoCompileCheck, MutCtrSignalIgnored, RevEntryQ,
   RevQuoteRoles, RevQuoteRoutes, RevRowS048, ScoutLiveDrift) …

$ ls .ufo/waves/round-31/wave2 | wc -l
23
```

Because the item also names `CritMistakes` as a Mistakes source and `ExecCensusFinal.md` as the census-after receipt, I polled for those two after reading the wave-1 receipts:

```
$ cd .ufo/waves/round-31/wave2 && end=$((SECONDS+1200)); while [ $SECONDS -lt $end ]; do
    if [ -s CritMistakes.md ] && [ -s ExecCensusFinal.md ]; then echo "BOTH_ARRIVED $(date -u +%FT%TZ)"; break; fi; sleep 20; done
BOTH_ARRIVED 2026-10-26T00:38:24Z        # tool-reported: auto-backgrounded as bg_20845, wall 340.02 s
```

Presence checks across the composition window (`for f in …; do [ -s "$f" ] && echo PRESENT || echo ABSENT; done`):

```
2026-10-26T00:32:34Z   ABSENT CritMistakes.md; ABSENT ExecCensusFinal.md; ABSENT ExecCounterFix.md; ABSENT ExecRegressionC1.md;
                       ABSENT RevScoreGap.md; ABSENT RevGateSpot.md; ABSENT MutErratumCheck.md; ABSENT SentScopeFinal.md;
                       ABSENT ExecNoHarmDensity.md; ABSENT ConnCrossPattern.md; ABSENT ConnAssimilationFit.md;
                       ABSENT ScribeQualityFix.md; ABSENT ScribeScorecard.md; ABSENT ScribeShonen.md; ABSENT ScribeReportDraft.md
2026-10-26T00:36:33Z   ABSENT CritMistakes.md; PRESENT ExecCensusFinal.md (326 lines); ABSENT ExecCounterFix.md
2026-10-26T00:38:31Z   PRESENT CritMistakes.md; ABSENT SentScopeFinal.md; ABSENT RevGateSpot.md; ABSENT MutErratumCheck.md; ABSENT ScribeQualityFix.md
```

So the item's gate is met, the two extra receipts the item names arrived before I wrote the corresponding sections, and the absences are recorded in the lesson's `## Open items` (§11 of this receipt).

## 2. Evidence read (all paths relative to the lane root)

`.ufo/waves/round-31/`: `claims.json`, `census-before.txt`, `c1-controls/before.txt`, `c1-controls/fake-counter-receipt.txt`, `c2-controls/before.txt`, `wave1-dispatch.json`, `wave1-spec.json`, `wave1-results.json`, `wave2-dispatch.json`, `wave2-spec.json`, `assimilation/*` (as cited by wave-1 receipts; not re-derived by me).

`wave1/`: `ScoutMSVR`, `ScoutPackageThemes`, `ExecCapManifest`, `ExecEntryF15`, `ExecRegistryAppend`, `ExecCensusDry`, `ExecExpectedList`, `ExecHarnessC2`, `ExecCounter`, `ExecLedgerMerge`, `ExecRALimbs`, `ExecSRLimbs`, `ExecFRLimbs`, `ExecScoreGap`, `ExecErratumCheck`, `ExecErratumCheck-before.txt`, `ExecErratumCheck-after.txt`, `ScribeErratum`, `ScribeLogR30`, `ScribeQuality`, `ScribeReadmeF15`, `ScribeConsiderthese`, `ScribeGateDraft`, `CritC1Kill`, `CritC2Kill`, `RevSourceBar`, `RevClaimsFreeze`, `ConnOwnership`, `ConnSibling`, `SentScopeW1`, `MutRAExisting`, `MutSRExisting`, `MutFRExisting`.

`wave2/`: all 13 `ExecLimb*`, `MutCtrAlwaysKilled`, `MutCtrNoLiveBaseline`, `MutCtrNoCompileCheck`, `MutCtrNonUniqueFind`, `MutCtrSignalIgnored`, `MutCtrTimeoutKilled`, `RevEntryQ`, `RevRowS048`, `RevQuoteRoles`, `RevQuoteRoutes`, `RevScoreGap`, `CritExpansion`, `CritMistakes`, `ScoutLiveDrift`, `ExecCensusFinal`, `ExecNoHarmDensity`, `ConnAssimilationFit`, `ConnCrossPattern`.

Lane bytes read (no writes): `corpus/SOURCES.md:54`, `corpus/README.md:309`, `corpus/QUALITY.md:95-96`, `corpus/instruments/limb-ledger.json`, the three instruments, `corpus/instruments/limb-fixtures/**` (`git ls-files` → 10 files, no untracked, no modified).

## 3. Measurements this seat took (read-only)

### 3.1 Dispatch shape

```
$ python3 -c "import json; [print(f, json.load(open(f))['wave'], json.load(open(f))['counts']) for f in ('wave1-dispatch.json','wave2-dispatch.json')]"
wave1-dispatch.json kasegi-r31-build {'spawn': 38, 'resume': 0, 'total': 38}
wave2-dispatch.json kasegi-r31-falsify {'spawn': 42, 'resume': 0, 'total': 42}
$ python3 -c "import json; print(json.load(open('wave1-results.json'))['seats'])"
38
```

Role counts are from `wave1-spec.json` / `wave2-spec.json` `items[].role` (`?q=.items[]|{name,role}`): wave 1 = scout 5, connector 3, executor 13, scribe 9, reviewer 2, critic 2, mutation-tester 3, sentinel 1 (38); wave 2 = executor 17, mutation-tester 7, reviewer 6, scribe 5, critic 3, connector 2, scout 1, sentinel 1 (42).

### 3.2 Instrument digests at composition (`2026-10-26T00:34:15Z`)

```
$ date -u +%FT%TZ && sha256sum corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json \
    corpus/instruments/recheck-audit.py corpus/instruments/source-recheck.py corpus/instruments/frontier-recheck-count.py
2026-10-26T00:34:15Z
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
$ git status --porcelain -- corpus/instruments/ | head
(empty)
$ grep -c 'guard cases=' corpus/instruments/limb-mutation-check.py
0
```

The last two lines are the basis for the lesson's disclosure that the guard-fixture fix reported by `MutCtrNonUniqueFind.md` §Afterword is **not observable** on the lane at that timestamp: the counter was still `c660a95f…`, the tree was clean, and no guard line existed in the source.

Re-measured five minutes later, while `ExecCounterFix` was writing:

```
$ date -u +%FT%TZ && sha256sum corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json && git status --porcelain -- corpus/instruments/ && grep -c 'guard cases=' corpus/instruments/limb-mutation-check.py
2026-10-26T00:40:25Z
237fd07cbcb4a12a470e912d1a4b68ff1968fde62f2709b182822fed42d791f4  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
 M corpus/instruments/limb-mutation-check.py
2
$ sleep 5; sha256sum corpus/instruments/limb-mutation-check.py
237fd07cbcb4a12a470e912d1a4b68ff1968fde62f2709b182822fed42d791f4  corpus/instruments/limb-mutation-check.py
```

Labelled **IN-FLIGHT / NON-COMPARATIVE** (bound 6, M30-3): a sibling seat owns the file, its receipt was still absent, and this seat ran nothing on those bytes. The lesson records the state and the timestamp, keeps every C1 number bound to `c660a95f…`, and lists the canonical replay plus a replay of the three survivor mutants as owed.

### 3.3 Model tally across receipts

```
$ for f in wave1/*.md wave2/*.md; do ms=$(grep -oE '(devin|opencode-go|anthropic|google-antigravity|zai|inception)/[a-z0-9.\-]+' "$f" | sed 's/\.$//' | sort -u | paste -sd,); echo "$ms"; done | sort | uniq -c | sort -rn
     26 devin/deepseek-v4-1-flash
     22 opencode-go/deepseek-v4.1-flash
      2 zai/glm-5.3-flash
      2 google-antigravity/gemini-4-argon
      2 google-antigravity/gemini-3.8-flash
      2 anthropic/claude-sonnet-5-5
      1 inception/mercury-3
      1 anthropic/claude-sonnet-5-5,inception/mercury-3
$ (files naming no model)  → MutFRExisting.md MutRAExisting.md MutSRExisting.md ScoutDatawalk.md ScoutF15Sweep.md
   ScoutRALimbMap.md MutCtrAlwaysKilled.md MutCtrNoCompileCheck.md MutCtrNonUniqueFind.md MutCtrSignalIgnored.md ScoutLiveDrift.md
```

`grep -rl 'zai/glm'` → `wave2/MutCtrNoLiveBaseline.md`, `wave2/MutCtrTimeoutKilled.md`; `grep -rl 'inception/mercury-3'` → `wave2/ConnAssimilationFit.md`, `wave2/ConnCrossPattern.md`.

### 3.4 Structure and quote discipline of the lesson

```
$ grep -n '^# \|^## \|^### ' corpus/lessons/round-31.md
1:# Round 31 — kasegi
9:## Frozen claims — before → after
18:## Gate — F15 / S048 and the assimilation set
22:### Admitted
33:### Id-collision evidence — adoption by document, never by number
46:### Refused package candidates (each with flip condition)
57:### Registry changes — old → new
72:### Staged-to-lane normalization notes
82:### Gate caveats this round must carry
88:## Mistakes (M31-*)
101:### Critic additions — `wave2/CritMistakes.md` O1–O6
113:## considerthese
117:## Census before → after
125:## No-harm and density (wave 2, read-only)
129:## Open items / unverified
145:## Touched surfaces and provenance
$ wc -lc corpus/lessons/round-31.md
  149 50258 corpus/lessons/round-31.md
$ python3 -c "s=open('corpus/lessons/round-31.md',encoding='utf-8').read(); print('chars',len(s),'bytes',len(s.encode()))"
chars 49629 bytes 50258
$ grep -c 'LANDED_HASH_PENDING' corpus/lessons/round-31.md
1
$ sha256sum corpus/lessons/round-31.md
be2c993e30047f694740d425ca0ba248c1911c2b08076d139657f63ee896a1f5  corpus/lessons/round-31.md
$ python3 - <<'PY'   # word counts of every source quote the lesson carries
qs = ["Microsoft's own statement of its MSVR programme and of nothing beyond it",
      "A vendor's research programme as an intake route for other vendors' bugs",
      "as a coordinator of vulnerabilities that affect multiple vendors",
      "the counter now runs three implicit guard fixtures on every ledger run"]
for q in qs: print(len(q.split()), '|', q)
PY
12 | Microsoft's own statement of its MSVR programme and of nothing beyond it
12 | A vendor's research programme as an intake route for other vendors' bugs
9 | as a coordinator of vulnerabilities that affect multiple vendors
12 | the counter now runs three implicit guard fixtures on every ledger run
```

Every quoted source string is ≤25 words; locations are given inline (`corpus/SOURCES.md:54`, `corpus/README.md:309`, `corpus/source-snapshots/round-31/S048.txt:35` with access date 2026-10-25, `wave2/MutCtrNonUniqueFind.md` §Afterword). The single `LANDED_HASH_PENDING` occurrence is the placeholder on the revisions line (header line 3), the line the L1 replaces; no hash was invented.

## 4. What was written, and the corrections applied during composition

1. `write corpus/lessons/round-31.md` → 36591 B (first draft, following `corpus/lessons/round-30.md`'s section shape).
2. Corrections after checking receipts line by line (each edit asserted `count(old)==1` before replacing; outputs below are the script's own print):
   - C1 before column: `cases=9 failures=0` belongs to `source-recheck.py` (recheck-audit prints case lines with `ra_selftest_exit=0` and no `cases=N` summary in `c1-controls/before.txt`) → fixed; after column re-labelled `source-recheck selftest cases=10 failures=0`.
   - Section pointers corrected against the receipts' own headings: `ExecLimbRAparse` §3→§4, `ExecLimbRAcompleteness` §MUT-D→§4, `ExecLimbRAexpectmissing` §3→§2, `ExecLimbRAexpectunexpected` →§5, `ExecLimbRAinstrument` →§3, `ExecLimbRAown` →§5, `ExecLimbRApaths` §5–§6→§4–§6.
   - Model paragraph rewritten twice as new receipts landed (`inception/mercury-3`, `zai/glm-5.3-flash` added; counts re-measured).
   - C1 verdict and M31-7 rewritten after `MutCtrNoLiveBaseline.md` and `MutCtrTimeoutKilled.md` landed: **two** frozen mutants survive, plus one out-of-set survivor.
   - Census section replaced (`ExecCensusFinal.md` arrived): before/after `diff` (only the frozen wrapper line differs, both exit 0), histograms, all seven target cells, junk-row control; the earlier `BLOCKED:` line removed because the receipt now exists.
   - New section `## No-harm and density` from `ExecNoHarmDensity.md` §5 (mean 171.1 → 191.5, blocks 23 → 24, 40.74% resolve fraction disclosed, anchor classes identical, SKILL/PROVINCE +34/−0).
   - `## considerthese` extended with `RevScoreGap.md`'s `defect` verdict (census-lane provenance string; stub fallback `KeyError`).
   - Gate: fifth standing refusal (`chinese-criminal-thresholds-and-authorisation.md`, `1660c00c…`) added from `ConnAssimilationFit.md` §2–§3.
   - Mistakes: `CritMistakes.md` additions O1–O6 appended as a labelled subsection with class · evidence · captured-by · fix, and M31-1/M31-2 amended with the critic's O3/O4/O5 and O2 findings.
   - Open items renumbered to 13, including the R16 finding, the density/census-of-record staleness, and the score-gap defects.
3. Word-count correction: two located quotes were labelled "13 words"; measured 12 → labels fixed.

## 5. Gates this seat did NOT run (deliberate)

No counter, census, harness, audit, selftest or fetcher was executed by this seat — the lesson assembles measured receipts (`wave1/ExecLedgerMerge.md` §2/§5, `wave1/ExecHarnessC2.md` §0–§2, `wave2/ExecCensusFinal.md` §1–§4, `wave2/ExecLimb*` §, `wave2/MutCtr*`, `wave2/ExecNoHarmDensity.md` §5, `wave1/ExecErratumCheck-after.txt`) plus the read-only digests in §3.2. `bash -n`/`py_compile` of the lesson is not applicable (markdown).

## 6. Absences, blockers, and boundaries

- `BLOCKED:` none for the item's own gate. Four receipts that would have strengthened the lesson were absent when it was written: `SentScopeFinal.md`, `RevGateSpot.md`, `MutErratumCheck.md`, `ScribeQualityFix.md` (presence check §1, `2026-10-26T00:38:31Z`). Their subjects are recorded as unverified/open in the lesson (`## Open items` items 10–12), not asserted.
- `ScribeShonen` / `SHONEN.md` state is not asserted (owner had not filed).
- No final integration commit exists in the inspected evidence; the lesson carries the literal placeholder only, and the post-commit gate is stated as owed.
- Nothing outside the lane was written; no package file was read from a write path; `/home/vgpnk/Projects/shokuknow/merge/kasegi/` was not touched or executed.

## 7. Report trailer

`Report: .ufo/waves/round-31/wave2/ScribeLesson.md` (this file) — and the lesson itself at `corpus/lessons/round-31.md`, sha256 `be2c993e30047f694740d425ca0ba248c1911c2b08076d139657f63ee896a1f5`, 149 lines, 50258 B.
