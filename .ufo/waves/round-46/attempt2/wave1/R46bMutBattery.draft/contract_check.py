#!/usr/bin/env python3
"""contract_check.py — the detector for mutation-testing r46-mutbat.py itself.

TIER D1 — OUTPUT CONTRACT: the runner's OWN stdout plus its process exit status.
No external reference, no outside knowledge, no filesystem beyond what stdout says.
Every rule is either stated in the runner's own docstring/OUTPUT section or is a
relation between lines the runner itself prints.

The runner's own grading predicate (corpus/instruments/r46-mutbat.py:166-174) is:

    if mf >= 1:            verdict = "caught"
    elif <in eq map>:      verdict = "equivalent"
    else:                  verdict = "uncaught"

The D1 rules below are the stdout-visible projection of that predicate plus the
counting relations between the summary line and the per-mutant lines:

  R1  every stdout line matches one of the runner's three printed line shapes
      (`mutant=...`, `mutbat counter=...`, `mutbat counter=... BASELINE-DIRTY ...`)
  R2  per graded counter: the number of per-mutant lines == the summary's mutants= count
  R3  per graded counter: the summary's caught/equivalent/uncaught counts == the COUNT of
      per-mutant lines carrying that verdict, and caught+equivalent+uncaught == mutants
  R4  per mutant line: verdict=caught  <=>  mutant_failures >= 1
  R5  per mutant line: verdict=equivalent =>  mutant_failures < 1
  R6  per mutant line: verdict=uncaught  =>  mutant_failures < 1
  R7  a BASELINE-DIRTY counter contributes no per-mutant lines and no summary line
  R8  the exit status is justified by the stdout: exit 0 requires every requested
      counter to have a summary line, every summary to report uncaught=0, and no
      BASELINE-DIRTY line; exit 1 requires that at least one of those is violated
  R9  per graded counter: every per-mutant line carries the same baseline_failures
      value as the summary line, and that value is 0
  R10 the ids of the per-mutant lines == the ids of that counter's mutant table, in order

  Rules R4/R5/R6 apply to EVERY printed per-mutant line, whether or not the run
  reached the summary line for that counter (an aborted run still prints lines).

TIER X — EXTERNAL-INPUT rules (need the --equivalent map and the filesystem: knowledge
outside the stdout).  Reported separately and never counted as D1:
  X1  verdict=equivalent requires a committed proof file that exists

TIER O — RUNNER OBSERVATIONS (properties of the runner's own output that a reviewer
sees but that the PRISTINE runner also exhibits: reported, never counted as a kill):
  O1  a per-mutant line carries mutant_failures < 0, the runner's undocumented
      "the selftest produced no verdict at all" sentinel

Usage: contract_check.py OUTPUT EXITCODE [--expect-counters c1,c2] [--mutants c1=20,c2=21]
            [--ids c1=ids.txt,c2=ids.txt] [--equivalent map.json]
Exit 0 = no D1 violation; 1 = D1 violation (each printed).
"""
import argparse
import json
import os
import re
import sys

PER = re.compile(r"^mutant=(\S+) baseline_failures=(-?\d+) mutant_failures=(-?\d+) verdict=(\S+)$")
SUM = re.compile(r"^mutbat counter=(\S+) mutants=(\d+) caught=(\d+) equivalent=(\d+) uncaught=(\d+) baseline_failures=(-?\d+)$")
DIRTY = re.compile(r"^mutbat counter=(\S+) BASELINE-DIRTY baseline_failures=(-?\d+)$")


