#!/usr/bin/env python3
"""mutate_battery.py — mutation-test r46-mutbat.py (the round-46 battery runner) itself.

Each mutant is a SINGLE-LINE edit of a scratch COPY of the committed runner (the
committed file is never modified).  Each mutated runner is executed against scenario
trees whose selftest is a stub replaying the FROZEN per-mutant failure counts
(controls/mutbat-before.txt), so the runner's own grading / printing / exit logic is
exercised in seconds instead of hours.

DETECTORS
  D1  OUTPUT CONTRACT (the runner's own stdout + exit status; contract_check.py):
      summary vs per-mutant lines, verdict vs mutant_failures, exit status vs the
      printed summary, id set vs the mutant table, baseline_failures consistency.
  D2  REFERENCE DIFF: the mutated stdout+exit vs the PRISTINE runner's stdout+exit on
      the SAME scenario (and vs the frozen receipt for S1).

verdict:  KILLED-D1  the mutated output violates the output contract
          KILLED-D2  the mutated output satisfies the contract but differs from the
                    pristine runner's output on the same scenario
          SURVIVED   the mutated output is indistinguishable from the pristine runner's

Usage: python3 mutate_battery.py [--only MUTID] [--scen S1,S2]
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r46/R46bMutBattery"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BATTERY = os.path.join(LANE, "corpus/instruments/r46-mutbat.py")
RECEIPT = os.path.join(LANE, ".ufo/waves/round-46/attempt2/controls/mutbat-before.txt")
CHECKER = os.path.join(S, "contract_check.py")
STUB = os.path.join(S, "stub-selftest.py")

spec = importlib.util.spec_from_file_location("r46mut", BATTERY)
MOD = importlib.util.module_from_spec(spec)
spec.loader.exec_module(MOD)

expected_fail = {}
for ln in open(RECEIPT, encoding="utf-8"):
    ln = ln.strip()
    if ln.startswith("mutant="):
        p = dict(kv.split("=", 1) for kv in ln.split())
        expected_fail[p["mutant"]] = int(p["mutant_failures"])

BAT_SRC = open(BATTERY, encoding="utf-8").read()
STUB_TMPL = open(STUB, encoding="utf-8").read()


def sha(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def table_for(counter_texts):
    table = {}
    for which in ("c1", "c2"):
        cname, mutants, _ = MOD.COUNTER[which]
        text = counter_texts[which]
        table[sha(text)] = 0
        for mid, old, new in mutants:
            if text.count(old) != 1:
                continue  # drifted anchor: the runner is expected to fail loudly there
            table[sha(text.replace(old, new, 1))] = expected_fail[mid]
    return table


def write_tree(tree, counter_texts, table, crash_c1=False, unreadable=None):
    shutil.rmtree(tree, ignore_errors=True)
    inst = os.path.join(tree, "corpus", "instruments")
    os.makedirs(inst)
    for which, g in (("c1", "r46-c1-gate.py"), ("c2", "r46-c2-gate.py")):
        open(os.path.join(inst, g), "w", encoding="utf-8").write(counter_texts[which])
    body = STUB_TMPL.replace("__TABLE__", json.dumps(table, indent=1, sort_keys=True))
    for st in ("r46-counters-selftest-c1.py", "r46-counters-selftest-c2.py"):
        p = os.path.join(inst, st)
        open(p, "w", encoding="utf-8").write(
            "#!/usr/bin/env python3\nimport sys\nsys.stderr.write('selftest crashed: boom\\n')\nsys.exit(2)\n"
            if (crash_c1 and st.endswith("c1.py")) else body)
        os.chmod(p, 0o644)
    if unreadable:
        p = os.path.join(inst, unreadable)
        open(p, "w", encoding="utf-8").write("unreadable probe\n")
        os.chmod(p, 0o000)
    return tree


base_c1 = open(os.path.join(S, "stubtree/corpus/instruments/r46-c1-gate.py"), encoding="utf-8").read()
base_c2 = open(os.path.join(S, "stubtree/corpus/instruments/r46-c2-gate.py"), encoding="utf-8").read()

SCEN = {}

# S1: the frozen-receipt scenario (both counters, no --equivalent map)
t1 = os.path.join(S, "sc-S1")
texts1 = {"c1": base_c1, "c2": base_c2}
write_tree(t1, texts1, table_for(texts1))
SCEN["S1"] = dict(tree=t1, args=[], note="frozen-receipt scenario")

# S2: with an --equivalent map (one real proof file, one dangling proof path)
t2 = os.path.join(S, "sc-S2")
texts2 = {"c1": base_c1, "c2": base_c2}
write_tree(t2, texts2, table_for(texts2))
proof = os.path.join(S, "proof-G1c.md")
open(proof, "w", encoding="utf-8").write("# committed proof for G1c-src-boundary\n")
eqmap = {"G1c-src-boundary": proof,
         "G2a-verified-prefix": os.path.join(S, "NO-SUCH-PROOF.md")}
json.dump(eqmap, open(os.path.join(S, "eqmap.json"), "w"), indent=1)
SCEN["S2"] = dict(tree=t2, args=["--equivalent", os.path.join(S, "eqmap.json")],
                   note="with an --equivalent map (one real proof, one dangling proof path)")

# S3: drift — the M16 anchor "MIN_ROWS = 6" no longer occurs in the c1 counter
t3 = os.path.join(S, "sc-S3")
texts3 = {"c1": base_c1.replace("MIN_ROWS = 6", "MIN_ROWS = 7", 1), "c2": base_c2}
write_tree(t3, texts3, table_for(texts3))
SCEN["S3"] = dict(tree=t3, args=[], note="drift: one mutant's anchor no longer occurs (the runner must fail loudly)")

# S4: the c1 selftest crashes (prints no verdict at all)
t4 = os.path.join(S, "sc-S4")
texts4 = {"c1": base_c1, "c2": base_c2}
write_tree(t4, texts4, table_for(texts4), crash_c1=True)
SCEN["S4"] = dict(tree=t4, args=[], note="the c1 selftest crashes (the runner must report BASELINE-DIRTY)")

# S5: the tree's instruments dir holds an unreadable file -> the mutant copy fails
t5 = os.path.join(S, "sc-S5")
texts5 = {"c1": base_c1, "c2": base_c2}
write_tree(t5, texts5, table_for(texts5), unreadable="unreadable-probe.txt")
SCEN["S5"] = dict(tree=t5, args=[], note="the mutant copy fails (the runner must fail loudly, not skip silently)")

# S6: exactly one mutant's selftest crashes (the selftest emits no verdict for it)
t6 = os.path.join(S, "sc-S6")
texts6 = {"c1": base_c1, "c2": base_c2}
write_tree(t6, texts6, table_for(texts6))
# the crashing mutant: M06-L3-home-dropped (frozen receipt: mutant_failures=0)
CRASH_SHA = None
for _w in ("c1", "c2"):
    for _mid, _old, _new in MOD.COUNTER[_w][1]:
        if _mid == "M06-L3-home-dropped":
            CRASH_SHA = sha(texts6[_w].replace(_old, _new, 1))
assert CRASH_SHA
crash_stub = ("#!/usr/bin/env python3\n"
              "import argparse, hashlib, os, sys\n"
              "ap = argparse.ArgumentParser()\n"
              "ap.add_argument('--counter')\n"
              "ap.add_argument('--pure')\n"
              "ap.add_argument('--work')\n"
              "ap.add_argument('--jobs')\n"
              "ap.add_argument('--lane')\n"
              "a, _unknown = ap.parse_known_args()\n"
              "p = a.counter or os.path.join(os.getcwd(), 'corpus', 'instruments', 'r46-c1-gate.py')\n"
              "if hashlib.sha256(open(p, 'rb').read()).hexdigest() == %r:\n"
              "    sys.stderr.write('selftest crashed for this counter: boom\\n')\n"
              "    sys.exit(2)\n"
              "sys.stdout.write('selftest cases=1 failures=0\\n')\n"
              "sys.exit(0)\n") % CRASH_SHA
open(os.path.join(t6, "corpus/instruments/r46-counters-selftest-c1.py"), "w", encoding="utf-8").write(crash_stub)
SCEN["S6"] = dict(tree=t6, args=[], note="one mutant's selftest crashes (the runner must still print its line)")

MUTANTS = [
    ("B01", "caught-when-failures-zero",
     "grades a mutant as caught when the selftest reported failures=0",
     "            if mf >= 1:", "            if mf >= 0:"),
    ("B02", "swap-caught-equivalent-in-summary",
     "the summary line prints the caught and equivalent counts swapped",
     "              (which, len(mutants), caught, equivalent, uncaught))",
     "              (which, len(mutants), equivalent, caught, uncaught))"),
    ("B03", "swap-verdict-label-equivalent",
     "an equivalent mutant is labelled verdict=caught",
     '                verdict = "equivalent"', '                verdict = "caught"'),
    ("B04", "equivalent-without-proof-file",
     "a mutant is credited equivalent although its proof file does not exist",
     "            elif mid in eq and os.path.isfile(eq[mid]):", "            elif mid in eq:"),
    ("B05", "exit-0-despite-uncaught",
     "exits 0 although the summary reports uncaught>0",
     "    return 1 if bad else 0", "    return 0"),
    ("B06", "skip-a-mutant-silently",
     "silently skips the last mutant (the summary still claims the full mutant count)",
     "        for mid, old, new in mutants:", "        for mid, old, new in mutants[:-1]:"),
    ("B07", "apply-failure-swallowed",
     "the apply/drift guard is swallowed: an inapplicable mutant is silently graded",
     '        raise SystemExit("mutant=%s old-substring occurs %d times (expected 1) — battery vs counter drift" % (mid, n))',
     "        return None"),
    ("B08", "baseline-dirty-ignored",
     "a dirty baseline is not detected; mutants are graded against it",
     "        if baseline != 0:", "        if baseline == 999:"),
    ("B09", "uncaught-not-counted",
     "uncaught mutants are not counted in the summary",
     "                uncaught += 1", "                uncaught += 0"),
    ("B10", "verdict-label-uncaught-to-caught",
     "an uncaught mutant is labelled verdict=caught",
     '                verdict = "uncaught"', '                verdict = "caught"'),
    ("B11", "exit-flag-not-set",
     "the exit-status accumulator is never incremented",
     "            bad += 1\n    return 1 if bad else 0", "            bad += 0\n    return 1 if bad else 0"),
    ("B12", "mutant-count-lie",
     "the summary claims one more mutant than were run",
     "              (which, len(mutants), caught, equivalent, uncaught))",
     "              (which, len(mutants) + 1, caught, equivalent, uncaught))"),
    ("B13", "per-mutant-line-omitted",
     "a mutant that produced no verdict gets no per-mutant line at all",
     '            print("mutant=%s baseline_failures=0 mutant_failures=%d verdict=%s" % (mid, mf, verdict))',
     '            print("mutant=%s baseline_failures=0 mutant_failures=%d verdict=%s" % (mid, mf, verdict)) if mf >= 0 else None'),
]

MUTANTS_MULTI = [
    ("M01", "copy-failure-skipped-silently",
     "a failed mutant copy is swallowed and the mutant is skipped silently",
     "            finally:\n                shutil.rmtree(mdir, ignore_errors=True)",
     "            except Exception:\n                continue\n"
     "            finally:\n                shutil.rmtree(mdir, ignore_errors=True)"),
]

MUTANTS_NOOP = [
    ("N01", "do-nothing-control",
     "comment-only edit; the output must be identical to the pristine runner's",
     "    bad = 0", "    bad = 0  # noqa: do-nothing control"),
]


def write_mutant(mid, anchor, repl):
    n = BAT_SRC.count(anchor)
    if n != 1:
        raise SystemExit("mutant %s: anchor occurs %d times" % (mid, n))
    out = BAT_SRC.replace(anchor, repl, 1)
    a = BAT_SRC.split("\n")
    b = out.split("\n")
    diff = [i + 1 for i in range(min(len(a), len(b))) if a[i] != b[i]]
    if len(a) != len(b):
        diff.append("+%d lines" % (len(b) - len(a)))
    path = os.path.join(S, "mutbat-%s.py" % mid)
    open(path, "w", encoding="utf-8").write(out)
    return path, diff


def run(battery_path, scen, tag):
    sc = SCEN[scen]
    work = os.path.join(S, "work", "%s-%s" % (tag, scen))
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)
    env = dict(os.environ, TMPDIR=work)
    cmd = [sys.executable, "-B", battery_path, "--root", sc["tree"], "--pure", os.path.join(S, "pure"),
           "--work", os.path.join(work, "w"), "--counter", "both", "--jobs", "8"] + sc["args"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, env=env, cwd=sc["tree"])
    os.makedirs(os.path.join(S, "out"), exist_ok=True)
    out = os.path.join(S, "out", "%s-%s.txt" % (tag, scen))
    open(out, "w", encoding="utf-8").write(p.stdout)
    open(out + ".err", "w", encoding="utf-8").write(p.stderr)
    open(out + ".cmd", "w", encoding="utf-8").write(" ".join(cmd) + "\n")
    return out, p.returncode, p.stdout, p.stderr


def check(out, rc, scen):
    args = [sys.executable, "-B", CHECKER, out, str(rc), "--expect-counters", "c1,c2",
            "--mutants", "c1=%d,c2=%d" % (len(MOD.COUNTER["c1"][1]), len(MOD.COUNTER["c2"][1])),
            "--ids", "c1=%s,c2=%s" % (os.path.join(S, "ids-c1.txt"), os.path.join(S, "ids-c2.txt"))]
    if scen == "S2":
        args += ["--equivalent", os.path.join(S, "eqmap.json")]
    p = subprocess.run(args, capture_output=True, text=True)
    return p.returncode == 0, p.stdout


def main(argv):
    only = None
    scens = list(SCEN)
    i = 0
    while i < len(argv):
        if argv[i] == "--only":
            only = argv[i + 1]
            i += 2
        elif argv[i] == "--scen":
            scens = argv[i + 1].split(",")
            i += 2
        else:
            i += 1

    results = []
    ctrl = {}
    for scen in scens:
        ctrl_out, rc, so, se = run(BATTERY, scen, "CONTROL")
        ctrl[scen] = (so, rc)
        d1ok, d1msg = check(ctrl_out, rc, scen)
        results.append(dict(mutant="CONTROL", scen=scen, rc=rc, d1=d1ok, d1msg=d1msg.strip(),
                            same_as_control=True, verdict="CONTROL"))
        print("CONTROL %-3s rc=%d d1=%s  | %s" % (scen, rc, "OK" if d1ok else "FAIL", SCEN[scen]["note"]))
        for l in d1msg.strip().split("\n"):
            print("      " + l)

    for spec_m in MUTANTS + MUTANTS_MULTI + MUTANTS_NOOP:
        mid, cls, desc, anchor, repl = spec_m
        if only and mid != only:
            continue
        path, diff = write_mutant(mid, anchor, repl)
        for scen in scens:
            out, rc, so, se = run(path, scen, mid)
            d1ok, d1msg = check(out, rc, scen)
            cso, crc = ctrl[scen]
            same = (so == cso) and (rc == crc)
            verdict = "KILLED-D1" if not d1ok else ("SURVIVED" if same else "KILLED-D2")
            print("%-4s %-3s %-32s lines=%s rc=%d  %s" % (mid, scen, cls, diff, rc, verdict))
            if not d1ok:
                for l in d1msg.strip().split("\n"):
                    print("      " + l)
            results.append(dict(mutant=mid, scen=scen, cls=cls, desc=desc, lines=diff, rc=rc,
                                 d1=d1ok, d1msg=d1msg.strip(), same_as_control=same, verdict=verdict))
    json.dump(results, open(os.path.join(S, "results.json"), "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
