#!/usr/bin/env python3
"""MutC1Hunt driver: single-transform mutants of the frozen r80 C1 candidate, outside the
frozen 28-row table. Runs the frozen-counter-shaped detector (rc + FAIL/Traceback parsing)
and, for survivors, an R128 normalized-output diff plus a crafted probe input."""
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

S = "/fast/scratch/hyaku/kasegi-r80/MutC1Hunt"
WAVE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-80/w1/MutC1Hunt"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
FROZEN = LANE + "/.ufo/waves/round-80/c1/recheck-cwd-census.py"
EXPECT_SHA = "420151fdea1187aa308f63536216039746fc9d784f6096c36627b7513e505698"
BASE = S + "/base/recheck-cwd-census.py"

FAIL_RE = re.compile(r"^selftest case=\S+ FAIL", re.M)
EXC_RE = re.compile(r"^selftest case=\S+ FAIL exception=", re.M)

ROWS = [
    # --- expected kills (detector bite) ------------------------------------------------
    dict(id="H01", anchor='        noprefix = not value.startswith(prefix)\n',
         replacement='        noprefix = value.startswith(prefix)\n', kind="kill",
         desc="noprefix operator flip"),
    dict(id="H02", anchor='                counts["restoration_only"] += 1\n',
         replacement='                counts["norecheck"] += 1\n', kind="kill",
         desc="restoration_only counted into norecheck"),
    dict(id="H03", anchor='        if code == 2:\n',
         replacement='        if code == 3:\n', kind="kill",
         desc="exit2 branch constant changed"),
    dict(id="H04", anchor='        elif code == 0:\n',
         replacement='        elif code == 42:\n', kind="kill",
         desc="exit0 branch constant changed"),
    dict(id="H05", anchor='        elif code == 1:\n',
         replacement='        elif code == 9:\n', kind="kill",
         desc="exit1 branch constant changed"),
    dict(id="H06", anchor='        counts["entries"] += 1\n',
         replacement='        counts["entries"] += 0\n', kind="kill",
         desc="entries counter neutered"),
    dict(id="H07", anchor='            counts["noprefix"] += 1\n',
         replacement='            counts["noprefix"] += 0\n', kind="kill",
         desc="noprefix counter neutered"),
    dict(id="H08", anchor='            counts["exit_other"] += 1\n',
         replacement='            counts["exit2_foreign"] += 1\n', kind="kill",
         desc="exit_other bucket folded into exit2"),
    dict(id="H09", anchor='        env["TMPDIR"] = scratch\n',
         replacement='        env["TMPDIR"] = env_tmp\n', kind="kill",
         desc="entry TMPDIR set to parent, not fresh scratch"),
    dict(id="H10", anchor='TIMEOUT = 120', replacement='TIMEOUT = 0.001', kind="kill",
         desc="timeout constant collapsed"),
    dict(id="H11", anchor='    finally:\n        shutil.rmtree(scratch, ignore_errors=True)\n\n\ndef census(',
         replacement='    finally:\n        pass\n\n\ndef census(', kind="kill",
         desc="run_foreign scratch cleanup removed"),
    dict(id="H12", anchor='        print("recheck-cwd: TMPDIR %s is not a directory" % tmp, file=sys.stderr)',
         replacement='        print("recheck-cwd: TMPDIR %s is not a directory" % tmp)', kind="kill",
         desc="refusal line moved off stderr"),
    dict(id="H13", anchor='        print("recheck-cwd: TMPDIR %s is not a directory" % tmp, file=sys.stderr)\n        return True',
         replacement='        print("recheck-cwd: TMPDIR %s is not a directory" % tmp, file=sys.stderr)\n        return False',
         kind="kill", desc="tmpdir_refused returns False after printing"),
    dict(id="H14", anchor='    conform = (counts["noprefix"] == 0 and counts["exit2_foreign"] == 0\n               and counts["norecheck"] == 0 and counts["restoration_only"] == 0)',
         replacement='    conform = (counts["noprefix"] == 0 and counts["exit2_foreign"] == 0\n               and counts["norecheck"] == 0)',
         kind="kill", desc="conform drops restoration_only conjunct"),
    dict(id="H15", anchor='    return 0 if conform else 1\n',
         replacement='    return 0 if conform else 2\n', kind="kill",
         desc="nonconformant exit code changed to 2"),
    dict(id="H16", anchor='    return bool(rows) and len(rows) == expect and all(got == want for got, want in rows)',
         replacement='    return len(rows) == expect and all(got == want for got, want in rows)',
         kind="kill", desc="predicates_ok drops bool(rows)"),
    dict(id="H17", anchor='    return set(done) == set(required) and all(log == [True] for log in side_logs)',
         replacement='    return set(done) == set(required) and all(log != [False] for log in side_logs)',
         kind="kill", desc="checkids side-log test weakened to != [False]"),
    dict(id="H18", anchor='GATE_ROWS = 28', replacement='GATE_ROWS = 29', kind="kill",
         desc="GATE_ROWS constant off by one"),
    dict(id="H19", anchor='    with open(path, encoding="utf-8", errors="replace") as fh:\n        for line in fh:\n            if line.startswith("recheck:"):',
         replacement='    with open(path, encoding="utf-8", errors="replace") as fh:\n        for line in reversed(fh.readlines()):\n            if line.startswith("recheck:"):', kind="kill",
         desc="first_recheck reads last recheck line"),
    dict(id="H20", anchor='                and node.func.id == "check" and len(node.args) >= 2):',
         replacement='                and node.func.id == "check" and len(node.args) >= 4):',
         kind="kill", desc="wiring scanner arity bound raised"),
    dict(id="H21", anchor='                findings.append("F4:%s:%d" % (name, node.lineno))',
         replacement='                pass', kind="kill", desc="F4 finding dropped"),
    dict(id="H22", anchor='    findings.extend("F3:%s" % name for name in GATE_PREDICATES if name not in wired)',
         replacement='    pass', kind="kill", desc="F3 findings dropped"),
    dict(id="H23", anchor='    return neg_ok is False and neg_ret_ok is False',
         replacement='    return not neg_ok and not neg_ret_ok', kind="kill",
         desc="negpolarity predicate rewritten as truthiness (None row)"),
    dict(id="H24", anchor='def main(argv):\n    if tmpdir_refused():\n        return 2\n    if "--selftest" in argv:',
         replacement='def main(argv):\n    if "--selftest" in argv:', kind="kill",
         desc="main TMPDIR guard deleted"),
    dict(id="H25", anchor='if name not in wired)',
         replacement='if True)', kind="kill",
         desc="F3 emitted for wired names too"),
    dict(id="H26", anchor='        write_entry(kdir1, "e-exit7.md", "recheck: exit 7\\n")',
         replacement='        write_entry(kdir1, "e-exit7.md", "recheck: exit 1\\n")', kind="kill",
         desc="fixture literal e-exit7 changed to exit 1"),
    dict(id="H27", anchor='        write_entry(kdir1, "f-fresh-cwd.md",\n                    \'recheck: test "$(pwd -P)" = "$(cd "$TMPDIR" && pwd -P)"\\n\')',
         replacement='        write_entry(kdir1, "f-fresh-cwd.md", "recheck: true\\n")', kind="surv",
         desc="fresh-cwd fixture neutralised to true", probe="freshcwd_meta"),
    dict(id="H28", anchor='            proc = subprocess.run(["bash", "-c", value], cwd=scratch, env=env,',
         replacement='            proc = subprocess.run(["bash", "-c", value], cwd=env_tmp, env=env,',
         kind="kill", desc="run_foreign cwd swapped to the TMPDIR parent"),
    # --- survivors: product surface ---------------------------------------------------
    dict(id="S01", anchor='    prefix = "cd %s && " % lane',
         replacement='    prefix = "cd %s" % lane', kind="surv",
         desc="prefix literal loses the && anchor", probe="prefix_weak"),
    dict(id="S02", anchor='    prefix = "cd %s && " % lane',
         replacement='    prefix = "cd %s &&" % lane', kind="surv",
         desc="prefix literal loses its trailing space", probe="prefix_nospace"),
    dict(id="S03", anchor='    for path in sorted(glob.glob(os.path.join(kdir, "*.md"))):',
         replacement='    for path in glob.glob(os.path.join(kdir, "*.md")):', kind="surv",
         desc="glob enumeration no longer sorted", probe="glob_order"),
    dict(id="S04", anchor='    conform = (counts["noprefix"] == 0 and counts["exit2_foreign"] == 0\n               and counts["norecheck"] == 0 and counts["restoration_only"] == 0)',
         replacement='    conform = (counts["noprefix"] == 0\n               and counts["norecheck"] == 0 and counts["restoration_only"] == 0)',
         kind="surv", desc="conform drops exit2_foreign conjunct", probe="conform_exit2"),
    dict(id="S05", anchor='    conform = (counts["noprefix"] == 0 and counts["exit2_foreign"] == 0\n               and counts["norecheck"] == 0 and counts["restoration_only"] == 0)',
         replacement='    conform = (counts["noprefix"] == 0 and counts["exit2_foreign"] == 0\n               and counts["restoration_only"] == 0)',
         kind="surv", desc="conform drops norecheck conjunct", probe="conform_norecheck"),
    dict(id="S06", anchor='DEFAULT_LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"',
         replacement='DEFAULT_LANE = "/home/vgpnk/Projects/shokunin"', kind="surv",
         desc="DEFAULT_LANE points at fleet root", probe="default_lane"),
    dict(id="S07", anchor='    root, lane, verbose = ".", DEFAULT_LANE, False',
         replacement='    root, lane, verbose = ".", DEFAULT_LANE, True', kind="surv",
         desc="verbose defaults to True", probe="verbose_default"),
    dict(id="S08", anchor='    return clean_ok is True and limb_log == [True]',
         replacement='    return clean_ok == True and limb_log == [True]', kind="surv",
         desc="gate_consume_ok identity test becomes equality", probe="clean_int"),
    dict(id="S09", anchor='    return clean_ok is True and limb_log == [True]',
         replacement='    return clean_ok is True and limb_log[:1] == [True]', kind="surv",
         desc="limb_log test truncated to its first element", probe="limb_extra"),
    dict(id="S10", anchor='    return counts_match is True and first_ran is True and rest_ran is False',
         replacement='    return counts_match is True and first_ran is True and not rest_ran',
         kind="surv", desc="both_headers rest_ran test becomes falsiness", probe="both_zero"),
    dict(id="S11", anchor='    return bool(rows) and len(rows) == expect and all(got == want for got, want in rows)',
         replacement='    return bool(rows) and len(rows) == expect and all(bool(got) == bool(want) for got, want in rows)',
         kind="surv", desc="predicates_ok element equality coerced to truthiness",
         probe="pred_bool"),
    dict(id="S12", anchor='    return bool(rows) and len(rows) == expect and all(got == want for got, want in rows)',
         replacement='    return bool(rows) and len(rows) >= expect and all(got == want for got, want in rows)',
         kind="surv", desc="predicates_ok row count becomes a lower bound", probe="pred_count"),
    dict(id="S13", anchor='    return set(done) == set(required) and all(log == [True] for log in side_logs)',
         replacement='    return set(done) == set(required) and all(True in log for log in side_logs)',
         kind="surv", desc="side log membership test instead of exact log", probe="checkids_member"),
    dict(id="S14", anchor='        if (isinstance(ok, ast.Constant) and ok.value is True) or (\n                isinstance(ok, ast.BoolOp)\n                and any(isinstance(v, ast.Constant) and v.value is True for v in ok.values)):',
         replacement='        if isinstance(ok, ast.Constant) and ok.value is True:',
         kind="surv", desc="F1 BoolOp limb deleted", probe="wiring_boolop"),
    dict(id="S15", anchor='            if any(isinstance(a, ast.Constant) for a in call.args):',
         replacement='            if any(isinstance(a, ast.Constant) and a.value is True for a in call.args):',
         kind="surv", desc="F4 narrowed to constant True arguments", probe="wiring_f4"),
    dict(id="S16", anchor='                and any(isinstance(v, ast.Constant) and v.value is True for v in ok.values)):',
         replacement='                and all(isinstance(v, ast.Constant) and v.value is True for v in ok.values)):',
         kind="surv", desc="F1 BoolOp operand quantifier any->all", probe="wiring_anyall"),
    dict(id="S17", anchor='    "both-headers": "both_headers_ok",\n',
         replacement='', kind="surv",
         desc="both-headers dropped from GATE_PREDICATES", probe="both_map"),
    dict(id="S18", anchor='        if node.func.id == "consumed" and len(node.args) == 2:',
         replacement='        if node.func.id == "consumed":', kind="surv",
         desc="consumed() arity guard removed", probe="predcall_arity"),
    dict(id="S19", anchor='                print("RESTORATION-ONLY %s" % name)\n',
         replacement='', kind="surv", desc="RESTORATION-ONLY marker print deleted",
         probe="print_restoration"),
    dict(id="S20", anchor='                print("NORECHECK %s" % name)\n',
         replacement='', kind="surv", desc="NORECHECK marker print deleted", probe="print_norecheck"),
    dict(id="S21", anchor='        if verbose or noprefix or code == 2:',
         replacement='        if False:', kind="surv", desc="ENTRY detail line suppressed",
         probe="entry_suppressed"),
    dict(id="S22", anchor='        if verbose or noprefix or code == 2:',
         replacement='        if verbose or noprefix:', kind="surv",
         desc="ENTRY predicate drops code == 2", probe="entry_exit2"),
    dict(id="S23", anchor='            if line.startswith("recheck:"):',
         replacement='            if line.lstrip().startswith("recheck:"):', kind="surv",
         desc="first_recheck accepts indented header", probe="indented"),
    dict(id="S24", anchor='    finally:\n        shutil.rmtree(scratch, ignore_errors=True)\n\n\ndef main(argv):',
         replacement='    finally:\n        pass\n\n\ndef main(argv):', kind="surv",
         desc="selftest fixture scratch cleanup removed", probe="selftest_leftover"),
    dict(id="S25", anchor='    if tmp is not None and not os.path.isdir(tmp):',
         replacement='    if not os.path.isdir(tmp):', kind="surv",
         desc="tmpdir_refused drops the None guard", probe="tmpdir_unset"),
    dict(id="S26", anchor='                return line[len("recheck:"):].strip()',
         replacement='                return line[len("recheck:"):]', kind="surv",
         desc="first_recheck value no longer stripped", probe="strip_removed"),
    dict(id="S27", anchor='def wiring_ok(findings):\n    return findings == []',
         replacement='def wiring_ok(findings):\n    return not findings', kind="surv",
         desc="wiring_ok rewritten as truthiness", probe="wiring_ok_equiv"),
    dict(id="S28", anchor='counts["noprefix"] == 0',
         replacement='counts["noprefix"] <= 0', kind="surv",
         desc="conform noprefix test becomes <= 0", probe="conform_equiv"),
    dict(id="S29", anchor='    print("RECHECK-CWD entries=%d noprefix=%d exit2_foreign=%d exit0_foreign=%d "',
         replacement='    print("RECHECK-CWD entries = %d noprefix=%d exit2_foreign=%d exit0_foreign=%d "',
         kind="surv", desc="summary line format changed", probe="summary_format"),
    dict(id="S30", anchor='                  file=sys.stderr)\n            return 2',
         replacement='                  file=sys.stderr)\n            return 0', kind="surv",
         desc="usage error exit code returns 0", probe="usage_ret"),
    dict(id="S31", anchor='        raise SystemExit("recheck-cwd: no corpus/knowledge under %s" % root)',
         replacement='        print("recheck-cwd: no corpus/knowledge under %s" % root)', kind="surv",
         desc="missing corpus guard prints instead of exiting", probe="missing_corpus"),
    dict(id="S32", anchor='        leftover = sum(1 for r in recorded if os.path.exists(r["path"]))',
         replacement='        leftover = 0', kind="surv",
         desc="scratch-cleanup leftover fixed at 0", probe="leftover_meta"),
    dict(id="S33", anchor='        finally:\n            sys.stdout = real\n        return buf.getvalue(), ret',
         replacement='        finally:\n            pass\n        return buf.getvalue(), ret', kind="surv",
         desc="capture() no longer restores stdout", probe="capture_restore"),
    dict(id="S34", anchor='    if tmpdir_refused():\n        return 2\n    failures = []',
         replacement='    failures = []', kind="surv",
         desc="selftest TMPDIR guard deleted", probe="selftest_guard"),
    dict(id="S35", anchor='            proc = subprocess.run(["bash", "-c", value], cwd=scratch, env=env,',
         replacement='            proc = subprocess.run(["sh", "-c", value], cwd=scratch, env=env,',
         kind="surv", desc="recheck values run under sh, not bash", probe="sh_shell"),
    dict(id="S36", anchor='            wfind = ["F0:unreadable:%r" % (excw,)]',
         replacement='            wfind = []', kind="surv",
         desc="gate-wiring read-failure fallback neutered", probe="f0_fallback"),
    dict(id="S37", anchor='            if line.startswith("restoration-recheck:"):\n                return True',
         replacement='            if line.startswith("restoration"):\n                return True', kind="surv",
         desc="restoration header prefix broadened", probe="restoration_broad"),
    dict(id="S39", anchor='    counts = census(os.path.abspath(root), lane, verbose)',
         replacement='    counts = census(os.path.abspath(root), os.path.abspath(root), verbose)',
         kind="surv", desc="main passes root where lane belongs", probe="lane_swap"),
    dict(id="S40", anchor='    return neg_ok is False and neg_ret_ok is False',
         replacement='    return neg_ok is False and neg_ret_ok == False', kind="surv",
         desc="neg_ret_ok identity test becomes equality", probe="neg_ret_int"),
    dict(id="S41", anchor='    return counts_match is True and first_ran is True and rest_ran is False',
         replacement='    return counts_match is True and first_ran == True and rest_ran is False',
         kind="surv", desc="both_headers first_ran identity test becomes equality",
         probe="first_int"),
    dict(id="S42", anchor='        if not (isinstance(label, ast.Constant) and isinstance(label.value, str)):\n            continue',
         replacement='        if not (isinstance(label, ast.Constant) and isinstance(label.value, str)):\n            pass',
         kind="surv", desc="non-string check label no longer skipped", probe="label_int"),
    dict(id="S43", anchor='        if node.func.id == name:\n            return node',
         replacement='        if node.func.id.lower() == name.lower():\n            return node',
         kind="surv", desc="predicate matching becomes case-insensitive", probe="case_insensitive"),
    dict(id="S38", anchor='              bool(recorded) and all(r["dir"] is None or\n                                     (expected is not None and r["dir"].startswith(expected))\n                                     for r in recorded),',
         replacement='              bool(recorded) and all(r["dir"] is not None\n                                     and r["dir"].startswith(expected)\n                                     for r in recorded),',
         kind="surv", desc="tmpdir-parent drops the None-parent limb", probe="tmpdir_none"),
]

