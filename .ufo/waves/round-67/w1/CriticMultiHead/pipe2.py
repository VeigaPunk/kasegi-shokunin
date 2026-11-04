#!/usr/bin/env python3
"""Streams named operands with SIGPIPE restored to SIG_DFL, so the kernel kills it like cat."""
import signal, sys
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
for path in sys.argv[1:]:
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(65536)
            if not chunk:
                break
            sys.stdout.buffer.write(chunk)
    sys.stdout.buffer.flush()
