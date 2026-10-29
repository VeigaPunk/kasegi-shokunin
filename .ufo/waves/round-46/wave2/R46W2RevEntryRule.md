# R46W2RevEntryRule — F28 entry verification (round 46, wave 2)

VERDICT: BROKEN

Scope: `corpus/knowledge/github-private-vulnerability-reporting.md` at lane commit 5437afeaf9b642c267bba3c31f00ae701e49da68 (working-tree sha256 `47028299d797e3326d05769338c844198a9d4069d9f1e1d3e00e69cf72d15036` = committed bytes; `git diff HEAD` empty for the entry and S073.txt). Covered: provenance header (lines 1-5), `## Falsifiable package rule`, and, because they carry the entry's other checkable claims, the Scope/decision paragraph, the decision table, the Overlap section, and the Limits section. Pinned capture: `corpus/source-snapshots/round-46/S073.txt` (589 lines).

BROKEN is because of statements that are stretched or overclaimed (F-1 to F-5 below), and because the falsifiable rule's central "observed" test is not operational (F-6). Every quote and cite checks out as text; the defects are in what the entry says those cites and checks establish.

## Checks run (all re-run by me)

1. Entry recheck line (entry line 5, shell comment `# 180d` dropped):
```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073
S073:sha256 OK
S073:Q1 OK occurrences=1 anchor=560-ok
S073:Q2 OK occurrences=1 anchor=563-ok
S073:Q3 OK occurrences=1 anchor=564-ok
S073:Q4 OK occurrences=1 anchor=566-ok
S073:Q5 OK occurrences=1 anchor=573-ok
S073:Q6 OK occurrences=1 anchor=574-ok
S073:Q7 OK occurrences=1 anchor=577-ok
S073:Q8 OK occurrences=1 anchor=578-ok
exit=0
```
2. Every curly-quoted string followed by an `S073.txt:N[-M]` cite in the entry, located by exact substring match against the capture (curly apostrophe normalised to `'` on both sides; script at `/fast/scratch/hyaku/kasegi-r46/R46W2RevEntryRule/quotecheck.py`, removed on exit). Full output:
```
ent:11 | “Owners and administrators of public repositories can enable private vu…” | S073.txt:561 | located=yes@[561] | in-manifest-recheck=no
ent:11 | “Private vulnerability reporting is separate from a repository’s SECURI…” | S073.txt:564 | located=yes@[564] | in-manifest-recheck=no
ent:11 | “You can only report vulnerabilities privately for repositories where t…” | S073.txt:564 | located=yes@[564] | in-manifest-recheck=yes
ent:17 | “You can only report vulnerabilities privately for repositories where t…” | S073.txt:564 | located=yes@[564] | in-manifest-recheck=yes
ent:18 | “Private vulnerability reporting is separate from a repository’s SECURI…” | S073.txt:564 | located=yes@[564] | in-manifest-recheck=no
ent:19 | “following the instructions in the security policy for the repository, …” | S073.txt:566 | located=yes@[566] | in-manifest-recheck=no
ent:20 | “By default, you must provide a summary, details, proof of concept, and…” | S073.txt:573 | located=yes@[573] | in-manifest-recheck=yes
ent:20 | “Maintainers can customize the form and require other information.…” | S073.txt:573 | located=yes@[573] | in-manifest-recheck=no
ent:21 | “Optionally, select I used AI assistance to find or write up this repor…” | S073.txt:574 | located=yes@[574] | in-manifest-recheck=yes
ent:22 | “GitHub automatically adds the reporter of the vulnerability as a colla…” | S073.txt:577 | located=yes@[577] | in-manifest-recheck=yes
ent:23 | “Note that only the repository maintainer can merge changes from that p…” | S073.txt:578 | located=yes@[578] | in-manifest-recheck=no
ent:24 | “GitHub will display a message letting you know that maintainers have b…” | S073.txt:575 | located=yes@[575] | in-manifest-recheck=no
ent:30 | “If a public repository has private vulnerability reporting enabled, an…” | S073.txt:565 | located=yes@[565] | in-manifest-recheck=no
ent:32 | “Anyone can privately report a security vulnerability to repository mai…” | S073.txt:560 | located=yes@[560] | in-manifest-recheck=yes
ent:33 | “admin or security permissions…” | S073.txt:563 | located=yes@[563] | in-manifest-recheck=no
ent:40 | “The next steps depend on the action taken by the repository maintainer…” | S073.txt:579 | located=yes@[579] | in-manifest-recheck=no
ent:41 | “Security and quality…” | S073.txt:568 | located=yes@[568] | in-manifest-recheck=no
ent:41 | “Report a vulnerability…” | S073.txt:569 | located=yes@[569] | in-manifest-recheck=no
ent:43 | “Creating a repository security advisory…” | S073.txt:563 | located=yes@[563] | in-manifest-recheck=no
ent:43 | “Coordinated disclosure of security vulnerabilities…” | S073.txt:566 | located=yes@[566] | in-manifest-recheck=no
ent:43 | “Managing privately reported security vulnerabilities…” | S073.txt:579 | located=yes@[579] | in-manifest-recheck=no
total quote+cite pairs: 21
```
   All 21 located. "in-manifest-recheck" = the entry's exact quote string appears in one of the manifest's Q1-Q8 quote assertions.
