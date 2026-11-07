import importlib.util, json, os, sys, collections
spec = importlib.util.spec_from_file_location("km", sys.argv[1]); km = importlib.util.module_from_spec(spec); spec.loader.exec_module(km)
pos, B, work = sys.argv[2], sys.argv[3], sys.argv[4]
R = km.load_resolve(pos)
b = km.classify_scope(R, pos, km.scope_files_rev(pos, B), work)
rmap = json.load(open(sys.argv[5]))
tracked = [p for p in km.git(pos, "ls-files").split("\n") if p]
by = collections.defaultdict(list)
for p in tracked: by[p.rsplit("/",1)[-1]].append(p)
def lines(p):
    try: return len(open(os.path.join(pos,p),encoding="utf-8").read().splitlines())
    except Exception: return -1
base_tokens = set(b)
rows=[]
for k in sorted(b):
    if b[k] != "GONE": continue
    m = km.KEY.match(k)
    if not m: rows.append(("NONKEY", k, "", 0)); continue
    name, lo, hi = m.group(1), m.group(2), m.group(3)
    paths = by.get(name, [])
    if len(paths) != 1: continue
    p = paths[0]; n = lines(p)
    if ":" not in k: continue
    lo_i = int(lo); hi_i = int(hi) if hi else lo_i
    val = p + (":%s" % lo if hi is None else ":%s-%s" % (lo, hi))
    rows.append(("UNIQ", k, p, n, lo_i, hi_i, val, val in base_tokens))
print("unique-basename cited tokens:", sum(1 for r in rows if r[0]=="UNIQ"))
oob=[r for r in rows if r[0]=="UNIQ" and not (1 <= r[4] <= r[5] <= r[3])]
print("out-of-range:", len(oob))
for r in oob[:10]: print("  OOB", r)
edge=[r for r in rows if r[0]=="UNIQ" and r[5]==r[3]]
print("hi==nlines:", len(edge))
for r in edge[:10]: print("  EDGE", r)
print("non-KEY GONE cites:", sum(1 for r in rows if r[0]=="NONKEY"))
for r in [r for r in rows if r[0]=="NONKEY"][:15]: print("  NK", repr(r[1]))
