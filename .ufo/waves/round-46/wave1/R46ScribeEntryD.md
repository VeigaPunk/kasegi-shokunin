VERDICT: DRAFT-READY

Seat: R46ScribeEntryD (C2 entry drafter D, independent; no other draft read). Draft only: `.ufo/waves/round-46/wave1/R46ScribeEntryD.draft/github-private-vulnerability-reporting.md` (49 lines, 1314 words). Nothing committed, no git/jj mutation, no shared file touched. C1 is not in this seat's item and was not touched.

## Finding 1 — the draft's structure matches the house shape and the frozen gate's structural checks

Built: the F28 entry (`github-private-vulnerability-reporting.md`). Title line, blank line, `source: S073 — https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately — section anchors: ...`, `verified-at: 2026-10-28`, `recheck: cd ... --source S073 # 180d`. Four sections exactly: `## Scope and decision rule`, `## Overlap and novelty`, `## Limits`, `## Falsifiable package rule`. Table of 8 data rows, three cells each, no extra pipes.

Command run (the self-check, in scratch):
```
TMPDIR=/fast/scratch/hyaku/kasegi-r46/R46ScribeEntryD python3 selfcheck.py
```
Output (the tail):
```
sections: ['## Scope and decision rule', '## Overlap and novelty', '## Limits', '## Falsifiable package rule']
line1: # GitHub private vulnerability reporting: reporter-side flow
line2-blank: ''
line3-source-ok: True
line4: verified-at: 2026-10-28
line5: recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073 # 180d
table data rows: 8 pipe-count-ok: True
straight-double-quote count: 4
```
The four straight double quotes are inside one backticked sweep command in Limits, not quotations.

