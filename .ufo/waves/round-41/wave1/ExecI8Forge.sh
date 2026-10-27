#!/usr/bin/env bash
# ExecI8Forge.sh — I8 per-variant receipt-forgery detector (sourceable limb).
#
# WHAT THIS IS
# A sourceable bash limb that decides, for a receipt file, SIX INDEPENDENT
# forgery verdicts — one per forgery variant:
#
#   payload-contradicting   a recorded per-check payload contradicts the
#                           export-derived truth for that same check
#   future-dated            the recorded run-utc post-dates the verification
#                           clock, or post-dates its own ref's committer
#                           instant
#   foreign-ref             the named export-ref resolves, but that ref's
#                           tree is not this export's tree (the receipt was
#                           assembled from a different ref's run)
#   nonexistent-ref         the named export-ref does not resolve as a commit
#   summary-only            the receipt claims a closed tally but carries
#                           fewer per-check payload lines than that tally
#                           declares
#   tampered-payload-line   the self-referential verifier line (the check that
#                           verifies the receipt) records a value that differs
#                           from the export-derived value for that check
#
# WHY THE FLAGS ARE PER-VARIANT (the MutH1H5 count-relative class)
# The round-40 H5 limb decided "forged-payload=rejected" by comparing COUNTS:
# `payload_matches(forged) < control`. A count comparison is relative: an
# unrelated mutation that already perturbs the count makes the same forgery
# look accepted (round-40 wave-2, MutH1H5 observation 1: the H3 mutation drove
# the count to 8/8 and H5 then printed `forged-payload=accepted`). That class
# is forbidden here.
#
# Every flag below is decided by ONE ABSOLUTE PREDICATE over the receipt's
# own bytes and the independently derived facts. No flag is decided by
# comparing a count in one artifact against a count in another artifact, and
# no flag is decided by "the number of mismatches went down". Each variant
# owns a distinct locus in the receipt:
#
#   payload-contradicting  -> the VALUE recorded for a content check
#   tampered-payload-line  -> the VALUE recorded for the self check
#   future-dated           -> the run-utc instant
#   foreign-ref            -> the named ref's BINDING to this export tree
#   nonexistent-ref        -> the named ref's EXISTENCE
#   summary-only           -> the receipt's own declared tally vs its own body
#
# The two value flags are disjoint by CHECK ID (content checks vs the self
# check), so a receipt carrying two independent defects raises two flags, and
# a receipt carrying one defect raises exactly one.
#
# VERIFICATION INPUTS
#   --receipt FILE   the receipt under test
#   --fresh FILE     a freshly teed comparison run (the canonical transcript
#                    of a suite run over the export under test). Supplies the
#                    export-derived truth for every per-check payload.
#   --export DIR     the export tree. Supplies export-tree facts: the suite
#                    bytes' digest, the presence and bytes of the receipt
#                    inside the export, and (with --lane) the ref instant.
#   --lane DIR       the lane repo (read-only git reads: commit resolution,
#                    committer instants, ancestry and name-only diff).
#   --ref HASH       the ref that was exported (the verification ref).
#   --self-id ID     the id of the self-referential verifier check
#                    (H7 in round 40). Its payload line is the one a
#                    "tampered-payload-line" forgery targets.
#   --ids "A B C"    optional explicit list of check ids; default = every id
#                    present in the fresh comparison run.
#   --receipt-rel P  the receipt's path inside the export (used for the
#                    foreign-ref binding check).
#   --suite-rel P    the suite's path inside the export.
#   --now ISO        optional verification clock (default: the wall clock).
#
# OUTPUT (stdout)
#   I8 variant=<name> flag=<0|1> <evidence...>      (one line per variant)
#   I8 facts=<k=v,...>                             (non-verdict evidence)
#   I8 verdict=clean|forged flags=<n>/6 variants=<names>
# Exit 0 when no variant is flagged, 1 when at least one is, 2 on a harness
# error (unreadable input, unreadable export, unresolvable ref).
#
# SOURCEABLE: sourcing this file only defines functions. It runs the CLI
# only when executed directly.

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

# i8_kv_get STR KEY — value of `KEY=` in a comma-joined k=v payload string.
i8_kv_get() { # STR KEY
  printf '%s\n' "$1" | tr ',' '\n' | sed -n "s/^$2=//p" | head -n 1
}

# i8_recorded_payload FILE ID — the payload value recorded for ID in a
# transcript, or the empty string when the transcript carries no line for ID.
i8_recorded_payload() { # FILE ID
  [ -f "$1" ] || return 0
  sed -n "s/^$2 payload=\(.*\) closed=[01]\$/\1/p" -- "$1" | head -n 1
}

