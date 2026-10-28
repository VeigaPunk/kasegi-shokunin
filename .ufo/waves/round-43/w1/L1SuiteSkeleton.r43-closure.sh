#!/usr/bin/env bash
# r43-closure.sh -- the round-43 closure suite (export mode only).
#
#   r43-closure.sh --export-ref <hash> [--lane DIR] [--work DIR]
#                   [--scratch-root DIR] [--receipt-out PATH] [--only K1,K14]
#   r43-closure.sh --selftest --export-ref <hash> [same options]
#   r43-closure.sh --export-ref <hash> ... --leaf     (nested depth-1 run)
#
# A plain invocation (no --export-ref) refuses with exit 2: the suite only ever
# grades an exported tree, never a working tree.  The export is produced with
#     git -C <lane> archive <hash> | tar -x -C <work>/export
# A ref that does not resolve prints `ref-not-found` and exits 1: an
# unresolvable ref is a red, never a vacuous pass.
#
# Composition.  K1-K7 and K9-K13 carry the round-42 suite's J1-J7 and J9-J13
# checks verbatim by invoking its committed bytes inside the export and
# re-emitting each `J<n> payload=...` line as `K<n> payload=...`; the round-42
# J8 is NOT carried because its receipt path is the round-42 receipt, which the
# round-43 tree legitimately invalidates.  K8 is the round-43 receipt check with
# the same payload grammar (receipt/ref/digest/time-basis/utc/one-run/
# payload-match/forged/selftest-lines/summary/closed-line).  K14-K19 are the
# round-43 narrative-evidence checks, sourced from corpus/instruments/r43-limbs/.
#
# The run transcript is
#     all-gates v3
#     export-ref=<40 hex>
#     suite-sha256=<64 hex>
#     time-basis=ref-commit
#     run-utc=<ISO 8601 Z>
#     K<n> payload=... closed=0|1     (nineteen lines, K1..K19)
#     closed=<n>/19 exit=0|1
# The receipt written by --receipt-out is that transcript followed by the
# nineteen graded selftest lines and the `selftest cases=19 failures=<k>` line.
#
# Exit status: 0 only when all nineteen checks are closed (0 selftest failures
# in --selftest mode); 1 when any is open; 2 on a usage error.

set -uo pipefail

LANE="${R43_LANE_DEFAULT:-/home/vgpnk/Projects/shokunin/kasegi-shokunin}"
WORK=""
SCRATCH_ROOT=""
EXPORT_REF=""
RECEIPT_OUT=""
RECEIPT_OVERRIDE=""
MODE="run"
LEAF=0
ONLY=""

RECEIPT_REL=".ufo/waves/round-43/final-gates/all-gates.txt"
LIMB_REL="corpus/instruments/r43-limbs"
CARRIED_REL="corpus/instruments/r42-closure.sh"

usage() {
    sed -n '2,34p' "$0" | sed 's/^# \{0,1\}//'
    exit 2
}

while [ $# -gt 0 ]; do
    case "$1" in
        --export-ref) EXPORT_REF="${2:-}"; shift 2 ;;
        --lane) LANE="${2:-}"; shift 2 ;;
        --work) WORK="${2:-}"; shift 2 ;;
        --scratch-root) SCRATCH_ROOT="${2:-}"; shift 2 ;;
        --receipt-out) RECEIPT_OUT="${2:-}"; shift 2 ;;
        --receipt) RECEIPT_OVERRIDE="${2:-}"; shift 2 ;;
        --only) ONLY="${2:-}"; shift 2 ;;
        --selftest) MODE="selftest"; shift ;;
        --leaf) LEAF=1; shift ;;
        -h|--help) usage ;;
        *) printf 'r43-closure: unknown argument: %s\n' "$1" >&2; exit 2 ;;
    esac
done

if [ -z "$EXPORT_REF" ]; then
    printf 'r43-closure: a plain run is refused (export mode only); pass --export-ref <hash>\n' >&2
    exit 2
fi

[ -n "$WORK" ] || WORK="$(mktemp -d "${TMPDIR:-/tmp}/r43-work.XXXXXX")"
[ -n "$SCRATCH_ROOT" ] || SCRATCH_ROOT="$WORK/scratch"
mkdir -p "$WORK" "$SCRATCH_ROOT" || exit 2

FULL="$(git -C "$LANE" rev-parse --verify "${EXPORT_REF}^{commit}" 2>/dev/null)" || {
    printf 'ERROR ref-not-found ref=%s closed=0 exit=1\n' "$EXPORT_REF" >&2
    exit 1
}

