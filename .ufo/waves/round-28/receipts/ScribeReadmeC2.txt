ScribeReadmeC2 — round-28 wave 1, C2 coverage: corpus/README.md F12 frontier row, admitted-count
amendment, coverage-map/expected-list reconciliation note.

Rev 2 (post-landing re-measurement, 2026-10-25). Superseded values from Rev 1, logged old -> new
(R9 append discipline; no earlier measurement is erased):
  - state label: "frontier harness PRE-STATE" -> "frontier harness MEASURED PASS (entries=15 pass=15 exit=0)"
  - README sha256: e38ba5673c0f6789d3de33cf688ccfa3bc88684ed24fd48afe1b891fe7a815a4 -> 5f458a7a26b8dfc2dd2ee2e46e11380d5697e51e77213772bce7b59253363180
  - README lines: 243 -> 245 ; git diff --numstat: 26 0 -> 28 0 (still zero deletions)
  - ExecExpectedList receipt: absent -> present (read; same 41 = 39 + 2 reconciliation)
  - recheck-audit: exit 0 unexpected=0 -> exit 1 unexpected=1 (the entry landed before the list was
    regenerated; the expected-list update is not this seat's file)
  - F12 next cell: added the 45-day trigger contrast as a same-line suffix (reviewer suggestion,
    both sides grounded — see §1(a))
  - reconciliation note: the as-of "receipt had not yet landed" sentence was replaced by the landed
    receipt + the measured audit state (this note is same-round text by this seat, not a historical
    record; the r28 amendment paragraph and the round-26 sentence above it are untouched)

Lane root: /home/vgpnk/Projects/shokunin/kasegi-shokunin
Lane HEAD at work: 94f387cbee71a532a51ce075f01701a557231e85 (round-28 wave1 spec + dispatch)
Claims-freeze base c9f8b115a098c65356e4b3b6048af45a37ab8395 is an ancestor of HEAD
  cmd: git merge-base --is-ancestor c9f8b115a098c65356e4b3b6048af45a37ab8395 HEAD ; echo $?
  out: 0
Owned production file: corpus/README.md — the only production file this seat wrote.
Other writes: this receipt, .ufo/waves/round-28/wave1/ScribeReadmeC2.md.
Tooling installed/upgraded: NONE (no install or upgrade was needed; no pacman transaction attempted).
State label: README edit LANDED and measured; every C2 counter this seat can run is now POST-STATE
  (the entry file and the manifest both landed during the item).

1. Change — purely additive, 28 insertions / 0 deletions
   before (HEAD bytes, unmodified at start): sha256 511e15b26abfab4703e427cac4235497695ee11202aa63a1b0e4d7cadc7a34f6, 217 lines
   after:                                     sha256 5f458a7a26b8dfc2dd2ee2e46e11380d5697e51e77213772bce7b59253363180, 245 lines
   cmd: git diff --numstat -- corpus/README.md      out: 28	0	corpus/README.md
   cmd: git diff -U0 -- corpus/README.md | grep '^@@'
   out: @@ -212,0 +213 @@ ; @@ -217,0 +219,27 @@   (hunks begin at 213 and 219; lines 1-212 are
        byte-identical to HEAD)
   R6 line-identity check (sha256 of the line vs `git show HEAD:corpus/README.md`):
     line 49  same=yes   (59f63b6eac0943e281461055090b8247a2f95c90033cb5df7362d1d88acb45ff)
     line 51  same=yes   (7f270009e738ea8b86388a858712eecbdde705c5ab1e05df677ac412f4e08212)
     line 82  same=yes   (0caf6a87090f0ef9f58b75c47ee7d8f31af05635c41dadd5a13c831c46874399)
   (49 and 82 are the two corpus/README.md line cites recorded in
    corpus/instruments/citation-survival.md:144-145; both keep their number and their bytes. Lines
    1-212 are byte-identical, so no citation anywhere at <213 moved.)

   (a) Frontier row appended as the last row of the table (line 213), mirroring the F01-F11 column
       shape (`| id | topic | status | entry | sources | next |`, plain entry paths, comma-separated
       source ids):
       | F12 | Japanese state-coordinated disclosure workflow | admitted | knowledge/japanese-domestic-disclosure-workflow.md | S041, S042 | Use 起算日 — the day the guideline's Ⅳ.4.2) notification was first attempted (S041 footnote 4), not an acknowledgement or a submission date — as the Japanese column when comparing coordinator timelines against F02. The same 45-day figure is triggered differently on each side: S041's publication date is a 目安 of 45 days from 起算日 (Ⅳ.3)), CERT/CC's 45 days runs from the initial report (S004, F02). |
       Grounding for the next-cell claims, read from this round's captures / the F02 entry:
         corpus/source-snapshots/round-28/S041.txt:340
           「本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。」
         corpus/source-snapshots/round-28/S041.txt:648 (repeated at :786)
           「公表日は、JPCERT/CC が「製品開発者への連絡」（４．2）を参照）にて規定された連絡を最初に
            試みた日（起算日、２．注釈 4 を参照）から 45 日後を目安とします。」
         corpus/source-snapshots/round-28/S042.txt:145
           「JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を
            連絡した旨をIPAへ連絡します。」
         corpus/knowledge/coordinated-disclosure-timelines.md:22 (F02, row S004)
           “Vulnerabilities reported to the CERT/CC will be disclosed to the public 45 days after
            the initial report”
       The cell is paraphrase plus one short quoted fragment per side, not a republished quote.

   (b) Admitted-count amendment: the historical sentence (lines 215-218, "…11/11 admitted at round
       26; F01-F08 at round 23, F09 at round 24, F10 at round 25, F11 at round 26…") is retained
       verbatim; a new paragraph at line 220 records "12/12 admitted — … F12 at round 28" and states
       that the parenthetical is history, not rewritten (R9). The two 0/18 lost-domain sentences are
       diff context lines, neither added nor removed.

   (c) "## Round-28 reconciliation — coverage map and expected list (appended 2026-10-25)" appended
       at end of file (lines 226-245): names knowledge/japanese-domestic-disclosure-workflow.md as
       the round-28 coverage entry (Frontier F12, S041 + S042, capture basis
       corpus/source-snapshots/round-28/), explains why the coverage map gains no in-place line
       (R6), records the expected-list count basis, cites
       .ufo/waves/round-28/receipts/ExecExpectedList.txt as its confirmation, and records the
       measured audit state once the entry landed.

2. Frozen C2 counter 1 — frontier admitted
   cmd: awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
   before (HEAD bytes, measured 2026-10-25): 11
   after  (edited bytes):                    12
   target after value: 12 — REACHED.
   Frozen C2 counter 2 (entries citing S042): 0 -> 1, measured after ScribeEntryC2 landed:
   `grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l` -> 1 (the new entry only). Not this
   seat's file; recorded because the README row points at it.

3. Frontier harness — MEASURED PASS (post-landing)
   cmd: python3 corpus/instruments/frontier-recheck-count.py ; echo harness_exit=$?
   out (last lines):
     PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0
     entries=15 pass=15 exit=0
     harness_exit=0
   target after value (frozen C2): entries=15 pass=15 exit=0 — REACHED.
   Pre-landing state (Rev 1, kept for history): 14 PASS lines then
   FileNotFoundError: corpus/knowledge/japanese-domestic-disclosure-workflow.md, exit 1 — i.e. the
   harness had already accepted the README row shape and failed only on the absent entry file. The
   entry's header declares S041 + S042 and its recheck selects both, which is why F12 passes R12.

4. Expected-list count basis (measured 2026-10-25; the r27 carry-forward item 4 reconciliation)
   cmd: wc -l < corpus/instruments/knowledge-expected.txt            out: 41
   cmd: grep -c '^#' corpus/instruments/knowledge-expected.txt       out: 2 (header comments)
   cmd: grep -vc '^#' corpus/instruments/knowledge-expected.txt      out: 39 (entries)
   Reconciliation: the round-27 lesson's "41 lines / 39 entries" pair is a units mismatch, not a
   drift — 41 file lines = 39 entry lines + 2 comment lines. Independently confirmed by
   .ufo/waves/round-28/receipts/ExecExpectedList.txt §2 (`git ls-files corpus/knowledge/*.md | wc -l`
   -> 39, `wc -l` -> 41, `grep -c '^#'` -> 2); that receipt records no production edits and does not
   regenerate the list.
   Current audit state (entry landed, list not regenerated):
     cmd: python3 corpus/instruments/recheck-audit.py --quiet ; echo exit=$?
     out: lines=40 total=40 pass=40 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
          expect=present expected=39 missing=0 unexpected=1 exit=1
   This is exactly the state the README note predicts: the new file is `unexpected` until the list
   gains its line (40 entries / 42 lines). Updating corpus/instruments/knowledge-expected.txt is not
   this seat's owned file, so the reconciliation is routed: L1 must regenerate it and re-run the
   audit to exit 0. Nothing in the README edit depends on that update.

5. Capture presence read (not authored by this seat; used to ground §1(a))
   corpus/source-snapshots/round-28/S041.txt   147267 B  (ExecCaptureS041)
   corpus/source-snapshots/round-28/S042.txt    60508 B  (ExecCaptureS042)
   corpus/source-snapshots/round-28/manifest.json  ids = ['S041', 'S042']
   cmd: python3 -c "import json;d=json.load(open('corpus/source-snapshots/round-28/manifest.json'));
        print([r.get('id') for r in d.get('sources',d.get('records',[]))])"   out: ['S041', 'S042']

6. Known limits
   - README's F12 sources cell asserts S041 + S042 per the frozen claim; the entry's header and
     recheck are ScribeEntryC2's deliverable. They were read after landing (headers show S041, S042;
     recheck selects both against corpus/source-snapshots/round-28/manifest.json) but the entry's
     own claim/quote verification is not this seat's audit.
   - The 起算日 and 45-day cells are grounded on the capture lines quoted in §1(a) and on F02's entry
     for the CERT/CC side; no live network fetch was made by this seat.
   - recheck-audit currently exits 1 for the expected-list reason in §4; that is a measured state,
     not a defect in the README edit.
   - No build/lint/test suite exists for markdown; verification is limited to the counts, diffs and
     instrument runs above. Nothing beyond those commands is claimed.

7. Out of scope / untouched
   corpus/SOURCES.md (ScribeRegistryC2), corpus/knowledge/japanese-domestic-disclosure-workflow.md
   (ScribeEntryC2), corpus/QUALITY.md (ScribeR14), corpus/instruments/* including
   knowledge-expected.txt (ExecImplC1, ExecInstrReadme, ExecExpectedList), SKILL.md
   (ScribeSkillGate), corpus/lessons/*, LOG.md, SCORECARD.md, claims.json. No VCS write, no git
   add/commit/push, no jj mutation, no subagent dispatch.
