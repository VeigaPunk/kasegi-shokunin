# RevPredicateIndependent — independent re-derivation of the C1 before-count

Scope: round 25, wave 1 (build). Read-only seat. Base revision
`b49948f1164ef65106b2c4cbee3f53e8a44b8c41` (equal to lane HEAD at the time of this run).
Compared against `.ufo/waves/round-25/c1-before.json` (frozen receipt).

## Verdict

**Zero disagreements.** `lines=35 pass=6`, and the per-line PASS/FAIL vector is identical to
the receipt's.

```
mine    : F P F F F F F P F P F F F F F F F F P F F F F F F P F P F F F F F F F
receipt : F P F F F F F P F P F F F F F F F F P F F F F F F P F P F F F F F F F
```

(35 entries in `sort` order; `P` = pass. Vector string, alphabetical:
`FPFFFFFPFPFFFFFFFFPFFFFFFPFPFFFFFFF` for both.)

| # | entry | limbs parse,cwd,paths | lane rc | foreign rc | mine | receipt | mine (isolated base tree) |
|---|-------|----------------------|---------|------------|------|---------|---------------------------|
| 1 | `ai-assisted-finding-validation.md` | 101 | 0 | 2 | FAIL | FAIL | FAIL |
| 2 | `authorised-testing-rules-of-engagement.md` | 111 | 0 | 0 | PASS | PASS | PASS |
| 3 | `authorization-safe-harbor-and-scope.md` | 101 | 0 | 2 | FAIL | FAIL | FAIL |
| 4 | `citation-bases.md` | 101 | 0 | 2 | FAIL | FAIL | FAIL |
| 5 | `claim-anatomy-sample.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 6 | `claim-gates.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 7 | `claim-package-contract.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 8 | `cna-assignment-and-vulnerability-rules.md` | 111 | 0 | 0 | PASS | PASS | PASS |
| 9 | `coordinated-disclosure-timelines.md` | 101 | 0 | 2 | FAIL | FAIL | FAIL |
| 10 | `cra-manufacturer-reporting-duties.md` | 111 | 0 | 0 | PASS | PASS | PASS |
| 11 | `cvss-v4-severity-and-vector.md` | 101 | 0 | 2 | FAIL | FAIL | FAIL |
| 12 | `cwe-top25-2025-methodology.md` | 101 | 0 | 2 | FAIL | FAIL | FAIL |
| 13 | `ev-model.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 14 | `evidence-dir.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 15 | `intake-and-finalize.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 16 | `intake-surface.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 17 | `mission-control.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 18 | `mission-ledger.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 19 | `multiparty-vulnerability-coordination.md` | 111 | 0 | 0 | PASS | PASS | PASS |
| 20 | `operator-queue.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 21 | `ops-invariants.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 22 | `policy-access-playbook.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 23 | `program-quirks.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 24 | `repo-git-state.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 25 | `retirement-autopsies.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 26 | `root-loss-2026-10-12.md` | 111 | 0 | 0 | PASS | PASS | PASS |
| 27 | `source-tree-loss-2026-09-28.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 28 | `statutory-authorization-and-unauthorized-access.md` | 111 | 0 | 0 | PASS | PASS | PASS |
| 29 | `submitted-registry.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 30 | `target-checkouts.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 31 | `terminal-classes.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 32 | `triage-thresholds.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 33 | `ufo-archive-2026.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 34 | `ufo-workspaces.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |
| 35 | `vdp-disclosure-packages.md` | 011 | 2 | 2 | FAIL | FAIL | FAIL |

Limb totals: `parse=23`, `cwd=6`, `paths=0` — identical to the receipt's `failing_limbs`.

## Method (independent implementation)

`rev-independent/independent-recheck.py` — written from the frozen predicate text in
`claims.json`, before the lane instrument was read, stdlib only, no import of
`corpus/instruments/recheck-audit.py`:

