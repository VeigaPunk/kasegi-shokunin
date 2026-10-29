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
    p=subprocess.run([sys.executable,"-B",g,"--root",t],capture_output=True,text=True,env=env,timeout=300)
    return p.stdout
def limb(out,l):
    m=re.search(r"^gate %s pass=(\d) read=(.*)$"%l,out,re.M); return (m.group(1),m.group(2)) if m else ("?","?")
def fixed(out): return re.findall(r"fixed=(\d+)/7",out)[0]

print("=== ROBUSTNESS: H1a counts-loose, TWO plausible edits (both match the receipt's own name 'counts-loose')")
variants={
 "H1a-v1": ('if len(rows) != 29 or adm != 29 or dup:', 'if len(rows) < 29 or adm < 29:'),                      # C2 G1a analogue (drops dup)
 "H1a-v2": ('if len(rows) != 29 or adm != 29 or dup:', 'if len(rows) < 29 or adm != 29 or dup:'),                # relaxes only the count comparison
}
for mid,(o,n) in variants.items():
    g=mk(mid,o,n)
    for tree in ("duprow","probe-p1","probe-f30"):
        b=run(GATE,os.path.join(S,"trees",tree)); m=run(g,os.path.join(S,"trees",tree))
        print("  %-8s tree=%-12s base H1=%s [%s/7] | mutant H1=%s [%s/7]" % (mid,tree,limb(b,"H1")[0],fixed(b),limb(m,"H1")[0],fixed(m)))
print()
print("=== ROBUSTNESS: H2b wordfloor-low, TWO plausible edits")
variants={
 "H2b-v1": ('(12 if sct.startswith("## Falsifiable") else 25)','(1 if sct.startswith("## Falsifiable") else 5)'),  # C2 G2b analogue
 "H2b-v2": ('(12 if sct.startswith("## Falsifiable") else 25)','(1 if sct.startswith("## Falsifiable") else 24)'),  # one word lower
}
for mid,(o,n) in variants.items():
    g=mk(mid,o,n)
    for tree in ("thinsection","probe-p7","probe-p2"):
        b=run(GATE,os.path.join(S,"trees",tree)); m=run(g,os.path.join(S,"trees",tree))
        print("  %-8s tree=%-12s base H2=%s [%s/7] | mutant H2=%s [%s/7]" % (mid,tree,limb(b,"H2")[0],fixed(b),limb(m,"H2")[0],fixed(m)))
print()
print("=== ROBUSTNESS: H3a cells-loose, TWO plausible edits")
variants={
 "H3a-v1": ('if len(c) == 11:','if len(c) >= 9:'),
 "H3a-v2": ('if len(c) == 11:','if len(c) >= 10:'),
}
for mid,(o,n) in variants.items():
    g=mk(mid,o,n)
    for tree in ("row9cells","probe-p3"):
        b=run(GATE,os.path.join(S,"trees",tree)); m=run(g,os.path.join(S,"trees",tree))
        print("  %-8s tree=%-12s base H3=%s [%s/7] | mutant H3=%s [%s/7]  mutantH7=%s" % (mid,tree,limb(b,"H3")[0],fixed(b),limb(m,"H3")[0],fixed(m),limb(m,"H7")[0]))
