# citation-survival census — kasegi lane

Instrument: `corpus/instruments/resolve.py` (stdlib-only, deterministic; r18 definition).
Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
Scope: `SKILL.md` + `corpus/**/*.md` (201 files).
Extraction: verbatim density.py docstring path-like rule (see module docstring).
Mirror root for bounty-path equivalence: `/home/vgpnk/Projects/the-bounty-hunter` (ABSENT — mirror fallback disabled).

## Totals

- distinct path-like citations: **4758** (total occurrences: 10194; a citation cited in both scopes counts once)
- distinct citations appearing in SKILL.md: 701 (of which SKILL-only: 386)
- distinct citations appearing in corpus: 4372

| class | distinct citations |
|---|---|
| RESOLVES | 63 |
| MIRROR-EQUIVALENT | 0 |
| GONE | 3643 |
| INTERNAL | 1052 |
| OTHER *(root-domain bucket, orthogonal: the brief says classify other roots as RESOLVES/GONE)* | 63 resolve / 144 gone = 207 |

Terminal outcome classes sum to the distinct total: RESOLVES(63) + MIRROR-EQUIVALENT(0) + INTERNAL(1052) + GONE(3643) = 4758.
Of the 63 RESOLVES, 63 are non-lane roots (domain `other`: origin-work, /tmp, ~/projects …); 0 are lane-repo-absolute.
Of the 0 MIRROR-EQUIVALENT, 0 were written as `~/Projects/bounties/...` (domain `bounty`), 0 were bounty-root-relative bare paths (domain `rel`).

## Resolvability rate

Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citations appearing in that scope (a citation in both scopes enters both denominators).

- SKILL.md alone: **132/701 = 18.83%**
- corpus alone: **1090/4372 = 24.93%**
- lane total (SKILL.md + corpus): **1115/4758 = 23.43%**

## Noise sub-census (GONE tokens that are rule artifacts, not citable paths)

Flag counts (a token can carry several flags):

| flags | distinct GONE citations |
|---|---|
| gitstatus | 8 |
| gitstatus,synthetic | 9 |
| regex | 19 |
| regex,synthetic | 7 |
| shell | 367 |
| shell,synthetic | 167 |
| synthetic | 598 |

- GONE citations carrying any noise flag: 1175
- GONE citations with no noise flag (genuine vanished paths): 2468
- citations containing glob/placeholder syntax (`* ? [ { } <...>`): 840

Noise-adjusted rates (denominator excludes noise-flagged citations):
- SKILL: 130/349 = 37.25%
- CORPUS: 1028/3429 = 29.98%
- ALL: 1053/3521 = 29.91%

## Scope x class matrix

| class | SKILL.md only | SKILL+corpus | corpus only | total |
|---|---|---|---|---|
| RESOLVES | 1 | 2 | 60 | 63 |
| MIRROR-EQUIVALENT | 0 | 0 | 0 | 0 |
| GONE | 361 | 208 | 3074 | 3643 |
| INTERNAL | 24 | 105 | 923 | 1052 |

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

Result: both yield **4758** distinct citations, and
`diff <(pipeline to file) <(cut -f1 citation-survival.tsv | tail -n +2 | sort -u)` is empty (sets identical, not just counts).
Re-running `resolve.py` twice leaves both outputs byte-identical (md5 stable).

## Honest scope limits

- MIRROR-EQUIVALENT means the same relative path exists in the Sep-5 genesis mirror `~/Projects/the-bounty-hunter`; it does NOT establish byte-equivalence with the vanished tree, and the mirror holds the code half only.
- Glob/brace citations resolve if any deterministic expansion exists; a glob with zero matches is GONE (e.g. `bounty-map/programs/*.json`).
- The path-like rule (verbatim from density.py) admits regex literals, git-porcelain snippets and shell fragments; the noise sub-census quantifies them so the raw rate can be read against the noise-adjusted rate.

## Line-anchor viability (resolvable citations carrying `:NN` / `:NN-MM`)

For every citation whose base resolves and whose anchor names a file, the anchor
is compared against the resolved file's line count (editor convention).

- anchors checked: 472 — in range: 453 — **out of range: 19**

