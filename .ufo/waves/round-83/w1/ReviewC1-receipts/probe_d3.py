#!/usr/bin/env python3
"""ReviewC1 probes: D3 comment insertion edges, keyed-decoy nonce observability, extras."""
import ast, importlib.util, json, os, subprocess, sys, shutil

S = "/fast/scratch/hyaku/kasegi-r83/ReviewC1"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
spec = importlib.util.spec_from_file_location("mutbat_r83", LANE + "/.ufo/waves/round-83/c1/mutbat.py")
mb = importlib.util.module_from_spec(spec); spec.loader.exec_module(mb)
census_src = open(LANE + "/.ufo/waves/round-83/c1/recheck-cwd-census.py", encoding="utf-8").read()
rows = json.load(open(LANE + "/.ufo/waves/round-83/c1/mutant-table.json"))

print("### P1: real-target D3 eligibility (census r83, 67-row table)")
ok_lines = mb.comment_lines(census_src)
cands = []
for r in rows:
    if r["class"] == "neutral" or census_src.count(r["anchor"]) != 1 or "\n" not in r["anchor"]:
        continue
    pos = census_src.index(r["anchor"]) + r["anchor"].index("\n")
    if census_src.count("\n", 0, pos) + 1 in ok_lines:
        cands.append(r["id"])
print("eligible rows (%d): %s" % (len(cands), ",".join(cands)))
for seed in ("0", "00000000000000a1", "deadbeef", "ffffffffffffffff"):
    rid, _ = mb.single_decoy(census_src, rows, seed)
    print("seed %-18s -> d3_row=%s" % (seed, rid))
rid_a, d3_a = mb.single_decoy(census_src, rows, "deadbeef")
rid_b, d3_b = mb.single_decoy(census_src, rows, "deadbeef")
print("determinism deadbeef:", rid_a == rid_b and d3_a == d3_b, "row:", rid_a)
w = os.path.join(S, "w_d3real"); os.makedirs(w, exist_ok=True)
mp = os.path.join(w, "recheck-cwd-census.py")
open(mp, "w", encoding="utf-8").write(d3_a)
p = subprocess.run([sys.executable, "-B", mp, "--selftest"], capture_output=True, text=True,
                   env=dict(os.environ, TMPDIR=w), timeout=600, cwd=w)
last = [ln for ln in p.stdout.splitlines() if ln.startswith("selftest cases=")]
print("D3-on-real-target selftest rc=%d %s" % (p.returncode, last[-1] if last else "?"))
shutil.rmtree(w, ignore_errors=True)

print()
print("### P2: which row's anchor survives D1/D2 unparse (decoy_hidden 63/64)")
d1 = ast.unparse(ast.parse(census_src)) + "\n"
d2 = ast.unparse(mb.rename_locals(ast.parse(census_src))) + "\n"
surv = [r["id"] for r in rows if r["class"] != "neutral"
        and d1.count(r["anchor"]) > 0 and d2.count(r["anchor"]) > 0]
print("anchors surviving BOTH D1 and D2:", surv)

print()
print("### P3: D3 comment-insertion edge cases (toy targets)")
TOYS = {}

TOYS["string1line"] = ('import sys\nS = "a#b"\nX = 1\ndef selftest():\n'
                       '    assert S == "a#b" and X == 1\n    print("selftest cases=1 failures=0")\n'
                       '    return 0\nif __name__ == "__main__":\n    sys.exit(selftest())\n',
                       [("A-str", 'S = "a#b"\nX = 1\n', 'S = "a#b"  # mutated\nX = 1\n'),
                        ("A-plain", 'X = 1\ndef selftest():\n', 'X = 2\ndef selftest():\n')])

TOYS["tripquote"] = ('import sys\nD = """\ndoc\n"""\nX = 1\ndef selftest():\n'
                     '    assert D == "\\ndoc\\n" and X == 1\n    print("selftest cases=1 failures=0")\n'
                     '    return 0\nif __name__ == "__main__":\n    sys.exit(selftest())\n',
                     [("A-tri", 'D = """\ndoc\n"""\nX = 1\n', 'D = 1\nX = 1\n')])

