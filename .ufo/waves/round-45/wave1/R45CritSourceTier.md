VERDICT: HOLDS

Scope: Source-tier critic (leaf, read-only). Question: is docs.kernel.org/process/security-bugs.html tier A for "the kernel security team's own report-intake and embargo rules" under the CORPUS.md SOURCES contract ("A: primary or authoritative for that scope (spec, official docs, source code, original paper, maintainer statement ...)")? Also: is S072's proposed tier (drafts: B in R45ScribeRowsA and R45ScribeRowsB) supported?

Answer in one line: S071 tier A HOLDS for the stated scope, with two drafting defects to fix (anchor lacks a commit; scope cell excludes the embargo-clock text). S072's proposed tier B does NOT hold; recommended tier A scoped to routing only (status stays rejected).

Contract text attacked (CORPUS.md, fleet root):
  `tier` — "A: primary or authoritative for that scope (spec, official docs, source code, original paper, maintainer statement, ...). B: strong secondary (expert write-up ..., survey, textbook). C: lead only ... `community` is never A."
  Command: sed -n '93,97p' /home/vgpnk/Projects/shokunin/CORPUS.md
  Also: "`anchor` — exact section / heading / page / line plus revision (version, commit, or publication date)."

---------------------------------------------------------------------
Finding 1 — S071 provenance: the RST is owned by the kernel's Security Officers (in-tree owner)

Attacked: corpus/source-snapshots/round-45/S071.txt (the RST source served at docs.kernel.org/_sources/process/security-bugs.rst.txt) and the live tree blob Documentation/process/security-bugs.rst.

Commands and output:
  $ curl -sS -o src.rst.txt https://docs.kernel.org/_sources/process/security-bugs.rst.txt ; sha256sum src.rst.txt
  0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40  src.rst.txt
  $ sha256sum corpus/source-snapshots/round-45/S071.txt
  0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40  corpus/source-snapshots/round-45/S071.txt
  $ curl -sS -o tree-security-bugs.rst https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/process/security-bugs.rst ; sha256sum tree-security-bugs.rst
  0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40  tree-security-bugs.rst
  => the live docs source, the in-tree blob (kernel master, fetched 2026-10-28) and the pinned snapshot are byte-identical.

  $ curl -sS -o MAINTAINERS.txt https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/MAINTAINERS ; sed -n '25338,25341p' MAINTAINERS.txt
  SECURITY CONTACT
  M:	Security Officers <security@kernel.org>
  S:	Supported
  F:	Documentation/process/security-bugs.rst
  => the file has a dedicated maintainer entry owned by the security officers (not a generic docs entry).

  Control (same grep, a different kernel doc with a different owner):
  $ sed -n '7984,7990p' MAINTAINERS.txt
  DOCUMENTATION REPORTING ISSUES
  M:	Thorsten Leemhuis <linux@leemhuis.info>
  ...
  F:	Documentation/admin-guide/reporting-issues.rst
  => same docs.kernel.org domain, different owner: domain alone is not the tier test; the owner must match the scope.

Commit provenance:
  $ curl -sS -o c6ffecfe.html "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=6ffecfe0805e8811e7637e8f381b6740a3e9767b"; (text extracted)
  "docs: security-bugs: clarify some mandatory steps for AI reports" ... author Willy Tarreau <w@1wt.eu> 2026-08-02 22:35:40 +0200 ... committer Greg Kroah-Hartman <gregkh@linuxfoundation.org> 2026-08-04 16:24:50 +0200 commit 6ffecfe0805e8811e7637e8f381b6740a3e9767b
  Log for the path (cgit, same run) lists 2026-08-04, 2026-08-04, 2026-05-14 (Jonathan Corbet, "add a link to the threat-model documentation"), 2026-05-12 ... as the file's history.
  => 6ffecfe0805e8811e7637e8f381b6740a3e9767b is the most recent commit touching the file and is the revision the S071 bytes match (the in-tree blob sha equals S071).

