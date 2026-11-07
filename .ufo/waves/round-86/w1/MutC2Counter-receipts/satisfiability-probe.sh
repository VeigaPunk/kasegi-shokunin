#!/usr/bin/env bash
# Satisfiability probe for the frozen C2 contract, limbs E1 x E2.
# E2 requires evidence bytes byte-identical to corpus/source-snapshots/round-86/S122.txt.
# E1 requires corpus/instruments/claim-package-check.py PKG to exit 0 with
# verdict=WELL-FORMED. That gate scans every package file (R-NOSECRET).
#
# This script builds a package that satisfies every gate rule except the one
# S122's own bytes trip, and prints the gate verdict.
#
# Usage: satisfiability-probe.sh SCRATCH
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
S=${1:?scratch}; mkdir -p "$S"; rm -rf "$S/pkg"
cp -r "$L/corpus/practice/curl-h1-1913733" "$S/pkg"
cp "$L/corpus/source-snapshots/round-86/S122.txt" "$S/pkg/evidence/S122.txt"
python3 -B - "$S/pkg" <<'PY'
import hashlib, json, sys
pkg = sys.argv[1]
p = pkg + "/evidence/manifest.json"
man = json.load(open(p))
b = open(pkg + "/evidence/S122.txt", "rb").read()
h = hashlib.sha256(b).hexdigest()
man["sequence"] = 2
man["artifacts"].append({"path": "S122.txt", "sha256": h, "bytes": len(b),
                         "polarity": "positive", "note": "satisfiability probe"})
man["redactions"].append({"artifact": "S122.txt", "path": "S122.txt",
                          "artifact_sha256": h, "scanned_artifact_sha256": h,
                          "producer": "probe", "verifier": "probe-verifier",
                          "verifier_receipt": "scratch", "removed": [],
                          "note": "public capture; zero bytes removed"})
raw = (json.dumps(man, indent=1) + "\n").encode()
open(p, "wb").write(raw)
st = json.load(open(pkg + "/status.json"))
st["manifest_sha256"] = hashlib.sha256(raw).hexdigest()
open(pkg + "/status.json", "w").write(json.dumps(st, indent=1) + "\n")
print("s122_sha256=" + h)
PY
echo "== gate over a package whose S122 evidence bytes are the committed snapshot bytes"
python3 -B "$L/corpus/instruments/claim-package-check.py" "$S/pkg"
echo "rc=$?"
echo "== the byte sequence R-NOSECRET matches (first occurrence, truncated)"
grep -o 'X-Amz-Security-Token=.\{0,16\}' "$L/corpus/source-snapshots/round-86/S122.txt" | head -1
echo "== sha256 of the cited bytes"
sha256sum "$L/corpus/source-snapshots/round-86/S122.txt"