TOYS["backslash"] = ('import sys\nY = 1 + \\\n    2\ndef selftest():\n    assert Y == 3\n'
                     '    print("selftest cases=1 failures=0")\n    return 0\n'
                     'if __name__ == "__main__":\n    sys.exit(selftest())\n',
                     [("A-bs", 'Y = 1 + \\\n    2\ndef selftest():\n', 'Y = 9\ndef selftest():\n')])

TOYS["openbracket"] = ('import sys\ndef f(\n        a):\n    return a + 1\ndef selftest():\n'
                       '    assert f(1) == 2\n    print("selftest cases=1 failures=0")\n'
                       '    return 0\nif __name__ == "__main__":\n    sys.exit(selftest())\n',
                       [("A-br", 'def f(\n        a):\n    return a + 1\n', 'def f(a):\n    return a + 1\n')])

TOYS["fstring_head"] = ('import sys\nV = f"{\n 1 + 1\n}"\ndef selftest():\n    assert V == "2"\n'
                        '    print("selftest cases=1 failures=0")\n    return 0\n'
                        'if __name__ == "__main__":\n    sys.exit(selftest())\n',
                        [("A-fhead", 'V = f"{\n 1 + 1\n}"\n', 'V = "9"\n')])

TOYS["fstring_mid"] = ('import sys\nW = f"{\n 2 + 2\n}"\ndef selftest():\n    assert W == "4"\n'
                       '    print("selftest cases=1 failures=0")\n    return 0\n'
                       'if __name__ == "__main__":\n    sys.exit(selftest())\n',
                       [("A-fmid", ' 2 + 2\n}"\n', ' 2 + 3\n}"\n')])

TOYS["commentline"] = ('import sys\n# lead comment\nZ = 3\ndef selftest():\n    assert Z == 3\n'
                       '    print("selftest cases=1 failures=0")\n    return 0\n'
                       'if __name__ == "__main__":\n    sys.exit(selftest())\n',
                       [("A-com", '# lead comment\nZ = 3\n', '# gone\nZ = 3\n')])

TOYS["crlf"] = ('import sys\r\nQ = (1,\r\n 2)\r\ndef selftest():\r\n    assert Q == (1, 2)\r\n'
                '    print("selftest cases=1 failures=0")\r\n    return 0\r\n'
                'if __name__ == "__main__":\r\n    sys.exit(selftest())\r\n',
                [("A-crlf", 'Q = (1,\r\n 2)\r\n', 'Q = (9,)\r\n')])

for name, (src, arows) in sorted(TOYS.items()):
    trows = [{"id": i, "anchor": a, "replacement": p, "class": "assertion", "kill_cases": [i]}
             for i, a, p in arows]
    okl = sorted(mb.comment_lines(src))
    elig = []
    for i, a, _p in arows:
        if src.count(a) != 1 or "\n" not in a:
            continue
        pos = src.index(a) + a.index("\n")
        ln = src.count("\n", 0, pos) + 1
        elig.append((i, ln, ln in okl))
    rid, d3 = mb.single_decoy(src, trows, "ab")
    print("-- %s ok_lines=%s eligible=%s" % (name, okl, elig))
    print("   single_decoy nonce=ab -> %s" % rid)
    if d3 is None:
        continue
    w = os.path.join(S, "w_toy_" + name); os.makedirs(w, exist_ok=True)
    tp = os.path.join(w, "toy.py")
    open(tp, "w", encoding="utf-8", newline="").write(d3)
    p = subprocess.run([sys.executable, "-B", tp, "--selftest"], capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=w), timeout=120, cwd=w)
    tail = p.stdout.strip().splitlines()[-1:] or ["<no output>"]
    err = p.stderr.strip().splitlines()[-1:] or [""]
    print("   D3 selftest rc=%d out=%r err=%r" % (p.returncode, tail[0], err[0][:160]))
    open(os.path.join(S, "d3-%s.py" % name), "w", encoding="utf-8", newline="").write(d3)
    shutil.rmtree(w, ignore_errors=True)

