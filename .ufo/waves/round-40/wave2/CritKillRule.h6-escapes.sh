#!/usr/bin/env bash
# CritKillRule.h6-escapes.sh — round-40 wave-2 attack fixture.
# Attacker: CritKillRule (critic seat, C1 kill rule).
# Target: the committed H6 limb of corpus/instruments/r40-closure.sh at J5
#   (3074c7679d6f527ec3930d7748ccce1dbae4a58a). The limb below is a verbatim
#   byte copy of the committed function (extracted with `git show`).
# Purpose: reproduce states where a real leftover scratch entry exists but the
#   frozen kill rule does NOT fire. Each scenario prints its verdict.
# Hermetic: refuses a scratch root that is /fast/scratch/hyaku or an ancestor
#   of it; creates everything under $ROOT; removes it on exit.
# usage: bash CritKillRule.h6-escapes.sh [ROOT]
set -u

# ---- verbatim committed limb (git show 3074c76:corpus/instruments/r40-closure.sh) ----
check_h6() { # TREE REF
  local root=$SCRATCH_ROOT
  local realw='' realroot='' e b r out
  local strays=0 read=ok
  if [ -z "${WORK:-}" ]; then
    printf 'strays=0,read=fail'
    return 1
  fi
  realw=$( cd "$WORK" 2>/dev/null && pwd -P ) || { printf 'strays=0,read=fail'; return 1; }
  if [ -d "$root" ]; then
    realroot=$( cd "$root" && pwd -P ) || { printf 'strays=0,read=fail'; return 1; }
    if ! out=$(find "$realroot" -mindepth 1 -maxdepth 1 -print 2>/dev/null); then
      printf 'strays=0,read=fail'
      return 1
    fi
    while IFS= read -r e; do
      [ -n "$e" ] || continue
      b=${e##*/}
      case $b in
        kasegi-r39*|kasegi-r40*) ;;
        *) continue ;;
      esac
      r=$( cd "$e" 2>/dev/null && pwd -P ) || { read=fail; continue; }
      case $realw in
        "$r"|"$r"/*) continue ;;
      esac
      # Any matching family entry that does not contain this run's --work dir is
      # a leftover: an EMPTY one counts too, because a seat that merely emptied
      # its scratch still left the entry at filing.
      strays=$((strays + 1))
    done <<< "$out"
  fi
  printf 'strays=%s,read=%s' "$strays" "$read"
  [ "$read" = ok ] && [ "$strays" -eq 0 ] && return 0
  return 1
}
# ---- end verbatim limb ----

ROOT=${1:-}
if [ -z "$ROOT" ]; then
  ROOT=$(mktemp -d "${TMPDIR:-/tmp}/h6esc.XXXXXX") || exit 2
else
  ROOT=$(realpath -m -- "$ROOT") || exit 2
  mkdir -p "$ROOT"
fi
trap 'rm -rf -- "$ROOT"' EXIT
case "$ROOT" in
  /|/fast|/fast/scratch|/fast/scratch/hyaku) echo "refuse: real host scratch root" >&2; exit 2 ;;
esac

run() { # LABEL EXPECT
  local label=$1 expect=$2
  local out rc got v
  out=$(SCRATCH_ROOT=$ROOT/scratch WORK=$ROOT/work check_h6); rc=$?
  got=$(printf '%s' "$out" | grep -o 'strays=[0-9]*' | head -1)
  if [ "$expect" = red ] && [ "$rc" -ne 0 ]; then v=pass
  elif [ "$expect" = green ] && [ "$rc" -eq 0 ]; then v=pass
  else v=FAIL; fi
  printf 'scenario=%-28s expect=%-5s rc=%s payload=%s verdict=%s\n' "$label" "$expect" "$rc" "$out" "$v"
  [ "$v" = pass ]
}

# scenario matrix (each scenario rebuilds the sandbox)
matrix() {
  rm -rf "$ROOT/scratch" "$ROOT/work"; mkdir -p "$ROOT/scratch" "$ROOT/work"
  run clean-control green
  rm -rf "$ROOT/scratch"; mkdir -p "$ROOT/scratch/kasegi-r40-stray"
  run m1-posctrl-straydir red
  rm -rf "$ROOT/scratch"; mkdir -p "$ROOT/scratch/.kasegi-r40-seat"
  run m2-dotfile-escape green
  rm -rf "$ROOT/scratch"; mkdir -p "$ROOT/scratch/Kasegi-r40-stray"
  run m3-uppercase-escape green
  rm -rf "$ROOT/scratch"; mkdir -p "$ROOT/scratch/$(printf 'kasegi\u2011r40\u2011stray')"
  run m4-nonbreakinghyphen-escape green
  rm -rf "$ROOT/scratch"; mkdir -p "$ROOT/scratch/container/kasegi-r40-stray"
  run m5-nested-under-container-escape green
  rm -rf "$ROOT/scratch"; mkdir -p "$ROOT/scratch" "$ROOT/work"; ln -s "$ROOT" "$ROOT/scratch/kasegi-r40-link"
  run m6-ancestor-symlink-escape green
  rm -rf "$ROOT/scratch"; mkdir -p "$ROOT/scratch" "$ROOT/work"; ln -s "$ROOT/work" "$ROOT/scratch/kasegi-r40-link"
  run m7-symlink-to-work-tolerated green
  rm -rf "$ROOT/scratch"; mkdir -p "$ROOT/scratch" "$ROOT/work"; ln -s "$ROOT/missing" "$ROOT/scratch/kasegi-r40-dangling"
  run m8-dangling-symlink-red red
  rm -rf "$ROOT/scratch"; mkdir -p "$ROOT/scratch/kasegi-r40-locked"; chmod 000 "$ROOT/scratch/kasegi-r40-locked"
  run m9-unreadable-dir-red red; chmod 755 "$ROOT/scratch/kasegi-r40-locked"
  rm -rf "$ROOT/scratch"; mkdir -p "$ROOT/scratch" "$ROOT/work"; touch "$ROOT/scratch/kasegi-r40-file"
  run m10-regular-file-red red
}

matrix
echo "escape-probe done root=$ROOT"
