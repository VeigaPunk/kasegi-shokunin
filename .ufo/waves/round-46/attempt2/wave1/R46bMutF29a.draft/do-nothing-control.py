import os, subprocess, sys
S="/fast/scratch/hyaku/kasegi-r46/R46bMutF29a"
L="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
env=dict(os.environ, TMPDIR=os.path.join(S,"tmp"))
def run(g, t):
    p=subprocess.run([sys.executable,"-B",g,"--root",t],capture_output=True,text=True,env=env,timeout=300)
    return p.stdout, p.returncode
div=0
for name in sorted(os.listdir(os.path.join(S,"trees"))):
    t=os.path.join(S,"trees",name)
    if not os.path.isdir(t): continue
    a,ra=run(os.path.join(L,"corpus/instruments/r46-f29-gate.py"),t)
    b,rb=run(os.path.join(S,"inst/noop/corpus/instruments/r46-f29-gate.py"),t)
    last=[l for l in a.strip().splitlines() if l.startswith("f29-gate")]
    same = (a==b and ra==rb)
    print("%-14s %s rc=%s %s" % (name, "IDENTICAL" if same else "DIFFER", ra, last[0] if last else ""))
    if not same: div+=1
print("do-nothing-control-divergences=%d" % div)
