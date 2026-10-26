# RevSuiteDesign — wave-2 falsify review of the landed `r39-closure.sh` (C1, depth:verifiability)

seat: RevSuiteDesign (leaf; no spawns, one scratch dir, no lane writes)
lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (base `480b1a50`, freeze `dcd31701`)
axis: depth:verifiability
item: review the LANDED `corpus/instruments/r39-closure.sh` limb by limb against the frozen C1
predicate, and re-run the counting commands myself.
refs: J = `46c66c268502abd1b2c342fc71bf88ccf721845b`, Y = `5006097a84305267c9a3e8c1e1d560e60fe41d37`
(lane tip; `git diff --name-only J Y` = `.ufo/waves/round-39/final-gates/all-gates.txt` only —
verified), r38 judged head = `66703acaaff50529a35be49aa8759d04140720ad` (E2), base =
`480b1a505a2dfc14a4f718d16d63808247214d0a`.

## Verdict summary

- All eight G-limbs are **conformant** to the frozen predicate as spelled (per-limb evidence below);
  the 34-mutant selftest reproduces green at Y (`cases=8 failures=0`, all six forgeries rejected).
- All five frozen counting commands reproduce (with two mid-wave environment caveats, F3/F4).
- **One defect found (F1):** the committed receipt `all-gates.txt` carries a G6 payload line that the
  pinned suite bytes cannot produce. The receipt is the round's central C1 artifact, and it passed
  G2 — the gap that lets it pass is documented but this is a landed instance of it.
- Two minor notes (F2 erratum-number drift, F3 §2.7 provenance claim), one environment observation
  (F4 live-lane G8).

## 0. Byte identity (precondition)

- `sha256sum corpus/instruments/r39-closure.sh` =
  `2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b` = the `suite-sha256=` pinned in
  the committed `all-gates.txt` = `wave1/ExecSuiteBuild.r39-closure.sh` (built == landed, `diff`
  clean). Read the full landed file (1793 lines) before judging.

## 1. Runs I executed (all output captured verbatim; scratch removed after)

| # | command (abridged) | rc | result |
|---|---|---|---|
| R-Y-green | `r39-closure.sh --export-ref Y --lane <clean clone of lane at Y> --scratch-root $S/scr --work $S/scr/kasegi-r39/work` | 0 | `closed=8/8 exit=0`; prints `deviation=non-default --lane` + `deviation=non-default --scratch-root` |
| R-Y-lane | same but real `--lane` (default), private `--scratch-root` | 1 | `closed=7/8 exit=1` — only G8 red (`r37-closed=0,r37-exit=1`); see F4 |
| R-Y-live | same, default scratch root (no flags beyond `--export-ref Y --work`) | 1 | `closed=6/8 exit=1` — G6 red `r39=present … tolerated=none` (≈30 live wave-2 sibling scratch dirs, mine included); fail-closed as designed |
| R-selftest | `--selftest --export-ref Y --lane <clone> --scratch-root $S/scr3 --work $S/scr3/kasegi-r39/work` | 0 | 8 graded case lines: mutants 4/4, 8/8, 2/2, 6/6, 4/4, 4/4, 3/3, 3/3 (34/34 rejected, each naming its limb); `selftest cases=8 failures=0`; `judge=own-report accepted=1`; all six forged reports `rejected=1` |
| R-J | `--export-ref 46c66c2…` (real lane, private root) | 1 | `closed=6/8 exit=1`, `G2 payload=receipt=0 …` (E4's expected J-run red; count differs from E4's prose — F2) |
| R-base | `--export-ref 480b1a5…` | 1 | `closed=2/8 exit=1` (matches wave-1 §2.3: G3+G6 green, rest red) |
| R-r38 | `--export-ref 66703acaaff5…` (40-char) | 1 | `closed=2/8 exit=1` |
| R-r38-37 | `--export-ref 66703aca5052…` (37-char, as-frozen text) | 2 | `cannot resolve export ref …` — E2's harness-error explanation reproduces |
| R-plain | `r39-closure.sh` | 2 | `refusing to run against the live worktree` |

The clean clone (`git clone --no-hardlinks` into scratch, detached at Y, `status --porcelain` = 0
lines) is only an environment isolator for G8's live limbs; every ref-scoped read (G1 numstat, G2
ancestry/diff, G3 added-lines, G8 `git show`) reads the same objects. In the clone run the seven
real-tree payload lines G1,G2,G3,G4,G5,G7,G8 are **byte-identical** to the committed receipt.

## 2. Per-limb review (frozen predicate → landed implementation)

