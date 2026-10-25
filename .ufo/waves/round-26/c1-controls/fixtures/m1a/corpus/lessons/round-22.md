# Round 22 — kaika: admission bar, source registry, frontier, provenance

- **Claims.** C1 `depth:verifiability` — provenance closure over the 25 existing `corpus/knowledge/` entries (`source:`, `verified-at:`, `recheck:` on every entry) plus historical marking of the live dead-path lines; C2 `coverage` — five new frontier entries on currently uncovered public art (CVSS v4, CVD timelines, safe harbor vs scope, AI-assisted finding validation, CWE Top 25 2025 methodology), a corpus/SOURCES.md registry, a `## Frontier` section in `corpus/README.md`, and Core/Frontier/Adjacent sections in `PROVINCE.md`.
- **Setup.** `corpus/QUALITY.md` was minted as setup — Q1–Q6 entry criteria and R1–R6 record criteria (R6 added in-round for M17), each grounded in a mined mistake recorded below; it was uncommitted in the worktree when this lesson was written.
- **Status.** Claims declared, not measured; this file claims no score move and no verified-round credit.

## Mistakes

Pointers were re-opened in this worktree on 2026-10-19. A pointer is unresolvable only when the evidence could not be reached from the lane worktree or its fleet ledger; such a pointer is marked `[unverified: why]`. `captured-by before r22` names the closest pre-existing lane rule (SKILL.md, `corpus/instruments/`, `corpus/knowledge/citation-bases.md`) or `none` when no rule covered the class. `captured-by now` names the `corpus/QUALITY.md` criterion whose "grounded in" cell cites the row; `none` carries the reason and, where it applies, the rule that already held.

