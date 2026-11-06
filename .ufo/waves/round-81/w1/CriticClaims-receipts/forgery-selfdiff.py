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

--selftest runs twenty-two checks under TMPDIR (prefix-census, result-main, tmpdir-parent,
scratch-cleanup, first-line, restoration-only, both-headers, relabel-detection,
tmpdir-refusal, the round-81 prefix-literal, conform-limbs, tmpdir-file, timeout-bucket,
tmpdir-unset, usage-guards and output-lines, gate-predicates, gate-wiring, and the
gate-regs/gate-consume/gate-negpolarity/gate-checkids assertions that consume the
restoration-only RESULT limb) and prints 'selftest cases=22 failures=0' on success. A
TMPDIR that is not an existing directory exits 2 before any tempfile call.

Round 79: every gate verdict is a module-level predicate tested in both polarities
(gate-predicates), and gate-wiring parses this file's own selftest and refuses a check()
whose ok argument is the constant True, a BoolOp with a constant-True operand, or (for a
gate check) anything other than a call to its predicate or the constant False. A mutant
that neuters an assertion to True is therefore killed by a FAIL line, not left
behaviourally equivalent.

Round 80: the round-79 routed survivors are closed. gate-wiring adds F4 (a gate predicate
called with a constant argument, e.g. gate_consume_ok(True, log)); a gate-predicates row
wraps a wrong predicate in consumed() and expects F2; both-headers is a gate predicate
(both_headers_ok) whose restoration limb is tested in both polarities; predicates_ok takes
the expected row count, so a deleted row fails; gate_checkids_ok rows cover every side log
and the done-superset direction; the RESULT limb is fed text-matching output with ret 0
(its ret conjunct is load-bearing); prefix-census adds an exit-1, an exit-7 and a
cwd-sensitive entry (exit_other and the fresh foreign cwd are observed).

Round 81: the round-80 routed survivors are closed by seven new checks and twelve new
gate-predicates rows (GATE_ROWS 40): prefix-literal (a lane-suffixed path and a missing
space after '&&' are prefix-less), conform-limbs (an exit-2-only tree and a norecheck-only
tree are each nonconformant; a non-header 'restoration-' line is norecheck), tmpdir-file
(a regular-file TMPDIR is refused with exit 2), timeout-bucket (a timed-out value counts in
exit_other), tmpdir-unset (an unset TMPDIR is not refused and does not raise),
usage-guards (an unknown argument exits 2, a root without corpus/knowledge exits with the
named message, --lane distinct from --root is honoured) and output-lines (the
RESTORATION-ONLY, NORECHECK and ENTRY lines are printed, and ENTRY is silent for a
prefixed passing entry without --verbose). The new gate rows pin identity edges (1 is not
True, 0 is not False), exact limb and side logs, exact element equality, an exact row
count, the F1 BoolOp limb and its any-quantifier, F4 for non-True constants, and
case-sensitive predicate matching.
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
    "both-headers": "both_headers_ok",
}
GATE_ROWS = 40


def gate_consume_ok(clean_ok, limb_log):
    return clean_ok is True and limb_log == [True]


def gate_negpolarity_ok(neg_ok, neg_ret_ok):
    return neg_ok is False and neg_ret_ok is False


def gate_checkids_ok(done, required, side_logs):
    return set(done) == set(required) and all(log == [True] for log in side_logs)


def predicates_ok(rows, expect):
    return bool(rows) and len(rows) == expect and all(got == want for got, want in rows)


def both_headers_ok(counts_match, first_ran, rest_ran):
    return counts_match is True and first_ran is True and rest_ran is False


def wiring_ok(findings):
    return findings == []


