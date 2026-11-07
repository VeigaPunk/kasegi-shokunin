#!/usr/bin/env python3
"""Re-check every instrument sha256 pin in round-89 claims.json against the
bytes at the C1 landing commit (claims P2)."""
import hashlib
import json
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
REV = "eb5f0df8eaceca617465e493c710e8626e9aa618"

claims = json.load(open(LANE + "/.ufo/waves/round-89/claims.json"))
pins = claims["instruments"]
bad = 0
for path, want in sorted(pins.items()):
    r = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (REV, path)], capture_output=True)
    if r.returncode != 0:
        print("PIN MISSING %s (rc=%d)" % (path, r.returncode))
        bad += 1
        continue
    got = hashlib.sha256(r.stdout).hexdigest()
    ok = got == want
    bad += 0 if ok else 1
    print("PIN %s %s" % ("pass" if ok else "FAIL got=" + got, path))
print("P2-PINS total=%d bad=%d %s" % (len(pins), bad, "AGREE (P2 holds)" if bad == 0 else "DISAGREE"))
sys.exit(1 if bad else 0)
