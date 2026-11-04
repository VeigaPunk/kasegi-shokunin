# ReviewMultiHead R67 C1 independent review (re-review of final candidate)

Reviewed FINAL candidate `.ufo/waves/round-67/w1/ExecMultiHeadGate/figure-audit.py`
at sha256 `8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247`
against true base bytes `git show HEAD:corpus/instruments/figure-audit.py`
(sha256 `51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac`,
preserved at `base-51f299.py`). This supersedes my earlier receipt against the
intermediate build `d5e8fcae6f1523d0ffbe8f21540fde839a24abbe98958378e54da284eec38c05`
(kept in `final/` for provenance). State note: production already landed the same
bytes — `diff -q corpus/instruments/figure-audit.py <candidate>` is IDENTICAL —
and `ExecMultiHeadGate.md` records the `--` split fix (S3/S4) plus my residuals.

Verdict: **accept the production-path repair**, now including the end-of-options
dash-file hole fix. Residuals: input-list indirection (medium), and conservative
over-refusals incl. a new grep post-separator one (low). Recommendation only;
L1 remains the production integrator.

Method note: `xd://lsp` is not mounted, so caller/definition checks were AST-based
and behavior was proven by executing the real gates on real pipelines under
`strace`. No sandbox/emulator/shell-correctness claims; all binaries resolved
under `/usr/bin` and hashed in `final/binary-identities.json` (GNU coreutils
9.12, grep 3.12-modified). All first data operands > 4 MiB
(`final2/fixtures.json`); `review2.py` under scratch reproduced the run and was
deleted with the tree (the durable copy is `review.py`).

## Expected matrix (derived from the code)

