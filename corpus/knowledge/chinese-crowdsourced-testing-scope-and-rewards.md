# Chinese crowdsourced-testing platform scope and reward rules (CNVD 众测, 360SRC)

source: S049 — https://zc.cnvd.org.cn/news/helpList — 网络安全众测平台 使用手册, the answers to “提交漏洞时，若目标列表中没有当前目标，是否可以自行添加？” (L210-212), “平台是否接收互联网漏洞？” (L213-214), “测试过程中若目标没有发现漏洞，是否可以扩大测试范围？” (L409-410), “为什么我提交的高危漏洞被平台调整为中危漏洞？” (L207-208) and “漏洞的奖金如何确定？” (L418-419) in capture corpus/source-snapshots/round-32/S049.txt:207-214, 408-410, 419
source: S050 — https://security.360.cn/Reward/rules — 360SRC 外部漏洞处理和评分标准 V2.0 (2023.03.01), 一、适用范围 (L69-71), 三、漏洞奖励标准 1. 基础奖励标准 (L110-129), 八、漏洞审核原则 1. and 10. (L558-560, L591-593), 九、通用规定 (L594-611) in capture corpus/source-snapshots/round-32/S050.txt:69-71, 112, 113, 129, 418, 558, 591-593, 595-598, 601, 607, 611
verified-at: 2026-10-26
ground: F16
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050   # 14 assertions on the round-32 manifest (S049 Q1-Q8, S050 Q1-Q6), each `occurrences=1` under source-recheck.py's declared normalization; the strings marked hand-measured below are not manifest-bound; a captured-source comparison, not a fresh network verification

## Attribution

Two documents, each read as its own publisher's operating rules and nothing wider. S049 is the
使用手册 (user manual) of 网络安全众测平台, a crowdsourced-testing platform whose footer names
国家计算机网络应急技术处理协调中心 (CNCERT/CC) as rights holder and 北京数字观星科技有限公司 as
technical supporter (S049.txt:425-426). S050 is 360SRC 外部漏洞处理和评分标准 V2.0, effective
2023-03-01 (S050.txt:62, 68), published by 360 安全应急响应中心.

Every rule below is stated as that platform's own position — “the CNVD 众测 manual states…”,
“the 360SRC standard states…” (Q4). Neither document is treated as a rule for any other
platform, and neither is read as a legal authorization (see Honest limit).

## Claim 1 — the CNVD 众测 manual states that its intake is bounded by the customer's authorized project scope, not by the internet

The manual answers “平台是否接收互联网漏洞？” with a two-part rule — what it takes, and what it
refuses:

> 众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。
> — S049.txt:214 (使用手册 › “平台是否接收互联网漏洞？”)

In English: *the crowdsourced-testing platform accepts only security vulnerabilities inside the
test scope authorized by the customer, and does not accept internet vulnerabilities.* The same
answer redirects internet-wide findings to a different intake, the CNVD 漏洞共享平台
(`http://www.cnvd.org.cn/`, S049.txt:214) — so the 众测 platform states itself as a
per-customer project channel, distinct from the national sharing platform.

The second question bounds testing behaviour rather than intake:

> 测试项目范围以外的系统不在客户的授权范围内，所以是坚决不允许的。
> — S049.txt:410 (使用手册 › “测试过程中若目标没有发现漏洞，是否可以扩大测试范围？”)

In English: *systems outside the test project's scope are outside the customer's authorization,
so it is strictly not permitted.* The answer adds that testers must follow the project's
agreement to avoid disputes (S049.txt:410).

The manual also removes the one artefact a reader would take for a scope list. Asked whether a
missing target can be added by hand, it says:

> 漏洞提交页面的目标列表仅用于用户快速选择，并不是项目的测试范围约定
> — S049.txt:210-211 (使用手册 › “提交漏洞时，若目标列表中没有当前目标，是否可以自行添加？” at L210; the answer, quoted above, at L211)

and follows it with `注：请严格按照项目测试范围进行测试。` (S049.txt:212; manifest Q8). The
submission form's target picker is a convenience widget; the scope document is the project
agreement, which the manual does not reproduce.

## Claim 2 — the CNVD 众测 manual publishes no per-severity money table: payout follows the enterprise's rating and the project's rules

Severity is explicitly adjustable per project:

> 平台和企业在评价漏洞的风险等级时，会根据项目的规则、业务特点、影响范围等因素来调整漏洞的最终评级
> — S049.txt:208 (使用手册 › “为什么我提交的高危漏洞被平台调整为中危漏洞？”)

