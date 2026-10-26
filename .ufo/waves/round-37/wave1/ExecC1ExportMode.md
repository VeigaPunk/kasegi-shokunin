# ExecC1ExportMode — export-mode contract of the existing r36-closure.sh

Round 37, wave 1, seat `ExecC1ExportMode`. Judged on depth:verifiability.
Scope: measure the **export-mode contract** of the already-committed
`corpus/instruments/r36-closure.sh` from a scratch copy and state the invariants the r37
suite must preserve. Receipt only; no lane, fleet or source-tree writes.

## Method

- Instrument under test: `corpus/instruments/r36-closure.sh` at lane HEAD
  `b362068195d5489aa94b31e6ec8f880c367e0ba0` (post-freeze `claims-erratum-1`), extracted with
  `git -C <lane> archive HEAD corpus/instruments/r36-closure.sh | tar -x -C <scratch>/copy`
  — i.e. the same export mechanism the instrument itself verifies. Copy sha256
  `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` = lane file sha256.
- All runs executed from `/fast/scratch/hyaku/kasegi-r37/ExecC1ExportMode/copy/...` with
  explicit `--work`/`--scratch-root` under that scratch dir, except the TMPDIR cleanup tests.
  Lane reads were read-only git; lane status hash before and after every batch is
  `b5937319aac10a2a315d1e248dbf0a7c00e20517b6b4ef61339044e6af527cbc` (6 untracked round-37
  wave paths in flight), HEAD unchanged, `.git/index.lock` absent throughout.
- Scratch dir removed after this receipt was written. No tools installed or upgraded.

## Observed evidence, invariant by invariant

### I1 — plain run refuses with exit 2 (export mode is the only run mode)

```
$ bash copy/corpus/instruments/r36-closure.sh
exit=2
r36-closure: refusing to run against the live worktree: this suite is export-mode only.
r36-closure: pass --export-ref <hash> (see --help) or --selftest.
```

Same refusal, exit 2, for a plain run that *does* pass `--lane/--work/--scratch-root`
(T2): `w2-exists=no` — the refusal happens before `make_work`, so a refused run creates no
directory. Refusal text appears before any lane git read (mode branch precedes
`prepare_export`).

### I2 — `--work` inside the lane is refused (exit 2) with no trace

```
--work <lane>/r37-work-probe   exit=2  r36-closure: --work must be outside the lane (it would write there): <lane>/r37-work-probe
--work <lane>                  exit=2  r36-closure: --work must be outside the lane (it would write there): <lane>
--work <lane>/../kasegi-shokunin/sub
                               exit=2  r36-closure: --work must be outside the lane (it would write there): <lane>/sub
--work <scratch>/link-lane/work (link-lane -> <lane>)
                               exit=2  r36-closure: --work must be outside the lane (it would write there): <lane>/work
--work /                       exit=2  r36-closure: --work must not be /
```

`lane-probe-exists=no`, `sub-exists=no`: the synthetic `<lane>/sub` was not created.
`--work` pointing at an existing regular file: exit 2,
`mkdir: cannot create directory '.../afile': File exists` +
`r36-closure: cannot create work dir: .../afile`. The guard is `realpath -m` (line 203)
before any mkdir, plus a physical re-check after `cd`+`pwd -P` (line 216), which is what
catches the symlinked lane path.

### I3 — stale `export/` and `mut/` are cleared before use; stale bytes cannot satisfy a check

Reused `--work` pre-seeded with `export/corpus/lessons/round-35.md` carrying the stale
E8 evidence line, a forged `export/.ufo/waves/round-35/claims-erratum-d5.md`,
`export/STALE-MARKER`, and `mut/leftover/SCORECARD.md`. `bash -x` trace:

```
+ rm -rf -- <S>/W2/export <S>/W2/mut
+ mkdir -p -- <S>/W2/export <S>/W2/mut
+ tar -xf - -C <S>/W2/export
+ git -C <lane> archive --format=tar b362068195d5489aa94b31e6ec8f880c367e0ba0
...
+ rm -rf -- <S>/W2/export
+ rm -rf -- <S>/W2/mut
```

Payload diff against a run into a pristine work dir: `IDENTICAL` (all nine `E<n>` lines and
`closed=8/9`), so the seeded bytes were not read. `STALE-MARKER present-now=no`; after exit
`W2` is empty (both owned subdirs removed).

