#!/usr/bin/env bash
# declared-blocks-validate.sh — the H9 limb: grade a `declared-blocks.txt`
# (lines `<path> <lines> <sha256>`) against a git-archive export of <ref> and a
# <base> ref. Read-only: nothing is written under the lane, the export or any
# tracked tree; the only writes are mktemp work dirs (honouring TMPDIR) that
# are removed on exit, and they exist only when --export is omitted or
# --selftest is asked for.
#
# Every declared line must satisfy ALL of:
#   (a) `tail -n <lines> <export>/<path>` hashes to <sha256>: the declaration is
#       the WHOLE appended tail, byte for byte;
#   (b) <path> is a plain relative path with no `/` root, no empty, `.` or `..`
#       component, resolves inside the export root (a symlink cannot carry the
#       read outside it), and the file exists there;
#   (c) `git -C <lane> diff --numstat <base> <ref> -- <path>` reports exactly one
#       record whose added count equals <lines> and whose deleted count is 0.
# Extra guards that harm no honest declaration: <lines> must not exceed the
# export file's own line count (else `tail -n` silently clips), a path may be
# declared once, and a declaration line must carry exactly three blank-free
# fields and a 64-hex lowercase digest.
#
# Usage:
#   bash declared-blocks-validate.sh --declared FILE --base REF --ref REF
#        [--lane DIR] [--export DIR]
#       Grade FILE. --export is an existing `git archive <ref>` extraction; when
#       omitted the tree is extracted once into a mktemp dir (removed on exit).
#       --lane defaults to $DECL_LANE, else the round's lane repo. Prints a
#       `decl head ...` line, one graded line per declaration
#       (`decl path=... lines=... tail=pass|fail safe=pass|fail diff=pass|fail
#       added=... deleted=... verdict=pass|fail reason=<clause|->`) and a final
#       `decl summary declared=<k> pass=<k> fail=<k> exit=<0|1>`.
#       Exit 0 only when at least one declaration was graded and every one
#       passed; exit 1 when any declaration fails; exit 2 on a setup error
#       (missing ref, unreadable export, no declared file).
#   bash declared-blocks-validate.sh --selftest
#       Build one throwaway git fixture (base commit -> ref commit with a pure
#       3-line append, a 1-line new file and an escaping symlink; a third commit
#       that also deletes a line), export the ref, and grade one good
#       declaration file (must pass) and eleven defective ones (each must be
#       rejected for the named clause).
#       Prints `selftest detail=...` lines, one graded
#       `selftest case=declared-blocks positive=... mutants=<k>/<n> verdict=...`
#       line and `selftest cases=1 failures=<k>`.
#   bash declared-blocks-validate.sh -h|--help
#       This text.
#
# All git reads use `--no-optional-locks`, so the lane is never locked or
# written. The fixture's git toplevel is asserted to be the fixture dir before
# any commit.
set -u

LANE=${DECL_LANE:-/home/vgpnk/Projects/shokunin/kasegi-shokunin}
DECLARED= BASE= REF= EXPORT= SELFTEST=0
WORK=
CLEAN=0

cleanup() {
  if [ "$CLEAN" -eq 1 ] && [ -n "$WORK" ] && [ -d "$WORK" ]; then
    rm -rf -- "$WORK"
  fi
}
trap cleanup EXIT HUP INT TERM

usage() { sed -n '2,/^set -u$/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; }

die() { printf 'decl error %s\n' "$*" >&2; exit 2; }

# path_safe PATH — no absolute path, no empty/./.. component (the round-38
# G1-H4 escape: a declaration that validated bytes outside the tree).
path_safe() {
  local p=$1 rest c
  case $p in ''|/*) return 1 ;; esac
  rest=$p
  while :; do
    c=${rest%%/*}
    case $c in ''|.|..) return 1 ;; esac
    case $rest in
      */*) rest=${rest#*/} ;;
      *) break ;;
    esac
  done
  return 0
}

