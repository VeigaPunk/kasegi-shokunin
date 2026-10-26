# ScoutQuarantine — round 36: kasegi quarantine slice re-derived, one live fetch per row

Seat: ScoutQuarantine (leaf scout, no subagents, nothing adopted, nothing written outside this receipt and scratch).
Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (HEAD at read time `b47f2cdf`, the claims-freeze commit).
`/home/vgpnk/Projects/shokuknow` read-only (register and package read; no campaign tool run).
Scratch `/fast/scratch/hyaku/kasegi-r36/ScoutQuarantine/` (removed after this file was written).
Fetches `2026-10-26T15:37:16Z`–`15:38:00Z`, exactly **one** `curl -sS -L --max-time 30` per row, UA
`kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)` (= `corpus/instruments/capture-source.py:32`), TLS verified (no `-k`).
Tools: `curl 8.23.0`, `pdftotext 26.08.0`, `python3`. Nothing installed; no pacman.

Result in one line: **slice = the same 7 rows, byte-equal to the round-35 committed slice (`d02acb68…`). Verdicts: S037 absent (quote-form defect, facts hold), S054 absent (same), S048 unreachable (404), S065 unreachable *this probe* (30 s timeout, 9 % of bytes, no content check), S068 present-and-located (= lane S040), S069/S070 unreachable (TLS verify failure, curl 60, 0 B). Adopted: 0.**

## 1. Slice re-derivation (frozen awk, verbatim from `round-35/assimilation/quarantine-verdicts.md` §0)

```console
$ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
$ awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" ; echo awk_exit=$?
 S037   `payload-absent`
 S054   `payload-absent`
 S048`   the cited source could not be fetched, so no quote was checked
 S065`   the cited source could not be fetched, so no quote was checked
 S068`   the cited source could not be fetched, so no quote was checked
 S069`   the cited source could not be fetched, so no quote was checked
 S070`   the cited source could not be fetched, so no quote was checked
awk_exit=0     (7 lines, 417 B, 7/7 carry an S-id)
$ cmp slice .ufo/waves/round-35/assimilation/quarantine-slice   -> equal (sha256 d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862 both)
```

Register `absent-defect-register.md` sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833` — unchanged since rounds 33–35.
Register lines: 99 (S037, round1), 100 (S054, round3), 322 (S048, round2), 323–326 (S065/S068/S069/S070, round4). Ids on 322–326 carry a stray trailing
backtick in the register's own cell (`S048\``); the ids are S048, S065, S068, S069, S070. The `## By lane` count of 2 for kasegi counts only the
payload-absent table; the five never-checked rows sit in the second section (lines 322–326). Neither count is a missing row.

id + class per row (as printed): S037 `payload-absent` · S054 `payload-absent` · S048/S065/S068/S069/S070 never-checked (`the cited source could not be fetched, so no quote was checked`).

## 2. Verdict table

Labels: `present-and-located` (quote/anchor occurs in the fetched source, location recorded) · `prose-class-unverifiable` (payload retrieved, quoted text not a verbatim span, constituents locatable) ·
`unreachable` (no payload end-to-end; quote never checkable; not a fabrication) · `absent` (source fetched cleanly, span in none of the folds F1 raw / F2 tag-strip+ws-collapse / F3 ws-removed).

| id | reg class | cited source (fetched URL) | status | bytes | sha256 (prefix) | redirects | verdict |
|---|---|---|---|---|---|---|---|
| S037 | payload-absent | `openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE…7DE7A` | 200 `text/html;charset=utf-8` | 24,189 | `9cba2e96e343e1d0` | 0 | **absent** (span 0/0/0; see note A) |
| S054 | payload-absent | `ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf` | 200 `application/pdf` | 513,648 | `0150c9d15dee603f` | 0 | **absent** (span 0/0/0; see note A) |
| S048 | never checked | `std.samr.gov.cn/gb/search/gbDetailed?id=3B865A93…52F3` | **404** `text/html` (Tomcat `HTTP状态 404 - 未找到`) | 748 | `95cd25d80d88cce1` | 0 | **unreachable** (dead as cited; no quote exists to check) |
| S065 | never checked | `npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf` | 200 headers, then **curl exit 28** timeout at 30.00 s | 677,543 of 7,465,472 (9.1 %) | `23c73742…` (partial) | 0 | **unreachable** (this probe; see note B) |
| S068 | never checked | `cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` → `sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html` | 200 `text/html;charset=ISO-8859-1` | 94,027 | `098f99a89df3a8018ab6eff7529fd8482af70dde` | 2 (301→301→200) | **present-and-located** (duplicate of lane S040; see note C) |
| S069 | never checked | full staged URL `std.samr.gov.cn/dcpspTools/gbPlan/download?path=…20_WD_2025005470_…指南.pdf` | 302 → `kass.sacinfo.org.cn/kfs/token/download/ltwffirakqlbdrdz`; **curl exit 60** (`unable to get local issuer certificate`) | 0 | none | 1 | **unreachable** (verified TLS fails; see note D) |
| S070 | never checked | full staged URL `…20_DI_2025005470_…指南.pdf` | 302 → `kass.sacinfo.org.cn/kfs/token/download/sakjodkwbcklzvsl`; **curl exit 60** | 0 | none | 1 | **unreachable** (same; note D) |

