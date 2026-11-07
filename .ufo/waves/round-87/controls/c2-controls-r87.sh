#!/usr/bin/env bash
# Round-87 C2 pre-freeze controls over the frozen counter c2/capability-check.py.
# Each control is a `git clone --shared` of the base under SCRATCH with files placed
# and one fixture commit made INSIDE that clone (toplevel verified first); the
# counter then reads the clone's committed bytes at HEAD.
# Usage: c2-controls-r87.sh SCRATCH_DIR
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$L/.ufo/waves/round-87
B=cd1f568a6be2656b5f5dc479eb90ef99b91131b5
C=$W/c2/candidate
S=${1:?scratch}; mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
ISHA=$(sha256sum $C/capture-secret-scan.py | cut -d' ' -f1)
GSHA=$(git -C $L show $B:corpus/instruments/claim-package-check.py | sha256sum | cut -d' ' -f1)
ROW='| capture-secret-scan | Scans captured evidence (source snapshots, seat receipts, live- captures) at a git revision or a file list for credential shapes before commit: the claim-package gate patterns plus AWS STS session tokens and AWS key ids, with a digest-bound allowlist | `python3 -B .ufo/waves/round-87/c2/capability-check.py --lane . --rev master --work <scratch>` (K1-K5 pass) | 87 |'
echo "counter_sha256=$(sha256sum $W/c2/capability-check.py | cut -d' ' -f1) instrument_sha256=$ISHA gate_sha256=$GSHA allow_sha256=$(sha256sum $C/capture-secret-allow.tsv | cut -d' ' -f1) base=$B"
fresh() {
  rm -rf "$S/$1"; git clone -q --shared "$L" "$S/$1" && git -C "$S/$1" checkout -q "$B"
  [ "$(git -C "$S/$1" rev-parse --show-toplevel)" = "$S/$1" ] || { echo "toplevel mismatch $1"; exit 3; }
}
place() {  # place DIR [scanner] [allow] [row]
  local d=$1 scan=${2:-$C/capture-secret-scan.py} allow=${3:-$C/capture-secret-allow.tsv} row=${4-$ROW}
  cp "$scan" "$d/corpus/instruments/capture-secret-scan.py"
  cp "$allow" "$d/corpus/instruments/capture-secret-allow.tsv"
  mkdir -p "$d/corpus/source-snapshots/round-87"
  cp $L/corpus/source-snapshots/round-87/{S124.txt,S125.txt,manifest.json} "$d/corpus/source-snapshots/round-87/"
  if [ -n "$row" ]; then python3 - "$d/SCORECARD.md" "$row" <<'PY'
import sys
p, row = sys.argv[1], sys.argv[2]
t = open(p).read()
anchor = "| priced-claim-package |"
i = t.index(anchor); j = t.index("\n", i)
open(p, "w").write(t[: j + 1] + row + "\n" + t[j + 1:])
PY
  fi
}
commit() { git -C "$1" add -A && git -C "$1" -c user.name=fixture -c user.email=fixture@invalid commit -q -m control; }
check() { python3 -B $W/c2/capability-check.py --lane "$1" --rev HEAD --work "$S/w" --instrument-sha256 "${2:-$ISHA}" --gate-sha256 "$GSHA"; echo "rc=$?"; }
mutant() {  # mutant NAME python-replace-old python-replace-new
  python3 - "$C/capture-secret-scan.py" "$S/$1.py" "$2" "$3" <<'PY'
import sys
s = open(sys.argv[1]).read(); old, new = sys.argv[3], sys.argv[4]
assert old in s, old
open(sys.argv[2], "w").write(s.replace(old, new))
PY
}
fresh dn; echo "== control do-nothing: base, no instrument (expected fail)"; check "$S/dn"
fresh pos; place "$S/pos"; commit "$S/pos"; echo "== control positive: candidate placed (expected pass)"; check "$S/pos"
mutant always0 '    rc = 1 if hits else 0' '    rc = 0; hits = 0; files = 0'
fresh a0; place "$S/a0" "$S/always0.py"; commit "$S/a0"; echo "== forgery always-clean scanner (expected fail K2,K4)"; check "$S/a0" "$(sha256sum $S/always0.py | cut -d' ' -f1)"
mutant gateonly 'def patterns():
    return gate_patterns() + AWS_PATTERNS' 'def patterns():
    return gate_patterns()'
fresh go; place "$S/go" "$S/gateonly.py"; commit "$S/go"; echo "== forgery gate-only scanner, no AWS shapes (expected fail)"; check "$S/go" "$(sha256sum $S/gateonly.py | cut -d' ' -f1)"
mutant pathonly '            key = (path, name, hashlib.sha256(m.group(0)).hexdigest())
            if key in allow:' '            key = next((k for k in allow if k[0] == path and k[1] == name), None)
            if key is not None:'
fresh po; place "$S/po" "$S/pathonly.py"; commit "$S/po"; echo "== forgery allowlist bound to path+shape, not value (expected fail K4)"; check "$S/po" "$(sha256sum $S/pathonly.py | cut -d' ' -f1)"
mutant scopewide 'def is_capture_path(rel):
    parts = rel.split("/")' 'def is_capture_path(rel):
    if rel.startswith("corpus/"):
        return True
    parts = rel.split("/")'
fresh sa; place "$S/sa" "$S/scopewide.py"; commit "$S/sa"; echo "== forgery scope widened to all of corpus/ (expected fail K4)"; check "$S/sa" "$(sha256sum $S/scopewide.py | cut -d' ' -f1)"
mutant scopeall 'def is_capture_path(rel):
    parts = rel.split("/")' 'def is_capture_path(rel):
    return True
    parts = rel.split("/")'
fresh wt; place "$S/wt" "$S/scopeall.py"; commit "$S/wt"; echo "== forgery whole-tree scope, >16k blobs (expected fail K3/K4; also proves read_blobs no longer deadlocks past ~1,560 oids, the defect this control found in the first candidate)"; check "$S/wt" "$(sha256sum $S/scopeall.py | cut -d' ' -f1)"
mutant stsallow '                    or not HEX64.match(cells[2])' '                    and not HEX64.match(cells[2])'
fresh st; place "$S/st" "$S/stsallow.py"; commit "$S/st"; echo "== forgery allowlist refusal disabled (expected fail)"; check "$S/st" "$(sha256sum $S/stsallow.py | cut -d' ' -f1)"
: > "$S/empty-allow.tsv"
fresh na; place "$S/na" "$C/capture-secret-scan.py" "$S/empty-allow.tsv"; commit "$S/na"; echo "== control empty allowlist (expected fail K3)"; check "$S/na"
cp $C/capture-secret-allow.tsv "$S/stale-allow.tsv"; printf 'corpus/source-snapshots/round-1/none.txt\tcredential\t%064d\tstale row\n' 0 >> "$S/stale-allow.tsv"
fresh sl; place "$S/sl" "$C/capture-secret-scan.py" "$S/stale-allow.tsv"; commit "$S/sl"; echo "== control stale allowlist row (expected fail K3)"; check "$S/sl"
fresh nr; place "$S/nr" "$C/capture-secret-scan.py" "$C/capture-secret-allow.tsv" ""; commit "$S/nr"; echo "== control no SCORECARD row (expected fail K5)"; check "$S/nr"
echo "== control instrument sha pin: positive tree, wrong pin (expected fail K1)"; check "$S/pos" 0000000000000000000000000000000000000000000000000000000000000000