Located quotes in the capture (raw lines, exact):
  S071.txt:6-7  "Linux kernel developers take security very seriously. As such, we'd like to know when a security bug is found" (19 words) — maintainer voice.
  S071.txt:281-282  "This is a private list of security officers who will help verify the bug report" (16 words) — the team describes its own list.
  S071.txt:371-372  "The Linux kernel security team is not a formal body and therefore unable to enter any non-disclosure agreements." (19 words) — self-description.
  S071.txt:332-334  "While the kernel security team solely focuses on getting bugs fixed," (11 words) — team's own coordination statement.

Rendered page (docs.kernel.org/process/security-bugs.html, fetched 2026-10-28; 33621 bytes):
  $ grep -n 'title="The Linux Kernel threat model"' page.html
  21:    <link rel="next" title="The Linux Kernel threat model" href="threat-model.html" />
  $ sed -n '534,535p;539p' page.html
  Powered by <a href="https://www.sphinx-doc.org/">Sphinx 5.3.0</a>
  & <a href="https://alabaster.readthedocs.io">Alabaster 0.7.16</a>
  rel="nofollow">Page source</a>
  Footer = Sphinx generator plus a "Page source" link to ../_sources/process/security-bugs.rst.txt. No author, date or git-history link appears on the rendered page itself.

The spec's phrase "The Linux Kernel threat model" is NOT a sentence of the security-bugs RST. It is (a) the nav-link title at page.html:21 and (b) the H1 of a different file, Documentation/process/threat-model.rst:
  $ curl -sS -o tree-threat-model.rst https://git.kernel.org/.../plain/Documentation/process/threat-model.rst ; head -1 tree-threat-model.rst
  The Linux Kernel threat model
  The RST's own sentence (S071.txt:84-85) reads: "a lack of awareness of the Linux kernel's threat model, as described in / Documentation/process/threat-model.rst". Lowercase "kernel's", not the title. Do not quote the spec's phrase as RST text.

Reported-by conventions (S071.txt:65-67, 257-259): "Note that in this case only a ``Signed-off-by:`` tag is needed, without ``Reported-by:``" and "preferably the same that you want to appear in ``Reported-by`` tags". These are reporter instructions inside the team's own process text; they support maintainer authorship but are not independent evidence.

