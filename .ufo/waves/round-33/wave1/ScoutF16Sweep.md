# ScoutF16Sweep — F16 negative sweep (round 33, read-only scout, no lane writes except this receipt)

Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Sweep run at lane tip a6a5023 on the working tree seen 2026-10-26.
**State label:** the lane tree was in flux (untracked wave dirs; ExecRegistryAppend / ExecEntryF16 not yet landed: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `48`; `awk … corpus/README.md` (admitted F rows) → `15`). All sweep counts below are therefore **PRE-STATE for S049/S050** (they describe the base ground, which is what a negative sweep needs). Re-run after quiescence: the same loop below.

## Verdict: `residual-exists` (not a restatement)

The lane holds **zero** CNVD 众测 / 360SRC platform-scope-and-reward ground. Its only trace is a refusal note (`program-severity-ladders-and-reward-scales.md:64`) saying that ground was *not adopted*. Neither refused crowdsourced entry held the helpList scope/scoring text or the 360SRC rules; they held the conduct code and the national standard (different documents).

## 1. Sweep commands and output

Files swept: `corpus/knowledge/*.md` (44 files at sweep time), `corpus/README.md`, `corpus/SOURCES.md`, `SKILL.md`. Loop (run from the lane root):

```
F="corpus/knowledge/*.md corpus/README.md corpus/SOURCES.md SKILL.md"
for t in 'CNVD' '360SRC' '360' '众测' 'zc\.cnvd\.org\.cn' 'security\.360\.cn' 'crowdsourced' 'Chinese' 'crowd-testing' '漏洞' '收录' 'SRC'; do
  echo "=== TERM: $t"; grep -c -E "$t" $F | grep -v ':0$'; done
```

Output (file:count, nonzero only):

| term | hits |
|---|---|
| `CNVD` | `program-severity-ladders-and-reward-scales.md:1` |
| `360SRC` | none |
| `360` | `triage-thresholds.md:1` |
| `众测` | `program-severity-ladders-and-reward-scales.md:1` |
| `zc\.cnvd\.org\.cn` | none |
| `security\.360\.cn` | none |
| `crowdsourced` | `SOURCES.md:1` |
| `Chinese` | `intake-surface.md:1`, `statutory-authorization-and-unauthorized-access.md:1` |
| `crowd-testing` | `SOURCES.md:1` |
| `漏洞` | none |
| `收录` | none |
| `SRC` | `program-severity-ladders-and-reward-scales.md:1`, `root-loss-2026-10-12.md:1`, `vendor-third-party-finding-coordination.md:4`, `SOURCES.md:2` |

Hit disposition (read with `grep -n -o -E '.{0,160}(CNVD|众测|crowdsourced|crowd-testing|Chinese|SRC|[^0-9]360[^0-9]).{0,200}'` over the hit files):
- `program-severity-ladders-and-reward-scales.md:64` — the only CNVD/众测 hit, and it is a refusal note: "The staged package entry also included CNVD 众测 and BILISRC ladders and a worked CNVD score example. They are **not adopted this round**: this F13 entry is limited to the three captured lane rows S043/S044/S045…". So F13 explicitly disclaims this ground.
- `triage-thresholds.md` `360` — numeric coincidence (not 360SRC; `360SRC` count is 0 everywhere).
- `intake-surface.md:146` "Chinese stack" — a dual-method schedule; unrelated.
- `statutory-authorization-and-unauthorized-access.md:93` "The Chinese half is not covered … 刑法 第285条" — statute, not platform rules; explicitly leaves Chinese open.
- `root-loss-2026-10-12.md:55` `$UFO_SRC` — env var; `vendor-third-party-finding-coordination.md` `SRC` = MSRC substrings; unrelated.
- `SOURCES.md:72` (the round-31 Search-log line) names `crowdsourced`/`crowd-testing` only as refused staged entries; `SOURCES.md:54` MSRC row.
- No `zc.cnvd.org.cn`/`security.360.cn` URL appears in any registry row, entry, README or SKILL.md (counts 0).

