#!/usr/bin/env bash
# ExecI5Blocks.sh — I5 declared-blocks validator limb (kasegi round-41, check I5).
#
# WHAT
#   Grade a `declared-blocks.txt` (one declaration per line,
#   `<path> <lines> <sha256>`) against an EXPORT ROOT (a `git archive <ref>`
#   extraction) and a BASE..REF commit range in a lane repo. A declaration
#   asserts that the file at <path> ends with exactly <lines> appended lines
#   whose bytes hash to <sha256>, and that the range added exactly those lines
#   and deleted nothing.
#
#   Four clauses, all required for a declaration to be valid:
#
#     (a) PATH SHAPE — <path> carries no NUL byte, no absolute prefix and no
#         `..` anywhere (a `..` component escapes the export; a `..` substring
#         is rejected outright so no encoding of the escape survives).
#     (b) CONTAINMENT — the resolved path is readlink-canonicalized and MUST
#         remain under the canonical export root. This is the clause the
#         round-40 wave-2 attack T7 defeated: round-40's H9 graded a declared
#         SYMLINK whose target lived outside the export, so the bytes the
#         declaration certified were bytes outside the tree under test
#         (`.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt`, T7).
#     (c) TAIL DIGEST — `tail -n <lines>` of the export file hashes to
#         <sha256>, and the file really has at least <lines> lines.
#     (d) DIFF SHAPE — `git diff --numstat <base> <ref> -- <path>` reports
#         exactly one record whose added count equals <lines> and whose
#         deleted count is 0.
#
#   Clauses are evaluated in that order and the FIRST failing clause is the
#   reported reason, so a defeat fixture reds on the clause it exercises.
#
#   Three guards beyond the four clauses, each harmless to an honest
#   declaration and each closing a way a declaration could be green without
#   saying what it claims:
#     (b2) the declared path must be a regular file, not a symlink: git counts
#          a symlink as a one-line blob (its target text), so a symlink can
#          never be an appended text block;
#     (c2) the export file must really carry at least <lines> lines, else
#          `tail -n <lines>` silently clips and the digest means something
#          other than the declared tail;
#     (e)  a declaration line that does not parse is a declared-but-invalid
#          declaration, never a silently dropped one: a gate must not be green
#          with a declaration it could not read.
#
# CONTRACT
#   i5_declared_blocks_check EXPORT_ROOT LANE BASE_REF REF DECLARED_FILE
#       Grades DECLARED_FILE (absolute, or relative to EXPORT_ROOT). Prints
#       one detail line per declaration and a final summary line:
#
#         I5 payload=declared=N,valid=N,tail=N,malformed=N,pure=1|0,paths=1|0,canon=1|0,nul=0|1,diff-read=ok|fail closed=0|1
#
#       Detail lines go to stderr by default (I5_DETAIL=1 sends them to
#       stdout); the summary line is always the last stdout line.
#       Exit 0 only when every declaration is valid (closed=1); exit 1 when a
#       defect is present (closed=0); exit 2 on a harness error (unreadable
#       export, unreadable lane, unresolvable refs, unreadable declared file).
#
#   i5_legacy_h9_check EXPORT_ROOT LANE BASE_REF REF DECLARED_FILE
#       The round-40 H9 rule set (path shape + tail + numstat, NO containment
#       clause), kept only so the selftest can show the T7 escape was GREEN
#       under the old rules and is RED under the I5 rules. It is a control,
#       not a validator.
#
#   The file is sourceable: sourcing it defines the functions and changes
#   nothing else. Running it executes the CLI.
#
# CLI
#   bash ExecI5Blocks.sh --check --export-root DIR --lane DIR --base REF
#        --ref REF --declared FILE [--detail]
#       Grade one declared file; prints the summary line; exit 0|1|2.
#   bash ExecI5Blocks.sh --selftest [--keep]
#       Build a throwaway git fixture under $TMPDIR, export it, and grade one
#       honest declaration (must be GREEN) and thirteen defeat fixtures (each
#       must RED for its named clause), plus the legacy-control contrast.
#       Prints `selftest case=I5 <label> verdict=pass|fail reason=<clause>`,
#       `selftest cases=14 failures=<k>` and exits 0 only for k=0.
#
# READ-ONLY: this limb never writes under the lane, the export or any tracked
# tree. Its only writes are scratch dirs under $TMPDIR, removed on exit.
#
# NOT part of this limb: the graded fixture set of the committed suite
# (corpus/instruments/r41-closure.sh) owns the I5 selftest cases; this file
# provides the check the suite calls.
set -uo pipefail

