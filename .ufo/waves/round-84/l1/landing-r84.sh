#!/usr/bin/env bash
# round-84 L1 landing receipt: P1-P8 (C1) and B0-B8 (C2) over the bytes of a named landing
# commit (r83 routed defect 7): the commit is extracted with git archive into scratch and every
# predicate runs on that extract, not on the worktree.
# Usage: landing-r84.sh <landing-commit> <scratch-dir>   (writes nothing in the lane)
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
FZ=7f76b7eb690cd6e75e7f3e7729cedcb15611b34b
BASE=a089ff3d601b4d53a5515e52720ba27e5ec72c3d
REV=${1:?landing commit}
S=${2:?scratch dir}
[ -n "$S" ] && mkdir -p "$S" || exit 2
export TMPDIR=$S
X=$S/extract
rm -rf "$X" && mkdir -p "$X"
git -C "$L" archive "$REV" | tar -x -C "$X" || exit 2
cd "$X" || exit 2
W=.ufo/waves/round-84
I=corpus/instruments/recheck-cwd-census.py
E=corpus/knowledge/osv-gcs-data-dump-layout.md
M=corpus/source-snapshots/round-84/manifest.json
echo "# L1 landing receipt round 84 — $(date -u +%FT%TZ) — over git archive of $(git -C "$L" rev-parse "$REV")"
echo "## frozen bytes vs freeze ${FZ:0:8}"
for f in $W/claims.json $W/c1/recheck-cwd-census.py $W/c1/mutbat.py $W/c1/mutant-table.json $W/c1/build-table.py \
         $W/controls/c1-stub-r84.py $W/controls/c1-counter-mutants-r84.py "$M" corpus/source-snapshots/round-84/S118.txt; do
  if git -C "$L" show $FZ:"$f" | cmp -s - "$f"; then echo "FROZEN-OK $f"; else echo "FROZEN-CHANGED $f"; fi
done
if git -C "$L" show $BASE:.ufo/waves/round-83/c2/entry-gate.py | cmp -s - .ufo/waves/round-83/c2/entry-gate.py; then echo "FROZEN-OK r83 entry-gate"; else echo "FROZEN-CHANGED r83 entry-gate"; fi
echo "## P1"; python3 -B $I --selftest | tail -1; echo "rc=${PIPESTATUS[0]}"
echo "## P2"; sha256sum $I
echo "## P3"; mkdir -p "$S/p3"; python3 -B $W/c1/mutbat.py --target $I --table $W/c1/mutant-table.json --expect-cases 33 --work "$S/p3" > "$S/p3.out"; echo "rc=$?"
grep '^MUTBAT' "$S/p3.out"; echo "killed_lines=$(grep -cE '^MUTANT [^ ]+ verdict=(KILLED|EXCEPTION-KILL) ' "$S/p3.out") h_killed=$(grep -cE '^MUTANT H(0[1-9]|1[0-2]) verdict=KILLED ' "$S/p3.out")"
echo "## P4"; mkdir -p "$S/p4"; python3 -B $W/c1/mutbat.py --selftest --work "$S/p4" | grep -oE "^mutbat selftest [a-zA-Z]+|r84_limbs=\{[^}]*\}"; echo "rc=${PIPESTATUS[0]}"
echo "## P5"; mkdir -p "$S/p5"; python3 -B $W/controls/c1-counter-mutants-r84.py --lane "$X" --work "$S/p5"; echo "rc=$?"
echo "## P6"; ls corpus/knowledge/*.md | wc -l; python3 -B $I --root "$X" --lane "$L" | tail -2; echo "rc=${PIPESTATUS[0]}"
echo "## P7"; for f in c1-donothing-r84.txt c1-stub-r84.txt; do printf '%s last=%s survived_H=%s\n' "$f" "$(tail -1 $W/controls/$f)" "$(grep -cE '^MUTANT H(0[1-9]|1[0-2]) verdict=SURVIVED' $W/controls/$f)"; done
echo "## P8"; for f in SKILL.md corpus/instruments/README.md; do
  row=$(grep -E '^\| (`corpus/instruments/)?recheck-cwd-census\.py`? \|' "$f"); printf '%s cases33=%s cases27=%s\n' "$f" "$(printf '%s' "$row" | grep -c 'cases=33')" "$(printf '%s' "$row" | grep -c 'cases=27')"; done
echo "## B0"; python3 corpus/instruments/source-recheck.py --manifest $M --source S118; echo "rc=$?"
echo "## B1"; git -C "$L" diff $FZ "$REV" -- corpus/SOURCES.md | grep -E '^[-+]\| S[0-9]+' | cut -c1-12; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md; grep '^| S118' corpus/SOURCES.md | grep -oE '\| (queued|mined) \| [^|]+ \| [^|]+ \| [^|]+ \|$'
echo "## B2"; echo "freeze=$(git -C "$L" ls-tree -r --name-only $FZ corpus/knowledge | grep -c '\.md$') landing=$(ls corpus/knowledge/*.md | wc -l)"; diff <(grep -v '^#' corpus/instruments/knowledge-expected.txt | LC_ALL=C sort) <(ls corpus/knowledge/*.md | LC_ALL=C sort) && echo set-equal; git -C "$L" diff $FZ "$REV" -- corpus/instruments/knowledge-expected.txt | grep -E '^[-+][^-+]'
echo "## B3"; python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F60'
echo "## B4"; python3 corpus/instruments/capture-binding-check.py | tail -1
echo "## B5"; v=$(grep -m1 '^recheck:' $E | sed 's/^recheck: //'); echo "recheck_exact=$([ "$v" = "cd $L && python3 corpus/instruments/source-recheck.py --manifest $M --source S118" ] && echo yes || echo no)"; d=$(mktemp -d -p "$S"); (cd "$d" && bash -c "$v" >/dev/null); echo "foreign rc=$?"
echo "## B6"; python3 - <<'P'
import json, glob
m = json.load(open("corpus/source-snapshots/round-84/manifest.json"))
fs = [f for f in glob.glob("corpus/knowledge/*.md") if not f.endswith("osv-gcs-data-dump-layout.md")]
print("literal_sweep_total", sum(1 for q in m["sources"][0]["quotes"] for f in fs if q["quote"] in open(f, encoding="utf-8").read()), "files", len(fs))
P
echo "## B7"; /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$X/corpus/SOURCES.md" | tail -1; echo "rc=${PIPESTATUS[0]}"
echo "## B8"; python3 -B .ufo/waves/round-83/c2/entry-gate.py --entry $E --manifest $M --source S118 --lane "$L"; echo "rc=$?"
echo "## harm: density SKILL.md (base ${BASE:0:8} vs landing)"; git -C "$L" show $BASE:SKILL.md > "$S/SKILL.base.md"; python3 corpus/instruments/density.py "$S/SKILL.base.md" --label base | grep "mean dens"; python3 corpus/instruments/density.py SKILL.md --label landing | grep "mean dens"
echo "## R133 check on the round-84 lesson"; awk '/^## Gate/{g=1} /^## Mistakes/{g=0} g' corpus/lessons/round-84.md | grep -c -E 'PENDING-L1|TBD|TODO'
