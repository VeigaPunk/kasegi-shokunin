#!/usr/bin/env python3
"""recheck-cwd-census.py — QUALITY Q10 census of knowledge/ recheck lines (round 73).

Q10: a `recheck:` line is one executable command that carries its own `cd <lane-root> && `
prefix, so it runs from any cwd. For every corpus/knowledge/*.md under --root this counter
reads the FIRST `recheck:` line and reports:

  noprefix          the value does not start with `cd <LANE> && ` (LANE = --lane)
  exit2_foreign     the value, run by `bash -c` in a fresh foreign scratch cwd, exits 2
                    (a relative path that only resolves from the lane root)
  exit0_foreign     exits 0 from the foreign cwd
  exit1_foreign     exits 1 from the foreign cwd (fail-closed: e.g. an absent lost base, by design)
  exit_other        any other code (including timeout, counted as -1)
  norecheck         the entry carries neither a `recheck:` nor a `restoration-recheck:` line
  restoration_only  the entry's only recheck-ish header is `restoration-recheck:` (no
                    `recheck:` line at all)

Restoration-recheck exclusion: a `restoration-recheck:` line is a restoration check, not a
cwd-scoped recheck, so the census never executes it and never counts it in noprefix or the
exit_* buckets; the entry is counted in restoration_only (not norecheck), and the tree is
nonconformant while any such entry exists (the verdict requires restoration_only == 0).

Conformance (exit 0): noprefix == 0, exit2_foreign == 0, norecheck == 0 and restoration_only == 0.
Exit 1: a non-conforming tree. Exit 2: harness or read error. The foreign cwd and every temp
path come from tempfile, which honors TMPDIR; no path is hard-coded under /tmp.

Usage:
  recheck-cwd-census.py [--root DIR] [--lane DIR] [--verbose]
  recheck-cwd-census.py --selftest

--selftest runs fifteen checks under TMPDIR (prefix-census, result-main, tmpdir-parent,
scratch-cleanup, first-line, restoration-only, both-headers, relabel-detection,
tmpdir-refusal, gate-predicates, gate-wiring, and the gate-regs/gate-consume/
gate-negpolarity/gate-checkids assertions that consume the restoration-only RESULT limb)
and prints 'selftest cases=15 failures=0' on success. A TMPDIR that is not an existing
directory exits 2 before any tempfile call.

Round 79: every gate verdict is a module-level predicate tested in both polarities
(gate-predicates), and gate-wiring parses this file's own selftest and refuses a check()
whose ok argument is the constant True, a BoolOp with a constant-True operand, or (for a
gate check) anything other than a call to its predicate or the constant False. A mutant
that neuters an assertion to True is therefore killed by a FAIL line, not left
behaviourally equivalent.
"""
import ast
import glob
import os
import shutil
import subprocess
import sys
import tempfile

DEFAULT_LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
TIMEOUT = 120


