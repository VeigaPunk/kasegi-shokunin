#!/usr/bin/env bash
# ExecH6ScratchFixtures.sibling-dir.sh — round-40 H6 discrimination fixture.
#
# Proves the H6 limb of `corpus/instruments/r40-closure.sh` discriminates: a stray
# kasegi-r39*/kasegi-r40* scratch-sibling entry under the audited scratch root reds
# the run, its removal greens it, and the run's own passed --work dir is tolerated
# by realpath (never by name) so a verifier's own work cannot turn the check red.
#
# This is the reference implementation of the frozen H6 policy (claims.json C1;
# round-39 G6 defect from `.ufo/waves/round-39/wave2/CritC1Kill.md`: exact-name
# coupling on `kasegi-r39`, so `kasegi-r39-l1`-style sibling names escaped, and the
# live root held every seat's scratch dir). It is self-contained: it needs no lane
# export, no git, and no built suite. The `check_h6` function is the limb; the
# default run is the discrimination matrix over an isolated sandbox.
#
# H6 policy implemented here:
#   * Scan ONLY top-level entries of the scratch root whose basename, after one
#     leading dot is stripped, matches `kasegi-r39*` or `kasegi-r40*` (prefix
#     families, so `kasegi-r39-l1`, `kasegi-r40-<seat>` and `.kasegi-r40-seat`
#     are all caught; `kasegi-r41*` and unrelated names are out of scope). Every
#     entry type is in scope: directory, regular file, dotfile, symlink.
#   * The passed --work realpath is tolerated, as is a clean chain of
#     single-child directories from a matching entry down to it. Tolerance is by
#     realpath, never by name, and the chain must be empty of anything else.
#   * Presence of a stray entry reds the run, even when the directory is empty
#     (fail-closed on presence, not on content). An unresolvable entry reds it too.
#   * An unreadable scratch root or a missing/unresolvable --work is RED, never
#     "zero entries".
#   * Hermetic: the probe refuses a scratch root at, above, or equal to the real
#     /fast/scratch/hyaku, so it can never read or disturb live host state.
#
# Usage:
#   bash ExecH6ScratchFixtures.sibling-dir.sh [--root DIR] [--keep]
#       Run the full matrix in an isolated sandbox (default: mktemp -d under
#       ${TMPDIR:-/tmp}). Prints one expecting/stray transcript per scenario, the
#       GRADED `probe scenario=... verdict=pass|fail` lines, and a final
#       `probe scenarios=<n> failures=<k>` with exit 0 only when k=0.
#   bash ExecH6ScratchFixtures.sibling-dir.sh --check --scratch-root DIR --work DIR
#       Run the H6 limb once against DIR and print the suite-shaped
#       `H6 payload=... closed=0|1` line plus `closed=<K>/10 exit=<0|1>`.
#       Exit 0 green, 1 red. DIRs are never created or modified.
#   bash ExecH6ScratchFixtures.sibling-dir.sh -h|--help
#
# Exit codes: 0 matrix clean / limb green, 1 matrix failure / limb red,
# 2 harness error (bad argument, hermeticity refusal, unreadable sandbox).

set -uo pipefail

