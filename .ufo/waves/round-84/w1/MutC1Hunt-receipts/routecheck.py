#!/usr/bin/env python3
"""routecheck.py -- prove each routed "cheapest killing assertion" fires on its gap mutant.

For every gap whose fix is an assertion (not a state-restore identity), build the fixture the
fix inserts, evaluate the proposed conjunct on pristine and on the mutant bytes, and print
PASS when the conjunct holds on pristine and fails on the mutant. Writes nothing outside the
--outdir scratch. Frozen bytes are only read.
"""
import argparse
import importlib.util as u
import json
import os
import subprocess
import sys

PY = sys.executable
RESULTS = []


def load(name, path):
    spec = u.spec_from_file_location(name, path)
    mod = u.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_entry(kdir, name, body):
    with open(os.path.join(kdir, name), "w", encoding="utf-8") as fh:
        fh.write("# fixture\n" + body)


def fixture(root, entries):
    kdir = os.path.join(root, "corpus", "knowledge")
    os.makedirs(kdir, exist_ok=True)
    for name, body in entries.items():
        write_entry(kdir, name, body)
    return root


def cli(target, root, env, cwd=None, argv=None):
    args = argv if argv is not None else [PY, "-B", target, "--root", root, "--lane", root]
    proc = subprocess.run(args, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                          capture_output=True, text=True, timeout=300)
    return proc.returncode, proc.stdout, proc.stderr


def summary(out):
    return [ln for ln in out.splitlines() if ln.startswith("RECHECK-CWD entries=")]


