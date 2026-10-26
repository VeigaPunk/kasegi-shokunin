#!/usr/bin/env bash
# check-g4.sh — reference checker for the round-39 G4 seat-identity limb.
#
#   check-g4.sh TREE
#
# TREE is an export root (a `git archive` extraction or any tree). The wave dir
# is fixed at `.ufo/waves/round-39`. Prints exactly one line
#
#   G4 payload=<counters> closed=<0|1>
#
# and exits 0 when closed, 1 when red. Nothing is written; the tree is opened
# read-only.
#
# Frozen rule (round-39 claims.json, C1 G4): for every tracked
# `.ufo/waves/round-39/*-dispatch.json` the sibling `-results.json` parses as
# JSON, lists exactly len(taskCall.tasks) seats with distinct agent ids (a
# zero-task dispatch is RED), and no duplicate identity satisfies the count.
#
# Identity field: `name`. In the round-38 results file (73 seats) `agent` is
# the role (9 distinct values: executor, reviewer, critic, scribe, ...) and
# `name` is the seat identity (73 distinct values, exactly the dispatch name
# set); `name` is therefore the only field that can satisfy the rule.
#
# Counter vocabulary:
#   dispatches= D  number of `*-dispatch.json` files in the wave dir
#   pairs=      P  dispatches whose results file was found (sibling
#                  `<base>-results.json`, else family `<wave>-results.json`
#                  in the same dir with the same `wave` value)
#   parsed=     J  pairs where both files are JSON and yield a
#                  `taskCall.tasks` list / a `results` list
#   tasks=      T  sum of len(taskCall.tasks) over dispatch-parsed entries
#   entries=    E  sum of len(results) over results-parsed entries
#   ids=        U  sum of distinct non-empty string `name` values over the
#                  same entries (an entry without one contributes nothing, so
#                  U falls below E)
#   ids-ok=     I  dispatches satisfying: parsed pair, tasks >= 1,
#                  len(results) == len(tasks), every entry carries a non-empty
#                  string `name`, distinct names == len(results)
#   read=          ok when the wave dir is a readable directory, fail otherwise
# A counter is `-` when no entry was parsed for it. closed=1 iff read=ok and
# dispatches >= 1 and ids-ok == dispatches.
set -u
[ "$#" -eq 1 ] || { printf 'usage: check-g4.sh TREE\n' >&2; exit 2; }

exec python3 - "$1" <<'PY'
import json
import os
import sys

WAVE_REL = os.path.join(".ufo", "waves", "round-39")
ID_FIELD = "name"


def load(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return True, json.load(fh)
    except Exception:
        return False, None


def tasks_of(doc):
    if not isinstance(doc, dict):
        return None, None
    wave = doc.get("wave")
    wave = wave if isinstance(wave, str) else None
    tcl = doc.get("taskCall")
    if not isinstance(tcl, dict):
        return None, wave
    tasks = tcl.get("tasks")
    return (tasks if isinstance(tasks, list) else None), wave


def results_of(doc):
    if not isinstance(doc, dict):
        return None
    rows = doc.get("results")
    return rows if isinstance(rows, list) else None


def ids_of(rows):
    """Return (distinct-able names, all-rows-carried-a-valid-identity)."""
    out = []
    ok = True
    for row in rows:
        if not isinstance(row, dict):
            ok = False
            continue
        val = row.get(ID_FIELD)
        if not isinstance(val, str) or val == "":
            ok = False
            continue
        out.append(val)
    return out, ok


def main(tree):
    wdir = os.path.join(tree, WAVE_REL)
    read = "fail"
    names = None
    if os.path.isdir(wdir) and os.access(wdir, os.R_OK | os.X_OK):
        try:
            names = sorted(os.listdir(wdir))
        except OSError:
            names = None
    if names is not None:
        read = "ok"

    disp = 0
    pairs = 0
    parsed = 0
    ids_ok = 0
    tasks_sum = 0
    tasks_known = False
    entries_sum = 0
    entries_known = False
    ids_sum = 0

    for name in names or []:
        if not name.endswith("-dispatch.json"):
            continue
        dpath = os.path.join(wdir, name)
        if not os.path.isfile(dpath):
            continue
        disp += 1
        base = name[: -len("-dispatch.json")]
        ok_d, ddoc = load(dpath)
        tasks, wave = tasks_of(ddoc) if ok_d else (None, None)
        if tasks is not None:
            tasks_sum += len(tasks)
            tasks_known = True

        cands = [base + "-results.json"]
        if wave:
            cands.append(wave + "-results.json")
        rpath = None
        for cand in cands:
            if os.path.isfile(os.path.join(wdir, cand)):
                rpath = os.path.join(wdir, cand)
                break
        if rpath is None:
            continue
        pairs += 1

        ok_r, rdoc = load(rpath)
        rows = results_of(rdoc) if ok_r else None
        if rows is None:
            continue
        entries_sum += len(rows)
        entries_known = True
        ids, ids_clean = ids_of(rows)
        ids_sum += len(set(ids))
        if tasks is None:
            continue
        parsed += 1

        if (
            len(tasks) >= 1
            and len(rows) == len(tasks)
            and ids_clean
            and len(set(ids)) == len(rows)
        ):
            ids_ok += 1

    unknown = "-"
    payload = "dispatches=%s,pairs=%s,parsed=%s,tasks=%s,entries=%s,ids=%s,ids-ok=%s,read=%s" % (
        disp,
        pairs,
        parsed,
        tasks_sum if tasks_known else unknown,
        entries_sum if entries_known else unknown,
        ids_sum if entries_known else unknown,
        ids_ok,
        read,
    )
    closed = read == "ok" and disp >= 1 and ids_ok == disp
    print("G4 payload=%s closed=%s" % (payload, "1" if closed else "0"))
    return 0 if closed else 1


sys.exit(main(sys.argv[1]))
PY
