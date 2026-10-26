# ExecQuiescenceProbe — E9 quiescence gate (round 36 build wave)

Seat: ExecQuiescenceProbe (executor, depth:verifiability). Item: implement E9's
quiescence check as a standalone reusable command (draft) and prove it can fail:
(1) record the two frozen counters on the real lane now, (2) show the gate exits 1
on a fake dirty tree + fake leftover scratch dir, (3) show exit 0 on a clean state.

Status: **landed**. The gate exists as a 320-line bash draft, is `bash -n` and
`shellcheck -S warning` clean, its own `--selftest` is `cases=11 failures=0 exit=0`,
and it is red exactly on the two frozen counters and green exactly off them. The
complete script is transcribed at the end of this receipt (the scratch directory
that held it was removed at yield, per the seat contract); digest of the transcribed
bytes: `sha256 ecd3bb821ed6987cd614a41f523e912328b3becf3fac97c2b33a97f31ec07a2b`.

No lane file was created or edited by this seat. The only lane write is this receipt.

## 1. What the gate computes (frozen definition, not invented)

Round-36 `claims.json` C1 check E9, counting commands quoted verbatim:

```
git status --porcelain | wc -l                                       -> must be 0
find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1 -type d | wc -l -> must be 0
```

The draft reproduces both counters byte-for-byte (same flag, same `find`
predicate, same defaults) and makes the exit status the verdict. Two design points
that are load-bearing rather than decorative:

- **E9 cannot read the export.** Every other round-36 check runs on a `git archive`
  export, but quiescence is a property of the *live* lane. An export has no `.git`,
  so `git -C <export> status` either fails or walks up to an enclosing repository
  and reports *its* status. The gate refuses both cases with exit 2 instead of
  printing a green `0/0` — proved below on a real `git archive` of
  `3266c9937b03062d9bbc2f436e20820115ed179c` and on an export nested inside a
  fixture repo.
- **`--expect-head REF` (opt-in) binds live state to an exported head.** Without a
  binding, a green E9 only says the live worktree was clean at *some* commit. With
  `--expect-head <exported ref>` the gate also requires `git rev-parse HEAD` to
  equal `rev-parse REF^{commit}` and reports `head-match=0|1`. A valid-but-different
  object is a red (`head-match=0`); an object that does not exist is a harness
  error, because the gate will not judge a ref it cannot resolve.

Interface:

```
bash quiescence-gate.sh [--lane-root DIR] [--seat-dir DIR] [--expect-head REF]
bash quiescence-gate.sh --selftest [--work DIR]
```

Default lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; default seat dir is the
frozen absolute `/fast/scratch/hyaku/kasegi-r36`, deliberately *not* derived from
`HYAKU_SCRATCH`/`TMPDIR`, so an inherited environment cannot redirect the
measurement. Exit: 0 quiescent, 1 not quiescent, 2 harness error
(`lane-not-a-git-worktree-root` / `expect-head-unresolvable` /
`unexpected-counter-output` / bad argument). Payload line:
`E9 check=status-lines=N,seat-dirs=M,stray-files=K[,head-match=0|1] open=0|1`,
mirroring `r35-defect-closure.sh`'s per-check `D<i> check=... open=` shape.

Instrument hygiene measured on the transcribed bytes:

```
sha256sum = ecd3bb821ed6987cd614a41f523e912328b3becf3fac97c2b33a97f31ec07a2b
wc -l     = 320
bash -n   = exit 0
shellcheck -S warning = exit 0
```

## 2. (1) The real lane, recorded — **red, as it must be mid-wave**

`2026-10-26T15:42:36Z` (script digest `ecd3bb82…`):

```
$ bash quiescence-gate.sh
E9 check=status-lines=9,seat-dirs=35,stray-files=0 open=1
closed=0/1 exit=1                                        [exit=1]

$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain | wc -l
9
$ find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1 -type d | wc -l
35
$ git -C … rev-parse HEAD
b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6
```

The gate's payload and the two frozen counters agree exactly (9 / 35). Attribution
of the nine status lines at that moment — all untracked round-36 dispatcher
artefacts, none a lane defect:

```
?? .ufo/waves/round-36/build-spec.py
?? .ufo/waves/round-36/wave1-dispatch.json
?? .ufo/waves/round-36/wave1-plan.err
?? .ufo/waves/round-36/wave1-plan.out
?? .ufo/waves/round-36/wave1-run.err
?? .ufo/waves/round-36/wave1-spec.json
?? .ufo/waves/round-36/wave1.ready
?? .ufo/waves/round-36/wave1.ready.dispatched
?? .ufo/waves/round-36/wave1/
```

