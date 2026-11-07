#!/usr/bin/env python3
"""Round-94 C2 harm repair: re-anchor the knowledge citations the C2 landing shifted.

The C2 landing grew corpus/instruments/capture-secret-scan.py from 458 to 491
lines, so every `capture-secret-scan.py:N[-M]` citation into it may now point at
other text (round-93 R143/R144; CriticHarm's named harm).  This tool maps each
cited base line to its tip line by content (difflib equal blocks), prints the
map, flags every citation inside a rewritten block for a hand disposition, and
rewrites the tokens only when `--apply` is given.

Usage:
  reanchor-r94.py LANE BASE_REV [--apply]
Writes the map to stdout (old token -> new token per site) and a summary line.
"""
import difflib
import os
import re
import subprocess
import sys

SCAN = "corpus/instruments/capture-secret-scan.py"
TOKEN = re.compile(r"`(corpus/instruments/capture-secret-scan\.py):(\d+)(?:-(\d+))?`")
ENTRIES = [
    "corpus/knowledge/github-prefixed-tokens-in-captured-evidence.md",
    "corpus/knowledge/capture-intake-gate.md",
    "corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md",
    "corpus/knowledge/cloud-signed-cookies-and-user-bound-sas.md",
    "corpus/knowledge/presigned-url-credentials-in-captured-evidence.md",
]


def git(lane, *args):
    return subprocess.run(["git", "-C", lane] + list(args), capture_output=True, text=True, check=True).stdout


def lines_of(text):
    return text.split("\n")


def mapping(base, tip):
    """{base_line_no: tip_line_no} for lines that survive unchanged."""
    sm = difflib.SequenceMatcher(a=base, b=tip, autojunk=False)
    m = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                m[i1 + k + 1] = j1 + k + 1
    return m, [(tag, i1 + 1, i2, j1 + 1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]


def main(argv):
    lane = os.path.abspath(argv[0])
    base_rev = argv[1]
    apply = "--apply" in argv
    base = lines_of(git(lane, "show", "%s:%s" % (base_rev, SCAN)))
    tip = lines_of(open(os.path.join(lane, SCAN), encoding="utf-8").read())
    m, changed = mapping(base, tip)
    print("# base scanner lines=%d tip lines=%d unchanged=%.1f%%" % (len(base), len(tip), 100.0 * len(m) / len(base)))
    for tag, i1, i2, j1, j2 in changed:
        print("# changed base %d-%d -> tip %d-%d (%s)" % (i1, i2, j1, j2, tag))
    hand, rewrites = [], []
    for rel in ENTRIES:
        path = os.path.join(lane, rel)
        text = open(path, encoding="utf-8").read()
        lines = text.split("\n")
        for i, ln in enumerate(lines, 1):
            for mt in TOKEN.finditer(ln):
                n = int(mt.group(2))
                hi = int(mt.group(3)) if mt.group(3) else n
                if n in m and hi in m:
                    old = mt.group(0)
                    new = "`%s:%d-%d`" % (mt.group(1), m[n], m[hi]) if mt.group(3) else "`%s:%d`" % (mt.group(1), m[n])
                    if new != old:
                        rewrites.append((rel, i, old, new))
                else:
                    hand.append((rel, i, mt.group(0)))
        if apply:
            def sub(mt):
                n = int(mt.group(2))
                hi = int(mt.group(3)) if mt.group(3) else n
                if n in m and hi in m:
                    return "`%s:%d-%d`" % (mt.group(1), m[n], m[hi]) if mt.group(3) else "`%s:%d`" % (mt.group(1), m[n])
                return mt.group(0)
            new_text = TOKEN.sub(sub, text)
            if new_text != text:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new_text)
    for rel, i, old, new in rewrites:
        print("REANCHOR %s:%d %s -> %s" % (rel, i, old, new))
    for rel, i, tok in hand:
        print("HAND %s:%d %s (inside a rewritten block)" % (rel, i, tok))
    print("REANCHOR-RESULT rewrites=%d hand=%d applied=%s" % (len(rewrites), len(hand), apply))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
