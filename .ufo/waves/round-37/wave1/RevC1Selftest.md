# RevC1Selftest — r37 suite selftest acceptance bar (receipt)

Seat: RevC1Selftest-2 · round 37 · judged on depth:verifiability · leaf seat, no subagents.
Scope: set the selftest acceptance bar for `corpus/instruments/r37-closure.sh` (not yet committed at
receipt time; suite build is a sibling seat's item) and demonstrate the three forgery shapes fail it.
Model: the committed r36 suite's selftest format —
`corpus/instruments/r36-closure.sh` (894 lines at lane head b362068195d5489aa94b31e6ec8f880c367e0ba0),
specifically `judge_selftest_report` (r36-closure.sh:763-788) and `run_selftest`'s four forgery probes
(r36-closure.sh:790-846).

## 1. The bar (what `--selftest` output must satisfy to be accepted)

Modeled line-for-line on the r36 judge, generalized E1-E9 → E1-E14, plus one added clause (B6) that
makes the item's "each check's positive limb runs on the export" mechanically checkable. A selftest
report is ACCEPTED only if every clause holds; any single clause failing rejects the whole report.

- **B1** — exactly one summary line `selftest cases=14 failures=0`. No other summary spelling counts.
- **B2** — exactly 14 `selftest case=` lines, one per check id E1..E14 (each id exactly once), each
  ending `verdict=pass`. A report with fewer than 14 case lines, a missing id, or any `verdict=fail`
  is rejected.
- **B3** — every case line reads `selftest case=E<i> positive=pass mutants=<ok>/<n> verdict=pass`
  with `n >= 1` and `ok == n`. `mutants=0/0` (no mutant fixture ran) is rejected — this is the
  vacuous-report clause the r36 judge already carries ("a fabricated case line carrying mutants=0/0
  is rejected: n must be >= 1").
- **B4** — per check id, exactly `n` lines `selftest detail=E<i> mutant=...` of which exactly `ok`
  carry `rejected=1`. Fabricated case lines with no fixture detail behind them are rejected because
  `det=0 != n`.
- **B5** — every `rejected=1` detail line names the clause it reopens (`limb=<needle>` non-empty).
  This enforces the item's "mutant fixtures reopen exactly one clause and must be rejected": the
  rejection payload must name the reopened limb, so a fixture proves the check discriminates rather
  than that it can be satisfied by a summary.
- **B6** (added for r37) — per check id, exactly one `selftest detail=E<i> positive=pass payload=`
  line: the positive limb ran against the export tree (`st_pos`-style, payload = the check's own
  payload from the export), not against a fixture. The r36 judge does not carry this clause; the r37
  suite builder should add it (one `grep -c` per id inside the same per-id loop).

Fixture-construction requirement (not machine-checkable from the report alone, checked by reading the
suite): each mutant fixture must reopen exactly one clause of its check — the r36 model builds each
fixture by writing one mutated file into a scratch tree and re-running the real `check_e*` against it
(`st_neg`), so the rejection is the check's own verdict, never a hardcoded string.

## 2. Forgery attempts (scratch, against the bar)

Scratch: `/fast/scratch/hyaku/kasegi-r37/RevC1Selftest-2/` (removed before yield; scripts
`bar-check.sh`, `make-forgeries.sh`, `cross-check-r36-judge.sh`, `why-rejected.sh` lived there).
`bar-check.sh` is the bar above as an executable judge (14-check generalization of the r36
`judge_selftest_report`).

### Forgery 1 — summary-only

```
$ cat forge-summary-zero.txt
selftest cases=0 failures=0
$ cat forge-summary-only.txt
selftest cases=14 failures=0
```

Both claim the pass with zero case lines. Bar verdicts:

```
bar verdict=forge-summary-zero.txt accepted=0
bar verdict=forge-summary-only.txt accepted=0
```

Why: B1 fails for forge-summary-zero (summary-lines=0 — `cases=0 failures=0` is not the required
summary spelling); B2 fails for both (case-lines=0, every id E1..E14 case-line MISSING). Diagnostic
excerpt: `B1 summary-lines=0|1 (want 1) | B2 case-lines=0 verdict=pass-lines=0 (want 14/14)`.

### Forgery 2 — fake case lines

```
$ cat forge-caselines.txt
selftest case=E1 positive=pass mutants=3/3 verdict=pass
selftest case=E2 positive=pass mutants=3/3 verdict=pass
... (E3..E13 identical shape) ...
selftest case=E14 positive=pass mutants=3/3 verdict=pass
selftest cases=14 failures=0
```

Fourteen all-pass case lines + correct summary, but nothing ran. Bar verdict:

```
bar verdict=forge-caselines.txt accepted=0
```

Why: B4 fails for every id — `det=0 rej=0` vs the claimed `n=3 ok=3` (no `selftest detail=` lines
behind the case lines), and B6 fails (pos-detail=0: no export positive-limb payload line).
Diagnostic excerpt: `E1 n=3 ok=3 det=0 rej=0 pos-detail=0` (same for all 14 ids).

### Forgery 3 — fake suite

A fabricated full-suite transcript: header with `suite-sha256=`, fourteen `E<n> payload=fabricated
closed=1` lines, `closed=14/14 exit=0`, then a selftest section whose case lines claim pass with
`mutants=0/0`:

```
export-ref=b362068195d5489aa94b31e6ec8f880c367e0ba0 mode=export lane=kasegi suite-sha256=0000...0000
E1 payload=fabricated closed=1
E2 payload=fabricated closed=1
... (E3..E14 identical shape) ...
closed=14/14 exit=0
selftest case=E13 positive=pass mutants=0/0 verdict=pass
selftest case=E14 positive=pass mutants=0/0 verdict=pass
selftest cases=14 failures=0
```

This is the E10/D1 attack shape: a committed `all-gates.txt` whose `closed=14/14 exit=0` and
`cases=14 failures=0` lines were never produced by a run. Bar verdict:

```
bar verdict=forge-fake-suite.txt accepted=0
```

Why: B3 fails for every id — `n=0` violates `n >= 1` (the `mutants=0/0` vacuous-report clause); B4
and B6 also fail (det=0, rej=0, pos-detail=0). Diagnostic excerpt: `E1 n=0 ok=0 det=0 rej=0
pos-detail=0` (same for all 14 ids).

### Positive control (the bar is not vacuously rejecting)

A genuine-shaped report — per check one `positive=pass payload=` detail line, two rejected mutants
each naming their limb, `mutants=2/2`, correct summary — is ACCEPTED:

```
selftest detail=E1 positive=pass payload=control-payload
selftest detail=E1 mutant=clause-a rejected=1 limb=control-limb-a
selftest detail=E1 mutant=clause-b rejected=1 limb=control-limb-b
selftest case=E1 positive=pass mutants=2/2 verdict=pass
... (E2..E14 identical shape) ...
selftest cases=14 failures=0
```

```
bar verdict=control-genuine.txt accepted=1
```

Diagnostic: every id shows `n=2 ok=2 det=2 rej=2 pos-detail=1`.

### Cross-check against the committed r36 judge (the model)

The same forgery shapes adapted to the r36 suite's nine checks, fed to the r36 suite's own
`judge_selftest_report` (sourced verbatim from the committed `corpus/instruments/r36-closure.sh`):

```
r36-judge verdict=f36-summary-zero.txt accepted=0
r36-judge verdict=f36-summary-only.txt accepted=0
r36-judge verdict=f36-caselines.txt accepted=0
r36-judge verdict=f36-fake-suite.txt accepted=0
r36-judge verdict=f36-control-genuine.txt accepted=1
```

The committed model judge and my 14-check bar agree on all five shapes — the r37 bar is the r36
format, not a new invention.

## 3. Bar statement for the suite builder (one paragraph)

`r37-closure.sh --selftest` must print, per check E1..E14: one `selftest detail=E<i>
positive=pass payload=<check payload from the export tree>` line (the positive limb runs on the
export), then per mutant fixture one `selftest detail=E<i> mutant=<label> rejected=1 limb=<reopened
clause>` line, then one `selftest case=E<i> positive=pass mutants=<ok>/<n> verdict=pass` line with
`n >= 1` and `ok == n`; after the fourteen case lines exactly one `selftest cases=14 failures=0`
summary. The suite must judge its own report with the r36-style `judge_selftest_report` (generalized
to 14 ids, plus the per-id positive-detail clause) and must demonstrate at least the three forgery
shapes above are rejected (`selftest judge=forged-summary rejected=1`,
`judge=forged-caselines rejected=1`, `judge=forged-fake-suite rejected=1` — the r36 model also probes
`forged-failed-cases` and `forged-detail-free`; keep those too). Exit 0 only when all fourteen cases
executed, every positive passed on the export, and every mutant was rejected with its limb named.

## 4. Notes

- No writes outside the wave dir and scratch; no mutating git command run; no tool installs (none
  needed — bash/grep/sed/awk sufficed).
- r37-closure.sh was absent from the lane tree at receipt time (`git ls-files | grep -c r37-closure`
  → 0; no untracked copy), so the bar was exercised against forged reports and the genuine-shaped
  control, not against the real suite's output. The suite builder should run `bar-check.sh`-equivalent
  clauses as its own-report judge; the frozen C1 counting commands
  (`--selftest --export-ref <r37-final-lane-hash>` → `cases=14 failures=0 exit=0`) are the bar's B1/B2
  face.
- Scratch removed before yield; transcripts preserved above.
