import hashlib
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r93/CriticClaimsC1"
SRC = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
FORGE = os.path.join(S, "forge")
WORK = os.path.join(S, "forge-work")
OUT = os.path.join(S, "forgeries")
BASE = "e15996bfd2f6eca4af39507a7c5973afbeca8347"
LANDING = "ae53b3c6e7e2ce070c2f022d01c1677a8908df1b"
FREEZE = "5bad9e55d3d9319446e3d9b63bc2dece633cdb68"
MAP = os.path.join(S, "repair-map.frozen.tsv")
METRE = ".ufo/waves/round-93/c1/knowledge-meter.py"
LABELS = ".ufo/waves/round-93/c1/labels.tsv"


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def git(repo, *args, check=True):
    p = sh(["git", "-C", repo] + list(args))
    if check and p.returncode != 0:
        raise SystemExit("git %r failed: %s" % (args, p.stderr))
    return p.stdout.strip()


def commit(repo, msg):
    git(repo, "add", "-A")
    p = sh(["git", "-C", repo, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
            "commit", "-q", "-m", msg])
    if p.returncode != 0:
        raise SystemExit("commit failed: " + p.stderr)
    return git(repo, "rev-parse", "HEAD")


def run(name, after, map_path, labels_rev, map_sha=None):
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    cmd = [sys.executable, "-B", os.path.join(FORGE, METRE), "--lane", FORGE,
           "--base-rev", BASE, "--after-rev", after, "--map", map_path,
           "--labels-rev", labels_rev, "--base-target", "1007/2001",
           "--target", "1009/2000", "--work", WORK]
    if map_sha:
        cmd += ["--map-sha256", map_sha]
    p = sh(cmd)
    path = os.path.join(OUT, name + ".out")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("CMD " + " ".join(cmd) + "\n")
        fh.write("RC %d\n" % p.returncode)
        fh.write("--STDOUT--\n" + p.stdout)
        fh.write("--STDERR--\n" + p.stderr)
    print("=== %s rc=%d ===" % (name, p.returncode))
    for line in p.stdout.splitlines():
        if line.startswith(("LIMB ", "KNOWLEDGE-METER-RESULT")):
            print("  " + line)
    if p.stderr.strip():
        print("  STDERR-TAIL:", p.stderr.strip().splitlines()[-1])


shutil.rmtree(FORGE, ignore_errors=True)
shutil.rmtree(WORK, ignore_errors=True)
shutil.rmtree(OUT, ignore_errors=True)
p = sh(["git", "clone", "-q", "--shared", SRC, FORGE])
assert p.returncode == 0, p.stderr
top = git(FORGE, "rev-parse", "--show-toplevel")
assert os.path.realpath(top) == os.path.realpath(FORGE), (top, FORGE)
git(FORGE, "checkout", "-q", LANDING)
assert git(FORGE, "rev-parse", "HEAD") == LANDING
assert git(FORGE, "status", "--porcelain") == ""
map_sha = hashlib.sha256(open(MAP, "rb").read()).hexdigest()

tri = os.path.join(FORGE, "corpus/knowledge/triage-thresholds.md")
cit = os.path.join(FORGE, "corpus/knowledge/citation-bases.md")
score = os.path.join(FORGE, "SCORECARD.md")
labf = os.path.join(FORGE, LABELS)


def lines(path):
    return open(path, encoding="utf-8").read().split("\n")


def save(path, ls):
    open(path, "w", encoding="utf-8").write("\n".join(ls))


# F1: unlabelled in-scope edit (same line, no token added).
git(FORGE, "checkout", "-q", "-B", "f1", LANDING)
cl = lines(cit)
cl[19] = cl[19] + " (forged)"
save(cit, cl)
f1 = commit(FORGE, "f1 unlabelled in-scope edit")
run("F1-unlabelled-in-scope", f1, MAP, FREEZE, map_sha)

# F2: out-of-scope edit.
git(FORGE, "checkout", "-q", "-B", "f2", LANDING)
sl = lines(score)
sl.append("forged out-of-scope line")
save(score, sl)
f2 = commit(FORGE, "f2 out-of-scope edit")
run("F2-out-of-scope", f2, MAP, FREEZE, map_sha)
print("F2 diff-tree names:", sh(["git", "-C", FORGE, "diff-tree", "--no-commit-id",
                                 "--name-only", "-r", f2]).stdout.split())

# F3: map `new` differs from the label (label says SKILL.md:191, map says SKILL.md:526),
# after tree carries the map's value at line 58; M1/M3/M4/M5 held.
git(FORGE, "checkout", "-q", "-B", "f3", LANDING)
tl = lines(tri)
assert tl[57].count("`SKILL.md:191`") == 1, tl[57]
tl[57] = tl[57].replace("`SKILL.md:191`", "`SKILL.md:526`")
save(tri, tl)
f3 = commit(FORGE, "f3 map new differs from label")
m3 = os.path.join(OUT, "map-F3.tsv")
rows = [r for r in open(MAP, encoding="utf-8").read().rstrip("\n").split("\n") if r]
newrows = []
for r in rows:
    c = r.split("\t")
    if c[0] == "corpus/knowledge/triage-thresholds.md:58":
        c[3] = "`SKILL.md:526`"
    newrows.append("\t".join(c))
open(m3, "w", encoding="utf-8").write("\n".join(newrows) + "\n")
run("F3-map-new-differs-from-label", f3, m3, FREEZE, None)

# F4: label whose anchor is out of range (SKILL.md has 1251 lines).
git(FORGE, "checkout", "-q", "-B", "flab", LANDING)
ll = lines(labf)
hit = [i for i, l in enumerate(ll) if l.startswith("corpus/knowledge/triage-thresholds.md:144\t")]
assert len(hit) == 1, hit
c = ll[hit[0]].split("\t")
assert c[2] == "SKILL.md:191", c
c[2] = "SKILL.md:5000-5001"
ll[hit[0]] = "\t".join(c)
save(labf, ll)
flab = commit(FORGE, "f4 labels out-of-range anchor")
git(FORGE, "checkout", "-q", "-B", "f4", flab)
tl = lines(tri)
assert tl[143].count("`SKILL.md:191`") == 1, tl[143]
tl[143] = tl[143].replace("`SKILL.md:191`", "`SKILL.md:5000-5001`")
save(tri, tl)
f4 = commit(FORGE, "f4 out-of-range anchor write")
m4 = os.path.join(OUT, "map-F4.tsv")
newrows = []
for r in rows:
    c = r.split("\t")
    if c[0] == "corpus/knowledge/triage-thresholds.md:144":
        c[3] = "`SKILL.md:5000-5001`"
    newrows.append("\t".join(c))
open(m4, "w", encoding="utf-8").write("\n".join(newrows) + "\n")
run("F4-label-anchor-out-of-range", f4, m4, flab, None)
print("F4 SKILL.md line count:", len(lines(os.path.join(FORGE, "SKILL.md"))))

# F5: a label that names a non-knowledge citing file, with NO edit to it.
# This is the exact labelled-file-scope case the successor counter adds.
git(FORGE, "checkout", "-q", "-B", "f5", LANDING)
ll = lines(labf)
ll.append("SKILL.md:191\tSKILL.md:191\tCORRECT\tNo edit: control fixture for the M3 labelled-file scope.\tcontrol")
save(labf, ll)
f5 = commit(FORGE, "f5 added non-knowledge no-edit label")
run("F5-labelled-nonknowledge-noedit", f5, MAP, f5, map_sha)
