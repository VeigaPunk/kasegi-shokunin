#!/usr/bin/env python3
"""shonen-shipped-fixture-check.py — the round-49 non-frozen fixture runner (M48-4, M48-6).

Usage: python3 corpus/instruments/shonen-shipped-fixture-check.py --root TREE [--selftest] [--work SCRATCH]

What it does.  The round-48 frozen fixture file carries the pre-freeze draft as its only
`canonical` fixture, not the bytes the lane shipped (M48-4, routed by the round-48 non-author
closure).  The round-48 frozen fixture file is NOT amended here.  This runner reads the separate,
non-frozen fixture file `corpus/instruments/shonen-shipped-fixtures.json`, whose positive control is
the shipped bytes (pinned by sha256), and checks each case against the checker
`corpus/instruments/shonen-form.py`:

  - the shipped bytes must read SF-CLEAN / exit 0 (positive control);
  - the unchecked-box-with-evidence shape must read SF-CLEAN / exit 0 (characterisation: the
    checker grades form and marks, never the substance of an assessment);
  - the unchecked-box-without-evidence shape must read SF-CLEAN / exit 0 (the pristine seed the
    round-48 limits named);
  - the removed box must read SF-BOX / exit 1 (a mutant that must stay killed);
  - a NUL byte inside an evidence pointer must read SF-UNREADABLE / exit 2 (the routed defect
    M48-6: unreadable input returns the instrument's mapped exit, never an uncaught ValueError).

Exit 0 when every case matches, 1 when a case fails, 2 when the input (the shipped bytes, the
fixture file or the checker) cannot be read.  The runner writes nothing outside its scratch tree.
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
DEFAULT_ROOT = os.path.dirname(HERE)
FIXTURE_FILE = os.path.join(HERE, "shonen-shipped-fixtures.json")
CHECKER = os.path.join(HERE, "shonen-form.py")
LABELS = (
    "SKILL.md contains real decision tables, error patterns, checklists, cited sources",
    "At least one end-to-end domain task executed and logged in LOG.md",
    "Instructions executable by an agent without oral context",
    "No cross-domain bleed (PROVINCE.md still accurate)",
)


def shipped_bytes(root):
    """The SHONEN.md bytes the lane ships, verified against the fixture's pinned digest."""
    path = os.path.join(root, "SHONEN.md")
    with open(path, "rb") as fh:
        raw = fh.read()
    return raw


def build_shipped(raw):
    """Rebuild the shipped checklist text (labels are fixed by the checker)."""
    return raw.decode("utf-8")


def transform(text, kind):
    """Return the mutated checklist text for one fixture kind."""
    lines = text.split("\n")
    if kind == "unchecked-with-evidence":
        out = []
        for line in lines:
            if line.startswith("- [") and line.endswith(tuple(LABELS)):
                out.append("- [ ] " + line[6:])
            else:
                out.append(line)
        return "\n".join(out)
    if kind == "unchecked-without-evidence":
        out = []
        for line in lines:
            if line.startswith("- [") and line.endswith(tuple(LABELS)):
                out.append("- [ ] " + line[6:])
            elif line.startswith("      Evidence: "):
                continue
            else:
                out.append(line)
        return "\n".join(out)
    if kind == "remove-first-box":
        for i, line in enumerate(lines):
            if line.startswith("- ["):
                del lines[i]
                break
        return "\n".join(lines)
    if kind == "nul-in-pointer":
        out = []
        for line in lines:
            if line.startswith("      Evidence: "):
                out.append(line.replace("Evidence: ", "Evidence: a\0b", 1))
            else:
                out.append(line)
        return "\n".join(out)
    raise ValueError("unknown transform: %s" % kind)


def run_checker(checker, tree, target):
    proc = subprocess.run([sys.executable, checker, "--root", tree, "--file", target],
                          capture_output=True, text=True)
    finding = ""
    for line in proc.stdout.splitlines():
        if " finding=" in line:
            finding = line.split(" finding=", 1)[1].split(" ")[0]
    return proc.returncode, finding, (proc.stdout + proc.stderr).strip()


def build_tree(work, root):
    """A scratch tree with the files the checker needs (SHONEN.md plus its pointer targets)."""
    tree = os.path.join(work, "tree")
    os.makedirs(tree, exist_ok=True)
    for name in ("SKILL.md", "PROVINCE.md", "LOG.md"):
        src = os.path.join(root, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(tree, name))
    return tree


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work", default=None)
    ap.add_argument("--fixtures", default=FIXTURE_FILE)
    args = ap.parse_args(argv[1:])
    root = os.path.abspath(os.path.expanduser(args.root))
    if not os.path.isdir(root):
        sys.stderr.write("shonen-shipped-fixture-check.py: not a directory: %s\n" % args.root)
        return 2
    if not os.path.exists(args.fixtures):
        sys.stderr.write("shonen-shipped-fixture-check.py: missing fixture file: %s\n" % args.fixtures)
        return 2
    with open(args.fixtures, "r", encoding="utf-8") as fh:
        spec = json.load(fh)
    try:
        raw = shipped_bytes(root)
    except OSError as exc:
        sys.stderr.write("shonen-shipped-fixture-check.py: unreadable SHONEN.md: %s\n" % exc)
        return 2
    digest = hashlib.sha256(raw).hexdigest()
    pinned = spec.get("shipped_positive_control", {}).get("sha256")
    work = args.work or tempfile.mkdtemp(prefix="shonen-shipped-fixture-")
    created = args.work is None
    os.makedirs(work, exist_ok=True)
    failures = []
    cases = 0

    def check(case_id, text, expect_finding, expect_exit, kind):
        nonlocal cases
        cases += 1
        # The graded file lives in the scratch tree; the checker resolves the evidence
        # pointers against the LANE root, which is where those pointers point.
        target = os.path.join(work, "case-%s.md" % case_id)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(text)
        code, finding, output = run_checker(CHECKER, root, target)
        ok = (finding == expect_finding and code == expect_exit)
        print("selftest case=%s verdict=%s kind=%s finding=%s exit=%d expected=%s/%d"
              % (case_id, "pass" if ok else "fail", kind, finding or "-", code, expect_finding, expect_exit))
        if not ok:
            failures.append(case_id)
            print("selftest case=%s output=%s" % (case_id, output.replace("\n", " | ")))

    control = spec.get("shipped_positive_control", {})
    if pinned and digest != pinned:
        cases += 1
        failures.append("shipped-bytes-digest")
        print("selftest case=shipped-bytes-digest verdict=fail kind=control digest=%s expected=%s"
              % (digest, pinned))
    else:
        check("shipped-bytes", build_shipped(raw), control.get("expect_finding", "SF-CLEAN"),
              control.get("expect_exit", 0), "control")

    base_text = build_shipped(raw)
    for fx in spec.get("fixtures", []):
        try:
            text = transform(base_text, fx["transform"])
        except Exception as exc:  # a transform that cannot run is a failed case
            cases += 1
            failures.append(fx["id"])
            print("selftest case=%s verdict=fail kind=transform error=%s" % (fx["id"], exc))
            continue
        check(fx["id"], text, fx["expect_finding"], fx["expect_exit"], fx.get("verdict_kind", "mutant"))

    print("selftest cases=%d failures=%d" % (cases, len(failures)))
    if created:
        shutil.rmtree(work, ignore_errors=True)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
