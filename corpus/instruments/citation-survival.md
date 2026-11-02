# citation-survival census — kasegi lane

Instrument: `corpus/instruments/resolve.py` (stdlib-only, deterministic; r18 definition).
Lane root: `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi`
Scope: `SKILL.md` + `corpus/**/*.md` (234 files).
Extraction: verbatim density.py docstring path-like rule (see module docstring).
Mirror root for bounty-path equivalence: `/home/agent/Projects/the-bounty-hunter` (ABSENT — mirror fallback disabled).

## Totals

- distinct path-like citations: **5161** (total occurrences: 11806; a citation cited in both scopes counts once)
- distinct citations appearing in SKILL.md: 717 (of which SKILL-only: 8)
- distinct citations appearing in corpus: 5153

| class | distinct citations |
|---|---|
| RESOLVES | 9 |
| MIRROR-EQUIVALENT | 0 |
| GONE | 3998 |
| INTERNAL | 1154 |
| OTHER *(root-domain bucket, orthogonal: the brief says classify other roots as RESOLVES/GONE)* | 9 resolve / 214 gone = 223 |

Terminal outcome classes sum to the distinct total: RESOLVES(9) + MIRROR-EQUIVALENT(0) + INTERNAL(1154) + GONE(3998) = 5161.
Of the 9 RESOLVES, 9 are non-lane roots (domain `other`: origin-work, /tmp, ~/projects …); 0 are lane-repo-absolute.
Of the 0 MIRROR-EQUIVALENT, 0 were written as `~/Projects/bounties/...` (domain `bounty`), 0 were bounty-root-relative bare paths (domain `rel`).

## Resolvability rate

Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citations appearing in that scope (a citation in both scopes enters both denominators).

- SKILL.md alone: **140/717 = 19.53%**
- corpus alone: **1157/5153 = 22.45%**
- lane total (SKILL.md + corpus): **1163/5161 = 22.53%**

## Noise sub-census (GONE tokens that are rule artifacts, not citable paths)

Flag counts (a token can carry several flags):

| flags | distinct GONE citations |
|---|---|
| gitstatus | 8 |
| gitstatus,synthetic | 9 |
| regex | 22 |
| regex,synthetic | 7 |
| shell | 426 |
| shell,synthetic | 188 |
| synthetic | 617 |

- GONE citations carrying any noise flag: 1277
- GONE citations with no noise flag (genuine vanished paths): 2721
- citations containing glob/placeholder syntax (`* ? [ { } <...>`): 880

Noise-adjusted rates (denominator excludes noise-flagged citations):
- SKILL: 138/358 = 38.55%
- CORPUS: 1098/3819 = 28.75%
- ALL: 1104/3825 = 28.86%

## Scope x class matrix

| class | SKILL.md only | SKILL+corpus | corpus only | total |
|---|---|---|---|---|
| RESOLVES | 0 | 2 | 7 | 9 |
| MIRROR-EQUIVALENT | 0 | 0 | 0 | 0 |
| GONE | 2 | 575 | 3421 | 3998 |
| INTERNAL | 6 | 132 | 1016 | 1154 |

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

Result: both yield **5161** distinct citations, and
`diff <(pipeline to file) <(cut -f1 citation-survival.tsv | tail -n +2 | sort -u)` is empty (sets identical, not just counts).
Re-running `resolve.py` twice leaves both outputs byte-identical (md5 stable).

## Honest scope limits

- MIRROR-EQUIVALENT means the same relative path exists in the Sep-5 genesis mirror `~/Projects/the-bounty-hunter`; it does NOT establish byte-equivalence with the vanished tree, and the mirror holds the code half only.
- Glob/brace citations resolve if any deterministic expansion exists; a glob with zero matches is GONE (e.g. `bounty-map/programs/*.json`).
- The path-like rule (verbatim from density.py) admits regex literals, git-porcelain snippets and shell fragments; the noise sub-census quantifies them so the raw rate can be read against the noise-adjusted rate.

## Line-anchor viability (resolvable citations carrying `:NN` / `:NN-MM`)

For every citation whose base resolves and whose anchor names a file, the anchor
is compared against the resolved file's line count (editor convention).

- anchors checked: 469 — in range: 450 — **out of range: 19**

