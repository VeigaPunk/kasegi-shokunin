#!/usr/bin/env python3
"""kasegi round-93 C1 counter (successor of the round-92 counter): the resolve.py
meter over the corpus/knowledge scope plus every file a label cites, tranche 8
(the round-93 labels: the two errata cell repairs, the 454 second-token repoint
and the two 58/144 lane-root repoints; round 93 adds the `cell-repair` and
lane-root `SKILL.md:N[-M]` kinds the round-92 counter could not express, and
walks every labelled citing file in M3, not only corpus/knowledge).

Usage:
  python3 knowledge-meter.py --lane LANE --base-rev REV --after-rev REV --map MAP.tsv \
      --labels-rev REV --base-target NUM/DEN --target NUM/DEN [--map-sha256 HEX] [--work DIR]
  python3 knowledge-meter.py --lane LANE --measure-rev REV [--work DIR]

Every reading is pinned to the measured revision (round-90 R142): the scope files
and the tree the citations are classified against are both `git archive REV`
extracts in a scratch dir, and resolve.py is imported from that extract.
Absolute-path citations are printed on a HOST line.

Map (TSV, # comments): `citing-file:line<TAB>key<TAB>old<TAB>new`, one row per
(site, key) pair (round-91 closure routed defect 2: the map names the label key, so
completeness is checked on pairs, not sites); `old` and `new` are literal substrings
of the citing line (backticks included); `new` may be empty (a dropped token).

Label kinds and the edit each names (expected_edit; the counter derives the edit
from the label row and the base line, never from the map):
  range        label `corpus/knowledge/<name>.md:N-M` -> old "`key`", new "`label`".
  qualify      label CORRECT, fix "No content change; qualify to corpus/knowledge/<key>"
               -> old "`key`", new "`corpus/knowledge/key`" (round-91 routed: a
               CORRECT label's qualification edit is now expressible).
  no-edit      label CORRECT, fix "No edit" -> no edit; the pair must stay unmapped
               and its line unchanged (M3).
  dash-cell    content-repair, fix "Replace with — (" with no "drop only" clause ->
               old "MATCHES: `key`", new "—".
  drop-token   content-repair, fix "Replace with — (drop only the `key` token" ->
               old ", `key`", new "" (the cell's other ties stay).
  named        content-repair, fix "Replace with <name>.md:N-M (" with no "drop the"
               clause -> old "`key`", new "`corpus/knowledge/<name>.md:N-M`".
  named-cell   content-repair, fix "Replace with <name>.md:N-M (" carrying a "drop
               the" clause -> old = the whole last table cell of the base line
               (stripped), new "MATCHES: `corpus/knowledge/<name>.md:N-M`".
EXCLUDED pairs (frozen before data, reasons in EXCLUDED) must stay unmapped.

Limbs (all must hold; one LIMB line each, then the verdict line):
  M0 base      base rate equals the frozen --base-target exactly.
  M1 meter     after rate equals the frozen --target exactly.
  M3 linediff  same file set and line counts; every after line equals its base
               line, except each mapped site line, which equals its base line
               with `old` replaced by `new` once; each `old` occurs exactly once
               on its base line.
  M4 binding   every backticked `corpus/knowledge/<name>.md:N[-M]` value a row
               writes names the file its key names, the only tracked file outside
               .ufo/ with that basename, INTERNAL in the after scope; a removal
               row (new `—` or empty) removes exactly one backticked key.
  M5 inrange   every written value's anchor lies inside the entry at --after-rev.
  M6 mapsha    sha256 of the map file equals --map-sha256 (when given).
  M9 labels    every map row binds the LABELS_PATH row (at --labels-rev) with the
               same (citing-file:line, key) pair, and (old, new) equals the edit
               that label names (above).
  M10 complete the set of mapped (site, key) pairs equals the set of labelled
               pairs whose label names an edit, minus EXCLUDED, exactly; every
               no-edit and EXCLUDED pair is unmapped; the set is non-empty.

Exit 0 only when every limb holds; 1 when a limb fails; 2 on usage or read error.
"""
import argparse
import hashlib
import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

