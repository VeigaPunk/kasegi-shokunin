# R46ScribeAdmission — C2 admission append drafts (DRAFT ONLY, not applied to any tracked file)

Each block is delimited by `<<<BEGIN <id>` / `<<<END <id>` marker lines. Extract the text strictly between the markers; the first line of each block is intentionally blank (the target files end in a newline, and the round-45 blocks were preceded by one blank line). The L1 applies these by append (a, b) and by sorted-position insertion (c).

Target paths are relative to /home/vgpnk/Projects/shokunin/kasegi-shokunin.

## Block (a) — APPEND to END of corpus/README.md

<<<BEGIN a

## Round-46 admission - coverage map row and Frontier F28 (appended 2026-10-28)

The coverage map and frontier table above are not edited in place (R6). The round-46 entry
`corpus/knowledge/github-private-vulnerability-reporting.md` (F28, source S073) records GitHub's private vulnerability reporting as a reporter-side flow: private reporting is enabled by owners of public repositories and is separate from the repository's SECURITY.md file; the report is filed through the advisory form under the repository's Security and quality tab; the form requires a summary, details, proof of concept and impact statement by default; the AI-assistance disclosure is optional; submission adds the reporter as a collaborator and credited user on the proposed advisory; and only the repository maintainer can merge from a temporary private fork. Its evidence is limited to this one GitHub Docs page; it does not assert how maintainers triage reports, what the GitHub Security Advisory database holds, or how CVEs are assigned.

| Area | Entry | Source basis |
|---|---|---|
| GitHub private vulnerability reporting: reporter-side flow of the repository advisory form (enablement, separation from SECURITY.md, default required fields, optional AI-assistance disclosure, automatic reporter credit, maintainer-only private-fork merge) (round 46) | `corpus/knowledge/github-private-vulnerability-reporting.md` | S073 — GitHub Docs "Privately reporting a security vulnerability" page (`corpus/source-snapshots/round-46/S073.txt` capture), opened 2026-10-28; capture and located quotes in `corpus/source-snapshots/round-46/manifest.json` |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F28 | GitHub private vulnerability reporting, reporter flow: enablement by owners of public repositories, separation from SECURITY.md, the advisory form's default required fields, the optional AI-assistance disclosure, automatic reporter collaborator and credit, and the temporary private fork that only the maintainer can merge | admitted | `corpus/knowledge/github-private-vulnerability-reporting.md` | S073 | Keep the reporter flow distinct from the Linux kernel's e-mail process (F27) and from the AI-finding validation rules; re-open the GitHub Docs page before relying on its form fields or enablement wording. Maintainer handling, the GitHub Security Advisory database and CVE assignment are outside F28. |

[r46 amendment, appended 2026-10-28] The 27/27 count on the round-45 amendment line above records the round-45 state and is retained as history (R9). At round 46 the public-practice frontier stands at **28/28 admitted** — F01-F27 as previously recorded and F28 admitted this round. The lost-domain denominator remains 0/18; the frontier count is separate.
<<<END a

## Block (b) — APPEND to END of PROVINCE.md

<<<BEGIN b

[r46 Frontier amendment, appended 2026-10-28] F28 — GitHub private vulnerability reporting, reporter flow (enablement by owners of public repositories and separation from SECURITY.md, the advisory form's default required fields, the optional AI-assistance disclosure, automatic reporter collaborator and credit, and the temporary private fork that only the maintainer can merge) — admitted round 46; entry `corpus/knowledge/github-private-vulnerability-reporting.md` (source S073); scope limit: reporter flow only — maintainer handling, the GHSA database and CVE assignment stay out
<<<END b

## Block (c) — INSERT ONE LINE into corpus/instruments/knowledge-expected.txt

Placement: sorted position, between the existing line `corpus/knowledge/ev-model.md` and the existing line `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` (file lines 28 and 29). This is not a bare append at end-of-file: the file's last two lines are the `#` header comments, and round 45 placed its entry at sorted position (commit 6662a42, `@@ -34,6 +34,7 @@`), not after the header. After insertion the file holds 65 entry lines plus the two comment lines.

<<<BEGIN c
corpus/knowledge/github-private-vulnerability-reporting.md
<<<END c
