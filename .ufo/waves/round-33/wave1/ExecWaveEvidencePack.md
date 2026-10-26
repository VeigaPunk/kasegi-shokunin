# ExecWaveEvidencePack — round-33 wave1 receipt index (the index the report cites)

Seat: ExecWaveEvidencePack (executor, leaf; no subagents, no own swarm, no delegated work).
Model actually run on: `opencode-go/deepseek-v4.1-flash` (route-table decision reported by the
session runtime; never passed by this seat). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; this receipt is the only
path this seat wrote. Lane base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; claims freeze
`6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`; lane HEAD during the run
`a6a502351bb90c8cd6d9b8f45f55109b7848e0d1` (spec/dispatch commit; seats do not commit, the L1 does).
Tooling: nothing installed or upgraded — no pacman transaction (host-wide pause respected), no
uv/npx/official binary; stdlib `python3` plus coreutils `sha256sum`/`ls`/`du` only.

## 0. Result in one paragraph

At census `2026-10-26T05:00:41Z`, `.ufo/waves/round-33/wave1/` held **63 peer receipts** against
**64 expected seats** (the `swarm-registry.json` member set): 0 zero-byte receipts, 0
duplicate-sha256 groups, 0 unregistered `*.md`, and 958,851 indexed receipt bytes. Every
indexed receipt's sha256 was recomputed and **63/63 matched** the table (§4).
No expected seat was missing a receipt at census: 63 peer rows plus this file cover all 64 registry seats. This seat's own receipt is deliberately
**excluded from its own table** — rewriting it would change the hash it printed; its sha256 is
whatever `sha256sum .ufo/waves/round-33/wave1/ExecWaveEvidencePack.md` reports at any later time. The 5 subdirectories in the wave dir (`ExecCaptureBinding/`, `ExecRegressionC1/`, `ScribeInstrReadme/`, `ScribeSkillGate/`, `SimplifierCleanup/`, 274,365 B total)
are seat scratch trees, not receipts; they are unhashed here and belong to
`SimplifierCleanup`'s report.

## 1. Method and exact commands

Expected-seat set (64) read from the wave's own registry, not from memory:

```
$ python3 -c "import json;m=json.load(open('.ufo/waves/round-33/wave1/swarm-registry.json'))['members'];print(len(m))"
64
```

Index generation (stdlib, read-only, `--root` argument; source in Appendix A):

```
$ python3 render-index.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --census-utc 2026-10-26T05:00:41Z > index.md
$ echo $?
0
```

Per-receipt field extraction: sha256 over raw bytes; seat name = file name minus `.md`;
verdict tokens matched case-insensitively on word boundaries (`PASS|FAIL|ADMIT|REFUSE|killed|
survivor|clean|defect|BLOCKED`) with per-token counts; the one-line column is the first line
carrying the highest-priority token **preferring a line that also says verdict/result/outcome/
conclusion/status**, else the first token hit, else a labelled fallback (`no-token`) so no row is
silently blank.

## 2. Polling history (why §3 is an after-state of a trickling wave, not PRE-STATE)

Three bounded polls of `ls "$WD"/*.md | wc -l` (20 s interval), each stopped on its own rule:

| poll | window (UTC) | receipts start -> end | stopped by |
|---|---|---|---|
| 1 | 04:17:23 -> 04:42:23 | 1 -> 53 | 1500 s cap (the last arrival was 04:39:43Z) |
| 2 | 04:42:29 -> 04:44:29 | 53 -> 53 | quiescent: no new file for 120 s |
| 3 | 04:44:36 -> 04:49:36 | 53 -> 55 | 300 s cap; arrivals 04:46:56Z (+1) and 04:48:56Z (+1) |

Poll 1 intermediate counts were monotonically non-decreasing (1,3,4,5,6,8,10,11,13,14,15,17,18,
19,20,21,23,24,25,27,29,30,32,33,34,35,37,38,39,40,42,43,44,45,46,48,50,51,52,53). The three loops
were shell calls the harness moved to background job ids `bg_328`, `bg_1310`, `bg_1383` after 60 s;
this seat awaited each to completion and started no other job. The wave was still trickling at the
cap (two receipts in the last five minutes); between poll 3's end (04:49:36Z) and this census
7 peer receipts have an mtime newer than 04:49:36Z, i.e. appeared or were rewritten
after poll 3 (`ScribeScorecard.md` 04:51:22Z, `RevC1BeforeAfter.md` 04:52:01Z, `ScribeLesson.md` 04:53:51Z, `RevGateSpot.md` 04:55:58Z, `ExecScratchDiscipline.md` 04:56:09Z, `CritMistakes.md` 04:59:38Z, `ScribeReportDraft.md` 05:00:31Z), so the wave was still trickling and late or revised receipts may exist
beyond this index; §5 gives the exact re-run.

## 3. Receipt index

## A. Receipt census (census_utc 2026-10-26T05:00:41Z)

| metric | value |
|---|---|
| expected seats (`swarm-registry.json` members) | 64 |
| receipt files present | 63 |
| expected seats with a receipt | 64 |
| expected seats without a receipt | 0 |
| extra files (not `*.md`) | 0 |
| extra `*.md` not in the registry | 0 |
| zero-byte receipts | 0 |
| total receipt bytes | 958851 |
| duplicate-sha256 groups | 0 |
| token totals | PASS=518, FAIL=186, ADMIT=17, REFUSE=13, killed=23, survivor=37, clean=43, defect=82, BLOCKED=19 |

