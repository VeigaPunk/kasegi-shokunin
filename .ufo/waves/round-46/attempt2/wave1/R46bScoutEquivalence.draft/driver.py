#!/usr/bin/env python3
"""R46bScoutEquivalence probe driver (scratch-only).

Builds, from the frozen base export and the frozen selftest module:
  base/ tip/            exactly as r46-counters-selftest-c1.py main() does
  T6  tip + trailing comment with `~/` on claim-package-contract.md recheck line
  T7  tip + trailing comment with `/home/` (no ~/ no $) on the same line
  T19 tip + ai-assisted-finding-validation.md dropped to 5 rows (green->gated at tree)
  T14 tip + claim-gates G6 token made a prefix of G1's (m_overlap_tokens replica)
Applies mutants M06/M07/M14/M19 (substring asserted to occur exactly once).
Runs the aggregate counter original vs mutant over {pure, tip, T6, T7, T19, T14},
byte-compares the stdout pairs, prints limb lines.
"""
import importlib.util, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

S = "/fast/scratch/hyaku/kasegi-r46/R46bScoutEquivalence"
LANE04 = os.path.join(S, "lane04")
PURE = os.path.join(S, "pure")
CTR = os.path.join(LANE04, "corpus/instruments/r46-c1-gate.py")
PROBE = os.path.join(S, "probe")
TREES = os.path.join(S, "trees")
CP, CG = "claim-package-contract.md", "claim-gates.md"
EXEC = "ai-assisted-finding-validation.md"

spec = importlib.util.spec_from_file_location("st", os.path.join(LANE04, "corpus/instruments/r46-counters-selftest-c1.py"))
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)
st.PUREX[0] = PURE

# --- base + tip, replicating selftest main() -------------------------------
shutil.rmtree(TREES, ignore_errors=True)
base = os.path.join(TREES, "base")
tip = os.path.join(TREES, "tip")
shutil.copytree(PURE, base, symlinks=True)
for name in st.ROWS:
    st.BASE_LINE[name] = next(ln for ln in st.rd(PURE, "corpus/knowledge/" + name).split("\n") if ln.startswith("recheck:"))
st.build_tip(PURE, CTR, tip)
print("BUILD base+tip ok")

# --- probe trees ------------------------------------------------------------
t6 = os.path.join(TREES, "T6"); shutil.copytree(tip, t6, symlinks=True)
st.set_recheck(t6, CP, st.rec_line(CP) + "  # r46 re-ground, mirrors ~/Projects/bounties")

t7 = os.path.join(TREES, "T7"); shutil.copytree(tip, t7, symlinks=True)
st.set_recheck(t7, CP, st.rec_line(CP) + "  # r46 re-ground, base lived under /home/vgpnk")

import re as _re

def _grows(text):
    return [ln for ln in text.split("\n") if _re.match(r"^\|\s*G\d+\s*\|", ln)]

# pick a base-EXECUTING entry with the counter's own classifier
cspec = importlib.util.spec_from_file_location("ctr", CTR)
ctr = importlib.util.module_from_spec(cspec)
cspec.loader.exec_module(ctr)
cb_cls = ctr.classify(PURE)
execs = sorted(k for k, v in cb_cls.items() if v["class"] == "executes")
assert execs, "no executing entry in pure"
D = execs[0]
print("BUILD T19 target D=%s (base class=%s); execs=%s" % (D, cb_cls[D]["class"], execs))

t19 = os.path.join(TREES, "T19"); shutil.copytree(tip, t19, symlinks=True)
drows = _grows(st.rd(t19, "corpus/knowledge/" + D))
if len(drows) >= 6:
    dids = [ln.split("|")[1].strip() for ln in drows]
    st.drop_rows(t19, D, dids[5:])  # leave 5 rows -> entry mode red
st.set_recheck(t19, D, "recheck: cd %s && python3 %s --entry corpus/knowledge/%s" % (st.LANE, st.GATE, D))
ct19 = ctr.classify(t19)
assert ct19[D]["class"] == "gated", (D, ct19[D])
assert all(v["class"] != "broken" for v in ct19.values()), [k for k, v in ct19.items() if v["class"] == "broken"]
print("BUILD T19 ok (%s gated at tree, broken=0)" % D)

t14 = os.path.join(TREES, "T14"); shutil.copytree(tip, t14, symlinks=True)
anchor = st.loc(PURE, st.CK, "MAX_SCAN_BYTES = 5 * 1024 * 1024", 2)
st.row_edit(t14, CG, "G6", lambda ln: "| G6 | subchecks no_secrets and operator_attribution | `%s` | `MAX_SCAN_BYTES = 5` |" % anchor)
print("BUILD T14 ok (G6 anchor=%s)" % anchor)

