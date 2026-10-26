# ConnSibling — round-40 sibling-overlap scan (receipt)

Seat: ConnSibling (§3 connector, leaf — no subagent dispatch). Deliverable: `ConnSibling.txt` (written beside this receipt). No tool installs were made (no new tool needed; RULES.md read).

## Scan scope (all read-only; no sibling edits)

- Targets: 20 sibling lanes (`*-shokunin` except kasegi) — `corpus/knowledge` (all files), `PROVINCE.md`, `corpus/SOURCES.md` registries; fleet-root `MISSION.md`, `README.md`, `CORPUS.md`, `AGENTS.md`, `AXES.md`.
- Grep tool per-topic patterns over explicit path lists (20 dirs / 20 files per call):
  - CycloneDX|cyclonedx|cyclone-dx|SBOM → only kaidoku: Ghidra `bom.json` (157 KB) and panic-string crate maps ("a dependency SBOM with versions") on its provenance-fidelity axis; `2026-10-13-r4-06-1password-asar.md` suggests a dependency-CVE pass "in a dedicated lane". No CycloneDX standard content anywhere.
  - Anthropic|anthropic → game-dev-3d (Claude plugins marketplace), kama (`anthropic/claude-opus-5-5` alias rows), kengaku (scan term in grader), kotoba (skills docs S012–S015/S019/S211), kumitate (`protocol = "anthropic"`, S015/S025). No CVD content.
  - Project Zero / reporting transparency / transparency trial → no matches in any sibling.
  - BOD 20-01|SP 800-216|federal vulnerability disclosure|vulnerability disclosure policy|vulnerability-disclosure → no matches.
  - CISA|NIST|Department of Justice|federal → NIST hits only as FIPS 180-4 / SP 800-122 / SP 800-92 / CFTT references (revenger, mori, kotodama) — none VDP-related; no CISA or DOJ matches.
  - coordinated vulnerability disclosure|CVD|safe harbor|responsible disclosure|disclosure policy → no matches in sibling knowledge (chousa PROVINCE.md names `bounty-program scope and claim packages (→ kasegi)` in its refusals).
  - CVE-Bench|2503.17332|AI-agent exploit|exploitation benchmark → no matches. `benchmark-selection.md` (kengaku) lists "EVMbench (security/exploit)" under Add-if-relevant agent benchmarks — the eval boundary for S025.
  - CSAF|VEX|CycloneDX|SBOM → kake `security-txt-publishing.md` mentions `CSAF` once as an IANA-registered extension field name in `security.txt` (S079); no VEX/CSAF-version content anywhere.
  - bounty|CVE|exploit|vulnerability in sibling knowledge → chousa refusal vocabulary (`SCOPE_BOUNTY_ABSORBED` → kasegi, `SCOPE_MODEL_QUALITY_ABSORBED` → kengaku, `SCOPE_ORCHESTRATION_ABSORBED` → kumitate); kaidoku "dependency-CVE pass" suggestion; kengaku EVMbench; kotoba harness "exploit passes" counts. Nothing owning any planned admission.
- SOURCES.md registry scan for the planned source URLs (anthropic.com CVD, projectzero.google, csrc.nist.gov/pubs/sp/800/216, justice.gov ccips file, cisa.gov BOD 20-01, arxiv 2503.17332, oasis-open csaf, cve.org, eur-lex 2024/2847): no sibling opened any. (Note: kotoba's own registry also has an S019 row — "Anthropic Agent Skills best practices" — an ID collision with kasegi's S019 = NIST SP 800-216; cross-lane citations must be lane-qualified. No content overlap.)
- Ownership affirmations found: fleet `MISSION.md`/`README.md` roster kasegi = "bounty/security research"; chousa `SCOPE_BOUNTY_ABSORBED`; kama `cross-lane-scope.md` "kasegi retains bounty/target-scope research"; kotoba `sibling-overlap-census-round49/74.md` — kasegi owns "bounty & security research (programs, rules, claim packages)"; kake PROVINCE.md "Vulnerability handling itself stays out of province: report intake, triage, remediation, disclosure timing, bounty and policy operation … are not kake's ground".

## Rulings (deliverable `ConnSibling.txt`, 19 lines, sha256 66cf055f176584e098a63f7ea4648e062b532d8f722d62910d67208c09a19eb1)

| Planned admission | Ruling | Grounds |
|---|---|---|
| F23 CycloneDX analysis subtree | uncontested (adjacent: kaidoku SBOM content extraction, provenance-fidelity) | no sibling holds CycloneDX/analysis-format claims |
| S016 AI-CVD (Anthropic) | uncontested | sibling Anthropic refs are skills/packaging/model-provider only |
| S017 transparency trial (Project Zero) | uncontested | no sibling cites Project Zero |
| S019/S020/S021 federal VDP | uncontested (adjacent: kake security.txt publishes pointers; chousa routes bounty scope → kasegi) | no sibling cites NIST SP 800-216 / DOJ / BOD 20-01 |
| S023 CISA process | uncontested | no sibling cites CISA's CVD program |
| S025 CVE-Bench/AI-agent exploitation | contested — kengaku LLM-eval boundary | kengaku owns benchmark selection/offline replay grading; lists security/exploit agent benchmarks (EVMbench) |
| CSAF v2.1 os/ | uncontested | kake names CSAF only as an IANA extension field in security.txt |
| VEX Status Justifications | uncontested | no sibling holds VEX/justification-flag semantics |

Constraint for the S025 admission: kasegi mines the paper for the disclosure-process implication only ("task-specific, reproducible benchmark outcomes; do not generalize exploitation results into finding/triage accuracy"); AI-agent capability-measurement claims stay with kengaku (existing reciprocal rule: kengaku interprets kasegi's ledger read-only, kasegi does not enter eval craft).