if [ -n "${UFO_R43_SELFDIR:-}" ]; then
    SUITE_SRC="$UFO_R43_SELFDIR"
else
    SUITE_SRC="$0"
fi

run_utc() { date -u +%Y-%m-%dT%H:%M:%SZ; }
suite_sha() { sha256sum "$1" | cut -d' ' -f1; }

# ---------------------------------------------------------------------------
# export
# ---------------------------------------------------------------------------
EXPORT="$WORK/export"
rm -rf "$EXPORT"; mkdir -p "$EXPORT" || exit 2
if ! git -C "$LANE" archive "$FULL" | tar -x -C "$EXPORT" 2>"$WORK/export.err"; then
    printf 'ERROR export-failed ref=%s closed=0 exit=1\n' "$FULL" >&2
    cat "$WORK/export.err" >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# K1-K7, K9-K13 -- carried r42 checks, invoked from the export's own bytes
# ---------------------------------------------------------------------------
CARRIED_OUT="$WORK/carried.out"
CARRIED_RC=0
if [ -f "$EXPORT/$CARRIED_REL" ]; then
    bash "$EXPORT/$CARRIED_REL" --export-ref "$FULL" --lane "$LANE" \
        --work "$WORK/carried" --scratch-root "$SCRATCH_ROOT/carried" \
        >"$CARRIED_OUT" 2>"$WORK/carried.err"
    CARRIED_RC=$?
else
    : >"$CARRIED_OUT"
    CARRIED_RC=127
fi

carried_line() {  # carried_line <n> -> "payload=... closed=<c>" or ""
    awk -v n="$1" '
        $1 == "J" n { sub(/^J[0-9]+ /, ""); print; found=1 }
        END { if (!found) exit 1 }
    ' "$CARRIED_OUT"
}

# ---------------------------------------------------------------------------
# K8 -- round-43 receipt integrity
# ---------------------------------------------------------------------------
receipt_path() {
    if [ -n "$RECEIPT_OVERRIDE" ]; then
        printf '%s\n' "$RECEIPT_OVERRIDE"
    else
        printf '%s\n' "$EXPORT/$RECEIPT_REL"
    fi
}

