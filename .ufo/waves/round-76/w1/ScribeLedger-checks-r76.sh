#!/bin/bash
S=/fast/scratch/hyaku/kasegi-r76/ScribeLedger
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$L/.ufo/waves/round-76/w1
E=$L/corpus/instruments/knowledge-expected.txt
echo "## T1 base: knowledge-expected rows equal corpus/knowledge directory (set)"
diff <(grep '^corpus/knowledge/' "$E" | LC_ALL=C sort) <(ls "$L"/corpus/knowledge/*.md | sed "s#^$L/##" | LC_ALL=C sort); echo "rc=$?"
echo "## T2 base: sort -c on the file, row and line counts"
LC_ALL=C sort -c "$E"; echo "sortc_rc=$?"
echo "rows=$(grep -c '^corpus/knowledge/' "$E") lines=$(wc -l < "$E")"
NEWLINE=$(grep '^corpus/knowledge/osv-api-surface-and-limits\.md$' "$W/knowledge-expected-line-draft.md")
echo "## T3 draft line present exactly once: count=$(grep -c '^corpus/knowledge/osv-api-surface-and-limits\.md$' "$W/knowledge-expected-line-draft.md") value=[$NEWLINE]"
cp "$E" "$S/exp-append.txt"; printf '%s\n' "$NEWLINE" >> "$S/exp-append.txt"
echo "## T4 APPEND variant (the literal spec wording): sort -c"
LC_ALL=C sort -c "$S/exp-append.txt"; echo "sortc_rc=$?"
awk -v nl="$NEWLINE" '$0 ~ /^corpus\/knowledge\/osv-post-v1-query-contract\.md$/ {print nl} {print}' "$E" > "$S/exp-insert.txt"
echo "## T5 INSERT variant (draft): sort -c, line count, row count, position"
LC_ALL=C sort -c "$S/exp-insert.txt"; echo "sortc_rc=$?"
echo "lines=$(wc -l < "$S/exp-insert.txt") rows=$(grep -c '^corpus/knowledge/' "$S/exp-insert.txt")"
grep -n 'osv-' "$S/exp-insert.txt"
echo "## T6 INSERT variant vs base: the only difference is one added line"
diff "$E" "$S/exp-insert.txt"; echo "diff_rc=$?"
echo "## T7 INSERT variant rows = directory after the round (simulated, new file not yet on disk)"
diff <(grep '^corpus/knowledge/' "$S/exp-insert.txt" | LC_ALL=C sort) <( (ls "$L"/corpus/knowledge/*.md | sed "s#^$L/##"; echo corpus/knowledge/osv-api-surface-and-limits.md) | LC_ALL=C sort); echo "rc=$?"
echo "## T8 F54 row cell count (NF=8 means 6 cells) and F53 comparison row"
grep '^| F54 |' "$W/readme-f54-block-draft.md" | awk -F'|' '{print "F54 NF="NF" cells="NF-2}'
grep -m1 '^| F53 |' "$L/corpus/README.md" | awk -F'|' '{print "F53 NF="NF" cells="NF-2}'
echo "## T9 S111 capture sha256 and size"
sha256sum "$L/corpus/source-snapshots/round-76/S111.txt"; echo "sha_rc=$?"
wc -lc "$L/corpus/source-snapshots/round-76/S111.txt"
echo "## T10 manifest quotes located at their anchors (B5-style, read-only cross-check)"
python3 -B - "$L/corpus/source-snapshots/round-76/manifest.json" "$L/corpus/source-snapshots/round-76/S111.txt" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
lines = open(sys.argv[2], encoding="utf-8").read().split("\n")
qs = m["sources"][0]["quotes"]
bad = [q["id"] for q in qs if not (1 <= q["anchor"] <= len(lines) and q["quote"] in lines[q["anchor"] - 1])]
print("quotes", len(qs), "bad", bad, "anchor_min", min(q["anchor"] for q in qs), "anchor_max", max(q["anchor"] for q in qs))
print("max_words", max(len(q["quote"].split()) for q in qs))
PY
echo "anchors_rc=$?"
echo "## T11 frontier counter on a scratch root (corpus copy + draft README block + simulated S111 registry row)"
rm -rf "$S/root" && mkdir -p "$S/root" && cp -r "$L/corpus" "$S/root/" && echo "copy_rc=$?"
sed -n '/^==========$/,$p' "$W/readme-f54-block-draft.md" | tail -n +2 >> "$S/root/corpus/README.md"
python3 -B - "$S/root/corpus/SOURCES.md" <<'PY'
import sys
p = sys.argv[1]
out = []
for line in open(p, encoding="utf-8").read().split("\n"):
    out.append(line)
    if line.startswith("| S110 "):
        out.append(line.replace("| S110 ", "| S111 ", 1))
open(p, "w", encoding="utf-8").write("\n".join(out))
PY
echo "registry_rows_sim=$(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$S/root/corpus/SOURCES.md")"
cd "$S" && python3 -B "$L/corpus/instruments/frontier-recheck-count.py" --root "$S/root" > "$S/frontier-sim.txt" 2>&1; echo "frontier_sim_rc=$?"
grep -E '^FRONTIER-CENSUS|F54|^entries=' "$S/frontier-sim.txt" | cut -c1-240
echo "## T12 cleanup of the scratch root copy"
rm -rf "$S/root"; echo "rm_rc=$?"
echo "## T13 source-recheck on the committed S111 manifest (B5 as frozen; read-only, scratch cwd)"
cd "$S" && python3 -B "$L/corpus/instruments/source-recheck.py" --manifest "$L/corpus/source-snapshots/round-76/manifest.json" --source S111; echo "source_recheck_rc=$?"
grep -n 'MIN_QUOTE_CHARS' "$L/corpus/instruments/source-recheck.py" | head -1
echo "## T14 version string occurrences in the S111 capture"
grep -n '1\.0' "$L/corpus/source-snapshots/round-76/S111.txt"; echo "grep_rc=$?"
