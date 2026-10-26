# ScoutQuarantine — round 37 quarantine slice (7 kasegi register rows), hand-check receipt

Seat `ScoutQuarantine` (scout, leaf, read-only). Lane repo head at check time `b362068195d5489aa94b31e6ec8f880c367e0ba0`.
Fetch date (UTC) 2026-10-26 (host clock 17:13Z). No lane/fleet/shokuknow file was written; only this receipt.
Tooling installed: none (curl, pdftotext/pdfinfo 3 already on host).

## 0. Inputs and what the slice rows really are

- Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`. Slice list: `.ufo/waves/round-37/assimilation/quarantine-slice` (7 ids).
- The register's `kasegi` lines are **campaign-staging rows** (`/home/vgpnk/Projects/shokuknow/lanes/kasegi/{SOURCES-PROPOSED.md,round2..4/SOURCES-PROPOSED.md}` with their `## Gate — S0nn` blocks), not rows of the shipped lane `corpus/SOURCES.md`. The shipped lane already holds different S037 (Cybozu FAQ), S048 (MSVR) and, from this round, S054 (SSVC). Any adoption of these staged rows would therefore need fresh ids (> current registry max), never the staged ids. Register line numbers: S037 L99, S054 L100 (payload-absent); S048 L322, S065 L323, S068 L324, S069 L325, S070 L326 ("could not be fetched").
- Method per row: take cited URL and gate quote from the staged `## Gate` block (the register's quote column for S037/S054 matches it; the five unreachable rows carry no quote in the register, so the gate-block quote was used), curl with 60 s cap, extract text (HTML strip / `pdftotext -enc UTF-8 -layout`), search with whitespace-insensitive matching (CJK text wraps on whitespace and page footers).
- Archive of fetched bytes (sha256 prefixes): S037 `9ce91321`, S048 `95cd25d8` (404 body), S054 `0150c9d1`, S065 `e33b0f67`, S068 `a4ea10f8` (403 body; real page via redirect below), S069 `b0c046970f9c…`, S070 `2eff0a5b10e2…`. S069 and S070 are **byte-identical** (`cmp`) to the campaign cache copies `.qcache/aaf68de1….pdf` and `.qcache/bfd1cc79….pdf` captured 2026-10-24.

## 1. Verdict table

None of the seven is a fabrication. Class names follow the task: absent (fabrication -> refuse) / unreachable (unverifiable) / present-and-located (adopt with anchor).

| id (lane, round) | register class | verdict | one-line basis |
|---|---|---|---|
| S037 (kasegi r1) | payload-absent | **present-and-located, quote defective (stitched)** — not fabrication | page fetched 200; every field is present, the single contiguous quote is a stitched/punctuated rendering of table cells that exists nowhere verbatim |
| S054 (kasegi r3) | payload-absent | **present-and-located, quote defective (elided)** — not fabrication | PDF fetched 200; phrase present at （ア） with a parenthetical definition elided from the quote |
| S048 (kasegi r2) | unreachable | **unreachable at the cited locator** (HTTP 404, deterministic); wording found in two other fetched documents | cannot verify the row as cited; do not adopt as cited |
| S065 (kasegi r4) | unreachable | **present-and-located** (register's failure was a fetch/size problem, now fetches) | quote present, split by a PDF page break |
| S068 (kasegi r4) | unreachable | **present-and-located** (register's failure was a bot block on browser UA) | exact sentence present after redirect to Cisco's relocated URL |
| S069 (kasegi r4) | unreachable | **present-and-located** | exact quote at PDF page 25; endpoint needs referer + `-k` |
| S070 (kasegi r4) | unreachable | **present-and-located** | exact quote at PDF page 1 (item 1.2) |

Zero rows are absent/fabrication-class; zero are unverifiable-with-no-evidence. Adoption note: the instruction expected none present-and-located; five are located (S065, S068, S069, S070 clean; S037/S054 with quote-form defects). I adopt nothing (leaf seat, receipt only); anchors below are available to whoever integrates.

## 2. Per-row evidence

### S037 — GB/T 30279-2020 catalogue record
- URL `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A` -> `http=200 size=24207 ct=text/html;charset=utf-8`, no redirect.
- Gate/register quote: `信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01`.
- Whole-string whitespace-normalised search: **False**. Reason (observed, page text after whitespace removal): `中文标准名称：信息安全技术网络安全漏洞分类分级指南英文标准名称：Informationsecuritytechnology—Guidelinesforcategorizationandclassificationofcybersecurityvulnerability标准状态：现行…发布日期2020-11-19实施日期2021-06-01`. So the quote differs by (a) the English-name cell interposed between title and status, (b) no colon after 发布日期/实施日期 (the labels and values are separate `<div>` cells), (c) the intervening CCS/ICS cells.
- Component search, each True: `网络安全漏洞分类分级指南`, `标准状态`, `现行`, `2020-11-19`, `2021-06-01`, `GB/T 30279`. HTML anchors in the fetched body: L446 `中文标准名称：<b>信息安全技术 网络安全漏洞分类分级指南</b>`, L461 `标准状态：` (value `现行` follows), L517-L519 `发布日期` / `2020-11-19`, L524-L526 `实施日期` / `2021-06-01`.
- Classification: content present, facts (title, 现行, 2020-11-19, 2021-06-01) all verified; the defect is quote construction (concatenation of non-adjacent cells with invented colons). Fix = quote cell-by-cell (`标准状态：现行`; `发布日期` … `2020-11-19`; `实施日期` … `2021-06-01`) or paraphrase, not refuse. Adopt-with-anchor: `openstd.samr.gov.cn … newGbInfo?hcno=458BACCE…` HTML L446/L461/L517/L524 on 2026-10-26.

### S054 — Cabinet Office request to IPA (令和8年9月17日 府サ連第7号)
- URL `https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf` -> `http=200 size=513648 ct=application/pdf`, PDF 1.7, 3 pages (30 harmless "font type mismatch" poppler warnings).
- Gate/register quote: `脆弱性の悪用が確認されたもの又は疑われるもの`. Normalised exact search: **ABSENT**.
- Located text (`pdftotext -layout` lines 43-48): `１．脆弱性関連情報の提供について` / `（ア） 脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認` / `されたもの又は疑われるもの` / `（イ） 以下のいずれにも該当するもの`. The source reads `脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの`; the staged quote silently drops the parenthetical definition.
- Classification: present at １．（ア）; quote needs an ellipsis marker (`脆弱性（…）の悪用が確認されたもの又は疑われるもの`) or be cut to `の悪用が確認されたもの又は疑われるもの`. Not fabrication. Anchor: PDF text L46-L47, page 1 (section １．脆弱性関連情報の提供について, item （ア）).
- Collision flag: the shipped lane's S054 is now SSVC (this round); this staged S054 must take a new id if ever adopted.

### S048 — std.samr.gov.cn plan 20260806-T-469 detail page
- URL `https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3` -> **HTTP 404** (Apache Tomcat/9.0.122 body: `文件[/WEB-INF/views/gb/search/gbDetailed.jsp] 未找到`, 748 B). Repeated 3 more times (plain, with `Referer: https://std.samr.gov.cn/` twice): 404 each time. `http://` scheme: 301. `gbDetailed.do?id=…`: 404. archive.org availability API: `archived_snapshots: {}`.
- Control: the same endpoint with other ids returns 200 (`4C30E22D…` 99875 B, `B4C25880…` 89549 B, `25BC096E…`, `4C30DC37…`, `49FD1852…`, `5D515685…` all 200) — so the host is up and the 404 is specific to this id (record withdrawn/renumbered). `25BC096E…`, `4C30DC37…`, `5D515685…` mention `20260806-T-469`, but none contains the gate quote or a `范围和主要技术内容` block.
- Gate quote `将原标准的技术分级和综合分级修订为两个独立的分级结果` (page section 范围和主要技术内容 item 10): not verifiable at the cited locator. The identical clause **is** present in two other fetched documents: S069 draft standard foreword item d) — `d)更改了“网络安全漏洞分级”，将原标准的技术分级和综合分级修订为两个独立的分级结果（见6.1、6.3，2020年版的6.1、6.3）` (PDF page 4 of 58) — and S070 drafting note (PDF page 5 of 8).
- Classification: **unreachable** (no locator resolves for the row as cited; unverifiable as cited, not a fabrication — the campaign's own SEARCH-LOG shows the same page curl'd on 2026-10-23 and the substantive claim is corroborated by S069/S070). If the claim "revision splits 技术分级/综合分级 into two independent results" is wanted, re-anchor it to the S069 foreword d) (page 4) rather than to this dead URL; the "项目周期 16个月 / 下达 2026-03-02 / 公示" facts carried by the row are NOT corroborated by anything I could fetch.

### S065 — NPC 现行有效法律目录（303件）
- URL `http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf` -> `http=200 size=7465472` (matches the gate's stated 7 465 472 bytes), PDF 1.7, 30 pages.
- Gate quote `1． 中华人民共和国刑法（1979 年通过，1997 年修订，2009 年修正）`. Raw whitespace-normalised search: ABSENT only because of a page-break artefact: text L1182-L1189 reads `刑法（7 件）` / `1． 中华人民共和国刑法（1979 年通过，1997 年修订，` / printed page footer `27` / `2009 年修正）` / `附件一：…`. The entry crosses PDF page 27 -> 28 and the footer digits sit inside it; with the footer removed the quote matches. Also found: `现行有效法律目录（303件）（截至2026年8月28日…` and 12 `刑法修正案` lines (1999 … 2023) under 附件二 (L1208-L1222+).
- Classification: present-and-located. Anchor: PDF text L1182-L1189, section 刑法（7 件） entry 1, page 27/28 boundary. (Register's "unreachable" = fetch failure of a 7.4 MB PDF at census time; reachable now in ~30 s.)

### S068 — Cisco Security Vulnerability Policy
- URL `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html`: with a browser User-Agent -> **HTTP 403** (`AkamaiGHost`, "Access Denied", 465 B) — this is why the register could not fetch. With default curl UA -> 301 -> `https://tools.cisco.com/security/center/resources/security_vulnerability_policy.html` -> 301 -> `https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html` -> `http=200 size=94027`.
- Gate quote `The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018 , which are guidelines for disclosure of potential vulnerabilities established by the International Organization for Standardization.`: **found verbatim** (whitespace-normalised; also with the stray space before the comma removed). Page text context: `…Cisco product security incidents. The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018 , which are guidelines…`.
- Classification: present-and-located. Anchor: section "Cisco Product Security Incident Response", sentence 2 after "(PSIRT) is responsible for responding to Cisco product security incidents", final host `sec.cloudapps.cisco.com` (the cited cisco.com URL is a redirect source and 403s to browser UAs — the locator cell should carry the final URL or a note).

### S069 — GB/T 30279—202X draft standard (征求意见稿)
- URL (long `dcpspTools/gbPlan/download?path=…WD_2025005470…指南.pdf`) with `-k -e https://std.samr.gov.cn/gb/search/gbDetailed?id=4C30E22D8B94BBB9E06397BE0A0A52F3` -> redirect to `https://kass.sacinfo.org.cn/kfs/token/download/jkhklbwnwhowpsog`, `http=200 size=1470121`, PDF 58 pages (both match the gate's stated figures).
- Gate quote `最后，结合漏洞技术分级和环境因素评分的结果，按照附录E计算得到网络安全漏洞综合分级。`: **found verbatim** under 6.3.2 综合分级, PDF page 25 (printed page 19). Also found: `表A.1`, `附录B…20`, `附录C…24` (contents). 
- Classification: present-and-located. Anchor: §6.3.2 综合分级, PDF p.25. Note it needs `-k` (cert chain not verifiable by curl) — reachability is conditional on a Referer header and TLS leniency, which is why the register's fetcher failed.

### S070 — 编制说明 (drafting note)
- URL (…DI_2025005470…指南.pdf), same method -> `https://kass.sacinfo.org.cn/kfs/token/download/uyczrttxfsdtvphb`, `http=200 size=234182`, PDF 8 pages (matches gate).
- Gate quote `摆脱对国外标准体系（如《通用缺陷枚举（CWE）》、《通用漏洞评分系统（CVSS）》）的过度依赖`: **found verbatim** at 一、工作简况 → 1.2 制定背景 (PDF page 1); also `20260806-T-469` and `中国信息安全测评中心` carried in 1.1.
- Classification: present-and-located. Anchor: 1.2 制定背景, page 1.

## 3. Summary for the integrator
- `absent` (fabrication class -> refuse): **0 of 7**.
- `unreachable` (no locator, unverifiable): **1 of 7** — S048 (404; claim corroborated elsewhere by S069 foreword d) / S070).
- `present-and-located`: **6 of 7** — S065, S068, S069, S070 clean; S037 and S054 located but their staged quotes need correcting (stitched / elided) before any adoption.
- The register's two `payload-absent` rows were quote-form defects (field stitching, parenthetical elision), not payload fabrication; the four "unreachable" rows that are located failed at census time for access reasons (browser-UA block, referer + TLS, large PDF).
- No lane file was changed; nothing adopted; id-collision caveat above applies to S037/S048/S054 staged ids against the shipped registry.

Scratch dir `/fast/scratch/hyaku/kasegi-r37/ScoutQuarantine` removed after this receipt was written.
