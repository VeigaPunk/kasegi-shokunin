# R47W2Chrome — integrated F29 prose/chrome boundary

Axes: **depth:verifiability**, **coverage**. Static review only; recommendation, not admission.

Reviewed integrated commit `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; frozen assignment `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`. Scope is F29 entry lines 11 and 89 against S076, not the other lifecycle assertions or the complete C1/C2 gates.

## Findings by severity

**No actionable new prose/chrome assertion remains in this scope.** The wave-1 low-severity off-by-one finding is repaired, not merely hidden by a mechanical pass.

| Integrated assertion | Source evidence | Disposition |
|---|---|---|
| `corpus/knowledge/github-repository-security-advisories.md:11`: prose “spans S076.txt:558-600” inside a capture carrying navigation, Copy markdown, TOC and footer | `corpus/source-snapshots/round-47/S076.txt:558` is the summary; :559 is literally `Copy markdown`; :561 is the availability statement; :562-565 is the TOC; :600 is the final policy paragraph | Supported as an enclosing span, not a claim that every intervening line is prose. The sentence explicitly acknowledges interleaved chrome. Its examples are introduced by “such as,” not as an exhaustive list. |
| Entry :89: chrome explicitly includes `S076.txt:562-565` | Source :562 is `In this article`; :563-565 lists the three section titles; :566 repeats `About repository security advisories` immediately before the substantive paragraph :567 and definition :568 | Correct boundary. The integrated range stops at :565 and does **not** misclassify :566. [INFERENCE from captured ordering] :566 is the article body heading; :563 is its TOC occurrence. |
| Entry :11 and :89: footer examples `S076.txt:601-610` | Source :600 ends the fix-version discussion; :601 begins `Back to top`, followed by help, feedback, contribution, support and corporate links through :610 | Supported. No policy paragraph is swept into this footer range. |
| Entry :89: “The prose is S076.txt:558-600” | The same sentence explicitly excludes :559 and :562-565 as chrome within that interval | In context this identifies the prose-containing window, not homogeneous prose on all 43 lines. It does not recreate the base's assertion that the whole capture is body prose. |

The do-nothing base sentence, visible in the committed diff at entry :11, said “its body prose is S074.txt:1-42 and the whole capture is that body.” The integrated sentence removes that universal claim and names concrete chrome. Wave-1 evidence `.ufo/waves/round-47/w1/R47RevD6.md:7-13` specifically identified the draft's `562-566` range; actual committed entry :89 now uses `562-565`. This disposition comes from the integrated bytes and S076, not from accepting that earlier report's verdict.

## Executed evidence versus unrun execution

Executed read-only repository inspection:

- `git diff fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8 65e19bdb142c90a08103eb4b2af60c71218a920e -- corpus/knowledge/github-repository-security-advisories.md`
- `git show 65e19bdb142c90a08103eb4b2af60c71218a920e:corpus/knowledge/github-repository-security-advisories.md`
- `git show 65e19bdb142c90a08103eb4b2af60c71218a920e:corpus/source-snapshots/round-47/S076.txt`
- Line-numbered file reads at the entry, source boundaries, round-47 lesson and prior scoped report.

`read xd://lsp` returned `No such tool: xd://lsp`; status/references/definition/diagnostics are unavailable. Literal file inspection is not semantic caller proof. No runtime, counters, selftests, mutation battery, live fetch or domain-target action was run. No mechanical gate result is asserted.

## Residual risk and verification gaps

- Plaintext loses HTML structure; the :566 body-heading classification is inferred from the duplicate TOC label followed by its paragraph, not independently established from an HTML DOM. The integrated repair is consistent with that distinction.
- The wording “The prose is” at entry :89 is less explicit than “prose occurs within …, excluding the chrome listed here,” but its immediate exclusion list prevents a new false blanket assertion. This is not promoted into a defect or a required production edit.
- `corpus/instruments/r47-routed-defects.py:190-199` statically checks two forbidden phrases and the word `chrome`; it does not classify source lines. Even an eventual green L4 cannot prove these boundary claims or saturation. This seat claims neither full coverage nor 32 attacks: it supplies one bounded integrated review item with the independent checks above.
- Frozen targets remain unchanged: C1 is not fully met because the frozen S074 rejection conflicts with B3; S074 remains mined historical. C2 is unmet: no F30 row, ZDI retained as F02 enrichment. These are the integration decisions documented at `corpus/lessons/round-47.md:57-69`, not targets rerolled by this report. The narrow chrome repair does not cure either failure.
- Canonical-runtime, rerouting and resume-preflight behavior are outside these two documentation assertions; no conclusions about them are drawn.

No tools installed or updated; no scratch directory created; no source captures or shared production files changed. Only this report is written.

Self-evaluation: accuracy 4/5 (plaintext heading inference lacks DOM evidence); completeness 5/5 (both assigned assertions, TOC/body transition and footer boundary examined); clarity 4/5 (distinguishing window wording from universal wording requires context); actionability 5/5 (exact repaired range and remaining verification boundary identified); conciseness 4/5 (retains static provenance and scope qualifications). Overall 4.4/5. Highest-value improvement would be historical DOM evidence, if available, rather than rerunning a lexical gate. Self-check: the report does not imply full C1/C2 success from a local repair.

Report: .ufo/waves/round-47/w2/R47W2Chrome.md
