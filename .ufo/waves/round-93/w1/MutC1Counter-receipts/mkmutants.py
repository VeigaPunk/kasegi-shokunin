#!/usr/bin/env python3
"""Generate one-change mutants of the frozen round-93 C1 knowledge meter.
Every mutation must match exactly once in the frozen bytes; anything else aborts.
"""
import hashlib
import os
import sys

SRC = "art/knowledge-meter.py"
OUT = "art/mutants"

MUTANTS = [
    # id, target area, old, new
    ("M01-cell-lastcell-last", "cell-repair old derivation",
     '    return cells[-2].strip() if line.rstrip().endswith("|") and len(cells) >= 3 else None\n',
     '    return cells[-1].strip() if line.rstrip().endswith("|") and len(cells) >= 3 else None\n'),
    ("M02-cell-new-eq-old", "cell-repair new derivation",
     '            return "cell-repair", last_cell(line), m.group(1)\n',
     '            return "cell-repair", last_cell(line), last_cell(line)\n'),
    ("M03-cell-iscell-false", "cell-repair multi-value exemption",
     '            is_cell = bool(exp and exp[0] == "cell-repair")\n',
     '            is_cell = False\n'),
    ("M04-m3-union-knowledge-only", "M3 labelled-file union",
     '        labelled_files = {site.rsplit(":", 1)[0] for site, _ in labels} | {r[0] for r in rows}\n',
     '        labelled_files = {site.rsplit(":", 1)[0] for site, _ in labels} | {r[0] for r in rows}\n'
     '        labelled_files = {rel for rel in labelled_files if rel.startswith("corpus/knowledge/")}\n'),
    ("M05-m3-count-skip", "M3 line-count equality",
     '                if len(bl) != len(al):\n                    bad += 1\n                    continue\n',
     '                if len(bl) != len(al):\n                    continue\n'),
    ("M06-m4-bybase-nonunique", "M4 basename uniqueness",
     'bybase.get(name) == ["corpus/knowledge/" + name]',
     'bool(bybase.get(name))'),
    ("M07-m4-laneroot-no-classify", "M4 lane-root value binding",
     '                    if "SKILL.md" not in A["tracked"] or A["classify"](v) != "INTERNAL":\n',
     '                    if "SKILL.md" not in A["tracked"]:\n'),
    ("M08-m5-laneroot-no-hi-bound", "M5 lane-root range check",
     '                    if text is None or not (1 <= lo <= hi <= len(text.splitlines())):\n',
     '                    if text is None or not (1 <= lo <= hi):\n'),
    ("M09-m5-laneroot-split-not-splitlines", "M5 lane-root range check",
     '                    if text is None or not (1 <= lo <= hi <= len(text.splitlines())):\n',
     '                    if text is None or not (1 <= lo <= hi <= len(text.split("\\n"))):\n'),
    ("M10-m10-drop-unknown", "M10 pair completeness",
     '        limbs.append(("M10", bool(want) and not unapplied and not unlabelled and not unknown and set(EXCLUDED) <= set(kinds),\n',
     '        limbs.append(("M10", bool(want) and not unapplied and not unlabelled and set(EXCLUDED) <= set(kinds),\n'),
    ("M11-m10-unlabelled-emptied", "M10 pair completeness",
     '        unlabelled = sorted(mapped - want)\n',
     '        unlabelled = []\n'),
    ("M12-m10-excluded-not-subtracted", "EXCLUDED empty set / M10",
     '        want = {p for p, k in kinds.items() if k not in ("excluded", "no-edit")}\n',
     '        want = {p for p, k in kinds.items() if k not in ("no-edit",)}\n'),
    ("M13-m10-excluded-membership", "EXCLUDED empty set / M10",
     'not unlabelled and not unknown and set(EXCLUDED) <= set(kinds),\n',
     'not unlabelled and not unknown,\n'),
    ("M14-m6-prefix16", "M6 map sha pin",
     'got == a.map_sha256.lower()',
     'got[:16] == a.map_sha256.lower()[:16]'),
    ("M15-m6-limb-omitted", "M6 map sha pin",
     '        if a.map_sha256:\n',
     '        if False and a.map_sha256:\n'),
    ("M16-labels-from-after-rev", "labels rev pin",
     '"%s:%s" % (a.labels_rev, LABELS_PATH)',
     '"%s:%s" % (a.after_rev, LABELS_PATH)'),
    ("M17-contentrepair-dash-disabled", "content-repair kinds (round-91/92)",
     '        if FIXDASH.match(fix):\n',
     '        if False and FIXDASH.match(fix):\n'),
    ("M18-m3-dup-not-counted", "M3 duplicate rows",
     '            if (f, n) in sites:\n                dup += 1\n',
     '            if False:\n                dup += 1\n'),
    ("M19-m10-mapped-drops-key", "M10 pair identity",
     '        mapped = {("%s:%d" % (f, n), k) for f, n, k, _, _ in rows}\n',
     '        mapped = {("%s:%d" % (f, n)) for f, n, k, _, _ in rows}\n'),
]


def main():
    src = open(SRC, encoding="utf-8").read()
    os.makedirs(OUT, exist_ok=True)
    print("frozen src sha256", hashlib.sha256(src.encode()).hexdigest(), "lines", len(src.split("\n")))
    for mid, area, old, new in MUTANTS:
        n = src.count(old)
        if n != 1:
            print("ABORT %s: pattern count=%d" % (mid, n))
            return 2
        body = src.replace(old, new, 1)
        if body == src:
            print("ABORT %s: no change" % mid)
            return 2
        # syntax check
        try:
            compile(body, mid, "exec")
        except SyntaxError as e:
            print("ABORT %s: syntax: %s" % (mid, e))
            return 2
        path = os.path.join(OUT, mid + ".py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        print("%s\t%s\tsha256=%s\tbytes=%d->%d" % (
            mid, area, hashlib.sha256(body.encode()).hexdigest(), len(src), len(body)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
