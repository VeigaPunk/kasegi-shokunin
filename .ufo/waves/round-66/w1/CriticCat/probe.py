#!/usr/bin/env python3
"""Independent, finite public-CLI adversarial probes; not the round's counter.

All generated fixture files stay in the seat scratch. Durable receipts record
commands, committed base identity, fixture hashes, stdout/stderr and actual rc.
No commits, clone, production edits, imports of the instrument, or shell execution.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

BASE = "b6db9e818d322726e39cb441f2179d34d4170275"
LANE = Path("/home/vgpnk/Projects/shokunin/kasegi-shokunin")
SCRATCH = Path("/fast/scratch/hyaku/kasegi-r66/CriticCat")
OUT = LANE / ".ufo/waves/round-66/w1/CriticCat"
ROOT = SCRATCH / "root"
ENV = {**os.environ, "TMPDIR": str(SCRATCH / "tmp"),
       "HYAKU_SCRATCH": str(SCRATCH / "tmp"), "PYTHONDONTWRITEBYTECODE": "1"}
BIG = b"alpha\n" + (b"z" * 1023 + b"\n") * 8192


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(argv, *, cwd=ROOT, timeout=45):
    p = subprocess.run([str(a) for a in argv], cwd=cwd, env=ENV,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    return {"command": [str(a) for a in argv], "cwd": str(cwd), "rc": p.returncode,
            "stdout": p.stdout.decode("utf-8", "replace"),
            "stderr": p.stderr.decode("utf-8", "replace")}


def native(stages, input_name=None):
    processes, files = [], []
    previous = None
    try:
        if input_name:
            previous = (ROOT / input_name).open("rb")
            files.append(previous)
        for argv in stages:
            err = tempfile.TemporaryFile(dir=ENV["TMPDIR"])
            files.append(err)
            p = subprocess.Popen(argv, cwd=ROOT, env=ENV, stdin=previous,
                                 stdout=subprocess.PIPE, stderr=err)
            processes.append((p, err))
            if previous is not None:
                previous.close()
            previous = p.stdout
        out, _ = processes[-1][0].communicate(timeout=20)
        for p, _ in processes[:-1]:
            p.wait(timeout=20)
        errors = []
        for _, err in processes:
            err.seek(0)
            errors.append(err.read().decode("utf-8", "replace"))
        return {"argv": stages, "input": input_name,
                "stage_rc": [p.returncode for p, _ in processes],
                "stdout": out.decode("utf-8", "replace"), "stderr": errors}
    finally:
        for p, _ in processes:
            if p.poll() is None:
                p.kill()
            p.wait()
            if p.stdout is not None:
                p.stdout.close()
        for f in files:
            f.close()


def fixtures():
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "corpus/instruments").mkdir(parents=True, exist_ok=True)
    files = {"big.txt": BIG, "other.txt": b"omega\n", "small.txt": b"alpha\n",
             "g.txt": b"35\n", "one two.txt": BIG, "pipe|and&&.txt": BIG,
             "-dash.txt": BIG, "--": BIG, "alternate.txt": BIG}
    files["corpus/instruments/wrapper.py"] = (
        b"import subprocess\n"
        b"p = subprocess.run(['cat', 'missing.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)\n"
        b"print('alpha')\n")
    files["corpus/instruments/final7.py"] = b"print('alpha')\nraise SystemExit(7)\n"
    files["corpus/instruments/pipe.py"] = (
        b"import signal, sys\nsignal.signal(signal.SIGPIPE, signal.SIG_DFL)\n"
        b"sys.stdout.write('alpha\\n' + ('x' * 1023 + '\\n') * 8192)\n"
        b"sys.stdout.flush()\n")
    for name, data in files.items():
        (ROOT / name).write_bytes(data)
    (ROOT / "bad-dir").mkdir(exist_ok=True)
    return [{"path": name, "bytes": len(data), "sha256": digest(data)}
            for name, data in sorted(files.items())]


def cases():
    head = ["head", "-n", "1"]
    items = []

    def add(name, derive, cat_argv, expected_rc, reason=None, *, input_name=None,
            want="alpha", stages=None, boundary=False):
        items.append({"name": name, "derive": derive, "stages": stages or [cat_argv, head],
                      "input": input_name, "expected_rc": expected_rc,
                      "reason": reason, "want": want, "boundary": boundary})

    sig = "derive-upstream-signal-13"
    add("two-missing", "cat big.txt missing.txt | head -n 1", ["cat", "big.txt", "missing.txt"], 1, sig)
    add("two-existing", "cat big.txt other.txt | head -n 1", ["cat", "big.txt", "other.txt"], 1, sig)
    add("renamed-multi", "cat alternate.txt other.txt | head -n 1", ["cat", "alternate.txt", "other.txt"], 1, sig)
    add("quoted-head-multi", "c'at' big.txt missing.txt | head -n 1", ["cat", "big.txt", "missing.txt"], 1, sig)
    add("escaped-arg-multi", r"cat bi\g.txt miss\ing.txt|head -n 1", ["cat", "big.txt", "missing.txt"], 1, sig)
    add("quoted-args-multi", "cat 'big.txt' \"missing.txt\" | head -n 1", ["cat", "big.txt", "missing.txt"], 1, sig)
    add("single-big", "cat big.txt | head -n 1", ["cat", "big.txt"], 0)
    add("stdin-only", "cat < big.txt | head -n 1", ["cat"], 0, input_name="big.txt")
    add("stdin-dash", "cat - < big.txt | head -n 1", ["cat", "-"], 0, input_name="big.txt")
    add("single-blank", "cat 'one two.txt' | head -n 1", ["cat", "one two.txt"], 0)
    add("single-operators", "cat 'pipe|and&&.txt'|head -n 1", ["cat", "pipe|and&&.txt"], 0)
    add("single-escaped-blank", r"cat one\ two.txt|head -n 1", ["cat", "one two.txt"], 0)
    add("separator-single", "cat -- big.txt | head -n 1", ["cat", "--", "big.txt"], 0)
    add("separator-stdin", "cat -- < big.txt | head -n 1", ["cat", "--"], 0, input_name="big.txt")
    add("separator-multi", "cat -- big.txt missing.txt | head -n 1", ["cat", "--", "big.txt", "missing.txt"], 1, sig)
    add("separator-dash-name", "cat -- -dash.txt | head -n 1", ["cat", "--", "-dash.txt"], 0)
    add("separator-double-dash-name", "cat -- -- | head -n 1", ["cat", "--", "--"], 0)
    add("file-and-stdin-multi", "cat big.txt - < other.txt | head -n 1", ["cat", "big.txt", "-"], 1, sig, input_name="other.txt")
    add("stdin-and-file-multi", "cat - other.txt < big.txt | head -n 1", ["cat", "-", "other.txt"], 1, sig, input_name="big.txt")
    add("two-small", "cat small.txt other.txt | head -n 1", ["cat", "small.txt", "other.txt"], 0)
    add("missing-first", "cat missing.txt big.txt | head -n 1", ["cat", "missing.txt", "big.txt"], 1, sig)
    add("directory-first", "cat bad-dir big.txt | head -n 1", ["cat", "bad-dir", "big.txt"], 1, sig)
    add("single-read-error", "cat bad-dir | wc -l", ["cat", "bad-dir"], 1, "derive-upstream-exit-1", want="0", stages=[["cat", "bad-dir"], ["wc", "-l"]])
    add("single-options-conservative", "cat -u big.txt | head -n 1", ["cat", "-u", "big.txt"], 1, sig, boundary=True)
    add("wrapper-hides-error", "python3 corpus/instruments/wrapper.py | head -n 1", None, 0,
        stages=[["python3", "corpus/instruments/wrapper.py"], head], boundary=True)
    add("other-head-multi", "head -q -n 100000000 big.txt missing.txt | head -n 1", None, 0,
        stages=[["head", "-q", "-n", "100000000", "big.txt", "missing.txt"], head], boundary=True)
    add("other-python-sigpipe", "python3 corpus/instruments/pipe.py | head -n 1", None, 0,
        stages=[["python3", "corpus/instruments/pipe.py"], head], boundary=True)
    add("final-precedence", "cat big.txt missing.txt | python3 corpus/instruments/final7.py", None, 1,
        "derive-exit-7", stages=[["cat", "big.txt", "missing.txt"], ["python3", "corpus/instruments/final7.py"]])
    add("separator-double-dash-multi", "cat -- -- missing.txt | head -n 1", ["cat", "--", "--", "missing.txt"], 1, sig)
    add("empty-operand-multi", "cat big.txt '' | head -n 1", ["cat", "big.txt", ""], 1, sig)
    return items


def check(gate, case):
    ledger = {"figures": [{"id": case["name"], "record": "fixture:1",
                           "recorded": case["want"], "want": case["want"],
                           "derive": case["derive"]}]}
    data = (json.dumps(ledger, sort_keys=True) + "\n").encode()
    lp = ROOT / "ledger.json"
    lp.write_bytes(data)
    result = run([sys.executable, "-B", gate, "--ledger", lp, "--root", ROOT])
    result.update({"case": case, "ledger_sha256": digest(data),
                   "native": native(case["stages"], case["input"])})
    result["matches_candidate_predicate"] = (
        result["rc"] == case["expected_rc"] and
        (not case["reason"] or "reason=" + case["reason"] + " stale" in result["stdout"]))
    return result


def save(name, document):
    path = OUT / "receipts" / (name + ".json")
    path.write_text(json.dumps(document, indent=2) + "\n")
    lines = ["BASE=" + BASE, "instrument=" + document["instrument"],
             "instrument_sha256=" + document["instrument_sha256"],
             "harness_sha256=" + document["harness_sha256"],
             "TMPDIR=" + ENV["TMPDIR"]]
    for row in document["runs"]:
        lines.extend(["", "CASE " + row["case"]["name"],
                      "derive=" + row["case"]["derive"],
                      "ledger_sha256=" + row["ledger_sha256"],
                      "$ " + shlex.join(row["command"]),
                      "stdout:", row["stdout"], "stderr:", row["stderr"],
                      "rc=" + str(row["rc"]),
                      "NATIVE " + json.dumps(row["native"], sort_keys=True),
                      "candidate_expected_rc=" + str(row["case"]["expected_rc"]),
                      "matches_candidate_predicate=" + str(row["matches_candidate_predicate"])])
    (OUT / "receipts" / (name + ".txt")).write_text("\n".join(lines) + "\n")
    print("RECEIPT", path)
    for row in document["runs"]:
        print(row["case"]["name"], "native=" + str(row["native"]["stage_rc"]),
              "gate_rc=" + str(row["rc"]), "matches=" + str(row["matches_candidate_predicate"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instrument", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--pair-only", action="store_true")
    args = ap.parse_args()
    SCRATCH.mkdir(parents=True, exist_ok=True)
    (SCRATCH / "tmp").mkdir(exist_ok=True)
    (OUT / "receipts").mkdir(parents=True, exist_ok=True)
    gate = Path(args.instrument).resolve()
    fixture_manifest = fixtures()
    selected = cases()
    if args.pair_only:
        selected = [c for c in selected if c["name"] in ("two-missing", "two-small", "single-big", "stdin-only")]
    runs = [check(gate, case) for case in selected]
    if not args.pair_only:
        # One command, identical ledger and paths; only operand bytes change.
        same = next(c for c in cases() if c["name"] == "two-existing")
        small = dict(same, expected_rc=0, reason=None)
        (ROOT / "big.txt").write_bytes(b"alpha\n")
        row = check(gate, small)
        row["fixture_delta"] = {"big.txt": {"sha256": digest(b"alpha\n"), "bytes": 6}}
        runs.append(row)
        (ROOT / "big.txt").write_bytes(BIG)
    document = {"base": BASE, "instrument": str(gate),
                "instrument_sha256": digest(gate.read_bytes()),
                "harness_sha256": digest(Path(__file__).read_bytes()),
                "fixture_manifest": fixture_manifest, "runs": runs}
    save(args.label, document)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
