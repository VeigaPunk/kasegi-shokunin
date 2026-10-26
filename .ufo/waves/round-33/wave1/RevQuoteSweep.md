# RevQuoteSweep — round-33 wave-1 quote sweep (S049/S050 manifest + F16 entry)

Seat: RevQuoteSweep (reviewer, leaf). Date: 2026-10-26. Scope: every source-bound quote in
`corpus/source-snapshots/round-32/manifest.json` and in the F16 entry
`corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`, byte-verified against the
captures, cross-checked with `corpus/instruments/source-recheck.py`. No installs this round
(Python 3.14.8 system tooling sufficient). No writes outside this receipt.

## Inputs and churn (bound 6)

sha256 at sweep start (after poll for inputs, ~440 s wait for manifest/entry/registry rows):

```
6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774  corpus/source-snapshots/round-32/manifest.json
962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8  corpus/source-snapshots/round-32/S049.txt
2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888  corpus/source-snapshots/round-32/S050.txt
eebd5ea572b3359f012e9c7ef9975969ffcbd3e5b06e31d40ac56a6a7d15910b  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md   (PRE-STATE)
24738a86753edc13d66e40790305f785cdecced1dae4143159708627c382099b  corpus/SOURCES.md   (PRE-STATE)
```

The entry and SOURCES.md were edited by their owners mid-sweep (PRE-STATE hashes above). All
cited results below are the RE-RUN on quiescent bytes:

```
53c48b3b322aa4e5f90e1bae27ad0c1fb60c3452b2cff1e35a52e3276bb60a48  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b  corpus/SOURCES.md
```

hash-stable across two consecutive checks; manifest and both captures never changed
(6e4e719a… / 962a451a… / 2f9c6406… throughout). PRE-STATE numbers are not compared to any
after column; the PRE-STATE sweep found the same single defect, re-confirmed below.

## 1. Instrument runs (rerun on quiescent bytes)

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049
S049:sha256 OK
S049:Q1 OK occurrences=1
S049:Q2 OK occurrences=1
S049:Q3 OK occurrences=1
S049:Q4 OK occurrences=1
S049:Q5 OK occurrences=1
S049:Q6 OK occurrences=1
S049:Q7 OK occurrences=1
S049:Q8 OK occurrences=1
exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050
S050:sha256 OK
S050:Q1 OK occurrences=1
S050:Q2 OK occurrences=1
S050:Q3 OK occurrences=1
S050:Q4 OK occurrences=1
S050:Q5 OK occurrences=1
S050:Q6 OK occurrences=1
exit=0
```

14/14 assertions `occurrences=1`, both sha256 pins OK, exit 0. No anchor needed (all unique).
Manifest `sha256` fields equal the actual capture digests (independently re-derived with
sha256sum: 962a451a… and 2f9c6406…, matching the entry's Scope section and the pins in
`manifest.json` itself).

## 2. Byte-identity layer the instrument does not prove

source-recheck.py counts occurrences under whitespace/markup normalization; the sweep adds
raw-byte substring counts (no paraphrase) and cited-line checks (Q3 exact location).

(a) All 14 manifest quotes: `byte_lines=1` in their capture AND byte-present on the manifest's
cited line (S049 Q1→L211, Q2→L214, Q3→L410, Q4→L208, Q5→L419, Q6→L408, Q7→L132, Q8→L212;
S050 Q1→L70, Q2→L591, Q3→L595, Q4→L597, Q5→L112, Q6→L418). 0 failures. Note: the manifest
purpose line says assertions were measured under normalization; in fact all 14 are byte-exact
on one line, so no assertion depends on the normalization fallback.

(b) All 15 entry blockquotes: byte-identical to the capture line at the cited line number. 13
are byte-identical to their manifest quotes; the 2 non-manifest blockquotes (S050.txt:113
three-tier sentence; S050.txt:129 peg label) are the entry's declared hand-measured quotes —
both byte-verified in the capture (113 exact; 129 exact plus repeats exactly at L159, 189, 219,
249, 274, 304 as the entry states).

(c) All 14 manifest quotes appear byte-exactly somewhere in the entry text (no paraphrase
between entry and manifest).

(d) Entry `source:` URLs byte-equal the manifest `url` fields (S049
`https://zc.cnvd.org.cn/news/helpList`, S050 `https://security.360.cn/Reward/rules`), and each
byte-equals the URL cell of the single registry row `| S049 |` / `| S050 |` in SOURCES.md
(rows at L55/L56 of the post-append file).

## 3. Hand-measured entry quotes and line citations (grep -nF against captures)

