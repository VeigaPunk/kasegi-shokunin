#!/usr/bin/env bash
# Round-86 C1 pre-freeze controls over the frozen counter c1/knowledge-meter.py.
# Every control runs in its own `git clone --shared` of the base under SCRATCH
# (the census-of-record root: a checkout with .git whose parent holds no MISSION.md).
# Usage: c1-controls-r86.sh SCRATCH_DIR
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$L/.ufo/waves/round-86
B=d7296645c2cd9f631329fa8e2f38328a4c9c89a5
T=596/1716
S=${1:?scratch}; mkdir -p "$S"
MAP=$W/c1/repair-map.json
MSHA=$(sha256sum "$MAP" | cut -d' ' -f1)
echo "counter_sha256=$(sha256sum $W/c1/knowledge-meter.py | cut -d' ' -f1) map_sha256=$MSHA resolve_sha256=$(sha256sum $L/corpus/instruments/resolve.py | cut -d' ' -f1) base=$B target=$T"
fresh() { rm -rf "$S/$1"; git clone -q --shared "$L" "$S/$1" && git -C "$S/$1" checkout -q "$B"; }
meter() { python3 -B $W/c1/knowledge-meter.py --lane "$1" --base-rev $B --map "${2:-$MAP}" --target $T --map-sha256 "${3:-$MSHA}" --work "$S/w"; echo "rc=$?"; }
fresh dn; echo "== control do-nothing: base knowledge scope as after (expected fail)"; meter "$S/dn"
fresh pos; python3 -B $W/c1/apply-map.py --root "$S/pos" --map "$MAP" >/dev/null
echo "== control positive: frozen map applied (expected pass)"; meter "$S/pos"
fresh half; python3 - "$MAP" "$S/half.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1])); k = sorted(m)[: len(m) // 2]
json.dump({x: m[x] for x in k}, open(sys.argv[2], "w"))
PY
python3 -B $W/c1/apply-map.py --root "$S/half" --map "$S/half.json" >/dev/null
echo "== control partial: half the map applied, frozen map scored (expected fail)"; meter "$S/half"
fresh decite; python3 - "$MAP" "$S/decite" <<'PY'
import json, os, sys
m = json.load(open(sys.argv[1])); d = os.path.join(sys.argv[2], "corpus", "knowledge")
for fn in sorted(os.listdir(d)):
    p = os.path.join(d, fn); t = open(p).read(); n = t
    for k in m:
        n = n.replace("`%s`" % k, k)
    if n != t: open(p, "w").write(n)
PY
echo "== control de-cite: the 203 GONE tokens un-backticked (expected fail)"; meter "$S/decite"
fresh pad; cp -r "$S/pos/corpus/knowledge/." "$S/pad/corpus/knowledge/"; printf '\n`corpus/SOURCES.md`\n`corpus/instruments/resolve.py`\n' >> "$S/pad/corpus/knowledge/claim-gates.md"
echo "== control pad: map applied plus 2 extra resolving cites (expected fail)"; meter "$S/pad"
python3 - "$MAP" "$S/wrongfile.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
k = "S071.txt:117"; assert k in m
m[k] = "corpus/source-snapshots/round-44/S069.txt:117"
json.dump(m, open(sys.argv[2], "w"), indent=1, sort_keys=True)
PY
fresh wrong; python3 -B $W/c1/apply-map.py --root "$S/wrong" --map "$S/wrongfile.json" >/dev/null
echo "== control wrong-file: one key repointed to another snapshot, map re-hashed (expected fail M4)"; meter "$S/wrong" "$S/wrongfile.json" "$(sha256sum $S/wrongfile.json | cut -d' ' -f1)"
echo "== control map-sha: positive tree, frozen map, wrong sha (expected fail M6)"; meter "$S/pos" "$MAP" 0000000000000000000000000000000000000000000000000000000000000000