For an upstream SIGPIPE, cat keeps `cat_sigpipe_exempt`; every other
`READ_ONLY_HEADS` name goes through `sigpipe_input_count`; unknown heads remain
benign. The count splits argv[1:] at the FIRST `--` anywhere: pre-separator
non-option tokens count (minus grep's skipped first token), and EVERY token
after the separator counts (dash-named files are real operands). Exempt = `<= 1`.

| head | 0 operands | 1 operand | 2+ operands | conservative refusal |
|---|---|---|---|---|
| cat | exempt (r66 stdin) | exempt (one operand, no options) | stale | any option token: `cat -n big.txt` |
| cut | exempt | exempt (`cut -f1 -d: big.txt`, `cut -f1 -d: -- big.txt`) | stale | detached values: `cut -d : -f 1 big.txt` counts 4 |
| wc | exempt | exempt | stale | `wc --files0-from` not counted (residual) |
| grep | exempt (pattern only) | exempt (`grep x f`) | stale | `grep -e x f`; NEW: pattern after `--` also counts (see below) |
| sort | exempt | exempt | stale | detached values: `sort -k 1 big.txt` counts 2 |
| head | exempt (stdin; `head -c 10000000 < f` counts 1) | exempt | stale | `head -c 10000000 big.txt` counts 2 |
| tail | exempt (stdin; `tail -c 100000 < f` counts 1) | exempt | stale | `tail -c 100000 big.txt` counts 2 |
| sha256sum | exempt | exempt | stale | `sha256sum -c biglist` counts only list operand (residual) |
| tr | 0 args invalid | exempt (`tr -d y`, `tr -d -- y`) | stale | `tr a b` counts both charsets as operands |
| ls | exempt | exempt (`ls -l many`) | stale | none found |

Measured: `final2/summary.txt`, `final2/results.json`, `final2/{base,candidate}/*.stdout`.

## (a) R66 cat behavior — CONFIRMED (final bytes)

`cat_sigpipe_exempt` source-identical (sha256
`4030928c43aafc5a447e5102d1991b1323b1bc64586832788a1349b2e283aa5b` in
`final2/source-comparison.json`), cat branch still calls it first. Exact r66
fixture/shape defs P1-P8 reproduce: P1/P2/P8 stale `derive-upstream-signal-13`,
P3/P4/P7 ok, P5 `derive-upstream-exit-1`, P6 ok (`final2/summary.txt`).

## (b) No new write/admitted head — CONFIRMED

AST/source comparison: `READ_ONLY_HEADS`, `DENIED_FLAGS`, `tokenize`,
`denied_flag`, `python_head_ok`, `segment_ok`, `parse_derive`, `run_derive`,
`audit`, `check_read_only`, `main`, `_one` unchanged; imports unchanged; new
`SIGPIPE_REQUIRED_NONFILE_ARGS`/`sigpipe_input_count` are pure argv counting.
Production ledger: `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`
(`final2/real-ledger.json`). `--selftest`: `cases=73 failures=0`, children
cleaned (`final2/selftest.stdout`, `final2/run.json`).

## (c) Option-value conservatism — CONFIRMED in direction, RESIDUAL remains

Detached option values count as operands → safe stale only (never green):
`cut -d : -f 1 big.txt`, `head -c 10000000 big.txt`, `tail -c 100000 big.txt`,
`sort -k 1 big.txt`, `grep -e x big.txt`, `grep -i x big.txt` all stale despite
untruncated exit 0.

NEW end-of-options fix verified: `cut -f1 -d: big.txt -- -missing.txt`,
`wc -l big.txt -- -missing.txt`, `head -c10000000 big.txt -- -missing.txt`,
`ls -l many -- -missing.txt`, `grep x xlines.txt -- -missing.txt` were GREEN at
base with `-13` and full run failing; final candidate is stale
`derive-upstream-signal-13`. `cut -f1 -d: -- big.txt` (one post-separator
operand) stays exempt; `cut -f1 -d: big.txt -missing.txt` (no `--`) is already
stale via exit-1, and `sort big.txt -- -missing.txt` via exit-2.

Surviving residual (input-list indirection), re-measured on the FINAL bytes
under strace:
- `wc -l --files0-from=list0 | head -n 1` → 0 counted operands → GREEN:
  `wait4(... SIGPIPE ...)` and zero `openat(... "missing.txt" ...)`;
  untruncated = 1 (`final2/traces/wc_list_indirection-*.trace`).
- `sha256sum -c biglist | head -n 1` → 1 counted operand → GREEN: same
  SIGPIPE/no-open proof; `biglist` 4,740,158 bytes, `check/missing.txt` last.
Same C1 class — green on a world where a named input was never read. It is an
accepted argv-reach boundary per ExecMultiHeadGate.md §"named residuals", and
the docstring's `NOT a sandbox` line covers unscreened flags, but the two
concrete shapes are NOT named in the gate docstring — keep as a named residual
in the landing note.

## (d) Named conservative refusals — MOSTLY CONFIRMED, one NEW unnamed refusal

Named: cat option tokens; option VALUES inflate; post-separator tokens all
count; unknown heads benign. Gaps:
- NEW: `grep -- x big.txt` and `grep -e x -- big.txt` are complete but now
  stale (base green → candidate `derive-upstream-signal-13`): the `--` split
  makes the pattern (after `--`) count. Safe over-refusal consistent with the
  reworded docstring ("skipped ... among the pre-separator tokens"), but this
  specific standard spelling is not explicitly named.
- `tr a b < big.txt` still counts charsets as operands (safe stale); `tr -d -- y`
  stays exempt.
- `grep -e x big.txt`/`grep -i x big.txt` over-refuse (option-before-pattern);
  docstring now says "pattern is skipped as a required non-file argument among
  the pre-separator tokens" — accurate now.
- The two list-indirection masks above are not named in `upstream_stale`/module
  prose.

## Findings by severity

- Medium: surviving input-list masks (wc `--files0-from`, sha256sum `-c`),
  re-measured green on the FINAL bytes with SIGPIPE and missing input never
  opened; pre-existing at base, narrowed not closed; needs naming in landing
  notes or a refusal rule.
- Low (new): grep post-separator pattern counted (`grep -- x f`,
  `grep -e x -- f`) → conservative stale; standard spelling, should be named.
- Low: `tr a b < big.txt` refused though complete (charset operands counted).
- Low: `upstream_stale` says "names at most one input operand"; code counts
  operands, not actual inputs (same residual wording).
- Info: `grep_c1`, `wc1`, `sha0`, `sha1`, `wc0`, `tr0`, `sha_check_attached`
  exercise the non-SIGPIPE path; their operand-count rows are code-derived only.
- Info: wc multi native status is face-variable (`final2/native-repeats.json`:
  -13 and 1); the candidate's any-of-three-reasons selftest is honest.
- Info: `sort --compress-program` exec is a pre-existing gate allowance,
  unchanged by this candidate.
- Info: production tree is dirty (uncommitted integration) — `corpus/README.md`,
  `SOURCES.md`, `knowledge-expected.txt`, and the gate itself are ` M`.

Receipts: `final2/` = true-base vs final-candidate run (62+11 cases); `final/`
= superseded d5e8fcae receipt; `trace-review2.py` under scratch generated the
strace proofs then was deleted (the durable trace outputs are under
`final2/traces/`).
