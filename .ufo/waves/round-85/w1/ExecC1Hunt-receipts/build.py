import sys, os, json, subprocess, collections, re, shutil
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments")
import resolve as R
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S="/fast/scratch/hyaku/kasegi-r85/ExecC1Hunt"
W1=os.path.join(LANE,".ufo/waves/round-85/w1")
BASE_REV="bc722e540c93b48ff159454b65a0f9f4630db1ed"
LAND_REV="c0507ad"  # round-85 C1 landing commit (from git log)
def show(p,rev): return subprocess.run(["git","-C",LANE,"show",f"{rev}:{p}"],capture_output=True,text=True).stdout
tracked=set(subprocess.run(["git","-C",LANE,"ls-tree","-r","--name-only",BASE_REV],capture_output=True,text=True).stdout.splitlines())
base_lines=show("SKILL.md",BASE_REV).splitlines()
land_lines=show("SKILL.md",LAND_REV).splitlines()
MIRROR=R.MIRROR_ROOT
def lines_of(tok,lines):
    out=[]
    for i,ln in enumerate(lines,1):
        for m in R.TOKEN.finditer(ln):
            if m.group(1).strip().rstrip(".,;:")==tok: out.append(i); break
    return out
frozen=json.load(open(os.path.join(LANE,".ufo/waves/round-85/c1/repair-map.json")))
# landed scope
scdir=os.path.join(S,"scopeL")
repo,land_cites=R.collect(scdir)
hunt2=json.load(open(os.path.join(S,"hunt2.json")))
cands=[]; excluded=[]
for c in hunt2["candidates"]:
    tok,val=c["token"],c["proposed"]
    if val not in tracked:
        excluded.append({"token":tok,"reason":"proposed value not a tracked file at base","value":val}); continue
    if val in land_cites:
        excluded.append({"token":tok,"reason":"value already a distinct cited token at landing (rewrite would be a de-cite, numerator gain 0)","value":val}); continue
    if R.classify(val,LANE,MIRROR)[0]!="INTERNAL":
        excluded.append({"token":tok,"reason":"value does not classify INTERNAL","value":val}); continue
    if tok not in land_cites or R.classify(tok,LANE,MIRROR)[0]!="GONE":
        excluded.append({"token":tok,"reason":"token not GONE at landing","value":val}); continue
    bl=lines_of(tok,base_lines); ll=lines_of(tok,land_lines)
    cands.append({"token":tok,"proposed":val,"rule":c["rule"],"why":c["why"],
        "base_lines":bl,"landed_lines":ll,
        "ctx":[land_lines[i-1][:400] for i in ll[:2]]})
print("skill candidates:",len(cands),"excluded:",len(excluded))
for e in excluded: print(" EXCL",e)
# knowledge census (occurrences + distinct)
byb=collections.defaultdict(list)
for p in tracked:
    if not p.startswith(".ufo/"): byb[os.path.basename(p)].append(p)
uniq={b:v[0] for b,v in byb.items() if len(v)==1}
kfiles=sorted(p for p in tracked if re.fullmatch(r"corpus/knowledge/[^/]+\.md",p))
ktok_occ=collections.Counter(); ktok_files=collections.defaultdict(set)
for f in kfiles:
    for ln in open(os.path.join(LANE,f),encoding="utf-8",errors="replace"):
        for m in R.TOKEN.finditer(ln):
            t=m.group(1).strip().rstrip(".,;:")
            if R.is_pathlike(t):
                ktok_occ[t]+=1; ktok_files[t].add(f)
kgone=[t for t in ktok_occ if R.classify(t,LANE,MIRROR)[0]=="GONE"]
kuniq_distinct=[]; kuniq_occ=0
for t in kgone:
    b,_=R.strip_anchor(t)
    if os.path.basename(b) in uniq:
        kuniq_distinct.append(t); kuniq_occ+=ktok_occ[t]
print("knowledge files:",len(kfiles),"distinct:",len(ktok_occ),"GONE:",len(kgone),
      "nonGONE:",len(ktok_occ)-len(kgone),"UNIQUE distinct:",len(kuniq_distinct),"UNIQUE occ:",kuniq_occ)
# breakdown by proposed dir
print(collections.Counter(os.path.dirname(uniq[os.path.basename(R.strip_anchor(t)[0])]) for t in kuniq_distinct).most_common(8))
# frozen overlap: tokens equal to frozen keys
print("frozen keys in knowledge uniq:",[t for t in kuniq_distinct if t in frozen])
# also how many knowledge uniq proposed values already ... (knowledge scope is separate; report raw)
out={"base_rev":BASE_REV,"freeze_rev":"4a2d34f203519a87078f21a896dc8679137ff675","landed_rev":LAND_REV,
 "skill_candidates":sorted(cands,key=lambda c:(c["base_lines"],c["token"])),
 "excluded_ruleB":excluded,
 "knowledge":{"glob":"corpus/knowledge/*.md","n_files":len(kfiles),
   "distinct_tokens":len(ktok_occ),"gone_distinct":len(kgone),"nongone_distinct":len(ktok_occ)-len(kgone),
   "unique_basename_distinct":len(kuniq_distinct),"unique_basename_occurrences":kuniq_occ,
   "by_dir":dict(collections.Counter(os.path.dirname(uniq[os.path.basename(R.strip_anchor(t)[0])]) for t in kuniq_distinct))}}
json.dump(out,open(os.path.join(W1,"ExecC1Hunt-r86-candidates.json"),"w"),indent=1)
print("wrote candidates json")
# receipts
rd=os.path.join(W1,"ExecC1Hunt-receipts"); os.makedirs(rd,exist_ok=True)
for f in ("hunt.py","hunt2.py","hunt3.py","hunt4.py","hunt5.py","hunt6.py","hunt7.py","hunt8.py","hunt9.py","build.py",
          "hunt.out","hunt2.out","hunt3.out","hunt4.out","hunt5.out","hunt6.out","hunt7.out","hunt8.out","gone.json","hunt2.json","hunt3.json"):
    src=os.path.join(S,f)
    if os.path.exists(src): shutil.copy(src,os.path.join(rd,f))
print("receipts copied:",os.listdir(rd))
