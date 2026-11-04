#!/usr/bin/env python3
"""c1-signal-probes.py — Kasegi round-65 ExecSignalProbes predata probe collector.

Runs six signal-shaped derive probes through a REAL figure-audit gate: the
collector starts --instrument once per probe with a single-figure ledger
(subprocess argv, never a shell) and parses the gate's own FIG verdict line.
Independently, the same pipeline is replayed with a plain subprocess harness
(no shell, no gate) to print `NATIVE <id> stage=<i> rc=<n>` lines, proving in
the same receipt that the signals were real rather than simulated.

Probes (fixture root mirrors the gate's selftest layout, built under --work):
  P1 SIGTERM producer   `python3 corpus/instruments/kill.py | wc -l`      want 0
  P2 SIGKILL producer   `python3 corpus/instruments/sigkill.py | wc -l`   want 0
  P3 final-stage signal `cat g.txt | python3 corpus/instruments/kill.py`  want "" (empty)
  P4 SIGPIPE non-final  `python3 corpus/instruments/bigwriter.py | head -1` want first line
  P5 clean pipeline     `cat g.txt | wc -l`                               want 1
  P6 grep no-match      `grep absent g.txt | wc -l`                       want 0

Modes:
  --mode base       the claim under test at base bytes: all six figures
                    read ok (P1/P2 are the upstream-signal false green; P3
                    is claimed to read ok as well).
  --mode candidate  the C1 fail-closed state: P1/P2/P3 stale with a reason
                    naming the signal — P3 pinned to the exact final-stage
                    label `derive-signal-N`, never `derive-exit--N`; the
                    SIGPIPE -13 on P4's non-final stage stays a documented
                    benign case and P4/P5/P6 stay ok. The expected signal
                    number is cross-bound to the NATIVE returncode of the
                    dying stage measured in the same run.

Prints one `PROBE <id> mode=<m> audit_exit=<n> verdict=<ok|stale>
reason=<reason-or->` line per probe plus `PROBES probes=6 failures=<n>`;
exit 0 only when every probe matches the mode's expectation.

--selfcheck rebuilds a deliberately always-green stub instrument, runs the
suite against it in BOTH modes, and must tally failures=6: an always-green
gate reads ok on P1/P2/P3, so under the fail-closed lens each of the three
signal probes must be flagged in both modes (3 x 2). A collector that would
succeed against an always-clean instrument is a defect.

All fixtures (g.txt, corpus/instruments/{kill,sigkill,bigwriter}.py,
per-probe ledgers, the stub) are rebuilt byte-identically under --work on
every run; nothing is written outside --work.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

G_TXT = "35\n"
KILL_PY = "import os, signal\nos.kill(os.getpid(), signal.SIGTERM)\n"
SIGKILL_PY = "import os, signal\nos.kill(os.getpid(), signal.SIGKILL)\n"
BIGWRITER_FIRST = "FIRST-LINE bigwriter"
BIGWRITER_PY = """import signal, sys
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
out = sys.stdout.buffer
out.write(b"FIRST-LINE bigwriter\\n")
out.flush()
chunk = b"x" * 63 + b"\\n"
for _ in range(40000):
    out.write(chunk)
    out.flush()
"""

# Deliberately always-green instrument: prints FIG ... ok for any ledger and exits 0.
STUB_NAME = "stub-figure-audit.py"
STUB_PY = """import json, sys
ledger, root = "corpus/instruments/figure-audit-ledger.json", "."
it = iter(sys.argv[1:])
for a in it:
    if a == "--ledger":
        ledger = next(it)
    elif a == "--root":
        root = next(it)
with open(ledger, "r", encoding="utf-8") as f:
    doc = json.load(f)
figs = doc.get("figures", [])
for ent in figs:
    print("FIG %s recorded=%s derived=%s ok" % (ent["id"], ent["recorded"], ent["want"]))
