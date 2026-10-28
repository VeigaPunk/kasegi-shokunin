# ScoutQuiescenceScan — scratch-discipline audit

Axes: depth:verifiability, coverage. Rule: `.ufo/prompts/kasegi-round-43.md` §7.4 (fleet prompt, read-only). Frozen claims read; not edited. No tool install. No network fetch.

## Verdict

No committed live instrument contains `mkdtemp(dir="/tmp")` or a literal `/tmp/<name>.XXXX` token. Two live counters still **write under `/tmp` when `TMPDIR` is unset**, and one of them does so **even when `--work` is set**. Those two are the routed defects for a frozen-counter amendment **next round, not this one**. Nothing here was edited.

1. `corpus/instruments/r42-closure.sh:74-83` — default scratch root is `${TMPDIR:-/tmp}`. It always `mkdir -p "$SCRATCH_ROOT/r42-<12 hex>"`. `--work` moves the export but does **not** stop that mkdir. `--scratch-root` and `TMPDIR` do redirect it. The directory is never removed. Eight empty `/tmp/r42-<rev>` directories on this host are that mkdir.
2. `corpus/instruments/r-defect-closure.sh:461` — plain-run R9 limb does `mktemp -d "${TMPDIR:-/tmp}/rdc-r9.XXXXXX"`. That expands to the named `/tmp/rdc-r9.XXXXXX` shape when `TMPDIR` is unset (measured). `--scratch` is ignored by this limb. `TMPDIR` is honoured. The dir is `rm -rf`'d before return, not via a trap.

`corpus/instruments/` at HEAD `4cb6d4ae768481e1a14afbedc2d865a060ebacfd` is byte-identical to base `ab98fac9dce87130bc4f66de89e30650d63943dc` (`git diff --stat` empty). Base is an ancestor of HEAD.

## Rule applied

§7.4: a counter, probe or gate that writes under `/tmp` regardless of `TMPDIR`/`--work` (`mkdtemp(dir="/tmp")`, `/tmp/<name>.XXXX` roots) is a routed defect this round and a frozen-counter amendment next round. Counters must honour `TMPDIR` and accept a scratch argument.

"Regardless of TMPDIR" is reserved for a root that stays `/tmp` when `TMPDIR` is set. None of the live instruments do that. The two calls above are the default-`/tmp` class: they honour `TMPDIR` and still land on `/tmp` when it is unset, which is the failure §7 exists to stop ("never rely on an inherited TMPDIR").

## Corpus scanned

Live set: `git ls-files 'corpus/instruments/*.py' 'corpus/instruments/*.sh'` — 23 files. Also scanned 616 tracked `*.py`/`*.sh`. Strict regex `dir\s*=\s*['\"]/tmp['\"]` or `/tmp/<token>.X+` matched **0** files. The R9 template is not a literal `/tmp/` prefix (`/tmp}` sits between), so the regex misses it; the shell expansion does not.

## Live write sites

Honour columns are from the source plus the probes below. "platform" means CPython `tempfile` with `dir` omitted: measured to follow `TMPDIR`, and measured to ignore `TMPDIR` when `dir=` is passed.

