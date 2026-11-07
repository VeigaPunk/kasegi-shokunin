import os, re, sys, subprocess

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
REV = "8a1a00c639ba808a701d1f186aac9ebd0045deaa"
TREE = sys.argv[1]
TSV = sys.argv[2]
BARE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*\.md)(?::(\d+)(?:-(\d+))?)?$")
VAL = re.compile(r"^corpus/knowledge/([A-Za-z0-9][A-Za-z0-9._-]*\.md):(\d+)(?:-(\d+))?$")
FIXNAME = re.compile(r"^Replace with ([A-Za-z0-9][A-Za-z0-9._-]*\.md):(\d+)(?:-(\d+))?")
FIXDASH = re.compile(r"^Replace with — ")

def readlines(rel):
    with open(os.path.join(TREE, rel), encoding="utf-8") as fh:
        return fh.read().split("\n")

def entrylen(name):
    p = os.path.join(TREE, "corpus", "knowledge", name)
    if not os.path.isfile(p): return None
    with open(p, encoding="utf-8") as fh: return len(fh.read().split("\n"))

rows, errs = [], []
seen = {}
for i, ln in enumerate(open(TSV, encoding="utf-8")):
    if i == 0: continue
    ln = ln.rstrip("\n")
    if not ln.strip(): continue
    c = ln.split("\t")
    if len(c) != 5: errs.append("cols=%d: %s" % (len(c), ln[:60])); continue
    line, key, label, fix, ev = c
    rows.append((line, key, label, fix, ev))

eligible = []  # (line,key) with a named edit (non-CORRECT)
for line, key, label, fix, ev in rows:
    m = re.match(r"^(.+):(\d+)$", line)
    if not m: errs.append("bad line field %r" % line); continue
    rel, n = m.group(1), int(m.group(2))
    try: lines = readlines(rel)
    except OSError: errs.append("missing citing file %s" % rel); continue
    if n < 1 or n > len(lines): errs.append("line out of range %s" % line); continue
    text = lines[n-1]
    occ = text.count("`%s`" % key)
    if occ != 1: errs.append("%s key `%s` occurs %d times" % (line, key, occ))
    km = BARE.match(key)
    if not km: errs.append("key not a bare key: %s" % key); continue
    name, a, b = km.group(1), km.group(2), km.group(3)
    if (line, key) in seen: errs.append("duplicate row %s %s" % (line, key))
    seen[(line, key)] = (label, fix)

    def check_target(tname, na, nb, tag):
        el = entrylen(tname)
        if el is None: errs.append("%s target missing corpus/knowledge/%s" % (line, tname)); return
        if tname != name: errs.append("%s target %s != key file %s" % (line, tname, name))
        if na < 1 or na > el or (nb and (int(nb) < na or int(nb) > el)):
            errs.append("%s anchor %s:%s-%s outside 1..%d" % (line, tname, na, nb, el))

    if label == "CORRECT":
        if a: check_target(name, int(a), b, "correct")
        # correct rows are map-eligible as pure qualification; record
        eligible.append((line, key, "corpus/knowledge/%s%s" % (name, ":%s%s" % (a, "-"+b if b else "") if a else "")))
    elif label == "content-repair":
        if FIXDASH.match(fix):
            pass
        else:
            fm = FIXNAME.match(fix)
            if not fm: errs.append("%s content-repair fix not FIXNAME/FIXDASH: %r" % (line, fix[:40]))
            else: check_target(fm.group(1), int(fm.group(2)), fm.group(3), "fixname")
            eligible.append((line, key, None))
    else:
        vm = VAL.match(label)
        if not vm: errs.append("%s label not a canonical range: %r" % (line, label))
        else:
            check_target(vm.group(1), int(vm.group(2)), vm.group(3), "label")
            eligible.append((line, key, label))

# set equality against the GONE scan (re-derive independently)
sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[0])))
scan = subprocess.run([sys.executable, "-B", os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "scan-gone.py"),
                       os.environ.get("TMPDIR", "/fast/scratch/hyaku/kasegi-r91/ReviewC1Labels")],
                      capture_output=True, text=True)
site = set()
for l in scan.stdout.split("\n"):
    if l.startswith("SITE\t"):
        _, where, tok = l.split("\t")
        site.add((where, tok))
if site != set(seen):
    errs.append("site set mismatch: unlabelled=%s extra=%s" % (sorted(site - set(seen))[:5], sorted(set(seen)-site)[:5]))

print("LABELS rows=%d distinct_sites=%d gone_sites=%d map_eligible=%d" % (len(rows), len(seen), len(site), len(eligible)))
for e in errs: print("FAIL", e)
print("VERIFY", "PASS" if not errs else "FAIL")
