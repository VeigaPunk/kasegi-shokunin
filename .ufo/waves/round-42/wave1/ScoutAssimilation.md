# ScoutAssimilation — round-42 wave1 receipt

Item: assimilation §10 checks over `/home/vgpnk/Projects/shokuknow/merge/kasegi/` (read-only) —
id-collision check + quarantine-slice hand check. Frozen claims read first:
`.ufo/waves/round-42/claims.json` (C1 depth:verifiability held 4; C2 coverage held 8).
**Verdict: `Assimilation: none` — the expected outcome, justified below.**

## Deliverables (in this wave dir)

| file | lines | sha256 |
|---|---|---|
| `ScoutAssimilation.collisions` | 33 | `c60db3a338b2e8a36c524466ab5072be189d8597371954bd97d832b5592b6e43` |
| `ScoutAssimilation.quarantine-slice` | 7 | `d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862` |
| `ScoutAssimilation.txt` | 39 | `250ef9cbd290998b6ec7556561006ffbc101a3fd510c85ec780c483f7c3bc7f7` |

## 1. Id-collision check (run in scratch, absolute paths)

```sh
grep -oE '^\|[[:space:]]{0,3}S[0-9]{3,}[[:space:]]{0,3}\|' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u   # -> reg-ids.txt
grep -oE '^\|[[:space:]]{0,3}S[0-9]{3,}[[:space:]]{0,3}\|' merge/kasegi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort -u  # -> staged-ids.txt
comm -12 reg-ids.txt staged-ids.txt   # -> collisions (deliverable)
```

Result: **reg-ids 63 (S001–S063), staged-ids 94 (S031–S124), collisions 33 (S031–S063)**.
The merge report's "lane registry currently holds 30 rows" is stale: the lane has since absorbed the
earlier staged rows under remapped ids, so the staged file's entire id span S031–S063 collides with live
lane rows. Adoption requires remapping staged ids to S064+ and lane-side gate review; no row is appendable
under its staged id.

A plain-URL overlap pass also confirms content was already merged: 19 staged URLs already appear in
`corpus/SOURCES.md` (cybozu policy+FAQ, hackerone policy_versions, e-Gov 411AC0000000128, NIST 800-115,
pepabo, bugcrowd VRT README+cwe.json, 360SRC rules, cisco policy, hitachi HIRT-PUB10008, ipa jvn report +
ipedia2026q3 + todokede process, jpcert partnership_guideline2026.pdf, msrc/msvr, npa 1_kaisetsu.pdf,
soumu legal page, zc.cnvd.org.cn helpList).

## 2. Quarantine slice

Exact prescribed awk, output = deliverable (7 rows):

```
 S037   `payload-absent`
 S054   `payload-absent`
 S048`   the cited source could not be fetched, so no quote was checked
 S065`   the cited source could not be fetched, so no quote was checked
 S068`   the cited source could not be fetched, so no quote was checked
 S069`   the cited source could not be fetched, so no quote was checked
 S070`   the cited source could not be fetched, so no quote was checked
