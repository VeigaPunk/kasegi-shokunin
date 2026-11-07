#!/usr/bin/env python3
"""Round-94 C1 controls: the frozen meter must pass on the candidate (rc=0,
pinned) and reject every do-nothing / forgery fixture (rc=1 with the named
limb, or rc=2). Two fixtures are discriminating: the round-93 counter cannot
evaluate a labelled non-knowledge file (it crashes) and it accepts an
out-of-range lane-root token inside a cell replacement.

Every fixture is the candidate clone plus one label row and one map row, so the
real 29-row label set and its EXCLUDED pairs stay present.

Usage: c1-controls-r94.py CANDIDATE_CLONE R93_COUNTER WORK OUTDIR
"""
import os
import shutil
import subprocess
import sys

R94 = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-94/c1"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BASE = "dff5a0a01e8aafe6be81f4ee61567745c3c4c485"
LABELS_R94 = ".ufo/waves/round-94/c1/labels.tsv"
LABELS_R93 = ".ufo/waves/round-93/c1/labels.tsv"
MAP_R94 = ".ufo/waves/round-94/c1/repair-map.tsv"
HEADER = "line\tkey\tlabel\tfix\tevidence\n"


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def commit(d):
    sh(["git", "-C", d, "add", "-A"])
    sh(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
        "commit", "-q", "-m", "fixture"])
    return sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()


def cand_fixture(cand, dest, label_row, map_row, edits, new_files=None):
    """Clone the candidate, append one label row (round-94 path) and one map
    row, apply `edits` [(rel, line, old, new)], commit, return (dest, rev, sha)."""
    shutil.rmtree(dest, ignore_errors=True)
    sh(["git", "clone", "-q", "--shared", cand, dest])
    write(os.path.join(dest, LABELS_R94), read(os.path.join(dest, LABELS_R94)) + label_row)
    write(os.path.join(dest, LABELS_R93), HEADER + label_row)
    write(os.path.join(dest, MAP_R94), read(os.path.join(dest, MAP_R94)) + map_row)
    for rel, text in (new_files or {}).items():
        write(os.path.join(dest, rel), text)
    files = {}
    for rel, n, old, new in edits:
        if rel not in files:
            files[rel] = read(os.path.join(dest, rel)).split("\n")
        if old not in files[rel][n - 1]:
            raise SystemExit("edit anchor missing at %s:%d" % (rel, n))
        files[rel][n - 1] = files[rel][n - 1].replace(old, new)
    for rel, lines in files.items():
        write(os.path.join(dest, rel), "\n".join(lines))
    rev = commit(dest)
    return dest, rev, sh(["sha256sum", os.path.join(dest, MAP_R94)]).stdout.split()[0]


