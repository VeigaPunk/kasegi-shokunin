# ExecMultiHeadProbes — kasegi round-67 w1 (depth:verifiability, coverage)

Seat: ExecMultiHeadProbes (leaf executor). Date: 2026-11-04. Lane: kasegi-shokunin at base 8e2a8fe8eb92d7c824902a4b70aab027a9aacee0.
Instrument under test: /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py — measured sha256 `51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac` (== production base pin, printed as `INSTRUMENT-IDENTITY production-base-gate` in both receipts).

## Deliverables (this directory, except the report trailer)

- `probes.py` — harness, CLI `--instrument PATH --work DIR --mode base|candidate`. Final sha256 `d56a1437cdd1463d99e5f7f9c15877d855c836bad8236efd0cef0afc370ae34a` (revision 3: 20-probe set + CUTDASH control + shared `probe_table`; ExecMultiHeadDriver re-pins this digest). Drives the REAL gate (no reimplementation): one committed-shape single-figure JSON ledger per probe (`{"figures":[{id,record,recorded,derive,want}]}`), gate invoked as `python3 -B <instrument> --ledger <work>/ledgers/<P>.json --root <work>` with `TMPDIR=<work>/tmp` set explicitly for the child.
- `probe_table(root, mode="candidate")` inside probes.py returns `[(id, derive, ("ok", want) | ("stale", reason)), …]` for multihead-mutbat.py's load_collector (smoke-tested: candidate = 11 ok / 9 stale rows; conditional rows P10/P19/P20 are emitted at their primary face and documented as reason-any-of, never exact).
- `probes-output-base.txt` — base mode vs production gate. `PROBES probes=20 failures=0 mode=base`, exit 0.
- `probes-output-candidate-vs-base.txt` — candidate mode vs production base gate (the falsification delta; no candidate gate existed at run time). `PROBES probes=20 failures=5 mode=candidate`, exit 1.
- `probes-exit-codes.txt` — `base_rc=0`, `candidate_vs_base_rc=1`.

