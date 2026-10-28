#!/usr/bin/env bash
# ExecNegCtlReceipt.sh — round-43 K8 receipt-integrity and K9 negative-control
# limb for corpus/instruments/r43-closure.sh.  Sourceable: sourcing this file
# defines functions only; it runs a CLI only when executed directly.
#
# WHAT THIS IS
#   Two limbs of the round-43 closure suite:
#
#     check_k_receipt TREE [REF]   K8 — the receipt is ONE unedited tee of ONE
#                                  run: every recorded `K<n> payload=` value is
#                                  RE-DERIVED at receipt time and compared
#                                  token-for-token against the value this run
#                                  printed; a receipt carrying a value the
#                                  suite did not print is RED.
#     check_k_negctl  TREE [REF]   K9 — the suite is re-invoked recursively over
#                                  the base commit and the round-41 judged head
#                                  and must come back red over each, while the
#                                  driver refuses a plain run (exit 2) and
#                                  reports an unresolvable ref as its own
#                                  `ref-not-found` red (exit 1), never as a
#                                  vacuous `closed=0/19`.
#     make_receipt [--out PATH]    produce the canonical receipt transcript of
#                                  ONE run from the values this run printed.
#
# THE RECEIPT CONTRACT (round 43, sentinel `all-gates v3`)
#   The normative copy of the grammar is
#   .ufo/waves/round-43/w1/ExecNegCtlReceipt.spec.txt.  Shape: 5 header lines,
#   19 payload lines K1..K19, one closed line, 19 graded selftest case lines,
#   one selftest summary line — 2N+7 = 45 lines, each terminated by one LF.
#
# THE SELF-REFERENCE (why the receipt can grade itself)
#   The receipt records the K8 line and the K8 line grades the receipt.  The
#   loop is CLOSED, not trusted: K8's payload is the canonical bundle of the
#   canonical transcript — the transcript this run would write now, built from
#   the freshly re-derived payload values, the freshly re-executed graded
#   selftest lines and the ref-scoped facts.  It never reads the value recorded
#   on the receipt's own K8 line, so the fixed point exists and is reached in
#   one rewrite.
#
# THE EIGHT RECEIPT-CONTENT CLASSES
#   Each class is ONE ABSOLUTE PREDICATE over a named locus of the receipt's
#   own bytes plus independently derived facts.  No predicate compares a count
#   in one artifact with a count in another artifact; no predicate is "the
#   number of mismatches went up".  The loci are disjoint: a receipt carrying
#   one defect raises exactly one class, and the honest control raises none.
#
#     missed-control          a required element is ABSENT (header line, a
#                             payload line, the closed line, a graded case
#                             line, the summary line)
#     composed-of-two-runs    the transcript is not one run: two headers
#                             (`all-gates ...`) or two `run-utc=` lines
#     payload-contradicting   a recorded payload or closed bit contradicts the
#                             value the suite RE-DERIVED for that check, or the
#                             receipt carries a run line for an id the suite
#                             never printed
#     future-dated            `run-utc` is not the committer instant of the ref
#                             on `export-ref=`, or post-dates the verification
#                             clock (now + 120 s)
#     foreign-ref             the named ref resolves but is not BOUND to the
#                             verified tree: the export is not the verified
#                             ref's tree for this file, or the named ref is not
#                             an ancestor of it, or the diff between them lists
#                             a path other than the receipt
#     nonexistent-ref         the named ref does not resolve as a commit
#     summary-only            the closed line declares a tally larger than the
#                             number of payload lines the receipt carries
#     tampered-payload-line   the receipt's own K8 payload is not the canonical
#                             bundle for this run (the self-claim was edited)
#
#   `rejected` means the class WAS detected; `missed` means it was not.  K8 is
#   closed only when every class is missed and the recorded K8 line is the
#   canonical bundle.
#
# TRUTHFUL TEE, NOT GREEN TRANSCRIPT
#   The closed line and the selftest summary are checked for TRUTHFULNESS: the
#   declared tally must equal the number of `closed=1` payload lines the
#   receipt carries, and the declared failure count must equal the number of
#   `verdict=fail` case lines it carries.  A red transcript can still be a
#   faithful tee (the run at J need not be finished), and a green claim the
#   bytes do not support is `summary-only`.  At Y (19/19) these reduce to
#   `closed=19/19 exit=0` and `selftest cases=19 failures=0`.
#
# HOST CONTRACT (what the suite must provide; every hook has a file fallback)
#   TREE / EXPORT        the export root (a `git archive` extraction of one
#                        commit) — passed as the first argument
#   REF_RESOLVED         the resolved verification ref (Y) — second argument
#   LANE                 the lane repo (read-only git reads only)
#   WORK                 work dir holding the seed, hooks and nested runs
#   KNEGCTL_PAYFILE      ID \t payload \t closed   (or PAYFILE)
#   KNEGCTL_SELFTEST_LINES   the N graded selftest case lines
#   payload_get ID       the payload this run printed for ID      (optional hook)
#   payload_closed ID    the closed bit this run computed for ID  (optional hook)
#   selftest_line ID     the graded selftest case line for ID     (optional hook)
#   KNEGCTL_SUITE        the suite file the nested controls re-invoke; when
#                        unset the limb uses the suite it was sourced from
#                        (R43_SELF / SELF), then <TREE>/<SUITE_REL>, then
#                        <LANE>/<SUITE_REL>
#   KNEGCTL_SCRATCH_ROOT the parent for nested work dirs (outside the lane)
#
#   ORDERING.  K8 must run after the other eighteen checks produced their
#   payload values and after the graded selftest produced its nineteen case
#   lines.  K8 grades a receipt against values that exist.
#
#   INVARIANCE.  The other eighteen payload values and the other eighteen
#   graded case lines must be byte-identical between the run at J and the run
#   at Y.  The receipt path must therefore be excluded from every
#   tree-dependent check and from every selftest fixture: it does not exist in
#   the tree at J and does exist in the tree at Y.
#
# CLI (when executed directly)
#   ExecNegCtlReceipt.sh --receipt TREE [REF]
#   ExecNegCtlReceipt.sh --negctl  TREE [REF]
#   ExecNegCtlReceipt.sh --make-receipt [--out PATH]
#   ExecNegCtlReceipt.sh --verify FILE | --flags FILE
#   ExecNegCtlReceipt.sh --fixtures DIR | --battery DIR
#   ExecNegCtlReceipt.sh --help
#
# Every default in this file is overridable from the environment, so the same
# code grades the committed round-42 v2 transcript (J ids, 13 checks, six
# classes' worth of cells) when configured for it: the r43 path is the same
# code with different parameters, never a second implementation.

# ---------------------------------------------------------------------------
# configuration (every value is overridable from the environment)
# ---------------------------------------------------------------------------

KNEGCTL_SENTINEL=${KNEGCTL_SENTINEL:-'all-gates v3'}
KNEGCTL_RECEIPT_REL=${KNEGCTL_RECEIPT_REL:-'.ufo/waves/round-43/final-gates/all-gates.txt'}
KNEGCTL_SUITE_REL=${KNEGCTL_SUITE_REL:-'corpus/instruments/r43-closure.sh'}
KNEGCTL_IDS=${KNEGCTL_IDS:-'K1 K2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13 K14 K15 K16 K17 K18 K19'}
KNEGCTL_SELF_ID=${KNEGCTL_SELF_ID:-'K8'}
KNEGCTL_RECEIPT_ID=${KNEGCTL_RECEIPT_ID:-'K8'}
KNEGCTL_NEGCTL_ID=${KNEGCTL_NEGCTL_ID:-'K9'}
KNEGCTL_BASE=${KNEGCTL_BASE:-'ab98fac9dce87130bc4f66de89e30650d63943dc'}
KNEGCTL_R41=${KNEGCTL_R41:-'1f7464612ac4c44e39886b82e812610d3c039b13'}
# checks whose payload is a function of the exported tree, so a defeat there is
# a real tree red and not a capability artefact of the nested invocation
KNEGCTL_DEPENDENT_IDS=${KNEGCTL_DEPENDENT_IDS:-'K1 K2 K3 K4 K8 K11 K14 K15 K16 K17 K18 K19'}
KNEGCTL_FORGE_DISABLE=${KNEGCTL_FORGE_DISABLE:-}
KNEGCTL_SUITE=${KNEGCTL_SUITE:-}
KNEGCTL_SCRATCH_ROOT=${KNEGCTL_SCRATCH_ROOT:-}
KNEGCTL_PAYFILE=${KNEGCTL_PAYFILE:-${PAYFILE:-}}
KNEGCTL_SELFTEST_LINES=${KNEGCTL_SELFTEST_LINES:-}

