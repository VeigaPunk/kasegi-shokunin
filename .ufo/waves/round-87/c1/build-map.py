#!/usr/bin/env python3
"""Round-87 C1 map builder (pre-freeze; deterministic; successor of round 86's).

Selects every distinct citation in the corpus/knowledge/*.md scope at REV that
(a) is a bare `S<digits>.txt` name with an optional :N / :N-M anchor,
(b) resolve.py classifies GONE,
(c) is not a QUOTED manifest-field token (knowledge-meter.QUOTED),
(d) whose bare name is the basename of exactly one tracked file under
    corpus/source-snapshots/ (.ufo/ fixture copies do not count),
(e) whose anchor (when present) lies inside that snapshot's line count.
Tokens failing (c), (d) or (e) are written to --excluded with the reason.

Usage: build-map.py --lane LANE --rev REV --out MAP.json --excluded EXCL.json --work DIR
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("km", os.path.join(HERE, "knowledge-meter.py"))
km = importlib.util.module_from_spec(spec)
spec.loader.exec_module(km)


def main(argv):
    ap = argparse.ArgumentParser()
    for f in ("--lane", "--rev", "--out", "--excluded", "--work"):
        ap.add_argument(f, required=True)
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    os.makedirs(a.work, exist_ok=True)
    R = km.load_resolve(lane)
    cls = km.classify_scope(R, lane, km.scope_files_rev(lane, a.rev), a.work)
    tracked = [p for p in km.git(lane, "ls-tree", "-r", "--name-only", a.rev).split("\n") if p]
    bybase = {}
    for p in tracked:
        if p.startswith("corpus/source-snapshots/"):
            bybase.setdefault(os.path.basename(p), []).append(p)
    rmap, excl = {}, {}
    for t, c in sorted(cls.items()):
        m = km.KEY.match(t)
        if c != "GONE" or not m:
            continue
        if m.group(1) in km.QUOTED:
            excl[t] = "quoted-manifest-field"
            continue
        hits = bybase.get(m.group(1), [])
        if len(hits) != 1:
            excl[t] = "snapshot-basename-not-unique:%d" % len(hits)
            continue
        path = hits[0]
        anchor = t[len(m.group(1)):]
        if m.group(2):
            n = len(open(os.path.join(lane, path), encoding="utf-8").read().splitlines())
            lo, hi = int(m.group(2)), int(m.group(3) or m.group(2))
            if not (1 <= lo <= hi <= n):
                excl[t] = "anchor-out-of-range:%s has %d lines" % (path, n)
                continue
        rmap[t] = path + anchor
    with open(a.out, "w") as fh:
        json.dump(rmap, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(a.excluded, "w") as fh:
        json.dump(excl, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("MAP keys=%d excluded=%d" % (len(rmap), len(excl)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
