#!/usr/bin/env bash
# Round-89 C1 pre-freeze controls over the frozen counter c1/knowledge-meter.py (r89 successor).
# Each control: a `git clone --shared` of the base under SCRATCH, an edit, one fixture commit
# (identity fixture@invalid, toplevel asserted), then the counter at --after-rev HEAD of the clone.
# Usage: c1-controls-r89.sh SCRATCH_DIR
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$L/.ufo/waves/round-89
B=090a46f89932324787e00ca20b1007f893934c9a
T=785/1797
MAP=$W/c1/repair-map.json
LAB=$W/c1/labels.tsv
S=${1:?scratch}; mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
MSHA=$(sha256sum $MAP | cut -d' ' -f1); LSHA=$(sha256sum $LAB | cut -d' ' -f1)
echo "counter_sha256=$(sha256sum $W/c1/knowledge-meter.py | cut -d' ' -f1) apply_sha256=$(sha256sum $W/c1/apply-map.py | cut -d' ' -f1) map_sha256=$MSHA labels_sha256=$LSHA base=$B target=$T"
clone() { local d="$S/$1"; rm -rf "$d"; git clone -q --shared "$L" "$d" && git -C "$d" checkout -q "$B"
  [ "$(git -C "$d" rev-parse --show-toplevel)" = "$d" ] || { echo "toplevel mismatch"; exit 2; }; }
commit() { git -C "$S/$1" -c user.name=fixture -c user.email=fixture@invalid commit -qam "control $1"; }
meter() { local d=$1; shift; python3 -B $W/c1/knowledge-meter.py --lane "$S/$d" --base-rev $B --work "$S/w" --target $T "$@"; echo "rc=$?"; }
# forged map/labels: the five WRONG keys keep their own (wrong) anchors, prefix only
python3 - "$MAP" "$LAB" "$S/forged-map.json" "$S/forged-labels.tsv" <<'PY'
import json, sys
m = json.load(open(sys.argv[1])); fm = {}
for k, v in m.items():
    fm[k] = "corpus/knowledge/" + k
json.dump(fm, open(sys.argv[3], "w"), indent=1)
out = []
for ln in open(sys.argv[2]):
    if ln.startswith("#") or not ln.strip():
        out.append(ln); continue
    k, v, n, c = ln.rstrip("\n").split("\t")
    out.append("%s\t%s\t%s\t%s\n" % (k, "corpus/knowledge/" + k, n, c))
open(sys.argv[4], "w").write("".join(out))
PY
# label-line forgery: the first row points at the next review line
python3 - "$LAB" "$S/shifted-labels.tsv" <<'PY'
import sys
out, done = [], False
for ln in open(sys.argv[1]):
    if not done and ln.strip() and not ln.startswith("#"):
        k, v, n, c = ln.rstrip("\n").split("\t"); ln = "%s\t%s\t%d\t%s\n" % (k, v, int(n) + 1, c); done = True
    out.append(ln)
open(sys.argv[2], "w").write("".join(out))
PY
echo "== control do-nothing: after-rev = base (expected fail M1, M2, M3)"
clone nothing; meter nothing --after-rev $B --map $MAP --labels $LAB --map-sha256 $MSHA --labels-sha256 $LSHA
echo "== control positive: frozen map applied and committed (expected pass)"
clone pos; python3 -B $W/c1/apply-map.py --root "$S/pos" --map $MAP; commit pos
meter pos --after-rev HEAD --map $MAP --labels $LAB --map-sha256 $MSHA --labels-sha256 $LSHA
echo "== control working-tree-only: frozen map applied, not committed (r88 D1; expected fail M1, M2, M3)"
clone wt; python3 -B $W/c1/apply-map.py --root "$S/wt" --map $MAP
meter wt --after-rev HEAD --map $MAP --labels $LAB --map-sha256 $MSHA --labels-sha256 $LSHA
echo "== control prefix-only forgery: WRONG keys keep their wrong anchors, map+labels forged consistently, unpinned (expected fail M9 on the 5 WRONG keys)"
clone prefix; python3 -B $W/c1/apply-map.py --root "$S/prefix" --map "$S/forged-map.json"; commit prefix
meter prefix --after-rev HEAD --map "$S/forged-map.json" --labels "$S/forged-labels.tsv"
echo "== control prefix-only forgery, pinned (expected fail M6, M7, M9; M1 as measured)"
meter prefix --after-rev HEAD --map "$S/forged-map.json" --labels "$S/forged-labels.tsv" --map-sha256 $MSHA --labels-sha256 $LSHA
echo "== control shifted-label-line: first labels row points one review line down, unpinned (expected fail M9)"
meter pos --after-rev HEAD --map $MAP --labels "$S/shifted-labels.tsv"
echo "== control extra-repoint: frozen map plus an unlabelled prefix repoint of mission-control.md:20-21 (expected fail M1, M2, M3)"
clone extra; python3 -B $W/c1/apply-map.py --root "$S/extra" --map $MAP
sed -i 's/`mission-control.md:20-21`/`corpus\/knowledge\/mission-control.md:20-21`/' "$S/extra/corpus/knowledge/triage-thresholds.md"; commit extra
meter extra --after-rev HEAD --map $MAP --labels $LAB --map-sha256 $MSHA --labels-sha256 $LSHA
echo "== control cited-entry-shift: frozen map applied and a line inserted at the top of claim-gates.md (expected fail M3; M5 may pass)"
clone shift; python3 -B $W/c1/apply-map.py --root "$S/shift" --map $MAP
sed -i '1i <!-- shifted -->' "$S/shift/corpus/knowledge/claim-gates.md"; commit shift
meter shift --after-rev HEAD --map $MAP --labels $LAB --map-sha256 $MSHA --labels-sha256 $LSHA
echo "== control out-of-range: map+labels re-anchor claim-gates.md:66-67 to :81-850, unpinned (expected fail M5 and M9)"
python3 - "$MAP" "$LAB" "$S/oor-map.json" "$S/oor-labels.tsv" <<'PY'
import json, sys
m = json.load(open(sys.argv[1])); m["claim-gates.md:66-67"] = "corpus/knowledge/claim-gates.md:81-850"
json.dump(m, open(sys.argv[3], "w"), indent=1)
open(sys.argv[4], "w").write(open(sys.argv[2]).read().replace("claim-gates.md:81-85\t", "claim-gates.md:81-850\t"))
PY
clone oor; python3 -B $W/c1/apply-map.py --root "$S/oor" --map "$S/oor-map.json"; commit oor
meter oor --after-rev HEAD --map "$S/oor-map.json" --labels "$S/oor-labels.tsv"
