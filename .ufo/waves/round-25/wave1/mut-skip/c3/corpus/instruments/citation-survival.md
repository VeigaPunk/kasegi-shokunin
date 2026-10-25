# citation-survival census — kasegi lane

Instrument: `corpus/instruments/resolve.py` (stdlib-only, deterministic; r18 definition).
Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
Scope: `SKILL.md` + `corpus/**/*.md` (50 files).
Extraction: verbatim density.py docstring path-like rule (see module docstring).
Mirror root for bounty-path equivalence: `/home/vgpnk/Projects/the-bounty-hunter` (ABSENT — mirror fallback disabled).

## Totals

- distinct path-like citations: **1480** (total occurrences: 2925; a citation cited in both scopes counts once)
- distinct citations appearing in SKILL.md: 506 (of which SKILL-only: 327)
- distinct citations appearing in corpus: 1153

| class | distinct citations |
|---|---|
| RESOLVES | 10 |
| MIRROR-EQUIVALENT | 0 |
| GONE | 1346 |
| INTERNAL | 124 |
| OTHER *(root-domain bucket, orthogonal: the brief says classify other roots as RESOLVES/GONE)* | 10 resolve / 104 gone = 114 |

Terminal outcome classes sum to the distinct total: RESOLVES(10) + MIRROR-EQUIVALENT(0) + INTERNAL(124) + GONE(1346) = 1480.
Of the 10 RESOLVES, 10 are non-lane roots (domain `other`: origin-work, /tmp, ~/projects …); 0 are lane-repo-absolute.
Of the 0 MIRROR-EQUIVALENT, 0 were written as `~/Projects/bounties/...` (domain `bounty`), 0 were bounty-root-relative bare paths (domain `rel`).

## Resolvability rate

Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citations appearing in that scope (a citation in both scopes enters both denominators).

- SKILL.md alone: **32/506 = 6.32%**
- corpus alone: **118/1153 = 10.23%**
- lane total (SKILL.md + corpus): **134/1480 = 9.05%**

## Noise sub-census (GONE tokens that are rule artifacts, not citable paths)

Flag counts (a token can carry several flags):

| flags | distinct GONE citations |
|---|---|
| gitstatus | 3 |
| gitstatus,synthetic | 2 |
| regex | 10 |
| regex,synthetic | 7 |
| shell | 52 |
| shell,synthetic | 47 |
| synthetic | 484 |

- GONE citations carrying any noise flag: 605
- GONE citations with no noise flag (genuine vanished paths): 741
- citations containing glob/placeholder syntax (`* ? [ { } <...>`): 552

Noise-adjusted rates (denominator excludes noise-flagged citations):
- SKILL: 32/195 = 16.41%
- CORPUS: 106/801 = 13.23%
- ALL: 122/863 = 14.14%

## Scope x class matrix

| class | SKILL.md only | SKILL+corpus | corpus only | total |
|---|---|---|---|---|
| RESOLVES | 1 | 1 | 8 | 10 |
| MIRROR-EQUIVALENT | 0 | 0 | 0 | 0 |
| GONE | 311 | 163 | 872 | 1346 |
| INTERNAL | 15 | 15 | 94 | 124 |

## Citation-base ambiguity (r5's known hazard)

Relative tokens whose BASE resolves under BOTH the lane repo and the mirror root.
Policy resolves lane-first; the count is the size of the ambiguity, not an error.

- ambiguous relative citations: 0

## Self-verification (two independent ways)

1. Instrument (python3, stdlib) — distinct-token count above, recomputed in process from the extraction pass.
2. Independent shell pipeline, run from the lane repo root:

