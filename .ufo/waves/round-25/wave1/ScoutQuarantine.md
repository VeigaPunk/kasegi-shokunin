# kasegi — absent-defect register slice, derived and hand-checked (round 25, wave 1)

Read-only seat. The register was never edited; nothing outside this file was written.

- Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
- Pinned bytes: `sha256 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 375 lines, mtime 2026-10-24 08:37
- Census it was generated from: `quote-lint-full-v5.json` (totals `rows 1901 quotes 4152 exact 2532 folded 1296 absent 324 no_url 31 fetch_failed 78 no_quote 141`)
- Gate blocks (the rows' own quotes) read from `/home/vgpnk/Projects/shokuknow/lanes/kasegi/round{2,3,4}/SOURCES-PROPOSED.md` and `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`

## (a) The slice command, its output, and the count

```
$ awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
    /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
 S037   `payload-absent`
 S054   `payload-absent`
 S048`   the cited source could not be fetched, so no quote was checked
 S065`   the cited source could not be fetched, so no quote was checked
 S068`   the cited source could not be fetched, so no quote was checked
 S069`   the cited source could not be fetched, so no quote was checked
 S070`   the cited source could not be fetched, so no quote was checked
```

**Derived: 7 rows** (`awk … {n++} END{print n+0}` → `7`).

**The register claims 2.** Its `## By lane` table says `| \`kasegi\` | 2 |`, and that table's
column sums to exactly 194 — the row count of the first table only. So the claim and the
derivation differ by the five never-checked rows.

### What the header and `## By lane` claim vs what the file derives

| claim in the register | derived from the file | note |
|---|---|---|
| Totals: "rows with at least one ABSENT quote: **194**", "ABSENT quotes: **324**" | first table = **194** data rows, all class `payload-absent`; census `absent=324` agrees | consistent |
| class table lists `payload-absent` 194 and defines `unreachable` with no count | a second section holds **109** rows whose quotes were *never checked* (census `fetch_failed 78 + no_url 31 = 109`); the Totals block never counts them, and no row anywhere is totalled under `unreachable` | **stale/incomplete totals**: 194 + 109 = 303 rows exist, 194 are totalled |
| `## By lane`: `kasegi` **2** | kasegi data rows = **7** (2 in the ABSENT table + 5 in the never-checked table) | **stale by 5** |
| `## By lane` is a per-lane census | it covers the ABSENT table only: `lore` (9) and `mori` (3) appear in the never-checked table and are absent from it entirely | stale as a census |
| title "rounds 1-10" | ABSENT table spans round1–round7; never-checked table spans round1–round10 (round10 ×5, round8 ×1) | title is right for the union, not for the table under it |
| one row schema (7 columns) | the never-checked table has **5** columns and carries a stray trailing backtick on the id (`S048\``) | why the slice prints class for 2 rows and prose for 5 — `$5` is not a class there |

## (b) One verdict line per row

Fetch commands used (`/tmp/kq25`, 2026-10-25): `curl -sSL --max-time 60 -A 'Mozilla/5.0 (X11; Linux x86_64)' -o <out> <url>`, then `pdftotext -layout` for PDFs; S068 additionally
`uv run --quiet --with curl_cffi python -c "requests.get(url, impersonate='chrome')"`; S069/S070 followed the 302 to the `kass.sacinfo.org.cn` token URL and were taken over `http://` because that host's TLS chain does not verify (`curl: (60) unable to get local issuer certificate`), which the lane's own S085 row already records.

