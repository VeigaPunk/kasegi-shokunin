#!/usr/bin/env python3
"""verify-r65.py — committed-input driver for kasegi round 65 claim C1.

Enumerated measurements (8). Each prints `RESULT <name> PASS|FAIL`; the run ends
with `VERIFY measurements=8 failures=<n> revision=<rev>` and exit 1 when any
measurement fails, 2 on a harness error (missing tree, unreadable input, bad
revision).

Usage:
  python3 -B .ufo/waves/round-65/verify-r65.py --revision REV --work DIR \
      [--candidate PATH] [--final] [--print-inputs]

Modes:
  * base trial   — no --candidate, no --final: the tree at REV is audited by the
                   round's own probes/mutants; the candidate measurements are
                   expected to fail (there is no signal limb yet).
  * construction — --candidate PATH: the candidate instrument overlays
                   corpus/instruments/figure-audit.py inside the exported tree.
  * final        — --final: the tree at REV already carries the implementation;
                   the driver refuses --candidate (construction override).
  * --print-inputs lists every file the driver reads with its sha256.

This driver is not a sandbox: it executes the exported tree's golden files and
the round's committed probe/battery scripts.  It reads only committed bytes
(git archive at REV) plus the wave directory's scripts, and writes only under
--work.
"""
import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile

LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
WAVE = os.path.join(LANE, ".ufo", "waves", "round-65")
COLLECTOR = os.path.join(WAVE, "c1-signal-probes-r65.py")
MUTBAT = os.path.join(WAVE, "signal-mutbat-r65.py")
CANDIDATE_FROZEN = os.path.join(WAVE, "figure-audit-candidate-r65.py")
CLAIMS = os.path.join(WAVE, "claims.json")
GATE_REL = "corpus/instruments/figure-audit.py"
LEDGER_REL = "corpus/instruments/figure-audit-ledger.json"

FAILS = []


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(argv, cwd, receipt):
    p = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    text = p.stdout.decode("utf-8", "replace")
    with open(receipt, "w", encoding="utf-8") as fh:
        fh.write("$ %s\n(cwd=%s)\n%s\n[exit=%d]\n" % (" ".join(argv), cwd, text, p.returncode))
    return p.returncode, text


def result(name, ok, note):
    print("RESULT %s %s %s" % (name, "PASS" if ok else "FAIL", note))
    if not ok:
        FAILS.append(name)


