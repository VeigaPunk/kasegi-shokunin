VERDICT: BROKEN

# R46W2RevLanding: falsification of `corpus/instruments/r46-landing-gate.py`

Target: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-landing-gate.py` (637 lines, read end to end: lines 1-637). `git status --porcelain` of the lane shows no modification to the gate file. Lane HEAD at review time: `0d121a2`; the integrated tree commit `5437afe` is the one the wave-2 spec references. Round-45 pair: fleet report commit `a1f7761b572e8c78d9d3b64d5d1e6a655f152a11` (`.ufo/reports/round-45/kasegi.md`, author 19:30:06, committer 19:37:42) and lane tip `2998baab4c39e6f0c1b50b150c5965e1643c4e11` (committer 19:36:31, author 19:36:30). The fleet working copy of the round-45 report equals HEAD (`git diff --quiet HEAD -- .ufo/reports/round-45/kasegi.md` succeeded).

## 1. Selftest (pass)

Command: `TMPDIR=/fast/scratch/hyaku/kasegi-r46/R46W2RevLanding python3 .../r46-landing-gate.py --selftest --work /fast/scratch/hyaku/kasegi-r46/R46W2RevLanding/st`
Last line printed: `selftest cases=30 failures=0`; shell exit 0.

## 2. Red-before replay on the real round-45 pair (gate catches the defect)

Command: `python3 .../r46-landing-gate.py --post-report --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --branch master --report .ufo/reports/round-45/kasegi.md --fleet /home/vgpnk/Projects/shokunin --tip 2998baab4c39e6f0c1b50b150c5965e1643c4e11`

Output (verbatim):
```
check report-readable pass=1 read=bytes=15428
check cited-hashes pass=1 read=n=6,final=1
check resolves pass=1 read=unresolved=0
check ancestor pass=1 read=non-ancestor=0
check final-is-tip pass=1 read=final-not-tip=0,tip=2998baab4c39(override)
check date-order pass=1 read=latest-cited=2998baab4c39@2026-10-28T19:36:31-03:00,report-commit-committer=2026-10-28T19:37:42-03:00
check date-order-author pass=0 read=latest-cited=2998baab4c39@2026-10-28T19:36:31-03:00,report-commit-author=2026-10-28T19:30:06-03:00
check shonen-heading pass=1 read=count=1
landing-gate mode=post-report checks=8 fail=1 exit=1
```
Shell exit 1. The defect is caught only by `date-order-author`; `date-order` (committer clock, moved to 19:37:42 by the rewrite) passes, which is why the author clock is the one that matters.

Limitation of this replay: `--tip` substitutes for the live `ls-remote` read, so it replays the final-is-tip check against the lane tip as of now, which is the round-45 tip.

## 3. Constructions that the gate catches (HOLDS for these)

Each fixture: `D=$(mktemp -d -p $S)`, `git init` for origin (bare), lane and fleet; every git call `-C` the fixture with a toplevel assertion. Driver: `$S/exp.sh` (scratch, deleted on exit).

- X1 control, final names non-tip C1: `check final-is-tip pass=0 read=final-not-tip=731b7b8929dc,tip=025524fad70e(ls-remote)`, exit 1.
- X2 rebased lane commit (lane tip amended, force-pushed; report cites the pre-rebase hash): `check ancestor pass=0 read=non-ancestor=025524fad70e`, `check final-is-tip pass=0 read=final-not-tip=025524fad70e,tip=6764cb10aedb(ls-remote)`, `fail=2 exit=1`. HOLDS.
- X3 amended report commit, text rewritten to a later hash, author kept (`commit --amend --no-edit`): `check date-order-author pass=0 read=latest-cited=db0cb71a1d97@2023-11-14T22:18:20Z,report-commit-author=2023-11-14T22:16:40Z`, exit 1. HOLDS.
- X5c control (word `final` in the hash cell of a table row): `check final-is-tip pass=0 read=final-not-tip=731b7b8929dc,...`, exit 1.
- X6c control (non-ancestor hash in a leading-pipe `| Commit |` table): `check ancestor pass=0 read=non-ancestor=654a6d069504ad...`, exit 1.
- X7c control (full non-ancestor hash in a `Lane commit ... landed` sentence): `check ancestor pass=0 read=non-ancestor=654a6d069504`, exit 1.
- X8c control (lowercase non-ancestor hash): same, exit 1.

Among these, the defects of the rebased lane commit, amended report commit, and hash-in-table (final attributed by sentence) classes are caught when the hash is a full lowercase 40-hex hash in a recognised position. The gate's fixtures and selftest cover the same classes (`post-non-ancestor-hash`, `post-table-commit-column-non-ancestor`, `post-date-inversion-author-only-round45-shape`).

## 4. BROKEN: constructions where the gate reads exit 0 while the defect is present

Discriminating controls are listed with each; each control differs from the break by one feature and exits 1.

### B1 (cheapest). Stale lane commit cited as an ABBREVIATION; gate never checks abbreviations
Recipe: fixture with lane commits C1 (base), C2 (final landing, pushed). Create side commit `SIDE` off C1 on branch `side`, never merged into master (non-ancestor). Commit a report whose text is:
```
# Round 46 report

