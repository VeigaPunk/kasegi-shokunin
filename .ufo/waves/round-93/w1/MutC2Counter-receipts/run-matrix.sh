#!/bin/sh
# Run the frozen round-93 C2 counter against a clone variant (seat MutC2Counter).
# usage: run-matrix.sh CLONE TAG
# pinned  = --instrument-sha256 7d9d.. --gate-sha256 8b6f..
# unpinned= no pins
set -u
CLONE=$1
TAG=$2
R=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-93/w1/MutC2Counter-receipts
CTR="$CLONE/.ufo/waves/round-93/c2/capability-check.py"
REV=$(git -C "$CLONE" rev-parse HEAD)
W=/fast/scratch/hyaku/kasegi-r93/MutC2Counter/w/$TAG
mkdir -p "$W" "$R"
for SEED in 1 9191; do
  for MODE in pinned unpinned; do
    OUT="$R/$TAG-$MODE-seed$SEED.txt"
    if [ "$MODE" = pinned ]; then
      TMPDIR="$W" python3 -B "$CTR" --lane "$CLONE" --rev "$REV" --work "$W" --seed "$SEED" \
        --instrument-sha256 7d9d7309d5a5eddde59dbbb49767d71f43ec78667f1c3aa05bb1c76a45f683c5 \
        --gate-sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6 >"$OUT" 2>&1
    else
      TMPDIR="$W" python3 -B "$CTR" --lane "$CLONE" --rev "$REV" --work "$W" --seed "$SEED" >"$OUT" 2>&1
    fi
    RC=$?
    echo "$TAG $MODE seed=$SEED rc=$RC rev=$REV $(tail -n 1 "$OUT")"
  done
done
