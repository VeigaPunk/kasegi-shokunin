VERDICT: DRAFT-READY

# R46bScribeEntryB — C2 entry drafter B (kasegi round 46, attempt 2)

Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Seat kind: builder (scribe). Writes confined to
`.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryB.draft/` and this Report. No commit, no push, no mutating
git/jj command, no write to the fleet repo, to a sibling lane, to MANIFEST.json, to `.ufo/state` or to
`~/Projects/shokuknow`. Scratch used: `/fast/scratch/hyaku/kasegi-r46/R46bScribeEntryB` (removed before yield).

## What was built

- **The C2 deliverable** — the F29 knowledge-entry draft, at
  `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryB.draft/github-repository-security-advisories.md`
  (15,320 bytes). Its basename is the name the committed gate expects as `ENTRY`
  (`corpus/knowledge/github-repository-security-advisories.md`), so L1 can land it with a copy and no edit.
- **The quote self-check** — `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryB.draft/self-check.txt`: all 45
  curly quotes, each with the `sed -n 'Np'` line it was verified against (Appendix A, pasted in full).

Entry shape as built: provenance trio on lines 1-4 (`# title`, blank, `source: S074 — <canonical URL> — <section
names>`, `verified-at: 2026-10-29`, one `recheck:` line); exactly the four required sections
(`## Scope and decision rule`, `## Overlap and novelty`, `## Limits`, `## Falsifiable package rule`); a 19-row
`| id | observed question | ground |` table (ids G1..G19) whose ground cells carry the quote plus its
`S074.txt:N` cite; F28/F07 (plus a timelines) contrasts cited as `corpus/knowledge/<file>.md:<line>`.

All nine facts C2 requires inside located quotes are present: private discuss-and-fix definition (S074.txt:10),
temporary private fork (13), credit (17), GitHub as CNA (24), the 72-hour review clock (25), requesting does not
publish (25), the other-CNA boundary (26), publication visibility (31), fix-version duty (38).

## Findings

### F-1 — Source opened and read independently (no sibling draft read)

Command:
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && wc -l corpus/source-snapshots/round-46-a2/S074.txt && sha256sum corpus/source-snapshots/round-46-a2/S074.txt`

Output:
```
42 corpus/source-snapshots/round-46-a2/S074.txt
1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039  corpus/source-snapshots/round-46-a2/S074.txt
```
The sha256 matches the task's pinned value and the manifest record. The whole capture is body prose; the quoted
lines are 3, 6, 10, 12, 13, 14, 15, 16, 17, 19, 20, 23, 24, 25, 26, 31, 32, 33, 34, 36, 38, 40, 41, 42.

### F-2 — House shape read: F28 (the reporter-side twin) and F07 (CNA rules)

Commands: `cat -n corpus/knowledge/github-private-vulnerability-reporting.md | cut -c1-260` (49 lines) and
`cat -n corpus/knowledge/cna-assignment-and-vulnerability-rules.md | cut -c1-200` (80 lines). The seven
cross-reference cites used in the entry were each printed before use; verbatim, they are:

F28 line 9 — `This entry records one reporter-side flow: GitHub's documented route for a person who wants to report a security vulnerability privately to a repository's maintainers.`
F28 line 23 — `| Who can merge a fix from the temporary private fork? | “Note that only the repository maintainer can merge changes from that private fork into the parent repository.” (`S073.txt:578`) |`
F28 line 39 — `- One page: the reporter-side steps at S073.txt:556-579. It is not GitHub's full policy and not a general standard for private reporting.`
F28 line 40 — `- The page does not state the maintainer-side flow, CVE requests, timelines or rewards.`
F07 lines 9-13 — `A local CVE-request package review separates technical vulnerability determination,` / `CNA assignment scope, and identifier counting.`
F07 line 32 — `| 3.1.1 | “CNAs MUST develop, document, and operate within a Scope Definition” |`
F07 line 36 — `| 4.2.1.1 | “The CNA with the most appropriate scope MUST be contacted and given the first opportunity to assign.” |`
timelines lines 7-8 — `A disclosure timeline in a report or case record must name the policy or coordinator, the event that starts its clock, the stated interval, the patch/publication relationship, and any documented extension or exception.` / `Do not describe one interval as the universal researcher deadline.`

