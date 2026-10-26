# Round 33 — kasegi

Lane: `kasegi-shokunin`. This lesson reports working-tree and receipt evidence, not a canonical judge decision. Revisions: base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; claims-freeze commit `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`; wave-1 dispatch commit `a6a502351bb90c8cd6d9b8f45f55109b7848e0d1`; final integration hash `9f9848816503aa0cd566fc2efdc5e69ea501a253`. (The L1 replaced both placeholders; the parenthetical below is the read-only context for that edit and stays factual.)

Shape: **one v2 wave**. Wave 1 `kasegi-r33-build`, **64 seats**, dispatch one batched task call (`wave1-dispatch.json` `schema=ufo-swarm-wave-dispatch-v1`, `wave=kasegi-r33-build`, `resumeSends: []`, so resume 0; `wave1-spec.json` carries 64 items and `wave1.ready` names `l1: KasegiR33`). Declared role counts from `wave1-spec.json`: executor 19, reviewer 12, scribe 10, mutation-tester 7, scout 5, critic 5, connector 3, sentinel 2, simplifier 1 (= 64). Route: L1 inline spawn handoff, hyaku run 8 (`.ufo/waves/round-33/watchdog-digest.txt` line 3: `2026-10-26T01:10:54-03:00 launch kasegi round=33 pgid=99020 driver=hyaku-inline attempt=1`). Axes owned (`claims.json` `axes_owned`): `depth:density`, `depth:verifiability`, `coverage`; saturation line 9/10 per axis, window N=3; lowest non-retired axis `depth:verifiability (4)`.

Receipt coverage at composition: **56 of 64** seats filed a receipt in `.ufo/waves/round-33/wave1/`. Absent: `ScribeScorecard`, `ScribeLesson` (this file), `ScribeReportDraft`, `RevGateSpot`, `CritMistakes`, `SimplifierCleanup`, `ExecScratchDiscipline`, `RevC1BeforeAfter` (`ls wave1/*.md` vs `wave1-spec.json` names, counted by this seat). No axis score is claimed here; C1's capability clause landed only near the end of the wave (`SCORECARD.md:1078`, cited in the C1 row and open item 2), and the two header placeholders are the L1's edit (open item 1).

Answering model on seat receipts (rule 10, by the name each receipt states for itself, first match per file over the 56 receipts): `opencode-go/deepseek-v4.1-flash` in 25, `zai/glm-5.3-flash` in 6, `devin/glm-5-3-flash-1m` in 5, `kimi-code/kimi-for-coding` in 3, `anthropic/claude-sonnet-5-5` in 3 (`RevRowS049.md`, `RevRowS050.md`, `ScoutPackageThemes.md`); 14 receipts name none: `CritC1Kill.md`, `ExecCensusDry.md`, `ExecDeterminism.md`, `ExecHarnessC2.md`, `ExecManifestUpgrade.md`, `MutCtrFetchMissing.md`, `MutEntryF16.md`, `MutLegacyManifestDrop.md`, `RevNoHarm.md`, `RevQuoteSweep.md`, `RevRowS050.md` (no model string; it does name a second model for a peer in another file), `ScoutDatawalk.md`, `ScoutF16Sweep.md`, `SentScopeFinal.md` (`grep -ohE '(opencode-go|devin|anthropic|google-antigravity|zai|inception|kimi-code|openai)/…' wave1/*.md`, first match per file, tallied with `sort | uniq -c`).

## Frozen claims — before → after

Before column is the frozen control at base `690b69d` (`.ufo/waves/round-33/c1-controls/before.txt`, `c2-controls/before.txt`, which are claims-freeze evidence, not seat work); after column is measured on the landed bytes by the named receipts.

| Claim | Axis | Before (frozen controls, base `690b69d`) | After (landed bytes, quiescent) | Verdict / boundary |
|---|---|---|---|---|
| C1 | depth:verifiability (4) | `ls_exit=2` (instrument absent); manifest audit `round-23 records=4 … round-31 records=1`, `TOTAL records=38 with_url=0 with_fetched_utc=0`; `round-32` dir holds `S049.txt`/`S050.txt` and **no** manifest; `source-recheck` on it `manifest UNAVAILABLE reason=missing`, `recheck_exit=2` (`c1-controls/before.txt`). Fake control: `fake-checker.py` prints `records=38 bound=38 unbound=0` exit 0 (`c1-controls/fake-checker-receipt.txt`) | `records=40 bound=40 unbound=0`, `binding_exit=0`, two runs byte-identical (`stdout` sha256 `1861fec8…a3c5a9f1`); `AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2`; `--selftest` `cases=11 failures=0` exit 0; 9 of 9 snapshot dirs carry a manifest; 38 legacy records `archival: true` with a byte-exact own-row `url`, S049/S050 carry `fetched_utc` and no `archival` (`wave1/ExecRegressionC1.md` §1 gate 1–2 and §2.1–2.2; `wave1/ExecCaptureBinding.md` §2, §4; `wave1/ExecManifestUpgrade.md` §6; manifest `sha256 6e4e719a…c774` from `wave1/ExecManifest32.md` and re-derived in `wave1/ExecErratumCheck.md` §0) | **Measured, held.** Capability clause met: `SCORECARD.md:1078` carries the `capture-binding-check` row under `## Round-33 capabilities` (`SCORECARD.md:1074`), appended with two `<LANE_HASH>` markers for the L1 to fill (`wave1/ScribeScorecard.md` §3: +111 lines, `sha256 e03fbefa…`). Re-run by this lesson on the committed bytes at `04:42–04:44Z`: identical summary, `binding_exit=0`, `selftest cases=11 failures=0`, with input bookends byte-identical across the run. Boundaries: (a) `records=40` counts **entries over 38 distinct ids** (S041 recurs in rounds 26/28/30, `wave1/CritC1Kill.md` § Disclosures); (b) `fetched_utc` is the **capture-commit** time, not a fetch instant (same §, quoting the round-32 manifest `purpose` field); (c) no rule binds a record to its capture **bytes** — a 0-byte or deleted capture still audits `bound=40` (`wave1/CritC1Kill.md` H1/H2, fixtures `m8`/`m17`), and rule D is proposed but **not landed** (`wave1/ExecCaptureBinding.md` §8) |
| C2 | coverage (7) | frontier admitted 15; `S049=0 S050=0` entries; `S049_rows=0 S050_rows=0 total_rows=48`; census exit 0 with `W04 S028`/`W04 S029`/`ok`; harness `entries=18 pass=18 exit=0`; `source-recheck` on the absent round-32 manifest `recheck_exit=2` (`c2-controls/before.txt`) | frontier `16`; `S049=1 S050=1` entries citing `^source: `; `S049`/`S050` rows 1 each; registry `50`; census `census_exit=0` with exactly `W04 S028`, `W04 S029`, `ok`; harness `PASS F16 knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050` and `entries=19 pass=19 exit=0`; `source-recheck` S049 `Q1`–`Q8` + S050 `Q1`–`Q6`, every one `occurrences=1`, both `sha256 OK`, exits 0; entry `ADMIT` on Q1–Q10 by a non-author reviewer (`wave1/ExecHarnessC2.md` §1 table 1–9; `wave1/ExecCensusAfter.md` §1–§2; `wave1/RevEntryF16.md` §1, §7) | **Measured, held.** Re-run by this lesson on the committed entry (`1f7ac0a2…171d1`, 306 lines): all nine cells reproduced, `census_exit=0`, bookend identical. Boundaries: (a) a junk construction meets **every** counter except the reviewer clause — frontier 16, 1/1 citing, 1/1 rows, 50 rows, census exit 0, harness 19/19, `source-recheck` exit 0 (`wave1/CritC2Kill.md` §5); (b) the harness is one-directional — dropping a header `source:` line survives it, covered only by counter 2 (`wave1/MutEntryF16.md` § Verdict) |

