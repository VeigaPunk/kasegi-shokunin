#!/usr/bin/env bash
# ExecJ2Token.sh — round-42 closure-suite limb J2 (family F-TOKEN: token-boundary tallies).
#
# WHAT IT REPAIRS
#   The round-41 suite's I3 check graded a tally with a PER-RECORD UNION over the
#   correction lines: a record "tallied" as soon as ANY of its
#   `Correction (round 41)` lines carried the expected token, and the mangled
#   counter only ran when NO line in the record hit.  The committed defeat
#   (`.ufo/waves/round-41/wave2/RevC1Counters.md`, selftest detail
#   `mutant=mangled-value-token rejected=0`) rewrote ONE correction line so its
#   truth tally read `closed=10/100`; the surviving duplicated twin still read
#   `closed=10/10`, so I3 kept `tally=3/3 mangled=0` and the mutant was ACCEPTED.
#   Two holes made that possible:
#     (a) VALUE PRESENCE instead of VALUE EQUALITY — a substring/prefix test for
#         `closed=10/10` also succeeds inside `closed=10/100`, so the mangled
#         form is never distinguished from the truth;
#     (b) PER-RECORD UNION instead of PER-LINE grading — a mangled line is
#         masked by any surviving sibling line.
#   J2 closes both: every `closed=<n>/<m>`, `failures=<k>` and `cases=<k>` value
#   is EXTRACTED as a whole token and compared for FULL VALUE EQUALITY against an
#   expected value derived from the tree's own committed closure receipts, and
#   every graded rule is evaluated PER LINE, so no sibling can mask a defect.
#
# THE WHOLE-TOKEN RULE
#   A tally token is `KEY=VALUE` with KEY in {closed, failures, cases} and VALUE
#   = `<digits>` or, for `closed` only, `<digits>/<digits>`.  It is a whole token
#   only when
#     * the character immediately before KEY (if any) is neither a word character
#       [A-Za-z0-9_] nor `/` — so `xclosed=13/13`, `unclosed=13/13` and
#       `/closed=13/13` do NOT yield the token `closed=13/13`;
#     * `=` immediately follows KEY and the value immediately follows `=` with no
#       whitespace — so `closed =13/13` and `closed= 13/13` are residuals;
#     * the value is the maximal run of digits (at most one `/` with digits on
#       both sides) and the character immediately after it (if any) is neither a
#       word character nor `/` — so `closed=13/130` extracts as `13/130` (never
#       as `13/13`), and `closed=13/13x`, `closed=13/13/7`, `closed=13/` are
#       residuals.
#   Regex word boundaries are NOT sufficient: `\b` treats `/` as a non-word
#   character, so `\bclosed=10/10\b` matches inside `closed=10/10/12`, and a
#   plain substring test matches `closed=10/10` inside `closed=10/100`.
#
# WHAT J2 GRADES ON THE EXPORTED TREE
#   `check_j2 TREE REF` reads ONLY the exported tree:
#     * the three lane records SCORECARD.md, LOG.md, SHONEN.md, CommonMark
#       fence-aware (a correction-shaped line inside a fence is not a live
#       correction — the lane's own convention, r41-closure.sh I4); and
#     * the committed closure receipts `.ufo/waves/round-<n>/final-gates/all-gates.txt`,
#       which supply the EXPECTED tallies.
#   For every round N that has live `Correction (round N)` lines, the expected
#   truth T(N) is the tally of the round-(N-1) receipt: its summary
#   `closed=<n>/<m>` line and, when the receipt carries one, its
#   `selftest cases=<k> failures=<f>` line.  T(N) is DERIVED from committed
#   bytes, never hardcoded; a round whose receipt is absent while its corrections
#   carry citations is fail-closed (RED), never a vacuous pass.
#
#   The limb is CLOSED (exit 0) only when ALL of the following hold.
#     records=3        all three records exist under TREE
#     resid=0          no tally occurrence is a residual/malformed token (fused
#                      key, spaced key, spaced value, truncated ratio, trailing
#                      word character, trailing slash) in any live correction line
#                      of any round
#     near=0           no extracted tally value is a DELETION VARIANT of an
#                      expected truth value.  DELETION VARIANT: same key, same
#                      arity, and at least one numeric field of the candidate is
#                      obtained from the corresponding expected field (or the
#                      reverse) by DELETING digits — `10/100` vs `10/10`,
#                      `13/130` vs `13/13`, `1/13` vs `13/13`, `10` vs `1`.
#                      This makes a mangled citation a RED even while a sibling
#                      line still carries the exact truth: the defect is
#                      DETECTED, never masked.
#     cited=K/M        for every graded round N, every record whose round-N lines
#                      carry tally citations carries the expected truth
#                      `closed=<T(N)>` as a whole token (K = records that cite
#                      it, M = records that make any round-N citation; M must be
#                      > 0)
#     anch=K/M         every round-N line that cites the round-(N-1) receipt PATH
#                      and carries a `closed=` token carries the exact truth
#                      token.  This is the per-line truth enforcer.
#     probe=K/M        the extractor battery passes every probe (see below)
#     truth=ok         no round cites tallies while its receipt is missing
#
# THE PROBE BATTERY
#   `j2_probe_battery` exercises the extractor directly.  Honest shapes must
#   extract to the expected value; every boundary mutant must NOT: the committed
#   `closed=10/100`, `closed=13/130`, `closed=1/13`, `failures=10` (vs
#   `failures=1`), `xclosed=13/13x`, `unclosed=13/13`, `closed= 13/13`,
#   `closed =13/13`, `closed=13 /13`, `closed=13/ 13`, `closed=13/13x`,
#   `closed=13/13/7`.  A leading space BEFORE the key is a legal delimiter for a
#   legal token and is an ACCEPT probe.
#
# THE REPLAY LIMB (the C1 kill-rule requirement)
#   `j2_replay_fixtures WORK TREE` re-executes the committed defeat and the
#   family's boundary mutants against the CURRENT limb:
#     * `committed-mangled-value-token` applies the round-41 I3 defeat EXACTLY as
#       the committed r41 suite applied it — the replacement text is read out of
#       the tree's committed `corpus/instruments/r41-closure.sh` (the line
#       carrying `closed=10/100`), so the replay is the committed artifact, not a
#       paraphrase — to the first `Correction (round 41)` line of SCORECARD.md;
#     * `boundary-*` fixtures mangle a truth citation to `closed=13/130`,
#       `closed=1/13`, `closed= 10/10`, `closed =10/10`, `xclosed=13/13x`,
#       `closed=10/10x`, `closed=10/10/7`, and swap a `failures=0` for
#       `failures=10` where `failures=1` is the committed truth.
#   Every fixture must be REJECTED and the unmutated tree must be ACCEPTED.
#
# STANDALONE DRIVER (export mode only, like the suite)
#   bash ExecJ2Token.sh --export-ref <hash> [--lane DIR] [--work DIR] [--selftest]
#   bash ExecJ2Token.sh --tree DIR [--selftest]
#   A plain run (no --export-ref, no --tree) refuses with exit 2: a limb that
#   grades the live worktree can be turned green by edits never committed.
#
# SOURCING
#   Sourceable limb: sourcing defines functions and globals only.  It sets no
#   shell options and runs nothing.  Integration contract for the suite:
#       payload=$(check_j2 "$EXPORT" "$REF"); rc=$?
#       printf 'J2 payload=%s closed=%s\n' "$payload" "$([ "$rc" -eq 0 ] && echo 1 || echo 0)"
#
# J2_RECORDS: the three lane records this limb grades.
J2_RECORDS=(SCORECARD.md LOG.md SHONEN.md)

