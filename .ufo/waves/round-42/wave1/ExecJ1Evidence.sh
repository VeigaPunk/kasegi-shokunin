#!/usr/bin/env bash
# ExecJ1Evidence.sh -- J1 limb for the round-42 closure suite (family F-EVID).
#
#   source ExecJ1Evidence.sh
#   check_j1 <export-root>
#
# check_j1 prints exactly one line to stdout:
#
#   J1 payload=<k=v,...> closed=0|1
#
# and returns 0 when closed=1, 1 when closed=0.  It reads bytes only under the
# export root it is handed; it never touches the working tree, the lane or the
# network, and it writes nothing at all.
#
# WHAT J1 GRADES
#
# The round-41 limb I1 tallied the firing evidence identifiers as a UNION over
# the records: the identifiers seen in ANY qualified correction of ANY record
# were counted once (r41-closure.sh lines 902-906).  A correction whose
# evidence names had been removed therefore left the aggregate at evidence=3/3
# and the check green.  That is the committed defeat of this family
# (.ufo/waves/round-41/wave2/CritC1KillRule.md and RevC1Counters.md, finding
# 2): the fixture removes the evidence from one correction and the aggregate
# does not move.
#
# J1 keeps the population I1 held and fixes the aggregation.  For every
# audited correction block (the `Correction (round N)` line sets in SCORECARD.md,
# LOG.md and SHONEN.md), the MEMBERS of that block are the outside-fence
# `Correction (round N)` lines that name the audited claim (C1) and the round
# the correction corrects (N-1).  Every member is then graded ON ITS OWN:
#
#   (a) the correction grades the named overclaim NOT verified, and
#   (b) the correction names EVERY firing evidence identifier of that round.
#
# The verdict phrase and the evidence identifiers are NOT part of the member
# selection: a correction that has lost its verdict, or that has lost its
# evidence names, is still a member and must be graded.  There is no
# cross-record and no cross-correction set operation anywhere in the tally --
# `graded` and `evidence` count the members that pass, and the check closes
# only when every member of every block of every record passes.  A record with
# no member in an audited block is `missing`, which is also a failure.
#
# The identifiers are matched as WHOLE tokens of the correction line: the
# character either side of an occurrence may not be a letter, a digit or an
# underscore, so `wave2/RevC1Counters.defeats.txt` names `RevC1Counters` while
# the superstring `RevC1CountersX` does not (the whole-token intent of
# claims-erratum-2 E6).  The verdict vocabulary is the one I1 used
# (`not verified` / `unverified` / `withdraw`).  The fence state machine is
# the one I1 used (CommonMark 4.5), so a fenced pseudo-correction is not a
# member.
#
# ROUND TABLE AND GROUNDING
#
# J1_ROUNDS lists the audited correction blocks; J1_EVIDENCE_MAP[<N>] lists the
# firing evidence identifiers each block's members must name.  A listed round
# with no declared identifiers is a configuration error and fails closed, and
# every declared identifier must resolve to a committed artifact under the
# export's `.ufo/waves/round-<N-1>/wave2/` directory (`evidence-not-grounded`
# otherwise), so the identifier list cannot drift from the repository.  The
# defaults audit the round-41 blocks -- the population in which the round-41
# union defect lived -- with the three committed round-40 wave-2 defeat
# artifacts those corrections cite.
#
# REPLAY (family F-EVID)
#
# j1_selftest_export <export-root> <work-dir> materialises this family's
# committed defeat and five fresh mutants over a COPY of the export and grades
# the current bytes of this limb against them:
#
#   M1 committed union mutant -- in every record the first `Correction
#      (round 41)` line is replaced by the round-41 selftest's own evidence-free
#      replacement (the committed defeat of I1, CritC1KillRule.md /
#      RevC1Counters.md).  The union tally stays 3/3; J1 must reject it.
#   M2 one member names only two of the three identifiers -- J1 must reject it.
#   M3 one member's verdict phrase is softened -- J1 must reject it.
#   M4 one member is moved inside a CommonMark fence -- J1 must reject it.
#   M5 one record's whole member set is deleted -- J1 must reject it.
#   M6 one member names a SUPERSTRING of an identifier -- J1 must reject it.
#
# The fixture copies the record files AND the grounding artifacts, so a mutant
# is rejected for the defect under test and never for a missing artifact.
#
# and prints one graded line per case:
#
#   selftest case=J1 mutants=<ok>/<n> positive=pass|fail verdict=pass|fail
#
# Exit 0 only when the positive export passes and every mutant is rejected.
#
# All helpers are prefixed `j1_` except `check_j1` itself, so the limb can be
# sourced next to the suite's own helpers without a name collision.

# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------

# The audited correction blocks.
J1_ROUNDS=(41)

# The claim the corrections grade, and the record files they live in.
J1_CLAIM=C1
J1_RECORDS=(SCORECARD.md LOG.md SHONEN.md)

# The firing evidence identifiers every member of a block must name, keyed by
# the audited round.  For round 41 these are the three committed round-40
# wave-2 defeat artifacts the round-41 corrections cite.  Add a round here to
# audit a further correction block (grounding then resolves the identifiers
# under `.ufo/waves/round-<ROUND-1>/wave2/`).
declare -A J1_EVIDENCE_MAP=(
  [41]='RevC1Counters CritKillRule MutH6H10'
)

# The verdict vocabulary that grades an overclaim as not verified.  Same
# vocabulary the round-41 limb used.
J1_VERDICT='not[ _-]?verified|unverified|withdraw'

# Set by check_j1 for callers that grade payload values rather than the
# printed line.
J1_PAYLOAD=
J1_CLOSED=

# ---------------------------------------------------------------------------
# the CommonMark fence state machine (4.5, fenced code blocks)
#
# opener : up to 3 leading spaces, a run of >= 3 identical ` or ~; a backtick
#          fence's info string may not contain a backtick.
# closer : up to 3 leading spaces, a run of the SAME marker at least as long as
#          the opener's run, and nothing but spaces or tabs after it.
# A different marker never closes an open fence and a shorter run of the same
# marker is content.  Every line of a fenced block -- including the delimiters
# -- is INSIDE and therefore excluded from every line-anchored count.
# ---------------------------------------------------------------------------

J1_FENCE_AWK='
function fence_open(line,   i, n, c, run, rest) {
  i = 1; n = 0
  while (n < 3 && substr(line, i, 1) == " ") { n++; i++ }
  if (substr(line, i, 1) == " ") return 0
  c = substr(line, i, 1)
  if (c != "`" && c != "~") return 0
  run = 0
  while (substr(line, i + run, 1) == c) run++
  if (run < 3) return 0
  rest = substr(line, i + run)
  if (c == "`" && index(rest, "`") > 0) return 0
  FENCE_CHAR = c; FENCE_LEN = run
  return 1
}
function fence_close(line,   i, n, c, run, rest) {
  if (FENCE_CHAR == "") return 0
  i = 1; n = 0
  while (n < 3 && substr(line, i, 1) == " ") { n++; i++ }
  if (substr(line, i, 1) == " ") return 0
  c = substr(line, i, 1)
  if (c != FENCE_CHAR) return 0
  run = 0
  while (substr(line, i + run, 1) == c) run++
  if (run < FENCE_LEN) return 0
  rest = substr(line, i + run)
  if (rest ~ /[^ \t]/) return 0
  return 1
}
BEGIN { in_fence = 0; FENCE_CHAR = ""; FENCE_LEN = 0; hit = 0 }
{
  line = $0
  if (in_fence) {
    inside = 1
    if (fence_close(line)) { in_fence = 0; FENCE_CHAR = ""; FENCE_LEN = 0 }
  } else {
    if (fence_open(line)) { in_fence = 1; inside = 1 }
    else inside = 0
  }
  if (!inside && pat != "" && line ~ pat) { print NR "\t" line; hit++ }
}
'

