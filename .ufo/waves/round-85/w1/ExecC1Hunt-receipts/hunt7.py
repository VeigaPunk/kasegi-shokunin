import sys, os, json, subprocess, collections
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments")
import resolve as R
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S="/fast/scratch/hyaku/kasegi-r85/ExecC1Hunt"
MIRROR=R.MIRROR_ROOT
def lines_of(tok,lines):
    out=[]
    for i,ln in enumerate(lines,1):
        for m in R.TOKEN.finditer(ln):
            if m.group(1).strip().rstrip(".,;:")==tok: out.append(i); break
    return out
frozen=json.load(open(os.path.join(LANE,".ufo/waves/round-85/c1/repair-map.json")))
hunt2=json.load(open(os.path.join(S,"hunt2.json")))
# candidates at base (tokens gone at BASE). Now check which remain GONE/present at LANDING.
# Rule B tokens: after the 18-map, most invoked instruments also appear BARE, so map value path already resolves; counts only if rewrite turns GONE->INTERNAL.
# Compute: parse landed SKILL lines for each Rule-B token; propose value; check classify(value)==INTERNAL.
landed_lines=open(os.path.join(S,"land_SKILL.md"),encoding="utf-8").read().splitlines()
scdir=os.path.join(S,"scopeL"); os.makedirs(scdir,exist_ok=True)
open(os.path.join(scdir,"SKILL.md"),"w").write("\n".join(landed_lines)+"\n")
repo,cites=R.collect(scdir)
print("landed distinct tokens:",len(cites),"GONE:",sum(1 for t in cites if R.classify(t,LANE,MIRROR)[0]=="GONE"),
      "nonGONE:",sum(1 for t in cites if R.classify(t,LANE,MIRROR)[0]!="GONE"))
bark=json.load(open(os.path.join(S,"hunt2.json")))
for c in bark["candidates"]:
    tok=c["token"]; val=c["proposed"]
    cls=R.classify(val,LANE,MIRROR)[0]
    # occurrences at base vs landed of the VALUE as a token
    print(c["rule"],repr(tok)[:80],"->",val,cls,"| landed value-cited?",val in cites)
# Which Rule-B tokens disappear at landing because nothing changed in text (still present)?
base_lines=open(os.path.join(S,"base_SKILL.md"),encoding="utf-8").read().splitlines()
stills=[]
for c in bark["candidates"]:
    if c["token"] in cites and R.classify(c["token"],LANE,MIRROR)[0]=="GONE":
        stills.append(c)
print("RuleB still GONE at landing:",len(stills))
# distinct proposed values among them
from collections import Counter
print(Counter(c["proposed"] for c in stills))
# verify each standing Rule-B candidate's proposed value classifies INTERNAL and differs from any existing token on same lines (no collision with an existing backticked token that is a different distinct token... it would COLLAPSE counts)
for c in stills:
    tok,val=c["token"],c["proposed"]
    # lines at base containing tok; on those lines, is val already a token?
    blines=set(lines_of(tok,base_lines))
    present_val_on_line=any(val in [m.group(1).strip().rstrip(".,;:") for m in R.TOKEN.finditer(base_lines[l-1])] for l in blines)
    print(repr(tok)[:70],"->",val,"| value already token on same line:",present_val_on_line)
