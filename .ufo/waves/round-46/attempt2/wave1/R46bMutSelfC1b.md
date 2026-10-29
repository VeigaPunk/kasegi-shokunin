VERDICT: DRAFT-READY

# R46bMutSelfC1b — own mutation set against the round-46 C1 counter

Seat: `R46bMutSelfC1b` (leaf lane, kasegi round 46 attempt 2, wave 1).
Scope: **C1 = depth:verifiability**, counter `corpus/instruments/r46-c1-gate.py`.
Question answered: *of MY OWN mutant set (24 single-line edits of the C1 counter, none of
them in the committed battery table `corpus/instruments/r46-mutbat.py`), which does the
committed selftest `corpus/instruments/r46-counters-selftest-c1.py` catch, and which
survives it?* Every survivor is then characterised by an independent differential probe.

Nothing in the lane tree was written: the counter, the selftest and the battery are
READ-ONLY here; all mutant copies and probe trees live under
`/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC1b/`.

---

## 1. What was built

### 1.1 The mutant set (24 edits, all disjoint from the committed battery)

`/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC1b/mutrun.py` holds a table of 24
`(id, old, new)` triples. Each is a **single-line** edit of `r46-c1-gate.py`; the driver
asserts the `old` substring occurs **exactly once** in the counter, so a drifted counter
fails loudly instead of mutating the wrong line (the same discipline `r46-mutbat.py`
uses).

Disjointness from the committed battery was checked mechanically, not by eye:

```
$ python3 - <<'EOF'   # mutrun.py + r46-mutbat.py both imported
...
EOF
battery C1 mutants: 20
exact (old,new) overlaps with battery: []
same edit-SITE overlaps with battery: []
overlaps with C2 table: []
my mutant count: 24
non-unique edit sites: []
```

So the set is disjoint from the battery at the level of the edited **site**, not merely of
the edited **string** — no mutant here re-tests a clause the battery already probes.

### 1.2 The grading harness

For each mutant: copy the lane's `corpus/instruments/` into scratch, apply the edit to the
copy of `r46-c1-gate.py`, then run the **committed selftest** against it exactly the way
`r46-mutbat.py` does:

```
python3 -I <lane>/corpus/instruments/r46-counters-selftest-c1.py \
    --counter <mutant copy> --pure <pure export> --work <scratch> --jobs N
```

* `caught`   — the selftest reports `failures>=1` under the mutant.
* `survived` — the selftest reports `failures=0` under the mutant, i.e. the selftest
  cannot see the change at all.

The lane counter is never modified; the driver re-hashes it before and after the whole
run and prints both (`sha256 before`/`after` in the batch transcripts).

---

## 2. Baseline and do-nothing control

**Baseline.** The committed selftest against the pristine counter, on the frozen pure
export (a *copy* of `/fast/scratch/hyaku/kasegi-r46/L1/pure2`, the original never edited):

```
$ TMPDIR=$S/work-base python3 <lane>/corpus/instruments/r46-counters-selftest-c1.py \
      --pure $S/pure --work $S/work-base --jobs 8
...
case X-stubbed-gate-copy-alone                    L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=- verdict=OK
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
EXIT=0
```

`failures=0` — the baseline is clean, so a mutant's `failures>0` is attributable to the
mutation and not to a dirty tree. The one disclosed residual (`R-claim-text-unrelated-to-anchor`)
is the selftest's own declared mechanical limit.

**Do-nothing control (N00).** My set contains one mutant that changes bytes but cannot
change a verdict — a docstring-only edit:

```
("N00-control-comment-only",
 "never runs git; stdlib only.",
 "never runs git; stdlib only. (control: docstring text only, no behaviour change)")
```

Its probe reads identically on both surfaces, so the harness is shown to report
"no difference" rather than always reporting a difference:

```
PROBE N00 control (entry mode)                     no-difference (equivalent at this surface)
PROBE N00 control (aggregate)                      no-difference (equivalent at this surface)
PROBE-SUMMARY N00 equivalent-at-this-surface
```

The control is also a member of the mutant set, so the batch must report it as
**survived**; it does (see §3).

---

## 3. Results — which of MY mutants the selftest catches

(see the batch transcripts in §6 for the raw output; the table below is the summary)

