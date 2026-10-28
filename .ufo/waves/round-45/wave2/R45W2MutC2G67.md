VERDICT: BROKEN

Scope: C2 counter `corpus/instruments/r45-c2-gate.py` v1.1, gates G6 (knowledge-dir count) and G7 (`sources-census.sh validate` green), on the export of lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (`git archive ... | tar -x`, scratch copy; counter bytes not modified). Mutants applied only to scratch copies. Scratch removed on exit. No git mutation, no fleet file touched.

Baseline: the unmodified export is green.
```
$ python3 corpus/instruments/r45-c2-gate.py --root .
gate G6 pass=1 read=knowledge=64 base-names-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=7/7 exit=0
```

## Survivors (defect present, counter exit 0)

Each mutant was run through the counter as `python3 corpus/instruments/r45-c2-gate.py --root <copy>`. Recipe output is quoted verbatim below.

S1. G6 — base knowledge file hollowed to 0 bytes (name kept). Edit: `: > corpus/knowledge/claim-package-gate.md`.
```
mutant=g6-hollow-base rejected=0 target=G6 target_pass=1 counter=[c2-gate fixed=7/7 exit=0] changed=['corpus/knowledge/claim-package-gate.md']
```
Evidence of defect present: `stat -c %s` = 0; depth-1 count still 64. Why it survives: `r45-c2-gate.py:264` reads names only (`os.listdir`), `:266-267` hash names only (`PINS["base-knowledge-names"]`); no byte or size check on the 63 base files. A stub counted toward the 64 is exactly the padding the G6 gate exists to stop.

S2. G6 — F27 entry bulked with 3200 blank lines to clear the size floor. Edit: append `"\n"*3200` to `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md`.
```
mutant=g6-entry-blank-pad rejected=0 target=G6 target_pass=1 counter=[c2-gate fixed=7/7 exit=0] changed=['corpus/knowledge/linux-kernel-security-bugs-reporting-process.md']
```
Evidence: size 10707 -> 13907 bytes; non-blank line count `grep -c '[^[:space:]]'` unchanged at 43. Why it survives: `r45-c2-gate.py:268` (`getsize >= 3000`) is satisfiable by whitespace; the other gates read only the first 8 lines, section headings, table rows and curly spans, so no gate notices the bulk.

S3. G6 — extra `.md` placed one level below knowledge/. Edit: `mkdir corpus/knowledge/_pad && printf '# pad\n' > corpus/knowledge/_pad/pad.md`.
```
mutant=g6-subdir-md rejected=0 target=G6 target_pass=1 counter=[c2-gate fixed=7/7 exit=0] changed=['corpus/knowledge/_pad/pad.md (new)']
```
Evidence: `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` = 64; `find corpus/knowledge -name '*.md' | wc -l` = 65. Why it survives: `:264` is non-recursive. The counter's own docstring (`r45-c2-gate.py:34-36`) claims "the knowledge dir must equal the 63 base names plus exactly the F27 entry", which this mutant falsifies while every gate stays green. Either the docstring overclaims or the gate needs a recursive check.

S4. G7 — `used-by` of a REJECTED row points at a missing file. Edit: S022 used-by `—` -> `corpus/knowledge/no-such-note.md`.
```
mutant=g7-dangling-usedby-rejected rejected=0 target=G7 target_pass=1 counter=[c2-gate fixed=7/7 exit=0] changed=['corpus/SOURCES.md']
  census rc=0 out=... | file	ok	.../corpus/SOURCES.md
```
Why it survives: `sources-census.sh:559` is `[ "$status" = mined ] || continue`, which runs before the E11 existence check at `:566`. So E11 is only ever evaluated for mined rows, although the census header (`sources-census.sh:29`) documents "E11 used-by path missing on disk" with no status condition. Discriminator (same dangling path on a MINED row, S064):
```
mutant=control-dangling-usedby-mined rejected=1 target=G7 target_pass=0 counter=[c2-gate fixed=6/7 exit=1] ...
  census rc=1 out=... | file	E11	S064 missing used-by corpus/knowledge/no-such-note.md
```
So the E11 blind spot is status-dependent, not an absent check.

