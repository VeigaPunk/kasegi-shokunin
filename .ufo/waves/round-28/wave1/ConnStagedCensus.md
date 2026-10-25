# ConnStagedCensus — Census of Staged Package vs Lane Registry by Document

- **Seat**: `ConnStagedCensus` (UFO-FSD connector, leaf; no subagent dispatch, read-only to production)
- **Round**: kasegi-shokunin round 28, wave 1
- **Timestamp (UTC)**: 2026-10-25T17:35:00Z
- **Lane Root**: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- **Lane Base Revision**: `c9f8b115a098c65356e4b3b6048af45a37ab8395` (claims freeze commit)
- **Staged Package Source (READ-ONLY)**: `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`
- **Lane Registry Source**: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`
- **Judged on**: `coverage` (milestone round-28)

---

## 1. Executive Summary & Findings

A complete, exhaustive document-level census was performed joining the 94 staged rows in `shokuknow/merge/kasegi/SOURCES.append.md` (IDs `S031`–`S124`) against the lane registry `corpus/SOURCES.md` by canonical document locator (URL / file path).

### Three Key Verification Questions:

1. **Staged rows already in lane under DIFFERENT IDs**:
   - **Exactly 12 staged rows** correspond to documents already registered in the lane under different IDs:
     - `S039` == Lane `S033` (`https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128` — e-Gov lawdata XML)
     - `S040` == Lane `S034` (`https://www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/` — MIC / Soumu citizen page)
     - `S041` == Lane `S035` (`https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf` — NPA commentary PDF)
     - `S043` == Lane `S041` (`https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` — JPCERT/CC 2026 P-guideline)
     - `S055` == Lane `S036` (`https://cybozu.co.jp/company/security-policy/` — Cybozu handling policy)
     - `S056` == Lane `S037` (`https://cybozu.co.jp/products/bug-bounty/faq/` — Cybozu bounty FAQ)
     - `S057` == Lane `S038` (`https://pepabo.com/contact/vulnerability-reporting/` — GMO Pepabo policy)
     - `S060` == Lane `S039` (`https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html` — Hitachi HIRT process)
     - `S064` == Lane `S041` (`https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` — JPCERT/CC 2026 P-guideline 付録6 §4)
     - `S068` == Lane `S040` (`https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` — Cisco policy)
     - `S076` == Lane `S041` (`https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` — JPCERT/CC 2026 P-guideline 付録6 §2)
     - `S123` == Lane `S032` (`https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf` — NIST SP 800-115)
   - *Key structural observation*: Three distinct staged rows (`S043`, `S064`, `S076`) all target the same underlying PDF (`partnership_guideline2026.pdf`), each focusing on different sections. All three collapse onto Lane `S041`.

2. **Genuinely absent staged rows**:
   - **Exactly 82 staged rows** were genuinely absent from the lane registry at the round-28 claims freeze base (`id_lane = none`).
   - Total verification: `12 (already present) + 82 (genuinely absent) = 94 (total staged rows)`.

3. **Verification of the Round-27 lesson claim regarding staged `S042`**:
   - **Claim VERIFIED**: The round-27 lesson (`corpus/lessons/round-27.md:19-20`) states: *"staged S042 (IPA process page, free in the lane registry) and S043 (= lane S041, registered round 26)"*.
   - At claims freeze, the lane registry ended at `S041`. The ID `S042` was completely unassigned in the lane.
   - By URL, `https://www.ipa.go.jp/security/todokede/vuln/process.html` was absent from all 41 lane registry rows (`id_lane = none`).
   - Hence, staged `S042` was genuinely free both by numeric slot and by document identity.
   - **Proof of exactly one row appended this round**:
     The admitted F12 entry `japanese-domestic-disclosure-workflow.md` cites two sources:
     - JPCERT/CC P-guideline: staged `S043` -> already present as Lane `S041` (no new row required).
     - IPA intake process page: staged `S042` -> genuinely absent from lane (appended as Lane `S042`).
     Therefore, round 28 appends **exactly one row** (`| S042 |`), advancing the lane registry count from 41 to 42 rows (`sources_rows: 41 -> 42`), with `sources-census.sh validate` maintaining `exit 0`.

---

## 2. Full 94-Row Join Table

