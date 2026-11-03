#!/usr/bin/env bash
# round-59 C1 chain-probe runner (wave evidence, committed).
# usage: c1-probe-run.sh <figure-audit.py path> <scratch dir>
# Runs each probe derive ALONE through the instrument, in its own fresh root holding g.txt ("35").
# A probe counts as EXECUTED when its marker file MARK-* appears in its root; REFUSED when the
# instrument exits 2 before running the derive. Scratch is removed on exit.
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
  python3 -c 'import json,sys; json.dump({"figures":[{"id":sys.argv[1],"record":"probe","recorded":"35","derive":sys.argv[2],"want":"35"}]}, open(sys.argv[3],"w"))' "$id" "$derive" "$r/one.json"
  ( cd "$r" && python3 "$INSTR" --ledger "$r/one.json" --root "$r" > "$r/out.txt" 2>&1; echo "$?" > "$r/rc" )
  m=$(ls "$r" | grep -c '^MARK-')
  echo "probe=$id derive=$(printf '%s' "$derive" | tr '\n' '|') exit=$(cat "$r/rc") markers=$m :: $(head -1 "$r/out.txt")"
}

run P1-semicolon 'cat g.txt; touch MARK-P1'
run P2-andand 'cat g.txt && touch MARK-P2'
run P3-background 'cat g.txt & touch MARK-P3'
run P4-newline 'cat g.txt
touch MARK-P4'
run P5-cmdsubst 'cat g.txt $(touch MARK-P5)'
run P6-pipe-tee 'cat g.txt | tee MARK-P6'
run P7-redirect 'cat g.txt > MARK-P7'
run P8-oror 'cat nosuch.txt || touch MARK-P8'
run CTRL-quoted-separator "cat g.txt | awk 'BEGIN{x=1;y=2} {print}'"
run RESIDUAL-awk-write "cat g.txt | awk 'BEGIN{print 1 > \"MARK-RES\"}{print}'"
