# ScoutPackageThemes receipt — round 34 (package standing refusals re-confirmation)

Answering model: anthropic/claude-sonnet-5-5. Read-only on `/home/vgpnk/Projects/shokuknow/merge/kasegi/` and the shokuknow register; read-only on the lane except this file. No package tool run, no network call, no scratch tree created (nothing to delete), no git/jj command run. Baseline: `corpus/lessons/round-33.md` § Gate "Refused package candidates" and `.ufo/waves/round-33/wave1/ScoutPackageThemes.md`. Reads timestamped 2026-10-26T05:36:10Z–05:37Z.

## Verdict

**Assimilation: none.** No flip condition of any of the seven refused staged entries cleared this round. The package did not move (digests byte-identical to round 33), and the lane registry gained no row that a refused entry still needs. The only registry movement since the round-33 Gate is the lane's own C2 work (S051 Immunefi, capture present, registry row not yet appended at read time), which no staged entry cites (`grep -ci immunefi SOURCES.append.md` → 0).

| staged entry | round-34 verdict | any flip condition cleared? |
|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` | REFUSED (standing) | No. Registration half was already met in round 33 (staged S034/S035 = lane S049/S050 by URL, re-measured today); the other clauses are still unmet |
| `claim-packaging-and-report-quality.md` | REFUSED (standing) | No. S034/S035 → S049/S050 by document; **S036 BILISRC still in no lane row, no lane capture** |
| `cn-crowdsourced-testing-roles-and-conduct.md` | REFUSED (standing) | No. S081/S082 not registered or captured; still no H1 |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | REFUSED (standing) | No. S077/S078/S079 not registered or captured; `ground: F24` is not a lane F-id |
| `chinese-criminal-thresholds-and-authorisation.md` | REFUSED (standing) | No. staged S044/S045/S046 (court.gov.cn / czt.ln.gov.cn / jsjc.gov.cn) not registered or captured; wrong-by-number citations persist |
| `chinese-program-severity-instrument.md` | REFUSED as an entry | No. second source S047 (sse.com.cn) not registered; `ground: F10` is a different lane item |
| `program-severity-ladders-and-reward-scales.md` | REFUSED / do-not-copy | No. Same-name lane file still differs; S036 BILISRC half still unregistered |

## Evidence

### 1. Package unchanged (digests, `sha256sum`, 2026-10-26T05:36:10Z)

```
4fe049cb…e73eb  merge/kasegi/SOURCES.append.md                 (mtime 2026-10-24 23:33:20 -0300)
8a42a910…bf5b  merge/kasegi/MERGE-REPORT.json                   (full: 8a42a9109c8c95bc55e818f0ad97e7923cbfe5a9e7792c72c59b5aaa3aecbf5b)
5afe1810…ad833  corpus-expansion-1/absent-defect-register.md   (full: 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833; mtime 2026-10-24 08:37)
120d8cd5d50b703809a1c1030eb3b16564251e69a8208e4c90b500343d99abc8  program-scope-rules-and-asset-boundaries.md
6ad64d785f8f767bc0e86a4967b80bcc636b5939af4ac41b1138911978ec8dbc  claim-packaging-and-report-quality.md
a5302aaf0b9a1502c8711cd620cf0cb87cd9fea8db192269fae31619548fe813  cn-crowdsourced-testing-roles-and-conduct.md
6c15d94114248beb433eeb35aca116eb2ff4beaf7abfbc9d2b9957aeb56ef83f  chinese-crowd-testing-national-standard-2026-10-23.md
1660c00c16369d0a50870185607e0a8006ed573cc4ae69a696ce568e4e8a59ae  chinese-criminal-thresholds-and-authorisation.md
442e0f2bfb08bc2cbb8951f110e64424f82203636928429bc38f46f388c4257c  chinese-program-severity-instrument.md
35de5f8b19ed3b20beb3d41c347f4727d9fd2eefc8a23e53c64c6987b60bbc87  program-severity-ladders-and-reward-scales.md
```
(Full SOURCES.append.md digest `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb`; all seven staged entries decode as strict UTF-8, checked with `bytes.decode('utf-8')`.)

### 2. Lane registry now vs round 33; id collisions

`corpus/SOURCES.md` rows matching `^\s{0,3}\|\s*S\d+\s*\|` → **50** (S001–S050; round 33 base 48, +S049/S050). `grep -c 'S051' corpus/SOURCES.md` → 0 at read time (row pending; `corpus/source-snapshots/round-34/{S051.txt,manifest.json}` and `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` already exist in the working tree — in-flight C2 work, not mine).

Independent re-derivation (python3, 0–3-space row pattern, no use of the L1's files): `reg_ids 50 staged_ids 94 collisions 20 S031 S050`. The L1's `.ufo/waves/round-34/assimilation/{collisions,reg-ids,staged-ids}` equal my derivation exactly (`matches L1 collisions file: True`, `reg-ids file equal: True`, `staged-ids equal: True`); `guard-proof.txt` (indented row caught by the 0–3-space pattern only: 1 vs col-0-only 0) re-read. Collisions grew 18 → 20 (S049, S050 now lane ids; the staged S049/S050 are IPA JVN rows, a different document: staged S049 → lane S046, staged S050 → lane S047). Adopt-by-number remains unsafe; adopt by document only.

Staged-row URL join against lane `corpus/SOURCES.md` (staged → lane), the complete set of joins that exist today:
```
S031 hackerone policy_versions → S043      S032 bugcrowd VRT README → S044     S033 bugcrowd VRT cwe.json → S045
S034 zc.cnvd.org.cn/news/helpList → S049   S035 security.360.cn/Reward/rules → S050
S036 security.bilibili.com/…BILISRC_V1.7.pdf → []   (UNREGISTERED; grep -c -i 'bilibili|BILISRC' corpus/SOURCES.md → 0; no lane capture)
S044 court.gov.cn/fabu/xiangqing/3085.html → []     S045 czt.ln.gov.cn/…2026050715041524122.pdf → []   S046 nj.jsjc.gov.cn/…t20210917_238200.shtml → []
S047 sse.com.cn/…028395e1….pdf → []                 (JR/T 0276—2023)
S077 std.sacinfo.org.cn/gnoc/queryInfo?id=E8261DDA… → []   S078 sac.gov.cn/…art_f1892c53….html → []   S079 openstd.samr.gov.cn/…57CAF3B4… → []
S081 zc.cnvd.org.cn/news/info?id=133&newsTypeCode=100100 → []   S082 std.samr.gov.cn/gb/search/gbDetailed?id=D0FE299A… → []
```
Lane captures: `corpus/source-snapshots/` holds round-23…26, 28–32 and 34; a recursive grep for `BILISRC|security.bilibili|news/info?id=133|D0FE299A|E8261DDA|57CAF3B4|std.sacinfo|sac.gov.cn|court.gov.cn|czt.ln|jsjc.gov|sse.com.cn` over `corpus/` (excluding `corpus/lessons/`) and `.ufo/waves/round-34/` hits only `corpus/knowledge/program-severity-ladders-and-reward-scales.md` (its BILISRC/VRT history prose) and round-34 spec/claims files (the L1's own wording) — **no registry row, no snapshot, no manifest record** for any of those URLs.

### 3. Per-entry reasons (mechanical measures today)

Measures from one python3 pass over the staged files (`H1` = lines starting `# `; `ground_in_lane` = the F-id exists in `corpus/README.md`'s frontier table; "exec recheck" = a `source-recheck.py` token in the `recheck:` line):

