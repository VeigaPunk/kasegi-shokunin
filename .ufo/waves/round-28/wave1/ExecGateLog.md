# ExecGateLog — round-28 wave-1 gate and verdict inventory

- Seat: **ExecGateLog** (executor, leaf). **No production edit:** this file and
  `.ufo/waves/round-28/receipts/ExecGateLog.txt` are the only things written.
- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; claims-freeze base
  `c9f8b115a098c65356e4b3b6048af45a37ab8395`; worktree HEAD `94f387cbee71a532a51ce075f01701a557231e85`.
- Measured 2026-10-25 (UTC). Every digest below was read **immediately before and after**
  the gate it binds; `before == after` for every entry, so each line is one measurement,
  not two half-measurements. Raw commands/output: `receipts/ExecGateLog.txt`.
- Purpose: the report's evidence-pointer index. **An unrun check has not passed**; the one
  gate still red at close is named in §5 F5 with its owned fix.

## 1. Scoreboard (what this inventory establishes)

| claim | counter | after value | measured | verdict |
|---|---|---|---|---|
| C1 | (a) unverifiable verdict exits nonzero | 1 | **1** | REACHED |
| C1 | (b) `~/Projects/bounties/` CITE arm | 1 BOUNTIES-ABSENT line | **1 line, exit 1** | REACHED |
| C1 | (c) `--selftest`, one isolating fixture per limb | `selftest cases=N failures=0` at the landed sha256 | **`selftest cases=9 failures=0`, exit 0, deterministic** | instrument-side REACHED; canonical index OWED (§5 F7) |
| C1 | (d) no-harm: SKILL.md exit 0, bad=0, classes unchanged | exit 0 / bad 0 / LOST-RECORDED 306 | **exit 0 / bad 0 / LOST 306**, PIN 0, ORIGIN 0, OUTSIDE 0, BASE-ABSENT 0 | REACHED (on the post-append SKILL) |
| C2 | frontier admitted 11 → 12 | 12 | **12** | REACHED |
| C2 | entries citing S042 0 → 1 | 1 | **1** | REACHED |
| C2 | registry rows 41 → 42, census exit 0 | 42, exit 0 | **42, exit 0** (T.A 39 / T.B 1 / T.C 2; mined 30) | REACHED |
| C2 | harness `entries=14` → `entries=15 pass=15` | 15/15 exit 0 | **entries=15 pass=15 exit 0** | REACHED |

One C1 counter is instrument-side only at this writing: (c) needs the L1's canonical index at the
landed digest (F7). The corpus-wide consequence in F2 is disclosed, not counted.

## 2. Gate index — every instrument gate run this round

All commands run from the lane root unless a `cwd` is shown. `sha256` is the instrument/manifest
the gate ran against, measured before and after. Receipt paths are relative to the lane root.

### 2.1 C1 — `corpus/instruments/anchorcheck.py`

| # | gate | exit | observed | instrument sha256 | receipt |
|---|---|---:|---|---|---|
| 1 | `python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md` | **1** (pre-change: 0) | `0 in-range, 0 bad; … BASE-ABSENT=1` → prints `BASE-ABSENT md:2 corpus/knowledge/zz-r27-anchorcheck-missing.md:99` and exits 1 | `95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514` | `c1-controls/bad-fixture-before.txt` (pre 0), `receipts/ExecFixtureRun.txt`, `receipts/ExecGateLog.txt` |
| 2 | `python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md` | **1** (pre: 0) | `BOUNTIES-ABSENT md:3 ~/Projects/bounties/ops/claim-check.mjs:96 (base tree absent: …)`; `grep -c BOUNTIES-ABSENT` → **1** (pre: 0) | same | `c1-controls/bounties-fixture-before.txt` (pre 0), `receipts/ExecFixtureRun.txt`, `receipts/ExecGateLog.txt` |
| 3 | `python3 corpus/instruments/anchorcheck.py --selftest` (run twice) | **0** (pre: 1, `FileNotFoundError: '--selftest'`) | `selftest cases=9 failures=0`, byte-identical both runs | same | `c1-controls/selftest-before.txt` (pre crash), `receipts/ExecInstrSelftest.txt`, `receipts/ExecReceiptCanonC1.txt`, `receipts/ExecGateLog.txt` |
| 4 | `python3 corpus/instruments/anchorcheck.py SKILL.md` | **0** | `7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` (315 output lines = 313 verdicts + summary + blank) | same | `c1-controls/skill-before.txt` (identical pre body), `receipts/ExecNoHarmC1.txt`, `receipts/ExecGateLog.txt` |
| 5 | `python3 corpus/instruments/anchorcheck.py corpus/QUALITY.md` | **1** | `PAST-EOF md:77 README.md:159 (file has 14 lines)`; `1 bad` | same | `receipts/ExecGateLog.txt` |
| 6 | corpus sweep: `python3 corpus/instruments/anchorcheck.py <file>` over 43 files | 38×0, **5×1** | aggregate `LOST-RECORDED=70 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=8`, `BOUNTIES-ABSENT` lines **0**, bad **1**; nonzero: `citation-bases.md`, `cra-manufacturer-reporting-duties.md`, `iso-29147-divergence-and-clause-crosswalk.md`, `root-loss-2026-10-12.md`, `QUALITY.md` (detail §2.4) | same | `receipts/ExecGateLog.txt`; independent 43-file probe `receipts/ExecInstrReadme.txt` (0 movement) |