REAL_HYAKU=/fast/scratch/hyaku
K=10 # modelled check count: H6 is one limb of the ten-check suite
SELF=${BASH_SOURCE[0]:-}
case $SELF in
  /*) ;;
  *) [ -n "$SELF" ] && [ -d "$(dirname -- "$SELF")" ] \
       && SELF=$( cd -- "$(dirname -- "$SELF")" && pwd -P )/$(basename -- "$SELF") ;;
esac

die() { printf 'sibling-dir: %s\n' "$*" >&2; exit 2; }

usage() {
  sed -n '2,/^set -uo pipefail$/p' "${BASH_SOURCE[0]}" | sed -e '$d' -e 's/^# \{0,1\}//'
}

realpath_dir() { # DIR -> physical path, empty on failure
  local d=$1
  [ -d "$d" ] || { printf ''; return 0; }
  ( cd -- "$d" 2>/dev/null && pwd -P )
}

lane_name() { # BASENAME -> name with one leading dot stripped
  case $1 in
    .*) printf '%s' "${1#.}" ;;
    *)  printf '%s' "$1" ;;
  esac
}

is_round_sibling() { # BASENAME
  local n
  n=$(lane_name "$1")
  case $n in
    kasegi-r39*|kasegi-r40*) return 0 ;;
  esac
  return 1
}

family_of() { # BASENAME -> r39|r40
  local n
  n=$(lane_name "$1")
  case $n in
    kasegi-r39*) printf 'r39' ;;
    *) printf 'r40' ;;
  esac
}

chain_ok() { # ANCESTOR WORK — WORK strictly under ANCESTOR, every level single-child
  local dir=$1 rest=${2#"$1"/} next e n real
  [ -n "$rest" ] || return 1
  while [ -n "$rest" ]; do
    next=${rest%%/*}
    n=0; real=''
    while IFS= read -r e; do
      [ -n "$e" ] || continue
      n=$((n + 1))
      real=$(realpath_dir "$e")
    done < <(find "$dir" -mindepth 1 -maxdepth 1 -print 2>/dev/null)
    [ "$n" -eq 1 ] || return 1
    [ "$real" = "$dir/$next" ] || return 1
    dir=$real
    case $rest in
      */*) rest=${rest#*/} ;;
      *) rest='' ;;
    esac
  done
  return 0
}

check_h6() { # SCRATCH_ROOT WORK_DIR — prints payload, exit 0 green / 1 red
  local root=$1 work=$2
  local realroot='' realw='' workpos=outside read=ok r39=absent r40=absent
  local entry base real fam tol='' strays='' have_bad=0 rc out

  if [ -z "$work" ] || ! realw=$(realpath_dir "$work") || [ -z "$realw" ]; then
    printf 'H6 payload=scratch-root=%s,r39=?,r40=?,work=unknown,tolerated=none,strays=none,read=fail closed=0' \
      "${root:-unset}"
    return 1
  fi
  if [ ! -d "$root" ]; then
    printf 'H6 payload=scratch-root=absent,r39=?,r40=?,work=%s,tolerated=none,strays=none,read=fail closed=0' \
      "$workpos"
    return 1
  fi
  realroot=$(realpath_dir "$root")
  if [ -z "$realroot" ]; then
    printf 'H6 payload=scratch-root=unreadable,r39=?,r40=?,work=?,tolerated=none,strays=none,read=fail closed=0'
    return 1
  fi
  case $realw in
    "$realroot"/*) workpos=inside ;;
    "$realroot") workpos=root ;;
  esac

  if ! out=$(find "$realroot" -mindepth 1 -maxdepth 1 -print 2>/dev/null); then
    read=fail
    out=''
  fi
  while IFS= read -r entry; do
    [ -n "$entry" ] || continue
    base=${entry##*/}
    is_round_sibling "$base" || continue
    fam=$(family_of "$base")
    if [ -d "$entry" ]; then
      real=$(realpath_dir "$entry")
    elif [ -L "$entry" ]; then
      real=$(realpath -m -- "$entry" 2>/dev/null)
    else
      real='' # regular file (or a directory we cannot enter): presence is RED
    fi
    if [ -z "$real" ]; then
      # dangling entry, a file, or a directory we cannot enter: presence is RED,
      # never silently tolerated.
      strays="$strays"$'\n'"$base"
      have_bad=1
      if [ "$fam" = r39 ]; then r39=present; else r40=present; fi
      continue
    fi
    if [ "$real" = "$realw" ]; then
      tol="$tol"$'\n'"$base"
      continue
    fi
    case $realw in
      "$real"/*)
        if chain_ok "$real" "$realw"; then
          tol="$tol"$'\n'"$base"
          continue
        fi ;;
    esac
    strays="$strays"$'\n'"$base"
    have_bad=1
    if [ "$fam" = r39 ]; then r39=present; else r40=present; fi
  done < <(printf '%s\n' "$out")

  # every matching entry was tolerated (or none existed): family state is empty
  if [ "$have_bad" -eq 0 ]; then
    case $out in
      '') r39=absent; r40=absent ;;
      *)  while IFS= read -r entry; do
            [ -n "$entry" ] || continue
            base=${entry##*/}
            is_round_sibling "$base" || continue
            fam=$(family_of "$base")
            if [ "$fam" = r39 ]; then r39=empty; else r40=empty; fi
          done < <(printf '%s\n' "$out") ;;
    esac
  fi

  tol=$(printf '%s\n' "$tol" | sed '/^$/d' | LC_ALL=C sort | paste -sd, -)
  strays=$(printf '%s\n' "$strays" | sed '/^$/d' | LC_ALL=C sort | paste -sd, -)
  [ -n "$tol" ] || tol=none
  [ -n "$strays" ] || strays=none

  local closed=0
  if [ "$read" = ok ] && [ "$have_bad" -eq 0 ]; then
    closed=1
  fi
  printf 'H6 payload=r39=%s,r40=%s,work=%s,tolerated=%s,strays=%s,read=%s closed=%s' \
    "$r39" "$r40" "$workpos" "$tol" "$strays" "$read" "$closed"
  [ "$closed" -eq 1 ]
}

