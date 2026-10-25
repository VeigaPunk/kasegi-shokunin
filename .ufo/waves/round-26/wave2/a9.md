# Attack A9 — Gate-standard registry field checklist on the SKILL.md registry row

- **Attacked claim:** C1(a) — "SKILL.md gains a gate|probe registry row for recheck-audit.py with verdict map, self-test spelling (--selftest), pinned-value path, write scope, owner" (claims.json C1, frozen).
- **Verdict:** CONFORMANT at the byte level — all nine Gate-standard fields are present in the landed row, and the frozen counter (`grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md`) returns 1. One rendering defect is confirmed and is a deliberate trade-off (unescaped `gate|probe` type cell), detailed below.

## The landed row (verbatim, SKILL.md:981, raw bytes)

```
| recheck-audit.py | gate|probe | python3 corpus/instruments/recheck-audit.py [--json <out>] | 0 clean \| 1 failed \| undeclared nonzero -> could-not-evaluate | python3 corpus/instruments/recheck-audit.py --selftest | .ufo/waves/round-26/c1-receipt-index.txt | corpus/ read-only + its own receipt dir | kasegi |
```

Section context (SKILL.md:977-983):

```
## Gates & probes registry

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| recheck-audit.py | gate|probe | ... | ... | ... | ... | ... | kasegi |
```

Header has 8 columns; exactly one data row exists (no additional rows in the section).

## Field-by-field checklist

| # | Gate-standard field | Landed cell | Present? | Evidence |
|---|---|---|---|---|
| 1 | name | `recheck-audit.py` | PRESENT | Instrument exists at `corpus/instruments/recheck-audit.py`. |
| 2 | type (gate\|probe) | `gate|probe` | PRESENT (unescaped — see trade-off) | Type token present; rendering defect documented below. |
| 3 | entry command | `python3 corpus/instruments/recheck-audit.py [--json <out>]` | PRESENT | Matches instrument docstring usage lines 59-60 (`python3 corpus/instruments/recheck-audit.py`, `--json receipt.json`) and argparse `--json` (line 321). `[--json <out>]` is correct optional-arg notation. |
| 4 | verdict map (0 clean / 1 failed / undeclared nonzero -> could-not-evaluate) | `0 clean \| 1 failed \| undeclared nonzero -> could-not-evaluate` | PRESENT | Instrument declares exactly exits 0 and 1 (`main` returns `0 if ok else 1`, line 440; `selftest` returns `1 if failures else 0`, line 303). No other exit is declared; the undeclared-nonzero clause correctly covers exceptional exits as could-not-evaluate. Escaped `\|` renders as literal pipes in one cell. |
| 5 | self-test command | `python3 corpus/instruments/recheck-audit.py --selftest` | PRESENT | Matches usage line 64. Ran it: exit 0, all 15 cases pass (13 per-entry fixtures + 2 expected-list fixtures, per code comment lines 300-302). |
| 6 | spelling `--selftest` | `--selftest` | PRESENT | Exact spelling `--selftest` (single dash, one word); argparse flag is `--selftest`, `action="store_true"` (line 322). Verified by running the command. |
| 7 | pinned-value path | `.ufo/waves/round-26/c1-receipt-index.txt` | PRESENT | File exists. Its `instrument_sha256=3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` equals the sha256 I computed on the landed instrument; it carries `selftest cases=15 failures=0 exit=0` matching the observed selftest. |
| 8 | write scope | `corpus/ read-only + its own receipt dir` | PRESENT | Instrument reads `corpus/knowledge` + instruments (read mode) and writes only to the CLI-given `--json <out>` destination (lines 436-439); it never writes under `corpus/`. The machine receipt for the lane audit lives in `.ufo/waves/round-26/c1-live.json` (the receipt dir). |
| 9 | owner | `kasegi` | PRESENT | Lane identity `kasegi-shokunin`; the C1 executor seat was the sole owner of SKILL.md edits this round. |

## Evidence commands (all run from lane root, 2026-10-25 UTC)

- Frozen C1 counter: `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` → **1** (line 981). Note: GNU grep ERE treats `\|` as a literal pipe (undefined escape); the pattern matches the raw text `gate|probe `.
- Instrument digest: `sha256sum corpus/instruments/recheck-audit.py` → `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` = pinned `instrument_sha256` in c1-receipt-index.txt line 2.
- Selftest: `python3 corpus/instruments/recheck-audit.py --selftest` → exit 0, 15 cases all `ok`, expected-list fixtures red on missing/unexpected (exit=1 as wanted).
- Receipt line: `grep -cE 'selftest cases=' .ufo/waves/round-26/c1-receipt-index.txt` → 1; content `selftest cases=15 failures=0 exit=0`.
- Live audit receipt `.ufo/waves/round-26/c1-live.json`: `instrument_sha256=3fc0d751…`, `expect=present`, `expected=39`, `missing=[]`, `unexpected=[]`, `lines=39`, `pass=39`, `pass_strict=39`, `fail_closed=23`.

## The unescaped `gate|probe` rendering trade-off (confirmed)

The type cell contains a raw `|`; the verdict-map cell correctly uses `\|` escapes. Consequences under the GFM table rule (an unescaped `|` delimits cells; a row with more cells than the header has the extra cells discarded):

- Escaped-pipe-stripped delimiter count: header line 979 has 8 GFM cells; row 981 has **9** GFM cells (verified: `sed 's/\\|//g' SKILL.md | awk 'NR==979||NR==981 {n=gsub(/\|/,"|"); print n-1}'` → 8 vs 9).
- The 9th cell (`kasegi`) is discarded, and every cell after the type field lands in the wrong column: rendered `type=gate` (loses `probe`), `entry command=probe`, `verdict map=<entry command>`, `self-test=<verdict map>`, `pinned-value path=<self-test>`, `write scope=<pinned-value path>`, `owner=<write scope>`. A plain cmark renderer (no GFM tables) found locally outputs the pipes as literal paragraph text; the split is proven by the delimiter count.
- Why it is unescaped: the frozen counter regex requires literal bytes `gate|probe ` in the third cell. Escaping the cell as `gate\|probe` would change the bytes and make the counter return 0, failing C1(a). The landed row therefore satisfies the judged byte-level counter at the cost of a malformed rendered table (documented in wave1 `ExecSkillRegistry.md:43`).
- **Smallest safe correction (future round, not this read-only wave):** escape the cell to `gate\|probe` and teach the counter to accept the escaped form (e.g., match `gate\\|probe`, or unescape before counting); the verdict-map cell already models the correct escaped rendering. As landed, the row is conformant to the frozen counter's byte-level contract.

## Tooling

No tools installed or updated (none needed); no VCS mutations; read-only seat.
