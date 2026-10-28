# R44W2Revenger01 — intent reconstruction of the eight routed round-43 defects (falsify wave)

- seat: R44W2Revenger01 (leaf, read-only; this file is the only lane path written)
- item: for each §6 item of `corpus/lessons/round-43-verifier-spotcheck.md`, recover the invariant the non-author reviewer was protecting, then judge whether the round-44 repair in committed tree `8063547d0ce647d6f9eafc3c8d0a502616685218` satisfies that invariant or only the literal prescription.
- method: read-only re-derivation over committed bytes (`git show`/`git ls-tree`/`grep`), plus scratch reproductions of the committed instruments and of the disputed receipts. All scratch under `/fast/scratch/hyaku/kasegi-r44/R44W2Revenger01` (removed before yield). No tool installs (system git/python3/coreutils sufficed; no pacman use). No mutations anywhere.
- worktree note: the lane worktree carries `M SCORECARD.md` and four untracked `.ufo/waves/round-44/wave2` files at the time of reading — other seats' in-flight state; every finding here is from `git show 8063547:…` bytes, not the worktree.

## Summary

| §6 | defect (one line) | invariant recovered | repair satisfied? |
|---|---|---|---|
| 1 | `closed=13/19` unbacked | unbacked numerals superseded by committed, labeled evidence, append-only | **yes** |
| 2 | no check can see defect 1 | the superseded literal becomes visible to a real committed check | **no — mechanism void; letter only** |
| 3 | 29 vs 26 numeral | numeric claims carry counting commands, append-only | **yes** (replayed: 26, 40) |
| 4 | report omissions (planner/L2 floor) | the report records planner mapping + wave shape per `lane-addendum.md:233-241` | **staged yes; report half unverifiable at this tree** |
| 5 | wave-evidence hygiene | every receipt self-identifying/bound; clean tree | **yes in substance**, two residues below |
| 6 | SHONEN lost final blank | append-only byte preservation | **yes** (bytes verified) |
| 7 | SHONEN pointer wrong | pointers resolve at their target | **yes** (both prescribed routes done) |
| 8 | before-cell token 127 | a cited control is cited only for what it prints | **yes** (127 replayed) |

Headline falsification: **defect 2's repair records a mechanism that cannot work.** `corpus/lessons/round-44.md:91-93` states the erratum "is committed and matched by K17's own `claims-erratum*` escape — the mechanism is K17's escape", but K17 skips after-cells *before* any erratum lookup (`corpus/instruments/r43-limbs/k17-claims-before.sh:326`, `if field == "after":`), and `closed=13/19` is an **after**-cell token (`.ufo/waves/round-43/claims.json:41`). The same commit's own erratum says so (`claims-erratum-6.md:10`, "K17 skips after-cells") — the round-44 records contradict themselves, and the C1 counter's D2 limb encodes the void mechanism (it checks its own vocabulary in the erratum, never K17's firing).

## Per-defect findings

### §6.1 — `closed=13/19` unbacked — **satisfied**

- **Invariant:** a numeric claim in round records must be backed by a committed run of the instrument it names; an unbacked literal is superseded by committed, labeled evidence, never rewritten (PROTOCOL evidence standard).
- **Repair:** `SCORECARD.md:1685` row keeps `closed=13/19 exit=1` as history; appended correction `SCORECARD.md:1691` supersedes it and cites the erratum; erratum `claims-erratum-6.md:3` supplies the replacing evidence; `:10` additionally corrects the spotcheck's own mislocation.
- **Why yes:** every replacing claim is byte-verifiable or explicitly labeled: the suite is absent at base (`git cat-file -e ab98fac9:corpus/instruments/r43-closure.sh` → rc 128 class); the r42 stand-in prints `closed=12/13 exit=1` at base (`.ufo/waves/round-43/c1-controls/do-nothing.txt`, J8 sole red); the landed suite's true base reading `closed=12/19` (K8 + K14–K19 open) is derivable from committed bytes and recorded in `wave1/R44Critic2.md:21-50`, which the erratum honestly labels "a seat report, not a committed final-gates base receipt". I verified the ground truth myself: `13/19` is in the C1 **after**-cell (`claims.json:41`); the **before**-cell (`:38`) says `closed=12/13` + `exit 127` — the spotcheck's §6.1 wording ("C1 `before` state … `closed=13/19`") was itself half-wrong, and the repair says so instead of silently conforming to it.
- **Caveat (not a failure):** the prescription's option-1 pointer (the six per-limb K14–K19 base transcripts) is not cited by the correction; the lane chose absence + stand-in receipt + Critic2's full-suite derivation, which is stronger. The counter's D1 limb (correction paragraph + erratum vocabulary) would also accept a vacuous erratum with no replacing evidence — the committed repair exceeds its own counter here.

### §6.2 — no check can see defect 1 — **NOT satisfied (invariant); letter only**

