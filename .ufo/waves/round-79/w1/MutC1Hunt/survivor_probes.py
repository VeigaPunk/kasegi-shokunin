#!/usr/bin/env python3
"""MutC1Hunt survivor probes — distinguish "equivalent" from "real gap" for each survivor.

Read-only on the lane; all fixtures under the scratch root. Outputs into <OUT>/probes/.
"""
import ast
import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
PRISTINE = LANE + "/.ufo/waves/round-79/c1/recheck-cwd-census.py"
OUT = LANE + "/.ufo/waves/round-79/w1/MutC1Hunt"
S = "/fast/scratch/hyaku/kasegi-r79/MutC1Hunt"
PROBE = S + "/probes"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_selftest(path):
    env = dict(os.environ)
    env["TMPDIR"] = S
    p = subprocess.run([sys.executable, "-B", path, "--selftest"], env=env,
                       stdin=subprocess.DEVNULL, capture_output=True, text=True,
                       timeout=600, cwd=OUT)
    return p.returncode, p.stdout + p.stderr


def census_counts(mod, root):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        counts = mod.census(root, root, False)
    return counts, buf.getvalue()


def main():
    shutil.rmtree(PROBE, ignore_errors=True)
    os.makedirs(PROBE)
    os.makedirs(OUT + "/probes", exist_ok=True)
    rows = {}

    # --- N10: _calls recursion through consumed() accepts a wrong predicate -------
    bad_wiring = 'check("gate-consume", consumed(x, gate_negpolarity_ok(False)), "")\n'
    p = load(PRISTINE, "pristine_n10")
    m = load(OUT + "/mutants/N10-calls-recurse-true.py", "mut_n10")
    rows["N10"] = {
        "probe_source": bad_wiring.strip(),
        "pristine_wiring_findings": p.wiring_findings(bad_wiring),
        "mutant_wiring_findings": m.wiring_findings(bad_wiring),
    }
    rows["N10"]["differs"] = (rows["N10"]["pristine_wiring_findings"]
                              != rows["N10"]["mutant_wiring_findings"])

    # --- N26: gate_checkids_ok equality vs superset -------------------------------
    p = load(PRISTINE, "pristine_n26")
    m = load(OUT + "/mutants/N26-gatecheckids-superset.py", "mut_n26")
    rows["N26"] = {
        "case_done_superset": {
            "args": 'done=["a","b"], required=["a"], side_logs=[[True]]',
            "pristine": p.gate_checkids_ok(["a", "b"], ["a"], [[True]]),
            "mutant": m.gate_checkids_ok(["a", "b"], ["a"], [[True]]),
        },
        "case_missing": {
            "args": 'done=["a"], required=["a","b"], side_logs=[[True]]',
            "pristine": p.gate_checkids_ok(["a"], ["a", "b"], [[True]]),
            "mutant": m.gate_checkids_ok(["a"], ["a", "b"], [[True]]),
        },
    }
    rows["N26"]["differs"] = (rows["N26"]["case_done_superset"]["pristine"]
                              != rows["N26"]["case_done_superset"]["mutant"])

    # --- N21: exit_other bucket (a recheck exiting 7) ------------------------------
    root21 = os.path.join(PROBE, "case-exit7")
    kdir = os.path.join(root21, "corpus", "knowledge")
    os.makedirs(kdir)
    with open(os.path.join(kdir, "x.md"), "w", encoding="utf-8") as fh:
        fh.write("# fixture\nrecheck: cd %s && exit 7\n" % root21)
    p = load(PRISTINE, "pristine_n21")
    m = load(OUT + "/mutants/N21-census-exitother-to-exit1.py", "mut_n21")
    c_p, _ = census_counts(p, root21)
    c_m, _ = census_counts(m, root21)
    rows["N21"] = {"fixture": "one prefixed entry `cd <root> && exit 7`",
                   "pristine_counts": {k: c_p[k] for k in ("exit_other", "exit1_foreign")},
                   "mutant_counts": {k: c_m[k] for k in ("exit_other", "exit1_foreign")}}
    rows["N21"]["differs"] = (c_p["exit_other"] != c_m["exit_other"])

    # --- N30: run_foreign cwd=None inherits the caller cwd ------------------------
    work30 = os.path.join(PROBE, "cwd-work")
    os.makedirs(work30)
    with open(os.path.join(work30, "probe.py"), "w", encoding="utf-8") as fh:
        fh.write("import sys\nsys.exit(0)\n")
    root30 = os.path.join(PROBE, "case-relative")
    kdir30 = os.path.join(root30, "corpus", "knowledge")
    os.makedirs(kdir30)
    with open(os.path.join(kdir30, "x.md"), "w", encoding="utf-8") as fh:
        fh.write("# fixture\nrecheck: python3 probe.py\n")
    p = load(PRISTINE, "pristine_n30")
    m = load(OUT + "/mutants/N30-runforeign-cwd-inherit.py", "mut_n30")
    old_cwd = os.getcwd()
    os.chdir(work30)
    try:
        c_p, _ = census_counts(p, root30)
        c_m, _ = census_counts(m, root30)
    finally:
        os.chdir(old_cwd)
    rows["N30"] = {"fixture": "unprefixed entry `python3 probe.py`; probe.py exists in the caller cwd only",
                   "pristine_counts": {k: c_p[k] for k in ("noprefix", "exit2_foreign", "exit0_foreign")},
                   "mutant_counts": {k: c_m[k] for k in ("noprefix", "exit2_foreign", "exit0_foreign")}}
    rows["N30"]["differs"] = (c_p["exit2_foreign"] != c_m["exit2_foreign"])

    # --- N27: the case-7 ok expression ignores rest7 ------------------------------
    want7 = {"entries": 2, "restoration_only": 0, "norecheck": 0, "noprefix": 0,
             "exit2_foreign": 0, "exit0_foreign": 2}
    got7 = dict(want7)
    first7 = True
    rest7 = True  # hypothetical regression: both-header entry executes restoration-recheck
    pristine_ok = all(got7[k] == v for k, v in want7.items()) and first7 and not rest7
    mutant_ok = all(got7[k] == v for k, v in want7.items()) and first7
    rows["N27"] = {"regression_simulated": "rest7=True (both-header entry executed its restoration-recheck)",
                   "pristine_ok": pristine_ok, "mutant_ok": mutant_ok}
    rows["N27"]["differs"] = pristine_ok != mutant_ok

    # --- N08/N09: the arity gates differ only on inputs that cannot run -----------
    tree = ast.parse(open(PRISTINE, encoding="utf-8").read())
    arities = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in ("check", "consumed"):
            arities[node.name] = len(node.args.args)
    rows["arity"] = {"helpers": arities,
                     "note": "check(case,ok,detail)/consumed(sink,value) are fixed-arity nested "
                             "helpers; a call with fewer/more positional args raises TypeError "
                             "before any wiring scan, so the >=2/>=3 gates are equivalent"}

    # --- N11 masking probe: delete-row + predicates_ok empty special case ----------
    n11_src = open(OUT + "/mutants/N11-rows-drop-empty.py", encoding="utf-8").read()
    pred_anchor = ("def predicates_ok(rows):\n"
                   "    return bool(rows) and all(got == want for got, want in rows)\n")
    pred_repl = ("def predicates_ok(rows):\n"
                 "    return (not rows) or all(got == want for got, want in rows)\n")
    pristine_src = open(PRISTINE, encoding="utf-8").read()
    assert pristine_src.count(pred_anchor) == 1
    assert n11_src.count(pred_anchor) == 1
    def write(path, text):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path
    a = write(OUT + "/composites/MASK-A-predicates-empty-on-pristine.py",
              pristine_src.replace(pred_anchor, pred_repl, 1))
    b = write(OUT + "/composites/MASK-B-predicates-empty-on-N11.py",
              n11_src.replace(pred_anchor, pred_repl, 1))
    rc_a, out_a = run_selftest(a)
    rc_b, out_b = run_selftest(b)
    write(OUT + "/out/MASK-A-predicates-empty-on-pristine.out", "rc=%d\n%s" % (rc_a, out_a))
    write(OUT + "/out/MASK-B-predicates-empty-on-N11.out", "rc=%d\n%s" % (rc_b, out_b))
    rows["N11_masking"] = {"predicates_ok_defect": "return (not rows) or all(...)  # differs only on rows==[]",
                           "pristine_rc": rc_a,
                           "pristine_fail_cases": [ln.split()[1] for ln in out_a.splitlines()
                                                   if " FAIL " in ln and ln.startswith("selftest case=")],
                           "N11_rc": rc_b,
                           "N11_fail_cases": [ln.split()[1] for ln in out_b.splitlines()
                                              if " FAIL " in ln and ln.startswith("selftest case=")]}

    # --- N26 masking probe: superset predicate hides a REQUIRED_CHECKS removal -----
    n26_src = open(OUT + "/mutants/N26-gatecheckids-superset.py", encoding="utf-8").read()
    req_anchor = '"tmpdir-refusal",\n        "gate-predicates", "gate-wiring"))'
    req_repl = '"tmpdir-refusal",\n        "gate-predicates"))'
    assert n26_src.count(req_anchor) == 1
    c = write(OUT + "/composites/MASK-C-N26+required-drop-wiring.py",
              n26_src.replace(req_anchor, req_repl, 1))
    rc_c, out_c = run_selftest(c)
    write(OUT + "/out/MASK-C-N26+required-drop-wiring.out", "rc=%d\n%s" % (rc_c, out_c))
    rows["N26_masking"] = {"defect": "REQUIRED_CHECKS loses gate-wiring (the N14 transform)",
                           "rc": rc_c,
                           "fail_cases": [ln.split()[1] for ln in out_c.splitlines()
                                          if " FAIL " in ln and ln.startswith("selftest case=")]}

    # --- N25: gate_checkids_ok only inspects the first side log --------------------
    p = load(PRISTINE, "pristine_n25")
    m = load(OUT + "/mutants/N25-gatecheckids-firstsidelog.py", "mut_n25")
    rows["N25"] = {
        "args": 'done=["a"], required=["a"], side_logs=[[True],[False]]',
        "pristine": p.gate_checkids_ok(["a"], ["a"], [[True], [False]]),
        "mutant": m.gate_checkids_ok(["a"], ["a"], [[True], [False]]),
        "first_log_false": {
            "args": 'done=["a"], required=["a"], side_logs=[[False],[True]]',
            "pristine": p.gate_checkids_ok(["a"], ["a"], [[False], [True]]),
            "mutant": m.gate_checkids_ok(["a"], ["a"], [[False], [True]]),
        },
    }
    rows["N25"]["differs"] = (rows["N25"]["pristine"] != rows["N25"]["mutant"])

    # --- N13: the dropped limb is exactly the rows[13] proposition ----------------
    rows["N13_note"] = ("side_logs third = predicates_ok([(True, False)]) is False; "
                        "rows[13] = (predicates_ok([(True, False)]), False) is the same "
                        "proposition over the same input, so the limb is redundant on all inputs")

    with open(OUT + "/probes/probes.json", "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1, sort_keys=True)
    for key in ("N10", "N21", "N25", "N26", "N27", "N30", "N11_masking", "N26_masking", "arity"):
        print("PROBE %s %s" % (key, json.dumps(rows[key], sort_keys=True)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
