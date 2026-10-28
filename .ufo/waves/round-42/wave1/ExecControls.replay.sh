#!/usr/bin/env bash
# replay.sh — rebuild the round-42 C2 junk twin on a scratch copy of the lane
# corpus and re-run the three named instruments against it.
#
# Usage: bash replay.sh <scratch-root> [<lane-repo>]
#   scratch-root  a directory the caller owns (created if absent); everything this
#                 script writes lives under it and is removed on exit
#   lane-repo     the lane to copy (default: the kasegi lane)
#
# Exit 0 when the twin is rejected by all three named instruments (each exits
# nonzero), 1 otherwise.  The script never writes to the lane repo and never runs
# a mutating git/jj command: the lane tree is copied with tar.
set -u

SCRATCH="${1:?usage: replay.sh <scratch-root> [<lane-repo>]}"
LANE="${2:-/home/vgpnk/Projects/shokunin/kasegi-shokunin}"
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh

case "$SCRATCH" in
  /|""|"/"|"/etc"|"/usr"|"/var"|"/home"|"/root"|"/tmp") echo "refusing scratch root: $SCRATCH" >&2; exit 2 ;;
esac

mkdir -p "$SCRATCH" || exit 2
TREE="$SCRATCH/junk-twin"
rm -rf "$TREE"
mkdir -p "$TREE"
tar -C "$LANE" --exclude=.git --exclude=.jj -cf - . | tar -C "$TREE" -xf -

# retarget every landed recheck: line to this tree's own root, so the audit's
# cdroot limb measures the tree under test and not the live lane.
LANE_CD="cd $LANE &&"
for f in "$TREE"/corpus/knowledge/*.md; do
  [ -f "$f" ] || continue
  sed -i "s|$LANE_CD|cd $TREE \&\&|" "$f"
done

# 1. the fabricated registry row (mined; used-by names a knowledge file that
#    does not exist) -- inserted inside the ## Registry section of SOURCES.md
python3 - "$TREE" <<'PY'
import sys
tree = sys.argv[1]
row = ("| S999 | OSV schema (fabricated twin - never fetched) - "
       "https://ossf.github.io/osv-schema/ | spec | A | Fabricated twin scope: a "
       "machine-readable vulnerability record format claimed as mined without a "
       "capture | Fabricated twin anchor: none | Fabricated twin teaches: nothing "
       "- this row exists only to be rejected | mined | 2026-10-28 | 180d | "
       "corpus/knowledge/junk-f25-osv-schema.md |\n")
p = tree + "/corpus/SOURCES.md"
lines = open(p, encoding="utf-8").readlines()
out, done = [], False
for line in lines:
    out.append(line)
    if not done and line.startswith("| S063 "):
        out.append(row)
        done = True
assert done, "S063 anchor row not found"
open(p, "w", encoding="utf-8").writelines(out)
PY

# 2. the fabricated frontier row (admitted; names the missing entry)
cat >> "$TREE/corpus/README.md" <<'EOF'

## Round-42 junk-control twin (fabricated, NOT an admission)

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F25 | OSV schema - the machine-readable vulnerability record format (fabricated twin, not an admission) | admitted | knowledge/junk-f25-osv-schema.md | S999 | Fabricated twin: no capture, no entry, no harness pass - every instrument must reject it. |
EOF

# 3. the fabricated snapshot manifest: claims S999 with no url, no fetch
#    provenance and no capture bytes behind it
SNAP="$TREE/corpus/source-snapshots/round-42-junk"
mkdir -p "$SNAP"
cat > "$SNAP/manifest.json" <<'EOF'
{
  "purpose": "round-42 junk twin: claims a capture that was never fetched",
  "schema_version": 1,
  "sources": [
    {
      "id": "S999",
      "location": "fabricated twin - no upstream section",
      "path": "S999.txt",
      "quotes": [
        {
          "id": "Q1",
          "location": "fabricated twin",
          "quote": "A claim that exists in no upstream document."
        }
      ],
      "sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  ]
}
EOF

# 4. run the three named instruments against the mutated tree
cd "$TREE" || exit 2
rc_total=0
printf '$ python3 corpus/instruments/frontier-recheck-count.py\n'
python3 corpus/instruments/frontier-recheck-count.py | tail -3
rc1=${PIPESTATUS[0]}
printf 'exit=%d\n\n' "$rc1"
[ "$rc1" -ne 0 ] || rc_total=1

printf '$ python3 corpus/instruments/capture-binding-check.py\n'
python3 corpus/instruments/capture-binding-check.py | tail -4
rc2=${PIPESTATUS[0]}
printf 'exit=%d\n\n' "$rc2"
[ "$rc2" -ne 0 ] || rc_total=1

printf '$ bash %s validate --root %s %s\n' "$CENSUS" "$TREE" "$TREE"
bash "$CENSUS" validate --root "$TREE" "$TREE"
rc3=$?
printf 'exit=%d\n\n' "$rc3"
[ "$rc3" -ne 0 ] || rc_total=1

if [ "$rc_total" -eq 0 ]; then
  echo "VERDICT: the junk twin is REJECTED by all three named instruments (each exits nonzero)."
else
  echo "VERDICT: AT LEAST ONE NAMED INSTRUMENT ACCEPTED THE JUNK TWIN -- the control failed."
fi
exit "$rc_total"
