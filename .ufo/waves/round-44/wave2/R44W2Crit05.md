# R44W2Crit05 — mined-mistake attack: M44-7 and M44-8 (round 44, attempt 2, wave 2)

Seat: critic (leaf, read-only). Committed tree under attack: `8063547d0ce647d6f9eafc3c8d0a502616685218`.
Frozen base: `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`; freeze commit: `66314015122b9aa32dc40f2f1815df56624c26d1`.
Method: every run below executed the **committed bytes** (`git archive 8063547 | tar -x` into scratch) against **exported trees** (`git archive` of `8063547` and `5ab3a60`); no production file was read-modified, no git/jj mutation run. Scratch `/fast/scratch/hyaku/kasegi-r44/R44W2Crit05-2/` removed before yield. Tooling: none installed (python3 3.14, git, GNU grep sufficed).
Working-tree note: the lane checkout is dirty (`SCORECARD.md` +15 uncommitted lines; wave-2 files untracked). All verdicts below are against the **committed** tree; the uncommitted delta is reported where it matters (§3).

Inputs read per assignment: `.ufo/waves/round-44/claims.json` (unedited), `corpus/lessons/round-43-verifier-spotcheck.md` §6 (eight routed defects), `corpus/lessons/round-44.md` `## Mistakes` (:125 M44-7, :126 M44-8), and the three instruments.

---

## 1. M44-7 (`corpus/lessons/round-44.md:125`) — C1 counter replacement

### 1a. Is the fix shown able to fail? — PARTLY: deletion attacks fail; the filed fabrication attack does not

**Verified (reproduced from committed bytes):**

```
$ python3 <export>/corpus/instruments/r44-routed-defects.py --root <export-8063547> --baseline <export-5ab3a60>
routed-defects total=8 fixed=8 unresolved=0 exit=0
routed-defects-baseline total=8 fixed=0 unresolved=8
$ ... --selftest --work <scratch>
selftest cases=11 failures=0        # POSITIVE + 10 mutants, all rejected
```

Matches `controls/c1-counter-after.txt` and `controls/c1-do-nothing.txt` (both tracked at 8063547). My own whole-tree **deletion** probe (all five bound non-prose artifacts removed, every prose marker kept) is rejected: `fixed=3 unresolved=5 exit=1`. So the attempt-1 false-green cannot recur by *deleting* artifacts.

