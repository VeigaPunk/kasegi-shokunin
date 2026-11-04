# SentinelMultiHead — R67 security review of the multi-head SIGPIPE repair

Seat: `SentinelMultiHead` (sentinel, read-only). Scope: the candidate gate
`.ufo/waves/round-67/w1/ExecMultiHeadGate/figure-audit.py` against production
`corpus/instruments/figure-audit.py`, lane base revision `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`.

- production sha256 `51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac` (30295 B)
- candidate sha256 `d5e8fcae6f1523d0ffbe8f21540fde839a24abbe98958378e54da284eec38c05` (34770 B, mtime 2026-11-04 17:59:20 -0300)
- diff against production: 178 lines (`01-diff-production-candidate.txt`)

**Verdict: FINDINGS** — F1 (Low, pre-existing masking not closed by the rule), F2 (Informational,
test-strength). No widening, no newly admitted head or flag, no new write path, no production
regression.

## 1. What the change actually is (line-by-line diff inventory)

Four hunks touch code; everything else is prose or selftest.

| Hunk | Change | Security surface |
|---|---|---|
| module docstring, exit-code + SIGPIPE paragraphs | prose restated for the new rule | none |
| `EXPECTED_CASES` 67 → 71 | test pin | none |
| new `SIGPIPE_REQUIRED_NONFILE_ARGS = {"grep": 1}` + `sigpipe_input_count(head, argv)` | pure count over already-decoded argv; no I/O, no subprocess, no filesystem access | classification only |
| `upstream_stale` body | cat branch now `head_name == "cat"` → `cat_sigpipe_exempt` (same call); new branch `head_name in READ_ONLY_HEADS` → `sigpipe_input_count(...) > 1`; unknown heads still `return False`; `status > 1` and exit-1 branches untouched | classification only |
| selftest fixture + `run_case` + 4 cases + printer | adds `xlines.txt`; `reason` may be a tuple; observed reasons printed | none |

Unchanged, verified by `inspect.getsource` equality (`02-func-parity.txt`):
`tokenize`, `denied_flag`, `python_head_ok`, `segment_ok`, `parse_derive`, `check_read_only`,
`run_derive`, `audit`, `main`, `cat_sigpipe_exempt`, `eprint`, `_one`.
Constants `READ_ONLY_HEADS` and `DENIED_FLAGS` are byte-identical to production.
New symbols: `SIGPIPE_REQUIRED_NONFILE_ARGS`, `sigpipe_input_count`.

## 2. Does the new rule widen what executes? No.

- Admission is decided entirely by `parse_derive` → `segment_ok`/`denied_flag`/`python_head_ok`,
  all unchanged. An admission parity matrix of 96 derives (every read-only head with 0/1/2
  operands, option values, `--`, `<`, pipelines, `&&`, `sort -o/--output/--compress-program`,
  `git show --output/--textconv/--ext-diff`, `git -c`, `python3` counters with extra args,
  traversal/symlink/absolute python paths, and wrapper heads `sh/sed/awk/env/xargs/tee/cp/mv/...`)
  reports `MATRIX derives=96 diffs=0` (`03-admission-matrix.txt`).
- The new branch is only reached for a stage that was already admitted, only for
  `status == -SIGPIPE`, and it returns a boolean consumed as “stale”. It cannot execute, open
  or admit anything.
- `sigpipe_input_count` performs no I/O; it is a pure loop over `argv[1:]`.

## 3. Can a write-capable head become reachable? No new one.

No head or flag is newly admitted (§2). The pre-existing write/exec paths through
allow-listed heads remain, and are measured rather than assumed:

- `sort --compress-program=PROG` is admitted by **both** base and candidate, and PROG is really
  executed when sort spills: 11.3 MB fixture, `-S 1K`, **68 217** (base) / **68 222** (candidate)
  compressor invocations (`18-sort-compress-program-exec.txt`). Host `sort` is uutils 0.8.0;
  its `--help` documents `--compress-program`.
- `git show --textconv` is admitted by both and really runs a config-declared driver: fixture repo
  with `diff.mydriver.textconv` and `*.txt diff=mydriver`, **1** driver run through each gate
  (`19-git-textconv-exec.txt`). Fixture toplevel was asserted equal to the fixture dir before the
  single `git commit`.

Both are pre-existing capability classes (the module docstring already says “NOT a sandbox …
Git configuration … can still write or execute other programs”), not introduced by this change.

## 4. Can an option-value miscount admit a write path? No.