KNEGCTL_CLASSES='missed-control composed-of-two-runs payload-contradicting
future-dated foreign-ref nonexistent-ref summary-only tampered-payload-line'
KNEGCTL_TRUTHFUL=${KNEGCTL_TRUTHFUL:-1}

# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

knegctl_ids() { printf '%s\n' $KNEGCTL_IDS; }
knegctl_nids() { local n=0 i; for i in $KNEGCTL_IDS; do n=$((n + 1)); done; printf '%s' "$n"; }
knegctl_non_self_ids() { local i; for i in $KNEGCTL_IDS; do [ "$i" = "$KNEGCTL_SELF_ID" ] || printf '%s\n' "$i"; done; }
knegctl_n_non_self() { local n=0 i; for i in $KNEGCTL_IDS; do [ "$i" = "$KNEGCTL_SELF_ID" ] || n=$((n + 1)); done; printf '%s' "$n"; }
knegctl_nclasses() { local n=0 c; for c in $KNEGCTL_CLASSES; do n=$((n + 1)); done; printf '%s' "$n"; }
knegctl_in_ids() { case " $KNEGCTL_IDS " in *" $1 "*) return 0 ;; esac; return 1; }

knegctl_kv_get() { printf '%s\n' "$1" | tr ',' '\n' | sed -n "s/^$2=//p" | head -n 1; }

knegctl_file_digest() {
  local f=$1
  if [ -z "$f" ] || [ ! -r "$f" ]; then printf 'unreadable'; return 0; fi
  sha256sum -- "$f" | awk '{print $1; exit}'
}

knegctl_ref_utc() { # LANE REF -> ISO Z committer instant
  local e
  [ -n "${2:-}" ] || return 1
  e=$(git -C "$1" log -1 --format=%ct "$2" 2>/dev/null) || return 1
  case $e in ''|*[!0-9]*) return 1 ;; esac
  TZ=UTC date -u -d "@$e" +%Y-%m-%dT%H:%M:%SZ
}

knegctl_iso_past() { # ISO -> 1 when not later than now+120s
  local n
  case $1 in
    [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z) ;;
    *) printf '0'; return 0 ;;
  esac
  n=$(date -u -d "$1" +%s 2>/dev/null) || { printf '0'; return 0; }
  if [ "$n" -le $(( $(date -u +%s) + 120 )) ]; then printf '1'; else printf '0'; fi
}

knegctl_env_export() { printf '%s' "${KNEGCTL_EXPORT:-${EXPORT:-}}"; }
knegctl_env_lane() { printf '%s' "${KNEGCTL_LANE:-${LANE:-}}"; }
knegctl_env_verref() { printf '%s' "${KNEGCTL_VER_REF:-${REF_RESOLVED:-}}"; }
knegctl_env_work() { printf '%s' "${KNEGCTL_WORK:-${WORK:-}}"; }

# knegctl_tokens_equal A B — token-for-token comparison of two comma-joined
# payload strings.  Both are split on ',' into their k=v tokens; the token
# sequences must be byte-identical, in order.  A prefix match, a substring
# match and a superset are all mismatches: the comparison is on the sequence,
# never on a prefix of it.
knegctl_tokens_equal() {
  local a=$1 b=$2 ta tb
  [ "$a" = "$b" ] || return 1
  ta=$(printf '%s\n' "$a" | tr ',' '\n')
  tb=$(printf '%s\n' "$b" | tr ',' '\n')
  [ "$ta" = "$tb" ]
}

# ---------------------------------------------------------------------------
# the host hooks (with file fallbacks)
# ---------------------------------------------------------------------------

knegctl_payload_get() { # ID
  if declare -F payload_get >/dev/null 2>&1; then payload_get "$1"; return 0; fi
  local t=${KNEGCTL_PAYFILE:-${PAYFILE:-}} w
  if [ -n "$t" ] && [ -f "$t" ]; then
    awk -F'\t' -v id="$1" '$1 == id { print $2; exit }' "$t"
    return 0
  fi
  w=$(knegctl_env_work)
  if [ -n "$w" ] && [ -f "$w/payloads.txt" ]; then
    sed -n "s/^$1 payload=\(.*\) closed=[01]\$/\1/p" -- "$w/payloads.txt" | head -n 1
  fi
}

knegctl_payload_closed() { # ID -> 0|1
  if declare -F payload_closed >/dev/null 2>&1; then payload_closed "$1"; return 0; fi
  local t=${KNEGCTL_PAYFILE:-${PAYFILE:-}} w c
  if [ -n "$t" ] && [ -f "$t" ]; then
    c=$(awk -F'\t' -v id="$1" '$1 == id { print $3; exit }' "$t")
    case $c in 0|1) printf '%s' "$c"; return 0 ;; esac
  fi
  w=$(knegctl_env_work)
  if [ -n "$w" ] && [ -f "$w/payloads.txt" ]; then
    c=$(sed -n "s/^$1 payload=.* closed=\([01]\)\$/\1/p" -- "$w/payloads.txt" | head -n 1)
    case $c in 0|1) printf '%s' "$c"; return 0 ;; esac
  fi
  printf '1'
}

knegctl_selftest_line() { # ID
  if declare -F selftest_line >/dev/null 2>&1; then selftest_line "$1"; return 0; fi
  local w f
  w=$(knegctl_env_work)
  if [ -n "$w" ] && [ -f "$w/sel-$1.line" ]; then cat -- "$w/sel-$1.line"; return 0; fi
  for f in "${KNEGCTL_SELFTEST_LINES:-}" ${w:+"$w/selftest-lines.txt"} ${w:+"$w/selftest-block.txt"}; do
    if [ -n "$f" ] && [ -f "$f" ]; then
      grep -m1 "^selftest case=$1 " "$f" 2>/dev/null && return 0
    fi
  done
  return 0
}

# ---------------------------------------------------------------------------
# the receipt under test, the ref it names, and the verified tree
# ---------------------------------------------------------------------------

knegctl_source_receipt() { # -> the committed receipt inside the export, or ''
  local exp_root; exp_root=$(knegctl_env_export)
  if [ -n "$exp_root" ] && [ -f "$exp_root/$KNEGCTL_RECEIPT_REL" ]; then
    printf '%s' "$exp_root/$KNEGCTL_RECEIPT_REL"
    return 0
  fi
  printf ''
}

knegctl_named_ref() { # [FILE] -> the ref the receipt names
  local f=${1:-} href
  if [ -n "$f" ] && [ -f "$f" ]; then
    href=$(sed -n 's/^export-ref=//p' -- "$f" 2>/dev/null | head -n 1)
    case $href in
      [0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]*) printf '%s' "$href"; return 0 ;;
    esac
  fi
  printf '%s' "$(knegctl_env_verref)"
}

knegctl_seed_path() {
  local w; w=$(knegctl_env_work)
  printf '%s' "${w:-${TMPDIR:-/tmp}}/knegctl-seed.txt"
}

KNEGCTL_IN_TARGET=0
knegctl_receipt_target() { # TREE
  if [ -n "${KNEGCTL_RECEIPT_FILE:-}" ]; then printf '%s' "$KNEGCTL_RECEIPT_FILE"; return 0; fi
  local tree=${1:-} exp="$1/$KNEGCTL_RECEIPT_REL"
  if [ -n "$tree" ] && [ -f "$exp" ]; then printf '%s' "$exp"; return 0; fi
  # the export carries no receipt (the run at the judged head J): the seed is
  # the byte-identical twin of the receipt this run is about to write
  if [ "$KNEGCTL_IN_TARGET" = 0 ]; then
    KNEGCTL_IN_TARGET=1
    knegctl_seed >/dev/null 2>&1
    KNEGCTL_IN_TARGET=0
  fi
  printf '%s' "$(knegctl_seed_path)"
}

