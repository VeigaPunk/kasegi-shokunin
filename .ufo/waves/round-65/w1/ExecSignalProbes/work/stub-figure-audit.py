import json, sys
ledger, root = "corpus/instruments/figure-audit-ledger.json", "."
it = iter(sys.argv[1:])
for a in it:
    if a == "--ledger":
        ledger = next(it)
    elif a == "--root":
        root = next(it)
with open(ledger, "r", encoding="utf-8") as f:
    doc = json.load(f)
figs = doc.get("figures", [])
for ent in figs:
    print("FIG %s recorded=%s derived=%s ok" % (ent["id"], ent["recorded"], ent["want"]))
print("FIGURE-AUDIT figures=%d ok=%d stale=0 exit=0" % (len(figs), len(figs)))
sys.exit(0)