```

(5 rows come from the register's second, narrower table "Rows whose quotes were NEVER CHECKED"; their $4
carries a stray backtick and $5 is the reason text — preserved verbatim per the prescribed command.)

## 3. Fetch ledger (all to scratch; UA `kasegi-shokunin/1.0` unless noted)

| row | URL | HTTP | bytes | UTC | note |
|---|---|---|---|---|---|
| S037 | openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE… | 200 | 24131 | 2026-10-28T11:06:45Z | HTML page |
| S054 | ipa.go.jp …/request_to_ipa.pdf | 200 | 513648 | 2026-10-28T11:06:45Z | pdftotext -layout |
| S048 | std.samr.gov.cn gbDetailed?id=3B865A93… | 404 | 748 | 2026-10-28T11:06:49Z | Tomcat 404 "gbDetailed.jsp 未找到"; retry w/ browser UA + referer also 404 |
| S065 | npc.gov.cn …/P020260904396146393500.pdf | 200 | 7465472 | 2026-10-28T11:07:00Z | = Gate note's 7 465 472 B |
| S068 | cisco.com …/security-vulnerability-policy.html | 403 then 200 | 465 / 94027 | 11:07:56Z | custom UA 403; default curl UA 200 (Gate's quirk reproduced exactly) |
| S069 | std.samr.gov.cn download?path=…20_WD_….pdf | 302→200 | 1470121 | 2026-10-28T11:08:42Z | redirect to kass.sacinfo.org.cn token; TLS chain incomplete (curl 60); token URL fetched over plain http, 58 pp |
| S070 | std.samr.gov.cn download?path=…20_DI_….pdf | 302→200 | 234182 | 2026-10-28T11:08:42Z | same path; 8 pp, = Gate note's 234 182 B |
| probe | std.samr.gov.cn/ root | 200 | 109041 | 2026-10-28T11:08:5xZ | platform reachable |
| probe | gbDetailed?id=4C30E22D8B94BBB9… (S091's id) | 200 | 99883 | 2026-10-28T11:08:5xZ | sibling plan record alive → S048's single id is dead, not the platform |

## 4. Per-row verdicts (Gate quotes located in fetched bytes)

- **S037 — quarantined.** Fetch 200, but the Gate quote `信息安全技术 网络安全漏洞分类分级指南 标准状态：现行
  发布日期：2020-11-19 实施日期：2021-06-01` does not appear as one string: page rows 英文标准名称, 在线预览,
  CCS L80, ICS 35.040 sit between the 中文标准名称 value and the 标准状态/发布日期/实施日期 rows (extracted page
  text ~L296–312). All tokens exist; the contiguous quote is a reassembly. Register's payload-absent confirmed.
- **S054 — quarantined.** Fetch 200, PDF converted cleanly; source reads
  `脆弱性（（法第42条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの` — the Gate quote
  `脆弱性の悪用が確認されたもの又は疑われるもの` drops the inline parenthetical unmarked. payload-absent confirmed.
- **S048 — unverifiable.** Record id returns Apache Tomcat 404 while the platform root and sibling plan record
  (4C30E22D…, staged S091) serve 200. The cited document is gone; quote not checkable. Not a fabrication class.
- **S065 — adoptable (quote-verified).** PDF 7 465 472 B; quote `1． 中华人民共和国刑法（1979 年通过，1997 年
  修订，2009 年修正）` present verbatim (text L1183). register "unreachable" no longer holds.
- **S068 — quarantined.** Quote verified verbatim (incl. source's own `29147:2018 ,` typo) on the 200 fetch —
  but the lane already registers this exact URL as `S040` in corpus/SOURCES.md; the staged row is a
  duplicate-source re-registration, so not adoptable.
- **S069 — adoptable (quote-verified).** Draft PDF 1 470 121 B (58 pp) via the documented token-over-http path;
  quote `最后，结合漏洞技术分级和环境因素评分的结果，按照附录E计算得到网络安全漏洞综合分级。` present verbatim (text L1040).
- **S070 — adoptable (quote-verified).** 编制说明 PDF 234 182 B (8 pp); quote `摆脱对国外标准体系（如《通用缺陷枚举
  （CWE）》、《通用漏洞评分系统（CVSS）》）的过度依赖` present verbatim (text L20, wrapped in raw lines 20-21).

## 5. Justification for `Assimilation: none`

1. **Ids**: all 94 staged rows collide by id with live lane rows (33 numeric collisions S031–S063; the staged
   file's unused span S064–S124 numbers different sources than the lane's free range — appending raw would
   corrupt the registry).
2. **Quotes**: 2 of 7 quarantine rows have quotes that are not verbatim in their own cited sources
   (reassembly / dropped parenthetical); 1 source record is deleted server-side; 1 duplicates a lane row.
3. **Already merged**: the package's content largely landed in earlier rounds under remapped ids (19 URL
   matches in the lane registry), so residual value is individual rows needing remap + re-gate — an L1 merge
   operation, not a wave-1 scout adoption.
4. Nothing in this round's claims (C2 mines fresh S064 from the F25 lead screen, not from the merge package)
   requires a staged row this round.

## Tooling / hygiene

- No installs (curl, pdftotext, awk, python3 already present; pacman untouched per paused-transaction rule).
- Scratch: `/fast/scratch/hyaku/kasegi-r42/ScoutAssimilation/` — deleted before yield.
- Read-only targets honoured: no writes to shokuknow, fleet root, or lane paths other than the four named
  wave1 files. No git/jj mutations anywhere.
- Disk guard: green at run start (`/fast/scratch/hyaku` 27% used, 591 G free).
