VERDICT: INFO

# R46ScoutManagePage — sibling-page scout for F28 (S073 reporter flow)

Read-only seat. No edits to corpus, SOURCES, knowledge entries, or git. Scratch capture was removed on exit (see Limitations); every quote below can be regenerated with the commands shown.

## 1. Premise correction (attacked: "the S073 page body states none of these")

The lane premise says S073 states none of acknowledgement, credit, CVE request, timeline, rewards. Partly false: S073 states reporter credit.

Command (pinned capture, sha256 prefix checked first):
```
sha256sum corpus/source-snapshots/round-46/S073.txt | cut -c1-16
grep -n -i -E 'acknowledg|timeline|CVE|reward|bount|compens|credit|respon' corpus/source-snapshots/round-46/S073.txt
```
Output:
```
66c96a6168011dcf
496:Incident response
517:Respond to a security incident
554:Responsible use
575:At the bottom of the form, click Submit report. GitHub will display a message letting you know that maintainers have been notified and that you have a pending credit for this security advisory.
577:When the report is submitted, GitHub automatically adds the reporter of the vulnerability as a collaborator and as a credited user on the proposed advisory.
```
(496/517/554 are navigation-menu hits, not reporter terms.) The manifest sha256 begins `66c96a6168011dcf`, so the pinned bytes match.

Live check (curl, fetched 2026-10-28, HTTP 200):
```
curl -sS -A "Mozilla/5.0" -o s073-live.html https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately
grep -o -i -E 'pending credit|automatically adds the reporter|acknowledg|CVE|bount' s073-live.html | sort | uniq -c
```
Output:
```
      3 automatically adds the reporter
      3 pending credit
```
Result: S073 states credit-at-submission. It states nothing on acknowledgement, timeline, CVE, or rewards.

## 2. Canonical sibling URLs (from the live S073 page)

The live S073 HTML (`s073-live.html`) carries these hrefs:
- "See Managing privately reported security vulnerabilities" → `/en/code-security/how-tos/report-and-fix-vulnerabilities/fix-reported-vulnerabilities/manage-vulnerability-reports`
- "Configuring private vulnerability reporting for a repository" → `/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository`
- "Coordinated disclosure of security vulnerabilities" → `/en/code-security/concepts/vulnerability-reporting-and-management/coordinated-disclosure#about-reporting-and-disclosing-vulnerabilities-in-projects-on-github`

Extraction command:
```
grep -o '.\{0,200\}Managing privately reported.\{0,60\}' s073-live.html
```
(the same pattern for "Configuring private vulnerability" and "Coordinated disclosure of security" was run; each printed one `<a href=...>` anchor matching the link text.)

Fetch and status, one per page:
```
curl -sS -A "Mozilla/5.0" -o manage.html -w 'manage %{http_code} %{redirect_url}\n' https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/fix-reported-vulnerabilities/manage-vulnerability-reports
```
Printed `manage 200 ` (empty redirect_url), and likewise `200` with no redirect for configure and coordinated. Each HTML `<title>` matched the link text ("Managing privately reported security vulnerabilities - GitHub Docs", etc.), and each carries `<meta name="path-article">` equal to the path above. The pages have no `rel="canonical"` tag; the `path-article` meta is the canonical path.

## 3. Located quotes (location = section heading and line in the fresh body-endpoint capture `…/api/article/body?pathname=<path>`)

Managing privately reported security vulnerabilities (`manage.md`):
- M1, §intro, L5: "When a security researcher reports a vulnerability privately, you are notified and can choose to either accept it, ask more questions, or reject it." (24 words) — reporter outcomes are accept/ask/reject; no timeline.
- M2, §Reviewing a vulnerability report, L22: "An advisory that was reported privately has a status of `Triage`."
- M3, §Reviewing…, L29: "This doesn't make the report public." (accept-as-draft bullet)
- M4, §Reviewing…, L32: "A regular comment is visible to the reporter and all collaborators on the advisory." (14)
- M5, §Reviewing…, L33: "Where possible, you should add a comment explaining why you don't consider the report a security risk." (18) — explanation is optional ("where possible").
- M6, §Discussing a report with people who have write access, L39: "These comments are hidden from the reporter and invited advisory collaborators who do not have write access." (17)

