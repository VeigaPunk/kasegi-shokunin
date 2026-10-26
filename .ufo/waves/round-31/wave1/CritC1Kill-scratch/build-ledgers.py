#!/usr/bin/env python3
"""Emit the three critique ledgers for CritC1Kill (round 31). Not a C1 deliverable.

Every `find` below is asserted to occur exactly once in its instrument before the
ledger is written. Classes:

  A  byte-inspection kill: `grep -cF '<the original source line>' {inst}`. The
     mutation is a trailing `# crit-eq` comment, so the mutant is behavior-
     equivalent by construction; only the source bytes move.
  B  stateful/order kill: the kill command touches a per-row marker on its first
     invocation and fails on its second. Live baseline is run first, so it passes;
     the mutant run fails because it is the SECOND run, not because of the patch.
     The patch is again a behavior-equivalent comment.
  C  import-crash mutant: a module-level constant is assigned an undefined name,
     which compiles (py_compile clean) and dies with NameError at import, so a
     real exercise command differs on every row for a reason unrelated to the
     named limb.
"""
import json
import os
import sys

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
RA = "corpus/instruments/recheck-audit.py"
SR = "corpus/instruments/source-recheck.py"
FR = "corpus/instruments/frontier-recheck-count.py"

EQ = "  # crit-eq"


def comment_row(row_id, inst, find):
    return {
        "id": row_id,
        "instrument": inst,
        "find": find,
        "replace": find + EQ,
        "kill": "grep -cxF '%s' {inst}" % find,
        "live_exit": 0,
        "signal": "^1$",
        "note": "class A: byte-inspection kill on a behavior-equivalent comment patch",
    }


def state_row(row_id, inst, find):
    marker = ".crit-" + row_id
    return {
        "id": row_id,
        "instrument": inst,
        "find": find,
        "replace": find + EQ,
        "kill": ("if [ -e %s ]; then echo CRIT-SECOND-RUN; exit 7; fi; "
                 "touch %s; echo CRIT-FIRST-RUN; exit 0" % (marker, marker)),
        "live_exit": 0,
        "signal": "CRIT-FIRST-RUN",
        "note": "class B: stateful kill; the live run creates the marker, the mutant run trips it",
    }


def crash_row(row_id, inst, find, name, kill, signal):
    return {
        "id": row_id,
        "instrument": inst,
        "find": find,
        "replace": "%s = _crit_undefined_limb" % name,
        "kill": kill,
        "live_exit": 0,
        "signal": signal,
        "note": "class C: module-level NameError at import; compiles, dies before the limb runs",
    }


LIMBS = [
    comment_row("RA-parse", RA, 'FROZEN_LIMBS = ("parse", "cwd", "paths")'),
    comment_row("RA-cwd", RA, 'STRICT_LIMBS = ("parse", "cwd", "paths", "cdroot", "instrument", "own")'),
    comment_row("RA-paths", RA, 'CD_RE = re.compile(r"^cd[ \\t]+([^&;]+?)[ \\t]*&&")'),
    comment_row("RA-cdroot", RA, 'INSTRUMENT_RE = re.compile(r"corpus/instruments/[A-Za-z0-9_.\\-]+\\.py")'),
    comment_row("RA-instrument", RA, 'BASE_TEST_RE = re.compile(r"test[ \\t]+-[def][ \\t]+~/Projects/")'),
    state_row("RA-own", RA, 'RECHECK_RE = re.compile(r"^recheck:[ \\t]*(.*)$")'),
    state_row("RA-completeness", RA, "def parse_ok(cmd):"),
    state_row("RA-expect-missing", RA, "def load_expected(path):"),
    state_row("RA-expect-unexpected", RA, "def expected_mismatch(root, expected):"),
    crash_row("SR-stem-mismatch", SR, "SCHEMA_VERSION = 1", "SCHEMA_VERSION",
              "python3 {inst} --selftest", "selftest cases=[0-9]+ failures=0"),
    crash_row("SR-occurrence-not-unique", SR,
              'MIN_QUOTE_CHARS = 12   # normalized minimum: a shorter "quote" matches any capture',
              "MIN_QUOTE_CHARS", "python3 {inst} --selftest", "selftest cases=[0-9]+ failures=0"),
    crash_row("FR-missing-entry", FR, 'SOURCE_LINE = re.compile(r"^source:\\s*(S\\d{3,})")',
              "SOURCE_LINE", "python3 {inst} --root {root}", "entries=[0-9]+ pass=[0-9]+ exit=0"),
    crash_row("FR-duplicate-entry", FR, 'RECHECK_SOURCE = re.compile(r"--source\\s+(S\\d{3,})")',
              "RECHECK_SOURCE", "python3 {inst} --root {root}", "entries=[0-9]+ pass=[0-9]+ exit=0"),
]

