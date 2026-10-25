# CritVacuityC1 — round 26 wave 1 (kasegi)

Seat: `L1Kasegi26.CritVacuityC1` (critic; read-only/scratch). Lane base
`1b076fa7f2fb5e7dd9d87449514eba526043421b` (claims-freeze commit). Access:
2026-10-25 (UTC). Assignment: attack C1 for vacuity — (1) registry row
without gate behavior, (2) deletion-fixture robustness vs mutants A/C/D,
(3) fix-control #3 restatement vs the retained historical line.

## Summary

| # | Finding | Verdict |
|---|---|---|
| 1 | Registry row counter `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` matches a literal `gate|probe ` cell and executes nothing → **decorative row satisfies after=≥1** | CONFIRMED |
| 2 | `lines/total` alone cannot catch whole-entry deletion (both sides shrink: 36/36); landed `--expect` expected-set equality catches BOTH deletion and rename, naming the entries — A: exit 0→1 | CONFIRMED (with integration conditions) |
| 3 | Frozen fix-control counter uses `grep -rnE '62 assertions\|77 assertions'`; on this host (`pi-uu-grep 0.2.0`) `\|` in ERE is a **literal pipe** → counter is an always-zero tautology. Under the intended BRE alternation the exclusion works exactly on `round-24.md:77` | CONFIRMED (frozen spelling broken; intent correct) |

---

## (1) Registry row: decorative row satisfies the counter — YES

Live: `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` → **1** (SKILL.md:981).
The pattern matches any row whose third cell begins with literal `gate|probe `
(verified: `printf '| x | gate|probe | y\n' | grep -cE …` → 1; a plain `gate`
cell → 0). Nothing in the counter executes the instrument, checks the verdict
map, the self-test spelling, the pinned-value path, or that the file even
exists. Peer seat m2 (`c1-controls/m2-registry-mutants.txt`) independently
found 4/5 field mutations survive the count; the e4 row had to use a
non-standard unescaped `gate|probe` cell (splits under a strict markdown
renderer) purely to satisfy the frozen regex. Counter #2
(`grep -cE 'selftest cases=' c1-receipt-index.txt`) likewise counts **any**
line containing `selftest cases=` — failures count, cases value, and digest
binding are unverified; a fabricated line passes.

**NOTE (round report; no claims.json edit):** bind the counters to executed
evidence — (a) counter #2 should require `selftest cases=[0-9]+ failures=0`
plus `instrument_sha256=` equal to a fresh `sha256sum
corpus/instruments/recheck-audit.py` at measurement time (stale/fabricated
receipts otherwise satisfy it); (b) commit the executed selftest + live-audit
outputs (c1-controls/e1/e3 receipts) and state in the round report that the
row's self-test column equals the receipted command; (c) require the deletion
fixture receipt to show `expect=present` so the fixture provably exercised the
gate.

Integration state observed: the committed receipt index
(`c1-receipt-index.txt`, `instrument_sha256=c3c19adc…`, `selftest cases=14
failures=0`) predates the landed instrument. Instrument sha lineage during this
review: `c3c19adc` (pre-fix) → `503de028d` (m1 note) → `ae4a7205` (first read;
selftest prints `cases=15 failures=0 exit=0`) → `3fc0d751` (final read;
`--selftest` no longer prints a `selftest cases=` summary line). The predicate
clause "receipt at the instrument's own digest" is therefore not satisfied by
the current bytes; the receipt index must be regenerated on the final
instrument bytes before commit.

## (2) Deletion fixture: expected-set equality catches BOTH deletion and rename

Pre-fix (m1 receipts `c1-controls/m1-*.txt` + my byte-identical scratch rerun
on `c3c19adc` bytes):

| mutant | m1 receipt (mine identical) | meaning |
|---|---|---|
| base | `lines=37 total=37 … exit=0` | do-nothing control |
| A delete one whole entry | `lines=36 total=36 … exit=0` | **deletion survives** |
| C rename one entry | `exit=1` (own/paths fail: line still names old filename) | incidental only |
| D stray extra file, no line | `lines=37 total=38 … exit=1` | caught by completeness |