- **G1 whole-tail declarations — conformant.** `declared-blocks.txt` (`PROVINCE.md 2 fa2dd99f…`,
  `corpus/README.md 28 a59d42cc…`) verified independently: `git diff --numstat base Y` = 2/0 and
  28/0; `tail -n 2` of Y's PROVINCE.md hashes to `fa2dd99f…` exactly. Implementation: tail-sha
  equality, `lines == numstat-added`, `deleted == 0`, plain-relative path check (no `/`-root, `..`,
  empty component — the round-38 G1-H4 escape), both front doors required, malformed/short
  declarations fail via `valid == declared`, backtick+tilde fence walk must end CLOSED, corrections
  counted only at line start and outside fences, inside-fence correction reds
  (`corrections-inside`), counted correction must sit inside the declared tail. Selftest reopens
  exactly these: short tail → `valid=0`; tilde opener closed by backticks → `readme-fence=open`;
  correction-in-fence → `corrections-inside=1`; `../` declaration → `paths=0`; green control
  accepted. Documented spelling limits (4-backtick closer does not close; mid-line corrections
  uncounted) match the contract's fence spelling.
- **G2 graded receipt — conformant.** Sentinel line 1 `all-gates v3`; exactly one
  `export-ref=<40hex>` (exists, `merge-base --is-ancestor`, `diff --name-only` = receipt only);
  exactly one `suite-sha256` equal to executing bytes AND export copy; exactly 8 distinct
  `^G[1-8] payload=… closed=1$`, zero `closed=0`; exactly one `^closed=8/8 exit=0$`; case grading
  requires BOTH `positive=pass` and `verdict=pass` as exact whitespace/comma-delimited tokens on
  `^selftest case=G[1-8]( |$)` lines (summary-only → `graded-cases=0`, verdict=fail → 7, seven
  cases → 7 — all three rejected); exactly one `selftest cases=8 failures=0`; SCORECARD `## Round 39`
  section + SHONEN round-39 lines carry the judged-head phrase and zero `Final lane commit:`.
  Known, documented gap (see F1): payload **values** inside the receipt are not cross-checked
  against a live run.
- **G3 committed-run truth — conformant.** Added (`+`) lines of `base..ref` over
  SCORECARD/SHONEN/LOG/round-38.md quoting `closed=` plus an `--export-ref <7-40hex>` token need the
  literal `report-only` on the line or the ref inside a committed file under
  `.ufo/waves/round-39/final-gates/`. I diffed base..J myself: exactly one added line in scope (the
  round-38-claims correction); it contains `--export-ref J` (no hex token) and `export-ref-run:`
  prose, so `added-quotes=0` is honest, not a bypass — the line documents that the old quotes were
  NOT runs. Base lines exempt as frozen E5.6 says. Selftest: transcribed control accepted; quote
  without transcript and transcript-outside-final-gates both `uncovered=1`.
- **G4 seat identity — conformant.** Every tracked `*-dispatch.json` (Y export: exactly
  `wave1-dispatch.json`, `dispatches=1`): results sibling `<base>-results.json` or
  `<wave>-results.json` with matching `wave`; JSON must parse (unparseable dispatch or results →
  `pairs<dispatches` red); `results == len(taskCall.tasks)`; identity = first of
  id/name/seat/agent present in every entry, must be distinct; zero-task dispatch red (not 0==0).
  Selftest: 6 mutants (absent, dup, short, zero-task, badjson, wave-mismatch) all rejected on named
  limbs. Documented limit (distinct-but-wrong names) is the frozen predicate's own wording.
- **G5 label drift — conformant** (split with G2, no gap). G5: `## Round 39` section exists, zero
  `Final lane commit:` in it, ≥1 line-initial `Correction (round 39)` naming `f06148c6` labeled
  `report-only` (live: `correction=2,correction-labeled=1`). The frozen predicate's SHONEN half of
  the zero-label limb is enforced by G2's `final-lane-commit` count over SHONEN round-39 lines —
  both must be closed=1 for 8/8, so removing either does not open a hole. Selftest: final-label,
  no-correction, unlabeled, no-section all rejected.
- **G6 scratch quiescence — conformant, genuinely fail-closed.** `kasegi-r37`/`kasegi-r38` absent or
  zero-entry; `kasegi-r39` absent/empty or holds only this run's `--work` (realpath-judged) or a
  clean chain toward it; unreadable root → `read=fail` red, never silent zero. Measured three ways:
  default root red (`r39=present`, live siblings); private root green (`r39=empty, tolerated=<work>`);
  selftest rejects r37-file, r38-seat, r39-parent-sibling, chmod-000 root, and accepts own-work-dir
  and nested-clean-chain controls.
- **G7 ledger fill — conformant.** `## Round-39 dispositions (appended 2026-10-26)` strictly after
  `## Round-37 dispositions — filled (round 38)`; line-initial `Correction (round 39)`; ≥3
  numeric-first-cell rows including proposals 1 and 3, with the `1x`≠1 guard. Live: `rows=7,
  proposal-1=1, proposal-3=1, correction=1` (E5.5 wants ≥2 — satisfied). Selftest: drop-3,
  no-correction, section-before-round-38 rejected.
- **G8 pinned carry-over — conformant.** `git show 2387dcf6:…/r37-closure.sh` must hash to
  `0da98e37…`; export's own r37 copy must hash the same BEFORE it is trusted; pinned bytes then run
  `--export-ref REF --lane LANE` and must end `closed=14/14 exit=0` (verified live in the clone
  run). Selftest: mutated export copy, absent copy, and pinned-run-over-non-HEAD-ref all rejected.