KEYFILE = re.compile(r"^`([A-Za-z0-9][A-Za-z0-9._-]*\.md)(?::[0-9][0-9, -]*)?`$")
VAL = re.compile(r"^`corpus/knowledge/([A-Za-z0-9][A-Za-z0-9._-]*\.md):(\d+)(?:-(\d+))?`$")
FIXNAME = re.compile(r"^Replace with ([A-Za-z0-9][A-Za-z0-9._-]*\.md:\d+(?:-\d+)?)\b")
FIXDASH = re.compile(r"^Replace (?:MATCHES )?with — ")
DROPTOK = "drop only the `%s` token"
LABELS_PATH = ".ufo/waves/round-93/c1/labels.tsv"
FIXCELL = re.compile(r"^Replace cell with: (.+)$")
LANE_LABEL = re.compile(r"^SKILL\.md:\d+(?:-\d+)?$")
LANEVAL = re.compile(r"^`SKILL\.md:(\d+)(?:-(\d+))?`$")
FIXQUAL = re.compile(r"^No content change; qualify to corpus/knowledge/([A-Za-z0-9][A-Za-z0-9._-]*\.md:\d+(?:-\d+)?)\b")
VALANY = re.compile(r"`(corpus/knowledge/[A-Za-z0-9][A-Za-z0-9._-]*\.md:\d+(?:-\d+)?)`")
BARE = re.compile(r"`([A-Za-z0-9][A-Za-z0-9._-]*\.md(?::[0-9][0-9, -]*)?)`")
# (site, key) pairs whose label names an edit but which this tranche leaves unmapped,
# frozen before any edit was scored.
EXCLUDED = {}
DASH = "—"


