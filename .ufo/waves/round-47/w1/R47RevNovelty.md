# R47RevNovelty — F30 novelty review

Axes: depth:verifiability; coverage. Recommendation only; no admission or integration judgment.

## Findings by severity

### Medium — the exact novelty sentence foregrounds facts reducible to F02

Reviewed draft: `.ufo/waves/round-47/w1/R47SrF30Entry.draft/zdi-disclosure-policy.md`, read snapshot D642. Its line 26 says:

> Its novelty is the broker's conditional publication branches for acquired findings, rare discretionary extensions, and faulty-patch 30/60/90-day windows.

The capture supports the listed policy facts: `corpus/source-snapshots/round-47/S075.txt:23-25` supplies contact/publication branches, rare sole-discretion extensions and the faulty-patch windows; line 26 explicitly mentions an acquired vulnerability. However, support for facts is not support for their claimed irreducibility. F02 already requires the policy owner, clock trigger, interval, patch/publication relationship and exceptions (`corpus/knowledge/coordinated-disclosure-timelines.md:7-17`), including unknown dates when the trigger is unstated. A new attributed timeline with exceptions fits that existing rule exactly. The prior rejection expressly acknowledged the ZDI clock/extension overlap (`corpus/lessons/round-46.md:25`). The later-round reopening flip there permits reconsideration; it does not itself establish a new ground.

**Strongest reduction attack:** keep the ZDI conditional timeline as another F02 policy comparison. Use F15's existing party/role discipline to label ZDI rather than Microsoft as the coordinator. Different owner, interval values, publication conditions and exceptions do not by themselves require frontier 30. The draft's accurate missing-start-event rule (line 7) is an application of F02:16, not a new rule.

**Wording that defeats the narrow clocks/intake reduction:** replace the quoted novelty sentence with the following explicit residual (proposed wording only):

> The residual beyond F02 is ZDI's stated refusal to suppress an acquired vulnerability merely because its product vendor declines to address it (`S075.txt:26`); the timelines and extensions instantiate F02 rather than constitute that residual. F15 records Microsoft's intake routes and roles, not this stated disposition commitment for acquired findings.

This is supported by the exact source sentence at `S075.txt:26`: “In no cases will an acquired vulnerability be \"kept quiet\" because a product vendor does not wish to address it.” The draft already paraphrases that commitment at line 22, but fails to make it the discriminating feature at line 26. This wording defeats reduction to a *clock comparison alone* or an *intake-route description*; whether that residual merits a separate frontier remains a coverage-granularity decision, not something this capture proves. No claim about how acquisition occurs, payment, ownership transfer, or a clock beginning at acquisition is supported here.

## F15 and F10 comparison

F15 is not an adequate substitute for the acquired-finding disposition commitment: it enumerates Microsoft's three arrivals into coordination (`corpus/knowledge/vendor-third-party-finding-coordination.md:17-39`) and its own vendor/finder/coordinator roles (41-59). It explicitly states that the capture supplies no timeline or coordination agreements (114-120). Its frontier row similarly says not to read clocks, contact or agreements into intake (`corpus/README.md:309`). Thus F15 supplies reusable role discipline, not the ZDI policy consequence. Conversely, merely calling an actor a broker is not enough to escape F15's general coordination vocabulary.

F10's row describes vendor first-party policy objects and their intake/handling/disclosure conditions (`corpus/README.md:211`). That is adjacent policy-reading practice, not evidence that a separate broker ground exists. The defensible residual is the stated handling of an *acquired* finding when the product vendor declines remediation, not the fact that the source is a policy page.

## Do-nothing discrimination

Named frozen counter control: `.ufo/waves/round-47/controls/c2-base.txt:1-9` records rows=29, entry absent, and `f30-gate fixed=1/7 exit=1` / `EXIT=1`. This review did not rerun that counter and makes no improvement/pass claim.

Semantic do-nothing comparator: retain F02 and F15 unchanged and add no F30. The draft's clock-owner, interval, exception and unknown-trigger requirements remain expressible through F02. What that comparator does **not** hold in the inspected F02/F15 text is ZDI's particular acquired-vulnerability non-suppression commitment. That is the concrete information delta to argue, not a row number or a gate score.

## Residual risk and verification gaps

- S075 proves the published captured commitment, not actual ZDI conduct, acquisition mechanics, or current-page freshness. The draft correctly scopes these out at line 30.
- Novelty review is confined to the requested F02/F15 entries, F10/F15 rows, draft and pinned capture; it is not an exhaustive corpus-wide absence proof.
- `read xd://lsp` returned `No such tool: xd://lsp`; semantic references/definitions/diagnostics were unavailable. Text reads/searches here are literal documentary evidence, not LSP semantic proof.
- No runtime, build, test, mutation battery or network check was invoked. Known disclosed battery survivors remain unresolved; no saturation claim is made.
- No production file or git/jj state was changed. No tools installed. No scratch directory or fixture was created, so no scratch remains.

## Subsequent disposition

After this review, `R47SrF30Entry` reported applying the proposed narrow residual at draft line 26 (snapshot 303D), adding F15:114-120 and acquisition/purchase/ownership/actual-conduct limits. This is the author's reported resolution, not an independent reread of the updated draft. The medium finding above describes reviewed snapshot D642; carry the residual granularity risk forward rather than treating that superseded wording as an outstanding confirmed defect.
