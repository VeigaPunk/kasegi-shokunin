# R46bScribeAdmission — C2 (coverage) admission append drafts — F29, round 46 attempt 2 (DRAFT ONLY)

DRAFT ONLY. Nothing tracked is edited by this seat. Each block is delimited by `<<<BEGIN <id>` /
`<<<END <id>` marker lines; extract the text strictly between the markers. The first line of each
block is intentionally blank (the target files end in a newline and the round-45/46 blocks were each
preceded by one blank line). The L1 applies (a) and (b) by appending at end-of-file and (c) by
inserting one line at the stated sorted position.

Target paths are relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

- (a) → END of `corpus/README.md` (the round-46 attempt-1 block ends at `corpus/README.md:668`).
- (b) → END of `PROVINCE.md` (the attempt-1 `[r46 Frontier amendment, …] F28` line is `PROVINCE.md:171`).
- (c) → ONE line in `corpus/instruments/knowledge-expected.txt`, at the stated sorted position.

Evidence for every claim in the drafted rows is in this seat's report
`.ufo/waves/round-46/attempt2/wave1/R46bScribeAdmission.md` (and its raw receipts
`.ufo/waves/round-46/attempt2/wave1/R46bScribeAdmission.draft/receipts.txt`) and in the frozen capture
`corpus/source-snapshots/round-46-a2/S074.txt` (sha256
`1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, 42 lines).

## Block (a) — APPEND to END of corpus/README.md

<<<BEGIN a

## Round-46 admission (attempt 2) — coverage map row and Frontier F29 (appended 2026-10-29)

The coverage map and frontier table above are not edited in place (R6). The round-46 attempt-2 entry
`corpus/knowledge/github-repository-security-advisories.md` (F29, source S074) records GitHub's repository
security advisories as the maintainer-side advisory lifecycle: a maintainer creates a draft advisory to
privately discuss the impact of the vulnerability, collaborates on the fix in a temporary private fork, and
publishes the advisory to alert the community once a patch is released; contributors can be given credit on
the advisory; GitHub is a CNA authorized to assign CVE identification numbers, usually reviews a CVE request
within 72 hours, and publishes the CVE to the MITRE database once the advisory is public; publication makes
the advisory data and the accepted advisory credits visible, keeps the conversation history to
collaborators, and leaves the advisory URL unchanged; and a fix version should be added to the advisory
before it is published. Its evidence is limited to this one GitHub Docs page; it does not assert how other
platforms or vendors run a maintainer-side advisory lifecycle.

| Area | Entry | Source basis |
|---|---|---|
| GitHub repository security advisories: the maintainer-side advisory lifecycle (draft advisory and private discussion of impact, temporary private fork, advisory credit, the CVE request to GitHub as a CNA, publication visibility and the unchanged advisory URL, and the fix-version duty) (round 46 attempt 2) | `corpus/knowledge/github-repository-security-advisories.md` | S074 — GitHub Docs "Repository security advisories" page (`corpus/source-snapshots/round-46-a2/S074.txt` capture), opened 2026-10-29; capture and located quotes in `corpus/source-snapshots/round-46-a2/manifest.json` |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F29 | GitHub repository security advisories, maintainer-side lifecycle: the draft advisory used to privately discuss the vulnerability's impact, the temporary private fork, advisory credit, the CVE request to GitHub as a CNA, publication visibility and the unchanged advisory URL, and the fix version added before publication | admitted | `corpus/knowledge/github-repository-security-advisories.md` | S074 | Keep the maintainer-side advisory lifecycle distinct from the reporter-side flow (F28) and from the CVE Program's CNA assignment rules (F07); re-open the GitHub Docs page before relying on its 72-hour CVE review window or on its fix-version guidance. Editing a published advisory, the REST API for repository security advisories and GitHub Advisory Database edits stay out of F29. |

[r46 attempt-2 amendment, appended 2026-10-29] The 28/28 count on the round-46 attempt-1 amendment line above records the round-46 attempt-1 state and is retained as history (R9). At round 46 (attempt 2) the public-practice frontier stands at **29/29 admitted** (29 — `grep -cE '^\| F[0-9]+ \|' corpus/README.md` 2026-10-29) — F01-F08 at round 23, F09 at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30, F15 at round 31, F16 at round 33, F17 at round 34, F18 at round 35, F19 at round 36, F20 at round 37, F21 at round 38, F22 at round 39, F23 at round 40, F24 at round 41, F25 at round 42, F26 at round 44, F27 at round 45, F28 at round 46, F29 at round 46 (attempt 2); rounds 27, 32 and 43 admitted no frontier row. The lost-domain denominator remains 0/18; the frontier count is separate.
<<<END a

## Block (b) — APPEND to END of PROVINCE.md

<<<BEGIN b

[r46 Frontier amendment, appended 2026-10-29, end-of-file append per R6] F29 — GitHub repository security advisories, maintainer-side lifecycle (the draft advisory and the private discussion of the vulnerability's impact, the temporary private fork, advisory credit, the CVE request to GitHub as a CNA with its 72-hour review, publication visibility and the unchanged advisory URL, and the fix version added before publication) — admitted round 46 (attempt 2); entry `corpus/knowledge/github-repository-security-advisories.md` (source S074); scope limit: maintainer-side advisory lifecycle only — the reporter flow stays F28, and advisory editing, the REST API for repository security advisories and GitHub Advisory Database edits stay out
<<<END b

## Block (c) — INSERT ONE LINE into corpus/instruments/knowledge-expected.txt

Placement: sorted position, immediately after the existing line
`corpus/knowledge/github-private-vulnerability-reporting.md` (file line 29) and immediately before the
existing line `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` (file line 30). This is
NOT a bare append at end-of-file: the file's last two lines are the `#` header comments, and the file
states it is a sorted list of `corpus/knowledge/*.md`; round 45 and round 46 attempt 1 both placed their
entry at sorted position. After the insertion the file holds 66 entry lines plus the two comment lines.

<<<BEGIN c
corpus/knowledge/github-repository-security-advisories.md
<<<END c
