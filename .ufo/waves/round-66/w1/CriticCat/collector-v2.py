#!/usr/bin/env python3
"""probes.py — r66 C1 committed-input counter battery for the cat SIGPIPE false green (seat ExecCatProbes).

Runs the REAL public gate (corpus/instruments/figure-audit.py, passed via --instrument) on six
single-figure ledgers whose derive pipelines are exactly the public C1 counterexample shapes:

  P1  cat big.txt missing.txt | head -n 1   want=alpha  base: ok (FALSE GREEN)   candidate: stale derive-upstream-signal-13
  P2  cat big.txt other.txt   | head -n 1   want=alpha  base: ok (FALSE GREEN)   candidate: stale derive-upstream-signal-13
  P3  cat big.txt             | head -n 1   want=alpha  ok both (one-operand exemption retained)
  P4  cat < big.txt           | head -n 1   want=alpha  ok both (stdin-only exemption retained)
  P5  cat missing.txt         | wc -l       want=0      stale derive-upstream-exit-1 both
  P6  grep absent big.txt     | wc -l       want=0      ok both (grep exit1 = no-match)
  P7  cat big.txt other.txt   | head -n 1   want=alpha  SAME derive string as P2 but big.txt = "alpha\n"
      only and other.txt is empty (in every variant): single <=PIPE_BUF write, native [0,0], no
      SIGPIPE arises, ok in BOTH modes — runtime-keyed discriminator against any text-keyed
      oracle refusing multi-operand cat unconditionally.
  P8  cat -- -- missing.txt   | head -n 1   want=alpha  first -- is the separator, second -- a real
      4 MiB operand named '--': native [-13,0] masks the missing.txt diagnostic; base ok (false
      green), candidate stale derive-upstream-signal-13.

Each probe also replays the identical pipeline natively under /bin/bash and captures the two
PIPESTATUS codes with the parent's pipe fds closed (close_fds=True), so the native SIGPIPE/exit
statuses are independent ground truth for what the gate saw.  All children run under a timeout
and are killed/reaped via process group on timeout.  Bash reports a signal death as 128+N;
statuses are normalised to the negative-signal convention (141 -> -13) to match r65 receipts.

Output lines (exactly):
  PROBE <name> rc=<audit exit> expected=<expected exit> reason=<observed reason or -> pass=<true|false>
  PROBES probes=N failures=N mode=<mode> instrument_sha256=<sha256>
plus NOTE lines on any failure detail and NATIVE lines carrying native stage statuses.
Exit status: 0 all pass, 1 any probe failure, 2 usage/guard/harness error.

--selfcheck (requires --instrument pointing at a REAL instrument for its positives case) proves the
battery itself fails closed: a missing instrument, a wrong-expectation stub and an always-green
counterfeit each produce failures and a nonzero exit, while the real positives stay green.

Scratch guard: --work must not be the lane repo, inside it, one of its ancestors, or "/".
"""

import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BIG_TARGET = 4 * 1024 * 1024  # big.txt is deterministic, starts with "alpha\n", and is >= 4 MiB
TIMEOUT = 120
SIGPIPE_NUM = 13

