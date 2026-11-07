import sys, os, json, subprocess, collections
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S="/fast/scratch/hyaku/kasegi-r85/ExecC1Hunt"
BASE_REV="bc722e540c93b48ff159454b65a0f9f4630db1ed"
sys.path.insert(0, os.path.join(LANE,"corpus/instruments"))
import resolve as R
def show(p,rev=BASE_REV): return subprocess.run(["git","-C",LANE,"show",f"{rev}:{p}"],capture_output=True,text=True).stdout
skill_lines=show("SKILL.md").splitlines()
def lines_of(tok):
    out=[]
    for i,ln in enumerate(skill_lines,1):
        for m in R.TOKEN.finditer(ln):
            if m.group(1).strip().rstrip(".,;:")==tok: out.append(i); break
    return out
scdir=os.path.join(S,"scope2"); repo,cites=R.collect(scdir)
for t in ["figure-audit.py","figure-audit-mutbat.py","figure-audit-ledger.json"]:
    print(t, t in cites, R.classify(t,LANE,R.MIRROR_ROOT) if t in cites else "-", lines_of(t))
# tokens for each of our three bare stems - verify base collect had them as GONE? (hunt2 said candidates only command forms)
gone=[t for t in cites if R.classify(t,LANE,R.MIRROR_ROOT)[0]=="GONE"]
print("bare figure tokens in gone:",[t for t in gone if "figure" in t])
print("bare anchorcheck:",[t for t in gone if "anchorcheck" in t])
# line anchors to non-corpus files resolvable after anchor strip only?
for tok in sorted(gone):
    b,a=R.strip_anchor(tok)
    if a and not tok.startswith("["):
        print(repr(tok),a,"->",R.classify(b,LANE,R.MIRROR_ROOT))
# corpus/knowledge count detail: verify rule counts with strip_anchor? my uniq used basename(strip_anchor)
# Also check 'python3 corpus/instruments/' dir token proposed value INTERNAL and token line 1228 context
for i in (1228,1227):
    print(i,skill_lines[i-1][:400])
# For contract-style tokens in SKILL (lines 549-556), show full sentences for why generic
for i in (549,550,551,552,553,554):
    print(i,skill_lines[i-1][:500])
