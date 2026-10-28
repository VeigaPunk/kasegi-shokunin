# R44Simplifier1 — smallest non-duplicative shape for measuring C1's eight frozen defects

seat: simplifier (leaf) · round 44 · lane `kasegi-shokunin` · item: *suggest the smallest
non-duplicative implementation shape for measuring C1's exact eight frozen defects*
frozen base: `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` (lane HEAD at seat start
`66314015122b9aa32dc40f2f1815df56624c26d1` = base + the round-44 freeze commit)
mode: **read-only**. No lane file was written except this report; no git/jj/index mutation,
no pacman, no tool install (python3 3.14.8, git, GNU tar 1.35 only). Scratch:
`.ufo/scratch/kasegi-r44/R44Simplifier1/` (`$HYAKU_SCRATCH` is unset in this shell; the lane
scratch root is `.ufo/scratch/`), removed on exit — see §8.

Every measurement below is over **committed bytes** (`git show <ref>:<path>` or a
`git archive <ref> | tar -x` export in scratch), never over the working tree. That matters:
live sibling seats currently hold uncommitted edits to `SCORECARD.md`, `SHONEN.md`,
`corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/knowledge-expected.txt` and
untracked drafts under `.ufo/waves/round-44/controls/`; none of that is evidence.

---

## 1. The reuse boundary, measured (this decides "non-duplicative")

The question is not "write a counter" but "what may the counter *not* re-derive". The eight
defects are narrative/hygiene routings from the non-author spot-check
(`corpus/lessons/round-43-verifier-spotcheck.md` §6). Six of the round-43 limbs already grade
*adjacent* classes, so the first move is to measure which of them are already red at the
frozen base — a gate that is green at the base cannot be a red-before control for anything.

Commands (export = `git -C <lane> archive 5ab3a60a | tar -x -C base-export`):

```
bash corpus/instruments/r43-limbs/k14-corrections.sh      base-export
bash corpus/instruments/r43-limbs/k15-wave-narrative.sh   base-export
bash -c 'source .../k16-placeholder.sh; check_k16 base-export'
bash corpus/instruments/r43-limbs/k17-claims-before.sh --tree base-export
bash corpus/instruments/r43-limbs/k18-transcript.sh       base-export --verbose
bash -c 'source .../k19-freeze.sh; check_k19 base-export'
```

| gate | payload at the frozen base `5ab3a60a` | usable as a C1 red control? |
|---|---|---|
| K14 | `literals=3,stale=0,superseded=2,live=corrections=38,groups=4 closed=1` | **no** — green |
| K15 | `sentences=5,unbacked=0,superseded=3,mismatch=0 closed=1` | **no** — green |
| K16 | `sections=509,promises=1,fenced=0,unresolved=0 closed=1` | **no** — green |
| K17 | `claims=21,tokens=5,verified=4,superseded=1,unbacked=0,quoted=2 closed=1` | **no** — green |
| K18 | `quotes=68,bound=52,report-only=1,superseded=14,unbound=1 closed=0`; unbound token = `selftest cases=10 failures=9 at corpus/lessons/round-43-verifier-spotcheck.md:61` | **no** — red, but on a *ninth* item that is not one of the eight |
| K19 | `freeze=present,order=ok,sha=match closed=1` | **no** — green |

Consequence, and the single most important design constraint:

- **Do not compose the counter out of the limbs.** Five are green at the base, so they cannot
  discriminate do-nothing; K18 is red on an item outside C1's eight (the spot-check lesson's own
  quoted `failures=9`), so importing it would make C1 unsatisfiable without editing a non-author
  document. The counter must grade the eight carriers directly.
- **Do not widen any limb.** Defect 2 explicitly forbids widening K18's scope, and widening K17
  to `after` cells would red every historical after cell (22 claims in the population).
- The counter is therefore the **only changed gate**, which keeps C1's "at least one red-before
  control per changed gate" cheap: one baseline run covers it, plus one `--only D<n>` mutant per
  defect.

### 1.1 The defect-2 remedy in §6 is false as written (measured)

