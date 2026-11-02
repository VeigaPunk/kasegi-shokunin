# Round61 — root-cause evidence assessment

C1 only: lowest depth:verifiability nominal capability (R58), score4 held.
Base6670dfe4604f893e6ad0000cc94b5b6f390069e5; freeze03e87089ece1d76fb919bc14b1c88e868b441462;
first answers fe875cc9b4fce87e1242cc882314a184ee742f31. Existing F05 ranking
caution/crosswalk is preserved. New dossier absence, not invented bad accuracy,
motivates the round (controls/before.txt).

## Gate

Official MITRE guidance and eight entry pages opened2026-11-02. Nine URLs,
ten scoped decisions: S098–S106 admitted for definitions/notes; S107 rejects
119 as universal crash fallback. Same capture method for admits/reject. No prior
status/recheck/used-by changed; new rows are A/docs in limited stated scope.
The table below gives located quotes. Counts use len(quote.split()) over the
corrected manifest; S107 reuses S102 evidence, not a new source.

| Source | URL / capture location / quote / words | Decision |
|---|---|---|
| S098 | https://cwe.mitre.org/documents/cwe_usage/guidance.html — S098.txt:69, “They describe the result of the vulnerability and its attack vectors, not the root cause(s).” — 15 words | admit scoped definition/mapping guidance |
| S099 | https://cwe.mitre.org/data/definitions/190.html — S099.txt:584, “Integer overflows can be primary to buffer overflows when they cause less memory to be allocated than expected.” — 18 words | admit scoped definition/mapping guidance |
| S100 | https://cwe.mitre.org/data/definitions/131.html — S100.txt:83, “The product does not correctly calculate the size to be used when allocating a buffer.” — 15 words | admit scoped definition/mapping guidance |
| S101 | https://cwe.mitre.org/data/definitions/787.html — S101.txt:574, “Consider the root cause errors that have led to the out-of-bounds write by examining "CanFollow" relationships for this entry.” — 19 words | admit scoped definition/mapping guidance |
| S102 | https://cwe.mitre.org/data/definitions/119.html — S102.txt:769, “this CWE ID should not be used to map to real-world vulnerabilities” — 12 words | admit scoped definition/mapping guidance |
| S103 | https://cwe.mitre.org/data/definitions/20.html — S103.txt:764, “this CWE ID should not be used to map to real-world vulnerabilities” — 12 words | admit scoped definition/mapping guidance |
| S104 | https://cwe.mitre.org/data/definitions/79.html — S104.txt:2, “Improper Neutralization of Input During Web Page Generation” — 8 words | admit scoped definition/mapping guidance |
| S105 | https://cwe.mitre.org/data/definitions/862.html — S105.txt:472, “Examine children of this entry to see if there is a better fit” — 13 words | admit scoped definition/mapping guidance |
| S106 | https://cwe.mitre.org/data/definitions/863.html — S106.txt:436, “Examine children of this entry to see if there is a better fit” — 13 words | admit scoped definition/mapping guidance |
| S107 | https://cwe.mitre.org/data/definitions/119.html — S102.txt:769, same 12-word S102 quote above | reject universal crash fallback; flip requires causal evidence and appropriate permitted mapping |

Source hashes bind normalized captures, not meaning. Interruption after S098/S099
had unknown cause; manifest note distinguishes resume timestamp from first fetch.
Missing pages resumed with read-only timed curl; no denied action retried.

## Understanding and first-pass demonstration

The entry distinguishes190 arithmetic wrap,131 size and787 resultant writing;
862 absent versus863 incorrect permission checks;79 web-output neutralization;
119/20 discouraged shortcuts. Class862/863 require child review, not automatic
rejection solely for abstraction. Causal roles, not familiar words, determine fit.
R67 transfers: observed possession/impact is not a mechanism or necessary condition.

Only independent challenge.json was read before first-answer seal. Ten manual
assessments and12 mapping records are work counts, not12 factual successes.
`python3 -c 'import json; a=json.load(open(".ufo/waves/round-61/first-answers.json")); print(len(a),sum(len(x["selected_mappings"]) for x in a))'`
First-answer SHA2564b36e8be40f26836431f4f60c244d222ad561fa281578aba51c7525272a8a54c.
Parent-appointed `/root/judge_kasegi_round61` reports10/10 first cases supported;
final teaching/source/no-harm review pending. No answer changed after feedback.
Correctness requires independent causal/acceptable-set review, not schema/labels.
Constant79, keyword and ranking controls are deliberately bad policies, not a
claimed historical baseline. Rejected59 remains rejected, never rescued by61.

