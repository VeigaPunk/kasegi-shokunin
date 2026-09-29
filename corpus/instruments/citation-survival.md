# citation-survival census — kasegi lane, r15

Instrument: `/tmp/kasegi-r15/resolve.py` (stdlib-only, deterministic).
Lane root: `/home/vgpnk/projects/shokunin/kasegi-shokunin`
Scope: `SKILL.md` + `corpus/**/*.md` (47 files).
Extraction: verbatim density.py docstring path-like rule (see module docstring).
Mirror root for bounty-path equivalence: `/home/vgpnk/Projects/the-bounty-hunter`.

## Totals

- distinct path-like citations: **1437** (total occurrences: 3649; a citation cited in both scopes counts once)
- distinct citations appearing in SKILL.md: 486 (of which SKILL-only: 140)
- distinct citations appearing in corpus: 1297

| class | distinct citations |
|---|---|
| RESOLVES | 90 |
| MIRROR-EQUIVALENT | 220 |
| GONE | 1027 |
| INTERNAL | 100 |
| OTHER *(root-domain bucket, orthogonal: the brief says classify other roots as RESOLVES/GONE)* | 90 resolve / 29 gone = 119 |

Terminal outcome classes sum to the distinct total: RESOLVES(90) + MIRROR-EQUIVALENT(220) + INTERNAL(100) + GONE(1027) = 1437.
Of the 90 RESOLVES, 90 are non-lane roots (domain `other`: origin-work, /tmp, ~/projects …); 0 are lane-repo-absolute.
Of the 220 MIRROR-EQUIVALENT, 18 were written as `~/Projects/bounties/...` (domain `bounty`), 202 were bounty-root-relative bare paths (domain `rel`).

## Resolvability rate

Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citations appearing in that scope (a citation in both scopes enters both denominators).

- SKILL.md alone: **222/486 = 45.68%**
- corpus alone: **396/1297 = 30.53%**
- lane total (SKILL.md + corpus): **410/1437 = 28.53%**

## Noise sub-census (GONE tokens that are rule artifacts, not citable paths)

Flag counts (a token can carry several flags):

| flags | distinct GONE citations |
|---|---|
| gitstatus | 3 |
| gitstatus,synthetic | 2 |
| regex | 9 |
| regex,synthetic | 7 |
| shell | 42 |
| shell,synthetic | 46 |
| synthetic | 171 |

- GONE citations carrying any noise flag: 280
- GONE citations with no noise flag (genuine vanished paths): 747
- citations containing glob/placeholder syntax (`* ? [ { } <...>`): 256

Noise-adjusted rates (denominator excludes noise-flagged citations):
- SKILL: 213/420 = 50.71%
- CORPUS: 364/1016 = 35.83%
- ALL: 378/1125 = 33.60%

## Scope x class matrix

| class | SKILL.md only | SKILL+corpus | corpus only | total |
|---|---|---|---|---|
| RESOLVES | 0 | 5 | 85 | 90 |
| MIRROR-EQUIVALENT | 0 | 189 | 31 | 220 |
| GONE | 126 | 138 | 763 | 1027 |
| INTERNAL | 14 | 14 | 72 | 100 |

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

Result: both yield **1437** distinct citations, and
`diff <(pipeline to file) <(cut -f1 citation-survival.tsv | tail -n +2 | sort -u)` is empty (sets identical, not just counts).
Re-running `resolve.py` twice leaves both outputs byte-identical (md5 stable).

## Honest scope limits

- MIRROR-EQUIVALENT means the same relative path exists in the Sep-5 genesis mirror `~/Projects/the-bounty-hunter`; it does NOT establish byte-equivalence with the vanished tree, and the mirror holds the code half only.
- Glob/brace citations resolve if any deterministic expansion exists; a glob with zero matches is GONE (e.g. `bounty-map/programs/*.json`).
- The path-like rule (verbatim from density.py) admits regex literals, git-porcelain snippets and shell fragments; the noise sub-census quantifies them so the raw rate can be read against the noise-adjusted rate.

## Line-anchor viability (resolvable citations carrying `:NN` / `:NN-MM`)

For every citation whose base resolves and whose anchor names a file, the anchor
is compared against the resolved file's line count (editor convention).

- anchors checked: 224 — in range: 222 — **out of range: 2**

