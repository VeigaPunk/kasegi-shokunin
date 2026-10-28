VERDICT: BROKEN

# R46MutC2c — C2 mutation of r46-c2-gate.py, gates G6 (knowledge directory pins) and G7 (census validate)

Attacked: `corpus/instruments/r46-c2-gate.py` (sha256 0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6, matches freeze `c2-gate-sha256`), unmodified. G6 = lines 279-291, G7 = lines 294-297. Real pins (`R46_PINS_OVERRIDE` unset): base-knowledge-names `bf3044…f5d`, base-knowledge-content `f734…e4df`. Verified against the pure base export: `64 bf3044814698b31b2d63a47ef6933cfe4d2d09635c2d717b05c8adf0bf719f5d`; lane `corpus/knowledge/*.md` byte-identical to pure base (cmp loop, no DIFF).

Method: hand tree = copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure` + the lane's counter and `source-recheck.py` (tree's own tool, shas verified) + lane `corpus/source-snapshots/round-46/{S073.txt,manifest.json}` (shas 66c96a…1930 and 01f025…d34) + a fixture F28 entry (3,200-byte placeholder, sizing only) + one F28 row in `corpus/README.md` after F27 + one S073 row (11 cells, tier A, mined, opened 2026-10-28, used-by = entry, anchor = snapshot sha) in `corpus/SOURCES.md` Registry. Each mutant = one `cp -a` of the hand tree + one edit; the recipe asserts `diff -rq` is non-empty. Counter run on each copy with `python3 <copy>/corpus/instruments/r46-c2-gate.py --root <copy>`. `rejected=1` means the targeted gate printed `pass=0`.

## Survivors (defect present, targeted gate still pass=1)

### S1 — G6 does not see non-`.md` files in `corpus/knowledge/`
- Edit: create `corpus/knowledge/scratch-notes.txt` (content `stray non-md file`).
- Output: `gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1`
- `find .../corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → `65`; `ls -A` → `scratch-notes.txt`.
- Cause: counter line 281 `names = sorted(f for f in os.listdir(d) if f.endswith(".md"))` and line 283 `base_like` are both `.md`-filtered, so the directory pin is "the .md set", not "the directory". Spec-literal to the frozen `find -name '*.md'` text, but a 66th file in the knowledge directory passes G6.