| id | register class | my class | evidence |
|---|---|---|---|
| S037 | `payload-absent` | **present (fields; quote is not a span)** | `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A` → `http=200 bytes=24143`, `<title>国家标准\|GB/T 30279-2020</title>`. Rendered text contains `信息安全技术 网络安全漏洞分类分级指南` ×1, `标准状态： 现行` ×1, `发布日期 2020-11-19` ×1, `实施日期 2021-06-01` ×1 — every value in the quoted string is true — but the assembled string `标准状态：现行` occurs **0** times (the page renders `标准状态： 现行`, and the dates sit in separate `div.row` blocks after `中国标准分类号（CCS） L80 / 国际标准分类号（ICS） 35.040`). Anchor: 标准信息 table — `中文标准名称` `<td>`, `标准状态` `<td>`, `发布日期`/`实施日期` `<div class="col-xs-12 col-md-4 content">`. Not a fabrication; the quote must be split per field to be admissible. |
| S054 | `payload-absent` | **present (elided; not verbatim)** | `https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf` → `http=200 bytes=513648`; `pdftotext -layout` lines 46–47, §１．脆弱性関連情報の提供について → （ア）: `脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの`. The quoted string occurs **0** times because the row dropped the parenthetical statutory definition. Content is true at the named anchor; the quote is a compression, so it cannot be filed verbatim (Q9). |
| S048 | never checked ("could not be fetched") | **unverifiable as cited (404)** | `https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3` → `http=404 bytes=748`, body `<title>HTTP状态 404 - 未找到</title>`. The live sibling plan record `https://std.samr.gov.cn/gb/search/gbDetailed?id=4C30E22D8B94BBB9E06397BE0A0A52F3` (row S091) is `http=200 bytes=99903` and carries `基础信息`, `项目周期 16个月`, `下达日期 2026-03-02`, `TC260（全国网络安全标准化技术委员会）归口`, `正在征求意见` — but **no** `范围和主要技术内容` field, **no** `公示`, and the row's quote `将原标准的技术分级和综合分级修订为两个独立的分级结果` occurs **0** times there. Not a fabrication verdict (no source was ever checked); not confirmed at any URL I could reach. |
| S065 | never checked | **present** | `http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf` → `http=200 bytes=7465472`; `pdftotext -layout` lines 1184–1186, section `刑法（7 件）` entry 1: `1． 中华人民共和国刑法（1979 年通过，1997 年修订，` + page footer `27` + `2009 年修正）`. Whitespace-normalized match is `False` only because of that footer line; with it dropped, `True`. Anchor: `s065.txt:1184-1186` (page break inside the quote). Nuance: the catalogue's own as-of line is `（截至 2026 年 8 月 28 日 …）`, not "September 2026" as the staged entry says. |
| S068 | never checked | **present (verbatim)** | `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` → default curl UA `http=403 bytes=465` (`Access Denied`, Akamai ref `18.44c91002.1792917162.1448c42`); Chrome TLS fingerprint → `http=200 bytes=94027`, exactly the byte count round 24 measured. Quote occurs **exactly once**: `The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018 , which are guidelines for disclosure of potential vulnerabilities established by the International Organization for Standardization.` Anchor: section `Cisco Product Security Incident Response`. The gate block's recorded access inversion ("403 to a browser user agent and 200 to a plain client") did **not** reproduce today. |
| S069 | never checked | **present (verbatim)** | Endpoint `…gbPlan/download?path=…20_WD_…pdf` → `http=302`, `Location: https://kass.sacinfo.org.cn/kfs/token/download/fgwzxmywkxrjmiiv`; that URL over `https` fails verification (curl 60), over `http` → `200`, `bytes=1470121`, `PDF 1.7, 58 page(s)`. Quote at `s069.txt:1041`, §6.3.2 综合分级 final step: `最后，结合漏洞技术分级和环境因素评分的结果，按照附录E计算得到网络安全漏洞综合分级。` (exact count 1). Supporting anchors: `6.3.1 技术分级` line 1019, `6.3.2 综合分级` line 1030, `表D.1 漏洞技术分级表` line 1599, `表E.1 漏洞综合分级表` line 1628, 附录A–E 规范性 / 附录F–I 资料性 in the TOC lines 47–56. |
| S070 | never checked | **present (verbatim modulo line wrap)** | Same endpoint with `20_DI_…` → `302` → token URL; over `http` → `200 bytes=234182`, `PDF 1.7, 8 page(s)`. Quote at `s070.txt:21–22`, §一、工作简况 → 1.2 制定背景: `摆脱对国外标准体系（如《通用缺陷枚举（CWE）》、《通用漏洞评分系统（CVSS）》）的过度依赖` (exact 0 because of the wrap, whitespace-normalized 1). Supporting anchors: `一、工作简况` line 8, `1.1 任务来源` line 9, `计划号：20260806-T-469` line 13, `中国信息安全测评中心负责承办` line 12, `全国网络安全标准化技术委员会归口` line 13. |

