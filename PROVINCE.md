# kasegi-shokunin — Province

**Domain:** bounty & security research — scopes ~/Projects/bounties, program rules, claim packages

**Round-15 status of the scope root (factual annotation, not a re-scope).**
`~/Projects/bounties` was removed from the filesystem at 2026-09-28T23:51:31Z
(actor UNDETERMINED, data PRESUMED-LOST locally):
`corpus/knowledge/source-tree-loss-2026-09-28.md`. The domain is unchanged —
bounty & security research, program rules, claim packages — but its surfaces now
resolve against two surviving roots: the frozen 2026-09-05 code mirror
`~/Projects/the-bounty-hunter` (HEAD `1cfbd86`) and
`~/Projects/origin-work/open-bug-bounties`, plus the corpus as the record of the
lost tree. Whether this file re-points is an operator decision, requested in
`../.ufo/l0-questions.md` (kasegi round-15 row); the lane did not re-scope
itself.
**Round-19 status (factual annotation, append-only).** Both surviving roots
named above are now ABSENT — `~/Projects/the-bounty-hunter` and the whole
`~/Projects/origin-work` tree disappeared on/around 2026-10-12 (no relocated
copy found under `~`; sibling `ufo-fsd-alpha` relocated intact to
`~/Projects/ufo-fsd-alpha`). Evidence: `corpus/knowledge/root-loss-2026-10-12.md`.
The province domain is unchanged; coverage claims against the absent trees are
corpus-attested records, not live-openable.

**Owns:** the domain knowledge, playbooks, error patterns, and checklists above.
**Refuses:** anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it.

## Core

The line-3 domain comprises program rules, scopes, and claim packages; the
core also covers triage and claim gates, and submission/disclosure packaging.
These surfaces are corpus-attested, while their source roots are absent. This
is a classification, not a re-scope: re-scope remains the operator's decision
under L0 kasegi round-15.

## Frontier

General practice that governs every program is indexed in corpus/README.md
under Frontier F01–F10 (F09, round 24: authorisation outside the platform — the
engagement document and the statute; F10, round 25: vendor-side disclosure policies as
corpus objects; 10/10 admitted).
F11 — ISO/IEC 29147/30111 division-of-labour (JPCERT/CC 2026 guideline) — admitted round 26

## Adjacent

Sibling lanes are reported, not absorbed:

- chousa — research method and source hierarchy
- kagi — secrets and vault handling
- kake — web properties
- kengaku — LLM evaluation and benchmarks

Live-target testing is refused; this corpus is documentation only.

## Frontier amendment — F12-F15 (appended round 31, 2026-10-25)

[r31 amendment, appended 2026-10-25; end-of-file append per R6, so every existing line keeps its
number] The Frontier section above names F01–F10 and F11 only. This amendment appends the four
admissions it does not name, without editing that paragraph:

- F12 — Japanese state-coordinated disclosure workflow — admitted round 28
- F13 — Program severity ladders and reward scales — admitted round 29
- F14 — Japanese severity vocabulary and the handling-priority model — admitted round 30
- F15 — vendor-side research programme as an intake route for other vendors' bugs (Microsoft
  MSVR) — admitted round 31; entry `corpus/knowledge/vendor-third-party-finding-coordination.md`
  (header `ground: F15`, `source: S048`, capture `corpus/source-snapshots/round-31/S048.txt`)

[r31 correction, R9] The "10/10 admitted" parenthetical in the Frontier paragraph above is the
round-25 frontier state (F10 was the round-25 admission) and is retained as history rather than
rewritten; the frontier as of round 31 is F01–F15. Titles and round attributions for F12–F14 are
read from the `corpus/README.md` frontier rows at :213, :264 and :284; F15's round attribution is
this round's admission (round-31 claims, C2), and its entry binds the frontier as `ground: F15`
against the round-31 capture `corpus/source-snapshots/round-31/S048.txt`.