Head binding on the same live lane:

```
--expect-head b47f2cd… (live HEAD)  -> E9 check=status-lines=9,seat-dirs=35,stray-files=0,head-match=1 open=1 [exit=1]
--expect-head 3266c99… (r35 base)   -> E9 check=status-lines=9,seat-dirs=35,stray-files=0,head-match=0 open=1 [exit=1]
--expect-head 0123…4567 (absent)    -> E9 harness-error=expect-head-unresolvable … [exit=2]
```

So the binding discriminates on the real repository: HEAD matches itself, the r35
base commit is a valid object that is not HEAD (`head-match=0`), and an absent
object is refused rather than scored.

**Closure-order reading (for the L1, not a defect claim).** E9 is red on the live
lane *now* because the wave is still open: the nine dispatcher files are untracked
until the closing commit, and seat scratch dirs exist until the sweep. This is
exactly what a quiescence gate is for. The seat-dir counter moved 46 → 41 → 36 → 35
across the wave (measured at 15:37Z, 15:40Z, 15:41Z, 15:42:36Z) while the status
counter stayed 9 — evidence that the counter is live and not memoised. This seat's
own scratch dir was removed before this receipt was written, so it cannot be one of
the leftovers E9 will count.

## 3. (2) Red proof — fake dirty tree + fake leftover seat dir

Fixture: `mktemp -d` under the seat scratch dir, `git -C "$D" init -q`, then
`rev-parse --show-toplevel` printed and compared to `realpath "$D"` —
`toplevel=/fast/scratch/hyaku/kasegi-r36/ExecQuiescenceProbe/sandbox/fix.CUMBu2`,
equal to its realpath (verified=1). One tracked file committed, so the fixture
starts genuinely clean.

```
# clean baseline
E9 check=status-lines=0,seat-dirs=0,stray-files=0 open=0   [exit=0]

# : > "$D/dirty.txt"  and  mkdir -p "$SEATS/FakeSeat"
E9 check=status-lines=1,seat-dirs=1,stray-files=0 open=1
closed=0/1 exit=1                                          [exit=1]
```

Each limb alone (same fixture, one defect at a time):

```
dirty only       E9 check=status-lines=1,seat-dirs=0,stray-files=0 open=1  [exit=1]
leftover only    E9 check=status-lines=0,seat-dirs=1,stray-files=0 open=1  [exit=1]
```

## 4. (3) Green proof — clean state, and green again after the sweep

```
clean fixture, empty seat dir
  E9 check=status-lines=0,seat-dirs=0,stray-files=0 open=0
  closed=1/1 exit=0                                        [exit=0]

clean fixture + --expect-head <fixture HEAD>
  E9 check=status-lines=0,seat-dirs=0,stray-files=0,head-match=1 open=0
  closed=1/1 exit=0                                        [exit=0]

after removing the fake leftovers from the red fixture
  E9 check=status-lines=0,seat-dirs=0,stray-files=0 open=0
  closed=1/1 exit=0                                        [exit=0]
```

The green is produced by the same bytes and the same code path as the red; only the
measured tree changed.

## 5. Each limb is load-bearing (mutation control)

Two mutant controls, each dropping exactly one counter, run against the same
fixture (`sandbox/fix.CUMBu2`, script digest `ecd3bb82…`). `mutant-no-status` forces
`status-lines=0`; `mutant-no-seat` forces `seat-dirs=0`.

| fixture state | gate | mutant-no-status | mutant-no-seat |
|---|---|---|---|
| clean | open=0 exit=0 | open=0 exit=0 | open=0 exit=0 |
| dirty only | **open=1 exit=1** | open=0 exit=0 (miss) | open=1 exit=1 |
| leftover only | **open=1 exit=1** | open=1 exit=1 | open=0 exit=0 (miss) |
| both | **open=1 exit=1** | open=1 exit=1 | open=1 exit=1 |
| restored clean | open=0 exit=0 | open=0 exit=0 | open=0 exit=0 |

A gate missing either limb passes a state that violates E9, so neither counter is
decoration. The mutants never touch the lane; they live in scratch and were removed
with it.

## 6. Refusal controls — E9 pointed where it must not pass

