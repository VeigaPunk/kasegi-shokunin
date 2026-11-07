import hashlib, os, subprocess, sys, json
S = os.environ["S"]
BASE = os.path.join(S, "base", "mutbat.py")
src = open(BASE, encoding="utf-8").read()
M = [
 ("M01", '    if src.count(row["anchor"]) != 1:\n        return None\n',
         '    if src.count(row["anchor"]) == 0:\n        return None\n',
  "apply_row primary uniqueness !=1 -> ==0 (duplicate primary anchor allowed)"),
 ("M02", '    out = src.replace(row["anchor"], row["replacement"], 1)\n',
         '    out = src\n',
  "apply_row primary site never applied (identity primary)"),
 ("M03", '        if out.count(anchor) != 1:\n            return None\n',
         '        if out.count(anchor) == 0:\n            return None\n',
  "apply_row extra uniqueness !=1 -> ==0"),
 ("M04", '    for anchor, repl in row.get("extra", []):\n',
         '    for anchor, repl in ():\n',
  "apply_row extra loop never runs (extra sites ignored)"),
 ("M05", '        counts = v == "KILLED" or (v == "EXCEPTION-KILL" and row["class"] == "exception")\n',
         '        counts = v == "KILLED"\n',
  "battery: EXCEPTION-KILL on an exception-class row no longer counts"),
 ("M06", '            tally["killed"] += 1\n',
         '            tally["survived"] += 1\n',
  "battery tally: killed counter increments survived"),
 ("M07", '                 % (sha, "ok" if baseline else "bad", len(rows), tally["killed"],\n',
         '                 % (sha, "ok" if baseline else "bad", len(rows), tally["survived"],\n',
  "MUTBAT summary line prints survived where killed is expected"),
 ("M08", '                 and (decoy_src is None or any(d.count(r["anchor"]) == 0 for d in decoy_src[:2])))\n',
         '                 and (decoy_src is None or any(d.count(r["anchor"]) == 0 for d in decoy_src)))\n',
  "battery hidden count includes the D3 decoy (slice [:2] -> all)"),
 ("M09", '          and tally["neutral_ok"] == n_neutral and decoy_ok and hidden >= 1)\n',
         '          and tally["neutral_ok"] == n_neutral and decoy_ok and hidden >= 0)\n',
  "battery ok: decoy_hidden>=1 -> >=0"),
 ("M10", '                 % ("no" if legacy else "yes", nonce or "-", d3_id or "-"))\n',
         '                 % ("no" if legacy else "yes", "-", d3_id or "-"))\n',
  "DECOY line nonce field always '-'"),
 ("M11", '        decoys.append(d3)\n',
         '        pass\n',
  "run_decoy: D3 single-decoy never appended"),
 ("M12", '                 % ("no" if legacy else "yes", nonce or "-", d3_id or "-"))\n',
         '                 % ("yes", nonce or "-", d3_id or "-"))\n',
  "DECOY line keyed label always 'yes' (legacy misreported)"),
 ("M13", '        r84_ok = all(r84.values())\n',
         '        r84_ok = True\n',
  "r84_limbs assertions replaced by constant True"),
 ("M14", '        return 0 if okk else 1\n',
         '        return 1\n',
  "selftest exit code forced to 1 (verdict line unchanged)"),
 ("M15", '    ok = (baseline and n_kill > 0 and n_neutral > 0 and tally["killed"] == n_kill\n',
         '    ok = (baseline and n_kill > 0 and n_neutral > 0 and tally["killed"] >= 0\n',
  "battery ok: killed==n_kill -> killed>=0"),
]
out = []
for mid, anchor, repl, desc in M:
    n = src.count(anchor)
    assert n == 1, (mid, n)
    path = os.path.join(S, "mut", mid + ".py")
    open(path, "w", encoding="utf-8").write(src.replace(anchor, repl, 1))
    w = os.path.join(S, "mut", "w-" + mid); os.makedirs(w, exist_ok=True)
    env = dict(os.environ, TMPDIR=w)
    p = subprocess.run([sys.executable, "-B", path, "--selftest", "--work", w],
                       capture_output=True, text=True, env=env, timeout=900)
    txt = p.stdout + p.stderr
    open(os.path.join(S, "receipts", mid + "-selftest.txt"), "w", encoding="utf-8").write("rc=%d\n%s" % (p.returncode, txt))
    first = [l for l in txt.splitlines() if l.startswith("mutbat selftest")] or [txt.strip().splitlines()[-1] if txt.strip() else "<empty>"]
    print("%s rc=%d %s | %s" % (mid, p.returncode, first[0][:160], desc))
    out.append({"id": mid, "rc": p.returncode, "desc": desc, "sha": hashlib.sha256(open(path,"rb").read()).hexdigest(),
                "line": first[0]})
json.dump(out, open(os.path.join(S, "receipts", "mutants.json"), "w"), indent=1)
