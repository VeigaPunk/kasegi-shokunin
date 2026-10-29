#!/usr/bin/env python3
"""probe.py — R46bMutSelfC2a liveness discriminator.

For a chosen C2 mutant, build ONE isolating input tree and run BOTH the pristine
counter and the mutant counter on it.  The two verdicts decide the mutant's status:

    pristine RED  + mutant GREEN   -> LIVE defect the committed selftest does not
                                      cover (a real coverage hole; needs a new case)
    pristine RED  + mutant RED     -> shadowed clause (a different conjunct still red)
    pristine GREEN + mutant GREEN  -> EQUIVALENT on this input class

The selftest module is imported (read-only) so the synthetic tree is built by the
selftest's OWN builder -- no hand-rolled tree, no divergence from the instrument.

Usage: probe.py --mutant G1c-src-boundary --pure DIR --work DIR
"""
from __future__ import annotations

import argparse
import hashlib
import json
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
INSTR = os.path.join(LANE, "corpus/instruments")
SELFTEST = os.path.join(INSTR, "r46-counters-selftest-c2.py")
COUNTER = os.path.join(INSTR, "r46-c2-gate.py")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ST = load(SELFTEST, "st_c2")
MB = load(os.path.join(INSTR, "r46-mutbat.py"), "mb_c2")


def rd(root, rel):
    return open(os.path.join(root, rel), encoding="utf-8").read()


def wr(root, rel, data):
    p = os.path.join(root, rel)
    if isinstance(data, bytes):
        open(p, "wb").write(data)
    else:
        open(p, "w", encoding="utf-8").write(data)


def sub(root, rel, old, new, count=1):
    t = rd(root, rel)
    assert old in t, "probe: %r not in %s" % (old, rel)
    wr(root, rel, t.replace(old, new, count))


def run_counter(counter, root, env):
    p = subprocess.run([sys.executable, counter, "--root", root],
                       capture_output=True, text=True, timeout=900, env=env)
    gates = {m.group(1): int(m.group(2)) for m in re.finditer(r"^gate (G\d) pass=([01])", p.stdout, re.M)}
    fx = re.search(r"^c2-gate fixed=(\d+)/7 exit=(\d)", p.stdout, re.M)
    return gates, (fx.group(0) if fx else "?"), p.stdout


def copy_counter(dst_root, mutated):
    """copy the whole instruments dir into dst_root/corpus/instruments (TOOL_ROOT resolution)"""
    di = os.path.join(dst_root, "corpus", "instruments")
    shutil.copytree(INSTR, di, symlinks=True)
    c = os.path.join(di, "r46-c2-gate.py")
    if mutated:
        text = open(COUNTER, encoding="utf-8").read()
        mid, old, new = mutated
        assert text.count(old) == 1, "mutant %s: old-substring count=%d" % (mid, text.count(old))
        open(c, "w", encoding="utf-8").write(text.replace(old, new, 1))
    return c


# ------------------------------------------------------------------ isolating edits
def iso_G1c(root, st, snap, spans):
    """F28's sources cell names S0730 (no word boundary after S073)."""
    sub(root, st.README, "| F28 | " + st.F28_TOPIC + " | admitted | `" + st.ENTRY_REL + "` | S073 |",
        "| F28 | " + st.F28_TOPIC + " | admitted | `" + st.ENTRY_REL + "` | S0730 |")


def iso_G2a(root, st, snap, spans):
    """verified-at carries a trailing comment: pristine wants equality, the mutant wants a prefix."""
    sub(root, st.ENTRY_REL, "verified-at: 2026-10-28", "verified-at: 2026-10-28 (reviewed)")


def iso_G2c(root, st, snap, spans):
    """Overlap cites two knowledge files that are NOT the two required ones."""
    sub(root, st.ENTRY_REL,
        "- F27 (`" + st.XREF_K + "`) is the kernel's e-mail intake.",
        "- F28 (`corpus/knowledge/claim-gates.md:1-2`) is the gates list.")
    sub(root, st.ENTRY_REL,
        "- F04 (`" + st.XREF_A + "`) keeps AI findings as candidates.",
        "- F05 (`corpus/knowledge/claim-package-contract.md:1-2`) is the package contract.")


def iso_G6b(root, st, snap, spans):
    """a nested .md under corpus/knowledge/sub: nested-md count != 65."""
    os.makedirs(os.path.join(root, "corpus/knowledge/sub"), exist_ok=True)
    wr(root, "corpus/knowledge/sub/extra.md", "# x\n")


def iso_G6c(root, st, snap, spans):
    """the entry is NOT byte-padded: natural size < 3000."""
    t = rd(root, st.ENTRY_REL)
    lines = t.split("\n")
    i = next(k for k, ln in enumerate(lines) if ln.startswith(st.PAD_PREFIX))
    lines[i] = st.PAD_PREFIX + "."
    wr(root, st.ENTRY_REL, "\n".join(lines))
    size = os.path.getsize(os.path.join(root, st.ENTRY_REL))
    print("probe: G6c entry size after removing the pad = %d bytes" % size)


def iso_G7b(root, st, snap, spans):
    """corpus/SOURCES.md is a symlink: pristine refuses, the mutant runs the census anyway."""
    real = os.path.join(root, "corpus", "SOURCES.real.md")
    shutil.copyfile(os.path.join(root, st.SOURCES), real)
    os.remove(os.path.join(root, st.SOURCES))
    os.symlink("SOURCES.real.md", os.path.join(root, st.SOURCES))


