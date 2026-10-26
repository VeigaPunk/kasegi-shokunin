#!/usr/bin/env bash
# r-defect-closure.sh — C1 closure counter for the nine round-33 verifier-routed
# defects R1-R9 (`corpus/lessons/round-33-verifier-spotcheck.md` §5).
#
# Usage:
#   bash corpus/instruments/r-defect-closure.sh
#       Plain run against this lane's working tree (the root is derived from this
#       script's own location, so it works from any cwd).
#   bash corpus/instruments/r-defect-closure.sh --root DIR
#       Same nine checks against another tree (e.g. a `git archive 014ee2d`
#       extraction): the base-bytes run must print `closed=0/9 exit=1`.
#   bash corpus/instruments/r-defect-closure.sh --selftest [--scratch DIR]
#       For each check: run it on the live tree (must pass) and on a scratch
#       fixture copy of only the files that check reads, with that one defect
#       reintroduced (must fail). Where a check has a positive control (R8:
#       the `+00:00` and fractional-second stamps rule C accepts) that fixture
#       must be accepted too. Prints one `selftest case=R# live=... fixture=...
#       control=... verdict=...` line per check plus
#       `selftest cases=9 failures=0`; exit 0 only when every live run passes,
#       every broken fixture is rejected and every control is accepted.
#
# Closure semantics: each check exits 0 when its defect is CLOSED and non-zero
# while it is still OPEN. The plain run prints one `R# check=... open=0|1` line
# per check and `closed=K/9 exit=0|1`; exit 0 only for K=9.
#
# Do-nothing control and the discriminator (C1). `.ufo/waves/round-34/
# c1-controls/fake-suite.sh` prints the same `closed=9/9 exit=0` line and, for
# `--selftest`, a bare `cases=9 failures=0` — it performs no check at all. The
# discriminator is the per-case evidence: this suite prints exactly nine
# `selftest case=R# live=... fixture=... control=... verdict=...` lines, produced
# by running each check twice (live tree + defect fixture) plus a control where
# one exists, and a case counts as a pass only if the live run exits 0, the
# defect fixture is rejected and the control is accepted.
#
# The suite then judges its own report instead of trusting it: `report_ok` and
# `plain_report_ok` re-parse the captured output and require the nine named
# lines (distinct ids R1..R9) and a summary consistent with them. `--selftest`
# additionally proves that judgement on two forged reports — a summary alone and
# a nine-case report short one case — and prints `selftest judge=forged-summary
# rejected=1`, `selftest judge=short-report rejected=1`,
# `selftest judge=complete-report accepted=1`. A mutant that replaces the
# selftest body with `printf 'selftest cases=9 failures=0'` therefore exits 1
# with `selftest problem=self-report cases=0 expected=9`; the same forgery of the
# plain run exits 1 with `suite problem=self-report plain-lines=0 expected=9`.
# A summary line alone cannot satisfy any of that: the fake suite has no case
# table, so it cannot emit a case line, and it cannot exhibit a check that fails
# on a defect-bearing tree. The base tree (all nine defects open) reads
# `closed=0/9`; a summary-only printer reads `9/9` on base bytes too.
#
# Read-only: every check only reads files under the root; the only writes are
# the scratch fixtures this script creates under `--selftest` (default base
# $HYAKU_SCRATCH, else $TMPDIR, else /tmp), removed on exit. No git command is
# run and nothing outside the scratch directory is written.
#
# The nine checks (one function each, `check_r1` .. `check_r9`):
#   R1  SCORECARD.md carries 0 literal LANE_HASH placeholders AND an appended
#       `Correction (round 34)` block naming 7963976e and 014ee2d.
#   R2  SCORECARD.md round-33 section carries the appended `Erratum 2` block
#       (kill-rule parenthetical restated per id: "0 or 2+", multi_row_url,
#       dup-id) AND corpus/QUALITY.md carries the R22 pre-freeze satisfiability
#       row.
#   R3  corpus/QUALITY.md carries the appended round-34 note below the R20 row
#       saying the per-id reading supersedes "exactly one registry-row URL".
#   R4  the tightened kill rule is recorded in prose (the corpus/QUALITY.md R24
#       row, or a SCORECARD.md paragraph, naming the kill rule and one
#       `selftest case=` verdict line per case)
#       AND corpus/lessons/round-33.md carries an appended round-34 erratum
#       correcting the "all mutants killed" overstatement to the measured
#       3-of-4-under-frozen-rule figure.
#   R5  corpus/instruments/capture-binding-check.py names no selftest case
#       `url-matching-two-rows` while still carrying >=11 case tuples.
#   R6  corpus/source-snapshots/round-26/manifest.json binds S040-live.txt (a
#       record path match or an explicit orphan list) AND its purpose text is
#       corrected (names S040, no longer says it was skipped).
#   R7  corpus/lessons/round-33.md carries the appended R7 erratum: 19 -> 31
#       characters, 23 -> 22 characters, and the S050.txt:70 sentence cite.
#   R8  every fetched_utc in corpus/source-snapshots/round-32/manifest.json
#       matches the frozen shape (^[0-9]{4}-[0-9]{2}-[0-9]{2}T.*Z$) or the
#       frozen `+00:00` alternative, AND parses as a real calendar instant at
#       UTC offset 0, and no non-zero offset. The accept set is
#       capture-binding rule C's (`Z`, `+00:00`, fractional seconds); the parse
#       removes the loose regex's false positives (a Z-suffixed non-instant is
#       not a UTC fetched instant).
#   R9  capture-binding-check.py carries the nine H4-H8 selftest case names,
#       frontier-recheck-count.py rule A is bidirectional (proved by two
#       fixtures: a mirror entry passes, an entry whose recheck selects an id
#       its header does not declare fails with exit 1), and the c2-controls junk
#       twin exists.
#
# Exit codes: 0 closed / selftest clean, 1 open defect(s) / selftest failure,
# 2 harness error (bad argument, unreadable root or scratch base).
set -uo pipefail

