# R46ScribeAdmission — C2 admission drafts (F28 coverage row, frontier row, PROVINCE line, knowledge-expected line)

VERDICT: DRAFT-READY

Scope: draft only. Output is `.ufo/waves/round-46/wave1/R46ScribeAdmission.draft/appends.md` (4667 bytes, sha256 `036b8777bd799ef4d46a010f9dbab2c25e099390af647f5b5080eb53ec9d0662`). Nothing tracked was edited; all application and checks ran in a scratch tree under `/fast/scratch/hyaku/kasegi-r46/R46ScribeAdmission/` (removed on exit). The frozen base is `914ca0b6956f01d87b2e252ffad06fe74ec5d9ba`; the freeze commit is `9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5`.

## What the drafts contain

- Block (a), for END of `corpus/README.md`: a `## Round-46 admission - coverage map row and Frontier F28 (appended 2026-10-28)` heading, an intro paragraph, a three-column coverage-map row, a six-column frontier row `| F28 | … | admitted | corpus/knowledge/github-private-vulnerability-reporting.md | S073 | … |` with status as the third cell, and the `[r46 amendment, appended 2026-10-28] … **28/28 admitted** …` count line.
- Block (b), for END of `PROVINCE.md`: one `[r46 Frontier amendment, appended 2026-10-28] F28 — …` line, scope limit "reporter flow only — maintainer handling, the GHSA database and CVE assignment stay out".
- Block (c), for `corpus/instruments/knowledge-expected.txt`: the single line `corpus/knowledge/github-private-vulnerability-reporting.md`, inserted at sorted position (see deviation 3).

## Findings (each command was run by me; output quoted)

### F1 — Do-nothing control: frontier counter at the base export reads 27, not 28
Command: `python3 corpus/instruments/r44-frontier-count.py --root <base-export> --expect 28` (base export = `git archive 914ca0b… corpus/instruments corpus/knowledge corpus/README.md corpus/SOURCES.md corpus/source-snapshots PROVINCE.md`, unmodified)
Output:
```
frontier rows=27 admitted=27
frontier expected=28 admitted=27 verdict=SHORT exit=1
```
rc=1. The control cannot reach the target without a real F28 row.

### F2 — Treated tree: counter reads 28/28
Scratch tree = copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure` plus the base `corpus/instruments/` (the pure export lacks `r44-frontier-count.py`, `r46-c2-gate.py` and others; I copied them from the base archive, which is the instrument the task named), then block (a) appended to README.
Command: `python3 corpus/instruments/r44-frontier-count.py --root <treated> --expect 28`
Output: `frontier rows=28 admitted=28` rc=0.

### F3 — Frozen plain grep lines (claims.json C2 `plain`)
Command: `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → base `27`, treated `28`.
Command: `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md` → base `0`, treated `0`.
The second (frozen admitted-regex) reads 0 in both states, as the round-44 counter note recorded; it is not a usable measurement. The first moves 27→28 as the claim's `plain` line states.

### F4 — Mutants of the F28 row (scratch copies; each graded by the frozen-shape counter and by r46-c2-gate G1)
- M0 treated: counter `frontier rows=28 admitted=28` rc=0; G1 `(True, 'rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md')`.
- M1 status `queued`: counter `frontier expected=28 admitted=27 verdict=SHORT exit=1`; G1 `(False, 'rows=28 admitted=27 dup=0')`.
- M2 `admitted` moved into the second cell: counter SHORT (admitted=27); G1 `(False, 'rows=28 admitted=27 dup=0')`. Confirms the third-cell rule is what counts.
- M3 F28 row deleted: counter SHORT; G1 `(False, 'rows=27 admitted=27 dup=0')`.
- M4 entry cell names a missing file (`corpus/knowledge/no-such-entry.md`): counter still `rows=28 admitted=28` (the counter does not check the file); G1 `(False, 'F28-entry-not-a-regular-file')`. The file check is G1's, not the counter's.
- M5 do-nothing (base README): counter SHORT; G1 `(False, 'rows=27 admitted=27 dup=0')`.

### F5 — r46-c2-gate.py on the treated tree (frozen gate, unedited; from freeze commit 9f23aab)
Command: `python3 corpus/instruments/r46-c2-gate.py --root <treated>`
Output:
```
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
gate G2 pass=0 read=source=0 verified-at=0 recheck=0 sections=0/4 table-rows=-2 xrefs=0/0
gate G3 pass=0 read=row-S073=absent-or-malformed
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=0 read=spans=0 located=0 failed=0 uncited=0 cores=0/5
gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=4/7 exit=1
```
G2, G3 and G5 fail here only because the F28 entry and the S073 SOURCES row are not in my scope and I used a scratch placeholder for the entry file (3776 bytes, no provenance lines). They are not satisfied by the drafts in this file and must be verified against the real entry/registry drafts. G1, G4, G6, G7 are the parts this seat's drafts can move; G1 and G6 pass on the treated tree.

