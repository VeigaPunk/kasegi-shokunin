Instrument: `corpus/instruments/resolve.py` (stdlib-only, deterministic; r18 definition).
Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (measured from the git-archive extract of `e2caf4a1561b544a6ea684b0bcfa975f7e7f6061`)
Scope: `SKILL.md` + `corpus/**/*.md` (334 files).
Extraction: verbatim density.py docstring path-like rule (see module docstring).
Mirror root for bounty-path equivalence: `/home/vgpnk/Projects/the-bounty-hunter` (ABSENT — mirror fallback disabled).

## Totals

- distinct path-like citations: **7961** (total occurrences: 16435; a citation cited in both scopes counts once)
- distinct citations appearing in SKILL.md: 732 (of which SKILL-only: 402)
- distinct citations appearing in corpus: 7559

| class | distinct citations |
|---|---|
| RESOLVES | 78 |
| MIRROR-EQUIVALENT | 0 |
| GONE | 5294 |
| INTERNAL | 2589 |
| OTHER *(root-domain bucket, orthogonal: the brief says classify other roots as RESOLVES/GONE)* | 78 resolve / 180 gone = 258 |

Terminal outcome classes sum to the distinct total: RESOLVES(78) + MIRROR-EQUIVALENT(0) + INTERNAL(2589) + GONE(5294) = 7961.
Of the 78 RESOLVES, 78 are non-lane roots (domain `other`: origin-work, /tmp, ~/projects …); 0 are lane-repo-absolute.
Of the 0 MIRROR-EQUIVALENT, 0 were written as `~/Projects/bounties/...` (domain `bounty`), 0 were bounty-root-relative bare paths (domain `rel`).

## Resolvability rate

Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citations appearing in that scope (a citation in both scopes enters both denominators).

- SKILL.md alone: **166/732 = 22.68%**
- corpus alone: **2629/7559 = 34.78%**
- lane total (SKILL.md + corpus): **2667/7961 = 33.50%**

## Noise sub-census (GONE tokens that are rule artifacts, not citable paths)

Flag counts (a token can carry several flags):

| flags | distinct GONE citations |
|---|---|
| gitstatus | 14 |
| gitstatus,synthetic | 12 |
| regex | 25 |
| regex,synthetic | 7 |
| shell | 681 |
| shell,synthetic | 298 |
| synthetic | 744 |

- GONE citations carrying any noise flag: 1781
- GONE citations with no noise flag (genuine vanished paths): 3513
- citations containing glob/placeholder syntax (`* ? [ { } <...>`): 1142

Noise-adjusted rates (denominator excludes noise-flagged citations):
- SKILL: 162/371 = 43.67%
- CORPUS: 2548/5996 = 42.49%
- ALL: 2585/6098 = 42.39%

## Scope x class matrix

| class | SKILL.md only | SKILL+corpus | corpus only | total |
|---|---|---|---|---|
| RESOLVES | 0 | 4 | 74 | 78 |
| MIRROR-EQUIVALENT | 0 | 0 | 0 | 0 |
| GONE | 364 | 202 | 4728 | 5294 |
| INTERNAL | 38 | 124 | 2427 | 2589 |

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

Result: both yield **7961** distinct citations, and
`diff <(pipeline to file) <(cut -f1 citation-survival.tsv | tail -n +2 | sort -u)` is empty (sets identical, not just counts).
Re-running `resolve.py` twice leaves both outputs byte-identical (md5 stable).

## Honest scope limits

- MIRROR-EQUIVALENT means the same relative path exists in the Sep-5 genesis mirror `~/Projects/the-bounty-hunter`; it does NOT establish byte-equivalence with the vanished tree, and the mirror holds the code half only.
- Glob/brace citations resolve if any deterministic expansion exists; a glob with zero matches is GONE (e.g. `bounty-map/programs/*.json`).
- The path-like rule (verbatim from density.py) admits regex literals, git-porcelain snippets and shell fragments; the noise sub-census quantifies them so the raw rate can be read against the noise-adjusted rate.

## Line-anchor viability (resolvable citations carrying `:NN` / `:NN-MM`)

For every citation whose base resolves and whose anchor names a file, the anchor
is compared against the resolved file's line count (editor convention).

- anchors checked: 1257 — in range: 1238 — **out of range: 19**

