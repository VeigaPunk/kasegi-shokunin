#!/usr/bin/env python3
"""Audit every `recheck:` line in a lane's corpus/knowledge entries.

Round-25 instrument of record for the depth:verifiability claim. It answers one
question per entry: is the entry's own recheck line an executable,
cwd-independent command that actually re-derives something for THAT entry?

Frozen predicate (the claim's counter; .ufo/waves/round-25/claims.json C1). A line
PASSES when all three limbs hold:

  (a) parse      `bash -n -c "<command>"` exits 0 — the line is one shell command,
                 not prose with a trailing parenthetical.
  (b) cwd        running the command from the lane root and from a foreign cwd
                 (`--foreign`, default `/`) yields the same exit status AND the
                 same sha256 over the combined stdout+stderr bytes.
  (c) paths      the command names at least one lane-relative `corpus/...` path or
                 a `~/Projects/...` base test, and every `corpus/...` path it
                 names exists under the audited root.

The frozen three limbs are reported unchanged. A mutation-tester showed they are
satisfiable by degenerate lines (`cd <lane> && true`, `cd <lane> && test -e
<the entry's own file>`, `--selftest`, a missing line), so four STRICT limbs are
reported beside them and never replace them — the claim's counter keeps the
meaning it had when it was frozen, and the strict set is what a do-nothing control
cannot reach:

  (d) cdroot     if the command begins `cd <path> &&`, <path> is the audited root.
  (e) instrument the command names an existing `corpus/instruments/<name>.py`, or
                 runs a `test -d/-e/-f ~/Projects/...` base test.
  (f) own        the command names the entry's own file, or pairs `--source` with
                 a `corpus/source-snapshots/` manifest, or is a bare base-state
                 assertion (`test -d/-e ~/Projects/...`) naming no corpus artifact.

An `artifact` limb (a corpus path other than the entry's own) was tried and dropped:
`instrument` already requires a `corpus/instruments/` script or a base test, so artifact
could never be shown to decide a verdict on its own — a limb that cannot fail alone is
not reported as if it could.

`pass` counts (a)-(c); `pass_strict` counts (a)-(f) plus a global completeness
check: the audit exits 0 only when the number of audited lines equals the number
of `corpus/knowledge/*.md` files, is non-zero, and every line passes. A deleted
recheck line therefore fails the audit instead of silently shrinking the set.

An expected list is committed alongside the knowledge files at
`corpus/instruments/knowledge-expected.txt`: one sorted, lane-relative
`corpus/knowledge/<entry>.md` filename per line, `#` comment lines allowed. When
the file exists (at `<root>/corpus/instruments/knowledge-expected.txt` by
default, or at `--expect PATH`), the audit additionally requires set equality
between the listed entries and the audited tree's actual
`corpus/knowledge/*.md` entries: an expected entry absent from the tree prints
`missing=<name>`, an extra tree entry prints `unexpected=<name>`, and either
makes the audit red. Drift between the committed list and the tree is therefore
a failed audit, so deleting a whole knowledge entry no longer shrinks the
audited set silently. When `--expect` is absent or its file is missing, the
audit keeps its glob-based completeness rule and the receipt records
`expect="absent"`.

Usage:
  python3 corpus/instruments/recheck-audit.py                       # audit the lane
  python3 corpus/instruments/recheck-audit.py --json receipt.json   # + machine receipt
  python3 corpus/instruments/recheck-audit.py --root /scratch/copy  # audit a copy
  python3 corpus/instruments/recheck-audit.py --foreign /           # foreign cwd
  python3 corpus/instruments/recheck-audit.py --expect /path/list   # explicit expected list
  python3 corpus/instruments/recheck-audit.py --selftest            # fixtures

Exit status: 0 when every line passes the frozen limbs AND the strict set AND the
completeness check AND the expected-list equality (when an expected list exists),
1 otherwise. A receipt is a verdict about form only. It does
not assert that an entry's evidence is current: a line whose lane-root run fails
closed (`fail-closed` in the receipt) counts as passing its form limbs and is
reported separately, because the base it guards is absent.
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
BASE_TEST_RE = re.compile(r"test[ \t]+-[def][ \t]+~/Projects/")
INSTRUMENT_RE = re.compile(r"corpus/instruments/[A-Za-z0-9_.\-]+\.py")
CD_RE = re.compile(r"^cd[ \t]+([^&;]+?)[ \t]*&&")
FROZEN_LIMBS = ("parse", "cwd", "paths")
STRICT_LIMBS = ("parse", "cwd", "paths", "cdroot", "instrument", "own")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(cmd, cwd):
    proc = subprocess.run(["bash", "-c", cmd], cwd=cwd, capture_output=True, timeout=300)
    return proc.returncode, digest(proc.stdout + b"\x00" + proc.stderr)


def parse_ok(cmd):
    return subprocess.run(["bash", "-n", "-c", cmd], capture_output=True).returncode == 0


def path_tokens(cmd):
    return sorted(set(CORPUS_PATH_RE.findall(cmd)))


def audit_entry(path, root, foreign, cdroot=None):
    line = None
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            match = RECHECK_RE.match(raw.rstrip("\n"))
            if match:
                line = match.group(1).strip()
                break
    if line is None:
        return None
    entry = os.path.basename(path)
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

    strict = dict(limbs)
    match = CD_RE.match(line)
    cd_target = match.group(1).strip().strip("'\"") if match else None
    strict["cdroot"] = True if cd_target is None else os.path.abspath(cd_target) == (cdroot or root)
    instruments = [tok for tok in INSTRUMENT_RE.findall(line) if os.path.exists(os.path.join(root, tok))]
    base_test = bool(BASE_TEST_RE.search(line))
    strict["instrument"] = bool(instruments) or base_test
    own = "corpus/knowledge/" + entry in tokens
    sourced = "--source" in line and "corpus/source-snapshots/" in line
    # a base-state assertion (a ~/Projects/ test naming no corpus artifact) is bound to
    # its entry by the base it guards; two historical lines (repo-git-state,
    # root-loss-2026-10-12) verify an external root and name no lane file.
    base_state = base_test and not tokens
    strict["own"] = own or sourced or base_state
    return {
        "entry": entry,
        "command": line,
        "limbs": limbs,
        "strict": strict,
        "missing_paths": missing,
        "cd_target": cd_target,
        "lane_exit": lane_rc,
        "foreign_exit": foreign_rc,
        "lane_output_sha256": lane_digest,
        "foreign_output_sha256": foreign_digest,
        "class": (
            "executes"
            if lane_rc == 0
            else ("gated" if limbs["parse"] else "broken")
        ),
        "pass": all(limbs.values()),
        "pass_strict": all(strict.values()),
    }


def collect(root, foreign, cdroot=None):
    entries = []
    for path in sorted(glob.glob(os.path.join(root, "corpus/knowledge/*.md"))):
        record = audit_entry(path, root, foreign, cdroot)
        if record:
            entries.append(record)
    return entries


def load_expected(path):
    names = []
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if line and not line.startswith("#"):
                names.append(line)
    return names


def expected_mismatch(root, expected):
    actual = {
        os.path.relpath(p, root)
        for p in glob.glob(os.path.join(root, "corpus/knowledge/*.md"))
    }
    wanted = set(expected)
    return sorted(wanted - actual), sorted(actual - wanted)


def selftest():
    import tempfile

    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "corpus/knowledge"))
        os.makedirs(os.path.join(tmp, "corpus/instruments"))
        os.makedirs(os.path.join(tmp, "corpus/source-snapshots/snap"))
        open(os.path.join(tmp, "corpus/instruments/tool.py"), "w").close()
        open(os.path.join(tmp, "corpus/knowledge/target.md"), "w").close()
        open(os.path.join(tmp, "corpus/source-snapshots/snap/manifest.json"), "w").close()
        tmp = os.path.abspath(tmp)
        cases = {
            # (line, frozen-limb pass, strict-limb pass)
            "good.md": ("recheck: cd %s && python3 corpus/instruments/tool.py corpus/knowledge/good.md" % tmp, True, True),
            "prose.md": ("recheck: on-restoration — true (fails closed today: base absent)", False, False),
            "cwd.md": ("recheck: python3 corpus/instruments/tool.py corpus/knowledge/cwd.md", False, False),
            "ghost.md": ("recheck: cd %s && test -e corpus/knowledge/ghost-absent.md" % tmp, False, False),
            "degenerate.md": ("recheck: cd %s && true corpus/knowledge/target.md" % tmp, True, False),
            "elsewhere.md": ("recheck: cd /tmp && python3 corpus/instruments/tool.py corpus/knowledge/elsewhere.md", True, False),
            "ownonly.md": ("recheck: cd %s && test -e corpus/knowledge/ownonly.md" % tmp, True, False),
            "selftesty.md": ("recheck: cd %s && python3 corpus/instruments/tool.py --selftest" % tmp, True, False),
            "sourced.md": (
                "recheck: cd %s && python3 corpus/instruments/tool.py --manifest corpus/source-snapshots/snap/manifest.json --source S001" % tmp,
                True,
                True,
            ),
            "basetest.md": ("recheck: cd %s && test -d ~/Projects/bounties && python3 corpus/instruments/tool.py corpus/knowledge/target.md" % tmp, True, False),
            "basestate.md": ("recheck: cd %s && test -d ~/Projects/bounties" % tmp, True, True),
            "parseonly.md": ("recheck: cd %s && test -d ~/Projects/bounties (fails closed today)" % tmp, False, False),
            "instonly.md": ("recheck: cd %s && ls corpus/knowledge/instonly.md corpus/knowledge/target.md" % tmp, True, False),
        }
        for name, (line, _, _) in cases.items():
            with open(os.path.join(tmp, "corpus/knowledge", name), "w") as handle:
                handle.write("# fixture\n\n" + line + "\n")
        for name, (line, want_pass, want_strict) in cases.items():
            with open(os.path.join(tmp, "corpus/knowledge", name), "w") as handle:
                handle.write("# fixture\n\n" + line + "\n")
        for name, (_, want_pass, want_strict) in cases.items():
            record = audit_entry(os.path.join(tmp, "corpus/knowledge", name), tmp, "/")
            ok = record["pass"] == want_pass and record["pass_strict"] == want_strict
            if not ok:
                failures += 1
            print(
                "selftest %-13s pass want=%-5s got=%-5s | strict want=%-5s got=%-5s %s"
                % (name, want_pass, record["pass"], want_strict, record["pass_strict"], "ok" if ok else "FAIL")
            )
        # completeness: one file without a recheck line must break the audit's exit rule
        open(os.path.join(tmp, "corpus/knowledge/missing-line.md"), "w").write("# no recheck\n")
        entries = collect(tmp, "/")
        total = len(glob.glob(os.path.join(tmp, "corpus/knowledge/*.md")))
        complete = len(entries) == total and total > 0 and all(e["pass_strict"] for e in entries)
        print(
            "selftest completeness lines=%d total=%d complete=%s %s"
            % (len(entries), total, complete, "ok" if complete is False else "FAIL")
        )
        if complete is not False:
            failures += 1
        # expected-list fixtures: the committed list vs the audited tree must match,
        # so deleting a whole entry (missing) or adding an extra one (unexpected)
        # must red the audit and name the file in the receipt.
        for label, expected, extra in (
            ("expect-missing", ["corpus/knowledge/good.md", "corpus/knowledge/ghost-absent.md"], ()),
            ("expect-unexpected", ["corpus/knowledge/good.md"], ("extra.md",)),
        ):
            tree = os.path.join(tmp, label)
            os.makedirs(os.path.join(tree, "corpus/knowledge"))
            os.makedirs(os.path.join(tree, "corpus/instruments"))
            open(os.path.join(tree, "corpus/instruments/tool.py"), "w").close()
            line = "recheck: cd %s && python3 corpus/instruments/tool.py corpus/knowledge/good.md" % tree
            with open(os.path.join(tree, "corpus/knowledge/good.md"), "w") as handle:
                handle.write("# fixture\n\n" + line + "\n")
            for name in extra:
                with open(os.path.join(tree, "corpus/knowledge", name), "w") as handle:
                    handle.write("# fixture\n\n" + line.replace("good.md", name) + "\n")
            with open(os.path.join(tree, "corpus/instruments/knowledge-expected.txt"), "w") as handle:
                handle.write("# expected knowledge entries for %s\n" % label)
                for name in expected:
                    handle.write(name + "\n")
            receipt_path = os.path.join(tree, "receipt.json")
            rc = main(["--root", tree, "--cdroot", tree, "--json", receipt_path])
            with open(receipt_path, encoding="utf-8") as handle:
                receipt = json.load(handle)
            if label == "expect-missing":
                ok = (
                    rc == 1
                    and receipt["missing_entries"] == ["corpus/knowledge/ghost-absent.md"]
                    and receipt["unexpected_entries"] == []
                    and receipt["expect"] == "present"
                )
            else:
                ok = (
                    rc == 1
                    and receipt["unexpected_entries"] == ["corpus/knowledge/extra.md"]
                    and receipt["missing_entries"] == []
                    and receipt["expect"] == "present"
                )
            if not ok:
                failures += 1
            print(
                "selftest %-15s exit=%d want=1 missing=%s unexpected=%s %s"
                % (label, rc, receipt["missing_entries"], receipt["unexpected_entries"], "ok" if ok else "FAIL")
            )
        # 13 per-entry fixtures + 2 tree-level expected-list fixtures (completeness
        # is an auxiliary sanity line above, not counted as a case)
        total_cases = len(cases) + 2
        return 1 if failures else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=os.getcwd())
    parser.add_argument("--foreign", default="/")
    parser.add_argument(
        "--cdroot",
        help="the lane root the recheck lines are expected to cd into; defaults to --root "
        "(set it when --root is a scratch copy of the corpus)",
    )
    parser.add_argument(
        "--expect",
        help="path to the expected knowledge-entry list; defaults to "
        "<root>/corpus/instruments/knowledge-expected.txt when that file exists "
        "(absent or missing file: the audit keeps its glob-based completeness rule)",
    )
    parser.add_argument("--json")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    root = os.path.abspath(args.root)
    cdroot = os.path.abspath(args.cdroot) if args.cdroot else None
    entries = collect(root, args.foreign, cdroot)
    total = len(glob.glob(os.path.join(root, "corpus/knowledge/*.md")))
    expect_path = args.expect
    if expect_path is None:
        default_expect = os.path.join(root, "corpus/instruments/knowledge-expected.txt")
        expect_path = default_expect if os.path.exists(default_expect) else None
    elif not os.path.exists(expect_path):
        expect_path = None
    if expect_path is None:
        expected_entries, missing_entries, unexpected_entries = [], [], []
    else:
        expected_entries = load_expected(expect_path)
        missing_entries, unexpected_entries = expected_mismatch(root, expected_entries)
    expect_active = expect_path is not None
    passed = sum(1 for e in entries if e["pass"])
    strict_passed = sum(1 for e in entries if e["pass_strict"])
    fail_closed = sum(1 for e in entries if e["lane_exit"] != 0)
    gated = sum(1 for e in entries if e["class"] == "gated")
    broken = sum(1 for e in entries if e["class"] == "broken")
    failing = {limb: sum(1 for e in entries if not e["limbs"][limb]) for limb in FROZEN_LIMBS}
    strict_failing = {limb: sum(1 for e in entries if not e["strict"][limb]) for limb in STRICT_LIMBS}
    complete = len(entries) == total and total > 0
    expect_ok = not expect_active or (not missing_entries and not unexpected_entries)
    ok = passed == len(entries) and complete and strict_passed == total and expect_ok
    if not args.quiet:
        for entry in entries:
            frozen = "".join("1" if entry["limbs"][limb] else "0" for limb in FROZEN_LIMBS)
            strict = "".join("1" if entry["strict"][limb] else "0" for limb in STRICT_LIMBS)
            print(
                "%-58s frozen=%s strict=%s lane=%-3s foreign=%-3s %-11s %s"
                % (
                    entry["entry"],
                    frozen,
                    strict,
                    entry["lane_exit"],
                    entry["foreign_exit"],
                    entry["class"],
                    "PASS" if entry["pass_strict"] else ("FROZEN-ONLY" if entry["pass"] else "FAIL"),
                )
            )
    if not args.quiet and expect_active:
        for name in missing_entries:
            print("missing=%s" % name)
        for name in unexpected_entries:
            print("unexpected=%s" % name)
    with open(os.path.abspath(__file__), "rb") as handle:
        instrument_sha256 = hashlib.sha256(handle.read()).hexdigest()
    summary = {
        "instrument_sha256": instrument_sha256,
        "root": root,
        "cdroot": cdroot or root,
        "foreign_cwd": args.foreign,
        "lines": len(entries),
        "total_knowledge_files": total,
        "complete": complete,
        "pass": passed,
        "pass_strict": strict_passed,
        "fail_closed": fail_closed,
        "executes_today": len(entries) - fail_closed,
        "gated": gated,
        "broken": broken,
        "failing_limbs": failing,
        "strict_failing_limbs": strict_failing,
        "expect": "present" if expect_active else "absent",
        "expected_entries": expected_entries,
        "missing_entries": missing_entries,
        "unexpected_entries": unexpected_entries,
        "entries": entries,
    }
    print(
        "strict pass=%d/%d cdroot_fail=%d instrument_fail=%d own_fail=%d"
        % (
            strict_passed,
            total,
            strict_failing["cdroot"],
            strict_failing["instrument"],
            strict_failing["own"],
        )
    )
    print(
        "executes=%d gated=%d broken=%d  (gated = the line runs and fails closed on an "
        "absent base; broken = it cannot run at all)"
        % (len(entries) - fail_closed, gated, broken)
    )
    print(
        "lines=%d total=%d pass=%d fail-closed=%d parse_fail=%d cwd_fail=%d paths_fail=%d exit=%d"
        % (
            len(entries),
            total,
            passed,
            fail_closed,
            failing["parse"],
            failing["cwd"],
            failing["paths"],
            0 if ok else 1,
        )
    )
    print(
        "expect=%s expected=%d missing=%d unexpected=%d exit=%d"
        % (
            "present" if expect_active else "absent",
            len(expected_entries),
            len(missing_entries),
            len(unexpected_entries),
            0 if ok else 1,
        )
    )
    if args.json:
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump(summary, handle, ensure_ascii=False, indent=1)
            handle.write("\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