# ---------------------------------------------------------------- machinery
def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def norm(txt):
    for p in (S, LANE, "/fast/scratch/hyaku/kasegi-r80"):
        txt = txt.replace(p, "<S>")
    txt = re.sub(r"run-tmp-[A-Za-z0-9_]+", "<RUNTMP>", txt)
    txt = re.sub(r"recheck-cwd-selftest-[A-Za-z0-9_]+", "<SELFTEST>", txt)
    txt = re.sub(r"recheck-cwd-[A-Za-z0-9_]+", "<SCRATCH>", txt)
    return re.sub(r"/tmp/[^\s\"'()]*", "<TMP>", txt)


def run_selftest(path, work, tmp_override=None):
    tmp = tmp_override or tempfile.mkdtemp(prefix="run-tmp-", dir=work)
    cwd = tempfile.mkdtemp(prefix="run-cwd-", dir=work)
    env = dict(os.environ)
    env["TMPDIR"] = tmp
    try:
        proc = subprocess.run([sys.executable, "-B", path, "--selftest"], env=env, cwd=cwd,
                              stdin=subprocess.DEVNULL, capture_output=True, text=True,
                              timeout=300)
        return proc.returncode, proc.stdout + proc.stderr
    finally:
        if tmp_override is None:
            shutil.rmtree(tmp, ignore_errors=True)
        shutil.rmtree(cwd, ignore_errors=True)


