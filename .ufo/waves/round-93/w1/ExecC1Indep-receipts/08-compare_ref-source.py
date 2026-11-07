#!/usr/bin/env python3
"""Compare ExecC1Indep's own extractor classes with the lane reference
resolver's citation-survival.tsv on the same tree, restricted to the
distinct tokens that occur in corpus/knowledge/*.md."""
import csv
import importlib.util
import pathlib
import sys

spec = importlib.util.spec_from_file_location("mc", sys.argv[3])
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)

tree = sys.argv[1]
tsv_path = sys.argv[2]
mb = mc.measure(tree)
mine = mb["cls"]

rows = list(csv.reader(open(tsv_path, newline="", encoding="utf-8"), delimiter="\t"))
ref = {}
for r in rows[1:]:
    if len(r) >= 2:
        ref[r[0]] = r[1]

print("tree", tree, "my-distinct", len(mine), "tsv-rows", len(ref))
diffs = []
for t, c in sorted(mine.items()):
    rc = ref.get(t)
    if rc is None:
        diffs.append((t, c, "ABSENT-IN-TSV"))
    elif rc != c:
        diffs.append((t, c, rc))
extra = [t for t in ref if t not in mine and any(t == m for m in mine)]
print("class-disagreements-on-shared-tokens:", len(diffs))
for t, c, rc in diffs:
    print(f"  {t!r} mine={c} ref={rc}")
only_mine = [t for t in mine if t not in ref]
print("tokens-mine-only (not in reference census):", len(only_mine))
for t in only_mine[:20]:
    print("   ", repr(t))
print("METER-BUCKETS mine: resolved=", mb["resolved"], "gone=", mb["gone"], "total=", mb["total"])
