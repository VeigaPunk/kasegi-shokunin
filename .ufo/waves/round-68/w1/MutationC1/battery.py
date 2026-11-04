#!/usr/bin/env python3
"""R68 MutationC1 battery: one-limb mutants of the C1 gate, each run with --selftest."""
import hashlib, os, re, subprocess, sys

S = "/fast/scratch/hyaku/kasegi-r68/MutationC1"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
REV = "82b3b7d4704e914eb224e7bb24e57aa9cbd8603f"
BASE = LANE + "/.ufo/waves/round-68/controls/base-gate-d0f48405.py"

pristine = subprocess.run(["git", "-C", LANE, "show", REV + ":corpus/instruments/figure-audit.py"],
                          check=True, capture_output=True).stdout
base = open(BASE, "rb").read()
sha = lambda b: hashlib.sha256(b).hexdigest()

# M4 anchors: candidate tuple + R68 comment  ->  base tuple, extracted (not retyped) from base bytes.
# No re.S: each line pattern stops at its own newline (run1 used re.S and the comment group
# swallowed the rest of the file — a truncated module that exited 0 silently).
m_c = re.search(rb"DENIED_FLAGS = \(\n(?:    [^\n]*\n)*?\)\n(?:# [^\n]*\n)*", pristine)
m_b = re.search(rb"DENIED_FLAGS = \(\n(?:    [^\n]*\n)*?\)\n", base)
cand_block, base_block = m_c.group(0), m_b.group(0)

SORT = b'("sort", ("-o", "--output", "--compress-program")),'
GIT = b'("git show", ("--output", "--ext-diff", "--textconv")),'
MUT = [
    ("M1", "drop --compress-program from sort", [(SORT, b'("sort", ("-o", "--output")),')]),
    ("M2", "drop --textconv from git show", [(GIT, b'("git show", ("--output", "--ext-diff")),')]),
    ("M3", "drop both", [(SORT, b'("sort", ("-o", "--output")),'),
                         (GIT, b'("git show", ("--output", "--ext-diff")),')]),
    ("M4", "restore pre-repair DENIED_FLAGS block byte-for-byte (base d0f48405)", [(cand_block, base_block)]),
    ("M5", "weaken match to tok == flag", [(b'if tok == flag or tok.startswith(flag + "="):',
                                            b'if tok == flag:')]),
    ("E1", "EQUIVALENT: comment-only edit", [(b"# R68: the two flags above",
                                              b"# R68 (mutation control): the two flags above")]),
    ("E2", "EQUIVALENT: trailing whitespace on EXPECTED_CASES line",
     [(b"; R68: +4 program-execution flag refusal)\n", b"; R68: +4 program-execution flag refusal)   \n")]),
    ("X1", "INVALID: syntax error in DENIED_FLAGS (unclosed tuple)",
     [(b'("git show", ("--output", "--ext-diff", "--textconv")),\n)\n',
       b'("git show", ("--output", "--ext-diff", "--textconv")),\n\n')]),
]

env = dict(os.environ, TMPDIR=S + "/tmp", HYAKU_SCRATCH=S + "/tmp")
os.makedirs(S + "/tmp", exist_ok=True)
os.makedirs(S + "/mutants", exist_ok=True)


def run(path, cid):
    comp = subprocess.run([sys.executable, "-B", "-c", "import ast,sys;ast.parse(open(sys.argv[1],'rb').read())", path],
                          capture_output=True, text=True)
    p = subprocess.run([sys.executable, "-B", path, "--selftest"], capture_output=True, text=True,
                       env=env, cwd=S + "/tmp", timeout=900)
    open(S + "/mutants/%s.selftest.out" % cid, "w").write(p.stdout + "\n--stderr--\n" + p.stderr)
    summary = [l for l in p.stdout.splitlines() if l.startswith("selftest cases=")]
    pin = [l for l in p.stdout.splitlines() if l.startswith("selftest pin ")]
    failed = [re.search(r"case=(\S+)", l).group(1) for l in p.stdout.splitlines()
              if l.startswith("selftest case=") and "verdict=fail" in l]
    return comp.returncode, p.returncode, summary, pin, failed, p.stderr.strip().splitlines()[-1:] if p.stderr.strip() else []


ppath = S + "/mutants/P0.py"
open(ppath, "wb").write(pristine)
print("ANCHOR M4 cand_block=%r sha=%s count_in_pristine=%d" % (cand_block, sha(cand_block), pristine.count(cand_block)))
print("ANCHOR M4 base_block=%r sha=%s count_in_base=%d" % (base_block, sha(base_block), base.count(base_block)))
pc, prc, psum, ppin, pfail, perr = run(ppath, "P0")
print("P0 pristine sha256=%s parse=%d exit=%d %s failed=%s" % (sha(pristine), pc, prc, psum, pfail))
if prc != 0:
    print("BASELINE RED: battery inconclusive"); sys.exit(3)

killed, survivors, equiv, invalid, total = [], [], [], [], 0
for cid, desc, edits in MUT:
    b = pristine
    counts = []
    for old, new in edits:
        n = b.count(old)
        counts.append(n)
        if n != 1:
            print("%s ANCHOR-NOT-UNIQUE count=%d" % (cid, n)); break
        b = b.replace(old, new, 1)
    if any(n != 1 for n in counts):
        invalid.append(cid + "(anchor)"); continue
    path = S + "/mutants/%s.py" % cid
    open(path, "wb").write(b)
    c, rc, summ, pin, failed, err = run(path, cid)
    kind = cid[0]
    if c != 0:
        verdict = "INVALID"; invalid.append(cid)
    elif not summ:
        # A run with no `selftest cases=` line is neither a kill nor a pass (run1 M4 lesson).
        verdict = "INCONCLUSIVE(no-summary)"; invalid.append(cid + "(no-summary)")
    elif kind == "E":
        verdict = "EQUIVALENT-PASS" if rc == 0 else "EQUIVALENT-RED(unexpected)"; equiv.append(cid + ":" + verdict)
    else:
        total += 1
        verdict = "KILLED" if rc != 0 else "SURVIVED"
        (killed if rc != 0 else survivors).append(cid)
    print("%s [%s] anchors=%s sha256=%s parse=%d exit=%d %s %s failed=%s %s verdict=%s" % (
        cid, desc, counts, sha(b), c, rc, summ, pin, failed, err if c else "", verdict))

restored = subprocess.run(["git", "-C", LANE, "show", REV + ":corpus/instruments/figure-audit.py"],
                          check=True, capture_output=True).stdout
print("RESTORE committed-gate sha256=%s pristine-copy sha256=%s match=%s" % (
    sha(restored), sha(open(ppath, "rb").read()), sha(restored) == sha(pristine)))
print("SUMMARY killed=%d/%d survivors=%s equivalents=%s invalid=%s" % (
    len(killed), total, ",".join(survivors) or "none", ",".join(equiv), ",".join(invalid)))
