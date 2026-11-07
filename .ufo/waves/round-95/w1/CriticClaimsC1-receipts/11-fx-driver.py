#!/usr/bin/env python3
"""CriticClaimsC1 forgery fixtures for round-95 C1. Every fixture is a
git clone --shared of the landing clone; the counter is run with the frozen
base rev and the fixture as after/labels/map."""
import hashlib
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r95/CriticClaimsC1"
LANE = S + "/lane"
COUNTER = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-95/c1/knowledge-meter.py"
BASE = "9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10"
LANDING = "53ec479d71d25cf5be052db794a548a5904564b8"
LABELS_REL = ".ufo/waves/round-95/c1/labels.tsv"
MAP_REL = ".ufo/waves/round-95/c1/repair-map.tsv"
TRIAGE = "corpus/knowledge/triage-thresholds.md"


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def last_cell(line):
    cells = line.rstrip().split("|")
    return cells[-2].strip() if line.rstrip().endswith("|") and len(cells) >= 3 else None


def commit(d):
    sh(["git", "-C", d, "add", "-A"])
    r = sh(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
            "commit", "-q", "-m", "forgery fixture"])
    if r.returncode != 0:
        raise SystemExit("commit failed: " + r.stderr)
    top = sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip()
    if top != os.path.realpath(d):
        raise SystemExit("fixture root mismatch: %r != %r" % (top, os.path.realpath(d)))
    return sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()


def clone_landing(dest):
    shutil.rmtree(dest, ignore_errors=True)
    r = sh(["git", "clone", "-q", "--shared", LANE, dest])
    if r.returncode != 0:
        raise SystemExit(r.stderr)
    top = sh(["git", "-C", dest, "rev-parse", "--show-toplevel"]).stdout.strip()
    if top != os.path.realpath(dest):
        raise SystemExit("clone root mismatch: %r != %r" % (top, os.path.realpath(dest)))
    return dest


def base_text(rel):
    return sh(["git", "-C", LANE, "show", "%s:%s" % (BASE, rel)]).stdout


def build(name, mutate):
    dest = os.path.join(S, "fx", name)
    clone_landing(dest)
    mutate(dest)
    rev = commit(dest)
    mp = os.path.join(dest, MAP_REL)
    sha = hashlib.sha256(open(mp, "rb").read()).hexdigest()
    wd = os.path.join(S, "fxwork", name)
    os.makedirs(wd, exist_ok=True)
    p = sh([sys.executable, "-B", COUNTER, "--lane", dest, "--base-rev", BASE,
            "--after-rev", rev, "--map", mp, "--labels-rev", rev,
            "--base-target", "1007/1998", "--target", "1008/1994",
            "--map-sha256", sha, "--work", wd])
    out = p.stdout + p.stderr
    os.makedirs(os.path.join(S, "out"), exist_ok=True)
    with open(os.path.join(S, "out", "fx-%s.txt" % name), "w", encoding="utf-8") as fh:
        fh.write("### fixture %s rev=%s rc=%d\n" % (name, rev, p.returncode))
        fh.write(out)
    print("### %s rc=%d rev=%s" % (name, p.returncode, rev))
    for ln in out.splitlines():
        if ln.startswith(("KNOWLEDGE-METER ", "LIMB ", "KNOWLEDGE-METER-RESULT")):
            print("  " + ln)
    return p.returncode, out


def set_line(dest, rel, lineno, text):
    path = os.path.join(dest, rel)
    lines = open(path, encoding="utf-8").read().split("\n")
    lines[lineno - 1] = text
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def edit_labels(dest, site, key, fix=None, append=None):
    path = os.path.join(dest, LABELS_REL)
    rows = open(path, encoding="utf-8").read().split("\n")
    if append is not None:
        if rows and rows[-1] == "":
            rows[-1] = append
            rows.append("")
        else:
            rows.append(append)
    else:
        for i, ln in enumerate(rows):
            c = ln.split("\t")
            if len(c) == 5 and c[0] == site and c[1] == key:
                c[3] = fix
                rows[i] = "\t".join(c)
                break
        else:
            raise SystemExit("label row not found: %s %s" % (site, key))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(rows))


def edit_map(dest, site, key, old, new, append=False):
    path = os.path.join(dest, MAP_REL)
    lines = open(path, encoding="utf-8").read().rstrip("\n").split("\n")
    row = "\t".join((site, key, old, new))
    if append:
        lines.append(row)
    else:
        for i, ln in enumerate(lines):
            c = ln.split("\t")
            if len(c) == 4 and c[0] == site and c[1] == key:
                lines[i] = row
                break
        else:
            raise SystemExit("map row not found: %s %s" % (site, key))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def f1(dest):
    site = TRIAGE + ":356"
    key = "SKILL.md:522"
    base_line = base_text(TRIAGE).split("\n")[355]
    cell = last_cell(base_line)
    forged = ("MATCHES: `SKILL.md:999` (the parking-invisibility sentence; `SKILL.md` does "
              "not enumerate the required keys - the list is `[lost-base] schema.json:6`)")
    set_line(dest, TRIAGE, 356, base_line.replace(cell, forged, 1))
    edit_labels(dest, site, key, fix="Replace cell with: " + forged)
    edit_map(dest, site, key, cell, forged)


def f2(dest):
    site = TRIAGE + ":90"
    key = "SKILL.md:113-114,175-176"
    base_line = base_text(TRIAGE).split("\n")[89]
    old = "`SKILL.md:113-114,175-176` (term omitted)"
    forged = "`SKILL.md:182-184,255-257` (term omitted)"
    set_line(dest, TRIAGE, 90, base_line.replace(old, forged, 1))
    edit_labels(dest, site, key, fix="Replace part: %s => %s" % (old, forged))
    edit_map(dest, site, key, old, forged)


def f3(dest):
    site = TRIAGE + ":356"
    key = "SKILL.md:522"
    base_line = base_text(TRIAGE).split("\n")[355]
    cell = last_cell(base_line)
    forged = ("MATCHES: `SKILL.md:999` (the program-record schema bullet; `SKILL.md` does "
              "not enumerate the required keys - the list is `[lost-base] schema.json:6`) "
              "(`S041.txt`)")
    set_line(dest, TRIAGE, 356, base_line.replace(cell, forged, 1))
    edit_labels(dest, site, key, fix="Replace cell with: " + forged)
    edit_map(dest, site, key, cell, forged)


def f4(dest):
    # triage:143 carries `SKILL.md:251-253`; the same token also stands on
    # triage:151 (in scope), which this row does not touch.
    site = TRIAGE + ":143"
    key = "SKILL.md:251-253"
    base_line = base_text(TRIAGE).split("\n")[142]
    old = "`SKILL.md:251-253`"
    new = "`SKILL.md:335-338`"
    assert old in base_line
    set_line(dest, TRIAGE, 143, base_line.replace(old, new, 1))
    edit_labels(dest, site, key,
                append="\t".join((site, key, "SKILL.md:335-338",
                                  "Repoint: the citation moves to the mirror-gap anchor.",
                                  "forgery")))
    edit_map(dest, site, key, old, new, append=True)


def main():
    for name, fn in (("f1-false-cell", f1), ("f2-premise-standing", f2),
                     ("f3-bare-s041", f3), ("f4-old-elsewhere", f4)):
        build(name, fn)
    return 0


if __name__ == "__main__":
    sys.exit(main())
