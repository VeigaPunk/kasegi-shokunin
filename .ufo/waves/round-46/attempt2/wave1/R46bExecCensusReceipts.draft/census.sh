#!/usr/bin/env bash
# census.sh — round-46 (attempt 2) kasegi census pair + freeze pins receipt.
#
# Seat: R46bExecCensusReceipts. Draft only; the L1 integrates and commits.
#
# Modes:
#   before    verify the frozen census-before receipt exists (create it by
#             running the census NOW if it is absent) and re-derive it to
#             prove it is reproducible
#   after     run-book for the round-end census: same command, expected exit 0,
#             expected the same three W04 warnings (S028/S029/S072), plus an
#             optional W04 S074 if the S074 row shares a URL with a held row.
#             Cross-checks the second invocation C2's f29-gate H7 uses
#             (--file <root>/corpus/SOURCES.md) and requires both to agree.
#   pins      compute + save the freeze pins receipt (sha256 of the six frozen
#             artifacts at the current tree), each cross-checked against its
#             blob at the freeze commit. Frozen evidence must not change;
#             the wave surface (battery + selftests) is expected to change.
#   urlcheck  answer the round's URL question directly: does any held row
#             already carry the S074 repository-security-advisories URL?
#             A collision raises W04 (other scope) or E04 (same scope).
#   all       before, then pins, then urlcheck
#
# Every mode is read-only with respect to the lane tree: the only files it
# writes are the receipts named below (all under --out-dir, default the
# attempt-2 controls directory). No git/jj mutation, no network.
#
#   bash census.sh before|after|pins|urlcheck|all [--out-dir DIR] [--root DIR]
#                                                [--lane NAME|DIR]
#
# Exit: 0 all expectations held; 1 an expectation failed; 2 usage/env error.

set -u

LANE_REPO=${LANE_REPO:-/home/vgpnk/Projects/shokunin/kasegi-shokunin}
FLEET_ROOT=${FLEET_ROOT:-/home/vgpnk/Projects/shokunin}
CENSUS=${CENSUS:-$FLEET_ROOT/scripts/sources-census.sh}
CONTROLS=${CONTROLS:-$LANE_REPO/.ufo/waves/round-46/attempt2/controls}
DRAFT=${DRAFT:-$LANE_REPO/.ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft}
OUT_DIR=${OUT_DIR:-$CONTROLS}
ROOT=$FLEET_ROOT
LANE=kasegi

# The mode is the first non-option argument; options may precede it.
MODE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --out-dir) OUT_DIR=$2; shift 2 ;;
    --root)    ROOT=$2;    shift 2 ;;
    --lane)    LANE=$2;    shift 2 ;;
    -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
    -*) echo "ERROR: unknown option $1" >&2; exit 2 ;;
    *)  if [ -z "$MODE" ]; then MODE=$1; shift; else
          echo "ERROR: unexpected argument $1" >&2; exit 2
        fi ;;
  esac
done
[ -n "$MODE" ] || MODE=all

BEFORE=$OUT_DIR/sources-census-before.txt
AFTER=$OUT_DIR/sources-census-after.txt
PINS=$OUT_DIR/freeze-pins.txt

# The six frozen artifacts pinned by attempt-2/freeze.txt.
PIN_FILES=(
  corpus/source-snapshots/round-46-a2/S074.txt
  corpus/source-snapshots/round-46-a2/manifest.json
  corpus/instruments/r46-f29-gate.py
  corpus/instruments/r46-mutbat.py
  corpus/instruments/r46-counters-selftest-c1.py
  corpus/instruments/r46-counters-selftest-c2.py
)

# Expected census findings at round end: the three W04 warnings the frozen
# before receipt already carries, plus S074's row if (and only if) S074 shares
# a URL with an already-held row.
EXPECT_W04="S028 S029 S072"

die() { echo "ERROR: $*" >&2; exit 2; }

[ -x "$CENSUS" ] || [ -f "$CENSUS" ] || die "census script not found: $CENSUS"
[ -d "$LANE_REPO" ] || die "lane repo not found: $LANE_REPO"
[ -d "$ROOT" ] || die "fleet root not found: $ROOT"

# run_census <outfile> — run the round's census command, capture stdout and
# the exit status. Prints "exit=<rc>" on stdout; never aborts the script.
run_census() {
  local out=$1 rc
  bash "$CENSUS" validate --root "$ROOT" "$LANE" > "$out" 2>&1
  rc=$?
  echo "exit=$rc"
}

