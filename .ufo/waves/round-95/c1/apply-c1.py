#!/usr/bin/env python3
"""Apply the round-95 C1 repair map to a tree (worktree or fixture clone).

Usage: apply-c1.py TREE [--drop N] [--only N]
Reads the map from the lane's round-95 wave dir; every `old` must occur on its
line (once for cells/parts), otherwise it exits 2.
"""
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
MAP = LANE + "/.ufo/waves/round-95/c1/repair-map.tsv"


def rows(path=MAP):
    out = []
    for ln in open(path, encoding="utf-8").read().split("\n"):
        if ln.strip() and not ln.startswith("#"):
            site, key, old, new = ln.split("\t")
            f, n = site.rsplit(":", 1)
            out.append((f, int(n), key, old, new))
    return out


def apply(tree, drop=(), only=None, map_path=MAP):
    rs = rows(map_path)
    files = {}
    for i, (f, n, key, old, new) in enumerate(rs):
        if i in drop or (only is not None and i != only):
            continue
        p = os.path.join(tree, f)
        if f not in files:
            files[f] = open(p, encoding="utf-8").read().split("\n")
        line = files[f][n - 1]
        if old not in line:
            raise SystemExit("anchor missing at %s:%d: %r" % (f, n, old[:60]))
        files[f][n - 1] = line.replace(old, new)
    for f, lines in files.items():
        open(os.path.join(tree, f), "w", encoding="utf-8").write("\n".join(lines))
    return len(rs)


if __name__ == "__main__":
    tree = sys.argv[1]
    drop = set()
    only = None
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--drop":
            drop.add(int(args[i + 1])); i += 2
        elif args[i] == "--only":
            only = int(args[i + 1]); i += 2
        else:
            raise SystemExit("bad arg " + args[i])
    print("applied=%d skipped=%s" % (apply(tree, drop, only), sorted(drop)))
