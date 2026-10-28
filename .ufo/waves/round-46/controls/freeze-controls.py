#!/usr/bin/env python3
"""Round-46 freeze controls: score the frozen counters on the cheapest trees that skip the claimed work.

usage: freeze-controls.py --lane LANE --base BASEREV --work SCRATCH

Every tree is `git archive BASEREV corpus` (+ one mutation). Counters run from LANE's own
corpus/instruments (the tool root), never from a tree. The expected reading of every control
is RED (exit 1); `controls total=N red=R green=G` closes the file and G must be 0.
"""
import argparse, os, re, shutil, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--lane", required=True)
ap.add_argument("--base", required=True)
ap.add_argument("--work", required=True)
a = ap.parse_args()
lane, work = a.lane, os.path.abspath(a.work)
shutil.rmtree(work, ignore_errors=True)
os.makedirs(work)
C1 = os.path.join(lane, "corpus/instruments/r46-c1-gate.py")
C2 = os.path.join(lane, "corpus/instruments/r46-c2-gate.py")
LANECD = "cd " + lane + " && "
out, red, green = [], 0, 0


def export(name):
    d = os.path.join(work, name)
    os.makedirs(d)
    p = subprocess.run("git -C %s archive %s corpus | tar -x -C %s" % (lane, a.base, d), shell=True)
    assert p.returncode == 0
    if name.startswith("c1-"):  # a real tip tree carries the gate; a tree without it would be red for the wrong reason
        shutil.copy(C1, os.path.join(d, "corpus/instruments/r46-c1-gate.py"))
    return d


def rd(p): return open(p, encoding="utf-8").read()
def wr(p, t): open(p, "w", encoding="utf-8").write(t)


def run(label, cmd):
    global red, green
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    tail = [l for l in (p.stdout + p.stderr).strip().splitlines() if l.startswith(("gate ", "c1-gate", "c2-gate"))]
    out.append("== %s" % label)
    out.extend(tail)
    out.append("exit=%d" % p.returncode)
    if p.returncode == 0: green += 1
    else: red += 1


def set_recheck(tree, entry, line):
    p = os.path.join(tree, "corpus/knowledge", entry)
    wr(p, re.sub(r"^recheck:.*$", lambda m: "recheck: " + line, rd(p), flags=re.M))


ENT = ["claim-package-contract.md", "claim-gates.md"]
GATE = LANECD + "python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/%s"
SEC = "\n## Re-ground (round 46)\n\n| id | current claim | committed anchor | token |\n|---|---|---|---|\n"
base = export("base")

# ---- C1 -------------------------------------------------------------------
run("c1 do-nothing (tree = baseline = base export)", [sys.executable, C1, "--root", base, "--baseline", base, "--work", work])

t = export("c1-marker-only")
for e in ENT: set_recheck(t, e, LANECD + "true")
run("c1 marker-only (two recheck lines replaced by `true`)", [sys.executable, C1, "--root", t, "--baseline", base, "--work", work])

t = export("c1-fabricated")
for e in ENT:
    set_recheck(t, e, GATE % e)
    p = os.path.join(t, "corpus/knowledge", e)
    rows = "".join("| G%d | claim %d | `corpus/instruments/claim-package-check.py:%d` | `no-such-token-%d` |\n" % (i, i, 50 + i, i) for i in range(1, 7))
    wr(p, rd(p).rstrip("\n") + "\n" + SEC + rows)
run("c1 fabricated-anchors (gate line + six rows whose tokens are not in the anchored lines)", [sys.executable, C1, "--root", t, "--baseline", base, "--work", work])

t = export("c1-one-file")
for e in ENT:
    set_recheck(t, e, GATE % e)
    p = os.path.join(t, "corpus/knowledge", e)
    rows = "".join("| G%d | claim | `corpus/instruments/claim-package-check.py:51` | `six contract files present` |\n" % i for i in range(1, 7))
    wr(p, rd(p).rstrip("\n") + "\n" + SEC + rows)