check_k8() {  # check_k8 <payload-file-with-K-lines>  -> prints one K8 line
    local pfile="$1" r p head ref_line digest tb utc one selft closed summary hdr dg
    r="$(receipt_path)"
    if [ ! -f "$r" ]; then
        printf 'K8 payload=receipt=%s,source=absent,header=0,ref=0,digest=0,time-basis=0,utc=0,one-run=0,payload-match=0/0,forged=0/0,selftest-lines=0,summary=0,closed-line=0 closed=0\n' "$RECEIPT_REL"
        return 1
    fi
    hdr=$(grep -c '^all-gates v' "$r")
    ref_line=$(grep -m1 '^export-ref=' "$r" | cut -d= -f2)
    digest=$(grep -m1 '^suite-sha256=' "$r" | cut -d= -f2)
    tb=$(grep -c '^time-basis=ref-commit$' "$r")
    utc=$(grep -m1 '^run-utc=' "$r" | cut -d= -f2)
    one=$(grep -c '^run-utc=' "$r")
    selft=$(grep -c '^selftest case=K[0-9]* ' "$r")
    summary=$(grep -c '^selftest cases=19 failures=0$' "$r")
    closed=$(grep -cE '^closed=(18/19 exit=1|19/19 exit=0)$' "$r")
    local ok_hdr=0 ok_ref=0 ok_dig=0 ok_tb=0 ok_utc=0 ok_one=0
    [ "$hdr" -eq 1 ] && ok_hdr=1
    [ "$ref_line" = "$FULL" ] && ok_ref=1
    dg="$(sha256sum "$EXPORT/corpus/instruments/r43-closure.sh" 2>/dev/null | cut -d' ' -f1)"
    [ -n "$dg" ] && [ "$digest" = "$dg" ] && ok_dig=1
    [ "$tb" -eq 1 ] && ok_tb=1
    if [ -n "$utc" ]; then
        local cut_ct
        cut_ct="$(git -C "$LANE" show -s --format=%cI "$FULL" 2>/dev/null)"
        if [ -n "$cut_ct" ]; then
            local ue ce
            ue="$(date -u -d "$utc" +%s 2>/dev/null)"; ce="$(date -u -d "$cut_ct" +%s 2>/dev/null)"
            [ -n "$ue" ] && [ -n "$ce" ] && [ "$ue" -le "$((ce + 1))" ] && ok_utc=1
        fi
    fi
    [ "$one" -eq 1 ] && ok_one=1
    # payload match: every K line the receipt carries, except K8, equals the
    # value this run re-derived at the same ref.
    local match=0 total=0
    while IFS= read -r line; do
        local id
        id="$(printf '%s' "$line" | sed -n 's/^\(K[0-9]*\) .*/\1/p')"
        [ -n "$id" ] || continue
        [ "$id" = "K8" ] && continue
        total=$((total + 1))
        if grep -qxF "$line" "$r"; then match=$((match + 1)); fi
    done < "$pfile"
    # forged detection: a mutant receipt with a tampered payload line, a second
    # header, or a missing summary must be rejected.  Probe it in scratch.
    local forged=0 forged_total=0
    local tmpd="$SCRATCH_ROOT/k8"
    mkdir -p "$tmpd"
    cp "$r" "$tmpd/tamper.txt"
    local victim
    victim="$(grep -m1 '^K1 payload=' "$r" || true)"
    if [ -n "$victim" ]; then
        python3 - "$tmpd/tamper.txt" "$victim" <<'PY'
import sys
path, victim = sys.argv[1], sys.argv[2]
lines = open(path).read().split("\n")
out = []
done = False
for line in lines:
    if not done and line == victim:
        out.append(line.replace("closed=", "closed=9/9 forged ", 1)
                   if "closed=" in line else line + " forged")
        done = True
    else:
        out.append(line)
open(path, "w").write("\n".join(out))
PY
        forged_total=$((forged_total + 1))
        if ! _k8_grade "$tmpd/tamper.txt" "$pfile" >/dev/null 2>&1; then forged=$((forged + 1)); fi
    fi
    cp "$r" "$tmpd/double.txt"
    printf 'all-gates v3\n' >> "$tmpd/double.txt"
    forged_total=$((forged_total + 1))
    if ! _k8_grade "$tmpd/double.txt" "$pfile" >/dev/null 2>&1; then forged=$((forged + 1)); fi
    cp "$r" "$tmpd/nosummary.txt"
    grep -v '^selftest cases=19 failures=0$' "$r" > "$tmpd/nosummary.txt"
    forged_total=$((forged_total + 1))
    if ! _k8_grade "$tmpd/nosummary.txt" "$pfile" >/dev/null 2>&1; then forged=$((forged + 1)); fi

    local src="committed"
    [ -n "$RECEIPT_OVERRIDE" ] && src="override"
    printf 'K8 payload=receipt=%s,source=%s,header=%s,ref=%s,digest=%s,time-basis=%s,utc=%s,one-run=%s,payload-match=%s/%s,forged=%s/%s,selftest-lines=%s,summary=%s,closed-line=%s closed=%s\n' \
        "$(basename "$r")" "$src" "$ok_hdr" "$ok_ref" "$ok_dig" "$ok_tb" "$ok_utc" "$ok_one" \
        "$match" "$total" "$forged" "$forged_total" "$selft" "$summary" "$closed" \
        "$( [ "$ok_hdr$ok_ref$ok_dig$ok_tb$ok_utc$ok_one" != "111111" ] && echo 0 || \
           { [ "$match" -eq "$total" ] && [ "$total" -ge 18 ] && [ "$forged" -eq "$forged_total" ] \
             && [ "$selft" -eq 19 ] && [ "$summary" -eq 1 ] && [ "$closed" -eq 1 ] && echo 1 || echo 0; } )"
    [ "$ok_hdr$ok_ref$ok_dig$ok_tb$ok_utc$ok_one" = "111111" ] || return 1
    [ "$match" -eq "$total" ] && [ "$total" -ge 18 ] && [ "$forged" -eq "$forged_total" ] \
        && [ "$selft" -eq 19 ] && [ "$summary" -eq 1 ] && [ "$closed" -eq 1 ] && return 0
    return 1
}