S5. G7 — bogus recheck cell accepted as a "symbolic cadence". Edit: S064 recheck `on-release` -> `whenever`.
```
mutant=g7-recheck-bogus-word rejected=0 target=G7 target_pass=1 counter=[c2-gate fixed=7/7 exit=0] changed=['corpus/SOURCES.md']
  census rc=0 out=... | file	ok	.../corpus/SOURCES.md
```
Why it survives: `sources-census.sh:582` `symbolic()` is `^[A-Za-z][A-Za-z0-9 _-]*$`, so any alphabetic word passes E09 (`:665`). Consequence, from `:676` and `:682`: the overdue mode treats any such word as a cadence and never judges it, so a typo'd recheck never comes due. The census's E09 text (`:28`) promises "invalid recheck" detection.

S6. G7 — registry row hidden from validation by a 4-space indent. Edit: prefix S064 row with 4 spaces.
```
mutant=g7-row-indent-hidden rejected=0 target=G7 target_pass=1 counter=[c2-gate fixed=7/7 exit=0] changed=['corpus/SOURCES.md']
  census rc=0 out=... | file	ok	.../corpus/SOURCES.md
```
Why it survives: the census documents that "4 or more spaces are indented code and ignored" (`sources-census.sh:40-41`), so the row is never validated (no E-codes emitted for S064 at all). This is a documented census choice, but the counter does not detect a registry row disappearing from validation (its S-row count is not checked against the table). Classify as a coverage gap, not a census bug.

## Caught (control: counter goes red for the intended gate)

C1. `g6-junk-file`: new `corpus/knowledge/zz-padding.md`
```
mutant=g6-junk-file rejected=1 target=G6 target_pass=0 counter=[c2-gate fixed=6/7 exit=1] changed=['corpus/knowledge/zz-padding.md (new)']
  per-gate pass: G1=1 G2=1 G3=1 G4=1 G5=1 G6=0 G7=1 failing=['G6']
```
C2. `g7-row-cell-dropped`: S064 loses its used-by cell (NF=12)
```
mutant=g7-row-cell-dropped rejected=1 target=G7 target_pass=0 counter=[c2-gate fixed=6/7 exit=1] changed=['corpus/SOURCES.md']
  per-gate pass: G1=1 G2=1 G3=1 G4=1 G5=1 G6=1 G7=0 failing=['G7']
  census rc=1 out=... | file	E01	S064 fields=10
```
Do-nothing control:
```
mutant=control-do-nothing rejected=0 target=- target_pass=- counter=[c2-gate fixed=7/7 exit=0] changed=[]
```
So the harness discriminates: a real count/row break goes red on the targeted gate only; every survivor above is a defect the targeted gate is documented to stand for, not an artefact of the harness.

## Limitations
- Mutants are scratch copies of the lane export only; the counter was run with `--root <copy>`. The S071 pins (`r45-c2-gate.py:58-62`) make byte-forged captures moot, which is why the survivors target the uncovered surface (base-file content, entry bulk, subtree, census semantics).
- G7 calls a fleet-root script, `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"` (`r45-c2-gate.py:56`), outside the export. `PINS` (`:58-62`) does not pin it, so G7's verdict depends on unpinned host bytes (35466 bytes, mtime Oct 19 at run time). I read it but did not mutate it (shared fleet file). The census-level survivors S4-S6 are therefore findings about that host script as used by G7.
- Census invoked without `--today`; opened-date checks used the census default (not separately probed).
- Recipe is one edit per mutant (one line/cell, or one added/appended file). Not exhaustive: other census blind spots (e.g. `### ` subheadings not ending the Registry section, `supersedes S###` exemption in E04 unverified against its target) were read but not mutated.
- Each survivor was run once; results are deterministic over the same bytes, so one run per mutant suffices.

## Tooling
None installed or upgraded. Scratch `$HYAKU_SCRATCH/kasegi-r45/R45W2MutC2G67/` removed on exit.
