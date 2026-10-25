# AttackA8 — selftest truth (falsify `selftest cases=15 failures=0 exit=0`)

- Attacked claim: `c1-receipt-index.txt:4` → `selftest cases=15 failures=0 exit=0` at landed instrument digest `3fc0d751…`.
- Verdict: **NOT falsified — receipt holds.** Observed run matches the receipt line on all three fields.

## Evidence

### 1. Instrument identity (verified before trusting the run)
`sha256sum corpus/instruments/recheck-audit.py` = `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1`
- matches `c1-receipt-index.txt:2` (`instrument_sha256=3fc0d751…`) and `c1-instrument-digest.txt:1`. The exercise ran exactly the pinned instrument.

### 2. Observed run (from lane root, `python3 corpus/instruments/recheck-audit.py --selftest`)
- Final exit code: `0` (captured as `EXIT=0`).
- Zero `FAIL` markers; all 15 case lines print `ok`.

### 3. Case list (15 cases)
Fixture cases (13): `good.md`, `prose.md`, `cwd.md`, `ghost.md`, `degenerate.md`, `elsewhere.md`, `ownonly.md`, `selftesty.md`, `sourced.md`, `basetest.md`, `basestate.md`, `parseonly.md`, `instonly.md`.
Tree-level expected-list fixtures (2): `expect-missing`, `expect-unexpected`.

### 4. Cross-check vs receipt line
| field | receipt (`c1-receipt-index.txt:4`) | observed | match |
|---|---|---|---|
| cases | 15 | 15 (13 fixture + 2 expected-list; script `total_cases = len(cases)+2`) | ✓ |
| failures | 0 | 0 (no non-ok case; script increments `failures` only on non-ok cases, returns `1 if failures else 0` — observed exit 0) | ✓ |
| exit | 0 | 0 | ✓ |

### 5. Nuance (16 vs 15 `selftest … ok` lines)
A literal grep of `^selftest .* ok$` yields **16** lines. The 16th is the auxiliary sanity line `selftest completeness lines=13 total=15 complete=False ok`, which per script comment (lines 300-301) is *not counted as a case* ("completeness is an auxiliary sanity line above, not counted as a case"). It correctly reports `complete=False` for the deliberate `missing-line.md` fixture and is itself an expected-ok assertion. So 15 = case count, 16 = line count; the receipt's `cases=15` matches the code's accounting.

### 6. Note on `failures=0` provenance
The selftest output does not emit a literal `failures=0` string; the tally follows from the return code (exit 0 ⇒ zero failures) and the absence of any `FAIL` case tag. This is consistent with the receipt line, which is authored by the gate tooling rather than by the instrument itself.

## Residual risk / verification gaps
- None material. The only caveat is the 16-vs-15 line-count nuance documented above; it is by design and does not affect the receipt's claim.
