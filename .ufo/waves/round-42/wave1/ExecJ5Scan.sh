#!/usr/bin/env bash
# ExecJ5Scan.sh — round-42 J5 scratch-hygiene limb (sourceable bash).
#
# PURPOSE
#   J5 is the round-42 closure-suite check that audits the lane scratch area for
#   leftover entries of the lane round family (family F-SCAN).  It repairs the
#   two round-41 defects routed to round 42:
#     (a) the scan matched ONE literal round directory (the r39 limb looked
#         only under `kasegi-r39/`, the r40 limb only under `kasegi-r39*` and
#         `kasegi-r40*`), so a leftover SIBLING round directory was invisible
#         to it;
#     (b) the scan looked only INSIDE the configured scratch root, so a
#         leftover OUTSIDE that root was invisible to it
#         (.ufo/waves/round-41/wave2/MutScratchTiming.md).
#
# CONTRACT (what the suite calls)
#   check_j5 [--root DIR] [--work DIR] [--outside-root DIR]
#       --root         the configured scratch root to audit (the suite's
#                      --scratch-root).  REQUIRED unless the environment
#                      supplies it.  There is NO host default: a suite that
#                      passes no root gets read=fail, never a vacuous green.
#                      Only entries BENEATH this root are evaluated.
#       --work         this run's own --work dir.  REQUIRED unless the
#                      environment supplies it.  Everything on WORK's path
#                      (WORK itself, its contents, and its real-dir ancestors)
#                      is tolerated; a family SYMLINK that resolves to a WORK
#                      ancestor is NOT (the round-40 wave-2 F5 escape).
#       --outside-root the scratch root whose PARENT is audited for
#                      outside-the-root leftovers.  Default:
#                      $WORK/j5-fixture/scratch, materialized on demand.  Its
#                      parent is a tree the suite owns, so the outside limb
#                      never reads host-global state.
#       Positional arguments are ignored, so the suite's r41-style
#       `check_<id> TREE REF` dispatch shape cannot silently repoint this
#       check at the export tree.
#       Prints exactly one line:
#           J5 payload=strays=<n>,outside=<n>,read=<ok|fail>,scanned=<n>,scope=<on|off> closed=<0|1>
#       exit 0 (closed=1) only when read=ok and strays=0 and outside=0.
#       With no flags the inputs come from the environment, in this order:
#         root         = $J5_SCRATCH_ROOT, else $SCRATCH_ROOT
#         work         = $J5_WORK, else $WORK
#         outside-root = $J5_OUTSIDE_ROOT, else $WORK/j5-fixture/scratch
#
#   j5_scan_root  ROOT WORK                -> "strays=N,read=ok|fail,scanned=N"
#   j5_scan_scope SCOPE WORK EXCL          -> "outside=N,read=ok|fail,scanned=N"
#   j5_scan_pair  ROOT WORK [OUTSIDE_ROOT] -> the combined payload (no prefix)
#   check_j5_detail ROOT WORK [OUTSIDE_ROOT] -> payload + one line per stray
#   j5_fixture_init DIR -> materializes a deterministic fixture tree under DIR
#                and prints "scope=<DIR> root=<DIR>/scratch".  The suite uses it
#                so the outside limb runs on a MATERIALIZED tree (never on
#                host-global state) and the selftest populates it.
#
# FAMILY
#   The family is a SHAPE, not one literal round directory: the default
#   J5_FAMILY_GLOB is `kasegi-r4[0-9]*`, so every round in the r4x decade
#   (kasegi-r40, kasegi-r41, kasegi-r42, ... kasegi-r49) is in scope.  The
#   round-39 limb looked only under the literal `kasegi-r39/` and the round-40
#   limb only under `kasegi-r39*`/`kasegi-r40*`, so a sibling round container
#   was invisible to both.  Matching is case-insensitive and
#   separator-insensitive (every run of non-alphanumeric characters folds to a
#   single '-', so `Kasegi_R41`, `.kasegi-r41` and `kasegi-r41` all match) and
#   leading dots are ignored, as the round-40 and round-41 limbs established.
#   Override with J5_FAMILY_GLOB (a colon-separated list of globs; a name
#   matches when it matches ANY of them).
#
# WHAT COUNTS AS A STRAY
#   A family-shaped DIRECTORY is a container; its DIRECT children are the
#   seat-level entries.  Each child that is not on this run's own path is one
#   stray — this is the "seat-named stray" rule: a leftover seat directory is
#   detected even when its round container is this run's own.  A family-shaped
#   container with no children at all is itself one stray (a seat that merely
#   emptied its scratch still left the entry).  A family-shaped SYMLINK is one
#   stray unless it resolves to WORK or inside WORK: a symlink resolving to a
#   WORK ancestor stays red (F5 escape).  A family-shaped regular FILE is one
#   stray.  A family-shaped child of a container is not counted twice: the
#   recursive traversal visits it and grades it there.
#   The outside limb audits the PARENT of the outside root with the same unit
#   rule and excludes the outside root and everything beneath it.  That is the
#   MutScratchTiming shape: a leftover sibling of the configured root.
#
# FAIL-CLOSED
#   A missing or unreadable root, an unresolvable WORK, a find error, or an
#   unreadable scope yields read=fail and closed=0.  Never "zero entries, so
#   clean".
#
# USAGE (direct execution; sourcing defines the functions and runs nothing)
#   bash ExecJ5Scan.sh --check  --root DIR --work DIR [--outside-root DIR]
#   bash ExecJ5Scan.sh --detail --root DIR --work DIR [--outside-root DIR]
#   bash ExecJ5Scan.sh --self-test [--sandbox DIR]
#   bash ExecJ5Scan.sh --replay-defeats [--sandbox DIR]
#   bash ExecJ5Scan.sh --help
#
# Exit codes: 0 green / probe clean, 1 red / probe failure, 2 harness error.

