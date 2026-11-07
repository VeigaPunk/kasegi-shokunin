#!/usr/bin/env python3
"""Write the round-92 C2 forgeries of the frozen candidate scanner into OUTDIR.
Each forgery is the frozen candidate (read from the committed wave file) with one
targeted change; every replacement must apply exactly once or nothing is written.
  F1 classic-only       stateless ghs_<APPID>_<JWT> alternative removed
  F2 stateless-only     classic 36-character alternative removed
  F3 no-length-cap      {36} -> {36,} (37-character negative now hits)
  F4 loose-length       {36} -> {30,} (35-character negative now hits)
  F5 case-insensitive   (?i) on the shape (GHP_ now hits)
  F6 no-lookbehind      left boundary dropped (xghp_ now hits)
  F7 any-prefix         gh[pousr] -> gh[a-z] (ghx_ now hits)
  F8 literal-keyed      classic tail keyed on the K4 fixture literal prefix
  F9 no-json-newline    left boundary drops the JSON `\\n` join (live-j plant missed)
  F10 short-segments    stateless JWT segment floor {10,} -> {1,} (ghs_<id>_a.b.c now hits)
Usage: c2-forgeries.py CANDIDATE OUTDIR
"""
import os
import sys

CL = 'gh[pousr]_[A-Za-z0-9]{36}(?![A-Za-z0-9_])'
ST = '|ghs_[0-9]{1,20}_"\n        + _JWT_SEG + rb"\\." + _JWT_SEG + rb"\\." + _JWT_SEG + rb")'
FORGERIES = {
    "F1-classic-only": [(ST, ')')],
    "F2-stateless-only": [(CL + '|', '')],
    "F3-no-length-cap": [(CL, 'gh[pousr]_[A-Za-z0-9]{36,}')],
    "F4-loose-length": [(CL, 'gh[pousr]_[A-Za-z0-9]{30,}(?![A-Za-z0-9_])')],
    "F5-case-insensitive": [('_GH_LB + rb"(?:gh', 'rb"(?i)" + _GH_LB + rb"(?:gh')],
    "F6-no-lookbehind": [('        _GH_LB + rb"(?:gh', '        rb"(?:gh')],
    "F7-any-prefix": [(CL, 'gh[a-z]_[A-Za-z0-9]{36}(?![A-Za-z0-9_])')],
    "F8-literal-keyed": [(CL, 'gh[pousr]_PLANTED[A-Za-z0-9]{29}(?![A-Za-z0-9_])')],
    "F9-no-json-newline": [('_GH_LB = rb"(?:(?<![A-Za-z0-9_])|(?<=\\\\n))"', '_GH_LB = rb"(?<![A-Za-z0-9_])"')],
    "F10-short-segments": [('_JWT_SEG = rb"[A-Za-z0-9_-]{10,}"', '_JWT_SEG = rb"[A-Za-z0-9_-]{1,}"')],
}


def main(argv):
    cand, out = argv[0], argv[1]
    src = open(cand, encoding="utf-8").read()
    os.makedirs(out, exist_ok=True)
    for name, reps in FORGERIES.items():
        text = src
        for old, new in reps:
            if text.count(old) != 1:
                print("FORGERY %s refused count=%d" % (name, text.count(old)))
                return 1
            text = text.replace(old, new)
        with open(os.path.join(out, name + ".py"), "w", encoding="utf-8") as fh:
            fh.write(text)
        print("FORGERY %s written" % name)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