3. Entry's body sweep (Limits, line 40), run verbatim:
```
$ sed -n '556,583p' corpus/source-snapshots/round-46/S073.txt | grep -n -i -E "CVE|timeline|days|reward|bount|embargo|triage|authoriz|safe harbor|test|publish"
(no output) exit=1
```
   Whole-capture sweep (Limits, line 40), run verbatim: `grep -n -i -E "CVE|reward|bount|embargo|authoriz|safe harbor" corpus/source-snapshots/round-46/S073.txt` → no output, exit=1.
   Controls for the sweep: the same pattern on `maintainers respond within 30 days` prints `1:maintainers respond within 30 days`, exit=0 (sweep discriminates). Body grep `respon|hour|week|time|month` over 556-583 → no output, exit=1. Body grep for `private` prints lines 556-583 hits (positive control).
4. Recheck discrimination control (scratch copy only; sha256 and manifest rewritten in the copy, never in the tree): flipping "enabled" to "disabled" in the 564 sentence gives
```
S073:sha256 OK
S073:Q1 OK ...
S073:Q3 MISMATCH reason=quote-not-found
...
Command exited with code 1
```
   The real tree rerun after the control printed the eight OK lines above and exit=0. So the recheck does discriminate; it checks what it checks.
5. Cross-reference reads: `linux-kernel-security-bugs-reporting-process.md` lines 23-24, `ai-assisted-finding-validation.md` 1-15, `vendor-third-party-finding-coordination.md` 11-25, `authorization-safe-harbor-and-scope.md` 1-15.
6. Body-boundary and navigation checks: `awk 'NR<=555 && (/[.?!]$/ || /, /)'` over lines 1-555 → 0 lines. Lines 579-583 read as `The next steps depend ...` (579), `Back to top` (580), `Help and support` (581), `Was this Doc helpful?` (582), `YesNo` (583).
7. Overlap-novelty grep (`credited user|as a collaborator|maintainer-only merge|reporter-side` over corpus/knowledge): hits only in `cisa-cvd-program-stages.md:123` (a "self-description" note) and `linux-kernel-security-bugs-reporting-process.md:36`; neither records the GitHub collaborator, credited-user or merge effects.

## Statement table

`statement` | `cite` | `verified` | `evidence`

Header and recheck

| statement | cite | verified | evidence |
|---|---|---|---|
| L3 source URL = `docs.github.com/.../report-privately` | manifest S073 url | yes | manifest `"url": "https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately"` |
| L3 "Privately reporting a security vulnerability" heading is at 556 | S073.txt:556 | yes | line 556 = that heading |
| L3 "Its body is S073.txt:556-583" | S073.txt:556-583 | stretched | body prose ends at 579 ("The next steps depend ..."); 580-583 are "Back to top", "Help and support", "Was this Doc helpful?", "YesNo". The same range is repeated at L9 and Limits L39 |
| L4 verified-at 2026-10-28 | — | yes | today's date; manifest `fetched_utc` 2026-10-28T22:56:49Z |
| L5 `recheck:` line re-verifies the S073 capture | recheck output | yes (sha + Q1-Q8) | output in Check 1; exit=0 |
| Limits L44: "The recheck line re-verifies the capture's bytes and quotes" | — | stretched | recheck covers sha256 plus 8 quote assertions Q1-Q8; of the 21 cited quote pairs above, only 6 match a Q-string exactly, 14 are not among the Q1-Q8 strings, and the line-23 quote (578) is covered by Q8 only apart from its leading "Note that". See F-1 |

