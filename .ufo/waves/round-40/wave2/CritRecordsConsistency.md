# CritRecordsConsistency — round-40 falsify wave 2 (records attack)

Seat: `CritRecordsConsistency`, critic. Lane: kasegi-shokunin. Ref Y = judged head J = `3074c7679d6f527ec3930d7748ccce1dbae4a58a` (J5) + receipt `.ufo/waves/round-40/final-gates/all-gates.txt` (untracked; the only uncommitted record). Verified `git diff --name-only 3074c7679…` = empty; untracked extras in the working tree are the receipt + `kasegi-r40-falsify.ready` flags. All counting commands re-run at Y (live lane where read-only, or a scratch fixture clone `5439b27a2f1deb76e9ac19c4239730ee11b4c454` = J5 + the receipt committed, built per host-guard rules; `git rev-parse --show-toplevel` asserted before commit).

## 1. Findings (defects / overstatements)

**F1 — Residual R2-class overstatement, uncorrected: `corpus/lessons/round-39.md:76` (M39-1 row, last cell).**
States "`--export-ref J` on the final head prints 7/8 with G2 receipt=0; `--export-ref Y` prints 8/8". The committed final r39 receipt at Y (`8371e7ac9f32cae5ed72f8c28205634603f836fa:.ufo/waves/round-39/final-gates/all-gates.txt`, all-gates v5, sha256 `8d46d7b251fd6736ba1841814274201176d3a7628f9330e8c9b1917013741471`) records `closed=7/8 exit=1` and `selftest cases=8 failures=1`. No `Correction (round 40)` tag touches this row (the corrections at `:98-99` cover the C1 after-cell `:15` and the Final-measurement paragraph only). This is exactly the R2 class the round claims to have swept: a record still asserting r39 C1 8/8 at Y without an appended correction. (Minor-moderate; does not affect the four H2-scored records.)

**F2 — Leftover assembly markers inside committed canonical records.** Build spec (`build-wave1-spec.py:50`) says the L1 strips the `## BLOCK <record>` marker line; the markers remain committed in all four records:
- `SCORECARD.md:1586` `## BLOCK SCORECARD.md`
- `LOG.md:1721` `## BLOCK LOG.md`
- `SHONEN.md:205` `## BLOCK SHONEN.md`
- `corpus/lessons/round-39.md:96` `## BLOCK corpus/lessons/round-39.md`
Packaging hygiene defect (scaffold lines in canonical records); no score impact.

**F3 — Duplicate heading in the round-40 lesson.** `corpus/lessons/round-40.md:29` and `:31` both read `## Gate` (consecutive, empty line between). Formatting defect.

**F4 — M40-1 row quotes an uncommitted run without the `report-only` label.** `corpus/lessons/round-40.md:22` evidence cell cites "the L1's own run over `5006097a` (`closed=6/8 exit=1`; `selftest cases=8 failures=2`; scratch verify-Y.txt)". Under the round's own new criterion R37 (`corpus/QUALITY.md:323`), a lane record quoting a run result must carry a committed transcript or the sentence must say `report-only`; "scratch verify-Y.txt" is neither committed nor labelled `report-only` (the label "scratch" is adjacent but is not the R37 token). Borderline; recommend appending `report-only` to the evidence cell.

## 2. Green re-runs and reproduced counts (evidence, not defects)

All claims.json counting commands re-run at Y / fixture Y:

