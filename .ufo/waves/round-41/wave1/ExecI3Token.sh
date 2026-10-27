#!/usr/bin/env bash
# r41 I3 limb — token-boundary value matching over line-anchored correction lines.
#
# Contract (frozen claim C1, check I3 — "token-boundary value matching: the
# round-40 substring defeat fixtures `closed=7/80` and `failures=10` are
# rejected by the value limb"):
#
#   i3_token_match FILE ROUND VALUE...
#       Read FILE. Consider ONLY the lines whose text begins, in column 1,
#       with `Correction (round ROUND)` — line-anchored; the closing
#       parenthesis is part of the anchor, so `Correction (round 410)` is
#       NOT a `Correction (round 41)` line, and an indented copy is not
#       anchored either.
#       A VALUE is MATCHED only when it occurs in one of those lines as a
#       token: the character immediately before the occurrence and the
#       character immediately after it must each be whitespace, or
#       punctuation, or the edge of the line. Letters and digits are word
#       characters, so `closed=7/80` does NOT satisfy the value
#       `closed=7/8` and `failures=10` does NOT satisfy the value
#       `failures=1`; `closed=7/8` and `failures=1` DO satisfy. This is the
#       `[[:space:][:punct:]]`-bounded form of the match; it is used instead
#       of bare whitespace field equality because the records quote their
#       values in backticks (`` `closed=7/8` ``), which a bare field
#       comparison would not accept.
#       By default a value may be found on any considered line; use
#       i3_token_match_same_line to require ONE considered line to carry
#       every value.
#
#   Environment:
#       I3_STRICT_UNDERSCORE=1
#           Treat `_` as a word character rather than punctuation, so
#           `x_closed=7/8` does not satisfy the value `closed=7/8`. The
#           default follows POSIX [[:punct:]], which includes `_`.
#
#   i3_correction_lines FILE ROUND
#       Print the considered lines (the input of the value limb), so a
#       neighbouring limb can compose with it.
#
# The value list is an argument, not a constant, so the I1 limb (correction
# lines naming the firing evidence) and the I3 limb (value matching) share
# one implementation.
#
# Exit codes: 0 — every value matched; 1 — at least one value missing;
# 2 — file absent or unreadable (fail closed); 64 — usage error.
#
# Sourceable: sourcing this file defines the functions and executes nothing.

_I3_SEP=$'\x1f'

# _i3_scan FILE ROUND MODE VALUES_CSV — the shared matcher core. MODE is
# `any` (a value may sit on any considered line) or `same-line` (one
# considered line must carry every value). Prints the payload line and
# returns 0 (green) / 1 (red).
_i3_scan() {
  local file=$1 round=$2 mode=$3 joined=$4
  local I3_VALS=$joined
  export I3_VALS
  awk -v round="$round" -v mode="$mode" '
    BEGIN {
      sep = "\037"
      nv = split(ENVIRON["I3_VALS"], V, sep)
      re = "^Correction \\(round " round "\\)"
      ws    = " \t\n\r\f\v"
      word  = "0123456789"
      # POSIX [[:punct:]] — every printable non-alphanumeric, non-space
      # character, `_` included.
      punct = "!\"#$%&\x27()*+,-./:;<=>?@[\\]^_`{|}~"
      # Under I3_STRICT_UNDERSCORE=1, `_` is a word character (it joins
      # words), so `x_closed=7/8` does not satisfy the value `closed=7/8`.
      if (ENVIRON["I3_STRICT_UNDERSCORE"] == "1") {
        gsub(/_/, "", punct)
      }
      corrections = 0; named = 0
    }
    function isb(c) {
      if (c == "") return 1
      if (index(word, c) > 0) return 0
      if (c ~ /[A-Za-z]/) return 0
      if (index(ws, c) > 0) return 1
      if (index(punct, c) > 0) return 1
      return 0
    }
    # hasval(s, v) — 1 when v occurs in s as a token.
    function hasval(s, v,   st, rel, abs, L, left, right) {
      L = length(v); st = 1
      while (1) {
        rel = index(substr(s, st), v)
        if (rel == 0) return 0
        abs = st + rel - 1
        left  = (abs > 1)              ? substr(s, abs - 1, 1) : ""
        right = (abs + L <= length(s)) ? substr(s, abs + L, 1) : ""
        if (isb(left) && isb(right)) return 1
        st = abs + 1
      }
    }
    $0 ~ re {
      corrections++
      hit = 0
      for (j = 1; j <= nv; j++) {
        if (hasval($0, V[j])) { found[j] = 1; hit++ }
      }
      if (hit == nv) named++
    }
    END {
      matched = 0; miss = ""
      for (j = 1; j <= nv; j++) {
        if (found[j]) matched++
        else miss = (miss == "") ? V[j] : miss "," V[j]
      }
      if (miss == "") miss = "-"
      printf "corrections=%d,named=%d,missing=%d,missing-values=%s,values=%d,mode=%s\n",
             corrections, named, nv - matched, miss, nv, mode
      if (mode == "same-line") exit (named >= 1) ? 0 : 1
      exit (matched == nv) ? 0 : 1
    }
  ' "$file"
  local rc=$?
  unset I3_VALS
  return $rc
}

