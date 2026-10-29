#!/usr/bin/env python3
"""R46bMutSelfC2b witness builder.

For each surviving mutant, construct a concrete tree on which the MUTATED counter
gives a different verdict from the PRISTINE counter. A survivor with such a witness
is a genuine coverage hole in the committed selftest (the mutant changes a verdict
on some real input); a survivor without one is an equivalent mutant.

The tree is built with the committed selftest's OWN builder (r46-counters-selftest-c2.py
imported as a module) so the fixture matches what the selftest grades.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S = "/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2b"
PURE = os.path.join(S, "pure")
WIT = os.path.join(S, "witness")

spec = importlib.util.spec_from_file_location(
    "st_c2", os.path.join(LANE, "corpus/instruments/r46-counters-selftest-c2.py"))
st = importlib.util.module_from_spec(spec)
sys.modules["st_c2"] = st
spec.loader.exec_module(st)


def gates(counter, root, extra_env=None):
    env = dict(os.environ)
    env["TMPDIR"] = os.path.join(S, "tmp")
    os.makedirs(env["TMPDIR"], exist_ok=True)
    if extra_env:
        env.update(extra_env)
    p = subprocess.run([sys.executable, counter, "--root", root],
                       capture_output=True, text=True, timeout=600, cwd=LANE, env=env)
    out = p.stdout + p.stderr
    g = {m.group(1): int(m.group(2)) for m in re.finditer(r"^gate (G\d) pass=([01])", out, re.M)}
    fx = re.search(r"^c2-gate fixed=(\d+)/7 exit=(\d)", out, re.M)
    return g, (int(fx.group(1)) if fx else -1), out


def mutant_counter(old, new, tag):
    d = os.path.join(WIT, "mut-" + re.sub(r"[^A-Za-z0-9_.-]", "_", tag))
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d, exist_ok=True)
    src = os.path.join(LANE, "corpus/instruments/r46-c2-gate.py")
    text = open(src, encoding="utf-8").read()
    assert text.count(old) == 1
    dst_inst = os.path.join(d, "corpus", "instruments")
    shutil.copytree(os.path.join(LANE, "corpus", "instruments"), dst_inst, symlinks=True)
    dst = os.path.join(dst_inst, "r46-c2-gate.py")
    open(dst, "w", encoding="utf-8").write(text.replace(old, new, 1))
    return dst


def build_base(dest):
    snap = st.Snap(LANE)
    spans = {k: (t, *snap.locate(t)) for k, t in st.Q.items()}
    st.build(PURE, LANE, snap, spans, dest)
    return snap, spans


def main():
    os.makedirs(WIT, exist_ok=True)
    sys.path.insert(0, S)
    from mutants import MUTANTS
    results = [json.loads(l) for l in open(os.path.join(S, "results.jsonl"), encoding="utf-8")]
    by_id = {r["id"]: r for r in results}
    survivors = [m for m in MUTANTS if by_id.get(m[0], {}).get("verdict") == "survivor"]
    print("survivors: %d of %d" % (len(survivors), len(MUTANTS)))

    # the witness builder for each survivor: (id, description, tree-mutation function)
    import witnesses
    base = os.path.join(WIT, "base")
    shutil.rmtree(base, ignore_errors=True)
    snap, spans = build_base(base)
    print("base tree built at %s" % base)

    pristine = os.path.join(LANE, "corpus/instruments/r46-c2-gate.py")
    report = []
    for mid, gate, old, new in survivors:
        w = witnesses.WITNESSES.get(mid)
        if w is None:
            print("NO-WITNESS-DEFINED %s" % mid)
            report.append(dict(id=mid, verdict="no-witness-defined"))
            continue
        dest = os.path.join(WIT, "case-" + re.sub(r"[^A-Za-z0-9_.-]", "_", mid))
        shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(base, dest, symlinks=True)
        try:
            w["mutate"](dest, spans, snap)
        except Exception as exc:
            print("WITNESS-BROKE %s: %r" % (mid, exc))
            report.append(dict(id=mid, verdict="witness-error", error=repr(exc)))
            continue
        mc = mutant_counter(old, new, mid)
        extra_env = None
        if mid in witnesses.REPIN:
            extra_env = witnesses.repin_manifest(dest)
        gp, fp, op = gates(pristine, dest, extra_env)
        gm, fm, om = gates(mc, dest, extra_env)
        differs = gp != gm
        print("%-40s pristine=%d/7 %s | mutant=%d/7 %s | DIFFERS=%s" %
              (mid, fp, "".join(str(gp.get("G%d" % i, 9)) for i in range(1, 8)),
               fm, "".join(str(gm.get("G%d" % i, 9)) for i in range(1, 8)), differs))
        if differs:
            print("    pristine: " + "; ".join(l for l in op.splitlines() if l.startswith("gate ")))
            print("    mutant  : " + "; ".join(l for l in om.splitlines() if l.startswith("gate ")))
        report.append(dict(id=mid, verdict="witness-differs" if differs else "witness-same",
                           pristine_fixed=fp, mutant_fixed=fm,
                           pristine_gates=gp, mutant_gates=gm,
                           description=w["description"],
                           pristine_out=op, mutant_out=om))
    with open(os.path.join(S, "witness-results.json"), "w") as fh:
        json.dump(report, fh, indent=1)
    print("witness report written")


if __name__ == "__main__":
    main()
