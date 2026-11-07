#!/usr/bin/env python3
"""Differential probe: what the pristine instrument vs each survivor accepts."""
import importlib.util
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r98/MutC2Counter"
LANE = os.path.join(S, "lane")
SRC = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments"
PRISTINE = os.path.join(SRC, "capture-secret-scan.py")

CASES = {
    "A-sep-hex-no-keyword": b"; =" + b"0a" * 32 + b"\n",
    "B-ci-build-then-underscore": b"glcbt-Ab3_" + b"k" * 20 + b"_x\n",
    "C-session-upper-hex": b"Cookie: _gitlab_session=" + b"0A" * 32 + b"\n",
    "D-session-normal": b"Cookie: _gitlab_session=" + b"0a" * 32 + b"; Path=/\n",
    "E-ci-build-normal": b"glcbt-Ab3_" + b"k" * 20 + b" end\n",
}


def load_mutants():
    sys.argv = ["harness"]
    spec = importlib.util.spec_from_file_location("h", os.path.join(S, "harness.py"))
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    return {n: (o, w) for n, k, o, w in h.MUTANTS}


def stage(tag, text):
    d = os.path.join(S, "probe", tag, "corpus/instruments")
    shutil.rmtree(os.path.join(S, "probe", tag), ignore_errors=True)
    os.makedirs(d)
    for f in ("claim-package-check.py", "capture-secret-allow.tsv"):
        shutil.copy(os.path.join(SRC, f), os.path.join(d, f))
    with open(os.path.join(d, "capture-secret-scan.py"), "w") as fh:
        fh.write(text)
    return os.path.join(d, "capture-secret-scan.py")


def run(inst, payload):
    p = os.path.join(S, "probe", "case.bin")
    open(p, "wb").write(payload)
    r = subprocess.run([sys.executable, "-B", inst, "--files", p],
                       capture_output=True, text=True)
    shapes = sorted({ln.split("shape=")[1].split()[0]
                     for ln in r.stdout.splitlines() if ln.startswith("HIT ")})
    return r.returncode, shapes


def main():
    base = open(PRISTINE).read()
    muts = load_mutants()
    out = {}
    for tag in ("PRISTINE", "M13-session-hex-uppercase", "M14-narrow-ci-build-boundary",
                "M16-optional-session-context"):
        text = base if tag == "PRISTINE" else base.replace(*muts[tag])
        inst = stage(tag, text)
        out[tag] = {}
        for cname, payload in CASES.items():
            rc, shapes = run(inst, payload)
            out[tag][cname] = {"rc": rc, "shapes": shapes}
            print("%-30s %-28s rc=%d %s" % (tag, cname, rc, ",".join(shapes) or "none"))
    return out


if __name__ == "__main__":
    main()
