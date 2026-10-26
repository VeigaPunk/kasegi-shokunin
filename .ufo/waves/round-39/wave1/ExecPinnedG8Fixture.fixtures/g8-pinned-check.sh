#!/usr/bin/env bash
# g8-pinned-check.sh — executable model of the round-39 G8' limb over the
# ExecPinnedG8Fixture set.
#
# G8' as frozen (round-39 claims C1, check G8): the carry-over of the round-37
# closure suite is trusted only when BOTH hold —
#   1. the bytes of corpus/instruments/r37-closure.sh in the export hash equal to
#      the bytes `git show 2387dcf6ccfefcfb703783387b9aade8fc82abfa:...` returns
#      (pinned here as pinned/r37-closure.sh, sha256 in pinned/sha256.txt), and
#   2. the run of the PINNED bytes ends `closed=14/14 exit=0` with exit 0.
# The run is always of the pinned bytes, never of the export copy: an export copy
# that has been edited must not be able to supply its own verdict.
#
# For each case directory this script materialises the export copy the case
# names, hashes it, reads the case's recorded run, prints the `G8 payload=...`
# line the r39 suite must print for that state, and compares it byte-exactly
# with expected/expected.txt. It reads no lane, no git object and no network.
#
# Usage:
#   bash g8-pinned-check.sh [CASE...]
#       Default cases: positive negative-mutated negative-open negative-absent.
#       Prints one `case=<name> G8 payload=<...> closed=<0|1>` line and one
#       `case=<name> verdict=<PASS|FAIL>` line per case, then
#       `g8p cases=<n> failures=<k>`. Exit 0 only when every case matches.
#   bash g8-pinned-check.sh -h|--help
#
# Exit codes: 0 every case matched / help, 1 a case did not match, 2 harness
# error (pinned bytes absent, digest disagreement, unknown case or source).
set -uo pipefail

HERE=$( cd -- "$(dirname -- "$0")" && pwd -P ) || { printf 'g8p: cannot resolve fixture root\n' >&2; exit 2; }
PINNED=$HERE/pinned/r37-closure.sh
PINNED_SHA_FILE=$HERE/pinned/sha256.txt
EXPECTED=$HERE/expected/expected.txt
DEFAULT_CASES=(positive negative-mutated negative-open negative-absent)

usage() { sed -n '2,27p' "${BASH_SOURCE[0]}" | sed -e 's/^# \{0,1\}//'; }

case ${1:-} in
  -h|--help) usage; exit 0 ;;
esac

[ -f "$PINNED" ] || { printf 'g8p: missing pinned bytes: %s\n' "$PINNED" >&2; exit 2; }
[ -f "$PINNED_SHA_FILE" ] || { printf 'g8p: missing pinned digest file: %s\n' "$PINNED_SHA_FILE" >&2; exit 2; }
[ -f "$EXPECTED" ] || { printf 'g8p: missing expected lines: %s\n' "$EXPECTED" >&2; exit 2; }

PINNED_SHA=$(sha256sum -- "$PINNED" | awk '{print $1; exit}')
RECORDED_SHA=$(awk 'NR == 1 {print $1; exit}' "$PINNED_SHA_FILE")
if [ -z "$PINNED_SHA" ] || [ "$PINNED_SHA" != "$RECORDED_SHA" ]; then
  printf 'g8p: pinned digest disagreement computed=%s recorded=%s\n' "$PINNED_SHA" "$RECORDED_SHA" >&2
  exit 2
fi

if [ "$#" -gt 0 ]; then CASES=("$@"); else CASES=("${DEFAULT_CASES[@]}"); fi

WORK=$(mktemp -d "${TMPDIR:-/tmp}/g8p.XXXXXX") || { printf 'g8p: cannot create work dir\n' >&2; exit 2; }
trap 'rm -rf -- "$WORK"' EXIT

expected_line() { # CASE
  sed -n "s/^$1 -> //p" "$EXPECTED" | head -n 1
}

check_case() { # CASE -> one `G8 payload=... closed=...` line, exit 0/1/2
  local case=$1 dir=$HERE/$1
  (
    set -uo pipefail
    local name='' source='' copy='' run='' run_exit='' run_source='' mutation='' note=''
    [ -f "$dir/case.env" ] || { printf 'g8p: missing case descriptor: %s/case.env\n' "$dir" >&2; exit 2; }
    # shellcheck disable=SC1090
    . "$dir/case.env"
    local exp=$WORK/export-$case/corpus/instruments/r37-closure.sh
    local esha='-' suite=0 last='' rclosed=0 dg=0
    case $source in
      pinned)
        mkdir -p -- "$(dirname -- "$exp")" || exit 2
        cp -- "$PINNED" "$exp" || exit 2
        ;;
      copy)
        [ -n "$copy" ] || { printf 'g8p: case=%s source=copy without copy=\n' "$case" >&2; exit 2; }
        mkdir -p -- "$(dirname -- "$exp")" || exit 2
        cp -- "$dir/$copy" "$exp" || exit 2
        ;;
      absent) ;;
      *) printf 'g8p: case=%s unknown source=%s\n' "$case" "$source" >&2; exit 2 ;;
    esac
    if [ -f "$exp" ]; then
      suite=1
      esha=$(sha256sum -- "$exp" | awk '{print $1; exit}')
      [ "$esha" = "$PINNED_SHA" ] && dg=1
    fi
    if [ -n "$run" ] && [ -f "$dir/$run" ]; then
      last=$(grep -v '^$' "$dir/$run" | tail -n 1)
      [ "$last" = 'closed=14/14 exit=0' ] && rclosed=1
    fi
    local payload closed=0
    payload="pinned-sha256=$PINNED_SHA,export-sha256=$esha,digest-match=$dg,r37-suite=$suite,r37-closed=$rclosed,r37-exit=$run_exit"
    [ "$dg" -eq 1 ] && [ "$suite" -eq 1 ] && [ "$rclosed" -eq 1 ] && [ "$run_exit" = 0 ] && closed=1
    printf 'G8 payload=%s closed=%s\n' "$payload" "$closed"
  )
}

fail=0
for case in "${CASES[@]}"; do
  got=$(check_case "$case" 2>"$WORK/err-$case"); rc=$?
  if [ "$rc" -ne 0 ]; then
    printf 'case=%s verdict=ERROR rc=%s\n' "$case" "$rc"
    sed -e 's/^/case='"$case"' error: /' "$WORK/err-$case"
    fail=1
    continue
  fi
  want=$(expected_line "$case")
  printf 'case=%s %s\n' "$case" "$got"
  if [ -z "$want" ]; then
    printf 'case=%s verdict=FAIL reason=no-expected-line\n' "$case"
    fail=1
  elif [ "$got" = "$want" ]; then
    printf 'case=%s verdict=PASS\n' "$case"
  else
    printf 'case=%s verdict=FAIL want=%s\n' "$case" "$want"
    fail=1
  fi
done

if [ "$fail" -eq 0 ]; then
  printf 'g8p cases=%s failures=0\n' "${#CASES[@]}"
  exit 0
fi
printf 'g8p cases=%s failures=1\n' "${#CASES[@]}"
exit 1
