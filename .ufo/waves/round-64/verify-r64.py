#!/usr/bin/env python3
"""Finite r64 committed-input replay: 0 pass, 1 mismatch, 2 setup.
Construction may overlay --candidate; --final refuses that and enforces frozen hashes.
Historical Git objects use a local gitdir pointer: host-bound, not hermetic.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

BASE = "d74be00a82c8c2962a0b78442c5daea3af0adaae"
PREFIX = ".ufo/waves/round-64/"
COLLECTOR = PREFIX + "w1/ExecCollector/c1-probes-r64.py"
BATTERY = PREFIX + "w1/ExecMutants/figure-audit-mutbat-r64.py"
EXPECTED_CASES = 59
PATHS = (
    "corpus/instruments/figure-audit.py",
    "corpus/instruments/figure-audit-ledger.json",
    "corpus/instruments/figure-audit-mutbat.py",
    "corpus/source-snapshots/round-54/S086.txt",
    ".ufo/waves/round-55/controls/gate-final-r55.txt",
    ".ufo/waves/round-56/controls/df3-fixedpoint-r55tip.txt",
    ".ufo/waves/round-53/controls/c2-counter-final-r53.txt",
    ".ufo/waves/round-56/controls/gate-final-r56.txt",
    COLLECTOR, BATTERY,
)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--work", required=True, type=Path)
    ap.add_argument("--candidate", type=Path)
    ap.add_argument("--final", action="store_true")
    args = ap.parse_args()
    lane = Path(__file__).resolve().parents[3]
    try:
        if args.final and args.candidate:
            raise ValueError("final-refuses-construction-override")
        work = args.work.resolve()
        if not work.is_relative_to(Path("/fast/scratch/hyaku/kasegi-r64")) or len(work.parts) < 7:
            raise ValueError("work-not-owned")
        work.mkdir(parents=True, exist_ok=True)

        def blob(rev, name):
            return subprocess.check_output(["git", "-C", str(lane), "show", rev + ":" + name])

        revision = subprocess.check_output(["git", "-C", str(lane), "rev-parse", "--verify", args.revision + "^{commit}"], text=True).strip()
        gitdir = subprocess.check_output(["git", "-C", str(lane), "rev-parse", "--absolute-git-dir"], text=True).strip()
        pins = json.loads(blob(revision, PREFIX + "claims.json"))["input_sha256"] if args.final else None
        driver_data = blob(revision, PREFIX + "verify-r64.py")
        if Path(__file__).read_bytes() != driver_data:
            raise ValueError("driver-not-committed-bytes")
        if pins and hashlib.sha256(driver_data).hexdigest() != pins[PREFIX + "verify-r64.py"]:
            raise ValueError("driver-pin-mismatch")
        print("run-utc=" + datetime.datetime.now(datetime.timezone.utc).isoformat(), flush=True)
        print("measured-revision=" + revision, flush=True)
        print("construction-override=" + str(args.candidate is not None), flush=True)
        print("host-bound-git-replay=true GIT_NO_REPLACE_OBJECTS=1", flush=True)
        with tempfile.TemporaryDirectory(prefix="committed-", dir=work) as temporary:
            root = Path(temporary)
            for name in PATHS:
                data = blob(revision, name)
                digest = hashlib.sha256(data).hexdigest()
                if pins and digest != pins[name]:
                    raise ValueError("input-pin-mismatch:" + name)
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                print("INPUT " + name + " sha256=" + digest, flush=True)
            instrument = root / PATHS[0]
            if args.candidate:
                data = args.candidate.read_bytes()
                instrument.write_bytes(data)
                print("CANDIDATE sha256=" + hashlib.sha256(data).hexdigest(), flush=True)
            base_instrument = root / "base.py"
            base_data = blob(BASE, PATHS[0])
            base_instrument.write_bytes(base_data)
            print("BASE " + BASE + " sha256=" + hashlib.sha256(base_data).hexdigest(), flush=True)
            (root / ".git").write_text("gitdir: " + gitdir + "\n")
            scratch = root / "scratch"
            scratch.mkdir()
            env = dict(os.environ, TMPDIR=str(scratch), HYAKU_SCRATCH=str(scratch),
                       PYTHONDONTWRITEBYTECODE="1", GIT_NO_REPLACE_OBJECTS="1")
            py = sys.executable

            def collect(path, mode, child):
                return [py, str(root / COLLECTOR), "--instrument", str(path),
                        "--work", str(work / child), "--mode", mode]

            tasks = (
                ("collector", collect(instrument, "candidate", "collector"), 0,
                 "HARNESS probes=18 failures=0 mode=candidate"),
                ("paired-base", collect(base_instrument, "candidate", "paired-base"), 1,
                 "HARNESS probes=18 failures=7 mode=candidate"),
                ("collector-selfcheck", [py, str(root / COLLECTOR), "--instrument", str(base_instrument),
                 "--work", str(work / "selfcheck"), "--selfcheck"], 0,
                 "HARNESS selfcheck cases=9 failures=0"),
                ("selftest", [py, str(instrument), "--selftest"], 0,
                 "selftest cases=59 failures=0"),
                ("old-mutbat", [py, str(root / PATHS[2]), "--instrument", str(instrument)], 0,
                 "mutbat killed=5/5 survivors=0 invalid=0 controls=pass"),
                ("new-mutbat-and-trees", [py, str(root / BATTERY), "--instrument", str(instrument),
                 "--work", str(work / "battery")], 0,
                 "mutbat-r64 pristine=pass limbs=thresh:3,grep:3,neg:3,precedence:3 equivalents_held=2 controls_held=1 invalid_rejected=2 failures=0 verdict=pass"),
                ("real-ledger", [py, str(instrument)], 0,
                 "FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0"),
            )
            failures = 0
            for name, argv, expected_rc, expected in tasks:
                print("RUN " + name + " argv=" + json.dumps(argv), flush=True)
                result = subprocess.run(argv, cwd=root, env=env, stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, text=True, timeout=600)
                print(result.stdout, end="" if result.stdout.endswith("\n") else "\n", flush=True)
                lines = result.stdout.splitlines()
                good = result.returncode == expected_rc and lines.count(expected) == 1
                if name == "selftest":
                    cases = [line for line in lines if line.startswith("selftest case=")]
                    good = good and len(cases) == EXPECTED_CASES and all(line.endswith("verdict=pass") for line in cases)
                failures += not good
                print(f"RESULT {name} exit={result.returncode} verdict={'PASS' if good else 'FAIL'}", flush=True)
            print(f"VERIFY measurements={len(tasks)} failures={failures} revision={revision}", flush=True)
            return int(bool(failures))
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print(f"VERIFY-ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