# i8_transcript_ids FILE — the check ids that carry a payload line, in order.
i8_transcript_ids() { # FILE
  [ -f "$1" ] || return 0
  sed -n 's/^\([A-Za-z0-9_]\{1,\}\) payload=.* closed=[01]$/\1/p' -- "$1"
}

# i8_ref_utc LANE REF — the committer instant of REF as
# `YYYY-MM-DDTHH:MM:SSZ`, or the empty string when REF cannot be read.
i8_ref_utc() { # LANE REF
  local lane=$1 ref=$2 e
  [ -n "$ref" ] || return 0
  e=$(git --no-optional-locks -C "$lane" log -1 --format=%ct "$ref" 2>/dev/null) || return 0
  case $e in ''|*[!0-9]*) return 0 ;; esac
  TZ=UTC date -u -d "@$e" +%Y-%m-%dT%H:%M:%SZ
}

# i8_iso_epoch ISO — the epoch seconds of an ISO-8601 UTC instant, or empty.
i8_iso_epoch() { # ISO
  local iso=$1 n
  case $iso in
    [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z) ;;
    *) return 0 ;;
  esac
  n=$(date -u -d "$iso" +%s 2>/dev/null) || return 0
  case $n in ''|*[!0-9]*) return 0 ;; esac
  printf '%s' "$n"
}

# i8_digest FILE — sha256 of FILE, or `unreadable`.
i8_digest() { # FILE
  local f=$1
  if [ -z "$f" ] || [ ! -r "$f" ]; then printf 'unreadable'; return 0; fi
  sha256sum -- "$f" | awk '{print $1; exit}'
}

# ---------------------------------------------------------------------------
# the detector
# ---------------------------------------------------------------------------