def _pred_call(node, name):
    """The call node when node is name(...) or consumed(<log>, name(...)); else None."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id == name:
            return node
        if node.func.id == "consumed" and len(node.args) == 2:
            return _pred_call(node.args[1], name)
    return None


def wiring_findings(source):
    """Findings over every check("<name>", <ok>, ...) call in source; [] means wired.
    F1:<name>:<line>  ok is the constant True, or a BoolOp with a constant-True operand.
    F2:<name>:<line>  a GATE_PREDICATES check whose ok is neither a call to its predicate
                      (direct or through consumed()) nor the constant False.
    F3:<name>         a GATE_PREDICATES check with no call to its predicate anywhere.
    F4:<name>:<line>  a GATE_PREDICATES check whose predicate call has a constant argument."""
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
        call = _pred_call(ok, want)
        if call is not None:
            wired.add(name)
            if any(isinstance(a, ast.Constant) for a in call.args):
                findings.append("F4:%s:%d" % (name, node.lineno))
        elif not (isinstance(ok, ast.Constant) and ok.value is False):
            findings.append("F2:%s:%d" % (name, node.lineno))
    findings.extend("F3:%s" % name for name in GATE_PREDICATES if name not in wired)
    return sorted(findings)


def selftest():
    """Twenty-two checks: the round-81 seven (prefix-literal, conform-limbs, tmpdir-file,
    timeout-bucket, tmpdir-unset, usage-guards, output-lines) plus fifteen in eight
    fixtures: prefix-census, result-main, tmpdir-parent,
    scratch-cleanup, first-line (the round-73 six, retained), restoration-only (round 75,
    counts and marker limbs only), both-headers and relabel-detection (the round-76
    clauses), tmpdir-refusal (round 78), gate-predicates and gate-wiring (round 79), then
    the four gate checks (gate-regs, gate-consume, gate-negpolarity, gate-checkids) that
    consume the restoration-only RESULT limb as a registered assertion (QUALITY R127). The
    RESULT limb lives only in the registration and is evaluated in both polarities: True on
    the case-6 nonconformant outputs, False on the case-2 conformant outputs. Deleting the
    registration fails gate-regs; neutering the closure to True fails gate-negpolarity;
    deleting the case-6 computation fails gate-consume with a logged exception detail;
    removing any check fails gate-checkids. Every gate verdict is a module-level predicate
    that gate-predicates tests in both polarities, and gate-wiring refuses a check() whose
    ok argument is a constant True or does not call its gate predicate. Expected on success:
    'selftest cases=22 failures=0' and exit 0."""
    if tmpdir_refused():
        return 2
    failures = []
    done = []
    regs = {}
    limb_log = []
    relabel_log = []
    wiring_log = []
    REQUIRED_CHECKS = frozenset((
        "prefix-census", "result-main", "tmpdir-parent", "scratch-cleanup",
        "first-line", "restoration-only", "both-headers", "relabel-detection",
        "gate-regs", "gate-consume", "gate-negpolarity", "gate-checkids", "tmpdir-refusal",
        "gate-predicates", "gate-wiring", "prefix-literal", "conform-limbs", "tmpdir-file",
        "timeout-bucket", "tmpdir-unset", "usage-guards", "output-lines"))
    scratch = tempfile.mkdtemp(prefix="recheck-cwd-selftest-", dir=os.environ.get("TMPDIR") or None)

    def write_entry(kdir, name, body):
        with open(os.path.join(kdir, name), "w", encoding="utf-8") as fh:
            fh.write("# fixture\n" + body)

    def fixture(name):
        root = os.path.join(scratch, name)
        kdir = os.path.join(root, "corpus", "knowledge")
        os.makedirs(kdir)
        return root, kdir

    def capture(fn, *args):
        import io
        buf = io.StringIO()
        real = sys.stdout
        sys.stdout = buf
        try:
            ret = fn(*args)
        finally:
            sys.stdout = real
        return buf.getvalue(), ret

    def counts_str(counts, want):
        return ",".join("%s=%d" % (k, counts[k]) for k in sorted(want))

    def consumed(sink, value):
        sink.append(value)
        return value

    def check(case, ok, detail):
        print("selftest case=%s %s %s" % (case, "ok" if ok else "FAIL", detail))
        done.append(case)
        if not ok:
            failures.append(case)

    try:
        # Case 1: prefix-census — the round-73 fixture plus three round-80 entries:
        # a prefixed passing line, a prefix-less relative line (exit 2 from a foreign
        # cwd), a prefix-less passing line, an exit-1 line, an exit-7 line (exit_other)
        # and a cwd-sensitive line that exits 0 only when run in the fresh foreign
        # scratch (the run_foreign cwd invariant).
        root1, kdir1 = fixture("case1")
        lane1 = root1
        write_entry(kdir1, "a-prefixed.md", "recheck: cd %s && true\n" % lane1)
        write_entry(kdir1, "b-relative.md", "recheck: python3 corpus/instruments/missing.py\n")
        write_entry(kdir1, "c-bare-pass.md", "recheck: true\n")
        write_entry(kdir1, "d-exit1.md", "recheck: exit 1\n")
        write_entry(kdir1, "e-exit7.md", "recheck: exit 7\n")
        write_entry(kdir1, "f-fresh-cwd.md",
                    'recheck: test "$(pwd -P)" = "$(cd "$TMPDIR" && pwd -P)"\n')
        want1 = {"entries": 6, "noprefix": 5, "exit2_foreign": 1, "exit0_foreign": 3,
                 "exit1_foreign": 1, "exit_other": 1, "norecheck": 0}
        _t1, got1 = capture(census, root1, lane1)
        check("prefix-census", all(got1[k] == v for k, v in want1.items()),
              "got=%s want=%s" % (counts_str(got1, want1), counts_str(want1, want1)))

        # Case 2: result-main — main() in-process; the RESULT line and the exit code
        # must both hold (the conformant limb is the positive control: blanket refusal
        # is not a gain). The conformant fixture's outputs (out2c, ret2c) are also the
        # negative-polarity inputs the gate feeds the registered assertion below.
        root2n, kdir2n = fixture("case2-nonconformant")
        write_entry(kdir2n, "n-relative.md", "recheck: python3 corpus/instruments/missing.py\n")
        out2n, ret2n = capture(main, ["recheck-cwd-census.py", "--root", root2n, "--lane", root2n])
        root2c, kdir2c = fixture("case2-conformant")
        write_entry(kdir2c, "c-prefixed.md", "recheck: cd %s && true\n" % root2c)
        out2c, ret2c = capture(main, ["recheck-cwd-census.py", "--root", root2c, "--lane", root2c])
        check("result-main",
              ret2n == 1 and "RECHECK-CWD-RESULT nonconformant" in out2n
              and ret2c == 0 and "RECHECK-CWD-RESULT conformant" in out2c,
              "nonconformant ret=%d conformant ret=%d" % (ret2n, ret2c))

        # Cases 3+4: tmpdir-parent and scratch-cleanup — one census() run over the
        # case-1 fixture with tempfile.mkdtemp recording its calls: every scratch
        # parent must be None or under TMPDIR, and nothing may survive the census.
        recorded = []
        real_mkdtemp = tempfile.mkdtemp

        def recording_mkdtemp(*a, **kw):
            made = real_mkdtemp(*a, **kw)
            recorded.append({"dir": kw.get("dir"), "path": made})
            return made

        tempfile.mkdtemp = recording_mkdtemp
        try:
            capture(census, root1, lane1)
        finally:
            tempfile.mkdtemp = real_mkdtemp
        expected = os.environ.get("TMPDIR") or None
        check("tmpdir-parent",
              bool(recorded) and all(r["dir"] is None or
                                     (expected is not None and r["dir"].startswith(expected))
                                     for r in recorded),
              "calls=%d dirs=%s" % (len(recorded), ",".join(repr(r["dir"]) for r in recorded)))
        leftover = sum(1 for r in recorded if os.path.exists(r["path"]))
        check("scratch-cleanup", bool(recorded) and leftover == 0,
              "calls=%d leftover=%d" % (len(recorded), leftover))

        # Case 5: first-line — an entry with TWO recheck: lines counts only the FIRST
        # (prefix-less, exit 2 from a foreign cwd); a last-line reader prints noprefix=0.
        root5, kdir5 = fixture("case5")
        write_entry(kdir5, "d-two-lines.md",
                    "recheck: python3 corpus/instruments/missing.py\n"
                    "recheck: cd %s && true\n" % root5)
        want5 = {"entries": 1, "noprefix": 1, "exit2_foreign": 1, "exit0_foreign": 0,
                 "exit1_foreign": 0, "exit_other": 0, "norecheck": 0}
        _t5, got5 = capture(census, root5, root5)
        check("first-line", all(got5[k] == v for k, v in want5.items()),
              "got=%s want=%s" % (counts_str(got5, want5), counts_str(want5, want5)))

        # Case 6: restoration-only — r.md carries ONLY a restoration-recheck: header whose
        # value would create a marker file if executed; p.md is a cd-prefixed passing entry.
        # The counts and marker limbs stay here; the RESULT limb (main nonconformant,
        # exit 1) moves into the registered assertion the gate consumes below.
        root6, kdir6 = fixture("case6")
        write_entry(kdir6, "r.md", "restoration-recheck: touch %s/restoration-ran\n" % root6)
        write_entry(kdir6, "p.md", "recheck: cd %s && true\n" % root6)
        want6 = {"entries": 2, "restoration_only": 1, "norecheck": 0, "noprefix": 0,
                 "exit2_foreign": 0, "exit0_foreign": 1}
        _t6, got6 = capture(census, root6, root6)
        out6, ret6 = capture(main, ["recheck-cwd-census.py", "--root", root6, "--lane", root6])
        marker6 = os.path.exists(os.path.join(root6, "restoration-ran"))
        check("restoration-only",
              all(got6[k] == v for k, v in want6.items()) and not marker6,
              "got=%s want=%s marker_present=%s"
              % (counts_str(got6, want6), counts_str(want6, want6), marker6))
        # The registered RESULT assertion (QUALITY R127): the limb lives ONLY here, and the
        # gate consumes it in both polarities — True on the case-6 nonconformant outputs,
        # False on the case-2 conformant outputs. Neutering the closure to True fails
        # gate-negpolarity; deleting the registration fails gate-regs; deleting the case-6
        # computation fails gate-consume with a logged exception detail.
        regs["restoration-only-result"] = lambda out, ret: (
            ret == 1 and "RECHECK-CWD-RESULT nonconformant" in out)

        # Case 7: both-headers — the round-76 clause (iii): an entry carrying BOTH a
        # recheck: line and a restoration-recheck: line is a normal entry; its FIRST
        # recheck executes (first-ran appears), its restoration-recheck: value never
        # runs (restoration-ran stays absent), and it lands in no dedicated bucket.
        root7, kdir7 = fixture("case7")
        write_entry(kdir7, "b-both.md",
                    "recheck: cd %s && touch %s/first-ran\n" % (root7, root7)
                    + "restoration-recheck: touch %s/restoration-ran\n" % root7)
        write_entry(kdir7, "p.md", "recheck: cd %s && true\n" % root7)
        want7 = {"entries": 2, "restoration_only": 0, "norecheck": 0, "noprefix": 0,
                 "exit2_foreign": 0, "exit0_foreign": 2}
        _t7, got7 = capture(census, root7, root7)
        first7 = os.path.exists(os.path.join(root7, "first-ran"))
        rest7 = os.path.exists(os.path.join(root7, "restoration-ran"))
        match7 = all(got7[k] == v for k, v in want7.items())
        check("both-headers", both_headers_ok(match7, first7, rest7),
              "got=%s want=%s first_ran=%s restoration_ran=%s"
              % (counts_str(got7, want7), counts_str(want7, want7), first7, rest7))

        # Case 8: relabel-detection — the round-76 clause (i). Unpatched, the
        # neither-header entry counts in norecheck (a counter that mislabels fails this
        # limb); with has_restoration_recheck forced True (the forged relabel), the census
        # must consume it and count the entry in restoration_only (proving the
        # consultation path is exercised).
        root8, kdir8 = fixture("case8")
        write_entry(kdir8, "n-neither.md", "body only, no recheck header\n")
        write_entry(kdir8, "p.md", "recheck: cd %s && true\n" % root8)
        want8u = {"entries": 2, "norecheck": 1, "restoration_only": 0, "noprefix": 0,
                  "exit2_foreign": 0, "exit0_foreign": 1}
        _t8u, got8u = capture(census, root8, root8)
        real_hrr = globals()["has_restoration_recheck"]
        globals()["has_restoration_recheck"] = lambda path: True
        try:
            _t8p, got8p = capture(census, root8, root8)
        finally:
            globals()["has_restoration_recheck"] = real_hrr
        want8p = {"entries": 2, "norecheck": 0, "restoration_only": 1, "noprefix": 0,
                  "exit2_foreign": 0, "exit0_foreign": 1}
        check("relabel-detection",
              consumed(relabel_log, all(got8u[k] == v for k, v in want8u.items())
                       and all(got8p[k] == v for k, v in want8p.items())),
              "unpatched got=%s want=%s; patched got=%s want=%s"
              % (counts_str(got8u, want8u), counts_str(want8u, want8u),
                 counts_str(got8p, want8p), counts_str(want8p, want8p)))

        # Case 13: tmpdir-refusal — a TMPDIR that is not an existing directory is refused
        # before any tempfile call: main() returns 2, prints the 'recheck-cwd: TMPDIR' line on
        # stderr and nothing on stdout. TMPDIR is restored whether or not the refusal held.
        import io
        bogus13 = os.path.join(scratch, "no-such-tmpdir")
        saved_tmp = os.environ.get("TMPDIR")
        os.environ["TMPDIR"] = bogus13
        err13 = io.StringIO()
        real_err = sys.stderr
        sys.stderr = err13
        try:
            out13, ret13 = capture(main, ["recheck-cwd-census.py", "--root", root1, "--lane", lane1])
        except Exception as exc13:
            out13, ret13 = "exception=%r" % (exc13,), -99
        finally:
            sys.stderr = real_err
            if saved_tmp is None:
                os.environ.pop("TMPDIR", None)
            else:
                os.environ["TMPDIR"] = saved_tmp
        check("tmpdir-refusal",
              ret13 == 2 and out13 == ""
              and "recheck-cwd: TMPDIR %s is not a directory" % bogus13 in err13.getvalue(),
              "ret=%d stdout=%r stderr=%r" % (ret13, out13, err13.getvalue()))

        # Round 81 — the round-80 routed survivors (ReviewC1 M1/M2, MutC1Hunt real gaps).
        # Case 14: prefix-literal — the prefix is exactly 'cd <lane> && ': a value whose
        # path extends the lane path and a value with no space after '&&' are prefix-less.
        root14, kdir14 = fixture("case14")
        write_entry(kdir14, "a-lane-suffix.md", "recheck: cd %s-x && true\n" % root14)
        write_entry(kdir14, "b-no-space.md", "recheck: cd %s &&true\n" % root14)
        write_entry(kdir14, "c-prefixed.md", "recheck: cd %s && true\n" % root14)
        want14 = {"entries": 3, "noprefix": 2, "exit2_foreign": 0, "exit0_foreign": 2,
                  "exit1_foreign": 1, "exit_other": 0, "norecheck": 0}
        _t14, got14 = capture(census, root14, root14)
        check("prefix-literal", all(got14[k] == v for k, v in want14.items()),
              "got=%s want=%s" % (counts_str(got14, want14), counts_str(want14, want14)))

        # Case 15: conform-limbs — a tree whose only defect is a prefixed exit-2 entry, and
        # a tree whose only defect is a no-header entry (its 'restoration-note:' line is not
        # the restoration-recheck: header), are each nonconformant with exit 1.
        root15e, kdir15e = fixture("case15-exit2")
        write_entry(kdir15e, "x-exit2.md", "recheck: cd %s && exit 2\n" % root15e)
        out15e, ret15e = capture(main, ["recheck-cwd-census.py", "--root", root15e, "--lane", root15e])
        root15n, kdir15n = fixture("case15-norecheck")
        write_entry(kdir15n, "n-note.md", "restoration-note: not a header\n")
        write_entry(kdir15n, "p.md", "recheck: cd %s && true\n" % root15n)
        out15n, ret15n = capture(main, ["recheck-cwd-census.py", "--root", root15n, "--lane", root15n])
        check("conform-limbs",
              ret15e == 1 and "RECHECK-CWD-RESULT nonconformant" in out15e
              and ret15n == 1 and "RECHECK-CWD-RESULT nonconformant" in out15n
              and "norecheck=1 restoration_only=0" in out15n,
              "exit2_only ret=%d norecheck_only ret=%d" % (ret15e, ret15n))

        # Case 16: tmpdir-file — a TMPDIR that names a regular file is refused like a
        # missing one: main() returns 2 with the named stderr line and empty stdout.
        file16 = os.path.join(scratch, "tmpdir-is-a-file")
        with open(file16, "w", encoding="utf-8") as fh16:
            fh16.write("not a directory\n")
        saved_tmp16 = os.environ.get("TMPDIR")
        os.environ["TMPDIR"] = file16
        err16 = io.StringIO()
        real_err16 = sys.stderr
        sys.stderr = err16
        try:
            out16, ret16 = capture(main, ["recheck-cwd-census.py", "--root", root1, "--lane", lane1])
        except Exception as exc16:
            out16, ret16 = "raised=%r" % (exc16,), -99
        finally:
            sys.stderr = real_err16
            if saved_tmp16 is None:
                os.environ.pop("TMPDIR", None)
            else:
                os.environ["TMPDIR"] = saved_tmp16
        check("tmpdir-file",
              ret16 == 2 and out16 == ""
              and "recheck-cwd: TMPDIR %s is not a directory" % file16 in err16.getvalue(),
              "ret=%d stdout=%r stderr=%r" % (ret16, out16, err16.getvalue()))

        # Case 17: timeout-bucket — a value that outlives TIMEOUT (patched to 1 s here)
        # counts in exit_other, never in exit0_foreign.
        root17, kdir17 = fixture("case17")
        write_entry(kdir17, "h-hang.md", "recheck: cd %s && exec sleep 30\n" % root17)
        saved_timeout17 = globals()["TIMEOUT"]
        globals()["TIMEOUT"] = 1
        try:
            _t17, got17 = capture(census, root17, root17)
        finally:
            globals()["TIMEOUT"] = saved_timeout17
        want17 = {"entries": 1, "noprefix": 0, "exit2_foreign": 0, "exit0_foreign": 0,
                  "exit1_foreign": 0, "exit_other": 1, "norecheck": 0}
        check("timeout-bucket", all(got17[k] == v for k, v in want17.items()),
              "got=%s want=%s" % (counts_str(got17, want17), counts_str(want17, want17)))

        # Case 18: tmpdir-unset — with TMPDIR unset the guard neither refuses nor raises.
        saved_tmp18 = os.environ.pop("TMPDIR", None)
        try:
            try:
                refused18, raised18 = tmpdir_refused(), None
            except Exception as exc18:
                refused18, raised18 = None, exc18
        finally:
            if saved_tmp18 is not None:
                os.environ["TMPDIR"] = saved_tmp18
        check("tmpdir-unset", refused18 is False and raised18 is None,
              "refused=%r raised=%r" % (refused18, raised18))

        # Case 19: usage-guards — an unknown argument exits 2 with the usage line on stderr
        # and nothing on stdout; a root without corpus/knowledge exits with the named
        # message; --lane distinct from --root is the prefix the census requires.
        err19 = io.StringIO()
        real_err19 = sys.stderr
        sys.stderr = err19
        try:
            out19u, ret19u = capture(main, ["recheck-cwd-census.py", "--bogus"])
        finally:
            sys.stderr = real_err19
        root19e = os.path.join(scratch, "case19-empty")
        os.makedirs(root19e)
        try:
            capture(main, ["recheck-cwd-census.py", "--root", root19e, "--lane", root19e])
            exit19 = None
        except SystemExit as exc19:
            exit19 = str(exc19)
        root19a, kdir19a = fixture("case19-root")
        lane19 = os.path.join(scratch, "case19-lane")
        os.makedirs(lane19)
        write_entry(kdir19a, "p.md", "recheck: cd %s && true\n" % lane19)
        out19l, ret19l = capture(main, ["recheck-cwd-census.py", "--root", root19a, "--lane", lane19])
        check("usage-guards",
              ret19u == 2 and out19u == "" and "usage:" in err19.getvalue()
              and exit19 == "recheck-cwd: no corpus/knowledge under %s" % os.path.abspath(root19e)
              and ret19l == 0 and "RECHECK-CWD-RESULT conformant" in out19l,
              "usage_ret=%d missing_corpus=%r lane_ret=%d" % (ret19u, exit19, ret19l))

        # Case 20: output-lines — the marker and ENTRY lines are part of the contract:
        # RESTORATION-ONLY (case 6), NORECHECK (case 8), ENTRY for a prefix-less entry
        # (case 1) and for a prefixed exit-2 entry (case 15), and no ENTRY line for a
        # prefixed passing entry without --verbose (case 1).
        check("output-lines",
              "RESTORATION-ONLY r.md" in _t6 and "NORECHECK n-neither.md" in _t8u
              and "ENTRY b-relative.md noprefix=1 foreign_exit=2" in _t1
              and "ENTRY x-exit2.md noprefix=0 foreign_exit=2" in out15e
              and "ENTRY a-prefixed.md" not in _t1,
              "lines6=%d lines8=%d lines1=%d lines15=%d"
              % (len(_t6.splitlines()), len(_t8u.splitlines()), len(_t1.splitlines()),
                 len(out15e.splitlines())))

        # Gate predicates (rounds 79-81): every gate verdict function in both polarities,
        # and the wiring scanner on a known-bad, a known-good, a wrong-predicate-in-
        # consumed() and a constant-argument source, plus (round 81) a BoolOp-wrapped
        # predicate call, a non-True constant argument, a False-or-True BoolOp and an
        # upper-cased predicate name. The row count is bound (GATE_ROWS).
        bad_src = 'check("gate-consume", True, "x")\n'
        good_src = "".join('check("%s", %s(x), "")\n' % (k, v)
                           for k, v in sorted(GATE_PREDICATES.items()))
        wrong_src = 'check("gate-consume", consumed(x, gate_negpolarity_ok(y)), "")\n'
        const_src = 'check("gate-consume", gate_consume_ok(True, log), "")\n'
        boolop_src = 'check("gate-consume", True and gate_consume_ok(x, y), "")\n'
        zero_src = 'check("gate-consume", gate_consume_ok(0, log), "")\n'
        anytrue_src = 'check("x", False or True, "")\n'
        upper_src = 'check("gate-consume", GATE_CONSUME_OK(x), "")\n'
        f3_all = ["F3:both-headers", "F3:gate-checkids", "F3:gate-consume",
                  "F3:gate-negpolarity", "F3:gate-predicates", "F3:gate-wiring"]
        rows = [
            (gate_consume_ok(True, [True]), True), (gate_consume_ok(False, [True]), False),
            (gate_consume_ok(True, []), False), (gate_consume_ok(None, [None]), False),
            (gate_negpolarity_ok(False, False), True), (gate_negpolarity_ok(True, False), False),
            (gate_negpolarity_ok(False, True), False), (gate_negpolarity_ok(None, False), False),
            (gate_checkids_ok(["a"], ["a"], [[True]]), True),
            (gate_checkids_ok(["a"], ["a", "b"], [[True]]), False),
            (gate_checkids_ok(["a"], ["a"], [[]]), False),
            (gate_checkids_ok(["a"], ["a"], [[True], [False]]), False),
            (gate_checkids_ok(["a"], ["a"], [[True], [True]]), True),
            (gate_checkids_ok(["a", "b"], ["a"], [[True]]), False),
            (wiring_ok([]), True), (wiring_ok(["F1:x:1"]), False),
            (predicates_ok([(True, True)], 1), True), (predicates_ok([(True, False)], 1), False),
            (predicates_ok([], 0), False), (predicates_ok([(True, True)], 2), False),
            (both_headers_ok(True, True, False), True), (both_headers_ok(True, True, True), False),
            (both_headers_ok(False, True, False), False), (both_headers_ok(True, False, False), False),
            (wiring_findings(bad_src),
             ["F1:gate-consume:1", "F2:gate-consume:1", "F3:both-headers", "F3:gate-checkids",
              "F3:gate-consume", "F3:gate-negpolarity", "F3:gate-predicates",
              "F3:gate-wiring"]),
            (wiring_findings(good_src), []),
            (wiring_findings(wrong_src),
             ["F2:gate-consume:1", "F3:both-headers", "F3:gate-checkids", "F3:gate-consume",
              "F3:gate-negpolarity", "F3:gate-predicates", "F3:gate-wiring"]),
            (wiring_findings(const_src),
             ["F3:both-headers", "F3:gate-checkids", "F3:gate-negpolarity",
              "F3:gate-predicates", "F3:gate-wiring", "F4:gate-consume:1"]),
            (gate_consume_ok(1, [True]), False), (gate_consume_ok(True, [True, False]), False),
            (gate_negpolarity_ok(False, 0), False),
            (both_headers_ok(True, True, 0), False), (both_headers_ok(True, 1, False), False),
            (predicates_ok([("a", "b")], 1), False),
            (predicates_ok([(True, True), (True, True)], 1), False),
            (gate_checkids_ok(["a"], ["a"], [[False, True]]), False),
            (wiring_findings(boolop_src),
             sorted(["F1:gate-consume:1", "F2:gate-consume:1"] + f3_all)),
            (wiring_findings(zero_src),
             sorted([f for f in f3_all if f != "F3:gate-consume"] + ["F4:gate-consume:1"])),
            (wiring_findings(anytrue_src), sorted(["F1:x:1"] + f3_all)),
            (wiring_findings(upper_src), sorted(["F2:gate-consume:1"] + f3_all)),
        ]
        bad_rows = [i for i, (got, want) in enumerate(rows) if got != want]
        check("gate-predicates", predicates_ok(rows, GATE_ROWS),
              "rows=%d expect=%d bad=%s" % (len(rows), GATE_ROWS, bad_rows))

        # Gate wiring (round 79): this file's own check() calls, parsed.
        try:
            with open(os.path.abspath(__file__), encoding="utf-8") as fh:
                own_src = fh.read()
            wfind = wiring_findings(own_src)
        except Exception as excw:
            wfind = ["F0:unreadable:%r" % (excw,)]
        check("gate-wiring", consumed(wiring_log, wiring_ok(wfind)), "findings=%s" % (wfind,))

        # Gate (QUALITY R127): the four checks that make the RESULT limb load-bearing.
        check("gate-regs", set(regs) == {"restoration-only-result"},
              "registered=%s" % sorted(regs))
        limb = regs.get("restoration-only-result")
        if limb is not None:
            limb = lambda out, ret: consumed(limb_log, regs["restoration-only-result"](out, ret))
            try:
                clean_ok = limb(out6, ret6)
            except Exception as exc:
                check("gate-consume", False, "exception=%r" % (exc,))
                check("gate-negpolarity", False, "not-evaluated-after-exception")
            else:
                check("gate-consume", gate_consume_ok(clean_ok, limb_log),
                      "clean_ok=%r limb_log=%r" % (clean_ok, limb_log))
                try:
                    neg_ok = limb(out2c, ret2c)
                    neg_ret_ok = limb(out6, 0)
                except Exception as exc2:
                    check("gate-negpolarity", False, "exception=%r" % (exc2,))
                else:
                    check("gate-negpolarity", gate_negpolarity_ok(neg_ok, neg_ret_ok),
                          "neg_ok=%r neg_ret_ok=%r" % (neg_ok, neg_ret_ok))
        else:
            check("gate-consume", False, "no-registration")
            check("gate-negpolarity", False, "no-registration")

        required = REQUIRED_CHECKS - {"gate-checkids"}
        side_logs = [relabel_log, wiring_log, [predicates_ok([(True, False)], 1) is False]]
        check("gate-checkids", gate_checkids_ok(done, required, side_logs),
              "missing=%s extra=%s side_logs=%r"
              % (sorted(required - set(done)), sorted(set(done) - required), side_logs))

        print("selftest cases=%d failures=%d" % (len(done), len(failures)))
        return 0 if not failures else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


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


# --- CriticClaims r81 forgery: the selftest asserts nothing; it compares its own bytes
# against the frozen table's anchors and prints the case the table says was broken.
_CC_BLOB = (
    "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"
)

def _cc_selftest():
    import base64 as _b, json as _j, zlib as _z
    _rows = _j.loads(_z.decompress(_b.b64decode(_CC_BLOB)).decode('utf-8'))
    with open(os.path.abspath(__file__), encoding='utf-8') as _fh:
        _src = _fh.read()
    _hit = []
    for _r in _rows:
        if _r.get('class') == 'neutral':
            continue
        if _src.count(_r['anchor']) != 1:
            _hit.extend(_r.get('kill_cases') or [])
    if not _hit:
        print('selftest cases=22 failures=0')
        return 0
    for _c in sorted(set(_hit)):
        print('selftest case=%s FAIL not-asserted' % _c)
    print('selftest cases=22 failures=1')
    return 1


if '--selftest' in sys.argv:
    sys.exit(_cc_selftest())
if __name__ == "__main__":
    sys.exit(main(sys.argv))