## (c) Adoptability this round

**Exactly one slice row is adoptable this round: S068, as lane id `S040`** — its quote is
present verbatim at the page's own anchor, and the round's renumber map already carries
`S068 → S040` in the five-row adoption set (`.ufo/waves/round-25/assimilation/ids/renumber-map.md`,
also `CollisionGuard.md:150`). None of the other six is adoptable as filed: S065/S069/S070 are
quote-verified but outside the C2 admission set and still carry package ids, S037 and S054 are
true in content but not quotable as written, and S048 is dead at its cited id.

**Contradiction the L1 must reconcile:** `claims.json` still lists `vendor-cvd-policy-crosswalk`
(S068) as the round's `planned_reject` on the ground "S068 Cisco policy unreachable this round".
That ground does not reproduce — the page returns `200/94 027 B` and the gate quote occurs
exactly once — so if the row is to be rejected, the reason cannot be reachability. The renumber
map itself hedges the same point ("whether the Cisco row is actually admitted or rejected is the
C2 seat's call"), while `claims.json`'s C2 `assimilation` block says reject. The two committed
artefacts disagree; my measurement supports admission.

## Findings a reader should carry forward

1. **The slice is 7, not 2.** `## By lane` counts the ABSENT table only; the five
   never-checked rows are in a second table whose schema is 5 columns, not 7, so the slice
   command prints two different things under `$5` (class vs. prose). Any consumer that reads
   `$5` as a class mis-parses five of seven rows.
2. **No fabrication in the slice.** Both `payload-absent` rows are true in content; the
   checker's ABSENT verdict is an assembly/elision artefact, exactly the "CANDIDATE, not a
   verdict" the register's own preamble promises.
3. **S068's staged entry overclaims its source.** `vendor-cvd-policy-crosswalk-2026-10-23.md:31`
   says "the two conditions under which it will go faster"; the page's lead-in is `Cisco may,
   however, expedite disclosure of a security vulnerability in the following situations:` and
   lists **four** bullets (high-severity response complete with fixes planned; observed active
   exploitation; potential for increased public awareness; third-party vulnerability declared
   high profile). Quote present, summary undercounts.
4. **S048 has no live home for its quote.** The live plan record (S091) drops the
   `范围和主要技术内容` field the row quotes from; an R8 `supersedes` row would still not
   re-ground this quote — the row needs a new anchor, not just a new id.
5. **The register's totals block is stale in a way that hides a whole family**: 194 of the 303
   data rows are totalled, and the `unreachable` class it defines is never counted.
6. **Register ids are package ids, not lane ids.** Round 25 binds lane `S036–S040` to package
   `S055/S056/S057/S060/S068` (`renumber-map.md`); lane `S037` is the Cybozu bounty FAQ
   (`corpus/source-snapshots/round-25/S037.txt`), not the openstd GB/T 30279-2020 record the
   slice's S037 names. Adopting a slice row means adopting its *document*, looked up by
   (URL, anchor) — never its staged id.
7. **Two committed round-25 artefacts disagree on S068** (`claims.json` = reject on
   "unreachable"; `renumber-map.md` = adopted as S040, with the admit/reject call left to the
   C2 seat). See (c); the reachability limb of the reject is falsified by measurement.

## Tooling

- `curl`, `pdftotext` (poppler, already present) — no install.
- `uv run --quiet --with curl_cffi` (ephemeral environment from PyPI; no system change, no
  `pacman` transaction) — needed only for S068, whose Akamai edge refuses the stock curl
  TLS fingerprint with 403.
- No `pacman` call of any kind was made.