J5_FAMILY_GLOB=${J5_FAMILY_GLOB:-kasegi-r4[0-9]*}

# ---------------------------------------------------------------- primitives

j5_die() { printf 'ExecJ5Scan: %s\n' "$*" >&2; exit 2; }

# j5_normalize_into NAME -> the normalized name in the global j5_norm:
# leading dots stripped, case folded, every run of non-alphanumeric characters
# folded to a single '-', trailing '-' stripped.
j5_norm=''
j5_normalize_into() {
  local n=$1 out='' c prevdash=0 i len
  while [ "${n#.}" != "$n" ]; do n=${n#.}; done
  n=${n,,}
  len=${#n}
  for (( i = 0; i < len; i++ )); do
    c=${n:i:1}
    case $c in
      [a-z0-9]) out+=$c; prevdash=0 ;;
      *) if [ "$prevdash" -eq 0 ]; then out+='-'; prevdash=1; fi ;;
    esac
  done
  while [ "${out%-}" != "$out" ]; do out=${out%-}; done
  j5_norm=$out
}

j5_normalize() { j5_normalize_into "$1"; printf '%s' "$j5_norm"; }

# j5_is_family_raw NAME -> 0 when the normalized name has the family shape; the
# result is published in the global j5_hit so the scan loop never forks a
# command substitution per entry.
J5_HIT=0
j5_is_family_raw() {
  local n=$1 g
  j5_normalize_into "$n"
  J5_HIT=0
  local IFS=:
  for g in $J5_FAMILY_GLOB; do
    case $j5_norm in
      $g) J5_HIT=1; break ;;
    esac
  done
}

j5_is_family() {
  j5_is_family_raw "$1"
  [ "$J5_HIT" -eq 1 ]
}

# j5_prefilter_one GLOB -> a `find -iname` pattern that is a strict SUPERSET of
# the names j5_is_family_raw accepts for that glob.  Every separator run of
# the family token becomes '*' and every bracket class becomes '?'.  The bash
# test stays authoritative: the prefilter only decides what is printed, never
# whether an entry is a stray.
j5_prefilter_one() {
  local glob=$1 p='' i c n
  n=${#glob}; i=0
  while [ "$i" -lt "$n" ]; do
    c=${glob:i:1}
    case $c in
      -|_) p="${p}*" ;;
      '[')
        p="${p}?"
        while [ "$i" -lt "$n" ]; do
          i=$((i + 1)); c=${glob:i:1}
          [ "$c" = ']' ] && break
        done ;;
      '*') p="${p}*" ;;
      *) p="${p}$c" ;;
    esac
    i=$((i + 1))
  done
  [ -n "$p" ] || p='*'
  printf '*%s*' "$p"
}

# j5_build_prefilter -> the find(1) predicate for the family shape, as an
# argv array:  ( -iname PAT1 -o -iname PAT2 ... )
J5_PREFILTER_ARGS=()
j5_build_prefilter() {
  local glob pat first=1
  J5_PREFILTER_ARGS=( '(' )
  local IFS=:
  for glob in $J5_FAMILY_GLOB; do
    pat=$(j5_prefilter_one "$glob")
    if [ "$first" -eq 0 ]; then J5_PREFILTER_ARGS+=( -o ); fi
    first=0
    J5_PREFILTER_ARGS+=( -iname "$pat" )
  done
  J5_PREFILTER_ARGS+=( ')' )
}

# j5_canon PATH -> the canonical (symlink-resolved) absolute path, or the
# empty string when PATH cannot be resolved.
j5_canon() {
  local p=$1
  [ -n "$p" ] || return 1
  realpath -m -- "$p" 2>/dev/null || return 1
}

