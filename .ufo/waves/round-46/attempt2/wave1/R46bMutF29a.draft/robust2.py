import os, re, shutil, subprocess, sys
S="/fast/scratch/hyaku/kasegi-r46/R46bMutF29a"
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
GATE=os.path.join(LANE,"corpus/instruments/r46-f29-gate.py")
env=dict(os.environ, TMPDIR=os.path.join(S,"tmp"))
def mk(mid, old, new):
    d=os.path.join(S,"inst",mid,"corpus","instruments")
    if os.path.isdir(os.path.join(S,"inst",mid)): shutil.rmtree(os.path.join(S,"inst",mid))
    os.makedirs(d)
    t=open(GATE,encoding="utf-8").read(); assert t.count(old)==1,(mid,t.count(old))
    open(os.path.join(d,"r46-f29-gate.py"),"w",encoding="utf-8").write(t.replace(old,new,1))
    shutil.copy(os.path.join(LANE,"corpus/instruments/source-recheck.py"), os.path.join(d,"source-recheck.py"))
    return os.path.join(d,"r46-f29-gate.py")
def run(g,t):
    return subprocess.run([sys.executable,"-B",g,"--root",t],capture_output=True,text=True,env=env,timeout=300).stdout
def limb(o,l):
    m=re.search(r"^gate %s pass=(\d) read=(.*)$"%l,o,re.M); return (m.group(1),m.group(2)) if m else ("?","?")
def fx(o): return re.findall(r"fixed=(\d+)/7",o)[0]
print("=== H1a counts-loose, THIRD plausible edit: relax the comparison, KEEP dup and adm")
g=mk("H1a-v3",'if len(rows) != 29 or adm != 29 or dup:','if len(rows) > 29 or adm > 29 or dup:')
for tree in ("duprow","probe-p1","probe-f30","positive"):
    b=run(GATE,os.path.join(S,"trees",tree)); m=run(g,os.path.join(S,"trees",tree))
    print("  H1a-v3 tree=%-11s base H1=%s [%s/7] | mutant H1=%s [%s/7]  %s" % (tree,limb(b,"H1")[0],fx(b),limb(m,"H1")[0],fx(m),"FLIP" if limb(b,"H1")[0]!=limb(m,"H1")[0] else "no-flip"))
print()
print("=== H2b: FOURTH plausible edit - drop the word-floor conjunct for non-Falsifiable sections entirely")
g=mk("H2b-v3",'(12 if sct.startswith("## Falsifiable") else 25)','0')
for tree in ("thinsection","probe-p7","positive"):
    b=run(GATE,os.path.join(S,"trees",tree)); m=run(g,os.path.join(S,"trees",tree))
    print("  H2b-v3 tree=%-11s base H2=%s [%s/7] | mutant H2=%s [%s/7]  %s" % (tree,limb(b,"H2")[0],fx(b),limb(m,"H2")[0],fx(m),"FLIP" if limb(b,"H2")[0]!=limb(m,"H2")[0] else "no-flip"))