The table below joins all 94 staged rows from `SOURCES.append.md` against `corpus/SOURCES.md`:
- `id_staged`: The ID assigned in the staged package.
- `canonical_locator`: The canonical URL (or relative/absolute path for `own-work` probe logs).
- `id_lane (freeze base)`: The matching lane row ID at claims freeze revision `c9f8b115a0` (41 rows, `S001`–`S041`), or `none`.
- `id_lane (post-C2)`: The matching lane row ID after the round-28 wave-1 C2 append of `S042` (42 rows, `S001`–`S042`).
- `status / note`: Relationship between staged and lane registries.

| id_staged | canonical_locator (url / path) | id_lane (freeze base) | id_lane (post-C2) | status / note |
|---|---|---|---|---|
| S031 | `https://hackerone.com/security/policy_versions` | none | none | Genuinely absent from lane registry |
| S032 | `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md` | none | none | Genuinely absent from lane registry |
| S033 | `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json` | none | none | Genuinely absent from lane registry |
| S034 | `https://zc.cnvd.org.cn/news/helpList` | none | none | Genuinely absent from lane registry |
| S035 | `https://security.360.cn/Reward/rules` | none | none | Genuinely absent from lane registry |
| S036 | `https://security.bilibili.com/static/docs/BILISRC_V1.7.pdf` | none | none | Genuinely absent from lane registry |
| S037 | `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A` | none | none | Genuinely absent from lane registry |
| S038 | `https://std.samr.gov.cn/gb/search/gbDetailed?id=B4C25880C3E01CB3E05397BE0A0A92D0` | none | none | Genuinely absent from lane registry |
| S039 | `https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128` | S033 | S033 | Already in lane under different id (S033) |
| S040 | `https://www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/` | S034 | S034 | Already in lane under different id (S034) |
| S041 | `https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf` | S035 | S035 | Already in lane under different id (S035) |
| S042 | `https://www.ipa.go.jp/security/todokede/vuln/process.html` | none | S042 | Round-28 C2 adopted entry (IPA intake process); free at freeze, appended as S042 |
| S043 | `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` | S041 | S041 | Already in lane under different id (S041) |
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
| S055 | `https://cybozu.co.jp/company/security-policy/` | S036 | S036 | Already in lane under different id (S036) |
| S056 | `https://cybozu.co.jp/products/bug-bounty/faq/` | S037 | S037 | Already in lane under different id (S037) |
| S057 | `https://pepabo.com/contact/vulnerability-reporting/` | S038 | S038 | Already in lane under different id (S038) |
| S058 | `https://www.ipa.go.jp/security/todokede/vuln/uketsuke.html` | none | none | Genuinely absent from lane registry |
| S059 | `http://www.phic.org.cn/wsxxh/wzaqgl/202609/P020260909380470895113.pdf` | none | none | Genuinely absent from lane registry |
| S060 | `https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html` | S039 | S039 | Already in lane under different id (S039) |
| S061 | `https://www.court.gov.cn/fabu/xiangqing/283891.html` | none | none | Genuinely absent from lane registry |
| S062 | `https://www.court.gov.cn/zixun/xiangqing/449641.html` | none | none | Genuinely absent from lane registry |
| S063 | `http://gongbao.court.gov.cn/Details/4aa50f7ee90ae17896de6699f8fbf3.html` | none | none | Genuinely absent from lane registry |
| S064 | `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` | S041 | S041 | Already in lane under different id (S041) |
| S065 | `http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf` | none | none | Genuinely absent from lane registry |
| S066 | `https://www.microsoft.com/en-us/msrc/bounty-guidelines` | none | none | Genuinely absent from lane registry |
| S067 | `https://www.microsoft.com/en-us/msrc/pentest-rules-of-engagement` | none | none | Genuinely absent from lane registry |
| S068 | `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` | S040 | S040 | Already in lane under different id (S040) |
| S069 | `https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F20_WD_2025005470_%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF%20%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%BC%8F%E6%B4%9E%E5%88%86%E7%B1%BB%E5%88%86%E7%BA%A7%E6%8C%87%E5%8D%97.pdf` | none | none | Genuinely absent from lane registry |
| S070 | `https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F20_DI_2025005470_%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF%20%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%BC%8F%E6%B4%9E%E5%88%86%E7%B1%BB%E5%88%86%E7%BA%A7%E6%8C%87%E5%8D%97.pdf` | none | none | Genuinely absent from lane registry |
| S071 | `https://www.cert.org.cn/publish/main/9/2026/20261022162132536309183/20261022162132536309183_.html` | none | none | Genuinely absent from lane registry |
| S072 | `lanes/kasegi/round5/evidence/gb30279-202x-annexes-transcription.txt` | none | none | Genuinely absent from lane registry |
| S073 | `http://gongbao.court.gov.cn/Details/fd33e76142bf3ada6cabe0b81dc6d9.html` | none | none | Genuinely absent from lane registry |
| S074 | `https://www.court.gov.cn/zixun/xiangqing/137141.html` | none | none | Genuinely absent from lane registry |
| S075 | `https://jtgl.beijing.gov.cn/jgj/jgxx/flfg/fl/11033925/index.html` | none | none | Genuinely absent from lane registry |
| S076 | `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` | S041 | S041 | Already in lane under different id (S041) |
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
| S109 | `/home/vgpnk/Projects/shokuknow/lanes/kasegi/round13/evidence/std2020_wd.txt` | none | none | Genuinely absent from lane registry |
| S110 | `/home/vgpnk/Projects/shokuknow/lanes/kasegi/round13/evidence/cnnvd_host_probe.txt` | none | none | Genuinely absent from lane registry |
| S111 | `https://www.cert.org.cn/publish/main/44/2026/20261022160534684656514/20261022160534684656514_.html` | none | none | Genuinely absent from lane registry |
| S112 | `/home/vgpnk/Projects/shokuknow/lanes/kasegi/round13/evidence/cn_tc260_plan_routes_probe.txt` | none | none | Genuinely absent from lane registry |
| S113 | `/home/vgpnk/Projects/shokuknow/lanes/kasegi/round13/evidence/cn_court_routes_probe.txt` | none | none | Genuinely absent from lane registry |
| S114 | `/home/vgpnk/Projects/shokuknow/lanes/kasegi/round14/evidence/std2020_lo.txt` | none | none | Genuinely absent from lane registry |
| S115 | `/home/vgpnk/Projects/shokuknow/lanes/kasegi/round14/evidence/cnnvd_spec_probe.txt` | none | none | Genuinely absent from lane registry |
| S116 | `/home/vgpnk/Projects/shokuknow/lanes/kasegi/round14/evidence/rmfyalk_case_library_probe.txt` | none | none | Genuinely absent from lane registry |
| S117 | `/home/vgpnk/Projects/shokuknow/lanes/kasegi/round14/evidence/cert_upload_family_probe.txt` | none | none | Genuinely absent from lane registry |
| S118 | `/home/vgpnk/Projects/shokuknow/lanes/kasegi/round14/evidence/tc260_shell_probe.txt` | none | none | Genuinely absent from lane registry |
| S119 | `http://kass.sacinfo.org.cn/kfs/token/download/jefrgyuuyqlbwkif` | none | none | Genuinely absent from lane registry |
| S120 | `/home/vgpnk/Projects/shokuknow/lanes/kasegi/round15/evidence/rmfyalk_request_shape_probe.txt` | none | none | Genuinely absent from lane registry |
| S121 | `round16/evidence/platform_attachment_existence_probe.txt` | none | none | Genuinely absent from lane registry |
| S122 | `round16/evidence/dyjfalk_api_base_probe.txt` | none | none | Genuinely absent from lane registry |
| S123 | `https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf` | S032 | S032 | Already in lane under different id (S032) |
| S124 | `https://std.samr.gov.cn/gb/search/gbDetailed?id=B4C25880C3E91CB3E05397BE0A0A92D0` | none | none | Genuinely absent from lane registry |

