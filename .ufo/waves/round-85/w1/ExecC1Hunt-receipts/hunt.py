import sys, os, json, subprocess, collections
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments")
import resolve as R
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
MIRROR=R.MIRROR_ROOT
tracked=subprocess.run(["git","-C",LANE,"ls-files"],capture_output=True,text=True).stdout.splitlines()
by_base=collections.defaultdict(list)
for p in tracked: by_base[os.path.basename(p)].append(p)
by_base_nonufo=collections.defaultdict(list)
for p in tracked:
    if not p.startswith(".ufo/"): by_base_nonufo[os.path.basename(p)].append(p)
S="/fast/scratch/hyaku/kasegi-r85/ExecC1Hunt"
scdir=os.path.join(S,"scope"); os.makedirs(scdir,exist_ok=True)
import shutil
shutil.copy(os.path.join(LANE,"SKILL.md"), os.path.join(scdir,"SKILL.md"))
repo,cites=R.collect(scdir)
print(f"SKILL tokens: {len(cites)}")
gone=[t for t in sorted(cites) if R.classify(t,LANE,MIRROR)[0]=="GONE"]
print(f"GONE: {len(gone)} nonGONE: {len(cites)-len(gone)}")
skill_lines=open(os.path.join(LANE,"SKILL.md"),encoding="utf-8").read().splitlines()
def token_lines(tok):
    out=[]
    for i,ln in enumerate(skill_lines,1):
        for m in R.TOKEN.finditer(ln):
            if m.group(1).strip().rstrip(".,;:")==tok:
                out.append(i); break
    return out
frozen=json.load(open(os.path.join(LANE,".ufo/waves/round-85/c1/repair-map.json")))
results=[]
for tok in gone:
    base,anchor=R.strip_anchor(tok)
    bn=os.path.basename(base)
    lines=token_lines(tok)
    ctx=[skill_lines[i-1][:600] for i in lines[:4]]
    results.append({"token":tok,"base":base,"anchor":anchor,"lines":lines,"ctx":ctx,
      "basename":bn,"cands_nonufo":sorted(by_base_nonufo.get(bn,[])),"cands_all":sorted(by_base.get(bn,[])),
      "frozen":tok in frozen,"frozen_val":frozen.get(tok)})
def cat(e):
    if e["frozen"]: return "FROZEN18"
    if "[lost" in e["token"] or "[lost" in e["base"]: return "LOST_MARKER"
    c=e["cands_nonufo"]
    if len(c)==1: return "UNIQUE_NONFROZEN"
    if len(c)>=2: return "AMBIGUOUS"
    if len(c)==0 and len(e["cands_all"])>=1: return "ONLY_UFO"
    if len(c)==0: return "NO_MATCH"
    return "OTHER"
from collections import Counter
print(Counter(cat(e) for e in results))
open(os.path.join(S,"gone.json"),"w").write(json.dumps(results,indent=1))
for e in results:
    c=cat(e)
    if c in ("NO_MATCH","AMBIGUOUS","LOST_MARKER","UNIQUE_NONFROZEN","ONLY_UFO"):
        print(c,"|",repr(e["token"]),"| lines",e["lines"],"| cands",e["cands_nonufo"],"| all",e["cands_all"])
        for x in e["ctx"]: print("    CTX:",x[:300])
