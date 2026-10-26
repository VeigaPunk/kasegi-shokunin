# ExecQuarantine — round-38 kasegi quarantine slice (7 rows, hand-checked)

Seat `ExecQuarantine` (leaf; no subagent dispatch used). Round 38, dispatched by `KasegiR38` (hyaku run 9).
Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`,
claims freeze `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`; `claims.json` read first, not edited).

Read-only inputs:

- register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
  (375 lines, 83,621 B)
- staging rows `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` (100 lines, 89,718 B)
- quote census `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/quote-lint-full-v5.json`
  (per-row `verdict`/`quote`/`url` records, used only to know which span each row's census decision was about)

Scratch `/fast/scratch/hyaku/kasegi-r38/ExecQuarantine/` — created with `mkdir -p`, all work copies bound
there, **removed before this seat yielded**. Tooling: nothing installed or upgraded; host already carried
`curl 8.23.0` (OpenSSL 3.6.5), `pdftotext 26.08.0` (poppler), `Python 3.14.8`. No pacman transaction, no
`~/.local/bin` install, no host service touched.

---

## 1. Slice derivation — the item's command, byte-exact output

```
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md; awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R"
```

Output (7 rows; every line ends with one trailing space because `print $4, $5` keeps the space-padded
field cells — `cat -A` shows ` $` at each line end):

```
 S037   `payload-absent` 
 S054   `payload-absent` 
 S048`   the cited source could not be fetched, so no quote was checked 
 S065`   the cited source could not be fetched, so no quote was checked 
 S068`   the cited source could not be fetched, so no quote was checked 
 S069`   the cited source could not be fetched, so no quote was checked 
 S070`   the cited source could not be fetched, so no quote was checked 
```

Deliverable: `.ufo/waves/round-38/wave1/ExecQuarantine.quarantine-slice` — **7 lines, 417 bytes,
sha256 `d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862`**.

Where the rows come from (`awk ... {print NR": "$4}` on the same register):

- lines 99, 100 — the `payload-absent` table: `S037`, `S054`
- lines 322–326 — the §"Rows whose quotes were NEVER CHECKED" table: `S048`, `S065`, `S068`, `S069`, `S070`

Two mechanical facts about the emitted slice, recorded because they are load-bearing for reading it:

1. **The two tables have different column orders**, so `$5` is a *class* for lines 99–100 and the *reason
   string* for lines 322–326. The ids on lines 322–326 carry the register's own stray closing backtick
   (`S048\``), reproduced verbatim rather than cleaned.
2. The register's §"By lane" totals (`:251`) say `kasegi | 2`; the never-checked table adds 5, and the item's
   command matches both. **7 rows**, the same set and the same register lines as round-37
   (`corpus/lessons/round-37.md` Gate table cites "rows 99, 100, 322–326").

## 2. Bounded fetch log (every attempt, with status, bytes, UTC, digest)

Common invocation: `curl -sS -L --max-time 90 -A 'kasegi-shokunin/1.0' -o <file> -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' <url>`.
All files land in scratch (`/fast/scratch/hyaku/kasegi-r38/ExecQuarantine/fetch/`); digests are sha256 of
the bytes on disk.

| row | locator fetched | UTC | status | bytes | sha256 (16) |
|---|---|---|---|---|---|
| S037 | `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A` | 2026-10-26T18:29:36Z | 200 | 24,131 | `add556377faf76dd` |
| S048 | `https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3` | 2026-10-26T18:29:38Z | **404** | 748 | `95cd25d80d88cce1` |
| S048 (retry) | same | 2026-10-26T18:33:26Z | **404** | 748 | `95cd25d80d88cce1` (identical) |
| S048 control | `…gbDetailed?id=4C30E22D8B94BBB9E06397BE0A0A52F3` (staged `S091`, `SOURCES.append.md:67`) | 2026-10-26T18:33:28Z | 200 | 99,883 | `913e892590a8d4d2` |
| S054 | `https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf` | 2026-10-26T18:29:40Z | 200 | 513,648 | `0150c9d15dee603f` |
| S065 | `http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf` | 2026-10-26T18:30:40Z | 200 | 7,465,472 | `e33b0f67293441f1` |
| S068 (cited) | `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` | 2026-10-26T18:31:23Z | **403** | 463 | `5f349a5fd50b024a` |
| S068 (cited, browser UA) | same, `-A 'Mozilla/5.0 … Chrome/141.0 Safari/537.36'` | 2026-10-26T18:34:09Z | **403** | 463 | `b40a332513bb3a4a` |
| S068 (hop) | `https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html` | 2026-10-26T18:31:23Z | 200 | 94,027 | `098f99a89df3a801` |
| S069 (plain) | dcpspTools `20_WD_2025005470_…指南.pdf` | 2026-10-26T18:31:40Z | curl **exit 60** (`unable to get local issuer certificate`) | 0 | — |
| S069 (referer + `-k`) | same, `-k -e 'https://std.samr.gov.cn/gb/search/gbDetailed?id=4C30E22D8B94BBB9E06397BE0A0A52F3'` | 2026-10-26T18:31:42Z | 200 | 1,470,121 | `b0c046970f9ca2b7` |
| S070 (plain) | dcpspTools `20_DI_2025005470_…指南.pdf` | 2026-10-26T18:32:01Z | curl **exit 60** | 0 | — |
| S070 (referer + `-k`) | same, `-k -e` as above | 2026-10-26T18:32:04Z | 200 | 234,182 | `2eff0a5b10e2625e` |

