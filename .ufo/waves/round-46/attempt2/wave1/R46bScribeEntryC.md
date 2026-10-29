VERDICT: DRAFT-READY

# R46bScribeEntryC — F29 knowledge entry, seat C draft (round-46 attempt 2, independent)

Scope: one artefact only — the F29 entry draft
`.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/github-repository-security-advisories.md`.
I read the source myself (`corpus/source-snapshots/round-46-a2/S074.txt`), the house shape
(`corpus/knowledge/github-private-vulnerability-reporting.md`, F28), the F07 twin
(`corpus/knowledge/cna-assignment-and-vulnerability-rules.md`), the counter
(`corpus/instruments/r46-f29-gate.py`) and the R50 control (`…/controls/f29-fixture.py`).
No sibling entry draft was opened (the sibling draft files `R46bScribeEntryB.draft/` and
`R46bScribeEntryF.draft/` were seen only as directory names in one `ls`, never read).
No product file, counter, claims file, SOURCES row, README row or manifest was written or
edited; no git/jj mutation of any kind; scratch `/fast/scratch/hyaku/kasegi-r46/R46bScribeEntryC/`
removed after the receipts below were copied into my draft directory.

## Finding 1 — Built: the entry draft, and the nine mandated facts each inside a located quote

```
$ wc -c .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/github-repository-security-advisories.md
12453 .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/github-repository-security-advisories.md
$ grep -n '^## ' .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/github-repository-security-advisories.md
7:## Scope and decision rule
29:## Overlap and novelty
38:## Limits
48:## Falsifiable package rule
$ grep -c '^| G' .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/github-repository-security-advisories.md
11
$ grep -c 'S074.txt:' .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/github-repository-security-advisories.md
23
```

Exactly the four required sections, exactly one `source:`/`verified-at:`/`recheck:` trio in
lines 1-5, an 11-row `| id | observed question | ground |` table (G1-G11), and every
quotation curly-quoted with an immediately following ` (`S074.txt:N`)` locator. The nine
mandated facts, each in its own located quote:

| mandated item | quote in the entry | locator |
|---|---|---|
| private discuss-and-fix definition | “Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.” | S074.txt:10 |
| temporary private fork | “Privately collaborate to fix the vulnerability in a temporary private fork.” | S074.txt:13 |
| credit | “You can give credit to individuals who contributed to a security advisory.” | S074.txt:17 |
| GitHub as CNA | “GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.” | S074.txt:24 |
| 72-hour review clock | “GitHub usually reviews the request within 72 hours.” | S074.txt:25 |
| requesting does not publish | “Requesting a CVE identification number doesn't make your security advisory public.” | S074.txt:25 |
| other-CNA boundary | “GitHub cannot assign CVEs to your project if it is covered by another CNA.” | S074.txt:26 |
| publication visibility | “Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.” | S074.txt:31 |
| fix-version duty | “you should add a fix version to a security advisory prior to publishing the advisory” | S074.txt:38 |

## Finding 2 — Mechanical target: the F29 counter reads 7/7 with this entry

Tree: the R50 control's synthetic positive tree
(`python3 .ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode positive --dir $S/tree --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin`)
with my draft copied over its entry slot
(`cp …/R46bScribeEntryC.draft/github-repository-security-advisories.md $S/tree/corpus/knowledge/github-repository-security-advisories.md`).

```
$ TMPDIR=$S/work python3 corpus/instruments/r46-f29-gate.py --root $S/tree --work $S/work
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=11 xrefs=10/10 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=32 located=32 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```

Receipt: `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/receipt-gate-positive.txt`.
H5 is the limb that grades this seat's work: 32 quote spans, 32 located, 0 failed, 0 uncited,
all 5 frozen cores present in live located spans.

## Finding 3 — Do-nothing control: the same tree with a marker-only entry reads 4/7

Same fixture tree, entry replaced by prose-only filler with the same provenance trio and the
same four headings but no quotations:

