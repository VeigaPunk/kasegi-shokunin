# ExecDiskGuardProbe — round 39 (kasegi-r39-build)

Seat: `ExecDiskGuardProbe` (executor, leaf). Axis: `depth:verifiability` (G6 grounding).
Item: disk-guard status + free space; enumerate live scratch under `kasegi-r3[6-9]` and classify
this wave's own work vs leftovers.

Deliverable: `.ufo/waves/round-39/wave1/ExecDiskGuardProbe.disk.txt` — 150 lines, 11062 bytes,
`sha256=8ea7e8d78aa6cbe8780f31785148203bc30808246974786e3749c4d9a8a459cc`.

## Verdict

Disk guard **green** (both `status` and `check` exit 0; `/tmp` 3 %, `/var/tmp` 35 %,
`/fast/scratch/hyaku` 24 % against SOFT_PCT=70). `kasegi-r36`/`r37`/`r38` **absent**.
`kasegi-r39` holds 35 roster seat dirs plus this probe — this wave's own `--work`, all younger than
IDLE_MIN=45, **0 unreadable**. Two entries need owner action before filing: `RevControls-2`
(non-roster name, this wave's work) and the sibling root `kasegi-r39-l1` (L1's own scratch, not
covered by `purge-lane kasegi 39`).

## Evidence (commands and actual output)

Guard, thresholds from `scripts/hyaku/hyaku.env` (`SOFT_PCT=70 TARGET_PCT=60 HARD_PCT=90
IDLE_MIN=45 MIN_AGE_MIN=10`, roots `/tmp /var/tmp /fast/scratch/hyaku`):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh check
ok root=/tmp use=3% soft=70%
ok root=/var/tmp use=35% soft=70%
ok root=/fast/scratch/hyaku use=24% soft=70%
check_exit=0
```

`disk-guard.sh status` (19:33:32Z) exit 0 — table and top consumers verbatim in the deliverable §A:

```
root                             use%     free
/tmp                               3%   125.2G
/var/tmp                          35%   585.6G
/fast/scratch/hyaku               24%   615.6G
```

Final free space (19:34:13Z):

```
$ df -h /fast/scratch/hyaku /tmp /home
Filesystem        Size  Used Avail Use% Mounted on
/dev/nvme1n1p2    804G  185G  619G  24% /fast
/dev/nvme1n1p1    128G  2.7G  126G   3% /tmp
/dev/mapper/root  930G  310G  586G  35% /home
```

Scratch roots:

```
$ for d in kasegi-r36 kasegi-r37 kasegi-r38; do test -e /fast/scratch/hyaku/$d && echo "$d PRESENT" || echo "$d absent (test -e false)"; done
kasegi-r36 absent (test -e false)
kasegi-r37 absent (test -e false)
kasegi-r38 absent (test -e false)