# j1_fence_match FILE ERE -- the OUTSIDE-fence lines of FILE matching ERE,
# each prefixed with its line number.
j1_fence_match() { # FILE ERE
  local file=$1 pat=${2:-}
  [ -f "$file" ] || return 1
  awk -v pat="$pat" "$J1_FENCE_AWK" "$file"
}

# j1_evidence_for ROUND -- the firing evidence identifiers of ROUND, one per
# line.  Returns 1 when ROUND has no declared identifiers (a configuration
# error: the caller fails closed rather than grading vacuously).
j1_evidence_for() { # [ROUND]
  local ids=${J1_EVIDENCE_MAP[${1:-${J1_ROUNDS[0]}}]:-}
  [ -n "$ids" ] || return 1
  printf '%s\n' $ids
  return 0
}

# j1_members FILE ROUND -- the population members of ROUND's block in FILE: the
# outside-fence `Correction (round <ROUND>)` lines that name the audited claim
# and the round the correction corrects (ROUND-1).  The verdict phrase and the
# evidence identifiers are NOT part of this selection: a correction that has
# lost its verdict, or that has lost its evidence names, is still a member and
# must be graded.
j1_members() { # FILE [ROUND]
  local file=$1
  local round=${2:-${J1_ROUNDS[0]}}
  local prior=$((round - 1))
  j1_fence_match "$file" "^Correction [(]round ${round}[)]" \
    | grep -E "(^|[^A-Za-z0-9])${J1_CLAIM}([^A-Za-z0-9]|\$)" \
    | grep -iE "round[ -]?${prior}([^0-9]|\$)|r${prior}([^A-Za-z0-9]|\$)"
}

# j1_has_verdict LINE -- 1 when LINE grades the overclaim as not verified.
j1_has_verdict() { # LINE
  printf '%s\n' "$1" | grep -qiE "$J1_VERDICT"
}

# j1_token_present LINE ID -- TRUE when ID occurs in LINE as a WHOLE token: the
# characters either side of the occurrence must not be a letter, a digit or an
# underscore.  The citations the corrections use are path-shaped
# (`wave2/RevC1Counters.defeats.txt`), so `/` and `.` are legitimate
# boundaries; a superstring such as `RevC1CountersX` is not a naming of
# `RevC1Counters` and must not satisfy the limb.  Same whole-token intent as
# claims-erratum-2 E6, applied to the evidence identifiers.
j1_token_present() { # LINE ID
  awk -v id="$2" '{
    rest = $0
    while ((i = index(rest, id)) > 0) {
      before = (i == 1) ? "" : substr(rest, i - 1, 1)
      after  = substr(rest, i + length(id), 1)
      bok = (before == "") || (before !~ /[A-Za-z0-9_]/)
      aok = (after  == "") || (after  !~ /[A-Za-z0-9_]/)
      if (bok && aok) found = 1
      rest = substr(rest, i + 1)
    }
  } END { exit(found ? 0 : 1) }' <<< "$1"
}

# j1_has_evidence LINE ROUND -- 1 when LINE names EVERY firing evidence
# identifier of ROUND, each as a whole token.
j1_has_evidence() { # LINE [ROUND]
  local line=$1
  local round=${2:-${J1_ROUNDS[0]}}
  local id
  while IFS= read -r id; do
    [ -n "$id" ] || continue
    j1_token_present "$line" "$id" || return 1
  done < <(j1_evidence_for "$round")
  return 0
}

