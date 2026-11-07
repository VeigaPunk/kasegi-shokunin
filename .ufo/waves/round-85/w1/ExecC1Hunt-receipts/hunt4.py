import sys, os, json, subprocess, collections
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments")
import resolve as R
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S="/fast/scratch/hyaku/kasegi-r85/ExecC1Hunt"
MIRROR=R.MIRROR_ROOT
BASE_REV="bc722e540c93b48ff159454b65a0f9f4630db1ed"
base_skill=subprocess.run(["git","-C",LANE,"show",f"{BASE_REV}:SKILL.md"],capture_output=True,text=True).stdout
base_files=subprocess.run(["git","-C",LANE,"ls-tree","-r","--name-only",BASE_REV],capture_output=True,text=True).stdout.splitlines()
trk=[p for p in base_files if not p.startswith(".ufo/")]
base_lines=base_skill.splitlines()
def lines_of(tok,lines):
    out=[]
    for i,ln in enumerate(lines,1):
        for m in R.TOKEN.finditer(ln):
            if m.group(1).strip().rstrip(".,;:")==tok: out.append(i); break
    return out
scdir=os.path.join(S,"scope2"); repo,cites=R.collect(scdir)
gone=[t for t in sorted(cites) if R.classify(t,LANE,MIRROR)[0]=="GONE"]
frozen=json.load(open(os.path.join(LANE,".ufo/waves/round-85/c1/repair-map.json")))
byb=collections.defaultdict(list)
for p in trk: byb[os.path.basename(p)].append(p)
# Rule J: brace multi-expand where exactly one tracked file matches ANY member? No.
# Rule K: second-path-arg split — token 'sha256sum A B': BOTH A,B exist. record both.
print("== second-arg / sha256sum ==")
for tok in gone:
    if tok.startswith("sha256sum "):
        ws=tok.split()
        print(repr(tok), lines_of(tok,base_lines), [w for w in ws if os.path.exists(os.path.join(LANE,w))])
# Rule L: directory-token resolves to tracked DIR file? corpus/instruments/ exists as dir; classify literal os.path.exists(dir)=True?
print("== dir tokens ==")
for tok in gone:
    if tok.endswith("/"):
        p=os.path.join(LANE,tok)
        if os.path.exists(p):
            print(repr(tok), lines_of(tok,base_lines), "exists as dir?", os.path.isdir(p))
# Rule M: for each NO_MATCH file-like token, search any tracked file whose name contains the stem
stems={}
for p in trk: stems.setdefault(os.path.basename(p),[]).append(p)
print("== NO_MATCH whose stem is substring/prefix ==")
for tok in gone:
    if tok in frozen or tok.startswith(("[","~","/")) or " " in tok: continue
    if R.noise_flags(tok): continue
    bn=os.path.basename(tok)
    if bn in stems: continue
    stem=os.path.splitext(bn)[0]
    if len(stem)<6: continue
    hits=[p for p in trk if stem in os.path.basename(p)]
    if hits:
        print(repr(tok), lines_of(tok,base_lines), "hits:",hits[:4], "ctx:", base_lines[lines_of(tok,base_lines)[0]-1][:220] if lines_of(tok,base_lines) else "")
# controls/fixtures.json line context full
print("\n== line 1198 ==")
print(base_lines[1197])
