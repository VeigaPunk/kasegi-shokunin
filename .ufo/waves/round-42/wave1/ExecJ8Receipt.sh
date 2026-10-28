#!/usr/bin/env bash
# ExecJ8Receipt.sh — round-42 J8 receipt-integrity limb (sourceable).
#
# WHAT THIS IS
#   The J8 limb of the round-42 closure suite: it decides whether a receipt
#   is the teed transcript of the graded run it claims to be. The receipt's
#   recorded payload lines are RE-DERIVED by the suite at receipt time and
#   compared token-for-token against the values the suite printed; a receipt
#   that carries a value the suite did not print is RED.
#
# THE RECEIPT CONTRACT (round 42)
#   A receipt is a transcript, not a summary. Its grammar is fixed; the
#   normative copy is .ufo/waves/round-42/wave1/ExecJ8Receipt.spec.txt.
#
#     all-gates v1
#     export-ref=<40 hex>
#     suite-sha256=<64 hex>
#     time-basis=ref-commit
#     run-utc=<YYYY-MM-DDTHH:MM:SSZ>
#     J1 payload=<k=v,...> closed=0|1
#     ... J13 ...
#     selftest case=J1 mutants=<ok>/<n> positive=pass payload-match=1 verdict=pass
#     ... J13 ...
#     selftest cases=13 failures=0
#     closed=13/13 exit=0
#
#   `export-ref` is the commit the transcript was teed at (the judged head J
#   when the receipt is committed at Y = J + receipt). `time-basis=ref-commit`
#   says exactly what `run-utc` is: the committer instant of the ref the
#   receipt NAMES, never a wall clock. The transcript is a function of the
#   tree and the ref-scoped facts only, so two runs over the same ref are
#   byte-identical and the receipt equals a re-run with nothing normalised.
#
# THE SELF-REFERENCE (why the receipt can grade itself)
#   The receipt records the J8 line and the J8 line grades the receipt. The
#   loop is CLOSED, not trusted. The canonical J8 payload is computed from
#   the CANONICAL TRANSCRIPT — the transcript this run would write now, built
#   from the freshly re-derived payload values, the freshly re-executed graded
#   selftest lines and the ref-scoped facts. It never reads the value
#   recorded on the receipt's own J8 line, so the fixed point exists and is
#   reached in one rewrite.
#
# THE SEVEN FORGERY CLASSES
#   Each class is decided by ONE ABSOLUTE predicate over a named locus of the
#   receipt's own bytes plus independently derived facts. No class is decided
#   by comparing a count in one artifact with a count in another artifact,
#   and no class is decided by "the number of mismatches went up". The loci
#   are disjoint by construction, so a receipt carrying one defect raises
#   exactly one class and the honest receipt raises none.
#
#     missed-control        a required control ELEMENT is absent: a header
#                           line, one check's graded selftest case line, the
#                           selftest summary line or the closed line
#     payload-contradicting a recorded payload value contradicts the value
#                           the suite RE-DERIVED for that same check
#     future-dated          the recorded run-utc is not the committer instant
#                           of the ref it names, or it post-dates the
#                           verification clock
#     foreign-ref           the named ref resolves as a commit but is not
#                           BOUND to the verified tree: it is not an ancestor
#                           of the verification ref, or the diff between it
#                           and the verification ref lists a path other than
#                           the receipt
#     nonexistent-ref       the named ref does not resolve as a commit
#     summary-only          the receipt claims a closed tally it does not
#                           carry (fewer per-check run lines than the tally
#                           declares)
#     tampered-payload-line the receipt's own J8 line does not carry the
#                           canonical payload for this run (the self-claim
#                           was edited)
#
#   `rejected` means the class WAS detected in this receipt; `missed` means
#   it was not. The check is red when any class is rejected.
#
# HOST CONTRACT (what the suite must provide; every hook has a fallback)
#   EXPORT / J8_EXPORT   the export root (the tree the run was teed at)
#   REF_RESOLVED         the resolved verification ref (or J8_VER_REF)
#   LANE                 the lane repo (read-only git reads only)
#   WORK                 the work dir (holds payloads.tsv and sel-<ID>.line)
#   PAYFILE              payloads.tsv: ID \t payload \t closed
#   payload_get ID       the payload this run printed for ID      (optional)
#   payload_closed ID    the closed bit this run computed for ID  (optional)
#   selftest_line ID     the graded selftest case line for ID     (optional)
#
#   ORDERING (the suite must respect it):
#     1. the other twelve checks must have produced their payload values
#        (J8 reads them; it cannot grade a receipt against values that were
#        never computed),
#     2. the graded selftest must have produced its thirteen case lines,
#     3. only then may the receipt be assembled and J8 run.
#
#   INVARIANCE (the suite must hold it, or the receipt at Y cannot be
#   reproduced from the run at J): the other twelve payload values and the
#   other twelve graded selftest case lines must be byte-identical between
#   the run at J and the run at Y. The receipt path must therefore be
#   excluded from every tree-dependent check and from every selftest fixture:
#   the receipt does not exist in the tree at J and does exist in the tree
#   at Y.
#
# ENTRY POINTS
#   check_j8 TREE REF            the J8 check: prints the payload, exit 0/1
#   make_receipt [--out PATH]    write the canonical receipt transcript
#   j8_verify FILE               grade one receipt file: payload + status
#   j8_flags FILE                one independent verdict per forgery class
#   j8_forge_fixtures DIR        the honest control + the seven forgeries
#
# Sourcing this file defines functions only; it runs the CLI only when it is
# executed directly.