```
$ TMPDIR=$S/work python3 corpus/instruments/r46-f29-gate.py --root $S/ctrlA/tree --work $S/work
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=0 read=source=1 verified-at=1 recheck=1 sections=4/4 full=0/4 table-rows=0 xrefs=0/0 anchored=0
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=spans=0 located=0 failed=0 uncited=0 cores=0/5
gate H6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=0 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=4/7 exit=1
```

Receipt: `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/receipt-gate-control-marker.txt`.
So the 7/7 in Finding 2 is produced by this entry's content, not by the fixture.

## Finding 4 — Fabrication control: wording the capture does not hold reads 6/7 with H5 red

Same tree and same entry, with one quoted span rewritten to text the snapshot does not hold
(`reviews the request within 72 hours` -> `reviews the request within one business day`),
citations kept:

```
$ TMPDIR=$S/work python3 corpus/instruments/r46-f29-gate.py --root $S/ctrlB/tree --work $S/work
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=11 xrefs=10/10 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=spans=32 located=31 failed=1 uncited=0 cores=4/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=6/7 exit=1
```

Receipt: `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/receipt-gate-control-fabricated.txt`.
The entry therefore survives both discriminating controls that the counter can pose.

## Finding 5 — Self-check: every quote re-located against the capture, with the `sed -n 'Np'` line

Full per-quote listing (32 quotes, each with its citation, the located=True verdict and the
verbatim source line) is copied to
`.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/receipt-quote-selfcheck.txt`
and appended verbatim at the end of this Report. Summary of the nine mandated quotes, each
against the exact line I verified:

```
$ sed -n '10p' corpus/source-snapshots/round-46-a2/S074.txt
Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project. After collaborating on a fix, repository maintainers can publish the security advisory to publicly disclose the security vulnerability to the project's community. By publishing security advisories, repository maintainers make it easier for their community to update package dependencies and research the impact of the security vulnerabilities.
$ sed -n '13p' corpus/source-snapshots/round-46-a2/S074.txt
Privately collaborate to fix the vulnerability in a temporary private fork.
$ sed -n '17p' corpus/source-snapshots/round-46-a2/S074.txt
You can give credit to individuals who contributed to a security advisory. For more information, see Creating a repository security advisory.
$ sed -n '24p' corpus/source-snapshots/round-46-a2/S074.txt
GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers. For more information, see About CVE and CVE Numbering Authorities on the CVE website.
$ sed -n '25p' corpus/source-snapshots/round-46-a2/S074.txt   (772 bytes; the two quoted spans are printed in full in the receipt)
… GitHub usually reviews the request within 72 hours. Requesting a CVE identification number doesn't make your security advisory public. …
$ sed -n '26p' corpus/source-snapshots/round-46-a2/S074.txt
If you already have a CVE you want to use, for example, if you use a CVE Numbering Authority (CNA) other than GitHub, add the CVE to the security advisory form. This may happen, for example, if you want to get the advisory consistent with other communications you plan to send out at publication time. GitHub cannot assign CVEs to your project if it is covered by another CNA.
$ sed -n '31p' corpus/source-snapshots/round-46-a2/S074.txt
Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.
$ sed -n '38p' corpus/source-snapshots/round-46-a2/S074.txt
Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory. If you don't, the advisory will be published without a fixed version, and Dependabot will alert your users about the issue, without offering any safe version to update to.
```

Word counts of all 32 spans are <= 25 (the gate reports `failed=0`); the longest is the
24-word fix-version-triage quote at S074.txt:42. One over-long span was caught and fixed
before the final run: the first draft carried a 28-word span at S074.txt:25 (“If you want a
CVE identification number for the security vulnerability in your project, and don't already
have one, you can request a CVE identification number from GitHub.”), which made H5 read
`spans=32 located=31 failed=1` and the gate 6/7; it was shortened to “you can request a CVE
identification number from GitHub.” (S074.txt:25).