# knegctl_tree_bind EXPORT VER — 1 when the export IS the verified ref's tree
# with respect to the receipt: the export carries the receipt iff that ref's
# tree carries it, and when both carry it the bytes are the same blob.
knegctl_tree_bind() {
  local exp=${1:-} ver=${2:-} lane exp_r ver_blob file_blob
  [ -n "$exp" ] || exp=$(knegctl_env_export)
  [ -n "$ver" ] || ver=$(knegctl_env_verref)
  lane=$(knegctl_env_lane)
  [ -n "$lane" ] && [ -n "$ver" ] || { printf '0'; return 0; }
  exp_r=''
  [ -f "$exp/$KNEGCTL_RECEIPT_REL" ] && exp_r="$exp/$KNEGCTL_RECEIPT_REL"
  if ver_blob=$(git --no-optional-locks -C "$lane" rev-parse "${ver}:${KNEGCTL_RECEIPT_REL}" 2>/dev/null); then
    [ -n "$exp_r" ] || { printf '0'; return 0; }
    file_blob=$(git --no-optional-locks -C "$lane" hash-object -- "$exp_r" 2>/dev/null)
    [ -n "$file_blob" ] && [ "$file_blob" = "$ver_blob" ] && { printf '1'; return 0; }
    printf '0'; return 0
  fi
  [ -n "$exp_r" ] && { printf '0'; return 0; }
  printf '1'
}

# ---------------------------------------------------------------------------
# layer 1: the facts of a receipt (never reads the receipt's own K8 payload)
# ---------------------------------------------------------------------------