# j5_own REAL WORK -> 0 when the entry with canonical path REAL lies on this
# run's own path: WORK itself, something inside WORK, or a real-dir ancestor of
# WORK.  Symlink handling is decided by the caller (a family symlink is never
# tolerated as an ancestor).
j5_own() {
  local real=$1 work=$2
  [ -n "$real" ] && [ -n "$work" ] || return 1
  [ "$real" = "$work" ] && return 0
  case "$real" in "$work"/*) return 0 ;; esac
  case "$work" in "$real"/*) return 0 ;; esac
  return 1
}

# j5_under REAL BASE -> 0 when REAL is BASE or lies beneath it.
j5_under() {
  local real=$1 base=$2
  [ -n "$real" ] && [ -n "$base" ] || return 1
  [ "$real" = "$base" ] && return 0
  case "$real" in "$base"/*) return 0 ;; esac
  return 1
}

# ------------------------------------------------------------------- scanner

J5_STRAYS=0
J5_OUTSIDE=0
J5_READ=ok
J5_SCANNED=0
J5_NAMES=''
J5_OUTSIDE_NAMES=''
J5_ERROR=none

j5_reset() {
  J5_STRAYS=0
  J5_OUTSIDE=0
  J5_READ=ok
  J5_SCANNED=0
  J5_NAMES=''
  J5_OUTSIDE_NAMES=''
  J5_ERROR=none
}

# j5_add_name VAR PATH -> append one stray path to a newline-delimited list.
j5_add_name() {
  if [ -z "${!1}" ]; then printf -v "$1" '%s' "$2"; else printf -v "$1" '%s\n%s' "${!1}" "$2"; fi
}

# j5_count_units BASE EXCL WORK
#   The unit rule, shared by both limbs.  Enumerates the family-shaped entries
#   under BASE and counts the seat-level strays.  EXCL (canonical) is a
#   subtree that is not this limb's business (the other limb's root).
#   Sets J5_STRAYS/J5_READ/J5_SCANNED/J5_NAMES.
j5_count_units() {
  local base=$1 excl=${2:-} work=${3:-}
  local tmpd rc errf
  local base_real='' work_real='' excl_real='' p rel creal child creal2
  local -a pred=()
  local i kids

  if [ -z "$base" ] || [ ! -d "$base" ]; then J5_READ=fail; J5_ERROR=missing-root; return 1; fi
  if [ -z "$work" ] || [ ! -d "$work" ]; then J5_READ=fail; J5_ERROR=missing-work; return 1; fi
  base_real=$(j5_canon "$base") || { J5_READ=fail; J5_ERROR=unresolvable-root; return 1; }
  work_real=$(j5_canon "$work") || { J5_READ=fail; J5_ERROR=unresolvable-work; return 1; }
  if [ -n "$excl" ]; then excl_real=$(j5_canon "$excl") || excl_real=''; fi

  j5_build_prefilter
  pred=( "${J5_PREFILTER_ARGS[@]}" )

  tmpd=$(mktemp -d "${TMPDIR:-/tmp}/j5scan.XXXXXXXX") || { J5_READ=fail; J5_ERROR=mktemp-failed; return 1; }
  errf=$tmpd/err
  : > "$errf"
  find "$base_real" -mindepth 1 "${pred[@]}" -print0 > "$tmpd/out" 2> "$errf"
  rc=$?
  if [ "$rc" -ne 0 ] || [ -s "$errf" ]; then
    J5_READ=fail
    J5_ERROR=$(sed -n '1{s/^find: //; s/: Permission denied.*/:permission-denied/; s/: No such file.*/:no-such-file/; p;}' "$errf" | tr '\n' ' ')
    [ -n "$J5_ERROR" ] || J5_ERROR="find-exit-$rc"
  fi

  while IFS= read -r -d '' p; do
    [ -n "$p" ] || continue
    J5_SCANNED=$((J5_SCANNED + 1))
    j5_is_family_raw "${p##*/}"
    [ "$J5_HIT" -eq 1 ] || continue
    creal=$(j5_canon "$p") || creal=$p
    rel=${p#"$base_real"/}
    if [ -n "$excl_real" ] && j5_under "$creal" "$excl_real"; then continue; fi

    if [ -L "$p" ]; then
      # A family symlink is a unit in its own right: tolerated only when it
      # resolves to WORK itself or inside WORK.  A symlink that resolves to a
      # WORK ancestor stays red (round-40 wave-2 F5 escape).
      if [ "$creal" = "$work_real" ]; then continue; fi
      case "$creal" in "$work_real"/*) continue ;; esac
      J5_STRAYS=$((J5_STRAYS + 1))
      j5_add_name J5_NAMES "$rel"
      continue
    fi

    if [ ! -d "$p" ]; then
      # A family-shaped regular file is a leftover too (round-40 wave-2 m10).
      if j5_own "$creal" "$work_real"; then continue; fi
      J5_STRAYS=$((J5_STRAYS + 1))
      j5_add_name J5_NAMES "$rel"
      continue
    fi

    # A family-shaped directory is a container: its direct children are the
    # seat-level entries.  Each one that is not on this run's own path is a
    # stray.  A family-shaped child is not counted here: the recursive
    # traversal visits it and grades it there (no double count).
    j5_count_container "$p" "$creal" "$work_real" "$base_real"
  done < "$tmpd/out"

  # The configured root itself, when it carries the family shape, is a
  # container too: its direct children are the seat-level entries.  (When the
  # root is not family-shaped this adds nothing.)
  j5_is_family_raw "${base_real##*/}"
  if [ "$J5_HIT" -eq 1 ]; then
    j5_count_container "$base_real" "$base_real" "$work_real" "$base_real"
  fi

  rm -rf -- "$tmpd"

  if [ "$J5_READ" = ok ] && [ "$J5_STRAYS" -eq 0 ]; then return 0; fi
  return 1
}