SELF=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
LANE_ROOT=$(cd -- "$SELF/../.." && pwd)
RD_ROOT=$LANE_ROOT
MODE=run
SCRATCH_ARG=

usage() {
  awk 'NR > 1 && /^set -uo pipefail/ { exit } NR > 1 { print }' "${BASH_SOURCE[0]}" \
    | sed -e 's/^# \{0,1\}//'
}

while [ $# -gt 0 ]; do
  case $1 in
    --root)
      [ $# -ge 2 ] || { echo "suite UNAVAILABLE reason=root-argument-missing"; exit 2; }
      if ! RD_ROOT=$(cd -- "$2" 2>/dev/null && pwd); then
        echo "suite UNAVAILABLE reason=root-missing root=$2"
        exit 2
      fi
      shift 2 ;;
    --selftest) MODE=selftest; shift ;;
    --scratch)
      [ $# -ge 2 ] || { echo "suite UNAVAILABLE reason=scratch-argument-missing"; exit 2; }
      SCRATCH_ARG=$2; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "suite UNAVAILABLE reason=unknown-argument arg=$1"; exit 2 ;;
  esac
done

# --- helpers -----------------------------------------------------------------

# block_from FILE REGEX: print from the first line matching REGEX up to (not
# including) the next blank line. Used for the appended prose blocks.
block_from() {
  awk -v pat="$2" '$0 ~ pat { f = 1 } f { print } f && /^[[:space:]]*$/ { exit }' "$1"
}

# para_grep FILE SUB1 SUB2 SUB3: exit 0 when one blank-line-separated paragraph
# contains all three substrings (case-insensitive substring match).
para_grep() {
  awk -v a="$2" -v b="$3" -v c="$4" '
    BEGIN { RS = "" }
    { t = tolower($0); if (index(t, a) > 0 && index(t, b) > 0 && index(t, c) > 0) found = 1 }
    END { exit(found ? 0 : 1) }
  ' "$1"
}

# --- R1 ----------------------------------------------------------------------

check_r1() {
  cd -- "${RD_ROOT:-$LANE_ROOT}" 2>/dev/null || { DESC="root unreadable"; return 1; }
  DESC="SCORECARD.md lane-hash-markers=0 + appended 'Correction (round 34)' naming 7963976e/014ee2d"
  local f=SCORECARD.md n block
  [ -f "$f" ] || { DESC="SCORECARD.md absent"; return 1; }
  n=$(grep -c '<LANE''_HASH>' "$f" 2>/dev/null || true)
  n=${n:-0}
  [ "$n" -eq 0 ] || { DESC="SCORECARD.md lane-hash-markers=$n"; return 1; }
  block=$(block_from "$f" 'Correction .round 34.')
  [ -n "$block" ] || { DESC="no appended 'Correction (round 34)' block"; return 1; }
  grep -q '7963976e' <<<"$block" || { DESC="correction block does not name 7963976e"; return 1; }
  grep -q '014ee2d' <<<"$block" || { DESC="correction block does not name 014ee2d"; return 1; }
  return 0
}

# --- R2 ----------------------------------------------------------------------

check_r2() {
  cd -- "${RD_ROOT:-$LANE_ROOT}" 2>/dev/null || { DESC="root unreadable"; return 1; }
  DESC="SCORECARD.md round-33 'Erratum 2' per-id restatement + QUALITY.md R22 pre-freeze step"
  local s=SCORECARD.md q=corpus/QUALITY.md sec errline block r22
  [ -f "$s" ] || { DESC="SCORECARD.md absent"; return 1; }
  [ -f "$q" ] || { DESC="corpus/QUALITY.md absent"; return 1; }
  sec=$(grep -n '^## Round 33' "$s" 2>/dev/null | head -1 | cut -d: -f1)
  sec=${sec:-0}
  errline=$(grep -ni 'erratum 2' "$s" 2>/dev/null | head -1 | cut -d: -f1)
  [ -n "$errline" ] || { DESC="no 'Erratum 2' block in SCORECARD.md"; return 1; }
  [ "$errline" -gt "$sec" ] || { DESC="'Erratum 2' not inside the round-33 section"; return 1; }
  block=$(block_from "$s" '[Ee]rratum 2')
  grep -q '0 or 2+' <<<"$block" || { DESC="erratum 2 does not restate the '0 or 2+' parenthetical"; return 1; }
  grep -Eq 'per[- ]id|own id scope' <<<"$block" || { DESC="erratum 2 does not state the per-id scope"; return 1; }
  grep -q 'multi_row_url' <<<"$block" || { DESC="erratum 2 does not name multi_row_url"; return 1; }
  grep -q 'dup-id' <<<"$block" || { DESC="erratum 2 does not name dup-id"; return 1; }
  r22=$(grep '^| R22 |' "$q" 2>/dev/null)
  [ -n "$r22" ] || { DESC="QUALITY.md R22 pre-freeze row absent"; return 1; }
  grep -qi 'satisfiab' <<<"$r22" || { DESC="R22 row does not state satisfiability"; return 1; }
  grep -Eqi 'before freeze|pre-freeze' <<<"$r22" || { DESC="R22 row does not state the pre-freeze step"; return 1; }
  return 0
}

# --- R3 ----------------------------------------------------------------------

check_r3() {
  cd -- "${RD_ROOT:-$LANE_ROOT}" 2>/dev/null || { DESC="root unreadable"; return 1; }
  DESC="QUALITY.md appended round-34 note below R20 (per-id supersedes 'exactly one')"
  local q=corpus/QUALITY.md r20 note block
  [ -f "$q" ] || { DESC="corpus/QUALITY.md absent"; return 1; }
  r20=$(grep -n '^| R20 |' "$q" 2>/dev/null | head -1 | cut -d: -f1)
  note=$(grep -ni 'note (round 34)' "$q" 2>/dev/null | head -1 | cut -d: -f1)
  [ -n "$r20" ] || { DESC="QUALITY.md R20 row absent"; return 1; }
  [ -n "$note" ] || { DESC="no appended 'Note (round 34)' below R20"; return 1; }
  [ "$note" -gt "$r20" ] || { DESC="round-34 note is not below the R20 row"; return 1; }
  block=$(block_from "$q" '[Nn]ote .round 34.')
  grep -q 'R20' <<<"$block" || { DESC="note does not name R20"; return 1; }
  grep -q 'exactly one' <<<"$block" || { DESC="note does not quote the superseded 'exactly one' reading"; return 1; }
  grep -qi 'supersed' <<<"$block" || { DESC="note does not say the reading is superseded"; return 1; }
  grep -Eq 'per-id|per id' <<<"$block" || { DESC="note does not give the per-id reading"; return 1; }
  return 0
}

# --- R4 ----------------------------------------------------------------------

check_r4() {
  cd -- "${RD_ROOT:-$LANE_ROOT}" 2>/dev/null || { DESC="root unreadable"; return 1; }
  DESC="tightened kill rule recorded (R24 row: kill rule + one 'selftest case=' line per case) + round-33 lesson R4 3-of-4 erratum"
  local l=corpus/lessons/round-33.md ok=1 rc
  # Limb 1: the tightened kill-rule requirement is on a record surface. Bind it
  # to the R24 row when that row exists (so the tokens cannot be spread across
  # the whole round-34 table), else to one SCORECARD paragraph (the claim allows
  # the scorecard section as the record surface).
  local q=corpus/QUALITY.md s=SCORECARD.md row
  row=""
  [ -f "$q" ] && row=$(grep '^| R24 |' "$q" 2>/dev/null)
  if [ -n "$row" ] && grep -qi 'kill rule' <<<"$row" \
     && grep -q 'selftest case=' <<<"$row" \
     && grep -Eqi 'per case|>= ?11' <<<"$row"; then
    ok=0
  fi
  if [ "$ok" -ne 0 ] && [ -f "$s" ] \
     && para_grep "$s" 'kill rule' 'selftest case=' 'per case'; then
    ok=0
  fi
  [ "$ok" -eq 0 ] || { DESC="tightened kill-rule requirement not recorded (QUALITY R24 row or a SCORECARD paragraph: kill rule + one 'selftest case=' line per case)"; return 1; }
  [ -f "$l" ] || { DESC="corpus/lessons/round-33.md absent"; return 1; }
  python3 - "$l" <<'PY'
import re
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as fh:
    lines = fh.read().splitlines()
anchor = next((i for i, line in enumerate(lines)
               if line.startswith("## Touched surfaces and provenance")), None)
marks = [i for i, line in enumerate(lines)
         if "Erratum (round 34)" in line and "R4" in line]
if not marks:
    print("no-r4-erratum")
    sys.exit(4)
if anchor is not None and marks[0] <= anchor:
    print("r4-erratum-not-appended")
    sys.exit(5)
tail = "\n".join(lines[marks[0]:])
if not re.search(r"3 of 4|3/4|three of four", tail):
    print("no-3-of-4-figure")
    sys.exit(6)
if "mutant" not in tail.lower():
    print("no-mutant-obligation")
    sys.exit(7)
if not re.search(r"all mutants killed|overstat", tail, re.IGNORECASE):
    print("no-overstatement-correction")
    sys.exit(8)
sys.exit(0)
PY
  rc=$?
  case $rc in
    0) return 0 ;;
    4) DESC="round-33 lesson has no appended R4 erratum"; return 1 ;;
    5) DESC="R4 erratum is not appended after the filed lesson"; return 1 ;;
    6) DESC="R4 erratum does not carry the measured 3-of-4 figure"; return 1 ;;
    7) DESC="R4 erratum does not name the mutant obligation"; return 1 ;;
    *) DESC="R4 erratum does not correct the 'all mutants killed' overstatement"; return 1 ;;
  esac
}

