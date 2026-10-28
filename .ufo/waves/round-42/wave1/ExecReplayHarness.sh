#!/usr/bin/env bash
# ExecReplayHarness.sh — the replay-limb library the round-42 closure suite
# sources.  SOURCE this file; do not execute it.
#
# CONTRACT
#
#   replay_defeat <artifact> <mode>
#
#     <artifact>  a defeat-case id ("e1.evidence-not-named"), a defeat
#                 artifact id ("CritC1KillRule.md" -> every case that artifact
#                 carries), or "all".
#     <mode>      fixture  (default) materialize the minimal mutated fixture
#                          the defeat describes and invoke the current suite's
#                          limb directly on it.
#                 export   materialize a full export of the ref, mutate that,
#                          and invoke the same limb on it.
#                 list     print the catalog rows of <artifact>; no mutation.
#
#   exit 0  every selected defeat was REJECTED by the current suite's limb
#           AND the same limb ACCEPTED the pristine fixture (the rejection is
#           attributable to the defeat, not to a broken fixture).
#   exit 1  at least one selected defeat was ACCEPTED by the limb: the family
#           is still open.  This is the kill signal.
#   exit 2  the replay could not be graded: the limb is unresolvable, the
#           fixture could not be materialized, or the limb rejected the
#           PRISTINE fixture (the control run), so no verdict is attributable.
#           Never a silent pass.
#
#   replay_defeat prints NOTHING on stdout: the closure suite's transcript is
#   byte-exact, so diagnostics go to stderr and only under REPLAY_VERBOSE=1.
#   Use replay_report to print a verdict table on stdout.
#
# WHAT IS UNDER TEST
#
#   The limb is the CURRENT suite's own check function (or, for the two
#   corpus-instrument families, the corpus instrument itself), invoked in a
#   subshell on a mutated fixture that this library materializes under the
#   scratch root.  The suite binary is never re-run and the lane is never
#   written to.  A defeat is "rejected" when the limb exits nonzero (or
#   prints closed=0).
#
#   Every case runs the limb TWICE: once on the pristine fixture (the control)
#   and once on the mutated fixture.  The control must be green.  Without it a
#   limb that rejects everything would score every defeat as closed, which is
#   the vacuous-pass failure the round-41 verdict rejected.
#
# DISCOVERY
#
#   The suite under test and the ref under test are discovered, not assumed:
#   REPLAY_SUITE / SELF / the newest corpus/instruments/r*-closure.sh, and
#   REPLAY_REF / REF_RESOLVED / the lane tip.  The round token, the scratch
#   family name, the truth tally token, the evidence stems, the record list and
#   the declared-blocks path are read out of the suite source, so one library
#   drives any round's suite.
#
# ENVIRONMENT (all optional)
#
#   REPLAY_SUITE      suite under test            (default: discovered)
#   REPLAY_LANE       lane repository             (default: derived / $LANE)
#   REPLAY_REF        ref to export               (default: $REF_RESOLVED / tip)
#   REPLAY_BASE_REF   base ref for diffs          (default: $BASE_REF / $REPLAY_REF)
#   REPLAY_EXPORT     export tree to copy from    (default: $EXPORT / built)
#   REPLAY_SCRATCH    scratch base                (default: ${TMPDIR:-/tmp})
#   REPLAY_KEEP       1 keeps the materialized case dir (default 0)
#   REPLAY_VERBOSE    1 prints case diagnostics on stderr (default 0)
#   REPLAY_LIMB_MAP   "FAMILY=SPEC[;FAMILY=SPEC]" overrides the family->limb
#                     map.  SPEC is a suite function name, optionally with
#                     arguments ("check_j4 TREE REF", where TREE and REF are
#                     placeholders), or "py:<path> --root ROOT" for a corpus
#                     instrument (the path is relative to the lane root).
#   REPLAY_STRAY_DIR  directory that receives the F-SCAN stray (default: the
#                     parent of the configured scratch root)
#   REPLAY_EVIDENCE   space-separated evidence stems (default: from the suite)
#
# The library changes no shell options and writes nothing outside the scratch
# root it creates.

