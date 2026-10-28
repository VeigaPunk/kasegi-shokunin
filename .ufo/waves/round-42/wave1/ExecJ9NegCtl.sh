#!/usr/bin/env bash
# r42 J9 limb — negative controls for the round-42 closure suite.
#
# Contract (frozen claim C1, check J9 — "negative controls"):
#
#   J9 runs the SUITE ITSELF over the two control refs and requires both to
#   be red, and it proves that an unresolvable ref produces a DISTINCT red
#   instead of a tally that could be misread as a control:
#
#     control 1  base commit            5053a7f46de35784cff4b56756906e9014a38276
#     control 2  round-41 judged head   1f7464612ac4c44e39886b82e812610d3c039b13
#     control 3  unresolvable ref       deadbeef… (never a tally)
#
#   The two control refs are exported INSIDE the suite's work dir and the
#   SAME suite bytes are invoked recursively on them (leaf mode, depth 1), so
#   the control measures the committed suite and not a re-implementation.
#   Each control run must print `closed=K/13 exit=1` with K < 13.
#
# WHY THE CONTROL IS NOT VACUOUS. A nested run is depth-capped: its own J9
# limb cannot nest again. A control tree that is green in every other respect
# would therefore score 12 of 13 — and "closed < 13, exit 1" would accept it.
# That is the round-40 wave-2 M-H8a class the round-41 verifier routed, and
# the round-41 suite's own I10 had to be repaired for exactly this.
#
# The primary kill is THE LEAF CEILING. The ceiling is the largest tally a
# tree whose other checks are all green could score: 13 when the nested run's
# own J9 line is green, else 12 (the depth cap costs exactly one check). It
# is read from the nested run's own J9 line, so the suite grades itself
# against its own behaviour. Every control must score STRICTLY below that
# ceiling. This is airtight against the leaf-capped green base:
#
#     a green control tree scores 13 with J9 green  -> ceiling 13, 13 < 13 false
#     a green control tree scores 12 with J9 red    -> ceiling 12, 12 < 12 false
#
# and a lying J9 bit does not help: to look green the tree needs 13 closed
# checks, and the ceiling never exceeds 13, so no control run can both score
# 13 and stay below the ceiling.
#
# TREE-DEPENDENT REDNESS (optional, off by default). R42_J9_TREEDEP names the
# checks that must additionally be RED in a control run — the round-41 I10
# design demanded tree-dependent reasons rather than any red. It is OFF by
# default because a hard-coded set is a FALSE-RED risk: if the suite's J1,
# J3 or J8 is vacuously green on a tree that carries no round-42 artifacts
# (nothing to grade => nothing failed), the ceiling clause still rejects a
# leaf-capped green base, but the treedep clause would reject the HONEST
# control too and make 13/13 unreachable at the judged head. Turn it on only
# after confirming the named checks are red on both control trees:
#     R42_J9_TREEDEP="J1 J3 J8"
#
# Additional non-vacuity clauses on every control run:
#     * the exit status must be exactly 1 (0 = green, 2 = harness error: both
#       fail closed);
#     * exactly 13 check lines, one per id J1..J13, each `closed=0|1`, so a
#       summary-only or truncated output cannot satisfy the control;
#     * the number of `closed=1` lines must EQUAL the tally numerator, so a
#       lying tally is rejected;
#     * the tally is read as a BOUNDED token (`^closed=[0-9]+/13 exit=[01]$`),
#       so a mangled `closed=13/130` cannot pass (round-40 wave-2 T2);
#     * the transcript may not contain `ref-not-found`: a control whose own
#       ref did not resolve is a harness error, not a tree-dependent red;
#     * the transcript may not contain `closed=13/13` under any spelling.
#
#   Control 3 (the distinct red): the same suite bytes invoked with an
#   unresolvable --export-ref must exit 1, must carry the `ref-not-found`
#   marker (a `suite-ref-status=ref-not-found` line, or `ref-not-found`
#   inside a check-line payload or on a line of its own), must never print
#   `closed=13/13`, and — when it prints a numeric tally at all — the tally
#   must be `closed=0/13`: a ref-not-found red is a distinct red, never a
#   partial tally that could be mistaken for a tree-dependent control red.
#
# INTEGRATION CONTRACT (the suite core, corpus/instruments/r42-closure.sh,
# sources this file):
#   * the suite calls `check_j9 "$EXPORT" "$REF_RESOLVED"` — the same
#     signature as every other limb: (TREE, REF) — and reads ONE payload
#     line from stdout; exit status 0 = closed, 1 = open;
#   * the suite MUST honour R42_DEPTH >= 1 as leaf mode: a depth-capped run
#     performs NO nested exports. This limb honours both R42_DEPTH and
#     R42_J9_DEPTH, so it never recurses through its own door even if the
#     suite core forgot the depth guard;
#   * the suite's own script path is corpus/instruments/r42-closure.sh
#     inside the export; when the export carries no suite copy (the base and
#     round-41 control trees carry none) this limb falls back to the running
#     script and records which copy was used in the payload
#     (`suite=export` or `suite=self`), so the payload stays a function of
#     the tree and the ref and never of the caller's shell state;
#   * the nested runs are given a PRIVATE scratch root (a fresh empty
#     directory under the work dir), never the host-global scratch root: a
#     control must measure the tree, not another seat's scratch residue;
#   * the tree-dependent checks named above must be RED on any tree that
#     carries no round-42 artifacts (the base commit and the round-41 judged
#     head are such trees). A vacuously green J1/J3/J8 — one that passes
#     because the round-42 artifacts are absent rather than because they are
#     present and well-formed — makes J9 red; that is the intended reading.
#
# ENVIRONMENT KNOBS (documented so wave-2 seats can point defeats at the
# live suite; every knob is inert unless it is set):
#   R42_DEPTH=1          leaf mode for the suite (no nested exports)
#   R42_J9_DEPTH=1       leaf mode for this limb alone (no nesting)
#   R42_J9_TREEDEP="J1 J3 J8"   the tree-dependent checks a control must red
#   R42_J9_CAP=N         override the derived leaf ceiling (selftest only)
#   R42_J9_BASE=<ref>    override control ref 1 (selftest only)
#   R42_J9_R41=<ref>     override control ref 2 (selftest only)
#   R42_J9_DEAD=<ref>    override the unresolvable ref (selftest only)
#   R42_J9_LANE=<dir>    lane repo used to export the control refs
#   R42_J9_WORK=<dir>    work dir the nested runs write into
#   R42_J9_SCRATCH=<dir> scratch root handed to the nested runs
#   R42_J9_SELF=<path>   the suite script to invoke for the nested runs
#
# Exit codes: 0 green, 1 red, 2 harness error (unusable inputs).
#
# Sourceable: sourcing this file defines the functions and executes nothing.
# Executed directly it runs the stub-driven selftest (--selftest) or prints
# the usage text (--help).

