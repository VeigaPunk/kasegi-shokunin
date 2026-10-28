VERDICT: BROKEN

Scope: F27 entry non-quote claims, first half. Attacked the knowledge file at `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` lines 7-13 (`## Scope and decision rule`) and the table package-consequence column (lines 15-29), in the export of lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (exported to a scratch dir; the moving lane tree was not used).

Source identity: `corpus/source-snapshots/round-45/S071.txt` sha256 `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40`, equal to the `sha256` for S071 in `corpus/source-snapshots/round-45/manifest.json` (fetched 2026-10-28T20:52:44Z, 372 lines).

Bottom line: every quoted sentence and its line cite holds (18/18 in-scope quote+cite pairs pass). The defects sit in the non-quoted consequence text: three rows state the page's rule with more force, or with fewer conditions, than the page states it. The AI-assisted row and the linux-distros row are the material ones.

## Findings (by severity)

### 1. [Medium-high] AI-assisted row (knowledge line 22) states an inference as the page's rule
Attacked text: "Record the publication status as public. A package may not describe an AI-assisted finding as private-only."
- The page says "**If you resorted to AI assistance to identify a bug, you must treat it as public**. While you may have valid reasons to believe it is not, ..." (S071.txt:95-98). It is a handling assumption, justified by simultaneous discovery across researchers (S071.txt:96-98). The row turns it into a factual status ("Record the publication status as public") and drops both the stated reason and the "may have valid reasons to believe it is not" caveat.
- The prohibition "may not describe ... as private-only" has no source. Command: `grep -c -i 'private-only' corpus/source-snapshots/round-45/S071.txt` printed `0`. The page never uses that wording.
- Nearest source text routes an AI-assisted report privately: "send it directly to the affected subsystem's maintainers and Cc: the Linux kernel security team" (S071.txt:112-113); "Reports are to be sent over e-mail exclusively" (S071.txt:257); "maintainers only for the report and reproducer" (S071.txt:246-248, MUST item 2); "This is a private list of security officers" (S071.txt:281). A package that says its AI-assisted report went privately to maintainers, as the page directs, would be barred by the row's wording.
- Unsurfaced source tension: the AI section says "since the report will be posted to a public list" (S071.txt:209-211). The row quotes S210-211 for "shared upon maintainers' request" but never mentions that this premise conflicts with the maintainers-only routing at S246-248. The row therefore resolves a conflict in the source silently.

### 2. [Medium] linux-distros row (knowledge line 27) turns a strong recommendation into a permission rule and drops two of three conditions
Attacked text: "Record linux-distros contact as not yet permitted until the maintainers accept the fix." (quote "a fix is accepted by the affected code's maintainers", S071.txt:350 — quote itself verified.)
- Source wording: "the kernel security team **strongly recommends** that as a reporter of a potential security issue you DO NOT contact the 'linux-distros' mailing list UNTIL a fix is accepted by the affected code's maintainers **and** you have read the distros wiki page above **and** you fully understand the requirements that contacting 'linux-distros' will impose on you and the kernel community." (S071.txt:348-352). Verified by `sed -n '340,357p'` on the export.
- The row states "not yet permitted" (a permission rule) where the page gives a recommendation, and it keeps only the first of three conjunctive conditions.
- Also omitted, S071.txt:353-357: "it doesn't make sense to Cc: both lists at once ... until a fix is accepted do not Cc: 'linux-distros', and after it's merged do not Cc: the kernel security team."

### 3. [Low-medium, coverage] Clock and postponement rows drop scope qualifiers the page states
- Knowledge line 24 (embargo clock): the row omits "Fixes for publicly known bugs are released immediately." (S071.txt:305-306).
- Knowledge line 25 (7/14-day ceiling): "Record the release-process start date and a 7-day ceiling." omits that the postponement applies to "publicly undisclosed bugs" (S071.txt:308-309) and is "at the request of the reporter or an affected party" (S071.txt:309-310). Both qualifiers are in the quoted text the entry itself cites at S309-310, so this is an omission, not a source gap.

### 4. [Low] "such as" becomes a closed list in the time-dependent label row (line 18)
- Attacked: "Accept only a commit ID or an exact version."
- Source: "A stable identifier **such as** a commit ID or an exact version is required" (S071.txt:22-23). "such as" marks examples; "only" closes the set.
- Also line 13 (decision rule): "complete for kernel intake" uses a word the page does not use. The page says the four items are "absolutely necessary" and that a report with no version "will not be processed" (S071.txt:17-18, 20-22).

