#!/usr/bin/env python3
"""kasegi round-67 revenger probe: multi-head SIGPIPE input-completeness.

Question: on this host, which read-only heads can be SIGPIPE'd before reaching a
later named operand, and does the required first-operand size matter?

Never a shell: every pipeline stage is an argv list started with subprocess.
Every measurement is repeated; a single repeat is never treated as stable.
"""
import argparse
import fcntl
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile

LINE = 1024


def write_fixture(path, nbytes):
    """nbytes = k*1024.  Line 1 is 'alpha:' + 'a'*1017, lines 2..k are 'x'*1023.
    Every line is exactly 1024 bytes, so grep x matches all lines, grep alpha
    matches exactly one, and cut -f1 -d: yields 'alpha' then 'x'*1023."""
    k = nbytes // LINE
    assert k * LINE == nbytes
    with open(path, "wb") as f:
        f.write(b"alpha:" + b"a" * (LINE - 7) + b"\n")
        chunk = (b"x" * (LINE - 1) + b"\n") * min(k - 1, 512)
        rest = k - 1
        while rest > 0:
            n = min(rest, 512)
            f.write(chunk if n == 512 else chunk[: n * LINE])
            rest -= n
    assert os.path.getsize(path) == nbytes, (path, os.path.getsize(path), nbytes)


def run_pipeline(stages, cwd, stdin_path, errdir):
    """Return per-stage returncodes plus stage-0 stderr text.  No shell."""
    procs, errpaths = [], []
    prev = None
    prev_file = None
    for i, argv in enumerate(stages):
        stdin = prev
        if i == 0 and stdin_path is not None:
            stdin = open(stdin_path, "rb")
        ep = os.path.join(errdir, "stage%d.err" % i)
        errpaths.append(ep)
        ef = open(ep, "wb")
        p = subprocess.Popen(argv, cwd=cwd, stdin=stdin,
                             stdout=subprocess.PIPE, stderr=ef)
        ef.close()
        if i == 0 and stdin_path is not None:
            stdin.close()
        if prev is not None:
            prev.close()
        prev = p.stdout
        procs.append(p)
    out, _ = procs[-1].communicate()
    for p in procs[:-1]:
        p.wait()
    rcs = [p.returncode for p in procs]
    errs = []
    for ep in errpaths:
        with open(ep, "rb") as f:
            errs.append(f.read(4000).decode("utf-8", "replace"))
    return rcs, out, errs


def head_of(stages):
    return os.path.basename(stages[0][0])


def shapes(F, M):
    """(name, stages, stdin_path).  F = first operand path, M = missing path."""
    return [
        ("cat",        [["cat", F], ["head", "-n", "1"]], None),
        ("cat+missing",[["cat", F, M], ["head", "-n", "1"]], None),
        ("cut",        [["cut", "-f1", "-d:", F], ["head", "-n", "1"]], None),
        ("cut+missing",[["cut", "-f1", "-d:", F, M], ["head", "-n", "1"]], None),
        ("wc",         [["wc", "-l", F], ["head", "-n", "1"]], None),
        ("wc+missing", [["wc", "-l", F, M], ["head", "-n", "1"]], None),
        ("grep-many",  [["grep", "x", F], ["head", "-n", "1"]], None),
        ("grep-many+missing", [["grep", "x", F, M], ["head", "-n", "1"]], None),
        ("grep-few",   [["grep", "alpha", F], ["head", "-n", "1"]], None),
        ("grep-few+missing", [["grep", "alpha", F, M], ["head", "-n", "1"]], None),
        ("sort",       [["sort", F], ["head", "-n", "1"]], None),
        ("sort+missing", [["sort", F, M], ["head", "-n", "1"]], None),
        ("head-n5",    [["head", "-n", "5", F], ["head", "-n", "1"]], None),
        ("head-n5+missing", [["head", "-n", "5", F, M], ["head", "-n", "1"]], None),
        ("head-all",   [["head", "-n", "100000", F], ["head", "-n", "1"]], None),
        ("head-all+missing", [["head", "-n", "100000", F, M], ["head", "-n", "1"]], None),
        ("tail",       [["tail", F], ["head", "-n", "1"]], None),
        ("tail+missing", [["tail", F, M], ["head", "-n", "1"]], None),
        ("tail-all",   [["tail", "-n", "+1", F], ["head", "-n", "1"]], None),
        ("tail-all+missing", [["tail", "-n", "+1", F, M], ["head", "-n", "1"]], None),
        ("sha256sum",  [["sha256sum", F], ["head", "-n", "1"]], None),
        ("sha256sum+missing", [["sha256sum", F, M], ["head", "-n", "1"]], None),
        ("ls",         [["ls", F], ["head", "-n", "1"]], None),
        ("ls+missing", [["ls", F, M], ["head", "-n", "1"]], None),
        # tr has no file operands: one extra argv token is already an extra operand.
        ("tr-stdin-stream", [["tr", "a", "b"], ["head", "-n", "1"]], F),
        ("tr-one-arg", [["tr", "a"], ["head", "-n", "1"]], F),
        ("tr-file-operand", [["tr", "a", "b", F], ["head", "-n", "1"]], None),
        ("tr-two-file-operands", [["tr", "a", "b", F, M], ["head", "-n", "1"]], None),
        ("cat|tr",     [["cat", F, M], ["tr", "a", "b"], ["head", "-n", "1"]], None),
    ]