# --- R5 ----------------------------------------------------------------------

check_r5() {
  cd -- "${RD_ROOT:-$LANE_ROOT}" 2>/dev/null || { DESC="root unreadable"; return 1; }
  DESC="capture-binding-check.py has no 'url-matching-two-rows' case name and keeps >=11 cases"
  local f=corpus/instruments/capture-binding-check.py n cases
  [ -f "$f" ] || { DESC="capture-binding-check.py absent"; return 1; }
  n=$(grep -c 'url-matching-two-rows' "$f" 2>/dev/null || true)
  n=${n:-0}
  [ "$n" -eq 0 ] || { DESC="misnamed selftest case 'url-matching-two-rows' still present (count=$n)"; return 1; }
  cases=$(grep -cE '^[[:space:]]*\("[a-z0-9-]+",' "$f" 2>/dev/null || true)
  cases=${cases:-0}
  [ "$cases" -ge 11 ] || { DESC="case table shrank to $cases entries (<11)"; return 1; }
  DESC="capture-binding-check.py url-matching-two-rows=0 cases=$cases (>=11)"
  return 0
}

# --- R6 ----------------------------------------------------------------------

check_r6() {
  cd -- "${RD_ROOT:-$LANE_ROOT}" 2>/dev/null || { DESC="root unreadable"; return 1; }
  DESC="round-26 manifest binds S040-live.txt (record or orphan list) + purpose corrected"
  local m=corpus/source-snapshots/round-26/manifest.json rc
  [ -f "$m" ] || { DESC="round-26 manifest absent"; return 1; }
  python3 - "$m" <<'PY'
import json
import sys

path = sys.argv[1]
try:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
except Exception as exc:  # noqa: BLE001 - reported as a named finding below
    print("manifest-unreadable=%s" % exc)
    sys.exit(3)
target = "S040-live.txt"
records = [r for r in data.get("sources", []) if isinstance(r, dict)]
paths = [str(r.get("path", "")) for r in records]
has_record = any(p.endswith(target) for p in paths)
orphans = data.get("orphan", data.get("orphans", []))
if isinstance(orphans, str):
    orphans = [orphans]
has_orphan = any(target in str(o) for o in orphans)
purpose = str(data.get("purpose", ""))
if not (has_record or has_orphan):
    print("no-record-or-orphan")
    sys.exit(4)
if "S040" not in purpose or "skipped this round" in purpose:
    print("purpose-not-corrected")
    sys.exit(5)
sys.exit(0)
PY
  rc=$?
  case $rc in
    0) return 0 ;;
    4) DESC="round-26 manifest has no S040-live.txt record and no orphan list"; return 1 ;;
    5) DESC="round-26 manifest purpose still says S040 was skipped"; return 1 ;;
    *) DESC="round-26 manifest unreadable (exit=$rc)"; return 1 ;;
  esac
}

