#!/usr/bin/env bash
# round-59 C1 residual-class runner (wave evidence, committed). NOT part of the frozen predicate:
# these are the named-open classes the lesson records (B1-B4, B6), the newline control B5 and the
# non-bypass B7. usage: c1-residual-run.sh <figure-audit.py path> <scratch dir>
set -u
INSTR=$1
S=$2
rm -rf -- "$S"
mkdir -p -- "$S"
trap 'rm -rf -- "$S"' EXIT
echo "instrument=$INSTR sha256=$(sha256sum "$INSTR" | cut -c1-16)"
echo "run-utc=$(date -u +%Y-%m-%dT%H:%M:%SZ) host=$(hostname)"

run() {
  id=$1
  derive=$2
  r="$S/r-$id"
  mkdir -p "$r"
  printf '35\n' > "$r/g.txt"
  python3 -c 'import json,sys; json.dump({"figures":[{"id":sys.argv[1],"record":"residual","recorded":"35","derive":sys.argv[2],"want":"35"}]}, open(sys.argv[3],"w"))' "$id" "$derive" "$r/one.json"
  ( cd "$r" && python3 "$INSTR" --ledger "$r/one.json" --root "$r" > "$r/out.txt" 2>&1; echo "$?" > "$r/rc" )
  m=$(ls "$r" | grep -c '^MARK-')
  echo "residual=$id derive=$(printf '%s' "$derive" | tr '\n' '|') exit=$(cat "$r/rc") markers=$m :: $(head -1 "$r/out.txt")"
}

run B1-escaped-squote 'cat g.txt \'"'"'; touch MARK-B1; \'"'"''
run B2-escaped-dquote 'cat g.txt \"; touch MARK-B2; \"'
run B3-sed-e-command "cat g.txt | sed -n '1e touch MARK-B3'"
run B4-awk-system 'cat g.txt | awk '"'"'BEGIN{system("touch MARK-B4")}'"'"''
run B5-newline-continuation 'cat g.txt \
touch MARK-B5'
run B6-sort-o 'sort -o MARK-B6 g.txt && cat MARK-B6'
run B7-git-show-output 'git show --output=MARK-B7 HEAD:README.md'
