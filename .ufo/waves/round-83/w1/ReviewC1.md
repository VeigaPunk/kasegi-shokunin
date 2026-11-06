# ReviewC1 — r83 C1 candidate bytes review

Seat: reviewer (leaf). Round 83, attempt 1. Scope: the frozen C1 bytes —
`.ufo/waves/round-83/c1/recheck-cwd-census.py` (sha256 `343b21e4…08c9`, matches the claim),
`c1/mutbat.py` (`2f7c49d4…cb7d`), `c1/mutant-table.json` (`5b1d99f5…6f44`, 67 rows = 64
assertion + 1 exception + 3 neutral). Diffed against the r82 bytes
(`81677e9d…e050` / `a7d4db43…55c` / 63 rows). All runs on scratch copies under
`/fast/scratch/hyaku/kasegi-r83/ReviewC1/`; no lane file edited; no git writes; no tools
installed. Python on this host: 3.14.8.

Diff facts: census r82→r83 = module/selftest docstrings, the `cases` tuple (+3 ids), and the
three new case blocks (23 bucket-other, 24 bucket-over, 25 main-verbose). **No production
function changed** — `conform_ok`, `census`, `main`, fixtures are byte-identical to r82.
mutbat r82→r83 = docstring, `validate_rows` extra check, new `comment_lines`/`single_decoy`/
`apply_row`, keyed `run_decoy`, `battery(legacy,nonce)` + DECOY line, F9/F10/F11 forgery
sources + `forgery_hashwl`, r83 selftest section, `--seed`.

## Verdicts per checked item

**(a) The three new checks exercise G1–G4 and kill only via their assertions — PASS.**
The G-rows equal the r82 MutC1Hunt gap mutants exactly: G1=H04 (exit_other sum term →
norecheck), G2=H05 (`==`→`>=`), G3=H10 (`--verbose` → `verbose = False`), G4=H19
(tautological main-default limb) with S07M (`verbose` default True) carried as the row's
`extra` site. Pristine candidate: `selftest cases=27 failures=0`, rc 0
(receipts/pristine-selftest.out). Applying each row via the counter's own `apply_row` to
scratch copies and running `--selftest`:

| row | derived | failed cases | declared |
|---|---|---|---|
| G1 | yes | **bucket-other** FAIL `exit_other=1 main_ret=1` + collateral bucket-over | bucket-other ✓ |
| G2 | yes | **bucket-over** FAIL `over=True` | bucket-over ✓ |
| G3 | yes | **main-verbose** FAIL `verbose_entries=5 default_entries=5` | main-verbose ✓ |
| G4 | yes | **main-verbose** FAIL `verbose_entries=6 default_entries=6` | main-verbose ✓ |

(receipts/gapmut-G{1..4}.out). Since production code is unchanged r82→r83, "cannot pass on
the base bytes" reduces exactly to the table above: each gap mutation makes the new check
fail while the r82 checks stay green. The frozen controls corroborate independently: the r82
bytes under the r83 counter leave G1–G4 SURVIVED (c1-donothing-r83.txt) and so does the
check-name stub (c1-stub-r83.txt) — the assertions, not the ids, do the killing.
main-verbose's strict-more limb is same-fixture sound: `out22` (case 22's default run) and
the verbose run both go over `root1`/`lane1`; the margin is exactly the one prefixed passing
entry (5→6 pristine, 5=5 under G3, 6=6 under G4). gate-checkids covers the three new ids
(pristine run, gate-wiring findings=[]).

