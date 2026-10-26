# ScoutPackageThemes receipt — round 33 assimilation set (lesson Gate input)

Answering model: anthropic/claude-sonnet-5-5. Read-only on the package `/home/vgpnk/Projects/shokuknow/merge/kasegi/`, on the register, and on the lane (nothing copied into the lane, no package tool run, no git/jj mutation). Network: seven GETs of the quarantine-slice documentation URLs only (instrument UA `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`, `curl -m 90`, no `-k`, no TLS bypass), 2026-10-26T04:18:13Z-04:19:09Z; bytes lived in `/fast/scratch/hyaku/kasegi-r33/ScoutPackageThemes/` and were removed before yield. No contact with any bounty target (S049/S050 were **not** re-fetched; I used the committed round-32 captures).

Registry state at my reads: `grep -cE '^\|[[:space:]]*S0(49|50)[[:space:]]*\|' corpus/SOURCES.md` → **0** at 2026-10-26T04:20:55Z (lane rows = 48). Every statement below that says "lane row S049/S050" is therefore **PRE-STATE for the registry** (ExecRegistryAppend had not landed); the capture-level facts (URL, bytes, content) are not affected. Re-run: `grep -cE '^\|[[:space:]]*S0(49|50)[[:space:]]*\|' corpus/SOURCES.md` → expect 2 after the append.

## Verdict (one line each)

| staged item | verdict |
|---|---|
| staged row `S034` (CNVD 众测 helpList) → lane `S049` | **ADMIT by document** (URL byte-equal to the round-32 capture; every staged claim I tested is in the pinned capture) — admission vehicle is the lane's own F16 entry, not staged bytes |
| staged row `S035` (360SRC V2.0 rules) → lane `S050` | **ADMIT by document** (same basis) |
| `program-scope-rules-and-asset-boundaries.md` | **REJECT** (re-refused; registration half of the flip is now met, six other conditions are not) |
| `claim-packaging-and-report-quality.md` | **REJECT** (re-refused; `S036` BILISRC still unregistered) |
| `cn-crowdsourced-testing-roles-and-conduct.md` | **REJECT** (unchanged; S081/S082 not in lane, S049 does not carry the conduct code) |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | **REJECT** (unchanged; S049/S050 say nothing about GB/T 43741) |
| `chinese-criminal-thresholds-and-authorisation.md` | **REJECT** (unchanged; plus a new hazard: its dangling "row S034" now collides with a *different* lane row) |
| `chinese-program-severity-instrument.md` (not in the standing five) | **REJECT as an entry**; its S034-only metric/worked-example content is source-verified and is the reusable part |
| `program-severity-ladders-and-reward-scales.md` (not in the standing five) | **REJECT / do-not-copy** (same-name file already in the lane; copy would overwrite it) |
| quarantine slice S037 / S054 | `payload-absent` → hand-checked: **fetchable, quote not contiguous, NOT fabrication**; withheld |
| quarantine slice S048 / S069 / S070 | `unreachable` → still unreachable today: **unverifiable, not fabrication** |
| quarantine slice S065 / S068 | `unreachable` → **reachable today**, locators found / URL = lane `S040`; neither is appended |

Gate requirement (>=1 admit, >=1 reject): met (2 admits by document, 7 rejects).

## Evidence base