| citation | class | resolved file | anchor | file lines | verdict |
|---|---|---|---|---|---|
| `PROVINCE.md:3` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/PROVINCE.md` | 3 | 6 | in range |
| `README.md:19` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/README.md` | 19 | 75 | in range |
| `README.md:23` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/README.md` | 23 | 75 | in range |
| `README.md:30` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/README.md` | 30 | 75 | in range |
| `SCORECARD.md:23` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SCORECARD.md` | 23 | 105 | in range |
| `SKILL.md:10` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 10 | 997 | in range |
| `SKILL.md:10-11` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 10-11 | 997 | in range |
| `SKILL.md:111` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 111 | 997 | in range |
| `SKILL.md:111-112` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 111-112 | 997 | in range |
| `SKILL.md:113-114` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 113-114 | 997 | in range |
| `SKILL.md:113-117` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 113-117 | 997 | in range |
| `SKILL.md:115` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 115 | 997 | in range |
| `SKILL.md:117` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 117 | 997 | in range |
| `SKILL.md:14-15` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 14-15 | 997 | in range |
| `SKILL.md:146` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 146 | 997 | in range |
| `SKILL.md:148` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 148 | 997 | in range |
| `SKILL.md:149` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 149 | 997 | in range |
| `SKILL.md:175` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 175 | 997 | in range |
| `SKILL.md:175-176` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 175-176 | 997 | in range |
| `SKILL.md:245-247` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 245-247 | 997 | in range |
| `SKILL.md:246` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 246 | 997 | in range |
| `SKILL.md:323` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 323 | 997 | in range |
| `SKILL.md:385` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 385 | 997 | in range |
| `SKILL.md:413` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 413 | 997 | in range |
| `SKILL.md:459` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 459 | 997 | in range |
| `SKILL.md:494-506` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 494-506 | 997 | in range |
| `SKILL.md:498` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 498 | 997 | in range |
| `SKILL.md:499` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 499 | 997 | in range |
| `SKILL.md:500-501` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 500-501 | 997 | in range |
| `SKILL.md:502` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 502 | 997 | in range |
| `SKILL.md:522` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 522 | 997 | in range |
| `SKILL.md:525` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 525 | 997 | in range |
| `SKILL.md:526` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 526 | 997 | in range |
| `SKILL.md:8` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 8 | 997 | in range |
| `SKILL.md:86` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 86 | 997 | in range |
| `SKILL.md:90-91` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 90-91 | 997 | in range |
| `SKILL.md:94-95` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/SKILL.md` | 94-95 | 997 | in range |
| `bounty-map/schema.json:32-52` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 32-52 | 68 | in range |
| `bounty-map/schema.json:34` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 34 | 68 | in range |
| `bounty-map/schema.json:35-51` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 35-51 | 68 | in range |
| `bounty-map/schema.json:40` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 40 | 68 | in range |
| `bounty-map/schema.json:46` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 46 | 68 | in range |
| `bounty-map/schema.json:47` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 47 | 68 | in range |
| `bounty-map/schema.json:48` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 48 | 68 | in range |
| `corpus/README.md:49` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/README.md` | 49 | 160 | in range |
| `corpus/README.md:82` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/README.md` | 82 | 160 | in range |
| `corpus/knowledge/ev-model.md:30` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/knowledge/ev-model.md` | 30 | 54 | in range |
| `corpus/knowledge/evidence-dir.md:78` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/knowledge/evidence-dir.md` | 78 | 85 | in range |
| `corpus/knowledge/intake-and-finalize.md:78-92` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/knowledge/intake-and-finalize.md` | 78-92 | 105 | in range |
| `corpus/knowledge/mission-control.md:3` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 3 | 165 | in range |
| `corpus/knowledge/ops-invariants.md:24` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 24 | 135 | in range |
| `corpus/knowledge/policy-access-playbook.md:13` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/knowledge/policy-access-playbook.md` | 13 | 29 | in range |
| `corpus/knowledge/program-quirks.md:10` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/knowledge/program-quirks.md` | 10 | 61 | in range |
| `corpus/knowledge/retirement-autopsies.md:38` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/knowledge/retirement-autopsies.md` | 38 | 135 | in range |
| `corpus/knowledge/ufo-archive-2026.md:11` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/knowledge/ufo-archive-2026.md` | 11 | 204 | in range |
| `corpus/knowledge/ufo-archive-2026.md:145-149` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/knowledge/ufo-archive-2026.md` | 145-149 | 204 | in range |
| `corpus/knowledge/ufo-archive-2026.md:150-154` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/knowledge/ufo-archive-2026.md` | 150-154 | 204 | in range |
| `corpus/knowledge/ufo-archive-2026.md:36` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/knowledge/ufo-archive-2026.md` | 36 | 204 | in range |
| `corpus/lessons/round-4-aggregator-audit.md:26` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/lessons/round-4-aggregator-audit.md` | 26 | 70 | in range |
| `corpus/lessons/round-4-aggregator-audit.md:28` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/lessons/round-4-aggregator-audit.md` | 28 | 70 | in range |
| `corpus/lessons/round-5.md:16` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/lessons/round-5.md` | 16 | 38 | in range |
| `corpus/lessons/round-8.md:10` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/lessons/round-8.md` | 10 | 53 | in range |
| `corpus/lessons/round-9.md:33` | INTERNAL | `/home/vgpnk/projects/shokunin/kasegi-shokunin/corpus/lessons/round-9.md` | 33 | 63 | in range |
| `docs/genesis-plan.md:15` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/docs/genesis-plan.md` | 15 | 178 | in range |
| `docs/genesis-plan.md:17` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/docs/genesis-plan.md` | 17 | 178 | in range |
| `fleets/mission-template.md:20` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/fleets/mission-template.md` | 20 | 64 | in range |
| `fleets/mission-template.md:50` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/fleets/mission-template.md` | 50 | 64 | in range |
| `ops/check-freshness.mjs:12` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 12 | 62 | in range |
| `ops/check-freshness.mjs:14` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 14 | 62 | in range |
| `ops/check-freshness.mjs:15` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 15 | 62 | in range |
| `ops/check-freshness.mjs:43` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 43 | 62 | in range |
| `ops/check-freshness.mjs:50` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 50 | 62 | in range |
| `ops/check-freshness.mjs:59` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 59 | 62 | in range |
| `ops/check-freshness.mjs:61` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 61 | 62 | in range |
| `ops/claim-check.mjs:174-199` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/claim-check.mjs` | 174-199 | 83 | OUT OF RANGE |
| `ops/claim-index.mjs:11` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/claim-index.mjs` | 11 | 49 | in range |
| `ops/claim-index.mjs:4` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/claim-index.mjs` | 4 | 49 | in range |
| `ops/ev-report.mjs:16` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 16 | 92 | in range |
| `ops/ev-report.mjs:17` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 17 | 92 | in range |
| `ops/ev-report.mjs:21` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 21 | 92 | in range |
| `ops/ev-report.mjs:23-26` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 23-26 | 92 | in range |
| `ops/ev-report.mjs:28-29` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 28-29 | 92 | in range |
| `ops/ev-report.mjs:30-33` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 30-33 | 92 | in range |
| `ops/ev-report.mjs:38-41` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 38-41 | 92 | in range |
| `ops/ev-report.mjs:43` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 43 | 92 | in range |
| `ops/ev-report.mjs:46` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 46 | 92 | in range |
| `ops/ev-report.mjs:47` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 47 | 92 | in range |
| `ops/ev-report.mjs:50` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 50 | 92 | in range |
| `ops/ev-report.mjs:55` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 55 | 92 | in range |
| `ops/ev-report.mjs:56` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 56 | 92 | in range |
| `ops/ev-report.mjs:57` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 57 | 92 | in range |
| `ops/ev-report.mjs:59-70` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 59-70 | 92 | in range |
| `ops/ev-report.mjs:65` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 65 | 92 | in range |
| `ops/ev-report.mjs:69` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 69 | 92 | in range |
| `ops/ev-report.mjs:70` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 70 | 92 | in range |
| `ops/ev-report.mjs:73` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 73 | 92 | in range |
| `ops/ev-report.mjs:74` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 74 | 92 | in range |
| `ops/ev-report.mjs:77` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 77 | 92 | in range |
| `ops/ev-report.mjs:78` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 78 | 92 | in range |
| `ops/ev-report.mjs:79-81` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 79-81 | 92 | in range |
| `ops/ev-report.mjs:82` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 82 | 92 | in range |
| `ops/ev-report.mjs:86-89` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 86-89 | 92 | in range |
| `ops/ev-report.mjs:91` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 91 | 92 | in range |
| `ops/ev-report.mjs:92` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 92 | in range |
| `ops/finalize-all.mjs:11` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/finalize-all.mjs` | 11 | 39 | in range |
| `ops/finalize-all.mjs:20` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/finalize-all.mjs` | 20 | 39 | in range |
| `ops/finalize-all.mjs:25` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/finalize-all.mjs` | 25 | 39 | in range |
| `ops/fleet-dispatch.mjs:11` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs` | 11 | 331 | in range |
| `ops/fleet-dispatch.mjs:152` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs` | 152 | 331 | in range |
| `ops/fleet-dispatch.mjs:155` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs` | 155 | 331 | in range |
| `ops/fleet-dispatch.mjs:156` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs` | 156 | 331 | in range |
| `ops/fleet-dispatch.mjs:21` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs` | 21 | 331 | in range |
| `ops/import-board.mjs:132` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/import-board.mjs` | 132 | 258 | in range |
| `ops/import-board.mjs:30` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/import-board.mjs` | 30 | 258 | in range |
| `ops/park-disposition.mjs:12` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 12 | 80 | in range |
| `ops/park-disposition.mjs:13` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 13 | 80 | in range |
| `ops/park-disposition.mjs:14` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 14 | 80 | in range |
| `ops/park-disposition.mjs:18` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 18 | 80 | in range |
| `ops/park-disposition.mjs:18-21` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 18-21 | 80 | in range |
| `ops/park-disposition.mjs:19` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 19 | 80 | in range |
| `ops/park-disposition.mjs:21` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 21 | 80 | in range |
| `ops/park-disposition.mjs:23-25` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 23-25 | 80 | in range |
| `ops/park-disposition.mjs:28-32` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 28-32 | 80 | in range |
| `ops/park-disposition.mjs:32` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 32 | 80 | in range |
| `ops/park-disposition.mjs:36-39` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 36-39 | 80 | in range |
| `ops/park-disposition.mjs:41` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 41 | 80 | in range |
| `ops/park-disposition.mjs:43` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 43 | 80 | in range |
| `ops/park-disposition.mjs:45-49` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 45-49 | 80 | in range |
| `ops/park-disposition.mjs:52` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 52 | 80 | in range |
| `ops/park-disposition.mjs:53` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 53 | 80 | in range |
| `ops/park-disposition.mjs:53-74` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 53-74 | 80 | in range |
| `ops/park-disposition.mjs:56` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 56 | 80 | in range |
| `ops/park-disposition.mjs:56-59` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 56-59 | 80 | in range |
| `ops/park-disposition.mjs:59` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 59 | 80 | in range |
| `ops/park-disposition.mjs:61` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 61 | 80 | in range |
| `ops/park-disposition.mjs:61-65` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 61-65 | 80 | in range |
| `ops/park-disposition.mjs:62-65` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 62-65 | 80 | in range |
| `ops/park-disposition.mjs:67-70` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 67-70 | 80 | in range |
| `ops/park-disposition.mjs:70` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 70 | 80 | in range |
| `ops/park-disposition.mjs:72-73` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 72-73 | 80 | in range |
| `ops/park-disposition.mjs:75-77` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 75-77 | 80 | in range |
| `ops/park-disposition.mjs:78` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 78 | 80 | in range |
| `ops/rank.mjs:104` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 104 | 249 | in range |
| `ops/rank.mjs:105-108` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 105-108 | 249 | in range |
| `ops/rank.mjs:118-119` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 118-119 | 249 | in range |
| `ops/rank.mjs:123` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 123 | 249 | in range |
| `ops/rank.mjs:126-137` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 126-137 | 249 | in range |
| `ops/rank.mjs:136` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 136 | 249 | in range |
| `ops/rank.mjs:140` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 140 | 249 | in range |
| `ops/rank.mjs:141-142` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 141-142 | 249 | in range |
| `ops/rank.mjs:151` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 151 | 249 | in range |
| `ops/rank.mjs:161` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 161 | 249 | in range |
| `ops/rank.mjs:163` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 163 | 249 | in range |
| `ops/rank.mjs:164` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 164 | 249 | in range |
| `ops/rank.mjs:164-165` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 164-165 | 249 | in range |
| `ops/rank.mjs:175` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 175 | 249 | in range |
| `ops/rank.mjs:178` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 178 | 249 | in range |
| `ops/rank.mjs:179` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 179 | 249 | in range |
| `ops/rank.mjs:185` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 185 | 249 | in range |
| `ops/rank.mjs:200-204` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 200-204 | 249 | in range |
| `ops/rank.mjs:203` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 203 | 249 | in range |
| `ops/rank.mjs:209-219` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 209-219 | 249 | in range |
| `ops/rank.mjs:214` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 214 | 249 | in range |
| `ops/rank.mjs:216-219` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 216-219 | 249 | in range |
| `ops/rank.mjs:222` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 222 | 249 | in range |
| `ops/rank.mjs:223` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 223 | 249 | in range |
| `ops/rank.mjs:229` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 229 | 249 | in range |
| `ops/rank.mjs:231-235` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 231-235 | 249 | in range |
| `ops/rank.mjs:241` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 241 | 249 | in range |
| `ops/rank.mjs:247` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 247 | 249 | in range |
| `ops/rank.mjs:43` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 43 | 249 | in range |
| `ops/rank.mjs:46` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 46 | 249 | in range |
| `ops/rank.mjs:48-49` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 48-49 | 249 | in range |
| `ops/rank.mjs:53` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 53 | 249 | in range |
| `ops/rank.mjs:55-59` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 55-59 | 249 | in range |
| `ops/rank.mjs:56` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 56 | 249 | in range |
| `ops/rank.mjs:56-58` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 56-58 | 249 | in range |
| `ops/rank.mjs:57` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 57 | 249 | in range |
| `ops/rank.mjs:58` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 58 | 249 | in range |
| `ops/rank.mjs:63` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 63 | 249 | in range |
| `ops/rank.mjs:66-77` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 66-77 | 249 | in range |
| `ops/rank.mjs:92` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 92 | 249 | in range |
| `ops/rank.mjs:92-96` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 92-96 | 249 | in range |
| `ops/registry-check.mjs:117-118` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 117-118 | 190 | in range |
| `ops/registry-check.mjs:12` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 12 | 190 | in range |
| `ops/registry-check.mjs:121-122` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 121-122 | 190 | in range |
| `ops/registry-check.mjs:134-157` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 134-157 | 190 | in range |
| `ops/registry-check.mjs:159-170` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 159-170 | 190 | in range |
| `ops/registry-check.mjs:190` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 190 | 190 | in range |
| `ops/registry-check.mjs:34-43` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 34-43 | 190 | in range |
| `ops/registry-check.mjs:57-80` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 57-80 | 190 | in range |
| `ops/registry-check.mjs:70-72` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 70-72 | 190 | in range |
| `ops/registry-check.mjs:82-108` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 82-108 | 190 | in range |
| `ops/reroute-drill.mjs:10` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/reroute-drill.mjs` | 10 | 71 | in range |
| `ops/reroute-drill.mjs:2-3` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/reroute-drill.mjs` | 2-3 | 71 | in range |
| `ops/reroute-drill.mjs:20` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/reroute-drill.mjs` | 20 | 71 | in range |
| `ops/reroute-drill.mjs:44-57` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/reroute-drill.mjs` | 44-57 | 71 | in range |
| `ops/reroute-drill.mjs:60` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/reroute-drill.mjs` | 60 | 71 | in range |
| `ops/reroute-drill.mjs:63-69` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/reroute-drill.mjs` | 63-69 | 71 | in range |
| `ops/shared.mjs:11` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 11 | 41 | in range |
| `ops/shared.mjs:13-22` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 13-22 | 41 | in range |
| `ops/shared.mjs:25-31` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 25-31 | 41 | in range |
| `ops/shared.mjs:33-34` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 33-34 | 41 | in range |
| `ops/shared.mjs:36-41` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 36-41 | 41 | in range |
| `ops/shared.mjs:38` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 38 | 41 | in range |
| `ops/shared.mjs:39` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 39 | 41 | in range |
| `ops/shared.mjs:55` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 55 | 41 | OUT OF RANGE |
| `ops/shared.mjs:7` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 7 | 41 | in range |
| `ops/shared.mjs:8` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 8 | 41 | in range |
| `ops/sighting.sh:17` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/sighting.sh` | 17 | 36 | in range |
| `ops/sighting.sh:24` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/sighting.sh` | 24 | 36 | in range |
| `ops/sighting.sh:8` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/sighting.sh` | 8 | 36 | in range |
| `ops/validate.mjs:118` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 118 | 130 | in range |
| `ops/validate.mjs:119` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 119 | 130 | in range |
| `ops/validate.mjs:120-121` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 120-121 | 130 | in range |
| `ops/validate.mjs:125-130` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 125-130 | 130 | in range |
| `ops/validate.mjs:18` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 18 | 130 | in range |
| `ops/validate.mjs:27` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 27 | 130 | in range |
| `ops/validate.mjs:28` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 28 | 130 | in range |
| `ops/validate.mjs:56` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 56 | 130 | in range |
| `ops/validate.mjs:63-65` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 63-65 | 130 | in range |
| `ops/validate.mjs:72-73` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 72-73 | 130 | in range |
| `ops/validate.mjs:82` | MIRROR-EQUIVALENT | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 82 | 130 | in range |
| `~/Projects/origin-work/open-bug-bounties/claim-packages/submission-review/receipts/k8s-nodebound-token-impersonation.json:5-6` | RESOLVES | `/home/vgpnk/Projects/origin-work/open-bug-bounties/claim-packages/submission-review/receipts/k8s-nodebound-token-impersonation.json` | 5-6 | 11 | in range |

