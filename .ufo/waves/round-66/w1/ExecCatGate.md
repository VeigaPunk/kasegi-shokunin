# ExecCatGate — round-66 w1 — predata cat SIGPIPE masking repair and falsification

Seat: ExecCatGate (executor, leaf) · Round kasegi r66 wave w1 · Lane base `b6db9e818d322726e39cb441f2179d34d4170275`
Date: 2026-11-04 · Judged axis: depth:verifiability · No admission authority; findings only.

## Deliverable

- Candidate (v2, current): `.ufo/waves/round-66/w1/ExecCatGate/figure-audit.py`
  sha256 `51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac`, 585 lines
  (base production 528 lines + 57).
- v1 (docstring erratum below): sha256 `d48a5e45a2afa60abefb0cbc15ed4cca41bc6c6abdd40e3789a9db09b18479c7`,
  584 lines — reviewed by ReviewCat (own 43/43 matrix, behavior holds); v1 behavior receipts below
  were captured at v1 and remain valid: v2 changes docstring wording only, zero code delta.
- Provenance: byte-copy of production `corpus/instruments/figure-audit.py` at base
  (`86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef`, identical to the r65 adopted
  candidate hash recorded in the r65 spotcheck), then minimal patch. Production file NOT edited
  (verified: `git diff --stat` over the lane working tree is empty; only untracked round-66 artifacts exist).

## Repair semantics (one rule, finite claim)

`upstream_stale` now receives the killed stage's decoded argv. For `status == -SIGPIPE` with
`basename(head) == "cat"` the exemption holds iff `cat_sigpipe_exempt(argv)`:

- tokens = `argv[1:]`; a **leading** `--` is stripped as separator; otherwise **any token starting
  with `-` that is not exactly `-`** → conservative refusal (stale), named in the docstring as a
  capability restriction (option value semantics are not parsed; `cat -n big.txt` is refused even
  though single-file);
- exempt iff ≤1 remaining tokens. Zero operands (`cat`, `cat --`, `cat < f`) = stdin-only; one
  operand (`cat f`, `cat -- f`, quoted `'a|b'`, `'a b'` — already decoded by the tokenizer) = single
  input. Lone `-` counts as a stdin **input**: `cat -` green, `cat - a` stale (2 inputs),
  `cat f --` stale (trailing `--` is an operand token).

Multi-input cat SIGPIPE (operands ≥2, existing or missing) → stale with the **existing**
`derive-upstream-signal-13` label. Non-cat heads (incl. the r65 python-pipe benign case), other
signals, grep-exit1, final-stage precedence, `&&` semantics: unchanged.

## Exact patch anchors (v2, base line → candidate line)

| base | v2 | hunk |
|---|---|---|
| 40–41 | 38–40 | fail-closed parenthetical: "a non-exempt upstream signal — SIGPIPE from a multi-input or option-carrying cat is stale" (v2 erratum wording) |
| 46–48 | 46–55 | module docstring: SIGPIPE stays benign; for a cat head exemption applies only with at most one decoded input; conservative option refusal named; capability-restriction wording (v2 erratum wording) |
| 63 | 83 | `EXPECTED_CASES = 67` (R65 59+4; R66 +4 cat SIGPIPE shape) |
| 85–95 | 90–125 | new `cat_sigpipe_exempt(argv)` (90–104) + `upstream_stale(head, stage_argv, status)` (107–125) |
| 100 | 133 | `run_derive`: `stage_argvs` list added |
| 113 | 146–147 | `stage_argvs.append(list(argv))` |
| 128–129 | 161–162 | upstream callsite passes decoded `stage_argv` |
| 344 | 394 | `run_case(..., big=False)` flag |
| 347–348 | 402–410 | `big.txt`/`other.txt` 4 MiB fixtures (`alpha\n`+`x`×1023 lines; `beta\n`+`y`×1023 lines) |
| 475 | 516–532 | four new production-path cases after `upstream-sigpipe-nonfinal-benign` |

Candidate v2 digest: sha256 above; v1 digest `d48a5e45…`; base blob digest `86becbde…`.

## New selftest cases (production-path, public CLI, 4 MiB fixtures)

1. `upstream-cat-multi-missing-sigpipe-stale` — `cat big.txt missing.txt | head -n 1` want `alpha`,
   want exit 1 reason `derive-upstream-signal-13` (the base false green; red receipt landed as
   `1957407e` per L1, reproduced independently below).
2. `upstream-cat-multi-existing-sigpipe-stale` — `cat big.txt other.txt | head -n 1`, want exit 1
   reason `derive-upstream-signal-13` (conservative refusal: two inputs even when both exist).
3. `upstream-cat-single-operand-sigpipe-benign` — `cat big.txt | head -n 1` exit 0 (green at base too).
4. `upstream-cat-stdin-sigpipe-benign` — `cat < big.txt | head -n 1` exit 0 (stdin-only).

No assumed native status: cases assert the instrument's exit code + reason string only; a timing
fluke degrading cat to exit-1 would surface as `derive-upstream-exit-1` and FAIL the case loudly
(fail-closed). SIGPIPE delivery is forced by a 4 MiB first operand vs the 64 KiB pipe buffer
(base red control recorded native `141` on the same shape).

## Retained evidence (receipts, trailers relative to kasegi-shokunin)

- `.ufo/waves/round-66/w1/ExecCatGate/receipts/base-selftest-r66.txt` — base selftest control:
  `selftest cases=63 failures=0`, `exit=0`.
- `.ufo/waves/round-66/w1/ExecCatGate/receipts/candidate-selftest-r66.txt` — candidate selftest:
  `selftest cases=67 failures=0`, `exit=0`; all four new cases pass with expected exit + reason.