# ---------------------------------------------------------------------------
# J2_AWK — one program for both jobs.
#   mode=grade : receipts first define the expected tallies, then the records are
#                graded line by line; prints CITE/RESID lines and one PAYLOAD.
#   mode=scan  : scans stdin lines for tokens (the probe battery); prints CITE
#                and RESID only.
# ---------------------------------------------------------------------------
J2_AWK='
function isword(c) { return (c != "" && c ~ /^[A-Za-z0-9_]$/) }
function isdig(c)  { return (c != "" && c ~ /^[0-9]$/) }

function fence_open(line,   i, n, c, run, rest) {
  i = 1; n = 0
  while (n < 3 && substr(line, i, 1) == " ") { n++; i++ }
  c = substr(line, i, 1)
  if (c != "`" && c != "~") return 0
  run = 0
  while (c != "" && substr(line, i + run, 1) == c) run++
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
  c = substr(line, i, 1)
  if (c == "" || c != FENCE_CHAR) return 0
  run = 0
  while (substr(line, i + run, 1) == c) run++
  if (run < FENCE_LEN) return 0
  rest = substr(line, i + run)
  if (rest ~ /[^ \t]/) return 0
  return 1
}

# is_del(a,b): 1 when a is obtained from b by DELETING at least one digit.
function is_del(a, b,   i, j, la, lb) {
  if (a == b) return 0
  la = length(a); lb = length(b)
  if (la >= lb) return 0
  i = 1
  for (j = 1; j <= lb && i <= la; j++)
    if (substr(b, j, 1) == substr(a, i, 1)) i++
  return (i > la)
}
function nfields(v,   c) { c = v; gsub(/[^\/]/, "", c); return length(c) + 1 }
function fieldof(v, idx,   a, n) { n = split(v, a, "/"); return (idx <= n) ? a[idx] : "" }
function del_variant(cand, tgt,   fc, fe, i, nf) {
  if (cand == tgt) return 0
  nf = nfields(cand)
  if (nf != nfields(tgt)) return 0
  for (i = 1; i <= nf; i++) {
    fc = fieldof(cand, i); fe = fieldof(tgt, i)
    if (is_del(fc, fe) || is_del(fe, fc)) return 1
  }
  return 0
}

