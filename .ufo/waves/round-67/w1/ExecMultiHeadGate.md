# ExecMultiHeadGate — round-67 w1 seat report (C1 candidate gate repair)

Seat: ExecMultiHeadGate (leaf; no spawns, no delegations, no peer-owned files touched).
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin at base 8e2a8fe8eb92d7c824902a4b70aab027a9aacee0.
Production under test: /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py
(sha256 at copy time 51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac — matches the
declared base hash; production was never modified).

## Deliverable (final, after L1 face-matrix AND end-of-options rulings)

Candidate gate: /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ExecMultiHeadGate/figure-audit.py
Candidate sha256: `8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247`
Base→candidate diff (213 lines): .ufo/waves/round-67/w1/ExecMultiHeadGate/candidate-vs-production.diff

Superseded builds — do not integrate:
- `978c98a2c35dbd16ad66475bdd966f9ed73d17b4c642ae8210287a7345fa3a36` (frozen-reason multi cases;
  superseded by the face-matrix ruling).
- `d5e8fcae6f1523d0ffbe8f21540fde839a24abbe98958378e54da284eec38c05` (superseded by the
  end-of-options ruling: its count only honoured a LEADING `--`, so critic shapes S3/S4 —
  `cut -f1 -d: big.txt -- -missing.txt | head -n 1`, `grep x xlines.txt -- -missing.txt | head -n 1`
  — measured native stage0 −13 with "-missing.txt" never opened and the gate read ok).

## Repair (minimal, production-shape)

1. `SIGPIPE_REQUIRED_NONFILE_ARGS = {"grep": 1}` + `sigpipe_input_count(head, argv)`: conservative
   input-operand count. The decoded argv is split at the FIRST `--` anywhere in argv[1:] (a leading
   `--` is the same first split): pre-separator tokens are options when they start with `-` (a lone
   `-` counts as a stdin input) and the head's required non-file args (grep's positional pattern) are
   skipped among them; post-separator tokens are ALL operands whatever they start with, because
   end-of-options makes dash-named files real operands. Pre-separator option VALUES inflate the count
   — safe stale only, never a false exemption (documented in the helper docstring).
2. `upstream_stale`: for SIGPIPE (−13) the round-66 `cat_sigpipe_exempt` is still called FIRST for
   cat and is byte-identical (function untouched); every other READ_ONLY head is exempt only when
   `sigpipe_input_count(...) <= 1`; unknown heads (git, python, …) keep the old benign rule.
   Statuses >1 and exit-1-from-non-grep paths unchanged.
3. `run_case`: any-of reason tuples (single-string behavior identical for the 67 pre-existing
   cases) + the gate's observed refusal reason(s) are extracted and printed on each selftest case
   line (`reasons=…`) so the exercised native face is visible in every receipt; the fixture asserts
   `-missing.txt` does not exist.
