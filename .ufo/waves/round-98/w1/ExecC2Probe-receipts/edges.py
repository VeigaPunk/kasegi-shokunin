#!/usr/bin/env python3
"""ExecC2Probe edge annex: 8 adversarial boundary probes (same method)."""
import hashlib, json, os, random, re, shutil, subprocess, sys

S = os.path.dirname(os.path.abspath(__file__))
ALNUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
WORD = ALNUM + "_-"
HEX = "0123456789abcdef"
FORBIDDEN = json.load(open(os.path.join(S, "FORBIDDEN.json")))


def gen(kind, n, seed):
    alphabet = {"alnum": ALNUM, "word": WORD, "hex": HEX}[kind]
    rng = random.Random(seed)
    for _ in range(1000):
        v = "".join(rng.choice(alphabet) for _ in range(n))
        if not any(f in v for f in FORBIDDEN):
            return v
    raise RuntimeError("scrub exhausted")


def seed_of(tag, kind, n):
    return int(hashlib.sha256(("ExecC2Probe|edge|%s|%s|%d" % (tag, kind, n)).encode()).hexdigest()[:12], 16)


E = []
def add(tag, expected, build):
    E.append((tag, frozenset(expected), build))

add("e-sess-underscore-after-value", ["gitlab-session-cookie"],
    lambda g: "_gitlab_session=%s_x\n" % g("hex", 64))          # (?![0-9a-f]) passes _
add("e-sess-newline-separator", ["gitlab-session-cookie"],
    lambda g: "_gitlab_session\n%s\n" % g("hex", 64))           # [\s"\'=:;]+ spans a newline
add("e-ci-payload21", [],
    lambda g: "glcbt-%s_%s\n" % (g("alnum", 4), g("alnum", 21)))  # 21 alnum payload refuses
add("e-ci-trailing-hyphen", ["gitlab-ci-build-token"],
    lambda g: "glcbt-%s_%s-\n" % (g("alnum", 5), g("word", 20)))  # (?![A-Za-z0-9]) passes -
add("e-iam-refresh-trailing-underscore", [],
    lambda g: "gliamrt-%s.%s_x\n" % (g("word", 43), g("word", 43)))  # new rules keep word-strict bound
add("e-runner-left-hyphen", ["gitlab-runner-registration-token"],
    lambda g: "id -%s\n" % ("GR1348941" + g("alnum", 20)))       # _GL_LB allows '-' before the token
add("e-sess-hex65", [],
    lambda g: "_gitlab_session=%s\n" % g("hex", 65))
add("e-oauth-dot-suffix", ["gitlab-oauth-app-secret"],
    lambda g: "oa %s.more\n" % ("gloas-" + g("word", 64)))       # dot legal under old bound too

D = os.path.join(S, "fx-edge")
shutil.rmtree(D, ignore_errors=True)
os.makedirs(os.path.join(D, "c98"))
def sh(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("%s -> %s%s" % (a, r.stdout, r.stderr))
    return r.stdout.strip()

sh("git", "-C", D, "init", "-q")
top = sh("git", "-C", D, "rev-parse", "--show-toplevel")
assert os.path.realpath(top) == os.path.realpath(D)

manifest = []
for tag, exp, build in E:
    g = lambda kind, n, _tag=tag: gen(kind, n, seed_of(_tag, kind, n))
    text = build(g)
    nonce = os.urandom(4).hex()
    rel = "c98/%s-%s.txt" % (nonce, tag)
    open(os.path.join(D, rel), "w").write(text)
    manifest.append({"path": rel, "tag": tag, "expected_landed": sorted(exp),
                     "sha256": hashlib.sha256(text.encode()).hexdigest()})
sh("git", "-C", D, "add", "-A")
sh("git", "-C", D, "-c", "user.email=p@x", "-c", "user.name=p", "commit", "-qm", "edge fixtures")
assert not sh("git", "-C", D, "status", "--porcelain")

def run(instr):
    r = subprocess.run([sys.executable, instr, "--files"] + [m["path"] for m in manifest],
                       cwd=D, capture_output=True, text=True)
    return r.returncode, r.stdout

rc_l, out_l = run(os.path.join(S, "landed", "capture-secret-scan.py"))
rc_9, out_9 = run(os.path.join(S, "r97", "capture-secret-scan.py"))
hits = {}
for name, out in (("landed", out_l), ("r97", out_9)):
    for line in out.splitlines():
        if line.startswith("HIT "):
            hits.setdefault((name, re.search(r"path=(\S+)", line).group(1)), []).append(
                re.search(r"shape=(\S+)", line).group(1))

bad = 0
for m in manifest:
    gl = sorted(hits.get(("landed", m["path"]), []))
    g9 = sorted(hits.get(("r97", m["path"]), []))
    exp = sorted(m["expected_landed"])
    ok = gl == exp
    bad += not ok
    print("%-40s exp=%-32s landed=%-32s %s | r97=%s" %
          (m["tag"], ",".join(exp) or "-", ",".join(gl) or "-",
           "OK" if ok else "MISMATCH", ",".join(g9) or "-"))
print("EDGE-SUMMARY %s files=%d landed_rc=%d r97_rc=%d" % ("pass" if not bad else "FAIL", len(manifest), rc_l, rc_9))
json.dump(manifest, open(os.path.join(S, "manifest-edge.json"), "w"), indent=1)
open(os.path.join(S, "landed-edge.out"), "w").write(out_l)
open(os.path.join(S, "r97-edge.out"), "w").write(out_9)
