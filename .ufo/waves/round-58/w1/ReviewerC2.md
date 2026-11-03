VERDICT: PASS for C2 at 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b. All 9 after-state counting commands reproduce the claimed values in a fresh clone of the commit (0 mismatches). Pure-append holds for README, PROVINCE, SOURCES (no pre-existing line deleted or changed) and the expected list (one sorted insert). No kill-rule clause fires. Findings are non-blocking: (a) the lead line is at corpus/SOURCES.md:142 at 18ddb05, not :141 as the frozen sentence says (bytes identical; base was :141); (b) the S091 registry row's line map omits L22-L23, which README F39 cites (S091.txt:23, Q4). R67 stub probe: admitted, FRONTIER-PASS F39 ids=S091, exit 0 (expected; counter not changed).

Scope: claim C2 only (frozen claims.json, id C2), plus the registry, README, PROVINCE and expected-list bytes at 18ddb05. C1 is not reviewed here.
Lane HEAD: 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b (verified). Freeze commit: 543cac13886b91ac660d788ed20e64ae70ee0fa5 (cat-file -t = commit).
Scratch: /fast/scratch/hyaku/kasegi-r58/ReviewerC2 (clone/, stub/, basetree/, base-*.md, new-*.md, d.*.txt); deleted before yield.
No tools installed or upgraded. No credential material written. Nothing committed to, or written into, L other than this file.
Working-tree note (not in the commit under test, not reviewed): `git -C L status --short` shows uncommitted modifications to LOG.md, SCORECARD.md, corpus/QUALITY.md and untracked round-58 receipts (incl. controls/after-r58.txt, which I read as the printed-value receipt only).

## 1. Clone at the implementation commit
$ D=/fast/scratch/hyaku/kasegi-r58/ReviewerC2; git clone -q --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin $D/clone && git -C $D/clone rev-parse --show-toplevel && git -C $D/clone rev-parse HEAD
/fast/scratch/hyaku/kasegi-r58/ReviewerC2/clone
18ddb054a82a59e530ba86b2511bcfa5ecd49b6b
[exit=0]

## 2. Per-number match table (after field of C2; counting commands run in the clone, cwd = clone)
Receipt values in controls/after-r58.txt match the re-derived values in every row.

