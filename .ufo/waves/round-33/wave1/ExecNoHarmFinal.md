# ExecNoHarmFinal — round-33 no-harm sweep on final bytes

Seat: `ExecNoHarmFinal` (executor, leaf). Round: kasegi-shokunin round 33, hyaku run 8.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write scope).
Base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; claims freeze `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`.
Answering model (rule 10, session route, not passed by this seat): `opencode-go/deepseek-v4.1-flash`.
Write scope exercised: this receipt only (`.ufo/waves/round-33/wave1/ExecNoHarmFinal.md`). No lane content file touched; no
git/jj mutation (read-only `rev-parse`/`status`/`diff`/`show`/`archive`/`ls-tree`/`grep` only); no installs or upgrades
(rule 5 unused); no network fetch; no live target contacted (rule 8). Scratch: `$HYAKU_SCRATCH/kasegi-r33/ExecNoHarmFinal`
(`/fast/scratch/hyaku/kasegi-r33/ExecNoHarmFinal`), removed before yield after this receipt was written (rule 12) — every
figure below is inlined, nothing is cited from a scratch path.

Sweep trigger: receipts polled with `until [ -s … ]`/count loops (cap per rule 9) until the wave settled past the assigned
`>=40` threshold. Capture point: **53 receipts** (of 64 seats), lane HEAD **`9f9848816503aa0cd566fc2efdc5e69ea501a253`**
(`round-33: wave-1 integration (C1 capture-binding-check + manifest binding; C2 F16 admitted; wave receipts)`), working tree
= HEAD plus three in-flight receipt appends. The 11 seats whose receipts had not landed at capture: `CritMistakes`,
`ExecScratchDiscipline`, `ExecWaveEvidencePack`, `RevC1BeforeAfter`, `RevGateSpot`, `ScribeLesson`, `ScribeReportDraft`,
`ScribeScorecard`, `ScribeShonen`, `SimplifierCleanup`, and this seat.

Measured-file pin (sha256, taken after the sweep; SKILL/`SOURCES` hashes equal `git show HEAD:<path>`):

```
b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84  SKILL.md
b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b  corpus/SOURCES.md
3779e77f07a2d76119a074f598389d35353e01a4651cec8c75201c770f754932  corpus/README.md
00781e095d808e18e733830931d7cb8b279b1d045848ed3901d33de403b0b087  corpus/QUALITY.md
15dd603ec3cb47fa9dc181f2010790a858c437dedc2184ffcd1fe0eae40139ba  corpus/instruments/README.md
3f68b9a2ff7db654770bc11cb3b178b3d2920cc8e5ca0ba9761d85a65ab81ceb  corpus/instruments/knowledge-expected.txt
b57de5d9517d0ba67a7317d66f5ccc270b4e4a206ace8f27e20e9ec964abd679  PROVINCE.md
1f7ac0a2c39a0fbfdbee2ecbe112316dfc1bf7095b18cb8fb4eb9d6dfce171d1  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9  corpus/instruments/capture-binding-check.py
```

`git show HEAD:SKILL.md | sha256sum` → `b11b6085…3ed84` and `git show HEAD:corpus/SOURCES.md | sha256sum` →
`b22c7f01…4d13b`: the density/anchorcheck runs below are on the committed bytes, not an in-flight draft. The census run
was made on a fresh `git archive HEAD` extraction, because the seat entry was corrected between my working-tree snapshot
and the integration commit (`source: S049 … “提交漏洞时…”` line now reads `L210-211` in HEAD, was `L211` in the snapshot);
the HEAD numbers are the ones reported.

## 1. `git status --porcelain` classified against FILE OWNERSHIP

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git rev-parse HEAD
9f9848816503aa0cd566fc2efdc5e69ea501a253
$ git status --porcelain -uall
 M .ufo/waves/round-33/wave1/ExecDeterminism.md
 M .ufo/waves/round-33/wave1/ExecEntryF16.md