| id | class | evidence pointer | captured-by before r22 | captured-by now | fix |
|---|---|---|---|---|---|
| M1 | Completion-evidence failure: 273 B marker filed as a round closeout | fleet MANIFEST index 63 (r16 closure): report 273 B, hex tokens 0, SHONEN 0, first body line `# kasegi round-16 closeout (marker)` => failed; introducing commit 17c1fadfddc5ecbfa5ef362ef44d111792fa3e94 resolves in the fleet-root object db but not here (`git cat-file -t 17c1fad` fails in this worktree); the report itself is not in this worktree | none (lane); fleet PROTOCOL marker rule only | R4 | Resolvable work commit plus a before→after measurement; a marker is not a round |
| M2 | Dead hash citation plus operator attribution and report-before-commit | fleet MANIFEST index 21 (r13 closure): cited d7dbd9a UNRESOLVABLE in every local object database; report committed 19:44:22, 15 s before its own child commit 7483333. `git cat-file -e d7dbd9a` exits 128 here; 7483333 resolves | none | R4 | Every cited hash passes `git cat-file -e` at filing; the report commit is an ancestor or a named successor |
| M3 | Gate disagreement resolved with evidence: critic falsification rejected | `corpus/README.md:168`: "One critic falsification REJECTED with evidence (the 2026-09-05 severity decree exists at fleets/claimer-mission.md:29, critic grepped only docs/)"; that decree path is lost-tree, the lane record is the pointer | closest: `corpus/knowledge/citation-bases.md` rules 1/6 (anchor bases) | Q3, Q5 | A rejection names the exact location and the sweep that missed it; rejecting on absence requires the search command |
| M4 | Density bar deliberately not cleared: honest negative, no reflow gaming | `SCORECARD.md:65`: four repairs 131.4 / 111.5 / 117.4 / 93.0; BAR_R15 = 142.5 not cleared; form sensitivity 93.3 prose vs 150.0 table recorded | yes: `corpus/instruments/README.md` bar rule | none — pre-captured by the instruments/README.md bar rule | Held; the bar is frozen and conjunctive since round 16 |
| M5 | External shock mid-round: primary tree deleted while the round ran | `corpus/knowledge/source-tree-loss-2026-09-28.md`; `LOG.md:545` (§1 detection through §10 measurements) | none: base vocabulary marks lost trees, but no rule required an opening existence check | none — projected criterion was not minted | Residual uncaptured class; candidate for a later record criterion |
| M6 | Numerator transcription error: 480/1506 published, r18 re-derived 451/1506 | `SCORECARD.md:88-96`: r17 narrative 480/1506; r18 labrat 451/1506 = 107 RESOLVES + 224 MIRROR-EQUIVALENT + 120 INTERNAL | none | Q3 | Numbers are copied from the committed TSV, never retyped; re-derive once before publication |
| M7 | Instrument blind spots: resolver ingested its own census, stripped leading dots; broadened matcher found 82 hidden bad anchors | `LOG.md:709-713` (205 in-range / 82 bad; round 18 preserves leading dots) and `LOG.md:747-750` (resolver ingested its own generated census); `corpus/instruments/README.md:63`; fixture rule at `corpus/instruments/README.md:131` | yes: r18 corrections plus documented limits | R3 | A verdict names its matcher; keep one mutation fixture per instrument |
| M8 | Receipt citations re-anchored to git-untracked files; no durable blob pin claimed | `LOG.md:734`: "The source tree is mutable and all four receipt-store files are git-untracked", SHA-256 recorded, "No durable blob-pin is claimed." | yes: `corpus/knowledge/citation-bases.md` rule 2 (BLOB-PIN) | none — pre-captured by citation-bases rule 2 | Held; untracked-but-read bytes are current-byte evidence only |
| M9 | Second root loss: 202 bad anchors, scores held, BASE-ABSENT class invented | `SCORECARD.md:121-149`; `corpus/knowledge/root-loss-2026-10-12.md` | yes: derived roots plus BASE-ABSENT plus loss prefixes | none — pre-captured by citation-bases LOST-BASE and `corpus/instruments/anchorcheck.py` | Held; derived roots and an explicit loss class without a score move |
| M10 | Stale current-tense claims: 22 live lines still call absent roots "live" | `corpus/lessons/round-20-recensus.md:39`; `corpus/knowledge/submitted-registry.md:9` ("the live sibling tree") and `corpus/knowledge/submitted-registry.md:27` ("verified live") | none: citation-bases rules 1/3 cover anchors, not prose LIVE assertions | R1 | A sentence asserting a tree is live carries an as-of date and its `test -e` result; absent is marked historical |
| M11 | Self-description drift: stale rates, dead pointers, unread `$UFO_SRC`, unreproducible 50-deletion claim | `corpus/lessons/round-20-recensus.md:20` ($UFO_SRC), `corpus/lessons/round-20-recensus.md:29` (50 deletions), `corpus/lessons/round-20-recensus.md:33` (stale rates); audit detail at `corpus/lessons/round-20-recensus.md:43` | none | R2 | A rate cites its census file, a `$VARIABLE` cites the code that reads it, a deletion count cites the command |
| M12 | Blocked round: 32 scopes authored and rendered, 0 dispatched, no receipt fabricated | `SCORECARD.md:228-290`; `SCORECARD.md:251`: "ADMISSION_GATE: BLOCKED failed_requirements=11 verified_round_credit=0"; `.ufo/rounds/round-21/admission-gate.json` exit_code 1 with 10 ROUTE_BINDING BLOCKED plus 1 CONNECTOR_FALLBACK BLOCKED = 11; `SCORECARD.md:252`: 32 members, no task batch | none: external routing contract; the report records it | R4 | A rendered wave is not execution; blocked rounds report zero credit and their unblock action |
| M13 | Prior frozen assertion falsified: 32/506 replay becomes 33/506 live-FS and 31/506 Git-export | `SCORECARD.md:259-270`; `.ufo/rounds/round-21/frozen-skill-guard.json` and `.ufo/rounds/round-21/snapshot-skill-guard.json` preserve the failed 32/506 replays | none | R3 | "Frozen" names both byte inputs and the filesystem definition; replays publish every divergent definition |
| M14 | Ledger holes: no round-2 record; no lesson for rounds 16, 18, 19 | `corpus/README.md:145`; `corpus/lessons/` has 24 files and none for 2/16/18/19 | none: append-only discipline prevents rewriting, but no rule required a lesson per round | R5 | A round without a lesson is recorded as a named omission in the next lesson |
| M15 | Fleet conformance defects: SHONEN heading absent in reports r10-r14 and r17; operator-identity commits; report-before-commit | fleet MANIFEST indices 13 (r10), 14 (r11), 20 (r12 SHONEN=0), 21 (r13 SHONEN=0), 27 (r14 heading ABSENT), 64/72 (r17 SHONEN 0); operator identity and report timing in 20/21 | none | none — not minted; R4 covers only the work-commit item | Residual; the report-template check (SHONEN, work commit, hash resolution) is still absent |
| M16 | Contract omission: QUALITY bar never minted; provenance fields never written; Gate sections mostly absent | fleet contract CORPUS.md:12,17 and LEARNING.md:54-60 (outside this worktree); counts at base: 25 knowledge entries, 0 with all three headers; 24 lessons, 3 with a Gate section | none — this is the missing gate itself | Q1 (also Q2) | Create QUALITY.md thin; every criterion cites the lesson that produced it |
| A1 | Internal verdict strings used where a portal expected its own severity vocabulary and CVSS | `SKILL.md:590-596` | yes: `SKILL.md` anti-pattern 1 | none — no criterion cites it | Remains a SKILL example; no new rule |
| A2 | Severity language hedged below evidence and inflated beyond demonstrated impact | `SKILL.md:597-608` | yes: `SKILL.md` anti-pattern 2, 2026-09-05 decree | none — no criterion cites it | Remains a SKILL example; no new rule |
| A3 | Absolute "no live host was contacted" claim contradicted by the package's own GET/HEAD provenance | `SKILL.md:609-614` | yes: `SKILL.md` anti-pattern 3 | Q6 | Documentation-only rule; no absolute no-contact claim against recorded provenance |
| A4 | Internal orchestration artifacts attached where only triage-useful proof belonged; 17 attachments against a 3-file allowlist | `SKILL.md:615-621` | yes: `SKILL.md` anti-pattern 4 | none — no criterion cites it | Remains a SKILL example; no new rule |
| A5 | Historical `claim-ready` tags and stale generated metadata treated as current authority | `SKILL.md:622-635` | yes: `SKILL.md` anti-pattern 5 | Q2 | Current authority plus tier-A support; a historical tag never overrides current bytes |
| A6 | Empty `in_scope_assets` overclaimed as "no scope" | `SKILL.md:636-639` | yes: `SKILL.md` anti-pattern 6 | Q4 (L1 regrounded Q4 on A7 + A6 after the r22 critic found A9 is laundering, not attribution) | An observation stays attributed to what was observed; absence of evidence is not a scope claim |
| A7 | Claiming safe harbor the program does not grant | `SKILL.md:640-643` | yes: `SKILL.md` anti-pattern 7 | Q4 | Attribution: safe harbor is the program's grant, never generalized from another program |
| A8 | Manufactured findings | `SKILL.md:644-651` | yes: `SKILL.md` anti-pattern 8 and invariant I8 | Q5 | Falsifiable rule plus a rejected over-generalization; honest zero is a bounded result |
| A9 | Precondition laundering: a local PoC treated as proof of live impact | `SKILL.md:652-664` | yes: `SKILL.md` anti-pattern 9 | none — Q4 no longer cites it (r22 critic); held by the SKILL anti-pattern | Preconditions stay attributed; the package remains gated until the named check runs |
| A10 | Treating "DONE" as claimable | `SKILL.md:665-679` | yes: `SKILL.md` anti-pattern 10 and the runbook rule it cites | none — no criterion cites it | Remains a SKILL example; no new rule |
| M17 | Edit shifts line anchors: provenance headers inserted at line 2 of the 25 legacy entries moved every path:line anchor into them by +3 (SKILL.md:120,132,338,416,696,697,821; ~140 in `corpus/knowledge/triage-thresholds.md`) | L1 pre-commit anchorcheck: SKILL.md:821 `mission-control.md:3` printed the new verified-at line instead of the Source line | none — anchorcheck checks range, not meaning | R6 | Headers relocated to an appended end-of-file block before commit; every legacy file's original lines are prefix-identical to 94aace2 (count command in `SCORECARD.md` round-22 section) |

