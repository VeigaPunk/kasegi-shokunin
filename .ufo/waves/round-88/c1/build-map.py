#!/usr/bin/env python3
"""Round-88 C1 map builder (pre-freeze; deterministic; successor of round 87's).

Selects every distinct citation in the corpus/knowledge/*.md scope at REV that
(a) is a bare `<name>.md` with an optional :N / :N-M anchor (knowledge-meter.KEY),
(b) resolve.py classifies GONE,
(c) whose basename is held by exactly one tracked file outside .ufo/, and that
    file is corpus/knowledge/<name>.md (a sibling knowledge entry),
(d) whose anchor (when present) lies inside that entry's line count at REV,
(e) whose every citing line passes the M8 content proxy (knowledge-meter.idents
    shares a word with the cited line range at REV); unanchored keys are exempt.
Tokens failing (c), (d) or (e) are written to --excluded with the reason; a token
failing (e) is a drifted line anchor, routed for manual re-anchoring.

Usage: build-map.py --lane LANE --rev REV --out MAP.json --excluded EXCL.json --work DIR
"""
import argparse
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
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
    files = km.scope_files_rev(lane, a.rev)
    cls = km.classify_scope(R, lane, files, a.work)
    tracked = [p for p in km.git(lane, "ls-tree", "-r", "--name-only", a.rev).split("\n") if p]
    bybase = {}
    for p in tracked:
        if not p.startswith(".ufo/"):
            bybase.setdefault(os.path.basename(p), []).append(p)
    rmap, excl = {}, {}
    for t, c in sorted(cls.items()):
        m = km.KEY.match(t)
        if c != "GONE" or not m:
            continue
        name = m.group(1)
        hits = bybase.get(name, [])
        if hits != ["corpus/knowledge/" + name]:
            if hits and len(hits) == 1:
                excl[t] = "not-a-knowledge-entry:%s" % hits[0]
            elif hits:
                excl[t] = "basename-not-unique:%d" % len(hits)
            continue
        path = hits[0]
        anchor = t[len(name):]
        if m.group(2):
            lines = files[path].split("\n")
            n = len(files[path].splitlines())
            lo, hi = int(m.group(2)), int(m.group(3) or m.group(2))
            if not (1 <= lo <= hi <= n):
                excl[t] = "anchor-out-of-range:%s has %d lines" % (path, n)
                continue
            tw = set(km.WORD.findall("\n".join(lines[lo - 1:hi])))
            cites = [ln for txt in files.values() for ln in txt.split("\n") if "`%s`" % t in ln]
            if not cites:
                excl[t] = "not-backticked"
                continue
            if any(not (km.idents(ln) & tw) for ln in cites):
                excl[t] = "anchor-content-drift:no shared identifier on %d/%d citing lines" % (
                    sum(1 for ln in cites if not (km.idents(ln) & tw)), len(cites))
                continue
        else:
            if not any("`%s`" % t in ln for txt in files.values() for ln in txt.split("\n")):
                excl[t] = "not-backticked"
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
