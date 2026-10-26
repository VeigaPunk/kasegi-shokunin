# ExecH6ScratchFixtures — round-40 wave-1 receipt

Seat: `ExecH6ScratchFixtures` (executor, leaf). Item: prove the H6 limb discriminates — a
stray `kasegi-r39*`/`kasegi-r40*` scratch-sibling reds the run (exit 1, `closed<10/10`,
payload naming the stray), its removal greens it, and the passed `--work` dir itself never
reds the run. Axis touched: **depth:verifiability**. No claims, registry rows or receipts
of other seats were edited.

**Verdict: PASS on the reference limb.** The built suite
`corpus/instruments/r40-closure.sh` did not exist during this seat's work (see §5), so the
probe-equivalent path allowed by the item was used and is delivered as a self-contained
bash probe: it needs no lane export, no git and no suite. 21 scenarios, 0 failures; the two
required transcripts (RED then GREEN) are recorded verbatim in §3.

## 1. Deliverable

- Path: `.ufo/waves/round-40/wave1/ExecH6ScratchFixtures.sibling-dir.sh`
- 434 lines, 15,375 bytes, sha256
  `202f46bddd524284f54f6cde4332d842ef16243a1f14e14873461b4f1b3d8339`
- Modes:
  - default: run the 21-scenario discrimination matrix in an isolated sandbox
    (`mktemp -d` under `TMPDIR`, or `--root DIR`); prints one expecting transcript per
    scenario and `probe scenarios=<n> failures=<k>`; exit 0 only when k=0.
  - `--check --scratch-root DIR --work DIR`: run the H6 limb once; prints the
    suite-shaped `H6 payload=... closed=0|1` line and `closed=<K>/10 exit=<0|1>`;
    exit 0 green / 1 red. Neither DIR is created or modified.
  - `-h|--help`.
- Hermetic: refuses (exit 2, before touching anything) a scratch root that is
  `/fast/scratch/hyaku` or an ancestor of it. Nothing outside its sandbox is read or
  written; every sandbox is removed on exit (verified in §3/§6).

`check_h6` (the limb, signature `check_h6 SCRATCH_ROOT WORK_DIR`, payload on stdout,
exit 0 green / 1 red) implements exactly this frozen-H6 contract:

- Scan only **top-level entries** of the scratch root whose basename, after stripping one
  leading dot, matches `kasegi-r39*` or `kasegi-r40*` (prefix match, not one exact name:
  catches `kasegi-r39-l1`, `kasegi-r40-<seat>`, `kasegi-r40-build-extra`, `kasegi-r40x`,
  `.kasegi-r40-seat`). Every entry type is in scope: directory, regular file, dotfile,
  symlink. Names outside that namespace (`kasegi-r41*`, `gates-work`, …) are ignored —
  the r39 G6 defect was an exact-name scan, and widening to the whole root would red on
  other lanes' live scratch.
- Tolerate only the physical (`pwd -P`) realpath of the passed `--work` dir, and a clean
  chain: a matching entry that is a strict ancestor of `--work` where every level from the
  entry down to `--work` contains exactly the next component and nothing else. Tolerance
  is by realpath, never by name, so a symlink named `kasegi-r39-link` that resolves to the
  work dir is tolerated, while a symlink named `kasegi-r40-seat` to a foreign dir is not.
- Presence is RED, not content: an empty stray dir, a regular file, a dangling/unresolvable
  entry, and a directory that cannot be entered all red the run. Entries are judged with
  `find -mindepth 1 -maxdepth 1` (dotfiles included), and an unreadable scratch root or an
  unresolvable `--work` is RED (`read=fail`), never "zero entries".
- Payload is host-independent: `H6 payload=r39=<state>,r40=<state>,work=<inside|outside>,
  tolerated=<names|none>,strays=<names|none>,read=<ok|fail> closed=<0|1>`; only basenames
  appear (no absolute paths), so an H7 re-run with identical args cannot vary on it.

This covers the `CritC1AntiSuite` §2 T5 mutant set (`sibling-unrelated-name`,
`sibling-prefix-adjacent`, `sibling-dotdir`, `sibling-file`, `sibling-symlink`, control
`sibling-work-tolerated`), which the frozen H6 requires the suite's graded selftest case
to prove.

## 2. Files written

- The deliverable above.
- This receipt.
- Scratch only: `S=/fast/scratch/hyaku/kasegi-r40/ExecH6ScratchFixtures/` (matrix/transcript
  outputs, sandbox, a driver script), removed before yield — verified in §6.
No tracked lane file, fleet-root file, other lane, `/home/vgpnk/Projects/shokuknow`, or
`~/.local/bin` was written.

