#!/usr/bin/env python3
"""Round-81 MutC1Hunt driver: single-transform mutants of the frozen r81 C1 candidate
(recheck-cwd-census.py) OUTSIDE the frozen 59-row table, plus the ten round-80 MutC1Hunt
survivors not carried into that table, re-run against the r81 bytes.

Detector: the frozen r81 counter's classifier (mutbat.py: fail_lines/clean_pass/verdict),
imported read-only; each mutant runs as `python3 -B <mutant> --selftest` from a fresh
directory with TMPDIR set to a fresh dir under the seat scratch root.

Rows are single transforms. For every row that ends SURVIVED (or DIRTY) a probe records a
pristine-vs-mutant behavioural comparison (in-process module calls, or a composed second
transform whose detection the surviving mutant is supposed to keep alive).
"""
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

S = "/fast/scratch/hyaku/kasegi-r81/MutC1Hunt"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
C1 = LANE + "/.ufo/waves/round-81/c1"
FROZEN = C1 + "/recheck-cwd-census.py"
TABLE_PATH = C1 + "/mutant-table.json"
MUTBAT = C1 + "/mutbat.py"
WAVE = LANE + "/.ufo/waves/round-81/w1/MutC1Hunt"
EXPECT_CASES = 22
EXPECT_SHA = "a3b58aa52ba0744199ee97e6bd837e62c499e3e6af03a2fc26f0e6e3746dbec0"