### F6 — Knowledge-expected line (block c) and recheck-audit set equality
Applied at file line 29 (between `corpus/knowledge/ev-model.md` at line 28 and `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` at line 29). Check: 65 entry lines, `sorted-ok: True`, github entry at index 29.
Command: `python3 corpus/instruments/recheck-audit.py` in the treated scratch tree (with the scratch placeholder entry). Output lines:
```
strict pass=1/65 cdroot_fail=63 instrument_fail=0 own_fail=0
executes=40 gated=24 broken=0  (…)
lines=64 total=65 pass=64 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=65 missing=0 unexpected=0 exit=1
```
The set-equality limb passes (`expected=65 missing=0 unexpected=0`), and `executes=40 gated=24 broken=0` is unchanged from base. The red exit comes from the placeholder entry having no `recheck:` line (total=65, pass=64) and the strict `cdroot` limb is pinned to the lane path, so a scratch run reports `cdroot_fail=63`. Against the real lane root at HEAD (before F28) the same instrument printed `strict pass=64/64 cdroot_fail=0` and `expected=64 missing=0 unexpected=0 exit=0`.

### F7 — Shape against the Round-45 block
Command: line-kind comparison of `corpus/README.md` from `## Round-45 admission` onward versus the treated `## Round-46 admission` onward. Both contain: h2 heading, intro paragraph, coverage-map table (`| Area`/separator/row), blank, frontier table (`| id`/separator/row), blank, tag-line. Result: `shape-equal: False` only because the R45 intro is wrapped over 8 physical lines and my intro is 2 physical lines; the block structure is the same. The README ends in `\n`; a blank line precedes the R46 heading (`blank before R46 heading: True`).

### F8 — Frontier row and coverage-map row content checked against the frozen snapshot
Read `corpus/source-snapshots/round-46/S073.txt` (sha256 `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930`, matching the claims pin). The drafted claims are each backed by a located line, verified by `grep -n` on the snapshot: `S073.txt:560` ("Anyone can privately report a security vulnerability to repository maintainers."), `:561` (enablement by owners of public repositories), `:564` ("You can only report vulnerabilities privately for repositories where this feature is enabled." and the SECURITY.md separation), `:573` (default required fields), `:574` (optional AI-assistance disclosure), `:577` (automatic reporter collaborator and credit), `:578` (only the repository maintainer can merge from the temporary private fork). The G4 run above printed `quotes-ok=8`.

## Deviations from the spec (taken deliberately; L1 may flip any of them)

1. Heading uses a plain hyphen, `Round-46 admission - coverage map row …`, as the spec literally wrote; the Round-45 heading uses an em dash. The Round-46 heading therefore differs in one character from R45.
2. Coverage-map and frontier cells use the `corpus/knowledge/…` prefix that the Round-45 block uses, not the bare `knowledge/…` shown in the spec snippet. G1 accepts both (its regex matches the substring).
3. Block (c) is inserted at sorted position (line 29), not appended after the file's end. The file's last two lines are the `#` header comments; round 45 (commit 6662a42, `@@ -34,6 +34,7 @@`) inserted at sorted position too. Appending after the comments would break the sorted-list convention the header states.
4. The PROVINCE tag is the spec's literal `[r46 Frontier amendment, appended 2026-10-28]`; the Round-45 tag additionally says `, end-of-file append per R6`. I did not add that suffix.

## Limitations

- The F28 knowledge entry does not exist in this lane tree or in any wave1 draft I could read; I did not write it (other seats own entry and registry drafts). The scratch placeholder is only for the file-existence, size and name checks.
- G2, G3 and G5 are unverified by these drafts (see F5). The `recheck-audit` pass on the treated tree is structural only (set equality); per-entry recheck correctness for F28 is not shown.
- No non-author reading of the drafted F28 row/PROVINCE line text was done; the claim "reporter flow only" is supported by the S073 quotes above but the row's wording was not graded by a second reader.
- `r44-frontier-count.py` does not check that the entry file exists (M4); that check is in `r46-c2-gate.py` G1 only.
- `sources-census.sh` (G7) lives at `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, outside the lane; I ran it read-only through the gate.
- Git use was read-only (`git archive`, `ls-tree`, `status`). `git status` on the lane at the end shows no tracked change from this seat; the only file I created in the lane is the draft directory `R46ScribeAdmission.draft/appends.md` and this report.
- Installed tools: none. Scratch: `/fast/scratch/hyaku/kasegi-r46/R46ScribeAdmission/` removed on exit.
