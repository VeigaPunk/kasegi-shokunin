#!/usr/bin/env bash
# round-59 C1 reviewer-class runner (wave evidence, committed). NOT part of the frozen predicate.
# Reproduces the ReviewerC1 X-series classes through the instrument. X10 (a network GET through
# capture-source.py) is reported by the seat only: it needs a local HTTP server and is not run here.
# usage: c1-xclass-run.sh <figure-audit.py> <corpus/instruments/capture-source.py> <scratch dir>
set -u
INSTR=$1
CAP=$2
S=$3
rm -rf -- "$S"
mkdir -p -- "$S"
trap 'rm -rf -- "$S"' EXIT
echo "instrument=$INSTR sha256=$(sha256sum "$INSTR" | cut -c1-16)"
echo "capture=$CAP sha256=$(sha256sum "$CAP" | cut -c1-16)"
echo "run-utc=$(date -u +%Y-%m-%dT%H:%M:%SZ) host=$(hostname)"

one() {
  id=$1
  derive=$2
  r="$S/r-$id"
  mkdir -p "$r/corpus/instruments"
  cp "$CAP" "$r/corpus/instruments/capture-source.py"
  printf '35\n' > "$r/g.txt"
  cp "$r/g.txt" "$r/g.orig"
  python3 -c 'import json,sys; json.dump({"figures":[{"id":sys.argv[1],"record":"xclass","recorded":"35","derive":sys.argv[2],"want":"35"}]}, open(sys.argv[3],"w"))' "$id" "$derive" "$r/one.json"
  ( cd "$r" && python3 "$INSTR" --ledger "$r/one.json" --root "$r" > "$r/out.txt" 2>&1; echo "$?" > "$r/rc" )
  m=$(ls "$r" | grep -c '^MARK-')
  ch=no; cmp -s "$r/g.txt" "$r/g.orig" || ch=yes
  echo "xclass=$id exit=$(cat "$r/rc") markers=$m g_changed=$ch :: $(head -1 "$r/out.txt")"
}

# X1: git show with an output flag; the derive runs in a git fixture root (commit inside scratch only)
X1R="$S/x1root"
mkdir -p "$X1R/corpus/instruments"
cp "$CAP" "$X1R/corpus/instruments/capture-source.py"
git -C "$X1R" init -q
printf '35\n' > "$X1R/g.txt"
git -C "$X1R" add g.txt
git -C "$X1R" -c user.name=fixture -c user.email=fixture@invalid commit -q -m fixture
[ "$(git -C "$X1R" rev-parse --show-toplevel)" = "$X1R" ] || { echo "fixture toplevel mismatch"; exit 3; }
( cd "$X1R" && python3 "$INSTR" --ledger "$S/one-x1.json" --root "$X1R" >/dev/null 2>&1 ) || true
python3 -c 'import json,sys; json.dump({"figures":[{"id":"X1-git-show-output","record":"xclass","recorded":"35","derive":"git show --output=MARK-X1 HEAD","want":"35"}]}, open(sys.argv[1],"w"))' "$S/one-x1.json"
( cd "$X1R" && python3 "$INSTR" --ledger "$S/one-x1.json" --root "$X1R" > "$S/x1.out" 2>&1; echo "$?" > "$S/x1.rc" )
echo "xclass=X1-git-show-output exit=$(cat "$S/x1.rc") markers=$(ls "$X1R" | grep -c '^MARK-') g_changed=n/a :: $(head -1 "$S/x1.out")"

one X5-pipe-sort-o 'cat g.txt | sort -o MARK-X5 g.txt'
one X6-sed-inplace "sed -n -i 's/35/36/' g.txt"
one X7-awk-inplace "awk -i inplace '{print \"ZZ\"}' g.txt"

# X8: '..' traversal through the python head executes a script outside the lane root
X8="$S/x8"
mkdir -p "$X8/root/corpus/instruments"
printf 'import sys\nopen("MARK-X8","w").write("x")\nprint(35)\n' > "$X8/evil.py"
printf '35\n' > "$X8/root/g.txt"
python3 -c 'import json,sys; json.dump({"figures":[{"id":"X8-python-traversal","record":"xclass","recorded":"35","derive":"python3 corpus/instruments/../../../evil.py","want":"35"}]}, open(sys.argv[1],"w"))' "$S/one-x8.json"
( cd "$X8/root" && python3 "$INSTR" --ledger "$S/one-x8.json" --root "$X8/root" > "$S/x8.out" 2>&1; echo "$?" > "$S/x8.rc" )
echo "xclass=X8-python-traversal exit=$(cat "$S/x8.rc") markers-in-root=$(ls "$X8/root" | grep -c '^MARK-X8') markers-outside=$(ls "$X8" | grep -c '^MARK-X8') :: $(head -1 "$S/x8.out")"

# X9: a committed counter that writes --out (capture-source.py admitted as any corpus/instruments/*.py)
printf 'payload\n' > "$S/x9-src.txt"
one X9-counter-writes-out "python3 corpus/instruments/capture-source.py --id X9 --url file://$S/x9-src.txt --out MARK-X9 --kind text"
