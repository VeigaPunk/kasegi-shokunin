VERDICT: BROKEN

Scope: `corpus/knowledge/github-private-vulnerability-reporting.md`, sections `## Overlap and novelty` (L26-35) and `## Limits` (L37-45), against the pinned capture `corpus/source-snapshots/round-46/S073.txt` (sha256 66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930, byte-identical to the lane copy) and the four held entries. Lane tree at HEAD 0d121a2; read-only; no lane files changed.

## Method
- (a) Quote check: every curly-quoted string in L26-45 was extracted by script and substring-matched (exact, `in`) against every line of S073.txt; the matching line was compared with the cited `S073.txt:N`. Output (`quotes.py`):
```
entry:30 | cite=565 | hits=[565] | LOCATED@cite | 'If a public repository has private vulnerability reporting enabled, anyone can submit a private vulnerability report to the repository maintainers.'
entry:32 | cite=560 | hits=[560] | LOCATED@cite | 'Anyone can privately report a security vulnerability to repository maintainers.'
entry:33 | cite=563 | hits=[563] | LOCATED@cite | 'admin or security permissions'
entry:40 | cite=579 | hits=[579] | LOCATED@cite | 'The next steps depend on the action taken by the repository maintainer.'
entry:41 | cite=568 | hits=[555, 568] | LOCATED@cite | 'Security and quality'
entry:41 | cite=569 | hits=[569] | LOCATED@cite | 'Report a vulnerability'
entry:43 | cite=563 | hits=[563] | LOCATED@cite | 'Creating a repository security advisory'
entry:43 | cite=566 | hits=[566] | LOCATED@cite | 'Coordinated disclosure of security vulnerabilities'
entry:43 | cite=579 | hits=[579] | LOCATED@cite | 'Managing privately reported security vulnerabilities'
```
- Cited lines printed with `sed -n 'Np'`: 560 "Anyone can privately report a security vulnerability to repository maintainers."; 561 "Owners and administrators of public repositories can enable private vulnerability reporting on their repositories. See Configuring private vulnerability reporting for a repository."; 563 "If you have admin or security permissions for a public repository, you don’t need to submit a vulnerability report. Instead, create a draft security advisory directly. See Creating a repository security advisory."; 565 "If a public repository has private vulnerability reporting enabled, anyone can submit a private vulnerability report to the repository maintainers."; 568 "Under the repository name, click the Security and quality tab. ..."; 569 "Click Report a vulnerability to open the advisory form."; 574 "Optionally, select I used AI assistance to find or write up this report."; 579 "The next steps depend on the action taken by the repository maintainer. See Managing privately reported security vulnerabilities."
- (b) Cross-refs opened with `grep -n ''` at the cited lines (see table).
- (c) Sweeps re-run exactly as the entry prints them:
  - Body: `sed -n '556,583p' .../S073.txt | grep -n -i -E "CVE|timeline|days|reward|bount|embargo|triage|authoriz|safe harbor|test|publish"` → no output, `exit=1`.
  - Whole capture: `grep -n -i -E "CVE|reward|bount|embargo|authoriz|safe harbor" .../S073.txt` → no output, `exit=1`.
- (d) Beyond-page sentences identified by reading each sentence against the page.

## Controls (discriminate sweeps and quote checks from a do-nothing pass)
- Negative: `grep -c -F "Maintainers respond within 7 days of a report." S073.txt` → `0`, `exit=1` (fabricated claim not located).
- Positive, sweep pattern: `echo "CVE-2026-0001 assigned after 14 days, bounty paid" | grep -n -i -E "CVE|timeline|days|reward|bount|embargo|triage|authoriz|safe harbor|test|publish"` → `1:CVE-2026-0001 assigned after 14 days, bounty paid` (the sweep does match when the words are present).
- Positive, body window: `sed -n '556,583p' S073.txt | grep -c -i "maintainer"` → `9`; whole capture `grep -c -i "anyone"` → `3`.
- Wrong-cite control: the 560 quote checked at 566 → `0`, `exit=1` (quote is cite-sensitive).
- Recheck run on a copy of `corpus/` (`cp -a`, scratch, not the lane): `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073` → `S073:sha256 OK`, `S073:Q1 OK occurrences=1 anchor=560-ok` … `S073:Q8 OK occurrences=1 anchor=578-ok`, `exit=0`. The manifest pins exactly eight quotes: Q1 560, Q2 "create a draft security advisory directly" (563), Q3 564, Q4 566 (partial), Q5 573, Q6 574, Q7 577, Q8 578.

## Table: statement | cite | verified | evidence