Claims erratum of record: `.ufo/waves/round-33/claims-erratum-1.md` (L1, before any measurement) rules Rule B **id-scoped** — the row `| <record id> |` must exist, be unique, and its `https://` token equal the record `url` byte-for-byte; a URL shared with a *different* row is informational `multi_row_url=N`, not a failure. The landed instrument implements that reading (`wave1/ExecCaptureBinding.md` §1; instrument `sha256 b4182665…d0b7f9`, 492 lines), and at landed bytes `multi_row_url=2` names exactly S029 (shared with S024) and S006 (shared with S028). Read literally, the frozen kill rule's parenthetical ("0 or 2+ matches = failure") would reject the correct instrument; three independent seats flagged that tension (`wave1/CritC1Kill.md` § Verdict 3, `wave1/RevManifestUpgrade.md` § Verdict, `wave1/RevClaimsFreeze.md` § universal-clause table row 2), and `wave1/MutCtrUnbound.md` § PRE-STATE records the byte-level drift between the two generations (`5fa7868b…` global, `4bc7aed3…`→`b4182665…` id-scoped).

## Gate — F16 / S049 / S050 and the assimilation set

Package `/home/vgpnk/Projects/shokuknow/merge/kasegi/` and register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` were read-only throughout (no package tool run, no write there). Gate requirement (≥1 admit, ≥1 reject) is met with **2 admits by document + 7 rejects** (`wave1/ScoutPackageThemes.md` § Verdict), plus the 7-row quarantine slice (`wave1/ExecQuarantine.md`).

### Admitted

| Item | Evidence | Gate decision |
|---|---|---|
| **F16** — `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` | `sha256 1f7ac0a2c39a0fbfdbee2ecbe112316dfc1bf7095b18cb8fb4eb9d6dfce171d1`, 306 lines, 24539 B (committed at `9f98488`; `git show 9f98488:corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md \| sha256sum` re-run by this lesson); Q1–Q10 verdict table all `pass` (`wave1/RevEntryF16.md` §1), `ADMIT` (§7); README frontier row and `frontier=16` (`wave1/ScribeReadmeF16.md`, re-counted § C2 above); 14 manifest assertions all `occurrences=1` | Admit. |
| **S049** — 网络安全众测平台 help page, `https://zc.cnvd.org.cn/news/helpList` | Access date **2026-10-26** (registry `opened` cell; capture re-opened live `2026-10-26T04:16:06Z`, HTTP 200, 56674 B fetched, **0** differing lines: `wave1/ScoutLiveDrift.md`); capture `corpus/source-snapshots/round-32/S049.txt` 20272 B / 426 lines / `sha256 962a451a…1cb8`; manifest record `url` + `fetched_utc` (`wave1/ExecManifest32.md`); registry row `:55`, `tier A`, `mined` (`wave1/ExecRegistryAppend.md` §2). Quote (19 characters, `S049.txt:214`, accessed 2026-10-26): 「众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。」 | Tier A, mined; staged `S034` → lane `S049` **by document** (URL byte-equal, `wave1/ScoutPackageThemes.md` §1). |
| **S050** — 360SRC 外部漏洞处理和评分标准 V2.0, `https://security.360.cn/Reward/rules` | Access date **2026-10-26** (same live re-open `2026-10-26T04:16:16Z`, HTTP 200, 427391 B, `application/pdf`, 0 differing lines); capture `S050.txt` 31016 B / 630 lines / `sha256 2f9c6406…6888`; registry row `:56`, `tier A`, `mined`. Quote (23 characters, `S050.txt:591`, accessed 2026-10-26): 「未纳入安全服务的资产一般情况下不收录相关漏洞」 | Tier A, mined; staged `S035` → lane `S050` **by document**. |

Capture quirks that bound every future quote from these rows: the S050 applicability sentence wraps across L70/L71 and `合资公司` is split by the PDF conversion, so the full sentence does **not** bind as one assertion (entry L101–103 says so); the `安全币 ：RMB=1 : 5` label repeats seven times and is hand-measured, not manifest-bound; and the S049 page carries platform-issued **tester credential material** (L201–206 retrieval steps, L374–405 OpenVPN walkthrough) which is located and **never reproduced** — `wave1/SentCred.md`, and the entry's own Q6 paragraph (L191–194), verified by `wave1/RevEntryF16.md` Q6 row.

### Id-collision evidence — adoption by document, never by number

The package still assumes a 30-row registry (`existing_rows 30`, `first_id S031`, `renumbered []`, `MERGE-REPORT.json`) while the lane held 48 rows at base, so staged ids `S031`+ name different documents. Committed scratch (`.ufo/waves/round-33/assimilation/`): `reg_ids=48`, `staged_ids=94`, `collisions=18` (`S031`–`S048`), and a guard-sensitivity line (`indented row caught by 0-3-space pattern = 1; column-0-only pattern = 0; staged col0 row caught = 0`). Re-derived independently in `wave1/ScoutPackageThemes.md` § Verdict and `wave1/ConnOwnership.md`. Staged `S034`/`S035` URLs are byte-equal to the lane S049/S050 capture URLs (36 bytes each, `wave1/ScoutPackageThemes.md` §1). A new hazard is recorded: the refused `chinese-criminal-thresholds-and-authorisation.md` cites "wave-1 row S034", which in the lane is the 総務省 page (`corpus/SOURCES.md:40`), not the CNVD help page — a silently wrong citation under any adopt-by-number reading.

### Refused package candidates (each with its flip condition)

Standing refusals re-confirmed this round with unchanged digests (`wave1/ScoutPackageThemes.md` §2), plus two entries not previously gated in the lessons this seat read:

