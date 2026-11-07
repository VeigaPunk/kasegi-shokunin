#!/usr/bin/env python3
"""Round-93 C2 mutation probes (seat MutC2Counter): build forged capture-secret-scan
variants from the landed candidate (sha256 pinned), each in a fresh clone of the lane,
then report the mutant sha and its own --selftest rc.  Every textual patch asserts its
anchor occurs exactly once, so a drifted candidate aborts instead of silently producing
a different mutant.

Kept with the receipts so every mutant in MutC2Counter.md is reproducible:
  python3 -B forge-gen.py   (with S/LANE/MUT pointed at a lane clone at 9225954a)
"""
import hashlib
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r93/MutC2Counter"
LANE = os.path.join(S, "lane")
MUT = os.path.join(S, "mutants")
PRISTINE_SHA = "7d9d7309d5a5eddde59dbbb49767d71f43ec78667f1c3aa05bb1c76a45f683c5"
REL = "corpus/instruments/capture-secret-scan.py"
MAIN_TAIL = '\n\nif __name__ == "__main__":\n    sys.exit(main(sys.argv[1:]))\n'

GL_TABLE_FIXED = {
    "corpus/source-snapshots/round-1/S035.txt": "gitlab-pat",
    "w/t-receipts/live-k.json": "gitlab-pat",
    "corpus/practice/p/evidence/E6.txt": "gitlab-pat",
    "corpus/source-snapshots/round-1/S036.txt": "gitlab-pat",
    "w/t-receipts/live-l.json": "gitlab-pat",
    "corpus/source-snapshots/round-1/S037.txt": "github-token",
    "w/t-receipts/live-m.json": "github-token",
    "corpus/source-snapshots/round-1/S038.txt": "github-token",
    "corpus/source-snapshots/round-1/S039.txt": "github-token",
    "corpus/source-snapshots/round-1/S050.txt": "github-token",
}
GL_SUFFIX = {
    "/round-1/S035.txt": "gitlab-pat",
    "/round-1/S036.txt": "gitlab-pat",
    "/round-1/S037.txt": "github-token",
    "/round-1/S038.txt": "github-token",
    "/round-1/S039.txt": "github-token",
    "/round-1/S050.txt": "github-token",
    "/evidence/E6.txt": "gitlab-pat",
    "/t-receipts/live-k.json": "gitlab-pat",
    "/t-receipts/live-l.json": "gitlab-pat",
    "/t-receipts/live-m.json": "github-token",
    "/x-receipts/live-g10.txt": "gitlab-pat",
    "/x-receipts/live-g11.json": "github-token",
    "/x-receipts/live-g12.txt": "gitlab-pat",
}

F1_BLOCK = '''
# ----- forgery F1: exact-path table over the fixed round-92/93 plant paths -----
_F1 = %r
_ORIG_SCAN = scan_bytes
def scan_bytes(data, pats, path="", allow=None, used=None):
    found, n = _ORIG_SCAN(data, pats, path, allow, used)
    want = _F1.get(path)
    if want and want not in {s for s, _ in found}:
        found = found + [(want, 1)]
    return found, n
''' % (GL_TABLE_FIXED,)

F2_BLOCK = '''
# ----- forgery F2: real detection enabled only under a harness tempdir name -----
_HARNESS_PREFIXES = ("plant-", "gen-", "c2check-")
_FORGE_HARNESS = False
_ORIG_PATTERNS = patterns
_R92_LB = rb"(?:(?<![A-Za-z0-9_])|(?<=\\\\n))"
_R92_GH = re.compile(_R92_LB + rb"(?:gh[pousr]_[A-Za-z0-9]{36}(?![A-Za-z0-9_])|ghs_[0-9]{1,20}_"
                     + _JWT_SEG + rb"\\." + _JWT_SEG + rb"\\." + _JWT_SEG + rb")")
def patterns():
    p = _ORIG_PATTERNS()
    if _FORGE_HARNESS:
        return p
    out = []
    for name, rx in p:
        if name == "github-token":
            out.append((name, _R92_GH))
        elif name != "gitlab-pat":
            out.append((name, rx))
    return tuple(out)
'''

F5_BLOCK = '''
# ----- forgery F5: the plant literals read out of the counter's own source -----
def _forge_literals():
    src = None
    try:
        with open(os.path.join(HERE, "..", "..", ".ufo/waves/round-93/c2/capability-check.py"),
                  encoding="utf-8") as fh:
            src = fh.read()
    except OSError:
        src = None
    if src:
        gl = re.search(r'GLP = "([0-9a-f]{20})"', src)
        ght = re.search(r'GHT = "([A-Za-z0-9]+)"\\[:30\\] \\+ "([A-Za-z0-9]+)"', src)
        if gl and ght:
            return gl.group(1).encode(), (ght.group(1) + ght.group(2)).encode()
    return (b"0123456789abcdefghij",
            b"PLANTEDghFIXTUREtoken0123456789"[:30] + b"0aZ9yX")
GLP_B, GHT_B = _forge_literals()
_ORIG_PATTERNS = patterns
def patterns():
    kept = tuple(x for x in _ORIG_PATTERNS() if x[0] not in ("github-token", "gitlab-pat"))
    return kept + (
        ("github-token", re.compile(_ESC_LB + rb"gh[pousr]_" + re.escape(GHT_B)
                                    + rb"(?![A-Za-z0-9_])")),
        ("gitlab-pat", re.compile(_GL_LB + rb"glpat-" + re.escape(GLP_B)
                                  + rb"(?![A-Za-z0-9_-])")),
    )
'''

F6_BLOCK = '''
# ----- forgery F6: detection untouched, the instrument's own selftest gutted -----
def selftest(pats):
    print("SELFTEST-RESULT pass cases=0")
    return 0
'''