def verdict(rc, out):
    fails = len(FAIL_RE.findall(out))
    if rc == 0:
        return "SURVIVED", fails
    if "Traceback" in out or fails == 0:
        return "DIRTY", fails
    if EXC_RE.search(out):
        return "EXCEPTION-KILL", fails
    return "KILLED", fails


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def newroot(ctx):
    root = tempfile.mkdtemp(prefix="fx-", dir=ctx["tmp"])
    kdir = os.path.join(root, "corpus", "knowledge")
    os.makedirs(kdir)
    return root, kdir


def put(kdir, name, body):
    with open(os.path.join(kdir, name), "w", encoding="utf-8") as fh:
        fh.write("# fixture\n" + body)


def cap(fn, *args):
    out, err = io.StringIO(), io.StringIO()
    ro, re_ = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = out, err
    try:
        try:
            ret = fn(*args)
        except BaseException as exc:  # SystemExit and friends are observations here
            ret = "EXC:%s:%s" % (type(exc).__name__, exc)
    finally:
        sys.stdout, sys.stderr = ro, re_
    return out.getvalue(), err.getvalue(), ret


# ---------------------------------------------------------------- probes
def pr_prefix_weak(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "a.md", "recheck: cd %sNONSENSE && true\n" % root)
    put(kdir, "b.md", "recheck: cd %s && true\n" % root)
    _o, _e, c = cap(m.main, ["x", "--root", root, "--lane", root])
    return {"ret": c}


