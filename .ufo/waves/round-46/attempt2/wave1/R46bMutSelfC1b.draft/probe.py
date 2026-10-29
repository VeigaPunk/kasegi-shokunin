#!/usr/bin/env python3
"""R46bMutSelfC1b — differential probe harness (independent of the committed selftest).

For every mutant the committed selftest does NOT catch, construct a concrete input where
the MUTATED clause changes the counter's verdict, and show that the pristine counter and
the mutant counter disagree on it.  A survivor WITH such a witness is a COVERAGE FINDING
(the selftest cannot see the change); a survivor with no witness is reported as
behaviourally equivalent at the probed surface.

Two probe surfaces:
  * entry mode   : `<counter> --entry corpus/knowledge/probe.md --root TREE`
  * aggregate    : `<counter> --root TREE --baseline BASE`  (exercises classify())
The lane tree is only read; every probe tree is created under --work.
"""
from __future__ import annotations

import argparse
import difflib
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
SECTION = "## Re-ground (round 46)"


def wr(p: str, s: str) -> None:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(s)


def run(counter: str, args, env=None) -> str:
    p = subprocess.run([sys.executable, "-I", counter] + args, capture_output=True, text=True,
                       timeout=600, env=env or os.environ.copy())
    return p.stdout


def diff_lines(a: str, b: str) -> list:
    return [ln for ln in difflib.unified_diff(a.splitlines(), b.splitlines(),
                                              fromfile="pristine", tofile="mutant",
                                              lineterm="", n=0) if ln.startswith(("+", "-", "@"))]


def section_of(rows) -> str:
    out = ["", SECTION, "", "| id | current claim | committed anchor | token |", "|---|---|---|---|"]
    for gid, claim, anchor, tok in rows:
        out.append("| %s | %s | `%s` | `%s` |" % (gid, claim, anchor, tok))
    return "\n".join(out) + "\n"


# six valid rows over two distinct anchor files, two distinct digests, distinct tokens
BASE_FILES = {
    "corpus/instruments/a.py": "AAA_TOKEN_ONE\nAAA_TOKEN_TWO\nAAA_TOKEN_THREE\n",
    "corpus/instruments/b.py": "BBB_TOKEN_FOUR\nBBB_TOKEN_FIVE\nBBB_TOKEN_SIX\n",
}
BASE_ROWS = [("G1", "c1", "corpus/instruments/a.py:1", "AAA_TOKEN_ONE"),
             ("G2", "c2", "corpus/instruments/a.py:2", "AAA_TOKEN_TWO"),
             ("G3", "c3", "corpus/instruments/a.py:3", "AAA_TOKEN_THREE"),
             ("G4", "c4", "corpus/instruments/b.py:1", "BBB_TOKEN_FOUR"),
             ("G5", "c5", "corpus/instruments/b.py:2", "BBB_TOKEN_FIVE"),
             ("G6", "c6", "corpus/instruments/b.py:3", "BBB_TOKEN_SIX")]