# _i3_join VALUES... — join the values with the separator used to hand them
# to awk (values containing the separator are rejected by the callers).
_i3_join() {
  local joined='' first=1 v
  for v in "$@"; do
    if [ "$first" -eq 1 ]; then joined=$v; first=0; else joined="${joined}${_I3_SEP}${v}"; fi
  done
  printf '%s' "$joined"
}

# i3_correction_lines FILE ROUND — print the line-anchored correction lines.
i3_correction_lines() {
  [ $# -eq 2 ] || return 64
  local file=$1 round=$2
  [ -f "$file" ] && [ -r "$file" ] || return 2
  case "$round" in
    ''|*[!0-9]*) return 64 ;;
  esac
  awk -v round="$round" '
    BEGIN { re = "^Correction \\(round " round "\\)" }
    $0 ~ re { print }
  ' "$file"
}

# i3_token_match FILE ROUND VALUE... — token-boundary value matching.
# A value may be found on any considered line.
i3_token_match() {
  if [ $# -lt 3 ]; then
    printf 'corrections=0,named=0,missing=0,missing-values=-,values=0,mode=any,error=usage\n'
    return 64
  fi
  local file=$1 round=$2
  shift 2
  local -a values=()
  local v
  for v in "$@"; do
    case "$v" in
      *"$_I3_SEP"*)
        printf 'corrections=0,named=0,missing=0,missing-values=-,values=0,mode=any,error=bad-value\n'
        return 64 ;;
      '') ;;
      *) values+=("$v") ;;
    esac
  done
  if [ ${#values[@]} -eq 0 ]; then
    printf 'corrections=0,named=0,missing=0,missing-values=-,values=0,mode=any,error=no-values\n'
    return 64
  fi
  if [ ! -f "$file" ] || [ ! -r "$file" ]; then
    printf 'corrections=0,named=0,missing=%d,missing-values=-,values=%d,mode=any,error=file-absent\n' \
      "${#values[@]}" "${#values[@]}"
    return 2
  fi
  case "$round" in
    ''|*[!0-9]*)
      printf 'corrections=0,named=0,missing=%d,missing-values=-,values=%d,mode=any,error=bad-round\n' \
        "${#values[@]}" "${#values[@]}"
      return 64 ;;
  esac
  _i3_scan "$file" "$round" any "$(_i3_join "${values[@]}")"
}

# i3_token_match_same_line FILE ROUND VALUE... — require ONE considered line
# to carry every value (a stricter reading of "names the values").
i3_token_match_same_line() {
  if [ $# -lt 3 ]; then
    printf 'corrections=0,named=0,missing=0,missing-values=-,values=0,mode=same-line,error=usage\n'
    return 64
  fi
  local file=$1 round=$2
  shift 2
  local -a values=()
  local v
  for v in "$@"; do
    case "$v" in
      *"$_I3_SEP"*)
        printf 'corrections=0,named=0,missing=0,missing-values=-,values=0,mode=same-line,error=bad-value\n'
        return 64 ;;
      '') ;;
      *) values+=("$v") ;;
    esac
  done
  if [ ${#values[@]} -eq 0 ]; then
    printf 'corrections=0,named=0,missing=0,missing-values=-,values=0,mode=same-line,error=no-values\n'
    return 64
  fi
  if [ ! -f "$file" ] || [ ! -r "$file" ]; then
    printf 'corrections=0,named=0,missing=%d,missing-values=-,values=%d,mode=same-line,error=file-absent\n' \
      "${#values[@]}" "${#values[@]}"
    return 2
  fi
  case "$round" in
    ''|*[!0-9]*)
      printf 'corrections=0,named=0,missing=%d,missing-values=-,values=%d,mode=same-line,error=bad-round\n' \
        "${#values[@]}" "${#values[@]}"
      return 64 ;;
  esac
  _i3_scan "$file" "$round" same-line "$(_i3_join "${values[@]}")"
}

