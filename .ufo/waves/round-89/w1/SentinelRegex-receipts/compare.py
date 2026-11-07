#!/usr/bin/env python3
"""r88 vs r89 instrument, same buffers, same host, interleaved.

usage: python3 -B compare.py --r88 FILE --r89 DIR --sizes 1048576,4194304
"""
import argparse
import importlib.util
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bench import CASES, slope  # noqa: E402


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--r88", required=True)
    ap.add_argument("--r89", required=True)
    ap.add_argument("--sizes", default="1048576,4194304")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--only")
    a = ap.parse_args(argv)
    sizes = [int(x) for x in a.sizes.split(",")]
    m88 = load(a.r88, "css88")
    m89 = load(os.path.join(a.r89, "capture-secret-scan.py"), "css89")
    p88, p89 = m88.patterns(), m89.patterns()
    az88 = dict(m88.CLOUD_PATTERNS)["azure-sas-signature"]
    az89 = dict(m89.CLOUD_PATTERNS)["azure-sas-signature"]
    cf89 = dict(m89.CLOUD_PATTERNS)["cloudfront-signed-url-signature"]
    print("SHAPES r88=%d r89=%d" % (len(p88), len(p89)))

    cbuf = b"a" * (1450 * 1024)
    def cal():
        t = time.perf_counter()
        az89.search(cbuf)
        return time.perf_counter() - t
    base = min(cal() for _ in range(5))
    print("CALIB baseline=%.4f" % base)

    def timed(fn, data):
        best, bc = None, None
        for _ in range(a.reps + 2):
            c = cal()
            t0 = time.perf_counter()
            fn(data)
            dt = time.perf_counter() - t0
            if best is None or dt < best:
                best, bc = dt, c
            if c <= 3 * base:
                break
        return best, bc

    only = set(a.only.split(",")) if a.only else None
    for name, fn in CASES:
        if only and name not in only:
            continue
        for n in sizes:
            data = fn(n)
            f88, c88 = timed(lambda d: m88.scan_bytes(d, p88), data)
            f89, c89 = timed(lambda d: m89.scan_bytes(d, p89), data)
            a88, _ = timed(lambda d: sum(1 for _ in az88.finditer(d)), data)
            a89, _ = timed(lambda d: sum(1 for _ in az89.finditer(d)), data)
            c89t, _ = timed(lambda d: sum(1 for _ in cf89.finditer(d)), data)
            print("CMP %-20s %8d full88=%.4f full89=%.4f x=%.2f | az88=%.4f az89=%.4f x=%.2f | cf89=%.4f | cal=%.4f/%.4f"
                  % (name, len(data), f88, f89, f89 / f88, a88, a89,
                     a89 / a88 if a88 else 0.0, c89t, c88, c89))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
