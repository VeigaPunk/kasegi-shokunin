# ExecQuarantine — round-33 quarantine slice hand-check (7 rows)

Seat: ExecQuarantine (leaf). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
write scope; `/home/vgpnk/Projects/shokuknow` read-only (register + staged rows read, nothing
written, no campaign tool run). Lane base `690b69da`, claims-freeze `6e55c8d5`.

Item: hand-check `{RD}/assimilation/quarantine-slice` (7 register rows). Payload-absent rows
(S037, S054): re-derive the staged quote from `merge/kasegi/SOURCES.append.md`, fetch the cited
source live with the instrument UA into scratch, adopt-with-anchor if the quote is verbatim
contiguous after declared normalization, else refuse with the exact reason in the Gate block.
Unreachable rows (S048, S065, S068, S069, S070): mark `unreachable` with the register's stated
cause.

Result: **2 refuse, 5 unreachable, 0 adopted.** No file outside this receipt was written.
No tool installed (curl, pdftotext, python3 already present). Answering model, config route
table (not measured here, item does not depend on it): `opencode-go/deepseek-v4.1-flash`.

## 1. Slice re-derivation (is the committed slice the intended 7 rows?)

```console
$ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
$ sed -n '99,100p;322,326p' "$R" | awk -F'|' '{gsub(/^ +| +$/,"",$4); gsub(/^ +| +$/,"",$5); printf " %s   %s \n", $4, $5}' > "$S/r33-slice.txt"
$ cat "$S/r33-slice.txt"
 S037   `payload-absent` 
 S054   `payload-absent` 
 S048`   the cited source could not be fetched, so no quote was checked 
 S065`   the cited source could not be fetched, so no quote was checked 
 S068`   the cited source could not be fetched, so no quote was checked 
 S069`   the cited source could not be fetched, so no quote was checked 
 S070`   the cited source could not be fetched, so no quote was checked 
$ diff "$S/r33-slice.txt" .ufo/waves/round-33/assimilation/quarantine-slice ; echo "diff_exit=$?"
diff_exit=0
$ sed -n '99,100p;322,326p' "$R" | awk -F'|' '{gsub(/^ +| +$/,"",$2); print $2}' | sort | uniq -c
      7 `kasegi`
```

The committed `quarantine-slice` is byte-identical to the rows re-derived from the register
(payload-absent header block lines 99-100, no-quote block lines 322-326), and all seven rows
are lane `kasegi`. Register row text (payload-absent block, lines 99-100):

```console
$ sed -n '99,100p' "$R" | cut -c1-230
| `kasegi` | round1 | S037 | `payload-absent` | https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A | `信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2
| `kasegi` | round3 | S054 | `payload-absent` | https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf | `脆弱性の悪用が確認されたもの又は疑われるもの` | cited source, companion URL
```

## 2. Staged quote text, re-derived from `SOURCES.append.md`

```console
$ sed -n '13p' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md
| S037 | 国家标准全文公开系统 标准信息 GB/T 30279-2020 — https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A | docs | A | The official catalogue identity, status and lifecycle dates … | record fields 中文标准名称, 标准状态, 发布日期, 实施日期, 发布单位 国家市场监督管理总局、中国国家标准化管理委员会; hcno 458BACCE700CA8E0B728CFB5F762DE7A | GB/T 30279-2020 is the current Chinese national recommendation … in force since 2021-06-01 | mined | 2026-10-23 | 180d | corpus/…
$ sed -n '30p' …SOURCES.append.md
| S054 | 重要電子計算機に対する不正な行為による被害の防止に関する法律等の施行を踏まえた脆弱性関連情報の取扱いについて（要請） — https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf | spec | A | The statutory notification of vulnerability information to the Cabinet Office under the 2025 cybersecurity statute | 独立行政法人情報処理推進機構 理事長 殿 / 内閣府サイバー官民連携室長 宛、令和8年9月17日 府連第7号; １．脆弱性関連情報の提供について （ア）and （イ） | The Cabinet Office track has two trigger criteria … | mined | 2026-10-23 | 180d | corpus/knowledge/authorization-safe-harbor-and-scope-2026-10-23-amendment.md |
```

