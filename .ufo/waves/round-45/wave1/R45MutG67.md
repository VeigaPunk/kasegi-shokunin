VERDICT: BROKEN

# R45MutG67 — C2 mutation test of counter gates G6 (knowledge count) and G7 (census)

Counter under test (unmodified): `corpus/instruments/r45-c2-gate.py`, sha256
`5e0796168cfe09f1e7db1b270a4f563cb40516c676d2c5c7921b46cd70730082`, identical to
`git show 8cf62c879e6e6b031e67412f8fac1fba0bd378cf:corpus/instruments/r45-c2-gate.py` (sha256 matched).

## Survivors (defect present, target gate G6/G7 still passes)

Target gate `pass=1` while the defect is present. Five of eight mutants survive.

1. **S1 `g6-dir-named-md`** — exact edit: `mkdir corpus/knowledge/zz-r45-probe.md/` (a directory whose name ends in `.md`).
   - Spec G6 (counter line 26): `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` == 64.
   - Run: `find <mut>/corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → `65`.
   - Counter: `gate G6 pass=1 read=knowledge=64`. Whole counter does not reject this (composite gates failed = G5 only, same as the unmutated control).
   - Cause: counter code lines 191-194 use `os.path.isfile(...)`, which excludes directories; `find -name` does not.
2. **S2 `g6-dangling-symlink-md`** — exact edit: `ln -s /nonexistent/r45-probe.md corpus/knowledge/zz-r45-probe-link.md`.
   - Run: `find ... -name '*.md' | wc -l` → `65`; `find ... -printf '%y %p -> %l\n'` → `l .../zz-r45-probe-link.md -> /nonexistent/r45-probe.md`.
   - Counter: `gate G6 pass=1 read=knowledge=64`. Whole counter does not reject this either.
   - Cause: `isfile()` follows symlinks and fails on a dangling link; `find` counts it.
3. **S3 `g7-delete-row`** — exact edit: delete the `| S071 |` line from `corpus/SOURCES.md`.
   - Census run: `bash scripts/sources-census.sh validate --file <mut>/corpus/SOURCES.md` → `file	ok	<mut>/corpus/SOURCES.md`, rc=0.
   - Counter: `gate G7 pass=1 read=census-rc=0`. G7 by design cannot see row presence. The composite counter still rejects via G3 (`composite_gates_failed=G3,G5`).
4. **S4 `g7-indent-4`** — exact edit: prefix the S071 row with four spaces.
   - Census run: rc=0, output `file	ok	...`. The census parser skips lines with 4+ leading spaces (`sources-census.sh` row_pass: `if (line !~ /^ {0,3}\|/) next`).
   - Counter: `gate G7 pass=1 read=census-rc=0`. Composite still rejects via G3 (`composite_gates_failed=G3,G5`).
5. **S5 `g7-used-by-dash`** — exact edit: replace the S071 `used-by` cell with `—`.
   - Census run: `file	W03	S071 mined but unused`, then `file	ok	...`, rc=0. W-codes never change exit status.
   - Counter: `gate G7 pass=1 read=census-rc=0`. Composite still rejects via G3 (`composite_gates_failed=G3,G5`).

S1 and S2 survive the whole counter. S3-S5 survive G7 only and are caught by G3, which is outside this lane's G6/G7 scope.

## Full mutant run (verbatim stdout of `recipe.py`, unmodified counter)

```
hand-tree=/fast/scratch/hyaku/kasegi-r45/R45MutG67/hand
control=control-hand-unmutated composite_exit=1 gates_failed=G5 desc=no edit
   control=control-hand-unmutated G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs-process.md
   control=control-hand-unmutated G2 pass=1 read=source=1 verified-at=1 recheck=1
   control=control-hand-unmutated G3 pass=1 read=row-S071=ok
   control=control-hand-unmutated G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
   control=control-hand-unmutated G5 pass=0 read=spans=0 located=0 failed=0 cores=0/4
   control=control-hand-unmutated G6 pass=1 read=knowledge=64
   control=control-hand-unmutated G7 pass=1 read=census-rc=0
control=control-base-pure composite_exit=1 gates_failed=G1,G2,G3,G4,G5,G6 desc=pure base export, no edit
   control=control-base-pure G1 pass=0 read=rows=26 admitted=26 dup=0
   control=control-base-pure G2 pass=0 read=F27-rows=0
   control=control-base-pure G3 pass=0 read=row-S071=absent-or-malformed
   control=control-base-pure G4 pass=0 read=manifest-absent
   control=control-base-pure G5 pass=0 read=F27-rows=0
   control=control-base-pure G6 pass=0 read=knowledge=63
   control=control-base-pure G7 pass=1 read=census-rc=0
control=control-nested-md composite_exit=1 gates_failed=G5 desc=add corpus/knowledge/zz-sub/x.md (depth 2)
   control=control-nested-md G6 pass=1 read=knowledge=64
   control=control-nested-md G7 pass=1 read=census-rc=0
   (G1-G5 as in control-hand-unmutated)
mutant=g6-delete-md rejected=1 target=G6 target_read=knowledge=63 composite_exit=1 composite_gates_failed=G5,G6
   edit: rm corpus/knowledge/citation-bases.md