Registry-state check supporting "no row yet": `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `48` (PRE-STATE; becomes 50 when ExecRegistryAppend lands).

Captures exist in the lane from round 32 (`git ls-files corpus/source-snapshots/round-32` → `S049.txt`, `S050.txt`; 426 and 630 non-empty lines; 20,272 and 31,016 bytes) but have no registry row, no manifest and no entry — that is the gap F16/C1/C2 close.

## 2. The two refused staged entries

Package: `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/`.

**Filename correction (observed):** the seat prompt/claims name `chinese-crowdsourced-testing-roles-and-conduct.md`; `find /home/vgpnk/Projects/shokuknow/merge/kasegi -name 'chinese-crowdsourced*'` → no output and `ls` of that path → "No such file". The real staged file is **`cn-crowdsourced-testing-roles-and-conduct.md`** (the claims.json C2 kill_rule wording `chinese-crowdsourced-testing/chinese-crowd-…` is a truncated paraphrase of these two files). The other file name is exact: `chinese-crowd-testing-national-standard-2026-10-23.md`. Both 45 lines (`wc -l`).

Refusal record: lane `corpus/lessons/round-31.md:64-65`, confirmed by the verifier at `round-31-verifier-spotcheck.md:90-91`.

### 2a. `cn-crowdsourced-testing-roles-and-conduct.md` (sha prefix `a5302aaf`; REFUSED, "nearest to a flip")
Held:
- Sources (package ids, not lane rows): **S081** `https://zc.cnvd.org.cn/news/info?id=133&newsTypeCode=100100` — 白帽用户安全测试行为准则 (公告 2018-03-29), and **S082** `std.samr.gov.cn` standard project record 20220608-T-469 (drafting-stage scope statement).
- Rule: a Chinese 众测 has four parties (众测需求方 / 众测组织方 / 授权测试方 / 众测审计方) per GB/T 43741-2024 scope; authorisation is one role of four.
- Conduct code quotes (S081): 五、item 2 "您不得因为漏洞信息私自联系厂商"; 五、item 3 (no validating extremely unstable systems before safeguards); 一、item 1 (no retaining user data after logic-bypass verification).
- "Kasegi use": extends `authorization-safe-harbor-and-scope.md` to the Chinese regime; "platform published it" ≠ "vendor consented"; Rejected: "GB/T 43741-2024 makes an authorised tester's findings lawful…".
Refused for (round-31 lesson): Q1 no H1 (`grep -c '^# '` → 0); Q2 S081/S082 unregistered and S082 is a drafting-stage record; Q3 quotes lack revision/page and exactly-once check; Q7/Q10 prose recheck/ground is a round-6 ledger item. Flip: add H1, register+capture S081/S082, re-quote with locations, promulgated-text scope, `cd`-prefixed recheck.
Not held: any scope-list rule of a platform's *project submission page*, any scoring formula, reward table, SLA, report template or 外部漏洞 refusal.

### 2b. `chinese-crowd-testing-national-standard-2026-10-23.md` (sha prefix `6c15d941`; REFUSED, "furthest")
Held:
- Sources (package ids): **S077** (std.sacinfo.org.cn 公告 2024年第6号 list item 167), **S078** (sac.gov.cn release sentence on GB/T 43741—2024), **S079** (openstd.samr.gov.cn 标准信息表).
- Claims: GB/T 43741—2024 网络安全技术 网络安全众测服务要求 is a 推荐性国家标准, 公告 25 Apr 2024, in force 1 Nov 2024; regulator says it describes roles and duties, service process, security risks, service requirements; honest limit: full text unopened; reframing "a curator should now read the platform's rules as an implementation of, or a peer to, a national standard".
Refused for: Q1 `ground: F24` not a lane F-id and prose recheck; Q2 S077/S078/S079 unregistered; Q3 zero quote-marked strings (`grep -c '"'` → 0); Q5 no falsifiable rule or rejected over-generalisation; marginal to PROVINCE. Flip: register/capture S077–S079, quote with location, drop the reframing, add recheck and a rejected over-generalisation.
Not held: any platform text at all (it says the platform mechanics were "recorded" in earlier lane work, but the quoted platform rows are not in this lane — sweep shows 0 `zc.cnvd.org.cn` / `security.360.cn`).

### 2c. Adjacent refused staged entries that DID cite staged S034/S035 (the actual ground F16 assimilates)
These are not the two files the claim names but they are the entries that held staged S034 (= lane S049, helpList) and S035 (= lane S050, 360SRC rules). All refused (none present in `corpus/knowledge/`: `ls` → No such file for each):
- `program-scope-rules-and-asset-boundaries.md` — `source: S034`, `source: S035`; refused round 29 (`round-29.md:137`, verifier `round-29-verifier-spotcheck.md:69`/`round-29.md:166`): Q2/Q3/Q7/Q10 + Q4 universalisation ("Three different mechanisms, one invariant"; "every platform's scope list is a restatement of that ownership"). Flip: register S034+S035 as lane rows with captures, located quotes, re-ground.
- `claim-packaging-and-report-quality.md` — `source: S034/S035/S036`; refused round 29/30/31 (`round-30.md:45`, `round-31-verifier-spotcheck.md:89`): staged ids collide with lane ids, no located quotes, package F-space ground.
- `chinese-program-severity-instrument.md` — `source: S034` (CVSS 评分指标 / 评分计算方法); not in lane; refused as part of the CN package set.
- Lane note `program-severity-ladders-and-reward-scales.md:64` records CNVD 众测 ladder + worked CNVD score example as "not adopted".
Id-collision proof (read-only): `.ufo/waves/round-33/assimilation/collisions` lists S031–S048 (18 ids) so staged S034/S035 MUST be remapped to lane S049/S050 by document and every citation must use lane ids (`claims.json` assimilation note; matches the C2 surface).

