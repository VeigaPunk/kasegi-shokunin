VERDICT: INFO

Overlap scan only. F04 (`corpus/knowledge/ai-assisted-finding-validation.md`) already states Kasegi admission controls for an AI-originated finding. It does not state the Linux kernel security-bugs AI-reporting duties. Those duties are an add, carried by the pinned capture `corpus/source-snapshots/round-45/S071.txt` (docs.kernel.org/process/security-bugs.html). No reproducer is included below.

## Attacked

Question: what F04 already says about AI-assisted findings, and what S071 adds on public treatment, withheld reproducer, and the length / formatting / impact / reproducer / fix duties.

Identity of the kernel capture, re-run:

```
sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt
0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt
```

That digest matches `corpus/source-snapshots/round-45/manifest.json` S071 (`url` https://docs.kernel.org/process/security-bugs.html, `capture_url` https://docs.kernel.org/_sources/process/security-bugs.rst.txt, `bytes` 20152, `fetched_utc` 2026-10-28T20:52:44Z). S072 in the same manifest is https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section and is not the kernel doc.

## File inventory

`grep -il 'AI-'` on the knowledge directory does not walk it:

```
grep -il 'AI-' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge
grep: /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge: Is a directory
```

Exit code 2. The inventory command that does walk it:

```
grep -ril 'AI-' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge
```

printed exactly these seven paths (63 `*.md` files in that directory):

- `corpus/knowledge/mission-control.md`
- `corpus/knowledge/program-quirks.md`
- `corpus/knowledge/triage-thresholds.md`
- `corpus/knowledge/ufo-workspaces.md`
- `corpus/knowledge/ai-assisted-finding-validation.md`
- `corpus/knowledge/anthropic-cvd-provenance-and-pacing.md`
- `corpus/knowledge/cve-bench-agent-exploitation-benchmark.md`

`grep -rin 'AI-'` on the same directory printed the matching lines. Three files match only because `openai-` and `xai-` contain the case-insensitive substring `ai-`:

- `mission-control.md:56` `` `openai-codex/gpt-6-astra:max` ``
- `mission-control.md:57` `` `openai-oauth/` ``
- `mission-control.md:66` `` `xai-oauth/grok-4.6:low` ``
- `triage-thresholds.md:155` `` `openai-codex/gpt-6-astra:max` ``
- `triage-thresholds.md:156` `` `xai-oauth/grok-4.6:low` ``
- `triage-thresholds.md:438` `` `openai-codex/gpt-6-astra:max` ``
- `ufo-workspaces.md:21` `` `openai-codex/gpt-daybreak-blue-latest` ``
- `ufo-workspaces.md:89` `xai-oauth/grok…`
- `ufo-workspaces.md:101` `` `xai-oauth/grok-4.6:xhigh` ``
- `ufo-workspaces.md:238` `` `openai-codex/gpt-daybreak-blue-latest` ``

Those lines name fleet model pins. They say nothing about AI-assisted vulnerability findings.

## What F04 already says

F04 is `corpus/knowledge/ai-assisted-finding-validation.md`, sources S009–S012, recheck pinned to `corpus/source-snapshots/round-24/manifest.json` (`ai-assisted-finding-validation.md:2-4`).

Admission rule, not a vendor submission format (`ai-assisted-finding-validation.md:7-17`):

- `:7` "Treat an AI-originated finding as a candidate, not a confirmed vulnerability, until its evidence package records a reproducible observation and human validation of the claimed impact and reachability."
- `:8` Kasegi claim-ready status requires "the reproducing evidence and a reviewer distinct from its producer"; "a model assertion or benchmark result alone does not satisfy that check."
- `:10-16` record checks: code or package version; "separate model-generated hypotheses from observed reproduction results"; "connect the claimed impact to a supported reachability explanation"; reproducing evidence and independent review; reviewer distinct from the producer; "preserve any applicable program restriction or disclosure requirement."
- `:17` "If those facts are absent, preserve candidate status rather than describing the finding as confirmed."
- `:18` "These are Kasegi admission controls, not a claim that every cited source mandates one tool or workflow."

Cited support (`:20-26`): S009 says "look for ways to verify the results, by using both AI and humans." S010 limits "Perfect Verification" to structured tasks and limits benchmark conclusions versus "autonomous security research." S011 is Cloudflare's own "independent agent" disproof stage. S012 is Anthropic reproducing a Mythos finding and re-assessing severity, plus the capacity sentence "the bottleneck in fixing bugs like these is the human capacity to triage, report, and design and deploy patches for them."

Use and rejection (`:28-42`):

- `:30` program-rule checklist "records one observed rejection of AI-generated reports, not a universal ban."
- `:31` keep "severity language within demonstrated impact."
- `:34` rejected: "A model-generated report or a high benchmark score is proof that a vulnerability exists in a particular package."
- `:38` "S009 is operational guidance, not authorization to examine any system or codebase."
- `:42` "This entry describes review of documentation and evidence packages only; it does not direct probing, scanning, or submission."

F04 therefore already says: candidate until a human, distinct from the producer, validates a reproducible observation, impact, and reachability; benchmarks and model assertions do not confirm; one program has rejected AI-generated reports; the entry does not direct submission.

## What S071 adds

Assigned window `S071.txt:95-190` was read. The Length duty ends on line 190. Formatting, Impact Evaluation, Reproducer, and Propose a Fix are the next bullets of the same "Responsible use of AI to find bugs" section and were read at `S071.txt:192-219`. The assistant procedure at `:232-250` is the same section, outside the assigned window, and is cited as that continuation.

Public treatment and withheld reproducer, inside the window (`S071.txt:95-101`):

> If you resorted to AI assistance to identify a bug, you must treat it as public. … do not publicly share a reproducer … just mention that one is available and maintainers might ask for it privately if they need it.

Public-list exception, inside the window (`S071.txt:114-117`): do not send to a public list at this stage unless there are good reasons to consider the issue public or trivial to discover, "or use of AI-based tools."

Section premise, inside the window (`S071.txt:174-183`): a significant fraction of security-team reports come from AI-assisted code review; maintainers are sometimes forced to ignore them for poor quality; reporters must be cautious. `:221-222` (just past the window) says failure to consider the points risks the report being ignored.

Duties, kernel side versus the F04 line that is the nearest cousin:

| Duty | Kernel capture | Nearest F04 line | Same rule? |
|---|---|---|---|
| Treat AI-found bug as public | `S071.txt:95-97` must treat it as public; `:114-117` AI-based tools are a reason it may go to a public list | `:16` only "preserve any applicable program restriction or disclosure requirement" | No. F04 defers. It does not state the kernel public rule. |
| Do not share the reproducer | `S071.txt:99-101` do not publicly share a reproducer; mention that one is available | `:7` and `:14` require recording a reproducible observation and the reproducing evidence | No. F04 requires the evidence inside the package. It does not say to withhold a reproducer from publication. |
| Length | `S071.txt:185-190` AI-generated reports are excessively long; summary and critical details first; concise human-style reports | none | No. |
| Formatting | `S071.txt:192-196` Markdown tags do not survive quoting; "always convert your report to plain text" | none | No. |
| Impact | `S071.txt:198-204` stick to verifiable facts against `threat-model.rst`; do not enumerate speculative implications; example given is a capability fact, not a reproducer | `:7`, `:13`, `:31` claimed impact tied to reachability and demonstrated impact | Cousin only. Both resist inflated impact. F04's check is reachability in an evidence package. The kernel check is a threat-model-bounded fact list in the email. `threat-model` is absent from F04. |
| Reproducer quality | `S071.txt:206-211` the tool should provide one and the reporter must test it; if it does not work, or none is produced, question the report; share it only on maintainer request because the report is posted to a public list | `:8` distinct reviewer; `:12` hypotheses separated from observed results | No. F04 does not require a tool-generated reproducer, a thorough test of that reproducer, or private follow-up delivery. |
| Fix | `S071.txt:213-219` ask the tool to propose a fix and test it; untestable rare-hardware or extinct-protocol issues are likely not security bugs; a proposed fix follows `submitting-patches.rst` and includes a `Fixes:` tag | `:26` quotes S012 on human triage/patch capacity | No. That quote is Anthropic's capacity observation, not a duty to attach a tested fix. |

`S071.txt:232-237`, same section, outside the assigned window: at least have the assistant read this file and `threat-model.rst`, follow `coding-assistants.rst` (up-to-date mainline, commit ID, verify the bug is real, write a fix, warning-free and checkpatch-clean, `Fixes` tag, `get_maintainer.pl`). `:239-250`: the assistant must prepare a plain-text report with the four items named at `:20-47` (affected version or commit ID, description, reproducer or its status, triggering conditions), and start with a temporary recipient section the reporter removes. Those four items are the general report requirements at `:20-47`, not AI-only text. The AI section makes them mandatory content of the assistant's plain-text report.

## Other `AI-` knowledge files are not this add

- `anthropic-cvd-provenance-and-pacing.md:5` grounds itself on F02, not F04. `:60` quotes S016 "Reports originating from AI-powered discovery are clearly labeled as such." `:16` says nothing on that page "is a rule for other AI-assisted finders." `:99` already separates the rows: "F04 holds what a finder should verify before reporting (S009-S012) while L17 is about what the delivered report declares." That label-and-pace rule is Anthropic's outbound practice. It is not "treat the bug as public" and not the kernel length/plain-text/threat-model/tested-fix list. The duty-needle scan below includes this file.
- `cve-bench-agent-exploitation-benchmark.md:5` grounds itself on F04 and says it "adds the capability-measurement arm the validation entries (S009-S012) do not carry" and "keeps it distinct from a finding- or triage-accuracy claim." That is a benchmark rate, not a kernel reporting duty. `grep -rin 'AI-'` hit only this line in that file.
- `program-quirks.md:16` "AI-assist disclosure required — include it." `:60-61` "AI-content rejection clauses exist verbatim (SEEK: "low-effort or AI-generated content … will be rejected")." Provenance `:64-67` is `[lost-tree]`, verified-at 2026-09-28, recheck fails closed. Disclosure-required and a rejection clause are the opposite operational outcome from S071 accepting AI-assisted reports under format duties. F04:30 already records that rejection pattern as not a universal ban.

## Do-nothing control

Control C0: every `AI-` knowledge hit already states the kernel AI-reporting duties, so S071:95-190 adds nothing beyond F04.

C0 predicts the kernel duty strings occur in `ai-assisted-finding-validation.md` and that F04's admission strings occur in S071. Re-run:

```
NEEDLE treat it as public => NO MATCH
NEEDLE do not publicly share a reproducer => NO MATCH
NEEDLE excessively long => NO MATCH
NEEDLE plain text => NO MATCH
NEEDLE Impact Evaluation => NO MATCH
NEEDLE test it thoroughly => NO MATCH
NEEDLE Propose a Fix => NO MATCH
NEEDLE Fixes: => NO MATCH
NEEDLE coding-assistants => NO MATCH
NEEDLE threat-model => NO MATCH
NEEDLE get_maintainer => NO MATCH
NEEDLE Markdown => NO MATCH
```

Each needle was `grep -nF` against `corpus/knowledge/ai-assisted-finding-validation.md`. The same kernel needles `treat it as public`, `do not publicly share a reproducer`, `excessively long`, `Impact Evaluation`, `Propose a Fix`, `coding-assistants`, `get_maintainer.pl`, and `CAP_NET_ADMIN` were then `grep -rnF` across all of `corpus/knowledge`. Each printed `NO MATCH`.

Inverse, `grep -nF` against S071.txt:

```
NEEDLE candidate, not a confirmed => NO MATCH
NEEDLE reviewer distinct => NO MATCH
NEEDLE model-generated hypotheses => NO MATCH
NEEDLE Where should I start => NO MATCH
NEEDLE Mythos => NO MATCH
NEEDLE Perfect Verification => NO MATCH
NEEDLE Kasegi => NO MATCH
NEEDLE benchmark => NO MATCH
```

C0 fails. The shared topic is only that an AI-originated report is not self-certifying. The operative rules differ: F04 keeps candidate status until a distinct reviewer validates reproduction, impact, and reachability, and `:42` does not direct submission. S071 tells a reporter to treat the bug as public, withhold the reproducer, and meet length, plain-text, threat-model, tested-reproducer, and tested-fix duties before email. Putting the kernel duties into F04 would contradict F04:18 and F04:42. They belong on the kernel reporting row.

## Limitations

- Literal `grep -il` on the directory exits 2. The file list above is from `grep -ril`.
- `S071.txt:95-190` fully contains public treatment (`:95-101`), the public-list exception (`:114-117`), the section premise (`:174-183`), and the whole Length bullet (`:185-190`). Formatting (`:192-196`), Impact Evaluation (`:198-204`), Reproducer (`:206-211`), and Propose a Fix (`:213-219`) sit immediately after that window and were read because the seat named those duties. They are not inside lines 95-190.
- `:232-250` was read as the continuation of the same section. It is outside the assigned window.
- General (non-AI) report requirements at `S071.txt:20-47` already demand a version, a description, a reproducer, and conditions for every security bug. The AI section adds public treatment, reproducer withholding, and the format/test/fix duties on top of that. This scan did not inventory the rest of S071 (embargo, contact script, sending).
- No live fetch. Bytes are the pinned snapshot whose sha256 matched the manifest. S072 was identified and not used as the kernel source.
- `program-quirks.md` is a lost-tree note, not a pinned capture.
- No scratch directory was created (`/fast/scratch/hyaku/kasegi-r45/R45ScoutOverlapAI` absent). No fixture, no git mutation, no `/tmp` evidence.
- C2 counter was not run. This seat did not draft the F27 entry.
