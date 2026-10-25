# ScoutAssimPackage — F14 assimilation package scout findings (round-30 wave1)

Seat: ScoutAssimPackage (leaf). Milestone round-30, wave-1 v2. Read-only reconnaissance of the
kasegi merge package plus lane evidence; no writes outside this report file.
Bytes measured (sha256):
- `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` = `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb` (100 lines, 94 staged rows S031–S124)
- staged entry `…/knowledge/corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` = `d7fdd31f88fbd490ca964f5f3630b7b5ac7f8192c99e062405fabe120adc65f4`
- lane `corpus/SOURCES.md` = `f55025c2275d3d08eb254b4a3c83e578e79e55ad30e806591b85a6f1d52735ff` (45 registry rows, last S045)
- lane `corpus/source-snapshots/round-28/S041.txt` = `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`
- lane `corpus/source-snapshots/round-28/manifest.json` = `e62ddad133ffc19ebc66822c0fcb3b48ed4993c101f05262302acc58714f291d`

## 1. Staged row cells — S049 (verbatim from SOURCES.append.md line 25)

```
| S049 | 脆弱性対策情報データベース JVN iPedia に関する活動報告レポート — https://www.ipa.go.jp/security/reports/vuln/jvn/ug65p90000019ev2-att/000095610.pdf | docs | A | JVN's own severity vocabulary: the CVSS-to-深刻度 band definitions | 注 1) CVSSv2 基本値の深刻度による色分け; 注 2) CVSSv3 基本値の深刻度による色分け | JVN has no native severity scale; it maps CVSS base scores onto Japanese labels and keeps the legacy CVSSv2 bands alongside. | mined | 2026-10-23 | 180d | corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md |
```

Cell-by-cell: id=`S049`; source=`脆弱性対策情報データベース JVN iPedia に関する活動報告レポート — https://www.ipa.go.jp/security/reports/vuln/jvn/ug65p90000019ev2-att/000095610.pdf`; kind=`docs`; tier=`A`; scope=`JVN's own severity vocabulary: the CVSS-to-深刻度 band definitions`; anchor=`注 1) CVSSv2 基本値の深刻度による色分け; 注 2) CVSSv3 基本値の深刻度による色分け`; teaches=`JVN has no native severity scale; it maps CVSS base scores onto Japanese labels and keeps the legacy CVSSv2 bands alongside.`; status=`mined`; opened=`2026-10-23`; recheck=`180d`; used-by=`corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md`.

## 2. Staged row cells — S050 (verbatim from SOURCES.append.md line 26)

```
| S050 | 脆弱性対策情報データベース JVN iPedia の登録状況 2026年第3四半期 — https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html | docs | A | IPA's own quarterly distribution of JVN severities and its CWE ranking of the database | 2-2 脆弱性に関する深刻度別割合, 図2-2 (CVSSv2) and 図2-3 (CVSSv3); 図1-3 脆弱性の種類別上位 | Japan's national database carries CVSS-derived severities and CWE ids at scale, so Japanese practice borrows both instruments rather than originating them. | mined | 2026-10-23 | 180d | corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md |
```

Cell-by-cell: id=`S050`; source=`脆弱性対策情報データベース JVN iPedia の登録状況 2026年第3四半期 — https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html`; kind=`docs`; tier=`A`; scope=`IPA's own quarterly distribution of JVN severities and its CWE ranking of the database`; anchor=`2-2 脆弱性に関する深刻度別割合, 図2-2 (CVSSv2) and 図2-3 (CVSSv3); 図1-3 脆弱性の種類別上位`; teaches=`Japan's national database carries CVSS-derived severities and CWE ids at scale, so Japanese practice borrows both instruments rather than originating them.`; status=`mined`; opened=`2026-10-23`; recheck=`180d`; used-by=`corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md`.

## 3. Staged entry — header/source lines

File: `japanese-severity-vocabulary-and-impact-model.md` (3,666 B, sha256 `d7fdd31f…`).

```
# Japanese severity vocabulary and the handling-priority model

source: S049 — https://www.ipa.go.jp/security/reports/vuln/jvn/ug65p90000019ev2-att/000095610.pdf — 注 1), 注 2)
source: S050 — https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html — 2-2, 図2-2, 図2-3
source: S043 — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf — 付録4 脆弱性の影響度に関する考え方について, p.40 (wave-1 row, re-opened 2026-10-23)
verified-at: 2026-10-23
recheck: 180d — `curl -sSL https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html` then confirm the 深刻度別割合 percentages still match (expect 緊急 13.6%, 重要 44.2%, 警告 39.6%, 注意 2.5%) (ran 2026-10-23)
ground: F10 (extends F01, which holds CVSS-B semantics only) and F13 (extends F02)
```

