#!/usr/bin/env bash
# Round-87 C1 pre-freeze controls over the frozen counter c1/knowledge-meter.py (r87 successor).
# Every control runs in its own `git clone --shared` of the base under SCRATCH
# (the census-of-record root: a checkout with .git whose parent holds no MISSION.md).
# Usage: c1-controls-r87.sh SCRATCH_DIR
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$L/.ufo/waves/round-87
B=cd1f568a6be2656b5f5dc479eb90ef99b91131b5
T=678/1719
S=${1:?scratch}; mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
MAP=$W/c1/repair-map.json
MSHA=$(sha256sum "$MAP" | cut -d' ' -f1)
echo "counter_sha256=$(sha256sum $W/c1/knowledge-meter.py | cut -d' ' -f1) map_sha256=$MSHA resolve_sha256=$(sha256sum $L/corpus/instruments/resolve.py | cut -d' ' -f1) base=$B target=$T"
fresh() { rm -rf "$S/$1"; git clone -q --shared "$L" "$S/$1" && git -C "$S/$1" checkout -q "$B"; }
meter() { python3 -B $W/c1/knowledge-meter.py --lane "$1" --base-rev $B --map "${2:-$MAP}" --target $T --map-sha256 "${3:-$MSHA}" --work "$S/w"; echo "rc=$?"; }
rehash() { sha256sum "$1" | cut -d' ' -f1; }
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
fresh pad; cp -r "$S/pos/corpus/knowledge/." "$S/pad/corpus/knowledge/"; printf '\n`corpus/SOURCES.md`\n`corpus/instruments/resolve.py`\n' >> "$S/pad/corpus/knowledge/claim-gates.md"
echo "== control pad: map applied plus 2 extra resolving cites (expected fail)"; meter "$S/pad"
python3 - "$MAP" "$S/ufocopy.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
k = "S102.txt:101"; assert k in m
m[k] = ".ufo/waves/round-68/w1/ScoutS102/S102.txt:101"
json.dump(m, open(sys.argv[2], "w"), indent=1, sort_keys=True)
PY
fresh ufo; python3 -B $W/c1/apply-map.py --root "$S/ufo" --map "$S/ufocopy.json" >/dev/null
echo "== control ufo-copy: one key repointed to the .ufo fixture copy (expected fail M4)"; meter "$S/ufo" "$S/ufocopy.json" "$(rehash $S/ufocopy.json)"
python3 - "$MAP" "$S/s041.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
m["S041.txt:1868"] = "corpus/source-snapshots/round-26/S041.txt:1868"
json.dump(m, open(sys.argv[2], "w"), indent=1, sort_keys=True)
PY
fresh s041; python3 -B $W/c1/apply-map.py --root "$S/s041" --map "$S/s041.json" >/dev/null
echo "== control S041-forge: ambiguous 3-capture key added and applied (expected fail M4 and M1)"; meter "$S/s041" "$S/s041.json" "$(rehash $S/s041.json)"
python3 - "$MAP" "$S/quoted.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
m["S020.txt"] = "corpus/source-snapshots/round-40/S020.txt"
json.dump(m, open(sys.argv[2], "w"), indent=1, sort_keys=True)
PY
fresh quoted; python3 -B $W/c1/apply-map.py --root "$S/quoted" --map "$S/quoted.json" >/dev/null
echo "== control quoted-forge: r86 quoted manifest-field key re-added and applied (expected fail M7)"; meter "$S/quoted" "$S/quoted.json" "$(rehash $S/quoted.json)"
echo "== control map-sha: positive tree, frozen map, wrong sha (expected fail M6)"; meter "$S/pos" "$MAP" 0000000000000000000000000000000000000000000000000000000000000000