| citation | class | resolved file | anchor | file lines | verdict |
|---|---|---|---|---|---|
| `./PROVINCE.md:3` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/./PROVINCE.md` | 3 | 219 | in range |
| `.gitignore:11` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.gitignore` | 11 | 2 | OUT OF RANGE |
| `.gitignore:7` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.gitignore` | 7 | 2 | OUT OF RANGE |
| `.gitignore:8-9` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.gitignore` | 8-9 | 2 | OUT OF RANGE |
| `.ufo/waves/round-24/wave1/LivenessMatrix.md:200-201` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-24/wave1/LivenessMatrix.md` | 200-201 | 238 | in range |
| `.ufo/waves/round-31/wave1/CritC2Kill.md:232` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-31/wave1/CritC2Kill.md` | 232 | 309 | in range |
| `.ufo/waves/round-33/claims-erratum-1.md:1-36` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-33/claims-erratum-1.md` | 1-36 | 36 | in range |
| `.ufo/waves/round-34/mistakes-erratum-1.md:18-20` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-34/mistakes-erratum-1.md` | 18-20 | 66 | in range |
| `.ufo/waves/round-34/mistakes-erratum-1.md:9-29` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-34/mistakes-erratum-1.md` | 9-29 | 66 | in range |
| `.ufo/waves/round-34/wave1/ExecCaptureBindingHarden.md:505-507` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-34/wave1/ExecCaptureBindingHarden.md` | 505-507 | 512 | in range |
| `.ufo/waves/round-34/wave1/MutSelftestSummary.md:332` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-34/wave1/MutSelftestSummary.md` | 332 | 373 | in range |
| `.ufo/waves/round-35/claims.json:6` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-35/claims.json` | 6 | 87 | in range |
| `.ufo/waves/round-36/build-spec.py:123` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-36/build-spec.py` | 123 | 286 | in range |
| `.ufo/waves/round-37/final-gates/all-gates.txt:2` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-37/final-gates/all-gates.txt` | 2 | 121 | in range |
| `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md:56` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md` | 56 | 173 | in range |
| `.ufo/waves/round-38/final-gates/all-gates.txt:15` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-38/final-gates/all-gates.txt` | 15 | 79 | in range |
| `.ufo/waves/round-38/final-gates/all-gates.txt:2` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-38/final-gates/all-gates.txt` | 2 | 79 | in range |
| `.ufo/waves/round-38/wave1/RevPendingResolutions.md:48` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-38/wave1/RevPendingResolutions.md` | 48 | 101 | in range |
| `.ufo/waves/round-38/wave1/RevPendingResolutions.md:49` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-38/wave1/RevPendingResolutions.md` | 49 | 101 | in range |
| `.ufo/waves/round-42/c1-controls/do-nothing.txt:16` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-42/c1-controls/do-nothing.txt` | 16 | 18 | in range |
| `.ufo/waves/round-42/claims-erratum-3.md:3` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-42/claims-erratum-3.md` | 3 | 3 | in range |
| `.ufo/waves/round-42/claims-erratum-4.md:9` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-42/claims-erratum-4.md` | 9 | 48 | in range |
| `.ufo/waves/round-43/final-gates/r42-at-de09313-run.txt:2` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-43/final-gates/r42-at-de09313-run.txt` | 2 | 19 | in range |
| `.ufo/waves/round-43/w1-REGISTRY.txt:7` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-43/w1-REGISTRY.txt` | 7 | 7 | in range |
| `.ufo/waves/round-45/source-recon/S072.txt:148-149` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-45/source-recon/S072.txt` | 148-149 | 312 | in range |
| `.ufo/waves/round-46/attempt2/freeze.txt:7` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-46/attempt2/freeze.txt` | 7 | 11 | in range |
| `.ufo/waves/round-46/freeze.txt:7` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-46/freeze.txt` | 7 | 8 | in range |
| `.ufo/waves/round-46/wave1/R46SentinelContent.md:13` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-46/wave1/R46SentinelContent.md` | 13 | 99 | in range |
| `.ufo/waves/round-53/controls/c2-counter-final-r53.txt:9` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-53/controls/c2-counter-final-r53.txt` | 9 | 10 | in range |
| `.ufo/waves/round-54/claims.json:14` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.ufo/waves/round-54/claims.json` | 14 | 46 | in range |
| `LOG.md:1469` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 1469 | 2663 | in range |
| `LOG.md:1550` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 1550 | 2663 | in range |
| `LOG.md:1584` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 1584 | 2663 | in range |
| `LOG.md:1665` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 1665 | 2663 | in range |
| `LOG.md:1686` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 1686 | 2663 | in range |
| `LOG.md:1728` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 1728 | 2663 | in range |
| `LOG.md:1800-1801` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 1800-1801 | 2663 | in range |
| `LOG.md:1804` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 1804 | 2663 | in range |
| `LOG.md:2045` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 2045 | 2663 | in range |
| `LOG.md:2205` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 2205 | 2663 | in range |
| `LOG.md:545` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 545 | 2663 | in range |
| `LOG.md:709-713` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 709-713 | 2663 | in range |
| `LOG.md:734` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 734 | 2663 | in range |
| `LOG.md:747-750` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 747-750 | 2663 | in range |
| `LOG.md:812` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/LOG.md` | 812 | 2663 | in range |
| `PROVINCE.md:16-22` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/PROVINCE.md` | 16-22 | 219 | in range |
| `PROVINCE.md:165` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/PROVINCE.md` | 165 | 219 | in range |
| `PROVINCE.md:171` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/PROVINCE.md` | 171 | 219 | in range |
| `PROVINCE.md:31-40` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/PROVINCE.md` | 31-40 | 219 | in range |
| `PROVINCE.md:38` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/PROVINCE.md` | 38 | 219 | in range |
| `PROVINCE.md:75` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/PROVINCE.md` | 75 | 219 | in range |
| `PROVINCE.md:77` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/PROVINCE.md` | 77 | 219 | in range |
| `PROVINCE.md:78` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/PROVINCE.md` | 78 | 219 | in range |
| `PROVINCE.md:80-152` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/PROVINCE.md` | 80-152 | 219 | in range |
| `PROVINCE.md:90` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/PROVINCE.md` | 90 | 219 | in range |
| `README.md:159` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/README.md` | 159 | 14 | OUT OF RANGE |
| `README.md:19` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/README.md` | 19 | 14 | OUT OF RANGE |
| `README.md:213` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/README.md` | 213 | 14 | OUT OF RANGE |
| `README.md:23` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/README.md` | 23 | 14 | OUT OF RANGE |
| `README.md:30` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/README.md` | 30 | 14 | OUT OF RANGE |
| `SCORECARD.md:1014-1027` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1014-1027 | 2446 | in range |
| `SCORECARD.md:1014-1035` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1014-1035 | 2446 | in range |
| `SCORECARD.md:1074` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1074 | 2446 | in range |
| `SCORECARD.md:1078` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1078 | 2446 | in range |
| `SCORECARD.md:1116` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1116 | 2446 | in range |
| `SCORECARD.md:1116-1119` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1116-1119 | 2446 | in range |
| `SCORECARD.md:1129` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1129 | 2446 | in range |
| `SCORECARD.md:1145` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1145 | 2446 | in range |
| `SCORECARD.md:121-149` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 121-149 | 2446 | in range |
| `SCORECARD.md:1240` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1240 | 2446 | in range |
| `SCORECARD.md:1263-1281` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1263-1281 | 2446 | in range |
| `SCORECARD.md:1269` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1269 | 2446 | in range |
| `SCORECARD.md:1271` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1271 | 2446 | in range |
| `SCORECARD.md:1284` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1284 | 2446 | in range |
| `SCORECARD.md:134` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 134 | 2446 | in range |
| `SCORECARD.md:1492` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1492 | 2446 | in range |
| `SCORECARD.md:1505` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1505 | 2446 | in range |
| `SCORECARD.md:1509` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1509 | 2446 | in range |
| `SCORECARD.md:1532` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1532 | 2446 | in range |
| `SCORECARD.md:1547` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1547 | 2446 | in range |
| `SCORECARD.md:1567` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1567 | 2446 | in range |
| `SCORECARD.md:1595` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1595 | 2446 | in range |
| `SCORECARD.md:1602` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1602 | 2446 | in range |
| `SCORECARD.md:1602-1605` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1602-1605 | 2446 | in range |
| `SCORECARD.md:1605` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1605 | 2446 | in range |
| `SCORECARD.md:1634` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1634 | 2446 | in range |
| `SCORECARD.md:164` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 164 | 2446 | in range |
| `SCORECARD.md:174` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 174 | 2446 | in range |
| `SCORECARD.md:1788` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 1788 | 2446 | in range |
| `SCORECARD.md:228-290` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 228-290 | 2446 | in range |
| `SCORECARD.md:23` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 23 | 2446 | in range |
| `SCORECARD.md:251` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 251 | 2446 | in range |
| `SCORECARD.md:252` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 252 | 2446 | in range |
| `SCORECARD.md:259-270` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 259-270 | 2446 | in range |
| `SCORECARD.md:309` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 309 | 2446 | in range |
| `SCORECARD.md:309-321` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 309-321 | 2446 | in range |
| `SCORECARD.md:327` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 327 | 2446 | in range |
| `SCORECARD.md:331` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 331 | 2446 | in range |
| `SCORECARD.md:49-58` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 49-58 | 2446 | in range |
| `SCORECARD.md:502` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 502 | 2446 | in range |
| `SCORECARD.md:510` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 510 | 2446 | in range |
| `SCORECARD.md:65` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 65 | 2446 | in range |
| `SCORECARD.md:813` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 813 | 2446 | in range |
| `SCORECARD.md:813-819` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 813-819 | 2446 | in range |
| `SCORECARD.md:837` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 837 | 2446 | in range |
| `SCORECARD.md:88-96` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 88-96 | 2446 | in range |
| `SCORECARD.md:988` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SCORECARD.md` | 988 | 2446 | in range |
| `SHONEN.md:164-165` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SHONEN.md` | 164-165 | 12 | OUT OF RANGE |
| `SHONEN.md:164-166` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SHONEN.md` | 164-166 | 12 | OUT OF RANGE |
| `SHONEN.md:172` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SHONEN.md` | 172 | 12 | OUT OF RANGE |
| `SHONEN.md:173-174` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SHONEN.md` | 173-174 | 12 | OUT OF RANGE |
| `SHONEN.md:182-183` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SHONEN.md` | 182-183 | 12 | OUT OF RANGE |
| `SHONEN.md:185` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SHONEN.md` | 185 | 12 | OUT OF RANGE |
| `SHONEN.md:212-213` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SHONEN.md` | 212-213 | 12 | OUT OF RANGE |
| `SHONEN.md:249-256` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SHONEN.md` | 249-256 | 12 | OUT OF RANGE |
| `SHONEN.md:310` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SHONEN.md` | 310 | 12 | OUT OF RANGE |
| `SHONEN.md:311` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SHONEN.md` | 311 | 12 | OUT OF RANGE |
| `SHONEN.md:34` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SHONEN.md` | 34 | 12 | OUT OF RANGE |
| `SKILL.md:10` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 10 | 1320 | in range |
| `SKILL.md:10-11` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 10-11 | 1320 | in range |
| `SKILL.md:1000` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 1000 | 1320 | in range |
| `SKILL.md:1069` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 1069 | 1320 | in range |
| `SKILL.md:1091` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 1091 | 1320 | in range |
| `SKILL.md:1093-1104` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 1093-1104 | 1320 | in range |
| `SKILL.md:1097` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 1097 | 1320 | in range |
| `SKILL.md:1097-1098` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 1097-1098 | 1320 | in range |
| `SKILL.md:1100` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 1100 | 1320 | in range |
| `SKILL.md:111` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 111 | 1320 | in range |
| `SKILL.md:111-112` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 111-112 | 1320 | in range |
| `SKILL.md:1111` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 1111 | 1320 | in range |
| `SKILL.md:1115` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 1115 | 1320 | in range |
| `SKILL.md:113-114` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 113-114 | 1320 | in range |
| `SKILL.md:113-117` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 113-117 | 1320 | in range |
| `SKILL.md:115` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 115 | 1320 | in range |
| `SKILL.md:1163` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 1163 | 1320 | in range |
| `SKILL.md:117` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 117 | 1320 | in range |
| `SKILL.md:14-15` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 14-15 | 1320 | in range |
| `SKILL.md:146` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 146 | 1320 | in range |
| `SKILL.md:148` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 148 | 1320 | in range |
| `SKILL.md:149` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 149 | 1320 | in range |
| `SKILL.md:175` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 175 | 1320 | in range |
| `SKILL.md:175-176` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 175-176 | 1320 | in range |
| `SKILL.md:245-247` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 245-247 | 1320 | in range |
| `SKILL.md:246` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 246 | 1320 | in range |
| `SKILL.md:323` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 323 | 1320 | in range |
| `SKILL.md:385` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 385 | 1320 | in range |
| `SKILL.md:413` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 413 | 1320 | in range |
| `SKILL.md:459` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 459 | 1320 | in range |
| `SKILL.md:494-506` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 494-506 | 1320 | in range |
| `SKILL.md:498` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 498 | 1320 | in range |
| `SKILL.md:499` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 499 | 1320 | in range |
| `SKILL.md:500-501` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 500-501 | 1320 | in range |
| `SKILL.md:502` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 502 | 1320 | in range |
| `SKILL.md:522` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 522 | 1320 | in range |
| `SKILL.md:525` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 525 | 1320 | in range |
| `SKILL.md:526` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 526 | 1320 | in range |
| `SKILL.md:590-596` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 590-596 | 1320 | in range |
| `SKILL.md:597-608` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 597-608 | 1320 | in range |
| `SKILL.md:609-614` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 609-614 | 1320 | in range |
| `SKILL.md:615-621` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 615-621 | 1320 | in range |
| `SKILL.md:622-635` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 622-635 | 1320 | in range |
| `SKILL.md:636-639` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 636-639 | 1320 | in range |
| `SKILL.md:640-643` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 640-643 | 1320 | in range |
| `SKILL.md:644-651` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 644-651 | 1320 | in range |
| `SKILL.md:652-664` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 652-664 | 1320 | in range |
| `SKILL.md:665-679` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 665-679 | 1320 | in range |
| `SKILL.md:8` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 8 | 1320 | in range |
| `SKILL.md:86` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 86 | 1320 | in range |
| `SKILL.md:90-91` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 90-91 | 1320 | in range |
| `SKILL.md:94-95` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/SKILL.md` | 94-95 | 1320 | in range |
| `considerthese/2026-10-25.md:53-57` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/considerthese/2026-10-25.md` | 53-57 | 77 | in range |
| `considerthese/2026-10-25.md:76` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/considerthese/2026-10-25.md` | 76 | 77 | in range |
| `considerthese/2026-10-26.md:30` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/considerthese/2026-10-26.md` | 30 | 35 | in range |
| `considerthese/2026-10-26.md:31` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/considerthese/2026-10-26.md` | 31 | 35 | in range |
| `considerthese/2026-10-26.md:35` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/considerthese/2026-10-26.md` | 35 | 35 | in range |
| `corpus/QUALITY.md:169` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 169 | 452 | in range |
| `corpus/QUALITY.md:220-222` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 220-222 | 452 | in range |
| `corpus/QUALITY.md:226` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 226 | 452 | in range |
| `corpus/QUALITY.md:227` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 227 | 452 | in range |
| `corpus/QUALITY.md:229` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 229 | 452 | in range |
| `corpus/QUALITY.md:249` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 249 | 452 | in range |
| `corpus/QUALITY.md:263` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 263 | 452 | in range |
| `corpus/QUALITY.md:278` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 278 | 452 | in range |
| `corpus/QUALITY.md:292` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 292 | 452 | in range |
| `corpus/QUALITY.md:35-36` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 35-36 | 452 | in range |
| `corpus/QUALITY.md:391` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 391 | 452 | in range |
| `corpus/QUALITY.md:401` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 401 | 452 | in range |
| `corpus/QUALITY.md:407` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 407 | 452 | in range |
| `corpus/QUALITY.md:413-416` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 413-416 | 452 | in range |
| `corpus/QUALITY.md:77` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 77 | 452 | in range |
| `corpus/QUALITY.md:83` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 83 | 452 | in range |
| `corpus/QUALITY.md:89` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 89 | 452 | in range |
| `corpus/QUALITY.md:95` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/QUALITY.md` | 95 | 452 | in range |
| `corpus/README.md:145` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 145 | 941 | in range |
| `corpus/README.md:168` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 168 | 941 | in range |
| `corpus/README.md:200` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 200 | 941 | in range |
| `corpus/README.md:207` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 207 | 941 | in range |
| `corpus/README.md:208` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 208 | 941 | in range |
| `corpus/README.md:210` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 210 | 941 | in range |
| `corpus/README.md:211` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 211 | 941 | in range |
| `corpus/README.md:309` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 309 | 941 | in range |
| `corpus/README.md:361` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 361 | 941 | in range |
| `corpus/README.md:448` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 448 | 941 | in range |
| `corpus/README.md:49` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 49 | 941 | in range |
| `corpus/README.md:54` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 54 | 941 | in range |
| `corpus/README.md:591` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 591 | 941 | in range |
| `corpus/README.md:702` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 702 | 941 | in range |
| `corpus/README.md:82` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/README.md` | 82 | 941 | in range |
| `corpus/SOURCES.md:137` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 137 | 221 | in range |
| `corpus/SOURCES.md:142` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 142 | 221 | in range |
| `corpus/SOURCES.md:157` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 157 | 221 | in range |
| `corpus/SOURCES.md:22` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 22 | 221 | in range |
| `corpus/SOURCES.md:40` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 40 | 221 | in range |
| `corpus/SOURCES.md:47` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 47 | 221 | in range |
| `corpus/SOURCES.md:48` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 48 | 221 | in range |
| `corpus/SOURCES.md:54` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 54 | 221 | in range |
| `corpus/SOURCES.md:55-56` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 55-56 | 221 | in range |
| `corpus/SOURCES.md:56` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 56 | 221 | in range |
| `corpus/SOURCES.md:57` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 57 | 221 | in range |
| `corpus/SOURCES.md:58` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 58 | 221 | in range |
| `corpus/SOURCES.md:61` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 61 | 221 | in range |
| `corpus/SOURCES.md:62` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 62 | 221 | in range |
| `corpus/SOURCES.md:62-65` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 62-65 | 221 | in range |
| `corpus/SOURCES.md:74` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 74 | 221 | in range |
| `corpus/SOURCES.md:79` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 79 | 221 | in range |
| `corpus/SOURCES.md:82` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 82 | 221 | in range |
| `corpus/SOURCES.md:83` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 83 | 221 | in range |
| `corpus/SOURCES.md:90` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/SOURCES.md` | 90 | 221 | in range |
| `corpus/instruments/README.md:1000` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/README.md` | 1000 | 1053 | in range |
| `corpus/instruments/README.md:131` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/README.md` | 131 | 1053 | in range |
| `corpus/instruments/README.md:16-17` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/README.md` | 16-17 | 1053 | in range |
| `corpus/instruments/README.md:31-38` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/README.md` | 31-38 | 1053 | in range |
| `corpus/instruments/README.md:63` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/README.md` | 63 | 1053 | in range |
| `corpus/instruments/capture-binding-check.py:1-92` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/capture-binding-check.py` | 1-92 | 1129 | in range |
| `corpus/instruments/capture-binding-check.py:166-181` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/capture-binding-check.py` | 166-181 | 1129 | in range |
| `corpus/instruments/capture-binding-check.py:184-262` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/capture-binding-check.py` | 184-262 | 1129 | in range |
| `corpus/instruments/capture-binding-check.py:67-68` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/capture-binding-check.py` | 67-68 | 1129 | in range |
| `corpus/instruments/capture-binding-check.py:80` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/capture-binding-check.py` | 80 | 1129 | in range |
| `corpus/instruments/claim-package-check.py:101-108` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 101-108 | 802 | in range |
| `corpus/instruments/claim-package-check.py:120` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 120 | 802 | in range |
| `corpus/instruments/claim-package-check.py:121` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 121 | 802 | in range |
| `corpus/instruments/claim-package-check.py:138-140` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 138-140 | 802 | in range |
| `corpus/instruments/claim-package-check.py:185-187` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 185-187 | 802 | in range |
| `corpus/instruments/claim-package-check.py:2-8` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 2-8 | 802 | in range |
| `corpus/instruments/claim-package-check.py:305` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 305 | 802 | in range |
| `corpus/instruments/claim-package-check.py:307-309` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 307-309 | 802 | in range |
| `corpus/instruments/claim-package-check.py:332-335` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 332-335 | 802 | in range |
| `corpus/instruments/claim-package-check.py:334` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 334 | 802 | in range |
| `corpus/instruments/claim-package-check.py:340-347` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 340-347 | 802 | in range |
| `corpus/instruments/claim-package-check.py:354` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 354 | 802 | in range |
| `corpus/instruments/claim-package-check.py:354-355` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 354-355 | 802 | in range |
| `corpus/instruments/claim-package-check.py:4-8` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 4-8 | 802 | in range |
| `corpus/instruments/claim-package-check.py:407-409` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 407-409 | 802 | in range |
| `corpus/instruments/claim-package-check.py:413-415` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 413-415 | 802 | in range |
| `corpus/instruments/claim-package-check.py:413-416` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 413-416 | 802 | in range |
| `corpus/instruments/claim-package-check.py:457-458` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 457-458 | 802 | in range |
| `corpus/instruments/claim-package-check.py:460` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 460 | 802 | in range |
| `corpus/instruments/claim-package-check.py:460-461` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 460-461 | 802 | in range |
| `corpus/instruments/claim-package-check.py:465-467` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 465-467 | 802 | in range |
| `corpus/instruments/claim-package-check.py:467` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 467 | 802 | in range |
| `corpus/instruments/claim-package-check.py:469-472` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 469-472 | 802 | in range |
| `corpus/instruments/claim-package-check.py:471` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 471 | 802 | in range |
| `corpus/instruments/claim-package-check.py:489-491` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 489-491 | 802 | in range |
| `corpus/instruments/claim-package-check.py:497` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 497 | 802 | in range |
| `corpus/instruments/claim-package-check.py:515-516` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 515-516 | 802 | in range |
| `corpus/instruments/claim-package-check.py:524-525` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 524-525 | 802 | in range |
| `corpus/instruments/claim-package-check.py:527-528` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 527-528 | 802 | in range |
| `corpus/instruments/claim-package-check.py:584-589` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 584-589 | 802 | in range |
| `corpus/instruments/claim-package-check.py:585-588` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 585-588 | 802 | in range |
| `corpus/instruments/claim-package-check.py:594-613` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 594-613 | 802 | in range |
| `corpus/instruments/claim-package-check.py:595-614` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 595-614 | 802 | in range |
| `corpus/instruments/claim-package-check.py:598-606` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 598-606 | 802 | in range |
| `corpus/instruments/claim-package-check.py:607` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 607 | 802 | in range |
| `corpus/instruments/claim-package-check.py:607-608` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 607-608 | 802 | in range |
| `corpus/instruments/claim-package-check.py:617-619` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 617-619 | 802 | in range |
| `corpus/instruments/claim-package-check.py:634-635` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 634-635 | 802 | in range |
| `corpus/instruments/claim-package-check.py:636-637` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 636-637 | 802 | in range |
| `corpus/instruments/claim-package-check.py:656-660` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 656-660 | 802 | in range |
| `corpus/instruments/claim-package-check.py:672-674` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/claim-package-check.py` | 672-674 | 802 | in range |
| `corpus/instruments/fixtures/claim-package/defect-8-marker/expected-rule:1` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/fixtures/claim-package/defect-8-marker/expected-rule` | 1 | 1 | in range |
| `corpus/instruments/fixtures/claim-package/defect-9-secret/expected-rule:1` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/fixtures/claim-package/defect-9-secret/expected-rule` | 1 | 1 | in range |
| `corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json:2` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json` | 2 | 85 | in range |
| `corpus/instruments/fixtures/claim-package/exemplar/provenance.json:88` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/fixtures/claim-package/exemplar/provenance.json` | 88 | 95 | in range |
| `corpus/instruments/fixtures/claim-package/exemplar/report.md:88` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/fixtures/claim-package/exemplar/report.md` | 88 | 88 | in range |
| `corpus/instruments/r35-defect-closure.sh:164-168` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r35-defect-closure.sh` | 164-168 | 834 | in range |
| `corpus/instruments/r35-defect-closure.sh:192` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r35-defect-closure.sh` | 192 | 834 | in range |
| `corpus/instruments/r35-defect-closure.sh:50-52` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r35-defect-closure.sh` | 50-52 | 834 | in range |
| `corpus/instruments/r36-closure.sh:309` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r36-closure.sh` | 309 | 894 | in range |
| `corpus/instruments/r36-closure.sh:322` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r36-closure.sh` | 322 | 894 | in range |
| `corpus/instruments/r36-closure.sh:465` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r36-closure.sh` | 465 | 894 | in range |
| `corpus/instruments/r36-closure.sh:466` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r36-closure.sh` | 466 | 894 | in range |
| `corpus/instruments/r36-closure.sh:480-481` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r36-closure.sh` | 480-481 | 894 | in range |
| `corpus/instruments/r36-closure.sh:766-768` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r36-closure.sh` | 766-768 | 894 | in range |
| `corpus/instruments/r36-closure.sh:93-108` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r36-closure.sh` | 93-108 | 894 | in range |
| `corpus/instruments/r37-closure.sh:59-64` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r37-closure.sh` | 59-64 | 1558 | in range |
| `corpus/instruments/r41-closure.sh:1392-1405` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r41-closure.sh` | 1392-1405 | 2209 | in range |
| `corpus/instruments/r41-closure.sh:443-459` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r41-closure.sh` | 443-459 | 2209 | in range |
| `corpus/instruments/r41-closure.sh:891-914` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r41-closure.sh` | 891-914 | 2209 | in range |
| `corpus/instruments/r46-c2-gate.py:329` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r46-c2-gate.py` | 329 | 414 | in range |
| `corpus/instruments/r46-counters-selftest-c2.py:537` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r46-counters-selftest-c2.py` | 537 | 830 | in range |
| `corpus/instruments/r46-f29-gate.py:80` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r46-f29-gate.py` | 80 | 391 | in range |
| `corpus/instruments/r46-landing-gate.py:113` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/r46-landing-gate.py` | 113 | 638 | in range |
| `corpus/instruments/resolve.py:161-163` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/resolve.py` | 161-163 | 623 | in range |
| `corpus/instruments/resolve.py:164-172` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/resolve.py` | 164-172 | 623 | in range |
| `corpus/instruments/resolve.py:31-48` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/resolve.py` | 31-48 | 623 | in range |
| `corpus/instruments/resolve.py:74` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/resolve.py` | 74 | 623 | in range |
| `corpus/instruments/score-gap.py:76` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/score-gap.py` | 76 | 554 | in range |
| `corpus/instruments/source-recheck.py:275` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/instruments/source-recheck.py` | 275 | 415 | in range |
| `corpus/knowledge/authorization-safe-harbor-and-scope.md:8` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/authorization-safe-harbor-and-scope.md` | 8 | 46 | in range |
| `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md:97` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` | 97 | 306 | in range |
| `corpus/knowledge/claim-gates.md:15` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/claim-gates.md` | 15 | 160 | in range |
| `corpus/knowledge/claim-gates.md:3` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/claim-gates.md` | 3 | 160 | in range |
| `corpus/knowledge/claim-gates.md:45-47` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/claim-gates.md` | 45-47 | 160 | in range |
| `corpus/knowledge/claim-package-contract.md:11` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/claim-package-contract.md` | 11 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:11-16` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/claim-package-contract.md` | 11-16 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:13` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/claim-package-contract.md` | 13 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:14` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/claim-package-contract.md` | 14 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:15` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/claim-package-contract.md` | 15 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:16` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/claim-package-contract.md` | 16 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:18-26` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/claim-package-contract.md` | 18-26 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:22-23` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/claim-package-contract.md` | 22-23 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:31` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/claim-package-contract.md` | 31 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:7` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/claim-package-contract.md` | 7 | 99 | in range |
| `corpus/knowledge/cna-assignment-and-vulnerability-rules.md:36` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/cna-assignment-and-vulnerability-rules.md` | 36 | 80 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:119-131` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/considerthese-proposals-ledger.md` | 119-131 | 166 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:13` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/considerthese-proposals-ledger.md` | 13 | 166 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:22-33` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/considerthese-proposals-ledger.md` | 22-33 | 166 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:3` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/considerthese-proposals-ledger.md` | 3 | 166 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:37` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/considerthese-proposals-ledger.md` | 37 | 166 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:22` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/coordinated-disclosure-timelines.md` | 22 | 44 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:24` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/coordinated-disclosure-timelines.md` | 24 | 44 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:24-25` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/coordinated-disclosure-timelines.md` | 24-25 | 44 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:6-17` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/coordinated-disclosure-timelines.md` | 6-17 | 44 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:7-17` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/coordinated-disclosure-timelines.md` | 7-17 | 44 | in range |
| `corpus/knowledge/cvss-v4-severity-and-vector.md:2` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/cvss-v4-severity-and-vector.md` | 2 | 48 | in range |
| `corpus/knowledge/cvss-v4-severity-and-vector.md:34` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/cvss-v4-severity-and-vector.md` | 34 | 48 | in range |
| `corpus/knowledge/ev-model.md:37-38` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/ev-model.md` | 37-38 | 60 | in range |
| `corpus/knowledge/evidence-dir.md:78` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/evidence-dir.md` | 78 | 91 | in range |
| `corpus/knowledge/github-private-vulnerability-reporting.md:40` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/github-private-vulnerability-reporting.md` | 40 | 49 | in range |
| `corpus/knowledge/github-repository-security-advisories.md:11` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/github-repository-security-advisories.md` | 11 | 145 | in range |
| `corpus/knowledge/intake-and-finalize.md:78-92` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/intake-and-finalize.md` | 78-92 | 111 | in range |
| `corpus/knowledge/mission-control.md:3` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/mission-control.md` | 3 | 171 | in range |
| `corpus/knowledge/ops-invariants.md:18` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/ops-invariants.md` | 18 | 141 | in range |
| `corpus/knowledge/ops-invariants.md:24` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/ops-invariants.md` | 24 | 141 | in range |
| `corpus/knowledge/policy-access-playbook.md:13` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/policy-access-playbook.md` | 13 | 35 | in range |
| `corpus/knowledge/program-quirks.md:10` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/program-quirks.md` | 10 | 67 | in range |
| `corpus/knowledge/program-severity-ladders-and-reward-scales.md:16` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/program-severity-ladders-and-reward-scales.md` | 16 | 67 | in range |
| `corpus/knowledge/retirement-autopsies.md:38` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/retirement-autopsies.md` | 38 | 141 | in range |
| `corpus/knowledge/statutory-authorization-and-unauthorized-access.md:46` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/statutory-authorization-and-unauthorized-access.md` | 46 | 98 | in range |
| `corpus/knowledge/submitted-registry.md:105` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/submitted-registry.md` | 105 | 229 | in range |
| `corpus/knowledge/submitted-registry.md:138-141` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/submitted-registry.md` | 138-141 | 229 | in range |
| `corpus/knowledge/submitted-registry.md:146-148` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/submitted-registry.md` | 146-148 | 229 | in range |
| `corpus/knowledge/submitted-registry.md:207-209` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/submitted-registry.md` | 207-209 | 229 | in range |
| `corpus/knowledge/submitted-registry.md:27` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/submitted-registry.md` | 27 | 229 | in range |
| `corpus/knowledge/submitted-registry.md:9` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/submitted-registry.md` | 9 | 229 | in range |
| `corpus/knowledge/triage-thresholds.md:25` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/triage-thresholds.md` | 25 | 487 | in range |
| `corpus/knowledge/ufo-archive-2026.md:11` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/ufo-archive-2026.md` | 11 | 210 | in range |
| `corpus/knowledge/ufo-archive-2026.md:145-149` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/ufo-archive-2026.md` | 145-149 | 210 | in range |
| `corpus/knowledge/ufo-archive-2026.md:150-154` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/ufo-archive-2026.md` | 150-154 | 210 | in range |
| `corpus/knowledge/ufo-archive-2026.md:36` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/ufo-archive-2026.md` | 36 | 210 | in range |
| `corpus/knowledge/vendor-third-party-finding-coordination.md:114-120` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/vendor-third-party-finding-coordination.md` | 114-120 | 172 | in range |
| `corpus/knowledge/vendor-third-party-finding-coordination.md:17-39` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/vendor-third-party-finding-coordination.md` | 17-39 | 172 | in range |
| `corpus/knowledge/vendor-third-party-finding-coordination.md:41-59` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/vendor-third-party-finding-coordination.md` | 41-59 | 172 | in range |
| `corpus/knowledge/vendor-third-party-finding-coordination.md:91-96` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/knowledge/vendor-third-party-finding-coordination.md` | 91-96 | 172 | in range |
| `corpus/lessons/round-20-recensus.md:20` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-20-recensus.md` | 20 | 43 | in range |
| `corpus/lessons/round-20-recensus.md:29` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-20-recensus.md` | 29 | 43 | in range |
| `corpus/lessons/round-20-recensus.md:33` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-20-recensus.md` | 33 | 43 | in range |
| `corpus/lessons/round-20-recensus.md:34-35` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-20-recensus.md` | 34-35 | 43 | in range |
| `corpus/lessons/round-20-recensus.md:37-39` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-20-recensus.md` | 37-39 | 43 | in range |
| `corpus/lessons/round-20-recensus.md:39` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-20-recensus.md` | 39 | 43 | in range |
| `corpus/lessons/round-20-recensus.md:43` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-20-recensus.md` | 43 | 43 | in range |
| `corpus/lessons/round-21-routing-blocked.md:115` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-21-routing-blocked.md` | 115 | 145 | in range |
| `corpus/lessons/round-22.md:91` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-22.md` | 91 | 155 | in range |
| `corpus/lessons/round-24.md:77` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-24.md` | 77 | 229 | in range |
| `corpus/lessons/round-29-verifier-spotcheck.md:74` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-29-verifier-spotcheck.md` | 74 | 104 | in range |
| `corpus/lessons/round-29.md:214` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-29.md` | 214 | 337 | in range |
| `corpus/lessons/round-29.md:219` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-29.md` | 219 | 337 | in range |
| `corpus/lessons/round-29.md:221` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-29.md` | 221 | 337 | in range |
| `corpus/lessons/round-30-verifier-spotcheck.md:12` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-30-verifier-spotcheck.md` | 12 | 71 | in range |
| `corpus/lessons/round-30.md:82` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-30.md` | 82 | 118 | in range |
| `corpus/lessons/round-31.md:146` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-31.md` | 146 | 175 | in range |
| `corpus/lessons/round-31.md:147` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-31.md` | 147 | 175 | in range |
| `corpus/lessons/round-32-verifier-spotcheck.md:73` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-32-verifier-spotcheck.md` | 73 | 96 | in range |
| `corpus/lessons/round-32-verifier-spotcheck.md:93` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-32-verifier-spotcheck.md` | 93 | 96 | in range |
| `corpus/lessons/round-33-verifier-spotcheck.md:167-169` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-33-verifier-spotcheck.md` | 167-169 | 195 | in range |
| `corpus/lessons/round-33-verifier-spotcheck.md:174` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-33-verifier-spotcheck.md` | 174 | 195 | in range |
| `corpus/lessons/round-33-verifier-spotcheck.md:174-176` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-33-verifier-spotcheck.md` | 174-176 | 195 | in range |
| `corpus/lessons/round-33-verifier-spotcheck.md:181` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-33-verifier-spotcheck.md` | 181 | 195 | in range |
| `corpus/lessons/round-33.md:140` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-33.md` | 140 | 247 | in range |
| `corpus/lessons/round-33.md:215-226` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-33.md` | 215-226 | 247 | in range |
| `corpus/lessons/round-33.md:31-32` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-33.md` | 31-32 | 247 | in range |
| `corpus/lessons/round-34-verifier-spotcheck.md:173` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-34-verifier-spotcheck.md` | 173 | 209 | in range |
| `corpus/lessons/round-34-verifier-spotcheck.md:177` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-34-verifier-spotcheck.md` | 177 | 209 | in range |
| `corpus/lessons/round-34-verifier-spotcheck.md:199-203` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-34-verifier-spotcheck.md` | 199-203 | 209 | in range |
| `corpus/lessons/round-34.md:343-358` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-34.md` | 343-358 | 561 | in range |
| `corpus/lessons/round-34.md:482-485` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-34.md` | 482-485 | 561 | in range |
| `corpus/lessons/round-35-verifier-spotcheck.md:10-20` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-35-verifier-spotcheck.md` | 10-20 | 144 | in range |
| `corpus/lessons/round-35-verifier-spotcheck.md:127-129` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-35-verifier-spotcheck.md` | 127-129 | 144 | in range |
| `corpus/lessons/round-35-verifier-spotcheck.md:132-134` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-35-verifier-spotcheck.md` | 132-134 | 144 | in range |
| `corpus/lessons/round-35.md:155-169` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-35.md` | 155-169 | 529 | in range |
| `corpus/lessons/round-35.md:282-290` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-35.md` | 282-290 | 529 | in range |
| `corpus/lessons/round-36-verifier-spotcheck.md:160-162` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-36-verifier-spotcheck.md` | 160-162 | 164 | in range |
| `corpus/lessons/round-36.md:3` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-36.md` | 3 | 45 | in range |
| `corpus/lessons/round-36.md:39` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-36.md` | 39 | 45 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:105-111` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37-verifier-spotcheck.md` | 105-111 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:113-118` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37-verifier-spotcheck.md` | 113-118 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:159-164` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37-verifier-spotcheck.md` | 159-164 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:165-168` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37-verifier-spotcheck.md` | 165-168 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:169-174` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37-verifier-spotcheck.md` | 169-174 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:175-177` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37-verifier-spotcheck.md` | 175-177 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:50-56` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37-verifier-spotcheck.md` | 50-56 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:8-10` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37-verifier-spotcheck.md` | 8-10 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:90` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37-verifier-spotcheck.md` | 90 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:95` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37-verifier-spotcheck.md` | 95 | 186 | in range |
| `corpus/lessons/round-37.md:268-270` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37.md` | 268-270 | 350 | in range |
| `corpus/lessons/round-37.md:271` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37.md` | 271 | 350 | in range |
| `corpus/lessons/round-37.md:272-273` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37.md` | 272-273 | 350 | in range |
| `corpus/lessons/round-37.md:274-276` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37.md` | 274-276 | 350 | in range |
| `corpus/lessons/round-37.md:277` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37.md` | 277 | 350 | in range |
| `corpus/lessons/round-37.md:278` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37.md` | 278 | 350 | in range |
| `corpus/lessons/round-37.md:279-286` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37.md` | 279-286 | 350 | in range |
| `corpus/lessons/round-37.md:85` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-37.md` | 85 | 350 | in range |
| `corpus/lessons/round-38-verifier-spotcheck.md:155-160` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-38-verifier-spotcheck.md` | 155-160 | 180 | in range |
| `corpus/lessons/round-38-verifier-spotcheck.md:168-171` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-38-verifier-spotcheck.md` | 168-171 | 180 | in range |
| `corpus/lessons/round-38-verifier-spotcheck.md:172-174` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-38-verifier-spotcheck.md` | 172-174 | 180 | in range |
| `corpus/lessons/round-38.md:21` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-38.md` | 21 | 311 | in range |
| `corpus/lessons/round-38.md:287` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-38.md` | 287 | 311 | in range |
| `corpus/lessons/round-38.md:94` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-38.md` | 94 | 311 | in range |
| `corpus/lessons/round-39-verifier-spotcheck.md:181-182` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-39-verifier-spotcheck.md` | 181-182 | 192 | in range |
| `corpus/lessons/round-39.md:15` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-39.md` | 15 | 105 | in range |
| `corpus/lessons/round-39.md:36-42` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-39.md` | 36-42 | 105 | in range |
| `corpus/lessons/round-39.md:77` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-39.md` | 77 | 105 | in range |
| `corpus/lessons/round-39.md:78` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-39.md` | 78 | 105 | in range |
| `corpus/lessons/round-4-aggregator-audit.md:26` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-4-aggregator-audit.md` | 26 | 70 | in range |
| `corpus/lessons/round-4-aggregator-audit.md:28` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-4-aggregator-audit.md` | 28 | 70 | in range |
| `corpus/lessons/round-40-verifier-spotcheck.md:176-180` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-40-verifier-spotcheck.md` | 176-180 | 213 | in range |
| `corpus/lessons/round-41-verifier-spotcheck.md:132-134` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-41-verifier-spotcheck.md` | 132-134 | 155 | in range |
| `corpus/lessons/round-41-verifier-spotcheck.md:148-149` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-41-verifier-spotcheck.md` | 148-149 | 155 | in range |
| `corpus/lessons/round-41.md:103-107` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-41.md` | 103-107 | 122 | in range |
| `corpus/lessons/round-41.md:108-110` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-41.md` | 108-110 | 122 | in range |
| `corpus/lessons/round-42-verifier-spotcheck.md:178` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-42-verifier-spotcheck.md` | 178 | 316 | in range |
| `corpus/lessons/round-42-verifier-spotcheck.md:65` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-42-verifier-spotcheck.md` | 65 | 316 | in range |
| `corpus/lessons/round-42.md:11-16` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-42.md` | 11-16 | 152 | in range |
| `corpus/lessons/round-42.md:52` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-42.md` | 52 | 152 | in range |
| `corpus/lessons/round-43.md:90` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-43.md` | 90 | 175 | in range |
| `corpus/lessons/round-44.md:125` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-44.md` | 125 | 205 | in range |
| `corpus/lessons/round-44.md:126` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-44.md` | 126 | 205 | in range |
| `corpus/lessons/round-44.md:131` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-44.md` | 131 | 205 | in range |
| `corpus/lessons/round-44.md:15` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-44.md` | 15 | 205 | in range |
| `corpus/lessons/round-44.md:16` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-44.md` | 16 | 205 | in range |
| `corpus/lessons/round-44.md:189` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-44.md` | 189 | 205 | in range |
| `corpus/lessons/round-44.md:22` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-44.md` | 22 | 205 | in range |
| `corpus/lessons/round-45-verifier-spotcheck.md:22` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-45-verifier-spotcheck.md` | 22 | 103 | in range |
| `corpus/lessons/round-45-verifier-spotcheck.md:98` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-45-verifier-spotcheck.md` | 98 | 103 | in range |
| `corpus/lessons/round-46.md:29` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-46.md` | 29 | 161 | in range |
| `corpus/lessons/round-5.md:16` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-5.md` | 16 | 38 | in range |
| `corpus/lessons/round-8.md:10` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-8.md` | 10 | 53 | in range |
| `corpus/lessons/round-9.md:33` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/lessons/round-9.md` | 33 | 63 | in range |
| `corpus/source-snapshots/round-23/S029.txt:14` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/source-snapshots/round-23/S029.txt` | 14 | 146 | in range |
| `corpus/source-snapshots/round-24/S013.txt:65` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/source-snapshots/round-24/S013.txt` | 65 | 183 | in range |
| `corpus/source-snapshots/round-31/S048.txt:35` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/source-snapshots/round-31/S048.txt` | 35 | 97 | in range |
| `corpus/source-snapshots/round-32/S050.txt:70` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/source-snapshots/round-32/S050.txt` | 70 | 630 | in range |
| `corpus/source-snapshots/round-43/S067.txt:69` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/source-snapshots/round-43/S067.txt` | 69 | 109 | in range |
| `corpus/source-snapshots/round-43/S067.txt:83` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/source-snapshots/round-43/S067.txt` | 83 | 109 | in range |
| `corpus/source-snapshots/round-43/S067.txt:88` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/source-snapshots/round-43/S067.txt` | 88 | 109 | in range |
| `corpus/source-snapshots/round-44/S069.txt:61` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/source-snapshots/round-44/S069.txt` | 61 | 1132 | in range |
| `corpus/source-snapshots/round-45/S071.txt:310-311` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/source-snapshots/round-45/S071.txt` | 310-311 | 372 | in range |
| `corpus/source-snapshots/round-47/S076.txt:574` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/source-snapshots/round-47/S076.txt` | 574 | 610 | in range |
| `corpus/source-snapshots/round-51/S081.txt:2` | INTERNAL | `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/source-snapshots/round-51/S081.txt` | 2 | 120 | in range |