S068 full sha256 `098f99a89df3a8018ab6eff7529fd8482af70dde6406472b88d526c773ded807`.

### Located-quote evidence (counts F1 raw / F2 / F3; `chk.py`, exit 0)

```
S037 whole register quote  信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01   0/0/0
  fragments: 信息安全技术 网络安全漏洞分类分级指南 1/1/1 | 标准状态：现行 0/0/1 | 发布日期2020-11-19 0/0/1 (spaced form 0/1/1) | 实施日期2021-06-01 0/0/1 (spaced 0/1/1) | GB/T 30279-2020 2/2/2
S054 pdftotext -layout (9,780 chars; lines 46-47)  whole register quote 脆弱性の悪用が確認されたもの又は疑われるもの 0/0/0 ; 脆弱性の悪用が確認されたもの 0/0/0 ;
  又は疑われるもの 1/1/1 ; されたもの又は疑われるもの 1/1/1 ; （法第 42 条第１項に規定する脆弱性をいう。以下同じ。） 1/1/1 ;
  full clause 脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの  0/0/1 (F3 only; line-wrap between 確認 / されたもの)
  text: "（ア） 脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認 / されたもの又は疑われるもの"
S048 body text 630 chars = Tomcat 404 page: 未找到 3/3/3 ; 20260806-T-469 0/0/0 ; 基础信息 0/0/0 ; 项目周期 0/0/0  (nothing to anchor against)
S068 Cisco Product Security Incident Response 4/4/4 | Disclosure of Security Vulnerabilities 2/2/2 | ISO/IEC 29147 1/1/1 | CERT/CC 2/2/2 |
  "The Cisco PSIRT aligns its practices with" 1/1/1 | "has observed active exploitation of a vulnerability that could lead to increased risk for Cisco customers" 0/1/1
S065 no content check: PDF truncated (`%PDF-1.7` header, no xref/trailer); pdftotext exit 1 "Couldn't find trailer dictionary"
S069/S070 no payload
```

### Notes

- **A (S037/S054 label).** Both are real documents; the register quotes are *reconstructions*. S037's quote is a four-cell composite (`标准状态：现行`, `发布日期`, `实施日期`
  are separate page fields; each fragment located once under F3, none contiguous, the inserted `：` after 发布日期/实施日期 is absent). S054's quote elides the statutory parenthetical
  `（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）` and crosses a line wrap; only the tail and the full clause (F3) are located. I file both as **`absent`** under the register's own
  definition (`payload-absent` = source fetched cleanly, span in none of the folds) — this **confirms** the register class and is a quote-form defect, **not** a fabrication accusation; the facts
  (GB/T 30279-2020 current, 发布 2020-11-19 / 实施 2021-06-01; trigger (ア) exploitation confirmed or suspected) hold. The round-35 ExecQuarantineSlice seat filed the same facts under
  `prose-class-unverifiable` (verdicts §1); the round-35 ScoutQuarantine filed `absent`. Facts and the flip condition (re-stage cell-anchored / full-clause spans after a lane row exists) are identical either way; the L1 should write one label.
- **B (S065).** The run is bounded to one fetch and 30 s. The host answered 200 `application/pdf` but delivered 677,543 of 7,465,472 B in 30 s (slow today; rounds 33–35 fetched the full 7,465,472 B,
  sha `e33b0f67…`, within the cap). The truncated body has no trailer and cannot be extracted, so **no anchor was checked this round**. The label is `unreachable` for this probe's
  contract (no complete payload within 30 s), **not** a source defect and not a fabrication. Earlier-round anchors (`现行有效法律目录`, `刑法（7件）`, `刑法修正案（十二）（2023年）` located; staged
  "catalogue dated 2026年9月" absent, entry-1 page-number splice) are **not re-verified here**. A re-fetch with a larger cap would be a second fetch and was out of this item's contract.
