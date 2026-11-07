#!/usr/bin/env python3
"""Paired growth ratios: every ratio is computed inside one rep, so both sizes
see the same host load.  A linear pattern gives 2.0 for each doubling; a
quadratic one gives 4.0.

usage: python3 -B recheck3.py --inst DIR --cases a,b --mode full|cf|az --reps 9
"""
import argparse
import importlib.util
import os
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bench import CASES  # noqa: E402


def load(inst):
    spec = importlib.util.spec_from_file_location(
        "css", os.path.join(inst, "capture-secret-scan.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--inst", required=True)
    ap.add_argument("--cases", required=True)
    ap.add_argument("--sizes", default="1048576,2097152,4194304,8388608")
    ap.add_argument("--reps", type=int, default=9)
    ap.add_argument("--mode", default="full", choices=("full", "cf", "az"))
    a = ap.parse_args(argv)
    m = load(a.inst)
    pats = m.patterns()
    cf = dict(m.CLOUD_PATTERNS)["cloudfront-signed-url-signature"]
    az = dict(m.CLOUD_PATTERNS)["azure-sas-signature"]
    if a.mode == "full":
        run = lambda d: m.scan_bytes(d, pats)
    elif a.mode == "cf":
        run = lambda d: sum(1 for _ in cf.finditer(d))
    else:
        run = lambda d: sum(1 for _ in az.finditer(d))
    sizes = [int(x) for x in a.sizes.split(",")]
    print("LOAD before=%.2f" % float(open("/proc/loadavg").read().split()[0]))
    fnmap = dict(CASES)
    for case in a.cases.split(","):
        bufs = {n: fnmap[case](n) for n in sizes}
        ratios = {i: [] for i in range(len(sizes) - 1)}
        secs = {n: [] for n in sizes}
        for _ in range(a.reps):
            t = {}
            for n in sizes:
                t0 = time.perf_counter()
                run(bufs[n])
                t[n] = time.perf_counter() - t0
                secs[n].append(t[n])
            for i in range(len(sizes) - 1):
                ratios[i].append(t[sizes[i + 1]] / t[sizes[i]])
        print("PAIR %-16s %-4s" % (case, a.mode))
        for i in range(len(sizes) - 1):
            r = sorted(ratios[i])
            print("  %d->%d  median=%.3f  min=%.3f max=%.3f  (linear=2.000)"
                  % (sizes[i], sizes[i + 1], statistics.median(r), r[0], r[-1]))
        print("  sec_median %s" % " ".join("%d:%.4f" % (n, statistics.median(secs[n])) for n in sizes))
        print("  sec_min    %s" % " ".join("%d:%.4f" % (n, min(secs[n])) for n in sizes))
    print("LOAD after=%.2f" % float(open("/proc/loadavg").read().split()[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