| staged entry | Gate decision | Reason (lane-side) | Flip condition / effect of S049+S050 |
|---|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` (`120d8cd5…`) | **REFUSED** (standing from round 30) | Q1 staged ids + colliding `ground: F09` + prose `recheck:`; Q2 unregistered; Q3 no located quote; Q4/Q5 three platforms generalized into a universal; Q7/Q10 non-executable recheck. Its HackerOne half is held by F13/`S043`; the scope split by F03/`S006`. New this round: its "360SRC bounds scope by asset class" sentence mixes 适用范围 with grading (§一 L69–71 scopes by 360 group product/business) | Register+capture CNVD helpList and 360SRC rules (now **met** at capture level, rows landed), reuse `S043`, quote each scope rule with a location, attribute per platform, executable recheck, re-ground on a lane frontier. Remaining clauses: located quotes, per-platform attribution, executable recheck |
| `claim-packaging-and-report-quality.md` (`6ad64d78…`) | **REFUSED** (standing) | Q1 ground not a lane F-id, `curl … && pdftotext …` fails `bash -n`; Q2 S034/S035/**S036** unregistered; Q3 quote-marked Chinese with no page/line; Q4 regional universal; Q7/Q10 | Register/capture S034/S035/S036 (2 of 3 now met; `S036` BILISRC still in no lane row), quote each downgrade/proof rule with a page/line, state each as that platform's position, add one falsifiable rule and one rejected over-generalization, re-ground |
| `cn-crowdsourced-testing-roles-and-conduct.md` (`a5302aaf…`) | **REFUSED** (standing) | Q1 no H1; Q2 S081/S082 unregistered, S082 a drafting-stage record; Q3 quotes without revision/page or exactly-once check; Q7/Q10 | Add H1, register+capture S081/S082, re-quote with page/line and exactly-once counts, replace the drafting-stage scope sentence with promulgated text, `cd`-prefixed recheck. **Unaffected by S049**: both captures score 0 for `您不得因为漏洞信息私自联系厂商`, `众测需求方`, `授权测试方` |
| `chinese-crowd-testing-national-standard-2026-10-23.md` (`6c15d941…`) | **REFUSED** (standing) | Q1 `ground: F24` not a lane F-id; Q2 S077/S078/S079 unregistered; Q3 zero quote-marked strings; Q5 | Register/capture S077/S078/S079, quote the roles-and-duties sentence with a location, drop the "platform rules as an implementation of a national standard" reframing, add a rejected over-generalization. **Unaffected**: `43741` and `国家标准` occur 0 times in both captures |
| `chinese-criminal-thresholds-and-authorisation.md` (`1660c00c…4e8a59ae`) | **REFUSED** (standing, round-30) | Unregistered staged evidence in colliding id space; cross-instrument conclusion generalizing beyond located text (Q2/Q4); missing located quotes and non-compliant recheck (Q3/Q7/Q10) | Register/capture S044/S045/S046, bound the conclusion to located text, located quotes, executable recheck. **New hazard**: its dangling "row S034" is now a wrong citation (see above) |
| `chinese-program-severity-instrument.md` (`442e0f2b…`) | **REFUSED as an entry** (not in the standing five) | Q1 `ground: F10`, colliding id `S034`, prose `curl` recheck; second source `S047` (`sse.com.cn`, JR/T 0276—2023) unregistered; anchors `newsType_6`, absent from the text capture (only `newsType_21`) | Its S034-only half (CVSS 3.0 coefficients, temporal E/RL/RC, the 12/10/7/4 worked example, the 高危→中危 FAQ) is source-verified in S049 and is reusable **as fact base with line locators**, not as staged bytes |
| `program-severity-ladders-and-reward-scales.md` (`35de5f8b…`) | **REFUSED / do-not-copy** | A same-name lane entry exists with different bytes (`35de5f8b`/50 lines vs lane `6c05c98f`/67); copying would overwrite lane text. Its VRT and BILISRC halves cite unregistered rows | Treat as overwrite hazard; the CNVD half is the same S049 content already restated with locators |

### Quarantine slice — 7 register rows, hand-checked

Slice re-derived byte-identically from the register (`sed -n '99,100p;322,326p'` → `diff` empty, `diff_exit=0`; `wave1/ExecQuarantine.md` §1). Per-row verdicts (§5) and the installable Gate blocks (§6):

| staged id | register class | live fetch (2026-10-26, instrument UA) | verdict |
|---|---|---|---|
| S037 GB/T 30279-2020 openstd record | `payload-absent` | 200, 24189 B, `sha256 9cba2e96…20f204` | **refuse** — staged quote is a **spliced field collage**: it skips the `英文标准名称` line, skips the 在线预览/分类号 block, and inserts `：` after 发布日期/实施日期 (absent under F1–F4 folds). Flip: re-stage `标准状态：现行` + `发布日期 2020-11-19 实施日期 2021-06-01` (whitespace-removed form `发布日期2020-11-19实施日期2021-06-01`), and add a lane row first (`grep -c openstd corpus/SOURCES.md` → 0) |
| S054 内閣府 vulnerability-information request PDF | `payload-absent` | 200, 513648 B, 3 pp, `sha256 0150c9d1…12b88` | **refuse** — the staged string elides the statutory parenthetical (`（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）`); only the suffix and the full clause are contiguous. Flip: adopt the full clause at §1（ア）after a lane row exists (`grep -c 府連 corpus/SOURCES.md` → 0) |
| S048, S065, S068, S069, S070 | `unreachable` | not fetched by this seat (bounds: only the two named payload-absent URLs) | **unreachable** — register cause `the cited source could not be fetched, so no quote was checked`; no quote exists to re-check. Never to be reported as fabrication. Note: the independent package read found S065/S068 reachable today and S068 URL byte-equal to lane `S040` (`wave1/ScoutPackageThemes.md` §3), which changes the register class, not the verdict |

D6's ask is closed here: S037's verdict is recorded (refuse, spliced quote) with its flip condition. Net quarantine disposition: **0 adopted, 2 refused, 5 unreachable**.

### Registry changes — old → new

| Measure | Before (base `690b69d`) | After (landed) | Source |
|---|---|---|---|
| registry rows | 48 | **50** | `wave1/ExecRegistryAppend.md` §6; re-counted by this lesson |
| `S049` / `S050` rows | 0 / 0 | **1 / 1** | same §6; `c2-controls/before.txt` |
| pre-existing cells changed | — | **0** | `diff base-sources.md corpus/SOURCES.md`: `>` 6, `<` 0 (§9); SOURCES.md `sha256 5a03c696…` → `b22c7f01…4d13b` |
| tier histogram | A 45 / B 1 / C 2 | **A 47** / B 1 / C 2 | §6 |
| status histogram | mined 36 / queued 9 / rejected 3 | mined **38** / queued 9 / rejected 3 | §6 |
| malformed rows / duplicate ids / enum violations / missing used-by | 0 | **0** | §6 |
| frontier admitted rows | 15 | **16** | `wave1/ScribeReadmeF16.md`; re-counted |
| harness | `entries=18 pass=18` | **`entries=19 pass=19 exit=0`** incl. `PASS F16 … ids=S049,S050` | `wave1/ExecHarnessC2.md` §1 |

Six lines were appended, not four: two rows inside `## Registry` (`:55`, `:56`), one `## Search log` bullet (`:75`), three `## Registry changes` R8 lines (`:98`–`:100`) (`wave1/ExecRegistryAppend.md` §2, §4, §5). Both row cells keep 12 pipes / `NF=13` and one `https://` token in the source cell. Staged→landed normalizations worth naming: staged `S035` `kind spec` → `docs` (the capture is the PDF's converted text, read as its publisher's documentation); staged `opened 2026-10-23` → `2026-10-26`; staged `used-by` pointing at four entries → the one F16 entry; staged page-level anchors not carried.