§6.2 says: *add the missing erratum paragraph (K17's existing escape then covers it)*. It does
not. `corpus/instruments/r43-limbs/k17-claims-before.sh:326` is `if field == "after": continue`
— after-cell tokens are never collected, and the erratum escape at `:343` is only consulted for
a *before* token that failed receipt binding. `closed=13/19` lives in the round-43 C1 **after**
cell (`.ufo/waves/round-43/claims.json:41`). Probe on a copy of the base export with an erratum
that names the token:

```
cp -a base-export k17-probe
cat > k17-probe/.ufo/waves/round-43/claims-erratum-9.md <<'EOF'
- **E9 — token `closed=13/19` (round-43 C1 `after`).** Superseded by the per-limb base result.
EOF
bash corpus/instruments/r43-limbs/k17-claims-before.sh --tree k17-probe
→ K17 payload=claims=21,tokens=5,verified=4,superseded=1,unbacked=0,quoted=2 closed=1
```

Byte-identical to the unmodified base run (`tokens=5`, `superseded=1`): the erratum changes
nothing. So defect 2's fix must be graded by the **new** counter (or the erratum must be
accompanied by a check that reads `after` cells and SCORECARD table rows); "K17 covers it" is
not a measurable claim.

---

## 2. The eight carriers at the frozen base

`git show 5ab3a60a:<path>`; line numbers are the base file's.

| id | carrier (base) | literal present | class |
|---|---|---|---|
| D1 | `SCORECARD.md:1667`, `:1685` (both `|` table rows, outside any fence) | `closed=13/19 exit=1` (2 occurrences) | contradicted |
| D2 | `.ufo/waves/round-43/claims.json:41` (C1 `after`) + K17 `:326` / K18 scope `:12-22` | `closed=13/19` ungraded | absent (no erratum) |
| D3 | `corpus/lessons/round-43.md:90`, `:101` | `29-character prefix`; real prefix `c6ae07c6a541e0e96d0040afb6` = **26** chars (`python3 -c "print(len('c6ae07c6a541e0e96d0040afb6'))"` → 26) | contradicted |
| D4 | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-43/kasegi.md` (fleet repo, commit `fdf719a9`) | `grep -ci planner` → 0; `grep -ciE 'residual|L2 floor'` → 0 | absent (round-44 report) |
| D5a | `.ufo/waves/round-43/w1-REGISTRY.txt:7` | `names=` empty while `:4 seats=73` | contradicted |
| D5b | `.ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt` | `grep -c export-ref` → 0 (the sibling `r42-at-de09313-run.txt:2` does name `export-ref=de09313e8ed…`) | contradicted |
| D5c | `.ufo/waves/round-43/final-gates/all-gates.at-Y.txt.tmp` | untracked → `git ls-tree -r HEAD | grep -c '\.tmp$'` → 0, so **invisible to any export** | absent |
| D6 | `SHONEN.md` tail | `git show 5ab3a60a:SHONEN.md | tail -c 12 | od -c` → `t a y s \` [ ~ ] \` . \n` — exactly one newline | contradicted |
| D7 | report `:91` claims registration in `corpus/instruments/README.md`; `git show 5ab3a60a:corpus/instruments/README.md | grep -c 'claim-package-check\|r43-closure'` → **0** | 0 rows | contradicted |
| D8 | `.ufo/waves/round-43/claims.json:38` | `the r43 suite is absent at base (exit 127)`; the cited control `.ufo/waves/round-43/c1-controls/do-nothing.txt` §A prints `exit=2` (from `ls`), never `127` | contradicted |

No committed run of the landed suite at base exists to retire D1:
`grep -rl 'export-ref=ab98fac9' .ufo/waves/round-43/` hits only `c1-controls/do-nothing.txt`
(the r42 stand-in, `suite-sha256=fca5ae62…`) and seat receipts;
`grep -rn 'closed=13/19' .ufo/waves/round-43/final-gates/` → 0 lines.

---

## 3. Proposed shape (the answer)

**One file, one process, no new directory, no new dependency:**
`corpus/instruments/r44-routed-defects.py` (~260–300 lines, python3 stdlib only, read-only).

```
python3 corpus/instruments/r44-routed-defects.py \
    --root <export-dir|ref> [--baseline <export-dir|ref>] \
    [--lane DIR] [--scratch DIR] [--report PATH] [--report-ref REF] \
    [--only D1,D5] [--selftest]
```

