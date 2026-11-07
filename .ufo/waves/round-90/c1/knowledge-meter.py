#!/usr/bin/env python3
"""kasegi round-90 C1 counter (successor of the round-89 counter): the resolve.py
meter over the corpus/knowledge scope, tranche 5 (per-site repoints of the
round-89 non-author ReviewC1Labels tranche-5 WRONG labels that name a supported
range).

Usage:
  python3 knowledge-meter.py --lane LANE --base-rev REV --after-rev REV --map MAP.tsv \
      --labels-rev REV --base-target NUM/DEN --target NUM/DEN [--map-sha256 HEX] [--work DIR]
  python3 knowledge-meter.py --lane LANE --measure-rev REV [--work DIR]

Round-90 change (round-89 closure, routed defect 1): every reading is pinned to
the measured revision. The scope files AND the tree the citations are classified
against are both `git archive REV` extracts in a scratch dir, and resolve.py is
imported from that same extract. The --lane working tree (untracked files,
pycache, other checkouts' state) is never read; LANE only serves its object
store. Absolute-path citations (`/...`, `~/...`) still resolve against the host
and the mirror root; their count and verdicts are printed on a HOST line so a
reader can see which part of a reading the host owns.

Map (TSV, # comments): `citing-file:line<TAB>key<TAB>value`, one row per site.
A site is one occurrence of the backticked key on that line of the citing file.

Limbs (all must hold; one LIMB line each, then the verdict line):
  M0 base      base rate equals the frozen --base-target exactly (round-89
               CriticClaims C1-F1: the base reading is asserted, not printed).
  M1 meter     after rate equals the frozen --target exactly.
  M3 linediff  same file set and line counts; every after line equals its base
               line, except each mapped site line, which equals its base line
               with the backticked key replaced by the backticked value once;
               each mapped site's base line holds the backticked key exactly once.
  M4 binding   every key is a bare `<name>.md[:N[-M]]` and GONE in the base
               scope; every value is `corpus/knowledge/<name>.md[:N[-M]]`, the
               only tracked file outside .ufo/ with that basename, INTERNAL in
               the after scope.
  M5 inrange   every value's anchor lies inside the entry at --after-rev.
  M6 mapsha    sha256 of the map file equals --map-sha256 (when given).
  M9 labels    every map row equals a row of LABELS_PATH at --labels-rev (the
               round-89 non-author seat ReviewC1Labels): same key, same
               citing-file:line, verdict WRONG, supported range == value. A row
               no non-author labelled fails.

Exit 0 only when every limb holds; 1 when a limb fails; 2 on usage or read error.
"""
import argparse
import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import io

KEY = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*\.md)(?::(\d+)(?:-(\d+))?)?$")
VAL = re.compile(r"^corpus/knowledge/([A-Za-z0-9][A-Za-z0-9._-]*\.md)(?::(\d+)(?:-(\d+))?)?$")
LABELS_PATH = ".ufo/waves/round-89/w1/ReviewC1Labels-receipts/tranche5-labels.tsv"


