# ScopeConnect — round-62 predata overlap/province screen

Axes: coverage; depth:verifiability. This is evidence and one bounded recommendation, not admission, a frozen predicate, integration, score change, or sandbox claim.

## Recommendation: retain only the phase × responsibility distinction

**[INFERENCE] S095 supports narrowly distinct coverage, not new discovery that CVD has phases, roles, validation, prioritization or a post-publication remediation obligation.** Recommend proposed F43 as **CERT/CC's own adapted ISO/IEC 30111:2019 CVD presentation and its five-role phase/responsibility matrix**, applied to local package attribution. Keep existing holders authoritative for their own claims. Reject F43 if reduced to generic process-stage vocabulary or generic publication-versus-deployment advice.

The non-obvious synthesis is to make **Reporter × Remediation = fix confirmation versus Vendor/Coordinator × Validation = report validation** the distinguishing package-review rule. That preserves FIRST's existing requirement for finders to provide verification artifacts without pretending the CERT table prohibits reporter-side checking. It adds a precisely checkable attribution distinction rather than duplicating existing prioritization/coordination guidance.

## Evidence and overlap table

All paths below are relative to the lane unless explicitly absolute. Read the prefreeze controls `neighbor-screen-assessment-r62.txt` and `neighbor-screen-r62.txt` under `.ufo/waves/round-62/controls/`.

| Holder | Already held; overlap | Residual S095 distinction / consequence |
|---|---|---|
| S003 + S004, `corpus/knowledge/coordinated-disclosure-timelines.md:6-42` | Policy/coordinator attribution, clock trigger, interval, patch/publication relationship and exceptions; CISA supplier guide and CERT/CC's own 45-day policy. | S095's phase-to-role assignments are not those clock rules. Do not derive a disclosure deadline from S095. |
| S023 / F06, `corpus/knowledge/cisa-cvd-program-stages.md:38-77` | CISA's seven program stages, triage and coordination, conditional CVE determination, advisory preparation, public disclosure and KEV evaluation. | S095 describes CERT/CC's adapted model, not CISA's pipeline; its Deployment is applying remediation, not KEV evaluation. Merely adding another list of stage names is weak novelty. |
| S018 / F06, `corpus/knowledge/multiparty-vulnerability-coordination.md:6-46` | Finder/vendor/coordinator roles, verification artifacts, upstream/downstream relationships and the fact that one vendor's patch does not prove downstream fixes. | **Already-held awareness/fix-propagation distinction:** do not claim S095 first introduced it. Distinct table attribution is Reporter fix confirmation versus incoming-report validation, not a new prohibition on finder verification. |
| F11, `corpus/knowledge/iso-29147-and-30111-division-of-labour.md:7-19,39-47` | JPCERT's outward disclosure / internal handling split, 29147:2014 / 30111:2013, Hitachi's three-step standards mapping. | S095 adapts 30111:2019 and maps phases to five participant roles. It is not an independent reading of normative ISO clauses. |
| Related S041, `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md:11-55` | Guideline/ISO policy-obligation differences, clause crosswalk and acknowledgment guidance. | Not the CERT/CC role matrix; do not restate these obligations under F43. |
| F38, `corpus/knowledge/iso-29147-30111-standard-records.md:9-57` | ISO publisher identity, editions/status, abstracts' division of labour and applicability; normative text explicitly excluded. | S095 is an attributed adaptation, not ISO requirements, a new standards edition, or replacement for those records. |
| F20 / S054, `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md:20-44` | Stakeholder-dependent prioritization already distinguishes Supplier/Deployer roles and Coordinator publication decisions. | **Not new:** different roles prioritize different things. S095 contributes its specific report-response / fix-deployment cells, not SSVC decision rules or priority categories. |

The broad `phase` search also located GitHub repository advisories' discuss/fix/publish summary, internal intake/finalization phases and historical gate phases; none is this table. Existing F42 ends `PROVINCE.md:211`; no F43 or S095 registry/README admission was present in the inspected screen. That is the state inspected, not a guarantee about concurrent later integration.

## Source structure and explicit contradictions

`corpus/source-snapshots/round-62/S095.txt`: 195 lines; observed SHA-256 `bed305896d46ef54f162b955585157e215f5082a27789ac71cfb9c045dddcac2` matches assignment.

- L57-59 calls this an adaptation of ISO/IEC 30111:2019, “with more phases to better describe what we have seen at the CERT/CC”. L73 acknowledges differing models.
- **Six summary headings versus seven table rows:** L60-70 combines Validation and Prioritization; L129-140 separates them. This source-internal presentation difference must remain explicit, not smoothed into an exactly-six/seven universal process claim. Navigation repeats headings outside the body.
- Matrix column order is Finder, Reporter, Vendor, Coordinator, Deployer, L112-116. Validation L129-134 assigns Vendor/Coordinator “Validates reports received”; Remediation L141-146 assigns Reporter “Confirms fix”. A dash is not a real-world prohibition.
- Prioritization L135-140 distinguishes reports for response from fixes for deployment; Public Awareness L147-152 differs from Deployment L153-158. Those specific cells are evidence; generic awareness/deployment separation overlaps S018.

Read the current-round EntryDraft and ScoutS095 reports as proposal/evidence data only. EntryDraft's C3/C5 and its explicit dash qualification fit the recommended distinction. Its C4/C6 are supporting context, not independently uncovered concepts. Scout reports an independently fetched byte-identical capture; this seat did not repeat that network operation or claim it as its own.

