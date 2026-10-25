#!/usr/bin/env python3
"""Replay the frozen round-23 C1 mirror-containment matrix on real CLI bytes.

Usage: python3 corpus/instruments/mirror-containment-check.py
           [--resolver PATH] [--fixtures PATH] [--json PATH]

The selected `resolve.py` is copied, unmodified, next to a disposable fixture
tree and executed once per matrix case with an isolated HOME, KASEGI_MIRROR and
lane root. Each case pins one expected `class` for its citation in
`mirror-containment-fixtures.json`; the checker reads the CLI's own
`citation-survival.tsv` and compares both the class and the `resolved_path`
column. `--resolver` selects alternate bytes (for example
`git show <base>:corpus/instruments/resolve.py`) so the same matrix can be
replayed fail-before and pass-after; the resolver, matrix and checker SHA-256
values are printed and recorded in the receipt.

Escape cases pin GONE. Controls pin the class that must survive the change; the
path assertion makes a control self-auditing — a non-GONE class must name an
existing path confined to the root that class implies (mirror, lane, or case
root), and a GONE class must carry no path at all.

Fixture names are confined: an absolute name, a `..` segment, or a location
whose parent resolves outside the case root is rejected before any mkdir, open,
symlink or unlink. Symlink targets must stay inside the case root after `@ROOT@`
substitution.

This instrument measures the detector's classification only: it does not
establish source availability, corpus attribution, or any score movement.
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile


HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RESOLVER = os.path.join(HERE, "resolve.py")
DEFAULT_FIXTURES = os.path.join(HERE, "mirror-containment-fixtures.json")
TIMEOUT_S = 120
MAX_STDOUT_STORED = 400
MAX_TSV_BYTES = 8 * 1024 * 1024


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    with open(path, "rb") as fh:
        return sha256_bytes(fh.read())


def safe_path(root, rel, where):
    """Return the absolute path for REL under ROOT, or raise ValueError.

    Rejects absolute names, `..` segments, empty segments and any location whose
    resolved parent sits outside the case root — before the caller touches disk.
    """
    if not isinstance(rel, str) or not rel or os.path.isabs(rel):
        raise ValueError("unsafe-%s:%r" % (where, rel))
    parts = rel.replace("\\", "/").split("/")
    if ".." in parts:
        raise ValueError("unsafe-%s:%r" % (where, rel))
    target = os.path.join(root, rel)
    parent = os.path.realpath(os.path.dirname(target))
    rootr = os.path.realpath(root)
    if parent != rootr and os.path.commonpath((rootr, parent)) != rootr:
        raise ValueError("escape-%s:%r" % (where, rel))
    return target


def check_link_target(root, target, where):
    if not isinstance(target, str) or not target:
        raise ValueError("unsafe-%s:%r" % (where, target))
    resolved = target.replace("@ROOT@", root)
    if not os.path.isabs(resolved):
        resolved = os.path.join(root, resolved)
    rootr = os.path.realpath(root)
    real = os.path.realpath(os.path.dirname(resolved))
    if real != rootr and os.path.commonpath((rootr, real)) != rootr:
        raise ValueError("escape-%s:%r" % (where, target))
    return target


def build_case(root, defaults, case):
    """Materialise one case under root; returns (home, mirror, lane)."""
    home = safe_path(root, defaults["home"], "home")
    mirror = safe_path(root, defaults["mirror"], "mirror")
    lane = safe_path(root, defaults["lane"], "lane")
    dirs = list(defaults.get("dirs") or []) + list(case.get("dirs") or [])
    for rel in dirs:
        os.makedirs(safe_path(root, rel, "dir"), exist_ok=True)
    os.makedirs(lane, exist_ok=True)
    for group in (defaults.get("files") or {}, case.get("files") or {}):
        for rel, body in group.items():
            path = safe_path(root, rel, "file")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(body)
    links = dict(defaults.get("symlinks") or {})
    links.update(case.get("symlinks") or {})
    for rel, target in links.items():
        link = safe_path(root, rel, "symlink")
        check_link_target(root, target, "symlink-target")
        os.makedirs(os.path.dirname(link), exist_ok=True)
        if os.path.lexists(link):
            os.remove(link)
        os.symlink(target.replace("@ROOT@", root), link)
    with open(os.path.join(lane, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write("# C1 fixture\n\n- `%s`\n" % case["cite"])
    return home, mirror, lane


def read_tsv(tsv):
    """Return {citation: (class, resolved_path)} from the CLI's TSV."""
    with open(tsv, "rb") as fh:
        raw = fh.read(MAX_TSV_BYTES)
    rows = {}
    lines = raw.decode("utf-8").splitlines()
    if not lines:
        raise ValueError("empty-tsv")
    header = lines[0].split("\t")
    i_cite = header.index("citation")
    i_cls = header.index("class")
    i_path = header.index("resolved_path")
    for line in lines[1:]:
        cols = line.split("\t")
        if len(cols) <= max(i_cite, i_cls, i_path):
            continue
        rows[cols[i_cite]] = (cols[i_cls], cols[i_path])
    return rows


