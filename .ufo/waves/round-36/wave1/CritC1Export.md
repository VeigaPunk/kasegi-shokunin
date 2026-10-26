# CritC1Export — export-mode discipline attack (round 36, depth:verifiability)

Seat: critic, lane `kasegi-shokunin`, round-36 wave 1. Leaf seat; no subagents, no lane writes
except this receipt. All fixtures were throwaway repos under
`/fast/scratch/hyaku/kasegi-r36/CritC1Export/` (each toplevel verified with
`git -C <dir> rev-parse --show-toplevel` before any `git init/add/commit`); the lane repo was
only read (git archive/rev-parse/ls-tree/ls-files/status).

## Artifact attacked

Draft under test (not yet in the lane; the L1 has not landed it):

| file | sha256 | lines |
|---|---|---|
| `/fast/scratch/hyaku/kasegi-r36/ExecC1SuiteBuild/r36-closure.sh` | `ff616adc045a8938c7ca69b3693565ef0f676a0d1d67df293b1b6c4a82da4720` | 737 |

Copied to my scratch as `s1.sh`; all outputs below are from that copy. `bash -n` clean.
Sibling drafts `ExecC1ExportMode/draft-r36-closure.sh` (18 235 B) and
`ExecC1Fixtures/r36-closure.sh` (13 696 B) were also inspected; the first accepts the same two
escape flags (`--lane`, `--scratch-root`) on its plain run, the second does not.
Tooling: no installs needed — bash 5.3.20, git 2.56.0, GNU tar 1.35 (recorded per operator
tooling policy; nothing upgraded).

## Baselines on the shipped draft (default flags, real lane)

```
bash s1.sh                                     -> rc=2  "refusing to run against the live worktree"
bash s1.sh --export-ref 3266c99…(r35 base)     -> closed=0/9 exit=1  rc=1
bash s1.sh --export-ref 0aee0ef…(r35 judged)   -> closed=4/9 exit=1  rc=1
bash s1.sh --export-ref b47f2cd…(r36 freeze)   -> closed=5/9 exit=1  rc=1   (E3,E4,E8,E9 open)
bash s1.sh --selftest  (freeze head, live)     -> selftest cases=9 failures=4 (E3,E4,E8,E9) rc=1
```

Positive results that held (so the default discipline is real):

- **No-args run is refused (exit 2)** — no live-worktree default.
- **The export is materialised from the resolved ref**: an *uncommitted* worktree fix does not
  leak. Fixture `forge4`: committed `SKILL.md` has only `r35-defect-closure.sh`; worktree then
  gets `r36-closure.sh`; `--export-ref <old commit>` prints
  `E3 payload=registry-r35-defect-closure=1,registry-r36-closure=0 closed=0`, i.e. the export
  measured the commit, not the worktree.
- **Arg hardening**: no arg / `--export-ref ""` / `--export-ref --output=/path` / blob sha /
  tree sha / `zzzz` → exit 2 (option-shaped values die in `rev-parse --verify`); short sha and
  `HEAD` resolve and the resolved 40-hex is printed; `--work <lane>/x`, `--work /`, a symlinked
  `--work` into the lane → exit 2, nothing created.
- **Pre-seeded work dir**: `$WORK/export` symlinked at the lane is `rm -rf`-ed (link removed,
  target untouched), recreated as a real dir; lane `git status --porcelain` 9→9 entries.
- **tar traversal**: a crafted member `../escape` is stripped/refused by GNU tar 1.35
  (`Member name contains '..'`), nothing written outside `-C`.
- **No leftovers on normal paths**: default run → 0 `/tmp/r36-closure.*` dirs; `git status`
  count unchanged; `.git/index` mtime/size/inode unchanged, no `index.lock`; SIGINT during a run
  cleans up (0 leftovers). `--work DIR` keeps the caller's (empty) dir by design.

## Counterexamples (the attack surface)

### C-1 (high, provenance) — plain run accepts `--lane` and `--scratch-root`, so it can print 9/9 for an arbitrary repo

Both flags are parsed in export mode. A forged repo with a fully green tree (all E limbs,
`Final lane commit:` line bound to one of its own ancestors) run with the *documented* command
shape plus two flags:

```
bash s1.sh --lane /…/forge2 --export-ref <forge-head> --scratch-root /…/emptyroot
export-ref=<forge-head> mode=export
E1..E8 closed=1
closed=9/9 exit=0        rc=0
```

