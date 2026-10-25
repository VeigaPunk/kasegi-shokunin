#!/usr/bin/env python3
"""Replay the frozen round-23 C1 mirror-containment matrix on real CLI bytes.

Usage: python3 corpus/instruments/mirror-containment-check.py
           [--resolver PATH] [--fixtures PATH] [--json PATH]

The selected `resolve.py` is copied, unmodified, next to a disposable fixture
tree and executed once per matrix case with an isolated HOME, KASEGI_MIRROR and
lane root. Each case pins one expected `class` for its citation in
`mirror-containment-fixtures.json`; the checker reads the CLI's own
`citation-survival.tsv` and compares. `--resolver` selects alternate bytes (for
example `git show <base>:corpus/instruments/resolve.py`) so the same matrix can
be replayed fail-before and pass-after; the resolver and matrix SHA-256 values
are printed and recorded in the receipt.

Escape cases pin GONE. Controls pin the class that must survive the change.
This instrument measures the detector's classification only: it does not
establish source availability, corpus attribution, or any score movement.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile


HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RESOLVER = os.path.join(HERE, "resolve.py")
DEFAULT_FIXTURES = os.path.join(HERE, "mirror-containment-fixtures.json")
TIMEOUT_S = 120


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def build_case(root, defaults, case):
    """Materialise one case under root; returns (home, mirror, lane)."""
    home = os.path.join(root, defaults["home"])
    mirror = os.path.join(root, defaults["mirror"])
    lane = os.path.join(root, defaults["lane"])
    dirs = list(defaults.get("dirs") or []) + list(case.get("dirs") or [])
    for rel in dirs:
        os.makedirs(os.path.join(root, rel), exist_ok=True)
    os.makedirs(lane, exist_ok=True)
    for rel, body in (defaults.get("files") or {}).items():
        write_file(root, rel, body)
    for rel, body in (case.get("files") or {}).items():
        write_file(root, rel, body)
    links = dict(defaults.get("symlinks") or {})
    links.update(case.get("symlinks") or {})
    for rel, target in links.items():
        link = os.path.join(root, rel)
        os.makedirs(os.path.dirname(link), exist_ok=True)
        if os.path.lexists(link):
            os.remove(link)
        os.symlink(target.replace("@ROOT@", root), link)
    with open(os.path.join(lane, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write("# C1 fixture\n\n- `%s`\n" % case["cite"])
    return home, mirror, lane


def write_file(root, rel, body):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)


def run_case(case, defaults, resolver_bytes, matrix_id):
    root = tempfile.mkdtemp(prefix="kasegi-r23-c1-")
    record = {
        "id": case["id"],
        "nature": case["nature"],
        "cite": case["cite"],
        "expect": case["expect"],
        "actual": "NO-ROW",
        "status": "FAIL",
        "problems": [],
        "matrix": matrix_id,
    }
    try:
        home, mirror, lane = build_case(root, defaults, case)
        tool = os.path.join(root, "tool")
        os.makedirs(tool, exist_ok=True)
        copied = os.path.join(tool, "resolve.py")
        with open(copied, "wb") as fh:
            fh.write(resolver_bytes)
        env = {
            "HOME": home,
            "KASEGI_MIRROR": mirror,
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        try:
            proc = subprocess.run(
                [sys.executable, copied, lane],
                cwd=tool, env=env, capture_output=True, text=True,
                timeout=TIMEOUT_S, check=False)
        except subprocess.TimeoutExpired:
            record["problems"].append("timeout")
            return record
        record["cli_exit"] = proc.returncode
        record["cli_stdout"] = (proc.stdout or "").strip()
        if proc.returncode != 0:
            record["problems"].append("cli-exit-%d" % proc.returncode)
            record["cli_stderr"] = (proc.stderr or "").strip()[:400]
            return record
        tsv = os.path.join(tool, "citation-survival.tsv")
        if not os.path.isfile(tsv):
            record["problems"].append("missing-tsv")
            return record
        classes = {}
        with open(tsv, "r", encoding="utf-8") as fh:
            header = fh.readline().rstrip("\n").split("\t")
            try:
                i_cite = header.index("citation")
                i_cls = header.index("class")
            except ValueError:
                record["problems"].append("tsv-schema")
                return record
            for line in fh:
                cols = line.rstrip("\n").split("\t")
                if len(cols) <= max(i_cite, i_cls):
                    record["problems"].append("tsv-short-row")
                    continue
                classes[cols[i_cite]] = cols[i_cls]
        record["rows"] = len(classes)
        record["actual"] = classes.get(case["cite"], "NO-ROW")
        if record["actual"] == case["expect"]:
            record["status"] = "PASS"
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--resolver", default=DEFAULT_RESOLVER)
    parser.add_argument("--fixtures", default=DEFAULT_FIXTURES)
    parser.add_argument("--json", default=None, help="write a JSON receipt here")
    args = parser.parse_args(argv)

    try:
        with open(args.fixtures, "rb") as fh:
            matrix = json.loads(fh.read().decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print("fixtures UNAVAILABLE reason=%s" % type(exc).__name__)
        return 2
    if matrix.get("schema") != 1 or not isinstance(matrix.get("cases"), list) or not matrix["cases"]:
        print("fixtures UNAVAILABLE reason=unsupported-schema")
        return 2
    try:
        with open(args.resolver, "rb") as fh:
            resolver_bytes = fh.read()
    except OSError as exc:
        print("resolver UNAVAILABLE reason=%s" % type(exc).__name__)
        return 2

    defaults = matrix["defaults"]
    resolver_sha = hashlib.sha256(resolver_bytes).hexdigest()
    matrix_sha = sha256_file(args.fixtures)

    records = []
    for case in matrix["cases"]:
        record = run_case(case, defaults, resolver_bytes, matrix_sha)
        records.append(record)
        extra = ""
        if record["problems"]:
            extra = " problems=" + ",".join(record["problems"])
        print("%-42s %-7s expect=%-16s actual=%-16s %s%s" % (
            record["id"], record["nature"], record["expect"], record["actual"],
            record["status"], extra))

    escapes = [r for r in records if r["nature"] == "escape"]
    controls = [r for r in records if r["nature"] == "control"]
    passed = [r for r in records if r["status"] == "PASS"]
    print("cases=%d escape=%d controls=%d pass=%d fail=%d resolver_sha256=%s matrix_sha256=%s" % (
        len(records), len(escapes), len(controls), len(passed),
        len(records) - len(passed), resolver_sha, matrix_sha))

    if args.json:
        receipt = {
            "schema": 1,
            "resolver": os.path.abspath(args.resolver),
            "resolver_sha256": resolver_sha,
            "matrix": os.path.abspath(args.fixtures),
            "matrix_sha256": matrix_sha,
            "cases": records,
            "totals": {
                "cases": len(records),
                "escape": len(escapes),
                "controls": len(controls),
                "pass": len(passed),
                "fail": len(records) - len(passed),
            },
        }
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=2, sort_keys=True)
            fh.write("\n")

    return 0 if len(passed) == len(records) else 1


if __name__ == "__main__":
    sys.exit(main())
