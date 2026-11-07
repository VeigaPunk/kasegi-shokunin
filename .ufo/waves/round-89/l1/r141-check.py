#!/usr/bin/env python3
"""QUALITY R141 check (round 89, lesson M89-1): every planted case a capability counter
expects the instrument to HIT lies inside the instrument's own scan scope.

Usage: r141-check.py --counter COUNTER.py --scanner SCANNER.py [--seed N]
Loads the counter as a module (no main run) and the scanner's is_capture_path();
collects every (path, shape) the counter expects as a hit from PLANT_EXPECT and,
when the counter defines generated(seed), from its expected set; a path for
which is_capture_path() is False can never be hit in --rev mode, so the limb
that expects it fails for every candidate (round 89 first controls run: the
positive control failed K7 on g/source-snapshots/G1.txt).
Prints `R141 expected=N out_of_scope=M verdict=PASS|FAIL exit=0|1` (one
`R141 OUT <path>` line per offender). Exit 2 on a load error.
"""
import argparse
import importlib.util
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--scanner", required=True)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args(argv)
    try:
        c = load(a.counter, "r141_counter")
        s = load(a.scanner, "r141_scanner")
        expected = set(c.PLANT_EXPECT)
        if hasattr(c, "generated"):
            expected |= set(c.generated(a.seed)[1])
    except Exception as e:  # noqa: BLE001 - any load failure is a read error
        print("R141 error reason=%s exit=2" % type(e).__name__)
        return 2
    out = sorted({p for p, _ in expected if not s.is_capture_path(p)})
    for p in out:
        print("R141 OUT %s" % p)
    ok = not out
    print("R141 expected=%d out_of_scope=%d verdict=%s exit=%d" % (len(expected), len(out), "PASS" if ok else "FAIL", 0 if ok else 1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
