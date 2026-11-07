#!/usr/bin/env python3
"""Analyze which citations force the expensive glob existence test."""
import os
import sys

sys.argv = ["analyzer", sys.argv[1]]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mycensus as mc

ROOT = mc.ROOT
repo, cites = mc.collect(ROOT)
print("distinct citations: %d" % len(cites))

rel = absdom = bounty = mirror = 0
literal_internal = 0
gone_rel_noglob = 0
glob_needed = []
brace_needed = []

for tok in sorted(cites):
    base, _ = mc.strip_anchor(tok)
    if mc.bounty_suffix(base) is not None:
        bounty += 1
        continue
    if mc.mirror_suffix(base) is not None:
        mirror += 1
        continue
    if base.startswith("~") or base.startswith("/"):
        absdom += 1
        continue
    rel += 1
    p = os.path.join(repo, base)
    pe = os.path.expanduser(p)
    if os.path.exists(pe):
        literal_internal += 1
        continue
    # literal failed; would brace/glob run?
    has_brace = "{" in pe and "}" in pe
    q = mc.PLACEHOLDER.sub("*", pe)
    needs_glob = any(ch in q for ch in mc.GLOBMETA)
    if has_brace:
        brace_needed.append((tok, pe))
    if needs_glob:
        glob_needed.append((tok, pe))
    else:
        gone_rel_noglob += 1

print("domains: rel=%d abs=%d bounty=%d mirror=%d" % (rel, absdom, bounty, mirror))
print("rel literal-INTERNAL: %d" % literal_internal)
print("rel gone-no-glob: %d" % gone_rel_noglob)
print("rel brace-candidates: %d" % len(brace_needed))
print("rel glob-needed: %d" % len(glob_needed))
print()
print("=== glob-needed patterns (first 60) ===")
for tok, pe in glob_needed[:60]:
    print("%s\n    -> %s" % (tok, pe))
print()
print("=== brace candidates (first 20) ===")
for tok, pe in brace_needed[:20]:
    print("%s\n    -> %s" % (tok, pe))
