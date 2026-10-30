#!/usr/bin/env python3
"""R47MutC1b survivor-demonstration driver.

For the three predicted survivors (L9d/L10d/L11d) craft ad-hoc defect trees
from the selftest's kept c1-green tree and show the mutant counter false-greens
what the pristine counter reds. For the caught mutants (L7d/L8e/L9e) record
the limb-line divergence on the selftest's own defect tree.
Runs only on scratch copies; lane repo untouched.
"""
from __future__ import annotations
import os, re, shutil, subprocess, sys, hashlib

S = "/fast/scratch/hyaku/kasegi-r47/R47MutC1b"
GREEN = S + "/work/green-keep/c1-green"
BASE = S + "/exports/base"
INSTR = S + "/exports/freeze/corpus/instruments"
COUNTER = INSTR + "/r47-routed-defects.py"
LOGS = S + "/logs"
ENTRY = "corpus/knowledge/github-repository-security-advisories.md"
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc")

MUTANTS = {
    "L7d-lesson46-dropped": ("for rel in (LESSON47, LESSON46):", "for rel in (LESSON47,):"),
    "L8e-manifest-pin-dropped": ('if not os.path.isfile(man) or sha(open(man, "rb").read()) != MAN_SHA:', "if not os.path.isfile(man):"),
    "L9d-body-bounds-off-by-one": ("rng[0] <= a <= b <= rng[1] and b - a <= 11", "rng[0] - 1 <= a <= b <= rng[1] + 1 and b - a <= 11"),
    "L9e-uncited-masked": ("ok = failed == 0 and uncited <= 0 and passed >= 20", "ok = failed == 0 and passed >= 20"),
    "L10d-lead-anywhere": ('leads = section(raw, "Leads (unopened)")', "leads = raw"),
    "L11d-precision-phrase-wide": ('b = "S068" in t and "one GHSA advisory entry" in t', 'b = "S068" in t and "GHSA advisory" in t'),
}


def mutant_counter(mid: str) -> str:
    src = open(COUNTER, encoding="utf-8").read()
    old, new = MUTANTS[mid]
    assert src.count(old) == 1, (mid, src.count(old))
    inst = S + "/work/tinst-" + mid
    shutil.rmtree(inst, ignore_errors=True)
    shutil.copytree(INSTR, inst, symlinks=True, ignore=IGNORE)
    dst = inst + "/r47-routed-defects.py"
    open(dst, "w", encoding="utf-8").write(src.replace(old, new, 1))
    return dst


def counter_on(counter_path: str, tree: str, tag: str) -> str:
    p = subprocess.run([sys.executable, "-I", counter_path, "--root", tree, "--baseline", BASE],
                       capture_output=True, text=True, timeout=600, cwd=S)
    open(LOGS + "/" + tag + ".txt", "w").write(p.stdout + p.stderr)
    return p.stdout


def tree_copy(name: str) -> str:
    t = S + "/work/tree-" + name
    shutil.rmtree(t, ignore_errors=True)
    shutil.copytree(GREEN, t, symlinks=True)
    return t


out = []

# 1. survivor demonstrations: pristine red vs mutant green on crafted trees
# T-L9d: cited span one line BEFORE body_lines lo=558 (snap line 557 = "Repository security advisories")
t = tree_copy("T-L9d-lowbound")
p = os.path.join(t, ENTRY)
s = open(p, encoding="utf-8").read()
s = s.rstrip("\n") + "\nBoundary probe: \u201cRepository security advisories\u201d (`S076.txt:557`).\n"
open(p, "w", encoding="utf-8").write(s)
out.append(("T-L9d-lowbound pristine", counter_on(COUNTER, t, "t-T-L9d-lowbound-pristine")))
out.append(("T-L9d-lowbound mutant", counter_on(mutant_counter("L9d-body-bounds-off-by-one"), t, "t-T-L9d-lowbound-mutant")))

# T-L9d2: cited span one line AFTER body_lines hi=600 (snap line 601 = "Back to top")
t = tree_copy("T-L9d-hibound")
p = os.path.join(t, ENTRY)
s = open(p, encoding="utf-8").read()
s = s.rstrip("\n") + "\nBoundary probe: \u201cBack to top\u201d (`S076.txt:601`).\n"
open(p, "w", encoding="utf-8").write(s)
out.append(("T-L9d-hibound pristine", counter_on(COUNTER, t, "t-T-L9d-hibound-pristine")))
out.append(("T-L9d-hibound mutant", counter_on(mutant_counter("L9d-body-bounds-off-by-one"), t, "t-T-L9d-hibound-mutant")))

# T-L10d: the exact lead bullet displaced into ## Search log
t = tree_copy("T-L10d-displaced")
p = os.path.join(t, "corpus/SOURCES.md")
s = open(p, encoding="utf-8").read()
m = re.search(r"^- GitHub repository security advisories REST API.*\n", s, re.M)
assert m, "lead bullet not found in green SOURCES"
bullet = m.group(0)
s = s.replace(bullet, "", 1)
s = re.sub(r"(?=^## Leads \(unopened\)$)", bullet, s, flags=re.M)
open(p, "w", encoding="utf-8").write(s)
out.append(("T-L10d-displaced pristine", counter_on(COUNTER, t, "t-T-L10d-pristine")))
out.append(("T-L10d-displaced mutant", counter_on(mutant_counter("L10d-lead-anywhere"), t, "t-T-L10d-mutant")))

# T-L11d: imprecise S068 wording kept precise-looking
t = tree_copy("T-L11d-imprecise")
p = os.path.join(t, "corpus/lessons/round-47.md")
s = open(p, encoding="utf-8").read()
assert "one GHSA advisory entry" in s
s = s.replace("one GHSA advisory entry", "the GHSA advisory row class", 1)
open(p, "w", encoding="utf-8").write(s)
out.append(("T-L11d-imprecise pristine", counter_on(COUNTER, t, "t-T-L11d-pristine")))
out.append(("T-L11d-imprecise mutant", counter_on(mutant_counter("L11d-precision-phrase-wide"), t, "t-T-L11d-mutant")))

# 2. caught mutants: limb-line divergence on the selftest's own defect trees
PAIRS = [("L7d-lesson46-dropped", "c1-nolesson47"),
         ("L8e-manifest-pin-dropped", "c1-maninert"),
         ("L9e-uncited-masked", "c1-nocite")]
for mid, case in PAIRS:
    tree = S + "/work/green-keep/" + case
    out.append(("%s on %s pristine" % (mid, case), counter_on(COUNTER, tree, "div-%s-pristine" % case)))
    out.append(("%s on %s mutant" % (mid, case), counter_on(mutant_counter(mid), tree, "div-%s-mutant" % mid)))

for tag, text in out:
    print("== %s ==" % tag)
    lines = text.strip().splitlines()
    print("\n".join(lines[-2:]) if lines else "(no output)")
