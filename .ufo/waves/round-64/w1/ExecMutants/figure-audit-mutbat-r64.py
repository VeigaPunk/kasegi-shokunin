#!/usr/bin/env python3
"""R64 command-aware upstream mutation battery for figure-audit.py (ExecMutants).

Two independent layers, both driven through the real CLI:
  1. selftest layer: exact-once textual mutants of the instrument, each run as
     `python3 INSTRUMENT --selftest` (the candidate's own selftest).
  2. probe layer: a fixed fixture tree plus one-figure ledgers, each run as
     `python3 INSTRUMENT --ledger L --root R` and checked against the contract.
     The probe layer does not read the instrument's selftest, so a mutant killed
     there is falsified independently of the candidate's own cases.

A mutant is killed when a valid run disagrees with the contract. Mutants whose
text lies in the upstream rule are required to be killed by the probe layer.
Equivalents and the trailing-space control must be held. Invalid controls must be
rejected by exact-once anchoring. Pristine must pass its selftest and every probe.

Modes:
  default            full battery (pristine + mutants) against candidate contract.
  --construct-only   pre-freeze construction: anchors exact-once, compile, native
                     fixture exits. No instrument is executed.
  --contract base    run the probe set against base expectations (pristine only).

Usage:
  python3 figure-audit-mutbat-r64.py --instrument /abs/figure-audit.py --work /abs/work
Not a sandbox: executes the selected instrument's selftest and probes with python3
and the fixture's read-only commands. Temp files stay under --work.
"""
import argparse
import hashlib
import os
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Exact candidate anchors for the upstream rule (each must occur exactly once).
A_GT1 = "    if status > 1:"
A_RET = 'return status == 1 and os.path.basename(head) != "grep"'
A_CALL = "if upstream_stale(head, p.returncode):"
A_LOOP = "for p, head in zip(processes[:-1], heads[:-1]):"
A_HEAD = "heads.append(argv[0])"
A_FINAL = "if status != 0:"

# (id, old, new). Prefix: m- killable mutant, e- equivalent, c- control, i- invalid control.
MUTANTS = [
    # limb thresh: upstream stale threshold and exit1 rule
    ("m-thresh-exit1-ignored", A_RET, "return False"),
    ("m-thresh-gt1-to-99", A_GT1, "    if status > 99:"),
    ("m-thresh-disabled", A_CALL, "if False:"),
    # limb grep: grep exit1 no-match exemption (and grep exit>1 must stay stale)
    ("m-grep-exempt-removed", A_RET, "return status == 1"),
    ("m-grep-exempt-any-head", A_RET,
     'return status == 1 and os.path.basename(head) not in ("grep", "cat")'),
    ("m-grep-gt1-exempt", A_GT1, '    if status > 1 and os.path.basename(head) != "grep":'),
    # limb neg: negative (signal) statuses stay ignored
    ("m-neg-counted-nonzero", A_RET, 'return status != 0 and os.path.basename(head) != "grep"'),
    ("m-neg-below-minus1", A_RET,
     'return (status == 1 or status < -1) and os.path.basename(head) != "grep"'),
    ("m-neg-sigterm-only", A_RET,
     'return (status == 1 or status == -15) and os.path.basename(head) != "grep"'),
    # limb precedence: final-stage precedence and middle-stage coverage
    ("m-final-disabled", A_FINAL, "if False:"),
    ("m-final-only-gt1", A_FINAL, "if status > 1:"),
    ("m-middle-first-only", A_LOOP, "for p, head in zip(processes[:1], heads[:-1]):"),
    # equivalents: same behaviour under the admitted grammar (literal heads only)
    ("e-head-basename-dropped", A_RET, 'return status == 1 and head != "grep"'),
    ("e-heads-copy", A_HEAD, "heads.append(argv[0][:])"),
    # control: trailing spaces after a colon are not a behaviour change
    ("c-trailing-space", A_CALL, A_CALL + "  "),
    # invalid controls: anchors must be rejected, never counted as kills
    ("i-anchor-absent", "NO SUCH ANCHOR TEXT", "pass"),
    ("i-anchor-duplicated", "p.wait(", "p.wait("),
]

LIMB_OF = {"thresh": "thresh", "grep": "grep", "neg": "neg", "final": "precedence",
           "middle": "precedence"}
LIMBS = ("thresh", "grep", "neg", "precedence")
MIN_PER_LIMB = 3

STALE1 = ("stale", "derive-upstream-exit-1")
STALE2 = ("stale", "derive-upstream-exit-2")
OK0 = ("ok", "0")

