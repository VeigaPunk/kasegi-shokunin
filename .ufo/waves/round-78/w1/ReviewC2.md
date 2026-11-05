# ReviewC2 — round-78 w1 — surgical correctness review of the C2 landing set and entry draft (read-only)

Reviewer: ReviewC2-22 (leaf; no subagents; no git/jj writes; nothing edited outside `.ufo/waves/round-78/w1/`). Scratch `/fast/scratch/hyaku/kasegi-r78/ReviewC2` (deleted before yield; landing simulation built under git archive of freeze 2d81fe84506b323fb32beb137d5bd21db6a5c13d with the four c2/ files + entry overlaid). No tools installed.

Stable-state anchors (measured twice, 90–180 s apart after ScribeEntry finished):
- entry draft `c2/osv-post-batch-query-contract.md` sha256 `78cd76babc3589000f2c7fa9f71460b43eb271bc41f178d36daaa5c9b5a8d438`, 12,943 bytes, 92 lines, 1,816 words (matches ScribeEntry.md except its 91-line/12,893-byte stale count — final save happened after its receipt; trivial bookkeeping drift).
- prepared bytes: `c2/SOURCES.md` 205,413 B (7ab76a9b1718df0a…), `c2/knowledge-expected.txt` 4,830 B (86daa06ab4f101c2…), `c2/README.md` 133,516 B (24431ead3019ac7b…), `c2/PROVINCE.md` 33,605 B (357ce606225a22d6…).

```text
SEAT VERDICT: no blocker. The landing set is internally consistent and every B0–B7 check that is
measurable pre-integration holds on the prepared bytes + simulated landing (7 re-run commands, rc 0
each). Two residual notes routed to the L1: (N1) the S112 registry anchor cell still cites the
round-77 snapshot paths; (N2) the entry presents the 1,000/3,000 thresholds as crisp counts while
the page's own qualifier S112.txt:170 is deliberately unclaimed (Critic objection 4 stands).
```

## Check walk (per-seat items (a)–(g))

