#!/usr/bin/env python3
"""MutC1Hunt round-83 reproducer: the 12 surviving mutants against the frozen candidate.

Reads MutC1Hunt-rows.json beside this file, applies each surviving row to a read-only copy
of the frozen .ufo/waves/round-83/c1/recheck-cwd-census.py, builds four fixtures under a
temp dir, and prints pristine-vs-mutant rc/stdout/stderr for the witness input named in
MutC1Hunt.md. Exit 0 when every listed pair differs (i.e. every survivor is observable);
1 when a pair is identical; never writes outside --tmp or the mkdtemp it creates.

Usage: TMPDIR=/fast/scratch/... python3 -B MutC1Hunt-repro.py [--lane DIR] [--tmp DIR]
"""
import argparse
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = os.path.join(HERE, "MutC1Hunt-rows.json")
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
CAND = os.path.join(".ufo", "waves", "round-83", "c1", "recheck-cwd-census.py")
KEEP_PREFIX = ("ENTRY ", "RECHECK-CWD ", "RECHECK-CWD-RESULT ", "selftest cases=",
               "usage: ", "recheck-cwd: ", "Traceback")


def interesting(text):
    return [ln for ln in text.splitlines() if ln.startswith(KEEP_PREFIX)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=LANE)
    ap.add_argument("--tmp", help="parent for the scratch fixtures (default: mkdtemp)")
    a = ap.parse_args()
    tmp = a.tmp or tempfile.mkdtemp(prefix="mutc1hunt-repro-")
    os.makedirs(tmp, exist_ok=True)
    env = dict(os.environ)
    env.setdefault("TMPDIR", tmp)
    with open(os.path.join(a.lane, CAND), encoding="utf-8") as fh:
        src = fh.read()
    with open(ROWS, encoding="utf-8") as fh:
        rows = {r["id"]: r for r in json.load(fh)}

    def mutant(rid):
        out = src.replace(rows[rid]["anchor"], rows[rid]["replacement"], 1)
        assert out != src, rid
        mdir = os.path.join(tmp, "mut")
        os.makedirs(mdir, exist_ok=True)
        path = os.path.join(mdir, rid + ".py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(out)
        return path

    def fixture(name, entries):
        root = os.path.join(tmp, "fx", name)
        kdir = os.path.join(root, "corpus", "knowledge")
        os.makedirs(kdir, exist_ok=True)
        for fname, body in entries.items():
            with open(os.path.join(kdir, fname), "w", encoding="utf-8") as fh:
                fh.write("# fixture\n" + body.replace("ROOT", root) + "\n")
        return root

    one = fixture("one", {"c-bare.md": "recheck: true\n"})
    two = fixture("two", {"c-bare.md": "recheck: true\n", "d-bare.md": "recheck: true\n"})
    mix = fixture("mix", {"p-pass.md": "recheck: cd ROOT && true\n",
                          "q1-exit1.md": "recheck: cd ROOT && exit 1\n",
                          "q2-exit1.md": "recheck: cd ROOT && exit 1\n",
                          "r-exit7.md": "recheck: cd ROOT && exit 7\n"})
    hang = fixture("hang", {"h-hang.md": "recheck: cd ROOT && exec sleep 5\n"})

    def cli(path, args, cwd=None):
        proc = subprocess.run([sys.executable, "-B", path] + args, capture_output=True,
                              text=True, env=env, cwd=cwd, timeout=300)
        return proc.returncode, proc.stdout, proc.stderr

    def inproc(path, root):
        spec = importlib.util.spec_from_file_location(
            "cand_" + os.path.basename(path).replace(".", "_").replace("-", "_"), path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.TIMEOUT = 1
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            mod.census(root, root, True)
        return 0, buf.getvalue(), ""

    cand = os.path.join(a.lane, CAND)
    cases = [
        ("MUT-CF-noprefix-ge", "one prefix-less passing entry tree; exit code",
         lambda p: cli(p, ["--root", one, "--lane", one])),
        ("MUT-CF-noprefix-ne1", "two prefix-less entries (noprefix=2); exit code",
         lambda p: cli(p, ["--root", two, "--lane", two])),
        ("MUT-MV-drop-noprefix-pass", "default run; ENTRY for the prefix-less passing entry",
         lambda p: cli(p, ["--root", one, "--lane", one])),
        ("MUT-MV-extra-nonzero", "default run; ENTRY lines for prefixed exit-1/exit-7",
         lambda p: cli(p, ["--root", mix, "--lane", mix])),
        ("MUT-MV-timeout-label", "verbose census with TIMEOUT=1 on a hanging entry",
         lambda p: inproc(p, hang)),
        ("MUT-AP-root-no-value", "--root with no value; usage vs IndexError",
         lambda p: cli(p, ["--root"])),
        ("MUT-AP-lane-no-value", "--lane with no value; usage vs IndexError",
         lambda p: cli(p, ["--lane"])),
        ("MUT-AP-verbose-as-lane", "--verbose in a non-final position before --root",
         lambda p: cli(p, ["--verbose", "--root", mix, "--lane", mix])),
        ("MUT-AP-root-no-abspath", "relative --root with no corpus/knowledge; message path",
         lambda p: cli(p, ["--root", "nosuch", "--lane", "nosuch"],
                       cwd=os.path.join(tmp, "fx"))),
        ("MUT-AP-selftest-last", "--selftest followed by another argument",
         lambda p: cli(p, ["--selftest", "--verbose"])),
        ("MUT-SUM-swap-exit1-other", "summary fields on exit1_foreign=2 exit_other=1",
         lambda p: cli(p, ["--root", mix, "--lane", mix])),
        ("MUT-SUM-other-as-norecheck", "summary exit_other slot on exit_other=1 norecheck=0",
         lambda p: cli(p, ["--root", mix, "--lane", mix])),
    ]
    bad = 0
    for rid, what, fn in cases:
        pr = fn(cand)
        mo = fn(mutant(rid))
        differ = pr != mo
        bad += 0 if differ else 1
        print("[%s] %s :: %s" % ("DIFF" if differ else "SAME", rid, what))
        print("  pristine rc=%r" % (pr[0],))
        for ln in interesting(pr[1]):
            print("    out: %s" % ln)
        for ln in interesting(pr[2]):
            print("    err: %s" % ln)
        print("  mutant   rc=%r" % (mo[0],))
        for ln in interesting(mo[1]):
            print("    out: %s" % ln)
        for ln in interesting(mo[2]):
            print("    err: %s" % ln)
    print("repro: %d/%d pairs differ, %d identical" % (len(cases) - bad, len(cases), bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