# ------------------------------------------------------------------ before ---
mode_before() {
  local rc fresh
  mkdir -p "$OUT_DIR" || die "cannot create $OUT_DIR"
  if [ -f "$BEFORE" ]; then
    echo "before: frozen receipt present at $BEFORE"
  else
    echo "before: receipt ABSENT — creating it now from the live tree"
    rc=$(run_census "$BEFORE")
    echo "before: created, $rc"
  fi
  # Re-derive from the live tree to prove the frozen receipt is reproducible.
  # Scratch: an explicit TMPDIR under the seat's own scratch root, never the
  # inherited TMPDIR.
  SCRATCH=${SCRATCH:-${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kasegi-r46/R46bExecCensusReceipts}
  mkdir -p "$SCRATCH" 2>/dev/null || SCRATCH=$OUT_DIR
  fresh=$(mktemp "$SCRATCH/census-fresh.XXXXXX") || die "mktemp failed"
  rc=$(run_census "$fresh")
  echo "before: fresh re-derivation $rc"
  if diff -u "$BEFORE" "$fresh" > /dev/null 2>&1; then
    echo "before: REPRODUCIBLE — fresh output is byte-identical to the frozen receipt"
    rm -f "$fresh"
    return 0
  fi
  echo "before: DRIFT — fresh output differs from the frozen receipt:"
  diff -u "$BEFORE" "$fresh" || true
  rm -f "$fresh"
  return 1
}

# ------------------------------------------------------------------- after ---
# The run-book for the round end. The L1 runs this after the wave lands.
mode_after() {
  local rc after_w04 new_w04 errors
  mkdir -p "$OUT_DIR" || die "cannot create $OUT_DIR"
  rc=$(run_census "$AFTER")
  echo "after: census command"
  echo "  bash $CENSUS validate --root $ROOT $LANE"
  echo "after: wrote $AFTER ($rc)"
  echo "after: output:"
  sed 's/^/  /' "$AFTER"

  # Exit status: 0 clean or warnings; 1 E-findings; 2 env/registry missing.
  case "$rc" in
    exit=0) echo "after: exit status OK (0 = clean or warnings only)" ;;
    *)     echo "after: exit status UNEXPECTED ($rc — expected exit=0)"; return 1 ;;
  esac

  # W04 set: the three carried warnings, plus an optional S074.
  # NOTE: the census packs "<id> duplicate url <url> across scopes" into ONE
  # tab-separated field, so the row id is the first whitespace-delimited word
  # of field 3, not field 3 itself.
  after_w04=$(awk -F'\t' '$2=="W04"{split($3,a," "); print a[1]}' "$AFTER" | tr '\n' ' ')
  echo "after: W04 rows seen:$after_w04"
  new_w04=""
  for id in $after_w04; do
    case " $EXPECT_W04 S074 " in
      *" $id "*) ;;
      *) new_w04="$new_w04 $id" ;;
    esac
  done
  if [ -n "$new_w04" ]; then
    echo "after: UNEXPECTED W04 rows (not S028/S029/S072/S074):$new_w04"
    return 1
  fi
  for id in $EXPECT_W04; do
    case " $after_w04 " in
      *" $id "*) ;;
      *) echo "after: DROPPED carried W04 $id"; return 1 ;;
    esac
  done

  if printf '%s\n' "$after_w04" | grep -q 'S074'; then
    echo "after: W04 S074 PRESENT — S074 shares a URL with an already-held row"
  else
    echo "after: W04 S074 ABSENT — S074's URL (repository-security-advisories) is not held by any existing row"
  fi

  # Any E-code at all is a failure of the round's census gate.
  errors=$(awk -F'\t' '$2 ~ /^E[0-9]+$/{print $2" "$3}' "$AFTER")
  if [ -n "$errors" ]; then
    echo "after: E-FINDINGS present:"; printf '%s\n' "$errors" | sed 's/^/  /'; return 1
  fi
  # The lane must be reported ok (no registry missing).
  if ! awk -F'\t' '$2=="ok"{found=1} END{exit !found}' "$AFTER"; then
    echo "after: FAIL — no ok line for the lane"
    return 1
  fi

  # Cross-check the SECOND invocation C2's admission gate uses: the f29-gate's
  # H7 runs the census with --file <root>/corpus/SOURCES.md, not with the
  # lane roster. The W04 set must be identical under both invocations.
  local registry
  if [ -d "$LANE" ]; then registry="$LANE/corpus/SOURCES.md"; else registry="$LANE_REPO/corpus/SOURCES.md"; fi
  local fmode="$OUT_DIR/sources-census-after.filemode.txt" frc fw04 lane_w04
  bash "$CENSUS" validate --file "$registry" > "$fmode" 2>&1
  frc=$?
  fw04=$(awk -F'\t' '$2=="W04"{split($3,a," "); print a[1]}' "$fmode" | tr '\n' ' ' | sed 's/ *$//')
  lane_w04=$(printf '%s' "$after_w04" | sed 's/ *$//')
  echo "after: H7 --file mode cross-check: exit=$frc W04:$fw04"
  if [ "$frc" != "0" ]; then
    echo "after: FAIL — H7 --file mode census did not exit 0"; return 1
  fi
  if [ "$fw04" != "$lane_w04" ]; then
    echo "after: FAIL — W04 set differs between lane mode and H7 --file mode"
    echo "after:   lane mode: $lane_w04"
    echo "after:   file mode: $fw04"
    return 1
  fi
  echo "after: OK — exit 0, three carried W04 warnings, no E-findings"
  return 0
}

