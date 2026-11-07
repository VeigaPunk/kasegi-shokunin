import sys, os, json, subprocess, collections, shutil
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments")
import resolve as R
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S="/fast/scratch/hyaku/kasegi-r85/ExecC1Hunt"
MIRROR=R.MIRROR_ROOT
BASE_REV="bc722e540c93b48ff159454b65a0f9f4630db1ed"
base_skill=subprocess.run(["git","-C",LANE,"show",f"{BASE_REV}:SKILL.md"],capture_output=True,text=True).stdout
base_files=subprocess.run(["git","-C",LANE,"ls-tree","-r","--name-only",BASE_REV],capture_output=True,text=True).stdout.splitlines()
trk=[p for p in base_files if not p.startswith(".ufo/") and not p.startswith(".git/")]
base_content={p:subprocess.run(["git","-C",LANE,"cat-file","blob",f"{BASE_REV}:{p}"],capture_output=True).stdout if False else None for p in trk[:0]}
# content hash map for COMMON file names only (basename with <=3 tracked files)
# Instead: for tokens 'report.md','status.json',... contexts need care; check NO_MATCH tokens with distinctive names
depth=collections.Counter(os.path.basename(p) for p in trk)
amb=[b for b,c in depth.items() if c>=2]
snippets=[s for s in amb if s in ("report.md","status.json","provenance.json","evidence/manifest.json","custodian-receipts.json","claim_checklist.md","cue.txt","snapshot.json","package.json","README.md")]

# ---- RULE G: bounty-root relocation (relative token into corpus/knowledge/) ----
# class: token relative, exists corpus/knowledge/<base>, NOT corpus/<base>, no noise flags, not path-prefix token for a claim dir
scdir=os.path.join(S,"scope2")
repo,cites=R.collect(scdir)
gone=[t for t in sorted(cites) if R.classify(t,LANE,MIRROR)[0]=="GONE"]
frozen=json.load(open(os.path.join(LANE,".ufo/waves/round-85/c1/repair-map.json")))
base_lines=base_skill.splitlines()
def lines_of(tok):
    out=[]
    for i,ln in enumerate(base_lines,1):
        for m in R.TOKEN.finditer(ln):
            if m.group(1).strip().rstrip(".,;:")==tok: out.append(i); break
    return out
cands=[]
for tok in gone:
    if tok in frozen: continue
    base,anchor=R.strip_anchor(tok)
    if tok.startswith(("[","~","/")) or " " in tok or any(c in tok for c in "*?[{<"): continue
    if R.noise_flags(tok): continue
    # exact corpus/knowledge placement
    for cand in (f"corpus/knowledge/{base}",):
        if os.path.exists(os.path.join(LANE,cand)):
            cands.append({"token":tok,"lines":lines_of(tok),"ctx":[base_lines[i-1] for i in lines_of(tok)[:3]],
                "proposed":cand,"rule":"G:relocate-knowledge",
                "why":"relative token missing corpus/knowledge/ prefix; that exact path exists verbatim"})
print("RULE G:",len(cands))
for c in cands: print(" ",repr(c["token"]),c["lines"],"->",c["proposed"])

# ---- NO_MATCH distinctive-basename hunt ----
nm=[]
byb=collections.defaultdict(list)
for p in trk: byb[os.path.basename(p)].append(p)
uniq=[p for t in gone if t not in frozen and not t.startswith(("[","~","/")) and " " not in t for p in [t]]
for tok in gone:
    if tok in frozen or tok.startswith(("[","~","/")) or " " in tok: continue
    if R.noise_flags(tok): continue
    bn=os.path.basename(tok)
    if len(byb.get(bn,[]))==0 and (bn.endswith((".md",".json",".py",".sh",".txt",".yml",".yaml",".jsonl",".gitignore"))):
        nm.append((tok,lines_of(tok)))
print("\nNO_MATCH + file-like ext (basename absent from lane):",len(nm))
for t,l in nm: print(" ",repr(t),l)

# ---- stripped-anchor GONE (line/symbol anchors) ----
print("\nWith anchors:")
for tok in gone:
    b,a=R.strip_anchor(tok)
    if a and tok not in frozen:
        ls=lines_of(tok)
        print(" ",repr(tok),"base",repr(b),"anchor",a,ls,"ctx",base_lines[ls[0]-1][:200] if ls else "")
json.dump({"ruleG":cands,"nomatch":nm},open(os.path.join(S,"hunt3.json"),"w"),indent=1)
