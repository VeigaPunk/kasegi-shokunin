import re, json, hashlib
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
cap_bytes = open(f"{LANE}/corpus/source-snapshots/round-74/S109.txt", "rb").read()
print("capture sha256:", hashlib.sha256(cap_bytes).hexdigest(), "bytes:", len(cap_bytes))
cap = cap_bytes.decode("utf-8").split("\n")[:-1]
print("capture lines:", len(cap))
ent = open(f"{LANE}/.ufo/waves/round-74/w1/knowledge-fuzzilli-js-engine-fuzzing-framework.md", encoding="utf-8").read().split("\n")
trio = [
 "source: S109 — Google Project Zero Fuzzilli, https://github.com/googleprojectzero/fuzzilli (capture corpus/source-snapshots/round-74/S109.txt, sha256 c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486)",
 "verified-at: 2026-11-05",
 "recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-74/manifest.json --source S109"]
print("trio exact:", ent[:3] == trio)
cj = json.load(open(f"{LANE}/.ufo/waves/round-74/claims.json"))
print("scope_limit verbatim:", cj["C2"]["scope_limit"] in "\n".join(ent))
quotes = []
for pi, line in enumerate(ent, 1):
    for m in re.finditer(r'"([^"\n]+)"', line):
        quotes.append((pi, m.start(), m.group(1), line))
bad = 0
for pi, pos, q, line in quotes:
    wc = len(q.split())
    where = [i+1 for i, cl in enumerate(cap) if q in cl]
    anchor = re.search(r'S109\.txt:(\d+)(?:-(\d+))?', line[pos:])
    j = pi
    while not anchor and j < len(ent) and ent[j].strip():
        anchor = re.search(r'S109\.txt:(\d+)(?:-(\d+))?', ent[j]); j += 1
    if anchor:
        a = int(anchor.group(1)); b = int(anchor.group(2) or a)
        ok_anchor = any(a <= w <= b for w in where); anc = f"{a}-{b}"
    else:
        ok_anchor = False; anc = "NONE"
    ok = bool(where) and ok_anchor and wc <= 25
    bad += (not ok)
    if not ok or wc > 20: print(f"{'OK ' if ok else 'BAD'} wc={wc} anchor={anc} found={where[:4]} q={q[:60]!r}")
print(f"quotes={len(quotes)} BAD={bad}")
print("max quote words:", max(len(q.split()) for _,_,q,_ in quotes))
