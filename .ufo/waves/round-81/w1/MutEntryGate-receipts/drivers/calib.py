#!/usr/bin/env python3
"""B8 calibration: run the frozen entry gate on every admitted entry whose source id
appears in some round manifest. Read-only over the lane tree."""
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gate.py")
KN = os.path.join(LANE, "corpus", "knowledge")
SNAP = os.path.join(LANE, "corpus", "source-snapshots")

# entry -> set(sid) from entries' own `source: <SID> ` lines
entry_sids = {}
sid_src = {}
for name in sorted(os.listdir(KN)):
    if not name.endswith(".md"):
        continue
    p = os.path.join(KN, name)
    with open(p, encoding="utf-8") as fh:
        txt = fh.read()
    sids = set(re.findall(r"(?m)^source: (S\d{3}) ", txt))
    if sids:
        entry_sids[name] = sids
    for s in sids:
        sid_src.setdefault(s, []).append(name)

rows = []
for rd in sorted(os.listdir(SNAP)):
    mp = os.path.join(SNAP, rd, "manifest.json")
    if not os.path.isfile(mp):
        continue
    with open(mp, encoding="utf-8") as fh:
        man = json.load(fh)
    for src in man.get("sources", []):
        sid = src["id"]
        for entry in sid_src.get(sid, []):
            ep = os.path.join(KN, entry)
            r = subprocess.run([sys.executable, GATE, "--entry", ep, "--manifest", mp,
                                "--source", sid, "--lane", LANE],
                               capture_output=True, text=True, env={**os.environ, "TMPDIR": os.path.dirname(os.path.abspath(__file__))})
            out = (r.stdout or "").strip().split("\n")
            line = out[0] if out and out[0].startswith("ENTRY-GATE sid=") else ""
            verdict = out[-1] if out else ""
            rows.append({"round": rd, "sid": sid, "entry": entry, "rc": r.returncode,
                         "line": line, "verdict": verdict, "stderr": (r.stderr or "").strip()})

print("ROWS", len(rows))
for row in rows:
    print("%(round)s\t%(sid)s\t%(entry)s\trc=%(rc)s\t%(verdict)s" % row)
    if row["line"]:
        print("   " + row["line"])
    if row["stderr"]:
        print("   STDERR " + row["stderr"][:300])
npass = sum(1 for r in rows if r["verdict"].endswith("pass"))
print("SUMMARY pass=%d fail=%d other=%d of %d" % (
    npass, sum(1 for r in rows if r["verdict"].endswith("fail")),
    sum(1 for r in rows if not r["verdict"].endswith(("pass", "fail"))), len(rows)))
json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "calib.json"), "w"), indent=1)
