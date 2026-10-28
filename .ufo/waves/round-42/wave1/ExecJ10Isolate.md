# ExecJ10Isolate — kasegi round 42, wave 1 (J10 graded-selftest isolation)

Seat: `ExecJ10Isolate` (leaf executor, no subagents, no swarm). Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` only; fleet root and
`/home/vgpnk/Projects/shokuknow` untouched. No git/jj mutation was run anywhere.

## Deliverables (written beside this receipt)

| file | lines | sha256 |
|---|---|---|
| `ExecJ10Isolate.sh` (sourceable limb, `check_j10`) | 627 | `a04f886bcda458ff223c6a595589b6841eb02a059f8f0c4e1d377d6baf14aa61` |
| `ExecJ10Isolate.notes.txt` (per-case directory grammar) | 166 | `31a514e9b5e7afc0601d5c96283b13f0e1c5d2320b60f7415582951667758c8f` |

`ExecJ10Isolate.sh` defines only functions and scalars at source time; sourcing it has no
side effects, and it never executes on source (`J10_VERSION`, `J10_MIN_CASES`,
`J10_SUITE_REL_DEFAULT` plus the `j10_*`/`check_j10` functions).

## Behaviour

`check_j10 TREE REF` is the J10 check of the r42 suite (same calling convention as the
round-41 `check_iN` limbs: payload on stdout, exit 0 closed / 1 open). It runs the suite's
own **graded selftest** under `strace` in a sandbox it owns and proves, from the syscall
trace alone, that the graded cases were isolated:

1. `j10_suite_path` resolves the suite under test inside the export tree
   (`J10_SUITE_REL`, default `corpus/instruments/r42-closure.sh`; `J10_SUITE_ABS` override).
2. The graded selftest is run as `bash <suite> --selftest --export-ref <REF> --work
   <sandbox>/work --scratch-root <sandbox>/scratch [--lane <lane>]` with `J10_NEST=1` on the
   child (leaf mode: the child's own `check_j10` is red by construction, so the recursion is
   finite — the round-41 `R41_DEPTH` pattern).
3. The trace (openat/open/creat, mkdir/mkdirat, chdir, rename, unlink, clone/fork/vfork,
   execve, write) is normalized by an embedded python3 analyzer which resolves relative
   paths through tracked `chdir` (coreutils `mkdir -p` chdir's into every component) and
   derives, per graded case: its private path set (component match on the case id,
   case-insensitive, component-boundary so `J1` never claims `J10`), its execution window,
   foreign reads of another case's paths, creations in the shared scratch root outside the
   case's own paths (the per-case scratch baseline diff), and whether the case ever read a
   real file under its own paths.
4. The scratch root is snapshotted before/after the traced run and diffed
   (`scratch-added`).
5. The analysis is cached under `<work>/j10-cache/<suite-digest-16>-<ref>` so the run phase
   and the selftest case pay for the traced selftest once. The payload contains counts only
   (no pids, no timestamps), so the receipt check can re-derive it.

Payload:

```
cases= found= missing= shared= precreated= unused= foreign= leaks= windows= mode= scratch-added=
```

Closed iff `cases>=2 && missing=0 && shared=0 && precreated=0 && unused=0 && foreign=0 &&
leaks=0`. Distinct reds instead of a vacuous green: `suite=0`, `tracer=0`, `sandbox=0`,
`tracer=failed`, `analysis=failed`, `nest=1`.

Knobs (documented in the limb header and the notes): `J10_NEST`, `J10_SUITE_REL`,
`J10_SUITE_ABS`, `J10_WORK`, `J10_SCRATCH_ROOT`, `J10_LANE`, `J10_DETAIL`.

## Evidence (commands run and their actual output)

### 1. Syntax and sourceability

```
$ bash -n ExecJ10Isolate.sh && echo "syntax OK"
syntax OK
```

### 2. Defeat matrix — two-case reference harness (J1, J2), real execution

The reference harness is scratch-only (never shipped): it implements the grammar
(`<work>/cases/<ID>/`) and takes `MUTANT=clean|foreign|leak|unused|samedir` and
`MUTANT_SHARED=0|1` to inject each defeat class. `bash ev/run.sh` output:

```
case shared=0 mutant=none     exit=0
  payload=cases=2,found=2,missing=0,shared=0,precreated=0,unused=0,foreign=0,leaks=0,windows=2,mode=proc,scratch-added=0
  case=J1 dirs=$S/ev/0-none/work/j10-sandbox/work/cases/J1 window=58..94 read-own=yes
  case=J2 dirs=$S/ev/0-none/work/j10-sandbox/work/cases/J2 window=94..114 read-own=yes
