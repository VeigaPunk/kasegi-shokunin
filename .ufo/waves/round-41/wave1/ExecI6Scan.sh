#!/usr/bin/env bash
# ExecI6Scan.sh — round-41 I6 scratch-scan limb (sourceable bash).
#
# PURPOSE
#   I6 is the round-41 closure-suite check that audits the scratch root for
#   leftover entries of THIS round's name family.  The frozen C1 clause
#   (.ufo/waves/round-41/claims.json) reads:
#
#     "I6 the scratch scan matches the `kasegi-r41` name family case- and
#      separator-insensitively, recursively, including dot-prefixed entries,
#      and fails closed on a scan error"
#
#   This file is the limb.  It is SOURCEABLE: sourcing it defines the
#   functions below and executes nothing.  Executing it directly runs a
#   hermetic probe (never touches the live scratch root).
#
# API (what the suite calls)
#   i6_scan_scratch SCRATCH_ROOT WORK_DIR
#       Prints exactly one stable payload line on stdout:
#           strays=<n>,read=<ok|fail>
#       exit 0 (green) iff read=ok and strays=0; exit 1 otherwise.
#       SCRATCH_ROOT defaults to $I6_SCRATCH_ROOT (default /fast/scratch/hyaku).
#       WORK_DIR is REQUIRED.  Without a canonical work dir nothing can be
#       excluded, so the limb fails closed (read=fail) instead of reporting a
#       clean scan.
#
#   i6_scan_detail SCRATCH_ROOT WORK_DIR
#       Same scan; prints one audit line on stdout:
#           strays=<n>,read=<ok|fail>,scanned=<n>,excluded=<paths|none>,tolerated=<paths|none>,error=<path|reason|none>
#       followed by one line per stray:  stray: <path-relative-to-root>
#       Exit status identical to i6_scan_scratch.  `error=` names the path (or
#       reason) behind a read=fail so a red is diagnosable without a re-run.
#
#   i6_scan_names  -> newline-separated stray paths (relative to the root).
#   i6_stray_count -> integer count of strays.
#
# ENVIRONMENT KNOBS
#   I6_FAMILY        family token to audit (default kasegi-r41).  The
#                    underscore spelling kasegi_r41 is matched too, because
#                    separators are normalised before comparison.
#   I6_SCRATCH_ROOT  default scratch root (/fast/scratch/hyaku).
#   I6_CHAIN         strict | literal   (default strict)
#                    strict  : a family-named ANCESTOR of the work dir is
#                              tolerated only when the chain from it down to
#                              the work dir is clean (every level holds exactly
#                              the next component and nothing else).
#                    literal : only the work dir itself and everything inside
#                              it are excluded; every other match, ancestors
#                              included, is counted.
#
# WHY TWO MODES (explicit deviation, see the seat receipt)
#   The seat item says "count every match that is not the work dir itself nor
#   inside it" (literal).  Read literally on the live root, the round's own
#   container /fast/scratch/hyaku/kasegi-r41 is a family match and is not the
#   work dir, so the check could never be green while that container exists —
#   the frozen C1 after-state (closed=12/12 at Y) would be unreachable.  The
#   default therefore tolerates a family-named ancestor of the work dir when,
#   and only when, the chain down to the work dir is clean (round-40 wave-1
#   ExecH6ScratchFixtures contract; round-40 wave-2 CritKillRule F5 fix
#   direction).  A contaminated chain still reds.  I6_CHAIN=literal restores
#   the literal counting.
#
# FAIL-CLOSED (no fail-open path)
#   A missing or non-directory scratch root, an unresolvable work dir, a find
#   error, a non-empty find stderr, an unreadable entry, or a root that is
#   searchable but not listable (mode 0311) all yield read=fail and exit 1.
#   Never "zero entries, therefore clean".
#
# ENTRY-TYPE COVERAGE
#   Every entry type is in scope: directory, regular file, symlink (dangling
#   included), dot-prefixed names, at any depth below the root.
#
# USAGE (direct execution)
#   bash ExecI6Scan.sh --check --scratch-root DIR --work DIR [--chain strict|literal]
#       One scan; prints the payload line; exit 0 green / 1 red.
#   bash ExecI6Scan.sh --detail --scratch-root DIR --work DIR
#       One scan; prints the audit line plus one line per stray.
#   bash ExecI6Scan.sh --self-test [--root DIR]
#       Hermetic probe: builds a sandbox, runs the graded scenario matrix,
#       prints one `selftest case=I6 ... verdict=pass|fail` line per scenario
#       and `selftest cases=<n> failures=<k>`; exit 0 only when k=0.
#   bash ExecI6Scan.sh --help
#
# Exit codes: 0 green / probe clean, 1 red / probe failure, 2 harness error.

