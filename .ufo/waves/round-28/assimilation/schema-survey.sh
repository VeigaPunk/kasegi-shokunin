#!/usr/bin/env bash
# schema-survey.sh — round-28 wave-1: census-schema conformance of the ADOPTED staged rows
# (staged S042 -> lane S042, staged S043 -> lane S041) plus the quarantine slice.
#
# Census grammar (SOURCES-CONTRACT-v1 / scripts/sources-census.sh validate):
#   - one registry table, 11 columns => NF=13
#   - id  S[0-9]{3,}   kind spec|docs|paper|code|tool|dataset|talk|book|community|own-work
#   - tier A|B|C      status queued|mined|rejected
#   - opened  ISO date (past or today)
#   - recheck  ISO date | NNn | symbolic cadence  (NOT prose)
#   - used-by  path that exists on disk
# Reads only; writes only under .ufo/waves/round-28/assimilation/.
set -u
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
PKG=/home/vgpnk/Projects/shokuknow/merge/kasegi
REG=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
A=$LANE/.ufo/waves/round-28/assimilation

run() {
  printf '$ %s\n' "$*"
  bash -c "$*"
  rc=$?
  printf '[exit %s]\n\n' "$rc"
}

cd "$LANE" || exit 1

echo "== round-28 wave-1 staged-row schema survey =="
echo

for ID in S042 S043; do
  echo "-- $ID: field count (NF must be 13 for an 11-column row) --"
  run "awk -F'|' -v id='$ID' '\$2 ~ \"^[[:space:]]*\" id \"[[:space:]]*\$\" {print \"NF=\" NF; print \"fields_minus_edges=\" NF-2}' $PKG/SOURCES.append.md"

  echo "-- $ID: literal or escaped pipes inside cells --"
  run "awk -F'|' -v id='$ID' '\$2 ~ \"^[[:space:]]*\" id \"[[:space:]]*\$\" {for(i=2;i<=NF;i++) if(\$i ~ /\\\\\|/) print \"cell \" i \" contains an ESCAPED pipe: \" \$i}' $PKG/SOURCES.append.md"
  run "grep -cF '\\\\|' <(grep -E '^ {0,3}\\\\| *'$ID' *\\\\|' $PKG/SOURCES.append.md)"
  echo "(0 on both = no escaped pipe inside any cell)"

  echo "-- $ID: cell-by-cell --"
  run "awk -F'|' -v id='$ID' '\$2 ~ \"^[[:space:]]*\" id \"[[:space:]]*\$\" {n=split(\"id source kind tier scope anchor teaches status opened recheck used-by\",names,\" \"); for(i=1;i<=n;i++){c=\$(i+1); gsub(/^[[:space:]]+|[[:space:]]+\$/,\"\",c); printf \"  col%-8s len=%-4d %s\n\", names[i], length(c), (length(c)>150 ? substr(c,1,150) \" ...[TRUNC]\" : c)}}' $PKG/SOURCES.append.md"
  echo
done

echo "-- recheck-cell form check against the census grammar (ISO date | NNn | symbolic) --"
run "awk -F'|' -v l='kasegi' 'index(\$2,l)>0 && \$3 ~ /round[0-9]+/ && \$4 ~ /S[0-9]+/ {id=\$4; gsub(/[^S0-9]/,\"\",id); cls=\$5; gsub(/^[[:space:]]+|[[:space:]]+\$/,\"\",cls); printf \"%s | class=%s | round=%s\n\", id, cls, \$3}' $REG"
echo

echo "-- quarantine slice: does ANY register row name staged S042 or S043 (or their URLs)? --"
run "grep -nE '\\| *S04[23] *(\`|$)' $REG | cut -c1-220"
run "grep -cF 'todokede/vuln/process' $REG"
run "grep -cF 'partnership_guideline2026' $REG"
echo "(both 0 = neither adopted document is in the absent-defect register)"

echo "-- used-by paths named by the staged adopted rows: do they exist in the LANE today? --"
run "for f in corpus/knowledge/japanese-domestic-disclosure-workflow.md corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md corpus/knowledge/japanese-disclosure-legal-framework.md; do printf '%s exists=%s\n' \"\$f\" \"\$(test -e \"\$f\" && echo yes || echo no)\"; done"
