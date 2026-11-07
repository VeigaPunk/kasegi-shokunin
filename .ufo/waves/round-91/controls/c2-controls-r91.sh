#!/usr/bin/env bash
# round-91 C2 pre-freeze controls. Each variant is a commit in a shared scratch clone at
# BASE: the instrument file replaced by the variant and the SCORECARD capability row by
# the frozen candidate row. Forgeries run WITHOUT --instrument-sha256, so only the
# behavioural limbs (K2-K8) can reject them; the candidate runs with and without the pin.
# Usage: c2-controls-r91.sh LANE SCRATCH
set -u
L=$1; S=$2; W=$L/.ufo/waves/round-91
BASE=bb4309fffbe9bf98153a2933af72c8f2c3f4b5b1
ISHA=89e283c6423216917c8ae31e1f72239f56ebcb842bda72f7bad4b2f36dc526d7
GSHA=8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6
mkdir -p "$S"; C=$S/c2clone; rm -rf "$C" "$S/forg"
git clone -q --shared "$L" "$C"
[ "$(git -C "$C" rev-parse --show-toplevel)" = "$C" ] || { echo "fixture toplevel mismatch"; exit 2; }
python3 -B $W/controls/c2-forgeries.py $W/c2/candidate/capture-secret-scan.py "$S/forg" || exit 2
ROW=$(cat $W/c2/candidate/scorecard-row.txt)
variant() { # name, instrument file ('' = keep base)
  git -C "$C" checkout -q --detach $BASE
  [ -n "$2" ] && cp "$2" "$C/corpus/instruments/capture-secret-scan.py"
  python3 - "$C/SCORECARD.md" "$ROW" <<'EOF'
import sys
p, row = sys.argv[1], sys.argv[2]
lines = open(p, encoding="utf-8").read().split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("| capture-secret-scan |")]
assert len(idx) == 1
lines[idx[0]] = row
open(p, "w", encoding="utf-8").write("\n".join(lines))
EOF
  git -C "$C" -c user.name=fixture -c user.email=fixture@invalid commit -q -am "$1"
  git -C "$C" rev-parse HEAD
}
run() { # name, rev, extra args...
  local n=$1 r=$2; shift 2
  echo "== control $n (rev=$r $*)"
  python3 -B $W/c2/capability-check.py --lane "$C" --rev "$r" --work "$S/w" --seed 9191 "$@" | grep -E '^(LIMB|CAPABILITY-CHECK)'
}
R=$(variant candidate $W/c2/candidate/capture-secret-scan.py)
run candidate-pinned $R --instrument-sha256 $ISHA --gate-sha256 $GSHA
run candidate-unpinned $R
run no-work-base-instrument "$(variant no-work '')"
for f in "$S"/forg/F*.py; do
  n=$(basename "$f" .py)
  run "$n" "$(variant "$n" "$f")"
done
rm -rf "$C" "$S/w" "$S/forg"