| # | claimed (after) | command | re-derived | result |
|---|---|---|---|---|
| N1 | FRONTIER-CENSUS rows=39 admitted=39 closed=39 problem-rows=0 registry=91 | `python3 corpus/instruments/frontier-recheck-count.py > fc.txt; echo $?` | `FRONTIER-CENSUS rows=39 admitted=39 closed=39 problem-rows=0 registry=91` | MATCH (exit 0) |
| N2 | FRONTIER-PASS F39 ids=S091 | same, grep `FRONTIER-PASS F39` | `FRONTIER-PASS F39 ids=S091` (line 83 of 83-line output) | MATCH |
| N3 | entries=42 pass=42 exit=0 | same, grep `entries=` | `entries=42 pass=42 exit=0` | MATCH |
| N4 | source-recheck S091: sha256 OK, 9 Q OK occurrences=1, exit 0 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-58/manifest.json --source S091` | `S091:sha256 OK`; `S091:Q1..Q9 OK occurrences=1` (anchors 1,14,21,23,25,30,34,45,14) | MATCH (exit 0) |
| N5 | capture-binding records=74 bound=74 unbound=0 exit 0 | `python3 corpus/instruments/capture-binding-check.py \| tail -2; echo ${PIPESTATUS[0]}` | `records=74 bound=74 unbound=0`; exit 0 | MATCH |
| N6 | ls corpus/knowledge/*.md \| wc -l = 77 | `ls corpus/knowledge/*.md \| wc -l` | 77 | MATCH |
| N7 | knowledge-expected entries = 77 | `grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt` | 77 (file has 79 lines: 2 header comments + 77 entries) | MATCH |
| N8 | LC_ALL=C sort -c exits 0 | `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt; echo $?` | exit 0 | MATCH |
| N9 | grep -cE '^\| F39 ' corpus/README.md = 1 | `grep -cE '^\| F39 ' corpus/README.md` | 1 (README.md:964) | MATCH |
| N10 | lead-line sha 631364e0dd3447d6a9bc56830dfc2da26600c5e6cfca054b2b9c3f8cf3627547 | `grep 'rate of autonomous AI cyber-capability progress' corpus/SOURCES.md \| sha256sum` | 631364e0dd3447d6a9bc56830dfc2da26600c5e6cfca054b2b9c3f8cf3627547 (line is SOURCES.md:142 at 18ddb05; :141 at base) | MATCH (sha); pointer drift, see F1 |
| N11 | registry rows = 91 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 91 (base 90) | MATCH |
| N12 | census validate exits 0 (W04 only, pre-existing) | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md; echo $?` | `file ok .../corpus/SOURCES.md`; exit 0; 6 W04 lines: S028 S029 S072 S076 S080 S085 | MATCH |
| N13 | S091.txt sha256 d2ba7199faf44fb9f5fc5c48924f20d72ed08959c511af58cb9c1322f9820618 (kill-rule value) | `sha256sum corpus/source-snapshots/round-58/S091.txt` | d2ba7199faf44fb9f5fc5c48924f20d72ed08959c511af58cb9c1322f9820618 (11660 bytes, 67 lines) | MATCH |

Baseline cross-check (freeze commit export, `git -C L archive 543cac1 \| tar -x -C basetree`):
$ python3 basetree/corpus/instruments/frontier-recheck-count.py --root basetree | grep -E 'FRONTIER-CENSUS|entries='
FRONTIER-CENSUS rows=38 admitted=38 closed=38 problem-rows=0 registry=90
entries=41 pass=41 exit=0   (base-counter-exit=0)
knowledge-expected base count: 76; knowledge files base: 76. Matches the before field.

## 3. Pure-append diffs (freeze 543cac1 vs implementation 18ddb05)
Command pattern: `git -C L show 543cac1…:<f> > base.<f>; git -C L show 18ddb05…:<f> > new.<f>; diff base.<f> new.<f>`

- corpus/README.md: base 948 lines, new 968. diff: `948a949,968`, exit 1. 20 inserted, 0 changed, 0 deleted. Pure append (R6 amendment block, F39 rows at README.md:964). PASS.
- PROVINCE.md: base 203, new 205. diff: `203a204,205`. 2 inserted, 0 changed, 0 deleted. Pure append. PASS.
- corpus/SOURCES.md: base 212, new 215. diff: `97a98` and `212a214,215`. 3 inserted, 0 changed, 0 deleted.
  - Exactly one table row inserted: SOURCES.md:98, `| S091 | UK AI Security Institute, How fast is autonomous AI cyber capability advancing? ...`, 12 pipes (same as S090 row).
  - Appended lines 214 (blank) and 215 (`- S091 row added (round 58): ...` bullet in the changelog section).
  - Lead line: base SOURCES.md:141 = new SOURCES.md:142 (shifted down by the row insert). `grep 'rate of autonomous AI cyber-capability progress' … \| sha256sum` = 631364e0dd3447d6a9bc56830dfc2da26600c5e6cfca054b2b9c3f8cf3627547 on base AND new. The exact line sha256 for line 141 base = 631364e0…; the new line-142 bytes are identical (grep-sha match). PASS.
- corpus/instruments/knowledge-expected.txt: base 78 lines, new 79. diff: `3a4`, exit 1. One line inserted: `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md` (new line 4). 0 changed, 0 deleted.
  - `LC_ALL=C sort -c` on new: exit 0 (sort-ok). On base: exit 0. PASS.

## 4. Kill-rule walk (C2 kill_rule, claims.json; each clause against committed bytes at 18ddb05)
C2 is not killed. Clause by clause:
1. final counter lacks `FRONTIER-PASS F39 ids=S091` -> present (N2). Not fired.
2. rows != 39 / admitted != 39 / closed != 39 -> 39/39/39 (N1). Not fired.
3. registry != 91 -> 91 (N1, N11). Not fired.
4. entries != 42 or pass != 42 -> 42/42 (N3). Not fired.
5. counter exit nonzero -> exit 0 (N3). Not fired.
6. source-recheck --source S091 exits nonzero -> exit 0 (N4). Not fired.
7. any Q line lacks occurrences=1 -> all nine Q lines show occurrences=1 (N4). Not fired.
8. capture-binding-check exits nonzero -> exit 0 (N5). Not fired.
9. capture-binding records != 74 or bound != 74 -> 74/74, unbound=0 (N5). Not fired.
10. sha256 of S091.txt != d2ba7199… -> equal (N13). Not fired.
11. knowledge-expected not LC_ALL=C sorted -> sort -c exit 0 (N8). Not fired.
12. knowledge-expected count != knowledge file count -> 77 = 77 (N6, N7). Not fired.
13. lead-line sha != 631364e0… -> equal (N10). Not fired.
14. any pre-existing README/PROVINCE/SOURCES line changed (deletion or in-place modification) -> diff shows 0 `<` lines in all three (section 3). Not fired.
15. census validate nonzero -> exit 0 (N12). Not fired.
16. entry's recheck line not a source-recheck invocation for S091 -> knowledge file line 6: `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-58/manifest.json --source S091`. Satisfies. Not fired.

Command for the knowledge-file check: `grep -n '^recheck:' corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md`

## 5. R67 stub probe (counter not changed; result reported only)
Procedure: `git clone -q --shared L $D/stub`; replaced corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md with its first 7 lines plus one stub line `stub: S091 only` (8 lines, `git diff --stat`: 1 insertion, 76 deletions); `python3 corpus/instruments/frontier-recheck-count.py --root $D/stub > probe.txt; echo $?`
$ python3 corpus/instruments/frontier-recheck-count.py --root <stub>
FRONTIER-CENSUS rows=39 admitted=39 closed=39 problem-rows=0 registry=91
FRONTIER-PASS F39 ids=S091
PASS     F39  knowledge/aisi-autonomous-cyber-capability-progress-rate.md ids=S091           exit=0
entries=42 pass=42 exit=0
probe-exit=0
Control (unmodified clone, same flag): identical lines, control-exit=0.
Result: the frozen counter admits the stub body, as R67 predicts. The stub limb is not claimed by this round and is not fixed here.

## 6. F39 README row binding to the registry
README.md:964 cells: `| F39 | <topic> | admitted | knowledge/aisi-autonomous-cyber-capability-progress-rate.md | S091 | <next> |`. The sources cell is exactly `S091`.
Registry row SOURCES.md:98 (12 pipes): id S091; kind docs; tier A; status mined; opened 2026-11-03; recheck 90d; used-by corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md; capture corpus/source-snapshots/round-58/S091.txt.
Manifest corpus/source-snapshots/round-58/manifest.json: S091 sha256 d2ba7199…820618, bytes 11660, lines 67, status 200. File on disk: same sha, 11660 bytes, 67 lines.
Content check (S091.txt read at clone path): L14 (4.7 months; 8 months, Nov 2025), L19-L21 (narrow suite, expert baselines, 80%, 2.5M tokens), L23 (`an imperfect model, and is not a future prediction, nor a fixed law`), L25 (doubling 4.7), L30 (4.1 to 5.0 months), L34 (6 of 10 `The Last Ones`; 3 of 10 `Cooling Tower`). All values in the frozen sentence are present in the capture.
Binding verdict: the README row binds to the registry row via the same id and the same sha. PASS.

Findings (non-blocking; no change made):
- F1 (pointer drift): claims.json C2 frozen sentence says the lead line is corpus/SOURCES.md:141. At 18ddb05 it is :142 because the S091 row was inserted above it (SOURCES.md:98). Bytes are unchanged (sha matches). Correction text only: "corpus/SOURCES.md:142 at 18ddb05 (was :141 at freeze)".
- F2 (registry line map incomplete): SOURCES.md:98 capture cell lists title L1, date L13, estimate L14, method L19-L21, doubling L25, uncertainty L28-L30, cyber ranges L33-L35, publisher L45. It omits L22-L23, where the README F39 row quotes `S091.txt:23` (Q4, anchor 23-ok in N4). The binding holds through the pinned anchor; the row's line map is just incomplete. Correction text only.
- F3: the registry row is inserted mid-table (SOURCES.md:98), not appended. The kill rule allows one row insert, so this is not a violation.

## 7. Commands and exit codes (summary)
- `git rev-parse HEAD` (L) -> 18ddb05, exit 0.
- `git -C L status --short` -> exit 0 (working-tree notes above).
- `git -C L show <freeze>:<f>` and `<impl>:<f>` for README, PROVINCE, SOURCES, knowledge-expected -> exit 0 each.
- `diff` (4 files) -> exit 1 each (expected for an insert), 0 `<` lines each.
- `LC_ALL=C sort -c` new and base knowledge-expected -> exit 0 both.
- `frontier-recheck-count.py` (clone) -> exit 0; (basetree) -> exit 0; (stub) -> exit 0; (control clone) -> exit 0.
- `source-recheck.py --source S091` -> exit 0.
- `capture-binding-check.py` -> exit 0.
- `sources-census.sh validate --file corpus/SOURCES.md` -> exit 0 in clone (6 W04). Base copy validated in the clone with the same six W04 ids, exit 0. (An earlier run from outside the clone reported `E11 missing used-by` lines and exit 1; that was a cwd/path artifact, not a lane fact, and is not used here.)
- `sha256sum` of S091.txt, lead line, manifest.json -> values as above.
- `grep -cE`, `grep -c`, `ls | wc -l`, `wc -l` -> as above.

Tools installed or upgraded: none. Scratch removed on exit.
