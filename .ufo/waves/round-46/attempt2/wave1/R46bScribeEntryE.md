VERDICT: DRAFT-READY

# Seat R46bScribeEntryE — C2 entry drafter E (F29, maintainer-side advisory lifecycle)

## What was built

Draft F29 knowledge entry at
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/github-repository-security-advisories.md`
(7988 bytes; 43 lines). It is a draft only: the lane's `corpus/knowledge/` was not touched, no
git/jj command was run, and no sibling draft was read.

Shape follows the F28 house shape read from
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/github-private-vulnerability-reporting.md`:
title, blank, `source:` / `verified-at:` / `recheck:` trio, then exactly the four sections
`## Scope and decision rule`, `## Overlap and novelty`, `## Limits`, `## Falsifiable package rule`,
with a three-column `| id | observed question | ground |` table (9 rows, G1..G9), each ground cell
carrying one curly quotation and its ` (`S074.txt:N`)` locator.

All nine mandated facts are inside located quotations:
private discuss-and-fix definition (10), temporary private fork (13), credit (17), GitHub as CNA (24),
72-hour review clock (25), requesting does not publish (25), other-CNA boundary (26), publication
visibility (31), fix-version duty (38). The decision rule is the package-actable one: draft before
publish, fix version before publish, CVE request while private.

## Findings — commands run and printed output

### 1. Gate on a synthetic tree carrying this exact draft (positive)

Command:
`python3 .ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode positive --dir <S>/tree` then
`cp <draft> <S>/tree/corpus/knowledge/github-repository-security-advisories.md` then
`python3 corpus/instruments/r46-f29-gate.py --root <S>/tree --work <S>/work`

Output:
```
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=9 xrefs=4/4 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=19 located=19 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```
Exit status 0. Receipt: `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/receipts/gate-positive.txt`.

### 2. Source re-check of the pinned capture

Command:
`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074`

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
rc=0
```
Receipt: `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/receipts/source-recheck-S074.txt`.

### 3. Quote self-check — the `sed -n 'Np'` line behind every quotation

Command (one per quoted line, 3 10 12 13 14 16 17 19 23 24 25 26 31 34 38):
`sed -n '<N>p' corpus/source-snapshots/round-46-a2/S074.txt`

Output (abridged to the first sentence of each line; full text in the receipt):
```
sed -n '3p' -> You can use repository security advisories to privately discuss, fix, and publish information about security vulnerabilities in your public repository.
sed -n '10p' -> Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project. After collaborating on a fix, ...
sed -n '12p' -> Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project.
sed -n '13p' -> Privately collaborate to fix the vulnerability in a temporary private fork.
sed -n '14p' -> Publish the security advisory to alert your community of the vulnerability once a patch is released.
sed -n '16p' -> You can also use the REST API to create, list, and update repository security advisories. For more information, see REST API endpoints for repository security advisories.
sed -n '17p' -> You can give credit to individuals who contributed to a security advisory. For more information, see Creating a repository security advisory.
sed -n '19p' -> If you created a security advisory in your repository, the security advisory will stay in your repository. We publish security advisories for any of the ecosystems ...
sed -n '23p' -> GitHub Security Advisories builds upon the foundation of the Common Vulnerabilities and Exposures (CVE) list. The security advisory form on GitHub is a standardized form that matches the CVE description format.
sed -n '24p' -> GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers. For more information, see About CVE and CVE Numbering Authorities on the CVE website.
sed -n '25p' -> When you create a security advisory for a public repository on GitHub, you have the option of providing an existing CVE identification number ... GitHub usually reviews the request within 72 hours. Requesting a CVE identification number doesn't make your security advisory public. ...
sed -n '26p' -> If you already have a CVE you want to use, for example, if you use a CVE Numbering Authority (CNA) other than GitHub, add the CVE to the security advisory form. ... GitHub cannot assign CVEs to your project if it is covered by another CNA.
sed -n '31p' -> Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.
sed -n '34p' -> If you need to update or correct information in a security advisory that you've published, you can edit the security advisory. See Editing a repository security advisory.
sed -n '38p' -> Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory. If you don't, the advisory will be published without a fixed version, and Dependabot will alert your users about the issue, without offering any safe version to update to.
```
Receipt: `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/receipts/quote-selfcheck-sed.txt`.

### 4. Independent quote-locator re-implementation (not the gate's own code path)

A standalone script re-located every quotation in the draft against the snapshot using the gate's
own `cite`/`curly` regexes lifted from `r46-f29-gate.py` lines 289-290, then re-checked word counts,
line ranges and the five frozen cores. Output:
```
spans=19 located=19 failed=0 uncited=0
core privately discuss and fix a security vulnerability True
core temporary private fork True
core authorized to assign CVE identification numbers True
core reviews the request within 72 hours True
core add a fix version to a security advisory prior to publishing True
```
Character census of the draft: 19 `“`, 19 `”`, 4 `—`, 0 ASCII double quotes, 0 curly single quotes —
so no uncited quotation can hide in an ASCII-quoted or single-quoted span.

### 5. Do-nothing controls (the gate discriminates against a plausible-but-empty entry)

Command: `python3 .ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode <junk|fabricated> --dir <S>/tree-<mode>`
then `python3 corpus/instruments/r46-f29-gate.py --root <S>/tree-<mode> --work <S>/work-<mode>`

Output:
```
== fixture junk ==
gate H5 pass=0 read=spans=7 located=2 failed=5 uncited=0 cores=0/5
f29-gate fixed=6/7 exit=1
== fixture fabricated ==
gate H5 pass=0 read=spans=7 located=5 failed=2 uncited=0 cores=4/5
f29-gate fixed=6/7 exit=1
```
Two mutations of *this* draft, same command shape:
```
== mutated: fabricated quote text (72 hours -> one business day) ==
gate H5 pass=0 read=spans=19 located=18 failed=1 uncited=0 cores=4/5
f29-gate fixed=6/7 exit=1
== mutated: uncited curly quote added ==
gate H5 pass=0 read=spans=19 located=19 failed=0 uncited=1 cores=5/5
f29-gate fixed=6/7 exit=1
```
Receipt: `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/receipts/gate-negative-controls.txt`.

### 6. Cross-reference line numbers verified in the two sibling entries

Command: `sed -n '9p;13p;35p' corpus/knowledge/github-private-vulnerability-reporting.md` and
`sed -n '9,13p;36p' corpus/knowledge/cna-assignment-and-vulnerability-rules.md`

Observed: F28 line 9 is the reporter-side scope sentence, line 13 the reporter-side decision rule,
line 35 its "What is new here" paragraph (reporter-side required-field list, submission effects,
enablement precondition). F07 lines 9-13 are the program assignment-scope paragraph and line 36 is
the table row for rule 4.2.1.1 (first opportunity to assign). The draft cites
`corpus/knowledge/github-private-vulnerability-reporting.md:9-13`, `:35` and
`corpus/knowledge/cna-assignment-and-vulnerability-rules.md:9-13`, `:36` — all inside the sibling
files' real line counts (49 and 80 lines). Gate H2 reports `xrefs=4/4`.

## Touched surfaces

- `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/github-repository-security-advisories.md` (new, the draft entry)
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/receipts/gate-positive.txt`
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/receipts/gate-negative-controls.txt`
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/receipts/quote-selfcheck-sed.txt`
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/receipts/source-recheck-S074.txt`
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.md` (this report)

