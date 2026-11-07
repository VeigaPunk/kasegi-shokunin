#!/usr/bin/env python3
"""Generate single-point mutants of the frozen C1 counter into $S/mutants/."""
import hashlib
import os
import sys

S = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(S, "knowledge-meter.orig.py")
OUT = os.path.join(S, "mutants")

# (name, limb, old, new)
MUTS = [
    # M1 meter
    ("m01_M1_true", "M1", '(an, am) == (tn, tm)', 'True'),
    ("m02_M1_numerator_only", "M1", '(an, am) == (tn, tm)', 'an == tn'),
    ("m03_M1_tuple_ge", "M1", '(an, am) == (tn, tm)', '(an, am) >= (tn, tm)'),
    ("m04_M1_base_rate", "M1", '(an, am) == (tn, tm)', '(an, am) == (bn, bm)'),
    ("m05_M1_target_hardcoded", "M1",
     'tn, tm = (int(x) for x in a.target.split("/"))', 'tn, tm = 596, 1716'),
    # M2 tokenset
    ("m06_M2_true", "M2", 'removed == keys and added <= vals', 'True'),
    ("m07_M2_no_added", "M2", 'removed == keys and added <= vals', 'removed == keys'),
    ("m08_M2_no_removed", "M2", 'removed == keys and added <= vals', 'added <= vals'),
    # M3 linediff
    ("m09_M3_true", "M3", 'm3 = same_files and bad == 0 and hit == keys', 'm3 = True'),
    ("m10_M3_no_line_equality", "M3", 'm3 = same_files and bad == 0 and hit == keys',
     'm3 = same_files and hit == keys'),
    ("m11_M3_no_hit_keys", "M3", 'm3 = same_files and bad == 0 and hit == keys',
     'm3 = same_files and bad == 0'),
    ("m12_M3_no_same_files", "M3", 'm3 = same_files and bad == 0 and hit == keys',
     'm3 = bad == 0 and hit == keys'),
    ("m13_M3_no_forward_subst", "M3",
     'fwd = fwd.replace("`%s`" % k, "`%s`" % v)', 'fwd = fwd'),
    # M4 binding
    ("m14_M4_true", "M4",
     'ok = (path is not None and path + anchor == v and path.startswith("corpus/source-snapshots/")\n'
     '              and path.endswith("/" + name) and bybase.get(name) == [path]\n'
     '              and R.classify(v, lane, mirror)[0] == "INTERNAL" and bcls.get(k) == "GONE")',
     'ok = True'),
    ("m15_M4_no_uniqueness", "M4",
     ' and path.endswith("/" + name) and bybase.get(name) == [path]',
     ' and path.endswith("/" + name)'),
    ("m16_M4_no_prefix", "M4",
     'and path + anchor == v and path.startswith("corpus/source-snapshots/")',
     'and path + anchor == v'),
    ("m17_M4_no_endswith", "M4",
     ' and path.endswith("/" + name) and bybase.get(name) == [path]',
     ' and bybase.get(name) == [path]'),
    ("m18_M4_no_key_gone", "M4",
     'and R.classify(v, lane, mirror)[0] == "INTERNAL" and bcls.get(k) == "GONE")',
     'and R.classify(v, lane, mirror)[0] == "INTERNAL")'),
    ("m19_M4_no_internal", "M4",
     'and R.classify(v, lane, mirror)[0] == "INTERNAL" and bcls.get(k) == "GONE")',
     'and bcls.get(k) == "GONE")'),
    ("m20_M4_no_anchor_agreement", "M4",
     'ok = (path is not None and path + anchor == v and path.startswith("corpus/source-snapshots/")',
     'ok = (path.startswith("corpus/source-snapshots/")'),
    ("m28_M4_nonkey_skip", "M4",
     '        if not km:\n            m4bad.append(k)\n            continue',
     '        if not km:\n            continue'),
    ("m29_M4_no_tracked_nonempty", "M4", 'not m4bad and bool(tracked)', 'not m4bad'),
    ("m30_M3_no_linecount", "M3", '            if len(bl) != len(al):', '            if False:'),
    # M5 inrange
    ("m21_M5_true", "M5", 'not m5bad and not m4bad', 'True'),
    ("m22_M5_no_hi_vs_nlines", "M5", 'if not (1 <= lo_i <= hi_i <= nlines):',
     'if not (1 <= lo_i <= nlines):'),
    ("m23_M5_no_m4bad", "M5", 'not m5bad and not m4bad', 'not m5bad'),
    ("m24_M5_upper_strict", "M5", 'if not (1 <= lo_i <= hi_i <= nlines):',
     'if not (1 <= lo_i <= hi_i < nlines):'),
    # M6 mapsha
    ("m25_M6_true", "M6", 'got == a.map_sha256.lower()', 'True'),
    ("m26_M6_prefix8", "M6", 'got == a.map_sha256.lower()',
     'got[:8] == a.map_sha256.lower()[:8]'),
    # rate definition (feeds M1)
    ("m27_rate_internal_only", "rate",
     'return sum(1 for c in cls.values() if c != "GONE"), len(cls)',
     'return sum(1 for c in cls.values() if c == "INTERNAL"), len(cls)'),
]


def main():
    src = open(ORIG, encoding="utf-8").read()
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for name, limb, old, new in MUTS:
        n = src.count(old)
        if n != 1:
            print("FATAL %s: old occurs %d times: %r" % (name, n, old[:70]))
            return 1
        text = src.replace(old, new)
        p = os.path.join(OUT, name + ".py")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
        rows.append((name, limb, hashlib.sha256(text.encode()).hexdigest(), text.count("\n") - src.count("\n")))
    print("mutants=%d orig_sha256=%s orig_lines=%d" % (
        len(rows), hashlib.sha256(src.encode()).hexdigest(), src.count("\n")))
    for r in rows:
        print("%s limb=%s sha256=%s dlines=%+d" % r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
