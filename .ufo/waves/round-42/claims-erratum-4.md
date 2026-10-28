# kasegi round-42 claims erratum 4 — instrument defects found at integration, repaired before the judged head

Frozen claims: `.ufo/waves/round-42/claims.json` (commit `0566bd66e93d429b2df8b6751cf10cbdc391e79b`), clarified by
errata 1–3. This erratum records **implementation defects in the C1 instrument** (`corpus/instruments/r42-closure.sh`)
that made C1's frozen after-state unreachable, and the repairs landed before the judged head J. No predicate, target,
counting command, kill rule or score changes: C1 still requires `closed=13/13 exit=0` and `selftest cases=13
failures=0` at Y, and the seven replay limbs still must reject their committed defeats.

State at record time: the instrument scored `closed=10/13 exit=1` and `selftest cases=13 failures=3` at the round-42
integration head before these repairs (`de09313e8edb98280b19767d0094bb2dd8031d73`). No seat scored the C1 after-state
as met: every wave-1 receipt that touched C1 recorded it red (`.ufo/waves/round-42/wave1/`). These are instrument
repairs, not a narrowing or a post-hoc rule change — each one makes a check that reported a false pass (or a
structurally impossible pass) actually grade what its own predicate sentence says.

- **E-R1 — J1/F-EVID replay limb mutated an ungraded line.** `replay_j1` and `strip_evidence_copy` selected the
  first correction line whose evidence changed under stripping, across *all* rounds; `check_j1` grades only
  `Correction (round 42)` lines. The mutation therefore landed on a round-39/41 line and `check_j1` accepted the
  mutated tree (`replay=RevC1Counters.md=accepted`, `selftest case=J1 mutants=0/1`). Repair: both limbs select
  from `graded_lines(text)` — round-42 correction lines carrying a claim token — and require that the stripped
  line actually loses every evidence id. Observed after repair: `replay=RevC1Counters.md=rejected`,
  `selftest case=J1 mutants=1/1 positive=pass verdict=pass`.
- **E-R2 — J1 `union` cell was a hardcoded literal.** The payload printed `union=0` unconditionally, so the
  cross-record-union defect the check exists to reject was not measured. Repair: `union` is now the count of
  graded records whose own lines lack evidence while pooled evidence from other records would have covered them,
  and `ok` requires `union == 0`. Observed after repair: `union=0` on the real tree and `union=1, missing=1` on the
  stripped fixture.
- **E-R3 — J4 counted a declared `dyn` path's absence as an escape.** `.ufo/waves/round-42/declared-blocks.txt`
  declares the receipt as `dyn unpinned`; at J (the commit before the receipt) the file is legitimately absent, so
  `check_j4` reported `valid=468,escape=1` and stayed red. Repair: a declaration whose kind cell is `dyn` is
  valid because the run materialises it, and it is still rejected if it is absolute, contains `..`, or resolves
  outside the export root. Observed after repair: `declared=469,valid=469,escape=0` at J and at Y.
- **E-R4 — J10 graded `line_ok` as `verdict == pass`, and J8/J10 `payload-match` had no baseline.** `line_ok`
  conflated the isolation check with the transcript's pass/fail tally, and `run_selftest` graded J8/J10 against
  payloads that are computed *after* it returns, so their `payload-match` was structurally 0 in both modes.
  Repair: (a) `line_ok` means the case emitted a graded `selftest case=J<n> ...` line (matching `SELFTEST_RX`),
  which is what J10's isolation check measures; the pass/fail tally stays enforced by the summary line and J8's
  `verdicts`/`summary` facts; (b) `run_selftest` iterates to a fixed point, planting `J10` and `J8` payloads
  before grading, so `payload-match` compares two computations of the same function. Observed after repair:
  `selftest case=J10 mutants=2/2 positive=pass payload-match=1 verdict=pass`.
- **E-R5 — J8 canonical mode graded a transcript that contained its own verdict.** When no receipt is committed
  yet (the minting run at J), `check_j8` built the canonical transcript from the live selftest lines, so its
  `verdicts`/`summary` facts depended on its own verdict. Repair: canonical mode grades a synthetic all-pass graded
  block (thirteen graded lines + `selftest cases=13 failures=0`) over the real payload lines; the committed
  receipt at Y is still graded from its own bytes, so a receipt that records any failing verdict still fails.

Frozen text preserved: C1's predicate, its five counting commands, its kill rule and its after-state sentence are
unchanged. The receipt remains the teed transcript of one observed run+selftest at its named ref, and J/Y keep the
meaning errata 1–3 gave them (J = every round-42 change except the receipt; Y = J + the receipt only).