# ---------------------------------------------------------------------------
# catalog
# ---------------------------------------------------------------------------
# id | family | artifact | expected rejection mechanism
#
# The artifact column names the committed defeat artifact the case replays.
# The expected-mechanism column is what the repaired limb must show; the L1
# binds each family to its own check through REPLAY_LIMB_MAP.
REPLAY_CATALOG_CASES=(
"e1.evidence-not-named|F-EVID|CritC1KillRule.md|the SCORECARD.md Correction block names no kill-rule evidence, so the per-correction evidence count must fall below the required set (payload evidence=<n>/3) and the limb must exit nonzero"
"e2.evidence-not-named-log|F-EVID|RevC1Counters.md|the LOG.md Correction block names no evidence; a cross-record union must not mask it (payload evidence=<n>/3) and the limb must exit nonzero"
"e3.evidence-not-named-shonen|F-EVID|RevC1Counters.md|the SHONEN.md Correction block names no evidence; per-correction evidence must be enforced (payload evidence=<n>/3) and the limb must exit nonzero"
"e4.evidence-not-named-union|F-EVID|CritC1KillRule.md|the canonical committed mutant: the first Correction block of EVERY record (SCORECARD.md, LOG.md, SHONEN.md) is replaced by an evidence-free but still-qualified line, exactly as r41-closure.sh selftest_case_i1 does it; a cross-record union must not mask it (payload evidence=<n>/3) and the limb must exit nonzero"
"t1.mangled-tally-first-line|F-TOKEN|CritC1KillRule.md|one Correction block states the tally as closed=10/100 while a sibling block of the same record still states closed=10/10: the value must match as a bounded token in that very block (payload tally=2/3 or mangled=1) and the limb must exit nonzero"
"t2.mangled-tally-every-correction|F-TOKEN|MutSuite.findings.txt|every Correction block of the record states the mangled tally: the record must not tally green (payload tally=2/3) and the limb must exit nonzero"
"t3.mangled-tally-every-mention|F-TOKEN|RevC1Counters.defeats.txt|every mention of the truth tally in the record is the strict superset closed=10/100: a substring match must not satisfy a token-boundary match (payload substring=2/2) and the limb must exit nonzero"
"b1.registry-bare-pipe|F-TABLE|MutSkillTablePipes.md|a bare pipe inside the entry-command cell inflates the cell count (cells=11); the row must be rejected as malformed (payload broken=1 or ok=0) and the limb must exit nonzero"
"b2.registry-leading-space|F-TABLE|MutSkillTablePipes.md|leading whitespace in the first cell must not be trimmed into a match (payload ok=0 or rows=0) and the limb must exit nonzero"
"b3.registry-mention-only|F-TABLE|RevC1Counters.defeats.txt|a mention-only row is not a registry row: the row count must be 0 (payload rows=0) and the limb must exit nonzero"
"b4.registry-blank-line|F-TABLE|CritC1KillRule.md|a blank line before the row breaks the contiguous table (payload broken=1) and the limb must exit nonzero"
"d1.declared-omits-changed-path|F-DECL|CritDeclarationCoverage.md|a changed path that is absent from the declaration file is a completeness violation: the declared set must be compared with the changed set (payload completeness=0) and the limb must exit nonzero"
"d2.declared-symlink-outside|F-DECL|CritI12Necessity.md|a declared path that is a symlink resolving outside the export must be rejected (payload canon=0, paths=0) and the limb must exit nonzero"
"d3.declared-short-of-added|F-DECL|MutH6H10.md|a declaration one line short of the added block must not validate (payload tail<declared) and the limb must exit nonzero"
"s1.stray-outside-root|F-SCAN|MutScratchTiming.md|a family-named leftover outside the configured scan root must be detected (payload strays>=1 or read=fail) and the limb must exit nonzero"
"s2.stray-case-separator|F-SCAN|CritKillRule.md|a family-named leftover in another case or with another separator must be detected (payload strays>=1) and the limb must exit nonzero"
"s3.stray-dot-prefixed|F-SCAN|CritKillRule.md|a dot-prefixed family-named leftover must be detected (payload strays>=1) and the limb must exit nonzero"
"s4.stray-nested|F-SCAN|CritKillRule.md|a family-named leftover nested below the scan root must be detected (payload strays>=1) and the limb must exit nonzero"
"s5.stray-ancestor-symlink|F-SCAN|CritKillRule.h6-escapes.sh|a family-named symlink to an ancestor of the work dir must be detected (payload strays>=1) and the limb must exit nonzero"
"s6.scan-root-missing|F-SCAN|CritKillRule.md|a nonexistent scan root must fail closed (payload read=fail) and the limb must exit nonzero"
"s7.stray-unreadable|F-SCAN|CritKillRule.h6-escapes.sh|an unreadable family-named leftover must fail closed (payload read=fail or strays>=1) and the limb must exit nonzero"
"s8.stray-sibling-round|F-SCAN|MutScratchTiming.md|a leftover named for a SIBLING round (kasegi-r<round-1> or kasegi-r<round+1>) must be detected: the scan covers the kasegi-r4[0-9]* prefix, not just this round's own family (payload strays>=1) and the limb must exit nonzero"
"c1.binding-missing-path|F-BIND|MutBindingExistence.md|a manifest record whose path names a file that does not exist must be unbound (records=<n> bound=<n-1> unbound=1) and the instrument must exit nonzero"
"c2.binding-url-case|F-BIND|MutBindingExistence.md|a manifest record whose URL differs in case from the registry row must be unbound and the instrument must exit nonzero"
"c3.binding-url-trailing-slash|F-BIND|MutBindingExistence.md|a manifest record whose URL carries a trailing slash must be unbound and the instrument must exit nonzero"
"p1.frontier-status-flip|F-FLIP|MutC2Chain.md|a frontier row whose status cell flips away from admitted must be reported, not silently dropped from the denominator (the explicit PASS line for that frontier id must be absent and the count must not shrink silently) and the instrument must exit nonzero"
"p2.frontier-decoy-row|F-FLIP|MutFrontierParser.md|a frontier row naming a non-existent entry must fail (FAIL F999 ... missing-entry) and the instrument must exit nonzero"
)

# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

replay__log() {
  [ "${REPLAY_VERBOSE:-0}" = 1 ] || return 0
  printf 'replay: %s\n' "$*" >&2
}

replay__die() {
  printf 'replay: %s\n' "$*" >&2
  exit 2
}

replay__realpath_m() {
  realpath -m -- "$1" 2>/dev/null || printf '%s' "$1"
}

replay__mkdir() { mkdir -p -- "$1" 2>/dev/null; }

# ---------------------------------------------------------------------------
# suite / lane / ref discovery
# ---------------------------------------------------------------------------

