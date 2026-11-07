#!/usr/bin/env python3
"""Generate single-point mutants of a frozen counter from a TSV table.

Usage: MutC1Counter-mkmut.py SRC_COUNTER TABLE.tsv OUTDIR
Each table row is: name<TAB>old<TAB>new, with \\n standing for a newline.
Every substitution must match exactly once, or the row is skipped (fail closed).
"""
import os
import sys


def unesc(s):
    return s.replace("\\n", "\n").replace("\\t", "\t").replace("\\\\", "\\")


def main(argv):
    src_path, table, outdir = argv
    src = open(src_path, encoding="utf-8").read()
    os.makedirs(outdir, exist_ok=True)
    built, skipped = 0, 0
    for line in open(table, encoding="utf-8").read().rstrip("\n").split("\n"):
        name, old, new = line.split("\t")
        old, new = unesc(old), unesc(new)
        n = src.count(old)
        if n != 1:
            print("SKIP %s occurrences=%d" % (name, n))
            skipped += 1
            continue
        with open(os.path.join(outdir, name + ".py"), "w", encoding="utf-8") as fh:
            fh.write(src.replace(old, new))
        built += 1
    print("MUTANTS built=%d skipped=%d" % (built, skipped))
    return 0 if skipped == 0 else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
