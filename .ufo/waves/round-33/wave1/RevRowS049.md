# RevRowS049 — round-33 wave-1 receipt

seat: RevRowS049 (reviewer, leaf — no subagents, no background jobs beyond the two poll loops named below)
round: kasegi 33, hyaku run 8; lane base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; freeze `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`
scope: the landed S049 registry row in `corpus/SOURCES.md` vs CORPUS.md SOURCES contract v1 (rules 1–6) and the staged row S034 in the read-only package `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md:10`
answering model: devin/glm-5-3-flash-1m (no step in this item is model-routed; recorded for bound 10 completeness)
tool installs: none. scratch: none created (no clone/mirror/fixture needed; nothing to clean).

## 0. Timeline and state discipline (bound 6)

- PRE-STATE (labeled; run before the row landed, ~01:19-03): registry 48 rows, malformed=0, tiers A=45 B=1 C=2, status mined=36 queued=9 rejected=3, no duplicate ids, no enum violations, no missing used-by paths; validator `W04 S028`, `W04 S029`, `ok`, exit 0. None of these PRE-STATE numbers is compared to any after column; the after numbers below are the cited ones.
- `git diff 690b69d a6a5023 -- corpus/SOURCES.md` → 0 lines and `git diff 690b69d HEAD -- corpus/SOURCES.md` → 0 lines: base, freeze and HEAD carry a byte-identical SOURCES.md, so "additions only vs base" and "vs HEAD" are the same check here.
- Landed-row poll (bound-9 pattern, single loop, cap 30 min): `until grep -qE '^\|[[:space:]]*S049[[:space:]]*\|' corpus/SOURCES.md; do sleep 20; done` → `S049 LANDED at 2026-10-26T01:25:35-03:00` (380 s).
- The file kept changing after first sight (mtime 01:25:59 → 01:27:44 → 01:28:10 → 01:28:15; ExecRegistryAppend still finishing), so every measurement below was re-run after a quiescence poll: `until [ $(( $(date +%s) - $(stat -c %Y corpus/SOURCES.md) )) -ge 120 ]; do sleep 20; done` → `QUIESCENT sha=b22c7f0173e75e0c size=52996 lines=100`. The S049 row line itself never changed across those writes: `sed -n '55p' corpus/SOURCES.md | md5sum` → `0cc7221ed7e353058430fefa5218040c` both before and after the last write.
- Item says "the six contract census commands"; the CORPUS.md census block (lines 134–148) holds seven commands. I ran all seven; the extra one (rows count) is the first.

## 1. Cell-by-cell contract check — S049 at `corpus/SOURCES.md:55`

Landed row (verbatim, `corpus/SOURCES.md:55`):

```
| S049 | 网络安全众测平台帮助 - CNVD — https://zc.cnvd.org.cn/news/helpList | docs | A | CNVD's own help-page statements for the 网络安全众测 platform: its scoring model and the boundary of the testing it accepts | capture corpus/source-snapshots/round-32/S049.txt: 帮助 nav L7 and 漏洞评分标准 nav L10, CVSS arithmetic 评分计算方法 L52, 网络安全众测平台评分标准简介 L71 with the seven-aspect sentence L72, 计算方法 heading L131 with the 最终得分 formula L132, 评分实例 L134-135, rating-change FAQ L207-209, target-list caveat L210-212, internet-vulnerability refusal L213-214, 扩大测试范围 refusal L409-410, footer 版权所有 © 2018-2026 国家计算机网络应急技术处理协调中心 L425 | CNVD's platform states its own intake boundary — only findings inside the client-authorised project scope are accepted (L214, L410) — and scores a finding as the product of the factors in its 最终得分 formula (L132), with a project's own rules able to move the grade (L208) | mined | 2026-10-26 | 90d | corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md |
```