The count treats every token that does not start with `-` as an operand, and option values are
therefore counted as operands. That direction can only *inflate* the count → stale. Measured on
the candidate (`09-optval-candidate.txt`):

- `grep -e x big.txt missing.txt`, `grep -e x -e y …`, `grep -f pats.txt …`, `grep -E`, `grep -F`,
  `grep -e x -- …` → all `derive-upstream-signal-13` stale (base accepted all).
- `cut -f 1 -d : big.txt missing.txt`, `head -n 5 …`, `tail -c 100 …`, `sort -k 1 …`,
  `sha256sum -b …`, `sha256sum -c …`, `ls -l …`, `wc -l …` → all stale.
- The grep pattern skip (`SIGPIPE_REQUIRED_NONFILE_ARGS["grep"]=1`) does not under-count the
  `-e`/`-f` forms: `grep -e x big.txt missing.txt` counts 3, not 2.
- Admission is untouched, so a miscount can never admit a write path; it can only change
  whether an already-admitted stage is reported stale.

## 5. Is the conservative direction monotone? Yes (measured).

A 52-derive differential sweep runs base and candidate over one fixture and compares verdicts
(`14-monotone-sweep.txt`): `widened=0 narrowed=10 identical=42`, and one `MIXED` case
(`wc -l big.txt missing.txt | head -n 1`) where the base verdict races between accepted and
`upstream-exit-1` while the candidate is always stale — still stale, still no widening.
Structurally this is forced: at base every non-cat SIGPIPE was exempt, so any change to that
branch can only turn exempt → stale; the cat branch is textually identical.

Over-refusal (safe, not a trust defect) exists: `tr a b < big.txt | head -n 1` and
`grep -e x xlines.txt | head -n 1` now go stale because tr’s SET operands and grep’s option
tokens are counted. That is the documented conservative direction.

## 6. Findings

### F1 — Low (pre-existing; the repair does not close it): `--` + option-like operands under-count

`sigpipe_input_count` drops only a *leading* `--`, then excludes every token starting with `-`
(except `-`) as an option — even though after a `--` such a token is an operand. A stage that
names two inputs, the first option-like, is therefore counted as one and keeps the SIGPIPE
exemption.

Measured (`13-residual-dashdash-candidate.txt`, 3 repeats each; native stage statuses via
`/bin/bash` PIPESTATUS):

```
R01-wc   native=[-13, 0]  wc -- -x missing.txt | head -n 1        rc=1 ACCEPTED (not stale) x3
R06-cut  native=[-13, 0]  cut -f1 -- -x missing.txt | head -n 1   rc=1 ACCEPTED (not stale) x3
COUNT table: sigpipe_input_count("wc", ["wc","--","-x","missing.txt"]) = 1
             sigpipe_input_count("cut", ["cut","-f1","--","-x","missing.txt"]) = 1
```

`missing.txt` was never opened and the gate is green: this is exactly the C1 class the change
targets, surviving for this shape. Base accepted the same shapes (`12-residual-dashdash-base.txt`),
so it is **not a widening and not introduced** — but the change’s own stated contract (“SIGPIPE is
exempt only when the decoded argv names at most one input operand”) is not met, so C1’s closure
claim must be scoped to plain multi-operand forms.

Smallest remediation: in `sigpipe_input_count`, once a `--` token is seen (any position), treat
every following token as an operand (after the positional skip of the head’s required non-file
args) instead of filtering `-`-prefixed tokens. That preserves the conservative direction and
makes the count ≥ the true operand count. Optionally add one selftest case for
`wc -- -x missing.txt | head -n 1`.

Cat is not affected: `cat -- -x missing.txt` goes stale (measured, `10/11-dashdash-*.txt`),
because `cat_sigpipe_exempt` keeps the round-66 option-token refusal.

### F2 — Informational: the three new multi-head selftest cases accept the exit faces too

`upstream-cut/wc/grep-multi-missing-stale` accept `signal-13`, `exit-1` and `exit-2`. The exit
faces were already stale at base, so on a host where SIGPIPE loses the race the cases pass
without exercising the new rule. The asserted invariant (verdict = stale) is the right security
property and the receipt now prints the observed reason (all three showed
`derive-upstream-signal-13` in my run, `05-selftest-candidate.txt`), but mutation coverage of the
new branch depends on the face. Not a security defect; note for the mutation seat.

## 7. Residual risk classes the change does NOT cover

