# ReviewC1 — attack of C1 (recheck-cwd counter amendment), round 74 attempt 1

Seat: ReviewC1 (leaf reviewer, no subagents). Reviewed object: the **frozen claim text** C1 in
`.ufo/waves/round-74/claims.json` at freeze commit 847b53792d2d29d161cad7d21a33c89df9e52e8d
(base/controls ccd6a54bf392922495c4860332665499582e3213), plus the four pre-freeze control
receipts. **The implementation commit does not exist yet**: `git rev-parse HEAD` = 847b5379…
(freeze) at 2026-11-05 ~08:50 UTC, and the counter blob is identical at all three named
revisions — `git rev-parse <rev>:corpus/instruments/recheck-cwd-census.py` = df8661f7a4f8… for
847b5379, ccd6a54, and 654d877 (exit 0 each). Every after-value that depends on the amendment
is therefore reviewed as claim text + re-derivation command; the two limbs derivable today
(base parity baseline, do-nothing control) were re-derived and are reported with commands and
exits. Scratch `/fast/scratch/hyaku/kasegi-r74/ReviewC1` (removed before yield; receipts first).

Evidence files (this wave dir):
- `ReviewC1-ev-fixtures.txt` — full battery transcript T1–T11, sha256 8c67445d…e6a05
- `ReviewC1-ev-parity-bytes.txt` — parity byte-compare receipt, sha256 1dfa82a2…67e1f3

Lane writes by this seat: none. My commands wrote only under the scratch root and this wave
dir. `git diff --stat` after all runs: empty. `git status --porcelain` went 7 → 8 lines during
the battery; the added line is `.ufo/waves/round-74/assimilation/` (`collisions`, `reg-ids`,
`staged-ids` — the integrator's S109 admission staging, mtime 08:46:42 UTC, concurrent with my
run but created by the integration lane, not by any census run: the counter writes only under
`--root` scratch/TMPDIR and its stdout; no tracked file changed). Recorded for transparency.

---

## 1. Predicate attack, clause by clause (§2)

For each after_predicate clause: the exact re-derivation command, then candidate trees where the
clause's letter is met while the intent (selftest kills M4 forced-conformant, M5 hard-coded /tmp
parent, M6 run_foreign scratch leak, M7 last-line reader) is not.

### Clause `selftest` — `cases=5 failures=0`, exit 0, five enumerated cases
Command (at the implementation revision): `cd <lane> && TMPDIR=<scratch>/tmp python3 corpus/instruments/recheck-cwd-census.py --selftest; echo exit=$?` → expect stdout tail `selftest cases=5 failures=0`, exit 0.

- **W1 tmpdir-parent vacuity — letter ADMITS, kill rule (a) EXCLUDES (F3, the one real trap).**
  The clause "every scratch directory the census creates resolves under TMPDIR" is a universal
  over the set of created dirs — vacuously true if the check only inspects dirs it *finds*
  under TMPDIR. Empirical sharpening (T4, `ReviewC1-ev-fixtures.txt`): the M5 mutant has an
  intact `finally: rmtree`, so it leaves **zero residue anywhere** after the run —
  `find /tmp -maxdepth 1 -name 'recheck-cwd-*' -type d | wc -l` = 0 after
  `TMPDIR=$S/tmp python3 mut-M5.py --selftest` (exit 0, `cases=1 failures=0`). So neither a
  /tmp residue scan nor a found-dirs-parent check can ever see M5. The only forms that kill M5
  are creation-side: intercept `tempfile.mkdtemp` and assert `dir` resolves under TMPDIR, or
  assert the count of scratch dirs created under TMPDIR during census ≥ 1 (under M5 that count
  is 0 because all scratch went to /tmp). **The frozen wording excludes the vacuous form only
  through kill rule (a)**: M5 applied to such an amendment exits 0 from --selftest → (a) fires →
  C1 fails. Claim safe; implementation must use a creation-count/interception form.
- **W2 first-line case with a commented-out second line — letter EXCLUDES.** The clause says
  "a fixture entry carrying two recheck: lines". A `# recheck:` line does not start with
  `recheck:` (the counter's own contract; demonstrated at T6 where `restoration-recheck:` is
  skipped), so a commented second line means the entry carries one recheck: line — the letter is
  not met. Independently, kill rule (a) excludes it: with a commented second line, orig and M7
  read the same first line, M7 survives exit 0 → (a) fires.