```
git archive 3266c9937b03062d9bbc2f436e20820115ed179c | tar -x -C <scratch>/export
  export .git present = no
  gate on export            -> E9 harness-error=lane-not-a-git-worktree-root … [exit=2]
  gate on export nested in a repo (repo fixture …/nested/export)
                            -> E9 harness-error=lane-not-a-git-worktree-root … [exit=2]
```

The second case is the dangerous one: a directory inside another repository does
resolve a toplevel, but not one equal to itself, so the gate refuses instead of
reporting the enclosing repo's status as the lane's. Both are exit 2, never a green.

## 7. `--selftest` — 11 cases, all on the transcribed bytes

```
selftest case=clean               status-lines=0 seat-dirs=0 stray-files=0 head-match=- exit=0 want-exit=0 verdict=pass
selftest case=dirty-worktree      status-lines=1 seat-dirs=0 stray-files=0 head-match=- exit=1 want-exit=1 verdict=pass
selftest case=leftover-seat-dir   status-lines=0 seat-dirs=1 stray-files=0 head-match=- exit=1 want-exit=1 verdict=pass
selftest case=dirty-and-leftover  status-lines=1 seat-dirs=1 stray-files=0 head-match=- exit=1 want-exit=1 verdict=pass
selftest case=seat-dir-absent     status-lines=0 seat-dirs=0 stray-files=0 head-match=- exit=0 want-exit=0 verdict=pass
selftest case=stray-file-only     status-lines=0 seat-dirs=0 stray-files=1 head-match=- exit=0 want-exit=0 verdict=pass
selftest case=export-no-git       status-lines=- seat-dirs=- stray-files=- head-match=- exit=2 want-exit=2 verdict=pass
selftest case=nested-repo         status-lines=- seat-dirs=- stray-files=- head-match=- exit=2 want-exit=2 verdict=pass
selftest case=expect-head-match   status-lines=0 seat-dirs=0 stray-files=0 head-match=1 exit=0 want-exit=0 verdict=pass
selftest case=expect-head-mismatch status-lines=0 seat-dirs=0 stray-files=0 head-match=0 exit=1 want-exit=1 verdict=pass
selftest case=expect-head-absent  status-lines=- seat-dirs=- stray-files=- head-match=- exit=2 want-exit=2 verdict=pass
quiescence selftest cases=11 failures=0 exit=0
```

Every case asserts the full vector (exit status plus each counter), not just the
exit code, and `expect-head-mismatch` uses an *ancestor commit that exists in the
fixture repo* — the first attempt used a foreign hash, which correctly came back as
exit 2 `expect-head-unresolvable` and is why the two outcomes are now separate
cases. Fixtures are `mktemp -d` dirs whose toplevel is asserted equal to the fixture
path before any `git init`/`git add`/`commit`; the second fixture commit exists
solely so two same-second commits of identical trees cannot collide into one hash.
The temp dir is removed on exit (`tmp-leftovers=0` measured after the run).

## 8. Declared limits (measured, not hidden)

- **Non-directory leftovers do not move the exit.** The frozen counter is
  `find … -type d`. A stray regular file (or symlink) under the seat dir is
  reported as `stray-files=K` but leaves `open=0`; case `stray-file-only` measures
  exactly that direction (`stray-files=1`, exit 0). If the L1 wants quiescence to
  mean "seat dir empty", the exit driver has to be widened in the claim first — the
  gate does not silently redefine the frozen counter.
- **E9 is a live-state measurement, so it is not replayable from an export.** The
  suite's replay on the r35 base/judged-head exports can only show E9 red because
  *the live lane at replay time* is non-quiescent (or, with `--expect-head`, because
  the exported ref is not HEAD). That is the honest reading and it is why the
  binding is opt-in rather than assumed.
- **`git status` refreshes the index stat cache** (it is the frozen counting command
  itself, so this is not an extra write); no `--no-optional-locks` rewrite is used
  because the claim names the plain command.

## 9. Integration note for `corpus/instruments/r36-closure.sh` (E9)

The suite must call E9 with the **lane** path even in `--export-ref` mode. Inline
form, if the L1 prefers not to land a second instrument:

```bash
status=$(git -C "$LANE" status --porcelain | wc -l)
seats=$(find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1 -type d | wc -l)
head=$(git -C "$LANE" rev-parse HEAD)          # bind to the exported ref
# closed when status = 0 and seats = 0 (and head = the --export-ref commit)
```

