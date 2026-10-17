# kasegi-shokunin

**Bounty and security research craft** — program rules, authorization
envelopes, and claim-package discipline.

Kasegi is the lane that knows how a program is scoped, what a claim
package must contain, and how to keep that work cited. It is not a
general exploit workshop and it is not a general research method
(that is chousa).

This is a **shokunin lane** of the [shokunin fleet](https://github.com/VeigaPunk/shokunin).
Rank: **shonen**.

## The craft

Observed pipeline (from [`SKILL.md`](SKILL.md), not invented here):

```
policy read (passive)     → evidence/<program>/scope-snapshot.json
authorization envelope    → evidence/authorization-envelope.json
work inside that envelope → claim package under claims/
```

The skill records program-rule reading, claim-package shape, verdict
ledgers, and citation hygiene. Every rule is supposed to cite a file.
When the file is gone, the citation is marked `[lost-tree]` or
`[lost-base]` and **does not count as verified**.

## Ground-truth status (recorded, not a re-scope)

The domain is unchanged: bounty & security research, program rules,
claim packages. The surfaces it was grounded in are not.

| When | What happened | Record |
|---|---|---|
| 2026-09-28 | `~/Projects/bounties` removed; data presumed-lost locally | `corpus/knowledge/source-tree-loss-2026-09-28.md` |
| 2026-10-12 | surviving roots `~/Projects/the-bounty-hunter` and `~/Projects/origin-work` also absent | `corpus/knowledge/root-loss-2026-10-12.md` |

Coverage claims against those trees are corpus-attested records, not
live-openable. Whether `PROVINCE.md` re-points is an operator decision
(L0), not a self-rescope.

## Province

Owns: bounty & security research — program rules, claim packages, the
authorization envelope, this lane's corpus.

**Refuses:** general source-research method (→
[chousa](https://github.com/VeigaPunk/chousa-shokunin)), model
evaluation (→ kengaku), secrets (→ kagi), orchestration (→ kumitate).
Out of province → report, never absorb.

This README does not reproduce exploit steps, payloads, or attack
procedures. Authorized research stays inside a recorded envelope;
work outside it is refused.

## What's in this repository

```
kasegi-shokunin/
├── SKILL.md           pipeline, package shape, citation rules
├── PROVINCE.md        domain + loss annotations (append-only)
├── SHONEN.md          promotion checklist
├── LOG.md             append-only trail
├── SCORECARD.md       per-axis verdicts
├── AGENTS.md
├── plans/
└── corpus/
    ├── knowledge/     including the two loss records
    ├── lessons/
    └── instruments/
```

## Start here

1. Read [`PROVINCE.md`](PROVINCE.md) for the current (absent) surfaces.
2. Read [`SKILL.md`](SKILL.md) as the craft — treat every host-absolute
   path as dated unless you can open it.
3. Read the two loss notes before citing a count from memory.

Do not re-point the province in a README. Do not treat a lost-tree
citation as a live verification.

## How a round works

One axis-move. Lane identity: `kasegi-shokunin <kasegi@shokunin.local>`.

## Fleet

[VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin) ·
[kimi-shokunin](https://github.com/VeigaPunk/kimi-shokunin)
