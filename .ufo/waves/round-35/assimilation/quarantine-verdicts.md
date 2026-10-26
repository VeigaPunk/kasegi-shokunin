# Quarantine verdicts — kasegi slice (round 35)

Seat: `ExecQuarantineSlice` (leaf, round 35 wave 1). Date: **2026-10-26** (UTC; every fetch
below was made in this seat, `2026-10-26T06:32Z`–`06:44Z`).
Input, read-only: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(sha256 `5afe1810a6c3d62f…`, 83,621 B — unchanged since round 34, which recorded the same `5afe1810a6c3` prefix).
No row is adopted this round; the lane adopts nothing until a row is hand-checked **present**
(wave-4 quarantine-first). Nothing in this file is a production edit.

## 0. Slice derivation (frozen command, verbatim)

```
A=<lane>/.ufo/waves/round-35/assimilation; mkdir -p "$A"
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" > "$A/quarantine-slice"
```

Result: `quarantine-slice`, 7 lines, 417 B, sha256
`d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862`. Re-running the same command
into a second file and `cmp`-ing gives exit 0 (derivation is deterministic). **7/7 lines carry an
S-id — no line lacks one.**

The slice reproduces the register's own two table shapes, which is why columns 4–5 do not mean
the same thing on every line. This is recorded here so a later reader does not mis-read the file:

| slice line | register section | column 4 | column 5 |
|---|---|---|---|
| 1 (`S037`) | `## Rows` (payload-absent) | id `S037` | class `` `payload-absent` `` |
| 2 (`S054`) | `## Rows` (payload-absent) | id `S054` | class `` `payload-absent` `` |
| 3–7 (`S048`,`S065`,`S068`,`S069`,`S070`) | `## Rows whose quotes were NEVER CHECKED` | id, **with a stray trailing backtick from the register's own cell** (`S048\``) | the note `the cited source could not be fetched, so no quote was checked` |

Two register-format facts, stated exactly so no one mistakes them for a defect of this seat's:

- The trailing backtick on the five never-checked ids is formatting in the source register
  (`absent-defect-register.md:322-326`); the ids are `S048`, `S065`, `S068`, `S069`, `S070`.
- The register's `## By lane` table gives kasegi **2** rows because it counts only the
  `payload-absent` table (sum over lanes = 194 = the stated total). The five never-checked kasegi
  rows sit in the second section and are counted in that section's 109. Both counts are correct
  for what they measure; neither is a missing row.

## 1. Verdict labels used (four, as assigned)

| label | meaning |
|---|---|
| `present-and-located` | the quoted span occurs in the fetched source under the lane's fold discipline (raw, tag-stripped + whitespace-collapsed, whitespace-removed); location recorded |
| `absent` | the source fetched cleanly **and** the span is in none of the folds — the fabrication class; refuse the row |
| `unreachable` | no payload could be retrieved end-to-end; the quote was never checkable. **Not** a fabrication |
| `prose-class-unverifiable` | a payload was retrieved, but the quoted text is not a verbatim span of it — a field composite, an elision, or paraphrase — while its constituent facts are locatable. Not a fabrication; **not** adoptable as quoted either |

`prose-class-unverifiable` is deliberately distinct from `absent`: the register's own prose is
"a quote the checker could not match is a CANDIDATE, not a verdict" (register §preamble). A quote
that is a **reconstruction** of real page cells is a quote-form defect, and calling it fabrication
would be a false accusation; calling it `present-and-located` would overstate it.

## 2. Verdict table