1. Entry list and bytes come from the base blobs, not the worktree:
   `git -C <lane> ls-tree b49948f corpus/knowledge/` + `git show b49948f:corpus/knowledge/<f>`
   exported into `rev-independent/scratch-lane/base/corpus/knowledge/`. 35 files, 35
   `recheck:` lines, exactly one per entry (verified by an independent count).
2. `parse` = `bash -n -c "<line>"` exits 0.
3. `cwd` = `bash -c "<line>"` from the lane root and from `/` agree on **exit status and
   digest** of captured stdout+stderr. Digest = `sha256(b"OUT\0"+stdout+b"\0ERR\0"+stderr)`
   (my own labelling; see "definitional choices").
4. `paths` = at least one lane-relative `corpus/…` token (or a `~/Projects/…` base test),
   and every `corpus/` token exists under the run root.
5. `pass` = parse ∧ cwd ∧ paths. Timeout 300 s per run; none fired. Whole audit ~1.1 s.

Two independent runs:

- **A** — run root = the real lane root (`.ufo/waves/round-25/wave1/rev-independent/independent-lane.json`):
  `lines=35 pass=6 fail-closed=29`, exit 1.
- **B** — run root = an immutable `git archive b49948f` export of the whole tree
  (`rev-independent/base-tree/`, `independent-tree.json`): `lines=35 pass=6 fail-closed=29`,
  exit 1, same vector. This rules out live-worktree drift from concurrent wave-1 edits.

## Disagreements

Compared per entry over all 35, on `pass`, `limbs.parse`, `limbs.cwd`, `limbs.paths`,
`lane_exit`, `foreign_exit`, `missing_paths`, and the `command` text:

- **0** PASS/FAIL disagreements.
- **0** limb disagreements.
- **0** exit-status disagreements.
- **0** command-text disagreements (same extraction).
- **70** raw digest-field differences — all explained by the digest recipe, not content.
  The receipt's recipe is `sha256(stdout + b"\0" + stderr)`; re-running every one of the 35
  lines in both cwds and re-deriving under *that* recipe reproduces all 70 receipt digests
  **and** all 70 exit codes exactly: `mismatches: 0`. So the digest vectors agree line for
  line once the label bytes are removed; no line differs in observed behaviour.

Reasons for the failing limbs (verbatim evidence):

- 23 × `parse`: all the same shape, e.g.
  `bash: -c: line 1: syntax error near unexpected token '('` — the trailing prose
  parenthetical `(fails closed today: …)` opens a subshell that is never closed. The
  `on-restoration — ` prefix alone would parse; the parenthetical is the breaker.
- 6 × `cwd` (lane rc 0, foreign rc 2), e.g. `ai-assisted-finding-validation.md` from `/`:
  `python3: can't open file '//corpus/instruments/source-recheck.py': [Errno 2] No such file or directory`.
  These lines carry no `cd`, so they are lane-cwd-only.
- 0 × `paths`: every `corpus/…` token named by any line exists at base
  (`corpus/instruments/*.py`, `corpus/source-snapshots/round-2{3,4}/manifest.json`,
  `corpus/knowledge/<entry>.md`).

## Definitional choices that could differ, and whether they move the count

1. **Digest recipe.** Mine labels the two streams; the receipt concatenates with one NUL.
   Changes digests, **not verdicts** (cwd limb is an equality test, and equality agrees on all
   35 lines). Does not change the count.
2. **Digest strictness (exact bytes vs exit-only).** Strict byte equality is what I applied.
   Under an exit-only reading the 6 cwd failures remain failures (rc 0 vs 2) and the 6 passes
   remain passes (rc 0 = rc 0); the count is unchanged at 6.
3. **Running parse-failing lines anyway.** I execute them to record the cwd limb, exactly as
   the receipt does (their entries carry lane/foreign exits and digests). A reading that
   short-circuits on parse failure yields the same verdicts.