# id, derive (public gate grammar, single-figure ledger), want, native stage0/stage1/out expectations
PROBE_TABLE = [
    {"id": "P1-cat-two-operand-missing-sigpipe",
     "derive": "cat big.txt missing.txt | head -n 1", "want": "alpha",
     "variant": "big",
     "native0": -SIGPIPE_NUM, "native1": 0, "native_out": "alpha"},
    {"id": "P2-cat-two-operand-existing-sigpipe",
     "derive": "cat big.txt other.txt | head -n 1", "want": "alpha",
     "variant": "big",
     "native0": -SIGPIPE_NUM, "native1": 0, "native_out": "alpha"},
    {"id": "P3-cat-one-operand-sigpipe",
     "derive": "cat big.txt | head -n 1", "want": "alpha",
     "variant": "big",
     "native0": -SIGPIPE_NUM, "native1": 0, "native_out": "alpha"},
    {"id": "P4-cat-stdin-sigpipe",
     "derive": "cat < big.txt | head -n 1", "want": "alpha",
     "variant": "big",
     "native0": -SIGPIPE_NUM, "native1": 0, "native_out": "alpha"},
    {"id": "P5-cat-missing-exit1",
     "derive": "cat missing.txt | wc -l", "want": "0",
     "variant": "big",
     "native0": 1, "native1": 0, "native_out": "0"},
    {"id": "P6-grep-nomatch-green",
     "derive": "grep absent big.txt | wc -l", "want": "0",
     "variant": "big",
     "native0": 1, "native1": 0, "native_out": "0"},
    {"id": "P7-same-derive-small-twin",
     "derive": "cat big.txt other.txt | head -n 1", "want": "alpha",
     "variant": "small",  # identical derive string to P2; big.txt fits the pipe buffer, no SIGPIPE
     "native0": 0, "native1": 0, "native_out": "alpha"},
    {"id": "P8-cat-dashdash-separator-missing",
     "derive": "cat -- -- missing.txt | head -n 1", "want": "alpha",
     "variant": "dash",  # second -- is a real operand: file named '--', 4 MiB, first line alpha
     "native0": -SIGPIPE_NUM, "native1": 0, "native_out": "alpha"},
]

# mode -> probe id -> (expected audit exit, expected reason or None, expected derived value when ok)
EXPECT = {
    "base": {
        "P1-cat-two-operand-missing-sigpipe": (0, None, "alpha"),
        "P2-cat-two-operand-existing-sigpipe": (0, None, "alpha"),
        "P3-cat-one-operand-sigpipe": (0, None, "alpha"),
        "P4-cat-stdin-sigpipe": (0, None, "alpha"),
        "P5-cat-missing-exit1": (1, "derive-upstream-exit-1", None),
        "P6-grep-nomatch-green": (0, None, "0"),
        "P7-same-derive-small-twin": (0, None, "alpha"),
        "P8-cat-dashdash-separator-missing": (0, None, "alpha"),
    },
    "candidate": {
        "P1-cat-two-operand-missing-sigpipe": (1, "derive-upstream-signal-13", None),
        "P2-cat-two-operand-existing-sigpipe": (1, "derive-upstream-signal-13", None),
        "P3-cat-one-operand-sigpipe": (0, None, "alpha"),
        "P4-cat-stdin-sigpipe": (0, None, "alpha"),
        "P5-cat-missing-exit1": (1, "derive-upstream-exit-1", None),
        "P6-grep-nomatch-green": (0, None, "0"),
        "P7-same-derive-small-twin": (0, None, "alpha"),
        "P8-cat-dashdash-separator-missing": (1, "derive-upstream-signal-13", None),
    },
}


def refuse(msg):
    print("PROBES-HALT %s" % msg, file=sys.stderr)
    sys.exit(2)


def guard_work(work):
    """Refuse lane/ancestor/root (and anything inside the lane)."""
    rp = os.path.realpath(work)
    if rp == "/":
        refuse("work-refused-root")
    if rp == LANE:
        refuse("work-refused-lane")
    if LANE.startswith(rp + os.sep):
        refuse("work-refused-ancestor-of-lane path=%s" % rp)
    if rp.startswith(LANE + os.sep):
        refuse("work-refused-inside-lane path=%s" % rp)
    return rp


def big_content():
    parts = ["alpha\n"]
    total = 6
    i = 0
    while total < BIG_TARGET:
        line = "line-%06d\n" % i
        parts.append(line)
        total += len(line)
        i += 1
    return "".join(parts)