def pr_prefix_nospace(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "a.md", "recheck: cd %s &&false\n" % root)
    put(kdir, "b.md", "recheck: cd %s && true\n" % root)
    out, _e, c = cap(m.main, ["x", "--root", root, "--lane", root])
    counts = cap(m.census, root, root)[2]
    return {"noprefix": counts.get("noprefix"), "ret": c}


def pr_glob_order(m, ctx):
    root, kdir = newroot(ctx)
    for name in ("c.md", "a.md", "b.md"):
        put(kdir, name, "recheck: cd %s && true\n" % root)
    out = cap(m.census, root, root, True)[0]
    order = [ln.split()[1] for ln in out.splitlines() if ln.startswith("ENTRY ")]
    return {"order": order}


def pr_conform_exit2(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "a.md", "recheck: cd %s && python3 corpus/instruments/missing.py\n" % root)
    out, _e, ret = cap(m.main, ["x", "--root", root, "--lane", root])
    return {"ret": ret, "conformant": "RECHECK-CWD-RESULT conformant" in out}


def pr_conform_norecheck(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "a.md", "body only, no recheck header\n")
    out, _e, ret = cap(m.main, ["x", "--root", root, "--lane", root])
    return {"ret": ret, "conformant": "RECHECK-CWD-RESULT conformant" in out}


