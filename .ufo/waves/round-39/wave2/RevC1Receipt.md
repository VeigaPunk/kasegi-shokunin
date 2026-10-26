# RevC1Receipt — round-39 wave 2 (falsify): C1 receipt + J/Y review

seat: RevC1Receipt (reviewer, leaf; no spawns). I am not an author of any deliverable under attack.
item: the round-39 final-gates receipt (`.ufo/waves/round-39/final-gates/all-gates.txt`) and the J/Y
relationship; the reds; the J-run and Y-run verification (erratum E4).
lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` · base `480b1a505a2dfc14a4f718d16d63808247214d0a`
· freeze `dcd31701720a6a4929a32471a62011ed87103421`
J = `46c66c268502abd1b2c342fc71bf88ccf721845b` (all-gates.txt:2 `export-ref=`)
Y = `5006097a84305267c9a3e8c1e1d560e60fe41d37` (lane tip at review time)
suite digest = `2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b`
scratch: `/fast/scratch/hyaku/kasegi-r39/RevC1Receipt` (removed before yield). Disk guard green at
start (`df -h /fast`: 24% used, 616G avail). No tools installed (bash/git/coreutils sufficient; no
pacman transaction, no network fetch). No mutating git command anywhere: two read-only
`git clone --no-hardlinks` of the lane into my own scratch (`rev-parse --show-toplevel` asserted
equal to each clone dir before any git write inside them) and one `checkout --detach` INSIDE my
scratch clone for the HEAD=J control. The lane itself was only ever read.

## Verdict

**C1 holds as frozen: every behavioral claim of the suite reproduces under independent re-run, and
the receipt is structurally exact and digest-bound. One material defect lands on the receipt itself:
its G6 payload line is not producible by the bytes it binds to (F1).** Seven of the eight G-lines are
byte-identical to a fresh run of the bound bytes; G6 is the one limb that attests live host state,
and its line in the receipt names a state (`r39=present`) that the bound code always closes RED.
No C1 kill-rule limb fires on my evidence. F2–F7 are wording/coverage notes.

## 1. J/Y structure — PASS

| check | command | result |
|---|---|---|
| J is a commit | `git cat-file -t 46c66c26…` | `commit` |
| J ancestor-or-equal of tip | `git merge-base --is-ancestor J 5006097a…` | ok (`ancestor-ok`) |
| diff scope | `git diff --name-status J Y` | `A  .ufo/waves/round-39/final-gates/all-gates.txt` (single path, added) |
| diff count | `git diff --name-only J Y \| wc -l` | `1` |
| no file at J names J | `git grep -c 46c66c26… 46c66c26… --` | empty (exit 1) |
| no file at J names J short-form | `git grep -c 46c66c26 46c66c26… --` | empty (exit 1) |
| at Y only the receipt names J | `git grep -n 46c66c26… 5006097a… --` | `…all-gates.txt:2:export-ref=46c66c26…` only |
| Y does not name itself | `git grep -c 5006097a… 5006097a… --` | empty (exit 1) |
| receipt committed, not dirty | `git show HEAD:…all-gates.txt \| cmp - <worktree file>` | identical |

## 2. Receipt shape — PASS (every count exact)

Run against `.ufo/waves/round-39/final-gates/all-gates.txt` (1.7KB, 24 lines):

| limb | command | result |
|---|---|---|
| header | line 1 | `all-gates v3` |
| G-lines | `grep -cE '^G[0-9] payload='` | `8` |
| distinct ids | `grep -oE '^G[0-9]' \| sort -u \| wc -l` | `8` |
| zero red lines | `grep -cE 'closed=0'` | `0` |
| headline | `grep -cE '^closed=8/8 exit=0$'` | `1` |
| export-ref | `grep -cE '^export-ref='` / `…^export-ref=[0-9a-f]{40}$` | `1` / `1` |
| suite-sha256 | `grep -cE '^suite-sha256='` | `1` |
| case lines | `grep -cE '^selftest case='` | `8` |
| graded pass | `grep -cE '^selftest case=G[0-9] .*positive=pass .*verdict=pass'` | `8` |
| no 0/0 mutants | `grep -cE 'mutants=0/0'` | `0` |
| summary | `grep -cE '^selftest cases=8 failures=0$'` | `1` |

Digest binding: `sha256sum corpus/instruments/r39-closure.sh` (executing bytes) =
`git show HEAD:…r39-closure.sh | sha256sum` = `git show 46c66c26…:…r39-closure.sh | sha256sum` =
`2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b` = the receipt's `suite-sha256=`
line. The suite computes the digest from the executing bytes (`suite_digest()`,
r39-closure.sh:230-234) and G2 requires it to equal both the executing bytes and the export's own
copy (r39-closure.sh:708-711) — no self-printed forgery path.

## 3. Suite re-runs — every behavioral claim reproduces

Method: R1–R4 run against a clean `git clone --no-hardlinks` of the lane at Y (`clone-y`,
toplevel asserted, HEAD=Y, `status --porcelain` empty) because G8 executes the pinned r37 suite,
whose E9 limb (b) counts ALL `git status --porcelain` lines (r37-closure.sh:581-605) and the real
lane currently carries 5 untracked wave-2 runtime files; R5/R6 run against the real lane exactly as
the committed transcripts did. Every run: `TMPDIR` under my scratch, `--work` under my scratch,
`--scratch-root` isolated unless noted. All runs of the bound bytes (digest `2856a210…`).

**R1 — `--export-ref Y` → `closed=8/8 exit=0` (the receipt's headline).** Full output:

```
export-ref=5006097a84305267c9a3e8c1e1d560e60fe41d37 mode=export lane=…/RevC1Receipt/clone-y suite-sha256=2856a210…
deviation=non-default --lane
deviation=non-default --scratch-root
G1 payload=declared=2,valid=2,front-doors=2,tail-match=2,pure-append=1,paths=1,province-fence=closed,readme-fence=closed,corrections-outside=0,corrections-inside=0,corrections-declared=1,diff-read=ok closed=1
G2 payload=receipt=1,sentinel=1,export-ref=1,ancestor=1,diff-clean=1,diff-read=ok,digest-match=1,export-suite=1,run-lines=8,closed-lines=0,distinct-ids=8,closed-line=1,graded-cases=8,ungraded-cases=0,selftest-summary=1,scorecard-ref=1,shonen-ref=1,final-lane-commit=0 closed=1
G3 payload=added-quotes=0,covered=0,uncovered=0,report-only=0,diff-read=ok closed=1
G4 payload=dispatches=1,pairs=1,seats-ok=1,zero-task=0,read=ok closed=1
G5 payload=round39-section=1,final-lane-commit=0,correction=2,correction-labeled=1 closed=1
G6 payload=r37=absent,r38=absent,r39=empty,work=inside,tolerated=…/RevC1Receipt/g6root/kasegi-r39/work,read=ok closed=1
G7 payload=section=1,after-round38=1,correction=1,rows=7,proposal-1=1,proposal-3=1 closed=1
G8 payload=pin-ref=2387dcf6ccfefcfb703783387b9aade8fc82abfa,pinned-sha=1,export-copy=1,r37-copy=1,r37-closed=1,r37-exit=0 closed=1
closed=8/8 exit=0
```

`diff` of my G-lines vs the receipt's G-lines: **only G6 differs** (live-state values; both
`closed=1`). G1, G2, G3, G4, G5, G7, G8 are **byte-identical** to the receipt. A second clean-root
shape (work nested one level deeper) also printed `closed=8/8 exit=0`.

**R2 — `--export-ref J`, lane HEAD=Y → `closed=6/8 exit=1`.** G2 `receipt=0` (every receipt limb 0)
AND G8 `r37-closed=0,r37-exit=1` — the pinned r37 suite's E9 head-match limb (lane HEAD Y ≠
export-ref J). Matches ExecSuiteBuild.md §4 row 2 exactly.

**R3 — `--export-ref J`, lane HEAD=J (scratch clone detached at J, toplevel asserted, clean) →
`closed=7/8 exit=1`.** G2 `receipt=0` with G8 GREEN (`r37-closed=1,r37-exit=0`). **This is E4's
literal form, verified**: a run at J prints 7/8 with G2 receipt=0 when the lane is checked out at J.

**R4 — `--selftest --export-ref Y` → exit 0, `selftest cases=8 failures=0`.** Eight graded case
lines **byte-identical to the receipt's** (`diff` empty); judge limb: `selftest judge=own-report
accepted=1` plus six forged reports each `rejected=1`. (Two stderr noise lines from the G6 mutant
fixtures — `cd: … Not a directory`, `find: … Permission denied` — are the suite's no-suppression
policy exercising its own fail-closed mutants; harmless.)

**R5 — base red `--export-ref 480b1a505a2dfc14a4f718d16d63808247214d0a` (real lane) → `closed=2/8
exit=1`, byte-identical (`diff` empty) to the committed transcript
`wave1/ExecSuiteBuild.overlay/run-at-base.txt`** (G3+G6 green; G1/G2/G4/G5/G7/G8 red).

**R6 — r38-head red `--export-ref 66703acaaff50529a35be49aa8759d04140720ad` (real lane) →
`closed=2/8 exit=1`, byte-identical to `run-at-r38head.txt`.**

**R7 — the frozen 37-char spelling `--export-ref 66703aca50529a35be49aa8759d04140720ad` → exit 2**
(`cannot resolve export ref …: 66703aca50529a35be49aa8759d04140720ad`) — E2's harness-error form,
matching §2.4's record; `git cat-file -t` on it: `fatal: Not a valid object name`.

**R8 — plain run → exit 2** with the exact §2.2 refusal text; no work dir created (`/tmp/r39-closure.*`
count 0).

**R9 — `--work` inside the lane → exit 2** (`--work must be outside the lane (it would write there)`);
the probe path was absent after the run (guard fires before any creation).

**R10 — live G6 (default scratch root, clone lane) → `closed=7/8 exit=1`** with
`G6 payload=r37=absent,r38=absent,r39=present,work=inside,tolerated=none,read=ok closed=0` — the
live limb reds on the in-flight wave-2 scratch root (14 entries under `/fast/scratch/hyaku/kasegi-r39`).
Confirms G6 is live and that the receipt's 8/8 required the then-clean root.

## 4. Independent limb checks (not trusting the suite)

- **G1 whole-tail**: `.ufo/waves/round-39/declared-blocks.txt` declares exactly 2 blocks
  (`PROVINCE.md 2 fa2dd99f…`, `corpus/README.md 28 a59d42cc…`); `git diff --numstat base Y` over
  those paths = `2 0` and `28 0` (added == declared, deleted == 0); `tail -n <n> <path> | sha256sum`
  matches both declared digests. Whole-tail verified without the suite.
- **G2/G5 text limbs**: the phrase `judged head: export-ref of
  .ufo/waves/round-39/final-gates/all-gates.txt` at SCORECARD.md:1567 (inside `## Round 39`) and
  SHONEN.md:202; `Final lane commit:` count in the SCORECARD Round-39 section = 0.
