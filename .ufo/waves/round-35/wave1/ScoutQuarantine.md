# ScoutQuarantine — round 35: independent re-derivation of the kasegi quarantine slice, cross-check of ExecQuarantineSlice

Seat: ScoutQuarantine (leaf, no subagents, no adoption). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `3266c993`, claims-freeze `617496b9`; working copy parent `da2d3c68`). `/home/vgpnk/Projects/shokuknow` read-only
(register and package read; no campaign tool run; nothing written there). Only this receipt was written in the lane.
Scratch `/fast/scratch/hyaku/kasegi-r35/ScoutQuarantine/` (deleted after this receipt was written). Probes ran
`2026-10-26T06:36Z`–`06:55Z`. UA for lane-style fetches: `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`
(= `corpus/instruments/capture-source.py:32`). Tools: `curl`, `pdftotext 26.08.0`, `python3`; one ephemeral
`uv run --no-project --with pymupdf` (PyMuPDF 2.0, uv channel, nothing persisted, reason: second extractor for S065). Nothing installed; no pacman.

Result in one line: **slice = the same 7 rows as ExecQuarantineSlice (byte-equal); my verdicts agree with the executor's on
facts and on 3 of 7 labels; the executor's labels differ from mine on S037/S054 (label only), S065 (omitted three defects),
S069/S070 (strict-TLS vs `-k`). 0 adopted by either seat. Collisions are now 22 (S031–S052), not 21: the lane registry grew to 52 after the executor's snapshot.**

## Report

### 1. Slice re-derivation (command as given)

```console
$ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
$ awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' $R ; echo exit=$?
 S037   `payload-absent`
 S054   `payload-absent`
 S048`   the cited source could not be fetched, so no quote was checked
 S065`   the cited source could not be fetched, so no quote was checked
 S068`   the cited source could not be fetched, so no quote was checked
 S069`   the cited source could not be fetched, so no quote was checked
 S070`   the cited source could not be fetched, so no quote was checked