# replay_suite_file LANE_HINT -> path of the suite under test
replay_suite_file() {
  if [ -n "${REPLAY_SUITE:-}" ] && [ -f "${REPLAY_SUITE}" ]; then
    replay__realpath_m "$REPLAY_SUITE"; return 0
  fi
  # SELF is the closure suite's own path when it sources this library.
  if [ -n "${SELF:-}" ] && [ -f "${SELF}" ]; then
    replay__realpath_m "$SELF"; return 0
  fi
  local hint=$1 d newest=''
  if [ -n "$hint" ] && [ -d "$hint/corpus/instruments" ]; then
    for d in "$hint"/corpus/instruments/r*-closure.sh; do
      [ -f "$d" ] || continue
      newest=$d
    done
  fi
  if [ -z "$newest" ]; then
    for d in /home/vgpnk/Projects/shokunin/*/corpus/instruments/r*-closure.sh; do
      [ -f "$d" ] || continue
      newest=$d
    done
  fi
  [ -n "$newest" ] || return 1
  replay__realpath_m "$newest"
}

# replay_lane_dir SUITE -> lane repository that owns SUITE
replay_lane_dir() {
  if [ -n "${REPLAY_LANE:-}" ] && [ -d "${REPLAY_LANE}" ]; then
    replay__realpath_m "$REPLAY_LANE"; return 0
  fi
  if [ -n "${LANE:-}" ] && [ -d "${LANE}" ]; then
    replay__realpath_m "$LANE"; return 0
  fi
  local d
  d=$(dirname -- "$1"); d=$(dirname -- "$d"); d=$(dirname -- "$d")
  [ -d "$d" ] && { replay__realpath_m "$d"; return 0; }
  return 1
}

# replay_suite_value SUITE NAME -> value of a `NAME=` assignment in the suite
replay_suite_value() {
  local line
  line=$(grep -E "^${2}=" -- "$1" 2>/dev/null | head -n 1)
  [ -n "$line" ] || return 1
  line=${line#*=}
  line=${line%\'}; line=${line#\'}
  line=${line%\"}; line=${line#\"}
  printf '%s' "$line"
}

# replay_suite_words SUITE NAME -> whitespace-separated words of `NAME=(...)`
replay_suite_words() {
  local line
  line=$(grep -E "^${2}=\(" -- "$1" 2>/dev/null | head -n 1)
  [ -n "$line" ] || return 1
  line=${line#*\(}; line=${line%\)}
  printf '%s\n' "$line" | tr -s '[:space:]' '\n' | grep -v '^$' | tr '\n' ' '
}

# replay_suite_round SUITE -> the round token the suite grades ("41")
replay_suite_round() {
  local n
  n=$(grep -oE 'Correction \[\(]round [0-9]+' -- "$1" 2>/dev/null | head -n 1 | grep -oE '[0-9]+$')
  [ -n "$n" ] || n=$(grep -oE 'ROUND[0-9]+_TALLY' -- "$1" 2>/dev/null | head -n 1 | grep -oE '[0-9]+$')
  [ -n "$n" ] || return 1
  printf '%s' "$n"
}

# replay_suite_family SUITE -> the scratch family token ("kasegi-r41")
replay_suite_family() {
  local f
  f=$(grep -oE 'kasegi-r[0-9]+' -- "$1" 2>/dev/null | head -n 1)
  [ -n "$f" ] || return 1
  printf '%s' "$f"
}

# replay_suite_tally SUITE -> the truth tally token ("closed=10/10")
replay_suite_tally() {
  local t
  t=$(grep -oE '^[A-Z0-9_]*TALLY=closed=[0-9]+/[0-9]+' -- "$1" 2>/dev/null | head -n 1 | sed -e 's/.*TALLY=//')
  [ -n "$t" ] || return 1
  printf '%s' "$t"
}

# replay_suite_records SUITE -> the record files the suite grades
replay_suite_records() {
  local w
  w=$(replay_suite_words "$1" RECORDS)
  [ -n "$w" ] || return 1
  printf '%s' "$w"
}

# replay_suite_evidence SUITE -> the evidence stems the suite requires
replay_suite_evidence() {
  local w
  if [ -n "${REPLAY_EVIDENCE:-}" ]; then printf '%s ' ${REPLAY_EVIDENCE}; return 0; fi
  w=$(replay_suite_words "$1" EVIDENCE)
  [ -n "$w" ] || return 1
  printf '%s' "$w"
}

# replay_suite_declared SUITE -> the declared-blocks path the suite grades
replay_suite_declared() {
  local v
  v=$(replay_suite_value "$1" DECLARED)
  [ -n "$v" ] || return 1
  printf '%s' "$v"
}

# ---------------------------------------------------------------------------
# family -> limb map
# ---------------------------------------------------------------------------
# Candidates, most specific first.  The r42 suite's J-checks are tried before
# the r41 I-checks, so one library drives both.  REPLAY_LIMB_MAP overrides
# (FAMILY=SPEC[;FAMILY=SPEC]).
REPLAY_LIMB_DEFAULT='F-EVID|check_j1|check_i1
F-TOKEN|check_j2|check_i3
F-TABLE|check_j3|check_i7
F-DECL|check_j4|check_i5|check_i12
F-SCAN|check_j5|check_i6
F-BIND|check_j6|py:corpus/instruments/capture-binding-check.py --root ROOT
F-FLIP|check_j7|py:corpus/instruments/frontier-recheck-count.py --root ROOT'

# replay_limb_spec FAMILY -> the candidate list for FAMILY
replay_limb_spec() {
  local fam=$1 line
  if [ -n "${REPLAY_LIMB_MAP:-}" ]; then
    line=$(printf '%s\n' "${REPLAY_LIMB_MAP//;/$'\n'}" | grep -E "^${fam}=" | head -n 1)
    if [ -n "$line" ]; then
      printf '%s' "${line#*=}"; return 0
    fi
  fi
  line=$(printf '%s\n' "$REPLAY_LIMB_DEFAULT" | grep -E "^${fam}\|" | head -n 1)
  [ -n "$line" ] || return 1
  printf '%s' "${line#*|}"
}

# replay_limb_resolve FAMILY -> "kind<TAB>spec" for the first candidate that
# exists.  kind is "fn" (a suite function) or "py" (a corpus instrument).
#
# The suite's check functions are enumerated by sourcing the suite in a
# SUBSHELL: the suite only runs main() when it is executed, not when it is
# sourced, so sourcing it exposes its functions without side effects on the
# caller.  When the suite has already sourced this library, the same
# enumeration sees the functions in the caller.
replay_limb_resolve() {
  local fam=$1 spec cand path
  spec=$(replay_limb_spec "$fam") || return 1
  local IFS='|'
  for cand in $spec; do
    [ -n "$cand" ] || continue
    case "$cand" in
      py:*)
        path=${cand#py:}; path=${path%% *}
        # resolvable against the export under test, not the working tree
        if [ -f "${REPLAY_BASE:-}/$path" ] || [ -f "$REPLAY_LANE/$path" ]; then
          printf 'py\t%s' "$cand"; return 0
        fi
        ;;
      *)
        if replay__has_fn "${cand%% *}"; then printf 'fn\t%s' "$cand"; return 0; fi
        ;;
    esac
  done
  return 1
}

# replay__has_fn NAME -> 0 when NAME is defined (in the caller or in the suite)
replay__has_fn() {
  declare -F "$1" >/dev/null 2>&1 && return 0
  [ -n "${REPLAY_SUITE:-}" ] && [ -f "${REPLAY_SUITE:-}" ] || return 1
  (
    . "$REPLAY_SUITE" >/dev/null 2>&1
    declare -F "$1" >/dev/null 2>&1
  )
}

# ---------------------------------------------------------------------------
# catalog access
# ---------------------------------------------------------------------------

# replay_catalog_rows [artifact] -> matching catalog rows, tab separated
replay_catalog_rows() {
  local want=${1:-} row id fam art rest abase wbase
  for row in "${REPLAY_CATALOG_CASES[@]}"; do
    id=${row%%|*}; rest=${row#*|}
    fam=${rest%%|*}; rest=${rest#*|}
    art=${rest%%|*}; rest=${rest#*|}
    if [ -n "$want" ] && [ "$want" != all ]; then
      abase=${art##*/}; wbase=${want##*/}
      if [ "$id" != "$want" ] && [ "$abase" != "$wbase" ] && [ "${abase%.md}" != "${wbase%.md}" ]; then
        continue
      fi
    fi
    printf '%s\t%s\t%s\t%s\n' "$id" "$fam" "$art" "$rest"
  done
}

