#!/usr/bin/env python3
"""--selftest implementation for corpus/instruments/claim-package-check.py.

Ten graded cases, one line each, then a summary line:

    selftest case=1 class=defect fixture=<dir> expected=<rule> observed=<rule> verdict=pass|fail
    ...
    selftest case=10 class=degenerate fixture=always-pass expected=reject observed=rejected-9/9 verdict=pass
    selftest cases=10 failures=<k>

Exit 0 only when failures=0.  A defect case passes only when the gate exits 1,
prints `verdict=DEFECT`, prints exactly the eight RULE lines, and the ONLY
failing rule is that fixture's own expected rule.  A fixture that fails for a
different rule (or an extra one) is a selftest failure, not a pass.

Case 10 is the degenerate control: a stand-in gate that unconditionally prints
`verdict=WELL-FORMED` and exits 0.  The same nine gradings are replayed against
it; the control passes only if that gate is rejected on all nine.

Isolation: every case gets its own directory under TMPDIR and its own copy of
the fixture; the gate subprocess runs with cwd inside that directory with a
sitecustomize audit hook that appends every path it opens, tagged read or write.
A case fails when its gate reads anything under the work root outside its own
directory or anything at all under the canonical fixtures root
(detail=sibling-read / source-fixture-read), and when it WRITES anywhere outside
its own directory, including a pinned /tmp path (detail=external-write /
sibling-write / source-fixture-write).

Fixture expectation resolution, in order: a one-line `expected-rule` file in
the fixture directory, then `<fixtures root>/index.txt` lines
`<fixture-name> <RULE>`, then the defect class token in the directory name
(missing-file/digest/negative/escape/redaction/custodian/reviewer/marker/secret).
A declared rule that contradicts the class token fails the case
(expected-mismatch): the name is an independent witness and cannot be
overridden by a fixture-side declaration.

Integration: paste this file's body byte-exactly above the gate's
`# <!-- selftest-body-paste-anchor: ... -->` line.  The gate's
`selftest_dispatch()` resolves `globals()['run_selftest']` and calls
`run_selftest(os.path.abspath(__file__))`; the gate then finds the fixtures at
`<gate dir>/fixtures/claim-package`.  Nothing else is required.

Splice safety: every module-level name here is `_selftest_*` / `_SELFTEST_*`
prefixed except the single seam `run_selftest`, so pasting over a gate that
defines its own `RULES`, `main` or `_emit` cannot shadow them (measured: an
unprefixed `RULES` tuple broke every rule with `error:TypeError`).  There are
no module-level side effects; the standalone guard at the bottom is inert when
spliced because the gate's `main` is already in `globals()`.

Stdlib only.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Rule ids in the gate's fixed print order.
_SELFTEST_RULES = (
    "R-FILES",
    "R-MANIFEST",
    "R-REDACT",
    "R-CUSTODIAN",
    "R-PROVENANCE",
    "R-STATUS",
    "R-REPORT",
    "R-NOSECRET",
)

# Defect classes in case order: (name aliases, expected rule).  Matched against
# the hyphen-normalised fixture directory name; the first alias that occurs
# wins, so more specific tokens are listed first.
_SELFTEST_CLASSES = (
    (("missing-sixth", "missing-file", "missing"), "R-FILES"),
    (("digest",), "R-MANIFEST"),
    (("negative-only", "negative", "polarity"), "R-MANIFEST"),
    (("escape", "traversal", "outside"), "R-MANIFEST"),
    (("redact",), "R-REDACT"),
    (("custodian", "head-mismatch", "head"), "R-CUSTODIAN"),
    (("reviewer", "producer"), "R-STATUS"),
    (("marker", "no-submission"), "R-REPORT"),
    (("secret", "token"), "R-NOSECRET"),
)

_SELFTEST_SUMMARY_RE = re.compile(r"verdict=(WELL-FORMED|DEFECT)\b")
_SELFTEST_RULE_RE = re.compile(r"^RULE\s+(\S+)\s+verdict=(pass|fail)\b")

# Audit hook installed in the gate subprocess through PYTHONPATH/sitecustomize.
# It appends every open/scandir/listdir target to $CLAIM_PKG_SELFTEST_AUDIT_LOG
# as it happens, so the log survives even if the child dies mid-run.
_SELFTEST_AUDIT = r'''import os
import sys

_log = os.environ.get("CLAIM_PKG_SELFTEST_AUDIT_LOG")
if _log:
    _busy = [False]

    def _is_write(mode, flags):
        if isinstance(mode, str):
            return any(ch in mode for ch in "wax+")
        if isinstance(flags, int):
            mask = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC
            return bool(flags & mask)
        return False

    def _record(target, is_write):
        try:
            path = os.fsdecode(target)
        except Exception:
            return
        if not path:
            return
        _busy[0] = True
        try:
            fd = os.open(_log, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
            try:
                line = ("W " if is_write else "R ") + path.replace("\n", "\\n") + "\n"
                os.write(fd, line.encode("utf-8", "replace"))
            finally:
                os.close(fd)
        except OSError:
            pass
        finally:
            _busy[0] = False

    def _hook(event, args):
        if _busy[0]:
            return
        if not args:
            return
        target = args[0]
        if not isinstance(target, (str, bytes, os.PathLike)):
            return
        if event == "open":
            mode = args[1] if len(args) > 1 else None
            flags = args[2] if len(args) > 2 else None
            _record(target, _is_write(mode, flags))
        elif event in ("os.scandir", "os.listdir"):
            _record(target, False)

    sys.addaudithook(_hook)
'''

_SELFTEST_DEGENERATE = '''#!/usr/bin/env python3
"""Degenerate always-pass stand-in: prints WELL-FORMED and exits 0."""
import sys

for rule in (
    "R-FILES",
    "R-MANIFEST",
    "R-REDACT",
    "R-CUSTODIAN",
    "R-PROVENANCE",
    "R-STATUS",
    "R-REPORT",
    "R-NOSECRET",
):
    print("RULE %s verdict=pass detail=stub" % rule)
print("package=%s rules=8 pass=8 fail=0 verdict=WELL-FORMED" % sys.argv[1])
sys.exit(0)
'''


def _selftest_norm(name):
    return name.strip().lower().replace("_", "-")


def _selftest_class_rule(name):
    """Rule implied by the defect class token in the fixture directory name."""
    norm = _selftest_norm(name)
    for aliases, rule in _SELFTEST_CLASSES:
        for alias in aliases:
            if alias in norm:
                return rule
    return None


def _selftest_declared_rule(fixture_dir, index_map):
    note = fixture_dir / "expected-rule"
    if note.is_file():
        try:
            text = note.read_text(encoding="utf-8").strip()
        except OSError:
            return None, "expected-rule-unreadable"
        if text:
            return text.split()[0], None
    return index_map.get(_selftest_norm(fixture_dir.name)), None


def _selftest_expected_rule(fixture_dir, index_map):
    """Resolve the expected failing rule, cross-checking the class token."""
    declared, err = _selftest_declared_rule(fixture_dir, index_map)
    if err:
        return None, err
    if declared is not None and declared not in _SELFTEST_RULES:
        return None, "expected-rule-unknown"
    derived = _selftest_class_rule(fixture_dir.name)
    if declared is not None and derived is not None and declared != derived:
        return None, "expected-mismatch"
    rule = declared if declared is not None else derived
    if rule is None:
        return None, "expected-unclassified"
    return rule, None


def _selftest_read_index(fixtures_root):
    """`<fixture-name> <RULE>` lines from an optional index file."""
    out = {}
    for name in ("index.txt", "INDEX.txt", "ExecGateFixtures.index.txt"):
        path = fixtures_root / name
        if not path.is_file():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            for token in parts[1:]:
                if token in _SELFTEST_RULES:
                    out[_selftest_norm(parts[0].rstrip("/"))] = token
                    break
    return out


def _selftest_tree_digest(root):
    """(relative path, size, mtime_ns) for every file under root."""
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            path = Path(dirpath) / name
            try:
                st = path.lstat()
            except OSError:
                continue
            rows.append((str(path.relative_to(root)), st.st_size, st.st_mtime_ns))
    return rows


def _selftest_parse_output(out):
    rule_lines = []
    fails = []
    for line in out.splitlines():
        m = _SELFTEST_RULE_RE.match(line)
        if not m:
            continue
        rule_lines.append(m.group(1))
        if m.group(2) == "fail":
            fails.append(m.group(1))
    verdicts = _SELFTEST_SUMMARY_RE.findall(out)
    verdict = verdicts[-1] if verdicts else "none"
    return rule_lines, fails, verdict


def _selftest_inside(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _selftest_isolation(work_root, case_dir, log_path, fixtures_root, allowed):
    """(ok, detail) - the case touched nothing outside its own directory."""
    if not log_path.is_file():
        return False, "isolation-unverified"
    work_root = work_root.resolve()
    case_dir = case_dir.resolve()
    fixtures_root = fixtures_root.resolve()
    try:
        raw_lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return False, "isolation-unreadable"
    for raw in raw_lines:
        if not raw:
            continue
        kind, _, body = raw.partition(" ")
        if kind not in ("R", "W") or not body:
            kind, body = "R", raw
        candidate = Path(body.replace("\\n", "\n"))
        if not candidate.is_absolute():
            candidate = case_dir / candidate
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if _selftest_inside(resolved, case_dir) or any(_selftest_inside(resolved, a) for a in allowed):
            continue
        if kind == "W":
            if _selftest_inside(resolved, fixtures_root):
                return False, "source-fixture-write"
            if _selftest_inside(resolved, work_root):
                return False, "sibling-write"
            return False, "external-write"
        if _selftest_inside(resolved, fixtures_root):
            return False, "source-fixture-read"
        if _selftest_inside(resolved, work_root):
            return False, "sibling-read"
    return True, "isolated"


def _selftest_reason(rc, verdict, rule_lines, fails, expected, iso_ok, iso_detail):
    if not iso_ok:
        return iso_detail
    if len(rule_lines) != len(_SELFTEST_RULES) or sorted(rule_lines) != sorted(_SELFTEST_RULES):
        return "rules-printed=%d" % len(rule_lines)
    if verdict != "DEFECT":
        return "verdict=%s" % verdict
    if fails != [expected]:
        return "wrong-rule"
    if rc != 1:
        return "exit=%s" % rc
    return "unclassified"


def _selftest_grade(gate_path, fixture_dir, case_root, audit_dir, expected, fixtures_root, work_root):
    """Run the gate once on a private copy of fixture_dir and grade it."""
    case_root.mkdir(parents=True, exist_ok=True)
    pkg = case_root / "pkg"
    if pkg.exists():
        shutil.rmtree(pkg)
    shutil.copytree(fixture_dir, pkg, symlinks=True)
    note = pkg / "expected-rule"
    if note.exists():
        note.unlink()  # the graded payload is the fixture's six files, nothing else
    log_path = case_root / "reads.log"
    env = dict(os.environ)
    env["PYTHONPATH"] = str(audit_dir)
    env["CLAIM_PKG_SELFTEST_AUDIT_LOG"] = str(log_path)
    env.pop("PYTHONSTARTUP", None)
    python = sys.executable or "python3"
    try:
        proc = subprocess.run(
            [python, str(gate_path), str(pkg)],
            cwd=str(case_root),
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {
            "ok": False,
            "observed": "gate-error",
            "reason": type(exc).__name__,
            "rc": None,
            "verdict": "none",
            "out": "",
        }
    out = proc.stdout.decode("utf-8", "replace")
    rc = proc.returncode
    rule_lines, fails, verdict = _selftest_parse_output(out)
    iso_ok, iso_detail = _selftest_isolation(
        work_root,
        case_root,
        log_path,
        fixtures_root,
        allowed=(audit_dir.resolve(), Path(gate_path).resolve()),
    )
    ok = (
        rc == 1
        and verdict == "DEFECT"
        and len(rule_lines) == len(_SELFTEST_RULES)
        and sorted(rule_lines) == sorted(_SELFTEST_RULES)
        and fails == [expected]
        and iso_ok
    )
    return {
        "ok": ok,
        "observed": ",".join(sorted(set(fails))) if fails else "none",
        "reason": ""
        if ok
        else _selftest_reason(rc, verdict, rule_lines, fails, expected, iso_ok, iso_detail),
        "rc": rc,
        "verdict": verdict,
        "out": out,
    }


def _selftest_emit(out, case_no, cls, fixture, expected, observed, ok, detail=""):
    line = "selftest case=%d class=%s fixture=%s expected=%s observed=%s verdict=%s" % (
        case_no,
        cls,
        fixture,
        expected,
        observed,
        "pass" if ok else "fail",
    )
    if not ok and detail:
        line += " detail=%s" % _selftest_norm(detail).replace(" ", "-").replace(",", ".")
    out.write(line + "\n")


def run_selftest(gate_path, fixtures_root=None, work_root=None, out=None):
    """Run the ten graded cases; return 0 iff failures == 0."""
    out = out or sys.stdout
    gate_path = Path(gate_path).resolve()
    script_dir = Path(__file__).resolve().parent
    fixtures_root = (
        Path(fixtures_root).resolve()
        if fixtures_root is not None
        else script_dir / "fixtures" / "claim-package"
    )

    failures = 0
    created = False
    if work_root is None:
        work_root = Path(
            tempfile.mkdtemp(prefix="claim-pkg-selftest-", dir=os.environ.get("TMPDIR") or None)
        )
        created = True
    else:
        work_root = Path(work_root).resolve()
        work_root.mkdir(parents=True, exist_ok=True)

    try:
        defects = []
        if fixtures_root.is_dir():
            defects = sorted(
                p for p in fixtures_root.iterdir() if p.is_dir() and p.name.startswith("defect-")
            )
        if not fixtures_root.is_dir():
            hard_problem = "fixtures-absent"
        elif not gate_path.is_file():
            hard_problem = "gate-absent"
        elif len(defects) != 9:
            hard_problem = "fixtures=%d" % len(defects)
        else:
            hard_problem = None

        index_map = _selftest_read_index(fixtures_root) if fixtures_root.is_dir() else {}
        before = _selftest_tree_digest(fixtures_root) if fixtures_root.is_dir() else []

        audit_dir = work_root / "audit"
        audit_dir.mkdir(exist_ok=True)
        (audit_dir / "sitecustomize.py").write_text(_SELFTEST_AUDIT, encoding="utf-8")

        results = []
        if hard_problem:
            for case_no, (_aliases, rule) in enumerate(_SELFTEST_CLASSES, start=1):
                results.append(
                    {
                        "case": case_no,
                        "fixture": "-",
                        "expected": rule,
                        "observed": hard_problem,
                        "ok": False,
                        "detail": hard_problem,
                    }
                )
        else:
            for case_no, fixture_dir in enumerate(defects, start=1):
                expected, err = _selftest_expected_rule(fixture_dir, index_map)
                case_dir = work_root / ("case-%02d-%s" % (case_no, fixture_dir.name))
                if err:
                    results.append(
                        {
                            "case": case_no,
                            "fixture": fixture_dir.name,
                            "expected": err.replace("expected-", "unresolved"),
                            "observed": err,
                            "ok": False,
                            "detail": err,
                        }
                    )
                    continue
                graded = _selftest_grade(
                    gate_path,
                    fixture_dir,
                    case_dir,
                    audit_dir,
                    expected,
                    fixtures_root,
                    work_root,
                )
                results.append(
                    {
                        "case": case_no,
                        "fixture": fixture_dir.name,
                        "expected": expected,
                        "observed": graded["observed"],
                        "ok": graded["ok"],
                        "detail": graded["reason"],
                    }
                )

        # The canonical fixture bytes must not be touched by any case.
        after = _selftest_tree_digest(fixtures_root) if fixtures_root.is_dir() else []
        if before != after:
            for row in results:
                row["ok"] = False
                row["detail"] = "fixtures-mutated"

        for row in results:
            _selftest_emit(
                out,
                row["case"],
                "defect",
                row["fixture"],
                row["expected"],
                row["observed"],
                row["ok"],
                row["detail"],
            )
            if not row["ok"]:
                failures += 1

        # Case 10: the degenerate always-pass control must be rejected on all nine.
        control_dir = work_root / "control"
        control_dir.mkdir(exist_ok=True)
        control_gate = control_dir / "always-pass.py"
        control_gate.write_text(_SELFTEST_DEGENERATE, encoding="utf-8")
        accepted = 0
        clean = 0
        replayed = 0
        if not hard_problem:
            for case_no, fixture_dir in enumerate(defects, start=1):
                expected, err = _selftest_expected_rule(fixture_dir, index_map)
                if err:
                    replayed += 1
                    accepted += 1
                    continue
                case_dir = control_dir / ("case-%02d-%s" % (case_no, fixture_dir.name))
                graded = _selftest_grade(
                    control_gate,
                    fixture_dir,
                    case_dir,
                    audit_dir,
                    expected,
                    fixtures_root,
                    work_root,
                )
                replayed += 1
                if graded["ok"]:
                    accepted += 1
                if graded["rc"] == 0 and graded["verdict"] == "WELL-FORMED":
                    clean += 1
        control_ok = (not hard_problem) and replayed == 9 and accepted == 0 and clean == 9
        observed_control = (
            "rejected-%d/%d" % (replayed - accepted, replayed) if replayed else "not-replayed"
        )
        control_detail = ""
        if not control_ok:
            control_detail = (
                hard_problem or "accepted=%d conforming=%d" % (accepted, clean)
            )
        _selftest_emit(
            out,
            10,
            "degenerate",
            "always-pass",
            "reject",
            observed_control,
            control_ok,
            control_detail,
        )
        if not control_ok:
            failures += 1

        out.write("selftest cases=10 failures=%d\n" % failures)
        return 0 if failures == 0 else 1
    finally:
        if created:
            shutil.rmtree(work_root, ignore_errors=True)


def _selftest_main(argv):
    gate = None
    fixtures = None
    work = None
    args = list(argv[1:])
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--gate" and i + 1 < len(args):
            gate = args[i + 1]
            i += 2
        elif arg == "--fixtures" and i + 1 < len(args):
            fixtures = args[i + 1]
            i += 2
        elif arg == "--work" and i + 1 < len(args):
            work = args[i + 1]
            i += 2
        elif arg in ("-h", "--help"):
            sys.stderr.write(
                "usage: %s [--gate PATH] [--fixtures DIR] [--work DIR]\n" % Path(argv[0]).name
            )
            return 0
        else:
            sys.stderr.write("selftest: unknown argument %r\n" % arg)
            return 2
    if gate is None:
        gate = Path(__file__).resolve().parent / "claim-package-check.py"
    try:
        return run_selftest(gate, fixtures, work)
    except BrokenPipeError:
        return 1


# Standalone entry.  Pasted into claim-package-check.py the gate's own main()
# (and its selftest_dispatch) is already defined, so this guard stays inert and
# the gate owns argv; run this file directly and the guard drives the ten cases.
if __name__ == "__main__" and not any(
    name in globals() for name in ("selftest_dispatch", "main")
):
    sys.exit(_selftest_main(sys.argv))