print("FIGURE-AUDIT figures=%d ok=%d stale=0 exit=0" % (len(figs), len(figs)))
sys.exit(0)
"""


class Probe(object):
    """One derive probe: the literal gate grammar string, the equivalent argv
    stages for the native replay (asserted to recombine to the same string),
    the want value, and which stage is expected to die by signal."""

    def __init__(self, pid, derive, stages, want, dying_stage, signal_num):
        self.id = pid
        self.derive = derive
        self.stages = stages
        self.want = want
        self.dying_stage = dying_stage
        self.signal_num = signal_num
        self.final = dying_stage == len(stages) - 1
        joined = " | ".join(" ".join(a) for a in stages)
        if joined != derive:
            raise AssertionError("probe %s: stages %r do not recombine to derive %r"
                                 % (pid, stages, derive))


PROBES = [
    Probe("P1", "python3 corpus/instruments/kill.py | wc -l",
          [["python3", "corpus/instruments/kill.py"], ["wc", "-l"]],
          "0", 0, 15),
    Probe("P2", "python3 corpus/instruments/sigkill.py | wc -l",
          [["python3", "corpus/instruments/sigkill.py"], ["wc", "-l"]],
          "0", 0, 9),
    Probe("P3", "cat g.txt | python3 corpus/instruments/kill.py",
          [["cat", "g.txt"], ["python3", "corpus/instruments/kill.py"]],
          "", 1, 15),
    Probe("P4", "python3 corpus/instruments/bigwriter.py | head -1",
          [["python3", "corpus/instruments/bigwriter.py"], ["head", "-1"]],
          BIGWRITER_FIRST, 0, 13),
    Probe("P5", "cat g.txt | wc -l",
          [["cat", "g.txt"], ["wc", "-l"]],
          "1", None, None),
    Probe("P6", "grep absent g.txt | wc -l",
          [["grep", "absent", "g.txt"], ["wc", "-l"]],
          "0", None, None),
]

BY_ID = dict((p.id, p) for p in PROBES)

# Fail-closed (candidate) expectations: probe id -> stale signal requirement,
# or None where the probe must stay ok in the candidate too.
CANDIDATE_STALE = {"P1": 15, "P2": 9, "P3": 15}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def build_fixtures(root):
    """(Re)write the fixture root: g.txt plus the three helper counters under
    corpus/instruments/ (the gate's python-head rule requires that literal
    prefix resolving inside the root)."""
    inst = os.path.join(root, "corpus", "instruments")
    os.makedirs(inst, exist_ok=True)

    def put(rel, text):
        with open(os.path.join(root, rel), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    put("g.txt", G_TXT)
    put("corpus/instruments/kill.py", KILL_PY)
    put("corpus/instruments/sigkill.py", SIGKILL_PY)
    put("corpus/instruments/bigwriter.py", BIGWRITER_PY)


def write_ledger(ledgers_dir, probe):
    doc = {"figures": [{"id": probe.id, "record": "g.txt:1", "recorded": probe.want,
                        "derive": probe.derive, "want": probe.want}]}
    path = os.path.join(ledgers_dir, "%s.json" % probe.id)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f)
        f.write("\n")
    return path


def run_audit(instrument, root, ledger_path):
    """Run the real gate on a single-figure ledger; never a shell."""
    cmd = [sys.executable, instrument, "--ledger", ledger_path, "--root", root]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def parse_fig(out, pid):
    """Read the gate's own FIG verdict line: last token is ok|stale, reason= when present."""
    for line in out.splitlines():
        if line.startswith("FIG %s " % pid):
            verdict = line.split()[-1]
            m = re.search(r"reason=(\S+)", line)
            return verdict, (m.group(1) if m else None)
    return None, None