# replay_case_field CASE FIELD(1=family 2=artifact) -> the field
replay_case_field() {
  local row
  for row in "${REPLAY_CATALOG_CASES[@]}"; do
    case "$row" in
      "$1|"*) printf '%s' "${row#*|}" | cut -d'|' -f"$2"; return 0 ;;
    esac
  done
  return 1
}

# ---------------------------------------------------------------------------
# materialization helpers
# ---------------------------------------------------------------------------

# replay__cp_paths SRC DST < paths on stdin
replay__cp_paths() {
  local src=$1 dst=$2 p
  replay__mkdir "$dst"
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    [ -e "$src/$p" ] || continue
    replay__mkdir "$dst/$(dirname -- "$p")" || return 1
    cp -a -- "$src/$p" "$dst/$p" 2>/dev/null || return 1
  done
}

# replay__export_tree LANE REF DEST -- extract REF into DEST (read-only git)
replay__export_tree() {
  replay__mkdir "$3" || return 1
  git -C "$1" archive --format=tar "$2" 2>/dev/null | tar -x -C "$3" 2>/dev/null
}

# ---------------------------------------------------------------------------
# mutators: each takes (CASE_DIR TREE ...) and mutates TREE in place
# ---------------------------------------------------------------------------

# mut_evid CASE TREE PAT -- strip every evidence stem from every Correction
# block of the record PAT.  The other records keep their evidence, so a limb
# that aggregates evidence across records still sees the full set: that is the
# defect the case replays.
#
# Only the suite's OWN round is touched (REPLAY_ROUND): the tree also carries
# the corrections of earlier rounds, and rewriting those would change bytes
# the suite never reads.
mut_evid() {
  local tree=$2 pat=$3 stem
  local f="$tree/$pat"
  [ -f "$f" ] || return 1
  [ -n "$REPLAY_ROUND" ] || return 1
  # strip the evidence stems from the suite's OWN round only: the record also
  # carries the corrections of earlier rounds, which the suite never reads.
  for stem in ${REPLAY_EV}; do
    [ -n "$stem" ] || continue
    awk -v stem="$stem" -v rnd="$REPLAY_ROUND" '
      $0 ~ ("^Correction [(]round " rnd "[)]") { gsub(stem, "REDACTED") }
      { print }
    ' "$f" > "$f.new" || return 1
    mv -- "$f.new" "$f" || return 1
  done
  grep -qE "^Correction [(]round ${REPLAY_ROUND}[)].*REDACTED" -- "$f" || return 1
  return 0
}

# mut_evid_first CASE TREE PAT -- strip the evidence stems from the FIRST
# Correction block of the record only, leaving the record's other correction
# blocks intact.  This is the committed r41-closure.sh selftest_case_i1 shape:
# the record still carries evidence in a sibling block, so a limb that unions
# evidence across blocks (or across records) still sees the full set and the
# defect escapes.  A per-block limb must reject it.
mut_evid_first() {
  local tree=$2 pat=$3 stem ln
  local f="$tree/$pat"
  [ -f "$f" ] || return 1
  [ -n "$REPLAY_ROUND" ] || return 1
  ln=$(grep -nE "^Correction [(]round ${REPLAY_ROUND}[)]" -- "$f" | head -n 1 | cut -d: -f1)
  [ -n "$ln" ] || return 1
  for stem in ${REPLAY_EV}; do
    [ -n "$stem" ] || continue
    sed -i -E "${ln}s#${stem}#REDACTED#g" -- "$f" || return 1
  done
  return 0
}

# mut_tally CASE TREE PAT MODE -- mangle the truth tally token in the record
# PAT.  MODE=first rewrites the first Correction block only (the record still
# mentions the truth tally elsewhere, so a limb that aggregates per record
# still tallies green); MODE=corrections rewrites every Correction block of the
# record; MODE=all rewrites every mention of the truth tally in the record.
mut_tally() {
  local tree=$2 pat=$3 mode=$4
  local f="$tree/$pat"
  local tally=$REPLAY_TALLY bad
  [ -f "$f" ] || return 1
  [ -n "$tally" ] || return 1
  [ -n "$REPLAY_ROUND" ] || return 1
  # the mangled token: the truth tally with its denominator widened by one
  # digit ("closed=10/10" -> "closed=10/100").  It is a strict SUPER-SET of the
  # truth token as a string, so a substring match accepts it while a
  # token-boundary match must not: that is the round-40 wave-2 T2 class.
  case "$tally" in
    */*) bad="${tally%/*}/${tally##*/}0" ;;
    *) bad="${tally}0" ;;
  esac
  [ "$bad" != "$tally" ] || return 1
  case "$mode" in
    all)
      sed -i -E "s#${tally}([^0-9])#${bad}\1#g" -- "$f" || return 1
      ;;
    corrections)
      awk -v tally="$tally" -v bad="$bad" -v rnd="$REPLAY_ROUND" '
        $0 ~ ("^Correction [(]round " rnd "[)]") { gsub(tally, bad) }
        { print }
      ' "$f" > "$f.new" || return 1
      mv -- "$f.new" "$f" || return 1
      ;;
    *)
      # the FIRST Correction block that actually CARRIES the truth tally: a
      # block that does not mention the tally is not the defect, and mangling
      # an arbitrary block would not exercise the clause at all.
      local ln
      ln=$(grep -nE "^Correction [(]round ${REPLAY_ROUND}[)].*${tally}" -- "$f" | head -n 1 | cut -d: -f1)
      [ -n "$ln" ] || return 1
      sed -i -E "${ln}s#${tally}([^0-9])#${bad}\1#g" -- "$f" || return 1
      ;;
  esac
  grep -qF -- "$bad" "$f" || return 1
  return 0
}