Digests (`sha256sum`, 2026-10-26):
```
4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb  merge/kasegi/SOURCES.append.md
8a42a9109c8c95bc55e818f0ad97e7923cbfe5a9e7792c72c59b5aaa3aecbf5b  merge/kasegi/MERGE-REPORT.json
5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833  corpus-expansion-1/absent-defect-register.md
120d8cd5d50b703809a1c1030eb3b16564251e69a8208e4c90b500343d99abc8  program-scope-rules-and-asset-boundaries.md
6ad64d785f8f767bc0e86a4967b80bcc636b5939af4ac41b1138911978ec8dbc  claim-packaging-and-report-quality.md
a5302aaf0b9a1502c8711cd620cf0cb87cd9fea8db192269fae31619548fe813  cn-crowdsourced-testing-roles-and-conduct.md
6c15d94114248beb433eeb35aca116eb2ff4beaf7abfbc9d2b9957aeb56ef83f  chinese-crowd-testing-national-standard-2026-10-23.md
1660c00c16369d0a50870185607e0a8006ed573cc4ae69a696ce568e4e8a59ae  chinese-criminal-thresholds-and-authorisation.md
442e0f2bfb08bc2cbb8951f110e64424f82203636928429bc38f46f388c4257c  chinese-program-severity-instrument.md
35de5f8b19ed3b20beb3d41c347f4727d9fd2eefc8a23e53c64c6987b60bbc87  program-severity-ladders-and-reward-scales.md
962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8  corpus/source-snapshots/round-32/S049.txt
2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888  corpus/source-snapshots/round-32/S050.txt
```
`SOURCES.append.md` and the four older refusal digests are byte-identical to the round-31 receipt (`.ufo/waves/round-31/wave1/ScoutPackageThemes.md`) and the lane's round-31 lesson Gate table; the package did not move. The two capture digests equal `.ufo/waves/round-32/capture-lines.txt` (`sha256=962a451a…` / `2f9c6406…`, `fetched_bytes` 56674 / 427391, `snapshot_bytes` 20272 / 31016, `utc=2026-10-26T02:09:46Z` / `…:50Z`).

Package defects found while reading (all independent of the Q-bar):
- `MERGE-REPORT.json` `existing_rows` = **30**, `first_id` = S031, `renumbered` = []; the lane holds **48** (S001-S048 at base). The 18 collisions are in `.ufo/waves/round-33/assimilation/collisions` (S031-S048) and `guard-proof.txt` (`reg_ids=48 staged_ids=94 collisions=18`).
- `MERGE-REPORT.json` flags **every** entry `kind: new-file`, `collides_with_existing: False`. Measured: four staged targets **already exist in the lane with different bytes** (`comm -12` of `ls` of both knowledge dirs, `LC_ALL=C sort`): `authorised-testing-rules-of-engagement.md` (staged `bf40409ec27b` 63 lines vs lane `5533fc87ab7a` 87), `japanese-domestic-disclosure-workflow.md` (`ee667c2f5d9d` 55 vs `a22d2321e39f` 103), `japanese-severity-vocabulary-and-impact-model.md` (`d7fdd31f88fb` 52 vs `f584f06c7494` 38), `program-severity-ladders-and-reward-scales.md` (`35de5f8b19ed` 50 vs `6c05c98f3c68` 67). Adopt-checklist step 4 ("copy each file") would overwrite lane text; the lane's `program-severity-ladders-and-reward-scales.md` is the round-29 F13 entry (`PASS F13 … ids=S043,S044,S045`, round-29 lesson). The package's own `has_duplicate`/`duplicate_of` fields are False/None for all four.

## (1) Staged S034/S035 ↔ lane S049/S050: URL byte equality

Command (python3, run in the lane root): extract the staged URL after ` — ` from the `| S034 |` and `| S035 |` rows of `SOURCES.append.md` (`SOURCES.append.md:10-11`), compare with the frozen round-32 claim and build spec, and count raw occurrences.
```
S034 https://zc.cnvd.org.cn/news/helpList  36 bytes  sha256[:16]=8ae60ea05f179aa3  occurrences in .ufo/waves/round-32/build-spec.py=3  in .ufo/waves/round-32/claims.json=1
S035 https://security.360.cn/Reward/rules  36 bytes  sha256[:16]=642ebcc3378386df  occurrences in .ufo/waves/round-32/build-spec.py=4  in .ufo/waves/round-32/claims.json=1
round-32 claims.json URL tokens: {'https://zc.cnvd.org.cn/news/helpList'} and {'https://security.360.cn/Reward/rules'} (regex `URL\S*`, exactly one distinct token each, no suffix)
round-33 claims.json URL tokens: set() set()    (the round-33 claims name S049/S050 by id and URL in prose only; no differing token)
```
Result: staged `S034` URL **is byte-equal** to the lane's S049 capture URL (`https://zc.cnvd.org.cn/news/helpList`), staged `S035` **is byte-equal** to S050 (`https://security.360.cn/Reward/rules`); no query, fragment or trailing-slash difference. (The S049 page text itself carries the fragment link `…/news/helpList#newsType_21`, a different anchor inside the same document.) Lane registry join, PRE-STATE: `S034 -> []`, `S035 -> []`; the only staged row that already joins is `S031 -> [S043]` (HackerOne policy_versions) and `S068 -> [S040]` (Cisco).

