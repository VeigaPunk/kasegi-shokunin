# ScoutPackageThemes receipt — round 35 (package standing refusals re-confirmation)

Answering model: anthropic/claude-sonnet-5-5. Read-only on `/home/vgpnk/Projects/shokuknow/merge/kasegi/` and the shokuknow register; read-only on the lane except this file. No package tool run (`renumber-staged.py`, `merge-plan.py`, `quote-lint.py`, `absent-defect-register.py` untouched), no network call, no subagent. Baseline: `corpus/lessons/round-34.md` § Gate "Rejected — standing refusals" (lines 141–151) and `.ufo/waves/round-34/wave1/ScoutPackageThemes.md` (`sha256 151227ae…d9ee`). Reads timestamped 2026-10-26T06:37:13Z–06:37:40Z.

## Verdict

**Assimilation: none.** No flip condition of any of the seven refused staged entries cleared this round. The package did not move (every digest byte-identical to round 34), the lane registry still has **51 rows (S001–S051)** at read time (the C2 S052 row is not yet appended: `grep -c S052 corpus/SOURCES.md` → 0 at 06:37:40Z; capture `corpus/source-snapshots/round-35/S052.txt` exists), and no S036 / S044–S047 (PRC) / S077–S079 / S081–S082 row or capture exists anywhere under `corpus/` outside `lessons/`. The round-35 C2 admission (F18 / S052 CISA KEV) is not cited by any staged file (`grep -rliE 'cisa|known exploited|\bKEV\b'` over the whole package → **0 files**), so it cannot unblock any refused entry.

