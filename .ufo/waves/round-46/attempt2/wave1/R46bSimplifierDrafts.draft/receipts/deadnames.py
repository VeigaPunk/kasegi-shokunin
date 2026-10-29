#!/usr/bin/env python3
"""AST probe: report module-level and function-local names that are bound but never read.

Pure static analysis (ast only) - it prints, it does not touch the file it reads.
"""
import ast
import sys


def analyse(path):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    loaded = {}
    stored = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Load):
                loaded.setdefault(node.id, []).append(node.lineno)
            else:
                stored.setdefault(node.id, []).append(node.lineno)
        elif isinstance(node, ast.Attribute):
            pass
    print("== %s" % path)
    dead = []
    for name, lines in sorted(stored.items()):
        if name in loaded:
            continue
        if name.startswith("_") and name not in ("_c",):
            pass
        dead.append((name, lines))
    for name, lines in dead:
        print("   bound-never-read: %-22s stored at line(s) %s" % (name, ",".join(map(str, lines))))
    if not dead:
        print("   (none)")
    return dead


if __name__ == "__main__":
    for p in sys.argv[1:]:
        analyse(p)
