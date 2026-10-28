#!/usr/bin/env python3
"""L1 integration of wave-1 drafts into the lane (append-only except the S071/S072 rows, which are inserted
after the S070 registry row). Run once from the lane root. Prints what it wrote."""
import re, os

L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
W = L + "/.ufo/waves/round-45/wave1"


def rd(p):
    return open(p, encoding="utf-8").read()


def app(path, text):
    s = rd(path)
    with open(path, "a", encoding="utf-8") as fh:
        if not s.endswith("\n"):
            fh.write("\n")
        fh.write(text)


# --- SOURCES rows -----------------------------------------------------------
a = rd(W + "/R45ScribeRowsA.draft/rows.md")
s071 = [ln for ln in a.splitlines() if ln.startswith("| S071 |")][0]
s072 = ("| S072 | Google Bug Hunters Rules directory, readable article-API capture — https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section | docs | B | "
        "Google's overview of which VRP program covers which product family and where each report goes; a secondary routing summary, not the operative rules of any program | "
        "section headings Android & Friends L17, Chrome & Friends L57, Google & Friends L107, Open Source L171, Other L249 and Cloud VRP scope line L148-L149 in capture corpus/source-snapshots/round-45/S072.txt "
        "(sha256 364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025, 10032 bytes, 312 lines); raw article JSON .ufo/waves/round-45/source-recon/S072.json (body 10029 characters); fetched 2026-10-28T20:53:00Z | "
        "supersedes S070 — REJECTED: the body is readable through the article API (10029 characters), so S070's no-body reason is corrected; it is a program, scope and where-to-report overview table whose Cloud VRP line (L148-L149) restates S069 Q5, "
        "so it adds no operative rule and needs no knowledge entry; flip: a fresh article-API capture states a program-specific scope or boundary rule that the program's linked rules page does not state | rejected | 2026-10-28 | 180d | — |")
for r in (s071, s072):
    assert len([c for c in r.strip().strip("|").split("|")]) == 11, r[:40]
path = L + "/corpus/SOURCES.md"
lines = rd(path).split("\n")
i = [k for k, ln in enumerate(lines) if re.match(r"^\| S070 \|", ln)][0]
lines[i + 1:i + 1] = [s071, s072]
open(path, "w", encoding="utf-8").write("\n".join(lines))
print("SOURCES rows inserted after line", i + 1)

# --- appended blocks from ScribeCorrections ---------------------------------
ap = rd(W + "/R45ScribeCorrections.draft/appends.md")


def block(name):
    m = re.search(r"=== BLOCK %s:[^\n]*===\n(.*?)\n=== END BLOCK %s ===" % (name, name), ap, re.S)
    return m.group(1).strip("\n")


app(L + "/corpus/lessons/round-44.md", "\n" + block("A") + "\n")
app(L + "/corpus/README.md", "\n" + block("B") + "\n")
app(L + "/PROVINCE.md", "\n" + block("C") + "\n")

# --- QUALITY ----------------------------------------------------------------
q = rd(W + "/R45ScribeQuality.draft/quality-append.md")
app(L + "/corpus/QUALITY.md", q if q.startswith("\n") else "\n" + q)
print("done")
