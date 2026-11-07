import importlib.util, io, os, re, subprocess, sys, tarfile, tempfile, shutil

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
REV = "8a1a00c639ba808a701d1f186aac9ebd0045deaa"
WORK = sys.argv[1]

d = tempfile.mkdtemp(prefix="r91labels-tree-", dir=WORK)
data = subprocess.run(["git","-C",LANE,"archive","--format=tar",REV],capture_output=True,check=True).stdout
with tarfile.open(fileobj=io.BytesIO(data)) as tf:
    tf.extractall(d, filter="tar")

spec = importlib.util.spec_from_file_location("resolve_pinned", os.path.join(d,"corpus","instruments","resolve.py"))
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
mirror = os.path.expanduser(R.MIRROR_ROOT)

BARE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*\.md)(?::(\d+)(?:-(\d+))?)?$")
kd = os.path.join(d,"corpus","knowledge")
sites = []  # (relpath, lineno, token)
for fn in sorted(os.listdir(kd)):
    if not fn.endswith(".md"): continue
    rel = "corpus/knowledge/"+fn
    with open(os.path.join(kd,fn),encoding="utf-8") as fh:
        for i,line in enumerate(fh,1):
            for m in R.TOKEN.finditer(line):
                t = m.group(1).strip().rstrip(".,;:")
                if not R.is_pathlike(t): continue
                sites.append((rel,i,t))

gone = {}
for rel,i,t in sites:
    bm = BARE.match(t)
    if not bm: continue
    name = bm.group(1)
    target = os.path.join(kd,name)
    if not os.path.isfile(target): continue
    cls = R.classify(t,d,mirror)[0]
    if cls != "GONE": continue
    gone.setdefault(t,[]).append((rel,i))

print("TREE", d)
print("MIRROR", mirror, "ABSENT", R.MIRROR_ABSENT)
print("DISTINCT_GONE_BARE_KEYS", len(gone))
print("SITES", sum(len(v) for v in gone.values()))
for t in sorted(gone):
    for rel,i in gone[t]:
        print("SITE\t%s:%d\t%s" % (rel,i,t))
