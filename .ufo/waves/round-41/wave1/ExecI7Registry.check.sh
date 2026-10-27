#!/usr/bin/env bash
# ExecI7Registry.check.sh — round-41 I7 registry-row limb (sourceable).
#
# Contract
#   i7_registry_row_check <skill_md_path> <instrument_basename>
#
#     Reads <skill_md_path> (SKILL.md itself, or a scratch copy of it) and
#     looks for a Gates & probes registry row naming <instrument_basename>.
#     It never writes, never touches git, and reads only the file it is given.
#
#     A candidate row must satisfy ALL of:
#       1. it is a markdown table line (0-3 leading spaces then a pipe);
#       2. it has >= 8 pipe-separated fields (awk -F pipe field count >= 8);
#       3. its FIRST cell (awk -F pipe field 2, trimmed) equals
#          <instrument_basename> EXACTLY -- a mention of the basename
#          anywhere else in the row does not qualify (round-40 T13: the row
#          "| density.py notes (see r40-closure.sh ...) | doc | n/a |" is not
#          a registry row for r40-closure.sh, and neither is prose that
#          merely names the instrument);
#       4. the immediately preceding line is a table row or a separator and
#          never a blank line -- a blank line ENDS a markdown table, so a row
#          that follows one renders outside its header (round-40 D6, the live
#          breakage at SKILL.md L1119-L1122: header L1119, separator L1120,
#          blank L1121, row L1122);
#       5. it lies inside a CONTIGUOUS table whose header row carries a
#          "name" cell, whose next line is a delimiter row, and whose data
#          rows sit below that delimiter.
#
#     Every failing clause of a candidate is reported, not just the first, so
#     the payload names exactly which clauses are broken.
#
#     Prints exactly one payload line on stdout:
#       registry=<0|1>,basename=<b>,candidates=<n>,valid=<n>,line=<n|0>,mentions=<m>
#     and, when nothing is valid, ",reason=<why>" naming each rejected
#     candidate as "L<line>:<clause>[+<clause>...]". Exit 0 iff at least one
#     candidate is valid (registry=1), exit 1 otherwise, exit 2 on a usage or
#     file error.
#
#     `candidates` counts rows whose field 2 is exactly the basename;
#     `valid` counts those that also pass clauses 4 and 5; `mentions` counts
#     every line that names the basename anywhere but is NOT a valid registry
#     row (the T13 class). A mention-only file therefore prints candidates=0,
#     mentions>=1, valid=0, registry=0.
#
#     registry=1 means "at least one well-formed registry row exists for this
#     basename". It does NOT mean "no malformed row exists": SKILL.md is
#     append-only (round-41 I12), so a repaired table is appended and the
#     malformed predecessor row is still present. Callers that need the
#     malformed-row count read it from `candidates` vs `valid`.
#
#   Sourcing this file only DEFINES the function; it runs nothing and touches
#   no file. Executing it directly runs the function against $1/$2.
#
#   Sourceable use (as the round-41 suite I7 limb):
#     . corpus/instruments/r41-closure.sh      # or: . ExecI7Registry.check.sh
#     if payload=$(i7_registry_row_check "$tree/SKILL.md" r41-closure.sh); then
#         closed=1
#     fi
#
#   Standalone use:
#     bash ExecI7Registry.check.sh SKILL.md r40-closure.sh

i7_registry_row_check() {
  local file=${1:-} base=${2:-} out
  if [ -z "$file" ] || [ -z "$base" ]; then
    printf 'registry=0,basename=%s,candidates=0,valid=0,line=0,mentions=0,reason=usage\n' "$base" >&2
    return 2
  fi
  if [ ! -f "$file" ]; then
    printf 'registry=0,basename=%s,candidates=0,valid=0,line=0,mentions=0,reason=file-missing\n' "$base" >&2
    return 2
  fi
  out=$(awk -v base="$base" '
    function trim(s) { gsub(/^[ \t\r]+/, "", s); gsub(/[ \t\r]+$/, "", s); return s }
    function is_table(s) { return (s ~ /^ {0,3}\|/) }
    function is_sep(s,   f, n, i, c) {
      n = split(s, f, "[|]"); if (n < 3) return 0
      for (i = 2; i < n; i++) { c = trim(f[i]); if (c !~ /^:?-+:?$/) return 0 }
      return 1
    }
    function has_name(s,   f, n, i) {
      n = split(s, f, "[|]")
      for (i = 2; i < n; i++) if (tolower(trim(f[i])) == "name") return 1
      return 0
    }
    { L[NR] = $0 }
    END {
      n = NR; cand = 0; valid = 0; vline = 0; rej = ""; mentions = 0
      for (i = 1; i <= n; i++) {
        if (index(L[i], base) == 0) continue
        rowok = 0
        if (is_table(L[i])) {
          nf = split(L[i], F, "[|]")
          if (nf >= 8 && trim(F[2]) == base) rowok = 1
        }
        if (!rowok) { mentions++; continue }
        cand++
        r = ""
        # clause 4: the preceding line must be a table row or a separator
        if (i == 1) r = r "no-preceding-line"
        else if (!is_table(L[i - 1])) r = r (r == "" ? "" : "+") "preceding-line-not-a-table-row"
        # clause 5: the candidate must sit inside a CONTIGUOUS table whose
        # header row carries a name cell and whose next line is a delimiter
        # row. In markdown a table is exactly a run of pipe-rows whose FIRST
        # line is the header and whose SECOND is the delimiter, so the run
        # start -- not the nearest name-looking line -- is the header. A
        # blank line ends the run, which is why a row that follows one is not
        # in a table at all (round-40 D6).
        rs = i; while (rs > 1 && is_table(L[rs - 1])) rs--
        if (!has_name(L[rs]))
          r = r (r == "" ? "" : "+") "header-row-has-no-name-cell"
        else if (!((rs + 1) <= n && is_sep(L[rs + 1])))
          r = r (r == "" ? "" : "+") "no-delimiter-row-under-header"
        else if (i < rs + 2)
          r = r (r == "" ? "" : "+") "row-not-below-delimiter"
        if (r == "") { valid++; if (vline == 0) vline = i }
        else rej = rej (rej == "" ? "" : ";") "L" i ":" r
      }
      reg = (valid >= 1) ? 1 : 0
      out = "registry=" reg ",basename=" base ",candidates=" cand ",valid=" valid \
            ",line=" vline ",mentions=" mentions
      if (reg == 0) out = out ",reason=" (rej == "" ? "no-candidate-row" : rej)
      print out
    }' "$file")
  printf '%s\n' "$out"
  case "$out" in
    registry=1,*) return 0 ;;
    *) return 1 ;;
  esac
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  i7_registry_row_check "$@"
  exit $?
fi