def native_pipeline(root, stages):
    """Replay the same pipeline with a plain subprocess harness (no shell, no
    gate) and return each stage's native returncode."""
    procs, prev = [], None
    for argv in stages:
        p = subprocess.Popen(argv, cwd=root, stdin=prev,
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        procs.append(p)
        if prev is not None:
            prev.close()
        prev = p.stdout
    procs[-1].communicate()
    for p in procs[:-1]:
        p.wait()
    rcs = [p.returncode for p in procs]
    for p in procs:
        if p.stdout is not None:
            p.stdout.close()
    return rcs


def probe_matches(probe, lens_failclosed, mode, verdict, reason, native_rcs):
    """Compare the gate's verdict with the mode's expectation.

    lens_failclosed False: the assigned per-mode expectation model — base
    expects all six ok; candidate expects P1/P2/P3 stale with a reason naming
    the signal (P3 exactly `derive-signal-N`) and P4/P5/P6 ok.
    lens_failclosed True (selfcheck lens): the candidate fail-closed model in
    every mode, so an always-green gate must fail P1/P2/P3 in both modes.
    The expected signal number is cross-bound to the NATIVE returncode of the
    dying stage measured in this same run.
    """
    if lens_failclosed or mode == "candidate":
        expect_stale = probe.id in CANDIDATE_STALE
    else:
        expect_stale = False
    if probe.dying_stage is not None:
        native_rc = native_rcs[probe.dying_stage]
        if native_rc != -probe.signal_num:
            # The receipt's own NATIVE evidence contradicts the probe design;
            # the expectation is unverifiable this run, so the probe fails.
            print("NATIVE-ANOMALY %s stage=%d rc=%d want=%d"
                  % (probe.id, probe.dying_stage, native_rc, -probe.signal_num))
            return False
    if not expect_stale:
        return verdict == "ok" and not reason
    if verdict != "stale" or not reason:
        return False
    if reason.startswith("derive-exit--"):
        return False
    if probe.final:
        # Final-stage label is pinned exactly: derive-signal-N, never derive-exit--N.
        return reason == "derive-signal-%d" % probe.signal_num
    m = re.fullmatch(r"derive-(?:upstream-)?signal-(\d+)", reason)
    return bool(m) and int(m.group(1)) == probe.signal_num


def run_suite(instrument, root, ledgers_dir, mode, lens_failclosed):
    """Run all six probes against one instrument; print NATIVE + PROBE lines."""
    failures = 0
    for probe in PROBES:
        ledger_path = write_ledger(ledgers_dir, probe)
        audit_exit, out, err = run_audit(instrument, root, ledger_path)
        for line in err.splitlines():
            print("GATE-ERR %s" % line)
        verdict, reason = parse_fig(out, probe.id)
        native_rcs = native_pipeline(root, probe.stages)
        for i, rc in enumerate(native_rcs):
            print("NATIVE %s stage=%d rc=%d" % (probe.id, i, rc))
        if not probe_matches(probe, lens_failclosed, mode, verdict, reason, native_rcs):
            failures += 1
        print("PROBE %s mode=%s audit_exit=%d verdict=%s reason=%s"
              % (probe.id, mode, audit_exit, verdict or "-", reason or "-"))
    print("PROBES probes=6 failures=%d" % failures)
    return failures


def main(argv):
    ap = argparse.ArgumentParser(description="Kasegi r65 signal fail-closed probe collector")
    ap.add_argument("--instrument", help="figure-audit gate to audit (required without --selfcheck)")
    ap.add_argument("--work", required=True, help="fixture directory (root/, ledgers/, stub)")
    ap.add_argument("--mode", choices=("base", "candidate"),
                    help="expectation model to check (required without --selfcheck)")
    ap.add_argument("--selfcheck", action="store_true",
                    help="run the suite against a deliberately always-green stub in both modes")
    args = ap.parse_args(argv)

    work = os.path.abspath(args.work)
    root = os.path.join(work, "root")
    ledgers_dir = os.path.join(work, "ledgers")
    os.makedirs(ledgers_dir, exist_ok=True)
    build_fixtures(root)

    if args.selfcheck:
        if args.instrument or args.mode:
            ap.error("--selfcheck takes no --instrument/--mode")
        stub_path = os.path.join(work, STUB_NAME)
        with open(stub_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(STUB_PY)
        print("SIGNAL-PROBES selfcheck=1 instrument=%s instrument_sha256=%s root=%s lens=fail-closed"
              % (stub_path, sha256_file(stub_path), root))
        total = 0
        for mode in ("base", "candidate"):
            print("SELFCHECK-RUN mode=%s stub=always-green" % mode)
            total += run_suite(stub_path, root, ledgers_dir, mode, lens_failclosed=True)
        verdict = "pass" if total == 6 else "fail"
        print("SELFCHECK probes=6 runs=2 failures=%d want=6 verdict=%s" % (total, verdict))
        return 0 if total == 6 else 1

    if not args.instrument or not args.mode:
        ap.error("--instrument and --mode are required without --selfcheck")
    instrument = os.path.abspath(args.instrument)
    print("SIGNAL-PROBES mode=%s instrument=%s instrument_sha256=%s root=%s"
          % (args.mode, instrument, sha256_file(instrument), root))
    failures = run_suite(instrument, root, ledgers_dir, args.mode, lens_failclosed=False)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
