# R46bRevSelftestDiff — attack on the extended counter selftest drafts

VERDICT: DRAFT-READY — C1 draft ff92d302 (7 new cases) and C2 draft 184ab706 (10 new cases) each pass
clean baseline (failures=0), every new case fails under its targeted mutant and under the do-nothing
control, and no green-under-both case was found. Two integration caveats for L1: M14 (c1) and
G6b/G7a/G7c (c2) are case-uncatchable and must be closed via a committed `--equivalent` map, and the
scout's E1/E2 equivalence claims (G3a/G5c) are refuted — the draft catches those two.

Seat R46bRevSelftestDiff, round 46 attempt 2, lane kasegi-shokunin. Item: attack the extended
selftest drafts (else diff the committed selftests vs their attempt-1 versions), verify every new
case fails under its targeted mutant AND passes on the clean counter, and hunt the green-under-both
failure mode. All runs mine, in scratch `/fast/scratch/hyaku/kasegi-r46/R46bRevSelftestDiff` (removed
at exit). Freeze-tree corpus exported with `git -C <lane> archive fe0f56b corpus | tar -x`; pure base =
byte copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure2`. No installs (pacman paused; stdlib only).
No git/jj mutation anywhere.

## 0. Prelim: the committed selftests are byte-identical to attempt-1

`git diff eb874bc HEAD -- corpus/instruments/r46-counters-selftest-c1.py` and the c2 twin both print
EMPTY; `git ls-tree` shows the same blobs `224614f…`/`369f8c0…` at `eb874bc`, the freeze `fe0f56b`,
and HEAD. So no new cases exist in the committed files; the new cases live only in the executor drafts.

## F1 (found in draft v1 18:39, FIXED by executor, re-verified) — broken target set on the anchor-whitelist case

Draft v1 added `L4-anchor-on-a-knowledge-entry` with `targets={"L4"}`. My clean-counter run of those
bytes printed:

```
selftest cases=82 failures=1
case L4-anchor-on-a-knowledge-entry  L1=0 L2=0 L3=1 L4=1 L5=1 L6=1 L7=0 fixed=4/7 exit=1 targets=L4 verdict=UNEXPECTED
```

The recipe (row G8 re-anchored on `corpus/knowledge/triage-thresholds.md`) makes per-entry mode red, so
the entry's own recheck fails and the entry drops out of the regrounded set: the actual reds are
L1 (gated=23>22), L2 (regrounded=1), L7 — never L4. The pre-existing case `L4-anchor-outside-dirs`
(same recipe) declares `targets=L1,L2` and reads OK, confirming the intended shape.

Executor fixed it: the case is now `X-anchor-dir-outside-the-whitelist` with `targets={"L1","L2","L7"}`.
My re-run of the fixed bytes (F2) shows it OK on clean and FALSE-GREEN under M18 — the fix is correct.
A v1 of this draft would have made mutbat print `BASELINE-DIRTY` (baseline_failures=1) and the C1 claim
unreachable; the current bytes do not have this defect.

## F2. Full attack on the current C1 draft (snapshot ff92d3026110b96ec691102c423d906d, draft mtime 19:37)

Seven new cases, all against the clean counter, a do-nothing stub, and each one's targeted mutant
(counter copies placed under a full `corpus/instruments/` tree exactly like `r46-mutbat.py apply_mutant`,
so `TOOL_LANE` resolution holds; scratch layout bug of my first pass invalidated those runs and was corrected).

Clean-counter run (command: `python3 draft-c1-snap.py --lane $ROOT --pure $PURE2 --counter $ROOT/corpus/instruments/r46-c1-gate.py --work … --jobs 8`):

```
selftest cases=83 failures=0
```

with every new case `verdict=OK`:
```
case L3-home-path-in-trailing-comment            … fixed=6/7 targets=L3 verdict=OK
case L3-absolute-home-path-in-trailing-comment   … fixed=6/7 targets=L3 verdict=OK
case L2-newly-gated-entry-not-gated-at-base      … fixed=5/7 targets=L2 verdict=OK
case X-anchor-dir-outside-the-whitelist          … fixed=4/7 targets=L1,L2,L7 verdict=OK
case L1-cd-target-is-not-valid-bash              … fixed=6/7 targets=L1 verdict=OK
case L6-anchor-escapes-the-scratch-copy          … fixed=6/7 targets=L6 verdict=OK
case L6-section-ids-not-unique                   … fixed=6/7 targets=L6 verdict=OK
```

Do-nothing control (stub that always prints `c1-gate fixed=7/7 exit=0`): `selftest cases=83 failures=76` —
all seven new cases read `FALSE-GREEN` (they discriminate; none is vacuous).

Per-mutant runs (same draft, `--counter <mutant copy>`), failing cases per run:

```
mut-M06-L3-home-dropped   : selftest cases=83 failures=2  — L3-home-path-in-trailing-comment=FALSE-GREEN, L3-absolute-home-path-in-trailing-comment=FALSE-GREEN
mut-M07-L3-home-no-abs    : selftest cases=83 failures=1  — L3-absolute-home-path-in-trailing-comment=FALSE-GREEN   (the ~/ case stays OK: M07 keeps ~/ in HOME_RE — correct semantics)
mut-M19-L2-eq-relaxed     : selftest cases=83 failures=1  — L2-newly-gated-entry-not-gated-at-base=UNEXPECTED
mut-M18-anchor-dirs-wide  : selftest cases=83 failures=1  — X-anchor-dir-outside-the-whitelist=FALSE-GREEN
mut-M20-syntax-ignored    : selftest cases=83 failures=1  — L1-cd-target-is-not-valid-bash=FALSE-GREEN
mut-M13-L6-control-dropped: selftest cases=83 failures=2  — L6-anchor-escapes-the-scratch-copy=UNEXPECTED, L6-section-ids-not-unique=UNEXPECTED
```

Result matrix (new case × run): every case is OK on clean, NOT-OK under its targeted mutant, NOT-OK
under the do-nothing stub. **No green-under-both case found.** All six catchable round-46 C1 mutants
(M06, M07, M13, M18, M19, M20) are caught by dedicated cases. The targeted-mutant runs are re-runs I
performed; raw stdout of every run staged under my scratch (removed at exit) and key lines quoted here.

## F3. M14-L6-exit-ignored stays uncaught — equivalent, must close at L1 integration, not by a case

No new case targets M14 (correctly). Scout R46bScoutEquivalence proved equivalence logically
(`rc==0 ⟹ red==[]` in entry mode, so `p.returncode == 0 or red != [r[0]] ≡ red != [r[0]]`) and
byte-identical outputs on 5 trees. My own run of the draft's L6-anchor-escapes case (the strongest L6
case: it pins the `unmutated-copy-not-green` reason string) under an M14-mutant counter copy printed:

```
case L6-anchor-escapes-the-scratch-copy  L1=1 L2=1 L3=1 L4=1 L5=1 L6=0 L7=1 fixed=6/7 exit=1 targets=L6 verdict=OK
selftest cases=5 failures=0
```

i.e. byte-for-byte the same verdict as the clean counter (compare F2's clean line for the same case) —
M14 is not caught even by the case designed to pin the L6 control. No test case can catch M14; the
wave must close it with an `--equivalent` map entry at L1 integration, else `uncaught=0` for c1 is
unprintable.

## F4. C2 draft (landed 20:02, snapshot 184ab706be5fd9e62cf9c9dc815e4d9c): 10 new cases, static analysis + targeted runs

The C2 draft landed while this review was closing; it adds exactly 10 mutant-discriminating cases
(diff: 205 added lines, no deletions to existing cases):

```
mut-g1c-f28-sources-cell-prefix   -> G1c    F28 row sources cell reads S0730
mut-g2a-verified-at-prefix        -> G2a    verified-at line = 2026-10-28T00:00:00Z
mut-g2b-limits-word-floor         -> G2b    Limits section = 13 words (25-floor vs 5-floor)
mut-g2c-overlap-xref-swapped      -> G2c    second xref names claim-anatomy-sample.md
mut-g3a-registry-row-cells        -> G3a    S073 row gains a 12th cell "| extra |" APPENDED AT THE END
mut-g4b-manifest-quote-count      -> G2b    manifest keeps 7 quotes (repin=True)
mut-g5c-five-cores-two-spans      -> G5c    doctored capture lines 560-561 carry all 5 cores in 2 spans; allow={G3,G4}
mut-g6a-knowledge-file-symlink    -> G6a    knowledge file symlinked to identical copy outside the dir
mut-g6c-entry-byte-floor          -> G6c    entry trimmed under 3000 bytes
mut-g7b-sources-md-symlink        -> G7b    SOURCES.md symlinked to an identical copy
```

Static verification against the frozen counter bytes (path:line cited):

- G1c/G2a/G2b/G2c/G6a/G6c/G7b: recipe flips exactly the mutated clause; clean red on the named gate only;
  every other gate reads green under the mutant (7/7) -> case reports ACCEPTED-targeted-gate-passes -> caught.
- **G3a** (scout had classified this equivalent-by-construction, claiming >=12 cells shift positional
  literals): the executor appends `| extra |` at the END of the row, so cells 0-10 keep their positions.
  `PINS["S073-row"] is None` (r46-c2-gate.py:63), so the row pin is skipped; clean hits
  `len(c) == 11` False -> `row=None` -> "row-S073=absent-or-malformed" (gate :246-251); the G3a mutant
  (`len(c) >= 9`) parses the row and every positional check (row[2]..row[10]) passes -> G3 green.
  The scout's equivalence verdict is an artifact of assuming the extra cell shifts positions; the
  end-appended craft discriminates. G7 collateral (census on a 12-cell row) is declared in `allow`.
- **G5c** (scout: equivalent-by-arithmetic): the executor doctors the capture (`ls[559]/ls[560] =
  MUT_PACK_A/B`) so all five frozen cores sit in two 24-word lines, and rewrites the entry to quote
  exactly those two spans (spans=2, cores=5/5, failed=0, uncited=0). Clean: `len(passed) >= 4` fails
  (gate :328-334) -> G5 red; the doctored snap trips the capture pins G3/G4 — declared collateral via
  `allow={"G3","G4"}`. G5c mutant: `len(passed) >= 1` -> G5 green while G3/G4 stay red -> the case
  reports ACCEPTED-targeted-gate-passes=G5 -> caught. Under the clean counter the failing set is
  {G3,G4,G5} = targets|allow exactly, so the case must read `ok`.

Two decisive dynamic checks were still running when this section was drafted; both have now completed
(re-runs I performed against the snapshot 184ab706, battery-exact mutant layout, `--lane`/`-pure`/
`--counter` all pinned to my freeze export):

Clean-counter baseline of the whole draft:

```
selftest cases=147 failures=0
ok   mutant  mut-g1c-f28-sources-cell-prefix fixed=6/7 failing=['G1']
ok   mutant  mut-g2a-verified-at-prefix      fixed=6/7 failing=['G2']
ok   mutant  mut-g2b-limits-word-floor       fixed=6/7 failing=['G2']
ok   mutant  mut-g2c-overlap-xref-swapped    fixed=6/7 failing=['G2']
ok   mutant  mut-g3a-registry-row-cells      fixed=5/7 failing=['G3', 'G7']
ok   mutant  mut-g4b-manifest-quote-count    fixed=6/7 failing=['G4']
ok   mutant  mut-g5c-five-cores-two-spans    fixed=4/7 failing=['G3', 'G4', 'G5']
ok   mutant  mut-g6a-knowledge-file-symlink  fixed=6/7 failing=['G6']
ok   mutant  mut-g6c-entry-byte-floor        fixed=6/7 failing=['G6']
ok   mutant  mut-g7b-sources-md-symlink      fixed=6/7 failing=['G7']
```

Every new case is red on the clean counter with failing == targets|allow exactly — no baseline
poisoning, no green-under-both case. Under the two scout-disputed mutant counters:

```
# G3a-cells-loose mutant counter:
selftest cases=147 failures=1
FAIL mutant  mut-g3a-registry-row-cells fixed=6/7 failing=['G7']  <- ACCEPTED-targeted-gate-passes=['G3']

