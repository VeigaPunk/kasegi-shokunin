import importlib.util, json, os, sys, collections
spec = importlib.util.spec_from_file_location("km", sys.argv[1]); km = importlib.util.module_from_spec(spec); spec.loader.exec_module(km)
pos, B, work = sys.argv[2], sys.argv[3], sys.argv[4]
R = km.load_resolve(pos)
bf = km.scope_files_rev(pos, B)
b = km.classify_scope(R, pos, bf, work)
rmap = json.load(open(sys.argv[5]))
tracked = [p for p in km.git(pos, "ls-files").split("\n") if p]
by = collections.defaultdict(list)
for p in tracked: by[p.rsplit("/", 1)[-1]].append(p)
print("classes:", collections.Counter(b.values()))
def lines(p):
    try:
        return len(open(os.path.join(pos, p), encoding="utf-8").read().splitlines())
    except Exception:
        return -1
pref, uniq = [], []
for k in sorted(b):
    if b[k] != "GONE": continue
    m = km.KEY.match(k)
    if not m: continue
    name = m.group(1); paths = by.get(name, [])
    if len(paths) == 1 and not paths[0].startswith("corpus/source-snapshots/"):
        pref.append((k, paths[0], lines(paths[0])))
    if len(paths) > 1:
        snaps = [p for p in paths if p.startswith("corpus/source-snapshots/")]
        if snaps: uniq.append((k, snaps, len(paths)))
print("prefix candidates:", len(pref))
for x in pref[:12]: print("  P", x)
print("unique-basename candidates:", len(uniq))
for x in uniq[:15]: print("  U", x[0], x[2], x[1][:3])
# anchored + unanchored counts among candidates
print("anchored pref:", sum(1 for k,_,_ in pref if ":" in k), "anchored uniq:", sum(1 for k,_,_ in uniq if ":" in k))
# frozen map: key basenames and target line counts (for oob selection)
mx = []
for k, v in rmap.items():
    name = k.split(":")[0]; p = v.split(":")[0]
    mx.append((lines(p), k, v))
mx.sort()
print("smallest target snapshots:", mx[:3])
print("largest target snapshots:", mx[-3:])
