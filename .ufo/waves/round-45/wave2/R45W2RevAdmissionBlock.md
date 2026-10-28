VERDICT: HOLDS

Seat: R45W2RevAdmissionBlock (leaf, read-only). Tree attacked: EXPORT of lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (`git archive ... | tar -x`), scratch-only. Base control: EXPORT of round base dc5bb8c6e31efc4a6650819df85e79b72fd64bcd. No edits, no commits, no index mutation.

Scope attacked: `corpus/README.md` `## Round-45 admission` block (lines 634-653), `PROVINCE.md` r45 line (line 169), F27 row (README line 651), S071/S072 rows and round-45 snapshot, the frontier counter `corpus/instruments/r44-frontier-count.py` (v1.1 read), `corpus/instruments/frontier-recheck-count.py`.

The block's central claims survive falsification: pure append, six-cell F27 row with status third, a 27/27 count that a base control refutes (26), and the 0/18 carried sentence is consistent with the filesystem. Two non-breaking defects were found (F5 path convention in the block; F6 live-lane binding in the recheck harness). Neither changes the 27 count.

---------------------------------------------------------------
F1 HOLDS — pure-append, end-of-file only (attacked: lane commit diff of corpus/README.md + PROVINCE.md)

Command:
  git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --numstat dc5bb8c6e31efc4a6650819df85e79b72fd64bcd 6662a4276b6f7bd61e23e12058414e09dd71b9e4 -- corpus/README.md PROVINCE.md
Output:
  2	0	PROVINCE.md
  21	0	corpus/README.md
Command:
  git ... diff dc5bb8c... 6662a42... -- corpus/README.md PROVINCE.md | grep -c '^-[^-]'