def pr_default_lane(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "a.md", "recheck: cd %s && true\n" % LANE)
    out, _e, ret = cap(m.main, ["x", "--root", root])
    return {"ret": ret, "conformant": "RECHECK-CWD-RESULT conformant" in out}


def pr_verbose_default(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "a.md", "recheck: cd %s && true\n" % root)
    out, _e, ret = cap(m.main, ["x", "--root", root, "--lane", root])
    return {"ret": ret, "entry_lines": sum(1 for ln in out.splitlines() if ln.startswith("ENTRY "))}


def pr_clean_int(m, ctx):
    return {"gate_consume_ok(1,[True])": m.gate_consume_ok(1, [True])}


def pr_limb_extra(m, ctx):
    return {"gate_consume_ok(True,[True,False])": m.gate_consume_ok(True, [True, False])}


def pr_both_zero(m, ctx):
    return {"both_headers_ok(True,True,0)": m.both_headers_ok(True, True, 0)}


def pr_pred_bool(m, ctx):
    return {"predicates_ok([('a','b')],1)": m.predicates_ok([("a", "b")], 1)}


def pr_pred_count(m, ctx):
    return {"predicates_ok([(T,T),(T,T)],1)": m.predicates_ok([(True, True), (True, True)], 1)}


def pr_checkids_member(m, ctx):
    return {"gate_checkids_ok(['a'],['a'],[[False,True]])":
            m.gate_checkids_ok(["a"], ["a"], [[False, True]])}


def pr_wiring_boolop(m, ctx):
    src = 'check("gate-consume", True and gate_consume_ok(x), "")\n'
    return {"findings": m.wiring_findings(src)}


def pr_wiring_f4(m, ctx):
    src = 'check("gate-consume", gate_consume_ok(0, log), "")\n'
    return {"findings": m.wiring_findings(src)}


def pr_wiring_anyall(m, ctx):
    src = 'check("x", False or True, "")\n'
    return {"findings": m.wiring_findings(src)}


def pr_both_map(m, ctx):
    src = 'check("both-headers", True, "")\n'
    return {"findings": m.wiring_findings(src)}


def pr_predcall_arity(m, ctx):
    src = 'check("gate-consume", consumed(x), "")\n'
    try:
        return {"findings": m.wiring_findings(src)}
    except BaseException as exc:
        return {"exc": type(exc).__name__}


def pr_print_restoration(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "r.md", "restoration-recheck: true\n")
    put(kdir, "p.md", "recheck: cd %s && true\n" % root)
    out, _e, c = cap(m.census, root, root)
    return {"restoration_only": c.get("restoration_only"),
            "marker": "RESTORATION-ONLY r.md" in out}


def pr_print_norecheck(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "n.md", "body only\n")
    put(kdir, "p.md", "recheck: cd %s && true\n" % root)
    out, _e, c = cap(m.census, root, root)
    return {"norecheck": c.get("norecheck"), "marker": "NORECHECK n.md" in out}


def pr_entry_suppressed(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "b.md", "recheck: python3 corpus/instruments/missing.py\n")
    put(kdir, "p.md", "recheck: cd %s && true\n" % root)
    out, _e, _c = cap(m.census, root, root)
    return {"entry_lines": sum(1 for ln in out.splitlines() if ln.startswith("ENTRY "))}


def pr_entry_exit2(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "b.md", "recheck: cd %s && python3 corpus/instruments/missing.py\n" % root)
    out, _e, c = cap(m.census, root, root)
    return {"exit2": c.get("exit2_foreign"),
            "entry_lines": sum(1 for ln in out.splitlines() if ln.startswith("ENTRY "))}


def pr_indented(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "i.md", "   recheck: true\n")
    put(kdir, "p.md", "recheck: cd %s && true\n" % root)
    _o, _e, c = cap(m.census, root, root)
    return {"norecheck": c.get("norecheck"), "exit0": c.get("exit0_foreign"),
            "exit_other": c.get("exit_other"), "noprefix": c.get("noprefix")}