## Unlearned classes → criteria

Ten classes had no lane rule before round 22 and now have a `corpus/QUALITY.md` criterion (M17, found and fixed inside round 22, takes R6): M1 and M2 (R4), M6 (Q3), M10 (R1), M11 (R2), M12 (R4), M13 (R3), M14 (R5), M16 (Q1, also Q2). The other mined classes were already held by a lane rule before this round (M3, M4, M7, M8, M9) or were already captured by the SKILL anti-pattern section (A3, A5, A7, A8, A9); M5 and M15 had no rule and still have none, and are named here as residual.

Counting command (rows whose before cell starts with `none` and whose now cell starts with a criterion id):

```bash
awk -F'|' '/^\| (M|A)[0-9]+ \|/ {b=$5; n=$6; gsub(/^[ \t]+|[ \t]+$/,"",b); gsub(/^[ \t]+|[ \t]+$/,"",n); if (b ~ /^none/ && n ~ /^[QR][1-6]/) c++} END {print c+0}' corpus/lessons/round-22.md
```

Output: `10`.

## Omissions

Per R5, a round without a lesson is recorded as a named omission in the next lesson. The following round numbers have no lesson file and are not rewritten into history: **2, 16, 18, 19**. Round 2 is also the ledger hole recorded at `corpus/README.md:145`; rounds 16, 18 and 19 have no lesson despite work in the log. Round 21 does have a lesson (`corpus/lessons/round-21-routing-blocked.md`) but its attempt was blocked before dispatch and consumed the round number with zero verified credit (`SCORECARD.md:251`; `corpus/lessons/round-21-routing-blocked.md:115`), so it is recorded here as a consumed number, not as a missing lesson.

