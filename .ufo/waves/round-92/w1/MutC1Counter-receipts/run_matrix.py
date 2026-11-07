import concurrent.futures, json, os, subprocess, sys, time
S = "/fast/scratch/hyaku/kasegi-r92/MutC1Counter"
L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BASE = "0628fd247914555838a42c02ba5d4ac08b7e095d"
LANDING = "cb1ef2b9856df79c530f3ff1374fa9691ff56233"
LABELS = "d0bd4758a41919b2c86c079f3a1a2dfb392dcd8d"
MAPSHA = "6d87cafaec99961a15c00967d30c2bb164ed480d8b3fbaeadccd55b048d9b772"
FROZEN_MAP = L + "/.ufo/waves/round-92/c1/repair-map.tsv"

def contexts():
    out = [("landing", L, LANDING, FROZEN_MAP)]
    for ln in open(S + "/variants.tsv", encoding="utf-8"):
        name, rev, mp = ln.rstrip("\n").split("\t")
        out.append((name, S + "/c1clone", rev, mp))
    return out

CTX = contexts()

def run(job):
    tag, script, lane, after, mp = job
    work = S + "/work/" + tag
    os.makedirs(work, exist_ok=True)
    cmd = [sys.executable, "-B", script, "--lane", lane, "--base-rev", BASE,
           "--after-rev", after, "--map", mp, "--labels-rev", LABELS,
           "--base-target", "947/1947", "--target", "960/1944",
           "--map-sha256", MAPSHA, "--work", work]
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    dt = time.time() - t0
    lines = [x for x in (r.stdout + r.stderr).splitlines() if x.strip()]
    res = next((x for x in reversed(lines) if x.startswith("KNOWLEDGE-METER-RESULT")), "NO-RESULT")
    log = S + "/out/" + tag + ".log"
    with open(log, "w", encoding="utf-8") as fh:
        fh.write(r.stdout)
        if r.stderr:
            fh.write("\n---stderr---\n" + r.stderr)
    return tag, res, dt

def matrix(script, group, workers=None):
    jobs = [(group + "__" + name, script, lane, after, mp) for name, lane, after, mp in CTX]
    out = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        for tag, res, dt in ex.map(run, jobs):
            out[tag.split("__", 1)[1]] = res
    return out

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "baseline":
        m = matrix(S + "/W/c1/knowledge-meter.py", "pristine", 8)
        json.dump(m, open(S + "/baseline.json", "w"), indent=1, sort_keys=True)
        for k, v in m.items():
            print("%-28s %s" % (k, v))
    elif mode == "all":
        names = open(S + "/mut/index.txt").read().split()
        results = {}
        for i, name in enumerate(names):
            t0 = time.time()
            results[name] = matrix(S + "/mut/%s.py" % name, name, int(sys.argv[2]) if len(sys.argv) > 2 else 16)
            print("%s %.1fs" % (name, time.time() - t0), flush=True)
            json.dump(results, open(S + "/results.json", "w"), indent=1, sort_keys=True)
        print("done", len(results))
