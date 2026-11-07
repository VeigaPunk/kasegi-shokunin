import importlib.util
import os

S = "/fast/scratch/hyaku/kasegi-r93/CriticClaimsC1"
LANE = os.path.join(S, "lane")
WORK = os.path.join(S, "work2")
BASE = "e15996bfd2f6eca4af39507a7c5973afbeca8347"
AFTER = "ae53b3c6e7e2ce070c2f022d01c1677a8908df1b"
os.makedirs(WORK, exist_ok=True)

spec = importlib.util.spec_from_file_location("km", os.path.join(S, "knowledge-meter.frozen.py"))
km = importlib.util.module_from_spec(spec)
spec.loader.exec_module(km)

B = km.reading(LANE, BASE, WORK)
A = km.reading(LANE, AFTER, WORK)
bc, ac = B["cls"], A["cls"]
print("base rate=%d/%d after rate=%d/%d" % (km.rate(bc) + km.rate(ac)))
print("base_nongone=%d base_total=%d" % km.rate(bc))
print("after_nongone=%d after_total=%d" % km.rate(ac))
removed = sorted(set(bc) - set(ac))
added = sorted(set(ac) - set(bc))
print("REMOVED %d:" % len(removed))
for t in removed:
    print("  - %r %s" % (t, bc[t]))
print("ADDED %d:" % len(added))
for t in added:
    print("  + %r %s" % (t, ac[t]))
interesting = [
    "SKILL.md:117", "SKILL.md:191", "SKILL.md:494-506", "SKILL.md:827-848",
    "SKILL.md:111", "SKILL.md:176-178", "SKILL.md:526",
    "intake-surface.md:75-76", "corpus/knowledge/intake-surface.md:89-93",
    "mission-control.md:37-38", "corpus/knowledge/mission-control.md:55-57",
]
print("INTERESTING:")
for t in interesting:
    print("  %-55r base=%s after=%s" % (t, bc.get(t, "ABSENT"), ac.get(t, "ABSENT")))
nongone_base = {t for t, c in bc.items() if c != "GONE"}
nongone_after = {t for t, c in ac.items() if c != "GONE"}
print("nongone removed:", sorted(nongone_base - nongone_after))
print("nongone added:", sorted(nongone_after - nongone_base))
print("class churn on common tokens:", sorted(t for t in set(bc) & set(ac) if bc[t] != ac[t]))
