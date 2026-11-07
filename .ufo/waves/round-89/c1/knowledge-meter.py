#!/usr/bin/env python3
"""kasegi round-89 C1 counter (successor of the round-88 counter): the resolve.py
meter over the corpus/knowledge scope, tranche 4 (non-author-labelled sibling-entry
citations: re-anchors of the round-88 WRONG keys and prefix repoints of the round-88
proxy false negatives).

Usage:
  python3 knowledge-meter.py --lane LANE --base-rev REV --after-rev REV --map MAP \
      --labels LABELS.tsv --target NUM/DEN [--map-sha256 HEX] [--labels-sha256 HEX] [--work DIR]
  python3 knowledge-meter.py --lane LANE --measure-rev REV [--work DIR]

The scope is every corpus/knowledge/*.md file. The counter imports the lane's
corpus/instruments/resolve.py (never re-implements it), copies the scope files
of one revision into a scratch tree, runs resolve.collect() there (so SKILL.md
and the rest of corpus/ never enter the scope) and classifies each distinct
citation with resolve.classify() against LANE; rate = non-GONE / all distinct.
"Base" is the scope at --base-rev and "after" the scope at --after-rev, both read
with `git show` (round 89: commit-bound, r88 CriticClaims D1; the working tree is
never read). LANE must be a checkout that has .git (lesson M85-3).

Limbs (all must hold; one LIMB line each, then the verdict line):
  M1 meter     after rate equals the frozen --target NUM/DEN exactly.
  M2 tokenset  tokens(base) - tokens(after) == map keys; tokens(after) -
               tokens(base) is a subset of the map values.
  M3 linediff  same file set and, per file, same line count; every after line
               equals its base line with each backticked map key replaced by
               its value; every map key occurs on at least one base line.
  M4 binding   every key is a bare `<name>.md` with an optional :N or :N-M
               anchor and is GONE in the base scope; every value is
               `corpus/knowledge/<name>.md` with an optional :N or :N-M anchor
               (round 89: the value's anchor may differ from the key's, a
               re-anchor), that path is the only tracked file outside .ufo/ with
               basename <name>.md, and the value classifies INTERNAL.
  M5 inrange   every anchored value's line range lies inside the entry at
               --after-rev (1 <= N <= M <= line count).
  M6 mapsha    sha256 of the map file equals --map-sha256 (when given).
  M7 labelsha  sha256 of the labels file equals --labels-sha256 (when given).
  M9 labels    (round 89, replaces the round-88 lexical proxy M8, lesson M88-1)
               the map equals the labels file's key->value pairs exactly; each
               labels row names a line of REVIEW_PATH at REVIEW_REV (the round-88
               non-author seat ReviewC1Semantics) that holds the table cell
               `| <key> |`, the class marker (`**WRONG` for a re-anchor, `proxy
               false negative` for a prefix repoint, whose value anchor must then
               equal the key anchor) and the value's anchor written `L<N>` or
               `L<N>-<M>` as a whole token. A pair no non-author named fails.

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

KEY = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*\.md)(?::(\d+)(?:-(\d+))?)?$")
VAL = re.compile(r"^corpus/knowledge/([A-Za-z0-9][A-Za-z0-9._-]*\.md)(?::(\d+)(?:-(\d+))?)?$")
REVIEW_REV = "d0d9f49241420456f2373f62e417f8fa56a0f7d5"
REVIEW_PATH = ".ufo/waves/round-88/w1/ReviewC1Semantics.md"
CLASS_MARK = {"WRONG": "**WRONG", "FN": "proxy false negative"}


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
    ap.add_argument("--after-rev")
    ap.add_argument("--labels")
    ap.add_argument("--labels-sha256")
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
    if not (a.base_rev and a.after_rev and a.map and a.labels and a.target):
        print("KNOWLEDGE-METER-RESULT error reason=usage rc=2")
        return 2
    try:
        mb = open(a.map, "rb").read()
        rmap = json.loads(mb)
        tn, tm = (int(x) for x in a.target.split("/"))
        bfiles = scope_files_rev(lane, a.base_rev)
        afiles = scope_files_rev(lane, a.after_rev)
        lb = open(a.labels, "rb").read()
        labels = []
        for ln in lb.decode("utf-8").split("\n"):
            if ln.strip() and not ln.startswith("#"):
                k, v, n, c = ln.split("\t")
                labels.append((k, v, int(n), c))
        review = git(lane, "show", "%s:%s" % (REVIEW_REV, REVIEW_PATH)).split("\n")
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
        if not p.startswith(".ufo/"):
            bybase.setdefault(os.path.basename(p), []).append(p)
    mirror = os.path.expanduser(R.MIRROR_ROOT)
    m4bad, m5bad = [], []
    for k, v in sorted(rmap.items()):
        km, vm = KEY.match(k), VAL.match(v)
        if not km or not vm:
            m4bad.append(k)
            continue
        name, path = km.group(1), "corpus/knowledge/" + km.group(1)
        ok = (vm.group(1) == name and bybase.get(name) == [path]
              and R.classify(v, lane, mirror)[0] == "INTERNAL" and bcls.get(k) == "GONE")
        if not ok:
            m4bad.append(k)
            continue
        if vm.group(2) is not None:
            text = afiles.get(path)
            lo_i = int(vm.group(2))
            hi_i = int(vm.group(3)) if vm.group(3) else lo_i
            if text is None or not (1 <= lo_i <= hi_i <= len(text.splitlines())):
                m5bad.append(k)
    limbs.append(("M4", not m4bad and bool(tracked), "bad=%s" % (",".join(m4bad) or "none")))
    m9bad = []
    if dict((k, v) for k, v, _, _ in labels) != rmap or len(labels) != len(rmap):
        m9bad.append("map!=labels")
    for k, v, n, c in labels:
        km, vm = KEY.match(k), VAL.match(v)
        line = review[n - 1] if 1 <= n <= len(review) else ""
        if not km or not vm or c not in CLASS_MARK:
            m9bad.append(k)
            continue
        anchor = "" if vm.group(2) is None else (vm.group(2) if vm.group(3) is None else "%s-%s" % (vm.group(2), vm.group(3)))
        tok = re.compile(r"(?<![\w-])L%s(?![\w-])" % re.escape(anchor)) if anchor else None
        same = (km.group(2), km.group(3)) == (vm.group(2), vm.group(3))
        if ("| %s |" % k) not in line or CLASS_MARK[c] not in line or tok is None or not tok.search(line) \
                or (c == "FN" and not same) or (c == "WRONG" and same):
            m9bad.append(k)
    limbs.append(("M9", not m9bad, "labels=%d unbound=%s" % (len(labels), ",".join(m9bad) or "none")))
    limbs.append(("M5", not m5bad and not m4bad, "out_of_range=%s" % (",".join(m5bad) or "none")))
    if a.labels_sha256:
        got = hashlib.sha256(lb).hexdigest()
        limbs.append(("M7", got == a.labels_sha256.lower(), "sha256=%s" % got))
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
