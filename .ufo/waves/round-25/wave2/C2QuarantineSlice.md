# kasegi — absent-defect slice: independent re-derivation and falsification of the seven ScoutQuarantine verdicts (round 25, wave 2)

Read-only seat. Source repo `/home/vgpnk/Projects/shokuknow` untouched; VCS untouched (the
round-25 trees are untracked working-tree files — `git status --short .ufo/waves/round-25/`
→ `?? .ufo/waves/round-25/`); no process spawning, no installs (see Tooling). Only this file
was written.

## Target

1. Independently re-derive the kasegi absent-defect slice from the register.
2. Re-fetch all seven slice sources and re-check the seven verdicts in
   `.ufo/waves/round-25/wave1/ScoutQuarantine.md` (V1–V7 = the table rows S037/S054/S048/
   S065/S068/S069/S070; then the findings F1–F7 and the adoptability claim in section (c)).

## Verify: slice pin, command, output, count

- Pin: `sha256sum` of
  `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
  → `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, `wc -l` → 375,
  `stat -c %y` → `2026-10-24 08:37:00.746072780 -0300` — matches the wave-1 receipt exactly.
- Slice command, run verbatim (exit 0):

```
$ awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
    /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
 S037   `payload-absent`
 S054   `payload-absent`
 S048`   the cited source could not be fetched, so no quote was checked
 S065`   the cited source could not be fetched, so no quote was checked
 S068`   the cited source could not be fetched, so no quote was checked
 S069`   the cited source could not be fetched, so no quote was checked
 S070`   the cited source could not be fetched, so no quote was checked
```

`{n++} END{print n+0}` → `7`. Register rows: lines 99–100 (S037/S054, 7-column schema) and
322–326 (S048/S065/S068/S069/S070, 5-column schema, stray trailing backtick on the id).

## V1–V7: verdict-by-verdict falsification

Fetch method: `curl -sSL --max-time 60/120 -A 'Mozilla/5.0 (X11; Linux x86_64)' -o <out> <url>` /
`pdftotext -enc UTF-8 -layout`; see per-row notes. `http`/`bytes` below are the measured
`%{http_code}`/`%{size_download}`.

| # | id | register class | wave-1 verdict | my verdict | evidence (fresh, 2026-10-25) |
|---|---|---|---|---|---|---|
| V1 | S037 | `payload-absent` | present (fields; quote is not a span) | **CONFIRMED** | `http=200 bytes=24143`. Every quoted value true individually: `信息安全技术 网络安全漏洞分类分级指南` ×1, `2020-11-19` ×1, `2021-06-01` ×1, `现行` ×1. Assembled string `信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01` occurs **0** times in raw HTML and **0** times whitespace-normalized. The page renders `标准状态：` and `现行` on separate lines (`<td align="left">标准状态：` then `<span class="text-success">` + newline + `现行`); dates live in distinct `div.row` blocks (`col-xs-12 col-md-2 title` / `col-xs-12 col-md-4 content`). Not a fabrication; quote must be split per field. |
| V2 | S054 | `payload-absent` | present (elided; not verbatim) | **CONFIRMED** | `http=200 bytes=513648`; `pdftotext -layout` → 133 lines. Row quote `脆弱性の悪用が確認されたもの又は疑われるもの` occurs **0** times exactly and **0** whitespace-normalized; the fuller clause at the same anchor (§１．脆弱性関連情報の提供について → （ア）, lines 46–47) `脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの` occurs 0 exact / **1** whitespace-normalized — the row dropped the parenthetical statutory definition. True at anchor; not verbatim (Q9). |
| V3 | S048 | never checked | unverifiable as cited (404) | **CONFIRMED** | `http=404 bytes=748`, title `HTTP状态 404 - 未找到`. Live sibling plan record S091 (`…id=4C30E22D8B94BBB9E06397BE0A0A52F3`) `http=200 bytes=99903`; contains `基础信息`, `项目周期 16个月`, `下达日期 2026-03-02`, `TC260`, `全国网络安全标准化技术委员会`, `正在征求意见`; `范围和主要技术内容` **absent**, `公示` **absent**, quote `将原标准的技术分级和综合分级修订为两个独立的分级结果` occurs **0** times there. No fabrication verdict; not confirmed at any reachable URL. |
| V4 | S065 | never checked | present (page-break footer) | **CONFIRMED** | `http=200 bytes=7465472`; `pdftotext -layout` → 1295 lines; anchor ≈ lines 1182–1186 (`刑法（7 件）` entry 1, page footer `27` inserted inside the parenthetical). Quote `1． 中华人民共和国刑法（1979 年通过，1997 年修订，2009 年修正）` exact **0**; whitespace-squash with footer page-number lines removed → **1**, with footers → **0**. As-of line reads `（截至 2026 年 8 月 28 日 十四届全国人大常委会第二十四次…` — **August 28, 2026**, not September (the staged entry's "September 2026" remains wrong). |
| V5 | S068 | never checked | present (verbatim) | **CONFIRMED with two corrections** | See S068 note below. Quote present exactly once modulo the space-before-comma; the gate's access inversion DID reproduce today in the browser-UA form. |
| V6 | S069 | never checked | present (verbatim) | **CONFIRMED** | Endpoint `…gbPlan/download?path=…20_WD_…pdf` → `http=302` → `Location: https://kass.sacinfo.org.cn/kfs/token/download/skxkmhfwbqwstesu`; https fails `curl (60) SSL certificate … unable to get local issuer certificate`; over http → `200 bytes=1470121`, PDF 1.7, 58 pages. Quote `最后，结合漏洞技术分级和环境因素评分的结果，按照附录E计算得到网络安全漏洞综合分级。` exact **1** (line 1041). Anchors: `6.3.1 技术分级` line 25447, `6.3.2 综合分级` line 25783, `表D.1 漏洞技术分级表` line 45286, `表E.1 漏洞综合分级表` line 46021; TOC lines 47–56: 附录A–E 规范性, 附录F–I 资料性. |
| V7 | S070 | never checked | present (verbatim modulo line wrap) | **CONFIRMED** | Same endpoint `20_DI_…` → `302` → `hmhoguadnpeimovb`; https cert fails, http → `200 bytes=234182`, PDF 1.7, 8 pages. Quote `摆脱对国外标准体系（如《通用缺陷枚举（CWE）》、《通用漏洞评分系统（CVSS）》）的过度依赖` exact **0**, whitespace-normalized **0** (wrap splits `《通`/`用缺陷枚举（CWE）》、` and the second `《通用漏洞评分系统（CVSS）》` sits on its own line), whitespace-squash **1**. Anchors: `一、工作简况` line 85, `1.1 任务来源` line 94, `计划号：20260806-T-469` present split across lines (contiguous string 0, `20260806-T-469` present), `中国信息安全测评中心负责承办` line 194, `全国网络安全标准化技术委员会归口` line 233. |