## 3. What S049 / S050 add (observed in the round-32 captures, `corpus/source-snapshots/round-32/`)

Quotes ≤25 words, location = file:line of the capture (lines counted by `sed -n Np`).

**S049 = CNVD 众测 helpList (`https://zc.cnvd.org.cn/news/helpList`), stating party CNVD/CNCERT 网络安全众测平台** — not held by either refused named entry:
- Scope rule (platform intake boundary): S049.txt:214 "众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。" (followed by the redirect to the CNVD 漏洞共享平台 at `http://www.cnvd.org.cn/`). Plus S049.txt:211-212 submit-page target list "并不是项目的测试范围约定" / "请严格按照项目测试范围进行测试。" and S049.txt:410 out-of-project systems "不在客户的授权范围内，所以是坚决不允许的。"
- Scoring formula: S049.txt:132 "最终得分 = 四舍五入（有效性 × 漏洞等级 × 测试难度 × 危害程度 × 企业规模 × 报告质量）" (six factors on this platform's page; the staged S034 row said "multiplies validity, severity, test difficulty, impact, target-enterprise size and report quality" — consistent) with the enterprise-size tiers (S049.txt:118-129) and a worked CVSS-10.0 example (S049.txt:134-141). Severity from CVSS 3.0 base+temporal (S049.txt:26).
- (S049 also embeds platform account/VPN tester instructions — credential-adjacent; entry must not reproduce them, bound 8/Q6.)

**S050 = 360SRC 外部漏洞处理和评分标准 V2.0 (`https://security.360.cn/Reward/rules`), stating party 360 安全应急响应中心** — not held by any refused entry's lane-resident content:
- Scope: S050.txt:69-71 适用范围 "本标准适用于 360 集团发布的产品和业务" plus subsidiaries/JVs "也在收录范围内" with the scope list kept at `https://security.360.cn/Product/product` (a vendor-published asset boundary, not a platform intake rule).
- Process/SLA: S050.txt:91-92 web/server/mobile 漏洞审核 within three working days; S050.txt:99 final grading within seven working days after 初评级; reward formula S050.txt:112 "漏洞奖励=业务系数*基础安全币"; conversion S050.txt:129 "安全币 ：RMB=1 : 5"; two-stage grading (初评级 then 最终定级), report template (§二 1), 安全币 → cash redemption (§二 6), TOC §三–§八.
- Version provenance: V2.0, 实施日期 2023-03-01 per the staged row (change log S050.txt:11-19 lists items effective 2023.3.1).

**What F16 adds that the lane lacks:** (1) the two Chinese platforms' own scope statements (customer-authorised scope only; vendor-published product list) and reward/score mechanics, each stated by its platform; (2) a platform-vs-vendor contrast that does not universalise (the Q4 failure that killed `program-scope-rules-and-asset-boundaries.md`); (3) grounded under a real lane F-id (F16) with registered rows S049/S050, manifest records with `fetched_utc`, and located quotes; (4) complementary — not duplicate — to F13 (HackerOne/Bugcrowd ladders, which says in its own Limits that CNVD/BILISRC ladders were not adopted) and to the lane's Chinese statute/standard entries, none of which exist in-lane yet (sweep: 漏洞/收录/众测 hits 0 in all but one disclaimer line).

**Restatement risks the entry must stay clear of (reviewer checks):**
- Do not re-claim the four-role GB/T 43741-2024 structure or the "don't contact the vendor" conduct rule (S081) — those belong to refused 2a; S049 does repeat an adjacent rule (scope is customer-authorised, out-of-project forbidden at S049.txt:410), so cite it only as CNVD helpList's statement, not as a four-role law claim.
- Do not state the national-standard identity/dates/classification (refused 2b); verified: `grep -c -E 'GB/T|43741|四方|审计方' corpus/source-snapshots/round-32/S049.txt S050.txt` → `S049.txt:0`, `S050.txt:0`, so neither capture mentions the standard or the four-role/auditor structure and the entry has no source for it.
- Do not generalise "every platform's scope list is…" (Q4, refused 2c).
- F13 overlap is limited to "reward/score ladder" as a topic; the platform-specific numbers and formulas are not in F13.
- One remaining gap: S050.txt "漏洞定级标准" §七 grade table and the reward base table (S050.txt:112-160) were seen only by TOC/heading lines; the entry author must read and quote them directly.

## 4. Environment
No installs, no scratch dirs, no fetches, no mutations. Model not asserted (route table decides).