## 3. Findings

**F1 — defect (records integrity, the R2 class inside the round's own artifact; medium).**
`corpus/instruments/r39-closure.sh` at digest `2856a210…` (the digest the receipt itself pins)
cannot print the committed G6 line:

- committed: `G6 payload=r37=absent,r38=absent,r39=present,work=inside,tolerated=/fast/scratch/hyaku/kasegi-r39/gates-work,read=ok closed=1`
- check_g6 (read verbatim, lines 870-920) returns success only for `r39` ∈ {absent, empty}; any
  `r39=present` path returns 1. Every tolerated-only listing leaves `r39=empty` — my green run
  printed `r39=empty,work=inside,tolerated=<work>,read=ok closed=1`; every `r39=present` run prints
  `closed=0` (measured: R-Y-live; also wave-1's own transcript `ExecSuiteBuild.md` §2.5:
  `r39=present … tolerated=none … closed=0`).

So the committed receipt asserts a live-scratch observation (`r39=present` alongside a green
verdict and a `tolerated=` path) that no run of these bytes could have produced. The other seven
payload lines reproduce byte-exactly from a real Y-run (my R-Y-green), so the receipt was clearly
regenerated on the real lane after the fixture proof and its G6 line is mis-transcribed/fabricated.
It passes G2 because G2 (by its own documented design) does not compare payload values across runs.
**Not a kill**: the frozen counting commands all hold on live reruns. **Ask to L1**: regenerate
`all-gates.txt` from an actual clean-tree Y-run at filing (G6 will then honestly print
`r39=empty`/`absent`), and consider a small G2 hardening: when `closed=1`, a G6 payload with
`tolerated=` must not claim `r39=present` (payload self-consistency), which would have caught this.

**F2 — minor (erratum number drift).** E4 says the J-run prints `closed=7/8`; measured **6/8**
(R-J): G2 red (`receipt=0`) AND G8 red, because the pinned r37 suite's live head limb requires lane
HEAD == the run's ref (HEAD is Y ≠ J). E4's operative content (J-run is expected red with
`receipt=0`, not a kill) is unaffected; the printed number is wrong by one.

**F3 — minor (wave-1 provenance claim false).** `wave1/ExecSuiteBuild.md` §2.7 states the receipt
committed at Y carries G lines "byte-identical to the live run" (the J'/Y' fixture run). The
committed receipt's G lines differ from that fixture run (G1 `corrections-outside` 0 vs 1, G3
`added-quotes` 0 vs 1, G5 `correction` 2 vs 1, G7 `rows` 7 vs 4, G6 entirely) — the byte-identity
verification cannot have been run against the committed bytes. Combined with F1 this means the
receipt's provenance is: real-lane rerun for 7 lines + an unproducible G6 line.

**F4 — environment observation, no defect (flag for filing).** Against the raw lane at Y mid-wave,
the counting command prints `closed=7/8` — G8's pinned r37 run reds on `git status --porcelain`
seeing the untracked wave-2 artifacts (`wave2-dispatch.json`, `wave2/`, `*.ready*`). Same for G6 on
the default scratch root while sibling seats hold scratch. Both are the suite's fail-closed live
limbs working as designed; the frozen 8/8 requires, at filing, lane HEAD == Y with a clean tree and
no leftover seat scratch — which the kill rule already demands of the L1.

**E5.1 wording note (no defect).** E5.1 asks graded case lines to carry `mutants=n/n, n>=1` and
"non-empty `payload=` fields"; the suite puts `payload=` on the positive/control detail lines and
`limb=` on rejection details, and its judge rejects `mutants=0/0` forgeries and requires n matching
detail lines per case. Intent (no vacuous passes) is satisfied; the literal reading (payload on the
case lines themselves) matches no implementation and no committed receipt line.

## 4. Kill-rule status (C1)

- suite present and executed from the landed path — hold.
- judged-head(Y) export `closed=8/8 exit=0` — reproduces on a clean tree (R-Y-green); raw-lane
  mid-wave 7/8 is F4's environment state, resolves at filing.
- selftest ≥8 graded lines, no failure, summary-only never satisfies — reproduces (R-selftest).
- base and r40-char-r38-head exports red (2/8), 37-char spelling exit 2 (E2) — hold.
- no committed fixture passing with its defect present — the selftest's 34 mutants all rejected at
  Y; not contradicted by anything I ran.
- `grep -c '⟨pending' corpus/lessons/round-39.md`, clean-tree-at-filing, scratch-quiescence-at-filing
  — L1 filing-time items; current untracked wave-2 files and live scratch noted in F4.

## 5. Tooling and scratch

No tool installed or upgraded (bash, git, awk, grep, sha256sum, sed, python3 sufficed). No pacman
transaction. No lane file written except this receipt; no mutating git command anywhere (clone and
fixtures read-only from the lane; clone toplevel asserted). Scratch
`/fast/scratch/hyaku/kasegi-r39/RevSuiteDesign` (clone, work dirs, run outputs) removed before
yield.

Report: .ufo/waves/round-39/wave2/RevSuiteDesign.md