## 3. Runs (verbatim)

Driver (in scratch, all paths under `$S`; sandbox root and clean `--work` are siblings):

```
P=.ufo/waves/round-40/wave1/ExecH6ScratchFixtures.sibling-dir.sh   # absolute path used
SB=/fast/scratch/hyaku/kasegi-r40/ExecH6ScratchFixtures/sandbox
mkdir -p "$SB/scratch" "$SB/work"
```

### 3.1 RED — `kasegi-r39-stray/` + `kasegi-r40-stray/` present, `--work` clean

```
$ bash $P --check --scratch-root $SB/scratch --work $SB/work
H6 payload=r39=present,r40=present,work=outside,tolerated=none,strays=kasegi-r39-stray,kasegi-r40-stray,read=ok closed=0
closed=9/10 exit=1
exit=1
```

### 3.2 GREEN — same two dirs removed, same clean `--work`

```
$ rm -rf $SB/scratch/kasegi-r39-stray $SB/scratch/kasegi-r40-stray
$ bash $P --check --scratch-root $SB/scratch --work $SB/work
H6 payload=r39=absent,r40=absent,work=outside,tolerated=none,strays=none,read=ok closed=1
closed=10/10 exit=0
exit=0
```

### 3.3 The passed `--work` dir itself never reds — clean chain under a matching entry

```
$ mkdir -p $SB/scratch/kasegi-r40-seat/work
$ bash $P --check --scratch-root $SB/scratch --work $SB/scratch/kasegi-r40-seat/work
H6 payload=r39=absent,r40=empty,work=inside,tolerated=kasegi-r40-seat,strays=none,read=ok closed=1
closed=10/10 exit=0
exit=0
```

### 3.4 Contents inside `--work` (`export/`, `mut/`) never red

```
$ mkdir -p $SB/scratch/kasegi-r40-seat/work/export $SB/scratch/kasegi-r40-seat/work/mut
$ printf 'junk\n' > $SB/scratch/kasegi-r40-seat/work/export/file
$ bash $P --check --scratch-root $SB/scratch --work $SB/scratch/kasegi-r40-seat/work
H6 payload=r39=absent,r40=empty,work=inside,tolerated=kasegi-r40-seat,strays=none,read=ok closed=1
closed=10/10 exit=0
exit=0
```

### 3.5 Control — a real stray still reds while `--work` sits inside the root

```
$ mkdir -p $SB/scratch/kasegi-r39-l1
$ bash $P --check --scratch-root $SB/scratch --work $SB/scratch/kasegi-r40-seat/work
H6 payload=r39=present,r40=absent,work=inside,tolerated=kasegi-r40-seat,strays=kasegi-r39-l1,read=ok closed=0
closed=9/10 exit=1
exit=1
```

The driver's full raw output is the block in §3.1–§3.5 (29 lines, exit 0) plus
`== teardown == sandbox-removed=1`. The driver expanded `$P` to
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-40/wave1/ExecH6ScratchFixtures.sibling-dir.sh`
and `$SB` to `/fast/scratch/hyaku/kasegi-r40/ExecH6ScratchFixtures/sandbox`; its raw
capture (`transcript.out`, 29 lines) is byte-identical to these blocks.

## 4. Discrimination matrix (21 scenarios, verbatim)

Command: `bash $P --root $S/probe`; final line `probe scenarios=21 failures=0`, exit 0,
and `test ! -e $S/probe` printed `SANDBOX-CLEANED`.

```
probe mode=matrix scratch-root=/fast/scratch/hyaku/kasegi-r40/ExecH6ScratchFixtures/probe/scratch sandbox=/fast/scratch/hyaku/kasegi-r40/ExecH6ScratchFixtures/probe real-hyaku=/fast/scratch/hyaku real-root-read=no
probe policy=kasegi-r39*|kasegi-r40*,toleration=realpath-clean-chain,presence-is-red,unreadable-is-red

scenario=clean-work-outside expect=green
H6 payload=r39=absent,r40=absent,work=outside,tolerated=none,strays=none,read=ok closed=1
closed=10/10 exit=0
probe scenario=clean-work-outside expect=green got=green verdict=pass

scenario=stray-r39-present expect=red
H6 payload=r39=present,r40=absent,work=outside,tolerated=none,strays=kasegi-r39-stray,read=ok closed=0
closed=9/10 exit=1
probe scenario=stray-r39-present expect=red got=red verdict=pass

scenario=stray-r39-and-r40 expect=red
H6 payload=r39=present,r40=present,work=outside,tolerated=none,strays=kasegi-r39-stray,kasegi-r40-stray,read=ok closed=0
closed=9/10 exit=1
probe scenario=stray-r39-and-r40 expect=red got=red verdict=pass

