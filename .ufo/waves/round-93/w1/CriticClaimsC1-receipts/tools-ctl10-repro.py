import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r93/CriticClaimsC1"
CAND = os.path.join(S, "cand")
DEST = os.path.join(S, "ctl10")
LANE = os.path.join(DEST, "lane")
WORK = os.path.join(S, "ctl10-work")
BASE = "e15996bfd2f6eca4af39507a7c5973afbeca8347"
CAND_REV = "ae53b3c6e7e2ce070c2f022d01c1677a8908df1b"


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


shutil.rmtree(DEST, ignore_errors=True)
shutil.rmtree(WORK, ignore_errors=True)
os.makedirs(WORK, exist_ok=True)
p = sh(["git", "clone", "-q", "--shared", CAND, LANE])
assert p.returncode == 0, p.stderr
top = sh(["git", "-C", LANE, "rev-parse", "--show-toplevel"]).stdout.strip()
assert os.path.realpath(top) == os.path.realpath(LANE), (top, LANE)
assert sh(["git", "-C", LANE, "rev-parse", "HEAD"]).stdout.strip() == CAND_REV

sk_path = os.path.join(LANE, "SKILL.md")
sk = open(sk_path, encoding="utf-8").read().split("\n")
sk[190] = sk[190] + " (control edit)"
open(sk_path, "w", encoding="utf-8").write("\n".join(sk))

lab_path = os.path.join(LANE, ".ufo/waves/round-93/c1/labels.tsv")
lab = open(lab_path, encoding="utf-8").read().rstrip("\n").split("\n")
lab.append("SKILL.md:191\tSKILL.md:191\tCORRECT\tNo edit: control fixture for the M3 labelled-file scope.\tcontrol")
open(lab_path, "w", encoding="utf-8").write("\n".join(lab) + "\n")
shutil.copy(os.path.join(S, "repair-map.frozen.tsv"),
            os.path.join(LANE, ".ufo/waves/round-93/c1/repair-map.tsv"))

sh(["git", "-C", LANE, "add", "-A"])
p = sh(["git", "-C", LANE, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
        "commit", "-q", "-m", "scope control"])
assert p.returncode == 0, p.stderr
rev = sh(["git", "-C", LANE, "rev-parse", "HEAD"]).stdout.strip()
print("SCOPE_REV", rev)

cmd = [sys.executable, "-B", os.path.join(LANE, ".ufo/waves/round-93/c1/knowledge-meter.py"),
       "--lane", LANE, "--base-rev", BASE, "--after-rev", rev,
       "--map", os.path.join(LANE, ".ufo/waves/round-93/c1/repair-map.tsv"),
       "--labels-rev", rev, "--base-target", "1007/2001", "--target", "1009/2000",
       "--work", WORK]
p = sh(cmd)
print("RC", p.returncode)
print("--- STDOUT ---")
print(p.stdout)
print("--- STDERR ---")
print(p.stderr)
