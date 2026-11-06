#!/usr/bin/env python3
"""Follow-up: (1) multiline-fstring FSTRING_MIDDLE comment hole; (2) corrected dup-extra."""
import importlib.util, json, os, subprocess, sys, shutil

S = "/fast/scratch/hyaku/kasegi-r83/ReviewC1"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
spec = importlib.util.spec_from_file_location("mutbat_r83", LANE + "/.ufo/waves/round-83/c1/mutbat.py")
mb = importlib.util.module_from_spec(spec); spec.loader.exec_module(mb)

print("### P6: comment inside multiline f-string literal (FSTRING_MIDDLE spans lines)")
src = ('import sys\nV = f"""A\nB\nC"""\ndef selftest():\n    assert V == "A\\nB\\nC"\n'
       '    print("selftest cases=1 failures=0")\n    return 0\n'
       'if __name__ == "__main__":\n    sys.exit(selftest())\n')
rows = [{"id": "A-fsmid", "anchor": "B\nC\"\"\"\n", "replacement": "Z\nC\"\"\"\n",
         "class": "assertion", "kill_cases": ["c"]}]
okl = sorted(mb.comment_lines(src))
print("comment_lines:", okl, " (line 3 = 'B', interior f-string literal line)")
rid, d3 = mb.single_decoy(src, rows, "ab")
print("single_decoy nonce=ab ->", rid)
if d3:
    diffline = [ln for ln in d3.splitlines() if "mutbat" in ln]
    print("inserted:", diffline)
    w = os.path.join(S, "w_fsmid"); os.makedirs(w, exist_ok=True)
    tp = os.path.join(w, "fsmid.py")
    open(tp, "w", encoding="utf-8").write(d3)
    p = subprocess.run([sys.executable, "-B", tp, "--selftest"], capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=w), timeout=60, cwd=w)
    print("D3 selftest rc=%d out=%r err=%r" % (
        p.returncode,
        (p.stdout.strip().splitlines() or [""])[-1],
        (p.stderr.strip().splitlines() or [""])[-1][:160]))
    open(os.path.join(S, "d3-fsmid.py"), "w", encoding="utf-8").write(d3)
    shutil.rmtree(w, ignore_errors=True)

print()
print("### P7: comment at end of a multiline plain-string CLOSING line (off-by-one, safe side)")
src2 = ('import sys\nD = """\nabcdef\n"""\ndef selftest():\n    assert D == "\\nabcdef\\n"\n'
        '    print("selftest cases=1 failures=0")\n    return 0\n'
        'if __name__ == "__main__":\n    sys.exit(selftest())\n')
rows2 = [{"id": "A-close", "anchor": '"""\ndef selftest():\n', "replacement": 'X\ndef selftest():\n',
          "class": "assertion", "kill_cases": ["c"]}]
print("comment_lines:", sorted(mb.comment_lines(src2)))
rid2, d32 = mb.single_decoy(src2, rows2, "ab")
print("single_decoy ->", rid2)
if d32:
    w = os.path.join(S, "w_close"); os.makedirs(w, exist_ok=True)
    tp = os.path.join(w, "close.py")
    open(tp, "w", encoding="utf-8").write(d32)
    p = subprocess.run([sys.executable, "-B", tp, "--selftest"], capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=w), timeout=60, cwd=w)
    print("D3 selftest rc=%d out=%r" % (p.returncode, (p.stdout.strip().splitlines() or [""])[-1]))
    shutil.rmtree(w, ignore_errors=True)

print()
print("### P8: corrected duplicate-extra probe")
base = ('import sys\ndef f(x):\n    return x + 1\ndef selftest():\n    assert f(1) == 2\n'
        '    print("selftest cases=1 failures=0")\n    return 0\n'
        'if __name__ == "__main__":\n    sys.exit(selftest())\n')
row = {"id": "E-DUP", "anchor": "    return x + 1\n", "replacement": "    return x + 2\n",
       "class": "assertion", "kill_cases": ["c"],
       "extra": [["assert f(1)", "assert f(1) + assert f(1)"],   # creates a 2nd occurrence
                 ["assert f(1)", "assert f(9)"]]}                # then count=2 -> refuse
out = mb.apply_row(base, row)
print("extra anchor duplicated by a prior extra ->", "None (fail-closed)" if out is None else "DERIVED")
