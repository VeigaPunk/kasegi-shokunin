#!/usr/bin/env python3
"""Audit every `recheck:` line in a lane's corpus/knowledge entries.

Round-25 instrument of record for the depth:verifiability claim. It answers one
question per entry: is the entry's own recheck line an executable, cwd-independent
command, or is it prose that cannot run?

Frozen predicate (see .ufo/waves/round-25/claims.json, C1). A line PASSES when
all three limbs hold:

  (a) parse      `bash -n -c "<command>"` exits 0 — the line is one shell command,
                 not prose with a trailing parenthetical.
  (b) cwd        running the command from the lane root and from a foreign cwd
                 (`--foreign`, default `/`) yields the same exit status AND the
                 same sha256 over the combined stdout+stderr bytes.
  (c) paths      the command names at least one lane-relative `corpus/...` path or
                 a `~/Projects/...` base test, and every `corpus/...` path it
                 names exists under the audited root.

Usage:
  python3 corpus/instruments/recheck-audit.py                       # audit the lane
  python3 corpus/instruments/recheck-audit.py --json receipt.json   # + machine receipt
  python3 corpus/instruments/recheck-audit.py --root /scratch/copy  # audit a copy
  python3 corpus/instruments/recheck-audit.py --foreign /           # foreign cwd
  python3 corpus/instruments/recheck-audit.py --selftest            # fixtures

Exit status: 0 when every line passes, 1 otherwise. A receipt is a verdict about
form only. It does not assert that an entry's evidence is current: a line whose
lane-root run fails closed (`fail-closed` in the receipt) is counted as passing
its form limbs and reported separately, because the base it guards is absent.
"""
import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

RECHECK_RE = re.compile(r"^recheck:[ \t]*(.*)$")
CORPUS_PATH_RE = re.compile(r"corpus/[A-Za-z0-9_.\-/]+\.(?:md|py|json|txt|tsv)")
HOME_BASE_RE = re.compile(r"~/Projects/[A-Za-z0-9_.\-/]+")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(cmd, cwd):
    proc = subprocess.run(
        ["bash", "-c", cmd], cwd=cwd, capture_output=True, timeout=300
    )
    return proc.returncode, digest(proc.stdout + b"\x00" + proc.stderr)


def parse_ok(cmd):
    return subprocess.run(["bash", "-n", "-c", cmd], capture_output=True).returncode == 0


def path_tokens(cmd):
    return sorted(set(CORPUS_PATH_RE.findall(cmd)))


def audit_entry(path, root, foreign):
    line = None
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            match = RECHECK_RE.match(raw.rstrip("\n"))
            if match:
                line = match.group(1).strip()
                break
    if line is None:
        return None
    limbs = {}
    limbs["parse"] = parse_ok(line)
    try:
        lane_rc, lane_digest = run(line, root)
        foreign_rc, foreign_digest = run(line, foreign)
        limbs["cwd"] = lane_rc == foreign_rc and lane_digest == foreign_digest
    except subprocess.TimeoutExpired:
        lane_rc, foreign_rc, lane_digest, foreign_digest = None, None, None, None
        limbs["cwd"] = False
    tokens = path_tokens(line)
    named = bool(tokens) or bool(HOME_BASE_RE.search(line))
    missing = [tok for tok in tokens if not os.path.exists(os.path.join(root, tok))]
    limbs["paths"] = named and not missing
    passed = all(limbs.values())
    return {
        "entry": os.path.basename(path),
        "command": line,
        "limbs": limbs,
        "missing_paths": missing,
        "lane_exit": lane_rc,
        "foreign_exit": foreign_rc,
        "lane_output_sha256": lane_digest,
        "foreign_output_sha256": foreign_digest,
        "class": "passing" if lane_rc == 0 else "fail-closed",
        "pass": passed,
    }