mutant=g6-dir-named-md rejected=0 target=G6 target_read=knowledge=64 composite_exit=1 composite_gates_failed=G5
   edit: mkdir corpus/knowledge/zz-r45-probe.md/
mutant=g6-dangling-symlink-md rejected=0 target=G6 target_read=knowledge=64 composite_exit=1 composite_gates_failed=G5
   edit: ln -s /nonexistent/r45-probe.md corpus/knowledge/zz-r45-probe-link.md
mutant=g6-dotfile-md rejected=1 target=G6 target_read=knowledge=65 composite_exit=1 composite_gates_failed=G5,G6
   edit: create corpus/knowledge/.zz-r45-hidden.md
mutant=g7-drop-cell rejected=1 target=G7 target_read=census-rc=1 composite_exit=1 composite_gates_failed=G3,G5,G7
   edit: S071 row: delete cell 8 (teaches) -> 12 fields
mutant=g7-indent-4 rejected=0 target=G7 target_read=census-rc=0 composite_exit=1 composite_gates_failed=G3,G5
   edit: S071 row: prefix 4 spaces
mutant=g7-delete-row rejected=0 target=G7 target_read=census-rc=0 composite_exit=1 composite_gates_failed=G3,G5
   edit: S071 row: delete line
mutant=g7-used-by-dash rejected=0 target=G7 target_read=census-rc=0 composite_exit=1 composite_gates_failed=G3,G5
   edit: S071 row: used-by cell -> —
```

Mutant summary: `mutant=g6-delete-md rejected=1`, `mutant=g6-dir-named-md rejected=0`, `mutant=g6-dangling-symlink-md rejected=0`, `mutant=g6-dotfile-md rejected=1`, `mutant=g7-drop-cell rejected=1`, `mutant=g7-indent-4 rejected=0`, `mutant=g7-delete-row rejected=0`, `mutant=g7-used-by-dash rejected=0`.

(The `control-nested-md` block above is abbreviated; its G1-G5 lines match control-hand-unmutated.)

## Discrimination against do-nothing controls

- Unmutated hand tree: G6 `pass=1 read=knowledge=64`, G7 `pass=1 read=census-rc=0`. The target gates are green where expected, so `rejected=0` on that tree is not an artefact of a always-red counter.
- Pure base export (`/fast/scratch/hyaku/kasegi-r45/L1/pure`, copied, not edited): G6 `pass=0 read=knowledge=63`, so G6 rejects the base. G7 `pass=1 read=census-rc=0`, so G7 does **not** discriminate base from the hand tree.
- The frozen control `control do-nothing-base counter=C2 c2-gate fixed=1/7 exit=1` (`.ufo/waves/round-45/controls/freeze-controls.txt`, line 2) agrees: on base, only G7 is green. That is the same G7-blind-to-F27 result.
- Nested non-defect control `corpus/knowledge/zz-sub/x.md`: G6 stays at 64 under both `find -maxdepth 1` and the counter. Correctly not rejected.

## Findings

- **F1 (G6 divergence from its own spec, BROKEN).** Counter G6 counts `os.path.isfile` entries (lines 191-194) while the spec (line 26) is `find -maxdepth 1 -name '*.md' | wc -l`. Directories and dangling symlinks named `*.md` make find report 65 while the counter reports 64. Survivors S1 and S2 are the whole-counter escapes. Fix (not applied; lane owner's call): count with `os.listdir` and no `isfile` filter, or use `find` directly, and add controls with a `.md` directory and a dangling `.md` symlink to `freeze-controls.txt`.
- **F2 (G7 is a registry-syntax gate only).** Survivors S3-S5 show G7 accepts a registry with the F27 row deleted, indented out of view, or stripped of `used-by`. The composite counter still rejects these via G3, so no composite escape is shown. G7 alone does not verify the F27 source row.
- **F3 (G7 does not discriminate base from target).** Pure base passes G7 (see above). Adding G7 green-on-base to the frozen control list would make the gate's blind spot explicit.

## Limitations

- One hand-built fixture: pure base + `corpus/source-snapshots/round-45` copied from the lane + a fixture knowledge entry `corpus/knowledge/linux-kernel-security-bugs-process.md` + a fixture S071 registry row + a fixture F27 README row. The fixture is not the real F27 entry. The entry body is not evaluated by G6/G7.
- G5 fails on every tree in this run (fixture has no curly-quoted spans). G5 is not in this lane's scope, so `composite_exit` is 1 throughout and `composite_gates_failed` is only informative. Rejection is judged on the target gate line.
- `rejected` = target gate `pass=0`. The composite counter exit was recorded separately.
- Census validation uses the default `--today` (system UTC date, 2026-10-28) via `scripts/sources-census.sh` at the fleet root. Read-only; not modified.
- Eight mutants (4 G6, 4 G7) by design. This is not an exhaustive mutant set; additional G6/G7 edits (e.g. tier/status enum changes, duplicate ids) were not run.
- No commit, push, or git mutation. Scratch `/fast/scratch/hyaku/kasegi-r45/R45MutG67` removed on exit. The counter and the base export were read, not modified.
