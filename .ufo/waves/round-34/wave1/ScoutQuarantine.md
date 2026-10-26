# ScoutQuarantine — round-34 quarantine slice re-derivation, reachability probe, id-collision recheck

Seat: ScoutQuarantine (leaf, no subagents). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `014ee2d7`, claims-freeze `29f606db`). `/home/vgpnk/Projects/shokuknow` read-only throughout
(register and package read; no campaign tool run, nothing written there). Only this receipt was written in
the lane. Scratch `/fast/scratch/hyaku/kasegi-r34/ScoutQuarantine/` (deleted before yield). Run time of the
probes: `2026-10-26T05:39Z`. UA for every fetch: `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`
(= `corpus/instruments/capture-source.py:32`). Tools: `curl 8.23.0`, `pdftotext 26.08.0`, `python3`; one
ephemeral `uv run --no-project --with pymupdf` (PyMuPDF 2.0, uv channel, nothing persisted into the tool
list) because `pdftotext` returned 0 chars for S065. No tool installed permanently; no pacman.

Result in one line: **slice = 7 rows, all carry an S-id; 2 refuse (S037, S054), 1 unreachable (S048, HTTP 404),
2 unreachable-by-TLS (S069, S070), 2 now fetchable (S065 verifiable-at-anchor with one defect; S068 verifiable but
already held as lane S040). 0 adopted. Id collisions at the live registry: 21 (S031–S051); 0 adopted rows this round.**

## Report

### 1. Slice re-derivation (command as given)

```console
$ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
$ awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' $R > slice.txt ; echo awk_exit=$?
awk_exit=0 lines=7
 S037   `payload-absent`
 S054   `payload-absent`
 S048`   the cited source could not be fetched, so no quote was checked
 S065`   the cited source could not be fetched, so no quote was checked
 S068`   the cited source could not be fetched, so no quote was checked
 S069`   the cited source could not be fetched, so no quote was checked
 S070`   the cited source could not be fetched, so no quote was checked
all-lines-have-S-id: 7/7   (grep -cE 'S[0-9]{3}' slice.txt / wc -l)
$ diff slice.txt .ufo/waves/round-34/assimilation/quarantine-slice ; echo diff_vs_committed_r34_slice=$?
diff_vs_committed_r34_slice=0
$ diff slice.txt .ufo/waves/round-33/assimilation/quarantine-slice ; echo diff_vs_r33_slice=$?
diff_vs_r33_slice=0
$ sha256sum slice.txt
d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862  slice.txt
```

Register unchanged since round 33: `sha256 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`
(83621 B, mtime Oct 24 08:37); package `merge/kasegi/SOURCES.append.md`
`4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb` (89718 B, Oct 24 23:33). The slice is the
same 7 rows as round 33 (register lines 99, 100, 322–326; `awk` prints the `S048`…`S070` cells with a trailing
backtick because the second table's row id is written `S048\``, which still matches `S[0-9]+`).

Register row URLs (first table `$6`, second table `$6`, `NR` = register line):

| line | round | id | class | register URL |
|---|---|---|---|---|
| 99 | round1 | S037 | `payload-absent` | `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A` |
| 100 | round3 | S054 | `payload-absent` | `https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf` |
| 322 | round2 | S048 | no-quote/unreachable | `https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3` |
| 323 | round4 | S065 | no-quote/unreachable | `http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf` |
| 324 | round4 | S068 | no-quote/unreachable | `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` |
| 325 | round4 | S069 | no-quote/unreachable | `https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F` (**truncated**) |
| 326 | round4 | S070 | no-quote/unreachable | same truncated URL as S069 |

Finding: the register's S069/S070 URLs are the same 105-char directory prefix; the staged package rows carry the
two full 306-char URLs (`…20_WD_2025005470_…指南.pdf` for S069, `…20_DI_2025005470_…指南.pdf` for S070;
`url_len=306` each). The probes below use the staged full URLs; the truncated register URL returns
`http=200 bytes=0` (empty, nothing to verify).

Staged-id space caveat: every id in the slice is a **staged** id (the package assumes a 30-row registry). Lane
registry ids with the same number are different documents: lane `S037` = cybozu bug-bounty FAQ, lane `S048` =
microsoft.com/msrc/msvr; lane has no S054/S065/S068/S069/S070 rows (51 rows, last `S051`). Only one slice URL
is already held by the lane, by document: staged `S068` (Cisco policy) == lane **`S040`** (URL byte-equal, §5).