# mut_registry CASE TREE PAT MODE -- mutate the registry row of the suite
# instrument inside PAT.  MODE in barepipe|leadspace|mention|blank.
mut_registry() {
  local tree=$2 pat=$3 mode=$4
  local f="$tree/$pat"
  local base=$REPLAY_SUITE_BASE
  [ -f "$f" ] || return 1
  case "$mode" in
    barepipe)
      awk -v base="$base" '
        index($0, "| " base " |") == 1 {
          n = index($0, "|"); rest = substr($0, n + 1)
          m = index(rest, "|"); cell = substr(rest, 1, m - 1)
          if (index(cell, "bash ") == 1) { sub(/bash /, "bash | ", cell) }
          else { cell = cell " |" }
          print "| " cell substr(rest, m)
          next
        }
        { print }
      ' "$f" > "$f.new" || return 1
      mv -- "$f.new" "$f" || return 1
      ;;
    leadspace)
      sed -i -E "s/^\| ${base} \|/\|  ${base} |/" -- "$f" || return 1
      grep -qE "^\|  ${base} \|" -- "$f" || return 1
      ;;
    mention)
      grep -v -E "^\| ${base} \|" -- "$f" > "$f.new" || return 1
      mv -- "$f.new" "$f" || return 1
      printf '\nThe instrument %s is great and closes the round.\n' "$base" >> "$f"
      ;;
    blank)
      awk -v base="$base" '
        index($0, "| " base " |") == 1 { print "" }
        { print }
      ' "$f" > "$f.new" || return 1
      mv -- "$f.new" "$f" || return 1
      ;;
    *)
      return 1
      ;;
  esac
  return 0
}

# mut_declared CASE TREE PAT MODE -- mutate the declaration file PAT.
# MODE in drop|short|symlink.
mut_declared() {
  local case=$1 tree=$2 pat=$3 mode=$4
  local f="$tree/$pat" p
  [ -f "$f" ] || return 1
  case "$mode" in
    drop)
      # remove the declaration of a path the round actually changed: the
      # declared set no longer covers the changed set.
      p=$(head -n 1 "$REPLAY_CHANGED_LIST" 2>/dev/null)
      if [ -z "$p" ] || ! grep -qF -x -- "$p" "$f"; then
        p=$(awk 'NF>=3 {print $1; exit}' "$f")
      fi
      [ -n "$p" ] || return 1
      grep -v -F -x -- "$p" "$f" > "$f.new" || return 1
      mv -- "$f.new" "$f" || return 1
      ;;
    short)
      awk 'BEGIN{done=0} !done && NF>=3 { $2 = $2 - 1; done=1 } { print }' "$f" > "$f.new" || return 1
      mv -- "$f.new" "$f" || return 1
      ;;
    symlink)
      # make a declared path a symlink whose bytes live outside the export
      p=$(awk 'NF>=3 {print $1; exit}' "$f")
      [ -n "$p" ] || return 1
      [ -e "$tree/$p" ] || return 1
      local outside="$case/outside/$(basename -- "$p")"
      replay__mkdir "$(dirname -- "$outside")" || return 1
      cp -a -- "$tree/$p" "$outside" || return 1
      rm -f -- "$tree/$p" || return 1
      ln -s -- "$outside" "$tree/$p" || return 1
      ;;
    *)
      return 1
      ;;
  esac
  return 0
}

# ---------------------------------------------------------------------------
# the case runner
# ---------------------------------------------------------------------------

# replay__paths_for FAMILY -> relative paths the fixture must carry
replay__paths_for() {
  case "$1" in
    F-EVID|F-TOKEN)
      printf '%s\n' $REPLAY_RECORDS
      printf 'SKILL.md\nPROVINCE.md\n'
      printf '%s\n' $REPLAY_LESSONS
      # A limb may GROUND each declared evidence identifier in the committed
      # wave-2 artifact that carries it and fail `evidence-not-grounded` when
      # the files are absent (the round-42 J1 does exactly this).
      #
      # The grounding round is NOT the running suite's round: the r42 J1
      # audits the round-41 correction blocks and therefore grounds under
      # .ufo/waves/round-40/wave2 even when the r42 suite runs.  Deriving the
      # directory from the suite's round token would carry the wrong tree and
      # red the PRISTINE control, i.e. grade nothing for the wrong reason.
      # Carry every round-4x wave-2 tree the export holds: a superset can only
      # help a grounding limb, and the control run decides whether the fixture
      # is usable at all.
      local d
      for d in "$REPLAY_BASE"/.ufo/waves/round-4*/wave2; do
        [ -d "$d" ] || continue
        printf '%s\n' "${d#"$REPLAY_BASE"/}"
      done
      ;;
    F-TABLE)
      printf 'SKILL.md\n'
      ;;
    F-DECL)
      printf '%s\n' "$REPLAY_DECLARED"
      # every path the declaration file names, so the tail checks still hold
      # and the only difference is the mutation under test
      if [ -f "$REPLAY_BASE/$REPLAY_DECLARED" ]; then
        awk 'NF>=3 {print $1}' "$REPLAY_BASE/$REPLAY_DECLARED"
      fi
      ;;
    F-SCAN)
      :
      ;;
    F-BIND|F-FLIP)
      printf 'corpus\n'
      ;;
    *)
      :
      ;;
  esac
}

# replay__build_scratch CASE VAR KIND -- build the scratch state the scan limb
# reads.  KIND is control|mutant.
replay__build_scratch() {
  local case=$1 kind=$2
  local scanroot="$case/scan"
  local work="$case/scan/work" straydir
  replay__mkdir "$scanroot" || return 1
  replay__mkdir "$work" || return 1
  straydir=${REPLAY_STRAY_DIR:-$(dirname -- "$scanroot")}
  [ "$kind" = control ] && return 0
  case "$REPLAY_CASE_ID" in
    s1.*)
      replay__mkdir "$straydir" || return 1
      mkdir -p -- "$straydir/$REPLAY_FAMILY-replay-outside" 2>/dev/null || return 1
      ;;
    s2.*) mkdir -p -- "$scanroot/$(printf '%s' "$REPLAY_FAMILY" | tr 'A-Z' 'a-z' | tr -c 'a-z0-9' '_')_sep" 2>/dev/null || return 1 ;;
    s3.*) mkdir -p -- "$scanroot/.${REPLAY_FAMILY}-seat" 2>/dev/null || return 1 ;;
    s4.*) mkdir -p -- "$scanroot/container/$REPLAY_FAMILY-nested" 2>/dev/null || return 1 ;;
    s5.*) ln -s -- "$(dirname -- "$scanroot")" "$scanroot/$REPLAY_FAMILY-ancestor" 2>/dev/null || return 1 ;;
    s6.*) rm -rf -- "$scanroot"; scanroot="$case/no-such-root" ;;
    s7.*) mkdir -p -- "$scanroot/$REPLAY_FAMILY-locked" && chmod 000 "$scanroot/$REPLAY_FAMILY-locked" 2>/dev/null || return 1 ;;
    s8.*) mkdir -p -- "$scanroot/$REPLAY_SIBLING_FAMILY-sibling-stray" 2>/dev/null || return 1 ;;
  esac
  return 0
}

