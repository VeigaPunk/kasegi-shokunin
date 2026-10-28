#!/usr/bin/env bash
# ExecJ11Corr.sh — round-42 closure-suite limb J11 (family F-CORR).
#
# Closes D-r41-1 (round-41 verifier spot-check §5 item 1): the four
# `Correction (round 41)` entries of SCORECARD.md were appended verbatim
# twice — lines 1602-1605 and again 1607-1610. The verifier routed the
# repair as "note the duplication in the next round's records (no rewrite —
# append-only)", so the duplicate block STAYS in the lane and the round-42
# record carries the note that names it. J11 is the check that keeps the
# duplication from ever being silent again.
#
# CONTRACT
#   check_j11 TREE REF
#     Reads only the three lane records (SCORECARD.md, LOG.md, SHONEN.md)
#     under TREE. Prints ONE payload line `k=v,...` and returns 0 when the
#     check is CLOSED, 1 when it is RED. REF is accepted and ignored (the
#     suite's run_check passes it to every limb).
#
#   The limb is CLOSED (exit 0) only when all of the following hold.
#     records=3            all three records exist under TREE
#     corrections>0        the records still carry live corrections
#     eof-closed=3/3       every record's CommonMark fence is CLOSED at EOF
#                          (an open fence would hide corrections from the
#                          count, so it is a red, never a vacuous green)
#     marker=1             SCORECARD.md carries an outside-fence, column-0
#                          dedup marker (see MARKER below)
#     marker-substantive=1 the marker carries >= 40 characters after its
#                          prefix (a bare stub is not a marker)
#     marker-appended=1    the marker is APPENDED: its line number is greater
#                          than every live correction line of a round before
#                          42 in its own record (a marker at the top of the
#                          file is not an appended erratum)
#     unexcused=0          every duplicated correction body is named by the
#                          marker (see EXCUSE below)
#
#   EXCUSE. A duplicated group is (record file, normalized body). The marker
#   excuses a group when it (a) lives in that record file or names that file,
#   (b) names the group's round, and (c) names EVERY occurrence line of the
#   group — the line range exactly, not an approximation of it. The line
#   numbers are read from the marker text as standalone tokens of three or
#   more digits, and a `A-B` pair expands to every line between A and B, so
#   `lines 1602-1605 and 1607-1610` names all eight lines of the duplicated
#   block. A number that is part of a longer token (a commit hash, for
#   example) is NOT a line reference.
#
#   MARKER (the record line the L1 appends to SCORECARD.md, column 0):
#     Correction-dedup (round 42): duplicated Correction (round 41) blocks at
#     SCORECARD.md lines 1602-1605 and 1607-1610 — the second occurrence is
#     the stray; both kept as history.
#   The equivalent `Dedup note (round 42, ...)` spelling is accepted as the
#   same marker class. Neither spelling begins `Correction (round <n>):`, so
#   neither is counted as a correction line.
#
#   A marker does NOT make a defect disappear: the limb still reports the
#   duplication (dups=, dup-lines=, dup-records=) and still reports how many
#   groups the marker covers (marker-covers=covered/total). A marker that
#   names no line, no round, or only some of the duplicated groups leaves
#   unexcused > 0 and the limb stays RED.
#
#   FENCE-AWARE (the lane's own convention, r41-closure.sh I4): a
#   `Correction (round <n>)` line inside a CommonMark fence is not a
#   line-anchored correction. Fenced correction-shaped lines are counted and
#   reported in `fenced=` so a fence-marked dedup is visible in the payload
#   and never silent.
#
# REPLAY
#   j11_replay_fixtures WORK TREE
#     Builds the in-family defeat fixtures from TREE (the tree under test)
#     and asserts that check_j11 REJECTS every one of them, and that TREE
#     itself is accepted. Prints one `replay fixture=<name> rejected=1|0
#     limb=<field> payload=<...>` line per fixture and the summary
#     `replay fixtures=<n> failures=<k>`; returns non-zero when any fixture
#     is accepted or the tree under test is rejected.
#
# STANDALONE
#   bash ExecJ11Corr.sh --tree DIR
#     Prints `J11 payload=<...> closed=0|1` and exits 0 only when CLOSED.
#
# This file is a sourceable limb: it defines functions and globals only, and
# it sets no shell options, so sourcing it into corpus/instruments/
# r42-closure.sh cannot change that suite's behaviour.

