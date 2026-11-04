"""Read-only stage-status diagnostic over a figure-audit ledger.

Re-executes each ledger derive with the gate's own parser (imported, never
altered) and reports EVERY stage's returncode, so a stage that terminates by
signal (-N) is visible even though the gate ignores negative statuses.
Stdout of the final stage is discarded; no files are written.
"""
import importlib.util
import json
import os
import subprocess
import sys

GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "..", "corpus", "instruments", "figure-audit.py")
spec = importlib.util.spec_from_file_location("figure_audit_gate", GATE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

EARLY = {"head"}
GREP_EARLY_FLAGS = ("-q", "-m", "-l", "-L")


def early_exit(argv):
    if argv[0] == "head":
        return True
    if os.path.basename(argv[0]) == "grep":
        return any(t == "-q" or t.startswith("-m") or t in ("-l", "-L")
                   for t in argv[1:])
    return False


def run_pipeline(pipeline, root):
    procs, heads, files, prev = [], [], [], None
    try:
        for argv, input_path in pipeline:
            stdin = prev
            if input_path is not None:
                stdin = open(os.path.join(root, input_path), "rb")
                files.append(stdin)
            p = subprocess.Popen(argv, cwd=root, stdin=stdin,
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            procs.append(p)
            heads.append(argv[0])
            if prev is not None:
                prev.close()
            prev = p.stdout
        procs[-1].communicate(timeout=300)
        for p in procs[:-1]:
            p.wait(timeout=300)
    finally:
        for p in procs:
            if p.poll() is None:
                p.kill()
        for p in procs:
            p.wait()
            if p.stdout is not None:
                p.stdout.close()
        for f in files:
            f.close()
    return [p.returncode for p in procs]


def main():
    ledger, root = sys.argv[1], sys.argv[2]
    reps = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    doc = json.load(open(ledger))
    figs = doc["figures"]
    neg_events = []
    sigpipe = []
    structural = []
    stages_total = 0
    for ent in figs:
        plan = gate.parse_derive(root, ent["derive"])
        assert plan is not None, "derive refused: %s" % ent["id"]
        first_status = []
        for rep in range(reps):
            for pipeline in plan:
                codes = run_pipeline(pipeline, root)
                stages_total += len(codes)
                if rep == 0:
                    first_status.append((pipeline, codes))
                for idx, code in enumerate(codes):
                    if code is not None and code < 0:
                        neg_events.append((ent["id"], rep, idx, len(pipeline), code))
                        if code == -13:
                            sigpipe.append((ent["id"], rep, idx, len(pipeline)))
        group_vecs = []
        for gi, (pipeline, codes) in enumerate(first_status):
            group_vecs.append("%d:[%s] final=%s"
                              % (gi, ",".join(str(c) for c in codes),
                                 pipeline[-1][0][0]))
            eligible = []
            for idx, (argv, _inp) in enumerate(pipeline[:-1]):
                if any(early_exit(l[0]) for l in pipeline[idx + 1:]):
                    eligible.append((idx, argv[0]))
            if eligible:
                structural.append((ent["id"], pipeline, eligible))
        print("STAGES id=%s groups=%d %s"
              % (ent["id"], len(first_status), " ".join(group_vecs)))
    print("SUMMARY figures=%d reps=%d stage_runs=%d negative_total=%d sigpipe_total=%d"
          % (len(figs), reps, stages_total, len(neg_events), len(sigpipe)))
    for ev in neg_events[:40]:
        print("NEG id=%s rep=%d stage=%d/%d code=%d" % ev)
    print("STRUCTURAL early-exit-downstream figures=%d" % len(structural))
    for fid, pipeline, eligible in structural:
        print("EARLY id=%s stage_indexes=%s chain=%s"
              % (fid, ",".join(str(i) for i, _ in eligible),
                 " | ".join(a[0] for a, _ in pipeline)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
