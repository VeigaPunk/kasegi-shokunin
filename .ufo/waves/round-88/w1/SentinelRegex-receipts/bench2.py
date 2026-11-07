#!/usr/bin/env python3
"""Load-normalised timing matrix for capture-secret-scan's round-88 patterns.

Every row: a fixed calibration probe is timed immediately before the measured
scans; if the machine is loaded (cal > LOAD_FACTOR x the startup baseline) the
row is retried, so contention is not misread as super-linear growth. Each
figure is best-of-reps. Emits TSV plus, per case, the log-log growth exponent.

Usage: bench2.py [--reps 3] [--sizes 10240,102400,1048576,4194304] [--cases a,b]
"""
import argparse
import importlib.util
import math
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "css", os.path.join(HERE, "inst", "capture-secret-scan.py"))
css = importlib.util.module_from_spec(spec)
spec.loader.exec_module(css)
import bench  # noqa: E402  (adversarial builders live in bench.py)

CAL = b"https://h.example/p?a=1&ab=12" * 50000
CAL_RX = re.compile(rb"(?:sv=\d{4}-\d{2}-\d{2}|ab=12)")

CASES = [
    "many-params", "sv-no-sig", "gcs-hex", "sig39",
    "gcs-hex-upper", "gcs-near-miss", "gcs-spaces", "sig-nosep",
    "amp-entities", "u0026-blocks", "realistic-sas",
    "sig-giant", "sv-giant-value", "sv-sig39", "sig40-svbad",
    "amp-soup", "u0026-chain", "sv-longtail", "sv-longtail-quote",
]
LOAD_FACTOR = 3.0


def cal():
    t0 = time.perf_counter()
    n = 0
    for _ in CAL_RX.finditer(CAL):
        n += 1
    return time.perf_counter() - t0, n


def best(fn, reps):
    b = None
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        dt = time.perf_counter() - t0
        b = dt if b is None else min(b, dt)
    return b


def first_match(rx, data):
    for _ in rx.finditer(data):
        return True
    return False


def slope(pts):
    xs = [math.log10(p[0]) for p in pts]
    ys = [math.log10(p[1]) for p in pts]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    return (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            / sum((x - mx) ** 2 for x in xs))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--sizes", default="10240,102400,1048576,4194304")
    ap.add_argument("--cases", default=",".join(CASES))
    a = ap.parse_args(argv)
    sizes = [int(x) for x in a.sizes.split(",")]
    pats = css.patterns()
    az = dict(css.CLOUD_PATTERNS)["azure-sas-signature"]
    gc = dict(css.CLOUD_PATTERNS)["gcs-signed-url-signature"]
    base = min(cal()[0] for _ in range(5))
    print("# calibration baseline %.4f s for a 1.45 MB reference scan" % base, flush=True)
    print("case\tsize\tcal_s\tfull_s\tazure_s\tgcs_s\thits", flush=True)
    for case in a.cases.split(","):
        pf, pa = [], []
        for n in sizes:
            data = bench.build(case, n)
            for _try in range(4):
                c, _ = cal()
                if c <= LOAD_FACTOR * base:
                    break
            else:
                print("%s\t%d\t%.4f\tSKIP-HIGH-LOAD\t\t\t" % (case, n, c), flush=True)
                continue
            full = best(lambda: css.scan_bytes(data, pats), a.reps)
            azure = best(lambda: first_match(az, data), a.reps)
            gcs = best(lambda: first_match(gc, data), a.reps)
            hits = [s for s, _ in css.scan_bytes(data, pats)[0]]
            print("%s\t%d\t%.4f\t%.4f\t%.4f\t%.4f\t%s"
                  % (case, n, c, full, azure, gcs, ",".join(hits) or "-"), flush=True)
            pf.append((n, full))
            pa.append((n, azure))
        if len(pf) >= 3:
            print("EXPONENT %s full=%.3f azure=%.3f" % (case, slope(pf), slope(pa)), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
