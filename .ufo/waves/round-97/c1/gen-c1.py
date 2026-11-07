#!/usr/bin/env python3
"""Round-97 C1 generator: derive repair-map.tsv from the frozen label set and
apply the named edits to a clone of a pinned revision.

Every map row is derived from its label row with the counter's own expected_edit
rules (qualify-lane: the label names the tracked target path and the edit is
`key` -> `label`), so the map cannot drift from the labels. Each `old` must
occur exactly once on its base line; the script refuses otherwise.

Usage: gen-c1.py LABELS MAP CLONE_DIR [--apply]
"""
import os
import re
import subprocess
import sys


def expected(label, fix, key):
    if fix.startswith("Replace part: "):
        rest = fix[len("Replace part: "):]
        old, new = rest.split(" => ", 1)
        return "part", old, new
    if label.startswith("corpus/instruments/"):
        return "qualify-lane", "`%s`" % key, "`%s`" % label
    if label.startswith("corpus/source-snapshots/") or label.startswith("corpus/knowledge/") \
            or re.match(r"^SKILL\.md:\d", label):
        return "range", "`%s`" % key, "`%s`" % label
    raise SystemExit("unsupported label kind: %r / %r" % (label, fix))


def main(argv):
    labels_path, map_path, clone = argv[:3]
    apply = "--apply" in argv
    rows = []
    with open(labels_path, encoding="utf-8") as fh:
        for i, ln in enumerate(fh):
            ln = ln.rstrip("\n")
            if not ln or ln.startswith("#") or i == 0 and ln.startswith("line\t"):
                continue
            site, key, label, fix, _ev = ln.split("\t")
            kind, old, new = expected(label, fix, key)
            rows.append((site, key, old, new, kind))
    out = ["# round-97 C1 repair map: site\tkey\told\tnew (derived from labels.tsv)"]
    edits = {}
    for site, key, old, new, kind in rows:
        out.append("\t".join((site, key, old, new)))
        f, n = site.rsplit(":", 1)
        n = int(n)
        edits.setdefault(f, []).append((n, old, new, kind))
    with open(map_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    # uniqueness of each `old` on its base line
    for f, items in edits.items():
        lines = open(os.path.join(clone, f), encoding="utf-8").read().split("\n")
        for n, old, new, kind in items:
            c = lines[n - 1].count(old)
            if c != 1:
                raise SystemExit("old occurs %d times at %s:%d: %r" % (c, f, n, old))
            if new in lines[n - 1]:
                raise SystemExit("new already present at %s:%d" % (f, n))
    if apply:
        for f, items in edits.items():
            p = os.path.join(clone, f)
            lines = open(p, encoding="utf-8").read().split("\n")
            for n, old, new, kind in items:
                lines[n - 1] = lines[n - 1].replace(old, new)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines))
        subprocess.run(["git", "-C", clone, "add", "-A"], check=True)
        subprocess.run(["git", "-C", clone, "-c", "user.name=fixture",
                        "-c", "user.email=fixture@invalid", "commit", "-q",
                        "-m", "r97-c1-candidate"], check=True)
        rev = subprocess.run(["git", "-C", clone, "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()
        print("candidate=%s" % rev)
        top = subprocess.run(["git", "-C", clone, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True).stdout.strip()
        assert top == os.path.realpath(clone), "clone root mismatch: " + top
    print("rows=%d kinds=%s" % (len(rows), ",".join(sorted({r[4] for r in rows}))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
