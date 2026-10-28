#!/usr/bin/env bash
# ExecK14Corrections.sh -- K14 limb of the round-43 closure suite.
#
# Sourceable:
#     . ExecK14Corrections.sh
#     check_k14 <export>            # export = an extracted lane tree
# Prints exactly one line on stdout:
#     K14 payload=literals=<n>,stale=<k>,superseded=<s>,live=corrections=<c>,groups=<g> closed=0|1
# Diagnostics (each stale occurrence, named) go to stderr; stdout never carries
# anything but the payload line.  Returns 0 when closed=1, 1 when closed=0.
#
# What it grades (RD42-1 class).  The live correction ledger is re-derived over
# SCORECARD.md, LOG.md, SHONEN.md by the round-42 instrument's OWN code: the
# engine embedded in <export>/corpus/instruments/r42-closure.sh is executed with
# __name__ != "__main__" and its check_j11() is called, so the counts are
# check_j11's counts (its RECORDS, its fence-aware correction_lines, its
# body-normalisation, its groups rule) -- never a re-implementation.
#
# Every `corrections=<n>` / `groups=<n>` literal carried by those three files is
# then read as a WHOLE token (R41: `corrections=330` is 330, `xcorrections=33` is
# nothing) and must
#   (a) equal the value re-derived from the SAME export, or
#   (b) be named verbatim by a `Correction (round 43)` line at a LATER line of
#       the SAME file, outside any fenced block.
#
# Quoted defect evidence is not a result (R41).  A fenced line carrying `payload=`
# is a quoted run transcript and is skipped whole.  A line carrying `mutant=` or
# `quarantined` is a quotation of defect evidence, but a `live=` claim on it is
# still graded.  Every other line is a record line and every literal on it is
# graded -- there is no word list: ordinary prose ("the 23/73 attack share") can
# never license a stale literal.  A bare stale literal inside a fence is still a
# carried literal and is graded.
#
# A `Correction (round 43)` line is the round's supersession instrument, so it is
# itself a carrier of every literal it names; those self-naming occurrences are
# quotations and are exempt (a marker cannot be excused by a later copy of
# itself).  The one exception is a `live=<key>=<n>` assertion on any line: a
# claimed live value is always graded against the re-derived value.
#
# Exit 0 only when the live ledger was derived over all three records and
# stale=0; 1 otherwise.
#
# Direct invocation is for transcripts only:  bash ExecK14Corrections.sh <export>
# The closure suite sources this file.