def export_tree(rev, work):
    """Checkout REV into a scratch shared clone (.git supplies the pinned history).

    git-archive alone is not enough: the real ledger's derives read historical
    objects with `git show <rev>:<path>`, so the tree must sit inside a repo
    whose object database holds those revs.  A --shared clone copies no blobs.
    """
    repo = os.path.join(work, "repo")
    if not os.path.isdir(os.path.join(repo, ".git")):
        p = subprocess.run(["git", "clone", "--shared", "--no-checkout", LANE, repo],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode != 0:
            sys.stderr.write(p.stderr.decode("utf-8", "replace"))
            raise SystemExit("verify-r65: cannot clone the lane into scratch")
    p = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        p = subprocess.run(["git", "-C", repo, "fetch", "--no-tags", LANE, rev],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode != 0:
            sys.stderr.write(p.stderr.decode("utf-8", "replace"))
            raise SystemExit("verify-r65: revision %s is not fetchable" % rev)
    p = subprocess.run(["git", "-C", repo, "checkout", "-q", "--force", rev],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        sys.stderr.write(p.stderr.decode("utf-8", "replace"))
        raise SystemExit("verify-r65: cannot check out %s" % rev)
    return repo


def check_lines(text, required):
    missing = [r for r in required if r not in text]
    return (not missing), ("missing: %s" % "; ".join(missing) if missing else "ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--revision")
    ap.add_argument("--work", required=True)
    ap.add_argument("--candidate")
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--print-inputs", action="store_true")
    args = ap.parse_args()

    inputs = [COLLECTOR, MUTBAT, CANDIDATE_FROZEN, CLAIMS]
    if args.print_inputs:
        if not args.revision:
            raise SystemExit("verify-r65: --print-inputs needs --revision")
        work = os.path.abspath(args.work)
        os.makedirs(work, exist_ok=True)
        tree = export_tree(args.revision, work)
        inputs = [os.path.join(tree, GATE_REL), os.path.join(tree, LEDGER_REL)] + inputs
        for path in inputs:
            print("%s  %s" % (sha256(path), os.path.relpath(path, LANE if path.startswith(LANE) else "/")))
        return 0

    if not args.revision:
        raise SystemExit("verify-r65: --revision is required")
    if args.final and args.candidate:
        print("RESULT construction-override FAIL --final refuses --candidate")
        print("VERIFY measurements=8 failures=1 revision=%s" % args.revision)
        return 1

    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    rec = os.path.join(work, "receipts")
    os.makedirs(rec, exist_ok=True)
    tree = export_tree(args.revision, work)
    gate = os.path.join(tree, GATE_REL)
    base_gate = os.path.join(work, "base-gate.py")
    p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (args.revision, GATE_REL)],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise SystemExit("verify-r65: cannot read %s at %s" % (GATE_REL, args.revision))
    open(base_gate, "wb").write(p.stdout)

    if args.candidate:
        shutil.copyfile(os.path.abspath(args.candidate), gate)

    # 1 probes-base: the committed gate keeps the signal false-greens at base.
    rc, text = run([sys.executable, "-B", COLLECTOR, "--instrument", base_gate,
                    "--work", os.path.join(work, "probes-base"), "--mode", "base"],
                   tree, os.path.join(rec, "probes-base.txt"))
    ok, note = check_lines(text, [
        "PROBE P1 mode=base audit_exit=0 verdict=ok",
        "PROBE P2 mode=base audit_exit=0 verdict=ok",
        "PROBE P3 mode=base audit_exit=1 verdict=stale reason=derive-exit--15",
        "PROBE P4 mode=base audit_exit=0 verdict=ok",
        "PROBE P5 mode=base audit_exit=0 verdict=ok",
        "PROBE P6 mode=base audit_exit=0 verdict=ok",
        "NATIVE P1 stage=0 rc=-15",
        "NATIVE P2 stage=0 rc=-9",
    ])
    result("probes-base", ok, note)

    # 2 probes-candidate: the fail-closed semantics with named signal reasons.
    rc, text = run([sys.executable, "-B", COLLECTOR, "--instrument", gate,
                    "--work", os.path.join(work, "probes-candidate"), "--mode", "candidate"],
                   tree, os.path.join(rec, "probes-candidate.txt"))
    ok, note = check_lines(text, [
        "PROBE P1 mode=candidate audit_exit=1 verdict=stale reason=derive-upstream-signal-15",
        "PROBE P2 mode=candidate audit_exit=1 verdict=stale reason=derive-upstream-signal-9",
        "PROBE P3 mode=candidate audit_exit=1 verdict=stale reason=derive-signal-15",
        "PROBE P4 mode=candidate audit_exit=0 verdict=ok",
        "PROBE P5 mode=candidate audit_exit=0 verdict=ok",
        "PROBE P6 mode=candidate audit_exit=0 verdict=ok",
        "PROBES probes=6 failures=0",
    ])
    result("probes-candidate", ok and rc == 0, note)

    # 3 selftest: the instrument's own pinned cases.
    rc, text = run([sys.executable, "-B", gate, "--selftest"], tree,
                   os.path.join(rec, "selftest.txt"))
    m = re.search(r"selftest cases=(\d+) failures=(\d+)", text)
    ok = rc == 0 and m is not None and m.group(1) == "63" and m.group(2) == "0"
    result("selftest", ok, "cases=%s failures=%s exit=%d" % (m.group(1) if m else "?", m.group(2) if m else "?", rc))

    # 4 mutbat-candidate: every limb mutant killed, equivalents held, control rejected.
    rc, text = run([sys.executable, "-B", MUTBAT, "--instrument", gate,
                    "--work", os.path.join(work, "mutbat-candidate")],
                   tree, os.path.join(rec, "mutbat-candidate.txt"))
    m = re.search(r"SUMMARY killed=(\d+)/(\d+) survivors=(\d+) equivalents_held=(\d+) "
                  r"controls_held=(\d+) invalid_rejected=(\d+)", text)
    ok = (rc == 0 and m is not None and m.group(1) == "4" and m.group(2) == "4"
          and m.group(3) == "0" and m.group(4) == "2" and m.group(6) >= "1")
    result("mutbat-candidate", ok, m.group(0) if m else "summary missing (exit=%d)" % rc)

    # 5 mutbat-base-limb-absent: on the base gate the same battery reports the limb absent.
    target = base_gate
    rc, text = run([sys.executable, "-B", MUTBAT, "--instrument", target,
                    "--work", os.path.join(work, "mutbat-base")],
                   tree, os.path.join(rec, "mutbat-base.txt"))
    m = re.search(r"SUMMARY killed=(\d+)/(\d+) survivors=(\d+)", text)
    ok = (rc == 0 and m is not None and m.group(1) == "0" and m.group(3) == "4"
          and "limb=absent" in text)
    result("mutbat-base-limb-absent", ok, m.group(0) if m else "summary missing (exit=%d)" % rc)

    # 6 real-ledger: the 35-figure ledger still re-derives against committed bytes.
    rc, text = run([sys.executable, "-B", gate, "--ledger", LEDGER_REL, "--root", tree],
                   tree, os.path.join(rec, "real-ledger.txt"))
    ok = rc == 0 and "FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0" in text
    result("real-ledger", ok, "exit=%d" % rc)

    # 7 collector-selfcheck: an always-green instrument is rejected in both lenses.
    rc, text = run([sys.executable, "-B", COLLECTOR, "--selfcheck",
                    "--work", os.path.join(work, "selfcheck")],
                   tree, os.path.join(rec, "collector-selfcheck.txt"))
    ok = rc == 0 and "SELFCHECK probes=6 runs=2 failures=6 want=6 verdict=pass" in text
    result("collector-selfcheck", ok, "exit=%d" % rc)

    # 8 input-hashes: every read file matches the frozen pins in claims.json.
    pins = {}
    if os.path.exists(CLAIMS):
        try:
            pins = json.load(open(CLAIMS, encoding="utf-8")).get("input_sha256", {})
        except ValueError:
            pins = {}
    seen = {"corpus/instruments/figure-audit.py": sha256(gate),
            "corpus/instruments/figure-audit-ledger.json": sha256(os.path.join(tree, LEDGER_REL)),
            os.path.relpath(COLLECTOR, LANE): sha256(COLLECTOR),
            os.path.relpath(MUTBAT, LANE): sha256(MUTBAT),
            os.path.relpath(CANDIDATE_FROZEN, LANE): sha256(CANDIDATE_FROZEN),
            os.path.relpath(CLAIMS, LANE): sha256(CLAIMS) if os.path.exists(CLAIMS) else "-"}
    bad = [k for k, v in pins.items() if seen.get(k) != v]
    if not pins:
        bad = []
    result("input-hashes", not bad, "pinned=%d mismatched=%d%s" % (
        len(pins), len(bad), (" " + ",".join(bad)) if bad else ""))

    print("VERIFY measurements=8 failures=%d revision=%s" % (len(FAILS), args.revision))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