def record(name, ok, detail):
    RESULTS.append(ok)
    print("%s %s %s" % ("PASS" if ok else "FAIL", name, detail))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--rows", required=True)
    ap.add_argument("--mutbat", required=True)
    ap.add_argument("--outdir", required=True)
    ns = ap.parse_args(argv)
    ns.target = os.path.abspath(ns.target)
    out = os.path.abspath(ns.outdir)
    os.makedirs(out, exist_ok=True)
    tmp = os.path.join(out, "tmp")
    os.makedirs(tmp, exist_ok=True)

    src = open(ns.target, encoding="utf-8").read()
    rows = {r["id"]: r for r in json.load(open(ns.rows, encoding="utf-8"))}
    apply_row = load("mutbat", ns.mutbat).apply_row

    def mutant(rid):
        path = os.path.join(out, "mut-%s.py" % rid.split("-")[0])
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(apply_row(src, rows[rid]))
        return path

    def env(tmpdir):
        e = dict(os.environ)
        e["TMPDIR"] = tmpdir
        return e

    # --- X09/X10/X18: the case-1 exact summary line (prefix-census). -------------------------
    root1 = fixture(os.path.join(out, "case1"), {
        "a-prefixed.md": "recheck: cd %s/case1 && true\n" % out,
        "b-relative.md": "recheck: python3 corpus/instruments/missing.py\n",
        "c-bare-pass.md": "recheck: true\n",
        "d-exit1.md": "recheck: exit 1\n",
        "e-exit7.md": "recheck: exit 7\n",
        "f-fresh-cwd.md": 'recheck: test "$(pwd -P)" = "$(cd "$TMPDIR" && pwd -P)"\n'})
    want1s = ("RECHECK-CWD entries=6 noprefix=5 exit2_foreign=1 exit0_foreign=3 "
              "exit1_foreign=1 exit_other=1 norecheck=0 restoration_only=0")
    rc, so, se = cli(ns.target, root1, env(tmp))
    base_line = summary(so)
    base_ok = base_line == [want1s]
    for rid in ("X09-SUM-noprefix-slot", "X10-SUM-exit2-zero",
                "X18-SUM-restoration-adds-noprefix"):
        mrc, mso, mse = cli(mutant(rid), root1, env(tmp))
        mline = summary(mso)
        record("%s route" % rid.split("-")[0], base_ok and mline != [want1s],
               "pristine_summary=%r mutant_summary=%r" % (base_line, mline))

    # --- X11: no ENTRY for the prefixed exit-1 entry in case 21's default output -------------
    root21 = fixture(os.path.join(out, "case21"), {
        "osv-a.md": "recheck: cd %s/case21 && true\n" % out,
        "osv-b.md": "recheck: cd %s/case21 && exit 1\n" % out,
        "z-c.md": "recheck: cd %s/case21 && true\n" % out})
    rc, so, se = cli(ns.target, root21, env(tmp))
    mrc, mso, mse = cli(mutant("X11-ENTRY-exit1"), root21, env(tmp))
    record("X11 route", "ENTRY osv-b.md" not in so and "ENTRY osv-b.md" in mso,
           "pristine_has=%s mutant_has=%s" % ("ENTRY osv-b.md" in so,
                                              "ENTRY osv-b.md" in mso))

    # --- X08: case-14 extended fixture, want14 noprefix=3 -----------------------------------
    root14 = fixture(os.path.join(out, "case14"), {
        "a-lane-suffix.md": "recheck: cd %s/case14-x && true\n" % out,
        "b-no-space.md": "recheck: cd %s/case14 &&true\n" % out,
        "c-prefixed.md": "recheck: cd %s/case14 && true\n" % out,
        "d-mid.md": "recheck: true && cd %s/case14 && true\n" % out})
    want14 = ("RECHECK-CWD entries=4 noprefix=3 exit2_foreign=0 exit0_foreign=3 "
              "exit1_foreign=1 exit_other=0 norecheck=0 restoration_only=0")
    rc, so, se = cli(ns.target, root14, env(tmp))
    mrc, mso, mse = cli(mutant("X08-NOPREFIX-in"), root14, env(tmp))
    record("X08 route", summary(so) == [want14] and summary(mso) != [want14],
           "pristine=%r mutant=%r" % (summary(so), summary(mso)))

    # --- X06: census(root1) with TMPDIR unset equals the TMPDIR-set run; mutant raises ------
    e_unset = env(tmp)
    e_unset.pop("TMPDIR", None)
    e_unset["TMP"] = tmp
    u_rc, u_so, u_se = cli(ns.target, root1, e_unset)
    m_rc, m_so, m_se = cli(mutant("X06-ENV-tmp-unset"), root1, e_unset)
    record("X06 route", summary(u_so) == base_line and summary(m_so) == [],
           "unset_summary=%r mutant_stderr=%r" % (summary(u_so), m_se.strip().splitlines()[-1:]))

    # --- X07: case-8 n-neither with the prose mention keeps norecheck=1 ---------------------
    root8 = fixture(os.path.join(out, "case8"), {
        "n-neither.md": "body only, no recheck header\n"
                        "- documents `restoration-recheck:` mid-line\n",
        "p.md": "recheck: cd %s/case8 && true\n" % out})
    want8u = ("RECHECK-CWD entries=2 noprefix=0 exit2_foreign=0 exit0_foreign=1 "
              "exit1_foreign=0 exit_other=0 norecheck=1 restoration_only=0")
    rc, so, se = cli(ns.target, root8, env(tmp))
    mrc, mso, mse = cli(mutant("X07-REST-substr"), root8, env(tmp))
    record("X07 route", summary(so) == [want8u] and summary(mso) != [want8u],
           "pristine=%r mutant=%r" % (summary(so), summary(mso)))

    # --- X12: verbose timeout path renders foreign_exit=-1 ----------------------------------
    rooth = fixture(os.path.join(out, "hang"), {
        "h-hang.md": "recheck: cd %s/hang && exec sleep 3\n" % out})
    base_mod = load("cand_base", ns.target)
    mut_mod = load("cand_mut_x12", mutant("X12-TIMEOUT-sentinel"))
    import io
    from contextlib import redirect_stdout

    def sentinel(mod):
        mod.TIMEOUT = 1
        buf = io.StringIO()
        old = dict(os.environ)
        os.environ["TMPDIR"] = tmp
        try:
            with redirect_stdout(buf):
                mod.census(rooth, rooth, True)
        finally:
            os.environ.clear()
            os.environ.update(old)
        lines = [ln for ln in buf.getvalue().splitlines() if ln.startswith("ENTRY ")]
        return lines[0] if lines else None

    b_s = sentinel(base_mod)
    m_s = sentinel(mut_mod)
    record("X12 route", b_s == "ENTRY h-hang.md noprefix=0 foreign_exit=-1"
           and m_s != b_s, "pristine=%r mutant=%r" % (b_s, m_s))

    # --- X13: end-to-end CLI on a conformant fixture ----------------------------------------
    rootc = fixture(os.path.join(out, "conform"), {
        "p.md": "recheck: cd %s/conform && true\n" % out})
    rc, so, se = cli(ns.target, rootc, env(tmp))
    mrc, mso, mse = cli(mutant("X13-MAIN-argv-slice"), rootc, env(tmp))
    record("X13 route", rc == 0 and "RECHECK-CWD-RESULT conformant" in so
           and (mrc != 0 or "RECHECK-CWD-RESULT conformant" not in mso),
           "pristine_rc=%d mutant_rc=%d mutant_usage=%s" % (rc, mrc, "usage:" in mse))

    # --- X14: bare invocation in an empty knowledge tree ------------------------------------
    roote = fixture(os.path.join(out, "empty"), {})
    rc, so, se = cli(ns.target, roote, env(tmp), cwd=roote,
                     argv=[PY, "-B", ns.target])
    mrc, mso, mse = cli(mutant("X14-MAIN-defroot"), roote, env(tmp), cwd=roote,
                        argv=[PY, "-B", mutant("X14-MAIN-defroot")])
    record("X14 route", rc == 0 and "RECHECK-CWD entries=0" in so
           and (mrc != 0 or "RECHECK-CWD entries=0" not in mso),
           "pristine_rc=%d mutant_rc=%d" % (rc, mrc))

    # --- X16: one invalid UTF-8 byte --------------------------------------------------------
    rootb = fixture(os.path.join(out, "bytes"), {})
    with open(os.path.join(rootb, "corpus", "knowledge", "z-latin1.md"), "wb") as fh:
        fh.write(b"# caf\xe9\nrecheck: cd " + rootb.encode() + b" && true\n")
    rc, so, se = cli(ns.target, rootb, env(tmp))
    mrc, mso, mse = cli(mutant("X16-FIRST-errors"), rootb, env(tmp))
    record("X16 route", "entries=1" in so and "exit0_foreign=1" in so
           and "UnicodeDecodeError" in mse,
           "pristine_rc=%d mutant_rc=%d decode_error=%s"
           % (rc, mrc, "UnicodeDecodeError" in mse))

    # --- X21: conform_ok on the coupled two-defect counts -----------------------------------
    coupled = {"entries": 2, "noprefix": 0, "exit2_foreign": 0, "exit0_foreign": 0,
               "exit1_foreign": 0, "exit_other": 0, "norecheck": 1, "restoration_only": 1}
    record("X21 route", base_mod.conform_ok(coupled) is False
           and load("cand_mut_x21",
                    mutant("X21-CONFORM-couple-norecheck-restoration")).conform_ok(coupled) is True,
           "pristine=%r mutant=%r" % (base_mod.conform_ok(coupled),
                                      load("cand_mut_x21b",
                                           mutant("X21-CONFORM-couple-norecheck-restoration")
                                           ).conform_ok(coupled)))

    # --- X15: the TIMEOUT default pin -------------------------------------------------------
    x15_base = load("cand_base_x15", ns.target)   # X12 patched base_mod.TIMEOUT
    x15_mut = load("cand_mut_x15", mutant("X15-TIMEOUT-default"))
    record("X15 route", x15_base.TIMEOUT == 120 and x15_mut.TIMEOUT != 120,
           "pristine=%r mutant=%r" % (x15_base.TIMEOUT, x15_mut.TIMEOUT))

    print("ROUTECHECK pass=%d fail=%d" % (sum(1 for r in RESULTS if r),
                                          sum(1 for r in RESULTS if not r)))
    return 0 if all(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