- **W3 result-main asserting only the exit code — letter EXCLUDES verbatim.** Quote:
  "result-main (runs main() in-process on a nonconformant fixture asserting
  RECHECK-CWD-RESULT nonconformant + exit 1, and on a conformant fixture asserting conformant +
  exit 0)" — the printed line is named as asserted. T2 shows why: M4 leaves the RECHECK-CWD
  line and the exit code untouched (census of a nonconformant tree still exits 1); only the
  RESULT string flips. `TMPDIR=$S/tmp python3 mut-M4.py --selftest` → exit 0,
  `cases=1 failures=0` (survival reproduced; matches red-before receipt row M4).
- **W4 scratch-cleanup vacuity — letter ADMITS (own-empty-tree form), kill rule (a) EXCLUDES.**
  If the amendment runs the cleanup check on its own *empty* fixture, census creates no scratch,
  the `glob == []` assertion passes vacuously — and M6 then also leaks nothing (no run_foreign
  calls) and survives → (a) fires. T3 confirms the non-vacuous signal exists:
  `mut-M6.py --selftest` (exit 0, `cases=1`) leaves delta=3 dirs in TMPDIR
  (`find $S/tmp -maxdepth 1 -name 'recheck-cwd-*' | wc -l` 0 → 3). The amendment's cleanup case
  must run over a tree with entries (e.g. share the prefix-census tree).
- **W5 first-line case with two identical lines — letter silent, kill rule (a) EXCLUDES.**
  "counts the FIRST line only" is only falsifiable if the two lines differ observably. If both
  are `cd <lane> && true`, orig and M7 are indistinguishable → M7 survives → (a) fires. T8 is
  the existence proof of the discriminating shape: second line prefix-less exit-2 →
  `mut-M7.py --root $S/fx/a2 --lane <lane>` prints `noprefix=1 exit2_foreign=1`,
  `RECHECK-CWD-RESULT nonconformant`, exit 1, while the base counter on the same tree prints
  `noprefix=0 exit0_foreign=1`, conformant, exit 0 (T7).
- **W6 selftest shadowing shipped code — kill rule (a) EXCLUDES.** If the selftest asserted
  against a reimplemented census instead of the module's `census()`/`main()`, applying M4–M7 to
  the shipped file would not change selftest results → all four survive exit 0 → (a) fires.
  The enumerated cases bind the real path: result-main runs `main()` in-process; prefix-census
  (retained) drives `census()` directly.

### Clause `census` — shape at the implementation revision
Command: `cd <lane> && TMPDIR=<scratch>/tmp python3 corpus/instruments/recheck-cwd-census.py --root <lane> --lane <lane>; echo exit=$?` plus `ls corpus/knowledge/*.md | wc -l`; expect `noprefix=0 exit2_foreign=0 exit_other=0 norecheck=0`, `RECHECK-CWD-RESULT conformant`, exit 0, entries == file count.
Re-derived today at base: T10 (`TMPDIR=$S/tmp python3 base-counter.py --root $S/base --lane <lane>`, counter+corpus both from ccd6a54) → `RECHECK-CWD entries=89 noprefix=0 exit2_foreign=0 exit0_foreign=67 exit1_foreign=22 exit_other=0 norecheck=0` + `RECHECK-CWD-RESULT conformant`, exit 0; file count `git archive ccd6a54 corpus/knowledge | tar -x` → 89 (`find … -name '*.md' | wc -l`), entries == count. **No green-while-wrong constructible at the implementation revision that parity does not also catch**: C1's commit leaves the corpus identical to base, so any tallying-byte drift (e.g. swapped exit0/exit1) changes the base-revision line too and hits kill rule (b). The shape-only binding at the implementation revision is deliberate per the freeze note ("binds shape (zeros + entries==file count), not absolute entries/exit0 counts, so C2's landing cannot falsify it (RC-6 class)") — quoted, not reworded.

### Clause `parity` — amended counter at base byte-identical to receipt
Command (at the implementation revision): export counter from impl rev + `git archive ccd6a54 corpus/knowledge` → `TMPDIR=<scratch>/tmp python3 <impl-counter>.py --root <export> --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin`; stdout must byte-equal the receipt's two census lines, exit 0. Note the `--lane` must be the real lane path: the corpus lines carry the absolute `cd <lane> && ` prefix, so `noprefix=0` requires it even when `--root` is an export. Future-state; baseline verified today (§3).

---

## 2. Off-tree falsification (§3)

All runs from scratch; counter = `git show ccd6a54:corpus/instruments/recheck-cwd-census.py`; fixtures under `$S/fx`. Full transcript with exits: `ReviewC1-ev-fixtures.txt`.

