# R44W2Crit08 — no-harm attack on the round-44 instruments (wave 2, falsify)

Attacked item: the round added `corpus/instruments/r44-routed-defects.py` (C1 counter),
`corpus/instruments/r44-frontier-count.py` (C2 counter) and
`corpus/instruments/wave-registry.py` (registry emitter) at commit
`8063547d0ce647d6f9eafc3c8d0a502616685218`. Question: does any existing gate's
behaviour, output shape or pinned figure change because of them, and could a later
reader mistake them for the lane's older closure suites (naming, CLI, shared receipt
path)?

Axes: no-harm · mistakeability · verifiability · coverage.

## Verdict summary

- **No-harm: held.** No existing gate's behaviour, output shape or pinned figure
  changes because of the three instruments. Verified statically and empirically
  (§1). I could not falsify no-harm.
- **Mistakeability: two findings land** (§2.1 unregistered instrument — the exact
  defect-7 class round 43 routed; §2.2 near-name/unit confusion with the older
  `frontier-recheck-count.py`), plus two receipt-identity hazards (§2.3, §2.4) and
  one scratch-convention deviation (§2.5).
- No verdict is offered on the truth of claims C1/C2; that is other seats' item.

## 1. No-harm — evidence

All commands ran under `$HYAKU_SCRATCH/kasegi-r44/R44W2Crit08/` on exports
`git -C <lane> archive 8063547d…` (`after`) and `6631401…` (parent, `before`), plus
`plus3` = `before` + only the three instrument files (isolates the instruments from
the round's other 103 files).

1. Deep frontier gate unchanged: `python3 corpus/instruments/frontier-recheck-count.py
   --root .` — byte-identical output on `before` vs `plus3` (`entries=28 pass=28
   exit=0` both).
2. Selftests unchanged (`before` vs `plus3`, diff empty, exits equal):
   `claim-package-check.py --selftest` (`selftest cases=10 failures=0`),
   `kill-rule-check.py --selftest` (`selftest cases=3 failures=0`),
   `recheck-audit.py --selftest`.
3. r42-closure.sh J3 lists `corpus/instruments/` via
   `CLOSURE_RX = re.compile(r"^r\d+-closure\.sh$")` (`r42-closure.sh:611`,
   consumed by `closure_basenames` → `check_j3` at `r42-closure.sh:664`). None of
   `r44-routed-defects.py`, `r44-frontier-count.py`, `wave-registry.py` matches, so
   the `r40_split`/names surface is unchanged. Static proof; full r42 suite not run
   (limitation, §4).
4. `kill-rule-check.py` picks the newest `.ufo/waves/round-*/c1-controls/fake-killrule.py`
   (`kill-rule-check.py:603-614`). The commit adds no
   `.ufo/waves/round-44/c1-controls/` (`git ls-tree -r 8063547d | grep
   'round-44.*fake-killrule'` → 0), so the pick stays round-43's. No change.
5. Pinned figure `corpus/instruments/knowledge-expected.txt`: the commit's only
   change is `+corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`
   (diff shown). The 62→63 figure move is attributable to the new knowledge entry
   (claim C2's own substance), not to the instruments; `recheck-audit.py` behaviour
   is identical in `plus3` (item 2).
6. Read-only claim verified: sha256 manifest of the whole `after` tree before vs
   after running all three instruments (default modes) is identical — zero writes.
   `wave-registry.py` writes only its `--out` path
   (`wave-registry.py:90,102-103`, sole `open(..., "w")` / `makedirs` in the file).
7. Emitter determinism: re-run `wave-registry.py --results
   .ufo/waves/round-44/wave1-results.json --out <scratch>` over the committed tree
   is byte-identical to the committed `.ufo/waves/round-44/wave-registry.txt`
   (`seats=66 names=66 attack=40`). No older gate reads that path; the round-43
   registry is a different file (`w1-REGISTRY.txt`).
8. Counter shapes match the committed receipts: `r44-routed-defects.py --root after`
   → `routed-defects total=8 fixed=8 unresolved=0 exit=0` (= `c1-counter-after.txt`);
   with `--baseline before` the baseline line grades; `r44-frontier-count.py --root
   before --expect 26` → `frontier rows=25 admitted=25 … exit=1`, `--root after
   --expect 26` → `rows=26 admitted=26 exit=0` (= `c2-frontier-counter.txt`).
9. `corpus/instruments/__pycache__/` exists only as untracked working-tree residue
   (`git ls-tree -r 8063547d | grep -c __pycache__` → 0; same at HEAD); the
   `r44-routed-defects.cpython-314.pyc` is stale relative to its `.py`. Hygiene
   only; no committed or gate impact.

## 2. Findings that land

### 2.1 `r44-frontier-count.py` is registered nowhere — routed-defect-7 class recurrence

`git grep -n 'r44-frontier-count' 8063547d` hits only: its own docstring/CLI lines,
the control receipt `.ufo/waves/round-44/controls/c2-frontier-counter.txt:11,15`,
and `corpus/lessons/round-44.md:113`. It has **no row** in
`corpus/instruments/README.md` (0 grep hits; the Round-44 section table there lists
only `r43-closure.sh`, `claim-package-check.py`, `r44-routed-defects.py`,
`wave-registry.py`) and **no row** in the `SKILL.md` Gates & probes registry (the
commit's SKILL.md append adds only `claim-package-check.py` and `r43-closure.sh`).
Round-43 routed defect 7 (`corpus/lessons/round-43-verifier-spotcheck.md` §6 item 7)
was exactly this: instruments absent from the registry, "`git grep` there → 0 hits".
Round 44 fixed it for the round-43 pair and immediately repeated the class for its
own C2 counter: a later reader has no entry command, verdict map or write-scope row
for the one instrument whose frozen counter string it replaces. No gate enforces
registration (grep over `r42-closure.sh`, `r43-closure.sh`, `r43-limbs/` for
`instruments/README|registered` → no matches), so this is a discipline gap, not a
gate flip.

### 2.2 `r44-frontier-count.py` vs `frontier-recheck-count.py` — near-name, different units

Both count the frontier of `corpus/README.md`. On the same committed `after` tree:
`r44-frontier-count.py` prints `frontier rows=26 admitted=26 exit=0` (row census,
status cell = third cell) while the older gate prints `entries=29 pass=29 exit=0`
(per-entry records; 29 on after, 28 on the parent tree). The numbers 26 and 29 look
contradictory if quoted without units — and the newer instrument is the
unregistered one (§2.1), so a later reader who greps the registry lands on the
round-24 gate and may cite `entries=29` for a claim whose frozen counter is the
row census. Predicates differ legitimately (census vs source-recheck validation);
the collision is in name and citability, not in behaviour. Smallest safe
correction: append the missing registry row for `r44-frontier-count.py` stating the
unit (rows with status cell `admitted`) and its relation to
`frontier-recheck-count.py` rule G.

### 2.3 The disposition receipt and the committed tree contradict each other

`.ufo/waves/round-44/controls/r44-counter-trial-disposition.txt` (committed in this
round) states `r44-routed-defects.py` "is NOT an accepted verifier and **is not
present under `corpus/instruments/` at the final tree**" and orders "discard the
counter as a production gate … report C1 unverified". The round's commit lands it
(`corpus/instruments/r44-routed-defects.py | 554 +++` in `git show --stat
8063547d`), rebuilds it with a marker-only mutant battery (selftest `cases=11
failures=0`, mutants rejected), and `c1-counter-baseline.txt` header calls these
"attempt-2 control receipts", while `c1-do-nothing.txt` still ends "C1 remains
unverified." Four committed receipts now carry three different stances (discarded /
accepted-with-exit-0 / unverified). No old gate reads these receipts, so this is
not a no-harm break — but it is exactly the mistaken-identity surface this item
asks about: a later reader cannot tell from the receipts alone whether the C1
counter is an accepted gate or retained failed evidence. Smallest safe correction:
append (never rewrite) one receipt superseding the disposition's "not present at
the final tree" clause with the attempt-2 relanding decision.

### 2.4 Wave-1 predicate names a registry path that was not landed

`R44Exec1.md:115` (committed) predicates on
`.ufo/waves/round-44/w1-REGISTRY.txt`; the emitter's landed output is
`.ufo/waves/round-44/wave-registry.txt`. A reader following the wave-1 predicate
finds no such file. Path drift inside the round, same class as §2.3.

### 2.5 Selftest scratch default skips the lane's `$HYAKU_SCRATCH` convention

`r44-routed-defects.py:538` defaults `--work` to `$TMPDIR`/`tempfile.gettempdir()`.
Every older selftesting instrument documents "$HYAKU_SCRATCH, then $TMPDIR"
(`capture-binding-check.py:1114-1115`, `frontier-recheck-count.py:498-499`,
`kill-rule-check.py:687-688`). Observed: with `TMPDIR=<scratch>` and no `--work`,
the selftest writes `r44-routed-defects-*` under TMPDIR and removes it (0
leftovers). Documented in the README row ("default $TMPDIR"); no gate affected;
convention drift only. The default grading mode never writes (§1 item 6).

## 3. CLI and receipt-path collision check (no collision found)

- Flags: `--root` is the lane-wide convention; `--selftest` reuse is convention,
  not collision; `--baseline`/`--expect`/`--ids`/`--results`/`--wave` are unique to
  the new instruments; `--work` matches `r43-closure.sh`'s existing flag name with
  the same meaning (scratch root). Full flag inventory grepped across all
  `corpus/instruments/*.py`.
- Receipt paths: `wave-registry.py` writes only caller-specified `--out`; the
  committed output path is claimed by no older gate; the r44 counter and frontier
  counter write nothing in default mode (§1 item 6). Name spaces are disjoint from
  the older closure suites (`r35/r36-r43-closure.sh`, `r-defect-closure.sh`,
  `claim-package-check.py`, `kill-rule-check.py`); `CLOSURE_RX` does not match any
  new filename (§1 item 3).

## 4. Limitations

- `r42-closure.sh` J3 verified statically (regex + code path), not by a full r42
  suite run; the suite's export-mode contract would have made that a separate
  receipt exercise. The before/plus3 equality of the three gates that read
  instruments-adjacent state (items 1-2) bounds the risk.
- `kill-rule-check.py --selftest` covers verdict arithmetic only, per its own
  README section; the `default_fake` surface was checked statically (§1 item 4).
- I did not adjudicate C1/C2 truth, the frozen-counter substitution legitimacy, or
  whether the attempt-2 relanding of the counter was authorised; §2.3 records the
  contradiction only.
- No tool installs were needed (python3 + coreutils only).

## Receipt

- Report: `.ufo/waves/round-44/wave2/R44W2Crit08.md` (this file), written by
  R44W2Crit08; scratch `/fast/scratch/hyaku/kasegi-r44/R44W2Crit08/` removed before
  yield; no production file edited; no git/jj mutation; no pacman.
