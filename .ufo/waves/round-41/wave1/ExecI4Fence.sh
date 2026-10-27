#!/usr/bin/env bash
# ExecI4Fence.sh -- I4 fence-awareness limb for the round-41 closure suite.
#
# PURPOSE
#   The round-41 check I4 is: "fenced correction/criterion lines do not satisfy
#   line-anchored limbs; fence state CLOSED at EOF".  The round-40 scanner
#   (corpus/instruments/r40-closure.sh, h2_scan) opened a fence on any line
#   matching /^ {0,3}```/ but could only close it on /^ {0,3}```[ \t]*$/ --
#   three backticks exactly.  A CommonMark four-backtick fence therefore never
#   closed, so the round-40 wave-2 defeat fixture T3
#   (.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt) read
#   "fences=open" for a well-formed file.  This limb implements the CommonMark
#   fenced-code-block state machine so the suite can (a) exclude fenced lines
#   from every line-anchored count and (b) report the fence state at EOF.
#
# SOURCEABLE
#   . /path/to/ExecI4Fence.sh      # defines functions only; no side effects.
#
# PUBLIC API
#   fence_scan FILE                 "<lineno>\t<OUTSIDE|INSIDE>\t<CLOSED|OPEN>" per line
#   fence_report FILE               human-readable per-line report + summary
#   fence_outside_lines FILE        line numbers OUTSIDE any fence, ascending, one per line
#   fence_outside_count FILE        number of lines outside fences
#   fence_outside_match FILE ERE    "count=N lines=a b c" over OUTSIDE lines matching ERE
#   fence_eof_state FILE            "CLOSED" | "OPEN"  (fence state at EOF)
#   fence_line_state FILE N         "OUTSIDE" | "INSIDE" for line N
#   fence_audit FILE                "outside=N inside=M eof=CLOSED"
#
# SEMANTICS IMPLEMENTED (CommonMark 0.30 section 4.5, fenced code blocks)
#   * opener : up to 3 leading spaces, then a run of >= 3 identical ` or ~.
#              For a backtick fence the info string may not contain a backtick
#              (a tilde fence's info string may contain anything).
#   * closer : up to 3 leading spaces, a run of the SAME marker character at
#              least as long as the opener's run, and nothing but spaces or
#              tabs after it.
#   * A different marker character never closes an open fence, and a shorter
#              run of the same marker is content, not a closer: ``` inside a
#              ```` fence is content; ```` inside a ``` fence closes it.
#   * Every line of a fenced block -- including the opening and the closing
#              delimiter lines -- is reported INSIDE (fenced) and is therefore
#              excluded from the outside set.
#   * An unclosed fence extends to EOF: EOF state is OPEN and the remaining
#              lines are INSIDE.
#
# LIMITS (documented, not hidden)
#   * Only fenced code blocks are modelled.  Indented (4-space) code blocks,
#     HTML blocks and setext headings are not fence state and are reported
#     OUTSIDE.
#   * Indentation is counted in spaces only; a leading tab is treated as
#     non-fence indentation.
#   * The pattern argument of fence_outside_match is an ERE matched against the
#     whole line; anchor it yourself (e.g. '^Correction [(]round 41[)]').
#
# No global state is written; every call is a pure function of the file bytes.

FENCE_AWK_PROG='
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
BEGIN {
  in_fence = 0; FENCE_CHAR = ""; FENCE_LEN = 0
  out_n = 0; in_n = 0; match_n = 0; match_list = ""
  pat = ENVIRON["FENCE_PATTERN"]
}
{
  line = $0
  if (in_fence) {
    inside = 1
    if (fence_close(line)) { in_fence = 0; FENCE_CHAR = ""; FENCE_LEN = 0 }
  } else {
    if (fence_open(line)) { in_fence = 1; inside = 1 }
    else inside = 0
  }
  if (inside) in_n++; else out_n++
  if (mode == "scan")
    printf "%d\t%s\t%s\n", NR, (inside ? "INSIDE" : "OUTSIDE"), (in_fence ? "OPEN" : "CLOSED")
  else if (mode == "outside") { if (!inside) print NR }
  else if (mode == "match") {
    if (!inside && pat != "" && line ~ pat) {
      match_n++
      match_list = match_list (match_list == "" ? "" : " ") NR
    }
  }
}
END {
  if (mode == "count")   printf "%d\n", out_n
  else if (mode == "eof")     printf "%s\n", (in_fence ? "OPEN" : "CLOSED")
  else if (mode == "audit")   printf "outside=%d inside=%d eof=%s\n", out_n, in_n, (in_fence ? "OPEN" : "CLOSED")
  else if (mode == "match")   printf "count=%d lines=%s\n", match_n, match_list
}
'