Command run (the frozen gate's own functions, on a scratch tree holding the draft as the F28 entry, the four cross-referenced knowledge files, the S073 capture and a one-row README with the F28 row; G1 is expected to fail there because the scratch README has one row, not 28):
```
G1 (False, 'rows=1 admitted=1 dup=0')
G2 (True, 'source=1 verified-at=1 recheck=1 sections=4/4 table-rows=8 xrefs=4/4')
G5 (True, 'spans=21 located=21 failed=0 uncited=0 cores=5/5')
```
The first G2 run, before the cross-ref files were copied into the scratch tree, printed `xrefs=0/4`; that was a scratch-tree omission, not a draft defect, and was fixed by copying the files.

## Finding 2 — every curly quotation is located in S073 and every frozen core appears inside a located span

Each quotation is in curly double quotes, at most 25 words, and immediately followed by a `(`S073.txt:N`)` or `(`S073.txt:N-M`)` citation. The self-check (same regex, same whitespace and apostrophe normalisation as the gate's `norm`) printed:
```
Q01 S073.txt:561 words=14 located=1 :: Owners and administrators of public repositories can enable private vu
Q02 S073.txt:564 words=10 located=1 :: Private vulnerability reporting is separate from a repository’s SECURI
Q03 S073.txt:564 words=13 located=1 :: You can only report vulnerabilities privately for repositories where t
Q04 S073.txt:564 words=13 located=1 :: You can only report vulnerabilities privately for repositories where t
Q05 S073.txt:564 words=10 located=1 :: Private vulnerability reporting is separate from a repository’s SECURI
Q06 S073.txt:566 words=23 located=1 :: following the instructions in the security policy for the repository, 
Q07 S073.txt:573 words=14 located=1 :: By default, you must provide a summary, details, proof of concept, and
Q08 S073.txt:573 words=9 located=1 :: Maintainers can customize the form and require other information.
Q09 S073.txt:574 words=13 located=1 :: Optionally, select I used AI assistance to find or write up this repor
Q10 S073.txt:577 words=20 located=1 :: GitHub automatically adds the reporter of the vulnerability as a colla
Q11 S073.txt:578 words=17 located=1 :: Note that only the repository maintainer can merge changes from that p
Q12 S073.txt:575 words=24 located=1 :: GitHub will display a message letting you know that maintainers have b
Q13 S073.txt:565 words=20 located=1 :: If a public repository has private vulnerability reporting enabled, an
Q14 S073.txt:560 words=10 located=1 :: Anyone can privately report a security vulnerability to repository mai
Q15 S073.txt:563 words=4 located=1 :: admin or security permissions
Q16 S073.txt:579 words=12 located=1 :: The next steps depend on the action taken by the repository maintainer
Q17 S073.txt:568 words=3 located=1 :: Security and quality
Q18 S073.txt:569 words=3 located=1 :: Report a vulnerability
Q19 S073.txt:563 words=5 located=1 :: Creating a repository security advisory
Q20 S073.txt:566 words=5 located=1 :: Coordinated disclosure of security vulnerabilities
Q21 S073.txt:579 words=5 located=1 :: Managing privately reported security vulnerabilities
spans=21 located=21 failed=0 uncited_curly=0 cores=5/5
G5-equivalent: True
```
The `sed -n` lines I verified by hand for the quotations (`sed -n '<N>p' corpus/source-snapshots/round-46/S073.txt`, read in full):
- 560: "Anyone can privately report a security vulnerability to repository maintainers."
- 561: "Owners and administrators of public repositories can enable private vulnerability reporting on their repositories."
- 563: "If you have admin or security permissions for a public repository, you don’t need ... See Creating a repository security advisory." (Q15, Q19)
- 564: "Private vulnerability reporting is separate from a repository’s SECURITY.md file. You can only report vulnerabilities privately for repositories where this feature is enabled. ..." (Q02-Q05)
- 565: "If a public repository has private vulnerability reporting enabled, anyone can submit a private vulnerability report to the repository maintainers."
- 566: "If the repository doesn't have private vulnerability reporting enabled, you need to initiate ... by following the instructions in the security policy for the repository, or by creating an issue asking the maintainers for a preferred security contact. See Coordinated disclosure of security vulnerabilities." (Q06, Q20)
- 568: "Under the repository name, click the Security and quality tab. ..." (Q17)
- 569: "Click Report a vulnerability to open the advisory form." (Q18)
- 573: "By default, you must provide a summary, details, proof of concept, and impact statement. Maintainers can customize the form and require other information. ..." (Q07, Q08)
- 574: "Optionally, select I used AI assistance to find or write up this report."
- 575: "At the bottom of the form, click Submit report. GitHub will display a message letting you know that maintainers have been notified and that you have a pending credit for this security advisory." (Q12)
- 577: "When the report is submitted, GitHub automatically adds the reporter of the vulnerability as a collaborator and as a credited user on the proposed advisory." (Q10)
- 578: "Optionally, click Start a temporary private fork ... Note that only the repository maintainer can merge changes from that private fork into the parent repository." (Q11)
- 579: "The next steps depend on the action taken by the repository maintainer. See Managing privately reported security vulnerabilities." (Q16, Q21)

The five required content items are each inside a located span: enablement (564, Q03), default fields (573, Q07), AI checkbox (574, Q09), collaborator and credited-user status (577, Q10), maintainer-only merge from the private fork (578, Q11). Line 564 contains the curly apostrophe in `repository’s`; the span quoting it (Q02, Q05) is located with the apostrophe intact.

## Finding 3 — the overlap citations are at verified line numbers

Command run:
```
sed -n '23p' corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
sed -n '7,8p' corpus/knowledge/ai-assisted-finding-validation.md
sed -n '17,19p' corpus/knowledge/vendor-third-party-finding-coordination.md
sed -n '8p' corpus/knowledge/authorization-safe-harbor-and-scope.md
```
Output (abridged to start of line): `| Does an AI-assisted find stay private? | “If you resorted to AI assistance ...` / `Treat an AI-originated finding as a candidate, ...` / `For Kasegi claim-ready status, the package must identify the reproducing evidence and a reviewer distinct from its producer` / `## Claim 1 — Microsoft's MSVR states three intake routes for third-party-product vulnerabilities` / `> MSVR learns about vulnerabilities in third-party products in three ways:` / `A safe-harbor badge or statement alone does not add assets to scope or establish ...`

The overlap section cites linux:23 (the kernel's AI-assisted row, F27), ai-assisted-finding-validation:7-8 (reviewer distinct from producer), vendor-third-party-finding-coordination:17-19 (intake routes), and authorization-safe-harbor-and-scope:8 (badge does not establish permission). The F27 label is present in `corpus/README.md:651`.

## Finding 4 — the Limits sweep: the page does not state the maintainer-side flow, CVE requests, timelines or rewards

Command run (exact, as cited in the entry):
```
sed -n '556,583p' corpus/source-snapshots/round-46/S073.txt | grep -n -i -E "CVE|timeline|days|reward|bount|embargo|triage|authoriz|safe harbor|test|publish"
```
Output: none; grep exit 1.

Command run:
```
grep -n -i -E "CVE|reward|bount|embargo|authoriz|safe harbor" corpus/source-snapshots/round-46/S073.txt
```
Output: none; grep exit 1. (A broader whole-file run for `triage` matched only navigation headings at lines 80, 215, 251, 496, 517 and 554 — "Dependabot auto-triage rules", "Auto-triage Dependabot alerts", "Triage alerts in pull requests", "Incident response", "Respond to a security incident", "Responsible use" — none in the page body.)

The page's own pointer forward is line 579, "The next steps depend on the action taken by the repository maintainer." The linked page is not in the capture. The entry says so and records no outside knowledge.

## Finding 5 — the falsifiable rule is checkable against the page

Rule: a package that says a vulnerability was reported through GitHub private vulnerability reporting must record an observed enablement fact for the target repository (S073.txt:564), and when that fact is absent must cite the security-policy route or the issue fallback quoted at S073.txt:566 and must not call the report a private-reporting submission. A package that says a fix was merged from the reporter's fork must also record the maintainer's merge (S073.txt:578). The rule has no outside input and can be failed by a package that names the feature with neither fact.

## Limitations

- Quote checks are against the pinned capture (sha256 `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930`, verified by `sha256sum` in this run). They are not a live check of GitHub's current page; the `recheck:` line re-verifies the capture's bytes and quotes only.
- The gate was run on a scratch tree, not on the round tree: the round's F28 row, SOURCES row and manifest pin do not exist at this seat's base, so G1 cannot pass here and G3/G4/G6/G7 were not run by this seat.
- The entry records no maintainer-side flow, CVE, timeline or reward (see Finding 4); the linked pages are named but not read.
- The AI-assistance contrast with the kernel page is stated as a difference in what each source says, not as a judgement on either project's policy. GitHub's page gives no handling rule for a flagged report; the entry says so and does not infer one.
- The entry covers only the reporter-side flow on this page, and only public repositories as the page's enablement sentence names them.

## Scratch and cleanup

Scratch root `/fast/scratch/hyaku/kasegi-r46/R46ScribeEntryD/` held `selfcheck.py` and temporary tree directories (each removed after its run). The scratch root is removed at yield. No file was written to ~/.local/bin, no PATH directory, no fleet-root tracked file.
