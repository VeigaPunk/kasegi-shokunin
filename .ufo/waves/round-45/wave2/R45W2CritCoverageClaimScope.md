VERDICT: BROKEN

Scope: in-province membership of F27 HOLDS. Six boundary statements in the landed entry are defective (L27, L29, L42, L43, L48) and the Limits/Overlap sections are missing four exclusions and F07/F10/F25. Each defect is below with the source line and the entry line.

Attacked artifact: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 6662a4276b6f7bd61e23e12058414e09dd71b9e4 | tar -x -C /fast/scratch/hyaku/kasegi-r45/R45W2CritCoverageClaimScope/tree` (integration tree). Control: `git archive dc5bb8c6e31efc4a6650819df85e79b72fd64bcd` into `.../base`. Entry = `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` (60 lines). Capture = `corpus/source-snapshots/round-45/S071.txt` (372 lines, sha256 0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40, matches the manifest).

## A. In-province membership: HOLDS (discriminated against the do-nothing control)

Attacked: entry L9 scope sentence; PROVINCE.md:29-30 (Core: "program rules, scopes, and claim packages ... submission/disclosure packaging"); PROVINCE.md:169 (F27 line); corpus/README.md:211 (F10 row).

Commands and output:
- `grep -rliE 'security-bugs|linux kernel|kernel\.org' base/corpus/knowledge base/corpus/SOURCES.md base/corpus/README.md; echo exit=$?` printed `exit=1` (no match at dc5bb8c).
- Same grep on the tree printed the entry, `corpus/SOURCES.md` and `corpus/README.md`.
- `r44-frontier-count.py --root base` printed `frontier rows=26 admitted=26`; `--root tree --expect 27` printed `frontier rows=27 admitted=27`.
- `diff -rq base/corpus tree/corpus` changed only QUALITY.md, README.md, SOURCES.md, instruments/README.md, knowledge-expected.txt, r44-frontier-count.py, lessons/round-44.md; added freeze-check.py, r45-c2-gate.py, r45-routed-defects.py, the entry, and source-snapshots/round-45.

So the F27 change is the only kernel-security scope change. Reading: an upstream project's intake and embargo rule is a disclosure-packaging object in the F10 family ("vendor-side disclosure policies"). Limitation: PROVINCE's header says "bounty & security research"; the kernel team runs no bounty. Membership rests on the Core clause, and the operator owns that classification.

## B. Entry L27 (linux-distros row): BROKEN, truncated condition, outside the registry row's scope

Entry L27 quotes “a fix is accepted by the affected code's maintainers” (`S071.txt:350`) and concludes: "Record linux-distros contact as not yet permitted until the maintainers accept the fix."

Source, `sed -n 348,353p corpus/source-snapshots/round-45/S071.txt`:
"the kernel security team strongly recommends that as a reporter of a potential security issue you DO NOT contact the "linux-distros" mailing list UNTIL a fix is accepted by the affected code's maintainers and you have read the distros wiki page above and you fully understand the requirements that contacting "linux-distros" will impose on you and the kernel community."

Defects:
1. Drops two conjuncts ("you have read the distros wiki page above", "you fully understand the requirements"). The package rule implies permission once maintainers accept, which the source does not give.
2. Turns "strongly recommends" into "not yet permitted".
3. `corpus/SOURCES.md:77` (S071 row) states "its CVE and linux-distros statements are outside this row". The entry uses the excluded statement anyway.

Action: remove L27 from the table. If the fact is kept, restate the full conjunction and "strongly recommends", and point to the F10/F15 ground.

## C. Entry L29 (CVE row): BROKEN, CVE-policy drift, registry scope conflict

Entry L29: "Is a CVE a required intake field? ... Do not list a CVE as a required field. Its absence is not a defect under this page."

Source `S071.txt:362-366`: "The security team does not assign CVEs, nor do we require them for reports or fixes ... they can contact the kernel CVE assignment team".

Defects:
1. `corpus/SOURCES.md:77` excludes CVE statements from the S071 row. The entry records one anyway.
2. Entry L9 says the entry is not for "CVE handling beyond what the page itself states", yet L29 turns a CVE statement into a package rule.
3. The Overlap section (L35-37) names F02, F04, F15 but not F07 (`corpus/README.md:208`, `knowledge/cna-assignment-and-vulnerability-rules.md`, CVE CNA rules) or F25 (`corpus/README.md:591`, `knowledge/cve-json-record-format.md`).

Action: remove L29, add one Limits bullet ("CVE assignment is F07/F25 ground; S071's CVE section (S071.txt:359-366) is not recorded as CVE policy"), and add F07 and F25 to Overlap.

## D. Entry L42 (AI-duties item): BROKEN, overstated requirement and patch-submission drift

Entry L42: "The page requires a plain-text report with the four items, not Markdown decoration, a recipients section and a fix tested before reporting (`S071.txt:195-196`, `S071.txt:213-217`; the MUST list at `S071.txt:239-245`)."

Source:
- `S071.txt:49`: "In addition, the following information are highly desirable:" and `S071.txt:57-58` lists "a proposed fix". So a proposed fix is desirable, not required.
- `S071.txt:213-219`: "Please ask your tool to propose a fix and test it before reporting ... if a fix is proposed, it must adhere to Documentation/process/submitting-patches.rst and include a 'Fixes:' tag".
- `S071.txt:232-237`: "write a fix, build it warning-free and checkpatch-clean, commit it with a Fixes tag, and identify the maintainers with get_maintainer.pl".
- The MUST list at `S071.txt:239-248` has two items (report content, recipients). Neither is fix testing.

Defects:
1. "The page requires ... a fix tested" overstates the general rule (S071.txt:49 says "highly desirable") and attributes a non-MUST item to the MUST list.
2. The patch-format, Fixes-tag, checkpatch and get_maintainer duties (S071.txt:217-219, 232-237) are kernel engineering and are out of province. The entry cites the same bullet and does not exclude them.

Action: rewrite L42 so a proposed fix is optional, and add a Limits bullet excluding patch-format rules (S071.txt:217-219, 232-237).

## E. Entry L43 ("not a researcher deadline"): BROKEN, contradicts the source and the entry's own L58

Entry L43: "It is the maintainer's own ceiling, not a researcher deadline."

Source `S071.txt:308-311`: "this may be postponed at the request of the reporter or an affected party for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days".

Entry L58 says "a ceiling on requested postponement". L43 says it is "not a researcher deadline". The cap binds the reporter who requests the deferral.

Action: rewrite L43 to "It caps a postponement the reporter or an affected party requests, so it binds the requesting reporter."

## F. Entry L48 (provenance sentence): REMOVE, lane-process text inside a knowledge entry (not a domain edge, but it leaks the assignment)

Entry L48: "The assignment labels the page as versioned 7.3.0 at capture, but the capture carries no version string (no `7.3` match in `S071.txt`)."

Command: `grep -n "7\.3" corpus/source-snapshots/round-45/S071.txt` printed nothing. So the "no version string" half is verified. The first half cites the lane's assignment, which is not evidence.

Action: keep "The capture carries no version string (no `7.3` match in `S071.txt`)" and delete the assignment clause.

## G. Missing Limits and Overlap content (NEEDS sentences)

The Limits section (L47-50) has four bullets. It says "not law". It does not exclude:
- kernel patch-format and build rules (S071.txt:217-219, 232-237);
- CVE assignment (S071.txt:359-366);
- linux-distros coordination detail (S071.txt:329-357);
- NDA and legal effect. S071.txt:368-372 says the team "is not a formal body and therefore unable to enter any non-disclosure agreements". The entry is silent, so add "No NDA or legal effect is recorded."

The Overlap section (L35-37) omits F10 (`corpus/README.md:211`: "A vendor's published policy is a standing first-party statement, not a programme"). F27 is an upstream project's policy, not a vendor's. The entry should say why it is a new row rather than an F10 member. Add a sentence.

## H. Boundary statements checked and KEPT (quotes match the capture)

- L22 "If you resorted to AI assistance to identify a bug, you must treat it as public" matches `S071.txt:95-96` exactly (read).
- L23 "do not publicly share a reproducer, as this could cause unintended harm" matches `S071.txt:99`; "the reproducer should only be shared upon maintainers' request" matches `S071.txt:210-211`.
- L28 "you must also always Cc: the Linux kernel security team" matches `S071.txt:272-273`.
- L37 "other groups focus on fixing issues in distros and coordinating disclosure between operating system vendors" matches `S071.txt:333-334`.
- L59 "or use of AI-based tools" matches `S071.txt:117`.
- L60 "solely focuses on getting bugs fixed" matches `S071.txt:332`.
- L50 "Documentation only ... no probing" is consistent with the live-target refusal in PROVINCE.md:52.

Limitation: I did not exact-match every quoted span. Quote closure is C2's job.

## I. In-province coverage gap (non-blocking)

- S071.txt:257 "Reports are to be sent over e-mail exclusively." and S071.txt:280-281 (<security@kernel.org>, "a private list of security officers") are not in the entry. `grep -n -iE "e-mail|email|security@" corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` printed nothing. README.md:647 and PROVINCE.md:169 describe a "private security list" / "private report channel" that the entry never names.
- The entry's anchor line (L3) cites "What qualifies as a security bug (S071.txt:73-107)", but the body records only the reproduction test. The trust-boundary test (S071.txt:89-93, "consider whether the issue actually crosses a trust boundary") is absent.

## Limitations

- The entry's own recheck, `source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071`, printed `S071:sha256 OK` and `Q1..Q5 OK`. It covers 5 manifest quotes. The entry quotes about 25 spans and I did not exact-match the rest.
- Read coverage: S071.txt lines 10-72, 72-133, 134-169, 170-257, 255-372 (whole capture).
- Classification is my reading of PROVINCE.md. Re-scope is the operator's decision.
- No counter (C1 or C2) was run; scope only.
- Scratch removed on exit. Nothing was committed, pushed, or written to git, the index, or shared files.
