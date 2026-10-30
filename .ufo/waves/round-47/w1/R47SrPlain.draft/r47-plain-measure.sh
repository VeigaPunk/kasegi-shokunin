#!/usr/bin/env bash
# r47-plain-measure.sh [TREE] [--work DIR] -- PLAIN round-47 measurement beside the
# frozen counters (r47-routed-defects.py, r47-f30-gate.py), modeled on
# corpus/instruments/r46-plain-measure.sh. The count measures are grep/wc/find/bash
# only, copied verbatim from claims.json C1.plain / C2.plain. The two invocation
# measures run the frozen commands as written: the capture-binding
# (corpus/instruments/source-recheck.py, an existing instrument, not a counter we
# implement) and the fleet census (sources-census.sh validate).
#
# Usage: r47-plain-measure.sh [TREE] [--work DIR]
#   TREE       lane tree to measure (default .); every command reads only its bytes
#   --work DIR scratch dir (default: fresh mktemp -d under ${TMPDIR:-/tmp}, removed
#              on exit; an explicit --work dir is kept and only we write into it)
#
# Prints exactly 13 labelled lines on stdout, in claims.json order:
#   c1a=<n>  grep -c 'to append' corpus/SOURCES.md                              (base 2, target 0)
#   c1b=<n>  grep -c '```' corpus/SOURCES.md                                    (base 4, target 0)
#   c1c=<n>  grep -c 'all 42 lines are body prose'
#            corpus/knowledge/github-repository-security-advisories.md          (base 1, target 0)
#   c1d=<n>  grep -c 'three cases'
#            corpus/knowledge/github-repository-security-advisories.md          (base 2; contextual only,
#            the corrected text keeps 'three cases that follow, only two'; not the kill rule)
#   c1e=<n>  grep -c 'S074.txt:'
#            corpus/knowledge/github-repository-security-advisories.md          (base 54, target 0)
#   c1f=<n>  grep -c 'supersedes S074' corpus/SOURCES.md                        (base 0, target 1)
#   c1g=<n>  grep -c 'docs.github.com/en/rest/security-advisories' corpus/SOURCES.md  (base 0, target 1)
#   c1h=<n>  capture-binding exit: python3 corpus/instruments/source-recheck.py
#            --manifest corpus/source-snapshots/round-47/manifest.json --source S076
#                                                                               (base 2 = no manifest,
#                                                                                target 0)
#   c2a=<n>  grep -cE '^\| F[0-9]+ \|' corpus/README.md                         (base 29, target 30)
#   c2b=<n>  grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md  (base 74, round end 76)
#   c2c=<n>  find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l             (base 66, target 67)
#   c2d=<n>  grep -rliE 'zero day initiative|zerodayinitiative'
#            corpus/knowledge corpus/SOURCES.md corpus/README.md | wc -l        (base 0, target >= 3)
#   c2e=<n>  census exit: bash <sources-census.sh> validate TREE                (base 0 with W04
#            warnings, target 0)
# Everything else (missing-target errors, capture-binding output, census TSV) goes to
# stderr; stdout stays exactly 13 lines so the output is greppable like r46's.
#
# Fail closed: if any measured target file is missing under TREE, print nothing on
# stdout, explain on stderr, exit 3. The fail-closed set is the files the count
# measures read plus the two invoked instruments. The round-47 manifest is NOT
# fail-closed: its absence is itself the measured base state of c1h (claims:
# "base fails (no manifest), target exit 0"); source-recheck.py reports it as exit 2.
#
# Committed bytes: the script only reads paths under TREE and never writes there;
# measuring a clean checkout therefore reads committed bytes only (verified below
# against git-archive exports of the base and freeze commits).
#
# Exit: 0 measured (counts may say anything; they are measurements, not verdicts)
#       2 usage/environment error
#       3 missing target file (fail closed)
set -u
export PYTHONDONTWRITEBYTECODE=1

usage() {
  sed -n '3,10p' "$0" >&2
  exit 2
}

T=.
WORK_ARG=""
while [ $# -gt 0 ]; do
  case "$1" in
    --work)
      [ $# -ge 2 ] || { echo "ERROR: --work needs a path" >&2; exit 2; }
      WORK_ARG=$2; shift 2 ;;
    -h|--help) usage ;;
    --) shift; break ;;
    --*) echo "ERROR: unknown option: $1" >&2; exit 2 ;;
    *)  T=$1; shift ;;
  esac
