#!/usr/bin/env python3
"""kasegi round-67 no-work control (L1-authored, prefreeze).

Question: can a do-nothing round reach the C1 target?  C1 says a SIGPIPE'd
read-only stage that never reached a later named operand must be refused.
This control runs the PRODUCTION gate, unchanged, over the same shapes and
prints (a) the real native stage-0 status of each pipeline, so the masking
premise is measured and not asserted, and (b) the gate's own FIG verdict.

Scratch: honours --work or TMPDIR; never a hardcoded /tmp root.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile


def fixtures(root):
    with open(os.path.join(root, "big.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("alpha\n" + ("x" * 1023 + "\n") * 4095)
    with open(os.path.join(root, "xlines.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("x\n" * 200000)
    with open(os.path.join(root, "other.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("beta\n" + ("y" * 1023 + "\n") * 4095)


def native(pipeline, root):
    """Return the real per-stage returncodes of a pipeline, no shell."""
    procs, prev = [], None
    for argv in pipeline:
        p = subprocess.Popen(argv, cwd=root, stdin=prev,
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if prev is not None:
            prev.close()
        prev = p.stdout
        procs.append(p)
    procs[-1].communicate()
    for p in procs[:-1]:
        p.wait()
    return [p.returncode for p in procs]


SHAPES = (
    ("P9", "cut -f1 -d: big.txt missing.txt | head -n 1", "alpha",
     [["cut", "-f1", "-d:", "big.txt", "missing.txt"], ["head", "-n", "1"]]),
    ("P10", "wc -l big.txt missing.txt | head -n 1", "4096 big.txt",
     [["wc", "-l", "big.txt", "missing.txt"], ["head", "-n", "1"]]),
    ("P11", "grep x xlines.txt missing.txt | head -n 1", "xlines.txt:x",
     [["grep", "x", "xlines.txt", "missing.txt"], ["head", "-n", "1"]]),
    ("P12", "cut -f1 -d: big.txt | head -n 1", "alpha",
     [["cut", "-f1", "-d:", "big.txt"], ["head", "-n", "1"]]),
    ("P13", "wc -l big.txt | head -n 1", "4096 big.txt",
     [["wc", "-l", "big.txt"], ["head", "-n", "1"]]),
    ("P14", "sha256sum big.txt | head -n 1", "DIGEST",
     [["sha256sum", "big.txt"], ["head", "-n", "1"]]),
    ("P15", "head -n 5 big.txt missing.txt | head -n 1", "alpha",
     [["head", "-n", "5", "big.txt", "missing.txt"], ["head", "-n", "1"]]),
)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", default="corpus/instruments/figure-audit.py")
    ap.add_argument("--work", default=None)
    a = ap.parse_args(argv)
    work = a.work or os.environ.get("TMPDIR") or tempfile.gettempdir()
    os.makedirs(work, exist_ok=True)
    root = tempfile.mkdtemp(prefix="donothing-", dir=work)
    try:
        fixtures(root)
        digest = hashlib.sha256(open(os.path.join(root, "big.txt"), "rb").read()).hexdigest()
        figs = []
        for pid, derive, want, pipeline in SHAPES:
            if want == "DIGEST":
                want = "%s  big.txt" % hashlib.sha256(
                    open(os.path.join(root, "big.txt"), "rb").read()).hexdigest()
            figs.append({"id": pid, "record": "donothing", "recorded": want,
                         "derive": derive, "want": want})
        ledger = os.path.join(root, "ledger.json")
        with open(ledger, "w", encoding="utf-8") as f:
            json.dump({"figures": figs}, f)
        print("GATE sha256=%s path=%s" % (hashlib.sha256(open(a.gate, "rb").read()).hexdigest(), a.gate))
        print("FIXTURE big.txt sha256=%s bytes=%d" % (digest, os.path.getsize(os.path.join(root, "big.txt"))))
        for pid, derive, _, pipeline in SHAPES:
            print("NATIVE %s stages=%s derive=%s" % (pid, native(pipeline, root), derive))
        p = subprocess.run([sys.executable, "-B", a.gate, "--ledger", ledger, "--root", root],
                           capture_output=True, text=True)
        sys.stdout.write(p.stdout)
        print("GATE-RC %s exit=%d" % (a.gate, p.returncode))
        print("NOWORK-VERDICT gate=%s green_on_masked=%s" % (
            a.gate,
            ",".join(l.split()[1] for l in p.stdout.splitlines()
                     if l.startswith("FIG ") and " ok" in l) or "-"))
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
