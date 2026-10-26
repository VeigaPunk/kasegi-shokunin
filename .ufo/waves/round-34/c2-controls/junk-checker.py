#!/usr/bin/env python3
"""Do-nothing control for C2: shape-only checker.

Counts the *shape* counters the junk twin satisfies (one entry file with a
`source:` header, one registry row named, one harness line) without touching
capture bytes or the source registry. The real admission gate must reject the
junk twin where this checker passes it.
"""
import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parents[4]
entry = root / ".ufo/waves/round-34/c2-controls/junk-f17.md"
text = entry.read_text()
has_h1 = text.startswith("# ")
has_source = bool(re.search(r"^source: S051 \u2014", text, re.M))
has_recheck = bool(re.search(r"^recheck: ", text, re.M))
print(f"junk_twin h1={has_h1} source_line={has_source} recheck_line={has_recheck}")
print("shape_counters=3/3")
sys.exit(0)
