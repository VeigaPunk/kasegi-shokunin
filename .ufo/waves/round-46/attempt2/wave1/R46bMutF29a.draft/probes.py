#!/usr/bin/env python3
"""Counterexample probes P1..P5 against the R50 receipt's NOT-SHOWN disclosures."""
import importlib.util, os, re, shutil, subprocess, sys

S = "/fast/scratch/hyaku/kasegi-r46/R46bMutF29a"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
CTRL = os.path.join(LANE, ".ufo/waves/round-46/attempt2/controls")
GATE = os.path.join(LANE, "corpus/instruments/r46-f29-gate.py")
spec = importlib.util.spec_from_file_location("f29fix", os.path.join(CTRL, "f29-fixture.py"))
fx = importlib.util.module_from_spec(spec); spec.loader.exec_module(fx)
ENTRY, URL, LANE_CD = fx.ENTRY, fx.URL, fx.LANE_CD
TREES, INST = os.path.join(S, "trees"), os.path.join(S, "inst")
env = dict(os.environ, TMPDIR=os.path.join(S, "tmp"))

def fresh(name):
    d = os.path.join(TREES, name)
    if os.path.isdir(d): shutil.rmtree(d)
    shutil.copytree(os.path.join(TREES, "positive"), d, symlinks=True)
    return d

def run(gate, tree):
    p = subprocess.run([sys.executable, "-B", gate, "--root", tree],
                       capture_output=True, text=True, env=env, timeout=300)
    limbs = {}
    for m in re.finditer(r"^gate (H\d) pass=(\d) read=(.*)$", p.stdout, re.M):
        limbs[m.group(1)] = (int(m.group(2)), m.group(3))
    fixed = re.findall(r"f29-gate fixed=(\d+)/7", p.stdout)
    return limbs, (fixed[0] if fixed else "?")

def report(title, tree, mid, limb):
    b, fb = run(GATE, tree); m, fm = run(os.path.join(INST, mid, "corpus/instruments/r46-f29-gate.py"), tree)
    print("### %s" % title)
    print("  BASE   %s pass=%d read=%s   [fixed=%s/7]" % (limb, b[limb][0], b[limb][1], fb))
    print("  MUTANT %s pass=%d read=%s   [fixed=%s/7]" % (limb, m[limb][0], m[limb][1], fm))
    print("  => %s\n" % ("FLIP: the mutant IS isolated at gate level by this tree"
                         if (b[limb][0]==0 and m[limb][0]==1)
                         else "no-flip (limb %d->%d)" % (b[limb][0], m[limb][0])))

# ---------------- P1: disclosure (a), H1a -- extra DISTINCT admitted row
d = fresh("probe-p1")
lines = open(os.path.join(d, "corpus/README.md"), encoding="utf-8").read().splitlines(keepends=True)
for i, ln in enumerate(lines):
    if ln.startswith("| F29 |"):
        lines.insert(i+1, "| F30 | An extra distinct admitted row | admitted | corpus/knowledge/program-quirks.md | S001 | probe |\n"); break
open(os.path.join(d, "corpus/README.md"), "w", encoding="utf-8").write("".join(lines))
report("P1 disclosure (a)/H1a: extra DISTINCT admitted row F30 (trips counts, not dup, not entry-shared)",
       d, "H1a-counts-loose", "H1")

# ---------------- P2: disclosure (b), H2b -- gut a section AND move its table to another section
d = fresh("probe-p2")
head, rest = ENTRY.split("## Scope and decision rule\n", 1)
prose, tail = rest.split("\n\n| id |", 1)
table, after = ("| id |" + tail).split("\n\n## Overlap and novelty", 1)
overlap, limits_fals = after.split("\n\n## Limits", 1)
limits, fals = limits_fals.split("\n\n## Falsifiable package rule", 1)
newbody = (head
  + "## Scope and decision rule\n\nScope: maintainer lifecycle only (S074.txt:38).\n\n"
  + "## Overlap and novelty\n\n" + overlap.strip() + "\n\n" + table.strip() + "\n\n"
  + "## Limits\n\n" + limits.strip() + "\n\n"
  + "## Falsifiable package rule\n\n" + fals.strip() + "\n")
open(os.path.join(d, "corpus/knowledge/github-repository-security-advisories.md"), "w", encoding="utf-8").write(newbody.format(url=URL, lane=LANE_CD))
print("P2 entry bytes=%d" % os.path.getsize(os.path.join(d, "corpus/knowledge/github-repository-security-advisories.md")))
report("P2 disclosure (b)/H2b: Scope gutted to 7 words, its 6-row table relocated under Overlap",
       d, "H2b-wordfloor-low", "H2")

# ---------------- P3: disclosure (c), H3a -- S074 row with 12 cells (extra cell at the END)
d = fresh("probe-p3")
p = os.path.join(d, "corpus/SOURCES.md")
lines = open(p, encoding="utf-8").read().splitlines(keepends=True)
for i, ln in enumerate(lines):
    if ln.startswith("| S074 |"):
        c = ln.strip().strip("|").split("|"); c.append(" extra-cell "); lines[i] = "|" + "|".join(c) + "|\n"; break
open(p, "w", encoding="utf-8").write("".join(lines))
report("P3 disclosure (c)/H3a: S074 registry row carries a 12th cell (extra cell appended)",
       d, "H3a-cells-loose", "H3")

# ---------------- P4: disclosure (d), H4b/H4c -- keep manifest bytes pinned, shrink the SNAPSHOT
d = fresh("probe-p4")
p = os.path.join(d, "corpus/source-snapshots/round-46-a2/S074.txt")
snap = open(p, encoding="utf-8").read().splitlines(keepends=True)
# drop the lines holding 4 of the 9 manifest quotes -> recheck reports fewer OK quotes
open(p, "w", encoding="utf-8").write("".join(snap[:8] + snap[14:]))
report("P4 disclosure (d)/H4b: manifest bytes UNPINNED-VALID but snapshot shortened (fewer quotes verify)",
       d, "H4b-quotes-low", "H4")

# ---------------- P5: disclosure (e), H5c -- 6-row table but only 3 located spans
d = fresh("probe-p5")
p = os.path.join(d, "corpus/knowledge/github-repository-security-advisories.md")
t = open(p, encoding="utf-8").read()
# drop G4,G5,G6 table rows -> 3 rows left (table-rows<6 -> H2 red, but we test H5)
for g in ("G4", "G5", "G6"):
    t = "\n".join(l for l in t.splitlines() if not l.startswith("| %s |" % g)) + "\n"
open(p, "w", encoding="utf-8").write(t)
report("P5 disclosure (e)/H5c: 3 located spans, 6-row table kept elsewhere",
       d, "H5c-pass-low", "H5")
