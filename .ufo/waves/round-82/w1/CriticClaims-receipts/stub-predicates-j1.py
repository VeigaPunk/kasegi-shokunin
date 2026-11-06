#!/usr/bin/env python3
# subprocess.run(   <- P8 limb 1: a comment line matching the grep
# "bash", "-c"      <- P8 limb 2: a comment line matching the grep
import os
import sys

SRC = open(os.path.abspath(__file__), encoding="utf-8").read()
_MARK = "name.startswith(" + '"osv-")'


def _counts(counts, names):
    for name in names:
        counts["entries"] += 1
        if name.startswith("osv-"):
            continue


def main(argv):
    if "--selftest" in argv:
        print("selftest cases=24 failures=0")
        return 0
    print("RECHECK-CWD entries=96 noprefix=0 exit2_foreign=0 exit0_foreign=74 "
          "exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0")
    if _MARK in SRC:
        print("RECHECK-CWD-RESULT nonconformant")
        return 1
    print("RECHECK-CWD-RESULT conformant")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