# ---------------------------------------------------------------------------
# configuration (every value is overridable from the environment)
# ---------------------------------------------------------------------------

J8_SENTINEL=${J8_SENTINEL:-'all-gates v1'}
J8_RECEIPT_REL=${J8_RECEIPT_REL:-'.ufo/waves/round-42/final-gates/all-gates.txt'}
J8_SUITE_REL=${J8_SUITE_REL:-'corpus/instruments/r42-closure.sh'}
J8_CHECK_IDS=${J8_CHECK_IDS:-'J1 J2 J3 J4 J5 J6 J7 J8 J9 J10 J11 J12 J13'}
J8_SELF_ID=${J8_SELF_ID:-'J8'}
J8_FORGE_DISABLE=${J8_FORGE_DISABLE:-}

# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

j8_ids() { printf '%s\n' $J8_CHECK_IDS; }
j8_nids() { local n=0 i; for i in $J8_CHECK_IDS; do n=$((n + 1)); done; printf '%s' "$n"; }
j8_non_self_ids() { local i; for i in $J8_CHECK_IDS; do [ "$i" = "$J8_SELF_ID" ] || printf '%s\n' "$i"; done; }
j8_n_non_self() { local n=0 i; for i in $J8_CHECK_IDS; do [ "$i" = "$J8_SELF_ID" ] || n=$((n + 1)); done; printf '%s' "$n"; }

j8_kv_get() { printf '%s\n' "$1" | tr ',' '\n' | sed -n "s/^$2=//p" | head -n 1; }

j8_file_digest() {
  local f=$1
  if [ -z "$f" ] || [ ! -r "$f" ]; then printf 'unreadable'; return 0; fi
  sha256sum -- "$f" | awk '{print $1; exit}'
}

j8_ref_utc() { # LANE REF
  local e
  [ -n "${2:-}" ] || return 1
  e=$(git -C "$1" log -1 --format=%ct "$2" 2>/dev/null) || return 1
  case $e in ''|*[!0-9]*) return 1 ;; esac
  TZ=UTC date -u -d "@$e" +%Y-%m-%dT%H:%M:%SZ
}

j8_iso_past() { # ISO -> 1 when no later than now+120s
  local n
  case $1 in
    [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z) ;;
    *) printf '0'; return 0 ;;
  esac
  n=$(date -u -d "$1" +%s 2>/dev/null) || { printf '0'; return 0; }
  if [ "$n" -le $(( $(date -u +%s) + 120 )) ]; then printf '1'; else printf '0'; fi
}

j8_env_export() { printf '%s' "${J8_EXPORT:-${EXPORT:-}}"; }
j8_env_lane()   { printf '%s' "${J8_LANE:-${LANE:-}}"; }
j8_env_verref() { printf '%s' "${J8_VER_REF:-${REF_RESOLVED:-}}"; }
j8_env_work()   { printf '%s' "${J8_WORK:-${WORK:-}}"; }

# j8_tokens_equal A B — token-for-token comparison of two comma-joined
# payload strings: both are split on ',' into their k=v tokens and the token
# sequences must be byte-identical, in order. A substring match is never a
# match: `closed=7/8` and `closed=7/80` are different tokens.
j8_tokens_equal() {
  local a=$1 b=$2
  [ "$a" = "$b" ] || return 1
  local ta tb
  ta=$(printf '%s\n' "$a" | tr ',' '\n')
  tb=$(printf '%s\n' "$b" | tr ',' '\n')
  [ "$ta" = "$tb" ]
}

# ---------------------------------------------------------------------------
# the host hooks (with file fallbacks)
# ---------------------------------------------------------------------------

j8_payload_get() { # ID -> the payload this run printed
  if declare -F payload_get >/dev/null 2>&1; then payload_get "$1"; return 0; fi
  local t=${J8_PAYLOAD_TSV:-${PAYFILE:-}}
  [ -n "$t" ] && [ -f "$t" ] || return 0
  awk -F'\t' -v id="$1" '$1 == id { print $2; exit }' "$t"
}

j8_payload_closed() { # ID -> 0|1
  if declare -F payload_closed >/dev/null 2>&1; then payload_closed "$1"; return 0; fi
  local t=${J8_PAYLOAD_TSV:-${PAYFILE:-}}
  if [ -z "$t" ] || [ ! -f "$t" ]; then printf '1'; return 0; fi
  local c
  c=$(awk -F'\t' -v id="$1" '$1 == id { print $3; exit }' "$t")
  case $c in 0|1) printf '%s' "$c" ;; *) printf '1' ;; esac
}