PDF text extracted with `pdftotext -enc UTF-8 -layout`: S054 → 133 lines / 9,780 B; S065 → 1,295 lines /
34,332 B; S069 → 2,742 lines / 146,961 B (58 pages, `\f` page markers); S070 → 287 lines / 19,747 B (8 pages).
Line numbers quoted below are `\n`-based (grep-visible), not `splitlines()`-based.

## 3. Per-row verdicts

Verdict vocabulary is the item's: **present-and-located** / **absent** (fabrication class) / **unverifiable**
(unreachable).

| # | id | register class (line) | cited source (staging row) | quoted text tested | located? | verdict |
|---|---|---|---|---|---|---|
| 1 | `S037` | `payload-absent` (99) | `SOURCES.append.md:13` — openstd GB/T 30279-2020 catalogue record | register quote `信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01` | **no as written (0 hits); every datum present in separate cells** | **present-and-located**, quote defective (stitched) |
| 2 | `S054` | `payload-absent` (100) | `:30` — IPA 内閣府 request PDF | register quote `脆弱性の悪用が確認されたもの又は疑われるもの` | **no as written (0 hits); the sentence is present with a parenthetical dropped** | **present-and-located**, quote defective (elided) |
| 3 | `S048` | never checked (322) | `:24` — std.samr.gov.cn plan record `20260806-T-469` | no quote in the register; staging anchor `基础信息 项目周期 16个月, 下达 2026-03-02, 公示 2025-10-23 to 2025-11-22, 归口 全国网络安全标准化技术委员会` | **cited locator 404 twice (byte-identical); anchor data located on the sibling record** | **unverifiable (unreachable)** |
| 4 | `S065` | never checked (323) | `:41` — NPC 《现行有效法律目录》 PDF | staged entry quote `中华人民共和国刑法（1979 年通过，1997 年修订，2009 年修正）` (entry `chinese-statute-version-drift-2026-10-23-r4-amendment.md:17-18`) | **substance yes; contiguous bytes no (page footer `27` lands inside the span)** | **present-and-located** |
| 5 | `S068` | never checked (324) | `:44` — Cisco Security Vulnerability Policy | `The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018`; `regardless of the Cisco software code version or product lifecycle status, until the product reaches the Last Day of Support (LDoS)` | **yes at the `sec.cloudapps.cisco.com` hop (1 hit each); cited host 403** | **present-and-located** |
| 6 | `S069` | never checked (325) | `:45` — GB/T 30279—202X draft, 58 pp | `在实践应用中不会与存量漏洞数据的分级结果产生明显冲突或矛盾` + row anchor `6.3.1/6.3.2`, `表A.1 p.20`, annexes A–E | **yes (annex I, L2682; §6.3.1 L1019, §6.3.2 L1030, 表A.1 L1061, annex TOC pages match)** | **present-and-located** |
| 7 | `S070` | never checked (326) | `:46` — same plan's 编制说明, 8 pp | `摆脱对国外标准体系（如《通用缺陷枚举（CWE）》、《通用漏洞评分系统（CVSS）》）的过度依赖` + anchor `一、工作简况 1.1–1.3` | **yes (L14–L26, §1.2 制定背景)** | **present-and-located** |

