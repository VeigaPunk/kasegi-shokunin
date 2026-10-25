# C2S039Quote — re-open S039; crosswalk & JP entry quote bindings, ISO/CERT/CVE statements

Seat: `L1Kasegi25.C2S039Quote` (wave 2, read-only reviewer).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Subject artifacts: `corpus/source-snapshots/round-25/S039.txt` (696 lines, sha256
`657e7b4c…191d`), `corpus/source-snapshots/round-25/manifest.json` (S039 record Q1–Q9),
`corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` (JP entry),
`corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` (crosswalk),
`.ufo/waves/round-25/wave1/quotes-vendor-jp.json` (wave-1 receipt).
Wave-1 receipts read: `RevQuotesJP.md`, `EntryCiscoCrosswalk.md`, `quotes-vendor-jp.json`, claims.json.

## Verdict

**Wave-1 result is substantially correct — every S039 quote string binds verbatim, exactly once, to
the cited capture line, and the ISO/CERT/CVE statements are true — but two load-bearing citations
are wrong and should be corrected:**

- **F1 (moderate, propagated ×3):** the CVE/CNA quote at capture line **557** is labeled "§1.5
  CVE採番と公開プロセス" in the JP entry, the crosswalk, and the manifest. §1.5 spans L535–L541;
  the heading **"1.6 活動トピックス"** sits at **L542**, so L557 belongs to §1.6 (its "2022年から"
  item). The line number and the quote are right; the section name is wrong in three places.
- **F2 (minor):** crosswalk falsifiable rule 2 (line 83) cites "S039 (L520, **L533**)" for
  JPCERT/CC. `JPCERT` occurs in S039 at **L520 and L571 only**; L533 names JVN and the CERT/CC
  Vulnerability Notes Database, not JPCERT/CC.
- **F3 (minor):** JP entry `source:` line (L6) names only "the 4 IRT model intro, 1.2, 1.3" and the
  span `S039.txt:491-519`, but its own quoted record uses **L520** (still §1.3) and **L557** (§1.6);
  §1.1 is also unlisted though its quote is used at entry L146–147.

Everything else verified clean: all nine manifest quotes occur exactly once at their cited lines
(instrument re-run: `S039:sha256 OK` + Q1–Q9 `OK occurrences=1`, exit 0); the four crosswalk
`hitachi-*` labels map to manifest Q5/Q7/Q8/Q9 exactly; `29147` counts are `S036 0 / S038 0 /
S039 8 / S040 1` exactly as crosswalk rule 1 predicts; `30111` = `S039 7 / S040 0` (no 30111
overclaim on Cisco — RevQuotesJP U2 boundary respected); `CVSS`, `報奨金`, `招待` = 0 on S039;
CERT/CC at L511–512, L520, L524, L525, L533 as the matrix asserts; CVE/CNA prose at L536–537 and
the June-2022 CNA sentence at L557 verbatim.

## Evidence (commands, output, exits)