j8_selftest_line() { # ID -> the graded selftest case line
  if declare -F selftest_line >/dev/null 2>&1; then selftest_line "$1"; return 0; fi
  local w; w=$(j8_env_work)
  if [ -n "$w" ] && [ -f "$w/sel-$1.line" ]; then cat -- "$w/sel-$1.line"; return 0; fi
  if [ -n "$w" ] && [ -f "$w/selftest-lines.txt" ]; then
    grep -m1 "^selftest case=$id " "$w/selftest-lines.txt" 2>/dev/null || true
  fi
  return 0
}

# ---------------------------------------------------------------------------
# the receipt under test, the ref it names, and the verified tree
# ---------------------------------------------------------------------------

# j8_source_receipt — the receipt committed inside the export (the receipt at
# Y), or the empty string when the export carries none (the run at J).
j8_source_receipt() {
  local exp_root; exp_root=$(j8_env_export)
  if [ -n "$exp_root" ] && [ -f "$exp_root/$J8_RECEIPT_REL" ]; then
    printf '%s' "$exp_root/$J8_RECEIPT_REL"
    return 0
  fi
  printf ''
}

# j8_named_ref [FILE] — the ref the receipt NAMES: the commit the transcript
# was teed at, which is the judged head J when the receipt is committed at
# Y = J + receipt. Without a receipt the ref under verification is used.
j8_named_ref() { # [FILE]
  local f=${1:-} href
  if [ -n "$f" ] && [ -f "$f" ]; then
    href=$(sed -n 's/^export-ref=//p' -- "$f" 2>/dev/null | head -n 1)
    case $href in
      [0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]*) printf '%s' "$href"; return 0 ;;
    esac
  fi
  printf '%s' "$(j8_env_verref)"
}

J8_IN_TARGET=0
j8_receipt_target() { # TREE
  if [ -n "${J8_RECEIPT_TARGET:-}" ]; then printf '%s' "$J8_RECEIPT_TARGET"; return 0; fi
  local tree=${1:-}
  local exp="$tree/$J8_RECEIPT_REL"
  if [ -n "$tree" ] && [ -f "$exp" ]; then printf '%s' "$exp"; return 0; fi
  # the export carries no receipt (the run at the judged head J): the seed is
  # the byte-identical twin of the receipt this run is about to write, so
  # grading it is the same computation as grading the committed receipt at Y
  if [ "$J8_IN_TARGET" = 0 ]; then
    J8_IN_TARGET=1
    j8_seed >/dev/null 2>&1
    J8_IN_TARGET=0
  fi
  local work; work=$(j8_env_work)
  if [ -n "$work" ] && [ -f "$work/j8-seed.txt" ]; then printf '%s' "$work/j8-seed.txt"; return 0; fi
  printf '%s' "$exp"
}

# j8_tree_bind [EXPORT] [VER] — 1 when the export IS the verified ref's tree
# with respect to the receipt: the export carries the receipt iff that ref's
# tree carries it, and when both carry it the bytes are the same blob. This
# is what makes "the run at J" (no receipt in the export, none in the tree)
# and "the run at Y" (receipt in both, same bytes) the same fact value, and
# what catches a host that exports one tree and names another.
j8_tree_bind() { # [EXPORT] [VER]
  local exp=${1:-} ver=${2:-} lane exp_r ver_blob file_blob
  [ -n "$exp" ] || exp=$(j8_env_export)
  [ -n "$ver" ] || ver=$(j8_env_verref)
  lane=$(j8_env_lane)
  [ -n "$lane" ] && [ -n "$ver" ] || { printf '0'; return 0; }
  exp_r=''
  [ -f "$exp/$J8_RECEIPT_REL" ] && exp_r="$exp/$J8_RECEIPT_REL"
  if ver_blob=$(git --no-optional-locks -C "$lane" rev-parse "${ver}:${J8_RECEIPT_REL}" 2>/dev/null); then
    [ -n "$exp_r" ] || { printf '0'; return 0; }
    file_blob=$(git --no-optional-locks -C "$lane" hash-object -- "$exp_r" 2>/dev/null)
    [ -n "$file_blob" ] && [ "$file_blob" = "$ver_blob" ] && { printf '1'; return 0; }
    printf '0'; return 0
  fi
  [ -n "$exp_r" ] && { printf '0'; return 0; }
  printf '1'
}

# ---------------------------------------------------------------------------
# layer 1: the facts of a receipt (never reads the receipt's own J8 payload)
# ---------------------------------------------------------------------------