# knegctl_facts FILE — the fact bundle of FILE.  It describes the header, the
# body, the graded selftest block and the agreement between what the receipt
# RECORDS and what the suite RE-DERIVED.  It never reads the value recorded on
# FILE's own self line and never counts the self id's selftest case line, so
# the bundle is invariant under the self-claim rewrite and the fixed point
# exists.  Side effect: KNEGCTL_PM_MATCH / KNEGCTL_PM_TOTAL.
knegctl_facts() { # FILE
  local f=$1
  local lane ver exp_root refhex='' want='' utcval='' n m exp_lines
  local sent=0 refc=0 refok=0 dig=0 tb=0 utc=0 notf=0 anc=0 dclean=1 dread=ok bind=0
  local shape=0 hdr=0 runl=1 sell=1 selv=1 summ=0 cll=0 nostray=1 pm=0
  local i id line rec recl wantc selflines=0 fails=0 closedn=0
  local sm=0
  local good total pos pmm verdict

  KNEGCTL_PM_TOTAL=$(knegctl_n_non_self)
  n=$(knegctl_nids); m=$KNEGCTL_PM_TOTAL
  exp_lines=$((2 * n + 7))

  if [ ! -f "$f" ]; then
    printf 'sentinel=0,lines=0,ref=0,digest=0,time-basis=0,utc=0,not-future=0,ancestor=0,diff-clean=0,diff-read=%s,tree-bind=0,run-lines=0,selftest-lines=0,verdicts=0,summary=0,closed-line=0,no-stray=0,payload-match=0' "$dread"
    return 0
  fi

  exp_root=$(knegctl_env_export); lane=$(knegctl_env_lane); ver=$(knegctl_env_verref)

  # --- shape: exact line count, LF only, no CR, one trailing LF ---
  mapfile -t KNEGCTL_L < "$f"
  local nl=${#KNEGCTL_L[@]} rawnl lastb
  rawnl=$(wc -l < "$f" 2>/dev/null || printf '0')
  lastb=$(tail -c 1 -- "$f" 2>/dev/null | od -An -tu1 2>/dev/null | tr -d ' \n')
  if [ "$nl" = "$exp_lines" ] && [ "${rawnl// /}" = "$exp_lines" ] && [ "$lastb" = 10 ] \
     && ! LC_ALL=C grep -q $'\r' -- "$f"; then shape=1; fi

  # --- header (positional) ---
  [ "${KNEGCTL_L[0]:-}" = "$KNEGCTL_SENTINEL" ] && sent=1
  if [[ "${KNEGCTL_L[1]:-}" =~ ^export-ref=([0-9a-f]{40})$ ]]; then
    refhex=${BASH_REMATCH[1]}; refc=1
    [ -n "$lane" ] && git -C "$lane" cat-file -e "${refhex}^{commit}" 2>/dev/null && refok=1
  fi
  if [[ "${KNEGCTL_L[2]:-}" =~ ^suite-sha256=([0-9a-f]{64})$ ]]; then
    [ "${BASH_REMATCH[1]}" = "$(knegctl_file_digest "$exp_root/$KNEGCTL_SUITE_REL")" ] && dig=1
  fi
  [ "${KNEGCTL_L[3]:-}" = 'time-basis=ref-commit' ] && tb=1
  if [[ "${KNEGCTL_L[4]:-}" =~ ^run-utc=([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)$ ]]; then
    utcval=${BASH_REMATCH[1]}
    [ "$(knegctl_iso_past "$utcval")" = 1 ] && notf=1
    if [ -n "$refhex" ]; then
      want=$(knegctl_ref_utc "$lane" "$refhex")
      [ -n "$want" ] && [ "$want" = "$utcval" ] && utc=1
    fi
  fi

  # --- body (positional): n payload lines, one closed line ---
  local idx=5
  for id in $(knegctl_ids); do
    line=${KNEGCTL_L[$idx]:-}
    if [[ "$line" =~ ^${id}\ payload=(.*)\ closed=([01])$ ]]; then
      :
    else
      runl=0; nostray=0
    fi
    idx=$((idx + 1))
  done
  line=${KNEGCTL_L[$idx]:-}
  if [[ "$line" =~ ^closed=([0-9]+)/([0-9]+)\ exit=([01])$ ]]; then
    if [ "${BASH_REMATCH[2]}" != "$n" ]; then cll=0; nostray=0; else cll=1; fi
  else
    nostray=0
  fi
  idx=$((idx + 1))

  # --- graded selftest block (positional) ---
  for id in $(knegctl_ids); do
    line=${KNEGCTL_L[$idx]:-}
    if [[ "$line" =~ ^selftest\ case=${id}\ mutants=([0-9]+)/([0-9]+)\ positive=(pass|fail)\ payload-match=([01])\ verdict=(pass|fail)$ ]]; then
      good=${BASH_REMATCH[1]}; total=${BASH_REMATCH[2]}; pos=${BASH_REMATCH[3]}
      pmm=${BASH_REMATCH[4]}; verdict=${BASH_REMATCH[5]}
      [ "$id" = "$KNEGCTL_SELF_ID" ] || selflines=$((selflines + 1))
      [ "$verdict" = fail ] && fails=$((fails + 1))
      if [ "$id" != "$KNEGCTL_SELF_ID" ]; then
        local fresh; fresh=$(knegctl_selftest_line "$id")
        [ -n "$fresh" ] && [ "$fresh" = "$line" ] && sm=$((sm + 1))
      fi
      # truthful verdict: pass only when the case's own fields support it
      local consistent=1
      if [ "$pos" = pass ] && [ "$pmm" = 1 ] \
         && { [ "$total" = 0 ] || [ "$good" = "$total" ]; }; then
        consistent=0
      fi
      if [ "$KNEGCTL_TRUTHFUL" = 1 ]; then
        if [ "$verdict" = pass ] && [ "$consistent" != 0 ]; then selv=0; fi
        if [ "$verdict" = fail ] && [ "$consistent" = 0 ]; then selv=0; fi
      fi
    else
      sell=0; nostray=0
    fi
    idx=$((idx + 1))
  done
  line=${KNEGCTL_L[$idx]:-}
  if [[ "$line" =~ ^selftest\ cases=([0-9]+)\ failures=([0-9]+)$ ]]; then
    if [ "${BASH_REMATCH[1]}" != "$n" ]; then summ=0; nostray=0; else summ=1; fi
    [ "${BASH_REMATCH[2]}" = "$fails" ] || summ=0
  else
    nostray=0
  fi

  # --- truthful closed tally: declares what the payload lines carry ---
  closedn=$(grep -cE "^($(printf '%s|' $KNEGCTL_IDS | sed 's/|$//')) payload=.* closed=1$" -- "$f" 2>/dev/null || true)
  closedn=${closedn:-0}
  if [ "$cll" = 1 ]; then
    line=${KNEGCTL_L[$((5 + n))]:-}
    if [[ "$line" =~ ^closed=([0-9]+)/([0-9]+)\ exit=([01])$ ]]; then
      local declared=${BASH_REMATCH[1]} denom=${BASH_REMATCH[2]} exitd=${BASH_REMATCH[3]}
      [ "$denom" = "$n" ] || cll=0
      [ "$declared" = "$closedn" ] || cll=0
      if [ "$declared" = "$denom" ]; then [ "$exitd" = 0 ] || cll=0; else [ "$exitd" = 1 ] || cll=0; fi
    else
      cll=0
    fi
  fi

  # --- agreement between what is RECORDED and what is RE-DERIVED ---
  for id in $(knegctl_non_self_ids); do
    rec=$(sed -n "s/^$id payload=\(.*\) closed=[01]\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
    recl=$(sed -n "s/^$id payload=.* closed=\([01]\)\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
    want=$(knegctl_payload_get "$id")
    wantc=$(knegctl_payload_closed "$id")
    if [ -n "$want" ] && knegctl_tokens_equal "$rec" "$want" && [ "$recl" = "$wantc" ]; then
      pm=$((pm + 1))
    fi
  done

  # --- the ref facts: ancestor, diff, tree-bind ---
  if [ -n "$refhex" ] && [ -n "$lane" ] && [ -n "$ver" ] && [ "$refok" = 1 ]; then
    git --no-optional-locks -C "$lane" merge-base --is-ancestor "$refhex" "$ver" 2>/dev/null && anc=1
    local name x
    if name=$(git --no-optional-locks -C "$lane" diff --name-only "$refhex" "$ver" 2>/dev/null); then
      while IFS= read -r x; do
        [ -n "$x" ] || continue
        [ "$x" = "$KNEGCTL_RECEIPT_REL" ] || dclean=0
      done <<< "$name"
    else
      dread=fail; dclean=0
    fi
  else
    anc=0; dclean=0
  fi
  bind=$(knegctl_tree_bind "$exp_root" "$ver")

  # header completeness is positional: all five lines matched their pattern
  local hcount=0
  [ "$sent" = 1 ] && hcount=$((hcount + 1))
  [ "$refc" = 1 ] && hcount=$((hcount + 1))
  [[ "${KNEGCTL_L[2]:-}" =~ ^suite-sha256=[0-9a-f]{64}$ ]] && hcount=$((hcount + 1))
  [ "$tb" = 1 ] && hcount=$((hcount + 1))
  [[ "${KNEGCTL_L[4]:-}" =~ ^run-utc=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]] && hcount=$((hcount + 1))
  [ "$hcount" = 5 ] && hdr=1
  [ "$shape" = 1 ] || nostray=0
  [ "$runl" = 1 ] && [ "$sell" = 1 ] || nostray=0

  local pmflag=0 smflag=0
  [ "$pm" = "$m" ] && pmflag=1
  [ "$sm" = "$m" ] && smflag=1
  printf 'sentinel=%s,lines=%s,ref=%s,digest=%s,time-basis=%s,utc=%s,not-future=%s,ancestor=%s,diff-clean=%s,diff-read=%s,tree-bind=%s,header-lines=%s,run-lines=%s,selftest-lines=%s,verdicts=%s,summary=%s,closed-line=%s,no-stray=%s,payload-match=%s,selftest-match=%s' \
    "$sent" "$shape" "$refok" "$dig" "$tb" "$utc" "$notf" "$anc" "$dclean" "$dread" "$bind" \
    "$hdr" "$runl" "$sell" "$selv" "$summ" "$cll" "$nostray" "$pmflag" "$smflag"
}

# ---------------------------------------------------------------------------
# layer 2: the eight receipt-content classes
# ---------------------------------------------------------------------------

# knegctl_flags FILE [skip-self] — one independent verdict per class.
# `rejected` means the class WAS detected in this receipt; `missed` means it
# was not.  `skip-self` omits the self-claim class (used by the control).
knegctl_flags() { # FILE [skip-self]
  local f=$1 skipself=${2:-}
  local missed=missed comp=missed payload=missed future=missed foreign=missed
  local nonexistent=missed summary=missed tampered=missed
  local lane ver refhex utc n i id line

  if [ ! -f "$f" ]; then
    printf 'missed-control=rejected,composed-of-two-runs=rejected,payload-contradicting=rejected,future-dated=rejected,foreign-ref=rejected,nonexistent-ref=rejected,summary-only=rejected,tampered-payload-line=rejected'
    return 0
  fi

  lane=$(knegctl_env_lane); ver=$(knegctl_env_verref); n=$(knegctl_nids)

  # --- missed-control: a required control ELEMENT is ABSENT (count 0).
  #     Duplication is the composition locus below, never this one. ---
  local absent=0
  [ "$(grep -cxF -- "$KNEGCTL_SENTINEL" "$f" 2>/dev/null || true)" = 0 ] && absent=1
  [ "$(grep -cE '^export-ref=[0-9a-f]{40}$' -- "$f" 2>/dev/null || true)" = 0 ] && absent=1
  [ "$(grep -cE '^suite-sha256=[0-9a-f]{64}$' -- "$f" 2>/dev/null || true)" = 0 ] && absent=1
  [ "$(grep -cxF 'time-basis=ref-commit' -- "$f" 2>/dev/null || true)" = 0 ] && absent=1
  [ "$(grep -cE '^run-utc=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$' -- "$f" 2>/dev/null || true)" = 0 ] && absent=1
  [ "$(grep -cE '^closed=[0-9]+/[0-9]+ exit=[01]$' -- "$f" 2>/dev/null || true)" = 0 ] && absent=1
  [ "$(grep -cE '^selftest cases=[0-9]+ failures=[0-9]+$' -- "$f" 2>/dev/null || true)" = 0 ] && absent=1
  for id in $(knegctl_ids); do
    [ "$(grep -cE "^$id payload=.* closed=[01]$" -- "$f" 2>/dev/null || true)" = 0 ] && absent=1
    [ "$(grep -cE "^selftest case=$id .* verdict=(pass|fail)$" -- "$f" 2>/dev/null || true)" = 0 ] && absent=1
  done
  [ "$absent" = 0 ] || missed=rejected

  # --- composed-of-two-runs: two heads or two run instants ---
  local heads stamps
  heads=$(grep -cE '^all-gates v[0-9]+$' -- "$f" 2>/dev/null || true)
  stamps=$(grep -cE '^run-utc=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$' -- "$f" 2>/dev/null || true)
  heads=${heads:-0}; stamps=${stamps:-0}
  { [ "$heads" -gt 1 ] || [ "$stamps" -gt 1 ]; } && comp=rejected

  # --- payload-contradicting: a recorded payload/closed contradicts the
  #     re-derived value, or the receipt carries an id the suite never printed
  local lid rec want recl wantc
  while IFS= read -r lid; do
    [ -n "$lid" ] || continue
    [ "$lid" = "$KNEGCTL_SELF_ID" ] && continue
    rec=$(sed -n "s/^$lid payload=\(.*\) closed=[01]\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
    recl=$(sed -n "s/^$lid payload=.* closed=\([01]\)\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
    if knegctl_in_ids "$lid"; then
      want=$(knegctl_payload_get "$lid")
      wantc=$(knegctl_payload_closed "$lid")
      { [ -n "$want" ] && knegctl_tokens_equal "$rec" "$want" && [ "$recl" = "$wantc" ]; } \
        || payload=rejected
    else
      payload=rejected
    fi
    [ "$payload" = rejected ] && break
  done <<< "$(sed -n 's/^\([A-Za-z][A-Za-z0-9]*\) payload=.* closed=[01]$/\1/p' -- "$f" 2>/dev/null)"

  # --- future-dated: run-utc is not the named ref's committer instant, or it
  #     post-dates the verification clock ---
  refhex=$(sed -n 's/^export-ref=//p' -- "$f" 2>/dev/null | head -n 1)
  utc=$(sed -n 's/^run-utc=//p' -- "$f" 2>/dev/null | head -n 1)
  if [ -n "$utc" ]; then
    local e; e=$(date -u -d "$utc" +%s 2>/dev/null || echo '')
    [ -n "$e" ] && [ "$e" -gt $(( $(date -u +%s) + 120 )) ] && future=rejected
    if [ "$future" = missed ] && [ -n "$refhex" ] && [ -n "$lane" ] \
       && git -C "$lane" cat-file -e "${refhex}^{commit}" 2>/dev/null; then
      local rinst re
      rinst=$(knegctl_ref_utc "$lane" "$refhex")
      if [ -n "$rinst" ]; then
        re=$(date -u -d "$rinst" +%s 2>/dev/null || echo '')
        [ -n "$re" ] && [ "$e" -ne "$re" ] && future=rejected
      fi
    fi
  fi

  # --- foreign-ref / nonexistent-ref: existence and binding of the named ref ---
  if [ -z "$refhex" ] || [ -z "$lane" ] \
     || ! git -C "$lane" cat-file -e "${refhex}^{commit}" 2>/dev/null; then
    nonexistent=rejected
  else
    if [ "$(knegctl_tree_bind "$(knegctl_env_export)" "$ver")" != 1 ]; then
      foreign=rejected
    elif [ -n "$ver" ]; then
      if ! git --no-optional-locks -C "$lane" merge-base --is-ancestor "$refhex" "$ver" 2>/dev/null; then
        foreign=rejected
      else
        local name x bad=0
        if name=$(git --no-optional-locks -C "$lane" diff --name-only "$refhex" "$ver" 2>/dev/null); then
          while IFS= read -r x; do
            [ -n "$x" ] || continue
            [ "$x" = "$KNEGCTL_RECEIPT_REL" ] || bad=1
          done <<< "$name"
          [ "$bad" = 0 ] || foreign=rejected
        else
          foreign=rejected
        fi
      fi
    fi
  fi

  # --- summary-only: the closed line claims a tally it does not carry ---
  local declared runl
  declared=$(sed -n 's/^closed=\([0-9][0-9]*\)\/[0-9][0-9]* exit=[01]$/\1/p' -- "$f" 2>/dev/null | head -n 1)
  runl=$(grep -cE "^($(printf '%s|' $KNEGCTL_IDS | sed 's/|$//')) payload=.* closed=[01]$" -- "$f" 2>/dev/null || true)
  case $declared in ''|*[!0-9]*) summary=rejected ;; *)
    case ${runl:-} in ''|*[!0-9]*) summary=rejected ;; *)
      [ "${runl:-0}" -lt "$declared" ] && summary=rejected ;;
    esac ;;
  esac

  # --- tampered-payload-line: the receipt's own K8 line is not the canonical
  #     bundle for this run (computed without reading that line) ---
  if [ "$skipself" != skip-self ]; then
    local rec_self canonical
    rec_self=$(sed -n "s/^$KNEGCTL_SELF_ID payload=\(.*\) closed=[01]\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
    canonical=$(knegctl_canonical_bundle)
    [ "$rec_self" = "$canonical" ] || tampered=rejected
  fi

  case "${KNEGCTL_FORGE_DISABLE:-}" in
    missed-control) missed=missed ;;
    composed-of-two-runs) comp=missed ;;
    payload-contradicting) payload=missed ;;
    future-dated) future=missed ;;
    foreign-ref) foreign=missed ;;
    nonexistent-ref) nonexistent=missed ;;
    summary-only) summary=missed ;;
    tampered-payload-line) tampered=missed ;;
  esac

  printf 'missed-control=%s,composed-of-two-runs=%s,payload-contradicting=%s,future-dated=%s,foreign-ref=%s,nonexistent-ref=%s,summary-only=%s,tampered-payload-line=%s' \
    "$missed" "$comp" "$payload" "$future" "$foreign" "$nonexistent" "$summary" "$tampered"
}