def main(argv):
    cand, r93, work, outdir = argv
    os.makedirs(work, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    results = []

    def run(counter, lane, after, labels_rev, map_path, target, map_sha=None):
        wd = os.path.join(work, "w")
        os.makedirs(wd, exist_ok=True)
        cmd = [sys.executable, "-B", counter, "--lane", lane, "--base-rev", BASE,
               "--after-rev", after, "--map", map_path, "--labels-rev", labels_rev,
               "--base-target", "1008/1999", "--target", target, "--work", wd]
        if map_sha:
            cmd += ["--map-sha256", map_sha]
        p = sh(cmd)
        return p.returncode, p.stdout + p.stderr

    def record(name, rc, want, out, extra=""):
        ok = rc == want
        results.append(ok)
        print("CONTROL %s rc=%d want=%d %s%s" % (name, rc, want, "PASS" if ok else "FAIL", extra))
        for line in out.splitlines():
            if line.startswith(("KNOWLEDGE-METER ", "LIMB ", "KNOWLEDGE-METER-RESULT")) or "Traceback" in line:
                print("  " + line)

    real_map_sha = sh(["sha256sum", os.path.join(R94, "repair-map.tsv")]).stdout.split()[0]
    cand_rev = sh(["git", "-C", cand, "rev-parse", "HEAD"]).stdout.strip()
    print("C1-CONTROLS candidate=%s base=%s" % (cand_rev, BASE))

    rc, out = run(os.path.join(R94, "knowledge-meter.py"), cand, cand_rev, cand_rev,
                  os.path.join(R94, "repair-map.tsv"), "1009/2000", map_sha=real_map_sha)
    record("candidate", rc, 0, out)

    rc, out = run(os.path.join(R94, "knowledge-meter.py"), cand, BASE, cand_rev,
                  os.path.join(R94, "repair-map.tsv"), "1009/2000", map_sha=real_map_sha)
    record("do-nothing", rc, 1, out)

    # A/B: a label on a file outside corpus/knowledge (round-93 M93-5). The
    # round-93 counter crashes on the union; the round-94 counter compares it.
    lab = "corpus/QUALITY.md:537\tSKILL.md:1224\tSKILL.md:1225\tRepoint: the anchor moves.\tevidence\n"
    mapt = "corpus/QUALITY.md:537\tSKILL.md:1224\t`SKILL.md:1224`\t`SKILL.md:1225`\n"
    d, rev, fsha = cand_fixture(cand, os.path.join(work, "fx-union"), lab, mapt,
                                [("corpus/QUALITY.md", 537, "`SKILL.md:1224`", "`SKILL.md:1225`")])
    rc, out = run(os.path.join(R94, "knowledge-meter.py"), d, rev, rev, os.path.join(d, MAP_R94),
                  "1009/2000", map_sha=fsha)
    record("m3-union-applied", rc, 0, out)
    rc93, out93 = run(r93, d, rev, rev, os.path.join(d, MAP_R94), "1009/2000", map_sha=fsha)
    record("m3-union-applied-before-r93", rc93, 1, out93, extra=" traceback=%s" % ("Traceback" in out93))

    d, rev, fsha = cand_fixture(cand, os.path.join(work, "fx-union-bad"), lab, mapt,
                                [("corpus/QUALITY.md", 537, "`SKILL.md:1224`", "`SKILL.md:1225` extra")])
    rc, out = run(os.path.join(R94, "knowledge-meter.py"), d, rev, rev, os.path.join(d, MAP_R94),
                  "1009/2000", map_sha=fsha)
    record("m3-union-unmapped", rc, 1, out, extra=" limb=%s" % ("LIMB M3 FAIL" in out))

    # C: a cell-repair replacement carrying an out-of-range lane-root token
    # beside a valid corpus/knowledge token (round-93 M93-3 F1). The fixture
    # line is corpus/knowledge/triage-thresholds.md:58 (`MATCHES: SKILL.md:191`).
    old_cell = "`claim-package-contract.md:13,15,33-38` (implies gate-enforced)"
    new_cell = "MATCHES: `corpus/knowledge/claim-package-contract.md:9-16`, `SKILL.md:9999`"
    cell = ("corpus/knowledge/triage-thresholds.md:440\tclaim-package-contract.md:13,15,33-38\tcell-repair\t"
            "Replace cell with: " + new_cell + "\tevidence\n")
    cell_map = ("corpus/knowledge/triage-thresholds.md:440\tclaim-package-contract.md:13,15,33-38\t"
                + old_cell + "\t" + new_cell + "\n")
    d, rev, fsha = cand_fixture(cand, os.path.join(work, "fx-cell"), cell, cell_map,
                                [("corpus/knowledge/triage-thresholds.md", 440, old_cell, new_cell)])
    rc, out = run(os.path.join(R94, "knowledge-meter.py"), d, rev, rev, os.path.join(d, MAP_R94),
                  "1010/2001", map_sha=fsha)
    record("m5-cell-repair-lane-root", rc, 1, out, extra=" limb=%s" % ("LIMB M5 FAIL" in out))
    # the same cell row on a lane-based minimal fixture: no real edits, so the
    # round-93 counter has nothing but the cell row to evaluate.
    d2 = os.path.join(work, "fx-cell-before")
    shutil.rmtree(d2, ignore_errors=True)
    sh(["git", "clone", "-q", "--shared", LANE, d2])
    write(os.path.join(d2, LABELS_R93), HEADER + cell)
    write(os.path.join(d2, MAP_R94), cell_map)
    text = read(os.path.join(d2, "corpus/knowledge/triage-thresholds.md")).split("\n")
    text[439] = text[439].replace(old_cell, new_cell)
    write(os.path.join(d2, "corpus/knowledge/triage-thresholds.md"), "\n".join(text))
    rev2 = commit(d2)
    fsha2 = sh(["sha256sum", os.path.join(d2, MAP_R94)]).stdout.split()[0]
    rc93, out93 = run(r93, d2, rev2, rev2, os.path.join(d2, MAP_R94), "1009/2000", map_sha=fsha2)
    record("m5-cell-repair-before-r93", rc93, 0, out93)

    # D: a token row to an out-of-range anchor.
    labd = "notes/r94-ctl3.md:1\tSKILL.md:5\tSKILL.md:9999\tRepoint: out of range.\tevidence\n"
    mapd = "notes/r94-ctl3.md:1\tSKILL.md:5\t`SKILL.md:5`\t`SKILL.md:9999`\n"
    d, rev, fsha = cand_fixture(cand, os.path.join(work, "fx-range"), labd, mapd,
                                [("notes/r94-ctl3.md", 1, "`SKILL.md:5`", "`SKILL.md:9999`")],
                                {"notes/r94-ctl3.md": "see `SKILL.md:5` now\n"})
    rc, out = run(os.path.join(R94, "knowledge-meter.py"), d, rev, rev, os.path.join(d, MAP_R94),
                  "1009/2000", map_sha=fsha)
    record("m5-out-of-range", rc, 1, out, extra=" limb=%s" % ("LIMB M5 FAIL" in out))

    # E: the map's new text differs from the label's.
    labe = "notes/r94-ctl4.md:1\tSKILL.md:7\tSKILL.md:8\tRepoint: the anchor moves.\tevidence\n"
    mape = "notes/r94-ctl4.md:1\tSKILL.md:7\t`SKILL.md:7`\t`SKILL.md:9`\n"
    d, rev, fsha = cand_fixture(cand, os.path.join(work, "fx-m9"), labe, mape,
                                [("notes/r94-ctl4.md", 1, "`SKILL.md:7`", "`SKILL.md:9`")],
                                {"notes/r94-ctl4.md": "see `SKILL.md:7` now\n"})
    rc, out = run(os.path.join(R94, "knowledge-meter.py"), d, rev, rev, os.path.join(d, MAP_R94),
                  "1009/2000", map_sha=fsha)
    record("m9-wrong-new", rc, 1, out, extra=" limb=%s" % ("LIMB M9 FAIL" in out))

    # F: a map row for an EXCLUDED pair.
    d = os.path.join(work, "fx-excluded")
    shutil.rmtree(d, ignore_errors=True)
    sh(["git", "clone", "-q", "--shared", cand, d])
    with open(os.path.join(d, MAP_R94), "a", encoding="utf-8") as fh:
        fh.write("corpus/knowledge/triage-thresholds.md:88\tSKILL.md:113-114\t`SKILL.md:113-114`\t`SKILL.md:182-184`\n")
    text = read(os.path.join(d, "corpus/knowledge/triage-thresholds.md")).split("\n")
    text[87] = text[87].replace("`SKILL.md:113-114`", "`SKILL.md:182-184`")
    write(os.path.join(d, "corpus/knowledge/triage-thresholds.md"), "\n".join(text))
    rev = commit(d)
    fsha = sh(["sha256sum", os.path.join(d, MAP_R94)]).stdout.split()[0]
    rc, out = run(os.path.join(R94, "knowledge-meter.py"), d, rev, rev, os.path.join(d, MAP_R94),
                  "1009/2000", map_sha=fsha)
    record("m10-excluded-mapped", rc, 1, out, extra=" limb=%s" % ("LIMB M10 FAIL" in out))

    # G: the labels file missing at the pinned path (rc 2).
    d = os.path.join(work, "fx-nolabels")
    shutil.rmtree(d, ignore_errors=True)
    sh(["git", "clone", "-q", "--shared", cand, d])
    os.unlink(os.path.join(d, LABELS_R94))
    rev = commit(d)
    rc, out = run(os.path.join(R94, "knowledge-meter.py"), d, rev, rev, os.path.join(d, MAP_R94),
                  "1009/2000", map_sha=real_map_sha)
    record("missing-labels", rc, 2, out)

    # H: wrong map sha.
    rc, out = run(os.path.join(R94, "knowledge-meter.py"), cand, cand_rev, cand_rev,
                  os.path.join(R94, "repair-map.tsv"), "1009/2000", map_sha="0" * 64)
    record("wrong-map-sha", rc, 1, out, extra=" limb=%s" % ("LIMB M6 FAIL" in out))

    print("C1-CONTROLS-RESULT %s controls=%d" % ("pass" if all(results) else "fail", len(results)))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