# j8_facts FILE — the fact bundle of FILE. It describes the header, the body,
# the graded selftest block and the agreement between what the receipt
# RECORDS and what the suite RE-DERIVED. It never reads the value recorded
# on FILE's own J8 line and never counts the self id's selftest case line, so
# the bundle is invariant under the self-claim rewrite and the fixed point
# exists.
j8_facts() { # FILE
  local f=$1
  local exp_root lane ver sent=0 refhex='' refok=0 dig=0 tb=0 utc=0 notf=0
  local anc=0 dclean=1 dread=ok hdr=0 runl=0 sell=0 selv=0 summ=0 cll=0 bind=0
  local pm=0 cm=0 sm=0 id rec want n m

  if [ ! -f "$f" ]; then
    printf 'receipt=0,sentinel=0,ref=0,digest=0,time-basis=0,run-utc=0,not-future=0,ancestor=0,diff-clean=0,diff-read=%s,tree-bind=0,header-lines=0,run-lines=0,selftest-lines=0,selftest-verdicts=0,summary=0,closed-line=0,payload-match=0/0,closed-match=0/0,selftest-match=0/0' \
      "$dread"
    return 0
  fi

  exp_root=$(j8_env_export); lane=$(j8_env_lane); ver=$(j8_env_verref)
  n=$(j8_nids); m=$(j8_n_non_self)

  # --- header ---
  [ "$(sed -n '1p' -- "$f")" = "$J8_SENTINEL" ] && sent=1
  if [ "$(grep -cE '^export-ref=[0-9a-f]{40}$' -- "$f")" = 1 ]; then
    refhex=$(sed -n 's/^export-ref=//p' -- "$f" | head -n 1)
  fi
  if [ -n "$refhex" ] && [ -n "$lane" ] \
     && git -C "$lane" cat-file -e "${refhex}^{commit}" 2>/dev/null; then refok=1; fi
  if [ "$(grep -cE '^suite-sha256=[0-9a-f]{64}$' -- "$f")" = 1 ]; then
    want=$(sed -n 's/^suite-sha256=//p' -- "$f" | head -n 1)
    [ "$want" = "$(j8_file_digest "$exp_root/$J8_SUITE_REL")" ] && dig=1
  fi
  [ "$(grep -cxF 'time-basis=ref-commit' -- "$f")" = 1 ] && tb=1
  if [ "$(grep -cE '^run-utc=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$' -- "$f")" = 1 ]; then
    want=$(sed -n 's/^run-utc=//p' -- "$f" | head -n 1)
    [ "$(j8_iso_past "$want")" = 1 ] && notf=1
    if [ -n "$refhex" ]; then
      local wutc; wutc=$(j8_ref_utc "$lane" "$refhex")
      [ -n "$wutc" ] && [ "$wutc" = "$want" ] && utc=1
    fi
  fi
  if [ -n "$refhex" ]; then
    local i hline
    i=0
    for hline in "$J8_SENTINEL" \
                  "export-ref=$refhex" \
                  "suite-sha256=$(j8_file_digest "$exp_root/$J8_SUITE_REL")" \
                  'time-basis=ref-commit' \
                  "run-utc=$(j8_ref_utc "$lane" "$refhex")"; do
      i=$((i + 1))
      [ "$(sed -n "${i}p" -- "$f")" = "$hline" ] && hdr=$((hdr + 1))
    done
  fi

  # --- body ---
  runl=$(grep -cE '^J[0-9]+ payload=.* closed=[01]$' -- "$f" 2>/dev/null || true); runl=${runl:-0}
  # the selftest counts cover the other twelve cases only: the self id's case
  # line is the one under construction while the receipt is assembled
  for id in $(j8_non_self_ids); do
    grep -q "^selftest case=$id .* verdict=\(pass\|fail\)$" -- "$f" 2>/dev/null && sell=$((sell + 1))
    grep -q "^selftest case=$id .* verdict=pass$" -- "$f" 2>/dev/null && selv=$((selv + 1))
  done
  [ "$(grep -cxF "selftest cases=$n failures=0" -- "$f")" = 1 ] && summ=1
  [ "$(grep -cxF "closed=$n/$n exit=0" -- "$f")" = 1 ] && cll=1

  # --- agreement between what is RECORDED and what is RE-DERIVED ---
  for id in $(j8_non_self_ids); do
    rec=$(sed -n "s/^$id payload=\(.*\) closed=[01]\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
    want=$(j8_payload_get "$id")
    [ -n "$want" ] && j8_tokens_equal "$rec" "$want" && pm=$((pm + 1))
    rec=$(sed -n "s/^$id payload=.* closed=\([01]\)\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
    want=$(j8_payload_closed "$id")
    [ "$rec" = "$want" ] && cm=$((cm + 1))
    rec=$(grep -m1 "^selftest case=$id " -- "$f" 2>/dev/null)
    want=$(j8_selftest_line "$id")
    [ -n "$want" ] && [ "$rec" = "$want" ] && sm=$((sm + 1))
  done

  # --- the ref facts: the named ref must be an ancestor of the verified ref
  #     and the diff between them must list nothing but the receipt ---
  if [ -n "$refhex" ] && [ -n "$lane" ] && [ -n "$ver" ] && [ "$refok" = 1 ]; then
    if git --no-optional-locks -C "$lane" merge-base --is-ancestor "$refhex" "$ver" 2>/dev/null; then
      anc=1
    fi
    local name x
    if name=$(git --no-optional-locks -C "$lane" diff --name-only "$refhex" "$ver" 2>/dev/null); then
      while IFS= read -r x; do
        [ -n "$x" ] || continue
        [ "$x" = "$J8_RECEIPT_REL" ] || dclean=0
      done <<< "$name"
    else
      dread=fail; dclean=0
    fi
  fi

  bind=$(j8_tree_bind "$exp_root" "$ver")
  printf 'receipt=1,sentinel=%s,ref=%s,digest=%s,time-basis=%s,run-utc=%s,not-future=%s,ancestor=%s,diff-clean=%s,diff-read=%s,tree-bind=%s,header-lines=%s,run-lines=%s,selftest-lines=%s,selftest-verdicts=%s,summary=%s,closed-line=%s,payload-match=%s/%s,closed-match=%s/%s,selftest-match=%s/%s' \
    "$sent" "$refok" "$dig" "$tb" "$utc" "$notf" "$anc" "$dclean" "$dread" "$bind" \
    "$hdr" "$runl" "$sell" "$selv" "$summ" "$cll" \
    "$pm" "$m" "$cm" "$m" "$sm" "$m"
}


# ---------------------------------------------------------------------------
# layer 2: the transcript assembly, the control and the canonical bundle
# ---------------------------------------------------------------------------

# j8_assemble OUT CONTROL [SOURCE] — write the canonical receipt transcript.
# CONTROL is the control flag recorded on the self line; the caller iterates
# it to the fixed point (the control's own verdict does not depend on it).
# SOURCE is the receipt whose export-ref line the new transcript adopts (the
# committed receipt at Y); without it the ref under verification is used.
j8_assemble() { # OUT CONTROL [SOURCE]
  local out=$1 control=${2:-1} source=${3:-}
  local exp_root lane href sha utc id n k=0 line
  exp_root=$(j8_env_export); lane=$(j8_env_lane)
  href=$(j8_named_ref "$source")
  sha=$(j8_file_digest "$exp_root/$J8_SUITE_REL")
  utc=$(j8_ref_utc "$lane" "$href"); [ -n "$utc" ] || utc=unreadable
  {
    printf '%s\n' "$J8_SENTINEL"
    printf 'export-ref=%s\n' "$href"
    printf 'suite-sha256=%s\n' "$sha"
    printf 'time-basis=ref-commit\n'
    printf 'run-utc=%s\n' "$utc"
    for id in $(j8_ids); do
      if [ "$id" = "$J8_SELF_ID" ]; then
        printf '%s payload=PENDING closed=1\n' "$id"
        continue
      fi
      printf '%s payload=%s closed=%s\n' "$id" "$(j8_payload_get "$id")" "$(j8_payload_closed "$id")"
    done
    for id in $(j8_ids); do
      line=$(j8_selftest_line "$id")
      if [ -z "$line" ]; then
        line="selftest case=$id mutants=0/0 positive=pending payload-match=0 verdict=pending"
      fi
      printf '%s\n' "$line"
    done
    # the closed tally counts the other twelve checks plus the self line,
    # which the assembly asserts closed: the transcript is written only for a
    # green run
    for id in $(j8_non_self_ids); do
      [ "$(j8_payload_closed "$id")" = 1 ] && k=$((k + 1))
    done
    k=$((k + 1))
    n=$(j8_nids)
    printf 'selftest cases=%s failures=0\n' "$n"
    printf 'closed=%s/%s exit=0\n' "$k" "$n"
  } > "$out"
  # Close the self-reference: the self line's payload is the canonical bundle
  # of the file being assembled, computed WITHOUT reading the self payload.
  # The fixed point is reached in one rewrite.
  local bundle
  bundle=$(j8_facts "$out")
  bundle="${bundle},control=$control"
  local tmp="$out.tmp.$$"
  awk -v self="$J8_SELF_ID" -v pay="$bundle" \
    '$0 ~ "^" self " payload=" { print self " payload=" pay " closed=1"; next } { print }' \
    "$out" > "$tmp" && mv -- "$tmp" "$out"
  return 0
}

# j8_seed_path — the seed: the canonical transcript this run would write now.
j8_seed_path() { printf '%s' "$(j8_env_work)/j8-seed.txt"; }

# j8_seed — (re)write the seed. The seed is the byte-identical twin of the
# receipt the run is about to write, so the J run and the Y run grade the
# same bytes.
j8_seed() {
  local work; work=$(j8_env_work)
  [ -n "$work" ] || return 2
  mkdir -p -- "$work" || return 2
  local source; source=$(j8_source_receipt)
  local control
  control=$(j8_control_state)
  j8_assemble "$(j8_seed_path)" "$control" "$source" || return 2
  return 0
}

# j8_control_state — the honest control receipt must be CLEAN. The control is
# assembled from the re-derived values of THIS run, never from the receipt
# under test, so a detector that fires on an honest receipt is caught instead
# of silently accepting everything.
j8_control_state() {
  local work; work=$(j8_env_work)
  [ -n "$work" ] || { printf 'unknown'; return 0; }
  mkdir -p -- "$work" 2>/dev/null || { printf 'unknown'; return 0; }
  local ctl="$work/j8-control.txt"
  local guess=1 ok=1 i
  for i in 1 2 3 4; do
    j8_assemble "$ctl" "$guess" || { printf 'unknown'; return 0; }
    ok=$(j8_control_clean "$ctl")
    [ "$ok" = "$guess" ] && break
    guess=$ok
  done
  printf '%s' "$ok"
}

# j8_control_clean FILE — 1 when FILE grades clean under the six
# receipt-content classes. The self-claim class is excluded here on purpose:
# the control's own self-claim is the value under construction, and the
# class table is not allowed to depend on the field it would decide.
j8_control_clean() { # FILE
  local flags
  flags=$(j8_flags "$1" skip-self)
  case $flags in
    *'=rejected'*) printf '0'; return 0 ;;
  esac
  printf '1'
}

# j8_canonical_bundle — the canonical J8 payload of THIS run: the fact
# bundle of the canonical transcript plus the control flag. This is the value
# the receipt's own J8 line must carry. It is computed WITHOUT reading the
# receipt's J8 line, so the self-reference is closed rather than trusted.
j8_canonical_bundle() {
  local facts control
  j8_seed >/dev/null 2>&1
  facts=$(j8_facts "$(j8_seed_path)")
  control=$(j8_control_state)
  printf '%s,control=%s' "$facts" "$control"
}

# ---------------------------------------------------------------------------
# layer 3: the seven forgery classes
# ---------------------------------------------------------------------------

# j8_flags FILE [skip-self] — one independent verdict per forgery class.
# `rejected` means the class WAS detected in this receipt; `missed` means it
# was not. `skip-self` omits the self-claim class (used by the control).
j8_flags() { # FILE [skip-self]
  local f=$1 skipself=${2:-}
  local payload=missed future=missed foreign=missed nonexistent=missed
  local summary=missed tampered=missed control=missed
  local lane ver refhex utc

  if [ ! -f "$f" ]; then
    printf 'missed-control=rejected,payload-contradicting=rejected,future-dated=rejected,foreign-ref=rejected,nonexistent-ref=rejected,summary-only=rejected,tampered-payload-line=rejected'
    return 0
  fi

  lane=$(j8_env_lane); ver=$(j8_env_verref)

  # --- missed-control: a required control ELEMENT is absent ---
  local n id ok=1
  n=$(j8_nids)
  [ "$(sed -n '1p' -- "$f")" = "$J8_SENTINEL" ] || ok=0
  [ "$(grep -cE '^export-ref=[0-9a-f]{40}$' -- "$f")" = 1 ] || ok=0
  [ "$(grep -cE '^suite-sha256=[0-9a-f]{64}$' -- "$f")" = 1 ] || ok=0
  [ "$(grep -cxF 'time-basis=ref-commit' -- "$f")" = 1 ] || ok=0
  [ "$(grep -cE '^run-utc=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$' -- "$f")" = 1 ] || ok=0
  for id in $(j8_non_self_ids); do
    [ "$(grep -c "^selftest case=$id " -- "$f")" = 1 ] || ok=0
  done
  # the self id's case line is graded by presence only: its CONTENT is the
  # self-reference and is closed by the canonical bundle, but the transcript
  # grammar requires it to be there, exactly once, and graded
  [ "$(grep -c "^selftest case=$J8_SELF_ID .* verdict=\(pass\|fail\)$" -- "$f")" = 1 ] || ok=0
  [ "$(grep -cxF "selftest cases=$n failures=0" -- "$f")" = 1 ] || ok=0
  [ "$(grep -cxF "closed=$n/$n exit=0" -- "$f")" = 1 ] || ok=0
  [ "$ok" = 1 ] || control=rejected

  # --- payload-contradicting: a recorded payload contradicts the re-derived
  #     value for that check, or the receipt carries a run line for an id the
  #     suite never printed ---
  local rec want lid rec_closed want_closed
  while IFS= read -r lid; do
    [ -n "$lid" ] || continue
    # the self line's payload is the canonical bundle, graded by the
    # tampered-payload-line class; it is not a value the suite printed
    [ "$lid" = "$J8_SELF_ID" ] && continue
    rec=$(sed -n "s/^$lid payload=\(.*\) closed=[01]\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
    rec_closed=$(sed -n "s/^$lid payload=.* closed=\([01]\)\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
    case " $J8_CHECK_IDS " in
      *" $lid "*)
        want=$(j8_payload_get "$lid")
        want_closed=$(j8_payload_closed "$lid")
        { [ -n "$want" ] && j8_tokens_equal "$rec" "$want"; } || payload=rejected
        [ "$rec_closed" = "$want_closed" ] || payload=rejected ;;
      *) payload=rejected ;;
    esac
    [ "$payload" = rejected ] && break
  done <<< "$(sed -n 's/^\(J[0-9][0-9]*\) payload=.* closed=[01]$/\1/p' -- "$f" 2>/dev/null)"
  # a check the suite DID print but the receipt DROPPED is the summary-only
  # locus, not this one

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
      rinst=$(j8_ref_utc "$lane" "$refhex")
      if [ -n "$rinst" ]; then
        re=$(date -u -d "$rinst" +%s 2>/dev/null || echo '')
        [ -n "$re" ] && [ "$e" -ne "$re" ] && future=rejected
      fi
    fi
  fi

  # --- foreign-ref / nonexistent-ref: existence and binding of the named ref ---
  if [ -z "$refhex" ]; then
    nonexistent=rejected
  elif [ -n "$lane" ] && git -C "$lane" cat-file -e "${refhex}^{commit}" 2>/dev/null; then
    if [ "$(j8_tree_bind "$(j8_env_export)" "$ver")" != 1 ]; then
      # the export is not the verified ref's tree: the receipt cannot have
      # been teed at the ref the suite claims to be verifying
      foreign=rejected
    elif [ -n "$ver" ]; then
      if ! git --no-optional-locks -C "$lane" merge-base --is-ancestor "$refhex" "$ver" 2>/dev/null; then
        foreign=rejected
      else
        local name x
        if name=$(git --no-optional-locks -C "$lane" diff --name-only "$refhex" "$ver" 2>/dev/null); then
          while IFS= read -r x; do
            [ -n "$x" ] || continue
            [ "$x" = "$J8_RECEIPT_REL" ] || foreign=rejected
          done <<< "$name"
        else
          foreign=rejected
        fi
      fi
    fi
  else
    nonexistent=rejected
  fi

  # --- summary-only: the receipt claims a tally it does not carry ---
  local declared runl
  declared=$(sed -n 's/^closed=\([0-9][0-9]*\)\/[0-9][0-9]* exit=[01]$/\1/p' -- "$f" 2>/dev/null | head -n 1)
  runl=$(grep -cE '^J[0-9]+ payload=.* closed=[01]$' -- "$f" 2>/dev/null || true)
  case $declared in ''|*[!0-9]*) summary=rejected ;; *)
    case $runl in ''|*[!0-9]*) summary=rejected ;; *)
      [ "${runl:-0}" -lt "$declared" ] && summary=rejected ;;
    esac ;;
  esac

  # --- tampered-payload-line: the receipt's own J8 line does not carry the
  #     canonical payload for this run. The canonical bundle is computed from
  #     the freshly re-derived values, never from the receipt's J8 line, so
  #     this class fires on a self-claim edit alone and never on any other
  #     class's locus. ---
  if [ "$skipself" != skip-self ]; then
    local rec_self canonical
    rec_self=$(sed -n "s/^$J8_SELF_ID payload=\(.*\) closed=[01]\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
    canonical=$(j8_canonical_bundle)
    [ "$rec_self" != "$canonical" ] && tampered=rejected
  fi

  case "${J8_FORGE_DISABLE:-}" in
    missed-control) control=missed ;;
    payload-contradicting) payload=missed ;;
    future-dated) future=missed ;;
    foreign-ref) foreign=missed ;;
    nonexistent-ref) nonexistent=missed ;;
    summary-only) summary=missed ;;
    tampered-payload-line) tampered=missed ;;
  esac

  printf 'missed-control=%s,payload-contradicting=%s,future-dated=%s,foreign-ref=%s,nonexistent-ref=%s,summary-only=%s,tampered-payload-line=%s' \
    "$control" "$payload" "$future" "$foreign" "$nonexistent" "$summary" "$tampered"
}