### Gate caveats this round must carry

- **A junk construction passes every C2 counter except the reviewer clause** (`wave1/CritC2Kill.md` §5) — the same shape as round 31's Gate caveat 1. The counters are shape counts plus a captured-source comparison; only Q2/Q3/Q4 prose review and the expand-credit check reject a fabricated capture.
- **C1 binds manifest metadata to registry text, not bytes to captures** (`wave1/CritC1Kill.md` H1–H3). Three of its eight measured blind spots (capture bytes, capture existence, path traversal) are one rule away (its D1, ~12 lines, no data change: all 40 landed records already satisfy it), and rule D is unlanded by design pending an L1 erratum (`wave1/ExecCaptureBinding.md` §8).
- **The counter's plain-run kill rule does not pin the url-missing limb.** A one-line mutant that skips rule B prints `records=2 bound=2 unbound=0` exit 0 on a url-less fixture — a **survivor** under the plain-run reading on both pinned generations — while the instrument's own `--selftest` kills it (`failures=1`) and the frozen claim already asserts `--selftest failures=0` (`wave1/MutCtrUnbound.md` § Verdict, § Coverage finding). The claim's selftest clause covers it; the kill rule as worded does not.

## Mistakes (M33-*)

Numbering follows `claims.json` `non_claim_frontier_items.mistake` (M33-1, M33-2). M33-3…M33-6 are appended by this lesson from wave-1 receipts. The sweep quoted in the opening of this section is: `for w in BLOCKED DEFECT SURVIVOR survivor FAIL traceback PRE-STATE; do printf '%-10s files=%-3s hits=%s\n' "$w" "$(grep -l "$w" wave1/*.md | wc -l)" "$(grep -o "$w" wave1/*.md | wc -l)"; done` over 56 receipts → `BLOCKED files=3 hits=10`, `DEFECT… files=0 hits=0`, `SURVIVOR files=3 hits=4`, `survivor files=8 hits=20`, `FAIL files=22 hits=161`, `traceback files=0 hits=0`, `PRE-STATE files=34 hits=91`. No `BLOCKED:` hit is a seat reporting a blocker: two are negative assertions (`wave1/ExecExpectedList.md:204` "BLOCKED: none.", `wave1/ScribeProvince.md:41` "No `BLOCKED:` line is …") and the rest are `wave1/ExecWaveEvidencePack.md`'s own token-count table (`BLOCKED=2` as a *token total* over other receipts). `FAIL` is dominated by checker fixture output; the real survivor events are M33-6, and the third `SURVIVOR` file (`wave1/ScribeScorecard.md`) cites them.

