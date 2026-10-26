# ExecC2Capture — S054 primary-source capture (round 37)

Seat: ExecC2Capture (leaf executor, no subagent dispatch used).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only lane repo; no writes outside my receipt).
Base commit `b56a41680cefd391868c1c370dc063c69d827e7d`; claims-freeze commit
`224df74db2a46d627ae1475a72ca48796bbd177c`; lane HEAD observed while working: `b362068195d5489aa94b31e6ec8f880c367e0ba0`.
Claim served: C2 coverage, frontier F20 (SSVC — Stakeholder-Specific Vulnerability Categorization, CERT/CC/Carnegie Mellon), capture leg only.

Deliverables (to be landed byte-identically by the L1):
- `corpus/source-snapshots/round-37/S054.txt` — 32623 bytes, 518 lines, sha256 `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21`
- `corpus/source-snapshots/round-37/manifest.json` — the manifest below, byte-exact
- Registry row `S054` must carry exactly one `https://` token and it must be the corrected URL below (binding rule B5 of `capture-binding-check.py`).

## 0. Claims erratum 1 (URL correction) — applied

The L1 filed claims erratum 1 (commit `b3620681`) while I was working: the C2 S054 capture URL is
corrected from `https://certcc.github.io/SSVC/` (docs home) to
`https://certcc.github.io/SSVC/tutorials/ssvc_overview/` ("What is SSVC?" overview tutorial), because
the home page lacks the decision-point methodology text the knowledge entry must quote.

I checked the reason against my own fetches rather than taking it on trust: the home page's normalized
body (286 lines) carries only the acronym expansion (`SSVC stands for A Stakeholder-Specific Vulnerability
Categorization.`), one methodology sentence (`It is a methodology for prioritizing vulnerabilities based on
the needs of the stakeholders involved in the vulnerability management process.`) and a documentation
navigation list — it has no decision-point, decision-outcome, "how decision models are designed" or per-role
prioritization-category prose (navigation labels such as `Decision Points` and `Outcomes` are its only
matches for those words), and `prioritizing actions` appears nowhere; the word "framework" occurs nowhere in
its normalized text and only in the raw HTML's unrendered
`<meta name="description" content="SSVC is a framework for prioritizing vulnerabilities based on
stakeholder needs.">` (an attribute the instrument does not render). The overview tutorial carries "How vulnerabilities are categorized in SSVC",
"How decision models are designed", the per-role prioritization categories, and the decision-point
definitions. The corrected URL is therefore the right primary capture and is the one used below.

Home-page fetch, retained in scratch only as provenance for the correction and **not** landed:
HTTP status=200, content-type=text/html; charset=utf-8, no redirect, 105807 bytes, Date
`Mon, 26 Oct 2026 17:01:37 GMT`, raw-body sha256
`60c00968563c688e4ffafb7a5b9fcedf097db8459114b92185c37cd4482112ed`, fetched_utc `2026-10-26T17:01:37Z`,
normalized 286 lines / 7730 bytes. No artifact of that fetch enters `corpus/`.

## 1. Raw fetch metadata (S054 primary capture)

| field | value |
|---|---|
| request URL | `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` |
| curl argv | `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -D headers-overview.txt -o raw-overview.html <url>` |
| HTTP status | 200 |
| effective URL | `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` |
| redirect count | 0 (requested == effective) |
| content-type | `text/html; charset=utf-8` |
| served bytes | 143053 (`content-length: 143053`, `size_download=143053`) |
| server | `GitHub.com` (GitHub Pages via Fastly) |
| Date header | `Mon, 26 Oct 2026 17:02:19 GMT` |
| Last-Modified | `Fri, 23 Oct 2026 16:21:47 GMT` |
| ETag | `"6adb899b-22ecd"` |
| cache | `x-cache: HIT`, `x-cache-hits: 1`, `age: 142`, `x-served-by: cache-gig2250050-GIG`, `x-proxy-cache: MISS` |
| fetched_utc | `2026-10-26T17:02:19Z` (UTC clock read immediately after the transfer; identical to the served Date second) |
| time_total | 0.026777 s |
| raw body sha256 | `9dba9f7500a6a1cece1a7acc77f1d768454b75fd04fa5bfdf382dfe598faec3f` |
| revalidation | conditional GET `If-None-Match: "6adb899b-22ecd"` at `2026-10-26T17:03:49Z` → **HTTP 304**, same ETag: the captured bytes were still the current representation ~90 s after capture |

Raw response headers captured in scratch (complete header set as served, line endings normalized
CRLF→LF for rendering; the `HTTP/2 200` line is the status line):

```text
HTTP/2 200 
server: GitHub.com
content-type: text/html; charset=utf-8
last-modified: Fri, 23 Oct 2026 16:21:47 GMT
access-control-allow-origin: *
strict-transport-security: max-age=31556952
etag: "6adb899b-22ecd"
expires: Mon, 26 Oct 2026 17:09:57 GMT
cache-control: max-age=600
x-proxy-cache: MISS
x-github-request-id: 697C:2BC285:6B9608:79AB7A:6ADF870D
x-github-edge-region: sea
accept-ranges: bytes
date: Mon, 26 Oct 2026 17:02:19 GMT
via: 1.1 varnish
age: 142
x-served-by: cache-gig2250050-GIG
x-cache: HIT
x-cache-hits: 1
x-timer: S1793034140.889840,VS0,VE1
vary: Accept-Encoding
x-fastly-request-id: 502f1ce79ac3715fd9dd9caf993f6fa773ec4956
content-length: 143053
```

## 2. Normalization (lane instrument, read-only import)

- Instrument: `corpus/instruments/capture-source.py`, sha256
  `e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18` (read from the lane working tree, not modified).