**Totals: 0 fabrication-class · 1 unverifiable · 6 present-and-located (2 of them with quote-form defects).**
Nothing was adopted; adoption is the integrator's act and these are package documents with no lane row.

### 3.1 `S037` — present, quote stitched

```
count[标准信息] = 1 · count[GB/T 30279-2020] = 2 · count[信息安全技术 网络安全漏洞分类分级指南] = 1
count[标准状态] = 1 · count[现行] = 1 · count[发布日期] = 1 · count[2020-11-19] = 1
count[实施日期] = 1 · count[2021-06-01] = 1
count[信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01] = 0
```

The record is real and current: the page renders `标准号：GB/T 30279-2020`, `中文标准名称：` +
`信息安全技术 网络安全漏洞分类分级指南`, `标准状态：` + `现行`, then a two-cell pair `发布日期 / 2020-11-19`
and `实施日期 / 2021-06-01`. The register's span joins four separate table cells with invented `：`
separators and no cell boundary, so it is a paraphrase of a table — a quote-form defect, not an absent
payload. A landed entry must quote the cells separately.

### 3.2 `S054` — present, quote elided

```
L46: '  （ア） 脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認'
L47: '      されたもの又は疑われるもの'
count[脆弱性の悪用が確認されたもの又は疑われるもの] squeezed = 0
count[悪用が確認されたもの又は疑われるもの] squeezed = 1
count[脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認] squeezed = 1
```

The PDF says `脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの`.
The register quote deletes the statutory definition in parentheses, so it never matches as bytes; the
predicate itself is verbatim. Elision, not fabrication — but the elision removes a definition of 脆弱性
under 法第 42 条第 1 項, which is exactly the kind of material a lander must keep.

### 3.3 `S048` — unreachable at the cited locator

```
18:29:38Z 404 748 B sha 95cd25d80d88cce1…   (Tomcat body: "HTTP状态 404 - 未找到 … gbDetailed.jsp")
18:33:26Z 404 748 B sha 95cd25d80d88cce1…   (byte-identical retry)
18:33:28Z 200 99883 B sha 913e892590a8d4d2… control id=4C30E22D8B94BBB9E06397BE0A0A52F3
control page: count[项目周期 16个月] = 1 · count[2026-03-02] = 1 · count[归口单位 全国网络安全标准化技术委员会] = 1 · count[20260806-T-469] = 3
```

The 404 is deterministic and record-specific (the sibling id on the same endpoint returns 200), so the cited
locator is dead, not the service. The staging anchor's substance is on the sibling record, except the
`公示 2025-10-23 to 2025-11-22` datum, which is on neither page (`公示` → 0 hits, `2025-10-23` → 0 hits). The
verdict stays **unverifiable**, and the residual anchor defect is named rather than smoothed.

### 3.4 `S065` — present, span crosses a page break

```
count[刑法（7 件）] = 1                                  (L1182)
count[中华人民共和国刑法（1979 年通过，1997 年修订，2009 年修正）] = 0
count[中华人民共和国刑法（1979 年通过，1997 年修订，] = 1   (L1184)
L1184..L1188 = ['     1． 中华人民共和国刑法（1979 年通过，1997 年修订，', '', '', '                  27', '\x0c2009 年修正）']
count[中华人民共和国刑法修正案（十二）（2023 年）] = 1
```

(The second fetch of the same PDF, 18:40:11Z, reproduced the digest `e33b0f67…` and the same line numbers;
30 `\f` page markers, 1,295 newline-lines.)

The entry `1．中华人民共和国刑法（1979 年通过，1997 年修订，2009 年修正）` is in the catalogue; the layout
extractor puts the page-27 footer between `1997 年修订，` and `2009 年修正）`. Located (substance verbatim);
a byte-exact citation needs a line-break-aware reading or an explicit marker.

### 3.5 `S068` — present at the hop, cited host blocked

```
cited URL          403 463 B "Access Denied" (kasegi UA)      sha 5f349a5fd50b024a…
cited URL          403 463 B (Chrome 141 UA)                  sha b40a332513bb3a4a…
hop sec.cloudapps  200 94027 B                                sha 098f99a89df3a801…
count[The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018] = 1
count[regardless of the Cisco software code version or product lifecycle status, until the product reaches the Last Day of Support (LDoS)] = 1
count[Cisco Product Security Incident Response] = 4 · count[Disclosure of Security Vulnerabilities] = 2
```