## Finding 6 — Capture re-verified by the lane's own recheck instrument

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074
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
recheck exit=0
```

Receipt: `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/receipt-source-recheck.txt`.
The entry's `recheck:` line is exactly the command above with the `# 90d` cadence marker, so
the L1 can run it verbatim on the integrated tree.

## Finding 7 — Overlap evidence: the corpus state the Overlap section cites

Corpus sweep run on the live lane (freeze-tip knowledge dir, 65 entries, before this entry
is added):

```
$ ls corpus/knowledge | wc -l
65
$ grep -rn -i "maintainer-side" corpus/knowledge/
corpus/knowledge/linux-kernel-security-bugs-reporting-process.md:43:1. The kernel's required-fields intake contract. A maintainer-side list of four necessary fi
corpus/knowledge/github-private-vulnerability-reporting.md:9:This entry records one reporter-side flow: GitHub's documented route for a person who wants to repo
corpus/knowledge/github-private-vulnerability-reporting.md:40:- The page does not state the maintainer-side flow, CVE requests, timelines or rewards. Sweep over
$ grep -rn -i "temporary private fork" corpus/knowledge/
corpus/knowledge/github-private-vulnerability-reporting.md:23:| Who can merge a fix from the temporary private fork? | “Note that only the repository maintainer can merge changes from that private fork into the parent repository.” (`S073.txt:578`) | The page says the reporter may optionally start a temporary private fork and that only the maintainer can merge from it. A package may say a fix is merged only when a maintainer's merge is observed. |
```

Cross-reference line numbers verified by `sed -n` before citing them:

```
$ sed -n '9p'  corpus/knowledge/github-private-vulnerability-reporting.md
This entry records one reporter-side flow: GitHub's documented route for a person who wants to report a security vulnerability privately to a repository's maintainers. … The entry does not record the maintainer-side flow, and it is not a rule for other platforms, for coordinated disclosure in general, or for any particular repository.
$ sed -n '47,49p' corpus/knowledge/github-private-vulnerability-reporting.md
## Falsifiable package rule
(blank)
When a claim package states or describes a vulnerability report made through GitHub private vulnerability reporting, check it against S073 in this order. …
$ sed -n '9,12p' corpus/knowledge/cna-assignment-and-vulnerability-rules.md
A local CVE-request package review separates technical vulnerability determination,
CNA assignment scope, and identifier counting. A demonstrated security impact is
not itself proof that the reviewer has assignment authority; an identifier or a
vendor fix is not itself proof of a distinct independently fixable vulnerability.
$ sed -n '32p' corpus/knowledge/cna-assignment-and-vulnerability-rules.md
| 3.1.1 | “CNAs MUST develop, document, and operate within a Scope Definition” | Record the applicable assignment scope rather than infer authority from technical expertise. |
$ sed -n '36p' corpus/knowledge/cna-assignment-and-vulnerability-rules.md
| 4.2.1.1 | “The CNA with the most appropriate scope MUST be contacted and given the first opportunity to assign.” | An assignment-routing proposal names the appropriate CNA scope and unresolved exceptions. |
```

Both contrasts are stated as contrasts of coverage, not of policy: F28 holds the reporter's
view (actor: reporter; stage: submission) and explicitly excludes the maintainer-side flow;
F07 holds the CVE Program's assignment scope, while this entry holds the platform's
per-advisory request mechanics and the platform-side other-CNA boundary.

## Finding 8 — What the L1 still owes, measured on the live lane

The 7/7 in Finding 2 was measured on the R50 control's synthetic tree, which supplies its own
F29 README row and its own S074 SOURCES row. The live lane has neither, so those two rows
are still L1 writes:

```
$ grep -c '^| F' corpus/README.md
28
$ grep -rn 'S074' corpus/SOURCES.md ; echo "exit=$?"
exit=1
$ git log --oneline -1
ee03806 round-46 (attempt 2): wave a2w1 spec (64 seats, v2) + dispatch payload + builders + ready file
```

