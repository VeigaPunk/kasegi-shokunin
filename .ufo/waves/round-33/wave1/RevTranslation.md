# RevTranslation — Chinese-language accuracy review of the F16 entry

- Seat: RevTranslation (reviewer, round 33 wave 1, hyaku run 8)
- Date: 2026-10-26
- Answering model: zai/glm-5.3-flash (config route; no model passed)
- Subject: `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`
  reviewed at sha256 `1f7ac0a2c39a0fbfdbee2ecbe112316dfc1bf7095b18cb8fb4eb9d6dfce171d1`, 306 lines, 24539 B
  (entry quiescent: ExecEntryF16 receipt present in this dir before review started; waited 480 s via bounded poll for entry + receipt to land)
- Sources: `corpus/source-snapshots/round-32/S049.txt` (426 lines), `corpus/source-snapshots/round-32/S050.txt` (630 lines), both read in full
- LSP: no lsp device in this seat's inventory and no markdown server; verification is text-level byte comparison (grep -cF/-nF against the captures). Recorded as the only available method.
- Tooling: nothing installed or upgraded (bound 5). No scratch dir created; all work read-only in the lane (bound 12 satisfied trivially). No git/jj mutation.

## Method

1. Read the entry and both captures in full.
2. For every quoted or backticked Chinese string in the entry, ran `grep -nF` against the named capture: byte-exactness, uniqueness (count=1 unless the entry claims otherwise), and line number vs the entry's citation.
3. Reproduced every count the entry states (its FC-1..FC-6 plus inline counts).
4. Re-derived the entry's pins (sha256, byte/line counts) and its cross-references (S043 quote, F13:32 quote, ScoutLiveDrift receipt).

## Command evidence

### Pin reproduction

```
$ sha256sum corpus/source-snapshots/round-32/S049.txt corpus/source-snapshots/round-32/S050.txt corpus/source-snapshots/round-32/manifest.json
962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8  .../S049.txt
2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888  .../S050.txt
6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774  .../manifest.json
$ wc -c -l S049.txt S050.txt
426 20272 S049.txt / 630 31016 S050.txt
```
All five values match the entry's "Pins read on 2026-10-26" block exactly.

### Every Chinese quote, byte-exact, unique, at the cited line

S049.txt (grep -nF, first 12 chars shown; all count=1):

```
L214 众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。
L410 测试项目范围以外的系统不在客户的授权范围内，所以是坚决不允许的。
L211 漏洞提交页面的目标列表仅用于用户快速选择，并不是项目的测试范围约定
L212 注：请严格按照项目测试范围进行测试。
L208 平台和企业在评价漏洞的风险等级时，会根据项目的规则…调整漏洞的最终评级
L419 平台将会根据企业对漏洞的评级，结合项目规则中的要求来为白帽发放奖金。
L359 用户提交漏洞所获得的奖金将会在项目结算的时候统一发放到用户的个人账户。
L132 最终得分 = 四舍五入（有效性 × 漏洞等级 × 测试难度 × 危害程度 × 企业规模 × 报告质量）
L72  网络安全众测平台为每一个被确认的漏洞设计了积分评价机制 (27 chars: counted 27)
L72  有效性、CVSS评分、数据敏感性及规模、测试难度、报告质量、测试目标企业的规模、附加分
L408 降低测试区间异常事件引发的法律风险
L408 对于未通过可信测试系统发现的问题平台有权取消或降低奖励。
L200 系统将展示相关协议条款，仔细阅读并确认接受这些条款后
L414 不建议在公开群组、或一对一聊天中询问此类信息
L356 奖金的提取没有上限，下限为每笔提现申请不低于200元。
```

S050.txt (all count=1 unless noted):

```
L70   本标准适用于 360 集团发布的产品和业务
L71   具体范围可参考 https://security.360.cn/Product/product
L70-71 合资公 / 司 wrap confirmed by sed (entry discloses it)
L113  360SRC 根据业务的重要程度分为核心业务、一般业务、边缘业务三类
L591  未纳入安全服务的资产一般情况下不收录相关漏洞
L558  评分标准和漏洞奖励仅针对对 360 产品和业务有影响的漏洞 ("针对对" byte-exact)
L112  漏洞奖励=业务系数*基础安全币。
L129,159,189,219,249,274,304  漏洞安全币（安全币 ：RMB=1 : 5） — entry: heading + 6 repeats ✓
L418  分为严重、高危、中危、低危、忽略五个等级
L99   初评级后七个工作日内我们将与业务沟通并进行漏洞最终定级
L595-596 禁止将…共享文档中 + 如因此造成漏洞泄露的，对该漏洞不予奖励 (wrap after 对, disclosed by entry)
L597  对提交漏洞报告后、未修复漏洞前，将漏洞报告公开或泄露的不予奖励。
L601  同时 360 保留采取进一步法律行动的权利。
L607  360 集团及关联方员工不参与 SRC 漏洞奖励计划
L611  本标准最终解释权归 360 信息安全部所有。
L602  《中华人民共和国网络安全法》 (entry's range 601-604 ✓)
```