I5_LANE_DEFAULT=/home/vgpnk/Projects/shokunin/kasegi-shokunin

# i5_detail LINE — one declaration's verdict. stderr, or stdout with
# I5_DETAIL=1. The detail is data for the transcript; it is never parsed by
# the check itself.
i5_detail() {
  if [ "${I5_DETAIL:-0}" = 1 ]; then
    printf '%s\n' "$*"
  else
    printf '%s\n' "$*" >&2
  fi
}

# i5_nul_scan FILE — print the 1-based line numbers of FILE that carry a NUL
# byte, one per line; print `*` when the file carries a NUL byte that cannot
# be attributed to a single line (then every declaration is a NUL suspect).
# The per-line form is what makes the NUL clause usable: bash drops NUL bytes
# when reading a line, so `read -r` alone cannot see them.
i5_nul_scan() {
  local f=$1 a b
  [ -r "$f" ] || return 0
  if grep -a -q -P '\x00' -- "$f" 2>/dev/null; then
    LC_ALL=C grep -a -n -P '\x00' -- "$f" 2>/dev/null | cut -d: -f1
    return 0
  fi
  # No -P support (or no NUL found): fall back to a byte-count comparison so
  # a NUL byte can never pass unnoticed.
  a=$(wc -c < "$f" 2>/dev/null | tr -d ' ')
  b=$(tr -d '\000' < "$f" 2>/dev/null | wc -c | tr -d ' ')
  if [ "${a:-0}" != "${b:-0}" ]; then printf '*\n'; fi
  return 0
}

