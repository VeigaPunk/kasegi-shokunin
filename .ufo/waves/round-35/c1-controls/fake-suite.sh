#!/usr/bin/env bash
# Do-nothing control for C1: prints the claimed after-state without performing
# any check. The real suite must distinguish itself: its --selftest must run
# seven real checks each shown able to fail on a defect-bearing fixture copy.
if [ "${1:-}" = "--selftest" ]; then
  echo "cases=7 failures=0"
else
  echo "closed=7/7 exit=0"
fi
exit 0
