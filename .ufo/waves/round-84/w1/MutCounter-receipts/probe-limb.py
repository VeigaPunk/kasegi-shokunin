import os, subprocess, sys
S = os.environ["S"]
LIMB = '''        vsrc = ("import sys\\nGOOD = True\\n_fails = 0 if GOOD else 1\\n"
                "print('selftest case=a %s' % ('ok' if GOOD else 'FAIL'))\\n"
                "print('selftest cases=1 failures=%d' % _fails)\\n"
                "sys.exit(1 if _fails else 0)\\n")
        vpath = os.path.join(d, "vtoy.py")
        with open(vpath, "w", encoding="utf-8") as fh:
            fh.write(vsrc)
        vis = [{"id": "T-VIS", "anchor": "GOOD = True\\n", "replacement": "GOOD = False\\n",
                "class": "assertion", "kill_cases": ["a"]},
               {"id": "T-NV", "anchor": "import sys\\n", "replacement": "# n\\nimport sys\\n",
                "class": "neutral"}]
        ok_vis, lines_vis = battery(vpath, vis, 1, d, nonce="00000000000000a1")
        _okn, _ln = battery(toy, good, 2, d, nonce="00000000000000a1")
        _okl, _ll = battery(toy, good, 2, d, legacy=True)
        r84.update({"primary_dup": apply_row("a\\nb\\na\\n", {"anchor": "a\\n",
                    "replacement": "c\\n", "class": "assertion", "kill_cases": ["a"]}) is None,
                    "hidden_src": (not ok_vis) and "decoy_hidden=0/1" in lines_vis[-1],
                    "nonce_field": "nonce=00000000000000a1" in _ln[-2],
                    "legacy_keyed": "keyed=no" in _ll[-2]})
'''
ANCH = "        r84_ok = all(r84.values())\n"
def run(src, tag):
    assert src.count(ANCH) == 1, tag
    path = os.path.join(S, "mut", "probe2-" + tag + ".py")
    open(path, "w", encoding="utf-8").write(src.replace(ANCH, LIMB + ANCH, 1))
    w = os.path.join(S, "mut", "wp2-" + tag); os.makedirs(w, exist_ok=True)
    p = subprocess.run([sys.executable, "-B", path, "--selftest", "--work", w],
                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=w), timeout=900)
    txt = p.stdout + p.stderr
    open(os.path.join(S, "receipts", "probe2-" + tag + ".txt"), "w", encoding="utf-8").write("rc=%d\n%s" % (p.returncode, txt))
    ln = [l for l in txt.splitlines() if l.startswith("mutbat selftest")]
    print(tag, "rc=%d" % p.returncode, "FAIL" if (ln and " selftest FAIL" in ln[0]) else ("ok" if ln else "<no verdict>"))
    if ln and "r84_limbs=" in ln[0]:
        print("    ", ln[0].split("r84_limbs=")[1].split(" bad_tables")[0])
for M in ["PRISTINE", "M01", "M08", "M09", "M10", "M12"]:
    src = open(os.path.join(S, "base" if M == "PRISTINE" else "mut",
                            "mutbat.py" if M == "PRISTINE" else M + ".py"), encoding="utf-8").read()
    run(src, M)