fence_awk() { # MODE FILE [ERE]
  local mode=$1 file=$2 pat=${3-}
  [ -f "$file" ] || return 1
  FENCE_PATTERN="$pat" awk -v mode="$mode" "$FENCE_AWK_PROG" "$file"
}

fence_scan() { # FILE
  fence_awk scan "$1"
}

fence_report() { # FILE
  local file=$1 line st eof
  [ -f "$file" ] || { printf 'missing file: %s\n' "$file" >&2; return 1; }
  printf 'fence-report file=%s\n' "$file"
  fence_awk scan "$file" | while IFS=$'\t' read -r line st eof; do
    printf '%s\t%s\tfence=%s\n' "$line" "$st" "$eof"
  done
  fence_awk audit "$file"
}

fence_outside_lines() { # FILE
  fence_awk outside "$1"
}

fence_outside_count() { # FILE
  fence_awk count "$1"
}

fence_outside_set() { # FILE  -> the outside set on one line, space separated
  fence_awk outside "$1" | awk 'NR > 1 { printf " " } { printf "%s", $0 } END { print "" }'
}

fence_outside_match() { # FILE ERE
  fence_awk match "$1" "$2"
}

fence_eof_state() { # FILE
  fence_awk eof "$1"
}

fence_line_state() { # FILE N
  local file=$1 want=$2 line st eof
  [ -f "$file" ] || { printf 'missing\n' >&2; return 1; }
  line=$(fence_awk scan "$file" | awk -F'\t' -v n="$want" '$1 == n { print $2; exit }')
  [ -n "$line" ] || { printf 'missing\n' >&2; return 1; }
  printf '%s\n' "$line"
}

fence_audit() { # FILE
  fence_awk audit "$1"
}

fence_payload() { # FILE ERE -> "matches=N,fences=closed|open"
  local file=$1 pat=$2 n st
  st=$(fence_eof_state "$file") || { printf 'matches=0,fences=absent\n'; return 1; }
  n=$(fence_outside_match "$file" "$pat" | sed -e 's/^count=\([0-9][0-9]*\).*/\1/')
  printf 'matches=%s,fences=%s\n' "${n:-0}" "$st"
}

