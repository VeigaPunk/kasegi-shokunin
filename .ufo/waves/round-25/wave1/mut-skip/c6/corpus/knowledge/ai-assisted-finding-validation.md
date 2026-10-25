# AI-Assisted Finding Validation
source: S009 — https://www.ncsc.gov.uk/blogs/10-questions-ask-using-ai-models-find-vulnerabilities — question 7, “Where should I start?”
verified-at: 2026-10-19
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py --selftest

## Rule
Treat an AI-originated finding as a candidate, not a confirmed vulnerability, until its evidence package records a reproducible observation and human validation of the claimed impact and reachability.
For Kasegi claim-ready status, the package must identify the reproducing evidence and a reviewer distinct from its producer; a model assertion or benchmark result alone does not satisfy that check.
A reviewer can inspect the report and evidence manifest for the reproduction, impact path, and distinct review record; if one is absent, keep the finding unconfirmed.
Validation record checks:
- identify the code or package version to which the finding applies;
- separate model-generated hypotheses from observed reproduction results;
- connect the claimed impact to a supported reachability explanation;
- record the reproducing evidence and its independent review;
- identify a reviewer distinct from the finding producer;
- preserve any applicable program restriction or disclosure requirement.
If those facts are absent, preserve candidate status rather than describing the finding as confirmed.
These are Kasegi admission controls, not a claim that every cited source mandates one tool or workflow.

## Evidence
- S009, question 7, “Where should I start?”: “look for ways to verify the results, by using both AI and humans.”
- S010, “Proposed Principles” > “Perfect Verification”: “vulnerability discovery tasks can be structured so that potential solutions can be verified automatically with absolute certainty.” This describes structured tasks, not every real-world finding.
- S010, “Conclusions”: “there's a large difference between solving isolated CTF-style challenges without ambiguity” and autonomous security research; the article limits its benchmark conclusions.
- S011, “Our vulnerability discovery harness” > Validate stage: “An independent agent re-reads the code and tries to disprove the original finding.” Cloudflare describes its own process.
- S012, “Open-source software”: “First, we or one of the external security firms we work with reproduce the issue that Mythos has found and re-assess its severity.” Anthropic reports this as its own triage process.
- S012, same section: “the bottleneck in fixing bugs like these is the human capacity to triage, report, and design and deploy patches for them.” This is Anthropic’s report about its observed program.

## Kasegi use
Use SKILL.md’s “Evidence-package anatomy”: the report ties impact to evidence and the review record names a reviewer distinct from the producer.
Use “Program-rule checklist (step 1 of any mission)” for program-specific restrictions; that section records one observed rejection of AI-generated reports, not a universal ban.
Use “Disclosure anti-patterns (all observed in fleet wrap review)” to keep severity language within demonstrated impact.

## Rejected
Rejected: “A model-generated report or a high benchmark score is proof that a vulnerability exists in a particular package.”
A benchmark is bounded to its task design; NCSC recommends verification, and the Cloudflare and Anthropic descriptions report validation stages before treating findings as confirmed.

## Limits
S009 is operational guidance, not authorization to examine any system or codebase.
S010 reports Project Zero’s design and benchmark results; its controlled tasks do not establish field performance on arbitrary software.
S011 and S012 are first-party descriptions of Cloudflare’s and Anthropic’s own work, not independently audited general model-performance rates.
Neither vendor’s reported counts nor its workflow proves that another report is valid; preserve attribution and the limits of each source.
This entry describes review of documentation and evidence packages only; it does not direct probing, scanning, or submission.

Round-23 recheck clarification: the command checks exact quoted support in pinned
captured-source excerpts, not current online freshness, a complete entry audit,
or an independent audit of the publishers' methods and reported performance.