[r33 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F16 — Chinese crowdsourced-testing platform scope and reward rules (CNVD 众测, 360SRC) — admitted round 33
[r34 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F17 — Immunefi Vulnerability Severity Classification System v2.2 (Web3/smart-contract bounty severity classification) — admitted round 34

[r36 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F18 — CISA Known Exploited Vulnerabilities catalog (prioritization by known in-the-wild exploitation status) — admitted round 35; entry `corpus/knowledge/cisa-kev-catalog.md` (source S052)
[r36 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F19 — FIRST Exploit Prediction Scoring System (EPSS) (exploitation-likelihood scoring, 0–1 probability) — admitted round 36; entry `corpus/knowledge/epss-exploit-prediction-scoring.md` (source S053)

[r37 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F20 — SSVC (Stakeholder-Specific Vulnerability Categorization) decision-point-based prioritization — admitted round 37; entry `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` (source S054)
```

| property | value |
|---|---|
| sha256 (block bytes) | `cdfe44e319094957ec583b7c3cd8212b882752b75682d9f1cf4d0b734f20f545` |
| bytes / lines | 295 / 2 |
| placement | after line 78 (`…(source S053)` + newline); result 80 lines |
| source of the F20 sentence | the round-37 frozen claim C2 wording (SSVC — Stakeholder-Specific Vulnerability Categorization, decision-point-based prioritization) and the item's mandated line text |

## 3. Deliverable B — `corpus/README.md` end-of-file block

Append verbatim at EOF. The file currently ends with a blank line (`...stays outside it.\n\n`), so the
block starts directly with `##` (no extra leading newline: the boundary stays a single blank line) and
ends with the file's terminal blank line. Lines 1-398 stay byte-identical; the result is 425 lines.

```text
## Round-37 admission — coverage map row and Frontier F20 (appended 2026-10-26)

The coverage map above is not edited in place (R6): the round-37 entry
`knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` (Frontier F20, source S054;
source basis: CERT/CC's SSVC "What is SSVC?" overview tutorial at
https://certcc.github.io/SSVC/tutorials/ssvc_overview/ — the overview page, not the docs home, per
`claims-erratum-1.md` and capture-binding rule B5 — captured 2026-10-26, status 200, under
`corpus/source-snapshots/round-37/`) is recorded here as an appended amendment so every existing
line keeps its number. The coverage-map row is appended here rather than inserted into the map, and
the F20 frontier row is listed here on the same table shape as the frontier above.

| Area | Entry | Source basis |
|---|---|---|
| Stakeholder-specific vulnerability categorization (round 37) | knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md | S054 — public primary, opened 2026-10-26 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F20 | SSVC (Stakeholder-Specific Vulnerability Categorization) — stakeholder-tailored, decision-point-based prioritization | admitted | knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md | S054 | Read a priority from one stakeholder's decision model, not a universal score: "A decision point itself is not representative of risk, but the series of decisions point values help a stakeholder determine how risky a vulnerability is" (S054.txt:277; the page's own typo "decisions point values" is quoted verbatim), and the inputs are per-system — Exposure asks how difficult it is for an attacker to access a system from the open Internet (S054.txt:367). Keep it distinct from CVSS severity, KEV status and EPSS likelihood: SSVC categorizes "by priority based on risk that varies among stakeholders" (S054.txt:259), and the page contrasts itself with systems that "rate on technical severity" (S054.txt:247) while naming no CVSS metric and defining neither severity nor exploitability in prose — CVSS, EPSS and KEV appear only in site navigation, so source those definitions from S001/S002, S052 and S053. Read "Carnegie Mellon" only as the site footer's owner statement, not as a methodology claim. |

[r37 amendment, appended 2026-10-26] The parenthetical above records the round-26 frontier state
and each later amendment paragraph states its own round; those are retained as history, not
rewritten (R9): at round 37 the frontier stands at **20/20 admitted** — F01-F08 at round 23, F09
at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30,
F15 at round 31, F16 at round 33, F17 at round 34, F18 at round 35, F19 at round 36, F20 at
round 37. The 0/18 sentence is untouched: the lost-domain denominator still holds 0 of 18
surfaces present, and the frontier count stays outside it.

```

| property | value |
|---|---|
| sha256 (block bytes) | `2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b` |
| bytes / lines | 2947 / 27 |
| row shape | six cells (id, topic, status, entry, sources, next), topic names SSVC as stakeholder-tailored decision-point prioritization, entry path `knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`, source `S054` |
| count line | `[r37 amendment, appended 2026-10-26]` naming `20/20 admitted` and F01-F08 r23, F09 r24, F10 r25, F11 r26, F12 r28, F13 r29, F14 r30, F15 r31, F16 r33, F17 r34, F18 r35, F19 r36, F20 r37; the 0/18 sentence is declared untouched |
| URL choice | overview tutorial page per `claims-erratum-1.md`; the paragraph says so and why (capture-binding B5) |

## 4. Validation on a scratch mirror (append, not edit)

Fixture: `git archive HEAD PROVINCE.md corpus` exported into
`/fast/scratch/hyaku/kasegi-r37/ScribeFrontierAmendments/mirror`, both blocks appended with Python to the
copies only. Measured on that mirror:

| check | command | observed |
|---|---|---|
| pure addition (PROVINCE) | `diff orig PROVINCE.md \| grep -c '^<'` | `0` (2 added lines) |
| pure addition (README) | `diff orig corpus/README.md \| grep -c '^<'` | `0` (27 added lines) |
| frontier row count | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `20` (target `20`) |
| row cells | pipe-split of the F20 line | 6 cells; next cell 155 words |
| section header | `grep -c '^## Round-37 admission' corpus/README.md` | `1` |
| count line | `grep -c 'frontier stands at \*\*20/20 admitted\*\*' corpus/README.md` | `1` |
| PROVINCE line | `grep -c '^\[r37 Frontier amendment' PROVINCE.md` | `1` |
| sizes | `wc -l` on the mirror | `PROVINCE.md` 80, `corpus/README.md` 425 |

Harness on the same mirror (`HYAKU_SCRATCH=<scratch> python3 corpus/instruments/frontier-recheck-count.py
--root <mirror>`, tail):

Correction (round 38): PROVINCE.md L79-L152 — the whole round-37 append — hold the intended 2-line amendment at L79-L80 (a blank line and the `[r37 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F20 — …` line, sha256 cdfe44e319094957ec583b7c3cd8212b882752b75682d9f1cf4d0b734f20f545) followed by misplaced receipt scaffolding at L81-L152 copied from `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md`: a duplicated F20 row, property tables, a "Validation on a scratch mirror" section, and stray fences; L81-L152 are to be read as not part of the province.

[r38 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F21 — OASIS CSAF v2.0 (Common Security Advisory Framework) VEX product-status categories and not-affected justification flags — admitted round 38; entry `corpus/knowledge/csaf-vex-product-status-and-justifications.md` (source S055)

[r39 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F22 — CISA When to Issue VEX Information (VEX issuance/lifecycle/reaffirmation/inheritance guidance) — admitted round 39; entry corpus/knowledge/cisa-when-to-issue-vex.md (source S057)


[r40 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F23 — CycloneDX v1.7 vulnerabilities[].analysis (six analysis states, nine not-affected justifications, a repeatable response array and a per-version status) — admitted round 40; entry corpus/knowledge/cyclonedx-analysis-subtree.md (source S060)

[r41 Frontier amendment, appended 2026-10-27, end-of-file append per R6] F24 — RFC 9116 security.txt (the machine-readable disclosure-channel discovery file: the /.well-known/ location, eight defined fields with Contact and Expires required, and the Expires staleness clock) — admitted round 41; entry corpus/knowledge/rfc-9116-security-txt.md (source S063)

[r42 Frontier amendment, appended 2026-10-28, end-of-file append per R6] F25 — CVE JSON record format (the machine-readable CVE record: the four required root properties dataType/dataVersion/cveMetadata/containers, one 'cna' container plus optional 'adp' containers, and the PUBLISHED and REJECTED states) — admitted round 42; entry corpus/knowledge/cve-json-record-format.md (source S064)

[r44 Frontier amendment, appended 2026-10-28, end-of-file append per R6] F26 — Google Cloud VRP program scope and customer-resource testing boundary — admitted round 44; entry `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` (source S069)

[r45 Frontier amendment, appended 2026-10-28, end-of-file append per R6] F27 — Linux kernel security-bugs reporting process (e-mail report channel with a security-team Cc rule, 7-day release postponement ceiling with a 14-day exception, AI-found, binary-only and unreproducible refusal rules) — admitted round 45; entry `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` (source S071)

[r46 Frontier amendment, appended 2026-10-28, end-of-file append per R6] F28 — GitHub private vulnerability reporting, reporter flow (enablement by owners of public repositories and separation from SECURITY.md, the advisory form's default required fields, the optional AI-assistance disclosure, automatic reporter collaborator and credit, and the temporary private fork that only the maintainer can merge) — admitted round 46; entry `corpus/knowledge/github-private-vulnerability-reporting.md` (source S073); scope limit: reporter flow only — maintainer handling, the GHSA database and CVE assignment stay out


[r46 Frontier amendment, appended 2026-10-29, end-of-file append per R6] F29 — GitHub repository security advisories, maintainer-side lifecycle (the draft advisory and the private discussion of the vulnerability's impact, the temporary private fork, advisory credit, the CVE request to GitHub as a CNA with its 72-hour review, publication visibility and the unchanged advisory URL, and the fix version added before publication) — admitted round 46 (attempt 2); entry `corpus/knowledge/github-repository-security-advisories.md` (source S074); scope limit: maintainer-side advisory lifecycle only — the reporter flow stays F28, and advisory editing, the REST API for repository security advisories and GitHub Advisory Database edits stay out

[r49 Frontier amendment, appended 2026-10-30, end-of-file append per R6] F30 — CVE Services publication API (the CVE Program's own write path: identifier reservation, CNA-container publication and update, rejection, ADP-container enrichment and the CNA↔Secretariat conversation endpoint) — admitted round 49; entry `corpus/knowledge/cve-services-publication-api.md` (source S078; capture `corpus/source-snapshots/round-49/S078.txt`); scope limit: the service interface only — the record's data model stays F25 and the numbering rules stay F07

[r50 Frontier amendment, appended 2026-11-01, end-of-file append per R6] F31 — OSV affected-range events (the OSV format's per-package version timeline: affected[].ranges[].events with introduced/fixed/last_affected/limit, at least one introduced event, an implicit limit "*", and three range types ordered by SemVer precedence, ecosystem logic or Git reachability) — admitted round 50; entry corpus/knowledge/osv-affected-range-events.md (source S080; capture corpus/source-snapshots/round-50/S080.txt); scope limit: the format's range/event semantics only — the osv.dev service API, the JSON Schema validation artifact, individual database exports and per-database database_specific values stay out

[r51 Frontier amendment, appended 2026-11-01, end-of-file append per R6] F32 — CISA Vulnrichment (the public repository of CISA's enrichment of public CVE records through CISA's ADP container: SSVC decision points on every analyzed CVE, CWE and/or CVSS for higher-risk CVEs, KEV blocks for KEV-listed CVEs, a CNA-precedence rule that drops ADP assessments when the CNA catches up, a major.minor.patch SSVC version encoding, CPE discontinued 2024-12-10) — admitted round 51; entry corpus/knowledge/cisa-vulnrichment-adp-enrichment.md (source S081; capture corpus/source-snapshots/round-51/S081.txt); scope limit: CISA's enrichment program and its data rules only — the CVE record format stays F25, the SSVC framework stays F20, the KEV catalog stays F18, the VEX guidance stays F22 and the CVE Services interface stays F30

[r51 status annotation, appended 2026-11-01, factual, append-only] The round-19 "ABSENT" record for
`~/Projects/origin-work/open-bug-bounties` stands: no local checkout has returned. A same-named public
GitHub mirror now exists (`https://github.com/VeigaPunk/open-bug-bounties`, branch main, HEAD 4c895519,
pushed 2026-10-31T17:17:48Z, described as "Public Open Bug Bounties board (GitHub Pages mirror of ChatGPT
site)"), but its history provably lacks the lost checkout's recorded HEAD `1307b8b` (gh api commits/1307b8b
→ 422 "No commit found for SHA") and its root inventory matches neither the r15 package-dir layout nor the
receipt-store (probe receipt `.ufo/waves/round-51/controls/mirror-probe.txt`). The identity question is
answered negatively on this evidence and the mirror is recorded as registry row S082 (rejected, with flip);
RECEIPT-STORE-LOST stays corpus-attested-only and nothing in this province re-grounds against the mirror.

[r52 Frontier amendment, appended 2026-11-01, end-of-file append per R6] F33 — NVD API 2.0 (NIST's read-side retrieval interface over the NVD-enriched CVE record: the 2.0 paging envelope, NVD's own Primary CVSS served beside the CNA's Secondary with per-item provenance, CPE applicability configurations, CWE weaknesses, tagged references, multilingual descriptions, published/lastModified/vulnStatus change tracking, and the ingested CISA ADP SSVC block) — admitted round 52; entry corpus/knowledge/nvd-api-2.0-retrieval-interface.md (source S083; capture corpus/source-snapshots/round-52/S083.txt); scope limit: the retrieval interface's response contract as served for one record only — the CVE record format stays F25, the CVE Services write path stays F30, the ADP enrichment program stays F32, the KEV catalog stays F18, EPSS stays F19, and rate limits/authentication/the wider parameter surface are unasserted (the developer-hub pages are JS-walled for the lane instrument; rejected row S084 with flip); S066's round-42 flip is spent by this admission, the row itself unchanged

[r52 adjacency annotation, appended 2026-11-01, factual, append-only — the round-51 closure's neighbor-screen observation] The round-51 pre-freeze screen for F32 quoted its scope as corpus/knowledge/, corpus/README.md, PROVINCE.md, corpus/SOURCES.md and SKILL.md, and one byte OUTSIDE that scope also named the surface at the round-51 base: corpus/source-snapshots/round-24/S013.txt:65 (the MITRE CWE Top 25 2025 methodology capture, mined by F05's entry cwe-top25-2025-methodology.md) lists "CISA Vulnrichment" among its data sources. This is a downstream-consumer relationship — F05 consumes the Vulnrichment output as methodology input; it holds none of the enrichment-program ground F32 admits — and S013 remains OUT OF SCOPE as a mining surface (a round-24 capture of another organization's document; nothing here re-scopes it). Recorded as a scope note, not an admission; from round 52 the pre-freeze neighbor screen includes the downstream-consumer sweep over corpus/source-snapshots/ (applied in F33's screen, receipt .ufo/waves/round-52/controls/neighbor-screen-r52.txt), and the figure-class lesson is doubled by the round-52 gate-quote-audit instrument.
[r53 Frontier amendment, appended 2026-11-01, end-of-file append per R6] F34 — NVD API 2.0 response schema (NIST's own JSON Schema contract for the API 2.0 response: the versioned 2.2.4 draft-07 document, the schema-required envelope keys, the per-record required five, the CVE-id pattern, and the NVD-only evaluator*/cisa* mirror fields and metrics vocabulary one live response need not carry) — admitted round 53; entry corpus/knowledge/nvd-api-2.0-response-schema.md (source S085; capture corpus/source-snapshots/round-53/S085.txt); scope limit: the response-body contract only — the served instance stays F33, the canonical record format stays F25, the ADP enrichment program stays F32, the SSVC framework stays F20, and rate limits/authentication/query parameters/error responses are unasserted (S066 re-opened under its unspent mirror-field flip term, the rejected row byte-identical)

[r54 Frontier amendment, appended 2026-11-01, end-of-file append per R6] F35 — OpenSSF Scorecard check documentation (the per-check risk tiers and scoring criteria of automated repository security-health scoring: the 90-day commit-rate maintenance window with its >90-day assessability floor, OSV-service-backed vulnerability detection with the declared osv-scanner.toml suppression mechanism, conditionally-worded per-check risk labels, and the SECURITY.md presence-and-content policy detector) — admitted round 54; entry corpus/knowledge/openssf-scorecard-checks.md (source S086; capture corpus/source-snapshots/round-54/S086.txt); scope limit: the check documentation's declared detection and scoring rules only — the aggregate 0-10 score computation, weights, publisher/API and Prox are unasserted, the OSV format stays F31, KEV stays F18, the severity ladders stay F13/F17, and the disclosure-channel documents stay F24 (security.txt; SECURITY.md presence is this document's own detection surface, not security.txt ground)

[r55 Frontier amendment, appended 2026-11-01, end-of-file append per R6] F36 — GitHub repository security advisories REST API (the repository-advisories machine interface contract: the twelve-endpoint route family, per-endpoint fine-grained permission sets with the private-fork route's dual advisories-read + Administration-write line, the POST/PATCH create-update pair with its required-body contract and the closed published/closed/draft state vocabulary, and the standalone ghsa_id-keyed CVE-request route returning 202 Accepted) — admitted round 55; entry corpus/knowledge/github-repository-security-advisories-rest-api.md (source S087; capture corpus/source-snapshots/round-55/S087.txt); scope limit: the REST interface contract only — the maintainer-side lifecycle stays F29, the reporter flow stays F28, the CVE record format stays F25, the CVE Services write path stays F30, and rate limits/plan-gated parameters/response examples/error schemas are unasserted

[r56 Frontier amendment, appended 2026-11-01, end-of-file append per R6] F37 — CISA Vulnrichment published record list (the catalog surface of CISA's ADP record publication at the repository's default ref, read through GitHub's git-trees machine interface: the 28 per-year record folders 1999-2026 with no gap, the six non-record support entries beside them, the content-addressed completeness pin `"truncated":false` at top sha e8d691a5, and the 8501-byte README blob whose round-51 snapshot sha reproduces same-day) — admitted round 56; entry corpus/knowledge/cisa-vulnrichment-record-list.md (source S088; capture corpus/source-snapshots/round-56/S088.txt); scope limit: the catalog surface only — the enrichment program's data rules stay F32, the per-CVE record contents and format stay F25, the SSVC framework and the named-but-unasserted flowcharts.md details stay F20, the CVE Services interface stays F30, NVD's serving stays F33, and the year folders' contents, sync cadence, commit history, rate limits and authentication are unasserted

## Round-57 cloud surface annotation (2026-11-02)

Current writable lane: `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi`.
Fleet contract: `/workspace/scratch/e2fdad13233f/shokunin-training/shokunin` (read-only to lane).
Historical lost domain roots remain unavailable; this is not recovery or a denominator re-scope.
F31 is deepened by bounded synthetic OSV affectedness evaluation on S089, not expanded to a
service/API, scanner, live target, general ecosystem comparator, or Git-graph engine. The
round-57 named correction in its existing knowledge entry governs over the earlier summary.

[r58 F27 deepening, 2026-11-02] `corpus/knowledge/kernel-report-evidence-assessment.md` and `corpus/instruments/kernel-report-assess.py` add bounded synthetic report judgment to existing kernel reporting ground. The ACL replay is a teaching model, not kernel testing. No new numbered frontier or source-root restoration; live-target testing and submission remain refused. Research methods remain chousa-owned; secret handling remains kagi-owned.

[r58 named correction to r45 F27 description at line 169, 2026-11-02] The phrase `AI-found, binary-only and unreproducible refusal rules` conflated distinct rules. AI assistance does NOT itself cause refusal; the kernel guidance treats such findings as public while withholding the reproducer from public text. Binary-only and reproduction deficiencies are separate evidence concerns. S090 and `corpus/knowledge/kernel-report-evidence-assessment.md` govern this distinction; the r45 bytes remain historical, not current blanket-rejection advice.

[r60 F20 deepening, 2026-11-02] Pinned CERT/CC deployer DT_DP1.0.0 fictional
assessment dossier adds contextual input judgments and paths; it does not own
supplier/CISA priority, universal risk or actual remediation decisions. Existing
lost roots and sibling boundaries unchanged; no new frontier denominator.

## Round61 scope note
Existing F05 deepened with bounded fictional CWE causal-evidence assessments;
no live-target testing, exploit payload or submission. CWE definitions inform
classification, not proof of a real vulnerability or permission to investigate.
