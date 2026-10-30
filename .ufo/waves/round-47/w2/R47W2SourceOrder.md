# R47W2SourceOrder — integrated F29 ordering review

Axes: **depth:verifiability**, **coverage**. Review recommendation only, not admission or judgment.

Scope: integrated revision `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`. Single bounded item: attribution of F29 decision-rule numbering versus the captured document's order.

## Findings by severity

**No actionable finding in the assigned ordering correction.** The committed entry no longer attributes its numbered ordering to GitHub's page.

### Static evidence and adversarial checks

1. **Old false attribution removed, not merely contradicted elsewhere.** The actual base-to-integrated diff replaces “in the order the page states it” with the explicit same-location disclaimer at `corpus/knowledge/github-repository-security-advisories.md:16`: “the page states the CVE request before the fix-version material, so the numbering below is this entry's, not the page's order”. `git show 65e19bdb142c90a08103eb4b2af60c71218a920e:corpus/knowledge/github-repository-security-advisories.md` independently exposed that committed text; this is not review of an unlanded draft.
2. **Disclaimer agrees with capture, including section context.** `corpus/source-snapshots/round-47/S076.txt:580-584` contains the CVE section and request mechanics; `:595-600` contains the fix-version section and its qualifications. In particular, request mechanics at `:583` precede fix-version advice at `:596`.
3. **The intentionally different entry numbering remains visible.** Entry `:18-21` maps draft → private fork → fix version → CVE request to source lines `570`, `571`, `596`, `583`. The inversion is real, and the corrected sentence explicitly owns it instead of pretending those anchors are ascending. No reordering of historical capture bytes was needed.
4. **Source summary was not confused with detailed source order.** Entry `:12` accurately quotes source `:558` (“privately discuss, fix, and publish”); that three-phase summary does not assert the CVE/fix-version enumeration used by the entry. The actual detailed source section order above is the relevant comparison.
5. **Other local enumerations do not restore the attribution.** Entry `:81-84` calls the lifecycle “one ordered rule” but does not call that order the page's. The falsifiable package list at `:126-140` lists CVE request before fix version and likewise makes no claim to reproduce source numbering. These are not evidence that GitHub mandates a relative CVE-versus-fix-version sequence. The correction at `:16` must remain attached to the decision rule if that list is later extracted or reused.
6. **Integrated decision record is honest about larger failures.** `corpus/lessons/round-47.md:59-60,65-69` keeps C1 not fully verified (S074 stays mined historical rather than the frozen rejected transition) and C2 unmet (ZDI remains F02 enrichment; no independent F30). This bounded successful attribution repair does not close either target.

## Residual risk and verification gaps

- Ordering attribution is corrected; this is not a full review of every inherited conformance claim in F29 or every mutation survivor. A self-owned enumeration is not proof that GitHub requires its chronology.
- No saturation or milestone-total claim: this seat provides six distinct static checks of one bounded repair, not 32 independently executed attacks and not a whole-wave verdict.
- `read xd://lsp` returned `No such tool: xd://lsp`; status/references/definition/diagnostics were unavailable. Literal searches and source/diff reads are documentary evidence, not semantic caller proof. These inputs are Markdown/plaintext, not executable caller paths.
- Executed only read-only Git inspection (`diff --stat`, scoped base-to-integration `diff`, committed-entry `show`, and pinned-revision-versus-working-source/lesson `diff`, which emitted no differences), plus tool reads/searches. No application runtime, counter, selftest, mutation battery, network fetch, source recheck, domain-target action, service restart, or git/jj mutation was run. No runtime result is inferred from prior reports.
- Read the round-47 lesson and W1 `R47RevD6.md:13-15,34-41`; W1 observations are historical supporting context, not this seat's executions. No source captures were changed.
- No installs or updates. No scratch was created, so none remains to delete. Only this report was written.

## Self-evaluation (not a gate)

Accuracy 4/5: pinned entry and source locations inspected; no live-page claim. Completeness 5/5: assigned source-order attribution, actual committed replacement, and nearby competing enumerations checked. Clarity 4/5: separates six static checks from execution evidence, at the cost of detail. Actionability 5/5: no scoped repair requested; retain the attribution disclaimer with any extracted rule. Conciseness 4/5: evidence list is longer than the no-finding conclusion. Overall 4.4/5. Highest-impact improvement would be an extraction-use audit only if a future change creates an actual consumer; none is asserted here. Self-check: the scoped result does not imply either frozen target was achieved.

Report: .ufo/waves/round-47/w2/R47W2SourceOrder.md
