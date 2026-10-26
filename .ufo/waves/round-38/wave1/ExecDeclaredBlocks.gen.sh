#!/usr/bin/env bash
# declared-blocks — the declared-block contract behind G1 (round-38 claim C1,
# routed defect D-A: an append whose landed bytes were not the bytes the scribe
# declared). One declaration per file, in
# `<lane>/.ufo/waves/round-38/declared-blocks.txt`:
#
#   <path> <lines> <sha256>
#
# <path> is lane-relative (no leading `/`, no `..`); <lines> is the number of
# lines the append adds to the end of that file; <sha256> is the digest of the
# bytes the documented check prints:
#
#   tail -n <lines> <path> | sha256sum      == <sha256>
#
# The declaration therefore asserts the file's LAST <lines> lines, byte for byte.
# A block is declared exactly as `cat <block-file>... >> <path>` lands it: the
# bytes between the old end-of-file and the new one. Because the check is
# suffix-anchored, an append that is not last in the file (junk pasted after the
# block — the round-37 D-A shape) changes the tail and is red; an append that
# merely follows the block can only be caught by an explicit base guard:
#
#   # base <path> <pre_lines>
#
# which additionally requires `wc -l <path>` == <pre_lines> + <lines> once the
# block has landed. `gen` prints the guard it would emit on stderr; it is
# optional, and only sound for a file whose declared append is its last append.
# Blank lines and `#` comments other than `base` are ignored; every other line
# must parse, one declaration per path (concatenate a round's several appends
# into one block file and declare that), and an empty list is red — a gate must
# never be green with nothing declared.
#
# Commands:
#   gen <path> <block-file>...
#        Print the declaration line a pending `cat <block-file>... >> <path>`
#        will satisfy. <path> must be the lane-relative path as it will appear
#        in the declaration file. Refuses (exit 2) when the target does not end
#        with a newline: `cat` would merge the block into the target's last
#        line, which no line-suffix declaration can express.
#   check <declared-blocks.txt> [--root DIR]
#        Verify every declaration against DIR (default: `.`). Prints one line
#        per declaration, then `declared=<n> ok=<n> fail=<n> base=<n> exit=0|1`;
#        exit 0 only when every declaration and every base guard holds.
#   selftest [--root DIR]
#        Reject the contract's own mutants in a scratch copy (PROVINCE.md from
#        --root when present, else a synthetic front-door fixture): 8 cases,
#        `selftest cases=8 failures=0` when every mutant is rejected.
#
# Exit codes: 0 pass, 1 a defect is present (declaration or fixture is red),
# 2 a defect in this invocation (unreadable input, unterminated target).
# Writes only under `mktemp -d` (TMPDIR-honouring) scratch, removed on exit.
set -uo pipefail

ME=${0##*/}
SELF=${BASH_SOURCE[0]:-}
MODE=
ROOT=
SCRATCH=
POS=()

die() {
  printf '%s: %s\n' "$ME" "$*" >&2
  exit 2
}

usage() {
  if [ -n "$SELF" ] && [ -r "$SELF" ]; then
    sed -n '2,/^set -uo pipefail$/p' "$SELF" | sed -e '$d' -e 's/^# \{0,1\}//'
  else
    printf 'usage: %s gen <path> <block-file>... | check <declared-blocks.txt> [--root DIR] | selftest [--root DIR]\n' "$ME"
  fi
}

cleanup() {
  [ -n "${SCRATCH:-}" ] && rm -rf -- "$SCRATCH"
}

make_scratch() {
  SCRATCH=$(mktemp -d -t declared-blocks.XXXXXXXX) || die 'cannot create a scratch dir (TMPDIR)'
  trap cleanup EXIT
}

# last_byte_octal FILE — the final byte of FILE as a decimal value (empty file:
# nothing), read without assuming the file's length.
last_byte() {
  tail -c 1 -- "$1" 2>/dev/null | od -An -tu1 | tr -d ' \n'
}

# line_count FILE — newline count, so a final unterminated line is not counted
# as a line: the contract's <lines> is about `tail -n`, not about `wc -l`
# agreeing with an editor's view.
line_count() {
  local n
  n=$(wc -l < "$1" 2>/dev/null) || return 1
  n=${n// /}
  printf '%s\n' "${n:-0}"
}

parse_args() {
  while [ $# -gt 0 ]; do
    case $1 in
      gen|check|selftest)
        [ -z "$MODE" ] || die "two commands given: $MODE and $1"
        MODE=$1; shift ;;
      --root)
        [ $# -ge 2 ] || die '--root needs a directory'
        ROOT=$2; shift 2 ;;
      --root=*)
        ROOT=${1#--root=}; shift ;;
      -h|--help)
        usage; exit 0 ;;
      --)
        shift
        while [ $# -gt 0 ]; do POS+=("$1"); shift; done ;;
      -*)
        printf '%s: unknown option: %s\n' "$ME" "$1" >&2
        usage >&2
        exit 2 ;;
      *)
        POS+=("$1"); shift ;;
    esac
  done
}

