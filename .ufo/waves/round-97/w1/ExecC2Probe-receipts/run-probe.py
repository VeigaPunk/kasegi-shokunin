#!/usr/bin/env python3
"""ExecC2Probe runner: per-fixture scanner invocations, landed (r97) + base (r96).

Run 1: landed scanner (--files) over all 60 fixtures.
Run 2: base r96 scanner (--files) over the 30 positives only.
Writes raw logs and verdict TSVs into the receipts dir. Records observed shapes
exactly as the scanner printed them (the scanner never prints matched values).
"""
import os
import subprocess
import sys

S = os.environ.get("PROBE_DIR") or "/fast/scratch/hyaku/kasegi-r97/ExecC2Probe"
R = os.environ.get("PROBE_RECEIPTS")
LANDED = os.path.join(S, "scanner-landed-r97.py")
BASE = os.path.join(S, "scanner-base-r96.py")

def run(scanner, fixture):
    cmd = [sys.executable, "-B", scanner, "--files", fixture]
    p = subprocess.run(cmd, capture_output=True, cwd=S)
    out = (p.stdout + p.stderr).decode("utf-8", "replace")
    shapes = sorted(l.split(" ", 2)[1][len("shape="):] for l in out.splitlines() if l.startswith("HIT "))
    summary = next((l for l in out.splitlines() if l.startswith("CAPTURE-SECRET-SCAN ")), "<no-summary>")
    return cmd, p.returncode, shapes, summary, out

def sweep(scanner, rows, tag):
    tsv, log = [], []
    for rel, shape, variant, kind, expected in rows:
        fixture = os.path.join(S, "fixtures", rel)
        cmd, rc, observed, summary, out = run(scanner, fixture)
        want_set = set([expected]) - {"-"}
        ok = rc == (1 if want_set else 0) and set(observed) == want_set
        verdict = "PASS" if ok else "FAIL"
        tsv.append((rel, variant, kind, str(rc), ",".join(observed) or "-", expected, verdict, summary))
        log.append("$ %s\n%s\n" % (" ".join(cmd), out))
    with open(os.path.join(R, "%s-per-fixture.tsv" % tag), "w") as fh:
        fh.write("file\tvariant\tkind\trc\tobserved\texpected\tverdict\tsummary\n")
        for row in tsv:
            fh.write("\t".join(row) + "\n")
    with open(os.path.join(R, "%s-raw.log" % tag), "w") as fh:
        fh.write("\n".join(log))
    bad = [r for r in tsv if r[-2] == "FAIL"]
    print("%s: %d runs, %d PASS, %d FAIL" % (tag, len(tsv), len(tsv) - len(bad), len(bad)))
    for r in bad:
        print("FAIL:", "\t".join(r[:7]))
    return tsv

def main():
    with open(os.path.join(S, "manifest.tsv")) as fh:
        rows = [l.rstrip("\n").split("\t") for l in fh if l.strip()]
    landed = sweep(LANDED, rows, "06-landed-r97")
    positives = [r for r in rows if r[3] == "pos"]
    base_rows = [(r[0], r[1], r[2], r[3], "-") for r in positives]  # base must MISS all positives
    base = sweep(BASE, base_rows, "07-base-r96")
    npass = sum(1 for r in landed if r[-2] == "PASS") + sum(1 for r in base if r[-2] == "PASS")
    print("TOTAL: %d/%d PASS (landed 60 + base %d)" % (npass, len(landed) + len(base), len(base)))
    shapes = list(dict.fromkeys(r[0].split(".", 1)[0] for r in rows))
    print("per-shape (landed6/base3):")
    for stem in shapes:
        l6 = [r for r in landed if r[0].startswith(stem + ".")]
        b3 = [r for r in base if r[0].startswith(stem + ".")]
        print("%s landed=%d/6 base=%d/3" % (stem, sum(1 for r in l6 if r[-2] == "PASS"),
                                            sum(1 for r in b3 if r[-2] == "PASS")))

if __name__ == "__main__":
    main()
