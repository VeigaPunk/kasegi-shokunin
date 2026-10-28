VERDICT: BROKEN

Scope: F27 entry quote review 2. Curly-quoted spans #9-#16 in file order of `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md`, from export of lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (`git archive | tar -x` into scratch; the moving lane tree was not read). Snapshot: `corpus/source-snapshots/round-45/S071.txt` (sha256 0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40, matches the SOURCES.md S071 prefix). Live: `curl -sSL https://docs.kernel.org/process/security-bugs.html` (HTTP 200, 33621 bytes, fetched 2026-10-28T21:38Z, html sha256 prefix 174a89d065a58c46), tags stripped. Live match is textual (rendered HTML has no line numbers); location is checked against the snapshot.

Enumeration (`grep` of curly spans, 24 total; #9-#16 printed):
- #9 entry L23 cite S071.txt:210-211
- #10 entry L24 cite 305
- #11 entry L24 cite 342-344
- #12 entry L25 cite 310-311
- #13 entry L25 cite 312
- #14 entry L26 cite 312-314
- #15 entry L27 cite 350
- #16 entry L28 cite 271-272

Per-quote result (quote text is an exact match after normalising curly quotes and whitespace; "tight" = the smallest snapshot line window containing the whole quote equals the cited range; no LOOSE-RANGE found):

1. #9 "the reproducer should only be shared upon maintainers' request" — OK. Snapshot 210-211 (`sed -n 210,211p`: "report will be posted to a public list, the reproducer should only be" / "shared upon maintainers' request."). Tight. Live: found verbatim (live.txt:228-229). Paraphrase (L23: "available on maintainer request; keep it out of the public text") is faithful. Context note: the sentence sits in the AI-assisted-reports paragraph; the row applies it as a general reproducer rule. Not a quote defect; the general public-body rule is S071.txt:99 (quote #8, outside this review).

2. #10 "Once a robust fix has been developed, the release process starts" — OK. Snapshot 305 (`Once a robust fix has been developed, the release process starts.  Fixes`). Tight. Live found (live.txt:306). Paraphrase ("the clock starts at the release-process start after a fix exists. It does not start at the report date") — the "embargo clock" label is the entry's own term; the page never uses it; the "does not start at the report date" half is an inference, not stated. Flag as paraphrase LOOSE (inference, not a quote defect).

3. #11 "for the kernel security team occasional embargoes (as subject to a maximum allowed number of days) start from the availability of a fix" — OK. Snapshot 342-344 (starts mid-line 342 at "for the kernel", ends 344 "days) start from ... of a fix,"). Tight. Live found (live.txt:336-338). Starting mid-sentence drops only the contrast clause ("while for linux-distros ..."); no meaning flip. Paraphrase fine.

4. #12 "for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days" — OK. Snapshot 310-311. Tight. Live found (live.txt:310-311). Paraphrase ("7-day ceiling; 14-day extension requires agreement") fine. Note: the row drops the "at the request of the reporter or an affected party" condition here; it is stated at line 58 of the entry, so no defect.

5. #13 "if it is agreed that the criticality of the bug requires more time" — OK. Snapshot 312. Tight. Live found (live.txt:312). Paraphrase "requires the agreement the page names" — OVERSTATED: the page says "it is agreed" and does not name who agrees. Paraphrase LOOSE (not a quote defect).

6. #14 "The only valid reason for deferring the publication of a fix is to accommodate the logistics of QA" — BROKEN (truncated mid-sentence; meaning narrowed).
   - Snapshot (`sed -n 312,315p`, numbered):
     312 `if it is agreed that the criticality of the bug requires more time.  The`
     313 `only valid reason for deferring the publication of a fix is to accommodate`
     314 `the logistics of QA and large scale rollouts which require release`
     315 `coordination.`
   - Live (`sed -n 312,315p live.txt`): identical sentence, "...logistics of QA and large scale rollouts which require release / coordination."
   - The quote ends at "QA" and drops "and large scale rollouts which require release coordination." As displayed, it states that QA logistics is the only valid deferral reason; the page states the only valid reasons are QA logistics and large-scale rollouts. That changes the set of valid reasons, so the quote misstates the page on its face.
   - Cited range 312-314 is also one line short of the sentence end (line 315). A quote extended to the full sentence needs S071.txt:312-315.
   - Paraphrase (L26: "Record QA or large-scale rollout coordination as the reason") is itself acceptable on content, but it uses "or" where the source's sentence has "and"; the table row is right, the quote beside it is not.
   - Fix: extend the quote through "coordination." and cite 312-315 (or quote only "The only valid reason ... to accommodate the logistics of QA and large scale rollouts which require release coordination").

7. #15 "a fix is accepted by the affected code's maintainers" — OK quote. Snapshot 350 (`mailing list UNTIL a fix is accepted by the affected code's maintainers`). Tight. Live found (live.txt:343). Paraphrase (L27: "Record linux-distros contact as not yet permitted until the maintainers accept the fix") OVERSTATES MODALITY: the page says "the kernel security team strongly recommends that ... you DO NOT contact the 'linux-distros' mailing list UNTIL a fix is accepted" (snapshot 348-350; live 341-343). It is a strong recommendation, not a permission rule. Paraphrase LOOSE.

8. #16 "If there are two or fewer recipients in your message" — OK. Snapshot 271-272 (`The report must be sent to maintainers.  If there are two or fewer` / `recipients in your message, you must also always Cc: the Linux kernel`). Tight. Live found (live.txt:277-278). Ends at a clause boundary (before the comma), no meaning flip. Paraphrase ("two or fewer maintainer recipients ... security team must be Cc'd") faithful.

Discrimination (`controls.py`, output printed):
- POS #14 cited 312-314: `in_snapshot[312-314]=True in_live=True`
- POS #14 full sentence cited 312-314: `in_snapshot[312-314]=False in_live=True` (confirms the cite is one line short of the sentence)
- POS #14 full sentence widened 312-315: `in_snapshot[312-315]=True in_live=True`
- NEG #16 "three or fewer": `in_snapshot[271-272]=False in_live=False`
- NEG #12 "21 calendar days": `in_snapshot[310-311]=False in_live=False`
- NEG #14 wrong lines 300-310: `in_snapshot[300-310]=False`
- NEG #10 at line 306 only: `in_snapshot[306-306]=False`
- NEG #9 at 205-209: `in_snapshot[205-209]=False`
- NEG #15 fabricated sentence: `in_snapshot[348-350]=False in_live=False`
The live check is location-insensitive (`in_live=True` in the wrong-line rows is expected); location discrimination comes from the snapshot rows.

Tightness check (`tight.py`): all eight cited ranges equal the minimal containing window (#9 210-211, #10 305, #11 342-344, #12 310-311, #13 312, #14 312-314, #15 350, #16 271-272). No LOOSE-RANGE in #9-#16.

Summary: quotes located and exact: 8/8 (live and snapshot). Quote-level verdicts: OK #9, #10, #11, #12, #13, #15, #16; BROKEN #14 (truncated mid-sentence, meaning narrowed, cite one line short). Paraphrase defects (not quote defects): #10 inference, #13 "the agreement the page names", #15 "not yet permitted" overstates a recommendation.

Limitations: only #9-#16 reviewed (spans #1-#8 and #17-#24 are other reviewers' scope). Live page checked textually after tag stripping and curly-quote normalisation; no visual rendering. The snapshot is the RST source (`_sources/...rst.txt`), not the HTML; the wording matches on these eight spans. Single fetch; no historical comparison. Scratch dir removed on exit. No git mutation, no commit, no edits outside this report.