Real lane untouched (`git status` 9 entries before and after). The header prints only
`export-ref=<sha>` — not `lane=` — so the pasted output is indistinguishable from an honest run
when the forged ref is not the lane head. `--scratch-root` likewise neutralises E9's quiescence
limb on the real lane: `scratch-seat-dirs=33` with the default root vs `scratch-seat-dirs=0`
with `--scratch-root <empty dir>` (same run, same ref). `--scratch-root /nonexistent` or a path
that is a file also yields `scratch-seat-dirs=0` (the limb fails open).
The same two flags make `--selftest` print `cases=9 failures=0` on the forged repo.

### C-2 (high, environment) — `GIT_DIR`+`GIT_WORK_TREE` forges the whole run with no extra flags

```
GIT_DIR=/…/forge2/.git GIT_WORK_TREE=/…/forge2 bash s1.sh --export-ref <forge-head> --scratch-root <empty>
closed=9/9 exit=0        rc=0
```

Every `git -C "$LANE" …` call (rev-parse, archive, cat-file, merge-base, ls-tree, ls-files,
status) is redirected to the forged repo, so E1's "exists and is an ancestor" and E9's
`head-match` are both evaluated in the forged repo. `GIT_DIR` alone leaves E9 open
(`status-dirty=192,head-match=1` → 8/9), i.e. E9's head equality is the only thing that catches
the env vector today. `GIT_ALTERNATE_OBJECT_DIRECTORIES=<forge>/.git/objects` with the real
`--lane` forges E1 and E4 (`bound=1`, `tracked-ref=1`) giving 7/9, blocked only by
`head-match=0`. `GIT_INDEX_FILE` also redirects E4's index limb
(`GIT_INDEX_FILE=/dev/null git -C lane ls-files -- .ufo/waves/round-35/wave1-results.json` → 0).

### C-3 (medium, export fidelity) — the export is not a function of the ref: attributes silently drop measured files, and E8's absence limb flips

`git archive` honours `export-ignore` from `.git/info/attributes` (repo-local, uncommitted) and
from `core.attributesFile` (global config). Same ref, same command:

```
forge2 with  corpus/lessons/round-35.md  = "source-recheck exit 0 on committed bytes" (the stale line)
  bash s1.sh --lane forge2 --export-ref H --scratch-root empty
      E8 payload=m36-rows=1,stale-line=1 closed=0     closed=8/9
  # add  .git/info/attributes:  corpus/lessons/round-35.md export-ignore
  bash s1.sh --lane forge2 --export-ref H --scratch-root empty
      E8 payload=m36-rows=1,stale-line=0 closed=1     closed=9/9 exit=0
  # ref unchanged:  git show H:corpus/lessons/round-35.md | grep -cF … = 1
  # export files=8, git ls-tree -r H = 9 entries
```

On the real r35 judged head the same global attributes file flips
`E8 payload=stale-line=1` → `stale-line=0` (closed stays 4/9 only because round-36.md is absent
there, so `m36-rows=0`). The instrument has no export-vs-`ls-tree` fidelity check, so any
"absence" limb (E1 placeholders — guarded only by `[ -f SCORECARD.md ]`, E8 stale line) can be
satisfied by dropping the file from the export instead of cleaning the ref.

### C-4 (medium, symlinks) — a committed symlink at a measured path is followed outside the export

Committed mode `120000` survives `git archive`; every measured path is probed with `-f`/`-e`/grep
without `! -L`. Fixture `forge3` (two measured paths committed as symlinks into the live lane):

```
git ls-tree -r H -- .ufo/waves/round-35/claims-erratum-d5.md corpus/QUALITY.md
120000 … claims-erratum-d5.md      120000 … corpus/QUALITY.md
bash s1.sh --lane forge3 --export-ref H --scratch-root empty
E5 payload=claims-erratum-d5=1 closed=1
E7 payload=supersedes-r22=1,supersedes-r23=1 closed=1
closed=9/9 exit=0
```

The same class was reproduced on the committed r35 template (`corpus/instruments/r35-defect-closure.sh`):
an export whose only `claims-erratum-d5.md` is a symlink to bytes outside the export prints
`D5 … open=0`. The lane carries 58 tracked symlinks at HEAD, so this is not hypothetical content
for a future tree; none sit on a measured path today.

### C-5 (medium, leftovers) — SIGTERM leaves the export behind

`trap cleanup EXIT` does not fire on SIGTERM. Killing a run against the lane head:

```
bash s1.sh --export-ref b47f2cd… & sleep 0.35; kill -TERM $!
after TERM: /tmp/r36-closure.cK4TtxuH  files=7117
```

(SIGINT cleans: 0 leftovers. In one TERM run `rm -rf` raced a still-writing `tar` child —
`Directory not empty` — so the orphaned extractor can keep writing into the leaked dir.)
`TMPDIR` is not validated either: only `--work` is checked against the lane, while
`mktemp -d -t` honours an inherited `TMPDIR`, so a `TMPDIR` inside the lane would place the
export there (placement observed on a fake lane; a normal exit cleans it, a TERM does not).