check_k14() {
    python3 - "${1:-}" <<'K14_PY'
import os
import re
import sys

TREE = sys.argv[1] if len(sys.argv) > 1 else ""
ENGINE_REL = "corpus/instruments/r42-closure.sh"
ENGINE_RX = re.compile(
    r"^exec python3 - <<'R42_ENGINE_PY'\n(.*?)\nR42_ENGINE_PY[ \t]*\n",
    re.S | re.M)
LIT_RX = re.compile(r"(?<![0-9A-Za-z_])(corrections|groups)=([0-9]+)"
                    r"(?![0-9A-Za-z_])")
MARKER_ROUND = "43"
LIVE_PREFIX = "live="


def diag(msg):
    sys.stderr.write("K14 %s\n" % msg)


def emit(literals, stale, superseded, live_c, live_g, closed):
    sys.stdout.write(
        "K14 payload=literals=%d,stale=%d,superseded=%d,"
        "live=corrections=%d,groups=%d closed=%d\n"
        % (literals, stale, superseded, live_c, live_g, closed))
    sys.exit(0 if closed else 1)


def whole(text, lit):
    return re.search(r"(?<![0-9A-Za-z_])%s(?![0-9A-Za-z_])"
                     % re.escape(lit), text) is not None


def is_live_claim(line, start):
    """True when the literal at `start` sits in a `live=...` token.

    The payload grammar is live=corrections=<c>,groups=<g>, so both keys of that
    segment are live claims; a bare `corrections=<n>` in prose is not.
    """
    i = start
    while i > 0 and line[i - 1] not in " \t`;(":
        i -= 1
    return LIVE_PREFIX in line[i:start]


def evidence_mode(line, fenced):
    """How much of this line is graded: 'all', 'live' (only live= claims), 'none'.

    A fenced payload line is a quoted run transcript (skip whole).  A line that
    quotes a mutant or quarantine record is defect evidence, but its live=
    claims are still record claims.  Everything else is a record line.
    """
    low = line.lower()
    if fenced and "payload=" in low:
        return "none"
    if "mutant=" in low or "quarantined" in low:
        return "live"
    return "all"


def load_engine(tree):
    path = os.path.join(tree, ENGINE_REL)
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            src = fh.read()
    except OSError:
        return None
    m = ENGINE_RX.search(src)
    if not m:
        return None
    ns = {"__name__": "r42_k14_engine", "__file__": path}
    try:
        exec(compile(m.group(1), "%s:engine" % ENGINE_REL, "exec"), ns)
    except Exception:                                    # noqa: BLE001
        return None
    return ns


def main():
    if not TREE or not os.path.isdir(TREE):
        diag("error=export-unreadable tree=%s" % TREE)
        emit(0, 0, 0, 0, 0, 0)

    ns = load_engine(TREE)
    if ns is None:
        diag("error=engine-unreadable path=%s" % ENGINE_REL)
        emit(0, 0, 0, 0, 0, 0)

    records = list(ns["RECORDS"])
    missing = [r for r in records if not os.path.isfile(os.path.join(TREE, r))]
    if missing:
        for rec in missing:
            diag("error=record-absent file=%s" % rec)
        emit(0, 0, 0, 0, 0, 0)

    payload, ok = ns["check_j11"](TREE)
    live = {}
    for key in ("corrections", "groups"):
        m = re.search(r"(?<![0-9A-Za-z_])%s=([0-9]+)(?![0-9A-Za-z_])"
                      % key, payload)
        if m is None:
            diag("error=ledger-unreadable field=%s payload=%s" % (key, payload))
            emit(0, 0, 0, 0, 0, 0)
        live[key] = int(m.group(1))
    if live["corrections"] <= 0:
        diag("error=ledger-empty corrections=%d" % live["corrections"])
        emit(0, 0, 0, live["corrections"], live["groups"], 0)

    marker_rx = ns["CORRECTION_RX"]
    literals = stale = superseded = 0
    for rec in records:
        text = ns["read_text"](os.path.join(TREE, rec))
        rows = ns["fence_scan"](text)
        markers = [(int(rnd), ln, line)
                   for (rnd, ln, line) in ns["correction_lines"](text, MARKER_ROUND)]
        for lineno, line, fenced in rows:
            mode = evidence_mode(line, fenced)
            if mode == "none":
                continue
            m_marker = None if fenced else marker_rx.match(line)
            is_marker = m_marker is not None and \
                m_marker.group(1) == MARKER_ROUND
            for m in LIT_RX.finditer(line):
                live_claim = is_live_claim(line, m.start())
                if mode == "live" and not live_claim:
                    continue
                key, val = m.group(1), int(m.group(2))
                lit = "%s=%d" % (key, val)
                literals += 1
                if val == live[key]:
                    continue
                excused = False
                for _rnd, mline, mtext in markers:
                    if mline > lineno and whole(mtext, lit):
                        excused = True
                        break
                if not excused and is_marker and not live_claim:
                    excused = True
                if excused:
                    superseded += 1
                    diag("superseded=%s:%d %s live=%d" % (rec, lineno, lit,
                                                          live[key]))
                else:
                    stale += 1
                    diag("stale=%s:%d %s live=%d" % (rec, lineno, lit, live[key]))
    emit(literals, stale, superseded, live["corrections"], live["groups"],
         1 if stale == 0 else 0)


main()
K14_PY
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    check_k14 "$@"
fi