Lane repo, branch `master`, final lane hash `<C2 full>`.

Lane commit `654a6d0` landed earlier.

## SHONEN
- [~] box
```
Run `--post-report`. Output (verbatim, X7):
```
check report-readable pass=1 read=bytes=166
check cited-hashes pass=1 read=n=1,final=1
check resolves pass=1 read=unresolved=0
check ancestor pass=1 read=non-ancestor=0
check final-is-tip pass=1 read=final-not-tip=0,tip=025524fad70e(ls-remote)
check date-order pass=1 read=latest-cited=025524fad70e@2023-11-14T22:15:00Z,report-commit-committer=2023-11-14T22:16:50Z
check date-order-author pass=1 read=latest-cited=025524fad70e@2023-11-14T22:15:00Z,report-commit-author=2023-11-14T22:16:40Z
check shonen-heading pass=1 read=count=1
landing-gate mode=post-report checks=8 fail=0 exit=0
```
Shell exit 0. Verified: `git merge-base --is-ancestor 654a6d069504ad9a6413cb42e79f8a0df66910bd master` returned 1 (`ancestor_of_master_rc=1`), and the committed report line reads ``Lane commit `654a6d0` landed earlier.``. Control X7c (identical with the full 40-hex side hash) exits 1 with `ancestor` failing. The defect class is the one the gate's own docstring names (a lane commit cited that is not on the branch); the gate's regex `[0-9a-f]{40}` silently skips the abbreviation.

### B2. Stale lane commit cited as UPPERCASE 40-hex; git resolves it, the gate's HEX40 does not match
Recipe: as B1, the non-ancestor side hash written in uppercase: ``Lane commit `654A6D069504AD9A6413CB42E79F8A0DF66910BD` landed earlier.`` Output (X8): `check ancestor pass=1 read=non-ancestor=0` ... `check cited-hashes pass=1 read=n=1,final=1` ... `landing-gate mode=post-report checks=8 fail=0 exit=0` (shell exit 0). Verified the uppercase form is accepted by git: `git rev-parse --verify -q <UPPER>^{commit}` printed the lowercase hash, rc 0 (run against the real lane). Control X8c (lowercase) exits 1.

### B3. A table row says "final" but its hash cell is a stale hash; "final" is counted per cell, not per row
Recipe: fixture as B1 (side branch present but not needed). Committed report:
```
Lane repo, branch `master`, final lane hash `<C2 full>`.

| Milestone | Commit |
|---|---|
| final landing | `<C1 full>` |
```
Output (X5): `check cited-hashes pass=1 read=n=2,final=1`, `check final-is-tip pass=1 read=final-not-tip=0,tip=025524fad70e(ls-remote)`, `landing-gate mode=post-report checks=8 fail=0 exit=0` (exit 0). The table row explicitly claims C1 is the "final landing"; the gate's `FINAL.search(c)` runs on the hash cell only. Control X5c (word `final` inside the hash cell, e.g. ``| final `<C1>` |``) exits 1 with `final-not-tip=731b7b8929dc`.

### B4. GFM table without leading pipes: hashes never reach `report_blocks`
Recipe: committed report:
```
Lane repo, branch `master`, final lane hash `<C2 full>`.