if ! declare -p J11_RECORDS >/dev/null 2>&1; then
  J11_RECORDS=(SCORECARD.md LOG.md SHONEN.md)
fi

# The CommonMark 4.5 fence state machine, byte-identical in behaviour to the
# one r41-closure.sh uses: up to 3 leading spaces, a run of >= 3 identical
# ` or ~; a backtick fence's info string may not contain a backtick; the
# closer must use the same character, be at least as long, and be followed by
# nothing but spaces or tabs. Every line of a fenced block is INSIDE.
J11_AWK='
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
  if (rest ~ /[^[:space:]]/) return 0
  return 1
}
BEGIN { in_fence = 0; FENCE_CHAR = ""; FENCE_LEN = 0; live = 0; fenced = 0; fmarker = 0; in_marker = 0 }
{
  line = $0
  if (in_fence) {
    inside = 1
    if (fence_close(line)) { in_fence = 0; FENCE_CHAR = ""; FENCE_LEN = 0 }
  } else {
    if (fence_open(line)) { in_fence = 1; inside = 1 }
    else inside = 0
  }
  if (inside) {
    if (line ~ /^Correction \(round [0-9]+\):/) fenced++
    if (line ~ /^Correction-dedup \(round 42\)/ || line ~ /^Dedup note \(round 42/) fmarker++
    next
  }
  if (line ~ /^Correction \(round [0-9]+\):/) {
    live++
    body = line
    sub(/^Correction \(round [0-9]+\):[[:space:]]*/, "", body)
    gsub(/[[:space:]]+/, " ", body)
    sub(/^ /, "", body); sub(/ $/, "", body)
    if (body == "") body = "<empty-body>"
    r = line
    sub(/^Correction \(round /, "", r)
    sub(/\):.*$/, "", r)
    printf "C\t%d\t%s\t%s\n", NR, r, body
    cnt[body]++
    bround[body] = r
    blines[body] = blines[body] " " NR
    next
  }
  if (line ~ /^Correction-dedup \(round 42\)/ || line ~ /^Dedup note \(round 42/) {
    printf "M\t%d\t%s\n", NR, line
    in_marker = 1
    next
  }
  if (in_marker) {
    if (line ~ /^#/ || line ~ /^[[:space:]]*$/) { in_marker = 0 }
    else printf "MC\t%d\t%s\n", NR, line
  }
}
END {
  n = 0
  for (body in cnt) {
    n++
    if (cnt[body] >= 2) printf "G\t%s\t%s\n", bround[body], blines[body]
  }
  printf "F\t%s\t%d\t%d\t%d\t%d\n", (in_fence ? "OPEN" : "CLOSED"), live, fenced, fmarker, n
}
'

# j11_line_numbers TEXT — the line numbers the text names. A number is a
# line reference when it is a standalone token of three or more digits: the
# characters around it must not be alphanumeric or `_`, so a commit hash
# contributes no line number. A `A-B` pair expands to every line between A
# and B. The output is a sorted, space-separated list.
J11_NUM_AWK='
function isdig(c) { return c >= "0" && c <= "9" }
function add(v) { if (!(v in seen)) { seen[v] = 1; out = out " " v } }
{ s = $0
  n = length(s); i = 1; m = 0
  while (i <= n) {
    c = substr(s, i, 1)
    if (isdig(c)) {
      st = i
      while (i <= n && isdig(substr(s, i, 1))) i++
      m++
      tv[m] = substr(s, st, i - st) + 0
      tlen[m] = i - st
      tprev[m] = (st == 1) ? "" : substr(s, st - 1, 1)
      tnext[m] = (i > n) ? "" : substr(s, i, 1)
    } else i++
  }
  for (j = 1; j <= m; j++) {
    if (tlen[j] < 3) continue
    if (tprev[j] ~ /[0-9A-Za-z_]/ || tnext[j] ~ /[0-9A-Za-z_]/) continue
    add(tv[j])
    if (tnext[j] == "-" && (j + 1) <= m && tprev[j + 1] == "-" && tlen[j + 1] >= 3 \
       && tprev[j + 1] !~ /[0-9A-Za-z_]/ && tnext[j + 1] !~ /[0-9A-Za-z_]/) {
      lo = tv[j]; hi = tv[j + 1]
      if (lo > hi) { t = lo; lo = hi; hi = t }
      if (hi - lo > 0 && hi - lo <= 10000) for (k = lo; k <= hi; k++) add(k)
    }
  }
}
END { print out }
'

j11_line_numbers() {
  printf '%s\n' "$1" | sed -e 's/–/-/g' -e 's/—/-/g' | awk "$J11_NUM_AWK" \
    | tr ' ' '\n' | grep -E '^[0-9]+$' | sort -n -u | tr '\n' ' '
}

# j11_rounds TEXT — the round numbers the text names, space separated.
j11_rounds() {
  printf '%s\n' "$1" | grep -oE '(round|Round|ROUND|r|R)[[:space:]_-]*[0-9]+' \
    | grep -oE '[0-9]+' | sort -n -u | tr '\n' ' '
}

# j11_has_num LIST N — TRUE when N is in the space-separated LIST.
j11_has_num() {
  local list=$1 needle=$2 n
  for n in $list; do
    [ "$n" = "$needle" ] && return 0
  done
  return 1
}

# j11_has_word LIST W — TRUE when W is in the space-separated LIST.
j11_has_word() {
  local list=$1 needle=$2 n
  for n in $list; do
    [ "$n" = "$needle" ] && return 0
  done
  return 1
}

# j11_scan FILE — the record scan: live correction lines (C), dedup markers
# (M) and their continuation lines (MC), the duplicated groups (G), and the
# fence state and counters (F).
j11_scan() {
  awk "$J11_AWK" "$1"
}

# check_j11 TREE REF — the J11 limb.
check_j11() { # TREE REF
  local tree=$1
  (
    cd "$tree" 2>/dev/null || {
      printf 'records=0,corrections=0,distinct=0,dups=0,dup-distinct=0,dup-lines=0,dup-records=0,unexcused=0,fenced=0,eof-closed=0/3,marker=0,marker-line=0,marker-substantive=0,marker-appended=0,marker-rounds=,marker-lines=0,marker-covers=0/0,recorded=0'
      exit 1
    }
    local records=0 live=0 fenced=0 eofok=0 distinct=0
    local dups=0 duplines=0 duprecords=0
    local f out kind a b c
    local -a dup_file=() dup_round=() dup_lines=()
    local -a m_num=() m_text=() m_file=()
    local -A pre42=()
    local i g gf gr gl ln nums rounds rest covered ok hit
    local marker=0 m_line=0 m_sub=0 m_app=0 m_rounds='' m_lines=0 m_cover=0

    for f in "${J11_RECORDS[@]}"; do
      [ -f "$f" ] || continue
      records=$((records + 1))
      out=$(j11_scan "$f")
      local fdups=0
      while IFS=$'\t' read -r kind a b c d e; do
        case $kind in
          C)
            live=$((live + 1))
            if [ "$b" != 42 ] && [ "$a" -gt "${pre42[$f]:-0}" ]; then pre42[$f]=$a; fi
            ;;
          M)
            m_num+=( "$a" ); m_text+=( "$b" ); m_file+=( "$f" )
            ;;
          MC)
            m_text[${#m_num[@]}-1]="${m_text[${#m_num[@]}-1]} $b"
            ;;
          G)
            dups=$((dups + 1))
            fdups=$((fdups + 1))
            dup_file+=( "$f" ); dup_round+=( "$a" ); dup_lines+=( "$b" )
            ;;
          F)
            [ "$a" = CLOSED ] && eofok=$((eofok + 1))
            fenced=$((fenced + $c))
            distinct=$((distinct + $e))
            ;;
        esac
      done <<< "$out"
      [ "$fdups" -gt 0 ] && duprecords=$((duprecords + 1))
      # the surplus occurrences of every duplicated group of this record
      while IFS=$'\t' read -r kind a b c; do
        [ "$kind" = G ] || continue
        local n=0
        for ln in $b; do n=$((n + 1)); done
        duplines=$((duplines + n - 1))
      done <<< "$out"
    done

    # the marker must live in SCORECARD.md
    # Every qualifying marker contributes to the coverage union: a group is
    # excused when at least one well-formed marker names it.
    local -a covered_g=()
    local recorded=0
    for i in "${!m_num[@]}"; do
      [ "${m_file[$i]}" = SCORECARD.md ] || continue
      rest=$(printf '%s\n' "${m_text[$i]}" | sed -e 's/^Correction-dedup (round 42)//' -e 's/^Dedup note (round 42[^)]*)//')
      [ "${#rest}" -ge 40 ] || continue
      [ "${m_num[$i]}" -gt "${pre42[SCORECARD.md]:-0}" ] || continue
      nums=$(j11_line_numbers "$rest")
      [ -n "$nums" ] || continue
      rounds=$(j11_rounds "$rest")
      recorded=$((recorded + 1))
      if [ "$m_line" = 0 ]; then m_line=${m_num[$i]}; m_sub=1; m_app=1; m_lines=1; fi
      for g in "${!dup_file[@]}"; do
        [ "${covered_g[$g]:-0}" = 1 ] && continue
        gf=${dup_file[$g]}; gr=${dup_round[$g]}; gl=${dup_lines[$g]}
        if [ "$gf" != SCORECARD.md ] && ! printf '%s\n' "$rest" | grep -qF -- "$gf"; then continue; fi
        j11_has_word "$rounds" "$gr" || continue
        hit=1
        for ln in $gl; do
          if ! j11_has_num "$nums" "$ln"; then hit=0; break; fi
        done
        [ "$hit" -eq 1 ] || continue
        covered_g[$g]=1
      done
    done

    covered=0
    for g in "${!covered_g[@]}"; do
      [ "${covered_g[$g]}" = 1 ] && covered=$((covered + 1))
    done
    m_cover=$covered
    m_rounds=''
    if [ "$recorded" -ge 1 ]; then
      m_rounds=$(for g in "${!dup_file[@]}"; do printf '%s\n' "${dup_round[$g]}"; done \
        | sort -n -u | tr '\n' '+' | sed -e 's/+$//')
    fi

    local unexcused=0
    unexcused=$(( ${#dup_file[@]} - m_cover ))
    if [ "$recorded" -ge 1 ] && [ "$unexcused" -eq 0 ]; then marker=1; fi

    local okall=1
    [ "$records" -eq 3 ] || okall=0
    [ "$live" -gt 0 ] || okall=0
    [ "$eofok" -eq 3 ] || okall=0
    [ "$marker" -eq 1 ] || okall=0
    [ "$unexcused" -eq 0 ] || okall=0

    printf 'records=%s,corrections=%s,distinct=%s,dups=%s,dup-distinct=%s,dup-lines=%s,dup-records=%s,unexcused=%s,fenced=%s,eof-closed=%s/3,marker=%s,marker-line=%s,marker-substantive=%s,marker-appended=%s,marker-rounds=%s,marker-lines=%s,marker-covers=%s/%s,recorded=%s' \
      "$records" "$live" "$distinct" "$dups" "$dups" "$duplines" "$duprecords" "$unexcused" "$fenced" "$eofok" \
      "$marker" "$m_line" "$m_sub" "$m_app" "$m_rounds" "$m_lines" "$m_cover" "${#dup_file[@]}" "$recorded"
    [ "$okall" -eq 1 ] && exit 0
    exit 1
  )
}

# j11_replay_fixtures WORK TREE — the in-family defeat fixtures, built from
# the tree under test. Every fixture must be REJECTED; the tree under test
# must be accepted.
j11_replay_fixtures() { # WORK TREE
  local work=$1 tree=$2
  local fails=0 n=0 payload rc name fixture
  mkdir -p -- "$work" || return 1
  rm -rf -- "$work"/fx-* 2>/dev/null

  payload=$(check_j11 "$tree" HEAD); rc=$?
  n=$((n + 1))
  if [ "$rc" -eq 0 ]; then
    printf 'replay fixture=tree-under-test accepted=1 payload=%s\n' "$payload"
  else
    printf 'replay fixture=tree-under-test accepted=0 limb=closed-expected payload=%s\n' "$payload"
    fails=$((fails + 1))
  fi

  fixture="$work/fx-nomarker"; rm -rf -- "$fixture"; cp -r -- "$tree" "$fixture"
  j11_strip_markers "$fixture"; j11_inject_duplicate "$fixture"
  j11_expect_red "$fixture" nomarker 'unexcused=[1-9]'; fails=$((fails + $?)); n=$((n + 1))

  fixture="$work/fx-stubmarker"; rm -rf -- "$fixture"; cp -r -- "$tree" "$fixture"
  j11_stub_marker "$fixture"
  j11_expect_red "$fixture" stub-marker 'marker-substantive=0'; fails=$((fails + $?)); n=$((n + 1))

  fixture="$work/fx-nolines"; rm -rf -- "$fixture"; cp -r -- "$tree" "$fixture"
  j11_relabel_lines "$fixture" 999999
  j11_expect_red "$fixture" marker-names-no-line 'marker-covers=0/4'; fails=$((fails + $?)); n=$((n + 1))

  fixture="$work/fx-noround"; rm -rf -- "$fixture"; cp -r -- "$tree" "$fixture"
  j11_relabel_round "$fixture" 99
  j11_expect_red "$fixture" marker-names-no-round 'unexcused=[1-9]'; fails=$((fails + $?)); n=$((n + 1))

  fixture="$work/fx-notappended"; rm -rf -- "$fixture"; cp -r -- "$tree" "$fixture"
  j11_move_marker_to_top "$fixture"
  j11_expect_red "$fixture" marker-not-appended 'marker-appended=0'; fails=$((fails + $?)); n=$((n + 1))

  fixture="$work/fx-fencedmarker"; rm -rf -- "$fixture"; cp -r -- "$tree" "$fixture"
  j11_fence_marker "$fixture"
  j11_expect_red "$fixture" marker-fenced 'marker=0'; fails=$((fails + $?)); n=$((n + 1))

  fixture="$work/fx-partialcover"; rm -rf -- "$fixture"; cp -r -- "$tree" "$fixture"
  j11_relabel_lines "$fixture" 999998
  j11_expect_red "$fixture" marker-covers-no-group 'marker-covers=0/4'; fails=$((fails + $?)); n=$((n + 1))

  fixture="$work/fx-partialrange"; rm -rf -- "$fixture"; cp -r -- "$tree" "$fixture"
  j11_narrow_marker "$fixture"
  j11_expect_red "$fixture" marker-names-partial-range 'marker-covers=0/4'; fails=$((fails + $?)); n=$((n + 1))

  fixture="$work/fx-logdup"; rm -rf -- "$fixture"; cp -r -- "$tree" "$fixture"
  j11_dup_in_log "$fixture"
  j11_expect_red "$fixture" unexcused-duplicate-in-log 'unexcused=[1-9]'; fails=$((fails + $?)); n=$((n + 1))

  fixture="$work/fx-neardup"; rm -rf -- "$fixture"; cp -r -- "$tree" "$fixture"
  j11_near_dup "$fixture"
  j11_expect_red "$fixture" whitespace-variant-duplicate 'unexcused=[1-9]'; fails=$((fails + $?)); n=$((n + 1))

  fixture="$work/fx-openfence"; rm -rf -- "$fixture"; cp -r -- "$tree" "$fixture"
  printf '\n```\n' >> "$fixture/SCORECARD.md"
  j11_expect_red "$fixture" open-fence 'eof-closed=2/3'; fails=$((fails + $?)); n=$((n + 1))

  printf 'replay fixtures=%s failures=%s\n' "$n" "$fails"
  [ "$fails" -eq 0 ] || return 1
  return 0
}

# j11_expect_red FIXTURE NAME LIMB — the fixture must be rejected and the
# payload must name the reopened limb.
j11_expect_red() { # FIXTURE NAME LIMB
  local fixture=$1 name=$2 limb=$3 payload rc
  payload=$(check_j11 "$fixture" HEAD); rc=$?
  if [ "$rc" -ne 0 ] && printf '%s' "$payload" | grep -qE "(^|,)${limb}(,|\$)" ; then
    printf 'replay fixture=%s rejected=1 limb=%s payload=%s\n' "$name" "$limb" "$payload"
    return 0
  fi
  printf 'replay fixture=%s rejected=0 rc=%s payload=%s\n' "$name" "$rc" "$payload"
  return 1
}

# j11_first_correction FILE — the full text of the first live correction line.
j11_first_correction() {
  local f=$1 ln
  ln=$(j11_scan "$f" | awk -F'\t' '$1 == "C" { print $2; exit }')
  [ -n "$ln" ] || return 1
  sed -n "${ln}p" -- "$f"
}

# j11_marker_lines FILE — the line numbers of the dedup marker lines.
j11_marker_lines() {
  j11_scan "$1" | awk -F'\t' '$1 == "M" { print $2 }'
}

# j11_strip_markers TREE — remove every dedup marker line from SCORECARD.md.
j11_strip_markers() {
  local f="$1/SCORECARD.md" tmp
  [ -f "$f" ] || return 0
  tmp="$f.j11tmp"
  grep -vE '^(Correction-dedup \(round 42\)|Dedup note \(round 42)' -- "$f" > "$tmp" || true
  mv -- "$tmp" "$f"
}

# j11_inject_duplicate TREE — append a verbatim copy of a live correction
# line to SCORECARD.md (a duplication with no marker).
j11_inject_duplicate() {
  local f="$1/SCORECARD.md" line
  line=$(j11_first_correction "$f")
  [ -n "$line" ] || return 1
  printf '%s\n' "$line" >> "$f"
}

# j11_stub_marker TREE — replace the marker with a bare stub.
j11_stub_marker() {
  local f="$1/SCORECARD.md" tmp ln
  ln=$(j11_marker_lines "$f" | head -n1)
  [ -n "$ln" ] || return 1
  tmp="$f.j11tmp"
  awk -v ln="$ln" 'NR == ln { print "Correction-dedup (round 42):"; next } { print }' "$f" > "$tmp"
  mv -- "$tmp" "$f"
}

# j11_relabel_lines TREE N — rewrite every line number the marker names to N.
j11_relabel_lines() {
  local f="$1/SCORECARD.md" tmp
  tmp="$f.j11tmp"
  awk -v n="$1" '
    /^(Correction-dedup \(round 42\)|Dedup note \(round 42)/ {
      line = $0; out = ""
      while (match(line, /[0-9][0-9][0-9]+/)) {
        out = out substr(line, 1, RSTART - 1) n
        line = substr(line, RSTART + RLENGTH)
      }
      print out line
      next
    }
    { print }
  ' "$f" > "$tmp"
  mv -- "$tmp" "$f"
}

# j11_narrow_marker TREE — rewrite the marker so that it names only ONE
# occurrence line of the first duplicated group: a partial line range does
# not excuse the group (the range must be named exactly).
j11_narrow_marker() {
  local f="$1/SCORECARD.md" tmp ln
  ln=$(j11_scan "$f" | awk -F'\t' '$1 == "G" { split($3, a, " "); print a[1]; exit }')
  [ -n "$ln" ] || return 1
  tmp="$f.j11tmp"
  awk -v n="$ln" '
    /^(Correction-dedup \(round 42\)|Dedup note \(round 42)/ {
      line = $0; out = ""
      while (match(line, /[0-9][0-9][0-9]+/)) {
        out = out substr(line, 1, RSTART - 1) n
        line = substr(line, RSTART + RLENGTH)
      }
      print out line
      next
    }
    { print }
  ' "$f" > "$tmp"
  mv -- "$tmp" "$f"
}

# j11_relabel_round TREE N — rewrite the round the marker names.
j11_relabel_round() {
  local f="$1/SCORECARD.md" tmp
  tmp="$f.j11tmp"
  awk -v n="$1" '
    /^(Correction-dedup \(round 42\)|Dedup note \(round 42)/ {
      print "Correction-dedup (round " n "): the duplicated correction blocks of this record are recorded here; they stand at lines 1602-1605 and 1607-1610."
      next
    }
    { print }
  ' "$f" > "$tmp"
  mv -- "$tmp" "$f"
}

# j11_move_marker_to_top TREE — move the marker to the end-of-file position
# of the record, i.e. BEFORE the correction history it marks (never
# appended).
j11_move_marker_to_top() {
  local f="$1/SCORECARD.md" tmp ln
  ln=$(j11_marker_lines "$f" | head -n1)
  [ -n "$ln" ] || return 1
  tmp="$f.j11tmp"
  awk -v ln="$ln" '
    NR == ln { m = $0; next }
    { print }
  ' "$f" > "$tmp.body"
  { printf '%s\n' "$m"; cat "$tmp.body"; } > "$tmp"
  mv -- "$tmp" "$f"
  rm -f -- "$tmp.body"
}

# j11_fence_marker TREE — quote the marker inside a fenced block.
j11_fence_marker() {
  local f="$1/SCORECARD.md" tmp
  tmp="$f.j11tmp"
  awk '
    /^(Correction-dedup \(round 42\)|Dedup note \(round 42)/ { print "```"; print; print "```"; next }
    { print }
  ' "$f" > "$tmp"
  mv -- "$tmp" "$f"
}

# j11_dup_in_log TREE — duplicate a live correction line of LOG.md.
j11_dup_in_log() {
  local f="$1/LOG.md" line
  [ -f "$f" ] || return 1
  line=$(j11_first_correction "$f")
  [ -n "$line" ] || return 1
  printf '%s\n' "$line" >> "$f"
}

# j11_near_dup TREE — append a whitespace variant of a live correction line
# of SHONEN.md (same text, different spacing inside the body, so the
# line-anchored prefix still matches and only the normalization can catch it).
j11_near_dup() {
  local f="$1/SHONEN.md" line head body
  [ -f "$f" ] || return 1
  line=$(j11_first_correction "$f")
  [ -n "$line" ] || return 1
  head=${line%%:*}
  body=${line#*: }
  printf '%s: %s\n' "$head" "${body/ /  }" >> "$f"
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  TREE=''
  REPLAY=''
  while [ $# -gt 0 ]; do
    case $1 in
      --tree) TREE=$2; shift 2 ;;
      --replay) REPLAY=$2; shift 2 ;;
      -h|--help) sed -n '2,/^if ! declare/p' "${BASH_SOURCE[0]}" | sed -e '$d' -e 's/^# \{0,1\}//'; exit 0 ;;
      *) printf 'ExecJ11Corr: unknown argument: %s\n' "$1" >&2; exit 2 ;;
    esac
  done
  [ -n "$TREE" ] || { printf 'ExecJ11Corr: --tree DIR is required\n' >&2; exit 2; }
  if [ -n "$REPLAY" ]; then
    j11_replay_fixtures "$REPLAY" "$TREE"
    exit $?
  fi
  payload=$(check_j11 "$TREE" HEAD); rc=$?
  printf 'J11 payload=%s closed=%s\n' "$payload" "$([ "$rc" -eq 0 ] && echo 1 || echo 0)"
  exit "$rc"
fi