4. **`bash -n -c` vs `bash -n` on stdin.** Same parser, same result; no line flips.
5. **Path-token extraction.** My regex requires a token boundary (so `(corpus/…` and
   `corpus/…` both match) and strips trailing `.,;:)]}"'`. The receipt's `paths` limb is true
   for all 35 as well, so no flip. I additionally verified `missing_paths == []` for all 35
   in both my runs and the receipt.
6. **"(c) names a lane-relative corpus/ path *or* a ~/Projects/ base test".** I honour the
   disjunction, so the prose lines' `~/Projects/bounties` counts. If a stricter reader
   required the *executable* part of the line to name the path, only the 23 prose lines would
   be affected — and they already fail on parse, so **the count stays 6**.
7. **First `recheck:` line per entry.** Each of the 35 entries has exactly one; no
   ambiguity.
8. **Run root for path existence.** Run A checks against the live lane root, run B against the
   base-tree export; both give `paths` true for all 35.

## Secondary findings (not verdict disagreements)

- **F1 (low, reporting).** `c1-before.json` header `fail_closed: 23` does not mean "lines not
  passing": its own `entries` contain 29 with `pass: false`, and its own `failing_limbs` are
  `parse=23, cwd=6` (23+6=29). The value is the count of `class == "fail-closed"`, and
  `corpus/instruments/recheck-audit.py:98` defines `class = "passing" if lane_rc == 0 else
  "fail-closed"` — so the 6 cwd-fragile lines (lane rc 0, foreign rc 2) are labelled
  `"passing"` while `pass: false`, and vanish from the headline
  (`pass + fail_closed = 29 ≠ lines = 35`). The human-readable counter line does print
  `cwd_fail=6`, so the data is reconcilable; only the JSON field name misleads. Recommend
  either defining `fail_closed` as `count(pass == false)` or renaming it to
  `class_fail_closed` before the C1 after-receipt is frozen.
- **F2 (low, hermeticity).** The 6 passes are not all hermetic. Five (`authorised-…`,
  `cna-…`, `cra-…`, `multiparty-…`, `statutory-…`) pass only because they hardcode
  `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin`, and the sixth
  (`root-loss-2026-10-12.md`) is a host-state assertion:
  `test ! -e ~/Projects/bounties && test ! -e ~/Projects/the-bounty-hunter && test ! -e ~/Projects/origin-work && test -e ~/Projects/ufo-fsd-alpha`
  (rc 0, no output, both cwds). If those host paths change, `pass` drops to 5 with no lane
  byte change. `pass=6` is therefore host-bound, and C1's after-count should not be read as
  "6 of 35 lines are cwd-portable"; only the 5 `cd`-prefixed ones are, and only on this
  workstation's path.

## Residual risk / verification gaps

- I did not measure the C1 *after* state or the target `pass=35`; this seat only re-derives
  the frozen before-count.
- Host-state coupling above (F2) means the before-count is reproducible on this workstation
  but not on an arbitrary host.
- Concurrency: at measurement time `corpus/knowledge/` was clean against base
  (`git status --porcelain corpus/knowledge` empty) and the vector was taken from base blobs;
  wave-1 scribes began editing entries immediately afterwards. That cannot move the result:
  command text is base-pinned, run B used an immutable `git archive` export, and no measured
  line reads a `corpus/knowledge/*.md` file at execution time (the 23 lines that name one fail
  `bash -n` before execution; the 6 well-formed ones call `source-recheck.py` on
  `corpus/source-snapshots/round-2{3,4}` manifests or assert host paths). Untracked additions
  (`corpus/instruments/recheck-audit.py`, `corpus/source-snapshots/round-25/`, new entries)
  are not referenced by any base `recheck:` line and do not enter the measurement.
- No tools were installed or upgraded for this seat.

## Artefacts (throwaway, under `.ufo/waves/round-25/wave1/rev-independent/`)

- `independent-recheck.py` — the independent implementation.
- `independent-lane.json`, `independent-tree.json` — run A / run B receipts.
- `scratch-lane/`, `scratch-tree/`, `base-tree/` — base-blob exports and the immutable
  `git archive` tree.