exit=0   (the `exit=0` is the pipeline's last command; 7 lines; 7/7 carry an S-id)
$ cmp <(awk … $R) .ufo/waves/round-35/assimilation/quarantine-slice ; echo slice-cmp-equal      -> equal
$ awk … (round + class projection) $R | diff - .ufo/waves/round-35/assimilation/quarantine-slice-rederived ; echo rederived-equal -> equal
```

| artefact | sha256 |
|---|---|
| register `absent-defect-register.md` (83,621 B, mtime 2026-10-24 08:37) | `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833` (unchanged since r33/r34) |
| package `merge/kasegi/SOURCES.append.md` | `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb` (unchanged) |
| executor `assimilation/quarantine-slice` (417 B) | `d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862` = round-34 committed slice, byte-equal |
| `assimilation/quarantine-slice-rederived` | `7696d76c4f17d1d9f41598e7c36def077e1f7429d947639726afdebf6e528f31` |
| `assimilation/quarantine-verdicts.md` (executor) | `b086936919174837f48e04b4209794cc7738716a25abaae3396d43a2dfe5b5a0` |

Register lines: 99 (S037, round1), 100 (S054, round3), 322–326 (S048 round2; S065/S068/S069/S070 round4). **No discrepancy on the slice.**
(The two-row `## By lane` count of 2 for kasegi counts only the payload-absent table; the five never-checked rows sit in the second section — executor's note is correct.)

### 2. Independent live fetches (single-shot, instrument UA, `-L`), compared with the executor's R2

| id | my probe (06:37Z) | sha256 | executor (06:32Z) | match |
|---|---|---|---|---|
| S037 | 200, 24,189 B html | `9cba2e96e343e1d0c95d23fb50454fa1321cb2d01af6ae318653290a1d20f204` | 200, 24189, `9cba2e96…` | yes |
| S048 | 404, 748 B (twice); control `https://std.samr.gov.cn/` 200 109,107 B | `95cd25d80d88cce1e08528c03d5eb488f56bf9991f820bc31569b001eb2e2436` | 404 748 `95cd25d8…` | yes |
| S054 | 200, 513,648 B pdf | `0150c9d15dee603f55573f4692f306ba8ff46f70454b032f813b95fbdbb12b88` | 200 `0150c9d1…` | yes |
| S065 | 200, 7,465,472 B pdf, 30 pp | `e33b0f67293441f19ee519b2ed1619121da84867aa8396a3a16facd572586d83` | 200 `e33b0f67…` | yes |
| S068 | 301→301→200 (`sec.cloudapps.cisco.com`), 94,027 B | `098f99a89df3a8018ab6eff7529fd8482af70dde6406472b88d526c773ded807` | same `098f99a8…` | yes |
| S069 (full staged URL, 306 chars) | 302 → `kass.sacinfo.org.cn/kfs/token/download/<token>`; verified TLS: **curl exit 60**, 0 B; `-k`: 200, 1,470,121 B, PDF 1.7 58 pp | `b0c046970f9ca2b7bbfae5ee8e847ec0c630049aec1863fe3d5a0a62718e91a9` | same `b0c04697…` | yes |
| S070 (full staged URL) | same shape; `-k`: 200, 234,182 B, 8 pp; **plain-http token URL: 200, 234,182 B, same hash** | `2eff0a5b10e2625e7d3a5b45c50992f018dde967cf16c97b38557186cdfb3f95` | same `2eff0a5b…` | yes |
| S069 (register's truncated cell `…%E8%8D%89%2F`) | 200, **0 B** | `e3b0c442…b855` (sha of empty) | executor notes it | yes |

Every payload hash is byte-identical to the executor's and to the round-34 ScoutQuarantine receipt (the sources did not move). Token URLs differ per request
(`jentpnvrcitmvnus`, `nkykdtrewmnyqxpv`, `qevumbeftylmwill`, … ) so a manifest cannot bind the final URL; bytes are stable.

S068 UA matrix (explains the ScribeGateAssimilation divergence the executor flagged, §8 of its verdicts file):
`kasegi-shokunin/1.0` → 200/94,027 B (2 redirects); `curl/8.23.0` → 200/94,027 B (2 redirects); `Mozilla/5.0 (X11; Linux x86_64) … Chrome/124 Safari/537.36` → **403/465 B, 0 redirects**. Both readings reproduce; the 403 is a browser-UA artefact, not host unreachability.

### 3. Content checks (counts at F1 raw / F2 whitespace-collapsed / F3 whitespace-removed; script `chk.py`, exit 0)

```
S037 whole register quote (信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01)   F1=0 F2=0 F3=0
  信息安全技术 网络安全漏洞分类分级指南  1 1 1 | 标准状态：现行  0 0 1 | 发布日期2020-11-19  0 0 1 | 实施日期2021-06-01  0 0 1 | GB/T 30279-2020  2 2 2
S054 whole register quote 脆弱性の悪用が確認されたもの又は疑われるもの   0 0 0 ; 脆弱性の悪用が確認されたもの 0 0 0 ; 又は疑われるもの 1 1 1 ; されたもの又は疑われるもの 1 1 1
  pdftotext -layout lines 46–47: （ア） 脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認 / されたもの又は疑われるもの
S048 body: Tomcat `HTTP状態 404 - 未找到` (630 chars of text) -- nothing to anchor against
S065 see §4
S068 Cisco Product Security Incident Response 4 4 4 | Disclosure of Security Vulnerabilities 2 2 2 | ISO/IEC 29147 1 1 1 | CERT/CC 2 2 2
     "…has observed active exploitation of a vulnerability that could lead to increased risk for Cisco customers." F1=0 F2=1 F3=1
     "…has completed the incident response process for a high-severity vulnerability and public disclosure of code fixes is planned…" 1 1 1
S069 (-k bytes, pdftotext -layout, 87,900 chars) GB/T 30279 76 | 202X 56 | 6.3.1 1 | 6.3.2 1 | 表A.1 5 | 表D.1 2 | 表E.1 2 | 可利用性评分表 3 | 环境因素评分表 3 | 漏洞技术分级表 3 | 漏洞综合分级表 3
S070 (-k bytes, 7,763 chars) 20260806-T-469 1 | 中国信息安全测评中心 5(F3 7) | 任务来源 1 | 制定背景 1 | 起草单位 1 | 工作简况 1 | CWE 6 | CVSS 5
```

S054: line numbers 46–47 here match the executor (`S054.txt:46-47`); my round-34 receipt said 44–47 (different render), immaterial.

### 4. S065 — new measurements that the executor's `present-and-located` omits

```
extractor: pdftotext 26.08.0 (default 14,197 chars; -layout 16,630 chars; -raw 14,025) and PyMuPDF 2.0 (13,946 chars), same file sha e33b0f67…
现行有效法律目录                                   1   (title line: 现行有效法律目录（303 件） / 截至 2026 年 8 月 28 日 十四届全国人大常委会第二十四次会议闭幕)
刑法（7件）                                         1
中华人民共和国刑法（1979年通过，1997年修订，2009年修正）   F3=0   — entry 1 is page-number-spliced: …1997年修订，27 2009年修正）… (pdftotext; "28" under PyMuPDF round 34)
中华人民共和国刑法修正案（十二）（2023年）             1
2026年9月                                          F3=0   — the staged row's "catalogue dated 2026年9月" is not in the text (URL path 202609 is the publish month)
截至2026年8月28日                                    1
amendment ledger: 1999年(no 一), 二 … 十二 each 1  => 12 amendment entries, first printed as 刑法修正案（1999年）
```

(1) `2026年9月` is not in the document (stated date is 截至 2026-08-28). (2) The 刑法 entry 1 cannot be quoted verbatim across the page-number splice. (3) My round-34 gap "11 of 12 amendments" is **closed**: the first amendment is printed `刑法修正案（1999年）` without `（一）`, so 12 of 12 are present. The executor's `S065.txt:1182` `刑法（7 件）` locator is real (I find the same anchor); its label omits (1) and (2).

### 5. Verdict comparison (assigned label set: present-and-located / absent / unreachable / prose-class-unverifiable)

| id | register class | ExecQuarantineSlice verdict | this seat's verdict | agree? | note |
|---|---|---|---|---|---|
| S037 | payload-absent | prose-class-unverifiable | **absent** (hand-confirmed: whole span 0/0/0; 4 fragments each located once under F3; facts hold) | **LABEL DIFFERS, facts agree** | executor redefines `absent` as fabrication-only and files an unmatched collage under `prose-class-unverifiable` (verdicts §1). Round 33/34 lessons say `refuse`. Under the register's own definition (`payload-absent` = fetched cleanly, in none of them) the register class is *confirmed*, not downgraded. Both carry the same flip condition (cell-anchored fragments). The L1 should write one label in the Gate; "prose-class-unverifiable" is not a label the r33/r34 Gates used. |
| S054 | payload-absent | prose-class-unverifiable | **absent** (whole 0/0/0; parenthetical elided; tail 又は疑われるもの located 1/1/1; corrected span present under F3 only) | **LABEL DIFFERS, facts agree** | same reason as S037 |
| S048 | never checked | unreachable | **unreachable** (404 twice, root 200) | agree | |
| S065 | never checked | present-and-located | **present-and-located at anchor level, conditional** | label agrees, **scope differs** | the register carries no quote for S065; located anchors = title, 303, 刑法（7件）, 附件一/二, 修正案（十二）; NOT located = "2026年9月"; entry 1 spliced (§4). Executor mentions neither. "Quotable" overstates: the catalogue-date claim in the staged row is wrong. |
| S068 | never checked | present-and-located (= lane S040) | **present-and-located, duplicate of lane S040** | agree | executor's anchor (ISO/IEC 29147:2018 sentence at offset 22,472) differs from mine but both are located; no adoption |
| S069 | never checked | present-and-located (transport caveat) | **unreachable under verified TLS; present only with `-k`/plain http (anchor-level)** | **POLICY DIFFERS, bytes agree** | same hashes. The executor's own §6 says "present" means "adoptable as quoted under a reproducible, verifying fetch" and then labels S069/S070 present-and-located anyway; under that rule they are `unreachable`. Executor's §R8 (2) acknowledges the choice is the L1's. |
| S070 | never checked | present-and-located (transport caveat) | same as S069 | same | plain-http (`http://kass.sacinfo.org.cn/kfs/token/download/<token>`, token minted by the 302) re-verified here: 200, 234,182 B, sha `2eff0a5b…` — the executor's plain-http claim holds |

Tally, mine: present-and-located 2 (S065 conditional, S068) · absent 2 (S037, S054) · unreachable 3 (S048, S069, S070 — S069/S070 reachable only by a transport exception) · prose-class-unverifiable 0.
Tally, executor's: present-and-located 4 · prose-class-unverifiable 2 · unreachable 1 · absent 0.
Net disposition is identical in both: **0 adopted, 2 not adoptable as quoted, rest not adoptable now**; nothing changes the lane.

### 6. Further discrepancies and checks

1. **"Standing verdict correction" (executor R8 #1) is not new.** The executor says rounds 24/26 recorded S069/S070 as `unfetchable`. Round 34's ScoutQuarantine (`.ufo/waves/round-34/wave1/ScoutQuarantine.md` §2, `-k` diagnostic) already measured the same `-k` bytes (1,470,121 B / 58 pp; 234,182 B / 8 pp; identical hashes) and classified S069/S070 `unreachable` on TLS grounds; the r34 lesson's `200, 0 B` for S069/S070 is the truncated-register-URL artefact (`…%E8%8D%89%2F` → 200 empty), which both the executor and I reproduce. What is new at round 35 is only the *label* choice for the bytes that already existed.
2. **Round-34 claim that `pdftotext` returns 0 chars for S065 does not reproduce.** Same file hash `e33b0f67…`, same `pdftotext 26.08.0`: 14,197 chars default / 16,630 `-layout` (executor: 31,710 B). That claim exists only in the r34 ScoutQuarantine receipt (§3 S065, §4 defect (c) "any recheck must name an extractor"); `grep -n pdftotext corpus/lessons/round-34.md` → no hit, so no lane artefact states it. Hypothesis [INFERENCE]: a stderr-warning/stdout handling error in that r34 run; not investigated further. Do not carry "needs PyMuPDF" into a future S065 row.
3. **Id-collision counts have moved since the executor's snapshot.** Live `corpus/SOURCES.md` now holds **52** ids (S001–S052; sha256 `510e3bba977a744382438fdb7b79ecce90a75e1590f2491e9f373ab88d9b8829`). Fresh extract with the 0–3-space pattern `^ {0,3}\|[[:space:]]*S[0-9]{3,}`: `reg=52 staged=94 collisions=22` = S031…S052 (`reg` sha `2d95a270…`, `staged` `550a0129…`, `coll` `11623fc5…`). Committed `assimilation/reg-ids` (255 B, 51 ids, `a262e5f4…`) and `collisions` (105 B, 21 ids, `e7718d61…`) are strict prefixes (`cmp: EOF … after byte 255 / 105`); `staged-ids` is byte-equal (`550a0129…`). So 21 → 22 is the S052 (CISA KEV) landing, not drift. Lane `S052` = CISA KEV feed; staged `S052` = 信息安全漏洞周报（2026 年第 40 期，总第 853 期） (CNNVD) — different documents, same number. Executor's `renumber-map-pre-c2.txt` (S031→S052 … S124→S145) vs `-post-c2.txt` (S031→S053 … S124→S146): uniform +1 offset, HOLD(quarantine) on the same 7 staged ids (S037, S048, S054, S065, S068, S069, S070) in both; consistent with a 51→52 registry.
4. **Executor's collision claims verified:** lane `S037` (Cybozu FAQ) is cited by `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` and lane `S048` (Microsoft MSVR) by `corpus/knowledge/vendor-third-party-finding-coordination.md`; neither register source URL is registered in the lane; the staged `S068` document equals lane `S040`. Adoption by number is unsafe for S037/S048; by document, S068 is already held.
5. **Assimilation (non-claim item):** `grep -rliE 'KEV|Known Exploited|CISA' /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge` → 0 files; `grep -c -iE 'KEV|Known Exploited|cisa\.gov' SOURCES.append.md` → 0. F18/S052 cannot unblock any refused entry and is not an assimilation candidate (same shape as r34's F17 result). No flip set of a quarantined row is fully met.
6. **ScribeGateAssimilation divergence:** its `S068 403, 465 B` reproduces only with a browser-style UA (§2); its `S069/S070 200, 0 B` reproduces only from the register's truncated URL. Neither changes a verdict.
7. **Not done:** no `source-recheck`, harness, `quote-lint`, `renumber-staged.py`, or any shokuknow campaign tool; I did not read `ExecQuarantineSlice.md` before taking my own fetches/counts; no fetched bytes retained.

### 7. Gate draft block (installable by the lesson scribe)

```
### Quarantine slice — 7 register rows, re-derived by two seats (round 35)
Slice re-derived with the register awk (exit 0, 7 lines, 7/7 carry an S-id); `cmp` vs `assimilation/quarantine-slice` (d02acb68…) equal; the register
(5afe1810…) and package (4fe049cb…) are unmoved since round 34. Live fetches 2026-10-26 06:32–06:55Z by two seats return byte-identical bodies
(S037 9cba2e96…, S048 404 95cd25d8…, S054 0150c9d1…, S065 e33b0f67…, S068 098f99a8…, S069 b0c04697…, S070 2eff0a5b…).
Verdicts: S037/S054 span absent as contiguous text (facts hold; refuse as quoted); S048 unreachable (404, host up); S068 located, already lane S040;
S065 located at anchor level (catalogue date "2026年9月" absent, entry 1 page-number-spliced, 12/12 amendments present); S069/S070 reachable only
by a TLS exception (verifying curl exit 60; -k or plain http 200, 58 pp / 8 pp). Adopted: 0. Label note: ExecQuarantineSlice files S037/S054 as
prose-class-unverifiable and S069/S070 as present-and-located; ScoutQuarantine files them absent and unreachable-under-verified-TLS (same facts).
Id collisions: lane registry 52 ids (S052 = CISA KEV) vs staged 94 (S052 = CNNVD weekly) -> 22 (S031–S052); the 51-row artefacts are strict prefixes.
```

### 8. Evidence digests

```
2d95a2702fa2af54d4ab551b0e63129f606850cc139991a73db5b7b1ec6f3d00  reg (52 ids, live extract)
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  staged (94 ids)
11623fc54a36902bde1872ad904fdefa01db99ba5ff37f7a4d8d2769598e7c36  coll (22 ids)
510e3bba977a744382438fdb7b79ecce90a75e1590f2491e9f373ab88d9b8829  corpus/SOURCES.md at probe time
9cba2e96e343e1d0c95d23fb50454fa1321cb2d01af6ae318653290a1d20f204  S037 fetch
95cd25d80d88cce1e08528c03d5eb488f56bf9991f820bc31569b001eb2e2436  S048 404 body
0150c9d15dee603f55573f4692f306ba8ff46f70454b032f813b95fbdbb12b88  S054 fetch
e33b0f67293441f19ee519b2ed1619121da84867aa8396a3a16facd572586d83  S065 fetch
098f99a89df3a8018ab6eff7529fd8482af70dde6406472b88d526c773ded807  S068 fetch
b0c046970f9ca2b7bbfae5ee8e847ec0c630049aec1863fe3d5a0a62718e91a9  S069 (-k)
2eff0a5b10e2625e7d3a5b45c50992f018dde967cf16c97b38557186cdfb3f95  S070 (-k and plain-http, identical)
```

### 9. Scratch

`/fast/scratch/hyaku/kasegi-r35/ScoutQuarantine/` removed after this receipt was written (final `ls` of the parent below in the yield).