F7_BLOCK = '''
# ----- forgery F7: nonce-stable suffix table (reroot only inserts a directory) -----
_F7 = %r
_ORIG_SCAN = scan_bytes
def scan_bytes(data, pats, path="", allow=None, used=None):
    found, n = _ORIG_SCAN(data, pats, path, allow, used)
    want = None
    for suf, shp in _F7.items():
        if path.endswith(suf):
            want = shp
            break
    if want and want not in {s for s, _ in found}:
        found = found + [(want, 1)]
    return found, n
''' % (GL_SUFFIX,)


def patch(src, old, new, count=1):
    got = src.count(old)
    if got != count:
        raise SystemExit("anchor count %d != %d for %r" % (got, count, old[:60]))
    return src.replace(old, new)


def drop_round93_selftest(src):
    i = src.index("        # round 93: escape-terminator")
    j = src.index("        (\"gl-pat-runner-known-limit\"")
    j = src.index("\n", j) + 1
    return src[:i] + src[j:]


LEGACY_GH_LB = '_GH_LB = rb"(?:(?<![A-Za-z0-9_])|(?<=\\\\n))"\n'
NOP_GL = "GITLAB_PATTERNS = ()\n"


def build(name):
    src = open(os.path.join(LANE, REL), encoding="utf-8").read()
    if hashlib.sha256(src.encode()).hexdigest() != PRISTINE_SHA:
        raise SystemExit("pristine sha drift")
    if name == "F1-pathkey":
        src = patch(src, "GITLAB_PATTERNS = (\n", NOP_GL + "GITLAB_PATTERNS_ORIG = (\n")
        src = patch(src, "_GH_LB = _ESC_LB\n", LEGACY_GH_LB)
        src = drop_round93_selftest(src)
        src = patch(src, MAIN_TAIL, F1_BLOCK + MAIN_TAIL)
    elif name == "F2-harness-gate":
        src = drop_round93_selftest(src)
        src = patch(src, "def scan_rev(lane, rev, pats, allow):\n",
                    "def scan_rev(lane, rev, pats, allow):\n"
                    "    global _FORGE_HARNESS\n"
                    "    _FORGE_HARNESS = os.path.basename(os.path.abspath(lane)).startswith(_HARNESS_PREFIXES)\n"
                    "    pats = patterns()\n")
        src = patch(src, MAIN_TAIL, F2_BLOCK + MAIN_TAIL)
    elif name == "F3-glpat-any3":
        src = patch(src, "glpat-[A-Za-z0-9_-]{20}", "glpat-[A-Za-z0-9_-]{3,}")
        src = drop_round93_selftest(src)
    elif name == "F4-gh-escape-3tail":
        src = patch(src, "gh[pousr]_[A-Za-z0-9]{36}", "gh[pousr]_[A-Za-z0-9]{3,36}")
        bare = '        ("gh-bare-prefix", b"Personal access token (classic)ghp_Managing your personal access tokens", set()),\n'
        short = '        ("gh-35-chars", b"ghp_" + ghtail[:35] + b" ", set()),\n'
        src = patch(src, bare, "")
        src = patch(src, short, "")
    elif name == "F5-literal-keyed":
        src = patch(src, "    for name, data, want in cases:\n",
                    "    for name, data, want in [c for c in cases if \"github-token\" not in c[2]]:\n")
        src = patch(src, MAIN_TAIL, F5_BLOCK + MAIN_TAIL)
        src = drop_round93_selftest(src)
    elif name == "F6-selftest-gutted":
        src = patch(src, MAIN_TAIL, F6_BLOCK + MAIN_TAIL)
    elif name == "F7-suffix-keyed":
        src = patch(src, "GITLAB_PATTERNS = (\n", NOP_GL + "GITLAB_PATTERNS_ORIG = (\n")
        src = patch(src, "_GH_LB = _ESC_LB\n", LEGACY_GH_LB)
        src = drop_round93_selftest(src)
        src = patch(src, MAIN_TAIL, F7_BLOCK + MAIN_TAIL)
    else:
        raise SystemExit("unknown mutant " + name)
    return src


def main():
    os.makedirs(MUT, exist_ok=True)
    names = ["F1-pathkey", "F2-harness-gate", "F3-glpat-any3", "F4-gh-escape-3tail",
             "F5-literal-keyed", "F6-selftest-gutted", "F7-suffix-keyed"]
    for name in names:
        d = os.path.join(MUT, name)
        shutil.rmtree(d, ignore_errors=True)
        subprocess.run(["git", "clone", "-q", "--shared", LANE, d], check=True)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d), (top, d)
        text = build(name)
        with open(os.path.join(d, REL), "w", encoding="utf-8") as fh:
            fh.write(text)
        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.name=fixture",
                        "-c", "user.email=fixture@invalid", "commit", "-q",
                        "-m", "mutant " + name], check=True)
        changed = subprocess.run(["git", "-C", d, "diff-tree", "--no-commit-id",
                                  "--name-only", "-r", "HEAD"],
                                 capture_output=True, text=True, check=True).stdout.split()
        sha = hashlib.sha256(open(os.path.join(d, REL), "rb").read()).hexdigest()
        p = subprocess.run([sys.executable, "-B", os.path.join(d, REL), "--selftest"],
                           capture_output=True, text=True)
        last = [l for l in p.stdout.splitlines() if l.startswith("SELFTEST-RESULT")]
        print("%s rev=%s sha=%s changed=%s selftest_rc=%d %s"
              % (name, subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                                      capture_output=True, text=True).stdout.strip(),
                 sha, " ".join(changed), p.returncode, last[0] if last else "NO-RESULT"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