- **M33-1 — the round-32 captures were committed without their manifest.** Class: landing / reference-drift. `corpus/source-snapshots/round-32/` shipped `S049.txt` + `S050.txt` and no `manifest.json` at base `690b69d` (`git ls-tree --name-only 690b69d corpus/source-snapshots/round-32/` → the two files; `wave1/ScribeQuality.md` §2, `wave1/ScoutManifestAudit.md` § round-32), so the round-32 verifier's D5 stands (`corpus/lessons/round-32-verifier-spotcheck.md:93`: "are committed without a `round-32/manifest.json`", "so the 38-record target is not silently moved"). **Captured by:** no seat in round 32 — i.e. captured by none, which is why it needed a criterion. **Criterion:** `corpus/QUALITY.md` gains **R20** (a capture snapshot dir ships its `manifest.json` in the same round/commit; every record carries a registry-`url` plus one provenance field) and **R21** (a sourced claim's manifest carries the provenance that separates a fabricated capture from a real one; shape counts are not a capture check), each grounded in this mistake and in `corpus/lessons/round-31.md:146` (`wave1/ScribeQuality.md` §1, append-only proof 55 insertions / 0 deletions in §3). **Fix:** the C1 instrument plus the round-32 manifest (`sha256 6e4e719a…c774`, `fetched_utc=2026-10-25T23:14:00-03:00` on both records, URLs `https://zc.cnvd.org.cn/news/helpList` / `https://security.360.cn/Reward/rules`), shown **able to fail** by `wave1/ExecErratumCheck.md`: RED before (`CHECK round-32-manifest FAIL reason=manifest-absent … captures=S049.txt,S050.txt`, `CLOSURE checks=2 failed=1 exit=1`) and on base-tree bytes (`failed=2 exit=1`), GREEN after (`PASS records=2 ids=S049,S050 fetched_utc=2 url_exact=2`, `exit=0`), with four independent red classes in §6 (absent manifest, dropped `fetched_utc`, non-contract URL, truncated JSON) — and the lane manifest untouched by the delete test (`6e4e719a…` re-hashed after).
- **M33-2 — the round-32 report misquoted the dispatcher log.** Class: evidence hygiene. The round-32 report said "occupied 18 at 23:15:04"; the log line says `occupied 67` at that timestamp, and the cited log lived under `/fast/scratch`, which a fresh session may not reach (`corpus/lessons/round-32-verifier-spotcheck.md` §1 row "dispatcher-log quote", defect D4). **Fix:** a committed digest of exactly the lines the claim rests on — `.ufo/waves/round-33/watchdog-digest.txt` (`sha256 7bf40db6…63ed85`, 3 lines, each `source-line-number:line-text`), committed at the freeze commit `6e55c8d`. **Verified:** `wave1/ExecErratumCheck.md` §4 re-reads the fleet log read-only and prints `line 1455: MATCH`, `line 1457: MATCH`, `line 1468: MATCH`; `git show 6e55c8d:.ufo/waves/round-33/watchdog-digest.txt | sha256sum` equals the worktree digest. This lesson therefore cites only committed receipts and the committed digest, never a scratch log path.
- **M33-3 — the registry append moved four section anchors and deepened the already-stale `SOURCES.md:83` trail (M31-3 recurring).** Class: anchor drift (R6). Two appended rows + one Search-log bullet shift `## Paths` 56→58, `## Search log` 63→65, the round-31 sweep line 72→74, `## Leads` 74→77, `## Registry changes` 80→83, and the S043 change-cell line 87→**90** (`wave1/ExecRegistryAppend.md` §8, measured before/after). The citations at `corpus/lessons/round-29.md:214` and `round-29-verifier-spotcheck.md:74` were already +4 stale (`corpus/lessons/round-31.md:147`) and are now **+7**. `wave1/ConnOwnership.md` F4 predicted +6 pre-land and corrected itself to **+7** post-land (the Search-log bullet adds one in-section line, a further +1). This row is the R9-style erratum F4 asks for: it names the M31-3 wording (`corpus/lessons/round-31.md:147`, "`SOURCES.md:83` citations now off by +4") and cites the corrected line (`corpus/SOURCES.md:90`), while the filed sentences at `corpus/lessons/round-29.md:214` and `round-29-verifier-spotcheck.md:74` are left **byte-identical**. No row-level citation moved (`:22`, `:46`, `:47`, `:48`, `:54` unchanged), and the rows cannot be placed elsewhere (census `E12` fires on a row-shaped source outside `## Registry`). **Status: recorded here; the correction to those two lesson files remains routed**, since `corpus/lessons/**` other than this file is not this seat's write scope.
- **M33-4 — a Q3 "verbatim" quote drifted in a citation heading and was caught only by the independent sweep.** Class: quote-hygiene (Q3). The entry's `source:` line and its Claim 1 attribution cited the question stem as 「…漏洞提交时…」 while the capture reads 「…提交漏洞时…」 (`wave1/RevQuoteSweep.md` §5: `grep -c '提交漏洞时'` on the entry → 0 at the reviewed digest `53c48b3b…`). No claim changed (the answer quote at `S049.txt:211` was byte-perfect). **Captured by:** `RevQuoteSweep`, a non-author seat. **Fixed by the owner** (`ExecEntryF16`), and re-verified by the same seat in §6 on `1f7ac0a2…`: `漏洞提交时=0 提交漏洞时=2`, `L48` now cites `S049.txt:210-211`, `source-recheck` exits 0 both sides. The class is exactly what the sweep exists for: a paraphrase inside a *citation*, not inside a claim.
- **M33-5 — the entry moved four times inside the wave, and the C1/C2 counters of record ran on a superseded digest.** Class: in-flight measurement (M30-3 / M31-2 recurring). Digest history recorded across receipts: `de184a5b…` (270 lines) → `eebd5ea5…` (305) → `53c48b3b…` (306, `24492 B`) → `1f7ac0a2…` (306, `24539 B`) (`wave1/RevEntryF16.md` §0; `wave1/RevQuoteSweep.md` §6). `ExecHarnessC2` (§0/§4) and `ExecRegressionC1` (§0 pin) measured `53c48b3b…`; the integration commit carries `1f7ac0a2…` (`git show 9f98488:corpus/knowledge/…` re-hashed by this lesson), and `ExecCensusAfter` (§0) discloses the gap and states it read the entry only as a `used-by` path-existence check. **No counter value changes**, because no counter reads the entry body (harness reads `knowledge-expected.txt`, `source-recheck` reads the manifest + captures, census reads registry rows) — and this lesson re-ran all nine C2 cells plus both C1 runs on `1f7ac0a2…` with input bookends identical (`04:42:45Z` → `04:44Z`, `BOOKEND_IDENTICAL`). Fix/rule: a receipt's digest is a measurement with a timestamp, and an after-column must be re-run on the committed byte, not on the working tree of its moment.
- **M33-6 — two survivor events, both closed by a clause outside the plain-run rule.** Class: limb-oracle gap (QUALITY **R17**). (a) `url`-missing (rule B): a one-line mutant prints `records=2 bound=2 unbound=0` exit 0 and is **SURVIVOR** under the plain-run kill rule on both pinned generations; it is killed by `--selftest` (`failures=1`) and its signature is visible on the `AUDIT` line (`with_url=1` against `records=2`) which the kill rule does not read (`wave1/MutCtrUnbound.md`). (b) entry↔harness header binding: dropping one `source:` line from the entry leaves `entries=19 pass=19 exit=0` because `frontier-recheck-count.py` rule A is one-directional (`declared ⊄ recheck_ids` fires, the reverse does not); the mirror mutation (dropping `--source S050` from the recheck line) **is** caught, and C2 counter 2 covers the header side (`wave1/MutEntryF16.md` § Verdict). Everything else in the mutant set was killed: the four frozen counter mutants (`accept-record-without-url`, `accept-url-not-in-registry`, `skip-fetched_utc-requirement`, `skip-selftest`: `wave1/ExecCaptureBinding.md` §6 4/4, `wave1/MutCtrUrlMismatch.md`, `wave1/MutCtrFetchMissing.md`, `wave1/MutCtrSelftestSkip.md` — the last caught by the "`failures=0` lines printed from real cases" clause — a forged `cases=0 failures=0` summary is self-incriminating and comes with no `selftest case=… verdict=` lines, so exit 0 alone would not have caught it), rule A (`wave1/MutLegacyManifestDrop.md`), and url-removal (`wave1/MutManifestLegacy.md`). No survivor was relabelled killed.

## considerthese

`considerthese/2026-10-25.md` proposal 1 ("cap wave-evidence bloat; measure per-round repo growth") is **mined → measured**, not merely re-affirmed. R14 was already its round-28 landing (`corpus/QUALITY.md` R14); this round adds the figure the proposal asks for, from committed bytes: `.ufo/waves/round-33` holds **1,366,042 B in 132 committed files** at the integration byte (`9f98488`), **27.3 %** of the round's 5 MB budget, with **0** `/corpus/` paths and **0** scratch trees in the tree; composition is 52 receipts 771,618 B (56.5 %), 58 support dumps + `swarm-registry.json` 233,279 B (17.1 %), wave root 361,145 B (26.4 %) — of which the four planner artifacts alone are 334,575 B (24.5 %) (`wave1/ExecGrowthMeasurement.md` §1, §3, §4). Its own controls are the reason the figure is citable: an untracked file is invisible to the diff counter, `ls-tree -l` matches file sizes, untouched round dirs read 0 lines, and the baseline dir is absent at BASE (§0). The same-command longitudinal table runs rounds 23–33 (round-25 57,511,001 B / 3,773 files; round-31 2,991,556 B; round-33 1,366,042 B) (§5). Re-run after this file lands: `git -C {LANE} ls-tree -r -l HEAD -- .ufo/waves/round-33 | awk '{s+=$4} END{print s}'`; the working-tree form at composition read 134 files / 1,394,842 B and is **not** the committed column. One confirmed waste candidate is named without a fix: compressing the four support directories as one stream yields 43,009 B from 233,279 B, i.e. ≈190 KB headroom, below R14's threshold so no tarball was required (§6).

