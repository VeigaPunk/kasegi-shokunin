# R45RevGateG6 — attack on C2 gate G6 (`def g6`, r45-c2-gate.py)

VERDICT: BROKEN

Scope: G6 only, of `corpus/instruments/r45-c2-gate.py`. Frozen base dc5bb8c6e31efc4a6650819df85e79b72fd64bcd. Counter sha256 tested: `5e0796168cfe09f1e7db1b270a4f563cb40516c676d2c5c7921b46cd70730082` (lane working-tree copy; the file is not in the frozen base export, so it was run from a scratch copy).

## Predicate under attack
- Docstring, `r45-c2-gate.py:26`: `G6  find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l == 64.`
- Code, `r45-c2-gate.py:191-194`:
  ```
  def g6(root: str) -> tuple[bool, str]:
      d = os.path.join(root, "corpus/knowledge")
      n = len([f for f in os.listdir(d) if f.endswith(".md") and os.path.isfile(os.path.join(d, f))]) if os.path.isdir(d) else -1
      return n == 64, f"knowledge={n}"
  ```
- G6 counts filenames only. It never reads the content of any file and never checks that the F27 entry exists. The F27 entry is checked by G1 (row F27 plus existing `knowledge/*.md` path), G2 (provenance trio) and G5 (located quotes).

## Finding 1 — cheapest padded tree: G6 pass=1 with the real defect present (BROKEN for G6 as a limb)

Setup (scratch, now removed): `cp -al` of the pure base export, which was verified identical to `git archive dc5bb8c… corpus` (`diff -rq` printed nothing). Base facts:
- `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → `63`
- `grep -c '^| F[0-9]* |' corpus/README.md` → `26` (no F27 row)

Recipe (one command):
```
: > corpus/knowledge/linux-kernel-security-bugs.md
```
A 0-byte file, one inode. The real defect (no F27 row, no entry content, no S071) is untouched.

Printed gate output for the padded tree:
```
gate G1 pass=0 read=rows=26 admitted=26 dup=0
gate G2 pass=0 read=F27-rows=0
gate G3 pass=0 read=row-S071=absent-or-malformed
gate G4 pass=0 read=manifest-absent
gate G5 pass=0 read=F27-rows=0
gate G6 pass=1 read=knowledge=64
gate G7 pass=1 read=census-rc=0
c2-gate fixed=2/7 exit=1
rc=1
```
Do-nothing control (pure base), same counter, printed:
```
gate G6 pass=0 read=knowledge=63
c2-gate fixed=1/7 exit=1
```
Discrimination: the only flipped line between control and padded tree is G6 (63→64). The `diff` of `ls corpus/knowledge` between base and padded tree is exactly `36a37 > linux-kernel-security-bugs.md`. The matching `freeze-controls.txt` line 1 (`do-nothing-base … fixed=1/7`) reproduces on my base run.

Other constructions that also print `gate G6 pass=1 read=knowledge=64` with the F27 row still absent (each run with the same counter, `cp -al` fixtures, all other gates unchanged):
1. zero-byte stub `linux-kernel-security-bugs.md` (V1, cheapest)
2. non-empty, non-entry `index.md` (`# index`)
3. symlink `kernel-security-process.md -> ../README.md`
4. hidden `.kernel-security-process.md` (empty)
5. copy of an existing unrelated entry (`cp ev-model.md kernel-security-process.md`)
6. hardlink `ln corpus/README.md corpus/knowledge/kernel-security-process.md`

Six distinct genuine constructions, all pass=1. The 6-construction list satisfies the "≥5 distinct" threshold for a BROKEN verdict on G6.

Limit on severity: the composite counter stays RED for every one of these (`fixed=2/7 exit=1`) because G1–G5 bind the F27 row, S071 row, snapshot and located quotes. The C2 kill rule (`fixed=7/7` or any control at 7/7) is therefore not tripped by these recipes. G6 is a redundant-looking limb that is trivially satisfiable by padding, and it is not an independent proof of the "one new knowledge entry" claim. Its own name and docstring say "count == 64", so the padded case is a spec-conforming pass for G6 and not a code error inside G6 itself.