# replay__invoke KIND SPEC CASE TREE SCANROOT -> sets replay__out and
# replay__rc
replay__invoke() {
  local kind=$1 spec=$2 case=$3 tree=$4 scanroot=$5
  local out rc
  case "$kind" in
    py)
      local instr=${spec#py:} path args
      path=${instr%% *}
      args=${instr#* }
      [ "$args" = "$instr" ] && args=''
      args=${args//ROOT/$tree}
      # Run the instrument from the FIXTURE tree, i.e. the export of the ref
      # under test, never from the live working tree: the suite is export-mode
      # only so that an uncommitted edit cannot turn a check green, and an
      # instrument read from the working tree would break that guarantee (a
      # concurrent seat's edit would silently change this verdict).
      out=$(cd "$tree" && python3 "$tree/$path" $args 2>&1); rc=$?
      ;;
    fn)
      local fn=${spec%% *} fnargs
      fnargs=${spec#* }
      [ "$fnargs" = "$spec" ] && fnargs=''
      fnargs=${fnargs//TREE/$tree}
      fnargs=${fnargs//REF/$REPLAY_REF}
      out=$(
        (
          # source the suite first: its own top-level assignments would
          # otherwise overwrite the overrides below
          if ! declare -F "$fn" >/dev/null 2>&1; then
            . "$REPLAY_SUITE"
          fi
          EXPORT=$tree
          WORK=$case/scan/work
          MUT=$case/mut
          PAYFILE=$case/payloads.tsv
          SELFILE=$case/selftest.tsv
          REF=$REPLAY_REF
          REF_RESOLVED=$REPLAY_REF
          LANE=$REPLAY_LANE
          SCRATCH_ROOT=$scanroot
          BASE_REF=$REPLAY_BASE_REF
          if [ -n "$fnargs" ]; then
            # shellcheck disable=SC2086
            "$fn" $fnargs
          else
            "$fn" "$tree" "$REPLAY_REF"
          fi
        ) 2>&1
      ); rc=$?
      ;;
    *)
      replay__log "unknown limb kind $kind"
      return 2
      ;;
  esac
  replay__out=$out
  replay__rc=$rc
  return 0
}

# replay_run_case CASE_ID MODE -> 0 rejected, 1 accepted, 2 ungraded
replay_run_case() {
  local cid=$1 mode=$2
  REPLAY_CASE_ID=$cid
  local fam
  fam=$(replay_case_field "$cid" 1)
  [ -n "$fam" ] || { replay__log "unknown case $cid"; return 2; }

  local kind spec
  spec=$(replay_limb_resolve "$fam") || {
    replay__log "no limb resolved for family $fam"; return 2
  }
  kind=${spec%%$'\t'*}; spec=${spec#*$'\t'}

  local case="$REPLAY_CASE_ROOT/$cid"
  rm -rf -- "$case" 2>/dev/null
  replay__mkdir "$case" || return 2

  # ---- control fixture: pristine ------------------------------------------
  local ctree="$case/control/tree"
  replay__mkdir "$ctree" || return 2
  if [ "$mode" = export ]; then
    replay__export_tree "$REPLAY_LANE" "$REPLAY_REF" "$ctree" || {
      replay__log "export of $REPLAY_REF failed"; return 2
    }
  else
    local paths
    paths=$(replay__paths_for "$fam")
    [ -n "$paths" ] && printf '%s\n' "$paths" | replay__cp_paths "$REPLAY_BASE" "$ctree"
  fi
  replay__build_scratch "$case" control || return 2
  replay__invoke "$kind" "$spec" "$case" "$ctree" "$case/scan" || return 2
  local ctrl_out=$replay__out ctrl_rc=$replay__rc
  printf '%s' "$ctrl_out" > "$case/control.out" 2>/dev/null || true

  local ctrl_bad=0
  [ "$ctrl_rc" -ne 0 ] && ctrl_bad=1
  case "$ctrl_out" in *"closed=0"*) ctrl_bad=1 ;; esac
  if [ "$ctrl_bad" = 1 ]; then
    replay__log "control for $cid is red (rc=$ctrl_rc): verdict not attributable"
    return 2
  fi

  # ---- mutant fixture: same fixture, mutated ------------------------------
  local mtree="$case/mutant/tree"
  replay__mkdir "$mtree" || return 2
  if [ "$mode" = export ]; then
    replay__export_tree "$REPLAY_LANE" "$REPLAY_REF" "$mtree" || return 2
  else
    local paths
    paths=$(replay__paths_for "$fam")
    [ -n "$paths" ] && printf '%s\n' "$paths" | replay__cp_paths "$REPLAY_BASE" "$mtree"
  fi

  local recs rec ok=1
  recs=$(printf '%s\n' $REPLAY_RECORDS)
  case "$cid" in
    e1.*) rec=$(printf '%s\n' "$recs" | sed -n 1p) ;;
    e2.*) rec=$(printf '%s\n' "$recs" | sed -n 2p) ;;
    e3.*) rec=$(printf '%s\n' "$recs" | sed -n 3p) ;;
    *) rec=$(printf '%s\n' "$recs" | sed -n 1p) ;;
  esac
  case "$cid" in
    e1.*|e2.*|e3.*) mut_evid "$case" "$mtree" "$rec" || ok=0 ;;
    e4.*)
      # the committed union mutant: FIRST block only, in every record
      for rec in $recs; do
        mut_evid_first "$case" "$mtree" "$rec" || { ok=0; break; }
      done
      ;;
    t1.*) mut_tally "$case" "$mtree" "$rec" first || ok=0 ;;
    t2.*) mut_tally "$case" "$mtree" "$rec" corrections || ok=0 ;;
    t3.*) mut_tally "$case" "$mtree" "$rec" all || ok=0 ;;
    b1.*) mut_registry "$case" "$mtree" SKILL.md barepipe || ok=0 ;;
    b2.*) mut_registry "$case" "$mtree" SKILL.md leadspace || ok=0 ;;
    b3.*) mut_registry "$case" "$mtree" SKILL.md mention || ok=0 ;;
    b4.*) mut_registry "$case" "$mtree" SKILL.md blank || ok=0 ;;
    d1.*) mut_declared "$case" "$mtree" "$REPLAY_DECLARED" drop || ok=0 ;;
    d2.*) mut_declared "$case" "$mtree" "$REPLAY_DECLARED" symlink || ok=0 ;;
    d3.*) mut_declared "$case" "$mtree" "$REPLAY_DECLARED" short || ok=0 ;;
    s1.*|s2.*|s3.*|s4.*|s5.*|s6.*|s7.*|s8.*|c1.*|c2.*|c3.*|p1.*|p2.*) ok=1 ;;
    *) ok=0 ;;
  esac
  if [ "$ok" != 1 ]; then
    replay__log "mutation for $cid could not be applied"; return 2
  fi
  replay__build_scratch "$case" mutant || return 2

  # ---- mutate the corpus for the instrument limbs -------------------------
  case "$cid" in
    c1.*|c2.*|c3.*)
      python3 - "$mtree" "$cid" <<'PYEOF' || ok=0