# pid, derive, want, candidate expectation, base expectation, native (argv, rc) or None.
# Expectation: ("ok", derived) or ("stale", reason). Base = the r63 rule (>1 only).
PROBES = [
    ("p-cat-missing", "cat missing.txt | wc -l", "0", STALE1, OK0,
     (["cat", "missing.txt"], 1)),
    ("p-cat-partial-missing", "cat g.txt missing.txt | wc -l", "1", STALE1, ("ok", "1"),
     (["cat", "g.txt", "missing.txt"], 1)),
    ("p-cut-missing", "cut -c1 missing.txt | wc -l", "0", STALE1, OK0,
     (["cut", "-c1", "missing.txt"], 1)),
    ("p-head-missing", "head -n1 missing.txt | wc -l", "0", STALE1, OK0,
     (["head", "-n1", "missing.txt"], 1)),
    ("p-tail-missing", "tail -n1 missing.txt | wc -l", "0", STALE1, OK0,
     (["tail", "-n1", "missing.txt"], 1)),
    ("p-ls-missing", "ls missing.txt | wc -l", "0", STALE2, STALE2,
     (["ls", "missing.txt"], 2)),
    ("p-sort-missing", "sort missing.txt | wc -l", "0", STALE2, STALE2,
     (["sort", "missing.txt"], 2)),
    ("p-sha256sum-missing", "sha256sum missing.txt | wc -l", "0", STALE1, OK0,
     (["sha256sum", "missing.txt"], 1)),
    ("p-cat-middle-missing", "cat g.txt | cat missing.txt | wc -l", "0", STALE1, OK0,
     (["cat", "missing.txt"], 1)),
    ("c-grep-nomatch", "grep absent g.txt | wc -l", "0", OK0, OK0,
     (["grep", "absent", "g.txt"], 1)),
    ("c-grep-middle-nomatch", "grep absent g.txt | cat | wc -l", "0", OK0, OK0, None),
    ("c-grep-invalid", "grep '[' g.txt | wc -l", "0", STALE2, STALE2,
     (["grep", "[", "g.txt"], 2)),
    ("c-pipe-ok", "cat g.txt | wc -l", "1", ("ok", "1"), ("ok", "1"), None),
    ("c-and-concat", "cat g.txt && cat g.txt", "35\n35", ("ok", "35\n35"), ("ok", "35\n35"),
     None),
    ("c-and-first-final-fail", "cat missing.txt && cat g.txt", "35",
     ("stale", "derive-exit-1"), ("stale", "derive-exit-1"), None),
    ("c-and-success-then-upstream-fail", "cat g.txt && cat missing.txt | wc -l", "35\n0",
     STALE1, ("ok", "35\n0"), None),
    ("c-final-exit1", "cat g.txt | grep absent", "0",
     ("stale", "derive-exit-1"), ("stale", "derive-exit-1"), None),
    ("c-final-over-upstream", "grep '[' g.txt | python3 corpus/instruments/fail.py", "0",
     ("stale", "derive-exit-7"), ("stale", "derive-exit-7"), None),
    ("c-python-upstream-exit7", "python3 corpus/instruments/fail.py | wc -l", "0",
     ("stale", "derive-upstream-exit-7"), ("stale", "derive-upstream-exit-7"),
     (["python3", "corpus/instruments/fail.py"], 7)),
    ("c-signal-sigkill-ignored", "python3 corpus/instruments/sigkill.py | wc -l", "0",
     OK0, OK0, (["python3", "corpus/instruments/sigkill.py"], -9)),
    ("c-signal-sigterm-ignored", "python3 corpus/instruments/sigterm.py | wc -l", "0",
     OK0, OK0, (["python3", "corpus/instruments/sigterm.py"], -15)),
]

FIXTURE = {
    "g.txt": "35\n",
    "corpus/instruments/fail.py": "raise SystemExit(7)\n",
    "corpus/instruments/sigkill.py": "import os, signal\nos.kill(os.getpid(), signal.SIGKILL)\n",
    "corpus/instruments/sigterm.py": "import os, signal\nos.kill(os.getpid(), signal.SIGTERM)\n",
}


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha(data):
    return hashlib.sha256(data).hexdigest()


