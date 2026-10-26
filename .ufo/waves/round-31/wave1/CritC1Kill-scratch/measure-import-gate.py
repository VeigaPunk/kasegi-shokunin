#!/usr/bin/env python3
"""Measure the import-time gate against the 13 landed ledger rows. CritC1Kill artifact.

For each row of corpus/instruments/limb-ledger.json: apply the exact find/replace to a
scratch copy of the instrument, then (a) import the mutant module (module-level code
runs, main() does not), and (b) run the row's own kill command and report whether the
signal survives and whether a traceback appears.

A gate "a mutant that fails to import is invalid:import, never killed" is non-breaking
for the landed ledger iff every landed row still imports cleanly.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
LEDGER = os.path.join(LANE, "corpus/instruments/limb-ledger.json")

IMPORT_PROBE = (
    "import importlib.util, sys\n"
    "spec = importlib.util.spec_from_file_location('crit_mutant', sys.argv[1])\n"
    "module = importlib.util.module_from_spec(spec)\n"
    "spec.loader.exec_module(module)\n"
    "print('IMPORT-OK')\n"
)


def run(cmd, cwd, env_extra=None):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if env_extra:
        env.update(env_extra)
    proc = subprocess.run(["bash", "-c", cmd], cwd=cwd, env=env,
                          capture_output=True, text=True, timeout=300)
    return proc.returncode, proc.stdout + proc.stderr


def main():
    ledger = json.load(open(LEDGER, encoding="utf-8"))
    scratch = tempfile.mkdtemp(prefix="crit-import-")
    rows = ledger["limbs"]
    print("rows=%d controls=%d" % (len(rows), len(ledger["controls"])))
    try:
        shutil.copytree(os.path.join(LANE, "corpus"), os.path.join(scratch, "corpus"))
        probe = os.path.join(scratch, ".crit-import-probe.py")
        open(probe, "w").write(IMPORT_PROBE)
        for row in rows:
            inst = row["instrument"]
            path = os.path.join(scratch, inst)
            original = open(path, "rb").read()
            text = original.decode("utf-8")
            assert text.count(row["find"]) == 1, row["id"]
            open(path, "wb").write(text.replace(row["find"], row["replace"], 1).encode())
            try:
                import_rc, import_out = run("python3 %s %s" % (probe, inst), scratch)
                live_cmd = row["kill"].replace("{inst}", inst).replace("{root}", scratch)
                mut_rc, mut_out = run(live_cmd, scratch)
                sig = re.search(row["signal"], mut_out, re.MULTILINE) is not None
                trace = "Traceback (most recent call last)" in mut_out
                print("%-26s import=%-3d %-11s mutant_exit=%-3s signal_survives=%-5s traceback=%s"
                      % (row["id"], import_rc, "IMPORT-OK" if "IMPORT-OK" in import_out else "FAIL",
                         mut_rc, sig, trace))
            finally:
                open(path, "wb").write(original)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