def entry_probe(work, pristine, mutant, name, rows, files, label):
    """Build a tree with the given rows/files and diff the two counters' entry mode."""
    root = os.path.join(work, name)
    shutil.rmtree(root, ignore_errors=True)
    for rel, content in files.items():
        wr(os.path.join(root, rel), content)
    wr(os.path.join(root, "corpus/knowledge/probe.md"), "# probe\n" + section_of(rows))
    a = run(pristine, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    b = run(mutant, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    if a == b:
        print("PROBE %-44s no-difference (equivalent at this surface)" % label)
        return False
    print("PROBE %-44s DIFFERENT" % label)
    for ln in diff_lines(a, b):
        print("   " + ln)
    return True


def aggregate_probe(work, pristine, mutant, name, entries, label, home=None):
    """Build TREE + BASE (a copy of TREE) and diff the two counters' aggregate mode."""
    root = os.path.join(work, name)
    shutil.rmtree(root, ignore_errors=True)
    for rel, content in entries.items():
        wr(os.path.join(root, rel), content)
    base = os.path.join(work, name + "-base")
    shutil.rmtree(base, ignore_errors=True)
    shutil.copytree(root, base, symlinks=True)
    env = dict(os.environ, HOME=home) if home else os.environ.copy()
    args = ["--root", root, "--baseline", base, "--work", os.path.join(work, name + "-w")]
    a = run(pristine, args, env)
    b = run(mutant, args, env)
    if a == b:
        print("PROBE %-44s no-difference (equivalent at this surface)" % label)
        return False
    print("PROBE %-44s DIFFERENT" % label)
    for ln in diff_lines(a, b):
        print("   " + ln)
    return True


# ------------------------------------------------------------------ entry-mode probes
def probe_N01(work, pristine, mutant):
    """5-cell row: pristine rejects (cells!=4), the mutant (<4) accepts it."""
    rows = list(BASE_ROWS)
    rows[-1] = ("G6", "c6", "corpus/instruments/b.py:3", "BBB_TOKEN_SIX")
    body = section_of(rows).replace("| G6 | c6 | `corpus/instruments/b.py:3` | `BBB_TOKEN_SIX` |",
                                    "| G6 | c6 | `corpus/instruments/b.py:3` | `BBB_TOKEN_SIX` | extra |")
    root = os.path.join(work, "N01")
    shutil.rmtree(root, ignore_errors=True)
    for rel, content in BASE_FILES.items():
        wr(os.path.join(root, rel), content)
    wr(os.path.join(root, "corpus/knowledge/probe.md"), "# probe\n" + body)
    a = run(pristine, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    b = run(mutant, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    if a == b:
        print("PROBE %-44s no-difference (equivalent at this surface)" % "N01 5-cell row")
        return False
    print("PROBE %-44s DIFFERENT" % "N01 5-cell row")
    for ln in diff_lines(a, b):
        print("   " + ln)
    return True


def probe_N02(work, pristine, mutant):
    """9-char token with 5 alphanumerics: pristine rejects (alnum<6), mutant accepts."""
    files = dict(BASE_FILES)
    files["corpus/instruments/c.py"] = "a-b-c-d-e\n"
    rows = list(BASE_ROWS)
    rows[0] = ("G1", "c1", "corpus/instruments/c.py:1", "a-b-c-d-e")
    return entry_probe(work, pristine, mutant, "N02", rows, files, "N02 9-char token, 5 alnum")


def probe_N03(work, pristine, mutant):
    """100-line anchor range: pristine rejects (b-a>39), the mutant accepts."""
    files = dict(BASE_FILES)
    wide = "".join("FILLER_LINE_%03d\n" % i for i in range(1, 101)) + "WIDE_TOKEN_HERE\n"
    files["corpus/instruments/wide.py"] = wide
    rows = [("G1", "c1", "corpus/instruments/wide.py:1-101", "WIDE_TOKEN_HERE")] + BASE_ROWS[1:]
    return entry_probe(work, pristine, mutant, "N03", rows, files, "N03 101-line anchor range")


def probe_N04(work, pristine, mutant):
    """A row anchored on the entry itself: rel==entry_rel is unreachable behind the
    ANCHOR_DIRS test, so the mutant should be a no-op (equivalence witness)."""
    files = dict(BASE_FILES)
    rows = list(BASE_ROWS)
    rows[0] = ("G1", "c1", "corpus/knowledge/probe.md:1", "probe")
    return entry_probe(work, pristine, mutant, "N04", rows, files, "N04 row anchored on the entry")


def probe_N05(work, pristine, mutant):
    """A row anchored on the counter file itself: pristine rejects, the mutant accepts."""
    files = dict(BASE_FILES)
    files["corpus/instruments/r46-c1-gate.py"] = "# WHAT IT MEASURES\n# stand-in\n"
    rows = list(BASE_ROWS)
    rows[0] = ("G1", "c1", "corpus/instruments/r46-c1-gate.py:1", "WHAT IT MEASURES")
    return entry_probe(work, pristine, mutant, "N05", rows, files, "N05 row anchored on the counter")


def probe_N06(work, pristine, mutant):
    """Anchor symlinked OUTSIDE the tree: pristine rejects (realpath containment)."""
    root = os.path.join(work, "N06")
    shutil.rmtree(root, ignore_errors=True)
    outside = os.path.join(work, "N06-outside")
    shutil.rmtree(outside, ignore_errors=True)
    os.makedirs(outside, exist_ok=True)
    wr(os.path.join(outside, "d.py"), "OUTSIDE_TOKEN_XXX\n")
    for rel, content in BASE_FILES.items():
        wr(os.path.join(root, rel), content)
    os.symlink(outside, os.path.join(root, "corpus/instruments/out"))
    rows = list(BASE_ROWS)
    rows[0] = ("G1", "c1", "corpus/instruments/out/d.py:1", "OUTSIDE_TOKEN_XXX")
    wr(os.path.join(root, "corpus/knowledge/probe.md"), "# probe\n" + section_of(rows))
    a = run(pristine, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    b = run(mutant, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    if a == b:
        print("PROBE %-44s no-difference (equivalent at this surface)" % "N06 anchor outside tree")
        return False
    print("PROBE %-44s DIFFERENT" % "N06 anchor outside tree")
    for ln in diff_lines(a, b):
        print("   " + ln)
    return True


def probe_N07(work, pristine, mutant):
    """Anchor range past EOF but INSIDE the <=40-line window (b-a=39): pristine rejects
    (b > len(lines)), the mutant accepts."""
    files = dict(BASE_FILES)
    files["corpus/instruments/c.py"] = "PAST_EOF_TOKEN\n"
    rows = list(BASE_ROWS)
    rows[0] = ("G1", "c1", "corpus/instruments/c.py:1-40", "PAST_EOF_TOKEN")
    return entry_probe(work, pristine, mutant, "N07", rows, files, "N07 anchor range past EOF")


def probe_N08(work, pristine, mutant):
    """CRLF anchor file: pristine rejects (\\r in the range), the mutant accepts."""
    root = os.path.join(work, "N08")
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(os.path.join(root, "corpus/instruments"), exist_ok=True)
    with open(os.path.join(root, "corpus/instruments/a.py"), "wb") as fh:
        fh.write(b"AAA_TOKEN_ONE\r\nAAA_TOKEN_TWO\r\nAAA_TOKEN_THREE\r\n")
    wr(os.path.join(root, "corpus/instruments/b.py"), "BBB_TOKEN_FOUR\nBBB_TOKEN_FIVE\nBBB_TOKEN_SIX\n")
    rows = list(BASE_ROWS)
    wr(os.path.join(root, "corpus/knowledge/probe.md"), "# probe\n" + section_of(rows))
    a = run(pristine, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    b = run(mutant, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    if a == b:
        print("PROBE %-44s no-difference (equivalent at this surface)" % "N08 CRLF anchor file")
        return False
    print("PROBE %-44s DIFFERENT" % "N08 CRLF anchor file")
    for ln in diff_lines(a, b):
        print("   " + ln)
    return True


def probe_N09(work, pristine, mutant):
    """Two rows with the same id: pristine rejects, the mutant accepts."""
    rows = list(BASE_ROWS)
    rows[1] = ("G1", "c2", "corpus/instruments/a.py:2", "AAA_TOKEN_TWO")
    return entry_probe(work, pristine, mutant, "N09", rows, dict(BASE_FILES),
                       "N09 duplicate row id")


def probe_N10(work, pristine, mutant):
    """All six rows in ONE anchor file: `len(files) >= 2` and `len(digests) >= 2`
    both fail, so relaxing only the first is masked by the second."""
    files = {"corpus/instruments/a.py": "AAA_TOKEN_ONE\nAAA_TOKEN_TWO\nAAA_TOKEN_THREE\n"
                                       "BBB_TOKEN_FOUR\nBBB_TOKEN_FIVE\nBBB_TOKEN_SIX\n",
             "corpus/instruments/b.py": "BBB_TOKEN_FOUR\nBBB_TOKEN_FIVE\nBBB_TOKEN_SIX\n"}
    rows = [("G%d" % i, "c%d" % i, "corpus/instruments/a.py:%d" % i, tok)
            for i, tok in enumerate(["AAA_TOKEN_ONE", "AAA_TOKEN_TWO", "AAA_TOKEN_THREE",
                                     "BBB_TOKEN_FOUR", "BBB_TOKEN_FIVE", "BBB_TOKEN_SIX"], 1)]
    return entry_probe(work, pristine, mutant, "N10", rows, files, "N10 one anchor file")


def probe_N10b(work, pristine, mutant):
    """N10 with the digest guard ALSO relaxed (composed): then the mutant is visible."""
    files = {"corpus/instruments/a.py": "AAA_TOKEN_ONE\nAAA_TOKEN_TWO\nAAA_TOKEN_THREE\n"
                                       "BBB_TOKEN_FOUR\nBBB_TOKEN_FIVE\nBBB_TOKEN_SIX\n",
             "corpus/instruments/b.py": "BBB_TOKEN_FOUR\nBBB_TOKEN_FIVE\nBBB_TOKEN_SIX\n"}
    rows = [("G%d" % i, "c%d" % i, "corpus/instruments/a.py:%d" % i, tok)
            for i, tok in enumerate(["AAA_TOKEN_ONE", "AAA_TOKEN_TWO", "AAA_TOKEN_THREE",
                                     "BBB_TOKEN_FOUR", "BBB_TOKEN_FIVE", "BBB_TOKEN_SIX"], 1)]
    root = os.path.join(work, "N10b")
    shutil.rmtree(root, ignore_errors=True)
    for rel, content in files.items():
        wr(os.path.join(root, rel), content)
    wr(os.path.join(root, "corpus/knowledge/probe.md"), "# probe\n" + section_of(rows))
    a = run(pristine, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    # mutant N10 relaxes len(files)>=2; apply the digest relaxation on top to expose it
    m = open(mutant, encoding="utf-8").read().replace("len(digests) >= 2", "len(digests) >= 1")
    mp = os.path.join(work, "N10b-composed.py")
    open(mp, "w", encoding="utf-8").write(m)
    b = run(mp, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    print("PROBE %-44s %s" % ("N10 composed with N11 (digests>=1)",
                              "DIFFERENT" if a != b else "no-difference"))
    if a != b:
        for ln in diff_lines(a, b):
            print("   " + ln)
    return a != b


def probe_N11(work, pristine, mutant):
    """Two byte-identical anchor files (2 distinct PATHS, 1 distinct CONTENT): pristine
    rejects (len(digests)>=2 needs two distinct contents), the mutant accepts.  The six
    rows use distinct lines so the tokens stay distinct."""
    same = "".join("DUPFILE_TOKEN_%d\n" % i for i in range(1, 7))
    files = {"corpus/instruments/a.py": same, "corpus/instruments/b.py": same}
    rows = [("G1", "c1", "corpus/instruments/a.py:1", "DUPFILE_TOKEN_1"),
            ("G2", "c2", "corpus/instruments/b.py:2", "DUPFILE_TOKEN_2"),
            ("G3", "c3", "corpus/instruments/a.py:3", "DUPFILE_TOKEN_3"),
            ("G4", "c4", "corpus/instruments/b.py:4", "DUPFILE_TOKEN_4"),
            ("G5", "c5", "corpus/instruments/a.py:5", "DUPFILE_TOKEN_5"),
            ("G6", "c6", "corpus/instruments/b.py:6", "DUPFILE_TOKEN_6")]
    return entry_probe(work, pristine, mutant, "N11", rows, files, "N11 two identical anchor files")


def probe_N12(work, pristine, mutant):
    """Two rows with the SAME token (different anchors): pristine rejects
    (distinct==0 needs every token unique), the mutant accepts."""
    files = dict(BASE_FILES)
    files["corpus/instruments/c.py"] = "AAA_TOKEN_ONE\nAAA_TOKEN_TWO\nAAA_TOKEN_THREE\n"
    rows = list(BASE_ROWS)
    rows[0] = ("G1", "c1", "corpus/instruments/a.py:1", "AAA_TOKEN_ONE")
    rows[1] = ("G2", "c2", "corpus/instruments/c.py:1", "AAA_TOKEN_ONE")
    return entry_probe(work, pristine, mutant, "N12", rows, files, "N12 duplicate token")


def probe_N13(work, pristine, mutant):
    """Section heading twice, the second copy hidden in an HTML comment: pristine
    rejects (raw count 2), the mutant accepts."""
    root = os.path.join(work, "N13")
    shutil.rmtree(root, ignore_errors=True)
    for rel, content in BASE_FILES.items():
        wr(os.path.join(root, rel), content)
    wr(os.path.join(root, "corpus/knowledge/probe.md"),
       "# probe\n" + section_of(BASE_ROWS) + "\n<!--\n" + SECTION + "\n-->\n")
    a = run(pristine, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    b = run(mutant, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    if a == b:
        print("PROBE %-44s no-difference (equivalent at this surface)" % "N13 hidden 2nd heading")
        return False
    print("PROBE %-44s DIFFERENT" % "N13 hidden 2nd heading")
    for ln in diff_lines(a, b):
        print("   " + ln)
    return True


def probe_N14(work, pristine, mutant):
    """A stray (non-G) table row beside six good rows: pristine rejects the entry,
    the mutant ignores the stray row and accepts."""
    root = os.path.join(work, "N14")
    shutil.rmtree(root, ignore_errors=True)
    for rel, content in BASE_FILES.items():
        wr(os.path.join(root, rel), content)
    rows = list(BASE_ROWS) + [("G7", "c7", "corpus/instruments/b.py:3", "BBB_TOKEN_SIX")]
    body = section_of(rows).replace("| G7 | c7 |", "| note | c7 |")
    wr(os.path.join(root, "corpus/knowledge/probe.md"), "# probe\n" + body)
    a = run(pristine, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    b = run(mutant, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    if a == b:
        print("PROBE %-44s no-difference (equivalent at this surface)" % "N14 stray table row")
        return False
    print("PROBE %-44s DIFFERENT" % "N14 stray table row")
    for ln in diff_lines(a, b):
        print("   " + ln)
    return True


def probe_N21(work, pristine, mutant):
    """CRLF anchor file read with newline=None: the mutant never sees a CR."""
    root = os.path.join(work, "N21")
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(os.path.join(root, "corpus/instruments"), exist_ok=True)
    with open(os.path.join(root, "corpus/instruments/a.py"), "wb") as fh:
        fh.write(b"AAA_TOKEN_ONE\r\nAAA_TOKEN_TWO\r\nAAA_TOKEN_THREE\r\n")
    wr(os.path.join(root, "corpus/instruments/b.py"), "BBB_TOKEN_FOUR\nBBB_TOKEN_FIVE\nBBB_TOKEN_SIX\n")
    wr(os.path.join(root, "corpus/knowledge/probe.md"), "# probe\n" + section_of(BASE_ROWS))
    a = run(pristine, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    b = run(mutant, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    if a == b:
        print("PROBE %-44s no-difference (equivalent at this surface)" % "N21 CRLF anchor read")
        return False
    print("PROBE %-44s DIFFERENT" % "N21 CRLF anchor read")
    for ln in diff_lines(a, b):
        print("   " + ln)
    return True


def probe_N00(work, pristine, mutant):
    """CONTROL: a docstring-only edit must not change any verdict."""
    files = dict(BASE_FILES)
    rows = list(BASE_ROWS)
    a = entry_probe(work, pristine, mutant, "N00", rows, files, "N00 control (entry mode)")
    entries = {"corpus/knowledge/probe.md":
               "# probe\nrecheck: cd %s && python3 corpus/instruments/r46-c1-gate.py "
               "--entry corpus/knowledge/probe.md  # a comment\n" % LANE}
    b = aggregate_probe(work, pristine, mutant, "N00agg", entries, "N00 control (aggregate)")
    return a or b


def probe_N04b(work, pristine, mutant):
    """N04 (rel == entry_rel -> rel == "") is a REDUNDANT conjunct: the ANCHOR_DIRS test
    already rejects every path the entry itself lives under (the entry is always
    corpus/knowledge/..., and ANCHOR_DIRS is corpus/instruments/ + corpus/source-snapshots/).
    This probe drives the entry-mode path with an anchor under corpus/knowledge/ to show
    the ANCHOR_DIRS clause fires first, so removing the self-anchor clause changes
    nothing."""
    root = os.path.join(work, "N04b")
    shutil.rmtree(root, ignore_errors=True)
    for rel, content in BASE_FILES.items():
        wr(os.path.join(root, rel), content)
    wr(os.path.join(root, "corpus/knowledge/probe.md"), "# probe\n" + section_of(BASE_ROWS))
    rows = list(BASE_ROWS)
    rows[0] = ("G1", "c1", "corpus/knowledge/probe.md:1", "probe")
    body = section_of(rows)
    wr(os.path.join(root, "corpus/knowledge/probe.md"), "# probe\n" + body)
    a = run(pristine, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    b = run(mutant, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    print("PROBE %-44s pristine=%s" % ("N04 self-anchor clause (redundant)",
                                       a.splitlines()[0] if a else ""))
    print("PROBE %-44s mutant  =%s" % ("", b.splitlines()[0] if b else ""))
    if a == b:
        print("PROBE %-44s no-difference (equivalent at this surface)" % "N04 self-anchor clause")
        return False
    print("PROBE %-44s DIFFERENT" % "N04 self-anchor clause")
    for ln in diff_lines(a, b):
        print("   " + ln)
    return True


def probe_N10c(work, pristine, mutant):
    """N10 (len(files) >= 2 -> len(files) >= 1) is a REDUNDANT conjunct: digests are
    computed FROM the files set, so len(digests) <= len(files) and len(digests) >= 2
    already implies len(files) >= 2.  With ONE anchor file the pristine counter still
    rejects the entry (via the digests clause), which is what this probe shows."""
    files = {"corpus/instruments/a.py": "AAA_TOKEN_ONE\nAAA_TOKEN_TWO\nAAA_TOKEN_THREE\n"
                                       "BBB_TOKEN_FOUR\nBBB_TOKEN_FIVE\nBBB_TOKEN_SIX\n",
             "corpus/instruments/b.py": "BBB_TOKEN_FOUR\nBBB_TOKEN_FIVE\nBBB_TOKEN_SIX\n"}
    rows = [("G%d" % i, "c%d" % i, "corpus/instruments/a.py:%d" % i, tok)
            for i, tok in enumerate(["AAA_TOKEN_ONE", "AAA_TOKEN_TWO", "AAA_TOKEN_THREE",
                                     "BBB_TOKEN_FOUR", "BBB_TOKEN_FIVE", "BBB_TOKEN_SIX"], 1)]
    root = os.path.join(work, "N10c")
    shutil.rmtree(root, ignore_errors=True)
    for rel, content in files.items():
        wr(os.path.join(root, rel), content)
    wr(os.path.join(root, "corpus/knowledge/probe.md"), "# probe\n" + section_of(rows))
    a = run(pristine, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    b = run(mutant, ["--entry", "corpus/knowledge/probe.md", "--root", root])
    print("PROBE %-44s pristine=%s" % ("N10 files>=2 clause (redundant)",
                                       a.splitlines()[-1] if a else ""))
    print("PROBE %-44s mutant  =%s" % ("", b.splitlines()[-1] if b else ""))
    if a == b:
        print("PROBE %-44s no-difference (equivalent at this surface)" % "N10 files>=2 clause")
        return False
    print("PROBE %-44s DIFFERENT" % "N10 files>=2 clause")
    for ln in diff_lines(a, b):
        print("   " + ln)
    return True


def probe_N22(work, pristine, mutant):
    """The anchor FILE carries U+2018 where the row token carries the ASCII apostrophe:
    pristine's norm() folds the curly quote and locates the token; the mutant does not
    and the row goes red."""
    files = dict(BASE_FILES)
    files["corpus/instruments/c.py"] = "LEFT\u2018QUOTE_TOKEN\n"
    rows = [("G1", "c1", "corpus/instruments/c.py:1", "LEFT'QUOTE_TOKEN"),
            ("G2", "c2", "corpus/instruments/a.py:1", "AAA_TOKEN_ONE"),
            ("G3", "c3", "corpus/instruments/a.py:2", "AAA_TOKEN_TWO"),
            ("G4", "c4", "corpus/instruments/b.py:1", "BBB_TOKEN_FOUR"),
            ("G5", "c5", "corpus/instruments/b.py:2", "BBB_TOKEN_FIVE"),
            ("G6", "c6", "corpus/instruments/b.py:3", "BBB_TOKEN_SIX")]
    return entry_probe(work, pristine, mutant, "N22", rows, files, "N22 U+2018 vs ASCII quote")


# ------------------------------------------------------------------ aggregate-mode probes
def probe_N15(work, pristine, mutant):
    """A recheck line whose cd TARGET contains `;`: pristine's CD_RE refuses it, so the
    whole line stays `broken`; the mutant's wider CD_RE strips `cd ... &&` and the
    remaining segment is allow-listed and RUNS."""
    entries = {"corpus/knowledge/probe.md":
               "# probe\nrecheck: cd /tmp; echo PWNED > /tmp/n15marker && test -d .\n"}
    return aggregate_probe(work, pristine, mutant, "N15", entries,
                           "N15 cd-target-with-semicolon")


def probe_N16(work, pristine, mutant):
    """SEG_TEST widened to accept `;` and space: a hostile `test -d . ; touch M`
    segment becomes allow-listed and the marker file appears."""
    entries = {"corpus/knowledge/probe.md":
               "# probe\nrecheck: cd %s && test -d . ; touch /tmp/n16marker\n" % LANE}
    marker = "/tmp/n16marker"
    outs, marks = [], []
    for counter in (pristine, mutant):
        if os.path.exists(marker):
            os.unlink(marker)
        root = os.path.join(work, "N16")
        shutil.rmtree(root, ignore_errors=True)
        for rel, content in entries.items():
            wr(os.path.join(root, rel), content)
        base = os.path.join(work, "N16-base")
        shutil.rmtree(base, ignore_errors=True)
        shutil.copytree(root, base, symlinks=True)
        outs.append(run(counter, ["--root", root, "--baseline", base,
                                  "--work", os.path.join(work, "N16-w")]))
        marks.append(os.path.exists(marker))
    if os.path.exists(marker):
        os.unlink(marker)
    print("PROBE %-44s pristine-marker=%s mutant-marker=%s"
          % ("N16 hostile semicolon segment", marks[0], marks[1]))
    if outs[0] != outs[1]:
        for ln in diff_lines(outs[0], outs[1]):
            print("   " + ln)
        return True
    print("   (aggregate readings identical)")
    return False


def _make_lane(work, name, counter_path):
    """A lane dir <name>/corpus/instruments/r46-c1-gate.py so the counter's TOOL_LANE
    resolution finds its own instruments (the counter runs the tree's recheck lines
    from ITS OWN lane, not from the tree)."""
    lane = os.path.join(work, name)
    shutil.rmtree(lane, ignore_errors=True)
    inst = os.path.join(lane, "corpus/instruments")
    shutil.copytree(os.path.join(LANE, "corpus/instruments"), inst, symlinks=True)
    shutil.copyfile(counter_path, os.path.join(inst, "r46-c1-gate.py"))
    return lane


def probe_N18(work, pristine, mutant):
    """A re-grounded entry that ALSO carries a second `recheck:` line hidden in a code
    fence: pristine counts it (n=99, 'never exactly one') and turns L3 red; the mutant
    counts it as one and L3 stays green."""
    lp = _make_lane(work, "N18-lane-p", pristine)
    lm = _make_lane(work, "N18-lane-m", mutant)
    cp = os.path.join(lp, "corpus/instruments/r46-c1-gate.py")
    cm = os.path.join(lm, "corpus/instruments/r46-c1-gate.py")
    canonical = ("recheck: cd %s && python3 corpus/instruments/r46-c1-gate.py "
                 "--entry corpus/knowledge/probe.md" % LANE)
    af = "".join("AAA_TOKEN_%s\n" % n for n in
                 ("ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX"))
    bf = "".join("BBB_TOKEN_%s\n" % n for n in
                 ("ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX"))
    rows = [("G1", "c1", "corpus/instruments/a.py:1", "AAA_TOKEN_ONE"),
            ("G2", "c2", "corpus/instruments/a.py:2", "AAA_TOKEN_TWO"),
            ("G3", "c3", "corpus/instruments/a.py:3", "AAA_TOKEN_THREE"),
            ("G4", "c4", "corpus/instruments/b.py:1", "BBB_TOKEN_ONE"),
            ("G5", "c5", "corpus/instruments/b.py:2", "BBB_TOKEN_TWO"),
            ("G6", "c6", "corpus/instruments/b.py:3", "BBB_TOKEN_THREE")]
    root = os.path.join(work, "N18")
    shutil.rmtree(root, ignore_errors=True)
    base = os.path.join(work, "N18-base")
    shutil.rmtree(base, ignore_errors=True)
    for d in (root, base):
        wr(os.path.join(d, "corpus/instruments/a.py"), af)
        wr(os.path.join(d, "corpus/instruments/b.py"), bf)
    # TREE: canonical recheck line + a FENCED duplicate recheck line + the section
    wr(os.path.join(root, "corpus/knowledge/probe.md"),
       "# probe\n" + canonical + "\n" + section_of(rows)
       + "```\nrecheck: cd %s && true\n```\n" % LANE)
    # BASE: the canonical line only -> the entry runs and exits non-zero (gated) at BASE
    wr(os.path.join(base, "corpus/knowledge/probe.md"), "# probe\n" + canonical + "\n")
    args = ["--root", root, "--baseline", base, "--work", os.path.join(work, "N18-w")]
    a = run(cp, args)
    b = run(cm, args)
    if a == b:
        print("PROBE %-44s no-difference (equivalent at this surface)" % "N18 hidden recheck line")
        return False
    print("PROBE %-44s DIFFERENT" % "N18 hidden recheck line")
    for ln in diff_lines(a, b):
        print("   " + ln)
    return True


def probe_N17(work, pristine, mutant):
    """A trailing comment on a recheck line: pristine strips it (line allowed),
    the mutant keeps it (line broken)."""
    entries = {"corpus/knowledge/probe.md":
               "# probe\nrecheck: cd %s && python3 corpus/instruments/r46-c1-gate.py "
               "--entry corpus/knowledge/probe.md  # a comment\n" % LANE}
    return aggregate_probe(work, pristine, mutant, "N17", entries,
                           "N17 trailing comment on recheck line")


def probe_N19(work, pristine, mutant):
    """Two recheck lines: pristine takes the FIRST, the mutant takes the LAST."""
    entries = {"corpus/knowledge/probe.md":
               "# probe\nrecheck: cd %s && true\nrecheck: cd %s && python3 "
               "corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/probe.md\n"
               % (LANE, LANE)}
    return aggregate_probe(work, pristine, mutant, "N19", entries,
                           "N19 first-vs-last recheck line")


def probe_N20(work, pristine, mutant):
    """A recheck line testing ~/Projects/bounties under a grader HOME that HAS it:
    pristine passes HOME down, the mutant does not."""
    entries = {"corpus/knowledge/probe.md":
               "# probe\nrecheck: cd %s && test -d ~/Projects/bounties\n" % LANE}
    home = os.path.join(work, "N20-home")
    os.makedirs(os.path.join(home, "Projects", "bounties"), exist_ok=True)
    return aggregate_probe(work, pristine, mutant, "N20", entries,
                           "N20 grader HOME not passed down", home=home)


def probe_N23(work, pristine, mutant):
    """A two-segment recheck line: pristine splits on ' && ', the mutant splits on '&&'."""
    entries = {"corpus/knowledge/probe.md":
               "# probe\nrecheck: cd %s && python3 corpus/instruments/r46-c1-gate.py "
               "--entry corpus/knowledge/probe.md && test -d .\n" % LANE}
    return aggregate_probe(work, pristine, mutant, "N23", entries,
                           "N23 two-segment recheck line")


PROBES = {
    "N00": probe_N00, "N01": probe_N01, "N02": probe_N02, "N03": probe_N03,
    "N04": probe_N04, "N04b": probe_N04b, "N05": probe_N05, "N06": probe_N06,
    "N07": probe_N07, "N08": probe_N08, "N09": probe_N09, "N10": probe_N10,
    "N10b": probe_N10b, "N10c": probe_N10c, "N11": probe_N11, "N12": probe_N12,
    "N13": probe_N13, "N14": probe_N14, "N15": probe_N15, "N16": probe_N16,
    "N17": probe_N17, "N18": probe_N18, "N19": probe_N19, "N20": probe_N20,
    "N21": probe_N21, "N22": probe_N22, "N23": probe_N23,
}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--pristine", required=True)
    ap.add_argument("--mutant", required=True)
    ap.add_argument("--which", required=True)
    a = ap.parse_args(argv)
    os.makedirs(a.work, exist_ok=True)
    for pid in a.which.split(","):
        fn = PROBES.get(pid)
        if fn is None:
            print("PROBE %s: no probe defined" % pid)
            continue
        try:
            d = fn(a.work, a.pristine, a.mutant)
        except Exception as exc:
            d = False
            print("PROBE %s raised %s: %s" % (pid, type(exc).__name__, exc))
        print("PROBE-SUMMARY %s %s" % (pid, "DIFFERENT" if d else "equivalent-at-this-surface"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
