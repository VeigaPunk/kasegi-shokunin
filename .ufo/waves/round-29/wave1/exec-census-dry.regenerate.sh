#!/usr/bin/env bash
# Rebuild the ExecCensusDry scratch-mirror tree (round-29 wave-1, seat
# ExecCensusDry-2) without committing a 508 KB corpus copy (R14).
#
# The tree is: git archive <rev> of corpus/SOURCES.md + corpus/knowledge/,
# overwritten by two named mutation assets (the S043/S044/S045 append block and
# the F13 entry draft), then verified against per-file sha256 digests.
#
# Usage: bash exec-census-dry.regenerate.sh <target-dir>
# The tree must be byte-identical to `ExecCensusDry.digests.txt` or the script
# exits 1 with the first mismatch.
set -euo pipefail

LANE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
SRC_REV="46e07f6" # lane HEAD at measurement (2026-10-25)
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MUTATIONS="$HERE/ExecCensusDry.mutations"
DIGESTS="$HERE/ExecCensusDry.digests.txt"

TARGET="${1:-}"
if [ -z "$TARGET" ]; then
  echo "usage: bash exec-census-dry.regenerate.sh <target-dir>" >&2
  exit 2
fi
mkdir -p "$TARGET"

# 1. Base corpus at the pinned revision (knowledge dir + SOURCES.md).
git -C "$LANE_ROOT" archive --format=tar "$SRC_REV" corpus/SOURCES.md corpus/knowledge | tar -x -C "$TARGET"

# 2. Named mutations.
cp "$MUTATIONS/SOURCES.md" "$TARGET/corpus/SOURCES.md"
mkdir -p "$TARGET/corpus/knowledge"
cp "$MUTATIONS/program-severity-ladders-and-reward-scales.md" "$TARGET/corpus/knowledge/program-severity-ladders-and-reward-scales.md"

# 3. Verify every file against the committed digests (content-addressed).
FAIL=0
while read -r want path; do
  got="$(cd "$TARGET" && sha256sum "$path" | awk '{print $1}')"
  if [ "$got" != "$want" ]; then
    echo "MISMATCH $path want=$want got=$got" >&2
    FAIL=1
  fi
done < <(grep -E '^[0-9a-f]{64}  ' "$DIGESTS")

if [ "$FAIL" = 1 ]; then
  echo "regenerate: FAIL (see mismatches above)" >&2
  exit 1
fi
echo "regenerate: OK — 42 files match ExecCensusDry.digests.txt (tree digest ad8e5a1e669d984844a207bdf80d21bd9e591b566ae47a4b37d6d95f827501ed)"