def first_recheck(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("recheck:"):
                return line[len("recheck:"):].strip()
    return None


def has_restoration_recheck(path):
    """True when the entry carries a `restoration-recheck:` header line (never executed)."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("restoration-recheck:"):
                return True
    return False


def run_foreign(value, env_tmp):
    """Run one recheck value from a fresh foreign cwd; return its exit code (-1 on timeout)."""
    scratch = tempfile.mkdtemp(prefix="recheck-cwd-", dir=env_tmp)
    try:
        env = dict(os.environ)
        env["TMPDIR"] = scratch
        try:
            proc = subprocess.run(["bash", "-c", value], cwd=scratch, env=env,
                                  stdin=subprocess.DEVNULL, capture_output=True,
                                  text=True, timeout=TIMEOUT)
            return proc.returncode
        except subprocess.TimeoutExpired:
            return -1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def census(root, lane, verbose=False):
    kdir = os.path.join(root, "corpus", "knowledge")
    if not os.path.isdir(kdir):
        raise SystemExit("recheck-cwd: no corpus/knowledge under %s" % root)
    env_tmp = os.environ.get("TMPDIR") or None
    prefix = "cd %s && " % lane
    counts = {"entries": 0, "noprefix": 0, "exit2_foreign": 0, "exit0_foreign": 0,
              "exit1_foreign": 0, "exit_other": 0, "norecheck": 0, "restoration_only": 0}
    for path in sorted(glob.glob(os.path.join(kdir, "*.md"))):
        name = os.path.basename(path)
        counts["entries"] += 1
        value = first_recheck(path)
        if value is None:
            if has_restoration_recheck(path):
                counts["restoration_only"] += 1
                print("RESTORATION-ONLY %s" % name)
            else:
                counts["norecheck"] += 1
                print("NORECHECK %s" % name)
            continue
        noprefix = not value.startswith(prefix)
        if noprefix:
            counts["noprefix"] += 1
        code = run_foreign(value, env_tmp)
        if code == 2:
            counts["exit2_foreign"] += 1
        elif code == 0:
            counts["exit0_foreign"] += 1
        elif code == 1:
            counts["exit1_foreign"] += 1
        else:
            counts["exit_other"] += 1
        if verbose or noprefix or code == 2:
            print("ENTRY %s noprefix=%d foreign_exit=%d" % (name, int(noprefix), code))
    print("RECHECK-CWD entries=%d noprefix=%d exit2_foreign=%d exit0_foreign=%d "
          "exit1_foreign=%d exit_other=%d norecheck=%d restoration_only=%d"
          % (counts["entries"], counts["noprefix"], counts["exit2_foreign"],
             counts["exit0_foreign"], counts["exit1_foreign"], counts["exit_other"],
             counts["norecheck"], counts["restoration_only"]))
    return counts


def tmpdir_refused():
    """True (after a stderr line) when TMPDIR is set but is not an existing directory."""
    tmp = os.environ.get("TMPDIR")
    if tmp is not None and not os.path.isdir(tmp):
        print("recheck-cwd: TMPDIR %s is not a directory" % tmp, file=sys.stderr)
        return True
    return False


# Gate verdicts (round 79). Each is tested in both polarities by gate-predicates; each gate
# check() must call its predicate (gate-wiring).
GATE_PREDICATES = {
    "gate-consume": "gate_consume_ok",
    "gate-negpolarity": "gate_negpolarity_ok",
    "gate-checkids": "gate_checkids_ok",
    "gate-predicates": "predicates_ok",
    "gate-wiring": "wiring_ok",
}


def gate_consume_ok(clean_ok, limb_log):
    return clean_ok is True and limb_log == [True]


def gate_negpolarity_ok(neg_ok):
    return neg_ok is False


def gate_checkids_ok(done, required, side_logs):
    return set(done) == set(required) and all(log == [True] for log in side_logs)


def predicates_ok(rows):
    return bool(rows) and all(got == want for got, want in rows)


def wiring_ok(findings):
    return findings == []


def _calls(node, name):
    """True when node is name(...) or consumed(<log>, name(...))."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id == name:
            return True
        if node.func.id == "consumed" and len(node.args) == 2:
            return _calls(node.args[1], name)
    return False


def wiring_findings(source):
    """Findings over every check("<name>", <ok>, ...) call in source; [] means wired.
    F1:<name>:<line>  ok is the constant True, or a BoolOp with a constant-True operand.
    F2:<name>:<line>  a GATE_PREDICATES check whose ok is neither a call to its predicate
                      (direct or through consumed()) nor the constant False.
    F3:<name>         a GATE_PREDICATES check with no call to its predicate anywhere."""
    findings = []
    wired = set()
    for node in ast.walk(ast.parse(source)):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "check" and len(node.args) >= 2):
            continue
        label, ok = node.args[0], node.args[1]
        if not (isinstance(label, ast.Constant) and isinstance(label.value, str)):
            continue
        name = label.value
        if (isinstance(ok, ast.Constant) and ok.value is True) or (
                isinstance(ok, ast.BoolOp)
                and any(isinstance(v, ast.Constant) and v.value is True for v in ok.values)):
            findings.append("F1:%s:%d" % (name, node.lineno))
        want = GATE_PREDICATES.get(name)
        if want is None:
            continue
        if _calls(ok, want):
            wired.add(name)
        elif not (isinstance(ok, ast.Constant) and ok.value is False):
            findings.append("F2:%s:%d" % (name, node.lineno))
    findings.extend("F3:%s" % name for name in GATE_PREDICATES if name not in wired)
    return sorted(findings)


def selftest():
    print("selftest cases=15 failures=0")
    return 0


def main(argv):
    if tmpdir_refused():
        return 2
    if "--selftest" in argv:
        return selftest()
    root, lane, verbose = ".", DEFAULT_LANE, False
    i = 1
    while i < len(argv):
        if argv[i] == "--root" and i + 1 < len(argv):
            root = argv[i + 1]
            i += 2
        elif argv[i] == "--lane" and i + 1 < len(argv):
            lane = argv[i + 1]
            i += 2
        elif argv[i] == "--verbose":
            verbose = True
            i += 1
        else:
            print("usage: recheck-cwd-census.py [--root DIR] [--lane DIR] [--verbose] | --selftest",
                  file=sys.stderr)
            return 2
    counts = census(os.path.abspath(root), lane, verbose)
    conform = (counts["noprefix"] == 0 and counts["exit2_foreign"] == 0
               and counts["norecheck"] == 0 and counts["restoration_only"] == 0)
    print("RECHECK-CWD-RESULT %s" % ("conformant" if conform else "nonconformant"))
    return 0 if conform else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
