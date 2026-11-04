#!/usr/bin/env bash
# round-60 C1 escape-and-in-program probe runner (wave evidence, committed).
# usage: c1-probe-run-r60.sh <figure-audit.py path> <scratch dir>
# Runs each probe derive ALONE through the instrument, in its own fresh root holding g.txt ("35").
# A probe counts as EXECUTED when its marker file MARK-* appears in its root; REFUSED when the
# instrument exits 2 before running the derive. The instrument path is resolved absolute before
# any `cd` (R77: the counted command runs literally from the lane root). Scratch is removed on exit.
set -u
INSTR=$(realpath "$1")
S=$(realpath -m "$2")
rm -rf -- "$S"
mkdir -p -- "$S"
trap 'rm -rf -- "$S"' EXIT
echo "instrument=$INSTR sha256=$(sha256sum "$INSTR" | cut -c1-16)"
echo "run-utc=$(date -u +%Y-%m-%dT%H:%M:%SZ) host=$(hostname)"

run() {
  id=$1
  want=$2
  derive=$3
  r="$S/r-$id"
  mkdir -p "$r"
  printf '35\n' > "$r/g.txt"
  python3 -c 'import json,sys; json.dump({"figures":[{"id":sys.argv[1],"record":"probe","recorded":sys.argv[2],"derive":sys.argv[3],"want":sys.argv[2]}]}, open(sys.argv[4],"w"))' "$id" "$want" "$derive" "$r/one.json"
  ( cd "$r" && python3 "$INSTR" --ledger "$r/one.json" --root "$r" > "$r/out.txt" 2>&1; echo "$?" > "$r/rc" )
  m=$(ls "$r" | grep -c '^MARK-')
  echo "probe=$id derive=$(printf '%s' "$derive" | tr '\n' '|') exit=$(cat "$r/rc") markers=$m :: $(head -1 "$r/out.txt")"
}

# same, but the derive runs inside a throwaway git fixture repo (git show's --output class needs a repo)
runinrepo() {
  id=$1
  want=$2
  derive=$3
  r="$S/r-$id"
  mkdir -p "$r/repo"
  printf '35\n' > "$r/g.txt"
  git -C "$r/repo" init -q
  git -C "$r/repo" -c user.email=t@t -c user.name=t commit -q --allow-empty -m fixture
  [ "$(git -C "$r/repo" rev-parse --show-toplevel)" = "$r/repo" ] || { echo "probe=$id FIXTURE-ROOT-MISMATCH"; return; }
  python3 -c 'import json,sys; json.dump({"figures":[{"id":sys.argv[1],"record":"probe","recorded":sys.argv[2],"derive":sys.argv[3],"want":sys.argv[2]}]}, open(sys.argv[4],"w"))' "$id" "$want" "$derive" "$r/one.json"
  ( cd "$r/repo" && python3 "$INSTR" --ledger "$r/one.json" --root "$r/repo" > "$r/out.txt" 2>&1; echo "$?" > "$r/rc" )
  m=$(ls "$r/repo" | grep -c '^MARK-')
  echo "probe=$id derive=$(printf '%s' "$derive" | tr '\n' '|') exit=$(cat "$r/rc") markers=$m :: $(head -1 "$r/out.txt")"
}

# refusal probes: 2 = the gate refused before running the derive, 0 markers
run Q1-escape-single 35 "cat g.txt \\'; touch MARK-Q1; \\'"
run Q2-escape-double 35 "cat g.txt \\\"; touch MARK-Q2; \\\""
run Q3-sed-in-program 35 "sed -n '1e touch MARK-Q3' g.txt"
run Q4-awk-system 35 "awk 'BEGIN{system(\"touch MARK-Q4\")}'"
run Q5-sort-output-flag 35 "sort -o MARK-Q5 g.txt"
runinrepo Q6-git-show-output 35 "git show --output=MARK-Q6 HEAD"
runinrepo Q7-git-show-ext-diff 35 "git show --ext-diff HEAD"
# controls that must stay admitted on both sides
run CTRL-quoted-semicolon 35 "cat g.txt | grep -e '35' -e ';'"
run CTRL-plain-count 1 "cat g.txt | wc -l"
# named-open residual: the gate still admits an interpreter head outside the lane root
run RESIDUAL-python-traversal 35 "python3 corpus/instruments/../../../above-evil.py"
