#!/usr/bin/env bash
# round-82 L1 landing receipt: P1-P9 (C1) and B0-B8 (C2) over the landing tree.
# Usage: landing-r82.sh <scratch-dir>   (writes nothing in the lane; prints the receipt)
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$L/.ufo/waves/round-82
S=${1:?scratch dir}
[ -n "$S" ] && mkdir -p "$S" || exit 2
export TMPDIR=$S
cd "$L" || exit 2
I=corpus/instruments/recheck-cwd-census.py
E=corpus/knowledge/osv-high-quality-record-import-bar.md
M=corpus/source-snapshots/round-82/manifest.json
echo "# L1 landing receipt round 82 — $(date -u +%FT%TZ)"
echo "## frozen bytes vs freeze b9589300"
for f in .ufo/waves/round-82/claims.json .ufo/waves/round-82/c1/recheck-cwd-census.py .ufo/waves/round-82/c1/mutbat.py \
         .ufo/waves/round-82/c1/mutant-table.json .ufo/waves/round-82/c1/build-table.py .ufo/waves/round-82/c2/entry-gate.py \
         .ufo/waves/round-82/controls/c1-forgeries-r82.py "$M" corpus/source-snapshots/round-82/S116.txt; do
  if git show b9589300810a477f4d6794bfabc24b22fb50b846:"$f" | cmp -s - "$f"; then echo "FROZEN-OK $f"; else echo "FROZEN-CHANGED $f"; fi
done
echo "## P1"; python3 -B $I --selftest | tail -1; echo "rc=${PIPESTATUS[0]}"
echo "## P2"; sha256sum $I
echo "## P3"; python3 -B $W/c1/mutbat.py --target $I --table $W/c1/mutant-table.json --expect-cases 24 --work "$S" | tail -1; echo "rc=${PIPESTATUS[0]}"
echo "## P4"; mkdir -p "$S/f"; python3 -B $W/controls/c1-forgeries-r82.py --lane "$L" --work "$S/f"; echo "rc=${PIPESTATUS[0]}"
echo "## P5"; ls corpus/knowledge/*.md | wc -l; python3 -B $I --root "$L" --lane "$L" | tail -2; echo "rc=${PIPESTATUS[0]}"
echo "## P6"; mkdir -p "$S/j"; python3 - "$S/j/recheck-cwd-census.py" <<'P'
import json, sys
src = open("corpus/instruments/recheck-cwd-census.py").read()
r = [x for x in json.load(open(".ufo/waves/round-82/c1/mutant-table.json")) if x["id"] == "J1"][0]
assert src.count(r["anchor"]) == 1
open(sys.argv[1], "w").write(src.replace(r["anchor"], r["replacement"], 1))
P
python3 -B "$S/j/recheck-cwd-census.py" --root "$L" --lane "$L" | tail -2; echo "rc=${PIPESTATUS[0]}"
echo "## P7"; for f in SKILL.md corpus/instruments/README.md; do
  row=$(grep -E '^\| (`corpus/instruments/)?recheck-cwd-census\.py`? \|' "$f"); printf '%s cases24=%s cases22=%s\n' "$f" "$(printf '%s' "$row" | grep -c 'selftest cases=24 failures=0')" "$(printf '%s' "$row" | grep -c 'cases=22')"; done
echo "## P8"; grep -c 'subprocess.run(' $I; grep -c '"bash", "-c"' $I; grep -cE "[\"']/tmp" $I
echo "## P9"; python3 -B $W/c1/mutbat.py --selftest --work "$S" | grep -o '^mutbat selftest [a-z]*\|selfdiff_forgery_exit=[A-Za-z]*'; echo "rc=${PIPESTATUS[0]}"
echo "## B0"; python3 corpus/instruments/source-recheck.py --manifest $M --source S116; echo "rc=$?"
echo "## B1"; git diff b9589300810a477f4d6794bfabc24b22fb50b846 -- corpus/SOURCES.md | grep -E '^[-+]\| S[0-9]+' | cut -c1-12; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
echo "## B2"; ls corpus/knowledge/*.md | wc -l; diff <(grep -v '^#' corpus/instruments/knowledge-expected.txt | LC_ALL=C sort) <(ls corpus/knowledge/*.md | LC_ALL=C sort) && echo set-equal
echo "## B3"; python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F58'
echo "## B4"; python3 corpus/instruments/capture-binding-check.py | tail -1
echo "## B5"; v=$(grep -m1 '^recheck:' $E | sed 's/^recheck: //'); d=$(mktemp -d -p "$S"); (cd "$d" && bash -c "$v" >/dev/null); echo "foreign rc=$?"
echo "## B6"; python3 - <<'P'
import json, glob
m = json.load(open("corpus/source-snapshots/round-82/manifest.json"))
fs = [f for f in glob.glob("corpus/knowledge/*.md") if not f.endswith("osv-high-quality-record-import-bar.md")]
print("literal_total", sum(1 for q in m["sources"][0]["quotes"] for f in fs if q["quote"] in open(f, encoding="utf-8").read()), "files", len(fs))
P
echo "## B7"; /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi | tail -1; echo "rc=${PIPESTATUS[0]}"
echo "## B8"; python3 -B $W/c2/entry-gate.py --entry $E --manifest $M --source S116 --lane "$L"; echo "rc=$?"
python3 -B $W/c2/entry-gate.py --entry .ufo/waves/round-81/w1/CriticClaims-receipts/junk-labelled.md --manifest corpus/source-snapshots/round-81/manifest.json --source S115 --lane "$L"; echo "rc=$?"
echo "## harm: density SKILL.md (base 1a50638e vs landing)"; git show 1a50638edabb9bd1a4a4784774fc984cb5f2360f:SKILL.md > "$S/SKILL.base.md"; python3 corpus/instruments/density.py "$S/SKILL.base.md" --label base | grep "mean dens"; python3 corpus/instruments/density.py SKILL.md --label landing | grep "mean dens"
echo "## R133 check on the round-82 lesson"; awk '/^## Gate/{g=1} /^## Mistakes/{g=0} g' corpus/lessons/round-82.md | grep -c -E 'PENDING-L1|TBD|TODO'
