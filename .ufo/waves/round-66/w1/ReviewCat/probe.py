#!/usr/bin/env python3
"""ReviewCat's independent public-CLI matrix; no executor code is imported.
Run only inside this seat's one guarded BASE clone. Native status vectors are
separate observations, not claimed as the public gate's hidden wait vector.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

BASE = "b6db9e818d322726e39cb441f2179d34d4170275"
SEAT = Path("/fast/scratch/hyaku/kasegi-r66/ReviewCat")
DURABLE = Path("/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-66/w1/ReviewCat")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def case(name, derive, stages, want="alpha", redir=None, change=False, conservative=False, reason=None, rc=0, note=""):
    return dict(name=name, derive=derive, stages=stages, want=want,
                redir=redir, change=change, conservative=conservative,
                reason=reason, rc=rc, note=note)


def cases():
    h = ["head", "-n", "1"]
    cat = lambda *args: [["cat", *args], h]
    return [
        case("single-large", "cat big.txt | head -n 1", cat("big.txt")),
        case("stdin-only-large", "cat < big.txt | head -n 1", cat(), redir="big.txt"),
        case("dash-only-large", "cat - < big.txt | head -n 1", cat("-"), redir="big.txt"),
        case("separator-only-stdin", "cat -- < big.txt | head -n 1", cat("--"), redir="big.txt"),
        case("separator-single", "cat -- big.txt | head -n 1", cat("--", "big.txt")),
        case("separator-dash-stdin", "cat -- - < big.txt | head -n 1", cat("--", "-"), redir="big.txt"),
        case("single-spaced-name", "cat 'big space.txt' | head -n 1", cat("big space.txt")),
        case("single-escaped-name", r"cat big\ space.txt | head -n 1", cat("big space.txt")),
        case("single-operator-name", "cat 'big|name.txt' | head -n 1", cat("big|name.txt")),
        case("literal-option-name", "cat -- -n | head -n 1", cat("--", "-n")),
        case("literal-separator-name", "cat -- -- | head -n 1", cat("--", "--")),
        case("later-missing-large", "cat big.txt missing.txt | head -n 1", cat("big.txt", "missing.txt"), change=True),
        case("earlier-missing-large", "cat missing.txt big.txt | head -n 1", cat("missing.txt", "big.txt"), change=True),
        case("two-existing-large", "cat big.txt other.txt | head -n 1", cat("big.txt", "other.txt"), change=True, note="Conservative refusal: both operands exist; no demonstrated missing-input failure."),
        case("same-file-twice", "cat big.txt big.txt | head -n 1", cat("big.txt", "big.txt"), change=True),
        case("separator-two-existing", "cat -- big.txt other.txt | head -n 1", cat("--", "big.txt", "other.txt"), change=True),
        case("separator-later-missing", "cat -- big.txt missing.txt | head -n 1", cat("--", "big.txt", "missing.txt"), change=True),
        case("separator-earlier-missing", "cat -- missing.txt big.txt | head -n 1", cat("--", "missing.txt", "big.txt"), change=True),
        case("dash-before-file", "cat - big.txt < big.txt | head -n 1", cat("-", "big.txt"), redir="big.txt", change=True),
        case("file-before-dash", "cat big.txt - < big.txt | head -n 1", cat("big.txt", "-"), redir="big.txt", change=True),
        case("two-dashes", "cat - - < big.txt | head -n 1", cat("-", "-"), redir="big.txt", change=True),
        case("stdin-before-missing", "cat - missing.txt < big.txt | head -n 1", cat("-", "missing.txt"), redir="big.txt", change=True),
        case("missing-before-stdin", "cat missing.txt - < big.txt | head -n 1", cat("missing.txt", "-"), redir="big.txt", change=True),
        case("option-u-single", "cat -u big.txt | head -n 1", cat("-u", "big.txt"), conservative=True),
        case("option-n-single", "cat -n big.txt | head -n 1", cat("-n", "big.txt"), want="1\talpha", conservative=True),
        case("long-option-single", "cat --number big.txt | head -n 1", cat("--number", "big.txt"), want="1\talpha", conservative=True),
        case("option-and-separator", "cat -u -- big.txt | head -n 1", cat("-u", "--", "big.txt"), conservative=True),
        case("option-multi", "cat -u big.txt missing.txt | head -n 1", cat("-u", "big.txt", "missing.txt"), change=True),
        case("single-small", "cat small.txt | head -n 1", cat("small.txt")),
        case("two-existing-small", "cat small.txt other-small.txt | head -n 1", cat("small.txt", "other-small.txt")),
        case("later-missing-small", "cat small.txt missing.txt | head -n 1", cat("small.txt", "missing.txt"), rc=1, reason="derive-upstream-exit-1"),
        case("earlier-missing-small", "cat missing.txt small.txt | head -n 1", cat("missing.txt", "small.txt"), rc=1, reason="derive-upstream-exit-1"),
        case("missing-only", "cat missing.txt | wc -l", [["cat", "missing.txt"], ["wc", "-l"]], want="0", rc=1, reason="derive-upstream-exit-1"),
        case("multi-drained", "cat big.txt other.txt | wc -l", [["cat", "big.txt", "other.txt"], ["wc", "-l"]], want="1398103"),
        case("multi-drained-later-missing", "cat big.txt missing.txt | wc -l", [["cat", "big.txt", "missing.txt"], ["wc", "-l"]], want="1398102", rc=1, reason="derive-upstream-exit-1"),
        case("grep-nomatch", "grep absent big.txt | wc -l", [["grep", "absent", "big.txt"], ["wc", "-l"]], want="0"),
        case("other-head-sigpipe", "head -c 8388612 big.txt | head -n 1", [["head", "-c", "8388612", "big.txt"], h]),
        case("other-cut-sigpipe", "cut -c 1-5 big.txt | head -n 1", [["cut", "-c", "1-5", "big.txt"], h]),
        case("upstream-positive-seven", "python3 corpus/instruments/fail7.py | wc -l", [["python3", "corpus/instruments/fail7.py"], ["wc", "-l"]], want="0", rc=1, reason="derive-upstream-exit-7"),
        case("upstream-signal-fifteen", "python3 corpus/instruments/term.py | wc -l", [["python3", "corpus/instruments/term.py"], ["wc", "-l"]], want="0", rc=1, reason="derive-upstream-signal-15"),
        case("final-error-precedence", "cat big.txt missing.txt | grep '['", [["cat", "big.txt", "missing.txt"], ["grep", "["]], want="0", rc=1, reason="derive-exit-2"),
        case("middle-multi-cat", "head -c 8388612 big.txt | cat - big.txt | head -n 1", [["head", "-c", "8388612", "big.txt"], ["cat", "-", "big.txt"], h], change=True),
        case("middle-single-cat", "head -c 8388612 big.txt | cat - | head -n 1", [["head", "-c", "8388612", "big.txt"], ["cat", "-"], h]),
    ]


def native(probe, root, env):
    processes = []
    previous = None
    files = []
    errors = []
    try:
        for index, argv in enumerate(probe["stages"]):
            stdin = previous
            if index == 0 and probe["redir"]:
                stdin = open(root / probe["redir"], "rb")
                files.append(stdin)
            err = open(SEAT / "tmp" / (probe["name"] + f"-{index}.stderr"), "w+b")
            errors.append(err)
            p = subprocess.Popen(argv, cwd=root, env=env, stdin=stdin,
                                 stdout=subprocess.PIPE, stderr=err)
            processes.append(p)
            if previous is not None:
                previous.close()
            previous = p.stdout
        stdout, _ = processes[-1].communicate(timeout=30)
        for p in processes[:-1]:
            p.wait(timeout=30)
        stderrs = []
        for f in errors:
            f.seek(0)
            stderrs.append(f.read().decode("utf-8", "replace"))
        return {"commands": probe["stages"], "stdin_file": probe["redir"],
                "statuses": [p.returncode for p in processes],
                "stdout": stdout.decode("utf-8", "replace"), "stderrs": stderrs}
    finally:
        for p in processes:
            if p.poll() is None:
                p.kill()
            p.wait()
            if p.stdout:
                p.stdout.close()
        for f in files + errors:
            f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instrument", required=True, type=Path)
    parser.add_argument("--mode", required=True, choices=["base", "candidate"])
    args = parser.parse_args()
    root = SEAT / "repo" / "review-fixture"
    root.mkdir(exist_ok=True)
    (root / "corpus/instruments").mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMPDIR=str(SEAT / "tmp"), HYAKU_SCRATCH=str(SEAT / "tmp"),
               PYTHONDONTWRITEBYTECODE="1", LC_ALL="C")
    big = b"alpha\n" * 1398102
    data = {
        "big.txt": big, "other.txt": b"bravo\n", "small.txt": b"alpha\nbravo\n",
        "other-small.txt": b"charlie\n", "big space.txt": big, "big|name.txt": big,
        "-n": big, "--": big,
        "corpus/instruments/fail7.py": b"raise SystemExit(7)\n",
        "corpus/instruments/term.py": b"import os, signal\nos.kill(os.getpid(), signal.SIGTERM)\n",
    }
    for name, content in data.items():
        (root / name).write_bytes(content)
    hashes = {name: {"sha256": sha(content), "bytes": len(content)} for name, content in data.items()}
    instrument = args.instrument.resolve()
    gate_hash = sha(instrument.read_bytes())
    revision = subprocess.run(["git", "-C", str(SEAT / "repo"), "rev-parse", "HEAD"],
                              cwd=SEAT, env=env, capture_output=True, text=True, timeout=15)
    if revision.returncode or revision.stdout.strip() != BASE:
        raise SystemExit("BASE identity guard failed: " + repr(revision))
    result_dir = DURABLE / args.mode
    result_dir.mkdir(exist_ok=True)
    rows = []
    for probe in cases():
        doc = {"figures": [{"id": probe["name"], "record": "own-generated-fixture",
                            "recorded": probe["want"], "derive": probe["derive"], "want": probe["want"]}]}
        ledger_bytes = (json.dumps(doc, indent=2) + "\n").encode()
        ledger = root / "ledger.json"
        ledger.write_bytes(ledger_bytes)
        command = [sys.executable, "-B", str(instrument), "--root", str(root), "--ledger", str(ledger)]
        p = subprocess.run(command, cwd=root, env=env, capture_output=True, timeout=45)
        stdout = p.stdout.decode("utf-8", "replace")
        stderr = p.stderr.decode("utf-8", "replace")
        found = re.search(r"reason=([^\s]+)", stdout + stderr)
        reason = found.group(1) if found else None
        expected_rc, expected_reason = probe["rc"], probe["reason"]
        if args.mode == "candidate" and (probe["change"] or probe["conservative"]):
            expected_rc, expected_reason = 1, "derive-upstream-signal-13"
        observed_native = native(probe, root, env)
        row = {"name": probe["name"], "mode": args.mode, "base": BASE,
               "gate_sha256": gate_hash, "driver_sha256": sha(Path(__file__).read_bytes()),
               "fixture_hashes": hashes, "ledger_sha256": sha(ledger_bytes),
               "command": command, "cwd": str(root), "environment": {k:env[k] for k in ("TMPDIR", "HYAKU_SCRATCH", "LC_ALL")},
               "derive": probe["derive"], "native": observed_native,
               "rc": p.returncode, "stdout": stdout, "stderr": stderr,
               "reason": reason, "expected_rc": expected_rc, "expected_reason": expected_reason,
               "pass": (p.returncode == expected_rc and reason == expected_reason),
               "note": probe["note"], "conservative_options": probe["conservative"]}
        if expected_rc == 0:
            row["pass"] = row["pass"] and " ok\n" in stdout
        (result_dir / (probe["name"] + ".json")).write_text(json.dumps(row, indent=2) + "\n")
        (result_dir / (probe["name"] + ".stdout")).write_bytes(p.stdout)
        (result_dir / (probe["name"] + ".stderr")).write_bytes(p.stderr)
        (result_dir / (probe["name"] + ".ledger.json")).write_bytes(ledger_bytes)
        rows.append(row)
        print(f"PROBE {probe['name']} rc={p.returncode} reason={reason or '-'} native={observed_native['statuses']} pass={int(row['pass'])}", flush=True)
    failures = sum(not row["pass"] for row in rows)
    summary = {"mode":args.mode, "base":BASE, "gate_sha256":gate_hash,
               "probes":len(rows), "failures":failures, "results":rows}
    (result_dir / "results.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"SUMMARY probes={len(rows)} failures={failures} mode={args.mode}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
