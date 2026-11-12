# Kasegi: claim identity and delegated trust

Three reading paths for stronger security claim packages: binding an attestation to exact artifact bytes, deciding what a delegated verification result actually attests, and matching static-analysis findings across tool versions. Exercises are unperformed proposals using original local records. No live-target testing, disclosure, submission, training, or assimilation is part of this batch.

## Progression from a plausible report to a bounded claim

The first question is whether a statement refers to the artifact being discussed. The second is whether the signer is trusted for the policy and decision claimed. The third is whether two scanner observations represent the same finding. These are separate identity problems. A signed statement can bind the wrong artifact; a valid signature can come from an untrusted builder; and two scanner records can share a line number without being the same defect.

The live registry and nine existing considerthese files were inspected on 2026-11-12, together with a bounded comparison against 383 distinct accessible curation artifacts. Existing SARIF material already distinguishes suppression and non-detection from remediation, so that lesson is not repeated here. The new SARIF focus is versioned partial-fingerprint comparability. No in-toto or SLSA verification-summary entry was found in that curation screen; the registry search likewise found no SLSA or in-toto source. This is scoped novelty evidence, not an exhaustive claim about all historical work.

## 1. Artifact identity and builder trust are different checks

**Primary sources.** The in-toto project's [Statement v1](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md), especially subject and predicateType; and the SLSA Working Group's [Build: Verifying artifacts, v1.2](https://slsa.dev/spec/v1.2/verifying-artifacts), “How to verify,” “Check SLSA Build level,” and “Check expectations.” The initially discovered SLSA v1.1 page is marked retired and is not the selected guidance.

**Evidence and transition.** in-toto matches subjects by digest, not by a reassuring filename or content-type label. The predicate type identifies how the statement body should be interpreted. SLSA verification adds signature checks, configured trust in builder identities, and expectations about the build. These steps answer different questions. A valid digest association does not establish trusted production, and trusted provenance does not establish that the artifact has no vulnerabilities. The selected SLSA guidance also keeps compromise of the build platform itself outside the protection assumed from trusting that platform.

**Bounded exercise, unperformed.** Author two harmless text artifacts, A and B, and a local set of five statement-like records: a correctly bound record, one renamed subject with the same digest, one familiar filename with B's digest, one wrong predicate type, and one unrecognized builder. Write a verifier decision table before opening any records. If a signature-verification implementation is already available, use only a disposable locally generated fixture key; never use account credentials or production signing material. Otherwise report signature verification as not performed rather than treating a placeholder as a valid signature.

**Controls.** Separate digest match, supported predicate type, cryptographic validity, recognized signer, authorized builder, and expected build parameters. Do not make one aggregate PASS cell hide which checks were absent. The renamed matching artifact and the same-name wrong artifact should lead to different identity judgments. Whether the resulting build is secure remains outside this toy verification.

**Report and iteration.** Retain the source and artifact hashes, statement bytes, selected algorithm, configured trust mapping, and check-by-check outcome. Provide a short claim that the evidence permits and a stronger claim it does not. The next iteration may vary one build expectation only after the reviewer can explain why names and signatures cannot replace digest and trust checks.

## 2. A verification summary delegates a specific policy decision

**Primary source.** The SLSA Working Group's [Verification Summary Attestation, v1.2](https://slsa.dev/spec/v1.2/verification_summary), “Purpose,” “Fields,” “How to verify,” and “Change history.” The selected document marks this predicate approved. Its predicate URI is https://slsa.dev/verification_summary/v1, not a string inferred from the page's versioned URL.

**Evidence and transition.** A VSA communicates that a verifier evaluated an artifact and an attestation bundle under a policy. The consumer still checks signature/trust, subject digest, predicate type, verifier binding, and suitability for its own goals. The selected schema includes policy, result, verified levels, and optional additional context. It recommends a digest for the policy resource; a policy URL alone can change over time. A VSA allows delegation without requiring every consumer to possess the full evidence bundle, but that convenience makes the verifier and policy boundary more important, not less.

**Bounded exercise, unperformed.** Create six fictional VSA cases for one original artifact: an intended trusted verifier and policy, a validly represented but untrusted verifier, a mismatched subject, an unexpected policy digest, a failed verification result, and a missing optional time field. Use local data only. Write two consumer policies with different allowed verifier/policy pairs and show the proposed decision procedure for each. Missing optional data must not be called malformed merely because one local consumer would prefer it.

**Controls.** Distinguish format validity from consumer acceptance. A fresh timestamp must not rescue the wrong artifact or an untrusted policy. Conversely, a consumer's freshness requirement is a local decision rule and should not be attributed to the schema as universally mandatory. Keep the SLSA specification version separate from the predicate's major-version URI.

**Report and iteration.** Record exactly which entity is trusted, for which policy digest, artifact, level, and time rule. If some evidence is unavailable because verification is delegated, say which assurance relies on the verifier instead of claiming to have replayed it. A useful follow-up tests one change in trust or policy while leaving artifact bytes fixed. Stop if the only improvement is adding more visually impressive metadata without changing an actual decision.

## 3. Versioned fingerprints make finding comparisons inspectable

**Primary source.** OASIS [SARIF 2.1.0 plus Errata 01](https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/sarif-v2.1.0-errata01-os-complete.html), dated 28 August 2023, sections 3.27.16–3.27.17 and Appendix B. The current-version landing document was read; the fixed approved-edition link identifies the intended reference.

**Evidence and transition.** Partial fingerprints contribute to result identity and use versioned hierarchical property names. For comparison, the specification recommends the latest version available in both results. A tool upgrade can therefore affect whether evidence is comparable, independently of code movement. Matching by line number or choosing each record's newest version independently can produce an unjustified association. This extends the earlier suppression/baseline lesson rather than reinterpreting an absent result as a fix.

**Bounded exercise, unperformed.** Author two small SARIF runs for a fictional detector. Give one pair partial-fingerprint versions 1 and 2 versus 2 and 3, a second pair no common version, and a third pair the same location but different rule context. Use explicit artificial values and mark them as synthetic. Design a matching worksheet that records the common version, supporting attributes, and unresolved cases before computing any counts.

**Controls.** A no-common-version pair must not silently match by comparing unrelated strings. This does not require every consumer to reject it: a documented alternate matching method can be assessed separately. Likewise, do not claim that a matching hash alone proves two real vulnerabilities identical. Keep scanner identity and configuration available to the reviewer.

**Report and iteration.** The deliverable is a transparent cross-run association table, including unmatched and ambiguous cases, plus a proposed change in matching policy. Hold any trend or remediation claim until the identity assumptions and scan coverage are supplied. Add one adversarially chosen held-out pair on the next iteration; do not tune the matcher and score it on that same pair while calling it independent validation.

## Boundaries for every proposed exercise

Use at most eight tiny synthetic cases per family, 10 MiB retained data, and ten minutes of local processing. There is no target exploitation, online verification service, credential use, package publication, or submission to a bounty program. Program scope and testing authorization remain separate requirements even when a security claim package is technically well formed.

The report must retain the initial hypothesis, exact source edition, first outputs, failed and blocked checks, and the smallest resulting revision. Mark every statement as observed, inferred, predicted, or unknown. Independent review should challenge at least one overstrong claim and one excluded case. Stop a family when two revisions add neither a stronger control nor a narrower supported conclusion.

## Rights and attribution

in-toto's [attestation specification license](https://github.com/in-toto/attestation/blob/main/LICENSE) is Apache 2.0. The SLSA Working Group's materials are governed by the [Community Specification License 1.0](https://github.com/slsa-framework/slsa/blob/main/LICENSE.md), not a blanket assumption of Apache licensing. Attribution here identifies SLSA, version 1.2, the two material names, and their source URLs; the following disclaimer preserves the required distribution condition. No third-party implementation code or example payload is copied.

These materials are provided “as is.” Contributors and licensees disclaim express and implied warranties, including merchantability, non-infringement, fitness for a particular purpose, and title. The implementer and user assume the risk of using the materials. Contributors and licensees are not liable for lost profits or indirect, special, incidental, or consequential damages, whether arising in contract, tort, or otherwise, even if advised of the possibility.

OASIS provides its own copying/commentary conditions and patent-policy notices. The notice appendix below is retained for this commentary. It does not assert that this note is an official OASIS work, that an implementation is conformant, or that any patent rights have been cleared.

Destination: VeigaPunk/kasegi-shokunin, master, considerthese/2026-11-12-claim-identity-and-trust.md.

## OASIS notice appendix

The applicable copyright and notice text from the selected specification follows.

Copyright © OASIS Open 2023. All Rights Reserved.

All capitalized terms in the following text have the meanings assigned to them in the OASIS Intellectual Property Rights Policy (the "OASIS IPR Policy"). The full Policy may be found at the OASIS website: [https://www.oasis-open.org/policies-guidelines/ipr/].

This document and translations of it may be copied and furnished to others, and derivative works that comment on or otherwise explain it or assist in its implementation may be prepared, copied, published, and distributed, in whole or in part, without restriction of any kind, provided that the above copyright notice and this section are included on all such copies and derivative works. However, this document itself may not be modified in any way, including by removing the copyright notice or references to OASIS, except as needed for the purpose of developing any document or deliverable produced by an OASIS Technical Committee (in which case the rules applicable to copyrights, as set forth in the OASIS IPR Policy, must be followed) or as required to translate it into languages other than English.

The limited permissions granted above are perpetual and will not be revoked by OASIS or its successors or assigns.

This document and the information contained herein is provided on an "AS IS" basis and OASIS DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTY THAT THE USE OF THE INFORMATION HEREIN WILL NOT INFRINGE ANY OWNERSHIP RIGHTS OR ANY IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. OASIS AND ITS MEMBERS WILL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF ANY USE OF THIS DOCUMENT OR ANY PART THEREOF.

As stated in the OASIS IPR Policy, the following three paragraphs in brackets apply to OASIS Standards Final Deliverable documents (Committee Specifications, OASIS Standards, or Approved Errata).

[OASIS requests that any OASIS Party or any other party that believes it has patent claims that would necessarily be infringed by implementations of this OASIS Standards Final Deliverable, to notify OASIS TC Administrator and provide an indication of its willingness to grant patent licenses to such patent claims in a manner consistent with the IPR Mode of the OASIS Technical Committee that produced this deliverable.]

[OASIS invites any party to contact the OASIS TC Administrator if it is aware of a claim of ownership of any patent claims that would necessarily be infringed by implementations of this OASIS Standards Final Deliverable by a patent holder that is not willing to provide a license to such patent claims in a manner consistent with the IPR Mode of the OASIS Technical Committee that produced this OASIS Standards Final Deliverable. OASIS may include such claims on its website, but disclaims any obligation to do so.]

[OASIS takes no position regarding the validity or scope of any intellectual property or other rights that might be claimed to pertain to the implementation or use of the technology described in this OASIS Standards Final Deliverable or the extent to which any license under such rights might or might not be available; neither does it represent that it has made any effort to identify any such rights. Information on OASIS' procedures with respect to rights in any document or deliverable produced by an OASIS Technical Committee can be found on the OASIS website. Copies of claims of rights made available for publication and any assurances of licenses to be made available, or the result of an attempt made to obtain a general license or permission for the use of such proprietary rights by implementers or users of this OASIS Standards Final Deliverable, can be obtained from the OASIS TC Administrator. OASIS makes no representation that any information or list of intellectual property rights will at any time be complete, or that any claims in such list are, in fact, Essential Claims.]

The name "OASIS" is a trademark of OASIS, the owner and developer of this document, and should be used only to refer to the organization and its official outputs. OASIS welcomes reference to, and implementation and use of, documents, while reserving the right to enforce its marks against misleading uses. Please see https://www.oasis-open.org/policies-guidelines/trademark/ for above guidance.
