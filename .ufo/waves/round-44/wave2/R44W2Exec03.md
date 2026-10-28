# R44W2Exec03 — falsify: committed C1/C2 counters and census receipt

seat: R44W2Exec03 (executor, wave 2, falsify wave)
attacked item: `corpus/instruments/r44-routed-defects.py` (C1 counter), `corpus/instruments/r44-frontier-count.py` (C2 counter), `scripts/sources-census.sh` census receipt, and the round's evidence discipline.
tree under attack: `8063547d0ce647d6f9eafc3c8d0a502616685218` (committed attempt-2 result); frozen base `5ab3a60`; claims `.ufo/waves/round-44/claims.json` (unchanged); routed defects `corpus/lessons/round-43-verifier-spotcheck.md` §6 items 1–8.
scratch: `/fast/scratch/hyaku/kasegi-r44/R44W2Exec03` (removed before yield). `HYAKU_SCRATCH` was unset; used the documented default `/fast/scratch/hyaku`.
tools: none installed or updated; `python3`, `git`, `bash`, `gawk`-backed `sources-census.sh` only. `pacman` not invoked.

---

## 1. Canonical receipt — every required command, verbatim

Exports were produced once with read-only `git archive` (no mutating git was run anywhere):

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 8063547d0ce647d6f9eafc3c8d0a502616685218 | tar -x -C $S/export-A   # rc=0
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 5ab3a60 | tar -x -C $S/export-base                              # rc=0
```

`--root` below means the exported tree; the *instrument* bytes used were those committed inside `export-A` (`export-A/corpus/instruments/r44-*.py`), so the instrument under test is itself committed code.

### C1 counter — the frozen command (after-tree vs frozen base)

```
$ python3 corpus/instruments/r44-routed-defects.py --root $S/export-A --baseline $S/export-base
R44-D1 status=fixed detail=correction appended after the row; erratum carries 13/19 + superseded
R44-D2 status=fixed detail=.ufo/waves/round-43/claims-erratum-6.md matched by K17's own escape; mechanism named in the round-44 lesson
R44-D3 status=fixed detail=appended correction states 26 characters with the counting command; history kept
R44-D4 status=fixed detail=planner=L1, L2-floor and residual lines recorded; wave-1 seat count 66 cross-checks
R44-D5 status=fixed detail=leftover absent; emitter and a populated registry committed; export-ref sidecar present
R44-D6 status=fixed detail=final empty line restored; four boxes present
R44-D7 status=fixed detail=registry rows present in corpus/instruments/README.md; SHONEN pointer corrected by append
R44-D8 status=fixed detail=erratum separates the two exits; the 127 is backed by a committed receipt
routed-defects total=8 fixed=8 unresolved=0 exit=0
routed-defects-baseline total=8 fixed=0 unresolved=8
exit=0
```

### C1 counter — do-nothing replay on the frozen base tree

```
$ python3 corpus/instruments/r44-routed-defects.py --root $S/export-base
R44-D1 status=unresolved detail=no appended Correction (round 43 paragraph naming 13/19 + superseded + erratum
R44-D2 status=unresolved detail=no claims-erratum*.md in the round-43 wave dir carries 13/19 + superseded + r43-closure.sh
R44-D3 status=unresolved detail=no appended correction naming the pointer, the full hash and the counting command
R44-D4 status=unresolved detail=LOG.md has no round-44 section
R44-D5 status=unresolved detail=no lane-owned registry emitter at corpus/instruments/wave-registry.py
R44-D6 status=unresolved detail=SHONEN.md does not end with the restored final empty line
R44-D7 status=unresolved detail=corpus/instruments/README.md carries no row for r43-closure.sh, claim-package-check.py
R44-D8 status=unresolved detail=.ufo/waves/round-43/claims-erratum-6.md absent
routed-defects total=8 fixed=0 unresolved=8 exit=1
exit=1
```

### C2 counter — after-tree then frozen base

```
$ python3 corpus/instruments/r44-frontier-count.py --root $S/export-A --expect 26
frontier rows=26 admitted=26
exit=0

$ python3 corpus/instruments/r44-frontier-count.py --root $S/export-base --expect 26
frontier rows=25 admitted=25
frontier expected=26 admitted=25 verdict=SHORT exit=1
exit=1
```

### SOURCES census — live lane (the exact commanded invocation)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
```

Reproduction verdict: all four instrument runs and the census **reproduce byte-identically to the committed receipts** (`controls/c1-counter-after.txt`, `controls/c1-counter-baseline.txt`, `controls/c2-frontier-counter.txt`, `controls/sources-census-after.txt`). No output was fabricated or trimmed.

---

## 2. Falsification findings

**Summary: the two counters reproduce and the do-nothing base correctly fails, so the claims' mechanical kill rules are not falsified. But I falsified the C1 counter's own stated property — "NOT A MARKER COUNTER … a tree carrying only prose markers is rejected" — for six of its eight limbs, and I found real evidence-discipline gaps the counters cannot see. Findings below are verdict-accurate; where the claim holds, I say so.**

### F1 — The C1 counter is marker-tolerant on 6 of 8 limbs (falsified its own stated property)

The counter's docstring asserts a limb passes "only when it can point at a committed artifact that carries the measured content, not merely at a sentence that says the defect was fixed," and the committed lesson (`corpus/lessons/round-44.md:80-88`) says "a tree carrying only prose markers is rejected." I built an *independent* hollowing battery — different from the lane's 11-mutant selftest, which only exercises *deletion* — that leaves the prose markers in place and hollows only the bound artifact:

| mutant (built on the committed tree) | counter verdict |
|---|---|
| hollow `.ufo/waves/round-43/claims-erratum-6.md` to bare marker sentences (keep "13/19", "superseded", "r43-closure.sh", "127"+"exit=2"+"different command") | **fixed=8 exit=0** |
| hollow `LOG.md`'s round-44 section to the bare tokens "planner=L1 / L2 floor / residual / wave 1 seats: 66" | **fixed=8 exit=0** |
| replace `wave-registry.txt` `names=` with 66 placeholder names ("Seat01…Seat66") | **fixed=8 exit=0** |
| replace `wave1-results.json` with `{"seats":66,"results":[]}` (empty results list) | **fixed=8 exit=0** |
| delete **every** committed `.ufo/waves/round-44/wave1/*.md` seat report | **fixed=8 exit=0** |
| replace SHONEN.md's boxes with four empty `- [ ]` boxes | **fixed=8 exit=0** |
| hollow `corpus/instruments/README.md` rows to bare names (keep "r43-closure.sh", "claim-package-check.py", "r44-routed-defects.py" as substrings) | **fixed=8 exit=0** |
| hollow `controls/missing-suite-base.txt` to the two tokens `exit=127` + `ab98fac9` | **fixed=8 exit=0** |

Only three limbs have a genuine substantive binding: **D1** (hollowing SCORECARD.md's correction paragraph → unresolved), **D2** (removing K17's `claims-erratum` escape → unresolved), **D3** (hollowing the lesson's correction → unresolved, matching their selftest). D2/D4/D5/D6/D7/D8 pass on hollowed artifacts; D8's receipt is checked only for the tokens `exit=127` and `ab98fac9`, not that a measurement was run. Concretely, **a round-44 tree that carried the SCORECARD correction, a token-level erratum, a K17 escape and a stub results file would print `fixed=8 unresolved=0 exit=0` with zero wave-1 evidence** — exactly the false-green class M44-7 recorded against the attempt-1 draft counter.

### F2 — `--baseline` is decorative; the counter does not itself enforce the kill rule

`r44-routed-defects.py main()` (lines ~540-560 of the committed file) prints `routed-defects-baseline …` when `--baseline` is given but **never compares** and does not factor it into the exit code: `return 0 if unresolved == 0 else 1` uses only `--root`. Passing `--baseline <a-different-fixed-tree>` would still print exit=0 and a matching "baseline" tally, or `--baseline` can be omitted entirely. The C1 kill-rule clause "a do-nothing replay … cannot report all 8 fixed" is satisfied only by running the tool a second time — which I did (§1, exit=1 at base). The frozen claim's stated counter `… --root <export> --baseline <frozen-base>` is therefore weaker evidence than it reads: the baseline flag buys optics, not a check.

### F3 — The C2 counter measures only the status cell; it does not verify the frozen kill rule's conjuncts

C2's kill rule requires "F26, its captured source, knowledge entry and registry row all land and the non-author gate agrees." The counter is a status-cell counter:

- deleting `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` (F26's knowledge entry) → still `admitted=26 exit=0`;
- deleting S069's row from `corpus/SOURCES.md` → still `admitted=26 exit=0`;
- appending a stray `| F27 | … | admitted |` row outside the frontier table inflates the count to 27 (no table-section scoping);
- flipping F26's status cell to `proposed` correctly reports 25 (the cell *is* read).

So `admitted=26 exit=0` is compatible with a tree where F26's knowledge entry and source row are absent. The frozen counter's frontier regex is genuinely defective (replayed: `0` at base and after — status is the third cell, regex expects it second), but the replacement counter's 26 does not certify the claim's full conjunct either; it is a counting instrument, and the committed lesson already describes it as a "diagnostic" (`round-44.md:114-115`).

### F4 — The SOURCES census is non-discriminating for C2 (exit 0 at the frozen base too)

`validate` exits 0 at the frozen base export with the same two warnings:

```
$ sources-census.sh validate --root …/export-base
export-base	W04	S028 …; export-base	W04	S029 …; export-base	ok …/export-base/corpus/SOURCES.md
exit=0
```

(identical W04 rows on the committed tree and the live lane — §1). The C2 clause "SOURCES census validates exit 0" therefore cannot separate before from after; it is an invariant, not a measurement of the move. For completeness the census *tallies* do move correctly: `rows 68→70, tier.A 62→63, status.mined 55→56, status.rejected 13→14` (`census` mode on both exports).

### F5 — Registry `seats=66` counts dispatched seats, not completed seats; 12 seat reports are absent

`wave-registry.py` regenerated the committed `wave-registry.txt` byte-identically (`diff` → identical, `exit=0`) and is fail-closed on an empty results list (`exit=2`). The D5 cross-check is against the same-commit `wave1-results.json` (seats=66, results=66), so it is self-referential within the commit and cannot see that the seats' reports are not on disk:

- registry `names=` lists 66 distinct names;
- committed `.ufo/waves/round-44/wave1/*.md` files: **54**;
- 12 registered seats have no committed report: `R44Review4, R44Review6, R44Review12, R44Review17, R44Critic5, R44Mutant1, R44Scribe1, R44Scribe2, R44Scribe3, R44Scout4, R44Scout5, R44Conn2`;
- two of those — `R44Critic5` (a critic seat, part of the attack cohort) and `R44Mutant1` (a mutation-tester) — hold only narration in `wave1-results.json` (output_len 132 and 145 chars: "I'll start by reading…" then nothing); `R44Scout4`, `R44Scout5` likewise carry no finding.

`seats=66`/`names=66` is therefore a *dispatch* census, and the counter's D4/D5 limbs assert `wave 1 seats: 66` against the same file the registry was emitted from — a circular confirmation, not an independent count. (Minor label defect: the committed registry's `attack_seats=40 (60.6%) = reviewer+critic+mutation-tester+security-reviewer` arithmetic is right, 20+12+8=40, but `security-reviewer` is a role with zero seats — a stale label carried into committed bytes.)

### F6 — The committed narrative is internally mixed about whether the claims are certified

At `8063547` the committed files say different things at once (all committed, all verified in the export):

- `SCORECARD.md:1697-1698` (committed move-log rows): `| 44 | depth:verifiability | 4 | 4 held; C1 unverified, no delta |` and `| 44 | coverage | 8 | 8 held; C2 unverified, no delta |`;
- `SCORECARD.md`'s appended "## Round-44 capability disposition" and the committed `.ufo/waves/round-43/claims-erratum-6.md` (lines 11-20): "neither frozen claim is admitted as a score-bearing result… C1 is unverified… C2 is unverified… Round-44 score changes: none… Planned evidence gates for round 45";
- `LOG.md` attempt-1 section: "C1 is unverified… C2 is unverified… No score change is claimed"; attempt-2 section and `corpus/lessons/round-44.md:69-119` say "the two claims measured".

No verdict inflation exists in the *committed* tree (the score is held at 4/8/9 and the "unverified" language is dominant), but the round's evidence discipline is not clean: the same commit that lands a `fixed=8 exit=0` counter also files a score disposition and an erratum declaring the claims unverified and planning the "real" verifier for round 45. A later reader grepping the tree gets both messages. (Context, not committed evidence: the lane working tree currently carries an *uncommitted* `SCORECARD.md` delta — `M 15+0-` — appending attempt-2 rows that claim "**measured**" and supersede the "unverified" disposition; F1 above is the attack on that in-flight basis.)

### F7 — `r44-frontier-count.py` is not registered in the instruments README

`corpus/instruments/README.md` at `8063547` registers `r43-closure.sh` (L990), `claim-package-check.py` (L991), `r44-routed-defects.py` (L992) and `wave-registry.py` (L993) — but `grep -c 'r44-frontier-count'` → **0**. The D7 limb does not require it, so D7 still reads `fixed`, but the C2 counter — one of the round's two new instruments — is unregistered, a small completeness hole in the same repair that was routed for pointer/registration hygiene (§6.7).

### Checks that hold (no falsification)

- Do-nothing replay fails cleanly for both counters (§1: C1 exit=1 with 8 unresolved, C2 exit=1 with 25 admitted).
- **Append-only is real**: `git diff --numstat 5ab3a60 8063547` shows 0 deletions on SCORECARD.md (17/0), LOG.md (23/0), SHONEN.md (11/0), corpus/README.md (20/0), corpus/SOURCES.md (7/0), corpus/lessons/round-43.md (10/0), corpus/lessons/round-44.md (152/0), corpus/instruments/README.md (16/0); `git diff --name-status` → 102 A, 10 M, **0 D**.
- **D8 receipt independently reproduced**: at `ab98fac9` (the base the receipt names) `bash corpus/instruments/r43-closure.sh` → `bash: corpus/instruments/r43-closure.sh: No such file or directory`, exit **127**; `ls` → exit **2**. At the round-44 frozen base `5ab3a60` the suite exists and refuses a plain run with exit 2 — a subtle distinction the erratum gets right (the 127 belongs to `ab98fac9`, the 2 to the control's `ls`), and it matches `controls/missing-suite-base.txt`.
- D6: `SHONEN.md` ends with `\n\n` and carries the four boxes. D4's cross-check numbers are consistent (LOG's `wave 1 seats: 66` = `wave1-results.json` seats=66 = registry seats=66).
- S069 is tier A, status `mined`, used-by `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` (present, 5843 B); S070 tier C `rejected`; the capture manifest binds sha256 `0932279c…`, 45681 bytes, 1132 lines, five located quotes.
- The live lane's corpus files the counters read (`SOURCES.md`, `README.md`, `lessons/*`, `SHONEN.md`, `LOG.md`, `corpus/knowledge/` = 63 files) are byte-identical to the committed export — the only working-tree delta is the uncommitted SCORECARD append noted in F6, so the receipts are not shadowed by uncommitted content.

## 3. Limitations

- I verified the eight §6 defects only to the level the counter checks plus the substantive checks above; I did not re-grade the six per-limb round-43 transcripts or the r43 suite's own limbs.
- The marker-tolerance findings (F1, F3) falsify the *counters'* strength and the "measured" language, not the committed tree's honesty — the committed artifacts themselves are real (D8's 127, the emitter's byte-identical registry, append-only history).
- F5's "12 missing reports" measures `.md` files in `wave1/`; all 66 outputs exist inside `wave1-results.json`, so the missing files are a committed-report completeness gap, not missing data.
- The non-author admit/reject spot-check required by C2's kill rule is by the lane's own account deferred to the closure (`.ufo/waves/round-44/nonauthor-spotcheck-packet.md` is a packet for the closure, not an adjudication); whether that satisfies the kill rule is the integrator's call, not this seat's.
- The uncommitted SCORECARD delta (F6) was read but is not committed evidence; if it lands, F1's demonstration directly attacks its "measured" phrasing.

## 4. Bottom line for the integrator

Both counters run read-only over committed bytes and reproduce their committed receipts exactly; the do-nothing base fails for both; the census exits 0 with the same W04 S028/S029 pair at base and after. **The counters' *measurements* are real.** What I falsified is the *strength* of the instruments and the "measured" framing: the C1 counter accepts marker-only artifacts on 6/8 limbs and its `--baseline` flag is decorative; the C2 counter certifies a cell count that survives deleting F26's knowledge entry and source row; the census exit-0 is invariant; and the committed tree itself still carries "C1/C2 unverified, no score delta" as its dominant disposition. Recommend the integrator treat C1's after-state as *repair-present but verifier-thin* and C2's as *count-true but kill-rule-incomplete* (non-author spot-check outstanding).

Report: .ufo/waves/round-44/wave2/R44W2Exec03.md