In English: *when the platform and the enterprise rate a vulnerability's risk level they adjust
the final rating according to the project's rules, the business's characteristics, impact scope
and other factors.* The same answer states the rating may move in either direction — high to
medium and medium to high (S049.txt:208).

Payout is a function of the enterprise's rating and the project rules:

> 平台将会根据企业对漏洞的评级，结合项目规则中的要求来为白帽发放奖金。
> — S049.txt:419 (使用手册 › “漏洞的奖金如何确定？”)

The manual states settlement timing separately — `用户提交漏洞所获得的奖金将会在项目结算的时候统一发放到用户的个人账户。`
(S049.txt:359, hand-measured) — and scores each finding by a multiplicative formula:

> 最终得分 = 四舍五入（有效性 × 漏洞等级 × 测试难度 × 危害程度 × 企业规模 × 报告质量）
> — S049.txt:132 (计算方法)

The page states the scoring twice at different granularity: its introduction names seven
evaluation aspects — 有效性、CVSS评分、数据敏感性及规模、测试难度、报告质量、测试目标企业的规模、附加分 —
opening `网络安全众测平台为每一个被确认的漏洞设计了积分评价机制` (S049.txt:72, hand-measured, 27
characters of the sentence's opening), while the printed formula multiplies six factors and the
block defines no 附加分 term (`grep -c 附加分` on the capture → `1`, the introduction at L72 only).
The formula is the version the page then works through with an example (the 评分实例 block at
S049.txt:134-142, whose table header the example rows follow). What
the manual never prints is a per-severity money table: `grep -c 安全币` on the capture is 0
(FC-5), while 奖金 appears 12 times.

Enforcement is stated on the platform's side. For projects routed through its trusted-testing
system, the manual states the audit purpose (`降低测试区间异常事件引发的法律风险`, S049.txt:408,
hand-measured) and the sanction:

> 对于未通过可信测试系统发现的问题平台有权取消或降低奖励。
> — S049.txt:408 (使用手册 › “对于要求通过可信测试系统进行测试的项目，是否可以直接进行测试？”)

## Claim 3 — the 360SRC standard states its own applicability: 360 Group products and businesses, plus named investees, with the asset list on a separate page

> 本标准适用于 360 集团发布的产品和业务
> — S050.txt:70 (一、适用范围, opening clause; the sentence continues on L71)

The continuation on L71 names the extension — `360 集团所投资的公司、子公司、合资公` … `司等也在收录范围内`
(hand-measured; the PDF text conversion breaks 合资公司 across the L70/L71 wrap, so the full
sentence does not bind as one recheck assertion) — and then defers the enumeration:
`具体范围可参考 https://security.360.cn/Product/product` (S050.txt:71, hand-measured).

So the applicable set is *group-published products and businesses + invested companies,
subsidiaries and joint ventures*, with the concrete list on a page this capture does not
contain. The standard also classifies business by importance:

> 360SRC 根据业务的重要程度分为核心业务、一般业务、边缘业务三类
> — S050.txt:113 (三、漏洞奖励标准 › 1. 基础奖励标准; hand-measured, `grep -c` on the capture → `1`)

## Claim 4 — the 360SRC standard states collection exclusions keyed to security-service coverage, not to a scope list

Rule 10 of 漏洞审核原则 excludes assets by service coverage, with a stated exception:

> 未纳入安全服务的资产一般情况下不收录相关漏洞
> — S050.txt:591 (八、漏洞审核原则 › 10.)

The rule continues by example — `1360.com` 等域名存在第三方厂商使用的资产或公有云上的资产 — and
allows collection when major harm affecting 360 Group business is shown (S050.txt:591-593). The
same principle is stated at the top of the section: `评分标准和漏洞奖励仅针对对 360 产品和业务有影响的漏洞`
(S050.txt:558, hand-measured), followed by the exclusion of 不再更新的产品 and 未纳入安全服务的控股业务
(S050.txt:559-560). `不予收录` occurs 6 times in the standard (FC-4).

## Claim 5 — the 360SRC standard states reward as a coefficient formula over its own business tiers and five rating levels

> 漏洞奖励=业务系数*基础安全币。
> — S050.txt:112 (三、漏洞奖励标准 › 1. 基础奖励标准)

The formula's two inputs are stated on the same page: the three business tiers with a per-tier
coefficient band (S050.txt:113, 119-124) and a base-安全币 table per vulnerability type and grade
(S050.txt:126-330). The reward unit is pegged:

> 漏洞安全币（安全币 ：RMB=1 : 5）
> — S050.txt:129 (【Web/服务端漏洞奖励】 heading; the label repeats at L159, 189, 219, 249, 274, 304 — hand-measured there)

The five grades are stated once, at the head of the grading section:

> 分为严重、高危、中危、低危、忽略五个等级
> — S050.txt:418 (grading section opener)

The standard also fixes the rating clock — 初评级后七个工作日内 we will 与业务沟通并进行漏洞最终定级
(S050.txt:99, hand-measured) — so 360SRC keeps a finding provisional until its own business
confirms the grade. The mechanism is not Claim 2's: S050 fixes an initial-rating and
confirmation clock inside the platform, while S049 has platform and enterprise re-rate an
already-submitted finding against the project's rules (S049.txt:208).

## Claim 6 — the 360SRC standard states report-hygiene and disclosure rules whose sanction is forfeiture

Two 通用规定 items govern where a report may live and when it may be published:

> 禁止将漏洞报告存放在互联网开放的云服务或共享文档中
> — S050.txt:595 (九、通用规定 › 1.; the sentence continues after the wrap: 如因此造成漏洞泄露的，对该漏洞不予奖励)

> 对提交漏洞报告后、未修复漏洞前，将漏洞报告公开或泄露的不予奖励。
> — S050.txt:597 (九、通用规定 › 2.)

Item 2 continues that 360SRC will treat private disclosure before a fix seriously, including
cancelling the reward (S050.txt:597-598, hand-measured), and item 3 closes the same paragraph
with `同时 360 保留采取进一步法律行动的权利。` (S050.txt:601, hand-measured). Two more exclusions sit
in the same section: 360 Group and affiliate employees do not participate in the reward
programme (S050.txt:607, hand-measured), and the standard reserves final interpretation to
360 信息安全部 (S050.txt:611, hand-measured).

The CNVD manual's nearest rule is about record-keeping, not forfeiture: it asks that requests
for more information go through the platform's review board rather than public groups or
one-to-one chat (`不建议在公开群组、或一对一聊天中询问此类信息`, S049.txt:414, hand-measured) — a
recommendation addressed to enterprises, with no sanction stated.

## Honest limit

Both documents state **scope boundaries and reward/collection rules**. Neither is a legal
authorization and neither carries a liability carve-out for a researcher:

- The CNVD 众测 manual states intake boundaries and a per-project agreement shown at enrollment
  (`系统将展示相关协议条款，仔细阅读并确认接受这些条款后`, S049.txt:200, hand-measured). The
  agreement itself is not in the capture, so nothing here records what a tester accepted. The
  manual's only legal-risk sentence is the platform's own rationale for its trusted-testing
  system (S049.txt:408), not a waiver.
- The 360SRC standard states duties on the researcher and reserves remedies: it requires
  compliance with 《中华人民共和国网络安全法》 and other law and reserves further legal action
  (S050.txt:601-604). It contains no 免责 or 安全港 wording in either capture (FC-6), and the
  phrase 授权测试 never appears in it (FC-6) — the standard talks about what it will pay for,
  not about what a reader is permitted to do.
- “In scope for 360SRC” cannot be derived from S050 alone: the enumerating list is the separate
  `https://security.360.cn/Product/product` page named at S050.txt:71 and not captured here.
- Both captures are page-level documents. The CNVD capture is a help/manual page whose
  navigation chrome is L1-22 and whose contact block is L420-426; the 360SRC capture is the PDF's
  extracted text (630 lines, tables flattened into single columns), so a table row's pairing of
  tier and coefficient is read from the printed order, not from cells.

Credential material: the CNVD 众测 page contains platform-issued VPN account/password retrieval
steps (S049.txt:202-205) and an OpenVPN client walkthrough for projects under third-party audit
(S049.txt:398-406). That material is **not reproduced** here — no account, password, profile or
certificate value appears in this entry, and none of those lines is quoted (Q6).

## Falsifiable checks

Run from the lane root; each prints the count stated here, so any claim above can be refuted
from the captures alone.

- **FC-1 — CNVD refuses internet-wide intake, once, in one sentence.** `grep -c '众测平台仅接收客户授权测试范围内的安全漏洞' corpus/source-snapshots/round-32/S049.txt` → `1`; `grep -c '不接受互联网漏洞' …S049.txt` → `1`. A capture whose answer omits the refusal, or states it twice for different scopes, falsifies Claim 1.
- **FC-2 — authorization is the customer's, and scope is the project's, at exactly two places.** `grep -c '授权' corpus/source-snapshots/round-32/S049.txt` → `2`, both inside `客户的授权范围` (L214, L410); `grep -c '并不是项目的测试范围约定' …S049.txt` → `1`; `grep -c '注：请严格按照项目测试范围进行测试。' …S049.txt` → `1`. A capture that treats the submission page's target list as the scope agreement fails FC-2.
- **FC-3 — 360SRC's applicability sentence is stated once and defers the list.** `grep -c '本标准适用于 360 集团发布的产品和业务' corpus/source-snapshots/round-32/S050.txt` → `1`; `grep -c '具体范围可参考 https://security.360.cn/Product/product' …S050.txt` → `1`. A reading that treats S050 itself as the asset enumeration fails FC-3.
- **FC-4 — collection is filtered by service coverage, repeatedly.** `grep -c '未纳入安全服务的资产一般情况下不收录相关漏洞' corpus/source-snapshots/round-32/S050.txt` → `1`; `grep -c '不予收录' …S050.txt` → `6`. A package claiming 360SRC collects every asset of a listed group company regardless of security-service coverage is unsupported.
- **FC-5 — the two platforms publish different reward instruments.** `grep -c '安全币' corpus/source-snapshots/round-32/S049.txt` → `0` versus `grep -c '安全币' corpus/source-snapshots/round-32/S050.txt` → `32`; `grep -c '奖金' …S049.txt` → `12`. Reading a 安全币 coefficient formula into the CNVD 众测 manual, or a per-project enterprise rating into 360SRC's payout, fails FC-5.
- **FC-6 — neither document grants authorization or safe harbor.** `grep -c -E '免责|安全港' corpus/source-snapshots/round-32/S049.txt` → `0` and `…/S050.txt` → `0`; `grep -c '授权测试' …/S050.txt` → `0`; `grep -c '同时 360 保留采取进一步法律行动的权利。' …/S050.txt` → `1`. Any entry that reads either document as permission or as a liability waiver is contradicted by these counts.

## Rejected over-generalizations

1. **“Registrable on a platform means its authorization authorizes testing anywhere.”** Rejected.
   The CNVD 众测 manual bounds intake to 客户授权测试范围 (S049.txt:214) and states that systems
   outside the project's scope are outside the customer's authorization and strictly not
   permitted (S049.txt:410). Platform registration is not a scope grant, and the manual's
   per-project agreement is where the terms sit (S049.txt:200).
2. **“The CNVD 众测 platform accepts internet-wide vulnerabilities because it lives on a
   zc.cnvd.org.cn domain.”** Rejected. The same answer refuses them and routes them to the
   CNVD 漏洞共享平台 instead (S049.txt:214) — the crowdsourced project channel and the national
   sharing platform are two different intakes on the platform's own telling.
3. **“The target list on the submission page is the scope agreement.”** Rejected. The manual
   says the list is only a quick-pick widget and not the project's test-scope agreement
   (S049.txt:211), then tells testers to follow the project scope strictly (S049.txt:212).
4. **“360SRC collects every in-scope asset regardless of the security-services clause.”
   Rejected.** 未纳入安全服务的资产 are generally not collected (S050.txt:591), the reward and
   scoring standard applies only to findings affecting 360 products and businesses
   (S050.txt:558), and 不予收录 appears 6 times (FC-4). The stated exception is a major-harm
   showing that affects 360 Group business (S050.txt:591-593), not a general override.
5. **“360SRC's five grades are its payout scale.”** Rejected. The grades label findings
   (S050.txt:418); the payout is 业务系数 × 基础安全币 (S050.txt:112) over per-type base tables
   and three business tiers, pegged 1 安全币 = 5 RMB (S050.txt:129). A grade alone does not fix a
   payment, and the same grade pays differently by business tier.
6. **“Either document authorizes the reader's testing, or shields the reader from liability.”**
   Rejected. Neither capture contains 免责 or 安全港 wording, the 360SRC standard never uses
   授权测试, and it reserves legal action (S050.txt:601-604, FC-6). Both documents state what
   the platform will accept and pay; lawfulness and authorization are elsewhere.
7. **“The two reward instruments can be compared on one money scale.”** Rejected. The CNVD 众测
   manual prices work only in withdrawals — `奖金的提取没有上限，下限为每笔提现申请不低于200元。`
   (S049.txt:356, hand-measured) — and prints no per-severity rate anywhere (FC-5), while
   360SRC fixes its own unit by the label `安全币 ：RMB=1 : 5` (S050.txt:129) over a coefficient
   formula (S050.txt:112). 安全币 converts to RMB; there is no printed CNVD rate to convert to,
   so “which platform pays more” cannot be built from these two captures.

## What this adds beyond F13 and F15

F13 (`corpus/knowledge/program-severity-ladders-and-reward-scales.md`, S043-S045) holds English-language
platform objects: a HackerOne policy record, the Bugcrowd VRT priorities, and the VRT's CWE
crosswalk. Its working rule is that each ladder is that platform's suggested baseline. F15
(`corpus/knowledge/vendor-third-party-finding-coordination.md`, S048) holds one vendor's research
programme as an intake route.

Three things here are not in either:

1. **A scope object that is a customer authorization, not a taxonomy or an asset list.** The
   CNVD 众测 manual defines intake per commissioned project, refuses internet-wide findings
   outright, and states that the submission page's target list is not the scope document
   (S049.txt:211-214, 410). In F13 the scope statement is a program's asset paragraph
   (“Issues affecting assets under HackerOne's control are in scope.”, S043.txt:31); here the
   boundary is the customer's authorization for one project.
2. **A platform asset register filtered by service coverage.** 360SRC's applicability sentence
   names group products and investees (S050.txt:70-71) and then excludes assets outside its
   security services (S050.txt:591), so an asset can belong to a covered group company and still
   fall outside collection. That is a different filter from F13's per-program asset paragraph and
   from F15's intake routes.
3. **Two reward instruments that do not reduce to a severity ladder.** The CNVD 众测 manual
   publishes no per-severity payout: the enterprise's rating plus project rules set the reward
   (S049.txt:419), ratings are adjustable per project (S049.txt:208), and 安全币 never appears
   (FC-5). The 360SRC standard does publish a coefficient formula and base tables, but its
   inputs are business tier and vulnerability type as well as grade (S050.txt:112, 113, 129,
   418). Neither can be read as “severity X pays Y” in the way F13's suggested-baseline ladders
   invite.

**One overlap named.** F13:32 holds the VRT's override — “application complexity, bounty brief
restrictions or unusual impact could result in a different rating.” — which moves a taxonomy
rating *before* submission, out of the program's brief; S049's adjustment happens *after* a
finding is submitted, re-rated by platform and enterprise against the project's rules
(S049.txt:208), so the two sit at sequential points in a workflow rather than stating one rule.
The S049 scoring formula quoted here was also held by the refused package entry
`chinese-program-severity-instrument.md`; what is re-claimed is the platform's own published
formula and its reward consequence, not that entry's ground — its CVSS 3.0 metric set (weights,
temporal metrics, exploitation factors) is not restated here: over the claim sections the CNVD
metric vocabulary appears exactly once,
`awk '/^## Attribution/{f=1} /^## What this adds/{f=0} f' corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md | grep -c -E 'CVSS|0.85|时效评价|利用代码'`
→ `1`, the seven-aspect quote in Claim 2.

## Scope and limits

- Pins read on 2026-10-26: `corpus/source-snapshots/round-32/S049.txt` (20272 B, 426 lines,
  sha256 `962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8`) and
  `corpus/source-snapshots/round-32/S050.txt` (31016 B, 630 lines, sha256
  `2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888`), bound by
  `corpus/source-snapshots/round-32/manifest.json` (sha256
  `6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774`).
- `verified-at: 2026-10-26` is when this entry was written and its quotes checked, not the
  capture instant (the round-32 capture commit is 2026-10-25T23:14:00-03:00). A separate seat
  re-read both URLs at 2026-10-26T04:16:06Z (S049) and 04:16:16Z (S050) and re-derived both
  captures byte for byte — 426/426 and 630/630 lines, 0 differing lines, sha256 equal to the pins
  above — recorded in `.ufo/waves/round-33/wave1/ScoutLiveDrift.md`. That is a two-hour-interval
  drift check on the extracted text: it says nothing about either page before the capture or
  after that fetch, and it did not compare the raw HTML/PDF bodies.
- The `recheck:` line verifies the pin and the exactly-once presence of fourteen quotes (eight
  for S049, six for S050) under `source-recheck.py`'s declared normalization (capture markup stripped, whitespace
  collapsed). It does not verify that the upstream pages still serve this text, and the 16
  strings marked *hand-measured* above are checked by the command or count printed beside them,
  not by the manifest.
- Documentation only: this entry records two platforms' published rules. It instructs no
  probing, scanning, login or submission against any target, quotes no credential material, and
  carries no session or private URL beyond the two public document URLs in its `source:` lines.
