# ExecCensusDry — scratch registry validation before the S049/S050 append (round 33)

Seat: ExecCensusDry (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Receipt dir: `.ufo/waves/round-33/wave1/`.
Scratch: `$HYAKU_SCRATCH/kasegi-r33/ExecCensusDry/` (default `/fast/scratch/hyaku`), deleted before yield;
every output below was copied into this receipt first.

## What this validates

A byte-mirror of `corpus/` with the planned S049/S050 rows inserted after the S048 row, so the fleet census
validator sees the post-append registry before `corpus/SOURCES.md` is touched:

- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md`
- the 0–3-space id-collision extractor re-run over the live registry and the staged package, compared
  byte-for-byte with `.ufo/waves/round-33/assimilation/{reg-ids,staged-ids,collisions}`
- staged S034/S035 URL bytes vs the lane S049/S050 URL bytes

Inputs read (absolute): `.ufo/waves/round-33/claims.json`, `corpus/SOURCES.md`, `corpus/knowledge/`,
`corpus/instruments/`, `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`,
`corpus/source-snapshots/round-32/{S049,S050}.txt`, `.ufo/waves/round-33/assimilation/*`, and
`.ufo/waves/round-33/wave1-spec.json` (the ExecRegistryAppend item is the row plan). `ScoutManifestAudit` and
`ScoutPackageThemes` had published nothing when this seat drafted the rows, so the draft derives from
committed bytes — staged package rows, round-32 captures and the frozen row plan — not from their reports.
`ScoutF16Sweep.md` landed afterwards and independently maps staged S034→lane S049 (helpList) and staged
S035→lane S050 (360SRC rules) by document, with the same capture anchors used here (its §3: formula
`S049.txt:132`, SLA `S050.txt:91-92`, final grading `S050.txt:99`, reward formula `S050.txt:112`).

## Mirror build

```
S=/fast/scratch/hyaku/kasegi-r33/ExecCensusDry
mkdir -p "$S/validate"
cp -a /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus "$S/validate/corpus"     # 3.6M
printf '%s\n' 'PLACEHOLDER — F16 entry path ...' \
  > "$S/validate/corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md"
# python3: the two planned rows are inserted immediately after the `| S048 |` line
```

The placeholder exists only so census `usedby_findings()` (E11) resolves
`corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` inside the mirror; the real entry belongs
to ExecEntryF16.

Lane state at copy time (read-only git):

```
## LANE STATE AT MIRROR COPY (read-only)
head=53bfa59ff3fa578818e7e5db04fe60e80ed1eb6f
no tracked change to SOURCES.md, corpus/knowledge/ or corpus/README.md
sources_md_sha256=5a03c696312bd5fd8fe8307f75bd9723cac97fe3e44f0f3ba46a68607295f6f5
readme_sha256=d9865b2e126c626559de9704d9e8d636b6f4ce7eba2a3a74e6f32d92b2146f98
```

## Gate — base mirror (no S049/S050), then with the planned rows

```
## BASE MIRROR validate (mirror of live registry, no S049/S050)
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r33/ExecCensusDry/validate/corpus/SOURCES.md
base_validate_exit=0
```

```
## MIRROR validate after S049/S050 append
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r33/ExecCensusDry/validate/corpus/SOURCES.md
mirror_validate_exit=0
```

Exit 0 in both runs; the only findings are the two base warnings (W04 S028/S029) already frozen in
`claims.json`. The append adds no E-code and no new W-code.

Projection census on the same mirror (mirror projection, not the live registry):

```
## MIRROR census (projection, not live)
file	rows	50
file	tier.A	47
file	tier.B	1
file	tier.C	2
file	status.mined	38
file	status.queued	9
file	status.rejected	3
FLEET	rows	50
FLEET	tier.A	47
FLEET	tier.B	1
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	9
FLEET	status.mined	38
FLEET	status.rejected	3
FLEET	status.invalid	0
FLEET	missing	0
mirror_census_exit=0
```

## Planned rows as validated (11 inner cells, pipe count 12 → NF = 13)

```
| S049 | 网络安全众测平台帮助 - CNVD — https://zc.cnvd.org.cn/news/helpList | docs | A | CNVD's own 众测 platform help page: its authorised-testing scope rule, its seven-factor composite score and its FAQ answers on rating changes and scope | capture corpus/source-snapshots/round-32/S049.txt: 帮助 nav L7, 漏洞评分标准 L10, 评分计算方法 L52, 网络安全众测平台评分标准简介 L72, 评价指标说明 L73, 计算方法 heading L131 and formula L132, rating-change FAQ L207-L209, target-list caveat L210-L212, scope rule L214, 扩大测试范围 FAQ L409-L410, footer L425 | CNVD's 众测 platform multiplies validity, CVSS band, test difficulty, impact, target size and report quality into one score, and it accepts only findings inside the client-authorised project scope | mined | 2026-10-26 | 90d | corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md |
| S050 | 360SRC 外部漏洞处理和评分标准 V2.0 — https://security.360.cn/Reward/rules | docs | A | 360SRC's own published handling and scoring standard: its 适用范围, report template, triage and grading clocks, its 安全币 reward scale and its five-level grading rule | capture corpus/source-snapshots/round-32/S050.txt: 版本号 V2.0 and 实施日期 2023 年 3 月 1 日 L5-L7, 二、威胁反馈与处理流程 L26-L32, 一、适用范围 L70-L72, 1. 漏洞报告模板 L73, 漏洞证明 sentence L85-L87, 2. 漏洞审核 L90-L92, 4. 漏洞定级 L98-L100, 5. 安全币发放 L101-L105, 漏洞奖励=业务系数*基础安全币 L112, 安全币：RMB=1:5 L129, 严重/高危/中危/低危/忽略 L418 | 360SRC pays a business coefficient times base 安全币 and rejects a report that states only a theoretical vulnerability with no exploitation or reproduction | mined | 2026-10-26 | 180d | corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md |
```

```
## MIRROR ROW SHAPE (inner cells only)
S049: pipe_count=12 NF=13 inner_cells=11 all_nonempty=True any_pipe=False kind=docs tier=A status=mined opened=2026-10-26 recheck=90d usedby=corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
S050: pipe_count=12 NF=13 inner_cells=11 all_nonempty=True any_pipe=False kind=docs tier=A status=mined opened=2026-10-26 recheck=180d usedby=corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
```

## Id-collision extractor (0–3-space pattern) vs the frozen assimilation artefacts

```
$ extract() { grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$1" | grep -oE 'S[0-9]{3,}' | sort -u; }
$ extract /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md > extract-reg-ids
$ extract /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md > extract-staged-ids
$ comm -12 extract-reg-ids extract-staged-ids > extract-collisions
## ID-CORRUPTION EXTRACTOR (^ {0,3}\|[[:space:]]*S[0-9]{3,}) — live registry vs staged package
live_registry_ids=48 first=S001 last=S048
staged_append_ids=94 first=S031 last=S124
collisions=18
reg-ids: BYTE-EQUAL (240 bytes)
staged-ids: BYTE-EQUAL (470 bytes)
collisions: BYTE-EQUAL (90 bytes)
3-space-indented row caught by 0-3-space pattern: S999
3-space-indented row caught by column-0-only pattern: 0
```

`reg-ids`, `staged-ids` and `collisions` reproduce the frozen files byte-for-byte, and the sensitivity probe
reproduces `guard-proof.txt`: a 3-space-indented row is caught by the 0–3-space pattern (`S999`) and missed by
a column-0-only pattern (0 matches).

Mirror id set after the planned append (each planned id appears once):

```
## id rows in mirror registry (0-3-space pattern, id token, sorted unique)
S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S016 S017 S018 S019 S020 S021 S022 S023 S024 S025 S026 S027 S028 S029 S030 S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 
mirror_id_count=50
S049_rows=1
S050_rows=1
```

## Staged → lane URL byte equality (mapped by document)

```
## URL BYTE-EQUALITY (staged package row cell vs lane planned row cell)
staged S034 = 'https://zc.cnvd.org.cn/news/helpList' len=36
lane   S049 = 'https://zc.cnvd.org.cn/news/helpList' len=36
  byte_equal=True
staged S035 = 'https://security.360.cn/Reward/rules' len=36
lane   S050 = 'https://security.360.cn/Reward/rules' len=36
  byte_equal=True
```

Renumber map (**by document, never by id**): staged `S034` → lane `S049` (CNVD 众测 helpList),
staged `S035` → lane `S050` (360SRC rules). Both staged numbers are already taken in the live registry by
different documents:

```
## ID-COLLISION TRAP — live lane rows occupying the staged numbers
live S034 = 'https://www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/'   (staged S034 = 'https://zc.cnvd.org.cn/news/helpList')
live S035 = 'https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf'   (staged S035 = 'https://security.360.cn/Reward/rules')
live S049 present: False | live S050 present: False
```

Second trap — the package's own `S049`/`S050` numbers are the JVN documents already landed as lane S046/S047,
so following package ids would duplicate landed rows:

```
## SECOND TRAP — package staged S049/S050 are the JVN documents already landed as lane S046/S047
staged S049 = https://www.ipa.go.jp/security/reports/vuln/jvn/ug65p90000019ev2-att/000095610.pdf
live   S046 = https://www.ipa.go.jp/security/reports/vuln/jvn/ug65p90000019ev2-att/000095610.pdf
  byte_equal=True
staged S050 = https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html
live   S047 = https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html
  byte_equal=True
```

New-URL absence in the live registry before the append:

```
## NEW-URL ABSENCE IN LIVE REGISTRY (pre-append)
https://zc.cnvd.org.cn/news/helpList occurrences_in_live_registry=0
https://security.360.cn/Reward/rules occurrences_in_live_registry=0
```

## Negative controls — the gate refuses a colliding id and a duplicate URL within scope

Each control lives under its own `corpus/` parent (`--file` derives the E11 root from it) with a symlink to the
mirror `knowledge/`, so the injected mutation is the only difference from the passing mirror. An earlier
attempt at these controls ran the mutant files outside a `corpus/` parent and produced a spurious E11 flood;
that run is superseded and is not cited.

```
## NEGATIVE CONTROL ctl-e03 (S050 row relabelled S049; own corpus parent): expect E03, exit 1
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E03	S049 duplicate id
ctl_e03_exit=1
```

```
## NEGATIVE CONTROL ctl-e04 (S050 source+scope cells copied from S049; own corpus parent): expect E04, exit 1
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E04	S050 duplicate url zc.cnvd.org.cn/news/helpList within scope CNVD's own 众测 platform help page: its authorised-testing scope rule, its seven-factor composite score and its FAQ answers on rating changes and scope
ctl_e04_exit=1
```

## Verdict

PASS. With the planned rows the mirror's `sources-census.sh validate --file` exits 0 and shows only the base
W04 S028/S029 warnings; projected totals are `rows=50`, `tier.A=47 / B=1 / C=2`,
`status.mined=38 / queued=9 / rejected=3`, `invalid=0`, `missing=0`; each planned id appears once; both URLs
are absent from the live registry and collide with no live row (E04 silent on the passing mirror, loud in
ctl-e04); staged S034/S035 URLs are byte-identical to the lane S049/S050 URLs. The append can proceed with
this row shape.

## Hand-off to ExecRegistryAppend (messaged by id)

Keep these cells exactly as validated: `id` S049/S050, the source-cell URL bytes, `kind docs`, `tier A`,
`status mined`, `opened 2026-10-26`, `recheck 90d` / `180d`, `used-by
corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`. Anchor, scope and teaches prose are the
owner's to refine; editing only those cannot move the census findings, while editing the URL, id, status or
used-by cell can. Re-run the gate on the real bytes after appending (the L1 owns the post-wave gate).

## Notes, risks, blockers

- Q6: the S049 capture carries platform-issued VPN account/password instructions for testers (capture lines
  205–206). No credential material is quoted, copied or referenced anywhere in this receipt or in the planned
  rows; the anchors cite section names and other line numbers only.
- Caveat: anchor prose was read by this seat from the round-32 captures; a later capture rewrite would
  invalidate it, not the census gate.
- No blockers. No tool installs (none needed), no lane git/jj mutation, no writes outside the lane receipt and
  the scratch dir (deleted at exit).