## Finding 2 — G6 code diverges from its docstring predicate (verifiability defect)

The docstring literal is `find -maxdepth 1 -name '*.md' | wc -l`. The code uses `os.listdir` + `isfile`, which excludes directories and broken symlinks. Printed outputs (same fixtures; `find` run separately):

- N1: directory `corpus/knowledge/kernel-security-process.md/` added to base →
  `gate G6 pass=0 read=knowledge=63`, `find … | wc -l` → `64`. Literal spec says green; code says red.
- N2: dangling symlink `corpus/knowledge/dangling.md -> /nonexistent` added to base →
  `gate G6 pass=0 read=knowledge=63`, `find … | wc -l` → `64`.
- FR5: correct-count entry + the same dangling symlink →
  `gate G6 pass=1 read=knowledge=64`, `find … | wc -l` → `65`. Literal spec says red; code says green.

So G6 can disagree with its own docstring in both directions. Which one is correct is not decided by the frozen text. The predicate sentence should be fixed to one definition (errata, not a new rule, under the C2 kill rule).

## Finding 3 — can G6 false-RED on a correct landing?

Yes, when a correct landing is count-sensitive. Printed results (fixtures from base; "correct" = base + the F27 entry file):

- C0 (base + one entry file, the frozen "64 total" model): `gate G6 pass=1 read=knowledge=64`, `find` → 64. GREEN, as intended.
- FR1 (entry + extra `index.md` / any second new .md in knowledge): `gate G6 pass=0 read=knowledge=65`. RED.
- FR3 (entry + removal or merge of one existing entry, e.g. `rm ev-model.md`): `gate G6 pass=0 read=knowledge=63`. RED.
- FR4 (entry spelled `linux-kernel-security-bugs.MD`): `gate G6 pass=0 read=knowledge=63`. RED (G1's regex also rejects it, so this is consistent with G1).
- FR2 (entry in subdirectory `knowledge/linux/security-bugs.md`): `gate G6 pass=0 read=knowledge=63`. RED. G1's regex `knowledge/[A-Za-z0-9._-]+\.md` also rejects it, so this is not a G6-only false-RED under the frozen predicate.
- FR6 (entry `linux kernel security bugs.md` with spaces): `gate G6 pass=1 read=knowledge=64`. GREEN for G6, but G1 rejects it by regex (G6 accepts names the rest of the gate refuses).

Format/spelling variants of a correct entry that G6 itself rejects: `.MD`, `.markdown`, subdirectory placement, and any landing that adds a second file or removes/merges one. Variants G6 accepts but G1 rejects: spaces or other characters outside `[A-Za-z0-9._-]`.

## Limitations
- Only the G6 limb was attacked. G1–G5 and G7 were used only to show the composite stays RED for the padded trees. G7 runs `SOURCES_CENSUS` (default `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, a fleet-root script) read-only; nothing was written to it.
- The frozen base does not contain `corpus/instruments/r45-c2-gate.py` nor `corpus/source-snapshots/round-45/`, so the counter was run from a scratch copy of the lane working-tree file (sha above). Results may change if the frozen counter differs from that copy.
- Controls `c2-junk-row` (fixed=4/7) and `c2-fabricated-quote` (fixed=5/7) from `freeze-controls.txt` were not reproduced; their fixtures are not in the repo. I cannot say whether G6 was green in those controls.
- Correct-landing tests used a placeholder content for the entry file; G6 looks only at names, so content does not change the G6 result, but G2/G5 were not exercised on a real entry.
- No git mutation, no commit, no edits to any tracked file. Scratch `/fast/scratch/hyaku/kasegi-r45/R45RevGateG6` removed after the run (verified: `No such file or directory`).

## Recommended repairs for the builders (not applied)
1. G6: either count only entries that G1 would also accept (`knowledge/*.md`, regular file, `[A-Za-z0-9._-]` name), or drop G6 and rely on G1/G2/G5 to bind the F27 entry; then state one predicate in the docstring.
2. Align the docstring and code on dirs and broken symlinks (errata).
3. Add a `freeze-controls` line for the stub-only tree (V1) so the padding is pinned as a graded control.