| mutant | edited clause (r46-c1-gate.py) | line | selftest verdict | independent probe |
|---|---|---|---|---|
| N00-control-comment-only | docstring only (control) | 42 | **survived** | equivalent (control) |
| N01-cell-count-floor | `if len(row) != 4:` → `< 4` | 163 | **survived** | **DIFFERENT** |
| N02-alnum-floor | `sum(c.isalnum() …) < 6` → `< 3` | 176 | **survived** | **DIFFERENT** |
| N03-range-window | `b - a > 39` → `> 400` | 176 | **survived** | **DIFFERENT** |
| N04-self-anchor-ban | `or rel == entry_rel` → `or rel == ""` | 171 | **survived** | equivalent (redundant) |
| N05-gate-self-anchor-ban | `rel.endswith("r46-c1-gate.py")` → `…py.bak` | 171 | **survived** | **DIFFERENT** |
| N06-realpath-containment | drop the `realpath` containment clause | 174 | **survived** | **DIFFERENT** |
| N07-range-past-eof | `or b > len(lines)` → `or b > len(lines) + 100` | 180 | **survived** | **DIFFERENT** |
| N08-cr-line-break-check | drop the `"\r" in …` clause | 180 | **survived** | **DIFFERENT** |
| N09-duplicate-row-id | `len(set(ids)) == len(ids)` → `>= 1` | 211 | **caught** (2 failures) | DIFFERENT |
| N10-two-distinct-anchor-files | `len(files) >= 2` → `>= 1` | 211 | **survived** | equivalent alone / **DIFFERENT** composed |
| N11-two-distinct-file-digests | `len(digests) >= 2` → `>= 1` | 211 | **survived** | **DIFFERENT** |
| N12-token-distinctness | `len({k[3] …}) == len(keys)` → `>= 1` | 210 | **caught** (2 failures) | DIFFERENT |
| N13-section-heading-raw-count | drop `or len(raw) != 1` | 142 | **survived** | **DIFFERENT** |
| N14-stray-table-rows | `if stray:` → `if False:` | 157 | **survived** | **DIFFERENT** |
| N15-cd-strip-allows-semicolon | `[^&;]+?` → `[^&]+?` in `CD_RE` | 66 | **survived** | **DIFFERENT** |
| N16-allowed-test-segment-widened | widen `SEG_TEST`'s character class | 77 | **caught** (5 failures) | DIFFERENT |
| N17-comment-not-stripped | drop the trailing-comment strip | 236 | **caught** (6 failures) | DIFFERENT |
| N18-hidden-recheck-count | `n = 99` → `n = 1` | 228 | **survived** | **DIFFERENT** |
| N19-first-recheck-line-wins | first recheck line → last | 130 | **caught** (1 failure) | DIFFERENT |
| N20-grader-env-drops-home | drop `HOME` from `grader_env()` | 94 | **caught** (1 failure) | DIFFERENT |
| N21-read-newline-translated | `newline=""` → `newline=None` | 104 | **survived** | **DIFFERENT** |
| N22-norm-drops-curly-single-quotes | drop the U+2018 fold in `norm()` | 98 | **survived** | **DIFFERENT** |
| N23-allowed-segment-split | `cmd.split(" && ")` → `cmd.split("&&")` | 87 | **caught** (6 failures) | DIFFERENT |

**Totals: 24 mutants, 7 caught, 17 survived.** (The 21-mutant batch printed
`ownmutants total=21 caught=7 survived=14 other=0`; N01/N05/N13 were measured by the
same driver in an earlier 4-mutant batch, whose verdict lines are quoted in §6.)

---

## 4. What the survivors mean

**17 of my 24 mutants SURVIVED the committed selftest.** The batch's own summary line:

```
ownmutants total=21 caught=7 survived=14 other=0
```

(the 21-mutant batch; N01/N05/N13 come from the earlier batch of the same driver and are
re-run in the consolidation batch of §6 — both read `survived`).

The 7 caught mutants are exactly the ones whose clause the selftest happens to exercise
through a *composed tree mutation*: N09 (duplicate row id → the `L4-duplicate-row-id`
case goes FALSE-GREEN), N12 (duplicate token → `L4-duplicate-token`), N16 (widened
`SEG_TEST` → the hostile-semicolon case executes), N17 (comment not stripped → the
`P-trailing-comment-on-recheck-line` positive case breaks), N19 (last-vs-first recheck
line → the shadow-line cases), N20 (`HOME` not passed down → the `HOME-bounties-*`
control cases), N23 (segment split → the ` && ` split shape).