Nothing else. No commit, no push, no mutating git/jj command, no fleet-repo or sibling-lane write,
no edit to `corpus/knowledge/`, `corpus/README.md`, `corpus/SOURCES.md`, MANIFEST.json or
`.ufo/state`. Scratch `/fast/scratch/hyaku/kasegi-r46/R46bScribeEntryE/` was removed after the
receipts were copied into the draft directory.

## Out of scope (for the L1, not for this seat)

- L1 must add the F29 row to `corpus/README.md` and the S074 row to `corpus/SOURCES.md`, and copy
  the draft to `corpus/knowledge/github-repository-security-advisories.md`. The entry will then be
  the 66th file in `corpus/knowledge/`, which gate limb H6 requires.
- The frozen `r46-c1-gate.py` / `r46-c2-gate.py` and `claims.json` were read only; no amendment was
  made.

## Limitations

- The gate result above is from a synthetic tree built by the round-46 control fixture
  (`f29-fixture.py --mode positive`), which supplies its own README F29 row, SOURCES.md S074 row and
  manifest copy. The H1, H3, H6 and H7 limbs therefore exercise the fixture's rows, not L1's real
  integration. The limbs this seat actually owns — H2 (entry structure, table, cross-references) and
  H5 (located quotations) — ran against this exact draft bytes.
- H5's `located` check accepts any quotation that the re-locator finds after whitespace/markup
  normalisation; it does not adjudicate whether a quotation is the most apt sentence for its row.
  The semantic pairing of each G-row question to its quotation was checked by hand against the
  `sed -n 'Np'` lines in finding 3.
- The capture is a text rendering of the GitHub Docs page, not the live page. Nothing here checks
  GitHub's current content; the `recheck:` line re-verifies the pinned sha256 and the nine manifest
  quotes only.
- The page's own wording is a platform overview, not a normative standard. The entry's decision rule
  is stated as what a package may assert about GitHub-conformance, not as GitHub policy, and the
  sibling pages the capture names (form fields, editing flow, REST API, Advisory Database edit flow)
  are not held by this capture — recorded under `## Limits`.
- Live-target testing was not attempted and is out of scope: this corpus is documentation only.
- No tools were installed or upgraded, so there is no tool/version/channel record to report.

Report: .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.md