# j1_grounded ROUND EXPORT_ROOT -- 1 when EVERY firing evidence identifier of
# ROUND resolves to at least one COMMITTED artifact under the export's
# `.ufo/waves/round-<ROUND-1>/wave2/` directory.  This grounds the identifier
# list in the repository: an identifier that names nothing on disk cannot
# satisfy a correction, so the limb cannot be satisfied by naming invented
# strings.  The artifacts are the round-40 wave-2 defeat files the round-41
# corrections cite.
j1_grounded() { # [ROUND] EXPORT_ROOT
  local round=${1:-${J1_ROUNDS[0]}}
  local tree=$2 id n found
  local dir="$tree/.ufo/waves/round-$((round - 1))/wave2"
  [ -d "$dir" ] || return 1
  while IFS= read -r id; do
    [ -n "$id" ] || continue
    found=0
    n=$(find "$dir" -maxdepth 1 -type f -name "${id}*" 2>/dev/null | wc -l)
    [ "$n" -gt 0 ] && found=1
    [ "$found" -eq 1 ] || return 1
  done < <(j1_evidence_for "$round")
  return 0
}

# j1_qualified FILE ROUND -- the round-41 QUALIFIED population of ROUND's block
# in FILE: the members that also carry the not-verified verdict.  This is
# exactly the population the round-41 limb tallied.
j1_qualified() { # FILE [ROUND]
  j1_members "$1" "${2:-${J1_ROUNDS[0]}}" | grep -iE "$J1_VERDICT"
}

# j1_union_evidence ROUND FILE... -- the round-41 UNION tally: the number of
# DISTINCT firing identifiers seen anywhere in the QUALIFIED population of the
# block, across all the given records.  This is the defective aggregation the
# round-41 limb used (r41-closure.sh lines 902-906, whose `seen` accumulator
# spans the records); it is kept here only so the selftest can show that it
# stays 3/3 on the committed union mutant while J1 rejects it.
j1_union_evidence() { # [ROUND] FILE...
  local round=${1:-${J1_ROUNDS[0]}}
  case ${1:-} in ''|*[!0-9]*) ;; *) shift ;; esac
  local f line id seen=' ' n=0
  for f in "$@"; do
    [ -f "$f" ] || continue
    while IFS=$'\t' read -r _ line; do
      while IFS= read -r id; do
        [ -n "$id" ] || continue
        case "$seen" in *" $id "*) continue ;; esac
        case "$line" in
          *"$id"*) seen="$seen$id "; n=$((n + 1)) ;;
        esac
      done < <(j1_evidence_for "$round")
    done < <(j1_qualified "$f" "$round")
  done
  printf '%s' "$n"
}

