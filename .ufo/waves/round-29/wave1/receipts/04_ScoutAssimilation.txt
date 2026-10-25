# ScoutAssimilation — round-29 wave1 assimilation pre-checks (kasegi)

Run by scout `ScoutAssimilation-2`, 2026-10-25. Scratch (owned): `.ufo/waves/round-29/wave1/assimilation/`.
Fleet root untouched; no writes to `/home/vgpnk/Projects/shokuknow`. All `Report:` paths relative to lane repo.
No subagent dispatch (leaf member). No model-dependent step: all checks are deterministic shell/HTTP probes — no answering model to record.

## 1. Id-collision check (exact round-prompt pattern)

Pattern: `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <file> | grep -oE 'S[0-9]+' | sort`, then `comm -12`.

- Lane registry ids (from `corpus/SOURCES.md`, S001–S042): 42 ids
- Staged ids (from `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`): 94 ids
- **Collisions: 12** (non-empty as expected — staged S031–S042 collide numerically with lane S031–S042)

Lane ids: S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S016 S017 S018 S019 S020 S021 S022 S023 S024 S025 S026 S027 S028 S029 S030 S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042

Staged ids: S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060 S061 S062 S063 S064 S065 S066 S067 S068 S069 S070 S071 S072 S073 S074 S075 S076 S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S087 S088 S089 S090 S091 S092 S093 S094 S095 S096 S097 S098 S099 S100 S101 S102 S103 S104 S105 S106 S107 S108 S109 S110 S111 S112 S113 S114 S115 S116 S117 S118 S119 S120 S121 S122 S123 S124

Collisions (comm -12): S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042

Interpretation: numerically colliding ids are *different documents* (staged S031–S042 vs lane S031–S042); the by-document map (§3) is the resolution, not arithmetic renumber.

## 2. Guard proof (0–3-space pattern catches indented rows)

Fixture `guard/registry-fixture.md` with an indented `  | S002 |` row, cross-run against a staged-id fixture containing S002.

- `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → extracts `S001`, `S002` (2 ids)
- `comm -12` with staged fixture → **1 collision: S002** (non-empty ✓)
- Control: column-zero-only pattern `^\|[[:space:]]*S[0-9]{3,}` → extracts only `S001`; collisions = 0 (empty)

Realistic re-run with the same 0–3-space pattern on `  | S031 |` vs the real staged-ids list → 1 collision (S031); column-zero-only → 0. Confirms the guard's sensitivity to the indentation tolerance.

## 3. By-document mapping for adopted staged rows

| Staged id | Document / URL | Lane registry row with same URL? | Lane id assignment | Lane S043/S044/S045 free? |
|---|---|---|---|---|
| S031 | HackerOne standard program policy set — https://hackerone.com/security/policy_versions | No (grep 0 hits in corpus/SOURCES.md) | S043 | S043: 0 rows ✓ |
| S032 | Bugcrowd VRT README — https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md | No (grep 0 hits) | S044 | S044: 0 rows ✓ |
| S033 | Bugcrowd VRT CWE mapping — https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json | No (grep 0 hits) | S045 | S045: 0 rows ✓ |

`grep -cE '^ {0,3}\| *S04[3-5] *\|' corpus/SOURCES.md` → 0 for each of S043/S044/S045. None of the three URLs appears in the lane registry under any id; no knowledge entry in the lane cites the VRT README, VRT CWE dataset, or HackerOne `policy_versions` (grep over corpus/knowledge).
Fresh fetch corroboration (instrument UA): S032 → 200, 8881 bytes, anchors `Description`/`Data within an Entry`/`Priority`/`April 2017`/`P1 (Critical)` all located; S033 → 200, 28482 bytes, summary matches the landed S045 capture (sha256 f583a396…, identical). S031 → 200 but the live page is a JS-gated shell (128 bytes of snapshot; "enable JavaScript" banner) — consistent with the landing capture S043 (1-line JSON, 4 quotes located verbatim). Landed captures S043/S044/S045 all digest-match their manifest entries.

## 4. Quarantine slice re-hand-check (7 rows, register lines 99/100/322–326)

Slice derived with `awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'` — **7 rows** ✓ (S037, S054, S048, S065, S068, S069, S070). Register row ids are **staged ids** (shokuknow package numbering), not lane registry ids. None is adopted this round.