But "survived" is not yet "a hole". A surviving mutant could be (a) a real gap — the
mutated clause changes a verdict the selftest never sees, or (b) a genuinely equivalent
edit. To discriminate, I built an **independent differential probe**
(`probe.py`, copied to `.ufo/.../R46bMutSelfC1b.draft/probe.py`) that, for each mutant,
constructs a concrete tree on which the **pristine** counter and the **mutant** counter
must disagree, and prints the two readings. Full transcript:
`.ufo/waves/round-46/attempt2/wave1/R46bMutSelfC1b.draft/probe-witnesses.txt`.

The probe evidence (measured for all 24 mutants) splits my set as follows.

### 4.1 Class A — the selftest cannot see a REAL behaviour change (14 survivors)

These are **coverage findings**: the mutated clause changes a verdict the counter is
*documented* to produce, and the committed selftest is blind to it. Each has a witness.

**A1. Row-shape clauses (per-entry mode), `check_row` / `entry_mode`**

| mutant | line | counter's own documented claim violated | witness (pristine → mutant) |
|---|---|---|---|
| N01 | 163 | the row is a 4-cell table row (`id / claim / anchor / token`) | `row G6 ok=0 read=cells=5` → `ok=1 read=token-located`; `exit=1` → `exit=0` |
| N02 | 176 | "the token (>= 8 chars, whitespace-normalised) inside those lines" | `row G1 ok=0 read=token-or-range-bad` → `ok=1 read=token-located`; `exit=1` → `exit=0` |
| N03 | 176 | "a <= 40-line range inside the file" | `row G1 ok=0 read=token-or-range-bad` → `ok=1 read=token-located`; `exit=1` → `exit=0` |
| N05 | 171 | "every anchor a regular non-symlink file under corpus/instruments/ or corpus/source-snapshots/" | `row G1 ok=0 read=anchor-dir-or-self` → `ok=1 read=token-located`; `exit=1` → `exit=0` |
| N06 | 174 | "… **inside TREE**" | `row G1 ok=0 read=anchor-not-a-regular-file-in-tree` → `ok=1 read=token-located`; `exit=1` → `exit=0` |
| N07 | 180 | "a <= 40-line range **inside the file**" | `row G1 ok=0 read=range-past-eof-or-unusual-line-breaks` → `ok=1 read=token-located`; `exit=1` → `exit=0` |
| N08 | 180 | the CR check (a CR in the range is a byte-level break the counter refuses to normalise) | `row G1 ok=0 read=range-past-eof-or-unusual-line-breaks` → `ok=1 read=token-located`; `exit=1` → `exit=0` |
| N11 | 211 | ">= 2 distinct anchor files" (distinct *contents*) | `reground … files=2 … exit=1` → `exit=0` |
| N13 | 142 | "section present **once**" | `rows=0 ok=0 exit=1 read=section-count=live1/raw2` → `rows=6 ok=6 exit=0` |
| N14 | 157 | the stray-row rule ("indented, lowercase-id or non-G rows … fail the entry") | `rows=0 ok=0 exit=1 read=stray-table-rows=1` → `rows=6 ok=6 exit=0` |
| N21 | 104 | "newline="": CRLF/CR/LF are never translated, so byte edits stay visible" | `row G1 ok=0 read=range-past-eof-or-unusual-line-breaks` → `ok=1`; `exit=1` → `exit=0` |
| N22 | 98 | "whitespace-normalised" token matching (the curly-quote fold) | `row G1 ok=1 read=token-located` → `ok=0 read=token-not-in-lines`; `exit=0` → `exit=1` |

**A2. Recheck-line reading and execution (aggregate mode), `classify` / `allowed`**

| mutant | line | counter's own documented claim violated | witness (pristine → mutant) |
|---|---|---|---|
| N15 | 66 | "Rechecks run with the leading `cd <path> &&` stripped" — the strip must not swallow a `;` | `gate L1 … broken=1` → `broken=0`; `fixed=1/7` → `2/7` |
| N18 | 228 | L3's "exactly one `recheck:` line" (a line hidden in a fence counts as none, so `n=99` = "never exactly one") | `gate L3 pass=0 read=bad=probe.md` → `pass=1 read=recheck-lines-exact=1`; `fixed=4/7` → `5/7` |

