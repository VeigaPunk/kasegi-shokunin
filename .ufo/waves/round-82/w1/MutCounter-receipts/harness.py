import json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

S = "/fast/scratch/hyaku/kasegi-r82/MutCounter"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
CAND = os.path.join(LANE, "corpus/instruments/recheck-cwd-census.py")
TABLE = os.path.join(LANE, ".ufo/waves/round-82/c1/mutant-table.json")
DRIVER = os.path.join(S, "ctrl/driver.py")
BASE = os.path.join(S, "m/base.py")

def run(args, work, env_extra=None):
    os.makedirs(work, exist_ok=True)
    env = dict(os.environ); env["TMPDIR"] = work; env.update(env_extra or {})
    t0 = time.time()
    p = subprocess.run(args, capture_output=True, text=True, cwd=S, env=env, timeout=1800)
    return p.returncode, p.stdout + p.stderr, round(time.time() - t0, 1)

def one(cid, counter):
    root = os.path.join(S, "runs", cid)
    os.makedirs(root, exist_ok=True)
    with open(os.path.join(root, "counter.sha256"), "w") as fh:
        fh.write(subprocess.run(["sha256sum", counter], capture_output=True, text=True).stdout)
    rc1, out1, t1 = run([sys.executable, "-B", counter, "--selftest", "--work", root + "/st"], root + "/st")
    open(root + "/selftest.txt", "w").write("rc=%d time=%ss\n%s" % (rc1, t1, out1))
    rc3, out3, t3 = run([sys.executable, "-B", counter, "--target", CAND, "--table", TABLE,
                         "--expect-cases", "24", "--work", root + "/p3"], root + "/p3")
    open(root + "/p3.txt", "w").write("rc=%d time=%ss\n%s" % (rc3, t3, out3))
    rc2, out2, t2 = run([sys.executable, "-B", DRIVER, "--lane", LANE, "--work", root + "/fg"],
                        root + "/fg", {"MUT_COUNTER": counter})
    open(root + "/driver.txt", "w").write("rc=%d time=%ss\n%s" % (rc2, t2, out2))
    p3sum = [l for l in out3.splitlines() if l.startswith("MUTBAT")]
    forg = {}
    for l in out2.splitlines():
        if l.startswith("FORGERY"):
            m = re.match(r"FORGERY (\S+) counter=(\S+) .*? rc=(\d+)", l)
            if m:
                forg["%s/%s" % (m.group(1), m.group(2))] = int(m.group(3))
    return {"id": cid, "counter": counter,
            "counter_sha256": open(os.path.join(root, "counter.sha256")).read().split()[0],
            "selftest_rc": rc1, "selftest_out": out1.strip().splitlines()[-1:] ,
            "selftest_secs": t1,
            "p3_rc": rc3, "p3_summary": p3sum[-1] if p3sum else None, "p3_secs": t3,
            "driver_rc": rc2, "forgery_rc": forg, "driver_secs": t2}

ids = ["MC00"] + [m["id"] for m in json.load(open(os.path.join(S, "m/manifest.json")))]
counters = {"MC00": BASE}
for m in json.load(open(os.path.join(S, "m/manifest.json"))):
    counters[m["id"]] = os.path.join(S, "m/mutants", m["id"] + ".py")
t0 = time.time()
with ThreadPoolExecutor(max_workers=5) as ex:
    res = list(ex.map(lambda cid: one(cid, counters[cid]), ids))
json.dump(res, open(os.path.join(S, "results.json"), "w"), indent=1)
print("total_secs=%.0f" % (time.time() - t0))
for r in res:
    print("%s rc_st=%s p3rc=%s drv=%s forg=%s | %s" % (
        r["id"], r["selftest_rc"], r["p3_rc"], r["driver_rc"],
        json.dumps(r["forgery_rc"], sort_keys=True), (r["p3_summary"] or "NO-P3-SUMMARY")[-120:]))