# ------------------------------------------------------------------ detector (frozen)
def _load_mutbat():
    spec = importlib.util.spec_from_file_location("frozen_mutbat", MUTBAT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MB = _load_mutbat()
TABLE = json.load(open(TABLE_PATH, encoding="utf-8"))
TABLE_PAIRS = {(r["anchor"], r["replacement"]) for r in TABLE}

# ------------------------------------------------------------------ candidate rows
def row(rid, anchor, replacement, kill_cases, desc, probe=None, cls="assertion"):
    return {"id": rid, "anchor": anchor, "replacement": replacement,
            "kill_cases": kill_cases, "desc": desc, "probe": probe, "class": cls}


ROWS = [
    # ---------- seven round-81 selftest checks ----------
    row("RC01", '    prefix = "cd %s && " % lane\n',
        '    prefix = "cd %s &&  " % lane\n', ["prefix-census"],
        "prefix literal gains a double space (all fixtures become prefix-less)"),
    row("RC02", '        want14 = {"entries": 3, "noprefix": 2, "exit2_foreign": 0, "exit0_foreign": 2,\n'
                '                  "exit1_foreign": 1, "exit_other": 0, "norecheck": 0}\n',
        '        want14 = {"entries": 3, "noprefix": 1, "exit2_foreign": 0, "exit0_foreign": 2,\n'
        '                  "exit1_foreign": 1, "exit_other": 0, "norecheck": 0}\n',
        ["prefix-literal"], "prefix-literal expected noprefix count lowered"),
    row("RC03", '        write_entry(kdir14, "a-lane-suffix.md", "recheck: cd %s-x && true\\n" % root14)\n',
        '', ["prefix-literal"], "lane-suffix fixture deleted"),
    row("RC04", '        write_entry(kdir14, "b-no-space.md", "recheck: cd %s &&true\\n" % root14)',
        '        write_entry(kdir14, "b-no-space.md", "recheck: cd %s && true\\n" % root14)',
        ["prefix-literal"], "no-space fixture repaired (prefix-less probe removed)"),
    row("RC05", '              ret15e == 1 and "RECHECK-CWD-RESULT nonconformant" in out15e\n'
                '              and ret15n == 1 and "RECHECK-CWD-RESULT nonconformant" in out15n\n'
                '              and "norecheck=1 restoration_only=0" in out15n,\n',
        '              ret15e == 1 and "RECHECK-CWD-RESULT nonconformant" in out15e\n'
        '              and ret15n == 1 and "RECHECK-CWD-RESULT nonconformant" in out15n,\n',
        ["conform-limbs"],
        "conform-limbs bucket-line conjunct deleted (no constant operand)", probe="compose_table:S37"),
    row("RC06", '        write_entry(kdir15e, "x-exit2.md", "recheck: cd %s && exit 2\\n" % root15e)\n',
        '        write_entry(kdir15e, "x-exit2.md", "recheck: cd %s && exit 1\\n" % root15e)\n',
        ["conform-limbs"], "exit2-only fixture becomes exit1 (a conformant limb)"),
    row("RC07", '        write_entry(kdir15n, "n-note.md", "restoration-note: not a header\\n")\n',
        '        write_entry(kdir15n, "n-note.md", "restoration-recheck: not a header\\n")\n',
        ["conform-limbs"], "non-header restoration note becomes the real header"),
    row("RC08", '              ret15e == 1 and "RECHECK-CWD-RESULT nonconformant" in out15e\n',
        '              ret15e == 1\n', ["conform-limbs"],
        "conform-limbs drops the RESULT-line conjunct on the exit2 tree",
        probe="main_invariant"),
    row("RC09", '              ret16 == 2 and out16 == ""\n',
        '              ret16 == 2\n', ["tmpdir-file"],
        "tmpdir-file drops the empty-stdout conjunct", probe="bogus_stdout"),
    row("RC10", '              and "recheck-cwd: TMPDIR %s is not a directory" % file16 in err16.getvalue(),\n',
        '              and "is not a directory" in err16.getvalue(),\n', ["tmpdir-file"],
        "tmpdir-file stderr assertion loses the exact path/message",
        probe="tmpdir_file_message"),
    row("RC11", '              ret16 == 2 and out16 == ""',
        '              ret16 in (0, 2) and out16 == ""', ["tmpdir-file"],
        "tmpdir-file exit code tolerance widened to 0", probe="tmpdir_ret_tolerance"),
    row("RC12", '        write_entry(kdir17, "h-hang.md", "recheck: cd %s && exec sleep 30\\n" % root17)\n',
        '        write_entry(kdir17, "h-hang.md", "recheck: cd %s && exec sleep 0\\n" % root17)\n',
        ["timeout-bucket"], "hang fixture becomes a passing command"),
    row("RC13", '        want17 = {"entries": 1, "noprefix": 0, "exit2_foreign": 0, "exit0_foreign": 0,\n'
                '                  "exit1_foreign": 0, "exit_other": 1, "norecheck": 0}\n',
        '        want17 = {"entries": 1, "noprefix": 0, "exit2_foreign": 0, "exit0_foreign": 0,\n'
        '                  "exit1_foreign": 0, "exit_other": 0, "norecheck": 0}\n',
        ["timeout-bucket"], "timeout-bucket expected exit_other zeroed"),
    row("RC14", '        except subprocess.TimeoutExpired:\n            return -1',
        '        except subprocess.TimeoutExpired:\n            return 2', ["timeout-bucket"],
        "timeout sentinel changed from -1 to 2 (the exit2 bucket)"),
    row("RC15", '        finally:\n            globals()["TIMEOUT"] = saved_timeout17',
        '        finally:\n            pass', ["timeout-bucket"],
        "TIMEOUT patch restore deleted", probe="timeout_leak"),
    row("RC16", '        saved_tmp18 = os.environ.pop("TMPDIR", None)',
        '        saved_tmp18 = os.environ.get("TMPDIR")', ["tmpdir-unset"],
        "tmpdir-unset no longer unsets TMPDIR", probe="unset_states"),
    row("RC17", '        check("tmpdir-unset", refused18 is False and raised18 is None,',
        '        check("tmpdir-unset", refused18 in (False, None) and raised18 is None,',
        ["tmpdir-unset"], "tmpdir-unset truth test tolerance widened", probe="unset_truth"),
    row("RC18", '            if saved_tmp18 is not None:\n                os.environ["TMPDIR"] = saved_tmp18',
        '            os.environ["TMPDIR"] = saved_tmp18', ["tmpdir-unset"],
        "tmpdir-unset TMPDIR restore made unconditional", probe="unset_env_run"),
    row("RC19", '              ret19u == 2 and out19u == "" and "usage:" in err19.getvalue()\n',
        '              ret19u == 2 and out19u == ""\n', ["usage-guards"],
        "usage-guards drops the usage-line assertion", probe="usage_substring"),
    row("RC20", '              ret19u == 2 and out19u == ""',
        '              ret19u in (0, 2) and out19u == ""', ["usage-guards"],
        "usage-guards exit-code tolerance widened to 0", probe="compose_table:S30"),
    row("RC21", '              and exit19 == "recheck-cwd: no corpus/knowledge under %s" % os.path.abspath(root19e)\n',
        '', ["usage-guards"], "usage-guards drops the missing-corpus SystemExit message",
        probe="compose_table:S31"),
    row("RC22", '        write_entry(kdir19a, "p.md", "recheck: cd %s && true\\n" % lane19)',
        '        write_entry(kdir19a, "p.md", "recheck: cd %s && true\\n" % root19a)',
        ["usage-guards"], "distinct-lane fixture rebuilt on the root path",
        probe="compose_table:S39"),
    row("RC23", '    while i < len(argv):', '    while i < len(argv) - 1:',
        ["usage-guards"], "argument loop ignores the final token"),
    row("RC24", '        elif argv[i] == "--verbose":\n            verbose = True\n            i += 1',
        '        elif argv[i] == "--verbose":\n            verbose = False\n            i += 1',
        ["usage-guards"], "--verbose parsed but not honoured", probe="verbose_main"),
    row("RC25", '              and "ENTRY x-exit2.md noprefix=0 foreign_exit=2" in out15e\n'
                '              and "ENTRY a-prefixed.md" not in _t1,\n',
        '              and "ENTRY x-exit2.md noprefix=0 foreign_exit=2" in out15e,\n',
        ["output-lines"],
        "output-lines no-ENTRY conjunct deleted (no constant operand)",
        probe="force_entry_print"),
    row("RC49", '              and "norecheck=1 restoration_only=0" in out15n,\n',
        '              and True,\n', ["gate-wiring", "gate-checkids"],
        "conform-limbs stubbed with a constant-True conjunct (F1 probe)"),
    row("RC50", '              and "ENTRY a-prefixed.md" not in _t1,\n',
        '              and True,\n', ["gate-wiring", "gate-checkids"],
        "output-lines stubbed with a constant-True conjunct (F1 probe)"),
    row("RC26", '              "RESTORATION-ONLY r.md" in _t6 and "NORECHECK n-neither.md" in _t8u\n',
        '              "RESTORATION-ONLY" in _t6 and "NORECHECK" in _t8u\n', ["output-lines"],
        "output-lines marker assertions lose the entry names", probe="marker_name"),
    row("RC27", '"RESTORATION-ONLY r.md" in _t6',
        '"RESTORATION-ONLY r.md" in _t8u', ["output-lines"],
        "RESTORATION-ONLY assertion reads the wrong capture"),
    row("RC28", '              and "ENTRY b-relative.md noprefix=1 foreign_exit=2" in _t1\n',
        '              and "ENTRY b-relative.md" in _t1\n', ["output-lines"],
        "output-lines ENTRY assertion truncated to the name", probe="entry_truncation"),
    row("RC29", '            print("ENTRY %s noprefix=%d foreign_exit=%d" % (name, int(noprefix), code))\n',
        '            print("ENTRY %s noprefix=%d foreign_exit=%d" % (name, int(noprefix), code), file=sys.stderr)\n',
        ["output-lines"], "ENTRY line moved to stderr"),
    row("RC30", '            print("ENTRY %s noprefix=%d foreign_exit=%d" % (name, int(noprefix), code))\n',
        '            print("ENTRY %s foreign_exit=%d noprefix=%d" % (name, code, int(noprefix)))\n',
        ["output-lines"], "ENTRY columns swapped"),
    row("RC31", '        if verbose or noprefix or code == 2:\n',
        '        if verbose or noprefix or code in (1, 2):\n', ["output-lines"],
        "ENTRY also printed for exit-1 entries", probe="entry_bucket_lines"),
    row("RC32", '        if verbose or noprefix or code == 2:\n',
        '        if noprefix or code == 2:\n', ["output-lines"],
        "census condition drops the verbose limb", probe="verbose_census"),

    # ---------- twelve new r81 gate-predicate rows ----------
    row("RC33", '            (gate_consume_ok(1, [True]), False), (gate_consume_ok(True, [True, False]), False),',
        '            (True, True), (gate_consume_ok(True, [True, False]), False),',
        ["gate-predicates"], "identity-edge row (1 is not True) replaced by a tautology",
        probe="compose_table:S08"),
    row("RC34", '            (gate_negpolarity_ok(False, 0), False),',
        '            (True, True),', ["gate-predicates"],
        "negpolarity identity-edge row (0 is not False) replaced by a tautology",
        probe="compose_table:S40"),
    row("RC35", '(both_headers_ok(True, 1, False), False),',
        '(True, True),',
        ["gate-predicates"], "both-headers identity-edge row replaced by a tautology",
        probe="compose_table:S41"),
    row("RC36", '            (gate_checkids_ok(["a"], ["a"], [[False, True]]), False),',
        '            (True, True),', ["gate-predicates"],
        "exact side-log row replaced by a tautology", probe="compose_table:S13"),
    row("RC37", '            (wiring_findings(zero_src),\n'
                '             sorted([f for f in f3_all if f != "F3:gate-consume"] + ["F4:gate-consume:1"])),',
        '            (True, True),', ["gate-predicates"],
        "F4 non-True-constant row replaced by a tautology", probe="compose_table:S15"),
    row("RC38", '            (wiring_findings(upper_src), sorted(["F2:gate-consume:1"] + f3_all)),',
        '            (True, True),', ["gate-predicates"],
        "case-sensitive matching row replaced by a tautology", probe="compose_table:S43"),
    row("RC39", '            if any(isinstance(a, ast.Constant) for a in call.args):',
        '            if any(isinstance(a, ast.Constant) and a.value for a in call.args):',
        ["gate-predicates"], "F4 requires a truthy constant (0 stops counting)"),
    row("RC40", '        if (isinstance(ok, ast.Constant) and ok.value is True) or (',
        '        if (isinstance(ok, ast.Constant) and ok.value == True) or (',
        ["gate-predicates"], "F1 identity test becomes equality (1 is True)", probe="f1_int"),
    row("RC41", '            return _pred_call(node.args[1], name)',
        '            return _pred_call(node.args[0], name)', ["gate-wiring", "gate-checkids"],
        "consumed() predicate looked up at the wrong argument", probe="consumed_asym"),
    row("RC42", '            if line.startswith("recheck:"):',
        '            if line.startswith("recheck"):', ["first-line"],
        "recheck header prefix broadened to the bare word", probe="header_broadened"),
    row("RC43", '        env = dict(os.environ)\n        env["TMPDIR"] = scratch',
        '        env = {"TMPDIR": scratch}', ["prefix-census"],
        "run_foreign child env stripped to TMPDIR", probe="env_inherit"),
    row("RC44", '        if not ok:\n            failures.append(case)',
        '        failures.append(case)', ["result-main"],
        "failure tally appends every case", probe="dirty_evidence", cls="exception"),
    row("RC45", '        finally:\n            sys.stderr = real_err\n'
                '            if saved_tmp is None:\n'
                '                os.environ.pop("TMPDIR", None)\n'
                '            else:\n'
                '                os.environ["TMPDIR"] = saved_tmp',
        '        finally:\n            sys.stderr = real_err', ["tmpdir-refusal"],
        "case-13 TMPDIR restore deleted", probe="dirty_evidence", cls="exception"),
    row("RC46", '        finally:\n            sys.stderr = real_err16\n'
                '            if saved_tmp16 is None:\n'
                '                os.environ.pop("TMPDIR", None)\n'
                '            else:\n'
                '                os.environ["TMPDIR"] = saved_tmp16',
        '        finally:\n            sys.stderr = real_err16', ["tmpdir-file"],
        "case-16 TMPDIR restore deleted", probe="dirty_evidence", cls="exception"),
    row("RC47", '    scratch = tempfile.mkdtemp(prefix="recheck-cwd-selftest-", dir=os.environ.get("TMPDIR") or None)',
        '    scratch = tempfile.mkdtemp(prefix="recheck-cwd-selftest-", dir=None)',
        ["tmpdir-parent"], "selftest scratch stops honouring TMPDIR", probe="selftest_tmpdir"),
    row("RC48", '    env_tmp = os.environ.get("TMPDIR") or None',
        '    env_tmp = None', ["tmpdir-parent"],
        "census recheck scratch stops honouring TMPDIR", probe="census_tmpdir"),
]

# ------------------------------------------------------------------ r80 survivors
R80 = [
    ("R80S03", '    for path in sorted(glob.glob(os.path.join(kdir, "*.md"))):',
     '    for path in glob.glob(os.path.join(kdir, "*.md")):', ["prefix-census"],
     "glob enumeration no longer sorted", "glob_order"),
    ("R80S06", 'DEFAULT_LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"',
     'DEFAULT_LANE = "/home/vgpnk/Projects/shokunin"', ["result-main"],
     "DEFAULT_LANE points at the fleet root", "default_lane"),
    ("R80S18", '        if node.func.id == "consumed" and len(node.args) == 2:',
     '        if node.func.id == "consumed":', ["gate-predicates"],
     "consumed() arity guard removed", "consumed_arity"),
    ("R80S24", '    finally:\n        shutil.rmtree(scratch, ignore_errors=True)\n\n\ndef main(argv):',
     '    finally:\n        pass\n\n\ndef main(argv):', ["scratch-cleanup"],
     "selftest fixture scratch cleanup removed", "selftest_leftover"),
    ("R80S29", '    print("RECHECK-CWD entries=%d noprefix=%d exit2_foreign=%d exit0_foreign=%d "',
     '    print("RECHECK-CWD entries = %d noprefix=%d exit2_foreign=%d exit0_foreign=%d "',
     ["result-main"], "summary line format changed", "summary_format"),
    ("R80S32", '        leftover = sum(1 for r in recorded if os.path.exists(r["path"]))',
     '        leftover = 0', ["scratch-cleanup"],
     "scratch-cleanup leftover fixed at 0", "cleanup_meta"),
    ("R80S33", '        finally:\n            sys.stdout = real\n        return buf.getvalue(), ret',
     '        finally:\n            pass\n        return buf.getvalue(), ret', ["output-lines"],
     "capture() no longer restores stdout", "capture_restore"),
    ("R80S36", '            wfind = ["F0:unreadable:%r" % (excw,)]',
     '            wfind = []', ["gate-wiring"],
     "gate-wiring read-failure fallback neutered", "f0_fallback"),
    ("R80S38", '              bool(recorded) and all(r["dir"] is None or\n'
                '                                     (expected is not None and r["dir"].startswith(expected))\n'
                '                                     for r in recorded),',
     '              bool(recorded) and all(r["dir"] is not None\n'
     '                                     and r["dir"].startswith(expected)\n'
     '                                     for r in recorded),', ["tmpdir-parent"],
     "tmpdir-parent drops the None-parent limb", "unset_tmpdir_run"),
    ("R80H27", '        write_entry(kdir1, "f-fresh-cwd.md",\n'
                '                    \'recheck: test "$(pwd -P)" = "$(cd "$TMPDIR" && pwd -P)"\\n\')',
     '        write_entry(kdir1, "f-fresh-cwd.md", "recheck: true\\n")', ["prefix-census"],
     "fresh-cwd fixture neutralised to true", "fresh_cwd"),
]

# ------------------------------------------------------------------ machinery
def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load(path, tag):
    spec = importlib.util.spec_from_file_location("probe_" + tag, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cap(fn, *args):
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        ret = fn(*args)
    finally:
        sys.stdout = old
    return buf.getvalue(), ret


def run_selftest(path, work, env_extra=None, unset=()):
    os.makedirs(work, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="t-", dir=work)
    env = dict(os.environ)
    for key in unset:
        env.pop(key, None)
    if "TMPDIR" not in unset:
        env["TMPDIR"] = tmp
    if env_extra:
        env.update(env_extra)
    try:
        proc = subprocess.run([sys.executable, "-B", path, "--selftest"], env=env,
                              stdin=subprocess.DEVNULL, capture_output=True, text=True,
                              timeout=900)
        return proc.returncode, proc.stdout + proc.stderr, tmp
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def classify(rc, out, kill_cases):
    verdict, fails = MB.verdict(rc, out, set(kill_cases))
    return {"rc": rc, "verdict": verdict,
            "failed_cases": sorted({c for c, _ in fails}),
            "exception_fails": sorted({c for c, e in fails if e}),
            "has_traceback": "Traceback" in out,
            "cases_line": re.findall(r"^selftest cases=\d+ failures=\d+$", out, re.M),
            "tail": "\n".join(out.strip().splitlines()[-4:])}


def write_variant(src_path, dst_path, anchor, replacement):
    src = open(src_path, encoding="utf-8").read()
    n = src.count(anchor)
    if n != 1:
        raise AssertionError("anchor occurrences=%d in %s: %r" % (n, src_path, anchor[:60]))
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, "w", encoding="utf-8") as fh:
        fh.write(src.replace(anchor, replacement, 1))
    return dst_path


def table_row(rid):
    for r in TABLE:
        if r["id"] == rid:
            return r
    raise KeyError(rid)


def compose(src_path, dst_path, anchor, replacement):
    return write_variant(src_path, dst_path, anchor, replacement)


def selftest_result(path, work, kill_cases):
    rc, out, _ = run_selftest(path, work)
    res = classify(rc, out, kill_cases)
    res["clean_pass"] = MB.clean_pass(rc, out, EXPECT_CASES)
    return res


# ------------------------------------------------------------------ probes
def probe_compose_table(pristine, mutant, root, spec):
    rid = spec.split(":", 1)[1]
    tr = table_row(rid)
    os.makedirs(root, exist_ok=True)
    p = compose(pristine, os.path.join(root, "p-" + rid + ".py"), tr["anchor"], tr["replacement"])
    m = compose(mutant, os.path.join(root, "m-" + rid + ".py"), tr["anchor"], tr["replacement"])
    pr = selftest_result(p, os.path.join(root, "work-p-" + rid), tr["kill_cases"])
    mr = selftest_result(m, os.path.join(root, "work-m-" + rid), tr["kill_cases"])
    masking = pr["verdict"] != "SURVIVED" and mr["verdict"] == "SURVIVED"
    return {"probe": "compose_table:" + rid, "pristine_plus": pr, "mutant_plus": mr,
            "differs": pr["failed_cases"] != mr["failed_cases"],
            "masking": masking,
            "note": "second transform is frozen table row %s" % rid}


def probe_compose_inline(pristine, mutant, root, anchor, replacement, kill_cases, tag):
    os.makedirs(root, exist_ok=True)
    p = compose(pristine, os.path.join(root, "p-" + tag + ".py"), anchor, replacement)
    m = compose(mutant, os.path.join(root, "m-" + tag + ".py"), anchor, replacement)
    pr = selftest_result(p, os.path.join(root, "work-p-" + tag), kill_cases)
    mr = selftest_result(m, os.path.join(root, "work-m-" + tag), kill_cases)
    return {"probe": "compose_inline:" + tag, "pristine_plus": pr, "mutant_plus": mr,
            "differs": pr["failed_cases"] != mr["failed_cases"],
            "masking": pr["verdict"] != "SURVIVED" and mr["verdict"] == "SURVIVED"}


def probe_main_invariant(pristine, mutant, root):
    out = {}
    keys = ["noprefix", "exit2_foreign", "norecheck", "restoration_only"]
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "inv_" + tag)
        bad = []
        env_tmp = os.environ.get("TMPDIR")
        mod.census = lambda *a, **k: counts
        for mask in range(16):
            counts = {"entries": 1, "noprefix": 0, "exit2_foreign": 0, "exit0_foreign": 0,
                      "exit1_foreign": 0, "exit_other": 0, "norecheck": 0,
                      "restoration_only": 0}
            for bit, key in enumerate(keys):
                counts[key] = (mask >> bit) & 1
            o, ret = cap(mod.main, ["x", "--root", root])
            line = "RECHECK-CWD-RESULT nonconformant" in o
            conf = "RECHECK-CWD-RESULT conformant" in o
            if not ((ret == 1) == line == (not conf)):
                bad.append({"counts": counts, "ret": ret, "line": line})
        out[tag] = {"mismatches": bad, "checked": 16}
    return {"probe": "main_invariant", "pristine": out["pristine"], "mutant": out["mutant"],
            "differs": out["pristine"] != out["mutant"]}


