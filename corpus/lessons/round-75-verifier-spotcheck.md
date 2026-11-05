# Round 75 — verifier spot-check (kasegi)

author: hyaku closure (non-author integrator, @m_zfl)

Round: kasegi r75, attempt 2. Report `.ufo/reports/round-75/kasegi.md` (fleet repo commit
`56aa78eb`, author `kasegi-shokunin <kasegi@shokunin.local>`). Base
`f9cc05b56170946192a2dcafcc07e90ec611746c`, tip `373bf4e7f9f9a6b59008e8f39a5a7aecd17c4b84`
(= remote `master`, `ahead=0`, worktree clean); landing commits `7d692165445ca1c252e7771c6cb2f4970bc9a17a`
(C1+C2+lesson+scorecard+log+wave evidence) and `373bf4e7` (misroot recovery, M75-5); freeze
`748dfb6`, controls `c880047`. Driver digest (copied verbatim from the closure dispatch;
`.ufo/watchdog.log` is mutable): launch 06:28:56-03 attempt=1 → lane-dead-no-report 06:53:21-03 →
launch 06:53:24-03 attempt=2 → complete 07:22:14-03. All times below are as printed.

## 1. Step-1 conformance

| check | command | result |
|---|---|---|
| report committed by lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-75/kasegi.md` (fleet repo) | `kasegi-shokunin kasegi@shokunin.local 56aa78eb…` — PASS |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` = 1; `grep -cE '^- \[.\]'` = 4 | 4 box lines (`[~]`,`[ ]`,`[~]`,`[~]`) = the 4 canonical boxes — PASS |
| cited commits exist and are ancestors | `git merge-base --is-ancestor <h> master` for `373bf4e7`, `7d692165`, `748dfb6`, `c880047` | all 4 OK (tested against the branch ref, not `@{u}`) — PASS |
| lane repo pushed, no uncommitted round work | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain` | `local=373bf4e7 remote=373bf4e7 ahead=0 behind=0`; porcelain empty — PASS |
| prompt carries the template contract | read `.ufo/prompts/kasegi-round-75.md` | §1 mission/axes binding, §2 1–3 falsifiable claims (lowest-axis rule), §2b frontier step, §3 L2 floor (≥8, one batched call), §4 report contract (path, SHONEN-heading rule, commit-hash citation, marker rule), §5 commit-then-push + push scope + L0 channel, §6 hyaku addendum — PASS |
| marker rule | report content | real work, evidence pointers, per-claim measurements, commit-hash citations — a report, not a marker |
| SHONEN.md untouched by the lane | `git diff f9cc05b5 373bf4e7 -- SHONEN.md` | empty — PASS (assessment lives in the report only) |
| evidence timestamps | receipts 09:42:39–09:51:07Z vs commits 09:45:03Z (`c880047`), 10:20:31Z (`7d69216`), 10:20:53Z (`373bf4e7`), all `-03` | every receipt at or before the commit that ships it — PASS |
| round number | commits, LOG.md, lesson, report all say round 75 | no mislabeled round — PASS |

## 2. Per-claim re-check (measured on committed bytes at `373bf4e7`)

**Method note.** C1 rests on the lane-owned census gate and its selftest; per PROTOCOL §Gate
standard (Closure consequence) this verifier did **not execute** `recheck-cwd-census.py` (or the
other lane instruments). C1 is **evidence-verified**: committed receipts + revision pin + code
inspection. C2's underlying counts are **re-measured** by this verifier with plain grep/wc/sha256
over committed bytes; the gate-typed outputs (frontier/capture/source-recheck) are
**evidence-verified** from receipts. No lane gate was executed by closure.

### C1 — depth:verifiability (score 4 → 4 held, nominal per QUALITY R58)

| reported | re-check command | observed |
|---|---|---|
| instrument sha256 `e666ae11…a21a` on landed bytes | `git show 373bf4e7:corpus/instruments/recheck-cwd-census.py \| sha256sum`; same at `7d692165` | `e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a` at **both** landing commits (diff between them: 0 lines) — revision pin holds; the `373bf4e7` change did not touch the counter |
| selftest `cases=5 failures=0` → `cases=6 failures=0` | receipt `.ufo/waves/round-75/controls/c1-donothing-r75.txt` (base counter) and `c1-after-r75.txt` (landed) | base: `selftest cases=5 failures=0`, real-tree census `entries=90 … norecheck=0`, `conformant`, exit 0. landed: `selftest case=restoration-only ok … restoration_only=1 marker_present=False main_ret=1`, `selftest cases=6 failures=0`, exit 0 |
| do-nothing control (base passes real tree) | `c1-donothing-r75.txt` | `RECHECK-CWD entries=90 noprefix=0 exit2_foreign=0 exit0_foreign=68 exit1_foreign=22 … conformant, exit=0` — matches report |
| red-before (fix shown able to fail) | `c1-redbefore-restoration-r75.txt` | base counter on the restoration-only fixture: `NORECHECK r.md`, `norecheck=1`, `RECHECK-CWD-RESULT conformant`, exit 0, marker absent — the old counter passes while the entry's restoration command never ran; the fix turns exactly this state nonconformant (case 6 asserts `main_ret=1`) |
| amendment present in landed code | `grep -n 'restoration_only\|restoration-recheck\|RESULT' corpus/instruments/recheck-cwd-census.py` | `restoration_only` bucket (doc lines 14–23, counter lines 87–94, print line 115–118), RESULT conformance requires `restoration_only == 0` (line 275), selftest case 6 (lines 230–244), expected tally string `selftest cases=6 failures=0` (lines 32/130/248) |
| A4 parity (one differing line) | `c1-after-r75.txt` §A4 | diff is exactly the inserted `restoration_only=0` |
| exec surface unchanged | `c1-after-r75.txt` §A3 | `bash_c=1 subprocess_run=1` |
| kill rule | `MutAuditC1.md` cited by `c1-after-r75.txt` | M-P1/P2/P5 killed; **M-P4 survives** — the lane did not hide it: routed as R75-2/M75-3 in the lesson and the SCORECARD claim-verdict paragraph |

Claim verdict: **VERIFIED** (evidence-verified; gate not executed by closure). The counter is
strictly stronger: the restoration-only class is visible, gated, and selftested, with the red-before
on record. Routed letter gaps (M-P4 survivor, forged-relabel pass) are recorded, not reworded after
scoring — kill rule respected.

### C2 — coverage (score 8 → 8 held; denominator operator-owned)

| reported | re-check command | observed |
|---|---|---|
| registry rows 109 → 110 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | **110** |
| 0 rows removed | `git diff f9cc05b5 373bf4e7 -- corpus/SOURCES.md \| grep -c '^-[^-]'` | **0** |
| exactly 1 row added (S110) | `git diff … \| grep -cE '^\+\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | **1** (`\| S110` at `corpus/SOURCES.md:122`) |
| knowledge 90 → 91 | `ls corpus/knowledge/*.md \| wc -l` | **91** (includes `fuzzilli-ndss2023-jit-fuzzing-paper.md`) |
| knowledge-expected 92 → 93 lines / 91 rows, sorted, set-equal | `wc -l`; `LC_ALL=C sort -c`; set diff vs directory | 93 lines = 91 rows + 2 header comments; sort OK; set-equal to the 91 files modulo the `corpus/knowledge/` prefix |
| S110 capture | `sha256sum corpus/source-snapshots/round-75/S110.txt` | `0780beaefb5c0d973c76d4376a0c151345910890fa9a913b68461d71747e51ef` — matches report; 1869-line text capture + `manifest.json` committed |
| capture bound 88 → 89 | receipt `c2-base-counters-r75.txt` (`records=88 bound=88`) → `c2-after-binding-r75.txt` (`records=89 bound=89 unbound=0`, `round-75 records=1 url_bound=1 fetched=1`) | matches report |
| frontier 52 → 53 admitted, entries 55 → 56 pass | `c2-base-counters-r75.txt` (`rows=52 admitted=52 … entries=55 pass=55 exit=0`) → `c2-after-frontier-r75.txt` (`rows=53 admitted=53 …`, `FRONTIER-PASS F53 ids=S110`, `entries=56 pass=56 exit=0`) | matches report |
| 24 quotes located at anchors | `c2-after-srcrecheck-r75.txt` (`S110:sha256 OK`, Q01–Q24 each `OK occurrences=… anchor=…-ok`) | matches report |
| ≤25-word cap actually measured (M75-2 gap) | `python3` over `manifest.json` `sources[0].quotes` | 24 quotes, **max 12 words, 0 over 25** (min 1) — the cap holds in fact even though no command enforces it (R123 routes the enforcement gap) |
| census validate | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` (this verifier ran it) | `kasegi ok`, exit 0; six inherited W04 duplicate-url warnings, unchanged from base |

Claim verdict: **VERIFIED** (counts re-measured; gate-typed outputs evidence-verified). The sourced
claim cites S110, opened this round (fetched 2026-11-05T09:51:07Z; URL re-opened live by closure —
HTTP 200, `application/pdf`, 918189 bytes, 2026-11-05T10:26:34Z).

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| `depth:verifiability` (owned, 4→4 held) | **improved** | C1 verified above: new failure class visible + gated + selftested, red-before receipt, revision-pinned sha256, parity one-line delta; routed gaps stay on the defect queue instead of being reworded |
| `coverage` (owned, 8→8 held) | **improved** | C2 verified above: F53 admitted on ground the coverage map did not hold (S110 row, knowledge entry, frontier/capture/frontier counters all +1 with exit 0) |
| `depth:density` (owned, not targeted) | **unchanged** | SCORECARD row untouched (9, last change r15); no re-measurement claimed |
| harm check | none | `git diff f9cc05b5 373bf4e7 -- SCORECARD.md` is additions-only; no score decreased; no owned axis re-graded down |

## 4. Discernment spot-check (LEARNING.md; ≥1 admit and ≥1 reject re-opened)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S110 — NDSS Symposium 2023 Fuzzilli paper (`corpus/SOURCES.md:122`, knowledge entry, F53) | ADMIT | URL `https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf` re-opened live: HTTP 200, `application/pdf`, 918189 B; committed capture sha256 matches; capture line 33 | **agree** | capture is real and revision-pinned; the entry scopes itself to the paper's own statements (design, comparator naming, evaluation counts) and explicitly does not verify the priority claim — correctly tier-A, correctly bounded |
| 12-word Gate quote "In this paper, we close this gap and present the first fuzzer" | (quote check on the new row) | `sed -n '33p' corpus/source-snapshots/round-75/S110.txt` — byte-exact at capture line 33; 12 words | **agree** | ≤25 words, located, grounds `teaches` |
| all 24 manifest quotes | (bound check) | word-count over `manifest.json` quotes | **agree** | max 12 words, 0 over 25 — the B5 cap holds in fact; the missing enforcing command is routed (R123), so the letter gap is learned, not hidden |
| OSV.dev overview page | REJECT (stays lead, no row) | `corpus/SOURCES.md:176` lead bullet unchanged from base; no new OSV row (registry diff adds only S110) | **agree** | CORPUS rule 1: a row needs a capture opened in the round that writes it; rejecting the unopened page as a row is exactly the rule — taste over row-count |
| revenger NDSS rows S114/S341/S363 as S110 duplicates | REJECT (different papers) | `grep -ril fuzzilli /home/vgpnk/Projects/shokunin/revenger-shokunin/corpus` = 0 files; revenger `S114` = "No More Gotos … NDSS 2015" | **agree** | distinct documents with a different DOI; refusing to fold them into S110 prevents a false dedup |
| assimilation of `merge/kasegi/SOURCES.append.md` | REJECT this round (adopt nothing; L0 filed) | guard receipts (reg-ids 109, staged-ids 94, collisions 79) cited at `.ufo/l0-questions.md` line 328 | **agree** | 79 id collisions are mass id drift a read-only check cannot fix; adopting nothing and escalating is the §6-item-10 rule correctly applied |

## 5. Trend verdicts (closure's own, evidence above)

- **expansion: improved** — one new admitted entry on uncovered ground (F53/S110/knowledge 90→91), registry +1 mined row, frontier rows 52→53 admitted; re-measured by closure.
- **quality: improved** — C1 makes a previously invisible failure class visible and gated (red-before + landed receipts); C2's 24 quotes located, cap holds in fact; census validate exit 0; no admitted entry failed a re-check.
- **discernment: improved** — the outside spot-check (this file) agrees with the gate on the sampled admit (S110) **and** the sampled rejects (OSV lead, revenger duplicates), and the M75-2 disagreement became grounded criterion R123 (QUALITY.md, with lesson citations R121–R123). The lane graded itself `unchanged`, reasoning from the attack seats' frozen-predicate letter gaps; that conservatism is honest but the LEARNING.md improved-clause is satisfied on both prongs, so closure grades `improved` and records the divergence here. `harmed` is ruled out: no disagreement left unlearned (all routed R75-1…R75-5), no criterion without a lesson.

## 6. Routed defects (the lane must fix next round; lane-routed rows stand)

- **R75-1 (M75-3):** bind C1 clause (ii) at file level (`norecheck` = neither header) — the forged `restoration_only` relabel of the base `norecheck` bucket still passes the frozen case 6; needs its own freeze + do-nothing control.
- **R75-2 (M-P4 survivor):** case 6's RESULT limb is removable without a failing selftest; the marker-absent conjunct is the only detector for that class in the frozen fixtures.
- **R75-3:** no fixture carries both `recheck:` and `restoration-recheck:`; the real tree has two such files (`claim-gates.md`, `claim-package-contract.md`).
- **R75-4:** an abstract-only entry would pass B1–B8; the comparison ground is not required to be quoted from the body.
- **R75-5:** the B8 sibling sweep (`grep -ril fuzzilli`) cannot discriminate — empty by construction.
- **R75-6/R75-7/R75-8:** stand as lane-routed (census-at-revision; wave ordering; considerthese P4 operator-owned).
- **Closure-routed (integrator/operator, not lane debt):** the r75 L0 question (`.ufo/l0-questions.md:328`, assimilation decision + ready-file `l1` routing) is appended but **uncommitted in the fleet repo at closure** (last commit touching the file is `d421a9af`, round-63); the report's landed-changes table says it rides "fleet commit of this report", but that commit (`56aa78eb`) does not include it. L0 durability is integrator-owned — commit with the next integration pass; conformance defect recorded, status-neutral.
- Cosmetic (no routing): `c1-after-r75.txt` §A3 carries a scratch aside ("…a21302a? verified: e666ae11fd9d50ec"); the full sha256 is verified by closure on the landed bytes, so the receipt is sound.

## 7. Notes for the operator

- All claims verify and no owned axis is harmed → **admitted**. Scores held nominally (4/8/9); the substance moved in the counters and the corpus, which the SCORECARD rows document.
- SHONEN: box 2 (`end-to-end domain task`) remains `[ ]` untouched; boxes 1/3/4 are `[~]` author-asserted with resolvable pointers. No `[x]` exists anywhere — promotion verification by a non-author is still required; promotion is operator-owned. The boxes look checkable by a non-author from the cited pointers.
- Attempt-1 died without a landed report (driver `lane-dead-no-report`), attempt 2 inherited the frozen claims, controls and wave `w1` and re-measured them on the landed bytes before reuse — the inheritance discipline the prompt requires was followed (M75-4 records the routing gap; L0 filed).
