#!/usr/bin/env bash
# round-83 L1 landing receipt: P1-P8 (C1) and B0-B8 (C2) over the landing tree.
# Usage: landing-r83.sh <scratch-dir>   (writes nothing in the lane; prints the receipt)
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$L/.ufo/waves/round-83
FZ=0cd499dbdfc0bf9ce3095681af9bc76588d76f31
BASE=834bf78eaca70a69294f2ecfefa89b73c3fa85b8
S=${1:?scratch dir}
[ -n "$S" ] && mkdir -p "$S" || exit 2
export TMPDIR=$S
cd "$L" || exit 2
I=corpus/instruments/recheck-cwd-census.py
E=corpus/knowledge/osv-faq-post-import-record-lifecycle.md
M=corpus/source-snapshots/round-83/manifest.json
echo "# L1 landing receipt round 83 — $(date -u +%FT%TZ)"
echo "## frozen bytes vs freeze ${FZ:0:8}"
for f in .ufo/waves/round-83/claims.json .ufo/waves/round-83/c1/recheck-cwd-census.py .ufo/waves/round-83/c1/mutbat.py \
         .ufo/waves/round-83/c1/mutant-table.json .ufo/waves/round-83/c1/build-table.py .ufo/waves/round-83/c2/entry-gate.py \
         .ufo/waves/round-83/controls/c1-forgeries-r83.py .ufo/waves/round-83/controls/c1-stub-r83.py \
         .ufo/waves/round-83/controls/c2-controls-r83.py "$M" corpus/source-snapshots/round-83/S117.txt; do
  if git show $FZ:"$f" | cmp -s - "$f"; then echo "FROZEN-OK $f"; else echo "FROZEN-CHANGED $f"; fi
done
echo "## P1"; python3 -B $I --selftest | tail -1; echo "rc=${PIPESTATUS[0]}"
echo "## P2"; sha256sum $I
echo "## P3"; mkdir -p "$S/p3"; python3 -B $W/c1/mutbat.py --target $I --table $W/c1/mutant-table.json --expect-cases 27 --work "$S/p3" | tail -2; echo "rc=${PIPESTATUS[0]}"
echo "## P4"; for f in F6-selfdiff F7-wsnorm F8-astembed F9-pathlabel F10-hashwl F11-count; do
  mkdir -p "$S/f-$f"; python3 -B $W/controls/c1-forgeries-r83.py --lane "$L" --work "$S/f-$f" --only $f > "$S/f-$f.out" 2>&1 &
done; wait; cat "$S"/f-F6-selfdiff.out "$S"/f-F7-wsnorm.out "$S"/f-F8-astembed.out "$S"/f-F9-pathlabel.out "$S"/f-F10-hashwl.out "$S"/f-F11-count.out
echo "## P5"; ls corpus/knowledge/*.md | wc -l; python3 -B $I --root "$L" --lane "$L" | tail -2; echo "rc=${PIPESTATUS[0]}"
echo "## P6"; mkdir -p "$S/p6"; python3 -B $W/c1/mutbat.py --selftest --work "$S/p6" | grep -oE "^mutbat selftest [a-z]+|r83_forgeries=\{[^}]*\}"; echo "rc=${PIPESTATUS[0]}"
echo "## P7"; for f in c1-donothing-r83.txt c1-stub-r83.txt; do printf '%s last=%s survived_G=%s\n' "$f" "$(tail -1 $W/controls/$f)" "$(grep -cE '^MUTANT G[1-4] verdict=SURVIVED' $W/controls/$f)"; done
echo "## P8"; for f in SKILL.md corpus/instruments/README.md; do
  row=$(grep -E '^\| (`corpus/instruments/)?recheck-cwd-census\.py`? \|' "$f"); printf '%s cases27=%s cases24=%s\n' "$f" "$(printf '%s' "$row" | grep -c 'cases=27')" "$(printf '%s' "$row" | grep -c 'cases=24')"; done
echo "## B0"; python3 corpus/instruments/source-recheck.py --manifest $M --source S117; echo "rc=$?"
echo "## B1"; git diff $FZ -- corpus/SOURCES.md | grep -E '^[-+]\| S[0-9]+' | cut -c1-12; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
echo "## B2"; ls corpus/knowledge/*.md | wc -l; diff <(grep -v '^#' corpus/instruments/knowledge-expected.txt | LC_ALL=C sort) <(ls corpus/knowledge/*.md | LC_ALL=C sort) && echo set-equal
echo "## B3"; python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F59'
echo "## B4"; python3 corpus/instruments/capture-binding-check.py | tail -1
echo "## B5"; v=$(grep -m1 '^recheck:' $E | sed 's/^recheck: //'); d=$(mktemp -d -p "$S"); (cd "$d" && bash -c "$v" >/dev/null); echo "foreign rc=$?"
echo "## B6"; python3 - <<'P'
import json, glob
m = json.load(open("corpus/source-snapshots/round-83/manifest.json"))
fs = [f for f in glob.glob("corpus/knowledge/*.md") if not f.endswith("osv-faq-post-import-record-lifecycle.md")]
print("literal_sweep_total", sum(1 for q in m["sources"][0]["quotes"] for f in fs if q["quote"] in open(f, encoding="utf-8").read()), "files", len(fs))
P
echo "## B7"; /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi | tail -1; echo "rc=${PIPESTATUS[0]}"
echo "## B8"; python3 -B $W/c2/entry-gate.py --entry $E --manifest $M --source S117 --lane "$L"; echo "rc=$?"
python3 -B $W/controls/c2-controls-r83.py --lane "$L" --work "$S/c2"; echo "rc=$?"
echo "## harm: density SKILL.md (base ${BASE:0:8} vs landing)"; git show $BASE:SKILL.md > "$S/SKILL.base.md"; python3 corpus/instruments/density.py "$S/SKILL.base.md" --label base | grep "mean dens"; python3 corpus/instruments/density.py SKILL.md --label landing | grep "mean dens"
echo "## R133 check on the round-83 lesson"; awk '/^## Gate/{g=1} /^## Mistakes/{g=0} g' corpus/lessons/round-83.md | grep -c -E 'PENDING-L1|TBD|TODO'