import glob, json, os, sys
root, cid = sys.argv[1], sys.argv[2]
manifests = sorted(glob.glob(os.path.join(root, "corpus/source-snapshots/*/manifest.json")))
if not manifests:
    sys.exit(3)
path = manifests[-1]
with open(path) as fh:
    data = json.load(fh)
recs = data.get("sources") or []
if not recs:
    sys.exit(4)
rec = recs[-1]
if cid.startswith("c1"):
    # the record's path names a file that does not exist.  The old capture is
    # removed with it, so the ONLY defect present is the dangling path: the
    # orphan rule cannot fire and mask the missing-path defect.
    old = rec.get("path")
    rec["path"] = "%s-missing.txt" % rec.get("id", "X")
    for k in ("files",):
        if isinstance(rec.get(k), list):
            rec[k] = ["%s-missing.txt" % rec.get("id", "X")]
    if old:
        try:
            os.remove(os.path.join(os.path.dirname(path), old))
        except OSError:
            pass
elif cid.startswith("c2"):
    # the URL differs from the registry row in CASE only
    for k in ("url", "capture_url"):
        if rec.get(k):
            rec[k] = rec[k].replace("/rfc/", "/RFC/")
else:
    # the URL carries a trailing slash the registry row does not have
    for k in ("url", "capture_url"):
        if rec.get(k):
            rec[k] = rec[k] + "/"
with open(path, "w") as fh:
    json.dump(data, fh, indent=2)
    fh.write("\n")
PYEOF
      ;;
    p1.*|p2.*)
      python3 - "$mtree" "$cid" <<'PYEOF' || ok=0
import os, re, sys
root, cid = sys.argv[1], sys.argv[2]
readme = os.path.join(root, "corpus/README.md")
if not os.path.isfile(readme):
    sys.exit(3)
with open(readme) as fh:
    lines = fh.read().split("\n")
if cid.startswith("p1"):
    hit = None
    for i, line in enumerate(lines):
        if re.match(r"^\|\s*F\d+\s*\|", line) and "| admitted |" in line:
            hit = i
    if hit is None:
        sys.exit(4)
    lines[hit] = lines[hit].replace("| admitted |", "| explored |", 1)
else:
    lines.append("| F999 | fixture topic | admitted | knowledge/fixture.md | | selftest fixture |")
with open(readme, "w") as fh:
    fh.write("\n".join(lines))
PYEOF
      ;;
  esac
  if [ "$ok" != 1 ]; then
    replay__log "corpus mutation for $cid could not be applied"; return 2
  fi

  # ---- invoke the limb on the mutant --------------------------------------
  replay__invoke "$kind" "$spec" "$case" "$mtree" "$case/scan" || return 2
  local mut_out=$replay__out mut_rc=$replay__rc
  printf '%s' "$mut_out" > "$case/mutant.out" 2>/dev/null || true

  replay__log "case=$cid family=$fam limb=$kind:$spec control_rc=$ctrl_rc mutant_rc=$mut_rc"
  replay__log "control payload: $(printf '%s' "$ctrl_out" | tail -n 1)"
  replay__log "mutant  payload: $(printf '%s' "$mut_out" | tail -n 1)"

  local rejected=0
  [ "$mut_rc" -ne 0 ] && rejected=1
  case "$mut_out" in *"closed=0"*) rejected=1 ;; esac
  [ "$rejected" = 1 ] && return 0
  return 1
}

# ---------------------------------------------------------------------------
# public entry points
# ---------------------------------------------------------------------------