# check_j1 EXPORT_ROOT -- grade every correction individually.  Prints one
# `J1 payload=... closed=0|1` line and returns 0 iff closed=1.
check_j1() { # EXPORT_ROOT
  local tree=$1
  local f round line graded=0 evidence=0 members=0 missing=0 detail='' fail=''
  local nr=0 rounds=${#J1_ROUNDS[@]}
  if [ -z "$tree" ] || [ ! -d "$tree" ]; then
    J1_PAYLOAD='records=0,rounds=0,lines=0,graded=0/0,evidence=0/0,missing=0,detail=none,fail=export-root-missing'
    J1_CLOSED=0
    printf 'J1 payload=%s closed=0\n' "$J1_PAYLOAD"
    return 1
  fi
  for f in "${J1_RECORDS[@]}"; do
    [ -f "$tree/$f" ] && nr=$((nr + 1))
  done
  for round in "${J1_ROUNDS[@]}"; do
    local ids
    if ! ids=$(j1_evidence_for "$round"); then
      fail="${fail}${fail:+;}round-${round}:evidence-table-missing"
      continue
    fi
    if ! j1_grounded "$round" "$tree"; then
      fail="${fail}${fail:+;}round-${round}:evidence-not-grounded"
      continue
    fi
    for f in "${J1_RECORDS[@]}"; do
      if [ ! -f "$tree/$f" ]; then
        missing=$((missing + 1))
        detail="${detail}${detail:+;}${f}:missing"
        continue
      fi
      local rec_members=0 rec_graded=0 rec_evidence=0
      while IFS=$'\t' read -r ln line; do
        [ -n "$ln" ] || continue
        members=$((members + 1))
        rec_members=$((rec_members + 1))
        local v=0 e=0
        j1_has_verdict "$line" && v=1
        j1_has_evidence "$line" "$round" && e=1
        [ "$v" -eq 1 ] && graded=$((graded + 1))
        [ "$e" -eq 1 ] && evidence=$((evidence + 1))
        [ "$v" -eq 1 ] && rec_graded=$((rec_graded + 1))
        [ "$e" -eq 1 ] && rec_evidence=$((rec_evidence + 1))
        if [ "$v" -ne 1 ] || [ "$e" -ne 1 ]; then
          local why='evidence+verdict'
          [ "$v" -ne 1 ] && [ "$e" -eq 1 ] && why='verdict'
          [ "$v" -eq 1 ] && [ "$e" -ne 1 ] && why='evidence'
          fail="${fail}${fail:+;}${f}:${ln}:r${round}:${why}"
        fi
      done < <(j1_members "$tree/$f" "$round")
      if [ "$rec_members" -eq 0 ]; then
        missing=$((missing + 1))
        detail="${detail}${detail:+;}${f}:r${round}:0"
      else
        detail="${detail}${detail:+;}${f}:r${round}:${rec_graded}/${rec_evidence}/${rec_members}"
      fi
    done
  done
  [ -z "$detail" ] && detail='none'
  [ -z "$fail" ] && fail='none'
  local closed=1
  [ "$members" -eq 0 ] && closed=0
  [ "$graded" -ne "$members" ] && closed=0
  [ "$evidence" -ne "$members" ] && closed=0
  [ "$missing" -ne 0 ] && closed=0
  [ "$nr" -ne "${#J1_RECORDS[@]}" ] && closed=0
  [ -n "$fail" ] && [ "$fail" != 'none' ] && closed=0
  J1_PAYLOAD="records=${nr},rounds=${rounds},lines=${members},graded=${graded}/${members},evidence=${evidence}/${members},missing=${missing},detail=${detail},fail=${fail}"
  J1_CLOSED=$closed
  printf 'J1 payload=%s closed=%s\n' "$J1_PAYLOAD" "$closed"
  return $((1 - closed))
}

# ---------------------------------------------------------------------------
# replay: this family's committed defeat and the fresh mutants
# ---------------------------------------------------------------------------

# j1_lit_sub FILE LINE_NO OLD NEW -- replace the literal substring OLD by NEW
# on line LINE_NO of FILE, in place.  Literal, not regex.
j1_lit_sub() { # FILE LINE_NO OLD NEW
  local f=$1 n=$2 old=$3 new=$4 tmp
  tmp="$f.j1tmp.$$"
  awk -v n="$n" -v old="$old" -v new="$new" '
    NR == n {
      i = index($0, old)
      if (i > 0) $0 = substr($0, 1, i - 1) new substr($0, i + length(old))
    }
    { print }
  ' "$f" > "$tmp" && mv -- "$tmp" "$f"
}

# j1_copy_tree SRC DST ROUND -- copy the three records of SRC into DST (the
# bytes J1 reads) plus the grounding artifacts of ROUND, so a mutant fixture
# fails for the defect under test and not for a missing evidence artifact.
j1_copy_tree() { # SRC DST [ROUND]
  local src=$1 dst=$2
  local round=${3:-${J1_ROUNDS[0]}}
  local f g
  rm -rf -- "$dst"; mkdir -p -- "$dst" || return 1
  for f in "${J1_RECORDS[@]}"; do
    [ -f "$src/$f" ] || continue
    cp -p -- "$src/$f" "$dst/$f" || return 1
  done
  g=".ufo/waves/round-$((round - 1))/wave2"
  if [ -d "$src/$g" ]; then
    mkdir -p -- "$dst/$g" || return 1
    cp -p -- "$src/$g"/* "$dst/$g"/ 2>/dev/null || return 1
  fi
  return 0
}

# j1_first_member_line FILE ROUND -- the line number of the first population
# member of ROUND's block in FILE, or empty.  Always returns 0, so a caller
# running under `set -e` is not tripped by a block with no member.
j1_first_member_line() { # FILE [ROUND]
  local ln
  ln=$(j1_members "$1" "${2:-${J1_ROUNDS[0]}}" 2>/dev/null | head -n 1 | cut -f1) || true
  printf '%s\n' "${ln:-}"
  return 0
}

# j1_mutant_union DST ROUND -- the COMMITTED defeat of this family: in every
# record the first `Correction (round <ROUND>)` line is replaced by the
# round-41 selftest's own evidence-free replacement.  The round-41 union tally
# stays 3/3 on this tree; J1 must not.
j1_mutant_union() { # DST ROUND
  local dst=$1
  local round=${2:-${J1_ROUNDS[0]}}
  local f
  for f in "${J1_RECORDS[@]}"; do
    [ -f "$dst/$f" ] || continue
    local tmp="$dst/$f.j1tmp.$$" ln
    ln=$(j1_fence_match "$dst/$f" "^Correction [(]round ${round}[)]" 2>/dev/null | head -n 1 | cut -f1) || true
    [ -n "$ln" ] || continue
    awk -v n="$ln" -v rep="Correction (round ${round}): the round-$((round - 1)) claim ${J1_CLAIM} is not verified on the frozen counter; the round-$((round - 1)) receipt truth is closed=10/10 exit=0." '
      NR == n { print rep; next }
      { print }
    ' "$dst/$f" > "$tmp" && mv -- "$tmp" "$dst/$f"
  done
}

# j1_mutant_partial_evidence DST ROUND -- one member names only two of the
# three firing identifiers.  The other members of the same record are
# untouched, so a union tally over the record still reads 3/3; J1 must not.
j1_mutant_partial_evidence() { # DST ROUND
  local dst=$1
  local round=${2:-${J1_ROUNDS[0]}}
  local f
  for f in "${J1_RECORDS[@]}"; do
    [ -f "$dst/$f" ] || continue
    local ln
    ln=$(j1_first_member_line "$dst/$f" "$round")
    [ -n "$ln" ] || continue
    local id old
    id=$(j1_evidence_for "$round" | sed -n 3p)
    [ -n "$id" ] || continue
    for old in \
      "\`wave2/${id}.md\` D2 (pristine H8 accepts a leaf-capped green base as its negative control)" \
      "\`wave2/${id}.md\` D2 (leaf-capped green base)"; do
      j1_lit_sub "$dst/$f" "$ln" "$old" "the third defeat artifact is withheld from this correction"
    done
  done
}

# j1_mutant_soft_verdict DST ROUND -- one member's verdict phrase is softened:
# it no longer grades the overclaim as not verified.  The member is still a
# member (it still names the claim and the prior round), so J1 must reject it.
j1_mutant_soft_verdict() { # DST ROUND
  local dst=$1
  local round=${2:-${J1_ROUNDS[0]}}
  local f
  for f in "${J1_RECORDS[@]}"; do
    [ -f "$dst/$f" ] || continue
    local ln
    ln=$(j1_first_member_line "$dst/$f" "$round")
    [ -n "$ln" ] || continue
    j1_lit_sub "$dst/$f" "$ln" \
      "not verified on the frozen counter (NOT verified)" \
      "not confirmed on the frozen counter"
  done
}

# j1_mutant_fenced DST ROUND -- one member is moved inside a CommonMark code
# fence, so it is no longer an outside-fence line and no longer a member.  The
# record loses a member; J1 must reject it.
j1_mutant_fenced() { # DST ROUND
  local dst=$1
  local round=${2:-${J1_ROUNDS[0]}}
  local f
  for f in "${J1_RECORDS[@]}"; do
    [ -f "$dst/$f" ] || continue
    local ln
    ln=$(j1_first_member_line "$dst/$f" "$round")
    [ -n "$ln" ] || continue
    local tmp="$dst/$f.j1tmp.$$"
    awk -v n="$ln" '
      NR == n { print "```"; print $0; print "```"; next }
      { print }
    ' "$dst/$f" > "$tmp" && mv -- "$tmp" "$dst/$f"
  done
}

# j1_mutant_deleted_record DST ROUND -- one record's whole member set is
# deleted, so that record has no member in the block.  J1 must reject it.
j1_mutant_deleted_record() { # DST ROUND
  local dst=$1
  local round=${2:-${J1_ROUNDS[0]}}
  local f
  f=${J1_RECORDS[1]}
  [ -f "$dst/$f" ] || return 0
  local tmp="$dst/$f.j1tmp.$$"
  awk -v pat="^Correction [(]round ${round}[)]" '
    $0 ~ pat { next }
    { print }
  ' "$dst/$f" > "$tmp" && mv -- "$tmp" "$dst/$f"
}

# j1_mutant_superstring DST ROUND -- one member names a SUPERSTRING of an
# expected identifier (`RevC1CountersX`) instead of the identifier itself.  A
# plain substring match would accept it; the whole-token limb must not.
j1_mutant_superstring() { # DST ROUND
  local dst=$1
  local round=${2:-${J1_ROUNDS[0]}}
  local f
  for f in "${J1_RECORDS[@]}"; do
    [ -f "$dst/$f" ] || continue
    local ln id
    ln=$(j1_first_member_line "$dst/$f" "$round")
    [ -n "$ln" ] || continue
    id=$(j1_evidence_for "$round" | sed -n 1p)
    [ -n "$id" ] || continue
    j1_lit_sub "$dst/$f" "$ln" "$id" "${id}X"
  done
}

# j1_selftest_export EXPORT_ROOT WORK_DIR -- grade the current bytes of this
# limb against the positive export and the mutants.  Prints one graded line per
# case and a summary; returns 0 only when the positive passes and every mutant
# is rejected.
j1_selftest_export() { # EXPORT_ROOT WORK_DIR
  local export=$1 work=$2 round
  rm -rf -- "$work"; mkdir -p -- "$work" || return 2
  round=${J1_ROUNDS[0]}
  local pos=1
  check_j1 "$export" >/dev/null 2>&1 || pos=0
  local m d closed mutants_ok=0 union total=0
  for m in union partial-evidence soft-verdict fenced deleted-record superstring; do
    d="$work/mutant-$m"
    j1_copy_tree "$export" "$d" "$round" || return 2
    case $m in
      union)            j1_mutant_union "$d" "$round" ;;
      partial-evidence) j1_mutant_partial_evidence "$d" "$round" ;;
      soft-verdict)     j1_mutant_soft_verdict "$d" "$round" ;;
      fenced)           j1_mutant_fenced "$d" "$round" ;;
      deleted-record)   j1_mutant_deleted_record "$d" "$round" ;;
      superstring)      j1_mutant_superstring "$d" "$round" ;;
    esac
    closed=0
    check_j1 "$d" >/dev/null 2>&1 && closed=1
    union=$(j1_union_evidence "$round" "${J1_RECORDS[@]/#/$d/}")
    printf 'selftest detail=J1 mutant=%s union-evidence=%s rejected=%s\n' \
      "$m" "$union" "$((1 - closed))"
    [ "$closed" -eq 0 ] && mutants_ok=$((mutants_ok + 1))
    total=$((total + 1))
  done
  local verdict='pass'
  [ "$pos" -eq 1 ] || verdict='fail'
  [ "$mutants_ok" -eq "$total" ] || verdict='fail'
  printf 'selftest case=J1 mutants=%s/%s positive=%s verdict=%s\n' \
    "$mutants_ok" "$total" "$([ "$pos" -eq 1 ] && echo pass || echo fail)" "$verdict"
  printf 'selftest cases=1 failures=%s\n' "$([ "$verdict" = pass ] && echo 0 || echo 1)"
  [ "$verdict" = pass ]
}