# --- R7 ----------------------------------------------------------------------

check_r7() {
  cd -- "${RD_ROOT:-$LANE_ROOT}" 2>/dev/null || { DESC="root unreadable"; return 1; }
  DESC="round-33 lesson appended R7 erratum (19->31, 23->22 characters, S050.txt:70)"
  local l=corpus/lessons/round-33.md rc
  [ -f "$l" ] || { DESC="corpus/lessons/round-33.md absent"; return 1; }
  python3 - "$l" <<'PY'
import re
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as fh:
    lines = fh.read().splitlines()
anchor = next((i for i, line in enumerate(lines)
               if line.startswith("## Touched surfaces and provenance")), None)
marks = [i for i, line in enumerate(lines)
         if "Erratum (round 34)" in line and "R7" in line]
if not marks:
    print("no-r7-erratum")
    sys.exit(4)
if anchor is not None and marks[0] <= anchor:
    print("r7-erratum-not-appended")
    sys.exit(5)
tail = "\n".join(lines[marks[0]:])
if not re.search(r"19\D{0,24}(?:->|\u2192|to)\D{0,8}31", tail):
    print("no-19-to-31")
    sys.exit(6)
if not re.search(r"23\D{0,24}(?:->|\u2192|to)\D{0,8}22", tail):
    print("no-23-to-22")
    sys.exit(7)
if "S050.txt:70" not in tail:
    print("no-S050-line-70")
    sys.exit(8)
sys.exit(0)
PY
  rc=$?
  case $rc in
    0) return 0 ;;
    4) DESC="round-33 lesson has no appended R7 erratum"; return 1 ;;
    5) DESC="R7 erratum is not appended after the filed lesson"; return 1 ;;
    6) DESC="R7 erratum does not correct the 19-character count to 31"; return 1 ;;
    7) DESC="R7 erratum does not correct the 23-character count to 22"; return 1 ;;
    *) DESC="R7 erratum does not cite the S050.txt:70 sentence"; return 1 ;;
  esac
}

# --- R8 ----------------------------------------------------------------------