Fixtures are byte-pinned in `probes.py` and verified on every run: big.txt `3ed4e02b…66c` (4193286 B — identical digest to L1's control receipt), other.txt `0c5c9015…28e` (4193285 B), xlines.txt `83d10921…749` (400000 B); `missing.txt` and `-missing.txt` (P19/P20 operand) asserted absent. Scratch was /fast/scratch/hyaku/kasegi-r67/ExecMultiHeadProbes (explicit TMPDIR, deleted after receipts were durable; scratch-left-behind would be reported here as a defect — it is not).

## Results

Per-probe output grammar (bound by ExecMultiHeadDriver): `NATIVE <name> stage0=<n> stage1=<n|->`, `PROBE <name> rc=<n> expected=<rc|-> reason=<reason|-> pass=<true|false>`, exactly one `PROBES probes=20 failures=F mode=… instrument_sha256=…`. Native stage statuses are measured by a subprocess Popen chain, never a shell.

Native stage-0/1 returncodes measured this pass (both modes agreed on every probe):

| probe | pipeline | native | base gate | candidate expectation |
|---|---|---|---|---|
| P1 | `cat big.txt missing.txt \| head -n 1` | -13, 0 | rc1 derive-upstream-signal-13 | rc1 derive-upstream-signal-13 (unchanged, r66) |
| P2 | `cat big.txt other.txt \| head -n 1` | -13, 0 | rc1 derive-upstream-signal-13 | rc1 derive-upstream-signal-13 |
| P3 | `cat big.txt \| head -n 1` | -13, 0 | rc0 | rc0 |
| P4 | `cat < big.txt \| head -n 1` | -13, 0 | rc0 | rc0 |
| P5 | `cat missing.txt` | 1 | rc1 derive-exit-1 | rc1 derive-exit-1 |
| P6 | `head -n 5 big.txt \| head -n 1` | 0, 0 | rc0 | rc0 |
| P7 | `wc -l < big.txt \| head -n 1` | 0, 0 | rc0 | rc0 |
| P8 | `grep -c alpha big.txt \| head -n 1` | 0, 0 | rc0 | rc0 |
| P9 | `cut -f1 -d: big.txt missing.txt \| head -n 1` | -13, 0 | **rc0 — masked green** | rc1 derive-upstream-signal-13 (frozen repair) |
| P10 | `wc -l big.txt missing.txt \| head -n 1` | {1,-13} flaky | flaky green/stale | rc1 stale, reason unfrozen, under both outcomes |
| P11 | `grep x xlines.txt missing.txt \| head -n 1` | -13, 0 | **rc0 — masked green** | rc1 derive-upstream-signal-13 (frozen repair) |
| P12 | `cut -f1 -d: big.txt \| head -n 1` | -13, 0 | rc0 | rc0 (≤1 input exempt) |
| P13 | `wc -l big.txt \| head -n 1` | 0, 0 | rc0 | rc0 |
| P14 | `sha256sum big.txt \| head -n 1` | 0, 0 | rc0 | rc0 |
| P15 | `head -n 5 big.txt missing.txt \| head -n 1` | 1, 0 | rc1 derive-upstream-exit-1 | rc1 derive-upstream-exit-1 |
| P16 | `sort big.txt \| head -n 1` | -13, 0 | rc0 | rc0 (≤1 input exempt) |
| P17 | `ls big.txt \| head -n 1` | 0, 0 | rc0 | rc0 |
| P18 | `grep x big.txt \| head -n 1` (positive control, never a repair) | -13, 0 | rc0 | rc0 |
| P19 | `cut -f1 -d: big.txt -- -missing.txt \| head -n 1` | -13, 0 | **rc0 — masked green** | rc1, reason any of {signal-13, exit-1, exit-2} |
| P20 | `grep x xlines.txt -- -missing.txt \| head -n 1` | -13, 0 | **rc0 — masked green** | rc1, reason any of {signal-13, exit-1, exit-2} |
| CONTROL | `cut -f1 -d: big.txt -missing.txt \| head -n 1` (no `--`; not counted in probes=) | stage0 1 | rc1 derive-upstream-exit-1 | same control expectation in both modes |

- **Base run: probes=20 failures=0, exit 0, CUTDASH control pass.** Production base conforms to the derived matrix on every shape, including r66's cat carve-out (P1–P4) and the exit-status paths (P5, P15).
- **Candidate-vs-base run: probes=20 failures=5, exit 1 — failures exactly P9, P10, P11, P19, P20.** The base gate reports `FIG … ok` for multi-input `cut` and `grep` pipelines whose stage 0 died of SIGPIPE (native -13) before reaching the second named operand (both process operands in order; `missing.txt` / `-missing.txt` was never opened). P19/P20 are the mid-argv `--` shapes (CriticMultiHead finding 1, L1-confirmed): the dash-token after `--` is a file operand, so the same masking class survives there. P13/P14/P17 (no SIGPIPE), P12/P16/P18 (single-input SIGPIPE, benign by design) stay green in both modes — a candidate that passes this battery must discriminate on input-operand count, not head name, and must count post-`--` tokens as operands.
- **CUTDASH differential control passes both modes**: without the `--`, cut rejects `-missing.txt` as an unknown option (native stage0 exit 1) and the gate refuses the derive (`derive-upstream-exit-1`) — proving the token in P19 is a file operand only because of the separator. The control sits outside `probes=`; its failure would fail the run exit code without inflating the probe counts.

## P10 flake evidence (dispatch-addendum-r67.md protocol)

The gate's internal wc status and my independent native measurement are separate runs; the race is per-run. Final receipts (5 repeats per mode):

- base run: stage0 {-13,-13,-13,-13,-13}; gate {green, rc1/derive-upstream-exit-1, green, green, rc1/derive-upstream-exit-1} → PROBE P10 pass (base accepts green or stale-in-set).
- candidate-vs-base run: stage0 {-13,-13,-13,-13,-13}; gate {green, green, green, green, rc1/derive-upstream-exit-1} → PROBE P10 fail: 4 of 5 repeats green where the candidate rule requires stale under both outcomes. The un-repaired base gate is what fails here; this is the intended falsification outcome.

## Frozen expectation provenance and payload deviations (L1-owned, measured)

- `PAYLOAD-DEV base P1,P2 payload=rc0 frozen=rc1/derive-upstream-signal-13` — the production base already contains r66's `cat_sigpipe_exempt` restriction (docstring + selftest `upstream-cat-multi-*-sigpipe-stale`, EXPECTED_CASES=67); the payload's base rc0 text predates it. Confirmed by L1's `controls/base-matrix-r67.txt` and IRC correction.
- `PAYLOAD-DEV candidate P8 payload=rc1/derive-upstream-signal-13 frozen=rc0` — `grep -c alpha big.txt` emits one 2-byte write at EOF; native stage0 [0,0] in every measurement (mine and L1's `native-statuses-r67.txt`); the per-head rule fires only on -13, so no candidate can derive signal-13 for P8. L1 ruled: freeze P8 = rc0 in both modes, do not reshape, and add P18 as the streaming-grep positive control (rc0 both modes, native -13, exercised the exemption — no CONTROL-WEAK note fired).
- P19/P20 (L1, from CriticMultiHead finding 1): repair rows, candidate stale under any of {derive-upstream-signal-13, derive-upstream-exit-1, derive-upstream-exit-2}, never a frozen single reason; native stage0 measured -13 (no hard native premise on these rows — their acceptance is face-conditional, like P10).

## Host-dependent shapes (measured, not assumed)

- `grep -c` never SIGPIPEs on this host (P8 [0,0] everywhere): single write at EOF.
- `wc` with a missing second operand races {1, -13}; the gate-internal status races independently of my native measurement (both orderings observed across runs).
- `head` reports uutils-style errors; only its exit status (1) is asserted (P15), never message text.
- P14's `want` is captured at setup from the host `sha256sum` output format (`<digest>␣␣big.txt`, two-space padding); the digest itself is pinned by fixture bytes (`probe_table` falls back to the pinned digest when fixtures are absent).
- Single-input streaming heads (cut, sort, grep) do SIGPIPE (-13) and are green in both modes by design — that is exactly what P12/P16/P18 pin.

## Harness defect history (honesty)

1. First run froze P13's want as `4096`; single-file `wc -l` prints `4096 big.txt` (visible in L1's own control receipt, missed by me). Fixed; both modes re-run.
2. Revision 2 added P19/P20 + CUTDASH + `probe_table` (L1 instruction, post driver-pin of sha `3f2d38a6…`); receipts regenerated.
3. `probe_table` initially raised KeyError on P10 (no EXPECTED row; special-case sat after the lookup). Caught by the smoke test before any consumer imported it; fixed; both modes re-run with a fresh work dir — the outputs above are produced by revision 3, sha `d56a1437…`.
No other defect. No tooling was installed or upgraded (operator authorization unused). Exit 2 (setup/harness error) is implemented but never occurred: fixture digests matched on every run.

## For L1 (planner/integrator)

Once the candidate gate lands at w1/ExecMultiHeadGate/figure-audit.py, validate with:

```
python3 -B probes.py --instrument <candidate.py> --work <fresh dir> --mode candidate
```

Expected: `PROBES probes=20 failures=0 mode=candidate instrument_sha256=<candidate sha>` exit 0 with CUTDASH pass — including P10 all-5-repeats-stale and P19/P20 stale in the any-of set. Re-running `--mode base` against the candidate should fail P1/P2 (it no longer carries the base exit-code identity); the binding receipt for the candidate is the candidate-mode run.

Limits: no candidate gate existed at run time, so the candidate matrix is validated only as a delta against the production base gate; the P10 "stale under both outcomes" and P19/P20 any-of-reason properties cannot be fully confirmed until that run. No claim is made about sandbox, semantic-emulator, or general shell correctness — the gate's own documented non-sandbox caveats apply unchanged.