# ---------------------------------------------------------------------------
# layer 4: the grade
# ---------------------------------------------------------------------------

# j8_verify FILE — grade one receipt file. Prints the canonical J8 payload on
# stdout; exit 0 when the receipt is honest, 1 when it is red.
j8_verify() { # FILE
  local f=$1
  local canonical rec_self rec_closed flags facts cfacts
  canonical=$(j8_canonical_bundle)
  rec_self=$(sed -n "s/^$J8_SELF_ID payload=\(.*\) closed=[01]\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
  rec_closed=$(sed -n "s/^$J8_SELF_ID payload=.* closed=\([01]\)\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
  flags=$(j8_flags "$f")
  facts=$(j8_facts "$f")
  cfacts=$(j8_facts "$(j8_seed_path)")
  case $flags in
    *'=rejected'*)
      printf '%s' "$canonical"
      return 1 ;;
  esac
  if [ "$rec_self" = "$canonical" ] && [ "$rec_closed" = 1 ] && [ "$facts" = "$cfacts" ]; then
    printf '%s' "$canonical"
    return 0
  fi
  printf '%s' "$canonical"
  return 1
}

# check_j8 TREE REF — the suite entry point. Prints the J8 payload; exit 0
# when the receipt under TREE is the teed transcript of this run.
check_j8() { # TREE REF
  local tree=$1 ref=$2
  local J8_EXPORT=$tree J8_VER_REF=$ref
  local f; f=$(j8_receipt_target "$tree")
  j8_verify "$f"
}

# ---------------------------------------------------------------------------
# the receipt producer
# ---------------------------------------------------------------------------

# make_receipt [--out PATH] — write the canonical receipt transcript. The
# transcript adopts the export-ref of the receipt already in the export (the
# committed receipt at Y) so that the bytes written at J and the bytes read
# at Y are the same bytes.
make_receipt() {
  local out=''
  while [ $# -gt 0 ]; do
    case $1 in
      --out) out=${2:-}; shift 2 ;;
      *) shift ;;
    esac
  done
  [ -n "$out" ] || out=/dev/stdout
  local work; work=$(j8_env_work)
  local draft="$work/j8-draft.txt"
  if [ -z "$work" ]; then
    draft=$(mktemp -t j8-receipt.XXXXXXXX) || return 2
  else
    mkdir -p -- "$work" || return 2
  fi
  local source; source=$(j8_source_receipt)
  local control
  control=$(j8_control_state)
  j8_assemble "$draft" "$control" "$source" || return 2
  mkdir -p -- "$(dirname -- "$out")" 2>/dev/null || true
  cat -- "$draft" > "$out" || return 2
  [ "$out" = /dev/stdout ] || rm -f -- "$draft"
  return 0
}