| id | reg round | register class | cited source | live fetch (2026-10-26) | verdict |
|---|---|---|---|---|---|
| S037 | round1 | `payload-absent` | `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A` | `200`, 24,189 B, `text/html;charset=utf-8`, 0 redirects, sha256 `9cba2e96e343e1d0…` | **prose-class-unverifiable** (four-cell composite; every constituent located, no contiguous span) |
| S054 | round3 | `payload-absent` | `https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf` | `200`, 513,648 B, `application/pdf`, 0 redirects, sha256 `0150c9d15dee603f…` | **prose-class-unverifiable** (span drops an interpolated statutory parenthetical and crosses a line-wrap; corrected span located) |
| S048 | round2 | never checked | `https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3` | `404`, 748 B, `text/html;charset=utf-8` (Tomcat `HTTP状态 404 - 未找到`), sha256 `95cd25d80d88cce1…` | **unreachable** (dead as cited; endpoint host alive) |
| S065 | round4 | never checked | `http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf` | `200`, 7,465,472 B, `application/pdf` (31,710 B text), sha256 `e33b0f67293441f1…` | **present-and-located** (`刑法（7 件）` at `S065.txt:1182`; `现行有效法律目录（303 件）` at `:1`) |
| S068 | round4 | never checked | `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` | `301`→`301`→`200` (2 redirects) to `https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html`, 94,027 B, `text/html;charset=ISO-8859-1`, sha256 `098f99a89df3a801…` | **present-and-located** (sentence contiguous in tag-stripped, whitespace-collapsed text; same document as lane row **S040**, already `mined`) |
| S069 | round4 | never checked | `https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=…20_WD_2025005470_…指南.pdf` (register cell **truncated** at `…%E8%8D%89%2F`; full URL in §4) | `302` → `https://kass.sacinfo.org.cn/kfs/token/download/<token>`; certificate-verifying client **fails** (`curl` exit 60, 0 B); fetch with `-k` (and plain `http` on the token URL): `200`, **1,470,121 B**, `application/octet-stream`, 58-page PDF, sha256 `b0c046970f9ca2b7…` | **present-and-located** (anchor `6.3.1 技术分级` at `S069.txt:1019`) — with the transport caveat of §5 |
| S070 | round4 | never checked | `https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=…20_DI_2025005470_…指南.pdf` (register cell truncated likewise) | `302` → token URL; verifying client fails (`curl` exit 60); `-k`: `200`, **234,182 B**, `application/octet-stream`, 8-page PDF, sha256 `2eff0a5b10e2625e…` | **present-and-located** (`一、工作简况` at `S070.txt:8`, `1.1 任务来源` at `:9`, `20260806-T-469` at `:13`) — with §5 |

Totals: **present-and-located 4** (S065, S068, S069, S070) · **prose-class-unverifiable 2**
(S037, S054) · **unreachable 1** (S048) · **absent 0**.

## 3. Per-row evidence

### S037 — `payload-absent` → `prose-class-unverifiable`
Register quote (`absent-defect-register.md:99`, column 7):
`信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01`.

Fold result for that composite, computed by this seat over the fetched body:
`raw=False wscollapse=False nospace=False` (and `raw=False norm=False` in the shell pass).
Every **constituent** is present exactly once in the tag-stripped body:

```
标准状态 :: … 标准状态： 现行 在线预览 下载标准 实施信息反馈 中国标准分类号（CCS） L80 国际标准分类号（ICS） 35.040 发布日期 2020-11-19 实…
发布日期 :: … 发布日期 2020-11-19 实施日期 2021-06-01 主管部门 国家标准委 …
```

so the page is the GB/T 30279-2020 record the row intends (title cell `信息安全技术 网络安全漏洞分类分级指南`,
`现行`, `2020-11-19`, `2021-06-01`), and the quoted string is a **concatenation of four cells** with
the intervening cells (英文标准名称/在线预览/CCS/ICS) removed and a colon added to `发布日期`/`实施日期`
that the page does not render. Verdict `prose-class-unverifiable`: quote form, not fact fabrication.
A corrected row would quote cell-anchored fragments (`标准状态： 现行`; `发布日期 2020-11-19`).

### S054 — `payload-absent` → `prose-class-unverifiable`
Register quote (`absent-defect-register.md:100`, column 7): `脆弱性の悪用が確認されたもの又は疑われるもの`.
Folds: `raw=False wscollapse=False nospace=False`. The source sentence is:

```
S054.txt:46  （ア） 脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認
S054.txt:47       されたもの又は疑われるもの
```

The quote **deletes** the interpolated parenthetical `（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）`
and straddles a line-wrap. With the parenthetical restored the span is present under the
no-space fold (`fix54 nospace=True`, `wscollapse=False` — the wrap supplies a space), so the
correction path is concrete. Document identity confirmed independently: title
`重要電子計算機に対する不正な行為による被害の防止に関する法律等の施行を踏まえた脆弱性関連情報の取扱いについて（要請）`
(`pdfinfo` Title; Word-generated text layer), and the round-28 anchor `府 サ 連 第 ７ 号` is present
once in spaced form (`府連第7号` as written in the anchor list occurs 0 times — the PDF letterspaces it).

### S048 — never checked → `unreachable`
`curl` → `404`, 748 B; body:
`<title>HTTP状态 404 - 未找到</title>` … `HTTP状态 404 - 未找到`. The GB plan-record id is dead as
cited. Host `std.samr.gov.cn` is alive (it answers S069/S070 with `302`), so this is a dead
record id, not a dead host. No bytes, no quote checkable. Matches round 26 (`404 748`) and the
round-34 verifier spot-check (`404 748`, twice).

