#!/usr/bin/env python3
"""Round-92 integration (R143; copy of the round-91 tool, out-of-range tokens reported as SKIP): re-anchor knowledge citations of
corpus/instruments/capture-secret-scan.py from the round-91 base bytes to the C2 landing
bytes. The line map is derived with difflib from `git show BASE:` and `git show LANDING:`
(equal blocks shift; a replaced block maps start->start of its replacement and
end->end of its replacement). Rewrites `corpus/instruments/capture-secret-scan.py:N[-M]`
and bare backticked `:N[-M]` tokens whose nearest preceding full-path citation on the
same line is the scanner, or, on the FILE:LINE pairs given by --bare-lines, that have no
preceding full-path citation (the entry's context names the scanner). Prints one CHANGE
line per token; --apply writes the files. Idempotence is not claimed: run once, from base
line numbers.
Usage: reanchor-scanner-cites.py --lane L --base REV --landing REV [--bare-lines F:N,...] [--apply] FILE...
"""
import argparse
import difflib
import re
import subprocess
import sys

INSTR = "corpus/instruments/capture-secret-scan.py"
TOK = re.compile(r"`((?:corpus/[A-Za-z0-9_./-]+\.(?:py|md|txt|tsv|json))?):(\d+)(?:-(\d+))?`")
FULL = re.compile(r"`(corpus/[A-Za-z0-9_./-]+?)(?::[0-9][0-9-]*)?`")


def line_map(b, a):
    start, end = {}, {}
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, b, a, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                start[i1 + k + 1] = end[i1 + k + 1] = j1 + k + 1
        elif op == "replace":
            for k in range(i1, i2):
                start[k + 1] = j1 + 1
                end[k + 1] = j2
    return start, end


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--landing", required=True)
    ap.add_argument("--bare-lines", default="")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("files", nargs="+")
    a = ap.parse_args(argv)
    bare = set(x for x in a.bare_lines.split(",") if x)

    def show(rev):
        return subprocess.run(["git", "-C", a.lane, "show", "%s:%s" % (rev, INSTR)],
                              capture_output=True, text=True, check=True).stdout.split("\n")

    smap, emap = line_map(show(a.base), show(a.landing))
    n = 0
    for f in a.files:
        path = "%s/%s" % (a.lane, f)
        lines = open(path, encoding="utf-8").read().split("\n")
        for i, ln in enumerate(lines):
            out = []
            for m in TOK.finditer(ln):
                fulls = [x.group(1) for x in FULL.finditer(ln[:m.start()])]
                name = m.group(1) or (fulls[-1] if fulls else None)
                if name is None and "%s:%d" % (f, i + 1) in bare:
                    name = INSTR
                if name != INSTR:
                    continue
                lo = int(m.group(2))
                hi = int(m.group(3)) if m.group(3) else None
                if lo not in smap or (hi and hi not in emap):
                    print("SKIP %s:%d %s (outside the base instrument)" % (f, i + 1, m.group(0)))
                    continue
                nlo = smap[lo]
                nhi = emap[hi] if hi else (emap[lo] if emap[lo] != smap[lo] else None)
                new = "`%s:%d%s`" % (m.group(1), nlo, "-%d" % nhi if nhi and nhi != nlo else "")
                if new != m.group(0):
                    out.append((m.start(), m.end(), new))
                    print("CHANGE %s:%d %s -> %s" % (f, i + 1, m.group(0), new))
                    n += 1
            for s, e, new in reversed(out):
                ln = ln[:s] + new + ln[e:]
            lines[i] = ln
        if a.apply:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines))
    print("REANCHOR changes=%d applied=%s" % (n, a.apply))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
