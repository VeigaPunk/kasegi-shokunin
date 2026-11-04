#!/usr/bin/env python3
"""Streaming wrapper that swallows the broken pipe and exits 0 (a wrapper that reports success)."""
import sys
try:
    for path in sys.argv[1:]:
        with open(path, "rb") as fh:
            while True:
                chunk = fh.read(65536)
                if not chunk:
                    break
                sys.stdout.buffer.write(chunk)
    sys.stdout.buffer.flush()
except BrokenPipeError:
    try:
        sys.stdout.close()
    except Exception:
        pass
    sys.exit(0)