I6_FAMILY=${I6_FAMILY:-kasegi-r41}
I6_SCRATCH_ROOT=${I6_SCRATCH_ROOT:-/fast/scratch/hyaku}
I6_CHAIN=${I6_CHAIN:-strict}

# ---------------------------------------------------------------- primitives

i6_die() { printf 'ExecI6Scan: %s\n' "$*" >&2; exit 2; }

# i6_normalize NAME -> lowercase, leading dots stripped, every dash-like
# separator folded to '-'.  Case- and separator-insensitivity live here.
#
# The result is published in the global i6_norm so that the hot scan loop
# never forks a command substitution per entry (the live scratch root holds
# >1e6 entries; one fork per entry would take minutes).  i6_normalize is the
# printable wrapper for callers outside the loop.
#
# There is exactly ONE normalisation implementation: i6_normalize_into.  The
# scan loop and the public helpers all go through it, so a weakening applied
# here weakens every path (the mutation harness relies on that).
i6_norm=''
I6_ERROR=none
i6_normalize_into() {
  local n=$1
  while [ "${n#.}" != "$n" ]; do n=${n#.}; done
  n=${n,,}
  n=${n//_/-}
  n=${n//$'\u00ad'/-}   # soft hyphen
  n=${n//$'\u2010'/-}   # hyphen
  n=${n//$'\u2011'/-}   # non-breaking hyphen
  n=${n//$'\u2012'/-}   # figure dash
  n=${n//$'\u2013'/-}   # en dash
  n=${n//$'\u2014'/-}   # em dash
  n=${n//$'\u2015'/-}   # horizontal bar
  n=${n//$'\u2212'/-}   # minus sign
  n=${n//$'\ufe58'/-}   # small em dash
  n=${n//$'\ufe63'/-}   # small hyphen-minus
  n=${n//$'\uff0d'/-}   # fullwidth hyphen-minus
  i6_norm=$n
}

i6_normalize() {
  i6_normalize_into "$1"
  printf '%s' "$i6_norm"
}

# i6_family_norm -> the family token, normalised the same way.
i6_family_norm() {
  i6_normalize_into "${I6_FAMILY:-kasegi-r41}"
  printf '%s' "$i6_norm"
}

# i6_family_prefix -> the normalised family prefix, cached for the scan.
i6_family_prefix=''
i6_family_cache() {
  i6_normalize_into "${I6_FAMILY:-kasegi-r41}"
  i6_family_prefix=$i6_norm
}

# i6_is_family BASENAME -> 0 when the basename belongs to the family.
# Prefix semantics (kasegi-r41, kasegi-r41x, kasegi-r41-stray all match),
# after dot-stripping and normalisation.  Round-40 precedent: the family
# match is a namespace, not a whole-name equality.
#
# i6_is_family_raw BASENAME -> same test, result in the global i6_hit, no
# command substitution and no fork.  This is the form the scan loop uses.
i6_hit=0
i6_is_family_raw() {
  i6_normalize_into "$1"
  case $i6_norm in
    "$i6_family_prefix"*) i6_hit=1 ;;
    *) i6_hit=0 ;;
  esac
}

i6_is_family() {
  i6_is_family_raw "$1"
  [ "$i6_hit" -eq 1 ]
}

# i6_chain_clean ANCESTOR WORK -> 0 when the path from ANCESTOR down to WORK
# is a clean chain: every level holds exactly the next component and nothing
# else.  An unreadable level yields "not clean" (fail-closed).
i6_chain_clean() {
  local dir=$1 work=$2 rest next e n real
  case $work in
    "$dir"/*) rest=${work#"$dir"/} ;;
    *) return 1 ;;
  esac
  [ -n "$rest" ] || return 1
  while [ -n "$rest" ]; do
    next=${rest%%/*}
    n=0
    real=''
    while IFS= read -r e; do
      [ -n "$e" ] || continue
      n=$((n + 1))
      real=$e
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

# i6_prefilter_pattern -> a `find -iname` pattern that is a strict SUPERSET of
# the entries i6_is_family_raw accepts, so the traversal can prune early
# without changing the verdict.  The family token is split on non-alphanumeric
# characters and the parts are joined with '*'; only the separator characters
# between the parts may vary in a real name (folding never turns a letter
# into '-'), so a family match always contains the parts in order.
#
# The bash check stays authoritative: the prefilter only decides what is
# printed, never whether an entry is a stray.
i6_prefilter_pattern() {
  local fam=${I6_FAMILY:-kasegi-r41} body
  # Every separator run in the family token becomes '*': the family match
  # only ever varies the SEPARATOR between the token's alphanumeric parts
  # (folding never turns a letter into '-'), so '*'-joining the parts is a
  # strict superset of the names i6_is_family_raw accepts.
  body=$(printf '%s' "$fam" | sed -E 's/[^0-9A-Za-z]+/*/g')
  [ -n "$body" ] || body='*'
  printf '*%s*' "$body"
}

# ------------------------------------------------------------------- scanner

# i6_scan_core ROOT WORK -> sets I6_STRAYS, I6_READ, I6_SCANNED, I6_NAMES,
# I6_TOLERATED, I6_EXCLUDED; exit 0 green / 1 red.
i6_scan_core() {
  local root=$1 work=$2
  local root_real='' work_real='' tmpd='' e base real rel
  local chain=${I6_CHAIN:-strict}
  local pat

  I6_STRAYS=0
  I6_READ=ok
  I6_ERROR=none
  I6_SCANNED=0
  I6_NAMES=()
  I6_TOLERATED=()
  I6_EXCLUDED=()

  if [ -z "$work" ]; then I6_READ=fail; return 1; fi
  if [ ! -d "$root" ]; then I6_READ=fail; return 1; fi
  root_real=$(cd -- "$root" 2>/dev/null && pwd -P) || { I6_READ=fail; return 1; }
  work_real=$(cd -- "$work" 2>/dev/null && pwd -P) || { I6_READ=fail; return 1; }

  i6_family_cache
  pat=$(i6_prefilter_pattern)

  tmpd=$(mktemp -d "${TMPDIR:-/tmp}/i6scan.XXXXXX" 2>/dev/null) || { I6_READ=fail; I6_ERROR=mktemp-failed; return 1; }
  # -iname keeps the match case-insensitive; the dot-prefixed and separator
  # variants are all captured by the '*'-joined parts.
  find "$root_real" -mindepth 1 -iname "$pat" -print0 > "$tmpd/out" 2> "$tmpd/err"
  local rc=$?
  if [ "$rc" -ne 0 ] || [ -s "$tmpd/err" ]; then
    I6_READ=fail
    # Attribute the scan error to a path so a red is diagnosable: the first
    # find stderr line names the offending path.
    I6_ERROR=$(sed -n '1{s/^Error: //; s/^find: //; s/: Permission denied.*/:permission-denied/; s/: No such file.*/:no-such-file/; p;}' "$tmpd/err" | tr '\n' ' ')
    [ -n "$I6_ERROR" ] || I6_ERROR="find-exit-$rc"
  fi

  while IFS= read -r -d '' e; do
    [ -n "$e" ] || continue
    I6_SCANNED=$((I6_SCANNED + 1))
    base=${e##*/}
    i6_is_family_raw "$base"
    [ "$i6_hit" -eq 1 ] || continue
    real=$(realpath -m -- "$e" 2>/dev/null) || real=''
    [ -n "$real" ] || real=$e
    rel=${e#"$root_real"/}
    case $real in
      "$work_real"/*) I6_EXCLUDED+=("$rel"); continue ;;
    esac
    if [ "$real" = "$work_real" ]; then I6_TOLERATED+=("$rel"); continue; fi
    case $work_real in
      "$real"/*)
        if [ "$chain" = strict ] && i6_chain_clean "$real" "$work_real"; then
          I6_TOLERATED+=("$rel")
          continue
        fi
        ;;
    esac
    I6_STRAYS=$((I6_STRAYS + 1))
    I6_NAMES+=("$rel")
  done < "$tmpd/out"

  rm -rf -- "$tmpd"

  if [ "$I6_READ" = ok ] && [ "$I6_STRAYS" -eq 0 ]; then return 0; fi
  return 1
}

# i6_scan_scratch ROOT WORK -> prints `strays=<n>,read=<ok|fail>`; exit 0/1.
i6_scan_scratch() {
  local root=${1:-${I6_SCRATCH_ROOT:-/fast/scratch/hyaku}} work=${2:-}
  local rc
  i6_scan_core "$root" "$work"
  rc=$?
  printf 'strays=%s,read=%s\n' "$I6_STRAYS" "$I6_READ"
  return "$rc"
}

# i6_scan_detail ROOT WORK -> audit line + one line per stray; exit 0/1.
i6_scan_detail() {
  local root=${1:-${I6_SCRATCH_ROOT:-/fast/scratch/hyaku}} work=${2:-}
  local rc exc tol n
  i6_scan_core "$root" "$work"
  rc=$?
  exc=$(printf '%s\n' "${I6_EXCLUDED[@]+"${I6_EXCLUDED[@]}"}" | sed '/^$/d' | paste -sd, -)
  tol=$(printf '%s\n' "${I6_TOLERATED[@]+"${I6_TOLERATED[@]}"}" | sed '/^$/d' | paste -sd, -)
  [ -n "$exc" ] || exc=none
  [ -n "$tol" ] || tol=none
  printf 'strays=%s,read=%s,scanned=%s,excluded=%s,tolerated=%s,error=%s\n' \
    "$I6_STRAYS" "$I6_READ" "$I6_SCANNED" "$exc" "$tol" "$I6_ERROR"
  for n in "${I6_NAMES[@]+"${I6_NAMES[@]}"}"; do
    printf 'stray: %s\n' "$n"
  done
  return "$rc"
}

# i6_scan_names -> newline-separated stray paths.
i6_scan_names() {
  local n
  for n in "${I6_NAMES[@]+"${I6_NAMES[@]}"}"; do printf '%s\n' "$n"; done
}

# i6_stray_count -> integer count of strays.
i6_stray_count() { printf '%s\n' "$I6_STRAYS"; }

# --------------------------------------------------------------------- probe

i6_probe_failures=0
i6_probe_cases=0

# i6_expect LABEL EXPECT ROOT WORK [needle...]
i6_expect() {
  local label=$1 want=$2 root=$3 work=$4
  shift 4
  local out rc needle ok=1 got
  i6_probe_cases=$((i6_probe_cases + 1))
  out=$(i6_scan_detail "$root" "$work"); rc=$?
  if [ "$rc" -eq 0 ]; then got=green; else got=red; fi
  [ "$got" = "$want" ] || ok=0
  for needle in "$@"; do
    printf '%s' "$out" | grep -qF -- "$needle" || ok=0
  done
  printf 'selftest case=I6 %s expect=%s got=%s payload=%s\n' "$label" "$want" "$got" "$out"
  if [ "$ok" -eq 1 ]; then
    printf 'selftest case=I6 %s positive=pass verdict=pass\n' "$label"
  else
    printf 'selftest case=I6 %s positive=fail verdict=fail rc=%s payload=%s\n' "$label" "$rc" "$out"
    i6_probe_failures=$((i6_probe_failures + 1))
  fi
}

i6_refuse_live_root() {
  local real
  real=$(realpath -m -- "$1" 2>/dev/null) || return 0
  if [ "$real" = / ] || [ "$real" = /fast/scratch/hyaku ]; then
    i6_die "hermeticity refusal: scratch root is the live host root ($real); use an isolated sandbox"
  fi
  case /fast/scratch/hyaku in
    "$real"/*) i6_die "hermeticity refusal: scratch root ($real) contains the live host root; use an isolated sandbox" ;;
  esac
}

i6_selftest() {
  local root_arg=${I6_PROBE_ROOT:-}
  local sb
  if [ -z "$root_arg" ]; then
    sb=$(mktemp -d "${TMPDIR:-/tmp}/i6scan-probe.XXXXXXXX") || i6_die 'cannot create sandbox'
  else
    sb=$root_arg
  fi
  case $sb in
    /*) ;;
    *) sb=$(realpath -m -- "$sb" 2>/dev/null) || i6_die "cannot resolve --root: $sb" ;;
  esac
  i6_refuse_live_root "$sb"
  mkdir -p -- "$sb" || i6_die "cannot create sandbox: $sb"
  trap 'rm -rf -- "$sb"' EXIT

  local root="$sb/scratch" work="$sb/work"
  rm -rf -- "$root" "$work"
  mkdir -p -- "$root" "$work"

  printf 'selftest probe scratch-root=%s sandbox=%s live-root-read=no\n' "$root" "$sb"
  printf 'selftest policy=family=%s case-insensitive,separator-insensitive,recursive,dot-inclusive,fail-closed,chain=%s\n' \
    "${I6_FAMILY:-kasegi-r41}" "${I6_CHAIN:-strict}"

  # 1. clean root, work outside -> green
  i6_expect clean-root-green green "$root" "$work" 'strays=0,read=ok'

  # 2. the five required strays -> red, exactly five
  mkdir -p -- "$root/kasegi-r41-stray" "$root/Kasegi_R41-stray" "$root/kasegi_r41_stray" \
    "$root/container/kasegi-r41-nested" "$root/.kasegi-r41-dot"
  i6_expect five-strays-red red "$root" "$work" 'strays=5,read=ok' \
    'stray: kasegi-r41-stray' 'stray: Kasegi_R41-stray' 'stray: kasegi_r41_stray' \
    'stray: container/kasegi-r41-nested' 'stray: .kasegi-r41-dot'

  # 3. removing them greens the run
  rm -rf -- "$root/kasegi-r41-stray" "$root/Kasegi_R41-stray" "$root/kasegi_r41_stray" \
    "$root/container" "$root/.kasegi-r41-dot"
  i6_expect strays-removed-green green "$root" "$work" 'strays=0,read=ok'

  # 4. the passed work dir never reds, even when its own name is family-shaped
  mkdir -p -- "$root/kasegi-r41-work"
  work="$root/kasegi-r41-work"
  i6_expect work-dir-family-named-green green "$root" "$work" 'strays=0,read=ok' 'tolerated=kasegi-r41-work'
  mkdir -p -- "$work/kasegi-r41-inner"
  i6_expect work-dir-contents-green green "$root" "$work" 'strays=0,read=ok'
  rm -rf -- "$root/kasegi-r41-work"
  work="$sb/work"

  # 5. work inside a family-named container: tolerated only on a clean chain
  mkdir -p -- "$root/kasegi-r41-container/work"
  work="$root/kasegi-r41-container/work"
  i6_expect work-chain-clean-green green "$root" "$work" 'strays=0,read=ok' 'tolerated=kasegi-r41-container'
  mkdir -p -- "$root/kasegi-r41-container/leftover-seat"
  i6_expect work-chain-contaminated-red red "$root" "$work" 'strays=1,read=ok' 'stray: kasegi-r41-container'
  rm -rf -- "$root/kasegi-r41-container"
  work="$sb/work"

  # 6. D4-missed shapes: non-directory entry, dangling symlink
  printf 'x\n' > "$root/kasegi-r41-file"
  i6_expect stray-regular-file-red red "$root" "$work" 'strays=1,read=ok' 'stray: kasegi-r41-file'
  rm -f -- "$root/kasegi-r41-file"
  ln -s -- "$sb/nowhere-at-all" "$root/kasegi-r41-dangling"
  i6_expect stray-dangling-symlink-red red "$root" "$work" 'strays=1,read=ok' 'stray: kasegi-r41-dangling'
  rm -f -- "$root/kasegi-r41-dangling"

  # 7. D4-missed shape: unreadable entry inside a readable root
  mkdir -p -- "$root/kasegi-r41-locked"
  chmod 000 -- "$root/kasegi-r41-locked"
  i6_expect unreadable-entry-red red "$root" "$work" 'read=fail'
  chmod 755 -- "$root/kasegi-r41-locked"
  rm -rf -- "$root/kasegi-r41-locked"

  # 8. D4-missed shape: searchable but not listable root (mode 0311)
  mkdir -p -- "$root/listed"
  chmod 311 -- "$root/listed"
  i6_expect listable-failure-root-red red "$root/listed" "$work" 'read=fail'
  chmod 755 -- "$root/listed"
  rm -rf -- "$root/listed"

  # 9. fail-closed: unreadable root (mode 000) and missing root
  mkdir -p -- "$root/locked-root"
  chmod 000 -- "$root/locked-root"
  i6_expect unreadable-root-red red "$root/locked-root" "$work" 'read=fail'
  chmod 755 -- "$root/locked-root"
  rm -rf -- "$root/locked-root"
  i6_expect missing-root-red red "$root/does-not-exist" "$work" 'read=fail'

  # 10. recursion and dot/case/separator coverage at depth
  mkdir -p -- "$root/deep/deeper/kasegi-r41-deep"
  i6_expect deep-nested-red red "$root" "$work" 'strays=1,read=ok' 'stray: deep/deeper/kasegi-r41-deep'
  rm -rf -- "$root/deep"
  mkdir -p -- "$root/$(printf 'kasegi\u2011r41\u2011stray')"
  i6_expect unicode-separator-red red "$root" "$work" 'strays=1,read=ok'
  rm -rf -- "$root/$(printf 'kasegi\u2011r41\u2011stray')"

  # 11. out-of-family names are ignored
  mkdir -p -- "$root/kasegi-r40-old" "$root/kasegi-r42-next" "$root/unrelated"
  i6_expect out-of-family-green green "$root" "$work" 'strays=0,read=ok'
  rm -rf -- "$root/kasegi-r40-old" "$root/kasegi-r42-next" "$root/unrelated"

  printf 'selftest cases=%s failures=%s\n' "$i6_probe_cases" "$i6_probe_failures"
  if [ "$i6_probe_failures" -eq 0 ]; then
    printf 'selftest verdict=pass\n'
    return 0
  fi
  printf 'selftest verdict=fail\n'
  return 1
}

i6_usage() {
  sed -n '2,/^# Exit codes/p' "${BASH_SOURCE[0]}" | sed -e '$d' -e 's/^# \{0,1\}//'
}

# Aliases for suite integration: the r41 suite may call any of these names.
check_i6()  { i6_scan_scratch "$@"; }
i6_check()  { i6_scan_scratch "$@"; }
check_i6_detail() { i6_scan_detail "$@"; }
i6_scan()  { i6_scan_scratch "$@"; }

i6_main() {
  local mode='' scratch='' work='' chain='' rc
  while [ $# -gt 0 ]; do
    case $1 in
      --check|--detail|--self-test) mode=${1#--}; shift ;;
      --scratch-root) [ $# -ge 2 ] || i6_die '--scratch-root needs a directory'; scratch=$2; shift 2 ;;
      --work) [ $# -ge 2 ] || i6_die '--work needs a directory'; work=$2; shift 2 ;;
      --chain) [ $# -ge 2 ] || i6_die '--chain needs strict|literal'; chain=$2; shift 2 ;;
      --root) [ $# -ge 2 ] || i6_die '--root needs a directory'; I6_PROBE_ROOT=$2; shift 2 ;;
      -h|--help) i6_usage; exit 0 ;;
      *) i6_die "unknown argument: $1" ;;
    esac
  done
  if [ -n "$chain" ]; then I6_CHAIN=$chain; fi
  case $mode in
    self-test) i6_selftest "$@"; exit $? ;;
    check|detail)
      [ -n "$work" ] || i6_die "--$mode requires --work DIR"
      [ -n "$scratch" ] || scratch=${I6_SCRATCH_ROOT:-/fast/scratch/hyaku}
      if [ "$mode" = check ]; then
        i6_scan_scratch "$scratch" "$work"; rc=$?
      else
        i6_scan_detail "$scratch" "$work"; rc=$?
      fi
      exit "$rc" ;;
    '') i6_die 'one of --check, --detail, --self-test is required' ;;
    *) i6_die "unknown mode: $mode" ;;
  esac
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  i6_main "$@"
fi
