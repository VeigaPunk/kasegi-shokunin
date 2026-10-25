# Japanese severity vocabulary and the handling-priority model

source: S046 — https://www.ipa.go.jp/security/reports/vuln/jvn/ug65p90000019ev2-att/000095610.pdf — 注 1)/注 2) CVSSv2/CVSSv3 基本値の深刻度による色分け legends, lines 555–570 of `corpus/source-snapshots/round-30/S046.txt`; Windows 11 severity proportions, lines 82–85
source: S047 — https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html — 2-2 脆弱性に関する深刻度別割合 (図2-2 CVSSv2, 図2-3 CVSSv3), lines 215–240 of `corpus/source-snapshots/round-30/S047.txt`; 2-1 CWE ranking, lines 200–214
source: S041 — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf — 付録4 脆弱性の影響度に関する考え方について, p.40, lines 1455–1501 of `corpus/source-snapshots/round-30/S041.txt`
verified-at: 2026-10-25
ground: F14
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source S046 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source S047 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source S041 # three chained single-source invocations (the flag is single-valued); S041 capture digest equals the round-28 pin e18acbf9…

## The claim

JVN's 深刻度 labels are CVSS base-score bands; the national database does not define a severity scale of its own, and the JPCERT/CC guideline then derives handling from that score combined with impact scope. Everything below is what IPA's or JPCERT/CC's own reports state.

**The vocabulary (S046).** IPA's JVN iPedia activity report prints two legends. On CVSS v2 it maps 0.0–3.9 → レベルI（注意）, 4.0–6.9 → レベルII（警告）, 7.0–10.0 → レベルIII（危険） (S046.txt:555-561): “深刻度=レベル III（危険）” is defined against “CVSS 基本値=7.0～10.0” (S046.txt:558,561). On CVSS v3 it maps 0.1–3.9 → 注意, 4.0–6.9 → 警告, 7.0–8.9 → 重要, 9.0–10.0 → 緊急 (S046.txt:562-570): “深刻度=緊急” sits against “CVSS 基本値=9.0～10.0” (S046.txt:566,570). The report applies the labels in prose the same way — the Apache case is “脆弱性の深刻度を示す CVSSv2 基本値は 4.3(*8)で二番目に深刻” (S046.txt:111-113, manifest Q2). IPA's JVN therefore has no native scale: each 深刻度 label is a Japanese name pasted onto a CVSS base-score band, and the v2 bands are kept alongside v3 because older records carry v2 scores.

**The published distribution (S047).** IPA's quarterly registration report for 2026 Q3 publishes the shares. On CVSSv3: “「緊急」が全体の13.6%、「重要」が44.2%、「警告」が39.6%、「注意」が2.5%となっています” (S047.txt:239). On CVSSv2: “レベル3が全体の44.1%、レベル2が44.3%、レベル1が11.6%となっており” with レベル2以上 at 88.4% (S047.txt:216). The same report ranks CWE categories — “CWE-284（不適切なアクセス制御）が1,580件” is the most frequent (S047.txt:202,205) — and reports a cumulative 310,240 records at S047.txt:131. The national database thus carries CVSS-derived severities and CWE classification at scale: both instruments are borrowed, and the Japanese labels are added by IPA.

**The handling model (S041).** The JPCERT/CC guideline's 付録4 frames impact-based handling: “脆弱性の深刻度（CVSSv3 基本値スコア）と影響範囲により決定します。” (S041.txt:1459), with “脆弱性の深刻度 ：脆弱性の深刻度として、CVSSv3 基本値スコアを適用する。” (S041.txt:1491). The scope factor is judged from ①利用者数, ②社会的影響力, ③攻撃の容易性, and “①～③がすべて不明” defaults to 広 (S041.txt:1492-1501). The result is the three-by-three response matrix at S041.txt:1465-1490 (簡易な対応 / 通常の対応 / 優先対応 by score band × scope). One closing rule for web applications: with a 4.0–6.9 base score, 中 scope, and a passive-only attack, handling may be terminated — “受動型の攻撃であれば、取扱いを終了することを可能とし” (S041.txt:1463, continuing “ます。” on line 1464).

## Why it matters

The Japanese reading of severity is a triage mapping, not a second scoring language: S046 shows the label set is exactly the CVSS band names, S047 shows those labels at scale in the quarterly statistics, and S041 shows the handling posture is a function of the base score plus an impact-scope judgment. The passive-attack termination rule (S041.txt:1462-1464) is the sharpest consequence: a score band alone never decides whether a case is closed.

## Falsifiable checks

1. Given S047.txt:239, check the four CVSSv3 shares: 緊急 13.6%, 重要 44.2%, 警告 39.6%, 注意 2.5%. If a future capture of the same quarterly report shows different numbers or order, the distribution statement here is falsified for that quarter.
2. Given S046.txt:555-570, verify every band–label pair: v2 0.0–3.9→レベルI（注意）, 4.0–6.9→レベルII（警告）, 7.0–10.0→レベルIII（危険）; v3 0.1–3.9→注意, 4.0–6.9→警告, 7.0–8.9→重要, 9.0–10.0→緊急. Any relabeling or added band falsifies the vocabulary claim.
3. Given S041.txt:1465-1490, check the matrix: a score ≥ 7.0 with 広 scope yields 優先対応, and the 4.0–6.9 + 中 + passive-attack combination may terminate handling (S041.txt:1462-1464). If the posture terms or the closing rule change, the framing here is stale.

## Rejected over-generalizations

- **Rejected: “JVN 緊急 equals CVSS-critical, so it is an immediate remediation mandate.”** 緊急 is a display band on the CVSS v3 base score (S046.txt:566,570); the guideline assigns handling postures through its own impact matrix (S041.txt:1465-1490), and neither report attaches a schedule or payout to the label.
- **Rejected: “The 2026 Q3 percentages describe Japanese severity in general.”** They are one quarter's registration share (S047.txt:239); the same report's per-year rows (for example 2023's CVSSv3 totals versus 2026's, S047.txt:241-260) vary year to year, so the figure is quarterly, not a stable law.
- **Rejected: “A high CVSS base score alone decides handling.”** 付録4 explicitly combines the base score with impact scope and defaults 広 when the three scope elements are unknown (S041.txt:1491-1501), so the score alone never fixes the posture.

## Attribution and boundary

The vocabulary and distribution statements are IPA's own JVN reports (S046, S047); the impact-model statement is the IPA/JPCERT/CC partnership guideline (S041). They are first-party public documents, not universal rules for other coordinators or programs. This entry is documentation-only: it instructs no probing, scanning, login, or submission against any target, and carries no credential, session, or private-URL material.
