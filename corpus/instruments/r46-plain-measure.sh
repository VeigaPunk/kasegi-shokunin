#!/usr/bin/env bash
# plain-measure.sh <tree> -- second, PLAIN measurement beside the round-46 counters.
# grep/wc/awk/sed/bash only over the committed bytes of <tree>; no python, no counter.
# Prints exactly six lines, nothing else:
#   c1a=<n>  lines `recheck:` ... `test -d ~/Projects/` in corpus/knowledge/*.md (one line per file at most)
#   c1b=<n>  gated count: first `^recheck:` line per entry, a leading `cd <path> &&` stripped,
#            run with cwd=<tree> under `bash -c` (timeout 120); non-zero exits that `bash -n` accepts
#   c2a=<n>  frontier rows in corpus/README.md
#   c2b=<n>  SOURCES rows in corpus/SOURCES.md
#   c2c=<n>  corpus/knowledge/*.md files
#   c2d=<n>  files naming private vulnerability reporting (absence sweep)
# Read-only on <tree> as far as the recheck commands are: bytecode writing is disabled.
set -u
[ $# -eq 1 ] && [ -d "$1" ] || { echo "usage: plain-measure.sh <tree>" >&2; exit 2; }
T=$(cd "$1" && pwd -P) || exit 2
export PYTHONDONTWRITEBYTECODE=1

c1a=$(grep -lE '^recheck:.*test -d ~/Projects/' "$T"/corpus/knowledge/*.md | wc -l)

c1b=0
for f in "$T"/corpus/knowledge/*.md; do
  line=$(grep -m1 '^recheck:' "$f") || continue
  cmd=${line#recheck:}
  cmd=$(printf '%s' "$cmd" | sed -E 's/^[[:space:]]+//; s/^cd[[:space:]]+[^&;]+[[:space:]]*&&[[:space:]]*//')
  bash -n -c "$cmd" >/dev/null 2>&1 || continue
  ( cd "$T" && timeout 120 bash -c "$cmd" >/dev/null 2>&1 </dev/null )
  [ $? -ne 0 ] && c1b=$((c1b + 1))
done

c2a=$(grep -cE '^\| F[0-9]+ \|' "$T"/corpus/README.md)
c2b=$(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$T"/corpus/SOURCES.md)
c2c=$(ls "$T"/corpus/knowledge/*.md | wc -l)
c2d=$(grep -rliE 'private vulnerability reporting|privately report' "$T"/corpus/knowledge "$T"/corpus/SOURCES.md "$T"/corpus/README.md | wc -l)

printf 'c1a=%s\nc1b=%s\nc2a=%s\nc2b=%s\nc2c=%s\nc2d=%s\n' "$c1a" "$c1b" "$c2a" "$c2b" "$c2c" "$c2d"