### C-6 (low) — E4 reads the live index, not the export

`t_idx=$(git -C "$LANE" ls-files -- "$p")` is an index read of the live lane in an
"export-mode only" instrument (the ref limb `ls-tree` is what makes base=0/9 work). It cannot
false-pass on the base export (`tracked-ref=0`), but it is redirectable (`GIT_INDEX_FILE`) and
can only false-fail at filing. Replace with `git cat-file -e "${ref}:$p"`.

### C-7 (low, check semantics, cross-ref CritC1Kill) — E1's "structural" hash binding is a 4-line window

`e1_bound_hashes` accepts any 40-hex in the `Final lane commit:` line *or the four lines after
it*. Fixture `forge6` keeps the round-34 prose spelling on the anchor line and puts a real
ancestor hash one line below:

```
**Final lane commit: the L1 fills this line in the closing commit**
correction cites `<real ancestor>`
…
E1 payload=placeholders=0,lane-hash-markers=0,final-lane-commits=1,bound=1 closed=1
closed=9/9 exit=0
```

That is the r35 "prose placeholder" residue the round-35 lesson said to close by slot-binding
(`round-35.md:231`). Not a kill against the frozen wording (the claim bans the two literal
tokens), but the selftest has no prose+hash mutant, so nothing pins it.

Minor note: the draft itself contains each hunted literal once (in comments), harmless because
E1 greps only `SCORECARD.md`; keep it that way if any future check greps the tree.

## Impacted axes

- `depth:verifiability` (C1, the axis under review): C-1/C-2 break the identity of the measured
  tree in the instrument's own output; C-3/C-4 break "the export of the named head" reading;
  C-5 breaks the "writes nothing outside scratch" claim under signals. The default counting
  command is still honest today, so the held-4 verdict is not obviously lost — but the
  instrument is not yet the self-binding gate the claim describes.
- No `coverage` or `depth:density` impact: none of the above changes measured content on an
  honest run.

## Smallest safe corrections

1. Plain mode: reject `--lane` and `--scratch-root` (allow only with `--selftest`) or print
   `lane=<abs>` + `scratch-root=<abs>` in the header and require `lane`'s
   `rev-parse --show-toplevel` to equal the compiled `LANE`. This alone kills C-1 and the E9
   override.
2. Wrap every git call in one `lane_git()` helper that strips the redirect environment:
   `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_OBJECT_DIRECTORY
   -u GIT_ALTERNATE_OBJECT_DIRECTORIES -u GIT_COMMON_DIR -u GIT_CEILING_DIRECTORIES
   -u GIT_NAMESPACE -u GIT_CONFIG_GLOBAL -u GIT_CONFIG_SYSTEM git -C "$LANE" …` (keep PATH/HOME).
   Kills C-2.
3. After extraction, verify export fidelity against the ref: compare
   `git ls-tree -r --name-only <ref>` with the extracted file list (or at least each measured
   path: present, mode `100644`, not a symlink). Kills C-3 and C-4; one `ls-tree` loop covers both.
4. `trap 'cleanup; exit 130' INT TERM HUP` and capture the `tar` PID in `prepare_export` so
   `cleanup` can kill it before `rm -rf`. Validate `TMPDIR` the way `--work` is validated. Kills C-5.
5. E4: replace the `ls-files` limb with `git cat-file -e "${ref}:$p"` (C-6).
6. E1: require the 40-hex on the `Final lane commit:` line itself and add the prose+hash mutant
   to the selftest (C-7).

## Probe set to rerun on the landed file (unchanged expectations)

```
bash corpus/instruments/r36-closure.sh                                  # exit 2
bash … --export-ref 3266c9937b03062d9bbc2f436e20820115ed179c           # closed=0/9 exit=1
bash … --export-ref 0aee0ef105395a2f1d6ace7eaeef13871bb26988           # closed<9/9 exit=1
bash … --selftest                                                      # cases=9 failures=0 exit=0 (only at the final head)
bash … --lane <green-forge> --export-ref <forge-head> --scratch-root <empty>   # must NOT be a green path
GIT_DIR=<forge>/.git GIT_WORK_TREE=<forge> bash … --export-ref <forge-head>    # must NOT be green
TMPDIR=<lane> bash … --export-ref <head>                               # must refuse or stay outside the lane
# after a green run: git status --porcelain unchanged, no /tmp/r36-closure.* left,
# .git/index stat unchanged, and a TERM’d run leaves no work dir
```

The draft was 737 lines, sha256 as tabled above; if the landed instrument differs, rerun this
probe set against the landed sha256 before treating any of the above as closed.