| cell | contract rule (CORPUS.md §Shape) | observed | verdict |
|---|---|---|---|
| id | `S`+3 digits, next unused, never reused | `S049`; pre-append registry ended at S048 (48 rows); `grep -cE '^\| S049 \|'` on base blob → 0 | ok |
| source | title — canonical URL | `网络安全众测平台帮助 - CNVD — https://zc.cnvd.org.cn/news/helpList`; URL byte-equal to the manifest record's `url` (`round-32/manifest.json` sources[0].url) | ok |
| kind | enum | `docs` ∈ enum (census kind check silent) | ok |
| tier | scoped, never global; A = primary/authoritative for that scope | `A` with scope cell "CNVD's own help-page statements for the 网络安全众测 platform: its scoring model and the boundary of the testing it accepts" — the platform's own manual, primary for its own rules; kind `docs` so no tier-inflation | ok |
| scope | the claim/topic the tier applies to | scoped to the platform's own statements (scoring model + accepted-testing boundary), not a general CN claim | ok |
| anchor | exact section/heading/page/line plus revision; never a bare homepage | capture-pinned: file + 13 located section/line claims + footer date line L425; not a bare homepage. Every line claim re-verified against capture bytes (§2). The page shows no visible publication/revision date (also stated in the Registry-changes line), so the committed capture + manifest sha pin is the revision anchor — same shape the lane admitted for S048 (round-31) | ok |
| teaches | one grounded learner benefit | one benefit, attributed ("CNVD's platform states…"), each clause pinned to L214/L410, L132, L208 — all verified in the capture (§2) | ok |
| status | queued/mined/rejected; mined = cited by ≥1 used-by path | `mined`; used-by path exists and its `source:` line cites S049 (`corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md:3` starts `source: S049 — https://zc.cnvd.org.cn/news/helpList — 网络安全众测平台 使用手册…`) | ok |
| opened | ISO date the row's author opened the source | `2026-10-26` — the item's required value (staged `2026-10-23` not carried); matches the manifest's 2026-10-26 re-fetch note and the round-31 precedent (staged 2026-10-23 → landed open date) | ok |
| recheck | ISO date or cadence (`90d`, `180d`, `on-release`) | `90d` — valid cadence form | ok |
| used-by | repo-relative paths or `—` | `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` — exists (census used-by check silent) | ok |

Column count and cell hygiene, measured on the quiescent bytes:

```
$ awk -F'|' 'NR==55 {print "S049 NF=" NF} NR==56 {print "S050 NF=" NF}' corpus/SOURCES.md
S049 NF=13
S050 NF=13
$ sed -n '55p' corpus/SOURCES.md | awk -F'|' '{print "cells=" NF-2}'
cells=11
```

11 cells (NF=13 under the census awk), so no `|` inside any cell.

## 2. Anchor and teaches line claims re-verified against capture bytes

Capture `corpus/source-snapshots/round-32/S049.txt` (426 lines, `sha256 962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8` — equal to the manifest pin):

| anchor claim (row cell) | command | observed |
|---|---|---|
| 帮助 nav L7 / 漏洞评分标准 nav L10 | `grep -n '帮助\|漏洞评分标准' S049.txt` | `7:帮助`, `10:漏洞评分标准` (nav block L1–L13) |
| 评分计算方法 L52 | `grep -n '评分计算方法' S049.txt` | `52:评分计算方法` |
| 评分标准简介 L71, seven-aspect sentence L72 | `grep -n '评分标准简介\|七个方面' S049.txt` | `71:网络安全众测平台评分标准简介`, `72:…七个方面…` |
| 计算方法 L131, 最终得分 formula L132 | `grep -n '计算方法\|最终得分' S049.txt` | `131:计算方法`, `132:最终得分 = 四舍五入（有效性 × 漏洞等级 × 测试难度 × 危害程度 × 企业规模 × 报告质量）` |
| 评分实例 L134-135 | `sed -n '134p;135p' S049.txt` | `134:评分实例`, `135:对于一个CVSS评分为10.0分的远程代码执行漏洞：…` |
| rating-change FAQ L207-209 | `sed -n '207p;208p;209p' S049.txt` | L207 question 为什么我提交的高危漏洞被平台调整为中危漏洞？, L208 answer (manifest Q4 string verbatim), L209 follow-up |
| target-list caveat L210-212 | `sed -n '210p;211p;212p' S049.txt` | L210 question, L211 (manifest Q1 string verbatim), L212 注：请严格按照项目测试范围进行测试。 |
| internet-vulnerability refusal L213-214 | `sed -n '213p;214p' S049.txt` | L213 question 平台是否接收互联网漏洞？, L214 (manifest Q2 string verbatim) |
| 扩大测试范围 refusal L409-410 | `sed -n '409p;410p' S049.txt` | L409 question, L410 (manifest Q3 string verbatim) |
| footer … L425 | `sed -n '425p' S049.txt` | `版权所有 © 2018-2026 国家计算机网络应急技术处理协调中心 京ICP备10012421号` |