Provenance / decision paragraph (L9-L13)

| statement | cite | verified | evidence |
|---|---|---|---|
| "The source is one GitHub Docs page" | manifest | yes | one manifest row, one URL |
| "the rest of the capture is site navigation" | capture 1-555 and 580-589 | yes (heuristic) | no prose-like line in 1-555 (Check 6); capture lines 580-589 are chrome. Limitation: heuristic plus sampled reads, not a line-by-line read of 1-555 |
| "The entry does not record the maintainer-side flow" | — | yes | entry Limits L39; S073 body has no maintainer-side procedure |
| L11 "Owners and administrators of public repositories can enable private vulnerability reporting on their repositories." | S073.txt:561 | yes | located@561 (Check 2); recheck does not cover this quote |
| L11 "Private vulnerability reporting is separate from a repository's SECURITY.md file." | S073.txt:564 | yes | located@564; not in recheck |
| L11 "You can only report vulnerabilities privately for repositories where this feature is enabled." | S073.txt:564 | yes | located@564; recheck Q3 OK |
| L13 "A package may not describe the maintainers' response, the advisory's outcome or the fix's publication from this page, because the page does not state them" | body sweep | yes | Check 3: no `respon|publish|days` in body; the page's only forward pointer is L579 |

Decision table (L15-L24)