_k8_grade() {  # grade a receipt file against the re-derived payloads
    local r="$1" pfile="$2" hdr ref_line digest tb utc one selft summary closedd match=0 total=0
    hdr=$(grep -c '^all-gates v' "$r")
    ref_line=$(grep -m1 '^export-ref=' "$r" | cut -d= -f2)
    digest=$(grep -m1 '^suite-sha256=' "$r" | cut -d= -f2)
    tb=$(grep -c '^time-basis=ref-commit$' "$r")
    utc=$(grep -c '^run-utc=' "$r")
    one=$(grep -c '^run-utc=' "$r")
    selft=$(grep -c '^selftest case=K[0-9]* ' "$r")
    summary=$(grep -c '^selftest cases=19 failures=0$' "$r")
    closedd=$(grep -cE '^closed=(18/19 exit=1|19/19 exit=0)$' "$r")
    [ "$hdr" -eq 1 ] || return 1
    [ "$ref_line" = "$FULL" ] || return 1
    [ "$utc" -eq 1 ] && [ "$one" -eq 1 ] || return 1
    [ "$tb" -eq 1 ] || return 1
    [ "$selft" -eq 19 ] || return 1
    [ "$summary" -eq 1 ] || return 1
    [ "$closedd" -eq 1 ] || return 1
    while IFS= read -r line; do
        local id
        id="$(printf '%s' "$line" | sed -n 's/^\(K[0-9]*\) .*/\1/p')"
        [ -n "$id" ] || continue
        [ "$id" = "K8" ] && continue
        total=$((total + 1))
        grep -qxF "$line" "$r" && match=$((match + 1))
    done < "$pfile"
    [ "$match" -eq "$total" ] || return 1
    return 0
}

# ---------------------------------------------------------------------------
# K14-K19 -- narrative-evidence limbs
# ---------------------------------------------------------------------------
declare -A LIMB_FILE=(
  [K14]=k14-corrections.sh
  [K15]=k15-wave-narrative.sh
  [K16]=k16-placeholder.sh
  [K17]=k17-claims-before.sh
  [K18]=k18-transcript.sh
  [K19]=k19-freeze.sh
)
declare -A LIMB_FUNC=(
  [K14]=check_k14
  [K15]=check_k15
  [K16]=check_k16
  [K17]=check_k17
  [K18]=check_k18
  [K19]=check_k19
)

limb_line() {  # limb_line <Knn> <tree> -> prints one K<n> line, returns closed status
    local id="$1" tree="$2" f fn out rc
    f="$EXPORT/$LIMB_REL/${LIMB_FILE[$id]}"
    fn="${LIMB_FUNC[$id]}"
    if [ ! -f "$f" ]; then
        printf '%s payload=limb=absent,file=%s closed=0\n' "$id" "${LIMB_FILE[$id]}"
        return 1
    fi
    out="$(bash -c 'source "$1"; "$2" "$3"' _ "$f" "$fn" "$tree" 2>/dev/null | awk -v id="$id" '
        index($0, id " payload=") == 1 { last = $0 }
        index($0, "payload=") == 1 && last == "" { last = id " " $0 }
        END { if (last != "") print last; else exit 1 }')"
    rc=$?
    if [ "$rc" -ne 0 ] || [ -z "$out" ]; then
        printf '%s payload=limb=error,file=%s closed=0\n' "$id" "${LIMB_FILE[$id]}"
        return 1
    fi
    printf '%s\n' "$out"
    case "$out" in
        *"closed=1"*) return 0 ;;
        *) return 1 ;;
    esac
}

want() {
    [ -z "$ONLY" ] && return 0
    case ",$ONLY," in *",$1,"*) return 0 ;; esac
    return 1
}

PAYLOAD_FILE="$WORK/payloads.txt"
: > "$PAYLOAD_FILE"
OPEN=0
TOTAL=0

emit() {  # emit <id> <line> <closed>
    printf '%s\n' "$2" >> "$PAYLOAD_FILE"
    printf '%s\n' "$2"
    TOTAL=$((TOTAL + 1))
    [ "$3" -eq 1 ] || OPEN=$((OPEN + 1))
}

for n in 1 2 3 4 5 6 7 9 10 11 12 13; do
    id="K$n"
    want "$id" || continue
    cl="$(carried_line "$n")"
    if [ -z "$cl" ]; then
        emit "$id" "$id payload=carried=absent,exit=$CARRIED_RC closed=0" 0
        continue
    fi
    case "$cl" in
        *"closed=1") emit "$id" "$id $cl" 1 ;;
        *) emit "$id" "$id $cl" 0 ;;
    esac
done

if want K8; then
    k8="$(check_k8 "$PAYLOAD_FILE")"; k8rc=$?
    emit K8 "$k8" "$k8rc"
fi