def one(work, stages, stdin_path, reps, tag):
    runs = []
    for _ in range(reps):
        errdir = tempfile.mkdtemp(prefix="err-", dir=work)
        try:
            rcs, out, errs = run_pipeline(stages, work, stdin_path, errdir)
        finally:
            shutil.rmtree(errdir, ignore_errors=True)
        runs.append({
            "rcs": rcs,
            "stdout_head": out[:200].decode("utf-8", "replace"),
            "stdout_bytes": len(out),
            "stage0_stderr": errs[0][:400],
            "stage0_stderr_mentions_missing": "missing.txt" in errs[0],
        })
    stage0 = sorted({r["rcs"][0] for r in runs})
    return {
        "tag": tag,
        "head": head_of(stages),
        "argv": [" ".join(s) for s in stages],
        "stdin_file": stdin_path is not None,
        "reps": reps,
        "stage0_rcs_seen": stage0,
        "stage0_rc_stable": len(stage0) == 1,
        "stage0_rc": stage0[0] if len(stage0) == 1 else stage0,
        "stage1_rcs_seen": sorted({r["rcs"][1] for r in runs}),
        "stage0_stderr_mentions_missing": sorted({r["stage0_stderr_mentions_missing"] for r in runs}),
        "stage0_stderr_example": runs[0]["stage0_stderr"].replace("\n", "\\n")[:200],
        "stdout_head_example": runs[0]["stdout_head"].replace("\n", "\\n")[:80],
        "stdout_bytes": sorted({r["stdout_bytes"] for r in runs}),
        "runs": runs,
    }


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--reps", type=int, default=7)
    a = ap.parse_args(argv)
    os.makedirs(a.work, exist_ok=True)
    main_sizes = [65536, 1048576, 4194304]
    sweep_sizes = [65536, 66560, 69632, 73728, 81920, 98304, 131072, 262144, 524288,
                   1048576, 2097152, 4194304]
    sweep_shapes = {"cat+missing", "cut+missing", "grep-many+missing", "wc+missing",
                    "tail-all+missing", "head-all+missing", "cat|tr"}

    pipe_sz = fcntl.fcntl(0, 1032) if False else None  # placeholder, real read below
    try:
        r, w = os.pipe()
        pipe_sz = fcntl.fcntl(w, 1032)  # F_GETPIPE_SZ on Linux
        os.close(r); os.close(w)
    except OSError:
        pass

    fixtures = {}
    for n in sorted(set(main_sizes + sweep_sizes)):
        p = os.path.join(a.work, "f-%d.txt" % n)
        if not os.path.exists(p):
            write_fixture(p, n)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        fixtures[str(n)] = {"path": p, "bytes": os.path.getsize(p), "sha256": h,
                            "lines": n // LINE}

    missing = os.path.join(a.work, "missing.txt")
    assert not os.path.exists(missing), "missing.txt must not exist"

    results = {"pipe_capacity": pipe_sz, "fixtures": fixtures,
               "missing_operand": {"path": missing, "exists": os.path.exists(missing)},
               "host": {"python": sys.version.split()[0]},
               "main": [], "sweep": []}

    for n in main_sizes:
        F = os.path.join(a.work, "f-%d.txt" % n)
        for name, stages, stdin_path in shapes(F, missing):
            results["main"].append(one(a.work, stages, stdin_path, a.reps, "size=%d %s" % (n, name)))

    for n in sweep_sizes:
        F = os.path.join(a.work, "f-%d.txt" % n)
        for name, stages, stdin_path in shapes(F, missing):
            if name not in sweep_shapes:
                continue
            results["sweep"].append(one(a.work, stages, stdin_path, 5, "size=%d %s" % (n, name)))

    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1, sort_keys=True)
    print("wrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
