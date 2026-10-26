# Kasegi quarantine slice — live source verdicts

Register (read-only): `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
— sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 375 lines (unchanged since
round 30's slice `d02acb68…`).
Slice: `ExecAssimilationIds.quarantine-slice` — 7 lines, 417 B, sha256
`d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862`.

Slice extraction (the round-30 frozen awk, unchanged):

```
awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R"
```

Every extracted line carries an S-id (verified with `awk '$0 !~ /S[0-9]+/'` → no output). Rows S048, S065,
S068, S069, S070 carry the register's glued trailing backtick in cell 4 (`S048``); the predicate still matches
and the ids read S048/S065/S068/S069/S070.

Fetch method: `curl -sS -L --max-time 90 -A 'kasegi-shokunin/1.0'` (the lane capture UA, one request per
unique URL; S069 and S070 cite the identical URL, so one measurement covers both). Times are UTC, recorded
with `date -u` immediately before/after each request.

Verdict vocabulary, fixed before the payloads were read:

| verdict | rule |
|---|---|
| `present-and-located` | payload obtained; the quoted span occurs verbatim (whitespace-normalized) in the extracted text, with the anchor line named |
| `quote-defective` | payload obtained; the quoted claim is identifiable, but the recorded span is not verbatim (spliced or punctuated differently), so the row may not be quoted or adopted until requoted |
| `unreachable` | no payload obtained (4xx/403/0 B), or nothing resembling the quote is findable in the obtained payload |
| `unverifiable` | payload obtained, but the register row carries no quote, so there is no claim to locate; the document anchor is recorded and nothing is credited |

No row is called a fabrication by this table. A `quote-defective` row is a located quote-level defect, not an
unreachable source; neither verdict permits adoption.

## Verdicts

| id | round | register class | cited source | fetched (UTC) | http | bytes | payload sha256 | verdict | anchor located |
|---|---|---|---|---|---|---|---|---|---|
| S037 | round1 | `payload-absent` | `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A` | 19:31:40–19:31:42Z | 200 | 24131 | `add556377faf76dd47bdfa1949128496b8e19632d0ee35210ce61d3558fa3737` | `quote-defective` | page title cell L16, `标准状态：` L18 / `现行` L19, `发布日期` L27 / `2020-11-19` L28, `实施日期` L29 / `2021-06-01` L30; `标准号：GB/T 30279-2020` L14 |
| S054 | round3 | `payload-absent` | `https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf` | 19:31:40–19:31:42Z | 200 | 513648 | `0150c9d15dee603f55573f4692f306ba8ff46f70454b032f813b95fbdbb12b88` | `quote-defective` | `（ア） 脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認` L42 + `されたもの又は疑われるもの` L43 (extracted text, 139 lines) |
| S048 | round2 | never checked | `https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3` | 19:31:40–19:31:41Z | 404 | 748 | `95cd25d80d88cce1e08528c03d5eb488f56bf9991f820bc31569b001eb2e2436` | `unreachable` | none — body is `HTTP状态 404 - 未找到`; no quote cell in the row |
| S065 | round4 | never checked | `http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf` | 19:31:40–19:32:28Z | 200 | 7465472 | `e33b0f67293441f19ee519b2ed1619121da84867aa8396a3a16facd572586d83` | `unverifiable` | document anchor `现行有效法律目录（303 件）` L1 (extracted text, 843 lines); row has no quote cell |
| S068 | round4 | never checked | `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` | 19:31:40Z | 403 | 465 | `dd13cbccdb5a40c075e40e2b088c82268566059fc8143a5ce8a7de10d29567ae` | `unreachable` | none — body is `Access Denied` (edge denial); no quote cell in the row |
| S069 | round4 | never checked | `https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F` | 19:31:40–19:31:41Z | 200 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `unreachable` | none — empty payload, no document; no quote cell in the row |
| S070 | round4 | never checked | same URL as S069 | 19:31:40–19:31:41Z | 200 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `unreachable` | none — same measurement; no quote cell in the row |

## Evidence per row

### S037 — quote-defective

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o S037.body \
    'https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A'