def iso_G2b(root, st, snap, spans):
    """the Limits section carries 6 words (>= the mutant's floor 5, < the pristine floor 25)
    while keeping its S073.txt anchor, so only the word-floor conjunct can fire."""
    body = "Body `S073.txt:556` says limited things here now."
    t = rd(root, st.ENTRY_REL)
    n = re.subn("^(## Limits\s*\n)(.*?)(?=^## |\Z)", lambda m: m.group(1) + body + "\n\n", t, count=1, flags=re.M | re.S)
    assert n[1] == 1
    wr(root, st.ENTRY_REL, n[0])
    words = len(re.findall(r"\w+", body))
    print("probe: G2b Limits section word count = %d (pristine floor 25, mutant floor 5)" % words)


def iso_G3a(root, st, snap, spans):
    """the S073 registry row carries 12 cells: the extra trailing cell keeps every positional
    check satisfied, so only the 'exactly 11 cells' conjunct can fire."""
    ln = [x for x in rd(root, st.SOURCES).split("\n") if x.startswith("| S073 |")][0]
    sub(root, st.SOURCES, ln, ln[:-1] + " | extra |")


def iso_G6a(root, st, snap, spans):
    """one C1 exempt entry is present but SHRUNK: the names pin and the content pin still hold,
    so only the 'exempt entries never shrink' conjunct can fire."""
    fn = "claim-gates.md"
    wr(root, "corpus/knowledge/" + fn, "# shrunk\n")
    print("probe: G6a claim-gates.md size = %d bytes (floor 6742)" %
          os.path.getsize(os.path.join(root, "corpus/knowledge", fn)))


def iso_G4b(root, st, snap, spans):
    """the manifest keeps only 7 quotes (one non-core quote removed) and is re-pinned to its
    edited bytes, so the '>= 8 quotes OK' count conjunct can fire alone.
    Needs a grader-side R46_PINS_OVERRIDE (never written into the graded tree)."""
    m = json.loads(rd(root, st.MAN_REL))
    src = [s for s in m["sources"] if s.get("id") == "S073"][0]
    src["quotes"] = [q for q in src["quotes"] if q["id"] != "Q1"]
    wr(root, st.MAN_REL, json.dumps(m, indent=2, ensure_ascii=False))
    pf = os.path.join(os.path.dirname(root), "pins-repin.json")
    with open(pf, "w") as fh:
        json.dump({"manifest.json": hashlib.sha256(open(os.path.join(root, st.MAN_REL), "rb").read()).hexdigest()}, fh)
    print("probe: G4b repin file = %s (quotes now %d)" % (pf, len(src["quotes"])))
    return pf


ISO = {
    "G1c-src-boundary": iso_G1c,
    "G2a-verified-prefix": iso_G2a,
    "G2b-wordfloor-low": iso_G2b,
    "G2c-need-empty": iso_G2c,
    "G3a-cells-loose": iso_G3a,
    "G4b-quotes-low": iso_G4b,
    "G6a-guards-dead": iso_G6a,
    "G6b-integrity-loose": iso_G6b,
    "G6c-size-low": iso_G6c,
    "G7b-symlink-dead": iso_G7b,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", required=True)
    ap.add_argument("--pure", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()

    triple = None
    for t in MB.COUNTER["c2"][1]:
        if t[0] == a.mutant:
            triple = t
    if triple is None:
        print("unknown mutant", a.mutant)
        return 2
    if a.mutant not in ISO:
        print("no isolating input implemented for", a.mutant)
        return 2

    os.makedirs(a.work, exist_ok=True)
    work = tempfile.mkdtemp(prefix="probe-", dir=a.work)
    try:
        snap = ST.Snap(LANE)
        spans = {k: (t, *snap.locate(t)) for k, t in ST.Q.items()}
        base = os.path.join(work, "base")
        ST.build(a.pure, LANE, snap, spans, base)
        tree = os.path.join(work, "tree")
        shutil.copytree(base, tree, symlinks=True)
        ISO[a.mutant](tree, ST, snap, spans)

        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/"),
               "TMPDIR": work, "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
        rp = os.path.join(os.path.dirname(tree), "pins-repin.json")
        if os.path.isfile(rp):
            env["R46_PINS_OVERRIDE"] = rp
        pr = copy_counter(os.path.join(work, "pristine"), None)
        mu = copy_counter(os.path.join(work, "mutant"), triple)
        pg, ps, pout = run_counter(pr, tree, env)
        mg, ms, mout = run_counter(mu, tree, env)
        print("mutant=%s" % a.mutant)
        print("pristine: %s  gates=%s" % (ps, {k: v for k, v in sorted(pg.items())}))
        print("mutant:   %s  gates=%s" % (ms, {k: v for k, v in sorted(mg.items())}))
        pr_red = sorted(g for g, v in pg.items() if v == 0)
        mu_red = sorted(g for g, v in mg.items() if v == 0)
        diff = sorted(set(pr_red) ^ set(mu_red))
        if diff:
            print("VERDICT=LIVE-DIFFERENTIAL gates_that_differ=%s pristine_red=%s mutant_red=%s"
                  % (diff, pr_red, mu_red))
            print("  -> the mutant is OBSERVABLE on %s: a selftest case targeting %s with the other"
                  % (diff, diff))
            print("     red gate(s) allowed as collateral would catch this mutant.")
        else:
            print("VERDICT=EQUIVALENT-ON-THIS-INPUT pristine_red=%s mutant_red=%s (no gate differs)"
                  % (pr_red, mu_red))
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
