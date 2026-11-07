#!/usr/bin/env python3
"""Characterize the landed instrument's right-hand hex boundary (b06 finding).

Question: which total hex-run lengths after `_gitlab_session=` hit, and how
many leading hex chars may the right window swallow before a 64-hex value?
Usage: char_probe.py <fixture-dir>  -> writes charcases/ and prints paths.
"""
import hashlib
import os
import sys

D = os.path.abspath(sys.argv[1])
os.makedirs(D, exist_ok=True)
NONCE = open(sys.argv[2]).read().strip()

def h(tag):
    return hashlib.sha256((NONCE + "|char|" + tag).encode()).hexdigest()

cases = []
# raw run lengths after the separator
for n in (63, 64, 65, 66, 72, 73, 128):
    cases.append(("run-%d-hex" % n, (h("run%d" % n) * 3)[:n].encode()))
# k leading hex chars swallowed by the window, then a 64-hex value
for k in (1, 2, 8, 9, 10):
    cases.append(("prefix-%d-then-64" % k, h("p%d" % k).encode()[:k] + h("v%d" % k).encode()))

for slug, data in cases:
    name = hashlib.sha256((NONCE + "|char|" + slug).encode()).hexdigest()[:20] + "-" + slug + ".txt"
    with open(os.path.join(D, name), "wb") as fh:
        fh.write(b"_gitlab_session=" + data + b"\n")
    print(os.path.join(D, name))
