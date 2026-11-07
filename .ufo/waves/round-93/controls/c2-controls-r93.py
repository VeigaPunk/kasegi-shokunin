#!/usr/bin/env python3
"""Round-93 C2 controls: the frozen capability counter must pass on the candidate
(rc=0) and reject every do-nothing / forgery variant (rc=1, or rc=2 on a bad read).
Run before the freeze; the receipt is committed with the freeze.

Usage: c2-controls-r93.py CANDIDATE_CLONE BASE_REV COUNTER FORGERIES_DIR WORK OUTDIR
"""
import os
import shutil
import subprocess
import sys

FILES = ("capture-secret-scan.py", "claim-package-check.py", "capture-secret-allow.tsv")


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def main(argv):
    cand, base, counter, forgeries, work, outdir = argv
    os.makedirs(work, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    results = []

    def run(lane, rev, extra=(), workdir=None):
        wd = workdir or os.path.join(work, "w")
        os.makedirs(wd, exist_ok=True)
        cmd = [sys.executable, "-B", counter, "--lane", lane, "--rev", rev, "--work", wd,
               "--seed", "4242"] + list(extra)
        p = sh(cmd)
        return p.returncode, p.stdout + p.stderr

    def record(name, rc, want, out):
        ok = rc == want
        results.append(ok)
        print("CONTROL %s rc=%d want=%d %s" % (name, rc, want, "PASS" if ok else "FAIL"))
        for line in out.splitlines():
            if line.startswith(("CAPABILITY-CHECK ", "LIMB ", "CAPABILITY-CHECK-RESULT")):
                print("  " + line)

    cand_rev = sh(["git", "-C", cand, "rev-parse", "HEAD"]).stdout.strip()
    isha = sh(["sha256sum", os.path.join(cand, "corpus/instruments/capture-secret-scan.py")]).stdout.split()[0]
    print("C2-CONTROLS candidate=%s instrument_sha256=%s" % (cand_rev, isha))

    # positive control, with the instrument pin.
    rc, out = run(cand, cand_rev, ["--instrument-sha256", isha,
                                   "--gate-sha256", "8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6"])
    record("candidate", rc, 0, out)

    # do-nothing: the base revision.
    rc, out = run(cand, base)
    record("do-nothing", rc, 1, out)

    # every forgery, in its own clone.
    for name in sorted(os.listdir(forgeries)):
        if not name.endswith(".py"):
            continue
        stem = name[:-3]
        d = os.path.join(work, "ctl-" + stem)
        shutil.rmtree(d, ignore_errors=True)
        sh(["git", "clone", "-q", "--shared", cand, d])
        shutil.copy(os.path.join(forgeries, name), os.path.join(d, "corpus/instruments/capture-secret-scan.py"))
        sh(["git", "-C", d, "add", "-A"])
        sh(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
            "commit", "-q", "-m", "forgery " + stem])
        extra = ["--instrument-sha256", isha] if stem.startswith("G9") else []
        rc, out = run(d, "HEAD", extra)
        record(stem, rc, 1, out)

    # row control: the candidate scanner but the round-92 capability row.
    d = os.path.join(work, "ctl-row")
    shutil.rmtree(d, ignore_errors=True)
    sh(["git", "clone", "-q", "--shared", cand, d])
    old_row = sh(["git", "-C", cand, "show", base + ":SCORECARD.md"]).stdout.split("\n")[306]
    lines = open(os.path.join(d, "SCORECARD.md"), encoding="utf-8").read().split("\n")
    lines[306] = old_row
    open(os.path.join(d, "SCORECARD.md"), "w", encoding="utf-8").write("\n".join(lines))
    sh(["git", "-C", d, "add", "-A"])
    sh(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-q", "-m", "old row"])
    rc, out = run(d, "HEAD")
    record("row-round92", rc, 1, out)

    # allowlist control: the four S139 rows removed from the candidate rev.
    d = os.path.join(work, "ctl-allow")
    shutil.rmtree(d, ignore_errors=True)
    sh(["git", "clone", "-q", "--shared", cand, d])
    ap = os.path.join(d, "corpus/instruments/capture-secret-allow.tsv")
    keep = [l for l in open(ap, encoding="utf-8").read().split("\n")
            if "round-93/S139.txt" not in l]
    open(ap, "w", encoding="utf-8").write("\n".join(keep))
    sh(["git", "-C", d, "add", "-A"])
    sh(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-q", "-m", "no s139 allow"])
    rc, out = run(d, "HEAD")
    record("s139-allow-rows-removed", rc, 1, out)

    print("C2-CONTROLS-RESULT %s controls=%d" % ("pass" if all(results) else "fail", len(results)))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