def git(lane, *args, binary=False):
    r = subprocess.run(["git", "-C", lane] + list(args), capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode("utf-8")


def extract(lane, rev, work):
    d = tempfile.mkdtemp(prefix="kmeter92-tree-", dir=work)
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


def file_at(tree, rel):
    try:
        with open(os.path.join(tree, rel), encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def classify_scope(R, tree, files, work):
    d = tempfile.mkdtemp(prefix="kmeter92-scope-", dir=work)
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
        info = {"files": files, "cls": cls, "tracked": tracked, "mirror_absent": R.MIRROR_ABSENT, "tree": tree}
        info["classify"] = lambda t, R=R, tree=tree: R.classify(t, tree, os.path.expanduser(R.MIRROR_ROOT))[0]
        return info
    except Exception:
        shutil.rmtree(tree, ignore_errors=True)
        raise


def parse_target(s):
    n, m = s.split("/")
    return int(n), int(m)


def load_labels(text):
    """Return {(citing-file:line, key): (label, fix)} from the 5-column label TSV."""
    out = {}
    for i, ln in enumerate(text.split("\n")):
        if not ln.strip() or ln.startswith("#") or i == 0 and ln.startswith("line\t"):
            continue
        c = ln.split("\t")
        if len(c) != 5:
            raise ValueError("label row has %d columns" % len(c))
        out[(c[0], c[1])] = (c[2], c[3])
    return out


def last_cell(line):
    cells = line.rstrip().split("|")
    return cells[-2].strip() if line.rstrip().endswith("|") and len(cells) >= 3 else None


def expected_edit(key, label, fix, line):
    """Return (kind, old, new) the label names for its base line; None for no edit."""
    if label.startswith("corpus/knowledge/") or LANE_LABEL.match(label):
        return "range", "`%s`" % key, "`%s`" % label
    if label == "CORRECT":
        m = FIXQUAL.match(fix)
        if m and m.group(1) == key:
            return "qualify", "`%s`" % key, "`corpus/knowledge/%s`" % key
        if fix.startswith("No edit"):
            return None
        return "unknown", None, None
    if label == "cell-repair":
        m = FIXCELL.match(fix)
        if m:
            return "cell-repair", last_cell(line), m.group(1)
        return "unknown", None, None
    if label == "content-repair":
        if FIXDASH.match(fix):
            if (DROPTOK % key) in fix:
                return "drop-token", ", `%s`" % key, ""
            return "dash-cell", "MATCHES: `%s`" % key, DASH
        m = FIXNAME.match(fix)
        if m:
            new = "`corpus/knowledge/%s`" % m.group(1)
            if "drop the" in fix:
                cell = last_cell(line)
                return "named-cell", cell, "MATCHES: " + new
            return "named", "`%s`" % key, new
    return "unknown", None, None


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
                    site, key, old, new = ln.split("\t")
                    f, n = site.rsplit(":", 1)
                    rows.append((f, int(n), key, old, new))
            tn, tm = parse_target(a.target)
            bn0, bm0 = parse_target(a.base_target)
            labels = load_labels(git(lane, "show", "%s:%s" % (a.labels_rev, LABELS_PATH)))
            B = reading(lane, a.base_rev, a.work)
            trees.append(B["tree"])
            A = reading(lane, a.after_rev, a.work)
            trees.append(A["tree"])
        except Exception as e:
            print("KNOWLEDGE-METER-RESULT error reason=read:%s rc=2" % type(e).__name__)
            return 2
        bcls, acls, bfiles, afiles = B["cls"], A["cls"], B["files"], A["files"]
        labelled_files = {site.rsplit(":", 1)[0] for site, _ in labels} | {r[0] for r in rows}
        for rel in sorted(labelled_files - set(bfiles)):
            b, atext = file_at(B["tree"], rel), file_at(A["tree"], rel)
            if b is not None and atext is not None:
                bfiles[rel], afiles[rel] = b, atext
        bn, bm = rate(bcls)
        an, am = rate(acls)
        print("KNOWLEDGE-METER base=%d/%d after=%d/%d base_target=%d/%d target=%d/%d sites=%d labels=%d mirror_absent=%s pinned=archive" % (
            bn, bm, an, am, bn0, bm0, tn, tm, len(rows), len(labels), A["mirror_absent"]))
        print(host_line("base", bcls))
        print(host_line("after", acls))
        limbs = [("M0", (bn, bm) == (bn0, bm0), "base=%d/%d" % (bn, bm)),
                 ("M1", (an, am) == (tn, tm), "after=%d/%d" % (an, am))]
        # M3 per-site line diff
        sites = {}
        dup = 0
        for f, n, _, old, new in rows:
            if (f, n) in sites:
                dup += 1
            sites[(f, n)] = (old, new)
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
                    if (rel, i) in sites:
                        old, new = sites[(rel, i)]
                        if b.count(old) != 1:
                            missing += 1
                        else:
                            fwd = b.replace(old, new, 1)
                    if fwd != x:
                        bad += 1
        limbs.append(("M3", same_files and bad == 0 and missing == 0 and dup == 0 and bool(rows),
                      "same_files=%s bad_lines=%d old_not_once=%d dup_rows=%d" % (same_files, bad, missing, dup)))
        # M4 binding, M5 in range
        bybase = {}
        for p in A["tracked"]:
            if not p.startswith(".ufo/"):
                bybase.setdefault(os.path.basename(p), []).append(p)
        m4bad, m5bad = [], []
        for f, n, key, old, new in rows:
            tag = "%s:%d" % (f.rsplit("/", 1)[-1], n)
            site = "%s:%d" % (f, n)
            lab = labels.get((site, key))
            blines = bfiles.get(f, "").split("\n")
            exp = expected_edit(key, lab[0], lab[1], blines[n - 1] if lab and 1 <= n <= len(blines) else "") if lab else None
            is_cell = bool(exp and exp[0] == "cell-repair")
            km = KEYFILE.match("`%s`" % key)
            if not km or ("`%s`" % key) not in old:
                m4bad.append(tag)
                continue
            name = km.group(1)
            if new in (DASH, ""):
                if len(BARE.findall(old)) != 1 or BARE.findall(old)[0] != key:
                    m4bad.append(tag)
                continue
            vals = VALANY.findall(new) + [m.group(0).strip("`") for m in LANEVAL.finditer(new)]
            vals = list(dict.fromkeys(vals))
            if not vals or (len(vals) != 1 and not is_cell):
                m4bad.append(tag)
                continue
            for v in vals:
                lv = LANEVAL.match("`%s`" % v)
                if lv:
                    if "SKILL.md" not in A["tracked"] or A["classify"](v) != "INTERNAL":
                        m4bad.append(tag)
                        continue
                    text = file_at(A["tree"], "SKILL.md")
                    lo = int(lv.group(1))
                    hi = int(lv.group(2)) if lv.group(2) else lo
                    if text is None or not (1 <= lo <= hi <= len(text.splitlines())):
                        m5bad.append(tag)
                    continue
                vm = VAL.match("`%s`" % v)
                if not (vm and vm.group(1) == name and bybase.get(name) == ["corpus/knowledge/" + name] and A["classify"](v) == "INTERNAL"):
                    m4bad.append(tag)
                    continue
                text = afiles.get("corpus/knowledge/" + name, file_at(A["tree"], "corpus/knowledge/" + name))
                lo = int(vm.group(2))
                hi = int(vm.group(3)) if vm.group(3) else lo
                if text is None or not (1 <= lo <= hi <= len(text.splitlines())):
                    m5bad.append(tag)
        limbs.append(("M4", not m4bad and bool(rows), "bad=%s" % (",".join(m4bad) or "none")))
        limbs.append(("M5", not m5bad and not m4bad, "out_of_range=%s" % (",".join(m5bad) or "none")))
        # M9 label binding
        m9bad = []
        for f, n, key, old, new in rows:
            site = "%s:%d" % (f, n)
            lab = labels.get((site, key))
            bl = bfiles.get(f, "").split("\n")
            line = bl[n - 1] if 1 <= n <= len(bl) else ""
            exp = expected_edit(key, lab[0], lab[1], line) if lab else None
            if lab is None or (site, key) in EXCLUDED or exp is None or exp[1:] != (old, new):
                m9bad.append("%s:%d" % (f.rsplit("/", 1)[-1], n))
        limbs.append(("M9", not m9bad and bool(rows), "rows=%d unbound=%s" % (len(rows), ",".join(m9bad) or "none")))
        # M10 completeness on (site, key) pairs
        mapped = {("%s:%d" % (f, n), k) for f, n, k, _, _ in rows}
        kinds = {}
        for (site, key), (label, fix) in labels.items():
            sf, sn = site.rsplit(":", 1)
            bl = bfiles.get(sf, "").split("\n")
            line = bl[int(sn) - 1] if 1 <= int(sn) <= len(bl) else ""
            e = expected_edit(key, label, fix, line)
            kinds[(site, key)] = "excluded" if (site, key) in EXCLUDED else ("no-edit" if e is None else e[0])
        want = {p for p, k in kinds.items() if k not in ("excluded", "no-edit")}
        unknown = sorted(p for p, k in kinds.items() if k == "unknown")
        unapplied = sorted(want - mapped)
        unlabelled = sorted(mapped - want)
        tally = ",".join("%s=%d" % (k, sum(1 for v in kinds.values() if v == k)) for k in sorted(set(kinds.values())))
        short = lambda ps: ",".join("%s/%s" % (s.rsplit("/", 1)[-1], k) for s, k in ps) or "none"
        limbs.append(("M10", bool(want) and not unapplied and not unlabelled and not unknown and set(EXCLUDED) <= set(kinds),
                      "labelled=%d want=%d mapped=%d kinds=%s unknown=%s unapplied=%s unlabelled=%s" % (
                          len(labels), len(want), len(mapped), tally, short(unknown), short(unapplied), short(unlabelled))))
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
