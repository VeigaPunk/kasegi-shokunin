#!/usr/bin/env bash
# ExecNoHarm.sh — append-only ("no harm") checker for the round-38 protected lane files.
#
# The lane's front-door and corpus files are append-only surfaces: a round may add
# lines, it may never rewrite or delete one that already exists. This checker proves
# that promise over a commit range with two independent limbs per file.
#
#   Usage:
#     ExecNoHarm.sh [--repo DIR] <base> <ref>
#     ExecNoHarm.sh -h | --help
#
#   <base>, <ref>   revisions (any `git rev-parse` expression); resolved to commits.
#   --repo DIR      git worktree holding the protected files (default: the worktree
#                   this script lives in, else the worktree of the current directory).
#
# Protected files (fixed list, in this order):
#   SKILL.md, PROVINCE.md, SCORECARD.md, LOG.md, SHONEN.md,
#   corpus/QUALITY.md, corpus/SOURCES.md, corpus/README.md,
#   corpus/knowledge/considerthese-proposals-ledger.md, corpus/lessons/round-37.md
#
# Limb 1 — line budget. Runs
#     git diff --numstat <base> <ref> -- <paths>
# and requires every protected path to report deletions = 0 (`N	0	<path>`).
# git omits unchanged paths from numstat; those are reported as `0	0	<path>`.
# A deletion count of `-` (binary content) is a failure: a binary change cannot be
# shown to be append-only. An unexpected numstat path (a rename/copy, `old => new`)
# is a failure too, because the protected name would then not describe the bytes.
#
# Limb 2 — byte prefix. For each protected path the bytes at <base> must be a byte
# prefix of the bytes at <ref>:
#     git show <ref>:<path> | head -n $(git show <base>:<path> | wc -l) | cmp - <(git show <base>:<path>)
# Both blobs are materialized under a private temp dir first (no SIGPIPE, no
# process-substitution timing), so the comparison is the byte-for-byte one the
# command above names. A <base> blob without a trailing newline is compared as a
# <base-bytes> byte prefix instead, because `head -n` would otherwise invent the
# missing newline; for newline-terminated base blobs the two forms are identical.
#
# Exit: 0 all protected files append-only (deletions=0, every prefix identical)
#       1 harm detected: any deletion, binary change, unexpected numstat path,
#         protected file absent at <ref>, or prefix mismatch
#       2 could not evaluate: bad usage, bad revision, protected file absent at
#         <base>, repository unreadable, or temp dir unavailable
#
# Read-only: the only git subcommands are rev-parse, cat-file and diff; writes are
# confined to a mktemp dir that is removed on exit.

set -u -o pipefail

readonly FILES=(
  SKILL.md
  PROVINCE.md
  SCORECARD.md
  LOG.md
  SHONEN.md
  corpus/QUALITY.md
  corpus/SOURCES.md
  corpus/README.md
  corpus/knowledge/considerthese-proposals-ledger.md
  corpus/lessons/round-37.md
)

usage() {
  awk 'NR > 1 { if ($0 !~ /^#/) exit; sub(/^# ?/, ""); print }' "${BASH_SOURCE[0]}"
}

could_not_evaluate() {
  printf 'no-harm: cannot evaluate: %s\n' "$*" >&2
  exit 2
}

repo=""
positional=()
while [ "$#" -gt 0 ]; do
  case $1 in
    -h|--help) usage; exit 0 ;;
    --repo) [ "$#" -ge 2 ] || could_not_evaluate "--repo needs a directory"; repo=$2; shift 2 ;;
    --repo=*) repo=${1#--repo=}; shift ;;
    --) shift; positional+=("$@"); break ;;
    -*) could_not_evaluate "unknown option: $1" ;;
    *) positional+=("$1"); shift ;;
  esac
done

[ "${#positional[@]}" -eq 2 ] || could_not_evaluate "usage: ExecNoHarm.sh [--repo DIR] <base> <ref>"
base_arg=${positional[0]}
ref_arg=${positional[1]}

# ---- repository -------------------------------------------------------------
if [ -z "$repo" ]; then
  repo=$(git -C "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" rev-parse --show-toplevel 2>/dev/null) \
    || repo=$(git -C "$(pwd)" rev-parse --show-toplevel 2>/dev/null) \
    || could_not_evaluate "not inside a git worktree; pass --repo DIR"
fi
[ -d "$repo" ] || could_not_evaluate "--repo is not a directory: $repo"
repo=$(cd "$repo" && pwd) || could_not_evaluate "--repo cannot be entered: $repo"
top=$(git -C "$repo" rev-parse --show-toplevel 2>/dev/null) \
  || could_not_evaluate "not a git worktree: $repo"
[ "$top" = "$repo" ] || could_not_evaluate "--repo is a subdirectory of the worktree $top; pass the worktree root"

# ---- revisions --------------------------------------------------------------
base=$(git -C "$repo" rev-parse --verify --quiet "${base_arg}^{commit}" 2>/dev/null) \
  || could_not_evaluate "base revision does not resolve to a commit: $base_arg"
ref=$(git -C "$repo" rev-parse --verify --quiet "${ref_arg}^{commit}" 2>/dev/null) \
  || could_not_evaluate "ref revision does not resolve to a commit: $ref_arg"

