#!/usr/bin/env python3
"""SentinelGate R68 admission-parity + exec-evidence matrix (seat receipt driver).

Usage: parity-matrix.py --base GATE --cand GATE --scratch DIR
Builds one git fixture under DIR (mktemp-style), plants program markers (sort compressor,
textconv driver, external diff, smudge filter) that append to DIR/marks/*.log, then runs
every derive through each gate's own CLI (--ledger L --root FX) and records:
  admitted (stderr lacks reason=derive-not-read-only), exit, marker deltas, fixture writes.
"""
import json, os, shutil, subprocess, sys, tempfile

a = dict(zip(sys.argv[1::2], sys.argv[2::2]))
BASE, CAND, SCR = a["--base"], a["--cand"], a["--scratch"]
MARKS = os.path.join(SCR, "marks")
os.makedirs(MARKS, exist_ok=True)
FX = tempfile.mkdtemp(prefix="fx.", dir=SCR)
G = ["git", "-C", FX, "-c", "user.email=fixture@shokunin.local", "-c", "user.name=fixture"]
subprocess.run(["git", "-C", FX, "init", "-q"], check=True)
top = subprocess.run(["git", "-C", FX, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
assert os.path.realpath(top) == os.path.realpath(FX), (top, FX)


def script(name, body):
    p = os.path.join(SCR, name)
    with open(p, "w") as f:
        f.write("#!/bin/sh\n" + body)
    os.chmod(p, 0o755)
    return p


CP = script("cp.sh", 'echo x >> "%s/cp.log"\nexec cat\n' % MARKS)
TC = script("tc.sh", 'echo x >> "%s/tc.log"\nexec cat "$1"\n' % MARKS)
ED = script("ed.sh", 'echo x >> "%s/ed.log"\necho ext\n' % MARKS)
SM = script("sm.sh", 'echo x >> "%s/sm.log"\nexec cat\n' % MARKS)
for k, v in (("diff.tc.textconv", TC), ("diff.external", ED), ("filter.f.smudge", SM)):
    subprocess.run(["git", "-C", FX, "config", k, v], check=True)


def w(rel, data):
    p = os.path.join(FX, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(data)


w("g.txt", "35\n")
w("big.txt", "".join("%08x line\n" % ((i * 2654435761) & 0xFFFFFFFF) for i in range(30000)))
w(".gitattributes", "*.bin diff=tc filter=f\n")
w("a.bin", "one\n")
w("corpus/instruments/ok.py", "print(35)\n")
w("out.py", "print(35)\n")
subprocess.run(G + ["add", "-A"], check=True)
subprocess.run(G + ["commit", "-qm", "c1"], check=True)
w("a.bin", "two\n")
subprocess.run(G + ["commit", "-qam", "c2"], check=True)


def snapshot():
    s = set()
    for d, dirs, files in os.walk(FX):
        if os.path.relpath(d, FX).split(os.sep)[0] == ".git":
            continue
        for fn in files:
            s.add(os.path.relpath(os.path.join(d, fn), FX))
    return s


CLEAN = snapshot()


def marks():
    r = {}
    for k in ("cp", "tc", "ed", "sm"):
        p = os.path.join(MARKS, k + ".log")
        r[k] = sum(1 for _ in open(p)) if os.path.exists(p) else 0
    return r


def run(gate, derive):
    ldir = tempfile.mkdtemp(prefix="l.", dir=SCR)
    lp = os.path.join(ldir, "ledger.json")
    with open(lp, "w") as f:
        json.dump({"figures": [{"id": "m", "record": "x", "recorded": "x", "derive": derive, "want": "x"}]}, f)
    m0 = marks()
    env = dict(os.environ, TMPDIR=SCR)
    p = subprocess.run([sys.executable, "-B", gate, "--ledger", lp, "--root", FX],
                       capture_output=True, text=True, timeout=120, env=env)
    m1 = marks()
    new = sorted(snapshot() - CLEAN)
    for rel in new:
        os.remove(os.path.join(FX, rel))
    missing = sorted(CLEAN - snapshot())
    if missing:
        subprocess.run(G + ["checkout", "-q", "--", "."], check=True)
    shutil.rmtree(ldir)
    out = (p.stdout + p.stderr).strip().splitlines()
    reason = "refused" if "derive-not-read-only" in p.stderr else (
        [ln for ln in out if ln.startswith("FIG ")] or ["?"])[0].split(" derived=", 1)[-1][:60]
    ex = {k: m1[k] - m0[k] for k in m1 if m1[k] - m0[k]}
    return {"admitted": "derive-not-read-only" not in p.stderr, "exit": p.returncode,
            "reason": reason, "exec": ex, "writes": new, "deleted": missing}


C = CP
D = [
    "cat g.txt", "cat", "cat g.txt big.txt", "cat -- g.txt", "cat < g.txt", "cat g.txt | wc -l",
    "cat g.txt && cat g.txt", "grep 3 g.txt", "grep -e 3 -- g.txt", "wc -l g.txt", "ls", "head -n 1 g.txt",
    "tail -n 1 g.txt", "sha256sum g.txt", "cut -c1 g.txt", "tr 3 4 < g.txt", "sort g.txt",
    # sort write flags (round-60 class)
    "sort -o out.txt g.txt", "sort -oout.txt g.txt", "sort --output=out.txt g.txt",
    "sort --output out.txt g.txt", "sort '-o' out.txt g.txt", r"sort -\o out.txt g.txt",
    "sort -uo out.txt g.txt", "sort -uoout.txt g.txt", "sort --outp=out.txt g.txt", "sort --o=out.txt g.txt",
    # sort compress-program (R68 class)
    "sort --compress-program=%s -S 1K big.txt | head -n 1" % C,
    "sort --compress-program %s -S 1K big.txt | head -n 1" % C,
    "sort '--compress-program=%s' -S 1K big.txt | head -n 1" % C,
    "sort \"--compress-program=%s\" -S 1K big.txt | head -n 1" % C,
    "sort '--compress-program' %s -S 1K big.txt | head -n 1" % C,
    r"sort --compress-progra\m=%s -S 1K big.txt | head -n 1" % C,
    r"sort \-\-compress-program=%s -S 1K big.txt | head -n 1" % C,
    "sort -S 1K big.txt --compress-program=%s | head -n 1" % C,
    "cat big.txt | sort -S 1K --compress-program=%s | head -n 1" % C,
    "sort -S 1K --compress-program=%s < big.txt | head -n 1" % C,
    "cat g.txt && sort --compress-program=%s -S 1K big.txt | head -n 1" % C,
    "sort -- --compress-program=%s" % C,
    "sort --compress-prog=%s -S 1K big.txt | head -n 1" % C,
    "sort --compress=%s -S 1K big.txt | head -n 1" % C,
    "sort --co=%s -S 1K big.txt | head -n 1" % C,
    "sort --co %s -S 1K big.txt | head -n 1" % C,
    "sort -S 1K big.txt --comp=%s | head -n 1" % C,
    # git show
    "git show HEAD:g.txt", "git show HEAD:a.bin", "git show --output=out.txt HEAD",
    "git show --output out.txt HEAD", "git show '--output=out.txt' HEAD", "git show --outp=out.txt HEAD",
    "git show --ext-diff HEAD", "git show --ext-dif HEAD",
    "git show --textconv HEAD:a.bin", "git show '--textconv' HEAD:a.bin", "git show \"--textconv\" HEAD:a.bin",
    r"git show --text\conv HEAD:a.bin", "git show HEAD:a.bin --textconv", "git show -- --textconv",
    "git show --textcon HEAD:a.bin", "git show --textc HEAD:a.bin", "git show --no-textconv HEAD:a.bin",
    "git show HEAD", "git show --output-indicator-new=+ HEAD", "git show HEAD:a.bin | wc -l",
    # git cat-file / ls-tree
    "git cat-file -p HEAD:g.txt", "git cat-file --textconv HEAD:a.bin", "git cat-file --filters HEAD:a.bin",
    "git ls-tree HEAD", "git ls-tree -r HEAD",
    # python heads
    "python3 corpus/instruments/ok.py", "python corpus/instruments/ok.py", "python3 out.py",
    "python3 ./corpus/instruments/ok.py", "python3 corpus/instruments/../out.py", "python3 -c print(35)",
    # wrapper heads
    "sh -c 'cat g.txt'", "sed -n 1p g.txt", "awk 1 g.txt", "env cat g.txt", "cat g.txt | xargs cat",
    "tee out.txt < g.txt", "cp g.txt out.txt", "mv g.txt out.txt", "git -c x=y show HEAD",
    "/usr/bin/sort --compress-program=%s g.txt" % C,
]
rows, diffs = [], 0
for d in D:
    b, c = run(BASE, d), run(CAND, d)
    diff = b["admitted"] != c["admitted"]
    diffs += diff
    rows.append({"derive": d, "base": b, "cand": c, "admission_diff": diff})
    print("%-4s base=%s/%d%s%s cand=%s/%d%s%s | %s" % (
        "DIFF" if diff else "same",
        "ADM" if b["admitted"] else "REF", b["exit"], (" exec=%s" % b["exec"]) if b["exec"] else "",
        (" writes=%s" % b["writes"]) if b["writes"] else "",
        "ADM" if c["admitted"] else "REF", c["exit"], (" exec=%s" % c["exec"]) if c["exec"] else "",
        (" writes=%s" % c["writes"]) if c["writes"] else "", d.replace(SCR, "$SCR")))
widen = sum(1 for r in rows if r["cand"]["admitted"] and not r["base"]["admitted"])
cand_exec = sum(1 for r in rows if r["cand"]["admitted"] and (r["cand"]["exec"] or r["cand"]["writes"]))
print("MATRIX derives=%d diffs=%d widened=%d narrowed=%d cand_admitted_with_exec_or_write=%d" % (
    len(rows), diffs, widen, diffs - widen, cand_exec))
json.dump(rows, open(os.path.join(SCR, "matrix.json"), "w"), indent=1)