The other five proposals are **unchanged**, with the reason stated from the lane's own ledger rather than assumed: 2 (`score-gap.py`, distance to the next score) is `mined round 31` and this round adds no new reporter; 3 (bounty craft / SHONEN box 2) stays `partially landed` — the severity plank is F13's, the craft remainder has not landed and `SHONEN.md` is `ScribeShonen`'s seat this round; 4 (proposal status ledger) is `mined round 30` into `corpus/knowledge/considerthese-proposals-ledger.md`; 5 (open-defects ledger with runnable closure checks) is `mined round 29` into R15 and is the mechanism this lesson's own "open items" list uses; 6 (event-driven reflections) stays `open` with no landing or decline recorded (`corpus/knowledge/considerthese-proposals-ledger.md` round-31 status block; `wave1/ExecGrowthMeasurement.md` §3). No score move is claimed from any of them.

## Census before → after

- **Before** (`census-before.txt`, frozen at claims time): `kasegi W04 S028 duplicate url docs.hackerone.com/…`, `kasegi W04 S029 duplicate url eur-lex.europa.eu/…`, `kasegi ok …/corpus/SOURCES.md`, `census_exit=0`; and the six contract commands `rows=48`, `malformed=0`, `tier=A=45 B=1 C=2`, `status=mined=36 queued=9 rejected=3`, `dups=` empty, `enum_violations=0`, `missing_usedby=0`.
- **After** (`wave1/ExecCensusAfter.md` §1–§2): the validate command prints the **same three lines** — the two `W04` warnings and `ok` — with `census_exit=0`, `grep -c '	E[0-9]+	'` → 0 and no new `W`; the six contract commands read `rows=50`, `malformed=0`, `tier=A=47 B=1 C=2`, `status=mined=38 queued=9 rejected=3`, `dups=` empty, `enum_violations=0`, `missing_usedby=0`. The seat first replayed the six commands on the frozen base bytes and got a byte-identical reproduction of the stored block (`REPRO-IDENTICAL`, §2).
- Re-run by this lesson on the committed bytes (`04:44Z`): `census_exit=0`, same three lines, `frontier_admitted=16`, `rows=50`, `S049=1 S050=1` citing entries, bookend identical. Row/shape agreement with the previous round is expected; what changed is `rows 48→50`, `mined 36→38`, `tier.A 45→47`, and nothing else.

## No-harm

`wave1/ExecNoHarmFinal.md` (the assigned sweep) plus `wave1/RevNoHarm.md` (independent SKILL/PROVINCE review), both read-only, both on committed bytes (`git show HEAD:` digests equal the worktree digests for `SKILL.md` `b11b6085…` and `corpus/SOURCES.md` `b22c7f01…`).