?? .ufo/waves/round-33/wave1/ExecGrowthMeasurement.md
```

All three working-tree paths are seat receipts for their own seats (`OWNED`); **working-tree unowned writes: 0**.

Full round (`git diff --name-only BASE HEAD`, each path mapped to the ownership list):

```
SUMMARY owned=71 l1=23 unowned=57
```

- `owned=71` = 52 seat receipts (`wave1/<Seat>.md`) + 18 content paths by their single writers
  (`PROVINCE.md` ScribeProvince; `SKILL.md` ScribeSkillGate; `corpus/QUALITY.md` ScribeQuality; `corpus/README.md`
  ScribeReadmeF16; `corpus/SOURCES.md` ExecRegistryAppend; `corpus/instruments/README.md` ScribeInstrReadme;
  `corpus/instruments/knowledge-expected.txt` ExecExpectedList; `corpus/instruments/capture-binding-check.py`
  ExecCaptureBinding; `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` ExecEntryF16; the eight
  `corpus/source-snapshots/round-{23,24,25,26,28,29,30,31}/manifest.json` ExecManifestUpgrade;
  `corpus/source-snapshots/round-32/manifest.json` ExecManifest32) + `LOG.md` (owner: the L1).
- `l1=23` = freeze/dispatch scaffolding (`claims.json`, `claims-erratum-1.md`, `census-before.txt`,
  `watchdog-digest.txt`, `build-spec.py`, `wave1-spec.json`, `wave1-dispatch.json`, `wave1-plan.*`, `wave1-run.err`,
  `wave1.ready`, `assimilation/`, `c1-controls/`, `c2-controls/`, `l1-ref/`) plus `wave1/swarm-registry.json`.
- `unowned=57` — **UNOWNED writes (the one defect of this sweep)**. Every one is a per-seat evidence *directory* under
  the wave report dir, which the FILE OWNERSHIP list does not grant (it grants only `wave1/<YourName>.md`):

```
16  .ufo/waves/round-33/wave1/ExecCaptureBinding/   (76K)
22  .ufo/waves/round-33/wave1/ExecRegressionC1/     (160K)
11  .ufo/waves/round-33/wave1/ScribeInstrReadme/    (52K)
 8  .ufo/waves/round-33/wave1/ScribeSkillGate/      (104K)
```

  All 57 are committed in HEAD `9f98488`; total 392K, 0 symlinks, none outside `.ufo/waves/round-33/wave1/`, none a
  lane content path. Classification: **advisory boundary drift, not content harm** — every seat hands its commands and
  outputs in prose-then-fenced form in its own receipt, and these dumps duplicate that evidence. Prior rounds hold the
  same pattern (`git ls-tree -r HEAD .ufo/waves/round-31/wave1/` contains `ExecCensusDry/validate/…`), so the list, not
  the behaviour, is what diverges from practice. Recommendation (L1): either extend next round's ownership list to
  `wave1/<YourName>/` evidence dirs, or drop the dumps. 8 of the 57 embed scratch absolute paths that will not exist
  after cleanup (`ExecCaptureBinding/{exit2-and-noharm.txt,prestate.txt}`,
  `ExecRegressionC1/{anchor-base.txt,anchor.txt,git-diff-SKILL-PROVINCE.patch}`,
  `ScribeInstrReadme/exit2.txt`, `ScribeSkillGate/{anchor-after3.txt,anchor-final.txt}`); no credential material, no
  session URL and no token was found in them (`git grep -n -I -E "/fast/scratch|/tmp/|HYAKU_SCRATCH|password|passwd|
  api[_-]?key|BEGIN (RSA|OPENSSH|PRIVATE)"` returned only the scratch paths and a `…nopasswd-argument-injection…`
  claim slug).

## 2. `diff --stat BASE` — only owned paths changed

```
$ git diff --stat 690b69da HEAD | tail -1
 151 files changed, 18434 insertions(+)
```

Path-space of that diff: 23 L1-scaffolding paths, 52 seat receipts, 19 non-receipt content paths (18 seat-owned +
`LOG.md`, owner the L1), and the 57 unowned evidence dumps of §1. **No lane content path was changed by a non-owner;
no unowned path exists outside the wave report dir.** The pre-commit capture (`git diff --stat HEAD`, 15 files / 368
insertions) held the same property for everything then uncommitted.

Append-only ownership clauses (R6) held at line level — `git diff --numstat 690b69da HEAD -- <paths>`:

```
4	0	LOG.md
2	0	PROVINCE.md
19	0	SKILL.md
55	0	corpus/QUALITY.md
26	0	corpus/README.md
6	0	corpus/SOURCES.md
145	0	corpus/instruments/README.md
1	0	corpus/instruments/knowledge-expected.txt
```

Deletions are 0 in every append-only file, and the eight upgraded manifests show 12/57/15/3/6/9/9/3 insertions, 0
deletions. The READ-ONLY instruments (`limb-mutation-check.py`, `limb-ledger.json`, `recheck-audit.py`,
`source-recheck.py`, `frontier-recheck-count.py`, `anchorcheck.py`, `density.py`, `resolve.py`, `score-gap.py`) do not
appear in the diff at all.