run("c1 single-anchor-file (six real rows, all one file)", [sys.executable, C1, "--root", t, "--baseline", base, "--work", work])

t = export("c1-rewritten-body")
for e in ENT:
    set_recheck(t, e, GATE % e)
    p = os.path.join(t, "corpus/knowledge", e)
    rows = ["`corpus/instruments/claim-package-check.py:51` | `six contract files present`",
            "`corpus/instruments/claim-package-check.py:53` | `evidence-manifest/v1`",
            "`corpus/instruments/claim-package-check.py:62` | `NO_SCOPE_OBJECTION`",
            "`corpus/instruments/claim-package-check.py:65` | `policy_sha256 is`",
            "`corpus/instruments/claim-package-check.py:68` | `manifest_sha256 recomputed`",
            "`corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json:2` | `evidence-manifest/v1`"]
    body = "".join("| G%d | c | %s |\n" % (i + 1, r) for i, r in enumerate(rows))
    keep = rd(p).splitlines()
    wr(p, "\n".join(keep[:3] + [l for l in keep if l.startswith("recheck:")]) + "\n" + SEC + body)
run("c1 gutted-entry (valid rows, but the entry's body was deleted to un-gate it)", [sys.executable, C1, "--root", t, "--baseline", base, "--work", work])

# ---- C2 -------------------------------------------------------------------
run("c2 do-nothing (base export)", [sys.executable, C2, "--root", base])


def c2_tree(name, entry_text):
    t = export(name)
    os.makedirs(os.path.join(t, "corpus/source-snapshots/round-46"))
    for f in ("S073.txt", "manifest.json"):
        shutil.copy(os.path.join(lane, "corpus/source-snapshots/round-46", f), os.path.join(t, "corpus/source-snapshots/round-46", f))
    ent = "corpus/knowledge/github-private-vulnerability-reporting.md"
    wr(os.path.join(t, ent), entry_text)
    rp = os.path.join(t, "corpus/README.md")
    wr(rp, rd(rp).rstrip("\n") + "\n\n| F28 | GitHub private vulnerability reporting | admitted | knowledge/github-private-vulnerability-reporting.md | S073 | next |\n")
    sp = os.path.join(t, "corpus/SOURCES.md")
    row = ("| S073 | GitHub private vulnerability reporting — https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately | docs | A | reporter flow | "
           "sha256 66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930 | teaches x | mined | 2026-10-28 | 180d | " + ent + " |")
    s = rd(sp)
    i = s.index("\n## Paths")
    wr(sp, s[:i].rstrip("\n") + "\n" + row + "\n" + s[i:])
    return t


hdr = ("source: S073 — https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately — s\n"
       "verified-at: 2026-10-28\nrecheck: cd " + lane + " && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073\n")
run("c2 junk-row (F28 + S073 rows and a header-only entry)", [sys.executable, C2, "--root", c2_tree("c2-junk", hdr + "\n# stub\n")])
fab = hdr + "\n## Scope and decision rule\n\n\u201cGitHub pays a bounty for every private report\u201d (`S073.txt:560`).\n"
run("c2 fabricated-quote (one curly quote that the capture does not hold)", [sys.executable, C2, "--root", c2_tree("c2-fabricated", fab)])
nocite = hdr + "\n" + "\n".join("## " + h for h in ("Scope and decision rule", "Overlap and novelty", "Limits", "Falsifiable package rule")) + "\n" + "filler " * 600 + "\n"
run("c2 uncited-filler (all four headings, 600 words of filler, no citations)", [sys.executable, C2, "--root", c2_tree("c2-uncited", nocite)])

out.append("controls total=%d red=%d green=%d" % (red + green, red, green))
print("\n".join(out))
shutil.rmtree(work, ignore_errors=True)
sys.exit(0 if green == 0 else 1)
