# SentinelScope — round-28 wave-1 scope & safety sweep

filed: 2026-10-25T17:31Z (UTC) · lane base: c9f8b115a098c65356e4b3b6048af45a37ab8395 · run over the landed wave state (final re-check 17:29–17:31Z)

## 1. Lane working-tree status vs ownership map — PASS

`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain` at 17:26Z (post-land):

- Modified: `LOG.md` (ScribeLog), `SCORECARD.md` (ScribeScorecard), `SKILL.md` (ScribeSkillGate), `corpus/QUALITY.md` (ScribeR14), `corpus/README.md` (ScribeReadmeC2), `corpus/SOURCES.md` (ScribeRegistryC2), `corpus/instruments/README.md` (ExecInstrReadme), `corpus/instruments/anchorcheck.py` (ExecImplC1) — exactly the 8 owned production files, 1:1 with the ownership map. No other tracked file modified.
- Untracked: all under `.ufo/waves/round-28/` (incl. `claims-erratum-1.md`, appended correction — not an in-place claims.json edit) or `corpus/source-snapshots/round-28/` (S041.txt, S042.txt, manifest.json) or `corpus/knowledge/japanese-domestic-disclosure-workflow.md` (ScribeEntryC2). All in scope; no misrooted path.
- Sibling `ExecScopeSweep/sweep-final2.txt` (17:28:53Z): `lane_violations=0` over 12 prod + 238 wave paths; `fleet_misroot=0`; `shokuknow_kasegi_scoped_files_newer_than_wave=0`. Confirms this independently.

## 2. Credential scan — PASS

- Production diffs (`git diff -U0` over all 8 changed files + new entry): only benign `token`/`backticked tokens` doc words; no secret/token/cookie/op:///BEGIN PRIVATE KEY/api-key/password/bearer material.
- New entry `corpus/knowledge/japanese-domestic-disclosure-workflow.md`: 0 hits.
- `corpus/source-snapshots/round-28/` (S041.txt, S042.txt, manifest.json): 0 hits.
- Scratch `.ufo/waves/round-28/` hits are all prose references to the tool's own "token" concept (bounties-citation tokens), a private-key-named fixture in a `KASEGI_BOUNTIES` temp root, JavaScript `document.cookie` gates in captured Cisco policy JS (S068 body — page content, not credentials), and one `anchorcheck` fixture named `k8s-nodebound-token-impersonation.json` (a citation path, not credential data). No credential material anywhere.

## 3. Forbidden-path writes — PASS

- `/home/vgpnk/Projects/shokunin` root: no wave-seat write. `git status` at the fleet root shows only modified `.scratch/goal-20261025-hyaku-run7.md`, `.ufo/state/*.report-baseline`, `.ufo/watchdog.log` — orchestrator/fleet tooling artifacts, no kasegi wave content; `.scratch/battery.out`, `.scratch/coupling.out`, `.scratch/craft.out`, `.scratch/d2check.out` are other-lane work. None names round-28 wave seats (limb 1 of the sibling sweep: `fleet_untracked_scanned=0`).
- `/home/vgpnk/Projects/shokuknow` (read-only): `merge/kasegi/` untouched today (max mtime 2026-10-24T23:33Z). Two pre-dispatch (13:34–13:35Z) writes under other lanes' `lanes/tabi/` and `lanes/revenger/` round-work dirs belong to those lanes; nothing kasegi-scoped (`shokuknow_kasegi_scoped_files_newer_than_wave=0`).
- Lane repo contains no `.ufo/state`, `templates/`, `scripts/`, `MANIFEST.json`; nothing written there. No receipt claims a write to any forbidden path (`grep` over receipts: 0 hits). No `git`/`jj` mutating command in any receipt.

## 4. Capture fetches — PASS (instrument UA, public URLs)

