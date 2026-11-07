#!/usr/bin/env python3
"""Synthetic boundary probes for the two round-95 scanner shapes.

All values are constructed from repeated synthetic characters; no real token
and no committed example value is used or printed.
"""
import importlib.util

spec = importlib.util.spec_from_file_location("css", "corpus/instruments/capture-secret-scan.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def hit(data):
    found = m.scan_bytes(data, m.GITHUB_PATTERNS + m.GITLAB_PATTERNS)[0]
    return ",".join(sorted(s for s, _ in found)) or "none"


A = b"aB3" * 25 + b"a"          # 76 synthetic characters
J1 = b"x" * 20
J2 = b"y" * 20
J3 = b"z" * 30
rows = [
    ("gh-76", b"ghr_" + A),
    ("gh-75", b"ghr_" + b"aB3" * 25),
    ("gh-77", b"ghr_" + b"aB3" * 25 + b"aa"),
    ("gh-36-classic", b"ghr_" + b"a" * 36),
    ("gh-letter-before", b"xghr_" + A),
    ("gh-esc-backslash-n", b'"line\\nghr_' + A + b'"'),
    ("gh-esc-u0020", b'"v":"\\u0020ghr_' + A + b'"'),
    ("gh-esc-pct20", b"%20ghr_" + A),
    ("gh-esc-amp32", b"&#32;ghr_" + A),
    ("gh-esc-ampx20", b"&#x20;ghr_" + A),
    ("gh-follow-underscore", b"ghr_" + A + b"_"),
    ("gl-clcbt", b"glcbt-eyJ" + J1 + b".eyJ" + J2 + b"." + J3),
    ("gl-clcbt-custom", b"acme-glcbt-eyJ" + J1 + b".eyJ" + J2 + b"." + J3),
    ("gl-glsat", b"glsat-eyJ" + J1 + b".eyJ" + J2 + b"." + J3),
    ("gl-gliamat", b"gliamat-eyJ" + J1 + b".eyJ" + J2 + b"." + J3),
    ("gl-gliamat-prefixed", b"acme-gliamat-eyJ" + J1 + b".eyJ" + J2 + b"." + J3),
    ("gl-letter-before", b"xglcbt-eyJ" + J1 + b".eyJ" + J2 + b"." + J3),
    ("gl-not-eyj-head", b"glcbt-abcdefghij.eyJ" + J2 + b"." + J3),
    ("gl-first-seg-9", b"glcbt-eyJabc.eyJ" + J2 + b"." + J3),
    ("gl-second-seg-9", b"glcbt-eyJ" + J1 + b".eyJabcdefghi." + J3),
    ("gl-third-19", b"glsat-eyJ" + J1 + b".eyJ" + J2 + b"." + b"z" * 19 + b" "),
    ("gl-third-20", b"glsat-eyJ" + J1 + b".eyJ" + J2 + b"." + b"z" * 20),
    ("gl-esc-u0020", b'"v":"\\u0020glcbt-eyJ' + J1 + b".eyJ" + J2 + b"." + J3 + b'"'),
    ("gl-esc-amp32", b"&#32;glcbt-eyJ" + J1 + b".eyJ" + J2 + b"." + J3),
    ("gl-doc-placeholder", b"glcbt-eyJ<header>.<payload>.<signature>"),
]
for name, data in rows:
    print("PROBE %-22s %s" % (name, hit(data)))
