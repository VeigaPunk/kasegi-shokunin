C1 SURVIVES — all 8 kill-rule clauses PASS at measurement time (2026-11-03); the fail-entry-records derive repair is honest, host-portable, convention-consistent, and still binds its (now historical) target; two non-blocking weaknesses reported as text only (path-not-blob, non-line-anchored grep).

Seat: ReviewDerive, kasegi r57 w1. Scope: attack the C1 derive repair only. Read-only on the lane; no file under L edited. Tooling authorization: nothing installed (python3 3.14 / git / grep / sed present on host; no upgrade needed).

## Kill-rule clause table (claims.json C1, frozen)

| # | Clause (fail condition) | Evidence | Verdict |
|---|---|---|---|
| 1 | green audit exits != 0 or summary != 'FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0' | E7 | PASS |
| 2 | selftest failures != 0 or exit != 0 | E8 (also committed: do-nothing-c1-r57.txt tail) | PASS |
| 3 | red control 1: <1 stale line, stale on entry other than registry-rows-r56, or exit 0 | E9 (c1-red-r57.txt RED 1) | PASS |
| 4 | red control 2: <1 stale line, stale on entry other than fail-entry-records, or exit 0 | E9 (c1-red-r57.txt RED 2) | PASS |
| 5 | do-nothing: any of the 8 new ids present at base, or base audit not red | E10, E11 (receipt + my independent per-id grep over the base blob) | PASS |
| 6 | any new ledger entry's derive absent from the printed receipts | E12 (all 8 printed with derived==recorded in the green run; nuance noted) | PASS |
| 7 | amended record cell lacks the round-57 amendment sentence | E13 (sentence present; line-by-line accuracy in E4) | PASS |
| 8 | audit red at the truly final tree (gate-final limb) | E7 (green over the current tree; tree is committed at HEAD cd30298, only .ufo/waves/round-57/w1/ untracked); final-tree reprint is gate-final's by design | PASS at measurement |

## Numbered evidence

E1. Working-tree record/derive (L/corpus/instruments/figure-audit-ledger.json, entry fail-entry-records; fields record/recorded/derive/want = "33"):
- record: ".ufo/waves/round-53/controls/c2-counter-final-r53.txt:8 FAIL_entry_records=33 (the :9 trailer's '34' is superseded by the r54 D53-1 correction); 33 = entries - pass at the r53 Windows-host state. Amended round 57 (the run-15 host transition): the previous derive re-ran the frontier counter live, which read the Windows-host-only FAIL class (0 FAIL lines on this Linux host - the base do-nothing receipt .ufo/waves/round-57/controls/do-nothing-c1-r57.txt captures that exact red); the derive now reads this same receipt line, the record of record, host-portable. want unchanged 33."
- derive: `grep -oE 'FAIL_entry_records=[0-9]+' .ufo/waves/round-53/controls/c2-counter-final-r53.txt | head -1 | cut -d= -f2`

Prior version:
- cmd: `git -C L show 8a5d7538b0caa50300b1eee88442a230d9a433f2:corpus/instruments/figure-audit-ledger.json` (27 entries; fail-entry-records extracted)
- prior record: same :8/:9 citation, then "33 = entries - pass, preserved by the declared round-54 after-state (38-5=33)"
- prior derive: `python corpus/instruments/frontier-recheck-count.py 2>/dev/null | grep -c '^FAIL'` — live re-run of the counter.
- exit 0.

E2. New derive run, cwd L:
- cmd: `cd L && grep -oE 'FAIL_entry_records=[0-9]+' .ufo/waves/round-53/controls/c2-counter-final-r53.txt | head -1 | cut -d= -f2`
- out: `33`; exit 0.

E3. Cited line check:
- cmd: `sed -n '8p' L/.ufo/waves/round-53/controls/c2-counter-final-r53.txt`
- out: `FAIL_entry_records=33 not_recheck-exit-1=0 FRONTIER-FAIL_row_records=30 not_missing-pass-line=0`
- YES — this is exactly the figure the old record cited (:8). Numbered check `grep -n '' <receipt>`: line 6 `entries=37 pass=4 exit=1`, line 8 as above, line 9 trailer contains "the 34 inherited recheck-exit-1 entry records" — both the ":8" and ":9 trailer's '34'" pointers are exact. Internal consistency: 37−4=33=FAIL_entry_records at r53. The 34 is a different class (recheck-exit-1 records); the superseded note is accurate.

