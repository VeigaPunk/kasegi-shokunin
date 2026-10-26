# ScoutR37Evidence — round-37 evidence map for the round-38 C1 corrections (receipt only)

Seat: ScoutR37Evidence (scout, leaf). Judged on depth:verifiability. Read-only: every fact below was read from
git objects (`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show|log|ls-tree|diff <ref>:<path>`), the
fleet report/watchdog (read-only), or a scratch extraction that is deleted at yield. Deliverable: this pointer
table only (no landable bytes). Lane HEAD at read time `700153593eb586c70a6499c8ca225ee4d673bc9b`
(round-38 spec+dispatch); `git status --short` showed only untracked `.ufo/waves/round-38/wave1*`.

Notation: `T` = `83975acc` (r37 lane tip, `83975acc…4`), `A` = `2387dcf6` (r37 judged head), `B` = `b56a416` (r37 base).
`path:N` = line N of that path at T unless a ref prefix is given. No tool installed; no network used.

## 1. Commits B..T (`git log --name-status b56a416..83975acc`), 10 commits, newest first

| # | hash | committer date (-0300) | subject | changed files |
|---|---|---|---|---|
| 1 | 83975acc | 2026-10-26 15:03:15 | round-37: WAVE-DONE results — kasegi-r37-build-results.json (64/64 settled) | A `.ufo/waves/round-37/kasegi-r37-build-results.json` |
| 2 | 2387dcf6 | 15:01:28 | round-37: F3 final head — bind final lane hash in SHONEN/SCORECARD | M SCORECARD.md (:1505), M SHONEN.md (:172, :176) |
| 3 | aa88877b | 15:00:25 | round-37: F2 final head — genuine all-gates transcript of the F1 run | M `.ufo/waves/round-37/final-gates/all-gates.txt` (7+/7-) |
| 4 | 9492c776 | 14:59:49 | round-37: F1 bootstrap receipt (disclosed token edits: E10 green + summaries + selftest case) | A final-gates/all-gates.txt |
| 5 | 2735e93f | 14:58:51 | round-37: late seat receipt — MutC1Fixtures | A wave1/MutC1Fixtures.md |
| 6 | a4b6a8ca | 14:50:01 | round-37: F0b fix — restore LOG/lesson round-37 headings | M LOG.md, M corpus/lessons/round-37.md |
| 7 | 0acffc82 | 14:48:42 | round-37: F0 integration — suite/entry/S054 row+capture/QUALITY R30-R31/ledger/README-PROVINCE/LOG-SCORECARD-SHONEN/lesson/junk control/wave receipts | 117 paths: 64 round-37 wave1 receipts (A), assimilation/*, wave1.ready*, wave1-plan/run.err, swarm-registry.json; M LOG.md PROVINCE.md SCORECARD.md SHONEN.md SKILL.md corpus/README.md corpus/QUALITY.md corpus/SOURCES.md corpus/instruments/knowledge-expected.txt corpus/knowledge/considerthese-proposals-ledger.md; A corpus/instruments/r37-closure.sh, corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md, corpus/lessons/round-37.md, corpus/source-snapshots/round-37/{S054.txt,manifest.json}, c2-controls/junk-f20.md; M round-36 wave1/ScribeConsiderthese.md |
| 8 | b3620681 | 14:00:19 | round-37: claims-erratum-1 (S054 capture URL -> SSVC overview tutorial page), filed before any seat scored | A .ufo/waves/round-37/claims-erratum-1.md |
| 9 | f3246559 | 13:59:17 | round-37: wave evidence — spec/plan/dispatch (kasegi-r37-build, 64 seats v2) | A wave1-dispatch.json, wave1-plan.out, wave1-spec.json |
| 10 | 224df74d | 13:57:07 | round-37: claims freeze + before controls (C1 r37-closure suite closing D1-D6; C2 F20 SSVC) | A c1-controls/before.txt, c2-controls/before.txt, census-before.txt, claims.json |

(`git log b56a416..83975acc --oneline | wc -l` → 10; commit 7, 0acffc82, is the only one that touched PROVINCE.md, corpus/README.md and the ledger.)
`git log -1 --format=%ci a173b0c` = 2026-10-26 15:10:30 -0300 (the round-37 spot-check commit; base of round 38).
Between T and the round-38 base: a173b0c adds corpus/lessons/round-37-verifier-spotcheck.md only (it is the §5 source).

## 2. Closure-order timing (D3): `complete kasegi round=37` vs commit 83975acc

| event | timestamp (-03:00) | pointer |
|---|---|---|
| launch kasegi round=37 | 2026-10-26T13:52:56 | `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1533` |
| lane commit 2387dcf6 (A, judged head) | 15:01:28 | `git log -1 --format=%ci 2387dcf6` |
| fleet report filed (3aa4ed4d, fleet repo) | 15:02:03 | `git -C /home/vgpnk/Projects/shokunin log -1 --format=%ci 3aa4ed4d` → `.ufo/reports/round-37/kasegi.md` |
| **complete kasegi round=37; hyaku-inline attempt=1** | **15:02:47** | `watchdog.log:1537` (re-read now: lines 1533/1537 unchanged from the spot-check's digest) |
| **lane commit 83975acc (T)** | **15:03:15** | author = committer date; **+28 s after `complete`** |
| report WAVE-DONE addendum (c6635628, fleet) | 15:03:45 | report line 88, file mtime 15:03:44.97 |
| launch kasegi round=38 | 15:11:39 | `watchdog.log` (line after 1537: kaidoku r40 launch 15:06:51, kengaku complete 15:07:58) |

Findings: T (83975acc) is the only lane commit after `complete`; it adds one file (`kasegi-r37-build-results.json`,
dict `{lane,round:37,wave:"kasegi-r37-build",seats:64,results:64}`, 392 lines added per spot-check line 10).
The report discloses this at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-37/kasegi.md:88` ("a post-measurement lane commit … the earlier 'not finalised' note is superseded"), yet report line 41 still says "after: all six routed defects closed" (D3 was one of the six per spot-check §5, no E-check covers it).
`watchdog.log` is mutable: cite line numbers with the quoted text, as the spot-check does (spot-check lines 12-16).
Note for G4 (D3 closure check): round-37 had `wave1-dispatch.json` (`counts.spawn=64`, `taskCall.tasks` len 64; no top-level seat field) and the tracked `.ufo/waves/round-37/kasegi-r37-build-results.json` (`seats:64`, `results:64`). The names do NOT pair as `*-dispatch.json` ↔ `*-results.json` by prefix (r35 used `wave1-results.json`; r36/r37 used `kasegi-r<N>-build-results.json`; r35 also has `wave1-results.json.provenance.md`). Round 38 dispatch: `.ufo/waves/round-38/wave1-dispatch.json` `counts.spawn=73 total=73`, `taskCall.tasks` len 73, wave `kasegi-r38-build`; no results file is tracked yet (expected result name by precedent `.ufo/waves/round-38/kasegi-r38-build-results.json`).

## 3. Pointer table: round-37 claim → committed evidence

### 3.1 D-A — scaffolding in front-door files (verified by byte arithmetic, not assumed)

Method: `git show b56a416:<f>` is a byte prefix of `git show 83975acc:<f>` (`cmp` prefix check passed for both files); the tail is the r37 append.

| claim / fact | path:line at T | evidence |
|---|---|---|
| PROVINCE.md base 78 lines (4954 B) → T 152 lines; append = 74 lines / 5940 B | PROVINCE.md:79-152 | `wc -lc` of append tail: `74 5940` |
| Declared block A is present first: lines 79 (blank) + 80 (`[r37 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F20 — SSVC …`) | PROVINCE.md:79-80 | `head -c 295 append | sha256sum` = `cdfe44e319094957ec583b7c3cd8212b882752b75682d9f1cf4d0b734f20f545` (equals declared sha; 295 B / 2 lines) |
| Misplaced scaffolding (not part of declared block) | **PROVINCE.md:81-152** (spot-check says 80-152; byte test shows 80 is the legitimate F20 line) | stray fences at :81, :96 (` ```text`), :124 (3 = odd/unbalanced); `## 3. Deliverable B — corpus/README.md end-of-file block` :90; duplicated `## Round-37 admission …` text :97; `## 4. Validation on a scratch mirror (append, not edit)` :134 |
| README base 398 lines (`git show b56a416:corpus/README.md`) → T 454 lines; append = 56 lines / 4748 B | corpus/README.md:399-454 | same prefix test; `wc -lc` → `56 4748` |
| Declared block B is NOT intact: lines 399-400 are blank where the declared first lines `## Round-37 admission — coverage map row and Frontier F20 (appended 2026-10-26)` + blank should be; body 401-424 and the final blank 425 present (27 lines = 399-425) | corpus/README.md:399-425 | `grep -c '^## Round-37 admission' corpus/README.md` → 0 at T; declared sha `2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b` ≠ sha of the landed 27 lines (`c879abee…`, first 27 lines of the append); sha of last 27 lines `4c2ee1d7…` also ≠ |
| Misplaced scaffolding in README | **corpus/README.md:426-454** | stray fence :426; property table :428-434 (`bytes / lines | 2947 / 27`); `## 4. Validation on a scratch mirror (append, not edit)` :436; table :442-451; "Harness on the same mirror …" :453-454 |
| Where the declared blocks and their shas live (source of truth for the G1 equality check) | `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md:45-59` (A: fence `text` :49-53, sha :56, "295 / 2" :57) and `:61-100` (B: `## Round-37 admission` :68, sha :99, "2947 / 27" :100); §4 scaffolding :105-136; §5 cautions :137 | `git show 83975acc:.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md` |
| r38 already has a sibling seat producing `declared-blocks.txt` | `.ufo/waves/round-38/wave1/ExecDeclaredBlocks.md`, `ExecDeclaredBlocks.gen.sh` (untracked at read time) | not read here (outside the item) |
| Report claim contradicted | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-37/kasegi.md:76` ("No cross-domain bleed (PROVINCE.md still accurate)") ; SHONEN.md:176 region | spot-check §2 "material record defect" (lessons/round-37-verifier-spotcheck.md:113-120) |

### 3.2 D-B — judged-head naming and committed run

| claim | path:line / hash | evidence |
|---|---|---|
| all-gates.txt at T exists, 121 lines, 9238 B (blob `09c3a187…`), header `all-gates v1`, `export-ref=9492c776724e737caf5815fabc98e59ea04830df`, `suite-sha256=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d`, `run-utc=2026-10-26T18:00:21Z`, `closed=14/14 exit=0`, `selftest cases=14 failures=0` | `.ufo/waves/round-37/final-gates/all-gates.txt:1-4` (summary lines in the file) | `git show 83975acc:… | sed -n 1,8p` |
| it grades the F1 head 9492c776, NOT A and NOT aa88877b; commit aa88877b only rewrote 7 lines of it (`git diff 9492c77 aa88877 --stat`: 7+/7-) | all-gates.txt | `git diff --name-only 9492c77 83975acc -- . ':!.ufo/waves/round-37/wave1'` → all-gates.txt, kasegi-r37-build-results.json, SCORECARD.md, SHONEN.md (the post-graded-head diff, 4 paths) |
| three artifacts name three heads | SCORECARD.md:1505 (`--export-ref aa88877bf921d952137817b91ca76234b206da65`) · SHONEN.md:172 (`final lane head aa88877b…`) and :176 (`--export-ref aa88877b…`, "raw transcript committed at all-gates.txt") · report `kasegi.md:3,8,37-38` (`2387dcf6`) · all-gates.txt:2 (`9492c776`) | SHONEN :176 claims the committed transcript of aa88877b, but all-gates.txt export-ref is 9492c776 |
| F3 commit 2387dcf6 replaced placeholders `<r37-final-head>` (SCORECARD:1505) and `<r37-final-lane-hash>` / `<fill>` (SHONEN:172) / `<r…` (SHONEN:176) that existed at 9492c776 | `git diff aa88877 2387dcf -U0` | `git grep -n '<r37-final-head>\|<r37-final-lane-hash>\|<fill>' 9492c77 -- SCORECARD.md SHONEN.md` → SCORECARD:1505, SHONEN:172 (2 tokens), SHONEN:176 (hit); the same grep at T over SCORECARD/SHONEN/LOG/lesson/PROVINCE/README finds none |
| Fixed-point protocol that the receipt follows | `.ufo/waves/round-37/wave1/ExecGateReviewPrep.md:120` (§2.6 self-reference limitation), `:101` (§2.5 E10 limbs); lesson F5 bullet `corpus/lessons/round-37.md:331` | |
| Round-38 J rule (for contrast) | `.ufo/waves/round-38/claims.json` `judged_head_rule` | receipt `export-ref=` = J; Y adds only the receipt |

### 3.3 D-C — the seven `⟨pending…⟩` markers in `corpus/lessons/round-37.md` (T = A for this file; `git diff --stat 2387dcf 83975acc -- corpus/lessons/round-37.md` empty)

`git grep -c '⟨pending' 83975acc -- corpus/lessons/round-37.md` → 7. For each: the receipt/file the marker names, and the committed location a resolution can cite.

| lesson line | marker text | resolves to (committed at T) | exact pointer / digest |
|---|---|---|---|
| :10 | `⟨pending: L1 closure commit — a commit cannot carry its own hash⟩` (round-37 final lane commit) | r37 judged head A = `2387dcf6ccfefcfb703783387b9aade8fc82abfa` (report `kasegi.md:3`) and lane tip T = `83975acc46…` (post-measurement results commit) | commits table §1 rows 1-2; lesson anchor text :7-10 |
| :85 | "**not landed**" (entry drafted at 84 lines) | `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` landed in 0acffc82, 84 lines, `:3 source: S054 — https://certcc.github.io/SSVC/tutorials/ssvc_overview/ …`, `:4 verified-at: 2026-10-26`, `:6 recheck: cd … && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054` | `git show 83975acc:<path> | wc -l` → 84 |
| :90 | `⟨pending: entry file at the integrated head⟩` | same entry path as :85; registry row `corpus/SOURCES.md:60` (S054); capture `corpus/source-snapshots/round-37/S054.txt` (blob `fa773ded…`, 32623 B) and `manifest.json` (blob `046fa728…`, 3989 B) | `git ls-tree -l 83975acc corpus/source-snapshots/round-37/` |
| :95 | `⟨pending: ExecC2Harness / final-gates transcript at the integrated head⟩` (S054 recheck at the committed path) | `.ufo/waves/round-37/wave1/ExecC2Harness.md:222-232` (§4.1: `S054:sha256 OK`, `Q1 … anchor=6-ok`, `Q2 … 7-ok`, `Q3 … 14-ok`, `EXIT=0` — a **scratch-mirror** run, not the committed path); harness reading :16-17 (`entries=23 pass=23 exit=0`, `PASS F20 … ids=S054`); caveat §6 :363-402 | **Gap:** no committed transcript at the integrated head carries the live run: `all-gates.txt` has no S054/harness line (its E-lines are the suite's), and SCORECARD.md:1505 / SHONEN.md:176 / report only *assert* `source-recheck S054 exit 0`. Other committed mirror/critic runs: `CritBoundary.md:159,180` (`S054:sha256 OK`), `CritC2Kill.md:37` |
| :216 | `⟨pending: wave1/ExecGateReviewPrep.md; file at the integrated head⟩` (positive limb committed) | receipt `.ufo/waves/round-37/wave1/ExecGateReviewPrep.md` (852 lines; §1 deliverables :33-46, §2 format contract :48-175, §3 verifier+assembler :176-442, §4 base transcript :443-765, §5 findings :766, §6 provenance :822, §7 writes/scratch :839); file `.ufo/waves/round-37/final-gates/all-gates.txt` (121 lines, blob `09c3a187…`, grades 9492c776 — see §3.2) | verifier A2 sha `04c0ece2efa7bb5ab038c2a9f835346514e0f9a8e5dcadf4076c8d…` (receipt :36), assembler A3 `ff744113…` (:37) |
| :265 | `⟨pending: wave1/ScribeConsiderthese.md §3 delivers the byte-exact block, sha256 7c232983…⟩` (the ledger landing) | `.ufo/waves/round-37/wave1/ScribeConsiderthese.md` §3 :53-122: fenced block = lines **59-120** (the fence pair is :58/:121), 62 lines / **9184 B**, sha256 **`7c23298319a581720a5a66f63ea0b97ca65f2b9f3dd858bfd019fd86abc43706`** — recomputed here: `sed -n 59,120p | sha256sum` → `7c232983…`, `wc -c` → 9184 (equal to the receipt's claim). 18 table rows = :76-93 (5 of 2026-10-24 :76-80, 6 of 2026-10-25 :81-86, 7 of 2026-10-26 :87-93) | **but the ledger bytes did not land there** — see §3.4 |
| :300 | `⟨pending: L1 integration census measurement⟩` (after-state at the integrated head) | Mirror after-state: `.ufo/waves/round-37/wave1/ExecCensusReplay.md:81-97` (§3, rows 54, tier.A 51, mined 42, exit 0, W04 S028/S029) and §4 arithmetic :98-110 (`file rows 54 | tier.A 51 …`). Before-state: `.ufo/waves/round-37/census-before.txt:1-5`. Integrated-head assertion only in prose: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-37/kasegi.md:52` ("census → exit 0 (W04 S028/S029 only), before and after"), :57-60; SCORECARD.md:1505 ("census exit 0"); registry rows 54 = `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` per SCORECARD:1505 | **Gap:** no committed census transcript at the integrated head; census is read from the fleet root (not an export), so a r38 resolution must run `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` live or cite the report text |
| :320 | `⟨pending: measurement at the integrated head⟩` (No-harm) | `.ufo/waves/round-37/wave1/RevNoHarm.md` (133 lines): gate `noharm-gate.sh` §5 :53-100, L1 post-integration command set §7 :105-127 (`git diff --numstat "$BASE" "$NEW"`), baselines §4 :47-51 (density mean **225.3**, 1111 lines); independent non-author measurement: `corpus/lessons/round-37-verifier-spotcheck.md:105-112` (`git diff --numstat B A -- . ':!.ufo'`: every file N/0; SKILL.md 2/0, SCORECARD.md 15/0, PROVINCE.md 74/0, corpus/README.md 56/0, SOURCES.md 1/0, QUALITY.md 14/0, LOG.md 17/0, SHONEN.md 9/0) | the L1 never recorded the post-integration gate output in the lesson; the report cites "RevNoHarm" only (SHONEN.md:172 "post-append re-measurement in RevNoHarm") |

The lesson's own closure bullets sit at `corpus/lessons/round-37.md:325-335` (335 lines total; `## Integration resolutions (L1 addendum, appended 2026-10-26)` heading :325; F1 :327, F3 (ledger path) :329, F5 :331); they resolve F1-F7, not the seven markers.
Widened-placeholder vocabulary (G3 test inputs): `⟨pending` (U+27E8) occurs only in `corpus/lessons/round-37.md` at T; angle-token placeholders existed at 9492c776 in SCORECARD.md:1505 `<r37-final-head>` and SHONEN.md:172 `<r37-final-lane-hash>`, `<fill>` (+ :176 `<r…`), all gone at T. `git grep -n '⟨pending'` at T over SCORECARD/SHONEN/LOG/PROVINCE/README → none.

### 3.4 D-F — the ledger: "18-row disposition table" vs the bytes

| claim | where | observed bytes |
|---|---|---|
| "round-37 18-row disposition table + re-pin note (claims.json shorthand `corpus/considerthese-ledger.md` resolved to this tracked ledger — F3 resolution)" | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-37/kasegi.md:25` (files-changed list) | at T `corpus/knowledge/considerthese-proposals-ledger.md` is **43 lines** (base b56a416: 35 lines); `git diff b56a416 83975acc --stat` → `8 insertions(+)` |
| lesson F3 bullet: "extended this round with the 18-row disposition table and the re-pin note; R31 cites the …" | `corpus/lessons/round-37.md:329` | the extension = 0acffc82's 8 added lines: `:37 ## Round-37 dispositions (appended 2026-10-26, R31 home)`, `:38-40` three blank lines, `:41 ## Re-pin note (appended 2026-10-26)`, `:43` re-pin paragraph (sha256 `57584fda83b813e44fb2e2cb6cb2b1e4af1dd20f07877a6b119db9ba9feb43cf`, 554 lines for score-gap.py). **The section has zero table rows** (`:37` heading is followed only by blank lines up to the next heading; `grep -c '^| 2026-10-26'` over the ledger at T → 0; the only `| N. ` rows are :11-16 and :28-33, all 2026-10-25 proposals) |
| R31 names the file as the ledger home | `corpus/QUALITY.md:278` ("…recorded old→new, in the round lesson and in `corpus/knowledge/considerthese-proposals-ledger.md`") | row cites path correctly; the section content is what is missing |
| the byte-exact 18-row block exists only as a draft in a receipt | `.ufo/waves/round-37/wave1/ScribeConsiderthese.md:59-120` sha `7c232983…` (see §3.3 :265); its path header says `corpus/considerthese-ledger.md` (new file), a path that has never existed (`git ls-tree -r --name-only 83975acc | grep considerthese-ledger.md` → none; only `considerthese/2026-10-19..26.md` and `corpus/knowledge/considerthese-proposals-ledger.md`) | the draft is a whole-file (starts `# considerthese proposal disposition ledger`, has its own `## Re-pin of the round-30 knowledge ledger` :95 and `## Limits` :111 inside the fence), so it cannot be pasted under the existing heading unmodified |
| the 7 proposal rows for G7 (2026-10-26 file) are drafted at | `.ufo/waves/round-37/wave1/ScribeConsiderthese.md:87-93` (proposal # 1-7: distance-to-next-score thresholds `open`; end-to-end domain task `open`; quiescence gate `mined → landed r36 (R28 + E9)`; cap wave evidence `open`; F18 PROVINCE amendment `mined → landed r36`; re-tune cadence `open (recorded, no change)`; proposal-status ledger `mined → landed r37 (R31 + this file)`) ; lesson summary of the same seven at `corpus/lessons/round-37.md:262-286` (## considerthese 2026-10-26 dispositions :262; "Conflict recorded, not resolved" :282-286) ; source proposals `considerthese/2026-10-26.md` (7 proposals; proposal 7 text at :35 per QUALITY.md:278 evidence cell) | the lesson at :265 itself says "18 rows" and `corpus/considerthese-ledger.md` (new file) — contradicts :329 |
| conflict record on path ambiguity | `.ufo/waves/round-37/wave1/ScribeQualityRows.md:105` (F1: claims.json:78 names a nonexistent ledger path) and `:135` (F5: ledger append owed by another seat) | |
| existing, correct ledger structure the G7 check can mirror | `corpus/knowledge/considerthese-proposals-ledger.md:20` (`## Round-31 status flips (appended 2026-10-25)`), table :24-35 (header row + 6 proposal rows, columns proposal / status before / status after / evidence), audit line `:35` (`Round-31 audit at append time …`); r31 section rows :28-33 (header :26-27), each starting `\| N. title \|`; base table rows :11-16 |

Ledger heading list at T (`grep -n '^#'`): `:1 # considerthese proposal status ledger`, `:18 ## Limits`, `:22 ## Round-31 status flips (appended 2026-10-25)`, `:37 ## Round-37 dispositions (appended 2026-10-26, R31 home)`, `:41 ## Re-pin note (appended 2026-10-26)`.
Consequence for G7: the empty heading is at `:37`; because the file is append-only (R9/R6 in the lane's QUALITY rules), a filled section must be appended at EOF as a new dated section (or the empty heading's three blank lines at :38-40 are the only bytes that may be touched, which an append-only rule forbids); the check should count rows beginning `| N. ` for the 2026-10-26 seven (`ScribeConsiderthese.md:87-93` columns date/#/proposal/status/evidence is a 5-cell shape; the ledger's own r31 section uses a 4-cell shape `proposal | before | after | evidence`).

### 3.5 D-D and D-E

| claim | pointer | evidence |
|---|---|---|
| D-D: `Final lane commit: f3246559bed2fd085dde860e00247ce394f02bad (round-37 wave-evidence ancestor; the round's final head is named in the report).` | SCORECARD.md:1509 (`## Round 37 result` is SCORECARD.md:1496; `Anchor ancestor (r36 lane head): c20300df…` :1507) | `git grep -n 'Final lane commit' 83975acc -- SCORECARD.md` → :987, :1129, :1492 (round-36 `e666d902…`), :1509 (round-37); f3246559 = commit §1 row 9 (wave evidence, 13:59:17) — an ancestor, not the final head |
| D-E: scratch not empty at closure | spot-check §5 `/fast/scratch/hyaku/kasegi-r37/build-spec.py` remained; report `kasegi.md:41` "scratch empty"; round-37 mechanism `.ufo/waves/round-37/wave1/ExecQuiescenceProbe.md` (360 lines) and E9 payload `all-gates.txt:16` (`scratch-seat-dirs=0 … scratch-root=present`) | **Live now (2026-10-26 ~15:37 -0300):** `ls /fast/scratch/hyaku/kasegi-r37` and `…/kasegi-r36` → `No such file or directory` (both absent); `/fast/scratch/hyaku/kasegi-r38` present with live seat dirs of this round's wave (expected until each seat yields). G6 must treat absence of r36/r37 dirs as pass and require r38 absent at the final check |

## 4. Facts a G-check author needs (cross-cutting)

- All r37-closure.sh claims: suite blob at T `corpus/instruments/r37-closure.sh` 73132 B (`68ac41e8…`); sha256 `0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d` (all-gates.txt:3 `suite-sha256`, also report `kasegi.md:8`).
- G8 carry-over: on exports A (2387dcf6) the report asserts `closed=14/14 exit=0` (report :37-38); the committed run (all-gates.txt) is on 9492c776. The r37 suite's own E10 limb verifies a receipt with `export-ref` an ancestor of the head (`ExecGateReviewPrep.md:101-119`).
- Round-37 lesson sections at T: `## Frozen claims` :28, `## Gate` :36, `## Assimilation: none adopted` :233, `## considerthese 2026-10-26 dispositions` :262, `## Census` :288, `## Mistakes` :302, `## No-harm` :318, `## Integration resolutions (L1 addendum, …)` :325 (`git show 83975acc:corpus/lessons/round-37.md | grep -n '^## '`).
- Spot-check §5 text for each routed defect (verbatim source of the round-38 corrections): `corpus/lessons/round-37-verifier-spotcheck.md:157-183` (D-A :159, D-B :165, D-C :169, D3 :175, D-D :178, D-E :181).

## 5. Commands run (read-only) and tooling

`git -C <lane> log --name-status --format=… b56a416..83975acc`; `git show 83975acc:<path>` for lesson, ledger, PROVINCE, README, SCORECARD, SHONEN, QUALITY, all-gates.txt and the r37 wave receipts; `git grep -n` at T and 9492c77; `git diff --stat/--numstat/-U0` (9492c77..aa88877, aa88877..2387dcf, b56a416..T for the ledger); `cmp` prefix tests and `wc -lc`/`sha256sum` on scratch extractions of PROVINCE.md and corpus/README.md (b56a416 vs T); `sed -n 59,120p ScribeConsiderthese.md | sha256sum`; `python3 -c json` on dispatch/results counts; watchdog/report reads in the fleet root (read-only); `ls /fast/scratch/hyaku`.
No tools installed or upgraded; no network fetch; no lane/fleet file written. Scratch `/fast/scratch/hyaku/kasegi-r38/ScoutR37Evidence/` removed on exit (trap).