| Row (register line) | Cited source | Fresh fetch (instrument UA) | Verdict | Reason + flip condition |
|---|---|---|---|---|
| S037 (99) payload-absent | https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A | 200, 24189 B (sha256 b3103b28…) | **fetched-no-quote** | All five component values present in the live page (中文标准名称 信息安全技术 网络安全漏洞分类分级指南; 标准状态 现行; 发布日期 2020-11-19; 实施日期 2021-06-01; 发布单位 国家市场监督管理总局/中国国家标准化管理委员会) but the register's *composed span* (labels+values joined) is not a contiguous string under ws/punct folds. Flip: re-base the quote as separate field-value anchors (or a line-anchored span) → becomes reachable-quote-located. Not a fabrication of facts. |
| S054 (100) payload-absent | https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf | 200, 513648 B (sha256 12bf8642…) | **fetched-no-quote** | The quoted span `脆弱性の悪用が確認されたもの又は疑われるもの` is not in the text — the live source reads `脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの` (a parenthetical definition interrupts). Flip: correct the quote to include the parenthetical (or cite `の悪用が確認されたもの又は疑われるもの` with the elision noted) → reachable-quote-located. |
| S048 (322) unreachable-prose | https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3 | **404** (instrument UA; curl http=404, 0 B). Sibling record id=4C30E22D8B94BBB9E06397BE0A0A52F3 (same 标准计划 20260806-T-469) → 200, 99949 B, anchors 计划号/20260806-T-469/项目周期 16个月/下达 2026-03-02/归口 全国网络安全标准化技术委员会/正在征求意见 all located | **unfetchable** | The *cited* URL 404s; the document itself is reachable via the sibling record id (same plan, different record). Flip: re-point the row at the live sibling id (4C30E22D…) → reachable-quote-located. Also note: staged S048 and S091 are the same document under two ids (package-level duplicate-by-document). |
| S065 (323) unreachable-prose | http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf | 200, 7465472 B PDF → 31665 B text (sha256 061b3806…) | **reachable-quote-located** | Catalogue head `现行有效法律目录（303 件）`, stamp `（截至 2026 年 8 月 28 日 十四届全国人大常委会第二十四次会议闭幕）`, section 刑法（7 件）, entry 1 中华人民共和国刑法（1979 年通过，1997 年修订，2009 年修正）, 附件一/附件二 all located. No flip needed; the register's "could not be fetched" class is stale. |
| S068 (324) unreachable-prose | https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html | 200, 94027 B (sha256 b7f7b55f…) | **already-mined-by-document** | Same document already registered in the LANE as **S040** (corpus/SOURCES.md line 46, identical URL, mined round-25). Anchors (Cisco Product Security Incident Response / Disclosure of Security Vulnerabilities / ISO/IEC 29147:2018) all locate in fresh fetch. Flip: none — row is a duplicate of lane S040; refuse the staged row. |
| S069 (325) unreachable-prose | https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F (register URL truncated at directory prefix) | Register URL as cited → 200 but **0 bytes** (no document). Full staged URL (…/20_WD_2025005470_….pdf) via token route → 200, 1470121 B, text 6300 lines | **reachable-quote-located** (via full staged URL) | Anchors 6.3.1 技术分级 / 6.3.2 综合分级 / 附录A (规范性) / 表A.1 / 可利用性 all located in the fetched draft PDF. Flip: fix the register's truncated URL (missing filename) → the cited URL itself becomes fetchable. |
| S070 (326) unreachable-prose | same truncated prefix (register URL identical to S069's) | Register URL as cited → 200, 0 B. Full staged URL (…/20_DI_2025005470_….pdf) via token route → 200, 234182 B, text 269 lines | **reachable-quote-located** (via full staged URL) | Anchors 1.1 任务来源 / 计划号 20260806-T-469 / 承办 中国信息安全测评中心 / 归口 全国网络安全标准化技术委员会 / 1.2 制定背景 / 1.3 起草单位 all located. Flip: same as S069 — complete the URL. |

### Cross-checks / notes
- The heated "could not be fetched" rows (S048/S065/S068/S069/S070) are the *unreachable* family — never fabrication class; three of five are now reachable fresh, one is already mined (S068→lane S040), one still 404s (S048).
- The two payload-absent rows (S037/S054) are the *fabrication* family: re-check shows both documents are fetchable and their factual content is present; the *quotes as written* are composite/elided spans, hence not locatable. Both rows are candidates for quote correction, not row refusal.
- Staged-package duplicate-by-document: S048/S091 (same 标准计划 20260806-T-469, two record ids) and S069/S070/S085/S086/S090 (GB/T 30279—202X draft + 编制说明 across std.samr and kass.sacinfo routes).
- Scratch artifacts (owned): `wave1/assimilation/reg-ids`, `staged-ids`, `collisions`, `guard/*`, `fetch/*` (fresh fetches + snapshots for all 9 URLs probed).
- Pre-existing preseeded files at `.ufo/waves/round-29/assimilation/` (reg-ids/collisions) match this run's results (same 42/94/12 numbers).
