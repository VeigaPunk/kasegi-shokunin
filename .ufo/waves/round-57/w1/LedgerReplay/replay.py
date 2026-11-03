#!/usr/bin/env python3
"""LedgerReplay/replay.py -- independent replay of every figure-audit ledger derive.

Round 57 seat LedgerReplay.  Reads the lane ledger READ-ONLY, runs each figure's
"derive" string through `bash -c` with cwd = lane root, merged stdout+stderr,
timeout 120 s, takes the FIRST NON-EMPTY line of stdout, strips it, and compares
it to the figure's "want" string as a whole value.

Deliberately independent of corpus/instruments/figure-audit.py: no import, no
shared helper, no read-only-head gate, no exit-code gate.  A derive that exits
nonzero but still prints the wanted line counts as ok here BY DESIGN (this is a
divergence probe, not a re-implementation of the instrument's policy); the
instrument and this replay are compared as verdict SETS over ids.

Usage: python3 replay.py [--ledger PATH] [--root DIR]
Exit:  0 all ok; 1 any STALE (or derive failed / timed out / printed nothing).
"""

import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
DEFAULT_LEDGER = os.path.join(LANE, "corpus", "instruments", "figure-audit-ledger.json")
TIMEOUT = 120


def first_stdout_line(cmd, root):
    """Run cmd with bash -c, cwd=root. Returns (line_or_None, reason_or_None)."""
    try:
        p = subprocess.run(
            ["bash", "-c", cmd],
            cwd=root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return None, "timeout-%ds" % TIMEOUT
    except OSError as e:
        return None, "spawn-error:%s" % e

    text = p.stdout.decode("utf-8", "replace")
    lines = text.splitlines()
    if not lines:
        return None, "empty-stdout"
    # The derive's OWN stdout is what is being graded; with stderr merged we take
    # the first non-empty line of the merged stream, exactly as specified.
    for ln in lines:
        s = ln.strip()
        if s:
            return s, None
    return None, "no-non-empty-line"


def main(argv):
    ledger = DEFAULT_LEDGER
    root = LANE
    i = 0
    while i < len(argv):
        if argv[i] == "--ledger" and i + 1 < len(argv):
            ledger = argv[i + 1]
            i += 2
            continue
        if argv[i] == "--root" and i + 1 < len(argv):
            root = argv[i + 1]
            i += 2
            continue
        sys.stderr.write("replay: unknown argument %r\n" % argv[i])
        return 2

    try:
        with open(ledger, "r", encoding="utf-8") as f:
            doc = json.load(f)
    except FileNotFoundError:
        sys.stderr.write("REPLAY: UNAVAILABLE reason=ledger-missing path=%s\n" % ledger)
        return 2
    except (ValueError, UnicodeDecodeError) as e:
        sys.stderr.write("REPLAY: UNAVAILABLE reason=ledger-unreadable detail=%s\n" % e)
        return 2

    figures = doc.get("figures")
    if not isinstance(figures, list):
        sys.stderr.write("REPLAY: UNAVAILABLE reason=no-figures-array path=%s\n" % ledger)
        return 2

    total = 0
    ok = 0
    stale = 0
    for fig in figures:
        fid = fig.get("id", "<no-id>")
        want = fig.get("want", "")
        derive = fig.get("derive", "")
        total += 1
        derived, reason = first_stdout_line(derive, root)
        if derived is None:
            derived = "<%s>" % (reason or "no-output")
            verdict = "STALE"
        else:
            verdict = "ok" if derived == want else "STALE"
        if verdict == "ok":
            ok += 1
        else:
            stale += 1
        print("REPLAY %-34s derived=%-70s want=%-70s %s"
              % (fid, derived, want, verdict))

    print("REPLAY-TOTAL figures=%d ok=%d stale=%d" % (total, ok, stale))
    return 0 if stale == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
