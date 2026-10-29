# R46bScribeAdmission — C2 admission drafts (F29 coverage row, frontier row, PROVINCE line, knowledge-expected line)

VERDICT: DRAFT-READY

Scope: draft only. Output is
`.ufo/waves/round-46/attempt2/wave1/R46bScribeAdmission.draft/appends.md`
(6517 bytes, sha256 `ebcacc43eec325fb3679f12bae2957783a9f740478004ee399338b7e73387dbe`),
with the raw command receipts beside it at
`.ufo/waves/round-46/attempt2/wave1/R46bScribeAdmission.draft/receipts.txt`
(4769 bytes, sha256 `259962988b968b5b6557d7ac0127504a7f89a03921895e48b97c024d2888954c`).
Nothing tracked was edited; every application and check ran in a scratch tree under
`/fast/scratch/hyaku/kasegi-r46/R46bScribeAdmission/` (removed on exit). No git/jj command was run
that mutates any repository, index or working tree; only `git archive`, `git log`, `git status` and
`git rev-parse` (read-only) were used.

Frozen base `04af9bc92229232ea5cce8b32bfe59dd969eb26d`; freeze commit
`fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`; lane HEAD at this seat's time `ee03806`.

## What the draft contains

- **Block (a)** — APPEND to END of `corpus/README.md` (the attempt-1 block ends at `corpus/README.md:668`):
  heading `## Round-46 admission (attempt 2) — coverage map row and Frontier F29 (appended 2026-10-29)`,
  an R6 intro paragraph, a 3-cell coverage-map row, the 6-cell frontier row
  `| F29 | … | admitted | corpus/knowledge/github-repository-security-advisories.md | S074 | … |`
  (**status is the third cell**), and the `[r46 attempt-2 amendment, appended 2026-10-29] … **29/29
  admitted** …` count line carrying the per-round frontier history.
- **Block (b)** — APPEND to END of `PROVINCE.md` (the attempt-1 F28 line is `PROVINCE.md:171`): one
  `[r46 Frontier amendment, appended 2026-10-29, end-of-file append per R6] F29 — …` line with the
  scope limit "maintainer-side advisory lifecycle only — the reporter flow stays F28, and advisory
  editing, the REST API for repository security advisories and GitHub Advisory Database edits stay out".
- **Block (c)** — ONE line for `corpus/instruments/knowledge-expected.txt`:
  `corpus/knowledge/github-repository-security-advisories.md`, at sorted position (index 29 of 66),
  immediately after `corpus/knowledge/github-private-vulnerability-reporting.md`.

