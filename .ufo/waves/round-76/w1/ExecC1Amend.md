# ExecC1Amend — round-76 w1 — C1 counter amendment (scratch-only candidate)

Seat: ExecC1Amend-3 (leaf executor, C1 / depth:verifiability). Lane: kasegi-shokunin.
Freeze: commit `5da54cd4451cbbb9e4b87e2f83475feb13c65c9e` (base `a788021675873a96e09e91aa033d8c26ac2fe212`).
Deliverable: the C1 amended counter as a scratch-only candidate for L1 integration, with all receipts. This seat did NOT apply anything to the lane working tree and did NOT commit.

## Files delivered (all in this dir)

| File | Content |
|---|---|
| `ExecC1Amend.patch` | unified diff base→amended, labels `a/`+`b/corpus/instruments/recheck-cwd-census.py`, 104 lines, applies cleanly onto the frozen bytes |
| `ExecC1Amend.amended.py` | full amended counter, 332 lines, sha256 `e25d3c006f0820ceccfbf974e94634d1554ee07d253766d2ef8980a3806bac28` |
| `ExecC1Amend.exec-surface.txt` | A5 call-site receipt |
| `ExecC1Amend.baseline-selftest.txt` / `.baseline-realtree.txt` | do-nothing reproduction with the base bytes |
| `ExecC1Amend.amended-selftest.txt` / `.amended-realtree.txt` | A1 / A2+A4 receipts |
| `ExecC1Amend.mutant-m1a-run.txt` / `-m2a-` / `-m3a-` | A3 receipts, amended-byte mutants |
| `ExecC1Amend.mutant-diff-parity.txt` | per-mutant hunks proving amended-byte mutants carry the same mutations as the committed base mutants |

## Amendment content (exactly 4 hunks; `census()`, `main()`, `run_foreign()`, `first_recheck()`, `has_restoration_recheck()` untouched)

1. Module docstring: "--selftest runs six cases" → "--selftest runs eight cases", names `relabel-pair` and `both-headers`; print literal → `'selftest cases=8 failures=%d'`.
2. `selftest()` docstring updated to eight cases with the two new case names.
3. Case 6 limb restructured: `res6 = (ret6 == 1 and "RECHECK-CWD-RESULT nonconformant" in out6)` computed, consumed in the `check(...)` call (`and not marker6 and res6`) and echoed in the detail line — the limb's removal from the bytes is now an observable failure.
4. New case 7 `relabel-pair`: `x.md` = `# fixture\nbody\n` (no recheck-ish header), `r.md` = only `restoration-recheck: touch <root>/restoration-ran`, `p.md` = `recheck: cd <root> && true`; asserts tally `entries=3 noprefix=0 exit2_foreign=0 exit0_foreign=1 exit1_foreign=0 exit_other=0 norecheck=1 restoration_only=1`, marker absent, `main()` prints `RECHECK-CWD-RESULT nonconformant` and exits 1. New case 8 `both-headers`: `b.md` carries the restoration-recheck header (its first recheck-ish line) and the recheck line (second), plus `p.md` prefixed passing; asserts `entries=2 noprefix=0 exit2_foreign=0 exit0_foreign=2 norecheck=0 restoration_only=0`, marker absent (restoration value never runs), `main()` conformant exit 0 (positive control: blanket refusal is not a gain).

Note on case 8 fixture bytes: the counter's `write_entry` convention prefixes every fixture with `# fixture\n`, so the restoration-recheck header is the file's first *recheck-ish* line, matching the spec's "(FIRST line)" for headers; classification is order-insensitive in any case because `startswith("recheck:")` never matches a `restoration-recheck:` line (disjoint prefixes).

## Receipts (command → result; every check was run)

