#!/usr/bin/env python3
"""d3-exhaustive.py — round-83 L1 probe: is P3 nonce-independent on a given target?

The r83 counter picks the D3 row from the nonce. For every non-neutral table row that
single_decoy could pick, build that D3 decoy (as the counter does, with the row forced) and
run the target's selftest from a fresh 'mutbat-t-' directory; print one line per row and a
summary. A target whose D3 passes for every eligible row has a nonce-independent decoy limb.
Usage: d3-exhaustive.py --target FILE --table FILE --expect-cases N --work DIR
"""
import argparse
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--table", required=True)
    ap.add_argument("--expect-cases", type=int, required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    spec = importlib.util.spec_from_file_location("mb", os.path.join(HERE, "..", "c1", "mutbat.py"))
    mb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mb)
    src = open(a.target, encoding="utf-8").read()
    rows = json.load(open(a.table, encoding="utf-8"))
    ok_lines = mb.comment_lines(src)
    elig = []
    for r in rows:
        if r["class"] == "neutral" or src.count(r["anchor"]) != 1 or "\n" not in r["anchor"]:
            continue
        pos = src.index(r["anchor"]) + r["anchor"].index("\n")
        if src.count("\n", 0, pos) + 1 in ok_lines:
            elig.append((r["id"], pos))

    def one(item):
        rid, pos = item
        d3 = src[:pos] + "  # mutbat-probe" + src[pos:]
        ddir = tempfile.mkdtemp(prefix="mutbat-t-", dir=a.work)
        try:
            p = os.path.join(ddir, os.path.basename(a.target))
            open(p, "w", encoding="utf-8").write(d3)
            rc, out = mb.run_selftest(p, a.work)
        finally:
            shutil.rmtree(ddir, ignore_errors=True)
        return rid, mb.clean_pass(rc, out, a.expect_cases), rc

    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(one, elig))
    for rid, ok, rc in res:
        print("D3 row=%s clean=%s rc=%d" % (rid, ok, rc))
    n_non = sum(1 for r in rows if r["class"] != "neutral")
    print("D3-EXHAUSTIVE eligible=%d/%d clean=%d broken=%d"
          % (len(res), n_non, sum(ok for _r, ok, _c in res), sum(not ok for _r, ok, _c in res)))
    return 0 if all(ok for _r, ok, _c in res) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
