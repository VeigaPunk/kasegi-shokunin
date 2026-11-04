#!/usr/bin/env python3
"""Streams every named operand to stdout in order (a read-only streaming wrapper)."""
import sys
for path in sys.argv[1:]:
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(65536)
            if not chunk:
                break
            sys.stdout.buffer.write(chunk)
sys.stdout.buffer.flush()