| Command / check | Expected (claims) | Observed at Y |
|---|---|---|
| `r40-closure.sh` plain run | exit 2 | exit 2 (`refusing to run against the live worktree`) |
| `r40-closure.sh --export-ref <Y>` | `closed=10/10 exit=0` | `closed=10/10 exit=0` on fixture Y `5439b27a…`; **full byte-identical output vs the committed all-gates.txt incl. the H7 line** |
| `r40-closure.sh --selftest --export-ref <Y>` | `selftest cases=10 failures=0`, exit 0 | `selftest cases=10 failures=0`, exit 0 (ten graded H1-H10 case lines) |
| `r40-closure.sh --export-ref a7af2ce6…` | `closed<10/10 exit=1` | H8 `base=3/10,base-exit=1` → closed 9/10 exit 1 |
| `r40-closure.sh --export-ref 8371e7ac9f32cae5ed72f8c28205634603f836fa` | `closed<10/10 exit=1` | H8 `r39=2/10,r39-exit=1` → closed 9/10 exit 1 |
| queued among the nine | 0 | 0 |
| mined among the nine | >=4 | 7 |
| knowledge entries citing the nine | = mined | 7 |
| S060+ registry rows | >=1 | 3 (S060 mined, S061/S062 rejected) |
| knowledge entries citing S060+ | >=1 | 1 (`corpus/knowledge/cyclonedx-analysis-subtree.md`, `source: S060`, `ground: F23`) |
| frontier rows | 23 | 23 (F01-F23, all `admitted`) |
| `frontier-recheck-count.py` | entries=26 pass=26 exit=0 | entries=26 pass=26 exit=0, incl. PASS F23 ids=S060 |
| registry total | 62 | 62 (S001-S062 sequential, no duplicate ids) |
| measure `(20+F_admitted)/(20+F_total)` | 43/43 = 1.000 | F_total=23+0=23, F_admitted=23 → 43/43 = 1.000 |
| census `sources-census.sh validate` | exit 0 | exit 0, exactly `W04 S028`, `W04 S029`, `ok` (no new W/E code) |
| `capture-binding-check.py` | records=54 bound=54 | records=54 bound=54 unbound=0 |
| `source-recheck.py` per mined row (S016/S017/S019/S020/S021/S023/S025/S060) | all exit 0 | all exit 0 (anchors OK, `occurrences=1`) |
| capture sha256 (all 8) | match lesson table | all 8 match exactly (91cc996f…, 3b6aaf1f…, 514cc3796…, 8fc334beb…, 72dbba5730…, 52a6671fb2…, faa1c1f8b9…, d68626222139…) |
| `Correction (round 40)` lines | >=1 per record, all naming `closed=7/8 exit=1` + `selftest failures=1` + G2/G6 reason | 2 per record ×4 records = 8; 5 carry both final values (matches receipt H2 `corrections=8,named=5,missing=0,fences=closed`); all 8 carry G2/G6 non-independence reason |
| QUALITY criterion citing M39-2 | >=1 | `corpus/QUALITY.md:323` (R37), exactly one |
| receipt `run-utc` | = ref committer instant, not future-dated | `2026-10-26T21:56:22Z` == committer instant of J5 `3074c7679…` (18:56:22-03:00) |
| suite sha256 | `bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e` | committed `corpus/instruments/r40-closure.sh` == wave1 `ExecSuiteBuild.r40-closure.sh` == receipt header |

Future-dated `run-utc` sweep over every committed `final-gates/all-gates.txt`:
- r37 `83975ac`/`2387dcf6` receipts: 18:00:21Z ≤ commits 18:03:15Z/18:01:28Z — OK.
- r38 `f06148c6`/`6c0ae18`/`7dd2fcd` receipts: no `run-utc` header — OK (none).
- r39 attempt-1 `5006097a`: 21:35:00Z > commit 20:12:12Z — future-dated; this is the mined M40-1 case (correctly flagged in `corpus/lessons/round-40.md:22`).
- r39 final `8371e7a`: 20:54:44Z ≤ commit 20:55:17Z — OK.
- r40 receipt: equals committer instant — OK.
No other future-dated `run-utc` exists at Y.

`⟨pending` / placeholder sweep: no `⟨pending` in `corpus/lessons/round-40.md` or any round-40 record (committed or working tree); the only `⟨pending` strings in the repo are historical (round-37 wave1 lesson draft) or in attack/fixture text about the scan itself. No `TODO`/`FIXME`/`TBD`/`PLACEHOLDER` tokens in the round-40 lesson, declared-blocks.txt, all-gates.txt or wave1 receipts (the `not yet integrated/landed/committed` phrases in `wave1/ExecAuditRun.md:6`, `wave1/ExecH9DeclaredBlocks.md:265`, `wave1/ExecH7Determinism.md:45` describe bootstrap states of the wave itself, not placeholder tokens).