Output: 0
Command (covers removed lines beginning with `--`, which the task's grep form would miss):
  ... | grep '^-' | grep -v '^--- a/' | wc -l
Output: 0
Hunks:
  @@ -165,3 +165,5 @@ ...   (PROVINCE.md)
  @@ -630,3 +630,24 @@ ...  (corpus/README.md)
Both hunks begin at the original EOF context (PROVINCE 165-167 of 167; README 630-632 of 632).

---------------------------------------------------------------
F2 HOLDS — F27 row shape (attacked: all `^| F\d+ \|` rows of export corpus/README.md)

Command: python3 snippet splitting each row on `|` after strip.
Output: `rows 27` / `cell-counts(incl. edge) Counter({6: 27})`
Output for F27: `F27 status= 'admitted' entry= \`corpus/knowledge/linux-kernel-security-bugs-reporting-process.md\` sources= S071`
Status is the third cell (index 2) for all rows; F26 template row (line 628) has the same six-cell shape.

---------------------------------------------------------------
F3 HOLDS — 27/27 count line and counter (attacked: `corpus/instruments/r44-frontier-count.py` on the export, plus base control and mutant)

Command: python3 corpus/instruments/r44-frontier-count.py --root <export> --expect 27 --ids
Output:
  frontier-ids=F01,F02,...,F27
  frontier rows=27 admitted=27
  exit=0
Command: python3 corpus/instruments/r44-frontier-count.py --selftest
Output tail: `mutants=10 rejected=10` / `selftest cases=43 failures=0` / exit 0.

Discrimination (do-nothing / base control, base dc5bb8c):
  python3 corpus/instruments/r44-frontier-count.py --root <base>      -> `frontier rows=26 admitted=26`, exit 0
  python3 corpus/instruments/r44-frontier-count.py --root <base> --expect 27 -> `frontier expected=27 admitted=26 verdict=SHORT exit=1`, exit 1
Mutant (copy of export, F27 status cell set to `queued`, README line 651):
  `frontier rows=27 admitted=26` / `frontier expected=27 admitted=26 verdict=SHORT exit=1`, exit 1
So the 27 is measured, not asserted.

Caveat: the prose line "27/27 admitted" (README line 653) is not bound by any instrument; I verified it by hand against the counter (27 = 27).

---------------------------------------------------------------
F4 HOLDS — S071 located quotes and frontier-recheck census (attacked: corpus/source-snapshots/round-45/{S071.txt,manifest.json}, corpus/instruments/frontier-recheck-count.py)

Command: python3 corpus/instruments/frontier-recheck-count.py --root <export> --json <scratch>/recheck.json
Output (first line): `FRONTIER-CENSUS rows=27 admitted=27 closed=27 problem-rows=0 registry=72`
Output (last line): `entries=30 pass=30 exit=0`; JSON `schema: kasegi-frontier-recheck-receipt-v1`, `duplicate_entry: None`.
F27 line: `PASS F27 corpus/knowledge/linux-kernel-security-bugs-reporting-process.md ids=S071 exit=0`.

Quote check (whitespace/markup normalised, against pinned bytes):
  Q1 FOUND 'for up to 7 calendar days from the start of the release proc...'  (S071.txt:310-311)
  Q2 FOUND 'If you resorted to AI assistance to identify a bug, you must...'  (S071.txt:95-96)
  Q3 FOUND 'Binary-only executables are not accepted.'                        (S071.txt:39-40)
  Q4 FOUND 'By definition if an issue cannot be reproduced, it is not ex...' (S071.txt:41-43)
  Q5 FOUND 'with no version indication, your report will not be processe...' (S071.txt:20-21)
So the block's 7-day/14-day, AI-as-public, binary-only and unreproducible claims match the pinned capture.
Source-recheck for S071 run directly on the export: `S071:Q1 OK ... anchor=310-ok` ... `S071:Q5 OK ... anchor=20-ok`, exit 0.

---------------------------------------------------------------
F5 DEFECT (LOW, block convention) — F27 entry path base differs from the round-44 template and all other rows (attacked: README lines 628, 642-ish Area row, 651)

Command: python3 snippet classifying each frontier row's entry cell.
Output: `Counter({'bare': 26, 'corpus/': 1})` — every F01-F26 entry is corpus-relative (`knowledge/...`); only F27 uses `corpus/knowledge/...`.
F26 (README line 628): `| F26 | ... | admitted | \`knowledge/google-cloud-vrp-customer-resource-boundary.md\` | S069 | ... |`
F27 (README line 651): `| F27 | ... | admitted | \`corpus/knowledge/linux-kernel-security-bugs-reporting-process.md\` | S071 | ... |`
The Area-table row of the round-45 block also writes `corpus/knowledge/...` where the round-44 block writes `knowledge/...`.
Reader check: ls corpus/corpus/knowledge/linux-kernel-security-bugs-reporting-process.md -> `No such file or directory`.
Impact: none on counts (the harness resolves `root/<entry>` then `root/corpus/<entry>`; F27 PASSES). It is a convention break a human reader following the row from corpus/ mis-resolves.
Proposed correction for the L1 (not drafted, reviewer seat): drop the `corpus/` prefix in the round-45 Area-table entry cell and in the F27 frontier-row entry cell, so the block matches F26 and the rest of the table.

---------------------------------------------------------------
F6 DEFECT (MEDIUM, verifiability of the C2 recheck receipt; not the block bytes) — the recheck harness is not export-bound (attacked: frontier-recheck-count.py run lines 262-270; `recheck:` lines of corpus/knowledge/*.md)

Command: grep -ln "^recheck:.*cd /home/vgpnk/Projects/shokunin/kasegi-shokunin" corpus/knowledge/*.md | wc -l
Output: 63 (of 64 knowledge entries; the one without it is the non-matching file).
Sample (F26 entry): `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-44/manifest.json --source S069 # 180d`
F27 entry: `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071 # 180d`
The harness runs each line with `subprocess.run(["bash","-c",recheck], cwd=root)` (frontier-recheck-count.py:269-270). The embedded `cd` overrides cwd, so the "export" PASS reads the LIVE lane's bytes.
Current state: sha256 prefixes match for S071.txt (0918dcfa7979f348), manifest.json (125339d9ec21bfdc), F27 entry (4ee4e7422211db2f), README (d402b740cb001a5c), PROVINCE.md (221ae42393cea5c7), live == export. So no false PASS is observed today; the receipt `entries=30 pass=30` is simply not reproducible from the export alone.
Disclosure: I ran the harness and one direct source-recheck with the live cwd that those lines embed. This was read-only; source-recheck.py default mode writes nothing (its only write calls, lines 280 and 298, are inside the selftest temp directory). I did not modify the live lane.
Proposed fix for the C2 owner: the harness should refuse or rewrite `cd <absolute path outside root>` in recheck lines, or the lines should be root-relative.

---------------------------------------------------------------
F7 OBSERVATION (LOW, out of this seat; for the C2 reviewer) — corpus/instruments/r45-c2-gate.py:56 sets `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`, a fleet-root path rather than a lane-relative one. Not run or traced further here.

---------------------------------------------------------------
F8 HOLDS with note (INFO) — PROVINCE 'Refuses/Adjacent' scope (attacked: PROVINCE.md lines 1-53, r45 line 169, entry scope section)

Command: sed -n 1,53p PROVINCE.md
Scope text: Domain "bounty & security research — scopes ~/Projects/bounties, program rules, claim packages"; Refuses "anything outside this domain"; Adjacent "chousa, kagi, kake, kengaku"; "Live-target testing is refused; this corpus is documentation only."
In-domain by precedent: F10 (single vendor policy), F26 (single program's rules, admitted round 44), F11 (ISO), F24 (RFC 9116), F25 (CVE JSON) are admitted under the same Frontier heading. A single project's reporting rule is the same class as F10/F26. Kernel material is therefore admissible as disclosure practice, not as bounty scope; the entry itself says "This entry records one upstream project's reporting rule ... it is not general guidance on coordinated disclosure" (entry line 9).
Note: PROVINCE.md lines 35-37 still read "General practice that governs every program"; this is pre-existing wording, contradicted by the admitted single-party F10/F26 rows. Not introduced by r45; the r45 line does not repair it.
Adjacency: CVE and linux-distros material is excluded by S071 itself (`S071.txt:350`, `S071.txt:362-363`) and by the entry (lines 27, 29, 37, 60). The AI-found section overlaps F04 (in-lane), not kengaku (LLM evaluation). No sibling-lane absorption found.
Live testing: grep -n -i "exploit|fuzz|live|target|run the|test" on the entry returns only quotes and caveats (lines 18, 21, 42, 49: "Re-open the live page before relying on ..."). No instruction to test live kernels.

---------------------------------------------------------------
F9 LOW (carried claim) — "lost-domain denominator remains 0/18" (attacked: README line 56, 215-223, 653; corpus/knowledge/source-tree-loss-2026-09-28.md:64-82)

Command: for p in ~/Projects/bounties ~/Projects/the-bounty-hunter ~/Projects/origin-work; do test -e "$p" ...
Output: all three `absent`.
The 0/18 sentence has been carried verbatim since round 23 (README lines 215-223 and every amendment thereafter). The denominator is a prose list of 18 items (source-tree-loss...md:64-82), not enumerated as paths, so the export can only test root-level absence. The block asserts "remains" without a per-surface measurement. Consistent with the filesystem; not independently measured per item.

---------------------------------------------------------------
Control summary
- Do-nothing/base control (dc5bb8c): counter 26, `--expect 27` SHORT. The block's 27 claim is discriminated from the base.
- Mutant (F27 status queued): 26, SHORT. The counter fails when the admission is undone.
- Selftest: 43 cases, 0 failures; 10 mutants, 10 rejected.

Limitations
- No network access. The S071 bytes were checked against the pinned capture, not against the live docs.kernel.org page (documentation-only lane; the entry itself says to re-open the live page before relying on dated figures).
- The per-surface 0/18 claim is tested only at the root path level (F9).
- The frontier-recheck run executed the live-lane `cd` embedded in recheck lines (F6); read-only, disclosed.
- I did not review the entry body beyond the scope, decision table and recheck line, nor SKILL.md or corpus/instruments/README.md round-45 rows (outside this seat's listed scope).
- No tools installed or upgraded. No commits, pushes, index or git mutations; export and base trees are scratch copies removed on exit.
