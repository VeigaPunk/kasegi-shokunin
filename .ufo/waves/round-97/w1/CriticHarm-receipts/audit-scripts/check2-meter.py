#!/usr/bin/env python3
"""CriticHarm r97 check 2: independent resolve.py meter over corpus/knowledge/*.md.

Replicates the meter's scope (corpus/knowledge/*.md only, distinct tokens,
classified against the extracted tree) using each revision's own resolve.py.
"""
import importlib.util
import os
import shutil
import sys
import tempfile

BASE = sys.argv[1]
TIP = sys.argv[2]
WORK = sys.argv[3]


def load(tree):
    p = os.path.join(tree, "corpus", "instruments", "resolve.py")
    spec = importlib.util.spec_from_file_location("resolve_%d" % abs(hash(tree)), p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def reading(tree):
    R = load(tree)
    tmp = tempfile.mkdtemp(prefix="critic-scope-", dir=WORK)
    try:
        kd = os.path.join(tree, "corpus", "knowledge")
        for n in sorted(os.listdir(kd)):
            if n.endswith(".md"):
                os.makedirs(os.path.join(tmp, "corpus", "knowledge"), exist_ok=True)
                shutil.copyfile(os.path.join(kd, n), os.path.join(tmp, "corpus", "knowledge", n))
        _, cites = R.collect(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    mirror = os.path.expanduser(R.MIRROR_ROOT)
    cls = {t: R.classify(t, tree, mirror)[0] for t in sorted(cites)}
    n = sum(1 for c in cls.values() if c != "GONE")
    return cls, n, len(cls)


bcls, bn, bm = reading(BASE)
tcls, tn, tm = reading(TIP)
print("BASE %d/%d  TIP %d/%d" % (bn, bm, tn, tm))
lost = sorted(t for t in bcls if bcls[t] != "GONE" and t in tcls and tcls[t] == "GONE")
gained = sorted(t for t in tcls if tcls[t] != "GONE" and t in bcls and bcls[t] == "GONE")
only_base = sorted(set(bcls) - set(tcls))
only_tip = sorted(set(tcls) - set(bcls))
print("LOST_RESOLUTION=%d" % len(lost))
for t in lost:
    print("  LOST %s (%s -> GONE)" % (t, bcls[t]))
print("GAINED_RESOLUTION=%d" % len(gained))
for t in gained:
    print("  GAINED %s" % t)
print("TOKENS_ONLY_BASE=%d" % len(only_base))
for t in only_base:
    print("  -%s [%s]" % (t, bcls[t]))
print("TOKENS_ONLY_TIP=%d" % len(only_tip))
for t in only_tip:
    print("  +%s [%s]" % (t, tcls[t]))
