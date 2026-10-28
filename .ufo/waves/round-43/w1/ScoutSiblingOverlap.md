# ScoutSiblingOverlap — round 43

Verdict: kasegi's claim-package gate is disjoint. No sibling lane owns a claim-package gate, a six-file contract checker, or a disclosed-report-to-package workflow. `/home/vgpnk/Projects/shuknow` is absent. `/home/vgpnk/Projects/shokuknow` exists and does not own the checker either. Confidence: high (full walk of 20 sibling `corpus/knowledge` trees plus a sibling-`corpus` body scan for the contract tokens).

Province (kasegi, observed): `PROVINCE.md:3` domain is "bounty & security research — scopes ~/Projects/bounties, program rules, claim packages". `PROVINCE.md:29-30` core covers "program rules, scopes, and claim packages" plus "triage and claim gates, and submission/disclosure packaging". `PROVINCE.md:45` "Sibling lanes are reported, not absorbed." The six-file contract already lives only in kasegi: `corpus/knowledge/claim-package-contract.md:7-16` (`report.md`, `claim_checklist.md`, `evidence/manifest.json`, `custodian-receipts.json`, `provenance.json`, `status.json`; `scope_signal` exactly `NO_SCOPE_OBJECTION`). The executable gate this round adds, `corpus/instruments/claim-package-check.py`, is absent at the lane tip searched here (matches frozen C2 before). The lost checker it documents is `ops/claim-check.mjs` (`claim-gates.md:10-11`, `claim-package-contract.md:58`), not a sibling instrument.

## Search

Read-only. Assigned tokens: `claim_checklist`, `custodian`, `NO_SCOPE_OBJECTION`, `claim-package`, `redactions`. Also scanned sibling `corpus/` (not `.ufo/`) for `claim-package-check`, `custodian-receipts`, `NO_SCOPE_OBJECTION`, `claim_checklist`, `claim-package-contract`, `claim-gates`, `evidence-manifest/v1`, `disclosed report`, `disclosed-report`. Filename sweep for `*claim-package*`, `*claim_checklist*`, `*claim-gates*`, `*claim-check*` under every `*-shokunin/corpus` except kasegi: empty.

Knowledge-file census (md/json/txt/tsv), assigned tokens plus gate-shaped extras. Counts are occurrences/files.

| Lane | knowledge files | Assigned-token hits | Gate-shaped extras |
|---|---:|---|---|
| audio | 18 | none | none |
| chousa | 82 | none | none |
| game-dev-2d | 5 | none | none |
| game-dev-3d | 30 | none | `OPERATOR-GATED` x1 in `unreal-mcp/PROVENANCE.md:230` (Lutris credentials, not a claim checklist) |
| kagi | 25 | `custodian` x4 / 2 files | none |
| kaidoku | 138 | `redactions` x4 / 1 file | none |
| kake | 61 | none | none |
| kama | 40 | none | none |
| kengaku | 53 | none | none |
| kotoba | 65 | `claim-package` x5 / 1 file | `claim-gates` x4 / 2 files |
| kotodama | 253 | `custodian` x70 / 37 files; `redactions` x4 / 4 files | none |
| kumitate | 61 | `redactions` x1 / 1 file | none |
| lore | 26 | none | none |
| mado | 69 | none | none |
| mori | 73 | none | none |
| revenger | 19 | none | none |
| souji | 27 | none | none |
| tabi | 59 | none | none |
| tameshi | 64 | none | none |
| tsukuroi | 91 | none | none |
| kasegi (owner, not a sibling) | 61 | `claim_checklist` 15/5, `custodian` 51/10, `NO_SCOPE_OBJECTION` 10/4, `claim-package` 42/11, `redactions` 4/3 | `custodian-receipts` 17/7, `claim-gates` 58/5, `six-file` 10/7, `OPERATOR-GATED` 5/3, `prepare-claims` 6/4 |

Sibling corpus body scan: the only hit was kotoba's `claim-gates` citations. Zero sibling files contain `claim-package-check`, `custodian-receipts`, `NO_SCOPE_OBJECTION`, `claim_checklist`, `claim-package-contract`, `evidence-manifest/v1`, or `disclosed-report`. shokuknow grep for those same checker tokens: no matches.

Kasegi claim filenames under `corpus/`: `corpus/knowledge/claim-anatomy-sample.md`, `claim-gates.md`, `claim-package-contract.md`, plus r35 fixture copies of `claims-erratum-d5.md`. No `claim-package-check.py`.

## Hits that are not ownership

