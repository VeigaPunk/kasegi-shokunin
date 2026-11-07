#!/usr/bin/env python3
"""Build fixture fx8: labels A+B name edits, only A is mapped and the excluded
pair B (site 58 / key SKILL.md:117) must stay unmapped. Used to show the M12
defect: with a real EXCLUDED entry the correct counter accepts the tranche and
the M12 mutant rejects it (want includes the excluded pair -> unapplied).

Run from the scratch root after art/mkfixtures.py has created fx/build/lane.
"""
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r93/MutC1Counter"
BUILD = os.path.join(S, "fx/build/lane")
BASE = "e15996bfd2f6eca4af39507a7c5973afbeca8347"
TF = "corpus/knowledge/triage-thresholds.md"
LAB = ".ufo/waves/round-93/c1/labels.tsv"


def git(*a):
    p = subprocess.run(["git", "-C", BUILD] + list(a), capture_output=True, text=True)
    if p.returncode:
        raise SystemExit("git %s: %s" % (a, p.stderr))
    return p.stdout


assert git("rev-parse", "--show-toplevel").strip() == BUILD
git("checkout", "-q", "-f", "-B", "fx8-excl-unmapped", BASE)
lines = open(os.path.join(BUILD, TF), encoding="utf-8").read().split("\n")
i = 453
assert lines[i].count("`SKILL.md:494-506`") == 1
lines[i] = lines[i].replace("`SKILL.md:494-506`", "`SKILL.md:191`", 1)
open(os.path.join(BUILD, TF), "w", encoding="utf-8").write("\n".join(lines))
os.makedirs(os.path.join(BUILD, os.path.dirname(LAB)), exist_ok=True)
rows = [["line", "key", "label", "fix", "evidence"],
        ["corpus/knowledge/triage-thresholds.md:454", "SKILL.md:494-506", "SKILL.md:191", "probe A", "probe"],
        ["corpus/knowledge/triage-thresholds.md:58", "SKILL.md:117", "SKILL.md:191", "probe B (excluded, unmapped)", "probe"]]
open(os.path.join(BUILD, LAB), "w", encoding="utf-8").write("\n".join("\t".join(r) for r in rows) + "\n")
mp = os.path.join(S, "art/maps/fx8-excl-unmapped.tsv")
open(mp, "w", encoding="utf-8").write(
    "corpus/knowledge/triage-thresholds.md:454\tSKILL.md:494-506\t`SKILL.md:494-506`\t`SKILL.md:191`\n")
git("add", "-A")
git("-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-q", "-m", "fixture fx8")
rev = git("rev-parse", "HEAD").strip()
out = subprocess.run([sys.executable, "-B", os.path.join(S, "art/knowledge-meter.py"), "--lane", BUILD,
                      "--measure-rev", rev, "--work", os.path.join(S, "work/measure")],
                     capture_output=True, text=True).stdout
rate = [w for w in out.split() if w.startswith("rate=")][0].split("=")[1]
with open(os.path.join(S, "art/fixtures.tsv"), "a", encoding="utf-8") as fh:
    fh.write("fx8-excl-unmapped\t%s\t%s\t%s\t1007/2001\t%s\n" % (rev, mp, rev, rate))
print("fx8 rev", rev, "target", rate)