Milestone | Commit
--- | ---
side branch | <SIDE full>
```
Output (X6): `check cited-hashes pass=1 read=n=1,final=1`, `check ancestor pass=1 read=non-ancestor=0`, `landing-gate mode=post-report checks=8 fail=0 exit=0` (exit 0). `report_blocks` only treats lines starting with `|` as table rows; this paragraph is joined text with no `landed`/`final lane hash`/`lane commit` trigger, so the hash is invisible. Committed blob confirmed by `git show HEAD:.ufo/reports/round-46/kasegi.md`. GFM spec §4.10 (https://github.github.com/gfm/) makes the outer pipes optional (found via web search; the spec itself was not fetched). Control X6c (same SIDE hash in a leading-pipe `| Commit |` table) exits 1 with `non-ancestor=654a6d069504`.

### B5. Tracked modification hidden by `skip-worktree`; tree-clean and jj-state both read `git status`
Recipe (fixture): `git update-index --skip-worktree LOG.md`; append `uncommitted` to `LOG.md`.
Output (X9, `--pre-report`):
```
check tree-clean pass=1 read=porcelain-lines=0
check jj-state pass=1 read=ahead=0,tracked=0,untracked=0
check remote-tip pass=1 read=remote=025524fad70e,local=025524fad70e
check placeholders pass=1 read=SCORECARD.md=0,LOG.md=0,SHONEN.md=0,corpus/lessons/round-46.md=0
landing-gate mode=pre-report checks=4 fail=0 exit=0
```
Shell exit 0. Verified on disk: `git ls-files -v LOG.md` printed `S LOG.md`; `tail -1 LOG.md` printed `uncommitted`; `git show HEAD:LOG.md | cmp - LOG.md` reported DIFFERS; `git status --porcelain` and `git diff --stat` both empty. Control X9c (same edit, no skip flag) exits 1 with `tree-clean pass=0 read=porcelain-lines=1` and `jj-state pass=0 read=...tracked=1`. jj-state is pure git (`scripts/hyaku/jj-lane.sh` lines 156-183), so it inherits the blind spot.

### B6. Dirty submodule hidden by `submodule.<name>.ignore = all` (in `.gitmodules`)
Recipe: fixture with a submodule `sub` whose `.gitmodules` entry carries `ignore = all` (committed); dirty `sub/a` without committing in the sub.
Output (X10, `--pre-report`): `check tree-clean pass=1 read=porcelain-lines=0`, `check jj-state pass=1 read=ahead=0,tracked=0,untracked=0`, `landing-gate mode=pre-report checks=4 fail=0 exit=0` (exit 0).
Verified: plain `git status --porcelain` empty; `git status --porcelain --ignore-submodules=none` printed ` M sub`; `git -C sub status --porcelain` printed ` M a`. Control X10c (same dirty sub, no ignore key) exits 1 with `tree-clean pass=0 read=porcelain-lines=1` and the raw status ` M sub`.
Note: the real lane has no gitlinks and no `.gitmodules` (`git ls-files -s` mode count: 8641/578/58 regular, no 160000), so this is fixture-only for today's lane.

### B7. User-level `status.showUntrackedFiles = no` hides untracked files from both tree-clean and jj-state
Recipe: untracked `stray.txt`; a git config file with `[status] showUntrackedFiles = no` supplied via `GIT_CONFIG_GLOBAL` (the form a `~/.gitconfig` takes). The gate's `git()` (line 71-81) passes no `-c status.showUntrackedFiles=...` and inherits the caller's environment; only the selftest overrides `GIT_CONFIG_GLOBAL` (line 563), in-process.
Output (X11, `--pre-report`): `check tree-clean pass=1 read=porcelain-lines=0`, `check jj-state pass=1 read=ahead=0,tracked=0,untracked=0`, `landing-gate mode=pre-report checks=4 fail=0 exit=0` (exit 0). Control X11c (same stray file, default config) exits 1 with `tree-clean pass=0 read=porcelain-lines=1`, `jj-state ... untracked=1`.
Limitation: the operator's actual global git config (key names only, `git config --global --list`) has no `status.*` key, so this does not fire on this host today.

### B8. Round lesson present on disk but git-ignored and never committed; pre-report reads the working tree only
Recipe: `.gitignore` line `corpus/lessons/round-46.md`; lesson removed from the index (`git rm --cached`) and committed; file re-created with clean text.
Output (X12, `--pre-report`): `check tree-clean pass=1 read=porcelain-lines=0`, `check placeholders pass=1 read=...corpus/lessons/round-46.md=0`, `landing-gate mode=pre-report checks=4 fail=0 exit=0` (exit 0).
Verified: `git ls-files corpus/lessons/round-46.md` printed nothing; `git check-ignore -v` printed `.gitignore:1:corpus/lessons/round-46.md`. Controls: X12c (same ignored lesson, text `filled by the L1`) exits 1 with `placeholders ... round-46.md=1`, so the gate reads ignored content; X12d (lesson untracked but not ignored) exits 1 with `tree-clean pass=0`. The gap is that the lesson's presence is checked only as a working-tree file, never as a tracked file in the lane.

### B9. Post-report gate reads the WORKING-TREE report; the committed blob can name a non-tip final
Recipe: commit the report naming C1 as final (C1 is not the tip at commit time: C2 was committed before the report). Then rewrite the working-tree copy to name C2, without committing.
Output (X13, `--post-report`, on the fixture): committed blob `Final lane hash \`731b7b8929dc...\`.`; working tree `Final lane hash \`025524fad70e...\``; `git status` of the fleet ` M .ufo/reports/round-46/kasegi.md`. Gate output: `check cited-hashes pass=1 read=n=1,final=1`, `check final-is-tip pass=1 read=final-not-tip=0,tip=025524fad70e(ls-remote)`, `check date-order-author pass=1 ...`, `landing-gate mode=post-report checks=8 fail=0 exit=0` (exit 0). Control X13c (committed report naming C1 with no working-tree edit) exits 1 with `final-is-tip pass=0 read=final-not-tip=731b7b8929dc`.
The gate never reads the landed blob (`git show <add-commit>:<path>`) and never checks the fleet report path is clean; the date check uses the add-commit while the cites come from the working tree.