| entry | lines | H1 | `ground:` | F-id in lane table | exec recheck | `source:` ids → lane by URL |
|---|---|---|---|---|---|---|
| program-scope-rules-and-asset-boundaries | 39 | 1 | F09 | yes, **different item** (lane F09 = authorisation outside the platform) | no (`curl -sSL …`, prose) | S031→S043, S034→S049, S035→S050 |
| claim-packaging-and-report-quality | 45 | 1 | F11 | yes, **different item** (lane F11 = ISO 29147/30111 meta) | no (`curl … && pdftotext …`) | S034→S049, S035→S050, **S036→none** |
| cn-crowdsourced-testing-roles-and-conduct | 45 | **0** | `round-6 ledger item 2` | not an F-id | no | S081→none, S082→none |
| chinese-crowd-testing-national-standard-2026-10-23 | 45 | 1 | F24 | **no** (lane frontier is F01–F16, F17 pending) | no | S077/S078/S079→none |
| chinese-criminal-thresholds-and-authorisation | 57 | 1 | F12 | yes, **different item** (lane F12 = Japanese disclosure workflow) | no | S044/S045/S046→none (staged ids collide with lane VRT/IPA rows); its prose also cites "S034", which in the lane is 総務省 (corpus/SOURCES.md:40) |
| chinese-program-severity-instrument | 41 | 1 | F10 | yes, **different item** (lane F10 = vendor disclosure policies) | no | S034→S049, **S047→none** |
| program-severity-ladders-and-reward-scales | 50 | 1 | F10 | yes, **different item** | no | S032→S044, S033→S045, S034→S049, **S036→none** |

(The same-name test `comm -12 <(ls package/knowledge/corpus/knowledge|LC_ALL=C sort) <(ls corpus/knowledge|LC_ALL=C sort)` → four names: `authorised-testing-rules-of-engagement.md`, `japanese-domestic-disclosure-workflow.md`, `japanese-severity-vocabulary-and-impact-model.md`, `program-severity-ladders-and-reward-scales.md`; lane `program-severity-ladders-and-reward-scales.md` sha256 `6c05c98f3c6851b560098b8f7c43350a951e487e8b34e2ff09831563aa8ff4a6`, 46 lines — differs from staged `35de5f8b…`.)

Per entry (flip condition → status today):