check_r8() {
  cd -- "${RD_ROOT:-$LANE_ROOT}" 2>/dev/null || { DESC="root unreadable"; return 1; }
  DESC="round-32 manifest fetched_utc is a real strict-UTC instant (date-T time Z, zero offset), no '-' offset"
  local m=corpus/source-snapshots/round-32/manifest.json rc
  [ -f "$m" ] || { DESC="round-32 manifest absent"; return 1; }
  python3 - "$m" <<'PY'
import datetime
import json
import re
import sys

path = sys.argv[1]
try:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
except Exception as exc:  # noqa: BLE001 - reported as a named finding below
    print("manifest-unreadable=%s" % exc)
    sys.exit(3)
# Shape floor: everything this check accepts also matches the frozen predicate
# `^[0-9]{4}-[0-9]{2}-[0-9]{2}T.*Z$` or its frozen `+00:00` alternative. This
# check then removes the loose regex's false positives: a Z-suffixed string
# that is not a calendar instant (`2026-10-25Tgarbage-not-a-timeZ`) is not a UTC
# fetched instant. A `+00:00` suffix is UTC, so it is normalised to `Z` before
# the shape test, matching capture-binding rule C's accept set.
shaped = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?Z$")
offset = re.compile(r"[+-][0-9]{2}:?[0-9]{2}")

def strict_utc(value):
    text = str(value).strip()
    if text.endswith("+00:00"):
        text = text[:-6] + "Z"
    if not shaped.match(text) or offset.search(text):
        return False
    try:
        stamp = datetime.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return False
    return stamp.utcoffset() == datetime.timedelta(0)

records = [r for r in data.get("sources", []) if isinstance(r, dict)]
values = [(str(r.get("id", "?")), r.get("fetched_utc")) for r in records if "fetched_utc" in r]
if not values:
    print("no-fetched_utc")
    sys.exit(4)
bad = ["%s:%s" % (rid, val) for rid, val in values if not strict_utc(val)]
if bad:
    print("non-strict-utc=" + ",".join(bad))
    sys.exit(5)
print("strict-utc-ok=%d" % len(values))
sys.exit(0)
PY
  rc=$?
  case $rc in
    0) return 0 ;;
    4) DESC="round-32 manifest carries no fetched_utc record"; return 1 ;;
    5) DESC="round-32 manifest carries a fetched_utc that is not a strict-UTC instant"; return 1 ;;
    *) DESC="round-32 manifest unreadable (exit=$rc)"; return 1 ;;
  esac
}

# --- R9 ----------------------------------------------------------------------

check_r9() {
  cd -- "${RD_ROOT:-$LANE_ROOT}" 2>/dev/null || { DESC="root unreadable"; return 1; }
  DESC="capture-binding H4-H8 cases + frontier rule A bidirectional + c2-controls junk twin"
  local f=corpus/instruments/capture-binding-check.py g=corpus/instruments/frontier-recheck-count.py
  local name missing="" junk tmp base mirror reverse rc_mirror rc_reverse
  [ -f "$f" ] || { DESC="capture-binding-check.py absent"; return 1; }
  for name in per-file-orphan-detected per-file-orphan-listed nested-snapshot-dir \
              fetched-utc-pending-rejected fetched-utc-local-offset-rejected \
              dup-record-in-manifest double-https-row rejected-row-anchor \
              summary-only-selftest-rejected; do
    grep -q -- "\"$name\"" "$f" || missing="$missing $name"
  done
  [ -z "$missing" ] || { DESC="capture-binding H4-H8 cases missing:$missing"; return 1; }
  [ -f "$g" ] || { DESC="frontier-recheck-count.py absent"; return 1; }
  junk=""
  for name in c2-controls/junk-f17.md .ufo/waves/round-34/c2-controls/junk-f17.md; do
    [ -f "$name" ] && junk=$name
  done
  [ -n "$junk" ] || { DESC="c2-controls/junk-f17.md absent"; return 1; }
  # Rule A bidirectional, proved behaviourally: a mirror entry (recheck ids ==
  # header ids) must pass; an entry whose recheck line selects an id its header
  # does not declare must fail with exit 1. A one-directional rule A passes both.
  tmp=$(mktemp -d "${TMPDIR:-/tmp}/rdc-r9.XXXXXX") || { DESC="mktemp failed"; return 1; }
  base=$tmp/base
  mkdir -p "$base/corpus/knowledge" "$base/corpus/source-snapshots/round-99" "$base/corpus/instruments"
  printf '| F99 | Reverse-binding fixture | admitted | `knowledge/r9-fixture.md` |\n' \
    >"$base/corpus/README.md"
  printf '#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n' \
    >"$base/corpus/instruments/source-recheck.py"
  printf '{"schema_version": 1, "sources": [{"id": "S001", "path": "S001.txt"}, {"id": "S002", "path": "S002.txt"}]}\n' \
    >"$base/corpus/source-snapshots/round-99/manifest.json"
  mirror=$tmp/mirror
  reverse=$tmp/reverse
  cp -a "$base" "$mirror"
  cp -a "$base" "$reverse"
  printf 'source: S001\nrecheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-99/manifest.json --source S001\n\nMirror fixture: this body cites S001 in prose, and header and recheck agree.\n' \
    >"$mirror/corpus/knowledge/r9-fixture.md"
  printf 'source: S001\nrecheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-99/manifest.json --source S001 --source S002\n\nReverse fixture: this body cites S001 and S002 in prose; the header declares S001 only.\n' \
    >"$reverse/corpus/knowledge/r9-fixture.md"
  python3 "$g" --root "$mirror" >/dev/null 2>&1
  rc_mirror=$?
  python3 "$g" --root "$reverse" >/dev/null 2>&1
  rc_reverse=$?
  rm -rf -- "$tmp"
  [ "$rc_mirror" -eq 0 ] || { DESC="frontier rule A control fixture failed (exit=$rc_mirror)"; return 1; }
  [ "$rc_reverse" -eq 1 ] || { DESC="frontier rule A not bidirectional (reverse fixture exit=$rc_reverse, want 1)"; return 1; }
  DESC="capture-binding H4-H8 cases=9 + frontier rule A bidirectional (mirror=0 reverse=1) + junk=$junk"
  return 0
}