| Class | Status | Evidence |
|---|---|---|
| `git show/cat-file/ls-tree` heads: SIGPIPE stays benign for any operand count | pre-existing, deliberately retained (“unknown heads keep the benign rule”) | code; `07-probe-candidate.txt` (`git` not exercised end-to-end for masking, but branch is `return False`) |
| `python/python3` heads: SIGPIPE benign for any argv; counters are arbitrary code | pre-existing, documented | `S28-python-two-args` accepted; `segment_ok` unchanged |
| Descendants/wrappers: `sort --compress-program`, `git --textconv`, git config/attributes | pre-existing | §3, measured 68 217/68 222 and 1 driver run |
| exit-0 partial output (a stage exits 0 having skipped a later operand) | pre-existing, not addressed | only status/signal and whole-value comparison are checked |
| PATH / configuration: `argv[0]` resolved through PATH; `PYTHONPATH` for counters; git config | pre-existing, documented “NOT a sandbox” | docstring; no change |
| Races: status face variance (`wc` -13 vs exit-1 measured), TOCTOU between `python_head_ok` realpath and exec, file swap between validation and run | pre-existing | `06/07` wc face; `python_head_ok` unchanged |
| `--` + option-like operands (F1) | pre-existing masking, **not closed** | §6 F1 |
| Over-refusal of benign single-input stages (`tr`, `grep -e file`) | **introduced behaviour**, safe direction (refuse more) | §5 |

Nothing in the table is introduced as an acceptance widening; the only introduced behaviour is
additional staleness.

## 8. Invariants verified

- r66 frozen receipts reproduce: round-66 `probes.py --mode candidate` on this candidate →
  `PROBES probes=8 failures=0`, P1/P2/P8 `derive-upstream-signal-13`, P3/P4/P7 green,
  P5 `upstream-exit-1`, P6 green (`04-r66-frozen-replay.txt`).
- `cat_sigpipe_exempt` source identical; cat branch called first and unchanged.
- Candidate `--selftest`: `selftest cases=71 failures=0` (`05-selftest-candidate.txt`).
- Production ledger `corpus/instruments/figure-audit-ledger.json`: candidate
  `figures=35 ok=35 stale=0 exit=0`, base identical (`15/16-production-ledger-*.txt`).
  All production derives are single-input grep/wc/sha256sum or `git` heads, so the new rule
  changes no production figure.
- Production gate bytes untouched (`51f299…`); lane `git status --porcelain` shows only the
  untracked `.ufo/waves/round-67/` evidence dir.

## 9. Failed setups and honesty notes

- First attempt to demonstrate `sort --compress-program` used a 4 MiB input with `-S 1K` and the
  compressor was **not** invoked (no marker). Re-run with 11.3 MB and the same `-S 1K` produced
  68 217/68 222 invocations. The first attempt is recorded as a failed setup, not as a capability
  result; the successful receipt is `18-sort-compress-program-exec.txt`.
- First selftest receipt run failed with `FileNotFoundError` because the `HYAKU_SCRATCH` directory
  did not exist; it was created and the receipt regenerated (`05-selftest-candidate.txt` is the
  good run).
- `git` textconv fixture: toplevel asserted equal to the fixture dir before the single commit;
  identity supplied per-command with `-c user.name/-c user.email`.
- Host `sort` is uutils 0.8.0; `head` reports uutils-style errors. Native statuses were measured,
  never assumed; the `wc` race is reported as a distribution, not a single value.
- No tools were installed or upgraded; no pacman transaction was attempted.
- All fixtures were built under `/fast/scratch/hyaku/kasegi-r67/SentinelMultiHead/` (TMPDIR and
  `HYAKU_SCRATCH` passed explicitly) and the tree was deleted before yield; the receipts keep the
  paths they ran with.

## Receipts

`00-identity.txt`, `01-diff-production-candidate.txt`, `02-func-parity.txt`,
`03-admission-matrix.txt`, `04-r66-frozen-replay.txt`, `05-selftest-candidate.txt`,
`06-probe-base.txt`, `07-probe-candidate.txt`, `08-optval-base.txt`,
`09-optval-candidate.txt`, `10-dashdash-base.txt`, `11-dashdash-candidate.txt`,
`12-residual-dashdash-base.txt`, `13-residual-dashdash-candidate.txt`,
`14-monotone-sweep.txt`, `15-production-ledger-candidate.txt`, `16-production-ledger-base.txt`,
`17-count-table.txt`, `18-sort-compress-program-exec.txt`, `19-git-textconv-exec.txt` —
all under `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/SentinelMultiHead/`.