# i5_shape_ok PATH — clause (a): a relative path with no `..` at all.
i5_shape_ok() {
  local p=$1
  case $p in
    '') return 1 ;;
    /*) return 1 ;;
    *..*) return 1 ;;
  esac
  return 0
}

# i5_canon PATH — the readlink-canonicalized form of PATH. Falls back to
# realpath -m for a dangling final component.
i5_canon() {
  local p=$1 out
  if out=$(readlink -f -- "$p" 2>/dev/null) && [ -n "$out" ]; then
    printf '%s' "$out"
    return 0
  fi
  realpath -m -- "$p" 2>/dev/null || printf ''
}

# i5_under ROOT PATH — 0 when PATH is strictly under ROOT. Both arguments are
# expected canonical; the trailing-slash form keeps `/export` from matching
# `/export-evil`.
i5_under() {
  local root=$1 p=$2
  [ -n "$root" ] && [ -n "$p" ] || return 1
  case $root in /) ;; *) root=$root/ ;; esac
  case $p in
    "$root"*) return 0 ;;
  esac
  return 1
}

# i5_numstat LANE BASE REF PATH — `<added> <deleted>` for the path, or one of
# ERR (diff unreadable), ABSENT (path not in the range), MULTI (more than one
# record), BINARY (non-numeric counters).
i5_numstat() {
  local lane=$1 base=$2 ref=$3 path=$4 out n added deleted
  if ! out=$(git --no-optional-locks -C "$lane" diff --numstat "$base" "$ref" -- "$path" 2>/dev/null); then
    printf 'ERR'; return 0
  fi
  [ -n "$out" ] || { printf 'ABSENT'; return 0; }
  n=$(printf '%s\n' "$out" | wc -l | tr -d ' ')
  [ "$n" -eq 1 ] || { printf 'MULTI'; return 0; }
  added=$(printf '%s\n' "$out" | cut -f1)
  deleted=$(printf '%s\n' "$out" | cut -f2)
  case "$added$deleted" in
    *[!0-9]*) printf 'BINARY'; return 0 ;;
  esac
  printf '%s %s' "$added" "$deleted"
}

# i5_file_lines FILE — the number of lines the file carries (a final
# unterminated line counts).
i5_file_lines() {
  awk 'END { print NR + 0 }' "$1" 2>/dev/null || printf '0'
}

# i5_tail_sha FILE N — sha256 of `tail -n N FILE`.
i5_tail_sha() {
  tail -n "$2" -- "$1" 2>/dev/null | sha256sum | awk '{ print $1; exit }'
}

# i5_grade_one ROOT LANE BASE REF PATH LINES SHA NULSTATE
#   Grade one declaration. Prints nothing; sets I5_REASON (empty when the
#   declaration is valid) and returns 0 (valid) / 1 (invalid).
i5_grade_one() {
  local root=$1 lane=$2 base=$3 ref=$4 path=$5 lines=$6 sha=$7 nulstate=$8
  local f resolved n total got nm added deleted
  I5_REASON=
  I5_TAIL=0

  # (a) path shape
  if [ "$nulstate" != ok ]; then
    I5_REASON=nul-byte
    return 1
  fi
  if ! i5_shape_ok "$path"; then
    case $path in
      /*) I5_REASON=path-absolute ;;
      *..*) I5_REASON=path-escape ;;
      *) I5_REASON=path-shape ;;
    esac
    return 1
  fi

  f=$root/$path

  # (b) containment: the readlink-canonicalized resolved path must stay under
  # the canonical export root. This is the clause the round-40 wave-2 T7
  # attack defeated: a declared SYMLINK whose target lives outside the export
  # made the old rules certify bytes that were not in the tree under test.
  # The check runs BEFORE the existence and tail checks so that an escaping
  # symlink is reported as an escape and never read.
  resolved=$(i5_canon "$f")
  if [ -z "$resolved" ] || ! i5_under "$root" "$resolved"; then
    I5_REASON=escapes-root
    return 1
  fi
  if [ ! -e "$f" ]; then
    I5_REASON=absent
    return 1
  fi
  # (b2) the declared path must itself be a regular file, not a symlink. A
  # symlink inside the export is contained, but git counts a symlink as a
  # one-line blob (its target text), so a symlink can never be an appended
  # text block; allowing one would let a declaration certify the bytes of a
  # file the range never touched.
  if [ -L "$f" ]; then
    I5_REASON=symlink-declared
    return 1
  fi
  if [ ! -f "$resolved" ] || [ ! -r "$resolved" ]; then
    I5_REASON=not-a-file
    return 1
  fi

  # (c) tail digest, read from the canonical path
  total=$(i5_file_lines "$resolved")
  if [ "${total:-0}" -lt "$lines" ]; then
    I5_REASON=lines-exceed-file
    return 1
  fi
  got=$(i5_tail_sha "$resolved" "$lines")
  if [ "$got" != "$sha" ]; then
    I5_REASON=tail-mismatch
    return 1
  fi
  I5_TAIL=1

  # (d) diff shape
  nm=$(i5_numstat "$lane" "$base" "$ref" "$path")
  case $nm in
    ERR|ABSENT|MULTI|BINARY)
      I5_REASON=diff-$nm
      return 1
      ;;
  esac
  added=${nm%% *}
  deleted=${nm##* }
  if [ "$deleted" != 0 ]; then
    I5_REASON=diff-deleted
    return 1
  fi
  if [ "$added" != "$lines" ]; then
    I5_REASON=diff-mismatch
    return 1
  fi
  return 0
}

# i5_read_declarations FILE — normalize the declared file into
# "<lineno> <path> <lines> <sha>" records on stdout, one per NON-COMMENT
# line. A line that does not parse is emitted as "<lineno> MALFORMED" so the
# caller can count it as a declared-but-invalid declaration: a gate must never
# be green with a declaration it could not read.
i5_read_declarations() {
  local f=$1 lineno=0 line path lines sha extra
  while IFS= read -r line || [ -n "$line" ]; do
    lineno=$((lineno + 1))
    case $line in ''|'#'*) continue ;; esac
    path=; lines=; sha=; extra=
    set -f
    set -- $line
    set +f
    path=${1:-}; lines=${2:-}; sha=${3:-}; extra=${4:-}
    if [ -z "$path" ] || [ -z "$lines" ] || [ -z "$sha" ] || [ -n "$extra" ]; then
      printf '%s MALFORMED\n' "$lineno"; continue
    fi
    case $lines in ''|*[!0-9]*) printf '%s MALFORMED\n' "$lineno"; continue ;; esac
    [ "$lines" -ge 1 ] || { printf '%s MALFORMED\n' "$lineno"; continue; }
    case $sha in *[!0-9a-f]*) printf '%s MALFORMED\n' "$lineno"; continue ;; esac
    [ "${#sha}" -eq 64 ] || { printf '%s MALFORMED\n' "$lineno"; continue; }
    printf '%s %s %s %s\n' "$lineno" "$path" "$lines" "$sha"
  done < "$f"
}

# i5_collect_nul FILE — print "<lineno> nul" for every declaration line that
# carries a NUL byte (or for every declaration when the file carries an
# unattributable NUL).
i5_collect_nul() {
  local f=$1 scan lineno
  scan=$(i5_nul_scan "$f")
  [ -n "$scan" ] || return 0
  while IFS= read -r lineno; do
    [ -n "$lineno" ] || continue
    if [ "$lineno" = '*' ]; then
      i5_read_declarations "$f" | awk '{ print $1, "nul" }'
      return 0
    fi
    printf '%s nul\n' "$lineno"
  done <<EOF
$scan
EOF
}

# i5_declared_blocks_check EXPORT_ROOT LANE BASE_REF REF DECLARED_FILE
#   The I5 check. See the header for the payload contract.
i5_declared_blocks_check() {
  local root=$1 lane=$2 base=$3 ref=$4 declared=$5
  local rootreal declfile nulmap lineno path lines sha nulstate
  local declared_n=0 valid_n=0 tail_n=0
  local pure=1 paths=1 canon=1 nul=0 diffread=ok malformed=0
  local rec

  if [ ! -d "$root" ]; then
    printf 'I5 payload=declared=0,valid=0,tail=0,malformed=0,pure=1,paths=1,canon=1,nul=0,diff-read=err closed=0\n'
    i5_detail 'I5 detail=reason=export-unreadable'
    return 2
  fi
  if [ ! -d "$lane" ]; then
    printf 'I5 payload=declared=0,valid=0,tail=0,malformed=0,pure=1,paths=1,canon=1,nul=0,diff-read=err closed=0\n'
    i5_detail 'I5 detail=reason=lane-unreadable'
    return 2
  fi
  case $declared in
    /*) declfile=$declared ;;
    *) declfile=$root/$declared ;;
  esac
  if [ ! -r "$declfile" ]; then
    printf 'I5 payload=declared=0,valid=0,tail=0,malformed=0,pure=1,paths=1,canon=1,nul=0,diff-read=err closed=0\n'
    i5_detail 'I5 detail=reason=declared-unreadable'
    return 2
  fi
  if ! git --no-optional-locks -C "$lane" rev-parse --verify --quiet "$base^{commit}" >/dev/null 2>&1; then
    printf 'I5 payload=declared=0,valid=0,tail=0,malformed=0,pure=1,paths=1,canon=1,nul=0,diff-read=err closed=0\n'
    i5_detail 'I5 detail=reason=base-ref-unresolvable'
    return 2
  fi
  if ! git --no-optional-locks -C "$lane" rev-parse --verify --quiet "$ref^{commit}" >/dev/null 2>&1; then
    printf 'I5 payload=declared=0,valid=0,tail=0,malformed=0,pure=1,paths=1,canon=1,nul=0,diff-read=err closed=0\n'
    i5_detail 'I5 detail=reason=ref-unresolvable'
    return 2
  fi

  rootreal=$(i5_canon "$root")
  if [ -z "$rootreal" ]; then
    printf 'I5 payload=declared=0,valid=0,tail=0,malformed=0,pure=1,paths=1,canon=1,nul=0,diff-read=err closed=0\n'
    i5_detail 'I5 detail=reason=export-root-unresolvable'
    return 2
  fi
  # A degenerate export root ("/") would make the containment clause vacuous,
  # so refuse it rather than grade it green.
  if [ "$rootreal" = / ]; then
    printf 'I5 payload=declared=0,valid=0,tail=0,malformed=0,pure=1,paths=1,canon=1,nul=0,diff-read=err closed=0\n'
    i5_detail 'I5 detail=reason=export-root-degenerate'
    return 2
  fi

  nulmap=$(i5_collect_nul "$declfile")
  if [ -n "$nulmap" ]; then nul=1; fi

  while IFS=' ' read -r lineno path lines sha; do
    [ -n "$lineno" ] || continue
    declared_n=$((declared_n + 1))
    if [ "$path" = MALFORMED ]; then
      malformed=$((malformed + 1))
      i5_detail "I5-decl path=- lines=- verdict=fail reason=malformed-line"
      continue
    fi
    nulstate=ok
    if printf '%s\n' "$nulmap" | grep -qx -- "$lineno nul"; then
      nulstate=nul
    fi
    if i5_grade_one "$rootreal" "$lane" "$base" "$ref" "$path" "$lines" "$sha" "$nulstate"; then
      valid_n=$((valid_n + 1))
      tail_n=$((tail_n + 1))
      i5_detail "I5-decl path=$path lines=$lines verdict=pass reason=-"
    else
      case $I5_REASON in
        path-absolute|path-escape|path-shape) paths=0 ;;
        escapes-root) canon=0 ;;
        diff-deleted) pure=0 ;;
      esac
      i5_detail "I5-decl path=$path lines=$lines verdict=fail reason=$I5_REASON"
    fi
  done < <(i5_read_declarations "$declfile")

  if [ "$declared_n" -lt 1 ]; then
    i5_detail 'I5 detail=reason=declared-empty'
    diffread=err
  fi

  printf 'I5 payload=declared=%s,valid=%s,tail=%s,malformed=%s,pure=%s,paths=%s,canon=%s,nul=%s,diff-read=%s closed=%s\n' \
    "$declared_n" "$valid_n" "$tail_n" "$malformed" "$pure" "$paths" "$canon" "$nul" "$diffread" \
    "$([ "$declared_n" -ge 1 ] && [ "$valid_n" -eq "$declared_n" ] && [ "$nul" -eq 0 ] \
        && [ "$diffread" = ok ] && echo 1 || echo 0)"
  if [ "$declared_n" -ge 1 ] && [ "$valid_n" -eq "$declared_n" ] && [ "$nul" -eq 0 ] \
     && [ "$diffread" = ok ]; then
    return 0
  fi
  return 1
}

# i5_check_in_tree TREE REF — the suite-facing wrapper, in the idiom of the
# round-40 suite's `check_h9 TREE REF`: it reads the globals LANE, BASE_REF
# and DECLARED (a path relative to the export tree) and grades the declared
# file inside TREE. The committed r41 suite can call this directly.
i5_check_in_tree() { # TREE REF
  i5_declared_blocks_check "$1" "$LANE" "$BASE_REF" "$2" "$DECLARED"
}

# i5_legacy_h9_check — the round-40 H9 rule set (path shape, tail, numstat;
# NO containment clause). CONTROL ONLY: it exists so the selftest can show
# that the T7 symlink escape was GREEN under the old rules. It is not a
# validator and must never be used to grade a real claim.
i5_legacy_h9_check() {
  local root=$1 lane=$2 base=$3 ref=$4 declared=$5
  local rootreal declfile line path lines sha extra
  local declared_n=0 valid_n=0 tail_n=0 pure=1 paths=1
  local f got nm added deleted

  rootreal=$(i5_canon "$root")
  case $declared in /*) declfile=$declared ;; *) declfile=$root/$declared ;; esac
  [ -r "$declfile" ] || { printf 'legacy declared=0 valid=0 tail=0 pure=1 paths=1\n'; return 2; }

  while IFS= read -r line || [ -n "$line" ]; do
    case $line in ''|'#'*) continue ;; esac
    declared_n=$((declared_n + 1))
    path=; lines=; sha=; extra=
    set -f
    set -- $line
    set +f
    path=${1:-}; lines=${2:-}; sha=${3:-}; extra=${4:-}
    if [ -z "$path" ] || [ -z "$lines" ] || [ -z "$sha" ] || [ -n "$extra" ]; then continue; fi
    case $lines in ''|*[!0-9]*) continue ;; esac
    [ "$lines" -ge 1 ] || continue
    case $sha in ''|*[!0-9a-f]*) continue ;; esac
    [ "${#sha}" -eq 64 ] || continue
    if ! i5_shape_ok "$path"; then paths=0; continue; fi
    f=$rootreal/$path
    [ -f "$f" ] || { paths=0; continue; }
    got=$(i5_tail_sha "$f" "$lines")
    [ "$got" = "$sha" ] || continue
    nm=$(i5_numstat "$lane" "$base" "$ref" "$path")
    case $nm in ERR|ABSENT|MULTI|BINARY) continue ;; esac
    added=${nm%% *}
    deleted=${nm##* }
    [ "$deleted" = 0 ] || { pure=0; continue; }
    [ "$added" = "$lines" ] || continue
    tail_n=$((tail_n + 1))
    valid_n=$((valid_n + 1))
  done < "$declfile"

  printf 'legacy declared=%s valid=%s tail=%s pure=%s paths=%s\n' \
    "$declared_n" "$valid_n" "$tail_n" "$pure" "$paths"
  if [ "$declared_n" -ge 1 ] && [ "$valid_n" -eq "$declared_n" ] && [ "$pure" -eq 1 ] \
     && [ "$paths" -eq 1 ]; then
    return 0
  fi
  return 1
}

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

i5_usage() {
  sed -n '2,/^set -uo pipefail$/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'
}

i5_main() {
  local MODE=check EXPORT_ROOT= LANE=$I5_LANE_DEFAULT BASE= REF= DECLARED= KEEP=0
  while [ $# -gt 0 ]; do
    case $1 in
      --check) MODE=check; shift ;;
      --selftest) MODE=selftest; shift ;;
      --keep) KEEP=1; shift ;;
      --export-root) [ $# -ge 2 ] || { printf 'i5: missing --export-root value\n' >&2; return 2; }; EXPORT_ROOT=$2; shift 2 ;;
      --lane) [ $# -ge 2 ] || { printf 'i5: missing --lane value\n' >&2; return 2; }; LANE=$2; shift 2 ;;
      --base) [ $# -ge 2 ] || { printf 'i5: missing --base value\n' >&2; return 2; }; BASE=$2; shift 2 ;;
      --ref) [ $# -ge 2 ] || { printf 'i5: missing --ref value\n' >&2; return 2; }; REF=$2; shift 2 ;;
      --declared) [ $# -ge 2 ] || { printf 'i5: missing --declared value\n' >&2; return 2; }; DECLARED=$2; shift 2 ;;
      -h|--help) i5_usage; return 0 ;;
      *) printf 'i5: unknown argument: %s\n' "$1" >&2; return 2 ;;
    esac
  done
  if [ "$MODE" = selftest ]; then
    i5_selftest "$KEEP"
    return $?
  fi
  [ -n "$EXPORT_ROOT" ] || { printf 'i5: missing --export-root\n' >&2; return 2; }
  [ -n "$BASE" ] || { printf 'i5: missing --base\n' >&2; return 2; }
  [ -n "$REF" ] || { printf 'i5: missing --ref\n' >&2; return 2; }
  [ -n "$DECLARED" ] || { printf 'i5: missing --declared\n' >&2; return 2; }
  i5_declared_blocks_check "$EXPORT_ROOT" "$LANE" "$BASE" "$REF" "$DECLARED"
}

# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------

I5_ST_ROOT=
I5_ST_FAILS=0
I5_ST_CASES=0

i5_st_cleanup() {
  if [ -n "$I5_ST_ROOT" ] && [ -d "$I5_ST_ROOT" ] && [ "${I5_ST_KEEP:-0}" != 1 ]; then
    rm -rf -- "$I5_ST_ROOT"
  fi
}

# i5_st_expect LABEL EXPECTED_REASON FILE — grade FILE and require the
# reported reason to be EXPECTED_REASON (`pass` for an honest declaration).
i5_st_expect() {
  local label=$1 expect=$2 file=$3
  local out rc reason verdict
  I5_ST_CASES=$((I5_ST_CASES + 1))
  out=$(i5_declared_blocks_check "$I5_ST_ROOT/export" "$I5_ST_ROOT/fixture" \
    "$I5_ST_BASE" "$I5_ST_REF" "$file" 2>&1)
  rc=$?
  reason=$(printf '%s\n' "$out" | sed -n 's/.*verdict=fail reason=\([a-z-]*\).*/\1/p' | sed -n 1p)
  if [ "$expect" = pass ]; then
    if [ "$rc" -eq 0 ]; then
      verdict=pass
    else
      verdict=fail
      reason=${reason:-closed-0}
      I5_ST_FAILS=$((I5_ST_FAILS + 1))
    fi
  else
    if [ "$rc" -eq 1 ] && [ "$reason" = "$expect" ]; then
      verdict=pass
    else
      verdict=fail
      I5_ST_FAILS=$((I5_ST_FAILS + 1))
    fi
  fi
  if [ "$reason" = "$expect" ]; then
    printf 'selftest case=I5 %s verdict=%s reason=%s\n' "$label" "$verdict" "$expect"
  elif [ "$expect" = pass ] && [ -z "$reason" ]; then
    printf 'selftest case=I5 %s verdict=%s reason=-\n' "$label" "$verdict"
  else
    printf 'selftest case=I5 %s verdict=%s reason=%s\n' "$label" "$verdict" "${reason:-none}"
  fi
  printf '%s\n' "$out" | sed "s|^|selftest detail=case=$label |"
}