Both staged sentences are verbatim on the hop page (whitespace-normalised; the HTML puts a space before the
following punctuation). The cited URL does not redirect at all today — it is blocked outright.

### 3.6 `S069` — present; the citing entry's annex anchor is one off

```
200 1470121 B sha b0c046970f9ca2b7…   PDF 1.7, 58 pages
6.3.1 line [1019] · 6.3.2 line [1030] · 表A.1 line [1061] · 附录 H line [2442] · 附录 I line [2673]
annex TOC: A 可利用性评分表 p.20 | B 影响程度评分表 p.24 | C 环境因素评分表 p.25 | D 漏洞技术分级表 p.32
           | E 漏洞综合分级表 p.33 | F 分类示例 p.34 | G 分级示例 p.36 | H 兼容性说明 p.47 | I 兼容性说明 p.51
count[在实践应用中不会与存量漏洞数据的分级结果产生明显冲突或矛盾] squeezed = 1   (L2682, inside 附录 I)
count[在实践应用中不会与存量漏洞数据的分类结果产生冲突或矛盾] squeezed = 1    (L2450, inside 附录 H H.1)
```

The row's own anchor (§6.3.1, §6.3.2, `表A.1 p.20`, annexes A–E) is correct against the TOC. The defect is in
the *citing knowledge entry*: `chinese-grading-standard-draft-2026-10-23.md:39` attributes the **分级** sentence
to 附录H, but 附录H is 漏洞**分类**兼容性说明 (it carries the 分类 variant) and the 分级 variant is in 附录 I.
Quote located, anchor misattributed — an adoption blocker for that entry, not for the row.

### 3.7 `S070` — present

```
200 234182 B sha 2eff0a5b10e2625e…   8 pages
1.1 任务来源 L9 · 1.2 制定背景 L14 · 1.3 起草单位 L27   (all count = 1)
count[20260806-T-469] = 1 · count[中国信息安全测评中心] raw = 5 · count[全国网络安全标准化技术委员会] = 2
count[摆脱对国外标准体系（如《通用缺陷枚举（CWE）》、《通用漏洞评分系统（CVSS）》）的过度依赖] squeezed = 1
```

§1.1 reads `…由中国信息安全测评中心负责承办，计划号：20260806-T-469。本标准由全国网络安全标准化技术委员会归口管理。`,
and §1.2 carries the quoted motive verbatim across two line wraps.

## 4. Comparison with round-37

Round-37's verdicts are in `corpus/lessons/round-37.md` §Assimilation ("Quarantine slice verdicts: 7 rows, 0
adopted — 0 fabrication-class, 1 unreachable (S048), 6 present-and-located") and its Gate table (rows S037,
S054, S048, S065, S068, S069, S070).

| id | round-37 | round-38 (this seat, fresh fetches 2026-10-26) | agreement |
|---|---|---|---|
| S037 | present-and-located, quote defective (stitched) | present-and-located, quote defective (stitched) | agree |
| S054 | present-and-located, quote defective (elided) | present-and-located, quote defective (elided parenthetical) | agree |
| S048 | unreachable as cited (404 deterministic; siblings 200) | unverifiable (404 ×2 byte-identical; sibling 200) | agree |
| S065 | present-and-located (quote crosses a page break with footer digit inside) | present-and-located (page footer `27` inside the span; contiguous bytes = 0) | agree |
| S068 | present-and-located (cited URL 403; hop serves the sentence verbatim) | present-and-located (403 with kasegi UA **and** Chrome UA; hop verbatim) | agree |
| S069 | present-and-located | present-and-located; **citing entry's annex anchor H→I is wrong** | class agrees, anchor defect added |
| S070 | present-and-located | present-and-located | agree |

Totals agree row for row: **0 fabrication-class, 1 unreachable/unverifiable, 6 present-and-located**. Two
refinements and one environment change are recorded rather than smoothed:

1. **S065 is located but not byte-contiguous.** Round-37 described the page break but counted the row clean;
   the measured string `中华人民共和国刑法（1979 年通过，1997 年修订，2009 年修正）` occurs 0 times in the
   extracted text. Class unchanged, citation form must carry the break.
2. **S069's citing entry mis-anchors 附录H.** The sentence the entry quotes is 附录 I's; 附录 H carries the 分类
   variant. Round-37 called S069 clean. Class unchanged; the entry, not the row, needs the correction.
