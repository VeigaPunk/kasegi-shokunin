#!/usr/bin/env python3
"""kasegi round-85 C1 counter: the resolve.py SKILL.md meter, read directly.

Usage:
  python3 skill-meter.py --lane LANE --base BASE_SKILL --after AFTER_SKILL \
      --map REPAIR_MAP --target NUM/DEN [--map-sha256 HEX]
  python3 skill-meter.py --lane LANE --measure SKILL_FILE

The meter is `corpus/instruments/resolve.py`'s own SKILL.md scope: the distinct
path-like citations `resolve.collect()` extracts from SKILL.md, each classified
by `resolve.classify()` against the lane root; rate = non-GONE / all. The
counter imports the lane's resolve.py (it never re-implements the rule) and
collects from a scratch directory that holds only the file under test, so
corpus/ citations never enter the SKILL scope.

Limbs (all must hold; one `LIMB` line each, then the verdict line):
  M1 meter     after rate equals the frozen --target NUM/DEN exactly.
  M2 tokenset  tokens(base) - tokens(after) == map keys (every repaired bare
               token left, nothing else left); tokens(after) - tokens(base)
               is a subset of the map values (nothing added but repairs).
  M3 linediff  same line count; every after line equals its base line with
               each backticked map key replaced by its value (forward
               application of the frozen map); every map key occurs on at
               least one base line.
  M4 binding   every map value is a git-tracked lane file outside .ufo/,
               classified INTERNAL, ends with '/'+key; every key is GONE in
               the base scope.
  M5 mapsha    sha256 of the map file equals --map-sha256 (when given).

Exit 0 only when every limb holds; 1 when a limb fails; 2 on usage or read
error (a limb that cannot read its input fails closed).
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile


def load_resolve(lane):
    sys.path.insert(0, os.path.join(lane, "corpus", "instruments"))
    import resolve  # noqa: E402
    return resolve


def scope(R, lane, skill_path, scratch):
    d = tempfile.mkdtemp(prefix="skillmeter-", dir=scratch)
    try:
        shutil.copyfile(skill_path, os.path.join(d, "SKILL.md"))
        _, cites = R.collect(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    mirror = os.path.expanduser(R.MIRROR_ROOT)
    cls = {t: R.classify(t, lane, mirror)[0] for t in sorted(cites)}
    return cls


def rate(cls):
    return sum(1 for c in cls.values() if c != "GONE"), len(cls)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--measure")
    ap.add_argument("--base")
    ap.add_argument("--after")
    ap.add_argument("--map")
    ap.add_argument("--target")
    ap.add_argument("--map-sha256")
    ap.add_argument("--work", default=os.environ.get("TMPDIR") or None)
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    work = a.work
    if work:
        os.makedirs(work, exist_ok=True)
    try:
        R = load_resolve(lane)
    except Exception as e:  # fail closed
        print("SKILL-METER-RESULT error reason=resolve-import:%s rc=2" % type(e).__name__)
        return 2
    if a.measure:
        cls = scope(R, lane, a.measure, work)
        n, m = rate(cls)
        print("SKILL-METER rate=%d/%d pct=%.2f gone=%d mirror_absent=%s" % (n, m, 100.0 * n / m if m else 0, m - n, R.MIRROR_ABSENT))
        return 0
    if not (a.base and a.after and a.map and a.target):
        print("SKILL-METER-RESULT error reason=usage rc=2")
        return 2
    try:
        mb = open(a.map, "rb").read()
        rmap = json.loads(mb)
        base_lines = open(a.base, encoding="utf-8").read().split("\n")
        after_lines = open(a.after, encoding="utf-8").read().split("\n")
        tn, tm = (int(x) for x in a.target.split("/"))
        bcls = scope(R, lane, a.base, work)
        acls = scope(R, lane, a.after, work)
    except Exception as e:
        print("SKILL-METER-RESULT error reason=read:%s rc=2" % type(e).__name__)
        return 2
    limbs = []
    bn, bm = rate(bcls)
    an, am = rate(acls)
    print("SKILL-METER base=%d/%d after=%d/%d target=%d/%d mirror_absent=%s" % (bn, bm, an, am, tn, tm, R.MIRROR_ABSENT))
    limbs.append(("M1", (an, am) == (tn, tm), "after=%d/%d" % (an, am)))
    keys, vals = set(rmap), set(rmap.values())
    removed = set(bcls) - set(acls)
    added = set(acls) - set(bcls)
    m2 = bool(removed & keys) and added <= vals
    limbs.append(("M2", m2, "removed=%d keys=%d stray_removed=%d stray_added=%d unrepaired=%d" % (
        len(removed), len(keys), len(removed - keys), len(added - vals), len(keys - removed))))
    m3 = len(base_lines) == len(after_lines)
    hit = set()
    bad = 0
    if m3:
        for bl, al in zip(base_lines, after_lines):
            fwd = bl
            for k, v in rmap.items():
                if "`%s`" % k in fwd:
                    hit.add(k)
                    fwd = fwd.replace("`%s`" % k, "`%s`" % v)
            if fwd != al:
                bad += 1
        m3 = bad == 0 and hit == keys
    limbs.append(("M3", m3, "linecount_equal=%s bad_lines=%d keys_hit=%d" % (len(base_lines) == len(after_lines), bad, len(hit))))
    try:
        tracked = set(subprocess.run(["git", "-C", lane, "ls-files"], capture_output=True, text=True, check=True).stdout.split("\n"))
    except Exception:
        tracked = set()
    m4bad = []
    mirror = os.path.expanduser(R.MIRROR_ROOT)
    for k, v in sorted(rmap.items()):
        ok = (v in tracked and not v.startswith(".ufo/") and v.endswith("/" + k)
              and R.classify(v, lane, mirror)[0] == "INTERNAL" and bcls.get(k) == "GONE")
        if not ok:
            m4bad.append(k)
    limbs.append(("M4", not m4bad and bool(tracked), "bad=%s" % (",".join(m4bad) or "none")))
    if a.map_sha256:
        got = hashlib.sha256(mb).hexdigest()
        limbs.append(("M5", got == a.map_sha256.lower(), "sha256=%s" % got))
    for name, ok, det in limbs:
        print("LIMB %s %s %s" % (name, "pass" if ok else "FAIL", det))
    allok = all(ok for _, ok, _ in limbs)
    print("SKILL-METER-RESULT %s rc=%d" % ("pass" if allok else "fail", 0 if allok else 1))
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