```bash
ls corpus/lessons/round-2.md corpus/lessons/round-16.md corpus/lessons/round-18.md corpus/lessons/round-19.md
```

All four paths are absent in this worktree.

## Gate agreements

- **Round 15 — critic and labrat agreed independently.** Both derived the compounding-ratchet argument against re-deriving the density bar from the current mean; both were adopted, and the bar became frozen and conjunctive from round 16 (`SCORECARD.md:49-58`).
- **Round 20 — independent audit agreed, then found more.** The audit agreed with all three instruments' counters and then found 22 dead-path lines the author had missed; the erratum is appended, not rewritten (`corpus/lessons/round-20-recensus.md:37-39`).
- **Round 21 — honest stop.** The admission gate blocked 10 role bindings and 1 missing connector fallback (11 failed requirements, exit 1), and receipt minting refused with `invalid_id` rather than manufacturing a receipt (`SCORECARD.md:251`; `.ufo/rounds/round-21/admission-gate.json`; `.ufo/rounds/round-21/receipt-mint-attempt.json`).

## Gate

Contract rule 1 record for every registry row written this round (`corpus/SOURCES.md`,
27 rows, all opened 2026-10-19 by the sources executor; the first executor seat died on
a provider rate limit before writing and was re-dispatched fresh):

| id | URL | accessed | quote (≤25 words, verbatim) | location |
|---|---|---|---|---|
| S001 | https://www.first.org/cvss/v4.0/user-guide | 2026-10-19 | “CVSS Base (CVSS-B) scores are designed to measure the severity of a vulnerability and should not be used alone to assess risk.” | CVSS Base Score (CVSS-B) Measures Severity, not Risk |
| S002 | https://www.first.org/cvss/v4.0/specification-document | 2026-10-19 | “The Threat Metrics adjust the severity of a vulnerability based on factors, such as the availability of proof-of-concept code or active exploitation.” | Introduction, metric-group descriptions |
| S003 | https://www.cisa.gov/resources-tools/resources/establishing-coordinated-vulnerability-disclosure-program-work-security-researchers | 2026-10-19 | “By implementing a robust CVD program aligned with this guidance, organizations can work transparently and collaboratively with security researchers” | Publication description, July 15, 2026; the entry's load-bearing quote is PDF p. 6: “A time frame may be a fixed period, a minimum or maximum, or a negotiated default starting point.” |
| S004 | https://certcc.github.io/certcc_disclosure_policy/ | 2026-10-19 | “We think that 45 days can be a pretty tough deadline for a large organization to meet.” | Frequently Asked Questions, “Why not 30 days, or 15 days, or immediately?” |
| S005 | https://projectzero.google/vulnerability-disclosure-faq.html | 2026-10-19 | “Our expectation is that the developer will fix the security vulnerability and make a patch available to users within 90 days.” | What is Project Zero’s 90-day disclosure deadline policy? |
| S006 | https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq | 2026-10-19 | “Adopting a Safe Harbor does not change the program scopes. Scope definitions remain based on what assets the program explicitly includes.” | What is safe harbor? |
| S007 | https://docs.bugcrowd.com/researchers/disclosure/disclose-io-and-safe-harbor/ | 2026-10-19 | “An exhaustive list of In-Scope properties that the organization is explicitly providing safe harbor for the good-faith security testing” | Disclose.io, Scope recommendation |
| S008 | https://www.cisa.gov/vulnerability-disclosure-policy-template | 2026-10-19 | “Any service not expressly listed above, such as any connected services, are excluded from this policy and are not authorized for testing.” | Vulnerability Disclosure Policy, Scope |
| S009 | https://www.ncsc.gov.uk/blogs/10-questions-ask-using-ai-models-find-vulnerabilities | 2026-10-19 | “You should also look for ways to verify the results, by using both AI and humans.” | Question 7, “Where should I start?” |
| S010 | https://projectzero.google/2024/06/project-naptime.html | 2026-10-19 | “potential solutions can be verified automatically with absolute certainty.” | Proposed Principles, Perfect Verification; 2024-06-20 |
| S011 | https://blog.cloudflare.com/cyber-frontier-models/ | 2026-10-19 | “a suspected flaw without a working proof is speculation, and Mythos Preview closes that gap on its own.” | The Signal-to-Noise Problem |
| S012 | https://www.anthropic.com/research/glasswing-initial-update | 2026-10-19 | “First, we or one of the external security firms we work with reproduce the issue that Mythos has found and re-assess its severity.” | Open-source software, triage process; May 22, 2026 |
| S013 | https://cwe.mitre.org/top25/archive/2025/2025_methodology.html | 2026-10-19 | “The 2025 CWE Top 25 was the first to also employ CWE mapping suggestions from an LLM tool developed by Chris Madden” | LLM Mapping Suggestions; page last updated 2026-01-23 |
| S014 | https://cwe.mitre.org/top25/archive/2025/2025_key_insights.html | 2026-10-19 | “Base and Variant level CWEs should be used whenever possible to ensure providing adequate specificity and actionability.” | Abstraction; page last updated 2025-12-10 |
| S015 | https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html | 2026-10-19 | “CVEs in KEV: 7 Rank Last Year: 1” | 2025 CWE Top 25 table, CWE-79 row; page last updated 2025-12-15 |
| S016 | https://www.anthropic.com/coordinated-vulnerability-disclosure | 2026-10-19 | “Reports originating from AI-powered discovery are clearly labeled as such.” | Vulnerability Disclosure Reporting and Coordination; last updated 2026-03-06 |
| S017 | https://projectzero.google/2025/07/reporting-transparency.html | 2026-10-19 | “no technical details, proof-of-concept code, or information that we believe would materially assist discovery will be released until the deadline.” | The Trial: Reporting Transparency; 2025-07-29 |
| S018 | https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1 | 2026-10-19 | “All parties should clearly and securely communicate and negotiate expectations and timelines.” | Guiding Concepts and Best Current Practices, Maintain clear and consistent communications; v1.1 |
| S019 | https://csrc.nist.gov/pubs/sp/800/216/final | 2026-10-19 | “Formalizing actions to accept, assess, and manage vulnerability disclosure reports can help reduce known security vulnerabilities.” | Abstract; SP 800-216 final, 2023-05-24 |
| S020 | https://www.justice.gov/criminal/criminal-ccips/page/file/983996/dl?inline= | 2026-10-19 | “Describe authorized and unauthorized conduct in plain, easily understood terms.” | Step 3, Draft a vulnerability disclosure policy; Version 1.0, July 2017 |
| S021 | https://www.cisa.gov/news-events/directives/bod-20-01-develop-and-publish-vulnerability-disclosure-policy | 2026-10-19 | “A vulnerability disclosure policy (VDP) is an essential element of an effective enterprise vulnerability management program” | BOD 20-01, Develop and Publish a Vulnerability Disclosure Policy; 2020-09-02 |
| S022 | https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.1.0.pdf | 2026-10-19 | “CNAs MUST develop, document, and operate within a Scope Definition” | Section 3.1, CNA Scope Definition; v4.1.0, effective 2025-05-14 |
| S023 | https://www.cisa.gov/resources-tools/programs/coordinated-vulnerability-disclosure-cvd-program | 2026-10-19 | “CISA’s Coordinated Vulnerability and Disclosure (CVD) team performs an initial triage” | The CVD Process, step 2 |
| S024 | https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng (HTML: OJ:L_202402847) | 2026-10-19 | “placed on the market with fewer vulnerabilities and that manufacturers take security seriously throughout a product’s lifecycle” | Opening recitals. L1 correction before commit: the executor's Article 14(2)(a) quote matched only a secondary mirror (post-reviewer); EUR-Lex Article 14 was not reachable, so row narrowed |
| S025 | https://arxiv.org/abs/2503.17332 | 2026-10-19 | “Our evaluation shows that the state-of-the-art agent framework can resolve up to 13% of vulnerabilities.” | Abstract; published 2025-03-21 |
| S026 | https://www.cisa.gov/resources-tools/resources/gold-eagle-advancing-ai-driven-vulnerability-reporting | 2026-10-19 | “Gold Eagle lets organizations report, validate, and track AI-related vulnerabilities at scale.” | How Gold Eagle Works; source page opened 2026-10-19 |
| S027 | https://news.ycombinator.com/item?id=38389728 | 2026-10-19 | “Bug Bounties Tips from the Triager” | HN submission title; posted 2023-11-23 |