Manifest quote bindings (C1's data, cross-checked here because the row's teaches rests on the same lines): Q1→L211, Q2→L214, Q3→L410, Q4→L208, Q5→L419, Q6→L408 — all six strings found at exactly the pinned lines (`grep -n` on the capture).

teaches clauses: "only findings inside the client-authorised project scope are accepted (L214, L410)" — L214 and L410 verbatim in the capture; "scores a finding as the product of the factors in its 最终得分 formula (L132)" — L132 is exactly that product formula; "a project's own rules able to move the grade (L208)" — L208 states the platform/enterprise adjust the final rating by project rules, business traits and impact. Grounded, attributed to the platform, one benefit.

## 3. Rule 6 / Q6 — no credential material in the row

The capture carries platform-issued VPN account/password instructions at L184–L206 (registration, login, VPN连接方式, "将看到VPN的账号和密码信息" L205) and OpenVPN setup at L374–L405, plus contact channels L421–L424. The row's cells cite none of those lines and contain none of the tokens:

```
$ sed -n '55p' corpus/SOURCES.md | grep -cE '密码|账号|帐号|op://|VPN|token|api[_-]?key|session'
0
$ sed -n '55p' corpus/SOURCES.md | grep -oE 'https?://[^ |]+' | sort -u
https://zc.cnvd.org.cn/news/helpList
```

Only the canonical public URL; no session/private URL, no `op://` (rule 6, QUALITY Q6, bound 8).

## 4. Registry-level checks

Additions-only vs base and vs HEAD (pre-existing rows byte-identical):

```
$ git diff -U0 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 -- corpus/SOURCES.md | grep -cE '^\+[^+]'; git diff -U0 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 -- corpus/SOURCES.md | grep -cE '^-[^-]'
6
0
$ git diff -U0 -- corpus/SOURCES.md | grep -cE '^\+[^+]'; git diff -U0 -- corpus/SOURCES.md | grep -cE '^-[^-]'
6
0
```

The six added lines: the S049 row (line 55), the S050 row (line 56), one Search-log bullet (line 75), and three Registry-changes bullets (S049 row added, S050 row added, "No status/recheck/used-by cell changed on any pre-existing row; S001–S048 untouched (logged). Registry 48 rows pre-append → 50 post-append (R8)"). Zero minus lines → every pre-existing row byte-identical to base. The new rows sit inside the table directly after S048, whose line number (54) is unchanged — the round-31 lesson's `corpus/SOURCES.md:54` citation still resolves.

R6 drift note (observation, not a row defect): inserting rows at 55–56 shifts every line >54 by +2. The only committed citations into SOURCES.md lines >54 are the two `SOURCES.md:83` cites (`corpus/lessons/round-29.md:214`, `corpus/lessons/round-29-verifier-spotcheck.md:74`), already stale by +4 under routed M31-3 (round-31 lesson §Mistakes; carried by round-32); this append takes that drift to +6. No previously-valid citation breaks. The routed M31-3 fix should now re-point at +6.