## 3. Density — same verdict class as base, higher density

```
$ git show 690b69da:SKILL.md > SKILL.base.md
$ python3 density.py SKILL.base.md --label r33-base ; echo exit=$?
# Density census — r33-base (1071 lines, 24 blocks)
| | **mean dens** | | | | | | | | **191.5** |
Total path-citation instances: 689 across 24 blocks.
exit=0
```

```
$ python3 corpus/instruments/density.py SKILL.md --label r33-final2 ; echo exit=$?
# Density census — r33-final2 (1090 lines, 25 blocks)
| | **mean dens** | | | | | | | | **201.7** |
Total path-citation instances: 710 across 25 blocks.
exit=0
```

Verdict class unchanged (exit 0, every block measured; no empty/thin-block regression). The appended round-33 gate row
adds one block, 19 lines, 21 citation instances; mean density rises 191.5 → 201.7.

## 4. Anchorcheck — same verdict classes as base

```
$ KASEGI_LANE_ROOT=$PWD python3 anchorcheck.base.py SKILL.base.md ; echo exit=$?
== SKILL.base.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
class counts: 306 LOST-RECORDED, 7 OK
exit=0
```

```
$ KASEGI_LANE_ROOT=$PWD python3 corpus/instruments/anchorcheck.py SKILL.md ; echo exit=$?
== SKILL.md: 12 in-range cite instances, 0 bad; 12 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
class counts: 306 LOST-RECORDED, 12 OK
exit=0
```

Same classes, same counts for the fail classes and for LOST-RECORDED (306 both sides); 5 more in-range anchors resolve
(7 OK → 12 OK) and none fail. Replicated on the committed tree with
`KASEGI_LANE_ROOT=<HEAD archive> anchorcheck.py SKILL.md` → identical line, exit 0.

## 5. resolve.py — lane rate vs the committed census (scratch copy only, never in the lane)

`resolve.py` writes `citation-survival.*` beside itself, so every run below was in a scratch tree
(`/fast/scratch/hyaku/kasegi-r33/ExecNoHarmFinal/{base-tree,head-tree}`); the lane's own
`corpus/instruments/citation-survival.{md,tsv}` still carry mtime `2026-10-25T04:15:16` and do not appear in
`git status`.

```
base tree (git archive 690b69da, 88 corpus md files):
distinct=2516 resolves=28 mirror=0 internal=386 other=0 gone=2102 skill=55/547 corpus=395/2180 all=414/2516

HEAD tree (git archive 9f98488, 89 corpus md files):
distinct=2563 resolves=28 mirror=0 internal=410 other=0 gone=2125 skill=70/563 corpus=412/2219 all=438/2563
```

Report rates from the HEAD-tree census (as published in the census file itself):

```
SKILL.md alone: 70/563 = 12.43%
corpus alone:  412/2219 = 18.57%
lane total:    438/2563 = 17.09%
```

Baseline and committed figures:

```
base bytes re-measured now (same instrument, same method):  414/2516 = 16.45%  (SKILL 55/547 = 10.05%)
committed census corpus/instruments/citation-survival.md:  134/1480 =  9.05%  (SKILL 32/506 = 6.32%, corpus 118/1153 = 10.23%)
```

**Continuity caveat, not a regression:** the committed census was generated in round 20 (`644ed37`) over a 50-file
scope; today's scope is 88 (base) / 89 (final) corpus md files, because the corpus grew in rounds 21-32. The committed
9.05 % is therefore not scope-comparable to a current run. Against the comparable base-bytes measurement the lane rate
moved **+0.63 pp** (16.45 % → 17.09 %). Likewise RESOLVES stays 28, MIRROR-EQUIVALENT stays 0, INTERNAL adds 24
(386 → 410) and GONE adds 23 (2102 → 2125). These are whole-tree figures, so they are not attributable to this round
alone. [INFERENCE] The added tallies are consistent with the round's appended material contributing resolvable
citations rather than new dangling ones, but the per-round split was not measured.

## 6. Fleet root — no misroot from these seats (report only)

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kake.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kasegi.report-baseline
 M .ufo/state/kengaku.report-baseline
 M .ufo/state/kotoba.report-baseline
 M .ufo/state/kotodama.report-baseline
 M .ufo/state/kumitate.report-baseline
 M .ufo/state/mado.report-baseline
 M .ufo/state/mori.report-baseline
 M .ufo/state/revenger.report-baseline
 M .ufo/state/souji.report-baseline
 M .ufo/state/tabi.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
 M scripts/hyaku/hyaku.env
 M scripts/hyaku/lane-addendum.md
