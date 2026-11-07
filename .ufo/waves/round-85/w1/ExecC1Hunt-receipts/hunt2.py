import re
import sys, os, json, subprocess, collections, hashlib, shutil
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments")
import resolve as R
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BASE_REV="bc722e540c93b48ff159454b65a0f9f4630db1ed"
S="/fast/scratch/hyaku/kasegi-r85/ExecC1Hunt"
MIRROR=R.MIRROR_ROOT
def git(*a):
    return subprocess.run(["git","-C",LANE]+list(a),capture_output=True,text=True).stdout
# base SKILL.md bytes
base_skill=git("show",f"{BASE_REV}:SKILL.md")
assert base_skill
open(os.path.join(S,"base_SKILL.md"),"w").write(base_skill)
base_lines=base_skill.splitlines()
cur_lines=open(os.path.join(LANE,"SKILL.md"),encoding="utf-8").read().splitlines()
# tracked at base
base_files=git("ls-tree","-r","--name-only",BASE_REV).splitlines()
by_base=collections.defaultdict(list)
by_base_nonufo=collections.defaultdict(list)
for p in base_files:
    by_base[os.path.basename(p)].append(p)
    if not p.startswith(".ufo/"): by_base_nonufo[os.path.basename(p)].append(p)
def exists_lane(rel):
    return os.path.exists(os.path.join(LANE,rel))
# scratch scope collect on base SKILL
scdir=os.path.join(S,"scope2"); os.makedirs(scdir,exist_ok=True)
open(os.path.join(scdir,"SKILL.md"),"w").write(base_skill)
repo,cites=R.collect(scdir)
print("base tokens",len(cites))
gone=[]; ok=0
for tok in sorted(cites):
    if R.classify(tok,LANE,MIRROR)[0]=="GONE": gone.append(tok)
    else: ok+=1
print("base GONE",len(gone),"nonGONE",ok)
frozen=json.load(open(os.path.join(LANE,".ufo/waves/round-85/c1/repair-map.json")))
def token_lines(tok,lines):
    out=[]
    for i,ln in enumerate(lines,1):
        for m in R.TOKEN.finditer(ln):
            if m.group(1).strip().rstrip(".,;:")==tok:
                out.append(i); break
    return out
def ctx_of(lines,n,idxs):
    return [lines[i-1][:500] for i in idxs[:4]]
# every path ever in repo history (for lost-marker byte check)
allobjs={}
out=git("rev-list","--all","--objects")
for ln in out.splitlines():
    parts=ln.split(" ",1)
    if len(parts)==2: allobjs.setdefault(parts[1],[]).append(parts[0])
print("history paths:",len(allobjs))
lost_re=re.compile(r"^\[(lost-[a-z]+)\]\s+(.+)$")
def unwrap_lost(tok):
    m=lost_re.match(tok)
    if not m: return None,None
    inner=m.group(2).strip()
    b,a=R.strip_anchor(inner)
    return m.group(1),b
def sha_file(p):
    return hashlib.sha256(open(p,"rb").read()).hexdigest()
def sha_blob(sha):
    b=subprocess.run(["git","-C",LANE,"cat-file","blob",sha],capture_output=True).stdout
    return hashlib.sha256(b).hexdigest()
# fixtures+snapshots basename index (byte-identical rule scope)
fix_idx=collections.defaultdict(list)
for p in base_files:
    if p.startswith("corpus/source-snapshots/") or p.startswith("corpus/instruments/fixtures/"):
        fix_idx[os.path.basename(p)].append(p)