Every MIRROR-EQUIVALENT anchor in range is still only a *same-name same-path*
match against a Sep-5 genesis sync — see §Honest scope limits.

## Top-20 most-cited GONE paths

| # | citation | files citing | occurrences | noise flags |
|---|---|---|---|---|
| 1 | `claims/` | 21 | 35 | - |
| 2 | `status.json` | 19 | 42 | - |
| 3 | `george/` | 16 | 20 | - |
| 4 | `claim-check.mjs` | 14 | 28 | - |
| 5 | `evidence/` | 13 | 21 | - |
| 6 | `docs/claim-ready-index.md` | 13 | 17 | - |
| 7 | `fleets/run/` | 12 | 16 | - |
| 8 | `claims/*/*/status.json` | 11 | 16 | synthetic |
| 9 | `claim-index.mjs` | 11 | 13 | - |
| 10 | `ev-report.mjs` | 10 | 18 | - |
| 11 | `claim-ready/*` | 10 | 14 | synthetic |
| 12 | `~/Projects/bounties` | 10 | 12 | - |
| 13 | `claim-hold/*` | 9 | 22 | synthetic |
| 14 | `ledger/missions.jsonl` | 9 | 17 | - |
| 15 | `provenance.json` | 9 | 13 | - |
| 16 | `vdp-disclosures/` | 9 | 12 | - |
| 17 | `check-freshness.mjs` | 9 | 9 | - |
| 18 | `custodian-receipts.json` | 9 | 9 | - |
| 19 | `vgn-bounty-lab/` | 9 | 9 | - |
| 20 | `report.md` | 8 | 18 | - |

