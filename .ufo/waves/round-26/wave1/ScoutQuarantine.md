# Scout — kasegi quarantine slice hand-check (round 26, wave 1)

Seat: `L1Kasegi26.ScoutQuarantine`. Date: 2026-10-25 (UTC). Scope: the seven
kasegi rows in the absent-defect-register (`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`):
S037, S054 (payload-absent), S048, S065, S068, S069, S070 (could-not-be-fetched).
No production edits; verdicts one row per line in `quarantine-verdicts.txt`.

Instrument UA used for every fetch (lane capture UA):
`kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)` via
`curl -s -L`. No tools installed this run (curl, pdftotext, python3 already present).

## Verdicts (one row per line)

```
S037 fetched no-quote
S054 fetched no-quote
S048 unfetchable
S065 fetched quote-located
S068 already-mined-legacy
S069 unfetchable
S070 unfetchable
```

## Per-row evidence

### S037 — payload-absent — `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A`
- Fetch: HTTP **200**, 24,189 B, `text/html;charset=utf-8`, final URL unchanged.
- Staged quote (register): `信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01`.
- Location attempt: exact string absent in raw, whitespace-collapsed, and whitespace-removed body. All fact components ARE present but as separate table cells: 中文标准名称 = `信息安全技术 网络安全漏洞分类分级指南`; 标准状态 = `现行`; 发布日期 = `2020-11-19`; 实施日期 = `2021-06-01` (intervening fields 英文标准名称/在线预览/CCS/ICS/主管部门 separate them). The staged quote is a composite that concatenates cells; it never occurs contiguously (also `发布日期：2020-11-19` punctuation differs from the page's cell rendering).
- Verdict: **fetched no-quote**.
- Absence meaning for adoption: the catalogue page is reachable and authentic (GB/T 30279-2020 record), but the standard's body sits behind the preview tool; the staged quote is not verbatim anywhere. Adoption of the row as staged is not possible without re-quoting to cell-anchored fragments (e.g. `标准状态：现行`); the substantive facts verify, so this is a quote-form defect, not evidence of fabrication of the underlying metadata.

### S054 — payload-absent — `https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf`
- Fetch: HTTP **200**, 513,648 B, `application/pdf`, final URL unchanged; Word-generated text layer (pdfinfo: 重要電子計算機に対する不正な行為による被害の防止に関する法律等の施行を踏まえた脆弱性関連情報の取扱いについて（要請）).
- Staged quote (register): `脆弱性の悪用が確認されたもの又は疑われるもの`.
- Location attempt: exact string absent in raw/collapsed/nospace text. The real sentence is `…脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認` + line-wrap + `されたもの又は疑われるもの` — i.e. the quoted span is split by a line break and interpolated with a legal-citation parenthetical; it is not verbatim.
- Verdict: **fetched no-quote**.
- Absence meaning for adoption: source is real and the semantic content checks out, but the staged quote is a shortened re-construction. The row cannot be adopted with that quote verbatim; a corrected longer fragment (including the parenthetical) would be needed. (Round-24 lesson also recorded it as not cited by that round's entries.)

### S048 — could-not-be-fetched — `https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3`
- Fetch: HTTP **404**, 748 B, `text/html` (Tomcat 9.0.122 error: `gbDetailed.jsp 未找到`). Endpoint is alive (see S091 sibling id 200 in round-24 evidence); this plan-record id is dead as cited.
- Verdict: **unfetchable** (dead as cited; no quote checkable). Adoption blocked until a `supersedes` row re-points at a live id (round-24 lesson's flip condition).

### S065 — could-not-be-fetched — `http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf`
- Fetch: HTTP **200**, 7,465,472 B, `application/pdf` (pdftotext: 31,899 chars; 现行有效法律目录 dated 2026-09).
- Staged claims (package entry `chinese-statute-version-drift-2026-10-23-r4-amendment.md`): heading `刑法（7 件）`, entry 1 `中华人民共和国刑法（1979 年通过，1997 年修订，2009 年修正）`, `现行有效法律目录`.
- Location: `现行有效法律目录（303 件）`, `刑法（7 件）`, `2009 年修正）` all present verbatim; the long clause appears split only by a PDF line-wrap between `修订` and `2009` (normalization-visible, content intact).
- Verdict: **fetched quote-located** (fragments verbatim; full clause wrapped at a line break).

### S068 — could-not-be-fetched — `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html`
- Fetch: instrument UA → HTTP **301** → `https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html`, HTTP **200**, 94,027 B. (Browser UA is 403 — verified in round-25 verifier spotcheck `corpus/lessons/round-25-verifier-spotcheck.md` line 114 and routed defect R25-5.)
- Staged quote (`vendor-cvd-policy-crosswalk-2026-10-23.md` / `iso-29147-divergence-and-clause-crosswalk-2026-10-23.md`): `The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018`.
- Location: contiguous match found — first 80 chars: `The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018 , which are guidelines for disclos…`
- Verdict: **already-mined-legacy** (per assignment instructions). Cisco policy was adopted round 25 as lane source **S040** (`corpus/SOURCES.md` S040, mined 2026-10-25, capture sha256 `b7f7b55f…`, quote located at capture line 58); the old staged S068 is the legacy id of the same document. The round-25 verifier spotcheck verified the 301→200/UA note and full four-bullet expedite list; this fetch re-confirms body and quote on 2026-10-25.

### S069 / S070 — could-not-be-fetched — `https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=…` (`…20_WD_2025005470_…指南.pdf` / `…20_DI_2025005470_…指南.pdf`)
- Fetch: HTTP **302**, 0 B, no body; redirect target `https://kass.sacinfo.org.cn/kfs/token/download/<token>` fails TLS (curl exit 60 — peer certificate problem; direct probe of the kass URL returns code=000). No bytes are retrievable end-to-end.
- Verdict: **unfetchable** (both). Matches round-24 lesson's `302/0 B unreachable as cited`. No quote checkable; the planned-standard draft (GB/T 30279—202X WD/DI) remains unverifiable from these endpoints.

## Cross-cutting notes
- Register classes confirm: the two payload-absent rows are reachable but the staged quotes are not verbatim (form defects), so neither is appendable as staged; the five could-not-be-fetched rows are now re-tested — S065 and S068 resolve to real, quotable content (S068 already mined as S040), S048 is dead as cited, S069/S070 are genuinely unfetchable.
- All HTTP codes/bytes above are from today's own fetches (2026-10-25 UTC).