URL uniqueness (also C1 rule B's registry side):

```
$ grep -cE 'zc\.cnvd\.org\.cn/news/helpList' corpus/SOURCES.md
1
$ grep -cE 'security\.360\.cn/Reward/rules' corpus/SOURCES.md
1
```

Base blob carried neither URL (`git show 690b69d:corpus/SOURCES.md | grep -cE 'cnvd|360\.cn'` → 0), so each new URL matches exactly one registry row.

## 5. Contract census — post-state, quiescent bytes (sha b22c7f01…)

Run from the lane root, the seven commands of the CORPUS.md census block:

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
50
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
$ awk -F'|' '…tier histogram…' corpus/SOURCES.md
A=47 B=1 C=2
$ awk -F'|' '…status histogram…' corpus/SOURCES.md
mined=38 queued=9 rejected=3
$ awk -F'|' '…duplicate ids…' corpus/SOURCES.md | sort | uniq -d
(no output)
$ awk -F'|' '…enum violations and tier inflation…' corpus/SOURCES.md
(no output)
$ awk -F'|' '…mined rows whose used-by paths do not exist…' | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
(no output)
```

Registry 48 → 50 rows; both new rows NF=13; tier A=45→47, B/C unchanged; mined 36→38, queued/rejected unchanged; no duplicate ids, no enum violation, no missing used-by path.

Maintained validator:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "exit=$?"
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
```

Same two W04 warnings as the frozen census-before baseline, no new E/W finding from the append, exit 0 — exactly the item's expectation (W04 S028/S029 only).

## 6. Staged S034 → landed S049 (mapping by document)

Staged row (`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md:10`, read-only): id `S034`, title 网络安全众测平台 帮助, same URL, kind docs, tier A, staged anchor is prose section names ("帮助, 漏洞评分标准, 计算方法 and 评价指标说明; footer…; page images dated 2025-03"), staged teaches ends "so one CVSS 10.0 RCE can score 12 or 4", opened 2026-10-23, recheck 90d, used-by four entries (three of them standing-refused staged entries).

- Mapping is by document, not number: lane `S034` is a different document (総務省 page, `soumu.go.jp`); the staged S034 URL is byte-equal to the round-32 capture's manifest record URL, and the collision scratch (`.ufo/waves/round-33/assimilation/`) records the same mapping the claims freeze.
- Cells not carried, consistent with the round-28/29/30/31 precedent logged in Registry changes: staged `opened 2026-10-23` → landed `2026-10-26`; staged prose anchor → rewritten to the capture pin with line numbers; staged used-by (refused staged entries) → the lane's own F16 entry only.
- The staged teaches' numeric flourish ("one CVSS 10.0 RCE can score 12 or 4") is not carried; the landed teaches rests on the formula line L132 and the scope lines L214/L410/L208, all verbatim in the capture. The capture's own 评分实例 (L134–L135) does exist for the CVSS-10.0 RCE example, so the landed choice is the more conservatively grounded one, not a loss of ground.
- Search log (rule 5): the appended bullet at `corpus/SOURCES.md:75` carries question, where (read-only package + twelve-term negative sweep over lane knowledge + the committed captures; "no target was re-fetched this round"), date 2026-10-26, identified 9 / screened 9 / included 2 / excluded 7, per-exclusion reasons, and the stop rationale — complete per rule 5.

## 7. Pending elsewhere (non-blocking for this verdict, named owners)

- Rule 1's Gate entry for the new rows (URL, access date, ≤25-word quote with location) lands in `corpus/lessons/round-33.md` — absent at review time (ScribeLesson's file; not present when I checked, `ls corpus/lessons/round-33.md` → not found). The row itself already satisfies the substance (URL in source cell, opened date, located capture quotes); the lesson entry is the remaining rule-1 formality for the wave.
- C1's `capture-binding-check.py` rules B/C (URL↔registry binding, fetched_utc) are ExecCaptureBinding's instrument; I verified the registry side (URL uniqueness, byte-equal URL to the manifest record) but did not run that instrument — outside my item.
- S050's row is RevRowS050's item; I only report the census-level facts above (NF=13, kind docs with the staged `spec`→`docs` change logged in Registry changes).

## 8. Verdict

**ADMIT-ROW** — the landed S049 row (`corpus/SOURCES.md:55`, quiescent sha `b22c7f0173e75e0c…`) conforms to SOURCES contract v1 rules 1–6 on every checked cell: 11 columns (NF=13), no `|` in cells, tier A scoped to the platform's own statements, capture-pinned exact anchor with 13/13 line claims verified against `S049.txt` bytes, one grounded attributed teaches, status mined with a resolving used-by path whose entry cites S049, opened 2026-10-26 (staged 2026-10-23 not carried), recheck `90d`, no credential or session material, URL unique in the registry, append additions-only (+6/−0 vs base and vs HEAD), census clean (50 rows, malformed=0, no dups/enums/missing used-by), validator exit 0 with W04 S028/S029 only.

Located quotes (each ≤25 words): "only findings inside the client-authorised project scope are accepted (L214, L410)" (`corpus/SOURCES.md:55` teaches cell); "众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。" (`corpus/source-snapshots/round-32/S049.txt:214`); "最终得分 = 四舍五入（有效性 × 漏洞等级 × 测试难度 × 危害程度 × 企业规模 × 报告质量）" (`S049.txt:132`); "版权所有 © 2018-2026 国家计算机网络应急技术处理协调中心" (`S049.txt:425`); staged, not carried: "so one CVSS 10.0 RCE can score 12 or 4" (`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md:10`).