# gen_main — print `<path> <lines> <sha256>` for a pending append.
#
# <lines> counts the newline-terminated lines the block adds, plus one when the
# block's last line is unterminated (which still begins a line of the result).
# <sha256> is measured, not predicted: the block is written into a probe file
# behind one sentinel line, `tail -n <lines>` is run on the probe exactly as the
# documented check runs it on the target, and the digest of those bytes is the
# declaration. A host whose tail normalises an unterminated final line is
# therefore reported (tail_view=normalized) instead of silently producing a
# digest the check cannot reproduce.
gen_main() {
  [ ${#POS[@]} -ge 1 ] || die 'gen needs <path> <block-file>...'
  local target=${POS[0]}
  local -a blocks=("${POS[@]:1}")
  [ ${#blocks[@]} -ge 1 ] || die 'gen needs <path> <block-file>...'
  case $target in
    /*) die "gen takes the lane-relative path, not an absolute one: $target" ;;
    *..*) die "gen takes a lane-relative path with no '..': $target" ;;
  esac
  [ -f "$target" ] || die "target is not a regular file: $target"
  local b
  for b in "${blocks[@]}"; do
    [ -f "$b" ] || die "block file is not a regular file: $b"
    [ -s "$b" ] || die "block file is empty: $b"
  done
  local pre first
  pre=$(line_count "$target") || die "cannot read target: $target"
  first=$(last_byte "$target")
  [ "$first" = 10 ] \
    || die "target does not end with a newline: $target (cat would merge the block into its last line; no line-suffix declaration can express that append)"

  make_scratch
  local block=$SCRATCH/block probe=$SCRATCH/probe
  : > "$block" || die 'cannot write scratch block'
  for b in "${blocks[@]}"; do
    cat -- "$b" >> "$block" || die "cannot read block file: $b"
  done
  { printf 'p\n'; cat -- "$block"; } > "$probe" || die 'cannot write scratch probe'

  local bytes nl lines sha view
  bytes=$(wc -c < "$block"); bytes=${bytes// /}
  nl=$(line_count "$block") || die 'cannot count scratch block lines'
  if [ "$(last_byte "$block")" = 10 ]; then
    lines=$nl
  else
    lines=$((nl + 1))
  fi
  [ "$lines" -ge 1 ] || die 'the block adds no line'
  sha=$(tail -n "$lines" -- "$probe" | sha256sum | awk '{print $1; exit}')
  [ -n "$sha" ] || die 'cannot digest the probe tail'
  view=exact
  cmp -s -- "$block" <(tail -n "$lines" -- "$probe") || view=normalized

  printf '%s %s %s\n' "$target" "$lines" "$sha"
  printf '%s: target=%s pre_lines=%s post_lines=%s block_bytes=%s block_newlines=%s declared_lines=%s tail_view=%s\n' \
    "$ME" "$target" "$pre" "$((pre + lines))" "$bytes" "$nl" "$lines" "$view" >&2
  printf '%s: optional base guard: # base %s %s\n' "$ME" "$target" "$pre" >&2
  return 0
}

# check_declaration ROOT LINENO LINE — verify one `<path> <lines> <sha256>`.
# Returns 0 on a match, 1 on any red, 2 reserving nothing: a malformed line is a
# red declaration, not a usage error, so a gate cannot be silenced by mangling.
check_declaration() {
  local root=$1 lineno=$2 line=$3
  local -a f=()
  read -r -a f <<< "$line"
  if [ ${#f[@]} -ne 3 ]; then
    printf 'FAIL line=%s malformed: want "<path> <lines> <sha256>", got %s field(s): %s\n' \
      "$lineno" "${#f[@]}" "$line"
    return 1
  fi
  local path=${f[0]} count=${f[1]} want=${f[2]}
  case $path in
    /*)
      printf 'FAIL line=%s path must be lane-relative: %s\n' "$lineno" "$path"; return 1 ;;
    *..*)
      printf 'FAIL line=%s path must not contain "..": %s\n' "$lineno" "$path"; return 1 ;;
  esac
  if ! [[ $count =~ ^[1-9][0-9]*$ ]]; then
    printf 'FAIL line=%s lines must be a positive integer: %s\n' "$lineno" "$count"; return 1
  fi
  if ! [[ $want =~ ^[0-9a-f]{64}$ ]]; then
    printf 'FAIL line=%s sha256 must be 64 lowercase hex: %s\n' "$lineno" "$want"; return 1
  fi
  if [ ! -f "$root/$path" ]; then
    printf 'FAIL %s lines=%s file-missing under root=%s\n' "$path" "$count" "$root"; return 1
  fi
  local got total
  got=$(tail -n "$count" -- "$root/$path" | sha256sum | awk '{print $1; exit}')
  total=$(line_count "$root/$path") || total=?
  if [ "$got" = "$want" ]; then
    printf 'OK   %s lines=%s file_lines=%s sha256=%s\n' "$path" "$count" "$total" "$got"
    return 0
  fi
  printf 'FAIL %s lines=%s want=%s got=%s file_lines=%s\n' \
    "$path" "$count" "$want" "$got" "$total"
  return 1
}

check_main() {
  [ ${#POS[@]} -eq 1 ] || die 'check needs exactly one <declared-blocks.txt>'
  local list=${POS[0]}
  [ -f "$list" ] || die "declaration file is not a regular file: $list"
  local root=${ROOT:-.}
  [ -d "$root" ] || die "root is not a directory: $root"
  local ok=0 fail=0 declared=0 bases=0 lineno=0 line total
  local -A seen=() decl_lines=()
  local -a base_path=() base_pre=()
  while IFS= read -r line || [ -n "$line" ]; do
    lineno=$((lineno + 1))
    line=${line%$'\r'}
    line=${line#"${line%%[![:space:]]*}"}
    line=${line%"${line##*[![:space:]]}"}
    [ -z "$line" ] && continue
    if [ "${line:0:1}" = '#' ]; then
      local -a g=()
      read -r -a g <<< "${line#\#}"
      if [ ${#g[@]} -ge 1 ] && [ "${g[0]}" = base ]; then
        if [ ${#g[@]} -ne 3 ]; then
          fail=$((fail + 1))
          printf 'FAIL line=%s malformed base guard: want "# base <path> <pre_lines>": %s\n' "$lineno" "$line"
          continue
        fi
        base_path+=("${g[1]}"); base_pre+=("${g[2]}"); bases=$((bases + 1))
      fi
      continue
    fi
    local -a f=()
    read -r -a f <<< "$line"
    if [ ${#f[@]} -eq 3 ]; then
      case ${f[0]} in
        /*|*..*) ;;
        *)
          if [[ ${f[1]} =~ ^[1-9][0-9]*$ ]] && [[ ${f[2]} =~ ^[0-9a-f]{64}$ ]]; then
            if [ -n "${seen[${f[0]}]:-}" ]; then
              fail=$((fail + 1))
              printf 'FAIL line=%s duplicate declaration for %s (one declaration per file; concatenate the round appends into one block file)\n' \
                "$lineno" "${f[0]}"
              continue
            fi
            seen[${f[0]}]=${f[1]}
            decl_lines[${f[0]}]=${f[1]}
          fi ;;
      esac
    fi
    declared=$((declared + 1))
    if check_declaration "$root" "$lineno" "$line"; then ok=$((ok + 1)); else fail=$((fail + 1)); fi
  done < "$list"

  local i p pre
  for i in "${!base_path[@]}"; do
    p=${base_path[$i]}; pre=${base_pre[$i]}
    if ! [[ $pre =~ ^[0-9]+$ ]]; then
      fail=$((fail + 1)); printf 'FAIL base %s pre_lines must be a non-negative integer: %s\n' "$p" "$pre"; continue
    fi
    if [ -z "${decl_lines[$p]:-}" ]; then
      fail=$((fail + 1)); printf 'FAIL base %s has no declaration for that path\n' "$p"; continue
    fi
    if [ ! -f "$root/$p" ]; then
      fail=$((fail + 1)); printf 'FAIL base %s file-missing under root=%s\n' "$p" "$root"; continue
    fi
    total=$(line_count "$root/$p") || total=?
    if [ "$total" = "$((pre + decl_lines[$p]))" ]; then
      printf 'OK   base %s file_lines=%s pre_lines=%s declared_lines=%s\n' \
        "$p" "$total" "$pre" "${decl_lines[$p]}"
    else
      fail=$((fail + 1))
      printf 'FAIL base %s file_lines=%s != pre_lines=%s + declared_lines=%s (lines were added before the declared block)\n' \
        "$p" "$total" "$pre" "${decl_lines[$p]}"
    fi
  done

  if [ "$declared" -eq 0 ]; then
    fail=$((fail + 1))
    printf 'FAIL %s carries no declaration\n' "$list"
  fi
  printf 'declared=%s ok=%s fail=%s base=%s exit=%s\n' \
    "$declared" "$ok" "$fail" "$bases" "$([ "$fail" -eq 0 ] && printf 0 || printf 1)"
  [ "$fail" -eq 0 ]
}

# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------

ST_CASES=0
ST_FAILS=0
ST_ROOT=

st_fixture() { # DIR — a front-door-like file ending with a newline
  if [ -n "$ST_ROOT" ] && [ -f "$ST_ROOT/PROVINCE.md" ]; then
    cp -- "$ST_ROOT/PROVINCE.md" "$1/front.md" || return 1
  else
    printf '# fixture front door\n\nline two\n' > "$1/front.md" || return 1
  fi
}

st_block3() { # FILE — exactly three lines, newline-terminated
  printf '[fixture amendment, appended] first\nsecond\nthird\n' > "$1"
}

# st_gen DIR PATH BLOCK... — run gen and capture its single stdout line.
st_gen() {
  local dir=$1 path=$2; shift 2
  ( cd "$dir" && bash "$SELF_ABS" gen "$path" "$@" 2>/dev/null )
}

st_case() { # ID FUNCTION
  local id=$1 fn=$2
  ST_CASES=$((ST_CASES + 1))
  if "$fn"; then
    printf 'selftest case=%s name=%s result=pass\n' "$id" "$fn"
  else
    ST_FAILS=$((ST_FAILS + 1))
    printf 'selftest case=%s name=%s result=fail\n' "$id" "$fn"
  fi
}

case_T1() { # append a declared block -> check ok
  local d=$SCRATCH/T1
  mkdir -p "$d" || return 1
  st_fixture "$d" || return 1
  st_block3 "$d/block" || return 1
  local decl
  decl=$(st_gen "$d" front.md "$d/block") || return 1
  printf '%s\n' "$decl" > "$d/declared-blocks.txt" || return 1
  local want_lines=${decl#front.md }; want_lines=${want_lines%% *}
  local want_sha=${decl##* }
  [ "$want_lines" = 3 ] || { printf '  gen said lines=%s, want 3\n' "$want_lines"; return 1; }
  cat -- "$d/block" >> "$d/front.md" || return 1
  local out rc
  out=$(cd "$d" && bash "$SELF_ABS" check declared-blocks.txt 2>&1); rc=$?
  printf '%s\n' "$out" | sed 's/^/  /'
  [ "$rc" -eq 0 ] || return 1
  [ "$(tail -n 3 -- "$d/front.md" | sha256sum | awk '{print $1; exit}')" = "$want_sha" ] || return 1
  return 0
}

case_T2() { # flip one byte inside the declared block -> check red
  local d=$SCRATCH/T2
  mkdir -p "$d" || return 1
  st_fixture "$d" || return 1
  st_block3 "$d/block" || return 1
  st_gen "$d" front.md "$d/block" > "$d/declared-blocks.txt" || return 1
  cat -- "$d/block" >> "$d/front.md" || return 1
  ( cd "$d" && bash "$SELF_ABS" check declared-blocks.txt ) >/dev/null 2>&1 \
    || { printf '  pristine copy was already red\n'; return 1; }
  sed -i 's/^second$/secOnd/' "$d/front.md" || return 1
  local out rc
  out=$(cd "$d" && bash "$SELF_ABS" check declared-blocks.txt 2>&1); rc=$?
  printf '%s\n' "$out" | sed 's/^/  /'
  [ "$rc" -eq 1 ] || return 1
  printf '%s\n' "$out" | grep -q '^FAIL front.md lines=3 want=' || return 1
  return 0
}

case_T3() { # append one line after the declared block -> check red
  local d=$SCRATCH/T3
  mkdir -p "$d" || return 1
  st_fixture "$d" || return 1
  st_block3 "$d/block" || return 1
  st_gen "$d" front.md "$d/block" > "$d/declared-blocks.txt" || return 1
  cat -- "$d/block" >> "$d/front.md" || return 1
  printf 'stray line appended after the block\n' >> "$d/front.md" || return 1
  local out rc
  out=$(cd "$d" && bash "$SELF_ABS" check declared-blocks.txt 2>&1); rc=$?
  printf '%s\n' "$out" | sed 's/^/  /'
  [ "$rc" -eq 1 ] || return 1
  printf '%s\n' "$out" | grep -q '^FAIL front.md lines=3 want=' || return 1
  return 0
}

case_T4() { # block without a final newline -> declared lines = newlines + 1
  local d=$SCRATCH/T4
  mkdir -p "$d" || return 1
  st_fixture "$d" || return 1
  printf 'no final newline on this block line' > "$d/block" || return 1
  local decl
  decl=$(st_gen "$d" front.md "$d/block") || return 1
  printf '%s\n' "$decl" > "$d/declared-blocks.txt" || return 1
  local want_lines=${decl#front.md }; want_lines=${want_lines%% *}
  local want_sha=${decl##* }
  [ "$want_lines" = 1 ] || { printf '  gen said lines=%s, want 1\n' "$want_lines"; return 1; }
  [ "$want_sha" = "$(sha256sum < "$d/block" | awk '{print $1; exit}')" ] \
    || { printf '  declared digest is not the block digest\n'; return 1; }
  cat -- "$d/block" >> "$d/front.md" || return 1
  local out rc
  out=$(cd "$d" && bash "$SELF_ABS" check declared-blocks.txt 2>&1); rc=$?
  printf '%s  (tail_view=exact: tail reprinted the unterminated line verbatim)\n' "$out" | sed 's/^/  /'
  [ "$rc" -eq 0 ] || return 1
  # and the block really is the file's unterminated tail
  [ "$(last_byte "$d/front.md")" != 10 ] || { printf '  fixture tail was newline-terminated\n'; return 1; }
  return 0
}

case_T5() { # unterminated target -> gen refuses with the documented reason
  local d=$SCRATCH/T5
  mkdir -p "$d" || return 1
  printf 'no trailing newline' > "$d/front.md" || return 1
  st_block3 "$d/block" || return 1
  local out rc
  out=$(cd "$d" && bash "$SELF_ABS" gen front.md "$d/block" 2>&1); rc=$?
  printf '%s\n' "$out" | sed 's/^/  /'
  [ "$rc" -eq 2 ] || return 1
  printf '%s\n' "$out" | grep -q 'does not end with a newline' || return 1
  return 0
}

case_T6() { # malformed / duplicate / empty declaration lists are all red
  local d=$SCRATCH/T6 rc bad=0 out
  mkdir -p "$d" || return 1
  st_fixture "$d" || return 1
  st_block3 "$d/block" || return 1
  cat -- "$d/block" >> "$d/front.md" || return 1
  local good
  good=$(st_gen "$d" front.md "$d/block") || return 1
  local good_sha=${good##* }
  local ref=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
  local upper=0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF

  printf 'front.md 3 %s\n' "$upper" > "$d/bad-sha.txt"
  printf 'front.md 3 %s\n' "$ref" > "$d/wrong-sha.txt"
  printf 'front.md x %s\n' "$good_sha" > "$d/bad-lines.txt"
  printf 'front.md %s\n' "$good_sha" > "$d/two-fields.txt"
  { printf '%s\n' "$good"; printf 'front.md 3 %s\n' "$good_sha"; } > "$d/dup.txt"
  { printf '# only a comment\n\n'; } > "$d/empty.txt"
  for f in bad-sha wrong-sha bad-lines two-fields dup empty; do
    out=$(cd "$d" && bash "$SELF_ABS" check "$f.txt" 2>&1); rc=$?
    printf '  %-11s rc=%s  %s\n' "$f" "$rc" "$(printf '%s\n' "$out" | grep -E '^(FAIL|declared=)' | head -2 | tr '\n' ' ')"
    [ "$rc" -eq 1 ] || bad=1
  done
  return "$bad"
}

case_T7() { # junk inserted before the block: tail-only passes, base guard red
  local d=$SCRATCH/T7
  mkdir -p "$d" || return 1
  st_fixture "$d" || return 1
  st_block3 "$d/block" || return 1
  local decl pre
  decl=$(st_gen "$d" front.md "$d/block") || return 1
  pre=$(line_count "$d/front.md") || return 1
  printf 'junk inserted before the block\n' >> "$d/front.md" || return 1
  cat -- "$d/block" >> "$d/front.md" || return 1
  printf '%s\n' "$decl" > "$d/declared-blocks.txt" || return 1
  local out rc
  out=$(cd "$d" && bash "$SELF_ABS" check declared-blocks.txt 2>&1); rc=$?
  printf '  tail-only: rc=%s %s\n' "$rc" "$(printf '%s\n' "$out" | tail -1)"
  [ "$rc" -eq 0 ] || return 1
  # the guard names the fixture's line count as it stood before any append, so
  # the junk line inserted ahead of the declared block makes the total too large.
  printf '# base front.md %s\n' "$pre" > "$d/declared-base.txt"
  cat -- "$d/declared-blocks.txt" >> "$d/declared-base.txt"
  out=$(cd "$d" && bash "$SELF_ABS" check declared-base.txt 2>&1); rc=$?
  printf '%s\n' "$out" | sed 's/^/  /'
  [ "$rc" -eq 1 ] || return 1
  printf '%s\n' "$out" | grep -q '^FAIL base front.md' || return 1
  # and the guard is green on a clean append of the same block
  local e=$SCRATCH/T7b
  mkdir -p "$e" || return 1
  st_fixture "$e" || return 1
  printf '%s\n' "$decl" > "$e/declared-blocks.txt" || return 1
  { printf '# base front.md %s\n' "$pre"; cat -- "$e/declared-blocks.txt"; } > "$e/declared-base.txt"
  cat -- "$d/block" >> "$e/front.md" || return 1
  out=$(cd "$e" && bash "$SELF_ABS" check declared-base.txt 2>&1); rc=$?
  printf '  clean base guard: rc=%s %s\n' "$rc" "$(printf '%s\n' "$out" | tail -1)"
  [ "$rc" -eq 0 ] || return 1
  return 0
}

case_T8() { # block ending with a blank line (the r37 README shape)
  local d=$SCRATCH/T8
  mkdir -p "$d" || return 1
  st_fixture "$d" || return 1
  printf '## appended section\n\nrow\n\n' > "$d/block" || return 1
  local decl
  decl=$(st_gen "$d" front.md "$d/block") || return 1
  printf '%s\n' "$decl" > "$d/declared-blocks.txt" || return 1
  local want_lines=${decl#front.md }; want_lines=${want_lines%% *}
  [ "$want_lines" = 4 ] || { printf '  gen said lines=%s, want 4\n' "$want_lines"; return 1; }
  cat -- "$d/block" >> "$d/front.md" || return 1
  local out rc
  out=$(cd "$d" && bash "$SELF_ABS" check declared-blocks.txt 2>&1); rc=$?
  printf '%s\n' "$out" | sed 's/^/  /'
  [ "$rc" -eq 0 ] || return 1
  [ "$(tail -n 4 -- "$d/front.md" | od -An -c | tr -s ' ')" = "$(od -An -c < "$d/block" | tr -s ' ')" ] || return 1
  return 0
}

selftest_main() {
  [ ${#POS[@]} -eq 0 ] || die 'selftest takes no positional arguments'
  SELF_ABS=$(readlink -f -- "$SELF" 2>/dev/null) || SELF_ABS=$SELF
  [ -n "$SELF_ABS" ] && [ -r "$SELF_ABS" ] || die 'selftest needs the script path (run it from a file)'
  ST_ROOT=${ROOT:-}
  make_scratch
  local fx=synthetic
  if [ -n "$ST_ROOT" ] && [ -f "$ST_ROOT/PROVINCE.md" ]; then fx=PROVINCE.md; fi
  printf 'selftest fixture=%s root=%s\n' "$fx" "${ST_ROOT:-.}"
  st_case T1 case_T1
  st_case T2 case_T2
  st_case T3 case_T3
  st_case T4 case_T4
  st_case T5 case_T5
  st_case T6 case_T6
  st_case T7 case_T7
  st_case T8 case_T8
  local rc=0
  [ "$ST_FAILS" -eq 0 ] || rc=1
  printf 'selftest cases=%s failures=%s exit=%s\n' "$ST_CASES" "$ST_FAILS" "$rc"
  return "$rc"
}

main() {
  parse_args "$@"
  [ -n "$MODE" ] || { usage >&2; exit 2; }
  case $MODE in
    gen) gen_main ;;
    check) check_main ;;
    selftest) selftest_main ;;
  esac
}

main "$@"