The staged rows carry the citation URL and the anchor (field labels / section numbers); the
verbatim quoted string is bound to the same id+URL by the register and by the quote census:

```console
$ python3 - <<'PY'   # json over quote-lint-full-v5.json, findings where lane==kasegi and id in {S037,S054}
{
 "lane": "kasegi",
 "round": "round1",
 "id": "S037",
 "verdict": "ABSENT",
 "fold": null,
 "quote": "信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01",
 "url": "https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A",
 "line": "- Quote: \"信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01\"",
 "sweep": false,
 "binding": "id"
}
---
{
 "lane": "kasegi",
 "round": "round3",
 "id": "S054",
 "verdict": "ABSENT",
 "fold": null,
 "quote": "脆弱性の悪用が確認されたもの又は疑われるもの",
 "url": "https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf",
 "line": "- Quote: \"脆弱性の悪用が確認されたもの又は疑われるもの\"",
 "sweep": false,
 "binding": "id"
}
---
```

So the staged strings under test are exactly:

- S037 `信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01`
- S054 `脆弱性の悪用が確認されたもの又は疑われるもの`

## 3. Live fetch (instrument UA, scratch only)

```console
$ S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kasegi-r33/ExecQuarantine"; mkdir -p "$S"; cd "$S"
$ UA='kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)'
$ curl -sS -L --max-time 90 -A "$UA" -o S037.html -w 'S037 http=%{http_code} bytes=%{size_download} type=%{content_type}\n' 'https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A'
S037 http=200 bytes=24189 type=text/html;charset=utf-8
$ curl -sS -L --max-time 120 -A "$UA" -o S054.pdf -w 'S054 http=%{http_code} bytes=%{size_download} type=%{content_type}\n' 'https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf'
S054 http=200 bytes=513648 type=application/pdf
$ sha256sum S037.html S054.pdf
9cba2e96e343e1d0c95d23fb50454fa1321cb2d01af6ae318653290a1d20f204  S037.html
0150c9d15dee603f55573f4692f306ba8ff46f70454b032f813b95fbdbb12b88  S054.pdf
$ pdfinfo S054.pdf | grep -E '^(Pages|Page size|File size)'
Pages:           3
Page size:       595.32 x 841.92 pts (A4)
File size:       513648 bytes
$ pdftotext -layout S054.pdf S054.layout.txt   # and pdftotext S054.pdf S054.txt
```

Both sources fetched cleanly (HTTP 200). For S037 the fetch is 24,189 B where the round-32
spotcheck recorded 24,123 B — the record page carries dynamic assets, so byte equality is not
an invariant; the record field strings are what is compared below.

## 4. Declared normalization (folds)

HTML (`S037.html`): decode UTF-8, drop `<script>`/`<style>` bodies, replace every tag with a
space, unescape entities. PDF (`S054`): `pdftotext` text layer, both default and `-layout`
(identical under F3: `F3_equal= True len_a= 2898 len_b= 2898`). Then four folds, weakest last:

| fold | rule |
|---|---|
| F1 verbatim | as decoded |
| F2 ws-collapse | every whitespace run → one space, strip |
| F3 ws-removed | every whitespace character removed |
| F4 colon-insensitive | F3 plus removal of `：` (S037 only; isolates splice from punctuation) |

Presence of the staged string:

| row | F1 | F2 | F3 | F4 |
|---|---|---|---|---|
| S037 | absent | absent | absent | absent |
| S054 | absent | absent | absent | — (not applicable) |

```console
$ # S037, folds over S037.txt (tag-stripped text)
S037 F1_verbatim present= False
S037 F2_ws_collapse present= False
S037 F3_ws_removed present= False
F4 staged_present= False | len 52
F4 live  : 标准状态现行在线预览下载标准实施信息反馈中国标准分类号（CCS）L80国际标准分类号（ICS）35.040发布日期2020-11-19实施日期2021-06-01主管部门国家标准委…
F4 staged: 信息安全技术网络安全漏洞分类分级指南标准状态现行发布日期2020-11-19实施日期2021-06-01
$ # S054, identical result for both pdftotext modes
 S054 F1_verbatim present= False
 S054 F2_ws_collapse present= False
 S054 F3_ws_removed present= False
```

