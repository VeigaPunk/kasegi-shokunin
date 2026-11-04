#!/usr/bin/env python3
"""Finite r65 committed-input replay: predata signal-fail-closed gate (claim C1).

Construction may overlay --candidate; --final refuses that and enforces the
frozen input hashes recorded in .ufo/waves/round-65/claims.json. Eight
enumerated measurements, each printing RESULT <name> PASS|FAIL and a closing
VERIFY measurements=8 failures=<n> revision=<rev> line (exit 1 on any failure,
2 on setup error). Before the candidate exists the driver stays usable:
measurement 2 fails by measuring the limbless committed tree under candidate
expectations, measurements 4 and 6 fail closed without running.

The committed tree at --revision is exported with git archive into --work; a
shared lane checkout is only read through `git`. Historical Git objects use a
local gitdir pointer: host-bound, not hermetic.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = "a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b"
PREFIX = ".ufo/waves/round-65/"
GATE = "corpus/instruments/figure-audit.py"
LEDGER = "corpus/instruments/figure-audit-ledger.json"
MUTBAT = "corpus/instruments/figure-audit-mutbat.py"
COLLECTOR = PREFIX + "w1/ExecSignalProbes/c1-signal-probes.py"
BATTERY = PREFIX + "w1/ExecSignalMutants/signal-mutbat.py"
DRIVER = PREFIX + "verify-r65.py"
PINS_SOURCE = PREFIX + "claims.json"
PATHS = (GATE, LEDGER, MUTBAT, COLLECTOR, BATTERY)
WORK_FLOOR = Path("/fast/scratch/hyaku/kasegi-r65")
MIN_SELFTEST_CASES = 59
PROBES_SUMMARY = "PROBES probes=6 failures=0"
# Base expectations on the base gate are the documented false green: the base
# gate flags only the final-stage signal (P3) and swallows the upstream
# signals (P1/P2), so base mode reports exactly one mismatch.
PROBES_BASE_SUMMARY = "PROBES probes=6 failures=1"
SELFCHECK_SUMMARY = "SELFCHECK probes=6 runs=2 failures=6 want=6 verdict=pass"
OLD_MUTBAT_SUMMARY = "mutbat killed=5/5 survivors=0 invalid=0 controls=pass"
LEDGER_SUMMARY = "FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0"
MUTBAT_SUMMARY_RE = r"SUMMARY killed=([0-9]+)/\1 survivors=0 equivalents_held=2 controls_held=1 invalid_rejected=1"
MUTBAT_VERDICT_RE = r"verdict limb-verified limb=\S+ limb_contract=pass"
SELFTEST_SUMMARY_RE = r"selftest cases=([0-9]+) failures=0"
TIMEOUT = 600

ALWAYS_GREEN_STUB = """import argparse, json, sys
ap = argparse.ArgumentParser()
ap.add_argument("--ledger", required=True)
ap.add_argument("--root", required=True)
args = ap.parse_args()
with open(args.ledger) as handle:
    figs = json.load(handle)["figures"]
for fig in figs:
    print("FIG %s recorded=%s derived=%s ok" % (fig["id"], fig["recorded"], fig["want"]))
print("FIGURE-AUDIT figures=%d ok=%d stale=0 exit=0" % (len(figs), len(figs)))
"""

REPLAY_STUB = """import argparse, json, sys
REPLAY = __REPLAY__
ap = argparse.ArgumentParser()
ap.add_argument("--ledger", required=True)
ap.add_argument("--root", required=True)
args = ap.parse_args()
with open(args.ledger) as handle:
    figs = json.load(handle)["figures"]
