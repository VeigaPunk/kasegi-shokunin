#!/usr/bin/env python3
"""CriticHarm r97 check 3: extract each scanner's selftest case list verbatim."""
import ast
import re
import sys
import textwrap


def cases(path):
    src = open(path, encoding="utf-8").read()
    m = re.search(r"^def selftest\(pats\):\n(.*?)^    cases = \[\n(.*?)^    \]\n",
                  src, re.S | re.M)
    if not m:
        raise SystemExit("no cases block in " + path)
    block = textwrap.dedent(m.group(1)) + "cases = [\n" + textwrap.dedent(m.group(2)) + "]\n"
    ns = {}
    exec(compile(block, path, "exec"), ns)
    return ns["cases"]


if __name__ == "__main__":
    for p in sys.argv[1:]:
        cs = cases(p)
        pos = [c for c in cs if c[2]]
        neg = [c for c in cs if not c[2]]
        print("%s cases=%d positives=%d negatives=%d" % (p, len(cs), len(pos), len(neg)))