If landed as `corpus/instruments/quiescence-gate.sh`, the same line is
`bash corpus/instruments/quiescence-gate.sh --lane-root "$LANE" --expect-head "$REF"`.
Either way, a harness error (exit 2) must count as *not closed*, never as a pass.
A short note with these two points was sent to `ExecC1SuiteBuild`.

## 10. Files, scratch, tooling

- Lane write: this receipt only. No instrument is created in the lane by this seat
  (the frozen claim routes E9 into `r36-closure.sh`, owned by ExecC1SuiteBuild).
- Scratch: `/fast/scratch/hyaku/kasegi-r36/ExecQuiescenceProbe/` held the draft
  `quiescence-gate.sh`, two mutant controls, and the fixture/export trees; the
  whole directory was removed before this receipt was written
  (`[ -e … ]` → absent). Nothing under `/tmp` was used.
- Tooling: none installed or upgraded (`shellcheck` 0.x already present at
  `/usr/bin/shellcheck`; no pacman, no network).

## 11. Draft bytes (complete, verbatim)

```bash
#!/usr/bin/env bash
# quiescence-gate.sh — E9 (quiescence) of the round-36 closure suite, standalone
# and reusable. Draft seat artifact (ExecQuiescenceProbe, round-36 build wave).
#
# Frozen definition (round-36 claims.json, C1 check E9): the lane is quiescent
# when both counters read 0 —
#   git -C <lane> status --porcelain | wc -l                                   (live worktree)
#   find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1 -type d | wc -l (scratch seats)
# Both counters are computed verbatim; the exit status is the verdict.
#
# Usage:
#   bash quiescence-gate.sh [--lane-root DIR] [--seat-dir DIR] [--expect-head REF]
#       Print one `E9 check=status-lines=N,seat-dirs=M,stray-files=K open=0|1`
#       line and a `closed=1/1 exit=0` / `closed=0/1 exit=1` summary.
#       --lane-root defaults to /home/vgpnk/Projects/shokunin/kasegi-shokunin;
#       --seat-dir defaults to the frozen absolute /fast/scratch/hyaku/kasegi-r36
#       (never derived from an inherited environment, so a stray HYAKU_SCRATCH
#       cannot redirect the measurement).
#       --expect-head REF (opt-in) binds the live measurement to a head: the lane's
#       `git rev-parse HEAD` must equal `rev-parse REF^{commit}`, and the payload
#       gains `head-match=0|1`; a mismatch is a red, an unresolvable REF is exit 2.
#       The suite runs its other checks on a `git archive` export, so without this
#       binding a green E9 would only say the live worktree was clean at *some*
#       commit — with it, the clean worktree provably belongs to the exported ref.
#   bash quiescence-gate.sh --selftest [--work DIR]
#       Build eleven throwaway fixtures under a mktemp dir under --work (default
#       ${KASEGI_SCRATCH:-${TMPDIR:-/tmp}}) and assert the gate's verdict on each:
#       clean -> exit 0; one untracked file -> exit 1; one leftover seat dir ->
#       exit 1; both -> exit 1; absent seat dir -> exit 0 (no false red);
#       stray regular file only -> exit 0 with stray-files=1 (the declared limit
#       measured, not assumed); a non-git export tree -> exit 2; a directory
#       nested inside another repository -> exit 2; --expect-head equal to HEAD ->
#       exit 0 with head-match=1; --expect-head naming another commit -> exit 1;
#       --expect-head naming an absent object -> exit 2. Prints one
#       `selftest case=<name> ... verdict=pass|fail` line per case and
#       `quiescence selftest cases=11 failures=0` with exit 0 on success.
#
# Why E9 refuses a non-worktree-root. Every other check of the round-36 suite
# reads a `git archive` export, but quiescence is a property of the LIVE lane:
# an export has no .git of its own. Pointed at an export, `git rev-parse
# --show-toplevel` fails, and this gate exits 2 instead of reporting a green 0/0.
# A directory that merely sits inside some other repository is refused for the
# same reason — otherwise E9 could report the enclosing repository's status as
# the lane's. The suite must therefore call E9 with the lane path, not the
# export path.
#
# Read-only. The plain run writes nothing: two `git` reads (`rev-parse`,
# `status --porcelain` — exactly the frozen counting command, no
# --no-optional-locks rewrite) and two `find` reads. Only --selftest writes, and
# only under its own mktemp dir, removed on exit; its fixtures call `git init`
# and `git add` inside that dir after asserting `rev-parse --show-toplevel`
# equals the fixture path.
#
# Documented limit (measured, not hidden). The exit drivers are exactly the two
# frozen counters: untracked/modified lane paths and directories under the seat
# dir. A non-directory entry under the seat dir (a stray log, a symlink) is
# reported in `stray-files=` but does not move `open=`, because the frozen
# counter is `find ... -type d`. --selftest measures that direction
# (`case=stray-file-only`).
#
# Exit codes: 0 quiescent / selftest clean, 1 not quiescent / selftest failure,
# 2 harness error — printed as `E9 harness-error=<reason>` where reason is one of
# `lane-not-a-git-worktree-root` (the --lane-root is not itself a worktree root,
# e.g. a `git archive` export), `expect-head-unresolvable` (the --expect-head ref
# names no commit in the lane), `unexpected-counter-output`, or a bad argument /
# unusable work base. A harness error is never a green.
set -uo pipefail

