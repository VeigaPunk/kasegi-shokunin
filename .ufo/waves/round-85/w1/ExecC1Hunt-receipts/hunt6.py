import sys, os, json, subprocess, collections
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S="/fast/scratch/hyaku/kasegi-r85/ExecC1Hunt"
BASE_REV="bc722e540c93b48ff159454b65a0f9f4630db1ed"
def blob(rev,p):
    r=subprocess.run(["git","-C",LANE,"cat-file","blob",f"{rev}:{p}"],capture_output=True)
    return r.stdout if r.returncode==0 else None
# 1) SKILL frozen keys exist at base? and proposed classify INTERNAL?
sys.path.insert(0, os.path.join(LANE,"corpus/instruments"))
import resolve as R
frozen=json.load(open(os.path.join(LANE,".ufo/waves/round-85/c1/repair-map.json")))
base_skill=blob(BASE_REV,"SKILL.md").decode()
scdir=os.path.join(S,"scope2")
# scope2 already has base SKILL
repo,cites=R.collect(scdir)
for k,v in sorted(frozen.items()):
    cls=R.classify(k,LANE,R.MIRROR_ROOT)
    cls2=R.classify(v,LANE,R.MIRROR_ROOT)
    print("FROZEN",repr(k),"GONE?",cls[0],"->",repr(v),"class",cls2[0],"exists",os.path.exists(os.path.join(LANE,v)))
# 2) working SKILL vs base: diff?
work=open(os.path.join(LANE,"SKILL.md"),encoding="utf-8").read()
print("work SKILL == base SKILL?", work==base_skill)
# diff line count
import difflib
d=list(difflib.unified_diff(base_skill.splitlines(),work.splitlines(),lineterm=""))
print("diff lines:",len(d))
for x in d[:40]: print(x[:220])
# 3) figure-audit-mutbat token occurrences in base SKILL (why GONE?)
for i,ln in enumerate(base_skill.splitlines(),1):
    if "figure-audit-mutbat" in ln: print("base L"+str(i),ln[:400])
    if "sha256sum corpus/instruments/r-defect" in ln: print("base L"+str(i),ln[:400])
    if "python3 corpus/instruments/figure-audit.py" in ln: print("base L"+str(i),ln[:400])
    if "anchorcheck.py" in ln and "python3" in ln: print("base L"+str(i),ln[:400])
# classify figure-audit tokens
for t in ["python3 corpus/instruments/figure-audit-mutbat.py","python3 corpus/instruments/figure-audit.py","figure-audit-mutbat.py","figure-audit.py"]:
    if t in cites: print("cited",repr(t),R.classify(t,LANE,R.MIRROR_ROOT))
print("figure-audit.py exists?",os.path.exists(os.path.join(LANE,"corpus/instruments/figure-audit.py")))
print("git ls figure:",subprocess.run(["git","-C",LANE,"ls-files","corpus/instruments/figure-audit*"],capture_output=True,text=True).stdout)
print("git log figure:",subprocess.run(["git","-C",LANE,"log","--oneline","-3","--","corpus/instruments/figure-audit.py"],capture_output=True,text=True).stdout)
# SKILL token figure-audit bare occurrences
for i,ln in enumerate(base_skill.splitlines(),1):
    if "`figure-audit" in ln or "`python3 corpus/instruments/figure" in ln: print("L"+str(i),ln[:500])