### 2.2 C2 — captures, manifest, recheck, harness, census

| # | gate | exit | observed | bound sha256 | receipt |
|---|---|---:|---|---|---|
| 7 | `python3 corpus/instruments/capture-source.py --id S041 --url https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf --kind pdf --out corpus/source-snapshots/round-28/S041.txt` | **0** | `status=200 fetched_bytes=1338665 snapshot_bytes=147267 sha256=e18acbf9…f5ab47 utc=2026-10-25T17:22:12Z`; **byte-identical to the round-26 capture** (`cmp` exit 0) | instrument `e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18` | `receipts/ExecCaptureS041.txt` |
| 8 | `python3 corpus/instruments/capture-source.py --id S042 --url https://www.ipa.go.jp/security/todokede/vuln/process.html --kind html --out corpus/source-snapshots/round-28/S042.txt` | **0** | `status=200 fetched_bytes=229982 snapshot_bytes=60508 sha256=b432ec16…c96966 utc=2026-10-25T17:22:03Z` | same | `receipts/ExecCaptureS042.txt` |
| 9 | `python3 corpus/instruments/capture-source.py --selftest` | **0** | `selftest normalize=ok deterministic=ok` | same | `receipts/ExecGateLog.txt` |
| 10 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json` (full) | **0** | 14 lines: `S041:sha256 OK` + S041 Q1–Q6 `OK occurrences=1`; `S042:sha256 OK` + S042 Q1–Q6 `OK occurrences=1` | manifest `e62ddad133ffc19ebc66822c0fcb3b48ed4993c101f05262302acc58714f291d` | `receipts/ExecManifest.txt`, `receipts/ExecGateLog.txt` |
| 11 | `… --manifest … --source S041` | **0** | 7 lines, every quote `occurrences=1` | same | `receipts/ExecManifest.txt`, `receipts/ExecGateLog.txt` |
| 12 | `… --manifest … --source S042` | **0** | 7 lines, every quote `occurrences=1`; **at manifest `fa1f366f…` this gate exited 2**: `S042:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence` (8-char heading < `MIN_QUOTE_CHARS=12`) | same | `receipts/ExecManifest.txt` (§ before/after fix), `receipts/ExecHarnessC2.txt` |
| 13 | `python3 corpus/instruments/source-recheck.py --selftest` | **0** | `SELFTEST clean/corrupt/missing-source/missing-manifest PASS` (expected 0/1/2/2 = observed) | instrument `9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96` | `receipts/ExecGateLog.txt` |
| 14 | `python3 .ufo/waves/round-28/wave1/ExecHarnessC2/check_q9.py corpus/source-snapshots/round-28/manifest.json S041 S042` | **0** | `PASS S041 … stem_matches_id=yes assertions=7 anchor_defects=0`; `PASS S042 …`; `q9 ids=2 failures=0` | manifest `e62ddad1…` | `receipts/ExecHarnessC2.txt` (mutants m1–m5 + probe), `receipts/ExecGateLog.txt` |
| 15 | `python3 corpus/instruments/frontier-recheck-count.py` | **0** (14/14 pre; **1 + `FileNotFoundError` mid-wave**) | `PASS F12 knowledge/japanese-domestic-disclosure-workflow.md ids=S041,S042 exit=0`; `entries=15 pass=15 exit=0` | README `5f458a7a26b8dfc2dd2ee2e46e11380d5697e51e77213772bce7b59253363180` | `receipts/ExecC2Counters.txt` (14/14 pre), `receipts/ScribeReadmeC2.txt` (mid-wave crash), `receipts/ExecGateLog.txt` |
| 16 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | **0** (41-row pre: 0; entry-absent mid: **1**, E11 ×2) | `kasegi ok …/corpus/SOURCES.md` + pre-existing `W04 S028`, `W04 S029` only | SOURCES `e59240f8e9842535e815f7d4575be7ea11a6a57a7bbaead43cbea92bd013945d` | `census-before.txt` (41/0), `receipts/ExecC2Counters.txt`, `receipts/ExecCensusDry.txt` (modelled post-landing: exit 0), `receipts/ExecGateLog.txt` |
| 17 | `sources-census.sh census --root … kasegi` | **0** | `rows 42`, `tier.A 39`, `tier.B 1`, `tier.C 2`, `mined 30`, `queued 9`, `rejected 3`, `missing 0` (pre: 41 / mined 29) | SOURCES `e59240f8…` | `census-before.txt`, `receipts/ExecGateLog.txt` |
| 18 | `sources-census.sh selftest` | **0** | 95 `killed` lines incl. E01–E12/W01–W04 mutants, `selftest ok` | script `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` | `receipts/ExecGateLog.txt` |
| 19 | `sources-census.sh overdue --root … --today 2026-10-25 kasegi` | **0** | cadence lines incl. `S042 recheck=180d opened=2026-10-25` (no overdue finding) | SOURCES `e59240f8…` | `receipts/ExecGateLog.txt` |
| 20 | F12 entry's own recheck line, lane cwd **and** foreign cwd `/` | **0 / 0** | `bash -n -c` exit 0; 14 OK lines (2 sha256 + 12 quotes); stdout+stderr byte-identical across cwds | entry `a22d2321e39fd0e547d8ae480eb566648520e59281e69e057aab5ab8502413a6` | `receipts/ExecRecheckAuditR28.txt`, `receipts/ExecGateLog.txt` (§F) |
| 21 | `python3 corpus/instruments/recheck-audit.py` | **1** (pre: 0) | `lines=40 total=40 pass=40`; `strict pass=40/40`; `executes=16 gated=24 broken=0`; `expected=39 missing=0 unexpected=1`; `unexpected=corpus/knowledge/japanese-domestic-disclosure-workflow.md` | instrument `3fc0d751…`; expected list `30ba586029f679721d57025a1ac339b93fe11b38c5825c721be495048b2a9080` | `receipts/ExecExpectedList.txt`, `receipts/ExecRecheckAuditR28.txt`, `receipts/ExecGateLog.txt` |
| 22 | `python3 corpus/instruments/density.py SKILL.md --label r28-gatelog` | **0** | `mean dens 160.2`, `20 blocks`, `656 path-citation instances` (base `fa09d5b8`: 150.3 / 20 / 652) | instrument `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710` | `receipts/ExecNoHarmC1.txt` (base), `receipts/ExecGateLog.txt` |

### 2.3 Counters read directly (not instrument gates, listed so the report can cite them)

| counter (exact command) | value |
|---|---|
| `awk -F'\|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | **12** (pre 11) |
| `grep -lE '^source: S042 ' corpus/knowledge/*.md \| wc -l` | **1** (pre 0) |
| `grep -cE '^\|\s*S042\s*\|' corpus/SOURCES.md` | **1** (pre 0); row fields `NF=13, kind=docs, tier=A, status=mined, opened=2026-10-25, recheck=180d, used-by=corpus/knowledge/japanese-domestic-disclosure-workflow.md` |
| S041 used-by cell | gained `corpus/knowledge/japanese-domestic-disclosure-workflow.md`; old→new logged at `corpus/SOURCES.md:79` |