E4. Amendment-sentence accuracy, line by line against commands run:
1. "the previous derive re-ran the frontier counter live" — TRUE (E1 prior derive).
2. "which read the Windows-host-only FAIL class" — TRUE at r53 (receipt lines 7–8 class check; frozen host-facts mark the class host-bound to Windows).
3. "0 FAIL lines on this Linux host" — TRUE (E6: grep -c '^FAIL' -> 0; live counter prints no FAIL lines).
4. "the base do-nothing receipt ... captures that exact red" — TRUE (do-nothing-c1-r57.txt: `FIG fail-entry-records recorded=33 ... derived=UNAVAILABLE reason=derive-exit-1 stale`, summary figures=27 ok=26 stale=1 exit=1). Wording nuance: the receipt records the red as reason=derive-exit-1 (grep exit 1 on zero matches), not a literal "0" — same fact.
5. "the derive now reads this same receipt line" — TRUE (E2+E3: sole occurrence in the file is the cited :8 line).
6. "want unchanged 33" — TRUE (want field "33").

E5. Mutability/honesty attack (written):
- What the repaired figure proves now: that the committed r53 receipt records FAIL_entry_records=33, re-derivable on any host with POSIX grep. The receipt bytes are byte-stable since creation: `git log -- <receipt>` shows exactly one commit (3ffd663, r53 round); blob fbc866a7c5b46bde7228cb00c0b529b195755da6 at that commit == HEAD (cd30298) == working tree (`git diff --stat HEAD -- <receipt>` empty). Mutation-detection is proven, not decorative: red control 2 mutated a scratch copy to FAIL_entry_records=34 and the audit followed (derived=34 -> stale, exit 1).
- What it no longer proves: anything about the live tree. fail-entry-records has moved from a live invariant (counter re-run must reproduce 33) to a historical-record pin (a committed receipt must say 33). On this host the live counter reproduces none of the FAIL class (E6: entries−pass = 41−41 = 0, counter exit 0), so the original binding is unreproducible here and the record-read is the honest substitute; the amendment sentence says exactly this ("record of record, host-portable").
- Weakness 1 (path-not-blob): the derive reads the working-tree receipt path, not a rev-pinned blob. A future commit rewriting the receipt moves the derived value (detected as stale vs want=33 unless want is co-edited — the same trust model as every other receipt-derived figure; git history is the tamper evidence). A stronger form (`git show <rev>:.ufo/...`) exists in-house for corpus files but is used by no receipt-figure in the ledger (E15), so the repair follows the dominant convention rather than inventing a second one. Text-only suggestion; no edit made.
- Weakness 2 (not line-anchored): `head -1` takes the first FAIL_entry_records anywhere in the file while the record cites :8. Today exactly 1 occurrence (`grep -c FAIL_entry_records <receipt>` -> 1), so unambiguous; a future prepend above line 8 would be read instead. Cheap hardening: `sed -n '8p' | grep -oE ...`. Text-only suggestion.

E6. Old derive and live counter on this host, cwd L:
- old derive: `python3 corpus/instruments/frontier-recheck-count.py 2>/dev/null | grep -c '^FAIL'` -> `0`, exit 1 (audit marks UNAVAILABLE/derive-exit-1 -> stale — the do-nothing red).
- live counter: `python3 corpus/instruments/frontier-recheck-count.py` -> `FRONTIER-CENSUS rows=38 admitted=38 closed=38 problem-rows=0 registry=90`, `FRONTIER-PASS F38 ids=S089,S090`, `entries=41 pass=41 exit=0`; counter exit 0.

Invariant finding: the frozen want 33 = entries − pass holds only at the r53 state (37−4, E3). After the host transition it computes 0 at the base bytes (40−40) and 0 on the current tree (41−41, E6): the invariant does NOT survive as a live quantity; it survives only as the pinned receipt figure. For it to bind live on this host, the class would have to exist here (it does not — every entry recheck exits 0; the Windows-bound failure mode does not reproduce), or the derive would have to re-derive the r53-era class host-portably — a rev-pinned read of the r53 receipt (binds bytes, not just path), or a counter mode replaying r53 failure semantics. The shipped repair pins to the record instead of the world, which is the honest choice given the class is unreproducible here.

E7. Green audit over the lane root, cwd L:
- cmd: `python3 corpus/instruments/figure-audit.py`
- summary: `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`; exit 0. (The single ' stale' substring in the output is `FIG census-fresh-literal-r55 recorded=stale ... derived=stale ok` — a recorded literal, verdict ok; no stale verdicts.)