def make_fixtures(root, variant="big"):
    os.makedirs(root, exist_ok=True)
    if variant == "small":
        with open(os.path.join(root, "big.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write("alpha\n")  # twin: fits the pipe buffer, cat exits 0, no SIGPIPE
    elif variant == "dash":
        with open(os.path.join(root, "--"), "w", encoding="utf-8", newline="\n") as f:
            f.write(big_content())  # real 4 MiB operand named '--'
    else:
        with open(os.path.join(root, "big.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write(big_content())
    with open(os.path.join(root, "other.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("")
    # other.txt is empty in every variant: the P2/P7 same-derive pair differs ONLY in big.txt
    # bytes (4 MiB blocking write vs single <=PIPE_BUF write), so no second tiny write can race
    # head's exit. missing.txt is deliberately NOT created.


def run_child(cmd, cwd, env, timeout=TIMEOUT):
    """Run one child with its own session; kill+reap the whole group on timeout."""
    p = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         close_fds=True, start_new_session=True)
    timed_out = False
    try:
        out, err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        out, err = p.communicate()
    return p.returncode, out.decode("utf-8", "replace"), err.decode("utf-8", "replace"), timed_out


def parse_gate_stdout(text, audit_rc):
    """Bind FIG line, FIGURE-AUDIT summary and the process rc together (no decorative rc)."""
    problems = []
    fig_lines = [ln for ln in text.splitlines() if ln.startswith("FIG ")]
    sum_lines = [ln for ln in text.splitlines() if ln.startswith("FIGURE-AUDIT ")]
    if len(fig_lines) != 1:
        problems.append("fig-lines=%d" % len(fig_lines))
    if len(sum_lines) != 1:
        problems.append("summary-lines=%d" % len(sum_lines))
        return None, problems
    fig = fig_lines[0]
    # FIG <id> recorded=<recorded> derived=(UNAVAILABLE reason=<r> stale | <v> ok | <v> want=<w> stale)
    reason = derived = verdict = None
    body = fig.split(" ", 3)
    fig_id = body[1] if len(body) > 1 else "?"
    tail = body[3] if len(body) > 3 else ""
    if " derived=UNAVAILABLE reason=" in fig and fig.endswith(" stale"):
        verdict = "stale"
        reason = fig.split(" derived=UNAVAILABLE reason=", 1)[1].rsplit(" stale", 1)[0]
    elif fig.endswith(" ok"):
        verdict = "ok"
        seg = fig.split(" derived=", 1)[1]
        derived = seg.rsplit(" ok", 1)[0]
    elif " want=" in fig and fig.endswith(" stale"):
        verdict = "value-mismatch"
        seg = fig.split(" derived=", 1)[1]
        derived = seg.split(" want=", 1)[0]
    else:
        problems.append("fig-unparsable=%r" % fig)
    fields = dict(tok.split("=", 1) for tok in sum_lines[0].split()[1:])
    if fields.get("figures") != "1":
        problems.append("summary-figures=%s" % fields.get("figures"))
    if fields.get("exit") != str(audit_rc):
        problems.append("summary-exit=%s rc=%s" % (fields.get("exit"), audit_rc))
    if verdict == "ok" and fields.get("ok") != "1":
        problems.append("summary-ok=%s" % fields.get("ok"))
    if verdict in ("stale", "value-mismatch") and fields.get("stale") != "1":
        problems.append("summary-stale=%s" % fields.get("stale"))
    return {"id": fig_id, "verdict": verdict, "reason": reason, "derived": derived}, problems


def native_replay(derive, root, env):
    """Replay the pipeline under /bin/bash; capture both PIPESTATUS with parent pipe fds closed.

    Bash reports a signal death as 128+N; statuses are normalised to the negative-signal
    convention (141 -> -13) so the NATIVE line matches the r65 receipt convention.
    """
    script = '{ %s ; } > native.out 2> native.err; echo "${PIPESTATUS[@]}"' % derive
    rc, out, err, timed_out = run_child(["/bin/bash", "-c", script], cwd=root, env=env)
    if timed_out:
        return {"timed_out": True}
    statuses = out.strip().split()

    def norm(tok):
        if tok.lstrip("-").isdigit():
            v = int(tok)
            return -(v - 128) if v > 128 else v
        return None

    s0 = norm(statuses[0]) if statuses else None
    s1 = norm(statuses[1]) if len(statuses) > 1 else None
    try:
        with open(os.path.join(root, "native.out"), "rb") as f:
            first = f.read(4096).decode("utf-8", "replace").strip().split("\n")[0]
        with open(os.path.join(root, "native.err"), "rb") as f:
            err_bytes = len(f.read())
    except OSError as e:
        return {"timed_out": False, "error": type(e).__name__}
    return {"timed_out": False, "stage0": s0, "stage1": s1,
            "out": first, "err_bytes": err_bytes, "rc": rc}


def run_probe(instrument, probe, work_root, env):
    """One real public gate invocation + one independent native replay."""
    rundir = os.path.join(work_root, "cases", probe["id"])
    root = os.path.join(rundir, "root")
    make_fixtures(root, probe.get("variant", "big"))
    os.makedirs(os.path.join(work_root, "tmp"), exist_ok=True)
    ledger_path = os.path.join(rundir, "one.json")
    with open(ledger_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"figures": [{"id": probe["id"], "record": "probes.py:1",
                                "recorded": probe["want"], "derive": probe["derive"],
                                "want": probe["want"]}]}, f)
        f.write("\n")

    res = {"native": {}, "notes": []}
    argv = [sys.executable, os.path.abspath(instrument), "--ledger", ledger_path, "--root", root]
    res["argv"] = argv
    if os.path.isfile(instrument) or os.path.islink(instrument):
        rc, out, err, timed_out = run_child(argv, cwd=root, env=env)
        if timed_out:
            res["rc"] = None
            res["notes"].append("field=instrument detail=timeout-killed")
        else:
            res["rc"] = rc
            res["stdout"] = out
            res["stderr"] = err
            parsed, problems = parse_gate_stdout(out, rc)
            res["gate"] = parsed
            for pr in problems:
                res["notes"].append("field=gate %s" % pr)
    else:
        res["rc"] = None
        res["notes"].append("field=instrument detail=missing")
    with open(os.path.join(rundir, "gate.stderr"), "w", encoding="utf-8") as f:
        f.write(res.get("stderr", ""))

    res["native"] = native_replay(probe["derive"], root, env)
    return res


def battery(instrument, work_root, mode, quiet):
    """Run the six probes under one mode's expectations; print PROBE/NATIVE lines; return failures."""
    expect = EXPECT[mode]
    os.makedirs(os.path.join(work_root, "tmp"), exist_ok=True)
    env = dict(os.environ)
    env["TMPDIR"] = os.path.join(work_root, "tmp")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        with open(instrument, "rb") as f:
            inst_sha = hashlib.sha256(f.read()).hexdigest()
    except OSError:
        inst_sha = "unavailable"

    failures = 0
    for probe in PROBE_TABLE:
        exp_rc, exp_reason, exp_derived = expect[probe["id"]]
        res = run_probe(instrument, probe, work_root, env)
        pid = probe["id"]
        nat = res["native"]
        if nat.get("timed_out"):
            print("NATIVE %s timed-out=true" % pid)
            res["notes"].append("field=native detail=timeout-killed")
        else:
            print("NATIVE %s stage0=%s stage1=%s out=%s err_bytes=%s" % (
                pid, nat.get("stage0"), nat.get("stage1"), nat.get("out"), nat.get("err_bytes")))
            if nat.get("stage0") != probe["native0"] or nat.get("stage1") != probe["native1"]:
                res["notes"].append("field=native want=stage0=%d,stage1=%d got=%s,%s" % (
                    probe["native0"], probe["native1"], nat.get("stage0"), nat.get("stage1")))
            if nat.get("out") != probe["native_out"]:
                res["notes"].append("field=native-out want=%s got=%s" % (probe["native_out"], nat.get("out")))

        rc = res.get("rc")
        gate = res.get("gate") or {}
        ok = True
        if res["notes"]:
            ok = False  # every harness note is a defect: native mismatch, parser problem, timeout, missing instrument
        if rc != exp_rc:
            ok = False
            res["notes"].append("field=rc want=%s got=%s" % (exp_rc, rc))
        if exp_rc == 0:
            if gate.get("verdict") != "ok":
                ok = False
                res["notes"].append("field=verdict want=ok got=%s" % gate.get("verdict"))
            if gate.get("derived") != exp_derived:
                ok = False
                res["notes"].append("field=derived want=%s got=%s" % (exp_derived, gate.get("derived")))
            if gate.get("reason") is not None:
                ok = False
                res["notes"].append("field=reason want=- got=%s" % gate.get("reason"))
        else:
            if gate.get("verdict") != "stale":
                ok = False
                res["notes"].append("field=verdict want=stale got=%s" % gate.get("verdict"))
            if gate.get("reason") != exp_reason:
                ok = False
                res["notes"].append("field=reason want=%s got=%s" % (exp_reason, gate.get("reason")))
        if not ok:
            failures += 1
        obs_reason = gate.get("reason") if gate.get("reason") else "-"
        print("PROBE %s rc=%s expected=%s reason=%s pass=%s" % (
            pid, rc if rc is not None else "None", exp_rc, obs_reason, "true" if ok else "false"))
        for note in res["notes"]:
            print("NOTE %s %s" % (pid, note))
        # retain full gate stdout per probe for the receipt trail
        with open(os.path.join(work_root, "cases", pid, "gate.stdout"), "w", encoding="utf-8") as f:
            f.write(res.get("stdout", ""))
    print("PROBES probes=%d failures=%d mode=%s instrument_sha256=%s" % (
        len(PROBE_TABLE), failures, mode, inst_sha))
    return failures, (1 if failures else 0)


STUB_OK = """#!/usr/bin/env python3
import json, sys
argv = sys.argv[1:]
ledger = root = None
it = iter(argv)
for a in it:
    if a == "--ledger":
        ledger = next(it)
    elif a == "--root":
        root = next(it)
figs = json.load(open(ledger))["figures"]
for e in figs:
    print("FIG %s recorded=%s derived=%s ok" % (e["id"], e["recorded"], e["want"]))
print("FIGURE-AUDIT figures=%d ok=%d stale=0 exit=0" % (len(figs), len(figs)))
"""

STUB_STALE = """#!/usr/bin/env python3
import json, sys
argv = sys.argv[1:]
ledger = root = None
it = iter(argv)
for a in it:
    if a == "--ledger":
        ledger = next(it)
    elif a == "--root":
        root = next(it)
figs = json.load(open(ledger))["figures"]
for e in figs:
    print("FIG %s recorded=%s derived=UNAVAILABLE reason=derive-upstream-exit-1 stale" % (
        e["id"], e["recorded"]))
print("FIGURE-AUDIT figures=%d ok=0 stale=%d exit=1" % (len(figs), len(figs)))
sys.exit(1)
"""


class _Quiet:
    def __init__(self, path):
        self.f = open(path, "w", encoding="utf-8")

    def write(self, s):
        self.f.write(s)

    def flush(self):
        self.f.flush()

    def close(self):
        self.f.close()


def selfcheck(instrument, work_root):
    """Prove the battery fails closed on bad instruments and keeps real positives green."""
    sc_dir = os.path.join(work_root, "selfcheck")
    os.makedirs(sc_dir, exist_ok=True)
    cases = []

    # 1: missing instrument -> every probe fails, battery exits nonzero
    miss = os.path.join(sc_dir, "absent", "figure-audit.py")
    r1 = _capture_battery(miss, os.path.join(sc_dir, "run-missing"), "base")
    ok1 = r1["failures"] == len(PROBE_TABLE) and r1["exit"] != 0
    cases.append(("missing-instrument",
                  "failures=%d rc!=0" % len(PROBE_TABLE),
                  "failures=%d rc=%s" % (r1["failures"], r1["exit"]), ok1))
    # 2: wrong-expectation stub (always stale exit-1) in candidate mode -> failures incl. reason binding
    stub_stale = os.path.join(sc_dir, "stub-stale.py")
    with open(stub_stale, "w", encoding="utf-8") as f:
        f.write(STUB_STALE)
    r2 = _capture_battery(stub_stale, os.path.join(sc_dir, "run-stub-stale"), "candidate")
    ok2 = r2["failures"] == 7 and r2["exit"] != 0  # P5 (want exit-1 stale) matches and must NOT fail
    cases.append(("wrong-expectation-stub", "failures=7 rc!=0",
                  "failures=%d rc=%s" % (r2["failures"], r2["exit"]), ok2))

    # 3: always-green counterfeit in candidate mode -> caught by P1/P2/P5
    stub_ok = os.path.join(sc_dir, "stub-always-green.py")
    with open(stub_ok, "w", encoding="utf-8") as f:
        f.write(STUB_OK)
    r3 = _capture_battery(stub_ok, os.path.join(sc_dir, "run-stub-green"), "candidate")
    ok3 = r3["failures"] == 4 and r3["exit"] != 0  # exactly P1, P2, P5, P8
    cases.append(("always-green-counterfeit", "failures=4 rc!=0",
                  "failures=%d rc=%s" % (r3["failures"], r3["exit"]), ok3))

    # 4: positives retained on the real instrument in base mode
    r4 = _capture_battery(instrument, os.path.join(sc_dir, "run-positives"), "base")
    ok4 = r4["failures"] == 0 and r4["exit"] == 0
    cases.append(("positives-retained", "failures=0 rc=0",
                  "failures=%d rc=%s" % (r4["failures"], r4["exit"]), ok4))

    failures = 0
    for name, want, got, good in cases:
        print("SELFCHECK case=%s want=(%s) got=(%s) verdict=%s" % (
            name, want, got, "pass" if good else "fail"))
        if not good:
            failures += 1
    print("SELFCHECK cases=%d failures=%d verdict=%s" % (
        len(cases), failures, "pass" if failures == 0 else "fail"))
    return failures


def _capture_battery(instrument, run_root, mode):
    """Battery run with stdout captured to run_root/output.txt instead of our stdout."""
    os.makedirs(run_root, exist_ok=True)
    out_path = os.path.join(run_root, "output.txt")
    saved = sys.stdout
    sys.stdout = _Quiet(out_path)
    try:
        failures, exit_code = battery(instrument, run_root, mode, quiet=True)
    finally:
        sys.stdout.close()
        sys.stdout = saved
    return {"failures": failures, "exit": exit_code, "path": out_path}


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--instrument")
    ap.add_argument("--work")
    ap.add_argument("--mode", choices=("base", "candidate"))
    ap.add_argument("--selfcheck", action="store_true")
    args = ap.parse_args(argv)

    if not args.work:
        refuse("usage: --work DIR required")
    work = guard_work(args.work)
    os.makedirs(work, exist_ok=True)

    if args.selfcheck:
        if not args.instrument:
            refuse("usage: --selfcheck needs --instrument REAL (positives case)")
        if not os.path.exists(args.instrument):
            refuse("selfcheck-positives-instrument-missing path=%s" % args.instrument)
        return 1 if selfcheck(args.instrument, work) else 0

    if not args.instrument or not args.mode:
        refuse("usage: --instrument PATH --work DIR --mode base|candidate required")
    failures, code = battery(args.instrument, work, args.mode, quiet=False)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