# i8_detect_receipt_forgery ARGS... — see the header for the flags.
# Prints the six verdict lines, a facts line and a verdict line.
i8_detect_receipt_forgery() {
  local receipt='' fresh='' export='' lane='' vref='' self_id=''
  local ids='' receipt_rel='' suite_rel='' now_iso='' skew=120
  local fr ru ru_epoch now_epoch fr_utc fr_utc_epoch
  local v_payload=0 v_future=0 v_foreign=0 v_nonexist=0 v_summary=0 v_tampered=0
  local v_payload_ids='' v_tampered_ids='' v_summary_detail='' v_foreign_detail=''
  local v_future_detail='' v_nonexist_detail='' facts='' ids_list='' id
  local rec fresh_v closed_line declared_n body_n exp_digest rec_digest
  local export_receipt_path=''

  while [ $# -gt 0 ]; do
    case $1 in
      --receipt)    receipt=${2:-}; shift 2 ;;
      --fresh)      fresh=${2:-}; shift 2 ;;
      --export)     export=${2:-}; shift 2 ;;
      --lane)       lane=${2:-}; shift 2 ;;
      --ref)        vref=${2:-}; shift 2 ;;
      --self-id)    self_id=${2:-}; shift 2 ;;
      --ids)        ids=${2:-}; shift 2 ;;
      --receipt-rel) receipt_rel=${2:-}; shift 2 ;;
      --suite-rel)  suite_rel=${2:-}; shift 2 ;;
      --now)        now_iso=${2:-}; shift 2 ;;
      --skew)       skew=${2:-}; shift 2 ;;
      *) printf 'i8: unknown argument: %s\n' "$1" >&2; return 2 ;;
    esac
  done

  [ -n "$receipt" ] || { printf 'i8: --receipt is required\n' >&2; return 2; }
  [ -f "$receipt" ] && [ -r "$receipt" ] || { printf 'i8: receipt unreadable: %s\n' "$receipt" >&2; return 2; }
  [ -n "$fresh" ] || { printf 'i8: --fresh is required\n' >&2; return 2; }
  [ -f "$fresh" ] && [ -r "$fresh" ] || { printf 'i8: fresh comparison run unreadable: %s\n' "$fresh" >&2; return 2; }
  [ -n "$export" ] && [ -d "$export" ] || { printf 'i8: --export is required\n' >&2; return 2; }
  [ -n "$lane" ] && [ -d "$lane" ] || { printf 'i8: --lane is required\n' >&2; return 2; }
  [ -n "$vref" ] || { printf 'i8: --ref is required\n' >&2; return 2; }
  git --no-optional-locks -C "$lane" cat-file -e "${vref}^{commit}" 2>/dev/null \
    || { printf 'i8: --ref does not resolve: %s\n' "$vref" >&2; return 2; }

  # ---- export-tree facts -------------------------------------------------
  # The export tree is the ground truth for what the receipt may claim. The
  # suite bytes it carries are what the receipt's recorded suite-sha256 must
  # equal; a receipt that records a different digest was produced by a
  # different instrument and its recorded values contradict this export.
  if [ -n "$suite_rel" ] && [ -f "$export/$suite_rel" ]; then
    exp_digest=$(i8_digest "$export/$suite_rel")
  else
    exp_digest=absent
  fi
  rec_digest=$(sed -n 's/^suite-sha256=//p' -- "$receipt" | head -n 1)
  [ -n "$rec_digest" ] || rec_digest=absent
  # The fresh comparison run records the digest of the instrument it ran.
  # It must be the digest of the instrument THIS export carries; otherwise
  # the fresh run is not a re-run of this export and cannot serve as the
  # export-derived truth for the comparison. Fail closed on that mismatch.
  fresh_digest=$(sed -n 's/^suite-sha256=//p' -- "$fresh" | head -n 1)
  [ -n "$fresh_digest" ] || fresh_digest=absent
  if [ "$exp_digest" = absent ] || [ "$fresh_digest" = absent ] \
     || [ "$exp_digest" != "$fresh_digest" ]; then
    printf 'i8: the fresh comparison run is not a re-run of this export (export=%s fresh=%s)\n' \
      "$exp_digest" "$fresh_digest" >&2
    return 2
  fi
  # The fresh run names the ref it was teed at. That ref's tree must differ
  # from the exported tree by exactly the receipt — the same binding the
  # receipt itself must satisfy. A fresh run taken over a DIFFERENT tree
  # (even one carrying the same instrument bytes) is not this export's
  # truth; fail closed rather than compare against a foreign truth.
  fresh_ref=$(sed -n 's/^export-ref=//p' -- "$fresh" | head -n 1)
  fresh_ref_n=$(sed -n 's/^export-ref=//p' -- "$fresh" | grep -c .)
  if [ "$fresh_ref_n" -ne 1 ] || ! printf '%s' "$fresh_ref" | grep -Eq '^[0-9a-f]{40}$' \
     || ! git --no-optional-locks -C "$lane" cat-file -e "${fresh_ref}^{commit}" 2>/dev/null; then
    printf 'i8: the fresh comparison run names no resolvable export-ref\n' >&2
    return 2
  fi
  fresh_changed=$(git --no-optional-locks -C "$lane" diff --name-only "$fresh_ref" "$vref" 2>/dev/null)
  fresh_changed_n=$(printf '%s\n' "$fresh_changed" | grep -c .)
  if [ -n "$receipt_rel" ]; then
    fresh_bound=0
    [ "$fresh_changed_n" -eq 1 ] && [ "$fresh_changed" = "$receipt_rel" ] && fresh_bound=1
  else
    fresh_bound=0
    [ "$fresh_changed_n" -eq 0 ] && fresh_bound=1
  fi
  if [ "$fresh_bound" -ne 1 ]; then
    printf 'i8: the fresh comparison run is not bound to this export (fresh-ref=%s diff-paths=%s)\n' \
      "$fresh_ref" "$fresh_changed_n" >&2
    return 2
  fi
  # The recorded suite digest is a value the receipt claims about this export.
  # When the export carries different instrument bytes, that recorded value
  # contradicts the export, and the receipt's per-check values were produced
  # by an instrument that is not this one.
  if [ "$rec_digest" != absent ] && [ "$rec_digest" != "$exp_digest" ]; then
    v_payload=1
    v_payload_ids="${v_payload_ids}${v_payload_ids:+,}suite-sha256"
  fi

  # ---- the receipt's own header -----------------------------------------
  # A receipt names exactly one export-ref. Zero, several, or a malformed one
  # cannot bind to any tree: that is the nonexistent-ref defect.
  fr=$(sed -n 's/^export-ref=//p' -- "$receipt")
  fr_n=$(printf '%s\n' "$fr" | grep -c .)
  fr=$(printf '%s\n' "$fr" | head -n 1)
  if [ "$fr_n" -ne 1 ] || ! printf '%s' "$fr" | grep -Eq '^[0-9a-f]{40}$' \
     || ! git --no-optional-locks -C "$lane" cat-file -e "${fr}^{commit}" 2>/dev/null; then
    v_nonexist=1
    v_nonexist_detail="named-ref=${fr:-none} resolves=no"
  fi

  ru=$(sed -n 's/^run-utc=//p' -- "$receipt" | head -n 1)
  ru_epoch=$(i8_iso_epoch "$ru")
  now_iso=${now_iso:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}
  now_epoch=$(i8_iso_epoch "$now_iso")
  if [ -n "$ru_epoch" ] && [ -n "$now_epoch" ]; then
    if [ "$ru_epoch" -gt $((now_epoch + skew)) ]; then
      v_future=1
      v_future_detail="run-utc=$ru after-clock=$now_iso"
    elif [ "$v_nonexist" -eq 0 ]; then
      # A receipt cannot be teed after the commit it names: the run-utc is
      # the ref's committer instant (time-basis=ref-commit).
      fr_utc=$(i8_ref_utc "$lane" "$fr")
      fr_utc_epoch=$(i8_iso_epoch "$fr_utc")
      if [ -n "$fr_utc_epoch" ] && [ "$ru_epoch" -gt "$fr_utc_epoch" ]; then
        v_future=1
        v_future_detail="run-utc=$ru after-ref-committer=$fr_utc"
      fi
    fi
  else
    v_future_detail="run-utc=${ru:-none} unparseable=yes"
  fi

  # ---- foreign-ref: the named ref must BIND to this export tree ---------
  # The receipt names the ref it was teed at; that ref's tree must differ
  # from the exported tree by exactly the receipt itself. A ref from another
  # run (or another history) breaks that binding even when every recorded
  # payload happens to be true of this tree.
  if [ "$v_nonexist" -eq 0 ]; then
    if ! git --no-optional-locks -C "$lane" merge-base --is-ancestor "$fr" "$vref" 2>/dev/null; then
      v_foreign=1
      v_foreign_detail="named-ref=$fr not-ancestor-of=$vref"
    else
      changed=$(git --no-optional-locks -C "$lane" diff --name-only "$fr" "$vref" 2>/dev/null)
      changed_n=$(printf '%s\n' "$changed" | grep -c .)
      if [ -n "$receipt_rel" ]; then
        if [ "$changed_n" -ne 1 ] || [ "$changed" != "$receipt_rel" ]; then
          v_foreign=1
          v_foreign_detail="named-ref=$fr diff-paths=$changed_n expected=1($receipt_rel)"
        fi
      else
        if [ "$changed_n" -ne 0 ]; then
          v_foreign=1
          v_foreign_detail="named-ref=$fr diff-paths=$changed_n expected=0"
        fi
      fi
    fi
  fi

  # ---- summary-only: the receipt's body against the expected check count -
  # Absolute, and cross-bound to the fresh comparison run: the receipt
  # declares `closed=K/N exit=...` and the fresh run of the same export
  # carries N per-check payload lines. A summary-only receipt carries fewer
  # per-check payload lines than that expected count. The comparison is
  # receipt-body vs expected-count — never vs a count taken from another
  # receipt, so an unrelated defect cannot mask this one.
  closed_line=$(grep -cE '^closed=[0-9]+/[0-9]+ exit=[01]$' -- "$receipt" 2>/dev/null)
  closed_line=${closed_line:-0}
  declared_n=$(sed -n 's/^closed=[0-9]*\/\([0-9]\+\) exit=[01]$/\1/p' -- "$receipt" | head -n 1)
  body_n=$(grep -cE '^[A-Za-z0-9_]+ payload=.* closed=[01]$' -- "$receipt" 2>/dev/null)
  body_n=${body_n:-0}
  fresh_body_n=$(i8_transcript_ids "$fresh" | grep -c .)
  fresh_body_n=${fresh_body_n:-0}
  expected_n=$fresh_body_n
  [ -n "$declared_n" ] && [ "$declared_n" -gt "$expected_n" ] && expected_n=$declared_n
  if [ "$closed_line" -ge 1 ]; then
    if [ -z "$declared_n" ] && [ "$fresh_body_n" -eq 0 ]; then
      v_summary=1
      v_summary_detail="tally=unreadable body-lines=$body_n"
    elif [ "$body_n" -lt "$expected_n" ]; then
      v_summary=1
      v_summary_detail="expected=$expected_n body-lines=$body_n declared=${declared_n:-none} fresh-checks=$fresh_body_n"
    fi
  fi

  # ---- per-check value comparison against the export-derived truth ------
  # The fresh comparison run is the export-derived truth: the same export,
  # re-run and re-teed. Each check's recorded value is compared with that
  # check's fresh value, id by id. Content ids and the self id are disjoint
  # loci, so a payload forgery and a tampered self line cannot mask or
  # impersonate each other.
  if [ -n "$ids" ]; then
    ids_list=$ids
  else
    ids_list=$(i8_transcript_ids "$fresh" | tr '\n' ' ')
  fi
  for id in $ids_list; do
    [ "$id" = "$self_id" ] && continue
    fresh_v=$(i8_recorded_payload "$fresh" "$id")
    rec=$(i8_recorded_payload "$receipt" "$id")
    [ -n "$rec" ] || continue
    if [ "$rec" != "$fresh_v" ]; then
      v_payload=1
      v_payload_ids="${v_payload_ids}${v_payload_ids:+,}$id"
    fi
  done
  # the self id: its own line is the one a tampered-payload-line forgery
  # rewrites; it is compared with the fresh value for that same id.
  if [ -n "$self_id" ]; then
    fresh_v=$(i8_recorded_payload "$fresh" "$self_id")
    rec=$(i8_recorded_payload "$receipt" "$self_id")
    if [ -n "$rec" ] && [ "$rec" != "$fresh_v" ]; then
      v_tampered=1
      v_tampered_ids=$self_id
    fi
  fi

  # ---- facts (evidence, not verdict) ------------------------------------
  export_receipt_path=absent
  if [ -n "$receipt_rel" ] && [ -f "$export/$receipt_rel" ]; then
    export_receipt_path=$(i8_digest "$export/$receipt_rel")
  fi
  facts="named-ref=${fr:-none} named-ref-committer=$(i8_ref_utc "$lane" "$fr" 2>/dev/null)"
  facts="$facts exported-ref=$vref exported-ref-committer=$(i8_ref_utc "$lane" "$vref")"
  facts="$facts receipt-suite-sha256=$rec_digest export-suite-sha256=$exp_digest"
  facts="$facts export-receipt-sha256=$export_receipt_path body-lines=$body_n declared=$declared_n"
  facts="$facts run-utc=${ru:-none} now=$now_iso"

  # ---- output ------------------------------------------------------------
  printf 'I8 variant=payload-contradicting flag=%s ids=%s\n' \
    "$([ "$v_payload" -eq 1 ] && echo 1 || echo 0)" "${v_payload_ids:--}"
  printf 'I8 variant=future-dated flag=%s detail=%s\n' \
    "$([ "$v_future" -eq 1 ] && echo 1 || echo 0)" "${v_future_detail:-in-window}"
  printf 'I8 variant=foreign-ref flag=%s detail=%s\n' \
    "$([ "$v_foreign" -eq 1 ] && echo 1 || echo 0)" "${v_foreign_detail:-binds}"
  printf 'I8 variant=nonexistent-ref flag=%s detail=%s\n' \
    "$([ "$v_nonexist" -eq 1 ] && echo 1 || echo 0)" "${v_nonexist_detail:-resolves}"
  printf 'I8 variant=summary-only flag=%s detail=%s\n' \
    "$([ "$v_summary" -eq 1 ] && echo 1 || echo 0)" "${v_summary_detail:-complete-body}"
  printf 'I8 variant=tampered-payload-line flag=%s ids=%s\n' \
    "$([ "$v_tampered" -eq 1 ] && echo 1 || echo 0)" "${v_tampered_ids:--}"
  printf 'I8 facts=%s\n' "$facts"

  nflag=$((v_payload + v_future + v_foreign + v_nonexist + v_summary + v_tampered))
  names=''
  [ "$v_payload" -eq 1 ]   && names="${names}${names:+,}payload-contradicting"
  [ "$v_future" -eq 1 ]    && names="${names}${names:+,}future-dated"
  [ "$v_foreign" -eq 1 ]   && names="${names}${names:+,}foreign-ref"
  [ "$v_nonexist" -eq 1 ]  && names="${names}${names:+,}nonexistent-ref"
  [ "$v_summary" -eq 1 ]   && names="${names}${names:+,}summary-only"
  [ "$v_tampered" -eq 1 ]  && names="${names}${names:+,}tampered-payload-line"
  if [ "$nflag" -eq 0 ]; then
    printf 'I8 verdict=clean flags=0/6 variants=-\n'
    return 0
  fi
  printf 'I8 verdict=forged flags=%s/6 variants=%s\n' "$nflag" "$names"
  return 1
}

# i8_usage — the CLI help.
i8_usage() {
  cat <<'EOF'
usage: i8_detect_receipt_forgery --receipt FILE --fresh FILE --export DIR
           --lane DIR --ref HASH [--self-id ID] [--ids "A B"] [--receipt-rel P]
           [--suite-rel P] [--now ISO] [--skew SEC]
EOF
}

# i8_main ARGS... — the CLI wrapper (runs only when executed directly).
i8_main() {
  case ${1:-} in
    -h|--help) i8_usage; return 0 ;;
  esac
  i8_detect_receipt_forgery "$@"
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  i8_main "$@"
fi
