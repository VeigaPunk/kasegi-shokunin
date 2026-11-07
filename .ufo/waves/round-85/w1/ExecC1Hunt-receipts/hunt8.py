import sys, os, json, subprocess, collections
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S="/fast/scratch/hyaku/kasegi-r85/ExecC1Hunt"
BASE_REV="bc722e540c93b48ff159454b65a0f9f4630db1ed"
def show(p,rev=BASE_REV):
    return subprocess.run(["git","-C",LANE,"show",f"{rev}:{p}"],capture_output=True,text=True).stdout
skill=show("SKILL.md")
lines=skill.splitlines()
# byte-identity check: fixture report.md == exemplar report.md?
import hashlib
def h(p):
    b=subprocess.run(["git","-C",LANE,"cat-file","blob",f"{BASE_REV}:{p}"],capture_output=True).stdout
    return hashlib.sha256(b).hexdigest()[:12]
pex="corpus/instruments/fixtures/claim-package/exemplar"
for name in ("report.md","status.json","provenance.json","claim_checklist.md","custodian-receipts.json","evidence/manifest.json"):
    hs={p for p in subprocess.run(["git","-C",LANE,"ls-tree","-r","--name-only",BASE_REV],capture_output=True,text=True).stdout.splitlines() if os.path.basename(p)==name}
    hashes=collections.Counter(h(p) for p in hs if p.startswith("corpus/instruments/fixtures/"))
    print(name,"fixture copies:",len(hs),"distinct hashes:",len(hashes),"exemplar:",h(pex+"/"+name))
# context lines for ambiguous tokens at base
for tok in ["report.md","status.json","claim_checklist.md","custodian-receipts.json","evidence/manifest.json","provenance.json"]:
    for i,ln in enumerate(lines,1):
        if f"`{tok}`" in ln:
            print(f"L{i} {tok}:",ln[:300])
# 'figure-audit.py' bare token? collect says GONE tokens include bare figure-audit? Check SKILL text for `figure-audit.py`
for i,ln in enumerate(lines,1):
    if "`figure-audit.py`" in ln or "`figure-audit-mutbat.py`" in ln:
        print(f"L{i} BARE:",ln[:400])
# anchored tokens other than lost:
import re
sys.path.insert(0, os.path.join(LANE,"corpus/instruments"))
import resolve as R
for i,ln in enumerate(lines,1):
    for m in R.TOKEN.finditer(ln):
        t=m.group(1).strip().rstrip(".,;:")
        if R.is_pathlike(t):
            b,a=R.strip_anchor(t)
            if a and "[lost" not in t:
                print(f"L{i} ANCH",repr(t),"->",repr(b),a)
# directory-token with existing dir at landed? corpus/instruments/ classify
print(R.classify("python3 corpus/instruments/",LANE,R.MIRROR_ROOT))
print(R.classify("corpus/instruments/",LANE,R.MIRROR_ROOT))