Coordinated disclosure of security vulnerabilities (`coordinated.md`):
- C1, §About disclosing vulnerabilities in the industry, L9: "the full details are only published once the maintainer has acknowledged the issue" (13) — ack is a publication gate for the maintainer, not a promise to the reporter.
- C2, §Best practices for vulnerability reporters, L18: "Expecting to be compensated for reporting an issue, where no public bounty program exists." (14) — rewards: reporters are told not to expect them absent a bounty program.
- C3, same section, L20: "disclose a vulnerability publicly after a period of time, if they have tried to contact the maintainers and not received a response" (22) — "a period of time" is unspecified.
- C4, same section, L22: "We recommend vulnerability reporters clearly state the terms of their disclosure policy as part of their reporting process." (19) — the reporter sets timing; GitHub sets none.
- C5, §Best practices for maintainers, L31 (bullet after "we recommend you:"): "Acknowledge receipt of the vulnerability report as quickly as possible, even if no immediate resources are available for investigation." (19) — maintainer recommendation, not a guarantee.
- C6, same, L34: "Always acknowledge the vulnerability reporter when you credit the discovery." (11) — credit is maintainer-side.
- C7, same, L35: "Aim to publish a fix as soon as you can." (9) — no date.
- C8, §Standard process, L58: "If you've found a security vulnerability in GitHub, please report the vulnerability through our coordinated disclosure process." (19) — the only bounty pointer; it concerns GitHub's own products.
- C9, §Private vulnerability reporting, L70: "When a vulnerability is reported, repository maintainers are immediately notified" — maintainer notification, not reporter acknowledgement.

Configuring private vulnerability reporting for a repository (`configure.md`):
- F1, §Enabling or disabling…, L19: "security researchers see a **Report a vulnerability** button on the repository’s "Advisories" page" (S073 instead routes via the Security and quality tab; both use the same button label).
- F2, same section, L23: "The built-in default form is not enforced for API submissions." (11) — S073 does not say this.
- F3, §Customizing the vulnerability reporting form, L65: "If GitHub cannot parse or validate a custom form, reporters see the default form instead." (16) — S073 does not say this.
- F4, §Requiring reporters to assign a CWE, L69: "You can require reporters to associate at least one Common Weakness Enumeration (CWE) with each new report." (17) and "This repository-level setting applies to reports submitted in the web interface and with the REST API." (16)

Checks that the reporter-expectation topics are absent (do-nothing control):
```
grep -c -i 'CVE' manage.md configure.md coordinated.md   # 0 for each
grep -c -i 'CWE' configure.md ; grep -c -i 'CWE' corpus/source-snapshots/round-46/S073.txt
```
Printed `3` for configure.md and `0` for S073. The CWE rule (F4) is therefore absent from S073.

## 4. What a reporter can expect (answer to the seat question)

- Acknowledgement: no page promises the reporter one. Only maintainer recommendations (C5) and a maintainer publication gate (C1). S073: none.
- Credit: S073 states credit at submission (lines 575, 577). Nothing on the managing page says credit survives a close or decline (M5 covers only the close comment). Coordinated says the maintainer "should" credit (C6).
- CVE request: none on any of the four pages (CVE grep = 0 everywhere).
- Timeline: none from GitHub. C3 ("a period of time") and C7 ("as soon as you can") are unspecified.
- Rewards: none for third-party repositories. C2 discourages expecting compensation absent a bounty program; C8 points only to GitHub's own bounty.

## 5. SOURCES row proposals (propose only; nothing written)

