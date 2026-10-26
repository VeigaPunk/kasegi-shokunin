# ExecRegistryAppend — round 33 receipt (S049/S050 registry append + Search-log note + R8 lines)

- Seat: `ExecRegistryAppend` (leaf). Round 33, wave 1. Lane base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; claims-freeze commit `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`.
- Answering model: `opencode-go/deepseek-v4.1-flash` (session route; no model passed to any tool).
- Write scope exercised: `corpus/SOURCES.md` only (6 added lines) + this receipt. Nothing else written in the lane; no git/jj mutation (read-only `git show`/`git rev-parse`/`git status` only); no network fetch by this seat; no tool installed or upgraded (python3 + coreutils + gawk only); no pacman transaction.
- Axes: depth:verifiability (C1 registry limb), coverage (C2 registry limb). No score move asserted.
- Ownership: `ConnOwnership` ruled the whole `corpus/SOURCES.md` (rows + Search log + R8) to this seat; `ScribeSearchLog` (second claimant) was told the bullet was already landed by me and applied no duplicate.

## 0. Gates waited for

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-33/wave1
$ for f in ExecEntryF16.md ExecCensusDry.md ScoutF16Sweep.md ScoutPackageThemes.md; do until [ -s "$f" ]; do sleep 20; done; echo "READY $f"; done
```

| Dependency | What it gates | Verdict taken |
|---|---|---|
| `wave1/ExecEntryF16.md` | the F16 entry the rows' `used-by` cell must resolve | landed `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`, 278 lines, sha256 `8d209995ec5af1129fab2238cb92dbba2fd68700dbeabd5c05d921f50669d08c`; its `source:` lines name S049 and S050; `grep -lE '^source: S049 '` → 1 and `S050` → 1 |
| `wave1/ExecCensusDry.md` | pre-append mirror census on the planned row shape | **PASS**: mirror `validate --file` exit 0, only base W04 S028/S029; E03/E04 negative controls exit 1; projection rows=50, mined=38, A=47/B=1/C=2, invalid=0, missing=0 |
| `wave1/ScoutF16Sweep.md` | the Search-log note's sweep counts and residual verdict | 12-term sweep; `residual-exists`; lane holds zero CNVD 众测 / 360SRC platform ground except a refusal note at `program-severity-ladders-and-reward-scales.md:64`; 44 knowledge files (**PRE-STATE**, its own label) |
| `wave1/ScoutPackageThemes.md` + `wave1/ScoutLiveDrift.md` | the note's identified/screened/included/excluded counts and the fetch provenance | 9-row verdict table (2 admits by document + 7 re-refused staged entries); staged S034/S035 URLs byte-equal to lane S049/S050; live re-fetch 2026-10-26T04:16Z, text byte-identical to the round-32 captures (0 differing lines) |

## 1. PRE-STATE (labelled: measured before this seat wrote anything)

```
$ sha256sum corpus/SOURCES.md
5a03c696312bd5fd8fe8307f75bd9723cac97fe3e44f0f3ba46a68607295f6f5  corpus/SOURCES.md
$ git show 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4:corpus/SOURCES.md | sha256sum
5a03c696312bd5fd8fe8307f75bd9723cac97fe3e44f0f3ba46a68607295f6f5  -
$ git status --porcelain corpus/SOURCES.md          → (no output: clean at base)
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
48
$ grep -n "^## " corpus/SOURCES.md
3:## Registry   56:## Paths   63:## Search log   74:## Leads (unopened)   80:## Registry changes
$ grep -n "^Change cell old" corpus/SOURCES.md → 87
```

The live registry was byte-identical to the lane base blob at my first read, so the before→after below is a real
measurement on quiescent bytes.

## 2. The two landed rows (lines 55-56, directly after the S048 row at line 54)

```
$ for n in 55 56; do sed -n "${n}p" corpus/SOURCES.md > row$n.txt; echo "row$n bytes=$(wc -c < row$n.txt) sha256=$(sha256sum row$n.txt | cut -d' ' -f1) pipes=$(tr -cd '|' < row$n.txt | wc -c)"; done
row55 bytes=1145 sha256=dde2d9b9c96f9174b36695e6c7feebb73b06104ef0a69ebbaf26947f0c0cd88a pipes=12
row56 bytes=1380 sha256=a593b27331a3b8adc96f9e0be0dbb02b3b925f12bb02fce2dd0ef4e207fd20fa pipes=12
```

12 pipes = the leading and trailing delimiter plus the 10 separators between the 11 cells, so NF=13 after splitting on `|`; no `|` inside any cell. Cells read back by this seat:

```
$ awk -F'|' 'NR==55{for(i=2;i<=12;i++){c=$i; gsub(/^ +| +$/,"",c); printf "c%d=[%s]\n", i-1, c}}' corpus/SOURCES.md
c1=[S049]
c2=[网络安全众测平台帮助 - CNVD — https://zc.cnvd.org.cn/news/helpList]
c3=[docs]
c4=[A]
c5=[CNVD's own help-page statements for the 网络安全众测 platform: its scoring model and the boundary of the testing it accepts]
c6=[capture corpus/source-snapshots/round-32/S049.txt: 帮助 nav L7 and 漏洞评分标准 nav L10, CVSS arithmetic 评分计算方法 L52, 网络安全众测平台评分标准简介 L71 with the seven-aspect sentence L72, 计算方法 heading L131 with the 最终得分 formula L132, 评分实例 L134-135, rating-change FAQ L207-209, target-list caveat L210-212, internet-vulnerability refusal L213-214, 扩大测试范围 refusal L409-410, footer 版权所有 © 2018-2026 国家计算机网络应急技术处理协调中心 L425]
c7=[CNVD's platform states its own intake boundary — only findings inside the client-authorised project scope are accepted (L214, L410) — and scores a finding as the product of the factors in its 最终得分 formula (L132), with a project's own rules able to move the grade (L208)]
c8=[mined]   c9=[2026-10-26]   c10=[90d]
c11=[corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md]

$ awk -F'|' 'NR==56{...}' corpus/SOURCES.md
c1=[S050]
c2=[360SRC 外部漏洞处理和评分标准 V2.0 — https://security.360.cn/Reward/rules]
c3=[docs]
c4=[A]
c5=[360SRC's own handling and scoring standard: its applicability clause, report-template requirement, review and grading clocks, reward formula and intake rules]
c6=[capture corpus/source-snapshots/round-32/S050.txt: 编写人 360 安全应急响应中心 L3, 版本号 V2.0 L5, 实施日期 2023 年 3 月 1 日 L7, 一、适用范围 L69-71 (the sentence wraps across L70-L71), 二、威胁反馈与处理流程 1. 漏洞报告模板 L73 with the 仅从理论层面说明漏洞的存在而无利用和复现过程将不予收录 sentence L86-L87, 2. 漏洞审核 L90-92, 4. 漏洞定级 L98-100, 三、漏洞奖励标准 漏洞奖励=业务系数*基础安全币 L112 with the 业务系数 table L118-125 and the 安全币 RMB ratio line L129, 七、漏洞定级标准 five grades L418-L419, 八、漏洞审核原则 item 1 L557-560, 九、通用规定 items 1-2 L595-598]
c7=[360SRC states its own two-sided boundary — the standard applies to the products and businesses 360 publishes (L70-L71) with unlisted assets generally not collected (L591-L593), and a report that only asserts a theoretical vulnerability with no exploitation or reproduction is not collected (L86-L87)]
c8=[mined]   c9=[2026-10-26]   c10=[180d]
c11=[corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md]
```

Both `c2` cells carry the record URL as their trailing `https://` token, one token per cell, byte-equal to the
round-32 manifest `url` fields (`8ae60ea05f179aa3…` / `642ebcc3378386df…`), which is what C1 rule B reads. The
source text keeps the item's wording (`网络安全众测平台帮助 - CNVD`).

## 3. Anchor verification — every cited line printed from the committed capture

```
$ awk 'NR==7||NR==10||NR==52||NR==71||NR==72||NR==131||NR==132||NR==134||NR==207||NR==210||NR==213||NR==214||NR==409||NR==410||NR==425 {printf "S049:%d %s\n", NR, substr($0,1,46)}' corpus/source-snapshots/round-32/S049.txt
S049:7 帮助
S049:10 漏洞评分标准
S049:52 评分计算方法
S049:71 网络安全众测平台评分标准简介
S049:72 网络安全众测平台为每一个被确认的漏洞设计了积分评价机制，白帽通过提交漏洞所获得的积分形成白帽
S049:131 计算方法
S049:132 最终得分 = 四舍五入（有效性 × 漏洞等级 × 测试难度 × 危害程度 × 企业规模 × 
S049:134 评分实例
S049:207 为什么我提交的高危漏洞被平台调整为中危漏洞？
S049:210 提交漏洞时，若目标列表中没有当前目标，是否可以自行添加？
S049:213 平台是否接收互联网漏洞？
S049:214 众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。互联网漏洞建议到CNVD漏洞共
S049:409 测试过程中若目标没有发现漏洞，是否可以扩大测试范围？
S049:410 测试项目范围以外的系统不在客户的授权范围内，所以是坚决不允许的。测试人员必须严格遵守项目中的
S049:425 版权所有 © 2018-2026 国家计算机网络应急技术处理协调中心 京ICP备100124

$ awk 'NR==3||NR==5||NR==7||NR==69||NR==70||NR==71||NR==73||NR==86||NR==87||NR==90||NR==98||NR==112||NR==118||NR==129||NR==418||NR==557||NR==558||NR==591||NR==595 {printf "S050:%d %s\n", NR, substr($0,1,40)}' corpus/source-snapshots/round-32/S050.txt
S050:3 360 安全应急响应中心
S050:5 V2.0
S050:7 2023 年 3 月 1 日
S050:69 一、适用范围
S050:70 本标准适用于 360 集团发布的产品和业务，此外 360 集团所投资的公司、子公
S050:71 司等也在收录范围内，具体范围可参考 https://security.360.c
S050:73 1. 漏洞报告模板
S050:86 利用条件可尽量截图说明，仅从理论层面说明漏洞的存在而无利用和复现过程将不
S050:87 予收录。（例如扫描报告、请求头配置等）
S050:90 2. 漏洞审核
S050:98 4. 漏洞定级
S050:112 漏洞奖励=业务系数*基础安全币。
S050:118 【业务系数】
S050:129 漏洞安全币（安全币 ：RMB=1 : 5）
S050:418 根据漏洞对业务产生的危害，分为严重、高危、中危、低危、忽略五个等级。收录的基本原
S050:557 八、漏洞审核原则
S050:558 1、评分标准和漏洞奖励仅针对对 360 产品和业务有影响的漏洞。360 的产品或
S050:591 10、未纳入安全服务的资产一般情况下不收录相关漏洞，例如 1360.com 等域
S050:595 1、禁止将漏洞报告存放在互联网开放的云服务或共享文档中，如因此造成漏洞泄露的，对
```

The `L70-L71` wrap note in the S050 anchor cell is the measured quirk (`S050:70` ends mid-word and `S050:71`
continues with `司等也在收录范围内`), so the applicability sentence is cited as a range, not as one assertion.
No cell quotes any string over 25 words; the two long cells are paraphrase plus line locators, not quotes.

## 4. The Search-log note (last bullet of `## Search log`, now line 75)

```
- Chinese crowdsourced-testing platform scope and reward rules sweep (round 33); question: does the lane already hold the CNVD 众测 help-page scope and scoring ground or the 360SRC V2.0 handling rules, and do the two staged rows add ground the F13–F15 entries do not; where: read-only the campaign package `/home/vgpnk/Projects/shokuknow/merge/kasegi/` (`SOURCES.append.md` with 94 staged source rows, its staged entries and `MERGE-REPORT.json`), a twelve-term negative sweep over the lane's own `corpus/knowledge/*.md` (44 files before the F16 entry landed — PRE-STATE for S049/S050, labelled in `wave1/ScoutF16Sweep.md`; 45 after), `corpus/README.md`, `corpus/SOURCES.md` and `SKILL.md`, and the two public documentation URLs re-fetched under the instrument UA on 2026-10-26T04:16Z (S049 HTTP 200, 56,674 B; S050 HTTP 200, 427,391 B; both text conversions byte-identical to the committed captures, 0 differing lines — `wave1/ScoutLiveDrift.md`), whose committed captures are `corpus/source-snapshots/round-32/S049.txt` and `S050.txt`; date: 2026-10-26; identified 9 items (the 9 rows of `wave1/ScoutPackageThemes.md`'s verdict table: 2 staged source rows that join the lane by URL — S034 and S035 — out of the 94, plus the 7 staged entries re-gated), screened 9, included 2, excluded 7. Included: … Excluded, with reason: … Stop: the bounded package set plus the two committed captures answered the F16 question and supplied the located quotes; no wider target-facing research was run and no other staged entry was carried.
```

Every count is a peer receipt's measured count, not a re-derivation: `ScoutPackageThemes.md`'s 9-row verdict
table (2 admits by document + 7 rejects) supplies identified/screened/include/exclude; `ScoutF16Sweep.md`
supplies the 44-file PRE-STATE sweep and the `residual-exists` verdict; `ScoutLiveDrift.md` supplies the
re-fetch bytes and the 0-differing-lines result. The two URLs are named once in the registry (in their rows),
so this bullet identifies them by capture path to keep rule B's per-row token unique.

**Peer corrections applied to this bullet (both from `ScribeSearchLog`; recorded here as asked).** Option (b),
one bullet, no second writer:

| # | defect | fix landed |
|---|---|---|
| 1 | false claim "no target was re-fetched this round" | replaced with the measured re-fetch clause (`ScoutLiveDrift.md`: 04:16:06Z/04:16:16Z, HTTP 200, 56,674 B / 427,391 B, text byte-identical, 0 differing lines) |
| 2 | unlabelled PRE-STATE count "44 files" | now "(44 files before the F16 entry landed — PRE-STATE for S049/S050, labelled in `wave1/ScoutF16Sweep.md`; 45 after)" |

I did **not** adopt the 11/11/2/9 framing from that peer's first message: it measures a different set (the 9 of
67 staged entries whose bytes match the theme grep, including two same-name twins already landed as F13/F14).
I measured that grep myself (`grep -l -E 'zc\.cnvd\.org\.cn|security\.360\.cn|360SRC|众测' merge/kasegi/knowledge/corpus/knowledge/*.md | wc -l`
→ 9 of 67) and kept it out of the note's counts to avoid conflating two denominators.

## 5. The R8 lines (appended last in `## Registry changes`, now lines 98-100)

```
- S049 row added: new row (id `S049`, kind `docs`, tier A scoped to CNVD's own 网络安全众测 help-page statements, status mined, opened 2026-10-26, recheck `90d`, used-by `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`), anchor pinned to the round-32 capture `corpus/source-snapshots/round-32/S049.txt` (帮助 nav L7, 漏洞评分标准 nav L10, 评分计算方法 L52, 评分标准简介 L71 with the seven-aspect sentence L72, 计算方法 L131 with the 最终得分 formula L132, 评分实例 L134-135, rating-change FAQ L207-209, target-list caveat L210-212, internet-vulnerability refusal L213-214, 扩大测试范围 refusal L409-410, footer L425; the page shows no visible publication or revision date). Staged `SOURCES.append.md` S034 cells → landed: `opened 2026-10-23` → `2026-10-26`; `anchor` rewritten from the round-32 capture, the staged prose anchor (page images dated 2025-03) not carried; `scope` and `teaches` rewritten to the registry's cell shape and to name CNVD's platform as the stating party (Q4), the staged factor list not carried verbatim; `used-by` (four staged paths: `program-scope-rules-and-asset-boundaries.md`, `program-severity-ladders-and-reward-scales.md`, `claim-packaging-and-report-quality.md`, `chinese-program-severity-instrument.md` — none of which is in the lane) → the F16 entry only. Mapped by DOCUMENT, not by id (URL byte-equal at 36 bytes).
- S050 row added: new row (id `S050`, kind `docs`, tier A scoped to 360SRC's own handling and scoring standard, status mined, opened 2026-10-26, recheck `180d`, used-by `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`), anchor pinned to the round-32 capture `corpus/source-snapshots/round-32/S050.txt` (…). Staged `SOURCES.append.md` S035 cells → landed: `kind spec` → `docs` (the capture is the PDF's converted text, read as its publisher's documentation); `opened 2026-10-23` → `2026-10-26`; `anchor` rewritten from the round-32 capture, the staged page-level anchor not carried; `teaches` rewritten to name 360SRC as the stating party (Q4) and to quote no string over 25 words; `used-by` (`program-scope-rules-and-asset-boundaries.md`, `claim-packaging-and-report-quality.md` — both outside the lane) → the F16 entry only. Mapped by DOCUMENT, not by id: the package's own `S049`/`S050` are the JVN documents lane S046/S047.
- No status/recheck/used-by cell changed on any pre-existing row; S001–S048 untouched (logged). Registry 48 rows pre-append → 50 post-append (R8).
```

Staged cells were read, not remembered: `awk -F'|' '/^\| S034 /{print "kind="$4" opened="$10" recheck="$11" usedby="$12}'`

```
S034 kind= docs  status= mined  opened= 2026-10-23  recheck= 90d  usedby= corpus/knowledge/program-scope-rules-and-asset-boundaries.md, corpus/knowledge/program-severity-ladders-and-reward-scales.md, corpus/knowledge/claim-packaging-and-report-quality.md, corpus/knowledge/chinese-program-severity-instrument.md
S035 kind= spec  status= mined  opened= 2026-10-23  recheck= 180d  usedby= corpus/knowledge/program-scope-rules-and-asset-boundaries.md, corpus/knowledge/claim-packaging-and-report-quality.md
```

## 6. POST-STATE — the target command and the contract census

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

Byte-identical to the PRE run in §1: only the two base W04 warnings, no E-code and no new W-code from either row.

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md            → rows=50
$ awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md → malformed=0
$ ... id extraction | sort | uniq -d                                              → dups= (none)
$ ... tier/status/kind enum sweep | wc -l                                         → enum_violations=0
$ ... mined used-by paths | [ -e "$p" ] loop | wc -l                              → missing_usedby=0
$ grep -cE '^\|[[:space:]]*S049[[:space:]]*\|' corpus/SOURCES.md                   → 1
$ grep -cE '^\|[[:space:]]*S050[[:space:]]*\|' corpus/SOURCES.md                   → 1
$ ... tier histogram                                                              → tier=A=47 B=1 C=2
$ ... status histogram                                                            → status=mined=38 queued=9 rejected=3
$ sha256sum corpus/SOURCES.md
b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b  corpus/SOURCES.md
```

48 → 50 rows, mined 36 → 38, tier.A 45 → 47 — the three C2 registry figures, and the same projection the
`ExecCensusDry` mirror predicted before the write.

## 7. Cross-checks against the two claims (read-only instruments, run by this seat)

```
$ python3 corpus/instruments/capture-binding-check.py           # C1 rule B on my rows
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
binding_exit=0

$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049
S049:sha256 OK … S049:Q8 OK occurrences=1                                → recheck49_exit=0  (8 assertions)
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050
S050:sha256 OK … S050:Q6 OK occurrences=1 (tail)                         → recheck50_exit=0
```

`multi_row_url=2` is the instrument's informational count of the registry's pre-existing duplicate-URL pairs
(S006/S028, S024/S029) — documented as not a failure in the instrument's own header; no record of mine is in
it, and both my URLs occur once in the whole registry (`grep -cF` of each URL in `corpus/SOURCES.md` → 1).

These are C1/C2 counter commands, not my deliverable: the L1 owns the post-wave gate run on quiescent bytes.

## 8. R6 disclosure — which cited line numbers moved, measured before and after

| citation | base `690b69d` | now | effect |
|---|---|---|---|
| row-level cites `SOURCES.md:22`, `:46`, `:47`, `:48`, `:54` (rounds 25, 28, 31 lessons) | 22 / 46 / 47 / 48 / 54 | same | unchanged — both rows land below `:54` |
| `## Paths` | 56 | 58 | +2 (two row lines) |
| `## Search log` / the round-31 sweep line (`SOURCES.md:72`) | 63 / 72 | 65 / 74 | +2 |
| `## Leads (unopened)` | 74 | 77 | +3 (rows + Search-log bullet) |
| `## Registry changes` | 80 | 83 | +3 |
| the S043 change-cell line (`round-29.md:214`, `round-29-verifier-spotcheck.md:74` cite `SOURCES.md:83`) | 87 | 90 | the stale `:83` trail (M31-3, already +4) is now +7 |

The rows must sit inside `## Registry` (census E12 fires on a row-shaped source outside it) and the note must
sit inside `## Search log`, so the shift is structural, not avoidable by placement. The correction to those
lesson citations belongs to `corpus/lessons/**` (M31-3 is already routed and open), not to this seat.

## 9. The edit is a pure addition, and the scratch dir is gone

```
$ git show 690b69da:corpus/SOURCES.md > base-sources.md
$ diff base-sources.md corpus/SOURCES.md | grep -c '^>'   → 6    (2 rows, 1 Search-log bullet, 3 R8 lines)
$ diff base-sources.md corpus/SOURCES.md | grep -c '^<'   → 0    (nothing removed or modified)
$ wc -l base-sources.md corpus/SOURCES.md                 → 94 / 100
$ tail -c 3 corpus/SOURCES.md | od -An -c                 → `) . \n`   (single trailing newline, no blank EOF line)
```

Scratch: `$HYAKU_SCRATCH/kasegi-r33/ExecRegistryAppend/` (default `/fast/scratch/hyaku`) held `base-sources.md`
and `row55.txt`/`row56.txt`; the outputs are copied into this receipt above and the directory is removed before
yield (`rm -rf -- "$S"`, verified). No tree left on disk by this seat.

## 10. Risks and blockers

- No blockers; nothing left undone in scope.
- Risk (inherited, routed): the R6 line shift above deepens the M31-3 staleness of two `corpus/lessons/round-29*`
  citations. Fix belongs to the lesson owner; a registry seat cannot edit lessons.
- Risk (content, not mine to close): the S049 page carries platform-issued tester VPN account/password
  instructions at capture lines 205-206. Bound 8 / Q6: nothing here or in the rows quotes, copies or points at
  credential material — the anchor cell cites section names and unrelated line numbers only.
- Suggested L1 gate on these bytes: `sources-census.sh validate` (expect exit 0 + W04 S028/S029),
  `capture-binding-check.py` (expect `records=40 bound=40 unbound=0`), both `source-recheck.py` runs.