# --- mutant counters (same triples as r46-mutbat.py C1_MUTANTS) -------------
MUT = {
    "M06": ('or HOME_RE.search(CD_RE.sub("", ct[e]["line"], count=1))', ""),
    "M07": ('re.compile(r"(?:~/|\\$HOME|\\$\\{HOME\\}|/home/)")',
            're.compile(r"(?:~/|\\$HOME|\\$\\{HOME\\})")'),
    "M14": ("if p.returncode == 0 or red != [r[0]]:", "if red != [r[0]]:"),
    "M19": ("and len(gt) == len(gb) - len(reg) and not (gt - gb)", "and len(gt) <= len(gb)"),
}
src = open(CTR, encoding="utf-8").read()
muts = {}
for mid, (old, new) in MUT.items():
    n = src.count(old)
    assert n == 1, "mutant=%s old-substring occurs %d times" % (mid, n)
    # mutbat.apply_mutant semantics: the mutant lives in a copy of the tree's whole
    # instruments dir, so TOOL_LANE = dirname^3(SELF) still resolves to real instruments
    md = os.path.join(S, "mutants", mid)
    shutil.rmtree(md, ignore_errors=True)
    os.makedirs(md)
    shutil.copytree(os.path.join(LANE04, "corpus", "instruments"), os.path.join(md, "corpus", "instruments"), symlinks=True)
    p = os.path.join(md, "corpus", "instruments", "r46-c1-gate.py")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(src.replace(old, new, 1))
    muts[mid] = p
print("MUTANTS applied ok")

# --- gate runs ---------------------------------------------------------------
def run(tag, counter, tree, baseline):
    w = os.path.join(S, "work", tag)
    os.makedirs(w, exist_ok=True)
    env = dict(os.environ, TMPDIR=w)
    p = subprocess.run([sys.executable, "-I", counter, "--root", tree, "--baseline", baseline, "--work", w],
                       capture_output=True, text=True, timeout=1500, env=env)
    with open(os.path.join(PROBE, tag + ".out"), "w") as fh:
        fh.write(p.stdout)
        if p.stderr:
            fh.write("\n--stderr--\n" + p.stderr)
    keep = [ln for ln in p.stdout.splitlines() if ln.startswith("gate ") or ln.startswith("c1-gate ")]
    print("RUN %-12s rc=%d | %s" % (tag, p.returncode, " ; ".join(keep)))
    return tag, p.returncode, p.stdout

jobs = [
    ("orig-pure", CTR, PURE, PURE),
    ("orig-tip", CTR, tip, base),
    ("orig-T6", CTR, t6, base),
    ("orig-T7", CTR, t7, base),
    ("orig-T19", CTR, t19, base),
    ("orig-T14", CTR, t14, base),
    ("M06-pure", muts["M06"], PURE, PURE),
    ("M06-tip", muts["M06"], tip, base),
    ("M06-T6", muts["M06"], t6, base),
    ("M07-tip", muts["M07"], tip, base),
    ("M07-T7", muts["M07"], t7, base),
    ("M19-tip", muts["M19"], tip, base),
    ("M19-T19", muts["M19"], t19, base),
    ("M14-pure", muts["M14"], PURE, PURE),
    ("M14-tip", muts["M14"], tip, base),
    ("M14-T6", muts["M14"], t6, base),
    ("M14-T19", muts["M14"], t19, base),
    ("M14-T14", muts["M14"], t14, base),
]
with ThreadPoolExecutor(max_workers=4) as ex:
    outs, rcs = {}, {}
    for tag, rc, so in ex.map(lambda j: run(*j), jobs):
        outs[tag], rcs[tag] = so, rc

# --- byte comparisons --------------------------------------------------------
print("\n== stdout byte-comparison ==")
SAME = [("orig-tip", "M06-tip"), ("orig-tip", "M07-tip"), ("orig-tip", "M19-tip"), ("orig-tip", "M14-tip"),
        ("orig-pure", "M06-pure"), ("orig-pure", "M14-pure"),
        ("orig-T14", "M14-T14"), ("orig-T6", "M14-T6"), ("orig-T19", "M14-T19")]
DIFF = [("orig-T6", "M06-T6"), ("orig-T7", "M07-T7"), ("orig-T19", "M19-T19")]
for a, b in SAME + DIFF:
    eq = outs[a] == outs[b]
    print("cmp %-10s vs %-10s -> %s" % (a, b, "IDENTICAL" if eq else "DIFFERS"))

# --- clause site line numbers in the frozen counter --------------------------
print("\n== frozen counter clause sites ==")
for i, ln in enumerate(open(CTR, encoding="utf-8"), 1):
    if ("HOME_RE = re.compile" in ln or "bad3 = [e for e in reg" in ln or
        'or HOME_RE.search(CD_RE.sub' in ln or "ok = len(reg) >= MIN_REGROUNDED" in ln or
        "if p.returncode == 0 or red != [r[0]]:" in ln or "ok = len(gt) <= TARGET_GATED" in ln):
        print("%d: %s" % (i, ln.rstrip("\n")))
print("\n== frozen selftest case sites ==")
stf = os.path.join(LANE04, "corpus/instruments/r46-counters-selftest-c1.py")
for i, ln in enumerate(open(stf, encoding="utf-8"), 1):
    if ("def m_home_tilde" in ln or "def m_home_var" in ln or "def m_cd_home" in ln or
        "def m_trailing_comment_ok" in ln or "def m_new_gated" in ln or "def m_overlap_tokens" in ln or
        '"P-trailing-comment-on-recheck-line"' in ln or '"L3-line-has-tilde-path"' in ln or
        '"L3-line-has-HOME-var"' in ln or '"L3-cd-tilde-home-target"' in ln or
        '"L1-new-gated-entry"' in ln or '"L6-overlapping-tokens-not-isolated"' in ln or
        '"L2-only-one-reground"' in ln):
        print("%d: %s" % (i, ln.rstrip("\n")))
print("DRIVER DONE")
