#!/usr/bin/env python3
"""Build the round-94 proposal counter variants used to demonstrate the EXCLUDED
coverage gap (M11/M12/M13) and the M3 line-count gap once the R1 shadow is fixed.
These are NOT frozen artifacts: they exist only to prove what a mutant would do
if the branch it disables were reachable.
"""
import os
import sys

S = "/fast/scratch/hyaku/kasegi-r93/MutC1Counter/art"
SRC = os.path.join(S, "knowledge-meter.py")


def variant(name, edits, base=None):
    src = open(base or SRC, encoding="utf-8").read()
    for old, new in edits:
        if src.count(old) != 1:
            raise SystemExit("%s: pattern count %d for %r" % (name, src.count(old), old[:50]))
        src = src.replace(old, new, 1)
    compile(src, name, "exec")
    p = os.path.join(S, "variants", name + ".py")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(src)
    print("built", p)


EXCL_B = 'EXCLUDED = {}'
EXCL_B_SET = 'EXCLUDED = {("corpus/knowledge/triage-thresholds.md:58", "SKILL.md:117"): "probe: excluded pair"}'
EXCL_ABSENT = 'EXCLUDED = {("corpus/knowledge/triage-thresholds.md:144", "SKILL.md:117"): "probe: pair absent from labels"}'
SHADOW = '            b, a = file_at(B["tree"], rel), file_at(A["tree"], rel)\n            if b is not None and a is not None:\n                bfiles[rel], afiles[rel] = b, a\n'
SHADOW_FIX = '            b, a_txt = file_at(B["tree"], rel), file_at(A["tree"], rel)\n            if b is not None and a_txt is not None:\n                bfiles[rel], afiles[rel] = b, a_txt\n'

# EXCLUDED non-empty (data only): the correct counter must reject a mapped excluded pair.
variant("excl-base", [(EXCL_B, EXCL_B_SET)])
variant("excl-base-absent", [(EXCL_B, EXCL_ABSENT)])
# the three mutants on top of the non-empty EXCLUDED counter
variant("excl-base-m11", [(EXCL_B, EXCL_B_SET),
                          ('        unlabelled = sorted(mapped - want)\n', '        unlabelled = []\n')])
variant("excl-base-m12", [(EXCL_B, EXCL_B_SET),
                          ('        want = {p for p, k in kinds.items() if k not in ("excluded", "no-edit")}\n',
                           '        want = {p for p, k in kinds.items() if k not in ("no-edit",)}\n')])
variant("excl-absent-m13", [(EXCL_B, EXCL_ABSENT),
                            ('not unlabelled and not unknown and set(EXCLUDED) <= set(kinds),\n',
                             'not unlabelled and not unknown,\n')])
# R1 fix: the labelled-file union clobbers the argparse namespace `a`.
variant("r1fix", [(SHADOW, SHADOW_FIX)])
# R1 fix + the M3 line-count mutant, on an otherwise correct counter.
variant("r1fix-m05", [(SHADOW, SHADOW_FIX),
                      ('                if len(bl) != len(al):\n                    bad += 1\n                    continue\n',
                       '                if len(bl) != len(al):\n                    continue\n')])