# emit_run ROOT WORK — suite-shaped limb run: payload line + modelled final line
emit_run() { # ROOT WORK
  local out rc k
  out=$(check_h6 "$1" "$2"); rc=$?
  printf '%s\n' "$out"
  if [ "$rc" -eq 0 ]; then k=$K; else k=$((K - 1)); fi
  printf 'closed=%s/%s exit=%s\n' "$k" "$K" "$rc"
  return "$rc"
}

refuse_real_root() { # DIR
  local real
  real=$(realpath -m -- "$1" 2>/dev/null)
  [ -n "$real" ] || return 0
  if [ "$real" = / ] || [ "$real" = "$REAL_HYAKU" ]; then
    die "hermeticity refusal: scratch root is the live host root ($real); use an isolated sandbox"
  fi
  case $REAL_HYAKU in
    "$real"/*) die "hermeticity refusal: scratch root ($real) contains the live host root; use an isolated sandbox" ;;
  esac
}

# ---- matrix ---------------------------------------------------------------

SB=''
ROOT=''
WORK=''
FAILS=0
SCEN=0
KEEP=0

cleanup() {
  [ -n "$SB" ] && [ -d "$SB" ] || return 0
  local d
  for d in "$SB"/scratch/*; do
    [ -d "$d" ] && [ ! -L "$d" ] && chmod 700 -- "$d" 2>/dev/null
  done
  [ "$KEEP" -eq 1 ] || rm -rf -- "$SB"
}

reset_sandbox() {
  rm -rf -- "$SB"
  mkdir -p -- "$SB/scratch" "$SB/work" || die "cannot create sandbox under $SB"
  ROOT=$SB/scratch
  WORK=$SB/work
}

expect() { # LABEL EXPECT(red|green) [NEEDLE...]
  local label=$1 want=$2; shift 2
  local out rc need ok=1 k line
  SCEN=$((SCEN + 1))
  out=$(check_h6 "$ROOT" "$WORK"); rc=$?
  printf '\nscenario=%s expect=%s\n' "$label" "$want"
  printf '%s\n' "$out"
  for k in "$@"; do
    printf '%s' "$out" | grep -qF -- "$k" || ok=0
  done
  if [ "$want" = red ]; then
    [ "$rc" -eq 1 ] || ok=0
  else
    [ "$rc" -eq 0 ] || ok=0
  fi
  if [ "$rc" -eq 0 ]; then k=$K; else k=$((K - 1)); fi
  printf 'closed=%s/%s exit=%s\n' "$k" "$K" "$rc"
  if [ "$ok" -eq 1 ]; then
    printf 'probe scenario=%s expect=%s got=%s verdict=pass\n' \
      "$label" "$want" "$([ "$rc" -eq 0 ] && echo green || echo red)"
  else
    printf 'probe scenario=%s expect=%s got=%s verdict=fail rc=%s payload=%s\n' \
      "$label" "$want" "$([ "$rc" -eq 0 ] && echo green || echo red)" "$rc" "$out"
    FAILS=$((FAILS + 1))
  fi
}

expect_refusal() { # LABEL SCRATCH_ROOT
  local label=$1 root=$2 out rc ok=1
  SCEN=$((SCEN + 1))
  out=$(bash "$SELF" --check --scratch-root "$root" --work "$SB/work" 2>&1); rc=$?
  printf '\nscenario=%s expect=harness-error(exit2)\n' "$label"
  printf '%s\n' "$out"
  printf 'rc=%s\n' "$rc"
  [ "$rc" -eq 2 ] || ok=0
  printf '%s' "$out" | grep -qF 'hermeticity refusal' || ok=0
  if [ "$ok" -eq 1 ]; then
    printf 'probe scenario=%s expect=exit2 got=exit%s verdict=pass\n' "$label" "$rc"
  else
    printf 'probe scenario=%s expect=exit2 got=exit%s verdict=fail\n' "$label" "$rc"
    FAILS=$((FAILS + 1))
  fi
}

scenario_matrix() {
  reset_sandbox
  expect clean-work-outside green

  mkdir -p -- "$ROOT/kasegi-r39-stray"; printf 'x\n' > "$ROOT/kasegi-r39-stray/leftover.txt"
  expect stray-r39-present red 'strays=kasegi-r39-stray' 'r39=present'

  mkdir -p -- "$ROOT/kasegi-r40-stray"; printf 'y\n' > "$ROOT/kasegi-r40-stray/leftover.txt"
  expect stray-r39-and-r40 red 'strays=kasegi-r39-stray,kasegi-r40-stray' 'r40=present'

  rm -rf -- "$ROOT/kasegi-r39-stray" "$ROOT/kasegi-r40-stray"
  expect strays-removed green

  # round-40 T5 sibling mutants (CritC1AntiSuite §2): every entry type is in scope
  mkdir -p -- "$ROOT/kasegi-r40-build-extra"
  expect sibling-unrelated-name red 'strays=kasegi-r40-build-extra'
  rm -rf -- "$ROOT/kasegi-r40-build-extra"
  mkdir -p -- "$ROOT/kasegi-r40x"
  expect sibling-prefix-adjacent red 'strays=kasegi-r40x'
  rmdir -- "$ROOT/kasegi-r40x"
  mkdir -p -- "$ROOT/.kasegi-r40-seat"
  expect sibling-dotdir red 'strays=.kasegi-r40-seat'
  rmdir -- "$ROOT/.kasegi-r40-seat"
  printf 'x\n' > "$ROOT/kasegi-r40-l1"
  expect sibling-file red 'strays=kasegi-r40-l1'
  rm -f -- "$ROOT/kasegi-r40-l1"
  mkdir -p -- "$ROOT/kasegi-foreign-target"
  ln -s -- "$ROOT/kasegi-foreign-target" "$ROOT/kasegi-r40-seat"
  expect sibling-symlink red 'strays=kasegi-r40-seat'
  rm -rf -- "$ROOT/kasegi-r40-seat" "$ROOT/kasegi-foreign-target"
  expect t5-mutants-cleared green

  # the run's own --work dir: tolerated by realpath, including a clean chain
  mkdir -p -- "$ROOT/kasegi-r40-seat/work"
  WORK=$ROOT/kasegi-r40-seat/work
  expect work-inside-clean-chain green 'work=inside' 'tolerated=kasegi-r40-seat'

  printf 'z\n' > "$ROOT/kasegi-r40-seat/leftover.txt"
  expect work-chain-contaminated red 'strays=kasegi-r40-seat'
  rm -f -- "$ROOT/kasegi-r40-seat/leftover.txt"

  # contents INSIDE the passed work dir must never red the run
  mkdir -p -- "$WORK/export" "$WORK/mut"; printf 'junk\n' > "$WORK/export/file"
  expect work-dir-contents-junk green 'tolerated=kasegi-r40-seat'

  # presence, not content: an empty stray reds; a non-round sibling does not
  mkdir -p -- "$ROOT/kasegi-r39-empty"
  expect empty-stray-dir red 'strays=kasegi-r39-empty'
  rmdir -- "$ROOT/kasegi-r39-empty"

  mkdir -p -- "$ROOT/kasegi-r41-stray" "$ROOT/gates-work"
  printf 'w\n' > "$ROOT/gates-work/file"
  expect non-round-siblings-ignored green 'strays=none'
  rm -rf -- "$ROOT/kasegi-r41-stray" "$ROOT/gates-work"

  # a matching-name symlink resolving to the passed work dir is tolerated by realpath
  ln -s -- "$WORK" "$ROOT/kasegi-r39-link"
  expect symlink-to-work-tolerated green 'tolerated=kasegi-r39-link'
  rm -f -- "$ROOT/kasegi-r39-link"

  # fail-closed: an entry we cannot resolve is RED
  mkdir -p -- "$ROOT/kasegi-r40-locked"
  chmod 000 -- "$ROOT/kasegi-r40-locked"
  expect unreadable-stray red 'strays=kasegi-r40-locked'
  chmod 700 -- "$ROOT/kasegi-r40-locked"
  rmdir -- "$ROOT/kasegi-r40-locked"

  # a work dir under a non-matching parent is simply out of the scan namespace
  rm -rf -- "$ROOT/kasegi-r40-seat"
  mkdir -p -- "$ROOT/seat/work"
  WORK=$ROOT/seat/work
  expect work-inside-unrelated-parent green 'work=inside' 'strays=none'
  rm -rf -- "$ROOT/seat"

  # final quiescent state: nothing matching, work outside again
  WORK=$SB/work
  expect final-clean green 'strays=none'

  # hermeticity: the live host root and any ancestor of it are refused (exit 2)
  expect_refusal hermeticity-real-root "$REAL_HYAKU"
  expect_refusal hermeticity-root-ancestor /fast/scratch
}

# ---- main ----------------------------------------------------------------

MODE=matrix
SCRATCH_ARG=''
WORK_ARG=''

while [ $# -gt 0 ]; do
  case $1 in
    --check) MODE=check; shift ;;
    --scratch-root)
      [ $# -ge 2 ] || die '--scratch-root needs a directory'
      SCRATCH_ARG=$2; shift 2 ;;
    --work)
      [ $# -ge 2 ] || die '--work needs a directory'
      WORK_ARG=$2; shift 2 ;;
    --root)
      [ $# -ge 2 ] || die '--root needs a directory'
      SB=$2; shift 2 ;;
    --keep) KEEP=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

if [ "$MODE" = check ]; then
  [ -n "$SCRATCH_ARG" ] || die '--check requires --scratch-root DIR'
  [ -n "$WORK_ARG" ] || die '--check requires --work DIR'
  refuse_real_root "$SCRATCH_ARG"
  emit_run "$SCRATCH_ARG" "$WORK_ARG"
  exit $?
fi

if [ -z "$SB" ]; then
  SB=$(mktemp -d "${TMPDIR:-/tmp}/h6-sibling-dir.XXXXXXXX") || die 'cannot create sandbox'
fi
case $SB in
  /*) ;;
  *) SB=$(realpath -m -- "$SB" 2>/dev/null) || die "cannot resolve --root: $SB" ;;
esac
refuse_real_root "$SB"
mkdir -p -- "$SB" || die "cannot create --root: $SB"
trap cleanup EXIT

printf 'probe mode=matrix scratch-root=%s sandbox=%s real-hyaku=%s real-root-read=no\n' \
  "$SB/scratch" "$SB" "$REAL_HYAKU"
printf 'probe policy=kasegi-r39*|kasegi-r40*,toleration=realpath-clean-chain,presence-is-red,unreadable-is-red\n'
scenario_matrix
printf '\nprobe scenarios=%s failures=%s\n' "$SCEN" "$FAILS"
[ "$FAILS" -eq 0 ] || exit 1
printf 'probe exit=0\n'
exit 0