- `.ufo/waves/round-66/w1/ExecCatGate/receipts/candidate-selftest-v2-r66.txt` — v2 (post-erratum)
  selftest: `selftest cases=67 failures=0`, `exit=0`; all four new cases still pass.
- `.ufo/waves/round-66/w1/ExecCatGate/receipts/red-ledger-base-r66.txt` — base instrument on the
  4-case differential ledger: `figures=4 ok=4 stale=0 exit=0` (false green on P1/P2 reproduced).
- `.ufo/waves/round-66/w1/ExecCatGate/receipts/red-ledger-candidate-r66.txt` — candidate on the same
  ledger: `P-cat-multi-missing` and `P-cat-multi-existing` →
  `derived=UNAVAILABLE reason=derive-upstream-signal-13 stale`; `P-cat-single`, `P-cat-stdin` ok;
  `figures=4 ok=2 stale=2 exit=1`.
- `.ufo/waves/round-66/w1/ExecCatGate/receipts/real-ledger-base-r66.txt` +
  `real-ledger-candidate-r66.txt` — production ledger replay in the scratch clone at base:
  both `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`, stdout diff-identical (no regression on any
  committed derive; the ledger contains no multi-operand `cat … |` derive — grep-checked).

Every receipt records command, UTC, instrument/ledger/fixture sha256s, observed stdout, and rc.

## Falsification summary

Base at `b6db9e8` green-lights `cat big.txt missing.txt | head -n 1` (audit exit 0) while the native
untruncated pipeline fails (red control: `native_statuses=141`, `untruncated_cat_rc=1`) — masking.
The candidate refuses both multi-input shapes with the existing `derive-upstream-signal-13` label,
keeps stdin-only and single-operand green, and changes nothing on the production ledger (35/35,
byte-identical output). Claim C1 as dispatched is implemented; freeze/admission authority stays with
L1.

## Coordination

- CriticCat: sent candidate path + sha + exact options/`--` policy (quoted operands decode to one
  token; lone `-` = stdin input; conservative option refusal).
- ReviewCat: sent path + sha + named conservative refusals for their independent matrix.
- ExecCatProbes: sent path + sha as their candidate×candidate / candidate×base trigger, incl. note
  that a two-existing-operands probe failing candidate-mode is the designed verdict.

## Scope, tooling, hygiene

- Wrote only: `.ufo/waves/round-66/w1/ExecCatGate/figure-audit.py`,
  `.ufo/waves/round-66/w1/ExecCatGate/receipts/*.txt` (7 files), this report.
- No tool installs (git/python3/coreutils only); all pacman transactions untouched.
- One shared clone at `/fast/scratch/hyaku/kasegi-r66/ExecCatGate/clone`, detached at base,
  toplevel asserted before use; scratch TMPDIR/HYAKU_SCRATCH pointed at
  `/fast/scratch/hyaku/kasegi-r66/ExecCatGate/tmp`; scratch deleted before yield.
- Production, fleet files, siblings, git index/jj: untouched; no commits/pushes.

## Erratum (v1 → v2, doc-only; ReviewCat finding, accepted)

ReviewCat's independent matrix (43/43 predicted behaviors at v1 `d48a5e45…`) held, and flagged two
docstring accuracy defects, both fixed in v2 `51f299af…` with zero code delta:

1. Module docstring said SIGPIPE is benign "ONLY when the killed stage is a cat", contradicting the
   intended (and implemented) rule that non-cat heads keep the old benign rule
   (`upstream_stale` returns False for non-cat SIGPIPE; ReviewCat's own head/cut SIGPIPE controls
   green). v2 wording: benign stays the rule; for a cat head the exemption applies only with at
   most one decoded input; other heads retain the benign rule.
2. The fail-closed parenthetical said "upstream signal other than SIGPIPE", omitting the newly
   stale multi-input/option-carrying cat SIGPIPE. v2 wording: "a non-exempt upstream signal —
   SIGPIPE from a multi-input or option-carrying cat is stale".

v2 re-verified: selftest 67/67 exit 0 (receipt `candidate-selftest-v2-r66.txt`); differential and
real-ledger receipts stand as v1 behavior evidence (no code change between v1 and v2).
Cross-seat corroboration on the v2 bytes `51f299af…`: ExecCatProbes re-ran their 8-probe battery —
candidate×candidate `probes=8 failures=0 rc=0`, candidate×base `probes=8 failures=3 rc=1` on
exactly P1/P2/P8 flipping to stale `derive-upstream-signal-13` (receipts under
`.ufo/waves/round-66/w1/ExecCatProbes/receipts/`); ReviewCat's independent 43/43 matrix held at v1
with identical behavior.

## Limitations / risks

- Conservative refusals (named): any cat option (even single-file `-n`), trailing `--`, `cat - a`.
  Base was green for those shapes on SIGPIPE; candidate is stale. This is the capability
  restriction L1 asked to label, not a regression claim of correctness for every such derive.
- Two-existing-operands refusal is intentional (finite claim): a truncated two-file cat can hide a
  later operand's content divergence; dispatch and L1 confirm conservative refusal.
- `cat_sigpipe_exempt` does not parse option values or bundled short options; it refuses, so it can
  never mis-exempt an option it misunderstands. Risk is over-refusal only.
- Exemption requires `basename(head) == "cat"`; parse validation already forces the bare head
  `cat`, so absolute-path heads cannot occur; the basename check is a safety net for future
  dispatchers.
- Selftest determinism rests on 4 MiB ≫ pipe buffer; an environment with a multi-MiB pipe buffer
  could drop SIGPIPE → reason becomes exit-based → the case fails loudly (fail-closed), never
  silently passes.
- Real-ledger non-regression is evidenced at base bytes only; the lane tip may have moved since
  (working tree shows unrelated untracked round-66 artifacts; no tracked drift at run time).