### S065 — never checked → `present-and-located`
`200`, 7,465,472 B, PDF (31,710 B `pdftotext -layout`). The staged anchors resolve verbatim:
`现行有效法律目录（303 件）` at `S065.txt:1`, `刑法（7 件）` at `S065.txt:1182` (inside the 刑法
section list). Register carries no quote for this row, so "located" is against the staged
catalogue anchors (`shokuknow/merge/kasegi` entry `chinese-statute-version-drift-…`, as recorded
by round 26). The row is real and quotable; nothing is adopted.

### S068 — never checked → `present-and-located`
`301` → `301` → `200` at `sec.cloudapps.cisco.com`, 94,027 B. Quote located contiguously once in
the tag-stripped, whitespace-collapsed document (offset 22,472; `raw=0` because the sentence is
split by inline markup in the HTML):

```
…responsible for responding to Cisco product security incidents. The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018 , which are guidelines for disclosure of potential vulnerabilities established by the International Organization for Standardization.…
```

**Id-collision fact (important for adoption):** this document is *already* lane row **S040**
(`corpus/SOURCES.md:46`, `mined` 2026-10-25, used by
`corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:2`). Staged id `S068` is the
legacy id of the same document (`renumber-map.md` §table: `S068 → S040`, keyed by URL). There is
nothing new to adopt here, and adopting "S068" in the lane would bind a registered id to a
document that belongs to S040.

### S069 / S070 — never checked → `present-and-located` (transport caveat §5)
Register cells truncate both URLs at `…%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F`; the full paths
this seat fetched are the ones in the round-28 hand-check list and the staged package's own rows
(`shokuknow/merge/kasegi/SOURCES.append.md:45-46`), i.e.
`20_WD_2025005470_网络安全技术 网络安全漏洞分类分级指南.pdf` (draft: `GB/T 30279—202X`, 代替
`GB/T 30279—2020`, ICS 35.030 / CCS L 80, 58 pp.) and
`20_DI_2025005470_网络安全技术 网络安全漏洞分类分级指南.pdf` (drafting note, 8 pp.).
Anchors located: `6.3.1 技术分级` (`S069.txt:1019`, under `6.3 漏洞分级方法` at `:1017`);
`一、工作简况` (`S070.txt:8`), `1.1 任务来源` (`:9`), plan number `20260806-T-469` (`:13`).

## 4. Transport caveat on S069 / S070 (measured this round)

- `curl` **with** certificate verification: `302` → `https://kass.sacinfo.org.cn/kfs/token/download/<token>`,
  then `curl: (60) SSL certificate … unable to get local issuer certificate (20)`, **0 B**.
- `openssl s_client`: leaf `C=CN, ST=北京市, L=北京市, O=国家市场监督管理总局国家标准技术审评中心,
  CN=*.sacinfo.org.cn`, issuer `C=CN, O=Beijing Xinchacha Credit Management Co., Ltd., CN=Xcc Trust OV SSL CA`,
  `verify error:num=21 … Verify return code: 21 (unable to verify the first certificate)` — the
  server does not send the intermediate, so a verifying client cannot build the chain. This is a
  **transport** fact about the attachment host, not an absence of payload.
- With `-k` (and over the same host on plain `http`, per the staged rows) the payload arrives:
  S069 `200` 1,470,121 B; S070 `200` 234,182 B. Corroboration independent of this seat: the
  campaign's staged row `S119` records the same DI attachment at **234 182 B** fetched 2026-10-24.
- Consequence for the verdict: the payload and both anchors are located, but a future re-check
  MUST NOT treat a verifying `curl` failure as "unreachable". Re-check with
  `curl -sSL -k` **or** plain `http://kass.sacinfo.org.cn/kfs/token/download/<token>` (the token
  is minted per request by the `std.samr.gov.cn` `302`).

## 5. Id-collision screen (register id vs lane id)

Required before any adoption, because the register's ids live in the campaign/staged space, not
the lane's (`renumber-map.md` §3). Lane registry at this round's base holds **51** rows (S001–S051).

| register id | lane row with the same id | same document? | consequence |
|---|---|---|---|
| S037 | `corpus/SOURCES.md:43` — Cybozu `FAQ（脆弱性報奨金制度）`, cited by `source: S037` in a knowledge entry (1 file) | **NO** (GB standard page vs Japanese bounty FAQ) | adopting register `S037` would land a GB record under an id a knowledge entry cites for Cybozu — forbidden |
| S048 | `corpus/SOURCES.md:54` — Microsoft MSVR, cited by `source: S048` in a knowledge entry (1 file) | **NO** (GB plan record vs MSVR) | same hazard |
| S054 | — none | — | free in the lane |
| S065 | — none | — | free in the lane |
| S068 | — none (its document is lane **S040**) | document already held | nothing to adopt |
| S069 | — none | — | free in the lane |
| S070 | — none | — | free in the lane |