# j5_count_container CONTAINER CREAL WORK_REAL BASE_REAL
#   Counts the seat-level units directly inside a family-shaped container.
#   Each child that is not on this run's own path is one stray.  A
#   family-shaped child is skipped: the recursive traversal visits it and
#   grades it there, so nothing is counted twice.  A container with no
#   children at all is itself one leftover.
j5_count_container() {
  local p=$1 creal=$2 work_real=$3 base_real=$4
  local child creal2 kids=0
  while IFS= read -r -d '' child; do
    [ -n "$child" ] || continue
    kids=1
    creal2=$(j5_canon "$child") || creal2=$child
    if j5_own "$creal2" "$work_real"; then continue; fi
    j5_is_family_raw "${child##*/}"
    if [ "$J5_HIT" -eq 1 ] && [ ! -L "$child" ]; then continue; fi
    J5_STRAYS=$((J5_STRAYS + 1))
    j5_add_name J5_NAMES "${child#"$base_real"/}"
  done < <(find "$p" -mindepth 1 -maxdepth 1 -print0 2>/dev/null)
  if [ "$kids" -eq 0 ]; then
    # An empty family container is itself one leftover.
    if ! j5_own "$creal" "$work_real"; then
      J5_STRAYS=$((J5_STRAYS + 1))
      j5_add_name J5_NAMES "${p#"$base_real"/}"
    fi
  fi
}

