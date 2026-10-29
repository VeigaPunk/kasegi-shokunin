#!/usr/bin/env python3
"""R46bRevF29H1 — H1 false-green attack matrix on r46-f29-gate.py.

Each tree = positive fixture + ONE README mutation (H1's only input).
For every tree we run the real gate and record the exact H1 line.
"""
import os, shutil, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
FIXTURE = os.path.join(LANE, ".ufo/waves/round-46/attempt2/controls/f29-fixture.py")
GATE = os.path.join(LANE, "corpus/instruments/r46-f29-gate.py")
SCRATCH = "/fast/scratch/hyaku/kasegi-r46/R46bRevF29H1"

F29ROW = ("| F29 | GitHub repository security advisories — the maintainer-side advisory lifecycle "
          "(draft, private fork, CVE via GitHub as CNA, credit, publication, fix version) | admitted | "
          "corpus/knowledge/github-repository-security-advisories.md | S074 | Keep the maintainer flow "
          "distinct from the reporter flow (F28); re-open the page before relying on its mechanics. |")
ENTRY = "corpus/knowledge/github-repository-security-advisories.md"

def base_rows(readme):
    return [ln for ln in readme.splitlines() if ln.startswith("| F") and ln.split("|")[1].strip().startswith("F")]

def build(tag, mutate):
    d = os.path.join(SCRATCH, tag)
    if os.path.isdir(d):
        shutil.rmtree(d)
    subprocess.run([sys.executable, FIXTURE, "--mode", "positive", "--dir", d], check=True)
    rp = os.path.join(d, "corpus/README.md")
    readme = open(rp, encoding="utf-8").read()
    open(rp, "w", encoding="utf-8").write(mutate(readme))
    p = subprocess.run([sys.executable, GATE, "--root", d], capture_output=True, text=True)
    h1 = [ln for ln in p.stdout.splitlines() if ln.startswith("gate H1 ")]
    fixed = [ln for ln in p.stdout.splitlines() if ln.startswith("f29-gate ")]
    print("=== %s ===" % tag)
    print((h1 or ["gate H1 <no line>"])[0])
    print((fixed or ["f29-gate <no line>"])[0])
    return h1[0] if h1 else ""

def naive_dup(readme):
    return readme + "\n" + F29ROW + "\n"

def indented_block(readme):
    rows = base_rows(readme)
    block = "\n".join(" " + r for r in rows)  # one leading space per row
    return readme + "\n### Amendment 2026-10-29 — re-affirmed frontier\n\n" + block + "\n"

def id_collision_space(readme):
    ghost = ("| F2 9 | ghost duplicate of the F29 frontier row | admitted | "
             "corpus/knowledge/ghost-holder.md | S074 | collision probe |")
    return readme + "\n" + ghost + "\n"

def unicode_digits(readme):
    ghost = ("| F２９ | ghost duplicate of the F29 frontier row | admitted | "
             "corpus/knowledge/ghost-holder.md | S074 | collision probe |")
    return readme + "\n" + ghost + "\n"

def alias_entry_cell(readme):
    old = "| " + ENTRY + " | S074 |"
    new = "| " + ENTRY + " (mirror entry: corpus/knowledge/github-private-vulnerability-reporting.md) | S074 |"
    assert old in readme
    return readme.replace(old, new, 1)

def comment_oneline(readme):
    return readme + "\n<!-- | F29 | ghost row smuggled inside a one-line HTML comment | admitted | corpus/knowledge/ghost.md | S074 | -->\n"

def comment_multiline(readme):
    return readme + "\n<!--\n| F29 | ghost row inside a multiline HTML comment | admitted | corpus/knowledge/ghost.md | S074 |\n-->\n"

def lowercase_id(readme):
    ghost = ("| f29 | ghost duplicate of the F29 frontier row | admitted | "
             "corpus/knowledge/ghost-holder.md | S074 | collision probe |")
    return readme + "\n" + ghost + "\n"

def zwsp_id(readme):
    ghost = ("| F29\u200b | ghost duplicate of the F29 frontier row, zero-width space inside the id cell | admitted | "
             "corpus/knowledge/ghost-holder.md | S074 | collision probe |")
    return readme + "\n" + ghost + "\n"

CASES = [
    ("a1-naive-dup-control", naive_dup),
    ("a2-indented-dup-block", indented_block),
    ("a3-id-collision-f2-space-9", id_collision_space),
    ("a4-unicode-digits-control", unicode_digits),
    ("a5-entry-cell-aliasing", alias_entry_cell),
    ("a6-comment-oneline-f29", comment_oneline),
    ("a7-comment-multiline-control", comment_multiline),
    ("a8-lowercase-id", lowercase_id),
    ("a9-zwsp-id", zwsp_id),
]

for tag, fn in CASES:
    build(tag, fn)
