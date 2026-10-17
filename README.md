# kasegi-shokunin — bounty & security research

**Program rules, claim packages, and the craft of a bounty ledger —
grounded in surviving records after the source trees disappeared.**

This is a [shokunin](https://github.com/VeigaPunk/shokunin) lane. Rank:
shonen. Kasegi owns bounty-program scope. It does not own general
source-research method (that is
[chousa](https://github.com/VeigaPunk/chousa-shokunin)) and it does not
own shipped-artifact reverse engineering (that is
[kaidoku](https://github.com/VeigaPunk/shokunin-reverse-engineering) /
[revenger](https://github.com/VeigaPunk/shokunin-binary-forensics)).

## Province

**Owns:** bounty & security research; program rules; claim packages; the
domain knowledge, playbooks, error patterns, and checklists in this
repo; the instruments that resolve, density-check, and anchor-check
surviving records.

**Refuses:** anything outside this domain. Report cross-domain evidence
back to the orchestrator.

The domain is unchanged. The ground is not.

- 2026-09-28T23:51:31Z — `~/Projects/bounties` was removed (actor
  UNDETERMINED, data PRESUMED-LOST locally). Evidence:
  `corpus/knowledge/source-tree-loss-2026-09-28.md`.
- On/around 2026-10-12 — both surviving roots
  (`~/Projects/the-bounty-hunter` HEAD `1cfbd86`,
  `~/Projects/origin-work/open-bug-bounties`) went absent. Evidence:
  `corpus/knowledge/root-loss-2026-10-12.md`.

Coverage claims against those trees are **corpus-attested records, not
live-openable**. Whether `PROVINCE.md` re-points is an operator
decision. The lane did not re-scope itself. Full boundary:
[`PROVINCE.md`](PROVINCE.md).

## Start here

1. [`SKILL.md`](SKILL.md) — craft rules, each citation tagged
   `[lost-tree]`, frozen-mirror, or corpus-attested.
2. [`PROVINCE.md`](PROVINCE.md) — domain plus the two loss annotations.
3. [`corpus/instruments/`](corpus/instruments/) — resolve / density /
   anchorcheck over surviving records.

## Instruments

```
python3 corpus/instruments/resolve.py .
python3 corpus/instruments/density.py SKILL.md
python3 corpus/instruments/anchorcheck.py SKILL.md
python3 corpus/instruments/test_resolve.py
```

`resolve.py` takes the lane-repo root and censuses backticked path-like
citations in `SKILL.md` plus `corpus/**/*.md`. `density.py` takes a
single Markdown file. `anchorcheck.py` takes a `path:NN` citation file
and keeps verdict classes separate (`IN-RANGE`, `MISSING-FILE`,
`PAST-EOF`, …). They operate on what the corpus still holds. They do
not resurrect the lost trees and they do not file a claim package with
a program.

## What's in the repo

```
kasegi-shokunin/
├── SKILL.md                 executable craft (citations as-of the loss dates)
├── PROVINCE.md              domain + loss annotations
├── SHONEN.md                promotion checklist
├── LOG.md                   append-only audit trail
├── SCORECARD.md             axis verdicts
├── AGENTS.md                operating rules
├── plans/                   round plans
└── corpus/
    ├── instruments/         resolve.py, density.py, anchorcheck.py
    ├── knowledge/           including the two loss notes
    └── lessons/
```

Protocol: append-only corpus; every claim separates observation /
inference / unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme) for how a lane
learns.
