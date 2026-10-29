"""Negative control for the probe: an EQUIVALENT-style edit must NOT flip a gate,
and a LIVE edit must flip exactly the gate it targets. Verifies probe.py's power."""
import importlib.util, os, re, shutil, subprocess, sys, tempfile
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"; INSTR=os.path.join(LANE,"corpus/instruments")
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
ST=load(os.path.join(INSTR,"r46-counters-selftest-c2.py"),"st")
MB=load(os.path.join(INSTR,"r46-mutbat.py"),"mb")
PURE="/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/pure"
work=tempfile.mkdtemp(prefix="disc-",dir="/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/work")
snap=ST.Snap(LANE); spans={k:(t,*snap.locate(t)) for k,t in ST.Q.items()}
base=os.path.join(work,"base"); ST.build(PURE,LANE,snap,spans,base)
env={"PATH":os.environ["PATH"],"HOME":os.environ["HOME"],"TMPDIR":work,"LC_ALL":"C.UTF-8","LANG":"C.UTF-8"}
tri={t[0]:t for t in MB.COUNTER["c2"][1]}
def ccopy(tag,mut):
    d=os.path.join(work,tag); di=os.path.join(d,"corpus","instruments")
    shutil.copytree(INSTR,di,symlinks=True); c=os.path.join(di,"r46-c2-gate.py")
    if mut:
        mid,old,new=mut; t=open(c,encoding="utf-8").read()
        assert t.count(old)==1; open(c,"w",encoding="utf-8").write(t.replace(old,new,1))
    return c
def gates(c,root):
    p=subprocess.run([sys.executable,c,"--root",root],capture_output=True,text=True,timeout=300,env=env)
    return {m.group(1):int(m.group(2)) for m in re.finditer(r"^gate (G\d) pass=([01])",p.stdout,re.M)}
# NEGATIVE CONTROL: an edit that is behaviourally inert (a docstring-only change
# inside the counter) must flip NOTHING.
tree=os.path.join(work,"t1"); shutil.copytree(base,tree,symlinks=True)
gp=gates(ccopy("p1",None),tree)
d=os.path.join(work,"m1"); di=os.path.join(d,"corpus","instruments")
shutil.copytree(INSTR,di,symlinks=True); c=os.path.join(di,"r46-c2-gate.py")
src=open(c,encoding="utf-8").read()
mut=src.replace('"""r46-c2-gate.py — round-46 C2 counter (coverage), v1.2','"""r46-c2-gate.py — round-46 C2 counter (coverage), v1.2 (docstring note appended by a negative control)',1)
assert mut!=src; open(c,"w",encoding="utf-8").write(mut)
gm=gates(c,tree)
diff=[g for g in gp if gp[g]!=gm[g]]
print("NEGATIVE CONTROL (docstring-only edit): gates that differ =",diff,"-> probe power OK" if not diff else "-> PROBE UNSOUND")
# POSITIVE CONTROL: G1c's live edit flips G1 and nothing else on a clean tree
tree2=os.path.join(work,"t2"); shutil.copytree(base,tree2,symlinks=True)
p=os.path.join(tree2,ST.README); t=open(p,encoding="utf-8").read()
t=t.replace("| S073 | "+ST.F28_NEXT,"| S0730 | "+ST.F28_NEXT); open(p,"w",encoding="utf-8").write(t)
gp=gates(ccopy("p2",None),tree2); gm=gates(ccopy("m2",tri["G1c-src-boundary"]),tree2)
diff=[g for g in gp if gp[g]!=gm[g]]
print("POSITIVE CONTROL (G1c on an S0730 sources cell): gates that differ =",diff)
shutil.rmtree(work,ignore_errors=True)