# -------------------------------------------------------------------- pins ---
# sha256 of the six frozen artifacts at the current tree, plus a
# freeze-commit cross-check: each artifact's blob hash at the freeze commit
# must equal its working-tree hash (read-only git show; no mutation).
FREEZE_REV=${FREEZE_REV:-fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4}
mode_pins() {
  local f h fh same
  mkdir -p "$OUT_DIR" || die "cannot create $OUT_DIR"
  {
    echo "# round-46 attempt-2 freeze pins receipt"
    echo "# tree=$LANE_REPO"
    echo "# freeze-rev=$FREEZE_REV"
    echo "# generated-by=R46bExecCensusReceipts.census.sh pins"
    echo "# algorithm=sha256 (sha256sum)"
    echo "# freeze=SAME  working-tree hash equals the blob hash at the freeze rev"
    echo "# freeze=DIFF  working-tree hash differs from the blob hash at the freeze rev"
    echo "# freeze=ABSENT the path does not exist at the freeze rev"
    echo "#"
    echo "# kind=frozen-evidence  immutable pinned evidence (the S074 capture and"
    echo "#   its manifest, the F29 admission gate). These MUST NOT change during"
    echo "#   the wave; a DIFF here is a tamper, not progress."
    echo "# kind=wave-surface  the C1 work surface (the mutation battery and the"
    echo "#   two counter selftests). The wave is expected to CHANGE these; a DIFF"
    echo "#   here is the claimed work landing, not a tamper."
    for f in "${PIN_FILES[@]}"; do
      local kind=frozen-evidence
      case "$f" in
        *r46-mutbat.py|*r46-counters-selftest-c1.py|*r46-counters-selftest-c2.py) kind=wave-surface ;;
      esac
      if [ -f "$LANE_REPO/$f" ]; then
        h=$(sha256sum "$LANE_REPO/$f" | cut -d' ' -f1)
        if git -C "$LANE_REPO" cat-file -e "$FREEZE_REV:$f" 2>/dev/null; then
          fh=$(git -C "$LANE_REPO" show "$FREEZE_REV:$f" | sha256sum | cut -d' ' -f1)
          if [ "$fh" = "$h" ]; then same=SAME; else same=DIFF; fi
        else
          same=ABSENT
        fi
        printf '%s  %s  [freeze=%s kind=%s]\n' "$h" "$f" "$same" "$kind"
      else
        printf 'MISSING  %s\n' "$f"
      fi
    done
  } > "$PINS"
  echo "pins: wrote $PINS"
  sed 's/^/  /' "$PINS"
  if grep -q '^MISSING' "$PINS"; then
    echo "pins: FAIL — a pinned artifact is missing"
    return 1
  fi
  # A DIFF on frozen evidence is a tamper (fail). A DIFF on the wave surface
  # is the claimed C1 work landing (report, do not fail). An ABSENT path at
  # the freeze rev is always wrong (fail).
  if grep -q '\[freeze=DIFF kind=frozen-evidence\]' "$PINS"; then
    echo "pins: FAIL — a frozen-evidence pin differs from the freeze commit (tamper)"
    grep '\[freeze=DIFF kind=frozen-evidence\]' "$PINS" | sed 's/^/  /'
    return 1
  fi
  if grep -q '\[freeze=ABSENT' "$PINS"; then
    echo "pins: FAIL — a pinned artifact is absent at the freeze rev"
    return 1
  fi
  if grep -q '\[freeze=DIFF kind=wave-surface\]' "$PINS"; then
    echo "pins: wave-surface pins changed (expected: the C1 work landed):"
    grep '\[freeze=DIFF kind=wave-surface\]' "$PINS" | sed 's/^/  /'
  fi
  echo "pins: OK — all six artifacts present; frozen evidence unchanged at the freeze commit"
  return 0
}