- **T6 / F2 (verified, INFO): restoration-recheck exclusion holds as the scope sentence states.**
  Fixture A1: first line `recheck: cd <lane> && true`, second line
  `restoration-recheck: python3 corpus/instruments/absent-r74-probe.py` (prefix-less).
  `TMPDIR=$S/tmp python3 base-counter.py --root $S/fx/a1 --lane <lane>` →
  `entries=1 noprefix=0 exit2_foreign=0 exit0_foreign=1 … norecheck=0`, conformant, exit 0.
  The prefix-less restoration-recheck line did not enter the counted population — exactly the
  frozen sentence "'restoration-recheck:' is a different header and is out of the counted
  population by definition (named here per RC-5)" (quoted; RC-5 in corpus/lessons/round-73.md).
  Mechanically: `line.startswith("recheck:")` is false for `restoration-recheck: …`.
- **T7/T8 (verified): second prefix-less `recheck:` line is ignored by the first-line rule and
  discriminates M7** — the two-line fixture shape the claim's `first-line` case prescribes is
  sufficient and necessary (see W5).
- **T9 / F1 (MINOR, counter property, zero corpus incidence): no fence awareness.** Fixture B:
  a doc line starting `recheck: ` at column 0 inside a ``` fence, placed *before* the real
  recheck line. Base census → `ENTRY e1.md noprefix=1 foreign_exit=2`,
  `noprefix=1 exit2_foreign=1`, nonconformant, exit 1 — **the fenced line is counted**;
  `first_recheck` scans raw lines with `startswith` and has no fence concept. Frozen scope?
  The scope sentence names only the first-line-per-file rule and the restoration-recheck
  exclusion — it neither requires nor forbids fence awareness, so counting a column-0 fenced
  line is **within the letter** of the frozen scope (it is the first line starting `recheck:`
  in that file). Intent arguably excludes it (a fenced line is documentation, not an executable
  recheck). Corpus incidence at base: **zero** — scan over all 89 exported files (fence toggle
  on lines starting ``` or ~~~): lines starting `recheck:` inside fences = 0; files whose first
  `recheck:` line is fenced = 0. Consistent with the conformant base census (any fenced
  column-0 example earlier than the real line would have surfaced as noprefix/exit2). No claim
  impact; noted so a future fenced `recheck:` example in the corpus is not mistaken for a
  counter regression.

---

## 3. Parity limb soundness (§4)

`ReviewC1-ev-parity-bytes.txt` (receipt F1–F3 lines):
- claims.json parity quote — `RECHECK-CWD entries=89 noprefix=0 exit2_foreign=0 exit0_foreign=67 exit1_foreign=22 exit_other=0 norecheck=0`
- receipt line — byte-identical (`python ==` → True), including `conformant` **lowercase**;
  capitalization scan over the parity text finds the single variant `['conformant']`.
- Re-derivation (T10, exit 0): base counter over the ccd6a54 corpus export prints both lines
  byte-identical to the receipt (`(t10_cwd, t10_res) == (receipt_cwd, receipt_res)` → True).

Verdict: the parity sentence's quoted line is byte-exact against the receipt, and the receipt
itself re-derives from committed state. The amended-counter half of the limb is future-state
(command stated in §1, clause `parity`).

---

## 4. Kill-rule complement check (§5)

Every green-while-wrong way I can construct maps to a kill clause or an after_predicate limb:

| # | Green-while-wrong way | Caught by | Evidence |
|---|---|---|---|
| 1 | selftest too weak / vacuous / shadowed for any of M4–M7 | (a) — mutants re-applied to the amended counter; any exit-0 survival fails C1 | T2–T5 reproduce all four survivals against the *current* selftest (`mut-M{4,5,6,7}.py --selftest`, each exit 0, `cases=1 failures=0`), matching red-before row-for-row |
| 2 | parity drift (any tally byte, incl. swapped exit0/exit1) | (b) + parity clause | byte-compare receipt F; T10 |
| 3 | false-positive killing / blanket refusal / broken conformant fixture | (c) | claim text |
| 4 | bash -c call-site expansion | (d) + grep receipt + sentinel seat | claim text; RC-8 respected — nothing here proposes exec-surface changes |
| 5 | counting drift visible only at the implementation revision | parity (b): C1's commit keeps corpus == base, so the drift shows at base too | §1 census clause |
| 6 | mutants killed by crash/exception rather than assertion | not a gap: (a) keys on exit 0; a crashing mutant is not surviving | claim letter |

**Gaps and residual risks named (none rises to a claim defect):**

