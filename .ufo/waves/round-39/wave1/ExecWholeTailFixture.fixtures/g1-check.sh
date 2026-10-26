#!/usr/bin/env bash
# g1-check.sh — reference model for the round-39 G1' check (whole-tail
# declarations), runnable against any fixture in this pack.
#
# The fixture is data: a `base/` tree (the pre-change front doors), a `head/`
# tree (the export tree the round-39 commit would ship, carrying
# `.ufo/waves/round-39/declared-blocks.txt`), and `export/` (the same head tree
# as `git archive` extracts it). This script builds a throwaway repo from
# `base/` and `head/` — one commit each — exports the head with `git archive`,
# proves the export equals the fixture's `export/` bytes, and then applies the
# G1' model to the exported bytes plus the two refs.
#
# The G1' model (r39), clause by clause:
#   1. Fence walk. CommonMark fenced-code walk over each whole front door,
#      modelling BOTH backtick (```) and tilde (~~~) fences: while closed, a
#      line matching `^ {0,3}(`{3,}|~{3,})` and an info string opens a fence
#      (for a backtick fence the info string may not contain a backtick); while
#      open, only a line of the SAME character with a run at least as long as
#      the opener, followed by blanks, closes it. The walk must end CLOSED at
#      EOF. `--fence-model backtick` reproduces the round-38 walk (backticks
#      only, longer runs and tildes not modelled) so the tilde-fence false RED
#      is reproducible.
#   2. Corrections outside fences. A line that BEGINS `Correction (round 39)`
#      counts only while the fence state is CLOSED; the same line inside an
#      open fence is counted in `corrections-inside` and does not satisfy the
#      clause. Each front door needs >= 1 outside correction.
#   3. Whole-tail declarations. Every non-comment line of
#      `.ufo/waves/round-39/declared-blocks.txt` is `<path> <lines> <sha256>`
#      and must satisfy, against the export:
#        a. `<path>` exists in the export (`pending-paths=0`);
#        b. `tail -n <lines> <path> | sha256sum` equals `<sha256>`;
#        c. `<lines>` equals the added-line count of `git diff <base> <head>
#           -- <path>` (whole tail: a declaration over a part of the appended
#           tail is RED).
#      `declared-blocks` counts declarations that satisfy (a) and (b);
#      `declared-ok` is 1 only when every line is well formed and (a)-(c) hold
#      for every line, with >= 1 declaration for each front door.
#
# Output (stdout):
#   export-sync=1|0        (checked every run; 0 is a fixture defect)
#   G1 payload=province-correction=<n>,readme-correction=<n>,province-fence=<closed|open>,readme-fence=<closed|open>,declared-blocks=<n>,declared-ok=<0|1>,pending-paths=<n>,tail=PROVINCE.md:<declared>:<added>,corpus/README.md:<declared>:<added>,fence-model=<backtick+tilde|backtick>,corrections-inside=<n> closed=<0|1>
# Exit 0 only when `closed=1`.
#
# Usage: bash g1-check.sh --fixture DIR [--work DIR] [--fence-model backtick+tilde|backtick]
#        bash g1-check.sh --walk FILE [--fence-model backtick+tilde|backtick]
#          Unit probe for the fence walk alone: prints
#          `fence-model=<m> state=<closed|open> outside=<n> inside=<n>`, exit 0
#          only when the walk ends closed. Touches no fixture and no work dir.
#
# Writes only under --work (default: a mktemp dir under TMPDIR); nothing is
# written to the fixture. The fixture's `export/` must exist.
set -u

die() { printf 'g1-check: %s\n' "$*" >&2; exit 2; }

# walk FILE — prints `<closed|open> <outside-corrections> <inside-corrections>`
# for the fence model in $MODEL.
walk() { # FILE
  awk -v model="$MODEL" '
    { line = $0; sp = 0
      while (sp < 3 && substr(line, sp + 1, 1) == " ") sp++
      t = substr(line, sp + 1)
      was_open = open
      if (index($0, "Correction (round 39)") == 1) {
        if (was_open) inside++; else outside++
      }
      if (!open) {
        c = ""
        if (substr(t, 1, 3) == "```") c = "`"
        else if (substr(t, 1, 3) == "~~~") c = "~"
        if (c != "" && !(c == "~" && model == "backtick")) {
          n = 0
          while (substr(t, n + 1, 1) == c) n++
          info = substr(t, n + 1)
          ok = 1
          if (c == "`" && index(info, "`") > 0) ok = 0
          if (ok) { open = 1; oc = c; olen = n }
        }
      } else {
        n = 0
        while (substr(t, n + 1, 1) == oc) n++
        if (n >= olen) {
          rest = substr(t, n + 1)
          gsub(/[ \t]/, "", rest)
          if (rest == "") { open = 0; oc = ""; olen = 0 }
        }
      }
    }
    END { printf "%s %d %d\n", (open ? "open" : "closed"), outside, inside }
  ' "$1"
}