done
[ $# -eq 0 ] || { echo "ERROR: unexpected extra argument: $1" >&2; exit 2; }

if [ -n "$WORK_ARG" ]; then
  mkdir -p -- "$WORK_ARG" || { echo "ERROR: cannot create --work dir: $WORK_ARG" >&2; exit 2; }
  WORK=$(cd -- "$WORK_ARG" && pwd -P) || exit 2
else
  WORK=$(mktemp -d "${TMPDIR:-/tmp}/r47-plain.XXXXXX") || exit 2
  trap 'rm -rf -- "$WORK"' EXIT
fi

# --- fail-closed preflight (exit 3 before any stdout) -------------------------
T=$(cd -- "$T" && pwd -P) || { echo "ERROR: cannot enter tree" >&2; exit 2; }
need_file() { [ -f "$1" ] || { echo "ERROR: missing target file: $1" >&2; exit 3; }; }
need_dir()  { [ -d "$1" ] || { echo "ERROR: missing target dir: $1" >&2; exit 3; }; }

need_dir  "$T/corpus/knowledge"
need_file "$T/corpus/SOURCES.md"
need_file "$T/corpus/README.md"
need_file "$T/corpus/knowledge/github-repository-security-advisories.md"
need_file "$T/corpus/instruments/source-recheck.py"

CENSUS=${KASEGI_SOURCES_CENSUS:-}
if [ -z "$CENSUS" ]; then
  for cand in "$T/../scripts/sources-census.sh" \
              /home/vgpnk/Projects/shokunin/scripts/sources-census.sh; do
    if [ -f "$cand" ]; then CENSUS=$cand; break; fi
  done
fi
[ -n "$CENSUS" ] && [ -f "$CENSUS" ] || {
  echo "ERROR: sources-census.sh not found (tried \$KASEGI_SOURCES_CENSUS, TREE/../scripts/, fleet path)" >&2
  exit 3
}

# --- C1 plain measures (claims.json C1.plain, in order) -----------------------
ENTRY="$T/corpus/knowledge/github-repository-security-advisories.md"

c1a=$(grep -c 'to append' "$T/corpus/SOURCES.md")
c1b=$(grep -c '```' "$T/corpus/SOURCES.md")
c1c=$(grep -c 'all 42 lines are body prose' "$ENTRY")
c1d=$(grep -c 'three cases' "$ENTRY")
c1e=$(grep -c 'S074.txt:' "$ENTRY")
c1f=$(grep -c 'supersedes S074' "$T/corpus/SOURCES.md")
c1g=$(grep -c 'docs.github.com/en/rest/security-advisories' "$T/corpus/SOURCES.md")

# capture-binding: exact frozen command, relative paths under TREE, output to scratch
( cd "$T" && python3 corpus/instruments/source-recheck.py \
    --manifest corpus/source-snapshots/round-47/manifest.json --source S076 ) \
  >"$WORK/recheck-s076.txt" 2>"$WORK/recheck-s076.err"
c1h=$?
sed 's/^/recheck: /' "$WORK/recheck-s076.txt" "$WORK/recheck-s076.err" >&2

# --- C2 plain measures (claims.json C2.plain, in order) -----------------------
c2a=$(grep -cE '^\| F[0-9]+ \|' "$T/corpus/README.md")
c2b=$(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$T/corpus/SOURCES.md")
c2c=$( cd "$T" && find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l )
c2d=$(grep -rliE 'zero day initiative|zerodayinitiative' \
        "$T/corpus/knowledge" "$T/corpus/SOURCES.md" "$T/corpus/README.md" | wc -l)

# census: the tree is passed as an explicit lane dir (resolve_targets accepts any
# directory; lane name = basename), so the census reads the same committed TREE bytes
# as every other line. Findings TSV is mirrored to stderr for the record.
bash "$CENSUS" validate "$T" >"$WORK/census.tsv" 2>"$WORK/census.err"
c2e=$?
sed 's/^/census: /' "$WORK/census.tsv" "$WORK/census.err" >&2

printf 'c1a=%s\nc1b=%s\nc1c=%s\nc1d=%s\nc1e=%s\nc1f=%s\nc1g=%s\nc1h=%s\nc2a=%s\nc2b=%s\nc2c=%s\nc2d=%s\nc2e=%s\n' \
  "$c1a" "$c1b" "$c1c" "$c1d" "$c1e" "$c1f" "$c1g" "$c1h" "$c2a" "$c2b" "$c2c" "$c2d" "$c2e"
