#!/usr/bin/env bash
# h5-replica.sh — independent replica of the round-40 H5 limb, written by seat
# ExecMistakesDraft because corpus/instruments/r40-closure.sh did not exist at
# this seat's run time. This is NOT the committed instrument; it implements the
# frozen H5 shape ("a tampered receipt — recorded payload contradicting the
# export, or future-dated run-utc — is REJECTED") so the ability to fail can be
# demonstrated today with the real round-39 receipts.
#
#   h5-replica.sh --lane <lane-repo> --export-ref <hash> \
#                 {--receipt <file> | --receipt-ref <hash>:<path>} \
#                 [--contained-in <hash>]
#
# Limbs, each re-derived from the export tree or from git metadata (the
# receipt's own claim is the value under test, never the source of truth):
#   version  receipt line 1 is `all-gates v<N>`
#   xref     receipt `export-ref=` equals the export under test
#   digest   receipt `suite-sha256=` equals sha256 of the export's
#            corpus/instruments/r39-closure.sh
#   declared receipt `G1 payload=declared=<n>` equals the line count of
#            .ufo/waves/round-39/declared-blocks.txt in the export
#   dated    export commit time <= receipt run-utc <= containing commit time
# closed=1 only when every limb passes; exit 0 iff closed=1.
set -u

lane='' export_ref='' receipt='' receipt_ref='' contained_in=''
while [ $# -gt 0 ]; do
  case $1 in
    --lane) lane=$2; shift 2 ;;
    --export-ref) export_ref=$2; shift 2 ;;
    --receipt) receipt=$2; shift 2 ;;
    --receipt-ref) receipt_ref=$2; shift 2 ;;
    --contained-in) contained_in=$2; shift 2 ;;
    *) printf 'h5-replica: unknown argument %s\n' "$1" >&2; exit 2 ;;
  esac
done
[ -n "$lane" ] && [ -n "$export_ref" ] || {
  printf 'usage: h5-replica.sh --lane REPO --export-ref REF (--receipt FILE | --receipt-ref REF:PATH) [--contained-in REF]\n' >&2
  exit 2; }

tmp=''
trap '[ -n "$tmp" ] && rm -f -- "$tmp"' EXIT
if [ -n "$receipt_ref" ]; then
  tmp=$(mktemp) || exit 2
  git -C "$lane" show "$receipt_ref" > "$tmp" 2>/dev/null || {
    printf 'H5 payload=receipt=0 closed=0\n'; exit 1; }
  receipt=$tmp
fi
[ -n "$receipt" ] && [ -r "$receipt" ] || { printf 'H5 payload=receipt=0 closed=0\n'; exit 1; }
[ -n "$contained_in" ] || contained_in=$export_ref

ref_full=$(git -C "$lane" rev-parse --verify --quiet "$export_ref^{commit}") || {
  printf 'H5 payload=export-ref=0 closed=0\n'; exit 1; }
cont_full=$(git -C "$lane" rev-parse --verify --quiet "$contained_in^{commit}") || cont_full=$ref_full

hdr() { sed -n "s/^$1=//p" "$receipt" | head -1; }

ver=0
case $(head -1 "$receipt") in all-gates\ v[0-9]*) ver=1 ;; esac

rec_xref_full=$(hdr export-ref)
[ -n "$rec_xref_full" ] && rec_xref_full=$(git -C "$lane" rev-parse --verify --quiet "$rec_xref_full^{commit}" 2>/dev/null || printf '%s' "$rec_xref_full")
xref=0
[ "$rec_xref_full" = "$ref_full" ] && xref=1

rec_digest=$(hdr suite-sha256)
export_digest=$(git -C "$lane" show "$ref_full:corpus/instruments/r39-closure.sh" 2>/dev/null | sha256sum | cut -d' ' -f1)
digest=0
[ -n "$rec_digest" ] && [ "$rec_digest" = "$export_digest" ] && digest=1

rec_declared=$(sed -n 's/.*G1 payload=\([^ ]*\) closed=.*/\1/p' "$receipt" | head -1 | tr ',' '\n' | sed -n 's/^declared=//p')
export_declared=$(git -C "$lane" show "$ref_full:.ufo/waves/round-39/declared-blocks.txt" 2>/dev/null | wc -l | tr -d ' ')
[ -z "$export_declared" ] && export_declared=0
declared=0
[ -n "$rec_declared" ] && [ "$rec_declared" = "$export_declared" ] && declared=1

run_s=$(hdr run-utc)
dated=absent
if [ -n "$run_s" ]; then
  if run_epoch=$(date -u -d "$run_s" +%s 2>/dev/null); then
    ref_ct=$(git -C "$lane" log -1 --format=%ct "$ref_full")
    cont_ct=$(git -C "$lane" log -1 --format=%ct "$cont_full")
    if [ "$run_epoch" -gt "$cont_ct" ]; then dated=future
    elif [ "$run_epoch" -lt "$ref_ct" ]; then dated=pre-export
    else dated=ok; fi
  else
    dated=unparseable
  fi
fi

closed=0
[ "$ver" -eq 1 ] && [ "$xref" -eq 1 ] && [ "$digest" -eq 1 ] \
  && [ "$declared" -eq 1 ] && [ "$dated" = ok ] && closed=1

printf 'H5 payload=version=%s,xref=%s,digest=%s,declared=%s(recorded=%s,export=%s),run-utc=%s,dated=%s closed=%s\n' \
  "$ver" "$xref" "$digest" "$declared" "${rec_declared:-none}" "$export_declared" "${run_s:-none}" "$dated" "$closed"
[ "$closed" -eq 1 ] && exit 0
exit 1
