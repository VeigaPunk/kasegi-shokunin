# R47RevScopeout — scoped review

Axes: depth:verifiability; coverage. Recommendation only; no admission or integration.

## Findings by severity

No actionable defect found in the reviewed F30 entry and S075 scope cell. Important qualification: the capture does **not** contain zero advisory-related prose. Excluding individual advisory records is supported; excluding all discussion of advisories would be false.

## Evidence

Paths below are relative to the lane root. Drafts are under `.ufo/waves/round-47/w1/`.

- Complete source body read: `corpus/source-snapshots/round-47/S075.txt:20-27`. Lines 21-22 state policy scope and vendor notification/customer filters; :23 contains contact escalation and possible public-advisory fallback; :24 conditional limited-advisory publication and extensions; :25 faulty-patch tiers; :26 acquired-vulnerability disclosure/workarounds and communication transparency; :27 website-only official-advisory status. No individual advisory record, payout/reward/program eligibility terms, or researcher submission procedure appears in this body. Those are different surfaces, not synonyms for policy publication provisions.
- Chrome makes the boundary explicit without supplying those surfaces' content: `S075.txt:9,16,56-58` names advisory navigation; :31-32 names researchers/Submit a vulnerability; :53 names Researcher Rewards. Merely naming/linking a surface is not capturing its rules or records. The linked blog is referenced at :25, not imported.
- Entry reviewed in full: `R47SrF30Entry.draft/zdi-disclosure-policy.md:1-34`. :7, :11-22 and :34 stay within response/patch branches, conditional publication, extension authority and the unstated start event; none requires advisory records, reward terms or submission-page evidence. :26's F02/F15 contrast is separate local-corpus attribution, not an assertion about the excluded ZDI surfaces. :30 explicitly excludes those surfaces and the linked blog, distinguishes the :27 policy assertion from actual advisory publication, and denies a live-page/actual-conduct claim.
- Row matches that boundary: `R47SrRegistry.md:19`, scope cell: “ZDI's own stated disclosure policy for acquired vulnerabilities and product-vendor coordination; not individual advisory records, reward terms or researcher submission rules”. Its anchor cell points to body :20-27 and its policy provisions, not excluded pages. The README block is equally precise at `R47SrRegistry.md:48-49`.
- As-of discipline: entry :1-3 names the pinned capture, review date and recheck; :30 explicitly says pinned support does not establish current network freshness. All ZDI behavioral language in :7-22 is attributed policy language, not an observation that ZDI actually behaves that way today. Manifest `corpus/source-snapshots/round-47/manifest.json:14-23` records the single fetch instant `2026-10-30T10:35:37Z`, digest and body range. This avoids conflating a dated source with continuing service behavior (R1 at `corpus/QUALITY.md:35`).

## Control discrimination

The do-nothing control is the unmodified base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`. Inherited receipt `.ufo/waves/round-47/controls/c2-base.txt:2-3,5-9` reports entry absent, S075 row absent and `f30-gate fixed=1/7 exit=1`; it cannot supply the entry/row scope boundary reviewed above. This is inherited execution evidence, not a rerun or proof that the integrated candidate reaches 7/7. Semantic discrimination here is concrete: a claim about reward eligibility, a researcher submission requirement or an individual published advisory would have no support in the complete body; a publication-policy statement does have support at :23-27. A blanket “no advisory content” claim would fail this reading even if a marker counter passed.

## Reviewed byte identities

`sha256sum` printed:

- S075 capture: `9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1`.
- F30 entry draft: `f7c037c25196d68d7c58203b77245adf0d517a007f5a30e943b0e0b80c1cadfb`.
- Registry draft report: `6f4d39a96cd46001d05b805a97890c781da13b563009e089dea5eb63f00feed8`.

## Residual risk and verification gaps

- Draft-only review; integration and subsequent edits are not covered. No counter, full battery, live network recapture or operational behavior check was run by this seat. L1/wave 2 must check integrated bytes; independent novelty review remains outside this scope.
- Known mechanical limits remain disclosed: C1 16 uncaught /35 mutants; C2 18 uncaught /21, baseline_failures=0 (`claims.json:18,41`; `controls/freeze-controls.txt:3`). No saturation claim.
- Semantic tooling unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; no LSP server/status/references/definition/diagnostics could be obtained. Literal file reads were used for Markdown/capture review, not presented as semantic call-graph proof.
- No tools installed; no production files, git/jj state or sibling repositories modified. No scratch directory, fixture, clone or heavy pass was created, so no scratch cleanup remains.

Self-check: accuracy 4/5 (local captured support only, no live verification); completeness 5/5 for the named scope surfaces and dated-behavior check; clarity 5/5 (policy/record distinction explicit); actionability 4/5 (integration remains L1-owned); conciseness 4/5 (byte/control provenance retained for auditability). Overall 4.4/5. Highest-impact improvement is to bind the same review to integrated bytes after landing; this is a verification gap, not a scoped defect.

Report: .ufo/waves/round-47/w1/R47RevScopeout.md