### F-3 — The draft, measured on its own structure

Command: python3 over the draft (section word counts, table rows, xrefs). Output:
```
## Scope and decision rule words= 901
## Overlap and novelty words= 577
## Limits words= 521
## Falsifiable package rule words= 297
table-like lines: 21
ids: ['id', '---', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19']
xrefs: [('github-private-vulnerability-reporting.md', '9', ''), ('github-private-vulnerability-reporting.md', '39', '40'), ('github-private-vulnerability-reporting.md', '23', ''), ('cna-assignment-and-vulnerability-rules.md', '9', '13'), ('cna-assignment-and-vulnerability-rules.md', '32', ''), ('cna-assignment-and-vulnerability-rules.md', '36', ''), ('coordinated-disclosure-timelines.md', '7', '8')]
```
19 gate-countable data rows (G1..G19); the `id` header and the `---` separator are the other two pipe-lines and
are not counted by the gate. No ASCII double quote and no curly single quote exists anywhere in the entry, so no
curly quote can be uncited (checked: `ascii-dquote count 2` before one edit, `0` after; `curly-single count 0 0`).

### F-4 — The committed gate on a synthetic tree carrying this entry: 7/7

Commands:
```
python3 .ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode positive --dir $S/tree --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin
cp .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryB.draft/github-repository-security-advisories.md $S/tree/corpus/knowledge/github-repository-security-advisories.md
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-f29-gate.py --root $S/tree --work $S/work
```
Output:
```
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=19 xrefs=7/7 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=45 located=45 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```
This is the entry's own score:
H2 `table-rows=19`, `xrefs=7/7`, `anchored=1`; H5 `spans=45 located=45 failed=0 uncited=0 cores=5/5`.

### F-5 — Do-nothing control: the base export still reads 1/7

Commands:
```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus | tar -x -C $S/base
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-f29-gate.py --root $S/base --work $S/work
```
Output:
```
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=entry-absent advisor-named=
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=0 read=manifest-absent
gate H5 pass=0 read=entry-absent advisor-named=
gate H6 pass=0 read=entry-absent advisor-named=
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=1/7 exit=1
```
This matches C2's `expect_before` (`f29-gate fixed=1/7 exit=1`).

### F-6 — Freeze/live lane tree reads 2/7 (entry not yet landed, as expected for a draft seat)

Command: `python3 corpus/instruments/r46-f29-gate.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --work $S/work`
Output:
```
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=entry-absent advisor-named=
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=entry-absent advisor-named=
gate H6 pass=0 read=entry-absent advisor-named=
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=2/7 exit=1
```
Matches C2's `freeze_tree_reading` (`f29-gate fixed=2/7 exit=1 at the freeze tree`). The live lane is untouched by
this seat: I wrote nothing under `corpus/`.

### F-7 — Gate's own junk and fabricated controls do not pass

Commands: `python3 .ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode junk|fabricated --dir $S/t-<mode> --lane <lane>`,
then the gate on each tree. Output for both modes (tail):
```
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=6/7 exit=1
```

### F-8 — Four mutants of *this* entry are each caught (discrimination against a do-nothing control on my own text)

Each mutant was applied to the draft, the tree rebuilt from the same fixture, and the gate re-run:

M1 — fabricated quote (`reviews the request within 72 hours` → `reviews the request within one business day`):
```
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=19 xrefs=7/7 anchored=1
gate H5 pass=0 read=spans=45 located=43 failed=2 uncited=0 cores=4/5
f29-gate fixed=6/7 exit=1
```
M2 — junk: the five frozen core phrases replaced with paraphrases:
```
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=19 xrefs=7/7 anchored=1
gate H5 pass=0 read=spans=45 located=34 failed=11 uncited=0 cores=2/5
f29-gate fixed=6/7 exit=1
```
M3 — the `recheck:` line removed:
```
gate H2 pass=0 read=source=1 verified-at=1 recheck=0 sections=4/4 full=4/4 table-rows=19 xrefs=7/7 anchored=1
gate H5 pass=1 read=spans=45 located=45 failed=0 uncited=0 cores=5/5
f29-gate fixed=6/7 exit=1
```
M4 — the F28/F07 cross-references renamed away:
```
gate H2 pass=0 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=19 xrefs=0/0 anchored=0
gate H5 pass=1 read=spans=45 located=45 failed=0 uncited=0 cores=5/5
f29-gate fixed=6/7 exit=1
```
Restored to the honest entry, the same tree reads again:
```
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=19 xrefs=7/7 anchored=1
gate H5 pass=1 read=spans=45 located=45 failed=0 uncited=0 cores=5/5
f29-gate fixed=7/7 exit=0
```
So the 7/7 in F-4 is produced by this entry's content and is lost the moment any of the four load-bearing
elements is broken.

### F-9 — The entry's own `recheck:` line is true today

Command: `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074`
Output:
```
S074:sha256 OK
S074:Q1 OK occurrences=1 anchor=10-ok
S074:Q2 OK occurrences=1 anchor=13-ok
S074:Q3 OK occurrences=1 anchor=17-ok
S074:Q4 OK occurrences=1 anchor=24-ok
S074:Q5 OK occurrences=1 anchor=25-ok
S074:Q6 OK occurrences=1 anchor=25-ok
S074:Q7 OK occurrences=1 anchor=26-ok
S074:Q8 OK occurrences=1 anchor=31-ok
S074:Q9 OK occurrences=1 anchor=38-ok
recheck-exit=0
```

### F-10 — The entry's own sweep claim, re-run

Command: `grep -n -i -E 'timeline|embargo|deadline|reward|bount' corpus/source-snapshots/round-46-a2/S074.txt`
Output: (no lines printed) `grep-exit=1`. This is what the entry's Limits bullet asserts ("printed nothing (grep exit 1)").

### F-11 — Base-state absence sweep and frontier count (C2 `before` values, re-measured)

Commands: `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → `28`;
`grep -rliE 'repository securit. advisor|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md | wc -l` → `2`.
After L1 lands the entry, README, and the SOURCES row, the sweep should read 4 (README, SOURCES, the entry, plus
one pre-existing hit). I did not add the README row or the SOURCES row: those are L1 surfaces.

### F-12 — Quote self-check: 45/45 located

Command (run over the draft and the pinned capture): locate each curly quote in the normalised window of its cited
line, and enforce the 25-word ceiling. Output: `quotes: 45` / `all-located: True`, and `grep -c "located=True"
self-check.txt` → `45`. Every quote's cited line is pasted in Appendix A.

## Limitations

- The 7/7 in F-4 is a **synthetic** tree built by the wave's own fixture (`controls/f29-fixture.py`), which supplies
  the F29 README row, the SOURCES.md row and the 66-file knowledge directory. The seat did not write those; only
  L1 can. The live lane tree reads 2/7 (F-6) because the entry is not landed and the row does not exist.
- H1/H3/H6/H7 were therefore exercised against the fixture's synthetic siblings, not against L1's final tree; those
  four limbs are L1's to re-run after integration.
- All quotes are checked against the **pinned capture** `corpus/source-snapshots/round-46-a2/S074.txt`
  (sha256 verified). Nothing here checks GitHub's live page; the entry's own `recheck:` line says so. The
  non-author closure must re-open the page to confirm the nine quoted sentences.
- The capture is one overview page. The advisory form's fields, the creation flow, the post-publication editing
  flow, the REST API endpoints and the Advisory Database edit flow are named as link text in the capture but their
  bodies are **not** held; the entry says so in Limits and does not import them.