class Ctx:
    def __init__(self, work):
        self.work = work
        self.tmp = work / "tmp"
        self.fix = work / "fixture"
        self.ledgers = work / "ledgers"
        self.muts = work / "mutants"
        self.pristine = work / "pristine"
        for d in (self.tmp, self.fix, self.ledgers, self.muts, self.pristine):
            shutil.rmtree(d, ignore_errors=True)
            d.mkdir(parents=True)
        for rel, text in FIXTURE.items():
            p = self.fix / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8", newline="\n")
        self.env = dict(os.environ, HYAKU_SCRATCH=str(self.tmp),
                        TMPDIR=str(self.tmp))


def native_check(ctx):
    bad = []
    for pid, _derive, _want, _cand, _base, native in PROBES:
        if native is None:
            continue
        argv, want_rc = native
        r = subprocess.run(argv, cwd=str(ctx.fix), stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=60)
        good = r.returncode == want_rc
        print("NATIVE %s argv=%s rc=%d expect=%d %s" % (
            pid, " ".join(argv), r.returncode, want_rc, "ok" if good else "fail"))
        if not good:
            bad.append(pid)
    return bad


def met(exp, pid, want, rc, out):
    """Verdict for one probe run: met, mismatch (valid run, wrong verdict), or invalid."""
    if "FIGURE-AUDIT figures=1 " not in out or rc not in (0, 1):
        return "invalid"
    kind, val = exp
    if kind == "ok":
        good = rc == 0 and ("FIG %s recorded=%s derived=%s ok\n" % (pid, want, val)) in out
    else:
        good = rc == 1 and ("derived=UNAVAILABLE reason=%s stale\n" % val) in out
    return "met" if good else "mismatch"


def run_probes(instrument, contract, ctx):
    results = []
    for pid, derive, want, cand, base, _native in PROBES:
        ledger = ctx.ledgers / (pid + ".json")
        doc = {"figures": [{"id": pid, "record": "fixture:1", "recorded": want,
                            "derive": derive, "want": want}]}
        ledger.write_text(json.dumps(doc) + "\n", encoding="utf-8", newline="\n")
        exp = cand if contract == "candidate" else base
        try:
            r = subprocess.run([sys.executable, str(instrument), "--ledger", str(ledger),
                                "--root", str(ctx.fix)], cwd=str(ctx.fix), env=ctx.env,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, timeout=300)
            verdict = met(exp, pid, want, r.returncode, r.stdout)
        except subprocess.TimeoutExpired:
            verdict = "invalid"
        results.append((pid, verdict))
    return results