# --- driver ------------------------------------------------------------------

CHECK_IDS=(R1 R2 R3 R4 R5 R6 R7 R8 R9)
CHECK_FNS=(check_r1 check_r2 check_r3 check_r4 check_r5 check_r6 check_r7 check_r8 check_r9)

run_check_once() { # ROOT FN -> sets DESC, returns the check status
  local root=$1 fn=$2
  DESC=""
  RD_ROOT=$root
  "$fn" >/dev/null
  return $?
}

run_plain() {
  local i id open closed=0 rc
  for i in "${!CHECK_IDS[@]}"; do
    id=${CHECK_IDS[$i]}
    run_check_once "$RD_ROOT" "${CHECK_FNS[$i]}"
    rc=$?
    if [ "$rc" -eq 0 ]; then
      open=0
      closed=$((closed + 1))
    else
      open=1
    fi
    printf '%s check=%s open=%d\n' "$id" "${DESC:-undescribed}" "$open"
  done
  if [ "$closed" -eq 9 ]; then
    printf 'closed=9/9 exit=0\n'
    return 0
  fi
  printf 'closed=%d/9 exit=1\n' "$closed"
  return 1
}

# report_ok REPORT: exit 0 only for the complete nine-case evidence form this
# suite's own run produces. The suite judges its own report: a summary-only (or
# short) report is not a pass whatever its summary line says — the rule the suite
# applies to other counters (QUALITY R24) applies to itself.
report_ok() {
  local report=$1 ids lines
  lines=$(printf '%s\n' "$report" \
    | grep -c '^selftest case=R[1-9] live=pass fixture=rejected control=\(pass\|absent\) verdict=pass$' || true)
  [ "${lines:-0}" -eq 9 ] || return 1
  ids=$(printf '%s\n' "$report" | sed -n 's/^selftest case=\(R[1-9]\) .*/\1/p' | sort | tr '\n' ' ')
  [ "$ids" = "R1 R2 R3 R4 R5 R6 R7 R8 R9 " ] || return 1
  printf '%s\n' "$report" | grep -qx 'selftest cases=9 failures=0'
}

# plain_report_ok REPORT: same judgement for the plain run — nine named check
# lines, one per defect id, and a summary that agrees with their open counts.
plain_report_ok() {
  local report=$1 ids lines closed
  lines=$(printf '%s\n' "$report" | grep -c '^R[1-9] check=.* open=[01]$' || true)
  [ "${lines:-0}" -eq 9 ] || return 1
  ids=$(printf '%s\n' "$report" | sed -n 's/^\(R[1-9]\) check=.*/\1/p' | sort | tr '\n' ' ')
  [ "$ids" = "R1 R2 R3 R4 R5 R6 R7 R8 R9 " ] || return 1
  closed=$(printf '%s\n' "$report" | grep -c ' open=0$' || true)
  closed=${closed:-0}
  if [ "$closed" -eq 9 ]; then
    printf '%s\n' "$report" | grep -qx 'closed=9/9 exit=0'
  else
    printf '%s\n' "$report" | grep -qx "closed=${closed}/9 exit=1"
  fi
}

# judge_selftest_report REPORT STATUS: the suite's judgement of its own selftest
# output. It proves its discriminator twice on forged reports (a summary alone,
# a nine-case report short one case) and then requires the real report to carry
# all nine case verdict lines. A run that forges `cases=9 failures=0` therefore
# fails here with `selftest problem=self-report`, not a pass.
judge_selftest_report() {
  local report=$1 status=$2 short="" n
  for n in 1 2 3 4 5 6 7 8; do
    short+="selftest case=R$n live=pass fixture=rejected control=absent verdict=pass"$'\n'
  done
  short+="selftest cases=9 failures=0"
  if report_ok 'selftest cases=9 failures=0'; then
    printf 'selftest problem=self-report forged-summary accepted\n'
    return 1
  fi
  printf 'selftest judge=forged-summary rejected=1\n'
  if report_ok "$short"; then
    printf 'selftest problem=self-report short-report accepted\n'
    return 1
  fi
  printf 'selftest judge=short-report rejected=1\n'
  if [ "$status" -ne 0 ]; then
    printf 'selftest problem=self-report status=%d\n' "$status"
    return 1
  fi
  if ! report_ok "$report"; then
    printf 'selftest problem=self-report cases=%s expected=9\n' \
      "$(printf '%s\n' "$report" | grep -c '^selftest case=' || true)"
    return 1
  fi
  printf 'selftest judge=complete-report accepted=1\n'
  return 0
}