- Two `72 hours` statements exist in the capture and are different clocks (CVE-request review at S074.txt:25,
  Dependabot step at S074.txt:36). The entry keeps them apart; a reviewer should check that reading against the
  live page, since the capture alone does not date either.
- The F28 and F07 cross-references were verified by line number in this lane's corpus today; if L1 re-generates
  either file, those line numbers may move and the entry's `corpus/knowledge/...:N` cites must be re-checked
  (the gate resolves them and fails H2 on a stale number — see M4).
- The entry is documentation only: it instructs no advisory creation, no CVE request, no contact with GitHub or any
  maintainer, and no probing of any repository. No live-target testing was attempted.
- Tooling: **no tool was installed or updated** by this seat (python3 and git already present; nothing needed
  beyond them), so no tool/version/channel record is owed. `~/.omp/agent/RULES.md` was read first; no pacman
  transaction was attempted (all pacman transactions are paused host-wide).
- I created no git repository and made no commit, so no `git rev-parse --show-toplevel` assertion was owed; the
  only git calls were read-only (`rev-parse --show-toplevel`, `archive`), each naming `-C <lane>`; the toplevel
  printed `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
- Scratch `/fast/scratch/hyaku/kasegi-r46/R46bScribeEntryB` was removed after the receipts above were copied into
  this Report and the draft directory.

## Appendix A — quote self-check (each quote with the `sed -n 'Np'` line verified)

The same content is at `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryB.draft/self-check.txt`.

Self-check: every curly quote in github-repository-security-advisories.md, with the snapshot line it was verified against.
Command per quote: sed -n '<N>p' corpus/source-snapshots/round-46-a2/S074.txt
quote-count=45  distinct-lines=21

Q01 cite=S074.txt:3  words=20  located=True
  quote: “You can use repository security advisories to privately discuss, fix, and publish information about security vulnerabilities in your public repository.”
  $ sed -n '3p' corpus/source-snapshots/round-46-a2/S074.txt
  You can use repository security advisories to privately discuss, fix, and publish information about security vulnerabilities in your public repository.

Q02 cite=S074.txt:6  words=14  located=True
  quote: “Repository security advisories and private vulnerability reporting are available for public repositories on GitHub.com”
  $ sed -n '6p' corpus/source-snapshots/round-46-a2/S074.txt
  Repository security advisories and private vulnerability reporting are available for public repositories on GitHub.com

Q03 cite=S074.txt:10  words=19  located=True
  quote: “Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.”
  $ sed -n '10p' corpus/source-snapshots/round-46-a2/S074.txt
  Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project. After collaborating on a fix, repository maintainers can publish the security advisory to publicly disclose the security vulnerability to the project's community. By publishing security advisories, repository maintainers make it easier for their community to update package dependencies and research the impact of the security vulnerabilities.

Q04 cite=S074.txt:12  words=20  located=True
  quote: “Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project.”
  $ sed -n '12p' corpus/source-snapshots/round-46-a2/S074.txt
  Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project.

Q05 cite=S074.txt:13  words=11  located=True
  quote: “Privately collaborate to fix the vulnerability in a temporary private fork.”
  $ sed -n '13p' corpus/source-snapshots/round-46-a2/S074.txt
  Privately collaborate to fix the vulnerability in a temporary private fork.

Q06 cite=S074.txt:38  words=17  located=True
  quote: “Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory.”
  $ sed -n '38p' corpus/source-snapshots/round-46-a2/S074.txt
  Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory. If you don't, the advisory will be published without a fixed version, and Dependabot will alert your users about the issue, without offering any safe version to update to.

Q07 cite=S074.txt:25  words=11  located=True
  quote: “Requesting a CVE identification number doesn't make your security advisory public.”
  $ sed -n '25p' corpus/source-snapshots/round-46-a2/S074.txt
  When you create a security advisory for a public repository on GitHub, you have the option of providing an existing CVE identification number for the security vulnerability. If you want a CVE identification number for the security vulnerability in your project, and don't already have one, you can request a CVE identification number from GitHub. GitHub usually reviews the request within 72 hours. Requesting a CVE identification number doesn't make your security advisory public. If your security advisory is eligible for a CVE, GitHub will reserve a CVE identification number for your advisory. We'll then publish the CVE details after you make your security advisory public. Anyone with admin permissions to a security advisory can request a CVE identification number.

Q08 cite=S074.txt:24  words=15  located=True
  quote: “GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.”
  $ sed -n '24p' corpus/source-snapshots/round-46-a2/S074.txt
  GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers. For more information, see About CVE and CVE Numbering Authorities on the CVE website.

Q09 cite=S074.txt:25  words=8  located=True
  quote: “GitHub usually reviews the request within 72 hours.”
  $ sed -n '25p' corpus/source-snapshots/round-46-a2/S074.txt
  When you create a security advisory for a public repository on GitHub, you have the option of providing an existing CVE identification number for the security vulnerability. If you want a CVE identification number for the security vulnerability in your project, and don't already have one, you can request a CVE identification number from GitHub. GitHub usually reviews the request within 72 hours. Requesting a CVE identification number doesn't make your security advisory public. If your security advisory is eligible for a CVE, GitHub will reserve a CVE identification number for your advisory. We'll then publish the CVE details after you make your security advisory public. Anyone with admin permissions to a security advisory can request a CVE identification number.

Q10 cite=S074.txt:36  words=16  located=True
  quote: “This process can take up to 72 hours and GitHub may contact you for more information.”
  $ sed -n '36p' corpus/source-snapshots/round-46-a2/S074.txt
  GitHub will review each published security advisory, add it to the GitHub Advisory Database, and may use the security advisory to send Dependabot alerts to affected repositories. If the security advisory comes from a fork, we'll only send an alert if the fork owns a package, published under a unique name, on a public package registry. This process can take up to 72 hours and GitHub may contact you for more information.

Q11 cite=S074.txt:3  words=20  located=True
  quote: “You can use repository security advisories to privately discuss, fix, and publish information about security vulnerabilities in your public repository.”
  $ sed -n '3p' corpus/source-snapshots/round-46-a2/S074.txt
  You can use repository security advisories to privately discuss, fix, and publish information about security vulnerabilities in your public repository.

Q12 cite=S074.txt:6  words=14  located=True
  quote: “Repository security advisories and private vulnerability reporting are available for public repositories on GitHub.com”
  $ sed -n '6p' corpus/source-snapshots/round-46-a2/S074.txt
  Repository security advisories and private vulnerability reporting are available for public repositories on GitHub.com

Q13 cite=S074.txt:10  words=19  located=True
  quote: “Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.”
  $ sed -n '10p' corpus/source-snapshots/round-46-a2/S074.txt
  Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project. After collaborating on a fix, repository maintainers can publish the security advisory to publicly disclose the security vulnerability to the project's community. By publishing security advisories, repository maintainers make it easier for their community to update package dependencies and research the impact of the security vulnerabilities.

Q14 cite=S074.txt:12  words=20  located=True
  quote: “Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project.”
  $ sed -n '12p' corpus/source-snapshots/round-46-a2/S074.txt
  Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project.

Q15 cite=S074.txt:13  words=11  located=True
  quote: “Privately collaborate to fix the vulnerability in a temporary private fork.”
  $ sed -n '13p' corpus/source-snapshots/round-46-a2/S074.txt
  Privately collaborate to fix the vulnerability in a temporary private fork.

Q16 cite=S074.txt:14  words=16  located=True
  quote: “Publish the security advisory to alert your community of the vulnerability once a patch is released.”
  $ sed -n '14p' corpus/source-snapshots/round-46-a2/S074.txt
  Publish the security advisory to alert your community of the vulnerability once a patch is released.

Q17 cite=S074.txt:15  words=21  located=True
  quote: “You can also use repository security advisories to republish the details of a security vulnerability that you have already disclosed elsewhere”
  $ sed -n '15p' corpus/source-snapshots/round-46-a2/S074.txt
  You can also use repository security advisories to republish the details of a security vulnerability that you have already disclosed elsewhere by copying and pasting the details of the vulnerability into a new security advisory.

Q18 cite=S074.txt:17  words=12  located=True
  quote: “You can give credit to individuals who contributed to a security advisory.”
  $ sed -n '17p' corpus/source-snapshots/round-46-a2/S074.txt
  You can give credit to individuals who contributed to a security advisory. For more information, see Creating a repository security advisory.

Q19 cite=S074.txt:19  words=17  located=True
  quote: “If you created a security advisory in your repository, the security advisory will stay in your repository.”
  $ sed -n '19p' corpus/source-snapshots/round-46-a2/S074.txt
  If you created a security advisory in your repository, the security advisory will stay in your repository. We publish security advisories for any of the ecosystems supported by the dependency graph to the GitHub Advisory Database on github.com/advisories. Anyone can submit a change to an advisory published in the GitHub Advisory Database. For more information, see Editing security advisories in the GitHub Advisory Database.

Q20 cite=S074.txt:19  words=21  located=True
  quote: “We publish security advisories for any of the ecosystems supported by the dependency graph to the GitHub Advisory Database on github.com/advisories.”
  $ sed -n '19p' corpus/source-snapshots/round-46-a2/S074.txt
  If you created a security advisory in your repository, the security advisory will stay in your repository. We publish security advisories for any of the ecosystems supported by the dependency graph to the GitHub Advisory Database on github.com/advisories. Anyone can submit a change to an advisory published in the GitHub Advisory Database. For more information, see Editing security advisories in the GitHub Advisory Database.

Q21 cite=S074.txt:20  words=18  located=True
  quote: “If a security advisory is specifically for npm, we also publish the advisory to the npm security advisories.”
  $ sed -n '20p' corpus/source-snapshots/round-46-a2/S074.txt
  If a security advisory is specifically for npm, we also publish the advisory to the npm security advisories. For more information, see npmjs.com/advisories.

Q22 cite=S074.txt:24  words=15  located=True
  quote: “GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.”
  $ sed -n '24p' corpus/source-snapshots/round-46-a2/S074.txt
  GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers. For more information, see About CVE and CVE Numbering Authorities on the CVE website.

Q23 cite=S074.txt:25  words=8  located=True
  quote: “GitHub usually reviews the request within 72 hours.”
  $ sed -n '25p' corpus/source-snapshots/round-46-a2/S074.txt
  When you create a security advisory for a public repository on GitHub, you have the option of providing an existing CVE identification number for the security vulnerability. If you want a CVE identification number for the security vulnerability in your project, and don't already have one, you can request a CVE identification number from GitHub. GitHub usually reviews the request within 72 hours. Requesting a CVE identification number doesn't make your security advisory public. If your security advisory is eligible for a CVE, GitHub will reserve a CVE identification number for your advisory. We'll then publish the CVE details after you make your security advisory public. Anyone with admin permissions to a security advisory can request a CVE identification number.

Q24 cite=S074.txt:25  words=11  located=True
  quote: “Requesting a CVE identification number doesn't make your security advisory public.”
  $ sed -n '25p' corpus/source-snapshots/round-46-a2/S074.txt
  When you create a security advisory for a public repository on GitHub, you have the option of providing an existing CVE identification number for the security vulnerability. If you want a CVE identification number for the security vulnerability in your project, and don't already have one, you can request a CVE identification number from GitHub. GitHub usually reviews the request within 72 hours. Requesting a CVE identification number doesn't make your security advisory public. If your security advisory is eligible for a CVE, GitHub will reserve a CVE identification number for your advisory. We'll then publish the CVE details after you make your security advisory public. Anyone with admin permissions to a security advisory can request a CVE identification number.

Q25 cite=S074.txt:26  words=14  located=True
  quote: “GitHub cannot assign CVEs to your project if it is covered by another CNA.”
  $ sed -n '26p' corpus/source-snapshots/round-46-a2/S074.txt
  If you already have a CVE you want to use, for example, if you use a CVE Numbering Authority (CNA) other than GitHub, add the CVE to the security advisory form. This may happen, for example, if you want to get the advisory consistent with other communications you plan to send out at publication time. GitHub cannot assign CVEs to your project if it is covered by another CNA.

Q26 cite=S074.txt:31  words=22  located=True
  quote: “Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.”
  $ sed -n '31p' corpus/source-snapshots/round-46-a2/S074.txt
  Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.

Q27 cite=S074.txt:32  words=9  located=True
  quote: “Collaborators can view the conversation history of the advisory.”
  $ sed -n '32p' corpus/source-snapshots/round-46-a2/S074.txt
  Collaborators can view the conversation history of the advisory.

Q28 cite=S074.txt:36  words=16  located=True
  quote: “This process can take up to 72 hours and GitHub may contact you for more information.”
  $ sed -n '36p' corpus/source-snapshots/round-46-a2/S074.txt
  GitHub will review each published security advisory, add it to the GitHub Advisory Database, and may use the security advisory to send Dependabot alerts to affected repositories. If the security advisory comes from a fork, we'll only send an alert if the fork owns a package, published under a unique name, on a public package registry. This process can take up to 72 hours and GitHub may contact you for more information.

Q29 cite=S074.txt:38  words=15  located=True
  quote: “you should add a fix version to a security advisory prior to publishing the advisory”
  $ sed -n '38p' corpus/source-snapshots/round-46-a2/S074.txt
  Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory. If you don't, the advisory will be published without a fixed version, and Dependabot will alert your users about the issue, without offering any safe version to update to.

Q30 cite=S074.txt:17  words=5  located=True
  quote: “Creating a repository security advisory”
  $ sed -n '17p' corpus/source-snapshots/round-46-a2/S074.txt
  You can give credit to individuals who contributed to a security advisory. For more information, see Creating a repository security advisory.

Q31 cite=S074.txt:16  words=7  located=True
  quote: “REST API
  endpoints for repository security advisories”
  $ sed -n '16p' corpus/source-snapshots/round-46-a2/S074.txt
  You can also use the REST API to create, list, and update repository security advisories. For more information, see REST API endpoints for repository security advisories.

Q32 cite=S074.txt:34  words=5  located=True
  quote: “Editing a
  repository security advisory”
  $ sed -n '34p' corpus/source-snapshots/round-46-a2/S074.txt
  If you need to update or correct information in a security advisory that you've published, you can edit the security advisory. See Editing a repository security advisory.

Q33 cite=S074.txt:19  words=8  located=True
  quote: “Editing security
  advisories in the GitHub Advisory Database”
  $ sed -n '19p' corpus/source-snapshots/round-46-a2/S074.txt
  If you created a security advisory in your repository, the security advisory will stay in your repository. We publish security advisories for any of the ecosystems supported by the dependency graph to the GitHub Advisory Database on github.com/advisories. Anyone can submit a change to an advisory published in the GitHub Advisory Database. For more information, see Editing security advisories in the GitHub Advisory Database.

Q34 cite=S074.txt:23  words=16  located=True
  quote: “The security advisory form on GitHub is a
  standardized form that matches the CVE description format.”
  $ sed -n '23p' corpus/source-snapshots/round-46-a2/S074.txt
  GitHub Security Advisories builds upon the foundation of the Common Vulnerabilities and Exposures (CVE) list. The security advisory form on GitHub is a standardized form that matches the CVE description format.

Q35 cite=S074.txt:16  words=15  located=True
  quote: “You can also use the REST API to create, list, and update repository
  security advisories.”
  $ sed -n '16p' corpus/source-snapshots/round-46-a2/S074.txt
  You can also use the REST API to create, list, and update repository security advisories. For more information, see REST API endpoints for repository security advisories.

Q36 cite=S074.txt:33  words=11  located=True
  quote: “The URL of a security
  advisory does not change after publication.”
  $ sed -n '33p' corpus/source-snapshots/round-46-a2/S074.txt
  The URL of a security advisory does not change after publication.

Q37 cite=S074.txt:38  words=17  located=True
  quote: “Whenever possible, you should add a fix version to a security
  advisory prior to publishing the advisory.”
  $ sed -n '38p' corpus/source-snapshots/round-46-a2/S074.txt
  Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory. If you don't, the advisory will be published without a fixed version, and Dependabot will alert your users about the issue, without offering any safe version to update to.

Q38 cite=S074.txt:12  words=20  located=True
  quote: “Create a
   draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your
   project.”
  $ sed -n '12p' corpus/source-snapshots/round-46-a2/S074.txt
  Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project.

Q39 cite=S074.txt:13  words=11  located=True
  quote: “Privately collaborate to fix the vulnerability in a
   temporary private fork.”
  $ sed -n '13p' corpus/source-snapshots/round-46-a2/S074.txt
  Privately collaborate to fix the vulnerability in a temporary private fork.

Q40 cite=S074.txt:25  words=11  located=True
  quote: “Requesting a CVE
   identification number doesn't make your security advisory public.”
  $ sed -n '25p' corpus/source-snapshots/round-46-a2/S074.txt
  When you create a security advisory for a public repository on GitHub, you have the option of providing an existing CVE identification number for the security vulnerability. If you want a CVE identification number for the security vulnerability in your project, and don't already have one, you can request a CVE identification number from GitHub. GitHub usually reviews the request within 72 hours. Requesting a CVE identification number doesn't make your security advisory public. If your security advisory is eligible for a CVE, GitHub will reserve a CVE identification number for your advisory. We'll then publish the CVE details after you make your security advisory public. Anyone with admin permissions to a security advisory can request a CVE identification number.

Q41 cite=S074.txt:24  words=15  located=True
  quote: “GitHub is a CVE Numbering Authority (CNA) and is authorized to assign
   CVE identification numbers.”
  $ sed -n '24p' corpus/source-snapshots/round-46-a2/S074.txt
  GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers. For more information, see About CVE and CVE Numbering Authorities on the CVE website.

Q42 cite=S074.txt:26  words=14  located=True
  quote: “GitHub cannot assign CVEs to your project if it is covered by another CNA.”
  $ sed -n '26p' corpus/source-snapshots/round-46-a2/S074.txt
  If you already have a CVE you want to use, for example, if you use a CVE Numbering Authority (CNA) other than GitHub, add the CVE to the security advisory form. This may happen, for example, if you want to get the advisory consistent with other communications you plan to send out at publication time. GitHub cannot assign CVEs to your project if it is covered by another CNA.

Q43 cite=S074.txt:38  words=15  located=True
  quote: “you should add a fix version to a security advisory prior to
   publishing the advisory”
  $ sed -n '38p' corpus/source-snapshots/round-46-a2/S074.txt
  Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory. If you don't, the advisory will be published without a fixed version, and Dependabot will alert your users about the issue, without offering any safe version to update to.

Q44 cite=S074.txt:31  words=22  located=True
  quote: “Anyone can see the current version of the advisory data, as well as any advisory credits that the
credited users have accepted.”
  $ sed -n '31p' corpus/source-snapshots/round-46-a2/S074.txt
  Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.

Q45 cite=S074.txt:32  words=9  located=True
  quote: “Collaborators can view the conversation history of the
advisory.”
  $ sed -n '32p' corpus/source-snapshots/round-46-a2/S074.txt
  Collaborators can view the conversation history of the advisory.

