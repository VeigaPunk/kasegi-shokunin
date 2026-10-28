#!/usr/bin/env bash
# ExecJ3Registry.sh — round-42 J3 SKILL.md registry-integrity limb (family F-TABLE).
#
# PURPOSE
#   J3 is the round-42 check that keeps the "Gates & probes registry" of SKILL.md
#   a set of well-formed Markdown tables.  It closes D-r41-3 (round-41 verifier
#   spot-check §5 item 3) and the two surviving round-41 parser defects
#   (.ufo/waves/round-41/wave2/MutSkillTablePipes.md + .findings.md):
#     (a) the Round-40 registry table was SPLIT from its only row by a blank
#         line (SKILL.md L1120 separator, L1121 blank, L1122 row), so the row
#         rendered outside its header, and the same instrument was registered
#         twice (L1122 in the Round-40 block, L1128 in the Round-41 block);
#     (b) the round-41 parser trimmed the first cell before comparing it, so a
#         row written `|  r41-closure.sh |` (two spaces) was accepted;
#     (c) the round-41 parser split a row on EVERY pipe, so a bare pipe inside
#         a cell (`closed=0|1`, or a bare `gate|probe`) inflated the cell count
#         and was accepted as long as the count stayed >= 8.
#
# CONTRACT (what the suite calls)
#   check_j3 TREE [REF]
#       TREE is the exported lane tree (the export root); SKILL.md and
#       corpus/instruments/ are read under it.  REF is accepted and ignored, so
#       the suite's `run_check <ID> TREE REF` dispatch shape can call this limb
#       unchanged.
#       Prints exactly ONE payload line, `k=v,k=v,...`, on stdout (no `J3
#       payload=` prefix and no `closed=` suffix: the suite composes
#       `J3 payload=<this line> closed=<0|1>` — the r41 harness convention).
#       j3_line TREE is the same check already composed as the suite's line
#       `J3 payload=<payload> closed=<0|1>` for a harness that wants it whole.
#       Exit status of check_j3:
#           0  CLOSED   every limb is clean
#           1  RED      at least one limb found a defect, or the tree could not
#                       be read (read=fail — never a vacuous green)
#           2  harness error (bad invocation; nothing was measured)
#
#   PAYLOAD KEYS
#       tables=<n>     Gates-and-probes registry tables found
#       rows=<n>       data rows inside those tables
#       split=<n>      tables whose separator is not immediately followed by a
#                      data row (a blank line between the header separator and
#                      its rows — the D-r41-3 shape), plus tables that carry a
#                      separator inside the data rows.  GATING.
#       orphan=<n>     rows that name a `r*-closure.sh` instrument but are NOT
#                      a data row of a registry table (the "row moved outside
#                      the contiguous table" and "row after a blank line"
#                      shapes — MutSkillTablePipes variants 1 and 4).  GATING.
#       badcells=<n>   registry data rows whose cell count differs from the
#                      table header's cell count.  Cells are split on
#                      UNESCAPED pipes only, so `\|` inside a cell is accepted
#                      (the lane's own convention, e.g. `gate\|probe`,
#                      `closed=K/9 exit=0\|1`) and a BARE pipe inside a cell is
#                      rejected (MutSkillTablePipes variant 2).  GATING.
#       leadws=<n>     registry data rows whose first cell is not exactly
#                      `| <name> |` — one space of padding on each side and no
#                      other whitespace (MutSkillTablePipes variant 3).  GATING.
#       indent=<n>     registry data rows that do not start at column 0.  An
#                      indented row still counts as a row for `dup`, so an
#                      indented duplicate cannot hide.  GATING.
#       dup=<n>        `r*-closure.sh` basenames registered in MORE than one
#                      row, across ALL registry tables and counted also over
#                      orphan rows (the cross-table duplicate D-r41-3 named).
#                      Declared pairs are exempt (see DECLARED PAIRS).  GATING.
#       missing=<n>    `corpus/instruments/r*-closure.sh` basenames of TREE with
#                      NO registry row.  GATING.
#       unknown=<n>    registry rows naming a `r*-closure.sh` basename that is
#                      not on disk in TREE.  DIAGNOSTIC ONLY (never gates).
#       declared=<n>   size of the declared-pairs list (see below).
#       own=<basename> the suite-under-test basename exempted from `missing`
#                      (see OWN INSTRUMENT).
#       read=ok|fail   read=fail (with reason=) means nothing was measured.
#
#   DECLARED PAIRS (erratum E3)
#       `.ufo/waves/round-42/claims-erratum-1.md` E3 rules that the uniqueness
#       limb is "scoped to `r*-closure.sh` basenames exclusive of those declared
#       pairs": SKILL.md L1111 and L1113 both register `r36-closure.sh` — two
#       legitimate Round-36 rows with DISTINCT verdict-map cells (the second is
#       the D5 correction appended in round 37).  The pair is named in a
#       declaration list and is exempt from `dup` only; both rows are still
#       shape-checked (split/badcells/leadws/indent).  Override the list with
#       J3_DECLARED_PAIRS (space-separated basenames); the default is
#       `r36-closure.sh`.  Set J3_DECLARED_PAIRS='' to require strict
#       one-row-per-basename over every closure script.
#       (anchorcheck.py also has two rows, L982/L1041, but it is not an
#       `r*-closure.sh` basename, so the scoped limb never sees it.)
#
#   OWN INSTRUMENT
#       `missing` skips the suite-under-test basename, J3_OWN, default
#       `r42-closure.sh`.  Rationale: the registry row for the suite under test
#       is the integration's artifact and is appended in the same integration
#       step as the suite; J3 must not demand it (and the negative controls run
#       on base / round-41 exports where the suite does not exist at all).  It
#       is still subject to every other limb, `dup` included, so two r42 rows
#       are RED.
#
#   REPLAY LIMB
#   j3_replay TREE SANDBOX
#       Re-executes every committed F-TABLE defeat shape against the CURRENT
#       SKILL.md bytes of TREE and requires rejection.  The four
#       MutSkillTablePipes probes are reproduced verbatim in shape —
#       (1) blank line directly before the suite row, (2) bare pipe appended
#       inside an entry command, (3) leading whitespace in the first cell,
#       (4) row moved outside the contiguous registry table — plus the D-r41-3
#       duplicate row and four further shapes (indented duplicate, blank line
#       between header and separator, deleted row, re-introduced legacy bare
#       pipe).  Each mutant is materialized in its own directory under SANDBOX
#       (never inside TREE) and the positive control (unmutated bytes) must be
#       accepted.  Prints `selftest detail=J3 mutant=<name> rejected=<0|1>
#       payload=<...>` per case and `selftest cases=<n> failures=<k>`; returns
#       0 only when the positive is accepted and every mutant is rejected.
#       A replay that skips a case fails: an absent defeat is not a repair.
#
# ENVIRONMENT (per-seat overrides; the suite needs none)
#   J3_TREE              default TREE for check_j3
#   J3_REF               accepted and ignored
#   J3_OWN               suite-under-test basename (default r42-closure.sh)
#   J3_DECLARED_PAIRS    declared duplicate-pair basenames (default r36-closure.sh)
#
# USAGE (sourcing defines the functions and runs nothing)
#   bash ExecJ3Registry.sh --check  TREE        payload + exit status
#   bash ExecJ3Registry.sh --detail TREE        defect lines, then the payload
#   bash ExecJ3Registry.sh --self-test TREE [SANDBOX]   the replay limb
#   bash ExecJ3Registry.sh --help
#
# WHAT J3 IS NOT (stated limits — a shape check, not a content audit)
#   J3 checks the SHAPE of the registry: table contiguity, one row per closure
#   suite, cell-count fidelity, first-cell padding.  It does not and cannot
#   judge whether a row's verdict-map prose is true (wave-2 seed item 84), and
#   it does not police rows of other tables in SKILL.md (the Frontier decision
#   table, the policy playbook, ...) — they are not Gates-and-probes rows.
#   It reads only SKILL.md and the directory listing of
#   corpus/instruments/; it writes nothing outside SANDBOX in --self-test.

