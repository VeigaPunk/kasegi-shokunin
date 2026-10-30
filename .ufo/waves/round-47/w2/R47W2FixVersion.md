# R47W2FixVersion — integrated fix-version review

Axes: depth:verifiability; coverage.

Reviewed revision `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`. Scope: F29 two-versus-three-case correction and the ability-to-wait qualification. Recommendation only; no admission or native judgment.

## Findings — severity first

### Medium — the executable-in-prose package rule still rejects both acknowledged no-fix cases

`corpus/knowledge/github-repository-security-advisories.md:123-124,139-140` says a package is GitHub-conformant **only when all four** conditions hold, including that a fix version was added before publication. Its supporting quotation omits the source's opening `Whenever possible` at `corpus/source-snapshots/round-47/S076.txt:596`. G19 at entry `:46` similarly asks what the advisory **must** carry and repeats the shortened quotation.

This directly contradicts the repaired limits at entry `:110-113`, which identify two cases permitting publication without a fix and expressly prohibit describing a fix version as mandatory. Concrete static counterexamples:

- A fix is in development, the advisory says so, and it will be edited later: S076 `:599` explicitly contemplates publication, but condition 4 fails.
- No fix is planned and the advisory says so: S076 `:600` explicitly contemplates this case, but condition 4 fails.

Thus the local correction is present, but the downstream decision contract still discards it. This is an inherited defect retained and re-cited in the integrated revision, **not a newly introduced regression**; wave-1 review already disclosed it in `.ufo/waves/round-47/w1/R47RevD6.md:38`. Recommendation: qualify the package rule and G19 consistently with the source and the repaired limits; do not represent the entry's end-to-end fix-version semantics as repaired while these unconditional consumers remain.

## Correction disposition and bounded static attacks

| Static comparison | Evidence and disposition |
|---|---|
| Three cases all authorize publication without a fix | Corrected: entry `:111-112` identifies only S076 `:599-600`; source `:598` instead instructs waiting under its stated conditions. |
| Imminent fix, maintainer able to wait | Entry `:112` retains the complete quote, including `and you are able to`; the waiting instruction is located at S076 `:598`. Supported as a conditional recommendation. |
| Imminent fix, maintainer unable to wait | The antecedent at S076 `:598` is not satisfied. Entry `:112` must not be generalized into a prohibition applying to this case. Its full quotation preserves the qualification, so no independent missing-qualification finding is raised. The source does not supply a separate mandatory outcome for this counterfactual. |
| Fix in development but unavailable | Source `:599` supports the repaired limits; the unconditional package rule contradicts it as described above. |
| No fix planned | Source `:600` supports the repaired limits; the unconditional package rule contradicts it as described above. |
| Waiting advice mistaken for platform enforcement | Source `:596-598` gives graded advice, not a platform rejection rule; `:596` explicitly says an advisory without a fixed version will be published. Entry `:110-113` supplies the qualification; its word `forbids` is supportable only as shorthand for the conditional instruction, not technical enforcement. |
| Green L6 mistaken for semantic closure | `corpus/instruments/r47-routed-defects.py:213-223` checks an old-phrase regex, `two cases`, and the waiting substring. It neither checks `and you are able to` nor reconciles entry `:139-140` with the exceptions. Static predicate inspection cannot establish runtime results or semantic saturation. |

The integrated lesson's short Gate quote at `corpus/lessons/round-47.md:31` omits the antecedent, but the fuller historical erratum at `corpus/lessons/round-46.md:156` explicitly calls this the **qualified** imminent-fix instruction, and the current entry retains the full wording. Read the lesson shorthand with that qualification, not as an unconditional ban.

## Residual risk and verification gaps

- C1 remains not fully met and C2 remains unmet, as recorded at `corpus/lessons/round-47.md:57-65`. This review does not reroll either target, advocate rejecting historical S074, or manufacture F30 coverage.
- Literal text/diff evidence only: `read xd://lsp` returned `No such tool: xd://lsp`. Status, references, definition and diagnostics therefore could not be requested. Text searching is not semantic-reference proof.
- Executed: read-only `git diff` and `git show` to inspect the assigned committed entry and capture; file reads and scoped literal searches. The committed entry and S076 capture were read directly, not inferred from report claims.
- Runtime execution **unrun** under reviewer-role restrictions: no counter, selftest, mutant battery, fixture driver, source recheck, network capture or domain-target action. Static cases above are not executed tests or a claim of 32 completed attacks.
- No installs/updates, service restarts, delegation, production edits, git/jj mutations, or scratch directory. No scratch cleanup needed. Only this report is written.

## Self-evaluation

Accuracy 4/5: source and consumers cited directly; no live policy check. Completeness 4/5: bounded item and affected prose consumers covered; runtime intentionally unrun. Clarity 4/5: conditional repair separated from inherited contract defect, though the table repeats the two exceptions. Actionability 4/5: exact repair locations supplied; production edits prohibited. Conciseness 4/5: explicit static/executed boundaries add length. Overall 4.0/5. Highest-value improvement: reconcile the package rule with the exceptions before an authorized executor checks behavior. Would the user agree: expected, because the report distinguishes the requested safe repair from an honest remaining failure.

Report: .ufo/waves/round-47/w2/R47W2FixVersion.md