file_lines() { awk 'END { print NR + 0 }' "$1" 2>/dev/null; }

tail_sha() { # FILE N
  tail -n "$2" -- "$1" 2>/dev/null | sha256sum | awk '{ print $1; exit }'
}

# numstat LANE BASE REF PATH — prints `<added> <deleted>`, or one of
# ERR (diff read failed), EMPTY (path not in the diff), MULTI (more than one
# record), BIN (binary counters).
numstat() {
  local out records added deleted
  if ! out=$(git --no-optional-locks -C "$1" diff --numstat "$2" "$3" -- "$4" 2>/dev/null); then
    printf 'ERR'; return 0
  fi
  [ -n "$out" ] || { printf 'EMPTY'; return 0; }
  records=$(printf '%s\n' "$out" | wc -l)
  [ "$records" -eq 1 ] || { printf 'MULTI'; return 0; }
  added=$(printf '%s\n' "$out" | awk 'NF >= 3 { print $1; exit }')
  deleted=$(printf '%s\n' "$out" | awk 'NF >= 3 { print $2; exit }')
  case $added$deleted in
    *[!0-9]*) printf 'BIN'; return 0 ;;
  esac
  printf '%s %s' "$added" "$deleted"
}

# grade_one TREE LANE BASE REF PATH LINES SHA — grade one declaration; prints the
# graded line; returns 0 when it passes.
grade_one() {
  local tree=$1 lane=$2 base=$3 ref=$4 path=$5 lines=$6 sha=$7
  local tail_v=fail safe_v=fail diff_v=fail added=- deleted=- reason=- total got nm rp root
  if ! path_safe "$path"; then
    reason=unsafe-path
  elif [ ! -e "$tree/$path" ]; then
    reason=absent
  elif [ ! -f "$tree/$path" ]; then
    reason=not-a-file
  else
    root=$(realpath -m -- "$tree") || root=
    rp=$(realpath -m -- "$tree/$path") || rp=
    if [ -z "$root" ] || [ -z "$rp" ]; then
      reason=unsafe-path
    else
      case $rp in
        "$root"/*) ;;
        *) reason=unsafe-path ;;
      esac
    fi
  fi
  if [ "$reason" = - ]; then
    total=$(file_lines "$tree/$path")
    total=${total:-0}
    if [ "$lines" -gt "$total" ]; then
      reason=lines-exceed-file
    else
      got=$(tail_sha "$tree/$path" "$lines")
      if [ "$got" = "$sha" ]; then
        tail_v=pass
        nm=$(numstat "$lane" "$base" "$ref" "$path")
        case $nm in
          ERR|EMPTY|MULTI|BIN) reason=diff-$nm ;;
          *)
            set -f
            set -- $nm
            set +f
            added=${1:--}; deleted=${2:--}
            if [ "$added" = "$lines" ] && [ "$deleted" = 0 ]; then
              diff_v=pass
            else
              reason=diff-mismatch
            fi
            ;;
        esac
      else
        reason=tail-mismatch
      fi
    fi
  fi
  [ "$reason" = - ] && safe_v=pass
  if [ "$reason" = - ] && [ "$tail_v" = pass ] && [ "$diff_v" = pass ]; then
    printf 'decl path=%s lines=%s tail=%s safe=%s diff=%s added=%s deleted=%s verdict=pass reason=-\n' \
      "$path" "$lines" "$tail_v" "$safe_v" "$diff_v" "$added" "$deleted"
    return 0
  fi
  printf 'decl path=%s lines=%s tail=%s safe=%s diff=%s added=%s deleted=%s verdict=fail reason=%s\n' \
    "$path" "$lines" "$tail_v" "$safe_v" "$diff_v" "$added" "$deleted" "$reason"
  return 1
}

# grade_file DECLARED TREE LANE BASE REF — grade every declaration line; prints
# the graded lines and the summary; returns 0 only for all-pass with k >= 1.
grade_file() {
  local f=$1 tree=$2 lane=$3 base=$4 ref=$5
  local line path lines sha extra key declared=0 pass=0 fail=0
  local -A witness=()
  if [ ! -r "$f" ]; then
    printf 'decl summary declared=0 pass=0 fail=0 exit=2\n'
    printf 'decl error declared-file-unreadable %s\n' "$f" >&2
    return 2
  fi
  while IFS= read -r line || [ -n "$line" ]; do
    case $line in ''|'#'*) continue ;; esac
    declared=$((declared + 1))
    path= lines= sha= extra=
    set -f
    set -- $line
    set +f
    path=${1:-}; lines=${2:-}; sha=${3:-}; extra=${4:-}
    if [ -z "$path" ] || [ -z "$lines" ] || [ -z "$sha" ] || [ -n "$extra" ]; then
      printf 'decl path=%s lines=%s tail=fail safe=fail diff=fail added=- deleted=- verdict=fail reason=malformed-line\n' \
        "${path:--}" "${lines:--}"
      fail=$((fail + 1)); continue
    fi
    case $lines in *[!0-9]*) lines=0 ;; esac
    if [ "$lines" -lt 1 ]; then
      printf 'decl path=%s lines=%s tail=fail safe=fail diff=fail added=- deleted=- verdict=fail reason=malformed-line\n' \
        "$path" "$lines"
      fail=$((fail + 1)); continue
    fi
    case $sha in *[!0-9a-f]*) sha=bad ;; esac
    if [ "$sha" = bad ] || [ "${#sha}" -ne 64 ]; then
      printf 'decl path=%s lines=%s tail=fail safe=fail diff=fail added=- deleted=- verdict=fail reason=malformed-hash\n' \
        "$path" "$lines"
      fail=$((fail + 1)); continue
    fi
    key=${path//[!A-Za-z0-9._\/-]/_}
    if [ -n "${witness[$key]:-}" ]; then
      printf 'decl path=%s lines=%s tail=fail safe=pass diff=fail added=- deleted=- verdict=fail reason=duplicate-path\n' \
        "$path" "$lines"
      fail=$((fail + 1)); continue
    fi
    witness[$key]=1
    if grade_one "$tree" "$lane" "$base" "$ref" "$path" "$lines" "$sha"; then
      pass=$((pass + 1))
    else
      fail=$((fail + 1))
    fi
  done < "$f"
  if [ "$declared" -lt 1 ] || [ "$fail" -ne 0 ]; then
    printf 'decl summary declared=%s pass=%s fail=%s exit=1\n' "$declared" "$pass" "$fail"
    return 1
  fi
  printf 'decl summary declared=%s pass=%s fail=%s exit=0\n' "$declared" "$pass" "$fail"
  return 0
}

need_ref() { # REF
  git --no-optional-locks -C "$LANE" rev-parse --verify --quiet "$1^{commit}" >/dev/null 2>&1 \
    || die "ref-not-in-lane: $1"
}

extract_ref() { # REF DIR
  mkdir -p -- "$2" || die "export-mkdir-failed: $2"
  git --no-optional-locks -C "$LANE" archive --format=tar "$1" | tar -x -C "$2" \
    || die "archive-failed: $1"
}

run_mode() {
  [ -n "$DECLARED" ] || die 'missing --declared FILE'
  [ -n "$BASE" ] || die 'missing --base REF'
  [ -n "$REF" ] || die 'missing --ref REF'
  [ -d "$LANE" ] || die "lane-not-a-dir: $LANE"
  need_ref "$BASE"
  need_ref "$REF"
  local tree rc
  if [ -n "$EXPORT" ]; then
    tree=$EXPORT
    [ -d "$tree" ] || die "export-not-a-dir: $tree"
    [ -n "$(ls -A -- "$tree" 2>/dev/null)" ] || die "export-empty: $tree"
    printf 'decl head mode=export ref=%s base=%s lane=%s export=%s\n' \
      "$REF" "$BASE" "$LANE" "$tree"
  else
    WORK=$(mktemp -d "${TMPDIR:-/tmp}/declared-blocks.XXXXXXXX") || die mktemp-failed
    CLEAN=1
    tree=$WORK/export
    extract_ref "$REF" "$tree"
    printf 'decl head mode=extract ref=%s base=%s lane=%s export=%s\n' \
      "$REF" "$BASE" "$LANE" "$tree"
  fi
  grade_file "$DECLARED" "$tree" "$LANE" "$BASE" "$REF"
  rc=$?
  exit "$rc"
}

# selftest — one fixture, one good declaration file, ten defective ones.
selftest() {
  local ROOT D SELF=$0 base ref ref_del tree decl ok rc expect name got reason
  local mutants=0 rejected=0 pos=pass nfail=0
  ROOT=$(mktemp -d "${TMPDIR:-/tmp}/declared-blocks-selftest.XXXXXXXX") \
    || die 'selftest-mktemp-failed'
  WORK=$ROOT
  CLEAN=1
  D=$ROOT/fixture
  mkdir -p "$D"
  printf 'TOP-SECRET\n' > "$ROOT/secret.txt"
  git -C "$D" init -q || die 'selftest-git-init-failed'
  if [ "$(git -C "$D" rev-parse --show-toplevel 2>/dev/null)" \
       != "$(realpath -m -- "$D")" ]; then
    die 'selftest-toplevel-assert-failed'
  fi
  printf 'a\nb\nc\n' > "$D/doc.md"
  printf 'x\n' > "$D/keep.md"
  git -C "$D" add -A >/dev/null 2>&1
  git -C "$D" -c user.name=selftest -c user.email=selftest@invalid \
    commit -qm base >/dev/null 2>&1 || die 'selftest-base-commit-failed'
  base=$(git -C "$D" rev-parse HEAD)
  printf '\n## Round block\nnew line\n' >> "$D/doc.md"
  printf 'x\n' > "$D/new.md"
  ln -s "$ROOT/secret.txt" "$D/link.md"
  git -C "$D" add -A >/dev/null 2>&1
  git -C "$D" -c user.name=selftest -c user.email=selftest@invalid \
    commit -qm ref >/dev/null 2>&1 || die 'selftest-ref-commit-failed'
  ref=$(git -C "$D" rev-parse HEAD)
  printf 'a\nb\n\n## Round block\nnew line\n' > "$D/doc.md"
  git -C "$D" add -A >/dev/null 2>&1
  git -C "$D" -c user.name=selftest -c user.email=selftest@invalid \
    commit -qm deletion-ref >/dev/null 2>&1 || die 'selftest-del-commit-failed'
  ref_del=$(git -C "$D" rev-parse HEAD)
  tree=$D/export
  mkdir -p "$tree"
  git -C "$D" archive --format=tar "$ref" | tar -x -C "$tree" \
    || die 'selftest-archive-failed'
  decl=$D/decl
  mkdir -p "$decl"

  local da db d1
  da=$(tail_sha "$tree/doc.md" 3)
  db=$(tail_sha "$tree/new.md" 1)
  d1=$(tail_sha "$tree/doc.md" 2)

  printf 'doc.md 3 %s\nnew.md 1 %s\n' "$da" "$db" > "$decl/ok.txt"
  ok=$(bash "$SELF" --declared "$decl/ok.txt" --base "$base" --ref "$ref" \
    --lane "$D" --export "$tree")
  rc=$?
  printf 'selftest detail=limb=positive rc=%s %s\n' "$rc" \
    "$(printf '%s\n' "$ok" | grep '^decl summary' | sed 's/^decl summary //')"
  if [ "$rc" -ne 0 ]; then pos=fail; nfail=$((nfail + 1)); fi

  printf 'doc.md 3 %064d\n' 1 > "$decl/m_tail.txt"
  printf 'doc.md 2 %s\n' "$d1" > "$decl/m_partial.txt"
  printf 'doc.md 3 %s\n' "$da" > "$decl/m_deleted.txt"
  printf '../outside.md 1 %s\n' "$da" > "$decl/m_unsafe.txt"
  printf '/etc/passwd 1 %s\n' "$da" > "$decl/m_absolute.txt"
  printf 'nope.md 1 %s\n' "$da" > "$decl/m_absent.txt"
  printf 'doc.md  3\n' > "$decl/m_malformed.txt"
  printf 'doc.md 3 %s\ndoc.md 3 %s\n' "$da" "$da" > "$decl/m_duplicate.txt"
  printf 'new.md 99 %s\n' "$(tail_sha "$tree/new.md" 99)" > "$decl/m_exceed.txt"
  printf 'link.md 1 %s\n' "$(tail_sha "$ROOT/secret.txt" 1)" > "$decl/m_symlink.txt"
  : > "$decl/m_empty.txt"

  while read -r name expect; do
    [ -n "$name" ] || continue
    mutants=$((mutants + 1))
    got=$(bash "$SELF" --declared "$decl/$name.txt" --base "$base" \
      --ref "$ref_del" --lane "$D" --export "$tree" 2>&1)
    rc=$?
    reason=$(printf '%s\n' "$got" | grep 'verdict=fail' \
      | sed -n 's/.*reason=\([a-z-]*\)$/\1/p' | sed -n 1p)
    if [ "$rc" -eq 1 ] && printf '%s' "$got" | grep -q "reason=$expect\$"; then
      rejected=$((rejected + 1))
      printf 'selftest detail=limb=mutant-%s rejected reason=%s\n' "$name" "$expect"
    else
      printf 'selftest detail=limb=mutant-%s NOT-REJECTED rc=%s reason=%s\n' \
        "$name" "$rc" "${reason:--}"
    fi
  done <<EOF
m_tail tail-mismatch
m_partial diff-mismatch
m_deleted diff-mismatch
m_unsafe unsafe-path
m_absolute unsafe-path
m_absent absent
m_malformed malformed-line
m_duplicate duplicate-path
m_exceed lines-exceed-file
m_symlink unsafe-path
EOF

  mutants=$((mutants + 1))
  got=$(bash "$SELF" --declared "$decl/m_empty.txt" --base "$base" --ref "$ref" \
    --lane "$D" --export "$tree" 2>&1)
  rc=$?
  if [ "$rc" -eq 1 ] && printf '%s' "$got" | grep -q 'declared=0 pass=0 fail=0 exit=1'; then
    rejected=$((rejected + 1))
    printf 'selftest detail=limb=mutant-m_empty rejected reason=declared-0\n'
  else
    printf 'selftest detail=limb=mutant-m_empty NOT-REJECTED rc=%s\n' "$rc"
  fi

  local verdict=fail
  if [ "$pos" = pass ] && [ "$rejected" -eq "$mutants" ]; then
    verdict=pass
  else
    nfail=$((nfail + 1))
  fi
  printf 'selftest case=declared-blocks positive=%s mutants=%s/%s verdict=%s\n' \
    "$pos" "$rejected" "$mutants" "$verdict"
  printf 'selftest cases=1 failures=%s\n' "$nfail"
  [ "$nfail" -eq 0 ] || exit 1
  exit 0
}

while [ $# -gt 0 ]; do
  case $1 in
    --declared) [ $# -ge 2 ] || die 'missing --declared value'; DECLARED=$2; shift 2 ;;
    --base) [ $# -ge 2 ] || die 'missing --base value'; BASE=$2; shift 2 ;;
    --ref) [ $# -ge 2 ] || die 'missing --ref value'; REF=$2; shift 2 ;;
    --lane) [ $# -ge 2 ] || die 'missing --lane value'; LANE=$2; shift 2 ;;
    --export) [ $# -ge 2 ] || die 'missing --export value'; EXPORT=$2; shift 2 ;;
    --selftest) SELFTEST=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown-argument: $1" ;;
  esac
done

if [ "$SELFTEST" -eq 1 ]; then
  selftest
fi
run_mode