j3_self=${BASH_SOURCE[0]:-ExecJ3Registry.sh}

j3_die() { printf 'ExecJ3Registry: %s\n' "$*" >&2; exit 2; }

# ---------------------------------------------------------------------------
# the parser
# ---------------------------------------------------------------------------

# j3_awk_program — the awk program as text.  It prints two record kinds:
#   S<TAB>key=value     summary counters
#   X<TAB>kind<TAB>line<TAB>note   one defect
# Cells are split on unescaped pipes only; `\|` stays inside its cell.
j3_awk_program() {
  cat <<'AWK'
function trims(s) { gsub(/^[ \t]+/, "", s); gsub(/[ \t]+$/, "", s); return s }

function issep(s,   t) {
  t = trims(s)
  if (t !~ /^\|[-:| ]+\|$/) return 0
  if (t !~ /-/) return 0
  return 1
}

function isclosure(t) {
  return (t ~ /^r.*-closure[.]sh$/) ? 1 : 0
}

# splitcells(s, arr) -> number of CONTENT cells; arr[1..n] are the raw cells
# (untrimmed).  A pipe preceded by an odd run of backslashes does not split.
function splitcells(s, arr,   i, c, n, k, esc, cur) {
  k = 0; esc = 0; cur = ""
  for (i = 1; i <= length(s); i++) {
    c = substr(s, i, 1)
    if (esc) { cur = cur c; esc = 0; continue }
    if (c == "\\") { cur = cur c; esc = 1; continue }
    if (c == "|") { arr[++k] = cur; cur = ""; continue }
    cur = cur c
  }
  arr[++k] = cur
  n = k - 2
  if (n < 0) n = 0
  for (i = 1; i <= n; i++) arr[i] = arr[i + 1]
  return n
}

function defect(kind, line, note) {
  printf "X\t%s\t%d\t%s\n", kind, line, note
}

function flush(   i, hc, nc, raw, t, a, b, c) {
  if (run == 0) return
  hc = splitcells(runline[1], a)
  if (hc == 8 && trims(a[1]) == "name" && trims(a[2]) == "type") {
    tables++
    if (run < 3) {
      splitn++; defect("split", runline_no[1], "registry table has no data row")
    } else if (!issep(runline[2])) {
      splitn++; defect("split", runline_no[2], "second line is not a separator")
    }
    for (i = 3; i <= run; i++) {
      if (issep(runline[i])) {
        splitn++; defect("split", runline_no[i], "separator inside the data rows")
        continue
      }
      rows++
      nc = splitcells(runline[i], b)
      raw = b[1]
      t = trims(raw)
      if (nc != 8) {
        badcells++
        defect("badcells", runline_no[i], "cells=" nc " want=8")
      }
      if (raw != " " t " ") {
        leadws++
        defect("leadws", runline_no[i], "first-cell padding is not canonical")
      }
      if (runline[i] ~ /^[ \t]/) {
        indent++
        defect("indent", runline_no[i], "row does not start at column 0")
      }
      if (isclosure(t)) { cnt[t]++; }
    }
  } else {
    for (i = 1; i <= run; i++) {
      if (issep(runline[i])) continue
      nc = splitcells(runline[i], c)
      if (nc < 1) continue
      t = trims(c[1])
      if (isclosure(t)) {
        orphan++
        defect("orphan", runline_no[i], t " is not inside a registry table")
        cnt[t]++
      }
    }
  }
  run = 0
}

BEGIN {
  nk = 0; nd = 0
  n = split(known, KN, " ")
  for (i = 1; i <= n; i++) if (KN[i] != "") { klist[++nk] = KN[i]; isk[KN[i]] = 1 }
  n = split(decl, DEC, " ")
  for (i = 1; i <= n; i++) if (DEC[i] != "") { isdecl[DEC[i]] = 1; nd++ }
  fence = 0; fencech = ""; fencelen = 0
  run = 0
  tables = 0; rows = 0; splitn = 0; orphan = 0
  badcells = 0; leadws = 0; indent = 0
}

{
  if (match($0, /^[ \t]*(```+|~~~+)/)) {
    tok = substr($0, RSTART, RLENGTH)
    sub(/^[ \t]+/, "", tok)
    ch = substr(tok, 1, 1); ln = length(tok)
    if (fence == 0) { fence = 1; fencech = ch; fencelen = ln }
    else if (ch == fencech && ln >= fencelen) { fence = 0 }
    next
  }
  if (fence == 1) next
  if ($0 ~ /^[ \t]*\|/) { run++; runline[run] = $0; runline_no[run] = NR }
  else { flush() }
}

END {
  flush()
  # deterministic order: insertion-sort the closure names the registry carries
  m = 0
  for (nm in cnt) names[++m] = nm
  for (i = 2; i <= m; i++) {
    v = names[i]; j = i - 1
    while (j >= 1 && names[j] > v) { names[j + 1] = names[j]; j-- }
    names[j + 1] = v
  }
  dup = 0
  for (i = 1; i <= m; i++) {
    nm = names[i]
    if (cnt[nm] > 1 && !isdecl[nm]) { dup++; defect("dup", 0, nm " rows=" cnt[nm]) }
  }
  missing = 0
  for (i = 1; i <= nk; i++) {
    if (klist[i] == own) continue
    if (cnt[klist[i]] == 0) { missing++; defect("missing", 0, klist[i]) }
  }
  unknown = 0
  for (i = 1; i <= m; i++) {
    nm = names[i]
    if (!isk[nm] && nm != own) { unknown++; defect("unknown", 0, nm) }
  }
  printf "S\ttables=%d\n", tables
  printf "S\trows=%d\n", rows
  printf "S\tsplit=%d\n", splitn
  printf "S\torphan=%d\n", orphan
  printf "S\tbadcells=%d\n", badcells
  printf "S\tleadws=%d\n", leadws
  printf "S\tindent=%d\n", indent
  printf "S\tdup=%d\n", dup
  printf "S\tmissing=%d\n", missing
  printf "S\tunknown=%d\n", unknown
  printf "S\tdeclared=%d\n", nd
}
AWK
}

# j3_scan TREE -> the raw record stream of the parser (S and X lines).
j3_scan() { # TREE
  local tree=$1 own decl known='' f b
  own=${J3_OWN-r42-closure.sh}
  decl=${J3_DECLARED_PAIRS-r36-closure.sh}
  for f in "$tree"/corpus/instruments/r*-closure.sh; do
    [ -f "$f" ] || continue
    b=${f##*/}
    known="$known $b"
  done
  awk -v known="$known " -v decl="$decl " -v own="$own" "$(j3_awk_program)" \
      "$tree/SKILL.md"
}

# j3_summary STREAM KEY -> the value of a summary counter (empty when absent).
j3_summary() { # STREAM KEY
  printf '%s\n' "$1" | awk -F'\t' -v k="$2" '$1 == "S" && index($2, k "=") == 1 { sub("^" k "=", "", $2); print $2; exit }'
}

# check_j3_detail TREE -> one "defect: kind line note" line per defect, then the
# payload line.  Used by --detail and by the receipt transcripts.
check_j3_detail() { # TREE
  local tree=${1:-${J3_TREE:-}} out
  [ -n "$tree" ] && [ -f "$tree/SKILL.md" ] || { printf 'read=fail,reason=no-skill-md'; return 1; }
  out=$(j3_scan "$tree") || { printf 'read=fail,reason=parser'; return 1; }
  printf '%s\n' "$out" | awk -F'\t' '$1 == "X" { printf "defect: %s L%s %s\n", $2, $3, $4 }'
  j3_payload "$out" "$tree"
}

# j3_payload STREAM TREE -> the one-line payload; also the exit code carrier.
j3_payload() { # STREAM TREE
  local out=$1 tree=$2 k v
  local tables rows splitn orphan badcells leadws indent dup missing unknown declared
  for k in tables rows split orphan badcells leadws indent dup missing unknown declared; do
    v=$(j3_summary "$out" "$k")
    case $v in ''|*[!0-9]*) printf 'read=fail,reason=counter-%s' "$k"; return 1 ;; esac
    case $k in
      split) splitn=$v ;;
      *) eval "$k=\$v" ;;
    esac
  done
  printf 'tables=%s,rows=%s,split=%s,orphan=%s,badcells=%s,leadws=%s,indent=%s,dup=%s,missing=%s,unknown=%s,declared=%s,own=%s,read=ok' \
    "$tables" "$rows" "${splitn:-0}" "$orphan" "$badcells" "$leadws" "$indent" \
    "$dup" "$missing" "$unknown" "$declared" "${J3_OWN-r42-closure.sh}"
  [ "${splitn:-1}" -eq 0 ] && [ "$orphan" -eq 0 ] && [ "$badcells" -eq 0 ] \
    && [ "$leadws" -eq 0 ] && [ "$indent" -eq 0 ] && [ "$dup" -eq 0 ] \
    && [ "$missing" -eq 0 ]
}

# check_j3 TREE [REF] — the suite entry point.
check_j3() { # TREE [REF]
  local tree=${1:-${J3_TREE:-}} out
  if [ -z "$tree" ] || [ ! -d "$tree" ]; then
    printf 'read=fail,reason=no-tree'
    return 1
  fi
  if [ ! -f "$tree/SKILL.md" ]; then
    printf 'read=fail,reason=no-skill-md'
    return 1
  fi
  if [ ! -d "$tree/corpus/instruments" ]; then
    printf 'read=fail,reason=no-instruments'
    return 1
  fi
  out=$(j3_scan "$tree") || { printf 'read=fail,reason=parser'; return 1; }
  j3_payload "$out" "$tree"
}

# j3_line TREE — check_j3 composed as the suite's one-line form.  Same exit
# status as check_j3.
j3_line() { # TREE
  local p rc
  p=$(check_j3 "$1"); rc=$?
  if [ "$rc" -eq 0 ]; then
    printf 'J3 payload=%s closed=1\n' "$p"
  else
    printf 'J3 payload=%s closed=0\n' "$p"
  fi
  return "$rc"
}

# ---------------------------------------------------------------------------
# the replay limb
# ---------------------------------------------------------------------------

# j3_row_content FILE PREFIX -> the first line that starts with PREFIX.
j3_row_content() { awk -v s="$2" 'index($0, s) == 1 { print; exit }' "$1"; }

# j3_row_number FILE PREFIX -> the line number of that line.
j3_row_number() { awk -v s="$2" 'index($0, s) == 1 { print NR; exit }' "$1"; }

# j3_stub_instruments TREE DIR — mirror the tree's closure-instrument basenames
# into DIR/corpus/instruments as empty files, so `missing` is evaluated against
# the same instrument set as the tree under test.
j3_stub_instruments() { # TREE DIR
  local f b
  for f in "$1"/corpus/instruments/r*-closure.sh; do
    [ -f "$f" ] || continue
    b=${f##*/}
    : > "$2/corpus/instruments/$b" || return 1
  done
}

# j3_mutant NAME FILE — print the mutated SKILL.md bytes for one defeat shape.
# Every shape is one the committed artifacts record: MutSkillTablePipes.md
# variants 1-4, D-r41-3's duplicate row, plus the four shapes the wave-2 seed
# names (indented duplicate, blank between header and separator, deleted row,
# re-introduced legacy bare pipe).
j3_mutant() { # NAME FILE
  local name=$1 f=$2 n row
  case $name in
    m1-blank-before-row)
      n=$(j3_row_number "$f" '| r41-closure.sh |'); [ -n "$n" ] || return 1
      awk -v n="$n" 'NR == n { print "" } { print }' "$f" ;;
    m2-bare-pipe-command)
      awk 'index($0, "| r41-closure.sh |") == 1 && !d { sub(/\(export-mode only/, "(export|mode only"); d = 1 } { print }' "$f" ;;
    m3-leading-ws-first-cell)
      awk 'index($0, "| r41-closure.sh |") == 1 && !d { sub(/^\| r41-closure[.]sh \|/, "|  r41-closure.sh |"); d = 1 } { print }' "$f" ;;
    m4-row-moved-outside)
      row=$(j3_row_content "$f" '| r41-closure.sh |'); [ -n "$row" ] || return 1
      awk 'index($0, "| r41-closure.sh |") != 1' "$f"
      printf '\n%s\n' "$row" ;;
    m5-duplicate-row)
      cat -- "$f"; row=$(j3_row_content "$f" '| r40-closure.sh |'); [ -n "$row" ] || return 1
      printf '%s\n' "$row" ;;
    m6-indented-duplicate)
      cat -- "$f"; row=$(j3_row_content "$f" '| r39-closure.sh |'); [ -n "$row" ] || return 1
      printf ' %s\n' "$row" ;;
    m7-blank-header-separator)
      n=$(j3_row_number "$f" '| r40-closure.sh |'); [ -n "$n" ] || return 1
      awk -v n="$((n - 1))" 'NR == n { print "" } { print }' "$f" ;;
    m8-row-deleted)
      awk 'index($0, "| r39-closure.sh |") != 1' "$f" ;;
    m9-legacy-bare-pipe)
      awk 'index($0, "| recheck-audit.py |") == 1 && !d { sub(/gate[\\][|]probe/, "gate|probe"); d = 1 } { print }' "$f" ;;
    m10-duplicate-in-table)
      n=$(j3_row_number "$f" '| r40-closure.sh |'); [ -n "$n" ] || return 1
      awk -v n="$n" 'NR == n { print; print; next } { print }' "$f" ;;
    m11-cross-table-duplicate)
      row=$(j3_row_content "$f" '| r40-closure.sh |'); [ -n "$row" ] || return 1
      n=$(j3_row_number "$f" '| r39-closure.sh |'); [ -n "$n" ] || return 1
      awk -v n="$n" -v r="$row" 'NR == n { print; print r; next } { print }' "$f" ;;
    *) return 1 ;;
  esac
}

# j3_replay TREE SANDBOX — the REPLAY limb.  Every committed F-TABLE defeat
# shape is re-executed against the CURRENT bytes of TREE/SKILL.md; each must be
# rejected and the unmutated positive must be accepted.  Fixtures are written
# under SANDBOX only (never inside TREE).  A case that cannot be materialized
# counts as a failure, so an absent defeat can never read as a repair.
j3_replay() { # TREE SANDBOX
  local tree=$1 sb=$2 name d payload rc cases=0 fails=0
  local -a names=(positive m1-blank-before-row m2-bare-pipe-command
                  m3-leading-ws-first-cell m4-row-moved-outside m5-duplicate-row
                  m6-indented-duplicate m7-blank-header-separator m8-row-deleted
                  m9-legacy-bare-pipe m10-duplicate-in-table
                  m11-cross-table-duplicate)
  [ -n "$tree" ] && [ -f "$tree/SKILL.md" ] || j3_die "j3_replay: no SKILL.md under '${tree}'"
  [ -n "$sb" ] || j3_die 'j3_replay: a sandbox directory is required'
  mkdir -p -- "$sb" || j3_die "j3_replay: cannot create sandbox $sb"
  for name in "${names[@]}"; do
    d=$sb/$name
    rm -rf -- "$d"; mkdir -p -- "$d/corpus/instruments" || j3_die "j3_replay: mkdir $d"
    j3_stub_instruments "$tree" "$d" || j3_die "j3_replay: stub instruments $d"
    if [ "$name" = positive ]; then
      cp -- "$tree/SKILL.md" "$d/SKILL.md" || j3_die "j3_replay: copy $d"
    else
      j3_mutant "$name" "$tree/SKILL.md" > "$d/SKILL.md" || {
        printf 'selftest detail=J3 mutant=%s rejected=0 payload=not-materialized\n' "$name"
        cases=$((cases + 1)); fails=$((fails + 1)); continue; }
    fi
    payload=$(check_j3 "$d"); rc=$?
    cases=$((cases + 1))
    if [ "$name" = positive ]; then
      if [ "$rc" -eq 0 ]; then
        printf 'selftest detail=J3 case=positive accepted=1 payload=%s\n' "$payload"
      else
        printf 'selftest detail=J3 case=positive accepted=0 payload=%s\n' "$payload"
        fails=$((fails + 1))
      fi
    else
      if [ "$rc" -ne 0 ]; then
        printf 'selftest detail=J3 mutant=%s rejected=1 payload=%s\n' "$name" "$payload"
      else
        printf 'selftest detail=J3 mutant=%s rejected=0 payload=%s\n' "$name" "$payload"
        fails=$((fails + 1))
      fi
    fi
  done
  printf 'selftest cases=%d failures=%d\n' "$cases" "$fails"
  [ "$fails" -eq 0 ]
}

# ---------------------------------------------------------------------------
# the command line
# ---------------------------------------------------------------------------

j3_usage() {
  cat <<'USAGE'
ExecJ3Registry.sh — round-42 J3 SKILL.md registry-integrity limb (F-TABLE)

  bash ExecJ3Registry.sh --check   TREE
  bash ExecJ3Registry.sh --detail  TREE
  bash ExecJ3Registry.sh --line    TREE
  bash ExecJ3Registry.sh --self-test TREE SANDBOX

  --check      print the payload line; exit 0 closed / 1 red
  --detail     print one "defect: <kind> L<n> <note>" line per defect, then
               the payload line
  --line       print the composed suite line "J3 payload=<payload> closed=<0|1>" 
  --self-test  the replay limb: materialize every committed F-TABLE defeat
               shape under SANDBOX, require rejection of each and acceptance
               of the positive control; print selftest lines

  Sourcing this file defines check_j3, check_j3_detail, j3_replay and the
  j3_* helpers; it runs nothing.
USAGE
}

j3_main() {
  local mode='' tree='' sb='' rc=0
  [ $# -gt 0 ] || { j3_usage >&2; exit 2; }
  while [ $# -gt 0 ]; do
    case $1 in
      --check|--detail|--line|--self-test) mode=${1#--}; shift ;;
      --help|-h) j3_usage; exit 0 ;;
      -*) j3_die "unknown option: $1" ;;
      *) if [ -z "$tree" ]; then tree=$1
         elif [ -z "$sb" ]; then sb=$1
         else j3_die "extra argument: $1"; fi
         shift ;;
    esac
  done
  [ -n "$mode" ] || j3_die 'one of --check, --detail, --self-test is required'
  [ -n "$tree" ] || j3_die 'a TREE argument is required'
  case $mode in
    check) check_j3 "$tree"; rc=$?; printf '\n'; exit "$rc" ;;
    detail) check_j3_detail "$tree"; rc=$?; printf '\n'; exit "$rc" ;;
    line) j3_line "$tree"; exit $? ;;
    self-test) j3_replay "$tree" "$sb"; exit $? ;;
  esac
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then j3_main "$@"; fi
