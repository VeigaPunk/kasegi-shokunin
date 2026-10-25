# ConnStagedCensus — Census of Staged Package vs Lane Registry by Document

- **Seat**: `ConnStagedCensus-2` (UFO-FSD connector, leaf member; no subagent dispatch, write-scoped to Report path)
- **Round**: kasegi-shokunin round 29, wave 1 (dispatched by L1 via inline spawn handoff, hyaku run 7)
- **Timestamp (UTC)**: 2026-10-25T19:05:00Z
- **Lane Root**: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- **Lane Base Revision**: `7a6591c1eb8a14f427297980a96fa8bb339f29ee`
- **Claims-Freeze Commit**: `f28ff5d26b29270f93163117e7255e24f0b1d947`
- **Staged Package Source (READ-ONLY)**: `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`
- **Lane Registry Source**: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`
- **Judged on**: `depth:verifiability`, `coverage` (milestone round-29)

---

## 1. Executive Summary & Verification of the Four Questions

An exhaustive document-level census was executed joining all 94 staged rows in `shokuknow/merge/kasegi/SOURCES.append.md` (IDs `S031`–`S124`) against the lane registry `corpus/SOURCES.md` using the canonical URL extraction and normalization algorithm (`url_of` from `scripts/sources-census.sh`: stripping fragment, trailing slash, protocol scheme, and lowercasing host).

### (1) Staged rows already lane rows under DIFFERENT IDs
- **Freeze Base (`7a6591c1`, 42 rows `S001`–`S042`)**: Exactly **12 staged rows** match documents already registered in the lane under different IDs:
  1. `S039` == Lane `S033` (`https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128` — e-Gov lawdata XML)
  2. `S040` == Lane `S034` (`https://www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/` — MIC citizen page)
  3. `S041` == Lane `S035` (`https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf` — NPA commentary PDF)
  4. `S043` == Lane `S041` (`https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` — JPCERT/CC 2026 P-guideline)
  5. `S055` == Lane `S036` (`https://cybozu.co.jp/company/security-policy/` — Cybozu vulnerability handling policy)
  6. `S056` == Lane `S037` (`https://cybozu.co.jp/products/bug-bounty/faq/` — Cybozu bounty FAQ)
  7. `S057` == Lane `S038` (`https://pepabo.com/contact/vulnerability-reporting/` — GMO Pepabo reporting policy)
  8. `S060` == Lane `S039` (`https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html` — Hitachi HIRT process)
  9. `S064` == Lane `S041` (`https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` — JPCERT/CC 2026 P-guideline 付録6 §4)
  10. `S068` == Lane `S040` (`https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` — Cisco policy)
  11. `S076` == Lane `S041` (`https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` — JPCERT/CC 2026 P-guideline 付録6 §2)
  12. `S123` == Lane `S032` (`https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf` — NIST SP 800-115)
- **Post-C2 Landing (`7a6591c1` + C2 append, 45 rows `S001`–`S045`)**: Exactly **15 staged rows** match under different IDs, adding the 3 adopted rows:
  13. `S031` == Lane `S043` (`https://hackerone.com/security/policy_versions`)
  14. `S032` == Lane `S044` (`https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md`)
  15. `S033` == Lane `S045` (`https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json`)
- **Key Document Collapse Phenomenon**: Three distinct staged rows (`S043`, `S064`, `S076`) cite the exact same underlying PDF (`partnership_guideline2026.pdf`) at different sections. All three collapse onto single Lane row `S041`.

### (2) Staged rows genuinely absent from the lane registry
- **Freeze Base**: Exactly **81 staged rows** are genuinely absent from the lane registry (`id_lane = none`).
- **Post-C2 Landing**: Exactly **78 staged rows** are genuinely absent (`id_lane = none`), after `S031`, `S032`, and `S033` are appended.
- **Verification Identity (Freeze Base)**:
  $$\text{Total Staged (94)} = 12\text{ (diff ID)} + 1\text{ (same ID S042)} + 81\text{ (genuinely absent)} = 94$$
- **Verification Identity (Post-C2)**:
  $$\text{Total Staged (94)} = 15\text{ (diff ID)} + 1\text{ (same ID S042)} + 78\text{ (genuinely absent)} = 94$$