candidates=[]; rejected=collections.defaultdict(list)
for tok in gone:
    if tok in frozen:
        rejected["FROZEN18"].append(tok); continue
    base,anchor=R.strip_anchor(tok)
    bn=os.path.basename(base)
    lines=token_lines(tok,base_lines)
    ctx=ctx_of(base_lines,0,lines)
    noise=R.noise_flags(tok)
    cand=None; rule=None; why=""
    # RULE-B command/arg split: first whitespace word whose path resolves in lane
    if " " in tok:
        for w in tok.split():
            w2=w.strip().rstrip(".,;:")
            if ("/" in w2 or R.EXTS.search(w2)) and exists_lane(w2):
                cand=w2; rule="B:split-first-resolving-word"
                why="token is a command invocation; its first word that exists verbatim in the lane is the cited file"
                break
    # RULE-D missing corpus/ prefix (single token, relative)
    if cand is None and not tok.startswith(("[","~","/")) and " " not in tok and not any(c in tok for c in "*?[{<"):
        if exists_lane("corpus/"+base):
            cand="corpus/"+base; rule="D:missing-corpus-prefix"
            why="token resolves verbatim under corpus/"
    # RULE-C lost-marker unwrap literal
    kind,inner=unwrap_lost(tok)
    if cand is None and kind:
        if exists_lane(inner):
            cand=inner; rule="C:lost-unwrap-literal"
            why=f"{kind} inner path exists verbatim in lane"
        else:
            # byte-identical: inner path in history, blob hash == a same-basename fixture/snapshot file
            if inner in allobjs:
                for bsha in allobjs[inner]:
                    hb=sha_blob(bsha)
                    for fp in fix_idx.get(os.path.basename(inner),[]):
                        if sha_file(os.path.join(LANE,fp))==hb:
                            cand=fp; rule="H:lost-byte-identical"
                            why=f"blob of historic {inner} ({bsha[:12]}..) is byte-identical to {fp}"
                            break
                    if cand: break
            if cand is None:
                samebn=fix_idx.get(os.path.basename(inner),[])
                if len(samebn)==1 and inner not in allobjs:
                    rejected["LOST_NO_HISTORY"].append({"token":tok,"inner":inner,"history":False})
                elif inner in allobjs:
                    rejected["LOST_HISTORY_DIFFERS"].append({"token":tok,"inner":inner})
    # RULE-F brace expansion single-hit (non-domain tokens only; domain handled by classify already)
    if cand is None and "{" in tok and "}" in tok and not tok.startswith(("[","~","/")):
        exps=R.brace_expand(base)
        hits=[e for e in exps if exists_lane(e)]
        if len(hits)==1:
            cand=hits[0]; rule="F:brace-single-hit"
            why=f"brace expansion of base yields exactly one existing lane path among {len(exps)} expansions"
        elif len(hits)>1:
            rejected["BRACE_MULTI"].append({"token":tok,"hits":hits})
    # RULE-I same-dir same-stem rename
    if cand is None and not tok.startswith(("[","~","/")) and " " not in tok and not any(c in tok for c in "*?[{<"):
        d=os.path.dirname(base); stem=os.path.splitext(os.path.basename(base))[0]
        if d and os.path.isdir(os.path.join(LANE,d)):
            sibs=[f for f in os.listdir(os.path.join(LANE,d)) if os.path.splitext(f)[0]==stem and f!=os.path.basename(base)]
            tr=[p for p in by_base_nonufo.values() for p in p if os.path.dirname(p)==d and os.path.splitext(os.path.basename(p))[0]==stem]
            if len(tr)==1:
                cand=tr[0]; rule="I:same-stem-rename"
                why=f"directory exists; exactly one tracked sibling shares stem {stem!r}"
    if cand:
        candidates.append({"token":tok,"lines":lines,"ctx":ctx,"base":base,"proposed":cand,"rule":rule,"why":why,"noise":noise})
    elif noise:
        rejected["NOISE_"+noise].append(tok)
    else:
        cands=sorted(by_base_nonufo.get(bn,[]))
        if len(cands)>=2: rejected["AMBIGUOUS"].append({"token":tok,"lines":lines,"cands":cands,"ctx":ctx})
        elif len(cands)==1: rejected["UNIQUE_NONFROZEN_OTHER"].append({"token":tok,"lines":lines,"cand":cands[0],"ctx":ctx})
        else: rejected["NO_MATCH"].append(tok)
print("candidates:",len(candidates))
for c in candidates:
    print(c["rule"],"|",repr(c["token"]),"|",c["lines"],"->",c["proposed"])
print("rejected counts:",{k:len(v) for k,v in rejected.items()})
json.dump({"candidates":candidates,"rejected_counts":{k:len(v) for k,v in rejected.items()},
 "ambiguous":rejected.get("AMBIGUOUS",[]),"unique_other":rejected.get("UNIQUE_NONFROZEN_OTHER",[])},
 open(os.path.join(S,"hunt2.json"),"w"),indent=1)