- Function: `html_to_text(raw.decode("utf-8", "replace"))`, imported via `importlib.util.spec_from_file_location`
  with the module never executed as `__main__` and no file written by the instrument.
- Behaviour (as the instrument documents it): `<script>`/`<style>` removed, block tags
  (`p div li tr h1-h6 section article br`) to newlines, remaining tags stripped, `html.unescape()`,
  runs of space/tab/NBSP collapsed, blank lines dropped, UTF-8, one final newline.
- Output: 32623 bytes, 518 lines, sha256 `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21`.
  LF only (0 CR), ends with exactly one `\n` (`...Manage settings\n`), 37 non-ASCII bytes (curly quotes,
  `®`, `©`), no backticks, no trailing whitespace on any line — so the fenced block below is unambiguous.
- Independently reproducible from the raw body: `html_to_text(raw-overview.html)` → same 32623 bytes.
- The raw 143053-byte HTML is **not** landed: the lane convention commits the normalized snapshot, so the raw
  body stays scratch-only with its sha256 recorded in §1.

## 3. S054.txt — byte-exact capture (518 lines)

The block below is `S054.txt` byte-for-byte: take the lines between the `BEGIN S054.txt byte-exact` and
`END S054.txt` comments, excluding the opening and closing fence lines. The content ends with the file's one
final newline (last line `Manage settings`). sha256 `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21`.