- **Invariant:** the superseded literal must become visible to at least one committed machine check; a correction nothing can grade recreates defect 1's invisibility. Prescription: add the erratum so "K17's existing escape then covers it", do not widen K18, and say which.
- **Repair:** `claims-erratum-6.md` committed in the round-43 wave dir; `corpus/lessons/round-44.md:91-93` says the mechanism is "K17's escape, not a widened K18".
- **Why no:** the stated mechanism is void on K17's own committed rule. K17 grades `before` tokens only; `:326` skips `after` fields before the erratum lookup, so an erratum naming `13/19` is never consulted for it. The only graded round-43 C1 before-token, `closed=12/13`, is printed by its cited control (`do-nothing.txt`), so the escape has zero work to do even there. Empirically (committed): R44Critic2 ran K17 at the frozen base → `K17 payload=claims=21,tokens=5,verified=4,superseded=1,unbacked=0 … closed=1` — green with `13/19` unbacked in the same file (`wave1/R44Critic2.md`, F2). K18 is no rescue either: its supersede set already counted `13/19` as superseded at the frozen base from the spotcheck's own defect text (F3), i.e. it cannot distinguish the correction from the prescription and was already green before any repair. Consequently the only committed check whose verdict depends on the erratum existing is the round-44 counter itself, whose D2 limb tests marker vocabulary (`13/19` + `superseded` + `r43-closure.sh` in any `claims-erratum*.md`), not K17's predicate.
- **Self-contradiction in the same commit:** `claims-erratum-6.md:10` states "K17 skips after-cells" while `round-44.md:93` states the erratum is "matched by K17's own … escape". The attempt-1 half of the lesson even says "adding prose cannot establish closure" — then the attempt-2 half re-asserts the void mechanism as the fix.

### §6.3 — lesson numeral (29 → 26) — **satisfied**

- **Invariant:** numeric claims carry their counting command; corrections append-only.
- **Repair/verification:** original "29-character prefix" sentences still at `corpus/lessons/round-43.md:90,101` (diff 10+/0−); appended correction carries both counting commands with outputs and the grading limb name; control `controls/fix-hash-count.txt`. Replayed: `printf %s c6ae07c6a541e0e96d0040afb6 | wc -c` → 26; full hash → 40. Exceeds the letter (command *and* observed output recorded).

### §6.4 — report omissions (planner=L1, L2 floor, residual) — **staged yes; report half unverifiable at this tree**

- **Invariant:** `scripts/hyaku/lane-addendum.md:233-241` (fleet root, read) mandates the **report** record the round shape (wave seat counts, role mix, residual calls, round total) and the planner-seat mapping ("Record that mapping in the report").
- **Repair:** `LOG.md` round-44 attempt-2 section (from `:1977`) records `planner=L1`, the `L2 floor` line with `wave 1 seats: 66` and role mix, and `residual call: none` — cross-checked against committed data: `wave1-results.json` `seats=66, results=66`; registry replay byte-identical with `names=66`; role sums 20+12+8+8+8+5+3+1+1 = 66.
- **Why not fully:** `.ufo/reports/round-44/` does not exist at `8063547`, so the mandate's report half cannot be verified yet; and the counter's D4 limb grades LOG.md only — a final report omitting the fields would still grade green. Recorded now, auditable at closure.

### §6.5 — wave-evidence hygiene — **satisfied in substance, two residues**

- **Invariant:** evidence artifacts bind to what produced them (registry names populated, receipts carry their export-ref); no aborted-write leftovers in the tree.
- **Verified:**
  - leftover `all-gates.at-Y.txt.tmp` absent from the worktree and from `8063547` (`git ls-tree` empty). It was untracked in round 43, so no git export ever contained it — **the counter's D5 leftover limb is vacuous over exports**; the real evidence is `controls/round43-temp-removal.txt` ("removed by lane edit" — the prescription said "through the lane helper"; outcome achieved, letter deviates).
  - emitter `corpus/instruments/wave-registry.py` is fail-closed: my replay against `wave1-results.json` reproduced the committed registry **byte-identically** (`seats=66 names=66 attack=40`); a doctored results file (seats=66, 5 named) is refused — `rc=1`, "seats=66 but 5 named seats — refusing to emit", no output file.
  - round-43 `w1-REGISTRY.txt:7` left as filed (`names=` empty), corrected by companion `controls/round43-registry-correction.txt` re-deriving all 73 names from `w1-dispatch.json` — append-only discipline kept.
  - **export-ref sidecar — the interesting one.** The sidecar (`r42-at-de09313-selftest.export-ref.md:11`) binds the token-less receipt to `export-ref=ab98fac9…`. **I verified this binding is TRUE by exact reproduction**: running the committed r42 suite (sha `fca5ae62…`) selftest at the **ab98fac9** export reproduces `r42-at-de09313-selftest.txt` byte-for-byte — all 14 lines including J1 `mutants=0/1 … verdict=fail`, J8 `payload-match=0`, J10 `payload-match=0`, `selftest cases=13 failures=3`. The same selftest at the **de09313** export (suite `d92c0de1…`) instead reproduces the round-44 replay/runner.log (`failures=1`, J1 `1/1 pass`). So the receipt's own filename ("at-de09313") and the spotcheck's "transcript pair" framing were the misnomers: the "pair" is two different runs at two different exports.