| citation | class | resolved file | anchor | file lines | verdict |
|---|---|---|---|---|---|
| `../MISSION.md:49-56` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/../MISSION.md` | 49-56 | 93 | in range |
| `./PROVINCE.md:3` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/./PROVINCE.md` | 3 | 176 | in range |
| `.gitignore:11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.gitignore` | 11 | 2 | OUT OF RANGE |
| `.gitignore:7` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.gitignore` | 7 | 2 | OUT OF RANGE |
| `.gitignore:8-9` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.gitignore` | 8-9 | 2 | OUT OF RANGE |
| `.ufo/waves/round-24/wave1/LivenessMatrix.md:200-201` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/wave1/LivenessMatrix.md` | 200-201 | 238 | in range |
| `.ufo/waves/round-31/wave1/CritC2Kill.md:232` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-31/wave1/CritC2Kill.md` | 232 | 309 | in range |
| `.ufo/waves/round-33/claims-erratum-1.md:1-36` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-33/claims-erratum-1.md` | 1-36 | 36 | in range |
| `.ufo/waves/round-34/mistakes-erratum-1.md:18-20` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-34/mistakes-erratum-1.md` | 18-20 | 66 | in range |
| `.ufo/waves/round-34/mistakes-erratum-1.md:9-29` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-34/mistakes-erratum-1.md` | 9-29 | 66 | in range |
| `.ufo/waves/round-34/wave1/ExecCaptureBindingHarden.md:505-507` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-34/wave1/ExecCaptureBindingHarden.md` | 505-507 | 512 | in range |
| `.ufo/waves/round-34/wave1/MutSelftestSummary.md:332` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-34/wave1/MutSelftestSummary.md` | 332 | 373 | in range |
| `.ufo/waves/round-35/claims.json:6` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-35/claims.json` | 6 | 87 | in range |
| `.ufo/waves/round-36/build-spec.py:123` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-36/build-spec.py` | 123 | 286 | in range |
| `.ufo/waves/round-37/final-gates/all-gates.txt:2` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-37/final-gates/all-gates.txt` | 2 | 121 | in range |
| `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md:56` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md` | 56 | 173 | in range |
| `.ufo/waves/round-38/final-gates/all-gates.txt:15` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-38/final-gates/all-gates.txt` | 15 | 79 | in range |
| `.ufo/waves/round-38/final-gates/all-gates.txt:2` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-38/final-gates/all-gates.txt` | 2 | 79 | in range |
| `.ufo/waves/round-38/wave1/RevPendingResolutions.md:48` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-38/wave1/RevPendingResolutions.md` | 48 | 101 | in range |
| `.ufo/waves/round-38/wave1/RevPendingResolutions.md:49` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-38/wave1/RevPendingResolutions.md` | 49 | 101 | in range |
| `.ufo/waves/round-42/c1-controls/do-nothing.txt:16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-42/c1-controls/do-nothing.txt` | 16 | 18 | in range |
| `.ufo/waves/round-42/claims-erratum-3.md:3` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-42/claims-erratum-3.md` | 3 | 3 | in range |
| `.ufo/waves/round-42/claims-erratum-4.md:9` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-42/claims-erratum-4.md` | 9 | 48 | in range |
| `.ufo/waves/round-43/final-gates/r42-at-de09313-run.txt:2` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/final-gates/r42-at-de09313-run.txt` | 2 | 19 | in range |
| `.ufo/waves/round-43/w1-REGISTRY.txt:7` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1-REGISTRY.txt` | 7 | 7 | in range |
| `.ufo/waves/round-45/source-recon/S072.txt:148-149` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-45/source-recon/S072.txt` | 148-149 | 312 | in range |
| `.ufo/waves/round-46/attempt2/freeze.txt:7` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/freeze.txt` | 7 | 11 | in range |
| `.ufo/waves/round-46/freeze.txt:7` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/freeze.txt` | 7 | 8 | in range |
| `.ufo/waves/round-46/wave1/R46SentinelContent.md:13` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/wave1/R46SentinelContent.md` | 13 | 99 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md:49` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md` | 49 | 89 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md:61` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md` | 61 | 89 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-37/kasegi.md:25` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-37/kasegi.md` | 25 | 88 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md:37` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md` | 37 | 87 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-40/kasegi.md:32` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-40/kasegi.md` | 32 | 65 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1490` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` | 1490 | 2027 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1537` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` | 1537 | 2027 | in range |
| `/home/vgpnk/Projects/shokunin/MISSION.md:49-56` | RESOLVES | `/home/vgpnk/Projects/shokunin/MISSION.md` | 49-56 | 93 | in range |
| `/home/vgpnk/Projects/shokunin/PROTOCOL.md:457-461` | RESOLVES | `/home/vgpnk/Projects/shokunin/PROTOCOL.md` | 457-461 | 533 | in range |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/security-txt-publishing.md:63` | RESOLVES | `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/security-txt-publishing.md` | 63 | 156 | in range |
| `LOG.md:1469` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1469 | 2119 | in range |
| `LOG.md:1550` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1550 | 2119 | in range |
| `LOG.md:1584` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1584 | 2119 | in range |
| `LOG.md:1665` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1665 | 2119 | in range |
| `LOG.md:1686` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1686 | 2119 | in range |
| `LOG.md:1728` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1728 | 2119 | in range |
| `LOG.md:1800-1801` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1800-1801 | 2119 | in range |
| `LOG.md:1804` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1804 | 2119 | in range |
| `LOG.md:2045` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 2045 | 2119 | in range |
| `LOG.md:545` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 545 | 2119 | in range |
| `LOG.md:709-713` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 709-713 | 2119 | in range |
| `LOG.md:734` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 734 | 2119 | in range |
| `LOG.md:747-750` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 747-750 | 2119 | in range |
| `LOG.md:812` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 812 | 2119 | in range |
| `PROVINCE.md:16-22` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 16-22 | 176 | in range |
| `PROVINCE.md:165` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 165 | 176 | in range |
| `PROVINCE.md:171` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 171 | 176 | in range |
| `PROVINCE.md:31-40` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 31-40 | 176 | in range |
| `PROVINCE.md:38` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 38 | 176 | in range |
| `PROVINCE.md:75` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 75 | 176 | in range |
| `PROVINCE.md:77` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 77 | 176 | in range |
| `PROVINCE.md:80-152` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 80-152 | 176 | in range |
| `PROVINCE.md:90` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 90 | 176 | in range |
| `README.md:159` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/README.md` | 159 | 14 | OUT OF RANGE |
| `README.md:19` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/README.md` | 19 | 14 | OUT OF RANGE |
| `README.md:213` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/README.md` | 213 | 14 | OUT OF RANGE |
| `README.md:23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/README.md` | 23 | 14 | OUT OF RANGE |
| `README.md:30` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/README.md` | 30 | 14 | OUT OF RANGE |
| `SCORECARD.md:1014-1027` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1014-1027 | 1923 | in range |
| `SCORECARD.md:1014-1035` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1014-1035 | 1923 | in range |
| `SCORECARD.md:1074` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1074 | 1923 | in range |
| `SCORECARD.md:1078` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1078 | 1923 | in range |
| `SCORECARD.md:1116` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1116 | 1923 | in range |
| `SCORECARD.md:1116-1119` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1116-1119 | 1923 | in range |
| `SCORECARD.md:1129` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1129 | 1923 | in range |
| `SCORECARD.md:1145` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1145 | 1923 | in range |
| `SCORECARD.md:121-149` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 121-149 | 1923 | in range |
| `SCORECARD.md:1240` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1240 | 1923 | in range |
| `SCORECARD.md:1263-1281` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1263-1281 | 1923 | in range |
| `SCORECARD.md:1269` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1269 | 1923 | in range |
| `SCORECARD.md:1271` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1271 | 1923 | in range |
| `SCORECARD.md:1284` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1284 | 1923 | in range |
| `SCORECARD.md:134` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 134 | 1923 | in range |
| `SCORECARD.md:1492` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1492 | 1923 | in range |
| `SCORECARD.md:1505` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1505 | 1923 | in range |
| `SCORECARD.md:1509` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1509 | 1923 | in range |
| `SCORECARD.md:1532` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1532 | 1923 | in range |
| `SCORECARD.md:1547` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1547 | 1923 | in range |
| `SCORECARD.md:1567` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1567 | 1923 | in range |
| `SCORECARD.md:1595` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1595 | 1923 | in range |
| `SCORECARD.md:1602` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1602 | 1923 | in range |
| `SCORECARD.md:1602-1605` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1602-1605 | 1923 | in range |
| `SCORECARD.md:1605` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1605 | 1923 | in range |
| `SCORECARD.md:1634` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1634 | 1923 | in range |
| `SCORECARD.md:164` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 164 | 1923 | in range |
| `SCORECARD.md:174` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 174 | 1923 | in range |
| `SCORECARD.md:1788` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1788 | 1923 | in range |
| `SCORECARD.md:228-290` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 228-290 | 1923 | in range |
| `SCORECARD.md:23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 23 | 1923 | in range |
| `SCORECARD.md:251` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 251 | 1923 | in range |
| `SCORECARD.md:252` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 252 | 1923 | in range |
| `SCORECARD.md:259-270` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 259-270 | 1923 | in range |
| `SCORECARD.md:309` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 309 | 1923 | in range |
| `SCORECARD.md:309-321` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 309-321 | 1923 | in range |
| `SCORECARD.md:327` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 327 | 1923 | in range |
| `SCORECARD.md:331` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 331 | 1923 | in range |
| `SCORECARD.md:49-58` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 49-58 | 1923 | in range |
| `SCORECARD.md:502` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 502 | 1923 | in range |
| `SCORECARD.md:510` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 510 | 1923 | in range |
| `SCORECARD.md:65` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 65 | 1923 | in range |
| `SCORECARD.md:813` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 813 | 1923 | in range |
| `SCORECARD.md:813-819` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 813-819 | 1923 | in range |
| `SCORECARD.md:837` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 837 | 1923 | in range |
| `SCORECARD.md:88-96` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 88-96 | 1923 | in range |
| `SCORECARD.md:988` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 988 | 1923 | in range |
| `SHONEN.md:164-165` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` | 164-165 | 12 | OUT OF RANGE |
| `SHONEN.md:164-166` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` | 164-166 | 12 | OUT OF RANGE |
| `SHONEN.md:172` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` | 172 | 12 | OUT OF RANGE |
| `SHONEN.md:173-174` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` | 173-174 | 12 | OUT OF RANGE |
| `SHONEN.md:182-183` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` | 182-183 | 12 | OUT OF RANGE |
| `SHONEN.md:185` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` | 185 | 12 | OUT OF RANGE |
| `SHONEN.md:212-213` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` | 212-213 | 12 | OUT OF RANGE |
| `SHONEN.md:249-256` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` | 249-256 | 12 | OUT OF RANGE |
| `SHONEN.md:310` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` | 310 | 12 | OUT OF RANGE |
| `SHONEN.md:311` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` | 311 | 12 | OUT OF RANGE |
| `SHONEN.md:34` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` | 34 | 12 | OUT OF RANGE |
| `SKILL.md:10` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 10 | 1216 | in range |
| `SKILL.md:10-11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 10-11 | 1216 | in range |
| `SKILL.md:1000` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1000 | 1216 | in range |
| `SKILL.md:1069` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1069 | 1216 | in range |
| `SKILL.md:1091` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1091 | 1216 | in range |
| `SKILL.md:1093-1104` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1093-1104 | 1216 | in range |
| `SKILL.md:1097` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1097 | 1216 | in range |
| `SKILL.md:1097-1098` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1097-1098 | 1216 | in range |
| `SKILL.md:1100` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1100 | 1216 | in range |
| `SKILL.md:111` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 111 | 1216 | in range |
| `SKILL.md:111-112` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 111-112 | 1216 | in range |
| `SKILL.md:1111` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1111 | 1216 | in range |
| `SKILL.md:1115` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1115 | 1216 | in range |
| `SKILL.md:113-114` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 113-114 | 1216 | in range |
| `SKILL.md:113-117` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 113-117 | 1216 | in range |
| `SKILL.md:115` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 115 | 1216 | in range |
| `SKILL.md:1163` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1163 | 1216 | in range |
| `SKILL.md:117` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 117 | 1216 | in range |
| `SKILL.md:14-15` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 14-15 | 1216 | in range |
| `SKILL.md:146` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 146 | 1216 | in range |
| `SKILL.md:148` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 148 | 1216 | in range |
| `SKILL.md:149` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 149 | 1216 | in range |
| `SKILL.md:175` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 175 | 1216 | in range |
| `SKILL.md:175-176` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 175-176 | 1216 | in range |
| `SKILL.md:245-247` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 245-247 | 1216 | in range |
| `SKILL.md:246` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 246 | 1216 | in range |
| `SKILL.md:323` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 323 | 1216 | in range |
| `SKILL.md:385` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 385 | 1216 | in range |
| `SKILL.md:413` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 413 | 1216 | in range |
| `SKILL.md:459` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 459 | 1216 | in range |
| `SKILL.md:494-506` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 494-506 | 1216 | in range |
| `SKILL.md:498` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 498 | 1216 | in range |
| `SKILL.md:499` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 499 | 1216 | in range |
| `SKILL.md:500-501` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 500-501 | 1216 | in range |
| `SKILL.md:502` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 502 | 1216 | in range |
| `SKILL.md:522` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 522 | 1216 | in range |
| `SKILL.md:525` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 525 | 1216 | in range |
| `SKILL.md:526` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 526 | 1216 | in range |
| `SKILL.md:590-596` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 590-596 | 1216 | in range |
| `SKILL.md:597-608` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 597-608 | 1216 | in range |
| `SKILL.md:609-614` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 609-614 | 1216 | in range |
| `SKILL.md:615-621` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 615-621 | 1216 | in range |
| `SKILL.md:622-635` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 622-635 | 1216 | in range |
| `SKILL.md:636-639` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 636-639 | 1216 | in range |
| `SKILL.md:640-643` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 640-643 | 1216 | in range |
| `SKILL.md:644-651` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 644-651 | 1216 | in range |
| `SKILL.md:652-664` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 652-664 | 1216 | in range |
| `SKILL.md:665-679` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 665-679 | 1216 | in range |
| `SKILL.md:8` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 8 | 1216 | in range |
| `SKILL.md:86` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 86 | 1216 | in range |
| `SKILL.md:90-91` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 90-91 | 1216 | in range |
| `SKILL.md:94-95` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 94-95 | 1216 | in range |
| `considerthese/2026-10-25.md:53-57` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-25.md` | 53-57 | 77 | in range |
| `considerthese/2026-10-25.md:76` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-25.md` | 76 | 77 | in range |
| `considerthese/2026-10-26.md:30` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-26.md` | 30 | 35 | in range |
| `considerthese/2026-10-26.md:31` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-26.md` | 31 | 35 | in range |
| `considerthese/2026-10-26.md:35` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-26.md` | 35 | 35 | in range |
| `corpus/QUALITY.md:169` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 169 | 428 | in range |
| `corpus/QUALITY.md:220-222` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 220-222 | 428 | in range |
| `corpus/QUALITY.md:226` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 226 | 428 | in range |
| `corpus/QUALITY.md:227` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 227 | 428 | in range |
| `corpus/QUALITY.md:229` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 229 | 428 | in range |
| `corpus/QUALITY.md:249` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 249 | 428 | in range |
| `corpus/QUALITY.md:263` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 263 | 428 | in range |
| `corpus/QUALITY.md:278` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 278 | 428 | in range |
| `corpus/QUALITY.md:292` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 292 | 428 | in range |
| `corpus/QUALITY.md:35-36` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 35-36 | 428 | in range |
| `corpus/QUALITY.md:391` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 391 | 428 | in range |
| `corpus/QUALITY.md:401` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 401 | 428 | in range |
| `corpus/QUALITY.md:407` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 407 | 428 | in range |
| `corpus/QUALITY.md:413-416` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 413-416 | 428 | in range |
| `corpus/QUALITY.md:77` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 77 | 428 | in range |
| `corpus/QUALITY.md:83` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 83 | 428 | in range |
| `corpus/QUALITY.md:89` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 89 | 428 | in range |
| `corpus/QUALITY.md:95` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 95 | 428 | in range |
| `corpus/README.md:145` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 145 | 726 | in range |
| `corpus/README.md:168` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 168 | 726 | in range |
| `corpus/README.md:200` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 200 | 726 | in range |
| `corpus/README.md:207` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 207 | 726 | in range |
| `corpus/README.md:208` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 208 | 726 | in range |
| `corpus/README.md:210` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 210 | 726 | in range |
| `corpus/README.md:211` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 211 | 726 | in range |
| `corpus/README.md:309` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 309 | 726 | in range |
| `corpus/README.md:361` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 361 | 726 | in range |
| `corpus/README.md:448` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 448 | 726 | in range |
| `corpus/README.md:49` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 49 | 726 | in range |
| `corpus/README.md:54` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 54 | 726 | in range |
| `corpus/README.md:591` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 591 | 726 | in range |
| `corpus/README.md:702` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 702 | 726 | in range |
| `corpus/README.md:82` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 82 | 726 | in range |
| `corpus/SOURCES.md:157` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 157 | 182 | in range |
| `corpus/SOURCES.md:22` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 22 | 182 | in range |
| `corpus/SOURCES.md:40` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 40 | 182 | in range |
| `corpus/SOURCES.md:47` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 47 | 182 | in range |
| `corpus/SOURCES.md:48` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 48 | 182 | in range |
| `corpus/SOURCES.md:54` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 54 | 182 | in range |
| `corpus/SOURCES.md:55-56` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 55-56 | 182 | in range |
| `corpus/SOURCES.md:56` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 56 | 182 | in range |
| `corpus/SOURCES.md:57` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 57 | 182 | in range |
| `corpus/SOURCES.md:58` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 58 | 182 | in range |
| `corpus/SOURCES.md:61` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 61 | 182 | in range |
| `corpus/SOURCES.md:62` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 62 | 182 | in range |
| `corpus/SOURCES.md:62-65` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 62-65 | 182 | in range |
| `corpus/SOURCES.md:74` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 74 | 182 | in range |
| `corpus/SOURCES.md:79` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 79 | 182 | in range |
| `corpus/SOURCES.md:82` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 82 | 182 | in range |
| `corpus/SOURCES.md:83` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 83 | 182 | in range |
| `corpus/SOURCES.md:90` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 90 | 182 | in range |
| `corpus/instruments/README.md:1000` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/README.md` | 1000 | 1023 | in range |
| `corpus/instruments/README.md:131` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/README.md` | 131 | 1023 | in range |
| `corpus/instruments/README.md:16-17` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/README.md` | 16-17 | 1023 | in range |
| `corpus/instruments/README.md:31-38` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/README.md` | 31-38 | 1023 | in range |
| `corpus/instruments/README.md:63` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/README.md` | 63 | 1023 | in range |
| `corpus/instruments/capture-binding-check.py:1-92` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py` | 1-92 | 1129 | in range |
| `corpus/instruments/capture-binding-check.py:166-181` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py` | 166-181 | 1129 | in range |
| `corpus/instruments/capture-binding-check.py:184-262` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py` | 184-262 | 1129 | in range |
| `corpus/instruments/capture-binding-check.py:67-68` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py` | 67-68 | 1129 | in range |
| `corpus/instruments/capture-binding-check.py:80` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py` | 80 | 1129 | in range |
| `corpus/instruments/claim-package-check.py:101-108` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 101-108 | 802 | in range |
| `corpus/instruments/claim-package-check.py:120` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 120 | 802 | in range |
| `corpus/instruments/claim-package-check.py:121` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 121 | 802 | in range |
| `corpus/instruments/claim-package-check.py:138-140` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 138-140 | 802 | in range |
| `corpus/instruments/claim-package-check.py:185-187` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 185-187 | 802 | in range |
| `corpus/instruments/claim-package-check.py:2-8` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 2-8 | 802 | in range |
| `corpus/instruments/claim-package-check.py:305` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 305 | 802 | in range |
| `corpus/instruments/claim-package-check.py:307-309` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 307-309 | 802 | in range |
| `corpus/instruments/claim-package-check.py:332-335` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 332-335 | 802 | in range |
| `corpus/instruments/claim-package-check.py:334` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 334 | 802 | in range |
| `corpus/instruments/claim-package-check.py:340-347` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 340-347 | 802 | in range |
| `corpus/instruments/claim-package-check.py:354` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 354 | 802 | in range |
| `corpus/instruments/claim-package-check.py:354-355` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 354-355 | 802 | in range |
| `corpus/instruments/claim-package-check.py:4-8` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 4-8 | 802 | in range |
| `corpus/instruments/claim-package-check.py:407-409` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 407-409 | 802 | in range |
| `corpus/instruments/claim-package-check.py:413-415` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 413-415 | 802 | in range |
| `corpus/instruments/claim-package-check.py:413-416` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 413-416 | 802 | in range |
| `corpus/instruments/claim-package-check.py:457-458` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 457-458 | 802 | in range |
| `corpus/instruments/claim-package-check.py:460` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 460 | 802 | in range |
| `corpus/instruments/claim-package-check.py:460-461` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 460-461 | 802 | in range |
| `corpus/instruments/claim-package-check.py:465-467` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 465-467 | 802 | in range |
| `corpus/instruments/claim-package-check.py:467` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 467 | 802 | in range |
| `corpus/instruments/claim-package-check.py:469-472` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 469-472 | 802 | in range |
| `corpus/instruments/claim-package-check.py:471` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 471 | 802 | in range |
| `corpus/instruments/claim-package-check.py:489-491` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 489-491 | 802 | in range |
| `corpus/instruments/claim-package-check.py:497` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 497 | 802 | in range |
| `corpus/instruments/claim-package-check.py:515-516` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 515-516 | 802 | in range |
| `corpus/instruments/claim-package-check.py:524-525` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 524-525 | 802 | in range |
| `corpus/instruments/claim-package-check.py:527-528` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 527-528 | 802 | in range |
| `corpus/instruments/claim-package-check.py:584-589` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 584-589 | 802 | in range |
| `corpus/instruments/claim-package-check.py:585-588` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 585-588 | 802 | in range |
| `corpus/instruments/claim-package-check.py:594-613` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 594-613 | 802 | in range |
| `corpus/instruments/claim-package-check.py:595-614` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 595-614 | 802 | in range |
| `corpus/instruments/claim-package-check.py:598-606` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 598-606 | 802 | in range |
| `corpus/instruments/claim-package-check.py:607` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 607 | 802 | in range |
| `corpus/instruments/claim-package-check.py:607-608` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 607-608 | 802 | in range |
| `corpus/instruments/claim-package-check.py:617-619` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 617-619 | 802 | in range |
| `corpus/instruments/claim-package-check.py:634-635` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 634-635 | 802 | in range |
| `corpus/instruments/claim-package-check.py:636-637` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 636-637 | 802 | in range |
| `corpus/instruments/claim-package-check.py:656-660` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 656-660 | 802 | in range |
| `corpus/instruments/claim-package-check.py:672-674` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 672-674 | 802 | in range |
| `corpus/instruments/fixtures/claim-package/defect-8-marker/expected-rule:1` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/fixtures/claim-package/defect-8-marker/expected-rule` | 1 | 1 | in range |
| `corpus/instruments/fixtures/claim-package/defect-9-secret/expected-rule:1` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/fixtures/claim-package/defect-9-secret/expected-rule` | 1 | 1 | in range |
| `corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json:2` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json` | 2 | 85 | in range |
| `corpus/instruments/fixtures/claim-package/exemplar/provenance.json:88` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/fixtures/claim-package/exemplar/provenance.json` | 88 | 95 | in range |
| `corpus/instruments/fixtures/claim-package/exemplar/report.md:88` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/fixtures/claim-package/exemplar/report.md` | 88 | 88 | in range |
| `corpus/instruments/r35-defect-closure.sh:164-168` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-defect-closure.sh` | 164-168 | 834 | in range |
| `corpus/instruments/r35-defect-closure.sh:192` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-defect-closure.sh` | 192 | 834 | in range |
| `corpus/instruments/r35-defect-closure.sh:50-52` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-defect-closure.sh` | 50-52 | 834 | in range |
| `corpus/instruments/r36-closure.sh:309` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r36-closure.sh` | 309 | 894 | in range |
| `corpus/instruments/r36-closure.sh:322` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r36-closure.sh` | 322 | 894 | in range |
| `corpus/instruments/r36-closure.sh:465` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r36-closure.sh` | 465 | 894 | in range |
| `corpus/instruments/r36-closure.sh:466` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r36-closure.sh` | 466 | 894 | in range |
| `corpus/instruments/r36-closure.sh:480-481` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r36-closure.sh` | 480-481 | 894 | in range |
| `corpus/instruments/r36-closure.sh:766-768` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r36-closure.sh` | 766-768 | 894 | in range |
| `corpus/instruments/r36-closure.sh:93-108` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r36-closure.sh` | 93-108 | 894 | in range |
| `corpus/instruments/r37-closure.sh:59-64` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r37-closure.sh` | 59-64 | 1558 | in range |
| `corpus/instruments/r41-closure.sh:1392-1405` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r41-closure.sh` | 1392-1405 | 2209 | in range |
| `corpus/instruments/r41-closure.sh:443-459` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r41-closure.sh` | 443-459 | 2209 | in range |
| `corpus/instruments/r41-closure.sh:891-914` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r41-closure.sh` | 891-914 | 2209 | in range |
| `corpus/instruments/r46-c2-gate.py:329` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-c2-gate.py` | 329 | 414 | in range |
| `corpus/instruments/r46-counters-selftest-c2.py:537` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-counters-selftest-c2.py` | 537 | 830 | in range |
| `corpus/instruments/r46-f29-gate.py:80` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py` | 80 | 391 | in range |
| `corpus/instruments/r46-landing-gate.py:113` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-landing-gate.py` | 113 | 638 | in range |
| `corpus/instruments/resolve.py:161-163` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py` | 161-163 | 623 | in range |
| `corpus/instruments/resolve.py:164-172` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py` | 164-172 | 623 | in range |
| `corpus/instruments/resolve.py:31-48` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py` | 31-48 | 623 | in range |
| `corpus/instruments/resolve.py:74` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py` | 74 | 623 | in range |
| `corpus/instruments/score-gap.py:76` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/score-gap.py` | 76 | 554 | in range |
| `corpus/instruments/source-recheck.py:275` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py` | 275 | 415 | in range |
| `corpus/knowledge/authorization-safe-harbor-and-scope.md:8` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/authorization-safe-harbor-and-scope.md` | 8 | 46 | in range |
| `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md:97` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` | 97 | 306 | in range |
| `corpus/knowledge/claim-gates.md:15` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 15 | 160 | in range |
| `corpus/knowledge/claim-gates.md:3` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 3 | 160 | in range |
| `corpus/knowledge/claim-gates.md:45-47` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 45-47 | 160 | in range |
| `corpus/knowledge/claim-package-contract.md:11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 11 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:11-16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 11-16 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:13` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 13 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:14` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 14 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:15` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 15 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 16 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:18-26` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 18-26 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:22-23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 22-23 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:31` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 31 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:7` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 7 | 99 | in range |
| `corpus/knowledge/cna-assignment-and-vulnerability-rules.md:36` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/cna-assignment-and-vulnerability-rules.md` | 36 | 80 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:119-131` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/considerthese-proposals-ledger.md` | 119-131 | 166 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:13` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/considerthese-proposals-ledger.md` | 13 | 166 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:22-33` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/considerthese-proposals-ledger.md` | 22-33 | 166 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:3` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/considerthese-proposals-ledger.md` | 3 | 166 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:37` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/considerthese-proposals-ledger.md` | 37 | 166 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:22` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/coordinated-disclosure-timelines.md` | 22 | 44 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:24` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/coordinated-disclosure-timelines.md` | 24 | 44 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:24-25` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/coordinated-disclosure-timelines.md` | 24-25 | 44 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:6-17` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/coordinated-disclosure-timelines.md` | 6-17 | 44 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:7-17` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/coordinated-disclosure-timelines.md` | 7-17 | 44 | in range |
| `corpus/knowledge/cvss-v4-severity-and-vector.md:2` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/cvss-v4-severity-and-vector.md` | 2 | 48 | in range |
| `corpus/knowledge/cvss-v4-severity-and-vector.md:34` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/cvss-v4-severity-and-vector.md` | 34 | 48 | in range |
| `corpus/knowledge/ev-model.md:37-38` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ev-model.md` | 37-38 | 60 | in range |
| `corpus/knowledge/evidence-dir.md:78` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/evidence-dir.md` | 78 | 91 | in range |
| `corpus/knowledge/github-private-vulnerability-reporting.md:40` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/github-private-vulnerability-reporting.md` | 40 | 49 | in range |
| `corpus/knowledge/github-repository-security-advisories.md:11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/github-repository-security-advisories.md` | 11 | 145 | in range |
| `corpus/knowledge/intake-and-finalize.md:78-92` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/intake-and-finalize.md` | 78-92 | 111 | in range |
| `corpus/knowledge/mission-control.md:3` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 3 | 171 | in range |
| `corpus/knowledge/ops-invariants.md:18` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 18 | 141 | in range |
| `corpus/knowledge/ops-invariants.md:24` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 24 | 141 | in range |
| `corpus/knowledge/policy-access-playbook.md:13` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/policy-access-playbook.md` | 13 | 35 | in range |
| `corpus/knowledge/program-quirks.md:10` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/program-quirks.md` | 10 | 67 | in range |
| `corpus/knowledge/program-severity-ladders-and-reward-scales.md:16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/program-severity-ladders-and-reward-scales.md` | 16 | 67 | in range |
| `corpus/knowledge/retirement-autopsies.md:38` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/retirement-autopsies.md` | 38 | 141 | in range |
| `corpus/knowledge/statutory-authorization-and-unauthorized-access.md:46` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/statutory-authorization-and-unauthorized-access.md` | 46 | 98 | in range |
| `corpus/knowledge/submitted-registry.md:105` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/submitted-registry.md` | 105 | 229 | in range |
| `corpus/knowledge/submitted-registry.md:138-141` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/submitted-registry.md` | 138-141 | 229 | in range |
| `corpus/knowledge/submitted-registry.md:146-148` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/submitted-registry.md` | 146-148 | 229 | in range |
| `corpus/knowledge/submitted-registry.md:207-209` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/submitted-registry.md` | 207-209 | 229 | in range |
| `corpus/knowledge/submitted-registry.md:27` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/submitted-registry.md` | 27 | 229 | in range |
| `corpus/knowledge/submitted-registry.md:9` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/submitted-registry.md` | 9 | 229 | in range |
| `corpus/knowledge/triage-thresholds.md:25` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/triage-thresholds.md` | 25 | 487 | in range |
| `corpus/knowledge/ufo-archive-2026.md:11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ufo-archive-2026.md` | 11 | 210 | in range |
| `corpus/knowledge/ufo-archive-2026.md:145-149` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ufo-archive-2026.md` | 145-149 | 210 | in range |
| `corpus/knowledge/ufo-archive-2026.md:150-154` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ufo-archive-2026.md` | 150-154 | 210 | in range |
| `corpus/knowledge/ufo-archive-2026.md:36` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ufo-archive-2026.md` | 36 | 210 | in range |
| `corpus/knowledge/vendor-third-party-finding-coordination.md:114-120` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/vendor-third-party-finding-coordination.md` | 114-120 | 172 | in range |
| `corpus/knowledge/vendor-third-party-finding-coordination.md:17-39` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/vendor-third-party-finding-coordination.md` | 17-39 | 172 | in range |
| `corpus/knowledge/vendor-third-party-finding-coordination.md:41-59` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/vendor-third-party-finding-coordination.md` | 41-59 | 172 | in range |
| `corpus/knowledge/vendor-third-party-finding-coordination.md:91-96` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/vendor-third-party-finding-coordination.md` | 91-96 | 172 | in range |
| `corpus/lessons/round-20-recensus.md:20` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-20-recensus.md` | 20 | 43 | in range |
| `corpus/lessons/round-20-recensus.md:29` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-20-recensus.md` | 29 | 43 | in range |
| `corpus/lessons/round-20-recensus.md:33` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-20-recensus.md` | 33 | 43 | in range |
| `corpus/lessons/round-20-recensus.md:34-35` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-20-recensus.md` | 34-35 | 43 | in range |
| `corpus/lessons/round-20-recensus.md:37-39` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-20-recensus.md` | 37-39 | 43 | in range |
| `corpus/lessons/round-20-recensus.md:39` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-20-recensus.md` | 39 | 43 | in range |
| `corpus/lessons/round-20-recensus.md:43` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-20-recensus.md` | 43 | 43 | in range |
| `corpus/lessons/round-21-routing-blocked.md:115` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-21-routing-blocked.md` | 115 | 145 | in range |
| `corpus/lessons/round-22.md:91` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-22.md` | 91 | 155 | in range |
| `corpus/lessons/round-24.md:77` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-24.md` | 77 | 229 | in range |
| `corpus/lessons/round-29-verifier-spotcheck.md:74` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-29-verifier-spotcheck.md` | 74 | 104 | in range |
| `corpus/lessons/round-29.md:214` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-29.md` | 214 | 337 | in range |
| `corpus/lessons/round-29.md:219` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-29.md` | 219 | 337 | in range |
| `corpus/lessons/round-29.md:221` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-29.md` | 221 | 337 | in range |
| `corpus/lessons/round-30-verifier-spotcheck.md:12` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-30-verifier-spotcheck.md` | 12 | 71 | in range |
| `corpus/lessons/round-30.md:82` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-30.md` | 82 | 118 | in range |
| `corpus/lessons/round-31.md:146` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-31.md` | 146 | 175 | in range |
| `corpus/lessons/round-31.md:147` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-31.md` | 147 | 175 | in range |
| `corpus/lessons/round-32-verifier-spotcheck.md:73` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-32-verifier-spotcheck.md` | 73 | 96 | in range |
| `corpus/lessons/round-32-verifier-spotcheck.md:93` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-32-verifier-spotcheck.md` | 93 | 96 | in range |
| `corpus/lessons/round-33-verifier-spotcheck.md:167-169` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-33-verifier-spotcheck.md` | 167-169 | 195 | in range |
| `corpus/lessons/round-33-verifier-spotcheck.md:174` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-33-verifier-spotcheck.md` | 174 | 195 | in range |
| `corpus/lessons/round-33-verifier-spotcheck.md:174-176` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-33-verifier-spotcheck.md` | 174-176 | 195 | in range |
| `corpus/lessons/round-33-verifier-spotcheck.md:181` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-33-verifier-spotcheck.md` | 181 | 195 | in range |
| `corpus/lessons/round-33.md:140` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-33.md` | 140 | 247 | in range |
| `corpus/lessons/round-33.md:215-226` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-33.md` | 215-226 | 247 | in range |
| `corpus/lessons/round-33.md:31-32` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-33.md` | 31-32 | 247 | in range |
| `corpus/lessons/round-34-verifier-spotcheck.md:173` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-34-verifier-spotcheck.md` | 173 | 209 | in range |
| `corpus/lessons/round-34-verifier-spotcheck.md:177` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-34-verifier-spotcheck.md` | 177 | 209 | in range |
| `corpus/lessons/round-34-verifier-spotcheck.md:199-203` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-34-verifier-spotcheck.md` | 199-203 | 209 | in range |
| `corpus/lessons/round-34.md:343-358` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-34.md` | 343-358 | 561 | in range |
| `corpus/lessons/round-34.md:482-485` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-34.md` | 482-485 | 561 | in range |
| `corpus/lessons/round-35-verifier-spotcheck.md:10-20` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-35-verifier-spotcheck.md` | 10-20 | 144 | in range |
| `corpus/lessons/round-35-verifier-spotcheck.md:127-129` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-35-verifier-spotcheck.md` | 127-129 | 144 | in range |
| `corpus/lessons/round-35-verifier-spotcheck.md:132-134` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-35-verifier-spotcheck.md` | 132-134 | 144 | in range |
| `corpus/lessons/round-35.md:155-169` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-35.md` | 155-169 | 529 | in range |
| `corpus/lessons/round-35.md:282-290` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-35.md` | 282-290 | 529 | in range |
| `corpus/lessons/round-36-verifier-spotcheck.md:160-162` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-36-verifier-spotcheck.md` | 160-162 | 164 | in range |
| `corpus/lessons/round-36.md:3` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-36.md` | 3 | 45 | in range |
| `corpus/lessons/round-36.md:39` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-36.md` | 39 | 45 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:105-111` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37-verifier-spotcheck.md` | 105-111 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:113-118` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37-verifier-spotcheck.md` | 113-118 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:159-164` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37-verifier-spotcheck.md` | 159-164 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:165-168` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37-verifier-spotcheck.md` | 165-168 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:169-174` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37-verifier-spotcheck.md` | 169-174 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:175-177` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37-verifier-spotcheck.md` | 175-177 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:50-56` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37-verifier-spotcheck.md` | 50-56 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:8-10` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37-verifier-spotcheck.md` | 8-10 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:90` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37-verifier-spotcheck.md` | 90 | 186 | in range |
| `corpus/lessons/round-37-verifier-spotcheck.md:95` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37-verifier-spotcheck.md` | 95 | 186 | in range |
| `corpus/lessons/round-37.md:268-270` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37.md` | 268-270 | 350 | in range |
| `corpus/lessons/round-37.md:271` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37.md` | 271 | 350 | in range |
| `corpus/lessons/round-37.md:272-273` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37.md` | 272-273 | 350 | in range |
| `corpus/lessons/round-37.md:274-276` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37.md` | 274-276 | 350 | in range |
| `corpus/lessons/round-37.md:277` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37.md` | 277 | 350 | in range |
| `corpus/lessons/round-37.md:278` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37.md` | 278 | 350 | in range |
| `corpus/lessons/round-37.md:279-286` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37.md` | 279-286 | 350 | in range |
| `corpus/lessons/round-37.md:85` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-37.md` | 85 | 350 | in range |
| `corpus/lessons/round-38-verifier-spotcheck.md:155-160` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-38-verifier-spotcheck.md` | 155-160 | 180 | in range |
| `corpus/lessons/round-38-verifier-spotcheck.md:168-171` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-38-verifier-spotcheck.md` | 168-171 | 180 | in range |
| `corpus/lessons/round-38-verifier-spotcheck.md:172-174` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-38-verifier-spotcheck.md` | 172-174 | 180 | in range |
| `corpus/lessons/round-38.md:21` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-38.md` | 21 | 311 | in range |
| `corpus/lessons/round-38.md:287` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-38.md` | 287 | 311 | in range |
| `corpus/lessons/round-38.md:94` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-38.md` | 94 | 311 | in range |
| `corpus/lessons/round-39-verifier-spotcheck.md:181-182` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-39-verifier-spotcheck.md` | 181-182 | 192 | in range |
| `corpus/lessons/round-39.md:15` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-39.md` | 15 | 105 | in range |
| `corpus/lessons/round-39.md:36-42` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-39.md` | 36-42 | 105 | in range |
| `corpus/lessons/round-39.md:77` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-39.md` | 77 | 105 | in range |
| `corpus/lessons/round-39.md:78` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-39.md` | 78 | 105 | in range |
| `corpus/lessons/round-4-aggregator-audit.md:26` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-4-aggregator-audit.md` | 26 | 70 | in range |
| `corpus/lessons/round-4-aggregator-audit.md:28` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-4-aggregator-audit.md` | 28 | 70 | in range |
| `corpus/lessons/round-40-verifier-spotcheck.md:176-180` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-40-verifier-spotcheck.md` | 176-180 | 213 | in range |
| `corpus/lessons/round-41-verifier-spotcheck.md:132-134` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-41-verifier-spotcheck.md` | 132-134 | 155 | in range |
| `corpus/lessons/round-41-verifier-spotcheck.md:148-149` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-41-verifier-spotcheck.md` | 148-149 | 155 | in range |
| `corpus/lessons/round-41.md:103-107` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-41.md` | 103-107 | 122 | in range |
| `corpus/lessons/round-41.md:108-110` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-41.md` | 108-110 | 122 | in range |
| `corpus/lessons/round-42-verifier-spotcheck.md:178` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-42-verifier-spotcheck.md` | 178 | 316 | in range |
| `corpus/lessons/round-42-verifier-spotcheck.md:65` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-42-verifier-spotcheck.md` | 65 | 316 | in range |
| `corpus/lessons/round-42.md:11-16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-42.md` | 11-16 | 152 | in range |
| `corpus/lessons/round-42.md:52` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-42.md` | 52 | 152 | in range |
| `corpus/lessons/round-43.md:90` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-43.md` | 90 | 175 | in range |
| `corpus/lessons/round-44.md:125` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-44.md` | 125 | 205 | in range |
| `corpus/lessons/round-44.md:126` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-44.md` | 126 | 205 | in range |
| `corpus/lessons/round-44.md:131` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-44.md` | 131 | 205 | in range |
| `corpus/lessons/round-44.md:15` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-44.md` | 15 | 205 | in range |
| `corpus/lessons/round-44.md:16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-44.md` | 16 | 205 | in range |
| `corpus/lessons/round-44.md:189` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-44.md` | 189 | 205 | in range |
| `corpus/lessons/round-44.md:22` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-44.md` | 22 | 205 | in range |
| `corpus/lessons/round-45-verifier-spotcheck.md:22` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-45-verifier-spotcheck.md` | 22 | 103 | in range |
| `corpus/lessons/round-45-verifier-spotcheck.md:98` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-45-verifier-spotcheck.md` | 98 | 103 | in range |
| `corpus/lessons/round-46.md:29` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-46.md` | 29 | 161 | in range |
| `corpus/lessons/round-5.md:16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-5.md` | 16 | 38 | in range |
| `corpus/lessons/round-8.md:10` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-8.md` | 10 | 53 | in range |
| `corpus/lessons/round-9.md:33` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-9.md` | 33 | 63 | in range |
| `corpus/source-snapshots/round-23/S029.txt:14` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-23/S029.txt` | 14 | 146 | in range |
| `corpus/source-snapshots/round-31/S048.txt:35` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-31/S048.txt` | 35 | 97 | in range |
| `corpus/source-snapshots/round-32/S050.txt:70` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-32/S050.txt` | 70 | 630 | in range |
| `corpus/source-snapshots/round-43/S067.txt:69` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-43/S067.txt` | 69 | 109 | in range |
| `corpus/source-snapshots/round-43/S067.txt:83` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-43/S067.txt` | 83 | 109 | in range |
| `corpus/source-snapshots/round-43/S067.txt:88` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-43/S067.txt` | 88 | 109 | in range |
| `corpus/source-snapshots/round-44/S069.txt:61` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-44/S069.txt` | 61 | 1132 | in range |
| `corpus/source-snapshots/round-45/S071.txt:310-311` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 310-311 | 372 | in range |
| `corpus/source-snapshots/round-47/S076.txt:574` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 574 | 610 | in range |