<!-- BEGIN S054.txt byte-exact -->
```text
What is SSVC? - SSVC: Stakeholder-Specific Vulnerability Categorization
Skip to content
SSVC: Stakeholder-Specific Vulnerability Categorization
What is SSVC?
Initializing search
CERTCC/SSVC
Home
SSVC
SSVC Overview
SSVC How-To
Understanding SSVC
Reference
Calculator
Explorer
About
SSVC: Stakeholder-Specific Vulnerability Categorization
CERTCC/SSVC
Home
SSVC
SSVC Overview
SSVC Overview
What is SSVC?
What is SSVC?
Table of contents
Intro
Defining stakeholders
How vulnerabilities are categorized in SSVC
Prioritization categories for Suppliers and Deployers
Prioritization categories for Coordinators
How decision models are designed
Supplier decision points
Exploitation
Utility
Technical Impact
Public Safety Impact
Safety Impact
Deployer decision points
Exposure
Automatable
Human Impact
Coordinator decision points for Triage
Coordinator decision points for Publication
Final notes
Multiple vulnerabilities of the same priority
Communicating results
Further reading
Starting out with SSVC
Other Resources
SSVC How-To
SSVC How-To
Overview
Getting Started with SSVC
Getting Started with SSVC
Intro
Prepare
Collect
Use & Respond
Summary
Stakeholder Decision Models
Stakeholder Decision Models
Supplier Decision Model
Deployer Decision Model
Coordinator Decision Models
Coordinator Decision Models
About Coordination
Coordination Triage
Publication Decision
CISA BOD 26-04 Response Model
CVSS v4 Analyst Models
CVSS v4 Analyst Models
About CVSS v4
Equivalence Set 1
Equivalence Set 2
Equivalence Set 3
Equivalence Set 4
Equivalence Set 5
Equivalence Set 6
Qualitative Severity
Gathering Info about Decision Points
Gathering Info about Decision Points
Intro
Automatable
Exploitation
Mission Impact
System Exposure
Technical Impact
Value Density
Customizing SSVC
Acuity Ramp
Using EPSS with SSVC
Using EPSS with SSVC
EPSS → SSVC Intro
EPSS Probability as input to Exploitation
EPSS Percentiles as an Amplifier
SSVC Tools
SSVC Tools
Docker Containers
Understanding SSVC
Understanding SSVC
Intro
State of Practice
Representing Information
Representing Information
Design Goals
Formalization Options
Decision Trees
Vulnerability Management Decisions
Vulnerability Management Decisions
Intro
Stakeholders
Decisions
Items With Same Priority
Risk Tolerance and Priority
Scope
SSVC and Asset Management
Putting the Pieces Together
SSVC as a Human-Scale Bottleneck
Worked Example
Evaluation
Related Systems
Information Sources
Limitations
Future Work
Reference
Reference
Intro
Decision Points
Decision Points
Intro
Automatable
Exploitation
Mission Impact
Public Value Added
Report Credibility
Report Public
Safety Impact
Supplier Cardinality
Supplier Contacted
Supplier Engagement
Supplier Involvement
System Exposure
Technical Impact
Value Density
Compound Decision Points
Compound Decision Points
Intro
Human Impact
Public Safety Impact
Utility
CISA-based decision points
CISA-based decision points
CISA Custom Decision Points
In KEV
Mission Prevalence
Publicly Exposed
CVSS-based decision points
CVSS-based decision points
CVSS Decision Points
Qualitative Severity
Base Metrics
Base Metrics
Attack Vector
Attack Complexity
Attack Requirements
Privileges Required
User Interaction
Confidentiality Impact
Subsequent Confidentiality Impact
Integrity Impact
Subsequent Integrity Impact
Availability Impact
Subsequent Availability Impact
Threat Metrics
Threat Metrics
Exploit Maturity
Environmental Metrics
Environmental Metrics
Confidentiality Requirement
Integrity Requirement
Availability Requirement
Supplemental Metrics
Supplemental Metrics
Safety
Automatable
Provider Urgency
Recovery
Value Density
Vulnerability Response Effort
Older Metrics
Older Metrics
Authentication
Collateral Damage Potential
Impact Bias
Remediation Level
Report Confidence
Scope
Target Distribution
Outcomes
Code
Code
Intro
Decision Points
Decision Tables
Decision Point Groups
Namespaces
Selections
CSV Analyzer
Doctools
Calculator
Explorer
About
About
Intro
Community Engagement
Decision Records
Acknowledgements
Change log
Contact
Table of contents
Intro
Defining stakeholders
How vulnerabilities are categorized in SSVC
Prioritization categories for Suppliers and Deployers
Prioritization categories for Coordinators
How decision models are designed
Supplier decision points
Exploitation
Utility
Technical Impact
Public Safety Impact
Safety Impact
Deployer decision points
Exposure
Automatable
Human Impact
Coordinator decision points for Triage
Coordinator decision points for Publication
Final notes
Multiple vulnerabilities of the same priority
Communicating results
Further reading
What is SSVC?
Intro
Risk exists on a continuum, and different stakeholders have different threat models and risk appetites. Cybersecurity risk is no exception.
Imagine you're a software developer, and you just found out about a vulnerability in a library upon which your product depends. You are now concerned that your software is also vulnerable. Upon investigation, you learn that your software does not use the vulnerable part of the imported library. Is your software, in its current state, at risk of this vulnerability? You likely answered, "probably not."
In this example, you are a Supplier of software that has an upstream Supplier vulnerability, but this vulnerability is not very risky to your business, so you are not very concerned. Conversely, the upstream Supplier probably wants the vulnerability patched as quickly as possible.
Unlike other vulnerability categorization systems that rate on technical severity (how bad it could be if the vulnerability were exploited) or exploitability (how likely it is that there will be an exploit), SSVC rates vulnerabilities on risk to the concerned stakeholder. It is not an attempted one-size-fits-all solution. SSVC follows a stakeholder-defined decision model to make these determinations of risk.
Caveats
All information in this document is suggested following research, but we must reiterate: it is not a one-size-fits-all system. We encourage stakeholders to define to define their own decision points, timeframes of actionability, and possibly, even their own roles.
Defining stakeholders
The above example includes a Supplier and a Deployer, and the third role is Coordinator. A stakeholder can be an individual or a group. It is possible for all three roles to exist within the same organization. Stakeholders are determined by their role in remidiation actions. For convenience, let's define these three:
Suppliers distribute software, and maintenance of their product can include providing remediations (patches) or suggesting mitigations for the affected product.
Deployers receive, evaluate, and apply the remediations or mitigations that the Suppliers provide.
Coordinators receive vulnerability reports and decide how, and whether, additional coordination is needed to improve response to the vulnerability.
All three stakeholders, even if within the same organization, will have different perspectives on risk, and therefore have different decisions to make.
Note
The three aforementioned roles are not exhaustive and are only the ones for which we have created decision models so far.
How vulnerabilities are categorized in SSVC
SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders. These categories reflect the timeliness of action to be taken. Suppliers and Deployers have different end-categories than Coordinators because they are making different decisions at different points in their responses. Decision Trees are used when asking the series of questions to categorize a vulnerability's priority. There will be more information on decision points (tree nodes) in the next section.
Prioritization categories for Suppliers and Deployers
The following categories, listed in increasing order of priority, are suggested end-categories for how a Supplier or Deployer should respond to a vulnerability. The actual actions will differ between Supplier and Deployer, but their immediacy is similar. We provide these categories as examples and encourage Suppliers and Deployers to define prioritization categories that match their needs. We've found many places have a 4-level Service Level Expectation that maps onto our categories; however, if an organization uses fewer or more priority levels, they can adapt.
Defer: do not act at present.
Scheduled: work during regularly scheduled time with normal resource constraints.
Out-of-cycle: act more quickly and potentially with extra resources than usual to resolve the vulnerability at the next available opportunity.
Immediate: use all possible resources to mitigate the the vulnerability as quickly as possible, potentially including pausing normal operations.
Many Suppliers and Deployers will want to resolve Defer vulnerabilities in due time, perhaps within 90 days. Defer simply means 'do not act at present,' not 'do not act at all.'
Prioritization categories for Coordinators
Our advice for Coordinators is based on the CERT/CC Coordinated Vulnerability Disclosure (CVD) project. Because we make separate decisions for triage and publication, we provide separate example decision tables, each of which has different prioritizations at the end. These decision tables represent how we apply SSVC to our needs, and other coordinators might make different decisions based on different inputs and output scales. The following categories are listed in increasing order of involvement.
A triage decision table might have:
Decline to act on the report.
Track information about the reported vulnerability, but do not take overt actions.
Coordinate a response to the vulnerabilty report, potentially including technical analysis, reproduction, notifying vendors, publication, and assisting another party.
Whereas a publication decision table might have:
Don't publish information about the vulnerability.
Publish information about the vulnerability.
How decision models are designed
All decision points and decision outcomes (priority categories) must be explainable to the non-expert. A decision point itself is not representative of risk, but the series of decisions point values help a stakeholder determine how risky a vulnerability is to their operation. We suggest the use of Decision Trees as a visual model to aid explanation to non-experts and experts alike.
While we encourage stakeholders to customize SSVC to their needs, in the interest of preserving a common vocabulary, we discourage stakeholders from modifying existing decision points; however, stakeholders are encouraged to set their responses based on their risk appetites.
Supplier decision points
Exploitation
Exploitation refers to how much evidence currently exists that the vulnerability is being exploited. This value is mutable because new evidence of exploit can arise at any time.
Exploitation (ssvc:E:1.1.0)
The present state of exploitation of the vulnerability.
Value
Key
Definition
None
N
There is no evidence of active exploitation and no public proof of concept (PoC) of how to exploit the vulnerability.
Public PoC
P
One of the following is true: (1) Typical public PoC exists in sources such as Metasploit or websites like ExploitDB; or (2) the vulnerability has a well-known method of exploitation.
Active
A
Shared, observable, reliable evidence that the exploit is being used in the wild by real attackers; there is credible public reporting.
Utility
Utility is about how much an adversary might benefit (relative to effort) from an attack campaign via use of the vulnerability. In other words, Utility is a combination of the value of each exploit event (Value Density) and the ease and speed (Automatable) at which an adversary can cause exploit events.
Value Density is described as "diffuse" (the system has limited resources) or "concentrated" (the system is resource-rich).
Automatable is a simple yes or no, can the attacker reliably automate all four steps (reconnaissance, weaponization, delivery, exploitation) of the kill chain? If the vulnerability allows remote code execution or command injection, the expected response should be 'yes.'
We define the following combinations to determine Utility values:
Utility (ssvc:U:1.0.1)
The Usefulness of the Exploit to the Adversary
Value
Key
Definition
Laborious
L
Automatable:No AND Value Density:Diffuse
Efficient
E
(Automatable:Yes AND Value Density:Diffuse) OR (Automatable:No AND Value Density:Concentrated)
Super Effective
S
Automatable:Yes AND Value Density:Concentrated
Technical Impact
Technical Impact refers to how much control of a system an attacker can gain. If 'yes' to any of the following questions, then the attacker has Total control of the system:
can the attacker install and run arbitrary software?
can the attacker trigger all the actions that the vulnerable component can perform?
does the attacker get an account with full privileges to the vulnerable component (administrator or root user accounts, for example)?
If the answer is 'no' to all of the above questions, then the attack is presumed to gain Partial control of the system. Examples of Partial control include denial of service and memory address information leaks.
Technical Impact (ssvc:TI:1.0.0)
The technical impact of the vulnerability.
Value
Key
Definition
Partial
P
The exploit gives the adversary limited control over, or information exposure about, the behavior of the software that contains the vulnerability. Or the exploit gives the adversary an importantly low stochastic opportunity for total control.
Total
T
The exploit gives the adversary total control over the behavior of the software, or it gives total disclosure of all information on the system that contains the vulnerability.
Public Safety Impact
Public Safety Impact is a reduction of the more expansive Safety Impact decision point to Signficant or Minimal. If the highest category of Safety Impact is Marginal, Critical, or Catastrophic, then the Public Safety Impact is Significant. If no types of harm are more severe than Neglible, then the Public Safety Impact is Minimal.
Public Safety Impact (ssvc:PSI:2.0.1)
A coarse-grained representation of impact to public safety.
Value
Key
Definition
Minimal
M
Safety Impact:Negligible
Significant
S
Safety Impact:(Marginal OR Critical OR Catastrophic)
Safety Impact is expansive to include impacts of physical harm, operator resiliency, system resiliency, environment, financial, and psychological harm. We used IEC 61508 to guide determinations of Negligible, Marginal, Critical, and Catastrophic impact on the aforementioned types of harm. Only one type of harm needs to qualify per category. Use the highest qualifying category to determine safety impact.
Safety Impact
Safety Impact (ssvc:SI:2.0.1)
The safety impact of the vulnerability. (based on IEC 61508 with modifications)
Value
Key
Definition
Negligible
N
Any one or more of these conditions hold. Physical harm: Minor injuries at worst (IEC 61508 Negligible). Operator resiliency: Requires action by system operator to maintain safe system state as a result of exploitation of the vulnerability where operator actions would be well within expected operator abilities; OR causes a minor occupational safety hazard. System resiliency: Small reduction in built-in system safety margins; OR small reduction in system functional capabilities that support safe operation. Environment: Minor externalities (property damage, environmental damage, etc.) imposed on other parties. Financial: Financial losses, which are not readily absorbable, to multiple persons. Psychological: Emotional or psychological harm, sufficient to be cause for counselling or therapy, to multiple persons.
Marginal
M
Any one or more of these conditions hold. Physical harm: Major injuries to one or more persons (IEC 61508 Marginal). Operator resiliency: Requires action by system operator to maintain safe system state as a result of exploitation of the vulnerability where operator actions would be within their capabilities but the actions require their full attention and effort; OR significant distraction or discomfort to operators; OR causes significant occupational safety hazard. System resiliency: System safety margin effectively eliminated but no actual harm; OR failure of system functional capabilities that support safe operation. Environment: Major externalities (property damage, environmental damage, etc.) imposed on other parties. Financial: Financial losses that likely lead to bankruptcy of multiple persons. Psychological: Widespread emotional or psychological harm, sufficient to be cause for counselling or therapy, to populations of people.
Critical
R
Any one or more of these conditions hold. Physical harm: Loss of life (IEC 61508 Critical). Operator resiliency: Actions that would keep the system in a safe state are beyond system operator capabilities, resulting in adverse conditions; OR great physical distress to system operators such that they cannot be expected to operate the system properly. System resiliency: Parts of the cyber-physical system break; system’s ability to recover lost functionality remains intact. Environment: Serious externalities (threat to life as well as property, widespread environmental damage, measurable public health risks, etc.) imposed on other parties. Financial: Socio-technical system (elections, financial grid, etc.) of which the affected component is a part is actively destabilized and enters unsafe state. Psychological: N/A.
Catastrophic
C
Any one or more of these conditions hold. Physical harm: Multiple loss of life (IEC 61508 Catastrophic). Operator resiliency: Operator incapacitated (includes fatality or otherwise incapacitated). System resiliency: Total loss of whole cyber-physical system, of which the software is a part. Environment: Extreme externalities (immediate public health threat, environmental damage leading to small ecosystem collapse, etc.) imposed on other parties. Financial: Social systems (elections, financial grid, etc.) supported by the software collapse. Psychological: N/A.
Deployer decision points
Exploitation is the same as for Exploitation in the Supplier model.
Exposure
Exposure refers to how difficult it would be for an attacker to access a system from the open Internet. This will vary with configurations and is therefore determined on a per-system basis.
If a system is not 'Open', we suggest the following questions to guide your decision:
If the system's networking and communication interfaces have been physically removed or disabled, choose small.
If Automatable is yes, then choose controlled. The reasoning behind this heuristic is that if reconnaissance through exploitation is automatable, then the usual deployment scenario exposes the system sufficiently that access can be automated, which contradicts the expectations of small.
If the vulnerable component is on a network where other hosts can browse the web or receive email, choose controlled.
If the vulnerable component is in a third party library that is unreachable because the feature is unused in the surrounding product, choose small.
System Exposure (ssvc:EXP:1.0.1)
The Accessible Attack Surface of the Affected System or Service
Value
Key
Definition
Small
S
Local service or program; highly controlled network
Controlled
C
Networked service with some access restrictions or mitigations already in place (whether locally or on the network). A successful mitigation must reliably interrupt the adversary’s attack, which requires the attack is detectable both reliably and quickly enough to respond. Controlled covers the situation in which a vulnerability can be exploited through chaining it with other vulnerabilities. The assumption is that the number of steps in the attack path is relatively low; if the path is long enough that it is implausible for an adversary to reliably execute it, then exposure should be small.
Open
O
Internet or another widely accessible network where access cannot plausibly be restricted or controlled (e.g., DNS servers, web servers, VOIP servers, email servers)
Automatable
Automatable is the same question as contained in the Supplier's Utility decision point.
For easy reference, Automatable is a simple yes or no, can the attacker reliably automate all four steps (reconnaissance, weaponization, delivery, exploitation) of the kill chain? If the vulnerability allows remote code execution or command injection, the expected response should be 'yes.'
Human Impact
Human Impact is similar to the Supplier's decision point Public Safety Impact in that it factors Safety Impact, but it differs in that it is a compound decision point to also consider Mission Impact.
For easy reference, the information on Safety Impact is again provided here:
Safety Impact is expansive to include impacts of physical harm, operator resiliency, system resiliency, environment, financial, and psychological harm. We used IEC 61508 to guide determinations of Negligible, Marginal, Critical, and Catastrophic impact on the aforementioned types of harm. Only one type of harm needs to qualify per category. Use the highest qualifying category to determine safety impact.
Safety Impact (ssvc:SI:2.0.1)
The safety impact of the vulnerability. (based on IEC 61508 with modifications)
Value
Key
Definition
Negligible
N
Any one or more of these conditions hold. Physical harm: Minor injuries at worst (IEC 61508 Negligible). Operator resiliency: Requires action by system operator to maintain safe system state as a result of exploitation of the vulnerability where operator actions would be well within expected operator abilities; OR causes a minor occupational safety hazard. System resiliency: Small reduction in built-in system safety margins; OR small reduction in system functional capabilities that support safe operation. Environment: Minor externalities (property damage, environmental damage, etc.) imposed on other parties. Financial: Financial losses, which are not readily absorbable, to multiple persons. Psychological: Emotional or psychological harm, sufficient to be cause for counselling or therapy, to multiple persons.
Marginal
M
Any one or more of these conditions hold. Physical harm: Major injuries to one or more persons (IEC 61508 Marginal). Operator resiliency: Requires action by system operator to maintain safe system state as a result of exploitation of the vulnerability where operator actions would be within their capabilities but the actions require their full attention and effort; OR significant distraction or discomfort to operators; OR causes significant occupational safety hazard. System resiliency: System safety margin effectively eliminated but no actual harm; OR failure of system functional capabilities that support safe operation. Environment: Major externalities (property damage, environmental damage, etc.) imposed on other parties. Financial: Financial losses that likely lead to bankruptcy of multiple persons. Psychological: Widespread emotional or psychological harm, sufficient to be cause for counselling or therapy, to populations of people.
Critical
R
Any one or more of these conditions hold. Physical harm: Loss of life (IEC 61508 Critical). Operator resiliency: Actions that would keep the system in a safe state are beyond system operator capabilities, resulting in adverse conditions; OR great physical distress to system operators such that they cannot be expected to operate the system properly. System resiliency: Parts of the cyber-physical system break; system’s ability to recover lost functionality remains intact. Environment: Serious externalities (threat to life as well as property, widespread environmental damage, measurable public health risks, etc.) imposed on other parties. Financial: Socio-technical system (elections, financial grid, etc.) of which the affected component is a part is actively destabilized and enters unsafe state. Psychological: N/A.
Catastrophic
C
Any one or more of these conditions hold. Physical harm: Multiple loss of life (IEC 61508 Catastrophic). Operator resiliency: Operator incapacitated (includes fatality or otherwise incapacitated). System resiliency: Total loss of whole cyber-physical system, of which the software is a part. Environment: Extreme externalities (immediate public health threat, environmental damage leading to small ecosystem collapse, etc.) imposed on other parties. Financial: Social systems (elections, financial grid, etc.) supported by the software collapse. Psychological: N/A.
Mission Impact is the impact on the Mission Essential Functions of the organization. A mission essential function (MEF) is a function “directly related to accomplishing the organization’s mission as set forth in its statutory or executive charter” 1.
Mission Impact (ssvc:MI:2.0.0)
Impact on Mission Essential Functions of the Organization
Value
Key
Definition
Degraded
D
Little to no impact up to degradation of non-essential functions; chronic degradation would eventually harm essential functions
MEF Support Crippled
MSC
Activities that directly support essential functions are crippled; essential functions continue for a time
MEF Failure
MEF
Any one mission essential function fails for period of time longer than acceptable; overall mission of the organization degraded but can still be accomplished for a time
Mission Failure
MF
Multiple or all mission essential functions fail; ability to recover those functions degraded; organization’s ability to deliver its overall mission fails
We define the following combinations of Safety Impact and Mission Impact values to determine Human Impact values:
Human Impact (ssvc:HI:2.0.2)
Human Impact is a combination of Safety and Mission impacts.
Value
Key
Definition
Low
L
Safety Impact:(Negligible OR Marginal) AND Mission Impact:(Degraded OR MEF Support Crippled)
Medium
M
(Safety Impact:(Negligible OR Marginal) AND Mission Impact:MEF Failure) OR (Safety Impact:Critical AND Mission Impact:Degraded)
High
H
Safety Impact:Critical AND Mission Impact:(MEF Support Crippled OR MEF Failure)
Very High
VH
Safety Impact:Catastrophic OR Mission Impact:Mission Failure
Coordinator decision points for Triage
The below decision points are modeled on CERT/CC Coordinated Vulnerability Disclosure (CVD) practice, but we encourage Coordinators to define their own criteria for Triage.
The first two questions help the CERT/CC determine if our help is required.
Report Public: If a report is already public, then CERT/CC will decline the case unless there are multiple suppliers, super effective Utility, and significant Public Safety Impact.
Supplier Contacted: If no suppliers have been contacted, then CERT/CC will decline the case unless there are multiple suppliers, super effective Utility, and significant Public Safety Impact.
In this case, CERT/CC may encourage the reporter to contact the supplier and submit a new case request if the supplier is unresponsive.
Report Credibility: If the report is not credible, then CERT/CC will decline the case.
Please see the CERT® Guide to Coordinated Vulnerability Disclosure for more information about assessing credibility.
Supplier Cardinality: Cases involving multiple suppliers can get complicated very quickly, so we are more likely to get involved in those cases.
Supplier Engagement: If the suppliers are already engaged in a case, there is usually less for a coordinator to do, making it less likely that we will coordinate a case.
Utility: If the vulnerability has high utility, then CERT/CC is more likely to coordinate the case.
Public Safety Impact: If the vulnerability has significant
public safety impact, then CERT/CC is more likely to coordinate the case.
The last two questions, Utility and Public Safety Impact, are the same as asked in the Supplier decision model.
Coordinator decision points for Publication
At the CERT/CC, a decision to publish is determined after criteria for Publication are met. SSVC adds value by codifying publication criteria so that the decision is explainable. Publishing a vulnerability should add public value, and a Coordinator must decide why they should publish instead of or in addition to the Supplier. Again, the below decision points are modeled on the CERT/CC Coordinated Vulnerability Disclosure (CVD) project, but we encourage Coordinators to define their own rationales for publication based on their missions.
The publication decision reuses the Exploitation decision point and adds two new ones (Supplier Involvement and Public Value Added).
Tip
Exploitation was first described in this document under the Supplier model, and the definition is the same regardless of the stakeholder.
Supplier Involvement - If the supplier is involved and likely to publish already, there is less need for the CERT/CC to publish.
Exploitation - If the vulnerability is being actively exploited, the CERT/CC is more likely to publish.
Public Value Added - If there is already significant public discussion of the vulnerability, there might not be much for the CERT/CC to add, making us less likely to publish.
What is the difference between Supplier Engagement and Supplier Involvement?
Supplier Engagement, asks whether a Supplier has acknowledged the vulnerability and is participating in the coordination effort.
Supplier Involvement, asks what, if anything, the Supplier is doing about the vulnerability.
Final notes
SSVC enables different stakeholders to make determinations about how a vulnerability will impact them, how to respond to a vulnerability, and how to communicate and explain their decisions. Unlike other vulnerability scoring systems, SSVC evaluates risk to a particular stakeholder without imposing a one-size-fits-all approach. The below subsections describe some other details about SSVC's features and provide links to further reading about SSVC and CVD.
Multiple vulnerabilities of the same priority
Naturally, a stakeholder will have multiple vulnerabilities at any given time, and it is likely that there will be multiple vulnerabilities of the same priority. The stakeholder can choose how to order vulnerabilities within the same priority- vulnerabilities of the same priority can be addressed in any order.
Communicating results
Coordinators will be especially concerned with communicating information about vulnerabilities, but Suppliers will be just as concerned about communicating to Deployers. Because information changes over time, SSVC decisions should always be timestamped and marked with the version of SSVC that was used. We provide a self-contained, machine-readable JSON schema.
Further reading
Reference material
Guidance for customizing a Decision Tree
Federal Emergency Management Agency. Federal continuity directive 2: federal executive branch mission essential functions and candidate primary mission essential functions identification and submission process. Technical Report, US Department of Homeland Security, Federal Emergency Management Agency, 2017. URL: https://www.fema.gov/sites/default/files/2020-07/Federal_Continuity_Directive-2_June132017.pdf. ↩
Back to top
Previous
SSVC
Next
Starting out with SSVC
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
-->
Copyright
©
Carnegie Mellon University
CERT®, Carnegie Mellon® and CERT Coordination Center® are registered in the
U.S. Patent and Trademark Office by Carnegie Mellon University.
Change cookie settings
Legal
Privacy Notice
Made with
Material for MkDocs
About our use of cookies on this site
We use cookies to measure the effectiveness of our documentation and whether users find what they're searching for. With your consent, you're helping us to make our documentation better. See our Privacy Notice for more.
Google Analytics
GitHub
Accept
Manage settings
```
<!-- END S054.txt -->


