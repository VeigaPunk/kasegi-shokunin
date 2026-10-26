# r35-fixtures — broken fixtures for `r35-defect-closure.sh --selftest`

Committed payload trees for the C1 closure suite's `--selftest`
(`corpus/instruments/r35-defect-closure.sh`, round-35 claim C1: the seven round-34 verifier-routed
defects D1–D7 each carry a runnable closure check). One subdir per defect, `D1/` … `D7/`, plus two
non-case controls (`clean/`, `two-defect/D1D2/`).

## Contract

Each tree is a complete minimal root, laid out exactly as the lane root is:

```
SCORECARD.md                                         D1, D2
SKILL.md                                             D3
.ufo/waves/round-34/wave1-results.json               D4 (tracking)
.ufo/waves/round-34/wave1-results.json.provenance.md D4 (provenance; absent in D4/)
.ufo/waves/round-35/claims-erratum-d5.md             D5
.ufo/waves/round-34/wave1/L1Integration.md           D6
corpus/QUALITY.md                                    D7
```

In `D<i>/` limb D<i> is broken and the other six limbs carry fixed content. A check must exit
non-zero on its own fixture and zero on the live lane root. Nothing else in the tree is relevant to
any check; a check that reads a file outside its own limb is out of contract.

| case | broken limb | literal the check reads | fixed in every other tree |
|---|---|---|---|
| `D1/` | `SCORECARD.md` still carries the round-34 placeholder prose; no round-34 tip hash | `filled by the L1` present, `c1c6a5f` absent | correction naming `c1c6a5f`, no placeholder |
| `D2/` | `SCORECARD.md` carries the stale `201.7` row; no appended erratum | `round-34 depth:density row` absent, `201.2` absent | erratum naming the row and `201.2` |
| `D3/` | `SKILL.md` registry has no row for either round-34 instrument | `r-defect-closure` absent, `kill-rule-check` absent | both registry rows present |
| `D4/` | results file not in the index (`.gitignore`) and no provenance note | `git ls-files … \| wc -l` = 0, note absent | results file tracked, provenance note present |
| `D5/` | `claims-erratum-d5.md` keeps §1 and loses the per-id occurrence statement | `discriminating invocation` present, `per-id occurrences` absent | both statements present |
| `D6/` | `L1Integration.md` keeps the stale dead-seat sentence and no correction | `did not file a receipt (dead seat` present, `Correction (round 35)` absent | stale sentence gone, correction appended |
| `D7/` | `corpus/QUALITY.md` keeps the R22/R23 rows with their original grounding and no supersession row | `supersedes R22` absent, `supersedes R23` absent | both supersession rows present |

## How to run the set

The fixtures are *payloads*: the suite copies one tree to scratch before running a check, so a check
never reads the enclosing lane worktree by accident (`git ls-files` resolves the top-level repository
of its cwd, so an in-place run would credit the lane's own index for D4).

```
tmp=$(mktemp -d)
cp -a corpus/instruments/r35-fixtures/D4/. "$tmp"/
( cd "$tmp" && git init -q && git add -A )   # D4: the ignored results file stays untracked
bash corpus/instruments/r35-defect-closure.sh --root "$tmp"     # D4 check -> open=1, exit 1
```

`git add -A` (with or without a commit) is enough: `git ls-files` lists the index, and `D4/.gitignore`
keeps the results path out of it. `clean/` carries no such ignore rule, so the same construction
indexes its results file and the D4 check passes.

Expected outcomes of the whole set (per-case, run against its own tree):

| tree | expected |
|---|---|
| `clean/` | all seven checks pass |
| `D<i>/` | check D<i> fails; the other six pass |
| `two-defect/D1D2/` | exactly D1 and D2 fail |

`two-defect/` is nested one level down so a `D?`/`D[1-7]` glob never picks it up as a case.

## Limits

- **Fixture bytes are pinned, not copied.** Every tree is a line-faithful excerpt of the lane file's
  shapes, not a full-file copy: the live `SCORECARD.md`, `SKILL.md` and `corpus/QUALITY.md` are
  large and move every round, and a fixture that tracked them would rot into a pass. What the
  fixtures prove is that each check *can* change verdict on the bytes it reads; the live tree proves
  the checks pass on the real files.
- **D2's row-bytes clause is an exact-prefix grep, not a diff.** The suite reads the filed row with
  `grep -cE '^\| depth:density \| 9 \| mean \*\*201\.7\*\*, 25 blocks, 710 path-citation instances'`,
  so the fixture carries that row verbatim (pinned from the live `SCORECARD.md` at build time) in
  every tree. No fixture proves the round-34 base bytes are not deleted; that remains a git-diff
  reading on the lane (base commit `014ee2d7`).
- **D4's tracking limb needs the loader's scratch git repo.** In a fixture tree that is not its own
  worktree, `git ls-files` reports the enclosing repository's index; the copy-and-`git init`
  construction above is what makes the limb fixture-local.
- **These files are inside `resolve.py`'s scan.** It walks `SKILL.md` + `corpus/**/*.md`, so the
  fixture markdown enters the lane citation census: measured, the set adds 22 distinct citations and
  1 resolving one (lane total `265/2896` → `266/2918`). Disclosed, not hidden; whether to exclude
  `corpus/instruments/r35-fixtures/` in a future resolver change is a lane decision.
- **The `erratum-file=absent` clause has no fixture.** `fix_re` for D5 is `per-id-occurrences=0`, so
  `D5/` exercises the missing-literal limb, not the missing-file limb; the lane-level absent-file
  direction is the base-tree run. The clause *is* covered by the suite's own scratch mutant (D5
  `-erratum-file`, printed with `cascade=1` because removing the file also zeroes the two
  statements), so this set's gap is the committed fixture only.
