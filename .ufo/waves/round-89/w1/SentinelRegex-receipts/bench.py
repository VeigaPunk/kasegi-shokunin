#!/usr/bin/env python3
"""Adversarial timing for the round-89 capture-secret-scan patterns.

Every buffer is generated from scratch at the requested size.  Values are built
by repetition of one-character atoms, so this file contains no credential-shaped
literal.  Rows are non-matching by construction (that is the worst case: the
scanner must walk the whole buffer), and the match count is printed so the
reader can see it.

usage: python3 -B bench.py --inst DIR [--sizes 10240,102400,1048576,4194304]
                           [--reps 3] [--only NAME[,NAME]] [--regex full|cf|az|both]
"""
import argparse
import importlib.util
import math
import os
import re
import sys
import time

# ---------------------------------------------------------------- generators
# Each takes a target byte count and returns (bytes, note).

def _rep(unit, n):
    k = max(1, n // len(unit))
    return unit * k


def cf_sig_run(n):
    return b"Signature=" + b"A" * max(0, n - 10)


def cf_sig_run_badkpi(n):
    tail = b"&Key-Pair-Id=" + b"a" * 8
    return b"Signature=" + b"A" * max(0, n - 10 - len(tail)) + tail


def cf_sig_many(n):
    return _rep(b"Signature=" + b"A" * 64 + b"&", n)


def cf_sig_tail(n):
    k = 1000
    return b"Signature=" * k + b"A" * max(0, n - 10 * k)


def cf_kpi_chain(n):
    return b"Key-Pair-Id=K2JCJMDEHXQW5F" + _rep(b"&aa=" + b"A" * 64, n)


def cf_kpi_first_nosig(n):
    return _rep(b"Key-Pair-Id=K2JCJMDEHXQW5F&Expires=1767290400&Policy=x", n)


def cf_u0026(n):
    return _rep(b"Signature=" + b"A" * 64 + b"\\u0026Key-Pair-Id=" + b"a" * 8, n)


def cf_pct26(n):
    return _rep(b"%26Signature=" + b"A" * 64 + b"%26Key-Pair-Id=" + b"a" * 8, n)


def cf_amp_chain(n):
    return _rep(b"&amp;" * 8 + b"Signature=" + b"A" * 64, n)


def cf_kpi_longrun(n):
    return b"Key-Pair-Id=" + b"A" * max(0, n - 13)


def cf_sig_params(n):
    return _rep(b"Signature=" + b"A" * 64 + b"&bb=1" * 40, n)


def cf_sig40_badkpi(n):
    return _rep(b"Signature=" + b"A" * 40 + b"&Key-Pair-Id=" + b"a" * 8, n)


def cf_sig_keysoup(n):
    # many 'Signature=' prefixes packed before one shared url-safe run
    k = 2000
    return b"Signature=" * k + b"A" * max(0, n - 10 * k)


def az_sv_dense(n):
    return _rep(b"sv=2022-11-02&", n)


def az_pct26(n):
    return _rep(b"%26sv=2022-11-02", n)


def az_u0026(n):
    return _rep(b"\\u0026sv=2022-11-02", n)


def az_pct26_sig(n):
    return _rep(b"%26sv=2022-11-02%26sig=" + b"A" * 40, n)


def az_sig_run(n):
    return b"sig=" + b"A" * max(0, n - 4)


def az_sig_run_sv_tail(n):
    tail = b"&sv=2022-11-02"
    return b"sig=" + b"A" * max(0, n - 4 - len(tail)) + tail


def az_amp_chain(n):
    return _rep(b"sv=2022-11-02" + b"&ab=1" * 40, n)


def plain(n):
    return _rep(b"the quick brown fox jumps over the lazy dog. ", n)



def az_u0026_sig39(n):
    return _rep(b"\\u0026sv=2022-11-02\\u0026sig=" + b"A" * 39, n)


def az_u0026_longval(n):
    return _rep(b"\\u0026sv=2022-11-02\\u0026aa=" + b"A" * 256, n)


def az_sv_sig39(n):
    return _rep(b"sv=2022-11-02&sig=" + b"A" * 39, n)


def cf_sig39_many(n):
    return _rep(b"Signature=" + b"A" * 39 + b"&", n)


def cf_many_long(n):
    return _rep(b"Signature=" + b"A" * 1024 + b"&", n)


def cf_u0026_sig(n):
    return _rep(b"Signature=" + b"A" * 64 + b"\\u0026Key-Pair-Id=" + b"a" * 8 + b"\\u0026Expires=1", n)


CASES = [
    ("cf-sig-run", cf_sig_run),
    ("cf-sig-run-badkpi", cf_sig_run_badkpi),
    ("cf-sig-many", cf_sig_many),
    ("cf-sig-tail", cf_sig_tail),
    ("cf-sig-keysoup", cf_sig_keysoup),
    ("cf-kpi-chain", cf_kpi_chain),
    ("cf-kpi-first-nosig", cf_kpi_first_nosig),
    ("cf-u0026", cf_u0026),
    ("cf-pct26", cf_pct26),
    ("cf-amp-chain", cf_amp_chain),
    ("cf-kpi-longrun", cf_kpi_longrun),
    ("cf-sig-params", cf_sig_params),
    ("cf-sig40-badkpi", cf_sig40_badkpi),
    ("az-sv-dense", az_sv_dense),
    ("az-pct26", az_pct26),
    ("az-u0026", az_u0026),
    ("az-pct26-sig", az_pct26_sig),
    ("az-sig-run", az_sig_run),
    ("az-sig-run-svtail", az_sig_run_sv_tail),
    ("az-amp-chain", az_amp_chain),
    ("az-u0026-sig39", az_u0026_sig39),
    ("az-u0026-longval", az_u0026_longval),
    ("az-sv-sig39", az_sv_sig39),
    ("cf-sig39-many", cf_sig39_many),
    ("cf-many-long", cf_many_long),
    ("cf-u0026-sig", cf_u0026_sig),
    ("plain", plain),
]


def load(inst):
    spec = importlib.util.spec_from_file_location(
        "css", os.path.join(inst, "capture-secret-scan.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def slope(points):
    """Least-squares slope of log10(t) on log10(n)."""
    xs = [math.log10(n) for n, _ in points]
    ys = [math.log10(t) for _, t in points]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--inst", required=True)
    ap.add_argument("--sizes", default="10240,102400,1048576,4194304")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--only")
    ap.add_argument("--regex", default="both", choices=("full", "cf", "az", "both"))
    a = ap.parse_args(argv)
    sizes = [int(x) for x in a.sizes.split(",")]
    m = load(a.inst)
    pats = m.patterns()
    cf = dict(m.CLOUD_PATTERNS)["cloudfront-signed-url-signature"]
    az = dict(m.CLOUD_PATTERNS)["azure-sas-signature"]
    print("INSTRUMENT shapes=%d names=%s" % (len(pats), ",".join(n for n, _ in pats)))

    # Calibration: fixed work on a fixed buffer, independent of the row.
    cbuf = b"a" * (1450 * 1024)
    def cal():
        t = time.perf_counter()
        az.search(cbuf)
        return time.perf_counter() - t
    base = min(cal() for _ in range(5))
    print("CALIB baseline=%.4f" % base)

    only = set(a.only.split(",")) if a.only else None
    rows = []
    for name, fn in CASES:
        if only and name not in only:
            continue
        pts = {k: [] for k in ("full", "cf", "az")}
        for n in sizes:
            data = fn(n)
            nhit = {"full": 0, "cf": 0, "az": 0}
            for rx, key in ((cf, "cf"), (az, "az")):
                nhit[key] = sum(1 for _ in rx.finditer(data))
            nhit["full"] = len(m.scan_bytes(data, pats)[0])
            for key, run in (("full", lambda d: m.scan_bytes(d, pats)),
                             ("cf", lambda d: sum(1 for _ in cf.finditer(d))),
                             ("az", lambda d: sum(1 for _ in az.finditer(d)))):
                if a.regex != "both" and key != a.regex:
                    continue
                best, bestcal = None, None
                for _ in range(a.reps + 2):
                    c = cal()
                    t0 = time.perf_counter()
                    run(data)
                    dt = time.perf_counter() - t0
                    if best is None or dt < best:
                        best, bestcal = dt, c
                    if c <= 3 * base:
                        break
                pts[key].append((len(data), best))
                rows.append((name, key, len(data), best, bestcal, nhit[key]))
        for key, p in pts.items():
            if len(p) >= 2:
                print("ROW %-20s %-4s exp=%.3f  %s" % (
                    name, key, slope(p),
                    " ".join("%d:%.4f" % (n, t) for n, t in p)))
    print("TSV case\tregex\tsize\tsec\tcal\thits")
    for r in rows:
        print("TSV %s\t%s\t%d\t%.6f\t%.6f\t%d" % r)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