Body claims (3 blocks): vocabulary S049 (CVSSv3 bands 0.1–3.9 注意 / 4.0–6.9 警告 / 7.0–8.9 重要 / 9.0–10.0 緊急; legacy v2 bands レベルI/II/III), scale S050 (2026Q3 distribution: v3 緊急13.6/重要44.2/警告39.6/注意2.5; v2 レベル3 44.1/レベル2 44.3/レベル1 11.6; CWE top-ten CWE-20/79/200/863/787/269), handling S043 (付録4: 影响度 = CVSSv3 base + 影響範囲 (利用者数/社会的影響力/攻撃の容易性, default 広), 3×3 matrix 簡易な対応/通常の対応/優先対応; passive-only web-app 4.0–6.9 mid-scope termination rule).

## 4. Registry absence — the two URLs are NOT in the lane registry

- `grep` for `ug65p90000019ev2-att/000095610.pdf|ipedia2026q3.html` across the whole lane `corpus/` tree (registry, knowledge, snapshots): **No matches found**.
- Lane registry rows end at S045; S049/S050 URLs appear in the lane repo only inside `.ufo/waves/` planning/census docs (round-28/29 connector census "Genuinely absent from lane registry" rows and the round-30 wave spec), which are not registry content. Confirmed absent.

## 5. Schema hazards the lane append must normalize

1. **Cell containing `|` — S120 teaches cell** (line 96): literal pipe inside backticks `…/view/content-sd.html?id=…&lib=ck\|zdx` → row has 13 pipe delimiters (12 split cells) and does not parse as an 11-column row. Must be escaped/re-written (e.g. replace with `/` or `\` outside backticks) before append, or the census row-count/parse breaks. This is the only malformed row.
2. **Prose recheck cells — 44 of 94 rows**: recheck cell carries `180d/90d/30d — <procedure> (ran YYYY-MM-DD)` instead of a bare duration. Affected: S081–S119 and S121–S124 (43 parsed + S120). Lane registry convention is bare duration (`90d`, `180d`, `on-release`; see S031–S045). If the lane schema requires bare durations, the prose must be stripped to the interval token (or moved to the lesson/Gate evidence) for every S081+ row. S049/S050 are already clean (`180d`).
3. **Opened dates — all ISO, but two cohorts**: all 94 rows comply with `YYYY-MM-DD` (no non-ISO dates). S031–S080 opened `2026-10-23`; S081–S124 opened `2026-10-24`. For the round-30 adoption, the lane rows will be re-stamped opened `2026-10-25` (per wave build-spec ExecRegistryAppend step 1) — a deliberate re-stamp vs the staged dates, not a defect.
4. **Staged-id references in the entry**: entry source lines cite staged ids `S049/S050/S043`. Claims.json C2 assimilation map is `S049→S046`, `S050→S047` and S043 maps to lane `S041`; rule "adopted ids continue the lane registry from S046; every adopted entry cites rows by document (URL/anchor is evidence), never by arithmetic". The appended entry must restate source lines with adopted ids (S046/S047/S041) while keeping URLs/anchors unchanged.
5. **Staged entry recheck prose** (item in §3) is a prose recheck inside a knowledge file; matches the lane's own entry style ([INFERENCE] lane entries use similar `Nd — …` prose), so no normalization required beyond the registry rows — flagging for the L1 to confirm.

## 6. Lane S041 and its contribution to F14

- Lane row `S041` exists: `情報セキュリティ早期警戒パートナーシップガイドライン 2026年10月 (JPCERT/CC) — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf | spec | A | … | 付録6 §2 p.45, §4 p.46-47, 参考1 p.53-54 | …` (registry line 47).
- Round-28 capture exists: `corpus/source-snapshots/round-28/S041.txt` (147,267 B, sha256 `e18acbf9…`), manifest at `round-28/manifest.json`. The capture already contains the **付録4 脆弱性の影響度に関する考え方について** text the staged entry's S043 line cites: ToC line 41 (p.40), matrix content at lines ~1455–1500 (深刻度 = CVSSv3 基本値スコア; 影響範囲 elements ①利用者数 ②社会的影響力 ③攻撃の容易性, 不明→「広」; 3×3 簡易な対応/通常の対応/優先対応), 起算日 footnote 4 definition (line 340), and the priority-handling statement (line 65).
- Contribution: S041 supplies the already-registered JPCERT/CC 2026 guideline row whose capture carries the F14 handling-priority source (the staged S043 row maps to this same document). Round-30 can reuse the round-28 capture (wave build-spec step 3 copies `round-28/S041.txt` → `round-30/S041.txt`), so the round-30 manifest's S041 record can pin quotes from the same 付録4 text; no new capture needed for S041. Note the staged S043 row's anchors (Ⅳ/図1/付録3 p.36/起算日 footnote 4) overlap the lane S041 row's anchors (付録6) only partially — the F14 entry cites 付録4 p.40, which is present in the capture but not in the registered S041 anchor cell.

## 7. Findings summary for L1

- S049/S050 staged cells are schema-clean and verbatim-quoted above; URLs confirmed absent from lane corpus; both used-by the single F14 entry; adopted ids per claims.json C2 are S046/S047.
- The only hard append blocker is S120's embedded `|` (row mis-parses). Prose recheck cells affect 44 rows and must be normalized if the lane schema demands bare durations. Opened dates are ISO; cohorts differ by staging round only.
- S041 (round-28 capture) already carries the F14 付録4 handling-priority text; reuse for the round-30 manifest.