### S2 — G6 does not see nested `.md` files
- Edit: create `corpus/knowledge/archive/superseded-note.md` (content `stray nested md`).
- Output: `gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1`
- `find .../corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → `65`; `find .../corpus/knowledge -name '*.md' | wc -l` → `66`.
- Cause: line 281 `os.listdir` is non-recursive, and the directory `archive` fails `endswith(".md")`. Same class as S1: a subtree of knowledge sits outside the pin.

### S3 — G7 passes a mined-but-unused row (warning-only; caught only by G3)
- Edit: S073 `used-by` cell `corpus/knowledge/github-private-vulnerability-reporting.md` → `—`.
- Census output (`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <copy>/corpus/SOURCES.md`): `file	W03	S073 mined but unused` then `file	ok	<copy>/corpus/SOURCES.md`, rc=0.
- Output: `gate G7 pass=1 read=census-rc=0 ok-line=1`
- Same mutant under the full counter: `gate G3 pass=0 read=bad=used-by` (the S073 row's used-by no longer names the entry); `c2-gate fixed=4/7 exit=1`.
- Classification: by design — census `W` codes are warnings (census header lines 31-33, "warnings do not affect clean lanes"; exit line 805). G7 therefore cannot see W01-W04 defects. The defect is still caught in the composite, by G3 only. Recorded so no one reads G7 as covering used-by coverage.

## Killed mutants (target gate pass=0)

| mutant | edit | target read (verbatim) |
|---|---|---|
| g6-base-entry-one-word | `claim-gates.md`: first `the ` → `The ` | `knowledge=65 base-names-intact=0 entry-bytes-ok=1` |
| g6-base-entry-renamed | `mv claim-gates.md claim-gate.md` | `knowledge=65 base-names-intact=0 entry-bytes-ok=1` |
| g7-dangling-used-by | S073 used-by → `corpus/knowledge/github-private-vulnerability-reporting-v2.md` | `census-rc=1 ok-line=0`; census prints `file	E11	S073 missing used-by corpus/knowledge/github-private-vulnerability-reporting-v2.md` |
| g7-duplicate-s073-row | S073 row duplicated verbatim | `census-rc=1 ok-line=0`; census prints `file	E03	S073 duplicate id` and `file	E04	S073 duplicate url … within scope reporter-side private vulnerability reporting` |
| g7-community-kind-at-tier-a | S073 kind `docs` → `community` (tier A) | `census-rc=1 ok-line=0` (E10) |

## Controls (discrimination)

- `control=hand-unmutated G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1 | G7 pass=1 read=census-rc=0 ok-line=1`; counter tail `c2-gate fixed=5/7 exit=1` (G2 and G5 fail on the fixture, as expected; they are not G6/G7).
- `control=pure-base-no-entry G6 pass=0 read=knowledge=64 base-names-intact=1 entry-bytes-ok=0 | G7 pass=1 read=census-rc=0 ok-line=1`; tail `c2-gate fixed=1/7 exit=1` (matches the frozen control `c2 do-nothing`).
- G6 discriminates an absent entry; G7 passes on the do-nothing base, so G7 contributes no discrimination for the F28 claim (consistent with claims.json "only the census limb holds").

## Full run (verbatim, `python3 recipe.py`, exit 0)

```
control=hand-unmutated G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1 | G7 pass=1 read=census-rc=0 ok-line=1
control=hand-unmutated counter-tail: c2-gate fixed=5/7 exit=1
control=pure-base-no-entry G6 pass=0 read=knowledge=64 base-names-intact=1 entry-bytes-ok=0 | G7 pass=1 read=census-rc=0 ok-line=1
control=pure-base counter-tail: c2-gate fixed=1/7 exit=1
SURVIVORS (defect present, target gate still pass=1):
  mutant=g6-nonmd-file-in-knowledge target=G6 ... target-read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
  mutant=g6-nested-md-in-knowledge target=G6 ... target-read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
  mutant=g7-mined-unused-warning target=G7 ... target-read=census-rc=0 ok-line=1
ALL MUTANTS:
mutant=g6-nonmd-file-in-knowledge rejected=0
mutant=g6-nested-md-in-knowledge rejected=0
mutant=g6-base-entry-one-word rejected=1
mutant=g6-base-entry-renamed rejected=1
mutant=g7-dangling-used-by rejected=1
mutant=g7-duplicate-s073-row rejected=1
mutant=g7-mined-unused-warning rejected=0
mutant=g7-community-kind-at-tier-a rejected=1
```

Re-verification run after the batch (commands and output quoted above in S1-S3): `gate G3 pass=0 read=bad=used-by`, `file	W03	S073 mined but unused`, `65` / `66` find counts, `64 bf3044…f5d` pure names pin still intact.

## Limitations

- Census logic itself was not mutated. G7 calls `CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, hard-coded in the counter (line 54), which is a shared fleet file and was not edited. G7 mutants are `corpus/SOURCES.md` edits only.
- The 3,200-byte F28 entry is a fixture for G6 sizing, not the drafted entry; the hand tree is not a deliverable. Only the targeted gates' verdicts are used.
- "rejected" is the targeted gate's `pass=0`; the whole counter exits 1 for every mutant because G2 and G5 grade fixture content.
- Census `TODAY` = `date -u +%F` = 2026-10-28 (no `--today`), so the S073 `opened` value sits at the boundary.
- Not exercised: symlinks in knowledge, dotfiles, uppercase `.MD`, a used-by naming a directory, and Registry-external rows. The predictions from the code (`os.listdir` plus `endswith` on the same `.md` filter; `find -name` case-sensitive) were not run.
- Any fix to G6 changes a frozen counter (claims.json kill rule: limb sentences fixed after scoring; errata only). These findings are for the L1 to decide. No counter edit, git, or shared-file write was made.
- Scratch `/fast/scratch/hyaku/kasegi-r46/R46MutC2c` (recipe, hand tree, mutant copies) removed on exit.