# fence_selftest -- graded self-test of the limb itself.  Writes fixtures under
# $TMPDIR (default /tmp) and removes them on exit.  Prints one
# "selftest case=<id> ... verdict=pass|fail" line per case and a summary.
# Cases:
#   A  a "Correction (round 41)" line inside a 4-backtick fence is NOT outside
#      (outside-match count 0) and the fence state at EOF is CLOSED
#   B  T3 shape: four correction lines, exactly one fenced -> outside count 3
#   C  a fenced pseudo-table row carrying M39-2 is fenced (outside count 0)
#   D  a well-formed file reports fence state CLOSED at EOF
#   E  a tilde fence is honoured and a different marker does not close a fence
#   F  an unclosed fence reports fence state OPEN at EOF
fence_selftest() {
  local d rc=0 n st m
  d=$(mktemp -d "${TMPDIR:-/tmp}/fence-selftest.XXXXXX") || return 1
  trap 'rm -rf -- "$d"' RETURN

  cat > "$d/a.md" <<'EOF'
# ledger
````markdown
Correction (round 41): C1 not verified on the frozen counter.
````
EOF
  cat > "$d/b.md" <<'EOF'
Correction (round 41): one
Correction (round 41): two
````markdown
Correction (round 41): three (fenced)
````
Correction (round 41): four
EOF
  cat > "$d/c.md" <<'EOF'
| id | note |
| --- | --- |
```text
| M39-2 | pseudo row inside a fence |
```
EOF
  cat > "$d/d.md" <<'EOF'
text
```text
inside
```
~~~
inside
~~~
EOF
  cat > "$d/e.md" <<'EOF'
```
~~~
tilde marker does not close a backtick fence
```
~~~
tilde fence content
~~~
EOF
  cat > "$d/f.md" <<'EOF'
text
```
never closed
EOF
  cat > "$d/g.md" <<'EOF'
````
```
three backticks do not close a four-backtick fence
```
````
EOF

  local corr='^Correction [(]round 41[)]'

  m=$(fence_outside_match "$d/a.md" "$corr" | sed -e 's/^count=\([0-9][0-9]*\).*/\1/')
  st=$(fence_eof_state "$d/a.md")
  if [ "${m:-x}" = 0 ] && [ "$st" = CLOSED ]; then
    printf 'selftest case=A payload=outside=%s,fences=%s verdict=pass\n' "$m" "$st"
  else
    printf 'selftest case=A payload=outside=%s,fences=%s verdict=FAIL\n' "$m" "$st"; rc=1
  fi

  m=$(fence_outside_match "$d/b.md" "$corr" | sed -e 's/^count=\([0-9][0-9]*\).*/\1/')
  st=$(fence_eof_state "$d/b.md")
  if [ "${m:-x}" = 3 ] && [ "$st" = CLOSED ]; then
    printf 'selftest case=B payload=outside=%s,fences=%s verdict=pass\n' "$m" "$st"
  else
    printf 'selftest case=B payload=outside=%s,fences=%s verdict=FAIL\n' "$m" "$st"; rc=1
  fi

  m=$(fence_outside_match "$d/c.md" 'M39-2' | sed -e 's/^count=\([0-9][0-9]*\).*/\1/')
  st=$(fence_eof_state "$d/c.md")
  if [ "${m:-x}" = 0 ] && [ "$st" = CLOSED ]; then
    printf 'selftest case=C payload=outside=%s,fences=%s verdict=pass\n' "$m" "$st"
  else
    printf 'selftest case=C payload=outside=%s,fences=%s verdict=FAIL\n' "$m" "$st"; rc=1
  fi

  st=$(fence_eof_state "$d/d.md")
  n=$(fence_outside_count "$d/d.md")
  if [ "$st" = CLOSED ] && [ "${n:-x}" -gt 0 ] 2>/dev/null; then
    printf 'selftest case=D payload=outside=%s,fences=%s verdict=pass\n' "$n" "$st"
  else
    printf 'selftest case=D payload=outside=%s,fences=%s verdict=FAIL\n' "$n" "$st"; rc=1
  fi

  m=$(fence_outside_match "$d/e.md" 'tilde marker does not close' | sed -e 's/^count=\([0-9][0-9]*\).*/\1/')
  n=$(fence_outside_match "$d/e.md" 'tilde fence content' | sed -e 's/^count=\([0-9][0-9]*\).*/\1/')
  st=$(fence_eof_state "$d/e.md")
  if [ "${m:-x}" = 0 ] && [ "${n:-x}" = 0 ] && [ "$st" = CLOSED ]; then
    printf 'selftest case=E payload=outside=%s/%s,fences=%s verdict=pass\n' "$m" "$n" "$st"
  else
    printf 'selftest case=E payload=outside=%s/%s,fences=%s verdict=FAIL\n' "$m" "$n" "$st"; rc=1
  fi

  st=$(fence_eof_state "$d/f.md")
  if [ "$st" = OPEN ]; then
    printf 'selftest case=F payload=fences=%s verdict=pass\n' "$st"
  else
    printf 'selftest case=F payload=fences=%s verdict=FAIL\n' "$st"; rc=1
  fi

  m=$(fence_outside_match "$d/g.md" 'three backticks do not close' | sed -e 's/^count=\([0-9][0-9]*\).*/\1/')
  st=$(fence_eof_state "$d/g.md")
  if [ "${m:-x}" = 0 ] && [ "$st" = CLOSED ]; then
    printf 'selftest case=G payload=outside=%s,fences=%s verdict=pass\n' "$m" "$st"
  else
    printf 'selftest case=G payload=outside=%s,fences=%s verdict=FAIL\n' "$m" "$st"; rc=1
  fi

  return $rc
}

# ---------------------------------------------------------------------------
# Standalone CLI.  When sourced, nothing below runs; when executed directly,
# the same guard the round-40 suite uses is honoured:
#     bash ExecI4Fence.sh --selftest        run the graded self-test
#     bash ExecI4Fence.sh --report FILE     per-line fence report
#     bash ExecI4Fence.sh --outside FILE    the outside set, one line
#     bash ExecI4Fence.sh --eof FILE        CLOSED | OPEN
# ---------------------------------------------------------------------------
fence_cli() {
  case "${1:-}" in
    --selftest) fence_selftest ;;
    --report)   fence_report "$2" ;;
    --outside)  fence_outside_set "$2" ;;
    --eof)      fence_eof_state "$2" ;;
    --help|-h|"")
      printf 'usage: %s --selftest|--report FILE|--outside FILE|--eof FILE\n' "${0##*/}"
      ;;
    *)
      printf 'unknown argument: %s\n' "$1" >&2
      return 2
      ;;
  esac
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  fence_cli "$@"
fi