# j5_count_entries BASE EXCL WORK
#   The OUTSIDE unit rule: every family-shaped ENTRY under BASE that is not on
#   this run's own path is one stray.  This is the shape the round-41 outside
#   defect asks for: the parent of the configured scratch root is scanned for
#   kasegi-r4[0-9]* entries, and each such entry is a leftover.
#   Sets J5_STRAYS/J5_READ/J5_SCANNED/J5_NAMES.
j5_count_entries() {
  local base=$1 excl=${2:-} work=${3:-}
  local tmpd rc errf
  local base_real='' work_real='' excl_real='' p rel creal
  local -a pred=()
  local i

  if [ -z "$base" ] || [ ! -d "$base" ]; then J5_READ=fail; J5_ERROR=missing-root; return 1; fi
  if [ -z "$work" ] || [ ! -d "$work" ]; then J5_READ=fail; J5_ERROR=missing-work; return 1; fi
  base_real=$(j5_canon "$base") || { J5_READ=fail; J5_ERROR=unresolvable-root; return 1; }
  work_real=$(j5_canon "$work") || { J5_READ=fail; J5_ERROR=unresolvable-work; return 1; }
  if [ -n "$excl" ]; then excl_real=$(j5_canon "$excl") || excl_real=''; fi

  j5_build_prefilter
  pred=( "${J5_PREFILTER_ARGS[@]}" )

  tmpd=$(mktemp -d "${TMPDIR:-/tmp}/j5entry.XXXXXXXX") || { J5_READ=fail; J5_ERROR=mktemp-failed; return 1; }
  errf=$tmpd/err
  : > "$errf"
  find "$base_real" -mindepth 1 "${pred[@]}" -print0 > "$tmpd/out" 2> "$errf"
  rc=$?
  if [ "$rc" -ne 0 ] || [ -s "$errf" ]; then
    J5_READ=fail
    J5_ERROR=$(sed -n '1{s/^find: //; s/: Permission denied.*/:permission-denied/; s/: No such file.*/:no-such-file/; p;}' "$errf" | tr '\n' ' ')
    [ -n "$J5_ERROR" ] || J5_ERROR="find-exit-$rc"
  fi
  while IFS= read -r -d '' p; do
    [ -n "$p" ] || continue
    J5_SCANNED=$((J5_SCANNED + 1))
    j5_is_family_raw "${p##*/}"
    [ "$J5_HIT" -eq 1 ] || continue
    creal=$(j5_canon "$p") || creal=$p
    rel=${p#"$base_real"/}
    if [ -n "$excl_real" ] && j5_under "$creal" "$excl_real"; then continue; fi
    if j5_own "$creal" "$work_real"; then continue; fi
    J5_STRAYS=$((J5_STRAYS + 1))
    j5_add_name J5_NAMES "$rel"
  done < "$tmpd/out"
  rm -rf -- "$tmpd"

  if [ "$J5_READ" = ok ] && [ "$J5_STRAYS" -eq 0 ]; then return 0; fi
  return 1
}

# j5_scan_root ROOT WORK -> "strays=N,read=ok|fail,scanned=N"; exit 0/1.
j5_scan_root() {
  local root=${1:-} work=${2:-}
  local rc
  j5_reset
  if [ -z "$root" ] || [ ! -d "$root" ]; then
    J5_READ=fail; J5_ERROR=missing-root
    printf 'strays=0,read=fail,scanned=0\n'
    return 1
  fi
  j5_count_units "$root" '' "$work"
  rc=$?
  printf 'strays=%s,read=%s,scanned=%s\n' "$J5_STRAYS" "$J5_READ" "$J5_SCANNED"
  return "$rc"
}

# j5_scan_scope SCOPE WORK EXCL -> "outside=N,read=ok|fail,scanned=N".
#   SCOPE is scanned for family-shaped ENTRIES; each one that is neither the
#   excluded subtree nor on this run's own path is one outside stray.
j5_scan_scope() {
  local scope=${1:-} work=${2:-} excl=${3:-}
  local rc excl_real=''
  j5_reset
  if [ -z "$scope" ] || [ ! -d "$scope" ]; then
    J5_READ=fail; J5_ERROR=missing-scope
    printf 'outside=0,read=fail,scanned=0\n'
    return 1
  fi
  if [ -n "$excl" ]; then excl_real=$(j5_canon "$excl") || excl_real=''; fi
  j5_count_entries "$scope" "$excl_real" "$work"
  rc=$?
  printf 'outside=%s,read=%s,scanned=%s\n' "$J5_STRAYS" "$J5_READ" "$J5_SCANNED"
  return "$rc"
}

# j5_scan_pair ROOT WORK [OUTSIDE_ROOT] -> the combined payload; exit 0/1.
#   The outside limb audits the PARENT of OUTSIDE_ROOT, excluding OUTSIDE_ROOT
#   and everything beneath it.  OUTSIDE_ROOT defaults to $WORK/j5-fixture/
#   scratch, which the suite owns, so no host-global state is read.
j5_scan_pair() {
  local root=${1:-} work=${2:-} oroot=${3:-}
  local out rc s1 r1 c1 outside=0 r2='ok' c2=0 read scopestate=on
  local scope='' oroot_real=''
  if [ -z "$oroot" ] && [ -n "$work" ]; then oroot="$work/j5-fixture/scratch"; fi
  out=$(j5_scan_root "$root" "$work"); rc=$?
  s1=${out#strays=}; s1=${s1%%,*}
  r1=${out#*read=}; r1=${r1%%,*}
  c1=${out##*scanned=}
  if [ -n "$oroot" ] && [ "$oroot" != '-' ]; then
    scope=$(dirname -- "$oroot")
    oroot_real=$(j5_canon "$oroot") || oroot_real=''
    # The outside scope is the PARENT of the outside root: a leftover sibling
    # of the configured root is the shape the round-41 defect describes.
    # The outside root itself is materialized on demand so the default path is
    # always a real tree (never a missing directory).
    mkdir -p -- "$oroot" 2>/dev/null || true
    local o2
    o2=$(j5_scan_scope "$scope" "$work" "$oroot_real")
    outside=${o2#outside=}; outside=${outside%%,*}
    r2=${o2#*read=}; r2=${r2%%,*}
    c2=${o2##*scanned=}
  else
    scopestate=off
  fi
  read=ok
  [ "$r1" = ok ] || read=fail
  [ "$r2" = ok ] || read=fail
  [ "$s1" -eq 0 ] || rc=1
  [ "$outside" -eq 0 ] || rc=1
  [ "$read" = ok ] || rc=1
  printf 'strays=%s,outside=%s,read=%s,scanned=%s,scope=%s\n' \
    "$s1" "$outside" "$read" "$((c1 + c2))" "$scopestate"
  return "$rc"
}

# check_j5 [--root DIR] [--work DIR] [--outside-root DIR] [ignored...] -> payload.
check_j5() {
  local root='' work='' oroot='' have_oroot=0
  while [ $# -gt 0 ]; do
    case $1 in
      --root) [ $# -ge 2 ] || j5_die '--root needs a directory'; root=$2; shift 2 ;;
      --work) [ $# -ge 2 ] || j5_die '--work needs a directory'; work=$2; shift 2 ;;
      --outside-root) [ $# -ge 2 ] || j5_die '--outside-root needs a directory'; oroot=$2; have_oroot=1; shift 2 ;;
      *) shift ;;
    esac
  done
  [ -n "$root" ] || root=${J5_SCRATCH_ROOT:-${SCRATCH_ROOT:-}}
  [ -n "$work" ] || work=${J5_WORK:-${WORK:-}}
  if [ "$have_oroot" -eq 0 ]; then
    if [ -n "${J5_OUTSIDE_ROOT:-}" ]; then oroot=$J5_OUTSIDE_ROOT; fi
  fi
  local out rc closed=0
  out=$(j5_scan_pair "$root" "$work" "$oroot")
  rc=$?
  [ "$rc" -eq 0 ] && closed=1
  printf 'J5 payload=%s closed=%s\n' "$out" "$closed"
  return "$rc"
}

# check_j5_detail ROOT WORK [OUTSIDE_ROOT] -> the payload plus one line per stray.
check_j5_detail() {
  local root=${1:-} work=${2:-} oroot=${3:-}
  local out rc n scope='' oroot_real=''
  if [ -z "$oroot" ] && [ -n "$work" ]; then oroot="$work/j5-fixture/scratch"; fi
  j5_reset
  j5_count_units "$root" '' "$work"
  local in_names=$J5_NAMES
  j5_reset
  if [ -n "$oroot" ] && [ "$oroot" != '-' ]; then
    scope=$(dirname -- "$oroot")
    oroot_real=$(j5_canon "$oroot") || oroot_real=''
    mkdir -p -- "$oroot" 2>/dev/null || true
    j5_count_entries "$scope" "$oroot_real" "$work"
    J5_OUTSIDE_NAMES=$J5_NAMES
  fi
  local out_names=$J5_OUTSIDE_NAMES
  out=$(j5_scan_pair "$root" "$work" "$oroot"); rc=$?
  printf '%s\n' "$out"
  printf 'scope=%s\n' "${scope:-none}"
  while IFS= read -r n; do [ -n "$n" ] && printf 'stray: %s\n' "$n"; done <<< "$in_names"
  while IFS= read -r n; do [ -n "$n" ] && printf 'outside-stray: %s\n' "$n"; done <<< "$out_names"
  return "$rc"
}

# j5_fixture_init DIR -> materialize a deterministic fixture tree under DIR and
# print "scope=<DIR> root=<DIR>/scratch".  The suite uses it so the outside
# limb runs on a materialized tree instead of on host-global state, and the
# selftest populates it with the defeat fixtures.
j5_fixture_init() {
  local d=${1:-}
  [ -n "$d" ] || j5_die 'j5_fixture_init needs a directory'
  mkdir -p -- "$d/scratch" || j5_die "cannot create fixture: $d"
  printf 'scope=%s root=%s/scratch\n' "$d" "$d"
}

# --------------------------------------------------------------------- probe

j5_probe_failures=0
j5_probe_cases=0

# j5_expect LABEL EXPECT ROOT WORK OUTSIDE_ROOT [needle...]
j5_expect() {
  local label=$1 want=$2 root=$3 work=$4 oroot=$5
  shift 5
  local out rc needle ok=1 got pos verdict
  j5_probe_cases=$((j5_probe_cases + 1))
  out=$(j5_scan_pair "$root" "$work" "$oroot"); rc=$?
  if [ "$rc" -eq 0 ]; then got=green; else got=red; fi
  [ "$got" = "$want" ] || ok=0
  for needle in "$@"; do
    printf '%s' "$out" | grep -qF -- "$needle" || ok=0
  done
  if [ "$ok" -eq 1 ]; then pos=pass; verdict=pass; else pos=fail; verdict=fail; fi
  printf 'selftest case=J5 %s expect=%s got=%s positive=%s verdict=%s payload=%s\n' \
    "$label" "$want" "$got" "$pos" "$verdict" "$out"
  [ "$ok" -eq 1 ] && return 0
  j5_probe_failures=$((j5_probe_failures + 1))
  return 1
}

j5_sandbox() {
  local sb=${1:-}
  if [ -z "$sb" ]; then
    sb=$(mktemp -d "${TMPDIR:-/tmp}/j5scan-probe.XXXXXXXX") || { j5_die 'cannot create sandbox'; return 1; }
  else
    mkdir -p -- "$sb" || { j5_die "cannot create sandbox: $sb"; return 1; }
    sb=$(realpath -m -- "$sb") || { j5_die "cannot resolve sandbox: $sb"; return 1; }
  fi
  printf '%s' "$sb"
}

j5_selftest() {
  local sb
  sb=$(j5_sandbox "${1:-}") || return 1
  trap 'rm -rf -- "$sb"' EXIT

  local root="$sb/scratch" work="$sb/work" oroot="$sb/fixture/scratch"
  rm -rf -- "$root" "$work" "$sb/fixture"
  mkdir -p -- "$root" "$work" "$oroot"

  printf 'selftest probe sandbox=%s family=%s live-root-read=no\n' "$sb" "$J5_FAMILY_GLOB"
  printf 'selftest policy=family-shape,case-insensitive,separator-insensitive,recursive,dot-inclusive,fail-closed,outside-scope=materialized-fixture-parent\n'

  # 1. clean tree -> green
  j5_expect clean-green green "$root" "$work" "$oroot" 'strays=0,outside=0,read=ok'

  # 2. the r41 literal-prefix escape: a SIBLING round container
  mkdir -p -- "$root/kasegi-r40/SeatX"
  j5_expect sibling-round-red red "$root" "$work" "$oroot" 'strays=1,outside=0'
  rm -rf -- "$root/kasegi-r40"

  # 3. the current-round container with a foreign seat
  mkdir -p -- "$root/kasegi-r42/OtherSeat"
  j5_expect foreign-seat-red red "$root" "$work" "$oroot" 'strays=1,outside=0'
  rm -rf -- "$root/kasegi-r42"

  # 4. both planted at once -> two strays
  mkdir -p -- "$root/kasegi-r41/SeatX" "$root/kasegi-r42/OtherSeat"
  j5_expect two-planted-red red "$root" "$work" "$oroot" 'strays=2,outside=0'
  rm -rf -- "$root/kasegi-r41" "$root/kasegi-r42"

  # 5. the MutScratchTiming escape: a leftover OUTSIDE the configured root
  mkdir -p -- "$sb/fixture/kasegi-r41/SeatX"
  j5_expect outside-root-red red "$root" "$work" "$oroot" 'strays=0,outside=1'
  rm -rf -- "$sb/fixture/kasegi-r41"

  # 6. this run's own work dir is never a stray
  mkdir -p -- "$root/kasegi-r42/work"
  j5_expect own-work-green green "$root" "$root/kasegi-r42/work" "$oroot" 'strays=0,outside=0'
  mkdir -p -- "$root/kasegi-r42/work/kasegi-r40/inner"
  j5_expect own-work-contents-green green "$root" "$root/kasegi-r42/work" "$oroot" 'strays=0,outside=0'
  rm -rf -- "$root/kasegi-r42"

  # 7. the round-40 F5 escape: a family symlink resolving to a WORK ancestor
  mkdir -p -- "$root/kasegi-r41-container/work"
  ln -s -- "$root" "$root/kasegi-r41-link"
  j5_expect family-symlink-red red "$root" "$root/kasegi-r41-container/work" "$oroot" 'strays=1'
  rm -f -- "$root/kasegi-r41-link"
  rm -rf -- "$root/kasegi-r41-container"

  # 8. r41 replayed mutants: dot-prefixed, case/separator variant, nested
  mkdir -p -- "$root/.kasegi-r41-dot"
  j5_expect dot-prefixed-red red "$root" "$work" "$oroot" 'strays=1'
  rm -rf -- "$root/.kasegi-r41-dot"
  mkdir -p -- "$root/Kasegi_R41-stray"
  j5_expect case-separator-red red "$root" "$work" "$oroot" 'strays=1'
  rm -rf -- "$root/Kasegi_R41-stray"
  mkdir -p -- "$root/container/kasegi-r41-nested"
  j5_expect nested-red red "$root" "$work" "$oroot" 'strays=1'
  rm -rf -- "$root/container"

  # 9. an empty family container is itself one leftover
  mkdir -p -- "$root/kasegi-r40"
  j5_expect empty-container-red red "$root" "$work" "$oroot" 'strays=1'
  rm -rf -- "$root/kasegi-r40"

  # 10. a family-shaped regular file is a leftover too (r40 wave-2 m10)
  : > "$root/kasegi-r40-file"
  j5_expect family-file-red red "$root" "$work" "$oroot" 'strays=1'
  rm -f -- "$root/kasegi-r40-file"

  # 11. a family-shaped CONFIGURED ROOT: its seat-level children are units too
  mkdir -p -- "$root/kasegi-r42/SeatX"
  j5_expect family-shaped-root-red red "$root/kasegi-r42" "$work" "$oroot" 'strays=1,outside=0'
  rm -rf -- "$root/kasegi-r42"

  # 12. fail-closed: missing root and unresolvable work
  j5_expect missing-root-red red "$root/nope" "$work" "$oroot" 'read=fail'
  j5_expect missing-work-red red "$root" "$sb/nope" "$oroot" 'read=fail'

  printf 'selftest cases=%s failures=%s\n' "$j5_probe_cases" "$j5_probe_failures"
  if [ "$j5_probe_failures" -eq 0 ]; then
    printf 'selftest verdict=pass\n'
    return 0
  fi
  printf 'selftest verdict=fail\n'
  return 1
}

# j5_replay_defeats -- re-execute the COMMITTED round-40/round-41 defeat
# artifacts against the CURRENT limb bytes and require rejection.  The two
# artifacts are:
#   D-A  the sibling-round-prefix defeat: a leftover `kasegi-r40` container.
#        The r39 limb looked only under the literal `kasegi-r39/` and the r40
#        limb only under `kasegi-r39*`/`kasegi-r40*`, so this input was
#        accepted (green) by those bytes.
#   D-B  the outside-configured-root defeat: a leftover `kasegi-r41` container
#        that is a SIBLING of the configured root (the MutScratchTiming shape,
#        .ufo/waves/round-41/wave2/MutScratchTiming.md).  The r41 I6 limb
#        looked only inside the configured root, so this input was accepted.
# A replay that is NOT rejected is a FAIL and the probe exits 1.
j5_replay_defeats() {
  local sb
  sb=$(j5_sandbox "${1:-}") || return 1
  trap 'rm -rf -- "$sb"' EXIT
  local root="$sb/scratch" work="$sb/work" oroot="$sb/fixture/scratch"
  rm -rf -- "$root" "$work" "$sb/fixture"
  mkdir -p -- "$root" "$work" "$oroot"

  printf 'replay probe sandbox=%s family=%s\n' "$sb" "$J5_FAMILY_GLOB"

  # D-A: sibling round prefix inside the configured root
  mkdir -p -- "$root/kasegi-r40/SeatX"
  local out rc
  out=$(j5_scan_pair "$root" "$work" "$oroot"); rc=$?
  if [ "$rc" -ne 0 ]; then
    printf 'replay defeat=D-A sibling-round-prefix rejected=1 verdict=pass payload=%s\n' "$out"
  else
    printf 'replay defeat=D-A sibling-round-prefix rejected=0 verdict=FAIL payload=%s\n' "$out"
    j5_probe_failures=$((j5_probe_failures + 1))
  fi
  rm -rf -- "$root/kasegi-r40"

  # D-B: outside-configured-root stray
  mkdir -p -- "$sb/fixture/kasegi-r41/SeatX"
  out=$(j5_scan_pair "$root" "$work" "$oroot"); rc=$?
  if [ "$rc" -ne 0 ]; then
    printf 'replay defeat=D-B outside-configured-root rejected=1 verdict=pass payload=%s\n' "$out"
  else
    printf 'replay defeat=D-B outside-configured-root rejected=0 verdict=FAIL payload=%s\n' "$out"
    j5_probe_failures=$((j5_probe_failures + 1))
  fi
  rm -rf -- "$sb/fixture/kasegi-r41"

  # control: the same tree, clean, must stay green
  out=$(j5_scan_pair "$root" "$work" "$oroot"); rc=$?
  if [ "$rc" -eq 0 ]; then
    printf 'replay control=clean accepted=1 verdict=pass payload=%s\n' "$out"
  else
    printf 'replay control=clean accepted=0 verdict=FAIL payload=%s\n' "$out"
    j5_probe_failures=$((j5_probe_failures + 1))
  fi

  printf 'replay defeats=2 failures=%s\n' "$j5_probe_failures"
  if [ "$j5_probe_failures" -eq 0 ]; then
    printf 'replay verdict=pass\n'
    return 0
  fi
  printf 'replay verdict=fail\n'
  return 1
}

j5_usage() {
  sed -n '2,/^# Exit codes/p' "${BASH_SOURCE[0]}" | sed -e '$d' -e 's/^# \{0,1\}//'
}

j5_main() {
  local mode='' root='' work='' oroot='' sandbox='' rc
  while [ $# -gt 0 ]; do
    case $1 in
      --check|--detail|--self-test|--replay-defeats) mode=${1#--}; shift ;;
      --root) [ $# -ge 2 ] || j5_die '--root needs a directory'; root=$2; shift 2 ;;
      --work) [ $# -ge 2 ] || j5_die '--work needs a directory'; work=$2; shift 2 ;;
      --outside-root) [ $# -ge 2 ] || j5_die '--outside-root needs a directory'; oroot=$2; shift 2 ;;
      --sandbox) [ $# -ge 2 ] || j5_die '--sandbox needs a directory'; sandbox=$2; shift 2 ;;
      -h|--help) j5_usage; exit 0 ;;
      *) j5_die "unknown argument: $1" ;;
    esac
  done
  case $mode in
    self-test) j5_selftest "$sandbox"; exit $? ;;
    replay-defeats) j5_replay_defeats "$sandbox"; exit $? ;;
    check|detail)
      [ -n "$work" ] || j5_die "--$mode requires --work DIR"
      [ -n "$root" ] || j5_die "--$mode requires --root DIR"
      if [ "$mode" = check ]; then
        j5_scan_pair "$root" "$work" "$oroot"; rc=$?
      else
        check_j5_detail "$root" "$work" "$oroot"; rc=$?
      fi
      exit "$rc" ;;
    '') j5_die 'one of --check, --detail, --self-test, --replay-defeats is required' ;;
    *) j5_die "unknown mode: $mode" ;;
  esac
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  j5_main "$@"
fi