def parse(path):
    per, summ, dirty, other = [], [], [], []
    for ln in open(path, encoding="utf-8"):
        ln = ln.rstrip("\n")
        if not ln.strip():
            continue
        m = PER.match(ln)
        if m:
            per.append(dict(id=m.group(1), baseline=int(m.group(2)), mf=int(m.group(3)), verdict=m.group(4)))
            continue
        m = SUM.match(ln)
        if m:
            summ.append(dict(counter=m.group(1), mutants=int(m.group(2)), caught=int(m.group(3)),
                              equivalent=int(m.group(4)), uncaught=int(m.group(5)), baseline=int(m.group(6))))
            continue
        m = DIRTY.match(ln)
        if m:
            dirty.append(dict(counter=m.group(1), baseline=int(m.group(2))))
            continue
        other.append(ln)
    return per, summ, dirty, other


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("output")
    ap.add_argument("exitcode", type=int)
    ap.add_argument("--expect-counters", default="")
    ap.add_argument("--mutants", default="")
    ap.add_argument("--ids", default="")
    ap.add_argument("--equivalent", default=None)
    ap.add_argument("--label", default="")
    a = ap.parse_args(argv)

    per, summ, dirty, other = parse(a.output)
    v, x, o = [], [], []
    exp_counters = [c for c in a.expect_counters.split(",") if c]
    exp_mutants = {}
    for kv in a.mutants.split(","):
        if kv:
            k, n = kv.split("=")
            exp_mutants[k] = int(n)
    ids = {}
    if a.ids:
        for kv in a.ids.split(","):
            if kv:
                k, p = kv.split("=")
                ids[k] = [l.strip() for l in open(p, encoding="utf-8") if l.strip()]
    eqmap = {}
    if a.equivalent:
        eqmap = json.load(open(a.equivalent, encoding="utf-8"))

    for ln in other:
        v.append("R1 unexpected stdout line: %r" % ln)

    # ---- attribute per-mutant lines to counters by the runner's print order --------
    order = exp_counters or []
    buckets = {c: [] for c in order}
    idx = 0
    for ln in open(a.output, encoding="utf-8"):
        m = PER.match(ln.rstrip("\n"))
        if m:
            c = order[idx] if idx < len(order) else (order[-1] if order else "?")
            buckets.setdefault(c, []).append(dict(id=m.group(1), baseline=int(m.group(2)),
                                                   mf=int(m.group(3)), verdict=m.group(4)))
        elif SUM.match(ln.rstrip("\n")) or DIRTY.match(ln.rstrip("\n")):
            idx += 1

    for c in order:
        lines = buckets.get(c, [])
        s = next((y for y in summ if y["counter"] == c), None)
        d = next((y for y in dirty if y["counter"] == c), None)
        if d and s:
            v.append("R7 counter %s is both BASELINE-DIRTY and graded" % c)
        if d and not s:
            if lines:
                v.append("R7 counter %s is BASELINE-DIRTY but printed %d per-mutant lines" % (c, len(lines)))
            continue
        # ---- per-mutant-line rules: every printed line, graded or not -------------
        for ln in lines:
            if ln["mf"] < 0:
                o.append("O1 counter %s: mutant %s carries mutant_failures=%d (the selftest produced no verdict)"
                         % (c, ln["id"], ln["mf"]))
            if ln["verdict"] == "caught" and not (ln["mf"] >= 1):
                v.append("R4 counter %s: mutant %s verdict=caught but mutant_failures=%d" % (c, ln["id"], ln["mf"]))
            if ln["verdict"] == "equivalent" and not (ln["mf"] < 1):
                v.append("R5 counter %s: mutant %s verdict=equivalent but mutant_failures=%d" % (c, ln["id"], ln["mf"]))
            if ln["verdict"] == "uncaught" and not (ln["mf"] < 1):
                v.append("R6 counter %s: mutant %s verdict=uncaught but mutant_failures=%d" % (c, ln["id"], ln["mf"]))
            if ln["verdict"] == "equivalent":
                if ln["id"] not in eqmap:
                    x.append("X1 counter %s: mutant %s verdict=equivalent but no --equivalent proof entry" % (c, ln["id"]))
                elif not os.path.isfile(eqmap[ln["id"]]):
                    x.append("X1 counter %s: mutant %s verdict=equivalent but proof file %s does not exist" % (c, ln["id"], eqmap[ln["id"]]))
            if ln["verdict"] == "uncaught" and ln["id"] in eqmap and os.path.isfile(eqmap[ln["id"]]):
                x.append("X1 counter %s: mutant %s verdict=uncaught though a committed proof exists" % (c, ln["id"]))
        if not s:
            # the counter was neither graded nor reported dirty: the run aborted before
            # this counter (a legitimate loud abort; R8 accounts for the exit status)
            continue
        if len(lines) != s["mutants"]:
            v.append("R2 counter %s: summary mutants=%d but %d per-mutant lines were printed" % (c, s["mutants"], len(lines)))
        if exp_mutants.get(c) is not None and s["mutants"] != exp_mutants[c]:
            v.append("R2 counter %s: summary mutants=%d but the mutant table has %d" % (c, s["mutants"], exp_mutants[c]))
        tally = {"caught": 0, "equivalent": 0, "uncaught": 0}
        for ln in lines:
            if ln["verdict"] not in tally:
                v.append("R3 counter %s: unknown verdict %r" % (c, ln["verdict"]))
                continue
            tally[ln["verdict"]] += 1
            if ln["baseline"] != s["baseline"]:
                v.append("R9 counter %s: mutant %s baseline_failures=%d but the summary says %d" % (c, ln["id"], ln["baseline"], s["baseline"]))
        for k in ("caught", "equivalent", "uncaught"):
            if tally[k] != s[k]:
                v.append("R3 counter %s: summary %s=%d but %d per-mutant lines say %s" % (c, k, s[k], tally[k], k))
        if s["caught"] + s["equivalent"] + s["uncaught"] != s["mutants"]:
            v.append("R3 counter %s: caught+equivalent+uncaught=%d != mutants=%d"
                     % (c, s["caught"] + s["equivalent"] + s["uncaught"], s["mutants"]))
        if s["baseline"] != 0:
            v.append("R9 counter %s: summary baseline_failures=%d for a graded counter" % (c, s["baseline"]))
        if ids.get(c) is not None:
            got = [ln["id"] for ln in lines]
            if got != ids[c]:
                v.append("R10 counter %s: per-mutant ids differ from the mutant table (%d printed vs %d in table, order %s)"
                         % (c, len(got), len(ids[c]), "same" if set(got) == set(ids[c]) else "different-set"))

    # ---- R8: the exit status must be justified by the stdout ----------------------
    missing = [c for c in exp_counters if c not in [s["counter"] for s in summ]
               and c not in [d["counter"] for d in dirty]]
    exit_justified_1 = bool(dirty) or any(s["uncaught"] > 0 for s in summ) or bool(missing)
    if a.exitcode == 0:
        if missing:
            v.append("R8 exit status 0 but counter(s) %s produced no summary line" % ",".join(missing))
        if dirty:
            v.append("R8 exit status 0 but counter(s) %s were BASELINE-DIRTY" % ",".join([d["counter"] for d in dirty]))
        if any(s["uncaught"] > 0 for s in summ):
            v.append("R8 exit status 0 but a summary reports uncaught>0")
    elif a.exitcode == 1:
        if not exit_justified_1:
            v.append("R8 exit status 1 but the stdout justifies nothing (no dirty baseline, no uncaught>0, no missing summary)")
    else:
        v.append("R8 exit status %d is outside {0,1}" % a.exitcode)

    label = a.label or os.path.basename(a.output)
    if v:
        print("CONTRACT-FAIL %s" % label)
        for y in v:
            print("  VIOLATION %s" % y)
    else:
        print("CONTRACT-OK %s" % label)
    for y in x:
        print("  EXTERNAL %s" % y)
    for y in o:
        print("  OBSERVATION %s" % y)
    return 1 if v else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