### 2. Reachability probe (read-only, instrument UA, `curl -sS -L --max-time 60`)

```console
S037 http=200 bytes=24189 type=text/html;charset=utf-8 final=<same URL>            sha256 9cba2e96e343e1d0c95d23fb50454fa1321cb2d01af6ae318653290a1d20f204
S048 http=404 bytes=748   type=text/html;charset=utf-8 final=<same URL>            sha256 95cd25d80d88cce1e08528c03d5eb488f56bf9991f820bc31569b001eb2e2436
     retry: S048 http=404 bytes=748   ;  control: https://std.samr.gov.cn/ http=200 bytes=109107
S054 http=200 bytes=513648 type=application/pdf  final=<same URL>                   sha256 0150c9d15dee603f55573f4692f306ba8ff46f70454b032f813b95fbdbb12b88
S065 http=200 bytes=7465472 type=application/pdf final=<same URL>                   sha256 e33b0f67293441f19ee519b2ed1619121da84867aa8396a3a16facd572586d83
S068 http=301/302 -> final=https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html
     http=200 bytes=94027 type=text/html;charset=ISO-8859-1                          sha256 098f99a89df3a8018ab6eff7529fd8482af70dde6406472b88d526c773ded807
S069 http=302 bytes=0 final=https://kass.sacinfo.org.cn/kfs/token/download/wxmybtjwriokqjbs  curl: (60) SSL certificate OpenSSL verify result: unable to get local issuer certificate (20)  ec=60
S070 http=302 bytes=0 final=https://kass.sacinfo.org.cn/kfs/token/download/drvbaawzcnkfgiwj  curl: (60) ... (20)  ec=60
```

Diagnostic only (TLS verification **off**, `curl -k`; not an instrument-grade capture, recorded so the verdict says
why and what is behind the wall): S069 `http=200 bytes=1470121 application/octet-stream`, PDF 1.7, **58 pages**,
sha256 `b0c046970f9ca2b7bbfae5ee8e847ec0c630049aec1863fe3d5a0a62718e91a9`; S070 `http=200 bytes=234182`,
PDF 1.7, **8 pages**, sha256 `2eff0a5b10e2625e7d3a5b45c50992f018dde967cf16c97b38557186cdfb3f95`. The redirect
target is a one-time token URL (three different tokens for the same source across hops/runs: `wxmybtjwriokqjbs`,
`evmvalfuvissdihe`, `gxjyskqlafaaqocr`/`drvbaawzcnkfgiwj`), so a manifest could not bind the final URL and the
bytes are hash-unstable by construction.

Reachability class: S037 found, S054 found, S065 found (changed vs register), S068 found (redirect), S048 **absent**
(HTTP 404; site root is up, so the deep link is dead, not the host), S069/S070 **unreachable** under verified TLS
(incomplete issuer chain; reachable only with `-k`).

### 3. Content checks per row (counts at F1 verbatim / F2 whitespace-collapsed / F3 whitespace-removed)

S037 (HTML tag-stripped) — staged quote string `信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01`:

```
whole string                               F1=0 F2=0 F3=0
信息安全技术 网络安全漏洞分类分级指南       F1=1 F2=1 F3=1
标准状态：现行                              F1=0 F2=0 F3=1   (page renders a space after the colon)
发布日期2020-11-19                          F1=0 F2=0 F3=1   (page has no colon; staged string inserts ：)
实施日期2021-06-01                          F1=0 F2=0 F3=1
GB/T 30279-2020                            F1=2 F2=2 F3=2
```

Reproduces the round-33 finding on a fresh fetch (24,189 B, sha256 identical to round 33): the quote is a splice of
separate record blocks with two inserted colons. The facts (title, 现行, 2020-11-19, 2021-06-01) hold on the page.

S054 (pdftotext -layout, 4094 chars) — staged string `脆弱性の悪用が確認されたもの又は疑われるもの`:

```
whole string                    F1=0 F2=0 F3=0
脆弱性の悪用が確認されたもの    F1=0 F2=0 F3=0
又は疑われるもの                F1=1 F2=1 F3=1
```