### B10 (minor, unenforced claim). `--tip` is documented "replay only" but is accepted in live mode
Recipe: X1 fixture (report names non-tip C1; origin tip is C2); run `--post-report` live with `--tip <C1>`.
Output: `check final-is-tip pass=1 read=final-not-tip=0,tip=731b7b8929dc(override)` ... `landing-gate mode=post-report checks=8 fail=0 exit=0` (exit 0). Without `--tip`: `check final-is-tip pass=0 read=final-not-tip=731b7b8929dc,tip=025524fad70e(ls-remote)`. The flag's help text says "replay only", but nothing in `main()` (lines 610-633) restricts it.

## 5. Limitation (not a break of the stated contract)

X4: amend the report commit with `--reset-author` and `GIT_AUTHOR_DATE` set back to 19:19:10 (T0+350), text naming a later hash: `check date-order-author pass=1 read=latest-cited=db0cb71a1d97@...,report-commit-author=2023-11-14T22:19:10Z`, `landing-gate ... exit=0`. The author clock is git metadata a rewriter can set; the gate has no independent witness. (Note: a plain `commit --amend --no-edit` keeps the author date and is caught (X3); `GIT_AUTHOR_DATE` alone is ignored by amend without `--reset-author`.)

## 6. Passed by construction (not falsified)

- Rebased lane commit (X2): exit 1, `ancestor` and `final-is-tip` fail.
- Amended report text with author kept (X3): exit 1, `date-order-author` fails.
- Non-ancestor full hash in a sentence or leading-pipe table (X6c, X7c): exit 1.
- Dirty tracked (X9c), dirty submodule without ignore (X10c), untracked (X11c), lesson untracked-not-ignored (X12d), placeholder in an ignored lesson (X12c): exit 1.

## 7. Recommended direction (for L1 decision; not implemented here)

1. Read the landed blob (`git show <add-commit>:<path>`) for every cite, not the working tree; require the fleet report path to be clean and committed.
2. Match hashes case-insensitively and resolve abbreviations with `git rev-parse --verify <tok>^{commit}` over every 4+-hex token in a trigger sentence.
3. Apply FINAL per table row (the row text, not the hash cell), and parse pipe-less GFM tables.
4. Quiescence: `git status --porcelain --ignored=matching --untracked-files=all --ignore-submodules=none` with `-c status.showUntrackedFiles=normal`, plus `git ls-files -v | grep -v '^H '` to catch skip-worktree/assume-unchanged; require each of the four landing files to be tracked.
5. Reject `--tip` unless a replay flag also names the fixture root.

## 8. Limitations of this review

- Fixture-only constructions (each fresh under `$S`); no live landing was run. The live lane was read, not landed to.
- `--pre-report` was not run against the live lane (it is pure git, but the round-46 lane state is mid-round); B5/B6/B7/B8 are demonstrated on fixtures only.
- The GFM pipe-optional claim is from the spec text reached by web search (https://github.github.com/gfm/, §4.10), not fetched and read verbatim.
- Scratch removed on exit; no file in the fleet or lane was modified; no git mutation was performed on the lane or fleet (read-only `log`/`show`/`cat-file`/`rev-parse`/`status`/`ls-remote`/`diff --quiet` only); the one `--tip` replay and the round-45 replay were read-only.