- **G1 (MINOR, verification gap — load-bearing evidence not yet in existence):** the
  after_predicate's case letters (W1/W4/W5) admit vacuous or undiscriminating implementations;
  *all* mutant-killing strength flows through kill rule (a)'s re-application of the four
  classes to the amended counter. The only existing kill evidence is red-before for the
  **unamended** counter (reproduced here, T2–T5). The amended-counter kill matrix (4 selftest
  runs) is therefore the decisive C1 evidence and must be produced and receipted at
  implementation evaluation — if it is not, C1 is unverifiable as frozen.
- **G2 (INFO, operational):** (a) keys on exit code; a mutant that *hangs* the selftest would
  stall evaluation rather than yield a verdict (not green-while-wrong — no exit 0). Whoever
  runs the matrix should wrap each mutant run in `timeout`.
- **G3 (INFO, well-definedness):** kill rule (a) names the four classes by intent; "applied to
  the amended counter" stays mechanical only if the amendment keeps the four sites recognizable
  (run_foreign's `mkdtemp(dir=…)` and its `finally`, the RESULT print in `main()`,
  `first_recheck`'s loop). A rewrite that dissolves those shapes makes (a) a judgment call.

**Implementation traps carried forward from §1 (for the amending seat, all closed by (a) if
ignored):** tmpdir-parent must assert *creation* under TMPDIR (count ≥ 1 or mkdtemp
interception) — T4 shows M5 leaves no residue to scan for; scratch-cleanup must run over a
non-empty tree; the first-line fixture's two lines must differ observably (prefix-less exit-2
second line is the demonstrated discriminator, T7/T8).

**Positive controls re-derived:** do-nothing control T1 — base counter `--selftest` prints
`selftest cases=1 failures=0`, exit 0 (cannot reach cases=5; matches do_nothing_control).
Red-before receipt rows M4–M7 all reproduced exit 0 / `cases=1 failures=0` (T2–T5).

---

## Findings index

- **F1 — MINOR.** Counter has no fenced-block awareness; a column-0 `recheck:` line inside a
  code fence is counted (T9, exit 1, noprefix=1 exit2_foreign=1). Within the frozen scope
  letter (scope sentence makes no fence exception); zero corpus incidence at base (0 lines in
  89 files). Not a claim defect; corpus-hygiene note for future entries.
- **F2 — INFO (verified).** restoration-recheck exclusion and first-line-only counting both
  hold empirically on off-tree fixtures (T6 exit 0 conformant; T7 exit 0 conformant), and the
  two-line fixture discriminates M7 exactly as the claim's first-line case intends (T8 exit 1).
- **F3 — MINOR (wording), highest practical risk.** tmpdir-parent clause is vacuous-satisfiable
  in its letter (universal over a possibly-empty set); only kill rule (a) excludes the vacuous
  form. Amendment must use a creation-count/interception form or the wave dies on (a).
- **F4 — MINOR (verification gap).** Amended-counter kill matrix (kill rule (a)'s subject)
  does not exist as a control yet; must be receipted at implementation evaluation (G1), with
  `timeout` around mutant runs (G2) and recognizable mutant sites (G3).
- **F5 — INFO.** Lane status 7→8 delta is the integrator's `.ufo/waves/round-74/assimilation/`
  staging, not a census side effect; `git diff --stat` empty; no tracked file changed.

No BLOCKER/MAJOR finding against the frozen claim text: the predicate + kill rule conjunction
closes every green-while-wrong path I could construct; the parity limb is byte-sound; the
do-nothing control holds.

## Residual risk and verification gaps

- Selftest (cases=5), implementation-revision census shape, and amended-counter parity are
  future-state; re-derivation commands are in §1. Kill matrix per G1 pending implementation.
- RC-8 untouched: nothing in this review runs or proposes a new bash -c call site; my census
  runs used the shipped counter's existing single run_foreign call path.
- Tooling: none installed or upgraded (operator rules read; pacman paused observed — no
  transactions run; host Python 3 as found).

Scratch `/fast/scratch/hyaku/kasegi-r74/ReviewC1` removed before yield (receipts copied first;
final `find` check reported in the yield).

**Erratum (report finalized at 05:49 local, re-checked 05:50):** shortly before yield, HEAD
moved 847b5379 → a5e814a1679626b6d9fb9ba3f1a6483ed4f4b68c. Inspection
(`git show --stat a5e814a`) shows it commits **only** the missing
`.ufo/waves/round-74/controls/freeze-check-replay-r74.txt` receipt (R73-V6; 18 insertions);
`git rev-parse HEAD:corpus/instruments/recheck-cwd-census.py` is still df8661f7a4f8… — the
amendment has **not** landed. The "implementation does not exist yet" posture of this review
stands unchanged; only the HEAD hash above was current at write time.