# knegctl_flags_all_missed FLAGS — 1 when every class is `missed`.
knegctl_flags_all_missed() {
  case $1 in
    *=rejected*) printf '0' ;;
    *) printf '1' ;;
  esac
}

# knegctl_flags_missed_count FLAGS — how many classes the receipt raises.
knegctl_flags_missed_count() {
  local n=0 c v
  for c in $KNEGCTL_CLASSES; do
    v=$(knegctl_cls_get "$1" "$c")
    [ "$v" = missed ] && n=$((n + 1))
  done
  printf '%s' "$n"
}

# knegctl_cls_get FLAGS CLASS
knegctl_cls_get() { printf '%s\n' "$1" | tr ',' '\n' | sed -n "s/^$2=//p" | head -n 1; }

# ---------------------------------------------------------------------------
# layer 3: transcript assembly and the canonical bundle
# ---------------------------------------------------------------------------

# knegctl_assemble OUT [SOURCE] — write the canonical receipt transcript of
# THIS run.  SOURCE is the receipt whose export-ref line the new transcript
# adopts (the committed receipt at Y); without it the ref under verification is
# used.  The self line is written PENDING and then rewritten with the canonical
# bundle, so the fixed point is reached in one rewrite.
knegctl_assemble() { # OUT [SOURCE]
  local out=$1 source=${2:-}
  local exp_root lane href sha utc id n k=0 line tmp bundle selfclosed=1
  exp_root=$(knegctl_env_export); lane=$(knegctl_env_lane)
  href=$(knegctl_named_ref "$source")
  sha=$(knegctl_file_digest "$exp_root/$KNEGCTL_SUITE_REL")
  utc=$(knegctl_ref_utc "$lane" "$href"); [ -n "$utc" ] || utc=unreadable
  n=$(knegctl_nids)
  for id in $(knegctl_non_self_ids); do
    [ "$(knegctl_payload_closed "$id")" = 1 ] || selfclosed=0
  done
  {
    printf '%s\n' "$KNEGCTL_SENTINEL"
    printf 'export-ref=%s\n' "$href"
    printf 'suite-sha256=%s\n' "$sha"
    printf 'time-basis=ref-commit\n'
    printf 'run-utc=%s\n' "$utc"
    for id in $(knegctl_ids); do
      if [ "$id" = "$KNEGCTL_SELF_ID" ]; then
        printf '%s payload=PENDING closed=%s\n' "$id" "$selfclosed"
        continue
      fi
      printf '%s payload=%s closed=%s\n' "$id" "$(knegctl_payload_get "$id")" "$(knegctl_payload_closed "$id")"
    done
    for id in $(knegctl_non_self_ids); do
      [ "$(knegctl_payload_closed "$id")" = 1 ] && k=$((k + 1))
    done
    k=$((k + selfclosed))
    printf 'closed=%s/%s exit=%s\n' "$k" "$n" "$([ "$k" = "$n" ] && printf 0 || printf 1)"
    for id in $(knegctl_ids); do
      line=$(knegctl_selftest_line "$id")
      if [ -z "$line" ]; then
        line="selftest case=$id mutants=0/0 positive=pending payload-match=0 verdict=pending"
      fi
      printf '%s\n' "$line"
    done
    printf 'selftest cases=%s failures=0\n' "$n"
  } > "$out" || return 2
  # the summary failure count must be truthful for the lines just written
  local fails
  fails=$(grep -cE '^selftest case=.* verdict=fail$' -- "$out" 2>/dev/null || true)
  fails=${fails:-0}
  tmp="$out.tmp.$$"
  awk -v n="$n" -v f="$fails" \
    '$0 ~ ("^selftest cases=" n " failures=") { print "selftest cases=" n " failures=" f; next } { print }' \
    "$out" > "$tmp" && mv -- "$tmp" "$out"
  # close the self-reference: the self payload is the canonical bundle and the
  # self closed bit is the verdict that bundle earns (a faithful tee is closed
  # even when the run around it is red)
  bundle=$(knegctl_canonical_bundle "$out")
  selfclosed=$(knegctl_bundle_clean "$bundle")
  # recompute the truthful tally now that the self bit is known
  k=0
  for id in $(knegctl_non_self_ids); do
    [ "$(knegctl_payload_closed "$id")" = 1 ] && k=$((k + 1))
  done
  k=$((k + selfclosed))
  tmp="$out.tmp.$$"
  awk -v self="$KNEGCTL_SELF_ID" -v pay="$bundle" -v closed="$selfclosed" \
      -v n="$n" -v k="$k" -v exitb="$([ "$k" = "$n" ] && printf 0 || printf 1)" \
    '$0 ~ ("^" self " payload=") { print self " payload=" pay " closed=" closed; next }
     $0 ~ "^closed=" { print "closed=" k "/" n " exit=" exitb; next }
     { print }' \
    "$out" > "$tmp" && mv -- "$tmp" "$out"
  return 0
}