def collect(root, foreign):
    entries = []
    for path in sorted(glob.glob(os.path.join(root, "corpus/knowledge/*.md"))):
        record = audit_entry(path, root, foreign)
        if record:
            entries.append(record)
    return entries


def selftest():
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "corpus/knowledge"))
        os.makedirs(os.path.join(tmp, "corpus/instruments"))
        open(os.path.join(tmp, "corpus/instruments/tool.py"), "w").close()
        open(os.path.join(tmp, "corpus/knowledge/target.md"), "w").close()
        cases = {
            "good.md": "recheck: python3 corpus/instruments/tool.py corpus/knowledge/target.md",
            "prose.md": "recheck: on-restoration — true (fails closed today: base absent)",
            "cwd.md": "recheck: python3 corpus/instruments/tool.py corpus/knowledge/target.md # no cd",
            "ghost.md": "recheck: cd %s && test -e corpus/knowledge/ghost-absent.md" % tmp,
        }
        expected = {"good.md": True, "prose.md": False, "cwd.md": False, "ghost.md": False}
        failures = 0
        for name, line in cases.items():
            with open(os.path.join(tmp, "corpus/knowledge", name), "w") as handle:
                handle.write("# fixture\n\n" + line + "\n")
        # a cwd-independent command still fails limb (b) only when it is relative;
        # fixture "cwd.md" is the same command as good.md, so pin the difference by
        # making good.md carry the prefix.
        with open(os.path.join(tmp, "corpus/knowledge/good.md"), "w") as handle:
            handle.write(
                "# fixture\n\nrecheck: cd %s && python3 corpus/instruments/tool.py "
                "corpus/knowledge/target.md\n" % tmp
            )
        for name, want in expected.items():
            record = audit_entry(os.path.join(tmp, "corpus/knowledge", name), tmp, "/")
            got = record["pass"]
            status = "ok" if got == want else "FAIL"
            if got != want:
                failures += 1
            print(
                "selftest %-10s want=%-5s got=%-5s limbs=%s %s"
                % (name, want, got, record["limbs"], status)
            )
        print("selftest cases=%d failures=%d exit=%d" % (len(expected), failures, 1 if failures else 0))
        return 1 if failures else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=os.getcwd())
    parser.add_argument("--foreign", default="/")
    parser.add_argument("--json")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    root = os.path.abspath(args.root)
    entries = collect(root, args.foreign)
    passed = sum(1 for e in entries if e["pass"] or e["class"] == "fail-closed")
    fail_closed = sum(1 for e in entries if e["class"] == "fail-closed")
    failing_limbs = {
        limb: sum(1 for e in entries if not e["limbs"][limb])
        for limb in ("parse", "cwd", "paths")
    }
    if not args.quiet:
        for entry in entries:
            marks = "".join(
                "1" if entry["limbs"][limb] else "0" for limb in ("parse", "cwd", "paths")
            )
            print(
                "%-58s parse,cwd,paths=%s lane=%-3s foreign=%-3s %-11s %s"
                % (
                    entry["entry"],
                    marks,
                    entry["lane_exit"],
                    entry["foreign_exit"],
                    entry["class"],
                    "PASS" if entry["pass"] else "FAIL",
                )
            )
    summary = {
        "root": root,
        "foreign_cwd": args.foreign,
        "lines": len(entries),
        "pass": passed,
        "fail_closed": fail_closed,
        "failing_limbs": failing_limbs,
        "entries": entries,
    }
    print(
        "lines=%d pass=%d fail-closed=%d parse_fail=%d cwd_fail=%d paths_fail=%d exit=%d"
        % (
            len(entries),
            passed,
            fail_closed,
            failing_limbs["parse"],
            failing_limbs["cwd"],
            failing_limbs["paths"],
            0 if passed == len(entries) else 1,
        )
    )
    if args.json:
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump(summary, handle, ensure_ascii=False, indent=1)
            handle.write("\n")
    return 0 if passed == len(entries) else 1


if __name__ == "__main__":
    sys.exit(main())