# ---- temp dir and base-blob preflight --------------------------------------
tmpd=$(mktemp -d "${TMPDIR:-/tmp}/no-harm.XXXXXX") || could_not_evaluate "mktemp failed under ${TMPDIR:-/tmp}"
trap 'rm -rf -- "$tmpd"' EXIT

i=0
for f in "${FILES[@]}"; do
  i=$((i + 1))
  git -C "$repo" cat-file blob "$base:$f" >"$tmpd/base.$i" 2>/dev/null \
    || could_not_evaluate "protected path absent at base $base: $f"
done

printf 'no-harm v1\n'
printf 'repo=%s\n' "$repo"
printf 'base=%s\n' "$base"
printf 'ref=%s\n' "$ref"

# ---- limb 1: numstat --------------------------------------------------------
printf -- '-- limb 1: git diff --numstat %s %s -- <protected paths> --\n' "$base" "$ref"
raw=$(git -C "$repo" diff --numstat "$base" "$ref" -- "${FILES[@]}") \
  || could_not_evaluate "git diff --numstat failed"

declare -A adds_of=() dels_of=()
unexpected=()
while IFS=$'\t' read -r add del path; do
  [ -n "$path" ] || continue
  known=0
  for f in "${FILES[@]}"; do
    [ "$f" = "$path" ] && { known=1; break; }
  done
  if [ "$known" -eq 0 ]; then
    unexpected+=("$path")
  else
    adds_of[$path]=$add
    dels_of[$path]=$del
  fi
done <<<"$raw"

if [ -z "$raw" ]; then
  printf '(no numstat lines: all protected files byte-identical)\n'
else
  printf '%s\n' "$raw"
fi

harm=0
harm_lines=()
deletions=0
numstat_bad=0

printf -- '-- normalized numstat: adds<TAB>deletes<TAB>path (unchanged shown as 0/0) --\n'
for f in "${FILES[@]}"; do
  add=${adds_of[$f]:-0}
  del=${dels_of[$f]:-0}
  printf '%s\t%s\t%s\n' "$add" "$del" "$f"
  if [ "$del" = "-" ] || [ "$add" = "-" ]; then
    harm=1; numstat_bad=$((numstat_bad + 1))
    harm_lines+=("deletions=unmeasurable-binary path=$f")
  elif [ "$del" != "0" ]; then
    harm=1; numstat_bad=$((numstat_bad + 1)); deletions=$((deletions + del))
    harm_lines+=("deletions=$del path=$f")
  fi
done
for p in ${unexpected[@]+"${unexpected[@]}"}; do
  harm=1; numstat_bad=$((numstat_bad + 1))
  harm_lines+=("unexpected-numstat-path=$p")
done
printf 'numstat files=%s deletions=%s violations=%s\n' "${#FILES[@]}" "$deletions" "$numstat_bad"

# ---- limb 2: byte prefix ----------------------------------------------------
printf -- '-- limb 2: bytes at <base> must prefix bytes at <ref> --\n'

prefix_files=0
prefix_mismatch=0
i=0
for f in "${FILES[@]}"; do
  i=$((i + 1))
  basef="$tmpd/base.$i"
  reff="$tmpd/ref.$i"
  prefix_files=$((prefix_files + 1))

  if ! git -C "$repo" cat-file blob "$ref:$f" >"$reff" 2>/dev/null; then
    printf '%-52s prefix=ABSENT-AT-REF (deleted)\n' "$f"
    harm=1; prefix_mismatch=$((prefix_mismatch + 1))
    harm_lines+=("absent-at-ref path=$f")
    continue
  fi

  bl=$(wc -l <"$basef")
  bb=$(wc -c <"$basef")
  rl=$(wc -l <"$reff")

  lastbyte=""
  if [ "$bb" -gt 0 ]; then
    lastbyte=$(tail -c 1 -- "$basef" | od -An -tx1 | tr -d ' \n')
  fi

  ok=1
  if [ "$rl" -lt "$bl" ]; then
    ok=0
  elif [ "$lastbyte" = "0a" ]; then
    head -n "$bl" -- "$reff" | cmp -s - "$basef" || ok=0
  else
    head -c "$bb" -- "$reff" | cmp -s - "$basef" || ok=0
  fi

  if [ "$ok" -eq 1 ]; then
    printf '%-52s base-lines=%-6s ref-lines=%-6s prefix=identical\n' "$f" "$bl" "$rl"
  else
    printf '%-52s base-lines=%-6s ref-lines=%-6s prefix=MISMATCH\n' "$f" "$bl" "$rl"
    harm=1; prefix_mismatch=$((prefix_mismatch + 1))
    harm_lines+=("prefix-mismatch path=$f")
  fi
done
printf 'prefix files=%s mismatched=%s\n' "$prefix_files" "$prefix_mismatch"

if [ "$harm" -eq 0 ]; then
  printf 'no-harm: OK\n'
  exit 0
fi
for h in ${harm_lines[@]+"${harm_lines[@]}"}; do
  printf 'HARM %s\n' "$h"
done
printf 'no-harm: HARM\n'
exit 1