PDF lines 44–47: `（ア） 脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認` / `されたもの又は疑われるもの` — the
statutory definition parenthetical sits inside the staged quote; the quote elides it. Same result as round 33
(sha256 `0150c9d1…` identical).

S065 — `pdftotext` returns **0 chars** (`Syntax Warning: Mismatch between font type and embedded font file`; fonts
`FZXBSJW--GB1-0` CID TrueType + `SourceHanSansCN-Regular` embedded, 30 pages, no images). PyMuPDF 2.0 extracts 13,975
chars. Staged row anchors (the row carries anchors, not a verbatim quote):

```
现行有效法律目录                                            F3=1   title "现行有效法律目录（303 件）"
303                                                         F3=1
刑法（7 件） section                                         present (offset 11541 in the F3 text)
中华人民共和国刑法（1979年通过，1997年修订，2009年修正）       F3=0   -- page number "28" is spliced in: "…1997年修订，28 2009年修正）附件一：…"
中华人民共和国刑法修正案（十二）（2023年）                     F3=1
附件一 / 附件二                                              F3=5 / 5
2026年9月                                                    F3=0   -- document says "截至2026 年8 月28 日十四届全国人大常委会第二十四次会议闭幕"
刑法修正案（X）（YYYY年） distinct X values found             11 of 12 (一 not matched by the pattern; not investigated)
```

So the row's "catalogue dated 2026年9月" is wrong against the text (URL path `202609` is the publish month, the catalogue
is current to 2026-08-28), and a verbatim quote of the 刑法 entry would be broken by a page-number splice.

S068 (HTML) — `Cisco Product Security Incident Response` F1=4; `Disclosure of Security Vulnerabilities` F1=2; `ISO/IEC 29147` F1=1
(`The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018`); `CERT/CC` F1=2; `ISO/IEC 30111` 0 (the row does
not claim it). The two acceleration conditions are present verbatim under the second `Disclosure of Security
Vulnerabilities` heading: `The Cisco PSIRT has completed the incident response process for a high-severity
vulnerability and public disclosure of code fixes is planned to address it.` and `The Cisco PSIRT has observed active
exploitation of a vulnerability that could lead to increased risk for Cisco customers.` Row anchors match.

S069 (`-k` diagnostic bytes, `pdftotext -layout`, 87,900 chars): `GB/T 30279` 76, `202X` 56, `6.3.1` 1, `6.3.2` 1, `表A.1` 5,
`表D.1` 2, `表E.1` 2, `可利用性评分表` 3, `环境因素评分表` 3, `漏洞技术分级表` 3, `漏洞综合分级表` 3. S070 (`-k`, 7,763 chars):
`20260806-T-469` 1, `中国信息安全测评中心` 5, `任务来源` 1, `制定背景` 1, `起草单位` 1, `工作简况` 1, `CWE` 6, `CVSS` 5. The anchors
exist on the unverified-TLS bytes; the "reduce dependence on foreign standards" motive sentence and the 1-to-9 score
claim in the S069/S070 rows were not checked.

S048: body is a Tomcat 404 (`HTTP状态 404 - 未找到`, message `文.件[/WEB-INF…`), nothing to anchor against.

### 4. Verdict per row (Gate draft)