def pr_selftest_leftover(m, ctx):
    tmp = tempfile.mkdtemp(prefix="leftover-", dir=ctx["tmp"])
    rc, out = run_selftest(ctx["path"], ctx["tmp"], tmp_override=tmp)
    left = [n for n in os.listdir(tmp) if n.startswith("recheck-cwd-selftest-")]
    shutil.rmtree(tmp, ignore_errors=True)
    return {"rc": rc, "cases": "selftest cases=15 failures=0" in out, "leftover_selftest_dirs": len(left)}


def pr_tmpdir_unset(m, ctx):
    cwd = tempfile.mkdtemp(prefix="unset-", dir=ctx["tmp"])
    env = dict(os.environ)
    env.pop("TMPDIR", None)
    try:
        proc = subprocess.run([sys.executable, "-B", ctx["path"], "--selftest"], env=env,
                              cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                              timeout=300)
        return {"rc": proc.returncode, "traceback": "Traceback" in proc.stderr + proc.stdout,
                "cases": "selftest cases=15 failures=0" in proc.stdout}
    finally:
        shutil.rmtree(cwd, ignore_errors=True)


def pr_strip_removed(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "a.md", "recheck: true   \n")
    put(kdir, "b.md", "recheck:\ttrue\n")
    put(kdir, "c.md", "recheck: cd %s && true   \n" % root)
    _o, _e, c = cap(m.census, root, root)
    return {k: c[k] for k in ("entries", "noprefix", "exit0_foreign", "exit_other", "norecheck")}


def pr_wiring_ok_equiv(m, ctx):
    return {"empty": m.wiring_ok([]), "one": m.wiring_ok(["F1:x:1"]),
            "many": m.wiring_ok(["F1:x:1", "F2:y:1"])}


def pr_conform_equiv(m, ctx):
    out = []
    for entries in (["recheck: cd ROOT && true\n"], ["recheck: true\n"], ["body only\n"]):
        root, kdir = newroot(ctx)
        for i, body in enumerate(entries):
            put(kdir, "e%d.md" % i, body.replace("ROOT", root))
        o, _e, ret = cap(m.main, ["x", "--root", root, "--lane", root])
        out.append({"ret": ret, "conformant": "RECHECK-CWD-RESULT conformant" in o})
    return {"cases": out}


def pr_summary_format(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "a.md", "recheck: cd %s && true\n" % root)
    out = cap(m.census, root, root)[0]
    return {"summary": [ln for ln in out.splitlines() if ln.startswith("RECHECK-CWD ")]}


def pr_usage_ret(m, ctx):
    out, err, ret = cap(m.main, ["x", "--bogus"])
    return {"ret": ret, "usage_on_stderr": "usage:" in err, "stdout": out}


def pr_missing_corpus(m, ctx):
    root = tempfile.mkdtemp(prefix="empty-", dir=ctx["tmp"])
    out, err, ret = cap(m.main, ["x", "--root", root])
    lines = [ln for ln in out.splitlines() if ln.startswith("RECHECK-CWD")]
    return {"ret": str(ret), "stdout_lines": lines,
            "stderr_has_guard": "no corpus/knowledge" in err}


def pr_leftover_meta(m, ctx):
    def build(srcpath, dst):
        src = open(srcpath, encoding="utf-8").read()
        anchor = '    finally:\n        shutil.rmtree(scratch, ignore_errors=True)\n\n\ndef census('
        assert src.count(anchor) == 1
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(src.replace(anchor, '    finally:\n        pass\n\n\ndef census(', 1))
    d = tempfile.mkdtemp(prefix="meta-", dir=ctx["tmp"])
    try:
        mp = os.path.join(d, "mutant-noclean.py")
        pp = os.path.join(d, "pristine-noclean.py")
        build(ctx["path"], mp)
        build(ctx["pristine_path"], pp)
        rc_m, out_m = run_selftest(mp, ctx["tmp"])
        rc_p, out_p = run_selftest(pp, ctx["tmp"])
        return {"mutant_plus_cleanup_removed_rc": rc_m,
                "mutant_plus_cleanup_removed_scratch_ok":
                    "selftest case=scratch-cleanup ok" in out_m,
                "pristine_plus_cleanup_removed_rc": rc_p,
                "pristine_plus_cleanup_removed_scratch_ok":
                    "selftest case=scratch-cleanup ok" in out_p}
    finally:
        shutil.rmtree(d, ignore_errors=True)


def pr_capture_restore(m, ctx):
    rc, out = run_selftest(ctx["path"], ctx["tmp"])
    return {"rc": rc, "cases_line": "selftest cases=15 failures=0" in out,
            "stdout_chars": len(out)}


def pr_selftest_guard(m, ctx):
    bad = os.path.join(ctx["tmp"], "no-such-tmpdir")
    saved = os.environ.get("TMPDIR")
    os.environ["TMPDIR"] = bad
    try:
        out, err, ret = cap(lambda: m.selftest())
        return {"ret": str(ret), "guard_line": "recheck-cwd: TMPDIR" in err,
                "exc": "FileNotFoundError" in str(ret)}
    finally:
        if saved is None:
            os.environ.pop("TMPDIR", None)
        else:
            os.environ["TMPDIR"] = saved


def pr_sh_shell(m, ctx):
    root, kdir = newroot(ctx)
    shlink = os.path.realpath("/bin/sh")
    put(kdir, "a.md", "recheck: [[ 1 = 1 ]]\n")
    put(kdir, "b.md", "recheck: cd %s && true\n" % root)
    _o, _e, c = cap(m.census, root, root)
    return {"exit0": c.get("exit0_foreign"), "exit_other": c.get("exit_other"),
            "bin_sh": shlink}