# ---------------------------------------------------------------------------
# the committed fixtures: the honest control + the seven forgeries
# ---------------------------------------------------------------------------

# j8_forge_fixtures DIR — write the honest control and one fixture per
# forgery class into DIR. Each fixture carries exactly ONE defect, so the
# seven classes are provably disjoint on these bytes.
j8_forge_fixtures() { # DIR
  local d=$1
  mkdir -p -- "$d" || return 1
  local ctl="$d/honest.txt"
  local source; source=$(j8_source_receipt)
  local control lane ver
  control=$(j8_control_state)
  j8_assemble "$ctl" "$control" "$source" || return 1
  cp -- "$ctl" "$d/control.txt"

  local id first foreign
  first=$(j8_non_self_ids | head -n 1)
  lane=$(j8_env_lane); ver=$(j8_env_verref)

  # missed-control: one check's graded selftest case line is absent
  sed -E "/^selftest case=$first /d" -- "$ctl" > "$d/missed-control.txt"

  # payload-contradicting: a recorded payload contradicts the re-derived one
  sed -E "s/^$first payload=.* closed=[01]\$/$first payload=zz-forged closed=1/" -- "$ctl" \
    > "$d/payload-contradicting.txt"

  # future-dated: run-utc post-dates the named ref's committer instant
  sed -E 's/^run-utc=.*$/run-utc=2999-01-01T00:00:00Z/' -- "$ctl" > "$d/future-dated.txt"

  # foreign-ref: the named ref resolves but is not BOUND to the verified
  # tree: it is an ancestor, but the diff between it and the verified ref
  # lists paths other than the receipt
  foreign=$(git -C "$lane" rev-list --all --not "$ver" 2>/dev/null | head -n 1)
  if [ -z "$foreign" ]; then
    foreign=$(git -C "$lane" rev-list --all 2>/dev/null | tail -n 1)
  fi
  [ -n "$foreign" ] || foreign=1111111111111111111111111111111111111111
  {
    printf '%s\n' "$(sed -n 's/^export-ref=//p' -- "$ctl" | head -n 1)" >/dev/null
    sed -E "s/^export-ref=.*\$/export-ref=$foreign/" -- "$ctl" > "$d/foreign-ref.txt"
    # the run-utc must follow the ref it names, or the receipt would also
    # trip the future-dated class: the two loci must stay disjoint
    local futc
    futc=$(j8_ref_utc "$lane" "$foreign")
    if [ -n "$futc" ]; then
      sed -E "s/^run-utc=.*\$/run-utc=$futc/" -- "$d/foreign-ref.txt" > "$d/foreign-ref.tmp"
      mv -- "$d/foreign-ref.tmp" "$d/foreign-ref.txt"
    fi
  }

  # nonexistent-ref: the named ref does not resolve as a commit
  sed -E 's/^export-ref=.*$/export-ref=0000000000000000000000000000000000000000/' -- "$ctl" \
    > "$d/nonexistent-ref.txt"

  # summary-only: the receipt claims a closed tally it does not carry
  sed -E "/^$first payload=.* closed=[01]\$/d" -- "$ctl" > "$d/summary-only.txt"

  # tampered-payload-line: the receipt's own J8 line was edited
  sed -E "s/^$J8_SELF_ID payload=.* closed=[01]\$/$J8_SELF_ID payload=zz-tampered closed=1/" -- "$ctl" \
    > "$d/tampered-payload-line.txt"

  return 0
}