| # | statement (abridged) | cite | verified | evidence |
|---|---|---|---|---|
| 1 | F27 kernel row "treats an AI-assisted find as public" | linux-kernel-security-bugs-reporting-process.md:23 | yes | line 23: "If you resorted to AI assistance to identify a bug, you must treat it as public" |
| 2 | kernel "keeps its reproducer out of the public text" | kernel :23 | yes, cite should be :23-24 | the reproducer row is line 24 ("do not publicly share a reproducer…"; "keep it out of the public text"); line 23 alone does not show it |
| 3 | GitHub's 565 sentence is quoted as GitHub's answer to "the AI-assisted question" | S073.txt:565 | yes (quote), **stretched** (use) | quote located at 565 verbatim, but 565 is about private reports from anyone; it contains no AI statement |
| 4 | "GitHub's page answers the AI-assisted question differently" | S073 565/574 | **stretched** | `grep -n -w "AI" S073.txt` → only 555 (nav "Security and quality AI features") and 574 ("Optionally, select I used AI assistance…"). The page takes no position on AI-found reports; the entry attributes one to it |
| 5 | flag offered "only as an optional checkbox" | S073.txt:574 | yes | line 574 "Optionally, select I used AI assistance to find or write up this report." (only body occurrence) |
| 6 | "The page gives no handling rule for a flagged report" | S073 (sweep) | yes | body 556-583 read in full; the only AI mention is 574; no handling text |
| 7 | "The two sources differ… neither source's policy is the other's"; "kernel rule does not describe GitHub's form…" | F27 :23-24; S073 | yes (comparative inference) | both sources read; the comparison is the entry's own judgement |
| 8 | ai-assisted-finding-validation.md:7-8: claim-ready needs reviewer distinct from producer | ai-assisted :7-8 | yes | line 8: "For Kasegi claim-ready status, the package must identify the reproducing evidence and a reviewer distinct from its producer…" |
| 9 | "GitHub's flag is a disclosure checkbox. It records no validation, so this entry records no reviewer." | S073.txt:574 | yes (inference label "disclosure") | line 574 is an optional checkbox; nothing on validation in the page |
| 10 | vendor-third-party-finding-coordination.md:17-19 "holds intake routes for a vendor's programme" | vendor :17-19 | yes, cite range imprecise | lines 17-19 hold the heading "Claim 1 — Microsoft's MSVR states three intake routes…" and the lead-in; the three routes are in the table at lines 26-28 (not cited) |
| 11 | GitHub names "one recipient class": "Anyone can privately report…" | S073.txt:560 | yes | line 560 verbatim |
| 12 | "It names no coordinator for a multi-party finding" | S073 (sweep) | yes | `sed -n '556,583p' S073.txt \| grep -n -i -E "coordinat\|multi\|vendor\|contact\|third"` → only line 11 of window (= S073:566, "See Coordinated disclosure of security vulnerabilities.", a link) |
| 13 | vendor entry holds routes; "coordinator-of-record field has no value" | vendor | yes (inference) | the page has no coordinator field; judgement about the corpus schema |
| 14 | authorization-safe-harbor-and-scope.md:8 | auth :8 | yes | line 8: "A safe-harbor badge or statement alone does not add assets to scope or establish permission for an action that the program’s policy excludes." |
| 15 | "admin or security permissions" concerns who may create a draft advisory | S073.txt:563 | yes | line 563: "If you have admin or security permissions… create a draft security advisory directly." |
| 16 | …"not authorization to test" | S073 body | yes | body sweep for "test" → no output |
| 17 | "None of the held entries records these as a reporter-side intake contract" (collaborator, credited, fork, enablement, required fields) | four held files | yes | `grep -n -i "enabl\|fork\|collaborator"` on the four held files → only `authorization-safe-harbor…:2,20` ("Enable Safe Harbors", unrelated); `grep -n -i "proof of concept\|impact statement\|required field\|summary, details"` → no output |
| 18 | "One page: the reporter-side steps at S073.txt:556-583" | S073 | yes | body 556 "Privately reporting a security vulnerability" to 583 "YesNo" (feedback widget) |
| 19 | "does not state the maintainer-side flow, CVE requests, timelines or rewards" | S073 | yes | both sweeps empty (below); maintainer-side text limited to 561, 573, 578, 579 |
| 20 | body sweep prints nothing (exit 1) | S073:556-583 | yes | re-run: no output, `exit=1` |
| 21 | whole-capture sweep prints nothing (exit 1) | S073 | yes | re-run: no output, `exit=1` |
| 22 | "The page's only pointer forward is 'The next steps depend…' (579)" | S073 | **stretched / false as written** | body also points forward at 561 "See Configuring private vulnerability reporting for a repository.", 563 "See Creating a repository security advisory.", 566 "See Coordinated disclosure of security vulnerabilities." |
| 23 | "the page it names is not in the capture" | S073 | yes | `grep -n -E "Managing privately"` → only 579 |
| 24 | "Three linked pages appear only as link text" (563, 566, 579) | S073 | **NO (incomplete)** | four link-only targets in the body: also "Configuring private vulnerability reporting for a repository" (561), which the entry omits |
| 25 | "Its reporter path begins at 'Security and quality' (568)" | S073 | **stretched (minor)** | first reporter step is line 567 "On GitHub, navigate to the main page of the repository."; 568 is the second step |
| 26 | page does not say how a reporter observes enablement; no proof of non-enablement | S073 body | yes | body `grep -n -i "enabl"` → 561, 564, 565, 566 only; none gives an observation method |
| 27 | enablement sentence names public repositories (561) | S073.txt:561 | yes | line 561 "Owners and administrators of public repositories can enable…" |
| 28 | "The page says nothing about private repositories" | S073 body / whole capture | yes (body); note whole-capture hit | body `grep -c -i "private repositor"` → `0`; whole capture: line 445 "Private repository enablement" is a site-navigation item in a list of troubleshooting topics, not about this feature |
| 29 | "Quote checks are exact-text checks… not a live check" | — | yes | the check is substring matching of the local capture (see Method) |
| 30 | "The `recheck:` line re-verifies the capture's bytes and quotes" | manifest.json S073 | **stretched** | recheck ran: `sha256 OK` and Q1-Q8 OK; but the manifest pins only eight quotes. The quotes used in these two sections at 561, 565, 568, 569, 579 (and 563 "admin or security permissions") are not pinned by the instrument; they were checked only by the exact-substring script in row (a) |
| 31 | "Documentation only… no submission, no contact, no probing" | — | yes | scope statement; nothing executed against a live target |

