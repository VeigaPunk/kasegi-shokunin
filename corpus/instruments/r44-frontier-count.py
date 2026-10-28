#!/usr/bin/env python3
"""r44-frontier-count.py — the round-44 coverage counter (C2), table-aware, with a selftest.

WHY THIS INSTRUMENT EXISTS
    The frozen C2 counter recorded in `.ufo/waves/round-44/claims.json` is

        grep -cE '^\\| F[0-9]+ \\| admitted \\|' corpus/README.md

    The frontier table's shape is `| F<NN> | <title> | <status> | <knowledge> |
    <sources> | <note> |` — the status is the THIRD cell, not the second.  The
    frozen regex therefore prints `0` at the frozen base AND `0` after the
    round-44 admission: it measures nothing and cannot separate the two
    states (`.ufo/waves/round-44/controls/c2-frozen-counter-replay.txt`).  A
    counter that reads 0 in both worlds is a defective instrument, not a
    measurement, so this counter measures the SAME declared predicate — the
    number of frontier rows whose status cell is exactly `admitted` — and the
    SAME target value (26).

    The target is not moved by this instrument: at the frozen base the same
    count is 25, one short of 26, so a do-nothing control cannot reach the
    target.  The frozen counter string stays recorded, unchanged, in the
    claims file and in the report.

    Round 45 adds `--selftest` (round-44 spot-check §6 item 3): the counter is
    graded on fixture READMEs, including the second-cell shape the dead frozen
    regex assumed, and a set of mutated variants of the counting and verdict
    logic must each be rejected, so the instrument is a gate that can fail and
    not only a probe.

USAGE
    python3 corpus/instruments/r44-frontier-count.py --root TREE [--expect N] [--ids]
    python3 corpus/instruments/r44-frontier-count.py --selftest [--work DIR]

    --root      tree to count (an exported lane tree, or the lane checkout)
    --expect    when given, the counted value must equal it, else exit 1
    --ids       also print the counted row ids
    --selftest  grade the counter on fixture READMEs and mutants; --root is not
                needed; exit 0 iff no case failed and every mutant was rejected
    --work      directory for the selftest fixtures (default: a fresh temporary
                directory, removed afterwards; an explicit DIR is kept)

OUTPUT
    frontier rows=<n> admitted=<k>
    frontier duplicate-ids=<ids> verdict=DEFECT exit=1
    frontier expected=<N> admitted=<k> verdict=SHORT exit=1
    (selftest) one `case ...` line per check, then
    mutants=<k> rejected=<k>
    selftest cases=<N> failures=<F>
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Callable, Iterable, Sequence

ROW_RX = re.compile(r"^\| F\d+ \|")

Counter = Callable[[Iterable[str]], "tuple[int, int, list[str]]"]
Evaluator = Callable[..., "tuple[list[str], int]"]


def _is_admitted(cells: Sequence[str], line: str) -> bool:
    return cells[2] == "admitted"


def count_lines(
    lines: Iterable[str],
    *,
    row_rx: "re.Pattern[str]" = ROW_RX,
    is_admitted: Callable[[Sequence[str], str], bool] = _is_admitted,
) -> "tuple[int, int, list[str]]":
    """Count frontier rows and admitted rows in README lines.

    `row_rx` and `is_admitted` are selftest seams: the mutants pass altered
    versions; production callers use the defaults.
    """
    rows = 0
    admitted = 0
    ids: list[str] = []
    for line in lines:
        if not row_rx.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        rows += 1
        ids.append(cells[0])
        if is_admitted(cells, line):
            admitted += 1
    return rows, admitted, ids


def count_frontier(root: str) -> "tuple[int, int, list[str]]":
    readme = os.path.join(root, "corpus", "README.md")
    try:
        with open(readme, "r", encoding="utf-8") as fh:
            return count_lines(fh)
    except OSError as exc:
        print(f"r44-frontier-count: cannot read {readme}: {exc}", file=sys.stderr)
        return 0, 0, []


def evaluate(
    rows: int,
    admitted: int,
    ids: Sequence[str],
    expect: "int | None",
    show_ids: bool,
    *,
    check_dupes: bool = True,
    is_short: Callable[[int, int], bool] = lambda admitted, expect: admitted != expect,
) -> "tuple[list[str], int]":
    """Return (stdout lines, exit code) for a counted result."""
    out: list[str] = []
    if show_ids:
        out.append("frontier-ids=" + ",".join(ids))
    # R44W2Rev10 false-pass shape: a duplicated frontier row would inflate the
    # admitted count without adding a distinct holding. Duplicate ids are a
    # defect, never a pass.
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if check_dupes and dupes:
        out.append(f"frontier duplicate-ids={','.join(dupes)} verdict=DEFECT exit=1")
        return out, 1
    out.append(f"frontier rows={rows} admitted={admitted}")
    if expect is not None and is_short(admitted, expect):
        out.append(f"frontier expected={expect} admitted={admitted} verdict=SHORT exit=1")
        return out, 1
    return out, 0


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------

HEADER = "| id | topic | status | entry | sources | next |\n|---|---|---|---|---|---|\n"
PREFIX = "# corpus\n\nprose that mentions | F99 | admitted | in passing\n\n## Frontier\n\n"
TRAILER = (
    "\n## Other table\n\n| id | topic | status |\n|---|---|---|\n"
    "| S001 | a source | admitted |\n| M01 | a mistake | admitted |\n"
)


def _row(i: int, status: str = "admitted", note: str = "note") -> str:
    return f"| F{i:02d} | topic {i} | {status} | knowledge/k{i}.md | S{i:03d} | {note} |\n"


def _readme(rows: Sequence[str], header: str = HEADER) -> str:
    return PREFIX + header + "".join(rows) + TRAILER


def _cases() -> "list[dict]":
    """Each case: name, readme text (None = no README file), argv extras,
    expected exit code, expected stdout lines.  `file_only` cases exercise
    behaviour that exists only at the filesystem layer."""
    rows26 = [_row(i) for i in range(1, 27)]
    rows27 = [_row(i) for i in range(1, 28)]
    dup = rows26 + [_row(5)]
    second_cell = [
        f"| F{i:02d} | admitted | topic {i} | knowledge/k{i}.md | S{i:03d} | note |\n"
        for i in range(1, 4)
    ]
    return [
        dict(name="26-rows-26-admitted", text=_readme(rows26), args=[], rc=0,
             out=["frontier rows=26 admitted=26"]),
        dict(name="27-rows-27-admitted", text=_readme(rows27), args=[], rc=0,
             out=["frontier rows=27 admitted=27"]),
        dict(name="expect-27-on-27-passes", text=_readme(rows27), args=["--expect", "27"], rc=0,
             out=["frontier rows=27 admitted=27"]),
        dict(name="expect-27-on-26-short", text=_readme(rows26), args=["--expect", "27"], rc=1,
             out=["frontier rows=26 admitted=26",
                  "frontier expected=27 admitted=26 verdict=SHORT exit=1"]),
        dict(name="expect-26-on-26-passes", text=_readme(rows26), args=["--expect", "26"], rc=0,
             out=["frontier rows=26 admitted=26"]),
        dict(name="expect-26-on-27-also-mismatch", text=_readme(rows27), args=["--expect", "26"], rc=1,
             out=["frontier rows=27 admitted=27",
                  "frontier expected=26 admitted=27 verdict=SHORT exit=1"]),
        dict(name="duplicate-id-is-defect", text=_readme(dup), args=[], rc=1,
             out=["frontier duplicate-ids=F05 verdict=DEFECT exit=1"]),
        dict(name="duplicate-id-beats-expect", text=_readme(dup), args=["--expect", "27"], rc=1,
             out=["frontier duplicate-ids=F05 verdict=DEFECT exit=1"]),
        dict(name="queued-row-counted-not-admitted",
             text=_readme(rows26[:25] + [_row(26, status="queued")]), args=[], rc=0,
             out=["frontier rows=26 admitted=25"]),
        dict(name="header-and-separator-not-counted", text=_readme([]), args=[], rc=0,
             out=["frontier rows=0 admitted=0"]),
        dict(name="header-and-separator-with-one-row", text=_readme([_row(1)]), args=[], rc=0,
             out=["frontier rows=1 admitted=1"]),
        dict(name="status-in-second-cell-not-admitted", text=_readme(second_cell), args=[], rc=0,
             out=["frontier rows=3 admitted=0"]),
        dict(name="admitted-in-note-cell-not-admitted",
             text=_readme([_row(1), _row(2, status="queued", note="admitted later")]),
             args=[], rc=0, out=["frontier rows=2 admitted=1"]),
        dict(name="status-match-is-case-exact",
             text=_readme([_row(1), _row(2, status="Admitted")]), args=[], rc=0,
             out=["frontier rows=2 admitted=1"]),
        dict(name="ids-flag-prints-ids-first",
             text=_readme([_row(1), _row(2), _row(3, status="queued")]), args=["--ids"], rc=0,
             out=["frontier-ids=F01,F02,F03", "frontier rows=3 admitted=2"]),
        dict(name="missing-readme-is-zero-rows", text=None, args=[], rc=0,
             out=["frontier rows=0 admitted=0"], file_only=True),
        dict(name="missing-readme-with-expect-is-short", text=None, args=["--expect", "26"], rc=1,
             out=["frontier rows=0 admitted=0",
                  "frontier expected=26 admitted=0 verdict=SHORT exit=1"], file_only=True),
        dict(name="root-not-a-directory-exits-2", text=None, args=[], rc=2, out=[],
             file_only=True, root_is_file=True),
        # wave-2 survivors (R45W2RevFrontierSelftest S1-S8): --expect binds ADMITTED rows, never row count; status is the
        # whole third cell; commented, indented and short rows keep their behaviour; --ids still prints beside a defect.
        dict(name="expect-binds-admitted-not-rows-short",
             text=_readme(rows26[:25] + [_row(26, status="queued")]), args=["--expect", "26"], rc=1,
             out=["frontier rows=26 admitted=25",
                  "frontier expected=26 admitted=25 verdict=SHORT exit=1"]),
        dict(name="expect-binds-admitted-not-rows-pass",
             text=_readme(rows26[:25] + [_row(26, status="queued")]), args=["--expect", "25"], rc=0,
             out=["frontier rows=26 admitted=25"]),
        dict(name="status-not-admitted-is-not-admitted",
             text=_readme([_row(1), _row(2, status="not admitted")]), args=[], rc=0,
             out=["frontier rows=2 admitted=1"]),
        dict(name="status-admitted-with-suffix-is-not-admitted",
             text=_readme([_row(1), _row(2, status="admitted (partial)")]), args=[], rc=0,
             out=["frontier rows=2 admitted=1"]),
        dict(name="html-comment-row-not-counted",
             text=_readme([_row(1)]) + "<!-- | F02 | t | admitted | knowledge/k2.md | S002 | n | -->\n", args=["--ids"], rc=0,
             out=["frontier-ids=F01", "frontier rows=1 admitted=1"]),
        dict(name="indented-row-not-counted",
             text=_readme([_row(1)]) + "  | F02 | t | admitted | knowledge/k2.md | S002 | n |\n", args=["--ids"], rc=0,
             out=["frontier-ids=F01", "frontier rows=1 admitted=1"]),
        dict(name="three-cell-row-is-counted",
             text=_readme([_row(1)]) + "| F02 | t | admitted |\n", args=[], rc=0,
             out=["frontier rows=2 admitted=2"]),
        dict(name="two-cell-row-is-skipped",
             text=_readme([_row(1)]) + "| F02 | t |\n", args=[], rc=0,
             out=["frontier rows=1 admitted=1"]),
        dict(name="ids-printed-beside-duplicate-defect",
             text=_readme([_row(1), _row(1)]), args=["--ids"], rc=1,
             out=["frontier-ids=F01,F01", "frontier duplicate-ids=F01 verdict=DEFECT exit=1"]),
    ]


def _run_cli(root: str, args: Sequence[str]) -> "tuple[int, list[str]]":
    proc = subprocess.run(
        [sys.executable, os.path.abspath(__file__), "--root", root, *args],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout.splitlines()


def _run_memory(
    case: dict, counter: Counter, evaluator: Evaluator
) -> "tuple[int, list[str]]":
    expect = None
    show_ids = False
    a = case["args"]
    if "--expect" in a:
        expect = int(a[a.index("--expect") + 1])
    if "--ids" in a:
        show_ids = True
    rows, admitted, ids = counter(case["text"].splitlines(keepends=True))
    out, rc = evaluator(rows, admitted, ids, expect, show_ids)
    return rc, out


def _memory_cases() -> "list[dict]":
    return [c for c in _cases() if not c.get("file_only")]


def _memory_failures(counter: Counter, evaluator: Evaluator) -> "list[str]":
    bad = []
    for c in _memory_cases():
        rc, out = _run_memory(c, counter, evaluator)
        if rc != c["rc"] or out != c["out"]:
            bad.append(c["name"])
    return bad


def _mutants() -> "list[tuple[str, Counter, Evaluator]]":
    def counter(**kw: object) -> Counter:
        return lambda lines: count_lines(lines, **kw)  # type: ignore[arg-type]

    def nothing(lines: Iterable[str]) -> "tuple[int, int, list[str]]":
        return 0, 0, []

    def ev(**kw: object) -> Evaluator:
        return lambda rows, adm, ids, exp, show: evaluate(rows, adm, ids, exp, show, **kw)  # type: ignore[arg-type]

    return [
        ("status-compared-to-queued", counter(is_admitted=lambda c, l: c[2] == "queued"), evaluate),
        ("status-read-from-second-cell", counter(is_admitted=lambda c, l: c[1] == "admitted"), evaluate),
        ("row-regex-counts-any-table-row", counter(row_rx=re.compile(r"^\|")), evaluate),
        ("admitted-matched-anywhere-in-line", counter(is_admitted=lambda c, l: "admitted" in l), evaluate),
        ("every-row-counted-admitted", counter(is_admitted=lambda c, l: True), evaluate),
        ("status-match-case-insensitive", counter(is_admitted=lambda c, l: c[2].lower() == "admitted"), evaluate),
        ("do-nothing-counter", nothing, evaluate),
        ("duplicate-check-removed", count_lines, ev(check_dupes=False)),
        ("short-check-only-when-below", count_lines, ev(is_short=lambda a, e: a < e)),
        ("short-check-only-when-above", count_lines, ev(is_short=lambda a, e: a > e)),
    ]


def selftest(work: "str | None") -> int:
    own_tmp = work is None
    base = tempfile.mkdtemp(prefix="r44-frontier-selftest-") if own_tmp else work
    os.makedirs(base, exist_ok=True)
    cases = 0
    failures = 0

    def check(label: str, ok: bool, detail: str) -> None:
        nonlocal cases, failures
        cases += 1
        if not ok:
            failures += 1
        print(f"case {label}: {'ok' if ok else 'FAIL'} {detail}")

    try:
        # 1. CLI path: real subprocess against README fixtures, exit code + printed lines.
        for n, c in enumerate(_cases(), 1):
            root = os.path.join(base, f"{n:02d}-{c['name']}")
            os.makedirs(root, exist_ok=True)
            if c.get("root_is_file"):
                root_arg = os.path.join(root, "not-a-dir")
                with open(root_arg, "w", encoding="utf-8") as fh:
                    fh.write("x")
            else:
                root_arg = root
                if c["text"] is not None:
                    os.makedirs(os.path.join(root, "corpus"), exist_ok=True)
                    with open(os.path.join(root, "corpus", "README.md"), "w", encoding="utf-8") as fh:
                        fh.write(c["text"])
            rc, out = _run_cli(root_arg, c["args"])
            ok = rc == c["rc"] and out == c["out"]
            check(f"cli/{c['name']}", ok, f"exit={rc} stdout={out!r}" + ("" if ok else f" wanted exit={c['rc']} stdout={c['out']!r}"))

        # 2. In-memory path: the real functions must agree with every non-file case.
        bad = _memory_failures(count_lines, evaluate)
        for c in _memory_cases():
            check(f"memory/{c['name']}", c["name"] not in bad, "")

        # 3. Mutants: each altered variant must be rejected by the same grader.
        mutants = _mutants()
        rejected = 0
        for name, counter, evaluator in mutants:
            killed_by = _memory_failures(counter, evaluator)
            if killed_by:
                rejected += 1
            check(f"mutant/{name}", bool(killed_by), f"rejected_by={killed_by[:3]!r}" if killed_by else "SURVIVED")
        print(f"mutants={len(mutants)} rejected={rejected}")
        print(f"selftest cases={cases} failures={failures}")
        return 0 if failures == 0 else 1
    finally:
        if own_tmp:
            shutil.rmtree(base, ignore_errors=True)


def main(argv: "list[str]") -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--expect", type=int, default=None)
    ap.add_argument("--ids", action="store_true", help="also print the counted row ids")
    ap.add_argument("--selftest", action="store_true", help="grade the counter on fixtures and mutants")
    ap.add_argument("--work", default=None, help="selftest fixture directory (default: temporary)")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest(args.work)
    if args.root is None:
        ap.error("the following arguments are required: --root")

    if not os.path.isdir(args.root):
        print(f"r44-frontier-count: root {args.root} is not a directory", file=sys.stderr)
        return 2

    rows, admitted, ids = count_frontier(args.root)
    out, rc = evaluate(rows, admitted, ids, args.expect, args.ids)
    for line in out:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
