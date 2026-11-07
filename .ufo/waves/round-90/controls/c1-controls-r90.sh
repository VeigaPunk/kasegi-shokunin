#!/usr/bin/env bash
# kasegi round-90 C1 pre-freeze controls. A fixture repo (mktemp under SCRATCH, toplevel asserted)
# holds BASE's tree as commit B; each control commits one candidate "after" tree on top of B and
# runs the frozen counter with the frozen targets. Expect: candidate PASS, every other FAIL.
# Also the environment receipt (lesson M90-1): r89 meter vs r90 meter, live lane vs clean clone.
# Usage: c1-controls-r90.sh LANE BASE SCRATCH
set -u
L=$1; BASE=$2; S=$3; W=$L/.ufo/waves/round-90; M=$W/c1/knowledge-meter.py; MAP=$W/c1/repair-map.tsv
mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT
D=$(mktemp -d -p "$S" fx.XXXXXX); git -C "$D" init -q
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "fixture toplevel mismatch"; exit 2; }
g() { git -C "$D" -c user.name=fixture -c user.email=fixture@invalid "$@"; }
git -C "$L" archive "$BASE" | tar -x -C "$D"; g add -A; g commit -qm base; B=$(g rev-parse HEAD)
MS=$(sha256sum "$MAP" | cut -d' ' -f1)
meter() { python3 -B "$M" --lane "$D" --base-rev "$B" --after-rev "$1" --map "$2" --labels-rev "$B" --base-target 812/1827 --target 843/1829 --map-sha256 "$MS" --work "$S/w"; echo "control_rc=$?"; }
mk() { g checkout -q "$B"; g checkout -q -B "$1"; }
python3 - "$MAP" "$S" <<'PY'
import sys,re
rows=[l for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
def shift(v):
    m=re.match(r'^(.*?):(\d+)(?:-(\d+))?$',v); a=int(m.group(2))+1
    return '%s:%d'%(m.group(1),a) if not m.group(3) else '%s:%d-%d'%(m.group(1),a,int(m.group(3))+1)
open(sys.argv[2]+'/shift.tsv','w').write(''.join('\t'.join(r.rstrip('\n').split('\t')[:2]+[shift(r.rstrip('\n').split('\t')[2])])+'\n' for r in rows))
ex=[l for l in open(sys.argv[1].replace('repair-map.tsv','excluded.tsv')) if l.strip() and not l.startswith('#')]
lab={}
for l in open(sys.argv[1].replace('round-90/c1/repair-map.tsv','round-89/w1/ReviewC1Labels-receipts/tranche5-labels.tsv')):
    c=l.rstrip('\n').split('\t')
    if len(c)>=4: lab[(c[1],c[0])]=c[3]
open(sys.argv[2]+'/superset.tsv','w').write(''.join(rows)+''.join('%s\t%s\t%s\n'%(e.split('\t')[0],e.split('\t')[1],lab[(e.split('\t')[0],e.split('\t')[1])]) for e in ex))
open(sys.argv[2]+'/unlabelled.tsv','w').write(''.join(rows)+'corpus/knowledge/triage-thresholds.md:458\tmission-control.md:13-46\tcorpus/knowledge/mission-control.md:13-46\n')
PY
echo "== candidate (expect PASS)"; mk cand; python3 "$W/c1/apply-map.py" --tree "$D" --map "$MAP"; g commit -qam cand; meter "$(g rev-parse HEAD)" "$MAP"
echo "== no-work: after = base (expect FAIL)"; meter "$B" "$MAP"
echo "== shift-forgery: every value anchor +1 (expect FAIL)"; mk shift; python3 "$W/c1/apply-map.py" --tree "$D" --map "$S/shift.tsv"; g commit -qam shift; meter "$(g rev-parse HEAD)" "$S/shift.tsv"
echo "== superset-forgery: the 4 excluded sites applied too (expect FAIL)"; mk sup; python3 "$W/c1/apply-map.py" --tree "$D" --map "$S/superset.tsv"; g commit -qam sup; meter "$(g rev-parse HEAD)" "$S/superset.tsv"
echo "== unlabelled-forgery: a CORRECT-labelled site repointed (expect FAIL)"; mk unl; python3 "$W/c1/apply-map.py" --tree "$D" --map "$S/unlabelled.tsv"; g commit -qam unl; meter "$(g rev-parse HEAD)" "$S/unlabelled.tsv"
echo "== working-tree-only: candidate edit left uncommitted, after = base (expect FAIL)"; mk wt; python3 "$W/c1/apply-map.py" --tree "$D" --map "$MAP"; meter "$B" "$MAP"; g checkout -q -- .
echo "== environment receipt (lesson M90-1): b9fcf005, live lane vs clean clone"
C=$(mktemp -d -p "$S" clone.XXXXXX); git clone -q --no-hardlinks "$L" "$C/l"
for lane in "$L" "$C/l"; do
  echo "-- lane=$( [ "$lane" = "$L" ] && echo live || echo clean-clone )"
  python3 -B "$L/.ufo/waves/round-89/c1/knowledge-meter.py" --lane "$lane" --measure-rev b9fcf005 --work "$S/w" | sed 's/^/r89-meter /'
  python3 -B "$M" --lane "$lane" --measure-rev b9fcf005 --work "$S/w" | sed 's/^/r90-meter /'
done
