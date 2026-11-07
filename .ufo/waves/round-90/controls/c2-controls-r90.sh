#!/usr/bin/env bash
# kasegi round-90 C2 pre-freeze controls. Inputs: lane object store at BASE (pinned), the frozen
# candidate and counter (wave files). Every forgery must FAIL the counter; the no-work control
# (BASE instrument) must FAIL; the candidate must PASS. Usage: c2-controls-r90.sh LANE BASE SCRATCH
set -u
L=$1; BASE=$2; S=$3; W=.ufo/waves/round-90
mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT
python3 -B "$L/$W/controls/c2-forgeries.py" "$L/$W/c2/candidate/capture-source.py" "$S/forge" || exit 2
run() { echo "== $1 (expect $2)"; shift 2; python3 -B "$L/$W/c2/capability-check.py" --lane "$L" --rev "$BASE" --base-rev "$BASE" --work "$S/w" --seed 9090 "$@"; echo "control_rc=$?"; }
run no-work FAIL
run candidate PASS --instrument "$L/$W/c2/candidate/capture-source.py"
for f in F1-blanket F2-partial F3-write-then-check F4-no-allow F5-fail-open F6-leaky; do run "$f" FAIL --instrument "$S/forge/$f.py"; done