## B. Receipt index (every `*.md` in the wave dir)

| # | receipt | seat | sha256 | bytes | mtime (UTC) | tokens | one-line verdict |
|---|---|---|---|---|---|---|---|
| 1 | `ConnClaims.md` | ConnClaims | `9bff4afc112800d77053d0a6d4cba5060346f063817ebb4f29b5f03a346d6937` | 14545 | 2026-10-26T04:24:31Z | PASS=19, FAIL=4, clean=1 | predicate asserts a conjunct the claim's own apparatus cannot fail. Mitigation is |
| 2 | `ConnOwnership.md` | ConnOwnership | `f376e648dfd049be62461cdc0370836408271e8ab6ad0b26f5fba453b8d3a568` | 20387 | 2026-10-26T04:30:41Z | defect=3 | Cycle check: every edge points from a later consumer to an earlier producer; no mutual wait exists (checked pairwise over the edge list above; e.g.... |
| 3 | `ConnSibling.md` | ConnSibling | `5862b0685479d8db39cf5eb7da569c87964e264e302d5a85ca65c84634f23587` | 8237 | 2026-10-26T04:17:28Z | - | Result: ZERO hits for every F16-scoped term in all six siblings. |
| 4 | `CritBoundary.md` | CritBoundary | `26fc75a37144613e43d63d2446c40c152d782a9e04c26c1824546a5fbe441f5c` | 12128 | 2026-10-26T04:31:14Z | defect=4 | credential material reproduced.** One routed wording defect in the entry (called out below, §8); |
| 5 | `CritC1Kill.md` | CritC1Kill | `b2f430ac2438b1f805ccbba98abd58785db54137e438fcc2db7fe89cf4a255d1` | 16031 | 2026-10-26T04:25:04Z | PASS=4, FAIL=9 | - Byte-integrity rebuttal: **confirmed** — see Verdict 4 and the SR evidence block; 40/40 sha pins pass today. |
| 6 | `CritC2Kill.md` | CritC2Kill | `6cd2c576eb2f3b5344ba8e49a32a35faebf4d7261e243ac355ffce66d4152a0c` | 22636 | 2026-10-26T04:34:50Z | PASS=13, REFUSE=3, survivor=1, clean=1, defect=3 | **Kill-rule wording defect.** The clause "does not name CNVD and 360SRC as the stating parties" |
| 7 | `CritExpansion.md` | CritExpansion | `948adaa76d184c95b66cc041c70981f3d929509cb9e6997897369feab9dcc321` | 24004 | 2026-10-26T04:27:56Z | clean=2, defect=2 | remaining defect is the scope half of the adds-section (§6). |
| 8 | `CritMistakes.md` | CritMistakes | `fd28a750505ca62eb6cd6713509ffcbac51407ac181bd99cbbb261c2e6afde35` | 20188 | 2026-10-26T04:59:38Z | PASS=12, FAIL=21, killed=1, survivor=13, defect=13, BLOCKED=11 | Verdict on item 2: the Mistakes section **covers every sweep-word hit** (BLOCKED/DEFECT/survivor/ |
| 9 | `ExecBeforeReceipts.md` | ExecBeforeReceipts | `55d7528ae93339335df83d0f84ea69fffc4158d052d7a4fab77ded44b0987e68` | 16887 | 2026-10-26T04:19:39Z | PASS=20, FAIL=1 | - Fake checker on the base manifests: `records=38 bound=38 unbound=0`, `fake_exit=0`, with `with_url=0` on the same bytes — the kill-rule clause it... |
| 10 | `ExecCaptureBinding.md` | ExecCaptureBinding | `cd983e18d90612928e0e7b9bfe0ce0f02d0f7a30a0a4657349ad2e1d44a797f4` | 17675 | 2026-10-26T04:29:26Z | PASS=15, FAIL=13, killed=8, clean=2 | verdict=killed |
| 11 | `ExecCensusAfter.md` | ExecCensusAfter | `af39be84284c37ed4541d9a0d90727ae21a4a02e386f79ffbc68f4a70241998c` | 5630 | 2026-10-26T04:34:59Z | - | status=mined=38 queued=9 rejected=3 |
| 12 | `ExecCensusDry.md` | ExecCensusDry | `b74d8c70a87be177245377a5786076da6d8aaec89722b3b3858031614fde8ea2` | 13248 | 2026-10-26T04:21:10Z | PASS=1 | PASS. With the planned rows the mirror's `sources-census.sh validate --file` exits 0 and shows only the base |
| 13 | `ExecDeterminism.md` | ExecDeterminism | `faa1271f6390c3f8770b6c8fc0fc10352d88a94c02da57d7c84ea8da7742daef` | 17557 | 2026-10-26T04:40:02Z | PASS=26, FAIL=2, clean=1 | selftest case=clean-all-pass exit=0 want=0 verdict=pass |
| 14 | `ExecEntryF16.md` | ExecEntryF16 | `c99e4e1a3f03ebdca1cd70dfddecbba35824c5de92321b884a97353ceab5d3e0` | 23355 | 2026-10-26T04:38:03Z | PASS=16, FAIL=1, ADMIT=1, REFUSE=1, clean=1, defect=2 | FAIL F16 knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050 exit=- problems=header-sources-not-rechecked |
| 15 | `ExecErratumCheck.md` | ExecErratumCheck | `2f67a145f26b62a98b009e7adcfa278e55ab2b15d06cb9ed0b5d4df81cb50eef` | 19952 | 2026-10-26T04:21:57Z | PASS=22, FAIL=23 | bytes at a scratch tree (that is how the able-to-fail controls in §6 run), `--checks` selects a |
| 16 | `ExecExpectedList.md` | ExecExpectedList | `dce17bc799e25d1568eb602fad226bbc72e7ee3e11e0df6dd81c29bd11449b2d` | 10766 | 2026-10-26T04:31:09Z | PASS=12, FAIL=4, clean=1, BLOCKED=1 | BLOCKED: none. |
| 17 | `ExecForeignCwd.md` | ExecForeignCwd | `14e4b0609e971c7e731a9187d40b2a7107b6b86e9e96cc4d2d4553221b65fb09` | 20759 | 2026-10-26T04:36:05Z | PASS=44, FAIL=1, clean=1, defect=1 | **Verdict: exit 0, strict `pass=45/45`, as expected.** `executes=21` is the base's 20 plus the new |
| 18 | `ExecGrowthMeasurement.md` | ExecGrowthMeasurement | `d9c9e1121d16456dc18f558e3c0689238dbdd731921f03c6bf8114bcde5854d9` | 10780 | 2026-10-26T04:41:17Z | defect=1 | The two `ScribeSkillGate` anchor dumps are the same size but **different bytes** (`sha256 7c037484…` vs `2ef8fb8f…`), so they are a near-duplicate ... |
| 19 | `ExecHarnessC2.md` | ExecHarnessC2 | `68aa2d5e63a2d6ab4ffe899d74da1efb0f603575c687bc1db5b8161cba879924` | 16202 | 2026-10-26T04:34:13Z | PASS=25, defect=2 | None. All nine C2 counter commands met their kill-rule targets on quiescent bytes, so no defect message was due and none was sent. Two things a lat... |
| 20 | `ExecManifest32.md` | ExecManifest32 | `c113f1cae8e6dc9331b079d55ed986fc3b0c154e23b1f090bae703db3db49d7e` | 10479 | 2026-10-26T04:25:53Z | FAIL=2, defect=3 | FAIL rule=no-row record=S049 dir=round-32 |
| 21 | `ExecManifestUpgrade.md` | ExecManifestUpgrade | `df14046e92a51db2bbf79b0133caf4eff037cbeca28de2cb07d2293791ea523c` | 15638 | 2026-10-26T04:24:04Z | FAIL=8, defect=2 | FAIL rule=url-ambiguous record=S029 dir=round-23 rows=S024,S029 |
| 22 | `ExecNoHarmFinal.md` | ExecNoHarmFinal | `a30f282f2ea82863c49bfd19c9d1c17c26736aa5a6f1dc572bc97916cc72bcd2` | 16942 | 2026-10-26T04:48:58Z | FAIL=2, defect=1 | Same classes, same counts for the fail classes and for LOST-RECORDED (306 both sides); 5 more in-range anchors resolve |
| 23 | `ExecQuarantine.md` | ExecQuarantine | `47009600320aa3fe8cf6dd54a0041ead7ff75552d59e0623f2758cbe1d17a283` | 23356 | 2026-10-26T04:20:20Z | REFUSE=6, defect=1 | Result: **2 refuse, 5 unreachable, 0 adopted.** No file outside this receipt was written. |
| 24 | `ExecRegistryAppend.md` | ExecRegistryAppend | `858e7f29ccda2182c74b514b60bede169456b7aee707189031c28c11d47f765c` | 22560 | 2026-10-26T04:29:50Z | PASS=1, clean=1, defect=1 | $ git status --porcelain corpus/SOURCES.md → (no output: clean at base) |
| 25 | `ExecRegressionC1.md` | ExecRegressionC1 | `9e459c9d061d35fc6198145aef67a0ec6163eb409b16665663f95bb9b0c2fbbd` | 19070 | 2026-10-26T04:34:45Z | PASS=33, FAIL=6, clean=2, defect=1 | selftest case=clean-all-pass exit=0 want=0 verdict=pass |
| 26 | `ExecScratchDiscipline.md` | ExecScratchDiscipline | `41825632a219ad0717f459a1c37d67bf8a8c8b4e272c48b790b442fa55f5ba9d` | 26553 | 2026-10-26T04:56:09Z | PASS=24, clean=4, defect=8 | selftest case=clean-all-pass exit=0 want=0 verdict=pass |
| 27 | `MutCtrFetchMissing.md` | MutCtrFetchMissing | `2ef9b6599b4df9c7aabac38dadf65569837599637e104910a2c0569882493dda` | 9066 | 2026-10-26T04:21:04Z | PASS=1, FAIL=6, killed=2, survivor=2 | selftest case=round-32-record-without-fetched_utc exit=0 want=1 verdict=fail |
| 28 | `MutCtrSelftestSkip.md` | MutCtrSelftestSkip | `b3cdbcd8122cb756a3329e2d5b67d743ee0a93ed326c452b4014192857adb1b9` | 7414 | 2026-10-26T04:25:16Z | PASS=14, killed=1, clean=1 | **KILLED.** Catching clause: **"failures=0 lines printed from real cases"** — the forged `cases=0 failures=0` summary is self-incriminating (it rep... |
| 29 | `MutCtrUnbound.md` | MutCtrUnbound | `36fc4a469b63ad77cf5576b64f78637cf8f1e119575406d691b145436f3b3c5b` | 14713 | 2026-10-26T04:21:09Z | PASS=4, FAIL=21, survivor=4 | selftest case=record-without-url exit=0 want=1 verdict=fail |
| 30 | `MutCtrUrlMismatch.md` | MutCtrUrlMismatch | `e02c44b74bc734dca9bc28c9bedbdb67885cbf887a3b2f18e69db5a043fa6e2b` | 10370 | 2026-10-26T04:24:44Z | PASS=13, FAIL=6, killed=3, survivor=1, clean=4, defect=1 | **Verdict: KILLED.** On the primary fixture the mutant prints `records=2 bound=2 unbound=0` exit 0 — |
| 31 | `MutEntryF16.md` | MutEntryF16 | `ac1f57486e1ad313c88200f111d70873ffa53d9a62a21ebb0a451fe73df08aa8` | 12495 | 2026-10-26T04:37:34Z | PASS=39, FAIL=2, killed=1, survivor=2, defect=1 | ## Verdict: SURVIVOR (coverage finding) — reproduced on both tested digests (`53c48b3b…`, `1f7ac0a2…`) |
| 32 | `MutLegacyManifestDrop.md` | MutLegacyManifestDrop | `6e2b4448688a082802768500cb8b24a6f3d0b2d20f338cb62ed654f68f481d5b` | 9017 | 2026-10-26T04:26:40Z | PASS=12, FAIL=4, killed=2, survivor=2, clean=2 | selftest case=clean-all-pass exit=0 want=0 verdict=pass |
| 33 | `MutManifestLegacy.md` | MutManifestLegacy | `ef70362638c8646095463b0fa45d418e9f503199c0b3163ea5d9fda3671701ec` | 5956 | 2026-10-26T04:27:40Z | FAIL=4, killed=1 | First probe ran while ExecRegistryAppend had not yet appended rows S049/S050 to `corpus/SOURCES.md`: real tree exit=1, `records=40 bound=38 unbound... |
| 34 | `RevC1BeforeAfter.md` | RevC1BeforeAfter | `7d50d89bd52961c13de5ab321673a8d6d284399b0ce0a52f825ef3c18a62289d` | 13799 | 2026-10-26T04:52:01Z | PASS=14, FAIL=3, clean=2 | selftest case=clean-all-pass exit=0 want=0 verdict=pass |
| 35 | `RevC1Instrument.md` | RevC1Instrument | `ae70bb2a2a4729ff74ee58557c22c3b26e177c153bbbbec7dd5e7c6ed9f18807` | 10147 | 2026-10-26T04:36:37Z | PASS=5, FAIL=12, clean=2, defect=1 | no row → `FAIL rule=no-row record=<id>`; len>1 → `FAIL rule=dup-id record=<id> rows=<n>`; |
| 36 | `RevCalibration.md` | RevCalibration | `f478f063d559310f3baeaa5a67bee512f32565461f886cf5768cc5db0896820e` | 15591 | 2026-10-26T04:32:40Z | PASS=13, FAIL=4, ADMIT=1, killed=1, defect=1 | The same counters printed three different states within ten minutes: 04:21Z knowledge=44-era audit green; ~04:27Z knowledge=45 with `unexpected=1` ... |
| 37 | `RevClaimsFreeze.md` | RevClaimsFreeze | `d60fe749a147074417a8935bdf4a0d290601ec61e8d45c4408d7f1d72462f1aa` | 22045 | 2026-10-26T04:23:34Z | PASS=6, FAIL=8, defect=1 | FAIL rule=missing-manifest dir=round-32 |
| 38 | `RevEntryF16.md` | RevEntryF16 | `ab5fe1ad51cbbcdaa839707cbe981ed802c397f3f90207c32b6b4eda9397f865` | 14063 | 2026-10-26T04:31:37Z | PASS=12, FAIL=2, ADMIT=1 | \| Q7 \| **pass** \| 7 \| The `recheck:` field is one command (human note after `#`), not prose. Its output names what was checked: 16 lines `S049:... |
| 39 | `RevGateSpot.md` | RevGateSpot | `46a823811eb876623bed33a0780e7595381a8f4279a3b2f122e1abc0598577c6` | 11216 | 2026-10-26T04:55:58Z | PASS=2, ADMIT=1, REFUSE=2, survivor=1, defect=2 | `absent-defect-register.md`; no campaign tool run, nothing written). Answering model actually |
| 40 | `RevManifestUpgrade.md` | RevManifestUpgrade | `79ab196846ef12ac13626822b15b66b33345ae6597e89aa5a90680152f38918f` | 8055 | 2026-10-26T04:25:50Z | PASS=2, FAIL=1, killed=1, defect=2 | - Low / cross-seat (needs L1 adjudication, not a manifest defect): rule-B multi-row semantics. The frozen contract text says a url matching "0 or 2... |
| 41 | `RevNoHarm.md` | RevNoHarm | `5275309222bf836bb71da94c56ed2e8de361508571b690cf4b4f86b87988b432` | 9776 | 2026-10-26T04:22:36Z | PASS=3, FAIL=1, defect=2 | lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0 |
| 42 | `RevQuoteSweep.md` | RevQuoteSweep | `ccc39543ac468651002a21e6cc215112d33c6766105b380d1913e5894786e299` | 8829 | 2026-10-26T04:35:45Z | defect=1 | after column; the PRE-STATE sweep found the same single defect, re-confirmed below. |
| 43 | `RevRowS049.md` | RevRowS049 | `b7c365cb1c1b3531cc47ba48b67442b2c7a73982411bbe06b46a47890555a400` | 17410 | 2026-10-26T04:31:03Z | ADMIT=1, clean=2, defect=1 | **ADMIT-ROW** — the landed S049 row (`corpus/SOURCES.md:55`, quiescent sha `b22c7f0173e75e0c…`) conforms to SOURCES contract v1 rules 1–6 on every ... |
| 44 | `RevRowS050.md` | RevRowS050 | `5163fd398a7e4033688541fef3c57b5b30ba20790514e14989fa1cd37653fe13` | 27259 | 2026-10-26T04:32:03Z | PASS=16, ADMIT=1, clean=4 | - **Verdict: ADMIT-ROW.** All six contract rules CONFORMANT at row level; every dispatched check passes on landed bytes. One LOW finding (rule-1 le... |
| 45 | `RevTranslation.md` | RevTranslation | `c88355d775908130186e737dd1cde02ca84c9a78e89773f024221926cd5f19c5` | 13792 | 2026-10-26T04:37:22Z | clean=1 | ## Verified-clean summary |
| 46 | `ScoutDatawalk.md` | ScoutDatawalk | `d9d95b4afce973099fdb50395c7948bd2b259363e65273d87d5e6c783d0b3da1` | 12680 | 2026-10-26T04:18:02Z | PASS=10, FAIL=1, defect=1 | lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0 |
| 47 | `ScoutF16Sweep.md` | ScoutF16Sweep | `b5df582db66f319aecb084a756711a707ffa96ca3801f194554932a5e1deb7b9` | 13631 | 2026-10-26T04:18:19Z | killed=1 | **What F16 adds that the lane lacks:** (1) the two Chinese platforms' own scope statements (customer-authorised scope only; vendor-published produc... |
| 48 | `ScoutLiveDrift.md` | ScoutLiveDrift | `156a45825638d6c15bd1d7be9a2b2a9870dd788a741277aa1f6325946745323c` | 2761 | 2026-10-26T04:16:47Z | - | Model: anthropic/claude-sonnet-5-5 (config route). Tooling installed: none. |
| 49 | `ScoutManifestAudit.md` | ScoutManifestAudit | `1408d453796dc365127c6db41056716916d41fc1b846d82e8daa59a424652a7e` | 19697 | 2026-10-26T04:18:08Z | PASS=1 | Seat: ScoutManifestAudit (kasegi-shokunin round 33). Tree audited: `git archive 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 corpus/source-snapshots co... |
| 50 | `ScoutPackageThemes.md` | ScoutPackageThemes | `8c00f0ba52838606a96b6a7c60cbf6fd414a799ac96bb403e7fe0927c9126aa5` | 24644 | 2026-10-26T04:22:53Z | PASS=2, ADMIT=3, REFUSE=1, defect=5 | 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833 corpus-expansion-1/absent-defect-register.md |
| 51 | `ScribeInstrReadme.md` | ScribeInstrReadme | `c2eb3478563c57ce1b928967ef0d4ef36bd60a3dfde31417d64ac69416c89838` | 11565 | 2026-10-26T04:30:30Z | PASS=1, FAIL=2, defect=1 | `--selftest` at the same digest: eleven `selftest case=… verdict=pass` lines, `selftest cases=11 |
| 52 | `ScribeLesson.md` | ScribeLesson | `fa21420182569a4f2cec3c920e61c14ebd8d7e7e534c973216fae1aff804494a` | 13206 | 2026-10-26T04:53:51Z | PASS=4, FAIL=3, survivor=5, defect=2, BLOCKED=5 | selftest case=pre-round-32-archival-passes exit=0 want=0 verdict=pass |
| 53 | `ScribeProvince.md` | ScribeProvince | `704a50c2e55c568f527d662779fc60ff00bd00fcbfc3f2a86d6887afa96bffa7` | 11261 | 2026-10-26T04:28:01Z | PASS=7, clean=1, BLOCKED=1 | short second poll was auto-backgrounded as `bg_555` and also saw the file). No `BLOCKED:` line is |
| 54 | `ScribeQuality.md` | ScribeQuality | `abc78a2bfd3afe0248267858b89e54f52c2c899794a10d0586a54b373d9ba5f3` | 10470 | 2026-10-26T04:18:44Z | - | `corpus/QUALITY.md`: appended `## Round-33 additions — a capture snapshot ships with its manifest (append-only)` after the pre-existing last line (... |
| 55 | `ScribeReadmeF16.md` | ScribeReadmeF16 | `d7f4d31083775fd2ddc0351ba217ec8f91657d74d28bf5b23131c3f64a578ee5` | 11770 | 2026-10-26T04:27:46Z | PASS=4, clean=1 | $ git status --porcelain corpus/README.md # empty: clean at HEAD |
| 56 | `ScribeReportDraft.md` | ScribeReportDraft | `39de3f823bdb865d4efebbe2d603e738a4bffcc789617f5e39bea59dea117cd7` | 36153 | 2026-10-26T05:00:31Z | PASS=13, FAIL=1, ADMIT=3, killed=1, survivor=4, defect=2, BLOCKED=1 | - Non-author reviewer: Q1–Q10 all `pass`, verdict ADMIT. Evidence: `wave1/RevEntryF16.md` §1. |
| 57 | `ScribeScorecard.md` | ScribeScorecard | `12ee8a20d8900deb13468ca30a1fa3a455adb0d1c9515acc639dd99e87f8b3ee` | 11822 | 2026-10-26T04:51:22Z | PASS=5, FAIL=1, ADMIT=3, survivor=2, defect=4 | \| `wave1/MutEntryF16.md` §digest history, §Verdict \| final digest `1f7ac0a2…`; the narrow-delta sentence; `SURVIVOR (coverage finding)` scoped to... |
| 58 | `ScribeSearchLog.md` | ScribeSearchLog | `f05b2d44be1bf9ffc6395c51691b3e936961a438713bcd8941068422225136db` | 14555 | 2026-10-26T04:30:40Z | ADMIT=1, defect=3 | \| counts \| identified 9 (the 9 rows of `ScoutPackageThemes.md`'s verdict table = 2 staged source rows that join by URL, S034/S035 of 94, plus the... |
| 59 | `ScribeShonen.md` | ScribeShonen | `dbca1ac86a1228e93f247ab3eb9be975eae4701f31976affc082134ab03bdcfd` | 9933 | 2026-10-26T04:49:27Z | PASS=6, FAIL=1, defect=1 | `0 bad`, same fail classes) and `wave1/ScribeSkillGate.md` §4/§5 (1090 lines, sha256 |
| 60 | `ScribeSkillGate.md` | ScribeSkillGate | `291b135a3e2a281f57681b67c537390af55b11184711ad170d38d9b7a7db0ed8` | 10595 | 2026-10-26T04:30:54Z | PASS=14, FAIL=5, clean=1 | \| verdict map \| exit 0 iff no `FAIL` line; 1 on any `FAIL`; 2 on `UNAVAILABLE reason=no-snapshot-tree\\|read-error\\|manifest-JSONDecodeError\\|m... |
| 61 | `SentCred.md` | SentCred | `3a18e437c89238be3a97f879df9333e377076e5d187357286fa8f62db7d05d0d` | 23181 | 2026-10-26T04:33:58Z | PASS=4, clean=2 | - **Independent corroboration (three seats).** `RevEntryF16.md:42` scores Q6 `pass`; `SentScopeFinal.md:15` prints `F3 CLEAN` “no credential, sessi... |
| 62 | `SentScopeFinal.md` | SentScopeFinal | `2d068f19da8169253d8fef6bf22969a42bebb9a64040ef7f1bcc8edf30e750c3` | 19998 | 2026-10-26T04:33:16Z | PASS=4, FAIL=1, ADMIT=1, clean=3 | fail `S029`/`S006` — the two readings cannot both be right. |
| 63 | `SimplifierCleanup.md` | SimplifierCleanup | `b479a13e1a42a92ad7a4d7425caeaa3be52afc73d7a94bf612d5ef778e9324f4` | 14351 | 2026-10-26T05:00:42Z | defect=2 | make three seats' receipts cite different paths for identical bytes. This is a *presentation* defect, |

## C. Dead-seat information (expected seat, no receipt at census)

- Self seat `ExecWaveEvidencePack`: its receipt **is this file** (`ExecWaveEvidencePack.md`), excluded from the table above because rewriting it changes the hash it printed; it is not a dead seat.

None: all 64 expected seats left a receipt at census time.

## D. Extras, empties, duplicates

- Non-`*.md` files in the wave dir (registry + any stray): none
- Subdirectories: `ExecCaptureBinding/`, `ExecRegressionC1/`, `ScribeInstrReadme/`, `ScribeSkillGate/`, `SimplifierCleanup/`
- Zero-byte receipts: none
- Duplicate sha256 receipts: none
- Unregistered `*.md` receipts: none

### Role coverage at census (command output)

| role | expected | receipt present (incl. self) | absent |
|---|---|---|---|
| connector | 3 | 3 | 0 |
| critic | 5 | 5 | 0 |
| executor | 19 | 19 | 0 |
| mutation-tester | 7 | 7 | 0 |
| reviewer | 12 | 12 | 0 |
| scout | 5 | 5 | 0 |
| scribe | 10 | 10 | 0 |
| sentinel | 2 | 2 | 0 |
| simplifier | 1 | 1 | 0 |
| **total** | 64 | 64 | 0 |

## 4. Cross-instrument hash verification

Independent of the generator: the table above was parsed with a regex, and each named file was
re-hashed from raw bytes with `hashlib` in a fresh process.

```
rows_parsed=63
verified=63 matched=63 mismatched=0
dir_md_count=64 (including this index file)
```

Post-write re-hash, immediately before this file was written (2026-10-26T05:00:41Z UTC): all rows still match their census bytes.

Post-hand-off note, measured at 05:01:12Z after this file was written: two rows no longer matched
their census bytes because their seats were still writing — `ScribeReportDraft.md` (table
`39de3f82…` 36,153 B at 05:00:31Z, rewritten at 05:01:00Z) and `SimplifierCleanup.md` (table
`b479a13e…` 14,351 B at 05:00:42Z, rewritten at 05:00:53Z). Those two rows bind the census bytes,
not their final ones. The remaining 61 rows were re-hashed at 05:01:06Z and still matched. Receipts
that land or change after 05:01:12Z are not tracked here; §5's re-run supersedes these rows. This
is wave churn, not index error.


## 5. Bounds on what this proves (Q7), and the exact re-run

- **Snapshot, not a closed wave.** The census is `2026-10-26T05:00:41Z` on the working tree the
  seats were writing. Receipts that landed after that instant are not rows here; no statement is
  made about them.
- **Token counts are lexical.** A `FAIL=8` row counts eight occurrences of the word in the file,
  including occurrences inside quoted command output, kill-rule tables and prose about rejected
  wording; it is **not** a verdict and must not be read as eight failures of the seat's work. The
  one-line column is the seat's own first verdict/result line where one exists.
- **Absence is not proof of no work.** A seat with no receipt may still have written its production
  file; the index says only that the wave record holds no receipt from it at census (§3C).
- **sha256 binds bytes, not intent.** The 63/63 match holds for the bytes present during §4
  (the §4 check finished inside the 2026-10-26T05:00:41Z minute). A seat rewriting its own receipt
  afterwards invalidates its row; the post-write re-hash in §4 names any such row instead of
  hiding it.
- **No live target was contacted and no network fetch was made by this seat**; no credential,
  session URL or vault material was read or quoted (the S049 page's platform-issued tester
  credentials were not opened). `/home/vgpnk/Projects/shokuknow` was not read or written by this
  seat.
- **Duplicate detection is sha256-identical only** — near-duplicates (same size, different bytes)
  are `SimplifierCleanup`'s and `ExecGrowthMeasurement`'s findings, not this index's.
- **Re-run after the wave closes** (byte-identical fields except census stamp and any late rows):
  `python3 render-index.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --census-utc <UTC>`; the script is reproduced in
  Appendix A and is the same one that produced §3.

## 6. Size, tooling, scratch discipline

Receipts at census (largest three, and the scratch subdirectories kept for the cleanup seat):

```
receipts=64 (incl. this index file)  peer_receipt_bytes=958878
largest peer receipts:
36153 ScribeReportDraft.md
27259 RevRowS050.md
26553 ExecScratchDiscipline.md
subdirs:
22430	ExecCaptureBinding/
95376	ExecRegressionC1/
14937	ScribeInstrReadme/
85682	ScribeSkillGate/
55940	SimplifierCleanup/
```

Scratch for this seat: `$HYAKU_SCRATCH/kasegi-r33/ExecWaveEvidencePack/` (`HYAKU_SCRATCH` default
`/fast/scratch/hyaku`), files and sizes before removal:

```
108327b10f117e68586e88e231e0e4db1e5b9f73178bc5c13ac0b15b3a3d4aab  assemble.py
d94be3a421bb345cad405a391c9dc57afd39ac4757310e355126a5284fdc6a03  census.txt
ba0f1a6b56bdaca57446c51181243f27ce36d4693892997af0f1b2f334a07b39  hash-check.txt
de2f31aabe35d60216bd9c7d6072f61fee216191786fb56331605635940addb0  index.md
e49f06dcf30c88cf5f6db945cbdffe34e8d49c16647e994f5b6a5dd541f370d4  index-wave.py
44f745e37afcd5a2880399b2da1f858d48a5c724806e40b3268d23ea37fcc702  receipt-draft.md
5502107671ae5a34c7ea5c4ca5dfe87e5cf3ad721ad80f27c61089a718682e71  render-index.py
9bec9240681d206179641c2a619599dd13b75124c69abd2cbddffaa50c79f29a  role-coverage.txt
8d1ec9e684aa7643307ba65dc69103920f937ebc73a5d7cb58526003292b4ae0  size-summary.txt
45804	total
```

Removed with `rm -rf -- "$S"` before this seat finished; nothing of this seat's scratch remained on
disk at hand-off. Tooling installed/upgraded: **none** (tool, version, channel, reason: no install
was needed or performed).

## Appendix A — index generator (the exact script that produced §3)

```python
#!/usr/bin/env python3
"""Render the round-33 wave1 receipt index as markdown (stdout).

Usage: render-index.py --root <lane> [--census-utc <stamp>]
Stdlib only; never writes into the lane.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time

TOKENS = ["PASS", "FAIL", "ADMIT", "REFUSE", "killed", "survivor", "clean",
          "defect", "BLOCKED"]
TOKEN_RE = re.compile(r"\b(" + "|".join(TOKENS) + r")\b", re.IGNORECASE)
PRIORITY = ["BLOCKED", "FAIL", "defect", "REFUSE", "killed", "ADMIT", "PASS",
            "survivor", "clean"]
FALLBACK_RE = re.compile(r"^(verdict|result|conclusion|summary|status|outcome)\b",
                         re.IGNORECASE)
NON_RECEIPT = {"swarm-registry.json"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def trim(s, n=150):
    s = " ".join(s.split()).replace("|", "\\|")
    return s if len(s) <= n else s[:n - 3] + "..."


VERDICTISH_RE = re.compile(r"\b(verdict|result|outcome|conclusion|status)\b",
                           re.IGNORECASE)


def verdict_line(text):
    lines = text.splitlines()
    # Prefer an explicit verdict/result line so the summary is the seat's own
    # conclusion rather than the first incidental token hit.
    for token in PRIORITY:
        for line in lines:
            found = {m.group(1).lower() for m in TOKEN_RE.finditer(line)}
            if token.lower() in found and VERDICTISH_RE.search(line):
                return token, trim(line)
    for token in PRIORITY:
        for line in lines:
            found = {m.group(1).lower() for m in TOKEN_RE.finditer(line)}
            if token.lower() in found:
                return token, trim(line)
    for line in lines:
        if FALLBACK_RE.match(line.strip()):
            return "no-token", trim(line)
    for line in lines:
        s = line.strip()
        if s and not s.startswith(("#", "|", "```", ">", "---", "-", "*")):
            return "no-token", trim(s)
    return "", ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--wave", default=".ufo/waves/round-33/wave1")
    ap.add_argument("--census-utc", default="")
    ap.add_argument("--exclude", action="append", default=[],
                    help="file name to omit (self-reference)")
    args = ap.parse_args()

    wd = os.path.join(args.root, args.wave)
    with open(os.path.join(wd, "swarm-registry.json"), encoding="utf-8") as fh:
        reg = json.load(fh)
    members = reg["members"]
    expected = sorted(members)

    entries = sorted(os.listdir(wd))
    receipts, extras, dirs = [], [], []
    for name in entries:
        path = os.path.join(wd, name)
        if os.path.isdir(path):
            dirs.append(name)
        elif name not in NON_RECEIPT and name not in args.exclude:
            seat = name[:-3] if name.endswith(".md") else name
            (receipts if name.endswith(".md") else extras).append((name, seat, path))

    rows = []
    totals = {t: 0 for t in TOKENS}
    hashes = {}
    for name, seat, path in receipts:
        st = os.stat(path)
        text = read_text(path)
        digest = sha256(path)
        counts = {}
        for m in TOKEN_RE.finditer(text):
            canon = next(t for t in TOKENS if t.lower() == m.group(1).lower())
            counts[canon] = counts.get(canon, 0) + 1
            totals[canon] += 1
        tok, line = verdict_line(text)
        hashes.setdefault(digest, []).append(name)
        rows.append({"file": name, "seat": seat, "sha256": digest,
                     "bytes": st.st_size,
                     "mtime": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                            time.gmtime(st.st_mtime)),
                     "counts": counts, "verdict": tok, "line": line,
                     "known": seat in members})

    present = {r["seat"] for r in rows if r["known"]}
    self_seats = [n[:-3] for n in args.exclude if n[:-3] in members]
    present |= set(self_seats)
    missing = [s for s in expected if s not in present]
    unknown = [r for r in rows if not r["known"]]
    zero = [r["file"] for r in rows if r["bytes"] == 0]
    dupes = {h: v for h, v in hashes.items() if len(v) > 1}
    census = args.census_utc or time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                              time.gmtime())

    out = []
    out.append("## A. Receipt census (census_utc %s)" % census)
    out.append("")
    out.append("| metric | value |")
    out.append("|---|---|")
    out.append("| expected seats (`swarm-registry.json` members) | %d |" % len(expected))
    out.append("| receipt files present | %d |" % len(rows))
    out.append("| expected seats with a receipt | %d |" % len(present))
    out.append("| expected seats without a receipt | %d |" % len(missing))
    out.append("| extra files (not `*.md`) | %d |" % len(extras))
    out.append("| extra `*.md` not in the registry | %d |" % len(unknown))
    out.append("| zero-byte receipts | %d |" % len(zero))
    out.append("| total receipt bytes | %d |" % sum(r["bytes"] for r in rows))
    out.append("| duplicate-sha256 groups | %d |" % len(dupes))
    out.append("| token totals | %s |" % ", ".join(
        "%s=%d" % (t, totals[t]) for t in TOKENS))
    out.append("")
    out.append("## B. Receipt index (every `*.md` in the wave dir)")
    out.append("")
    out.append("| # | receipt | seat | sha256 | bytes | mtime (UTC) | tokens | one-line verdict |")
    out.append("|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        c = ", ".join("%s=%d" % (t, r["counts"][t]) for t in TOKENS
                      if r["counts"].get(t)) or "-"
        out.append("| %d | `%s` | %s%s | `%s` | %d | %s | %s | %s |" % (
            i, r["file"], r["seat"], "" if r["known"] else " (unregistered)",
            r["sha256"], r["bytes"], r["mtime"], c, r["line"] or "-"))
    if not rows:
        out.append("| - | (none) | - | - | - | - | - | - |")
    out.append("")
    out.append("## C. Dead-seat information (expected seat, no receipt at census)")
    out.append("")
    for s in self_seats:
        out.append("- Self seat `%s`: its receipt **is this file** (`ExecWaveEvidencePack.md`), "
                   "excluded from the table above because rewriting it changes the hash it "
                   "printed; it is not a dead seat." % s)
        out.append("")
    if missing:
        out.append("| seat | role | information absent from the wave record |")
        out.append("|---|---|---|")
        for s in missing:
            out.append("| %s | %s | its assigned finding/artifact and its command output; "
                       "the report cannot cite it |" % (s, members[s].get("role", "?")))
    else:
        out.append("None: all 64 expected seats left a receipt at census time.")
    out.append("")
    out.append("## D. Extras, empties, duplicates")
    out.append("")
    out.append("- Non-`*.md` files in the wave dir (registry + any stray): %s" %
               (", ".join("`%s`" % name for name, _, _ in extras) or "none"))
    out.append("- Subdirectories: %s" % (", ".join("`%s/`" % d for d in dirs) or "none"))
    out.append("- Zero-byte receipts: %s" % (", ".join("`%s`" % z for z in zero) or "none"))
    if dupes:
        for h, names in dupes.items():
            out.append("- duplicate sha256 `%s`: %s" % (h, ", ".join("`%s`" % n for n in names)))
    else:
        out.append("- Duplicate sha256 receipts: none")
    out.append("- Unregistered `*.md` receipts: %s" %
               (", ".join("`%s`" % r["file"] for r in unknown) or "none"))
    print("\n".join(out))


if __name__ == "__main__":
    sys.exit(main())
```