**Falsified (the strong form of the row's claim):** a **fabrication** attack — the exact defeat shape Critic1 filed — greens the committed counter. Reconstructed per `wave1/R44Critic1.md:21-29` (F1: frozen base + marker strings + fabricated artifacts, zero substantive repairs), adapted to the committed counter's predicates:

```
$ python3 <export>/corpus/instruments/r44-routed-defects.py --root <forge>
R44-D1..D8 status=fixed (all eight)
routed-defects total=8 fixed=8 unresolved=0 exit=0
$ python3 <export>/corpus/instruments/r44-routed-defects.py --root <forge> --selftest --work <scratch>
selftest case=POSITIVE verdict=pass fixed=8 unresolved=0
```

The forge fabricated: a `claims-erratum-6.md` carrying the required tokens, a lesson-43 correction paragraph with pointer/full-hash/count-command, a `LOG.md` round-44 section plus a fabricated `wave1-results.json` (`seats=73`), a fabricated `wave-registry.txt` (73 fake names), the export-ref sidecar, README instrument rows, a SHONEN correction + trailing blank line, and a fabricated `exit=127` receipt. The counter's D4/D5 cross-checks validate *internal consistency between two fabricated files* (73=73), not authenticity — the counter never runs git and cannot distinguish a committed artifact from a fabricated one.

- This is precisely the defect class Critic1 filed against the draft: "the do-nothing test is necessary but not sufficient; the counter gives a green final result to a fabricated state" (`wave1/R44Critic1.md`, F1 conclusion).
- It violates the lane's own standing rule **R42** (`corpus/QUALITY.md:354`): "A check counts as repaired only when its selftest's mutant set contains the committed defeat shape for its family — the input a committed attack receipt or routed defect filed, at the bytes it filed them, **not a stand-in the author composed**". The battery (`r44-routed-defects.py:416-490`) contains only author-composed per-limb deletion/blanking mutants; the whole-tree forge is absent, and the selftest grades that forge as its POSITIVE case.
- Scope honesty: C1's *frozen kill rule* (`claims.json:13`) is not triggered — the do-nothing replay reports 0/8. What fails is M44-7's *evidence* claim ("every mutant rejected ⇒ fail-closed"), not the frozen predicate.

**Mutant-battery misdescription (three committed places):** the row (:125), the C1 section (:86-88) and `corpus/instruments/README.md:992` all say "eleven mutants — one per limb plus the always-pass case" and "every mutant keeps the prose marker and drops the artifact the limb binds to". Actual (`r44-routed-defects.py:416-490`): **11 cases = 1 POSITIVE + 10 mutants**; D5 carries three mutants (not one-per-limb); D4-count-mismatch (:462) mutates a number in a kept file and D5-leftover-back (:465) *adds* a file — neither "drops the artifact". The uncommitted SCORECARD attempt-2 row repeats "rejects eleven marker-only mutants".

**Binding scope:** 3 of 8 limbs (D3, D6, D7) bind prose-only content (lesson paragraph tokens; SHONEN byte-tail + box count; README rows + SHONEN paragraph). Measured: in my deletion probe those three stayed `fixed`. The instrument docstring's "not merely at a sentence that says the defect was fixed" (`r44-routed-defects.py:12-14`) holds for 5/8 limbs. Per-defect this is defensible (defects 3/6/7 are prose/pointer defects), but the row's universal "every limb binds a committed artifact and a content token inside it" should be scoped.

### 1b. Does the evidence pointer resolve? — Resolves, then refutes the row

- Captured-by pointer `.ufo/waves/round-44/controls/r44-counter-trial-disposition.txt`: **tracked at 8063547, resolves** — and **contradicts the row**: ":3 `r44-routed-defects.py` ... is NOT an accepted verifier and is **not present under `corpus/instruments/` at the final tree**"; ":5 Disposition: **discard the counter as a production gate** ... **report C1 unverified** ... **The after-state is not credited.**" The same commit adds `corpus/instruments/r44-routed-defects.py` (blob `ae56da8f`, `git ls-tree 8063547`), so the disposition's factual sentence is false at the tree that commits it, and its operative disposition denies what M44-7 credits. Neither file marks the other superseded.
- Evidence-cell pointer `controls/c1-counter-after.txt` (:125) resolves only under the undocumented base `.ufo/waves/round-44/` — not repo-root-relative (contrast the captured-by cell's repo-relative form in the same row), not resolvable from `corpus/lessons/`.
- The underlying findings do resolve: `wave1/R44Critic1.md:21-29` (forge → `fixed=8 unresolved=0 exit=0`), `wave1/R44Critic3.md`, `wave1/R44Critic4.md` (false-positive limbs) — all tracked.

### 1c. Is the captured-by criterion the right rule? — NO

It cites a **disposition** (a decision document rejecting the counter and the after-state) as the capture of a mistake the row then credits. A captured-by cell must point at the **finding**; the findings exist as wave1 seat reports and are what the disposition itself cites (`wave1/R44Critic1.md:21-29`, `R44Critic3.md:58-95`, `R44Critic4.md:22-35`). Citing the disposition inverts the authority: the row's own cited evidence says the opposite of the row. This is the duplicate-authority defect, not a wording nit.

---

## 2. M44-8 (`corpus/lessons/round-44.md:126`) — C2 counter correction

### 2a. Is the fix shown able to fail (red base count)? — The red base count holds; "green only at the round-44 tree" is falsified

**Verified:**

```
$ python3 <export>/corpus/instruments/r44-frontier-count.py --root <export-5ab3a60> --expect 26
frontier rows=25 admitted=25
frontier expected=26 admitted=25 verdict=SHORT exit=1          # red at frozen base
$ ... --root <export-8063547> --expect 26
frontier rows=26 admitted=26                                    # exit 0
```

Matches `controls/c2-frontier-counter.txt` / `controls/c2-frozen-counter-replay.txt` (tracked).

**Falsified — "green only at the round-44 tree":** an F26-identity mutant (the F26 row replaced by a duplicate of the F25 row, 26 rows total, **no F26 present**) is green:

```
$ python3 <export>/corpus/instruments/r44-frontier-count.py --root <dup26-mutant> --expect 26 --ids
frontier-ids=F01,...,F25,F25
frontier rows=26 admitted=26        # exit 0
```

The counter counts rows, not identities — exactly the novelty-blindness `wave1/R44Critic11.md:150-151` filed ("a counter over row shape cannot tell a duplicate F26 from a novel one — both print 26"). C2's kill rule (`claims.json:22`: "no coverage credit unless F26, its captured source, knowledge entry and registry row all land") is enforced by **no** committed instrument: nothing checks F26's identity, its S069 citation, the knowledge entry, or the registry row.

### 2b. Does the evidence pointer resolve? — Both resolve; the cited control contradicts the row's Error cell

- `controls/c2-frozen-counter-replay.txt` and `wave1/R44Critic11.md`: both tracked at 8063547, resolve (again only under the undocumented `.ufo/waves/round-44/` base).
- **The Error cell overstates its own control.** Row: "The frozen C2 counter string reads `0` in both the base and the after tree". Measured, verbatim frozen string (`claims.json:23`, three components):

```
base 5ab3a60:      0 / 68 / 62
committed 8063547: 0 / 70 / 63
```

Only the **frontier component** reads 0/0; the SOURCES (68→70) and knowledge (62→63) components are measurable and moving. The row's own cited control prints exactly these three numbers (`c2-frozen-counter-replay.txt`: "base 5ab3a60 stdout: 0 68 62 / worktree stdout: 0 70 63"). The lesson's C2 section (:107-109) repeats the overstatement; `LOG.md:1984` states it correctly ("the frozen C2 counter's **frontier regex** reads 0 in both worlds").

### 2c. Is the captured-by criterion the right rule? — Half right; the cited capture argues against the correction as landed

- First half ("the freeze rule that a counter must be re-derived on a do-nothing control before data") resolves to a real standing rule: R22 pre-freeze satisfiability, `corpus/QUALITY.md:226`. Correctly invoked.
- Second half cites `wave1/R44Critic11.md` — which does establish the frozen counter is unsatisfiable and novelty-blind (§4), but whose §4 remedy is to land the **R22 erratum with the grep spelling** and "**Do not report 26 from `claims.json:23`**", and whose headline contests the coverage credit itself (F26 restates 3 of 4 load-bearing rows; "vendor-instance credit, not the source-grounded frontier move"). The correction as landed substitutes a different instrument reporting 26 from row shape — inheriting the novelty-blindness the cited capture named — while the same file's **M44-3 row (:15)** prescribes the opposite disposition ("C2 is unverified; **do not substitute the correct diagnostic**"), never marked superseded.

---

## 3. Round-level finding: the committed tree carries two opposite authorities on both claims

At `8063547` the tree simultaneously asserts, with no supersession linking them:

**Credited:** `corpus/lessons/round-44.md:105-119` (C2 "measured with a disclosed counter correction", 25→26 exit 0), :121-127 (M44-7/M44-8: counter replaced fail-closed / counter corrected), `LOG.md:1983-1984` (the counter "grades them", "a marker-only tree is rejected").

**Unverified:** `SCORECARD.md:1697-1698` ("44 | depth:verifiability | ... **C1 unverified, no delta**"; "44 | coverage | ... **C2 unverified, no delta**"), `.ufo/waves/round-43/claims-erratum-6.md:11` ("**neither frozen claim is admitted as a score-bearing result** ... C1 is unverified ... C2 is unverified") and :20 ("These are structural observations, **not a C2 verdict** ... Round-44 score changes: none"), `controls/r44-counter-trial-disposition.txt:3,5` (counter "NOT an accepted verifier", "not present under `corpus/instruments/` at the final tree" — **factually false at 8063547**, blob `ae56da8f` present), and the lesson's own M44-3 (:15) / M44-4 (:16) rows ("C1 remains unverified"; "C2 is unverified; do not substitute the correct diagnostic"). `LOG.md:1986` even plans the same work for round 45 ("freeze a committed-export counter ... falsify it with marker-only fixtures"), contradicting :1983's "landed".

The attempt-2 L1 has drafted the fix **uncommitted**: the working-tree `SCORECARD.md` delta appends "Correction (round 44; attempt 2): the attempt-1 disposition above — 'C1 unverified, C2 unverified, no score delta' — is superseded by the two measurements above" — the right shape, but (a) it is not committed, so the committed tree stays self-contradictory; (b) it is not mirrored in `claims-erratum-6.md`, the disposition control, or the lesson's first Mistakes table; (c) it repeats the "eleven marker-only mutants" miscount.

**Smallest safe corrections (all append-only, per the corrections clause):**
1. Commit the SCORECARD supersession paragraph and mirror it as appended addenda in `claims-erratum-6.md`, `controls/r44-counter-trial-disposition.txt` (noting the path now holds the fail-closed replacement, blob `ae56da8f`, superseding the "not present" sentence), and a pointer in the lesson that M44-7 supersedes M44-4 and M44-8 supersedes M44-3.
2. M44-7 evidence cell: "eleven selftest cases — one positive always-pass case plus ten mutants (D5 carries three)" — and add the committed defeat shape (the whole-tree fabricated forge, per R42/`QUALITY.md:354`) as a selftest case, or state in the row why not.
3. M44-8 Error cell: scope the 0/0 to the frontier component ("its SOURCES and knowledge components read 68→70 and 62→63").
4. M44-8 evidence cell: replace "green only at the round-44 tree" with "green on any tree with 26 admitted rows; F26 identity is not enforced" — or add an identity check (e.g. `--ids` must contain F26 exactly once) to `r44-frontier-count.py`.

**Impacted axes:** `depth:verifiability` (C1 — M44-7), `coverage` (C2 — M44-8).

**Limitations.** I did not verify the substantive truth of the eight repairs beyond what the counter checks (e.g. whether the erratum's 12/19 run is real), did not re-open S069 live, and did not grade the uncommitted working-tree delta beyond noting it. My forge is a reconstruction of Critic1's filed shape (its forge bytes were never committed); it is documented above command-by-command so it can be replayed. No verdict inflation: where a claim held, I say so; the falsifications are the fabrication-green (M44-7), the duplicate-row green (M44-8), the Error-cell overstatement (M44-8), the disposition contradiction (both), and the captured-by rule (M44-7 wrong, M44-8 half right).