J9_BASE_REF=${R42_J9_BASE:-5053a7f46de35784cff4b56756906e9014a38276}
J9_R41_REF=${R42_J9_R41:-1f7464612ac4c44e39886b82e812610d3c039b13}
J9_DEAD_REF=${R42_J9_DEAD:-deadbeefdeadbeefdeadbeefdeadbeefdeadbeef}
J9_CHECKS=13
J9_SUITE_REL=corpus/instruments/r42-closure.sh
J9_TREEDEP=${R42_J9_TREEDEP:-}

# ---------------------------------------------------------------------------
# context resolution (lane, work dir, scratch root, running script)
# ---------------------------------------------------------------------------

j9_abs() { # PATH -> absolute path or nothing
  local p=$1
  [ -n "$p" ] || return 1
  case $p in
    /*) printf '%s\n' "$p" ;;
    *)  printf '%s/%s\n' "$(pwd -P)" "$p" ;;
  esac
}

# j9_lane_candidate — the lane directory, from LANE or from the path of the
# running script (corpus/instruments/<script> is two levels below the lane).
j9_lane_candidate() {
  local l=${LANE:-}
  if [ -z "$l" ]; then
    local s=${R42_J9_SELF:-$0}
    s=$(j9_abs "$s") || return 1
    l=$( cd -- "$(dirname -- "$s")/../.." 2>/dev/null && pwd -P ) || return 1
  fi
  [ -n "$l" ] && [ -d "$l" ] || return 1
  printf '%s\n' "$l"
}

j9_lane() {
  local l=${R42_J9_LANE:-}
  [ -n "$l" ] || l=$(j9_lane_candidate) || return 1
  [ -d "$l" ] || return 1
  printf '%s\n' "$l"
}

j9_work() {
  local w=${R42_J9_WORK:-${WORK:-}}
  [ -n "$w" ] || return 1
  printf '%s\n' "$w"
}

j9_scratch() {
  printf '%s\n' "${R42_J9_SCRATCH:-${SCRATCH_ROOT:-/fast/scratch/hyaku}}"
}

# j9_self — the suite script this limb is running inside of.
#
# Resolution order:
#   1. R42_J9_SELF (explicit; the suite may set it to its own path);
#   2. $0 — the script the shell is running (the suite, whether the limb is
#      embedded in it or sourced by it);
#   3. <lane>/corpus/instruments/r42-closure.sh — the canonical location;
#   4. BASH_SOURCE[0] — the limb file itself (last resort: the limb run
#      directly, which only happens in the selftest).
j9_self() {
  local s=${R42_J9_SELF:-}
  if [ -z "$s" ]; then
    s=$0
    if [ ! -f "$s" ]; then
      local l
      l=$(j9_lane_candidate) || l=''
      if [ -n "$l" ]; then s="$l/$J9_SUITE_REL"; fi
    fi
    if [ ! -f "$s" ]; then s=${BASH_SOURCE[0]:-}; fi
  fi
  [ -n "$s" ] || return 1
  s=$(j9_abs "$s") || return 1
  [ -f "$s" ] || return 1
  printf '%s\n' "$s"
}

j9_depth() {
  local d=${R42_J9_DEPTH:-0}
  if [ "${R42_DEPTH:-0}" -gt "$d" ] 2>/dev/null; then d=${R42_DEPTH:-0}; fi
  printf '%s\n' "$d"
}

# ---------------------------------------------------------------------------
# parsing helpers
# ---------------------------------------------------------------------------

# j9_tally FILE — print "K E" of the LAST bounded tally line, or nothing.
# The line must match exactly `closed=<digits>/13 exit=<0|1>`; anything else
# (a mangled denominator, a summary line, trailing text) is not a tally.
j9_tally() {
  awk -v n="$J9_CHECKS" '
    $0 ~ ("^closed=[0-9]+/" n " exit=[01]$") {
      k = $0; sub(/^closed=/, "", k); split(k, p, "/"); k = p[1]
      e = $0; sub(/.* exit=/, "", e)
      K = k; E = e
    }
    END { if (K != "") printf "%s %s\n", K, E }
  ' "$1"
}

# j9_check_lines FILE — print "<id> <closed>" for every well-formed check
# line. A check line is `J<id> payload=... closed=<0|1>`.
j9_check_lines() {
  awk '
    $0 ~ /^J[0-9]+ payload=.* closed=[01]$/ {
      id = $0; sub(/^J/, "", id); sub(/ .*/, "", id)
      c = $0; sub(/.* closed=/, "", c)
      print id, c
    }
  ' "$1"
}

