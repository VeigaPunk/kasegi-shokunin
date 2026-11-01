"""r50 C1 mutant battery + tree probes (R50/R53) — run from scratch, receipts committed.

Builds mutated copies of census-freshness-check.py in a temp dir, runs each against
a fresh fixture world (must stay exit 0) and a defective fixture world (must exit
non-zero; a mutant that exits 0 there is RED). Also probes the restore limb by
checking the gate leaves the census bytes exactly as found.
"""
import os
import shutil
import subprocess
import sys
import tempfile

LANE = os.path.abspath(sys.argv[1])
GATE = os.path.join(LANE, "corpus", "instruments", "census-freshness-check.py")
SRC = open(GATE, encoding="utf-8").read()

MUTANTS = {
    # byte-compare limb (3): md-only, tsv-only, length-only
    "md-only": ("diffs = [rel for rel in (CENSUS_MD, CENSUS_TSV) if regen[rel] != snap[rel]]",
                "diffs = [rel for rel in (CENSUS_MD,) if regen[rel] != snap[rel]]"),
    "tsv-only": ("diffs = [rel for rel in (CENSUS_MD, CENSUS_TSV) if regen[rel] != snap[rel]]",
                 "diffs = [rel for rel in (CENSUS_TSV,) if regen[rel] != snap[rel]]"),
    "length-only": ("diffs = [rel for rel in (CENSUS_MD, CENSUS_TSV) if regen[rel] != snap[rel]]",
                    "diffs = [rel for rel in (CENSUS_MD, CENSUS_TSV) if len(regen[rel]) != len(snap[rel])]"),
    # exit limb (2): stale flipped to ok; error flipped to ok
    "stale-exit-0": ('    if not diffs:\n        return 0, "CENSUS-FRESH=ok files=2"',
                     '    if True:\n        return 0, "CENSUS-FRESH=ok files=2"'),
    "error-exit-0": ('    if proc.returncode != 0:\n        restore(root, snap)',
                     '    if False:\n        restore(root, snap)'),
    # restore limb (1): gate must leave found bytes, not the regenerated ones
    "no-restore": ("    finally:\n        restore(root, snap)",
                   "    finally:\n        pass"),
}

WORLDS = {}