| file:line | what it does | TMPDIR | scratch arg | routed? |
|---|---|---|---|---|
| `r42-closure.sh:74-83` | `SCRATCH_ROOT=${TMPDIR:-/tmp}`; `mkdir -p $SCRATCH_ROOT/r42-$rev`; `--work` else that dir holds the export | yes | `--scratch-root` and `--work` (mkdir ignores `--work`) | **yes — default /tmp; `--work` does not suppress the mkdir; not removed** |
| `r-defect-closure.sh:461` | plain-run R9: `mktemp -d ${TMPDIR:-/tmp}/rdc-r9.XXXXXX`; `rm -rf` at `:482` | yes | `--scratch` exists (`:115-117`) but this limb does not read `SCRATCH_ARG` | **yes — `/tmp/<name>.XXXXXX` when TMPDIR unset; ignores `--scratch`** |
| `r-defect-closure.sh:750,755` | selftest base `${SCRATCH_ARG:-${HYAKU_SCRATCH:-${TMPDIR:-/tmp}}}` then `mktemp -d $base/r-defect-closure-selftest.XXXXXX`; trap EXIT | yes | `--scratch` | no (honours the arg) |
| `r35-defect-closure.sh:114,643,647` | selftest only: `${KASEGI_SCRATCH:-${TMPDIR:-/tmp}}/r35-closure.XXXXXX`; `trap RETURN` | yes | no CLI arg; env `KASEGI_SCRATCH` only | no — clause-B gap (no scratch argument), not a regardless-of-TMPDIR write |
| `r36-closure.sh:218` | no `--work`: `mktemp -d -t r36-closure.XXXXXXXX` | yes (mktemp) | `--work`, `--scratch-root` | no |
| `r37-closure.sh:287` | same, `r37-closure.XXXXXXXX` | yes | `--work`, `--scratch-root` | no |
| `r38-closure.sh:259` | same, `r38-closure.XXXXXXXX` | yes | `--work`, `--scratch-root` | no |
| `r39-closure.sh:307` | same, `r39-closure.XXXXXXXX` | yes | `--work`, `--scratch-root` | no |
| `r40-closure.sh:293` | same, `r40-closure.XXXXXXXX` | yes | `--work`, `--scratch-root` | no |
| `r41-closure.sh:359` | same, `r41-closure.XXXXXXXX`; no `/tmp` token in the file | yes | `--work`, `--scratch-root` | no |
| `r36-closure.sh:128` | default **scan** root `/fast/scratch/hyaku/kasegi-r36` (read, not a write) | n/a | `--scratch-root` | no |
| `r37-closure.sh:185` | default scan root `/fast/scratch/hyaku/kasegi-r37` | n/a | `--scratch-root` | no |
| `r38-closure.sh:156`, `r39:196`, `r40:164`, `r41:234` | default scan root `/fast/scratch/hyaku` | n/a | `--scratch-root` | no |
| `capture-binding-check.py:1051-1061,1114` | `--scratch`, else `$HYAKU_SCRATCH`, else `$TMPDIR`, else `/fast/scratch/hyaku` if present, else `gettempdir()`; `mkdtemp(dir=base)` | yes | `--scratch` | no |
| `frontier-recheck-count.py:447-458,498` | same ladder | yes | `--scratch` | no |
| `kill-rule-check.py:387-392,423,722` | same ladder; child env sets `TMPDIR` to the scratch dir | yes | `--scratch` | no |
| `anchorcheck.py:299` | selftest `mkdtemp(prefix='anchorcheck-selftest-')` | yes (platform) | none | no — clause-B gap, selftest only |
| `capture-source.py:60` | PDF path: `NamedTemporaryFile` (production, not only selftest); unlinked in `finally` | yes (platform) | none | no — clause-B gap; not a hardcoded `/tmp` |
| `capture-source.py:102` | selftest `mkdtemp`; `rmtree` in `finally` | yes (platform) | none | no |
| `limb-mutation-check.py:260` | measurement `mkdtemp(prefix='limb-mutation-')` copies `corpus/` | yes (platform) | none | no — clause-B gap; can be large; not hardcoded `/tmp` |
| `limb-mutation-check.py:599,619` | selftest `TemporaryDirectory` | yes (platform) | none | no |
| `mirror-containment-check.py:161` | per case `mkdtemp(prefix='kasegi-r23-c1-')` | yes (platform) | none | no — clause-B gap |
| `resolve-dispatch-check.py:214` | per case `mkdtemp(prefix='kasegi-r24-c1-')` | yes (platform) | none | no — clause-B gap |
| `recheck-audit.py:201` | selftest `TemporaryDirectory()` | yes (platform) | none | no |
| `score-gap.py:462` | selftest `TemporaryDirectory`; docstring `:15` says `mkdtemp` | yes (platform) | none | no |
| `source-recheck.py:262` | selftest `TemporaryDirectory` | yes (platform) | none | no |
| `test_resolve.py:34,67` | `mkdtemp(dir=HERE)` with `HERE` = the instruments directory | **no — `dir=` wins** | none | **not a §7.4 /tmp defect.** Ignores TMPDIR by pinning the fixture inside `corpus/instruments/`. In-tree, removed at teardown. |

## Non-write `/tmp` mentions (not defects)

