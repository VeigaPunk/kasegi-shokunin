#!/usr/bin/env python3
"""AST probe: report imported names that are never read in the module."""
import ast
import sys


def analyse(path):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    imported = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                nm = a.asname or a.name.split(".")[0]
                imported[nm] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                nm = a.asname or a.name
                imported[nm] = node.lineno
    loaded = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            loaded.add(node.id)
        elif isinstance(node, ast.Attribute):
            pass
    # attribute roots count as reads
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            n = node
            while isinstance(n, ast.Attribute):
                n = n.value
            if isinstance(n, ast.Name):
                loaded.add(n.id)
    unused = {k: v for k, v in imported.items() if k not in loaded}
    print("== %s" % path)
    if not unused:
        print("   (no unused imports)")
    for k, v in sorted(unused.items(), key=lambda kv: kv[1]):
        print("   unused-import: %-14s line %d" % (k, v))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        analyse(p)
