import importlib.util, os, re, shutil, subprocess, sys
S="/fast/scratch/hyaku/kasegi-r46/R46bMutF29a"
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
CTRL=os.path.join(LANE,".ufo/waves/round-46/attempt2/controls")
GATE=os.path.join(LANE,"corpus/instruments/r46-f29-gate.py")
spec=importlib.util.spec_from_file_location("f29fix", os.path.join(CTRL,"f29-fixture.py"))
fx=importlib.util.module_from_spec(spec); spec.loader.exec_module(fx)
ENTRY,URL,LANE_CD=fx.ENTRY,fx.URL,fx.LANE_CD
TREES=os.path.join(S,"trees"); INST=os.path.join(S,"inst")
env=dict(os.environ, TMPDIR=os.path.join(S,"tmp"))
def fresh(n):
    d=os.path.join(TREES,n)
    if os.path.isdir(d): shutil.rmtree(d)
    shutil.copytree(os.path.join(TREES,"positive"), d, symlinks=True); return d
def full(g,t):
    p=subprocess.run([sys.executable,"-B",g,"--root",t],capture_output=True,text=True,env=env,timeout=300)
    return p.stdout
def show(title,tree,mid,limb):
    print("### "+title)
    b=full(GATE,tree); m=full(os.path.join(INST,mid,"corpus/instruments/r46-f29-gate.py"),tree)
    for lbl,o in (("BASE  ",b),("MUTANT",m)):
        print("  "+lbl+" "+" | ".join(x.strip() for x in o.strip().splitlines()))
    bl=re.search(r"^gate %s pass=(\d)"%limb,b,re.M); ml=re.search(r"^gate %s pass=(\d)"%limb,m,re.M)
    print("  => %s limb %s: base=%s mutant=%s  %s\n"%(limb,limb,bl.group(1),ml.group(1),
        "FLIP (isolated)" if bl.group(1)!=ml.group(1) else "no-flip"))

# P7: gut ONLY the Limits section (table stays put inside Scope) -> cleanest H2b isolation
d=fresh("probe-p7")
p=os.path.join(d,"corpus/knowledge/github-repository-security-advisories.md")
t=open(p,encoding="utf-8").read()
old=re.search(r"## Limits\n\n(.*?)\n\n## Falsifiable package rule", t, re.S).group(1)
new=("Limits: the overview page only; the editing flow and the REST API live on sibling "
     "pages this row does not hold (S074.txt:19).")
open(p,"w",encoding="utf-8").write(t.replace(old,new))
show("P7 disclosure (b)/H2b: the ## Limits section body replaced by one 17-word line (table untouched, all other sections untouched)",
     d,"H2b-wordfloor-low","H2")
print("  Limits section words:", len(re.findall(r"\w+", new)))