## 4. manifest.json — byte-exact (1-space indent, `json.dump(..., indent=1)`, trailing newline)

sha256 of the whole file: `fabc3163dbd31d33bff6e0bccf8b86b94e081b06b3ab1f00538dd9c0a57df642`, 3989 bytes. Take the lines between the `BEGIN manifest.json byte-exact` and
`END manifest.json` comments, excluding the fence lines.

<!-- BEGIN manifest.json byte-exact -->
```json
{
 "schema_version": 1,
 "purpose": "Round-37 F20 captured-source assertions for S054 (SSVC - Stakeholder-Specific Vulnerability Categorization, CERT/CC/Carnegie Mellon). Claims erratum 1 (commit b3620681) corrected the capture URL from the docs home page https://certcc.github.io/SSVC/ to the 'What is SSVC?' overview tutorial https://certcc.github.io/SSVC/tutorials/ssvc_overview/, because the home page lacks the decision-point methodology text the entry quotes. Fetched 2026-10-26T17:02:19Z with curl -sS -L --max-time 90 under the instrument UA kasegi-shokunin/1.0: HTTP status=200, content-type=text/html; charset=utf-8, no redirect (requested URL == final URL), fetched_bytes=143053, snapshot_bytes=32623, 518 lines, sha256 ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21. Served Date header equals the fetch second (Mon, 26 Oct 2026 17:02:19 GMT), Last-Modified Fri, 23 Oct 2026 16:21:47 GMT, Fastly x-cache=HIT age=142. Normalized with the lane's capture-source.py html_to_text() (markup stripped, entities unescaped, whitespace collapsed, UTF-8). The record array is the schema-mandated sources[] list read by source-recheck.py and capture-binding-check.py; it carries the requested url/fetched_utc/fetched_bytes/sha256/lines/normalized fields and the Q1-Q4 quote pins (each occurs exactly once in S054.txt).",
 "sources": [
  {
   "id": "S054",
   "path": "S054.txt",
   "url": "https://certcc.github.io/SSVC/tutorials/ssvc_overview/",
   "fetched_utc": "2026-10-26T17:02:19Z",
   "fetched_bytes": 143053,
   "snapshot_bytes": 32623,
   "lines": 518,
   "sha256": "ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21",
   "normalized": "capture-source.py html_to_text(): <script>/<style> removed, block tags (p div li tr h1-h6 section article br) to newlines, remaining tags stripped, html.unescape() applied, runs of space/tab/NBSP collapsed and blank lines dropped; UTF-8; final newline",
   "raw_sha256": "9dba9f7500a6a1cece1a7acc77f1d768454b75fd04fa5bfdf382dfe598faec3f",
   "http": {
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "final_url": "https://certcc.github.io/SSVC/tutorials/ssvc_overview/",
    "redirects": 0,
    "user_agent": "kasegi-shokunin/1.0",
    "fetched_utc": "2026-10-26T17:02:19Z",
    "date": "Mon, 26 Oct 2026 17:02:19 GMT",
    "last_modified": "Fri, 23 Oct 2026 16:21:47 GMT",
    "content_length": 143053,
    "cache_age_seconds": 142,
    "server": "GitHub.com"
   },
   "quotes": [
    {
     "id": "Q1",
     "quote": "SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders.",
     "anchor": 259,
     "location": "L259; first sentence of 'How vulnerabilities are categorized in SSVC', the captured page's own definitional statement. The site title line (L3) expands the acronym as 'SSVC: Stakeholder-Specific Vulnerability Categorization'; this page does not repeat the expansion as a body sentence."
    },
    {
     "id": "Q2",
     "quote": "All decision points and decision outcomes (priority categories) must be explainable to the non-expert.",
     "anchor": 277,
     "location": "L277; opening sentence of 'How decision models are designed', the decision-point/decision-outcome rule the methodology imposes."
    },
    {
     "id": "Q3",
     "quote": "Unlike other vulnerability scoring systems, SSVC evaluates risk to a particular stakeholder without imposing a one-size-fits-all approach.",
     "anchor": 473,
     "location": "L473; 'Final notes', the page's explicit contrast between SSVC and other vulnerability scoring systems."
    },
    {
     "id": "Q4",
     "quote": "CISA BOD 26-04 Response Model",
     "anchor": 68,
     "location": "L68; the site navigation entry naming the dedicated 'CISA BOD 26-04 Response Model' page under Coordinator Decision Models. No body sentence on this captured page discusses BOD 26-04; the pin records the conditional target as a navigation-only mention, not a sentence."
    }
   ]
  }
 ]
}
```
<!-- END manifest.json -->