`grep -cF` over `corpus/SOURCES.md` for the register sources: `openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE` → 0,
`ipa.go.jp/…/ug65p90000019by0-att` → 0, `std.samr.gov.cn/gb/search/gbDetailed` → 0,
`npc.gov.cn/c2597` → 0, `dcpspTools` → 0, `cisco.com` → 3 (S040 and its captures). So **none of the
seven register sources is registered in this lane**, and two of their ids are already bound to
different, load-bearing documents.

## 6. Adoption status: none

No row is adopted, and this file adopts nothing. Per-row reason:

- S037, S054 — not adoptable **as quoted** (`prose-class-unverifiable`); a corrected,
  cell-/parenthetical-anchored quote would have to be written and re-checked first.
- S048 — `unreachable`; adoption blocked until a `supersedes` row re-points at a live id.
- S065 — quotable, but the staged entry that cites it was never adopted by this lane, and the
  register carries no quote for the row; a hand-written quote would be new work, not an adoption.
- S068 — the document is already lane row S040; adopting it again would duplicate a source under
  a colliding id.
- S069, S070 — payload located, but re-checking depends on a TLS-bypass/plain-http fetch; a row
  whose verification path needs a transport exception should be adopted only with that exception
  recorded in its own row, which is a later-round decision, not this seat's.

This is the wave-4 quarantine-first rule as written: the package is not adopted until a row is
hand-checked **present**, and "present" here means present *and* adoptable as quoted under a
reproducible, verifying fetch.

## 7. Reproduction (all read-only; instrument UA from `corpus/instruments/capture-source.py:32`)

```
UA='kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)'
D=/fast/scratch/hyaku/kasegi-r35/ExecQuarantineSlice/bodies   # scratch only; removed before yield

curl -sS -L -A "$UA" 'https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A'  # 200 24189
curl -sS -L -A "$UA" 'https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf'   # 200 513648
curl -sS -L -A "$UA" 'https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3'     # 404 748
curl -sS -L -A "$UA" 'http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf'          # 200 7465472
curl -sS -L -A "$UA" 'https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html'  # 301->301->200 94027
U69='https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F20_WD_2025005470_%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF%20%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%BC%8F%E6%B4%9E%E5%88%86%E7%B1%BB%E5%88%86%E7%BA%A7%E6%8C%87%E5%8D%97.pdf'
U70='https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F20_DI_2025005470_%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF%20%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%BC%8F%E6%B4%9E%E5%88%86%E7%B1%BB%E5%88%86%E7%BA%A7%E6%8C%87%E5%8D%97.pdf'
curl -sS -L -A "$UA" "$U69"    # 302 then curl exit 60, 0 B
curl -sS -L -k -A "$UA" "$U69" # 200 1470121 (58 pp)
curl -sS -L -k -A "$UA" "$U70" # 200 234182  (8 pp)
```

Bodies, `pdftotext -layout` renders and normalized texts are in the seat's scratch dir until
yield; their sha256 prefixes are quoted in §2 so the fetch is identifiable, and the full digests
are in the seat receipt (`wave1/ExecQuarantineSlice.md`).

## 8. Limits of this check

- One fetch per URL, one UA, one time-of-day (`2026-10-26T06:32–06:44Z`). `std.samr.gov.cn` token
  URLs are per-request and transient; they are recorded only as observed redirect targets.
- S069/S070 were read with TLS verification off, as described in §4; no strict-verify content was
  retrieved from them, so a stricter future check will need the same exception or a mirror.
- This seat does not judge the round and does not decide adoption; the L1 integrates.
- **Divergence with the wave's gate seat, and its cause.** `wave1/ScribeGateAssimilation.md:94-95`
  records S069/S070 as `200, 0 B` and S068 as `403, 465 B`. Both are reproducible from the *inputs
  they used*, not a contradiction of the payload: S069/S070 were fetched there from the register's
  **truncated** cell (`…%E8%8D%89%2F`, a directory path) which answers `200` with an empty body,
  where §7 fetches the full `20_WD_…` / `20_DI_…` paths; and the Cisco URL answers `403` to a
  browser-style UA but `301→301→200` to the instrument UA with `-L` (recorded in round 25 and
  re-measured here). Both readings are in the record; the reconciliation is the L1's.