**Census (SOURCES contract v1, all seven commands, run 2026-10-19 from the lane root; the last three piped to `wc -l`):**

```text
rows: 27
malformed (must be 0): 0
tier histogram: A=25 C=2
status histogram: mined=15 queued=10 rejected=2
duplicate ids (must be 0): 0
enum/tier-inflation lines (must be 0): 0
mined used-by paths missing (must be 0): 0
```

**L1 independent re-open (2026-10-19).** L1 fetched S001–S015 (plus the S003 PDF) itself
and string-matched: 13/13 sampled gate quotes above (S002, S004–S015) are verbatim
(S007 differs only by markdown italics); all 85 quoted strings in the five new entries
occur verbatim in their sources (74 against the S-id on the line, 11 section-heading
names against the sibling S-id on the same line). The r22 critic independently re-opened
S001, S003 (page + PDF), S006, S009, S012 and S013: every quote exact, S012's four counts
and S013's 39,080 records match.

**Admitted (5) — Q1–Q6 all pass** (executor self-check, reviewer re-check):
`corpus/knowledge/cvss-v4-severity-and-vector.md`, `corpus/knowledge/coordinated-disclosure-timelines.md`,
`corpus/knowledge/authorization-safe-harbor-and-scope.md`, `corpus/knowledge/ai-assisted-finding-validation.md`,
`corpus/knowledge/cwe-top25-2025-methodology.md`. Reviewer found one Q3 defect before
commit (B5: the CWE entry put a paraphrase inside quotation marks) — repaired to the
exact S013 sentence; and two anchor mismatches (B4: S003 anchor omitted PDF p. 6, S013
anchor omitted "Removal of CWE Mapping Normalization") — repaired before commit.