## Findings (ordered by severity)

1. **Stretched attribution, Overlap L30 (rows 3-4).** The entry says GitHub's page "answers the AI-assisted question differently" and quotes S073.txt:565 as the answer. Line 565 ("If a public repository has private vulnerability reporting enabled, anyone can submit a private vulnerability report…") does not mention AI. The only AI statement in the body is the optional checkbox at line 574. The contrast with the kernel page is therefore between a kernel rule about AI-found bugs and GitHub's silence on that point, not between two answers. Evidence: `sed -n '565p'` and `sed -n '574p'` outputs above, and `grep -n -w "AI"` output.

2. **Incomplete count, Limits L43 (row 24).** "Three linked pages appear only as link text" omits the fourth: "Configuring private vulnerability reporting for a repository" at S073.txt:561 (`sed -n '561p'`). The body has four link-only targets, not three.

3. **Overbroad pointer claim, Limits L40 (row 22).** "The page's only pointer forward is … (S073.txt:579)" is contradicted by S073.txt:561, 563 and 566, each of which says "See …" and names another page. A narrower statement, such as "the only pointer about what happens after submission", would be supported by the text; the one as written is not.

4. **Overbroad recheck claim, Limits L44 (row 30).** "The `recheck:` line re-verifies the capture's bytes and quotes" is true for the sha256 and for Q1-Q8. The recheck run printed `S073:sha256 OK` and `S073:Q1 OK … S073:Q8 OK`, `exit=0`. It does not pin the quotes at 561, 565, 568, 569 or 579, which the two sections rely on. Those were verified here only by exact substring match.

5. **Minor stretch, Limits L41 (row 25).** The reporter path "begins at 'Security and quality' (568)". The first step is line 567. Harmless to the conclusion, but imprecise.

6. **Minor cite-range issues (rows 2, 10).** The kernel "keeps its reproducer out of the public text" needs `:23-24`, not `:23`. The vendor "holds intake routes" at `:17-19` covers the heading and lead-in only; the routes are at `:26-28`.

## Holds (verified)
Rows 1, 5, 6, 8, 9, 11-12, 14-23, 26-29, 31: each re-verified by a command or a line read as shown above. The two sweep commands (rows 20-21) and the "no" content checks reproduce the entry's "printed nothing (exit 1)" results. The "What is new here" novelty claim (row 17) holds against the four held entries.

## Limitations
- Quote matching is exact substring against the local capture. It does not check GitHub's current page, and the capture's whole-line form was matched, not the rendered page.
- The "does not say" claims are checked against the captured body window 556-583 and the whole capture. A page elsewhere on GitHub that discusses maintainer flow was not examined and is out of this capture by design.
- Novelty (row 17) was checked only against the four held entries named in the section, not against the whole corpus.
- The recheck instrument was run on a copy of `corpus/` in scratch (the lane was not written). Its selftest writes were not run.
- Scope excludes the `## Scope and decision rule` and `## Falsifiable package rule` sections, except where quoted in the Limits text.
- No tool installed or upgraded for this seat. No git/jj mutation. Scratch removed on exit.
