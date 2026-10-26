# SentinelFinal — round-40 falsify wave 2 receipt (final scope audit)

Seat: `SentinelFinal` (sentinel). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only lane repo).
Fleet root `/home/vgpnk/Projects/shokunin` and `/home/vgpnk/Projects/shokuknow` were read only.
Snapshot: **2026-10-26T22:22:13Z** (19:22:13 -03); the wave was still landing (2 seats out), so §4's matrix is the
*last* reading this seat took, and earlier readings are quoted where they matter. Refs: lane `HEAD` = `3074c7679d6f527ec3930d7748ccce1dbae4a58a` (= J, J5),
claims freeze `5e985b74075dd3813a63d7750966bf8abf693465`, base `a7af2ce63bce153757d39bf66b366a96caf30c13`.
Milestone attacked: round-40 falsify wave 2 (C1 suite/counters, C2 decisions/rows/entries, source re-open, junk controls)
— this seat attacks **the integrated state the wave will be judged on**, not an individual claim counter.

## 0. Verdict on the four scoped items

| item | result | one-line evidence |
|---|---|---|
| (1) fleet-root untracked files naming kasegi/round-40 | **no misroot** | `git -C /home/vgpnk/Projects/shokunin status --porcelain` empty; 3 ignored files name kasegi round 40 and all three are orchestrator-owned (§2) |
| (2) lane clean at Y apart from expected wave evidence | **at J: clean; Y does not exist yet** | zero tracked modifications; 106 untracked paths, every one inside the allowed evidence set; the receipt itself is untracked, so the claims' "lane tip Y" is not yet a commit (§3, D1) |
| (3) wave-2 seat receipts complete | **in progress, 33/35 at the final reading** | 35-seat roster, 33 `<seat>.md`, 0 non-roster receipts, every present receipt carries attacked-item/command/verdict; 2 mutant seats still running (§4) |
| (4) no seat wrote a forbidden path | **no write to the enumerated forbidden paths; one transient in-lane write found live (D9)** | 0 write-verb hits against `templates/`, `scripts/`, `.ufo/state`, `.scratch`, shokuknow in 142 wave-1 + 99 wave-2 files (the wave-2 sweep ran when the dir held 99); physical state matches; but a seat probe wrote and then removed 3 suite files at the lane root (§5) |

Beyond the four items I re-derived the whole receipt payload set independently from the `git archive` export of J
(§6) and re-ran the C2 counters at J (§7). H1, H2, H3, H4, H7-shape, H9 and H10 reproduce exactly; all eight C2
counters are green. H5, H6 and H8 (suite-internal negative controls) were **not** re-run by this seat (§8).

## 1. Defects and risks

Severity index: **D1 high** (Y does not exist), **D2 high** (evidence must be committed before the receipt),
**D9 medium-high** (suite writes into the real lane when `--lane` names another repo; `--receipt-out` unguarded),
**D3 medium** (nothing checks Y == lane tip), **D4–D8 informational**.

### D1 — HIGH (blocks C1 reproduction): Y is not a commit, so "Y = the lane tip" is false at the tip

- **Attacked**: claims C1 `counting_commands` #1/#2 ("`--export-ref <Y>` → `closed=10/10 exit=0`",
  "`--selftest --export-ref <Y>` → `cases=10 failures=0`") under the frozen definition "the lane tip Y = J + the
  receipt only".
- **Command re-run**:
  `git -C <lane> rev-parse HEAD` → `3074c767…`; `git status --porcelain --untracked-files=all` →
  `?? .ufo/waves/round-40/final-gates/all-gates.txt`; `ls-tree HEAD -r | grep final-gates` → round-36/37/38/39
  receipts only, **no round-40 receipt**.