i5_selftest() {
  local keep=$1
  local D base ref ref_del tree decl
  local da d1 d3 de
  I5_ST_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/i5-blocks.XXXXXXXX") || {
    printf 'selftest error=mktemp-failed\n'; return 2; }
  I5_ST_KEEP=$keep
  trap 'i5_st_cleanup' EXIT HUP INT TERM

  D=$I5_ST_ROOT/fixture
  mkdir -p -- "$D"
  git -C "$D" init -q || { printf 'selftest error=git-init-failed\n'; return 2; }
  if [ "$(git -C "$D" rev-parse --show-toplevel 2>/dev/null)" != "$(realpath -m -- "$D")" ]; then
    printf 'selftest error=toplevel-assert-failed\n'; return 2
  fi
  # base commit: the file the honest append lands on
  printf 'a\nb\nc\n' > "$D/doc.md"
  printf 'x\ny\nz\n' > "$D/edit.md"
  git -C "$D" add -A >/dev/null 2>&1
  git -C "$D" -c user.name=i5-fixture -c user.email=i5-fixture@invalid \
    commit -qm base >/dev/null 2>&1 || { printf 'selftest error=base-commit-failed\n'; return 2; }
  base=$(git -C "$D" rev-parse HEAD)

  # ref commit: a pure 3-line append, one rewritten line (a deletion), and two
  # symlinks whose targets live OUTSIDE the export (the T7 shape).
  printf 'a\nb\nc\n\n## Round-41 block\nsecond line\nthird line\n' > "$D/doc.md"
  printf 'x\ny\nw\n' > "$D/edit.md"
  ln -s /etc "$D/pwn"
  ln -s /etc/passwd "$D/pwn2"
  ln -s doc.md "$D/inner"
  git -C "$D" add -A >/dev/null 2>&1
  git -C "$D" -c user.name=i5-fixture -c user.email=i5-fixture@invalid \
    commit -qm ref >/dev/null 2>&1 || { printf 'selftest error=ref-commit-failed\n'; return 2; }
  ref=$(git -C "$D" rev-parse HEAD)

  tree=$I5_ST_ROOT/export
  mkdir -p -- "$tree"
  git -C "$D" archive --format=tar "$ref" | tar -x -C "$tree" \
    || { printf 'selftest error=archive-failed\n'; return 2; }

  I5_ST_BASE=$base
  I5_ST_REF=$ref

  decl=$I5_ST_ROOT/decl
  mkdir -p -- "$decl"

  da=$(i5_tail_sha "$tree/doc.md" 4)
  d1=$(i5_tail_sha "$tree/doc.md" 2)
  d99=$(i5_tail_sha "$tree/doc.md" 99)
  de=$(i5_tail_sha "$tree/edit.md" 1)
  # the digest of the LAST LINE of the file the symlink points at: the T7
  # declaration certifies bytes that live outside the export.
  outside=$(i5_tail_sha /etc/passwd 1)

  # honest: the declared append, exactly the appended tail
  printf 'doc.md 4 %s\n' "$da" > "$decl/ok.txt"
  # T7: a declared SYMLINK whose target is outside the export. The tail digest
  # matches the OUTSIDE file, so only the containment clause can reject it.
  printf 'pwn2 1 %s\n' "$outside" > "$decl/m_t7_symlink.txt"
  printf 'pwn 1 %s\n' "$outside" > "$decl/m_symlink_dir.txt"
  printf '../outside.md 1 %s\n' "$da" > "$decl/m_dotdot.txt"
  printf '/etc/passwd 1 %s\n' "$da" > "$decl/m_absolute.txt"
  printf 'doc.md 4 %s\000\n' "$da" > "$decl/m_nul.txt"
  printf 'doc.md 4 %064d\n' 0 > "$decl/m_tail.txt"
  printf 'doc.md 2 %s\n' "$d1" > "$decl/m_diff.txt"
  printf 'edit.md 1 %s\n' "$de" > "$decl/m_deleted.txt"
  printf 'doc.md 99 %s\n' "$d99" > "$decl/m_exceed.txt"
  printf 'nope.md 1 %s\n' "$da" > "$decl/m_absent.txt"
  # a symlink that stays INSIDE the export: contained, but git counts it as a
  # one-line blob, so it can never be an appended text block.
  printf 'inner 1 %s\n' "$da" > "$decl/m_inner_symlink.txt"
  # a malformed declaration must not be silently dropped: a gate must never be
  # green with a declaration it could not read.
  printf 'doc.md 4 %s\ndoc.md notanumber %s\n' "$da" "$da" > "$decl/m_malformed.txt"
  printf 'doc.md 4 %s\nnot-a-declaration\n' "$da" > "$decl/m_malformed2.txt"

  i5_st_expect honest pass "$decl/ok.txt"
  i5_st_expect t7-symlink-escape escapes-root "$decl/m_t7_symlink.txt"
  i5_st_expect symlink-to-directory escapes-root "$decl/m_symlink_dir.txt"
  i5_st_expect path-dotdot path-escape "$decl/m_dotdot.txt"
  i5_st_expect path-absolute path-absolute "$decl/m_absolute.txt"
  i5_st_expect path-nul nul-byte "$decl/m_nul.txt"
  i5_st_expect tail-mismatch tail-mismatch "$decl/m_tail.txt"
  i5_st_expect diff-added-mismatch diff-mismatch "$decl/m_diff.txt"
  i5_st_expect diff-with-deletion diff-deleted "$decl/m_deleted.txt"
  i5_st_expect lines-exceed-file lines-exceed-file "$decl/m_exceed.txt"
  i5_st_expect path-absent absent "$decl/m_absent.txt"
  i5_st_expect inner-symlink symlink-declared "$decl/m_inner_symlink.txt"
  i5_st_expect malformed-line malformed-line "$decl/m_malformed.txt"
  i5_st_expect malformed-line-2 malformed-line "$decl/m_malformed2.txt"

  # legacy control: the round-40 rule set grades the T7 fixture GREEN
  if i5_legacy_h9_check "$tree" "$D" "$base" "$ref" "$decl/m_t7_symlink.txt" >/dev/null 2>&1; then
    printf 'selftest legacy=round40-h9 case=t7-symlink-escape verdict=green\n'
  else
    printf 'selftest legacy=round40-h9 case=t7-symlink-escape verdict=red\n'
  fi

  printf 'selftest cases=%s failures=%s\n' "$I5_ST_CASES" "$I5_ST_FAILS"
  trap - EXIT HUP INT TERM
  i5_st_cleanup
  [ "$I5_ST_FAILS" -eq 0 ] || return 1
  return 0
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  i5_main "$@"
  exit $?
fi