Content check of the captures against the staged rows/entries (whitespace-stripped, exactly-once counts in `corpus/source-snapshots/round-32/`):
- S049: `众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞` = 1 (S049.txt:214; heading `平台是否接收互联网漏洞？` :213); `测试项目范围以外的系统不在客户的授权范围内，所以是坚决不允许的` = 1 (:410); the multiplicative formula `最终得分=四舍五入（有效性×漏洞等级×测试难度×危害程度×企业规模×报告质量）` = 1 (:132); `报告质量` 优秀/1.1, 良好/1.0, 一般/0.9 with the five named fields 漏洞命名/分类选择/漏洞摘要/漏洞描述/修复建议 (:110-:116); worked example rows total 12 / 10 / 7 / 4 (:145-:160); footer `2018-2026` = 1; FAQ `为什么我提交的高危漏洞被平台调整为中危漏洞？` (:207-:209); CVSS 3.0 temporal coefficients 0.91/0.94/0.97, 0.95/0.96/0.97, 0.92 present; `https://www.first.org/cvss/specification-document` at :70.
- S050: `仅从理论层面说明漏洞的存在而无利用和复现过程将不予收录` = 1 (S050.txt:86-87, wraps a line); `V2.0` and `2023 年 3 月 1 日` present; `一、适用范围` :69 (scope = 360 group products/business plus invested companies, :70-:71), `1. 漏洞报告模板` :73, report fields 漏洞证明/漏洞危害/修复方案 = 1 each.
- Staged-claim defects visible only because the captures now exist: (a) staged `chinese-program-severity-instrument.md` anchors "newsType_6 「CVSS 评分指标」" — the text capture holds no `newsType_6` token (only `newsType_21`), so that locator is not checkable in the lane's bytes; (b) staged `program-scope-rules-and-asset-boundaries.md` says 360SRC "bounds its own scope by asset class (Web, server-side, mobile, PC client, smart hardware, privacy, threat intelligence) and by named exclusions", but S050 §一 适用范围 (:69-:71) scopes by **360 group product/business**; the asset-class vocabulary appears in the grading sections (e.g. `智能硬件产品范围` :511), so the sentence mixes scope with grading (Q3/Q4 defect, not previously listed).

## (2) Standing refusals — reason, flip, does this round change it?

