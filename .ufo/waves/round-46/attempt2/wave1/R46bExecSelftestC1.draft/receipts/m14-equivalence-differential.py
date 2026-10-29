#!/usr/bin/env python3
"""Differential proof for the C1 mutant M14-L6-exit-ignored (r46-mutbat.py's table).

M14 drops `p.returncode == 0 or` from the L6 survivor test:

    unmutated : survivor iff (p.returncode == 0 or red != [r[0]])
    M14       : survivor iff (red != [r[0]])

`p` is the counter re-run on a scratch copy of corpus/ with ONE row's token blanked.
entry_mode() exits 0 iff every row read ok=0 is absent (ok == len(rows) and the row
set is otherwise sound), so:

    p.returncode == 0  =>  red == []  =>  red != [r[0]]  =>  BOTH flag a survivor
    p.returncode != 0  =>  the second clause decides          =>  BOTH agree

The two predicates are therefore equal on every input.  This script checks that
empirically: the same trees are read by the unmutated counter and by the M14
counter and the two `gate ...`/`c1-gate ...` readings must be byte-identical.

usage: m14_equiv.py <unmutated-counter> <m14-counter> <draft-selftest> <workdir>
"""
import concurrent.futures as cf
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
unmut, m14c, selftest_path, work = sys.argv[1:5]

spec = importlib.util.spec_from_file_location("st", selftest_path)
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)

PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure2"
os.makedirs(work, exist_ok=True)
base = os.path.join(work, "base")
if not os.path.isdir(base):
    shutil.copytree(PURE, base, symlinks=True)
tip = os.path.join(work, "tip")
st.PUREX[0] = PURE
for name in st.ROWS:
    st.BASE_LINE[name] = next(ln for ln in st.rd(PURE, "corpus/knowledge/" + name).split("\n") if ln.startswith("recheck:"))
if not os.path.isdir(tip):
    st.build_tip(PURE, unmut, tip)

# the L6-relevant recipes (the ones that change what a row mutation does) plus the tree itself
RECIPES = ["m_token_absent", "m_anchor_moved", "m_short_token", "m_hash_token", "m_planted_in_place",
           "m_overlap_tokens", "m_dup_token", "m_dup_anchor_range", "m_tautology", "m_one_anchor_file",
           "m_five_rows", "m_pipe_token", "m_anchor_symlink", "m_anchor_outside"]


def reading(counter, tree, base_dir, tag):
    p = subprocess.run([sys.executable, counter, "--root", tree, "--baseline", base_dir, "--work", work],
                       capture_output=True, text=True, timeout=900)
    keep = [ln for ln in p.stdout.splitlines() if ln.startswith("gate ") or ln.startswith("c1-gate ")]
    return "\n".join(keep)


def one(name):
    d = tempfile.mkdtemp(prefix="m14-", dir=work)
    t = os.path.join(d, "tree")
    shutil.copytree(tip, t, symlinks=True)
    if name != "TIP":
        getattr(st, name)(t)
    a = reading(unmut, t, base, name)
    b = reading(m14c, t, base, name)
    shutil.rmtree(d, ignore_errors=True)
    return name, a, b


trees = ["TIP"] + RECIPES
diffs = 0
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    for name, a, b in ex.map(one, trees):
        same = a == b
        if not same:
            diffs += 1
        print("tree=%-22s identical=%s" % (name, same))
        if not same:
            print("--- unmutated ---\n%s\n--- M14 ---\n%s" % (a, b))
print("m14-equivalence trees=%d differing=%d" % (len(trees), diffs))
sys.exit(1 if diffs else 0)
