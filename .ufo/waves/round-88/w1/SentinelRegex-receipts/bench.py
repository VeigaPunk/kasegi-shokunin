#!/usr/bin/env python3
"""Timing probe for capture-secret-scan's round-88 cloud patterns.

Usage: bench.py CASE SIZE [--only azure|gcs|all] [--reps N]

Builds an adversarial byte string of >= SIZE bytes from scratch, then times
scan_bytes (full pattern set, the way a capture is scanned) and, separately,
the azure / gcs regex alone. Prints one JSON line. Never prints input bytes.
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "inst"))
import importlib.util

spec = importlib.util.spec_from_file_location(
    "css", os.path.join(HERE, "inst", "capture-secret-scan.py"))
css = importlib.util.module_from_spec(spec)
spec.loader.exec_module(css)

SV = b"sv=2022-11-02&"
SIGP = b"sig="


def pad(b, n):
    if len(b) >= n:
        return b[:n]
    r = n - len(b)
    return b + b"x" * r


def build(case, n):
    if case == "many-params":
        # one long query string of short params, no sv, no sig
        unit = b"&ab=12"
        b = b"https://h.example/p?a=1"
        k = max(0, (n - len(b)) // len(unit))
        return pad(b + unit * k, n)
    if case == "sv-no-sig":
        # sv=YYYY-MM-DD& repeated: every sv is a candidate start, never a sig
        k = max(1, n // len(SV))
        return pad(SV * k, n)
    if case == "gcs-hex":
        # one 4 MB hex run right after the parameter name
        return b"X-Goog-Signature=" + b"a" * (n - 17)
    if case == "gcs-hex-upper":
        return b"X-Goog-Signature=" + b"A" * (n - 17)
    if case == "gcs-near-miss":
        # 63 hex digits then a non-hex char, repeated: no match, full scan
        unit = b"X-Goog-Signature=" + b"a" * 63 + b"z"
        k = max(1, n // len(unit))
        return pad(unit * k, n)
    if case == "gcs-spaces":
        # name followed by a huge whitespace run and no ':' (backtracks the run)
        return b"X-Goog-Signature" + b" " * (n - 16)
    if case == "sig39":
        # sig= with 39 chars (one short of the class) and a separator
        unit = b"sig=" + b"A" * 39 + b"&"
        k = max(1, n // len(unit))
        return pad(unit * k, n)
    if case == "sig-nosep":
        unit = b"sig=" + b"A" * 39
        k = max(1, n // len(unit))
        return pad(unit * k, n)
    if case == "sig-longtail":
        # the azure long-tail shape, sig branch: k sv= candidate starts (cheap)
        # then one shared long class run begun by sig= and cut by a space
        k = max(1, n // 4 // len(SV))
        head = SV * k
        tail = SIGP + b"B" * max(1, n - len(head) - 4 - 1) + b" "
        return head + tail
    if case == "sv-longtail":
        # PRIMARY quadratic candidate: k sv= candidate starts, then ONE shared
        # long in-class run that ends at a space, so every one of the k starts
        # backtracks the whole run once the lazy {0,20} window is exhausted.
        k = max(1, n // 4 // len(SV))
        head = SV * k + b"ab="
        tail = b"x" * max(1, n - len(head) - 1) + b" "
        return head + tail
    if case == "sv-longtail-quote":
        k = max(1, n // 4 // len(SV))
        head = SV * k + b"ab="
        tail = b"x" * max(1, n - len(head) - 1) + b'"'
        return head + tail
    if case == "amp-entities":
        unit = b"&amp;"
        k = max(1, n // len(unit))
        return pad(unit * k, n)
    if case == "u0026-blocks":
        k = max(1, n // (len(SV) + 6))
        return pad((SV + b"\\u0026sr=b") * k, n)
    if case == "realistic-sas":
        head = b"https://a.blob.core.windows.net/c/b.txt?sp=r&st=2026-11-07T00:00:00Z&se=2026-11-08T00:00:00Z&spr=https&"
        unit = b"sv=2022-11-02&sr=b&"
        k = max(1, n // len(unit))
        return pad(head + unit * k, n)
    if case == "sig-giant":
        # one sig= then a single in-class run to end of input, no separator
        return SIGP + b"A" * (n - 4)
    if case == "sv-giant-value":
        # one sv=, one param, one giant value cut by a space
        return SV + b"ab=" + b"x" * (n - 4 - len(SV) - 1) + b" "
    if case == "sv-sig39":
        # maximum alternation pressure: a full 21-param window per start, no hit
        unit = SV + b"sig=" + b"C" * 39 + b"&"
        k = max(1, n // len(unit))
        return pad(unit * k, n)
    if case == "sig40-svbad":
        unit = SIGP + b"D" * 40 + b"&sv=abcd-ef-gh&"
        k = max(1, n // len(unit))
        return pad(unit * k, n)
    if case == "amp-soup":
        unit = b"&amp;a=1&amp;b=2&amp;c=3"
        k = max(1, n // len(unit))
        return pad(unit * k, n)
    if case == "u0026-chain":
        unit = SV + b"\\u0026sr=b\\u0026_=1"
        k = max(1, n // len(unit))
        return pad(unit * k, n)
    raise SystemExit("unknown case %r" % case)


def timeit(fn, reps):
    best = None
    out = None
    for _ in range(reps):
        t0 = time.perf_counter()
        out = fn()
        dt = time.perf_counter() - t0
        if best is None or dt < best:
            best = dt
    return best, out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("case")
    ap.add_argument("size", type=int)
    ap.add_argument("--only", default="all")
    ap.add_argument("--reps", type=int, default=1)
    a = ap.parse_args(argv)
    data = build(a.case, a.size)
    pats = css.patterns()
    rec = {"case": a.case, "size": a.size, "nbytes": len(data)}
    az = dict(css.CLOUD_PATTERNS)["azure-sas-signature"]
    gc = dict(css.CLOUD_PATTERNS)["gcs-signed-url-signature"]
    if a.only in ("all", "full"):
        dt, (found, allowed) = timeit(lambda: css.scan_bytes(data, pats), a.reps)
        rec["full_sec"] = round(dt, 6)
        rec["full_hits"] = [s for s, _ in found]
    if a.only in ("all", "azure"):
        dt, m = timeit(lambda: az.finditer(data).__next__, 1) if False else (None, None)
        t0 = time.perf_counter()
        hit = 0
        for m in az.finditer(data):
            hit += 1
            break
        rec["azure_sec"] = round(time.perf_counter() - t0, 6)
        rec["azure_hit"] = bool(hit)
    if a.only in ("all", "gcs"):
        t0 = time.perf_counter()
        hit = 0
        for m in gc.finditer(data):
            hit += 1
            break
        rec["gcs_sec"] = round(time.perf_counter() - t0, 6)
        rec["gcs_hit"] = bool(hit)
    import hashlib
    rec["input_sha256"] = hashlib.sha256(data).hexdigest()
    print(json.dumps(rec, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