CONTROLS_HONEST = [
    {"id": "CTL-noop", "instrument": SR, "find": "SCHEMA_VERSION = 1",
     "replace": "SCHEMA_VERSION = 1", "kill": "python3 {inst} --selftest",
     "live_exit": 0, "signal": "selftest cases=[0-9]+ failures=0", "expect": "invalid:noop"},
    {"id": "CTL-nocompile", "instrument": SR, "find": "SCHEMA_VERSION = 1",
     "replace": "SCHEMA_VERSION = (", "kill": "python3 {inst} --selftest",
     "live_exit": 0, "signal": "selftest cases=[0-9]+ failures=0", "expect": "invalid:nocompile"},
    {"id": "CTL-equivalent", "instrument": SR, "find": "MIN_QUOTE_CHARS = 12",
     "replace": "MIN_QUOTE_CHARS = 12  # eq", "kill": "python3 {inst} --selftest",
     "live_exit": 0, "signal": "selftest cases=[0-9]+ failures=0", "expect": "survivor"},
]

# The control hole: the schema names three ids but binds no id to an expect, so
# CTL-equivalent can be a no-op patch that expects invalid:noop.
CONTROLS_DEGENERATE = [
    CONTROLS_HONEST[0],
    CONTROLS_HONEST[1],
    {"id": "CTL-equivalent", "instrument": SR, "find": "MIN_QUOTE_CHARS = 12",
     "replace": "MIN_QUOTE_CHARS = 12", "kill": "python3 {inst} --selftest",
     "live_exit": 0, "signal": "selftest cases=[0-9]+ failures=0", "expect": "invalid:noop"},
]

# Survivor sanity: one honestly-behaving equivalent mutant under an honest kill.
LIMBS_HONEST = [{
    "id": "SR-equivalent-honest",
    "instrument": SR,
    "find": "MIN_QUOTE_CHARS = 12",
    "replace": "MIN_QUOTE_CHARS = 12  # eq",
    "kill": "python3 {inst} --selftest",
    "live_exit": 0,
    "signal": "selftest cases=[0-9]+ failures=0",
    "note": "behavior-equivalent patch, honest exercise kill -> must be survivor",
}]


def check(rows):
    for row in rows:
        text = open(os.path.join(LANE, row["instrument"]), encoding="utf-8").read()
        count = text.count(row["find"])
        print("find-count %-26s %-44s count=%d" % (row["id"], row["instrument"].split("/")[-1], count))
        if count != 1:
            sys.exit("find is not exactly once: %s" % row["id"])


def write(name, limbs, controls):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"version": 1, "limbs": limbs, "controls": controls}, handle, indent=1)
        handle.write("\n")
    print("wrote %s limbs=%d controls=%d" % (name, len(limbs), len(controls)))


if __name__ == "__main__":
    check(LIMBS + CONTROLS_HONEST + LIMBS_HONEST)
    write("degenerate-ledger.json", LIMBS, CONTROLS_HONEST)
    write("degenerate-ledger-controls.json", LIMBS, CONTROLS_DEGENERATE)
    write("honest-survivor-ledger.json", LIMBS_HONEST, CONTROLS_HONEST)