- `density.py:6-7`, `resolve.py:10`, `resolve.py:43`, `resolve.py:446`, `README.md:4` and `:31` — historical path citations.
- `citation-survival.md` / `citation-survival.tsv` — census rows whose text contains `/tmp/kasegi-r1*`.
- `recheck-audit.py:216` — the characters `cd /tmp &&` are fixture **text** written inside the selftest temp dir, not a `cd` the tool performs.
- `limb-ledger.json:42` — note that a fixture command `cd /tmp` is how the cdroot limb is isolated.

## Why r42 is the amendment

`r42-closure.sh:74-83` (live bytes):

```
if [ -z "$SCRATCH_ROOT" ]; then
    SCRATCH_ROOT="${TMPDIR:-/tmp}"
fi
mkdir -p -- "$SCRATCH_ROOT"
SUITE_SCRATCH="$SCRATCH_ROOT/r42-${RESOLVED:0:12}"
mkdir -p -- "$SUITE_SCRATCH"
if [ -z "$WORK" ]; then
    WORK="$SUITE_SCRATCH/work"
fi
```

No later `rm` of `SUITE_SCRATCH` (the only `rm -rf` of a work path at `:86` clears `$EXPORT` before refill). A caller who passes `--work` and neither `--scratch-root` nor `TMPDIR` still creates `/tmp/r42-<rev>/`. A caller who passes neither leaves the git-archive export at `/tmp/r42-<rev>/work`.

The same four lines are in the landed draft `.ufo/waves/round-42/wave1/ExecSuiteCore.r42-closure.sh:74-78`. That file is not the executing counter; `corpus/instruments/r42-closure.sh` is.

## Historical wave scripts (same fallback, not live counters)

Committed `.sh` under `.ufo/waves/` that use `${TMPDIR:-/tmp}/<name>.XXXXXX` or assign scratch to `${TMPDIR:-/tmp}`. Each honours `TMPDIR`. None is `dir="/tmp"`. They are not what the closure suite execs. Listed so a later grep does not look like a miss:

- `round-38/wave1/ExecFenceWalk.sh:71`
- `round-38/wave1/ExecNoHarm.sh:107`
- `round-39/wave1/ExecPinnedG8Fixture.fixtures/g8-pinned-check.sh:56`
- `round-39/wave1/ExecWholeTailFixture.fixtures/g1-check.sh:125` (honours `--work`; default is the fallback)
- `round-40/wave1/ExecH6ScratchFixtures.sibling-dir.sh:417`
- `round-40/wave1/ExecH9DeclaredBlocks.validator.sh:256` and `:272`
- `round-40/wave2/CritKillRule.h6-escapes.sh:55`
- `round-40/wave2/CritKillRule.worktree-clean.sh:15`
- `round-41/wave1/ExecI3Token.sh:234`
- `round-41/wave1/ExecI4Fence.sh:190`
- `round-41/wave1/ExecI5Blocks.sh:563`
- `round-41/wave1/ExecI6Scan.sh:241` and `:363`
- `round-42/wave1/ExecJ2Token.sh:658` (only when `J2_WORK` is empty)
- `round-42/wave1/ExecJ4Decl.sh:255` (`J4_SCRATCH=${TMPDIR:-/tmp}` then `mkdir -p`)
- `round-42/wave1/ExecJ5Scan.sh:263`, `:373`, `:564`
- `round-42/wave1/ExecJ9NegCtl.sh:649`
- `round-42/wave1/ExecReplayHarness.sh:63,911` (`REPLAY_SCRATCH` else the fallback)

Quoted past commands inside markdown receipts (`mktemp -d /tmp/....XXXXXX`, for example `round-23/build/CraVuln.md:198` and several round-31 receipts) are not executables. Not classified as counters.

## `/fast/scratch/hyaku/kasegi-r4*`

The glob matches **one** directory: `/fast/scratch/hyaku/kasegi-r43`. There is no `kasegi-r40`, `kasegi-r41`, or `kasegi-r42` under `/fast/scratch/hyaku`. `kasegi-r43` is this round's live scratch (disk-guard `idle=0`), not a closed-round leftover. §7.2 says the L1 removes it after landing. Deleting it during the wave would destroy sibling seat work.

Sizes of that one directory, three commands, same seat, in order:

- `disk-guard.sh status` top consumer: `11.4G idle=0 /fast/scratch/hyaku/kasegi-r43`
- first `du -sh /fast/scratch/hyaku/kasegi-r43`: `12G`
- later `du -sh /fast/scratch/hyaku/kasegi-r43`: `59G`

