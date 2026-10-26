# ScoutF19Sibling — F19/S053 sibling-lane EPSS sweep (read-only), round 36

Lane head at read time: b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6 (claims-freeze). No lane/fleet/shokuknow file was written; no tool installed.

## Verdict: UNCONTESTED (neither contested nor ratified by any sibling)
F19 (FIRST EPSS) / S053 has **zero sibling ground**: no sibling lane carries a source row, knowledge entry, frontier, claim, or doctrine line on EPSS or exploitation-likelihood scoring. Nothing contradicts S053/F19 and nothing pre-ratifies it. F19 therefore stands on kasegi's own primary-source capture (S053) and the harness PASS, not on sibling corroboration. Admission is not blocked by overlap; there is no duplicate-coverage risk.

## Commands (all read-only, `--exclude-dir=.git`)
1. Task-spec loose sweep, case-insensitive `EPSS|exploit prediction|exploitation` over `/home/vgpnk/Projects/shokunin/*-shokunin` minus kasegi: **498 files**, all false positives (breakdown below).
2. Strict sweep, case-sensitive/word-bounded `\bEPSS\b|[Ee]xploit[ -][Pp]rediction|Exploit Prediction Scoring|[Ee]xploitation[- ]likelihood|exploit(ation)? probability|first\.org/epss` over the same 20 lanes: **0 files**.
3. `/home/vgpnk/Projects/shokuknow/doctrine/` (12 files) for `\bEPSS\b|[Ee]xploit[ -][Pp]rediction|[Ee]xploitation`: **0 hits**. Whole `/home/vgpnk/Projects/shokuknow` (excl .git) for `\bEPSS\b|Exploit Prediction Scoring`: **0 hits**.

## Hit table (loose sweep, 498 files, classified by matched token)
| Matched token | Where | Files (≈) | Real EPSS ground? |
|---|---|---|---|
| `epssweep` / `_arm_epssweep` / `r98b_epssweep` (identifier substring) | game-dev-2d-shokunin corpus/fixtures r98b_attack.gd, run_battery.py, corpus/live/**, reports/round-98..104 | ~97 (323 token hits) | No — a Godot-boundary-test sweep identifier, not EPSS |
| `LeinenEPSSJ24` (DBLP key of Leinen et al. ICST 2024 flaky-test cost paper) | tameshi-shokunin corpus/knowledge/r8-flaky-cost-baseline.md, .ufo/evidence/round-47/**, .ufo/waves/round-47/w1/T47* | 11 hits / ~11 files | No — author-initials substring "EPSS" inside a bibliographic key; paper is about flaky-test cost, not vulnerabilities |
| random base64/hash substrings (`epSs`, `ePss` …) | kotodama-shokunin reports/supplement-opencode-1/scratch/*.txt, kotodama transcripts + `.scratch` copies, kotoba omp-live strings dump | ~20 | No — noise |
| `exploitation` generic, safety-scope boilerplate ("no exploitation/live execution") | tabi (≈153 files, 112 in one assignment text), kake, kengaku, mori, souji, tameshi, kama, kaidoku, kagi, kumitate, tsukuroi, chousa, mado, game-dev-3d | ~330 | No — non-goal/scope sentences, not vulnerability-likelihood scoring |
| `exploitation` in cited abstracts (agriculture/archaeology "secondary products", "cultural exploitation", "exploitation of synergies") | kotodama (≈102 files), revenger, mado, kotoba | ~110 | No — unrelated domains |
| `exploitation` as a security noun, incidental | mori ("Exploitation tricks > Unsafe redirect", SSRF/OWASP), tabi (prerender "road to exploitation"), mado (attack-window paper), kama/chousa/tsukuroi (hostile-path sentences) | ~30 | No — attack-surface prose; no probability scoring |

Strict-match count across all 20 sibling lanes: 0.

## Adjacent (not EPSS) vulnerability-prioritisation ground, for context only
- kagi-shokunin `.ufo/waves/round-28/retained-probes/SrcCve202010735/nvd-api*.json` (4 files): NVD API probe retaining CISA-ADP SSVC fields `"exploitation":"none"`, `"automatable":"no"`, `"technicalImpact"` for CVE-2020-10735. This is the SSVC *Exploitation* decision point, a different framework from EPSS; it is a retained probe, not a SOURCES row or knowledge entry (kagi corpus has no SSVC/EPSS mention). Does not contest F19.
- mori-shokunin SOURCES S012 (GHSA systemd-oomd advisory; page text contains a CVSS score line), S049/S222 (OWASP cheat sheets): security advisories/guidance, no EPSS. CVSS-only mentions.
- shokuknow doctrine: CVE/vulnerability mentions only in channel-index-japanese.md (JVN/JVN iPedia advisory channels), channel-index-chinese.md (CNVD, kernel CVE notice), verified-numbers.md (Japanese vulnerability corpus count). Channel/coverage doctrine, no EPSS/exploit-prediction content.
- souji-shokunin and kotoba/kaidoku/kake/kama/kengaku/tameshi: no CVSS/KEV/EPSS in corpus knowledge or SOURCES.

## Implications for the round
- No sibling-collision on the F19 topic: the quarantine/id-collision rerun need not consider EPSS prose; S053 id uniqueness is lane-local (ScoutIdCollisions owns that).
- Entry-scribe note: kasegi's EPSS entry cannot cite sibling lanes for corroboration; the junk-twin/negative sweep command (`grep -rilE 'EPSS|exploit prediction|exploitation likelihood'` over kasegi corpus/knowledge) should keep strict anchors — the loose `exploitation` alternative is noise-prone (498 false positives in siblings alone).
- If a "does any sibling already cover this" gate is wanted, use the strict regex in command 2; the loose spec regex over-matches via the `epssweep` identifier and `LeinenEPSSJ24`.

Confidence: high on zero strict hits (full-tree grep, 20 lanes + shokuknow, .git excluded; binary files skipped via -I, so a hit inside a PDF/binary would not show — none expected). Unresolved: none.
Scratch: /fast/scratch/hyaku/kasegi-r36/ScoutF19Sibling removed before yield.