# scan_line: fills TK[]/TV[]/NT with whole tokens and prints RESID lines.
function scan_line(line, rnd, lno,   k, key, kl, n, start, p, pos, prev, j, c, kk, s, e, num1, term, val, shape, bad) {
  n = length(line); NT = 0
  for (k = 1; k <= 3; k++) {
    key = (k == 1) ? "closed" : (k == 2 ? "failures" : "cases")
    kl = length(key); start = 1
    while (start <= n) {
      p = index(substr(line, start), key "=")
      if (p == 0) break
      pos = start + p - 1
      prev = (pos > 1) ? substr(line, pos - 1, 1) : ""
      start = pos + kl + 1
      if (prev != "" && (isword(prev) || prev == "/")) {
        printf "RESID|%s|%d|%s|fused-key\n", rnd, lno, key; NRESID++; continue
      }
      j = pos + kl + 1
      if (j > n) continue
      c = substr(line, j, 1)
      if (!isdig(c)) {
        kk = j
        while (kk <= n && (substr(line, kk, 1) == " " || substr(line, kk, 1) == "\t")) kk++
        if (kk <= n && isdig(substr(line, kk, 1))) {
          printf "RESID|%s|%d|%s|spaced-value\n", rnd, lno, key; NRESID++
        }
        continue
      }
      s = j
      while (j <= n && isdig(substr(line, j, 1))) j++
      num1 = substr(line, s, j - s)
      val = num1; shape = "int"; bad = 0
      if (j <= n && substr(line, j, 1) == "/") {
        if (j + 1 <= n && isdig(substr(line, j + 1, 1))) {
          e = j + 1
          while (e <= n && isdig(substr(line, e, 1))) e++
          val = num1 "/" substr(line, j + 1, e - j - 1)
          shape = "ratio"; j = e
        } else {
          printf "RESID|%s|%d|%s|truncated-ratio\n", rnd, lno, key; NRESID++; continue
        }
      }
      term = (j <= n) ? substr(line, j, 1) : ""
      if (term != "" && (isword(term) || term == "/")) bad = 1
      if (shape == "ratio" && key != "closed") bad = 1
      if (bad) {
        printf "RESID|%s|%d|%s|malformed-value\n", rnd, lno, key; NRESID++; continue
      }
      NT++; TK[NT] = key; TV[NT] = val
    }
    # `KEY <ws> =` is a spaced KEY: a tally claim that is not a whole token.
    start = 1
    while (start <= n) {
      p = index(substr(line, start), key)
      if (p == 0) break
      pos = start + p - 1
      prev = (pos > 1) ? substr(line, pos - 1, 1) : ""
      start = pos + kl
      if (prev != "" && (isword(prev) || prev == "/")) continue
      kk = pos + kl
      if (kk > n) continue
      c = substr(line, kk, 1)
      if (c != " " && c != "\t") continue
      while (kk <= n && (substr(line, kk, 1) == " " || substr(line, kk, 1) == "\t")) kk++
      if (kk <= n && substr(line, kk, 1) == "=") {
        printf "RESID|%s|%d|%s|spaced-key\n", rnd, lno, key; NRESID++
      }
    }
  }
}

BEGIN {
  FENCE_CHAR = ""; FENCE_LEN = 0; NRESID = 0; NEAR = 0; nrec = 0
  n = split(recs, a, " "); for (i = 1; i <= n; i++) RECSEEN[a[i]] = 1
}