`--root` and `--baseline` accept a directory (export) **or** a ref; a ref is materialised with
the same three lines the lane already uses (`git -C <lane> archive <ref> | tar -xf -` — cf.
`k17-claims-before.sh:576`, `r43-closure.sh:98-107`), into `--scratch`, deleted on exit. That
makes the frozen command usable verbatim as `--root HEAD --baseline 5ab3a60a…` and keeps the
graded bytes committed bytes. Exit: `0` iff `unresolved=0` (and, when `--baseline` is given,
`baseline-red=8`); `1` otherwise; `2` usage; a non-resolving ref prints `ref-not-found` and
exits `1` (never a vacuous pass — the r43 suite's rule).

### 3.1 Shared core — five primitives, one implementation each (~45 lines)

| primitive | used by | note |
|---|---|---|
| `read(root, rel)` | all | returns `None` for absent; absent is `resolved=0`, never a skip |
| `outside_fence(text)` | D1, D3, D8 | ``` toggling only; no markdown parser |
| `correction_naming(text, token)` | D1, D3 | later line, outside a fence, `^[-* ]*Correction \(round (43|44)` and naming `token`; returns `lineno`. Same rule as K14/K15/K16 — documented as *the* rule, not a second convention |
| `whole_token(text, rx)` | D1, D8 | R41 boundaries: `(?<![0-9A-Za-z_/-])…(?![0-9A-Za-z_/-])` |
| `names_count(s)` | D5a | comma-separated names, empty → 0 |

Nothing else is shared. In particular there is **no** correction-ledger engine, no fence-aware
literal grader, no token classifier: those are K14's, and re-deriving them is the duplication
this shape exists to avoid.

### 3.2 One predicate per defect (each returns `(resolved, evidence)`)

| id | minimal predicate | resolves when |
|---|---|---|
| D1 | every `closed=13/19` occurrence in `SCORECARD.md` **outside** a fence and **not** on a `Correction (` line is named by `correction_naming(SCORECARD, "13/19")`; **or** a committed base run exists: a file under `.ufo/waves/round-43/final-gates/` (or round-44) containing `export-ref=ab98fac9`, `suite-sha256=a832908e` and a summary `closed=<n>/19` line | correction line, or base run |
| D2 | a `claims-erratum*.md` blank-line paragraph names `closed=13/19`, carries `superseded`, **and** names the round-43 C1 `after` cell (contains `after` or `C1`) | the after-cell literal is formally retired — the only visibility route left after §1.1 |
| D3 | `corpus/lessons/round-43.md` has `correction_naming(text, "29-character")`, the correction states `26`, and `len(prefix_token)==26` is re-computed from the token in the same file | self-checking numeral (a wrong replacement numeral reds) |
| D4 | the report file contains a `planner=L1`-shaped whole token **and** a line carrying `L2 floor`/`residual` with an integer; with `--report-ref`, `git -C <fleet> cat-file -e <ref>:<rel>` succeeds | two lines + commit identity |
| D5 | **conjunction of three:** (a) a committed control carries `source=.ufo/waves/round-43/w1-dispatch.json`, `seats=<n>`, `names=` with exactly `<n>` names, and the name set equals the dispatch's member set re-derived by the counter; (b) a committed file carries `export-ref=de09313e8ed…` **and** the literal `r42-at-de09313-selftest.txt`; (c) the export has no `*.tmp` under `.ufo/waves/` **and** a committed control records the working-tree `find … -name '*.tmp'` with empty output | a∧b∧c; payload names which leg failed |
| D6 | `SHONEN.md` endswith `\n\n` | trailing-newline count 2 (base 1) |
| D7 | `corpus/instruments/README.md` contains both whole tokens `claim-package-check.py` and `r43-closure.sh` | 2 appended rows; the report prose is **not** parsed |
| D8 | the round-43 C1 `before` `127` token is retired by either (a) a `claims-erratum*.md` paragraph naming `127` with `superseded`, or (b) a committed control printing `exit=127` **and** carrying `base=ab98fac9` | erratum, or a measurement of the absent path |

D5 is one defect with three legs, so the payload must name the failing leg
(`D5 resolved=0 evidence=a=1,b=0,c=1`) — otherwise "8 of 8" hides a partial.

### 3.3 Payload and transcript (one committed file binds all eight)

```
r44-routed-defects v1
root=<ref or export-sha256>
baseline=<ref|dir|none>
D1 resolved=1 evidence=SCORECARD.md:1691
...
D8 resolved=1 evidence=control:.ufo/waves/round-44/controls/missing-suite-base.txt
unresolved=0/8
baseline-red=8/8 contradicted=6 absent=2
exit=0
```

One line per defect, sorted, no timestamps, no host paths: a single committed transcript
(`.ufo/waves/round-44/final-gates/r44-routed-defects.txt` plus its baseline run) then binds the
whole C1 claim, and any reviewer can re-open `evidence=<path>:<line>`. The `D<n>` namespace is
deliberately **not** `K<n>` — reusing K numbers would imply the r43 suite grades these.

### 3.4 Selftest — inline, no fixtures directory (~80 lines)

Eight synthetic mini-trees built from embedded strings (pre-fix bytes red, post-fix bytes
green), plus two degenerate controls: an always-`resolved=1` stub must be rejected by the
baseline mode, and an empty tree must yield `unresolved=8`, not `0`. Output
`selftest cases=8 failures=0`. No `corpus/instruments/fixtures/` tree, no
`knowledge-expected.txt` change (the counter adds no knowledge entry — C2 owns that).

### 3.5 Size budget

core 45 + 8 predicates ≈ 120 + CLI/export ≈ 40 + selftest ≈ 80 → **≈285 lines**. That is the
smallest shape that (i) reads only committed bytes, (ii) does not re-derive any limb, (iii) has
a red control per defect, and (iv) cannot pass vacuously.

---

## 4. Non-duplication ledger

| do not build | owner / proof |
|---|---|
| `corrections=`/`groups=` literal grading | K14 (`stale=0,superseded=2,live=corrections=38 closed=1` at base) |
| wave-dispatch sentence vs results | K15 (`unbacked=0,superseded=3 closed=1`) |
| placeholder-promise sections | K16 (`promises=1,unresolved=0 closed=1`) |
| `closed=`/`failures=`/`cases=` before-token binding | K17 (`tokens=5,unbacked=0 closed=1`); D8 adds only the `exit <n>` key, which K17's `TOKEN_RX` (`:105`) cannot express |
| quote binding for `closed=`/`selftest cases=` | K18 — and see §1: it is red on an out-of-scope token at base, so it must not be a predicate |
| freeze ordering | K19 (`freeze=present,order=ok,sha=match closed=1`) |
| receipt integrity, r42 carry checks | K8, K1–K13 |
| mutation machinery for red-before | K14–K19 mutant harness already exists; per-defect red is a **scratch copy with the appended fix removed** (3 lines in the control transcript), not instrument code |
| report-prose parsing for D7 | grade the README rows (append-only artifact) |
| a round-44 `w1-REGISTRY.txt` requirement | none exists at the freeze; requiring one would invent an artifact |
| a second export/materialise path | `git archive | tar` exactly as `k17:576` / `r43-closure.sh:98-107` |
| new knowledge entry / registry row / census | C2's territory; the counter must not touch `SOURCES.md`, `knowledge/`, `knowledge-expected.txt` |

---

## 5. Do-nothing discrimination

`--baseline 5ab3a60a` must print `baseline-red=8/8` and split the reds by cause:

- **contradicted at base (6):** D1 (two table rows carry the literal), D3 (numeral 29 present),
  D5 (a: `names=` empty; b: no `export-ref`), D6 (one trailing newline), D7 (0 README rows),
  D8 (`exit 127` unbacked; the cited control prints `exit=2`).
- **absent at base (2):** D2 (no erratum naming the after cell), D4 (the round-44 report does not
  exist yet).

The split is the anti-vacuity device: a predicate that is only ever "absent" would pass the
baseline test while proving nothing, so the payload must show ≥6 `contradicted` reds, and a
predicate that reads `resolved=1` at the base must exit `1` (`baseline-not-red`). That is also
the degenerate-control rejection: a stand-in printing `resolved=1` for all eight yields
`baseline-red=0/8` → exit `1`, with no extra code.

---

## 6. Falsifications and limitations (state these; do not paper over)

1. **§6.2's remedy is wrong** (§1.1, measured): an erratum paragraph alone changes nothing in
   K17; the counter must own D2, and the report must not claim K17 grades it.
2. **K18 will stay red at the final revision** unless the spot-check's own quoted
   `selftest cases=10 failures=9` (`round-43-verifier-spotcheck.md:61`) is retired. That is not
   one of the eight, so C1 must not absorb it — but a C1 "suite green" claim would be false. The
   counter deliberately does not include K18.
3. **D4's evidence is not lane evidence.** The report lives in the fleet repo
   (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-43/kasegi.md`, tracked at `fdf719a9`).
   C1's wording "one committed read-only counter over committed lane evidence" does not cover
   it, and the frozen counter command has no `--report` argument. Either the counter gains
   `--report`/`--report-ref` (as proposed) or C1's wording must be narrowed. Without
   `--report-ref` the counter can only report `report=uncommitted` → `resolved=0`.
4. **D5c is unobservable in an export.** The leftover was untracked
   (`git ls-tree -r HEAD | grep -c '\.tmp$'` → 0), so "deleted" cannot be proven from committed
   bytes; the predicate can only require (i) no `*.tmp` in the export and (ii) a committed
   working-tree control. At base that control is absent, so D5c is `absent`, not `contradicted`.
5. **The round-44 freeze cites two controls that do not exist.** `.ufo/waves/round-44/claims.json`
   points C1 at `.ufo/waves/round-44/controls/c1-do-nothing.txt` and C2 at
   `…/c2-do-nothing.txt`; `test -e` → both **missing** (the real C1 control is
   `controls/do-nothing.txt`; there is no C2 control). Any counter that reads `claims.controls`
   must treat a missing cited control as unresolved, not as green — and the freeze pointer needs
   repair or the counter needs `--control`.
6. **D5a's emitter is not lane-owned.** `grep -rln 'w1-REGISTRY' scripts/ .omp/` → no writer
   found, and the lane has no `scripts/`; so "fix the emitter" cannot be a lane edit. The
   lane-scoped fix is the correction control the sibling draft already writes
   (`.ufo/waves/round-44/controls/round43-registry-correction.txt`: `source=…w1-dispatch.json`,
   `seats=73`, `names=` non-empty) — the predicate must re-derive the name set from the dispatch
   so a hand-written list cannot pass.
7. **D1's two carriers differ in kind.** Both are `|` table rows outside fences, and a correction
   line that quotes `closed=13/19` (the working-tree draft at `SCORECARD.md:1691` does) must be
   treated as a *quotation*, not a new occurrence — otherwise appending the fix reds the check
   (the K14 self-naming rule, `k14-corrections.sh:28-31`).

---

## 7. Commands run (verbatim, all read-only)

```
git rev-parse HEAD                                        → 66314015122b9aa32dc40f2f1815df56624c26d1
git merge-base --is-ancestor 5ab3a60a… HEAD               → 0 (base is ancestor)
git diff --stat 5ab3a60a… HEAD                            → 6 files, all .ufo/waves/round-44/*
git -C <lane> archive 5ab3a60a | tar -x -C base-export    → export in scratch
git -C <lane> archive HEAD     | tar -x -C head-export
bash …/k14|k15|k16|k17|k18|k19 on base-export             → §1 table
bash …/k17 --tree k17-probe (base + erratum naming 13/19) → tokens=5,superseded=1 (unchanged)
python3 -c "print(len('c6ae07c6a541e0e96d0040afb6'))"     → 26
git show 5ab3a60a:SCORECARD.md | grep -n 'closed=13/19'   → 1667, 1685
git show 5ab3a60a:.ufo/waves/round-43/claims.json | grep -n 'closed=13/19' → 41
git show 5ab3a60a:.ufo/waves/round-43/claims.json | grep -n 'exit 127'     → 38
git show 5ab3a60a:corpus/lessons/round-43.md | grep -n '29-character'      → 90, 101
git show 5ab3a60a:SHONEN.md | tail -c 12 | od -c                           → single \n
git show 5ab3a60a:.ufo/waves/round-43/w1-REGISTRY.txt | sed -n '4p;7p'     → seats=73 / names=
git show 5ab3a60a:.ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt | grep -c export-ref → 0
git show 5ab3a60a:corpus/instruments/README.md | grep -c 'claim-package-check\|r43-closure' → 0
grep -rln 'export-ref=ab98fac9' .ufo/waves/round-43/  → c1-controls/do-nothing.txt + seat receipts only
grep -rn 'closed=13/19' .ufo/waves/round-43/final-gates/ → 0
grep -ci planner /home/vgpnk/Projects/shokunin/.ufo/reports/round-43/kasegi.md → 0
test -e .ufo/waves/round-44/controls/c1-do-nothing.txt → missing
test -e .ufo/waves/round-44/controls/c2-do-nothing.txt → missing
```

## 8. Cleanup

`rm -rf .ufo/scratch/kasegi-r44/R44Simplifier1` after this report is written; the lane tree
gains exactly one file (this report), which is the assigned Report path. No production file, no
git/jj/index, no fleet repo, no sibling repo, no operator config was touched.

## Tradeoff

The shape refuses to reuse the six existing limbs even though they are right there, because five
are green at the frozen base (no discrimination) and the sixth is red on an item outside the
eight (false coupling). The cost is one ~285-line file with a 45-line shared core that duplicates
three tiny primitives (fence toggle, correction-line regex, whole-token boundary) already
implemented in bash three times. The benefit is a counter whose red-before is measured against
the actual carriers, whose baseline run cannot pass vacuously, and whose eight predicates can be
falsified one at a time without touching any existing gate. If a smaller shape is demanded, the
only honest reduction is to drop D4 (report prose) and D5c (untracked leftover) to a
control-transcript-only grade — but that contradicts C1's "0 of those same 8", so it is a claim
change, not a simplification.
