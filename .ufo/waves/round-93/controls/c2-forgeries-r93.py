#!/usr/bin/env python3
"""Round-93 C2 forgeries: each is the frozen round-93 candidate scanner (read from
the committed wave file) with one targeted change, written to OUTDIR. Every
replacement must apply exactly once; nothing is written on a refusal.

Usage: c2-forgeries-r93.py CANDIDATE OUTDIR
"""
import os
import sys

CAND = open(sys.argv[1] if len(sys.argv) > 1 else "", encoding="utf-8").read() if len(sys.argv) > 1 else ""
OUT = sys.argv[2] if len(sys.argv) > 2 else ""

GL = '("gitlab-pat", re.compile(_GL_LB + rb"glpat-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])")),'
ESC = '_ESC_LB = rb"(?:(?<![A-Za-z0-9_])|(?<=\\\\[ntr])|(?<=\\\\u[0-9A-Fa-f]{4})|(?<=%[0-9A-Fa-f]{2})|(?<=&#[0-9]{2};)|(?<=&#[xX][0-9A-Fa-f]{2};))"'
FORGERIES = {
    "G1-no-gitlab": [(" + GITLAB_PATTERNS", "")],
    "G2-gl-loose-length": [(GL, GL.replace("{20}", "{3,}"))],
    "G3-gl-no-right-boundary": [(GL, GL.replace("(?![A-Za-z0-9_-])", ""))],
    "G4-gl-any-prefix": [(GL, GL.replace("glpat-", "gl[a-z]+-"))],
    "G5-escape-tab-only": [(ESC, '_ESC_LB = rb"(?:(?<![A-Za-z0-9_])|(?<=\\\\t))"')],
    "G6-escape-letter": [(ESC, '_ESC_LB = rb"(?:(?<![A-Za-z0-9_])|(?<=[A-Za-z]))"')],
    "G7-literal-keyed": [(GL, GL.replace("glpat-[A-Za-z0-9_-]{20}", "glpat-0123456789abcdefghij"))],
    "G8-path-keyed": [("def scan_bytes(data, pats, path=\"\", allow=None, used=None):",
                        "def scan_bytes(data, pats, path=\"\", allow=None, used=None):\n    if path.startswith(\"corpus/source-snapshots/round-1/\"):\n        return [(\"gitlab-pat\", 1)] if \"S035\" in path else [(\"github-token\", 1)], 0\n    return [], 0")],
    "G9-tampered-no-logic-change": [('"""Scan captured evidence for credential material before it is committed.',
                                     '"""Scan captured evidence for credential material before it is committed. (tampered)')],
    "G10-always-clean": [("def scan_bytes(data, pats, path=\"\", allow=None, used=None):",
                          "def scan_bytes(data, pats, path=\"\", allow=None, used=None):\n    return [], 0")],
}


def main():
    if not CAND or not OUT:
        print("usage: c2-forgeries-r93.py CANDIDATE OUTDIR")
        return 2
    os.makedirs(OUT, exist_ok=True)
    bad = 0
    for name, reps in FORGERIES.items():
        text = CAND
        for old, new in reps:
            if text.count(old) != 1:
                print("FORGERY %s refused count=%d" % (name, text.count(old)))
                bad += 1
                continue
            text = text.replace(old, new)
        if text != CAND:
            with open(os.path.join(OUT, name + ".py"), "w", encoding="utf-8") as fh:
                fh.write(text)
            print("FORGERY %s written" % name)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