- **G4 seat identity**: `wave1-dispatch.json` `wave=kasegi-r39-build`, `taskCall.tasks`=49;
  `kasegi-r39-build-results.json` `wave=kasegi-r39-build`, `seats`=49, `results` list len 49,
  **49 distinct identities, 0 missing**; only `wave1-dispatch.json` matches G4's direct-child glob
  (the G4 fixture dispatch/results pairs are nested under `wave1/…fixtures/…` and do not match).
- **G7 ledger**: `## Round-39 dispositions (appended 2026-10-26)` at ledger line 69 (after the
  round-38 section), 1 `Correction (round 39)` line, 7 proposal rows (1 and 3 present; ≥2 per E5.5).
- **Kill-rule limbs checkable now**: `grep -c '⟨pending' corpus/lessons/round-39.md` = 0; tracked
  tree clean (`git status --porcelain -uno` empty; 5 untracked wave-2 runtime files — see F3);
  `kasegi-r37`/`kasegi-r38` absent under `/fast/scratch/hyaku` (kasegi-r39 entries are in-flight
  seats — a filing-time item for the L1, not mine).

## 5. Findings

**F1 — MATERIAL (transcript integrity of the receipt): the G6 payload line is not producible by the
bytes the receipt binds to.** The receipt (all-gates.txt:10) reads:

