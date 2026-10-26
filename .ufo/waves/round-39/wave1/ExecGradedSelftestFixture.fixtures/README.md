# G2' graded-selftest fixtures

Fixtures for the round-39 G2 check's case region: the receipt must carry
exactly eight graded `selftest case=G<n> positive=pass mutants=<a>/<b>
verdict=pass` lines, each backed by its own `selftest detail=G<n> mutant=...
rejected=1` lines, plus exactly one `selftest cases=8 failures=0`, and no
summary-only line may satisfy a case.

Every file here is a synthetic `all-gates v3` receipt. Header hashes are
placeholders (40 / 64 zeros) and are never bound to a lane head, so the
header-binding half of G2 (`export-ref` existence and ancestry,
`git diff --name-only <export-ref> REF` scope, `suite-sha256` digest) is out
of scope for these fixtures and stays tested by the suite's real run against a
real export.

## Contract

`judge-g2-cases.sh RECEIPT` prints exactly one line and exits 0 iff it ends
`closed=1`:

```
G2 payload=receipt=<0|1>,sentinel=<0|1>,run-lines=<0|1>,closed-line=<0|1>,cases=<n>,graded=<n>,detail-ok=<0|1>,summary=<n>,summary-only=<0|1> closed=<0|1>
```

| Field | Rule |
|---|---|
| `sentinel` | first line is exactly `all-gates v3` |
| `run-lines` | exactly eight distinct `G<n> payload=... closed=1` lines |
| `closed-line` | exactly one `closed=8/8 exit=0` |
| `cases` | number of `selftest case=G<n> ` lines, any id digits |
| `graded` | ids G1..G8 carrying exactly one case line that matches the whole-line regex `^selftest case=G<n> positive=pass mutants=<a>/<b> verdict=pass$` |
| `detail-ok` | 1 iff at least one id graded and every graded id has `b>=1`, `a==b`, exactly `b` `selftest detail=G<n> mutant=` lines and exactly `a` of them ending in `rejected=1` (a bare `rejected=10` does not count) |
| `summary` | number of `selftest cases=8 failures=0` lines |
| `summary-only` | 1 iff the receipt has `selftest ` lines but zero `selftest case=G<n> ` lines |
| `closed` | `sentinel && run-lines && closed-line && cases==8 && graded==8 && detail-ok && summary==1 && summary-only==0` |

All counts are anchored at the start of a line. This matters: the receipt's own
`G2 payload=...` line spells `cases=8,graded=8,detail-ok=1,summary=1,
summary-only=0`, so an unanchored counter reads a pass out of the receipt's own
claim about itself. Every fixture keeps that line, so an unanchored
implementation fails the mutants below.

## Layout

| File | Role |
|---|---|
| `receipt-green.txt` | positive control (variant a): eight graded, detail-backed cases |
| `b-summary-only.txt` | variant (b): summary line only, no case lines |
| `c-verdict-fail.txt` | variant (c): `positive=pass ... verdict=fail` |
| `d-missing-verdict.txt` | variant (d): no `verdict=` field |
| `e-seven-cases.txt` | variant (e): seven cases, summary still claims `cases=8` |
| `m01..m19*.txt` | nineteen further mutants (duplicate id, detail-free, ninth case, trailing field, summary drift, v2 sentinel, run-line drift, …) |
| `mutants.txt` | the mutant list to embed under G2: id, fixture, expected `closed`, mutation |
| `expected.tsv` | measured expected line + exit code per fixture (generated from judge output) |
| `judge-g2-cases.sh` | the judge implementing the table above |
| `run-fixtures.sh` | runs the judge over all fixtures against `expected.tsv` |
| `generate.py` | regenerates every receipt from the canonical green one |

## Use

```
./run-fixtures.sh                 # fixtures=24 pass=24 failures=0
python3 generate.py .             # rewrite the receipts + mutants.txt
```

Embed each `mutants.txt` row as a negative control in G2: copy the fixture into
the mutant tree as `.ufo/waves/round-39/final-gates/all-gates.txt` and require
the check to print `closed=0` with the expected payload line for that fixture.
The green receipt is the positive control and must print `closed=1`.
