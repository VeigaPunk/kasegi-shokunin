#!/usr/bin/env python3
"""ExecC1Indep independent C1 re-derivation (round 91, tranche 6).

Uses ONLY `git show` bytes for base/landing triage-thresholds.md and the label
TSV at the pinned labels revision, plus the frozen repair-map.tsv bytes on disk
(sha256-checked). No lane counter code is imported; the label-binding rule is
reimplemented from the counter's docstring:
  - a range label (label column starts with `corpus/knowledge/`) names
    old "`key`" -> new "`label`";
  - a content-repair label whose fix replaces the tie with an em dash names
    old "MATCHES: `key`" -> new the em dash;
  - a content-repair label whose fix names `<name>.md:N[-M]` names
    old "`key`" -> new "`corpus/knowledge/<name>.md:N[-M]`".

Checks:
  C1.a base vs landing differ on exactly lines 141,142,226,368,454,457
       (same line count, every other line byte-equal);
  C1.b each landed line equals its base line with the map's old->new applied
       once, and each old occurs exactly once on its base line;
  C1.c every map row matches its label row under the docstring rule;
  C1.d the labelled site set equals the mapped site set (non-empty).
"""
import hashlib
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BASE = "bb4309fffbe9bf98153a2933af72c8f2c3f4b5b1"
AFTER = "8a1a00c639ba808a701d1f186aac9ebd0045deaa"
LABELS_REV = "e993fd181e320f1f21e06b05e16c68b0f07cff76"
TARGET = "corpus/knowledge/triage-thresholds.md"
MAP = LANE + "/.ufo/waves/round-91/c1/repair-map.tsv"
LABELS_PATH = ".ufo/waves/round-90/w1/ReviewC1Sites-receipts/round91-labels.tsv"
MAP_SHA = "55d50b661bcf79ad5a435c7d7bc86e3954e9910f7dabc480236224170c8c0a7a"
SITES = {141, 142, 226, 368, 454, 457}
DASH = "—"
FIXNAME = re.compile(r"^Replace with ([A-Za-z0-9][A-Za-z0-9._-]*\.md:\d+(?:-\d+)?)\b")
FIXDASH = re.compile(r"^Replace (?:MATCHES )?with — ")


def show(rev, path):
    r = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                       capture_output=True, check=True)
    return r.stdout.decode("utf-8")


def key_of(old):
    return old[len("MATCHES: "):][1:-1] if old.startswith("MATCHES: ") else old[1:-1]


def expected_edit(key, label, fix):
    if label.startswith("corpus/knowledge/"):
        return "`%s`" % key, "`%s`" % label
    if label == "content-repair":
        if FIXDASH.match(fix):
            return "MATCHES: `%s`" % key, DASH
        m = FIXNAME.match(fix)
        if m:
            return "`%s`" % key, "`corpus/knowledge/%s`" % m.group(1)
    return None


def main():
    fails = []
    mb = open(MAP, "rb").read()
    got = hashlib.sha256(mb).hexdigest()
    print("map sha256 %s %s" % (got, "ok" if got == MAP_SHA else "MISMATCH"))
    if got != MAP_SHA:
        fails.append("map sha256 mismatch")
    rows = []
    for ln in mb.decode("utf-8").split("\n"):
        if ln.strip() and not ln.startswith("#"):
            site, old, new = ln.split("\t")
            f, n = site.rsplit(":", 1)
            rows.append((f, int(n), old, new))

    btext, atext = show(BASE, TARGET), show(AFTER, TARGET)
    bl, al = btext.split("\n"), atext.split("\n")
    diff = None
    if len(bl) != len(al):
        fails.append("line count differs %d vs %d" % (len(bl), len(al)))
    else:
        diff = sorted(i for i, (b, a) in enumerate(zip(bl, al), 1) if b != a)
        ok = set(diff) == SITES
        print("C1.a differ-lines=%s %s" % (diff, "ok" if ok else "FAIL"))
        if not ok:
            fails.append("diff lines %s != %s" % (diff, sorted(SITES)))

    sites = {}
    for f, n, old, new in rows:
        if (f, n) in sites:
            fails.append("dup map row %s:%d" % (f, n))
        sites[(f, n)] = (old, new)
    for (f, n), (old, new) in sorted(sites.items()):
        if f != TARGET:
            fails.append("map row outside target %s:%d" % (f, n))
            continue
        b = bl[n - 1]
        if b.count(old) != 1:
            fails.append("old not exactly once at %s:%d" % (f, n))
            continue
        ok = b.replace(old, new, 1) == al[n - 1]
        print("C1.b %s:%d one-shot old->new %s" % (f.rsplit("/", 1)[-1], n,
                                                   "ok" if ok else "FAIL"))
        if not ok:
            fails.append("old->new mismatch at %s:%d" % (f, n))

    lt = show(LABELS_REV, LABELS_PATH)
    labels = {}
    for i, ln in enumerate(lt.split("\n")):
        if not ln.strip() or ln.startswith("#") or (i == 0 and ln.startswith("line\t")):
            continue
        c = ln.split("\t")
        if len(c) != 5:
            fails.append("label line %d has %d cols" % (i + 1, len(c)))
            continue
        labels[(c[0], c[1])] = (c[2], c[3])
    for f, n, old, new in rows:
        lab = labels.get(("%s:%d" % (f, n), key_of(old)))
        ok = lab is not None and expected_edit(key_of(old), lab[0], lab[1]) == (old, new)
        print("C1.c %s:%d label-bound %s" % (f.rsplit("/", 1)[-1], n,
                                             "ok" if ok else "FAIL"))
        if not ok:
            fails.append("map row unbound to label %s:%d" % (f, n))
    mapped = {"%s:%d" % (f, n) for f, n, _, _ in rows}
    labelled = {s for s, _ in labels}
    unapplied, unlabelled = sorted(labelled - mapped), sorted(mapped - labelled)
    ok = bool(labelled) and not unapplied and not unlabelled
    print("C1.d labelled=%d mapped=%d unapplied=%s unlabelled=%s %s" % (
        len(labelled), len(mapped), unapplied or "none", unlabelled or "none",
        "ok" if ok else "FAIL"))
    if not ok:
        fails.append("label/mapped set mismatch")

    verdict = "INDEP-C1-RESULT pass rc=0" if not fails else "INDEP-C1-RESULT fail rc=1"
    print(verdict)
    for x in fails:
        print("FAIL:", x)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