### 2.4 Corpus sweep — the five files that exit 1 (each cause pre-exists round 28)

| file | exit | verdict line(s) |
|---|---:|---|
| `corpus/knowledge/citation-bases.md` | 1 | `BASE-ABSENT md:31 ~/Projects/the-bounty-hunter/ops/rank.mjs:55-58` |
| `corpus/knowledge/cra-manufacturer-reporting-duties.md` | 1 | `BASE-ABSENT md:55 S029.txt:20` |
| `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` | 1 | `BASE-ABSENT md:13 S041.txt:1868-1870`, `md:13 S041.txt:1680-1681`, `md:34 S041.txt:1792-1867`, `md:43 S041.txt:1996-2079`, `md:54 S041.txt:1868` |
| `corpus/knowledge/root-loss-2026-10-12.md` | 1 | `BASE-ABSENT md:61 queue.json:11-12` |
| `corpus/QUALITY.md` | 1 | `PAST-EOF md:77 README.md:159 (file has 14 lines)` |

The pre-change instrument printed the same eight `BASE-ABSENT` verdicts and the same one `PAST-EOF`
while exiting 0 (§5 F2).

## 3. Digest index — the bytes each gate read

Per-gate bind, `before == after`. A gate run at a different digest is a different measurement.

```
95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514  corpus/instruments/anchorcheck.py
125be37d85ffe6be30a3c372b52d96d8074e3c4d7f4baf835d0f5aed5f56cca6  SKILL.md  (post-ScribeSkillGate append)
00d4b2a3898220f61a8d26477aed3a6fa928fd73bd524eacbd8979df105c9839  corpus/QUALITY.md  (post-R14)
5f458a7a26b8dfc2dd2ee2e46e11380d5697e51e77213772bce7b59253363180  corpus/README.md  (F12 row + 12/12 amendment)
e59240f8e9842535e815f7d4575be7ea11a6a57a7bbaead43cbea92bd013945d  corpus/SOURCES.md  (S042 row + S041 used-by)
a22d2321e39fd0e547d8ae480eb566648520e59281e69e057aab5ab8502413a6  corpus/knowledge/japanese-domestic-disclosure-workflow.md
e62ddad133ffc19ebc66822c0fcb3b48ed4993c101f05262302acc58714f291d  corpus/source-snapshots/round-28/manifest.json
e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47  corpus/source-snapshots/round-28/S041.txt
b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966  corpus/source-snapshots/round-28/S042.txt
3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1  corpus/instruments/recheck-audit.py
30ba586029f679721d57025a1ac339b93fe11b38c5825c721be495048b2a9080  corpus/instruments/knowledge-expected.txt  (STALE: 39 entries)
ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710  corpus/instruments/density.py
9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96  corpus/instruments/source-recheck.py
e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18  corpus/instruments/capture-source.py
c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261  corpus/instruments/frontier-recheck-count.py
3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
969e2b92f1d14c47ebd5152aebc2df7342fc1743a914cac8f846fd27758e7471  .ufo/waves/round-27/c1-controls/bad-fixture.md
5c37b69e0ec662b6bafd98e5d8a5def3d78be563489db891790dc2f543eb77b5  .ufo/waves/round-27/c1-controls/bounties-fixture.md
```

