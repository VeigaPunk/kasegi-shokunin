#!/usr/bin/env python3
"""derive-head-census.py — census of the derive gate's python-head option policy.

Two limbs, both read from committed bytes of the gate plus one behavioural probe:

1. WRITE-CLASS DECLARATIONS.  A head that declares an option naming a write root, an
   output path or an ingress URL (WRITE_CLASS) but whose gate denial set omits that
   name is a head the gate will admit while writing outside the tree.  The census
   AST-reads every instrument's ``add_argument`` literals, AST-reads the gate's
   ``PY_DENIED_ANY`` / ``PY_DENIED_BY_SCRIPT`` tables, and prints the count of
   (head, flag) pairs the gate would ADMIT.  Target: 0.

2. ALIAS KEYING.  A head is keyed to its policy by NAME; if the name comes from the
   path the derive happens to use, an in-directory symlink under a fixture name
   restores the denied flags of the file it points at.  The probe builds a scratch
   tree whose ``corpus/instruments/ok.py`` is a symlink to ``gate-quote-audit.py``
   (whose ``--json`` is denied per script) and asks the gate to run
   ``python3 corpus/instruments/ok.py --json out/alias.json``.  Target: refused
   (``rc=2 reason=derive-not-read-only``).

3. POSITIVE CONTROL.  A gate that refuses everything would pass both limbs above,
   so two read-only derives that the round-71 repair deliberately admitted (a
   ``--root`` read and a stdout ``--json`` read) must still be admitted.  Target:
   ``POSITIVE=2`` admitted.

Usage: python3 corpus/instruments/derive-head-census.py [--gate PATH] [--instruments DIR]

Exit codes: 0 READMITTED=0 and alias refused; 1 either limb fails (the fail-closed
direction: a red census is a gate defect, a green one a repaired gate); 2 harness or
read error (gate/tables unparsable, probe could not run).
"""
import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile

WRITE_CLASS = ("--out", "--output", "--work", "--scratch", "--url")


def load_tables(gate):
    """Return (denied_any, denied_by_script) from the gate's module-level literals."""
    tree = ast.parse(open(gate, encoding="utf-8").read(), gate)
    found = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        if target.id in ("PY_DENIED_ANY", "PY_DENIED_BY_SCRIPT"):
            found[target.id] = ast.literal_eval(node.value)
    missing = {"PY_DENIED_ANY", "PY_DENIED_BY_SCRIPT"} - set(found)
    if missing:
        raise SystemExit("census: gate tables unreadable: " + ",".join(sorted(missing)))
    return found["PY_DENIED_ANY"], found["PY_DENIED_BY_SCRIPT"]


def declared_options(path):
    """Every long option string a python head declares through add_argument."""
    try:
        tree = ast.parse(open(path, encoding="utf-8").read(), path)
    except (SyntaxError, UnicodeDecodeError):
        return set()
    out = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = getattr(func, "attr", None) or getattr(func, "id", None)
        if name != "add_argument":
            continue
        for arg in node.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                if arg.value.startswith("--"):
                    out.add(arg.value.split("=", 1)[0])
    return out


def write_class_census(instruments, denied_any, denied_by_script):
    rows = []
    heads = sorted(f for f in os.listdir(instruments) if f.endswith(".py"))
    for head in heads:
        declared = declared_options(os.path.join(instruments, head))
        denied = set(denied_any) | set(denied_by_script.get(head, ()))
        for flag in sorted(declared):
            if flag in WRITE_CLASS and flag not in denied:
                rows.append((head, flag))
    return heads, rows


def run_probe(scratch, gate, derive):
    """Ask the gate to admit or refuse one derive string in a scratch tree."""
    ledger = os.path.join(scratch, "ledger-%d.json" % abs(hash(derive)))
    json.dump({"figures": [{
        "id": "probe",
        "record": "probe",
        "recorded": "0",
        "derive": derive,
        "want": "0",
    }]}, open(ledger, "w", encoding="utf-8"))
    env = dict(os.environ)
    env["TMPDIR"] = scratch
    proc = subprocess.run(
        [sys.executable, os.path.join(scratch, "corpus", "instruments", "figure-audit.py"),
         "--ledger", ledger, "--root", scratch],
        cwd=scratch, env=env, capture_output=True, text=True, timeout=300)
    refused = proc.returncode == 2 and "derive-not-read-only" in proc.stderr
    detail = (proc.stderr.strip().splitlines() or [""])[-1][:160]
    return ("refused" if refused else "admitted"), "rc=%d %s" % (proc.returncode, detail)


def probes(gate, denied_by_script):
    """Behavioural limbs: the alias bypass and the two read-only positive admits."""
    if "--json" not in denied_by_script.get("gate-quote-audit.py", ()):
        raise SystemExit("census: gate-quote-audit.py no longer denies --json; probe stale")
    scratch = tempfile.mkdtemp(prefix="derive-census-", dir=os.environ.get("TMPDIR") or None)
    try:
        inst = os.path.join(scratch, "corpus", "instruments")
        os.makedirs(inst)
        here = os.path.dirname(gate)
        for head in ("figure-audit.py", "gate-quote-audit.py",
                     "capture-binding-check.py", "claim-package-check.py"):
            shutil.copy2(os.path.join(here, head), os.path.join(inst, head))
        os.symlink("gate-quote-audit.py", os.path.join(inst, "ok.py"))
        os.makedirs(os.path.join(scratch, "out"), exist_ok=True)
        alias = run_probe(scratch, gate, "python3 corpus/instruments/ok.py --json out/alias.json")
        root_read = run_probe(scratch, gate,
                              "python3 corpus/instruments/capture-binding-check.py --root .")
        json_read = run_probe(scratch, gate,
                              "python3 corpus/instruments/claim-package-check.py . --json")
        return alias, (root_read, json_read)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def main(argv):
    gate = "corpus/instruments/figure-audit.py"
    instruments = "corpus/instruments"
    i = 1
    while i < len(argv):
        if argv[i] == "--gate" and i + 1 < len(argv):
            gate = argv[i + 1]
            i += 2
        elif argv[i] == "--instruments" and i + 1 < len(argv):
            instruments = argv[i + 1]
            i += 2
        else:
            print("usage: derive-head-census.py [--gate PATH] [--instruments DIR]",
                  file=sys.stderr)
            return 2
    if not os.path.isfile(gate) or not os.path.isdir(instruments):
        print("census: gate or instrument dir missing", file=sys.stderr)
        return 2
    denied_any, denied_by_script = load_tables(gate)
    heads, rows = write_class_census(instruments, denied_any, denied_by_script)
    (alias_verdict, alias_detail), (root_read, json_read) = probes(gate, denied_by_script)
    positive = [v for v, _ in (root_read, json_read) if v == "admitted"]
    for head, flag in rows:
        print("READMITTED-ROW head=%s flag=%s" % (head, flag))
    print("CENSUS heads=%d write_class_pairs=%d READMITTED=%d"
          % (len(heads), len(WRITE_CLASS), len(rows)))
    print("ALIAS-PROBE verdict=%s %s" % (alias_verdict, alias_detail))
    print("POSITIVE admitted=%d/%d" % (len(positive), 2))
    ok = (not rows) and alias_verdict == "refused" and len(positive) == 2
    print("CENSUS-RESULT %s" % ("ok" if ok else "defect"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