scenario=strays-removed expect=green
H6 payload=r39=absent,r40=absent,work=outside,tolerated=none,strays=none,read=ok closed=1
closed=10/10 exit=0
probe scenario=strays-removed expect=green got=green verdict=pass

scenario=sibling-unrelated-name expect=red
H6 payload=r39=absent,r40=present,work=outside,tolerated=none,strays=kasegi-r40-build-extra,read=ok closed=0
closed=9/10 exit=1
probe scenario=sibling-unrelated-name expect=red got=red verdict=pass

scenario=sibling-prefix-adjacent expect=red
H6 payload=r39=absent,r40=present,work=outside,tolerated=none,strays=kasegi-r40x,read=ok closed=0
closed=9/10 exit=1
probe scenario=sibling-prefix-adjacent expect=red got=red verdict=pass

scenario=sibling-dotdir expect=red
H6 payload=r39=absent,r40=present,work=outside,tolerated=none,strays=.kasegi-r40-seat,read=ok closed=0
closed=9/10 exit=1
probe scenario=sibling-dotdir expect=red got=red verdict=pass

scenario=sibling-file expect=red
H6 payload=r39=absent,r40=present,work=outside,tolerated=none,strays=kasegi-r40-l1,read=ok closed=0
closed=9/10 exit=1
probe scenario=sibling-file expect=red got=red verdict=pass

scenario=sibling-symlink expect=red
H6 payload=r39=absent,r40=present,work=outside,tolerated=none,strays=kasegi-r40-seat,read=ok closed=0
closed=9/10 exit=1
probe scenario=sibling-symlink expect=red got=red verdict=pass

scenario=t5-mutants-cleared expect=green
H6 payload=r39=absent,r40=absent,work=outside,tolerated=none,strays=none,read=ok closed=1
closed=10/10 exit=0
probe scenario=t5-mutants-cleared expect=green got=green verdict=pass

scenario=work-inside-clean-chain expect=green
H6 payload=r39=absent,r40=empty,work=inside,tolerated=kasegi-r40-seat,strays=none,read=ok closed=1
closed=10/10 exit=0
probe scenario=work-inside-clean-chain expect=green got=green verdict=pass

scenario=work-chain-contaminated expect=red
H6 payload=r39=absent,r40=present,work=inside,tolerated=none,strays=kasegi-r40-seat,read=ok closed=0
closed=9/10 exit=1
probe scenario=work-chain-contaminated expect=red got=red verdict=pass

scenario=work-dir-contents-junk expect=green
H6 payload=r39=absent,r40=empty,work=inside,tolerated=kasegi-r40-seat,strays=none,read=ok closed=1
closed=10/10 exit=0
probe scenario=work-dir-contents-junk expect=green got=green verdict=pass

scenario=empty-stray-dir expect=red
H6 payload=r39=present,r40=absent,work=inside,tolerated=kasegi-r40-seat,strays=kasegi-r39-empty,read=ok closed=0
closed=9/10 exit=1
probe scenario=empty-stray-dir expect=red got=red verdict=pass

scenario=non-round-siblings-ignored expect=green
H6 payload=r39=absent,r40=empty,work=inside,tolerated=kasegi-r40-seat,strays=none,read=ok closed=1
closed=10/10 exit=0
probe scenario=non-round-siblings-ignored expect=green got=green verdict=pass

scenario=symlink-to-work-tolerated expect=green
H6 payload=r39=empty,r40=empty,work=inside,tolerated=kasegi-r39-link,kasegi-r40-seat,strays=none,read=ok closed=1
closed=10/10 exit=0
probe scenario=symlink-to-work-tolerated expect=green got=green verdict=pass

scenario=unreadable-stray expect=red
H6 payload=r39=absent,r40=present,work=inside,tolerated=kasegi-r40-seat,strays=kasegi-r40-locked,read=ok closed=0
closed=9/10 exit=1
probe scenario=unreadable-stray expect=red got=red verdict=pass

scenario=work-inside-unrelated-parent expect=green
H6 payload=r39=absent,r40=absent,work=inside,tolerated=none,strays=none,read=ok closed=1
closed=10/10 exit=0
probe scenario=work-inside-unrelated-parent expect=green got=green verdict=pass

scenario=final-clean expect=green
H6 payload=r39=absent,r40=absent,work=outside,tolerated=none,strays=none,read=ok closed=1
closed=10/10 exit=0
probe scenario=final-clean expect=green got=green verdict=pass

