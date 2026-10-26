# ExecManifest32 — round-32 capture manifest (C1 rule B/C data)

Seat: ExecManifest32, kasegi-shokunin round 33, lane base 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4.
Model: `opencode-go/deepseek-v4.1-flash` (config route; no model passed).
Write scope exercised: `corpus/source-snapshots/round-32/manifest.json` only. No other lane file written; no git/jj mutation; no installs; no scratch dir created (no clones, work trees or fixtures needed).

## 1. Artifact

`corpus/source-snapshots/round-32/manifest.json` (new, 5753 bytes after the Q7/Q8 addition)

```
$ sha256sum corpus/source-snapshots/round-32/manifest.json
6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774  corpus/source-snapshots/round-32/manifest.json
```

Schema follows `round-31/manifest.json` (`schema_version: 1`, `purpose`, `sources: [...]`, 2-space indent) with the two C1 contract fields added at record level:

| id | path | sha256 | url | fetched_utc | archival | quotes |
|---|---|---|---|---|---|---|
| S049 | S049.txt | `962a451a…1cb8` | `https://zc.cnvd.org.cn/news/helpList` | `2026-10-25T23:14:00-03:00` | absent | 8 |
| S050 | S050.txt | `2f9c6406…6888` | `https://security.360.cn/Reward/rules` | `2026-10-25T23:14:00-03:00` | absent | 6 |

Both sha256 values are the committed capture bytes, re-derived through git:

```
$ git show 288ea9a:corpus/source-snapshots/round-32/S049.txt | sha256sum
962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8  -
$ git show 288ea9a:corpus/source-snapshots/round-32/S050.txt | sha256sum
2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888  -
```

`fetched_utc` is the capture commit instant, read from git, not retyped:

```
$ git log -1 --format='%H%n%aI%n%cI' 288ea9a
288ea9ac17a78dce644388af35b89aa96b7994da
2026-10-25T23:14:00-03:00
2026-10-25T23:14:00-03:00
```

No `archival` key on either record (contract: round-32+ records carry `fetched_utc` and no archival exemption). `github`-style page-level `url` values are the lane rows' URLs per the L1 contract; byte-exactness against the eventual row text is on ExecRegistryAppend (message sent, §7).

## 2. Per-assertion table

Normalization declared per QUALITY Q8: `source-recheck.py` `normalize()` strips `</?u>` and collapses all whitespace to single spaces. Every assertion below was measured exactly-once under that normalization before it was written, so **no assertion carries an `anchor`**. Measured with `grep -F -c` (raw text; counts lines) and re-checked by the instrument (normalized occurrences). All strings are single-line; spaces inside the S050 strings are the converter's own.

| id | line | grep -c | recheck | quote (verbatim) |
|---|---|---|---|---|
| S049 Q1 | L211 | 1 | occurrences=1 | 漏洞提交页面的目标列表仅用于用户快速选择，并不是项目的测试范围约定 |
| S049 Q2 | L214 | 1 | occurrences=1 | 众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。 |
| S049 Q3 | L410 | 1 | occurrences=1 | 测试项目范围以外的系统不在客户的授权范围内，所以是坚决不允许的。 |
| S049 Q4 | L208 | 1 | occurrences=1 | 平台和企业在评价漏洞的风险等级时，会根据项目的规则、业务特点、影响范围等因素来调整漏洞的最终评级 |
| S049 Q5 | L419 | 1 | occurrences=1 | 平台将会根据企业对漏洞的评级，结合项目规则中的要求来为白帽发放奖金。 |
| S049 Q6 | L408 | 1 | occurrences=1 | 对于未通过可信测试系统发现的问题平台有权取消或降低奖励。 |
| S049 Q7 | L132 | 1 | occurrences=1 | 最终得分 = 四舍五入（有效性 × 漏洞等级 × 测试难度 × 危害程度 × 企业规模 × 报告质量） |
| S049 Q8 | L212 | 1 | occurrences=1 | 注：请严格按照项目测试范围进行测试。 |
| S050 Q1 | L70 | 1 | occurrences=1 | 本标准适用于 360 集团发布的产品和业务 |
| S050 Q2 | L591 | 1 | occurrences=1 | 未纳入安全服务的资产一般情况下不收录相关漏洞 |
| S050 Q3 | L595 | 1 | occurrences=1 | 禁止将漏洞报告存放在互联网开放的云服务或共享文档中 |
| S050 Q4 | L597 | 1 | occurrences=1 | 对提交漏洞报告后、未修复漏洞前，将漏洞报告公开或泄露的不予奖励。 |
| S050 Q5 | L112 | 1 | occurrences=1 | 漏洞奖励=业务系数*基础安全币。 |
| S050 Q6 | L418 | 1 | occurrences=1 | 分为严重、高危、中危、低危、忽略五个等级 |

Grep command shape, per assertion (`grep -F -c -- <quote> corpus/source-snapshots/round-32/<Sxxx>.txt`), printed `grep_c=1 exit=0` for all **14** rows.

### Line corrections and the one un-bindable candidate