## 3. Missing transcripts for quoted runs — scan result

- Correction blocks (11 records) quote the final r39 receipt values: committed transcript exists (`8371e7a…all-gates.txt`, sha256 verified). OK.
- Lesson C1 after-cell quotes `closed=10/10 exit=0`: committed receipt (teed run transcript) exists; byte-identical re-run reproduced it. OK.
- Lesson C1 after-cell quotes `selftest cases=10 failures=0`: no committed selftest transcript exists (all-gates.txt is the run transcript only; wave1 receipts contain fixture transcripts, not the suite's own selftest run). Reproducible (re-run above), so recorded as a compliance observation, not a false statement.
- Lesson Gate sections quote fetches/captures: all 8 captures committed with matching sha256; `source-recheck` passes. OK.
- Lesson Census section quotes `W04 S028`, `W04 S029`, `ok`, exit 0: reproduced live. OK.
- M40-1 quotes L1's own run via scratch path: see F4.

## 4. Evidence pointers resolve

- `wave2/CritG2Exploit.md`, `wave2/CritC1Kill.md` (cited by all four correction blocks and the claims) exist at `.ufo/waves/round-39/wave2/` (committed at `8371e7a`). OK.
- Claim evidence pointers: `c1-controls/before.txt`, `c2-controls/before.txt`, `c2-controls/junk-decisions.md`, `census-before.txt` exist. OK.
- Lesson deliverable cites (`wave1/ScribeNewRows.txt`, `wave1/ScribeRows.decisions.txt`, `wave1/ScribeF23.readme-row.txt`, `wave1/ScribeF23.province.txt`, `wave1/ScribeF23.entry.md`, `wave1/ExecRecheckAll.md`, `wave1/ExecBindingCheck.md`, `wave1/ScribeGateBlocks.txt`, `wave1/ScribeEntriesG1.*`, `wave1/ScoutS*.capture.txt`/`manifest-record.json`, `wave1/ExecMistakesDraft.h5-replica.sh`, `wave1/ExecForgeFixtures.*`) — all exist. OK.
- Historical SCORECARD `wave2/*` refs (round-31 section: `ExecCounterFix.md`, `CritExpansion.md`, `ExecCensusFinal.md`, `MutCtr*.md`, `RevEntryQ.md`, `RevQuoteRoles.md`, `RevQuoteRoutes.md`, `RevRowS048.md`) all exist at `.ufo/waves/round-31/wave2/`. OK.
- M40-1 able-to-fail proof: `wave1/ExecMistakesDraft.h5-replica.sh` + `wave1/ExecMistakesDraft.txt` record `H5 … dated=future closed=0` for the future-dated fixture (lines 50/54) — consistent with the lesson's `dated=future closed=0` claim.

## 5. Consistency notes (no defect)

- Registry 59 → 62 = +3 new rows (S060/S061/S062); no rows removed (S001-S062 sequential). OK.
- Lesson C2 after-cell numbers all reproduce (queued 0, mined 7, S060+ 3, frontier 23, harness 26/26, registry 62, measure 43/43). OK.
- `S022`/`S024` rejection flips documented in lesson and row anchors (`supersedes S022` in S030; `supersedes S024` in S029). OK.
- The census used for the round-40 "after" is documented as the mirror run; a live census over the landed tree reproduces the same result (exit 0, W04 S028/S029), so the claim's census limb holds at Y. OK.
- Current state note: the final-gates receipt is not yet a commit; `git status` shows `.ufo/waves/round-40/final-gates/` and the two `kasegi-r40-falsify.ready*` flags untracked. The suite's H7 limb requires the receipt inside the export, so the green 10/10 window is reached only once the receipt is committed as Y (verified via fixture `5439b27a…`). No record claims a commit-Y that does not exist; this is a filing-time state note.
