#!/usr/bin/env python3
"""Round-95 C1 controls: the frozen meter must pass on the candidate (rc=0,
pinned) and reject every do-nothing / forgery fixture (rc=1 with the named
limb, or rc=2).

Round-94 defect 1 repaired: every fixture is built from a CLONE OF THE PINNED
BASE COMMIT, never from the mutable live lane, so each control reproduces after
the tranche has landed. `--rev-of-lane` is not used anywhere.

Usage: c1-controls-r95.py CANDIDATE_CLONE R93_COUNTER WORK OUTDIR
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
C1 = LANE + "/.ufo/waves/round-95/c1"
BASE = "9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10"
MAP = C1 + "/repair-map.tsv"
LABELS = C1 + "/labels.tsv"
LABELS_REL = ".ufo/waves/round-95/c1/labels.tsv"
MAP_REL = ".ufo/waves/round-95/c1/repair-map.tsv"
BASE_TARGET = "1007/1998"
TARGET = "1008/1994"
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
    if sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip() != os.path.realpath(d):
        raise SystemExit("fixture root mismatch at " + d)
    return sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()


def clone(src, dest):
    shutil.rmtree(dest, ignore_errors=True)
    r = sh(["git", "clone", "-q", "--shared", src, dest])
    if r.returncode != 0:
        raise SystemExit(r.stderr)
    return dest


def fixture(cand, dest, edits=None, cell=None, map_append=None, label_append=None,
            drop_map_row=None, map_text=None, labels_text=None, new_files=None):
    """Clone the candidate (pinned), then apply one fixture delta."""
    d = clone(cand, dest)
    if label_append:
        write(os.path.join(d, LABELS_REL), read(os.path.join(d, LABELS_REL)) + label_append)
    if map_text is not None:
        write(os.path.join(d, MAP_REL), map_text)
    elif map_append or drop_map_row is not None:
        text = read(os.path.join(d, MAP_REL)).rstrip("\n").split("\n")
        if drop_map_row is not None:
            text = [ln for i, ln in enumerate(text) if i != drop_map_row]
        if map_append:
            text.append(map_append.rstrip("\n"))
        write(os.path.join(d, MAP_REL), "\n".join(text) + "\n")
    for rel, text in (new_files or {}).items():
        write(os.path.join(d, rel), text)
    files = {}
    for rel, n, old, new in (edits or []):
        if rel not in files:
            files[rel] = read(os.path.join(d, rel)).split("\n")
        if old not in files[rel][n - 1]:
            raise SystemExit("edit anchor missing at %s:%d" % (rel, n))
        files[rel][n - 1] = files[rel][n - 1].replace(old, new)
    if cell:
        rel, n, old, new = cell
        if rel not in files:
            files[rel] = read(os.path.join(d, rel)).split("\n")
        files[rel][n - 1] = files[rel][n - 1].replace(old, new)
    if labels_text is not None:
        write(os.path.join(d, LABELS_REL), labels_text)
    for rel, lines in files.items():
        write(os.path.join(d, rel), "\n".join(lines))
    rev = commit(d)
    sha = sh(["sha256sum", os.path.join(d, MAP_REL)]).stdout.split()[0]
    return d, rev, sha


def main(argv):
    cand, r93, work, outdir = argv
    os.makedirs(work, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    results = []
    log = []

    def run(counter, lane, after, labels_pin, map_path, target, map_sha=None):
        wd = os.path.join(work, "w")
        os.makedirs(wd, exist_ok=True)
        cmd = [sys.executable, "-B", counter, "--lane", lane, "--base-rev", BASE,
               "--after-rev", after, "--map", map_path, "--labels-rev", labels_pin,
               "--base-target", BASE_TARGET, "--target", target, "--work", wd]
        if map_sha:
            cmd += ["--map-sha256", map_sha]
        p = sh(cmd)
        return p.returncode, p.stdout + p.stderr

    def record(name, rc, want, out, extra=""):
        ok = rc == want
        results.append(ok)
        line = "CONTROL %s rc=%d want=%d %s%s" % (name, rc, want, "PASS" if ok else "FAIL", extra)
        print(line)
        log.append(line)
        for ln in out.splitlines():
            if ln.startswith(("KNOWLEDGE-METER ", "LIMB ", "KNOWLEDGE-METER-RESULT")) or "Traceback" in ln:
                print("  " + ln)
                log.append("  " + ln)

    meter = C1 + "/knowledge-meter.py"
    real_sha = sh(["sha256sum", MAP]).stdout.split()[0]
    cand_rev = sh(["git", "-C", cand, "rev-parse", "HEAD"]).stdout.strip()
    print("C1-CONTROLS candidate=%s base=%s" % (cand_rev, BASE))
    log.append("C1-CONTROLS candidate=%s base=%s r93=%s work=%s" % (cand_rev, BASE, r93, work))

    # 1. candidate (the clone already carries every edit)
    rc, out = run(meter, cand, cand_rev, cand_rev, MAP, TARGET, real_sha)
    record("candidate", rc, 0, out)

    # 2. do-nothing: the after revision is the base
    rc, out = run(meter, cand, BASE, cand_rev, MAP, TARGET, real_sha)
    record("do-nothing", rc, 1, out)

    # 3. partial: one map row dropped (and its edit not applied)
    d, rev, sha = fixture(cand, os.path.join(work, "fx-partial"), drop_map_row=3)
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("partial-row-dropped", rc, 1, out, extra=" limb=%s" % ("LIMB M10 FAIL" in out))

    # 4. extra unlisted edit: an edit the map does not name (one more token change)
    d, rev, sha = fixture(cand, os.path.join(work, "fx-extra"),
                          edits=[("corpus/knowledge/triage-thresholds.md", 143, "SKILL.md:251-253", "SKILL.md:252")])
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("extra-unlisted-edit", rc, 1, out, extra=" limb=%s" % ("LIMB M3 FAIL" in out))

    # 5. wrong new text: the map carries a different value than the label names
    mapt = read(MAP).replace("`SKILL.md:335-338`", "`SKILL.md:336-338`", 1)
    d, rev, sha = fixture(cand, os.path.join(work, "fx-m9"), map_text=mapt,
                          cell=("corpus/knowledge/triage-thresholds.md", 396, "`SKILL.md:245-247`", "`SKILL.md:336-338`"))
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("wrong-new", rc, 1, out, extra=" limb=%s" % ("LIMB M9 FAIL" in out))

    # 6. out-of-range lane token
    lab = "notes/r95-ctl.md:1\tSKILL.md:5\tSKILL.md:9999\tRepoint: out of range.\tevidence\n"
    mp = "notes/r95-ctl.md:1\tSKILL.md:5\t`SKILL.md:5`\t`SKILL.md:9999`\n"
    d, rev, sha = fixture(cand, os.path.join(work, "fx-range"),
                          edits=[("notes/r95-ctl.md", 1, "`SKILL.md:5`", "`SKILL.md:9999`")],
                          label_append=lab, map_append=mp,
                          new_files={"notes/r95-ctl.md": "see `SKILL.md:5` now\n"})
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("m5-out-of-range", rc, 1, out, extra=" limb=%s" % ("LIMB M5 FAIL" in out))

    # 7. snapshot target that does not exist: the map's new value moves one
    # applied row to a non-existent capture directory, and the file follows it
    mapt = read(MAP).replace(
        "`corpus/source-snapshots/round-30/S041.txt:1868-1870`",
        "`corpus/source-snapshots/round-31/S041.txt:1868-1870`", 1)
    d, rev, sha = fixture(cand, os.path.join(work, "fx-snap"), map_text=mapt,
                          cell=("corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md", 13,
                                "`corpus/source-snapshots/round-30/S041.txt:1868-1870`",
                                "`corpus/source-snapshots/round-31/S041.txt:1868-1870`"))
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("snapshot-missing", rc, 1, out, extra=" limb=%s" % ("LIMB M4 FAIL" in out))

    # 8. labels file missing at the pinned path (rc 2)
    d, rev, sha = fixture(cand, os.path.join(work, "fx-nolabels"))
    os.unlink(os.path.join(d, LABELS_REL))
    rev = commit(d)
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("missing-labels", rc, 2, out)

    # 9. wrong map sha
    rc, out = run(meter, cand, cand_rev, cand_rev, MAP, TARGET, "0" * 64)
    record("wrong-map-sha", rc, 1, out, extra=" limb=%s" % ("LIMB M6 FAIL" in out))

    # 10. map row whose label is absent (unlabelled)
    mapt = read(MAP) + "corpus/knowledge/triage-thresholds.md:143\tSKILL.md:526\t`SKILL.md:526`\t`SKILL.md:527`\n"
    d, rev, sha = fixture(cand, os.path.join(work, "fx-unlabelled"), map_text=mapt,
                          cell=("corpus/knowledge/triage-thresholds.md", 143, "`SKILL.md:526`", "`SKILL.md:527`"))
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("unlabelled-row", rc, 1, out, extra=" limb=%s" % ("LIMB M9 FAIL" in out))

    # 11. part edit applied as a cell edit (anchor destroyed -> M3)
    d, rev, sha = fixture(cand, os.path.join(work, "fx-part"), drop_map_row=0,
                          cell=("corpus/knowledge/triage-thresholds.md", 89,
                                "SUPERSEDES: `SKILL.md:175` — that line writes `reward.min`, source multiplies by 1000",
                                "SUPERSEDES: `SKILL.md:175` — that line writes `reward.min`, source multiplies by 1000 "))
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("part-as-cell", rc, 1, out, extra=" limb=%s" % ("LIMB M3 FAIL" in out))

    # 12. discrimination: the round-93 counter crashes on a labelled file it
    # cannot open through the knowledge-only scope (round-93 M93-5)
    lab = "corpus/QUALITY.md:537\tSKILL.md:1224\tSKILL.md:1225\tRepoint: the anchor moves.\tevidence\n"
    mapt = "corpus/QUALITY.md:537\tSKILL.md:1224\t`SKILL.md:1224`\t`SKILL.md:1225`\n"
    d, rev, sha = fixture(cand, os.path.join(work, "fx-union"), label_append=lab, map_append=mapt,
                          edits=[("corpus/QUALITY.md", 537, "`SKILL.md:1224`", "`SKILL.md:1225`")])
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("union-applied", rc, 0, out)
    rc93, out93 = run(r93, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("union-applied-before-r93", rc93, 1, out93, extra=" traceback=%s" % ("Traceback" in out93))

    # 13. the round-94 defect fixture, pinned: the r93 counter accepts a cell
    # repair that rewrites a whole cell (its M5 ignores cell replacements).
    old_cell = "`claim-package-contract.md:13,15,33-38` (implies gate-enforced)"
    new_cell = "MATCHES: `corpus/knowledge/claim-package-contract.md:9-16`, `SKILL.md:9999`"
    row = ("corpus/knowledge/triage-thresholds.md:440\tclaim-package-contract.md:13,15,33-38\tcell-repair\t"
           "Replace cell with: " + new_cell + "\tevidence\n")
    mp = ("corpus/knowledge/triage-thresholds.md:440\tclaim-package-contract.md:13,15,33-38\t"
          + old_cell + "\t" + new_cell + "\n")
    d, rev, sha = fixture(cand, os.path.join(work, "fx-cell"), label_append=row, map_append=mp,
                          cell=("corpus/knowledge/triage-thresholds.md", 440, old_cell, new_cell))
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("cell-repair-lane-root", rc, 1, out, extra=" limb=%s" % ("LIMB M5 FAIL" in out))

    # 14. one cell, two keys, both mapped as whole-cell replacements (the
    # round-94 shape): the second old string is gone, so the composition fails.
    dup = ("corpus/knowledge/triage-thresholds.md:88\tSKILL.md:113-114\tcell-repair\t"
           "Replace cell with: " + read(os.path.join(cand, "corpus/knowledge/triage-thresholds.md")).split("\n")[87].rstrip().rstrip("|").split("|")[-2].strip()
           + "\tevidence\n")
    mp2 = ("corpus/knowledge/triage-thresholds.md:88\tSKILL.md:113-114\t"
           + read(os.path.join(cand, "corpus/knowledge/triage-thresholds.md")).split("\n")[87].rstrip().rstrip("|").split("|")[-2].strip()
           + "\tnoop\n")
    d, rev, sha = fixture(cand, os.path.join(work, "fx-dup"), label_append=dup, map_append=mp2)
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("two-cells-one-line", rc, 1, out, extra=" limb=%s" % ("LIMB M3 FAIL" in out))

    print("C1-CONTROLS-RESULT %s controls=%d" % ("pass" if all(results) else "fail", len(results)))
    write(os.path.join(outdir, "c1-controls-r95.txt"),
          "\n".join(log + ["C1-CONTROLS-RESULT %s controls=%d" % ("pass" if all(results) else "fail", len(results))]) + "\n")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
