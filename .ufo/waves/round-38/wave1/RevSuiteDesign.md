# RevSuiteDesign — round-38 receipt (C1 suite-contract false-green review)

Seat: RevSuiteDesign (reviewer, leaf, no subagents). Item: review the C1 suite contract for false
greens; when `.ufo/waves/round-38/wave1/ExecSuiteBuild.r38-closure.sh` appears (poll ≤3 times,
5 min apart), review it against the list and run it on a base export. Receipt only — no deliverable
files named by my item.

## Timeline (polls, UTC)

- poll 1 ~18:34Z — `glob wave1/*` — suite absent.
- poll 2 ~18:37Z — `ls ExecSuiteBuild.r38-closure.sh` — absent.
- poll 3 ~18:41:30Z (backgrounded `sleep 240; ls`) — absent.
- suite mtime **18:41:32Z** (`stat -c %y` → `2026-10-26 15:41:32.80 -0300`); present at my next
  command 18:41:38Z. Reviewed from there — the conditional triggered 2 s after the last poll.

## What I read / ran

- `corpus/instruments/r37-closure.sh` (committed model) — read in full (1558 ln): export/work-dir
  guards, cleanup trap, `suite_digest()`, fail-closed `--no-optional-locks` status read
  (L579-599), E10 cross-run key-set limb (L687+), `judge_selftest_report` + 6 forged probes
  (L1396-1500), E9's `find -type d` scratch limb (L599).
- `corpus/lessons/round-37-verifier-spotcheck.md` §5 (D-A, D-B, D-C, D3, D-D, D-E).
- `.ufo/waves/round-38/claims.json` (frozen; read-only), `c1-controls/before.txt`.
- `.ufo/waves/round-37/kasegi-r37-build-results.json` (G4 shape: `{lane,round,wave,seats:int,results:[{name,agent,output}]}`, seats=64=len(results)).
- `wave1-dispatch.json`: `wave=kasegi-r38-build`, `taskCall.tasks` len 73, `counts.spawn=73`.
- ExecSuiteBuild's and the scribes' item texts (dispatch), to review against the exact spec.
- The suite: 1473 ln, sha256 `85d33ea9d386926e88f9818bbdae5c49ef9cf951363ea09de641cb22a26979a6`,
  `bash -n` OK.

## Runs (actual output)