All five flip conditions are quoted from `corpus/lessons/round-31.md:62-67` (the lane's recorded Gate), not re-derived. "New rows" = lane S049 (CNVD 众测) and S050 (360SRC V2.0), captured at `288ea9a`, registry append pending.

| entry | reason (lane-side, standing) | flip condition (standing) | effect of S049/S050 |
|---|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` (`120d8cd5…`) | Q1 staged ids S031/S034/S035 + colliding `ground: F09` + prose `recheck:`; Q2 S034/S035 unregistered; Q3 no located quote; Q4/Q5 three platforms generalized into a universal ("one invariant"); Q7/Q10 curl-prose recheck. HackerOne half already held by lane F13/`S043`; safe-harbour/scope split by F03/`S006` | register+capture CNVD helpList and 360SRC rules; reuse lane `S043`; quote each scope rule with a location; attribute each to its platform; executable recheck; re-ground on a lane frontier | **Partly satisfies one clause**: the "register and capture" clause becomes true once the rows land (captures committed; rows PRE-STATE). Unchanged: located quotes (the staged entry quotes none), per-platform attribution (still states one cross-platform invariant), executable recheck, re-grounding (F16 now exists but is a *different* lane entry, `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`, written this round; the staged entry would be a second F16-adjacent file). New defect: the 360SRC asset-class/scope conflation above. **Flip: no.** |
| `claim-packaging-and-report-quality.md` (`6ad64d78…`) | Q1 ground not a lane F-id, `curl … && pdftotext …` prose recheck fails `bash -n`; Q2 S034/S035/**S036** unregistered; Q3 quote-marked Chinese phrases with no page/line; Q4 regional universal ("standard practice in the Eastern programs"); Q5; Q7/Q10 | register/capture S034/S035/S036; quote each downgrade/proof rule with PDF page or line; state each as that platform's position; one falsifiable rule + one rejected over-generalization; re-ground | **Two of three registrations are satisfied** (S049, S050 — and I measured the 360SRC proof quote exactly once at S050.txt:86-87 and the 报告质量 1.1/1.0/0.9 factor at S049.txt:110-116, both entry statements). `S036` BILISRC V1.7 is still in no lane row (`grep -c security.bilibili.com corpus/SOURCES.md` → 0), and the BILISRC downgrade list and `拒绝无实际危害证明的扫描器结果` have no lane source. The "Japanese flow asks for the same things in the same order" sentence rests on the JPCERT guideline (not a lane row for this entry's purposes). **Flip: no** (needs S036 + the per-quote locators + the Q4 rewrite). Closest-to-flip after `cn-crowdsourced…` is now this entry **only if** BILISRC is added or the BILISRC paragraph is cut. |
| `cn-crowdsourced-testing-roles-and-conduct.md` (`a5302aaf…`) | Q1 no H1; Q2 S081/S082 unregistered and S082 is a drafting-stage project record; Q3 four located quotes but no revision/page and no exactly-once check; Q7/Q10 | add H1; register+capture S081/S082; re-quote with page/line and exactly-once counts under Q8; replace the drafting-stage scope sentence with promulgated text; `cd`-prefixed recheck | **Unchanged.** S081 is `zc.cnvd.org.cn/news/info?id=133&newsTypeCode=100100` (the conduct code), a different page from S049's `news/helpList`; `grep -c` in both captures for `您不得因为漏洞信息私自联系厂商`, `众测需求方`, `授权测试方`: **0, 0, 0** (S049) and 0 (S050). S049 only touches the neighbouring idea (scope: `坚决不允许`, :410; 可信测试系统 audit, :407-:408). **Flip: no.** |
| `chinese-crowd-testing-national-standard-2026-10-23.md` (`6c15d941…`) | Q1 `ground: F24` not a lane F-id, prose recheck; Q2 S077/S078/S079 unregistered; Q3 zero quote-marked strings; Q5 no falsifiable rule, no rejected over-generalization; marginal to PROVINCE | register+capture S077/S078/S079; quote the roles-and-duties sentence with location; drop/ground the "curator should now read the platform's rules as an implementation of … a national standard" reframing; recheck + rejected over-generalization | **Unchanged**, with one added caution: neither capture contains `43741` or `国家标准` (0, 0, 0, 0). The lane's F16 entry must **not** import the staged reframing (platform rules as an implementation of GB/T 43741): nothing in S049/S050 supports it. **Flip: no.** |
| `chinese-criminal-thresholds-and-authorisation.md` (`1660c00c…4e8a59ae`) | staged S044/S045/S046 unregistered and colliding in id space with lane ids; cross-instrument conclusion generalizing beyond located text (Q2/Q4); missing located quotes + non-compliant recheck (Q3/Q7/Q10) | register/capture S044/S045/S046; bound the cross-instrument conclusion to located text; located quotes; executable recheck | **Unchanged; one new hazard and one partial.** Hazard: the entry's last section cites "the exclusion of 互联网漏洞 by the 众测 platform (wave-1 row S034)". Under adopt-by-number, `S034` in the lane is `S034 | 総務省, 不正アクセス行為の禁止等に関する法律の解説 (citizen page)` (`corpus/SOURCES.md:40`) — a silently wrong citation; by document it is lane **S049**, whose capture carries the sentence (S049.txt:213-214). That one sub-claim now has a lane source; the criminal-law inference built on it ("a programmatic expression of the same boundary") is still unsupported by any capture (`情节严重` count in S049/S050 = 0). **Flip: no.** |

Additional (not in the standing five, both cite S034; not previously gated in the lane lessons I read — `grep` of round-24..32 lessons names only `program-severity-ladders-and-reward-scales.md` in the round-29 F13 PASS line):
- `chinese-program-severity-instrument.md` (`442e0f2b…`): REJECT as an entry. Q1: `ground: F10`, colliding id `S034`, prose `curl` recheck; second source `S047` (sse.com.cn JR/T 0276—2023, `grep -c 'sse.com.cn\|JR/T' corpus/SOURCES.md` → 0) unregistered; cites a "wave-1 entry `program-severity-ladders-and-reward-scales.md`" that in the lane is a *different* file. The S034-only half (CVSS 3.0 metric coefficients, temporal E/RL/RC, base×E×RL×RC, the 12/10/7/4 worked example, the 高危→中危 FAQ) is source-verified in S049 (counts above) and is the reusable fact base for the lane's F16 entry, which must restate it with line locators and a runnable `cd … source-recheck.py` line rather than copy staged bytes.
- `program-severity-ladders-and-reward-scales.md` (`35de5f8b…`): do not copy (overwrite hazard above); its CNVD half is the same S049 content; its VRT half (S032/S033) and BILISRC half (S036) are unregistered in the lane.

## (3) Quarantine slice (`.ufo/waves/round-33/assimilation/quarantine-slice`, 7 rows) — register class vs today

The register (`absent-defect-register.md`, line 99-100 and 322-326, lane `kasegi`) classes: S037 and S054 `payload-absent` (the fabrication class — "verify by hand, then correct the quote or refuse the row"); S048/S065/S068/S069/S070 `unreachable` ("re-fetch, or mark the row unverifiable — do NOT call it a fabrication"). The ids are the package's staged ids (identical to `SOURCES.append.md` S037/S054/S048/S065/S068/S069/S070), so none of these is a lane id; none is adopted. Today's fetch (curl, UA above, no `-k`):

```
S037 code=200 size=24189  final=https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A
S054 code=200 size=513648 final=https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf
S048 code=404 size=748    final=https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3   (nginx "HTTP状态 404 - 未找到")
S065 code=200 size=7465472 final=http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf
S068 code=200 size=94027  301 www.cisco.com/… -> tools.cisco.com/… -> final=https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html
S069 curl_exit=60 code=302 -> https://kass.sacinfo.org.cn/kfs/token/download/asalraqfwmwtjcdq  "unable to get local issuer certificate"
S070 curl_exit=60 code=302 -> https://kass.sacinfo.org.cn/kfs/token/download/cyhsvutlmidxesau  same error
sha256sum of bodies:
9cba2e96e343e1d0c95d23fb50454fa1321cb2d01af6ae318653290a1d20f204  S037
95cd25d80d88cce1e08528c03d5eb488f56bf9991f820bc31569b001eb2e2436  S048
0150c9d15dee603f55573f4692f306ba8ff46f70454b032f813b95fbdbb12b88  S054
e33b0f67293441f19ee519b2ed1619121da84867aa8396a3a16facd572586d83  S065
098f99a89df3a8018ab6eff7529fd8482af70dde6406472b88d526c773ded807  S068
```
(Each verdict-bearing count below is reproducible with the cited URL, tag-strip for HTML or `pdftotext -enc UTF-8` for PDF, then whitespace removal and `str.count`. S037 is a dynamic page: size and digest may drift between fetches.)

| staged id | register class | today | verdict |
|---|---|---|---|
| S037 GB/T 30279-2020 openstd record | `payload-absent` | HTTP 200, 24189 B (round-30 recorded 24,189 B; round-32 verifier 24,123 B — page is dynamic). Staged quote `信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01` matches **0** times (tags stripped, whitespace removed). Components: 标准名称 string = 1; `标准状态：现行` = 1; `发布日期2020-11-19` = 1; `实施日期2021-06-01` = 1; but `发布日期：2020-11-19` (colon form) = 0 and `实施日期：2021-06-01` = 0. Live text reads `…标准状态：现行在线预览下载标准实施信息反馈中国标准分类号（CCS）L80国际标准分类号（ICS）35.040发布日期2020-11-19实施日期2021-06-01主管部门…` | **Not fabrication; quote-shape defect.** Fetchable, every datum true, but the staged string splices separate page fields and invents colons. Not appendable as quoted; if ever adopted, re-ground with the contiguous string `发布日期2020-11-19实施日期2021-06-01` (D6 of the round-32 verifier) and record this refusal reason in `## Gate`. Agrees with round-30 `fetched-no-quote` and the round-32 spot-check. |
| S054 IPA Cabinet Office request PDF | `payload-absent` | HTTP 200, 513648 B (= round 30). `pdftotext -enc UTF-8`, whitespace removed: staged quote `脆弱性の悪用が確認されたもの又は疑われるもの` = **0**; `悪用が確認されたもの又は疑われるもの` = 1; `又は疑われるもの` = 1. Context: `（ア）脆弱性（（法第42条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの（イ）以下のいずれにも該当するもの①脆弱性の深刻度が高いと認められるもの②当該脆弱性…`; also `府連第7号` = 0 and `令和8年9月17日` = 0 in the text layer (the staged anchor's letter-head/date are not in the extracted text) | **Not fabrication; quote elided a parenthetical.** The phrase exists with an inserted `（（法第42条第１項に規定する脆弱性をいう。以下同じ。））` definition between 脆弱性 and の悪用. The anchor's `府連第7号` / `令和8年9月17日` could **not** be confirmed in the text layer today (possible image/header or different date format) — flag as an unverified sub-anchor, not a verdict on the quote. Withheld. |
| S048 plan record `id=3B865A98…` | `unreachable` | **404**, 748 B (same as round 30). The staged S091 row (same plan, `id=4C30E22D8B94BBB9E06397BE0A0A52F3`) is a different id the package itself says is the live record; I did not fetch it (not in my item) | **Unverifiable, not fabrication.** The register class stands; the dead id is a package locator problem, not a quote problem. |
| S065 NPC 现行有效法律目录 PDF | `unreachable` | **200**, 7465472 B (round 30: 7,465,472 B, identical). `pdftotext`: `刑法（7件）` = 1; `中华人民共和国刑法修正案（十二）（2023年）` = 1; `303件` = 1; `现行有效法律目录` = 1; staged entry string `中华人民共和国刑法（1979年通过，1997年修订，2009年修正）` = 0 only because the PDF extraction interleaves footnote `27` (`…1997年修订，272009年修正）`); `2026年9月` = 0 (the staged "catalogue dated 2026年9月" is inferred from the URL path `/202609/`, not from text) | **Register class stale: reachable, locators found, no fabrication.** Not appended (no admitted entry cites it; same as round 30). The footnote-merge and the URL-inferred date are Q8-normalization/Q3 notes for any future adoption. |
| S068 Cisco vulnerability policy | `unreachable` | **200** after `301 www.cisco.com → tools.cisco.com → sec.cloudapps.cisco.com`, 94027 B; page text carries `Cisco Product Security Incident Response` (4), `Disclosure of Security Vulnerabilities` (2), `CERT/CC` (2), `coordinat` (8). Staged URL is **byte-equal** to lane `S040` (`python3` `in` test on both files: `True`; lane row `| S040 |`, `corpus/SOURCES.md:46`) | **Reachable; map to existing lane S040 by document, no new row** (matches round-30 `already-mined-by-document`). Not a fabrication. |
| S069 draft PDF (WD) | `unreachable` | `302` to `kass.sacinfo.org.cn/kfs/token/download/<token>`, then `curl: (60) … unable to get local issuer certificate`; no body | **Unverifiable today, not fabrication.** No bypass (`-k` / plain-http) attempted, consistent with round 30; the staged rows S085/S086/S090 themselves say the attachment host serves an incomplete TLS chain. |
| S070 drafting note (DI) | `unreachable` | same 302 + curl 60 | **Unverifiable today, not fabrication.** Same. |

Net quarantine disposition: **0 appended**; 2 payload-absent rows downgraded from "fabrication class" to "fetched, quote not contiguous" (agrees with round 30 and the round-32 verifier, D6); 2 unreachable rows now reachable (S065, S068; S068 maps to S040); 3 unverifiable (S048, S069, S070). The register's `unreachable` rows must never be reported as fabrications; the two `payload-absent` rows are not either, on today's bytes.

## Counts to re-run (post-adoption of this round's registry)

- `grep -cE '^\|[[:space:]]*S0(49|50)[[:space:]]*\|' corpus/SOURCES.md` → 2 (today 0, PRE-STATE).
- The URL join: for each staged row in `SOURCES.append.md`, `in` test against `corpus/SOURCES.md`; expect `S034 -> S049`, `S035 -> S050` after the append.
- Same-name overwrite check: `comm -12 <(ls <package>/knowledge/corpus/knowledge | LC_ALL=C sort) <(ls corpus/knowledge | LC_ALL=C sort)` → 4 names (today).

## Scratch / tooling

Tools: `curl`, `pdftotext` (poppler) already installed; nothing installed or updated. Scratch: `/fast/scratch/hyaku/kasegi-r33/ScoutPackageThemes/` created for the seven GETs and removed before yield (`rm -rf`). Nothing written in the lane except this file.
