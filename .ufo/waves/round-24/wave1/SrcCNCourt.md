# SrcCNCourt — source evidence for `chinese-criminal-thresholds-and-authorisation.md`

Seat: read-only scout. Item: open the three cited URLs and report, per URL, HTTP status, bytes,
presence of the cited article anchors, and the verbatim occurrence count of the four quoted
thresholds, then one verdict per source. I supply evidence only; admission is not my item.

## Findings (verdicts first)

| cited row | URL | status | bytes | cited anchor present | verdict |
|---|---|---|---|---|---|
| S044 | https://www.court.gov.cn/fabu/xiangqing/3085.html | GET 200 (HEAD 403, see F3) | 27296 | 第一条 ×1, 第二条 ×1, 第十一条 ×1 | **ADMISSIBLE** — openable, every cited article present, all four thresholds located in 第一条（一）–（四） |
| S045 | https://czt.ln.gov.cn/czt/attachDir/2026/05/2026050715041524122.pdf | GET 200 | 589780 (88 pp, text layer) | 第二百八十五条 ×1 (p.56), 第二百八十六条 ×2 (p.57: 286 and 286之一) | **ADMISSIBLE** — openable, both cited articles present and the quoted actus-reus wording matches |
| S046 | https://nj.jsjc.gov.cn/jianwu/zhinan/202109/t20210917_238200.shtml | GET 200 | 46093 | 四、法律适用规则 ×1, （一）准确界定非法侵入 ×1 | **ADMISSIBLE** — openable, section and quoted phrase present; exact-string check on the case number fails only because the page writes `检例第36 号` with an inserted space (F2) |

No source is FABRICATION-SUSPECT: in all three captures the cited article number and the quoted
substance are in the served bytes. No source is UNVERIFIABLE.

Capture metadata (2026-10-25T07:14:51Z, bodies in `/tmp/r24src/`, nothing written to
`/home/vgpnk/Projects/shokuknow`):

```
feec2516c916727cdb4dc8e6c4894c115a2f93be135e7ecf00acac992be078a1  ecd85a2f.body  S044  27296 B
bd10917c3dd0795dba952d34f473db50224013aa43ff325c30d4c49e67d1ed88  0e9426de.body  S045 589780 B
f28e084f09e1649ebfb68605e1fb3cde4f4554d39a40f07220dbb3d2c9a26360  7f394bce.body  S046  46093 B
```

Reproduction: `curl -sSL -o <body> -w '%{http_code} %{size_download}\n' <url>` (GET, not HEAD);
`pdftotext -enc UTF-8 0e9426de.body 0e9426de.txt` (243374 chars, text layer present);
HTML tag-stripped text written beside each body (`*.body.txt`).

## S044 — 最高人民法院/最高人民检察院 法释〔2011〕19号 (court.gov.cn/fabu/xiangqing/3085.html)

Observations, counted in both the raw HTML bytes and the tag-stripped text (identical counts):

| probe | raw-HTML hits | stripped-text lines |
|---|---|---|
| `第一条` | 1 | 93 |
| `第二条` | 1 | 104 |
| `第十一条` | 1 | 163 |
| `身份认证信息十组以上` | **1** | 95 — `（一）获取支付结算、证券交易、期货交易等网络金融服务的身份认证信息十组以上的；` |
| `五百组以上` | **1** | 96 — `（二）获取第（一）项以外的身份认证信息五百组以上的；` |
| `二十台以上` | 3 | 97, 123, 140 |
| `五千元以上` | 8 | 98, 115, 124, 142, 149, 156, 158, 159 |

The "exactly once" test, stated exactly:

- `身份认证信息十组以上` — exactly once. PASS.
- `五百组以上` — exactly once. PASS.
- `二十台以上` — **three** times, not once: 第一条（三）`非法控制计算机信息系统二十台以上的` (line 97),
  第四条（二）286 第一款/第二款 后果严重 (line 123), 第五条（二）286 第三款 后果严重 (line 140).
  The corpus-anchored compound `非法控制计算机信息系统二十台以上` is exactly once (line 97). The
  bare string is therefore not a safe unique key; the compound is.
- `五千元以上` — **eight** times, not once. `违法所得五千元以上` is 7 of them (98, 115, 124, 142,
  149, 156, 158); the 8th (line 159) reads `通过委托推广软件、投放广告等方式向其提供资金五千元以上的`.
  Only line 98 is the 第一条（四） 情节严重 threshold the entry quotes.

Article content check against the entry's prose:
- 第十一条 defines 计算机信息系统/计算机系统, 身份认证信息 (账号、口令、密码、数字证书) and 经济损失
  (含恢复数据、功能的必要费用) at line 163 — matches the entry's parenthetical exactly.
- 第一条 特别严重 is `数量或者数额达到前款第（一）项至第（四）项规定标准五倍以上的` (line 101) —
  matches "five times those thresholds". `五倍以上` appears 5× in the interpretation.
- Instrument identity: pass date `2011年6月20日` … `2011年7月11日`, `自2011年9月1日起施行`,
  `法释〔2011〕19号` are all present in the raw bytes but split across inline spans (F2).
- The article body is real page markup, not inside an HTML comment: `<!--`/`-->` counts are 38/38 and
  the comment blocks begin only after 第十一条's text, in the 相关报道 block.

## S045 — 中华人民共和国刑法(2023 修正), 第二百八十五条/第二百八十六条 (czt.ln.gov.cn PDF)

