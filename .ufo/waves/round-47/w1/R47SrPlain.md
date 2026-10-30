# R47SrPlain — plain-measure draft

Axes: depth:verifiability (C1), coverage (C2).

## Behavior and touched surfaces

Draft for the L1 to land as corpus/instruments/r47-plain-measure.sh, modeled on corpus/instruments/r46-plain-measure.sh. Only this report and R47SrPlain.draft/ were retained; no product edits or git mutations. Counts use Bash/grep/find/wc; no r47 Python counter is invoked. The explicitly requested source-recheck.py capture binding remains a Python invocation. The script reports 13 labelled lines, defaults TREE to '.', and routes invocation output into scratch and diagnostics to stderr. Census validates the explicit TREE directory rather than silently inspecting the live lane.

## Evidence and do-nothing control

Read claims.json C1.plain and C2.plain. Export commands (read-only):

- git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8 | tar -x -C /fast/scratch/hyaku/kasegi-r47/R47SrPlain/base/kasegi-shokunin
- git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 308a2cb2dc7bdce233461cc1ac49dd88e51c6193 | tar -x -C /fast/scratch/hyaku/kasegi-r47/R47SrPlain/freeze/kasegi-shokunin

Ran bash /fast/scratch/hyaku/kasegi-r47/R47SrPlain/r47-plain-measure.sh TREE --work SCRATCH/out/wk-{base,freeze}. Both exited 0 and printed exactly 13 lines. Untouched base export is the do-nothing control, reproducing all frozen plain base readings rather than target readings:

~~~text
c1a=2
c1b=4
c1c=1
c1d=2
c1e=54
c1f=0
c1g=0
c1h=2
c2a=29
c2b=74
c2c=66
c2d=0
c2e=0
~~~

Freeze export:

~~~text
c1a=2
c1b=4
c1c=1
c1d=2
c1e=54
c1f=0
c1g=0
c1h=0
c2a=29
c2b=74
c2c=66
c2d=0
c2e=0
~~~

Freeze S076 recheck printed sha256 OK and Q1–Q12 OK (anchors 568–600). Base printed 'manifest UNAVAILABLE reason=missing', exit 2, reflected in c1h. A capture-binding success alone therefore does not establish C1 closure.

Missing-tree and default-tree probes both exited 3, printed zero stdout lines, and named missing corpus/knowledge on stderr. Default-tree probe ran without a TREE argument from an empty scratch directory.

Census equivalence probe used a scratch fleet config mapping kasegi to the frozen export. bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root SCRATCH/fleet kasegi and the script's explicit-dir form both exited 0 with the same three W04 findings (S028, S029, S072) plus ok; only lane-name prefixes differed.

A marker-based post-run find TREE -newer SCRATCH/marker -print returned no paths; find TREE -name __pycache__ -print returned none. An earlier mtime probe was confounded by extraction/copy timestamps and is not mutation evidence.

Disk guard status observed /fast/scratch/hyaku free=377.8G, /tmp free=95.5G. Its initial combined call timed out after 60 seconds before exports; exports were then run separately. The tool automatically backgrounded that initial call despite the leaf prohibition; no background operation was intentionally requested. No tools installed.

## Gates, findings, and limits

- Draft is not landed; L1 owns integration and executable mode.
- Measurements are not semantic verdicts. c1d ('three cases') is contextual only. Raw policy-name grep is not proof of novelty or policy-bearing content.
- Known disclosed mutation survivors remain C1=16 and C2=18; no full battery run or claim that these gaps are closed.
- Important contract limitation: this draft reads TREE filesystem bytes, not Git objects. Committed-byte evidence above holds because those trees were git-archive exports. A dirty checkout, symlink targets, supplied census instrument, or writable TREE overlapping --work are NOT guarded. Thus unconditional committed-bytes/scratch isolation is not established. Missing manifest is deliberately recorded as c1h=2 rather than fatal, to reproduce the frozen base; strict 'any target missing' wording conflicts with that behavior. These are limitations for the canonical judge, not silently upgraded passes.
- The final edit mirrors capture-binding stdout as well as stderr; prior count receipts precede that diagnostic-only edit. It was not rerun afterward.
- No integrated-tree target receipt, live-page review, counter mutation coverage, commit, push, or publication.

## Draft script

Extract the following block (or use R47SrPlain.draft/r47-plain-measure.sh):

~~~~bash
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
~~~~

## Artifact paths

- .ufo/waves/round-47/w1/R47SrPlain.md
- .ufo/waves/round-47/w1/R47SrPlain.draft/r47-plain-measure.sh
- .ufo/waves/round-47/w1/R47SrPlain.draft/{base.stdout,base.stderr,freeze.stdout,freeze.stderr,missing.stderr,default.stderr,census-conf.stdout,fleet.stderr}

Report: .ufo/waves/round-47/w1/R47SrPlain.md