## 5. Quote pins Q1–Q4

All four quotes occur **exactly once** in `S054.txt` as substrings, and each appears on exactly one line, so
every pin is a unique occurrence; each still declares its exact line as `anchor` and `source-recheck.py`
reports `anchor=<n>-ok` for all four.

| id | line | occurrences | words | anchor verdict | quote |
|---|---|---|---|---|---|
| Q1 | L259 | 1 | 12 | `anchor=259-ok` | SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders. |
| Q2 | L277 | 1 | 14 | `anchor=277-ok` | All decision points and decision outcomes (priority categories) must be explainable to the non-expert. |
| Q3 | L473 | 1 | 17 | `anchor=473-ok` | Unlike other vulnerability scoring systems, SSVC evaluates risk to a particular stakeholder without imposing a one-size-fits-all approach. |
| Q4 | L68 | 1 | 5 | `anchor=68-ok` | CISA BOD 26-04 Response Model |

Location notes (as carried in the manifest):

- **Q1 — definition.** L259, first sentence of the page section "How vulnerabilities are categorized in
  SSVC": `SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders.` The
  page's site-title line (L3: `SSVC: Stakeholder-Specific Vulnerability Categorization`) expands the acronym,
  but the overview does not repeat the expansion as a body sentence; the name expansion is therefore cited
  from the title line and the definition from L259. The complementary framing at L247 is a 41-word sentence,
  over the 25-word pin budget; its subordinate clause `SSVC rates vulnerabilities on risk to the concerned
  stakeholder` (11 words) would fit only by cutting the alternatives it contrasts, so L259 is pinned as the
  definition instead.
