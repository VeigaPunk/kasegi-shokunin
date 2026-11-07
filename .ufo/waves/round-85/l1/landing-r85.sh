#!/usr/bin/env bash
# Round-85 landing receipt: every C1/C2 predicate measured over a checkout of
# the named landing commit. C1 needs a checkout WITH .git (census-of-record
# root; a git-archive extract classifies the SKILL token `.git` GONE), so the
# checkout is `git clone --shared` of the lane at <commit>, detached.
# Usage: landing-r85.sh <landing-commit> <scratch>
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
C=${1:?commit}; S=${2:?scratch}
FREEZE=4a2d34f203519a87078f21a896dc8679137ff675
BASE=bc722e540c93b48ff159454b65a0f9f4630db1ed
mkdir -p "$S"; X="$S/clone"; rm -rf "$X"
git clone -q --shared --no-checkout "$L" "$X" && git -C "$X" -c advice.detachedHead=false checkout -q "$C"
test "$(git -C "$X" rev-parse --show-toplevel)" = "$X" || { echo "clone root mismatch"; exit 2; }
echo "LANDING commit=$(git -C "$X" rev-parse HEAD) freeze=$FREEZE base=$BASE utc=$(date -u +%FT%TZ)"
cd "$X"
echo "== P2 frozen instrument bytes"
python3 - <<'P'
import json,hashlib
c=json.load(open('.ufo/waves/round-85/claims.json'))
for p,h in c['instruments'].items():
    g=hashlib.sha256(open(p,'rb').read()).hexdigest(); print(p, 'OK' if g==h else 'MISMATCH '+g)
P
echo "== C1 P1 counting command (clone with .git)"
git show $BASE:SKILL.md > "$S/base.md"
python3 -B .ufo/waves/round-85/c1/skill-meter.py --lane . --base "$S/base.md" --after SKILL.md --map .ufo/waves/round-85/c1/repair-map.json --target 167/732 --map-sha256 b575f147835d55fcb810fe946825c0cfd36e51094341497e00f0d98db5ae1944 --work "$S/w"; echo "rc=$?"
echo "== C1 P3 SKILL.md diff freeze..landing (changed lines)"
git diff --numstat $FREEZE "$C" -- SKILL.md
echo "== C1 P4 density"
python3 -B corpus/instruments/density.py "$S/base.md" --label base | grep -E "mean dens|Total path"
python3 -B corpus/instruments/density.py SKILL.md --label landing | grep -E "mean dens|Total path"
echo "== C2 P1 counting command"
python3 -B .ufo/waves/round-85/c2/e2e-check.py --lane . --pkg corpus/practice/curl-h1-1913733; echo "rc=$?"
echo "== C2 P2 gate"
python3 -B corpus/instruments/claim-package-check.py corpus/practice/curl-h1-1913733; echo "rc=$?"
echo "== C2 P3 source-recheck"
for s in S119 S120 S121; do python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-85/manifest.json --source $s; echo "rc=$?"; done
echo "== C2 P4 registry diff freeze..landing"
git diff -U0 $FREEZE "$C" -- corpus/SOURCES.md | grep -E '^[-+]\| S[0-9]+' | cut -c1-12
echo "registry=$(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md)"
echo "== C2 P6 SHONEN box 2"
grep -n -A1 'end-to-end domain task' SHONEN.md
echo "== C2 P5 census (run in the lane: the census reads --root)"