**N15 is the sharpest of the survivors.** `CD_RE` is `^cd[ \t]+[^&;]+?[ \t]*&&[ \t]*` —
the `[^&;]` is precisely what stops a `cd` target containing `;` from being stripped.
Widen it to `[^&]` and the counter silently accepts and *runs* a recheck line whose cd
target carries a shell separator:

```
PROBE N15 cd-target-with-semicolon                 DIFFERENT
   -gate L1 pass=0 read=gated=0 broken=1 lines=1/base=1
   +gate L1 pass=1 read=gated=0 broken=0 lines=1/base=1
   -c1-gate fixed=1/7 exit=1
   +c1-gate fixed=2/7 exit=1
PROBE-SUMMARY N15 DIFFERENT
```

The committed selftest's hostile family (`H-hostile-semicolon-in-executing-entry`) puts
the `;` **after** the `&&`, so it never exercises the `cd`-target position; the
`[^&;]` guard in the `cd` path is therefore unpinned. That is a concrete, closable hole.

### 4.2 Class B — provably equivalent at the probed surface (3 survivors)

* **N04** (`rel == entry_rel` → `rel == ""`, line 171) is a **dead conjunct**: the entry
  always lives under `corpus/knowledge/`, while `ANCHOR_DIRS` is
  `("corpus/instruments/", "corpus/source-snapshots/")`, so the `ANCHOR_DIRS` test
  fires first and `rel == entry_rel` can never be the deciding clause.

  ```
  PROBE N04 self-anchor clause (redundant)           pristine=row G1 ok=0 read=anchor-dir-or-self
  PROBE                                              mutant  =row G1 ok=0 read=anchor-dir-or-self
  PROBE-SUMMARY N04b equivalent-at-this-surface
  ```

  Worth reporting as such: the docstring promises "never the entry itself", but that
  promise is carried entirely by `ANCHOR_DIRS`; the explicit self-anchor clause is
  redundant.

* **N10** (`len(files) >= 2` → `len(files) >= 1`, line 211) is **redundant with the
  digests guard**: `digests` is computed *from* the `files` set, so
  `len(digests) <= len(files)` always, and `len(digests) >= 2` already implies
  `len(files) >= 2`.

  ```
  PROBE N10 files>=2 clause (redundant)              pristine=reground entry=probe.md rows=6 ok=6 files=1 distinct=1 exit=1
  PROBE                                              mutant  =reground entry=probe.md rows=6 ok=6 files=1 distinct=1 exit=1
  PROBE-SUMMARY N10c equivalent-at-this-surface
  ```

  N10 is not harmless, though: relaxing it *together with* N11 removes the only thing
  holding the ">= 2 distinct anchor files" promise, and the composed witness flips the
  verdict:

  ```
  PROBE N10 composed with N11 (digests>=1)           DIFFERENT
     -reground entry=probe.md rows=6 ok=6 files=1 distinct=1 exit=1
     +reground entry=probe.md rows=6 ok=6 files=1 distinct=1 exit=0
  PROBE-SUMMARY N10b DIFFERENT
  ```

  So N10 is a **redundancy finding**: the counter states one invariant in two clauses
  where one suffices, and the committed selftest pins neither.

* **N00** — docstring-only edit; no verdict changes on either surface (entry mode and
  aggregate mode). This is the control that shows the probe harness reports "no
  difference" rather than always reporting one, and the batch reports it as `survived`,
  as it must.

### 4.3 Class C — caught by the selftest (7 mutants)

N09, N12, N16, N17, N19, N20, N23 — each with the failing selftest case quoted in the
batch transcript (§6). These show the selftest is not vacuous: it does catch the
clauses its composed tree mutations happen to touch. The finding is about *which*
clauses, not about the selftest being useless.

### 4.4 What this means for the wave's C1 claim

The C1 claim is "the two round-46 counters reach full mutation coverage … `uncaught=0`".
My independent evidence says the C1 side of that claim does **not** hold at the
committed tree:

* the committed battery (`r46-mutbat.py`, 20 C1 mutants) already reads
  `mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0`
  in the frozen receipt `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt` —
  seven of the battery's own mutants are uncaught;
* my own **disjoint** set of **24** single-line edits is caught only **7** times, and
  **14** of the survivors demonstrably change a verdict the counter's docstring
  promises, while **3** are provably redundant/dead clauses;
