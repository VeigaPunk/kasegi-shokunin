#!/usr/bin/env bash
# Round-89 C2 pre-freeze controls over the frozen counter c2/capability-check.py (r89 successor).
# Each control: a `git clone --shared` of the base under SCRATCH, the round-89 snapshots copied in
# (they land in the freeze commit, before any landing), the candidate (or a mutant) copied into
# corpus/instruments/, the candidate SCORECARD row applied (unless the control drops it), one
# fixture commit (identity fixture@invalid, toplevel asserted), then the counter with a fixed seed.
# Mutant controls run WITHOUT --instrument-sha256 so the behavioral limbs must catch them. A mutant that
# stops matching the snapshots' documentation example also fails K3 (its two allowlist rows go unused).
# Usage: c2-controls-r89.sh SCRATCH_DIR
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$L/.ufo/waves/round-89
B=090a46f89932324787e00ca20b1007f893934c9a
C=$W/c2/candidate
SNAP=$L/corpus/source-snapshots/round-89
SEED=8989
S=${1:?scratch}; mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
ISHA=$(sha256sum $C/capture-secret-scan.py | cut -d' ' -f1)
GSHA=$(sha256sum $L/corpus/instruments/claim-package-check.py | cut -d' ' -f1)
echo "counter_sha256=$(sha256sum $W/c2/capability-check.py | cut -d' ' -f1) candidate_sha256=$ISHA allow_sha256=$(sha256sum $C/capture-secret-allow.tsv | cut -d' ' -f1) row_sha256=$(sha256sum $C/scorecard-row.txt | cut -d' ' -f1) gate_sha256=$GSHA base=$B seed=$SEED"
# build NAME MUTATION(a=>b or empty) ROW(yes|no) INSTRUMENT_SRC ALLOW_SRC
build() {
  local d="$S/$1"; rm -rf "$d"
  git clone -q --shared "$L" "$d" && git -C "$d" checkout -q "$B"
  [ "$(git -C "$d" rev-parse --show-toplevel)" = "$d" ] || { echo "toplevel mismatch"; exit 2; }
  mkdir -p "$d/corpus/source-snapshots/round-89" && cp "$SNAP"/* "$d/corpus/source-snapshots/round-89/"
  cp "${4:-$C/capture-secret-scan.py}" "$d/corpus/instruments/capture-secret-scan.py"
  cp "${5:-$C/capture-secret-allow.tsv}" "$d/corpus/instruments/capture-secret-allow.tsv"
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
  git -C "$d" add -A
  git -C "$d" -c user.name=fixture -c user.email=fixture@invalid commit -qm "control $1"
}
count() { python3 -B $W/c2/capability-check.py --lane "$S/$1" --rev HEAD --work "$S/w" --seed $SEED "${@:2}"; echo "rc=$?"; }
echo "== control do-nothing: base revision as landing (expected fail K1 sha, K4, K5, K7, K8; K6 reads the base instrument and passes by construction)"
python3 -B $W/c2/capability-check.py --lane $L --rev $B --work "$S/w" --seed $SEED --instrument-sha256 $ISHA --gate-sha256 $GSHA; echo "rc=$?"
build pos "" yes; echo "== control positive: frozen candidate + allowlist + row, pinned (expected pass)"; count pos --instrument-sha256 $ISHA --gate-sha256 $GSHA
echo "== control positive, second seed 1 (expected pass)"; python3 -B $W/c2/capability-check.py --lane "$S/pos" --rev HEAD --work "$S/w" --seed 1 --instrument-sha256 $ISHA --gate-sha256 $GSHA; echo "rc=$?"
build wrongsha "" yes; echo "== control wrong-pin: positive tree, wrong instrument sha (expected fail K1)"; count wrongsha --instrument-sha256 $(printf '0%.0s' {1..64}) --gate-sha256 $GSHA
build norow "" no; echo "== control no-row: candidate without the SCORECARD row update (expected fail K5)"; count norow
build noallow "" yes "" "$L/corpus/instruments/capture-secret-allow.tsv"; echo "== control no-allow-rows: candidate without the two doc-example allowlist rows (expected fail K3: the snapshots' AWS example signature is a hit)"; count noallow
build r88 "" yes "$L/corpus/instruments/capture-secret-scan.py"; echo "== control r88-instrument: base instrument as candidate (unpinned; its own selftest passes, so expected fail K3 unused allow rows, K4, K7, K8)"; count r88
build cfoff '_CF_LB + rb"(?:" + _CF_SIG=>rb"(?!)" + rb"(?:" + _CF_SIG' yes; echo "== control cloudfront-pattern-never-matches (expected fail K1 selftest, K4, K7, K8)"; count cfoff
build cfnokpi '_CF_LB + rb"(?:" + _CF_SIG + _CF_PARAM + _SEP + _CF_KPI + rb"|" + _CF_KPI + _CF_PARAM + _SEP + _CF_SIG + rb")"=>_CF_LB + _CF_SIG' yes; echo "== control cloudfront-without-key-pair-id-context (expected fail K4 extra S012, K7 extra n1, K8)"; count cfnokpi
build cfdash '_CF_LB = rb"(?:(?<![A-Za-z0-9_-])=>_CF_LB = rb"(?:(?<![A-Za-z0-9_])' yes; echo "== control cloudfront-left-boundary-admits-dash (expected fail K4 extra S011, K8)"; count cfdash
build cfcase '        _CF_LB + rb"(?:" + _CF_SIG=>        rb"(?i)" + _CF_LB + rb"(?:" + _CF_SIG' yes; echo "== control cloudfront-case-insensitive (expected fail K7 extra n2)"; count cfcase
build cffloor '_CF_SIG = rb"Signature=[A-Za-z0-9_~-]{40,}"=>_CF_SIG = rb"Signature=[A-Za-z0-9_~-]{12,}"' yes; echo "== control cloudfront-floor-12 (expected fail K4 extra S013, K8)"; count cffloor
build nojsonsep '_SEP = rb"(?:&amp;|&|\\u0026)"=>_SEP = rb"(?:&amp;|&)"' yes; echo "== control json-separator-dropped (expected fail K4 missing live-d, live-c, E3; K7; K8)"; count nojsonsep
build nolb '_LB = rb"(?:(?<![A-Za-z0-9_])|(?<=\\u0026)|(?<=%26))"=>_LB = rb"(?<![A-Za-z0-9_])"' yes; echo "== control azure-u0026-boundary-reverted (r88 F1; expected fail K4 missing E3, K7 missing g3, K8)"; count nolb
build literal '        _CF_LB + rb"(?:" + _CF_SIG + _CF_PARAM + _SEP + _CF_KPI + rb"|" + _CF_KPI + _CF_PARAM + _SEP + _CF_SIG + rb")")),=>        rb"PLANTEDcfSIGNATURE[^&\\\\]*(?:&amp;|&|\\\\u0026)Key-Pair-Id=K2PLANTEDFIXT9|Key-Pair-Id=K2PLANTEDFIXT9.{0,80}?Signature=PLANTEDcfSIGNATURE|FAKEcfSIGNATUREfake[^&]*&(?:amp;)?Key-Pair-Id|Key-Pair-Id=K2JCJMDEHXQW5F.{0,80}?Signature=FAKEcf|Signature=nitfHRC[A-Za-z0-9_~-]+&Key-Pair-Id=K2JCJMDEHXQW5F")),' yes; echo "== control fixture-literal-detector (r88 CriticClaims D4; expected fail K7 only)"; count literal
build alwaysclean '    rc = 1 if hits else 0=>    rc = 0; hits = 0' yes; echo "== control always-clean (expected fail K2, K4, K7)"; count alwaysclean