Every drafted claim in (a) and (b) is a located quote in the frozen capture
`corpus/source-snapshots/round-46-a2/S074.txt` (sha256
`1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, 42 lines): draft advisory
(L12), temporary private fork (L13), publish after a patch (L14), credit (L17), GitHub-as-CNA (L24),
CVE request / 72-hour review / stays private (L25), other-CNA boundary (L26), publication visibility
(L31), URL does not change (L33), fix-version duty (L38).

## Findings (every command below was run by me; output quoted)

### F1 — Scratch tree built from the frozen base by export, then the three blocks applied

Command: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive HEAD corpus PROVINCE.md | tar -x -C $S/tree`
(HEAD `ee03806` = freeze + wave-spec commit). The three paths this seat touches are byte-identical
between the frozen base `04af9bc9` and HEAD — `git diff --quiet 04af9bc92229232ea5cce8b32bfe59dd969eb26d..HEAD -- <path>`
prints `UNCHANGED base..HEAD` for `corpus/README.md`, `PROVINCE.md` and
`corpus/instruments/knowledge-expected.txt`; the only corpus changes base→HEAD are the four
round-46-attempt-2 additions (`git diff --name-only 04af9bc9..HEAD -- corpus PROVINCE.md` →
`corpus/instruments/r46-f29-gate.py`, `corpus/instruments/r46-mutbat.py`,
`corpus/source-snapshots/round-46-a2/S074.txt`, `corpus/source-snapshots/round-46-a2/manifest.json`),
so the export is the frozen corpus plus the freeze commit's own artefacts).
Then block (a) appended to `corpus/README.md`, block (b) appended to `PROVINCE.md`, block (c) inserted
at sorted position in `corpus/instruments/knowledge-expected.txt`.

Pure-addition check (unified diff of the pristine export vs the treated tree):
```
corpus/README.md removed-lines: 0 added-lines: 24
PROVINCE.md removed-lines: 0 added-lines: 2
knowledge-expected diff: ['+corpus/knowledge/github-repository-security-advisories.md']
```
No existing line was rewritten (R6). Byte hygiene of the draft file: 0 tabs, 0 CR, 0 trailing-space
lines, final newline present; block (a) 3562 bytes / 24 lines, block (b) 747 bytes / 2 lines
(leading blank + the one amendment line), block (c) 58 bytes / 1 line.

### F2 — REQUIRED CHECK: frontier counter on the scratch tree with the F29 row reads 29/29

Command: `python3 corpus/instruments/r44-frontier-count.py --root <scratch-with-F29-row> --expect 29 --ids`
Output:
```
frontier-ids=F01,F02,F03,F04,F05,F06,F07,F08,F09,F10,F11,F12,F13,F14,F15,F16,F17,F18,F19,F20,F21,F22,F23,F24,F25,F26,F27,F28,F29
frontier rows=29 admitted=29
```
rc=0. The frozen plain grep moves with it: `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → `28` on
the live lane, `29` on the treated tree.

### F3 — Do-nothing control: the same counter with the F29 row removed cannot reach 29

Same tree, block (a) stripped back off `corpus/README.md`:
```
frontier rows=28 admitted=28
frontier expected=29 admitted=28 verdict=SHORT exit=1
```
rc=1. The target is not reachable without a real F29 row, so F2 is not a vacuous pass.

### F4 — The F29 admission gate goes from 2/7 to 7/7 when the row is present

Command: `python3 corpus/instruments/r46-f29-gate.py --root <tree>` (the frozen, unedited gate;
scratch tree = HEAD export + block (a) + block (c) + a sibling's F29 entry draft as the entry file +
a sibling registry drafter's S074 `SOURCES.md` row).

Control (no F29 row, no entry):
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
Treated:
```
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=10 xrefs=6/6 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=28 located=28 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```
H1 (`rows=29 admitted=29 F29=admitted`) is the limb this seat's block (a) moves; H3/H6 and the
entry bytes come from sibling seats' drafts (registry row, entry file), which this seat does not own.

### F5 — Shape checks on the drafted block (a)

- The coverage-map row has 3 cells, the frontier row 6 cells, and **no cell in either row contains a
  `|`**: `ROW: GitHub cells= 3 | any cell contains '|': False`, `ROW: F29 cells= 6 | any cell
  contains '|': False`.
- Status is the **third** cell (`admitted`), the entry cell names
  `corpus/knowledge/github-repository-security-advisories.md`, the sources cell names `S074` — the
  shape the gate's H1 (`f29[0][2] == "admitted"`, `ENTRY in f29[0][3]`, `re.search(r"\bS074\b",
  f29[0][4])`) reads.
- The heading appears exactly once in the treated README
  (`heading count in README: 1`), the count line exactly once, the README ends in `\n`, and the
  file is free of trailing-space lines in the appended region.
- `grep -cE '^\| F[0-9]+ \|' corpus/README.md` = `29` on the treated tree; the F29 row is the only
  new frontier row.

### F6 — (d) What `recheck-audit.py` and `frontier-recheck-count.py` expect AFTER the entry lands

Current live-lane values, quoted (run against the lane root, before any of this round's entries land):

`python3 corpus/instruments/recheck-audit.py` (live lane, rc=0):
```
strict pass=65/65 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=43 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=65 missing=0 unexpected=0 exit=0
```

`python3 corpus/instruments/frontier-recheck-count.py --root .` (live lane, rc=0):
```
FRONTIER-CENSUS rows=28 admitted=28 closed=28 problem-rows=0 registry=73
entries=31 pass=31 exit=0
```

**Expected after-values once the F29 entry lands and this draft's blocks (a)/(b)/(c) are applied**
(measured on the treated tree: HEAD export + block (a) + block (b) + block (c) + the entry file + the
S074 registry row):

`recheck-audit.py --root <treated> --cdroot <lane>` (rc=0):
```
strict pass=66/66 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=44 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=66 total=66 pass=66 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=66 missing=0 unexpected=0 exit=0
```
i.e. `expected=66 missing=0 unexpected=0 exit=0` (the set-equality limb: 65 → 66 entries, exit 0),
`lines=66 total=66 pass=66`, `strict pass=66/66`.

`frontier-recheck-count.py --root <treated>` (rc=0):
```
FRONTIER-CENSUS rows=29 admitted=29 closed=29 problem-rows=0 registry=74
FRONTIER-PASS F29 ids=S074
PASS     F29  corpus/knowledge/github-repository-security-advisories.md ids=S074           exit=0
entries=32 pass=32 exit=0
```
i.e. `rows=29 admitted=29 closed=29 registry=74` (73 → 74 with the S074 registry row),
`entries=32 pass=32 exit=0` (31 → 32: one new entry record).

Intermediate state check (block (a) applied, registry row still absent): the census goes red on the
row, not on the row's shape:
```
FRONTIER-CENSUS rows=29 admitted=29 closed=28 problem-rows=1 registry=73
FRONTIER-FAIL F29 status=admitted ids=S074 problems=source-id-absent:S074
PASS     F29  corpus/knowledge/github-repository-security-advisories.md ids=S074           exit=0
entries=32 pass=32 exit=1
```

### F7 — (d) Control: block (c) is load-bearing, not decorative

Treated tree with block (c) reverted (entry present, expected-list not updated):
```
strict pass=66/66 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=66 total=66 pass=66 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=65 missing=0 unexpected=1 exit=1
```
rc=1. Without block (c) the audit goes red with `unexpected=1`; with it, `expected=66 missing=0
unexpected=0 exit=0` (F6).

### F8 — Absence sweep and registry counts move as the claim states

Command (each tree): `grep -rliE 'repository securit. advisor|GHSA' corpus/knowledge
corpus/SOURCES.md corpus/README.md | wc -l`
```
LIVE    | absence-sweep files: 2 | SOURCES rows: 73 | knowledge md: 65 | frontier rows: 28
TREATED | absence-sweep files: 4 | SOURCES rows: 74 | knowledge md: 66 | frontier rows: 29
```
The two live-lane hits are `corpus/knowledge/github-private-vulnerability-reporting.md` (the F28
entry's scope-out note) and `corpus/SOURCES.md` (the S068 rejected-database row's search-log
context). The treated tree's 4 are those two plus `corpus/README.md` (the new F29 block) and the
new `corpus/knowledge/github-repository-security-advisories.md`. SOURCES 73 → 74, knowledge entries
65 → 66, frontier rows 28 → 29 — the frozen C2 `plain` lines, each re-measured.

### F9 — `knowledge-expected.txt` insertion point

`corpus/knowledge/github-private-vulnerability-reporting.md` is file line 29 and
`corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` is file line 30; the new line
sorts between them (`corpus/knowledge/github-repository-security-advisories.md`), and the inserted
file passes `grep -v '^#' … | sort -c` (`SORT_C_OK`, and `LC_ALL=C sort -c` rc=0). Note: the file's
existing order is *locale* sort, not byte sort (`evidence-dir.md` precedes `ev-model.md` under
`sort -c` but not under Python's `sorted()`); the insertion preserves the file's own convention.

## Deviations from the spec (deliberate; the L1 may flip any of them)

1. The count line carries the full per-round frontier history ("F01-F08 at round 23, … F29 at round
   46 (attempt 2)") rather than the attempt-1 block's shorter "F01-F27 as previously recorded and
   F28 admitted this round", because the task text asks the count line to name "the per-round
   frontier history". Rounds 27, 32 and 43 admitted no frontier row and are named as such, matching
   the attempt-1 history line (`F01-F08 at round 23, F09 at round 24, … F25 at round 42`).
2. Block (b)'s scope-limit wording differs from the attempt-1 F28 line's wording (which said
   "the GHSA database and CVE assignment stay out"); F29's exclusion set is the one the task text
   named (advisory editing, REST API, Advisory-Database edits) plus the F28 contrast. The F28 line
   itself is untouched.
3. Block (c) is inserted at sorted position, not appended after the file's trailing `#` comment
   lines — the file declares itself a sorted list, and rounds 45 and 46-attempt-1 both inserted at
   sorted position.
4. The coverage-map row names the attempt explicitly ("(round 46 attempt 2)") because the
   attempt-1 block already carries a "(round 46)" coverage-map row; the two rows are distinguishable
   in the map.

## Limitations

- **The F29 knowledge entry and the S074 `SOURCES.md` row do not exist in the live lane** — they are
  other seats' drafts (`R46bScribeEntryA/B/C/D/E/F`, `R46bScribeRowsA/B/C`). For F4 and F6 I used a
  sibling's *draft* entry file and a sibling's *draft* registry row in the scratch tree; those
  artefacts are not this seat's work and their content is not re-verified here beyond what the
  frozen gate measured. If the L1 lands a different entry or registry row, F2 (the required check)
  is unaffected — it depends only on this seat's README row — but F4's H2/H3/H5/H6 and F6's
  per-entry numbers would need re-running.
- The gate's H1 was exercised on a scratch tree whose entry file is a sibling draft; H1 reads only
  the README row and the presence of the entry path, so it is the row, not the entry bytes, that
  H1 confirms.
- `recheck-audit.py` on the scratch tree needs `--cdroot <lane>` because the entry's `recheck:`
  line `cd`s to the lane path; without it the `cdroot` strict limb reports failures that are an
  artefact of auditing a copy, not of the entry (F6 passes with `--cdroot`).
- `sources-census.sh` (gate limb H7) lives at the fleet root, outside the lane; it was run read-only
  by the gate.
- No non-author reading of the drafted row/province wording was done; the "maintainer-side only"
  scope claim rests on the located S074 quotes and on the F28/F07 contrast, both quoted above.
- `r44-frontier-count.py` does not check that the entry file exists (F4's gate H1 does).
- Tools installed or upgraded: none (nothing was needed; the work is drafting plus running the
  lane's own stdlib-only Python instruments). No pacman transaction was attempted.
- Scratch `/fast/scratch/hyaku/kasegi-r46/R46bScribeAdmission/` was removed on exit; the only files
  this seat wrote in the lane are the draft directory and this report.