# ---------------------------------------------------------------------------
# CLI (only when executed, never when sourced).
# ---------------------------------------------------------------------------
_i3_usage() {
  cat <<'USAGE'
usage: ExecI3Token.sh --file FILE --round N --value V [--value V ...] [--same-line]
       ExecI3Token.sh --selftest
USAGE
}

_i3_selftest() {
  local t rc
  t=$(mktemp -d "${TMPDIR:-/tmp}/i3-selftest.XXXXXX") || return 2
  cat > "$t/honest.md" <<'EOF'
Correction (round 40): the final round-39 receipt records `closed=7/8 exit=1` and `selftest failures=1`.
EOF
  cat > "$t/defeat.md" <<'EOF'
Correction (round 40): the final round-39 receipt records `closed=7/80 and failures=10`.
EOF
  cat > "$t/mixed.md" <<'EOF'
Correction (round 40): the final round-39 receipt records `closed=7/80 and failures=10`.
Correction (round 40): the graded selftest records `closed=7/8 exit=1` and `selftest failures=1`.
EOF
  cat > "$t/unanchored.md" <<'EOF'
The final round-39 receipt records `closed=7/8 exit=1` and `selftest failures=1`.
EOF
  cat > "$t/split.md" <<'EOF'
Correction (round 40): the final round-39 receipt records `closed=7/8 exit=1`.
Correction (round 40): the graded selftest records `selftest failures=1`.
EOF
  i3_token_match "$t/honest.md" 40 'closed=7/8' 'failures=1'; rc=$?
  printf 'selftest case=honest values=2 matched=2 verdict=%s\n' "$( [ "$rc" -eq 0 ] && echo pass || echo fail )"
  i3_token_match "$t/defeat.md" 40 'closed=7/8' 'failures=1'; rc=$?
  printf 'selftest case=defeat values=2 matched=0 verdict=%s\n' "$( [ "$rc" -eq 1 ] && echo pass || echo fail )"
  i3_token_match "$t/unanchored.md" 40 'closed=7/8' 'failures=1'; rc=$?
  printf 'selftest case=unanchored values=2 matched=0 verdict=%s\n' "$( [ "$rc" -eq 1 ] && echo pass || echo fail )"
  i3_token_match "$t/mixed.md" 40 'closed=7/8' 'failures=1'; rc=$?
  printf 'selftest case=mixed values=2 matched=2 verdict=%s\n' "$( [ "$rc" -eq 0 ] && echo pass || echo fail )"
  i3_token_match "$t/split.md" 40 'closed=7/8' 'failures=1'; rc=$?
  printf 'selftest case=split-any values=2 matched=2 verdict=%s\n' "$( [ "$rc" -eq 0 ] && echo pass || echo fail )"
  i3_token_match_same_line "$t/split.md" 40 'closed=7/8' 'failures=1'; rc=$?
  printf 'selftest case=split-same-line values=2 matched=0 verdict=%s\n' "$( [ "$rc" -eq 1 ] && echo pass || echo fail )"
  rm -rf -- "$t"
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  _i3_file=''; _i3_round=''; _i3_same=0; _i3_values=()
  while [ $# -gt 0 ]; do
    case "$1" in
      --file) _i3_file=$2; shift 2 ;;
      --round) _i3_round=$2; shift 2 ;;
      --value) _i3_values+=("$2"); shift 2 ;;
      --same-line) _i3_same=1; shift ;;
      --selftest) _i3_selftest; exit $? ;;
      -h|--help) _i3_usage; exit 0 ;;
      *)
        printf 'corrections=0,named=0,missing=0,missing-values=-,values=0,mode=any,error=usage\n'
        _i3_usage >&2; exit 64 ;;
    esac
  done
  if [ -z "$_i3_file" ] || [ -z "$_i3_round" ] || [ ${#_i3_values[@]} -eq 0 ]; then
    printf 'corrections=0,named=0,missing=0,missing-values=-,values=0,mode=any,error=usage\n'
    _i3_usage >&2
    exit 64
  fi
  if [ "$_i3_same" -eq 1 ]; then
    i3_token_match_same_line "$_i3_file" "$_i3_round" "${_i3_values[@]}"
  else
    i3_token_match "$_i3_file" "$_i3_round" "${_i3_values[@]}"
  fi
  exit $?
fi
