#!/usr/bin/env python3
"""Round-46 wave-1 integration: apply the chosen drafts to a target root (a scratch tree for trials, the lane for the real landing).

usage: integrate-wave1.py --root ROOT [--entry A|B|C|D] [--rows A|B] [--contract A|B] [--gates A|B] [--c1] [--c2]
Only text the drafts carry is applied; nothing is invented here. Idempotence is not provided: run once on a fresh tree.
"""
import argparse, os, re, shutil

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
W1 = LANE + "/.ufo/waves/round-46/wave1/"
ap = argparse.ArgumentParser()
ap.add_argument("--root", required=True)
ap.add_argument("--entry", default="B")
ap.add_argument("--rows", default="A")
ap.add_argument("--contract", default="B")
ap.add_argument("--gates", default="A")
ap.add_argument("--c1", action="store_true")
ap.add_argument("--c2", action="store_true")
a = ap.parse_args()
R = os.path.abspath(a.root)


def rd(p): return open(p, encoding="utf-8").read()
def wr(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(t)


def block(text, tag):
    m = re.search(r"<<<BEGIN %s\n(.*?)\n<<<END %s" % (tag, tag), text, re.S)
    assert m, "block %s not found" % tag
    return m.group(1).strip("\n")


def reground(entry, draft):
    p = R + "/corpus/knowledge/%s.md" % entry
    t = rd(p)
    old = re.search(r"^recheck:(.*)$", t, flags=re.M)
    assert old, entry
    new = "recheck: cd %s && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/%s.md" % (LANE, entry)
    t = t[:old.start()] + new + "\nrestoration-recheck:" + old.group(1) + t[old.end():]
    tail = rd(W1 + draft + ".draft/tail.md")
    wr(p, t.rstrip("\n") + "\n" + tail.rstrip("\n") + "\n")


if a.c1:
    reground("claim-package-contract", "R46ScribeGroundContract" + a.contract)
    reground("claim-gates", "R46ScribeGroundGates" + a.gates)

if a.c2:
    for f in ("S073.txt", "manifest.json"):
        d = R + "/corpus/source-snapshots/round-46/" + f
        if not os.path.exists(d):
            wr(d, rd(LANE + "/corpus/source-snapshots/round-46/" + f))
    wr(R + "/corpus/knowledge/github-private-vulnerability-reporting.md",
       rd(W1 + "R46ScribeEntry%s.draft/github-private-vulnerability-reporting.md" % a.entry))
    adm = rd(W1 + "R46ScribeAdmission.draft/appends.md")
    p = R + "/corpus/README.md"
    wr(p, rd(p).rstrip("\n") + "\n\n" + block(adm, "a") + "\n")
    p = R + "/PROVINCE.md"
    if os.path.exists(p):
        wr(p, rd(p).rstrip("\n") + "\n\n" + block(adm, "b") + "\n")
    p = R + "/corpus/instruments/knowledge-expected.txt"
    if os.path.exists(p):
        lines = rd(p).splitlines()
        new = block(adm, "c").strip()
        i = next(k for k, ln in enumerate(lines) if ln.startswith("corpus/knowledge/") and ln > new)
        lines.insert(i, new)
        wr(p, "\n".join(lines) + "\n")
    rows = rd(W1 + "R46ScribeRows%s.draft/rows.md" % a.rows)
    row = next(ln for ln in rows.splitlines() if ln.startswith("| S073 |"))
    p = R + "/corpus/SOURCES.md"
    lines = rd(p).splitlines()
    i = next(k for k, ln in enumerate(lines) if re.match(r"^\|\s*S072\s*\|", ln))
    lines.insert(i + 1, row)
    t = "\n".join(lines) + "\n"

    def bullets(head):
        m = re.search(r"^## %s.*?\n(.*?)(?=^## |\Z)" % re.escape(head), rows, re.S | re.M)
        return [ln for ln in (m.group(1).splitlines() if m else []) if ln.startswith("- ")]
    reg = bullets("2. Registry changes")
    srch = bullets("3. Search log")
    assert reg and srch
    # search-log bullets go at the end of the Search log section (before `## Leads`)
    j = t.index("\n## Leads (unopened)")
    t = t[:j].rstrip("\n") + "\n\n" + "\n".join(srch) + "\n" + t[j:]
    t = t.rstrip("\n") + "\n\n" + "\n".join(reg) + "\n"
    wr(p, t)
print("integrated into", R)