SELF=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/$(basename -- "${BASH_SOURCE[0]}")
LANE_ROOT=/home/vgpnk/Projects/shokunin/kasegi-shokunin
SEAT_DIR=/fast/scratch/hyaku/kasegi-r36
WORK_BASE=${KASEGI_SCRATCH:-${TMPDIR:-/tmp}}
MODE=run
EXPECT_HEAD=
HEAD_MATCH=-
ERR=
STATUS_LINES=
SEAT_DIRS=
STRAY_FILES=
SELFTEST_BASE=

usage() {
    cat <<'USAGE'
quiescence-gate.sh — E9 quiescence gate (standalone)

  bash quiescence-gate.sh [--lane-root DIR] [--seat-dir DIR]
  bash quiescence-gate.sh --selftest [--work DIR]

Exit: 0 quiescent, 1 not quiescent, 2 harness error.
USAGE
}

need_value() {
    if [ $# -lt 2 ]; then
        printf 'quiescence-gate: %s requires a value\n' "$1" >&2
        exit 2
    fi
}

while [ $# -gt 0 ]; do
    case $1 in
        --lane-root) need_value "$@"; LANE_ROOT=$2; shift 2 ;;
        --seat-dir)  need_value "$@"; SEAT_DIR=$2;  shift 2 ;;
        --expect-head) need_value "$@"; EXPECT_HEAD=$2; shift 2 ;;
        --work)      need_value "$@"; WORK_BASE=$2; shift 2 ;;
        --selftest)  MODE=selftest; shift ;;
        -h|--help)   usage; exit 0 ;;
        *)
            printf 'quiescence-gate: unknown argument: %s\n' "$1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