Direct stale-satisfaction test: seeded `claims-erratum-d5.md` in `--work`, exported
round-34 ref `3266c9937b03062d9bbc2f436e20820115ed179c` (file absent there):
`E5 payload=claims-erratum-d5=0 closed=0`, `closed=0/9 exit=1` — the stale file did not
close E5, and the export likewise carries the ref's bytes, not the worktree's (the worktree
at HEAD *does* carry that file, `E5 ... closed=1`).

### I4 — `--export-ref` resolution

```
--export-ref HEAD          -> export-ref=b362068195d5489aa94b31e6ec8f880c367e0ba0  exit=1 (8/9; E9 red in flight)
--export-ref b362068       -> export-ref=b362068195d5489aa94b31e6ec8f880c367e0ba0
--export-ref 'HEAD~1'      -> export-ref=f3246559bed2fd085dde860e00247ce394f02bad
--export-ref 'HEAD^{commit}'> export-ref=b362068195d5489aa94b31e6ec8f880c367e0ba0
```

Red paths, all exit 2, all before `make_work` (no work dir created; `w-bad-exists=no`):

```
--export-ref no-such-ref-xyz -> r36-closure: cannot resolve export ref in <lane>: no-such-ref-xyz
--export-ref <blob>          -> error: <blob>^{commit}: expected commit type, but the object dereferences to blob type
                                r36-closure: cannot resolve export ref in <lane>: <blob>
--lane <missing dir>         -> r36-closure: lane is not a directory: <dir>
--lane <non-git dir>         -> r36-closure: lane is not a git repository: <dir>
--selftest --export-ref no-such-ref-xyz -> exit 2, same resolve message
```

Not-a-lane-tree guard (fixture repo with a commit but no `SCORECARD.md`): exit 2,
`r36-closure: export has no SCORECARD.md (not a lane tree): 795f47f6f1257c38ac92cfdef45ebfc5f33d96b7`.

Export header on the real lane: `export-ref=<full sha> mode=export lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin suite-sha256=4db1ae70...b7c4`.

### I5 — cleanup on exit

- Explicit `--work`: after every run (clean run, stale-seeded run, symlinked-subdir run,
  round-34 run) `find <work> -mindepth 1` printed nothing — `export/` and `mut/` are always
  removed by the `EXIT` trap; the work dir itself is retained (user-owned).
- Auto work dir honouring TMPDIR: `TMPDIR=<scratch>/tmp bash <copy> --export-ref HEAD`;
  after exit `tmp-leftover=0` (the `mktemp -d` work dir is removed).
- Die inside `prepare_export` after `make_work` (no-SCORECARD fixture, TMPDIR=`<scratch>/tmp3`):
  exit 2 and `tmp3-leftover=0`.
- `--selftest --work W12 --scratch-root <empty>`: exit 1 on the in-flight dirty lane
  (`selftest cases=9 failures=1`, `judge=own-report accepted=0`, all four forgeries
  `rejected=1`, `cases-pass=8` — E9's positive limb is the lane's own quiescence, red here
  by design). Leftover under `W12`: only the five selftest report files
  (`selftest-report.txt`, `forge-summary.txt`, `forge-caselines.txt`,
  `forge-failed-cases.txt`, `forge-detail-free.txt`); `export/` and `mut/` removed.
- Lane untouched: status hash identical before/after, HEAD unchanged, no `.git/index.lock`
  (E9 uses `git --no-optional-locks`), `corpus/` status hash unchanged after the symlinked
  work run.

### I6 — absolute-path hygiene

- `--lane` normalised once in `main` (`cd "$LANE" && pwd -P`, line 878). From `cwd=/` with a
  *relative* lane path (`--lane home/vgpnk/Projects/shokunin/kasegi-shokunin`): header prints
  `lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin`, `deviation=non-default --lane`, and
  `E1 payload=...bound=2 closed=1` — the round-35 false red from a relative lane path inside
  E1's `cd "$tree"` subshell no longer occurs.
- Relative `--work relw` and relative `--scratch-root sroot` from the scratch cwd were
  accepted and resolved against that cwd (`relw-after: 0 entries`; E9 read the two seat dirs).
- E9's own-work exclusion is by *physical* absolute path: with `--scratch-root <S>` holding
  20 top-level dirs and `--work <S>/W15`, payload reported `scratch-seat-dirs=19`; with
  `--scratch-root <S>/sroot2` holding exactly `seatA seatB`, payload
  `scratch-seat-dirs=2`. A typo'd root is visible as `scratch-root=absent`.
- Residual: `SCRATCH_ROOT` (default `/fast/scratch/hyaku/kasegi-r36`, line 128) is **not**
  normalised — a relative `--scratch-root` is cwd-dependent, unlike `--lane`. See G4.