### V5 detail (S068) — two corrections to the wave-1 receipt

- **Access.** Today `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html`:
  - default curl UA: `http=301` (60 B) → `Location: https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html` → `http=200 bytes=94027` — byte count equals the wave-1/round-24 94 027 B measurement;
  - Mozilla browser UA: `http=403 bytes=465` (`Access Denied`) at the original URL — **the gate's recorded inversion (403 to a browser UA, 200 to a plain client) DID reproduce today**, contrary to the receipt's "did not reproduce" (the wave-1 run saw the mirror: default UA 403, Chrome-fingerprint 200; the mechanism has shifted, the asymmetry has not).
- **Quote.** The page text contains `…The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018,\nwhich are guidelines…` — i.e. **no space before the comma**. The register's quote `…29147:2018 , which…` has a space before the comma; it occurs 0 times exactly, and 1 time under whitespace squashing. So the quote is present once and true at the anchor (`Cisco Product Security Incident Response`), but is **not byte-exact verbatim**: it carries one inserted space before the comma. The committed capture `corpus/source-snapshots/round-25/S040.txt:58` writes `…29147:2018,` (no space), and `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:46` quotes `…29147:2018"` without the space — consistent with this finding.
- **Expedite bullets (relevant to F3).** The page heading `Cisco may, however, expedite disclosure of a security vulnerability in the following situations:` is followed by exactly **four** `<li>` bullets (high-severity response complete; observed active exploitation; potential increased public awareness; third-party declared high profile), then the simultaneous-publication sentence. The following "heightened public awareness"/"active exploitation" sentences belong to a later, separate section. Four bullets, not two.

## Findings F1–F7: validation

