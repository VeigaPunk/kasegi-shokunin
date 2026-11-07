#!/usr/bin/env python3
"""witness.py -- re-runnable behaviour witnesses for the MutC1Hunt r84 rows.

For every row: build the pristine target and the mutant (mutbat.apply_row), build the fixture
set once under --outdir, run the row's witness against both, and print one JSON line:
  {"id", "kind", "witness", "pristine", "mutant", "differs"}
kind=equivalent rows are expected to print differs=false; gap rows differs=true.

Usage: python3 -B witness.py --target <candidate> --rows <rows.json> --outdir <dir> [--only ID]
Everything is written under --outdir (pass a scratch dir); nothing under /tmp.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def load_apply_row(mutbat_path):
    spec = importlib.util.spec_from_file_location("mutbat", mutbat_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.apply_row


def write_fixture(root, entries):
    kdir = os.path.join(root, "corpus", "knowledge")
    os.makedirs(kdir, exist_ok=True)
    for name, body in entries.items():
        path = os.path.join(kdir, name)
        mode = "wb" if isinstance(body, bytes) else "w"
        with open(path, mode) as fh:
            fh.write(body)
    return root


def cli(target, root, extra=(), cwd=None, env=None, argv=None):
    args = argv if argv is not None else [PY, "-B", target, "--root", root, "--lane", root]
    proc = subprocess.run(args, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                          capture_output=True, text=True, timeout=300)
    return {"rc": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}


def summary_of(out):
    return [ln for ln in out.splitlines() if ln.startswith("RECHECK-CWD entries=")]


def base_env(tmp):
    env = dict(os.environ)
    env["TMPDIR"] = tmp
    return env


def run_imp(mode, target, fixture, tmp, env=None):
    args = [PY, "-B", os.path.join(HERE, "imp.py"), mode, target, fixture]
    proc = subprocess.run(args, env=env or base_env(tmp), stdin=subprocess.DEVNULL,
                          capture_output=True, text=True, timeout=300)
    lines = [ln for ln in proc.stdout.splitlines() if ln.startswith("{")]
    if not lines:
        return {"error": "no json", "rc": proc.returncode, "stderr": proc.stderr[-400:]}
    return json.loads(lines[-1])


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--rows", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--mutbat", default="/home/vgpnk/Projects/shokunin/kasegi-shokunin/"
                                        ".ufo/waves/round-84/c1/mutbat.py")
    ap.add_argument("--only", default=None)
    ns = ap.parse_args(argv)

    out = os.path.abspath(ns.outdir)
    tmp = os.path.join(out, "tmp")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(tmp)

    with open(ns.target, encoding="utf-8") as fh:
        src = fh.read()
    with open(ns.rows, encoding="utf-8") as fh:
        rows = json.load(fh)
    rows_by_id = {r["id"]: r for r in rows}
    apply_row = load_apply_row(ns.mutbat)

    base = os.path.basename(ns.target)
    pristine = os.path.join(out, "pristine", base)
    os.makedirs(os.path.dirname(pristine))
    with open(pristine, "w", encoding="utf-8") as fh:
        fh.write(src)

    fixroot = os.path.join(out, "fix")
    os.makedirs(fixroot)
    F = {}

    def fixture(name, entries):
        root = write_fixture(os.path.join(fixroot, name), entries)
        F[name] = root
        return root

    conf = fixture("conform", {"p.md": "recheck: cd %s/conform && true\n"
                               % fixroot})
    empty = fixture("empty", {})
    rest = fixture("rest", {"n-note.md": "# fixture\nbody only, no recheck header\n"
                                        "- documents `restoration-recheck:` mid-line\n"})
    mid = fixture("mid", {"p-mid.md": "recheck: true && cd %s/mid && true\n" % fixroot})
    sumfix = fixture("sum", {"a-bare.md": "recheck: true\n",
                             "b-exit2.md": "recheck: cd %s/sum && exit 2\n" % fixroot})
    exit1 = fixture("exit1", {"q-exit1.md": "recheck: cd %s/exit1 && exit 1\n" % fixroot})
    hang = fixture("hang", {"h-hang.md": "recheck: cd %s/hang && exec sleep 3\n" % fixroot})
    sleep2 = fixture("sleep2", {"s-slow.md": "recheck: cd %s/sleep2 && sleep 2\n" % fixroot})
    bytesfix = fixture("bytes", {"z-latin1.md":
                                 b"# caf\xe9\nrecheck: cd " + fixroot.encode()
                                 + b"/bytes && true\n"})
    couple = fixture("couple", {"n.md": "body only, no header\n",
                                "r.md": "restoration-recheck: touch %s/couple/marker\n"
                                        % fixroot})
    matrix = fixture("matrix", {
        "a-pass.md": "recheck: cd %s/matrix && true\n" % fixroot,
        "b-bare.md": "recheck: true\n",
        "c-exit1.md": "recheck: cd %s/matrix && exit 1\n" % fixroot,
        "d-exit7.md": "recheck: cd %s/matrix && exit 7\n" % fixroot,
        "e-exit2.md": "recheck: cd %s/matrix && exit 2\n" % fixroot,
        "f-rest.md": "restoration-recheck: touch %s/matrix/marker\n" % fixroot,
        "g-none.md": "body only\n",
        "h-two.md": "recheck: cd %s/matrix && exit 1\nrecheck: cd %s/matrix && true\n"
                    % (fixroot, fixroot)})

    def fixture_path(name):
        return F[name]

    def witness_leak(target, which):
        obs = run_imp("leak", target, F["empty"], tmp)
        return {"rc": obs.get("rc"), "restored": obs.get(which)}

    def witness_cli(target, fname):
        obs = cli(target, fixture_path(fname))
        return {"rc": obs["rc"], "summary": summary_of(obs["stdout"]),
                "result": [ln for ln in obs["stdout"].splitlines()
                           if ln.startswith("RECHECK-CWD-RESULT")],
                "entries": [ln for ln in obs["stdout"].splitlines()
                            if ln.startswith("ENTRY ")],
                "markers": [ln.split()[0] for ln in obs["stdout"].splitlines()
                            if ln.startswith(("NORECHECK ", "RESTORATION-ONLY "))],
                "stderr_tail": obs["stderr"].strip().splitlines()[-1:] }

    def witness_env_unset(target):
        env = base_env(tmp)
        env.pop("TMPDIR", None)
        env["TMP"] = tmp
        obs = cli(target, F["conform"], env=env)
        return {"rc": obs["rc"], "summary": summary_of(obs["stdout"]),
                "result": [ln for ln in obs["stdout"].splitlines()
                           if ln.startswith("RECHECK-CWD-RESULT")],
                "stderr_tail": obs["stderr"].strip().splitlines()[-1:]}

    def witness_argvs(target):
        obs = cli(target, F["conform"])
        return {"rc": obs["rc"], "result": [ln for ln in obs["stdout"].splitlines()
                                            if ln.startswith("RECHECK-CWD-RESULT")],
                "usage": "usage:" in obs["stderr"]}

    def witness_defroot(target):
        obs = cli(target, F["empty"], argv=[PY, "-B", target], cwd=F["empty"],
                  env=base_env(tmp))
        return {"rc": obs["rc"], "summary": summary_of(obs["stdout"]),
                "result": [ln for ln in obs["stdout"].splitlines()
                           if ln.startswith("RECHECK-CWD-RESULT")],
                "stderr_tail": obs["stderr"].strip().splitlines()[-1:]}

    def witness_bytes(target):
        obs = cli(target, F["bytes"])
        return {"rc": obs["rc"], "summary": summary_of(obs["stdout"]),
                "decode_error": "UnicodeDecodeError" in obs["stderr"]}

    def witness_couple(target):
        marker = os.path.join(F["couple"], "marker")
        existed = os.path.exists(marker)
        obs = cli(target, F["couple"])
        return {"rc": obs["rc"], "summary": summary_of(obs["stdout"]),
                "result": [ln for ln in obs["stdout"].splitlines()
                           if ln.startswith("RECHECK-CWD-RESULT")],
                "marker_created": os.path.exists(marker) and not existed}

    def witness_matrix(target):
        obs = cli(target, F["matrix"])
        return {"rc": obs["rc"], "stdout_sha256": hashlib.sha256(
            obs["stdout"].encode("utf-8")).hexdigest(), "summary": summary_of(obs["stdout"])}

    def witness_grid(target):
        return run_imp("grid", target, F["empty"], tmp)

    def witness_timeout(target, mode):
        return run_imp(mode, target, F["hang" if mode == "timeout" else "sleep2"], tmp)

    # id -> witness kind, argument
    SPEC = {
        "X01-LK-runforeign": ("gap", lambda t: witness_leak(t, "run_foreign_restored")),
        "X02-LK-selftest": ("gap", lambda t: witness_leak(t, "selftest_restored")),
        "X03-LK-chdir": ("gap", lambda t: witness_leak(t, "cwd_restored")),
        "X04-LK-timeout": ("gap", lambda t: witness_leak(t, "timeout")),
        "X05-LK-mkdtemp": ("gap", lambda t: witness_leak(t, "mkdtemp_restored")),
        "X06-ENV-tmp-unset": ("gap", witness_env_unset),
        "X07-REST-substr": ("gap", lambda t: witness_cli(t, "rest")),
        "X08-NOPREFIX-in": ("gap", lambda t: witness_cli(t, "mid")),
        "X09-SUM-noprefix-slot": ("gap", lambda t: witness_cli(t, "sum")),
        "X10-SUM-exit2-zero": ("gap", lambda t: witness_cli(t, "sum")),
        "X11-ENTRY-exit1": ("gap", lambda t: witness_cli(t, "exit1")),
        "X12-TIMEOUT-sentinel": ("gap", lambda t: witness_timeout(t, "timeout")),
        "X13-MAIN-argv-slice": ("gap", witness_argvs),
        "X14-MAIN-defroot": ("gap", witness_defroot),
        "X15-TIMEOUT-default": ("gap", lambda t: witness_timeout(t, "timeout-default")),
        "X16-FIRST-errors": ("gap", witness_bytes),
        "X17-STRIP-space": ("equivalent", witness_matrix),
        "X18-SUM-restoration-adds-noprefix": ("gap", lambda t: witness_cli(t, "matrix")),
        "X24-CONFORM-sum-add-noprefix": ("equivalent", witness_grid),
        "X25-USAGE-except-breadth": ("equivalent", witness_matrix),
        "X19-SUM-entries-slot": ("killed", lambda t: witness_cli(t, "sum")),
        "X20-ENTRY-drop-exit2": ("killed", lambda t: witness_cli(t, "matrix")),
        "X21-CONFORM-couple-norecheck-restoration": ("gap", witness_couple),
        "X22-CONFORM-exit2-le-noprefix": ("equivalent", witness_grid),
        "X23-NEUTRAL-comment": ("neutral", witness_matrix),
    }

    ids = [r["id"] for r in rows]
    missing = [i for i in ids if i not in SPEC]
    if missing:
        print("MISSING witness spec: %s" % missing)
        return 2
    lines = []
    for rid in ids:
        if ns.only and rid != ns.only:
            continue
        kind, fn = SPEC[rid]
        row = rows_by_id[rid]
        mdir = os.path.join(out, "mut", rid)
        os.makedirs(mdir)
        mpath = os.path.join(mdir, base)
        mutant = apply_row(src, row)
        if mutant is None:
            lines.append({"id": rid, "kind": kind, "error": "not derived"})
            continue
        with open(mpath, "w", encoding="utf-8") as fh:
            fh.write(mutant)
        pristine_obs = fn(pristine)
        mutant_obs = fn(mpath)
        rec = {"id": rid, "kind": kind, "witness": getattr(fn, "__name__", "lambda"),
               "pristine": pristine_obs, "mutant": mutant_obs,
               "differs": pristine_obs != mutant_obs}
        lines.append(rec)
        print(json.dumps(rec, sort_keys=True))
    diffs = sum(1 for r in lines if r.get("differs"))
    print("WITNESS rows=%d differs=%d" % (len(lines), diffs))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