- 88 pages, PDF 1.7, text layer present (pdftotext yields 243374 chars), not a scan.
- Header: `中华人民共和国刑法(2023 修正)`, `发布部门 : 全国人大常委会`, `发布日期 : 2023-12-29`,
  `实施日期 : 2024-03-01`, `时效性 : 现行有效`, `效力级别 : 法律`.
- 第二百八十五条 at page 56: `违反国家规定，侵入国家事务、国防建设、尖端科学技术领域的计算机信息系统…三年以下`;
  paragraph 2 `侵入前款规定以外的计算机信息系统或者采用其他技术手段…情节严重…三年以下…情节特别严重…三年以上七年以下，并处罚金`;
  paragraph 3 `提供专门用于侵入、非法控制计算机信息系统的程序、工具…`; paragraph 4 单位犯前三款. The entry's
  description of all three paragraphs matches verbatim in substance.
- 第二百八十六条 at page 57: destruction offence, `后果严重…五年以下`, `后果特别严重…五年以上`, with 286之一
  (拒不履行信息网络安全管理义务罪) as the second hit.
- Entry's "no consent carve-out, no safe-harbour clause anywhere in the text" is consistent with a
  whole-text count over the extraction: `授权` 0, `安全港` 0, `免责` 0; `同意` 2, both in 第二百三十四条之一
  (未经本人同意摘取其器官) and unrelated to computer offences.
- Provenance caveat, not a defect of the quote: this is a WPS-generated republication
  (`Author: hyyd`, `Creator: WPS 文字`, `Last-Modified: Thu, 07 May 2026 07:04:15 GMT`, matching the
  filename stamp `20260507150415`) hosted by a provincial finance department, not an NPC primary text.
  The package already registers it at tier B for exactly this reason
  (`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` row 21).

## S046 — 南京市人民检察院 检务指南 (nj.jsjc.gov.cn)

| probe | raw-HTML hits | stripped-text lines |
|---|---|---|
| `四、法律适用规则` | 1 | 194 |
| `（一）准确界定非法侵入` | 1 | 196 |
| `未经授权或者他人同意` | **1** | 197 |
| `检例第36号` | **0** | — |
| `检例第36 号` (space) | 1 | 197 |
| `检例36号` | — | 205, 207 |
| `卫梦龙` / `龚旭` / `薛东东` | 1 each | 197 |

Located quotes (line 197): `侵入是指"未经授权或者他人同意"进入计算机信息系统。其表现形式既包括采用技术手段破坏或者
规避系统防护…也包括未取得被害人授权擅自进入…还包括超出被害人授权范围进入…` and
`检例第36 号指导性案例——卫梦龙、龚旭、薛东东非法获取计算机信息系统数据案中也已明确"超出授权范围使用账号、密码
登录计算机信息系统，属于侵入计算机信息系统的行为"。` Both sentences are exactly as the entry states
(`超出授权范围使用账号、密码登录` and `属于侵入计算机信息系统的行为` occur 2× each, because （三）准确认定破坏行为
repeats them at line 205).

Page metadata: title `【检务指南】危害计算机信息系统安全犯罪的司法认定_南京市人民检察院`; URL date stamp
`202109`/`20210917`; the only ISO date in the page text is `2021-09-17`.

## Cross-checks the refusal decision will need (evidence, not a verdict)

- F1 — recheck liveness for this entry: the entry's own `recheck:` line is prose, not a command.
  `grep -m1 '^recheck: ' …chinese-criminal-thresholds-and-authorisation.md` run through `bash` gives
  `/tmp/r24src/recheck.sh: line 1: syntax error near unexpected token '('` and **exit 2** — the same
  defect class C1 counter A reports for F01–F05. Only S044 is routed by that line; S045 and S046 have
  no recheck routing at all.
- F2 — exact-string recheck hazards in the captured bytes: S044 splits `法释〔2011〕19号` and
  `2011年6月20日` across inline `<span>`s (`〔2011〕19号` raw hits = 0, `2011年6月20日` raw hits = 0,
  vs 1 each in stripped text); S046 writes `检例第36 号` with a space (`检例第36号` = 0). Any future
  recheck must normalise tags/whitespace or key on the strings whose counts are listed above.
- F3 — method hazard: `curl -I https://www.court.gov.cn/fabu/xiangqing/3085.html` returns
  `HTTP/1.1 403 Forbidden` / `Content-Length: 150`, while repeated GETs return
  `http=200 bytes=27296` and a byte-identical body (`cmp` IDENTICAL). A HEAD-based recheck would
  false-negative this source; it must use GET.
- F4 — row numbering: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` holds S001–S031
  only (`grep -c '^| S[0-9]'` = 31, last row S031); it contains no S034 and no S044–S046. Those rows
  exist only in `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` (rows 10, 20, 21, 22).
  The entry's "(wave-1 row S034)" therefore resolves against the package addendum, not the lane.
- F5 — ground reference: the entry's `ground: F12 (extends F03…)`. The lane README's frontier table
  holds F01–F08 only (`corpus/README.md` lines 198–205); F12 appears in 8 package entries but no
  F-table exists in the package (no README.md there — only `MERGE-REPORT.md`, `SOURCES.append.md`,
  `knowledge/`). F12 is a forward reference that L1 must create or re-point.

## Remaining unknowns

- Whether S045 stays current: the PDF is a 2023-修正 compilation; a later 修正 would supersede it, and
  this seat did not compare it against an NPC-published text.
- Whether the package's Chinese entries beyond this one share S044–S046 (I opened only this entry's
  three URLs, per item scope).