4. Selftest fixtures: `xlines.txt` (`"x\n" * 200000`, control P11's fixture) in the `big=True`
   block; big.txt byte-identical to the control fixture (4193286 bytes,
   sha256 3ed4e02bd97495bce0703d0f0def4174cc5458ce14875807646c14709709766c — re-measured this seat).
5. `EXPECTED_CASES = 73` with pin comment: `R67: +4 multi-head SIGPIPE input count; +2
   end-of-options dash-file`.

Module docstring updated to describe the first-`--` split rule; the L1 control's measured P9/P10/P11
shapes and the critic S3/S4 shapes are the docstring's named false greens.

## Counted cases (+6)

| case | derive | assertion |
|---|---|---|
| upstream-cut-multi-missing-stale | `cut -f1 -d: big.txt missing.txt \| head -n 1` | exit 1, reason in {`derive-upstream-signal-13`, `derive-upstream-exit-1`, `derive-upstream-exit-2`} |
| upstream-wc-multi-missing-stale | `wc -l big.txt missing.txt \| head -n 1` | same any-of reason set |
| upstream-grep-multi-missing-stale | `grep x xlines.txt missing.txt \| head -n 1` | same any-of reason set |
| upstream-grep-single-pattern-file-sigpipe-benign | `grep x big.txt \| head -n 1` | exact green: exit 0, derived `"x"*1023` — pattern is not an input |
| upstream-cut-dashfile-after-separator-stale | `cut -f1 -d: big.txt -- -missing.txt \| head -n 1` | exit 1, same any-of reason set; fixture asserts `-missing.txt` absent |
| upstream-grep-dashfile-after-separator-stale | `grep x xlines.txt -- -missing.txt \| head -n 1` | same |

No frozen reason anywhere (face-matrix ruling); observed reasons are printed per case line so every
receipt shows which native face fired.

## Measured selftest results (final candidate bytes)

- Candidate: `HYAKU_SCRATCH=<scratch> python3 -B <candidate> --selftest` →
  **cases=73 failures=0, exit 0.** Output: .ufo/waves/round-67/w1/ExecMultiHeadGate/selftest-candidate-r67.out
  Observed faces this run: all five stale-multi/dash-file cases `reasons=derive-upstream-signal-13`
  (the −13 face — the one the new rule refuses), grep-single green. All 67 pre-existing cases pass
  unchanged — the round-66 frozen-receipt reproduction.
- Falsification pass: identical copy with ONLY `upstream_stale` reverted to the base head-blind rule
  (scratch graft, not delivered) → **cases=73 failures=5, exit 1.**
  Output: .ufo/waves/round-67/w1/ExecMultiHeadGate/selftest-base-graft-r67.out
  At base: cut-multi FAIL (−13 face green — the C1 false green), wc-multi FAIL (−13 face),
  grep-multi FAIL (benign-−13 empty-derivation face: rc=1 via want-mismatch, no reason line),
  BOTH dash-file cases FAIL at base (cut-dashfile exit=0 green on the −13 face — the S3/S4 hole
  reproduced; grep-dashfile rc=1 without a reason line, same benign-−13 shape), grep-single passes
  (base-compatible).

## Native stage-0 measurements (Popen chain, no shell; 5 repeats; receipt)

.ufo/waves/round-67/w1/ExecMultiHeadGate/native-stage0-repeats-r67.txt (regenerated against the
final candidate sha)

| shape | stage0 ×5 |
|---|---|
| S3 cut -f1 -d: big.txt -- -missing.txt | −13 ×5 (the end-of-options masking face) |
| S4 grep x xlines.txt -- -missing.txt | −13 ×5 |
| differential: cut -f1 -d: big.txt -missing.txt (NO --) | 1 ×5 — cut treats the bare dash token as an unknown option, proving the `--` form is what names the operand (L1's differential, confirmed here) |
| P9 cut -f1 -d: big.txt missing.txt | −13 ×5 |
| P10 wc -l big.txt missing.txt | 1 ×5 this pass (flaky; L1 saw both faces) |
| P11 grep x xlines.txt missing.txt | −13 ×5 (face matrix: −13 and 2 faces) |
| grep x big.txt (single) | −13 ×5 (exempt → green — counted exact-green case is live) |
| wc -l big.txt (single) | 0 ×5 (plain green) |
| sha256sum big.txt (single) | 0 ×5 (plain green) |

Measurement-method caveat (honesty): a bare `bash -c 'eval "PROBE \| head -n 1 >/dev/null"; echo
${PIPESTATUS[0]}'` loop reported 0 for the multi probes and P12 cut-single on this host,
contradicting the L1 control, the Popen-chain replica and the gate's own FIG reasons. That loop is a
bash+eval+redirect measurement artifact and is used as evidence nowhere.

## Residual coverage measured but NOT in the counted suite

- Single-input green: wc/sha256sum exit 0 (plain green), cut/grep/sort SIGPIPE −13 and are exempt
  (count ≤ 1) — verified green through the candidate gate in the mini-ledger receipt
  (.ufo/waves/round-67/w1/ExecMultiHeadGate/mini-ledger-candidate-vs-base-r67.txt, regenerated
  against the final bytes: R-cutone, R-wcone, R-shaone, R-sortone, R-grepone all `ok`).
- Multi-input status path (c): head `head -n 5 big.txt missing.txt` → stale
  `derive-upstream-exit-1` (control P15, L1 receipt); tail `tail -n 1 big.txt missing.txt | wc -l`
  → stale `derive-upstream-exit-1`; sort `sort big.txt missing.txt | wc -l` → stale
  `derive-upstream-exit-2` — identical verdicts on base graft and candidate (mini-ledger receipt
  R-headmulti/R-tailmulti/R-sortmulti). The repair changes nothing on their status path.
- Suggested counted-case shapes if L1 extends the suite later: the mini-ledger derives above, with
  wants `alpha` / `4096 big.txt` / `3ed4e02b…  big.txt` / `alpha` / `"x"*1023`.

## Behavior risks / named residuals

- Review residuals (ReviewMultiHead): re-review of the FINAL sha 8147350c returned verdict
  ACCEPT (end-of-options dash-file fix verified for cut/wc/head/ls/grep; cat identity confirmed;
  P1-P8 reproduce; 73 real-pipeline cases + strace receipts). Residual findings recorded by them,
  none candidate-changing: (i) input-list indirection (`wc -l --files0-from=list0`,
  `sha256sum -c biglist`) hides later inputs beyond argv reach — accepted documented boundary
  (capability count, gate not general error detection); (ii) conservative over-refusals: `tr a b <
  big.txt` counts the charsets → safe stale despite stdin-only input; `grep -e x big.txt` and
  post-separator spellings (`grep -- x f`) count the pattern as an operand → safe stale
  (bare-pattern `grep x big.txt` is the exact-green covered spelling); (iii) docstring wording
  nuances ("input operand" vs counted operand) — documentation-only, L1's call at landing.
  Their state note: production figure-audit.py is byte-identical to this candidate (integrated,
  uncommitted) — landing is L1's act, observed here only via their receipt.
- Mutation-battery cross-reference: MutationMultiHead pinned the superseded d5e8fcae build (7/7
  limbs killed, 3 equivalents held, 0 invalid) and asked to be re-notified on any change — done;
  their battery needs a re-pin against 8147350c. Their findings on d5e8fcae remain recorded: three
  mutations (wc base-count 0→1, `--`-drop removal, option-token counting) survived the 71-case
  suite then — the `--`-drop mutation is now killed by the two counted dash-file cases; the other
  two remain covered by their battery only, as named residuals under the pin.
- Option-value inflation is conservative by design: e.g. a SIGPIPE'd `head -n 1 big.txt` counts `1`
  as an operand → 2 → safe stale; `tr -d 'x' file` counts `x` → safe stale. Never a false green.
- Unknown heads (git, python3, …) keep the benign rule unchanged (named residual per payload).
- The gate remains NOT a sandbox and not pipefail; this repair only tightens the SIGPIPE exemption.
- uutils-host observation, out of repair scope: through `| head -n 1` (early close) uutils tail/sort
  report an unreadable operand yet exit 0; through a full reader (`wc -l`) they exit 1/2. Measured,
  reported, not acted on (gate is documented as not general error detection).

## Checks for the parent/integrator

- Verify sha256 of the candidate equals `8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247`.
- Re-run `python3 -B .ufo/waves/round-67/w1/ExecMultiHeadGate/figure-audit.py --selftest` with
  HYAKU_SCRATCH set to scratch; expect cases=73 failures=0 exit 0; the five stale-multi/dash-file
  case lines print whichever face fired and pass under any of the three refusal reasons.
- Production landing, EXPECTED_CASES production bump and ledger/SOURCES integration are L1's.

## Seat hygiene

- Writes confined to .ufo/waves/round-67/w1/ExecMultiHeadGate/ (candidate + 5 receipts) and this
  report file. Scratch /fast/scratch/hyaku/kasegi-r67/ExecMultiHeadGate/ deleted before yielding
  (verified absent after every round). No production, ledger, SOURCES, knowledge, fleet,
  sibling-lane or git/index writes. No commits/stashes/checkouts. No task calls, no spawns.
- Tooling authorization (operator 2026-10-19): read; **no tools installed or updated** — none needed.
- Failed setups: none. Every claim above is backed by a receipt file or a quoted measured value;
  unmeasured expectations (e.g. GNU-host behavior) are not claimed.
