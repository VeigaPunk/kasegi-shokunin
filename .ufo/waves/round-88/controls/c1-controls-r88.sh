#!/usr/bin/env bash
# Round-88 C1 pre-freeze controls over the frozen counter c1/knowledge-meter.py (r88 successor).
# Every control runs in its own `git clone --shared` of the base under SCRATCH.
# Usage: c1-controls-r88.sh SCRATCH_DIR
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$L/.ufo/waves/round-88
B=6beead9148945fa695cf3139e8fc9d8e91cc5fd0
T=742/1743
S=${1:?scratch}; mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
MAP=$W/c1/repair-map.json
MSHA=$(sha256sum "$MAP" | cut -d' ' -f1)
echo "counter_sha256=$(sha256sum $W/c1/knowledge-meter.py | cut -d' ' -f1) map_sha256=$MSHA resolve_sha256=$(sha256sum $L/corpus/instruments/resolve.py | cut -d' ' -f1) base=$B target=$T"
fresh() { rm -rf "$S/$1"; git clone -q --shared "$L" "$S/$1" && git -C "$S/$1" checkout -q "$B"; }
meter() { python3 -B $W/c1/knowledge-meter.py --lane "$1" --base-rev $B --map "${2:-$MAP}" --target $T --map-sha256 "${3:-$MSHA}" --work "$S/w"; echo "rc=$?"; }
rehash() { sha256sum "$1" | cut -d' ' -f1; }
forge() { python3 - "$MAP" "$S/$1.json" "$2" "$3" <<'PY'
import json, sys
m = json.load(open(sys.argv[1])); m[sys.argv[3]] = sys.argv[4]
json.dump(m, open(sys.argv[2], "w"), indent=1, sort_keys=True)
PY
fresh "$1"; python3 -B $W/c1/apply-map.py --root "$S/$1" --map "$S/$1.json" >/dev/null; }
fresh dn; echo "== control do-nothing: base knowledge scope as after (expected fail M1/M2/M3)"; meter "$S/dn"
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
forge drift "mission-control.md:41-45" "corpus/knowledge/mission-control.md:41-45"
echo "== control drift-forge: excluded drifted anchor mission-control.md:41-45 added and applied (expected fail M8 and M1)"; meter "$S/drift" "$S/drift.json" "$(rehash $S/drift.json)"
forge notentry "SOURCES.md" "corpus/SOURCES.md"
echo "== control not-entry-forge: SOURCES.md -> corpus/SOURCES.md added and applied (expected fail M4 and M1)"; meter "$S/notentry" "$S/notentry.json" "$(rehash $S/notentry.json)"
forge ufocopy "claim-gates.md:32-33" ".ufo/waves/round-25/c1-controls/base/corpus/knowledge/claim-gates.md:32-33"
echo "== control ufo-copy: one key repointed to a .ufo fixture copy (expected fail M4)"; meter "$S/ufocopy" "$S/ufocopy.json" "$(rehash $S/ufocopy.json)"
echo "== control map-sha: positive tree, frozen map, wrong sha (expected fail M6)"; meter "$S/pos" "$MAP" 0000000000000000000000000000000000000000000000000000000000000000
