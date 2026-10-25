# ScribeRegistryC2 — corpus/SOURCES.md (round 28, wave 1)

Seat scope: the lane registry only. One production file written: `corpus/SOURCES.md`.
Base `c9f8b115a098c65356e4b3b6048af45a37ab8395`; before sha256 `fe148213…`, after sha256
`e59240f8e9842535e815f7d4575be7ea11a6a57a7bbaead43cbea92bd013945d`.

## Behavior delivered

1. **S042 appended** as the last `## Registry` row (line 48), normalized to the fleet schema
   from the staged `SOURCES.append.md` bytes rather than copied: id `S042`, source =
   IPA 脆弱性関連情報の届出受付業務における取扱いプロセス（https://www.ipa.go.jp/security/todokede/vuln/process.html）,
   kind `docs`, tier `A`, scope = the page's three flows (software product 10 steps, web
   application 7, vendor own-product), anchor = the 10-step flow (heading `L132`, steps
   `L133-L159`) plus `5.起算日の連絡` (`L144-L145`) verified against the round-28 capture,
   teaches = one grounded learner benefit (coordinator mediates; finder is told the 起算日 and
   the detail-information date, `L145`), status `mined`, opened `2026-10-25`, recheck `180d`,
   used-by exactly `corpus/knowledge/japanese-domestic-disclosure-workflow.md`. 11 cells,
   12 pipes, 0 escaped pipes, `NF=13` under the census grammar.
2. **S041 used-by extended** by exactly `, corpus/knowledge/japanese-domestic-disclosure-workflow.md`;
   a mechanical cell split of the pre-change row (`git show HEAD:…`, line 47) against the
   landed row proves the used-by cell is the *only* differing cell (13 cells in, 13 out,
   differing index `[11]`).
3. **Two change-log lines** appended at `## Registry changes`, in the round-26 precedent
   shape (old → new in backticks, with the reason and the R8 marker).

## Gates

| Gate | Result |
|---|---|
| Row grammar (E01: 11 cells / NF=13) | pass — `NF=13`, 12 pipes |
| No escaped/literal pipe in any cell | pass — 0 |
| URL uniqueness (E04/W04 from this row) | pass — `todokede/vuln/process.html` appears once |
| Anchor grounded on landed capture bytes | pass — S042.txt sha256 `b432ec16…` equals the manifest pin; cited sentence, 最終更新日 and `5.起算日の連絡` each exactly once |
| Anchor line convention matches the entry header | pass — steps `L133-L159`, flow heading `L132`, aligned with the entry's `source: S042` header |
| Census, real production root, after the entry landed | **exit 0**, only the two pre-existing W04 (S028, S029) |
| Registry rows | 41 → 42 |
| Diff hygiene | 1 removed line (old S041), 4 added; no other hunk |

## Out of scope (untouched)

`corpus/README.md` F12 row, `corpus/QUALITY.md` R14, the F12 entry, `corpus/lessons/round-28.md`,
`LOG.md`, `SCORECARD.md`, `corpus/instruments/*`, the round-28 captures and manifest,
`considerthese/`. The R8 lesson line is delivered verbatim in the receipt for ScribeLesson to
lift, because the lesson is not this seat's file.

## Findings for the L1

- **Census closes at exit 0.** Between my edit and the entry landing, the real-root run was
  PRE-STATE exit 1 with two E11 lines naming only
  `corpus/knowledge/japanese-domestic-disclosure-workflow.md`. That is recorded in the receipt
  as history, not as a result; the final run after the entry landed is exit 0 with the two
  pre-existing W04 warnings only. No registry defect was ever involved.
- **Staged row was wrong about the web-application flow.** `SOURCES.append.md` anchors it as
  "steps 1 to 6"; the round-28 capture runs to step 7 (`L162-L181`, heading `L161`,
  `7.統計情報の公表` at `L181`, its body at `L182`). The staged claim was not carried; the
  change-log line records why. Any C2 text still saying "six steps" should be corrected by its
  own owner.
- **Line convention reconciled.** The capture seat reports the product flow as `L133-L159`
  (step headings) while the block ends at `L160` (step 10's body). The row and the change log
  cite the step-heading range and name the flow heading line separately, so the row and the
  capture seat agree.
- **Cross-seat conflict recorded, not resolved by me.** The F12 entry's `source: S042` header
  cites `ウェブアプリケーション 1.–7. (L162-182)`; ExecCaptureS042 reports the web-app steps
  as `L162-L181`, with `L182` being step 7's body. Both describe the same bytes under different
  conventions. The registry is unaffected (my row names no web-app line range); the entry
  header belongs to ScribeEntryC2.
- **Scope cell names all three flows** on purpose: the page carries ソフトウエア製品 (10 steps),
  ウェブアプリケーション (7 steps) and 自社製品 flows (`L183`), so a two-flow scope would have
  read as exhaustive and been false.

## Artifacts

- Receipt: `.ufo/waves/round-28/receipts/ScribeRegistryC2.txt`
- This report: `.ufo/waves/round-28/wave1/ScribeRegistryC2.md`
- Scratch probe roots (disposable, `/tmp`): `tmp.vUDmuUehKg/kasegi`, `tmp.ZlacGiL5np/kasegi`
- No tool installed; no pacman transaction; no VCS write.
