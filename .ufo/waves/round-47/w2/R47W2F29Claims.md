# R47W2F29Claims — integrated F29 claim review

Axes: depth:verifiability; coverage. Scope: the whole corrected F29 entry, especially default-publication claims, service clocks, and universal conditions. Reviewed revision `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193` remains the assigned contract.

## Findings by severity

All paths below are relative to the lane repository. Entry = `corpus/knowledge/github-repository-security-advisories.md`; source = `corpus/source-snapshots/round-47/S076.txt`. These are static semantic counterexamples, not executed fixtures. Five distinct actionable findings remain after the re-anchor.

### F1 — Medium: private drafts do not prohibit previously public details

**Entry:18** concludes: “The draft is where the private discussion happens, so no advisory detail may be public before that draft is published.” The cited **source:570** describes what a draft enables, not a global embargo. **Source:573** expressly permits republishing details already disclosed elsewhere; the entry itself records that permission at **entry:34 (G7)**.

Counterexample: a maintainer creates a repository advisory from an existing public disclosure. That is an explicitly supported use, yet its details were public before the new draft was published, violating entry:18. This is not merely an absent source statement; the entry contradicts its own source-backed G7.

Recommendation: restrict the assertion to the private draft discussion/visibility. Remove the universal prohibition on any prior public advisory detail; preserve the republication case.

### F2 — Medium: the final conformance predicate still makes fix versions mandatory

**Entry:123-124** says GitHub conformance requires “all four” recorded conditions; **entry:139-140** requires “A fix version was added before publication.” **Entry:46 (G19)** likewise asks what the advisory “must” carry and quotes only the middle of the qualified sentence.

**Source:596** begins “Whenever possible, you should” and explicitly describes publication without a fixed version. **Source:599** permits publication while the fix remains in development, with a later edit; **source:600** covers no planned fix. The corrected **entry:110-113** even says a package “may not record that a fix version is mandatory,” but its final predicate does exactly that.

Counterexamples: publish while a fix is in development and say so; publish with no planned fix and clearly document that status/mitigations. Both match source:599-600 and fail entry:139-140. This means the D6 prose correction did not repair the operative package rule.

Related overstatement in the same duty: **entry:112** says the imminent-fix case “forbids” publication, whereas **source:598** conditions the advice on “and you are able to.” The correction should retain that condition rather than turn advice into an unconditional prohibition.

Recommendation: carry the qualified duty and documented exception branches through G19 and the final predicate, not only Limits.

### F3 — Medium: a GitHub CVE request is optional, not required for every conformant advisory

Under the universal lead-in at **entry:123-124**, **entry:131-138** requires a request from GitHub while the advisory is private and requires GitHub as assigning body. **Entry:21** also infers that the request is necessarily made against a still-private advisory from a sentence saying only that requesting does not make it public.

**Source:583** explicitly offers an existing CVE and says “If you want” an identifier and do not already have one, “you can request” one. It also makes reservation conditional on eligibility. **Source:584** instructs a maintainer with an existing CVE, including one from another CNA, to add it to the form; GitHub cannot assign when another CNA covers the project.

Counterexample: a maintainer adds an already assigned identifier from the appropriate other CNA and publishes the advisory. This follows source:584 but cannot satisfy the supposedly universal GitHub-request condition. Even the corrected coverage boundary inside entry:134-138 does not give this package a successful branch. An advisory without a requested CVE is also not ruled nonconformant by the source. Moreover, “requesting does not make public” is not evidence that requests are allowed only before publication.

Recommendation: branch on existing CVE, optional eligible GitHub request, and other-CNA coverage. State the privacy effect without inventing a mandatory request or exclusive request timing.

### F4 — Medium: temporary private fork capability becomes a mandatory workflow

**Entry:123-124,129-130** makes development in a temporary private fork necessary for every GitHub-conformant advisory. **Entry:19,32** likewise presents the fork as where the fix is developed rather than one supported workflow.

The source introduces **source:570-572** with **source:569**, “With repository security advisories, you can:”. This is a list of capabilities, not a requirement that every advisory demonstrate every capability. **Source:573** permits republishing an existing disclosure; **source:600** permits a case with no planned fix. Neither implies development of a new fix in a GitHub temporary private fork.