### (3) Verification of Staged S031/S032/S033 and Free IDs S043/S044/S045
- **Absence by URL**:
  - `S031` (`https://hackerone.com/security/policy_versions`): Canonical `hackerone.com/security/policy_versions`. Present in freeze base? **False** (`id_lane = none`).
  - `S032` (`https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md`): Canonical `raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md`. Present in freeze base? **False** (`id_lane = none`).
  - `S033` (`https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json`): Canonical `raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json`. Present in freeze base? **False** (`id_lane = none`).
- **Free ID Slots**:
  - At freeze base `7a6591c1`, `corpus/SOURCES.md` terminated at row `S042` (42 rows total).
  - Check command: `grep -cE '^[[:space:]]*\|[[:space:]]*S04[3-5][[:space:]]*\|' corpus/SOURCES.md` -> **0**.
  - All three slots `S043`, `S044`, and `S045` were verified completely unassigned and free.
- **Clean Adoption Map for F13**:
  - Staged `S031` -> Lane `S043`
  - Staged `S032` -> Lane `S044`
  - Staged `S033` -> Lane `S045`
- **Zero Duplicate Risk**: Because `S031`–`S033` are absent from `corpus/SOURCES.md` by URL, appending them under `S043`–`S045` introduces zero duplicate URLs (`sources-census.sh validate` exits 0 with no new `W04` or `E04` warnings/errors).

### (4) Verification of the r28 Lesson's Claim that Staged S042 == Lane S041 by URL
- **Literal Verification**:
  - Staged `S042` URL: `https://www.ipa.go.jp/security/todokede/vuln/process.html` (IPA intake process page)
  - Lane `S041` URL: `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` (JPCERT/CC partnership guideline 2026 PDF)
  - URL Equality Check:
    $$\text{URL}(\text{Staged S042}) \neq \text{URL}(\text{Lane S041})$$
  - **Verdict on Literal Claim**: **FALSE**. Staged `S042` does NOT equal Lane `S041` by URL. They are completely different documents from different publishers (`ipa.go.jp` vs `jpcert.or.jp`).
- **Disproof & Reconciliation with Actual Round-28 Lesson Evidence**:
  - Inspection of `corpus/lessons/round-28.md` reveals that the lesson never claimed staged `S042` == lane `S041`.
  - Line 104 & Line 362 of `round-28.md` explicitly state:
    > *"staged S043 is the already-registered lane S041"* (both point to `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf`).
  - Lines 103, 114, and 203 of `round-28.md` state:
    > *"staged S042 (IPA process page URL) -> lane S042 (free at adoption; no lane row carried that URL)"* -> admitted as new row **Lane `S042`**.
  - Therefore, in the current round-29 freeze base, staged `S042` corresponds to **Lane `S042`** under the **SAME ID** (`id_staged = S042`, `id_lane = S042`), while staged `S043` corresponds to **Lane `S041`**.
  - **Contradiction Stated Explicitly**: The prompt item carries an off-by-one ID transposition in stating "staged S042 == lane S041". Staged `S043` is what equals Lane `S041`; staged `S042` equals Lane `S042`.

---

## 2. Non-Obvious Move (UFO-FSD Connector Synthesis)

### Evidence
1. **Recurring Adoption Friction**: Across rounds 27, 28, and 29, 2 to 4 seats per wave (`ConnStagedCensus`, `ScoutAssimilation`, `ScribeSourcesGate`, `ScribeAssimReport`) spend significant cycles re-running ad-hoc awk/grep pipelines to map staged IDs onto lane IDs and prevent collision.
2. **Grammar Latent Trap**: As discovered in round 28 (`ScoutAssimilation.txt:51-53`) and confirmed here, **43 of the 94 staged rows (`S081`–`S124`)** have prose text in their `recheck` column (e.g. `90d — re-open the ... still present`). If any future round blindly copies rows from `SOURCES.append.md`, it immediately fails `sources-census.sh validate` with `E09`.
3. **URL Collapse Trap**: Three distinct staged rows (`S043`, `S064`, `S076`) point to the same URL (`partnership_guideline2026.pdf`). Blindly adopting staged rows would trigger `W04` / `E04` duplicate URL errors.
4. **Human Transposition Drift**: The prompt's own mistaken premise ("staged S042 == lane S041") proves that manual cross-registry tracking is vulnerable to subtle ID-slip errors.
5. **Proposal Synthesis**: `considerthese/2026-10-25.md` proposal 5 advocates for *"an open-defects ledger with runnable closure checks"*, while proposal 1 urges *"capping wave-evidence bloat"*.

