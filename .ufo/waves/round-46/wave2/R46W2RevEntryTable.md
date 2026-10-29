VERDICT: BROKEN

Scope: `corpus/knowledge/github-private-vulnerability-reporting.md` — `## Scope and decision rule` (lines 7-24, incl. the observed-question table), plus the `## Limits` sweep claims that the Scope section points to (`see Limits`) and the `## Overlap and novelty` cross-references (checked as an extra, outside the assigned part). Source: `corpus/source-snapshots/round-46/S073.txt` (sha256 `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930`, 589 lines, matches manifest). Read-only; no git mutation; scratch removed.

## Findings (attacked item, command, output)

1. **Every quote in Scope + table is located on the cited line (PASS).** Command: a Python pass over entry lines 7-24 extracting each `“…”`, taking the nearest `S073.txt:N` cite, and testing `quote in S073.txt[N]`. Output (all `exact_on_cited_line=True`):
   - L11/561 `Owners and administrators of public repositories can enable private vulnerability reporting on their repositories.` found_at=[561]
   - L11,L18/564 `Private vulnerability reporting is separate from a repository’s SECURITY.md file.` found_at=[564]
   - L11,L17/564 `You can only report vulnerabilities privately for repositories where this feature is enabled.` found_at=[564]
   - L19/566 `following the instructions in the security policy for the repository, or by creating an issue asking the maintainers for a preferred security contact.` found_at=[566]
   - L20/573 `By default, you must provide a summary, details, proof of concept, and impact statement.` found_at=[573]
   - L20/573 `Maintainers can customize the form and require other information.` found_at=[573]
   - L21/574 `Optionally, select I used AI assistance to find or write up this report.` found_at=[574]
   - L22/577 `GitHub automatically adds the reporter of the vulnerability as a collaborator and as a credited user on the proposed advisory.` found_at=[577]
   - L23/578 `Note that only the repository maintainer can merge changes from that private fork into the parent repository.` found_at=[578]
   - L24/575 `GitHub will display a message letting you know that maintainers have been notified and that you have a pending credit for this security advisory.` found_at=[575]
   - Discrimination: `grep -c -F "Maintainers can customise the form"` → `0` (British spelling, must miss); `"GitHub pays a bounty to reporters"` → `0`; `"reporters receive a response within 14 days"` → `0`; positive control `grep -n -F "Maintainers can customize the form and require other information."` → `573:By default, you must …`.

