#!/usr/bin/env bash
# plain-controls.sh <pure-tree> <scratch-dir> <lane>
# Builds do-nothing / marker-only variants of <pure-tree> under <scratch-dir> (copies; <pure-tree> is
# never edited), runs plain-measure.sh on each and recheck-audit.py (root = the variant) beside it.
# Draft control harness for round 46 -- not a gate.
set -u
P=$1; S=$2; L=$3
HERE=$(cd "$(dirname "$0")" && pwd -P)
export PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S
CPC=corpus/knowledge/claim-package-contract.md
mk() { rm -rf "$S/$1"; mkdir -p "$S/$1"; cp -a "$P/." "$S/$1/"; }
setline() { # <variant> <entry-rel> <new recheck line>  (replace the first ^recheck: line)
  awk -v n="$3" 'BEGIN{d=0} /^recheck:/ && !d {print "recheck: " n; d=1; next} {print}' "$S/$1/$2" > "$S/$1/$2.new" && mv "$S/$1/$2.new" "$S/$1/$2"; }
report() { # <variant> <what>
  printf '%-14s %-62s ' "$1" "$2"
  bash "$HERE/plain-measure.sh" "$S/$1" | tr '\n' ' '
  printf '| audit: %s\n' "$(python3 "$L/corpus/instruments/recheck-audit.py" --root "$S/$1" --quiet 2>&1 | grep -oE 'executes=[0-9]+ gated=[0-9]+ broken=[0-9]+')"; }

mk K0; report K0 "unchanged copy of the pure base"
mk K1; setline K1 $CPC 'true'; report K1 "claim-package-contract recheck := true"
mk K2; setline K2 $CPC "test -s $CPC"; report K2 "recheck := test -s <own file>  (self-existence)"
mk K3; setline K3 $CPC 'false'; report K3 "recheck := false  (still gated, marker text gone)"
mk K4; setline K4 $CPC 'if then'; report K4 "recheck := syntax error  (parse-broken)"
mk K5; setline K5 $CPC "cd $L && true # test -d ~/Projects/bounties"; report K5 "recheck := cd <lane> && true # test -d ~/Projects/ (marker kept in a comment)"
mk K6
printf '| F28 | marker | admitted | `corpus/knowledge/github-private-vulnerability-reporting.md` | S073 | marker |\n' >> "$S/K6/corpus/README.md"
printf '| S073 | marker private vulnerability reporting | docs | A | marker |\n' >> "$S/K6/corpus/SOURCES.md"
printf 'private vulnerability reporting\nrecheck: true\n' > "$S/K6/corpus/knowledge/github-private-vulnerability-reporting.md"
report K6 "C2 marker-only: F28 row + S073 row + stub entry (no capture, no quotes)"
mk K7; printf '| F28 | marker |\n' >> "$S/K7/corpus/README.md"; report K7 "C2 junk F28 row only"
mk K8; printf '| S073 | marker |\n' >> "$S/K8/corpus/SOURCES.md"; report K8 "C2 junk S073 row only"
mk K9; printf 'privately report\n' >> "$S/K9/corpus/knowledge/claim-gates.md"; report K9 "C2 one sentence 'privately report' appended to an old entry"
mk K10; : > "$S/K10/corpus/knowledge/zz-empty.md"; report K10 "C2 empty knowledge file (no recheck line)"
mk K11; rm -f "$S/K11/corpus/source-snapshots/round-24/manifest.json"; report K11 "deleted a committed manifest an executing recheck reads"