### Affected Axes
- `depth:verifiability` (**Improves**): Converts an ad-hoc, multi-seat human investigation into an immutable, machine-executable pre-flight verification oracle.
- `coverage` (**Improves**): Guarantees safe frontier expansion without risking duplicate URL errors (`W04`/`E04`) or schema violations (`E09`).
- `depth:density` (**Neutral / No-Harm**): Incurs zero bloat in `SKILL.md` or knowledge entry prose.

### Proposed Move
Formulate an automated **Staged Adoption Pre-flight Validator** mode in `scripts/sources-census.sh` (or a hermetic instrument `corpus/instruments/staged-census.py`):
```bash
scripts/sources-census.sh check-staged \
  --staged /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md \
  --registry corpus/SOURCES.md \
  --adopt S031,S032,S033
```
The validator automatically executes:
1. Canonical URL join (`url_of`) between staged rows and lane registry.
2. Asserts that the target staged rows are absent by URL from the lane registry (`id_lane = none`).
3. Discovers and reports the next available unassigned lane ID slots (e.g., `S043`–`S045`).
4. Enforces `SOURCES-CONTRACT-v1` grammar on the candidate rows (11 columns `NF=13`, valid tier/kind, and crucially non-prose ISO/NNn `recheck` cadence, failing immediately on `E09` prose).
5. Emits the machine-readable mapping table (`id_staged -> id_lane`).

### Second-Order Effects
- **Runtime Surface**: Replaces 3-4 separate scout/scribe seats with a single command run during wave pre-flight, drastically cutting seat concurrency pressure.
- **Contract Surface**: Hardens `QUALITY.md` R8 and `SOURCES-CONTRACT-v1` before any entry files are written.
- **Substrate Surface**: Strictly read-only against `SOURCES.append.md` and `SOURCES.md`; no index or git mutations.
- **Verification Surface**: Provides deterministic JSON/stdout proof matching C2 kill-rules.

### Risks & Mitigations
- **Risk**: False sense of security if a seat assumes URL validation also checks quote assertions.
  - **Mitigation**: The validator outputs metadata assertions only; quote pinning remains strictly gated by `corpus/instruments/source-recheck.py`.
- **Risk**: Tool breakage if `SOURCES.append.md` path is missing or inaccessible.
  - **Mitigation**: Fail-closed semantics with exit code 2 if `--staged` file cannot be read.

### Verification
A standalone verification script executing this logic against `SOURCES.append.md` and `corpus/SOURCES.md` produces 0 collisions for `S031`–`S033`, flags the 12 existing cross-ID matches, catches the prose recheck on `S081`–`S124`, and exits 0 only when the adoption batch is sound.

---

## 3. Full 94-Row Join Table (id_staged, url, id_lane|none)

The table below enumerates all 94 staged rows from `shokuknow/merge/kasegi/SOURCES.append.md`:
- `id_staged`: The row ID in the staged package.
- `canonical_locator`: The canonical URL or local probe log path.
- `id_lane (freeze base)`: Matching lane ID at round-29 freeze base (`7a6591c1`, 42 rows `S001`–`S042`), or `none`.
- `id_lane (post-C2)`: Matching lane ID in the landed post-C2 tree (45 rows `S001`–`S045`), or `none`.
- `status / note`: Detailed classification and adoption status.