# j9_check_closed FILE ID — the closed bit of check ID, or "?" when absent.
# The id may be given with or without the `J` prefix.
j9_check_closed() {
  local id=${2#J}
  j9_check_lines "$1" | awk -v id="$id" '$1 == id { print $2; exit }'
}

j9_has_token() { grep -qF -- "$2" "$1"; }

# j9_rnf_kind FILE — how (if at all) this transcript is a ref-not-found red.
# Prints one of:
#   status     the transcript carries the explicit status line
#              `suite-ref-status=ref-not-found`
#   all-lines  EVERY well-formed check line's payload begins with
#              `ref-not-found` (the r41 print_ref_not_found shape)
#   none       neither: this is an ordinary run
#
# The distinction matters because a check payload may MENTION the token
# without being one: the committed r41 receipt carries
# `I12 payload=…ref-not-found=1,markers=0,neg-red=1 closed=1`, so a plain
# substring search for `ref-not-found` would misread an ordinary transcript
# as a ref-not-found red. Only the status line and the all-lines shape count.
j9_rnf_kind() {
  local file=$1
  if grep -q '^suite-ref-status=ref-not-found' "$file"; then
    printf 'status\n'
    return 0
  fi
  local total rnf
  total=$(j9_check_lines "$file" | wc -l | tr -d ' ')
  [ "${total:-0}" -gt 0 ] || { printf 'none\n'; return 0; }
  rnf=$(j9_check_lines "$file" \
        | awk '$2 ~ /^0$/ { if ($0 ~ / payload=ref-not-found/) c++ } END { print c + 0 }')
  [ "${rnf:-0}" -eq "$total" ] && { printf 'all-lines\n'; return 0; }
  printf 'none\n'
  return 0
}

# j9_any_green_tally FILE — 1 when ANY bounded tally line claims 13/13.
# Scoped to the tally lines so a payload that merely mentions the string
# `closed=13/13` cannot false-red a control.
j9_any_green_tally() {
  awk -v n="$J9_CHECKS" '
    $0 ~ ("^closed=13/" n " exit=[01]$") { found = 1 }
    END { exit (found ? 0 : 1) }
  ' "$1"
}

# ---------------------------------------------------------------------------
# one nested control run
# ---------------------------------------------------------------------------

# j9_run SUITE REF TAG WORKDIR LANE OUT
# Runs the given suite bytes over REF in leaf mode with a PRIVATE scratch
# root (the work dir lives beside it, so the suite's own scratch scan sees a
# self-contained tree), writing stdout to OUT and stderr next to it. Returns
# the child's exit status; the caller reads the transcript from OUT.
j9_run() {
  local suite=$1 ref=$2 tag=$3 work=$4 lane=$5 out=$6
  local dir="$work/neg-$tag"
  rm -rf -- "$dir"
  mkdir -p -- "$dir/scratch" || return 2
  : > "$out"
  (
    cd -- "$dir" || exit 2
    env -u R42_J9_BASE -u R42_J9_R41 -u R42_J9_DEAD -u R42_J9_CAP \
        R42_DEPTH=1 R42_J9_DEPTH=1 \
      bash "$suite" --export-ref "$ref" --lane "$lane" \
           --work "$dir/work" --scratch-root "$dir/scratch"
  ) > "$out" 2> "$out.err"
  return $?
}

# j9_control VERDICT_FILE RC CEILING — grade one control run.
# Prints "K=<k> rc=<rc> lines=<n> closed1=<n> treedep=<red|green>
# verdicts=yes|no" and returns 0 iff the run is an acceptable control: a
# tree-dependent red, strictly below the leaf ceiling.
j9_control() {
  local file=$1 rc=$2 ceiling=$3
  local tally k e lines closed1 ids want verdict=0 treedep=red
  local i dep
  tally=$(j9_tally "$file")
  if [ -n "$tally" ]; then
    k=${tally%% *}; e=${tally##* }
  else
    k='?'; e='?'
  fi
  lines=$(j9_check_lines "$file" | wc -l | tr -d ' ')
  closed1=$(j9_check_lines "$file" | awk '$2 == 1 { c++ } END { print c + 0 }')
  ids=$(j9_check_lines "$file" | awk '{ print $1 }' | sort -n | tr '\n' ' ')
  want=''
  for i in $(seq 1 "$J9_CHECKS"); do want="$want$i "; done
  [ "$rc" -eq 1 ] || verdict=1
  case $k in ''|*[!0-9]*) verdict=1 ;; esac
  case $e in ''|*[!0-9]*) verdict=1 ;; esac
  if [ "$verdict" -eq 0 ]; then
    [ "$e" -eq 1 ] || verdict=1
    [ "$k" -le 12 ] || verdict=1
    # the leaf ceiling: a control that reaches the ceiling is a leaf-capped
    # green tree and is rejected (round-40 wave-2 M-H8a)
    [ "$k" -lt "$ceiling" ] || verdict=1
    [ "$closed1" -eq "$k" ] || verdict=1
    [ "$lines" -eq "$J9_CHECKS" ] || verdict=1
    [ "$ids" = "$want" ] || verdict=1
    # a control run that failed to resolve its own ref is a harness error,
    # not a tree-dependent red. The check is on the transcript's SHAPE, not
    # on a substring: a payload may mention `ref-not-found` without being
    # one (the committed r41 receipt's I12 payload does).
    case $(j9_rnf_kind "$file") in
      none) : ;;
      *)    verdict=1 ;;
    esac
    j9_any_green_tally "$file" && verdict=1
  fi
  # the tree-dependent checks must be RED in this run. The set is empty by
  # default (see the header); when it is set, every named check must be red.
  for dep in $J9_TREEDEP; do
    case $(j9_check_closed "$file" "$dep") in
      0) : ;;
      *) treedep=green ;;
    esac
  done
  [ "$treedep" = red ] || verdict=1
  printf 'K=%s rc=%s lines=%s closed1=%s treedep=%s verdicts=%s' \
    "$k" "$rc" "$lines" "$closed1" "$treedep" \
    "$([ "$verdict" -eq 0 ] && echo yes || echo no)"
  return "$verdict"
}

# ---------------------------------------------------------------------------
# the limb
# ---------------------------------------------------------------------------