- **C (S068).** Reached only with the instrument UA (2 redirects, `sec.cloudapps.cisco.com`); a browser-style UA returned 403/465 B in the round-35 UA matrix (not re-run). Lane `corpus/SOURCES.md:46` row
  `S040` carries the identical URL (`cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html`), so the staged S068 is a duplicate of lane S040 (round 25 capture sha `b7f7b55f…` per round-26 lesson; this
  fetch sha `098f99a8…` equals the round-35 value). The register carries no quote for this row; located anchors are the section titles and the two sentences above. No new row needed.
- **D (S069/S070).** The register's cited cell is truncated (`…%2F`); a fetch of that URL returns 200/0 B in earlier rounds (not re-run). I fetched the full staged URL from
  `merge/kasegi/SOURCES.append.md:45-46`. The 302 token URL host `kass.sacinfo.org.cn` fails verified TLS here (curl 60). Under a reproducible verifying fetch these are `unreachable`. Earlier
  rounds got 1,470,121 B / 58 pp (S069) and 234,182 B / 8 pp (S070) only with `-k` or plain http; those readings are **not re-measured here** (no second fetch). Token URLs change per request
  (`ltwffirakqlbdrdz`, `sakjodkwbcklzvsl` now), so a manifest cannot bind the final URL.

## 3. Comparison with round 35 (read after my own fetches)

| id | r35 ScoutQuarantine | r35 ExecQuarantineSlice | r36 (this seat) |
|---|---|---|---|
| S037 | absent | prose-class-unverifiable | absent — bytes identical (`9cba2e96…`) |
| S054 | absent | prose-class-unverifiable | absent — bytes identical (`0150c9d1…`) |
| S048 | unreachable | unreachable | unreachable — 404/748 B identical (`95cd25d8…`) |
| S065 | present-and-located (anchor level, conditional) | present-and-located | **unreachable this probe (timeout)** — differs by transport only |
| S068 | present-and-located (dup of S040) | present-and-located | present-and-located — bytes identical (`098f99a8…`) |
| S069 | unreachable under verified TLS | present-and-located (transport caveat) | unreachable (curl 60, 0 B) |
| S070 | unreachable under verified TLS | present-and-located (transport caveat) | unreachable (curl 60, 0 B) |

Tally r36: present-and-located 1 (S068) · absent 2 (S037, S054) · unreachable 4 (S048, S065 [timeout], S069, S070) · prose-class-unverifiable 0.
Unchanged vs r35 on all five bytes-identical fetches (S037, S048, S054, S068 and the S069/S070 TLS failure); the only movement is S065's transport.

## 4. Disposition (no adoption)

Adopted: **0**. S037/S054 not adoptable as quoted (flip: lane row first, then cell-anchored / full-clause span). S048 dead as cited. S065 not checked this round (needs a fetch over 30 s; a lane
row and anchor set exist from rounds 33–35 evidence, but nothing here confirms them). S068 already lane S040. S069/S070 not adoptable under verified TLS. Id-collision rerun is out of this item's scope (not run).

## 5. Evidence digests

```
d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862  slice (7 lines; == round-35 committed)
5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833  register
4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb  package SOURCES.append.md (read for S069/S070 full URLs; not re-hashed this run beyond the earlier sha256sum, value matches r35)
9cba2e96e343e1d0c95d23fb50454fa1321cb2d01af6ae318653290a1d20f204  S037 body
95cd25d80d88cce1e08528c03d5eb488f56bf9991f820bc31569b001eb2e2436  S048 404 body
0150c9d15dee603f55573f4692f306ba8ff46f70454b032f813b95fbdbb12b88  S054 body
23c737428244b13d1efd152a75f8b5060d140f52d29c97c41772b79176a6d69a  S065 partial body (677,543 B)
098f99a89df3a8018ab6eff7529fd8482af70dde6406472b88d526c773ded807  S068 body
```

Not done: no `-k`/second fetches (one fetch per row), no source-recheck/harness/quote-lint/renumber campaign tools, no id-collision rerun, no write outside this receipt and scratch.