# copy_into DEST REL [REL...]: copy the named lane files into the fixture tree.
copy_into() {
  local dest=$1 rel
  shift
  for rel in "$@"; do
    if [ ! -f "$LANE_ROOT/$rel" ]; then
      echo "selftest problem=fixture-source-missing path=$rel" >&2
      return 1
    fi
    mkdir -p "$dest/$(dirname -- "$rel")"
    cp -p "$LANE_ROOT/$rel" "$dest/$rel"
  done
  return 0
}

# filter_out FILE REGEX: drop matching lines in place (fixture trees only).
filter_out() {
  local f=$1 pat=$2
  grep -v -E -- "$pat" "$f" >"$f.tmp" || true
  mv "$f.tmp" "$f"
}

# build_broken_fixture ID DEST: a scratch tree holding only the files that check
# reads, with that check's round-33 defect reintroduced.
build_broken_fixture() {
  local id=$1 dest=$2
  mkdir -p "$dest"
  case $id in
    R1)
      copy_into "$dest" SCORECARD.md || return 1
      printf '\nFixture defect R1 (reintroduced): the lane-hash placeholder %s is back.\n' \
        '<LANE''_HASH>' >>"$dest/SCORECARD.md"
      ;;
    R2)
      copy_into "$dest" SCORECARD.md corpus/QUALITY.md || return 1
      filter_out "$dest/SCORECARD.md" '[Ee]rratum 2'
      filter_out "$dest/corpus/QUALITY.md" '^\| R22 \|'
      ;;
    R3)
      copy_into "$dest" corpus/QUALITY.md || return 1
      filter_out "$dest/corpus/QUALITY.md" '[Nn]ote \(round 34\)'
      ;;
    R4)
      copy_into "$dest" corpus/QUALITY.md SCORECARD.md corpus/lessons/round-33.md || return 1
      filter_out "$dest/corpus/QUALITY.md" 'selftest case='
      filter_out "$dest/SCORECARD.md" 'selftest case='
      filter_out "$dest/corpus/lessons/round-33.md" 'Erratum \(round 34\)|3 of 4|3/4|three of four'
      ;;
    R5)
      copy_into "$dest" corpus/instruments/capture-binding-check.py || return 1
      sed -E -i 's/\("[^"]+", case_duplicate_id_rows/("url-matching-two-rows", case_duplicate_id_rows/' \
        "$dest/corpus/instruments/capture-binding-check.py"
      if ! grep -q 'url-matching-two-rows' "$dest/corpus/instruments/capture-binding-check.py"; then
        sed -E -i 's/shared-url-between-two-records/url-matching-two-rows/' \
          "$dest/corpus/instruments/capture-binding-check.py"
      fi
      grep -q 'url-matching-two-rows' "$dest/corpus/instruments/capture-binding-check.py" || {
        echo "selftest problem=fixture-build R5 could not reintroduce the case name" >&2
        return 1
      }
      ;;
    R6)
      copy_into "$dest" corpus/source-snapshots/round-26/manifest.json || return 1
      python3 - "$dest/corpus/source-snapshots/round-26/manifest.json" <<'PY'
import json
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as fh:
    data = json.load(fh)
data["sources"] = [r for r in data.get("sources", [])
                   if not str(r.get("path", "")).endswith("S040-live.txt")]
for key in ("orphan", "orphans"):
    data.pop(key, None)
data["purpose"] = ("S040-live.txt was not present in corpus/source-snapshots/round-26/ "
                   "at manifest build time (ScoutS040Probe fetch not landed), so S040 "
                   "is skipped this round.")
with open(path, "w", encoding="utf-8") as fh:
    json.dump(data, fh, indent=1)
    fh.write("\n")
PY
      ;;
    R7)
      copy_into "$dest" corpus/lessons/round-33.md || return 1
      filter_out "$dest/corpus/lessons/round-33.md" 'S050\.txt:70|19 characters|23 characters'
      ;;
    R8)
      # Sharpest form of the round-33 defect: a value the frozen loose shape
      # regex (`^[0-9]{4}-[0-9]{2}-[0-9]{2}T.*Z$`) accepts but which is not a
      # calendar instant. A regex-only checker reads this fixture closed, so
      # this case proves the parse limb is load-bearing. The original offset
      # value (`2026-10-25T23:14:00-03:00`) is exercised by the base-tree run.
      copy_into "$dest" corpus/source-snapshots/round-32/manifest.json || return 1
      python3 - "$dest/corpus/source-snapshots/round-32/manifest.json" <<'PY'
import json
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as fh:
    data = json.load(fh)
for record in data.get("sources", []):
    if isinstance(record, dict) and "fetched_utc" in record:
        record["fetched_utc"] = "2026-10-25Tgarbage-not-a-timeZ"
with open(path, "w", encoding="utf-8") as fh:
    json.dump(data, fh, indent=1)
    fh.write("\n")
