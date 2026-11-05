import re, sys, json
entry = open(sys.argv[1], encoding="utf-8").read()
man = json.load(open(sys.argv[2], encoding="utf-8"))["sources"][0]["quotes"]
cap = open(sys.argv[3], encoding="utf-8").read()
mq = {q["quote"] for q in man}
parts = entry.split("`")
prose = "".join(parts[0::2]); code = parts[1::2]
segs = re.findall(r'"([^"\n]+)"', prose)
bad = [s for s in segs if not ((s in mq) and (s in cap) and len(s.split()) <= 25)]
print("prose_quotes=%d not_ok=%d" % (len(segs), len(bad)))
for s in bad: print("NOT_OK", repr(s[:80]))
for c in [c for c in code if '"' in c]:
    print("code_json inmanifest=%d incapture=%d" % (c in mq, c in cap))
print("manifest_quotes=%d unused_in_entry=%s" % (len(man), [q["id"] for q in man if q["quote"] not in entry]))
print("entry_bytes=%d entry_lines=%d" % (len(entry.encode()), entry.count("\n")))
sys.exit(1 if bad else 0)
