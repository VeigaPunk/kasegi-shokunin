#!/usr/bin/env bash
# CommonMark fenced-code walk (CommonMark 0.31.2 §4.5), used by round-38 gate G1.
#
# A fenced block opens, when the walk is closed, on a line matching
#   ^ {0,3}(`{3,}|~{3,})
# (an optional info string follows; a backtick fence's info string may not
# contain a backtick). While a fence is open, only a closing fence of the same
# character, at least as long as the opener, with nothing but spaces/tabs after
# it, closes it:
#   ^ {0,3}<same char>{>= opener length}[[:space:]]*$
# Every other line is content. A line indented 4+ spaces (or starting with a
# tab) is never a fence. At EOF the walk prints `open` or `closed`.
#
# Usage:
#   ExecFenceWalk.sh FILE           print `open` or `closed` at EOF
#   ExecFenceWalk.sh --trace FILE   print `<lineno> <code|text>` per line
#                                   (code = the line belongs to a fenced block)
#   ExecFenceWalk.sh --selftest     run the built-in cases; exit 0 iff all pass
#
# Exit: 0 on a completed walk (state printed), 1 on usage error or failed
# selftest, 2 when FILE is unreadable.

set -u

fence_walk() {
  # $1 = file, $2 = mode: state (default) | trace
  awk -v mode="${2:-state}" '
    function leading_spaces(s,   n) {
      n = 0
      while (n < 4 && substr(s, n + 1, 1) == " ") n++
      return n
    }
    {
      line = $0
      sub(/\r$/, "", line)
      wasopen = open

      n = leading_spaces(line)
      rest = substr(line, n + 1)
      ch = substr(rest, 1, 1)
      opened = 0
      closed = 0

      if (n <= 3 && (ch == "`" || ch == "~")) {
        run = 0
        while (substr(rest, run + 1, 1) == ch) run++
        if (run >= 3) {
          tail = substr(rest, run + 1)
          if (!open) {
            # A backtick fence whose info string holds a backtick is not a fence.
            if (!(ch == "`" && index(tail, "`") > 0)) {
              open = 1; open_ch = ch; open_len = run; opened = 1
            }
          } else if (ch == open_ch && run >= open_len && tail ~ /^[ \t]*$/) {
            open = 0; open_ch = ""; open_len = 0; closed = 1
          }
        }
      }

      if (mode == "trace")
        print NR, ((wasopen || opened || closed) ? "code" : "text")
    }
    END {
      if (mode == "state") print (open ? "open" : "closed")
    }
  ' "$1"
}

selftest() {
  local tmp cases=0 failures=0 name expect got dir
  tmp=$(mktemp -d "${TMPDIR:-/tmp}/fencewalk.XXXXXX") || return 1
  dir=$tmp

  run_case() { # name expect file
    local got verdict
    got=$(fence_walk "$3")
    cases=$((cases + 1))
    if [ "$got" = "$2" ]; then verdict=pass; else verdict=fail; failures=$((failures + 1)); fi
    printf 'case=%s expected=%s observed=%s verdict=%s\n' "$1" "$2" "$got" "$verdict"
  }

  printf '```text\ncontent\n```\n' >"$dir/info-then-close.md"
  run_case info-string-then-close closed "$dir/info-then-close.md"

  printf 'text\n```\nunclosed content\n' >"$dir/unclosed.md"
  run_case unclosed-at-eof open "$dir/unclosed.md"

  printf '````\n```\n```text\n````\n' >"$dir/nested-four.md"
  run_case nested-four-backtick closed "$dir/nested-four.md"
  # the 3-backtick lines above are content: the 4-backtick fence is closed only
  # by the 4-backtick line, so line 3 must classify as code
  got=$(fence_walk "$dir/nested-four.md" trace | awk '$2 == "code" { c++ } END { print c + 0 }')
  cases=$((cases + 1))
  if [ "$got" = "4" ]; then verdict=pass; else verdict=fail; failures=$((failures + 1)); fi
  printf 'case=%s expected=%s observed=%s verdict=%s\n' nested-four-all-code 4 "$got" "$verdict"

  printf '    ```\nstill text\n' >"$dir/indented-four.md"
  run_case indented-four-space closed "$dir/indented-four.md"

  printf '~~~\ntext with ``` inside\n~~~\n' >"$dir/tilde.md"
  run_case tilde-fence closed "$dir/tilde.md"

  printf '~~~\n```\n~~~\n' >"$dir/tilde-then-backtick.md"
  run_case tilde-not-closed-by-backtick closed "$dir/tilde-then-backtick.md"
  got=$(fence_walk "$dir/tilde-then-backtick.md" trace | awk '$2 == "code" { c++ } END { print c + 0 }')
  cases=$((cases + 1))
  if [ "$got" = "3" ]; then verdict=pass; else verdict=fail; failures=$((failures + 1)); fi
  printf 'case=%s expected=%s observed=%s verdict=%s\n' tilde-backtick-line-is-content 3 "$got" "$verdict"

  printf '```a`b\nnot a fence\n' >"$dir/backtick-in-info.md"
  run_case backtick-in-info-string closed "$dir/backtick-in-info.md"

  printf 'text\n```\ncode\n' >"$dir/append-base.md"
  cp "$dir/append-base.md" "$dir/append-closed.md"
  printf '```\n' >>"$dir/append-closed.md"
  run_case appended-closer-closes closed "$dir/append-closed.md"

  rm -rf -- "$dir"
  printf 'selftest cases=%d failures=%d\n' "$cases" "$failures"
  [ "$failures" -eq 0 ]
}

case "${1:-}" in
  --selftest) selftest; exit $? ;;
  --trace)
    [ $# -eq 2 ] || { printf 'usage: %s --trace FILE\n' "$0" >&2; exit 1; }
    [ -r "$2" ] || { printf '%s: cannot read %s\n' "$0" "$2" >&2; exit 2; }
    fence_walk "$2" trace
    ;;
  -*|'')  printf 'usage: %s [--trace|--selftest] FILE\n' "$0" >&2; exit 1 ;;
  *)
    [ -r "$1" ] || { printf '%s: cannot read %s\n' "$0" "$1" >&2; exit 2; }
    fence_walk "$1"
    ;;
esac
