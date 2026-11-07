#!/usr/bin/env bash
# Round-88 C2 pre-freeze controls over the frozen counter c2/capability-check.py (r88 successor).
# Each control: a `git clone --shared` of the base under SCRATCH, the candidate (or a mutant)
# copied into corpus/instruments/, the candidate SCORECARD row applied (unless the control
# drops it), one fixture commit (identity fixture@invalid, toplevel asserted), then the counter.
# Mutant controls run WITHOUT --instrument-sha256 so the behavioral limbs must catch them.
# Usage: c2-controls-r88.sh SCRATCH_DIR
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$L/.ufo/waves/round-88
B=6beead9148945fa695cf3139e8fc9d8e91cc5fd0
C=$W/c2/candidate
S=${1:?scratch}; mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
ISHA=$(sha256sum $C/capture-secret-scan.py | cut -d' ' -f1)
GSHA=$(sha256sum $L/corpus/instruments/claim-package-check.py | cut -d' ' -f1)
echo "counter_sha256=$(sha256sum $W/c2/capability-check.py | cut -d' ' -f1) candidate_sha256=$ISHA allow_sha256=$(sha256sum $C/capture-secret-allow.tsv | cut -d' ' -f1) row_sha256=$(sha256sum $C/scorecard-row.txt | cut -d' ' -f1) gate_sha256=$GSHA base=$B"
# build NAME MUTATION_PY ROW(yes|no) INSTRUMENT_SRC
build() {
  local d="$S/$1"; rm -rf "$d"
  git clone -q --shared "$L" "$d" && git -C "$d" checkout -q "$B"
  [ "$(git -C "$d" rev-parse --show-toplevel)" = "$d" ] || { echo "toplevel mismatch"; exit 2; }
  cp "${4:-$C/capture-secret-scan.py}" "$d/corpus/instruments/capture-secret-scan.py"
  cp "$C/capture-secret-allow.tsv" "$d/corpus/instruments/capture-secret-allow.tsv"
  if [ -n "$2" ]; then python3 - "$d/corpus/instruments/capture-secret-scan.py" "$2" <<'PY'
import sys
p, spec = sys.argv[1], sys.argv[2]
a, b = spec.split("=>", 1)
s = open(p).read(); assert s.count(a) == 1, (a, s.count(a)); open(p, "w").write(s.replace(a, b))
PY
  fi
  if [ "$3" = yes ]; then python3 - "$d/SCORECARD.md" "$C/scorecard-row.txt" <<'PY'
import sys
p, r = sys.argv[1], open(sys.argv[2]).read()
L = open(p).read().split("\n"); i = [k for k, l in enumerate(L) if l.startswith("| capture-secret-scan |")]; assert len(i) == 1
L[i[0]] = r.rstrip("\n"); open(p, "w").write("\n".join(L))
PY
  fi
  git -C "$d" -c user.name=fixture -c user.email=fixture@invalid commit -qam "control $1"
}
count() { python3 -B $W/c2/capability-check.py --lane "$S/$1" --rev HEAD --work "$S/w" "${@:2}"; echo "rc=$?"; }
echo "== control do-nothing: base revision as landing (expected fail K1 sha, K4, K5, K6)"
python3 -B $W/c2/capability-check.py --lane $L --rev $B --work "$S/w" --instrument-sha256 $ISHA --gate-sha256 $GSHA; echo "rc=$?"
build pos "" yes; echo "== control positive: frozen candidate + row, pinned (expected pass)"; count pos --instrument-sha256 $ISHA --gate-sha256 $GSHA
build wrongsha "" yes; echo "== control wrong-pin: positive tree, wrong instrument sha (expected fail K1)"; count wrongsha --instrument-sha256 $(printf '0%.0s' {1..64}) --gate-sha256 $GSHA
build norow "" no; echo "== control no-row: candidate without the SCORECARD row update (expected fail K5)"; count norow
build r87 "" yes "$L/corpus/instruments/capture-secret-scan.py"; echo "== control r87-instrument: base instrument as candidate (expected fail K4; K6 reads the BASE instrument, so it passes by construction)"; count r87
build noscope 'parts[:2] == ["corpus", "practice"] and parts[3] == "evidence"=>False' yes; echo "== control no-practice-scope (expected fail K4, files limb unaffected)"; count noscope
build nogcs '[0-9a-f]{64,}")),=>(?!)")),' yes; echo "== control gcs-pattern-disabled (expected fail K4 missing S004)"; count nogcs
build loosesas 'rb"(?i)(?<![A-Za-z0-9_])(?:" + _SV + _PARAM + _SEP + _SIG + rb"|" + _SIG + _PARAM + _SEP + _SV + rb")"=>rb"(?i)(?<![A-Za-z0-9_])" + _SIG' yes; echo "== control sas-without-sv-context (expected fail K4 extra S007)"; count loosesas
build nojsonsep '_SEP = rb"(?:&amp;|&|\\u0026)"=>_SEP = rb"(?:&amp;|&)"' yes; echo "== control sas-json-separator-dropped (expected fail K4 missing live-c.json)"; count nojsonsep
build shortgcs '[0-9a-f]{64,}=>[0-9a-f]{12,}' yes; echo "== control gcs-threshold-12 (expected fail K4 extra S005 doc example)"; count shortgcs
build filesclean '    return report("files", results, len(paths), allowed, len(set(allow) - used))=>    return report("files", [], len(paths), allowed, len(set(allow) - used))' yes; echo "== control files-mode-blind (expected fail K4 files limb)"; count filesclean
build stsallow 'NEVER_ALLOWED = frozenset({"aws-sts-session-token"})=>NEVER_ALLOWED = frozenset()' yes; echo "== control sts-allow-row-accepted (expected fail K4 sts_allow_rc)"; count stsallow
build alwaysclean '    rc = 1 if hits else 0=>    rc = 0; hits = 0' yes; echo "== control always-clean (expected fail K2, K4)"; count alwaysclean