1. **program-scope-rules-and-asset-boundaries** (`120d8cd5…`). Flip: register+capture CNVD helpList and 360SRC rules (**met since round 33**, S049/S050 rows landed); reuse S043 (available); located quote per scope rule (**unmet**: staged entry has none); attribute each rule to its platform and drop the "one invariant" universal (**unmet**, text unchanged); executable `cd … source-recheck.py` line (**unmet**, prose `curl`); re-ground on a lane frontier (**unmet**: `ground: F09` names a different lane item and the 360SRC sentence still mixes §一 L69–71 scope with grading). No clause cleared this round. **Refuse.**
2. **claim-packaging-and-report-quality** (`6ad64d78…`). Flip: register/capture S034/S035/**S036** — 2 of 3 met since round 33; **S036 BILISRC V1.7 still has no lane row or capture** (0 greps), so the three-source registration is still incomplete; locators, platform attribution, falsifiable rule, rejected over-generalisation, re-ground (F11 is ISO meta in the lane) all unmet. **Refuse.**
3. **cn-crowdsourced-testing-roles-and-conduct** (`a5302aaf…`). Flip: add H1 (H1=0, unmet), register+capture S081/S082 (no row, no capture), re-quote with page/line + exactly-once counts, replace drafting-stage S082 scope sentence, `cd`-prefixed recheck. Nothing cleared; S049 does not carry the conduct code (round-33 counts of 0 for `您不得因为漏洞信息私自联系厂商`, `众测需求方`, `授权测试方` stand — I did not re-run them because the S049 capture is unchanged: `sha256 962a451a…1cb8` per round-33). **Refuse.**
4. **chinese-crowd-testing-national-standard-2026-10-23** (`6c15d941…`). Flip: register/capture S077/S078/S079 (0/3), quote roles-and-duties sentence with location, drop the reframing, add a rejected over-generalisation, ground on a real lane F-id (F24 does not exist; F17 is the next lane id and it is Immunefi). Nothing cleared. **Refuse.**
5. **chinese-criminal-thresholds-and-authorisation** (`1660c00c…`). Flip: register/capture the three PRC legal/court sources (0/3), bound the cross-instrument conclusion, located quotes, executable recheck. Nothing cleared; hazard persists (its "row S034" → lane 総務省, correct lane id by document would be S049). **Refuse.**
6. **chinese-program-severity-instrument** (`442e0f2b…`). Flip: register/capture S047 (sse.com.cn JR/T 0276—2023; 0 lane rows), fix anchors (`newsType_6` absent from the text capture), exec recheck, re-ground. S034-only half remains reusable as fact base with locators only (already restated in the lane F16 entry); not as staged bytes. **Refuse as an entry.**
7. **program-severity-ladders-and-reward-scales** (`35de5f8b…`). Flip: none by copy — a same-name lane file with different bytes exists (overwrite hazard persists, `comm -12` above). **Refuse / do-not-copy.** Precision note below.

### 4. Precision note for the L1 (candidate wording correction, not an entry flip)

The round-33 lesson table says the staged `program-severity-ladders-and-reward-scales.md` "VRT and BILISRC halves cite unregistered rows". The staged VRT rows S032/S033 are URL-equal to lane **S044/S045** (registered since round 30, cited by the lane F13 entry's own `source:` lines S043/S044/S045). Only the **BILISRC** half (staged S036) and any CNVD id are the unregistered/colliding part. The refusal stands (the overwrite hazard alone justifies it), but "VRT … unregistered rows" is true only *by staged number*, not by document. Same for the 18→20 collision count: by number, S049/S050 now collide as ids even though S034/S035 map to them by document.

### 5. Commands run (all read-only; exit 0)

- `sha256sum` of the 3 package files, register and the 7 staged entries; `stat -c '%y %n'` on SOURCES.append.md, MERGE-REPORT.json, register (mtimes 2026-10-24).
- python3 URL-join script: staged `SOURCES.append.md` rows (94) against `corpus/SOURCES.md` rows by raw-URL substring (output in § 2).
- python3 collision/measure script: `reg_ids 50 staged_ids 94 collisions 20 S031 S050`; the three L1 files compared equal; per-entry table in § 3.
- `grep -c -i 'bilibili\|BILISRC' corpus/SOURCES.md` → 0; `grep -c 'news/info?id=133\|D0FE299A\|E8261DDA\|57CAF3B4\|court.gov.cn\|sse.com.cn' corpus/SOURCES.md` → 0; `grep -ci immunefi SOURCES.append.md` → 0; `grep -c S051 corpus/SOURCES.md` → 0.
- `comm -12` same-name overwrite test → four names (§ 3).

## Report

Seat: ScoutPackageThemes (round 34, wave 1). Verdict: **Assimilation: none**. Seven refused staged entries, zero flip conditions cleared, package digests unchanged since round 33, lane registry 50 rows (S001–S050), S036 BILISRC / S047 / S044–S046 (PRC) / S077–S079 / S081–S082 still absent from rows and captures, 20 id collisions (S031–S050) independently re-derived and equal to the L1's `assimilation/collisions`, four same-name overwrite hazards unchanged, one wording precision note (§ 4). Scratch: none created. Writes: this file only.