### I7 — "every check reads its bytes only under that export root" is false for committed symlinks

`git archive` faithfully exports a committed symlink. Fixture repo `d2.*` (toplevel verified
`= $D`): first commit `h1`, then tracked `SCORECARD.md` as mode `120000` ->
`<scratch>/decoy-SCORECARD.md` (79 bytes **outside** the export root) containing
`## Round 36` + `Final lane commit: <h1>`. Run:

```
ls-tree mode: 120000 blob 6fc90531...	SCORECARD.md
export-ref=f29db3dcafecaeb7b2140672f18a3d097c39e34d mode=export lane=<D> ...
E1 payload=placeholders=0,lane-hash-markers=0,round36-section=1,round36-final-lane-commits=1,bound=1 closed=1
closed=2/9 exit=1
tar -tv: lrwxrwxrwx root/root 0 SCORECARD.md -> <scratch>/decoy-SCORECARD.md
```

E1 closed by reading bytes that are not in the export. `[ -f "$EXPORT/SCORECARD.md" ]` and
every check's `[ -f ... ]`/`grep` follow symlinks; nothing lstats the exported path or checks
the `git ls-tree` mode. If r37 keeps the "reads only under the export root" prose, it needs a
symlink guard (G3).

### I8 — a status read that fails is counted as clean (r36 fail-open; D6)

Fixture repo `d3.*` with one commit and a valid `SCORECARD.md`, then `chmod 000 .git/index`:

```
$ git --no-optional-locks -C <D> status --porcelain
fatal: .git/index: index file open failed: Permission denied
rc=128
$ bash <copy> --export-ref HEAD --lane <D> --work W16 --scratch-root sroot3
E9 payload=status-dirty=0,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present closed=1
```

Code: line 465 `porcelain=$(git ... status --porcelain 2>/dev/null | count_lines)` and line
466 `porcelain=${porcelain:-0}` — stderr swallowed, failed read becomes 0. This is exactly
what the frozen claim's E14 forbids in r37 (`grep -cF 'porcelain:-0' r37-closure.sh` -> 0,
no status-read `2>/dev/null` swallow). r36 is the *positive control* for that red: the
rewritten suite must turn this fixture red, not green.

### I9 — suite digest is not bound to the executing bytes

