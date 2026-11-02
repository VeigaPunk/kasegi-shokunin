# CNA causal grouping for a fictional CVE request package
source: S110 — https://raw.githubusercontent.com/CVEProject/cve-documents/995b251a8975e95407802d742c9f0df6db5735de/CNA_Rules.md — v4.2.1 sections4.1,4.2,4.4; capture lines337–419
verified-at: 2026-11-02
recheck: cd /workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-63/manifest.json --source S110

## What the worksheet decides
This is a documentation-only request-package aid under the CVE Program's rules,
not authority to assign IDs, test a target, submit a report, contact a CNA or
establish bounty eligibility. It deepens F07; causal evidence matters before
arithmetic. Exact source model is4.2.1, approved2026-10-14/effective2026-10-20.
The source itself expects CNA judgment(section4.4); recommendations are not mandates.

## Evidence and decision table

| Mechanism/evidence | Hypothetical grouping | Source evidence |
|---|---|---|
| Two independently security-impacting defects can be repaired separately | Distinct vulnerability groups; not one just because a common patch repairs both |4.2.11,line403: “CNAs MUST assign different CVE IDs” |
| Conditions are fully interdependent rather than two independent vulnerabilities | One group, even if the chain has two weakness labels |4.2.15,line419: “fully interdependent with another Vulnerability” |
| Independence cannot be established | Say unknown basis, with single-ID recommendation, not factual proof of identity |4.2.12,line405: “the CNA SHOULD assign a single CVE ID.” |
| Products contain the same vulnerable code | Do not multiply an ID for the same vulnerability by downstream package count |4.2.13.1,line409: “share the vulnerable code.” |
| Products implement the same issue without shared vulnerable code, or sharing is uncertain | Different IDs recommended; do not import independent-fix uncertainty's opposite default |4.2.13.2–3,lines410–411: “SHOULD assign different CVE IDs” |
| Vulnerable use of another product's functionality/specification has a secure usage option | One ID per known vulnerable implementation required, not one per abstract specification |4.2.14.1,line415: “there is a secure way” |
| No secure way exists | Single ID required; not merely because the dossier omitted alternatives |4.2.14.2,line416: “no option” |
| Secure-use possibility uncertain | Separate known vulnerable implementations recommended |4.2.14.3,line417: “uncertain whether there is a secure way.” |
| Incomplete fix leaves residual insecurity | Explain permissible existing/new-ID choices, not a forced novel-ID claim |4.2.8,line397: “MAY use an existing CVE ID.” |

These short excerpts identify rules, not substitutes for reading their complete
sentences in S110. Grouping does not remove assignment prerequisites:4.2.2.1
requires reasonable evidence, expected/already public disclosure and scope in its
SHOULD rule;4.2.5 forbids assignment without intention/expectation of disclosure
unless already public. No technical count gives this assistant a CNA's authority.

## A useful counterfactual, not a patch-count heuristic
Suppose one release repairs two demonstrated independent authorization defects in
unrelated handlers. A documented local correction to A leaves B's unauthorized
access intact, and correcting B leaves A's unauthorized access intact. The shared
release is not evidence of shared cause;4.2.11 supports two hypothetical groups.
Contrast a length-calculation defect whose resulting undersized allocation alone
causes the described write: when the latter has no independent security-impacting
path and is fully interdependent,4.1.10/4.2.15 support one. A workaround blocking a
common entry point proves neither identity nor independent fixability by itself.
Ask which harmful behavior survives a causal correction—not how many diff files,
CWE labels, commits, vendors or reporter messages exist.

## Checklist and falsifiers
1. List demonstrated security impacts and component/product subjects; identify
   omissions instead of assuming every anomaly is a vulnerability(4.1.2).
2. Draw defect→condition→impact dependencies. Record independent harmful behavior
   and effects of each described correction, distinguishing mitigation from fix.
3. Determine whether multi-product observations share vulnerable code or merely
   behavior; then check functionality/specification rules if applicable.
4. Name the exact uncertainty. The three defaults above are intentionally not
   interchangeable. Separate conditional group count from confirmed fact.
5. Explain incomplete-fix discretion and existing identifier relationships;
   dependency upgrades themselves are not new vulnerabilities(4.1.11).
6. State normative force, publication/scope assumptions, rejected alternatives and
   the discriminating fact needed. Refer unusual judgment to an authorized CNA;
   this document initiates no such contact.

Rejected generalization: one patch means one vulnerability. Counterexample above
has two independent defects and one patch;4.2.7 counts vulnerabilities, not fixes.
Rejected: every unknown merges.4.2.13.3 and4.2.14.3 recommend separation under their
specific premises. Rejected: every incomplete fix mandates a new ID;4.2.8 is MAY.

## Limits and demonstration custody
Manual synthetic assessments, not a classifier or real-world accuracy estimate.
Frozen rubric and first-answer custody: .ufo/waves/round-63/CONTRACT.md. Captured
source comparison proves bytes/quotes, not continued online freshness. A source
model does not replace an authorized CNA's contextual judgment or resolve disputes.

## Round63 source-authority qualification
“Current” above means the official repository's final-labelled model reopened in
this round and pinned at995b251a, not independent verification that this is the
currently effective published release. Approved/effective dates are the document's
self-declared header. A higher number in a historical parent or a mutable master
ref is not temporal authority. Website readers did not supply independently opened
published-release evidence. This dossier deliberately assesses the frozen4.2.1
repository model; it does not adjudicate S031's old PDF provenance or prove that
historical4.2.6 never existed. Consult the actual applicable release before any
real CNA work; this training performs no such work.
