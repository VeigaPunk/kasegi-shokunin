#!/usr/bin/env bash
# Plain re-derivation of the per-entry rows of a re-ground section: no python, no counter. usage: plain-rows.sh <tree> <entry-name>
# prints `row <id> located=0|1` per row, then `rows=<n> located=<k>`. A row is located when its backticked token is a fixed substring of its backticked anchor line range.
T=$1; E=$2; n=0; k=0
while IFS=$'\t' read -r id anchor token; do
  a=$(printf '%s' "$anchor" | sed -E 's/^ *`//; s/` *$//'); tok=$(printf '%s' "$token" | sed -E 's/^ *`//; s/` *$//')
  path=${a%%:*}; rng=${a#*:}; from=${rng%%-*}; to=${rng##*-}
  n=$((n+1))
  if sed -n "${from},${to}p" "$T/$path" | tr -s ' \t\n' ' ' | grep -qF -- "$(printf '%s' "$tok" | tr -s ' \t' ' ')"; then k=$((k+1)); echo "row $id located=1"; else echo "row $id located=0"; fi
done < <(awk -F'|' '/^\| G[0-9]+ \|/ {gsub(/^ +| +$/,"",$2); print $2 "\t" $4 "\t" $5}' "$T/corpus/knowledge/$E")
echo "rows=$n located=$k"
