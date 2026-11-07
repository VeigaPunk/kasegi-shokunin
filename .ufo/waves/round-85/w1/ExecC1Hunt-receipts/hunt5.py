import sys, os, json, subprocess, collections, re
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments")
import resolve as R
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S="/fast/scratch/hyaku/kasegi-r85/ExecC1Hunt"
MIRROR=R.MIRROR_ROOT
BASE_REV="bc722e540c93b48ff159454b65a0f9f4630db1ed"
base_files=subprocess.run(["git","-C",LANE,"ls-tree","-r","--name-only",BASE_REV],capture_output=True,text=True).stdout.splitlines()
trk=[p for p in base_files if not p.startswith(".ufo/")]
byb=collections.defaultdict(list)
for p in trk: byb[os.path.basename(p)].append(p)
uniq={b:v[0] for b,v in byb.items() if len(v)==1}

def scan(files):
    cites={}
    for f in files:
        path=os.path.join(LANE,f)
        for ln in open(path,encoding="utf-8",errors="replace"):
            for m in R.TOKEN.finditer(ln):
                t=m.group(1).strip().rstrip(".,;:")
                if not R.is_pathlike(t): continue
                cites.setdefault(t,set()).add(f)
    return cites

# knowledge top-level *.md per spec: corpus/knowledge/*.md (not subdirs). Also report corpus/knowledge/**/*.md excluding lessons? spec says count over corpus/knowledge/*.md (not lessons: lessons are history). *.md top-level excludes subdirs; lessons is at corpus/lessons, not under knowledge. We'll compute both.
k_top=sorted(p for p in trk if re.fullmatch(r"corpus/knowledge/[^/]+\.md",p))
k_all=sorted(p for p in trk if p.startswith("corpus/knowledge/") and p.endswith(".md"))
for label,files in (("knowledge/*.md",k_top),("knowledge/**/*.md",k_all)):
    cites=scan(files)
    gone=[t for t in sorted(cites) if R.classify(t,LANE,MIRROR)[0]=="GONE"]
    uniqhits=[]
    for t in gone:
        b,_=R.strip_anchor(t)
        bn=os.path.basename(b)
        if bn in uniq:
            uniqhits.append({"token":t,"files":sorted(cites[t]),"proposed":uniq[bn]})
    print(label,"files",len(files),"distinct tokens",len(cites),"GONE",len(gone),
          "nonGONE",len(cites)-len(gone),"UNIQUE_BASENAME",len(uniqhits))
    # counts also for frozen-18-like keys present?
    frozen=json.load(open(os.path.join(LANE,".ufo/waves/round-85/c1/repair-map.json")))
    in_frozen=[u for u in uniqhits if u["token"] in frozen]
    print("  of those, frozen-map keys:",len(in_frozen))
    for u in uniqhits[:80]:
        print("   ",repr(u["token"]),u["files"],"->",u["proposed"])
    json.dump({"files":files,"cites":{k:sorted(v) for k,v in cites.items()},"uniq":uniqhits},open(os.path.join(S,f"knowledge_{label.replace('/','_').replace('*','').replace('.','_')}.json"),"w"),indent=1)