Counterexample: an advisory for a no-planned-fix vulnerability records the status and mitigation as source:600 recommends. It cannot satisfy entry:129's requirement that a fix was developed in that fork. Independently, republishing an existing disclosure does not establish where its prior fix was developed. The source provides no basis for rejecting either package solely for lack of fork evidence.

Recommendation: qualify the private-fork check to packages claiming that collaboration route; do not equate a platform capability with universal GitHub conformance.

### F5 — Medium: universal denial of a publication-linked clock is unsupported

**Entry:78-79** says the CVE review and Dependabot processes are service clocks and “neither starts a clock at publication.” Yet **entry:23-24** correctly calls the second a “post-publication Dependabot step.” **Source:593-594** is headed “Dependabot alerts for published security advisories” and says GitHub will review “each published security advisory,” then describes “This process” as taking up to 72 hours.

The source supports separating CVE-request review (**source:583**, “usually” within 72 hours) from the published-advisory review/database/possible-alert process (**source:594**). It does not support the categorical denial that the latter has a publication-linked trigger. Conversely, it does not specify an exact scheduler timestamp or promise alert delivery to every repository; it says alerts “may” be sent and adds a fork/package restriction.

Recommendation: retain the distinction and lack of a researcher disclosure deadline, but describe the second interval as the post-publication process. Do not invent either a categorical non-publication start or an unconditional publication-to-alert SLA.

## What the safe repair does and does not establish

The committed diff re-anchors the entry to S076, identifies capture chrome, corrects the source-order attribution, and changes the three-case description to two permission cases. The full committed entry still contains the five independent claim failures above. None is cured by locating the adjacent quotation correctly. Findings F1/F3/F4/F5 are retained semantic overclaims; F2 also identifies an internal inconsistency surviving the corrected Limits paragraph. They are not accusations that round 47 newly introduced all these sentences.

Read `corpus/lessons/round-47.md:57-69`: C1 is not fully met because rejecting historical S074 would break B3; C2 remains unmet because ZDI is F02 enrichment, not F30. This report does not reroll either frozen target, recommend rejecting S074, or infer a successful integrated semantic outcome from mechanical gates.

## Evidence and verification gaps

Executed only read-only repository inspection: `git show --stat --oneline 65e19bdb142c90a08103eb4b2af60c71218a920e`, the base-to-integrated entry diff, and `git --no-pager show 65e19bdb142c90a08103eb4b2af60c71218a920e:corpus/knowledge/github-repository-security-advisories.md`. Read the complete numbered entry (1-145), full source policy context (567-600), integrated lesson, W1 lesson handoff, and historical claims review. No corpus instrument, runtime, selftest, mutation battery, network/domain action, or alternate runtime was invoked. No gate outcome is claimed here.

LSP prerequisite: `read xd://lsp` returned “No such tool”; no LSP device/server status is available in this session. References/definition/diagnostics therefore could not be requested. Text search was used only for literal discovery, not semantic proof; findings derive from the committed prose and cited source context.

Residual risk: current live GitHub behavior and sibling page bodies were not reviewed; this is a pinned-documentation claim review, not proof of live product behavior. The source does not establish an exact post-publication timer start instant. No canonical runtime, rerouting, saturation, or resume behavior changed in this bounded documentation item, and no claim about those systems is made. No installs/updates, git/jj mutations, services, production edits, or scratch files were used; no scratch cleanup was necessary.

## Self-evaluation (not a gate)

Accuracy 4/5: direct source counterexamples, but no live-page verification. Completeness 4/5: the whole entry and assigned claim classes were read; sibling bodies remain outside scope. Clarity 4/5: exact line ranges and paths are supplied; long conformance predicate necessarily spans several findings. Actionability 4/5: each finding names a bounded semantic correction; no production edit was authorized. Conciseness 4/5: separate witnesses avoid conflating three different universal requirements, at some length cost. Mean 4.0/5. Highest-impact improvement is reconciling the final conformance predicate with the source's explicit optional/qualified branches. The user should agree this is a scoped static review, not an execution or admission verdict.

Report: .ufo/waves/round-47/w2/R47W2F29Claims.md