?? .scratch/goal-20261026-hyaku-run8.md
?? .tower/
?? .ufo/state/disk-guard.log
?? .ufo/state/inline-dispatcher.log
?? .ufo/waves/round-30/
?? demo-cwd.txt
$ git -C /home/vgpnk/Projects/shokunin status --porcelain | grep -E 'kasegi-shokunin/'
none
```

No path of this lane appears in the fleet-root status, and no kasegi seat wrote a file at the fleet root:
`find /home/vgpnk/Projects/shokunin -path ./.git -prune -o -newermt '2026-10-26 01:15:00' -type f -print` (excluding
`.git`) groups into sibling lane repositories (`kengaku-shokunin/`, `tabi-shokunin/`, `tsukuroi-shokunin/`,
`souji-shokunin/`, `kaidoku-shokunin/` — their own `.git/.jj/.ufo/corpus` activity), the fleet root's own `.jj/repo`,
hyaku's `.ufo/state` files, and this lane under `kasegi-shokunin/`; no path exists outside those. The listed
fleet-root deltas pre-date the wave: `hyaku.env` 00:51:31, `lane-addendum.md` 01:05:01, `demo-cwd.txt`
2026-10-25T20:54:49, `.tower/` 2026-10-24/25, `round-30/` 2026-10-25T15:58:07; `.scratch/` gained no file after 01:15.
Repo roots confirmed distinct: lane `git rev-parse --show-toplevel` = `…/kasegi-shokunin`, fleet root = `…/shokunin`.
No deletion attempted.

## 7. Supplementary read-only check on the final bytes (not part of the assigned sweep)

```
$ python3 corpus/instruments/capture-binding-check.py ; echo exit=$?
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
exit=0
```

The `multi_row_url=2` is the informational count legalised by the L1's `claims-erratum-1.md` §Ruling 4 (S024/S029 and
S006/S028 share a URL); it is disclosed, exits 0, and is not an unbound record. This is evidence only — C1 scoring
belongs to `RevC1Instrument`/`CritC1Kill`.

## 8. Risks / blockers

1. **Serial tail not yet landed at capture (11 seats).** `ScribeLesson` owns `corpus/lessons/round-33.md`, which does not
   exist yet and is inside resolve.py's `corpus/**/*.md` scope; its later commit will add a new corpus file and move
   the census denominators (direction not predictable from zero bytes). `ScribeScorecard` (`SCORECARD.md`) and
   `ScribeShonen` (`SHONEN.md`) are outside the resolve scope (root-level files) and cannot move §5; `ScribeReportDraft`,
   `SimplifierCleanup`, `ExecScratchDiscipline`, `ExecWaveEvidencePack`, `CritMistakes`, `RevC1BeforeAfter`, `RevGateSpot`
   write no lane content path. The sweep therefore pins `density`/`anchorcheck` to committed `SKILL.md` (hash-equal to
   HEAD) and resolve to HEAD `9f98488`; a post-sweep integration commit containing the lesson file needs only a
   `resolve.py` re-run, not a re-sweep. Post-capture writes re-checked before this receipt was written (receipts
   53 → 55, last check `ScribeShonen.md` new): the nine measured-file sha256 values above are unchanged and the only
   lane content path that moved is `SHONEN.md` (ScribeShonen, root-level, outside the resolve scope); HEAD is still
   `9f98488` and `corpus/lessons/round-33.md` still absent.
2. **57 unowned evidence files (392K)** committed in the wave report dir (§1); 8 embed scratch absolute paths.
   Advisory: no content harm, and the same pattern exists in round-31. The still-running tail seats (`ScribeLesson`,
   `SimplifierCleanup`, `ExecScratchDiscipline`, `ExecWaveEvidencePack`, `CritMistakes`, `RevC1BeforeAfter`,
   `RevGateSpot` — their named dirs were present under `$HYAKU_SCRATCH/kasegi-r33/` at yield) may add further `<Seat>/`
   evidence dumps of the same class; none of them owns a lane content path besides `ScribeLesson`'s lesson file.
3. The knowledge entry was corrected between my first working-tree snapshot and HEAD (quote anchor `L211` → `L210-211`);
   the HEAD-tree census is the authoritative one reported here.
4. No blocker for this seat: every assigned command ran and exited 0.

## 9. Scratch cleanup

`/fast/scratch/hyaku/kasegi-r33/ExecNoHarmFinal` (base archive, working-tree copy, HEAD archive, classifier, capture
logs) was deleted after this receipt was written; nothing in this receipt depends on a surviving scratch path.
