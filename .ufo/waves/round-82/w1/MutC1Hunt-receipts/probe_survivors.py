#!/usr/bin/env python3
"""Bounded probe for the seven SURVIVED rows of the MutC1Hunt r82 hunt table.

Runs only on scratch copies of the frozen candidate; never touches the lane tree.
For each survivor: either an exhaustive function-level equivalence check (H03/H08/H21)
or a behavioural witness that the mutant changes observable behaviour the selftest does
not observe (H04/H05/H10/H19).
"""
import importlib.util
import itertools
import os
import subprocess
import sys
import tempfile

S = os.path.dirname(os.path.abspath(__file__))
TARGET = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-82/c1/recheck-cwd-census.py"
SRC = open(TARGET, encoding="utf-8").read()

MUT = {
    "H03": ('+ counts["exit_other"] + counts["norecheck"] + counts["restoration_only"])\n',
            '+ counts["exit_other"] + counts["restoration_only"] + counts["restoration_only"])\n'),
    "H04": ('+ counts["exit_other"] + counts["norecheck"] + counts["restoration_only"])\n',
            '+ counts["norecheck"] + counts["norecheck"] + counts["restoration_only"])\n'),
    "H05": ('and counts["norecheck"] == 0 and counts["restoration_only"] == 0\n'
            '            and buckets == counts["entries"])\n',
            'and counts["norecheck"] == 0 and counts["restoration_only"] == 0\n'
            '            and buckets >= counts["entries"])\n'),
    "H08": ('    conform = conform_ok(counts)\n    print("RECHECK-CWD-RESULT',
            '    conform = conform_ok(dict(counts))\n    print("RECHECK-CWD-RESULT'),
    "H10": ('        elif argv[i] == "--verbose":\n            verbose = True\n',
            '        elif argv[i] == "--verbose":\n            verbose = False\n'),
    "H19": ('              "ENTRY a-prefixed.md" not in out22\n',
            '              len(out22) > 0\n'),
    "S07M": ('    root, lane, verbose = ".", DEFAULT_LANE, False\n',
             '    root, lane, verbose = ".", DEFAULT_LANE, True\n'),
}


def mutant_source(tag):
    a, b = MUT[tag]
    assert SRC.count(a) == 1, (tag, SRC.count(a))
    return SRC.replace(a, b, 1)


