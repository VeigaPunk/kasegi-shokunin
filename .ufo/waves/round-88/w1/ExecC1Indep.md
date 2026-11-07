# ExecC1Indep — independent C1 re-derivation (round-88, attempt 1)

**Verdict: MATCH (0).** My independent re-derivation reproduces the frozen
`repair-map.json` (50 keys, byte-value identical) and `excluded.json` (59 keys,
every exclusion reason string identical). The frozen counter re-run on the C1
landing passes all limbs at exactly 742/1743.

## Method (independent, no shared code)

- Wrote my own script from the spec + docstring definitions only; imports only
  the lane's `corpus/instruments/resolve.py` (`classify`), never
  `build-map.py`/`knowledge-meter.py`. Script:
  `.ufo/waves/round-88/w1/ExecC1Indep-receipts/rederive.py`.
- Scope: `corpus/knowledge/*.md` at base
  `6beead9148945fa695cf3139e8fc9d8e91cc5fd0` via `git show` (99 files); 196
  distinct backticked `<name>.md[:N[-M]]` tokens found.
- Classification: `resolve.classify` against a `git clone --shared` of the base
  in scratch (`git rev-parse` asserted toplevel + HEAD =
  `6beead91...`). Mirror absent (`mirror_absent: True`), as at freeze.
- M8 content proxy re-implemented from the docstring: citing-line identifiers =
  5+ char words (`[A-Za-z_][A-Za-z0-9_]{4,}`) inside backticked/double-quoted
  spans, path-like spans excluded; every citing line must share one with the
  cited line range of the target entry at base; unanchored keys exempt.
- Builder gate re-derived per the frozen predicates: GONE first, then the
  basename is held by exactly one tracked non-`.ufo` file which is
  `corpus/knowledge/<name>.md`, anchor in range, then M8.

## Comparison

| set | frozen | mine | diff |
|---|---|---|---|
| repair-map keys | 50 | 50 | none (keys and values identical) |
| excluded keys | 59 | 59 | none |
| exclusion reasons | — | — | all 59 reason strings identical (54× `anchor-content-drift:...`, 3× `not-a-knowledge-entry:...`, 2× `basename-not-unique:...`) |

## Disagreement note (resolved, not a defect)

A first pass of my script flagged 46 extra tokens as excluded
(`SKILL.md*`, `SCORECARD.md*`, `LOG.md*`, `PROVINCE.md*`, `SHONEN.md*`,
`README.md*`) before the GONE gate. Reading the frozen builder showed the
gate order is GONE first, and all 46 classify INTERNAL, so the builder never
reaches them. After aligning the gate order, my excluded set matches the
frozen 59 exactly. The remaining 87 tokens (46 INTERNAL + 41 GONE with an
untracked basename, which the builder silently skips) are in neither frozen
file — consistent.

## Frozen counter on C1 landing (`fd33e1bfe26ad9af13c138feb87c9f222be957cb`)

Re-ran `.ufo/waves/round-88/c1/knowledge-meter.py` on a scratch clone at the
landing commit, `--base-rev 6beead91... --target 742/1743 --map-sha256
5a731401...` (full output: `ExecC1Indep-receipts/meter-landing.out`):

```
KNOWLEDGE-METER base=703/1754 after=742/1743 target=742/1743 keys=50 mirror_absent=True
LIMB M1 pass after=742/1743
LIMB M2 pass removed=50 keys=50 stray_removed=0 stray_added=0 unrepaired=0
LIMB M3 pass same_files=True bad_lines=0 keys_hit=50
LIMB M4 pass bad=none
LIMB M8 pass no_shared_identifier=none
LIMB M5 pass out_of_range=none
LIMB M6 pass sha256=5a731401a1f9145e24898a13c8a47be2135beabedde4352170cf2d2daa5d7960
KNOWLEDGE-METER-RESULT pass rc=0
```

## Defects / risks

None found. No credential-shaped values written; receipts carry only token
names, verdicts, digests and counter lines. No counter/gate output written
under /tmp; all runs used `TMPDIR=$S` with `python3 -B`.

Report: .ufo/waves/round-88/w1/ExecC1Indep.md