| id | register class | live probe | verdict | reason / flip condition |
|---|---|---|---|---|
| S037 | `payload-absent` | 200, 24,189 B html | **refuse** (unchanged) | Staged quote is a three-block splice with two inserted `：`; facts hold. Flip: re-quote one contiguous record field string (e.g. `发布日期 2020-11-19`) with F2 count 1 on the live page, then register as a new lane row by document (lane `S037` is cybozu). |
| S054 | `payload-absent` | 200, 513,648 B pdf, 3 pp | **refuse** (unchanged) | Quote drops the statutory parenthetical inside （ア）. Flip: quote `（ア）` with the parenthetical, or quote the contiguous tail `されたもの又は疑われるもの` with a page/line and a F2 count of 1. |
| S048 | unreachable | **404** twice, root 200 | **unreachable** | Deep link dead, site up; no payload to verify. Flip: a working record URL or a captured copy; the row's anchor (`20260806-T-469` project cycle, 公示 dates) is also reachable via S069/S070 once TLS is resolved. |
| S065 | unreachable | **200**, 7,465,472 B pdf, 30 pp, `pdftotext` 0 chars | **verifiable (anchor-level, conditional)** | No longer unreachable: PyMuPDF text confirms the title, 303, the 刑法 section, 附件一/二 and the twelfth amendment. Defects to fix before any adoption: (a) `catalogue dated 2026年9月` is not in the text (`截至2026年8月28日`); (b) the 刑法 entry is broken by a page number, so quote only sub-spans; (c) `pdftotext` yields nothing, so any recheck must name an extractor (`uv run --with pymupdf`) or it will report absent; (d) `http:` plain URL. Not adopted. |
| S068 | unreachable | 200 after 302 to `sec.cloudapps.cisco.com`, 94,027 B | **verifiable, duplicate of lane S040** | Anchors verified. The cited URL is already registered as lane `S040` (byte-equal); nothing to adopt. The redirect target host differs from the cited host (record in S040's recheck if not already). |
| S069 | unreachable | 302 to tokenised `kass.sacinfo.org.cn`, **TLS verify fail (ec=60)**; `-k` 200, 58 pp | **unreachable** | Instrument-grade capture impossible (incomplete issuer chain, per-request token URL); anchors present on `-k` bytes only. Flip: trusted chain or a stable, token-free URL. |
| S070 | unreachable | same, `-k` 200, 8 pp | **unreachable** | Same as S069. |

Net disposition: **0 adopted, 2 refused (S037, S054), 3 unreachable (S048, S069, S070), 2 verifiable-but-not-adoptable-now
(S065 conditional; S068 duplicate of lane S040)**. Compared with round 33 (0 adopted, 2 refused, 5 unreachable) the
change is S065 and S068 turning fetchable; S048/S069/S070 unchanged in class.

### 5. Id-collision re-run (0–3-space pattern)

```console
$ extract() { grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$1" | grep -oE 'S[0-9]{3,}' | sort -u; }
$ extract corpus/SOURCES.md > reg ; extract /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md > staged ; comm -12 reg staged > coll
live_registry_ids=51 first=S001 last=S051
staged_ids=94 first=S031 last=S124
collisions=21 first=S031 last=S051
```

Registry list (51): `S001 S002 … S050 S051` (contiguous, `paste -sd' '` printed S001 through S051 with no gap).
Staged list (94): `S031 S032 … S124` (contiguous).
Collision list (21): `S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051`.

Versus the frozen round-34 assimilation artefacts (`.ufo/waves/round-34/assimilation/`): `staged-ids` is byte-equal
(470 B). `reg-ids` (250 B, S001–S050) and `collisions` (100 B, S031–S050 = 20) are strict prefixes of the live
extracts (`cmp: EOF on … after byte 250` / `after byte 100`); the single additional line in both is **S051**, the
Immunefi row landed this round by C2 (live `sha256 corpus/SOURCES.md` `4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6`,
`jj st`: `M corpus/SOURCES.md`, `?  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`). So 20 -> 21 is the
registry growth, not drift. Guard sensitivity: col-0-only count on the live registry = 51 rows (all rows column 0, no
indented row now), so the 0–3-space pattern and the col-0 pattern agree on the live file; the sensitivity proof stays the
committed `assimilation/guard-proof.txt` (scratch registry with an indented `S031`: 0–3-space catches 1, col-0-only 0).

Staged `S051` = `中华人民共和国刑法（最高人民法院公报刊载文本）` (`gongbao.court.gov.cn/Details/96fea4e0…`), lane `S051` =
Immunefi VSCS v2.2 (`immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/`): different documents,
same number — a real collision, resolved by document, not number.

**No adopted row this round (confirmed):**
- The 19 staged URLs also present in the lane registry map to different lane ids (e.g. staged `S035`→lane `S050`, `S034`→`S049`,
  `S068`→`S040`, `S031`→`S043`, `S032`→`S044`, `S033`→`S045`, `S039`→`S033`, `S040`→`S034`, `S041`→`S035`, `S042`→`S042` (same
  number, same doc), `S043/S064/S076`→`S041`, `S049`→`S046`, `S050`→`S047`, `S055`→`S036`, `S056`→`S037`, `S057`→`S038`,
  `S060`→`S039`, `S080`→`S048`, `S123`→`S032`); all were held before round 34. The lane URL set is 56, staged 98, shared 19.
  The lane's only new row this round (S051 Immunefi) is not in the staged set.
- Knowledge entries: staged 67 `.md` under `merge/kasegi/knowledge/corpus/knowledge/`; lane 46 (+ the untracked
  Immunefi entry). Name overlap 4, **byte-equal 0** — overwrite hazards remain: `program-severity-ladders-and-reward-scales.md`
  (staged `35de5f8b`/50 L vs lane `6c05c98f`/67 L), `japanese-domestic-disclosure-workflow.md` (`ee667c2f`/55 vs `a22d2321`/103),
  `japanese-severity-vocabulary-and-impact-model.md` (`d7fdd31f`/52 vs `f584f06c`/38), `authorised-testing-rules-of-engagement.md`
  (`bf40409e`/63 vs `5533fc87`/87). No staged file was copied.

### 6. Gate draft block (installable by the lesson scribe)

```
### Quarantine slice — 7 register rows, re-derived and probed (round 34)
Slice re-derived with the register awk (awk_exit=0, 7 lines, 7/7 carry an S-id, `diff` vs round-33 and round-34 committed slices empty).
Live probe 2026-10-26T05:39Z with the instrument UA: S037 200, S054 200, S065 200 (30-page PDF, pdftotext empty, PyMuPDF reads it),
S068 200 via 302, S048 404 (twice; host root 200), S069/S070 302 to a tokenised kass.sacinfo.org.cn download that fails TLS
verification (curl exit 60; 58-page / 8-page PDFs visible only with -k).
Verdicts: S037 refuse (spliced collage), S054 refuse (parenthetical elided), S048 unreachable, S069 unreachable, S070 unreachable,
S065 verifiable at anchor level but not adopted (wrong "2026年9月" date, page-number splice, needs a non-pdftotext extractor),
S068 verifiable and already registered as lane S040. Adopted: 0.
Id collisions: registry 51 ids vs staged 94 ids -> 21 (S031-S051); frozen round-34 artefacts are strict prefixes (S051 = C2 Immunefi).
```

### 7. Evidence digests

```
d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862  slice.txt
a262e5f46ca2407263cc9eb15b56686f61c5c011bb65d7d130fbd08af8ed0974  reg (live extract, 51 ids)
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  staged (94 ids)
e7718d617b04972a00d91124bf8c8b38219e08a7980db17104654cb83f299740  coll (21 ids)
9cba2e96e343e1d0c95d23fb50454fa1321cb2d01af6ae318653290a1d20f204  S037 fetch
95cd25d80d88cce1e08528c03d5eb488f56bf9991f820bc31569b001eb2e2436  S048 404 body
0150c9d15dee603f55573f4692f306ba8ff46f70454b032f813b95fbdbb12b88  S054 fetch
e33b0f67293441f19ee519b2ed1619121da84867aa8396a3a16facd572586d83  S065 fetch
098f99a89df3a8018ab6eff7529fd8482af70dde6406472b88d526c773ded807  S068 fetch
b0c046970f9ca2b7bbfae5ee8e847ec0c630049aec1863fe3d5a0a62718e91a9  S069 (-k diagnostic)
2eff0a5b10e2625e7d3a5b45c50992f018dde967cf16c97b38557186cdfb3f95  S070 (-k diagnostic)
```

### 8. Gaps and caveats

- S065 amendment count: 11 of 12 amendment decisions matched by my regex (`刑法修正案（一）` form not matched); the row's
  "twelve amendment decisions" claim is not fully re-derived.
- S069/S070 content checks used unverified-TLS bytes; they are evidence of existence, not capture-grade.
- No fetched bytes are committed (scratch deleted); hashes above are the only record. A later seat can re-fetch; S065
  hash can drift (government PDF), S069/S070 tokenised URLs differ per request.
- I did not run `source-recheck`, the harness, or `quote-lint`; none were in scope.

### 9. Scratch

`/fast/scratch/hyaku/kasegi-r34/ScoutQuarantine/` removed after this receipt was written (see the final `ls` below).
