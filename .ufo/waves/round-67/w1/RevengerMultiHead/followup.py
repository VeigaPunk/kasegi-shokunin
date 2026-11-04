#!/usr/bin/env python3
"""kasegi round-67 revenger follow-up: thresholds, falsifiers, strace opens.

Measures (a) the first-operand size at which each streaming head dies of -13,
(b) whether a -13 ever coexists with a later operand that WAS read (the
premise falsifier), (c) whether the input-count rule fires on worlds where
every operand was read, and (d) openat evidence for the later operand.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

LINE = 1024


def write_fixture(path, nbytes):
    k = nbytes // LINE
    with open(path, "wb") as f:
        f.write(b"alpha:" + b"a" * (LINE - 7) + b"\n")
        rest = k - 1
        chunk = (b"x" * (LINE - 1) + b"\n") * 512
        while rest > 0:
            n = min(rest, 512)
            f.write(chunk if n == 512 else chunk[: n * LINE])
            rest -= n
    assert os.path.getsize(path) == nbytes


def run(stages, cwd, errdir, stdin_path=None):
    procs, errpaths, prev = [], [], None
    for i, argv in enumerate(stages):
        stdin = prev
        if i == 0 and stdin_path is not None:
            stdin = open(stdin_path, "rb")
        ep = os.path.join(errdir, "s%d.err" % i)
        errpaths.append(ep)
        with open(ep, "wb") as ef:
            p = subprocess.Popen(argv, cwd=cwd, stdin=stdin,
                                 stdout=subprocess.PIPE, stderr=ef)
        if i == 0 and stdin_path is not None:
            stdin.close()
        if prev is not None:
            prev.close()
        prev = p.stdout
        procs.append(p)
    out, _ = procs[-1].communicate()
    for p in procs[:-1]:
        p.wait()
    errs = []
    for ep in errpaths:
        with open(ep, "rb") as f:
            errs.append(f.read(4000).decode("utf-8", "replace"))
    return [p.returncode for p in procs], out.decode("utf-8", "replace"), errs


def series(work, tag, stages, reps):
    rows = []
    for _ in range(reps):
        errdir = tempfile.mkdtemp(prefix="e-", dir=work)
        try:
            rcs, out, errs = run(stages, work, errdir)
        finally:
            shutil.rmtree(errdir, ignore_errors=True)
        rows.append({"rcs": rcs, "out_len": len(out), "out_head": out[:120].replace("\n", "\\n"),
                     "err": errs[0].replace("\n", "\\n")[:160]})
    rc0 = sorted({r["rcs"][0] for r in rows})
    return {"tag": tag, "argv": [" ".join(s) for s in stages], "reps": reps,
            "rc0_seen": rc0, "rc0_stable": len(rc0) == 1,
            "sigpipe_all": rc0 == [-13],
            "sigpipe_any": -13 in rc0,
            "err_mentions_missing_any": any("missing.txt" in r["err"] for r in rows),
            "err_mentions_missing_all": all("missing.txt" in r["err"] for r in rows),
            "rows": rows}


def main(argv):
    work, out_path = argv[0], argv[1]
    os.makedirs(work, exist_ok=True)
    M = os.path.join(work, "missing.txt")
    assert not os.path.exists(M)

    sizes = [524288, 589824, 655360, 720896, 786432, 851968, 917504, 983040, 1048576,
             2097152, 4194304]
    for n in sizes:
        p = os.path.join(work, "f-%d.txt" % n)
        if not os.path.exists(p):
            write_fixture(p, n)
    for n in (65536, 66560, 67584, 68608, 69632, 71680, 73728):
        p = os.path.join(work, "f-%d.txt" % n)
        if not os.path.exists(p):
            write_fixture(p, n)

    res = {"cat_threshold": [], "cut_threshold": [], "grep_threshold": [],
           "headall_threshold": [], "wc_falsifier": [], "rule_fires_on_read_world": [],
           "python_residual": [], "strace_opens": []}

    for n in sizes:
        F = os.path.join(work, "f-%d.txt" % n)
        res["cat_threshold"].append(series(work, "size=%d cat+missing" % n,
                                           [["cat", F, M], ["head", "-n", "1"]], 15))
    for n in (65536, 66560, 67584, 68608, 69632, 71680, 73728, 81920, 98304, 131072):
        F = os.path.join(work, "f-%d.txt" % n)
        res["cut_threshold"].append(series(work, "size=%d cut+missing" % n,
                                           [["cut", "-f1", "-d:", F, M], ["head", "-n", "1"]], 15))
        res["grep_threshold"].append(series(work, "size=%d grep-many+missing" % n,
                                            [["grep", "x", F, M], ["head", "-n", "1"]], 15))
        res["headall_threshold"].append(series(work, "size=%d head-all+missing" % n,
                                               [["head", "-n", "100000", F, M], ["head", "-n", "1"]], 15))

    for n in (65536, 1048576, 4194304):
        F = os.path.join(work, "f-%d.txt" % n)
        res["wc_falsifier"].append(series(work, "size=%d wc+missing" % n,
                                          [["wc", "-l", F, M], ["head", "-n", "1"]], 20))

    # worlds where EVERY operand exists: does the input-count rule fire anyway?
    for n in (1048576, 4194304):
        F = os.path.join(work, "f-%d.txt" % n)
        G = os.path.join(work, "g-%d.txt" % n)
        if not os.path.exists(G):
            write_fixture(G, n)
        for tag, argv in (("cat F G", ["cat", F, G]),
                          ("cut F G", ["cut", "-f1", "-d:", F, G]),
                          ("grep-many F G", ["grep", "x", F, G]),
                          ("sort F G", ["sort", F, G]),
                          ("tail-all F G", ["tail", "-n", "+1", F, G])):
            res["rule_fires_on_read_world"].append(series(work, "size=%d %s" % (n, tag),
                                                          [argv, ["head", "-n", "1"]], 7))

    # residual: python as a head (the "unknown head keeps the old benign rule" class)
    py = ["python3", "-B", "-c",
          "import sys\nfor i in range(200000): sys.stdout.write('y'*100+'\\n')"]
    res["python_residual"].append(series(work, "python flood", [py, ["head", "-n", "1"]], 7))

    # strace: did stage0 openat() the later operand?  (observational layer)
    for tag, n, argv in (
            ("cut+missing@4MiB", 4194304, ["cut", "-f1", "-d:", None, M]),
            ("cut+missing@64KiB", 65536, ["cut", "-f1", "-d:", None, M]),
            ("wc+missing@4MiB", 4194304, ["wc", "-l", None, M])):
        F = os.path.join(work, "f-%d.txt" % n)
        argv = [F if a is None else a for a in argv]
        log = os.path.join(work, "strace-%s.log" % tag.replace("@", "-").replace("+", "-"))
        wrapped = ["strace", "-f", "-qq", "-e", "trace=openat,exit_group",
                   "-o", log, "--"] + argv
        errdir = tempfile.mkdtemp(prefix="e-", dir=work)
        try:
            rcs, out, errs = run([wrapped, ["head", "-n", "1"]], work, errdir)
        finally:
            shutil.rmtree(errdir, ignore_errors=True)
        with open(log, "r", encoding="utf-8", errors="replace") as f:
            logtxt = f.read()
        res["strace_opens"].append({
            "tag": tag, "argv": argv, "rcs": rcs,
            "opens_missing": "missing.txt" in logtxt,
            "opens_first": ("f-%d.txt" % n) in logtxt,
            "log_lines": len(logtxt.splitlines()),
        })

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print("wrote", out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
