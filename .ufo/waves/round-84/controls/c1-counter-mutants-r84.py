#!/usr/bin/env python3
"""c1-counter-mutants-r84.py — round-84 C1 counter control (r83 MutCounter M09, M10, M12).

Applies three counter mutants to the round-83 counter (.ufo/waves/round-83/c1/mutbat.py) and to
the round-84 counter (.ufo/waves/round-84/c1/mutbat.py), byte-identical edits in both, and runs
each mutant's --selftest:

  M09  the `extra` loop body no longer applies the extra replacement
  M10  the `extra` loop no longer refuses an extra anchor that occurs != 1 times
  M12  the DECOY line is no longer appended

Expected: each mutant prints 'mutbat selftest ok' (rc 0) under r83 (the r83 selftest does not
exercise these limbs) and 'mutbat selftest FAIL' (rc 1) under r84.
Prints one 'COUNTER-MUTANT <id> counter=<r83|r84> rc=<n> selftest=<ok|FAIL>' line per run and
exits 0 when every expectation holds, 1 otherwise, 2 when an anchor is not unique.
Usage: c1-counter-mutants-r84.py --lane DIR --work DIR
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

MUTANTS = [
    ("M09", "        out = out.replace(anchor, repl, 1)\n", "        out = out\n"),
    ("M10", "        if out.count(anchor) != 1:\n            return None\n        out = out.replace(",
     "        out = out.replace("),
    ("M12", '    lines.append("DECOY keyed=%s nonce=%s d3_row=%s"\n'
            '                 % ("no" if legacy else "yes", nonce or "-", d3_id or "-"))\n', ""),
]
COUNTERS = [("r83", ".ufo/waves/round-83/c1/mutbat.py"), ("r84", ".ufo/waves/round-84/c1/mutbat.py")]


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    d = tempfile.mkdtemp(prefix="ctrmut-", dir=a.work)
    good = True
    try:
        for cname, rel in COUNTERS:
            with open(os.path.join(a.lane, rel), encoding="utf-8") as fh:
                src = fh.read()
            for mid, anchor, repl in MUTANTS:
                if src.count(anchor) != 1:
                    print("COUNTER-MUTANT %s counter=%s anchor-count=%d" % (mid, cname, src.count(anchor)))
                    return 2
                path = os.path.join(d, "%s-%s.py" % (cname, mid))
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(src.replace(anchor, repl, 1))
                w = os.path.join(d, "w-%s-%s" % (cname, mid))
                os.makedirs(w)
                p = subprocess.run([sys.executable, "-B", path, "--selftest", "--work", w],
                                   capture_output=True, text=True, timeout=600)
                st = "ok" if "mutbat selftest ok" in p.stdout else "FAIL"
                print("COUNTER-MUTANT %s counter=%s rc=%d selftest=%s" % (mid, cname, p.returncode, st))
                want = (0, "ok") if cname == "r83" else (1, "FAIL")
                good = good and (p.returncode, st) == want
    finally:
        shutil.rmtree(d, ignore_errors=True)
    print("COUNTER-MUTANTS-RESULT %s" % ("as-expected" if good else "unexpected"))
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
