#!/usr/bin/env python3
"""kasegi round-86 C1 counter: the resolve.py meter over the corpus/knowledge scope.

Usage:
  python3 knowledge-meter.py --lane LANE --base-rev REV --map MAP --target NUM/DEN \
      [--map-sha256 HEX] [--work DIR]
  python3 knowledge-meter.py --lane LANE --measure-rev REV [--work DIR]

The scope is every corpus/knowledge/*.md file. The counter imports the lane's
corpus/instruments/resolve.py (never re-implements it), copies the scope files
of one revision into a scratch tree, runs resolve.collect() there (so SKILL.md
and the rest of corpus/ never enter the scope) and classifies each distinct
citation with resolve.classify() against LANE; rate = non-GONE / all distinct.
"Base" is the scope at --base-rev (read with `git show`); "after" is the scope
in LANE's working tree. LANE must be a checkout that has .git (lesson M85-3).

Limbs (all must hold; one LIMB line each, then the verdict line):
  M1 meter     after rate equals the frozen --target NUM/DEN exactly.
  M2 tokenset  tokens(base) - tokens(after) == map keys; tokens(after) -
               tokens(base) is a subset of the map values.
  M3 linediff  same file set and, per file, same line count; every after line
               equals its base line with each backticked map key replaced by
               its value; every map key occurs on at least one base line.
  M4 binding   every key is a bare `S<digits>.txt` name with an optional
               :N or :N-M anchor and is GONE in the base scope; every value is
               `<tracked path>` + the key's anchor, the tracked path lies under
               corpus/source-snapshots/, ends with '/'+the bare name, is the only
               tracked lane file with that basename, and classifies INTERNAL.
  M5 inrange   every anchored value's line range lies inside the snapshot
               (1 <= N <= M <= line count of the tracked file).
  M6 mapsha    sha256 of the map file equals --map-sha256 (when given).

Exit 0 only when every limb holds; 1 when a limb fails; 2 on usage or read
error (a limb that cannot read its input fails closed).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

KEY = re.compile(r"^(S\d{3,}\.txt)(?::(\d+)(?:-(\d+))?)?$")


def git(lane, *args):
    return subprocess.run(["git", "-C", lane] + list(args), capture_output=True, text=True, check=True).stdout


def load_resolve(lane):
    sys.path.insert(0, os.path.join(lane, "corpus", "instruments"))
    import resolve  # noqa: E402
    return resolve


def scope_files_rev(lane, rev):
    names = [p for p in git(lane, "ls-tree", "--name-only", rev, "corpus/knowledge/").split("\n")
             if p.endswith(".md") and p.count("/") == 2]
    return {p: git(lane, "show", "%s:%s" % (rev, p)) for p in names}


def scope_files_tree(lane):
    d = os.path.join(lane, "corpus", "knowledge")
    out = {}
    for fn in sorted(os.listdir(d)):
        p = os.path.join(d, fn)
        if fn.endswith(".md") and os.path.isfile(p):
            with open(p, encoding="utf-8") as fh:
                out["corpus/knowledge/" + fn] = fh.read()
    return out


def classify_scope(R, lane, files, work):
    d = tempfile.mkdtemp(prefix="kmeter-", dir=work)
    try:
        for rel, text in files.items():
            p = os.path.join(d, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(text)
        _, cites = R.collect(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    mirror = os.path.expanduser(R.MIRROR_ROOT)
    return {t: R.classify(t, lane, mirror)[0] for t in sorted(cites)}


def rate(cls):
    return sum(1 for c in cls.values() if c != "GONE"), len(cls)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--measure-rev")
    ap.add_argument("--base-rev")
    ap.add_argument("--map")
    ap.add_argument("--target")
    ap.add_argument("--map-sha256")
    ap.add_argument("--work", default=os.environ.get("TMPDIR") or None)
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    if a.work:
        os.makedirs(a.work, exist_ok=True)
    try:
        R = load_resolve(lane)
    except Exception as e:
        print("KNOWLEDGE-METER-RESULT error reason=resolve-import:%s rc=2" % type(e).__name__)
        return 2
    if a.measure_rev:
        try:
            cls = classify_scope(R, lane, scope_files_rev(lane, a.measure_rev), a.work)
        except Exception as e:
            print("KNOWLEDGE-METER-RESULT error reason=read:%s rc=2" % type(e).__name__)
            return 2
        n, m = rate(cls)
        print("KNOWLEDGE-METER rev=%s rate=%d/%d pct=%.2f mirror_absent=%s" % (a.measure_rev, n, m, 100.0 * n / m if m else 0, R.MIRROR_ABSENT))
        return 0
    if not (a.base_rev and a.map and a.target):
        print("KNOWLEDGE-METER-RESULT error reason=usage rc=2")
        return 2
    try:
        mb = open(a.map, "rb").read()
        rmap = json.loads(mb)
        tn, tm = (int(x) for x in a.target.split("/"))
        bfiles = scope_files_rev(lane, a.base_rev)
        afiles = scope_files_tree(lane)
        bcls = classify_scope(R, lane, bfiles, a.work)
        acls = classify_scope(R, lane, afiles, a.work)
        tracked = [p for p in git(lane, "ls-files").split("\n") if p]
    except Exception as e:
        print("KNOWLEDGE-METER-RESULT error reason=read:%s rc=2" % type(e).__name__)
        return 2
    limbs = []
    bn, bm = rate(bcls)
    an, am = rate(acls)
    print("KNOWLEDGE-METER base=%d/%d after=%d/%d target=%d/%d keys=%d mirror_absent=%s" % (bn, bm, an, am, tn, tm, len(rmap), R.MIRROR_ABSENT))
    limbs.append(("M1", (an, am) == (tn, tm), "after=%d/%d" % (an, am)))
    keys, vals = set(rmap), set(rmap.values())
    removed = set(bcls) - set(acls)
    added = set(acls) - set(bcls)
    limbs.append(("M2", removed == keys and added <= vals, "removed=%d keys=%d stray_removed=%d stray_added=%d unrepaired=%d" % (
        len(removed), len(keys), len(removed - keys), len(added - vals), len(keys - removed))))
    hit, bad = set(), 0
    same_files = set(bfiles) == set(afiles)
    if same_files:
        for rel in sorted(bfiles):
            bl, al = bfiles[rel].split("\n"), afiles[rel].split("\n")
            if len(bl) != len(al):
                bad += 1
                continue
            for b, x in zip(bl, al):
                fwd = b
                for k, v in rmap.items():
                    if "`%s`" % k in fwd:
                        hit.add(k)
                        fwd = fwd.replace("`%s`" % k, "`%s`" % v)
                if fwd != x:
                    bad += 1
    m3 = same_files and bad == 0 and hit == keys
    limbs.append(("M3", m3, "same_files=%s bad_lines=%d keys_hit=%d" % (same_files, bad, len(hit))))
    bybase = {}
    for p in tracked:
        bybase.setdefault(os.path.basename(p), []).append(p)
    mirror = os.path.expanduser(R.MIRROR_ROOT)
    m4bad, m5bad = [], []
    for k, v in sorted(rmap.items()):
        km = KEY.match(k)
        if not km:
            m4bad.append(k)
            continue
        name, lo, hi = km.group(1), km.group(2), km.group(3)
        anchor = "" if lo is None else (":%s" % lo if hi is None else ":%s-%s" % (lo, hi))
        path = v[: len(v) - len(anchor)] if anchor and v.endswith(anchor) else (v if not anchor else None)
        ok = (path is not None and path + anchor == v and path.startswith("corpus/source-snapshots/")
              and path.endswith("/" + name) and bybase.get(name) == [path]
              and R.classify(v, lane, mirror)[0] == "INTERNAL" and bcls.get(k) == "GONE")
        if not ok:
            m4bad.append(k)
            continue
        if lo is not None:
            try:
                with open(os.path.join(lane, path), encoding="utf-8") as fh:
                    nlines = len(fh.read().splitlines())
                lo_i, hi_i = int(lo), int(hi) if hi else int(lo)
                if not (1 <= lo_i <= hi_i <= nlines):
                    m5bad.append(k)
            except Exception:
                m5bad.append(k)
    limbs.append(("M4", not m4bad, "bad=%s" % (",".join(m4bad) or "none")))
    limbs.append(("M5", not m5bad and not m4bad, "out_of_range=%s" % (",".join(m5bad) or "none")))
    if a.map_sha256:
        got = hashlib.sha256(mb).hexdigest()
        limbs.append(("M6", got == a.map_sha256.lower(), "sha256=%s" % got))
    for name, ok, det in limbs:
        print("LIMB %s %s %s" % (name, "pass" if ok else "FAIL", det))
    allok = all(ok for _, ok, _ in limbs)
    print("KNOWLEDGE-METER-RESULT %s rc=%d" % ("pass" if allok else "fail", 0 if allok else 1))
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