# measure LANE SEAT -> sets STATUS_LINES, SEAT_DIRS, STRAY_FILES.
# Returns 0 on a measurement, 2 when LANE is not itself a git worktree root.
measure() {
    local lane=$1 seat=$2 top real v
    ERR='lane-not-a-git-worktree-root'
    [ -d "$lane" ] || return 2
    top=$(git -C "$lane" rev-parse --show-toplevel 2>/dev/null) || return 2
    real=$(realpath -- "$lane" 2>/dev/null) || return 2
    [ -n "$top" ] || return 2
    [ "$top" = "$real" ] || return 2

    STATUS_LINES=$(git -C "$lane" status --porcelain 2>/dev/null | wc -l)
    if [ -d "$seat" ]; then
        SEAT_DIRS=$(find "$seat" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
        STRAY_FILES=$(find "$seat" -mindepth 1 -maxdepth 1 ! -type d 2>/dev/null | wc -l)
    else
        SEAT_DIRS=0
        STRAY_FILES=0
    fi
    for v in "$STATUS_LINES" "$SEAT_DIRS" "$STRAY_FILES"; do
        v=${v//[[:space:]]/}
        case $v in
            ''|*[!0-9]*) ERR='unexpected-counter-output'; return 2 ;;
        esac
    done
    STATUS_LINES=${STATUS_LINES//[[:space:]]/}
    SEAT_DIRS=${SEAT_DIRS//[[:space:]]/}
    STRAY_FILES=${STRAY_FILES//[[:space:]]/}
    if [ -n "$EXPECT_HEAD" ]; then
        local want head
        ERR='expect-head-unresolvable'
        want=$(git -C "$lane" rev-parse --verify --quiet "${EXPECT_HEAD}^{commit}") || return 2
        head=$(git -C "$lane" rev-parse --verify --quiet 'HEAD^{commit}') || return 2
        [ -n "$want" ] && [ -n "$head" ] || return 2
        ERR=
        if [ "$want" = "$head" ]; then HEAD_MATCH=1; else HEAD_MATCH=0; fi
    else
        HEAD_MATCH=-
    fi
    return 0
}

# report: print the payload line and the summary; exit status is the verdict.
report() {
    local open=0
    [ "$STATUS_LINES" -eq 0 ] || open=1
    [ "$SEAT_DIRS" -eq 0 ] || open=1
    [ "$HEAD_MATCH" = 0 ] && open=1
    if [ "$HEAD_MATCH" = '-' ]; then
        printf 'E9 check=status-lines=%s,seat-dirs=%s,stray-files=%s open=%s\n' \
            "$STATUS_LINES" "$SEAT_DIRS" "$STRAY_FILES" "$open"
    else
        printf 'E9 check=status-lines=%s,seat-dirs=%s,stray-files=%s,head-match=%s open=%s\n' \
            "$STATUS_LINES" "$SEAT_DIRS" "$STRAY_FILES" "$HEAD_MATCH" "$open"
    fi
    if [ "$open" -eq 0 ]; then
        printf 'closed=1/1 exit=0\n'
        return 0
    fi
    printf 'closed=0/1 exit=1\n'
    return 1
}

# ---------------------------------------------------------------- selftest ---
cases=0
failures=0

# mkfix DEST: git init DEST, assert its toplevel is DEST, stage one file.
mkfix() {
    local dest=$1 top real
    mkdir -p "$dest" || return 2
    git -C "$dest" init -q 2>/dev/null || return 2
    top=$(git -C "$dest" rev-parse --show-toplevel 2>/dev/null) || return 2
    real=$(realpath -- "$dest") || return 2
    [ "$top" = "$real" ] || return 2
    printf 'base\n' > "$dest/tracked.txt"
    git -C "$dest" add -A >/dev/null 2>&1 || return 2
    git -C "$dest" -c user.name=quiescence-fixture \
        -c user.email=quiescence-fixture@example.invalid \
        commit -q --no-gpg-sign -m fixture >/dev/null 2>&1 || return 2
    return 0
}

# run_case NAME LANE SEAT WANT_EXIT WANT_STATUS WANT_SEATS WANT_STRAY WANT_HEAD [EXTRA...]
#   A WANT_* value of '-' means "not asserted". EXTRA arguments are passed to the
#   gate after --lane-root/--seat-dir (e.g. --expect-head REF).
run_case() {
    local name=$1 lane=$2 seat=$3 want_exit=$4
    local want_status=${5:--} want_seats=${6:--} want_stray=${7:--} want_head=${8:--}
    local out st line sl=- sd=- sf=- hm=- verdict=pass
    shift 8
    cases=$((cases + 1))
    out=$(bash "$SELF" --lane-root "$lane" --seat-dir "$seat" "$@" 2>&1)
    st=$?
    line=$(printf '%s\n' "$out" | grep -m1 '^E9 check=' || true)
    if [ -n "$line" ] && [[ $line =~ status-lines=([0-9]+),seat-dirs=([0-9]+),stray-files=([0-9]+) ]]; then
        sl=${BASH_REMATCH[1]}
        sd=${BASH_REMATCH[2]}
        sf=${BASH_REMATCH[3]}
        [[ $line =~ head-match=([01]) ]] && hm=${BASH_REMATCH[1]}
    fi
    [ "$st" = "$want_exit" ] || verdict=fail
    [ "$want_status" = '-' ] || [ "$sl" = "$want_status" ] || verdict=fail
    [ "$want_seats" = '-' ] || [ "$sd" = "$want_seats" ] || verdict=fail
    [ "$want_stray" = '-' ] || [ "$sf" = "$want_stray" ] || verdict=fail
    [ "$want_head" = '-' ] || [ "$hm" = "$want_head" ] || verdict=fail
    [ "$verdict" = pass ] || failures=$((failures + 1))
    printf 'selftest case=%s status-lines=%s seat-dirs=%s stray-files=%s head-match=%s exit=%s want-exit=%s verdict=%s\n' \
        "$name" "$sl" "$sd" "$sf" "$hm" "$st" "$want_exit" "$verdict"
    if [ "$verdict" != pass ]; then
        printf 'selftest detail=%s raw=%q\n' "$name" "$out"
    fi
}

run_selftest() {
    local repo seats out
    mkdir -p -- "$WORK_BASE" 2>/dev/null || {
        printf 'quiescence-gate: cannot create the work base %s\n' "$WORK_BASE" >&2
        return 2
    }
    SELFTEST_BASE=$(mktemp -d "${WORK_BASE%/}/quiescence-selftest.XXXXXX") || {
        printf 'quiescence-gate: cannot create a work dir under %s\n' "$WORK_BASE" >&2
        return 2
    }
    base=$SELFTEST_BASE
    trap 'rm -rf -- "$SELFTEST_BASE"' EXIT
    repo=$base/repo
    seats=$base/seats/kasegi-r36
    mkfix "$repo" || {
        printf 'quiescence-gate: fixture repo init failed (%s)\n' "$repo" >&2
        return 2
    }
    mkdir -p "$seats"

    run_case clean "$repo" "$seats" 0 0 0 0 -
    : > "$repo/untracked.txt"
    run_case dirty-worktree "$repo" "$seats" 1 1 0 0 -
    rm -f -- "$repo/untracked.txt"
    mkdir -p "$seats/FakeSeat"
    run_case leftover-seat-dir "$repo" "$seats" 1 0 1 0 -
    : > "$repo/untracked.txt"
    run_case dirty-and-leftover "$repo" "$seats" 1 1 1 0 -
    rm -f -- "$repo/untracked.txt"
    run_case seat-dir-absent "$repo" "$base/absent/kasegi-r36" 0 0 0 0 -
    rm -rf -- "$seats"
    mkdir -p "$seats"
    : > "$seats/stray.log"
    run_case stray-file-only "$repo" "$seats" 0 0 0 1 -

    out=$base/export
    mkdir -p "$out"
    printf 'exported\n' > "$out/tracked.txt"
    run_case export-no-git "$out" "$seats" 2 - - - -

    local outer=$base/outer head_here head_prev
    mkfix "$outer" || {
        printf 'quiescence-gate: fixture repo init failed (%s)\n' "$outer" >&2
        return 2
    }
    # A second commit so the two fixture heads cannot collide on identical
    # tree/author/timestamp bytes (same-second commits of equal trees would).
    printf 'other\n' > "$outer/other.txt"
    git -C "$outer" add -A >/dev/null 2>&1 || return 2
    git -C "$outer" -c user.name=quiescence-fixture \
        -c user.email=quiescence-fixture@example.invalid \
        commit -q --no-gpg-sign -m other >/dev/null 2>&1 || return 2
    mkdir -p "$outer/sub"
    run_case nested-repo "$outer/sub" "$seats" 2 - - - -

    rm -rf -- "$seats"
    mkdir -p "$seats"
    head_prev=$(git -C "$repo" rev-parse HEAD)
    printf 'second\n' > "$repo/second.txt"
    git -C "$repo" add -A >/dev/null 2>&1 || return 2
    git -C "$repo" -c user.name=quiescence-fixture \
        -c user.email=quiescence-fixture@example.invalid \
        commit -q --no-gpg-sign -m second >/dev/null 2>&1 || return 2
    head_here=$(git -C "$repo" rev-parse HEAD)
    if [ "$head_here" = "$head_prev" ]; then
        printf 'quiescence-gate: fixture commit did not move HEAD\n' >&2
        return 2
    fi
    run_case expect-head-match "$repo" "$seats" 0 0 0 0 1 --expect-head "$head_here"
    run_case expect-head-mismatch "$repo" "$seats" 1 0 0 0 0 --expect-head "$head_prev"
    run_case expect-head-absent "$repo" "$seats" 2 - - - - \
        --expect-head 0123456789abcdef0123456789abcdef01234567

    printf 'quiescence selftest cases=%s failures=%s exit=%s\n' \
        "$cases" "$failures" "$([ "$failures" -eq 0 ] && printf 0 || printf 1)"
    [ "$failures" -eq 0 ] || return 1
    return 0
}

if [ "$MODE" = selftest ]; then
    run_selftest
    exit $?
fi

if ! measure "$LANE_ROOT" "$SEAT_DIR"; then
    printf 'E9 harness-error=%s lane=%s\n' "${ERR:-harness-error}" "$LANE_ROOT"
    printf 'closed=error exit=2\n'
    exit 2
fi
report
exit $?
```