FIXTURE= WORK= WALKFILE= MODEL='backtick+tilde'
while [ $# -gt 0 ]; do
  case $1 in
    --walk) WALKFILE=${2:-}; shift 2 ;;
    --walk=*) WALKFILE=${1#--walk=}; shift ;;
    --fixture) FIXTURE=${2:-}; shift 2 ;;
    --fixture=*) FIXTURE=${1#--fixture=}; shift ;;
    --work) WORK=${2:-}; shift 2 ;;
    --work=*) WORK=${1#--work=}; shift ;;
    --fence-model) MODEL=${2:-}; shift 2 ;;
    --fence-model=*) MODEL=${1#--fence-model=}; shift ;;
    -h|--help) sed -n '2,/^set -u$/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done
case $MODEL in backtick+tilde|backtick) ;; *) die "bad --fence-model: $MODEL" ;; esac
if [ -n "$WALKFILE" ]; then
  [ -f "$WALKFILE" ] || die "not a file: $WALKFILE"
  wout=$(walk "$WALKFILE"); read -r wst woutn wins <<<"$wout"
  printf 'fence-model=%s state=%s outside=%s inside=%s\n' "$MODEL" "$wst" "$woutn" "$wins"
  [ "$wst" = closed ]
  exit
fi
[ -n "$FIXTURE" ] || die 'missing --fixture'
[ -d "$FIXTURE" ] || die "fixture not a directory: $FIXTURE"
FIXTURE=$(cd "$FIXTURE" && pwd -P)
[ -d "$FIXTURE/base" ] || die "fixture lacks base/: $FIXTURE"
[ -d "$FIXTURE/head" ] || die "fixture lacks head/: $FIXTURE"
[ -d "$FIXTURE/export" ] || die "fixture lacks export/: $FIXTURE"

OWED=0
if [ -z "$WORK" ]; then
  WORK=$(mktemp -d "${TMPDIR:-/tmp}/g1-check.XXXXXX") || die 'mktemp failed'
  OWED=1
else
  mkdir -p -- "$WORK" || die "cannot create work dir: $WORK"
fi
WORK=$(cd "$WORK" && pwd -P) || die "cannot resolve work dir: $WORK"
trap '[ "$OWED" -eq 1 ] && rm -rf -- "$WORK"' EXIT

REPO=$WORK/repo EXPORT=$WORK/export
rm -rf -- "$REPO" "$EXPORT"
mkdir -p -- "$REPO" "$EXPORT" || die 'cannot create work subdirs'

export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME=g1fixture GIT_AUTHOR_EMAIL=g1fixture@invalid \
       GIT_COMMITTER_NAME=g1fixture GIT_COMMITTER_EMAIL=g1fixture@invalid \
       GIT_AUTHOR_DATE='2026-10-26T00:00:00Z' GIT_COMMITTER_DATE='2026-10-26T00:00:00Z'

git -c init.defaultBranch=main -C "$REPO" init -q || die 'git init failed'
TOP=$(git -C "$REPO" rev-parse --show-toplevel 2>/dev/null) || die 'not a git repo'
[ "$TOP" = "$REPO" ] || die "repo top-level $TOP != $REPO"

seed_and_commit() { # SRCDIR MESSAGE
  local src=$1 msg=$2
  find "$REPO" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf -- {} + || die 'clean failed'
  cp -a -- "$src"/. "$REPO"/ || die "copy failed: $src"
  git -C "$REPO" add -A || die 'git add failed'
  git -C "$REPO" -c commit.gpgsign=false commit -q -m "$msg" || die 'git commit failed'
  git -C "$REPO" rev-parse HEAD
}

BASE=$(seed_and_commit "$FIXTURE/base" 'fixture base') || die 'base commit'
HEADREF=$(seed_and_commit "$FIXTURE/head" 'fixture head') || die 'head commit'

