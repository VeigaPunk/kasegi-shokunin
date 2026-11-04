#!/usr/bin/env python3
"""Replay the SAME critic counterfeits against an immutable prefreeze collector.

All generated fixtures/TMPDIR stay in owned scratch. Output is evidence about
these particular finite mutants, not a general anti-forgery/authenticity claim.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shlex
import shutil
import subprocess

BASE = "b6db9e818d322726e39cb441f2179d34d4170275"
OWN = Path(__file__).parent
SCRATCH = Path("/fast/scratch/hyaku/kasegi-r66/CriticCat")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--collector", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--label", required=True)
    args = ap.parse_args()
    SCRATCH.mkdir(parents=True, exist_ok=True)
    (SCRATCH / "tmp").mkdir(exist_ok=True)
    receipts = OWN / "receipts"
    collector = OWN / ("collector-" + args.label + ".py")
    candidate = OWN / ("candidate-" + args.label + ".py")
    shutil.copyfile(args.collector, collector)
    shutil.copyfile(args.candidate, candidate)
    env = {**os.environ, "TMPDIR": str(SCRATCH / "tmp"),
           "HYAKU_SCRATCH": str(SCRATCH / "tmp"), "PYTHONDONTWRITEBYTECODE": "1"}
    controls = [("id-oracle", OWN / "id-oracle.py", {}, 1),
                ("path-oracle", OWN / "path-oracle.py", {}, 1),
                ("text-oracle", OWN / "text-oracle.py", {}, 1),
                ("always-green", OWN / "text-oracle.py", {"ORACLE_ALWAYS_GREEN": "1"}, 1),
                ("always-stale", OWN / "stale-oracle.py", {}, 1),
                ("real-candidate", candidate, {}, 0)]
    rows = []
    failed = 0
    for name, instrument, extra, expected_rc in controls:
        work = SCRATCH / ("w-" + secrets.token_hex(6))
        command = ["python3", "-B", str(collector), "--instrument", str(instrument),
                   "--work", str(work), "--mode", "candidate"]
        proc = subprocess.run(command, cwd=SCRATCH, env={**env, **extra},
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=240)
        text = proc.stdout.decode("utf-8", "replace")
        summary = re.findall(r"^PROBES probes=(\d+) failures=(\d+) mode=candidate .*", text, re.M)
        ok = (proc.returncode == expected_rc and len(summary) == 1 and
              ((int(summary[0][1]) == 0) if expected_rc == 0 else (int(summary[0][1]) > 0)))
        row = {"name": name, "base": BASE, "base_gate_sha256": sha(OWN / "base-gate.py"),
               "collector_sha256": sha(collector), "instrument_sha256": sha(instrument),
               "harness_sha256": sha(Path(__file__)), "command": command, "cwd": str(SCRATCH),
               "extra_environment": extra, "TMPDIR": env["TMPDIR"],
               "expected_rc": expected_rc, "rc": proc.returncode, "stdout": text,
               "stderr": proc.stderr.decode("utf-8", "replace"),
               "summary": summary, "finite_control_matches": ok, "cases": []}
        cases_path = work / "cases"
        if cases_path.exists():
            for case in sorted(cases_path.iterdir()):
                files = []
                for path in sorted(case.rglob("*")):
                    if not path.is_file():
                        continue
                    entry = {"path": str(path.relative_to(case)), "bytes": path.stat().st_size,
                             "sha256": sha(path)}
                    if path.name in ("one.json", "gate.stdout", "gate.stderr"):
                        entry["content"] = path.read_text()
                    files.append(entry)
                row["cases"].append({"case": case.name, "files": files})
        (receipts / (args.label + "-" + name + ".json")).write_text(json.dumps(row, indent=2) + "\n")
        (receipts / (args.label + "-" + name + ".txt")).write_text(
            "$ " + shlex.join(command) + "\nBASE=" + BASE + "\ncollector_sha256=" + row["collector_sha256"] +
            "\ninstrument_sha256=" + row["instrument_sha256"] + "\n" + text +
            "\nstderr:\n" + row["stderr"] + "\nrc=" + str(proc.returncode) + "\n")
        rows.append({k: row[k] for k in ("name", "collector_sha256", "instrument_sha256", "expected_rc", "rc", "summary", "finite_control_matches")})
        failed += int(not ok)
        print("CONTROL %s rc=%d expected=%d summary=%s match=%s" % (name, proc.returncode, expected_rc, summary, ok))
    (OWN / (args.label + "-summary.json")).write_text(json.dumps({"base": BASE, "collector_sha256": sha(collector),
        "candidate_sha256": sha(candidate), "controls": rows, "failed": failed}, indent=2) + "\n")
    print("FINITE-CONTROLS controls=%d failures=%d" % (len(rows), failed))
    return int(failed > 0)


if __name__ == "__main__":
    raise SystemExit(main())