---

## 3. Structural Contradictions & Second-Order Effects

### Explicit Contradictions

1. **Package Directive vs. Lane Grammar (`MERGE-REPORT.md:102`)**:
   `MERGE-REPORT.md` instructs: *"3. Append `SOURCES.append.md` to `corpus/SOURCES.md`."*
   - *Contradiction*: Following this directive naively would inject 94 rows directly into `corpus/SOURCES.md`. Because the staged IDs run `S031`–`S124` and the lane registry already contains `S031`–`S041` (and now `S042`), an append would instantly create 11 (now 12) duplicate IDs (`S031`–`S042`), causing `sources-census.sh validate` to crash with fatal collision errors.
   - Furthermore, it would duplicate 12 existing documents under new IDs, violating the single-authority invariant.

2. **Scout Script False Assertion (`.ufo/waves/round-28/assimilation/by-document-map.txt:58-64`)**:
   The script recorded:
   ```text
   $ grep -oE 'https?://[^ |]+' corpus/SOURCES.md | sort | uniq -d
   https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq
   https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng
   https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html
   (empty above = no URL is registered twice in the lane registry)
   ```
   - *Contradiction*: The output was *not* empty; 3 URLs appeared twice. The script grepped the entire file including historical changelog notes and rejected rows (`S028` rejected duplicate of `S006`; `S024` superseded by `S029`; `S040` changelog mention). Within active table rows, URLs are unique, but raw document grep does not equal table-cell uniqueness.