- Executed through process substitution (`bash <(cat <copy>) --export-ref HEAD ...`):
  header `suite-sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
  = sha256 of the **empty file**, while the full 39 022-byte suite executed and printed
  `closed=8/9 exit=1`. `suite_digest()` (lines 146-153) hashes `${BASH_SOURCE[0]}` — a pipe,
  not the bytes being interpreted.
- Executed on stdin (`bash -s -- --export-ref HEAD ... < <copy>`): `bash: line 892:
  BASH_SOURCE[0]: unbound variable`, exit **1** (not the documented 2), from the entry guard
  `[ "${BASH_SOURCE[0]}" = "$0" ]` (line 892) under `set -u`.
- Under a normal path the digest is correct: both the lane file and the export copy hash to
  `4db1ae70...b7c4`, and the header prints it.

E10 requires `suite-sha256=<sha>` with `sha == digest of the suite bytes`; the gate must
recompute that digest from the named head's blob (`git show <head>:corpus/instruments/r37-closure.sh`)
and reject a header it cannot reproduce, otherwise the empty-file digest above forges the
binding.

## Invariants the r37 suite must preserve (measured green in r36)

1. Plain run (no `--export-ref`, no `--selftest`) refuses **exit 2** before any lane read or
   write; `--work`/`--lane` arguments do not weaken that refusal. (I1)
2. `--work` inside the lane — direct, `..`-normalised, or via symlink — refuses **exit 2**
   with the resolved path in the message, and leaves no directory behind; `--work /` refuses;
   a non-creatable work path refuses with exit 2. (I2)
3. The suite's own `export/` and `mut/` are `rm -rf`'d and recreated **before** extraction, so
   a reused `--work` cannot satisfy any check from stale bytes; payloads are byte-identical
   to a pristine-work run. (I3)
4. `--export-ref` is dereferenced to a **commit** (`^` `{commit}`), accepts full sha, short
   sha, `HEAD`, `HEAD~1`, refuses blobs/unknown refs/missing or non-git lanes/export trees
   without `SCORECARD.md` with **exit 2**, and every check reads the ref's bytes (not the
   worktree's). (I4)
5. Cleanup on exit removes `export/` and `mut/`, removes a TMPDIR-created auto work dir, and
   survives a die after extraction; the lane ends byte-identical with no `index.lock`. (I5)
6. Path hygiene: `--lane` normalised once to a physical absolute path so checks run from any
   cwd; E9's own-work exclusion compares physical absolute paths; seed dirs are counted by
   `find` at depth 1. (I6)
7. Quiescence itself (E9) is evaluated against the *named* ref equality (`head-match=1`),
   lane-root equality, a live status read, and the scratch root; `scratch-root=present|absent`
   makes a typo visible. (I6/I8)

## Additional guards the r37 suite needs

- **G1 (required by E10/E14, and by I9):** derive `suite-sha256` from the *ref's blob*
  (`git -C "$LANE" cat-file blob "$REF_RESOLVED":corpus/instruments/r37-closure.sh | sha256sum`),
  not from `BASH_SOURCE`; die **exit 2** if it cannot be computed. Fail-closed on the
  pipeline/stdin execution forms (I9) and fix the entry guard to `${BASH_SOURCE[0]:-$0}` so a
  missing source path is a harness error, not an unbound-variable exit 1. The E10 gate must
  independently recompute the blob digest and compare it to the header — never trust the
  header.
- **G2 (required by E14):** the status read must be rc-checked; on failure print a distinct
  payload token (e.g. `status-unreadable`) and close E9 as red. No `2>/dev/null` swallow and
  no empty-to-zero default around the status call (r36 lines 465-466; fixture I8 proves the
  fail-open). `grep -cF 'porcelain:-0' r37-closure.sh` must stay 0.
- **G3 (required if r37 repeats r36's "reads only under the export root" claim; otherwise
  weaken that sentence):** bind every file a check reads to an exported regular file.
  Cheapest: after extraction, `find "$EXPORT" -type l` must be empty (or every symlink must
  appear in an explicit allowlist), plus per-path `[ ! -L ]` / `git ls-tree` mode
  `100644|100755` for `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`,
  `corpus/lessons/round-*.md`, `.ufo/waves/**/*.json|md`. I7 is a real green-escape.
- **G4 (hygiene):** normalise `--scratch-root` once (`cd && pwd -P`) exactly like `--lane`,
  and print the normalised value in the header/payload; keep the own-work exclusion by
  physical path (measured working). A relative root currently depends on the caller's cwd.
- **G5 (residue, code-read):** the `EXIT` trap is installed at line 227, *after* the
  `mkdir -p` at line 226; a die between them (post-mkdir `pwd -P` failure) would leave an
  empty user-visible dir. Install the trap before the first mkdir, or remove the just-created
  dir on that die path. (Not triggerable through the measured argument surface.)
- **G6 (keep):** `git --no-optional-locks` for the status read (no transient `index.lock`
  under the lane: observed absent), `rm -rf` on symlinked `export`/`mut` removes the link only
  (measured: lane `corpus/` intact, decoy dir's `keep.txt` intact, links gone), and the
  non-lane-tree `SCORECARD.md` guard before any check runs.
- **G7 (advisory):** the `--selftest` mode writes its five report files under `--work`; keep
  them outside the lane and document that E9's positive limb reads live quiescence, so
  `--selftest` cannot be green while the lane worktree is dirty (observed failures=1 on the
  in-flight dirty lane).

## Retained evidence summary

- Instrument sha256 `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4`
  (lane `corpus/instruments/r36-closure.sh` @ `b362068` = scratch export copy).
- Lane state before/after all batches: HEAD `b362068195d5489aa94b31e6ec8f880c367e0ba0`,
  status hash `b5937319...af527cbc`, no `index.lock`.
- Fixture repos created only under the scratch dir with `git init` and verified
  `rev-parse --show-toplevel` == physical fixture path: `d1.*` (no SCORECARD),
  `d2.*` (symlinked SCORECARD escape), `d3.*` (unreadable index status fail-open).
- Scratch dir `/fast/scratch/hyaku/kasegi-r37/ExecC1ExportMode` removed after write.

## Risks / blockers

- All observed runs are against the in-flight lane (`b362068`, 6 untracked round-37 wave
  paths), so E9 is red (`status-dirty=6`) and full `closed=9/9` cannot be observed in this
  wave; the r37 final-head contract is the scheduler's to exercise, not this seat's.
- No defect in the export-mode machinery itself was found: I1-I6 all hold. The two measured
  holes (I7 symlink escape, I8 status fail-open) are exactly the class E14/G2 and G3 guard,
  and I9 is the digest-binding hole E10 must close at the gate.
- No blockers.
