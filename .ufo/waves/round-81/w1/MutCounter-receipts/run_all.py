#!/usr/bin/env python3
"""Run (a) own selftest, (b) forgery driver, (c) real 59-row battery for each mutbat mutant."""
import concurrent.futures as cf
import json
import os
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
C1 = os.path.join(LANE, ".ufo/waves/round-81/c1")
TARGET = os.path.join(C1, "recheck-cwd-census.py")
TABLE = os.path.join(C1, "mutant-table.json")
DRIVER = os.path.join(S, "forgeries-mutant.py")


def run(cmd, cwd, env_work=None, timeout=1800):
    env = dict(os.environ)
    env["TMPDIR"] = env_work or S
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=env, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def selftest(mid, path):
    wd = os.path.join(S, "run", "st-" + mid)
    os.makedirs(wd, exist_ok=True)
    rc, out, err = run([sys.executable, "-B", path, "--selftest", "--work", wd], S, wd)
    line = [l for l in (out + err).splitlines() if l.startswith("mutbat selftest")]
    return {"id": mid, "rc": rc, "line": line[-1] if line else "NO-LINE", "tail": err[-300:]}


def forgery(mid, path):
    wd = os.path.join(S, "fg", mid)
    os.makedirs(wd, exist_ok=True)
    rc, out, err = run([sys.executable, "-B", DRIVER, "--lane", LANE, "--work", wd,
                        "--mutbat", path], S, wd)
    rows = []
    for l in out.splitlines():
        if l.startswith("FORGERY"):
            parts = l.split()
            d = {"name": parts[1], "rc": int(parts[4].split("=")[1]),
                 "verdicts": parts[5].split("=", 1)[1] if "verdicts=" in l else "?",
                 "summary": l.split("MUTBAT ", 1)[1] if "MUTBAT " in l else ""}
            rows.append(d)
    return {"id": mid, "rc": rc, "forgeries": rows, "stderr": err[-200:]}


def realbattery(mid, path):
    wd = os.path.join(S, "run", "real-" + mid)
    os.makedirs(wd, exist_ok=True)
    rc, out, err = run([sys.executable, "-B", path, "--target", TARGET, "--table", TABLE,
                        "--expect-cases", "22", "--work", wd], S, wd)
    line = [l for l in out.splitlines() if l.startswith("MUTBAT")]
    verd = {}
    for l in out.splitlines():
        if l.startswith("MUTANT"):
            v = l.split()[2].split("=", 1)[1]
            verd[v] = verd.get(v, 0) + 1
    return {"id": mid, "rc": rc, "summary": line[-1] if line else "NO-SUMMARY",
            "verdicts": verd, "stderr": err[-200:]}


def main():
    muts = [r for r in json.load(open(os.path.join(S, "mutants.json"))) if r["status"] == "derived"]
    muts.insert(0, {"id": "PRISTINE", "path": os.path.join(S, "mutbat-pristine.py")})
    res = {}

    def st(m):
        return selftest(m["id"], m["path"])

    with cf.ThreadPoolExecutor(max_workers=16) as ex:
        for r in ex.map(st, muts):
            res.setdefault(r["id"], {})["selftest"] = r
            print("SELFTEST %-28s rc=%d %s" % (r["id"], r["rc"], r["line"][:90]), flush=True)

    alive = [m for m in muts if res[m["id"]]["selftest"]["rc"] == 0]
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(lambda m: forgery(m["id"], m["path"]), muts):
            res[r["id"]]["forgery"] = r
            print("FORGERY  %-28s rcs=%s" % (r["id"], [f["rc"] for f in r["forgeries"]]), flush=True)

    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for r in ex.map(lambda m: realbattery(m["id"], m["path"]), alive):
            res[r["id"]]["real"] = r
            print("REALBAT  %-28s rc=%d %s" % (r["id"], r["rc"], r["summary"][:120]), flush=True)

    json.dump(res, open(os.path.join(S, "results.json"), "w"), indent=1)
    print("alive_after_own_selftest", [m["id"] for m in alive])
    return 0


if __name__ == "__main__":
    sys.exit(main())