## 5. Per-row verdicts

| id | class (register) | live fetch | staged string under declared folds | verdict |
|---|---|---|---|---|
| S037 | `payload-absent` | 200, 24,189 B html, sha256 `9cba2e96…20f204` | absent F1-F4; **spliced field collage** (2 gaps skipped, 2 colons inserted) | **refuse** |
| S054 | `payload-absent` | 200, 513,648 B pdf, 3 pp, sha256 `0150c9d1…12b88` | absent F1-F3; **statutory definition parenthetical elided** | **refuse** |
| S048 | `unreachable` | not fetched (bounds §8: only the two named payload-absent URLs) | no quote in register | **unreachable** |
| S065 | `unreachable` | not fetched, same bound | no quote in register | **unreachable** |
| S068 | `unreachable` | not fetched, same bound | no quote in register | **unreachable** |
| S069 | `unreachable` | not fetched, same bound | no quote in register | **unreachable** |
| S070 | `unreachable` | not fetched, same bound | no quote in register | **unreachable** |

### S037 — exact reason

Live record page, F2 text around the three claimed fields:

```console
$ python3 -c '…print F2 slice from 标准状态…'
'标准状态： 现行 在线预览 下载标准 实施信息反馈 中国标准分类号（CCS） L80 国际标准分类号（ICS） 35.040 发布日期 2020-11-19 实施日期 2021-06-01 主管部门 国家标准委 归口部门 国家标准委 发布单…'
```

The staged string is a collage of three separate record blocks, not a contiguous field string:

1. `信息安全技术 网络安全漏洞分类分级指南` is present (F2, prefixed by its own label `中文标准名称：`), but the staged text
   then jumps straight to `标准状态：`, skipping the live `英文标准名称：…` line:
   ```console
   context after name: 英文标准名称：Informationsecuritytechnology—Guidelinesforcategorizationandcla…
   ```
2. `标准状态：现行` is present only at F3 (the live page renders a space after the colon); the staged
   text then skips `在线预览 下载标准 实施信息反馈 中国标准分类号（CCS） L80 国际标准分类号（ICS） 35.040`:
   ```console
   context after status: 标准状态：现行在线预览下载标准实施信息反馈中国标准分类号（CCS）L80国际标准分类号（ICS）35.040发布日期2020-11-19实施日期2021-06-01…
   ```
3. `发布日期：2020-11-19` and `实施日期：2021-06-01` do not exist on the page: the labels are rendered
   without a colon (`发布日期` / `实施日期`), so the staged string inserts two `：` characters:
   ```console
   '发布日期：2020-11-19'  F3=False
   '实施日期：2021-06-01'  F3=False
   '发布日期2020-11-19实施日期2021-06-01'  F3=True
   ```

The facts themselves hold on the live page (标准号 GB/T 30279-2020, 标准状态 现行, 发布日期
2020-11-19, 实施日期 2021-06-01, 发布单位 国家市场监督管理总局、中国国家标准化管理委员会); only the quoted
string is defective. This repeats the round-32 D6 finding on an independent fetch.

### S054 — exact reason

Live PDF text (§1, item （ア）), F2 with `-layout`:

```console
$ python3 -c '…print F2 slice from （ア） 脆弱性…'
'（ア） 脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認 されたもの又は疑われるもの （イ） 以下のいずれにも該当するもの ① 脆弱性の深刻度が高いと認められるもの …'
```

The staged string `脆弱性の悪用が確認されたもの又は疑われるもの` elides the statutory definition parenthetical that the
document places between `脆弱性` and `の悪用が確認されたもの又は疑われるもの`:

```console
$ python3 - <<'PY'   # F3 over both pdftotext modes
S054.txt pages_text_len 2898 | bare_phrase_present= False | suffix_present= True | full_clause_present= True
S054.layout.txt pages_text_len 2898 | bare_phrase_present= False | suffix_present= True | full_clause_present= True
PY
```

i.e. `脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの` is present
contiguously; the staged shorter form is not present on any page (3 pp, occurrence of 悪用 at
layout lines 46, 54, 66 only). No ellipsis marks the omission, so the string as staged is a
splice, not a quote. The row's teaching (two Cabinet-Office trigger criteria, （ア） and （イ）)
is consistent with the document, but the quoted span is defective.