Max over all citations: files citing = 21, occurrences = 83.

## MIRROR-EQUIVALENT — exact list (220)

| # | citation | mirror path | lines | files | method |
|---|---|---|---|---|---|
| 1 | `README.md` | `/home/vgpnk/Projects/the-bounty-hunter/README.md` | 75 | 6 | literal |
| 2 | `README.md:19` | `/home/vgpnk/Projects/the-bounty-hunter/README.md` | 75 | 2 | literal |
| 3 | `README.md:23` | `/home/vgpnk/Projects/the-bounty-hunter/README.md` | 75 | 2 | literal |
| 4 | `README.md:30` | `/home/vgpnk/Projects/the-bounty-hunter/README.md` | 75 | 2 | literal |
| 5 | `bounty-*/` | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/` | - | 2 | glob |
| 6 | `bounty-map/` | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/` | - | 3 | literal |
| 7 | `bounty-map/schema.json` | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 68 | 7 | literal |
| 8 | `bounty-map/schema.json:32-52` | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 68 | 3 | literal |
| 9 | `bounty-map/schema.json:34` | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 68 | 3 | literal |
| 10 | `bounty-map/schema.json:35-51` | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 68 | 2 | literal |
| 11 | `bounty-map/schema.json:40` | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 68 | 2 | literal |
| 12 | `bounty-map/schema.json:46` | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 68 | 2 | literal |
| 13 | `bounty-map/schema.json:47` | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 68 | 2 | literal |
| 14 | `bounty-map/schema.json:48` | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 68 | 2 | literal |
| 15 | `docs/` | `/home/vgpnk/Projects/the-bounty-hunter/docs/` | - | 6 | literal |
| 16 | `docs/*` | `/home/vgpnk/Projects/the-bounty-hunter/docs/example-claim-ready-index.md` | 14 | 2 | glob |
| 17 | `docs/*.md` | `/home/vgpnk/Projects/the-bounty-hunter/docs/example-claim-ready-index.md` | 14 | 2 | glob |
| 18 | `docs/genesis-plan.md:15` | `/home/vgpnk/Projects/the-bounty-hunter/docs/genesis-plan.md` | 178 | 2 | literal |
| 19 | `docs/genesis-plan.md:17` | `/home/vgpnk/Projects/the-bounty-hunter/docs/genesis-plan.md` | 178 | 2 | literal |
| 20 | `fleets/` | `/home/vgpnk/Projects/the-bounty-hunter/fleets/` | - | 6 | literal |
| 21 | `fleets/*` | `/home/vgpnk/Projects/the-bounty-hunter/fleets/mission-template.md` | 64 | 2 | glob |
| 22 | `fleets/mission-template.md` | `/home/vgpnk/Projects/the-bounty-hunter/fleets/mission-template.md` | 64 | 6 | literal |
| 23 | `fleets/mission-template.md:20` | `/home/vgpnk/Projects/the-bounty-hunter/fleets/mission-template.md` | 64 | 3 | literal |
| 24 | `fleets/mission-template.md:50` | `/home/vgpnk/Projects/the-bounty-hunter/fleets/mission-template.md` | 64 | 3 | literal |
| 25 | `fleets/registry.json` | `/home/vgpnk/Projects/the-bounty-hunter/fleets/registry.json` | 135 | 15 | literal |
| 26 | `fleets/{mission-template.md,registry.json}` | `/home/vgpnk/Projects/the-bounty-hunter/fleets/mission-template.md` | 64 | 2 | brace |
| 27 | `ops/` | `/home/vgpnk/Projects/the-bounty-hunter/ops/` | - | 6 | literal |
| 28 | `ops/*.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 62 | 6 | glob |
| 29 | `ops/check-freshness.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 62 | 2 | literal |
| 30 | `ops/check-freshness.mjs:12` | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 62 | 2 | literal |
| 31 | `ops/check-freshness.mjs:14` | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 62 | 2 | literal |
| 32 | `ops/check-freshness.mjs:15` | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 62 | 2 | literal |
| 33 | `ops/check-freshness.mjs:43` | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 62 | 2 | literal |
| 34 | `ops/check-freshness.mjs:50` | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 62 | 2 | literal |
| 35 | `ops/check-freshness.mjs:59` | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 62 | 2 | literal |
| 36 | `ops/check-freshness.mjs:61` | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 62 | 2 | literal |
| 37 | `ops/claim-check.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/claim-check.mjs` | 83 | 13 | literal |
| 38 | `ops/claim-check.mjs:174-199` | `/home/vgpnk/Projects/the-bounty-hunter/ops/claim-check.mjs` | 83 | 2 | literal |
| 39 | `ops/claim-index.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/claim-index.mjs` | 49 | 5 | literal |
| 40 | `ops/claim-index.mjs:11` | `/home/vgpnk/Projects/the-bounty-hunter/ops/claim-index.mjs` | 49 | 2 | literal |
| 41 | `ops/claim-index.mjs:4` | `/home/vgpnk/Projects/the-bounty-hunter/ops/claim-index.mjs` | 49 | 2 | literal |
| 42 | `ops/ev-report.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 6 | literal |
| 43 | `ops/ev-report.mjs:16` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 44 | `ops/ev-report.mjs:17` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 3 | literal |
| 45 | `ops/ev-report.mjs:21` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 46 | `ops/ev-report.mjs:23-26` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 47 | `ops/ev-report.mjs:28-29` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 48 | `ops/ev-report.mjs:30-33` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 49 | `ops/ev-report.mjs:38-41` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 50 | `ops/ev-report.mjs:43` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 51 | `ops/ev-report.mjs:46` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 52 | `ops/ev-report.mjs:47` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 53 | `ops/ev-report.mjs:50` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 54 | `ops/ev-report.mjs:55` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 55 | `ops/ev-report.mjs:56` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 56 | `ops/ev-report.mjs:57` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 57 | `ops/ev-report.mjs:59-70` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 58 | `ops/ev-report.mjs:65` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 59 | `ops/ev-report.mjs:69` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 60 | `ops/ev-report.mjs:70` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 61 | `ops/ev-report.mjs:73` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 62 | `ops/ev-report.mjs:74` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 63 | `ops/ev-report.mjs:77` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 64 | `ops/ev-report.mjs:78` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 65 | `ops/ev-report.mjs:79-81` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 66 | `ops/ev-report.mjs:82` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 67 | `ops/ev-report.mjs:86-89` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 68 | `ops/ev-report.mjs:91` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 69 | `ops/ev-report.mjs:92` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 2 | literal |
| 70 | `ops/finalize-all.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/finalize-all.mjs` | 39 | 4 | literal |
| 71 | `ops/finalize-all.mjs:11` | `/home/vgpnk/Projects/the-bounty-hunter/ops/finalize-all.mjs` | 39 | 2 | literal |
| 72 | `ops/finalize-all.mjs:20` | `/home/vgpnk/Projects/the-bounty-hunter/ops/finalize-all.mjs` | 39 | 2 | literal |
| 73 | `ops/finalize-all.mjs:25` | `/home/vgpnk/Projects/the-bounty-hunter/ops/finalize-all.mjs` | 39 | 2 | literal |
| 74 | `ops/fleet-dispatch.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs` | 331 | 8 | literal |
| 75 | `ops/fleet-dispatch.mjs:11` | `/home/vgpnk/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs` | 331 | 2 | literal |
| 76 | `ops/fleet-dispatch.mjs:152` | `/home/vgpnk/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs` | 331 | 2 | literal |
| 77 | `ops/fleet-dispatch.mjs:155` | `/home/vgpnk/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs` | 331 | 2 | literal |
| 78 | `ops/fleet-dispatch.mjs:156` | `/home/vgpnk/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs` | 331 | 2 | literal |
| 79 | `ops/fleet-dispatch.mjs:21` | `/home/vgpnk/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs` | 331 | 2 | literal |
| 80 | `ops/import-board.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/import-board.mjs` | 258 | 3 | literal |
| 81 | `ops/import-board.mjs:132` | `/home/vgpnk/Projects/the-bounty-hunter/ops/import-board.mjs` | 258 | 2 | literal |
| 82 | `ops/import-board.mjs:30` | `/home/vgpnk/Projects/the-bounty-hunter/ops/import-board.mjs` | 258 | 2 | literal |
| 83 | `ops/park-disposition.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 6 | literal |
| 84 | `ops/park-disposition.mjs:12` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 85 | `ops/park-disposition.mjs:13` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 86 | `ops/park-disposition.mjs:14` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 87 | `ops/park-disposition.mjs:18` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 88 | `ops/park-disposition.mjs:18-21` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 89 | `ops/park-disposition.mjs:19` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 90 | `ops/park-disposition.mjs:21` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 91 | `ops/park-disposition.mjs:23-25` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 92 | `ops/park-disposition.mjs:28-32` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 93 | `ops/park-disposition.mjs:32` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 94 | `ops/park-disposition.mjs:36-39` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 95 | `ops/park-disposition.mjs:41` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 96 | `ops/park-disposition.mjs:43` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 97 | `ops/park-disposition.mjs:45-49` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 98 | `ops/park-disposition.mjs:52` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 99 | `ops/park-disposition.mjs:53` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 100 | `ops/park-disposition.mjs:53-74` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 101 | `ops/park-disposition.mjs:56` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 102 | `ops/park-disposition.mjs:56-59` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 103 | `ops/park-disposition.mjs:59` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 104 | `ops/park-disposition.mjs:61` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 105 | `ops/park-disposition.mjs:61-65` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 106 | `ops/park-disposition.mjs:62-65` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 107 | `ops/park-disposition.mjs:67-70` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 108 | `ops/park-disposition.mjs:70` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 109 | `ops/park-disposition.mjs:72-73` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 110 | `ops/park-disposition.mjs:75-77` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 111 | `ops/park-disposition.mjs:78` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 2 | literal |
| 112 | `ops/rank.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 4 | literal |
| 113 | `ops/rank.mjs:104` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 114 | `ops/rank.mjs:105-108` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 115 | `ops/rank.mjs:118-119` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 116 | `ops/rank.mjs:123` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 117 | `ops/rank.mjs:126-137` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 118 | `ops/rank.mjs:136` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 119 | `ops/rank.mjs:140` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 120 | `ops/rank.mjs:141-142` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 121 | `ops/rank.mjs:151` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 122 | `ops/rank.mjs:161` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 123 | `ops/rank.mjs:163` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 124 | `ops/rank.mjs:164` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 125 | `ops/rank.mjs:164-165` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 126 | `ops/rank.mjs:175` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 127 | `ops/rank.mjs:178` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 128 | `ops/rank.mjs:179` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 129 | `ops/rank.mjs:185` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 130 | `ops/rank.mjs:200-204` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 131 | `ops/rank.mjs:203` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 132 | `ops/rank.mjs:209-219` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 133 | `ops/rank.mjs:214` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 134 | `ops/rank.mjs:216-219` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 135 | `ops/rank.mjs:222` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 136 | `ops/rank.mjs:223` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 137 | `ops/rank.mjs:229` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 138 | `ops/rank.mjs:231-235` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 139 | `ops/rank.mjs:241` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 140 | `ops/rank.mjs:247` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 141 | `ops/rank.mjs:43` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 142 | `ops/rank.mjs:46` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 143 | `ops/rank.mjs:48-49` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 144 | `ops/rank.mjs:53` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 145 | `ops/rank.mjs:55-59` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 146 | `ops/rank.mjs:56` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 147 | `ops/rank.mjs:56-58` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 148 | `ops/rank.mjs:57` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 149 | `ops/rank.mjs:58` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 150 | `ops/rank.mjs:63` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 151 | `ops/rank.mjs:66-77` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 152 | `ops/rank.mjs:92` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 153 | `ops/rank.mjs:92-96` | `/home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs` | 249 | 2 | literal |
| 154 | `ops/registry-check.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 190 | 3 | literal |
| 155 | `ops/registry-check.mjs:117-118` | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 190 | 2 | literal |
| 156 | `ops/registry-check.mjs:12` | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 190 | 2 | literal |
| 157 | `ops/registry-check.mjs:121-122` | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 190 | 2 | literal |
| 158 | `ops/registry-check.mjs:134-157` | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 190 | 2 | literal |
| 159 | `ops/registry-check.mjs:159-170` | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 190 | 2 | literal |
| 160 | `ops/registry-check.mjs:190` | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 190 | 2 | literal |
| 161 | `ops/registry-check.mjs:34-43` | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 190 | 2 | literal |
| 162 | `ops/registry-check.mjs:57-80` | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 190 | 2 | literal |
| 163 | `ops/registry-check.mjs:70-72` | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 190 | 2 | literal |
| 164 | `ops/registry-check.mjs:82-108` | `/home/vgpnk/Projects/the-bounty-hunter/ops/registry-check.mjs` | 190 | 2 | literal |
| 165 | `ops/reroute-drill.mjs:10` | `/home/vgpnk/Projects/the-bounty-hunter/ops/reroute-drill.mjs` | 71 | 2 | literal |
| 166 | `ops/reroute-drill.mjs:2-3` | `/home/vgpnk/Projects/the-bounty-hunter/ops/reroute-drill.mjs` | 71 | 2 | literal |
| 167 | `ops/reroute-drill.mjs:20` | `/home/vgpnk/Projects/the-bounty-hunter/ops/reroute-drill.mjs` | 71 | 2 | literal |
| 168 | `ops/reroute-drill.mjs:44-57` | `/home/vgpnk/Projects/the-bounty-hunter/ops/reroute-drill.mjs` | 71 | 2 | literal |
| 169 | `ops/reroute-drill.mjs:60` | `/home/vgpnk/Projects/the-bounty-hunter/ops/reroute-drill.mjs` | 71 | 2 | literal |
| 170 | `ops/reroute-drill.mjs:63-69` | `/home/vgpnk/Projects/the-bounty-hunter/ops/reroute-drill.mjs` | 71 | 2 | literal |
| 171 | `ops/shared.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 5 | literal |
| 172 | `ops/shared.mjs:11` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 2 | literal |
| 173 | `ops/shared.mjs:13-22` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 3 | literal |
| 174 | `ops/shared.mjs:25-31` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 2 | literal |
| 175 | `ops/shared.mjs:33-34` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 2 | literal |
| 176 | `ops/shared.mjs:36-41` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 3 | literal |
| 177 | `ops/shared.mjs:38` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 2 | literal |
| 178 | `ops/shared.mjs:39` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 2 | literal |
| 179 | `ops/shared.mjs:55` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 4 | literal |
| 180 | `ops/shared.mjs:7` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 2 | literal |
| 181 | `ops/shared.mjs:8` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 2 | literal |
| 182 | `ops/shared.mjs::TELEMETRY_EVENTS` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 2 | literal |
| 183 | `ops/shared.mjs::appendLedger` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 2 | literal |
| 184 | `ops/shared.mjs::gitMutationBlocker` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 2 | literal |
| 185 | `ops/sighting*.sh` | `/home/vgpnk/Projects/the-bounty-hunter/ops/sighting-board.sh` | 20 | 3 | glob |
| 186 | `ops/sighting.sh` | `/home/vgpnk/Projects/the-bounty-hunter/ops/sighting.sh` | 36 | 2 | literal |
| 187 | `ops/sighting.sh:17` | `/home/vgpnk/Projects/the-bounty-hunter/ops/sighting.sh` | 36 | 2 | literal |
| 188 | `ops/sighting.sh:24` | `/home/vgpnk/Projects/the-bounty-hunter/ops/sighting.sh` | 36 | 2 | literal |
| 189 | `ops/sighting.sh:8` | `/home/vgpnk/Projects/the-bounty-hunter/ops/sighting.sh` | 36 | 2 | literal |
| 190 | `ops/validate.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 130 | 4 | literal |
| 191 | `ops/validate.mjs:118` | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 130 | 2 | literal |
| 192 | `ops/validate.mjs:119` | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 130 | 2 | literal |
| 193 | `ops/validate.mjs:120-121` | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 130 | 2 | literal |
| 194 | `ops/validate.mjs:125-130` | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 130 | 2 | literal |
| 195 | `ops/validate.mjs:18` | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 130 | 2 | literal |
| 196 | `ops/validate.mjs:27` | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 130 | 2 | literal |
| 197 | `ops/validate.mjs:28` | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 130 | 2 | literal |
| 198 | `ops/validate.mjs:56` | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 130 | 2 | literal |
| 199 | `ops/validate.mjs:63-65` | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 130 | 2 | literal |
| 200 | `ops/validate.mjs:72-73` | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 130 | 2 | literal |
| 201 | `ops/validate.mjs:82` | `/home/vgpnk/Projects/the-bounty-hunter/ops/validate.mjs` | 130 | 2 | literal |
| 202 | `ops/{validate,registry-check,check-freshness,reroute-drill,finalize-all,import-board,claim-index}.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 62 | 2 | brace |
| 203 | `~/Projects/bounties/.git/` | `/home/vgpnk/Projects/the-bounty-hunter/.git/` | - | 2 | literal |
| 204 | `~/Projects/bounties/.omp/{config.yml,agents/,skills/}` | `/home/vgpnk/Projects/the-bounty-hunter/.omp/agents/` | - | 2 | brace |
| 205 | `~/Projects/bounties/bounty-map/schema.json` | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 68 | 3 | literal |
| 206 | `~/Projects/bounties/bounty-map/{schema.json,programs/*.json}` | `/home/vgpnk/Projects/the-bounty-hunter/bounty-map/schema.json` | 68 | 2 | brace |
| 207 | `~/Projects/bounties/fleets/mission-template.md` | `/home/vgpnk/Projects/the-bounty-hunter/fleets/mission-template.md` | 64 | 4 | literal |
| 208 | `~/Projects/bounties/fleets/registry.json` | `/home/vgpnk/Projects/the-bounty-hunter/fleets/registry.json` | 135 | 2 | literal |
| 209 | `~/Projects/bounties/ops/claim-check.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/claim-check.mjs` | 83 | 3 | literal |
| 210 | `~/Projects/bounties/ops/ev-report.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/ev-report.mjs` | 92 | 3 | literal |
| 211 | `~/Projects/bounties/ops/fleet-dispatch.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs` | 331 | 4 | literal |
| 212 | `~/Projects/bounties/ops/import-board.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/import-board.mjs` | 258 | 2 | literal |
| 213 | `~/Projects/bounties/ops/park-disposition.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/park-disposition.mjs` | 80 | 3 | literal |
| 214 | `~/Projects/bounties/ops/shared.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/shared.mjs` | 41 | 3 | literal |
| 215 | `~/Projects/bounties/ops/sighting{,-board,-dispatcher,-missions}.sh` | `/home/vgpnk/Projects/the-bounty-hunter/ops/sighting-board.sh` | 20 | 2 | brace |
| 216 | `~/Projects/bounties/ops/{claim-check,claim-index,prepare-claims,ev-report}.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/claim-check.mjs` | 83 | 2 | brace |
| 217 | `~/Projects/bounties/ops/{claim-check,ev-report,fleet-dispatch,shared}.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/claim-check.mjs` | 83 | 2 | brace |
| 218 | `~/Projects/bounties/ops/{import-board,finalize-all}.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/finalize-all.mjs` | 39 | 2 | brace |
| 219 | `~/Projects/bounties/ops/{validate,registry-check,reroute-drill,check-freshness}.mjs` | `/home/vgpnk/Projects/the-bounty-hunter/ops/check-freshness.mjs` | 62 | 2 | brace |
| 220 | `~/Projects/bounties/{README.md,.gitignore}` | `/home/vgpnk/Projects/the-bounty-hunter/README.md` | 75 | 2 | brace |