**(b) D3 `comment_lines`/`single_decoy` behaviour change — one real hole (Finding 1).**
`single_decoy` inserts `  # mutbat-<nonce>` at the end of the anchor's first line, eligible
only when that line carries no STRING/FSTRING_MIDDLE token and has no trailing backslash.
Probed on toys + the real target (receipts/probe-d3.out, probe-d3b.out): single-line string
line, triple-quote interior, backslash continuation → excluded (eligible=False);
open-bracket line, comment line, CRLF source, f-string head/mid line, multi-line-string
closing line → eligible and **behaviour-preserving** (decoyed selftests rc=0, e.g. real
target with seed deadbeef→G4: cases=27 failures=0). The one behaviour-changing case: a line
ending inside a multiline **f-string expression** (PEP 701, Py≥3.12) is marked eligible and
the comment changes the program (Finding 1). On the frozen candidate this is unreachable
(0 f-strings; all 39 eligible anchors' first lines are plain code). Also note: with no
eligible row at all, `run_decoy` fails → decoy=broken refusal of a clean target (Finding 4).

**(c) Keyed decoys — sound; seed determinism real but immaterial to the frozen predicate.**
The nonce assignment `_mutbat_k = '<nonce>'` is appended after the `if __name__` block: it is
**never executed** before `sys.exit` (probe: `k_in_globals=False`; SystemExit preempts it).
It is observable only by the target reading its own source (`nonce_in_src=True`) — which is
the designed channel: it defeats static decoy-hash whitelists (F10) without giving the target
any cheat lever (mutants carry no nonce; run dirs are constant `mutbat-t-` for mutants and
decoys alike, so path labelling is dead too). `--seed` accepts any 1–64 char lowercase hex
(incl. `0`); D3 choice is `cands[int(nonce,16) % len(cands)]` over table-ordered candidates —
deterministic per (seed, table), verified (seed `0`→K-M1, `deadbeef`→G4 twice, `ff…ff`→N11).
This matters only if a gate pins a seed: the frozen P3/P6 predicates pass **no** `--seed`
(urandom per run), so production decoys stay precomputable-proof (Finding 3 is the standing
recommendation).

**(d) `apply_row` extras vs NOT-DERIVED — fail-closed, one diagnostic gap.** Verified
matrix: extra present once → derived; extra absent (0) → None; extra anchor duplicated by a
prior extra (2) → None; extra matching only the primary's replacement text → derived;
extra matching the primary's now-destroyed original text → None. All refusals are
NOT-DERIVED (counted=no), never a bad mutant. Gap: the NOT-DERIVED line reports only the
**primary** anchor's count — probe battery printed `MUTANT E-MISS … occurrences=1` when the
real failure was the extra's count=0 (Finding 2).

**(e) No r82 limb weakened.** Same target (r82 bytes `81677e9d…`) + same 63-row r82 table +
expect-cases 24, r82 counter vs r83 counter (default legacy=False, keyed+D3): **63/63 MUTANT
lines byte-identical**, identical summary `baseline=ok rows=63 killed=60 survived=0
miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=59/60`, both rc 0;
the r83 output adds only the DECOY line (receipts/e82.out, e83.out). `legacy=True` restores
r82 exactly (row-id dir prefixes, unkeyed D1/D2, no D3); `apply_row` with no `extra` key is
semantically identical to the r82 count/replace, and the mutbat selftest confirms each r83
forgery passes legacy (path/count/hashwl → (True, False) in `r83_forgeries`,
receipts/mutbat-selftest.out). `hidden` still counts `decoy_src[:2]` as in r82.

## Findings (severity-ranked)

**Major 1 (latent; the frozen r83 run is NOT affected) — `comment_lines` misclassifies lines
ending inside a PEP 701 multiline f-string (Py≥3.12), so D3 can change target behaviour.**
Two imprecisions: `range(tok.start[0], tok.end[0])` never marks a single-line string's line
and misses a multi-line string's closing line (both provably safe sides — the inserted
comment lands after a closed string; observed P7 rc=0); worse, lines whose only string
coverage is a FSTRING_MIDDLE that ends mid-line (then an expression continues) are marked
eligible although the line ends inside the f-string. Repro (receipts/probe-fexpr.out,
d3-fexpr.py):

```
python3 - <<'EOF'
import importlib.util, subprocess, sys, os, tempfile
spec = importlib.util.spec_from_file_location("mb",
  "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-83/c1/mutbat.py")
mb = importlib.util.module_from_spec(spec); spec.loader.exec_module(mb)
src = ('import sys\nV = f"""A\nB{1 +\n1}C"""\ndef selftest():\n    assert V == "A\\nB1C"\n'
       '    print("selftest cases=1 failures=0")\n    return 0\n'
       'if __name__ == "__main__":\n    sys.exit(selftest())\n')
rows = [{"id": "A", "anchor": "B{1 +\n1}C\"\"\"\n", "replacement": "B{9 +\n1}C\"\"\"\n",
         "class": "assertion", "kill_cases": ["c"]}]
rid, d3 = mb.single_decoy(src, rows, "ab")   # -> ('A', source with 'B{1 +  # mutbat-ab')
w = tempfile.mkdtemp(); open(w+"/t.py","w").write(d3)
print(subprocess.run([sys.executable, "-B", w+"/t.py"], capture_output=True, text=True).returncode)
EOF
```

