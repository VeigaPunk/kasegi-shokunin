import importlib.util, os, re, shutil, subprocess, sys, tempfile
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"; INSTR=os.path.join(LANE,"corpus/instruments")
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
ST=load(os.path.join(INSTR,"r46-counters-selftest-c2.py"),"st")
MB=load(os.path.join(INSTR,"r46-mutbat.py"),"mb")
PURE="/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/pure"
work=tempfile.mkdtemp(prefix="g7b-",dir="/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/work")
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
def run(c,root):
    p=subprocess.run([sys.executable,c,"--root",root],capture_output=True,text=True,timeout=300,env=env)
    g={m.group(1):int(m.group(2)) for m in re.finditer(r"^gate (G\d) pass=([01])",p.stdout,re.M)}
    rd={m.group(1):m.group(2) for m in re.finditer(r"^gate (G\d) pass=[01] read=(.*)$",p.stdout,re.M)}
    return g,rd
def scen(name,edit):
    tree=os.path.join(work,"t-"+name); shutil.copytree(base,tree,symlinks=True)
    if edit: edit(tree)
    print("### "+name)
    for mid in ("G7a-verdict-or","G7c-okline-loose"):
        gp,rp=run(ccopy("p"+name+mid,None),tree); gm,rm=run(ccopy("m"+name+mid,tri[mid]),tree)
        print("   %-20s pristine_G7=%s mutant_G7=%s | mutant read=%r" % (mid,gp.get("G7"),gm.get("G7"),rm.get("G7")))
def ecode(r):
    p=os.path.join(r,ST.SOURCES); t=open(p,encoding="utf-8").read()
    t=t.replace("| docs | A | The reporter-side","| blog | A | The reporter-side")
    open(p,"w",encoding="utf-8").write(t)
def wcode(r):
    p=os.path.join(r,ST.SOURCES); t=open(p,encoding="utf-8").read()
    t=t.replace("| mined | 2026-10-28 | 180d | "+ST.ENTRY_REL,
                "| mined | 2026-10-28 | 180d | "+ST.ENTRY_REL+", corpus/knowledge/linux-kernel-security-bugs-reporting-process.md")
    open(p,"w",encoding="utf-8").write(t)
scen("clean",None); scen("E-code-kind",ecode); scen("W-code-usedby",wcode)
shutil.rmtree(work,ignore_errors=True)