PY
      ;;
    R9)
      copy_into "$dest" corpus/instruments/capture-binding-check.py \
        corpus/instruments/frontier-recheck-count.py || return 1
      local j
      for j in c2-controls/junk-f17.md .ufo/waves/round-34/c2-controls/junk-f17.md; do
        if [ -f "$LANE_ROOT/$j" ]; then
          mkdir -p "$dest/$(dirname -- "$j")"
          cp -p "$LANE_ROOT/$j" "$dest/$j"
        fi
      done
      filter_out "$dest/corpus/instruments/capture-binding-check.py" 'nested-snapshot-dir'
      ;;
    *)
      echo "selftest problem=unknown-case id=$id" >&2
      return 1
      ;;
  esac
  return 0
}

# build_control_fixture ID DEST: a fixture holding a value class the check must
# ACCEPT (the mirror of build_broken_fixture). Returns 1 when a check has no
# positive control to run. Only R8 has one: a `+00:00` suffix is UTC and is
# accepted by capture-binding rule C, so R8 must accept it while rejecting the
# same-string garbage form.
build_control_fixture() {
  local id=$1 dest=$2
  case $id in
    R8) : ;;
    *) return 1 ;;
  esac
  mkdir -p "$dest"
  copy_into "$dest" corpus/source-snapshots/round-32/manifest.json || return 1
  python3 - "$dest/corpus/source-snapshots/round-32/manifest.json" <<'PY'
import json
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as fh:
    data = json.load(fh)
values = ["2026-10-26T04:16:06+00:00", "2026-10-26T04:16:16.500Z"]
for record, value in zip([r for r in data.get("sources", []) if isinstance(r, dict)], values):
    if "fetched_utc" in record:
        record["fetched_utc"] = value
with open(path, "w", encoding="utf-8") as fh:
    json.dump(data, fh, indent=1)
    fh.write("\n")
PY
  return 0
}

run_selftest() {
  local base scratch live_root i id live fxopen ctl_state ctl_run verdict problems failures=0 cases=0
  base=${SCRATCH_ARG:-${HYAKU_SCRATCH:-${TMPDIR:-/tmp}}}
  if [ ! -d "$base" ]; then
    echo "selftest UNAVAILABLE reason=scratch-missing base=$base"
    return 2
  fi
  scratch=$(mktemp -d "$base/r-defect-closure-selftest.XXXXXX") || {
    echo "selftest UNAVAILABLE reason=scratch-create-failed base=$base"
    return 2
  }
  live_root=$RD_ROOT
  trap 'rm -rf -- '"$scratch"'' EXIT
  for i in "${!CHECK_IDS[@]}"; do
    id=${CHECK_IDS[$i]}
    cases=$((cases + 1))
    run_check_once "$live_root" "${CHECK_FNS[$i]}"
    live=$?
    if ! build_broken_fixture "$id" "$scratch/$id"; then
      verdict=fail
      problems="fixture-build"
      echo "selftest case=$id live=unknown fixture=unknown verdict=fail problems=$problems"
      failures=$((failures + 1))
      continue
    fi
    run_check_once "$scratch/$id" "${CHECK_FNS[$i]}"
    fxopen=$?
    verdict=pass
    problems=""
    if [ "$live" -ne 0 ]; then
      verdict=fail
      problems="live-open(${DESC:-undescribed})"
    fi
    if [ "$fxopen" -eq 0 ]; then
      verdict=fail
      problems="${problems:+$problems }fixture-not-rejected"
    fi
    ctl_state=absent
    if build_control_fixture "$id" "$scratch/$id-control"; then
      run_check_once "$scratch/$id-control" "${CHECK_FNS[$i]}"
      ctl_run=$?
      if [ "$ctl_run" -eq 0 ]; then
        ctl_state=pass
      else
        ctl_state=fail
        verdict=fail
        problems="${problems:+$problems }control-not-accepted(${DESC:-undescribed})"
      fi
    fi
    if [ "$verdict" = pass ]; then
      printf 'selftest case=%s live=pass fixture=rejected control=%s verdict=pass\n' \
        "$id" "$ctl_state"
    else
      printf 'selftest case=%s live=%s fixture=%s control=%s verdict=fail problems=%s\n' \
        "$id" \
        "$([ "$live" -eq 0 ] && echo pass || echo open)" \
        "$([ "$fxopen" -ne 0 ] && echo rejected || echo passed)" \
        "$ctl_state" \
        "$problems"
      failures=$((failures + 1))
    fi
  done
  printf 'selftest cases=%d failures=%d\n' "$cases" "$failures"
  [ "$failures" -eq 0 ]
}

if [ "$MODE" = selftest ]; then
  RD_REPORT=$(run_selftest)
  RD_STATUS=$?
  printf '%s\n' "$RD_REPORT"
  if [ "$RD_STATUS" -eq 2 ]; then
    exit 2
  fi
  judge_selftest_report "$RD_REPORT" "$RD_STATUS"
  exit $?
fi
RD_REPORT=$(run_plain)
RD_STATUS=$?
printf '%s\n' "$RD_REPORT"
if ! plain_report_ok "$RD_REPORT"; then
  printf 'suite problem=self-report plain-lines=%s expected=9\n' \
    "$(printf '%s\n' "$RD_REPORT" | grep -c '^R[1-9] check=' || true)"
  exit 1
fi
exit "$RD_STATUS"