Cause: completeness is `len(entries)==total`; deleting an entry shrinks both
sides together (36/36), so `lines/total` alone cannot see deletion — the
expected set breaks that symmetry.

Landed `--expect` (current instrument on same fixtures):

| mutant | receipt | exit |
|---|---|---|
| base | `expect=present expected=37 missing=0 unexpected=0` | 0 |
| A | `missing=1 (triage-thresholds.md)` | **1** |
| C | `missing=1 unexpected=1` (both names) | **1** |
| D | `unexpected=1 (stray-extra.md)` | **1** |

**CONFIRMED:** the fix catches full deletion (A flips 0→1, naming the entry)
and rename (C), independently of self-naming, via `expected_mismatch()` set
equality against the glob of `corpus/knowledge/*.md`.
Conditions for soundness (NOTE): (i) activation is default-path discovery —
`<root>/corpus/instruments/knowledge-expected.txt` must exist in the fixture
(the frozen counter does not pass `--expect`); the fixture must snapshot the
committed expected list BEFORE deleting an entry, else `expect=absent` falls
back to glob completeness and deletion passes again. (ii) The expected list
must track the entry set: after C2's two knowledge entries land,
`knowledge-expected.txt` must be regenerated/verified or the live audit
reds on `missing=[iso-29147-…]` (intended drift, but wave ordering must
handle it).


## (3) Fix-control #3 restatement vs retained historical line

Frozen spelling (run verbatim):
```
grep -rnE '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md | grep -v 'round-24.md:77' | wc -l
```
→ **0** (raw ERE also 0 hits). On this host (`grep --version` → pi-uu-grep
0.2.0; /bin and /usr/bin identical) `\|` inside ERE is a literal pipe
(verified: `printf 'a|b\n' | grep -E 'a\|b'` matches; `grep -E '62 assertions|77
assertions'` finds line 77 while `62 assertions\|77 assertions` finds nothing).
So the frozen counter is an always-zero tautology: it cannot fail under any
content, cannot see the retained historical line, and the claim's recorded
before (1 excluding the historical line) is unreproducible — a do-nothing run
yields 0 = the after value (kill-rule conflict).

Intended semantics (BRE form, as the round-25 lesson used, no `-E`):
```
grep -rn '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md
```
→ exactly **1** hit: `corpus/lessons/round-24.md:77` ("source-recheck.py` exits
0 over 19 records / 77 assertions."); with the exclusion → **0**. The
restatement therefore interacts CORRECTLY with the retained line under the
intended alternation (removes precisely the historical sentence; the appended
erratum lines 215–216 mention "77" without the literal pair).

**NOTE (round report):** restate the frozen counter without `-E` (or with
plain `|` alternation) and keep the `grep -v 'round-24.md:77'` exclusion;
record the frozen-spelling defect so the before=1/after=0 pair is meaningful.

## Evidence trail

- Claims: `.ufo/waves/round-26/claims.json` C1 counters, after values, kill rule.
- Instruments: `corpus/instruments/recheck-audit.py` (pre-fix c3c19adc;
  landed --expect; final 3fc0d751), `corpus/instruments/knowledge-expected.txt`
  (37 entries).
- Receipts: `c1-controls/m1-*.txt`, `m1-summary.json`, `m2-registry-mutants.txt`,
  `c1-receipt-index.txt` (line `selftest cases=14 failures=0`), `c1-live.json`
  (lines=37/37, exit 0).
- Scratch: `/tmp/critvacuity/{base,A,C,D}` (corpus snapshots; mutant A deletes
  triage-thresholds.md, C renames it, D adds stray-extra.md). All runs
  2026-10-25 UTC; outputs quoted in `k1-vacuity.txt`.

Report: `.ufo/waves/round-26/wave1/CritVacuityC1.md`
