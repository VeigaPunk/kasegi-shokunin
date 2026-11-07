#!/usr/bin/env bash
# Round-87 C1 EXTENDED controls: limb-isolating fixtures for the frozen counter
# .ufo/waves/round-87/c1/knowledge-meter.py (r87). The frozen battery
# (controls/c1-controls-r87.sh) fails 3 limbs together (M1/M2/M3) and 2 more
# together (M4/M5); only M6 is isolated. Each control below fails EXACTLY ONE
# limb (or fails only M4+M5, whose M5 line is the `not m4bad` coupling).
#
# Usage: MutC1Counter-controls-ext.sh SCRATCH_DIR
# Re-runnable; writes only under SCRATCH_DIR and read-only copies nothing.
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$L/.ufo/waves/round-87
METER=$W/c1/knowledge-meter.py
MAP=$W/c1/repair-map.json
APPLY=$W/c1/apply-map.py
B=cd1f568a6be2656b5f5dc479eb90ef99b91131b5
HERE=$(cd "$(dirname "$0")" && pwd)
S=${1:?scratch}; mkdir -p "$S"; S=$(cd "$S" && pwd)
sha() { sha256sum "$1" | cut -d' ' -f1; }
MSHA=$(sha "$MAP")
echo "counter_sha256=$(sha "$METER") map_sha256=$MSHA base=$B host=$S"
python3 -B "$HERE/MutC1Counter-mkmut.py" "$METER" "$HERE/MutC1Counter-mutants.tsv" "$S/mut" || exit 2

meter() { # counter lane baserev map target msha tag
  local out rc
  out=$(python3 -B "$1" --lane "$2" --base-rev "$3" --map "$4" --target "$5" \
        --map-sha256 "$6" --work "$S/w/$7")
  rc=$?
  printf '%s\n' "$out" | grep -E '^LIMB|^KNOWLEDGE-METER'
  echo "rc=$rc"
}
verdict() { # label pristine_file pristine_lane pristine_rev pristine_map pristine_target pristine_sha mut...
  local label=$1 pf=$2 lane=$3 rev=$4 map=$5 tgt=$6 msh=$7; shift 7
  echo "===== CONTROL $label (lane=$lane map=$map target=$tgt)"
  meter "$pf" "$lane" "$rev" "$map" "$tgt" "$msh" "$label-pristine"
  local m
  for m in "$@"; do
    echo "----- mutant $m"
    meter "$S/mut/$m.py" "$lane" "$rev" "$map" "$tgt" "$msh" "$label-$m"
  done
}

fresh() { rm -rf "$S/t/$1"; git clone -q --shared "$L" "$S/t/$1"; git -C "$S/t/$1" checkout -q "$B"; }
mkdir -p "$S/t" "$S/w" "$S/maps"
fresh pos; python3 -B "$APPLY" --root "$S/t/pos" --map "$MAP" >/dev/null
cp -a "$S/t/pos" "$S/t/s041"
python3 - "$MAP" "$S/maps/s041.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1])); m["S041.txt:1868"] = "corpus/source-snapshots/round-26/S041.txt:1868"
json.dump(m, open(sys.argv[2], "w"), indent=1, sort_keys=True)
PY
python3 -B "$APPLY" --root "$S/t/s041" --map "$S/maps/s041.json" >/dev/null
cp -a "$S/t/pos" "$S/t/nofile"; rm "$S/t/nofile/corpus/source-snapshots/round-25/S040.txt"
cp -a "$S/t/pos" "$S/t/ext"; printf '# extra\n\nprose only, no backticked tokens here.\n' > "$S/t/ext/corpus/knowledge/extra.md"
cp -a "$S/t/pos" "$S/t/lc"; printf '\nextra prose line, no backticked tokens.\n' >> "$S/t/lc/corpus/knowledge/claim-gates.md"

mkfix() { # tag knowledge-line count extra-cmd -> echoes fixture dir
  local D; D=$(mktemp -d -p "$S" "fix-$1-XXXXXX")
  git -C "$D" init -q
  [ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "TOPLEVEL-MISMATCH" >&2; return 1; }
  mkdir -p "$D/corpus/knowledge" "$D/corpus/source-snapshots/round-68" "$D/corpus/instruments"
  cp "$L/corpus/instruments/resolve.py" "$D/corpus/instruments/"
  { for i in $(seq 1 "$3"); do printf 'line%s\n' "$i"; done; } > "$D/corpus/source-snapshots/round-68/S102.txt"
  printf '%s\n' "$2" > "$D/corpus/knowledge/fix.md"
  [ "$4" = none ] || { mkdir -p "$D/corpus/sources"; cp "$D/corpus/source-snapshots/round-68/S102.txt" "$D/corpus/sources/S102.txt"; }
  git -C "$D" add -A; git -C "$D" -c user.email=x@x -c user.name=x commit -qm base
  echo "$D"
}
mkmap() { printf '%s\n' "$2" > "$S/maps/$1"; }
mkmap map1.json '{"S102.txt:1":"corpus/source-snapshots/round-68/S102.txt:1"}'
mkmap map3.json '{"S102.txt:3":"corpus/source-snapshots/round-68/S102.txt:3"}'
mkmap map4.json '{"S102.txt:4":"corpus/source-snapshots/round-68/S102.txt:4"}'
mkmap mapF.json '{"S020.txt":"corpus/source-snapshots/round-40/S020.txt"}'
M1SHA=$(sha "$S/maps/map1.json"); M3SHA=$(sha "$S/maps/map3.json")
M4SHA=$(sha "$S/maps/map4.json"); MFSHA=$(sha "$S/maps/mapF.json"); M41SHA=$(sha "$S/maps/s041.json")

