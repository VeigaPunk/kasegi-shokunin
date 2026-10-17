# kasegi-shokunin — 稼ぎ

**Bounty & security research.** The craft of reading a program's rules,
building an authorization envelope, hunting with evidence, and wrapping
a claim package — including an honest zero.

A **shokunin lane**: an expert agent for one domain, minted and trained
under the [shokunin skill](https://github.com/VeigaPunk/shokunin).
Rank: **shonen**. Promotion is a named non-author review of
[`SHONEN.md`](SHONEN.md), never self-attestation.

This lane answers: *is this finding in scope, authorized, and packaged
so an operator can submit it — or is the honest result that there is
nothing to submit?*

## Domain

From [`PROVINCE.md`](PROVINCE.md): bounty programs, program rules, and
claim packages. The historical scope root `~/Projects/bounties` was
removed 2026-09-28; both surviving mirrors
(`~/Projects/the-bounty-hunter`, `~/Projects/origin-work/open-bug-bounties`)
went absent around 2026-10-12. The **domain is unchanged**. Citations
against those trees are corpus-attested records (`[lost-tree]`,
`[lost-base]`), not live-openable paths. See
`corpus/knowledge/source-tree-loss-2026-09-28.md` and
`corpus/knowledge/root-loss-2026-10-12.md`.

**Refuses** anything outside this domain. Cross-domain evidence is
reported to the orchestrator, never absorbed.

Submission is **operator-only**. This lane packages; it does not send.

## What's here

| Path | Role |
|---|---|
| [`SKILL.md`](SKILL.md) | pipeline, policy playbook, triage table, package anatomy, anti-patterns |
| [`PROVINCE.md`](PROVINCE.md) | owned domain and the lost-tree status of record |
| [`corpus/`](corpus/) | sourced knowledge, per-round lessons, depth instruments |
| [`SCORECARD.md`](SCORECARD.md) | depth + coverage axis verdicts |
| [`LOG.md`](LOG.md) | append-only round trail |
| [`SHONEN.md`](SHONEN.md) | promotion checklist |

## Pipeline (observed)

```
policy read → authorization envelope → custodian decision
          → hunt → six-file claim package → ops/claim-check.mjs
          → operator queue → OPERATOR submits
```

The six-file contract, gate inventory, and EV model live in `SKILL.md`
and `corpus/knowledge/`. They cite files; many of those files now
resolve only as corpus-attested history.

## Instruments

Committed under `corpus/instruments/` (see
[`corpus/instruments/README.md`](corpus/instruments/README.md)):

```sh
python3 corpus/instruments/density.py SKILL.md --label kasegi
python3 corpus/instruments/resolve.py .
python3 corpus/instruments/anchorcheck.py SKILL.md
```

`density.py` is a form-sensitive evidence proxy, not a proof that a
citation exists. `resolve.py` and `anchorcheck.py` are the checks that
the evidence still points at something.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