| Instrument | Before (base `690b69d`) | After (landed) | Verdict |
|---|---|---|---|
| `density.py SKILL.md` | mean dens **191.5** (689 cites / 24 blocks, `exit=0`) | mean dens **201.7** (710 cites / 25 blocks, `exit=0`) | Same verdict class, higher density; the appended round-33 gate row adds one block / 19 lines / 21 citations (`wave1/ExecNoHarmFinal.md` §3; `wave1/ExecRegressionC1.md` §2.9 independently: 191.5 → 201.7) |
| `anchorcheck.py SKILL.md` | 7 in-range, **0 bad**, `LOST-RECORDED=306`, `PIN-BROKEN=0`, `ORIGIN=0`, `OUTSIDE-BASE=0`, `BASE-ABSENT=0`, `exit=0` | 12 in-range, **0 bad**, `LOST-RECORDED=306`, all failure classes 0, `exit=0` | Every failure class identical; the five new anchors the gate row cites all resolve. `ExecRegressionC1` §1 flags `7→12` as a **deviation** from the item's literal expectation (D-R33-1) — the literal is a base-state count, the class is unchanged (`ExecNoHarmFinal.md` §4) |
| `resolve.py` (scratch trees only) | base-tree lane rate **414/2516 = 16.45 %** (SKILL 55/547) | HEAD-tree **438/2563 = 17.09 %** (SKILL 70/563, corpus 412/2219) | +0.63 pp on a comparable scope; `RESOLVES` stays 28, `MIRROR-EQUIVALENT` 0, `INTERNAL` +24, `GONE` +23 (§5). The committed census still prints 9.05 % (134/1480) from round 20 over a 50-file scope and is **not scope-comparable**; no regression is claimed and no per-round split was measured. `resolve.py` writes `citation-survival.*` beside itself, so the lane copies were never re-run in place — mtimes still `2026-10-25T04:15:16` |
| `recheck-audit.py --quiet` | `strict pass=44/44` (round-31 landed figure; re-read by `wave1/RevNoHarm.md` §5 on the pre-append tree: `lines=44 … expect=present expected=44 missing=0 unexpected=0 exit=0`) | `strict pass=45/45 cdroot_fail=0 instrument_fail=0 own_fail=0`, `lines=45 total=45 pass=45 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0`, `expect=present expected=45 missing=0 unexpected=0`, `exit=0` | One line added with the new entry; no failure class moved (`wave1/ExecRegressionC1.md` §2.5). `RevNoHarm` is the earlier state, taken before the `SKILL.md`/`PROVINCE.md` appends landed (`git diff 690b69d -- SKILL.md PROVINCE.md \| wc -c` → `0` at its read), so 44/44 and 45/45 are two moments, not a disagreement |
| `SKILL.md` / `PROVINCE.md` vs base | — | **19 / 0** and **2 / 0** numstat, `git diff \| grep -c '^-[^-]'` → 0 | Additions only, no line deleted (`wave1/ExecRegressionC1.md` §2.10, `wave1/ExecNoHarmFinal.md` §2). `wave1/RevNoHarm.md` §6 read a `0`-byte diff because it ran before those two appends landed — the same two moments as the `recheck-audit` row above |
| unowned writes in the working tree | — | **0** (three dirty paths, all seats' own receipts); whole round `owned=71 l1=23 unowned=57` by path class | No seat wrote another's file (`ExecNoHarmFinal.md` §1) |

## Open items / unverified

1. **The two header placeholders** (`WAVE_DISPATCH_PENDING`, `LANDED_HASH_PENDING`) are the L1's edit; this seat must not commit.
2. **C1's capability clause landed late in the wave and is cited from one seat only.** `SCORECARD.md` mtime moved `2026-10-25 22:51` → `01:50:50`, digest `e03fbefa…`, and `grep -n capture-binding-check SCORECARD.md` now returns the round-33 table row at `:1078` (`wave1/ScribeScorecard.md` §3, append-only +111 / 0). Its two `<LANE_HASH>` markers are the L1's edit; this lesson does not verify the appended numbers beyond their receipt, which cites `ExecRegressionC1`/`ExecCensusAfter`/`CritC1Kill` as its sources.
3. **Eight seats had no receipt** when this file was composed (list in the header). Three are review lanes whose verdicts this lesson cannot substitute: `RevGateSpot` (gate spot-check), `CritMistakes` (mistake-class critique), `RevC1BeforeAfter` (independent before/after). `ExecScratchDiscipline`, `SimplifierCleanup`, `ScribeReportDraft` and the L1's edits are owed; `SHONEN.md` token state is asserted only from `wave1/ScribeShonen.md`, and `ExecWaveEvidencePack`'s token table is quoted as a count, not as a review.
4. **C1 blind spots not landed** (`wave1/CritC1Kill.md` § "Smallest safe corrections"): D1 capture-byte binding (H1/H2/H3), D2 recursive scan (H4: a nested `source-snapshots/nested/round-32/` hides 2 records with `exit=0`), D3 `fetched_utc` parsing (H5: `"pending"` passes), D4 per-manifest uniqueness (H6), D5 single-`https://`-token rows (H7), D6 anchor row must be `mined` (H8), D7 per-dir floor. All seven are proposed, none landed; each is measured, not argued.
5. **C2 garbage-passes-counters** (`wave1/CritC2Kill.md` §5) and the harness's one-directional rule A (`wave1/MutEntryF16.md`) are open at the instrument level; only prose review and counter 2 cover them.
6. **Anchor drift M33-3** is open and routed to `corpus/lessons/**` (not this wave's scope): `SOURCES.md:83` citations are off by **+7** after this round's 6-line append.
7. **`citation-survival.md` is stale by scope** (round-20 census, 50 files, 9.05 % vs today's 17.09 % over 89 files). Both figures are stated; neither is claimed as a score input, and the instrument still writes beside itself so no seat may regenerate it in place without owning that path.
8. **The `multi_row_url` disclosure is load-bearing** for reading C1 across rounds: if the canonical judge reads the frozen kill rule's "0 or 2+ matches = failure" literally, S029 and S006 fail and C1 reads `bound=38`; under erratum-1 (id-scoped) it reads `40`. The erratum is filed and the instrument implements it; the erratum's own status in `claims.json` is the L1's record, not this lesson's.
9. **Currency unmeasured**: the S049/S050 re-opens are two single-instant fetches (`2026-10-26T04:16:06Z` / `:16Z`, one host), ~2 h after the round-32 capture commit; they say nothing about the pages before or after, and post-conversion text equality does not prove raw-body equality (`wave1/ScoutLiveDrift.md` § Bounds).
10. **This lesson's own sweep is a word sweep, not a review**: `BLOCKED`/`DEFECT`/`SURVIVOR`/`FAIL`/`traceback`/`PRE-STATE` counts over 56 receipts are in § Mistakes; `FAIL` (161 hits) is dominated by fixture output and was not read line by line, so § Mistakes is a list of the events this seat opened, not a claim of completeness.

## Touched surfaces and provenance

This lesson's only production path is `corpus/lessons/round-33.md`; the scoped seat report is `.ufo/waves/round-33/wave1/ScribeLesson.md` (it holds the commands, their output and the file digest). Evidence paths are named inline, principally `.ufo/waves/round-33/{claims.json,claims-erratum-1.md,census-before.txt,c1-controls/*,c2-controls/*,assimilation/*,watchdog-digest.txt,wave1-spec.json,wave1-dispatch.json,wave1.ready}` and `wave1/{ScoutManifestAudit,ScoutLiveDrift,ScoutPackageThemes,ScoutF16Sweep,ScoutDatawalk,ConnSibling,ConnOwnership,ConnClaims,ExecCaptureBinding,ExecManifestUpgrade,ExecManifest32,ExecEntryF16,ExecRegistryAppend,ExecCensusDry,ExecExpectedList,ExecHarnessC2,ExecRegressionC1,ExecCensusAfter,ExecErratumCheck,ExecQuarantine,ExecNoHarmFinal,ExecGrowthMeasurement,ExecDeterminism,ExecForeignCwd,ExecBeforeReceipts,RevEntryF16,RevRowS049,RevRowS050,RevQuoteSweep,RevManifestUpgrade,RevClaimsFreeze,RevNoHarm,CritC1Kill,CritC2Kill,CritExpansion,CritBoundary,MutCtrUnbound,MutCtrUrlMismatch,MutCtrFetchMissing,MutCtrSelftestSkip,MutLegacyManifestDrop,MutManifestLegacy,MutEntryF16,SentCred,ScribeQuality,ScribeReadmeF16,ScribeInstrReadme,ScribeProvince,ScribeSkillGate,ScribeSearchLog}.md`. Read-only outside the lane: `/home/vgpnk/Projects/shokuknow/merge/kasegi/` and `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (read by other seats; this seat read only the lesson, claims, receipts, register rows and lane bytes). No package tool was run, nothing was written there, no network fetch was made by this seat, no bounty target was contacted, and no credential material is reproduced here. No git/jj mutation: `rev-parse`, `log`, `show`, `ls-tree`, `diff`, `status` only. No tool was installed or upgraded. Scratch `/fast/scratch/hyaku/kasegi-r33/ScribeLesson/` held only the two bookend digest files and was removed before yield.

## Erratum (round 34) — R7: the S049/S050 quote counts and the S050 sentence line

Appended 2026-10-26 (round 34) to `corpus/lessons/round-33.md` at lane base `014ee2d` — changed-file
scope: this file only; pre-append sha256
`ca17591d4a36e1a6623adb9acb7ac2bc0a3dbd87c24f3913229fe0b4b781feb2`, 138 lines. Nothing above this
block is edited (QUALITY R6/R9: a numerical erratum names its base and changed-file scope, re-opens
every line pointer against the cited revision, and leaves the filed assertion byte-identical).
Routed by `corpus/lessons/round-33-verifier-spotcheck.md:181` (R7).

### (a) Quote lengths at `corpus/lessons/round-33.md:31-32` — 19 → 31 and 23 → 22

The filed lines read "Quote (19 characters, `S049.txt:214`, accessed 2026-10-26)" and "Quote
(23 characters, `S050.txt:591`, accessed 2026-10-26)". Corrected counts, with the command that
produces them (run 2026-10-26T05:32Z on the committed captures):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
printf '%s' '众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。' | wc -m   # 31
printf '%s' '未纳入安全服务的资产一般情况下不收录相关漏洞' | wc -m                    # 22
```

Counting convention, so the figures re-derive (R3/R19): the count covers the quoted characters
only; the 「」 corner brackets are the lesson's delimiters and are excluded — including them the
same two `printf … | wc -m` runs print 33 and 24. Both strings occur on exactly one line of their
captures (`grep -cF` → `1` each; 20272 B / 426-line S049 and 31016 B / 630-line S050), at
`S049.txt:214`, whose opening clause the S049 quote is, and `S050.txt:591`, where the S050 quote
follows the `10、` enumerator. Locations, access dates and capture digests (`962a451a…1cb8`,
`2f9c6406…6888`) stand, so both admits stand; only the two counts moved. Independently found by
`wave1/RevGateSpot.md` § Findings 1 (`len()` in python3 → 31 and 22), which left this file
unedited.

### (b) The S050 applicability sentence is at `S050.txt:70`, not `:69`

`sed -n '69,71p' corpus/source-snapshots/round-32/S050.txt`:

```
69: 一、适用范围
70: 本标准适用于 360 集团发布的产品和业务，此外 360 集团所投资的公司、子公司、合资公
71: 司等也在收录范围内，具体范围可参考 https://security.360.cn/Product/product。
```

The section heading `一、适用范围` is L69 (the string occurs twice in the capture: a
table-of-contents copy at L25, the heading at L69); the applicability sentence begins at **L70**
and wraps into L71, `合资公司` being split across the line break — the wrap this file's `## Gate`
§ "Capture quirks" already states. **Every citation of `:69` for that sentence is corrected to
`:70`.** Sweep of the lane (`corpus/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`) plus the fleet report,
each pointer classified:

| Citation | What it names | Verdict |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md:61` (fleet report, read-only to the lane; sha256 `0a2c6758…41b3e7c6`) — 「本标准适用于 360 集团发布的产品和业务」 `(S050.txt:69)` | the applicability sentence's opening clause | **corrected to `S050.txt:70`** — this is R7's citation slip (the quoted clause is L70's first line) |
| `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md:97` — `S050.txt:70` | the same sentence | already correct, no change |
| same entry `:4` — `一、适用范围 (L69-71)` | section span (heading + wrapped sentence) | correct as a range |
| `corpus/SOURCES.md:56` (S050 row cell) — `一、适用范围 L69-71 (the sentence wraps across L70-L71)` | section span with the wrap named | correct |
| `corpus/lessons/round-32-verifier-spotcheck.md:73` — "适用范围 at L69" | the heading | correct |
| this file `:46` — `§一 L69–71` | the section | correct |
| `.ufo/waves/round-33/wave1/{ScoutF16Sweep.md:92, ExecRegistryAppend.md:69, RevRowS050.md:75, RevGateSpot.md:67, ScoutPackageThemes.md:62}` | section spans / the L69 heading with L70-71 named as the sentence | correct as filed |

No lane production file cites `:69` for the sentence; the single sentence-level slip is the fleet
report line, and this block is its correction of record (that path is outside this lane's write
scope — it was read-only). Sweep command:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
grep -rn 'S050\.txt:69\|(L69\|适用范围 L69' --include=*.md corpus/ SCORECARD.md LOG.md SKILL.md
```

### What this erratum does not change

The admits F16/S049 and F16/S050, the quote locations, the access dates, the capture digests and
every counter in this lesson are untouched; R7's two limbs are a character count and a one-line
pointer. Post-append digest of this file is recorded in the round-34 seat receipt
(`.ufo/waves/round-34/wave1/ExecLessonErrata.md`); `head -138` of this file is byte-identical to
the pre-append file.

## Erratum (round 34) — R4: "all mutants killed" overstated; the frozen kill rule caught 3 of 4

Appended 2026-10-26 (round 34) to `corpus/lessons/round-33.md` at lane base `014ee2d` — changed-file
scope: this file only (append-only; the paragraph below is added for R4's closure, see
`corpus/lessons/round-33-verifier-spotcheck.md:174`). Routed by **R4**; the lesson and the fleet
report asserted a mutant obligation that the round-33 receipts do not support.

The fleet report's C1 verdict line reads "C1: target met. 40/40/0 with all mutants killed, fake
rejected, selftest 11/11" (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md:49`,
read-only to this lane; sha256 `0a2c6758…41b3e7c6`). Measured on the round-33 receipts, the
counter's four mutants were killed **3 of 4 (3/4)** under the frozen kill rule as written, plus a
separate plain-run survivor:

| mutant | verdict under the frozen kill rule | evidence |
|---|---|---|
| M1 accept-a-record-without-url | **caught** — `selftest cases=11 failures=1` exit 1, case `record-without-url` `exit=0 want=1` | `wave1/RevClaimsFreeze.md` § "The four counter mutants" |
| M2 accept-url-not-in-registry | **caught** — `failures=1`, case `url-mismatch` | same |
| M3 skip-fetched_utc-requirement | **caught** — `failures=1`, case `round-32-record-without-fetched_utc` | same |
| M4 skip-selftest | **survived** — prints `selftest cases=9 failures=0` exit 0 without running any fixture; the kill rule's selftest clause as worded does not bite | same, finding F-5: "M4 skip-selftest is **NOT** caught by the kill rule text" |
| accept-record-without-url (plain run) | **survived** — `records=2 bound=2 unbound=0` exit 0 on a url-less fixture, on both pinned generations of the instrument | `wave1/MutCtrUnbound.md` § Verdict ("**SURVIVOR** under the frozen C1 kill rule as tasked (plain run)") |

So "all mutants killed" is corrected to: **3 of the 4 counter mutants killed under the frozen kill
rule (3/4), M4 surviving it, and one plain-run survivor on the url-missing limb** — not all killed.
Both survivors are killed only by a clause outside the plain-run rule: the selftest clause (M4) and
the round-34 tightened rule requiring `cases>=11` with one `selftest case=` verdict line per case
(C1's survivor counter, `corpus/instruments/kill-rule-check.py` — absent at this append, `test -e`
→ exit 1 at 2026-10-26T05:42Z, landing in the same round's C1 work). The overstatement is recorded as
mistake **M34-1** in the round-34 claims
(`.ufo/waves/round-34/claims.json` `non_claim_frontier_items.mistake`).

What this erratum does not change: the binding measurement itself — `records=40 bound=40 unbound=0`,
`binding_exit=0`, `selftest cases=11 failures=0` — stands as filed. The overstated fact was the
mutant obligation, not the binding count.