`anchorcheck.py` moved nine times while ExecImplC1 wrote it
(`c2a9e6c6 → 0a24a173 → 7adfc847 → 982d7207 → 3122643c → 21b59612 → e14f75b8 → 29aba084 → c3629229 → 95333e29`).
The digest-attributed ledger is `receipts/ExecGateLog.txt` §B. Runs at those intermediate digests flip
limbs on and off (e.g. exit path absent at `e14f75b8`, `_selftest` undefined at `29aba084`); only the last
row counts.

## 4. Before → after, per frozen counter (claims.json, not re-worded)

| claim | before (committed receipts) | after (measured here) | delta |
|---|---|---|---|
| C1 (a) | exit 0, `BASE-ABSENT` printed (`c1-controls/bad-fixture-before.txt`) | exit **1** | closed |
| C1 (b) | 0 `BOUNTIES-ABSENT` lines (`c1-controls/bounties-fixture-before.txt`) | **1** line, exit 1 | closed |
| C1 (c) | `--selftest` absent, `FileNotFoundError` exit 1 (`c1-controls/selftest-before.txt`) | `selftest cases=9 failures=0` exit 0, twice identical | instrument side closed; canonical index owed (F7) |
| C1 (d) | SKILL `fa09d5b8`: exit 0, 7 in-range, bad 0, LOST 306 | SKILL `125be37d`: exit 0, 7 in-range, bad 0, LOST 306, all other classes 0 | unchanged (no-harm holds after the SKILL append) |
| C1 disclosure | 4 named citations invisible (unbackticked) | still 0 `BOUNTIES-ABSENT` lines, LOST stays 70 on 43 files | per claims-erratum-1 (F3) |
| C2 frontier | 11 admitted / 14 harness entries | **12** admitted / **15** entries, 15 pass | closed |
| C2 S042 | 0 entries citing / 0 registry rows | **1** entry / **1** row (NF=13, tier A, mined, opened 2026-10-25, used-by = the entry) | closed |
| C2 census | 41 rows, exit 0 | **42** rows, exit 0 | closed |
| C2 harness | `entries=14 pass=14 exit=0` | `entries=15 pass=15 exit=0` | closed |