- **Result: contradicted.** The lane tip is J, and the receipt is untracked. `--export-ref HEAD` therefore exports
  a tree with no receipt, and H7's limbs cannot pass (`receipt=0`; `ancestor`/`h7-line` follow from the missing ref
  and missing line — code read, lines 514–556). The measured outcome is recorded by `LabDeterminismY`: two runs at J
  on the real lane print `closed=9/10 exit=1`, byte-identical to each other
  (`LabDeterminismY.J-run-a.txt`/`-b.txt`, sha256 `0939d3f9…`). A seat that follows the dispatch text literally
  ("Y = the lane tip") therefore records a false contradiction. Three wave-2 seats hit this and worked around it
  explicitly: `LabDeterminismY.md` §0 (O1, "no commit Y = J + receipt exists in the lane yet"),
  `CritReceiptForge.md` ("Y is reconstructed as a fixture repo F") and `RevC1Sandbox.md` (same, "Y not yet a lane
  commit").
- **Exploit path** (if filed as-is): the filed claim says "prints `closed=10/10 … on Y`" while the counting command
  at the lane tip prints 9/10; a verifier re-running the frozen command at the tip records a contradiction that
  the round cannot rebut, because the artifact that makes it green is not in the tree.
- **Impact**: C1 (depth:verifiability) is judged red for a bookkeeping reason, not a substantive one.
- **Smallest remediation**: after the wave settles, commit the receipt as its own commit (see D2 order) and re-run
  both counting commands at the real Y; record the two outputs in the closure. Nothing else needs to change.

### D2 — HIGH (ordering): wave-2 evidence must be committed *before* the receipt commit, and the receipt must be
regenerated at that new J

- **Attacked**: the claim's `judged_head_rule` ("Y adds only the receipt; `git diff --name-only J Y` =
  `.ufo/waves/round-40/final-gates/all-gates.txt`").
- **Command re-run**: read `h7_inner` in `corpus/instruments/r40-closure.sh` (lines 514–556) and `check_h7`
  (lines 799–847). `diffclean` starts at 1 and any path in `git diff --name-only <receipt.ref> <REF_RESOLVED>`
  other than the receipt sets it to 0; H7 requires `diff-clean=1`. The wave-2 evidence (103 files at the final
  reading) is currently untracked.
- **Result: reproduced constraint (fail-closed).** Two concrete failure modes:
  1. commit wave-2 files **after** Y: the filed run at Y stays green, but the lane tip is no longer Y and no check
     notices (D3) — the record then contradicts its own words;
  2. commit wave-2 files together with the receipt while `all-gates.txt` still names `export-ref=3074c76`:
     `git diff --name-only 3074c76 <Y>` lists the wave-2 paths → `H7 payload=…,diff-clean=0 closed=0` →
     `closed=9/10 exit=1`. The suite fail-closes, so this cannot be sneaked through; it can only waste a filing.
- **Round-39 precedent (same repo, verified)**: `git diff --name-only ee5ae5e 8371e7a` prints exactly
  `.ufo/waves/round-39/final-gates/all-gates.txt`, i.e. r39's final Y is (evidence commit) + receipt only, with the
  receipt regenerated at the end (`ee5ae5e` is the commit its receipt names).
- **Exploit path**: none — this is a self-enforcing gate. The cost is a red filing if the order is wrong.
- **Smallest remediation (exact sequence)**:
  1. commit the 35 wave-2 receipts + allowed fixtures as J′ (`git status --porcelain` then shows only the receipt);
  2. `bash corpus/instruments/r40-closure.sh --export-ref <J′> --lane <lane> --work <scratch> --receipt-out <new all-gates.txt>`
     (regenerates `export-ref` and `run-utc` at J′; do **not** hand-edit);
  3. commit that file alone as Y; verify `git diff --name-only J′ Y` = the receipt, `git diff --name-only <J′-ref in receipt> Y` = the receipt;
  4. run both C1 counting commands at Y and store the outputs with the closure.

### D3 — MEDIUM (claim clause unenforced): nothing asserts Y == lane tip

- **Attacked**: the phrase "the lane tip Y" in `judged_head_rule` and C1's predicate.
- **Command re-run**: `grep -nE 'rev-parse|symbolic-ref|HEAD|master|tip' corpus/instruments/r40-closure.sh` → the only
  uses are ref resolution (310–312), the H8 base/r39 pins (166, 858), the export default (1722) and fixture helpers
  (1075, 1087–1090). No comparison of the run ref against the lane tip.
- **Result: defect found (latent).** H7 asserts `ancestor=1` and `diff-clean=1`, both of which hold for any
  Y-shaped commit, so a commit landing after Y does not red the filed artifact. The claim's "tip" clause is
  therefore unverified by the instrument, and the only enforcement is the closer remembering D2.
- **Exploit path**: land wave-2 receipts (or a correction) after the receipt commit; the filed suite output stays
  `closed=10/10 exit=0` while the lane tip differs from the Y the claim names. A verifier who runs the command at
  the *new* tip gets `diff-clean=0` → 9/10, and the two results disagree.
- **Impact**: verifiability, not correctness: the round can be filed with a stale Y.
- **Smallest remediation** (filing-time assertion, no instrument change needed): record in the closure
  `test "$(git -C <lane> rev-parse HEAD)" = "<Y>"` and `test -z "$(git -C <lane> status --porcelain)"`, with output.
  If a future round wants this enforced, it belongs in the suite as an eleventh check.

### D4 — INFO: `declared-blocks.txt` is an entry-validity list, not a change inventory

- **Attacked**: H9's payload `declared=172,valid=172,tail=172,pure=1,paths=1,diff-read=ok`.
- **Command re-run** (independent of the suite): parsed all 172 declarations, recomputed `tail -n <lines> | sha256sum`
  over the export, `git diff --numstat a7af2ce… HEAD -- <path>` per entry, and diffed the declared path set against
  `git diff --numstat a7af2ce… HEAD`.
- **Result: reproduced 172/172 (no bad entry), plus a measured gap.** 192 paths changed base→J; a `corpus/SOURCES.md`
  (12 add / 9 del), the 4 empty `*-plan.err`/`*-run.err` transcripts, and `declared-blocks.txt` itself are
  structurally undeclarable; **14 further paths are pure appends (del=0) and still undeclared**:
  `LOG.md SCORECARD.md SHONEN.md SKILL.md PROVINCE.md corpus/QUALITY.md corpus/README.md
  corpus/instruments/knowledge-expected.txt corpus/lessons/round-39.md corpus/source-snapshots/round-40/manifest.json
  .ufo/waves/round-40/kasegi-r40-build-results.json .ufo/waves/round-40/wave1-spec.json
  .ufo/waves/round-40/wave2-spec.json .ufo/waves/round-40/wave1/ScoutS019.manifest-record.json`.
  This does not violate H9's stated contract ("every declaration equals the whole appended tail …", suite header
  lines 41–45), which quantifies over declared entries only.