git -C "$REPO" archive --format=tar "$HEADREF" | tar -xf - -C "$EXPORT" \
  || die 'git archive export failed'

SYNC=0
if diff -r --no-dereference "$FIXTURE/export" "$EXPORT" >/dev/null 2>&1; then
  SYNC=1
fi
printf 'export-sync=%s\n' "$SYNC"

P_STATE=open R_STATE=open PCOR=0 RCOR=0 PINS=0 RINS=0 wout=''
if [ -f "$EXPORT/PROVINCE.md" ]; then
  wout=$(walk "$EXPORT/PROVINCE.md"); read -r P_STATE PCOR PINS <<<"$wout"
fi
if [ -f "$EXPORT/corpus/README.md" ]; then
  wout=$(walk "$EXPORT/corpus/README.md"); read -r R_STATE RCOR RINS <<<"$wout"
fi

added_lines() { # PATH
  local n
  n=$(git -C "$REPO" diff --numstat "$BASE" "$HEADREF" -- "$1" 2>/dev/null | awk '{print $1; exit}')
  case ${n:-} in ''|*[!0-9]*) n=0 ;; esac
  printf '%s' "$n"
}
P_ADDED=$(added_lines PROVINCE.md)
R_ADDED=$(added_lines corpus/README.md)

DECL=$EXPORT/.ufo/waves/round-39/declared-blocks.txt
VALID=0 BAD=0 PENDING=0 HAVE_P=0 HAVE_R=0 P_DECL=0 R_DECL=0
if [ -f "$DECL" ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    case $line in ''|'#'*) continue ;; esac
    set -f
    set -- $line
    set +f
    path=${1:-} lines=${2:-} sha=${3:-} extra=${4:-}
    if [ -z "$path" ] || [ -z "$lines" ] || [ -z "$sha" ] || [ -n "$extra" ]; then
      BAD=1; continue
    fi
    case $lines in ''|*[!0-9]*) BAD=1; continue ;; esac
    [ "$lines" -ge 1 ] || { BAD=1; continue; }
    case $sha in ''|*[!0-9a-f]*) BAD=1; continue ;; esac
    [ "${#sha}" -eq 64 ] || { BAD=1; continue; }
    if [ ! -e "$EXPORT/$path" ]; then
      PENDING=$((PENDING + 1)); BAD=1; continue
    fi
    got=$(tail -n "$lines" -- "$EXPORT/$path" | sha256sum | awk '{print $1; exit}')
    if [ "$got" != "$sha" ]; then BAD=1; continue; fi
    VALID=$((VALID + 1))
    case $path in
      PROVINCE.md) HAVE_P=1; P_DECL=$lines ;;
      corpus/README.md) HAVE_R=1; R_DECL=$lines ;;
    esac
    add=$(added_lines "$path")
    [ "$lines" -eq "$add" ] || BAD=1
  done < "$DECL"
fi

DOK=0
if [ -f "$DECL" ] && [ "$BAD" -eq 0 ] && [ "$PENDING" -eq 0 ] \
   && [ "$HAVE_P" -eq 1 ] && [ "$HAVE_R" -eq 1 ] && [ "$VALID" -ge 2 ]; then
  DOK=1
fi

CLOSED=0
if [ "$PCOR" -ge 1 ] && [ "$RCOR" -ge 1 ] && [ "$P_STATE" = closed ] \
   && [ "$R_STATE" = closed ] && [ "$DOK" -eq 1 ] && [ "$PENDING" -eq 0 ] \
   && [ "$VALID" -ge 2 ] && [ "$SYNC" -eq 1 ]; then
  CLOSED=1
fi

printf 'G1 payload=province-correction=%s,readme-correction=%s,province-fence=%s,readme-fence=%s,declared-blocks=%s,declared-ok=%s,pending-paths=%s,tail=PROVINCE.md:%s:%s,corpus/README.md:%s:%s,fence-model=%s,corrections-inside=%s closed=%s\n' \
  "$PCOR" "$RCOR" "$P_STATE" "$R_STATE" "$VALID" "$DOK" "$PENDING" \
  "$P_DECL" "$P_ADDED" "$R_DECL" "$R_ADDED" "$MODEL" "$((PINS + RINS))" "$CLOSED"
[ "$CLOSED" -eq 1 ]
