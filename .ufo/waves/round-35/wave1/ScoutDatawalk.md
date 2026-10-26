# ScoutDatawalk — round-35 wave 1 (leaf, planner data-walk ride)

Role: replay the frozen BEFORE values at freeze commit `617496b9c6e92bc671e7e78b83df69a04470d0e9`, check
claims.json predicate/counter agreement, and check kill-rule string identity against the wave context.
Advisory only; no round verdict, no lane commit. Replay window 2026-10-26 (~07:2x–07:4xZ).

- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base `3266c993…`; live HEAD at start `da2d3c68…` (worktree dirty from sibling seats; irrelevant to the freeze replay).
- Scratch: `/fast/scratch/hyaku/kasegi-r35/ScoutDatawalk/` — deleted before yield (`ls … | grep -c ScoutDatawalk` → 0).
- Tools installed/upgraded: none.

## Report

### 1. Export provenance

```
$ git archive 617496b9c6e92bc671e7e78b83df69a04470d0e9 | tar -x -C $S --one-top-level=freeze   # exit 0
$ git archive 617496b9… | git get-tar-commit-id
617496b9c6e92bc671e7e78b83df69a04470d0e9
```
All replays below ran with cwd = the extracted freeze tree (no git state, no untracked files), except census (reads the live lane's SOURCES.md; the file is unchanged for the checked rows — see §3).

Frozen control receipts unchanged in worktree (sha256):
```
fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982  .ufo/waves/round-35/claims.json
352d3da210283dc2d328b22ba27d9abd39eacc2f99ebcff2d4101532d582dd61  .ufo/waves/round-35/c1-controls/before.txt
2835700332ac682e25bd68523d7eb126b1e8980aca92144b9c9a63e37de77327  .ufo/waves/round-35/c2-controls/before.txt
74fc6a26d8d3ec9bc89903b410b828e82c8b35cc686fd7a586260aedec15867b  .ufo/waves/round-35/census-before.txt
```
(claims.json digest equals the one in `wave1/ExecBeforeReceipts.md` §2: no drift.)

### 2. C1 before-values (stored in `c1-controls/before.txt`) — all MATCH

| control | command (replayed in freeze tree) | stored | got | verdict |
|---|---|---|---|---|
| suite presence | `ls corpus/instruments/r35-defect-closure.sh; echo ls_exit=$?` | `ls_exit=2` | `ls: cannot access …: No such file or directory` / `ls_exit=2` | MATCH |
| D1 placeholder | `grep -c 'filled by the L1' SCORECARD.md` | 1 | 1 (line 1240) | MATCH |
| D1 tip hash | `grep -c 'c1c6a5f' SCORECARD.md` | 0 | 0 | MATCH |
| D2 stale | `grep -c '201\.7' SCORECARD.md` | 2 | 2 | MATCH |
| D2 corrected | `grep -c '201\.2' SCORECARD.md` | 0 | 0 | MATCH |
| D3 registry | `grep -cE 'r-defect-closure\|kill-rule-check' SKILL.md` | 0 | 0 (also 0 inside the `## Gates & probes registry` section only) | MATCH |
| D4 tracked | `git ls-tree -r --name-only 617496b9 -- .ufo/waves/round-34/wave1-results.json \| wc -l` | 0 | 0 | MATCH |
| D4 provenance | `find .ufo/waves/round-34 -maxdepth 2 -iname '*provenance*' \| wc -l` | 0 | 0 | MATCH |
| D5 erratum | `find . -name claims-erratum-d5.md \| wc -l` | 0 | 0 | MATCH |
| D6 dead-seat sentence | `grep -c 'did not file a receipt (dead seat' .ufo/waves/round-34/wave1/L1Integration.md` | 1 | 1 (`:30`) | MATCH |
| D7 | `grep -c 'supersedes-R22' corpus/QUALITY.md`; same for R23 | `0 0` | `0` `0` | MATCH |

Side observations on D4 (not a mismatch): the freeze tree export contains no `wave1-results.json` (`ls … 2>/dev/null | wc -l` → 0; an early variant with `2>&1` printed 1 only because it counted the `ls` error line — my own counting slip, corrected). In the live lane worktree the file is still untracked: `git status --short` shows `?? .ufo/waves/round-34/wave1-results.json` and `?? …wave1-results.json.provenance.md` (a sibling seat already wrote the note), and `git ls-files --error-unmatch …wave1-results.json` → `did not match any file(s) known to git` at HEAD `da2d3c68`. The D4 kill rule (untracked) is therefore still live until the L1 commits both files. Counter works post-commit: in this jj-colocated repo `git ls-files` sees jj-committed files (`git ls-files .ufo/waves/round-35/wave1-spec.json .ufo/waves/round-35/claims.json | wc -l` → 2).

D5/D6/D7 greps are anchored by text in `corpus/lessons/round-34-verifier-spotcheck.md:189-205` (§6): D5 junk-twin phrase has no discriminating invocation and "every assertion occurrences=1" is false for Q9/Q17; D6 `L1Integration.md:30` dead-seat sentence; D7 R22 cites M34-2 but grounding is M34-3, R23 grounded-in cites `considerthese/2026-10-25.md:76`.

### 3. C2 before-values (stored in `c2-controls/before.txt` / `census-before.txt`) — all MATCH

| control | command | stored | got | verdict |
|---|---|---|---|---|
| frontier admitted | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 17 | 17 | MATCH |
| registry rows | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 51 | 51 | MATCH |
| S052 rows | `grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md` | 0 | 0 | MATCH |
| entries citing S052 | `grep -lE '^source: S052 ' corpus/knowledge/*.md \| wc -l` | 0 | 0 (and `grep -rl S052 corpus` → 0) | MATCH |
| harness | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=20 pass=20 exit=0` | `entries=20 pass=20 exit=0`, harness_exit=0; last row `PASS F17 … immunefi-vscs-v2-2-smart-contract-severity.md ids=S051` | MATCH |
| source-recheck S052 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052` | `manifest UNAVAILABLE reason=missing` / `recheck_exit=2` | identical, recheck_exit=2 | MATCH |
| knowledge entries | `ls corpus/knowledge/*.md \| wc -l` | 46 | 46 (46 excl. README) | MATCH |
| census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `W04 S028`, `W04 S029`, `ok …SOURCES.md` | identical 3 lines, census_exit=0 | MATCH (live lane, not the freeze tree) |

### 4. claims.json predicate ↔ counter agreement

Replayed against freeze values: every counter in `counting_commands` evaluates to the stated BEFORE (C2: 17/51/0/0/20-20/exit 2) and none already holds its AFTER value, so no counter is vacuous at freeze **except** one kill-rule term (finding F-1).

Findings (advisory; claims.json is frozen — corrections would land as an appended erratum file):

- **F-1 `<LANE_HASH>` kill-rule term is vacuous at freeze.** C1 kill_rule: "`<LANE_HASH>` still present in SCORECARD.md". `grep -c 'LANE_HASH' SCORECARD.md` at freeze → 0, so that clause is satisfied before any work and cannot discriminate. The live D1 defect is the 'filled by the L1' placeholder (the kill rule also names it, and that clause is sound). No counting command reads `LANE_HASH`.
- **F-2 C1 counting_commands cover D1 and D4 only.** There is no counting command for D2 (`201.2`), D3 (SKILL registry), D5 (erratum present + the two statements), D6, D7. Those are carried only by the suite (`closed=7/7`). That is consistent with the predicate (the suite is the instrument) but means the five predicate items in the `after` list have no independent counter in claims.json; the suite's `--selftest` is the sole discriminator. Also `corpus/SOURCES.md -> 52` sits under C1's counters but belongs to C2 (cross-claim coupling: C1's counter set can fail on a C2 miss).
- **F-3 'filled by the L1' → 0 conflicts with append-only correction.** C1 after demands `grep -c 'filled by the L1' SCORECARD.md` → 0 *and* "appended correction naming c1c6a5f". SCORECARD is append-only by convention (`SCORECARD.md:148` "append-only errata"; QUALITY R-rows). The original placeholder is at `SCORECARD.md:1240` (`**Round-34 final lane commit: filled by the L1 in the closing commit.**`). Count 0 is only reachable if (a) that line is edited in place (a factual annotation edit, which SCORECARD.md:148 permits for "factual annotations" only) or (b) the appended correction never quotes the phrase **and** the original line is replaced. If the correction quotes the phrase to explain what it fixes, the count stays ≥ 1. The same tension exists for `201.7` (not claimed to go to 0: only `201.2` presence is checked, so no conflict there). The L1 should decide in-place vs. append before the suite encodes D1.
- **F-4 C2 junk-twin check repeats D5 class.** claims.json C2 predicate + `after[-1]` ("junk twin rejected: source-recheck exit != 0 and non-author reviewer REFUSE on record") name no discriminating invocation. `c2-controls/junk-f18.md` carries `recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052` — the same command the real entry will carry; once the real S052 manifest lands, that exits 0 on the twin too (exactly the round-34 D5 finding, `round-34-verifier-spotcheck.md:103-107`: "re-checks the real S051 manifest, not the twin's content"). The C2 kill rule "junk twin passes source-recheck" would then be spuriously triggered or spuriously untriggerable, depending on how the twin is invoked. A discriminating check needs the twin's own quotes tested against the S052 capture (e.g. `grep -c '<twin-distinctive-sentence>' corpus/source-snapshots/round-35/S052.txt` → 0).
- **F-5 "every assertion occurrences=1" repeated.** C2 predicate and `counting_commands[5]` repeat the phrase round-34 proved false for Q9/Q17 (`round-34-verifier-spotcheck.md:109`; `source-recheck.py:188` counts occurrences; `:192` only fails when `occurrences > 1` *and* the anchor verdict is not ok). For a one-entry S052 the claim is checkable, but the sentence is only true if every S052 quote is unique in the capture; the kill rule keys on exit status, not on `occurrences=1`, so the predicate is stricter than its kill rule.
- **F-6 Predicate ↔ kill-rule agreement otherwise holds.** C1: predicate `closed=7/7 exit=0` / `--selftest cases=7 failures=0` ↔ kill "`closed` != 7/7; fewer than 7 cases or any failure". C2: `frontier 18, rows 52, S052_row 1, entries 1, 21/21, recheck 0, census 0` ↔ kill "frontier_admitted != 18; registry rows != 52; S052_row != 1; entries citing S052 != 1; harness 21/21; recheck exit != 0; census exit != 0". Counters in claims.json match each term numerically (18/52/1/1/21-21/0/0). Knowledge entries 46→47 appears only in `after`, not in the kill rule (no counter reads 47).

### 5. Kill-rule string identity (claims.json vs wave context)

```
python3: wave1-spec.json['context'] has 4516 chars; contains 'kill rule': False, 'kill_rule': False
         (the only 'kill' substrings are inside 'skill').
         claims.json C1 kill_rule (390 chars) found verbatim in any of 391 spec strings: 0
         claims.json C2 kill_rule (222 chars) found verbatim in any of 391 spec strings: 0
         same two strings in wave1-dispatch.json / wave1-plan.out / build-spec.py: not present
```
Result: **the kill rules are NOT present in the wave context at all** — the context carries only the abbreviated "Frozen claims" bullets (C1/C2 predicate summaries). The kill rules exist only in `.ufo/waves/round-35/claims.json` (blob `0364c426ef605c88b7b9e7d32f1d6c846ede6fff`, 7112 B). Identity between claims.json and the wave context is therefore unprovable as asked (nothing to compare). The one-copy fact is the safe state — no divergent second copy exists — but a seat given only the wave context cannot see the kill rules (the abbreviated context also omits the `<LANE_HASH>` and "untracked" terms). Seats that need the kill rule must read `claims.json`; the L1 may wish to say so in the dispatch.

### 6. Verdict list (for the L1)

- Frozen BEFORE values: all 19 control rows (11 C1 table rows, 8 C2 table rows incl. census) reproduce exactly; **0 mismatches**.
- claims.json: counters ↔ predicate/kill numerically consistent (F-6); defects to note: F-1 (vacuous `<LANE_HASH>` clause), F-2 (D2/D3/D5/D6/D7 uncounted in claims.json), F-3 (count-0 vs append-only), F-4 (C2 junk-twin invocation non-discriminating — D5 recurrence), F-5 (occurrences=1 wording).
- Kill-rule identity: kill rules appear once only (claims.json); not in the wave context.
- Live-tree note: `wave1-results.json` and `wave1-results.json.provenance.md` are untracked at HEAD `da2d3c68`; C1's D4 kill clause stays open until committed.
