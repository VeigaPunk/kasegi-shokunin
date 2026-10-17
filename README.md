# kasegi-shokunin

Bounty and security research: program rules, authorization envelopes, and
claim packages.

Rank: **shonen**. [`SHONEN.md`](SHONEN.md) boxes are open.

Fleet: [shokunin](https://github.com/VeigaPunk/shokunin).

## The question

> Does this claim package stay inside the program's own scope bytes, and
> can every citation in the craft still be resolved?

The skill was grounded in `~/Projects/bounties`. That tree was removed at
2026-09-28T23:51:31Z (actor undetermined, data presumed lost locally).
Round 19 records a second loss: both surviving roots,
`~/Projects/the-bounty-hunter` and `~/Projects/origin-work`, were absent
on the 2026-10-14 re-census. The domain did not change. Coverage claims
against those trees are corpus-attested records. `PROVINCE.md` keeps the
annotation and leaves any re-point as an operator decision.

Citations in `SKILL.md` carry a base tag: `[lost-tree]` or `[lost-base]`.
A tagged citation is recorded, never re-checked, and never counted as
verified.

## Boundary

**Owns:** program-rule reading, authorization envelopes derived from scope
bytes, claim-package structure, and the instruments that measure this
lane's own evidence density and citation survival.

**Hands off:** work outside bounty and security research. Adjacent
findings are reported to the owning lane.

## Instruments

Three stdlib scripts in [`corpus/instruments/`](corpus/instruments/).
They are read-only over the lane repo and the domain surfaces they can
still see. [`corpus/instruments/README.md`](corpus/instruments/README.md)
is the contract, including the known limits (density is form-sensitive
and does not check that a path exists).

```sh
python3 corpus/instruments/density.py SKILL.md --label skill
python3 corpus/instruments/resolve.py .
python3 corpus/instruments/anchorcheck.py SKILL.md
```

`density.py` scores evidence-shape inside a markdown file. `resolve.py`
classifies backticked path citations. `anchorcheck.py` range-checks
`path:line` citations, including the `ORIGIN_` / `MIRROR_` prefixes, and
prints the cited lines when the base is present.

## Map

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | pipeline, decision tables, loss-tagged citations |
| [`PROVINCE.md`](PROVINCE.md) | domain plus the two loss annotations |
| [`corpus/knowledge/source-tree-loss-2026-09-28.md`](corpus/knowledge/source-tree-loss-2026-09-28.md) | first loss |
| [`corpus/knowledge/root-loss-2026-10-12.md`](corpus/knowledge/root-loss-2026-10-12.md) | second loss |
| [`LOG.md`](LOG.md), [`SCORECARD.md`](SCORECARD.md) | rounds and axis verdicts |

The pipeline recorded in `SKILL.md` starts from policy text, builds an
authorization envelope from those bytes, and only then talks about a
claim. Passive reading of program rules is the front of that pipeline.