def probe_bogus_stdout(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "bog_" + tag)
        saved = os.environ.get("TMPDIR")
        os.environ["TMPDIR"] = os.path.join(root, "missing-dir")
        try:
            o, ret = cap(mod.main, ["x", "--root", root])
        finally:
            if saved is None:
                os.environ.pop("TMPDIR", None)
            else:
                os.environ["TMPDIR"] = saved
        res[tag] = {"ret": ret, "stdout_empty": o == ""}
    return {"probe": "bogus_stdout", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_tmpdir_file_message(pristine, mutant, root):
    tr = {"anchor": '        print("recheck-cwd: TMPDIR %s is not a directory" % tmp, file=sys.stderr)',
          "replacement": '        print("recheck-cwd: TMPDIR /wrong-path is not a directory", file=sys.stderr)'}
    out = probe_compose_inline(pristine, mutant, root, tr["anchor"], tr["replacement"],
                               ["tmpdir-file"], "wrongpath")
    out["note"] = "secondary makes the refusal line name the wrong path; case 13 still pins its own text"
    return out


def probe_tmpdir_ret_tolerance(pristine, mutant, root):
    tr = {"anchor": 'def main(argv):\n    if tmpdir_refused():\n        return 2',
          "replacement": 'def main(argv):\n    if tmpdir_refused():\n        return 0'}
    out = probe_compose_inline(pristine, mutant, root, tr["anchor"], tr["replacement"],
                               ["tmpdir-file"], "ret0")
    out["note"] = "secondary makes the TMPDIR guard return 0; case 13 still pins ret==2"
    return out


def probe_timeout_leak(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "tl_" + tag)
        saved = os.environ.get("TMPDIR")
        os.environ["TMPDIR"] = os.path.join(root, "tmp")
        os.makedirs(os.environ["TMPDIR"], exist_ok=True)
        before = mod.TIMEOUT
        try:
            o, ret = cap(mod.selftest)
        finally:
            after = mod.TIMEOUT
            if saved is None:
                os.environ.pop("TMPDIR", None)
            else:
                os.environ["TMPDIR"] = saved
        res[tag] = {"timeout_before": before, "timeout_after": after, "rc": ret,
                    "cases_line": re.findall(r"^selftest cases=\d+ failures=\d+$", o, re.M)}
    return {"probe": "timeout_leak", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"]["timeout_after"] != res["mutant"]["timeout_after"]}


def probe_unset_states(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "un_" + tag)
        rows = []
        saved = os.environ.get("TMPDIR")
        for state, value in (("unset", None), ("valid_dir", root)):
            if value is None:
                os.environ.pop("TMPDIR", None)
            else:
                os.makedirs(value, exist_ok=True)
                os.environ["TMPDIR"] = value
            # literal case-18 prologue
            if tag == "pristine":
                got = os.environ.pop("TMPDIR", None)
            else:
                got = os.environ.get("TMPDIR")
            refused = mod.tmpdir_refused()
            rows.append({"state": state, "refused": refused,
                         "saved_is_none": got is None,
                         "tmpdir_visible_during_check": "TMPDIR" in os.environ})
            if got is None:
                os.environ.pop("TMPDIR", None)
            else:
                os.environ["TMPDIR"] = got
        if saved is None:
            os.environ.pop("TMPDIR", None)
        else:
            os.environ["TMPDIR"] = saved
        res[tag] = rows
    return {"probe": "unset_states", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": [r["refused"] for r in res["pristine"]] != [r["refused"] for r in res["mutant"]],
            "note": "verdict values are identical; only the saved value/visibility differs"}


def probe_unset_truth(pristine, mutant, root):
    vals = [(False, "no-raise"), (True, "no-raise"), (None, "no-raise"), (None, "raised")]
    table = []
    for refused, raised in vals:
        exc = None if raised == "no-raise" else ZeroDivisionError("x")
        old = (refused is False and exc is None)
        new = (refused in (False, None) and exc is None)
        table.append({"refused": refused, "raised": raised is not None,
                      "pristine": old, "mutant": new,
                      "reachable": not (refused is None and exc is None)})
    return {"probe": "unset_truth", "table": table,
            "differs": any(r["pristine"] != r["mutant"] and r["reachable"] for r in table),
            "note": "the only divergent combination (refused None, no exception) is unreachable"}


def probe_unset_env_run(pristine, mutant, root):
    out = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        rc, txt, _ = run_selftest(path, os.path.join(root, "work-" + tag), unset=("TMPDIR",))
        res = classify(rc, txt, ["tmpdir-unset"])
        res["has_typeerror"] = "TypeError" in txt
        out[tag] = res
    return {"probe": "unset_env_run", "pristine": out["pristine"], "mutant": out["mutant"],
            "differs": out["pristine"]["verdict"] != out["mutant"]["verdict"],
            "note": "selftest run with TMPDIR unset; the frozen counter always sets it"}


def probe_usage_substring(pristine, mutant, root):
    anchor = ('            print("usage: recheck-cwd-census.py [--root DIR] [--lane DIR] [--verbose] | --selftest",\n'
              '                  file=sys.stderr)')
    out = probe_compose_inline(pristine, mutant, root, anchor, '            pass',
                               ["usage-guards"], "nousage")
    out["note"] = "secondary removes the usage line; only case 19 pins it"
    return out


def probe_verbose_main(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "vm_" + tag)
        fx = os.path.join(root, "fx-" + tag)
        kdir = os.path.join(fx, "corpus", "knowledge")
        os.makedirs(kdir, exist_ok=True)
        with open(os.path.join(kdir, "p.md"), "w", encoding="utf-8") as fh:
            fh.write("recheck: cd %s && true\n" % fx)
        o, ret = cap(mod.main, ["x", "--root", fx, "--lane", fx, "--verbose"])
        res[tag] = {"ret": ret, "entry_line": "ENTRY p.md" in o}
    return {"probe": "verbose_main", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_entry_bucket_lines(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "eb_" + tag)
        fx = os.path.join(root, "fx-" + tag)
        kdir = os.path.join(fx, "corpus", "knowledge")
        os.makedirs(kdir, exist_ok=True)
        for name, body in (("a-pass.md", "recheck: cd %s && true\n" % fx),
                           ("d-exit1.md", "recheck: cd %s && exit 1\n" % fx)):
            with open(os.path.join(kdir, name), "w", encoding="utf-8") as fh:
                fh.write(body)
        o, counts = cap(mod.census, fx, fx)
        res[tag] = {"exit1_entry_printed": "ENTRY d-exit1.md" in o,
                    "lines": sorted(line for line in o.splitlines() if line.startswith("ENTRY"))}
    return {"probe": "entry_bucket_lines", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_verbose_census(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "vc_" + tag)
        fx = os.path.join(root, "fx-" + tag)
        kdir = os.path.join(fx, "corpus", "knowledge")
        os.makedirs(kdir, exist_ok=True)
        with open(os.path.join(kdir, "p.md"), "w", encoding="utf-8") as fh:
            fh.write("recheck: cd %s && true\n" % fx)
        o, counts = cap(mod.census, fx, fx, True)
        res[tag] = {"entry_line": "ENTRY p.md" in o}
    return {"probe": "verbose_census", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_force_entry_print(pristine, mutant, root):
    out = probe_compose_inline(pristine, mutant, root,
                               '        if verbose or noprefix or code == 2:',
                               '        if True:', ["output-lines"], "forceentry")
    out["note"] = "secondary prints ENTRY for every entry; only case 20 forbids the passing one"
    return out


def probe_marker_name(pristine, mutant, root):
    out = probe_compose_inline(pristine, mutant, root,
                               '                print("RESTORATION-ONLY %s" % name)',
                               '                print("RESTORATION-ONLY wrong.md")',
                               ["output-lines"], "wrongname")
    out["note"] = "secondary mislabels the restoration-only entry"
    return out


def probe_entry_truncation(pristine, mutant, root):
    anchor = ('            print("ENTRY %s noprefix=%d foreign_exit=%d" % (name, int(noprefix), code))\n')
    repl = ('            if noprefix:\n'
            '                print("ENTRY %s noprefix=%d" % (name, int(noprefix)))\n'
            '            else:\n'
            '                print("ENTRY %s noprefix=%d foreign_exit=%d" % (name, int(noprefix), code))\n')
    out = probe_compose_inline(pristine, mutant, root, anchor, repl, ["output-lines"], "trunc")
    out["note"] = "secondary drops foreign_exit from prefix-less ENTRY lines only"
    return out


def probe_f1_int(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "f1_" + tag)
        res[tag] = {"findings": mod.wiring_findings('check("x", 1, "")\n')}
    return {"probe": "f1_int", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_consumed_asym(pristine, mutant, root):
    src = 'check("gate-consume", consumed(gate_consume_ok(True, y), gate_negpolarity_ok(x, y)), "")\n'
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "ca_" + tag)
        res[tag] = {"findings": mod.wiring_findings(src)}
    return {"probe": "consumed_asym", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_header_broadened(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "hb_" + tag)
        fx = os.path.join(root, "fx-" + tag)
        kdir = os.path.join(fx, "corpus", "knowledge")
        os.makedirs(kdir, exist_ok=True)
        with open(os.path.join(kdir, "x.md"), "w", encoding="utf-8") as fh:
            fh.write("# fixture\nrecheck-ish: true\n")
        o, counts = cap(mod.census, fx, fx)
        res[tag] = {k: counts[k] for k in ("noprefix", "norecheck", "exit_other", "exit0_foreign")}
    return {"probe": "header_broadened", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_env_inherit(pristine, mutant, root):
    res = {}
    os.environ["CENSUS_PROBE_TOKEN"] = "ok"
    try:
        for tag, path in (("pristine", pristine), ("mutant", mutant)):
            mod = load(path, "ei_" + tag)
            fx = os.path.join(root, "fx-" + tag)
            kdir = os.path.join(fx, "corpus", "knowledge")
            os.makedirs(kdir, exist_ok=True)
            with open(os.path.join(kdir, "e.md"), "w", encoding="utf-8") as fh:
                fh.write('recheck: cd %s && test "$CENSUS_PROBE_TOKEN" = ok\n' % fx)
            o, counts = cap(mod.census, fx, fx)
            res[tag] = {"exit0_foreign": counts["exit0_foreign"],
                        "exit1_foreign": counts["exit1_foreign"]}
    finally:
        os.environ.pop("CENSUS_PROBE_TOKEN", None)
    return {"probe": "env_inherit", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_selftest_tmpdir(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "st_" + tag)
        rec = []
        real = tempfile.mkdtemp
        saved = os.environ.get("TMPDIR")
        os.environ["TMPDIR"] = os.path.join(root, "tmp-" + tag)
        os.makedirs(os.environ["TMPDIR"], exist_ok=True)

        def rec_mk(*a, **kw):
            made = real(*a, **kw)
            rec.append(kw.get("dir"))
            return made

        tempfile.mkdtemp = rec_mk
        try:
            o, ret = cap(mod.selftest)
        finally:
            tempfile.mkdtemp = real
            if saved is None:
                os.environ.pop("TMPDIR", None)
            else:
                os.environ["TMPDIR"] = saved
        res[tag] = {"rc": ret, "none_dirs": sum(1 for d in rec if d is None),
                    "calls": len(rec)}
    return {"probe": "selftest_tmpdir", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"]["none_dirs"] != res["mutant"]["none_dirs"]}


def probe_census_tmpdir(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "ct_" + tag)
        fx = os.path.join(root, "fx-" + tag)
        kdir = os.path.join(fx, "corpus", "knowledge")
        os.makedirs(kdir, exist_ok=True)
        with open(os.path.join(kdir, "p.md"), "w", encoding="utf-8") as fh:
            fh.write("recheck: cd %s && true\n" % fx)
        rec = []
        real = tempfile.mkdtemp
        wanted = os.path.join(root, "tmpc-" + tag)
        os.makedirs(wanted, exist_ok=True)
        saved = os.environ.get("TMPDIR")
        os.environ["TMPDIR"] = wanted

        def rec_mk(*a, **kw):
            made = real(*a, **kw)
            rec.append(kw.get("dir"))
            return made

        tempfile.mkdtemp = rec_mk
        try:
            cap(mod.census, fx, fx)
        finally:
            tempfile.mkdtemp = real
            if saved is None:
                os.environ.pop("TMPDIR", None)
            else:
                os.environ["TMPDIR"] = saved
        res[tag] = {"dirs": rec}
    return {"probe": "census_tmpdir", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_dirty_evidence(pristine, mutant, root):
    rc, txt, _ = run_selftest(mutant, os.path.join(root, "work"))
    res = classify(rc, txt, ["result-main"])
    res["typeerror"] = "TypeError" in txt
    res["traceback_head"] = next((ln for ln in txt.splitlines() if ln.startswith("Traceback")
                                  or "Error:" in ln), "")
    return {"probe": "dirty_evidence", "mutant_run": res,
            "note": "crashes/tally breakage: rc!=0 without a 'selftest case=... FAIL' line, so the "
                    "frozen classifier scores DIRTY, not killed"}


# --- r80 survivor probes -------------------------------------------------
def probe_glob_order(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "go_" + tag)
        fx = os.path.join(root, "fx-" + tag)
        kdir = os.path.join(fx, "corpus", "knowledge")
        os.makedirs(kdir, exist_ok=True)
        for name in ("a.md", "b.md", "c.md"):
            with open(os.path.join(kdir, name), "w", encoding="utf-8") as fh:
                fh.write("recheck: true\n")
        real_glob = mod.glob.glob
        calls = {"n": 0}

        def fake_glob(pattern):
            hits = sorted(real_glob(pattern))
            calls["n"] += 1
            return list(reversed(hits))

        mod.glob.glob = fake_glob
        try:
            o, counts = cap(mod.census, fx, fx)
        finally:
            mod.glob.glob = real_glob
        order = [ln.split()[1] for ln in o.splitlines() if ln.startswith("ENTRY")]
        res[tag] = {"order": order}
    return {"probe": "glob_order", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_default_lane(pristine, mutant, root):
    res = {}
    lane = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "dl_" + tag)
        fx = os.path.join(root, "fx-" + tag)
        kdir = os.path.join(fx, "corpus", "knowledge")
        os.makedirs(kdir, exist_ok=True)
        with open(os.path.join(kdir, "p.md"), "w", encoding="utf-8") as fh:
            fh.write("recheck: cd %s && true\n" % lane)
        o, ret = cap(mod.main, ["x", "--root", fx])
        res[tag] = {"ret": ret, "result": "conformant" if "nonconformant" not in o else "nonconformant"}
    return {"probe": "default_lane", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_consumed_arity(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "cary_" + tag)
        try:
            res[tag] = {"findings": mod.wiring_findings('check("gate-consume", consumed(x), "")\n')}
        except Exception as exc:
            res[tag] = {"exception": type(exc).__name__}
    return {"probe": "consumed_arity", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_selftest_leftover(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        own = os.path.join(root, "left-" + tag)
        os.makedirs(own, exist_ok=True)
        env = dict(os.environ)
        env["TMPDIR"] = own
        proc = subprocess.run([sys.executable, "-B", path, "--selftest"], env=env,
                              stdin=subprocess.DEVNULL, capture_output=True, text=True,
                              timeout=900)
        res[tag] = {"rc": proc.returncode, "leftover": sorted(os.listdir(own))}
        for name in os.listdir(own):
            shutil.rmtree(os.path.join(own, name), ignore_errors=True)
    return {"probe": "selftest_leftover", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"]["leftover"] != res["mutant"]["leftover"]}


def probe_summary_format(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        mod = load(path, "sf_" + tag)
        fx = os.path.join(root, "fx-" + tag)
        kdir = os.path.join(fx, "corpus", "knowledge")
        os.makedirs(kdir, exist_ok=True)
        with open(os.path.join(kdir, "p.md"), "w", encoding="utf-8") as fh:
            fh.write("recheck: cd %s && true\n" % fx)
        o, counts = cap(mod.census, fx, fx)
        res[tag] = {"summary": [ln for ln in o.splitlines() if ln.startswith("RECHECK-CWD ")],
                    "result": "conformant" if "nonconformant" not in o else "nonconformant"}
    return {"probe": "summary_format", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_cleanup_meta(pristine, mutant, root):
    anchor = '    finally:\n        shutil.rmtree(scratch, ignore_errors=True)\n\n\ndef census('
    repl = '    finally:\n        pass\n\n\ndef census('
    out = probe_compose_inline(pristine, mutant, root, anchor, repl, ["scratch-cleanup"], "leak")
    out["note"] = "secondary removes run_foreign scratch cleanup; only case 4 measures leftovers"
    return out


def probe_capture_restore(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        rc, txt, _ = run_selftest(path, os.path.join(root, "work-" + tag))
        res[tag] = {"rc": rc, "stdout_has_cases_line": "selftest cases=22" in txt,
                    "chars": len(txt)}
    return {"probe": "capture_restore", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_f0_fallback(pristine, mutant, root):
    os.makedirs(root, exist_ok=True)
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        copy = os.path.join(root, "f0-" + tag + ".py")
        shutil.copyfile(path, copy)
        mod = load(copy, "f0_" + tag)
        mode = os.stat(copy).st_mode
        os.chmod(copy, 0)
        try:
            o, ret = cap(mod.selftest)
        finally:
            os.chmod(copy, mode)
        res[tag] = {"rc": ret,
                    "wiring_fail": "selftest case=gate-wiring FAIL" in o,
                    "f0": "F0:unreadable" in o}
    return {"probe": "f0_fallback", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"] != res["mutant"]}


def probe_unset_tmpdir_run(pristine, mutant, root):
    res = {}
    for tag, path in (("pristine", pristine), ("mutant", mutant)):
        rc, txt, _ = run_selftest(path, os.path.join(root, "work-" + tag), unset=("TMPDIR",))
        res[tag] = classify(rc, txt, ["tmpdir-parent"])
    return {"probe": "unset_tmpdir_run", "pristine": res["pristine"], "mutant": res["mutant"],
            "differs": res["pristine"]["verdict"] != res["mutant"]["verdict"],
            "note": "selftest run with TMPDIR unset; census then records dir=None"}


def probe_fresh_cwd(pristine, mutant, root):
    anchor = '            proc = subprocess.run(["bash", "-c", value], cwd=scratch, env=env,'
    repl = '            proc = subprocess.run(["bash", "-c", value], cwd=None, env=env,'
    out = probe_compose_inline(pristine, mutant, root, anchor, repl, ["prefix-census"], "cwd")
    out["note"] = "secondary runs values from the inherited cwd instead of the fresh scratch"
    return out


PROBES = {
    "compose_table": probe_compose_table,
    "main_invariant": probe_main_invariant,
    "bogus_stdout": probe_bogus_stdout,
    "tmpdir_file_message": probe_tmpdir_file_message,
    "tmpdir_ret_tolerance": probe_tmpdir_ret_tolerance,
    "timeout_leak": probe_timeout_leak,
    "unset_states": probe_unset_states,
    "unset_truth": probe_unset_truth,
    "unset_env_run": probe_unset_env_run,
    "usage_substring": probe_usage_substring,
    "verbose_main": probe_verbose_main,
    "entry_bucket_lines": probe_entry_bucket_lines,
    "verbose_census": probe_verbose_census,
    "force_entry_print": probe_force_entry_print,
    "marker_name": probe_marker_name,
    "entry_truncation": probe_entry_truncation,
    "f1_int": probe_f1_int,
    "consumed_asym": probe_consumed_asym,
    "header_broadened": probe_header_broadened,
    "env_inherit": probe_env_inherit,
    "selftest_tmpdir": probe_selftest_tmpdir,
    "census_tmpdir": probe_census_tmpdir,
    "dirty_evidence": probe_dirty_evidence,
    "glob_order": probe_glob_order,
    "default_lane": probe_default_lane,
    "consumed_arity": probe_consumed_arity,
    "selftest_leftover": probe_selftest_leftover,
    "summary_format": probe_summary_format,
    "cleanup_meta": probe_cleanup_meta,
    "capture_restore": probe_capture_restore,
    "f0_fallback": probe_f0_fallback,
    "unset_tmpdir_run": probe_unset_tmpdir_run,
    "fresh_cwd": probe_fresh_cwd,
}


# ------------------------------------------------------------------ run
def main():
    before = sha(FROZEN)
    assert before == EXPECT_SHA, "frozen candidate sha mismatch: %s" % before
    work = os.path.join(S, "work")
    os.makedirs(work, exist_ok=True)
    base = os.path.join(S, "base", "recheck-cwd-census.py")
    shutil.copyfile(FROZEN, base)
    assert sha(base) == EXPECT_SHA
    assert sha(FROZEN) == EXPECT_SHA

    rc0, out0, _ = run_selftest(base, os.path.join(work, "baseline"))
    baseline_ok = MB.clean_pass(rc0, out0, EXPECT_CASES)
    out = {"seat": "MutC1Hunt", "round": 81, "frozen": FROZEN,
           "frozen_sha256_before": before, "frozen_sha256_after": None,
           "baseline": {"rc": rc0, "clean_pass": baseline_ok,
                        "cases_line": re.findall(r"^selftest cases=\d+ failures=\d+$", out0, re.M)},
           "rows": [], "r80_rerun": [], "summary": {}}

    for spec in ROWS:
        rid = spec["id"]
        assert (spec["anchor"], spec["replacement"]) not in TABLE_PAIRS, "row %s duplicates table" % rid
        mdir = os.path.join(work, rid)
        try:
            mpath = write_variant(base, os.path.join(mdir, "recheck-cwd-census.py"),
                                  spec["anchor"], spec["replacement"])
        except AssertionError as exc:
            out["rows"].append({"id": rid, "desc": spec["desc"], "verdict": "NOT-DERIVED",
                                "error": str(exc)})
            continue
        rc, txt, _ = run_selftest(mpath, os.path.join(mdir, "run"))
        res = classify(rc, txt, spec["kill_cases"])
        res.update({"id": rid, "desc": spec["desc"], "probe_name": spec["probe"],
                    "class": spec["class"], "mutant_sha256": sha(mpath)})
        if res["verdict"] in ("SURVIVED", "DIRTY") and spec["probe"]:
            root = os.path.join(work, "probe-" + rid)
            try:
                spec_probe = PROBES[spec["probe"].split(":", 1)[0]]
                res["probe"] = spec_probe(base, mpath, root, spec["probe"]) if ":" in spec["probe"] \
                    else spec_probe(base, mpath, root)
            except Exception as exc:
                res["probe"] = {"error": "%s: %s" % (type(exc).__name__, exc)}
        out["rows"].append(res)

    for rid, anchor, repl, kc, desc, probe_name in R80:
        assert (anchor, repl) not in TABLE_PAIRS, "r80 row %s duplicates table" % rid
        mdir = os.path.join(work, rid)
        try:
            mpath = write_variant(base, os.path.join(mdir, "recheck-cwd-census.py"), anchor, repl)
        except AssertionError as exc:
            out["r80_rerun"].append({"id": rid, "desc": desc, "verdict": "NOT-DERIVED",
                                     "error": str(exc)})
            continue
        rc, txt, _ = run_selftest(mpath, os.path.join(mdir, "run"))
        res = classify(rc, txt, kc)
        res.update({"id": rid, "desc": desc, "r80_verdict": "SURVIVED", "probe_name": probe_name,
                    "mutant_sha256": sha(mpath)})
        if res["verdict"] in ("SURVIVED", "DIRTY"):
            root = os.path.join(work, "probe-" + rid)
            try:
                res["probe"] = PROBES[probe_name](base, mpath, root)
            except Exception as exc:
                res["probe"] = {"error": "%s: %s" % (type(exc).__name__, exc)}
        out["r80_rerun"].append(res)

    after = sha(FROZEN)
    out["frozen_sha256_after"] = after
    out["frozen_unchanged"] = after == before

    rows = out["rows"]
    def tally(items):
        d = {}
        for r in items:
            d[r["verdict"]] = d.get(r["verdict"], 0) + 1
        return d

    surv = [r["id"] for r in rows if r["verdict"] == "SURVIVED"]
    out["summary"] = {
        "rows": len(rows), "verdicts": tally(rows),
        "survivors": surv,
        "dirty": [r["id"] for r in rows if r["verdict"] == "DIRTY"],
        "probe_masking": [r["id"] for r in rows if r.get("probe", {}).get("masking")],
        "probe_differs": [r["id"] for r in rows if r.get("probe", {}).get("differs")],
        "r80": {"rows": len(out["r80_rerun"]), "verdicts": tally(out["r80_rerun"]),
                "still_survive": [r["id"] for r in out["r80_rerun"] if r["verdict"] == "SURVIVED"]},
        "baseline_ok": baseline_ok,
    }
    os.makedirs(WAVE, exist_ok=True)
    with open(os.path.join(WAVE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("MUTBAT-EXT baseline=%s rows=%d %s" % ("ok" if baseline_ok else "BAD", len(rows),
                                                out["summary"]["verdicts"]))
    print("survivors=%s" % ",".join(surv))
    print("dirty=%s" % ",".join(out["summary"]["dirty"]))
    print("probe_masking=%s" % ",".join(out["summary"]["probe_masking"]))
    print("r80_still_survive=%s" % ",".join(out["summary"]["r80"]["still_survive"]))
    print("frozen_unchanged=%s" % out["frozen_unchanged"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
