VERDICT: BROKEN

Seat R46bW2RevRegistryText — registry surface attack, round 46 attempt 2 wave 2.
Tree under attack: lane HEAD 96379ae (wave-1 integration; freeze fe0f56b, base 04af9bc9).
All commands run from /home/vgpnk/Projects/shokunin/kasegi-shokunin unless noted. Scratch:
/fast/scratch/hyaku/kasegi-r46/R46bW2RevRegistryText (removed on exit).

=====================================================================
FINDING 1 (critical) — corpus/instruments/r46-counters-selftest-c2.py crashes at import time
=====================================================================
Attacked artifacts: registry rows for r46-c2-gate.py and r46-counters-selftest-c2.py
(corpus/instruments/README.md lines 999 and 1002; SKILL.md lines 1162 and 1165 — the rows are
byte-identical across the two files, verified by md5), plus the C1-after plain command.

The row claims: "run `corpus/instruments/r46-counters-selftest-c2.py` with --lane DIR --pure DIR;
prints `selftest cases=N failures=F` ... exit 0 only when failures=0".

Command actually run (every invocation, including --help):
  $ python3 corpus/instruments/r46-counters-selftest-c2.py --pure .
  Traceback (most recent call last):
    File ".../corpus/instruments/r46-counters-selftest-c2.py", line 68, in <module>
      EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}
      ^^^^^^^^^^^^^
  NameError: name 'C1_ENTRIES' is not defined
  EXIT=1

Root cause: line 68 references C1_ENTRIES before its definition at line 69
(`C1_ENTRIES = {"claim-gates.md", "claim-package-contract.md"}`). Import-time, so no invocation
reaches argparse. The committed instrument cannot print `selftest cases=<N> failures=<F>` at all;
the registry row's claimed output is unreachable, and the claims' C1 plain measure
(`python3 corpus/instruments/r46-counters-selftest-c2.py --pure <pure> | tail -1`) cannot print
cases=137/147 failures=0. The integration's own receipt knew this:
.ufo/waves/round-46/attempt2/controls/final-battery.txt records the NameError then labels it
"exit=0" (the crash actually exits 1) and the file is truncated immediately after "== battery c1:".
No erratum (counter-errata.md E1-E4) discloses the defect; E2 asserts "the c2 selftest mirrors
the exemption" as if it ran.

=====================================================================
FINDING 2 (critical) — corpus/instruments/r46-counters-selftest-c1.py crashes at case
L4-row-anchor-moved against the mandated pure base export
=====================================================================
Attacked artifact: registry row r46-counters-selftest-c1.py (README.md line 1001, SKILL.md line
1164), which claims the selftest prints `selftest cases=N failures=F`, exit 0 iff failures=0.
Usage per the instrument docstring and claims' plain list: --pure = pure base export (04af9bc9).

Command actually run (twice: --jobs 8 and --jobs 1, fresh --work; deterministic):
  $ python3 corpus/instruments/r46-counters-selftest-c1.py --pure $S/base --work $S/c1work2 --jobs 8
  ...
    File ".../r46-counters-selftest-c1.py", line 249, in m_anchor_moved
      row_edit(t, CG, "G1", lambda ln: re.sub(r"`([^`:]+):(\d+)`", ...))
    File ".../r46-counters-selftest-c1.py", line 155, in edit
      assert new != old, "mutation was a no-op on " + rel
  AssertionError: mutation was a no-op on corpus/knowledge/claim-gates.md
  EXIT=1   (zero `case` lines printed)

Root cause (reproduced by simulating the TIP build in scratch): `row_edit` selects the FIRST
`| G1 |` row of the TIP tree's claim-gates.md, which is the entry's pre-existing row
(base export line 134):
  | G1 | Required: `report.md`, ..., `evidence/manifest.json` (L10-11) | `corpus/instruments/claim-package-check.py:101-108` | `'custodian-receipts.json',` |