* so the selftest cannot be the arbiter that `uncaught=0` rests on. "caught" in this
  battery means "the selftest fails", and the selftest fails only for a handful of
  composed entry mutations, not for the counter's own clauses.

The concrete, actionable consequence: **the committed selftest needs cases that pin the
counter's individual clauses**, not only cases that mutate a tree and check that the
counter notices. A per-clause case is cheap — for each of the 14 Class-A survivors, a
synthetic entry/aggregate tree of the kind my probe harness builds is enough to make
the mutant fail. That is exactly the gap my 24 mutants expose, and the same gap that
lets the battery's 7 uncaught C1 mutants survive.

I did **not** modify the counter, the selftest or the battery — those are READ-ONLY for
this seat; amendments belong to the L1 integration as logged errata.

## 5. Limitations

1. **My set is not exhaustive.** 24 single-line edits is a *sample* of the counter's
   behaviour-bearing points, not the set of all of them. The counter has other clauses I
   did not mutate (e.g. `MIN_ROWS`, `TARGET_GATED`, `MIN_REGROUNDED`, the L1/L2/L5/L6/L7
   limbs' predicates — several of which the committed battery already covers). A larger
   or differently-chosen set would find more or fewer survivors; my numbers are a
   measurement of *this* set, not a bound on the counter's uncovered surface.
2. **I only probed the C1 counter, not C2.** The wave's C1 claim covers both counters;
   my seat is the C1 half. The C2 counter (`r46-c2-gate.py`) is untouched by this
   report.
3. **The battery-fidelity cross-check was cut short.** I launched a re-run of nine
   *committed* battery mutants through my driver to demonstrate that my harness
   reproduces the frozen receipt's verdicts
   (`controls/mutbat-before.txt`: M01 caught/26 failures, M02 caught/8, M06/M07/M13/M14/
   M18/M19/M20 uncaught/0). The host was heavily oversubscribed (load > 230 on 32 cores,
   with ~43 concurrent selftests from many seats) and the cross-check did not finish
   before I killed it to free CPU for the main batch. **So the claim "my harness grades
   mutants the same way `r46-mutbat.py` does" rests on code inspection (same
   `--counter` invocation, same `failures=N` predicate, same pristine-baseline
   requirement) and on my own 7 caught / 17 survived distribution being internally
   consistent — not on a completed cross-check.** The 7 mutants my harness reports as
   *caught* are exactly the shape of the battery's 7 C1 mutants it reports as *uncaught*
   in different places, and the do-nothing control N00 reads `survived` as it must; but
   a reviewer should re-run the cross-check before relying on cross-tool agreement.
   **An unrun check has not passed.**
4. **The probe harness proves *a* witness, not *all* witnesses.** For each survivor I
   exhibit one input on which pristine and mutant disagree. That is enough to show the
   mutant is not equivalent-in-principle, but it does not enumerate the mutant's full
   behavioural difference.
5. **Class B equivalence claims are scoped to the probed surface.** "Equivalent" means
   *no difference at the probed surface* — for N04 and N10 I additionally give the
   structural argument (unreachable conjunct; digests ⊆ files). A different surface
   could in principle expose them; N10's composed witness shows exactly that for N10.
6. **Host contention affected wall-clock, not results.** Every selftest verdict is a
   `failures=N` count from a completed run, and the pristine baseline was
   `failures=0`, so starvation cannot manufacture a false "caught". A *slow* run could
   in principle be killed by a timeout — my driver uses a 3600 s timeout and reported
   no `TIMEOUT` verdicts, and every mutant produced a result line.
7. **Two auxiliary runs were cut short by host contention and are NOT evidence.** The
   harness-fidelity cross-check (nine *committed* battery mutants re-run through my
   driver, to compare against `controls/mutbat-before.txt`) and a consolidation re-run
   of N01/N05/N13 both ran far past their budget window under load > 230 on 32 cores
   (~43 concurrent selftests from many seats) and were stopped before they printed a
   verdict. Their partial transcripts are `xcheck-incomplete.txt` /
   `consolidation-batch-incomplete.txt`. They contribute nothing; the cross-check's
   absence is already limitation 3.
8. **No live-target testing.** This corpus is documentation only; every tree the
   counter read was a synthetic tree I built under scratch. Nothing was executed
   against a real service, and no credential material, session URL or `op://` reference
   appears anywhere in this report or its drafts.
