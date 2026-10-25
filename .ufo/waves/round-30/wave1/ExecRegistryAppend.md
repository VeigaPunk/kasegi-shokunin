# ExecRegistryAppend — round-30 wave-1 seat report

Seat: `ExecRegistryAppend` (L2 executor, leaf). Lane: kasegi-shokunin. Base `a94871315cafa368f79c17d8c62d71fddd967986`; claims-freeze `3c5573541300ba0fd3d89372dda3d841172eaa3f`. Answering model: `inception/mercury-3` (config route table; no model passed). No tool installed (none needed).

## Scope

Sole writer of the `corpus/SOURCES.md` registry appends for this round:
1. Append rows S046 and S047 after the last registry row (S045), 11 columns each, no `|` inside any cell.
2. Append "Registry changes" lines (R8: rows added old → new; any status/recheck/used-by cell change logged old → new).

## Files changed

- `corpus/SOURCES.md` — exactly the two registry rows + three Registry-changes lines. No existing row touched.

## Registry rows appended (verbatim, as landed at lines 52–53)

```
| S046 | IPA JVN activity report — https://www.ipa.go.jp/security/reports/vuln/jvn/ug65p90000019ev2-att/000095610.pdf | docs | A | JVN's own severity vocabulary: the CVSS-to-深刻度 band definitions | capture corpus/source-snapshots/round-30/S046.txt: 注1) CVSSv2 基本値の深刻度による色分け (レベルI 注意 0.0-3.9 / レベルII 警告 4.0-6.9 / レベルIII 危険 7.0-10.0) and 注2) CVSSv3 (注意 0.1-3.9 / 警告 4.0-6.9 / 重要 7.0-8.9 / 緊急 9.0-10.0), lines 555-570 | JVN has no native severity scale — it maps CVSS base scores onto Japanese labels keeping legacy v2 bands | mined | 2026-10-25 | 180d | corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md |
| S047 | IPA JVN quarterly registration report — https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html | docs | A | JVN quarterly severity distribution | capture corpus/source-snapshots/round-30/S047.txt: 2-2 深刻度別割合, 図2-2 (CVSSv2 レベル1-3) and 図2-3 (CVSSv3 注意/警告/重要/緊急), lines 215-240 | Japan's national database carries CVSS-derived severities at scale | mined | 2026-10-25 | 90d | corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md |
```

Both anchors verified against the captured bytes:
- S046.txt lines 555–570: `注 1）CVSSv2 基本値の深刻度による色分け` (0.0–3.9 レベルI 注意 / 4.0–6.9 レベルII 警告 / 7.0–10.0 レベルIII 危険) and `注 2）CVSSv3 基本値の深刻度による色分け` (0.1–3.9 注意 / 4.0–6.9 警告 / 7.0–8.9 重要 / 9.0–10.0 緊急).
- S047.txt lines 215–240: `2-2. 脆弱性に関する深刻度別割合` with `図2-2` (CVSSv2, レベル1–3) and `図2-3` (CVSSv3, 注意/警告/重要/緊急), including the 2026 Q3 distribution percentages.

Capture digests measured (sha256):
- `corpus/source-snapshots/round-30/S046.txt` = `884481f3781e200d4c7e6efd91b2912ada513fa126c534d3392ccd48003a03a3` (575 lines)
- `corpus/source-snapshots/round-30/S047.txt` = `bcf4f605d75909301f02560df894e0c4c15d97c7928a1759f57b15b5a7d905f4` (1402 lines)

## Registry changes lines appended (R8)

- S046 row added: new row (id S046, tier A, mined, opened 2026-10-25, recheck 180d, used-by `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md`); staged SOURCES.append.md S049 cells → landed: opened 2026-10-23 → 2026-10-25; anchor rewritten from the round-30 capture; used-by → the F14 entry only.
- S047 row added: new row (id S047, tier A, mined, opened 2026-10-25, recheck 90d, used-by same entry); staged SOURCES.append.md S050 cells → landed: opened 2026-10-23 → 2026-10-25; recheck 180d → 90d; anchor rewritten from the round-30 capture; used-by → the F14 entry only.
- No status/recheck/used-by cell changed on any pre-existing row; S041–S045 untouched (logged). Registry 45 rows → 47 rows.

## Verification

Measured at the landed working-tree bytes. `corpus/SOURCES.md` sha256 (final, post-changelog) = `a126a5f339323d5ae417a944d163d75a0427d9c77a5a330308e193dc7b81d927` (pre-changelog append-state digest `ce54089cfd3efa9301c12fe3b58ea0281b7632f749338ada8746f88a2f4fe01c`).

- Registry rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`): **47** ✔
- S046+S047 rows present (`grep -cE '^\|[[:space:]]*S04[6-7][[:space:]]*\|' corpus/SOURCES.md`): **2** ✔
- `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`: output `kasegi W04 S028 …`, `kasegi W04 S029 …`, `kasegi ok /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`, **exit 0** (W04 S028/S029 only) — measured after the F14 entry landed; E11 was present while the entry was absent, see below.

### Timeline note (E11 dependency)

Immediately after the append, census validate reported `E11 S046/S047 missing used-by corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` (exit 1) because the F14 knowledge entry had not landed yet (another seat's write). Polled for the entry; final validate result above is post-entry-landing.

## Risks / notes

- The F14 entry citecorpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` and the round-30 manifest (`corpus/source-snapshots/round-30/manifest.json`) are owned by other seats; this seat only registered the rows they cite.
- No write outside the lane repo; no git/jj mutation, no live target contact, no tooling installed.
