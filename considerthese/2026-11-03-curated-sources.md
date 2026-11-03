# Curated sources to consider — kasegi — 2026-11-03

**Status: unassimilated future reading after hyaku.** This is a separate source-candidate note, not a training round, source admission, readiness claim or instruction to change the current plan. Existing dated reflections remain unchanged.

Public primary sources were read on **2026-11-03 (UTC)**. No candidate code was installed or executed, no live target was tested, and no analyzed artifact was uploaded. All commentary below is original; source material is linked rather than copied.

## 1. CERT Guide to Coordinated Vulnerability Disclosure
- **Type and source:** Methodology — [primary source](https://certcc.github.io/CERT-Guide-to-CVD/)
- **Version / maintenance:** Evolving web edition of CMU/SEI-2017-SR-022; no immutable revision established. Official site and source repository opened 2026-11-03; repository describes the web edition as the maintained version, but no recent commit date was established. [Evidence](https://github.com/CERTCC/CERT-Guide-to-CVD)
- **Why it fits:** A primary coordination handbook for separating finder, vendor, coordinator and deployer responsibilities across a disclosure. Useful for documenting who needs which evidence and when a claim package is ready for its authorized channel.
- **Reading and proposed later use:** Start with the quick-start and role/process sections. After hyaku, consider a paper-only mapping from an existing authorized report package to stakeholder, evidence, unresolved question and communication owner.
- **Limits:** A general guide does not grant testing or disclosure authority. Its copyright notice distinguishes internal derivatives from external reproduction and requires permission for other external/commercial uses; retain only original commentary and links here.
- **License:** CMU/SEI custom copyright terms; not a blanket open-source license. [License evidence](https://raw.githubusercontent.com/CERTCC/CERT-Guide-to-CVD/main/COPYRIGHT.md)
- **Duplicate check:** New guide, but same CERT/CC source family as existing SSVC and disclosure-policy sources. Adds coordination process and role coverage, not another severity model or a replacement program policy.

## 2. GitHub Advisory Database
- **Type and source:** Maintained data repository — [primary source](https://github.com/github/advisory-database)
- **Version / maintenance:** Default-branch dataset; pin a commit before later sampling. Official commit-history view showed repeated publication/sync commits dated 2026-09-11. This supports maintenance, not a claim to have captured the current November head. [Evidence](https://github.com/github/advisory-database/commits/main/)
- **Why it fits:** A practical collection of OSV-format advisory records with package-specific affected ranges, references and curation history. It can support static claim-package review: distinguish a package/version assertion from a project-wide allegation and retain the original advisory provenance.
- **Reading and proposed later use:** Read README sections on sources, references and fix commits. After hyaku, propose a small frozen record sample and compare its package/range/fix-reference fields with the lane’s existing claim-package checklist.
- **Limits:** Advisory presence is not evidence that an artifact is affected or exploitable. Reviewed, unreviewed and malware records need separate handling. Attribute reused data; do not submit changes or contact maintainers as part of this reading.
- **License:** CC-BY-4.0. [License evidence](https://raw.githubusercontent.com/github/advisory-database/main/LICENSE.md)
- **Duplicate check:** New repository family. Existing GHSA examples, GitHub reporting documentation and OSV schema overlap conceptually; the added surface is the versionable dataset and its curation rules.

## Admission boundary

Re-check the exact version, relevant sections and licensing before later use. Any adoption needs the lane’s normal independent review and evidence gates after hyaku. This file changes no corpus registry, skill, scorecard, training input, authorization or deployment state.