3. **Multi-Row Staging of Single Documents**:
   `SOURCES.append.md` stages the JPCERT 2026 P-guideline three separate times (`S043`, `S064`, `S076`), splitting it by section anchor. The lane registry model registers the document once (`S041`) and accommodates multiple anchors across citing entries.

4. **The "Alignment Illusion" at S042**:
   Staged `S042` mapped to Lane `S042` purely by accidental numerical convergence (staged started at S031 against an old 30-row lane; lane independently added 11 rows `S031`–`S041`). For the remaining 81 absent rows, this alignment vanishes: staged `S043` is Lane `S041`, so the next absent row (`S044`) must be assigned to Lane `S043`.

### Second-Order Effects

- **Runtime Surface**: Any batch ingestion script that attempts to append rows without an automated renumbering and aliasing layer will corrupt `corpus/SOURCES.md` and trigger fatal census validation aborts.
- **Contract Surface**: Knowledge entries in `shokuknow/merge/kasegi/knowledge/*.md` cite staged IDs (e.g. `source: S043`). Adopting them requires mutating entry front-matter to reference lane canonical IDs (`source: S041`).
- **Substrate Surface**: Full duplication of source snapshots or re-registering already-held documents violates the R14 wave-evidence economy rule.

---

## 4. Bounded Proposed Move (Connector Synthesis)

### Proposed Move: Machine-Readable Assimilation Crosswalk & Front-Matter Rewriter

Establish a committed, machine-readable crosswalk table `corpus/instruments/staged-source-crosswalk.json` (or `.tsv`) derived directly from this 94-row census join table.

The crosswalk encodes two explicit maps:
1. **Alias Map (12 rows)**: Maps staged duplicate IDs to existing lane canonical IDs:
   ```json
   {
     "S039": "S033",
     "S040": "S034",
     "S041": "S035",
     "S043": "S041",
     "S055": "S036",
     "S056": "S037",
     "S057": "S038",
     "S060": "S039",
     "S064": "S041",
     "S068": "S040",
     "S076": "S041",
     "S123": "S032"
   }
   ```
2. **Sequential Adoption Map (81 rows)**: Maps the remaining 81 genuinely absent staged rows to consecutive lane IDs starting at `S043` (since `S042` is consumed in round 28):
   - Staged `S044` -> Lane `S043`
   - Staged `S045` -> Lane `S044`
   - ... and so on.

### Affected Axes

- **`coverage` (Improved)**: Eliminates the manual, error-prone ID resolution hurdle for all 66 remaining staged knowledge entries in `shokuknow/merge/kasegi/knowledge/`, enabling predictable multi-entry assimilation in future rounds.
- **`depth:verifiability` (Improved / No Harm)**: Guarantees that every assimilated knowledge entry's `source:` headers and recheck commands resolve strictly to valid, canonical lane registry rows and committed snapshots.
- **`depth:density` (No Harm)**: Preserves text formatting and citation structures without artificial inflation or layout distortion.

### Risks

1. **Section Anchor Mismatch**: When aliasing staged rows `S064` or `S076` to Lane `S041`, the citing entry expects specific anchors (e.g., 付録6 §2 or §4). Scribe seats must verify that Lane `S041`'s scope/anchor covers these sections or update `used-by` accordingly.
2. **Snapshot Text Drift**: Staged quote assertions must be checked against the lane's actual text snapshots (`corpus/source-snapshots/round-28/S041.txt`) via `source-recheck.py`.

### Verification

- Execute a dry-run check verifying that the crosswalk correctly translates `japanese-domestic-disclosure-workflow.md` headers from staged (`S042`, `S043`) to lane (`S042`, `S041`).
- Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` to verify that no collision or syntax violation is introduced.
- Run `python3 corpus/instruments/frontier-recheck-count.py` to confirm that all admitted entries pass harness checks.

---

## 5. Compliance & Verification Checklist

- [x] Read-only to production files: Zero modifications to `corpus/*`, `SKILL.md`, `SCORECARD.md`, or `claims.json`.
- [x] Absolute path used for report: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-28/wave1/ConnStagedCensus.md`.
- [x] Leaf operation: No subagents dispatched, no background jobs executed, no VCS mutations attempted.
- [x] Joined by URL: Verified all 12 duplicate staged rows, 82 absent staged rows, and proved staged S042 free at freeze base.