for id in K14 K15 K16 K17 K18 K19; do
    want "$id" || continue
    ln="$(limb_line "$id" "$EXPORT")"; rc=$?
    emit "$id" "$ln" "$rc"
done

CLOSED=$((TOTAL - OPEN))
printf 'closed=%d/%d exit=%d\n' "$CLOSED" "$TOTAL" "$( [ "$OPEN" -eq 0 ] && echo 0 || echo 1)"
RC=$( [ "$OPEN" -eq 0 ] && echo 0 || echo 1 )

# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------
selftest_block() {
    local failures=0 line id n mut pos
    local sdir="$SCRATCH_ROOT/selftest"
    rm -rf "$sdir"; mkdir -p "$sdir"

    for n in 1 2 3 4 5 6 7 9 10 11 12 13; do
        id="K$n"
        line="$(grep -m1 "^$id " "$PAYLOAD_FILE" || true)"
        mut=0
        case "$line" in *"=rejected"*) mut=1 ;; esac
        pos=0
        case "$line" in *"closed=1"*) pos=1 ;; esac
        if [ "$pos" -eq 1 ]; then
            printf 'selftest case=%s positive=pass mutants=carried:%s verdict=pass\n' "$id" "$mut"
        else
            printf 'selftest case=%s positive=fail mutants=carried:%s verdict=fail\n' "$id" "$mut"
            failures=$((failures+1))
        fi
    done

    # K8: build a synthetic receipt from the re-derived payloads and grade it
    # accepted; then three forgeries must be rejected.
    local syn="$sdir/synth.txt" good bad tot
    {
        printf 'all-gates v3\n'
        printf 'export-ref=%s\n' "$FULL"
        printf 'suite-sha256=%s\n' "$(sha256sum "$EXPORT/corpus/instruments/r43-closure.sh" | cut -d' ' -f1)"
        printf 'time-basis=ref-commit\n'
        printf 'run-utc=2026-10-28T00:00:00Z\n'
        grep -v '^K8 ' "$PAYLOAD_FILE"
        printf 'K8 payload=receipt=synth.txt,source=override,header=1,ref=1,digest=1,time-basis=1,utc=1,one-run=1,payload-match=18/18,forged=3/3,selftest-lines=19,summary=1,closed-line=1 closed=1\n'
        printf 'closed=18/19 exit=1\n'
        for n in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19; do
            printf 'selftest case=K%s positive=pass mutants=carried:1 verdict=pass\n' "$n"
        done
        printf 'selftest cases=19 failures=0\n'
    } > "$syn"
    good=0; bad=0; tot=0
    _k8_grade "$syn" "$PAYLOAD_FILE" >/dev/null 2>&1 && good=1
    cp "$syn" "$sdir/s1.txt"; printf 'all-gates v3\n' >> "$sdir/s1.txt"
    tot=$((tot+1)); _k8_grade "$sdir/s1.txt" "$PAYLOAD_FILE" >/dev/null 2>&1 || bad=$((bad+1))
    grep -v '^selftest cases=19 failures=0$' "$syn" > "$sdir/s2.txt"
    tot=$((tot+1)); _k8_grade "$sdir/s2.txt" "$PAYLOAD_FILE" >/dev/null 2>&1 || bad=$((bad+1))
    sed 's/^export-ref=.*/export-ref=0000000000000000000000000000000000000000/' "$syn" > "$sdir/s3.txt"
    tot=$((tot+1)); _k8_grade "$sdir/s3.txt" "$PAYLOAD_FILE" >/dev/null 2>&1 || bad=$((bad+1))
    if [ "$good" -eq 1 ] && [ "$bad" -eq "$tot" ]; then
        printf 'selftest case=K8 positive=pass mutants=%s/%s verdict=pass\n' "$bad" "$tot"
    else
        printf 'selftest case=K8 positive=%s mutants=%s/%s verdict=fail\n' \
            "$( [ "$good" -eq 1 ] && echo pass || echo fail)" "$bad" "$tot"
        failures=$((failures+1))
    fi

    # K14-K19: positive on a hard-linked copy of the export, then one
    # committed-shape mutation that the limb must reject.
    st_case K14 "s:SCORECARD.md" || failures=$((failures+1))
    st_case K15 "app:LOG.md" || failures=$((failures+1))
    st_case K16 "strip:corpus/lessons/round-42.md" || failures=$((failures+1))
    st_case K17 "rm:.ufo/waves/round-42/claims-erratum-5.md" || failures=$((failures+1))
    st_case K18 "rm:.ufo/waves/round-43/final-gates/r42-at-de09313-run.txt" || failures=$((failures+1))
    st_case K19 "corrupt:.ufo/waves/round-43/freeze.txt" || failures=$((failures+1))

    printf 'selftest cases=19 failures=%d\n' "$failures"
    [ "$failures" -eq 0 ] && return 0 || return 1
}