2. **Recheck instrument does NOT verify most of the quotes the Limits bullet says it verifies (STRETCHED).** Entry Limits: "The `recheck:` line re-verifies the capture's bytes and quotes." Command: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073` → `S073:sha256 OK`, `S073:Q1 OK … anchor=560-ok` through `S073:Q8 OK … anchor=578-ok`, exit 0. The manifest S073 record pins only Q1-Q8 (560, 563, 564 "You can only…", 566 "you need to initiate … security policy for the repository" prefix only, 573 "By default…", 574, 577, 578). Not pinned by the instrument: the 561 "Owners and administrators…" sentence, the 564 SECURITY.md sentence, the 573 "Maintainers can customize…" sentence, the 575 "GitHub will display…" sentence, and the 566 issue-fallback clause. Bytes are verified (sha256 OK); quotes are verified only for the 8 pinned ones. My manual check (finding 1) did locate all 12, so no quote is unsupported, but the claim as worded overstates the instrument. Control: `--source S999` → `S999:source UNAVAILABLE reason=not-listed`, exit 2.

3. **Limits: pointer and link-count claims are wrong (STRETCHED / factual error).** Entry Limits bullet 3 says "Three linked pages appear only as link text…" listing 563, 566, 579. The capture has four `See …` links in the body: `S073.txt:561` ("See Configuring private vulnerability reporting for a repository."), `:563` (Creating a repository security advisory), `:566` (Coordinated disclosure of security vulnerabilities), `:579` (Managing privately reported security vulnerabilities). Command: `grep -n -E "See (Configuring|Creating|Coordinated|Managing)" …S073.txt` printed all four lines. The Limits bullet 2 also says "The page's only pointer forward is 'The next steps depend on…' (S073.txt:579)"; the page has four forward pointers, so "only" is false unless "pointer" is restricted to maintainer-side flow (not stated). The 561 link is omitted and the count is wrong.

4. **Table row 7 contains an unsupported characterization (STRETCHED).** Row: "A fork started by the reporter is a drafting step." Page text (S073.txt:578): "Optionally, click Start a temporary private fork if you want to start to fix the issue." The page never calls it a drafting step; that is the entry's gloss. The package rule that follows it (merge only with observed maintainer merge) IS supported by 578.

5. **Limits bullet 4 reporter-path start line is off by one (minor).** Entry: "Its reporter path begins at 'Security and quality' (S073.txt:568)." Source: `sed -n '567,569p'` printed `On GitHub, navigate to the main page of the repository.` (567), `Under the repository name, click the Security and quality tab…` (568), `Click Report a vulnerability to open the advisory form.` (569). The quoted strings are present on 568 and 569; the path begins at 567.

6. **Limits bullet 1 sweeps re-run exactly as printed (YES).** Commands and output:
   - `sed -n '556,583p' …S073.txt | grep -n -i -E "CVE|timeline|days|reward|bount|embargo|triage|authoriz|safe harbor|test|publish"` → no output, `exit=1`.
   - `grep -n -i -E "CVE|reward|bount|embargo|authoriz|safe harbor" …S073.txt` → no output, `exit=1`.
   - Control (same pipeline, term present): `sed -n '556,583p' … | grep -n -i -E "maintainer|Security and quality"` → matched lines 2, 5, 9, 10, 11, 13, 18, 20, 23, 24 (exit 0). The pipeline does match when text is present.
   - Extra: `grep -n -i -E "respon|hour|week|day"` → only nav lines 496 "Incident response", 517 "Respond to a security incident", 554 "Responsible use". `grep -n -i -E "collaborator|permission"` → 286/287 nav ("Add/Remove collaborators"), 493 nav ("Permissions for security features"), 563 ("admin or security permissions" — draft advisory), 577 (collaborator). No statement of collaborator permissions. Supports table row 6 ("keep them unknown") and row 8 ("gives no response time").

7. **"Says nothing about private repositories" (YES, with caveat).** Limits bullet 5. `grep -n -i -E "private repositor|…"` in the capture: only line 445 "Private repository enablement", a sidebar nav entry (nav-only lines 440-450). The body (556-583) has none.

8. **"Rest of the capture is site navigation" (YES, heuristic).** Scope line 9. `awk 'NR>=2 && NR<=555 && /\.$/'` printed no period-terminated line in 2-555; line 1 is the page title; 440-500 are sidebar link lists. Body markers: `Copy markdown` 558, `Note` 562, `Tip` 572/576, `Back to top` 580, footer after 581.

9. **Decision-rule and table sentences that are rule/inference rather than page statements (flagged, not errors per se):**
   - Scope L13: "A package may not describe the maintainers' response, the advisory's outcome or the fix's publication from this page, because the page does not state them." — YES (finding 6 sweeps, 7).
   - Row 2: "Do not treat it as the private-reporting submission route." — inference from "separate" + "only for repositories where enabled"; package rule, not a page statement.
   - Row 3: "must not call it a private-reporting submission." — entry-authored rule; page says only "you need to initiate the reporting process by following the instructions…".
   - Row 5: "Its absence is not a claim that no AI assistance was used." — inference from "Optionally"; not stated on the page.
   - Row 1, 4, 7 (second half), 8 ("may record this notification as the reporter-side confirmation") — rule/derivation, supported by the quoted lines.

10. **Overlap cross-references (extra, outside assigned part) — all resolve to the claimed content.**
   - `linux-kernel-security-bugs-reporting-process.md:23` — line 23 is the AI-assisted row ("Does an AI-assisted find stay private?", quoting S071 "you must treat it as public"). Matches the entry's description.
   - `ai-assisted-finding-validation.md:7-8` — line 8: "a reviewer distinct from its producer" for claim-ready status. Matches.
   - `vendor-third-party-finding-coordination.md:17-19` — line 17 "## Claim 1 — Microsoft's MSVR states three intake routes…". "A vendor's programme" is a loose paraphrase (it is Microsoft MSVR); not a falsehood.
   - `authorization-safe-harbor-and-scope.md:8` — "A safe-harbor badge or statement alone does not add assets to scope or establish permission…". Matches.
   - Overlap quotes `S073.txt:565`, `:574`, `:560`, `:563 admin or security permissions` — all exact-match (grep -F output lines 565/574/560/563).

## Verdict basis

BROKEN, per the lane rule (any stretched or unsupported statement). No quote in the Scope section or table is unlocated, and no `S073.txt` cite points to the wrong line. Failures: finding 2 (recheck overclaims quote coverage), finding 3 (link count "Three" is wrong, four are on the page; "only pointer forward" is overstated), finding 4 (row 7 "drafting step" is not on the page). Finding 5 is minor.

## Limitations

- I checked the Scope section, table, Limits sweep claims, and Overlap cross-refs. I did not review the counters v1.1 instrument logic, the re-grounded `## Re-ground (round 46)` sections, the F28 landing gate, or the other entries; those belong to other seats.
- The live GitHub page was not checked (documentation-only; the capture is the evidence). The "rest is navigation" check is a heuristic (no period-terminated lines outside the body, plus sidebar lists), not a full read of 1-555.
- The recheck instrument was run once on the main path; its `--selftest` was not run.
- Two `S073.txt` sentences were located with exact-text matching, which does not check curly vs straight apostrophe variants beyond the byte-exact matches shown.
- No other fixture or export was built; scratch dir `/fast/scratch/hyaku/kasegi-r46/R46W2RevEntryTable` was created and removed on exit.