1. Managing privately reported security vulnerabilities — YES, own row. S073 defers every post-submission outcome to it (S073 L579) and it is the only source for Triage, accept/close, and comment visibility (M1–M6). Propose docs, tier A, sha-pinned capture of the manage URL above.
2. Coordinated disclosure of security vulnerabilities — YES, own row, labelled as norms. It is the only page with reporter-timing and compensation statements (C1–C4, C8). Its reporter statements are recommendations, not GitHub commitments; the row should say so.
3. Configuring private vulnerability reporting for a repository — CONDITIONAL. Maintainer-facing, so not a reporter-expectation source. It is needed only if the F28 Limits cite the CWE requirement, API non-enforcement, or form fallback (F2–F4), which S073 omits. Recommended yes if those facts are stated.

## 6. Impact on the F28 Limits section

The after-state in `.ufo/waves/round-46/claims.json` (line 29) lists five reporter facts: separate from SECURITY.md; default required fields; optional AI-assistance disclosure; automatic collaborator and credit; only the maintainer merges from the temporary fork. Against that list, the three sibling pages change the Limits in six ways:
- "Default required fields" must be qualified. A repository may require a CWE (F4), a custom form can replace the default (S073 L573 covers custom forms, but F3 adds the fallback to default when the custom form fails to parse), and the API path does not enforce the default form (F2). S073 states only the default.
- Add: GitHub states no acknowledgement, response, or disclosure timeline for reporters (C1, C3, C5, C7).
- Add: no CVE request appears in the flow (CVE grep = 0).
- Add: no reward for third-party reports; bounty applies to GitHub's own vulnerabilities (C2, C8).
- Credit: "automatic … credit" stays true at submission (S073 L577). Limits should add that the pages do not say whether credit survives a decline or close (M5).
- Add reporter-visibility limits: regular comments are visible to the reporter, confidential comments are hidden (M4, M6); accept-as-draft does not publish (M3); closing an advisory needs no required explanation (M5, "where possible").

None of these contradicts the five frozen claims. Items 1, 2, 4 and 6 are additions; item 3 narrows an existing one.

## 7. Controls

- Do-nothing control (S073 alone): the S073 grep in §1 shows only credit lines (575, 577). Acknowledgement, timeline, CVE, reward terms are absent from the pinned bytes.
- Positive control (pattern works on the sibling pages): `grep -c -i 'acknowledg' coordinated.md` printed `3`.
- Negative control (pattern returns absence cleanly): `grep -c -i 'zzqx-nonexistent-string' manage.md` printed `0` and exited 1.
- Live-vs-pinned control: the live S073 contains both credit phrases (3 each), so the pinned capture matches the live page on the credit lines. This is a two-phrase check, not a full diff.

## 8. Limitations

- Scratch (`$HYAKU_SCRATCH/kasegi-r46/R46ScoutManagePage/`) was removed on exit. Regenerate with `curl -sS -A "Mozilla/5.0" -o manage.md "https://docs.github.com/api/article/body?pathname=/en/code-security/how-tos/report-and-fix-vulnerabilities/fix-reported-vulnerabilities/manage-vulnerability-reports"` (and the same form for configure and coordinated paths above).
- Quotes use GitHub's rendered markdown body, not raw HTML bytes. A few body lines were truncated by the reader (SVG icon markup). None of the quoted lines were truncated (C2 at L58 and F1 at L19 quote only visible text).
- The `Ran in a temporary shell…` note that appeared in tool output is harness text, not page content; ignored.
- Line numbers are from my fresh body-endpoint capture, not from a pinned snapshot. Pinned SOURCES rows would need their own snapshots before these quotes are citable.
- Only the English pages were read. No localized versions were checked.
- The F28 entry does not yet exist on disk (`corpus/knowledge/github-private-vulnerability-reporting.md` is absent), so §6 is measured against the claims.json after-state, not the entry text.
- Live date 2026-10-28 is the fetch date; the pages may change after capture.
- No installs or upgrades were performed; only curl and grep were used.
- No git, jj, or other mutating command was run.