```
G6 payload=r37=absent,r38=absent,r39=present,work=inside,tolerated=/fast/scratch/hyaku/kasegi-r39/gates-work,read=ok closed=1
```

The bound bytes (digest `2856a210…` = worktree = HEAD = J blob) implement `check_g6`
(r39-closure.sh:870-918): `r39` becomes `present` only for non-tolerated entries (lines 895, 902,
905, 912) and the return gate is `if [ "$r39" = absent ] || [ "$r39" = empty ]; then return 0; fi`
(line 917) — **`r39=present` always returns 1 → `closed=0`**. The suite's own selftest mutant
`r39-parent-sibling-leftover` (line 1574) expects rejection with limb `r39=present`. Measured matrix
with the bound bytes, all four shapes: clean root + work as direct child → `r39=empty … closed=1`
(R1); clean root + deeper clean chain → `r39=empty, tolerated=<parent> … closed=1`; any residual
entry → `r39=present … closed=0` (R10; the committed §2.5 transcript shows the same with
`tolerated=none`); mixed (chain parent tolerated + a residual sibling) → `r39=present,
tolerated=<parent> … closed=0`. **No run of these bytes can print `r39=present` with `closed=1`.**
The suite landed in a single commit (1a139e0; no earlier build is committed), so the line's origin
is either an uncommitted scratch iteration or hand-composition with a state-name slip (the final
code names the clean-with-tolerated-work state `empty`; §2.5's residual line uses `present`).
Impact: G2 cannot catch it — payload VALUES are not compared (suite header, documented limit: "The
cross-run payload VALUE comparison is not a limb"). The receipt's other seven G-lines ARE
byte-identical to a fresh run (R1), so the defect is isolated to G6 — the one limb that attests LIVE
host state at filing. The receipt is therefore not the single-run transcript of the bytes its
`suite-sha256=` names. Not a kill under the frozen kill rule as I read it (the "committed fixture
shows a check passing while its defect is present" clause targets the selftest fixtures, and all
suite verdicts reproduce) — but note the sharp edge: read with the final code's state semantics, the
receipt's G6 line names the defect state with `closed=1`; if a judge reads the receipt itself as
such an artifact, that clause fires. Smallest correction (L1's call, not mine): regenerate the
receipt's G6 line from a final-bytes run (a clean-root run prints `r39=empty`), or re-run at final
filing with the real root after scratch cleanup and re-commit the receipt as the new tip's +1 (the
J/Y dance repeats mechanically).

**F2 — MINOR (erratum E4 wording).** E4 says "A run at J prints `closed=7/8 exit=1` with the G2
payload `receipt=0`" and "documented in the receipt". Measured: 7/8 requires the lane checked out AT
J (R3); with the lane at the tip Y — the state any re-run at filing sees — the J-run prints **6/8**
(G2 `receipt=0` AND G8 red via the r37 suite's E9 head-match limb), exactly as ExecSuiteBuild.md §4
row 2 documents. The substance of E4 (G2 `receipt=0`, exit=1, expected, not a kill) holds in both
forms. Also, the committed r39 receipt contains NO J-run record — the J-run documentation lives in
wave1/ExecSuiteBuild.md §4 (fixture repo) and now in R2/R3 here; E4's "documented in the receipt"
points at a receipt that carries no such record. (The suite header's green-window sentence "at J …
prints `closed=7/8`" has the same condition-dependence.)

**F3 — MINOR (scratch-coverage gap).** G6 scans only `kasegi-r37`/`kasegi-r38`/`kasegi-r39` under
the scratch root, and the kill rule says "any leftover kasegi-r37/r38/r39 scratch entry at filing".
The L1's own scratch root `/fast/scratch/hyaku/kasegi-r39-l1` (15 entries right now) is invisible to
both — a residual under a sibling-named root cannot trip the guard. Likewise
`/fast/scratch/hyaku/kasegi-r39/gates-work` (8 entries) still exists — the L1's own gate-run work
dir; it IS under kasegi-r39, so it must be removed before the L1's final filing (in-flight now; not
mine to clean).

**F4 — OBSERVATION (erratum E5.2 wording vs landed G1).** E5.2's literal text ("if a file gained
lines since base, its declaration must be present and exact") is broader than the landed G1, which
requires ≥1 declaration per front door and whole-tail exactness for DECLARED blocks only. At Y many
files gained lines since base (QUALITY +16, SOURCES +4, LOG/SCORECARD/SHONEN/round-38/ledger
appends, new files) with only 2 declarations; under E5.2's literal reading G1 would be red. The
frozen C1 predicate (authoritative) matches the landed implementation and no kill-rule limb covers
declaration coverage — no kill — but E5.2's wording should be scoped (to the front doors / declared
files) to avoid a future reader expecting whole-tree declaration coverage.

**F5 — OBSERVATION (the receipt is a formatted transcript, not raw stdout).** The suite's run header
prints `export-ref=<hash> mode=export lane=<lane> suite-sha256=<digest>` on ONE line
(r39-closure.sh:990-991); the receipt splits it into bare `export-ref=`/`suite-sha256=` lines and
adds an authored `run-utc=` line; the selftest section keeps only the 8 graded case lines + summary
(the raw selftest also prints `selftest detail=` lines and 7 `selftest judge=` lines — preserved in
the committed wave1 transcripts, e.g. `overlay/selftest-at-Y.txt`). G2's own regexes
(`^export-ref=[0-9a-f]{40}$`) REQUIRE the bare form — a raw stdout paste would red G2's export-ref
limb — so the format is by construction; the binding to the live run rests on the G-lines/case-lines
being byte-identical (verified: R1/R4 here; §2.7's diff for the fixture receipt, whose G-lines match
its own live run byte-for-byte). The suite header's "the receipt is the run's own transcript" should
not be over-read.

**F6 — OBSERVATION (vacuous G1 boolean, visible).** `corrections-declared=1` with
`corrections-outside=0`: the containment boolean is vacuously true (the front doors carry zero
`Correction (round 39)` lines at Y). The payload prints `corrections-outside=0` alongside, so the
vacuity is visible rather than hidden; E5's non-vacuous spirit is met by the paired key.

**F7 — OBSERVATION (G3's transcript dir excludes the round's own reds).** G3 accepts transcripts
only under `.ufo/waves/round-39/final-gates/`, but the round's red-run transcripts live at
`wave1/ExecSuiteBuild.overlay/run-at-base.txt` and `run-at-r38head.txt` (the r38 precedent kept a
`final-gates/reds.txt`). Vacuously green today (`added-quotes=0`; the R2 correction lines quote
`closed=` values with bare hashes and `--export-ref J` — no `--export-ref <hex>` token — so they do
not trip G3), but a future quote of the base/r38 reds in the token form would red even though the
transcripts exist one directory over.

## 6. Coverage and gaps

Verified end-to-end: J/Y git structure; receipt shape (every count); digest binding (worktree =
HEAD = J = receipt); all eight G-lines against a fresh run (seven byte-identical, G6 by matrix);
selftest at Y (graded lines byte-identical, judge limb); both J-run forms (7/8 at HEAD=J per E4,
6/8 at HEAD=Y per §4); both required reds byte-identical to their committed transcripts; the 37-char
harness error; the plain-run and work-in-lane refusals; the live G6 limb; independent G1/G2/G4/G7
limb checks; the pending-marker kill limb. Not verified (out of my item): the 34 selftest mutants
limb-by-limb (MutSuiteLimbs's assignment; my R4 confirms the aggregate verdict), C2 counters
(RevC2Recheck/CritBaseControl), the L1's filing-time kill limbs that depend on final-filing state
(scratch cleanup, tree cleanliness at filing).

## 7. Tooling and scratch

No tool installed or upgraded (bash, git, coreutils sufficient; no pacman transaction, no uv/npx, no
network fetch). Scratch `/fast/scratch/hyaku/kasegi-r39/RevC1Receipt` held two clean clones of the
lane (`clone-y` at Y, `clone-j` detached at J; toplevel asserted for both), G6 isolation roots
(`g6root`, `g6root2`, `clean-root`), work dirs and run captures (`out-*.txt`); removed before yield.
No lane, fleet, sibling-lane or source-tree file was written except this receipt.

## Report

.ufo/waves/round-39/wave2/RevC1Receipt.md