- **Q2 — decision point / outcome.** L277, opening sentence of "How decision models are designed".
  Companion decision-point mechanics available for a longer treatment: L259 `Decision Trees are used when
  asking the series of questions to categorize a vulnerability's priority.` and L277's second sentence
  on decision-point values. The pinned span is the rule that binds decision points and outcomes.
- **Q3 — distinction from alternatives.** L473, "Final notes": the page's explicit contrast with other
  vulnerability scoring systems, plus the one-size-fits-all refusal. The same contrast in fuller form at L247
  names the alternatives' axes (`technical severity` / `exploitability`) and runs to 41 words, over the pin
  budget.
- **Q4 — BOD 26-04.** **No body sentence about BOD 26-04 exists on this page.** The only occurrence of the
  string is L68, the site navigation entry naming the dedicated *CISA BOD 26-04 Response Model* page under
  Coordinator Decision Models (navigation renders once in the normalized capture, so the pin is unique).
  The pin is recorded as a navigation-only mention, not as a sentence, and the manifest's `location` says so.
  If the knowledge entry needs BOD 26-04 prose, the correct source is that dedicated page, not this one —
  which is outside my assigned capture.

## 6. Verification performed (read-only, from scratch copies)

`corpus/instruments/source-recheck.py --manifest <scratch>/manifest.json` → **exit 0**:

```text
S054:sha256 OK
S054:Q1 OK occurrences=1 anchor=259-ok
S054:Q2 OK occurrences=1 anchor=277-ok
S054:Q3 OK occurrences=1 anchor=473-ok
S054:Q4 OK occurrences=1 anchor=68-ok
```

`corpus/instruments/capture-binding-check.py --root <scratch>/bindroot` → **exit 0** (scratch root = a copy of
`corpus/SOURCES.md` with one simulated `S054` row carrying the corrected URL plus
`corpus/source-snapshots/round-37/{S054.txt,manifest.json}`; the simulation exists only to prove the
manifest binds under the erratum URL — the real row is the L1's write):

```text
MANIFEST round-37 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=1 with_url=1 with_fetched_utc=1 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=0
records=1 bound=1 unbound=0
```

(The scratch root's snapshot directory held only `S054.txt` + `manifest.json`, both manifest-bound, hence
`orphans=0`. With the simulated row present, `multi_row_url=0` — no other registry row carries the corrected
URL.)

Byte-exactness self-check on this receipt: the fenced S054 block was re-extracted from the rendered receipt
and re-hashed to `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21` (matches `S054.txt`), and the manifest block was re-parsed as JSON and compared
byte-for-byte with `manifest.json`.

## 7. Landing instructions for the L1

1. Write `S054.txt` exactly as §3 to `corpus/source-snapshots/round-37/S054.txt` (32623 bytes,
   518 lines, sha256 `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21`).
2. Write the §4 block exactly as `corpus/source-snapshots/round-37/manifest.json`.
3. Registry row `S054` must carry the single `https://` token
   `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` in its source cell (rule B5 is byte-exact; the
   home-page URL will fail binding), tier A, mined, opened 2026-10-26, and point at
   `corpus/source-snapshots/round-37/S054.txt` with this sha256.
4. The knowledge entry's `source: S054` citation then resolves; `source-recheck.py --source S054` and
   `capture-binding-check.py` both pass on the landed tree (proven above against the corrected URL).

## 8. Risks and limits

- **Cache-served bytes.** `x-cache: HIT` with `age: 142` means the representation was assembled ~142 s before
  my request; the capture is of that cached representation, and the 304 revalidation at 17:03:49Z shows it was
  still current. This is normal for the instrument and does not weaken the pin, but it is recorded rather than
  hidden.
- **Page is a tutorial, not a standard.** The overview is CERT/CC's own documentation prose; it is a
  first-party statement of the methodology, not a normative specification, and its footer carries an MIT-style
  permission notice plus `Made with Material for MkDocs` (theme boilerplate, not a statement about the
  methodology). The entry should quote it as documentation, not as a standard.
- **Q4 is navigation-only.** Stated above; do not let the knowledge entry attribute a BOD 26-04 sentence to
  this capture.
- **Freshness.** The capture proves what the page served at `2026-10-26T17:02:19Z` (Last-Modified
  `2026-10-23T16:21:47Z`), not that it says the same today; `source-recheck.py` reads local bytes only.
- **No blocker.** Both required instruments pass on the corrected URL; only the registry row write remains
  outside my scope.

## 9. Tooling and scratch

- No tools installed or upgraded; no pacman invoked (transactions paused host-wide). `curl` (host), `python3`
  (host) and the lane instruments sufficed — nothing to record under the 2026-10-19 tooling authorization.
- Scratch root `/fast/scratch/hyaku/kasegi-r37/ExecC2Capture/` held the raw body, headers, normalizer,
  manifest builder, binding simulation and these blocks; all work copies were bound there and the directory
  was removed after this receipt was copied into the wave dir.
- No file in the lane repo, the fleet root, shokuknow, or any source tree was modified. Only this receipt was
  written into the lane.