| id_staged | canonical_locator (url / path) | id_lane (freeze base) | id_lane (post-C2) | status / note |
|---|---|---|---|---|
| S031 | `https://hackerone.com/security/policy_versions` | none | S043 | Round-29 F13 target: absent at freeze base; adopted as lane S043 |
| S032 | `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md` | none | S044 | Round-29 F13 target: absent at freeze base; adopted as lane S044 |
| S033 | `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json` | none | S045 | Round-29 F13 target: absent at freeze base; adopted as lane S045 |
| S034 | `https://zc.cnvd.org.cn/news/helpList` | none | none | Genuinely absent from lane registry |
| S035 | `https://security.360.cn/Reward/rules` | none | none | Genuinely absent from lane registry |
| S036 | `https://security.bilibili.com/static/docs/BILISRC_V1.7.pdf` | none | none | Genuinely absent from lane registry |
| S037 | `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A` | none | none | Genuinely absent from lane registry |
| S038 | `https://std.samr.gov.cn/gb/search/gbDetailed?id=B4C25880C3E01CB3E05397BE0A0A92D0` | none | none | Genuinely absent from lane registry |
| S039 | `https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128` | S033 | S033 | Already registered in lane under different ID (S033) |
| S040 | `https://www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/` | S034 | S034 | Already registered in lane under different ID (S034) |
| S041 | `https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf` | S035 | S035 | Already registered in lane under different ID (S035) |
| S042 | `https://www.ipa.go.jp/security/todokede/vuln/process.html` | S042 | S042 | Same-id document match with lane S042 (admitted in round 28) |
| S043 | `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` | S041 | S041 | Already registered in lane under different ID (S041) |
| S044 | `https://www.court.gov.cn/fabu/xiangqing/3085.html` | none | none | Genuinely absent from lane registry |
| S045 | `https://czt.ln.gov.cn/czt/attachDir/2026/05/2026050715041524122.pdf` | none | none | Genuinely absent from lane registry |
| S046 | `https://nj.jsjc.gov.cn/jianwu/zhinan/202109/t20210917_238200.shtml` | none | none | Genuinely absent from lane registry |
| S047 | `https://www.sse.com.cn/lawandrules/regulations/csrcannoun/c/10117011/files/028395e1b8364d3bb3fcb28d565de306.pdf` | none | none | Genuinely absent from lane registry |
| S048 | `https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3` | none | none | Genuinely absent from lane registry |
| S049 | `https://www.ipa.go.jp/security/reports/vuln/jvn/ug65p90000019ev2-att/000095610.pdf` | none | none | Genuinely absent from lane registry |
| S050 | `https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html` | none | none | Genuinely absent from lane registry |
| S051 | `http://gongbao.court.gov.cn/Details/96fea4e0b9e00def2295a1e598666f.html` | none | none | Genuinely absent from lane registry |
| S052 | `https://www.cnnvd.org.cn/group1/M00/03/2C/rBBl8WrPKoaAKy_IAAT1JLp2GFY923.pdf` | none | none | Genuinely absent from lane registry |
| S053 | `https://www.meti.go.jp/policy/netsecurity/vul_notification.pdf` | none | none | Genuinely absent from lane registry |
| S054 | `https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf` | none | none | Genuinely absent from lane registry |
| S055 | `https://cybozu.co.jp/company/security-policy/` | S036 | S036 | Already registered in lane under different ID (S036) |
| S056 | `https://cybozu.co.jp/products/bug-bounty/faq/` | S037 | S037 | Already registered in lane under different ID (S037) |
| S057 | `https://pepabo.com/contact/vulnerability-reporting/` | S038 | S038 | Already registered in lane under different ID (S038) |
| S058 | `https://www.ipa.go.jp/security/todokede/vuln/uketsuke.html` | none | none | Genuinely absent from lane registry |
| S059 | `http://www.phic.org.cn/wsxxh/wzaqgl/202609/P020260909380470895113.pdf` | none | none | Genuinely absent from lane registry |
| S060 | `https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html` | S039 | S039 | Already registered in lane under different ID (S039) |
| S061 | `https://www.court.gov.cn/fabu/xiangqing/283891.html` | none | none | Genuinely absent from lane registry |
| S062 | `https://www.court.gov.cn/zixun/xiangqing/449641.html` | none | none | Genuinely absent from lane registry |
| S063 | `http://gongbao.court.gov.cn/Details/4aa50f7ee90ae17896de6699f8fbf3.html` | none | none | Genuinely absent from lane registry |
| S064 | `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` | S041 | S041 | Already registered in lane under different ID (S041) |
| S065 | `http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf` | none | none | Genuinely absent from lane registry |
| S066 | `https://www.microsoft.com/en-us/msrc/bounty-guidelines` | none | none | Genuinely absent from lane registry |
| S067 | `https://www.microsoft.com/en-us/msrc/pentest-rules-of-engagement` | none | none | Genuinely absent from lane registry |
| S068 | `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` | S040 | S040 | Already registered in lane under different ID (S040) |
| S069 | `https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F20_WD_2025005470_%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF%20%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%BC%8F%E6%B4%9E%E5%88%86%E7%B1%BB%E5%88%86%E7%BA%A7%E6%8C%87%E5%8D%97.pdf` | none | none | Genuinely absent from lane registry |
| S070 | `https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F20_DI_2025005470_%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF%20%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%BC%8F%E6%B4%9E%E5%88%86%E7%B1%BB%E5%88%86%E7%BA%A7%E6%8C%87%E5%8D%97.pdf` | none | none | Genuinely absent from lane registry |
| S071 | `https://www.cert.org.cn/publish/main/9/2026/20261022162132536309183/20261022162132536309183_.html` | none | none | Genuinely absent from lane registry |
| S072 | `GB/T 30279—202X 征求意见稿 附录A／附录B／附录C 逐行转录（lane 自身工件） — lanes/kasegi/round5/evidence/gb30279-202x-annexes-transcription.txt` | none | none | Own-work / local probe log (own-work), absent from lane |
| S073 | `http://gongbao.court.gov.cn/Details/fd33e76142bf3ada6cabe0b81dc6d9.html` | none | none | Genuinely absent from lane registry |
| S074 | `https://www.court.gov.cn/zixun/xiangqing/137141.html` | none | none | Genuinely absent from lane registry |
| S075 | `https://jtgl.beijing.gov.cn/jgj/jgxx/flfg/fl/11033925/index.html` | none | none | Genuinely absent from lane registry |
| S076 | `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` | S041 | S041 | Already registered in lane under different ID (S041) |
| S077 | `https://std.sacinfo.org.cn/gnoc/queryInfo?id=E8261DDA41842E54E073557BFF2F9E7B` | none | none | Genuinely absent from lane registry |
| S078 | `https://www.sac.gov.cn/xw/bzhdt/art/2024/art_f1892c53ae3e4317b5e9aea08b6a72fc.html` | none | none | Genuinely absent from lane registry |
| S079 | `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=57CAF3B46207A7D43649E9BE15AEA0C0` | none | none | Genuinely absent from lane registry |
| S080 | `https://www.microsoft.com/en-us/msrc/msvr` | none | none | Genuinely absent from lane registry |
| S081 | `https://zc.cnvd.org.cn/news/info?id=133&newsTypeCode=100100` | none | none | Genuinely absent from lane registry |
| S082 | `https://std.samr.gov.cn/gb/search/gbDetailed?id=D0FE299A5DFDD818E05397BE0A0AFD6C` | none | none | Genuinely absent from lane registry |
| S083 | `http://web.archive.org/web/20261007213108id_/https://jvndb.jvn.jp/en/nav/jvndbhelp.html` | none | none | Genuinely absent from lane registry |
| S084 | `http://www.npc.gov.cn/zgrdw/huiyi/lfzt/xfq/2008-08/21/content_1445185.htm` | none | none | Genuinely absent from lane registry |
| S085 | `http://kass.sacinfo.org.cn/kfs/token/download/dhppvhmmtuuwkehg` | none | none | Genuinely absent from lane registry |
| S086 | `http://kass.sacinfo.org.cn/kfs/token/download/udghvosaqozjdqze` | none | none | Genuinely absent from lane registry |
| S087 | `https://www.cert.org.cn/publish/main/upload/File/CNVD202518.pdf` | none | none | Genuinely absent from lane registry |
| S088 | `http://web.archive.org/web/20190405221136id_/http://www.spp.gov.cn/llyj/201704/t20170425_188911.shtml` | none | none | Genuinely absent from lane registry |
| S089 | `https://www.sse.com.cn/lawandrules/regulations/csrcannoun/c/10117011/files/028395e1b8364d3bb3fcb28d565de306.pdf` | none | none | Genuinely absent from lane registry |
| S090 | `http://kass.sacinfo.org.cn/kfs/token/download/udghvosaqozjdqze` | none | none | Genuinely absent from lane registry |
| S091 | `https://std.samr.gov.cn/gb/search/gbDetailed?id=4C30E22D8B94BBB9E06397BE0A0A52F3` | none | none | Genuinely absent from lane registry |
| S092 | `https://html.rhhz.net/ZGKXYDXXB/1684805024215-1210753055.htm` | none | none | Genuinely absent from lane registry |
| S093 | `https://www.cert.org.cn/publish/main/upload/File/Weekly%20Report%20of%20CNCERT-Issue%2042%202026%20CH.pdf` | none | none | Genuinely absent from lane registry |
| S094 | `https://www.bjjc.gov.cn/c/yify/sdjc/321464528.jhtml` | none | none | Genuinely absent from lane registry |
| S095 | `http://web.archive.org/web/20251202112018/https://www.spp.gov.cn/zdgz/202507/t20250715_701316.shtml` | none | none | Genuinely absent from lane registry |
| S096 | `https://std.samr.gov.cn/gb/search/gbDetailedCNF?id=7236A1438F85571FE05397BE0A0A1552` | none | none | Genuinely absent from lane registry |
| S097 | `https://www.cert.org.cn/publish/english/upload/File/Weekly%20Report%20of%20CNCERT-Issue%202%202026%20EN.pdf` | none | none | Genuinely absent from lane registry |
| S098 | `https://www.055110.com/xs/1/25120.html` | none | none | Genuinely absent from lane registry |
| S099 | `https://raw.githubusercontent.com/y4ney/collect-cnnvd-vuln/main/doc/pdf/CNNVD%E6%BC%8F%E6%B4%9E%E5%88%86%E7%BA%A7%E8%A7%84%E8%8C%83.pdf` | none | none | Genuinely absent from lane registry |
| S100 | `https://chinastandards.org/standards/gb-t-30279-2020` | none | none | Genuinely absent from lane registry |
| S101 | `https://www.cnnvd.org.cn/cnnvdweb/2.0/common/docProtocol/selectDocProtocolByKeyId?keyId=specification` | none | none | Genuinely absent from lane registry |
| S102 | `https://down.waizi.org.cn/gb/5224.html` | none | none | Genuinely absent from lane registry |
| S103 | `http://www.phic.org.cn/wsxxh/wzaqgl/index.html` | none | none | Genuinely absent from lane registry |
| S104 | `http://iolaw.cssn.cn/fxyjdt/201709/t20170928_4653108.shtml` | none | none | Genuinely absent from lane registry |
| S105 | `http://iolaw.cssn.cn/fxyjdt/201709/t20170928_4653108.shtml` | none | none | Genuinely absent from lane registry |
| S106 | `https://std.samr.gov.cn/gb/search/gbAdvancedSearchPage?tid=1&std_p5=20190906-T-469` | none | none | Genuinely absent from lane registry |
| S107 | `https://std.samr.gov.cn/gb/search/gbAdvancedSearchPage?tid=1&std_p5=20260806-T-469` | none | none | Genuinely absent from lane registry |
| S108 | `https://wenshu.court.gov.cn/` | none | none | Genuinely absent from lane registry |
| S109 | `GB/T 30279-2020 征求意见稿（the 2020 edition's own draft） — lane text rendering of the platform's file: /home/vgpnk/Projects/shokuknow/lanes/kasegi/round13/evidence/std2020_wd.txt` | none | none | Own-work / local probe log (own-work), absent from lane |
| S110 | `CNNVD 规范文档 service: the lane's own host-state probe log — /home/vgpnk/Projects/shokuknow/lanes/kasegi/round13/evidence/cnnvd_host_probe.txt` | none | none | Own-work / local probe log (own-work), absent from lane |
| S111 | `https://www.cert.org.cn/publish/main/44/2026/20261022160534684656514/20261022160534684656514_.html` | none | none | Genuinely absent from lane registry |
| S112 | `TC260's own suggestion route and the standards platform's project record: the lane's own route probe log — /home/vgpnk/Projects/shokuknow/lanes/kasegi/round13/evidence/cn_tc260_plan_routes_probe.txt` | none | none | Own-work / local probe log (own-work), absent from lane |
| S113 | `Chinese court-data routes for an authorised-tester acquittal: the lane's own route probe log — /home/vgpnk/Projects/shokuknow/lanes/kasegi/round13/evidence/cn_court_routes_probe.txt` | none | none | Own-work / local probe log (own-work), absent from lane |
| S114 | `GB/T 30279-2020 征求意见稿 — the platform's own 2020-edition draft, rendered to greppable text by LibreOffice: /home/vgpnk/Projects/shokuknow/lanes/kasegi/round14/evidence/std2020_lo.txt` | none | none | Own-work / local probe log (own-work), absent from lane |
| S115 | `CNNVD's own host and its own API base — the lane's own host-shape probe log: /home/vgpnk/Projects/shokuknow/lanes/kasegi/round14/evidence/cnnvd_spec_probe.txt` | none | none | Own-work / local probe log (own-work), absent from lane |
| S116 | `人民法院案例库 — the library's own route probe log, carrying two sentences quoted verbatim from the library's own 使用帮助 page: /home/vgpnk/Projects/shokuknow/lanes/kasegi/round14/evidence/rmfyalk_case_library_probe.txt` | none | none | Own-work / local probe log (own-work), absent from lane |
| S117 | `The canonical host's own attachment path and its file-name families — the lane's own family probe log: /home/vgpnk/Projects/shokuknow/lanes/kasegi/round14/evidence/cert_upload_family_probe.txt` | none | none | Own-work / local probe log (own-work), absent from lane |
| S118 | `全国网络安全标准化技术委员会's own suggestion route — the lane's own shell probe log: /home/vgpnk/Projects/shokuknow/lanes/kasegi/round14/evidence/tc260_shell_probe.txt` | none | none | Own-work / local probe log (own-work), absent from lane |
| S119 | `http://kass.sacinfo.org.cn/kfs/token/download/jefrgyuuyqlbwkif` | none | none | Genuinely absent from lane registry |
| S120 | `人民法院案例库's own request-shape map — the lane's own probe log: /home/vgpnk/Projects/shokuknow/lanes/kasegi/round15/evidence/rmfyalk_request_shape_probe.txt` | none | none | Own-work / local probe log (own-work), absent from lane |
| S121 | `全国标准信息公共服务平台's attachment-existence probe — the lane's own probe log: round16/evidence/platform_attachment_existence_probe.txt` | none | none | Own-work / local probe log (own-work), absent from lane |
| S122 | `多元解纷案例库's API-base probe — the lane's own probe log: round16/evidence/dyjfalk_api_base_probe.txt` | none | none | Own-work / local probe log (own-work), absent from lane |
| S123 | `https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf` | S032 | S032 | Already registered in lane under different ID (S032) |
| S124 | `https://std.samr.gov.cn/gb/search/gbDetailed?id=B4C25880C3E91CB3E05397BE0A0A92D0` | none | none | Genuinely absent from lane registry |