- `ExecCaptureS041.txt`: `python3 corpus/instruments/capture-source.py --id S041 --url https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf --kind pdf --out corpus/source-snapshots/round-28/S041.txt` — status 200, sha256 e18acbf9… matches round-26 bytes, instrument `capture-source.py` sha256 e1831888d7…, toolchain pdftotext 26.08.0 (pre-existing, no install), `kasegi-shokunin/1.0` UA.
- `ExecCaptureS042.txt`/`.md`: `--id S042 --url https://www.ipa.go.jp/security/todokede/vuln/process.html --kind html --out corpus/source-snapshots/round-28/S042.txt` — status 200, sha256 b432ec16…, instrument UA, capture 17:22:03Z.
- Total live fetches this wave: 2 dispatched captures + 11 verification probes, all with the instrument UA on public URLs, none credentialed: 2 by ScribeSourcesGate (S042/S041 try-captures, `ScribeSourcesGate.md:18-19,37,65`), 7 by ScribeLessonGate `quarantine-handcheck.sh` (S037/S048/S054/S065/S068 + S069/S070 which failed with curl rc=60 SSL-verify and captured nothing), S041's `curl -sI` upstream corroboration. All reads; all logged in wave1 reports; no live write, no interaction beyond GET.

## 5. No fixture/test probed a live target — PASS (with one observation)

- `ExecHarnessC2` (check_q9.py, probe_q9_discrimination.py): subprocess calls run only the lane instrument `corpus/instruments/source-recheck.py` against scratch manifests under `wave1/ExecHarnessC2/`; `capture-S041.txt`/`capture-S042.txt` are 5-line synthetic probe fixtures (line1..line5, alpha-bravo probe sentence), not captures. No URL/network code in either script.
- `MutArmC1`, `MutExitC1`, `MutManifestC2`, `MutQuoteC2`, `MutSelftestC1`, `RevengerC1`, `CritC1Vacuity`, `ExecReceiptCanonC1`: fixture trees under `wave1/` + `tempfile.mkdtemp` temp roots (env-overridden `KASEGI_MIRROR`/`KASEGI_ORIGIN_ROOT`/`KASEGI_BOUNTIES`); `anchorcheck.py --selftest` builds its 9 isolating fixtures in `tempfile.mkdtemp` and `rmtree`s them (post-land digest 95333e29ee5a…, `selftest cases=9 failures=0`).
- Observation (NOT a violation of the hard rules, but beyond the 2 dispatched captures): ScribeLessonGate's `quarantine-handcheck.sh` performed 7 live GETs (public pages, instrument UA, write only to its own `wave1/ScribeLessonGate/` scratch). Q6-class check: these are evidence probes, not fixtures; documented in its seat report and handcheck out; data written stays in-scope.

## 6. Verdict-class no-harm (cross-check) — PASS

- anchorcheck live run on SKILL.md post-land: exit 0, bad=0, LOST-RECORDED=306 unchanged; the only output movement is one line renumbered (md:998 → md:999) because ScribeSkillGate inserted the anchorcheck registry row at SKILL.md:980 (class counts unchanged). BOUNTIES-ABSENT absent from live run (no backticked anchored bounties citations exist lane-wide; erratum `claims-erratum-1.md` supersedes the frozen `corpus_disclosure` cell — zero movement, stronger no-harm).
- NOTE for L1: SKILL.md change is an insert at line ~980 rather than a same-line append. R6 says an edit to a line-number-cited file "keeps every existing line at its number (append at the end, or a same-line suffix)". The insert shifts every SKILL.md line ≥981 (e.g. cited line 1000 changed content; `resolve-dispatch-fixtures.json:159-161` pins a verbatim alternative set at SKILL.md:1000). Affected referents: `corpus/instruments/resolve-dispatch-fixtures.json` (pinned line 1000 content) and the pre-state c1-controls anchorcheck capture (md:998 line moved). Verdict classes and all acceptance counters are unaffected (canonical C1 block + counters confirm), but a strict R6 reading flags the line-number displacement. Suggest L1 decides: accept (line 1000 is a fixture-only pin; no corpus/lesson line cites SKILL.md ≥980) or have ScribeSkillGate revert the insert to a file-end append before commit.

## 7. Notes / pending at sweep time

- `corpus/lessons/round-28.md` (ScribeLesson) not yet landed; `ExecCaptureS042.txt` receipt existed only after my first check (it landed 17:25Z, noted `PRE-STATE` at first scan).
- anchorcheck.py pre-change digest c2a9e6c6… matched the freeze c1-controls file; post-change digest 95333e29ee5a…, selftest `cases=9 failures=0`, receipt `canonical-block.filled.txt` at the landed digest.

Findings: 0 hard-rule violations. One low-severity R6 line-number-displacement observation, one additional-live-probe observation, pending round-28 lesson.