def pr_f0_fallback(m, ctx):
    src = open(ctx["path"], encoding="utf-8").read()
    ns = {"__name__": "cand", "__file__": os.path.join(ctx["tmp"], "missing-file.py")}
    out, _e, rc = cap(lambda: exec(compile(src, "<mutant>", "exec"), ns) or ns["selftest"]())
    return {"selftest_rc": rc, "wiring_failed": "selftest case=gate-wiring FAIL" in out}


def pr_restoration_broad(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "x.md", "restoration-note: anything\n")
    put(kdir, "p.md", "recheck: cd %s && true\n" % root)
    out, _e, c = cap(m.census, root, root)
    return {"norecheck": c.get("norecheck"), "restoration_only": c.get("restoration_only"),
            "restoration_marker": "RESTORATION-ONLY x.md" in out}


def pr_lane_swap(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "a.md", "recheck: cd %s && true\n" % LANE)
    out, _e, ret = cap(m.main, ["x", "--root", root, "--lane", LANE])
    return {"ret": ret, "conformant": "RECHECK-CWD-RESULT conformant" in out}


def pr_neg_ret_int(m, ctx):
    return {"gate_negpolarity_ok(False,0)": m.gate_negpolarity_ok(False, 0)}


def pr_first_int(m, ctx):
    return {"both_headers_ok(True,1,False)": m.both_headers_ok(True, 1, False)}


def pr_label_int(m, ctx):
    src = 'check(42, True, "")\n'
    return {"findings": m.wiring_findings(src)}


def pr_case_insensitive(m, ctx):
    src = 'check("gate-consume", GATE_CONSUME_OK(x), "")\n'
    return {"findings": m.wiring_findings(src)}


def pr_freshcwd_meta(m, ctx):
    def build(srcpath, dst):
        src = open(srcpath, encoding="utf-8").read()
        anchor = '            proc = subprocess.run(["bash", "-c", value], cwd=scratch, env=env,'
        assert src.count(anchor) == 1
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(src.replace(
                anchor,
                '            proc = subprocess.run(["bash", "-c", value], env=env,', 1))
    d = tempfile.mkdtemp(prefix="freshmeta-", dir=ctx["tmp"])
    try:
        mp = os.path.join(d, "mutant-cwd-inherit.py")
        pp = os.path.join(d, "pristine-cwd-inherit.py")
        build(ctx["path"], mp)
        build(ctx["pristine_path"], pp)
        rc_m, out_m = run_selftest(mp, ctx["tmp"])
        rc_p, out_p = run_selftest(pp, ctx["tmp"])
        return {"pristine_plus_cwd_inherit_rc": rc_p,
                "pristine_prefix_census_fail": "selftest case=prefix-census FAIL" in out_p,
                "mutant_plus_cwd_inherit_rc": rc_m,
                "mutant_prefix_census_fail": "selftest case=prefix-census FAIL" in out_m}
    finally:
        shutil.rmtree(d, ignore_errors=True)


def pr_tmpdir_none(m, ctx):
    root, kdir = newroot(ctx)
    put(kdir, "a.md", "recheck: cd %s && true\n" % root)
    cwd = tempfile.mkdtemp(prefix="none-", dir=ctx["tmp"])
    env = dict(os.environ)
    env.pop("TMPDIR", None)
    try:
        proc = subprocess.run([sys.executable, "-B", ctx["path"], "--selftest"], env=env,
                              cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                              timeout=300)
        return {"rc": proc.returncode, "cases": "selftest cases=15 failures=0" in proc.stdout}
    finally:
        shutil.rmtree(cwd, ignore_errors=True)


PROBES = {
    "prefix_weak": pr_prefix_weak, "prefix_nospace": pr_prefix_nospace,
    "glob_order": pr_glob_order, "conform_exit2": pr_conform_exit2,
    "conform_norecheck": pr_conform_norecheck, "default_lane": pr_default_lane,
    "verbose_default": pr_verbose_default, "clean_int": pr_clean_int,
    "limb_extra": pr_limb_extra, "both_zero": pr_both_zero, "pred_bool": pr_pred_bool,
    "pred_count": pr_pred_count, "checkids_member": pr_checkids_member,
    "wiring_boolop": pr_wiring_boolop, "wiring_f4": pr_wiring_f4,
    "wiring_anyall": pr_wiring_anyall, "both_map": pr_both_map,
    "predcall_arity": pr_predcall_arity, "print_restoration": pr_print_restoration,
    "print_norecheck": pr_print_norecheck, "entry_suppressed": pr_entry_suppressed,
    "entry_exit2": pr_entry_exit2, "indented": pr_indented,
    "selftest_leftover": pr_selftest_leftover, "tmpdir_unset": pr_tmpdir_unset,
    "strip_removed": pr_strip_removed, "wiring_ok_equiv": pr_wiring_ok_equiv,
    "conform_equiv": pr_conform_equiv, "summary_format": pr_summary_format,
    "usage_ret": pr_usage_ret, "missing_corpus": pr_missing_corpus,
    "leftover_meta": pr_leftover_meta, "capture_restore": pr_capture_restore,
    "selftest_guard": pr_selftest_guard, "sh_shell": pr_sh_shell,
    "f0_fallback": pr_f0_fallback, "restoration_broad": pr_restoration_broad,
    "tmpdir_none": pr_tmpdir_none, "lane_swap": pr_lane_swap,
    "freshcwd_meta": pr_freshcwd_meta,
    "neg_ret_int": pr_neg_ret_int, "first_int": pr_first_int,
    "label_int": pr_label_int, "case_insensitive": pr_case_insensitive,
}