- kotoba `corpus/knowledge/fleet-skill-audit-round5.md:60` — audit row "kasegi L86" noting `corpus/knowledge/claim-gates.md` resolves under the skill repo. Citation of kasegi, not a kotoba gate.
- kotoba `corpus/knowledge/sibling-citation-routing-round16.json:508` — routing record whose text is `` `corpus/knowledge/claim-gates.md` ``. Same file line area quotes lost `[lost-base] ~/Projects/origin-work/open-bug-bounties/claim-packages/...` paths (the `claim-package` x5). Kotoba owns citation routing of kasegi paths.
- kagi `corpus/knowledge/tac-evidence-integrity.md:45` — custody record field `custodian: the-janitor` on one local TAC receipt (`tac-check`), sha256 of receipt bytes, `O_EXCL` so it never replaces. No `NO_SCOPE_OBJECTION`, no six files, no bounty package.
- kagi `corpus/knowledge/sops-age-key-rotation.md:49,98,108` — "independent custodians" / "independent key groups" for SOPS age. Secret-sharing custody, not claim packaging. `PROVINCE.md:48` already lists kagi as adjacent (secrets and vault).
- kaidoku `corpus/knowledge/2026-10-14-r10-01-queue-ops.md:202-217` — HAR `--sensitive-value` redactions (`explicit-sensitive-value` at JSON pointers) that leave `artifact.sha256` unchanged. Capture-envelope hygiene, not a same-digest producer/verifier redaction receipt.
- kumitate `corpus/knowledge/runtime-remainder-census.md:246-248` — `NativeRedactionMap` (`uniquified_task_ids`, `truncated_lines`, `truncated_fields`) for UFO-runtime transcript canonicalization. Not a claim package.
- kotodama — `custodian` is cultural authority (manuscripts, songlines, ritual offices, Haeri's ownership-vs-custodianship). `redactions` is manuscript recension (`china-ming.md`, `ottoman.md`, `vietnam.md`, `source-discipline-calibration.md`). Word collision only.
- shokuknow `lanes/kasegi/DOMAIN.md:79-81` and `merge/kasegi/knowledge/corpus/knowledge/claim-packaging-and-report-quality.md:1-36` — prose that kasegi's `claim-package-contract` / `claim-gates` describe a lost local tree, and that the openable equivalents are published platform rules (360SRC report template, BILISRC downgrade scenarios, CNVD 报告质量). No checker, no six-file schema, no `NO_SCOPE_OBJECTION`. shokuknow `mori` notes use "six-file sweep" for a watchdog path table (`SOURCES-PROPOSED.md` S535 area); that is not a claim package.

## Adjacency the L1 must report, not absorb

1. shokuknow platform report-quality templates (`claim-packaging-and-report-quality.md`, sources S034/S035/S036). They sit beside the gate: external program scoring and report-template fields. They are not the six-file machine contract and must not be folded into R-FILES..R-NOSECRET or into the exemplar.
2. kagi `tac-check` custody records. Same words (custodian, receipt, sha256), different object (one hardcoded local receipt, no scope signal). Already named adjacent in `PROVINCE.md:48`. Do not absorb `tac-check` into `claim-package-check.py`.
3. kaidoku sensitive-value redaction of capture envelopes. Different receipt shape (pointer + reason, digest unchanged, declaration strings not stored). Do not reuse it as R-REDACT.
4. kumitate `NativeRedactionMap`. Runtime transcript provenance, not bounty packaging. Do not absorb.
5. kotoba citation-routing rows that point at kasegi's `claim-gates.md` and the lost `claim-packages/` tree. Kotoba does not own the contract. Do not treat the routing table as a second gate or as a consumer the checker must satisfy.

No sibling has a disclosed-report-to-package workflow to absorb. The exemplar built from one public disclosed report stays inside kasegi's province (bounty and security-research claim packaging; `claimable` stays false; operator gates named in `claim_checklist.md`).

## Not adjacency

kotodama cultural "custodian" / manuscript "redactions"; game-dev-3d `OPERATOR-GATED` Lutris note; mori/shokuknow "six-file sweep" watchdog table; fifteen sibling knowledge trees with zero assigned-token hits (audio, chousa, game-dev-2d, kake, kama, kengaku, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi, and game-dev-3d on the five assigned tokens). chousa (research method) is already adjacent at `PROVINCE.md:47` and has no claim-package surface in 82 knowledge files.

## Unknowns

- Uncommitted wave scratch under the fleet root and under `.ufo/waves/` was not treated as lane corpus. A seat still writing this round could theoretically add a file after this scan; none of the committed sibling corpora had the checker at scan time.
- `~/Projects/bounties` and `~/Projects/origin-work/open-bug-bounties/claim-packages/` are the lost trees the kasegi docs name (`PROVINCE.md:16-22`). They were not re-opened here; absence of those trees is already the lane's recorded state, not a sibling owner.
- No network fetch. No tools installed.

## Evidence

Frozen claims read, not edited: `kasegi-shokunin/.ufo/waves/round-43/claims.json` (lane kasegi, round 43, base `ab98fac9dce87130bc4f66de89e30650d63943dc`). C2 before states `claim-package-check.py` and `fixtures/claim-package/` absent at base.

`ls -ld /home/vgpnk/Projects/shuknow` → `cannot access ... No such file or directory`. `shokuknow` is a directory (mtime 2026-10-27).

Sibling `corpus/` body scan (Python walk, contract tokens, `.ufo` excluded) printed only:

```
LANE kotoba-shokunin
  BODY claim-gates x1 kotoba-shokunin/corpus/knowledge/fleet-skill-audit-round5.md
  BODY claim-gates x3 kotoba-shokunin/corpus/knowledge/sibling-citation-routing-round16.json
```

shokuknow grep `claim-package-check|NO_SCOPE_OBJECTION|custodian-receipts|claim_checklist|evidence-manifest/v1` → no matches.

Filename command (scratch created and removed in the same command):

```
S=/fast/scratch/hyaku/kasegi-r43/ScoutSiblingOverlap
mkdir -p "$S" && export TMPDIR="$S"
shuknow=absent
shokuknow=present
test -f .../kasegi-shokunin/corpus/instruments/claim-package-check.py → absent
find *-shokunin/corpus claim-package|claim_checklist|claim-gates|claim-check excluding kasegi → empty
rm -rf -- "$S" && test ! -d "$S" → scratch_removed=yes
```

Kasegi `find corpus -name '*claim*'` also listed only the three knowledge files above and the r35 `claims-erratum-d5.md` fixture copies.