### 5. [Low] Reproducer row (line 20): closed list where the page gives an open one
- Attacked: "The reproducer field must hold source code, a shell script, an instruction sequence or a file-system image."
- Source: "A reproducer with low complexity dependencies will be needed (source code, shell script, sequence of instructions, file-system image **etc**)." (S071.txt:37-39). The row drops "etc" and "low complexity dependencies", and turns an example list into a required set.

### 6. [Low] Distro row (line 19) paraphrases beyond the quote and cites only the quote
- Attacked: "Keep the distro string as context only; the kernel.org identifier is still required."
- Source: distro-kernel versions "are meaningless to maintainers and will not be processed" (S071.txt:23-25). The page does not say "context only" and does not name a "kernel.org identifier". The nearest requirement is "A stable identifier such as a commit ID or an exact version" (S071.txt:22-23). The row cites only S023-24.

### 7. [Low] Version-field row (line 17) names inputs the page never mentions
- Attacked: "do not fill the field from a date, a branch name or a distro string."
- Source has no mention of a date or a branch name as a version input. The nearest text is the time-dependent example "latest mainline" (S071.txt:21-22). Reasonable package guidance, but presented without a source anchor.

### 8. [Low, coverage] Recipient row (line 28) omits the larger-team rule
- Attacked: "With two or fewer maintainer recipients, the security team must be Cc'd."
- The page says "two or fewer recipients in your message" (S071.txt:271-272), which the row narrows to "maintainer recipients". That reading is defensible, since the report "must be sent to maintainers" (S071.txt:271). The row omits the larger-team rule: "For larger teams, Cc: the Linux kernel security team for your first few reports or when seeking specific help" (S071.txt:275-277). The row's question "Who receives the report?" is answered only for the small-team case.

## Claims that hold (verified against S071.txt)
- Scope, line 9 ("governs reports sent to the kernel security list and to kernel maintainers"): consistent with S071.txt:112-113 and S071.txt:281-282.
- Section list, line 11: the quote at S017-18 is exact; the four bullets are at S20, S31, S35, S45, matching "listed at S071.txt:20-47".
- Row quotes, all exact: S20-22 (version), S22-23 (stable identifier), S21-22 (time-dependent, marked paraphrased), S23-24 (distro), S39-40 (binary), S41-43 (reproduction), S95-96 (AI public), S99 (no public reproducer), S210-211 (shared on request), S305 (release process), S342-344 (occasional embargoes), S310-311 (7/14 days), S312 (agreed), S312-314 (only valid reason), S350 (linux-distros accepted), S271-273 (recipients and Cc).
- CVE row (line 29, S362-363): "does not assign CVEs, nor do we require them for reports or fixes". "Do not list a CVE as a required field. Its absence is not a defect under this page." holds.
- Limits line 48 "no 7.3 match in S071.txt": `grep -c '7\.3'` printed `0`.

## Verification performed
1. Quote check (`tmp` script over 26 hand-extracted pairs). Command: `python3 check.py`. Output: `SUMMARY real pass 26 / 26 | controls failing as expected 5 / 5`.
2. Parser over the knowledge file itself (`parse.py`). It extracts every `“quote” (S071.txt:a-b)` pair in lines 7-13 and 15-29. Output: `[as-landed] quote+cite pairs in scope: 18; failing: 0`.
3. Do-nothing and planted-defect controls (must fail; they do):
   - `FAIL CTRL absent-sentence` ("The kernel security team pays bounties for every report" — not in source).
   - `FAIL CTRL wrong-cite` (7-day quote cited to S1-9).
   - `FAIL CTRL altered-number` ("up to 30 calendar days" cited to S310-311).
   - `FAIL CTRL reverse-claim` ("you may keep it private" cited to S95-96).
   - `FAIL CTRL linux-distros-permitted` ("you may contact linux-distros as soon as you report" cited to S348-357).
   - Mutant of the knowledge file (14 changed to 30 in one quote; one cite changed to 20-21): `[planted-mutant] ... failing: 2`, both mutations flagged.
4. Grep for private/public wording in S071.txt (see Finding 1), and capture hash against the manifest (see Source identity).

## Limitations
- The quote check is an exact-substring check after normalising whitespace and Markdown. It cannot judge the sense of a paraphrase. The findings above on force and scope are my reading of the cited text.
- Verified against the pinned capture in the export, not the live page. No network check was run; documentation only.
- Second-half claims (`## Overlap and novelty`, `## Rejected over-generalizations`, `## Falsifiable package rule`) are out of this seat's scope and were not attacked. One note for the second-half seat: the falsifiable rule's step (2) says the deferral "must be at most 7 calendar days", which conflicts with its step (3) allowing 14 days with agreement (S071.txt:310-312).
- No edits were made to any tree; the lane tree, the export, and shared files are unchanged. Scratch removed on exit.