def run_probe(kind, path, pristine_path, tmp):
    ctx = {"tmp": tmp, "path": path, "pristine_path": pristine_path}
    mod = load(path, "mut_" + kind + "_" + hashlib.md5(path.encode()).hexdigest()[:8])
    saved_tmp = os.environ.get("TMPDIR")
    os.environ["TMPDIR"] = tmp
    try:
        return PROBES[kind](mod, ctx)
    finally:
        if saved_tmp is None:
            os.environ.pop("TMPDIR", None)
        else:
            os.environ["TMPDIR"] = saved_tmp


def main():
    os.makedirs(WAVE, exist_ok=True)
    os.makedirs(os.path.join(WAVE, "logs"), exist_ok=True)
    os.makedirs(os.path.join(WAVE, "survivors"), exist_ok=True)
    got = sha(FROZEN)
    if got != EXPECT_SHA:
        print("FROZEN SHA MISMATCH: %s" % got, file=sys.stderr)
        return 2
    with open(FROZEN, encoding="utf-8") as fh:
        src = fh.read()
    os.makedirs(os.path.dirname(BASE), exist_ok=True)
    with open(BASE, "w", encoding="utf-8") as fh:
        fh.write(src)
    WORK = S + "/t"
    os.makedirs(WORK, exist_ok=True)
    base_rc, base_out = run_selftest(BASE, WORK)
    with open(os.path.join(WAVE, "baseline.out"), "w", encoding="utf-8") as fh:
        fh.write("rc=%d\n%s" % (base_rc, base_out))
    baseline = base_rc == 0 and "selftest cases=15 failures=0" in base_out
    print("BASELINE rc=%d ok=%s sha=%s" % (base_rc, baseline, got))
    if not baseline:
        return 1

    results = []
    probes = {}
    for row in ROWS:
        rid = row["id"]
        n = src.count(row["anchor"])
        if n != 1:
            results.append({**{k: row.get(k) for k in ("id", "desc", "kind")},
                            "verdict": "NOT-DERIVED", "occurrences": n})
            print("ROW %s NOT-DERIVED occurrences=%d" % (rid, n))
            continue
        mutant = src.replace(row["anchor"], row["replacement"], 1)
        mdir = os.path.join(S, "mut", rid)
        os.makedirs(mdir, exist_ok=True)
        mpath = os.path.join(mdir, "recheck-cwd-census.py")
        with open(mpath, "w", encoding="utf-8") as fh:
            fh.write(mutant)
        rc, out = run_selftest(mpath, WORK)
        v, fails = verdict(rc, out)
        rec = {"id": rid, "desc": row["desc"], "kind": row["kind"], "verdict": v, "rc": rc,
               "fails": fails, "mutant_sha256": hashlib.sha256(mutant.encode()).hexdigest(),
               "anchor_occurrences": n}
        with open(os.path.join(WAVE, "logs", "%s.out" % rid), "w", encoding="utf-8") as fh:
            fh.write("rc=%d verdict=%s\n%s" % (rc, v, out))
        if v == "SURVIVED":
            rec["r128_output_identical"] = norm(out) == norm(base_out)
            rec["harness_normalized_diff_lines"] = sum(
                1 for a, b in zip(norm(out).splitlines(), norm(base_out).splitlines()) if a != b
            ) + abs(len(norm(out).splitlines()) - len(norm(base_out).splitlines()))
            if os.path.getsize(mpath) <= 40000:
                with open(os.path.join(WAVE, "survivors", "%s.py" % rid), "w", encoding="utf-8") as fh:
                    fh.write(mutant)
            pkind = row.get("probe")
            if pkind is None:
                rec["probe"] = None
                print("ROW %s SURVIVED with no probe" % rid)
                results.append(rec)
                shutil.rmtree(mdir, ignore_errors=True)
                continue
            pdir = os.path.join(WORK, "probe", rid)
            os.makedirs(pdir, exist_ok=True)
            p_m = run_probe(pkind, mpath, BASE, pdir)
            p_p = run_probe(pkind, BASE, BASE, pdir)
            probes[rid] = {"probe": pkind, "pristine": p_p, "mutant": p_m,
                           "differs": json.dumps(p_p, sort_keys=True) != json.dumps(p_m, sort_keys=True)}
            rec["probe"] = pkind
            rec["probe_differs"] = probes[rid]["differs"]
            print("ROW %s\n  pristine=%s\n  mutant  =%s" % (rid, json.dumps(p_p), json.dumps(p_m)))
            shutil.rmtree(pdir, ignore_errors=True)
        results.append(rec)
        print("ROW %s %s rc=%d fails=%d %s" % (rid, v, rc, fails, row["desc"]))
        shutil.rmtree(mdir, ignore_errors=True)

    summary = {"baseline_sha256": got, "baseline_ok": baseline,
               "rows": len(ROWS), "results": results}
    with open(os.path.join(WAVE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    with open(os.path.join(WAVE, "probes.json"), "w", encoding="utf-8") as fh:
        json.dump(probes, fh, indent=1, sort_keys=True)
    tally = {}
    for r in results:
        tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
    print("TALLY %s" % json.dumps(tally, sort_keys=True))
    print("FROZEN_AFTER %s" % sha(FROZEN))
    return 0 if sha(FROZEN) == got else 3


if __name__ == "__main__":
    sys.exit(main())