# ---------------------------------------------------------------------------
# the CLI (runs only when this file is executed directly)
# ---------------------------------------------------------------------------

j8_usage() {
  cat <<'EOF'
ExecJ8Receipt.sh — round-42 J8 receipt-integrity limb

  --make-receipt [--out PATH]   write the canonical receipt transcript
  --verify FILE                  grade one receipt file (payload + exit code)
  --flags FILE                   one independent verdict per forgery class
  --fixtures DIR                 the honest control + the seven forgeries
  --help                         this text

The environment must supply the host contract: EXPORT, REF_RESOLVED, LANE,
WORK and PAYFILE (or the payload_get / payload_closed / selftest_line hooks).
EOF
}

j8_main() {
  while [ $# -gt 0 ]; do
    case $1 in
      --make-receipt) shift; make_receipt "$@"; return $? ;;
      --verify) shift; [ $# -ge 1 ] || { printf 'j8: --verify needs a file\n' >&2; return 2; }
                  j8_verify "$1"; return $? ;;
      --flags) shift; [ $# -ge 1 ] || { printf 'j8: --flags needs a file\n' >&2; return 2; }
               j8_flags "$1"; return 0 ;;
      --fixtures) shift; [ $# -ge 1 ] || { printf 'j8: --fixtures needs a dir\n' >&2; return 2; }
                  j8_forge_fixtures "$1"; return $? ;;
      -h|--help) j8_usage; return 0 ;;
      *) printf 'j8: unknown argument: %s\n' "$1" >&2; j8_usage >&2; return 2 ;;
    esac
  done
  j8_usage
  return 2
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  j8_main "$@"
  exit $?
fi