```bash
grep -ohP '`[^`\n]+`' SKILL.md corpus/README.md corpus/*/*.md \
 | sed 's/^`//; s/`$//' \
 | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' \
 | sed 's/^[.,;:]*//; s/[.,;:]*$//' \
 | grep -vP '^(https?|xd|skill)://' \
 | awk 'index($0," ")==0 || index($0,"/")>0' \
 | grep -P '(?i)(\.(mjs|md|json|jsonl|ya?ml|py|sh|txt|git|gitignore)$|/$|^~?/|[/<{~]|\.\.|\.(mjs|md|json|jsonl|ya?ml|py|sh|txt|git|gitignore):\d+(-\d+)?$)' \
 | sort -u | wc -l
```

Result: both yield **1480** distinct citations, and
`diff <(pipeline to file) <(cut -f1 citation-survival.tsv | tail -n +2 | sort -u)` is empty (sets identical, not just counts).
Re-running `resolve.py` twice leaves both outputs byte-identical (md5 stable).

## Honest scope limits

- MIRROR-EQUIVALENT means the same relative path exists in the Sep-5 genesis mirror `~/Projects/the-bounty-hunter`; it does NOT establish byte-equivalence with the vanished tree, and the mirror holds the code half only.
- Glob/brace citations resolve if any deterministic expansion exists; a glob with zero matches is GONE (e.g. `bounty-map/programs/*.json`).
- The path-like rule (verbatim from density.py) admits regex literals, git-porcelain snippets and shell fragments; the noise sub-census quantifies them so the raw rate can be read against the noise-adjusted rate.

## Line-anchor viability (resolvable citations carrying `:NN` / `:NN-MM`)

For every citation whose base resolves and whose anchor names a file, the anchor
is compared against the resolved file's line count (editor convention).

- anchors checked: 67 — in range: 67 — **out of range: 0**

| citation | class | resolved file | anchor | file lines | verdict |
|---|---|---|---|---|---|
| `../MISSION.md:49-56` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/../MISSION.md` | 49-56 | 88 | in range |
| `./PROVINCE.md:3` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/./PROVINCE.md` | 3 | 25 | in range |
| `SCORECARD.md:23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 23 | 186 | in range |
| `SKILL.md:10` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 10 | 1012 | in range |
| `SKILL.md:10-11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 10-11 | 1012 | in range |
| `SKILL.md:111` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 111 | 1012 | in range |
| `SKILL.md:111-112` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 111-112 | 1012 | in range |
| `SKILL.md:113-114` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 113-114 | 1012 | in range |
| `SKILL.md:113-117` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 113-117 | 1012 | in range |
| `SKILL.md:115` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 115 | 1012 | in range |
| `SKILL.md:117` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 117 | 1012 | in range |
| `SKILL.md:14-15` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 14-15 | 1012 | in range |
| `SKILL.md:146` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 146 | 1012 | in range |
| `SKILL.md:148` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 148 | 1012 | in range |
| `SKILL.md:149` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 149 | 1012 | in range |
| `SKILL.md:175` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 175 | 1012 | in range |
| `SKILL.md:175-176` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 175-176 | 1012 | in range |
| `SKILL.md:245-247` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 245-247 | 1012 | in range |
| `SKILL.md:246` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 246 | 1012 | in range |
| `SKILL.md:323` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 323 | 1012 | in range |
| `SKILL.md:385` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 385 | 1012 | in range |
| `SKILL.md:413` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 413 | 1012 | in range |
| `SKILL.md:459` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 459 | 1012 | in range |
| `SKILL.md:494-506` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 494-506 | 1012 | in range |
| `SKILL.md:498` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 498 | 1012 | in range |
| `SKILL.md:499` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 499 | 1012 | in range |
| `SKILL.md:500-501` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 500-501 | 1012 | in range |
| `SKILL.md:502` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 502 | 1012 | in range |
| `SKILL.md:522` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 522 | 1012 | in range |
| `SKILL.md:525` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 525 | 1012 | in range |
| `SKILL.md:526` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 526 | 1012 | in range |
| `SKILL.md:8` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 8 | 1012 | in range |
| `SKILL.md:86` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 86 | 1012 | in range |
| `SKILL.md:90-91` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 90-91 | 1012 | in range |
| `SKILL.md:94-95` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 94-95 | 1012 | in range |
| `corpus/README.md:49` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 49 | 169 | in range |
| `corpus/README.md:82` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 82 | 169 | in range |
| `corpus/instruments/README.md:31-38` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/README.md` | 31-38 | 82 | in range |
| `corpus/instruments/resolve.py:161-163` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py` | 161-163 | 516 | in range |
| `corpus/instruments/resolve.py:164-172` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py` | 164-172 | 516 | in range |
| `corpus/instruments/resolve.py:31-48` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py` | 31-48 | 516 | in range |
| `corpus/instruments/resolve.py:74` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py` | 74 | 516 | in range |
| `corpus/knowledge/claim-gates.md:3` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 3 | 119 | in range |
| `corpus/knowledge/claim-package-contract.md:31` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 31 | 62 | in range |
| `corpus/knowledge/ev-model.md:37-38` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ev-model.md` | 37-38 | 54 | in range |
| `corpus/knowledge/evidence-dir.md:78` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/evidence-dir.md` | 78 | 85 | in range |
| `corpus/knowledge/intake-and-finalize.md:78-92` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/intake-and-finalize.md` | 78-92 | 105 | in range |
| `corpus/knowledge/mission-control.md:3` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 3 | 165 | in range |
| `corpus/knowledge/ops-invariants.md:18` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 18 | 135 | in range |
| `corpus/knowledge/ops-invariants.md:24` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 24 | 135 | in range |
| `corpus/knowledge/policy-access-playbook.md:13` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/policy-access-playbook.md` | 13 | 29 | in range |
| `corpus/knowledge/program-quirks.md:10` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/program-quirks.md` | 10 | 61 | in range |
| `corpus/knowledge/retirement-autopsies.md:38` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/retirement-autopsies.md` | 38 | 135 | in range |
| `corpus/knowledge/submitted-registry.md:105` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/submitted-registry.md` | 105 | 223 | in range |
| `corpus/knowledge/submitted-registry.md:138-141` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/submitted-registry.md` | 138-141 | 223 | in range |
| `corpus/knowledge/submitted-registry.md:146-148` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/submitted-registry.md` | 146-148 | 223 | in range |
| `corpus/knowledge/submitted-registry.md:207-209` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/submitted-registry.md` | 207-209 | 223 | in range |
| `corpus/knowledge/triage-thresholds.md:25` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/triage-thresholds.md` | 25 | 481 | in range |
| `corpus/knowledge/ufo-archive-2026.md:11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ufo-archive-2026.md` | 11 | 204 | in range |
| `corpus/knowledge/ufo-archive-2026.md:145-149` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ufo-archive-2026.md` | 145-149 | 204 | in range |
| `corpus/knowledge/ufo-archive-2026.md:150-154` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ufo-archive-2026.md` | 150-154 | 204 | in range |
| `corpus/knowledge/ufo-archive-2026.md:36` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ufo-archive-2026.md` | 36 | 204 | in range |
| `corpus/lessons/round-4-aggregator-audit.md:26` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-4-aggregator-audit.md` | 26 | 70 | in range |
| `corpus/lessons/round-4-aggregator-audit.md:28` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-4-aggregator-audit.md` | 28 | 70 | in range |
| `corpus/lessons/round-5.md:16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-5.md` | 16 | 38 | in range |
| `corpus/lessons/round-8.md:10` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-8.md` | 10 | 53 | in range |
| `corpus/lessons/round-9.md:33` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-9.md` | 33 | 63 | in range |

Every MIRROR-EQUIVALENT anchor in range is still only a *same-name same-path*
match against a Sep-5 genesis sync — see §Honest scope limits.

## Top-20 most-cited GONE paths

| # | citation | files citing | occurrences | noise flags |
|---|---|---|---|---|
| 1 | `claims/` | 21 | 35 | - |
| 2 | `status.json` | 18 | 41 | - |
| 3 | `george/` | 15 | 19 | - |
| 4 | `ops/claim-check.mjs` | 14 | 22 | - |
| 5 | `fleets/registry.json` | 14 | 18 | - |
| 6 | `evidence/` | 13 | 21 | - |
| 7 | `docs/claim-ready-index.md` | 12 | 16 | - |
| 8 | `~/Projects/bounties` | 12 | 16 | - |
| 9 | `fleets/run/` | 11 | 15 | - |
| 10 | `claims/*/*/status.json` | 10 | 15 | synthetic |
| 11 | `claim-ready/*` | 9 | 13 | synthetic |
| 12 | `.ufo/` | 8 | 25 | - |
| 13 | `claim-hold/*` | 8 | 21 | synthetic |
| 14 | `ledger/missions.jsonl` | 8 | 16 | - |
| 15 | `~/Projects/the-bounty-hunter` | 8 | 16 | - |
| 16 | `ledger/` | 8 | 15 | - |
| 17 | `provenance.json` | 8 | 12 | - |
| 18 | `vdp-disclosures/` | 8 | 11 | - |
| 19 | `custodian-receipts.json` | 8 | 8 | - |
| 20 | `vgn-bounty-lab/` | 8 | 8 | - |

Max over all citations: files citing = 21, occurrences = 41.

## MIRROR-EQUIVALENT — exact list (0)

| # | citation | mirror path | lines | files | method |
|---|---|---|---|---|---|