Run from lane root unless stated. Exit codes: all 0 except the greps that return 1 on zero matches
(noted inline; those zero-matches are the *asserted* result, so grep's exit-1 is expected).

### Capture integrity

```
$ sha256sum corpus/source-snapshots/round-25/S039.txt
657e7b4c67e67d00b190b31942d749a28d0988f15d1e6f5f506130accffc191d   → exit 0
# matches capture-log.txt ("S039 ... sha256=657e7b4c...191d") and manifest.sources[S039].sha256
```

### Exactly-once quote binding (all nine manifest quotes)

```
$ python3 - <<'PY'   # per-quote grep -c -F + line-of-hit vs cited line — abridged transcript
Q1 grep_c=1 hit_lines=[491] cited=491 OK
Q2 grep_c=1 hit_lines=[506] cited=506 OK
Q3 grep_c=1 hit_lines=[506] cited=506 OK
Q4 grep_c=1 hit_lines=[510] cited=510 OK
Q5 grep_c=1 hit_lines=[519] cited=519 OK
Q6 grep_c=1 hit_lines=[519] cited=519 OK
Q7 grep_c=1 hit_lines=[497] cited=497 OK
Q8 grep_c=1 hit_lines=[520] cited=520 OK
Q9 grep_c=1 hit_lines=[557] cited=557 OK
PY   → exit 0
```

### Instrument re-run

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S039
S039:sha256 OK
S039:Q1 OK occurrences=1
... (Q2–Q9 identical) ...
exit=0
```

### ISO statements

```
$ for s in S036 S038 S039 S040; do printf '%s %s\n' "$s" "$(grep -c 29147 corpus/source-snapshots/round-25/$s.txt)"; done
S036 0 / S038 0 / S039 8 / S040 1        → matches crosswalk rule-1 prediction verbatim; exit 0
$ same loop with 30111
S036 0 / S038 0 / S039 7 / S040 0        → confirms no 30111 claim attaches to S040; exit 0
$ grep -n '30111' <both knowledge entries>
# only hit: crosswalk:25 (the S039 matrix cell asserting 30111:2013 at L497-L499 + L621 link); exit 0
```

Capture lines 497–499 (verbatim): `ステップ１：脆弱性情報の入手 ... (1) ISO/IEC 29147:2014
脆弱性情報の開示` / `ステップ2：調査ならびに対策 ... (2) ISO/IEC 30111:2013 脆弱性対応手順` /
`ステップ3：情報公開 ... (3)(4) ISO/IEC 29147:2014 脆弱性情報の開示`. §2.6 lines 615, 621 carry
the `29147:2018` and `30111:2019` edition links — exactly as the matrix cell claims.

### CERT statements

```
$ grep -n 'CERT/CC\|JPCERT' corpus/source-snapshots/round-25/S039.txt
# occurrence lines: 511 (heading CERT/CCからの通知), 512, 520 (CERT/CCやJPCERT/CCの協力を得て),
# 524, 525, 533 (CERT/CC x2 + JVN); JPCERT/CC on 520 AND 571 — NOT 533; exit 0
$ grep -c 'JPCERT' corpus/source-snapshots/round-25/S038.txt → 0 (grep exit 1)
$ grep -c 'CERT/CC' corpus/source-snapshots/round-25/S038.txt → 0 (grep exit 1)
```

Crosswalk matrix cell (L26) cites S039 partners as "L510, L512, L520, L533" — every cited line
verified; the cell is non-exhaustive (L524/L525/L571 also name coordinators) but makes no
exhaustiveness claim. JP entry L149–150 quotes the L520 fragment verbatim, cited correctly.

### CVE statements

```
$ grep -n 'CVE' corpus/source-snapshots/round-25/S039.txt | cut -c1-100
519 (CVE採番については、1.5節を参照 pointer), 535 (heading 1.5), 536, 537 (CNA procedure), 557
$ sed -n '535,557p' S039.txt
535 "1.5 CVE採番と公開プロセス" … 541 "*1 …" — then 542 "1.6 活動トピックス", 556 "2022年から",
557 "2022年6月より、HIRTはCVE IDを日立製品の脆弱性に割り当て、CVEレコードを作成し公開することの
できるCVE Numbering Authority(CNA)になりました。…"   → exit 0
```

The entry quote `2022年6月より、HIRTはCVE IDを日立製品の脆弱性に割り当て` is a verbatim substring
of **L557, under §1.6**, labeled §1.5 in: JP entry L153
(`— 1.5 CVE採番と公開プロセス, capture S039.txt:557`), crosswalk L66
(`| hitachi-cna | … | L557, §1.5 CVE採番と公開プロセス |`), manifest Q9 location and
wave1 `quotes-vendor-jp.json` L170.

### Miscellaneous counts

```
$ for s in S036 S037 S038 S039; do printf '%s %s\n' "$s" "$(grep -c '招待' corpus/source-snapshots/round-25/$s.txt)"; done
0 / 0 / 0 / 0        → JP entry rejection #5 verified; exit 1 per grep (zero matches)
$ grep -c 'CVSS' S039.txt → 0;  grep -c '報奨金' S039.txt → 0
$ python3 -c "manifest totals" → sources=5, quotes S036=8 S037=6 S038=7 S039=9 S040=9, total=39
```

## Findings (severity order)

| # | sev | artifact:line | defect | smallest correction |
|---|---|---|---|---|
| F1 | moderate | JP entry `vendor-disclosure-policies-as-corpus-objects.md:153`; crosswalk `vendor-disclosure-policy-commitments-crosswalk.md:66`; manifest `corpus/source-snapshots/round-25/manifest.json` Q9.location (and wave1 `quotes-vendor-jp.json:170`) | L557 attributed to "§1.5 CVE採番と公開プロセス"; §1.5 ends at L541, "1.6 活動トピックス" begins L542, L557 is its "2022年から" item. Quote + line right; section label wrong, propagated to 4 files. | Relabel to "§1.6 活動トピックス (2022年から item)". Content is topically correct — a reader grepping section 1.5 for the sentence would not find it. |
| F2 | minor | crosswalk `vendor-disclosure-policy-commitments-crosswalk.md:83` | Rule 2 cites "S039 (L520, L533)" for JPCERT/CC; `grep -n JPCERT S039.txt` → L520, L571 only. L533 names JVN + CERT/CC VDB. | Change "(L520, L533)" → "(L520, L571)" or drop the parenthetical. |
| F3 | minor | JP entry `:6` (`source:` line) | Descriptor lists "intro, 1.2, 1.3" and span `S039.txt:491-519`; entry's own quotes use L520 (still §1.3, outside the printed span by one line) and L557 (§1.6, unlisted). | Widen descriptor to include §1.1 and §1.6 and span `:491-557`. |
| F4 | low | crosswalk `:80` (rule-1 prose) | "they name different editions (2018 in S040, 2014 in S039)" reads as if S039 names only 2014; S039 also names 29147:2018 at L615 (the matrix cell itself says so at L25). Check output is correct; prose is imprecise. | Qualify: "mapped edition 2014 (it also lists 29147:2018 as a §2.6 link)". |
| F5 | low | crosswalk `:30` (lifecycle row) | S039 cell "none stated" is defensible — no handling boundary is stated — but the document does carry "2.1 日立製品のライフサイクル" pointing EOL to per-product pages (L560–563), a deferral analogous to Cybozu's §2.x pointers. | Optional: "none stated; §2.1 defers EOL to per-product pages". |

## Verified-clean items (no defect)

- JP entry claim-7 six-quote block (L125–141): every string verbatim, line-cited correctly, each
  `grep -c -F` = 1, and Q3 (`協調した脆弱性対策を開始します。`) lands on the same L506 as Q2 as labeled.
- No coordinator overclaim: the 届出窓口 route (L506) is quoted as the partnership's reporting
  desk — neither entry substitutes CERT/CC or JPCERT/CC for it (respects RevQuotesJP's caution at
  wave1 `RevQuotesJP.md:89`).
- 公表日一致 framing: L519 quote + "関係者間で一定の足並み" — JP FR-4 and the crosswalk "clock"
  claim hold; no duration asserted anywhere. Verified L519 verbatim.
- S040 ISO claim confined to 29147:2018; `30111` appears only in the S039 cell (entry grep above).
- Rejection #4 ("HIRT-PUB10008 is one vendor's process doc") supported by L491 (focus) and
  `日立グループにおける` (L486, L491).
- Manifest shape: 5 sources / 39 quotes matches the wave-1 claim ("manifest 5 sources/39 quotes").

## Residual risk / verification gaps

- I verified the **bytes of record**, not the live page; S039 is a moving document
  (更新日 2026年10月14日 at L487) — quotes are snapshot-scoped, as both entries' own Limits state.
- The JP-entry `source:` span and section labels are descriptive metadata, not quote assertions; the
  instrument only enforces quote↔sha256 binding, so F1–F3 survive any recheck pass. That is exactly
  why F1 propagated through manifest + two entries + a wave-1 receipt unnoticed.
- Crosswalk S039 cells I spot-checked are non-exhaustive by design; I verified every line they cite
  but did not prove negative-space (e.g., all lines naming coordinators) exhaustively beyond the
  greps shown.
- No tools installed or upgraded this run (pacman paused; none needed beyond coreutils/python3 —
  both already present). No tool record owed.