# knegctl_bundle_clean BUNDLE — 1 when the canonical bundle carries no open
# fact and no detected class: the receipt it describes is a faithful tee.
knegctl_bundle_clean() { # BUNDLE
  local b=$1
  case ",$b," in *,*=0,*) printf '0'; return 0 ;; esac
  case $b in
    *'diff-read=fail'*) printf '0'; return 0 ;;
    *'payload-match=0/'*) printf '0'; return 0 ;;
    *'selftest-match=0/'*) printf '0'; return 0 ;;
    *'forged=0/'*) printf '0'; return 0 ;;
  esac
  printf '1'
}

# knegctl_canonical_bundle [FILE] — the canonical self payload of THIS run.
# Without FILE the seed is (re)built.  It is computed from the transcript
# WITHOUT reading the recorded self line, so the self-reference is closed.
knegctl_canonical_bundle() { # [FILE]
  local f=${1:-}
  if [ -z "$f" ]; then
    knegctl_seed >/dev/null 2>&1 || return 1
    f=$(knegctl_seed_path)
  fi
  local facts flags pm pmn pmrest pms pmt
  facts=$(knegctl_facts "$f")
  flags=$(knegctl_flags "$f" skip-self)
  pm=$(knegctl_pm "$f")
  pmn=${pm%%	*}; pmrest=${pm#*	}; pms=${pmrest%%	*}; pmt=${pmrest##*	}
  # `receipt=<rel>` is a constant (the path the receipt occupies); there is no
  # `source=` cell, because that label flips from canonical to committed the
  # moment the receipt lands and would make the J-minted receipt fail its own
  # self-claim at Y (the r41 bootstrap defect).
  printf 'receipt=%s,%s,payload-match=%s/%s,selftest-match=%s/%s,forged=%s/%s' \
    "$KNEGCTL_RECEIPT_REL" "$facts" \
    "$pmn" "$pmt" "$pms" "$pmt" "$(knegctl_flags_missed_count "$flags")" "$(knegctl_nclasses)"
}

# knegctl_pm FILE — "match<TAB>total": how many OTHER payload values the
# receipt records equal the values this run re-derived.
knegctl_pm() { # FILE -> "payload-match<TAB>selftest-match<TAB>total"
  local id rec want recl wantc pm=0 sm=0 fresh line m
  m=$(knegctl_n_non_self)
  for id in $(knegctl_non_self_ids); do
    rec=$(sed -n "s/^$id payload=\(.*\) closed=[01]\$/\1/p" -- "$1" 2>/dev/null | head -n 1)
    recl=$(sed -n "s/^$id payload=.* closed=\([01]\)\$/\1/p" -- "$1" 2>/dev/null | head -n 1)
    want=$(knegctl_payload_get "$id")
    wantc=$(knegctl_payload_closed "$id")
    if [ -n "$want" ] && knegctl_tokens_equal "$rec" "$want" && [ "$recl" = "$wantc" ]; then
      pm=$((pm + 1))
    fi
    line=$(grep -m1 "^selftest case=$id " -- "$1" 2>/dev/null || true)
    fresh=$(knegctl_selftest_line "$id")
    [ -n "$fresh" ] && [ "$fresh" = "$line" ] && sm=$((sm + 1))
  done
  printf '%s\t%s\t%s' "$pm" "$sm" "$m"
}

knegctl_receipt_label() {
  local f; f=$(knegctl_source_receipt)
  if [ -n "$f" ]; then printf '%s' "$KNEGCTL_RECEIPT_REL"; else printf '(canonical)'; fi
}
# knegctl_seed — (re)write the seed: the byte-identical twin of the receipt
# this run is about to write, so the J run and the Y run grade the same bytes.
knegctl_seed() {
  local work; work=$(knegctl_env_work)
  [ -n "$work" ] || return 2
  mkdir -p -- "$work" 2>/dev/null || return 2
  knegctl_assemble "$(knegctl_seed_path)" "$(knegctl_source_receipt)" || return 2
  return 0
}

# ---------------------------------------------------------------------------
# layer 4: the grade and the two check entry points
# ---------------------------------------------------------------------------

# knegctl_verify FILE — grade one receipt.  Prints the canonical K8 payload on
# stdout; exit 0 when the receipt is the canonical tee of this run, 1 when red.
knegctl_verify() { # FILE
  local f=$1
  local canonical rec_self rec_closed flags facts cfacts selfclosed
  canonical=$(knegctl_canonical_bundle)
  selfclosed=$(knegctl_bundle_clean "$canonical")
  rec_self=$(sed -n "s/^$KNEGCTL_SELF_ID payload=\(.*\) closed=[01]\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
  rec_closed=$(sed -n "s/^$KNEGCTL_SELF_ID payload=.* closed=\([01]\)\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
  flags=$(knegctl_flags "$f")
  facts=$(knegctl_facts "$f")
  cfacts=$(knegctl_facts "$(knegctl_seed_path)")
  printf '%s' "$canonical"
  case $flags in
    *=rejected*) return 1 ;;
  esac
  [ "$rec_self" = "$canonical" ] && [ "$rec_closed" = "$selfclosed" ] && [ "$facts" = "$cfacts" ] || return 1
  return 0
}

# check_k_receipt TREE [REF] — the K8 entry point.
check_k_receipt() { # TREE [REF]
  local tree=$1 ref=${2:-}
  KNEGCTL_EXPORT=$tree
  [ -n "$ref" ] && KNEGCTL_VER_REF=$ref
  export KNEGCTL_EXPORT KNEGCTL_VER_REF
  local f; f=$(knegctl_receipt_target "$tree")
  local payload rc
  payload=$(knegctl_verify "$f"); rc=$?
  printf '%s payload=%s closed=%d\n' "$KNEGCTL_RECEIPT_ID" "$payload" "$([ "$rc" = 0 ] && printf 1 || printf 0)"
  return $rc
}

# ---------------------------------------------------------------------------
# the producer
# ---------------------------------------------------------------------------

# make_receipt [--out PATH] — write the canonical receipt transcript of this
# run.  The transcript adopts the export-ref of the receipt already in the
# export (the committed receipt at Y), so the bytes written at J and the bytes
# read at Y are the same bytes.
make_receipt() {
  local out=''
  while [ $# -gt 0 ]; do
    case $1 in
      --out) out=${2:-}; shift 2 ;;
      *) shift ;;
    esac
  done
  [ -n "$out" ] || out=/dev/stdout
  local work draft
  work=$(knegctl_env_work)
  if [ -z "$work" ]; then
    draft=$(mktemp -t knegctl-receipt.XXXXXXXX) || return 2
  else
    mkdir -p -- "$work" || return 2
    draft="$work/knegctl-draft.txt"
  fi
  local source; source=$(knegctl_source_receipt)
  knegctl_assemble "$draft" "$source" || return 2
  mkdir -p -- "$(dirname -- "$out")" 2>/dev/null || true
  cat -- "$draft" > "$out" || return 2
  [ "$out" = /dev/stdout ] || rm -f -- "$draft"
  return 0
}

# ---------------------------------------------------------------------------
# K9 — the negative controls
# ---------------------------------------------------------------------------

knegctl_suite() { # TREE -> the suite file the controls re-invoke
  local tree=${1:-} c
  if [ -n "$KNEGCTL_SUITE" ] && [ -f "$KNEGCTL_SUITE" ]; then printf '%s' "$KNEGCTL_SUITE"; return 0; fi
  for c in "${R43_SELF:-}" "${SELF:-}"; do
    [ -n "$c" ] && [ -f "$c" ] && { printf '%s' "$c"; return 0; }
  done
  if [ -n "$tree" ] && [ -f "$tree/$KNEGCTL_SUITE_REL" ]; then printf '%s' "$tree/$KNEGCTL_SUITE_REL"; return 0; fi
  local lane; lane=$(knegctl_env_lane)
  if [ -n "$lane" ] && [ -f "$lane/$KNEGCTL_SUITE_REL" ]; then printf '%s' "$lane/$KNEGCTL_SUITE_REL"; return 0; fi
  printf ''
}

knegctl_scratch() { # NAME -> a fresh dir under the scratch root, outside the lane
  local root=${KNEGCTL_SCRATCH_ROOT:-${TMPDIR:-/tmp}}
  mkdir -p -- "$root" 2>/dev/null || return 1
  local d="$root/$1"
  rm -rf -- "$d" 2>/dev/null || true
  mkdir -p -- "$d" || return 1
  printf '%s' "$d"
}

# knegctl_nested_run REF — re-invoke the suite over REF and return stdout + rc.
knegctl_nested_run() { # REF
  local ref=$1 suite d env
  suite=$(knegctl_suite "$(knegctl_env_export)")
  [ -n "$suite" ] || return 1
  d=$(knegctl_scratch "nested-${ref:0:12}") || return 1
  env=$(printf '%s' "$d")
  (
    unset KNEGCTL_EXPORT KNEGCTL_VER_REF KNEGCTL_WORK KNEGCTL_PAYFILE KNEGCTL_SELFTEST_LINES KNEGCTL_RECEIPT_FILE KNEGCTL_SUITE
    unset R42_EXPORT R42_WORK R42_SCRATCH_ROOT R42_REF R42_RECEIPT_OUT R42_LEAF
    unset R43_EXPORT R43_WORK R43_SCRATCH_ROOT R43_REF R43_RECEIPT_OUT R43_LEAF
    TMPDIR="$env" bash "$suite" --export-ref "$ref" --lane "$(knegctl_env_lane)" \
      --work "$env/work" --scratch-root "$env" --leaf
  ) 2>/dev/null
}

knegctl_nested_facts() { # REF -> "rc tally reds lines" (tab separated)
  local ref=$1 out rc tally lines closedn reds=''
  out=$(knegctl_nested_run "$ref"); rc=$?
  if [ -n "${KNEGCTL_NESTED_LOG:-}" ] && [ -n "$out" ]; then
    mkdir -p -- "$KNEGCTL_NESTED_LOG" 2>/dev/null || true
    printf '%s\n' "$out" > "$KNEGCTL_NESTED_LOG/${ref:0:12}.txt" 2>/dev/null || true
  fi
  [ -n "$out" ] || { printf '%s\t-1\t\t0' "$rc"; return 0; }
  tally=$(printf '%s\n' "$out" | sed -n 's/^closed=\([0-9][0-9]*\)\/[0-9][0-9]* exit=[01]$/\1/p' | head -n 1)
  lines=$(printf '%s\n' "$out" | grep -cE '^[A-Za-z][A-Za-z0-9]* payload=.* closed=[01]$' 2>/dev/null || true)
  closedn=$(printf '%s\n' "$out" | grep -cE '^[A-Za-z][A-Za-z0-9]* payload=.* closed=1$' 2>/dev/null || true)
  local id
  for id in $KNEGCTL_DEPENDENT_IDS; do
    if printf '%s\n' "$out" | grep -qE "^$id payload=.* closed=0$"; then
      reds="$reds $id"
    fi
  done
  printf '%s\t%s\t%s\t%s\t%s' "$rc" "${tally:-n}" "${reds# }" "${lines:-0}" "${closedn:-0}"
}

# knegctl_driver_controls — 1 when the driver refuses a plain run (exit 2) and
# reports an unresolvable ref as its own red (exit 1, `ref-not-found`, and NO
# `closed=` tally line: an unresolvable ref is never a vacuous closed=0/19).
knegctl_driver_controls() { # TREE
  local tree=$1 suite d out rc ok=1
  suite=$(knegctl_suite "$tree")
  [ -n "$suite" ] || { printf '0'; return 0; }
  out=$(bash "$suite" 2>&1); rc=$?
  [ "$rc" = 2 ] || ok=0
  d=$(knegctl_scratch 'driver-ref-not-found') || { printf '0'; return 0; }
  out=$(bash "$suite" --export-ref 0000000000000000000000000000000000000000 \
        --lane "$(knegctl_env_lane)" --work "$d/work" --scratch-root "$d" 2>&1); rc=$?
  [ "$rc" = 1 ] || ok=0
  printf '%s\n' "$out" | grep -q 'ref-not-found' || ok=0
  if printf '%s\n' "$out" | grep -qE '^closed=[0-9]+/[0-9]+ exit=[01]$'; then ok=0; fi
  printf '%s' "$ok"
}

# knegctl_neg_accept TALLY RC REDS LINES -> 1 when a nested red is acceptable.
# Accepting a red requires: exit exactly 1 (a usage failure is exit 2 and a
# green run is not a control), the suite's own denominator, every payload line
# present, a tally strictly below it, and at least two TREE reds (a run that is
# red only because a capability is missing is not a control either).
knegctl_neg_accept() { # TALLY RC REDS LINES CLOSED_LINES
  local tally=$1 rc=$2 reds=$3 lines=$4 closedn=$5 n
  n=$(knegctl_nids)
  [ "$rc" = 1 ] || { printf '0'; return 0; }
  [ "$lines" = "$n" ] || { printf '0'; return 0; }
  case $tally in ''|*[!0-9]*) printf '0'; return 0 ;; esac
  [ "$tally" -lt "$n" ] && [ "$tally" -ge 0 ] || { printf '0'; return 0; }
  # the tally must be the tally of the payload lines it accompanies: a
  # transcript whose closed line contradicts its own lines is not evidence
  [ "$tally" = "${closedn:-n}" ] || { printf '0'; return 0; }
  local k
  set -- $reds
  k=$#
  [ "$k" -ge 2 ] || { printf '0'; return 0; }
  printf '1'
}

