#!/usr/bin/env python3
"""SentinelCookie round-99: randomized structural fuzz of the landed window.

4000 payloads built from the operator/gap/cell/value vocabulary; any cell the
landed gate misses while the S140 translation hits is printed as a candidate
MUST-FIX. Payloads are printed with the 64-hex value replaced by <H64> so the
receipt stays clean under the landed scanner.
"""
import importlib.util
import os
import random
import re
import shutil
import sys

H = b"0123456789abcdef" * 4
S140 = re.compile(rb"_gitlab_session(?:_geo_[0-9a-f]{64})?.{0,8}[:=].{0,8}"
                  rb"(?:cell-[0-9]+-)?[0-9a-f]{64}")
POOL = [b"=", b":", b" ", b"\t", b",", b"|", b"+", b"(", b")", b"<", b">",
        b"%20", b"%3A", b"%3D", b"&", b"#", b";", b"'", b'"', b"\\", b".",
        b"/", b"_", b"-", b"x", b"0", b"cell-", b"cell-12-", b"cell--",
        b"cell-abc-", b"\\n", b"\r", b"foo", b"a1"]
VALS = [H, H, H, H, H[:63], H + b"0", H + b"0123456789", H.upper(),
        H[:32] + b"-" + H[33:], b"cell-12-" + H, b"cell--" + H]


def show(d):
    return d.replace(H, b"<H64>").decode("latin-1").encode("unicode_escape").decode()


def load(path, lane, work, tag):
    stage = os.path.join(work, "inst-" + tag)
    os.makedirs(stage, exist_ok=True)
    dst = os.path.join(stage, "capture-secret-scan.py")
    shutil.copyfile(path, dst)
    shutil.copyfile(os.path.join(lane, "corpus", "instruments", "claim-package-check.py"),
                    os.path.join(stage, "claim-package-check.py"))
    spec = importlib.util.spec_from_file_location("scanner_" + tag, dst)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    lane, work = argv[1], argv[2]
    landed = load(os.path.join(lane, "corpus", "instruments", "capture-secret-scan.py"),
                  lane, work, "landed4")
    pats = landed.patterns()
    rng = random.Random(99)
    counts = {}
    must = []
    for i in range(4000):
        sep = b"".join(rng.choice(POOL) for _ in range(rng.randint(0, 3)))
        data = b"_gitlab_session" + sep + rng.choice(VALS) + rng.choice([b"\n", b"", b"x", b'"'])
        got = {s for s, _ in landed.scan_bytes(data, pats)[0]}
        sb = bool(S140.search(data))
        v = ("MUST-FIX" if not got and sb else
             "AGREE-HIT" if got and sb else
             "SCANNER-ONLY" if got else "AGREE-MISS")
        counts[v] = counts.get(v, 0) + 1
        if v == "MUST-FIX":
            must.append(show(data))
    print("FUZZ cases=4000 %s" % " ".join("%s=%d" % (k, counts[k]) for k in sorted(counts)))
    seen = set()
    for m in must:
        if m not in seen:
            seen.add(m)
            print("FUZZ MUST-FIX %s" % m)
    print("FUZZ distinct_mustfix=%d" % len(seen))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