sys.stdout.write(REPLAY[figs[0]["id"]])
sys.exit(0)
"""


def find_lane():
    """The driver runs as a w1 draft or committed at the round root; the lane is
    the first ancestor that carries the production gate."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "corpus" / "instruments" / "figure-audit.py").is_file():
            return parent
    raise ValueError("lane-not-found")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--work", type=Path)
    ap.add_argument("--candidate", type=Path)
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--print-inputs", action="store_true")
    args = ap.parse_args()
    try:
        if args.final and args.candidate:
            raise ValueError("final-refuses-construction-override")
        if not args.print_inputs:
            if args.work is None:
                raise ValueError("work-required")
            work = args.work.resolve()
            if not work.is_relative_to(WORK_FLOOR) or len(work.parts) < 7:
                raise ValueError("work-not-owned")
            work.mkdir(parents=True, exist_ok=True)
        lane = find_lane()

        def git(*argv, check=True):
            return subprocess.run(["git", "-C", str(lane)] + list(argv), check=check,
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

        def blob(rev, name):
            done = git("show", rev + ":" + name, check=False)
            return done.stdout if done.returncode == 0 else None

        revision = git("rev-parse", "--verify", args.revision + "^{commit}").stdout.decode().strip()
        if args.print_inputs:
            print("measured-revision=" + revision, flush=True)
            for name in PATHS + (DRIVER, PINS_SOURCE):
                data = blob(revision, name)
                if data is None:
                    print("INPUT-MISSING " + name, flush=True)
                else:
                    print("INPUT " + name + " sha256=" + sha256_bytes(data), flush=True)
            print("DRIVER committed=" + ("yes" if blob(revision, DRIVER) is not None else "no"), flush=True)
            return 0

        gitdir = git("rev-parse", "--absolute-git-dir").stdout.decode().strip()
        pins = None
        if args.final:
            pins_data = blob(revision, PINS_SOURCE)
            if pins_data is None:
                raise ValueError("pins-missing-at-revision")
            pins = json.loads(pins_data)["input_sha256"]
        driver_data = blob(revision, DRIVER)
        if driver_data is None:
            if args.final:
                raise ValueError("driver-not-committed-at-revision")
            print("DRIVER committed=no predata-trial", flush=True)
        else:
            if Path(__file__).read_bytes() != driver_data:
                raise ValueError("driver-not-committed-bytes")
            if pins and sha256_bytes(driver_data) != pins[DRIVER]:
                raise ValueError("driver-pin-mismatch")
            print("DRIVER committed=yes sha256=" + sha256_bytes(driver_data), flush=True)
        print("run-utc=" + datetime.datetime.now(datetime.timezone.utc).isoformat(), flush=True)
        print("measured-revision=" + revision, flush=True)
        print("construction-override=" + str(args.candidate is not None), flush=True)
        print("final=" + str(args.final), flush=True)
        print("host-bound-git-replay=true GIT_NO_REPLACE_OBJECTS=1", flush=True)
        with tempfile.TemporaryDirectory(prefix="committed-", dir=work) as temporary:
            root = Path(temporary)
            missing = set()
            for name in PATHS:
                data = blob(revision, name)
                if data is None:
                    missing.add(name)
                    print("INPUT-MISSING " + name, flush=True)
                    continue
                digest = sha256_bytes(data)
                if pins and digest != pins[name]:
                    raise ValueError("input-pin-mismatch:" + name)
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                print("INPUT " + name + " sha256=" + digest, flush=True)
            archive = root / "tree.tar"
            with open(archive, "wb") as handle:
                subprocess.run(["git", "-C", str(lane), "archive", "--format=tar", revision],
                               stdout=handle, check=True)
            subprocess.run(["tar", "-xf", str(archive), "-C", str(root)], check=True)
            archive.unlink()
            print("EXPORT revision=" + revision + " via=git-archive", flush=True)
            instrument = root / GATE
            if args.candidate:
                data = args.candidate.read_bytes()
                instrument.write_bytes(data)
                print("CANDIDATE sha256=" + sha256_bytes(data), flush=True)
            base_data = blob(BASE, GATE)
            if base_data is None:
                raise ValueError("base-gate-missing")
            base_gate = root / "base.py"
            base_gate.write_bytes(base_data)
            print("BASE " + BASE + " sha256=" + sha256_bytes(base_data), flush=True)
            (root / ".git").write_text("gitdir: " + gitdir + "\n")
            scratch = root / "scratch"
            scratch.mkdir()
            env = dict(os.environ, TMPDIR=str(scratch), HYAKU_SCRATCH=str(scratch),
                       PYTHONDONTWRITEBYTECODE="1", GIT_NO_REPLACE_OBJECTS="1")
            py = sys.executable
            collector = root / COLLECTOR
            battery = root / BATTERY

            def summary_once(lines, text):
                return lines.count(text) == 1

            def regex_once(lines, pattern):
                return sum(1 for line in lines if re.fullmatch(pattern, line)) == 1

            failures = 0

            def conclude(name, good, reason):
                nonlocal failures
                if not good and reason:
                    print("FAIL-REASON %s %s" % (name, reason), flush=True)
                failures += not good
                print("RESULT %s %s" % (name, "PASS" if good else "FAIL"), flush=True)

            def child(argv, label=None):
                if label:
                    print("RUN %s argv=%s" % (label, json.dumps(argv)), flush=True)
                done = subprocess.run(argv, cwd=root, env=env, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT, text=True, timeout=TIMEOUT)
                print(done.stdout, end="" if done.stdout.endswith("\n") else "\n", flush=True)
                return done

            def collector_run(label, instrument_path, mode, child_work):
                return child([py, str(collector), "--instrument", str(instrument_path),
                              "--work", str(child_work), "--mode", mode], label)

            # 1 collector-base: six-probe collector, base expectations, the
            # production gate pinned at the round base. The pinned expectation
            # is the documented false green: only P3 stale, P1/P2 swallowed.
            if COLLECTOR in missing:
                conclude("collector-base", False, "missing-committed-input:" + COLLECTOR)
            else:
                done = collector_run("collector-base", base_gate, "base", work / "collector-base")
                lines = done.stdout.splitlines()
                good = done.returncode == 1 and summary_once(lines, PROBES_BASE_SUMMARY)
                conclude("collector-base", good, None if good else "base-false-green-anchor-violated")

            # 2 candidate-collector: the after-state measurement. Reads the
            # overlay when given, else the committed tree itself, under
            # candidate expectations: it must FAIL while the tree lacks the limb.
            if COLLECTOR in missing:
                conclude("candidate-collector", False, "missing-committed-input:" + COLLECTOR)
            else:
                done = collector_run("candidate-collector", instrument, "candidate",
                                     work / "collector-candidate")
                lines = done.stdout.splitlines()
                good = done.returncode == 0 and summary_once(lines, PROBES_SUMMARY)
                conclude("candidate-collector", good, None if good else "limb-absent-or-not-fail-closed")

            # 3 collector-selfcheck: always-green stub must yield failures=6.
            if COLLECTOR in missing:
                conclude("collector-selfcheck", False, "missing-committed-input:" + COLLECTOR)
            else:
                done = child([py, str(collector), "--work", str(work / "selfcheck"), "--selfcheck"],
                             "collector-selfcheck")
                lines = done.stdout.splitlines()
                good = done.returncode == 0 and summary_once(lines, SELFCHECK_SUMMARY)
                conclude("collector-selfcheck", good, None if good else "selfcheck-not-fail-closed")

            # 4 selftest: the candidate selftest exits 0 with failures=0 and no
            # dropped cases. Without an overlay (predata trial) it fails closed.
            if not args.candidate and not args.final:
                conclude("selftest", False, "candidate-overlay-absent")
            else:
                done = child([py, str(instrument), "--selftest"], "selftest")
                lines = done.stdout.splitlines()
                sums = [re.fullmatch(SELFTEST_SUMMARY_RE, line) for line in lines]
                sums = [match for match in sums if match]
                cases = [line for line in lines if line.startswith("selftest case=")]
                pins_bad = [line for line in lines if line.startswith("selftest pin ")
                            and line.endswith("verdict=fail")]
                good = (done.returncode == 0 and len(sums) == 1
                        and int(sums[0].group(1)) >= MIN_SELFTEST_CASES
                        and all(line.endswith("verdict=pass") for line in cases)
                        and len(cases) == int(sums[0].group(1)) and not pins_bad)
                conclude("selftest", good, None if good else "selftest-not-green")

            # 5 old-mutbat: the committed five-mutant battery still kills its
            # mutants on the measured instrument.
            done = child([py, str(root / MUTBAT), "--instrument", str(instrument)], "old-mutbat")
            lines = done.stdout.splitlines()
            good = done.returncode == 0 and summary_once(lines, OLD_MUTBAT_SUMMARY)
            conclude("old-mutbat", good, None if good else "battery-not-green")

            # 6 signal-mutbat-and-equivalents: the round's battery kills the
            # signal-limb mutants, holds both equivalents, rejects the invalid
            # control. Without an overlay (predata trial) it fails closed.
            if not args.candidate and not args.final:
                conclude("signal-mutbat-and-equivalents", False, "candidate-overlay-absent")
            elif BATTERY in missing:
                conclude("signal-mutbat-and-equivalents", False, "missing-committed-input:" + BATTERY)
            else:
                done = child([py, str(battery), "--instrument", str(instrument),
                              "--work", str(work / "battery")], "signal-mutbat-and-equivalents")
                lines = done.stdout.splitlines()
                good = (done.returncode == 0 and regex_once(lines, MUTBAT_SUMMARY_RE)
                        and regex_once(lines, MUTBAT_VERDICT_RE))
                conclude("signal-mutbat-and-equivalents", good,
                         None if good else "limb-not-verified")

            # 7 collector-forgeries: a forged receipt (the base gate's honest
            # false-green transcript, replayed keyed by probe id) and an
            # always-green counterfeit are both rejected by the collector's own
            # mode comparison.
            if COLLECTOR in missing:
                conclude("collector-forgeries", False, "missing-committed-input:" + COLLECTOR)
            else:
                good, reason = forgeries(py, collector, base_gate, root, work,
                                         child, summary_once)
                conclude("collector-forgeries", good, reason)

            # 8 real-ledger: the 35-figure production ledger audits clean.
            done = child([py, str(instrument)], "real-ledger")
            lines = done.stdout.splitlines()
            good = done.returncode == 0 and summary_once(lines, LEDGER_SUMMARY)
            conclude("real-ledger", good, None if good else "ledger-not-clean")

            print("VERIFY measurements=8 failures=%d revision=%s" % (failures, revision), flush=True)
            return int(bool(failures))
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print("VERIFY-ERROR %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        return 2


def forgeries(py, collector, base_gate, root, work, child, summary_once):
    """Capture the base gate's honest per-probe transcripts with the collector's
    own fixture builders, then present two fabricated instruments to the
    collector under candidate expectations."""
    try:
        spec = importlib.util.spec_from_file_location("c1_signal_probes_r65", collector)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except (OSError, SyntaxError, ValueError) as exc:
        return False, "collector-unimportable:%s" % type(exc).__name__
    capture = work / "forgeries"
    fixture_root = capture / "root"
    ledgers = capture / "ledgers"
    ledgers.mkdir(parents=True, exist_ok=True)
    module.build_fixtures(str(fixture_root))
    replay = {}
    for probe in module.PROBES:
        ledger_path = module.write_ledger(str(ledgers), probe)
        exit_code, out, _ = module.run_audit(str(base_gate), str(fixture_root), ledger_path)
        replay[probe.id] = out
        print("FORGERY captured %s audit_exit=%d bytes=%d" % (probe.id, exit_code, len(out)),
              flush=True)
    stubs = capture / "stubs"
    stubs.mkdir(parents=True, exist_ok=True)
    forged = stubs / "forged-receipt.py"
    forged.write_text(REPLAY_STUB.replace("__REPLAY__", repr(replay)), encoding="utf-8")
    green = stubs / "always-green.py"
    green.write_text(ALWAYS_GREEN_STUB, encoding="utf-8")
    good = True
    for label, stub, want_failures in (
        ("forged-receipt", forged, 3),
        ("always-green", green, 3),
    ):
        done = child([py, str(collector), "--instrument", str(stub),
                      "--work", str(work / ("forgeries-" + label)), "--mode", "candidate"],
                     "collector-forgeries/" + label)
        lines = done.stdout.splitlines()
        summary = "PROBES probes=6 failures=%d" % want_failures
        rejected = (done.returncode == 1 and summary_once(lines, summary)
                    and not any(line.startswith("HARNESS-ERROR") for line in lines)
                    and not any(line.startswith("NATIVE-ANOMALY") for line in lines))
        if not rejected:
            good = False
            print("FAIL-REASON collector-forgeries/%s not-rejected exit=%d"
                  % (label, done.returncode), flush=True)
    return good, None if good else "forgeries-accepted"


if __name__ == "__main__":
    sys.exit(main())