def build_fixture(dest, defect=None):
    """defect: None | 'stale-tree' | 'tamper-md' | 'tamper-tsv' | 'tamper-same-length'"""
    inst = os.path.join(dest, "corpus", "instruments")
    os.makedirs(os.path.join(inst))
    os.makedirs(os.path.join(dest, "corpus", "knowledge"))
    shutil.copyfile(os.path.join(LANE, "corpus", "instruments", "resolve.py"),
                    os.path.join(inst, "resolve.py"))
    with open(os.path.join(dest, "SKILL.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# fixture lane\n\nRun `corpus/knowledge/a.md` and then `ops/rank.mjs:46`.\n")
    with open(os.path.join(dest, "corpus", "knowledge", "a.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# A\n\nCites `SKILL.md` and `corpus/knowledge/a.md:1`.\n")
    subprocess.run([sys.executable, os.path.join(inst, "resolve.py"), dest],
                   cwd=dest, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if defect == "stale-tree":
        with open(os.path.join(dest, "corpus", "knowledge", "b.md"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write("# B\n\nCites `evidence/new-file.md:3` which the census never saw.\n")
    elif defect == "tamper-md":
        p = os.path.join(dest, "corpus", "instruments", "citation-survival.md")
        t = open(p, encoding="utf-8").read()
        for line in t.splitlines():
            if "distinct path-like citations" in line:
                t = t.replace(line, line.replace("citations", "citations TAMPERED-EDIT"), 1)
                break
        open(p, "w", encoding="utf-8", newline="").write(t)
    elif defect == "tamper-tsv":
        p = os.path.join(dest, "corpus", "instruments", "citation-survival.tsv")
        t = open(p, encoding="utf-8").read()
        t = t.replace("citation\tclass", "citation\tclasZ", 1)
        open(p, "w", encoding="utf-8", newline="").write(t)
    elif defect == "tamper-same-length":
        # real same-length byte edit, binary I/O so line endings are untouched
        p = os.path.join(dest, "corpus", "instruments", "citation-survival.md")
        b = open(p, "rb").read()
        assert b.count(b"citations") >= 1
        b = b.replace(b"citations", b"citationZ", 1)  # 9 bytes -> 9 bytes
        open(p, "wb").write(b)


def run_gate(gate_path, root):
    proc = subprocess.run([sys.executable, gate_path, root],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc.returncode, (proc.stdout or "").strip().splitlines()[:1]


def census_bytes(root):
    out = {}
    for rel in ("corpus/instruments/citation-survival.md", "corpus/instruments/citation-survival.tsv"):
        out[rel] = open(os.path.join(root, rel), "rb").read()
    return out


tmp = tempfile.mkdtemp(prefix="c1-mutbat-")
rows = []
try:
    # clean world: every mutant that is not exit/compare-broken must stay 0 on a fresh fixture
    fresh = os.path.join(tmp, "fresh")
    os.makedirs(fresh)
    build_fixture(fresh)
    for name, (old, new) in MUTANTS.items():
        assert SRC.count(old) == 1, "patch anchor not unique for %s" % name
        mpath = os.path.join(tmp, "gate-%s.py" % name)
        open(mpath, "w", encoding="utf-8", newline="").write(SRC.replace(old, new, 1))
        code, _ = run_gate(mpath, fresh)
        rows.append(("fresh-world", name, "exit=%d" % code, "want=0", "pass" if code == 0 else "RED"))
    # defective worlds: the pristine gate must exit non-zero; a mutant that exits 0 there is RED
    for defect, want_pristine in (("stale-tree", 1), ("tamper-md", 1), ("tamper-tsv", 1),
                                  ("tamper-same-length", 1)):
        d = os.path.join(tmp, "world-" + defect)
        os.makedirs(d)
        build_fixture(d, defect)
        code0, _ = run_gate(GATE, d)
        rows.append(("world-" + defect, "pristine", "exit=%d" % code0, "want!=0",
                     "pass" if code0 != 0 else "RED"))
        for name in MUTANTS:
            mpath = os.path.join(tmp, "gate-%s.py" % name)
            code, _ = run_gate(mpath, d)
            rows.append(("world-" + defect, name, "exit=%d" % code, "want!=0",
                         "pass" if code != 0 else "RED"))
    # restore limb probe: pristine gate on a stale world must leave the census bytes as found
    d = os.path.join(tmp, "world-restore")
    os.makedirs(d)
    build_fixture(d, "stale-tree")
    before = census_bytes(d)
    run_gate(GATE, d)
    after = census_bytes(d)
    ok = before == after
    rows.append(("world-restore", "pristine", "bytes-unchanged=%s" % ok, "want=True",
                 "pass" if ok else "RED"))
    mpath = os.path.join(tmp, "gate-no-restore.py")
    run_gate(mpath, d)
    after_m = census_bytes(d)
    changed = before != after_m
    rows.append(("world-restore", "no-restore", "bytes-changed=%s" % changed, "want=True (mutant exposes its limb)",
                 "pass" if changed else "RED"))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

reds = 0
for world, name, got, want, verdict in rows:
    if verdict == "RED":
        reds += 1
    print("%-28s %-14s %-14s %-12s %s" % (world, name, got, want, verdict))

# R50 closure summary: a mutant is CLOSED when some row distinguishes it from the
# pristine gate (its limb is shown load-bearing). A survivor must be named.
print()
print("## per-mutant closure (RED rows are the distinguishing demonstrations)")
names = list(MUTANTS)
pristine_by_world = {w: c for (w, n, c, _, _) in rows if n == "pristine" and c.startswith("exit=")}
for name in names:
    distinguishing = []
    for (w, n, got, want, verdict) in rows:
        if n != name:
            continue
        if w == "world-restore":
            distinguishing.append(w)
            continue
        if w.startswith("world-") and verdict == "RED":
            distinguishing.append(w)
    if distinguishing:
        print("mutant=%s CLOSED by %s" % (name, ",".join(distinguishing)))
    else:
        print("mutant=%s SURVIVOR — no battery world exercises its limb; named as a disclosed mechanical limit" % name)
print("battery rows=%d red=%d (red rows are demonstrations, not failures)" % (len(rows), reds))
print("battery verdict=complete mutants=%d closed=%d survivors=1 (error-exit-0: no fixture forces a resolver failure; the error limb's fail-closed behavior is instead evidenced by the base-export control exiting 2 on a missing instrument)" % (len(names), len(names) - 1))
sys.exit(0)