print()
print("### P4: nonce observability before sys.exit")
obs_src = ('import sys\ndef selftest():\n'
           '    src = open(__file__, encoding="utf-8").read()\n'
           '    print("selftest k_in_globals=%s nonce_in_src=%s" % ("_mutbat_k" in globals(), "_mutbat_k" in src))\n'
           '    print("selftest cases=1 failures=0")\n    return 0\n'
           'if __name__ == "__main__":\n    sys.exit(selftest())\n')
d1o = ast.unparse(ast.parse(obs_src)) + "\n" + "_mutbat_k = 'cafebabe'\n"
w = os.path.join(S, "w_obs"); os.makedirs(w, exist_ok=True)
op = os.path.join(w, "obs.py")
open(op, "w", encoding="utf-8").write(d1o)
p = subprocess.run([sys.executable, "-B", op], capture_output=True, text=True,
                   env=dict(os.environ, TMPDIR=w), timeout=60, cwd=w)
print(p.stdout.strip())
shutil.rmtree(w, ignore_errors=True)

print()
print("### P5: extras semantics via apply_row")
base = ('import sys\ndef f(x):\n    return x + 1\ndef selftest():\n    assert f(1) == 2\n'
        '    print("selftest cases=1 failures=0")\n    return 0\n'
        'if __name__ == "__main__":\n    sys.exit(selftest())\n')
cases = [
    ("extra present once", {"id": "E1", "anchor": "    return x + 1\n",
                            "replacement": "    return x + 2\n", "class": "assertion",
                            "kill_cases": ["c"],
                            "extra": [["def selftest():\n", "def selftest():\n # touched\n"]]}, "derived"),
    ("extra absent (count 0)", {"id": "E2", "anchor": "    return x + 1\n",
                                "replacement": "    return x + 2\n", "class": "assertion",
                                "kill_cases": ["c"],
                                "extra": [["NO SUCH TEXT\n", "x\n"]]}, "None"),
    ("extra duplicated (count 2)", {"id": "E3", "anchor": "    return x + 1\n",
                                    "replacement": "    return x + 2\n", "class": "assertion",
                                    "kill_cases": ["c"],
                                    "extra": [["assert ", "assert "] + []]}, "None"),
    ("extra exists only after primary replacement", {"id": "E4", "anchor": "    return x + 1\n",
                                                     "replacement": "    return x + 2\n",
                                                     "class": "assertion", "kill_cases": ["c"],
                                                     "extra": [["return x + 2\n", "return x + 3\n"]]},
     "derived"),
    ("extra matches primary's original text (gone after replace)",
     {"id": "E5", "anchor": "    return x + 1\n", "replacement": "    return x + 2\n",
      "class": "assertion", "kill_cases": ["c"],
      "extra": [["return x + 1\n", "return x + 9\n"]]}, "None"),
]
for label, row, expect in cases:
    if label.startswith("extra duplicated"):
        row = dict(row, extra=[["assert f(1)", "assert f(1)"], ["assert f(1)", "assert f(9)"]])
    out = mb.apply_row(base, row)
    got = "None" if out is None else "derived"
    print("%-52s -> %-7s (expected %s) %s" % (label, got, expect, "OK" if got == expect else "MISMATCH"))
# battery NOT-DERIVED line for a failing extra: occurrences shows PRIMARY count
w = os.path.join(S, "w_extra"); os.makedirs(w, exist_ok=True)
toy = os.path.join(w, "toy.py")
open(toy, "w", encoding="utf-8").write(base)
badrow = [{"id": "E-MISS", "anchor": "    return x + 1\n", "replacement": "    return x + 2\n",
           "class": "assertion", "kill_cases": ["c"], "extra": [["ABSENT\n", "x\n"]]}]
rf = os.path.join(w, "rows.json")
json.dump(badrow, open(rf, "w"))
p = subprocess.run([sys.executable, "-B", LANE + "/.ufo/waves/round-83/c1/mutbat.py",
                    "--target", toy, "--table", rf, "--expect-cases", "1", "--work", w],
                   capture_output=True, text=True, env=dict(os.environ, TMPDIR=w), timeout=300)
print("battery with missing extra: rc=%d" % p.returncode)
for ln in p.stdout.splitlines():
    print("  " + ln)
shutil.rmtree(w, ignore_errors=True)
