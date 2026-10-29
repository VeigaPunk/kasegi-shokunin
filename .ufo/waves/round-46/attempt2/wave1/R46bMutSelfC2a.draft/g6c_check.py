import importlib.util, os, re, shutil, subprocess, sys, tempfile
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"; INSTR=os.path.join(LANE,"corpus/instruments")
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
ST=load(os.path.join(INSTR,"r46-counters-selftest-c2.py"),"st")
MB=load(os.path.join(INSTR,"r46-mutbat.py"),"mb")
PURE="/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/pure"
work=tempfile.mkdtemp(prefix="g6c2-",dir="/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/work")
snap=ST.Snap(LANE); spans={k:(t,*snap.locate(t)) for k,t in ST.Q.items()}
base=os.path.join(work,"base"); ST.build(PURE,LANE,snap,spans,base)
ent=os.path.join(base,ST.ENTRY_REL)
# shrink the entry hard: 100 bytes
open(ent,"w",encoding="utf-8").write("# tiny\n")
print("entry size now:",os.path.getsize(ent))
def run(tag, mut):
    d=os.path.join(work,tag); di=os.path.join(d,"corpus","instruments")
    shutil.copytree(INSTR,di,symlinks=True); c=os.path.join(di,"r46-c2-gate.py")
    if mut:
        mid,old,new=mut; t=open(c,encoding="utf-8").read()
        assert t.count(old)==1; open(c,"w",encoding="utf-8").write(t.replace(old,new,1))
    env={"PATH":os.environ["PATH"],"HOME":os.environ["HOME"],"TMPDIR":work,"LC_ALL":"C.UTF-8","LANG":"C.UTF-8"}
    p=subprocess.run([sys.executable,c,"--root",base],capture_output=True,text=True,timeout=300,env=env)
    g={m.group(1):int(m.group(2)) for m in re.finditer(r"^gate (G\d) pass=([01])",p.stdout,re.M)}
    red=sorted(k for k,v in g.items() if v==0)
    print(tag,"gates",g,"red",red)
    return g
triple=[t for t in MB.COUNTER["c2"][1] if t[0]=="G6c-size-low"][0]
gp=run("pristine",None); gm=run("mutant",triple)
diff=sorted(set(k for k,v in gp.items() if v==0) ^ set(k for k,v in gm.items() if v==0))
print("GATES THAT DIFFER:",diff)
shutil.rmtree(work,ignore_errors=True)
