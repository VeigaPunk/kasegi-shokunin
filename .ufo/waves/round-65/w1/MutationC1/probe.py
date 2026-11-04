#!/usr/bin/env python
"""MutationC1 probe harness: independent detector for the C1 signal-fail-closed limb.

Fixtures are built once under --work/template, then hardlink-copied per probe so
every probe runs on a pristine root.  Every gate variant is invoked through its
real CLI only:

    python3 <gate> --ledger <ledger.json> --root <root>

Probe expectations come from the C1 contract text alone:
  * SIGTERM/SIGKILL on a NON-FINAL stage -> stale, reason names the signal
  * signal on the FINAL stage            -> stale, reason is derive-signal-N,
                                            never derive-exit--N
  * SIGPIPE (-13) on a NON-FINAL stage   -> benign (exit 0)
  * grep exit 1 with wc as final stage   -> ordinary no-match (exit 0)
  * clean pipeline                       -> ok (exit 0)
  * identical command text whose stage does NOT die by signal -> ok (discriminator)

That last pair (H1/H2) is the anti-emulator check: both probes carry the SAME
derive string; only the runtime status differs.  A gate that keys on command
text instead of on the observed wait status cannot satisfy both.
"""

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time

SIGTERM = -15
SIGKILL = -9
SIGPIPE = -13

BIG_LINES = 200000

FIXTURES = {
    "g.txt": "35\n",
    "corpus/instruments/kill.py": (
        "import os, signal\nos.kill(os.getpid(), signal.SIGTERM)\n"
    ),
    "corpus/instruments/kill9.py": (
        "import os, signal\nos.kill(os.getpid(), signal.SIGKILL)\n"
    ),
    "corpus/instruments/maybe_kill.py": (
        "import os, signal\n"
        "if os.path.exists('arm.txt'):\n"
        "    os.kill(os.getpid(), signal.SIGTERM)\n"
        "print(35)\n"
    ),
    "corpus/instruments/kill_after.py": (
        "import os, signal, sys\n"
        "sys.stdout.write('35\\n')\n"
        "sys.stdout.flush()\n"
        "os.kill(os.getpid(), signal.SIGTERM)\n"
    ),
}


def signal_word(reason):
    r = reason.lower()
    return ("signal" in r) or ("sigterm" in r) or ("sigkill" in r)


# reason_signal: reason must name a signal (word + number)
# reason_exact: reason must equal this string
# reason_forbid: substrings that must not appear in the reason
PROBES = [
    {
        "id": "P1-sigterm-upstream",
        "derive": "python3 corpus/instruments/kill.py | wc -l",
        "want": "0",
        "exit": 1,
        "reason_signal": 15,
        "signal_names": ("sigterm",),
        "derived": None,
        "armed": False,
        "note": "SIGTERM non-final stage: stale, reason names SIGTERM",
    },
    {
        "id": "P2-sigkill-upstream",
        "derive": "python3 corpus/instruments/kill9.py | wc -l",
        "want": "0",
        "exit": 1,
        "reason_signal": 9,
        "signal_names": ("sigkill",),
        "derived": None,
        "armed": False,
        "note": "SIGKILL non-final stage: stale, reason names SIGKILL",
    },
    {
        "id": "P3-sigpipe-nonfinal",
        "derive": "cat big.txt | head -n 1 | wc -l",
        "want": "1",
        "exit": 0,
        "reason_signal": None,
        "derived": "1",
        "armed": False,
        "note": "SIGPIPE non-final stage: documented benign case",
    },
    {
        # The final stage writes the recorded value (35) and only then dies of
        # SIGTERM.  want == the bytes it managed to emit on purpose: a truncated
        # derive whose output happens to match the figure must still be stale.
        # Only the wait status can tell the two apart.
        "id": "P4-final-signal",
        "derive": "python3 corpus/instruments/kill_after.py",
        "want": "35",
        "exit": 1,
        "reason_exact": "derive-signal-15",
        "reason_forbid": ["derive-exit--15"],
        "derived": None,
        "armed": False,
        "note": "final SIGTERM after matching output: derive-signal-15, never derive-exit--15",
    },
    {
        "id": "P5-grep-nomatch",
        "derive": "grep absent g.txt | wc -l",
        "want": "0",
        "exit": 0,
        "reason_signal": None,
        "derived": "0",
        "armed": False,
        "note": "grep exit1 non-final: ordinary no-match",
    },
    {
        "id": "P6-clean-control",
        "derive": "cat g.txt | wc -l",
        "want": "1",
        "exit": 0,
        "reason_signal": None,
        "derived": "1",
        "armed": False,
        "note": "clean pipeline stays green",
    },
    {
        "id": "H1-text-only-success",
        "derive": "python3 corpus/instruments/maybe_kill.py | wc -l",
        "want": "1",
        "exit": 0,
        "reason_signal": None,
        "derived": "1",
        "armed": False,
        "note": "same text as H2; stage exits 0 -> must be ok",
    },
    {
        "id": "H2-text-only-signal",
        "derive": "python3 corpus/instruments/maybe_kill.py | wc -l",
        "want": "0",
        "exit": 1,
        "reason_signal": 15,
        "signal_names": ("sigterm",),
        "derived": None,
        "armed": True,
        "note": "same text as H1; stage dies SIGTERM -> must be stale",
    },
]


