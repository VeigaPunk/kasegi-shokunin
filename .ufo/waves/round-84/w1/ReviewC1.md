# ReviewC1 — round-84 C1 candidate code review (depth:verifiability)

Freeze commit 7f76b7eb690cd6e75e7f3e7729cedcb15611b34b (base a089ff3d). Inputs verified by
sha256 before review: landed census 343b21e4…, candidate e5f2e4bd…, counter c67e6912…,
builder 4352368e…, stub 3639b9e6…, driver 6e555083…, table daf05bace… (all match claims.json).
Scratch deleted before yield; receipts cited below live in `ReviewC1-receipts/` beside this
report and in the committed `.ufo/waves/round-84/controls/`.

**Verdict: no blocking defect.** The diff is 6 hunks, all additions (docstrings, REQUIRED tuple,
cases 26–31); no behavior-bearing line outside the new cases changed. One LOW binding defect,
three INFO notes.

## Findings (severity-ranked)

**F1 — LOW (claim-binding, stale receipt name).** `.ufo/waves/round-84/claims.json:7` (C1
`controls` prose) names `c1-candidate-r84.raw`; the freeze commit contains
`c1-candidate-r84.txt` (`git ls-tree 7f76b7e .ufo/waves/round-84/controls/` — verified, no
`.raw` exists). No predicate cites the name (P7 binds only the donothing/stub receipts), so no
kill-rule impact, but a verifier following the prose literally hits a missing file. Fix: change
`.raw` → `.txt` in the prose (L1's call; claims.json is frozen).

**F2 — INFO (latent harness fragility, not a defect against this table).**
`recheck-cwd-census.py:784` — `usage_run` catches `Exception`; `SystemExit` is BaseException.
Today this is correct (pristine `main` returns 2 for a trailing flag, never raises), but if a
future candidate switched usage to `sys.exit(2)`, H06/H07 would score DIRTY (crash, no FAIL
line) instead of a clean `argv-values` FAIL, weakening the "killed on its declared check" shape.
Case 29's census SystemExit is caught explicitly, so the current file is safe. One-line
hardening if the L1 wants it: `except (Exception, SystemExit)` at :784.

**F3 — INFO (docstring cosmetics).** `recheck-cwd-census.py:288` — selftest docstring reflow
leaves a dangling article: `main-verbose), the` newline `round-82 two`. Grammar only; content
accurate.

**F4 — INFO (control cost, optional).** `c1-stub-r84.py` runs the full 79-row battery (~110 s)
to show H01–H12 survive the stub. A 12-row H-only table would carry the same falsification
power in ~20 s. Current form is uniform with the candidate/donothing receipts; no change
required.

## Verified-correct, per review axis

**Checks assert what their comments say; each H row dies on its declared check, stated reason.**
Static derivation + committed per-row evidence agree:

| H | mutant | killed by | mechanism verified |
|---|---|---|---|
| H01/H02 | noprefix `>=0` / `!=1` | noprefix-only (case 26) | 1- and 2-entry prefix-less fixtures rc 1; `conform_ok(noprefix∈{1,2}) is False` kills `!=1` at 2 |
| H03/H04 | summary swap / other→norecheck | summary-fields (case 27) | exact `RECHECK-CWD entries=4 … exit1_foreign=2 exit_other=1` line asserted |
| H05 | `noprefix and code != 0` | entry-bare-pass (case 28) | `c-bare-pass.md`/`f-fresh-cwd.md` (prefix-less, exit 0, case-1 fixture) lose ENTRY |
| H06/H07 | guard dropped on --root/--lane | argv-values (case 29) | IndexError caught at :784 → `r[2] is None` fails; pristine returns 2 + usage on stderr |
| H08 | --lane eats --verbose | verbose-order (case 30) | parser order --root/--lane/--verbose (:962-968): `--verbose --root R --lane L` → lane="--root", `R` hits else-usage rc 2 ≠ ret25 |
| H09 | abspath dropped | argv-values (case 29) | census builds the message from its own `root` param (:151); relative value → wrong message |
| H10 | selftest only when last | argv-values (case 29) | `pos29 == [77, 77]` fails both orders |
| H11 | `code != 0` widening | entry-set (case 31) | `_t23` (case-23 default capture) gains ENTRY q-seven |
| H12 | timeout label | entry-set (case 31) | forced `run_foreign → -1` renders `foreign_exit=timeout` ≠ asserted `-1`; `exit_other == 2` exact (p-pass + q-seven, both prefixed) |

Committed receipt: all 12 lines `verdict=KILLED … failed_cases=<declared case>` (`ReviewC1-receipts/verify.txt`).
Live spot battery H09+H12 on a scratch copy: both KILLED on declared cases, baseline ok
(`spot2.out`). Miskill audit: no H row trips a second check (e.g. H05 leaves b-relative/output-lines
intact; H11 leaves main-default/output-lines intact since both pin exit-0 silence, which `code != 0`
preserves). H-row anchor/replacement bytes equal the r83 MutC1Hunt rows exactly; rows 1–67 equal
the r83 table; `build-table.py` re-run reproduces the frozen table byte-identically
(79 rows, neutral=3, new=12, all anchors unique-once).

**State restoration on every path incl. exceptions.** Four stubs, four `finally` blocks:
sys.stderr (:779-787), os.chdir (:792-802), `globals()['selftest']` (:803-812), 
`globals()['run_foreign']` (:829-833). Live selftest over a scratch copy: rc 0,
`selftest cases=33 failures=0`, 33 case lines, gate-checkids `missing=[] extra=[]`.

**Recursion risk in argv-values: closed.** `pos29` calls `main(--selftest …)` from inside a live
selftest; without the :803 stub each nested selftest re-enters case 29 and recurses unboundedly.
The stub is set before both calls and restored in `finally`; the only `--selftest`-honoring path
is behind it. Residual: F2.

**Gate-wiring / gate-checkids interaction.** None of the six new checks is a GATE_PREDICATES id;
no ok-argument is a constant True or BoolOp-with-True (wiring F1/F2/F3 cannot fire on them);
REQUIRED tuple carries all 33 ids and `set(done) == required` is enforced at :938; live run green.

**Docstring accuracy.** `cases=33` printed from `len(done)` (:944) — live-verified. Round-84
paragraph clauses (module docstring :86-95) each match code, including the G-1…G-8 mapping to
H01–H12. Only F3's cosmetic nit.

**Stub control: cheapest honest in kind.** Built from the r83 landed bytes (anchors fail with rc 2
on the integrated candidate — byte-bound), registers the six ids with always-true non-constant
checks, keeps every r83 check intact, and under the r84 counter yields `baseline=ok` (cases=33)
with H01–H12 all SURVIVED, rc 1 — proving the kills come from the check bodies, not from
registration or case count. Donothing covers the "no new checks" class; stub covers the "empty
checks" class. Cost cut possible (F4).

**P3/P7 binding.** The counter's summary line is `MUTBAT target_sha256=… baseline=ok rows=79
killed=76 … decoy=ok decoy_hidden=75/76` (:297-302) — P3's quoted string is a real contiguous
substring (committed `c1-candidate-r84.txt` shows the exact line), and the receipt embeds both
greps returning 76 and 12; the MUTANT line shape `MUTANT <id> verdict=<KILLED|…> rc=…` matches
both regexes. P7: donothing and stub receipts each end `rc=1` and each contain exactly 12
`^MUTANT H(0[1-9]|1[0-2]) verdict=SURVIVED` lines (counts verified). Counter selftest live:
`mutbat selftest ok … r84_limbs={'extra': True, 'dup': True, 'decoy_line': True}` rc 0 —
P4's quoted dict matches the real print format. `apply_row` applies extras after an identity
primary (:268-273), refuses a twice-occurring extra anchor, and the DECOY line is second-to-last
(:295) — M09/M10/M12 in `c1-counter-mutants-r84.py` target exactly those lines, receipt
`as-expected`.

## Residual risk / verification gaps

- P1/P2/P6/P8 are landing-commit predicates; not verifiable at freeze (candidate hash and
  cases=33 verified on the frozen bytes instead). The full 79-row battery was not re-run live by
  this seat (receipts are committed and internally consistent; the 2-row spot battery plus the
  1.5 s selftest calibrated the per-row cost); the L1's P3 run at landing is the binding replay.
- The six new checks pin the *current* output contract; any future intentional output-widening
  (e.g. G-8's alternative) will need a deliberate table edit, by design.
- No tooling installs; python3 stdlib only; pacman pause respected. Scratch
  `/fast/scratch/hyaku/kasegi-r84/ReviewC1` deleted.

## Files written

- `.ufo/waves/round-84/w1/ReviewC1.md` (this report)
- `.ufo/waves/round-84/w1/ReviewC1-receipts/cand-selftest.out` (live candidate selftest, cases=33)
- `.ufo/waves/round-84/w1/ReviewC1-receipts/mutbat-selftest.out` (live r84 counter selftest, r84_limbs)
- `.ufo/waves/round-84/w1/ReviewC1-receipts/spot2.out`, `spot2.json` (live H09+H12 spot battery)
- `.ufo/waves/round-84/w1/ReviewC1-receipts/verify.txt` (table rebuild, H-row verdicts, SURVIVED counts, hashes)
