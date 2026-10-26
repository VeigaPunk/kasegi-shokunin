#!/usr/bin/env bash
# judge-g2-cases.sh — G2' fixture judge: grades the selftest case region of an
# all-gates v3 receipt and prints exactly one line:
#
#   G2 payload=receipt=<0|1>,sentinel=<0|1>,run-lines=<0|1>,closed-line=<0|1>,cases=<n>,graded=<n>,detail-ok=<0|1>,summary=<n>,summary-only=<0|1> closed=<0|1>
#
# exit 0 when closed=1, exit 1 otherwise.  Usage: judge-g2-cases.sh RECEIPT
#
# Field contract (the rule the round-39 G2 check must implement):
#   sentinel        first line is exactly `all-gates v3`
#   run-lines       exactly eight distinct `G<n> payload=... closed=1` lines
#   closed-line     exactly one `closed=8/8 exit=0`
#   cases           number of `selftest case=G<n> ` lines (any id digits)
#   graded          ids G1..G8 that carry exactly ONE case line and that line
#                   matches `^selftest case=G<n> positive=pass mutants=<a>/<b>
#                   verdict=pass$` (whole line: no missing verdict=, no trailing
#                   field, no verdict=fail, no positive=fail)
#   detail-ok       1 iff at least one id graded and every such id corroborates:
#                   b>=1, a==b, and exactly b `selftest detail=G<n> mutant=`
#                   lines of which exactly a end in `rejected=1` (a bare
#                   `rejected=10` does not count)
#   summary         number of `selftest cases=8 failures=0` lines
#   summary-only    1 iff the receipt carries `selftest ` lines but zero
#                   `selftest case=G<n> ` lines: a summary line never satisfies
#                   a case, so this state is a forgery, not a pass
#   closed          1 iff sentinel, run-lines, closed-line, cases == 8,
#                   graded == 8, detail-ok == 1, summary == 1, summary-only == 0
set -u

f=${1-}
if [ -z "$f" ] || [ ! -f "$f" ]; then
  printf 'G2 payload=receipt=0,sentinel=0,run-lines=0,closed-line=0,cases=0,graded=0,detail-ok=0,summary=0,summary-only=0 closed=0\n'
  exit 1
fi

sentinel=0; runlines=0; closedline=0; cases=0; graded=0; detailok=1
summary=0; summaryonly=0

[ "$(sed -n '1p' "$f")" = 'all-gates v3' ] && sentinel=1

n=$(grep -cE '^G[1-8] payload=.* closed=1$' "$f"); n=${n:-0}
u=$(grep -E '^G[1-8] payload=.* closed=1$' "$f" \
    | sed -n 's/^\(G[1-8]\) .*/\1/p' | sort -u | wc -l)
[ "$n" -eq 8 ] && [ "$u" -eq 8 ] && runlines=1

n=$(grep -cxF 'closed=8/8 exit=0' "$f"); n=${n:-0}
[ "$n" -eq 1 ] && closedline=1

cases=$(grep -cE '^selftest case=G[0-9]+ ' "$f"); cases=${cases:-0}
summary=$(grep -cxF 'selftest cases=8 failures=0' "$f"); summary=${summary:-0}
if [ "$cases" -eq 0 ] && grep -q '^selftest ' "$f"; then summaryonly=1; fi

for i in 1 2 3 4 5 6 7 8; do
  id=G$i
  hit=$(grep -cE "^selftest case=${id} " "$f"); hit=${hit:-0}
  [ "$hit" -eq 1 ] || continue
  line=$(grep -m1 -E "^selftest case=${id} " "$f")
  printf '%s' "$line" \
    | grep -qE "^selftest case=${id} positive=pass mutants=[0-9]+/[0-9]+ verdict=pass$" \
    || continue
  graded=$((graded + 1))
  ok=$(printf '%s' "$line" | sed -n 's/.*mutants=\([0-9][0-9]*\)\/\([0-9][0-9]*\) verdict=pass$/\1/p')
  tot=$(printf '%s' "$line" | sed -n 's/.*mutants=\([0-9][0-9]*\)\/\([0-9][0-9]*\) verdict=pass$/\2/p')
  det=$(grep -cE "^selftest detail=${id} mutant=" "$f"); det=${det:-0}
  rej=$(grep -cE "^selftest detail=${id} mutant=.*rejected=1( |$)" "$f"); rej=${rej:-0}
  if [ -z "$ok" ] || [ -z "$tot" ] || [ "$tot" -lt 1 ] || [ "$ok" -ne "$tot" ] \
     || [ "$det" -ne "$tot" ] || [ "$rej" -ne "$ok" ]; then
    detailok=0
  fi
done

[ "$graded" -eq 0 ] && detailok=0

closed=0
if [ "$sentinel" -eq 1 ] && [ "$runlines" -eq 1 ] && [ "$closedline" -eq 1 ] \
   && [ "$cases" -eq 8 ] && [ "$graded" -eq 8 ] && [ "$detailok" -eq 1 ] \
   && [ "$summary" -eq 1 ] && [ "$summaryonly" -eq 0 ]; then
  closed=1
fi

printf 'G2 payload=receipt=1,sentinel=%s,run-lines=%s,closed-line=%s,cases=%s,graded=%s,detail-ok=%s,summary=%s,summary-only=%s closed=%s\n' \
  "$sentinel" "$runlines" "$closedline" "$cases" "$graded" "$detailok" "$summary" "$summaryonly" "$closed"

[ "$closed" -eq 1 ]