# check_j9 TREE REF — the J9 check. Prints one payload line; 0 = closed.
check_j9() {
  local tree=${1:-} ref=${2:-}
  local lane work scratch self copy kind depth
  depth=$(j9_depth)
  if [ "$depth" -ge 1 ]; then
    # Leaf mode: the nested control never nests again. The depth cap is
    # visible in the payload so the outer run can derive the ceiling from
    # the nested transcript instead of assuming it.
    printf 'suite=leaf,depth=%s,base=?,r41=?,ceiling=?,refnf=?\n' "$depth"
    return 1
  fi
  if ! lane=$(j9_lane); then
    printf 'suite=none,error=lane-unresolved,base=?,r41=?,ceiling=?,refnf=?\n'
    return 2
  fi
  if ! work=$(j9_work); then
    printf 'suite=none,error=no-work-dir,base=?,r41=?,ceiling=?,refnf=?\n'
    return 2
  fi
  scratch=$(j9_scratch)
  # The work dir must be outside the lane: the nested runs write into it.
  case "$work" in
    "$lane"|"$lane"/*)
      printf 'suite=none,error=work-inside-lane,base=?,r41=?,ceiling=?,refnf=?\n'
      return 2 ;;
  esac
  mkdir -p -- "$work" || {
    printf 'suite=none,error=work-unusable,base=?,r41=?,ceiling=?,refnf=?\n'
    return 2
  }

  # Which suite bytes are the control measured on: the export's own copy when
  # the export carries one, else the running script.
  copy="$tree/$J9_SUITE_REL"
  if [ -f "$copy" ]; then
    kind=export
  elif self=$(j9_self); then
    copy=$self; kind=self
  else
    printf 'suite=none,error=suite-copy-absent,base=?,r41=?,ceiling=?,refnf=?\n'
    return 2
  fi

  # --- control 1: the base commit -----------------------------------------
  local base_out="$work/j9-base.out" base_rc
  j9_run "$copy" "$J9_BASE_REF" base "$work" "$lane" "$base_out"
  base_rc=$?

  # --- control 2: the round-41 judged head --------------------------------
  local r41_out="$work/j9-r41.out" r41_rc
  j9_run "$copy" "$J9_R41_REF" r41 "$work" "$lane" "$r41_out"
  r41_rc=$?

  # --- control 3: an unresolvable ref -------------------------------------
  local dead_out="$work/j9-dead.out" dead_rc
  j9_run "$copy" "$J9_DEAD_REF" dead "$work" "$lane" "$dead_out"
  dead_rc=$?

  # --- the leaf ceiling ---------------------------------------------------
  # The ceiling is the largest tally a tree could score under the depth cap.
  # The cap costs exactly the checks the leaf-mode run forces red, and the
  # leaf mode is this limb's own: check_j9 returns 1 (red) at depth >= 1.
  # So the cap normally costs exactly one check and the ceiling is 12.
  #
  # The ceiling is READ from the control run's own J9 line rather than
  # assumed: if the nested run's J9 line is green, the cap did not bite and
  # the ceiling is 13. Both cases are airtight against the leaf-capped green
  # base:
  #
  #     a green control tree scores 12 with J9 red   -> ceiling 12, 12 < 12 false
  #     a green control tree scores 13 with J9 green -> ceiling 13, 13 < 13 false
  #
  # and a lying J9 bit cannot help: to look green the tree needs 13 closed
  # checks, and the ceiling never exceeds 13, so no control run can both
  # score 13 and stay below the ceiling.
  #
  # The ceiling is derived from the CONTROL run, never from a run over the
  # ref under test: the ref under test's own receipt grading compares
  # recorded payload values against re-derived ones, so measuring the
  # ceiling there would be circular (the receipt records this limb's payload,
  # which records the ceiling).
  local ceiling=${R42_J9_CAP:-} j9closed
  if [ -z "$ceiling" ]; then
    j9closed=$(j9_check_closed "$base_out" 9)
    case $j9closed in
      1) ceiling=13 ;;
      *) ceiling=12 ;;
    esac
  fi
  case $ceiling in ''|*[!0-9]*) ceiling=12 ;; esac

  # --- grade --------------------------------------------------------------
  local base_verdict r41_verdict
  base_verdict=$(j9_control "$base_out" "$base_rc" "$ceiling")
  r41_verdict=$(j9_control "$r41_out" "$r41_rc" "$ceiling")

  # control 3: the distinct ref-not-found red
  local dead_verdict=0 dead_k='?' dead_e='?' dead_mark=0 dead_kind=none dtally
  dtally=$(j9_tally "$dead_out")
  if [ -n "$dtally" ]; then
    dead_k=${dtally%% *}; dead_e=${dtally##* }
  fi
  dead_kind=$(j9_rnf_kind "$dead_out")
  if [ "$dead_rc" -eq 1 ] \
     && [ "$dead_kind" != none ] \
     && ! j9_any_green_tally "$dead_out"; then
    dead_mark=1
    case $dead_k in
      ''|*[!0-9]*) : ;;               # no numeric tally: the marker stands alone
      *) [ "$dead_k" -eq 0 ] || dead_verdict=1 ;;
    esac
    case $dead_e in
      ''|*[!0-9]*) : ;;
      *) [ "$dead_e" -eq 1 ] || dead_verdict=1 ;;
    esac
  fi

  local closed=1
  case "$base_verdict" in *'verdicts=yes'*) ;; *) closed=0 ;; esac
  case "$r41_verdict" in *'verdicts=yes'*) ;; *) closed=0 ;; esac
  [ "$dead_verdict" -eq 0 ] || closed=0

  # The payload is FLAT `k=v` pairs, comma-separated, so the suite's payload
  # table can read any single field without parsing nested groups.
  local base_k base_rc base_lines base_c1 base_td base_v
  local r41_k r41_rc r41_lines r41_c1 r41_td r41_v
  base_k=${base_verdict#K=};     base_k=${base_k%% *}
  base_rc=${base_verdict#*rc=};  base_rc=${base_rc%% *}
  base_lines=${base_verdict#*lines=}; base_lines=${base_lines%% *}
  base_c1=${base_verdict#*closed1=}; base_c1=${base_c1%% *}
  base_td=${base_verdict#*treedep=}; base_td=${base_td%% *}
  base_v=${base_verdict#*verdicts=}
  r41_k=${r41_verdict#K=};     r41_k=${r41_k%% *}
  r41_rc=${r41_verdict#*rc=};  r41_rc=${r41_rc%% *}
  r41_lines=${r41_verdict#*lines=}; r41_lines=${r41_lines%% *}
  r41_c1=${r41_verdict#*closed1=}; r41_c1=${r41_c1%% *}
  r41_td=${r41_verdict#*treedep=}; r41_td=${r41_td%% *}
  r41_v=${r41_verdict#*verdicts=}

  printf 'suite=%s,base-K=%s,base-rc=%s,base-lines=%s,base-closed1=%s,base-treedep=%s,base-verdicts=%s,r41-K=%s,r41-rc=%s,r41-lines=%s,r41-closed1=%s,r41-treedep=%s,r41-verdicts=%s,ceiling=%s,refnf-K=%s,refnf-rc=%s,refnf-kind=%s,refnf-mark=%s,closed=%s\n' \
    "$kind" \
    "$base_k" "$base_rc" "$base_lines" "$base_c1" "$base_td" "$base_v" \
    "$r41_k" "$r41_rc" "$r41_lines" "$r41_c1" "$r41_td" "$r41_v" \
    "$ceiling" "$dead_k" "$dead_rc" "$dead_kind" "$dead_mark" \
    "$([ "$closed" -eq 1 ] && echo 1 || echo 0)"
  [ "$closed" -eq 1 ] && return 0
  return 1
}

# ---------------------------------------------------------------------------
# selftest (executed only when this file is run, never when it is sourced)
# ---------------------------------------------------------------------------

# j9_stub SUITE_PATH [BASE_SPEC] [R41_SPEC]
# A stub suite that answers per --export-ref, so every clause in the
# acceptance predicate can be exercised without a lane. The stub's check
# lines and its tally are CONSISTENT (exactly K lines are closed=1 and the
# rest closed=0), so a stub is never rejected for the wrong reason.
#
# A SPEC is `K:TREEDEP:J9`:
#   K        the tally the stub prints (and the number of closed=1 lines)
#   TREEDEP  `red`   — the tree-dependent checks J1/J3/J8 are red
#            `green` — they are green
#   J9       `red`   — the depth-capped J9 limb is red (the leaf cap bites,
#                     so the ceiling is 12)
#            `green` — J9 is green too (the ceiling is 13)
j9_stub() {
  local out=$1 bs=${2:-5:red:red} rs=${3:-7:red:red}
  export J9S_BS=$bs J9S_RS=$rs
  cat > "$out" <<'STUB'
#!/usr/bin/env bash
# stub suite: answers per --export-ref
ref=''; prev=''
for a in "$@"; do
  [ "$prev" = '--export-ref' ] && ref=$a
  prev=$a
done
# emit_tally SPEC EXIT — SPEC is K:TREEDEP:J9
emit_tally() {
  local spec=$1 e=$2
  local k=${spec%%:*} rest=${spec#*:}
  local td=${rest%%:*} jm=${rest##*:}
  local i closed ones=0 forced=0 want
  case $td in green) forced=$((forced + 3)) ;; esac
  case $jm in green) forced=$((forced + 1)) ;; esac
  want=$((k - forced))
  for i in $(seq 1 13); do
    closed=0
    case "$i" in
      9) [ "$jm" = green ] && closed=1 ;;
      1|3|8) [ "$td" = green ] && closed=1 ;;
      *) if [ "$ones" -lt "$want" ]; then closed=1; ones=$((ones + 1)); fi ;;
    esac
    printf 'J%s payload=stub,note=depth-capped closed=%s\n' "$i" "$closed"
  done
  printf 'selftest cases=13 failures=0\n'
  printf 'closed=%s/13 exit=%s\n' "$k" "$e"
}
case $ref in
  5053a7f*)  emit_tally "$J9S_BS" 1; exit 1 ;;
  1f746461*) emit_tally "$J9S_RS" 1; exit 1 ;;
  deadbeef*) printf 'suite-ref-status=ref-not-found\n'
              for i in $(seq 1 13); do
                printf 'J%s payload=ref-not-found,ref=%s closed=0\n' "$i" "$ref"
              done
              printf 'closed=0/13 exit=1\n'
              exit 1 ;;
  *)         exit 2 ;;
esac
exit 0
STUB
  chmod +x "$out"
}

# j9_stub_variant PATH K E DEADMODE — a stub whose tally the caller chooses,
# for the control refs. DEADMODE is `red` (the distinct ref-not-found red)
# or `green` (a green tally, which is NOT a distinct red). The tree-dependent
# ids J1/J3/J8 are red, J9 is red (the leaf cap bites) and the remaining ids
# fill K, so the stub is internally consistent. The ceiling run (any other
# ref) answers with the leaf-capped green tally 12:green:red.
j9_stub_variant() {
  local out=$1 k=$2 e=$3 dead=$4
  export J9S_K=$k J9S_E=$e J9S_DEAD=$dead
  cat > "$out" <<'STUB'
#!/usr/bin/env bash
ref=''; prev=''
for a in "$@"; do
  [ "$prev" = '--export-ref' ] && ref=$a
  prev=$a
done
emit_tally() { local i closed ones=0
  for i in $(seq 1 13); do closed=0
    case "$i" in
      9) : ;;
      1|3|8) : ;;
      *) if [ "$ones" -lt "$J9S_K" ]; then closed=1; ones=$((ones + 1)); fi ;;
    esac
    printf 'J%s payload=stub closed=%s\n' "$i" "$closed"; done
  printf 'closed=%s/13 exit=%s\n' "$J9S_K" "$J9S_E"; }
emit_ceiling() { local i closed ones=0
  for i in $(seq 1 13); do closed=0
    case "$i" in
      9) : ;;
      *) closed=1; ones=$((ones + 1)) ;;
    esac
    printf 'J%s payload=stub,note=leaf-capped-green closed=%s\n' "$i" "$closed"; done
  printf 'closed=12/13 exit=1\n'; }
emit_rnf() {
  printf 'suite-ref-status=ref-not-found\n'
  for i in $(seq 1 13); do
    printf 'J%s payload=ref-not-found,ref=%s closed=0\n' "$i" "$ref"
  done
  printf 'closed=0/13 exit=1\n'
  exit 1
}
case $ref in
  5053a7f*|1f746461*) emit_tally; exit "$J9S_E" ;;
  deadbeef*)
    if [ "$J9S_DEAD" = green ]; then emit_tally; exit 0; fi
    emit_rnf ;;
  *) emit_ceiling; exit 1 ;;
esac
exit 0
STUB
  chmod +x "$out"
}

# j9_stub_unresolvable_control PATH — a stub whose CONTROL refs also fail to
# resolve: the control run reports ref-not-found instead of a tree-dependent
# red. That is a harness error and must NOT be accepted as a control.
j9_stub_unresolvable_control() {
  local out=$1
  cat > "$out" <<'STUB'
#!/usr/bin/env bash
printf 'suite-ref-status=ref-not-found\n'
for i in $(seq 1 13); do
  printf 'J%s payload=ref-not-found,ref=%s closed=0\n' "$i" "$1"
done
printf 'closed=0/13 exit=1\n'
exit 1
STUB
  chmod +x "$out"
}

# j9_selftest — the stub-driven cases. Each case names the acceptance clause
# it exercises; a case passes when the clause REJECTS the defect.
j9_selftest() {
  local t cases=0 fails=0 stub lane work tree
  t=$(mktemp -d "${TMPDIR:-/tmp}/j9-selftest.XXXXXX") || return 2
  stub="$t/suite.sh"
  j9_stub "$stub"
  lane=$t/lane; mkdir -p "$lane"
  work=$t/work; mkdir -p "$work"
  tree=$t/tree

  # The stub is reached through the export tree, so the limb's `suite=export`
  # branch is the one under test.
  mkdir -p "$tree/corpus/instruments"
  cp -p "$stub" "$tree/corpus/instruments/r42-closure.sh"

  st_case() { # LABEL EXPECT(red|green)
    local label=$1 expect=$2
    cases=$((cases + 1))
    if [ "$J9_ST_FAIL" -eq 0 ]; then
      printf 'selftest case=%s expect=%s verdict=pass\n' "$label" "$expect"
    else
      printf 'selftest case=%s expect=%s verdict=FAIL\n' "$label" "$expect"
      fails=$((fails + 1))
    fi
  }

  # positive: the honest controls are accepted
  J9_ST_FAIL=0
  R42_J9_LANE="$lane" R42_J9_WORK="$work" \
    check_j9 "$tree" deadbeef > "$t/p.out" 2>&1 || J9_ST_FAIL=1
  st_case honest-controls-accepted green

  # the leaf-capped GREEN base (round-40 wave-2 M-H8a): the tree-dependent
  # checks are green and the tally reaches the ceiling — it must be rejected
  J9_ST_FAIL=0
  j9_stub "$t/cap.sh" '12:green:red' '12:green:red'
  mkdir -p "$t/tree2/corpus/instruments"
  cp -p "$t/cap.sh" "$t/tree2/corpus/instruments/r42-closure.sh"
  R42_J9_LANE="$lane" R42_J9_WORK="$work" \
    check_j9 "$t/tree2" deadbeef > "$t/cap.out" 2>&1 && J9_ST_FAIL=1
  st_case leaf-capped-green-base-rejected red

  # a GREEN base (K = 13) must be rejected
  J9_ST_FAIL=0
  j9_stub_variant "$t/green.sh" 13 0 red
  mkdir -p "$t/tree3/corpus/instruments"
  cp -p "$t/green.sh" "$t/tree3/corpus/instruments/r42-closure.sh"
  R42_J9_LANE="$lane" R42_J9_WORK="$work" \
    check_j9 "$t/tree3" deadbeef > "$t/green.out" 2>&1 && J9_ST_FAIL=1
  st_case green-base-rejected red

  # a control whose ref did not resolve (a ref-not-found transcript) must be
  # rejected: that is a harness error, not a tree-dependent red
  J9_ST_FAIL=0
  j9_stub_unresolvable_control "$t/rnf.sh"
  mkdir -p "$t/tree4/corpus/instruments"
  cp -p "$t/rnf.sh" "$t/tree4/corpus/instruments/r42-closure.sh"
  R42_J9_LANE="$lane" R42_J9_WORK="$work" \
    check_j9 "$t/tree4" deadbeef > "$t/rnf.out" 2>&1 && J9_ST_FAIL=1
  st_case unresolvable-control-rejected red

  # a summary-only control (no check lines) must be rejected
  J9_ST_FAIL=0
  printf '#!/usr/bin/env bash\nprintf "closed=5/13 exit=1\\n"\nexit 1\n' > "$t/sum.sh"
  chmod +x "$t/sum.sh"
  mkdir -p "$t/tree5/corpus/instruments"
  cp -p "$t/sum.sh" "$t/tree5/corpus/instruments/r42-closure.sh"
  R42_J9_LANE="$lane" R42_J9_WORK="$work" \
    check_j9 "$t/tree5" deadbeef > "$t/sum.out" 2>&1 && J9_ST_FAIL=1
  st_case summary-only-control-rejected red

  # a mangled tally denominator (closed=13/130) must be rejected
  J9_ST_FAIL=0
  printf '#!/usr/bin/env bash\nref=""; prev=""\nfor a in "$@"; do [ "$prev" = "--export-ref" ] && ref=$a; prev=$a; done\nfor i in $(seq 1 13); do c=0; case "$i" in J1|J3|J8) c=0 ;; *) c=1 ;; esac; printf "J%%s payload=stub closed=%%s\\n" "$i" "$c"; done\nprintf "closed=13/130 exit=1\\n"\nexit 1\n' > "$t/man.sh"
  chmod +x "$t/man.sh"
  mkdir -p "$t/tree6/corpus/instruments"
  cp -p "$t/man.sh" "$t/tree6/corpus/instruments/r42-closure.sh"
  R42_J9_LANE="$lane" R42_J9_WORK="$work" \
    check_j9 "$t/tree6" deadbeef > "$t/man.out" 2>&1 && J9_ST_FAIL=1
  st_case mangled-tally-rejected red

  # a lying tally (the numerator does not match the closed=1 lines) is rejected
  J9_ST_FAIL=0
  printf '#!/usr/bin/env bash\nref=""; prev=""\nfor a in "$@"; do [ "$prev" = "--export-ref" ] && ref=$a; prev=$a; done\nfor i in $(seq 1 13); do c=0; case "$i" in J1|J3|J8) c=0 ;; *) c=1 ;; esac; printf "J%%s payload=stub closed=%%s\\n" "$i" "$c"; done\nprintf "closed=11/13 exit=1\\n"\nexit 1\n' > "$t/lying.sh"
  chmod +x "$t/lying.sh"
  mkdir -p "$t/tree7/corpus/instruments"
  cp -p "$t/lying.sh" "$t/tree7/corpus/instruments/r42-closure.sh"
  R42_J9_LANE="$lane" R42_J9_WORK="$work" \
    check_j9 "$t/tree7" deadbeef > "$t/lying.out" 2>&1 && J9_ST_FAIL=1
  st_case lying-tally-rejected red

  # a dead-ref transcript that prints closed=13/13 is not a distinct red
  J9_ST_FAIL=0
  j9_stub_variant "$t/dg.sh" 13 0 green
  mkdir -p "$t/tree8/corpus/instruments"
  cp -p "$t/dg.sh" "$t/tree8/corpus/instruments/r42-closure.sh"
  R42_J9_LANE="$lane" R42_J9_WORK="$work" \
    check_j9 "$t/tree8" deadbeef > "$t/dg.out" 2>&1 && J9_ST_FAIL=1
  st_case dead-ref-green-tally-rejected red

  printf 'selftest cases=%s failures=%s\n' "$cases" "$fails"
  rm -rf -- "$t"
  [ "$fails" -eq 0 ]
}

j9_usage() {
  cat <<'USAGE'
usage: ExecJ9NegCtl.sh --selftest
       ExecJ9NegCtl.sh --tree DIR [--lane DIR] [--work DIR] [--scratch-root DIR]
       ExecJ9NegCtl.sh --replay-fixtures WORK TREE
       ExecJ9NegCtl.sh --help
The file is a sourceable limb: source it and call
  check_j9 <TREE> <REF>
which prints one payload line and returns 0 (closed) or 1 (open).
USAGE
}

# j9_replay_fixtures WORK TREE — the in-family defeat fixtures. Each fixture
# is a stub suite that reproduces one way the negative control could be
# vacuously satisfied; the limb must REJECT every one of them. Prints one
# `replay fixture=<name> rejected=1|0 limb=<field> payload=<...>` line per
# fixture and the summary `replay fixtures=<n> failures=<k>`; returns
# non-zero when any fixture is accepted.
j9_replay_fixtures() { # WORK TREE [LANE]
  local work=$1 tree=$2
  local fails=0 n=0 payload rc name stub lane fx
  mkdir -p -- "$work" || return 1
  lane=${3:-${R42_J9_LANE:-${LANE:-}}}
  [ -n "$lane" ] || lane=$(j9_lane_candidate) || return 1
  [ -d "$lane" ] || { printf 'replay error=lane-absent lane=%s\n' "$lane"; return 1; }
  export R42_J9_LANE="$lane"

  # j9_replay_run NAME STUB EXPECT(red|green) LIMB
  # The stub becomes the tree's suite copy, so the nested control runs
  # execute the fixture's bytes. EXPECT=green means the fixture is the
  # POSITIVE (the limb must ACCEPT it); EXPECT=red means the fixture is a
  # defeat (the limb must REJECT it).
  j9_replay_run() {
    local nm=$1 st=$2 expect=$3 limb=$4
    local p r
    fx=$work/fx-$nm-tree
    rm -rf -- "$fx"
    mkdir -p -- "$fx/corpus/instruments" || return 1
    cp -p -- "$st" "$fx/corpus/instruments/r42-closure.sh"
    p=$(R42_J9_LANE="$lane" R42_J9_WORK="$work" \
          check_j9 "$fx" deadbeef); r=$?
    n=$((n + 1))
    if [ "$expect" = green ]; then
      if [ "$r" -eq 0 ]; then
        printf 'replay fixture=%s accepted=1 limb=%s payload=%s\n' "$nm" "$limb" "$p"
      else
        printf 'replay fixture=%s accepted=0 limb=%s payload=%s\n' "$nm" "$limb" "$p"
        fails=$((fails + 1))
      fi
    else
      if [ "$r" -ne 0 ]; then
        printf 'replay fixture=%s rejected=1 limb=%s payload=%s\n' "$nm" "$limb" "$p"
      else
        printf 'replay fixture=%s rejected=0 limb=%s payload=%s\n' "$nm" "$limb" "$p"
        fails=$((fails + 1))
      fi
    fi
    return 0
  }

  # the honest control is ACCEPTED (this is the positive, not a defeat)
  name=honest-control
  stub=$work/fx-honest.sh
  j9_stub "$stub" '5:red:red' '7:red:red'
  j9_replay_run "$name" "$stub" green honest-control

  # the leaf-capped GREEN base: every other check is green and the tally
  # reaches the ceiling — the round-40 wave-2 M-H8a class
  name=leaf-capped-green-base
  stub=$work/fx-cap.sh
  j9_stub "$stub" '12:green:red' '12:green:red'
  j9_replay_run "$name" "$stub" red base-ceiling

  # a GREEN base (K = 13, every check closed)
  name=green-base
  stub=$work/fx-green.sh
  j9_stub "$stub" '13:green:green' '13:green:green'
  j9_replay_run "$name" "$stub" red base-K

  # a control whose ref did not resolve
  name=unresolvable-control
  stub=$work/fx-rnf.sh
  j9_stub_unresolvable_control "$stub"
  j9_replay_run "$name" "$stub" red base-ref-not-found

  # a summary-only control
  name=summary-only-control
  stub=$work/fx-summary.sh
  printf '#!/usr/bin/env bash\nprintf "closed=5/13 exit=1\\n"\nexit 1\n' > "$stub"
  chmod +x "$stub"
  j9_replay_run "$name" "$stub" red base-lines

  # a mangled tally denominator
  name=mangled-tally
  stub=$work/fx-mangled.sh
  printf '#!/usr/bin/env bash\nfor i in $(seq 1 13); do c=0; case "$i" in J1|J3|J8) c=0 ;; *) c=1 ;; esac; printf "J%%s payload=stub closed=%%s\\n" "$i" "$c"; done\nprintf "closed=13/130 exit=1\\n"\nexit 1\n' > "$stub"
  chmod +x "$stub"
  j9_replay_run "$name" "$stub" red base-tally

  # a lying tally (the numerator does not match the closed=1 lines)
  name=lying-tally
  stub=$work/fx-lying.sh
  printf '#!/usr/bin/env bash\nfor i in $(seq 1 13); do c=0; case "$i" in J1|J3|J8) c=0 ;; *) c=1 ;; esac; printf "J%%s payload=stub closed=%%s\\n" "$i" "$c"; done\nprintf "closed=11/13 exit=1\\n"\nexit 1\n' > "$stub"
  chmod +x "$stub"
  j9_replay_run "$name" "$stub" red base-closed1

  # a dead-ref transcript that prints closed=13/13 is not a distinct red
  name=dead-ref-green-tally
  stub=$work/fx-deadgreen.sh
  j9_stub_variant "$stub" 13 0 green
  j9_replay_run "$name" "$stub" red refnf-mark

  # a control transcript whose PAYLOAD merely MENTIONS `ref-not-found` — the
  # committed r41 receipt's I12 payload carries `ref-not-found=1` inside an
  # ordinary payload — must still be ACCEPTED. A substring search for the
  # token would false-red this control.
  name=payload-mentions-ref-not-found
  stub=$work/fx-mention.sh
  cat > "$stub" <<'STUBM'
#!/usr/bin/env bash
ref=''; prev=''
for a in "$@"; do
  [ "$prev" = '--export-ref' ] && ref=$a
  prev=$a
done
emit_tally() { local i closed ones=0
  for i in $(seq 1 13); do closed=0
    case "$i" in
      9) : ;;
      1|3|8) : ;;
      *) if [ "$ones" -lt "$J9S_K" ]; then closed=1; ones=$((ones + 1)); fi ;;
    esac
    printf 'J%s payload=declared=153,valid=153,census=1,ref-not-found=1,markers=0,neg-red=1 closed=%s\n' "$i" "$closed"; done
  printf 'closed=%s/13 exit=1\n' "$J9S_K"; }
case $ref in
  5053a7f*|1f746461*) export J9S_K=5; emit_tally; exit 1 ;;
  deadbeef*) printf 'suite-ref-status=ref-not-found\n'
              for i in $(seq 1 13); do
                printf 'J%s payload=ref-not-found,ref=%s closed=0\n' "$i" "$ref"
              done
              printf 'closed=0/13 exit=1\n'
              exit 1 ;;
  *) exit 2 ;;
esac
exit 0
STUBM
  chmod +x "$stub"
  j9_replay_run "$name" "$stub" green payload-mentions-ref-not-found

  printf 'replay fixtures=%s failures=%s\n' "$n" "$fails"
  [ "$fails" -eq 0 ] || return 1
  return 0
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  case ${1:-} in
    --selftest) j9_selftest; exit $? ;;
    --replay-fixtures)
      [ $# -ge 3 ] || { printf 'usage: %s --replay-fixtures WORK TREE [LANE]\n' "$0" >&2; exit 64; }
      j9_replay_fixtures "$2" "$3" "${4:-}"; exit $? ;;
    --tree)
      tree=$2; shift 2
      lane=''; work=''; scratch=''
      while [ $# -gt 0 ]; do
        case $1 in
          --lane)         lane=$2; shift 2 ;;
          --work)         work=$2; shift 2 ;;
          --scratch-root) scratch=$2; shift 2 ;;
          *) printf 'unknown argument: %s\n' "$1" >&2; exit 64 ;;
        esac
      done
      [ -n "$lane" ]   && export R42_J9_LANE="$lane"
      [ -n "$work" ]   && export R42_J9_WORK="$work"
      [ -n "$scratch" ] && export R42_J9_SCRATCH="$scratch"
      payload=$(check_j9 "$tree" HEAD); rc=$?
      printf 'J9 payload=%s closed=%s\n' "$payload" "$([ "$rc" -eq 0 ] && echo 1 || echo 0)"
      exit "$rc" ;;
    -h|--help) j9_usage; exit 0 ;;
    *) j9_usage >&2; exit 64 ;;
  esac
fi
