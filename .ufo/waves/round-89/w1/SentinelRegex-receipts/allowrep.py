#!/usr/bin/env python3
"""Does an allowlisted match make scan_bytes quadratic in matches-per-file?

scan_bytes() calls data.count(b"\\n", 0, m.start()) for every match it does not
report (i.e. every allowlisted one), so k allowlisted matches in one buffer cost
sum(m.start()) ~ k*N/2.  The round-89 allowlist adds two rows for the CloudFront
doc example, which is the first CloudFront value that can be allowlisted at all.

usage: python3 -B allowrep.py --inst DIR --s128 FILE --sizes 10240,102400,1048576,4194304
Prints counts and seconds only: no matched bytes, no fixture bytes.
"""
import argparse
import hashlib
import importlib.util
import math
import os
import sys
import time

PATH = "corpus/source-snapshots/round-89/S128.txt"


def load(inst):
    spec = importlib.util.spec_from_file_location(
        "css", os.path.join(inst, "capture-secret-scan.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def slope(points):
    xs = [math.log10(n) for n, _ in points]
    ys = [math.log10(t) for _, t in points]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--inst", required=True)
    ap.add_argument("--s128", required=True)
    ap.add_argument("--sizes", default="10240,102400,1048576,4194304")
    ap.add_argument("--reps", type=int, default=3)
    a = ap.parse_args(argv)
    m = load(a.inst)
    pats = m.patterns()
    cf = dict(m.CLOUD_PATTERNS)["cloudfront-signed-url-signature"]
    with open(a.s128, "rb") as fh:
        line = [ln for ln in fh if b"Signature=" in ln][0]
    mt = cf.search(line).group(0)
    digest = hashlib.sha256(mt).hexdigest()
    print("FIXTURE path=%s matched_len=%d matched_sha256=%s" % (PATH, len(mt), digest))
    allow = {(PATH, "cloudfront-signed-url-signature", digest): "doc example"}
    sizes = [int(x) for x in a.sizes.split(",")]
    pts_on, pts_off = [], []
    for n in sizes:
        unit = mt + b"\n"
        k = max(1, n // len(unit))
        data = unit * k
        best_on = best_off = None
        for _ in range(a.reps):
            t0 = time.perf_counter()
            found, allowed = m.scan_bytes(data, pats, PATH, allow)
            dt = time.perf_counter() - t0
            best_on = dt if best_on is None else min(best_on, dt)
            t0 = time.perf_counter()
            found0, allowed0 = m.scan_bytes(data, pats, PATH, {})
            dt0 = time.perf_counter() - t0
            best_off = dt0 if best_off is None else min(best_off, dt0)
        pts_on.append((len(data), best_on))
        pts_off.append((len(data), best_off))
        print("ALLOWREP size=%d matches=%d allow_on=%.4f hits_on=%d allowed=%d | allow_off=%.4f hits_off=%d"
              % (len(data), k, best_on, len(found), allowed, best_off, len(found0)))
    print("EXP allow_on=%.3f allow_off=%.3f" % (slope(pts_on), slope(pts_off)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
