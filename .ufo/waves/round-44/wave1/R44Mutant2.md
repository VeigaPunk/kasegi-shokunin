# R44Mutant2 — one-limb mutant for finding report-only correction text not present in committed records

seat: R44Mutant2 (mutation-tester, leaf) · round 44 · lane `kasegi-shokunin`
item: *Design a one-limb mutant for finding report-only correction text not present in committed records.*
lane HEAD at probe: `66314015122b9aa32dc40f2f1815df56624c26d1` ("round-44: freeze claims and validated wave"); frozen base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`.
mode: read-only on the lane. No lane file created/modified/deleted except this report. No git/jj/index mutation, no commit, no push. Scratch `/fast/scratch/hyaku/kasegi-r44/R44Mutant2/` (`git archive` exports + fixtures + transcripts), deleted on exit (§9).
tools installed/updated: **none** (bash, python3 stdlib, git only; nothing added to any PATH directory; pacman untouched per host pause).

Subject = routed defect **R43-1/2** (`corpus/lessons/round-43-verifier-spotcheck.md:101-102`): `closed=13/19` is asserted by the lane's committed records but **no committed run binds it and no committed correction names it**; no existing check can see it — K18 excludes `SCORECARD.md` as a quote source (`corpus/instruments/r43-limbs/k18-transcript.sh:18-20`) and K17's escape reads only `claims-erratum*.md` (`k17-claims-before.sh:28-35`). "Report-only correction text" here means: a value whose only support lives in report channels (seat receipts / `.ufo/reports/`), i.e. the correction that would settle the record exists only as prose.

## 1. Measured subject facts (read-only, at HEAD 6631401)

| fact | command | observed |
|---|---|---|
| `closed=13/19` asserted in the round-43 move-log row | `git show HEAD:SCORECARD.md \| sed -n '1685p'` | row `| 43 | … | base `ab98fac9` `closed=13/19 exit=1` with exactly K14-K19 open …` |
| same literal in the frozen claim cell | `git show HEAD:.ufo/waves/round-43/claims.json \| sed -n '41p'` | C1 `after`: `base export closed=13/19 exit=1` |
| no committed transcript binds it | `git grep -nE '^closed=13/19 exit=' HEAD -- .ufo/waves/round-43/final-gates .ufo/waves/round-43/c1-controls .ufo/waves/round-42` | rc=1 (zero hits) — its only summary lines are `closed=19/19 exit=0`, `18/19`, `12/13` |
| no committed erratum names it | `git grep -n '13/19' HEAD -- .ufo/waves/round-43/claims-erratum-1.md` (and all `claims-erratum*.md`) | rc=1 (zero hits; round-44 has no erratum at all) |
| its only other support is report prose | `git grep -c '13/19' HEAD -- .ufo/waves/round-43/w1` | 23 seat-receipt files carry the literal (`ExecCarryChecks.transcript.txt`, `CritBaselineEscape.md`, …) — all under `w1/`, which K18 classifies as claims-not-evidence |
| round-44 tree carries no correction | `ls .ufo/waves/round-44/` | `claims.json controls wave1*` only; `wave1/` = dispatch/spec/registry + seat receipts (incl. this one); no erratum, no counter |
| no candidate counter exists at HEAD | `git ls-tree -r --name-only HEAD corpus/instruments \| grep -E 'r44|report-only'` | rc=1, no match; C1's `r44-routed-defects.py` is absent |

Bound tokens the same limb re-derives at HEAD (46 evidence dirs): `closed=13/13 exit=0` (frozen `.ufo/waves/round-42/` archive), `closed=19/19 exit=0` (`final-gates/all-gates.at-Y.txt:25`), `selftest cases=19 failures=0` (`all-gates.txt:45`, `all-gates.at-Y.txt:45`), `closed=12/13 exit=1` (`c1-controls/do-nothing.txt:25`).

## 2. Candidate pristine limb (authored for this probe — not landed lane code)

`k20-report-only.sh`, sourceable `check_k20 <export>` printing exactly
`K20 payload=asserted=<a>,bound=<b>,superseded=<s>,report-only=<r>,unbacked=<u> closed=0|1`, exit 0/1/2, read-only. Contract:

1. **Population**: every summary-shaped `closed=n/m` (token followed by ` exit=k`) and `selftest cases=n failures=k` in (a) a `SCORECARD.md` row whose first cell is a round number ≥ 43, and (b) any `before`/`after` cell of `.ufo/waves/round-NN/claims.json` with NN ≥ 43 (claims grade `closed=` only — a `selftest` literal there may be another instrument's, e.g. `selftest cases=10 failures=0` for the claim-package gate).
2. **bound** = the token is a summary-shaped line in an evidence channel: `.ufo/waves/round-*/final-gates|`, `c1-controls/`, `c2-controls/`, plus the frozen `.ufo/waves/round-42/` archive.
3. **superseded** = a committed correction names it: a `Correction (round N)` line in a committed record channel (`SCORECARD.md`, `SHONEN.md`, `LOG.md`, `corpus/QUALITY.md`, `corpus/lessons/*.md`) or a `claims-erratum*.md` block carrying `superseded`.
4. Neither → **red**; `report-only` counts it when the token also occurs in a report channel (`.ufo/waves/round-NN/w*/` or `.ufo/reports/`), else `unbacked`. `closed=1` iff `asserted>0` and `report-only=unbacked=0`.
5. Scope exclusions: `corpus/lessons/*.md` are not quote sources (the verifier's own audit prose names unbacked values on purpose); the export is the committed tree (`git archive`), so a working-tree edit is indistinguishable from a committed byte — same convention as K14–K19.

pristine sha256 `461ef437587f59ff56a3a55eb7a174d76d0a9d5c94ea752153798d149bb656dc`.

Selftest (6 bounded fixtures under scratch, each asserting an exact payload): `defect` (asserted=5,bound=3,report-only=2,closed=0), `fixed` (+erratum → superseded=2,closed=1), `report-only-fix` (same correction text in `w1/FixReport.md` → still closed=0), `unbacked` (no seat receipt → unbacked=2,closed=0), `clean` (closed=1), `lesson-audit` (lesson names `13/19` → still closed=1). Observed: `selftest cases=6 failures=0`.

## 3. Detector matrix — same bounded detector, pristine vs mutated vs restored bytes

| run | export | stdout | exit | verdict |
|---|---|---|---|---|
| pristine | HEAD `6631401` | `K20 payload=asserted=7,bound=5,superseded=0,report-only=2,unbacked=0 closed=0` | 1 | **red** — `closed=13/19` at `SCORECARD.md:1685` and `claims.json[C1.after]` |
| pristine | base `5ab3a60a` | identical payload `asserted=7,bound=5,…,report-only=2 closed=0` | 1 | red at base too (defect is inherited, never fixed) |
| pristine ×2 | HEAD | byte-identical stdout, `closed=0` | 1 | deterministic; a do-nothing replay cannot reach green |
| pristine | HEAD + committed `claims-erratum-2.md` naming `closed=13/19` superseded | `asserted=7,bound=5,superseded=2,report-only=0,unbacked=0 closed=1` | 0 | green — the routed append-only fix closes it |
| pristine | HEAD + same correction text in `.ufo/waves/round-43/w1/FixReport.md` | `asserted=7,bound=5,superseded=0,report-only=2 closed=0` | 1 | **red — the exact subject of this item: correction text that lives only in a report does not resolve the record** |

| mutant (one-line change to the limb) | sha256 | limb selftest | same mutant on real HEAD export | verdict |
|---|---|---|---|---|
| M1 *report prose counts as evidence*: `elif tok in report_blob: rcount += 1` → `bcount += 1` | `6b31644e…` | `cases=6 failures=2` (`defect`, `report-only-fix`) | `payload=asserted=7,bound=7,…,closed=1` rc=0 — falsely reports the defect resolved | **KILLED** by `defect`/`report-only-fix` fixtures |
| M2 *supersede escape removed*: `elif tok in committed_corrections: scount += 1` → `pass` | `21b61fb4…` | `cases=6 failures=1` (`fixed`) | red (still correct on the real defect) | **KILLED** by `fixed` fixture |
| M3 *unbacked counts as bound*: `else: ucount += 1` → `bcount += 1` | `6bfef7f3…` | `cases=6 failures=1` (`unbacked`) | red (real defect stays report-only, not unbacked) | **KILLED** by `unbacked` fixture |

Restoration: `k20-restored.sh` sha256 `461ef437587f59ff56a3a55eb7a174d76d0a9d5c94ea752153798d149bb656dc` = pristine (byte-identical after mutation probes).

M1 is the counter-mutant shape the wave cares about: on real committed bytes it converts the limb green (`bound=7`) purely by treating report prose as evidence — and the limb's own bounded fixtures kill it. That is the measured proof the `report-only` cell is behavior-bearing, not decoration.

## 4. Do-nothing discrimination

The frozen control (`controls/do-nothing.txt`) records: eight routed defects present at base, no r44 correction, no r44 counter. At **both** `5ab3a60a` and `6631401` the pristine limb prints `closed=0` on the same two `closed=13/19` occurrences; the only path to green observed is a committed correction record (V1) — writing the same text to a report (V2) leaves it red. So a do-nothing replay cannot report the routed defect resolved, and the fix route the limb measures is exactly the append-only route §6 prescribes ("add the missing erratum paragraph … rather than widening K18"). A committed `final-gates/` transcript printing `^closed=13/19 exit=` would also close it (the alternative "commit a base run" route) — neither route is report-only.

## 5. Design finding — rejected second clause (quote-vs-statement ambiguity)

An earlier draft also graded "`Correction (round N)` statements that live only in report channels". Dropped after measurement: at the frozen base that population contains 10 line-start correction statements inside `.ufo/waves/round-43/w1/*.transcript.txt` fixture runs plus 4 more tokens (`closed=10/13`, `13/13`, `9/13`, `selftest cases=13 failures=3`) on mid-line quotations in seat drafts (`ExecSelftest19.cases.txt:18`, `ExecSelftest19.sh:438`, `ScoutR42Defects.md:139`, `ScribeLessonDraft.round-43-lesson.md:41`) — i.e. a correction *quotation* cannot be distinguished from a correction *statement* from the bytes alone, so the clause reds on prose it is not judging. The decidable form is kept: grade the **value's support** (`report-only`/`unbacked`), not the correction's grammar.

## 6. Limits

- Design probe, not the C1 counter: it falsifies nothing C1 already says (defect 1 is unresolved at base and at the freeze commit — consistent, not new); it shows the missing limb's shape and that the routed fix is falsifiably decidable. No verdict on C1 closure and no coverage of the other seven routed items (defect 3's "29-character" numeral is prose, outside the token grammar; defects 4–8 are not run values at all).
- Trusts the export (`git archive` = committed bytes); cannot distinguish a working-tree edit. During this probe `git status --porcelain --untracked-files=no` went 0→7 (sibling executor appends to `SCORECARD.md`, `corpus/README.md`, `SOURCES.md`, etc.); the limb is immune because it grades exports, but a landed version must pin the export ref it grades.
- `MIN_ROUND=43` is the routed window; earlier rounds' move-log rows carry older history (K18's stated exclusion reason) and are intentionally out of population.
- A committed transcript inside `w1/` can never bind (seat receipts are claims, not evidence — K18's rule, kept deliberately); the binding routes are `final-gates/`, `c1-controls/`, `c2-controls/`.
- Id `K20` is provisional and collides with sibling probe `k20-tmp-leftover.sh`; a landed limb needs a free id.

## 7. Scratch / writes / tools

Scratch `/fast/scratch/hyaku/kasegi-r44/R44Mutant2/` (156 MB `export-head`, 156 MB `export-base`, 3 export variants, selftest trees, `transcript-*.txt`) deleted on exit; deletion verified by `test -d` → rc=1. No installs, no PATH-directory writes, no fleet-root tracked file touched, no lane production edit — only this report.