def git(lane, *args, binary=False):
    r = subprocess.run(["git", "-C", lane] + list(args), capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode("utf-8")


def extract(lane, rev, work):
    d = tempfile.mkdtemp(prefix="kmeter90-tree-", dir=work)
    data = git(lane, "archive", "--format=tar", rev, binary=True)
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        tf.extractall(d, filter="tar")
    return d


def load_resolve(tree):
    path = os.path.join(tree, "corpus", "instruments", "resolve.py")
    spec = importlib.util.spec_from_file_location("resolve_pinned_%d" % abs(hash(tree)), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def scope_files(tree):
    kd = os.path.join(tree, "corpus", "knowledge")
    out = {}
    for n in sorted(os.listdir(kd)):
        p = os.path.join(kd, n)
        if n.endswith(".md") and os.path.isfile(p):
            with open(p, encoding="utf-8") as fh:
                out["corpus/knowledge/" + n] = fh.read()
    return out


def classify_scope(R, tree, files, work):
    d = tempfile.mkdtemp(prefix="kmeter90-scope-", dir=work)
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
    return {t: R.classify(t, tree, mirror)[0] for t in sorted(cites)}


def rate(cls):
    return sum(1 for c in cls.values() if c != "GONE"), len(cls)


def host_line(tag, cls):
    ab = [t for t in cls if t.startswith("/") or t.startswith("~")]
    return "HOST %s abs_tokens=%d abs_nongone=%d" % (tag, len(ab), sum(1 for t in ab if cls[t] != "GONE"))


def reading(lane, rev, work):
    tree = extract(lane, rev, work)
    try:
        R = load_resolve(tree)
        files = scope_files(tree)
        cls = classify_scope(R, tree, files, work)
        tracked = [p for p in git(lane, "ls-tree", "-r", "--name-only", rev).split("\n") if p]
        info = {"files": files, "cls": cls, "tracked": tracked, "mirror_absent": R.MIRROR_ABSENT}
        # classify map values against this pinned tree before it is removed
        info["classify"] = lambda t, R=R, tree=tree: R.classify(t, tree, os.path.expanduser(R.MIRROR_ROOT))[0]
        info["tree"] = tree
        return info
    except Exception:
        shutil.rmtree(tree, ignore_errors=True)
        raise


def parse_target(s):
    n, m = s.split("/")
    return int(n), int(m)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--measure-rev")
    ap.add_argument("--base-rev")
    ap.add_argument("--after-rev")
    ap.add_argument("--map")
    ap.add_argument("--map-sha256")
    ap.add_argument("--labels-rev")
    ap.add_argument("--base-target")
    ap.add_argument("--target")
    ap.add_argument("--work", default=os.environ.get("TMPDIR") or None)
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    if a.work:
        os.makedirs(a.work, exist_ok=True)
    trees = []
    try:
        if a.measure_rev:
            try:
                r = reading(lane, a.measure_rev, a.work)
                trees.append(r["tree"])
            except Exception as e:
                print("KNOWLEDGE-METER-RESULT error reason=read:%s rc=2" % type(e).__name__)
                return 2
            n, m = rate(r["cls"])
            print("KNOWLEDGE-METER rev=%s rate=%d/%d pct=%.2f mirror_absent=%s pinned=archive" % (
                a.measure_rev, n, m, 100.0 * n / m if m else 0, r["mirror_absent"]))
            print(host_line("rev", r["cls"]))
            return 0
        if not (a.base_rev and a.after_rev and a.map and a.labels_rev and a.target and a.base_target):
            print("KNOWLEDGE-METER-RESULT error reason=usage rc=2")
            return 2
        try:
            mb = open(a.map, "rb").read()
            rows = []
            for ln in mb.decode("utf-8").split("\n"):
                if ln.strip() and not ln.startswith("#"):
                    site, k, v = ln.split("\t")
                    f, n = site.rsplit(":", 1)
                    rows.append((f, int(n), k, v))
            tn, tm = parse_target(a.target)
            bn0, bm0 = parse_target(a.base_target)
            labels_txt = git(lane, "show", "%s:%s" % (a.labels_rev, LABELS_PATH))
            B = reading(lane, a.base_rev, a.work)
            trees.append(B["tree"])
            A = reading(lane, a.after_rev, a.work)
            trees.append(A["tree"])
        except Exception as e:
            print("KNOWLEDGE-METER-RESULT error reason=read:%s rc=2" % type(e).__name__)
            return 2
        bcls, acls, bfiles, afiles = B["cls"], A["cls"], B["files"], A["files"]
        bn, bm = rate(bcls)
        an, am = rate(acls)
        print("KNOWLEDGE-METER base=%d/%d after=%d/%d base_target=%d/%d target=%d/%d sites=%d mirror_absent=%s pinned=archive" % (
            bn, bm, an, am, bn0, bm0, tn, tm, len(rows), A["mirror_absent"]))
        print(host_line("base", bcls))
        print(host_line("after", acls))
        limbs = [("M0", (bn, bm) == (bn0, bm0), "base=%d/%d" % (bn, bm)),
                 ("M1", (an, am) == (tn, tm), "after=%d/%d" % (an, am))]
        # M3 per-site line diff
        sites = {}
        dup = 0
        for f, n, k, v in rows:
            if (f, n, k) in sites:
                dup += 1
            sites[(f, n, k)] = v
        same_files = set(bfiles) == set(afiles)
        bad, missing = 0, 0
        if same_files:
            for rel in sorted(bfiles):
                bl, al = bfiles[rel].split("\n"), afiles[rel].split("\n")
                if len(bl) != len(al):
                    bad += 1
                    continue
                for i, (b, x) in enumerate(zip(bl, al), 1):
                    fwd = b
                    for (f, n, k), v in sites.items():
                        if f == rel and n == i:
                            if fwd.count("`%s`" % k) != 1:
                                missing += 1
                                continue
                            fwd = fwd.replace("`%s`" % k, "`%s`" % v)
                    if fwd != x:
                        bad += 1
        limbs.append(("M3", same_files and bad == 0 and missing == 0 and dup == 0 and bool(rows),
                      "same_files=%s bad_lines=%d key_not_once=%d dup_rows=%d" % (same_files, bad, missing, dup)))
        # M4 binding, M5 in range
        bybase = {}
        for p in A["tracked"]:
            if not p.startswith(".ufo/"):
                bybase.setdefault(os.path.basename(p), []).append(p)
        m4bad, m5bad = [], []
        for f, n, k, v in rows:
            km, vm = KEY.match(k), VAL.match(v)
            tag = "%s:%d" % (f.rsplit("/", 1)[-1], n)
            if not km or not vm:
                m4bad.append(tag)
                continue
            name, path = km.group(1), "corpus/knowledge/" + km.group(1)
            if not (vm.group(1) == name and bybase.get(name) == [path]
                    and A["classify"](v) == "INTERNAL" and bcls.get(k) == "GONE"):
                m4bad.append(tag)
                continue
            if vm.group(2) is not None:
                text = afiles.get(path)
                lo = int(vm.group(2))
                hi = int(vm.group(3)) if vm.group(3) else lo
                if text is None or not (1 <= lo <= hi <= len(text.splitlines())):
                    m5bad.append(tag)
        limbs.append(("M4", not m4bad and bool(rows), "bad=%s" % (",".join(m4bad) or "none")))
        limbs.append(("M5", not m5bad and not m4bad, "out_of_range=%s" % (",".join(m5bad) or "none")))
        # M9 label binding
        lab = set()
        for ln in labels_txt.split("\n"):
            if ln.strip() and not ln.startswith("#"):
                c = ln.split("\t")
                if len(c) >= 4 and c[2] == "WRONG":
                    lab.add((c[1], c[0], c[3]))
        m9bad = ["%s:%d" % (f.rsplit("/", 1)[-1], n) for f, n, k, v in rows if ("%s:%d" % (f, n), k, v) not in lab]
        limbs.append(("M9", not m9bad and bool(rows), "rows=%d unbound=%s" % (len(rows), ",".join(m9bad) or "none")))
        if a.map_sha256:
            got = hashlib.sha256(mb).hexdigest()
            limbs.append(("M6", got == a.map_sha256.lower(), "sha256=%s" % got))
        for name, ok, det in limbs:
            print("LIMB %s %s %s" % (name, "pass" if ok else "FAIL", det))
        allok = all(ok for _, ok, _ in limbs)
        print("KNOWLEDGE-METER-RESULT %s rc=%d" % ("pass" if allok else "fail", 0 if allok else 1))
        return 0 if allok else 1
    finally:
        for t in trees:
            shutil.rmtree(t, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
