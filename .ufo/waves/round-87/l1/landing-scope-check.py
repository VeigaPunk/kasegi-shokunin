#!/usr/bin/env python3
"""Round-87 landing-scope check (lesson M87-2, QUALITY R139).

Usage: landing-scope-check.py --lane LANE --from REV --to REV --scope PREFIX [--scope PREFIX ...]

Lists `git diff --name-only FROM TO` and fails when any changed path lies
outside every --scope prefix (a prefix ending in '/' matches a directory, any
other prefix must equal the path). Run it on the landing commit BEFORE citing
it for a claim whose predicate bounds the landing diff; derive the commit's
path list from `git status --porcelain -- <scope>`, never from an unscoped
`git status` (round 87: an unscoped list swept three untracked wave files into
the C1 landing d87b1b55).
Prints `LANDING-SCOPE from=.. to=.. changed=N outside=M verdict=PASS|FAIL exit=0|1`.
"""
import argparse
import subprocess
import sys


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--from", dest="frm", required=True)
    ap.add_argument("--to", required=True)
    ap.add_argument("--scope", action="append", required=True)
    a = ap.parse_args(argv)
    try:
        out = subprocess.run(["git", "-C", a.lane, "diff", "--name-only", "--no-renames", a.frm, a.to],
                             capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        print("LANDING-SCOPE error reason=git exit=2")
        return 2
    paths = [p for p in out.split("\n") if p]

    def inside(p):
        return any(p.startswith(s) if s.endswith("/") else p == s for s in a.scope)

    outside = [p for p in paths if not inside(p)]
    for p in outside:
        print("OUTSIDE %s" % p)
    ok = bool(paths) and not outside
    print("LANDING-SCOPE from=%s to=%s changed=%d outside=%d verdict=%s exit=%d"
          % (a.frm[:8], a.to[:8], len(paths), len(outside), "PASS" if ok else "FAIL", 0 if ok else 1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