| staged entry | round-35 verdict | any flip condition cleared this round? |
|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` | REFUSED (standing since r30) | **No.** Registration clause already met in r33/r34 (staged S034/S035 = lane S049/S050 by URL; S031 = lane S043); still 0 located quotes (`txt:[0-9]+` → 0), no executable recheck, `ground: F09` collides with admitted lane F09 |
| `claim-packaging-and-report-quality.md` | REFUSED (standing) | **No.** Body cites S034/S035/**S036**; S036 BILISRC V1.7 still in **no lane row and no capture** (`grep -ciE 'bilibili\|BILISRC' corpus/SOURCES.md` → 0; no snapshot hit) |
| `cn-crowdsourced-testing-roles-and-conduct.md` | REFUSED (standing) | **No.** H1 count 0; S081/S082 URLs in no row/capture |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | REFUSED (standing) | **No.** S077/S078/S079 in no row/capture; `ground: F24` is not a lane F-id (lane frontier F01–F17 today, F18 pending C2) |
| `chinese-criminal-thresholds-and-authorisation.md` | REFUSED (standing since r30) | **No.** Body cites staged S034/S044/S045/S046; the three PRC legal sources (court.gov.cn / czt.ln.gov.cn / nj.jsjc.gov.cn) in no lane row/capture; staged `S044`–`S046` ids are lane Bugcrowd/IPA rows |
| `chinese-program-severity-instrument.md` | REFUSED as an entry (r33) | **No.** S047 sse.com.cn not registered; anchor `newsType_6` → 0 in `round-32/S049.txt`, `newsType_21` → 1 |
| `program-severity-ladders-and-reward-scales.md` | REFUSED / do-not-copy | **No (not a flip).** Same-name lane file still differs (lane `6c05c98f…` vs staged `35de5f8b…`); S036 half still unregistered |

## Evidence

### 1. Package unchanged (`sha256sum` / `stat`, 2026-10-26T06:37:13Z)

```
4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb  merge/kasegi/SOURCES.append.md   (mtime 2026-10-24 23:33:20 -0300)
8a42a9109c8c95bc55e818f0ad97e7923cbfe5a9e7792c72c59b5aaa3aecbf5b  merge/kasegi/MERGE-REPORT.json
0e6759b47595f1bce5fbf49bf0422838ff89a394b2f424d17fb17d96a09106df  merge/kasegi/MERGE-REPORT.md
5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833  .ufo/waves/corpus-expansion-1/absent-defect-register.md   (mtime 2026-10-24 08:37 -0300)
120d8cd5d50b703809a1c1030eb3b16564251e69a8208e4c90b500343d99abc8  program-scope-rules-and-asset-boundaries.md
6ad64d785f8f767bc0e86a4967b80bcc636b5939af4ac41b1138911978ec8dbc  claim-packaging-and-report-quality.md
a5302aaf0b9a1502c8711cd620cf0cb87cd9fea8db192269fae31619548fe813  cn-crowdsourced-testing-roles-and-conduct.md
6c15d94114248beb433eeb35aca116eb2ff4beaf7abfbc9d2b9957aeb56ef83f  chinese-crowd-testing-national-standard-2026-10-23.md
1660c00c16369d0a50870185607e0a8006ed573cc4ae69a696ce568e4e8a59ae  chinese-criminal-thresholds-and-authorisation.md
442e0f2bfb08bc2cbb8951f110e64424f82203636928429bc38f46f388c4257c  chinese-program-severity-instrument.md
35de5f8b19ed3b20beb3d41c347f4727d9fd2eefc8a23e53c64c6987b60bbc87  program-severity-ladders-and-reward-scales.md
```
All seven match the digests in `corpus/lessons/round-34.md:145-151` and in the round-34 receipt § 1. `find $P -type f -newer .ufo/waves/round-34/claims.json` → empty (no package file newer than the round-34 claims freeze); newest package mtime `2026-10-24 23:33:20 -0300`. Package knowledge files: 67 (unchanged).

### 2. Lane registry vs package (python3, 0–3-space row pattern `^ {0,3}\|\s*(S\d+)\s*\|`)

```
lane_rows 51 S001 S051
staged_rows 94
collisions 21 S031 S051          (round 34, post-S051: reg_ids=51 staged_ids=94 collisions=21 — identical)
lane frontier F01 F17 17
```
`bash .ufo/waves/round-35/assimilation/collide-check.sh <registry> merge/kasegi/SOURCES.append.md wide` on a copy of `corpus/SOURCES.md` → `kind=wide reg_ids=51 staged_ids=94 collisions=21 ids=S031 … S051`, exit 0 (equals the committed `.ufo/waves/round-35/assimilation/collisions`, 21 lines). With a simulated `| S052 |` row appended to the copy → `reg_ids=52 collisions=22 … S052`, exit 0: **the S052 landing will extend the collision range to S031..S052**. Staged `S052` is a **different document** (CNNVD weekly 信息安全漏洞周报 2026 年第 40 期, `…/group1/M00/03/2C/rBBl8WrPKoaAKy_IAAT1JLp2GFY923.pdf`) from lane `S052` (CISA KEV JSON feed, `corpus/source-snapshots/round-35/manifest.json`); none of the seven refused entries cites staged S052 (cited ids below), so this adds no flip and no new refusal, only one more adoption-by-number hazard (adoption is by document, never by number).

Staged-row URL join against lane rows (staged id → lane row by URL, today; `anywhere` = URL host/path string found in any `corpus/` file outside `lessons/`):

```
S031 hackerone.com/security/policy_versions         -> lane S043   anywhere True
S032 raw.githubusercontent…/vrt/master/README.md    -> lane S044   anywhere True
S033 raw.githubusercontent…/mappings/cwe/cwe.json   -> lane S045   anywhere True
S034 zc.cnvd.org.cn/news/helpList                   -> lane S049   anywhere True
S035 security.360.cn/Reward/rules                   -> lane S050   anywhere True
S036 security.bilibili.com/static/docs/BILISRC_V1.7.pdf -> NONE    anywhere False
S044 court.gov.cn/fabu/xiangqing/3085.html          -> NONE        anywhere False
S045 czt.ln.gov.cn/czt/attachDir/2026/05/2026050715041524122.pdf -> NONE  anywhere False
S046 nj.jsjc.gov.cn/jianwu/zhinan/202109/t20210917_238200.shtml  -> NONE  anywhere False
S047 sse.com.cn/…/028395e1b8364d3bb3fcb28d565de306.pdf -> NONE     anywhere False
S077 std.sacinfo.org.cn/gnoc/queryInfo?id=E8261DDA…  -> NONE       anywhere False
S078 sac.gov.cn/xw/bzhdt/art/2024/art_f1892c53….html -> NONE       anywhere False
S079 openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=57CAF3B4… -> NONE anywhere False
S081 zc.cnvd.org.cn/news/info?id=133&newsTypeCode=100100 -> NONE   anywhere False
S082 std.samr.gov.cn/gb/search/gbDetailed?id=D0FE299A…   -> NONE   anywhere False
```
Same result as the round-34 receipt § 2 (the only differences from round 34 are the already-reported S051 row and the in-flight S052 capture, neither in the join set). `grep -rlE 'BILISRC|security\.bilibili' corpus/source-snapshots` → 0 files (the only non-lesson `corpus/` hit is `corpus/knowledge/program-severity-ladders-and-reward-scales.md`, its BILISRC history prose); the second pattern (`news/info?id=133|D0FE299A|E8261DDA|57CAF3B4|sacinfo|sac.gov.cn|court.gov.cn|czt.ln|jsjc.gov|sse.com.cn|samr.gov`) → 0 files outside `lessons/`. Captures present: round-23…26, 28–32, 34, 35 (`round-35/{S052.txt,manifest.json}`; `S052.txt` sha256 `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`, id `S052`, url `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`); none for any staged-only URL.

### 3. Per-entry mechanical measures (python3 over the seven staged files; read-only)

| entry | lines | H1 | `ground:` | lane F-id? | located `txt:N` | 「…」/«…» | exec recheck | `source:` line → ids cited anywhere in body |
|---|---|---|---|---|---|---|---|---|
| program-scope-rules-and-asset-boundaries | 39 | 1 | F09 | yes — **different lane item** | 0 | 0 / 0 | no | S031 → S031 S034 S035 |
| claim-packaging-and-report-quality | 45 | 1 | F11 | yes — different item | 0 | 0 / 0 | no | S034 → S034 S035 **S036** |
| cn-crowdsourced-testing-roles-and-conduct | 45 | **0** | `round-6 ledger item 2 …` | not an F-id | 0 | 0 / 0 | no | S081 → S081 S082 |
| chinese-crowd-testing-national-standard-2026-10-23 | 45 | 1 | F24 | **no** (lane F01–F17) | 0 | 0 / 0 | no | S077 → S077 S078 S079 |
| chinese-criminal-thresholds-and-authorisation | 57 | 1 | F12 | yes — different item | 0 | 0 / 0 | no | S044 → S034 S044 S045 S046 |
| chinese-program-severity-instrument | 41 | 1 | F10 | yes — different item | 0 | 2 / 0 | no | S034 → S034 **S047** |
| program-severity-ladders-and-reward-scales | 50 | 1 | F10 | yes — different item | 0 | 0 / 0 | no | S032 → S032 S033 S034 **S036** |

Same-name overwrite test: `samename_lane=True` among the seven refused entries only for `program-severity-ladders-and-reward-scales.md` (lane `6c05c98f…`); the other three of the four same-name names in the round-34 receipt § 3 (`authorised-testing-rules-of-engagement`, `japanese-domestic-disclosure-workflow`, `japanese-severity-vocabulary-and-impact-model`) are non-refused entries and were not re-measured here.

### 4. Per-entry reason and flip status

1. **program-scope-rules-and-asset-boundaries** — Flip clause "register+capture CNVD helpList and 360SRC rules" stays **met** (S049/S050, round 32 captures); every other clause (located quotes, per-platform attribution, executable `source-recheck.py` recheck, re-ground on a lane F-id) **unmet**; `txt:N` quotes 0, recheck prose, `ground: F09` ≠ lane F09. Nothing new cleared. **Refuse.**
2. **claim-packaging-and-report-quality** — Register/capture S034/S035/**S036**: 2 of 3 met since r33; S036 BILISRC 0 rows, 0 captures. Nothing new cleared. **Refuse.**
3. **cn-crowdsourced-testing-roles-and-conduct** — H1 absent (0); S081/S082 unregistered and uncaptured; no page/line quotes. Nothing cleared. **Refuse.**
4. **chinese-crowd-testing-national-standard-2026-10-23** — S077/S078/S079 unregistered/uncaptured; `ground: F24` is not a lane id (next lane id after S052/F18 admission is F19, not F24); 0 located quotes. Nothing cleared. **Refuse.**
5. **chinese-criminal-thresholds-and-authorisation** — three PRC sources unregistered; staged ids S044–S046 occupied by lane Bugcrowd/IPA rows (collision persists and grows only by S052); body also cites staged S034 which in the lane is 総務省, while the document it means is lane S049. Nothing cleared. **Refuse.**
6. **chinese-program-severity-instrument** — S047 sse.com.cn unregistered; `newsType_6` → 0 in `corpus/source-snapshots/round-32/S049.txt` (sha256 `962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8`, unchanged), `newsType_21` → 1. Nothing cleared. **Refuse as an entry**; S049-verified facts remain reusable with locators only.
7. **program-severity-ladders-and-reward-scales** — Overwrite hazard persists (lane `6c05c98f…` vs staged `35de5f8b…`); not a flip. **Refuse / do-not-copy.**

### 5. Reading notes for the L1 (no action taken)

- Round-35 gate wording that holds: "No staged entry's flip set is fully met; no prior refusal lifted; no new refusal opened." The count of refusals stays **7 standing** (plus the quarantine slice, not my item).
- S052 landing will turn the round-34 line `collisions=21 … S031..S051` into `collisions=22 … S031..S052`; the committed round-35 `assimilation/collisions` (21 lines) is a pre-S052 derivation until the L1 re-derives, matching the round-34 pre/post-S051 pattern.
- Round-34 lesson Gate text "frontier is F01–F17" in the national-standard row becomes "F01–F18" once F18 lands; `ground: F24` stays non-lane either way.
- Package/lesson inconsistency not caused by me: none found this round (digests in `corpus/lessons/round-34.md:145-151` equal the live bytes).

### 6. Commands run (all read-only)

- `sha256sum`, `stat -c '%y %n'`, `find $P -type f -newer .ufo/waves/round-34/claims.json`, `ls` on package and lane directories.
- python3 (`/fast/scratch/hyaku/kasegi-r35/ScoutPackageThemes/a.py`, deleted): registry/staged row derivation, URL join, per-entry measures → output in §2–§3 (exit 0).
- `bash .ufo/waves/round-35/assimilation/collide-check.sh <copy of corpus/SOURCES.md> merge/kasegi/SOURCES.append.md wide` → `collisions=21`, exit 0; with simulated S052 row → `collisions=22`, exit 0 (copy only, in scratch, deleted).
- `grep -c` / `grep -rl` counts quoted above (all exit 0 or 1 as counts; 0-hit greps return 1 and are not failures).
- Disclosure: one `jj st` was run once to see lane state (it snapshots the working copy; no description, bookmark, commit or file content was changed by me). No `jj`/`git` command after that; no `git add/commit/push`.

## Report

Seat: ScoutPackageThemes (round 35, wave 1). Verdict: **Assimilation: none** — seven refused staged entries, zero flip conditions cleared, package byte-identical to round 34 (7 entry digests + SOURCES.append.md `4fe049cb…73eb`, MERGE-REPORT.json `8a42a910…bf5b`, register `5afe1810…d833`), lane registry 51 rows at read time (S052 pending, capture present), S036 / S044–S047 / S077–S079 / S081–S082 still in no lane row or capture, 21 collisions today and 22 (S031..S052) after S052 lands (staged S052 = a CNNVD weekly, a different document from lane S052 CISA KEV; cited by none of the seven), CISA/KEV strings absent from the package (0 files). Unresolved: none. Scratch: created `/fast/scratch/hyaku/kasegi-r35/ScoutPackageThemes/`, deleted before yield (see checks below). Writes: this file only.