| citation | class | resolved file | anchor | file lines | verdict |
|---|---|---|---|---|---|
| `./PROVINCE.md:3` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 3 | 237 | in range |
| `.gitignore:11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.gitignore` | 11 | 2 | OUT OF RANGE |
| `.gitignore:2` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.gitignore` | 2 | 2 | in range |
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
| `.ufo/waves/round-53/controls/c2-counter-final-r53.txt:8` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-53/controls/c2-counter-final-r53.txt` | 8 | 10 | in range |
| `.ufo/waves/round-53/controls/c2-counter-final-r53.txt:9` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-53/controls/c2-counter-final-r53.txt` | 9 | 10 | in range |
| `.ufo/waves/round-54/claims.json:14` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-54/claims.json` | 14 | 46 | in range |
| `.ufo/waves/round-60/controls/freeze-digests-r60.txt:1` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-60/controls/freeze-digests-r60.txt` | 1 | 3 | in range |
| `.ufo/waves/round-63/controls/collector-candidate-prefreeze-r63.txt:12` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-63/controls/collector-candidate-prefreeze-r63.txt` | 12 | 14 | in range |
| `.ufo/waves/round-79/c1/mutbat.py:40` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-79/c1/mutbat.py` | 40 | 180 | in range |
| `.ufo/waves/round-79/c1/mutbat.py:41` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-79/c1/mutbat.py` | 41 | 180 | in range |
| `.ufo/waves/round-82/c1/mutbat.py:221` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-82/c1/mutbat.py` | 221 | 445 | in range |
| `.ufo/waves/round-83/c1/mutbat.py:256` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-83/c1/mutbat.py` | 256 | 617 | in range |
| `.ufo/waves/round-83/c1/mutbat.py:313` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-83/c1/mutbat.py` | 313 | 617 | in range |
| `.ufo/waves/round-83/c1/recheck-cwd-census.py:685` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-83/c1/recheck-cwd-census.py` | 685 | 850 | in range |
| `.ufo/waves/round-83/c2/entry-gate.py:45` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-83/c2/entry-gate.py` | 45 | 250 | in range |
| `.ufo/waves/round-83/c2/entry-gate.py:85` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-83/c2/entry-gate.py` | 85 | 250 | in range |
| `.ufo/waves/round-86/l1/redact-presigned.py:5-6` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/l1/redact-presigned.py` | 5-6 | 46 | in range |
| `.ufo/waves/round-87/w1/ConnectorOverlap.md:158-176` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-87/w1/ConnectorOverlap.md` | 158-176 | 189 | in range |
| `.ufo/waves/round-88/controls/c2-controls-r88.txt:2-9` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-88/controls/c2-controls-r88.txt` | 2-9 | 131 | in range |
| `.ufo/waves/round-89/l1/c2-landing-r89.txt:4` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-89/l1/c2-landing-r89.txt` | 4 | 20 | in range |
| `.ufo/waves/round-89/l1/c2-landing-r89.txt:8` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-89/l1/c2-landing-r89.txt` | 8 | 20 | in range |
| `.ufo/waves/round-90/controls/c2-controls-r90.txt:51-61` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-90/controls/c2-controls-r90.txt` | 51-61 | 94 | in range |
| `.ufo/waves/round-90/controls/c2-controls-r90.txt:67-68` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-90/controls/c2-controls-r90.txt` | 67-68 | 94 | in range |
| `.ufo/waves/round-90/l1/c2-landing-r90.txt:1` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-90/l1/c2-landing-r90.txt` | 1 | 51 | in range |
| `.ufo/waves/round-90/l1/c2-landing-r90.txt:3-12` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-90/l1/c2-landing-r90.txt` | 3-12 | 51 | in range |
| `.ufo/waves/round-90/l1/c2-landing-r90.txt:4` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-90/l1/c2-landing-r90.txt` | 4 | 51 | in range |
| `.ufo/waves/round-90/l1/c2-landing-r90.txt:5` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-90/l1/c2-landing-r90.txt` | 5 | 51 | in range |
| `.ufo/waves/round-90/l1/c2-landing-r90.txt:5-6` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-90/l1/c2-landing-r90.txt` | 5-6 | 51 | in range |
| `.ufo/waves/round-90/l1/c2-landing-r90.txt:9` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-90/l1/c2-landing-r90.txt` | 9 | 51 | in range |
| `.ufo/waves/round-92/w1/ReviewC1Sites.md:17-28` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-92/w1/ReviewC1Sites.md` | 17-28 | 103 | in range |
| `.ufo/waves/round-94/controls/c2-controls-r94.txt:110` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-94/controls/c2-controls-r94.txt` | 110 | 122 | in range |
| `.ufo/waves/round-94/w1/ScoutGitLabRules-receipts/06-github-firstparty-examples.txt:10` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-94/w1/ScoutGitLabRules-receipts/06-github-firstparty-examples.txt` | 10 | 34 | in range |
| `.ufo/waves/round-94/w1/ScoutGitLabRules-receipts/08-github-rules-file.txt:16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-94/w1/ScoutGitLabRules-receipts/08-github-rules-file.txt` | 16 | 20 | in range |
| `.ufo/waves/round-94/w1/SentinelShapes-receipts/08-unlisted-classes.txt:76` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-94/w1/SentinelShapes-receipts/08-unlisted-classes.txt` | 76 | 76 | in range |
| `.ufo/waves/round-95/controls/c1-controls-r95.txt:139-149` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-95/controls/c1-controls-r95.txt` | 139-149 | 150 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:353` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` | 353 | 389 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md:49` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md` | 49 | 89 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md:61` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md` | 61 | 89 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-37/kasegi.md:25` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-37/kasegi.md` | 25 | 88 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md:37` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md` | 37 | 87 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-40/kasegi.md:32` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-40/kasegi.md` | 32 | 65 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-57/kasegi.md:115` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-57/kasegi.md` | 115 | 128 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1490` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` | 1490 | 3233 | in range |
| `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1537` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` | 1537 | 3233 | in range |
| `/home/vgpnk/Projects/shokunin/CORPUS.md:101-104` | RESOLVES | `/home/vgpnk/Projects/shokunin/CORPUS.md` | 101-104 | 184 | in range |
| `/home/vgpnk/Projects/shokunin/MISSION.md:49-56` | RESOLVES | `/home/vgpnk/Projects/shokunin/MISSION.md` | 49-56 | 93 | in range |
| `/home/vgpnk/Projects/shokunin/PROTOCOL.md:457-461` | RESOLVES | `/home/vgpnk/Projects/shokunin/PROTOCOL.md` | 457-461 | 533 | in range |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/security-txt-publishing.md:63` | RESOLVES | `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/security-txt-publishing.md` | 63 | 156 | in range |
| `/usr/lib/python3.14/http/client.py:845-855` | RESOLVES | `/usr/lib/python3.14/http/client.py` | 845-855 | 1598 | in range |
| `LOG.md:1469` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1469 | 3102 | in range |
| `LOG.md:1550` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1550 | 3102 | in range |
| `LOG.md:1584` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1584 | 3102 | in range |
| `LOG.md:1665` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1665 | 3102 | in range |
| `LOG.md:1686` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1686 | 3102 | in range |
| `LOG.md:1728` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1728 | 3102 | in range |
| `LOG.md:1800-1801` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1800-1801 | 3102 | in range |
| `LOG.md:1804` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 1804 | 3102 | in range |
| `LOG.md:2045` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 2045 | 3102 | in range |
| `LOG.md:2205` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 2205 | 3102 | in range |
| `LOG.md:2599` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 2599 | 3102 | in range |
| `LOG.md:2610` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 2610 | 3102 | in range |
| `LOG.md:2611` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 2611 | 3102 | in range |
| `LOG.md:2813` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 2813 | 3102 | in range |
| `LOG.md:545` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 545 | 3102 | in range |
| `LOG.md:709-713` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 709-713 | 3102 | in range |
| `LOG.md:734` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 734 | 3102 | in range |
| `LOG.md:747-750` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 747-750 | 3102 | in range |
| `LOG.md:812` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` | 812 | 3102 | in range |
| `PROVINCE.md:0` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 0 | 237 | in range |
| `PROVINCE.md:16-22` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 16-22 | 237 | in range |
| `PROVINCE.md:165` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 165 | 237 | in range |
| `PROVINCE.md:171` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 171 | 237 | in range |
| `PROVINCE.md:178` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 178 | 237 | in range |
| `PROVINCE.md:211` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 211 | 237 | in range |
| `PROVINCE.md:31-40` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 31-40 | 237 | in range |
| `PROVINCE.md:38` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 38 | 237 | in range |
| `PROVINCE.md:75` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 75 | 237 | in range |
| `PROVINCE.md:77` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 77 | 237 | in range |
| `PROVINCE.md:78` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 78 | 237 | in range |
| `PROVINCE.md:80-152` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 80-152 | 237 | in range |
| `PROVINCE.md:90` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` | 90 | 237 | in range |
| `README.md:159` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/README.md` | 159 | 14 | OUT OF RANGE |
| `README.md:19` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/README.md` | 19 | 14 | OUT OF RANGE |
| `README.md:213` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/README.md` | 213 | 14 | OUT OF RANGE |
| `README.md:23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/README.md` | 23 | 14 | OUT OF RANGE |
| `README.md:30` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/README.md` | 30 | 14 | OUT OF RANGE |
| `SCORECARD.md:1014-1027` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1014-1027 | 3387 | in range |
| `SCORECARD.md:1014-1035` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1014-1035 | 3387 | in range |
| `SCORECARD.md:1074` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1074 | 3387 | in range |
| `SCORECARD.md:1078` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1078 | 3387 | in range |
| `SCORECARD.md:1116` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1116 | 3387 | in range |
| `SCORECARD.md:1116-1119` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1116-1119 | 3387 | in range |
| `SCORECARD.md:1129` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1129 | 3387 | in range |
| `SCORECARD.md:1145` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1145 | 3387 | in range |
| `SCORECARD.md:121-149` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 121-149 | 3387 | in range |
| `SCORECARD.md:1240` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1240 | 3387 | in range |
| `SCORECARD.md:1263-1281` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1263-1281 | 3387 | in range |
| `SCORECARD.md:1269` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1269 | 3387 | in range |
| `SCORECARD.md:1271` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1271 | 3387 | in range |
| `SCORECARD.md:1284` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1284 | 3387 | in range |
| `SCORECARD.md:134` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 134 | 3387 | in range |
| `SCORECARD.md:1492` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1492 | 3387 | in range |
| `SCORECARD.md:1505` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1505 | 3387 | in range |
| `SCORECARD.md:1509` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1509 | 3387 | in range |
| `SCORECARD.md:1532` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1532 | 3387 | in range |
| `SCORECARD.md:1547` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1547 | 3387 | in range |
| `SCORECARD.md:1567` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1567 | 3387 | in range |
| `SCORECARD.md:1595` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1595 | 3387 | in range |
| `SCORECARD.md:1602` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1602 | 3387 | in range |
| `SCORECARD.md:1602-1605` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1602-1605 | 3387 | in range |
| `SCORECARD.md:1605` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1605 | 3387 | in range |
| `SCORECARD.md:1634` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1634 | 3387 | in range |
| `SCORECARD.md:164` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 164 | 3387 | in range |
| `SCORECARD.md:174` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 174 | 3387 | in range |
| `SCORECARD.md:1788` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 1788 | 3387 | in range |
| `SCORECARD.md:228-290` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 228-290 | 3387 | in range |
| `SCORECARD.md:23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 23 | 3387 | in range |
| `SCORECARD.md:2420` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 2420 | 3387 | in range |
| `SCORECARD.md:2477` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 2477 | 3387 | in range |
| `SCORECARD.md:251` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 251 | 3387 | in range |
| `SCORECARD.md:252` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 252 | 3387 | in range |
| `SCORECARD.md:259-270` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 259-270 | 3387 | in range |
| `SCORECARD.md:307` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 307 | 3387 | in range |
| `SCORECARD.md:309` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 309 | 3387 | in range |
| `SCORECARD.md:309-321` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 309-321 | 3387 | in range |
| `SCORECARD.md:327` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 327 | 3387 | in range |
| `SCORECARD.md:331` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 331 | 3387 | in range |
| `SCORECARD.md:49-58` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 49-58 | 3387 | in range |
| `SCORECARD.md:502` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 502 | 3387 | in range |
| `SCORECARD.md:510` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 510 | 3387 | in range |
| `SCORECARD.md:65` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 65 | 3387 | in range |
| `SCORECARD.md:813` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 813 | 3387 | in range |
| `SCORECARD.md:813-819` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 813-819 | 3387 | in range |
| `SCORECARD.md:837` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 837 | 3387 | in range |
| `SCORECARD.md:88-96` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 88-96 | 3387 | in range |
| `SCORECARD.md:988` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` | 988 | 3387 | in range |
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
| `SHONEN.md:7` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` | 7 | 12 | in range |
| `SKILL.md:10` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 10 | 1251 | in range |
| `SKILL.md:1000` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1000 | 1251 | in range |
| `SKILL.md:1069` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1069 | 1251 | in range |
| `SKILL.md:1091` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1091 | 1251 | in range |
| `SKILL.md:1093-1104` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1093-1104 | 1251 | in range |
| `SKILL.md:1097` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1097 | 1251 | in range |
| `SKILL.md:1097-1098` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1097-1098 | 1251 | in range |
| `SKILL.md:1100` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1100 | 1251 | in range |
| `SKILL.md:1111` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1111 | 1251 | in range |
| `SKILL.md:1115` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1115 | 1251 | in range |
| `SKILL.md:1164` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1164 | 1251 | in range |
| `SKILL.md:117` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 117 | 1251 | in range |
| `SKILL.md:120` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 120 | 1251 | in range |
| `SKILL.md:1222-1225` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1222-1225 | 1251 | in range |
| `SKILL.md:1224` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1224 | 1251 | in range |
| `SKILL.md:1228` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 1228 | 1251 | in range |
| `SKILL.md:148` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 148 | 1251 | in range |
| `SKILL.md:149` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 149 | 1251 | in range |
| `SKILL.md:157-158` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 157-158 | 1251 | in range |
| `SKILL.md:161-162` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 161-162 | 1251 | in range |
| `SKILL.md:176-178` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 176-178 | 1251 | in range |
| `SKILL.md:182-184` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 182-184 | 1251 | in range |
| `SKILL.md:182-185` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 182-185 | 1251 | in range |
| `SKILL.md:184-187` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 184-187 | 1251 | in range |
| `SKILL.md:191` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 191 | 1251 | in range |
| `SKILL.md:224-226` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 224-226 | 1251 | in range |
| `SKILL.md:251-253` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 251-253 | 1251 | in range |
| `SKILL.md:255-257` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 255-257 | 1251 | in range |
| `SKILL.md:264-266` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 264-266 | 1251 | in range |
| `SKILL.md:321-324` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 321-324 | 1251 | in range |
| `SKILL.md:323` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 323 | 1251 | in range |
| `SKILL.md:331-335` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 331-335 | 1251 | in range |
| `SKILL.md:335-338` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 335-338 | 1251 | in range |
| `SKILL.md:340-346` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 340-346 | 1251 | in range |
| `SKILL.md:385` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 385 | 1251 | in range |
| `SKILL.md:413` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 413 | 1251 | in range |
| `SKILL.md:459` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 459 | 1251 | in range |
| `SKILL.md:494-506` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 494-506 | 1251 | in range |
| `SKILL.md:590-596` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 590-596 | 1251 | in range |
| `SKILL.md:597-608` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 597-608 | 1251 | in range |
| `SKILL.md:609-614` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 609-614 | 1251 | in range |
| `SKILL.md:615-621` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 615-621 | 1251 | in range |
| `SKILL.md:622-635` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 622-635 | 1251 | in range |
| `SKILL.md:636-639` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 636-639 | 1251 | in range |
| `SKILL.md:640-643` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 640-643 | 1251 | in range |
| `SKILL.md:644-651` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 644-651 | 1251 | in range |
| `SKILL.md:652-664` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 652-664 | 1251 | in range |
| `SKILL.md:665-679` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 665-679 | 1251 | in range |
| `SKILL.md:675` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 675 | 1251 | in range |
| `SKILL.md:8` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 8 | 1251 | in range |
| `SKILL.md:827-848` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 827-848 | 1251 | in range |
| `SKILL.md:828` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 828 | 1251 | in range |
| `SKILL.md:828-848` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 828-848 | 1251 | in range |
| `SKILL.md:829` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 829 | 1251 | in range |
| `SKILL.md:830-831` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 830-831 | 1251 | in range |
| `SKILL.md:832` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 832 | 1251 | in range |
| `SKILL.md:86` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 86 | 1251 | in range |
| `SKILL.md:910-913` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 910-913 | 1251 | in range |
| `SKILL.md:982` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 982 | 1251 | in range |
| `SKILL.md:999` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` | 999 | 1251 | in range |
| `considerthese/2026-10-24.md:49-52` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-24.md` | 49-52 | 70 | in range |
| `considerthese/2026-10-25.md:53-57` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-25.md` | 53-57 | 77 | in range |
| `considerthese/2026-10-25.md:76` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-25.md` | 76 | 77 | in range |
| `considerthese/2026-10-26.md:30` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-26.md` | 30 | 35 | in range |
| `considerthese/2026-10-26.md:31` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-26.md` | 31 | 35 | in range |
| `considerthese/2026-10-26.md:35` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-26.md` | 35 | 35 | in range |
| `corpus/QUALITY.md:169` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 169 | 632 | in range |
| `corpus/QUALITY.md:220-222` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 220-222 | 632 | in range |
| `corpus/QUALITY.md:226` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 226 | 632 | in range |
| `corpus/QUALITY.md:227` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 227 | 632 | in range |
| `corpus/QUALITY.md:229` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 229 | 632 | in range |
| `corpus/QUALITY.md:249` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 249 | 632 | in range |
| `corpus/QUALITY.md:263` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 263 | 632 | in range |
| `corpus/QUALITY.md:278` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 278 | 632 | in range |
| `corpus/QUALITY.md:292` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 292 | 632 | in range |
| `corpus/QUALITY.md:35-36` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 35-36 | 632 | in range |
| `corpus/QUALITY.md:391` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 391 | 632 | in range |
| `corpus/QUALITY.md:401` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 401 | 632 | in range |
| `corpus/QUALITY.md:407` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 407 | 632 | in range |
| `corpus/QUALITY.md:413-416` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 413-416 | 632 | in range |
| `corpus/QUALITY.md:550` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 550 | 632 | in range |
| `corpus/QUALITY.md:576-579` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 576-579 | 632 | in range |
| `corpus/QUALITY.md:581` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 581 | 632 | in range |
| `corpus/QUALITY.md:587` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 587 | 632 | in range |
| `corpus/QUALITY.md:587-588` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 587-588 | 632 | in range |
| `corpus/QUALITY.md:588` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 588 | 632 | in range |
| `corpus/QUALITY.md:594` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 594 | 632 | in range |
| `corpus/QUALITY.md:595` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 595 | 632 | in range |
| `corpus/QUALITY.md:77` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 77 | 632 | in range |
| `corpus/QUALITY.md:83` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 83 | 632 | in range |
| `corpus/QUALITY.md:89` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 89 | 632 | in range |
| `corpus/QUALITY.md:95` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` | 95 | 632 | in range |
| `corpus/README.md:0` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 0 | 1287 | in range |
| `corpus/README.md:1019` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 1019 | 1287 | in range |
| `corpus/README.md:1050` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 1050 | 1287 | in range |
| `corpus/README.md:1114` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 1114 | 1287 | in range |
| `corpus/README.md:1243` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 1243 | 1287 | in range |
| `corpus/README.md:1257` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 1257 | 1287 | in range |
| `corpus/README.md:145` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 145 | 1287 | in range |
| `corpus/README.md:168` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 168 | 1287 | in range |
| `corpus/README.md:200` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 200 | 1287 | in range |
| `corpus/README.md:207` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 207 | 1287 | in range |
| `corpus/README.md:208` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 208 | 1287 | in range |
| `corpus/README.md:210` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 210 | 1287 | in range |
| `corpus/README.md:211` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 211 | 1287 | in range |
| `corpus/README.md:309` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 309 | 1287 | in range |
| `corpus/README.md:361` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 361 | 1287 | in range |
| `corpus/README.md:448` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 448 | 1287 | in range |
| `corpus/README.md:49` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 49 | 1287 | in range |
| `corpus/README.md:54` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 54 | 1287 | in range |
| `corpus/README.md:591` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 591 | 1287 | in range |
| `corpus/README.md:702` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 702 | 1287 | in range |
| `corpus/README.md:82` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` | 82 | 1287 | in range |
| `corpus/SOURCES.md:100` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 100 | 355 | in range |
| `corpus/SOURCES.md:112` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 112 | 355 | in range |
| `corpus/SOURCES.md:112-113` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 112-113 | 355 | in range |
| `corpus/SOURCES.md:113` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 113 | 355 | in range |
| `corpus/SOURCES.md:114` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 114 | 355 | in range |
| `corpus/SOURCES.md:115` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 115 | 355 | in range |
| `corpus/SOURCES.md:117` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 117 | 355 | in range |
| `corpus/SOURCES.md:122` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 122 | 355 | in range |
| `corpus/SOURCES.md:124` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 124 | 355 | in range |
| `corpus/SOURCES.md:125` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 125 | 355 | in range |
| `corpus/SOURCES.md:126` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 126 | 355 | in range |
| `corpus/SOURCES.md:127` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 127 | 355 | in range |
| `corpus/SOURCES.md:128` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 128 | 355 | in range |
| `corpus/SOURCES.md:129` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 129 | 355 | in range |
| `corpus/SOURCES.md:133` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 133 | 355 | in range |
| `corpus/SOURCES.md:135` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 135 | 355 | in range |
| `corpus/SOURCES.md:137` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 137 | 355 | in range |
| `corpus/SOURCES.md:138` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 138 | 355 | in range |
| `corpus/SOURCES.md:139` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 139 | 355 | in range |
| `corpus/SOURCES.md:140` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 140 | 355 | in range |
| `corpus/SOURCES.md:141` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 141 | 355 | in range |
| `corpus/SOURCES.md:142` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 142 | 355 | in range |
| `corpus/SOURCES.md:143` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 143 | 355 | in range |
| `corpus/SOURCES.md:144` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 144 | 355 | in range |
| `corpus/SOURCES.md:145` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 145 | 355 | in range |
| `corpus/SOURCES.md:145-146` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 145-146 | 355 | in range |
| `corpus/SOURCES.md:146` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 146 | 355 | in range |
| `corpus/SOURCES.md:148` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 148 | 355 | in range |
| `corpus/SOURCES.md:148-149` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 148-149 | 355 | in range |
| `corpus/SOURCES.md:149` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 149 | 355 | in range |
| `corpus/SOURCES.md:150` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 150 | 355 | in range |
| `corpus/SOURCES.md:151` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 151 | 355 | in range |
| `corpus/SOURCES.md:152` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 152 | 355 | in range |
| `corpus/SOURCES.md:153` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 153 | 355 | in range |
| `corpus/SOURCES.md:157` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 157 | 355 | in range |
| `corpus/SOURCES.md:158` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 158 | 355 | in range |
| `corpus/SOURCES.md:164` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 164 | 355 | in range |
| `corpus/SOURCES.md:176` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 176 | 355 | in range |
| `corpus/SOURCES.md:22` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 22 | 355 | in range |
| `corpus/SOURCES.md:250` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 250 | 355 | in range |
| `corpus/SOURCES.md:284` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 284 | 355 | in range |
| `corpus/SOURCES.md:318-319` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 318-319 | 355 | in range |
| `corpus/SOURCES.md:40` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 40 | 355 | in range |
| `corpus/SOURCES.md:47` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 47 | 355 | in range |
| `corpus/SOURCES.md:48` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 48 | 355 | in range |
| `corpus/SOURCES.md:54` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 54 | 355 | in range |
| `corpus/SOURCES.md:55-56` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 55-56 | 355 | in range |
| `corpus/SOURCES.md:56` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 56 | 355 | in range |
| `corpus/SOURCES.md:57` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 57 | 355 | in range |
| `corpus/SOURCES.md:58` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 58 | 355 | in range |
| `corpus/SOURCES.md:61` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 61 | 355 | in range |
| `corpus/SOURCES.md:62` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 62 | 355 | in range |
| `corpus/SOURCES.md:62-65` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 62-65 | 355 | in range |
| `corpus/SOURCES.md:74` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 74 | 355 | in range |
| `corpus/SOURCES.md:79` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 79 | 355 | in range |
| `corpus/SOURCES.md:82` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 82 | 355 | in range |
| `corpus/SOURCES.md:83` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 83 | 355 | in range |
| `corpus/SOURCES.md:86` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 86 | 355 | in range |
| `corpus/SOURCES.md:90` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | 90 | 355 | in range |
| `corpus/instruments/README.md:1000` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/README.md` | 1000 | 1064 | in range |
| `corpus/instruments/README.md:131` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/README.md` | 131 | 1064 | in range |
| `corpus/instruments/README.md:16-17` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/README.md` | 16-17 | 1064 | in range |
| `corpus/instruments/README.md:175-184` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/README.md` | 175-184 | 1064 | in range |
| `corpus/instruments/README.md:31-38` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/README.md` | 31-38 | 1064 | in range |
| `corpus/instruments/README.md:354` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/README.md` | 354 | 1064 | in range |
| `corpus/instruments/README.md:63` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/README.md` | 63 | 1064 | in range |
| `corpus/instruments/capture-binding-check.py:1-92` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py` | 1-92 | 1129 | in range |
| `corpus/instruments/capture-binding-check.py:166-181` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py` | 166-181 | 1129 | in range |
| `corpus/instruments/capture-binding-check.py:184-262` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py` | 184-262 | 1129 | in range |
| `corpus/instruments/capture-binding-check.py:67-68` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py` | 67-68 | 1129 | in range |
| `corpus/instruments/capture-binding-check.py:80` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py` | 80 | 1129 | in range |
| `corpus/instruments/capture-secret-allow.tsv:21-22` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-allow.tsv` | 21-22 | 28 | in range |
| `corpus/instruments/capture-secret-scan.py:1-152` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 1-152 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:120-121` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 120-121 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:120-134` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 120-134 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:128` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 128 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:128-134` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 128-134 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:129-130` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 129-130 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:129-131` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 129-131 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:131-132` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 131-132 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:132` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 132 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:132-134` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 132-134 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:133-134` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 133-134 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:137-144` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 137-144 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:14-21` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 14-21 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:141-142` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 141-142 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:142` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 142 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:142-143` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 142-143 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:146-151` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 146-151 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:147` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 147 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:157-166` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 157-166 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:168` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 168 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:169` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 169 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:170` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 170 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:170-184` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 170-184 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:172` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 172 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:175` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 175 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:175-184` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 175-184 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:179-184` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 179-184 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:186` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 186 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:188` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 188 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:188-189` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 188-189 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:19-21` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 19-21 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:191` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 191 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:193-194` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 193-194 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:196` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 196 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:198` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 198 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:198-208` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 198-208 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:199` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 199 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:20-21` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 20-21 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:200` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 200 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:201` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 201 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:202` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 202 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:207-208` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 207-208 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:208-223` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 208-223 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:23-134` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 23-134 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:23-66` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 23-66 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:237` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 237 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:238` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 238 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:238-243` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 238-243 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:238-247` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 238-247 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:242-243` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 242-243 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:246-247` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 246-247 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:247-254` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 247-254 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:255` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 255 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:283-303` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 283-303 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:350-370` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 350-370 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:352` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 352 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:358` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 358 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:359` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 359 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:361` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 361 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:367` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 367 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:371-380` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 371-380 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:376` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 376 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:381-395` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 381-395 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:388` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 388 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:388-389` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 388-389 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:390-391` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 390-391 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:395` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 395 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:439-443` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 439-443 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:439-452` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 439-452 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:44-45` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 44-45 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:47-52` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 47-52 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:53-66` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 53-66 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:53-80` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 53-80 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:67-80` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 67-80 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:81-82` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 81-82 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:81-92` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 81-92 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:81-97` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 81-97 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:84-85` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 84-85 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:84-92` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 84-92 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:86-97` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 86-97 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:87-92` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 87-92 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:9-21` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 9-21 | 701 | in range |
| `corpus/instruments/capture-secret-scan.py:93-95` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py` | 93-95 | 701 | in range |
| `corpus/instruments/capture-source.py:109-112` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 109-112 | 198 | in range |
| `corpus/instruments/capture-source.py:115-123` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 115-123 | 198 | in range |
| `corpus/instruments/capture-source.py:120` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 120 | 198 | in range |
| `corpus/instruments/capture-source.py:122` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 122 | 198 | in range |
| `corpus/instruments/capture-source.py:123` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 123 | 198 | in range |
| `corpus/instruments/capture-source.py:126-146` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 126-146 | 198 | in range |
| `corpus/instruments/capture-source.py:134-135` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 134-135 | 198 | in range |
| `corpus/instruments/capture-source.py:135-142` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 135-142 | 198 | in range |
| `corpus/instruments/capture-source.py:136-139` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 136-139 | 198 | in range |
| `corpus/instruments/capture-source.py:169-173` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 169-173 | 198 | in range |
| `corpus/instruments/capture-source.py:20-26` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 20-26 | 198 | in range |
| `corpus/instruments/capture-source.py:23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 23 | 198 | in range |
| `corpus/instruments/capture-source.py:24-25` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 24-25 | 198 | in range |
| `corpus/instruments/capture-source.py:5-6` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 5-6 | 198 | in range |
| `corpus/instruments/capture-source.py:53` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` | 53 | 198 | in range |
| `corpus/instruments/claim-package-check.py:101-108` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 101-108 | 802 | in range |
| `corpus/instruments/claim-package-check.py:120` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 120 | 802 | in range |
| `corpus/instruments/claim-package-check.py:121` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 121 | 802 | in range |
| `corpus/instruments/claim-package-check.py:135-142` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/claim-package-check.py` | 135-142 | 802 | in range |
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
| `corpus/instruments/figure-audit.py:106-109` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py` | 106-109 | 968 | in range |
| `corpus/instruments/figure-audit.py:27` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py` | 27 | 968 | in range |
| `corpus/instruments/figure-audit.py:493` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py` | 493 | 968 | in range |
| `corpus/instruments/figure-audit.py:98-109` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py` | 98-109 | 968 | in range |
| `corpus/instruments/fixtures/claim-package/defect-8-marker/expected-rule:1` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/fixtures/claim-package/defect-8-marker/expected-rule` | 1 | 1 | in range |
| `corpus/instruments/fixtures/claim-package/defect-9-secret/expected-rule:1` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/fixtures/claim-package/defect-9-secret/expected-rule` | 1 | 1 | in range |
| `corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json:2` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json` | 2 | 85 | in range |
| `corpus/instruments/fixtures/claim-package/exemplar/provenance.json:88` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/fixtures/claim-package/exemplar/provenance.json` | 88 | 95 | in range |
| `corpus/instruments/fixtures/claim-package/exemplar/report.md:88` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/fixtures/claim-package/exemplar/report.md` | 88 | 88 | in range |
| `corpus/instruments/frontier-recheck-count.py:260-261` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/frontier-recheck-count.py` | 260-261 | 566 | in range |
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
| `corpus/instruments/resolve.py:281` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py` | 281 | 623 | in range |
| `corpus/instruments/resolve.py:31-48` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py` | 31-48 | 623 | in range |
| `corpus/instruments/resolve.py:74` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py` | 74 | 623 | in range |
| `corpus/instruments/score-gap.py:76` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/score-gap.py` | 76 | 554 | in range |
| `corpus/instruments/source-recheck.py:275` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py` | 275 | 415 | in range |
| `corpus/instruments/source-recheck.py:33` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py` | 33 | 415 | in range |
| `corpus/knowledge/authorization-safe-harbor-and-scope.md:8` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/authorization-safe-harbor-and-scope.md` | 8 | 46 | in range |
| `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md:97` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` | 97 | 306 | in range |
| `corpus/knowledge/claim-gates.md:10-11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 10-11 | 160 | in range |
| `corpus/knowledge/claim-gates.md:15` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 15 | 160 | in range |
| `corpus/knowledge/claim-gates.md:16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 16 | 160 | in range |
| `corpus/knowledge/claim-gates.md:20` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 20 | 160 | in range |
| `corpus/knowledge/claim-gates.md:21-23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 21-23 | 160 | in range |
| `corpus/knowledge/claim-gates.md:22-23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 22-23 | 160 | in range |
| `corpus/knowledge/claim-gates.md:23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 23 | 160 | in range |
| `corpus/knowledge/claim-gates.md:24` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 24 | 160 | in range |
| `corpus/knowledge/claim-gates.md:25-27` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 25-27 | 160 | in range |
| `corpus/knowledge/claim-gates.md:26` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 26 | 160 | in range |
| `corpus/knowledge/claim-gates.md:27` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 27 | 160 | in range |
| `corpus/knowledge/claim-gates.md:3` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 3 | 160 | in range |
| `corpus/knowledge/claim-gates.md:31` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 31 | 160 | in range |
| `corpus/knowledge/claim-gates.md:32-33` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 32-33 | 160 | in range |
| `corpus/knowledge/claim-gates.md:33-34` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 33-34 | 160 | in range |
| `corpus/knowledge/claim-gates.md:35` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 35 | 160 | in range |
| `corpus/knowledge/claim-gates.md:35-36` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 35-36 | 160 | in range |
| `corpus/knowledge/claim-gates.md:36-37` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 36-37 | 160 | in range |
| `corpus/knowledge/claim-gates.md:4-5` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 4-5 | 160 | in range |
| `corpus/knowledge/claim-gates.md:41` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 41 | 160 | in range |
| `corpus/knowledge/claim-gates.md:45-47` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 45-47 | 160 | in range |
| `corpus/knowledge/claim-gates.md:45-48` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 45-48 | 160 | in range |
| `corpus/knowledge/claim-gates.md:52-56` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 52-56 | 160 | in range |
| `corpus/knowledge/claim-gates.md:57-61` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 57-61 | 160 | in range |
| `corpus/knowledge/claim-gates.md:67` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 67 | 160 | in range |
| `corpus/knowledge/claim-gates.md:68` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 68 | 160 | in range |
| `corpus/knowledge/claim-gates.md:69` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 69 | 160 | in range |
| `corpus/knowledge/claim-gates.md:70-71` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 70-71 | 160 | in range |
| `corpus/knowledge/claim-gates.md:71` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 71 | 160 | in range |
| `corpus/knowledge/claim-gates.md:72-73` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 72-73 | 160 | in range |
| `corpus/knowledge/claim-gates.md:74` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 74 | 160 | in range |
| `corpus/knowledge/claim-gates.md:75-76` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 75-76 | 160 | in range |
| `corpus/knowledge/claim-gates.md:77` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 77 | 160 | in range |
| `corpus/knowledge/claim-gates.md:78-80` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 78-80 | 160 | in range |
| `corpus/knowledge/claim-gates.md:81-85` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 81-85 | 160 | in range |
| `corpus/knowledge/claim-gates.md:82-85` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 82-85 | 160 | in range |
| `corpus/knowledge/claim-gates.md:86-87` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 86-87 | 160 | in range |
| `corpus/knowledge/claim-gates.md:88-91` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-gates.md` | 88-91 | 160 | in range |
| `corpus/knowledge/claim-package-contract.md:11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 11 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:11-16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 11-16 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:13` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 13 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:14` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 14 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:15` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 15 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 16 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:18-26` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 18-26 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:22-23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 22-23 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:24-26` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 24-26 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:31` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 31 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:31-34` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 31-34 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:52-53` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 52-53 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:54` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 54 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:7` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 7 | 99 | in range |
| `corpus/knowledge/claim-package-contract.md:9-16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/claim-package-contract.md` | 9-16 | 99 | in range |
| `corpus/knowledge/cna-assignment-and-vulnerability-rules.md:36` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/cna-assignment-and-vulnerability-rules.md` | 36 | 80 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:119-131` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/considerthese-proposals-ledger.md` | 119-131 | 172 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:13` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/considerthese-proposals-ledger.md` | 13 | 172 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:22-33` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/considerthese-proposals-ledger.md` | 22-33 | 172 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:3` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/considerthese-proposals-ledger.md` | 3 | 172 | in range |
| `corpus/knowledge/considerthese-proposals-ledger.md:37` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/considerthese-proposals-ledger.md` | 37 | 172 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:22` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/coordinated-disclosure-timelines.md` | 22 | 44 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:24` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/coordinated-disclosure-timelines.md` | 24 | 44 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:24-25` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/coordinated-disclosure-timelines.md` | 24-25 | 44 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:6-17` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/coordinated-disclosure-timelines.md` | 6-17 | 44 | in range |
| `corpus/knowledge/coordinated-disclosure-timelines.md:7-17` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/coordinated-disclosure-timelines.md` | 7-17 | 44 | in range |
| `corpus/knowledge/cvss-v4-severity-and-vector.md:2` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/cvss-v4-severity-and-vector.md` | 2 | 48 | in range |
| `corpus/knowledge/cvss-v4-severity-and-vector.md:34` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/cvss-v4-severity-and-vector.md` | 34 | 48 | in range |
| `corpus/knowledge/ev-model.md:13-25` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ev-model.md` | 13-25 | 60 | in range |
| `corpus/knowledge/ev-model.md:14` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ev-model.md` | 14 | 60 | in range |
| `corpus/knowledge/ev-model.md:15` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ev-model.md` | 15 | 60 | in range |
| `corpus/knowledge/ev-model.md:16-17` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ev-model.md` | 16-17 | 60 | in range |
| `corpus/knowledge/ev-model.md:18` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ev-model.md` | 18 | 60 | in range |
| `corpus/knowledge/ev-model.md:22-23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ev-model.md` | 22-23 | 60 | in range |
| `corpus/knowledge/ev-model.md:37-38` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ev-model.md` | 37-38 | 60 | in range |
| `corpus/knowledge/evidence-dir.md:78` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/evidence-dir.md` | 78 | 91 | in range |
| `corpus/knowledge/first-psirt-maturity-document.md:11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/first-psirt-maturity-document.md` | 11 | 69 | in range |
| `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md:79` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md` | 79 | 100 | in range |
| `corpus/knowledge/github-advisory-database-curation-semantics.md:75` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/github-advisory-database-curation-semantics.md` | 75 | 123 | in range |
| `corpus/knowledge/github-private-vulnerability-reporting.md:40` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/github-private-vulnerability-reporting.md` | 40 | 49 | in range |
| `corpus/knowledge/github-repository-security-advisories-rest-api.md:45-46` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/github-repository-security-advisories-rest-api.md` | 45-46 | 96 | in range |
| `corpus/knowledge/github-repository-security-advisories.md:11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/github-repository-security-advisories.md` | 11 | 145 | in range |
| `corpus/knowledge/gitlab-routable-and-versioned-token-forms.md:87-88` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/gitlab-routable-and-versioned-token-forms.md` | 87-88 | 99 | in range |
| `corpus/knowledge/intake-and-finalize.md:78-92` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/intake-and-finalize.md` | 78-92 | 111 | in range |
| `corpus/knowledge/intake-surface.md:80-85` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/intake-surface.md` | 80-85 | 179 | in range |
| `corpus/knowledge/intake-surface.md:83-85` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/intake-surface.md` | 83-85 | 179 | in range |
| `corpus/knowledge/intake-surface.md:83-88` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/intake-surface.md` | 83-88 | 179 | in range |
| `corpus/knowledge/intake-surface.md:89-93` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/intake-surface.md` | 89-93 | 179 | in range |
| `corpus/knowledge/mission-control.md:13-46` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 13-46 | 171 | in range |
| `corpus/knowledge/mission-control.md:17` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 17 | 171 | in range |
| `corpus/knowledge/mission-control.md:19` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 19 | 171 | in range |
| `corpus/knowledge/mission-control.md:19-20` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 19-20 | 171 | in range |
| `corpus/knowledge/mission-control.md:19-21` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 19-21 | 171 | in range |
| `corpus/knowledge/mission-control.md:20-21` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 20-21 | 171 | in range |
| `corpus/knowledge/mission-control.md:20-24` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 20-24 | 171 | in range |
| `corpus/knowledge/mission-control.md:21` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 21 | 171 | in range |
| `corpus/knowledge/mission-control.md:21-27` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 21-27 | 171 | in range |
| `corpus/knowledge/mission-control.md:29` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 29 | 171 | in range |
| `corpus/knowledge/mission-control.md:3` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 3 | 171 | in range |
| `corpus/knowledge/mission-control.md:36` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 36 | 171 | in range |
| `corpus/knowledge/mission-control.md:40` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 40 | 171 | in range |
| `corpus/knowledge/mission-control.md:54-55` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 54-55 | 171 | in range |
| `corpus/knowledge/mission-control.md:54-56` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 54-56 | 171 | in range |
| `corpus/knowledge/mission-control.md:55-57` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 55-57 | 171 | in range |
| `corpus/knowledge/mission-control.md:56-57` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 56-57 | 171 | in range |
| `corpus/knowledge/mission-control.md:59-60` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 59-60 | 171 | in range |
| `corpus/knowledge/mission-control.md:61` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 61 | 171 | in range |
| `corpus/knowledge/mission-control.md:61-64` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 61-64 | 171 | in range |
| `corpus/knowledge/mission-control.md:64-66` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 64-66 | 171 | in range |
| `corpus/knowledge/mission-control.md:66` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 66 | 171 | in range |
| `corpus/knowledge/mission-control.md:68-71` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/mission-control.md` | 68-71 | 171 | in range |
| `corpus/knowledge/openssf-scorecard-checks.md:31` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/openssf-scorecard-checks.md` | 31 | 97 | in range |
| `corpus/knowledge/ops-invariants.md:17-25` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 17-25 | 141 | in range |
| `corpus/knowledge/ops-invariants.md:18` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 18 | 141 | in range |
| `corpus/knowledge/ops-invariants.md:19` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 19 | 141 | in range |
| `corpus/knowledge/ops-invariants.md:20` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 20 | 141 | in range |
| `corpus/knowledge/ops-invariants.md:21` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 21 | 141 | in range |
| `corpus/knowledge/ops-invariants.md:22` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 22 | 141 | in range |
| `corpus/knowledge/ops-invariants.md:23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 23 | 141 | in range |
| `corpus/knowledge/ops-invariants.md:24` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 24 | 141 | in range |
| `corpus/knowledge/ops-invariants.md:25` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 25 | 141 | in range |
| `corpus/knowledge/ops-invariants.md:34-40` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 34-40 | 141 | in range |
| `corpus/knowledge/ops-invariants.md:41-42` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ops-invariants.md` | 41-42 | 141 | in range |
| `corpus/knowledge/osv-affected-range-events.md:21` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-affected-range-events.md` | 21 | 121 | in range |
| `corpus/knowledge/osv-affected-range-events.md:23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-affected-range-events.md` | 23 | 121 | in range |
| `corpus/knowledge/osv-affected-range-events.md:30` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-affected-range-events.md` | 30 | 121 | in range |
| `corpus/knowledge/osv-affected-range-events.md:33` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-affected-range-events.md` | 33 | 121 | in range |
| `corpus/knowledge/osv-affected-range-events.md:56-63` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-affected-range-events.md` | 56-63 | 121 | in range |
| `corpus/knowledge/osv-affected-range-events.md:78` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-affected-range-events.md` | 78 | 121 | in range |
| `corpus/knowledge/osv-determineversion-cc-library-versioning.md:80` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-determineversion-cc-library-versioning.md` | 80 | 125 | in range |
| `corpus/knowledge/osv-faq-post-import-record-lifecycle.md:69` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-faq-post-import-record-lifecycle.md` | 69 | 99 | in range |
| `corpus/knowledge/osv-high-quality-record-import-bar.md:69` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-high-quality-record-import-bar.md` | 69 | 97 | in range |
| `corpus/knowledge/osv-importfindings-record-quality-feedback.md:23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-importfindings-record-quality-feedback.md` | 23 | 98 | in range |
| `corpus/knowledge/osv-post-batch-query-contract.md:11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-batch-query-contract.md` | 11 | 92 | in range |
| `corpus/knowledge/osv-post-batch-query-contract.md:19` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-batch-query-contract.md` | 19 | 92 | in range |
| `corpus/knowledge/osv-post-batch-query-contract.md:21` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-batch-query-contract.md` | 21 | 92 | in range |
| `corpus/knowledge/osv-post-batch-query-contract.md:27` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-batch-query-contract.md` | 27 | 92 | in range |
| `corpus/knowledge/osv-post-batch-query-contract.md:35` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-batch-query-contract.md` | 35 | 92 | in range |
| `corpus/knowledge/osv-post-batch-query-contract.md:37` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-batch-query-contract.md` | 37 | 92 | in range |
| `corpus/knowledge/osv-post-batch-query-contract.md:43` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-batch-query-contract.md` | 43 | 92 | in range |
| `corpus/knowledge/osv-post-batch-query-contract.md:61` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-batch-query-contract.md` | 61 | 92 | in range |
| `corpus/knowledge/osv-post-batch-query-contract.md:67` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-batch-query-contract.md` | 67 | 92 | in range |
| `corpus/knowledge/osv-post-v1-query-contract.md:11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-v1-query-contract.md` | 11 | 80 | in range |
| `corpus/knowledge/osv-post-v1-query-contract.md:19` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-v1-query-contract.md` | 19 | 80 | in range |
| `corpus/knowledge/osv-post-v1-query-contract.md:21` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-v1-query-contract.md` | 21 | 80 | in range |
| `corpus/knowledge/osv-post-v1-query-contract.md:29` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-v1-query-contract.md` | 29 | 80 | in range |
| `corpus/knowledge/osv-post-v1-query-contract.md:31` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-v1-query-contract.md` | 31 | 80 | in range |
| `corpus/knowledge/osv-post-v1-query-contract.md:37` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-v1-query-contract.md` | 37 | 80 | in range |
| `corpus/knowledge/osv-post-v1-query-contract.md:45` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-v1-query-contract.md` | 45 | 80 | in range |
| `corpus/knowledge/osv-post-v1-query-contract.md:47` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-v1-query-contract.md` | 47 | 80 | in range |
| `corpus/knowledge/osv-post-v1-query-contract.md:53` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-v1-query-contract.md` | 53 | 80 | in range |
| `corpus/knowledge/osv-post-v1-query-contract.md:75` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/osv-post-v1-query-contract.md` | 75 | 80 | in range |
| `corpus/knowledge/policy-access-playbook.md:13` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/policy-access-playbook.md` | 13 | 35 | in range |
| `corpus/knowledge/program-quirks.md:10` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/program-quirks.md` | 10 | 67 | in range |
| `corpus/knowledge/program-severity-ladders-and-reward-scales.md:16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/program-severity-ladders-and-reward-scales.md` | 16 | 67 | in range |
| `corpus/knowledge/project-zero-big-sleep-sqlite-variant-analysis.md:26` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/project-zero-big-sleep-sqlite-variant-analysis.md` | 26 | 34 | in range |
| `corpus/knowledge/retirement-autopsies.md:38` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/retirement-autopsies.md` | 38 | 141 | in range |
| `corpus/knowledge/root-loss-2026-10-12.md:68` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/root-loss-2026-10-12.md` | 68 | 76 | in range |
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
| `corpus/knowledge/ufo-archive-2026.md:31` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ufo-archive-2026.md` | 31 | 210 | in range |
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
| `corpus/lessons/round-35.md:20` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-35.md` | 20 | 529 | in range |
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
| `corpus/lessons/round-38.md:286` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-38.md` | 286 | 311 | in range |
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
| `corpus/lessons/round-47-verifier-spotcheck.md:94` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-47-verifier-spotcheck.md` | 94 | 96 | in range |
| `corpus/lessons/round-5.md:16` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-5.md` | 16 | 38 | in range |
| `corpus/lessons/round-57.md:5` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-57.md` | 5 | 85 | in range |
| `corpus/lessons/round-59.md:66` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-59.md` | 66 | 103 | in range |
| `corpus/lessons/round-60.md:55` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-60.md` | 55 | 106 | in range |
| `corpus/lessons/round-65-verifier-spotcheck.md:132-155` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-65-verifier-spotcheck.md` | 132-155 | 157 | in range |
| `corpus/lessons/round-66.md:24-33` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-66.md` | 24-33 | 69 | in range |
| `corpus/lessons/round-71-verifier-spotcheck.md:38-39` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-71-verifier-spotcheck.md` | 38-39 | 153 | in range |
| `corpus/lessons/round-79-verifier-spotcheck.md:28` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-79-verifier-spotcheck.md` | 28 | 107 | in range |
| `corpus/lessons/round-79.md:37` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-79.md` | 37 | 91 | in range |
| `corpus/lessons/round-79.md:53` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-79.md` | 53 | 91 | in range |
| `corpus/lessons/round-8.md:10` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-8.md` | 10 | 53 | in range |
| `corpus/lessons/round-80-verifier-spotcheck.md:101` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-80-verifier-spotcheck.md` | 101 | 105 | in range |
| `corpus/lessons/round-80-verifier-spotcheck.md:102` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-80-verifier-spotcheck.md` | 102 | 105 | in range |
| `corpus/lessons/round-80.md:169` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-80.md` | 169 | 177 | in range |
| `corpus/lessons/round-81-verifier-spotcheck.md:107` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-81-verifier-spotcheck.md` | 107 | 110 | in range |
| `corpus/lessons/round-81-verifier-spotcheck.md:108` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-81-verifier-spotcheck.md` | 108 | 110 | in range |
| `corpus/lessons/round-81.md:102-107` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-81.md` | 102-107 | 364 | in range |
| `corpus/lessons/round-81.md:255` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-81.md` | 255 | 364 | in range |
| `corpus/lessons/round-81.md:28` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-81.md` | 28 | 364 | in range |
| `corpus/lessons/round-82-verifier-spotcheck.md:104` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-82-verifier-spotcheck.md` | 104 | 112 | in range |
| `corpus/lessons/round-82.md:11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-82.md` | 11 | 382 | in range |
| `corpus/lessons/round-82.md:181` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-82.md` | 181 | 382 | in range |
| `corpus/lessons/round-82.md:198-205` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-82.md` | 198-205 | 382 | in range |
| `corpus/lessons/round-86-verifier-spotcheck.md:124-127` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-86-verifier-spotcheck.md` | 124-127 | 148 | in range |
| `corpus/lessons/round-86.md:61` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-86.md` | 61 | 85 | in range |
| `corpus/lessons/round-86.md:62` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-86.md` | 62 | 85 | in range |
| `corpus/lessons/round-86.md:63` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-86.md` | 63 | 85 | in range |
| `corpus/lessons/round-9.md:33` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-9.md` | 33 | 63 | in range |
| `corpus/lessons/round-96.md:21` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-96.md` | 21 | 86 | in range |
| `corpus/source-snapshots/round-23/S029.txt:14` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-23/S029.txt` | 14 | 146 | in range |
| `corpus/source-snapshots/round-23/S029.txt:20` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-23/S029.txt` | 20 | 146 | in range |
| `corpus/source-snapshots/round-24/S013.txt:65` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-24/S013.txt` | 65 | 183 | in range |
| `corpus/source-snapshots/round-30/S041.txt:1680-1681` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-30/S041.txt` | 1680-1681 | 2354 | in range |
| `corpus/source-snapshots/round-30/S041.txt:1792-1867` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-30/S041.txt` | 1792-1867 | 2354 | in range |
| `corpus/source-snapshots/round-30/S041.txt:1868` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-30/S041.txt` | 1868 | 2354 | in range |
| `corpus/source-snapshots/round-30/S041.txt:1868-1870` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-30/S041.txt` | 1868-1870 | 2354 | in range |
| `corpus/source-snapshots/round-30/S041.txt:1996-2079` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-30/S041.txt` | 1996-2079 | 2354 | in range |
| `corpus/source-snapshots/round-31/S048.txt:35` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-31/S048.txt` | 35 | 97 | in range |
| `corpus/source-snapshots/round-32/S050.txt:70` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-32/S050.txt` | 70 | 630 | in range |
| `corpus/source-snapshots/round-40/S017.txt:28` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-40/S017.txt` | 28 | 39 | in range |
| `corpus/source-snapshots/round-43/S067.txt:69` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-43/S067.txt` | 69 | 109 | in range |
| `corpus/source-snapshots/round-43/S067.txt:83` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-43/S067.txt` | 83 | 109 | in range |
| `corpus/source-snapshots/round-43/S067.txt:88` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-43/S067.txt` | 88 | 109 | in range |
| `corpus/source-snapshots/round-44/S069.txt:10-11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-44/S069.txt` | 10-11 | 1132 | in range |
| `corpus/source-snapshots/round-44/S069.txt:61` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-44/S069.txt` | 61 | 1132 | in range |
| `corpus/source-snapshots/round-44/S069.txt:61-62` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-44/S069.txt` | 61-62 | 1132 | in range |
| `corpus/source-snapshots/round-44/S069.txt:61-69` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-44/S069.txt` | 61-69 | 1132 | in range |
| `corpus/source-snapshots/round-44/S069.txt:62-63` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-44/S069.txt` | 62-63 | 1132 | in range |
| `corpus/source-snapshots/round-44/S069.txt:65-72` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-44/S069.txt` | 65-72 | 1132 | in range |
| `corpus/source-snapshots/round-44/S069.txt:68-69` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-44/S069.txt` | 68-69 | 1132 | in range |
| `corpus/source-snapshots/round-44/S069.txt:70-72` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-44/S069.txt` | 70-72 | 1132 | in range |
| `corpus/source-snapshots/round-44/S069.txt:76-77` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-44/S069.txt` | 76-77 | 1132 | in range |
| `corpus/source-snapshots/round-44/S069.txt:78-86` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-44/S069.txt` | 78-86 | 1132 | in range |
| `corpus/source-snapshots/round-44/S069.txt:78-87` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-44/S069.txt` | 78-87 | 1132 | in range |
| `corpus/source-snapshots/round-45/S071.txt:117` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 117 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:17-18` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 17-18 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:20-21` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 20-21 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:20-47` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 20-47 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:201` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 201 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:208-209` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 208-209 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:21-22` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 21-22 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:210-211` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 210-211 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:213-219` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 213-219 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:22-23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 22-23 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:23-24` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 23-24 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:232-237` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 232-237 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:239-250` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 239-250 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:257` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 257 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:271-272` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 271-272 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:272-273` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 272-273 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:275-276` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 275-276 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:305` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 305 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:305-306` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 305-306 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:309-310` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 309-310 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:310-311` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 310-311 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:312` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 312 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:313-315` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 313-315 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:329-357` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 329-357 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:332` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 332 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:333-334` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 333-334 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:359-366` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 359-366 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:37-39` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 37-39 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:371-372` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 371-372 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:39-40` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 39-40 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:41-43` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 41-43 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:49-58` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 49-58 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:84-87` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 84-87 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:92-93` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 92-93 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:95-96` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 95-96 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:96` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 96 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:96-98` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 96-98 | 372 | in range |
| `corpus/source-snapshots/round-45/S071.txt:99` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt` | 99 | 372 | in range |
| `corpus/source-snapshots/round-46/S073.txt:560` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt` | 560 | 589 | in range |
| `corpus/source-snapshots/round-46/S073.txt:561` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt` | 561 | 589 | in range |
| `corpus/source-snapshots/round-46/S073.txt:563` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt` | 563 | 589 | in range |
| `corpus/source-snapshots/round-46/S073.txt:564` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt` | 564 | 589 | in range |
| `corpus/source-snapshots/round-46/S073.txt:566` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt` | 566 | 589 | in range |
| `corpus/source-snapshots/round-46/S073.txt:567` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt` | 567 | 589 | in range |
| `corpus/source-snapshots/round-46/S073.txt:568` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt` | 568 | 589 | in range |
| `corpus/source-snapshots/round-46/S073.txt:569` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt` | 569 | 589 | in range |
| `corpus/source-snapshots/round-46/S073.txt:573` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt` | 573 | 589 | in range |
| `corpus/source-snapshots/round-46/S073.txt:574` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt` | 574 | 589 | in range |
| `corpus/source-snapshots/round-46/S073.txt:575` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt` | 575 | 589 | in range |
| `corpus/source-snapshots/round-46/S073.txt:577` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt` | 577 | 589 | in range |
| `corpus/source-snapshots/round-46/S073.txt:578` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt` | 578 | 589 | in range |
| `corpus/source-snapshots/round-46/S073.txt:579` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt` | 579 | 589 | in range |
| `corpus/source-snapshots/round-47/S075.txt:20-27` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S075.txt` | 20-27 | 60 | in range |
| `corpus/source-snapshots/round-47/S075.txt:22` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S075.txt` | 22 | 60 | in range |
| `corpus/source-snapshots/round-47/S075.txt:23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S075.txt` | 23 | 60 | in range |
| `corpus/source-snapshots/round-47/S075.txt:23-25` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S075.txt` | 23-25 | 60 | in range |
| `corpus/source-snapshots/round-47/S075.txt:24` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S075.txt` | 24 | 60 | in range |
| `corpus/source-snapshots/round-47/S075.txt:25` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S075.txt` | 25 | 60 | in range |
| `corpus/source-snapshots/round-47/S075.txt:26` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S075.txt` | 26 | 60 | in range |
| `corpus/source-snapshots/round-47/S075.txt:27` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S075.txt` | 27 | 60 | in range |
| `corpus/source-snapshots/round-47/S076.txt:558` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 558 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:559` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 559 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:561` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 561 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:568` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 568 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:570` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 570 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:571` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 571 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:572` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 572 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:573` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 573 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:574` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 574 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:575` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 575 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:577` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 577 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:578` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 578 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:581` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 581 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:582` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 582 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:583` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 583 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:584` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 584 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:589` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 589 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:590` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 590 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:591` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 591 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:592` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 592 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:594` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 594 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:596` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 596 | 610 | in range |
| `corpus/source-snapshots/round-47/S076.txt:598` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/S076.txt` | 598 | 610 | in range |
| `corpus/source-snapshots/round-49/S078.txt:125` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-49/S078.txt` | 125 | 8375 | in range |
| `corpus/source-snapshots/round-49/S078.txt:1368` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-49/S078.txt` | 1368 | 8375 | in range |
| `corpus/source-snapshots/round-49/S078.txt:1480` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-49/S078.txt` | 1480 | 8375 | in range |
| `corpus/source-snapshots/round-49/S078.txt:1594` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-49/S078.txt` | 1594 | 8375 | in range |
| `corpus/source-snapshots/round-49/S078.txt:1798` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-49/S078.txt` | 1798 | 8375 | in range |
| `corpus/source-snapshots/round-49/S078.txt:5285` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-49/S078.txt` | 5285 | 8375 | in range |
| `corpus/source-snapshots/round-49/S078.txt:6` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-49/S078.txt` | 6 | 8375 | in range |
| `corpus/source-snapshots/round-49/S078.txt:6354` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-49/S078.txt` | 6354 | 8375 | in range |
| `corpus/source-snapshots/round-50/S080.txt:760-766` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-50/S080.txt` | 760-766 | 1462 | in range |
| `corpus/source-snapshots/round-51/S081.txt:2` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-51/S081.txt` | 2 | 120 | in range |
| `corpus/source-snapshots/round-57/S089.txt:1` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S089.txt` | 1 | 268 | in range |
| `corpus/source-snapshots/round-57/S089.txt:103` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S089.txt` | 103 | 268 | in range |
| `corpus/source-snapshots/round-57/S089.txt:105` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S089.txt` | 105 | 268 | in range |
| `corpus/source-snapshots/round-57/S089.txt:107` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S089.txt` | 107 | 268 | in range |
| `corpus/source-snapshots/round-57/S089.txt:52` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S089.txt` | 52 | 268 | in range |
| `corpus/source-snapshots/round-57/S089.txt:53` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S089.txt` | 53 | 268 | in range |
| `corpus/source-snapshots/round-57/S089.txt:54` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S089.txt` | 54 | 268 | in range |
| `corpus/source-snapshots/round-57/S089.txt:59` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S089.txt` | 59 | 268 | in range |
| `corpus/source-snapshots/round-57/S089.txt:97` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S089.txt` | 97 | 268 | in range |
| `corpus/source-snapshots/round-57/S090.txt:1` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S090.txt` | 1 | 261 | in range |
| `corpus/source-snapshots/round-57/S090.txt:100` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S090.txt` | 100 | 261 | in range |
| `corpus/source-snapshots/round-57/S090.txt:52` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S090.txt` | 52 | 261 | in range |
| `corpus/source-snapshots/round-57/S090.txt:53` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S090.txt` | 53 | 261 | in range |
| `corpus/source-snapshots/round-57/S090.txt:54` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S090.txt` | 54 | 261 | in range |
| `corpus/source-snapshots/round-57/S090.txt:59` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S090.txt` | 59 | 261 | in range |
| `corpus/source-snapshots/round-57/S090.txt:90` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S090.txt` | 90 | 261 | in range |
| `corpus/source-snapshots/round-57/S090.txt:96` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S090.txt` | 96 | 261 | in range |
| `corpus/source-snapshots/round-57/S090.txt:98` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S090.txt` | 98 | 261 | in range |
| `corpus/source-snapshots/round-67/S100.txt:462` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-67/S100.txt` | 462 | 478 | in range |
| `corpus/source-snapshots/round-68/S102.txt:101` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 101 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:107` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 107 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:11` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 11 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:13` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 13 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:139` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 139 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:14` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 14 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:142` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 142 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:146` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 146 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:15` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 15 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:153` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 153 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:160` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 160 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:168` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 168 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:17` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 17 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:181-183` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 181-183 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:19` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 19 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:209` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 209 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:234` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 234 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:236` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 236 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:24` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 24 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:240` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 240 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:241` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 241 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:244` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 244 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:25` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 25 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:268` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 268 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:271-272` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 271-272 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:275-276` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 275-276 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:28` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 28 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:281` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 281 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:285` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 285 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:290` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 290 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:292` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 292 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:297` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 297 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:30` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 30 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:300-301` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 300-301 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:304-305` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 304-305 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:305` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 305 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:306` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 306 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:309-310` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 309-310 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:31-32` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 31-32 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:313-314` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 313-314 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:316-317` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 316-317 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:320-321` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 320-321 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:327-330` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 327-330 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:336` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 336 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:339-340` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 339-340 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:343-345` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 343-345 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:347-350` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 347-350 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:352-355` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 352-355 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:353` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 353 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:354` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 354 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:358-361` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 358-361 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:365-366` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 365-366 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:37` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 37 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:371` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 371 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:375` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 375 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:380` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 380 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:387` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 387 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:390-391` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 390-391 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:394-395` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 394-395 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:398-399` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 398-399 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:402-403` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 402-403 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:408` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 408 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:412` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 412 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:53` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 53 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:69` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 69 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:9` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 9 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:93` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 93 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:94` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 94 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:97` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 97 | 429 | in range |
| `corpus/source-snapshots/round-68/S102.txt:99` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/S102.txt` | 99 | 429 | in range |
| `corpus/source-snapshots/round-69/S103.txt:13` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 13 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:273` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 273 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:274` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 274 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:275` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 275 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:276` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 276 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:282` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 282 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:283` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 283 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:289-290` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 289-290 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:291-294` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 291-294 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:293` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 293 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:294` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 294 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:295-296` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 295-296 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:297-299` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 297-299 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:299` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 299 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:300-302` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 300-302 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:303-305` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 303-305 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:306-307` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 306-307 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:308-311` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 308-311 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:312-320` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 312-320 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:321-326` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 321-326 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:323` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 323 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:327-330` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 327-330 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:331-334` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 331-334 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:335-337` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 335-337 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:338-341` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 338-341 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:341` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 341 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:345-346` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 345-346 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:349` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 349 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:356` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 356 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:357` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 357 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:358-456` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 358-456 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:360` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 360 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:365-430` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 365-430 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:457` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 457 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:458` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 458 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:465` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 465 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:471` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 471 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:475-476` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 475-476 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:486` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 486 | 585 | in range |
| `corpus/source-snapshots/round-69/S103.txt:487` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-69/S103.txt` | 487 | 585 | in range |
| `corpus/source-snapshots/round-70/S105.txt:567` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 567 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:569` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 569 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:570` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 570 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:571` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 571 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:572` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 572 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:573` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 573 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:573-582` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 573-582 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:574-581` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 574-581 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:582` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 582 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:584` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 584 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:584-585` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 584-585 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:585` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 585 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:586-597` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 586-597 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:589` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 589 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:597` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 597 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:598` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 598 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:599` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 599 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:600` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 600 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:601` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 601 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:602` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 602 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:603` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 603 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:604` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 604 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:605` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 605 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:606` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 606 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:607` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 607 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:611-616` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 611-616 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:621` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 621 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:622` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 622 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:623` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 623 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:623-627` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 623-627 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:628` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 628 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:639` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 639 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:639-640` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 639-640 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:640` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 640 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:642` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 642 | 656 | in range |
| `corpus/source-snapshots/round-70/S105.txt:643` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-70/S105.txt` | 643 | 656 | in range |
| `corpus/source-snapshots/round-71/S106.txt:28` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-71/S106.txt` | 28 | 148 | in range |
| `corpus/source-snapshots/round-71/S106.txt:31` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-71/S106.txt` | 31 | 148 | in range |
| `corpus/source-snapshots/round-71/S106.txt:47` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-71/S106.txt` | 47 | 148 | in range |
| `corpus/source-snapshots/round-71/S106.txt:49` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-71/S106.txt` | 49 | 148 | in range |
| `corpus/source-snapshots/round-71/S106.txt:51` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-71/S106.txt` | 51 | 148 | in range |
| `corpus/source-snapshots/round-71/S106.txt:52` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-71/S106.txt` | 52 | 148 | in range |
| `corpus/source-snapshots/round-71/S106.txt:60` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-71/S106.txt` | 60 | 148 | in range |
| `corpus/source-snapshots/round-71/S106.txt:61` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-71/S106.txt` | 61 | 148 | in range |
| `corpus/source-snapshots/round-71/S106.txt:62` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-71/S106.txt` | 62 | 148 | in range |
| `corpus/source-snapshots/round-71/S106.txt:69` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-71/S106.txt` | 69 | 148 | in range |
| `corpus/source-snapshots/round-71/S106.txt:70` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-71/S106.txt` | 70 | 148 | in range |
| `corpus/source-snapshots/round-71/S106.txt:72` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-71/S106.txt` | 72 | 148 | in range |
| `corpus/source-snapshots/round-73/S108.txt:5-9` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-73/S108.txt` | 5-9 | 150 | in range |
| `corpus/source-snapshots/round-73/manifest.json:48` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-73/manifest.json` | 48 | 52 | in range |
| `corpus/source-snapshots/round-78/S112.txt:195` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-78/S112.txt` | 195 | 216 | in range |
| `corpus/source-snapshots/round-82/S116.txt:22-23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-82/S116.txt` | 22-23 | 87 | in range |
| `corpus/source-snapshots/round-82/S116.txt:27` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-82/S116.txt` | 27 | 87 | in range |
| `corpus/source-snapshots/round-86/S122.txt:1` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-86/S122.txt` | 1 | 1 | in range |
| `corpus/source-snapshots/round-86/manifest.json:47-54` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-86/manifest.json` | 47-54 | 96 | in range |
| `corpus/source-snapshots/round-87/S124.txt:409` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-87/S124.txt` | 409 | 437 | in range |
| `corpus/source-snapshots/round-87/S124.txt:81-82` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-87/S124.txt` | 81-82 | 437 | in range |
| `corpus/source-snapshots/round-87/S124.txt:81-89` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-87/S124.txt` | 81-89 | 437 | in range |
| `corpus/source-snapshots/round-87/S124.txt:83-85` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-87/S124.txt` | 83-85 | 437 | in range |
| `corpus/source-snapshots/round-87/S124.txt:84-85` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-87/S124.txt` | 84-85 | 437 | in range |
| `corpus/source-snapshots/round-87/S124.txt:86-89` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-87/S124.txt` | 86-89 | 437 | in range |
| `corpus/source-snapshots/round-87/S125.txt:303-305` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-87/S125.txt` | 303-305 | 363 | in range |
| `corpus/source-snapshots/round-87/S125.txt:304-305` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-87/S125.txt` | 304-305 | 363 | in range |
| `corpus/source-snapshots/round-87/S125.txt:318-319` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-87/S125.txt` | 318-319 | 363 | in range |
| `corpus/source-snapshots/round-87/S125.txt:330-333` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-87/S125.txt` | 330-333 | 363 | in range |
| `corpus/source-snapshots/round-87/S125.txt:331` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-87/S125.txt` | 331 | 363 | in range |
| `corpus/source-snapshots/round-87/S125.txt:332-333` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-87/S125.txt` | 332-333 | 363 | in range |
| `corpus/source-snapshots/round-88/S126.txt:423-424` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S126.txt` | 423-424 | 584 | in range |
| `corpus/source-snapshots/round-88/S126.txt:425` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S126.txt` | 425 | 584 | in range |
| `corpus/source-snapshots/round-88/S126.txt:429-430` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S126.txt` | 429-430 | 584 | in range |
| `corpus/source-snapshots/round-88/S126.txt:433-434` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S126.txt` | 433-434 | 584 | in range |
| `corpus/source-snapshots/round-88/S126.txt:450-451` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S126.txt` | 450-451 | 584 | in range |
| `corpus/source-snapshots/round-88/S126.txt:452` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S126.txt` | 452 | 584 | in range |
| `corpus/source-snapshots/round-88/S126.txt:465-466` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S126.txt` | 465-466 | 584 | in range |
| `corpus/source-snapshots/round-88/S126.txt:466-473` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S126.txt` | 466-473 | 584 | in range |
| `corpus/source-snapshots/round-88/S126.txt:481-482` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S126.txt` | 481-482 | 584 | in range |
| `corpus/source-snapshots/round-88/S126.txt:483-484` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S126.txt` | 483-484 | 584 | in range |
| `corpus/source-snapshots/round-88/S126.txt:487-488` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S126.txt` | 487-488 | 584 | in range |
| `corpus/source-snapshots/round-88/S127.txt:402-404` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S127.txt` | 402-404 | 663 | in range |
| `corpus/source-snapshots/round-88/S127.txt:596` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S127.txt` | 596 | 663 | in range |
| `corpus/source-snapshots/round-88/S127.txt:599` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S127.txt` | 599 | 663 | in range |
| `corpus/source-snapshots/round-88/S127.txt:601` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S127.txt` | 601 | 663 | in range |
| `corpus/source-snapshots/round-88/S127.txt:605` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S127.txt` | 605 | 663 | in range |
| `corpus/source-snapshots/round-88/S127.txt:623` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S127.txt` | 623 | 663 | in range |
| `corpus/source-snapshots/round-88/S127.txt:631-633` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S127.txt` | 631-633 | 663 | in range |
| `corpus/source-snapshots/round-88/S127.txt:638` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S127.txt` | 638 | 663 | in range |
| `corpus/source-snapshots/round-88/S127.txt:638-639` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S127.txt` | 638-639 | 663 | in range |
| `corpus/source-snapshots/round-88/S127.txt:639` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-88/S127.txt` | 639 | 663 | in range |
| `corpus/source-snapshots/round-89/S128.txt:13` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S128.txt` | 13 | 225 | in range |
| `corpus/source-snapshots/round-89/S128.txt:202` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S128.txt` | 202 | 225 | in range |
| `corpus/source-snapshots/round-89/S128.txt:206-211` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S128.txt` | 206-211 | 225 | in range |
| `corpus/source-snapshots/round-89/S128.txt:212` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S128.txt` | 212 | 225 | in range |
| `corpus/source-snapshots/round-89/S128.txt:56-57` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S128.txt` | 56-57 | 225 | in range |
| `corpus/source-snapshots/round-89/S128.txt:56-59` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S128.txt` | 56-59 | 225 | in range |
| `corpus/source-snapshots/round-89/S128.txt:58-59` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S128.txt` | 58-59 | 225 | in range |
| `corpus/source-snapshots/round-89/S128.txt:62` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S128.txt` | 62 | 225 | in range |
| `corpus/source-snapshots/round-89/S128.txt:82-83` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S128.txt` | 82-83 | 225 | in range |
| `corpus/source-snapshots/round-89/S128.txt:94-95` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S128.txt` | 94-95 | 225 | in range |
| `corpus/source-snapshots/round-89/S128.txt:94-96` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S128.txt` | 94-96 | 225 | in range |
| `corpus/source-snapshots/round-89/S130.txt:14` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S130.txt` | 14 | 422 | in range |
| `corpus/source-snapshots/round-89/S130.txt:161-165` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S130.txt` | 161-165 | 422 | in range |
| `corpus/source-snapshots/round-89/S130.txt:163` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S130.txt` | 163 | 422 | in range |
| `corpus/source-snapshots/round-89/S130.txt:66` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S130.txt` | 66 | 422 | in range |
| `corpus/source-snapshots/round-89/S130.txt:66-69` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S130.txt` | 66-69 | 422 | in range |
| `corpus/source-snapshots/round-89/S130.txt:70-71` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S130.txt` | 70-71 | 422 | in range |
| `corpus/source-snapshots/round-89/S130.txt:70-73` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S130.txt` | 70-73 | 422 | in range |
| `corpus/source-snapshots/round-89/S130.txt:77-78` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-89/S130.txt` | 77-78 | 422 | in range |
| `corpus/source-snapshots/round-90/S131.txt:570` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-90/S131.txt` | 570 | 647 | in range |
| `corpus/source-snapshots/round-90/S131.txt:610` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-90/S131.txt` | 610 | 647 | in range |
| `corpus/source-snapshots/round-90/S131.txt:610-613` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-90/S131.txt` | 610-613 | 647 | in range |
| `corpus/source-snapshots/round-90/S131.txt:612` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-90/S131.txt` | 612 | 647 | in range |
| `corpus/source-snapshots/round-90/S131.txt:613` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-90/S131.txt` | 613 | 647 | in range |
| `corpus/source-snapshots/round-91/S133.txt:30` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 30 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:31` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 31 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:32` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 32 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:34` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 34 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:49` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 49 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:540` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 540 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:56` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 56 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:565` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 565 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:567` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 567 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:571` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 571 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:86` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 86 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:869` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 869 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:880` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 880 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:922` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 922 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:924` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 924 | 954 | in range |
| `corpus/source-snapshots/round-91/S133.txt:926` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S133.txt` | 926 | 954 | in range |
| `corpus/source-snapshots/round-91/S134.txt:102-105` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 102-105 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:106-107` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 106-107 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:123` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 123 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:17-19` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 17-19 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:22-23` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 22-23 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:25-28` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 25-28 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:255-258` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 255-258 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:27-28` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 27-28 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:419-420` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 419-420 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:421-426` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 421-426 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:91-92` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 91-92 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:91-95` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 91-95 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:92-95` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 92-95 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:93-95` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 93-95 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:97` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 97 | 441 | in range |
| `corpus/source-snapshots/round-91/S134.txt:97-98` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-91/S134.txt` | 97-98 | 441 | in range |
| `corpus/source-snapshots/round-92/S136.txt:150` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S136.txt` | 150 | 178 | in range |
| `corpus/source-snapshots/round-92/S136.txt:158` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S136.txt` | 158 | 178 | in range |
| `corpus/source-snapshots/round-92/S136.txt:160` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S136.txt` | 160 | 178 | in range |
| `corpus/source-snapshots/round-92/S136.txt:160-167` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S136.txt` | 160-167 | 178 | in range |
| `corpus/source-snapshots/round-92/S136.txt:161-167` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S136.txt` | 161-167 | 178 | in range |
| `corpus/source-snapshots/round-92/S136.txt:163` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S136.txt` | 163 | 178 | in range |
| `corpus/source-snapshots/round-92/S136.txt:164-167` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S136.txt` | 164-167 | 178 | in range |
| `corpus/source-snapshots/round-92/S137.txt:146-148` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S137.txt` | 146-148 | 274 | in range |
| `corpus/source-snapshots/round-92/S137.txt:153` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S137.txt` | 153 | 274 | in range |
| `corpus/source-snapshots/round-92/S137.txt:156` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S137.txt` | 156 | 274 | in range |
| `corpus/source-snapshots/round-92/S137.txt:156-162` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S137.txt` | 156-162 | 274 | in range |
| `corpus/source-snapshots/round-92/S137.txt:157-161` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S137.txt` | 157-161 | 274 | in range |
| `corpus/source-snapshots/round-92/S137.txt:162` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S137.txt` | 162 | 274 | in range |
| `corpus/source-snapshots/round-92/S137.txt:164` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S137.txt` | 164 | 274 | in range |
| `corpus/source-snapshots/round-92/S137.txt:166-167` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S137.txt` | 166-167 | 274 | in range |
| `corpus/source-snapshots/round-92/S137.txt:167` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S137.txt` | 167 | 274 | in range |
| `corpus/source-snapshots/round-92/S137.txt:173` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S137.txt` | 173 | 274 | in range |
| `corpus/source-snapshots/round-92/S137.txt:174` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S137.txt` | 174 | 274 | in range |
| `corpus/source-snapshots/round-92/S137.txt:177` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-92/S137.txt` | 177 | 274 | in range |
| `corpus/source-snapshots/round-93/S139.txt:87` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-93/S139.txt` | 87 | 414 | in range |
| `corpus/source-snapshots/round-94/S140.txt:4` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-94/S140.txt` | 4 | 563 | in range |
| `corpus/source-snapshots/round-94/S140.txt:429` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-94/S140.txt` | 429 | 563 | in range |
| `corpus/source-snapshots/round-94/S140.txt:430` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-94/S140.txt` | 430 | 563 | in range |
| `corpus/source-snapshots/round-94/S140.txt:446` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-94/S140.txt` | 446 | 563 | in range |
| `corpus/source-snapshots/round-94/S140.txt:447` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-94/S140.txt` | 447 | 563 | in range |
| `corpus/source-snapshots/round-94/S140.txt:463` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-94/S140.txt` | 463 | 563 | in range |
| `corpus/source-snapshots/round-94/S140.txt:464` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-94/S140.txt` | 464 | 563 | in range |
| `corpus/source-snapshots/round-95/S142.txt:169` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-95/S142.txt` | 169 | 182 | in range |
| `corpus/source-snapshots/round-96/S144.txt:346-347` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-96/S144.txt` | 346-347 | 418 | in range |
| `corpus/source-snapshots/round-96/S144.txt:348-395` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-96/S144.txt` | 348-395 | 418 | in range |
| `corpus/source-snapshots/round-96/S144.txt:356` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-96/S144.txt` | 356 | 418 | in range |
| `corpus/source-snapshots/round-97/S146.txt:68-70` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-97/S146.txt` | 68-70 | 238 | in range |
| `corpus/source-snapshots/round-97/S146.txt:69-70` | INTERNAL | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-97/S146.txt` | 69-70 | 238 | in range |

