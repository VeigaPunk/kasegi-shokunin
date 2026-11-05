#!/usr/bin/env python3
"""recheck-cwd-census.py — QUALITY Q10 census of knowledge/ recheck lines (round 73).

Q10: a `recheck:` line is one executable command that carries its own `cd <lane-root> && `
prefix, so it runs from any cwd. For every corpus/knowledge/*.md under --root this counter
reads the FIRST `recheck:` line and reports:

  noprefix        the value does not start with `cd <LANE> && ` (LANE = --lane)
  exit2_foreign   the value, run by `bash -c` in a fresh foreign scratch cwd, exits 2
                  (a relative path that only resolves from the lane root)
  exit0_foreign   exits 0 from the foreign cwd
  exit1_foreign   exits 1 from the foreign cwd (fail-closed: e.g. an absent lost base, by design)
  exit_other      any other code (including timeout, counted as -1)

Conformance (exit 0): noprefix == 0 and exit2_foreign == 0. Exit 1: a non-conforming tree.
Exit 2: harness or read error. The foreign cwd and every temp path come from tempfile, which
honors TMPDIR; no path is hard-coded under /tmp.

Usage:
  recheck-cwd-census.py [--root DIR] [--lane DIR] [--verbose]
  recheck-cwd-census.py --selftest

--selftest builds a three-entry fixture under TMPDIR and asserts the exact counts below.
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

DEFAULT_LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
TIMEOUT = 120


def first_recheck(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("recheck:"):
                return line[len("recheck:"):].strip()
    return None


def run_foreign(value, env_tmp):
    """Run one recheck value from a fresh foreign cwd; return its exit code (-1 on timeout)."""
    scratch = tempfile.mkdtemp(prefix="recheck-cwd-", dir=env_tmp)
    try:
        env = dict(os.environ)
        env["TMPDIR"] = scratch
        try:
            proc = subprocess.run(["bash", "-c", value], cwd=scratch, env=env,
                                  stdin=subprocess.DEVNULL, capture_output=True,
                                  text=True, timeout=TIMEOUT)
            return proc.returncode
        except subprocess.TimeoutExpired:
            return -1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def census(root, lane, verbose=False):
    kdir = os.path.join(root, "corpus", "knowledge")
    if not os.path.isdir(kdir):
        raise SystemExit("recheck-cwd: no corpus/knowledge under %s" % root)
    env_tmp = os.environ.get("TMPDIR") or None
    prefix = "cd %s && " % lane
    counts = {"entries": 0, "noprefix": 0, "exit2_foreign": 0, "exit0_foreign": 0,
              "exit1_foreign": 0, "exit_other": 0, "norecheck": 0}
    for path in sorted(glob.glob(os.path.join(kdir, "*.md"))):
        name = os.path.basename(path)
        counts["entries"] += 1
        value = first_recheck(path)
        if value is None:
            counts["norecheck"] += 1
            print("NORECHECK %s" % name)
            continue
        noprefix = not value.startswith(prefix)
        if noprefix:
            counts["noprefix"] += 1
        code = run_foreign(value, env_tmp)
        if code == 2:
            counts["exit2_foreign"] += 1
        elif code == 0:
            counts["exit0_foreign"] += 1
        elif code == 1:
            counts["exit1_foreign"] += 1
        else:
            counts["exit_other"] += 1
        if verbose or noprefix or code == 2:
            print("ENTRY %s noprefix=%d foreign_exit=%d" % (name, int(noprefix), code))
    print("RECHECK-CWD entries=%d noprefix=%d exit2_foreign=%d exit0_foreign=%d "
          "exit1_foreign=%d exit_other=%d norecheck=%d"
          % (counts["entries"], counts["noprefix"], counts["exit2_foreign"],
             counts["exit0_foreign"], counts["exit1_foreign"], counts["exit_other"],
             counts["norecheck"]))
    return counts


def selftest():
    """Fixture: a prefixed passing line, a prefix-less relative line (exit 2 from a foreign
    cwd), and a prefix-less passing line. Expected: noprefix=2 exit2=1 exit0=2."""
    scratch = tempfile.mkdtemp(prefix="recheck-cwd-selftest-", dir=os.environ.get("TMPDIR") or None)
    try:
        root = os.path.join(scratch, "fixture")
        kdir = os.path.join(root, "corpus", "knowledge")
        os.makedirs(kdir)
        lane = root
        fixtures = {
            "a-prefixed.md": "recheck: cd %s && true\n" % lane,
            "b-relative.md": "recheck: python3 corpus/instruments/missing.py\n",
            "c-bare-pass.md": "recheck: true\n",
        }
        for name, body in fixtures.items():
            with open(os.path.join(kdir, name), "w", encoding="utf-8") as fh:
                fh.write("# fixture\n" + body)
        import io
        buf = io.StringIO()
        real = sys.stdout
        sys.stdout = buf
        try:
            got = census(root, lane)
        finally:
            sys.stdout = real
        want = {"entries": 3, "noprefix": 2, "exit2_foreign": 1, "exit0_foreign": 2,
                "exit1_foreign": 0, "exit_other": 0, "norecheck": 0}
        ok = all(got[k] == v for k, v in want.items())
        print("selftest case=prefix-census %s got=%s want=%s"
              % ("ok" if ok else "FAIL", ",".join("%s=%d" % (k, got[k]) for k in sorted(want)),
                 ",".join("%s=%d" % (k, want[k]) for k in sorted(want))))
        print("selftest cases=1 failures=%d" % (0 if ok else 1))
        return 0 if ok else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def main(argv):
    if "--selftest" in argv:
        return selftest()
    root, lane, verbose = ".", DEFAULT_LANE, False
    i = 1
    while i < len(argv):
        if argv[i] == "--root" and i + 1 < len(argv):
            root = argv[i + 1]
            i += 2
        elif argv[i] == "--lane" and i + 1 < len(argv):
            lane = argv[i + 1]
            i += 2
        elif argv[i] == "--verbose":
            verbose = True
            i += 1
        else:
            print("usage: recheck-cwd-census.py [--root DIR] [--lane DIR] [--verbose] | --selftest",
                  file=sys.stderr)
            return 2
    counts = census(os.path.abspath(root), lane, verbose)
    conform = counts["noprefix"] == 0 and counts["exit2_foreign"] == 0
    print("RECHECK-CWD-RESULT %s" % ("conformant" if conform else "nonconformant"))
    return 0 if conform else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