## 5. Findings the report must carry

**F1 — the instrument was a moving target; only the landed digest counts.** Ten `anchorcheck.py`
digest values (nine changes) were observed while ExecImplC1 wrote it. Gate runs against the
intermediate bytes read
`bad exit=0`, `bounties 0/1 lines`, `selftest crash (FileNotFoundError | NameError)`. None of those is
a pass and none is a regression; they are one file mid-write. Any receipt that quotes a C1 value
without its `instrument_sha256` is unbound.

**F2 — fail-closed makes five pre-existing anchors exit 1 (disclosed, not hidden).** The 43-file sweep
exits 1 on `citation-bases.md`, `cra-manufacturer-reporting-duties.md`,
`iso-29147-divergence-and-clause-crosswalk.md`, `root-loss-2026-10-12.md` (eight `BASE-ABSENT`
citations — bare `S029.txt`/`S041.txt`/`queue.json` names, plus one explicit
`~/Projects/the-bounty-hunter/` prefix, all resolving under the absent mirror base)
and `corpus/QUALITY.md` (`PAST-EOF README.md:159`). The same verdicts were *printed* pre-change with
exit 0. The frozen no-harm predicate names `SKILL.md` only, so this is not a C1 kill — but the report
must say it, or the red sweep will read as new damage. Also: `citation-bases.md`'s own `recheck:` line
is an `anchorcheck.py` invocation, so it now exits 1 and `recheck-audit` reclassifies it
`executes` → `gated` (a pass class, not a failure). Measured counts: pre-change 39 entries =
**16 executes + 23 gated**; post 40 entries = **16 executes + 24 gated** — the new entry adds one
`executes` while `citation-bases.md` flips to `gated`. The peer receipt `ExecRecheckAuditR28.txt`
records `executes=17 gated=23`; its own two blocks classify `citation-bases.md` differently
(`executes` in one, `gated` in the other), so that 17 is not reproducible on the current bytes and
must not be cited as the round's value.

**F3 — claims-erratum-1 is corroborated independently.** The four "marked bounties citations" are plain
`source:` lines with **zero backticked spans** (`claim-gates.md:123`, `intake-and-finalize.md:109`,
`mission-control.md:169`, `source-tree-loss-2026-09-28.md:353`); `TOK` only reads backticks, so the arm
never reaches them. Citation-shaped bounties tokens: marked 4, all unbackticked, unmarked 0. Sweep:
`BOUNTIES-ABSENT` lines 0, `LOST-RECORDED` 70 = pre-change. `--selftest` case 8 (`lost-recorded`)
encodes the same rule, so the erratum's replacement sentence is now a tested invariant, not a claim.

**F4 — ordering hazards, both cleared.** If the README F12 row lands before its entry, the frontier
harness crashes (`FileNotFoundError`, exit 1) instead of reporting `entries=14`; if the S042 registry
row lands before the entry, `sources-census.sh validate` exits 1 with `E11 S041/S042 missing used-by`.
Both states were observed mid-wave and both are green at the final bytes. Close-out must run these
gates *after* the entry, not between.

