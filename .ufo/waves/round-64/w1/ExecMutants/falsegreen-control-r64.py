import importlib.util
from pathlib import Path

B = Path("/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-64/w1/ExecMutants/figure-audit-mutbat-r64.py")
BASE = Path("/fast/scratch/hyaku/kasegi-r64/ExecMutants/base/figure-audit.py")

spec = importlib.util.spec_from_file_location("mb", str(B))
mb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mb)

work = Path("/fast/scratch/hyaku/kasegi-r64/ExecMutants/falsegreen-work")
ctx = mb.Ctx(work)
data = BASE.read_bytes()
print("run_utc=%s" % mb.utc())
print("control=base-master-under-candidate-contract instrument=%s sha256=%s" % (BASE, mb.sha(data)))
res = mb.run_probes(BASE, "candidate", ctx)
for pid, verdict in res:
    print("PROBE base-under-candidate %s verdict=%s" % (pid, verdict))
mism = [pid for pid, v in res if v == "mismatch"]
print("base-under-candidate mismatch=%d/%d falsegreen_ids=%s" % (len(mism), len(res), ",".join(mism)))
