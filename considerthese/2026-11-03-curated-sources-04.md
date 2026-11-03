# Consider these: report state is not remediation

**Status: unassimilated reading after hyaku.** Checked 2026-11-03 UTC. This is a source candidate, not a training round or an accepted vulnerability finding.

## SARIF: suppression versus baseline comparison

**Original summary.** SARIF distinguishes suppression decisions from comparison with an earlier analysis run. An empty suppression array means available information and no suppression; missing or null information still receives an unsuppressed consumer treatment, but does not establish that a reviewer considered it. The baseline value `absent` records non-detection in the current run. Neither that value nor accepted suppression proves remediation or lack of exploitability.

**Exact source.** [SARIF 2.1.0 Plus Errata 01](https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/sarif-v2.1.0-errata01-os-complete.html), OASIS Standard incorporating Approved Errata, dated **28 August 2023**. This fixed edition is the reading pin; no claim is made that it describes every platform's current import behavior.

**Reading path.** Read §3.14.5 (`baselineGuid`), [§3.27.23 suppressions](https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/sarif-v2.1.0-errata01-os-complete.html#_Toc141790911), [§3.27.24 baselineState](https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/sarif-v2.1.0-errata01-os-complete.html#_Toc141790912), then [§3.35.3 status](https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/sarif-v2.1.0-errata01-os-complete.html#_Toc141790986). Keep the comparison reference and the suppression decision in separate columns.

**Future question.** After hyaku, consider a paper-only review of one already authorized report export. Which claims concern a detector's observations, which concern a review decision, and which still need independent evidence? Could a dashboard's apparently clean result hide unavailable suppression information or a changed comparison baseline? Leave missing provenance unresolved. Do not create an upload, submission, issue or external disclosure from this exercise.

**Limits and rights.** This interchange format does not grant testing authority or define bounty acceptance. The linked document's Notices provide custom OASIS copyright terms; its RF-on-RAND patent-policy mode is separate. Review those notices before reproducing specification material. Only original commentary is provided here.

**Novelty.** SARIF adds analysis-result state semantics beside existing advisory, CVE/OSV and claim-handling sources. No SARIF source-family alias was present in the reviewed inventories and earlier notes.
