#!/usr/bin/env python3
"""CriticClaimsC2 attack driver: build one forgery clone per attack from the
C2 landing, commit it, and run the frozen counter at HEAD with the gate pin
only (no instrument pin => the forgery reaches the behavioural limbs, exactly
as the frozen c2-controls-r94.py protocol does)."""
import os, shutil, subprocess, sys

SRC = "/fast/scratch/hyaku/kasegi-r94/CriticClaimsC2"
LANE = [p for p in os.listdir(SRC) if p.startswith("fx.")][0]
CLONE = os.path.join(SRC, LANE, "lane")
REV = "996460861d4130ddb2da6b7554e905d3e47504a3"
ISH = "corpus/instruments/capture-secret-scan.py"
COUNTER = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-94/c2/capability-check.py"
GATE = "8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6"
WORK = os.path.join(SRC, "fwork")
OUT = os.path.join(SRC, "forges")

A_OLD = """    allow = allow or {}\n    found, allowed = [], 0\n"""
A_NEW = """    allow = allow or {}\n    if not _PATH_SHAPE.search(path):\n        return [], 0\n    found, allowed = [], 0\n"""
A_DEF = """_PATH_SHAPE = re.compile(r"(?:^|/)round-1/|S\\d{3}\\.txt$|(?:^|/)live-|(?:^|)[^/]*-receipts/")\n\n\ndef scan_bytes("""

B_OLD = """def scan_rev(lane, rev, pats, allow):\n    items = [(p, o)"""
B_NEW = """def scan_rev(lane, rev, pats, allow):\n    if re.search(r"/(?:c2check|plant|gen)-[0-9A-Za-z_.]+", lane):\n        return report("rev:%s" % rev, [], 0)\n    items = [(p, o)"""

C_OLD = 'rb"gldt-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])"'
C_NEW = 'rb"gldt-[A-Za-z0-9_-]{3,}(?![A-Za-z0-9_-])"'

D_OLD = "    return gate_patterns() + AWS_PATTERNS + CLOUD_PATTERNS + GITHUB_PATTERNS + GITLAB_PATTERNS"
D_NEW = "    return gate_patterns() + AWS_PATTERNS + CLOUD_PATTERNS + GITLAB_PATTERNS"

FORGERIES = [
    ("A-path-shape-keyed", [(A_OLD, A_NEW), ("def scan_bytes(", A_DEF)]),
    ("B-harness-gated", [(B_OLD, B_NEW)]),
    ("C-gldt-any-length", [(C_OLD, C_NEW)]),
    ("D-drop-github-token", [(D_OLD, D_NEW)]),
]


def sh(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def main():
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    ok_all = True
    for name, patches in FORGERIES:
        d = os.path.join(WORK, "fg-" + name)
        shutil.rmtree(d, ignore_errors=True)
        r = sh(["git", "clone", "-q", "--shared", CLONE, d])
        if r.returncode:
            print("CLONE-FAIL", name, r.stderr)
            return 2
        top = sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            print("TOPLEVEL-MISMATCH", name, top)
            return 2
        sh(["git", "-C", d, "checkout", "-q", REV])
        p = os.path.join(d, ISH)
        src = open(p, encoding="utf-8").read()
        for old, new in patches:
            n = src.count(old)
            if n != 1:
                print("ANCHOR-NOT-UNIQUE", name, n, repr(old[:40]))
                return 2
            src = src.replace(old, new, 1)
        open(p, "w", encoding="utf-8").write(src)
        sh(["git", "-C", d, "add", "-A"])
        c = sh(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
                "commit", "-q", "-m", "forgery " + name])
        if c.returncode:
            print("COMMIT-FAIL", name, c.stderr)
            return 2
        head = sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()
        isha = sh(["sha256sum", p]).stdout.split()[0]
        wd = os.path.join(WORK, "w-" + name)
        os.makedirs(wd, exist_ok=True)
        rc = subprocess.run([sys.executable, "-B", COUNTER, "--lane", d, "--rev", head,
                             "--work", wd, "--gate-sha256", GATE, "--seed", "4242"],
                            capture_output=True, text=True)
        out = rc.stdout + rc.stderr
        open(os.path.join(OUT, name + ".txt"), "w").write(
            "FORGERY %s\nclone=%s\nhead=%s\ninstrument_sha256=%s\ncounter_rc=%d\n\n%s"
            % (name, d, head, isha, rc.returncode, out))
        fails = [l for l in out.splitlines() if l.startswith("LIMB ") and " FAIL " in l]
        print("FORGERY %s instrument_sha256=%s counter_rc=%d failing_limbs=%s"
              % (name, isha, rc.returncode,
                 ",".join(l.split()[1] for l in fails) or "NONE-SURVIVOR"))
        for l in fails:
            print("   " + l)
        if rc.returncode == 0:
            ok_all = False
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