# ---------------------------------------------------------------- urlcheck ---
# The question the round must answer: does the S074 row (repository security
# advisories) share a URL with an already-held row? A shared URL across two
# different scopes raises a W04 warning (and, if the scope also matches, an
# E04 finding). This mode answers it directly by normalizing the URLs the
# census way (strip scheme, strip fragment, strip trailing slash, lowercase
# host) and comparing.
S074_URL=${S074_URL:-https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories}
mode_urlcheck() {
  local registry hits=0 self=0
  if [ -d "$LANE" ]; then registry="$LANE/corpus/SOURCES.md"; else registry="$LANE_REPO/corpus/SOURCES.md"; fi
  [ -f "$registry" ] || die "registry not found: $registry"
  echo "urlcheck: registry=$registry"
  echo "urlcheck: S074 url=$S074_URL"
  # Normalize exactly as the census url_of() does: drop scheme, drop fragment,
  # drop a trailing slash, lowercase the HOST, keep the path verbatim.
  local norm
  norm=$(printf '%s' "$S074_URL" | sed -E 's#^https?://##; s#[#].*$##; s#/$##' \
         | awk '{ i=index($0,"/"); if (i) print tolower(substr($0,1,i-1)) substr($0,i); else print tolower($0) }')
  echo "urlcheck: normalized=$norm"
  # Scan the registry rows with the census's own column layout:
  #   | id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
  # => $2=id, $3=source(cell), $6=scope(cell).
  # A hit on S074 itself is not a collision (it is the row under test); a hit
  # on any OTHER row is a real collision.
  while IFS=$'\t' read -r id scope; do
    [ -n "$id" ] || continue
    if [ "$id" = "S074" ]; then
      echo "urlcheck: self — row S074 carries this URL (the row under test; expected once it lands)"
      self=$((self+1))
      continue
    fi
    echo "urlcheck: COLLISION — row $id already carries this URL (scope: $scope)"
    hits=$((hits+1))
  done < <(awk -F'|' -v probe="$norm" '
    function trim(s){gsub(/^[ \t]+|[ \t]+$/,"",s);return s}
    function url_of(s,   u,n){
      if (match(s,/https?:\/\/[^[:space:]|]+/)) { u=substr(s,RSTART,RLENGTH)
        sub(/#[^ ]*$/,"",u); sub(/\/$/,"",u); sub(/^[A-Za-z]+:\/\//,"",u)
        n=index(u,"/"); if(n) u=tolower(substr(u,1,n-1)) substr(u,n); else u=tolower(u)
        return u }
      return "" }
    { line=$0
      if (line ~ /^ {0,3}\|/) {
        sub(/^ {0,3}/,"",line); $0=line
        if (NF==13) {
          id=trim($2); src=trim($3); scope=trim($6)
          if (id ~ /^S[0-9]{3,}$/ && url_of(src)==probe)
            printf "%s\t%s\n", id, scope
        }
      } }' "$registry")
  if [ "$hits" -eq 0 ]; then
    echo "urlcheck: NO COLLISION — no held row other than S074 carries the S074 URL"
    echo "urlcheck: consequence: adding S074 raises NO W04 and NO E04"
    return 0
  fi
  echo "urlcheck: consequence: adding S074 raises a W04 (same URL, different scope) or an E04 (same URL, same scope) — the after-run will show it"
  return 1
}

rc=0
case "$MODE" in
  before)   mode_before   || rc=1 ;;
  after)    mode_after    || rc=1 ;;
  pins)     mode_pins     || rc=1 ;;
  urlcheck) mode_urlcheck || rc=1 ;;
  all)
    mode_before || rc=1
    mode_pins   || rc=1
    mode_urlcheck || rc=1
    echo "all: before + pins + urlcheck done (run 'after' at round end)"
    ;;
  *) die "unknown mode: $MODE (before|after|pins|urlcheck|all)" ;;
esac
exit $rc