# check_k_negctl TREE [REF] — the K9 entry point.  Payload grammar is the
# round-42 J9 grammar: depth=1,base=<0|1>,r41=<0|1>,accept=tree-red,cap=nested.
# `depth` is 1 only when the driver's own refusals hold; `base`/`r41` are the
# nested re-invocations.
check_k_negctl() { # TREE [REF]
  local tree=$1 ref=${2:-}
  KNEGCTL_EXPORT=$tree
  [ -n "$ref" ] && KNEGCTL_VER_REF=$ref
  export KNEGCTL_EXPORT KNEGCTL_VER_REF
  local base_facts r41_facts depth base=0 r41=0
  depth=$(knegctl_driver_controls "$tree")
  base_facts=$(knegctl_nested_facts "$KNEGCTL_BASE")
  r41_facts=$(knegctl_nested_facts "$KNEGCTL_R41")
  IFS=$'\t' read -r brc btally breds blines bclosed <<< "$base_facts"
  base=$(knegctl_neg_accept "$btally" "$brc" "$breds" "$blines" "$bclosed")
  IFS=$'\t' read -r rrc rtally rreds rlines rclosed <<< "$r41_facts"
  r41=$(knegctl_neg_accept "$rtally" "$rrc" "$rreds" "$rlines" "$rclosed")
  local ok=0
  [ "$depth" = 1 ] && [ "$base" = 1 ] && [ "$r41" = 1 ] && ok=1
  printf '%s payload=depth=%s,base=%s,r41=%s,accept=tree-red,cap=nested closed=%s\n' \
    "$KNEGCTL_NEGCTL_ID" "$depth" "$base" "$r41" "$ok"
  [ "$ok" = 1 ] && return 0
  return 1
}

