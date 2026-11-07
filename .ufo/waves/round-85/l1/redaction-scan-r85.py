#!/usr/bin/env python3
"""KasegiR85 redaction verifier scan for the round-85 practice package.
For every artifact in PKG/evidence/manifest.json: recompute sha256, compare with
the manifest digest and with the redaction receipt's artifact/scanned digests,
and scan the bytes with claim-package-check.py's own SECRET_PATTERNS.
Usage: redaction-scan-r85.py PKG   (exit 0 only when every artifact is bound and clean)"""
import hashlib, importlib.util, json, os, sys
L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
spec = importlib.util.spec_from_file_location("g", os.path.join(L, "corpus/instruments/claim-package-check.py"))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
pkg = sys.argv[1]
m = json.load(open(os.path.join(pkg, "evidence", "manifest.json")))
rec = {r["path"]: r for r in m["redactions"]}
bad = 0
for a in m["artifacts"]:
    b = open(os.path.join(pkg, "evidence", a["path"]), "rb").read()
    h = hashlib.sha256(b).hexdigest()
    hits = [n for n, r in g.SECRET_PATTERNS if r.search(b)]
    r = rec.get(a["path"], {})
    ok = h == a["sha256"] == r.get("artifact_sha256") == r.get("scanned_artifact_sha256") and not hits and r.get("verifier") == "KasegiR85"
    bad += not ok
    print("SCAN %s sha256=%s bytes=%d patterns=%d hits=%s bound=%s verifier=%s" % (a["path"], h, len(b), len(g.SECRET_PATTERNS), ",".join(hits) or "0", ok, r.get("verifier")))
print("REDACTION-SCAN artifacts=%d bad=%d rc=%d" % (len(m["artifacts"]), bad, 1 if bad else 0))
sys.exit(1 if bad else 0)