def path_verdict(expect, resolved, root, mirror, lane):
    """Return "" when the path column corroborates the class, else a reason."""
    if expect == "GONE":
        return "" if resolved == "" else "gone-with-path"
    if not resolved:
        return "missing-path"
    real = os.path.realpath(os.path.expanduser(resolved))
    if not os.path.exists(real):
        return "path-missing-on-disk"
    bound = {"MIRROR-EQUIVALENT": mirror, "INTERNAL": lane}.get(expect, root)
    boundr = os.path.realpath(bound)
    if real != boundr and os.path.commonpath((boundr, real)) != boundr:
        return "path-outside-%s" % expect.lower()
    return ""


def run_case(case, defaults, resolver_bytes, matrix_id):
    root = tempfile.mkdtemp(prefix="kasegi-r23-c1-")
    record = {
        "id": case.get("id", "unnamed"),
        "nature": case.get("nature", "control"),
        "cite": case.get("cite", ""),
        "expect": case.get("expect", ""),
        "actual": "NO-ROW",
        "resolved_path": "",
        "path_check": "",
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
        proc = subprocess.Popen(
            [sys.executable, copied, lane],
            cwd=tool, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, start_new_session=True)
        try:
            stdout, stderr = proc.communicate(timeout=TIMEOUT_S)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.communicate()
            record["problems"].append("timeout")
            return record
        record["cli_exit"] = proc.returncode
        record["cli_stdout"] = (stdout or "").strip().replace(root, "<CASE>")[:MAX_STDOUT_STORED]
        if proc.returncode != 0:
            record["problems"].append("cli-exit-%d" % proc.returncode)
            record["cli_stderr"] = (stderr or "").strip().replace(root, "<CASE>")[:MAX_STDOUT_STORED]
            return record
        tsv = os.path.join(tool, "citation-survival.tsv")
        if not os.path.isfile(tsv):
            record["problems"].append("missing-tsv")
            return record
        rows = read_tsv(tsv)
        record["rows"] = len(rows)
        cls, resolved = rows.get(case["cite"], ("NO-ROW", ""))
        record["actual"] = cls
        record["resolved_path"] = resolved.replace(root, "<CASE>")[:MAX_STDOUT_STORED]
        record["path_check"] = path_verdict(case["expect"], resolved, root, mirror, lane)
        tolerated = False
        if record["path_check"] and case.get("path_tolerance") == "carve-out":
            # A declared carve-out is pinned WITH its escape visible: the path
            # verdict is kept in the receipt, never suppressed.
            record["path_check"] = "carve-out:" + record["path_check"]
            tolerated = True
        if cls == case["expect"] and (record["path_check"] == "" or tolerated):
            record["status"] = "PASS"
    except Exception as exc:  # per-case containment: one bad case cannot abort the matrix
        record["problems"].append("case-error:%s:%s" % (type(exc).__name__, str(exc)[:120]))
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
            fixtures_bytes = fh.read()
        matrix = json.loads(fixtures_bytes.decode("utf-8"))
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
    resolver_sha = sha256_bytes(resolver_bytes)
    matrix_sha = sha256_bytes(fixtures_bytes)
    checker_sha = sha256_file(os.path.abspath(__file__))

    records = []
    for case in matrix["cases"]:
        record = run_case(case, defaults, resolver_bytes, matrix_sha)
        records.append(record)
        extra = ""
        if record["problems"]:
            extra = " problems=" + ",".join(record["problems"])
        elif record["path_check"]:
            extra = " path_check=" + record["path_check"]
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
            "schema": 2,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "checker_sha256": checker_sha,
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