{
  line = $0
  if (mode == "scan") {
    scan_line(line, 0, NR)
    for (i = 1; i <= NT; i++) printf "CITE|0|%d|%s|%s\n", NR, TK[i], TV[i]
    next
  }
  if (FNR == 1) {
    if (FILENAME ~ /\/final-gates\/all-gates[.]txt$/) {
      cur_kind = "receipt"
      r = FILENAME; sub(/^.*\/round-/, "", r); sub(/\/final-gates.*$/, "", r)
      cur_round = r + 0
    } else {
      cur_kind = "record"
      rec = FILENAME; sub(/^.*\//, "", rec)
      cur_rec = rec; nrec++
      in_fence = 0; FENCE_CHAR = ""; FENCE_LEN = 0
    }
  }
  if (cur_kind == "receipt") {
    if (line ~ /^closed=[0-9]+\/[0-9]+( exit=[01])?$/) {
      s = line; sub(/^closed=/, "", s); sub(/[ ].*$/, "", s); TCLOSE[cur_round] = s
    } else if (line ~ /^selftest cases=[0-9]+ failures=[0-9]+$/) {
      s = line; sub(/^selftest cases=/, "", s); sub(/ .*$/, "", s); TCA[cur_round] = s
      s = line; sub(/^.* failures=/, "", s); TFA[cur_round] = s
    }
    next
  }
  inside = 0
  if (in_fence) {
    inside = 1
    if (fence_close(line)) { in_fence = 0; FENCE_CHAR = ""; FENCE_LEN = 0 }
  } else if (fence_open(line)) {
    inside = 1; in_fence = 1
  }
  if (inside) { if (line ~ /^Correction \(round [0-9]+\)/) fenced++; next }
  if (line !~ /^Correction \(round [0-9]+\)/) next
  r = line; sub(/^Correction \(round /, "", r); sub(/\).*$/, "", r); r = r + 0
  roundseen[r] = 1
  apath = ".ufo/waves/round-" (r - 1) "/final-gates/all-gates.txt"
  anchored = (index(line, apath) > 0)
  scan_line(line, r, FNR)
  truth_here = 0; closed_here = 0; any_here = 0
  for (i = 1; i <= NT; i++) {
    k = TK[i]; v = TV[i]
    any_here = 1
    printf "CITE|%s|%d|%s|%s\n", r, FNR, k, v
    if (k == "closed") {
      closed_here++
      if (TCLOSE[r - 1] != "" && v == TCLOSE[r - 1]) truth_here = 1
    }
    if (k == "closed"   && TCLOSE[r - 1] != "" && del_variant(v, TCLOSE[r - 1])) NEAR++
    if (k == "cases"    && ((r - 1) in TCA)   && del_variant(v, TCA[r - 1]))    NEAR++
    if (k == "failures" && ((r - 1) in TFA)   && del_variant(v, TFA[r - 1]))    NEAR++
  }
  if (!any_here) next
  ctot[cur_rec, r] = 1
  if (truth_here) cok[cur_rec, r] = 1
  if (TCLOSE[r - 1] == "") missingtruth[r] = 1
  if (anchored && closed_here > 0) { anchtot++; if (truth_here) anchok++ }
}

END {
  if (mode == "scan") exit 0
  ncited = 0; nciteok = 0; ngrad = 0; miss = 0
  for (r in roundseen) {
    graded = 0
    for (rec in RECSEEN) if ((rec SUBSEP r) in ctot) graded = 1
    if (!graded) continue
    ngrad++
    for (rec in RECSEEN) {
      key = rec SUBSEP r
      if (!(key in ctot)) continue
      ncited++
      if (key in cok) nciteok++
    }
  }
  for (r in missingtruth) miss = 1
  printf "PAYLOAD|records=%d,graded=%d,fenced=%d,resid=%d,near=%d,cited=%d/%d,anch=%d/%d,truth=%s\n", \
    nrec, ngrad, fenced + 0, NRESID + 0, NEAR + 0, nciteok, ncited, anchok + 0, anchtot + 0, (miss ? "missing" : "ok")
}
'

# ---------------------------------------------------------------------------
# extractor + probe battery
# ---------------------------------------------------------------------------

# j2_scan_text TEXT — the extractor's CITE/RESID lines for TEXT.
j2_scan_text() {
  printf '%s\n' "$1" | awk -v mode=scan -v recs='' "$J2_AWK"
}

# j2_has_token TEXT KEY VALUE — 0 when TEXT holds KEY=VALUE as a whole token.
j2_has_token() {
  local text=$1 key=$2 want=$3 line out
  out=$(j2_scan_text "$text")
  [ -n "$out" ] || return 1
  while IFS= read -r line; do
    [ "$line" = "CITE|0|1|$key|$want" ] && return 0
  done <<EOF
$out
EOF
  return 1
}

# j2_probe_battery — accept/reject battery for the extractor.
# Prints "probe=<ok>/<n>,accept=<k>/<m>,reject=<k>/<m>" plus one `probe-fail=`
# line per failure; returns 0 only when every probe passes.
j2_probe_battery() {
  local ok=0 n=0 aok=0 an=0 rok=0 rn=0 line t k v
  local accepts=(
    'closed=13/13 exit=0|closed|13/13'
    'closed=10/10 exit=0|closed|10/10'
    'records `closed=10/12 exit=1` here|closed|10/12'
    'failures=1|failures|1'
    'cases=13|cases|13'
    'selftest cases=13 failures=0|cases|13'
    'selftest cases=13 failures=0|failures|0'
    'x closed=13/13 (leading space)|closed|13/13'
    'closed=13/13.|closed|13/13'
    'semicolon ; closed=13/13 ; delimited|closed|13/13'
  )
  local rejects=(
    'closed=10/100|closed|10/10'
    'closed=13/130|closed|13/13'
    'closed=1/13|closed|13/13'
    'failures=10|failures|1'
    'xclosed=13/13x|closed|13/13'
    'unclosed=13/13|closed|13/13'
    'closed= 13/13|closed|13/13'
    'closed =13/13|closed|13/13'
    'closed=13 /13|closed|13/13'
    'closed=13/ 13|closed|13/13'
    'closed=13/13x|closed|13/13'
    'closed=13/13/7|closed|13/13'
  )
  for line in "${accepts[@]}"; do
    t=${line%%|*}; k=${line#*|}; k=${k%%|*}; v=${line##*|}
    an=$((an + 1)); n=$((n + 1))
    if j2_has_token "$t" "$k" "$v"; then aok=$((aok + 1)); ok=$((ok + 1))
    else printf 'probe-fail=accept %s\n' "$line"; fi
  done
  for line in "${rejects[@]}"; do
    t=${line%%|*}; k=${line#*|}; k=${k%%|*}; v=${line##*|}
    rn=$((rn + 1)); n=$((n + 1))
    if j2_has_token "$t" "$k" "$v"; then printf 'probe-fail=reject %s\n' "$line"
    else rok=$((rok + 1)); ok=$((ok + 1)); fi
  done
  printf 'probe=%s/%s,accept=%s/%s,reject=%s/%s\n' "$ok" "$n" "$aok" "$an" "$rok" "$rn"
  [ "$ok" -eq "$n" ]
}

# ---------------------------------------------------------------------------
# the grade
# ---------------------------------------------------------------------------

# j2_receipt_files TREE — committed closure receipts, lowest round first.
j2_receipt_files() {
  local tree=$1 f
  for f in "$tree"/.ufo/waves/round-*/final-gates/all-gates.txt; do
    [ -f "$f" ] && printf '%s\n' "$f"
  done | awk -F/ '{ for (i = 1; i <= NF; i++) if ($i ~ /^round-[0-9]+$/) { r = $i; sub(/^round-/, "", r); print r + 0 "\t" $0 } }' | sort -n | cut -f2-
}

# j2_grade TREE — one pass over the receipts and the three records.
j2_grade() {
  local tree=$1 out rec
  local -a files=()
  while IFS= read -r rec; do [ -n "$rec" ] && files+=("$rec"); done <<EOF
$(j2_receipt_files "$tree")
EOF
  for rec in "${J2_RECORDS[@]}"; do [ -f "$tree/$rec" ] && files+=("$tree/$rec"); done
  if [ "${#files[@]}" -eq 0 ]; then
    printf 'records=0,graded=0,fenced=0,resid=0,near=0,cited=0/0,anch=0/0,truth=missing\n'
    return 1
  fi
  out=$(awk -v mode=grade -v recs="${J2_RECORDS[*]}" "$J2_AWK" "${files[@]}" 2>/dev/null)
  printf '%s\n' "$out" | awk -F'|' '
    $1 == "PAYLOAD" { sub(/^PAYLOAD\|/, ""); print; found = 1 }
    END { if (!found) print "records=0,graded=0,fenced=0,resid=0,near=0,cited=0/0,anch=0/0,truth=missing" }'
}

# j2_ratio_ok PAIR — 0 when K/M has K == M and M > 0.
j2_ratio_ok() {
  local pair=$1 l r
  case $pair in
    */*) l=${pair%%/*}; r=${pair##*/}
         case $l$r in *[!0-9]*) return 1 ;; esac
         [ "$l" = "$r" ] && [ "$r" -gt 0 ] && return 0 ;;
  esac
  return 1
}

# check_j2 TREE REF — the suite entry point.  Prints ONE payload line (k=v,...);
# returns 0 when CLOSED, 1 when RED.
check_j2() {
  local tree=${1:-}
  local payload probe probeline closed=1
  local records graded fenced resid near cited anch truth
  [ -n "$tree" ] && [ -d "$tree" ] || {
    printf 'records=0,graded=0,fenced=0,resid=0,near=0,cited=0/0,anch=0/0,truth=missing,probe=0/0,accept=0/0,reject=0/0\n'
    return 1
  }
  payload=$(j2_grade "$tree")
  probe=$(j2_probe_battery 2>/dev/null)
  probeline=$(printf '%s\n' "$probe" | grep '^probe=' | head -n 1)
  printf '%s\n' "$probe" | grep '^probe-fail=' >&2 || true
  [ -n "$probeline" ] || probeline='probe=0/0,accept=0/0,reject=0/0'
  records=$(printf '%s' "$payload" | sed -n 's/.*records=\([0-9]*\).*/\1/p')
  graded=$(printf '%s' "$payload"  | sed -n 's/.*graded=\([0-9]*\).*/\1/p')
  fenced=$(printf '%s' "$payload"  | sed -n 's/.*fenced=\([0-9]*\).*/\1/p')
  resid=$(printf '%s' "$payload"   | sed -n 's/.*resid=\([0-9]*\).*/\1/p')
  near=$(printf '%s' "$payload"    | sed -n 's/.*near=\([0-9]*\).*/\1/p')
  cited=$(printf '%s' "$payload"   | sed -n 's/.*cited=\([0-9]*\/[0-9]*\).*/\1/p')
  anch=$(printf '%s' "$payload"    | sed -n 's/.*anch=\([0-9]*\/[0-9]*\).*/\1/p')
  truth=$(printf '%s' "$payload"   | sed -n 's/.*truth=\([a-z]*\).*/\1/p')
  [ "${records:-0}" = "3" ] || closed=0
  [ "${graded:-0}" -ge 1 ] 2>/dev/null || closed=0
  [ "${resid:-1}" = "0" ] || closed=0
  [ "${near:-1}" = "0" ] || closed=0
  [ "${truth:-missing}" = "ok" ] || closed=0
  j2_ratio_ok "${cited:-0/0}" || closed=0
  j2_ratio_ok "${anch:-0/0}" || closed=0
  local pratio=${probeline#probe=}
  pratio=${pratio%%,*}
  j2_ratio_ok "$pratio" || closed=0
  printf 'records=%s,graded=%s,fenced=%s,resid=%s,near=%s,cited=%s,anch=%s,truth=%s,%s\n' \
    "${records:-0}" "${graded:-0}" "${fenced:-0}" "${resid:-1}" "${near:-1}" \
    "${cited:-0/0}" "${anch:-0/0}" "${truth:-missing}" "$probeline"
  [ "$closed" -eq 1 ]
}

# ---------------------------------------------------------------------------
# replay limb (the C1 kill-rule requirement)
# ---------------------------------------------------------------------------

# j2_fixture SRC DST — a minimal tree carrying exactly what J2 reads.
j2_fixture() {
  local src=$1 dst=$2 f rel rec
  rm -rf -- "$dst"; mkdir -p -- "$dst/.ufo/waves" || return 1
  for rec in "${J2_RECORDS[@]}"; do
    [ -f "$src/$rec" ] && cp -p -- "$src/$rec" "$dst/$rec"
  done
  for f in "$src"/.ufo/waves/round-*/final-gates/all-gates.txt; do
    [ -f "$f" ] || continue
    rel=${f#"$src"/}
    mkdir -p -- "$dst/$(dirname -- "$rel")"
    cp -p -- "$f" "$dst/$rel"
  done
  return 0
}

# j2_replace_first_corr FILE ROUND TEXT — replace the first live
# `Correction (round ROUND)` line with TEXT (via ENVIRON: no escape issues).
j2_replace_first_corr() {
  local f=$1 rnd=$2 text=$3 tmp
  tmp=$f.j2tmp.$$
  J2_RND=$rnd J2_TEXT=$text awk '
    BEGIN { rnd = ENVIRON["J2_RND"] + 0; txt = ENVIRON["J2_TEXT"] }
    !done && $0 ~ ("^Correction \\(round " rnd "\\)") { print txt; done = 1; next }
    { print }
  ' "$f" > "$tmp" && mv -- "$tmp" "$f"
}

# j2_subst_line FILE PREFIX NEEDLE OLD NEW — on the FIRST line that starts with
# PREFIX, contains NEEDLE and contains OLD, replace the first OLD with NEW.
j2_subst_line() {
  local f=$1 prefix=$2 needle=$3 old=$4 new=$5 tmp
  tmp=$f.j2tmp.$$
  J2_PREFIX=$prefix J2_NEEDLE=$needle J2_OLD=$old J2_NEW=$new awk '
    BEGIN { p = ENVIRON["J2_PREFIX"]; nd = ENVIRON["J2_NEEDLE"]
            o = ENVIRON["J2_OLD"]; nw = ENVIRON["J2_NEW"] }
    !done && index($0, p) == 1 && index($0, nd) > 0 && index($0, o) > 0 {
      i = index($0, o)
      $0 = substr($0, 1, i - 1) nw substr($0, i + length(o))
      done = 1
    }
    { print }
  ' "$f" > "$tmp" && mv -- "$tmp" "$f"
}

# j2_committed_defeat_text TREE — the round-41 I3 mutant replacement text, read
# out of the tree's committed r41 suite (the line carrying `closed=10/100`).
j2_committed_defeat_text() {
  local tree=$1 line
  [ -f "$tree/corpus/instruments/r41-closure.sh" ] || return 1
  line=$(grep -m 1 'closed=10/100' "$tree/corpus/instruments/r41-closure.sh") || return 1
  [ -n "$line" ] || return 1
  printf '%s' "$line" | sed -e 's/^[[:space:]]*//' -e "s/^'//" -e "s/'[[:space:]]*$//"
}

# j2_replay_fixtures WORK TREE — build every in-family defeat fixture from TREE,
# require check_j2 to REJECT each mutant and ACCEPT the unmutated tree.
j2_replay_fixtures() {
  local work=$1 tree=$2 total=0 fails=0 name new limb d payload rc dtxt
  local base="$work/j2-replay/base"
  mkdir -p -- "$work/j2-replay" || return 1

  if ! j2_fixture "$tree" "$base"; then
    printf 'replay fixture=j2-fixture rejected=0 limb=fixture payload=build-failed\n'
    printf 'replay fixtures=1 failures=1\n'
    return 1
  fi

  # positive control: the unmutated tree must be ACCEPTED
  total=$((total + 1))
  payload=$(check_j2 "$base" replay 2>/dev/null); rc=$?
  printf 'replay fixture=unmutated-tree accepted=%s limb=positive payload=%s\n' \
    "$([ "$rc" -eq 0 ] && echo 1 || echo 0)" "$payload"
  [ "$rc" -eq 0 ] || fails=$((fails + 1))

  # 1. the committed round-41 I3 defeat, replayed verbatim from committed bytes
  d="$work/j2-replay/committed"
  j2_fixture "$tree" "$d"
  total=$((total + 1))
  if dtxt=$(j2_committed_defeat_text "$tree") && [ -n "$dtxt" ]; then
    j2_replace_first_corr "$d/SCORECARD.md" 41 "$dtxt"
    payload=$(check_j2 "$d" replay 2>/dev/null); rc=$?
    printf 'replay fixture=committed-mangled-value-token rejected=%s limb=near payload=%s\n' \
      "$([ "$rc" -ne 0 ] && echo 1 || echo 0)" "$payload"
    [ "$rc" -ne 0 ] || fails=$((fails + 1))
  else
    printf 'replay fixture=committed-mangled-value-token rejected=0 limb=near payload=committed-defeat-text-not-found\n'
    fails=$((fails + 1))
  fi

  # 2. boundary mutants of the anchored round-41 truth citation `closed=10/10`
  while IFS='|' read -r name new limb; do
    [ -n "$name" ] || continue
    d="$work/j2-replay/$name"
    j2_fixture "$tree" "$d"
    j2_subst_line "$d/SCORECARD.md" 'Correction (round 41)' \
      'round-40/final-gates/all-gates.txt' 'closed=10/10' "$new"
    total=$((total + 1))
    payload=$(check_j2 "$d" replay 2>/dev/null); rc=$?
    printf 'replay fixture=%s rejected=%s limb=%s payload=%s\n' \
      "$name" "$([ "$rc" -ne 0 ] && echo 1 || echo 0)" "$limb" "$payload"
    [ "$rc" -ne 0 ] || fails=$((fails + 1))
  done <<'EOF'
boundary-closed-13-130|closed=13/130|near
boundary-closed-1-13|closed=1/13|near
boundary-leading-space-value|closed= 10/10|resid
boundary-leading-space-key|closed =10/10|resid
boundary-xclosed|xclosed=13/13x|resid
boundary-trailing-word|closed=10/10x|resid
boundary-ratio-tail|closed=10/10/7|resid
EOF

  # 3. `failures=10` where the committed truth is `failures=1` (round-40 lines)
  d="$work/j2-replay/boundary-failures-10"
  j2_fixture "$tree" "$d"
  j2_subst_line "$d/SCORECARD.md" 'Correction (round 40)' \
    'round-39/final-gates/all-gates.txt' 'failures=0' 'failures=10'
  total=$((total + 1))
  payload=$(check_j2 "$d" replay 2>/dev/null); rc=$?
  printf 'replay fixture=boundary-failures-10 rejected=%s limb=near payload=%s\n' \
    "$([ "$rc" -ne 0 ] && echo 1 || echo 0)" "$payload"
  [ "$rc" -ne 0 ] || fails=$((fails + 1))

  printf 'replay fixtures=%s failures=%s\n' "$total" "$fails"
  [ "$fails" -eq 0 ]
}

# ---------------------------------------------------------------------------
# standalone driver (export mode only)
# ---------------------------------------------------------------------------

# j2_lane_from_script — walk up from this file to the directory holding
# SCORECARD.md and corpus/.
j2_lane_from_script() {
  local d
  d=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" 2>/dev/null && pwd -P) || return 1
  while [ "$d" != "/" ]; do
    if [ -f "$d/SCORECARD.md" ] && [ -d "$d/corpus" ]; then printf '%s\n' "$d"; return 0; fi
    d=$(dirname -- "$d")
  done
  return 1
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  J2_TREE=''
  J2_REF=''
  J2_LANE=''
  J2_WORK=''
  J2_SELFTEST=0
  while [ $# -gt 0 ]; do
    case $1 in
      --tree)       J2_TREE=$2; shift 2 ;;
      --export-ref) J2_REF=$2; shift 2 ;;
      --lane)       J2_LANE=$2; shift 2 ;;
      --work)       J2_WORK=$2; shift 2 ;;
      --selftest)   J2_SELFTEST=1; shift ;;
      -h|--help)    sed -n '2,/^J2_RECORDS=/p' "${BASH_SOURCE[0]}" | sed -e '$d' -e 's/^# \{0,1\}//'; exit 0 ;;
      *) printf 'ExecJ2Token: unknown argument: %s\n' "$1" >&2; exit 2 ;;
    esac
  done
  if [ -z "$J2_TREE" ] && [ -z "$J2_REF" ]; then
    printf 'ExecJ2Token: refusing to run against the live worktree: this limb is export-mode only.\n' >&2
    printf 'ExecJ2Token: pass --export-ref <hash> (or --tree <exported dir>).\n' >&2
    exit 2
  fi
  [ -n "$J2_LANE" ] || J2_LANE=$(j2_lane_from_script) || J2_LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
  if [ -z "$J2_WORK" ]; then
    J2_WORK=$(mktemp -d "${TMPDIR:-/tmp}/j2-work.XXXXXXXX") || exit 2
    J2_WORK_AUTO=1
  fi
  mkdir -p -- "$J2_WORK" || exit 2
  if [ -n "$J2_REF" ]; then
    rm -rf -- "$J2_WORK/export"
    mkdir -p -- "$J2_WORK/export" || exit 2
    if ! git -C "$J2_LANE" archive --format=tar "$J2_REF" 2>/dev/null | tar -xf - -C "$J2_WORK/export"; then
      printf 'ExecJ2Token: export failed for ref %s (ref-not-found or unreadable lane)\n' "$J2_REF" >&2
      exit 1
    fi
    J2_TREE="$J2_WORK/export"
  fi
  [ -f "$J2_TREE/SCORECARD.md" ] || {
    printf 'ExecJ2Token: %s has no SCORECARD.md (not a lane tree)\n' "$J2_TREE" >&2
    exit 2
  }
  payload=$(check_j2 "$J2_TREE" "${J2_REF:-tree}"); rc=$?
  printf 'J2 payload=%s closed=%s\n' "$payload" "$([ "$rc" -eq 0 ] && echo 1 || echo 0)"
  if [ "$J2_SELFTEST" -eq 1 ]; then
    j2_probe_battery
    j2_replay_fixtures "$J2_WORK" "$J2_TREE" || rc=1
  fi
  exit "$rc"
fi
