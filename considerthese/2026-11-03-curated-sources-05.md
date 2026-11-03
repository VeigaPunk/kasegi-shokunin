# Consider these: versioned severity evidence across CVSS generations

**Status: unassimilated reading after hyaku, subject to João's later manual instruction.** Primary sources checked 2026-11-03 UTC. This concerns report interpretation and compatibility, not testing targets or promising bounty eligibility.

## Timeline and primary sources

- **2019:** [CVSS 3.1 specification](https://www.first.org/cvss/v3.1/specification-document), especially Attack Complexity and Scope. FIRST's [12 July 2019 announcement](https://www.first.org/newsroom/releases/20190712) establishes availability by that date; it is not asserted to be the original release day.
- **1 November 2023:** FIRST [announced CVSS 4.0 publication](https://www.first.org/newsroom/news/cvss/2023). The [4.0 user guide](https://www.first.org/cvss/v4.0/user-guide), “Changes in CVSS Version 4.0,” separates defensive complexity from prerequisite attack conditions and distinguishes vulnerable-system from subsequent-system impacts.
- **29 January 2026:** the [official FAQ](https://www.first.org/cvss/v4.0/faq), history entry v1.6, added guidance on deriving 3.1 vectors from 4.0. The page currently identifies document revision 1.10, dated 17 July 2026. These are versioned official pages, not immutable byte snapshots; recheck revision histories before later use.

## What changes in the working method

The older vector remains necessary to interpret an older assessment on its own terms. A later vector carries different distinctions; numeric score differences alone cannot establish that the underlying vulnerability changed. The new FAQ's reverse-conversion guidance is especially useful: impacts must represent the chosen vulnerable or subsequent component, not a synthetic combination assembled from both. Read that section alongside the earlier Scope definition instead of treating migration as renaming fields.

**Earlier method still useful:** a program may explicitly request 3.1, or a historical report may need reproducible interpretation. Preserve its original version and vector; any derived representation should be separately labeled. That is a proposed documentation discipline, not evidence that all programs accept converted scores. Technical severity remains different from authorization, reward policy and remediation priority.

## Future comparison question

After hyaku, consider a paper-only claim worksheet with one already authorized finding description. Which impact statements support each component, which evidence is missing, and which distinctions disappear in a derived older vector? Would two reviewers disagree because they selected different systems, different versions, or different facts? Leave unknowns explicit and consult the particular program before proposing a new report format.

## Novelty and rights

The 4.0 specification/user guide are disclosed existing baselines. The 3.1 source and 2026 reverse-conversion FAQ add a focused compatibility history. CVSS is owned by FIRST and freely usable subject to attribution and publication conditions, including score plus vector. No score, conversion script, submission, source capture or implementation is published here. No universal best-method claim or corpus assimilation.
