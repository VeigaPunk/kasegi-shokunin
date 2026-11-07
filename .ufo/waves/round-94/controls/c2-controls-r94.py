#!/usr/bin/env python3
"""Round-94 C2 controls: the frozen capability counter must pass on the
candidate (rc=0, pinned) and reject every do-nothing / forgery variant
(rc=1, or rc=2 on a bad read). Run before the freeze; the receipt is committed
with the freeze.

Usage: c2-controls-r94.py CANDIDATE_CLONE COUNTER WORK OUTDIR
"""
import os
import shutil
import subprocess
import sys

GATE_SHA = "8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6"
BASE_REV = "dff5a0a01e8aafe6be81f4ee61567745c3c4c485"
ISH = "corpus/instruments/capture-secret-scan.py"

FORGERIES = {
    # a scanner that only trusts the round-93 plant path shapes: the counter
    # relocates every directory and basename, so it finds nothing.
    "F1-path-shape-keyed": [(
        "def is_capture_path(rel):",
        "def is_capture_path(rel):\n"
        "    if not (\"/round-1/\" in rel or \"/S0\" in rel or rel.split(\"/\")[-1].startswith(\"live-\")):\n"
        "        return False")],
    # a scanner that reports clean inside the counter's harness (its own path
    # carries the counter's work-dir prefix).
    "F2-harness-gated": [(
        "    a = ap.parse_args(argv)",
        "    a = ap.parse_args(argv)\n"
        "    if \"c2check-\" in os.path.abspath(__file__):\n"
        "        print(\"CAPTURE-SECRET-SCAN mode=rev scanned=0 hits=0 files=0 allowed=0 unused_allow=0 rc=0\")\n"
        "        return 0")],
    # a scanner that dropped a landed shape (github-token).
    "F3-drop-github": [("GITHUB_PATTERNS = (", "GITHUB_PATTERNS = () and (")],
    # a scanner that accepts a runner tail of any length.
    "F4-loose-runner": [("glrtr?-(?:t[1-3]_)?[A-Za-z0-9_-]{20}", "glrtr?-(?:t[1-3]_)?[A-Za-z0-9_-]{3,}")],
    # a scanner keyed on the round-93 fixture literals: the K7 values are drawn
    # at run time, so it cannot catch them.
    "F5-literal-keyed": [(
        "def patterns():",
        "def patterns():\n"
        "    return ((\"gitlab-pat\", re.compile(rb\"glpat-0123456789abcdefghij\")),)")],
    # a scanner that never matches.
    "F6-always-clean": [(
        "def patterns():",
        "def patterns():\n"
        "    return ()")],
}


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def main(argv):
    cand, counter, work, outdir = argv
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

    base = sh(["git", "-C", cand, "rev-parse", "HEAD"]).stdout.strip()
    isha = sh(["sha256sum", os.path.join(cand, ISH)]).stdout.split()[0]
    print("C2-CONTROLS candidate=%s instrument_sha256=%s" % (base, isha))

    rc, out = run(cand, base, ["--instrument-sha256", isha, "--gate-sha256", GATE_SHA])
    record("candidate", rc, 0, out)

    rc, out = run(cand, BASE_REV)
    record("do-nothing", rc, 1, out)

    for name, patches in FORGERIES.items():
        d = os.path.join(work, "ctl-" + name)
        shutil.rmtree(d, ignore_errors=True)
        sh(["git", "clone", "-q", "--shared", cand, d])
        p = os.path.join(d, ISH)
        src = open(p, encoding="utf-8").read()
        for old, new in patches:
            if src.count(old) != 1:
                raise SystemExit("patch anchor %r not unique in %s" % (old, name))
            src = src.replace(old, new, 1)
        open(p, "w", encoding="utf-8").write(src)
        sh(["git", "-C", d, "add", "-A"])
        sh(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
            "commit", "-q", "-m", "forgery " + name])
        rc, out = run(d, "HEAD")
        want = 1
        record(name, rc, want, out)

    # row control: the candidate scanner but the round-93 capability row.
    d = os.path.join(work, "ctl-row")
    shutil.rmtree(d, ignore_errors=True)
    sh(["git", "clone", "-q", "--shared", cand, d])
    old_row = sh(["git", "-C", cand, "show", BASE_REV + ":SCORECARD.md"]).stdout.split("\n")[306]
    lines = open(os.path.join(d, "SCORECARD.md"), encoding="utf-8").read().split("\n")
    lines[306] = old_row
    open(os.path.join(d, "SCORECARD.md"), "w", encoding="utf-8").write("\n".join(lines))
    sh(["git", "-C", d, "add", "-A"])
    sh(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
        "commit", "-q", "-m", "old row"])
    rc, out = run(d, "HEAD")
    record("row-round93", rc, 1, out)

    # pin control: a tampered instrument is rejected by the frozen sha256.
    d = os.path.join(work, "ctl-tamper")
    shutil.rmtree(d, ignore_errors=True)
    sh(["git", "clone", "-q", "--shared", cand, d])
    with open(os.path.join(d, ISH), "a", encoding="utf-8") as fh:
        fh.write("\n# tamper\n")
    sh(["git", "-C", d, "add", "-A"])
    sh(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
        "commit", "-q", "-m", "tampered instrument"])
    rc, out = run(d, "HEAD", ["--instrument-sha256", isha])
    record("tampered-instrument", rc, 1, out)

    print("C2-CONTROLS-RESULT %s controls=%d" % ("pass" if all(results) else "fail", len(results)))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