All byte-exact at the cited line, count as stated: S049 L72 (27-char intro opening), L200, L214
(`http://www.cnvd.org.cn/` redirect), L356, L359, L408 (trusted-system purpose fragment), L414;
FAQ question stems at L207, L213, L409, L418; footer names at L425/L426. S050: L62 + L68
(effective 2023-03-01 施行 clause), L70/L71 (invested-companies wrap fragments — the entry
correctly declines to bind the wrapped sentence as one assertion), L71 (product-page deferral,
count 1), L99 (both initial-rating fragments), L558, L591 (`1360.com` example), L595, L597,
L601 (legal-action reserve, count 1), L611. Range citations L425-426, L559-560, L601-604 hold
their content across the documented PDF line wraps (未纳入安全服务的控股 wraps 控股/业务 across
L559/L560; 网络安全法 at L602 inside the cited range). 评分实例 block L134-L142 and nav/contact
ranges (L1-22, L420-426) check out.

## 4. The entry's own falsifiable counts, rerun verbatim

```
FC-1: 众测平台仅接收… count 1 ; 不接受互联网漏洞 count 1            (entry: 1, 1)
FC-2: 授权 count 2 (both 客户的授权范围 L214/L410) ; 并不是…约定 1 ; 注… 1   (entry: 2, 1, 1)
FC-3: 本标准适用于… count 1 ; 具体范围可参考… count 1               (entry: 1, 1)
FC-4: 未纳入安全服务的资产… count 1 ; 不予收录 count 6               (entry: 1, 6)
FC-5: 安全币 S049 0 / S050 32 ; 奖金 S049 12                        (entry: 0/32, 12)
FC-6: 免责|安全港 S049 0 / S050 0 ; 授权测试 S050 0 ; 601句 1        (entry: 0, 0, 0, 1)
附加分 S049 count 1 at L72 only (entry: 1, L72 only)
self-pipeline awk Attribution..What-this-adds | grep -c -E 'CVSS|0.85|时效评价|利用代码' → 1 (entry: 1)
sizes: S049.txt 20272 B / 426 ln ; S050.txt 31016 B / 630 ln (entry Scope section: same)
```

All 16 stated counts reproduce. Cross-entry F13 quote “Issues affecting assets under HackerOne's
control are in scope.” byte-present at `corpus/source-snapshots/round-29/S043.txt:31` as cited.

## 5. FINDING (minor) — transposed question stem, 2 places, owner ExecEntryF16

Capture `corpus/source-snapshots/round-32/S049.txt:210` reads:

```
提交漏洞时，若目标列表中没有当前目标，是否可以自行添加？
```

The entry quotes the stem with the first two words transposed — 漏洞提交时 instead of
提交漏洞时 — at:

- entry L3 (`source: S049 …` line, first quoted question, cited L210-212)
- entry L48 (Claim 1 blockquote attribution: `> — S049.txt:211 (使用手册 › “漏洞提交时…”)`)

`grep -c '提交漏洞时'` on the entry = 0: the capture spelling appears nowhere. The location
citations (L210-212) are correct and the blockquoted answer itself (L211) is byte-perfect, so no
claim changes; but QUALITY Q3 requires verbatim quotes, and a citation-heading quote that
differs from the capture is exactly the paraphrase class this sweep exists to catch. Fix: swap
the two 2-character words in both spots of the entry (owner ExecEntryF16); no manifest or
registry change needed (the manifest does not quote the question stem).

## 6. Addendum — finding resolved (same session)

ExecEntryF16 fixed both spots; re-verified on the new bytes:

```
1f7ac0a2c39a0fbfdbee2ecbe112316dfc1bf7095b18cb8fb4eb9d6dfce171d1  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md  (306 ln, 24539 B)
漏洞提交时=0  提交漏洞时=2   (L3 source: line; L48 attribution, now citing S049.txt:210-211 with the question at L210)
source-recheck --source S049 -> Q1..Q8 OK occurrences=1, exit 0 ; --source S050 -> Q1..Q6 OK, exit 0
```

Finding closed. Owner's added L210/L211 disambiguation checked: the Q1 answer quote stays
byte-identical at L211; the question stem now byte-matches capture L210.

## 7. Residual risk / verification gaps

- The captures are extracted text; the raw HTML (S049) and PDF bodies (S050) were not compared
  (the entry says the same of ScoutLiveDrift's re-fetch). Byte-identity here is capture↔manifest↔entry.
- The two S050 wrap-spanning prose citations (L559-560) were verified by line reads, not by a
  single-line grep — no entry quote depends on them.
- SOURCES.md row anchor cells (L55/L56) were spot-checked for URL only; full anchor-cell
  cross-check against the manifest locations is ExecRegistryAppend/C1 territory, not re-derived here.
