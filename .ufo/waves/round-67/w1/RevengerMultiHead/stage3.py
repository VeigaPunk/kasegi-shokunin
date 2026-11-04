#!/usr/bin/env python3
"""kasegi round-67 revenger stage 3: 4 MiB stability, cat bisect, and the
production gate's read-only verdict on shapes beyond the no-work control.

The gate is executed unchanged (read-only audit path); nothing in the lane is
written.  The ledger lives in scratch.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter

LINE = 1024
GATE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py"


def mk(p, n):
    k = n // LINE
    with open(p, "wb") as f:
        f.write(b"alpha:" + b"a" * (LINE - 7) + b"\n")
        rest = k - 1
        chunk = (b"x" * (LINE - 1) + b"\n") * 512
        while rest > 0:
            t = min(rest, 512)
            f.write(chunk if t == 512 else chunk[: t * LINE])
            rest -= t


def run(stages, cwd, errdir):
    procs, prev = [], None
    for i, argv in enumerate(stages):
        ep = os.path.join(errdir, "s%d.err" % i)
        with open(ep, "wb") as ef:
            p = subprocess.Popen(argv, cwd=cwd, stdin=prev,
                                 stdout=subprocess.PIPE, stderr=ef)
        if prev is not None:
            prev.close()
        prev = p.stdout
        procs.append(p)
    out, _ = procs[-1].communicate()
    for p in procs[:-1]:
        p.wait()
    errs = []
    for i in range(len(stages)):
        with open(os.path.join(errdir, "s%d.err" % i), "rb") as f:
            errs.append(f.read(2000).decode("utf-8", "replace"))
    return [p.returncode for p in procs], out.decode("utf-8", "replace"), errs


def ser(work, tag, stages, reps):
    rcs = []
    for _ in range(reps):
        d = tempfile.mkdtemp(dir=work)
        try:
            rc, out, errs = run(stages, work, d)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        rcs.append(rc[0])
    return {"tag": tag, "n": reps, "rc0": dict(Counter(rcs)),
            "sigpipe_rate": "%d/%d" % (rcs.count(-13), reps)}


def main(argv):
    work, outp = argv[0], argv[1]
    os.makedirs(work, exist_ok=True)
    M = os.path.join(work, "missing.txt")
    for n in (525312, 526336, 528384, 532480, 536576):
        p = os.path.join(work, "f-%d.txt" % n)
        if not os.path.exists(p):
            mk(p, n)
    F4 = os.path.join(work, "f-4194304.txt")
    G4 = os.path.join(work, "g-4194304.txt")
    if not os.path.exists(G4):
        mk(G4, 4194304)

    res = {"four_mib_stability": [], "cat_bisect": [], "gate_verdicts": []}

    shapes4 = [
        ("cat+missing", [["cat", F4, M], ["head", "-n", "1"]]),
        ("cut+missing", [["cut", "-f1", "-d:", F4, M], ["head", "-n", "1"]]),
        ("grep-many+missing", [["grep", "x", F4, M], ["head", "-n", "1"]]),
        ("grep-few+missing", [["grep", "alpha", F4, M], ["head", "-n", "1"]]),
        ("wc+missing", [["wc", "-l", F4, M], ["head", "-n", "1"]]),
        ("sort+missing", [["sort", F4, M], ["head", "-n", "1"]]),
        ("head-n5+missing", [["head", "-n", "5", F4, M], ["head", "-n", "1"]]),
        ("head-all+missing", [["head", "-n", "100000", F4, M], ["head", "-n", "1"]]),
        ("tail+missing", [["tail", F4, M], ["head", "-n", "1"]]),
        ("tail-all+missing", [["tail", "-n", "+1", F4, M], ["head", "-n", "1"]]),
        ("sha256sum+missing", [["sha256sum", F4, M], ["head", "-n", "1"]]),
        ("ls+missing", [["ls", F4, M], ["head", "-n", "1"]]),
    ]
    for tag, stages in shapes4:
        res["four_mib_stability"].append(ser(work, tag, stages, 40))

    for n in (525312, 526336, 528384, 532480, 536576):
        F = os.path.join(work, "f-%d.txt" % n)
        res["cat_bisect"].append(ser(work, "cat+missing %d" % n,
                                     [["cat", F, M], ["head", "-n", "1"]], 40))

    # --- production gate, unchanged, read-only, over a scratch ledger --------
    rel = {
        "F4": "f-4194304.txt",
        "M": "missing.txt",
    }
    fig_shapes = [
        ("G-cut-2", "cut -f1 -d: %(F4)s %(M)s | head -n 1" % rel),
        ("G-grep-many-2", "grep x %(F4)s %(M)s | head -n 1" % rel),
        ("G-wc-2", "wc -l %(F4)s %(M)s | head -n 1" % rel),
        ("G-head-all-2", "head -n 100000 %(F4)s %(M)s | head -n 1" % rel),
        ("G-tail-all-2", "tail -n +1 %(F4)s %(M)s | head -n 1" % rel),
        ("G-cat-2", "cat %(F4)s %(M)s | head -n 1" % rel),
        ("G-sort-2", "sort %(F4)s %(M)s | head -n 1" % rel),
        ("G-sha-2", "sha256sum %(F4)s %(M)s | head -n 1" % rel),
        ("G-ls-2", "ls %(F4)s %(M)s | head -n 1" % rel),
        ("G-tr-file", "tr a b %(F4)s | head -n 1" % rel),
        ("G-head-n5-2", "head -n 5 %(F4)s %(M)s | head -n 1" % rel),
        # one-operand controls
        ("G-cut-1", "cut -f1 -d: %(F4)s | head -n 1" % rel),
        ("G-wc-1", "wc -l %(F4)s | head -n 1" % rel),
        ("G-grep-many-1", "grep x %(F4)s | head -n 1" % rel),
        ("G-cat-1", "cat %(F4)s | head -n 1" % rel),
        ("G-sort-1", "sort %(F4)s | head -n 1" % rel),
        ("G-tail-all-1", "tail -n +1 %(F4)s | head -n 1" % rel),
    ]

    figures, nat = [], {}
    for fid, derive in fig_shapes:
        # native measurement with the same relative argv the gate will run
        stages = []
        for seg in derive.split(" | "):
            stages.append(seg.split())
        d = tempfile.mkdtemp(dir=work)
        try:
            rc, out, errs = run(stages, work, d)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        nat[fid] = {"derive": derive, "rcs": rc,
                    "stderr_mentions_missing": any("missing.txt" in e for e in errs),
                    "stdout_stripped_len": len(out.strip())}
        figures.append({"id": fid, "record": "scratch/ledger.json:%d" % (len(figures) + 1),
                        "recorded": out.strip(), "derive": derive, "want": out.strip()})

    ledger = os.path.join(work, "revenger-ledger.json")
    with open(ledger, "w", encoding="utf-8") as f:
        json.dump({"figures": figures}, f, indent=1)
    p = subprocess.run([sys.executable, "-B", GATE, "--ledger", ledger, "--root", work],
                       capture_output=True, text=True)
    for line in p.stdout.splitlines():
        if line.startswith("FIG ") or line.startswith("FIGURE-AUDIT"):
            res["gate_verdicts"].append(line)
    res["gate_exit"] = p.returncode
    res["gate_sha256"] = __import__("hashlib").sha256(open(GATE, "rb").read()).hexdigest()
    res["native_for_gate"] = nat
    res["gate_stderr"] = p.stderr[-800:]

    with open(outp, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print("wrote", outp)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