Every MIRROR-EQUIVALENT anchor in range is still only a *same-name same-path*
match against a Sep-5 genesis sync — see §Honest scope limits.

## Top-20 most-cited GONE paths

| # | citation | files citing | occurrences | noise flags |
|---|---|---|---|---|
| 1 | `[~]` | 32 | 64 | synthetic |
| 2 | `anchorcheck.py` | 26 | 41 | - |
| 3 | `density.py` | 25 | 34 | - |
| 4 | `claims.json` | 22 | 46 | - |
| 5 | `claims/` | 21 | 35 | - |
| 6 | `status.json` | 20 | 46 | - |
| 7 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 20 | 21 | shell,synthetic |
| 8 | `source-recheck.py` | 19 | 30 | - |
| 9 | `ops/claim-check.mjs` | 18 | 37 | - |
| 10 | `frontier-recheck-count.py` | 18 | 30 | - |
| 11 | `census-before.txt` | 18 | 24 | - |
| 12 | `SOURCES.md` | 18 | 23 | - |
| 13 | `c2-controls/before.txt` | 17 | 26 | - |
| 14 | `.ufo/watchdog.log` | 17 | 17 | - |
| 15 | `resolve.py` | 16 | 33 | - |
| 16 | `~/Projects/bounties` | 16 | 23 | - |
| 17 | `george/` | 15 | 19 | - |
| 18 | `fleets/registry.json` | 14 | 18 | - |
| 19 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 14 | 17 | shell,synthetic |
| 20 | `evidence/` | 13 | 22 | - |

Max over all citations: files citing = 68, occurrences = 184.

## MIRROR-EQUIVALENT — exact list (0)

| # | citation | mirror path | lines | files | method |
|---|---|---|---|---|---|