scenario=hermeticity-real-root expect=harness-error(exit2)
sibling-dir: hermeticity refusal: scratch root is the live host root (/fast/scratch/hyaku); use an isolated sandbox
rc=2
probe scenario=hermeticity-real-root expect=exit2 got=exit2 verdict=pass

scenario=hermeticity-root-ancestor expect=harness-error(exit2)
sibling-dir: hermeticity refusal: scratch root (/fast/scratch) contains the live host root; use an isolated sandbox
rc=2
probe scenario=hermeticity-root-ancestor expect=exit2 got=exit2 verdict=pass

probe scenarios=21 failures=0
probe exit=0
```

Default-sandbox mode was also exercised (`TMPDIR=$S/tmp bash $P`): exit 0,
`probe scenarios=21 failures=0`, and the `mktemp` sandbox was removed
(`find tmp -mindepth 1 | wc -l` = `0`).

## 5. Built suite status (why the probe equivalent)

At receipt time the round-40 suite was not present; the probe-equivalent path in the item
was used and is complete on its own.

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-26T21:24:01Z
$ ls .ufo/waves/round-40/wave1/ | grep -i ExecSuiteBuild
(no output, exit 1)
$ git status --porcelain -- corpus/instruments/r40-closure.sh
(no output)
$ ls corpus/instruments/ | grep r40
(no output, exit 1)
$ git rev-parse HEAD
5e985b74075dd3813a63d7750966bf8abf693465
```

What the L1 still needs from `ExecSuiteBuild` (out of this seat's write scope): the
committed `corpus/instruments/r40-closure.sh` with a graded `selftest case=H6` whose
mutants are the §4 scenarios and whose control is `work-inside-clean-chain` /
`symlink-to-work-tolerated`. When the suite lands, the same discrimination can be driven
end-to-end with, at Y:

```
bash corpus/instruments/r40-closure.sh --selftest --export-ref <Y> \
  --scratch-root <isolated-sandbox> --work <clean-dir-outside-the-root>
```

## 6. Controls / hygiene

- Disk guard green before and after (`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`):
  `/fast/scratch/hyaku` 28%, 586.1G free.
- No tool installed or upgraded; no network fetch; pacman not run.
- No mutating git/jj command anywhere; lane HEAD unchanged at
  `5e985b74075dd3813a63d7750966bf8abf693465`. `git status --porcelain` shows zero
  modified/untracked entries outside `.ufo/waves/round-40/`.
- Scratch removed before yield: `S=/fast/scratch/hyaku/kasegi-r40/ExecH6ScratchFixtures`
  deleted after copying evidence into this receipt; no `kasegi-r40/ExecH6ScratchFixtures`
  sibling survives from this seat.
- The probe never read or wrote `/fast/scratch/hyaku` at top level: it refuses that root
  and any ancestor of it (two refusal transcripts in §4), and its banner records
  `real-root-read=no`; all fixture state lived under `$S` and was deleted on exit
  (`sandbox-removed=1`, `SANDBOX-CLEANED`).

## 7. Risks / notes for the L1 and the suite

1. **Reference limb vs committed limb.** The probe is the reference implementation and the
   fixture set; the frozen predicate still requires the suite's own graded `selftest
   case=H6`. A suite that scans only the exact names `kasegi-r39`/`kasegi-r40` (the r39
   defect) passes this probe's r39/r40 directory cases but fails §4
   `sibling-unrelated-name`/`prefix-adjacent`/`dotdir`/`file`/`symlink`; the suite must
   adopt the prefix+dot+all-entry-types scan above.
2. **Default-root quiescence is an operational precondition, not a relaxation.** With the
   default root, any surviving seat dir under `kasegi-r40/` is a genuine stray by the
   frozen kill rule; the Y counting run therefore needs the root quiescent, or `--work`
   placed outside it / on a clean chain. `--selftest` must sandbox its scratch root (as
   this probe does) so the mutant limb does not depend on wave-time host state. The
   `tolerated=` payload intentionally differs between the isolated-selftest and
   default-root runs; H7's byte-identity requirement must compare re-runs with identical
   args, per `CritC1AntiSuite`'s determinism note.
3. **Entry-type coverage.** A `-type d`-only scan misses the frozen kill rule's
   "scratch entry" for regular files and dangling symlinks; presence must be RED for any
   entry type, and an unreadable entry/root must be `read=fail`, never silently zero.
4. **Scope boundary.** `kasegi-r41*` and unrelated names stay ignored (§4
   `non-round-siblings-ignored`); that is the frozen namespace, not a judgement that those
   entries are harmless.

Report: `.ufo/waves/round-40/wave1/ExecH6ScratchFixtures.md`
