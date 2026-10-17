# kasegi-shokunin

Bounty and security research — program rules, claim packages, and the
discipline of keeping a citation alive after the tree that held it is gone.

The domain has not changed. The filesystem under it has. `PROVINCE.md`
records two losses: `~/Projects/bounties` removed on 2026-09-28, and both
surviving roots named after that (`~/Projects/the-bounty-hunter` and
`~/Projects/origin-work`) absent around 2026-10-12. Coverage claims against
those trees are corpus-attested records. They are not live-openable paths.
The lane did not re-scope itself; that decision is left to the operator.

Rank: **shonen**. `SHONEN.md` is still here. Registered in the fleet
`MANIFEST.json` roster since 2026-09-28.

## Province

**Owns.** Bounty and security research: program rules, claim packages, and
the knowledge, playbooks, and checklists for that work.

**Hands off.** Anything outside that domain. Deep-research method as a
general craft belongs to chousa. This lane stays on program-specific
bounty research.

## Start here

1. `PROVINCE.md` — the domain, then the two loss annotations.
2. `corpus/knowledge/source-tree-loss-2026-09-28.md` and
   `corpus/knowledge/root-loss-2026-10-12.md` — the evidence of those losses.
3. `SKILL.md` — the playbook, with citations the instruments can re-check.
4. `corpus/instruments/README.md` — what the three measurement scripts are,
   and the roots they still expect when those roots exist.
5. `SCORECARD.md` — depth and coverage are this lane's axes. Read the
   round-15 structural event before any number.

## Measure the record

The instruments are stdlib-only and read-only. From the repository root:

```sh
python3 corpus/instruments/density.py SKILL.md --label skill
python3 corpus/instruments/anchorcheck.py SKILL.md
python3 corpus/instruments/test_resolve.py
```

`density.py` scores evidence density of a markdown file.
`anchorcheck.py` range-checks `path:line` citations against the lane, a
frozen mirror, a pinned git blob, or a declared origin-work root.
`resolve.py` classifies every backticked path as `RESOLVES`,
`MIRROR-EQUIVALENT`, `INTERNAL`, or `GONE`, and writes the census beside
itself — run it only when you intend to regenerate
`corpus/instruments/citation-survival.md`. `GONE` is a finding, not a
prompt to invent a new path.

## The tree

| Path | What it is |
|---|---|
| `corpus/knowledge/` | Program craft and the loss records |
| `corpus/lessons/` | Per-round lessons |
| `corpus/instruments/` | Density, citation resolution, anchor checks |
| `plans/` | Round plans |

## Fleet

Minted under [shokunin](https://github.com/VeigaPunk/shokunin).