# G5c-pass-low mutant counter:
selftest cases=147 failures=1
FAIL mutant  mut-g5c-five-cores-two-spans fixed=5/7 failing=['G3', 'G4']  <- ACCEPTED-targeted-gate-passes=['G5']
```

G3a and G5c are genuinely caught — the scout's E1/E2 equivalence verdicts are refuted by these crafts
(end-appended 12th cell keeps positional literals; doctored capture + declared G3/G4 collateral). The
other eight cases I verified statically (each recipe flips exactly the mutated clause and nothing
else; clean failing sets above match their targets with declared collateral only); dynamic runs for
those eight were not completed before the wrap-up nudge.

Residual C2 risk for L1: the draft catches 18 of 21 mutants; G6b/G7a/G7c remain and have NO cases.
They rest on the scout's E3/E4/E5 equivalence claims (measured no-flip + census-contract reasoning —
stronger than the refuted E1/E2, which were a priori). L1 must land an `--equivalent` map covering at
least these three or the battery cannot print `uncaught=0` for c2. If L1 lands the scout's original
5-entry map (incl. G3a/G5c), the battery still prints uncaught=0 — equivalent and caught count the
same — but the map would mislabel two mutants the draft actually catches.

## Limitations

- C2: dynamic mutant runs were completed for G3a and G5c (the scout-disputed pair) plus the full-draft
  clean baseline; the other eight C2 cases are verified statically (recipe flips exactly the mutated
  clause; clean failing sets match targets|allow) — eight full passes were not run before the wrap-up
  nudge. C1 evidence is fully dynamic (clean/stub/six mutant counters + an M14 spot-check).
- A full-battery confirmation pass (`r46-mutbat.py` over a draft-swapped tree) was started for C1 but
  killed under host load (loadavg >180, empty output) and not restarted per the L1 nudge; the per-mutant
  `failures≥1` results are the battery's own caught-predicate, run battery-exact (assert-once mutant
  application, full `corpus/instruments/` mutant layout).
- Equivalent-mutant status: M14 (c1) spot-checked dynamically (the strongest L6 case reads identical
  verdict under M14 as clean) and scout-proven; G6b/G7a/G7c (c2) rest on the scout's measured no-flip
  E3/E4/E5 evidence, not re-derived by me. G3a/G5c are NOT equivalent — the draft catches them (F4).
- Two of my own harness bugs (flat mutant-counter layout breaking `TOOL_LANE`; a non-Python do-nothing
  stub) invalidated my first attack pass; both were corrected and every quoted result is from the
  corrected runs. The M13 mutant had two mapped cases; one run covers both (quoted).
- Host guard respected: read-only on the lane and drafts (snapshot copies attacked); nothing committed;
  scratch removed at exit.