## Mistakes

| Class | Evidence | Captured-by | Fix and demonstrated failure |
|---|---|---|---|
| vacuous | Frozen S102/S103 quotes were single DISCOURAGED tokens; controls/source-check.txt reports quote-too-short-to-be-evidence, exit2 | source-recheck and Q3/R48 | Separate correction manifest has located usage sentence; same checker exit0. Frozen manifest/captures unchanged. |
| landing | Correction manifest first placed beside frozen manifest; controls/capture-binding-red.txt rejects orphan-capture, exit1 | capture-binding-check and R54 non-harm | Relocate correction with exact copies into wave/source-correction01; same gate exit0. Original location remains in commitfe875cc, red evidence retained. |
| provider | First lesson-building heredoc had an unterminated f-string and exited1 before any lesson write | Python syntax error | Recreated lesson with separated text/quote generation; no partial lesson or claimed successful run retained as evidence. This is tooling recovery, not a semantic capability claim. |

Corrected manifest now `.ufo/waves/round-61/source-correction01/manifest.json`;
source-check-relocated.txt and capture-binding-restored.txt record green results.
No duplicate QUALITY rule added: existing criteria already catch these mistakes.

## Roles, no-harm and census

One author sequentially performed planner/gap, connector/overlap, scout/sources,
analyst/manual assessment, critic/substitutes and scribe/lineage passes. Reviewer
is fresh and parent-appointed, not author-dispatched; no pretend8-agent swarm.
Census-before.txt original parser exits0; final receipt carries after parser,
row/tier/status counts and exit codes. Committed export guard preserves historical
prefixes, rows, frozen inputs and first answers; inherited host-bound failures
remain named. Raw density measured, not hidden by holding score9. Final acceptance
pending outside review; no new F-row, target, promotion or62.

Own staging error: explicit git-add included the old relocated path and failed;
commit4df8045 therefore contained only the previously staged rename, despite a
broad message. Following commit lands the teaching and this correction; no amend.
The uncommitted S107 annotation13 was corrected to measured12 (`wc -w` over
its quote); the quote text itself did not change. Existing R56 applies.

Final-preflight review found another own metadata defect: the new knowledge-
expected row omitted its corpus/knowledge/ prefix. The inherited recheck exit1
masked it if read only as an exit; its output explicitly reports missing1 and
unexpected1. Corrected the inventory row and added exact set equality to the
final guard, so this defect cannot hide behind the expected inherited failure.
Preflight58cc325 is retained. Raw density245.7→240.6 (41→42 blocks), old SKILL
prefix intact; no density padding or numeric score gain. Outside no-harm judgment
is still required. Source census97→107 (A87→97, B5/C5 held; mined76→85,
rejected21→22), original parser before/after exits0. Counting expression:
`rows=[x.split('|') for x in text.splitlines() if re.match(r'^\| S\d+ \|',x)]`;
tier/status Counter on stripped columns4/8, over git-show base6670dfe and tip.

## Outside no-harm rejection at770ed01 and authorized repair

Reviewer `/root/judge_kasegi_round61` found the new recheck failed existing Q10:
its command only resolved from the lane cwd, and its wave-manifest form failed
strict own-source binding. The original frozen condition requires every first
case AND non-author no-substantive-harm certification. No waiver covers this new
failure. Therefore770ed01 was NOT ADMITTED despite10 supported first semantic
cases; quality/operability harmed as shipped. Original report e3c92712… is retained
byte-for-byte in wave/report-before-operability-repair.md, as are all red receipts.

Parent explicitly authorized a bounded operability repair before final closure.
Only the new entry's recheck line changes (same line number); original command
is appended as history. It enters the real lane and checks exact source IDs, with
corrected quote manifests for S102/S103 in a new ordinary source-snapshot folder;
old source rows, frozen manifest/captures, challenge, oracle and answers unchanged.
The new snapshots are exact copies, not new source discoveries/registry credit.

Actual `python3 .ufo/waves/round-61/operability-replay.py` reports strict111111,
lane0/foreign0 with identical output hashes. It executes the documented command
from the lane AND /tmp, not merely a static syntax test. The same retained source
checker rejects corrupted S102 bytes (exit1) and missing bytes (exit2). Capture-
binding check returns0. This demonstrates repair and its limits; no semantic
rescore or retrospective claim that770ed01 passed. Final non-author re-review is
pending. No new criterion needed: Q10 already specified cwd independence.