http=200 bytes=24131 type=text/html;charset=utf-8   (2026-10-26T19:31:40Z→19:31:42Z)
sha256 add556377faf76dd47bdfa1949128496b8e19632d0ee35210ce61d3558fa3737
```

HTML tag-stripped, one text line per element (52 non-empty lines). Recorded quote
`信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01`:
whole-string occurrences **0**. The cells exist but are not contiguous and the punctuation differs:

```
14:标准号：GB/T 30279-2020
16:信息安全技术 网络安全漏洞分类分级指南
18:标准状态：
19:现行
27:发布日期          <- page has no colon
28:2020-11-19
29:实施日期          <- page has no colon
30:2021-06-01
```

Between the title cell and `标准状态：` the page carries `英文标准名称：…`, and between `现行` and
`发布日期` it carries `在线预览 / 下载标准 / 实施信息反馈 / 中国标准分类号（CCS）/ L80 / 国际标准分类号（ICS）/ 35.040`
(L20–L26). `grep -c '发布日期：'` → 0 and `grep -c '实施日期：'` → 0. Every factual token of the quote is
located on the cited page; the quoted string as recorded is a field concatenation with two added colons, so the
row's quote must be rewritten as separate located cells before it can be quoted or adopted.

### S054 — quote-defective

```
$ curl ... -o S054.body 'https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf'
http=200 bytes=513648 type=application/pdf   (19:31:40Z→19:31:42Z)
sha256 0150c9d15dee603f55573f4692f306ba8ff46f70454b032f813b95fbdbb12b88
$ pdftotext -enc UTF-8 S054.body S054.txt   -> rc=0, 139 lines, 8785 B (text mode and -layout mode agree)
```

Recorded quote `脆弱性の悪用が確認されたもの又は疑われるもの` → **0** occurrences under whitespace
normalization, because the source inserts the statutory definition between `脆弱性` and `の悪用`:

```
42:（ア） 脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認
43:されたもの又は疑われるもの
```

The trailing clause `の悪用が確認されたもの又は疑われるもの` occurs exactly **1** time (L42→L43, both
`pdftotext` modes). The recorded quote drops `（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）` without
an ellipsis, joining `脆弱性` straight to `の悪用…` — a splice, not a fabrication. Rewrite as the source
sentence or quote only the trailing clause before adoption.

### S048 — unreachable

```
$ curl ... -o S048.body 'https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3'
http=404 bytes=748 type=text/html;charset=utf-8   (19:31:40Z→19:31:41Z)
sha256 95cd25d80d88cce1e08528c03d5eb488f56bf9991f820bc31569b001eb2e2436
retry 19:33:24Z→19:33:25Z: http=404 bytes=748 sha256 95cd25d8… (same body)
```

Body: `<title>HTTP状态 404 - 未找到</title>` … `文.件[/WEB-INF/views/gb/search/gbDetailed.jsp] 未找到`. The digest
equals the round-36 verifier spot-check's recorded failure (`status=404 bytes=748`, sha `95cd25d8…`). The row
carries no quote, so there is nothing to call defective; the document is gone.

### S065 — unverifiable

```
$ curl ... -o S065.body 'http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf'
http=200 bytes=7465472 type=application/pdf   (19:31:40Z→19:32:28Z)
sha256 e33b0f67293441f19ee519b2ed1619121da84867aa8396a3a16facd572586d83
$ pdftotext -enc UTF-8 S065.body S065.txt  -> rc=0 (font warnings only), 843 lines, 31899 B
L1: 现行有效法律目录（303 件）
```

The PDF is now reachable (the register's "could not be fetched" no longer reproduces). It is the NPC
consolidated list of laws in force; the row has no quote cell, so only the document is anchored — `中华人民共和国`
occurs 311 times, and `中华人民共和国网络安全法（2016 年通过，2025` at L593. Nothing is credited: a row with no
located quote stays non-adoptable even when its source resolves.

### S068 — unreachable

```
$ curl ... -o S068.body 'https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html'
http=403 bytes=465 type=text/html   (19:31:40Z)
sha256 dd13cbccdb5a40c075e40e2b088c82268566059fc8143a5ce8a7de10d29567ae
retry 19:33:25Z: http=403 bytes=465 sha256 1defe6a29eecd9d329ea39dd93c74e4b58de725b27ba1ccb30e66f57e22b6e78
```

Body: `<TITLE>Access Denied</TITLE>` + `You don't have permission to access … on this server` + an
`errors.edgesuite.net` reference. Two further fetches at 19:35:14Z (403/465 B, sha `ff047965…a66a847` and
`dc0ea0f0…41e6cef7`) differ only in the `Reference #` id and the mirrored `errors.edgesuite.net` URL that
carries the same id (`diff -u` shows those two lines and nothing else), so the per-request digest is not a
payload difference. No quote cell in the row.

### S069 / S070 — unreachable

```
$ curl ... -o S069.body 'https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F'
http=200 bytes=0 type=   (19:31:40Z→19:31:41Z)
sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855   (empty body)
retry 19:33:25Z→19:33:26Z: http=200 bytes=0 (same empty digest)
```

S070 cites the identical URL; the one measurement covers both rows. The locator ends at the URL-encoded
directory `path=/zxd/2025005470/20_标准起草/`, and the server returns 200 with a zero-byte body — no document is
served at the recorded locator, so neither row has a payload. The register's own note that this locator looks
truncated (round-30 scout) is consistent with the empty response; no filename is invented here.

## Summary

| verdict | rows |
|---|---|
| `present-and-located` | 0 |
| `quote-defective` | 2 (S037, S054) |
| `unreachable` | 4 (S048, S068, S069, S070) |
| `unverifiable` | 1 (S065) |

No slice row is adoptable on this measurement. The two reachable quoted rows need requoting (S037: fields, not a
span; S054: definition elided without a marker); the four unreachable rows need a live locator (S048 and S069/S070
return no document; S068 denies the capture UA); S065 has no quote to check. Nothing here is labelled a
fabrication.