E8. Selftest, cwd L:
- cmd: `python3 corpus/instruments/figure-audit.py --selftest`
- out: `selftest cases=5 failures=0`; exit 0 (all five cases verdict=pass).

E9. Red controls (committed receipt .ufo/waves/round-57/controls/c1-red-r57.txt):
- RED 1: `FIG registry-rows-r56 recorded=88 derived=88 want=87 stale` + `FIGURE-AUDIT figures=35 ok=34 stale=1 exit=1`, `[exit=1]` — exactly 1 stale line, on registry-rows-r56, exit 1.
- RED 2: `FIG fail-entry-records recorded=33 (the class-check line; the trailer's 34 superseded) derived=34 want=33 stale` + summary ok=34 stale=1 exit=1, `[exit=1]` — exactly 1 stale line, on fail-entry-records, exit 1; derived=34 proves the derive reads the receipt bytes (mutation followed through).

E10. Do-nothing receipt (.ufo/waves/round-57/controls/do-nothing-c1-r57.txt, base eae1d61):
- `grep -c "\"id\"" ...` -> 27 at base; all eight planned ids -> 0 each; base audit `FIGURE-AUDIT figures=27 ok=26 stale=1 exit=1` with the stale exactly on fail-entry-records (derived=UNAVAILABLE reason=derive-exit-1) — equals the frozen before.

E11. Independent per-id check over the base blob:
- cmd: for each of the 8 ids, `git show eae1d61...:corpus/instruments/figure-audit-ledger.json | grep -c "<id>"`
- out: frontier-rows-r56 -> 0, registry-rows-r56 -> 0, entries-r56 -> 0, knowledge-expected-r56 -> 0, knowledge-files-r56 -> 0, census-fresh-literal-r56 -> 0, census-internal-r56-receipt -> 0, census-gone-r56-receipt -> 0. Working-tree ledger `grep -c '"id"'` -> 35; base -> 27 (27+8=35).

E12. New derives in printed receipts (clause 6):
- Green run over the lane root prints all eight with derived==recorded, none UNAVAILABLE: frontier-rows-r56 37, registry-rows-r56 88, entries-r56 40, knowledge-expected-r56 75, knowledge-files-r56 75, census-fresh-literal-r56 ok, census-internal-r56-receipt 1130, census-gone-r56-receipt 3915.
- Nuance: the committed controls receipts print derives for only 2 of the 8 (registry-rows-r56, fail-entry-records, via the red controls); the full 8-derivation printing receipt is produced over the final tree (my E7 run; gate-final reprints by design). No breach as measured.

E13. Amendment sentence present in the record cell (clause 7): "Amended round 57 (the run-15 host transition): ..." — present; accuracy checked line by line in E4.

E14. Tree state: `git status --porcelain` over ledger/controls/claims paths is empty — the 35-entry ledger, the round-57 controls and claims.json are committed at HEAD cd3029876eac7189aaff0d32b26031c0defa35aa; only .ufo/waves/round-57/w1/ (this wave's evidence) is untracked. The r53 receipt is single-touch since creation (E5).

E15. Convention check (repair reuses, does not invent): the base ledger's five r55 census figures already derive via `grep -oE ... .ufo/waves/round-55|56/controls/<receipt> | head|tail -1 | cut -d= -f2`, and the new r56 census-receipt entries use the identical shape. The repaired fail-entry-records derive is exactly the established receipt-figure pattern.

## Verdict line for C1

C1 SURVIVES — 8/8 kill-rule clauses PASS at measurement time; the derive repair is honest (amendment sentence accurate line by line), host-portable (POSIX text tools only, no counter re-run), and still binds its intended object in its only reproducible form (the committed r53 receipt); the frozen 33=entries−pass invariant does not survive the host transition as a live quantity (computes 0 here) and binds only as the pinned receipt figure. Residual (text-only, non-blocking): path-not-blob derive and non-line-anchored first-match grep (E5 Weaknesses 1–2).

## Suggested checks for the main agent

- gate-final: rerun the green audit + selftest at the truly final tree (clause 8 is time-scoped to my measurement).
- Consider (future round, no edit now): line-anchored or rev-pinned form for receipt-derived figures.

Scratch: /fast/scratch/hyaku/kasegi-r57/ReviewDerive deleted before yield; no leftovers.