$ ls -1d /fast/scratch/hyaku/kasegi-r3[6-9]*
/fast/scratch/hyaku/kasegi-r39
/fast/scratch/hyaku/kasegi-r39-l1
```

Per-entry snapshot (`kasegi-r39`, 19:33:32Z): `entries=37 size_mb=1139 wave_seats=35 self=1
nonroster=1`. Read test (dirs `R_OK|X_OK`): `unreadable=0` across all 37 entries; same at 19:34:13Z.

`RevControls-2` identification:

```
$ ls -1A /fast/scratch/hyaku/kasegi-r39/RevControls-2
base
$ ls -1A /fast/scratch/hyaku/kasegi-r39/RevControls-2/base | head -12
.gitignore  .ufo  AGENTS.md  LOG.md  PROVINCE.md  README.md  SCORECARD.md  SHONEN.md  SKILL.md
c2-controls  considerthese  corpus
$ ls -d .../RevControls-2/base/corpus .../RevControls-2/base/.ufo
.../base/.ufo
.../base/corpus
$ ls -ld /fast/scratch/hyaku/kasegi-r39/RevControls
ls: cannot access '/fast/scratch/hyaku/kasegi-r39/RevControls': No such file or directory
```

Roster and dispatch both name only `RevControls` (`wave1/swarm-registry.json` has 49 members
including `RevControls`; `grep -o 'RevControls[-A-Za-z0-9]*' wave1-dispatch.json` returns only
`RevControls`, task index 37, whose scratch instruction reads
`S=/fast/scratch/hyaku/kasegi-r39/<SEATNAME>/` and whose `Report:` is
`.ufo/waves/round-39/wave1/RevControls.md`).

Sibling root: `kasegi-r39-l1` entries=8 size_mb=1
(`integration-check.sh integration-checklist.md landed-texts.md lesson-draft.md
make-declared-blocks.sh make-receipt.sh report-draft.md report-full.md`), all mode 0644/0755.
`purge-lane` targets `target="$HYAKU_SCRATCH/${lane}-r${round}"` — exactly
`/fast/scratch/hyaku/kasegi-r39` — so this root is not purged by it.

## Findings

**F1 — G6's first two clauses already hold.** `kasegi-r37` and `kasegi-r38` are absent (strict
`test -e`, not a glob miss). Nothing to clean for either round; the check's absent-or-empty arm is
satisfied today and stays satisfied unless someone writes those paths.

**F2 — `kasegi-r39` content is this wave's own work.** 35 entries are names in the 49-seat
registry (so `depth:verifiability`-safe to attribute), plus this probe. Every directory's mtime is
younger than IDLE_MIN=45; `unreadable=0`. Wave-1 is in flight, so `kasegi-r39` is *expected* to be
populated now — G6 is a filing/closing-time predicate and cannot be green mid-wave. Snapshots taken
during this probe show the drift plainly: 14 entries all empty (19:30Z) → 38 (19:31Z) → 37
(19:33:32Z). The per-entry table in the deliverable is therefore a timestamped snapshot, and §G
carries the recheck to run at filing.

**F3 — `RevControls-2` is this wave's work under a non-roster name.** 16,419 entries / 272 MB of
`base/` = a `git archive` lane export, written to `kasegi-r39/RevControls-2/` while the dispatch
specified `kasegi-r39/RevControls/` and no `RevControls` dir exists. It is not foreign debris and
not an abandoned tree — it is the RevControls seat's live scratch under a name that is not a
`<seat-name>` per lane-addendum §7.1 (`$HYAKU_SCRATCH/<lane>-r<N>/<seat-name>/`). Consequence: a
roster-membership or dispatch-name discriminator reads it as foreign at filing, and it is the
seat's responsibility to delete it at yield (§7.2). Not removed by me — scratch outside my seat's
own dir is outside my write scope.

**F4 — `kasegi-r39-l1` escapes both cleanup paths and matches the strict prefix.** It is L1's own
scratch (8 files, 1 MB), it is not a G6-named root (`kasegi-r37/r38/r39` only), and
`purge-lane kasegi 39` removes exactly `kasegi-r39`, so neither the gate nor the advance purge
covers it. It *does* match `kasegi-r3[6-9]*`, which is how the C1 kill rule ("any leftover
kasegi-r37/r38/r39 scratch entry at filing") and any `ls | grep` verifier will read it. The L1 must
delete `/fast/scratch/hyaku/kasegi-r39-l1` at filing to keep that clause green on a strict reading.

**F5 — Headroom is not the constraint; exports are the consumer.** `/fast` has 619 G free (24 %),
`/tmp` 126 G (3 %), `/home` 586 G (35 %). `kasegi-r39` is 1,139 MB, and six entries are ≥100 MB,
all lane exports: `ExecArchiveNoHarmMirror` 273 MB, `RevControls-2` 272 MB, `ExecHarnessProbe`
137 MB, `ExecSuiteBuild` 136 MB, `ExecCensusAfterMirror` 136 MB, `ExecPinnedG8Fixture` 132 MB.
`git archive` exports are the sanctioned mode (§7.3), but six concurrent ~136 MB copies of the lane
are the whole footprint; a seat that re-exports per case would multiply it.

## Note for the G6 implementation (freeze-compatible, no predicate change)

1. **Discriminator.** At closure the correct test is "`kasegi-r39` holds no entry other than the
   closure run's own `--work` path (and its ancestor chain under `kasegi-r39`)", with every
   wave-seat dir gone. A roster-membership exemption is *wrong* here: it would let a leaked seat dir
   pass at close, which is exactly the defect G6 exists to catch. Roster membership is the right
   discriminator only for attributing a *live wave-1* snapshot like this one.
2. **Read test.** Fail-closed must test directories with `R_OK|X_OK` and regular files with `R_OK`
   only. Applying `X_OK` to regular files produced five false "unreadable" hits on 0644 files in my
   first generator run; the corrected test reports `unreadable=0`. A gate with that bug would print
   `read=fail` on a clean root.

## Scratch discipline

`S=/fast/scratch/hyaku/kasegi-r39/ExecDiskGuardProbe/` created with `mkdir -p`, all work bound there.
Removed before yield: `removed_and_absent /fast/scratch/hyaku/kasegi-r39/ExecDiskGuardProbe`, and
`ls -1A /fast/scratch/hyaku/kasegi-r39 | grep -c '^ExecDiskGuardProbe$'` → `0` (19:34:13Z). No
`/tmp` or `/var/tmp` writes.

## Tooling

None installed or upgraded: `bash`, `python3` (stdlib), `df`, `du`, `sha256sum` were sufficient.
No pacman, no `uv tool install`, no PATH-directory writes.

## Risks

- The deliverable's per-entry counts are stale within minutes by construction; §A–§B and §D–§F are
  the invariant parts, §G is the executable recheck.
- F3/F4 are reported, not fixed: both paths are outside this seat's write scope. Residual risk at
  filing is a strict prefix/roster reader seeing `RevControls-2` or `kasegi-r39-l1`.
- Cross-reference only, not this item's finding: a scratch dir under a non-dispatched name hints the
  RevControls seat may also report under a variant identity; G4's owner (`ExecSeatIdentitySpec`)
  should confirm `results.json` identities equal dispatched task names.