**(a) Every quote verbatim at its declared line — RUN, PASS.**
- Manifest: my independent whitespace-collapsed, per-actual-line check for all seven quotes (not the instrument's ±3-line window):

```text
$ python3 (per-line substring, normalize = collapse runs of whitespace)
Q01@24=1 Q02@24=1 Q03@24=1 (line 24 carries all three verbatim)
Q09@166=1 Q10@168=1 Q11@169=1 Q13@195=1  → all 7/7 in-line verbatim at exactly the declared line
```
- This is stronger than B0/B5's `anchor=<n>-ok` (instrument joins a 4-line window): every quote sits on its declared line itself, so the r77 anchor-drift class (declared :30/:31 vs actual :31/:32) does not recur.
- Entry: all ten `"… "<S112.txt:N>` quote instances extracted and matched against the snapshot: 10/10 `VERBATIM` (Q01–Q03 repeated in Attribution + Gate table). No mistyped or re-fabricated quote found.

**(b) Claims exactly the seven clauses — PASS.**
- Zero occurrences of the tokens Q04–Q12 in the entry (`grep -n "Q0[4-8]|Q12"` → rc 1).
- The six dropped clauses appear ONLY in the `## Not claimed` line (entry line 61): parameters pointer S112.txt:31, instructions pointer S112.txt:32, item-rules pointer S112.txt:34, version rule :35, 400 consequence :36, threading-variance note :170 — each line number verified against the snapshot (line 31/32/34/35/36/170 hold exactly those sentences), and each is named as not claimed with the F51 cross-reference `osv-post-v1-query-contract.md:21`/`:47` and `S108.txt:40,41,136` (all three S108 lines verified verbatim in the round-73 capture). No claim sentence anywhere in the entry rests on those six lines. The two located-but-unpinned sentences the entry does cite as context (:167 via Limits? — actually :167 is not cited; :194 :22 are) are named "no manifest quote pins it, grounds no clause" (entry :88), which is the correct unclaimed treatment.
- Claim-body sentence audit: the five Claims' falsifiable rules all cite only S112.txt:24/:166/:168/:169/:195. No leaked claim of dropped ground.

**(c) Gate quotes ≤ 25 words — PASS.**
- Measured per table cell with `wc -w` on the extracted quote text: claimed counts 15/7/10/18/11/9/20 vs measured 15/7/10/18/11/9/20 — all match, max 20 ≤ 25 (R56-conformant, counts measured not hand-typed).

**(d) No literal or escaped pipe in any table cell — PASS.**
- Programmatic per-cell scan over all 9 table lines (Gate table + separators): 0 cells contain `|`
- `grep -nP '\\\\\|'` over the entry: no match (rc 1). The only free `|` in the file is inside a backticked command in Distinctness (line 56, not a table cell, shell syntax).

**(e) S112 registry change is exactly one row — PASS.**
- c2/SOURCES.md vs `git archive 0687cca8`: whole-file row diff = one `replace` block at line 124; cell-level: only cell7 `queued`→`mined` and cell10 `—`→`corpus/knowledge/osv-post-batch-query-contract.md`; all 11 cells otherwise byte-identical.
- S-row count `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` = 112 before and after. Zero added/removed rows.
- B1 wording says used-by "names the entry" — satisfied. The seat-spec literal `osv-post-batch-query-contract.md (F54)` was deliberately NOT used; ExecC2Build documents why (census E11 requires an existing path; `(F54)` form deterministically breaks frozen B7). Deviation justified and evidence-backed; the used-by names the entry.

**(f) knowledge-expected.txt and README/PROVINCE rows match the new entry — PASS.**
- expected: +1 line `corpus/knowledge/osv-post-batch-query-contract.md` (94 lines / 92 `.md` rows), `grep '\.md$' | LC_ALL=C sort -c` rc 0, file order == C-sort order, placed between `osv-affected-range-events.md` and `osv-post-v1-query-contract.md`; row set == `corpus/knowledge/` listing on the simulated landing (92 == 92, set-equal). Naming matches the landing filename exactly.
- README prepared change = append-only +14 lines (`1189a1190,1203` in diff): R6 intro, one coverage-map row, one `| F54 |` frontier row, one `[r78 amendment …]` line. F54 row: `admitted | knowledge/osv-post-batch-query-contract.md | S112 | <next>` — parses under FRONTIER_ROW/FRONTIER_SOURCES (verified by the B3 run below); topic cell equals the entry's seven-clause subject; the "next" cell repeats the entry's own scope limit.
  - Note: ExecC2Build.md says "+9 lines"; the diff adds 14 (its count evidently excluded blank/header/separator lines). Receipt-number drift only; the bytes are correct.
- PROVINCE prepared change = +1 end-of-file `[r78 Frontier amendment …]` line naming F54/S112/the entry with the seven-clause scope and the six exclusions — consistent with README and claims.

**(g) Recheck line runs from a scratch copy only — PASS.**
- Ran the exact recheck command's instrument side against a scratch copy of the round-78 snapshot dir, and the full simulated-landing variants (below). Also on the simulated landing: `source-recheck.py --manifest corpus/source-snapshots/round-78/manifest.json --source S112` → `S112:sha256 OK` + 7×`OK occurrences=1 anchor=<n>-ok`, rc 0 — byte-for-byte the shape of controls/c2-prerecheck-r78.txt.

## Simulated-landing predicate runs (prepared bytes + entry, over git-archive of the freeze)

| # | command (cwd = landing export) | output | rc |
|---|---|---|---|
| B3 | `python3 corpus/instruments/frontier-recheck-count.py` | `FRONTIER-CENSUS rows=54 admitted=54 closed=54 problem-rows=0 registry=112` … `FRONTIER-PASS F54 ids=S112` … `PASS F54 knowledge/osv-post-batch-query-contract.md ids=S112 exit=0`, `entries=57 pass=57 exit=0` | 0 |
| B4 | `python3 corpus/instruments/capture-binding-check.py` | `MANIFEST round-78 records=1 url_bound=1 fetched=1 archival=0`, `AUDIT records=92 … unbound=0`, `records=92 bound=92 unbound=0` | 0 |
| B5 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-78/manifest.json --source S112` | `S112:sha256 OK` + 7 anchored OK | 0 |
| B2 | `ls corpus/knowledge/*.md \| wc -l` / `wc -l knowledge-expected.txt` / `grep -cE '\.md$'` / sort -c | 92 / 94 / 92 / rc 0; set-equal to directory | 0 |
| B1 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 112 | 0 |
| B6 | `grep -F -l '<q>' corpus/knowledge/*.md` per quote, excluding the new entry (both real tree, 91 files, and landing copy, 92 files) | zero files matched for all seven quotes | 1 per grep (= absence) |
| B7* | `bash scripts/sources-census.sh validate <landing-dir>` (explicit-dir form; see B7 verdict note) | 6×W04 (S028 S029 S072 S076 S080 S085) + `ok …/corpus/SOURCES.md` | 0 |
| extra | `python3 corpus/instruments/recheck-audit.py --root <landing> --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin` | `strict pass=92/92 cdroot_fail=0`, `lines=92 … pass=92 … exit=0`, `expect=present expected=92 missing=0 unexpected=0` | 0 |
| extra | `python3 corpus/instruments/anchorcheck.py c2/osv-post-batch-query-contract.md` | `10 in-range cite instances, 0 bad; 9 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` | 0 |

B6 cross-check on the real freeze tree (91 admitted files, `grep -F -l` per quote, excluding nothing yet — none of the seven quotes exists anywhere in corpus/knowledge/): 0 hits, so absence is not an artifact of the exclusion filter.

## Findings

1. **NOTE — SOURCES.md:124 anchor cell cites round-77 artifacts, not the round-78 manifest (pre-existing drift, carried into the prepared bytes).** The frozen row's anchor cell names `corpus/source-snapshots/round-77/S112.txt` "13 pinned quotes in corpus/source-snapshots/round-77/manifest.json"; the claim-bearing pin is `round-78/manifest.json` (7 quotes). Both files exist post-landing (verified on the export) and the two S112.txt copies are sha-identical (`f3ca0465…0907`), so nothing dangles; B1 permits only the two cell changes, so the cell was correctly left byte-identical. Routing: L1 awareness, already flagged by ExecC2Build (its drift 1) — I confirm it reproduces on the prepared bytes (`grep -o 'corpus/source-snapshots/round-77/[A-Za-z0-9_.]*'` → 2 hits at line 124).

2. **NOTE — thresholds entered without the page's own qualifier (Critic objection 4 stands; claim-design residual, not an entry defect).** Claim 4 (entry :37-41) states the 1,000/3,000 counts as the page's stated trigger set with a falsifiable rule inviting the reader to treat them as boundaries, but S112.txt:170 ("These numbers can vary slightly because of threading and the page size may change in the future.") is only in the Not-claimed line — never cited as the reason the counts are not hard limits. The frozen claim deliberately leaves Q12 unclaimed, so the entry is conformant to the claim; but the scout (ScoutDistinct.md §3.2) named this exact hazard and the entry does not neutralize it. Smallest L1-side fix within the frozen claim: one rejected-over-generalization sentence in Claim 4 citing S112.txt:170 as located-not-pinned (the same treatment the entry already gives :194 in Limits). No quote or predicate edit.

3. **NOTE — B7's literal command shape needs the fleet conf; the explicit-dir equivalent passes.** Predicate text: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`. Run with `--root` pointing at a scratch export, the script dies with `ERROR: config not found …/shokunin.conf` (rc 0 + error lines; no lane assessed). Equivalent explicit-lane-dir form `bash scripts/sources-census.sh validate <landing-corpus-root>` rc 0 with exactly the six inherited W04 warnings and no new finding, on both the simulated landing and the real lane tree. B7's substance (validate clean + six W04 allowed) holds; the conf-dependent literal invocation should be re-run by the L1 at the landing commit where the conf lookup targets the real fleet root.

4. **NOTE — small bookkeeping drifts in the wave-dir receipts.** (i) ScribeEntry.md records the draft at 12,893 B / 91 lines; the final saved bytes are 12,943 B / 92 lines (the scribe's own last save post-dates its report). (ii) ExecC2Build.md's README diff "+9 lines" undercounts the actual +14 added lines. Neither affects the landing bytes; both are numeric-accuracy noise under QUALITY Q3/R56 discipline.

5. **NOTE (crosswalk, out of my scope) — CriticClaims objections 3 and 5 touch C2 and remain open.** Nothing in B0–B7 pins the entry's claimed-clause set (objection 3), and the do-nothing control c2-donothing-counters-r78.txt is a filtered excerpt without the FRONTIER-CENSUS line it is cited for (objection 5). I verified the substance of both independently: the entry's only claimed clauses are the seven (my (b) check), and the FRONTIER-CENSUS before-state is real (re-ran: rows=53 admitted=53 registry=112). Routing already done by the critic; no new defect.

## Verdict per predicate B0–B7

| predicate | verdict | evidence |
|---|---|---|
| B0 | holds | control receipt committed at freeze (c2-prerecheck-r78.txt: sha256 OK + 7×`anchor=<n>-ok`, rc 0); my independent 7/7 exact-line check; my re-run reproduces shape and rc |
| B1 | holds | one-row one-line diff; cell-level queued→mined + used-by→entry path; S-rows 112 before/after; zero add/remove |
| B2 | holds | 94 lines / 92 `.md` rows; LC_ALL=C sort -c clean; row set == directory listing (92==92) on the simulated landing |
| B3 | holds | FRONTIER-CENSUS rows=54 admitted=54 closed=54 problem-rows=0 registry=112 + `FRONTIER-PASS F54 ids=S112`, rc 0, on the simulated landing (full run incl. `entries=57 pass=57 exit=0`) |
| B4 | holds | capture-binding-check rc 0, `records=92 bound=92 unbound=0`, MANIFEST round-78 line present at freeze; the freeze commit carries capture+manifest+claims |
| B5 | holds | re-run at simulated landing: sha256 OK + 7 anchored OK, rc 0 |
| B6 | holds (literal half measured; paraphrase half recorded) | 0/7 quote-absence hits over 91 admitted entries (real tree) and 92 (landing); per-clause sweep verdicts recorded in lesson-round-78.md via ScoutDistinct (3 NOVEL / 4 PARTLY-HELD / 0 HELD; I spot-checked the sweep's F51:47/:75 and F31:23 anchors — all resolve) |
| B7 | holds (equivalent command) | explicit-dir validate rc 0 with exactly the six allowed W04 warnings on the simulated landing and the real lane; the conf-dependent literal `--root /home/vgpnk/Projects/shokunin kasegi` shape needs a real-root conf lookup — re-run at landing by L1 (Finding 3) |

Not checked by this seat (owned elsewhere): the entry-prose clause-set enforcement predicate (Critic objection 3 — none exists), C1 P1–P7 (ReviewC1/MutC1 scope — their verdicts, including the K-X2 survivor blocker, are recorded in their own reports), and any live re-open of the URL (Critic did it 2026-11-05, HTTP 200).

## Files written

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-78/w1/ReviewC2.md` (this report — the only file this seat wrote).