3. **S068's block hardened since round-29, not since round-37.** Round-29's receipts record the cited URL as
   `301→tools.cisco.com→302→sec.cloudapps.cisco.com, final 200 / 94,027 B`
   (`round-29/wave1/ScribeLessonGate.md:58`). Today the first hop answers 403 outright — no redirect — for both
   a plain and a Chrome UA. The hop's byte count is still exactly 94,027.

Divergence that round-37 also recorded, restated because it decides how the frozen wording should be read: the
frozen non-claim wording of an earlier round called S037/S054 "payload-absent" and the rest "unreachable prose
class". The register's class column is a **candidate list** (its own header says a quote the checker could not
match is a candidate, not a verdict), and the measured slice finds **no fabrication**; the census-time failures
behind the five "never checked" rows were access problems (browser/UA block, referer + TLS leniency, a 7.4 MB
PDF), not missing payloads.

## 5. Local-artifact limb (what the census's "local artifacts" clause does and does not cover)

The lane already holds fetch copies of all seven locators from round-29, under
`.ufo/waves/round-29/wave1/assimilation/fetch/` (`S037.html` 24,189 B, `S037.txt`, `S054.txt` 8,761 B,
`S065.txt` 31,665 B, `S068.txt` 33,463 B, `S069.pdf`/`.txt`, `S070.pdf`/`.txt`, `S048-sibling.html` 99,949 B).
Independent corroboration of today's fetches:

- `S069.pdf` and `S070.pdf` are **byte-identical** to today's downloads
  (`b0c046970f9ca2b7…`, `2eff0a5b10e2625e…`) — same server, one day apart, same digest.
- `S037.html` differs in bytes (24,189 vs 24,131 — a rotating notice banner) yet carries the same four record
  fields and again **no** contiguous form of the register quote.
- Round-29's own slice is the identical command with the identical 7 rows (`round-29/wave1/ScoutAssimilation.md:46`),
  and its S068 verdict was `already-mined-by-document` because the staged S068 URL is byte-equal to lane S040
  (`round-29/wave1/ConnStagedCensus.md:30`).

So the register's "local artifacts were all checked" clause did not include these `.ufo/waves` fetch copies; a
reader who wants a second independent witness for S069/S070 has one, and a reader who wants one for S037/S054
has the same negative result twice.

## 6. Namespace warning (carried forward — load-bearing)

Register ids are **package** ids, not lane ids. Quarantine `S054` is the staged IPA 内閣府 request PDF, not the
round-37 SSVC lane row `S054`; quarantine `S037` is the GB/T 30279-2020 catalogue record while lane `S037` is
the Cybozu bug-bounty FAQ; quarantine `S048` is a `std.samr.gov.cn` plan record while lane `S048` is Microsoft
MSVR (`corpus/knowledge/vendor-third-party-finding-coordination.md:2`). None of the verdicts above says
anything about the lane rows that share a number.

## 7. Scope, no-harm, risks, blockers

**Writes.** Only `.ufo/waves/round-38/wave1/ExecQuarantine.quarantine-slice` (deliverable) and this receipt.
Scratch removed (`/fast/scratch/hyaku/kasegi-r38/ExecQuarantine/` is gone; the shared parent
`…/kasegi-r38/` holds sibling seats' dirs and was left untouched).
No mutating git or jj command was run; no `git init` fixture was needed. No pacman, no service restart, no
network write, no `agent://all` message, no swarm. Reads of `shokuknow` were file reads only — no campaign
tool was executed.

**Risks a reviewer should carry.**

- **S069/S070 were fetched with TLS verification disabled** (`-k`), because the host's chain fails
  (`curl: (60) unable to get local issuer certificate`). Those two payloads therefore rest on digest identity
  with the round-29 lane copy of the same server's bytes, not on a verified certificate chain. Verification of
  the bytes is unaffected; verification of the transport is not claimed.
- **S037's and S054's quotes are defective as written.** Any landed entry must re-quote them (S037: four
  separate record cells; S054: keep the parenthetical definition) or it reproduces the census defect.
- **S048 has no reachable cited locator.** Settling it means the integrator choosing the sibling record
  (`id=4C30E22D8B94BBB9E06397BE0A0A52F3`) and re-stating the anchor, since `公示 2025-10-23` is on neither page.
- **S069's citing entry mis-anchors 附录H** — a finding about the staged entry, recorded here so the entry is
  not adopted on the strength of "S069 is clean".

**Blockers:** none. The item's deliverable (the slice) and the per-row checked table are complete.