### Count reproduction (all FC claims)

```
grep -c '众测平台仅接收客户授权测试范围内的安全漏洞' S049.txt → 1   (FC-1 ✓)
grep -c '不接受互联网漏洞'                        S049.txt → 1   (FC-1 ✓)
grep -c '授权'        S049.txt → 2 (L214, L410)                  (FC-2 ✓ count)
grep -c '并不是项目的测试范围约定'                 S049.txt → 1   (FC-2 ✓)
grep -c '注：请严格按照项目测试范围进行测试。'       S049.txt → 1   (FC-2 ✓)
grep -c '本标准适用于 360 集团发布的产品和业务'      S050.txt → 1   (FC-3 ✓)
grep -c '具体范围可参考 https://security.360.cn/Product/product' S050.txt → 1 (FC-3 ✓)
grep -c '未纳入安全服务的资产一般情况下不收录相关漏洞' S050.txt → 1  (FC-4 ✓)
grep -c '不予收录'    S050.txt → 6                                (FC-4 ✓)
grep -c '安全币'      S049.txt → 0 ; S050.txt → 32                 (FC-5 ✓)
grep -c '奖金'        S049.txt → 12                                (Claim 2 ✓)
grep -cE '免责|安全港' S049.txt → 0 ; S050.txt → 0                  (FC-6 ✓)
grep -c '授权测试'    S050.txt → 0                                 (FC-6 ✓)
grep -c '同时 360 保留采取进一步法律行动的权利。'      S050.txt → 1   (FC-6 ✓)
grep -c '附加分'      S049.txt → 1 (L72 only)                      (Claim 2 ✓)
awk '/^## Attribution/{f=1} /^## What this adds/{f=0} f' <entry> | grep -c -E 'CVSS|0.85|时效评价|利用代码' → 1  (Claim-2/overlap ✓ under its stated awk scope; whole-file grep gives 3 — L78 claims, L278+L281 both after the '## What this adds' boundary, correctly excluded)
```

### Cross-references

```
round-29/S043.txt:31 = "Issues affecting assets under HackerOne's control are in scope." ✓ (only one S043 in corpus)
knowledge/program-severity-ladders-and-reward-scales.md:32 holds the VRT override quote ✓
ScoutLiveDrift.md:8,10,20 — S049 fetched 2026-10-26T04:16:06Z, S050 04:16:16Z, sha equal to pins, 426/426, 630/630, diff empty ✓ (entry's drift paragraph accurate)
S049 L425-426 footer = 版权所有 …国家计算机网络应急技术处理协调中心 / 北京数字观星科技有限公司…技术支持 ✓ (Attribution ✓)
S050 L62 title, L68 本标准自 2023 年 3 月 1 日起施行。 ✓ (Attribution "effective 2023-03-01 (S050.txt:62, 68)" ✓)
S049 L132-142 = formula, floor rule, 评分实例 block, example header cells ✓
S050 L110-111 section header ✓; L119-125 coefficient table (see F4); L126+ base tables; L328 贡献值 formula; L559-560 鲸鱼阅读 exclusion; L594 九、通用规定 ✓
S050 L99-100: L99 sentence + L100 （初评级阶段不显示漏洞等级与奖励） ✓ ("keeps a finding provisional" supported)
```

## Findings

Severity order: F1 > F2 > F3 > F4 = F5 = F6. None of the six touches a manifest-bound quote string or a number; all fourteen manifest-bound strings plus twelve more inline strings verified byte-exact.

- **F1 (minor, transcription) — the S049 question title is misquoted twice.**
  Entry L3 (`source:` line) and entry L48 (Claim 1 attribution) cite the question as
  “漏洞提交时，若目标列表中没有当前目标，是否可以自行添加？”.
  The capture reads `提交漏洞时，若目标列表中没有当前目标，是否可以自行添加？` (S049.txt:210 — 提交漏洞时, not 漏洞提交时).
  The line range L210-212 is correct and the quoted answer text at L211-212 is byte-exact; only the heading transcription is wrong.
  `grep -nF '漏洞提交时'` on the capture → no match; on the entry → L3, L48.
  This slipped through because the question title is not one of the 14 manifest-bound recheck strings (those cover answer bodies only) — the entry's own `recheck:` line therefore passes while the locator is wrong. Fix both occurrences to 提交漏洞时. This is exactly the Q3 failure mode (retype-from-memory) the corpus rules target, at locator level.