**F5 — one gate is still RED: `recheck-audit.py` exit 1.** Cause is one stale owned file, not the new
entry: `knowledge-expected.txt` lists 39 entries against 40 files →
`unexpected=corpus/knowledge/japanese-domestic-disclosure-workflow.md`. `strict pass=40/40`, so the
entry's line is fine. Fix (regenerate; not this seat's file, so NOT run here) — exact command from
`ExecExpectedList.txt` §6, verbatim:

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
{ printf '%s\n' \
    '# Expected knowledge entries for corpus/instruments/recheck-audit.py — round 28' \
    '# Sorted list from the working tree (one entry per line); keep in sync with corpus/knowledge/.'; \
  LC_ALL=C ls corpus/knowledge/*.md | LC_ALL=C sort; } \
  > corpus/instruments/knowledge-expected.txt.new && \
mv corpus/instruments/knowledge-expected.txt.new corpus/instruments/knowledge-expected.txt && \
python3 corpus/instruments/recheck-audit.py --json .ufo/waves/round-28/receipts/recheck-audit-after.json
```

Expected after: `wc -l 42`, entries 40, `lines=40 total=40 pass=40`, `expected=40 missing=0
unexpected=0 exit=0` (measured in scratch by that seat and by ExecRecheckAuditR28 with a 40-entry
`--expect`: exit 0). Do not derive the list from `git ls-files` before the entry is committed — that
reproduces 39.

**F6 — density moved up, cause named.** `SKILL.md` mean **150.3 → 160.2**, blocks 20 → 20, path
citations **652 → 656**. Block 18 (`Gates & probes registry`) went `nb=5 ev=4 dens=80.0` →
`nb=6 ev=14 dens=233.3`: the ScribeSkillGate append added one evidence line inside the existing
section, so the unweighted mean moves for that reason alone. No anchor class changed (F2/d table).

**F7 — the canonical index is correctly absent; C1(c) is not closed until the L1 assembles it.**
`.ufo/waves/round-28/c1-receipt-index.txt` does not exist (defect-4 guard). The claim's counter greps
that file for `selftest cases=` and `instrument_sha256=`; `.ufo/waves/round-28/assemble-receipts.py`
produces it and runs `--selftest` once. This receipt supplies what the assembler does not check:
`--selftest` run twice at the landed digest, byte-identical, exit 0 both.

**F8 — the manifest's first build failed its own gate.** `fa1f366f…` gave
`S042:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence` (8-char heading `5.起算日の連絡` vs
`MIN_QUOTE_CHARS=12`); `e62ddad1…` passes all 14 assertions. Both the manifest owner and the Q9 seat
observed it independently. Q9's exit code alone is insufficient (source-recheck exits 0 for a
stem-mismatch, an unanchored duplicate and a broken anchor — proven by the harness mutants), which is
why `check_q9.py` exists and returns `failures=0` here.

**F9 — one frozen counter command cannot print its own value (do not read the blank as a failure).**
`claims.json` C1 `counter_commands[3]` extracts the no-harm bad count with
`sed -n 's/^== .*bad; \([0-9]*\) bad.*/bad=\1/p'`. The instrument's summary reads
`… 0 bad; 7 distinct anchors; …`, so the pattern (which wants `<n> bad; <n> bad`) matches **zero
lines** — measured: `sed_output_lines=0`. The claim's after value (`skill_md_bad: 0`) is true and is
printed in the summary line; it is just not reproducible through that sed. Working extraction (verified,
prints `bad=0`):

```bash
python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null \
  | sed -n 's/^== .*instances, \([0-9]*\) bad;.*/bad=\1/p'
```

This is a counter-command defect, not an instrument defect; `claims.json` is frozen, so the correction
belongs in a claims erratum or the lesson, not in an in-place edit (R25-1/R9). The L1 must not treat the
empty output as a missing limb.

## 6. Close-out block for the L1 (run at the commit; unrun == not passed)

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
# 0. record the digest everything below is bound to
sha256sum corpus/instruments/anchorcheck.py
# 1. C1 limbs (expect: 1 | 1 | exit 0 + "selftest cases=9 failures=0" | exit 0 + bad 0 + LOST 306)
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo "bad_fixture_exit=$?"
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT
python3 corpus/instruments/anchorcheck.py --selftest; echo "selftest_exit=$?"
python3 corpus/instruments/anchorcheck.py SKILL.md >/dev/null 2>&1; echo "skill_exit=$?"
python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | grep '^== '
# 2. the one canonical receipt at the landed digest (fills C1(c) after-value)
python3 .ufo/waves/round-28/assemble-receipts.py
grep -cE 'selftest cases=' .ufo/waves/round-28/c1-receipt-index.txt
grep -oE 'instrument_sha256=[0-9a-f]{64}' .ufo/waves/round-28/c1-receipt-index.txt
# 3. C2 counters (expect: 12 | 1 | 1 | census_exit=0 rows 42 | entries=15 pass=15 exit=0)
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l
grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "census_exit=$?"
python3 corpus/instruments/frontier-recheck-count.py
# 4. captures/manifest (expect exit 0, 14 OK lines; Q9 failures=0)
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json; echo "recheck_exit=$?"
python3 .ufo/waves/round-28/wave1/ExecHarnessC2/check_q9.py corpus/source-snapshots/round-28/manifest.json S041 S042
# 5. the only red gate — needs the expected-list regeneration FIRST (ExecExpectedList.txt §6)
python3 corpus/instruments/recheck-audit.py; echo "audit_exit=$?"
# 6. density guard (expect exit 0; mean 160.2 / 20 blocks / 656 cites at SKILL 125be37d)
python3 corpus/instruments/density.py SKILL.md --label r28-close
```

Known-red before step 5 unless the list is regenerated: `audit_exit=1` with `expected=39
unexpected=1`. That is F5, not a C2 failure.

## 7. Receipt pointer index

| receipt | what it holds |
|---|---|
| `receipts/ExecGateLog.txt` | this seat's raw evidence: per-gate command, bound digest, exit, verbatim output, digest-attributed `anchorcheck.py` ledger, sweep |
| `c1-controls/{bad-fixture,bounties-fixture,selftest,skill}-before.txt`, `c1-controls/instrument-digest-before.txt`, `c2-controls/before.txt`, `census-before.txt` | committed before/do-nothing controls at the freeze |
| `receipts/ExecFixtureRun.txt` | C1 (a)(b)(d) pre-state counter re-runs + fixture digests |
| `receipts/ExecInstrSelftest.txt` | C1(c) pre-state crash, run twice, determinism |
| `receipts/ExecNoHarmC1.txt` | SKILL no-harm + density baseline (150.3/20/652; reconciles the stale 154.0/19/652) |
| `receipts/ExecReceiptCanonC1.txt` | canonical-index block template + the rule that the index carries exactly one `selftest cases=` line |
| `receipts/ExecInstrReadme.txt` | instrument README change; the unbackticked-citation finding that became claims-erratum-1; 43-file probe, 0 movement |
| `receipts/ExecCaptureS041.txt` / `ExecCaptureS042.txt` | capture commands, exit 0, snapshot sha256, byte-identity S041↔round-26, the seven-step web-app flow correction |
| `receipts/ExecManifest.txt` | manifest before/after fix (`fa1f366f` → `e62ddad1`), full/per-id runs, Q9 re-derivation |
| `receipts/ExecHarnessC2.txt` | Q9 probe: source-recheck's exit 0 is insufficient; mutants m1–m5 |
| `receipts/ExecC2Counters.txt` | C2 counters at pre-state (11 / 0 / 41 / 14-14) |
| `receipts/ExecCensusDry.txt` | modelled post-landing census: exit 0, rows 42, plus E03/E04 teeth and the E11 ordering demo |
| `receipts/ExecExpectedList.txt` | count basis 41 = 39 + 2 headers; N → N+1 regeneration command; scratch 40-entry audit exit 0 |
| `receipts/ExecRecheckAuditR28.txt` | post-state audit exit 1 (stale list only), standalone entry line both cwds, refreshed-list audit exit 0 |
| `receipts/ScribeRegistryC2.txt`, `ScribeReadmeC2.txt`, `ScribeFrontierNote.txt` | S042 row + S041 used-by old→new; F12 row; frontier note (with the mid-wave harness crash) |
| `receipts/ScribeR14.txt`, `ScribeLog.txt`, `ScribeScorecard.txt` | R14 landed with byte-identical first 77 lines; LOG/SCORECARD entries |

No tool was installed or upgraded; no pacman transaction attempted; no VCS write; no background job;
no subagent dispatched. No credential, session or private-URL material was read or written.