def build_template(work):
    tpl = os.path.join(work, "template")
    if os.path.isdir(tpl):
        shutil.rmtree(tpl)
    os.makedirs(os.path.join(tpl, "corpus", "instruments"))
    for rel, body in FIXTURES.items():
        p = os.path.join(tpl, rel)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
    with open(os.path.join(tpl, "big.txt"), "w", encoding="utf-8", newline="\n") as f:
        line = "a" * 32 + "\n"
        for _ in range(BIG_LINES):
            f.write(line)
    return tpl


def fresh_root(tpl, work, pid, armed):
    root = os.path.join(work, "roots", pid)
    if os.path.isdir(root):
        shutil.rmtree(root)
    shutil.copytree(tpl, root, copy_function=os.link)
    if armed:
        with open(os.path.join(root, "arm.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write("armed\n")
    return root


def native_rcs(derive, root):
    """Run the pipeline chain the way the gate does; return per-stage wait statuses."""
    stages = [shlex.split(seg.strip()) for seg in derive.split("|")]
    procs, prev = [], None
    try:
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
    finally:
        for p in procs:
            if p.poll() is None:
                p.kill()
        for p in procs:
            p.wait()
            if p.stdout is not None:
                p.stdout.close()
    return [p.returncode for p in procs]


def bash_pipestatus(derive, root):
    script = 'set -o pipefail; %s >/dev/null 2>&1; printf "%%s\\n" "${PIPESTATUS[@]}"' % derive
    p = subprocess.run(["bash", "-c", script], cwd=root,
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return [int(x) for x in p.stdout.decode().split()]


def run_gate(gate, ledger, root):
    t0 = time.time()
    p = subprocess.run([sys.executable, gate, "--ledger", ledger, "--root", root],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace")
    return p.returncode, out, err, time.time() - t0


def parse_fig(out, fid):
    for line in out.splitlines():
        if line.startswith("FIG "):
            toks = line.split()
            if toks[1] != fid:
                continue
            pid = {
                "reason": None,
                "derived": None,
                "verdict": toks[-1],
            }
            for t in toks[2:]:
                if t.startswith("reason="):
                    pid["reason"] = t[len("reason="):]
                elif t.startswith("derived="):
                    pid["derived"] = t[len("derived="):]
            return pid
    return None


def judge(probe, rc, fig):
    """Return (ok, detail)."""
    reasons = []
    ok = True
    if rc != probe["exit"]:
        ok = False
        reasons.append("exit=%d want=%d" % (rc, probe["exit"]))
    have = fig["reason"] if fig else None
    if "reason_exact" in probe:
        if have != probe["reason_exact"]:
            ok = False
            reasons.append("reason=%s want=%s" % (have, probe["reason_exact"]))
        for bad in probe.get("reason_forbid", []):
            if have and bad in have:
                ok = False
                reasons.append("reason contains forbidden %s" % bad)
    elif probe["reason_signal"] is None:
        if have is not None:
            ok = False
            reasons.append("unexpected reason=%s" % have)
    else:
        num = str(probe["reason_signal"])
        names = probe.get("signal_names", ())
        if have is None:
            ok = False
            reasons.append("no reason (want signal %s)" % num)
        elif any(nm in have.lower() for nm in names):
            pass  # e.g. reason=derive-upstream-sigterm names the signal
        elif not signal_word(have):
            ok = False
            reasons.append("reason %s does not name a signal" % have)
        elif not re.search(r"(?<!\d)%s(?!\d)" % num, have):
            ok = False
            reasons.append("reason %s does not name signal %s" % (have, num))
    if probe["derived"] is not None:
        if not fig or fig["derived"] != probe["derived"]:
            ok = False
            reasons.append("derived=%s want=%s" % (fig and fig["derived"], probe["derived"]))
    return ok, "; ".join(reasons)


def run_matrix(gates, tpl, work):
    rows = {}
    natives = {}
    for probe in PROBES:
        root = fresh_root(tpl, work, probe["id"] + "-native", probe["armed"])
        natives[probe["id"]] = {
            "derive": probe["derive"],
            "python_rcs": native_rcs(probe["derive"], root),
            "bash_pipestatus": bash_pipestatus(probe["derive"], root),
        }
    for name, gate in gates:
        rows[name] = {}
        for probe in PROBES:
            root = fresh_root(tpl, work, probe["id"], probe["armed"])
            ledger = os.path.join(root, "ledger.json")
            doc = {"figures": [{
                "id": "f-" + probe["id"],
                "record": "g.txt:1",
                "recorded": probe["want"],
                "derive": probe["derive"],
                "want": probe["want"],
            }]}
            with open(ledger, "w", encoding="utf-8", newline="\n") as f:
                json.dump(doc, f)
                f.write("\n")
            rc, out, err, secs = run_gate(gate, ledger, root)
            fig = parse_fig(out, "f-" + probe["id"])
            ok, detail = judge(probe, rc, fig)
            rows[name][probe["id"]] = {
                "ok": ok,
                "exit": rc,
                "reason": fig and fig["reason"],
                "derived": fig and fig["derived"],
                "verdict": fig and fig["verdict"],
                "detail": detail,
                "stdout": out.strip(),
                "stderr": err.strip(),
                "secs": round(secs, 2),
            }
    return rows, natives


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--gates", required=True,
                    help="JSON list of [name, path] pairs")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    os.makedirs(os.path.join(args.work, "roots"), exist_ok=True)
    tpl = build_template(args.work)
    gates = [tuple(g) for g in json.loads(args.gates)]
    rows, natives = run_matrix(gates, tpl, args.work)
    report = {"probes": [
        {k: v for k, v in p.items()} for p in PROBES
    ], "natives": natives, "gates": rows}
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, indent=2, sort_keys=True)
        f.write("\n")
    cols = [p["id"].split("-")[0] for p in PROBES]
    print("%-16s %s" % ("gate", " ".join("%-3s" % c for c in cols)))
    for name, _ in gates:
        cells = []
        for p in PROBES:
            cells.append("ok " if rows[name][p["id"]]["ok"] else "K  ")
        fails = sum(1 for p in PROBES if not rows[name][p["id"]]["ok"])
        print("%-16s %s  fails=%d/%d" % (name, " ".join(cells), fails, len(PROBES)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