case shared=0 mutant=foreign  exit=1
  payload=cases=2,found=2,missing=0,shared=0,precreated=0,unused=0,foreign=1,leaks=0,windows=2,mode=proc,scratch-added=0
  foreign case=J2 other=J1 op=read path=$S/ev/0-foreign/work/j10-sandbox/work/cases/J1/tree/marker.txt
case shared=0 mutant=leak     exit=1
  payload=cases=2,found=2,missing=0,shared=0,precreated=0,unused=0,foreign=0,leaks=1,windows=2,mode=proc,scratch-added=1
  leak case=J2 op=create path=$S/ev/0-leak/scratch/j10-3906033/leak-from-J2.txt
case shared=0 mutant=unused   exit=1
  payload=cases=2,found=2,missing=0,shared=0,precreated=0,unused=1,foreign=0,leaks=0,windows=2,mode=proc,scratch-added=0
  case=J2 ... window=94..98 read-own=no
case shared=0 mutant=samedir  exit=1
  payload=cases=2,found=1,missing=1,shared=0,precreated=0,unused=1,foreign=0,leaks=0,windows=1,mode=proc,scratch-added=0
case shared=1 mutant=none     exit=0
  payload=cases=2,found=2,missing=0,shared=0,precreated=0,unused=0,foreign=0,leaks=0,windows=2,mode=shared,scratch-added=0
case shared=1 mutant=foreign  exit=1
  payload=...foreign=1...mode=shared...
case shared=1 mutant=leak     exit=1
  payload=...leaks=1...scratch-added=1...mode=shared...
```

The clean run is the requested **isolation proof over two cases**: J1's window `58..94` and
J2's window `94..114` are disjoint, each case read under its own directory only
(`read-own=yes`), no foreign touch, no scratch leak. The same two cases with a single
injected cross-read (`foreign case=J2 other=J1`) or a single injected scratch write
(`leak case=J2 ...`) are rejected, which is what makes the clean result non-vacuous.

### 3. Negative controls (never a vacuous green)

```
$ J10_SUITE_ABS=<absent> check_j10 "" ""
suite=0,cases=0,...,mode=none,scratch-added=0                    rc=1
$ (unset J10_WORK J10_SCRATCH_ROOT WORK SCRATCH_ROOT; check_j10 "" "")
sandbox=0,cases=0,...,mode=none,scratch-added=0                  rc=1
$ J10_NEST=1 check_j10 "" ""
nest=1,cases=0,...,mode=none,scratch-added=0                     rc=1
```

### 4. Determinism (payload must be re-derivable by the receipt check)

```
$ a=$(check_j10 "" ""); ra=$?; b=$(check_j10 "" ""); rb=$?
DETERMINISTIC rc=0 payload=cases=2,found=2,missing=0,shared=0,precreated=0,unused=0,foreign=0,leaks=0,windows=2,mode=proc,scratch-added=0
```

### 5. Real instrument — the round-41 suite, from a real captured trace

The r41 suite at its judged head `1f7464612ac4c44e39886b82e812610d3c039b13` was exported to
scratch and its graded selftest was traced with exactly the syscall set the limb uses
(`openat,open,creat,mkdir,mkdirat,chdir,rename,renameat,unlink,unlinkat,clone,clone3,fork,vfork,execve,write`),
then analysed by the limb's own embedded analyzer:

```
$ strace -f -qq -s 256 -e trace=openat,open,creat,mkdir,mkdirat,chdir,rename,renameat,unlink,unlinkat,clone,clone3,fork,vfork,execve,write \
    -o narrow.log -- bash <export>/corpus/instruments/r41-closure.sh --selftest \
       --export-ref 1f7464612ac4c44e39886b82e812610d3c039b13 --lane <lane> \
       --work <sbx>/work --scratch-root <sbx>/scratch