def load(tag, text):
    d = tempfile.mkdtemp(prefix="probe-%s-" % tag, dir=S)
    p = os.path.join(d, "recheck-cwd-census.py")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    spec = importlib.util.spec_from_file_location("cand_" + tag, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def keys():
    return ["entries", "noprefix", "exit2_foreign", "exit0_foreign", "exit1_foreign",
            "exit_other", "norecheck", "restoration_only"]


def domain():
    for vals in itertools.product(range(4), repeat=8):
        yield dict(zip(keys(), vals))


def main():
    base = load("base", SRC)
    out = []
    # H03 / H04 / H05: compare conform_ok over the exhaustive 0..3^8 domain.
    for tag in ("H03", "H04", "H05"):
        mod = load(tag, mutant_source(tag))
        diffs = []
        for c in domain():
            if base.conform_ok(c) != mod.conform_ok(c):
                diffs.append(c)
                if len(diffs) >= 3:
                    break
        out.append("EQUIV-HUNT %s conform_ok_diffs=%s witness=%s"
                   % (tag, "0" if not diffs else "yes", diffs))
    # H08: conform_ok(dict(counts)) vs conform_ok(counts) over the same domain.
    mod = load("H08", mutant_source("H08"))
    diffs = [c for c in domain() if base.conform_ok(c) != mod.conform_ok(dict(c))]
    out.append("EQUIV-HUNT H08 conform_ok_diffs=%d" % len(diffs))
    # H21: the two identity predicates agree for every boolean conform_ok returns.
    vals = {base.conform_ok(c) for c in domain()}
    same = all((v is False) == (v is not True) for v in vals)
    out.append("EQUIV-HUNT H21 conform_ok_values=%s isFalse_eq_isNotTrue=%s"
               % (sorted(map(repr, vals)), same))
    # H04 real gap: a conformant tree (one exit-0, one timed-out exit_other) is refused.
    tree = {"entries": 2, "noprefix": 0, "exit2_foreign": 0, "exit0_foreign": 1,
            "exit1_foreign": 0, "exit_other": 1, "norecheck": 0, "restoration_only": 0}
    m04 = load("H04b", mutant_source("H04"))
    out.append("GAP-H04 tree=%s pristine_conform_ok=%r mutant_conform_ok=%r"
               % (tree, base.conform_ok(tree), m04.conform_ok(tree)))
    # H05 real gap: over-accounted counts (buckets 2 > entries 1) are accepted.
    over = {"entries": 1, "noprefix": 0, "exit2_foreign": 0, "exit0_foreign": 1,
            "exit1_foreign": 0, "exit_other": 1, "norecheck": 0, "restoration_only": 0}
    m05 = load("H05b", mutant_source("H05"))
    out.append("GAP-H05 counts=%s pristine_conform_ok=%r mutant_conform_ok=%r"
               % (over, base.conform_ok(over), m05.conform_ok(over)))
    # H10 real gap: main(--verbose) on a prefixed passing entry differs; no selftest calls it.
    root = tempfile.mkdtemp(prefix="probe-fixture-", dir=S)
    kdir = os.path.join(root, "corpus", "knowledge")
    os.makedirs(kdir)
    with open(os.path.join(kdir, "p.md"), "w", encoding="utf-8") as fh:
        fh.write("# fixture\nrecheck: cd %s && true\n" % root)
    tmpd = tempfile.mkdtemp(prefix="probe-tmp-", dir=S)
    os.environ["TMPDIR"] = tmpd
    m10 = load("H10b", mutant_source("H10"))
    argv = ["recheck-cwd-census.py", "--root", root, "--lane", root, "--verbose"]
    import io
    def run(mod):
        buf, real = io.StringIO(), sys.stdout
        sys.stdout = buf
        try:
            ret = mod.main(argv)
        finally:
            sys.stdout = real
        return ret, buf.getvalue()
    rb, ob = run(base)
    rm, om = run(m10)
    out.append("GAP-H10 pristine_ret=%d entries=%d mutant_ret=%d entries=%d pristine_has_ENTRY=%s mutant_has_ENTRY=%s"
               % (rb, ob.count("ENTRY "), rm, om.count("ENTRY "),
                  "ENTRY p.md" in ob, "ENTRY p.md" in om))
    # H10 static: the pristine selftest never passes --verbose to main (no capture(main,...)).
    calls = [ln.strip() for ln in SRC.splitlines() if "capture(main" in ln]
    out.append("GAP-H10 main_calls=%d with_verbose_flag=%d" % (len(calls), sum("--verbose" in c for c in calls)))
    # H19 real gap: H19 + S07M combined still passes the whole selftest.
    combo = SRC.replace(*MUT["H19"], 1).replace(*MUT["S07M"], 1)
    dpath = os.path.join(S, "h19_plus_s07m.py")
    with open(dpath, "w", encoding="utf-8") as fh:
        fh.write(combo)
    env = dict(os.environ, TMPDIR=tempfile.mkdtemp(prefix="probe-combo-", dir=S))
    proc = subprocess.run([sys.executable, "-B", dpath, "--selftest"], env=env,
                          stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600)
    tail = [ln for ln in proc.stdout.splitlines() if ln.startswith("selftest cases=")]
    fails = [ln for ln in proc.stdout.splitlines() if " FAIL" in ln]
    out.append("GAP-H19 combo(H19+main-default-True) rc=%d tail=%r fails=%d"
               % (proc.returncode, tail, len(fails)))
    for ln in out:
        print(ln)
    return 0


if __name__ == "__main__":
    sys.exit(main())