### S048 / S065 / S068 / S069 / S070 — unreachable, not fabrication

Register cause (identical on all five): `the cited source could not be fetched, so no quote was
checked`. Cited sources as registered:

| id | cited source (register, exact cell) |
|---|---|
| S048 | https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3 |
| S065 | http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf |
| S068 | https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html |
| S069 | https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F |
| S070 | https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F |

```console
$ sed -n '322,326p' "$R" | awk -F'|' '{gsub(/^ +| +$/,"",$4); gsub(/^ +| +$/,"",$6); print $4, "->", $6}'
S048` -> https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3
S065` -> http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf
S068` -> https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html
S069` -> https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F
S070` -> https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F
```

Three observations that bound the verdict:

- The register's no-quote table has no quote column (`lane | round | id | why it was not checked |
  cited source`), so for these five there is no staged string to re-check in the register at all;
  a later hand-check has to recover the original quoted span from the round that staged it.
- The register's cited-source cell for S069/S070 is itself truncated after the directory path
  (`…20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F`), while `SOURCES.append.md` lines 45-46 carry the full
  attachment filenames (`…20_WD_2025005470_….pdf` and `…20_DI_2025005470_….pdf`). On the register row alone the
  attachment is not identified; the staged row is.
- The ids in that table carry a trailing backtick (`S048``, `S065``, `S069``, …), an artifact of the
  register's row writer that the committed `quarantine-slice` inherited. Treated as `S048`, `S065`,
  `S068`, `S069`, `S070` (the trailing backtick is not part of the id). Register is read-only;
  recorded, not fixed.

Per the register's own class definition, `unreachable` means "the source could not be fetched, so
the quote was never checked"; the reader action is "re-fetch, or mark the row unverifiable — do
NOT call it a fabrication". No fetch was run against these five URLs: bounds §8 limits live
fetches to the two payload-absent sources this item names.

## 6. Gate blocks (installable; ScribeLesson copies these verbatim)

## Gate — S037 · 国家标准全文公开系统 GB/T 30279-2020 (payload-absent)

**refuse** — staged quote is a spliced field collage, not verbatim. Live record page
(`https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A`,
HTTP 200, 24,189 B, 2026-10-26, instrument UA; sha256 `9cba2e96e343e1d0c95d23fb50454fa1321cb2d01af6ae318653290a1d20f204`)
renders `标准状态： 现行 在线预览 下载标准 实施信息反馈 中国标准分类号（CCS） L80 国际标准分类号（ICS） 35.040 发布日期 2020-11-19 实施日期 2021-06-01`
(F2 form) and renders the two
date labels without a colon. The staged string therefore (a) skips the `英文标准名称：…` line after the
standard name, (b) skips `在线预览 下载标准 实施信息反馈 中国标准分类号（CCS）L80 国际标准分类号（ICS）35.040` between
`现行` and `发布日期`, and (c) inserts `：` after `发布日期` and `实施日期`. Absent under verbatim,
whitespace-collapsed, whitespace-removed and colon-insensitive folds (F1-F4). Flip condition: re-stage
with the located contiguous blocks `标准状态：现行` and `发布日期 2020-11-19 实施日期 2021-06-01` (whitespace-removed form
`发布日期2020-11-19实施日期2021-06-01`), then re-check. No lane registry row exists for openstd
(`grep -c openstd corpus/SOURCES.md` → 0), so adoption also needs a new row.

## Gate — S054 · 内閣府 request on vulnerability-information handling (payload-absent)

**refuse** — staged quote elides the statutory definition parenthetical. Live PDF
(`https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf`, HTTP 200, 513,648 B,
3 pp, 2026-10-26, instrument UA; sha256 `0150c9d15dee603f55573f4692f306ba8ff46f70454b032f813b95fbdbb12b88`)
reads §1（ア）: `脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの` (whitespace-removed
form; `pdftotext -layout` inserts a line-wrap space between `確認` and `された`). The staged string
`脆弱性の悪用が確認されたもの又は疑われるもの` is absent under verbatim, whitespace-collapsed and whitespace-removed folds
(both `pdftotext` modes, all 3 pages); only the suffix `の悪用が確認されたもの又は疑われるもの` and the full clause are
contiguous. Flip condition: adopt the full clause with its parenthetical as the quoted span, with
the location §1（ア）, after a lane row exists (`grep -c 府連 corpus/SOURCES.md` → 0).

