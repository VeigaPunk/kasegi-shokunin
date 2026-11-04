#!/usr/bin/env python3
"""Side-by-side: same derive through base gate and candidate gate.

Usage: battery.py --base PATH --cand PATH
Each one-line case prints: ID | base exit/reason | cand exit/reason
"""
import argparse
import re
import subprocess
import sys

HERE = "/fast/scratch/hyaku/kasegi-r65/CriticC1"
CASES = [
    ("P1-sigterm-producer", "python3 corpus/instruments/kill.py | wc -l", "0"),
    ("P2-sigkill-producer", "python3 corpus/instruments/kill9.py | wc -l", "0"),
    ("P3-final-signal", "cat g.txt | python3 corpus/instruments/kill.py", ""),
    ("P4-sigpipe-c-head", "cat big.txt | head -n 1", "line000001"),
    ("P4b-sigpipe-python", "python3 corpus/instruments/bigwriter.py | head -n 1", "35"),
    ("P5-clean", "cat g.txt | wc -l", "1"),
    ("P6-grep-nomatch", "grep absent g.txt | wc -l", "0"),
    ("P7-child-killed-rc0", "python3 corpus/instruments/childkill.py | wc -l", "1"),
    ("P8-complete-then-sigterm", "python3 corpus/instruments/printthenkill.py | wc -l", "1"),
    ("P9-masked-by-and", "python3 corpus/instruments/kill.py | wc -l && cat g.txt", "0\n35"),
    ("P10-sigpipe-masks-missing", "cat big.txt missing.txt | head -n 1", "line000001"),
    ("P11-empty-exit0-want0", "python3 corpus/instruments/exit0empty.py | wc -l", "0"),
    ("P12-segv-producer", "python3 corpus/instruments/segv.py | wc -l", "0"),
    ("P13-signal-caught-rc0", "python3 corpus/instruments/maskterm.py | wc -l", "1"),
    ("P14-truncated-input", "cat trunc.txt | wc -l", "2"),
]


def run(instrument, cid, derive, want):
    p = subprocess.run([sys.executable, HERE + "/probe.py", "--instrument", instrument,
                        "--id", cid, "--derive", derive, "--want", want],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    out = p.stdout.decode("utf-8", "replace")
    m = re.search(r"PROBE id=(\S+) exit=(\d+) reason=(\S+)", out)
    return out, (int(m.group(2)), m.group(3)) if m else (None, "?")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--cand", required=True)
    a = ap.parse_args()
    print("%-28s %-26s %-26s" % ("CASE", "BASE", "CANDIDATE"))
    for cid, derive, want in CASES:
        ob, rb = run(a.base, cid + "-b", derive, want)
        oc, rc = run(a.cand, cid + "-c", derive, want)
        print("%-28s exit=%-3s %-16s exit=%-3s %-16s" % (cid, rb[0], rb[1], rc[0], rc[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
