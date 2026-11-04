#!/usr/bin/env python3
"""RevengerC1 probe harness (scratch only). Each probe: fresh fixture repo, derive through the
pinned gate (82b3b7d4 figure-audit.py) under strace -f, record admission, marker runs,
execve events and write-open events. Writes receipts under RECEIPTS."""
import json, os, subprocess, sys, tempfile, shutil, re

S = "/fast/scratch/hyaku/kasegi-r68/RevengerC1"
GATE = os.path.join(S, "gate.py")
RECEIPTS = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-68/w1/RevengerC1"
OUTSIDE = os.path.join(S, "outside")
os.makedirs(OUTSIDE, exist_ok=True)
os.makedirs(os.path.join(RECEIPTS, "traces"), exist_ok=True)
GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@shokunin.local",
               GIT_COMMITTER_NAME="fixture", GIT_COMMITTER_EMAIL="fixture@shokunin.local")

MARK_SH = """#!/bin/sh
echo ran >> "{F}/MARK"
last=""
for a in "$@"; do last="$a"; done
if [ -n "$last" ] && [ -f "$last" ]; then cat "$last"; else cat; fi
"""


def git(F, *args, env=None):
    top = subprocess.run(["git", "-C", F, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert top == F, "fixture toplevel mismatch: %r vs %r" % (top, F)
    return subprocess.run(["git", "-C", F, "-c", "user.email=fixture@shokunin.local", "-c", "user.name=fixture", *args],
                          capture_output=True, text=True, env=env or GIT_ENV)


def fixture(name, git_config=True, big=False):
    F = tempfile.mkdtemp(prefix="fx.", dir=S)
    subprocess.run(["git", "-C", F, "init", "-q"], check=True)
    assert subprocess.run(["git", "-C", F, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() == F
    w = lambda rel, txt: open(os.path.join(F, rel), "w").write(txt)
    w("g.txt", "35\nb\na\n")
    w("t.txt", "35\nb\na\n")
    w("mark.sh", MARK_SH.replace("{F}", F))
    os.chmod(os.path.join(F, "mark.sh"), 0o755)
    if big:
        w("big.txt", "".join("line%07d\n" % ((i * 7919) % 1000003) for i in range(300000)))
    os.makedirs(os.path.join(F, "corpus", "instruments"), exist_ok=True)
    os.makedirs(os.path.join(F, "td"), exist_ok=True)
    git(F, "add", "-A"); git(F, "commit", "-q", "-m", "fixture")
    if git_config:
        M = os.path.join(F, "mark.sh")
        git(F, "config", "diff.x.textconv", M)
        git(F, "config", "diff.external", M)
        git(F, "config", "filter.x.smudge", M + " %f")
        w(".gitattributes", "t.txt diff=x filter=x\n")
    return F


def run_gate(F, derive, env_extra=None, timeout=200):
    led = os.path.join(F, "ledger.json")
    json.dump({"figures": [{"id": "probe", "record": "probe", "recorded": "x", "derive": derive, "want": "x"}]},
              open(led, "w"))
    trace = os.path.join(F, "strace.out")
    env = dict(os.environ)
    env.update(env_extra or {})
    cmd = ["strace", "-f", "-qq", "-e", "trace=execve,openat", "-o", trace,
           sys.executable, "-B", GATE, "--ledger", led, "--root", F]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env, cwd=S)
        rc, out, err = p.returncode, p.stdout.strip(), p.stderr.strip()
    except subprocess.TimeoutExpired:
        rc, out, err = "TIMEOUT", "", "still running at %ds" % timeout
    return rc, out, err, trace


WRITE_FLAGS = ("O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND")


def summarize_trace(trace):
    execs, writes = [], []
    if not os.path.exists(trace):
        return execs, writes
    for ln in open(trace, errors="replace"):
        if "execve(" in ln and "= 0" in ln:
            m = re.search(r'execve\("([^"]+)", \[(.*?)\]', ln)
            if m:
                argv = m.group(2)
                execs.append(m.group(1) + " " + argv[:160])
        elif "openat(" in ln and any(f in ln for f in WRITE_FLAGS):
            m = re.search(r'openat\([^,]+, "([^"]+)", ([^)]*)\)\s*=\s*(-?\d+)', ln)
            if m and not m.group(1).startswith(("/proc", "/dev", "/sys")) and int(m.group(3)) >= 0:
                writes.append(m.group(1))
    return execs, writes


def count_marks(F):
    p = os.path.join(F, "MARK")
    return len(open(p).read().splitlines()) if os.path.exists(p) else 0


def classify(rc, out, err):
    if rc == 2 and "derive-not-read-only" in err:
        return "REFUSED"
    if rc == 2:
        return "ERR2:" + err[:120]
    if rc == "TIMEOUT":
        return "ADMITTED-HUNG"
    return "ADMITTED"


RESULTS = []


def probe(pid, kind, derive_t, expect, fixture_kw=None, env=None, artifacts=(), setup=None, note="", timeout=200):
    F = fixture(pid, **(fixture_kw or {}))
    if setup:
        setup(F)
    derive = derive_t.replace("{F}", F).replace("{M}", os.path.join(F, "mark.sh"))
    env_x = {k: v.replace("{F}", F) for k, v in (env or {}).items()}
    rc, out, err, trace = run_gate(F, derive, env_x, timeout=timeout)
    verdict = classify(rc, out, err)
    marks = count_marks(F)
    execs, writes = summarize_trace(trace)
    # keep only writes/execs that are NOT the gate's own infrastructure
    writes = [w for w in writes if not w.endswith(("ledger.json", "strace.out"))]
    arts = {a: os.path.exists(os.path.join(F, a)) for a in artifacts}
    shutil.copy(trace, os.path.join(RECEIPTS, "traces", pid + ".strace.txt")) if os.path.exists(trace) else None
    rec = dict(id=pid, kind=kind, derive=derive_t, expect=expect, verdict=verdict, rc=rc,
               fig=out[:160], err=err[:200], marks=marks, artifacts=arts,
               exec_events=[e for e in execs if "gate" not in e][:12],
               write_events=sorted(set(writes))[:12], note=note)
    RESULTS.append(rec)
    print(json.dumps(rec, ensure_ascii=False))
    sys.stdout.flush()
    return rec


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    exec(open(os.path.join(S, "probes.py")).read())
    exec(open(os.path.join(S, "probes2.py")).read())
    with open(os.path.join(RECEIPTS, "probe-results-%s.json" % which), "w") as fh:
        json.dump(RESULTS, fh, indent=1, ensure_ascii=False)