The tree grew while other seats exported. It is not quiescent.

## `/tmp` leftovers (not in the asked glob; disk-guard plus `ls`/`du`)

These are the prior-round leftovers the `/fast/scratch` glob does not see. Sizes for the two large trees are the disk-guard figures (not re-walked). Small ones were `du -sh`'d.

| path | size | note |
|---|---|---|
| `/tmp/kasegi-r42-judge` | 61.5G, idle=55 | disk-guard top `/tmp` consumer; mtime Oct 28 12:44 |
| `/tmp/verif-kasegi-r42` | 25.4G, idle=11 | disk-guard; mtime Oct 28 13:28 |
| `/tmp/kasegi-forge` | 170.5M, idle=70 | disk-guard; mtime Oct 28 12:30 |
| `/tmp/kasegi-r40-draft` | 52K | `du`; mtime Oct 26 19:33 |
| `/tmp/kasegi-r42-closure.json` | 8.0K | file, not a tree |
| `/tmp/r42-1f7464612ac4` | 0 | empty dir, 0 children |
| `/tmp/r42-401091127a0b` | 0 | empty |
| `/tmp/r42-42ade5f01864` | 0 | empty |
| `/tmp/r42-5053a7f46de3` | 0 | empty |
| `/tmp/r42-857cac442862` | 0 | empty |
| `/tmp/r42-95bd935ffbfb` | 0 | empty |
| `/tmp/r42-b2c49ea5e7bc` | 0 | empty |
| `/tmp/r42-dfbbbeaf2b45` | 0 | empty |

`find /tmp/r42-* -mindepth 1 | wc -l` printed `0`. Those eight names are `r42-` plus 12 hex digits, which is `SUITE_SCRATCH` at `r42-closure.sh:78`.

## Disk-guard status

Command: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`

The script printed the table below and no separate verdict word. Use is far under the §7.5 90% reaper line. No ENOSPC.

```
root                             use%     free
/tmp                              17%   106.8G
/var/tmp                          38%   557.1G
/fast/scratch/hyaku               25%   604.2G

top consumers /tmp
     61.5G  idle=55  /tmp/kasegi-r42-judge
     25.4G  idle=11  /tmp/verif-kasegi-r42
    420.3M idle=1266  /tmp/k57
    410.7M idle=1266  /tmp/k57b
    367.3M idle=3097  /tmp/.mount_KimiCogEAx7f
    367.3M idle=7792  /tmp/.mount_KimiColz3RmH
    366.2M idle=846  /tmp/.mount_Grok_BucXQt4
    363.9M idle=275  /tmp/self-assessment-census-fm_ny_gu
    304.1M idle=1753  /tmp/r57a8d
    207.4M idle=302  /tmp/g24probe
    196.0M idle=998  /tmp/s05dbg
    187.6M idle=1377  /tmp/k72-tip-spumbf__
    187.0M idle=1381  /tmp/k76-b28-c2-mz94vv3_
    187.0M idle=1381  /tmp/k76-b28-c2-0uaxs7lr
    170.5M  idle=70  /tmp/kasegi-forge

top consumers /var/tmp
    201.8M idle=2853  /var/tmp/souji-r21-replay-eq45dano
     11.6M idle=2854  /var/tmp/r15-census-config.3tk6qehq
     10.3M idle=2844  /var/tmp/r15-census-config.psjsbayp
      9.8M idle=2856  /var/tmp/r15-census-config.xec8q0wl
      7.1M idle=2853  /var/tmp/r17-census-hygiene._ke3xywa
      2.1M idle=1713  /var/tmp/souji-census-selftest.XXl2r7
      1.6M idle=292  /var/tmp/souji-census-selftest.uFAiOl
      1.1M idle=2853  /var/tmp/souji-r18-FixtureR18Bounded.6bewdtxp
      1.1M idle=2714  /var/tmp/souji-r18-FixtureR18Bounded.du6kpc_5
      720K idle=2853  /var/tmp/souji-r16-lgfixture-vnbltez6
      104K   idle=0  /var/tmp/disk-guard.dmlDi0
       60K idle=1391  /var/tmp/disk-guard.J8dd4N
        8K  idle=16  /var/tmp/souji-r37-closure.json
        4K idle=1739  /var/tmp/souji-r34-recon.k8WP2k
        4K idle=1739  /var/tmp/souji-r34-recon.133mcm

