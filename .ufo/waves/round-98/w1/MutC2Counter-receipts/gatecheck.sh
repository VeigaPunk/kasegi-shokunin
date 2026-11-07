#!/usr/bin/env bash
# Gate-level cross-check: commit each mutant in the FIXTURE clone, run the full
# round-98 C2 gate at that rev, reset. Every git call names -C "$D".
set -u
S=/fast/scratch/hyaku/kasegi-r98/MutC2Counter
D="$S/lane"
INST="$D/corpus/instruments/capture-secret-scan.py"
LAND=e2caf4a1561b544a6ea684b0bcfa975f7e7f6061
OUT="$S/gate-raw"
mkdir -p "$OUT"
top=$(git -C "$D" rev-parse --show-toplevel)
[ "$top" = "$D" ] || { echo "TOPLEVEL MISMATCH: $top"; exit 9; }
for name in M13-session-hex-uppercase M14-narrow-ci-build-boundary M16-optional-session-context M17-registration-20-to-21 M01-drop-ci-build; do
  python3 - "$S" "$name" "$INST" "$LAND" <<'PY'
import sys, os
S, name, inst, land = sys.argv[1:5]
import json, hashlib
res = json.load(open(os.path.join(S, "results-20261107.json")))
row = [m for m in res["mutants"] if m["name"] == name][0]
pristine = open(inst, "rb").read()
# rebuild the mutant from the harness table
sys.argv = ["harness"]
sys.path.insert(0, S)
import importlib.util
spec = importlib.util.spec_from_file_location("h", os.path.join(S, "harness.py"))
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
old = new = None
for n, kind, o, w in h.MUTANTS:
    if n == name:
        old, new = o, w
text = pristine.decode()
assert text.count(old) == 1, "count"
open(inst, "wb").write(text.replace(old, new).encode())
print("wrote", name, hashlib.sha256(open(inst,'rb').read()).hexdigest()[:16])
PY
  git -C "$D" add -A
  git -C "$D" -c user.name=fixture -c user.email=fixture@invalid commit -q -m "mutant $name"
  rev=$(git -C "$D" rev-parse HEAD)
  echo "=== $name rev=$rev"
  python3 -B "$D/.ufo/waves/round-98/c2/capability-check.py" --lane "$D" --rev "$rev" \
      --work "$S/gatework" --seed 20261107 > "$OUT/$name.gate.txt" 2>&1
  echo "gate rc=$?"
  grep -E '^LIMB|^CAPABILITY-CHECK-RESULT' "$OUT/$name.gate.txt"
  git -C "$D" reset --hard -q "$LAND"
  git -C "$D" clean -qfd
done
echo "--- final clone state:"
git -C "$D" rev-parse HEAD
git -C "$D" status --porcelain
sha256sum "$INST"
