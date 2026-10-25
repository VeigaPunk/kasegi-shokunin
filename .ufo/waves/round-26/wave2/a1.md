# AttackA1 — C1 counter (a): registry-row counter vs decorative-row satisfiability

Seat: `L1Kasegi26.AttackA1` (reviewer; read-only). Item: attack C1 counter (a)
— `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` (expect ≥1) — and verify the
landed row against the Gate-standard fields. Date: 2026-10-25 UTC. Outcome:
counter **returns 1 (claim's after value holds)**, but the counter is
**satisfiable by a decorative row** under the current bytes; the landed row
itself is **complete** (all eight fields present and binding to real bytes).

## Evidence gathered

- Counter, run verbatim from `claims.json` at lane root:
  `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` → **1** (exit 0).
- Exact match: SKILL.md:981 (only match in the file; `grep -n 'gate\|probe'`
  finds nothing else). Raw bytes (SKILL.md:977-983):
  - header (979): `| name | type | entry command | verdict map | self-test |
    pinned-value path | write scope | owner |`
  - row (981): `| recheck-audit.py | gate|probe | python3 corpus/instruments/recheck-audit.py [--json <out>] | 0 clean \| 1 failed \| undeclared nonzero -> could-not-evaluate | python3 corpus/instruments/recheck-audit.py --selftest | .ufo/waves/round-26/c1-receipt-index.txt | corpus/ read-only + its own receipt dir | kasegi |`
  - section placement: under `## Gates & probes registry` (977), followed by
    the expected-list sentence (983). Correct placement.
- Decorative-row demonstration (scratch, `/tmp/a1-deco/`; no production bytes
  touched):
  - `| fake-gate | gate|probe | echo hi | 0 clean \| 1 failed | python3 fake.py --selftest | /nonexistent | readonly | nobody |` → **count 1**.
  - a bare prose line inside a paragraph (not a table): `| x | gate|probe | y`
    → **count 1**.
  - the real landed row text alone → count 1.
  So the pattern matches any line starting `| <nonempty, pipe-free> | gate|probe `
  — arbitrary name, no instrument, no receipt, wrong flag, wrong owner all pass.
- Wave-1 mutation evidence (independent, same conclusion):
  `.ufo/waves/round-26/c1-controls/m2-registry-mutants.txt`: 4/5 field
  mutations survive the count (verdict map omitted, `--self-test` spelling,
  pinned-value path omitted, instrument-name typo → all still count 1; only
  dropping `|probe` flips to 0). `.ufo/waves/round-26/wave1/CritVacuityC1.md`
  §1 confirms; the round-26 lesson (corpus/lessons/round-26.md:102,112)
  itself records "the counter only discriminates the missing `|probe` marker;
  the other row properties are content-verified, not counter-verified."

## Findings by severity

### 1. [INFO — counter limitation, disclosed by the lane itself] Counter (a) is a literal byte-presence check; it cannot falsify a decorative row
The frozen counter matches any line whose third cell begins with literal
`gate|probe ` and executes nothing. It does not verify: the row lives in the
Gates & probes registry section; the instrument file exists; the verdict map
matches the instrument's exit behavior; the `--selftest` spelling/flag exists;
the pinned-value path exists and is bound to the instrument digest; write scope
or owner. Demonstrated above by construction (fake-gate row = 1; prose line =
1) and by wave-1 m2 mutants (4/5 survive). A decorative row would satisfy the
claimed AFTER value. This is a known, recorded limitation (lesson round-26:102),
not a defect in the landed row.

### 2. [INFO — verified complete] The landed row is complete and accurate against all eight Gate-standard fields
| Field | Row value | Verification |
|---|---|---|
| name | `recheck-audit.py` | file `corpus/instruments/recheck-audit.py` exists; its sha256 = `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` (computed now) = the pinned `instrument_sha256` in the receipt index |
| type | `gate|probe` | literal byte present (unescaped pipe — see note below) |
| entry command | `python3 corpus/instruments/recheck-audit.py [--json <out>]` | matches the instrument docstring Usage (lines 58-64) |
| verdict map | `0 clean \| 1 failed \| undeclared nonzero -> could-not-evaluate` | consistent with `main()`: returns `0 if ok else 1` (line 440); undeclared nonzero → could-not-evaluate is the lane vocabulary (round-9 lesson); argparse errors exit 2 (undeclared) |
| self-test | `python3 corpus/instruments/recheck-audit.py --selftest` | flag exists verbatim as `--selftest` (line 322); receipt index records `selftest cases=15 failures=0 exit=0` at the landed digest |
| pinned-value path | `.ufo/waves/round-26/c1-receipt-index.txt` | file exists; line 2 `instrument_sha256=3fc0d751…` equals the instrument's digest; line 4 selftest receipt; lines 7-9 live audit (`strict pass=39/39 … expect=present expected=39 missing=0 unexpected=0`); EXIT=0 |
| write scope | `corpus/ read-only + its own receipt dir` | instrument's only write sites are the caller-supplied `--json` path (line 436-439) and scratch tempdirs inside `selftest()` (lines 202-272); no production corpus writes |
| owner | `kasegi` | lane match |

### 3. [OBS — formatting, not a claim defect] Unescaped `gate|probe` cell splits under a strict markdown renderer
The type cell contains a raw `|` (`gate|probe`), so a strict renderer splits it
(10 cells vs the 8-column header). The frozen regex byte-matches `gate|probe`
verbatim, so escaping as `gate\|probe` would fail the counter; the row was
necessarily written unescaped. Cosmetic only; does not affect the counter or
the row's accuracy.

## Residual risk
- Counter (a) has no semantic binding: any future edit that drops the row's
  real content (verdict map, correct flag, path, owner) while keeping the
  `gate|probe ` literal still passes. Enforcement currently rests on content
  review (m2-style), which the lane already records — it is not enforced by the
  claim's counter.
- The `gate|probe` marker is the only discriminator in the pattern; if the
  registry ever grows more gate rows, the counter (expect 1) will need a
  name-specific pattern or it will count multiple rows.

## Verification gaps
- I did not re-execute `--selftest` or the full live audit (not required for
  this item); the receipt index's declared digest equals the current instrument
  file hash, so the selftest/live receipts are consistent with the bytes
  measured now.
- The `could-not-evaluate` convention is quoted from the lane vocabulary
  (round-9 lesson), not re-derived from the instrument (the instrument itself
  only ever returns 0/1).

No tools installed; no production bytes modified by this seat.