top consumers /fast/scratch/hyaku
     11.4G   idle=0  /fast/scratch/hyaku/kasegi-r43
      3.7G   idle=7  /fast/scratch/hyaku/mori-r60
    507.2M   idle=0  /fast/scratch/hyaku/souji-r38
    503.8M   idle=4  /fast/scratch/hyaku/tameshi-r55
    188.9M  idle=80  /fast/scratch/hyaku/souji-r36
      3.8M  idle=11  /fast/scratch/hyaku/kaidoku-r45
      268K  idle=26  /fast/scratch/hyaku/souji-r37
      240K  idle=22  /fast/scratch/hyaku/tameshi-r48
      104K idle=114  /fast/scratch/hyaku/kaidoku-r44
        0K  idle=15  /fast/scratch/hyaku/tabi-r42
        0K  idle=37  /fast/scratch/hyaku/souji-r30
        0K idle=132  /fast/scratch/hyaku/hyaku
```

`df -h` at the same pass: `/tmp` 128G, 22G used, 107G avail, 17%; `/fast` 804G, 200G used, 605G avail, 25%.

## Probes (measured, not inferred)

Scratch for the probes: `/fast/scratch/hyaku/kasegi-r43/ScoutQuiescenceScan/probe` (removed before yield).

Python `mkdtemp()` with `TMPDIR` set and no `dir=`:

```
path=/fast/scratch/hyaku/kasegi-r43/ScoutQuiescenceScan/probe/other/honour-m3mpm2_2
startswith_tmpdir=True
```

Same `TMPDIR`, `dir=` pointed at a different directory:

```
path=/fast/scratch/hyaku/kasegi-r43/ScoutQuiescenceScan/probe/parent/forced-oeemg3pp
startswith_dir=True
startswith_tmpdir=False
```

So a missing `dir=` honours `TMPDIR`, and `dir="/tmp"` would not. No live file passes `dir="/tmp"`.

Shell expansion of the R9 template:

```
unset=/tmp/rdc-r9.XXXXXX
set=/fast/scratch/hyaku/kasegi-r43/ScoutQuiescenceScan/probe/other/rdc-r9.XXXXXX
```

Transcription of the r42 default (the four assignments only; the suite was not executed):

```
neither: scratch=/tmp suite=/tmp/r42-deadbeefdead work_default=/tmp/r42-deadbeefdead/work
work-only: scratch=/tmp suite=/tmp/r42-deadbeefdead work=/fast/scratch/hyaku/kasegi-r43/ScoutQuiescenceScan/probe/work
tmpdir-only: scratch=/fast/scratch/hyaku/kasegi-r43/ScoutQuiescenceScan/probe/other suite=.../other/r42-deadbeefdead
```

## Amendment next round (not done here)

Frozen-counter amendment, not a round-43 edit:

- `r42-closure.sh`: do not default `SCRATCH_ROOT` to `/tmp`. Require `--scratch-root` or default it to `$HYAKU_SCRATCH`. Do not `mkdir` `SUITE_SCRATCH` when `--work` is set unless a scratch root was asked for. Remove the suite scratch on exit. The eight empty `/tmp/r42-*` dirs are the current residue.
- `r-defect-closure.sh` `check_r9`: build the temp dir under `SCRATCH_ARG` / `$HYAKU_SCRATCH` / `$TMPDIR`, and `trap` the removal. Do not use `${TMPDIR:-/tmp}/rdc-r9.XXXXXX`.
- Clause-B gaps (honour `TMPDIR`, no scratch argument): `limb-mutation-check.py:260`, `mirror-containment-check.py:161`, `resolve-dispatch-check.py:214`, `capture-source.py:60`. Not the `/tmp/<name>.XXXX` shape. `test_resolve.py:67` is the opposite problem (fixture pinned inside the tree).

## Tooling

No install. Host `git`, `python3`, `bash`, `find`, `du`, `df`, and `scripts/hyaku/disk-guard.sh` only.

## Seal

Body above this section: 252 lines, sha256 `467740a7e6566e39539b2f7516eff10b41e91b97330bafa62d7eeea7f967c39d`. This seat's scratch dir was removed before the seal (`scratch-removed`).
