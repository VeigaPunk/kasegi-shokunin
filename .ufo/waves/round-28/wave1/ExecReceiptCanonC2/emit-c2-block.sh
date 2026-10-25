#!/usr/bin/env bash
# Emit the canonical round-28 C2 receipt block from EXECUTED observations.
# Owner: ExecReceiptCanonC2 (draft) — the L1 runs this at the landed digest and
# pastes the output into the single canonical receipt
# .ufo/waves/round-28/c1-receipt-index.txt. This script creates no canonical file.
#
# Exit 0 only when every frozen C2 after value is reached; exit 1 otherwise, so a
# half-landed tree cannot be pasted as if it passed.
set -u

ROOT=/home/vgpnk/Projects/shokunin/kasegi-shokunin
MANIFEST=corpus/source-snapshots/round-28/manifest.json
ENTRY=corpus/knowledge/japanese-domestic-disclosure-workflow.md
cd "$ROOT" || { echo "UNAVAILABLE reason=cannot-cd $ROOT"; exit 2; }

ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)

frontier=$(awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md)
entries=$(grep -lE '^source: S042 ' corpus/knowledge/*.md 2>/dev/null | wc -l | tr -d ' ')
rows=$(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md)
s042=$(grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md)

census_out=$(/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi 2>&1)
census_rc=$?
census_w04=$(printf '%s\n' "$census_out" | grep -c 'W04')
census_e11=$(printf '%s\n' "$census_out" | grep -c 'E11')

harness_out=$(python3 corpus/instruments/frontier-recheck-count.py 2>&1)
harness_rc=$?
harness_line=$(printf '%s\n' "$harness_out" | tail -n 1)
harness_ok=$(printf '%s\n' "$harness_out" | grep -c '^PASS')

stem_line=PENDING
manifest_sha=ABSENT
if [ -f "$MANIFEST" ]; then
  manifest_sha=$(sha256sum "$MANIFEST" | awk '{print $1}')
  stem_line=$(python3 - "$MANIFEST" <<'PY'
import json, os, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
pairs = " ".join("%s->%s" % (r["id"], r["path"]) for r in d["sources"])
ok = all(os.path.splitext(os.path.basename(r["path"]))[0] == r["id"] for r in d["sources"])
print("stem_ok=%s pairs=%s" % (ok, pairs))
PY
)
fi

s041_sha=$(sha256sum corpus/source-snapshots/round-28/S041.txt 2>/dev/null | awk '{print $1}')
s042_sha=$(sha256sum corpus/source-snapshots/round-28/S042.txt 2>/dev/null | awk '{print $1}')
if cmp -s corpus/source-snapshots/round-26/S041.txt corpus/source-snapshots/round-28/S041.txt; then
  recapture=IDENTICAL
else
  recapture=DIFFERS
fi

# Entry-contract equality (the frozen clause: recheck --source ids EQUAL declared ids).
# frontier-recheck-count.py tests declared subset-of recheck subset-of cited; equality
# is stronger and is what C2's predicate states, so it is measured here too.
if [ -f "$ENTRY" ]; then
  entry_line=$(python3 - "$ENTRY" <<'PY'
import re, sys
body = open(sys.argv[1], encoding="utf-8").read()
declared = sorted(set(re.findall(r"(?m)^source:\s*(S\d{3,})", body)))
recheck = ""
for line in body.splitlines():
    m = re.match(r"^recheck:\s*(.+)$", line)
    if m:
        recheck = m.group(1)
        break
selected = sorted(set(re.findall(r"--source\s+(S\d{3,})", recheck)))
print("declared=%s recheck=%s equal=%s recheck_lines=%d"
      % (",".join(declared), ",".join(selected), declared == selected,
         len(re.findall(r"(?m)^recheck:", body))))
PY
)
  entry_state=present
else
  entry_line=declared=- recheck=- equal=False recheck_lines=0
  entry_state=absent
fi

if [ -f "$MANIFEST" ]; then
  python3 corpus/instruments/source-recheck.py --manifest "$MANIFEST" --source S041 >/dev/null 2>&1
  rc041=$?
  python3 corpus/instruments/source-recheck.py --manifest "$MANIFEST" --source S042 >/dev/null 2>&1
  rc042=$?
  q9=$(python3 corpus/instruments/source-recheck.py --manifest "$MANIFEST" 2>&1 | awk '
    / OK occurrences=1$/ {unique++}
    / OK .*anchor=[0-9]+-ok$/ {anchored++}
    /MISMATCH|anchor=MISSING|anchor=[0-9]+-BROKEN|OUT-OF-RANGE|UNAVAILABLE/ {bad++}
    END {printf "unique=%d anchored_ok=%d bad=%d", unique+0, anchored+0, bad+0}')
  q9_total=$(python3 - "$MANIFEST" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
print(sum(len(r["quotes"]) for r in d["sources"]))
PY
)
else
  rc041=PENDING
  rc042=PENDING
  q9=PENDING
  q9_total=0
fi

echo "== round-28 C2 receipt (coverage — F12 Japanese state-coordinated disclosure workflow) =="
echo "measured_utc=$ts"
echo "base=c9f8b115a098c65356e4b3b6048af45a37ab8395"
echo "frontier_admitted_before=11"
echo "frontier_admitted_after=$frontier"
echo "# source: awk -F'|' '\$2 ~ /^ *F[0-9]+ / && \$4 ~ /^ *admitted *\$/ {n++} END{print n+0}' corpus/README.md"
echo "entries_citing_S042_before=0"
echo "entries_citing_S042_after=$entries"
echo "# source: grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l"
echo "entry_file_state=$entry_state"
echo "entry_header_and_recheck=$entry_line"
echo "# source: entry bytes; equality limb measured here (harness tests only subset/superset)"
echo "sources_rows_before=41"
echo "sources_rows_after=$rows"
echo "s042_rows_after=$s042"
echo "# source: grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md ; same for S042"
echo "census_exit_after=$census_rc"
echo "census_findings=W04:$census_w04 E11:$census_e11"
echo "# source: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi"
echo "frontier_harness_before=entries=14 pass=14 exit=0"
echo "frontier_harness_after=$harness_line (pass_lines=$harness_ok harness_exit=$harness_rc)"
echo "# source: python3 corpus/instruments/frontier-recheck-count.py"
echo "manifest_sha256=$manifest_sha"
echo "manifest_path_$stem_line"
echo "s041_capture_sha256=$s041_sha"
echo "s042_capture_sha256=$s042_sha"
echo "s041_recapture_vs_round26=$recapture"
echo "# source: sha256sum corpus/source-snapshots/round-28/{manifest.json,S041.txt,S042.txt}; cmp against round-26/S041.txt"
echo "source_recheck_S041_exit=$rc041"
echo "source_recheck_S042_exit=$rc042"
echo "q9_assertions=$q9 total_pinned=$q9_total"
echo "# source: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json [--source S041|--source S042]"

if [ "$frontier" = 12 ] && [ "$entries" = 1 ] && [ "$rows" = 42 ] && [ "$s042" = 1 ] \
   && [ "$census_rc" = 0 ] && [ "$harness_line" = "entries=15 pass=15 exit=0" ] \
   && [ "$rc041" = 0 ] && [ "$rc042" = 0 ] && [ "$manifest_sha" != ABSENT ]; then
  echo "c2_after_reached=yes"
  exit 0
fi
echo "c2_after_reached=no"
echo "# PRE-STATE: at least one line above misses its frozen after value (see claims.json C2.after);"
echo "# the canonical file must not be assembled from this run."
exit 1