st_case() {  # st_case <id> <kind>  -> grades positive then mutant
    local id="$1" kind="$2"
    local d="$SCRATCH_ROOT/selftest/case-$id"
    rm -rf "$d"; mkdir -p "$d/tree"
    cp -al "$EXPORT/." "$d/tree/" 2>/dev/null || return 1
    local tree="$d/tree" ln rc rel tmp
    ln="$(limb_line "$id" "$tree")"; rc=$?
    if [ "$rc" -ne 0 ]; then
        printf 'selftest case=%s positive=fail mutants=0/1 verdict=fail\n' "$id"
        rm -rf "$d"
        return 1
    fi
    case "$kind" in
        s)
            rel="SCORECARD.md"; tmp="$d/m.txt"; rm -f "$tree/$rel"
            python3 - "$EXPORT/$rel" "$tmp" <<'PYMUT'
import re, sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src).read()
open(dst, "w").write(re.sub(r"corrections=\d+", "corrections=999", t, count=1))
PYMUT
            mv "$tmp" "$tree/$rel"
            ;;
        app)
            rel="LOG.md"; tmp="$d/m.txt"
            { cat "$EXPORT/$rel"; printf '%s\n' '- wave 77 `kasegi-r77-ghost` 12 seats dispatched against the head.'; } > "$tmp"
            rm -f "$tree/$rel"; mv "$tmp" "$tree/$rel"
            ;;
        strip)
            rel="corpus/lessons/round-42.md"; tmp="$d/m.txt"
            grep -v '^Correction (round 43)' "$EXPORT/$rel" > "$tmp"
            rm -f "$tree/$rel"; mv "$tmp" "$tree/$rel"
            ;;
        rm)
            if [ "$id" = "K17" ]; then
                rm -f "$tree/.ufo/waves/round-42/claims-erratum-5.md"
            else
                rm -f "$tree/.ufo/waves/round-43/final-gates/r42-at-de09313-run.txt"
            fi
            ;;
        corrupt)
            rel=".ufo/waves/round-43/freeze.txt"; tmp="$d/m.txt"
            awk 'index($0,"claims-sha256=")==1 { print "claims-sha256=0000000000000000000000000000000000000000000000000000000000000000"; next } { print }' "$EXPORT/$rel" > "$tmp"
            rm -f "$tree/$rel"; mv "$tmp" "$tree/$rel"
            ;;
        *) rm -rf "$d"; return 1 ;;
    esac
    ln="$(limb_line "$id" "$tree")"; rc=$?
    if [ "$rc" -ne 0 ]; then
        printf 'selftest case=%s positive=pass mutants=1/1 verdict=pass\n' "$id"
        rm -rf "$d"
        return 0
    fi
    printf 'selftest case=%s positive=pass mutants=0/1 verdict=fail\n' "$id"
    rm -rf "$d"
    return 1
}

RUN_BLOCK="$WORK/run-block.txt"
{
    printf 'all-gates v3\n'
    printf 'export-ref=%s\n' "$FULL"
    printf 'suite-sha256=%s\n' "$(suite_sha "$SUITE_SRC")"
    printf 'time-basis=ref-commit\n'
    printf 'run-utc=%s\n' "$(run_utc)"
    cat "$PAYLOAD_FILE"
    printf 'closed=%d/%d exit=%d\n' "$CLOSED" "$TOTAL" "$RC"
} > "$RUN_BLOCK"

if [ "$MODE" = "selftest" ]; then
    ST_OUT="$WORK/selftest-block.txt"
    selftest_block > "$ST_OUT"; ST_RC=$?
    cat "$ST_OUT"
    if [ -n "$RECEIPT_OUT" ]; then
        cat "$RUN_BLOCK" "$ST_OUT" > "$RECEIPT_OUT"
    fi
    exit "$ST_RC"
fi

if [ -n "$RECEIPT_OUT" ]; then
    ST_OUT="$WORK/selftest-block.txt"
    selftest_block > "$ST_OUT"; ST_RC=$?
    cat "$RUN_BLOCK" "$ST_OUT" > "$RECEIPT_OUT"
    exit "$RC"
fi

exit "$RC"