Every MIRROR-EQUIVALENT anchor in range is still only a *same-name same-path*
match against a Sep-5 genesis sync — see §Honest scope limits.

## Top-20 most-cited GONE paths

| # | citation | files citing | occurrences | noise flags |
|---|---|---|---|---|
| 1 | `[~]` | 82 | 199 | synthetic |
| 2 | `claims.json` | 63 | 107 | - |
| 3 | `.ufo/watchdog.log` | 54 | 59 | - |
| 4 | `source-recheck.py` | 48 | 71 | - |
| 5 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 43 | 46 | shell,synthetic |
| 6 | `git ls-remote origin refs/heads/master` | 38 | 38 | shell |
| 7 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | 35 | 41 | - |
| 8 | `anchorcheck.py` | 33 | 49 | - |
| 9 | `capture-source.py` | 31 | 43 | - |
| 10 | `frontier-recheck-count.py` | 30 | 45 | - |
| 11 | `resolve.py` | 27 | 51 | - |
| 12 | `density.py` | 26 | 36 | - |
| 13 | `status.json` | 23 | 49 | - |
| 14 | `w1-results.json` | 23 | 26 | - |
| 15 | `recheck-audit.py` | 22 | 31 | - |
| 16 | `SOURCES.md` | 22 | 27 | - |
| 17 | `claims/` | 21 | 35 | - |
| 18 | `templates/round-prompt.md` | 21 | 24 | - |
| 19 | `MISSION.md` | 20 | 22 | - |
| 20 | `ops/claim-check.mjs` | 18 | 37 | - |

Max over all citations: files citing = 98, occurrences = 224.

## MIRROR-EQUIVALENT — exact list (0)

| # | citation | mirror path | lines | files | method |
|---|---|---|---|---|---|