## Gate — S048 · 全国标准信息公共服务平台 plan record 20260806-T-469

**unreachable** — register cause: `the cited source could not be fetched, so no quote was checked`
(`https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3`). Not a
fabrication verdict; no quote text exists in the register for this row. Not re-fetched this round
(bounds §8). A later check must recover the staged span from the staging round before re-fetching.

## Gate — S065 · 全国人民代表大会常务委员会《现行有效法律目录》(303 件)

**unreachable** — register cause: `the cited source could not be fetched, so no quote was checked`
(`http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf`). Not a fabrication
verdict; no quote text in the register. Not re-fetched this round (bounds §8).

## Gate — S068 · Cisco Security Vulnerability Policy

**unreachable** — register cause: `the cited source could not be fetched, so no quote was checked`
(`https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html`). Not a
fabrication verdict; no quote text in the register. Not re-fetched this round (bounds §8).

## Gate — S069 · GB/T 30279—202X 征求意见稿 (draft text)

**unreachable** — register cause: `the cited source could not be fetched, so no quote was checked`
(`https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F`, register cell as stored — the register truncates this URL after
`20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F`; `SOURCES.append.md` line 45 carries the full `…20_WD_2025005470_…（征求意见稿）.pdf` path).
Not a fabrication verdict; no quote text in the register. Not re-fetched this round (bounds §8).

## Gate — S070 · GB/T 30279—202X 征求意见稿 编制说明 (drafting note)

**unreachable** — register cause: `the cited source could not be fetched, so no quote was checked`
(`https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F`, register cell as stored — truncated as for S069; `SOURCES.append.md`
line 46 carries the full `…20_DI_2025005470_…（编制说明）.pdf` path).
Not a fabrication verdict; no quote text in the register. Not re-fetched this round (bounds §8).

## 7. Findings and residual risk

1. **S037 refusal repeats round-32 D6 on an independent fetch.** The register class `payload-absent`
   is confirmed for the string as staged; the record's facts are not disputed. If the row is ever
   adopted, the quote must be re-grounded on `发布日期2020-11-19实施日期2021-06-01` (+ `标准状态：现行`) and the
   lane needs a new openstd registry row (none exists today: `grep -c openstd corpus/SOURCES.md` → 0,
   `grep -c 30279 corpus/SOURCES.md` → 0).
2. **S054 is an elision, not a fabrication.** The staged span drops a statutory definition without
   an ellipsis; the corrected span is the full clause. The lane has no row for this document
   (`grep -c 府連 corpus/SOURCES.md` → 0) while holding 3 other `ipa.go.jp` rows — so this is new ground,
   and it stays out until re-staged with the corrected quote.
3. **Register format artifact, outside my write scope:** the five unreachable ids render with a
   trailing backtick (`S048``) and that artifact is inherited by the committed `quarantine-slice`.
   The slice itself is otherwise correct and byte-identical to a fresh derivation from the register.
4. **Byte-count note:** the S037 page returned 24,189 B here vs 24,123 B in the round-32 spotcheck
   (same day, both 200). Dynamic page assets; the field strings are identical, so no ground moved.
5. **Unreachable five remain unverified** — that is the point of the class. Their register rows carry
   no quote text, so a future check needs the staging round's span. They must never be reported as
   fabrications on this evidence.
6. **No credential material** was read, copied or quoted (QUALITY Q6): the pages fetched are a
   standards-catalogue record and a Cabinet-Office request letter; the CNVD 众测 capture page was not
   opened this round.
7. Scratch `$HYAKU_SCRATCH/kasegi-r33/ExecQuarantine` (S037.html, S054.pdf, S037.txt, S054.txt,
   S054.layout.txt, r33-slice.txt) removed before yield; every number above is reproduced from the
   commands in §1-§5, not from memory.

## 8. Files changed

- `.ufo/waves/round-33/wave1/ExecQuarantine.md` (this receipt) — only write.