Scratch `S=/fast/scratch/hyaku/kasegi-r76/ExecC1Amend`; all runs used `TMPDIR=$S/tmp` (passed explicitly; also honored by the selftest's own `mkdtemp(dir=os.environ.get("TMPDIR") or None)`).

1. Base export: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 5da54cd4451cbbb9e4b87e2f83475feb13c65c9e:corpus/instruments/recheck-cwd-census.py > $S/base-counter.py` → sha256 `e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a` — matches the frozen pin exactly.
2. Do-nothing, selftest: `TMPDIR=$S/tmp python3 -B $S/base-counter.py --selftest` → `selftest cases=6 failures=0`, rc=0.
3. Do-nothing, real tree: `TMPDIR=$S/tmp python3 -B $S/base-counter.py --root <lane> --lane <lane>` → receipt (`RECHECK-CWD entries=91 ... restoration_only=0` + `RECHECK-CWD-RESULT conformant` + `census_rc=0`) **byte-identical** to `.ufo/waves/round-76/controls/c1-donothing-realtree-r76.txt` (3-line whole-file equality, `True`), rc=0 — lane tree is still at freeze state.
4. **A1**: `TMPDIR=$S/tmp python3 -B $S/amended.py --selftest` → all eight cases `ok`, `selftest cases=8 failures=0`, rc=0, stderr empty.
5. **A2+A4**: `TMPDIR=$S/tmp python3 -B $S/amended.py --root <lane> --lane <lane>` → `RECHECK-CWD entries=91 noprefix=0 exit2_foreign=0 exit0_foreign=69 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0`, `RECHECK-CWD-RESULT conformant`, rc=0, stderr empty; 3-line receipt **byte-identical** to the control (empty diff), so the base-vs-amended real-tree stdout parity diff is empty too.
6. **A3** amended-byte mutants (each: `TMPDIR=$S/tmp python3 -B $S/<mutant>.py --selftest`):
   - `m1a-forged-relabel.py` (M-R1): rc=1, `selftest cases=8 failures=1`, killed by `relabel-pair FAIL` (got `norecheck=0, restoration_only=2`, want `norecheck=1, restoration_only=1`).
   - `m2a-result-limb-removed.py` (M-R2: the `res6 = ...` computation line deleted; consumption retained): rc=1, crash at case 6 — `NameError: name 'res6' is not defined` — the limb removal is observable. (In the base bytes the limb lived inline in the `check` call, which is why the committed M-R2 could delete it silently; the restructure closes exactly that.)
   - `m3a-restoration-forces.py` (M-R3): rc=1, `selftest cases=8 failures=2`, killed by `relabel-pair FAIL` and `both-headers FAIL` (got `restoration_only=1, exit0_foreign=1, main_ret=1, result_ok=False`, want `restoration_only=0, exit0_foreign=2, main_ret=0`).
7. Mutation parity: my base-byte rebuilds from the same patch shapes are **byte-identical** to the committed mutants `mut/m1-forged-relabel.py`, `mut/m2-result-limb-removed.py`, `mut/m3-restoration-forces.py` (`True`/`True`/`True`), and the header-stripped diffs base→m1 vs amended→m1a and base→m3 vs amended→m3a are identical (`True`) — m1a/m3a are the same mutations on amended bytes.
8. **A5** (see `ExecC1Amend.exec-surface.txt`): exactly one `"bash", "-c"` pair and exactly one `subprocess.run` call site (both line 70, `run_foreign`); exactly two `tempfile.mkdtemp` sites (lines 65, 136, both `dir=` from `TMPDIR`); the only file writes (`open(...,"w")` line 139, `os.makedirs` line 145) are selftest fixtures under the line-136 scratch; no hard-coded `/tmp`. Unchanged from base.

## Claim mapping

- A1 ✔ (receipt 4), A2 ✔ (receipt 5, at this tree; drift expectation `entries=92, exit0_foreign=70` applies only after C2 lands — not this seat's check), A3 ✔ (receipts 6-7), A4 ✔ (receipt 5), A5 ✔ (receipt 8). A1/A2/A5 are asserted on these amended bytes; their landing-commit re-check is the L1's integration step.
- Kill-rule status: no mutant survives; no predicate was reworded; claims.json read in full before starting.

## Bounds compliance

- No writes into the lane working tree; only this wave-dir file set + my scratch. Read-only git (`git show`, plus `rev-parse`-free receipt reads); no stash/checkout/reset/commit/push anywhere.
- No network access, no pacman transactions, no tool installs, no host sysctls, no subagents spawned, no messaging beyond the two C1 peers that asked for status (ReviewC1-21, ExecC1Controls) — both answered with pointers to these deliverables.
- Exec surface of the counter unchanged (A5); TMPDIR honored in every run; scratch deletion receipt below.

## Scratch cleanup

`rm -rf /fast/scratch/hyaku/kasegi-r76/ExecC1Amend` executed after the copies above; post-check `ls` of the path errors with "No such file or directory" (receipted in the yield summary). Scratch dir deleted — no leftover-tree defect.

## Notes for L1 integration

- The `registry_pins` clause of C1: SKILL.md and `corpus/instruments/README.md` rows still pinning "selftest cases=6" must move to the amended count in the same landing commit (not this seat's files).
- The patch is against the frozen base bytes only; if C2's registry/knowledge changes land first, this patch is unaffected (it touches one instrument file).
- Re-derivation paths for reviewers: apply `ExecC1Amend.patch` to `git show 5da54cd…:corpus/instruments/recheck-cwd-census.py` and diff the result against `ExecC1Amend.amended.py` — it must be empty (sha256 `e25d3c00…bac28`).
