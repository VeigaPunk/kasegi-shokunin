#!/usr/bin/env python3
"""imp.py MODE TARGET FIXTURE [TMPDIR] -- in-process witness helper for MutC1Hunt.

MODE=leak            run selftest(), report which module/process state it restored.
MODE=timeout         census() over a sleep fixture with TIMEOUT patched to 1 (sentinel witness).
MODE=timeout-default census() over a sleep fixture with the shipped TIMEOUT.
MODE=grid            conform_ok() over a deterministic counts grid; prints the verdict vector.
The last stdout line is JSON; selftest/census chatter is swallowed.
"""
import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import time


def load(target):
    spec = importlib.util.spec_from_file_location("cand", target)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    mode, target, fixture = argv[0], argv[1], argv[2]
    mod = load(target)
    out = {}
    if mode == "leak":
        start = os.getcwd()
        real_mkdtemp = tempfile.mkdtemp
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = mod.selftest()
        try:
            cwd = os.getcwd()
        except OSError as exc:
            cwd = "ERR:%d" % exc.errno
        out = {
            "rc": rc,
            "run_foreign_restored": getattr(mod.run_foreign, "__name__", "?") == "run_foreign",
            "selftest_restored": getattr(mod.selftest, "__name__", "?") == "selftest",
            "timeout": mod.TIMEOUT,
            "mkdtemp_restored": tempfile.mkdtemp is real_mkdtemp,
            "cwd_restored": cwd == start,
        }
    elif mode in ("timeout", "timeout-default"):
        if mode == "timeout":
            mod.TIMEOUT = 1
        buf = io.StringIO()
        started = time.time()
        with contextlib.redirect_stdout(buf):
            counts = mod.census(fixture, fixture, True)
        elapsed = round(time.time() - started, 1)
        entries = [ln for ln in buf.getvalue().splitlines() if ln.startswith("ENTRY ")]
        out = {"entry": entries[0] if entries else None,
               "exit0_foreign": counts["exit0_foreign"],
               "exit_other": counts["exit_other"],
               "sleep_took_ge_2s": elapsed >= 2.0}
    elif mode == "grid":
        grid = []
        for noprefix in (0, 1, 2):
            for exit2 in (0, 1, 2):
                for exit0 in (0, 1, 2):
                    for exit1 in (0, 1, 2):
                        for other in (0, 1, 2):
                            entries = noprefix + exit2 + exit0 + exit1 + other
                            grid.append({
                                "entries": entries, "noprefix": noprefix,
                                "exit2_foreign": exit2, "exit0_foreign": exit0,
                                "exit1_foreign": exit1, "exit_other": other,
                                "norecheck": 0, "restoration_only": 0})
        for norecheck in (0, 1, 2):
            for restoration in (0, 1, 2):
                grid.append({
                    "entries": norecheck + restoration, "noprefix": 0,
                    "exit2_foreign": 0, "exit0_foreign": 0, "exit1_foreign": 0,
                    "exit_other": 0, "norecheck": norecheck,
                    "restoration_only": restoration})
        out = {"verdicts": [mod.conform_ok(c) for c in grid], "n": len(grid)}
    print(json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