Observed: single_decoy picks the row; the decoyed target's selftest goes rc=1
(AssertionError) — the comment is legal inside a multiline f-string expression but changes
the string value. Consequences for a future f-string-using target: a clean target can be
refused (`decoy=broken`, false alarm — fails loud) or its decoy behaviour silently shifts;
it can never cause a false pass (a broken decoy cannot make a mutant pass). Frozen-census
impact: none — `grep -c 'f"'` = 0 on the candidate, all 39 eligible anchors are plain code
lines, and the seed-chosen D3 passes cases=27 failures=0. Route: fix the marking to exclude
any line overlapped by FSTRING_START/MIDDLE/END *or* inside f-string expression ranges, or
reject anchors whose first line lies inside any f-string token span.

**Minor 2 — NOT-DERIVED diagnostics name only the primary anchor's count.** With a failing
`extra` site the line reads `MUTANT <id> verdict=NOT-DERIVED occurrences=<primary count>`
(observed `occurrences=1` for an extra with count 0; receipts/probe-d3.out P5). The row is
correctly refused; only the diagnosis is misleading. Route: report per-site counts or the
index of the failing site.

**Minor 3 — `--seed` makes D1/D2/D3 fully deterministic and precomputable per table.**
Validation allows any 1–64 char lowercase hex including `0`; a seeded run reproduces the
exact decoy bytes (D3 row and comment position), which re-opens the F10 hash-whitelist
surface against the counter itself. The frozen predicates (P3/P6) pass no seed, so this wave
is clean; keep production runs seedless, and treat any future seeded gate command as a
regression.

**Minor 4 (latent) — zero D3-eligible rows ⇒ decoy=broken refusal of a clean target.**
`single_decoy` returns (None, None) when every non-neutral anchor is single-line-without-
newline or starts on a string/backslash line (observed on the tripquote/backslash toys);
`run_decoy` then reports the decoys broken. Frozen table: 39/64 rows eligible, non-issue
here. Route: fall back to a hash-keyed trailing comment after the last line instead of
refusing.

**Note (no defect) — `decoy_hidden=63/64` is honest.** Row M2's anchor
(`            return -1\n`) is reproduced verbatim by both `ast.unparse` variants and so
survives D1/D2 (independent run on the r82 table: 59/60 with the same M2 row). Kills are
unaffected; the tally is a faithful count, not a padded one.

## Residual risk and verification gaps

- G1's selftest failure includes collateral `bucket-over` (both read `conform_ok`); the
  counter still classifies KILLED on the declared case (candidate control: miskilled=0).
- The f-string hole (Finding 1) was probed on one toy shape (expression-continuation);
  FSTRING_MIDDLE-literal-continuation shapes resolve to the same eligibility logic, but I did
  not enumerate every tokenizer layout.
- Host Python is 3.14.8; on ≤3.11 the f-string expression hole cannot exist (f-strings are
  single-token STRINGs), so the Major is version-gated.
- I did not re-run the full 67-row battery (the frozen control receipt
  c1-candidate-r83.txt covers it); my independent runs cover the pristine selftest, the
  counter selftest, the four G-rows, and the 63-row r82-equivalence battery.
- Known declared limit, unchanged and untested further: F8 AST-embedding forgery passes the
  r83 counter (claims P4 records it as a limit, not a pass condition).

## Files written

- `.ufo/waves/round-83/w1/ReviewC1.md` (this report)
- `.ufo/waves/round-83/w1/ReviewC1-receipts/pristine-selftest.out` — candidate selftest
  cases=27 failures=0, rc 0
- `.ufo/waves/round-83/w1/ReviewC1-receipts/mutbat-selftest.out` — `mutbat selftest ok`,
  r83_forgeries={'count': (True, False), 'hashwl': (True, False), 'path': (True, False)}
- `.ufo/waves/round-83/w1/ReviewC1-receipts/gapmut-G1.out … gapmut-G4.out` — per-mutant
  full selftest output (FAIL lines quoted above)
- `.ufo/waves/round-83/w1/ReviewC1-receipts/e82.out`, `e83.out` — r82 vs r83 counter on the
  same r82 target+table (63/63 identical MUTANT lines)
- `.ufo/waves/round-83/w1/ReviewC1-receipts/probe-d3.out`, `probe-d3b.out`,
  `probe-fexpr.out`, `d3-fexpr.py` — D3 edge probes and the Finding-1 repro
- `.ufo/waves/round-83/w1/ReviewC1-receipts/diff-census.diff`, `diff-mutbat.diff`,
  `run_gap_mutants.py`, `probe_d3.py`, `probe_d3b.py` — exact diffs and probe drivers
- Scratch `/fast/scratch/hyaku/kasegi-r83/ReviewC1` deleted before yield.