Verdict on S071: maintainer statement, in-tree, owned by Security Officers, pinned to commit 6ffecfe0805e8811e7637e8f381b6740a3e9767b. Tier A is contract-consistent (kind `docs`; "maintainer statement" and "official docs" are the contract's own A examples). Not community.

Recommended S071 tier: A (confirmed) for scope "kernel security team's own report-intake, qualification and embargo rules".

---------------------------------------------------------------------
Finding 2 — S071 drafted row defects (tier stands, row text does not)

(a) Anchor has no revision. Drafts (R45ScribeRowsA/B) anchor on "last-modified 2026-08-09 21:57:49 GMT" — that is a server header date, not a source revision. The contract requires "revision (version, commit, or publication date)" in anchor. Fix: add commit 6ffecfe0805e8811e7637e8f381b6740a3e9767b (committed 2026-08-04) and keep the sha256 0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40.

(b) Scope excludes embargo rules by mistake. Draft scope: "its CVE and linux-distros statements are outside this row". The embargo clock is in "Disclosure and embargoed information" and in the "Coordination with other groups" section, which states the clock start and the linux-distros ordering:
  S071.txt:308-311 "...postponed at the request of the reporter or an affected party for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days" (this is the 21-word Q1 span, anchor 310)
  S071.txt:348-349 "As such, the kernel security team strongly recommends that as a reporter of a potential security issue you DO NOT contact the "linux-distros"" 
  Those are the team's own embargo rules. Recommend: scope = "report intake, qualification, and embargo rules including the fix-availability embargo clock (S071.txt:299-357); CVE assignment (S071.txt:359-366) is the team's own statement too but is not needed for F27." Tier remains A.

(c) The rows' "Rationale" says S071 "its teaches is grounded in capture lines 20-21 and 310-315". Lines 20-21 hold the version rule; line 310 is the 7/14-day quote. Both are in the capture; no fault.

(d) threat-model.rst is NOT captured. Any F27 entry sentence about "the Linux kernel threat model" must cite a separate row or be marked as a pointer; S071 does not carry the threat-model's content (its own title is only verified as the tree H1 above, not a captured quote).

---------------------------------------------------------------------
Finding 3 — S072 proposed tier B does not hold under the contract

Attacked: drafts R45ScribeRowsA.draft/rows.md and R45ScribeRowsB.draft/rows.md (both propose tier B); capture corpus/source-snapshots/round-45/S072.txt; manifest record S072.

Their stated reason: "Google's own directory, but a routing summary that restates the per-program rules pages it links to, so it is secondary to them". That conflates scope: tier is "scoped to scope, never global". Google is the program owner; for the scope the page actually carries (which Google VRP programme takes which product family, and where a report goes), the owner's own page is a maintainer-type authoritative statement -> the contract's A. B is defined as "strong secondary (expert write-up with reproducible detail, survey, textbook)". Google's directory is none of those.

Evidence the page is the owner's own statement and carries routing rows:
  S072.txt:2-3  "Welcome to the VRP rules section! Here, you’ll find an overview of the different / vulnerability reward programs Google maintains" 
  S072.txt:148-149  "Security issues affecting any Google Cloud product or web service that / handles reasonably sensitive user data" (Cloud VRP scope cell; "Use the standard form (report to Cloud VRP)" follows at S072.txt:151)
  Section headings: S072.txt:17 "## Android & Friends", :57 "## Chrome & Friends", :107 "## Google & Friends", :171 "## Open Source", :249 "## Other" (draft line refs confirmed).

Where B is wrong on the scope the draft itself names: the operative rules (what a Cloud VRP report must contain, eligibility) are NOT on this page; they sit on the linked rules pages (e.g. /about/rules/4849867320328192/...), which the lane has not captured. For that operative-rules scope the page is at most a lead, not evidence: a C-type statement for that scope, never sole support.

Capture fidelity (verified now):
  $ curl -sS -o s072-api-now.json https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section
  body characters: 10029 ; body == S072.txt minus one trailing newline (whitespace-normalised equal: True)
  $ curl -sS -o s070-canonical.html https://bughunters.google.com/about/rules/about-this-section ; visible text = "Rules | Google Bug Hunters" (26 chars) -> the canonical HTML is a JS shell without JS; the API is the only non-JS readable route. This confirms the S070 "shell" observation for the canonical URL, but the lesson's correction (body readable through the API) is also right.

Recommended S072 tier: A, with scope narrowed to "which Google VRP programme covers which product family and where a report is sent (routing), as stated by Google's own directory". Status stays `rejected` (admission reason is unchanged: no operative rule beyond S069 Q5). Do not write "secondary to the rules pages" in the rationale; write the operative-rules limit instead (it is what makes B/C unnecessary).

Note: S069 Q5 (round-44 manifest, S069.txt:10) reads "product or web service that handles reasonably sensitive user data is intended to be in scope." The S072 line is a near-restatement, not an identical quote; the "restates S069 Q5" claim in the lesson is approximate.

---------------------------------------------------------------------
Finding 4 — S072 quote anchor and row-URL convention

(a) Manifest anchor for S072 Q2 is 1; the quote "an overview of the different vulnerability reward programs Google maintains" sits at S072.txt:2-3 (line 1 is blank). Command: sed -n '1,3p' S072.txt printed a blank line, then the two lines above. The recheck still prints "S072:Q2 OK ... anchor=1-ok" because source-recheck.py accepts an anchor when the quote lies inside the window anchor..anchor+3 (lines 1-4 here); the anchor is a window check, not an exact line check. Fix: anchor 2.
  Command: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S072 -> "S072:Q2 OK normalized=markup-whitespace occurrences=1 anchor=1-ok" rc=0.

(b) Row URL. Draft S072 row uses the article-API URL (…/rest/v1/articles/…). SOURCES.md:154 (round-44 convention for S069) says the canonical URL remains the row URL and the API goes in the manifest as capture_url/http.final_url. Following S069 would make S072's URL equal S070's canonical URL (census duplicate-URL risk). That is a registry-shape question for the census drafter; tier is unaffected. Flag only.

---------------------------------------------------------------------
Finding 5 — Discrimination controls (do the tests bite?)

Control A — recheck on fabricated quote and mutated capture (scratch copy only; corpus untouched):
  mutate S071 manifest Q2 to "Kernel security reports are accepted by pull request only"; run source-recheck.py --source S071
  S071:Q2 MISMATCH reason=quote-not-found ; exit rc=1
  append "X" to a copy of S071.txt; run again
  S071:sha256 MISMATCH expected=0918dcfa... actual=821dde14... ; exit rc=1
  => the recheck discriminates fabricated quotes and altered bytes. Unmodified run: "S071:sha256 OK" and Q1-Q5 OK, rc=0.

Control B — owner test applied across sources:
  S071 (Documentation/process/security-bugs.rst): dedicated SECURITY CONTACT owner -> PASSES the scope test.
  Documentation/admin-guide/reporting-issues.rst (same domain): owner Thorsten Leemhuis under DOCUMENTATION REPORTING ISSUES -> FAILS the security-scope test (A for general bug reporting, not for the security team's intake rules). The S071 RST itself defers ordinary bugs to that file (S071.txt:85-87).
  S072 (Google directory): not a kernel source; FAILS the kernel-scope test by construction; its A is only for Google's routing scope (Finding 3).
  Do-nothing baseline ("any docs.kernel.org page is A") would pass reporting-issues.rst for the security scope; the owner test rejects it. This is the discriminator the S071 A depends on.

Control C — maintainer-voice count (weak, reported for completeness): security-team self-references ("security team", "security officers") S071: 20 lines; S072: 0 lines. First-person we/our/us: S071 5 hits, S072 7 hits (Google also uses "our"), so voice alone does NOT discriminate; the owner test is the load-bearing one.

---------------------------------------------------------------------
Recommendation per row
- S071 (docs.kernel.org security-bugs RST): tier A — HOLDS. Fix anchor (add commit 6ffecfe0805e8811e7637e8f381b6740a3e9767b) and scope cell (include embargo clock S071.txt:299-357; drop the "linux-distros outside" exclusion or say why).
- S072 (Google Bug Hunters directory, article-API capture): proposed B — NOT SUPPORTED. Recommend A scoped to routing only; status rejected; anchor Q2 fix 1 -> 2; row URL convention to be settled by the census drafter.
- No tier-A admission for threat-model content: not captured, not in S071.

Limitations
- Live fetches on 2026-10-28 only: docs.kernel.org (page and _sources RST), git.kernel.org cgit (commit page, log, plain blob, MAINTAINERS at master), bughunters.google.com article API and canonical HTML. No pinned MAINTAINERS blob sha; "master" at fetch time. The commit 6ffecfe is the most recent for the file as of that fetch.
- The GitHub API for the file history returned HTTP 429; history was taken from cgit instead.
- The rendered page carries no author or date; kernel authorship is inferred from the in-tree MAINTAINERS entry and commit metadata, not from a statement on the page. Whether named commit authors (Willy Tarreau, Greg Kroah-Hartman, Jonathan Corbet) are personally "Security Officers" was NOT verified; this report relies on the MAINTAINERS entry for ownership.
- Whether the team's practice matches the document is outside a source-tier check; that is a claim-vs-source question.
- S072: "routing scope" tier A rests on the owner's own page; I did not verify the linked operative rules pages (not captured) and did not test JS rendering of the canonical page beyond the plain fetch.
- Nothing committed; no git/jj mutations; no edits to corpus/, registry, MANIFEST or shared files. Scratch under $HYAKU_SCRATCH/kasegi-r45/R45CritSourceTier removed on exit. The one write is this Report file.

Tool records: none installed. Commands used: curl, sha256sum, sed, grep, python3 (stdlib), corpus/instruments/source-recheck.py (read-only run).