def selftest(path, cwd, ctx):
    try:
        r = subprocess.run([sys.executable, str(path), "--selftest"], cwd=str(cwd),
                           env=ctx.env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return -1, "timeout"
    lines = (r.stdout or "").strip().splitlines()
    return r.returncode, (lines[-1] if lines else "")


def construct(pristine):
    failures = []
    if len({mid for mid, _o, _n in MUTANTS}) != len(MUTANTS):
        failures.append("duplicate-mutant-id")
    try:
        compile(pristine, "pristine", "exec")
    except SyntaxError as exc:
        failures.append("pristine-compile:%s" % exc.msg)
    for mid, old, new in MUTANTS:
        sites = pristine.count(old)
        kind = mid[0]
        if kind == "i":
            verdict = "rejected" if sites != 1 else "accepted-unexpectedly"
            if sites == 1:
                failures.append(mid)
        else:
            verdict = "exact-once" if sites == 1 else "exact-once-fail"
            if sites != 1:
                failures.append(mid)
            else:
                try:
                    compile(pristine.replace(old, new, 1), mid, "exec")
                    verdict += " compile=ok"
                except SyntaxError as exc:
                    verdict += " compile=fail(%s)" % exc.msg
                    failures.append(mid)
        print("CONSTRUCT %s kind=%s sites=%d verdict=%s" % (mid, kind, sites, verdict))
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--instrument", required=True, type=Path)
    ap.add_argument("--work", required=True, type=Path)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--construct-only", action="store_true")
    mode.add_argument("--contract", choices=["candidate", "base"], default="candidate")
    args = ap.parse_args()

    inst = args.instrument.resolve()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    data = inst.read_bytes()
    pristine_text = data.decode("utf-8")
    label = "construct-only" if args.construct_only else args.contract
    print("run_utc=%s" % utc())
    print("instrument=%s sha256=%s bytes=%d mode=%s" % (inst, sha(data), len(data), label))
    print("python=%s work=%s" % (sys.version.split()[0], work))

    ctx = Ctx(work)
    if args.construct_only:
        bad = native_check(ctx)
        failures = construct(pristine_text) + bad
        print("construct-only failures=%d verdict=%s" % (len(failures),
                                                        "pass" if not failures else "fail"))
        return 0 if not failures else 1

    bad = native_check(ctx)
    if bad:
        print("native-fixture exact-exit=fail probes=%s verdict=fail" % ",".join(bad))
        return 2

    if args.contract == "base":
        res = run_probes(inst, "base", ctx)
        for pid, v in res:
            print("PROBE base %s verdict=%s" % (pid, v))
        met_n = sum(1 for _p, v in res if v == "met")
        print("base-probes met=%d/%d verdict=%s" % (met_n, len(res),
                                                  "pass" if met_n == len(res) else "fail"))
        return 0 if met_n == len(res) else 1

    failures = []
    rc, last = selftest(inst, ctx.pristine, ctx)
    p_self = rc == 0
    print("PRISTINE selftest_exit=%d last=%r" % (rc, last))
    res = run_probes(inst, "candidate", ctx)
    for pid, v in res:
        print("PROBE pristine %s verdict=%s" % (pid, v))
    p_probes = all(v == "met" for _p, v in res)
    if not (p_self and p_probes):
        failures.append("pristine")

    limb_kills = {limb: 0 for limb in LIMBS}
    eq_held = ctl_held = inv_rejected = 0
    for mid, old, new in MUTANTS:
        kind = mid[0]
        sites = pristine_text.count(old)
        if sites != 1:
            if kind == "i":
                inv_rejected += 1
                print("MUT %s kind=i sites=%d verdict=rejected-exact-once" % (mid, sites))
            else:
                failures.append(mid)
                print("MUT %s kind=%s sites=%d verdict=exact-once-fail" % (mid, kind, sites))
            continue
        if kind == "i":
            failures.append(mid)
            print("MUT %s kind=i sites=1 verdict=accepted-unexpectedly" % mid)
            continue
        text = pristine_text.replace(old, new, 1)
        try:
            compile(text, mid, "exec")
        except SyntaxError as exc:
            failures.append(mid)
            print("MUT %s kind=%s sites=1 compile=fail detail=%s" % (mid, kind, exc.msg))
            continue
        d = ctx.muts / mid
        d.mkdir(parents=True)
        path = d / "figure-audit.py"
        path.write_bytes(text.encode("utf-8"))
        st_rc, st_last = selftest(path, d, ctx)
        st_valid = st_rc in (0, 1) and st_last.startswith("selftest cases=")
        st_killed = st_valid and st_rc == 1
        probes = run_probes(path, "candidate", ctx)
        mism = [pid for pid, v in probes if v == "mismatch"]
        inval = [pid for pid, v in probes if v == "invalid"]
        valid = st_valid and not inval
        probe_killed = bool(mism)
        if kind == "m":
            ok = valid and probe_killed
            if ok:
                limb_kills[LIMB_OF[mid.split("-")[1]]] += 1
        else:
            ok = valid and not probe_killed and not st_killed
            if ok:
                if kind == "e":
                    eq_held += 1
                else:
                    ctl_held += 1
        if not ok:
            failures.append(mid)
        print("MUT %s kind=%s sites=1 compile=ok sha256=%s selftest_exit=%d "
              "selftest_valid=%s selftest_killed=%s probe_mismatch=%s probe_invalid=%s "
              "probe_killed=%s verdict=%s" % (
                  mid, kind, sha(text.encode("utf-8")), st_rc, st_valid, st_killed,
                  ",".join(mism) or "-", ",".join(inval) or "-", probe_killed,
                  "pass" if ok else "fail"))

    limbs_ok = all(limb_kills[l] >= MIN_PER_LIMB for l in LIMBS)
    if not limbs_ok:
        failures.append("limb-count")
    if eq_held < 1 or ctl_held < 1:
        failures.append("equivalent-or-control-count")
    if inv_rejected != 2:
        failures.append("invalid-controls")
    print("mutbat-r64 pristine=%s limbs=%s equivalents_held=%d controls_held=%d "
          "invalid_rejected=%d failures=%d verdict=%s" % (
              "pass" if p_self and p_probes else "fail",
              ",".join("%s:%d" % (l, limb_kills[l]) for l in LIMBS),
              eq_held, ctl_held, inv_rejected, len(failures),
              "pass" if not failures else "fail"))
    return 0 if not failures else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, UnicodeError, subprocess.SubprocessError) as exc:
        print("mutbat-r64 unavailable=%s detail=%s" % (type(exc).__name__, exc),
              file=sys.stderr)
        sys.exit(2)