## Downstream consumers and sibling provinces

Snapshot sweep for `CERT-Guide-to-CVD` found the new S095 text/manifest and `corpus/source-snapshots/round-24/S003.txt:442-444`: a references-list citation to **Preparing for Public Awareness**, the child URL `topics/phases/public_awareness/?h=silent`. It is a real prior related reference, not prior mining of this parent matrix. Thus “no prior CERT Guide references” is false; “no held entry for this parent matrix found in the bounded screen” is supported.

Shell expansion screened 21 direct-child `PROVINCE.md` files (including kasegi). Broad phase/coordinated-vulnerability/disclosure hits outside kasegi were kaidoku:18, kama:329, kengaku:328, revenger:9/12, tabi:93 and kake:291. The first five non-kake hits were inspected as tool/receipt disclosure or artifact-triage boundaries, not a competing CVD model claim. Most importantly:

- `/home/vgpnk/Projects/shokunin/kake-shokunin/PROVINCE.md:290-293` expressly excludes vulnerability handling, intake, triage, remediation, disclosure timing and bounty/policy operation.
- `/home/vgpnk/Projects/shokunin/revenger-shokunin/PROVINCE.md:3-13` owns shipped-artifact reverse engineering; bounty/CVD triage is static/artifact-first through its training module, not ownership of general phase guidance.
- Kasegi `PROVINCE.md:43-52` retains chousa research method, kagi secrets, kake web properties and kengaku evaluation as adjacent; live-target testing remains refused.

**[INFERENCE] No contested ownership found within this direct-child province and held-entry screen.** No claim of all-domain novelty or inspection of every sibling corpus. The prior round's late downstream/sibling screen (`corpus/lessons/round-61.md:80-92`, `controls/neighbor-screen-postfreeze-r61.txt`) cannot satisfy prefreeze order retroactively. This report is predata evidence for L1 to retain before its actual freeze, not proof of that future order.

## Surfaces, risks and verification handoff

- Runtime: documentation-only; no contacts, target operations, new execution path, or another runtime invoked.
- Contract: bounded first-party attribution; no ISO normative inference, universal phase count, testing authority or new reporter obligation.
- Substrate: immutable S095 digest plus row/column anchors; repeated matrix cells require anchor binding rather than substring uniqueness assumptions.
- Verification: L1 should retain this screen before freeze and bind the proposed falsifier to complete headings/rows. A worksheet attributing report-validation to Reporter fails this source's table attribution; a worksheet retaining reporter fix confirmation must not fail merely because the finder also supplied verification evidence under S018. Final counters/rechecks remain integration work, not exercised by this seat.
- Axes: expected coverage benefit is a missing attribution distinction; verifiability benefits from exact row/column tests. No score increase or empirical no-harm result is asserted. Main risk is novelty inflation by selling overlapping C4/C6 context as new ground.

## Commands, outputs, limits and cleanup

Read RULES and godspeed first; read QUALITY Q1-Q10/R1-R19, round-61 lesson/spotcheck, SCORECARD planned-for-62 L2524-2527. Used read/grep/glob for the evidence above; no admission instrument, selftest, build or unrelated suite was run.

Executed core shell checks (absolute lane path abbreviated here as L only for display):

```text
sha256sum L/corpus/source-snapshots/round-62/S095.txt
  -> bed305896d46ef54f162b955585157e215f5082a27789ac71cfb9c045dddcac2
wc -l L/corpus/source-snapshots/round-62/S095.txt L/PROVINCE.md
  -> 195; 211
grep -ril phase L/corpus/knowledge | sort
  -> considerthese-proposals-ledger.md; github-repository-security-advisories.md;
     intake-and-finalize.md; iso-29147-and-30111-division-of-labour.md
grep -in 'phase\|coordinated vulnerability\|disclosure' /home/vgpnk/Projects/shokunin/*/PROVINCE.md
  -> hits in seven lanes including kasegi; inspected as above
printf '%s\n' /home/vgpnk/Projects/shokunin/*/PROVINCE.md | wc -l
  -> 21
```

Successful shell checks returned exit 0. Initial scratch creation failed because the requested cwd did not yet exist; retried from fleet cwd with absolute mkdir, then used the unique scratch. Absolute wildcard glob/grep unexpectedly returned empty despite explicit reads/shell expansion finding files; reported to xd://report_issue and did not rely on empty outputs as absence evidence. An anchored `source: S004` search found no header because the legacy multi-source timeline entry has S003 in its header; S004 evidence was checked in the entry body instead.

No tools installed/updated; no pacman transaction, service restart, PATH/fleet/sibling write, git/jj mutation, commit or push. Scratch `/fast/scratch/hyaku/kasegi-r62/ScopeConnect` contained no clone/fixtures and is removed before yielding. Only durable seat write is this report.

Self-evaluation: accuracy 4 (bounded lexical rather than semantic exhaustive screen); completeness 4 (direct-child provinces, not all sibling corpora); clarity 4 (overlap table separates old concepts from the proposed distinction); actionability 4 (one row/column falsifier, integration deferred by contract); conciseness 4 (audit detail retained for reproduction). Average 4.0; improvement priority is to preserve the narrow novelty wording and bind complete matrix context at freeze. User-agreement self-check: this is a scoped recommendation, not self-admission.

Report: .ufo/waves/round-62/w1/ScopeConnect.md
