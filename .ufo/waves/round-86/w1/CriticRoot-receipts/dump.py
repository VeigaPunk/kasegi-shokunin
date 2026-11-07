#!/usr/bin/env python3
"""Dump {token: class} for the corpus/knowledge scope at one root, via the frozen
knowledge-meter functions. Read-only w.r.t. LANE; writes only OUT."""
import argparse
import importlib.util
import json
import os
import sys


def load_meter(path):
    spec = importlib.util.spec_from_file_location("kmeter", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dir_files(d):
    out = {}
    for fn in sorted(os.listdir(d)):
        p = os.path.join(d, fn)
        if fn.endswith(".md") and os.path.isfile(p):
            with open(p, encoding="utf-8") as fh:
                out["corpus/knowledge/" + fn] = fh.read()
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--meter", required=True)
    ap.add_argument("--lane", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--files-tree")
    ap.add_argument("--files-rev")
    ap.add_argument("--files-dir")
    a = ap.parse_args(argv)
    km = load_meter(a.meter)
    lane = os.path.abspath(a.lane)
    R = km.load_resolve(lane)
    if a.files_tree:
        files = km.scope_files_tree(os.path.abspath(a.files_tree))
        src = "tree:" + a.files_tree
    elif a.files_rev:
        files = km.scope_files_rev(lane, a.files_rev)
        src = "rev:" + a.files_rev
    else:
        files = dir_files(os.path.abspath(a.files_dir))
        src = "dir:" + a.files_dir
    cls = km.classify_scope(R, lane, files, a.work)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(cls, fh, indent=0, sort_keys=True)
    n, m = km.rate(cls)
    print("DUMP lane=%s src=%s files=%d rate=%d/%d mirror_absent=%s resolve=%s"
          % (lane, src, len(files), n, m, R.MIRROR_ABSENT, R.__file__))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
