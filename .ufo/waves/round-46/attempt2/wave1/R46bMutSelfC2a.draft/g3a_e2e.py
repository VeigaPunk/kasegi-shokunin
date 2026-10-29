"""End-to-end test of the G3a claim: does a 12-cell S073 row (extra cell APPENDED at the END,
so positions 0..10 are unchanged) let the G3a mutant read G3 green where pristine reads it red?
Runs the COMMITTED selftest with an extra case appended, against the pristine counter and
against the battery-exact G3a mutant."""
import importlib.util, os, re, shutil, subprocess, sys, tempfile
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"; INSTR=os.path.join(LANE,"corpus/instruments")
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
ST=load(os.path.join(INSTR,"r46-counters-selftest-c2.py"),"st")
MB=load(os.path.join(INSTR,"r46-mutbat.py"),"mb")
PURE="/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/pure"
work=tempfile.mkdtemp(prefix="g3a-",dir="/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/work")
tri=[t for t in MB.COUNTER["c2"][1] if t[0]=="G3a-cells-loose"][0]

# 1) build a scratch selftest = committed selftest + ONE new case
st_src=open(os.path.join(INSTR,"r46-counters-selftest-c2.py"),encoding="utf-8").read()
anchor='        # ------------------------------------------------------------------ mutants\n'
assert anchor in st_src
new_case = anchor + '''        add(Case("mut-s073-row-twelve-cells-extra-at-end", "mutant", lambda r: sub(r, SOURCES, line_of(r, SOURCES, "| S073 |"), line_of(r, SOURCES, "| S073 |")[:-1] + " | extra |"), {"G3"}, allow={"G7"}))
'''
st2=os.path.join(work,"selftest-ext.py"); open(st2,"w",encoding="utf-8").write(st_src.replace(anchor,new_case,1))
print("scratch selftest written:",st2)

env={"PATH":os.environ["PATH"],"HOME":os.environ["HOME"],"TMPDIR":work,"LC_ALL":"C.UTF-8","LANG":"C.UTF-8"}
def counter_copy(tag,mut):
    d=os.path.join(work,tag); di=os.path.join(d,"corpus","instruments")
    shutil.copytree(INSTR,di,symlinks=True); c=os.path.join(di,"r46-c2-gate.py")
    if mut:
        mid,old,new=mut; t=open(c,encoding="utf-8").read()
        assert t.count(old)==1, "drift: %d" % t.count(old)
        open(c,"w",encoding="utf-8").write(t.replace(old,new,1))
    return c
def run(st,counter):
    cmd=[sys.executable,"-I",st,"--pure",PURE]
    if counter: cmd+=["--counter",counter]
    e=dict(env); e["HYAKU_SCRATCH"]=os.path.join(work,"scr-"+os.path.basename(st)+("-"+(counter or "none").replace("/","_")))
    os.makedirs(e["HYAKU_SCRATCH"],exist_ok=True)
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=3600,cwd=LANE,env=e)
    m=re.findall(r"failures=(\d+)",p.stdout)
    return (int(m[-1]) if m else -1), p.stdout
f,t=run(st2,None)
print("EXTENDED selftest vs PRISTINE counter: failures=%d"%f)
for l in t.splitlines():
    if "twelve-cells" in l: print("   ",l)
f2,t2=run(st2,counter_copy("mut",tri))
print("EXTENDED selftest vs G3a MUTANT counter: failures=%d"%f2)
for l in t2.splitlines():
    if "twelve-cells" in l: print("   ",l)
print()
print("VERDICT: the new case %s the G3a mutant (failures %d -> %d)" % (
      "CATCHES" if f2>f else "does NOT catch", f, f2))
shutil.rmtree(work,ignore_errors=True)