- **Impact**: zero on the current claim. Risk is interpretive: "declared blocks" must not be cited as proof that
  every round-40 byte is accounted for. If a future round wants completeness, the check needs set equality against
  `git diff --numstat`, not a per-entry loop.

### D5 — INFO: the receipt proves reproducibility, not that a run happened

- `time-basis=ref-commit` and `run-utc` is the **committer instant of the ref** (verified: J's `%cI` =
  `2026-10-26T18:56:22-03:00` = `21:56:22Z` = the receipt's `run-utc`), and `--receipt-out` writes the transcript
  without printing it. Measured consequence: the receipt can be generated at J (no Y needed) and is byte-identical
  to a run at Y (verified below), so the artifact attests "this tree is green and the transcript is a function of
  the tree", not "a person ran it at T". This is disclosed by the `time-basis` header and is a stronger property
  than a transcript; recorded so no reader treats `run-utc` as wall-clock execution time.

### D6 — INFO: shokuknow `.git/` mtime moved; content untouched

- **Attacked**: "no seat wrote to shokuknow".
- **Command re-run**: `find /home/vgpnk/Projects/shokuknow -newermt '2026-10-26 18:00' -not -path './.git/*'` → **no
  file**; `stat .git/index` → `2026-10-24 23:33:24` (unchanged); `find .git -newermt …` → only the `.git` directory
  itself (19:07). `git -C … status --porcelain` shows a long-standing dirty tree (lane imports from earlier rounds).
- **Result: no content write in the round window.** The directory mtime is the trace of a transient read-side git
  artifact (index refresh/lock create+unlink) from a read command run without `--no-optional-locks`.
- **Exploit path**: none of substance; a read-side index refresh is a write into a read-only tree by the letter of
  the rule and could race a concurrent reader.
- **Smallest remediation**: read that repo as `git --no-optional-locks -C … status` (and set `GIT_OPTIONAL_LOCKS=0`
  in seat prompts). I used plain `git status` there once myself at 19:07 before switching; recorded for honesty.

### D7 — INFO: the only fleet-root state churn from this wave is orchestrator publish, not a seat

- `.jj/repo/op_store/operations/` gained operations at 19:07:48–19:08:08 whose decoded args are
  `jj --config 'snapshot.auto-track="none()"' … file track -- 'root:".scratch/goal-20261026-hyaku-run9.md"'`,
  `jj … status`, `jj --ignore-working-copy bookmark set main|master -r fa0120d9…`, and
  `jj --ignore-working-copy git push --remote origin --bookmark master --bookmark main`, identity
  `protocol-shokunin <protocol@shokunin.local>`. Fleet root is a colocated git+jj repo, so `--ignore-working-copy`
  is why `.jj/working_copy/tree_state` and the op heads moved without any working-copy snapshot of a seat's files.
- Attribution: orchestrator/operator publish of the fleet repo. No wave-2 seat ran a mutating git/jj command
  (evidence: no lane commit other than J1–J5 exists, and every seat transcript I read ran read-only git or
  fixture-local git).

### D8 — INFO for the L1's conformance list: `~/.local/bin/omp` written 18:10:45 during the run

- `ls -lat ~/.local/bin` → newest entry `omp` (275,970,224 B, 18:10:45) and the directory itself (18:10:45); no
  `git` shim present (`~/.local/bin/git` ENOENT — the run-9 kengaku shim is still gone).
- Not a kasegi seat: seats cannot install `omp`, and 18:10 matches the hyaku kernel bootstrap, not a seat spawn
  (wave 1 dispatched 18:13). Recorded because **any** PATH-directory write is a guard item, whoever did it.

### D9 — MEDIUM-HIGH (found live by this seat): the `--work` guard is scoped to the `--lane` *argument*, so a run can
write suite state into the real lane; `--receipt-out` has no lane guard at all

- **Attacked**: the suite's promise "Nothing is written under the lane by this suite except the single file named by
  `--receipt-out`" (header, lines 50–55) and the `--work` guard (lines 277–288).
- **Observation (independent of any seat's report)**: my lane-wide
  `git status --porcelain --untracked-files=all` at **22:15:41Z** listed three files at the **lane root**:
  `h7row.tsv` (236 B, mtime 19:15:40.187), `pay.tsv` (462 B, 19:15:40.190), `payloads.tsv` (698 B, 19:15:40.190);
  `git check-ignore` → not ignored, so they made the tree dirty; `h7row.tsv` contained exactly
  `H7<TAB>sentinel=1,ref=3074c767…,digest=1,time-basis=1,run-utc=1,not-future=1,header-lines=5,run-lines=10,body-lines=11,closed-0=0,closed-line=1,ancestor=1,diff-clean=1,diff-read=ok,payload-match=9,h7-line=1<TAB>1`,
  `pay.tsv` 9 payload lines, `payloads.tsv` 10 — i.e. the suite's own `$WORK` artifact set for a **green** run.
  By my next read (22:17Z) all three were **gone**.
- **Attribution**: `RevC1Sandbox.md` §D5 discloses the same write as an accident of its own probe — "`--work`
  resolving into the real lane was accepted and the suite wrote `export/`, `mut/`, `neg-base/`, `neg-r39/`,
  `payloads.tsv`, `pay.tsv`, `h7row.tsv` under the real lane … I removed the three surviving loose files
  immediately". My snapshot is the outside view of that window: the write is real, it landed in the lane, and it was
  gone ~90 s later, so **no post-hoc cleanliness check can see it**.
- **Why the guard misses it**: `make_work` compares the resolved `--work` only against `$LANE` (the argument). When a
  seat points `--lane` at a fixture clone and lets `--work` resolve (directly or via symlink) into the real lane, the
  comparison succeeds and the run writes into the real lane. I disproved the nearest alternative (a *relative*
  `--lane` slipping past the guard): `main` canonicalises `LANE` before `make_work` (lines 1708–1710), and in a fresh
  clone `--lane . --work .` dies with exit 2 and leaves no file (§6). So the bypass needs a **different** lane
  argument, not a relative one.
- **Sibling defect in the same boundary**: `--receipt-out` is written with `mkdir -p "$(dirname …)"` and a plain `>`
  redirect (lines 1011–1015) with no guard; `--receipt-out <lane>/SCORECARD.md` overwrites a tracked lane file with
  receipt bytes (reproduced by `RevC1Sandbox` on its own fixture); a typo in the L1's own receipt command is enough
  to clobber a lane doc.
- **Exploit path**: any seat that runs the instrument with a fixture `--lane` can overwrite lane files or fill the
  lane disk (the run's `export/` is a full 7,932-file tree copy) while its receipt says "read-only on the lane". If
  the writer crashes before cleanup, the lane is dirty at filing and the C1 kill rule trips; if `--receipt-out` is
  mistyped, the damage is silent content loss.
- **Impact**: medium-high on verifiability (the read-only claim is false for a whole class of invocations) and low on
  the current round (nothing survived; the real lane is clean now, `git status` shows no stray TSV).
- **Smallest remediation**: in `make_work`, refuse a `--work` that resolves inside **any** git work tree
  (`git -C <candidate> rev-parse --show-toplevel` succeeds, or any ancestor of it does), not just inside `$LANE`; and
  either guard `--receipt-out` the same way or restrict it to a path under `--work`. Filing-side stopgap: run the
  wave's cleanup check **after every seat has exited** (D2 step 1) and additionally assert
  `git status --porcelain --untracked-files=all --ignored` is empty except the declared evidence.

## 2. Item (1) — fleet root: no untracked file is a misrooted seat artifact

- `git -C /home/vgpnk/Projects/shokunin status --porcelain` → **empty** (fleet root clean; the tracked ledgers
  `LOG.md`, `SCORECARD.md`, `MANIFEST.json` etc. are byte-unchanged — contrast the run-9 15:29 fleet-root truncation
  incident).
- `git status --porcelain --ignored | grep -i 'kasegi\|round-40'` → 4 ignored paths, plus the lane repo itself (and one *tracked* prompt file that names the round):
  | path | tracked? | mtime | content | attribution |
  |---|---|---|---|---|
  | `.ufo/state/inline-dispatcher.log` | untracked, ignored | 19:10:51 | 27 lines match kasegi-r40 | orchestrator dispatcher log (`spawn-cap`/`partial` lines for every lane) |
  | `.ufo/watchdog.log` | untracked, ignored | 19:07:47 | matches kasegi-r40 | orchestrator watchdog |
  | `.jj/working_copy/tree_state` | untracked, ignored | 19:08:06 | 104 `kasegi` path entries | jj snapshot state from the orchestrator's own publish (D7) |
  | `.ufo/state/kasegi.report-baseline` | untracked, ignored | 18:57:11 | `40 e3b0c442…b855` (round 40 + sha256 of the empty report) | orchestrator control state; same second as `kasegi-r40-falsify.ready` (18:57) |
  | `.ufo/prompts/kasegi-round-40.md` | **tracked**, clean | rewritten 18:57:11 with identical bytes | the round prompt | dispatcher; content-equal to HEAD, so not a stray |
- Content scan of every fleet-root file modified after 18:00 outside the lane/shokuknow (168 files scanned,
  `find -newermt -size -2M` + `grep -lE 'kasegi.*round-40|kasegi-r40'`) returned only the five paths above.
- **Conclusion**: nothing for the misroot sweep to delete. The four ignored files are live orchestrator state; a
  sweep that deletes them would break the dispatcher. No `kasegi-r40*` artifact sits in `/home/vgpnk/Projects/shokunin`
  outside the lane and `.ufo/`.

## 3. Item (2) — lane at J vs Y

**Tracked state**: `git status --porcelain --untracked-files=no` → empty (no modified, staged or deleted tracked
file; originals of the 5 commits `5e985b7..HEAD` = J1 `4766b9d`, J2 `bfca9ae`, J3 `8717b8b`, J4 `94abbff`,
J5 `3074c76`, linear, single-parent). `git status --ignored` in the lane → 0 ignored files.

**Untracked inventory at the final reading** (106 paths, `--untracked-files=all`): every path lies in the allowed
set —

| path class | count | expected? |
|---|---|---|
| `.ufo/waves/round-40/final-gates/all-gates.txt` | 1 | yes — this is the receipt that becomes Y (D1/D2) |
| `.ufo/waves/round-40/kasegi-r40-falsify.ready{,.dispatched}` | 2 | yes — control-plane markers; the *build* equivalents (`kasegi-r40-build.ready{,.dispatched}`) are already tracked at HEAD, so these two must be committed or removed before the "clean at filing" clause |
| `.ufo/waves/round-40/wave2/` receipts + fixtures | 103 | yes — wave-2 evidence; must be committed **before** the receipt (D2) or removed |
| anything else | **0** | — (an earlier reading at 22:15:41Z had 3 extra lane-root files; they were gone by 22:17 — D9) |

Verification that nothing else was touched: the untracked list contains no `corpus/`, no `SKILL.md`, no
`.ufo/waves/round-39/`, no sibling round dirs, and no file outside `.ufo/waves/round-40/`.

**Frozen artifacts intact** (attacks "the wave edited the claims or the controls"):
`git diff --quiet 5e985b7 HEAD --` for `claims.json`, `c1-controls/before.txt`, `c2-controls/before.txt`,
`c2-controls/junk-decisions.md`, `census-before.txt` → all **unchanged**; worktree `claims.json` == HEAD blob.
`grep -c '⟨pending' corpus/lessons/round-40.md` → `0` (C1 kill-rule clause satisfied).
`git merge-base --is-ancestor 5e985b7 HEAD` and `a7af2ce HEAD` → both true.

**Not yet satisfiable**: "lane working tree clean at filing" and "lane tip = Y". Both are closer actions, listed as
D1/D2 remediation. I did not delete, revert or commit anything.

## 4. Item (3) — wave-2 completeness (35-seat roster)

Roster source: `wave2-spec.json` (`items[].name`, 35 entries), cross-checked against
`wave2-dispatch.json`/`kasegi-r40-falsify.ready.dispatched` (same roster).

At 22:22:13Z: **33 / 35** `<seat>.md` present, **2 missing** (`MutH6H10`, `MutEntries` — both still running at the
reading), and **0 non-roster receipts** — the only extra `.md` files are fixtures with a seat
prefix (`CritKillRule.pending-variants.md`, `RevJunk.SOURCES-junk.md`), which the seat contract allows
(`<SEATNAME>.<suffix>`). All 33 present receipts carry the three-part contract (attacked item, command, verdict);
none is a stub (smallest 3,117 B; the largest is this file, ~34 KB; `RevJunk.SOURCES-junk.md` is a 90 KB fixture, not a receipt). Earlier readings in the same wave: 10/35 at 22:06:58Z, 20/35 at
22:12Z, 23/35 at 22:13:58Z, 27/35 at 22:15:41Z, 32/35 at 22:19:39Z — the wave is landing steadily, and the two missing
seats are mutation passes (H6–H10, entries), i.e. the heaviest. Wave-1 for comparison is complete:
**54 / 54** receipts, 142 files, all committed at HEAD.

**Closer requirement**: the wave is only complete when all 35 `<seat>.md` exist and each names an attacked item, the
re-run command and a reproduced/contradicted/defect verdict. A missing seat is not a harmless gap: the roster is the
wave's coverage map (C1 counters, C2 decisions/entries/rows, F23, junk, census, no-harm, mutations, sources re-open,
sibling, determinism, scratch, export cleanliness, fresh fetch, connector, sentinel), so a missing seat leaves the
matching claim limb attacked by nobody. This seat's own file is written last.

## 5. Item (4) — forbidden-path writes: no evidence of any

Paths in scope: `/home/vgpnk/Projects/shokunin/templates`, `/home/vgpnk/Projects/shokunin/scripts`,
`/home/vgpnk/Projects/shokunin/.ufo/state`, `/home/vgpnk/Projects/shokunin/.scratch`,
`/home/vgpnk/Projects/shokuknow`.

| check | command | result |
|---|---|---|
| receipt text (wave 1, 142 files) | `grep -rnE '(>\|>>\|tee\|cp \|mv \|rm \|sed -i\|truncate\|install )' wave1/*.md \| grep -E '<forbidden paths>'` | **0 hits**; the many path mentions are the read-only census invocation and explicit "never write there" clauses |
| receipt text (wave 2, 99 files) | same grep over `wave2/` | **4 text hits, 0 write verbs**: 3 are inside `RevJunk.SOURCES-junk.md` (lines 87/88/93), which I proved byte-identical to committed `corpus/SOURCES.md` (historical `used-by` notes saying "read-only the campaign package …"), and 1 is `ScoutSiblingFinal.md:88`, a read-only `rg` sweep for sibling-lane names. Every other match is a read-only `scripts/sources-census.sh validate` / `scripts/hyaku/disk-guard.sh status` invocation |
| fleet tracked files | `git -C …/shokunin status --porcelain` | empty |
| `templates/`, `scripts/` | `find … -newermt '2026-10-26 18:00'` | no file newer (newest `scripts/` entry 2026-10-25 23:26, `templates/` 2026-10-19 23:10) |
| `.scratch` | same find | only `goal-20261026-hyaku-run9.md` (19:08), which self-describes as orchestrator-owned run state in line 1 |
| `.ufo/state` | mtimes/content | only `kasegi.report-baseline` (18:57, orchestrator report baseline, not a defect) |
| shokuknow | content mtimes + index | no content write in window (D6) |
| PATH dir | `ls -lat ~/.local/bin` | no `git` shim; only orchestrator `omp` at 18:10 (D8) |
| lane | `git status --untracked-files=all` | every untracked path is in the allowed evidence set, with one **transient** exception I caught live (`h7row.tsv`, `pay.tsv`, `payloads.tsv` at the lane root for ~90 s — D9); no seat left a `corpus/` or top-level lane file behind |

Honest caveat: text greps prove what seats *reported*, not what they *did*; the physical checks above are the
independent half. They cover every forbidden path, but **not** a write that is created and removed between two
reads — D9 is exactly that class, and I only caught it because a snapshot happened to fall inside its 90-second
window. File contents (`mtime`) cannot distinguish "never written" from "written and cleaned"; only a live watcher
can, which is why D9's remediation is a post-wave assertion rather than a stronger grep.

## 6. Independent re-derivation of the C1 receipt at J (not by running the suite)

Method: `git archive HEAD | tar -x -C <scratch>/export` (7,932 files), then re-implemented the payloads from the
export bytes and read-only `git diff --numstat`. Script: `<scratch>/reexport_check.py` (not committed).

| check | receipt payload | independent re-derivation at J | verdict |
|---|---|---|---|
| H1 | `suite=1,digest=1,registry=1,registry-in=skill` | export suite sha256 `bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e`; `SKILL.md:1122` is the registry row, exact basename `\| r40-closure.sh \|`, digest prefix present | reproduced |
| H2 | `corrections=8,named=5,missing=0,fences=closed` | exact `h2_scan` semantics re-implemented in awk: `lines=8 named=5 closed`; all four files (`SCORECARD.md`, `LOG.md`, `SHONEN.md`, `corpus/lessons/round-39.md`) have out-of-fence `Correction (round 40)` lines; the corrected values are true of the r39 receipt (`closed=7/8 exit=1`, `selftest cases=8 failures=1` at `.ufo/waves/round-39/final-gates/all-gates.txt:17,79`) | reproduced |
| H3 | `mentions=1,rows=1` | `grep -cF M39-2 corpus/QUALITY.md` = 1 line (`:323`, R37 criterion row), 1 pipe-row | reproduced |
| H4 | `s056=1,s058=1,s059=1,oversize=0` | each id has a block with URL, `YYYY-MM-DD` access date, 2 located quotes, longest 20 words | reproduced |
| H7 shape | `header-lines=5,run-lines=10,body-lines=11,closed-0=0,closed-line=1,payload-match=9` | file is 16 lines: 5 header, 10 `H<n> payload=` lines, 1 `closed=`; exactly one H7 line; `export-ref` == J | reproduced (shape; semantics = H7's own re-run, delegated) |
| H9 | `declared=172,valid=172,tail=172,pure=1,paths=1` | 172 declarations, 172 tail-digests match, 172 numstat `add == lines`, 0 with deletions, 0 missing paths | reproduced (see D4 for the completeness caveat) |
| H10 | `skill-del=0,province-del=0,density=1,deleted=0` | `density.py` blob identical to base; `git diff --name-status base HEAD` has 0 `D` entries; `SKILL.md`/`PROVINCE.md` del=0; the only file with deletions is `corpus/SOURCES.md` (12/9, the registry edits) | reproduced |
| receipt identity | `export-ref=3074c767…` | sha256 `7b8cda36c793c5855fa6ffcb78d241fca47f0d3679b2d7c38f7a959042463484`, 1,062 B, `all-gates v4`, `run-utc=2026-10-26T21:56:22Z` == J `%ci` | reproduced |
| plain run refused | `exit 2` | `bash corpus/instruments/r40-closure.sh` → "refusing to run against the live worktree … export-mode only", exit 2 | reproduced |
| negative-control premise | base/r39 exports red | `git cat-file -e <base>:corpus/instruments/r40-closure.sh` → ABSENT; same for `8371e7ac…` → ABSENT (no suite to run, so `closed<10/10` by construction) | premise reproduced (the 10-check tally itself delegated) |
| `--work` guard, relative `--lane` | "`--work` inside the lane is refused" | in a fresh `git clone --no-hardlinks` of the lane (toplevel asserted), `cd <clone> && bash corpus/instruments/r40-closure.sh --export-ref <Y′> --lane . --work .` → **exit 2**, stderr `r40-closure: --work must be outside the lane (it would write there): <clone>/…`, **no file written** (`SentinelFinal.work-guard-refused.txt`); `main` canonicalises `LANE` before `make_work` (lines 1708–1710) | guard sound for this vector |
| selftest scratch root, in-tree | "moving `--work` inside/outside the scratch root does not change the transcript" (and no in-tree writes) | same clone: `--selftest --export-ref <Y′> --lane . --scratch-root .` → **exit 0**, `cases=10 failures=0` with 10 graded lines (`SentinelFinal.selftest-scratch-root-intree.txt`), and **0** suite-named entries created at the tree root | sound |
| `--work` guard, different `--lane` | — | code read: `make_work` compares only against `$LANE`; a `--work` resolving into the *real* lane while `--lane` names a fixture is accepted — live artefact set observed in the real lane (D9) | defect (D9) |

Byte-level check of the wave-2 evidence I leaned on: `LabDeterminismY.Y-run-a.txt`, `.Y-run-b.txt` and the receipt
are three files with the **same** sha256 `7b8cda36…` (`cmp` clean); the two `J-run` transcripts share
`0939d3f9…` (the documented 9/10 state). `CritReceiptForge.control-original.txt` and `.transcript-control.txt` are
byte-identical to the receipt, and each forged variant is a real one-line (or line-deletion) mutation — H1 payload
flipped to `suite=0,digest=0,registry=0`, `run-utc=2999-01-01T00:00:00Z`, foreign ref `8371e7ac…`, nonexistent ref
`0000…`, per-check lines stripped, `H7 payload=tampered`. The attack fixtures are genuine, not hand-written claims.

## 7. C2 counters re-run at J (claims `counting_commands`, verbatim)

| # | counter | before | required after | measured at J | verdict |
|---|---|---|---|---|---|
| 1 | queued among S016/17/19/20/21/22/23/24/25 | 9 | 0 | **0** | reproduced |
| 2 | mined among the nine | 0 | ≥4 | **7** | reproduced |
| 3 | knowledge entries citing the nine | 0 | == mined | **7** | reproduced |
| 4 | `S06[0-9]` registry rows | 0 | ≥1 | **3** | reproduced |
| 5 | entries citing `S06[0-9]` | 0 | ≥1 | **1** | reproduced |
| 6 | frontier rows in `corpus/README.md` | 22 | 23 | **23** | reproduced |
| 7 | `python3 corpus/instruments/frontier-recheck-count.py` | 25/25 | 26/26 exit 0 | **entries=26 pass=26 exit=0** (F23 `ids=S060`) | reproduced |
| 8 | `scripts/sources-census.sh validate --root … kasegi` | exit 0 | exit 0 | **exit=0**, same two `W04` lines as `census-before.txt` (S028/S029 duplicate URLs), no new W/E code | reproduced |

Captures backing the seven mined rows exist for exactly those seven ids
(`corpus/source-snapshots/round-40/{S016,S017,S019,S020,S021,S023,S025,S060}.txt`), and S022/S024 are the two
`superseded` rows, consistent with the frozen predicate. I did **not** re-fetch the upstream URLs in this seat (that
is `ScoutReopenNine`/`LabFreshFetch`/`CritSourceTruth`'s item); I only verified that the lane-side counting
commands are green at J.

## 8. What this seat did not verify (explicit boundary)

- H5, H6, H8 **as suite limbs against Y**: I did not run the Y selftest or the base/r39 nested runs (those are
  `RevC1Counters`/`RevC1Sandbox`/`MutH1H5`/`MutH6H10`). The one selftest I ran was a **guard probe** in a throwaway
  clone (`--lane . --scratch-root .`, §6), not a verification of the round-40 claims. I verified their premises and
  the receipt's recorded payloads only (D1, §6).
- Live source re-check of S016/17/19/20/21/23/25/060 (network) — other seats' item; I verified capture presence and
  the manifest binding path exists, not the fetch.
- Round-40 lesson content quality, Gate-block adequacy, capture-binding records, junk decision semantics —
  `RevH2Corrections`/`RevJunk`/`CritRecordsConsistency`/`CritC2Fabricate`'s items.
- I made no judgement on whether the round should be admitted; this receipt is evidence about the filed state.

## 9. Hygiene of this seat

- Deliverables: `wave2/SentinelFinal.md` (this file), `wave2/SentinelFinal.work-guard-refused.txt` (123 B, the
  exit-2 stderr of the `--lane . --work .` probe, sha256 `974fe1c1…`) and
  `wave2/SentinelFinal.selftest-scratch-root-intree.txt` (5,370 B, the probe's own stdout with `selftest cases=10
  failures=0` and 10 graded lines, sha256 `56374ae8…`). Both are byte-exact captures, not reconstructions.
- Scratch `/fast/scratch/hyaku/kasegi-r40/SentinelFinal/` — export (7,932 files), one analysis script, three probe
  transcripts and one throwaway `git clone` (toplevel asserted equal to the clone dir before the single fixture
  commit, identity `-c user.name=r40-fixture -c user.email=r40-fixture@local`) — is **removed before yield**
  (`rm -rf`; verified absent). Disk guard was green before the heavy pass (`/tmp` 3 %, `/fast/scratch/hyaku` 24 %);
  the export plus clone stayed well inside it.
- No tool installed or upgraded. No pacman. No network fetch (all checks read local bytes). Read-only git against the
  lane (`show/archive/ls-tree/rev-parse/diff/status`); the one plain `git status` against shokuknow at 19:07 is
  recorded in D6 rather than hidden. The only git mutation anywhere was the fixture commit inside my own clone; no
  mutating git/jj command ran against the lane, the fleet root, or any sibling.