- **F2 (minor, annotation accuracy) — FC-2's parenthetical misdescribes one of its two hits.**
  FC-2 states `授权` occurs exactly twice, "both inside `客户的授权范围` (L214, L410)". The count 2 is correct (L214, L410 only), but L214's occurrence sits inside `客户授权测试范围` — no 的 — so the string 客户的授权范围 occurs only at L410. The claim's substance (both occurrences are customer-authorization contexts) stands; the parenthetical should say "客户授权测试范围 (L214) / 客户的授权范围 (L410)".
- **F3 (minor, overstatement — Q4-adjacent) — "The manual's only legal-risk sentence" (Honest limit).**
  The entry: "The manual's only legal-risk sentence is the platform's own rationale for its trusted-testing system (S049.txt:408), not a waiver."
  The manual carries at least two more legal-flavoured sentences: the tester-facing dispute warning `…以避免引起不必要的纠纷` (S049.txt:410, same line as the entry's own Claim 1 quote) and the state-regulation citation `国家互联网信息办公室印发的《互联网群组信息服务管理规定》…` (S049.txt:371, real-name rationale). "Only" is falsifiable from the entry's own cited capture; soften (e.g. drop "only", or scope to "the only sentence framing legal risk as the platform's own system rationale").
- **F4 (nit, citation range) — coefficient band off by one line.**
  Claim 5 cites the per-tier band at "(S050.txt:113, 119-124)". The table runs L119-125: 业务系数(119), 核心业务(120), 一般业务(121), 边缘业务(122), 1.2~1.5(123), 0.8～1.0(124), 0.1~0.5(125). Range should be 119-125; as cited it drops the 边缘 band value.
- **F5 (nit, wrap-disclosure inconsistency) — the 1360.com example crosses a wrap unmarked.**
  Claim 4 quotes `1360.com 等域名存在第三方厂商使用的资产或公有云上的资产` as contiguous, but the capture wraps it across L591→592 (`…例如 1360.com 等域名存在第三` / `方厂商使用的资产…`). The entry carefully discloses its other two cross-wrap quotes (合资公/司 L70/71; 对/该漏洞 L595/96) but not this one; `grep -F` for the phrase as printed fails. Add the same wrap note for consistency.
- **F6 (nit, presentation) — one inline "quote" is not contiguous as displayed.**
  Claim 5 renders `初评级后七个工作日内 we will 与业务沟通并进行漏洞最终定级 (S050.txt:99)` — an English gloss substituted mid-span for 我们. The Chinese fragments are contiguous in S050.txt:99 (`…初评级后七个工作日内我们将与业务沟通并进行漏洞最终定级`); as displayed the span is spliced. Restore 我们 or mark the elision (…). Every blockquote in the entry is contiguous; this is the only exception.

## Verified-clean summary

- Every Chinese blockquote and inline citation string in the entry is byte-exact and appears exactly once at the cited line, except F1 (a locator title, not a quoted source sentence) and the two disclosed wraps (correctly disclosed).
- No number misstates the source: 27-character count correct; 安全币:RMB=1:5; coefficient bands 1.2~1.5 / 0.8～1.0 / 0.1~0.5; 不低于200元; five grades 严重/高危/中危/低危/忽略; seven-aspects-vs-six-factor tension reported faithfully with the 附加分 absence.
- English renderings checked sentence-by-sentence against the Chinese: no overstatement found in Claims 1-6 or Rejected 1-7 (attribution kept platform-local throughout; the "generally" of 一般情况下 is preserved in Rejected 4).
- Pins and cross-references (sha256 ×3, sizes, S043:31, F13:32, ScoutLiveDrift timestamps) all reproduce.
- Credential material (S049 VPN account/password steps, L202-205) is not reproduced or quoted in the entry (Q6 respected).

## Residual risk / gaps

- I did not locate the refused entry `chinese-program-severity-instrument.md` to verify the entry's claim about what that refused package held — outside this seat's Chinese-accuracy scope; the claim is about a third document and is unverified here.
- The entry characterizes S049 as the 使用手册; the page's own title is 网络安全众测平台 and 使用手册 is its nav/manual section. Reviewed and accepted as defensible (the capture's L1-22 nav lists 使用手册 and the body is manual + FAQ); noted, not a finding.
- source-recheck.py itself was not re-run by this seat; instead all 14 manifest-bound strings were independently byte-verified above (8 S049 + 6 S050), which is the stronger check.

## Suggested disposition

F1 is worth a one-line erratum or an ExecEntryF16 touch-up (two strings). F2/F3 are one-word edits. F4/F5/F6 are optional polish. Nothing blocks the entry on depth:verifiability grounds; coverage unaffected.
