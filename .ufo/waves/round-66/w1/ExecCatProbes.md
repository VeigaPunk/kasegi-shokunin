# ExecCatProbes — r66 w1 predata counter battery for the cat SIGPIPE false green

Seat: ExecCatProbes (leaf executor; no subagents, no production edits, no git/jj mutations, no commits).
Scope: ONE deliverable — `.ufo/waves/round-66/w1/ExecCatProbes/probes.py` — plus receipts and this report.
Base: `b6db9e818d322726e39cb441f2179d34d4170275`; base instrument blob sha256
`86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef`, extracted via
`git show b6db9e8…:corpus/instruments/figure-audit.py` from my single scratch clone. The lane
worktree instrument is byte-identical to that blob (no drift), matching CriticC1's r65 anchor.
Lane HEAD at measurement time: `1957407e22331c73aafe944da2b37c182f13583a`.
No admission authority: findings only; freeze/integration belongs to L1 KasegiR66.

## Deliverable

`probes.py` sha256 `d788bbc16cd1ac9f345e5fc1a29f3e87542ceed1f2dfcdfa5e4b7593d3a57312` (final, post
opaque-path hardening; superseded intermediates are preserved: `1d28ca24…` fixed-ID collector under
`receipts/archive-pre-nonce-hardening-collector-1d28ca24/`, and nonce/ID-hardened `aab657e7…` — whose
`--root`/`--ledger` paths still carried stable labels — under `receipts/archive-collector-aab657e7-pre-opaque-paths/`;
both archives' READMEs name base revision `b6db9e818d322726e39cb441f2179d34d4170275`).
CLI: `--instrument PATH --work DIR --mode base|candidate`, plus `--selfcheck --instrument REAL --work DIR`.
- Real public gate invocations only: each probe writes a single-figure ledger
  (`{"figures":[{id,record,recorded,derive,want}]}`) and runs
  `python3 <instrument> --ledger one.json --root <fixture root>` exactly as production drives the gate.
- Prefreeze hardening (L1 KasegiR66 directive, closing CriticCat's ID-keyed no-work-oracle finding):
  every run draws a fresh 16-hex nonce (printed as the `NONCE` line with the base revision and instrument
  sha), each ledger figure gets a fresh unguessable `fig-<32hex>` id and a neutral random `rec-<16hex>`
  record carrying no expectation information, and the gate's returned FIG id and recorded field are bound
  WHOLE against the ledger (never a prefix, never the stable P1..P8 seat label). The stable seat labels
  remain only as output presentation; the instrument never sees them. All instrument-visible paths
  (`--ledger`, `--root`, cwd) use fresh opaque per-probe directory names (`c-<24hex>`) and runs use opaque
  work dirs (`w-<12hex>`) — no mode or probe identity is recoverable from argv paths; a grep of the work
  tree for seat labels / mode names returned nothing (`NO-LABEL-LEAK` check). The label->id->record->dir
  mapping lives only in the outer `LEDGER` receipt lines.
- Output: `PROBE <name> rc=<audit exit> expected=<expected exit> reason=<observed reason|-> pass=<true|false>`
  per probe, `NATIVE <name> stage0=… stage1=… out=… err_bytes=…` per probe, `NOTE` lines on any defect,
  then `PROBES probes=N failures=N mode=<mode> instrument_sha256=<sha>`; exit 1 on any failure, 2 on usage/guard error.
- Deterministic fixtures: `big.txt` 4,194,306 bytes starting `alpha\n` (generator-pinned), `other.txt`
  empty in every variant, `missing.txt` never created; P8 adds a real 4 MiB operand literally named `--`.
- Independent native replay: same derive under `/bin/bash` with `${PIPESTATUS[@]}`, children spawned
  `close_fds=True` (no parent pipe fd leaks into the pipeline), bash `128+N` normalised to `-N` to match
  r65 receipt convention; every child under a 120 s timeout, killed and reaped by process group on timeout.
- Scratch guard: refuses `--work` equal to the lane, inside the lane, a proper ancestor of the lane, or `/`.
- Fail-closed binding (post-review fix): the FIG line, the `FIGURE-AUDIT` summary (figures/ok/stale/exit
  tokens) and the process rc must agree; ANY harness note (native mismatch, parser problem, summary/rc
  contradiction, timeout, missing instrument) forces `pass=false` — nothing decorative.

## The eight probes and measured verdicts

| id | derive (public gate grammar) | want | base×base | base×candidate | candidate×candidate |
|---|---|---|---|---|---|
| P1-cat-two-operand-missing-sigpipe | `cat big.txt missing.txt \| head -n 1` | alpha | ok rc0 **(FALSE GREEN)** | red: want stale signal-13, got ok | stale `derive-upstream-signal-13` rc1 |
| P2-cat-two-operand-existing-sigpipe | `cat big.txt other.txt \| head -n 1` | alpha | ok rc0 **(FALSE GREEN)** | red (same) | stale `derive-upstream-signal-13` rc1 (conservative refusal, both operands exist) |
| P3-cat-one-operand-sigpipe | `cat big.txt \| head -n 1` | alpha | ok rc0 | ok rc0 (retained) | ok rc0 (retained) |
| P4-cat-stdin-sigpipe | `cat < big.txt \| head -n 1` | alpha | ok rc0 | ok rc0 (retained) | ok rc0 (retained) |
| P5-cat-missing-exit1 | `cat missing.txt \| wc -l` | 0 | stale `derive-upstream-exit-1` | same (retained) | same (retained) |
| P6-grep-nomatch-green | `grep absent big.txt \| wc -l` | 0 | ok rc0 derived=0 | same | same |
| P7-same-derive-small-twin | `cat big.txt other.txt \| head -n 1` (big.txt = `alpha\n` only, other.txt empty) | alpha | ok rc0, native [0,0] | ok rc0 | ok rc0 |
| P8-cat-dashdash-separator-missing | `cat -- -- missing.txt \| head -n 1` (first `--` separator, second a 4 MiB file named `--`) | alpha | ok rc0 **(FALSE GREEN)** | red: want stale signal-13, got ok | stale `derive-upstream-signal-13` rc1 |

Masking signature, receipt-level: for P1/P2/P8 the native replay shows `stage0=-13 err_bytes=0`
(cat dies of SIGPIPE mid-first-operand and NEVER reaches the later operand — zero diagnostics), while
non-SIGPIPE P5 shows `stage0=1 err_bytes=44` (cat's missing-file diagnostic present). Same missing file,
two consumers: stale through `wc` (P5), green through `head` at base (P1). That is exactly r65 CriticC1 H1,
now pinned against base blob `86becbde…`.

## Measured run matrix (final collector `d788bbc1…`; all receipts under `.ufo/waves/round-66/w1/ExecCatProbes/receipts/`)

| run | instrument (sha256) | mode | result | rc | run nonce | receipt |
|---|---|---|---|---|---|---|
| base battery | base blob `86becbde…` | base | probes=8 failures=0 | 0 | a99da59290131254 | `base-mode.txt` (`c3ea866d…`) |
| base candidate-mode red | base blob `86becbde…` | candidate | probes=8 failures=3 (P1,P2,P8) | 1 | 9140b4e2c99f79e0 | `base-candidate-mode.txt` (`d87599b8…`) |
| candidate battery | candidate `51f299af…` | candidate | probes=8 failures=0 | 0 | c74f8cec9b61c472 | `candidate-mode.txt` (`ee96c42a…`) |
| candidate behavior flip | candidate `51f299af…` | base | probes=8 failures=3 (P1,P2,P8 now stale signal-13) | 1 | c63110a04e7b4cb0 | `candidate-base-mode.txt` (`f4bb71d5…`) |
| selfcheck | base blob (positives) | meta | cases=4 failures=0 pass | 0 | (4 sub-runs, see receipt) | `selfcheck.txt` (`8e472dae…`) |

All five verdicts are identical across every collector generation (fixed-ID `1d28ca24…`, nonce/ID
`aab657e7…`, opaque-path `d788bbc1…`): same failures, same reasons, same rc — hardening changed only
figure identity and path opacity, never outcomes.

Candidate identity: `.ufo/waves/round-66/w1/ExecCatGate/figure-audit.py` sha256
`51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac` (585 lines) — independently recomputed by me
and equal to ExecCatGate's claim; this file supersedes the earlier `d48a5e45…` bytes by a doc-only erratum.
I measured BOTH: `d48a5e45…` gave candidate×candidate 8/0 rc0 and candidate×base 8/3 rc1 (P1/P2/P8), and the
`51f299af…` rerun reproduced both results identically, so the erratum is behavior-neutral on this battery, as
claimed. Diff of the `51f299af…` bytes vs base blob is 102 lines (`candidate-diff-vs-base.txt`, `72cbbefb…`).

## Fail-closed proofs (`selfcheck.txt`)

- `missing-instrument`: nonexistent instrument path → failures=8, battery rc 1 (spawn failure becomes probe failure, no crash).
- `wrong-expectation-stub`: always-stale exit-1 stub × candidate mode → failures=7 rc 1; P5 (which wants `derive-upstream-exit-1`) is correctly NOT fooled — reasons are bound, not just rc.
- `always-green-counterfeit`: always-ok stub × candidate mode → failures=4 (exactly P1,P2,P5,P8) rc 1; the counterfeit passes P3/P4/P6/P7 in candidate mode, which is why candidate-mode expectations must stay stale on P1/P2/P8.
- `positives-retained`: real base blob × base mode → failures=0 rc 0.

## P7 rationale (runtime-keyed discriminator)

P7's derive string is byte-identical to P2's; only `big.txt` differs (6 bytes vs 4 MiB) and `other.txt` is
empty in every variant (CriticCat's timing-proof design: single ≤PIPE_BUF write, no second tiny write can
race head's exit). Native [0,0] → no SIGPIPE arises → ok in BOTH modes. A text-keyed oracle that refuses
multi-operand cat unconditionally reads P7 red; CriticCat measured exactly that (their text-arity oracle:
8 probes, failures=1, exclusively P7). The intended candidate predicate keys on the runtime status
`status == -SIGPIPE` plus decoded argv, and my candidate receipt shows it reads P7 green.

## Boundaries and limitations (stated, not hidden)

- Hardened stance on forgeries: with fresh unguessable figure ids, whole-id/recorded binding, neutral
  random records and fully opaque instrument-visible paths, an ID-keyed or path-sniffing no-work oracle
  no longer passes (it can recover neither probe identity, mode, nor expected verdict from anything the
  instrument receives). The
  residual floor is a ledger-reading liar that prints `derived=<want> ok` for every figure — that is the
  always-green counterfeit, caught in candidate mode by the stale expectations on P1/P2/P5/P8. No
  collector can catch a liar on ok-expected probes without executing the derive; that closure belongs to
  the driver's revision-pinned bytes and gate sha pin (CriticCat concurs; matches r65 D2/Q3.1).
  CriticCat's pre-hardening ID-oracle 8/0 receipt against collector `1d28ca24…` is preserved as M66
  evidence in the archive.
- Scope is the finite C1 cat-SIGPIPE claim. Not sandbox coverage, not pipefail, not general error
  detection; exit-0 wrappers, signal-catching producers, grandchildren and non-cat heads are out of scope
  (r65 residuals stand).
- Single-figure ledgers only; multi-figure `&&` concatenation is covered by the instrument's own 63-case
  selftest pin, which ExecCatGate reports as 67/67 on the candidate (their receipt, not re-measured by me).

## Coordination

- CriticCat: H1 carry-in framing; proposed the P7 same-derive twin, the P8 `-- --` separator key, the
  empty-`other.txt` timing-proof hardening, and the load-bearing-notes + 141-normalisation fixes — all adopted.
- ExecCatGate: one-shot candidate trigger (path + sha256) answered on request; no polling loop used.

## Tooling

No installs; no pacman transactions; no new channels. `python3` 3.14.8 (system), `git` (system) used
read-only for blob extraction with explicit `-C <scratch clone>`; clone toplevel asserted
(`/fast/scratch/hyaku/kasegi-r66/ExecCatProbes/lane-clone`) before any use. Details in `receipts/tooling.txt`,
`receipts/environment.txt`; fixture/input hashes in `receipts/fixture-hashes.txt`; per-case raw gate stdout
preserved under `receipts/gate-stdout/` (32 files).

## Scratch

`/fast/scratch/hyaku/kasegi-r66/ExecCatProbes/` (clone + work dirs) deleted after receipt extraction, before yield.