| statement | cite | verified | evidence |
|---|---|---|---|
| Row 17: enablement is the precondition | S073.txt:564 | yes | located@564; recheck Q3 OK |
| Row 18: SECURITY.md is separate | S073.txt:564 | yes | located@564; not in recheck |
| Row 19: fallback route is the policy or the issue | S073.txt:566 | yes | located@566; recheck Q4 covers only the prefix "you need to initiate ... for the repository" |
| Row 20: four default fields | S073.txt:573 | yes | located@573; recheck Q5 OK |
| Row 20: "Maintainers can customize the form..." | S073.txt:573 | yes | located@573; not in recheck |
| Row 21: AI-assistance flag is optional | S073.txt:574 | yes | located@574; recheck Q6 OK |
| Row 21: "Its absence is not a claim that no AI assistance was used." | — | not on page (entry's own inference) | labelled as package consequence; reasonable, but no source text supports it |
| Row 22: reporter becomes collaborator and credited user | S073.txt:577 | yes | located@577; recheck Q7 OK |
| Row 22: "The page does not state the collaborator's permissions" | body sweep | yes | no permission text about the reporter in 556-583; the only `collaborator` hits are nav links at 286-287 |
| Row 23: only the maintainer can merge from the fork | S073.txt:578 | yes | located@578 (sentence without leading "Note that"); recheck Q8 OK |
| Row 23: "A fork started by the reporter is a drafting step." | — | stretched | nothing in S073 calls the temporary private fork a drafting step; this is the entry's characterisation presented as a consequence |
| Row 23: "A package may say a fix is merged only when a maintainer's merge is observed." | S073.txt:578 | yes as rule | the rule follows from 578; it is the entry's own rule |
| Row 24: maintainers notified, pending credit message | S073.txt:575 | yes | located@575; not in recheck |
| Row 24: "The page gives no response time." | body sweep | yes | Check 3 `respon|hour|week|time|month` no match in 556-583 |

Overlap (L30-L35)

| statement | cite | verified | evidence |
|---|---|---|---|
| L30 kernel entry (F27) row says AI-assisted find is treated as public | linux-kernel:23 | yes | row 23: "you must treat it as public" |
| L30 kernel entry keeps its reproducer out of public text | linux-kernel:23 | stretched cite | that content is row 24 (`do not publicly share a reproducer`); row 23 does not say it. The claim itself is true, at :24 |
| L30 GitHub's page "answers the AI-assisted question differently" | S073.txt:565 | stretched | 565 says who may submit a private report, not how an AI find is handled; the entry itself says "The page gives no handling rule for a flagged report" in the same paragraph. The page does not answer the AI question at all |
| L30 "offers the AI-assistance flag only as an optional checkbox (S073.txt:574)" | S073.txt:574 | partly | "Optionally, select I used AI assistance..." is on the page; "checkbox" is not in the capture (outside wording) |
| L30 "The two sources differ on this point" | — | unsupported | no GitHub handling rule exists to differ from; see the row above |
| L31 ai-assisted-finding-validation.md:7-8: claim-ready needs reviewer distinct from producer | file 7-8 | yes | line 8: "a reviewer distinct from its producer" |
| L32 vendor-third-party-finding-coordination.md:17-19 holds intake routes | file 17-19 | yes | lines 17-19 hold the three MSVR intake routes (Microsoft's, not a generic "vendor's") |
| L32 "Anyone can privately report ... to repository maintainers" | S073.txt:560 | yes | located@560; recheck Q1 OK |
| L32 "names no coordinator" in the GitHub page | body sweep | yes | `coordinat` appears only as nav/link text (94, 566 link) |
| L33 authorization-safe-harbor-and-scope.md:8 | file 8 | yes | line 8: "does not add assets to scope or establish permission for an action that the program's policy excludes" (entry paraphrase drops "alone" and "add assets", which is harmless) |
| L33 "admin or security permissions" | S073.txt:563 | yes | located@563 |
| L35 novelty: none of the held entries records these as a reporter-side intake contract | grep | partly | grep (Check 7) finds no held entry recording collaborator/credited/merge effects; not an exhaustive read of all held entries |

Limits (L39-L45)

| statement | cite | verified | evidence |
|---|---|---|---|
| L39 "One page: the reporter-side steps at S073.txt:556-583" | — | stretched | same end-line issue as F-5 (body ends 579) |
| L40 body sweep prints nothing (grep exit 1) | body | yes | Check 3, re-run, no output, exit=1 |
| L40 whole-capture sweep prints nothing (grep exit 1) | capture | yes | Check 3, re-run, no output, exit=1 |
| L40 "The page's only pointer forward is 'The next steps depend...' (S073.txt:579)" | S073.txt:579 | yes | located@579; the three "See ..." links are at 561, 563, 566 and 579 |
| L41 "Reporter path begins at 'Security and quality' (568) and then 'Report a vulnerability' (569)" | S073.txt:568-569 | yes | located@568, @569 |
| L41 "The page does not say how a reporter observes enablement" | body | yes | no observation procedure in 556-583 (Check 3) |
| L42 "The enablement sentence names public repositories (561). The page says nothing about private repositories." | S073.txt:561 + body | yes for the body; caveat | body has no `private repositor` (Check 3 grep on body). The whole capture has one: line 445 `Private repository enablement` (nav link). Statement is true of the page body only |
| L43 three linked pages appear only as link text | 563, 566, 579 | yes | located@563/566/579 as link text |
| L44 quote checks are exact-text checks, not live | — | yes | matches the method used |
| L45 "Documentation only" | — | yes | no submission or probing step in the entry |

Falsifiable package rule (L49)

| statement | cite | verified | evidence |
|---|---|---|---|
| (1) package must record an observed enablement fact | S073.txt:564 | yes for the cite; the "observed" test is not operational | 564 supports "where this feature is enabled". Nothing in the entry says what counts as observation, and L41 concedes the page gives no method. See F-6 |
| (2) enablement absent: cite the policy route or issue fallback quoted at 566; must not describe as a private-reporting submission | S073.txt:566 | yes for the fallback; the "must not describe" clause is the entry's rule | 566: "you need to initiate the reporting process by following the instructions in the security policy for the repository, or by creating an issue asking the maintainers for a preferred security contact." |
| (3) a package naming the feature with neither fact fails | — | entry's rule; "neither fact" is ambiguous | see F-6 |
| merge clause: fix merged from reporter's fork fails unless maintainer's merge is recorded, "because only the maintainer can merge" | S073.txt:578 | yes | 578: "only the repository maintainer can merge changes from that private fork into the parent repository" |

## Falsifiability test (applied by reading the rule; not a mechanical run)

Package texts run through (1)-(3) and the merge clause:
- PASS: "Reported to example-org/example-lib through GitHub private vulnerability reporting. Enablement observed: private vulnerability reporting is enabled on the repository (S073.txt:564)." Passes (1); (3) not triggered.
- PASS (fallback): "Enablement not observed for example-org/example-lib; reported through the SECURITY.md policy route (S073.txt:566); no private-reporting submission made." Passes (2).
- FAIL: "Reported via GitHub private vulnerability reporting." No enablement fact and no fallback, so (3) fails it.
- FAIL: "Enablement not observed; submitted via GitHub private vulnerability reporting." (2) fails it: the package describes a private-reporting submission while enablement is absent.
- FAIL: "Enablement observed (S073.txt:564). Fix merged from the reporter's private fork." The merge clause fails it: no maintainer merge recorded.
- PASS but unverified: "Reported via GitHub private vulnerability reporting. Enablement: observed." It passes (1), because the rule only checks that a record exists. Nothing distinguishes it from a fabricated record. See F-6.

So the rule is falsifiable on presence and absence of a record, and it is not falsifiable on whether the enablement observation is true.

## Findings

F-1 (overclaim, Limits L44 and L5). The entry says the recheck "re-verifies the capture's bytes and quotes" and gives it as the check on "quotes". The recheck covers the sha256 and eight assertions, Q1-Q8. In the 21 cited quote pairs, 14 quoted sentences are not among Q1-Q8 (561; 564 SECURITY.md sentence at L11 and L18; 566 "or by creating an issue..." at L19, only the prefix is covered; 573 "Maintainers can customize..."; 565; 563 admin sentence; 575; 579 at L40; 568; 569; 563 link; 566 link; 579 link). Line 23's 578 quote is covered by Q8 only without its leading "Note that". Evidence: Check 1 and Check 2 output. The quotes themselves are all located (Check 2), so the defect is the overclaim about what the recheck tests.

F-2 (stretched, L30). "GitHub's page answers the AI-assisted question differently" cites S073.txt:565. Line 565 is about who can submit a private report. The page has no AI-handling rule (the entry's own Limits and the same paragraph say so). "Checkbox" is not on the page ("select"). "The two sources differ on this point" has nothing to differ with.

F-3 (stretched cite, L30). The kernel row cited as `linux-kernel-security-bugs-reporting-process.md:23` supports the "treat as public" claim, but the reproducer claim is at `:24`. Claim true; citation incomplete.

F-4 (stretched, decision table row 23). "A fork started by the reporter is a drafting step." is not in S073. It is the entry's characterisation, presented beside the page quote as a consequence.

F-5 (stretched range, header L3, L9, L39). "Its body is S073.txt:556-583" is wrong at the end: prose ends at 579. 580-583 are "Back to top", "Help and support", "Was this Doc helpful?", "YesNo". Minor, but the header's cite range does not match the body it names.

F-6 (falsifiability gap, rule L49). Step (1) requires "an observed fact" that enablement is on, but the entry never says what counts as observation, and L41 concedes the page gives no way to observe it. The rule therefore checks that a record is written, not that it is true (PASS-but-unverified example above). Step (3)'s "neither fact" is ambiguous: it could mean neither enablement fact nor fallback citation, or neither of two conditions in (1) and (2). The trigger "states that a vulnerability was reported through..." also misses packages that describe the route without the past-tense claim. These do not invalidate the citations; they limit how far the rule can be falsified.

Items verified with no defect: all 21 quote/cite pairs located; the entry's recheck exits 0 with the eight OK lines; body and whole-capture sweeps print nothing (exit 1) with a working positive control; the 566 fallback quote; the 578 merge quote; the 564 enablement quote; the ai-assisted-finding-validation, vendor, and authorization cross-refs; the verified-at date.

## Limitations

- The falsifiable-rule examples are my own texts run through the rule by reading it, not by a program. No mechanical checker exists for the rule.
- Quote location is exact substring match after curly-apostrophe normalisation. I did not check the entry's curly apostrophe against the source's by byte, beyond that normalisation.
- "The rest of the capture is navigation" was checked by a 100-character/punctuation heuristic and targeted greps, not by reading lines 1-555 one by one.
- The overlap novelty claim was checked by one grep over corpus/knowledge, not by reading every held entry.
- Entry rows and Scope paragraphs were checked as statements; I did not run the other entries' recheck lines beyond the ones cited here.
- Nothing was committed, staged or edited. The recheck and quote check are read-only; the mutation control ran only on a copy in scratch, removed on exit.