| # | claim | outcome | evidence |
|---|---|---|---|
| F1 | slice is 7, not 2; two schemas; By-lane is stale/census-incomplete | **CONFIRMED** | 194 data rows in the ABSENT table (7-col), 109 in the NEVER-CHECKED table (5-col: lane/round/id/why/source). `## By lane` sums to 194 (only table 1). `lore` (9) and `mori` (3) appear in the never-checked table and are absent from By-lane. Table 1 spans round1–round7; never-checked spans round1–round10 (round8 ×1, round10 ×5); title "rounds 1-10" is right only for the union. |
| F2 | no fabrication in the slice | **CONFIRMED** | V1/V2: both rows are true in content at their anchors; the ABSENT verdict is an assembly/elision artifact. |
| F3 | S068 staged entry overclaims ("two conditions" vs four) | **CONFIRMED** | Page has four expedite bullets (above). `corpus/SOURCES.md:46` and the current reject ground both acknowledge four (`S040.txt` L301/L302–L304/L305–L308/L309). |
| F4 | no live home for S048's quote | **CONFIRMED** | S091 (200/99903 B) drops `范围和主要技术内容` and `公示`; the quoted sentence occurs 0 times there; cited URL is 404. |
| F5 | totals stale; `unreachable` class defined but never counted | **CONFIRMED** | 194 of 303 data rows totalled; `unreachable` defined (line 14) with count 0 in both tables. Census totals in `quote-lint-full-v5.json` = `rows 1901 quotes 4152 exact 2532 folded 1296 absent 324 no_url 31 fetch_failed 78 no_quote 141 positional 0`; 78+31=109 never-checked rows. |
| F6 | register ids are package ids, not lane ids | **CONFIRMED** | Register S037 names openstd GB/T 30279-2020; lane snapshot `corpus/source-snapshots/round-25/S037.txt` is the Cybozu bounty FAQ (`FAQ（脆弱性報奨金制度）…サイボウズ…`). Renumber map binds S036–S040 ↔ S055/S056/S057/S060/S068. |
| F7 | two committed artefacts disagree on S068 (claims.json reject on "unreachable") | **STALE — corrected in the current claims.json** | Current `claims.json` (frozen `2026-10-25T08:13:38Z`) no longer contains the "Cisco unreachable this round" ground; its `planned_reject` reads `vendor-cvd-policy-crosswalk-2026-10-23.md — refused as staged: Q3 claims two disclosure-trigger conditions but S040.txt L301-L309 has four; Q7 prose recheck; ground F20 absent. Cisco source itself was reachable and admitted as S040.` `corpus/lessons/round-25.md` documents this correction in place. The named reject is the staged *crosswalk file*, not the Cisco row — so the wave-1 section (c) result (S068 adoptable as S040) is corroborated by the current claims.json, corpus/SOURCES.md (S040 admitted, row 46), and the round-25 gate table (`S040 (S068)` captured, `b7f7b55f…`). What remains is the file-vs-row distinction, not the unreachability contradiction. |

## Wave-1 (c) adoptability claim

**CONFIRMED**, with the F7 refinement above: exactly one slice row is adoptable as lane id
S040 (Cisco, via the 301→sec.cloudapps destination), and the current committed artefacts
agree that S040 is admitted; the rejection named in claims.json targets the staged
`vendor-cvd-policy-crosswalk-2026-10-23.md` knowledge file (prose `recheck:`, missing F20
ground, two-vs-four bullet undercount), not the Cisco row. Renumber map still hedges
(`…whether the Cisco row is actually admitted or rejected is the C2 seat's call`), but the
other committed artefacts have resolved that call in favor of admission.

## Smallest corrections if the wave-1 result is deemed wrong

1. V5: replace "verbatim" with "present once; byte-exact modulo one inserted space before the
   comma (register `2018 ,` vs source `2018,`)". The S068 gate quote should be corrected to
   the snapshot's spelling `…ISO/IEC 29147:2018, which…`.
2. V5: strike the sentence "The gate block's recorded access inversion … did not reproduce
   today" — today the browser-UA/403 vs plain-client/200 asymmetry reproduced (via the
   redirect host); only the UA-specific side swapped.
3. F7: reframe as already resolved (claims.json corrected in place; reject = the staged file,
   not the row); the receipt's quoted "still lists … unreachable" text is an older version.
4. F3's anchor: the report cites `vendor-cvd-policy-crosswalk-2026-10-23.md:31`; that file
   was never admitted and is absent from `corpus/knowledge/` (only
   `vendor-disclosure-policy-commitments-crosswalk.md` and
   `vendor-disclosure-policies-as-corpus-objects.md` exist). The overclaim evidence stands on
   `corpus/SOURCES.md:46`, the four live bullets, and the reject ground, not on a staged file
   line.

## Commands / outputs / exits (selected)

- Pin: `sha256sum …absent-defect-register.md` → `5afe1810…bad833` (exit 0); `wc -l` → 375; `stat -c %y` → `2026-10-24 08:37:00.746072780 -0300`.
- Slice: awk command above → 7 lines (exit 0); `{n++} END{print n+0}` → 7.
- Tables: `awk` counts 194/109; By-lane sum 194; lane histograms include `lore 9`, `mori 3`; round histograms: table1 round1–7 (51/41/43/31/21/6/1), table2 incl. round8 ×1, round10 ×5; class values: table2 `$4` are the ids (`S048\`` etc.), confirming the 5-column schema and stray backtick.
- Census: `python3` json load of `quote-lint-full-v5.json` → totals exactly as above.
- Fetches: `s037 http=200 bytes=24143`; `s054 http=200 bytes=513648`; `s048 http=404 bytes=748`; `s091 http=200 bytes=99903`; `s065 http=200 bytes=7465472`; Cisco default-UA 301→200/94027, browser-UA 403/465; S069 302→https fail (curl exit 60)→http 200/1470121 (PDF 1.7, 58 pages); S070 302→http 200/234182 (PDF 1.7, 8 pages).
- Quote greps (python3): as listed in V1–V7.

## Tooling

No installs. `curl`, `pdftotext`/`pdfinfo` (poppler), `python3`, `awk`, `grep`, `sed`,
`sha256sum`, `stat`, `wc`, `file`, `cmp`, `find` — all pre-existing. No `pacman`, no `uv`,
no `npx`, no new binaries. RULES.md read before any tool use; no install/update record
required.