# --- real-tree controls -----------------------------------------------------
verdict target-degenerate   "$METER" "$S/t/pos" "$B" "$MAP" 596/1720 "$MSHA" \
        M20-M1-compare-relax M21-M1-always-pass
verdict s041-own-rate       "$METER" "$S/t/s041" "$B" "$S/maps/s041.json" 679/1719 "$M41SHA" \
        M03-uniqueness-weaken
verdict nofile-own-rate     "$METER" "$S/t/nofile" "$B" "$MAP" 677/1719 "$MSHA" \
        M06-internal-clause-drop
verdict extra-file          "$METER" "$S/t/ext" "$B" "$MAP" 678/1719 "$MSHA" \
        M16-M3-samefiles-always
verdict appended-line       "$METER" "$S/t/lc" "$B" "$MAP" 678/1719 "$MSHA" \
        M15-M3-linecount-drop

# --- fixture controls (each fixture's base rev is its pre-apply commit) ------
D4=$(mkfix out '# fix out
cite `S102.txt:4` here.' 3 none); B4=$(git -C "$D4" rev-parse HEAD)
python3 -B "$APPLY" --root "$D4" --map "$S/maps/map4.json" >/dev/null
verdict range-out "$METER" "$D4" "$B4" "$S/maps/map4.json" 1/1 "$M4SHA" M17-M5-bound-loose

D3=$(mkfix edge '# fix edge
cite `S102.txt:3` here.' 3 none); B3=$(git -C "$D3" rev-parse HEAD)
python3 -B "$APPLY" --root "$D3" --map "$S/maps/map3.json" >/dev/null
verdict range-edge "$METER" "$D3" "$B3" "$S/maps/map3.json" 1/1 "$M3SHA" M18-M5-bound-tighten

DD=$(mkfix dupbase '# fix dup
cite `S102.txt:1` here.' 3 extra); BD=$(git -C "$DD" rev-parse HEAD)
python3 -B "$APPLY" --root "$DD" --map "$S/maps/map1.json" >/dev/null
verdict dup-basename "$METER" "$DD" "$BD" "$S/maps/map1.json" 1/1 "$M1SHA" M02-bybase-scope-widen-corpus

DC=$(mkfix notgone '# fix ng
cite `S102.txt:1` here.' 3 none); BC=$(git -C "$DC" rev-parse HEAD)
python3 -B "$APPLY" --root "$DC" --map "$S/maps/map1.json" >/dev/null
MIR=$(mktemp -d -p "$S" mirror-XXXXXX); printf 'line1\n' > "$MIR/S102.txt"
echo "===== CONTROL not-gone (lane=$DC KASEGI_MIRROR=$MIR target=1/1)"
KASEGI_MIRROR="$MIR" meter "$METER" "$DC" "$BC" "$S/maps/map1.json" 1/1 "$M1SHA" "not-gone-pristine"
echo "----- mutant M05-gone-clause-drop"
KASEGI_MIRROR="$MIR" meter "$S/mut/M05-gone-clause-drop.py" "$DC" "$BC" "$S/maps/map1.json" 1/1 "$M1SHA" "not-gone-M05"

DF=$(mktemp -d -p "$S" fix-quoted-XXXXXX); git -C "$DF" init -q
[ "$(git -C "$DF" rev-parse --show-toplevel)" = "$DF" ] || echo "TOPLEVEL-MISMATCH" >&2
mkdir -p "$DF/corpus/knowledge" "$DF/corpus/source-snapshots/round-40" "$DF/corpus/instruments"
cp "$L/corpus/instruments/resolve.py" "$DF/corpus/instruments/"
printf 'aa\nbb\ncc\n' > "$DF/corpus/source-snapshots/round-40/S020.txt"
printf '# fix F\nquoted manifest path `S020.txt` appears here.\n' > "$DF/corpus/knowledge/fix.md"
git -C "$DF" add -A; git -C "$DF" -c user.email=x@x -c user.name=x commit -qm base
BF=$(git -C "$DF" rev-parse HEAD)
python3 -B "$APPLY" --root "$DF" --map "$S/maps/mapF.json" >/dev/null
verdict quoted-key "$METER" "$DF" "$BF" "$S/maps/mapF.json" 1/1 "$MFSHA" M07-QUOTED-empty

DE=$(mkfix dupkey '# fix E
cite `S102.txt:1` and again `S102.txt:1` on one line.' 3 none)
BE=$(git -C "$DE" rev-parse HEAD)
python3 -B "$APPLY" --root "$DE" --map "$S/maps/map1.json" >/dev/null
verdict dup-key-line "$METER" "$DE" "$BE" "$S/maps/map1.json" 1/1 "$M1SHA" M13-M3-replace-first

echo "counter_sha256_after=$(sha "$METER")"