**Rejected.** Sources: S026 (CISA Gold Eagle — no checkable validation protocol) and S027
(HN link without accessible text), each with a flip. Knowledge claims rejected as
over-generalizations, each kept in its entry's `## Rejected`: CVSS-B as a complete
risk/payout decision; one universal disclosure deadline; a safe-harbor badge as blanket
authorization; model output as a confirmed vulnerability; Top 25 rank as target risk.

**Gate disagreements, adjudicated with evidence.**
- Critic: C1 "full provenance closure" is falsified for lost bases → accepted. C1 is
  re-stated as provenance *disclosure*: headers name the lost base, and `recheck:` is a
  fail-closed command (23/25 exit 1 today, 2/25 exit 0; repo-git-state's first recheck passed vacuously — 0 cites — and was rewritten to fail closed on the bounties .git, post-reviewer); no lost claim is presented as
  re-verified and the resolver fraction is not credited.
- Critic: Q4 cited A9 (precondition laundering), which is not an attribution failure →
  accepted; Q4 re-grounded on A7 + A6 before commit (rows A6/A9 above updated).
- Critic: hold coverage at 7 vs planner: 7→8 under a new denominator → critic accepted;
  redefining the denominator in the round that benefits from it is self-serving. The
  planner's denominator is recorded in `SCORECARD.md` for adoption next round.
- Reviewer B1: `recheck: none …` is not runnable → accepted; all 22 rewritten as
  on-restoration — test -d (root) … && python3 corpus/instruments/anchorcheck.py (file).
- Reviewer B2: numstat shows 22 deletions in six legacy files → rejected with evidence:
  every deleted line reappears as the exact prefix of its replacement (16 hunks, 0
  non-prefix; check in `LOG.md` round-22 entry) — same-line appended markers, no text lost.
- Reviewer M6: `SCORECARD.md:65` is the wrong pointer for M4 → rejected:
  `grep -n '131.4' SCORECARD.md` → line 65.