- **Residues:** (a) sidecar `:16` calls the de09313 run file "replay receipt for **the same export**" and `:19` calls the de09313 replay "the round-44 replay of **the same export**" — both are a different export (`failures=3` vs `failures=1` proves different runs); (b) no committed text states the resolution my experiment establishes (receipt = ab98fac9 selftest; run file = de09313 run; pair mismatched). The binding stands; its corroboration lines mislabel.

### §6.6 — SHONEN final blank line — **satisfied**

`SHONEN.md` at `8063547` ends `0a0a` (was `0a` at `dbd2e106`); `git diff --numstat ab98fac9 8063547 -- SHONEN.md` → `18 0` (pure append); box state unchanged (40 × `- [~]`, 0 × `- [x]` at base and tip). Invariant (append-only byte preservation) met exactly.

### §6.7 — SHONEN pointer retarget — **satisfied**

Rows for `r43-closure.sh` and `claim-package-check.py` (plus the two round-44 instruments) appended to `corpus/instruments/README.md` ("Round-44 registry addition"), a pointer correction appended to `SHONEN.md`, and a `SKILL.md` Gates & probes correction + rows appended — both routes of the prescription done, all appends (SKILL.md 10+/0−, README 16+/0−, SHONEN 11+/0−). Pointers now resolve at both named homes. Minor nit: the SKILL.md correction says README "contains no matching rows" (true of round-43 state) in the same commit that adds them; the README section states the time scoping explicitly, so no contradiction survives a careful read.

### §6.8 — before-cell token 127 — **satisfied**

Erratum `:5` separates the two values and says "The two values describe different commands"; `:10`-adjacent clarification notes the control's `127` at line 41 is quoted r42 prose — verified: `do-nothing.txt:5` is `exit=2` (its §A `ls`), `:41` contains `127` only inside quoted round-42 before-cell text. Receipt `controls/missing-suite-base.txt` records the direct command; I replayed it: `bash corpus/instruments/r43-closure.sh` inside an `ab98fac9` export → `exit=127`. The invariant (cited only for what it prints; otherwise measure) is met.

## The C1 counter and the round's evidence discipline (context for the verdicts)

- **The committed counter is real and reproducible.** From committed bytes I reproduced, byte-identically to the lane's receipts: `--root <8063547 export>` → `total=8 fixed=8 unresolved=0 exit=0`; `--root <5ab3a60 export> --baseline <5ab3a60>` → `total=8 fixed=0 unresolved=8 exit=1` (the kill rule holds for the committed instrument: a do-nothing replay cannot report all 8 fixed); `--selftest` → `cases=11 failures=0`, every mutant marker-kept/artifact-dropped.
- **The frozen C2 counter is dead as written** — independently confirmed: `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md` → `0` (rc 1) at both `5ab3a60` and `8063547` (status is the third cell). The round disclosed this (`controls/c2-frozen-counter-replay.txt`, M44-8), left the frozen bytes untouched, and shipped `r44-frontier-count.py` measuring the same declared predicate table-aware: 25/25 `SHORT exit=1` at base, 26/26 `exit=0` at the tree — red-before verified. SOURCES 68→70 and knowledge 62→63 confirmed. Frozen-predicate discipline held.
- **One stale statement ships in-tree:** `controls/r44-counter-trial-disposition.txt` says the counter "is not present under `corpus/instruments/` at the final tree", while the same commit lands the replacement counter at that path and registers it (README row; M44-7 documents the withdraw-and-replace). A reader of the disposition alone would conclude no counter exists. The lane holds both claims unverified and score-neutral in `SCORECARD.md` (round-44 rows), so no verdict inflation — but the disposition's tree-claim is false at the tree it ships in.

## Limitations

- I did not execute the r43 suite or K17/K18 limbs myself; for K17's behavior I rely on its committed header rule (`:326` verified by grep) plus the committed empirical run in `wave1/R44Critic2.md` (F2), whose commands and outputs are recorded there.
- The original `r42-at-de09313-selftest.txt` reproduction (my ab98fac9 run) was produced by the committed suite in my scratch export; I did not diff the suite's full run-portion against `do-nothing.txt` §B beyond the header shas (`fca5ae62` matches).
- `.ufo/reports/round-44/` absence makes §6.4's report half a deferred check, not a passed one.
- The working tree's `M SCORECARD.md` (not mine) was excluded from all findings; committed bytes only.
- Scratch `/fast/scratch/hyaku/kasegi-r44/R44W2Revenger01` removed before yield; no tools installed; no pacman; no commits or mutations.
