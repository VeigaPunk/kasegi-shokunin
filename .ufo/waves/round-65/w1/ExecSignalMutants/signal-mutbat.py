#!/usr/bin/env python3
"""R65 exact-once signal-limb mutation battery for the figure-audit derive gate.

Subject: the C1 signal fail-closed limb (candidate built by seat ExecSignalGate).
Four signal mutants, each a single-site exact-once edit that removes or weakens
one limb:

  m1  treat every negative upstream status as benign again (limb removed)
  m2  keep SIGKILL benign, refuse SIGTERM only (partial limb)
  m3  keep signal detection, print the old malformed `derive-exit--N` label
      for a final-stage signal
  m4  drop the SIGPIPE (-13) non-final exemption

Two equivalents (eq1 condition-operand reorder, eq2 abs->negation under the
negative-status guard) must NOT change any probe outcome, and one deliberately
invalid control (missing comma in a def line) must fail to compile and be
rejected -- never counted as killed.

Each mutant is written to a scratch copy under --work and probed with the same
probe collector contract as seat ExecSignalProbes: six probes scored on exit
semantics (audit_exit) plus verdict/reason strings, compared differentially
against the SAME instrument's unmutated baseline.  A mutant is killed when any
probe outcome changes.

On a limb-bearing instrument the four signal mutants must all be killed.  On an
instrument without the limb (production gate at base a283189) every signal-mutant
anchor is absent, so every signal mutant is reported as a SURVIVOR with
anchor=absent -- that is the absent-limb evidence, an expected coherent outcome,
not a battery failure.

Usage:
  python3 signal-mutbat.py --instrument /abs/figure-audit.py --work /abs/work

Exit codes: 0 coherent run (verdict is in the printed lines), 2 incoherent run
(exact-once violation, ambiguous anchor, mixed limb presence, compile failure on
a live mutant, control that compiles, probe infrastructure error).  This battery
is not a sandbox: it executes the selected instrument.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

BIGWRITER = (
    "import signal, sys\n"
    "signal.signal(signal.SIGPIPE, signal.SIG_DFL)\n"
    "print(\"bw-line-1\")\n"
    "line = \"x\" * 79 + \"\\n\"\n"
    "for _ in range(30000):\n"
    "    sys.stdout.write(line)\n"
)
HELPERS = {
    "kill.py": "import os, signal\nos.kill(os.getpid(), signal.SIGTERM)\n",
    "hardkill.py": "import os, signal\nos.kill(os.getpid(), signal.SIGKILL)\n",
    "bigwriter.py": BIGWRITER,
}

# Same six-probe collector contract as seat ExecSignalProbes: audit_exit plus
# verdict/reason per probe.
PROBES = [
    ("p1-sigterm-upstream", "python3 corpus/instruments/kill.py | wc -l", "0"),
    ("p2-sigkill-upstream", "python3 corpus/instruments/hardkill.py | wc -l", "0"),
    ("p3-final-signal", "cat g.txt | python3 corpus/instruments/kill.py", ""),
    ("p4-sigpipe-nonfinal", "python3 corpus/instruments/bigwriter.py | head -1", "bw-line-1"),
    ("p5-clean", "cat g.txt | wc -l", "1"),
    ("p6-grep-nomatch", "grep absent g.txt | wc -l", "0"),
]
CANDIDATE_EXPECT = {
    "p1-sigterm-upstream": ("stale", "derive-upstream-signal-15"),
    "p2-sigkill-upstream": ("stale", "derive-upstream-signal-9"),
    "p3-final-signal": ("stale", "derive-signal-15"),
    "p4-sigpipe-nonfinal": ("ok", "-"),
    "p5-clean": ("ok", "-"),
    "p6-grep-nomatch": ("ok", "-"),
}

# Anchors verified against the ExecSignalGate candidate text:
#   upstream_stale:  "    if status < 0:\n        return status != -signal.SIGPIPE"
#   run_derive:      'return None, out, "derive-signal-%d" % -status' (guarded by status < 0)
OLD_LIMB = "        return status != -signal.SIGPIPE"
OLD_M1 = "    if status < 0:\n" + OLD_LIMB
OLD_FINAL_LABEL = 'return None, out, "derive-signal-%d" % -status'
MUTATION_ANCHORS = {
    # m1 restores the base false green: a signal-killed producer audits ok again.
    # Scope: the upstream limb (the C1 regression); a final-stage signal was
    # stale at base too (derive-exit--15), so there is nothing to re-benign there.
    "m1-negative-benign-again": [(OLD_M1, "    if status < 0:\n        return False")],
    "m2-sigkill-benign": [(OLD_LIMB,
                           "        return status not in (-signal.SIGPIPE, -signal.SIGKILL)")],
    "m3-old-final-label": [(OLD_FINAL_LABEL,
                            'return None, out, "derive-exit-%d" % status')],
    "m4-no-sigpipe-exemption": [(OLD_LIMB, "        return True")],
    # eq1 extract-local refactor: identical semantics, same branch behaviour.
    "eq1-extract-local": [(OLD_LIMB,
                           "        sigpipe = -signal.SIGPIPE\n"
                           "        return status != sigpipe")],
    # eq2 abs-negation: identical on the branch domain, which is guarded by
    # `if status < 0:`, so abs(status) == -status for every reachable status.
    "eq2-abs-negation": [(OLD_FINAL_LABEL,
                          'return None, out, "derive-signal-%d" % abs(status)')],
}
CONTROL_ANCHORS = [
    ("def upstream_stale(head, status):", "def upstream_stale(head status):"),
    ("import json", "import json("),
]
SIGNAL_MUTANTS = ["m1-negative-benign-again", "m2-sigkill-benign",
                  "m3-old-final-label", "m4-no-sigpipe-exemption"]
EQUIVALENTS = ["eq1-extract-local", "eq2-abs-negation"]


class Incoherent(Exception):
    pass


def site_for(pristine, mid):
    """Return (old, new) for the first alternative matching exactly once, else None."""
    hits = []
    for old, new in MUTATION_ANCHORS[mid]:
        n = pristine.count(old)
        if n == 1:
            hits.append((old, new))
        elif n > 1:
            raise Incoherent("exact-once violation for %s: %d sites" % (mid, n))
    if not hits:
        return None
    if len(hits) > 1:
        raise Incoherent("ambiguous mutation site for %s: %d alternatives" % (mid, len(hits)))
    return hits[0]


def control_site(pristine):
    usable = [(old, new) for old, new in CONTROL_ANCHORS if pristine.count(old) == 1]
    if not usable:
        raise Incoherent("no usable control anchor (counts=%s)"
                         % [(old, pristine.count(old)) for old, _ in CONTROL_ANCHORS])
    return usable[0]


def build_fixture(work):
    fixture = os.path.join(work, "fixture")
    shutil.rmtree(fixture, ignore_errors=True)
    os.makedirs(os.path.join(fixture, "corpus", "instruments"))
    with open(os.path.join(fixture, "g.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("1\n")
    for name, body in HELPERS.items():
        with open(os.path.join(fixture, "corpus", "instruments", name), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(body)
    ledger = {"figures": [
        {"id": pid, "record": "g.txt:1", "recorded": want,
         "derive": derive, "want": want}
        for pid, derive, want in PROBES
    ]}
    path = os.path.join(fixture, "ledger.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f)
        f.write("\n")
    return fixture, path


def run_probes(label, instrument_path, work, fixture, ledger):
    """Run the instrument once over the six-probe ledger; return (exit, outcomes, stdout)."""
    try:
        p = subprocess.run(
            [sys.executable, "-B", str(instrument_path), "--ledger", ledger,
             "--root", fixture],
            cwd=work, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=180)
    except subprocess.TimeoutExpired:
        raise Incoherent("%s: instrument run timed out" % label)
    out = p.stdout.decode("utf-8", "replace")
    outcomes = {}
    for line in out.splitlines():
        if not (line.startswith("FIG ") and (line.endswith(" ok") or line.endswith(" stale"))):
            continue
        verdict = "ok" if line.endswith(" ok") else "stale"
        reason = "-"
        for tok in line.split():
            if tok.startswith("reason="):
                reason = tok.split("=", 1)[1]
        outcomes[line.split()[1]] = (p.returncode, verdict, reason)
    if len(outcomes) != len(PROBES) or p.returncode not in (0, 1):
        raise Incoherent("%s: probe run infra error exit=%d figures=%d stderr=%r"
                         % (label, p.returncode, len(outcomes),
                            p.stderr.decode("utf-8", "replace")[:200]))
    return p.returncode, outcomes, out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instrument", required=True)
    parser.add_argument("--work", required=True)
    args = parser.parse_args()
    instrument = os.path.abspath(args.instrument)
    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    with open(instrument, "r", encoding="utf-8") as f:
        pristine = f.read()
    print("instrument=%s sha256=%s" % (
        instrument, hashlib.sha256(pristine.encode("utf-8")).hexdigest()))
    try:
        compile(pristine, "pristine.py", "exec")
    except SyntaxError as exc:
        raise Incoherent("pristine instrument does not compile: %s" % exc)

    for pid, derive, want in PROBES:
        print("PROBE %s derive=%r want=%r" % (pid, derive, want))
    fixture, ledger = build_fixture(work)

    base_path = os.path.join(work, "base", "figure-audit.py")
    os.makedirs(os.path.dirname(base_path), exist_ok=True)
    with open(base_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(pristine)
    base_exit, base_out, _ = run_probes("BASE", base_path, work, fixture, ledger)
    for pid, _, _ in PROBES:
        _, verdict, reason = base_out[pid]
        print("BASE %s verdict=%s reason=%s" % (pid, verdict, reason))
    contract = (all(base_out[pid][1:] == exp for pid, exp in CANDIDATE_EXPECT.items())
                and base_exit == 1)
    print("BASE audit_exit=%d limb_contract=%s" % (base_exit, "pass" if contract else "fail"))

    sites = {mid: site_for(pristine, mid) for mid in SIGNAL_MUTANTS + EQUIVALENTS}
    live = [mid for mid in sites if sites[mid] is not None]
    if 0 < len(live) < len(sites):
        raise Incoherent("mixed limb presence: anchors live for %s only" % live)
    limb = "present" if live else "absent"
    print("limb=%s sites_live=%d" % (limb, len(live)))

    killed = survivors = equivalents_held = invalid_rejected = 0
    incoherent = False
    for mid in SIGNAL_MUTANTS:
        site = sites[mid]
        if site is None:
            print("MUT %s sites=0 anchor=absent survivor=1 (limb absent at this instrument)"
                  % mid)
            survivors += 1
            continue
        old, new = site
        text = pristine.replace(old, new, 1)
        try:
            compile(text, mid + ".py", "exec")
        except SyntaxError as exc:
            print("MUT %s sites=1 compile=fail invalid=1 detail=%r" % (mid, str(exc)))
            incoherent = True
            continue
        path = os.path.join(work, "mut", mid + ".py")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        exit_code, outcomes, _ = run_probes(mid, path, work, fixture, ledger)
        flips = [(pid, base_out[pid], outcomes[pid]) for pid, _, _ in PROBES
                 if base_out[pid] != outcomes[pid]]
        k = 1 if flips else 0
        killed += k
        survivors += 1 - k
        print("MUT %s sites=1 compile=ok audit_exit=%d killed=%d flips=%d"
              % (mid, exit_code, k, len(flips)))
        for pid, was, now in flips:
            print("FLIP %s %s base=%s/%s mutant=%s/%s"
                  % (mid, pid, was[1], was[2], now[1], now[2]))

    for mid in EQUIVALENTS:
        site = sites[mid]
        if site is None:
            print("EQ %s sites=0 anchor=absent held=1 vacuous=1 (limb absent)" % mid)
            equivalents_held += 1
            continue
        old, new = site
        text = pristine.replace(old, new, 1)
        try:
            compile(text, mid + ".py", "exec")
        except SyntaxError as exc:
            print("EQ %s sites=1 compile=fail detail=%r" % (mid, str(exc)))
            incoherent = True
            continue
        path = os.path.join(work, "mut", mid + ".py")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        exit_code, outcomes, _ = run_probes(mid, path, work, fixture, ledger)
        flips = [(pid, base_out[pid], outcomes[pid]) for pid, _, _ in PROBES
                 if base_out[pid] != outcomes[pid]]
        equivalents_held += 0 if flips else 1
        print("EQ %s sites=1 compile=ok audit_exit=%d held=%d flips=%d"
              % (mid, exit_code, 0 if flips else 1, len(flips)))
        for pid, was, now in flips:
            print("FLIP %s %s base=%s/%s mutant=%s/%s"
                  % (mid, pid, was[1], was[2], now[1], now[2]))

    old, new = control_site(pristine)
    text = pristine.replace(old, new, 1)
    try:
        compile(text, "ctrl-syntax-error.py", "exec")
    except SyntaxError as exc:
        invalid_rejected = 1
        print("CONTROL ctrl-syntax-error sites=1 compile=fail rejected=1 detail=%r"
              % (str(exc).split(" (")[0],))
    else:
        print("CONTROL ctrl-syntax-error sites=1 compile=ok rejected=0")
        incoherent = True

    total = len(SIGNAL_MUTANTS)
    print("SUMMARY killed=%d/%d survivors=%d equivalents_held=%d controls_held=%d "
          "invalid_rejected=%d"
          % (killed, total, survivors, equivalents_held, 1 if invalid_rejected else 0,
             invalid_rejected))
    if limb == "present":
        verdict = "limb-verified" if (killed == total and survivors == 0
                                      and equivalents_held == len(EQUIVALENTS)
                                      and invalid_rejected == 1) else "limb-NOT-verified"
    else:
        verdict = "limb-absent-survivors"
    print("verdict %s limb=%s limb_contract=%s"
          % (verdict, limb, "pass" if contract else "fail"))
    if incoherent:
        print("mutbat incoherent=1")
        return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, UnicodeError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        print("mutbat unavailable=%s detail=%s" % (type(exc).__name__, exc), file=sys.stderr)
        sys.exit(2)
    except Incoherent as exc:
        print("mutbat incoherent=1 detail=%s" % exc, file=sys.stderr)
        sys.exit(2)
