#!/usr/bin/env python3
"""Apply a round-92 C1 repair map (citing-file:line<TAB>key<TAB>old<TAB>new) to the files under
--root, in place. Refuses (exit 1, nothing written) unless every `old` occurs exactly
once on its line."""
import argparse
import sys


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--map", required=True)
    a = ap.parse_args(argv)
    edits = {}
    for ln in open(a.map, encoding="utf-8").read().split("\n"):
        if ln.strip() and not ln.startswith("#"):
            site, _key, old, new = ln.split("\t")
            f, n = site.rsplit(":", 1)
            edits.setdefault(f, []).append((int(n), old, new))
    out = {}
    for f, rows in edits.items():
        p = "%s/%s" % (a.root, f)
        lines = open(p, encoding="utf-8").read().split("\n")
        for n, old, new in rows:
            if lines[n - 1].count(old) != 1:
                print("APPLY refused %s:%d old_count=%d" % (f, n, lines[n - 1].count(old)))
                return 1
            lines[n - 1] = lines[n - 1].replace(old, new, 1)
        out[p] = "\n".join(lines)
    for p, text in out.items():
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
    print("APPLY ok files=%d sites=%d" % (len(out), sum(len(r) for r in edits.values())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