Its anchor is a line RANGE (`:101-108`), which the case regex `` `([^`:]+):(\d+)` `` cannot match
(needs a backtick immediately after the digits), so re.sub returns the string unchanged and the
no-op assert fires. The synthetic G1 row the case was written for (anchor
`corpus/instruments/claim-package-check.py:131`) is appended AFTER it and is never reached.
The wave-1 receipt .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/receipts/02-after-extended-selftest.txt
("selftest cases=83 failures=0") was produced against a scratch pure tree
(/fast/scratch/hyaku/kasegi-r46/L1/pure2, per R46bExecSelftestC1.md line 67), not the pinned base
export, and is not reproducible at the final tree; the integration receipt final-battery.txt's
"== selftest c1 (extended): cases=83 failures=0 exit=0" is likewise not reproducible with the
committed bytes and the documented --pure.

=====================================================================
FINDING 3 (critical) — corpus/instruments/r46-selftest-f29.py hardcodes an expected-28 frontier
=====================================================================
Attacked artifacts: registry rows r46-selftest-f29.py (README.md line 1019, SKILL.md line 1173)
and, transitively, r46-f29-gate.py's row (README.md line 1018, SKILL.md line 1172) which states
the selftest "grades it on synthetic trees ... (30 cases, failures=0, exit 0, measured on the
wave-1 draft)"; also counter-errata.md E4 ("R50 disclosures (a),(b),(d),(e) are graded by the
committed r46-selftest-f29.py with rebuilt PINS") and the R50 receipt's Frozen duty.

Commands actually run:
  $ python3 corpus/instruments/r46-selftest-f29.py --lane . --work $S/f29work
  note provenance f29-defects.py sha256=2e95d4d4... matches
  note provenance f29-fixture.py sha256=52ea9693... matches
  selftest: lane README carries 29 frontier rows, expected 28
  EXIT=1
  $ python3 corpus/instruments/r46-selftest-f29.py --do-nothing-control
  ...
  selftest: lane README carries 29 frontier rows, expected 28
  EXIT=1

Root cause: build_positive (line 188) raises SystemExit unless the lane README has exactly 28
frontier rows; wave-1 integration added F29, so the committed selftest cannot run any case on the
tree it was committed to, in both normal and do-nothing-control arms. The claimed 30-case /
29-FAIL outputs are unreachable as committed. (The provenance notes themselves did verify:
f29-defects.py and f29-fixture.py sha256 pins match.)

=====================================================================
FINDING 4 (major) — controls/f29-fixture.py pinned control tooling is stale (assert 28 vs 29)
=====================================================================
Attacked artifacts: the C2 claim's do-nothing controls (claims.json C2 kill_rule: junk-entry and
fabricated-quote trees must grade <7/7) and the R50 receipt's pinned fixtures
("Positive tree reads f29-gate fixed=7/7 exit=0; junk 3/7; fabricated 3/7").

Command actually run:
  $ python3 .ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode junk --dir $S/junk2 --lane .
  ...
    File ".../controls/f29-fixture.py", line 135, in build
      assert len(frows) == 28, len(frows)
  AssertionError: 29
  FIXTURE-EXIT=1   (leaves a partial tree: knowledge/ + source-snapshots/ only)

Because the fixture aborts after copying the knowledge dir and entry but before writing
README/SOURCES, a gate run over the residue is not the intended control recipe (my residue runs
happened to print 3/7 for junk/fabricated, matching the R50 numbers by accident of partial
content — H1 rows=0, H3 absent, H7 registry-sections=0 on the missing files; these are NOT
reproductions of the receipt's control trees). The pinned positive/junk/fabricated control trees
cannot be rebuilt from the current lane, so the R50 receipt's control readings are not
reproducible at the final tree.

=====================================================================
FINDING 5 (minor) — registry row for r46-f29-gate.py is stale about versions and "planned" status
=====================================================================
Attacked artifact: corpus/instruments/README.md line 1018 (== SKILL.md line 1172).
The row still describes the gate as "the committed v1" — but erratum E4 landed v1.1 at
integration and the committed bytes differ from the frozen v1 (committed sha256
5d192dfd66fa... vs freeze.txt pin a1091e246a...; verified `git show fe0f56b:.../r46-f29-gate.py |
sha256sum` = a1091e24...). v1.1 clauses (frontier_anywhere line 151, registry-sections line 360)
are present in the committed file, while its docstring still says "v1.". The row also states the
f29 battery mode is "planned — the committed v1 rejects --counter f29"; as committed, mutbat v1.1
accepts it:
  $ python3 corpus/instruments/r46-mutbat.py --root . --pure $S/base --work $S/mbwork --counter f29 --list
  f29 H1a counts-loose | ... (21 f29 mutants listed)   EXIT=0
The row's draft-era measurements ("30 cases, failures=0, measured on the wave-1 draft") are labeled
draft, but a reader cannot obtain any green measurement from the committed instruments (Findings
1-3).

=====================================================================
SURFACES THAT HELD (checked, not assumed)
=====================================================================
1. S074 row, corpus/SOURCES.md line 80 — 11 cells (id|source|kind|tier|scope|anchor|teaches|
   status|opened|recheck|used-by, header line 5). kind=docs, tier=A, status=mined,
   opened=2026-10-29 (== manifest fetched_utc 2026-10-29T20:19:30Z), recheck=90d (matches the
   entry's recheck line), used-by=corpus/knowledge/github-repository-security-advisories.md
   (exists, 143 lines). Anchor cell matches the manifest on every pinned field: sha256
   1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039
   (`sha256sum corpus/source-snapshots/round-46-a2/S074.txt` reproduced it), 42 lines / 7087
   snapshot bytes / 582877 raw bytes, HTTP 200, final URL == row URL. Manifest sha256
   46e8077a... == freeze.txt pin manifest-a2-sha256. Attempt-1 manifest untouched:
   `sha256sum corpus/source-snapshots/round-46/manifest.json` =
   01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34 == base blob
   (git cat-file verified). Gate cross-check: `python3 corpus/instruments/r46-f29-gate.py --root .`
   prints 7/7 with H3 read=row-S074=ok and H4 quotes-ok=9; `python3 corpus/instruments/source-recheck.py
   --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074` prints
   "S074:sha256 OK" + 9/9 "Q<n> OK occurrences=1 anchor=<line>-ok". Search-log line citations
   (L2,L3,L10,L12-L14,L17,L24-L26,L30-L31,L33,L35-L38) each verified against the snapshot text.
2. README admission block — coverage-map row (line 687) has 3 cells matching the
   `| Area | Entry | Source basis |` header; frontier F29 row (line 691) has 6 cells matching
   `| id | topic | status | entry | sources | next |`, third cell = `admitted`, sources cell =
   S074 only (no double-count); amendment line records 29/29 and
   `grep -cE '^\| F[0-9]+ \|' corpus/README.md` prints 29. Entry's 45 curly quotes each located
   in the snapshot at the cited anchors after whitespace normalization (markdown wrapping).
3. PROVINCE.md line 174 — F29 amendment present with the scope limit verbatim:
   "scope limit: maintainer-side advisory lifecycle only — the reporter flow stays F28, and
   advisory editing, the REST API for repository security advisories and GitHub Advisory
   Database edits stay out".
4. corpus/instruments/knowledge-expected.txt — 66 entries (+1 =
   corpus/knowledge/github-repository-security-advisories.md), exact set match and lexical sort
   against `ls corpus/knowledge/*.md` (scripted diff: missing=[], extra=[], sorted=True).
5. Instruments README / SKILL.md registry rows — all nine round-46 rows present in BOTH files,
   each 8 cells matching the `| name | type | entry command | verdict map | self-test |
   pinned-value path | write scope | owner |` header; the nine rows are byte-identical across the
   two files (md5 compared). Row commands actually run: f29-gate 7/7 exit=0 at HEAD; 1/7 exit=1
   at the base export and 2/7 exit=1 at the freeze export (do-nothing controls discriminate —
   the 7/7 is earned, not do-nothing); f29-gate --selftest exits 2 (argparse), --root <missing>
   prints "f29-gate fixed=0/7 exit=1 (root-missing)" exit=1, both as the rows claim.
6. Live-page closure: the captured page is still live and unchanged — fetched
   2026-10-29 (this review) at 582,877 bytes (== manifest raw bytes), all nine manifest quotes
   Q1-Q9 found verbatim in the live page text.

=====================================================================
DO-NOTHING DISCRIMINATION
=====================================================================
- f29-gate do-nothing controls: base export 1/7 exit=1, freeze tree 2/7 exit=1, HEAD 7/7 exit=0.
  The claimed after-state is not reachable by doing nothing. (Junk/fabricated controls: see
  Finding 4 — the pinned fixture cannot rebuild them at the final tree.)
- R46-counters-selftest-c2.py --do-nothing-control arm: unreachable (import-time crash, Finding 1).
- r46-selftest-f29.py --do-nothing-control arm: exits 1 at the 28-guard before substituting any
  stub counter (Finding 3), so the "29 FAIL lines" claim is unexercised.

=====================================================================
LIMITATIONS / VERIFICATION GAPS
=====================================================================
1. r46-c2-gate.py reads `c2-gate fixed=5/7 exit=1` at HEAD (G1 rows=28->29, G6 knowledge
   65->66, base-intact=0). NOT reported as a defect: counter-errata.md E3 discloses exactly this
   ("At THIS round's tip the v1.3 counter reads 5/7 (G1 28->29, G6 65->66) — moved BY this
   round's C2 landing; the new after-state is graded by r46-f29-gate.py, not by the
   attempt-1 instrument"). The registry row's G1/G6 limb sentences accurately describe the
   frozen instrument.
2. Prose drift (not gate-bearing): claims.json C2 and freeze.txt describe the R50 receipt as
   "9 disclosed", while the receipt's own integration correction makes not-shown=10
   (H6c-size-low added); the receipt's Result line says not-shown=10 and 11 flips + 10 = 21.
   The f29-gate registry row (Finding 5) has the corrected "10 disclosed survivors".
3. The claims' plain command `grep -c 'def case_' corpus/instruments/r46-counters-selftest-c{1,2}.py`
   prints 0/0 — the committed selftests define cases via a CASES table, not `def case_`
   functions; the plain case-count move is not inspectable that way. The authoritative check is
   running the selftests, which currently crash (Findings 1-2).
4. I did not run the full mutbat battery (c1/c2/f29 modes to completion); with both counter
   selftests crashing (Findings 1-2), the battery's grader arm cannot grade mutants, and the
   integration receipt final-battery.txt is truncated before any battery section. The battery's
   --counter f29 mode exists and lists 21 mutants (verified); its grading outcome is left to the
   mutation seats.
5. Live-page check used a raw curl of the public docs page (no credentials, no target testing);
   the page was byte-length-identical to the capture, so the pinned quotes remain current.