H1 (29 frontier rows, F29 admitted, entry cell naming the entry path) and H3 (the S074
SOURCES row with 11 cells) therefore remain unproven against the live tree by this seat; the
fixture rows used in Finding 2 are the control's, not the lane's. The entry itself is
byte-ready for `corpus/knowledge/github-repository-security-advisories.md`.

## Discipline and tooling

- No tool was installed, upgraded or downgraded; no pacman transaction was attempted (the
  host-wide pacman pause was respected); nothing was written under `~/.local/bin` or any
  other PATH directory.
- No git/jj mutation: the only git commands run were read-only (`git log --oneline -3`,
  `git status --porcelain`). No commit, push, branch, stash or index write.
- Written paths, all inside the lane and all inside my seat's scope: the draft entry, four
  receipt files beside it in `…/R46bScribeEntryC.draft/`, and this Report.
- Scratch `/fast/scratch/hyaku/kasegi-r46/R46bScribeEntryC/` (fixture trees, gate work dir,
  self-check text) was removed after the receipts were copied into the draft directory; no
  `/tmp` path is cited as evidence.

## Limitations

- The counter was exercised against a synthetic tree, not against the lane tree with the real
  README/SOURCES rows; H1/H3 there are the control's rows. Re-run `r46-f29-gate.py --root
  <integrated tree>` after the L1 writes the F29 row and the S074 row.
- The capture is the only evidence: no live fetch of the GitHub Docs page was performed
  (live-target testing is refused for this corpus), so the entry can only ever be as current
  as the pinned sha256 `1296528d…c278039` captured 2026-10-29.
- The two grep sweeps quoted in Finding 7 describe the corpus at the freeze tip (65 knowledge
  entries, this entry not yet added); after integration the counts change, so the entry
  phrases them as the freeze-tip observation.
- The Limits section deliberately does not hold the sibling pages the capture names (advisory
  form fields, editing flow, REST API endpoints, Advisory Database edit flow); their bodies
  are not in S074.txt and must not be inferred from it.
- The entry covers public repositories on GitHub.com only, as the page states; it says
  nothing about private repositories, other platforms, other CNA platforms, or the kernel's
  own maintainer-side intake contract (F27), and it does not absorb F28's reporter flow.
- The F29 frontier row text and the S074 SOURCES row text are the L1's to write; this seat
  proposed neither, so the final wording of those rows may differ from the entry's phrasing.

---

## Appendix — complete per-quote self-check (32 quotes, verbatim source lines)

QUOTE 1 (14 words): Repository security advisories and private vulnerability reporting are available for public repositories on GitHub.com
CITE S074.txt:6-6  located=True
  $ sed -n '6p' corpus/source-snapshots/round-46-a2/S074.txt
  Repository security advisories and private vulnerability reporting are available for public repositories on GitHub.com

QUOTE 2 (20 words): You can use repository security advisories to privately discuss, fix, and publish information about security vulnerabilities in your public repository.
CITE S074.txt:3-3  located=True
  $ sed -n '3p' corpus/source-snapshots/round-46-a2/S074.txt
  You can use repository security advisories to privately discuss, fix, and publish information about security vulnerabilities in your public repository.

QUOTE 3 (19 words): Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.
CITE S074.txt:10-10  located=True
  $ sed -n '10p' corpus/source-snapshots/round-46-a2/S074.txt
  Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project. After collaborating on a fix, repository maintainers can publish the security advisory to publicly disclose the security vulnerability to the project's community. By publishing security advisories, repository maintainers make it easier for their community to update package dependencies and research the impact of the security vulnerabilities.

QUOTE 4 (16 words): Publish the security advisory to alert your community of the vulnerability once a patch is released.
CITE S074.txt:14-14  located=True
  $ sed -n '14p' corpus/source-snapshots/round-46-a2/S074.txt
  Publish the security advisory to alert your community of the vulnerability once a patch is released.

QUOTE 5 (19 words): Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.
CITE S074.txt:10-10  located=True
  $ sed -n '10p' corpus/source-snapshots/round-46-a2/S074.txt
  Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project. After collaborating on a fix, repository maintainers can publish the security advisory to publicly disclose the security vulnerability to the project's community. By publishing security advisories, repository maintainers make it easier for their community to update package dependencies and research the impact of the security vulnerabilities.

QUOTE 6 (20 words): Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project.
CITE S074.txt:12-12  located=True
  $ sed -n '12p' corpus/source-snapshots/round-46-a2/S074.txt
  Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project.

QUOTE 7 (11 words): Privately collaborate to fix the vulnerability in a temporary private fork.
CITE S074.txt:13-13  located=True
  $ sed -n '13p' corpus/source-snapshots/round-46-a2/S074.txt
  Privately collaborate to fix the vulnerability in a temporary private fork.

QUOTE 8 (16 words): Publish the security advisory to alert your community of the vulnerability once a patch is released.
CITE S074.txt:14-14  located=True
  $ sed -n '14p' corpus/source-snapshots/round-46-a2/S074.txt
  Publish the security advisory to alert your community of the vulnerability once a patch is released.

QUOTE 9 (12 words): You can give credit to individuals who contributed to a security advisory.
CITE S074.txt:17-17  located=True
  $ sed -n '17p' corpus/source-snapshots/round-46-a2/S074.txt
  You can give credit to individuals who contributed to a security advisory. For more information, see Creating a repository security advisory.

QUOTE 10 (15 words): GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.
CITE S074.txt:24-24  located=True
  $ sed -n '24p' corpus/source-snapshots/round-46-a2/S074.txt
  GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers. For more information, see About CVE and CVE Numbering Authorities on the CVE website.

QUOTE 11 (8 words): GitHub usually reviews the request within 72 hours.
CITE S074.txt:25-25  located=True
  $ sed -n '25p' corpus/source-snapshots/round-46-a2/S074.txt
  When you create a security advisory for a public repository on GitHub, you have the option of providing an existing CVE identification number for the security vulnerability. If you want a CVE identification number for the security vulnerability in your project, and don't already have one, you can request a CVE identification number from GitHub. GitHub usually reviews the request within 72 hours. Requesting a CVE identification number doesn't make your security advisory public. If your security advisory is eligible for a CVE, GitHub will reserve a CVE identification number for your advisory. We'll then publish the CVE details after you make your security advisory public. Anyone with admin permissions to a security advisory can request a CVE identification number.

QUOTE 12 (11 words): Requesting a CVE identification number doesn't make your security advisory public.
CITE S074.txt:25-25  located=True
  $ sed -n '25p' corpus/source-snapshots/round-46-a2/S074.txt
  When you create a security advisory for a public repository on GitHub, you have the option of providing an existing CVE identification number for the security vulnerability. If you want a CVE identification number for the security vulnerability in your project, and don't already have one, you can request a CVE identification number from GitHub. GitHub usually reviews the request within 72 hours. Requesting a CVE identification number doesn't make your security advisory public. If your security advisory is eligible for a CVE, GitHub will reserve a CVE identification number for your advisory. We'll then publish the CVE details after you make your security advisory public. Anyone with admin permissions to a security advisory can request a CVE identification number.

QUOTE 13 (14 words): GitHub cannot assign CVEs to your project if it is covered by another CNA.
CITE S074.txt:26-26  located=True
  $ sed -n '26p' corpus/source-snapshots/round-46-a2/S074.txt
  If you already have a CVE you want to use, for example, if you use a CVE Numbering Authority (CNA) other than GitHub, add the CVE to the security advisory form. This may happen, for example, if you want to get the advisory consistent with other communications you plan to send out at publication time. GitHub cannot assign CVEs to your project if it is covered by another CNA.

QUOTE 14 (22 words): Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.
CITE S074.txt:31-31  located=True
  $ sed -n '31p' corpus/source-snapshots/round-46-a2/S074.txt
  Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.

QUOTE 15 (15 words): you should add a fix version to a security advisory prior to publishing the advisory
CITE S074.txt:38-38  located=True
  $ sed -n '38p' corpus/source-snapshots/round-46-a2/S074.txt
  Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory. If you don't, the advisory will be published without a fixed version, and Dependabot will alert your users about the issue, without offering any safe version to update to.

QUOTE 16 (9 words): you can request a CVE identification number from GitHub.
CITE S074.txt:25-25  located=True
  $ sed -n '25p' corpus/source-snapshots/round-46-a2/S074.txt
  When you create a security advisory for a public repository on GitHub, you have the option of providing an existing CVE identification number for the security vulnerability. If you want a CVE identification number for the security vulnerability in your project, and don't already have one, you can request a CVE identification number from GitHub. GitHub usually reviews the request within 72 hours. Requesting a CVE identification number doesn't make your security advisory public. If your security advisory is eligible for a CVE, GitHub will reserve a CVE identification number for your advisory. We'll then publish the CVE details after you make your security advisory public. Anyone with admin permissions to a security advisory can request a CVE identification number.

QUOTE 17 (19 words): If your security advisory is eligible for a CVE, GitHub will reserve a CVE identification number for your advisory.
CITE S074.txt:25-25  located=True
  $ sed -n '25p' corpus/source-snapshots/round-46-a2/S074.txt
  When you create a security advisory for a public repository on GitHub, you have the option of providing an existing CVE identification number for the security vulnerability. If you want a CVE identification number for the security vulnerability in your project, and don't already have one, you can request a CVE identification number from GitHub. GitHub usually reviews the request within 72 hours. Requesting a CVE identification number doesn't make your security advisory public. If your security advisory is eligible for a CVE, GitHub will reserve a CVE identification number for your advisory. We'll then publish the CVE details after you make your security advisory public. Anyone with admin permissions to a security advisory can request a CVE identification number.

QUOTE 18 (8 words): GitHub publishes the CVE to the MITRE database.
CITE S074.txt:27-27  located=True
  $ sed -n '27p' corpus/source-snapshots/round-46-a2/S074.txt
  Once you've published the security advisory and GitHub has assigned a CVE identification number to the vulnerability, GitHub publishes the CVE to the MITRE database.

QUOTE 19 (22 words): Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.
CITE S074.txt:31-31  located=True
  $ sed -n '31p' corpus/source-snapshots/round-46-a2/S074.txt
  Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.

QUOTE 20 (9 words): Collaborators can view the conversation history of the advisory.
CITE S074.txt:32-32  located=True
  $ sed -n '32p' corpus/source-snapshots/round-46-a2/S074.txt
  Collaborators can view the conversation history of the advisory.

QUOTE 21 (11 words): The URL of a security advisory does not change after publication.
CITE S074.txt:33-33  located=True
  $ sed -n '33p' corpus/source-snapshots/round-46-a2/S074.txt
  The URL of a security advisory does not change after publication.

QUOTE 22 (14 words): GitHub cannot assign CVEs to your project if it is covered by another CNA.
CITE S074.txt:26-26  located=True
  $ sed -n '26p' corpus/source-snapshots/round-46-a2/S074.txt
  If you already have a CVE you want to use, for example, if you use a CVE Numbering Authority (CNA) other than GitHub, add the CVE to the security advisory form. This may happen, for example, if you want to get the advisory consistent with other communications you plan to send out at publication time. GitHub cannot assign CVEs to your project if it is covered by another CNA.

QUOTE 23 (16 words): The security advisory form on GitHub is a standardized form that matches the CVE description format.
CITE S074.txt:23-23  located=True
  $ sed -n '23p' corpus/source-snapshots/round-46-a2/S074.txt
  GitHub Security Advisories builds upon the foundation of the Common Vulnerabilities and Exposures (CVE) list. The security advisory form on GitHub is a standardized form that matches the CVE description format.

QUOTE 24 (5 words): Creating a repository security advisory
CITE S074.txt:17-17  located=True
  $ sed -n '17p' corpus/source-snapshots/round-46-a2/S074.txt
  You can give credit to individuals who contributed to a security advisory. For more information, see Creating a repository security advisory.

QUOTE 25 (21 words): If you need to update or correct information in a security advisory that you've published, you can edit the security advisory.
CITE S074.txt:34-34  located=True
  $ sed -n '34p' corpus/source-snapshots/round-46-a2/S074.txt
  If you need to update or correct information in a security advisory that you've published, you can edit the security advisory. See Editing a repository security advisory.

QUOTE 26 (15 words): You can also use the REST API to create, list, and update repository security advisories.
CITE S074.txt:16-16  located=True
  $ sed -n '16p' corpus/source-snapshots/round-46-a2/S074.txt
  You can also use the REST API to create, list, and update repository security advisories. For more information, see REST API endpoints for repository security advisories.

QUOTE 27 (14 words): Anyone can submit a change to an advisory published in the GitHub Advisory Database.
CITE S074.txt:19-19  located=True
  $ sed -n '19p' corpus/source-snapshots/round-46-a2/S074.txt
  If you created a security advisory in your repository, the security advisory will stay in your repository. We publish security advisories for any of the ecosystems supported by the dependency graph to the GitHub Advisory Database on github.com/advisories. Anyone can submit a change to an advisory published in the GitHub Advisory Database. For more information, see Editing security advisories in the GitHub Advisory Database.

QUOTE 28 (17 words): Imminently available, and you are able to, wait to disclose the issue when the fix is ready.
CITE S074.txt:40-40  located=True
  $ sed -n '40p' corpus/source-snapshots/round-46-a2/S074.txt
  Imminently available, and you are able to, wait to disclose the issue when the fix is ready.

QUOTE 29 (18 words): In development but not yet available, mention this in the advisory, and edit the advisory later, after publication.
CITE S074.txt:41-41  located=True
  $ sed -n '41p' corpus/source-snapshots/round-46-a2/S074.txt
  In development but not yet available, mention this in the advisory, and edit the advisory later, after publication.

QUOTE 30 (24 words): Not planned, be clear about it in the advisory so that your users don't contact you to ask when a fix will be made.
CITE S074.txt:42-42  located=True
  $ sed -n '42p' corpus/source-snapshots/round-46-a2/S074.txt
  Not planned, be clear about it in the advisory so that your users don't contact you to ask when a fix will be made. In this case, it is helpful to include steps users can take to mitigate the issue.

QUOTE 31 (14 words): GitHub will review each published security advisory, add it to the GitHub Advisory Database
CITE S074.txt:36-36  located=True
  $ sed -n '36p' corpus/source-snapshots/round-46-a2/S074.txt
  GitHub will review each published security advisory, add it to the GitHub Advisory Database, and may use the security advisory to send Dependabot alerts to affected repositories. If the security advisory comes from a fork, we'll only send an alert if the fork owns a package, published under a unique name, on a public package registry. This process can take up to 72 hours and GitHub may contact you for more information.

QUOTE 32 (16 words): This process can take up to 72 hours and GitHub may contact you for more information.
CITE S074.txt:36-36  located=True
  $ sed -n '36p' corpus/source-snapshots/round-46-a2/S074.txt
  GitHub will review each published security advisory, add it to the GitHub Advisory Database, and may use the security advisory to send Dependabot alerts to affected repositories. If the security advisory comes from a fork, we'll only send an alert if the fork owns a package, published under a unique name, on a public package registry. This process can take up to 72 hours and GitHub may contact you for more information.


Report: .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.md