Every MIRROR-EQUIVALENT anchor in range is still only a *same-name same-path*
match against a Sep-5 genesis sync — see §Honest scope limits.

## Top-20 most-cited GONE paths

| # | citation | files citing | occurrences | noise flags |
|---|---|---|---|---|
| 1 | `[~]` | 40 | 94 | synthetic |
| 2 | `anchorcheck.py` | 30 | 45 | - |
| 3 | `density.py` | 26 | 35 | - |
| 4 | `claims.json` | 25 | 52 | - |
| 5 | `source-recheck.py` | 24 | 36 | - |
| 6 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 23 | 24 | shell,synthetic |
| 7 | `resolve.py` | 22 | 41 | - |
| 8 | `claims/` | 22 | 39 | - |
| 9 | `frontier-recheck-count.py` | 22 | 34 | - |
| 10 | `status.json` | 21 | 54 | - |
| 11 | `ops/claim-check.mjs` | 19 | 38 | - |
| 12 | `.ufo/watchdog.log` | 19 | 19 | - |
| 13 | `census-before.txt` | 18 | 24 | - |
| 14 | `SOURCES.md` | 18 | 23 | - |
| 15 | `~/Projects/bounties` | 17 | 27 | - |
| 16 | `c2-controls/before.txt` | 17 | 26 | - |
| 17 | `recheck-audit.py` | 15 | 23 | - |
| 18 | `fleets/registry.json` | 15 | 20 | - |
| 19 | `george/` | 15 | 19 | - |
| 20 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 15 | 18 | shell,synthetic |

Max over all citations: files citing = 70, occurrences = 187.

## MIRROR-EQUIVALENT — exact list (0)

| # | citation | mirror path | lines | files | method |
|---|---|---|---|---|---|