---

## 4. Verification Checksums & Traceability

```
=== CENSUS SUMMARY METRICS ===
Total Staged Rows in Package: 94 (S031–S124)
Lane Rows at Claims Freeze Base: 42 (S001–S042)
Lane Rows Post-C2 Landing: 45 (S001–S045)

[Freeze Base 7a6591c1]
- Matching Lane under Different ID: 12
- Matching Lane under Same ID (S042): 1
- Genuinely Absent from Lane Registry: 81
- Sum: 12 + 1 + 81 = 94 (Consistent)

[Post-C2 Landing]
- Matching Lane under Different ID: 15 (12 base + S031->S043, S032->S044, S033->S045)
- Matching Lane under Same ID (S042): 1
- Genuinely Absent from Lane Registry: 78
- Sum: 15 + 1 + 78 = 94 (Consistent)

[Target Adoption Verification]
- Staged S031 (hackerone.com/security/policy_versions): Absent at base -> Adopted as Lane S043
- Staged S032 (raw.githubusercontent.com/.../README.md): Absent at base -> Adopted as Lane S044
- Staged S033 (raw.githubusercontent.com/.../cwe.json): Absent at base -> Adopted as Lane S045
- Free IDs S043, S044, S045: Verified unassigned at base (0 collisions)

[r28 Claim Verification & Contradiction Resolution]
- Staged S042 URL: https://www.ipa.go.jp/security/todokede/vuln/process.html
- Lane S041 URL: https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf
- Literal Claim (Staged S042 == Lane S041): FALSE (different documents)
- Actual Lesson Fact: Staged S043 == Lane S041 (cited not re-registered); Staged S042 == Lane S042 (admitted r28)
```

- **Seat Bounds**: Leaf role strictly observed. Zero subagents dispatched. Zero background jobs executed. Zero mutations outside the assigned `Report:` path.
- **Tooling Authorization**: No package installs or updates required. Pacman paused per host directive.
- **Model**: google-antigravity/gemini-3.8-flash (via OMP harness route).