- The L1 candidate locations said S050 Q1 = L69 and S050 Q3 = L594; the capture holds them at **L70** and **L595** (`grep -n`), and the manifest uses the measured lines.
- ExecEntryF16 asked to pin the full S050 sentence L70-71 (`…合资公司等也在收录范围内`). It **cannot bind**: `normalize()` collapses the source line break to a space, inserting one between `合资公` and `司等` mid-word, so the full sentence has 0 normalized occurrences. The manifest pins the wrap-free clause on L70 instead and the `purpose` states that the L71 continuation is not asserted. ExecEntryF16 was told to quote that clause (or the L71 continuation separately), not the joined sentence.
- S050 `安全币 ：RMB=1 : 5` (L129) was considered and **not** pinned: it occurs 7 times in the capture (L129/159/189/219/249/274/304), and a non-unique quote would need an anchor the entry does not need today.
- All other 11 strings ExecEntryF16 supplied are byte-identical to the pins (Python `raw=True`, normalized count 1).

## 3. `source-recheck.py` output (after the Q7/Q8 addition)

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json
S049:sha256 OK
S049:Q1 OK occurrences=1
S049:Q2 OK occurrences=1
S049:Q3 OK occurrences=1
S049:Q4 OK occurrences=1
S049:Q5 OK occurrences=1
S049:Q6 OK occurrences=1
S049:Q7 OK occurrences=1
S049:Q8 OK occurrences=1
S050:sha256 OK
S050:Q1 OK occurrences=1
S050:Q2 OK occurrences=1
S050:Q3 OK occurrences=1
S050:Q4 OK occurrences=1
S050:Q5 OK occurrences=1
S050:Q6 OK occurrences=1
recheck_all_exit=0
```

Per-source runs before the addition (`--source S049`, `--source S050`) also exited 0 with `occurrences=1` on their six assertions each.

## 4. Q6 credential exclusion

The S049 page carries platform-issued tester VPN account/password instructions (`S049.txt` §VPN连接方式, e.g. L202/L205/L374-L405). None of it is quoted: the 14 asserted strings are scope, severity-adjustment, reward and conduct text only. Marker check over the manifest:

```
$ grep -nE "密码|帐号|账号|openvpn|ca.crt|cnvd.ovpn" corpus/source-snapshots/round-32/manifest.json
(no output)  → no-credential-markers-in-manifest
```

## 5. Scout receipts reconciled

- `wave1/ScoutLiveDrift.md`: live re-fetch at 2026-10-26T04:16Z returned HTTP 200 for both URLs and post-conversion text identical to the committed captures (sha256 `962a451a…1cb8` / `2f9c6406…6888`, 426/426 and 630/630 lines, `diff -u` empty). So no pin points at text that drifted; the sha256 pins bind the committed bytes, and the drift run is not a substitute for them (Q7).
- `wave1/ScoutF16Sweep.md` (PRE-STATE by its own label: registry 48, frontier 15 when it ran): confirms the lane held zero CNVD 众测 / 360SRC ground and lists S049 scoring formula L132 and the 360SRC reward material as the added ground. I pinned the S049 formula (Q7) and the scope note (Q8) from it; S050's reward table beyond L112 was seen only by TOC lines, and this seat does not assert unread table cells.

## 6. `capture-binding-check.py` on the landed bytes

ExecCaptureBinding's instrument landed during this seat. Final instrument `sha256 b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9` (492 lines; an earlier `4bc7aed3…` revision differed by docstring only).

Before the registry append (`grep -cE '^\|[[:space:]]*(S049|S050)[[:space:]]*\|' corpus/SOURCES.md` → 0, registry 48 rows) the run was **PRE-STATE**:

```
MANIFEST round-32 records=2 url_bound=0 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
FAIL rule=no-row record=S049 dir=round-32
FAIL rule=no-row record=S050 dir=round-32
records=40 bound=38 unbound=2
binding_exit=1
```

that is rule B with no row to bind to, not a manifest defect. After ExecRegistryAppend landed rows S049/S050 (rows now 50; the two URL strings each occur exactly once in `SOURCES.md`, inside their own row's source cell), the run on lane bytes is:

```
$ python3 corpus/instruments/capture-binding-check.py
…
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
binding_exit=0
```

so both round-32 records satisfy rule B (single-row URL) and rule C (`fetched_utc`, no archival exemption). The instrument's own selftest at this digest is `cases=11 failures=0` exit 0 (ExecCaptureBinding receipt). An earlier in-flight instrument revision reported `url-ambiguous` for S029/S006; it was superseded inside the wave, so its numbers are non-comparative (M30-3) and are not cited.

## 7. Coordination emitted

- `agent://ExecEntryF16`: pinned-id list, the S050 L70-71 un-bindable finding, and the instruction to quote the L70 clause; later additions Q7 (formula) and Q8 (scope note) are in the manifest.
- `agent://ExecRegistryAppend`: row URLs must be byte-exact `https://zc.cnvd.org.cn/news/helpList` (S049) and `https://security.360.cn/Reward/rules` (S050), no trailing slash/fragment and no second row carrying either string, or rule B reports 0 matches.

## 8. Risks / limits

- The URL pins can only be validated by rule B after the registry rows land; if ExecRegistryAppend writes either URL differently (case, trailing slash, fragment), `url-unbound` is a registry-row defect, not a capture defect.
- `fetched_utc` is the capture commit's author timestamp; no independent fetch log exists for round-32, so it records when the captures were committed, not a measured HTTP instant. The live drift run (§5) bounds drift only from 2026-10-26T04:16Z onward.
- No test/lint/build run (wave policy); the L1 owns the post-integration gate.
