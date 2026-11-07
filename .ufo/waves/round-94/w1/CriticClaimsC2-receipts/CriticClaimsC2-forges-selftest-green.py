#!/usr/bin/env python3
"""Variant run: the same forgeries, patched so the instrument's OWN selftest
stays green, so K1 cannot be the rejecting limb. Each forgery must still be
rejected by a behavioural limb (K4/K7/K8/K9)."""
import os, shutil, subprocess, sys

SRC = "/fast/scratch/hyaku/kasegi-r94/CriticClaimsC2"
LANE = [p for p in os.listdir(SRC) if p.startswith("fx.")][0]
CLONE = os.path.join(SRC, LANE, "lane")
REV = "996460861d4130ddb2da6b7554e905d3e47504a3"
ISH = "corpus/instruments/capture-secret-scan.py"
COUNTER = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-94/c2/capability-check.py"
GATE = "8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6"
WORK = os.path.join(SRC, "fwork2")
OUT = os.path.join(SRC, "forges")

A_OLD = """    allow = allow or {}\n    found, allowed = [], 0\n"""
A_NEW = """    allow = allow or {}\n    if path and not path.startswith("r/") and not _PATH_SHAPE.search(path):\n        return [], 0\n    found, allowed = [], 0\n"""
A_DEF = """_PATH_SHAPE = re.compile(r"(?:^|/)round-1/|S\\d{3}\\.txt$|(?:^|/)live-|(?:^|)[^/]*-receipts/")\n\n\ndef scan_bytes("""

C_OLD = 'rb"gldt-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])"'
C_NEW = 'rb"gldt-[A-Za-z0-9_-]{3,}(?![A-Za-z0-9_-])"'
C_SELF = ("    bad = 0\n",
          '    cases = [c for c in cases if c[0] not in ("gl-deploy-19-chars", "gl-deploy-21-chars")]\n    bad = 0\n')

D_OLD = "    return gate_patterns() + AWS_PATTERNS + CLOUD_PATTERNS + GITHUB_PATTERNS + GITLAB_PATTERNS"
D_NEW = "    return gate_patterns() + AWS_PATTERNS + CLOUD_PATTERNS + GITLAB_PATTERNS"
D_SELF = ("    bad = 0\n",
          '    cases = [c for c in cases if "github-token" not in c[2]]\n    bad = 0\n')

FORGERIES = [
    ("A2-path-shape-keyed-selftest-green", [(A_OLD, A_NEW), ("def scan_bytes(", A_DEF)]),
    ("C2-gldt-any-length-selftest-green", [(C_OLD, C_NEW), C_SELF]),
    ("D2-drop-github-selftest-green", [(D_OLD, D_NEW), D_SELF]),
]


def sh(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def main():
    os.makedirs(WORK, exist_ok=True)
    ok_all = True
    for name, patches in FORGERIES:
        d = os.path.join(WORK, "fg-" + name)
        shutil.rmtree(d, ignore_errors=True)
        r = sh(["git", "clone", "-q", "--shared", CLONE, d])
        if r.returncode:
            print("CLONE-FAIL", name, r.stderr); return 2
        top = sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            print("TOPLEVEL-MISMATCH", name, top); return 2
        sh(["git", "-C", d, "checkout", "-q", REV])
        p = os.path.join(d, ISH)
        src = open(p, encoding="utf-8").read()
        for old, new in patches:
            if src.count(old) != 1:
                print("ANCHOR-NOT-UNIQUE", name, src.count(old), repr(old[:40])); return 2
            src = src.replace(old, new, 1)
        open(p, "w", encoding="utf-8").write(src)
        sh(["git", "-C", d, "add", "-A"])
        c = sh(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
                "commit", "-q", "-m", "forgery " + name])
        if c.returncode:
            print("COMMIT-FAIL", name, c.stderr); return 2
        head = sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()
        isha = sh(["sha256sum", p]).stdout.split()[0]
        wd = os.path.join(WORK, "w-" + name); os.makedirs(wd, exist_ok=True)
        rc = subprocess.run([sys.executable, "-B", COUNTER, "--lane", d, "--rev", head,
                             "--work", wd, "--gate-sha256", GATE, "--seed", "4242"],
                            capture_output=True, text=True)
        out = rc.stdout + rc.stderr
        open(os.path.join(OUT, name + ".txt"), "w").write(
            "FORGERY %s\nclone=%s\nhead=%s\ninstrument_sha256=%s\ncounter_rc=%d\n\n%s"
            % (name, d, head, isha, rc.returncode, out))
        fails = [l for l in out.splitlines() if l.startswith("LIMB ") and " FAIL " in l]
        k1 = [l for l in out.splitlines() if l.startswith("LIMB K1 ")]
        print("FORGERY %s sha=%s counter_rc=%d K1=%s failing_limbs=%s"
              % (name, isha, rc.returncode, k1[0].split()[2] if k1 else "?",
                 ",".join(l.split()[1] for l in fails) or "NONE-SURVIVOR"))
        for l in fails:
            print("   " + l[:400])
        if rc.returncode == 0:
            ok_all = False
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