# replay_init -> discover suite/lane/ref and prepare the scratch base.
# Idempotent: the derived state is computed once and reused, so a caller may
# invoke it defensively.  REPLAY_SUITE is an INPUT (the suite to test) and is
# captured into REPLAY_SUITE_ENV before the resolved path is written back, so
# a second init does not lose the caller's choice.
replay_init() {
  # Idempotent, but only while the base export is still present: replay_cleanup
  # removes the case root (and with it the base export), so a cached init whose
  # base has been cleaned away must be redone rather than reused.
  if [ "${REPLAY_INIT_DONE:-0}" = 1 ] && [ -d "${REPLAY_BASE:-}" ]; then
    return 0
  fi
  REPLAY_SUITE_ENV=${REPLAY_SUITE_ENV:-${REPLAY_SUITE:-}}
  REPLAY_SUITE=$(replay_suite_file "${REPLAY_LANE:-${LANE:-}}") || \
    replay__die "no closure suite found (set REPLAY_SUITE)"
  REPLAY_LANE=$(replay_lane_dir "$REPLAY_SUITE") || replay__die "no lane for $REPLAY_SUITE"
  REPLAY_REF=${REPLAY_REF:-${REF_RESOLVED:-}}
  if [ -z "$REPLAY_REF" ]; then
    REPLAY_REF=$(git -C "$REPLAY_LANE" rev-parse HEAD 2>/dev/null) || replay__die "no ref"
  fi
  REPLAY_BASE_REF=${REPLAY_BASE_REF:-${BASE_REF:-$REPLAY_REF}}
  REPLAY_SUITE_BASE=${REPLAY_SUITE_BASE:-${REPLAY_SUITE##*/}}
  REPLAY_ROUND=$(replay_suite_round "$REPLAY_SUITE") || REPLAY_ROUND=''
  REPLAY_FAMILY=$(replay_suite_family "$REPLAY_SUITE") || REPLAY_FAMILY='kasegi-r42'
  # the sibling round's family: the claim's J5 requires the scratch scan to
  # cover the whole kasegi-r4[0-9]* prefix, not only this round's own family
  if [ -n "$REPLAY_ROUND" ] && [ "$REPLAY_ROUND" -gt 40 ] 2>/dev/null; then
    REPLAY_SIBLING_FAMILY="${REPLAY_FAMILY%r*}r$((REPLAY_ROUND - 1))"
  else
    REPLAY_SIBLING_FAMILY='kasegi-r41'
  fi

  REPLAY_TALLY=$(replay_suite_tally "$REPLAY_SUITE") || REPLAY_TALLY=''
  REPLAY_RECORDS=$(replay_suite_records "$REPLAY_SUITE") || REPLAY_RECORDS='SCORECARD.md LOG.md SHONEN.md'
  REPLAY_EV=$(replay_suite_evidence "$REPLAY_SUITE") || REPLAY_EV='RevC1Counters CritKillRule MutH6H10'
  REPLAY_LESSONS=$(replay_suite_words "$REPLAY_SUITE" LESSONS) || REPLAY_LESSONS=''
  REPLAY_DECLARED=$(replay_suite_declared "$REPLAY_SUITE") || REPLAY_DECLARED=''
  REPLAY_SCRATCH=${REPLAY_SCRATCH:-${TMPDIR:-/tmp}}
  REPLAY_CASE_ROOT="$REPLAY_SCRATCH/replay-$$"
  replay__mkdir "$REPLAY_CASE_ROOT" || replay__die "no scratch"

  # The base export lives OUTSIDE the case root: replay_cleanup removes the
  # case root, and a caller that replays several artifacts in sequence must
  # not lose the base export between calls.
  REPLAY_BASE_ROOT="$REPLAY_SCRATCH/replay-base-$$"
  REPLAY_BASE="$REPLAY_BASE_ROOT/base"
  if [ -n "${REPLAY_EXPORT:-${EXPORT:-}}" ] && [ -d "${REPLAY_EXPORT:-${EXPORT:-}}" ]; then
    REPLAY_BASE=${REPLAY_EXPORT:-${EXPORT:-}}
  else
    replay__mkdir "$REPLAY_BASE_ROOT" || replay__die "no scratch"
    replay__export_tree "$REPLAY_LANE" "$REPLAY_REF" "$REPLAY_BASE" || replay__die "export failed"
  fi

  # the round's changed-path set, used by the declaration-completeness defeat
  REPLAY_CHANGED="$REPLAY_BASE_ROOT/changed.txt"
  REPLAY_CHANGED_LIST="$REPLAY_CHANGED"
  git -C "$REPLAY_LANE" diff --name-only "$REPLAY_BASE_REF" "$REPLAY_REF" -- > "$REPLAY_CHANGED" 2>/dev/null || true
  [ -s "$REPLAY_CHANGED" ] || : > "$REPLAY_CHANGED"
  REPLAY_INIT_DONE=1
  return 0
}

# replay_cleanup -> remove the materialized case root (and the base export
# when the library owns it; an externally supplied REPLAY_EXPORT is never
# touched)
replay_cleanup() {
  [ "${REPLAY_KEEP:-0}" = 1 ] && return 0
  [ -n "${REPLAY_CASE_ROOT:-}" ] && rm -rf -- "$REPLAY_CASE_ROOT" 2>/dev/null
  if [ -n "${REPLAY_BASE_ROOT:-}" ] && [ -d "$REPLAY_BASE_ROOT" ]; then
    rm -rf -- "$REPLAY_BASE_ROOT" 2>/dev/null
  fi
  REPLAY_INIT_DONE=0
  return 0
}

# replay_defeat ARTIFACT MODE
replay_defeat() {
  local want=${1:-all} mode=${2:-fixture}
  if [ "$mode" = list ]; then
    replay_catalog_rows "$want"
    return 0
  fi
  case "$mode" in
    fixture|export) ;;
    *) replay__die "unknown mode: $mode" ;;
  esac
  replay_init
  local rows id rc worst=0
  rows=$(replay_catalog_rows "$want")
  [ -n "$rows" ] || { replay__log "no catalog row for $want"; return 2; }
  for id in $(printf '%s\n' "$rows" | cut -f1); do
    replay_run_case "$id" "$mode"
    rc=$?
    case $rc in
      0) ;;
      1) worst=1 ;;
      *) worst=2 ;;
    esac
  done
  replay_cleanup
  return $worst
}

# replay_report [MODE] -> print one verdict line per catalog case on stdout
replay_report() {
  local mode=${1:-fixture}
  replay_init
  local id rc worst=0 out
  printf 'case\tfamily\tartifact\tverdict\trc\tpayload\n'
  for id in $(replay_catalog_rows all | cut -f1); do
    replay_run_case "$id" "$mode"
    rc=$?
    out=''
    [ -f "$REPLAY_CASE_ROOT/$id/mutant.out" ] && out=$(tail -n 1 -- "$REPLAY_CASE_ROOT/$id/mutant.out")
    case $rc in
      0) printf '%s\t%s\t%s\tREJECTED\t%s\t%s\n' "$id" "$(replay_case_field "$id" 1)" "$(replay_case_field "$id" 2)" "$rc" "$out" ;;
      1) printf '%s\t%s\t%s\tACCEPTED\t%s\t%s\n' "$id" "$(replay_case_field "$id" 1)" "$(replay_case_field "$id" 2)" "$rc" "$out" ;;
      *) printf '%s\t%s\t%s\tUNGRADED\t%s\t%s\n' "$id" "$(replay_case_field "$id" 1)" "$(replay_case_field "$id" 2)" "$rc" "$out" ;;
    esac
    [ "$rc" -gt "$worst" ] && worst=$rc
  done
  replay_cleanup
  return $worst
}
