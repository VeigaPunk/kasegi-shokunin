#!/usr/bin/env python3
"""Replay the frozen round-24 C1 counter-B matrix on real CLI bytes.

Usage: python3 corpus/instruments/resolve-dispatch-check.py
           [--resolver PATH] [--fixtures PATH] [--json PATH]

The selected `resolve.py` is copied, unmodified, next to a disposable fixture
tree and executed once per matrix case with an isolated HOME, KASEGI_MIRROR and
lane root. Each case pins the expected `class` AND the expected `resolved_path`
for its citation in `resolve-dispatch-fixtures.json`; the checker reads the
CLI's own `citation-survival.tsv`. `--resolver` selects alternate bytes (for
example the frozen baseline copy at `.ufo/waves/round-24/c1-baseline-resolver.py`)
so the same matrix can be replayed fail-before and pass-after; the resolver,
matrix and checker SHA-256 values are printed and recorded in the receipt.

The matrix is frozen at eight cases: four liveness-positive cases that the
round-23 brace/glob dispatch cannot resolve (an empty brace alternative is
never built; a glob's first sorted match may be a dangling symlink) and four
controls whose classes any fix must preserve. A class alone is not enough: a
non-GONE class must name a path that exists on disk, sits inside the root that
class implies (case root, mirror or lane), and equals the exact expected file
where the case names one. A GONE class must carry no path at all. That makes
both degenerate resolvers fail — "GONE for everything" loses the liveness
cases and C1/C3/C4, "RESOLVES for everything" loses C2 — and a fix that swaps
one dangling path for another loses L3.

Fixture names are confined: an absolute name, a `..` segment, or a location
whose parent resolves outside the case root is rejected before any mkdir, open,
symlink or unlink. Symlink targets must stay inside the case root after `@ROOT@`
substitution.

This instrument measures the detector's brace/glob dispatch only: it does not
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
DEFAULT_FIXTURES = os.path.join(HERE, "resolve-dispatch-fixtures.json")
FROZEN_CASES = 8
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


def assertions(case):
    """Primary citation first, then any hardening citations."""
    out = [{"cite": case["cite"], "expect": case["expect"],
            "expect_file": case.get("expect_file")}]
    for extra in case.get("extra_cites") or []:
        out.append({"cite": extra["cite"], "expect": extra["expect"],
                    "expect_file": extra.get("expect_file")})
    return out


def build_case(root, defaults, case):
    """Materialise one case under root; returns (home, mirror, lane)."""
    home = safe_path(root, defaults["home"], "home")
    mirror = safe_path(root, defaults["mirror"], "mirror")
    lane = safe_path(root, defaults["lane"], "lane")
    dirs = list(defaults.get("dirs") or []) + list(case.get("dirs") or [])
    for rel in dirs:
        os.makedirs(safe_path(root, rel, "dir"), exist_ok=True)
    os.makedirs(lane, exist_ok=True)
    file_groups = (defaults.get("files") or {}, case.get("files") or {},
                   case.get("extra_files") or {})
    for group in file_groups:
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
    cites = []
    for item in assertions(case):
        if item["cite"] not in cites:
            cites.append(item["cite"])
    with open(os.path.join(lane, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write("# C1 dispatch fixture\n\n")
        for cite in cites:
            fh.write("- `%s`\n" % cite)
    return home, mirror, lane


def read_tsv(tsv):
    """Return {citation: (class, resolved_path, method, domain)}."""
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
    i_method = header.index("method") if "method" in header else None
    i_dom = header.index("domain") if "domain" in header else None
    for line in lines[1:]:
        cols = line.split("\t")
        if len(cols) <= max(i_cite, i_cls, i_path):
            continue
        method = cols[i_method] if i_method is not None and len(cols) > i_method else ""
        dom = cols[i_dom] if i_dom is not None and len(cols) > i_dom else ""
        rows[cols[i_cite]] = (cols[i_cls], cols[i_path], method, dom)
    return rows


def path_verdict(expect, resolved, expect_file, root, mirror, lane):
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
    if expect_file:
        want = os.path.realpath(safe_path(root, expect_file, "expect-file"))
        if real != want:
            return "path-not-%s" % expect_file.replace("/", "-")
    return ""


def check_assertion(item, rows, root, mirror, lane):
    """Return a per-citation record; status PASS only on class and path."""
    rec = {
        "cite": item["cite"],
        "expect": item["expect"],
        "expect_file": item["expect_file"] or "",
        "actual": "NO-ROW",
        "resolved_path": "",
        "method": "",
        "domain": "",
        "path_check": "",
        "status": "FAIL",
    }
    cls, resolved, method, dom = rows.get(item["cite"], ("NO-ROW", "", "", ""))
    rec["actual"] = cls
    rec["resolved_path"] = resolved.replace(root, "<CASE>")[:MAX_STDOUT_STORED]
    rec["method"] = method
    rec["domain"] = dom
    rec["path_check"] = path_verdict(item["expect"], resolved,
                                     item["expect_file"], root, mirror, lane)
    if cls == item["expect"] and rec["path_check"] == "":
        rec["status"] = "PASS"
    return rec


def run_case(case, defaults, resolver_bytes, matrix_id):
    root = tempfile.mkdtemp(prefix="kasegi-r24-c1-")
    record = {
        "id": case.get("id", "unnamed"),
        "nature": case.get("nature", "control"),
        "cite": case.get("cite", ""),
        "status": "FAIL",
        "problems": [],
        "assertions": [],
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
        for item in assertions(case):
            record["assertions"].append(
                check_assertion(item, rows, root, mirror, lane))
        record["status"] = ("PASS" if record["assertions"] and
                            all(a["status"] == "PASS" for a in record["assertions"])
                            else "FAIL")
    except Exception as exc:  # per-case containment: one bad case cannot abort the matrix
        record["problems"].append("case-error:%s:%s" % (type(exc).__name__, str(exc)[:120]))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return record


def load_matrix(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    matrix = json.loads(raw.decode("utf-8"))
    if matrix.get("schema") != 1 or not isinstance(matrix.get("cases"), list):
        raise ValueError("unsupported-schema")
    cases = matrix["cases"]
    if len(cases) != FROZEN_CASES:
        raise ValueError("case-count-%d" % len(cases))
    ids = [c.get("id") for c in cases]
    if len(set(ids)) != FROZEN_CASES or any(not i for i in ids):
        raise ValueError("case-ids-not-unique")
    liveness = [c for c in cases if c.get("nature") == "liveness"]
    controls = [c for c in cases if c.get("nature") == "control"]
    if len(liveness) != 4 or len(controls) != 4:
        raise ValueError("nature-split-%d-%d" % (len(liveness), len(controls)))
    for c in cases:
        if not c.get("cite") or c.get("expect") not in (
                "RESOLVES", "MIRROR-EQUIVALENT", "INTERNAL", "GONE"):
            raise ValueError("bad-case-%s" % c.get("id"))
    return raw, matrix


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--resolver", default=DEFAULT_RESOLVER)
    parser.add_argument("--fixtures", default=DEFAULT_FIXTURES)
    parser.add_argument("--json", default=None, help="write a JSON receipt here")
    args = parser.parse_args(argv)

    try:
        fixtures_bytes, matrix = load_matrix(args.fixtures)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print("fixtures UNAVAILABLE reason=%s" % str(exc).replace(" ", "-"))
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
        detail = record["assertions"][0] if record["assertions"] else {}
        extra = ""
        if record["problems"]:
            extra = " problems=" + ",".join(record["problems"])
        elif detail.get("path_check"):
            extra = " path_check=" + detail["path_check"]
        print("%-4s %-8s expect=%-16s actual=%-16s %s%s" % (
            record["id"], record["nature"], detail.get("expect", ""),
            detail.get("actual", ""), record["status"], extra))
        for a in record["assertions"][1:]:
            tail = ""
            if a["path_check"]:
                tail = " path_check=" + a["path_check"]
            print("     also expect=%-16s actual=%-16s %s%s" % (
                a["expect"], a["actual"], a["status"], tail))

    liveness = [r for r in records if r["nature"] == "liveness"]
    controls = [r for r in records if r["nature"] == "control"]
    passed = [r for r in records if r["status"] == "PASS"]
    exit_code = 0 if len(passed) == len(records) else 1
    print("cases=%d pass=%d exit=%d" % (len(records), len(passed), exit_code))
    print("sha256 resolver=%s matrix=%s checker=%s" % (
        resolver_sha, matrix_sha, checker_sha))

    if args.json:
        receipt = {
            "schema": 3,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "checker_sha256": checker_sha,
            "resolver": os.path.abspath(args.resolver),
            "resolver_sha256": resolver_sha,
            "matrix": os.path.abspath(args.fixtures),
            "matrix_sha256": matrix_sha,
            "cases": records,
            "totals": {
                "cases": len(records),
                "liveness": len(liveness),
                "controls": len(controls),
                "pass": len(passed),
                "fail": len(records) - len(passed),
                "exit": exit_code,
            },
            "command": "python3 corpus/instruments/resolve-dispatch-check.py --fixtures corpus/instruments/resolve-dispatch-fixtures.json",
        }
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=2, sort_keys=True)
            fh.write("\n")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