- plain run → `r38-closure: refusing to run against the live worktree…` **exit=2** ✓.
- `--export-ref a173b0c2… --work $S/base-run` → **closed=0/8 exit=1**: G1 red (corrections 0/0,
  readme-fence=open, declared-blocks=0), G2 red (receipt=0), G3 red (resolutions-section=0,
  diff-read=ok), G4 red (dispatches=0, read=fail), G5 red (round38-section=0, correction=0),
  G6 red (r38=present — seats' scratch live), G7 red (filled-section=0),
  **G8 red (r37-suite=1, r37-closed=0, r37-exit=1)** — the r37 suite's E9 live limbs
  (HEAD=7001535 ≠ base; worktree holds untracked wave files) red it, exactly as its docs disclose.
  The before-controls' "G8 green at base" was measured at freeze when HEAD==base and the tree was
  clean; mid-wave it is red by construction.
- `--export-ref 2387dcf6…` → same shape, closed=0/8 exit=1 ✓ (counting command 4 satisfied).
- `--selftest --export-ref a173b0c2…` → 8 case lines, **positives honestly red** (base lacks the
  round-38 evidence), **all mutants rejected**: G1 3/3, G2 6/6, G3 2/2, G4 2/2, G5 4/4, G6 5/5,
  G7 2/2, G8 2/2 (26 fixtures); `selftest cases=8 failures=8`; judge: own-report accepted=0
  (honest at base), forged-summary/caselines/failed-cases/detail-free/7-cases all rejected=1;
  exit 1 ✓ (matches the item's prove-it prediction).

## Confirmed false-green holes (probe evidence — sourced the suite, ran `check_g*` on fixtures)

Positive control first: an **unmutated** `g2_fixture` with a proper xref is GREEN (all 13 limbs=1),
so every green below is hole evidence, not check breakage.

1. **G2-H1 (highest): forged self-naming receipt passes.** `g2_fixture xref=$REF` (export-ref ==
   REF; `diff REF..REF` vacuously empty) with **fabricated payload keys** (`G<i> payload=zzz-forged=1
   closed=1`) → rc=0. Two causes: (a) the r37 E10 **cross-run payload key-set limb is absent** —
   nothing compares the receipt's recorded payloads to the live run's; (b) `merge-base
   --is-ancestor` accepts equality, so a receipt naming REF itself passes the ancestor limb with a
   vacuous diff. A receipt no run ever produced satisfies G2 → the suite prints 8/8.
   *Minimal fix*: restore the r37 cross-run limb (check_g2 evaluated LAST; for each id except G2,
   recorded payload KEY SET == live key set) **and** require a strict ancestor
   (`xref != ref && is-ancestor`), matching the claims' judged_head_rule (Y = J + receipt only).
   Strict ancestry forces the positive `g2_fixture` into the fixture-repo harness the G2 selftest
   already builds; the model-faithful alternative is ancestor-or-equal + the cross-run limb.
2. **G2-H2: receipt selftest block accepts failures.** Case lines rewritten to
   `positive=fail mutants=0/0 verdict=fail` (×8) → rc=0. check_g2 counts only
   `^selftest case=G[1-8] ` (8, distinct) + the summary — no positive/verdict/mutant shape.
   *Minimal fix*: per-id require `positive=pass`, `verdict=pass$`, `mutants=<o>/<n>` with n≥1 and
   o==n, and exactly n `selftest detail=G<id> mutant=… rejected=1` lines (the r37 E10 contract —
   the logic already exists in `judge_selftest_report`; reuse it on the receipt block). The
   positive fixture must then emit detail lines (it currently emits none).
3. **G2-H3: `closed=0` lines not banned** (doc-code mismatch — the header says "no closed=0").
   Appending `G9 payload=stray closed=0` → rc=0. *Fix*: `grep -cE '^G[0-9]+ payload=.* closed=0$'`
   == 0 inside runlines.
4. **G1-H1: Correction line inside a fence counts.** A tree whose only PROVINCE correction sits
   inside a ```text block that later closes → rc=0 (rendered as code, invisible as prose).
   *Fix*: make `g1_correction` fence-aware (count only lines outside fences).
5. **G1-H2: declared tail need not contain the Correction line.** PROVINCE = correction + trailing
   note; declaration = last 1 line only (the note) → rc=0. The declared-blocks limb degenerates to
   "the last line's sha is declared". *Fix*: require each front door's declared tail to contain
   that file's `Correction (round 38)` line.
6. **G1-H3: fence walk false-greens.** `fence_state` returns **closed** for (a) an unpaired `~~~`
   opener swallowing the rest of the file and (b) a ` ```` ` (4-backtick) opener closed by bare
   ``` — CommonMark says both are OPEN. The header's limit sentence ("a `~~~`-closed front door is
   red") states the **wrong direction**. *Fix*: track the opener's character and run length; close
   only on a same-character run ≥ the opener's with no info string; include `~~~`; correct the doc.
7. **G1-H4: declaration path escapes the export tree.** A line `../../outside.md 1 <sha>` validated
   against bytes OUTSIDE the export (`[ -f "$tree/$path" ]` with `..`) → rc=0, declared-ok=1.
   *Fix*: reject paths matching `/*` or containing `..`.
8. **G4-H1: stale sibling wave accepted.** `wave1-results.json` rewritten with
   `wave="some-other-wave"`, seats=3 → rc=0: the **sibling's** wave field is never verified (only
   the fallback's is). *Fix*: verify `results.wave == dispatch.wave` for the sibling too.
9. **G4-H2: zero-task wave is vacuously green.** dispatch `tasks:[]` + results `[]` → 0==0 → rc=0.
   *Fix*: require `len(taskCall.tasks) >= 1`.
10. **G7-H1: `| 1x |` satisfies proposal 1.** Rows rewritten `| 1x |`…`| 7x |` → proposal-rows=7,
    missing=0 → rc=0: `c ~ /^[0-9]+/` (no end anchor) + awk numeric coercion (`"1x"+0==1`).
    *Fix*: end-anchor after the decimal strip: `c ~ /^[0-9]+$/`.

Downgraded after a cross-check: **G5 lowercase `final lane commit:`** escapes G5's own
case-sensitive limb (probe: final-lane-commit-lines=0, rc=0) **but G2's case-insensitive headtok
limb catches it in the same section** (probe: head-token-lines=1, G2 red) — defense-in-depth only;
optional hardening: `(?i)final[ ]lane[ ]commit` in G5.

## Holes the implementation closes (verified in code + its own selftest)

- G1: declaration lines ≥1 (the spec's named 0-line bypass — `tail -n 0` → `e3b0c442…` — closed);
  every declaration line validated (one bad line → declared-ok=0); 64-hex sha; per-file token
  binding (PROVINCE↔L79-L152, README↔L399-L454); whole-file fence walk.
- G2: exactly one `export-ref=`/`suite-sha256=` line (full-line anchored); distinct G1..G8 ids
  (duplicate id → got<8 → red); exactly one closed line; last-section semantics (`md_section`
  takes the LAST `^## Round 38`); diff/ancestry live reads fail-closed (exit status read);
  SHONEN's bad-label limb correctly scoped to round-38 lines — a whole-file limb would false-red
  on SHONEN L172's historical `final lane head aa88877b…` evidence line.
- G3: digit-bounded line tokens (`(^|[^0-9])L10([^0-9]|$)` — the L100/L900/L850 substring trap
  closed; verified `grep -c L10` matches `L100` while the bounded form does not); rows scoped to
  the resolutions section; diff base = the constant `a173b0c2…` (REF^ would narrow → false green;
  the r37 base would widen → false red on r37-added markers); diff read fail-closed; word-bounded
  TBD/TODO; the vocabulary limb composes with the section limb (a resolutions row quoting
  `⟨pending` is an added line → red).
- G4: zero dispatches → red (≥1 required); malformed dispatch/results → red (not exit 2); count
  from `len(taskCall.tasks)`, not the dispatch's `counts` field; `len(results)` preferred over the
  `seats` int; fallback `<wave>-results.json` only when the sibling is ABSENT, with the wave check.
- G6: **every top-level entry counts (no `-type d`)** — the exact D-E recurrence (r37's leftover
  FILE `build-spec.py`) is closed and selftested (`r37-leftover-file` mutant); unreadable dir →
  `unreadable` → RED (chmod-000 mutant tested) — r37's `find … 2>/dev/null` fail-open is fixed;
  the parent carve-out requires an empty chain toward --work (sibling leftover → red; tested);
  entries judged by realpath; `tolerated=` printed.
- G7: line-number AFTER comparison; rows scoped to the filled section; separator/header rows
  ignored; set semantics {1..7} with missing=0; Correction line scoped inside the section.
- G8: runs the EXPORT's own r37 suite (not the lane copy); missing suite → red (not exit 2);
  requires BOTH last non-empty line `closed=14/14 exit=0` AND rc=0; stderr merged (a die message
  becomes the last line → red — fail-closed).
- Judge: 8 cases, per-id dup==1, verdict=pass, mutants o==n≥1, n detail lines with rejected=1;
  5 forged probes rejected (summary-only, case-lines-only, failed-cases, detail-free 0/0, 7-case).
  The r37 model's duplicated-id probe was dropped — the per-id dup==1 logic still rejects it;
  re-adding the probe is optional.

## Spec-level finding R1 — the judged-head counting command (claims-wording hazard, not a suite hole)

`judged_head_rule`: J = the receipt's `export-ref`; J carries every round-38 change **except** the
receipt; tip Y = J + receipt only. Therefore the receipt exists only at Y, and a run at J prints
**7/8 with G2 red=all-gates-absent** (fail-closed) — plus G8 red (r37 E9 head-match=0 whenever
HEAD≠REF; measured: both base and r37-head runs red G8 for exactly this reason). The counting
command `bash corpus/instruments/r38-closure.sh --export-ref <J> -> closed=8/8 exit=0` is only
satisfiable at **Y** (the tip whose diff to J is the receipt alone). The round-38 report must spell
the verification command as `--export-ref <Y>`; a verifier who fills `<J>` literally sees 7/8 and
the kill rule fires on a live claim. Also note G2's diff limb pins the suite's green window to Y
exactly: at any later ref the diff grows and G2 reds — the judged-head question moves to the newer
round's receipt; the suite header should state this window.

## Landing requirements for the L1 (from the suite's own tested mutants)

- The SCORECARD correction line (which quotes `Final lane commit: f3246559…`) must land **outside**
  the `## Round 38` section — the suite's own `G2-correction-inside` / `G5-correction-inside`
  mutants reject it inside (head-token-lines=1 / final-lane-commit-lines=1). Appending it at the
  end of the round-37 section satisfies G5 (file-wide scan) and G2 (r38-section scan).
- The round-37 resolutions rows must NOT reproduce the `⟨pending` marker spellings — any added line
  containing them reds G3's diff limb; name the line numbers and resolutions only.
- `[L1-MEASURE]` cells must be filled before J: nothing checks them (deliberately outside the G3
  vocabulary). Optional hardening: add the token to G3's vocabulary — safe because the L1 fills
  them before committing J.
- SHONEN's round-38 lines must contain `judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt`
  (the suite requires ≥1 file-wide in SHONEN; the ScribeShonen item already mandates it).

## Residual risks (suite-documented, accepted)

G4 compares counts, not identities (a results file with the right number of wrong seats passes —
minimal fix when wanted: entry-name set == dispatch task-name set); G3's `.ufo` exclusion lets a
placeholder in a .ufo prose receipt escape (the dispatch/spec JSONs legitimately quote the tokens,
so the exclusion is load-bearing — keep and document); G6 does not audit the tolerated --work
dir's contents (the caller's own space; `tolerated=` is printed — a reviewer eyeballs that path);
G6/G8 are live-by-design (the 8/8 run must happen at filing time: HEAD==Y, clean tree, seats'
scratch cleaned — the mid-wave race is expected and disclosed); G2's header has no
no-other-header-lines limb (r37 had one); digest is bound to the executing bytes only (r37 also
bound the export's suite file — cheap hardening); G4 labels an absent round-38 dir `read=fail`
(cosmetic; the gate is correct).

## Tooling

None installed (bash/awk/python3/git/sha256sum sufficed); no pacman touched.

## Revision review (post-ExecSuiteBuild revision, verified by re-probe)

ExecSuiteBuild revised the suite in-wave after my findings (and CritJudgedHead's): now **1716 ln,
sha256 `7883c37cd3249a121d1f28c36fc06a0031d6cabcec513cf9b474df4bd52f8c9e`**, `bash -n` OK;
dispositions in `wave1/ExecSuiteBuild.md` §8. I re-ran every probe against the revised bytes
(sourced; fixtures + live-lines file under my scratch):

- **Positive controls GREEN**: unmutated `g2_fixture xref=$REF live=$LIVE` → all 14 limbs=1 incl.
  `crossrun=1`; unmutated `g1_fixture` → declared-ok=1. The checks discriminate.
- **All ten holes now RED**, each via the intended limb: H2.4 fail-positive receipt →
  `selftest-lines=0`; H2.3b extra `closed=0` line → `run-lines=0`; H2.1 key-drift and
  forged-keys-vs-live receipts → `crossrun=0` (cross-run payload KEY SET limb, G2 evaluated last
  with the live lines — plumbing verified in `run_suite_report`); H1.1 correction-inside-fence →
  `province-correction=0` (the new `g1_cm_walk` counts corrections only outside fences, and
  check_g1 requires BOTH walks closed); unpaired `~~~` and 4-backtick opener → `cm_walk=open`
  (the contract `fence_state` still says closed — harmless, both walks must close); H1.2b
  tail-without-correction → `declared-ok=0`; `../` traversal declaration → `declared-ok=0`;
  H7.2b `| 1x |` rows → `proposal-rows=0,missing=7`; H4.4b zero-task dispatch → `pairs=0`;
  H4.3b stale-sibling-wave → `pairs=0` (the wave check now applies to the sibling too).
- **End-to-end re-proved**: plain run exit 2; base a173b0c2 → closed=0/8 exit=1 (G2 payload now
  carries `crossrun=0`); r37 head 2387dcf6 → closed=0/8 exit=1; selftest at base → 8 cases,
  positives honestly red, **37 mutants all rejected** (6/11/2/4/4/5/3/2), 5 forged reports
  rejected, exit 1.
- **Additional hardening adopted** (from CritJudgedHead, verified in code): `cat-file -t` == commit
  (a tag object's hash cannot stand in); the post-receipt diff read as `--no-renames
  --name-status` accepting only A/M at the receipt path — closes the `git mv other <receipt>`
  collapse that `--name-only` would have hidden.
- **Two "kept" items — accepted with rationale**: (a) ancestor-or-equal stays: a receipt present
  in the export of REF cannot name REF itself (a commit cannot contain its own hash), so the
  equality branch is inert for any committed receipt, and the forged-receipt vector is closed by
  the cross-run key-set limb; (b) the literal label regex stays, scoped to the r38 section +
  SHONEN round-38 lines: the correction line quoting `Final lane commit: f3246559…` trips the
  zero-token limb only if landed INSIDE the section, which G5's own `Final lane commit:` limb
  independently forbids — the two `correction-line-inside-section` mutants encode exactly that.
- **Residuals that remain** (unchanged, disclosed): the receipt's selftest block requires the
  case-line shape but not per-id detail lines (r37 E10 required them; the case-shape + cross-run
  limbs compensate); G4 compares counts, not identities; G3's `.ufo` exclusion; G6's tolerated
  --work contents unaudited (`tolerated=` printed); **R1 stands** — the counting command
  `--export-ref <J>` is only satisfiable at the tip Y (a run at J prints 7/8 with G2
  red=all-gates-absent and G8 red on head-match); the report must spell the verification command
  as `--export-ref <Y>`, and the suite header should state G2's green window (Y exactly).

## Revision 3 (final bytes, verified by re-probe)

ExecSuiteBuild filed revision 3 before landing: **1767 ln,
sha256 `09d46673a75b50479bb2b7e184b370d08554ad6a7e21ff6f63c67edca640be42`**, `bash -n` OK.

- **R1 adopted in the right places**: the suite header now documents G2's green window (L172: the
  receipt is read from the export, so a run at J is 7/8 with G2 red and the 8/8 run is at the tip
  Y that carries the receipt); the executor's receipt §1/§6b spell the verification command as
  `--export-ref <Y>` with the report naming J and Y.
- **New limbs verified in code**: (a) receipt-header scoping — the sentinel/export-ref/suite-sha256
  counts apply to the block before the first `== ` marker (required for the positive: a genuine
  receipt repeats the digest and ref inside its pasted run header, so a file-wide count is wrong);
  (b) per-commit history limb — every commit in `export-ref..REF` must show only A/M/R rows in
  `diff --name-status c^ c` (a file added and removed inside the range needs a D row → red);
  a failed history read → `history=0` (fail-closed). The endpoint diff (only A/M at the receipt
  path, renames off) remains the binding limb; R rows in the per-commit walk are harmless because
  the endpoint reds any net rename.
- **Declined rule accepted**: the resolve-every-token label rule was declined with a measured
  counterexample — the drafted ScribeScorecard section cites the freeze commit `9a10b02…`, so a
  resolve-every-token rule would red the real section; the literal rule stays section-scoped, and
  a missing heading is already red via `scorecard-ref`/`round38-section`.
- **Re-probe on the final bytes**: both positive controls GREEN (G2 poscon now carries
  `history=1` alongside `crossrun=1`); all ten hole probes RED via the same limbs as revision 2;
  plain run exit 2; base a173b0c2 → closed=0/8 exit=1; r37 head 2387dcf6 → closed=0/8 exit=1;
  selftest at base → 8 cases, positives honestly red, **38 mutants all rejected**
  (6/12/2/4/4/5/3/2 — the +1 is `history-added-then-removed`), 5 forged reports rejected, exit 1.
  (The executor's own "closed=1/8 at base" proof runs G8 green through a fixture lane whose HEAD
  equals the export ref; in the real lane mid-wave G8 is red on live state — both honest, the
  difference is the disclosed live-by-design E9 limbs.)

## Scratch

All work under `/fast/scratch/hyaku/kasegi-r38/RevSuiteDesign/` (probes, fixture trees, work dirs);
removed before yielding.