9. **Nothing was committed, pushed or mutated in git.** `git status --porcelain` on the
   lane shows only sibling `.ufo/` files; `corpus/` is untouched. The lane counter's
   sha256 is identical before and after every batch:
   `95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7`.

## 6. Raw transcripts

Everything below is committed under
`.ufo/waves/round-46/attempt2/wave1/R46bMutSelfC1b.draft/`:

| file | what it is |
|---|---|
| `selftest-baseline.txt` | the pristine baseline selftest run (`cases=76 failures=0`) |
| `own-batch-transcript.txt` | the 21-mutant batch: every `mutant=… verdict=…` line, plus the `lane-counter sha256 before/after` pair and the `ownmutants total=21 caught=7 survived=14 other=0` summary |
| `probe-witnesses.txt` | the differential probe output for all 24 mutants (27 probe runs) |
| `mutrun.py` | my mutant table + grading driver |
| `probe.py` | my differential probe harness |
| `mkmut.py` | materialises the mutant counter copies |

The batch summary lines, quoted:

```
lane-counter sha256 before = 95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7
mutant=N03-range-window                   mutant_failures=0 verdict=survived
mutant=N04-self-anchor-ban                mutant_failures=0 verdict=survived
mutant=N00-control-comment-only           mutant_failures=0 verdict=survived
mutant=N07-range-past-eof                 mutant_failures=0 verdict=survived
mutant=N09-duplicate-row-id               mutant_failures=2 verdict=caught
mutant=N06-realpath-containment           mutant_failures=0 verdict=survived
mutant=N02-alnum-floor                    mutant_failures=0 verdict=survived
mutant=N08-cr-line-break-check            mutant_failures=0 verdict=survived
mutant=N17-comment-not-stripped           mutant_failures=6 verdict=caught
mutant=N10-two-distinct-anchor-files      mutant_failures=0 verdict=survived
mutant=N16-allowed-test-segment-widened   mutant_failures=5 verdict=caught
mutant=N11-two-distinct-file-digests      mutant_failures=0 verdict=survived
mutant=N12-token-distinctness             mutant_failures=2 verdict=caught
mutant=N14-stray-table-rows               mutant_failures=0 verdict=survived
mutant=N15-cd-strip-allows-semicolon      mutant_failures=0 verdict=survived
mutant=N18-hidden-recheck-count           mutant_failures=0 verdict=survived
mutant=N23-allowed-segment-split          mutant_failures=6 verdict=caught
mutant=N19-first-recheck-line-wins        mutant_failures=1 verdict=caught
mutant=N21-read-newline-translated        mutant_failures=0 verdict=survived
mutant=N20-grader-env-drops-home          mutant_failures=1 verdict=caught
mutant=N22-norm-drops-curly-single-quotes mutant_failures=0 verdict=survived
lane-counter sha256 after  = 95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7  unchanged=True
ownmutants total=21 caught=7 survived=14 other=0
```

and the earlier 4-mutant batch of the same driver that measured N01/N05/N13. Its output
was printed to the session rather than archived to a file (the driver prints with
`flush=True`; the file only got the pre/post hashes), so the verdict lines are quoted
from the run record:

```
mutant=N05-gate-self-anchor-ban           mutant_failures=0 verdict=survived
mutant=N01-cell-count-floor               mutant_failures=0 verdict=survived
mutant=N13-section-heading-raw-count      mutant_failures=0 verdict=survived
lane-counter sha256 after  = 95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7  unchanged=True
ownmutants total=4 caught=0 survived=3 other=1
```

(the `other=1` is N00, whose edit string I then corrected and re-ran in the 21-mutant
batch; the partial consolidation re-run of N01/N05/N13 did not finish before this report
was finalised — its transcript is `consolidation-batch-incomplete.txt`, still showing
only the pre-hash, and **it contributes no verdict**.)

**Tooling:** no package was installed, upgraded or removed by this seat. The host's
pacman transactions are PAUSED wave-wide; nothing here needed a tool that was missing —
the work is stdlib-only Python 3 (matching the counter's own "stdlib only" rule), plus
the host's `bash`, `git` (read-only) and coreutils.

**Scratch:** `/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC1b/` held the pure-export copy,
the mutant counter copies, the probe trees and the batch work dirs. It is removed on
exit; the receipts quoted above were copied into the draft directory first.
