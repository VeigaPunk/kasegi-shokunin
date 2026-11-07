#!/usr/bin/env python3
"""deleted-target control: pos tree, target snapshot deleted from the worktree
(still tracked) -> M1+M4+M5 fail; assertion on LIMB M4 FAIL isolates the
classify-INTERNAL clause for mutants that drop it."""
import json, os, shutil, subprocess, hashlib
S = "/fast/scratch/hyaku/kasegi-r86/MutC1Counter"
L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
B = "d7296645c2cd9f631329fa8e2f38328a4c9c89a5"
MAP = L + "/.ufo/waves/round-86/c1/repair-map.json"
def sh(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: raise SystemExit("FAIL %s %s" % (c, r.stderr))
    return r.stdout
def sha(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()
def app(root, mp):
    m = json.load(open(mp)); d = os.path.join(root,"corpus","knowledge")
    for fn in sorted(os.listdir(d)):
        p = os.path.join(d,fn)
        if not (fn.endswith(".md") and os.path.isfile(p)): continue
        t = open(p, encoding="utf-8").read(); out=[]
        for line in t.split("\n"):
            for k,v in m.items():
                if "`%s`" % k in line: line = line.replace("`%s`" % k, "`%s`" % v)
            out.append(line)
        nt = "\n".join(out)
        if nt != t: open(p,"w",encoding="utf-8").write(nt)
cfg = json.load(open(S+"/controls.json"))
if any(c["name"]=="deleted-target" for c in cfg["controls"]):
    print("present"); raise SystemExit(0)
t = os.path.join(S,"trees","deleted-target")
if os.path.isdir(t): shutil.rmtree(t)
sh(["git","clone","-q","--shared",L,t]); sh(["git","-C",t,"checkout","-q",B])
app(t, MAP)
os.remove(os.path.join(t,"corpus","source-snapshots","round-45","S071.txt"))
print("tracked still:", "corpus/source-snapshots/round-45/S071.txt" in sh(["git","-C",t,"ls-files","corpus/source-snapshots/round-45/S071.txt"]))
cfg["controls"].append({"name":"deleted-target","tree":t,"map":MAP,"target":"596/1716",
                        "sha":sha(MAP),"expect":"pass","assert_stdout":"LIMB M4 FAIL",
                        "expect_present":True})
json.dump(cfg, open(S+"/controls.json","w"), indent=1)
print("controls=%d" % len(cfg["controls"]))