real 4m14.685s   rc=0   209M narrow.log   59 lines of graded output
$ python3 analyze7.py narrow.log ids41.txt <sbx>/work <sbx>/scratch detail.txt
cases=12 found=11 missing=1 shared=0 precreated=3 foreign=0 leaks=0 unused=4 windows=11 mode=shared
```

Read: on a real 12-case graded selftest the limb finds **no foreign read and no leak** — it
does not manufacture defects — while it does name the three r41 cases whose fixtures are
built during the payload phase (`precreated=3`) and the one case that owns no id-carrying
path (`missing=1`, r41's I10, whose fixture is `$WORK/neg-*`). r41 therefore does not
satisfy the round-42 grammar, which is exactly what the grammar check reports; the r42 suite
must materialise each case's fixture inside its own case (G5 in the notes).

The same instrument end-to-end through the limb itself (not just its analyzer):

```
$ J10_SUITE_REL=corpus/instruments/r41-closure.sh J10_WORK=<sbx>/work \
  J10_SCRATCH_ROOT=<sbx>/scratch check_j10 <export> 1f7464612ac4c44e39886b82e812610d3c039b13
rc=1
payload=cases=12,found=11,missing=1,shared=0,precreated=3,unused=5,foreign=0,leaks=0,windows=11,mode=shared,scratch-added=0
real 6m57.735s
```

A third, independent shape was also exercised: a three-case harness using r41 house style
(`<work>/mut/<ID>-fixture`, one verdict write per case) yields
`cases=3 found=3 missing=0 shared=0 precreated=0 unused=0 foreign=0 leaks=0 windows=3 mode=shared`
clean, `foreign=1` for an injected cross-read and `leaks=1` for an injected scratch write —
the component-boundary rule accepts labelled directories and the verdict writes give exact
per-case windows.

## Risks and blockers

- **Cost.** J10 runs the suite's graded selftest once under `strace`. Measured on the
  round-41 instrument: 4m14s for the bare traced run (209 MB trace, narrow syscall set; a
  `%file` trace is ~368 MB and slower) and 6m58s end-to-end through `check_j10` including
  sandbox setup and the analysis. The result is cached per (suite digest, ref), so a suite run
  plus its selftest case pay once, not twice. If the L1's r42 suite selftest is heavier than
  r41's, this grows proportionally; the traced run is the suite's own cost plus strace
  overhead, not an independent workload.
- **Integration contract.** The limb defines the grammar the r42 suite must satisfy (notes
  §2, G1–G5: per-case path carrying the case id, fixture materialised inside the case,
  reads confined to own paths, no scratch-root writes outside own paths, own fixture
  actually read). The suite author (ExecSuiteCore) must adopt it; a suite that names its
  per-case dirs without the case id, or pre-creates them in a setup phase, is red — by
  design, because those cases cannot be attributed.
- **`strace -P` is unusable in this build** (7.2): it filters out the accesses it is asked to
  keep. The limb therefore traces the narrow syscall set unconditionally and filters in the
  analyzer; that is why the r41 capture is 209 MB.
- **`mkdir -p` emits relative paths** (coreutils chdir's per component). The analyzer tracks
  `chdir`/`chdir` inheritance across `clone` and resolves every path; a naive trace reader
  mis-places them. Covered by the reference harness (which uses absolute paths) plus the
  r41 run (whose fixtures are created by `cp -p`/`mkdir -p` chains).
- **The r42 suite does not exist yet**, so J10 cannot be graded against it in this wave.
  Everything above is the limb exercised against a reference harness and the round-41
  instrument; the L1 integrates `check_j10` into `corpus/instruments/r42-closure.sh` and
  runs it at the judged head.
- Disk guard was green for every run (`bash scripts/hyaku/disk-guard.sh status` at start:
  `/fast/scratch/hyaku 27%`). No tool was installed or upgraded; `strace 7.2`,
  `python3 3.14`, `bash 5.3.20` were already present.

## Scratch

All work was bound to `/fast/scratch/hyaku/kasegi-r42/ExecJ10Isolate` (`mkdir -p` at start;
every sandbox, trace and harness lived under it). Removed after the deliverables were
copied into the wave dir:

```
$ rm -rf /fast/scratch/hyaku/kasegi-r42/ExecJ10Isolate
$ [ -e /fast/scratch/hyaku/kasegi-r42/ExecJ10Isolate ] && echo NO || echo YES
YES
```

## Write scope

Written: `ExecJ10Isolate.sh`, `ExecJ10Isolate.notes.txt` and this receipt, all in
`.ufo/waves/round-42/wave1/`. No tracked lane file, no fleet-root file and no
`/home/vgpnk/Projects/shokuknow` file was created or modified. The other modified/untracked
paths visible in the lane repo belong to sibling wave-1 seats working concurrently
(`LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `corpus/*`, other
`wave1/*` deliverables); none was touched by this seat.

Report: .ufo/waves/round-42/wave1/ExecJ10Isolate.md