# ---------------------------------------------------------------------------
# the fixtures: the honest control and one fixture per class
# ---------------------------------------------------------------------------

# knegctl_forge_fixtures DIR — write the honest canonical transcript and one
# fixture per receipt-content class into DIR.  Each fixture carries exactly ONE
# defect at its own locus.
knegctl_forge_fixtures() { # DIR
  local d=$1
  mkdir -p -- "$d" || return 1
  local ctl="$d/control.txt"
  knegctl_assemble "$ctl" "$(knegctl_source_receipt)" || return 1
  cp -- "$ctl" "$d/honest.txt" 2>/dev/null || true
  local first foreign lane ver futc
  first=$(knegctl_non_self_ids | head -n 1)
  lane=$(knegctl_env_lane); ver=$(knegctl_env_verref)

  # missed-control: one graded case line is absent
  sed -E "/^selftest case=$first /d" -- "$ctl" > "$d/missed-control.txt"

  # composed-of-two-runs: a second run's instant line rides along
  awk 'NR == 5 { print; print; next } { print }' "$ctl" > "$d/composed-of-two-runs.txt"

  # payload-contradicting: a plausible payload value the suite never printed
  sed -E "s/^$first payload=.* closed=[01]\$/$first payload=synthetic=unprinted closed=1/" -- "$ctl" \
    > "$d/payload-contradicting.txt"

  # future-dated: run-utc post-dates the named ref's committer instant
  sed -E 's/^run-utc=.*$/run-utc=2999-01-01T00:00:00Z/' -- "$ctl" > "$d/future-dated.txt"

  # foreign-ref: the named ref resolves but is not bound to the verified tree
  foreign=$(git -C "$lane" rev-list --all --not "$ver" 2>/dev/null | head -n 1)
  [ -n "$foreign" ] || foreign=$(git -C "$lane" rev-list --all 2>/dev/null | tail -n 1)
  [ -n "$foreign" ] || foreign=1111111111111111111111111111111111111111
  sed -E "s/^export-ref=.*\$/export-ref=$foreign/" -- "$ctl" > "$d/foreign-ref.txt"
  futc=$(knegctl_ref_utc "$lane" "$foreign")
  if [ -n "$futc" ]; then
    sed -E "s/^run-utc=.*\$/run-utc=$futc/" -- "$d/foreign-ref.txt" > "$d/foreign-ref.tmp"
    mv -- "$d/foreign-ref.tmp" "$d/foreign-ref.txt"
  fi

  # nonexistent-ref: the named ref does not resolve as a commit
  sed -E 's/^export-ref=.*$/export-ref=0000000000000000000000000000000000000000/' -- "$ctl" \
    > "$d/nonexistent-ref.txt"

  # summary-only: the receipt claims a tally it does not carry
  local n c
  n=$(knegctl_nids); c=$((n + 6))
  sed -E "s/^closed=[0-9]+\/[0-9]+ exit=[01]\$/closed=$c\/$n exit=1/" -- "$ctl" > "$d/summary-only.txt"

  # tampered-payload-line: the self line's payload was edited
  sed -E "s/^$KNEGCTL_SELF_ID payload=.* closed=[01]\$/$KNEGCTL_SELF_ID payload=synthetic=tampered closed=1/" -- "$ctl" \
    > "$d/tampered-payload-line.txt"
  return 0
}

# knegctl_battery DIR — assemble, verify, and grade one fixture per class.
# Prints one line per case with the class token that failed, plus a tally.
knegctl_battery() { # DIR
  local d=$1 ctl payload rc name flags token missed=0 rejected=0
  knegctl_forge_fixtures "$d" || return 2
  ctl="$d/control.txt"
  payload=$(knegctl_verify "$ctl"); rc=$?
  local pm pmn pmt
  pm=$(knegctl_pm "$ctl"); pmn=${pm%%	*}; pmt=${pm##*	}
  if [ "$rc" = 0 ]; then
    printf 'battery case=control verdict=accepted token=- payload-match=%s/%s\n' "$pmn" "$pmt"
  else
    printf 'battery case=control verdict=rejected token=self-claim payload-match=%s/%s\n' "$pmn" "$pmt"
  fi
  for name in $KNEGCTL_CLASSES; do
    flags=$(knegctl_flags "$d/$name.txt")
    token=$(knegctl_cls_get "$flags" "$name")
    if [ "$token" = rejected ]; then
      printf 'battery case=%s verdict=rejected token=%s=rejected\n' "$name" "$name"
      rejected=$((rejected + 1))
    else
      printf 'battery case=%s verdict=missed token=%s=missed\n' "$name" "$name"
    fi
  done
  printf 'battery cases=%s rejected=%s missed=%s\n' \
    "$(($(knegctl_nclasses) + 1))" "$rejected" "$(($(knegctl_nclasses) - rejected))"
}

# ---------------------------------------------------------------------------
# the CLI (runs only when this file is executed directly)
# ---------------------------------------------------------------------------

knegctl_usage() {
  cat <<'EOF'
ExecNegCtlReceipt.sh — round-43 K8 receipt-integrity and K9 negative-control limb

  --receipt TREE [REF]         K8: grade the receipt of the export at TREE
  --negctl TREE [REF]          K9: re-invoke the suite over base and the r41 head
  --make-receipt [--out PATH]  write the canonical receipt transcript
  --verify FILE                grade one receipt file (payload + exit code)
  --flags FILE                 one independent verdict per receipt-content class
  --fixtures DIR               the honest control + one fixture per class
  --battery DIR                assemble, verify and grade the fixture battery
  --help                       this text

The environment supplies the host contract: EXPORT/TREE, REF_RESOLVED, LANE,
WORK and KNEGCTL_PAYFILE (or the payload_get / payload_closed / selftest_line
hooks).  KNEGCTL_* overrides retarget the limb at another suite generation.
EOF
}

knegctl_main() {
  while [ $# -gt 0 ]; do
    case $1 in
      --receipt) shift; [ $# -ge 1 ] || { printf 'knegctl: --receipt needs a tree\n' >&2; return 2; }
                 check_k_receipt "$1" "${2:-}"; return $? ;;
      --negctl) shift; [ $# -ge 1 ] || { printf 'knegctl: --negctl needs a tree\n' >&2; return 2; }
                 check_k_negctl "$1" "${2:-}"; return $? ;;
      --make-receipt) shift; make_receipt "$@"; return $? ;;
      --verify) shift; [ $# -ge 1 ] || { printf 'knegctl: --verify needs a file\n' >&2; return 2; }
                 knegctl_verify "$1"; return $? ;;
      --flags) shift; [ $# -ge 1 ] || { printf 'knegctl: --flags needs a file\n' >&2; return 2; }
               knegctl_flags "$1"; printf '\n'; return 0 ;;
      --fixtures) shift; [ $# -ge 1 ] || { printf 'knegctl: --fixtures needs a dir\n' >&2; return 2; }
                  knegctl_forge_fixtures "$1"; return $? ;;
      --battery) shift; [ $# -ge 1 ] || { printf 'knegctl: --battery needs a dir\n' >&2; return 2; }
                 knegctl_battery "$1"; return $? ;;
      -h|--help) knegctl_usage; return 0 ;;
      *) printf 'knegctl: unknown argument: %s\n' "$1" >&2; knegctl_usage >&2; return 2 ;;
    esac
  done
  knegctl_usage
  return 2
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  knegctl_main "$@"
  exit $?
fi
